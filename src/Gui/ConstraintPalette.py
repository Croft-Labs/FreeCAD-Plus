# SPDX-License-Identifier: LGPL-2.1-or-later
"""Contextual Sketcher actions using native constraints, diagnostics and transactions."""
from dataclasses import dataclass, field
import re
import FreeCAD as App
import FreeCADGui as Gui
import Sketcher
from freecad.gui import DesignSelection as Selection

DIMENSIONS = {"Distance", "DistanceX", "DistanceY", "Radius", "Diameter", "Angle",
              "AngleViaPoint", "Weight", "SnellsLaw"}
MESSAGES = {-1: "The native sketch solver did not converge.",
            -2: "The native sketch solver reports redundant constraints.",
            -3: "The native sketch solver reports conflicting constraints.",
            -4: "The native sketch solver reports an over-constrained sketch.",
            -5: "The native sketch solver reports malformed constraints."}


@dataclass
class Action:
    key: str
    label: str
    constraints: list = field(default_factory=list)
    reason: str = ""
    command: str = ""


def editing_sketch():
    view = Gui.activeDocument().getInEdit() if Gui.activeDocument() else None
    obj = view.Object if view else None
    return obj if obj and obj.isDerivedFrom("Sketcher::SketchObject") else None


def selected(sketch):
    """Use the full native selection, resolving occurrence paths without replacing them."""
    names = []
    for entry in Gui.Selection.getSelectionEx("*", 0):
        for sub in entry.SubElementNames or [""]:
            obj, _, element = Selection.resolve(entry.Object, sub)
            if obj != sketch or not element:
                return []
            if element not in names:
                names.append(element)
    return names


def _elements(sketch, names):
    edges, points, dimensions = [], [], []
    for name in names:
        match = re.fullmatch(r"(Edge|ExternalEdge|Vertex|Constraint)([1-9][0-9]*)", name)
        if name == "RootPoint":
            points.append((-1, 1))
        elif name in ("H_Axis", "V_Axis"):
            edges.append((-1 if name == "H_Axis" else -2, "Line"))
        elif match:
            kind, index = match.group(1), int(match.group(2)) - 1
            if kind == "Constraint":
                if index >= sketch.ConstraintCount or sketch.Constraints[index].Type not in DIMENSIONS:
                    return None
                dimensions.append(index)
            elif kind == "Vertex":
                points.append(tuple(sketch.getGeoVertexIndex(index)))
            else:
                if kind == "Edge":
                    geometry = sketch.Geometry[index]
                else:
                    geometry = sketch.getSubObject(name).Curve
                    index = -3 - index
                typename = geometry.TypeId
                family = next((value for value in ("Line", "Circle", "Ellipse", "Hyperbola", "Parabola", "BSpline")
                               if value in typename), "Other")
                edges.append((index, family))
        else:
            return None
    return edges, points, dimensions


def _same(a, b):
    keys = ("Type", "First", "FirstPos", "Second", "SecondPos", "Third", "ThirdPos")
    if all(getattr(a, key) == getattr(b, key) for key in keys):
        return True
    if a.Type == b.Type and a.Type in ("Equal", "Parallel", "Perpendicular", "Tangent", "Coincident"):
        return (a.First, a.FirstPos, a.Second, a.SecondPos) == (b.Second, b.SecondPos, b.First, b.FirstPos)
    return False


def _reason(sketch, additions):
    existing = [c for c in sketch.Constraints if c.IsActive and c.Driving]
    if any(_same(new, old) for new in additions for old in existing):
        return "This constraint already exists."
    # Fast exact contradictions; the native diagnostic also finds indirect ones.
    opposites = {"Horizontal": "Vertical", "Vertical": "Horizontal", "Parallel": "Perpendicular", "Perpendicular": "Parallel"}
    for new in additions:
        for old in existing:
            if old.Type == opposites.get(new.Type) and old.First == new.First and old.Second == new.Second:
                return "This conflicts with an existing constraint."
    if hasattr(sketch, "diagnoseConstraintAdditions"):
        status = sketch.diagnoseConstraintAdditions(additions)
        # Failure to converge is uncertain, and must not become a disabled action.
        if status in (-2, -3, -4, -5):
            return MESSAGES[status]
    return ""


def _expression(sketch, index):
    constraint = sketch.Constraints[index]
    paths = {"Constraints[%d]" % index}
    if constraint.Name:
        paths.add("Constraints." + constraint.Name)
    return any(path.lstrip(".") in paths and expression for path, expression in sketch.ExpressionEngine)


def actions(sketch, names):
    if not names:
        return []
    try:
        parsed = _elements(sketch, names)
    except (IndexError, ValueError, RuntimeError, AttributeError):
        return []
    if parsed is None:
        return []
    edges, points, dimensions = parsed
    result = []

    def add(key, label, specifications):
        constraints = [Sketcher.Constraint(*spec) for spec in specifications]
        reason = _reason(sketch, constraints)
        result.append(Action(key, label, constraints, reason))

    def dimension(key, label):
        command = "Sketcher_Constrain" + key
        reason = ""
        kinds = {key} if key not in ("Radius", "Diameter") else {"Radius", "Diameter"}
        chosen = {i for i, family in edges} | {i for i, pos in points}
        for constraint in sketch.Constraints:
            used = {i for i in (constraint.First, constraint.Second, constraint.Third) if i >= -2}
            if constraint.IsActive and constraint.Driving and used == chosen and constraint.Type in kinds:
                reason = "A driving dimension for this selection already exists."
        result.append(Action(key, label, reason=reason, command=command))

    if dimensions:
        if edges or points:
            return []
        for driving in (True, False):
            reason = ""
            if all(sketch.getDriving(index) == driving for index in dimensions):
                reason = "All selected dimensions already have this state."
            elif not driving and any(_expression(sketch, index) for index in dimensions):
                reason = "A selected dimension has a driving expression. Remove that expression explicitly before making it reference."
            elif driving and any(all(value < 0 for value in (sketch.Constraints[i].First,
                                    sketch.Constraints[i].Second, sketch.Constraints[i].Third)) for i in dimensions):
                reason = "A dimension on external geometry only cannot drive the sketch."
            result.append(Action("driving" if driving else "reference", "Make Driving" if driving else "Make Reference", reason=reason))
        return result
    ids = [index for index, family in edges]
    all_lines = edges and all(family == "Line" for _, family in edges)
    if edges and not points:
        if all(index >= 0 for index in ids):
            result.append(Action("construction", "Construction Geometry"))
            add("Block", "Block", [("Block", i) for i in ids])
        if all_lines:
            for kind in ("Horizontal", "Vertical"):
                add(kind, kind, [(kind, i) for i in ids])
            if len(ids) >= 2:
                add("Parallel", "Parallel", [("Parallel", a, b) for a, b in zip(ids, ids[1:])])
            if len(ids) == 2:
                add("Perpendicular", "Perpendicular", [("Perpendicular", *ids)])
            if len(ids) in (1, 2):
                dimension("Angle", "Angle")
            if len(ids) == 1:
                dimension("Distance", "Length")
                dimension("DistanceX", "Horizontal Distance")
                dimension("DistanceY", "Vertical Distance")
        if len(ids) >= 2 and len({family for _, family in edges}) == 1 and edges[0][1] not in ("BSpline", "Other") and all(i not in (-1, -2) for i in ids):
            add("Equal", "Equal", [("Equal", a, b) for a, b in zip(ids, ids[1:])])
        if len(ids) == 2:
            add("Tangent", "Tangent", [("Tangent", *ids)])
            if all(family in ("Circle", "Ellipse") for _, family in edges):
                add("Concentric", "Concentric", [("Coincident", ids[0], 3, ids[1], 3)])
        if len(ids) == 1 and edges[0][1] == "Circle":
            dimension("Radius", "Radius")
            dimension("Diameter", "Diameter")
    elif points and not edges:
        if len(points) >= 2:
            add("Coincident", "Coincident", [("Coincident", *a, *b) for a, b in zip(points, points[1:])])
        if len(points) == 2:
            for kind in ("Horizontal", "Vertical"):
                add(kind, kind, [(kind, *points[0], *points[1])])
            dimension("Distance", "Distance")
        if len(points) in (1, 2):
            dimension("DistanceX", "Horizontal Distance")
            dimension("DistanceY", "Vertical Distance")
        if len(points) == 3:
            add("Symmetric", "Symmetric", [("Symmetric", *points[0], *points[1], *points[2])])
    elif len(points) == 1 and len(edges) == 1:
        add("PointOnObject", "Point on Object", [("PointOnObject", *points[0], ids[0])])
    elif len(points) == 2 and len(edges) == 1 and all_lines:
        add("Symmetric", "Symmetric", [("Symmetric", *points[0], *points[1], ids[0])])
    # Native safeguards prohibit relations involving only fixed external geometry.
    if ids and all(i < 0 for i in ids) and all(i < 0 for i, pos in points):
        for action in result:
            action.reason = action.reason or "External geometry and sketch axes cannot be constrained alone."
    return result


def report(sketch, status):
    if not status:
        return ""
    message = MESSAGES.get(status, "The native sketch solver returned error %s." % status)
    details = []
    for name in ("ConflictingConstraints", "RedundantConstraints", "MalformedConstraints"):
        values = getattr(sketch, name, [])
        if values:
            details.append(name + ": " + ", ".join(map(str, values)))
    text = " ".join([message] + details)
    App.Console.PrintError(text + "\n")
    Gui.getMainWindow().statusBar().showMessage(text, 15000)
    return text


def execute(sketch, names, key):
    """Revalidate live inputs. API failures abort; invalid Make Driving commits."""
    if editing_sketch() != sketch or selected(sketch) != names:
        raise ValueError("The sketch selection changed. Choose the action again.")
    action = next((item for item in actions(sketch, names) if item.key == key), None)
    if action is None or action.reason:
        raise ValueError(action.reason if action else "This action no longer applies to the selection.")
    if action.command:
        command = Gui.Command.get(action.command)
        if not command or not command.isActive():
            raise ValueError("The native constraint command is unavailable in the current task.")
        before = sketch.ConstraintCount
        command.run()
        return sketch.ConstraintCount > before, ""
    edges, points, dimensions = _elements(sketch, names)
    doc = sketch.Document
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current sketch operation first.")
    doc.openTransaction(action.label)
    try:
        status = None
        if key == "construction":
            # Any construction member (including a mixed selection) means normal first.
            target = not any(sketch.getConstruction(index) for index, _ in edges)
            for index, _ in edges:
                sketch.setConstruction(index, target)
        elif key in ("driving", "reference"):
            if hasattr(sketch, "setDrivingBatch"):
                status = sketch.setDrivingBatch(dimensions, key == "driving")
            else:
                # Source-overlay compatibility only; packaged acceptance requires
                # the native batch method (one solve after all conversions).
                for index in dimensions:
                    sketch.setDriving(index, key == "driving")
        else:
            sketch.addConstraint(action.constraints)
        if status is None:
            status = sketch.solve()
        # Making dimensions reference can remove one conflict while another
        # remains. Keep that useful conversion available for individual diagnosis.
        if status and key not in ("driving", "reference"):
            raise ValueError(MESSAGES.get(status, "Native sketch solver error %s" % status))
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        sketch.solve()
        raise
    Selection.finish_operation()
    return True, report(sketch, status)
