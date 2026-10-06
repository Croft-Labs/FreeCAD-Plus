# SPDX-License-Identifier: LGPL-2.1-or-later
"""Design selection policy shared by native gates, toolbars and task commands.

No saved selection snapshots: commands which preserve entity identity may elect
not to clear selection. Topology-changing commands retain native cleanup.
"""
import math
import re

PARAM = "User parameter:BaseApp/Preferences/DesignSelection"
CATEGORIES = ("Planes", "Bodies", "Surfaces", "Faces", "Edges", "Curves", "Points", "Vertices")
ALL = (1 << len(CATEGORIES)) - 1
MODES = ("Single Curve", "Connected Curves", "Tangent Curves")
ENDPOINT_TOLERANCE = 1e-7  # mm, never screen-space proximity
TANGENT_ANGLE = 1e-5  # radians; absolute endpoint tangent, orientation independent


def parameters():
    import FreeCAD as App
    return App.ParamGet(PARAM)


def active():
    return parameters().GetBool("Active", False)


def persistent():
    return active() and parameters().GetBool("Persistent", True)


def finish_operation():
    """For identity-preserving commands only; never replay stale subelement IDs."""
    if not persistent():
        import FreeCADGui as Gui
        Gui.Selection.clearSelection()


def clear_after_escape(guard=None):
    """Let the native handler cancel/deselect first, then enforce explicit clear.

    Clearing before Sketcher receives Escape makes it see an empty selection and
    exit edit instead. This also avoids replacing an active collector's handler.
    """
    import FreeCAD as App
    import FreeCADGui as Gui
    from PySide import QtCore
    document = App.ActiveDocument
    def finish():
        if App.ActiveDocument == document and (guard is None or guard()):
            Gui.Selection.clearSelection()
    # Native edit teardown may queue a parent selection during the same key event.
    QtCore.QTimer.singleShot(0, lambda: QtCore.QTimer.singleShot(0, finish))


def resolve(root, path):
    """Resolve geometry ownership without replacing the stored occurrence path."""
    path = path or ""
    prefix, _, element = path.rpartition(".")
    # Native mapped picks append geometry identity (e.g. ;g1.edge1) after
    # the occurrence/object path. That token is not an owning container.
    tokens = prefix.split(".") if prefix else []
    while tokens and tokens[-1].startswith(";"):
        tokens.pop()
    prefix = ".".join(tokens)
    prefix = prefix + "." if prefix else ""
    obj = root.getSubObject(prefix, 1) if prefix else root
    if obj is not None:
        obj = obj.getLinkedObject(True)
        if obj.isDerivedFrom("Sketcher::SketchObject"):
            # Native NoResolve picks may use lower-case element-map names. Keep
            # occurrence prefixes unchanged while interpreting the sketch element.
            for token in ("ExternalEdge", "ExternalVertex", "Constraint", "Vertex", "Edge", "RootPoint", "H_Axis", "V_Axis"):
                if element.lower().startswith(token.lower()):
                    element = token + element[len(token):]
                    break
    return obj, prefix, element


def category(root, path):
    obj, _, element = resolve(root, path)
    if obj is None:
        return None
    derived = obj.isDerivedFrom
    # Sketch identity wins even if the native owner is a PartDesign Body.
    if derived("Sketcher::SketchObject"):
        if element.startswith(("Vertex", "ExternalVertex")) or element == "RootPoint":
            return "Points"
        if element.startswith("Constraint"):
            return None  # annotations are not geometric entity filters
        return "Curves"
    if derived("App::Plane") or derived("PartDesign::Plane"):
        return "Planes"
    if derived("App::Origin") or derived("App::Point") or derived("PartDesign::Point"):
        return "Points"
    if derived("App::Line") or derived("PartDesign::Line"):
        return "Curves"
    shape = getattr(obj, "Shape", None)
    body = derived("PartDesign::Body") or derived("PartDesign::Feature")
    if not body:
        owner = obj.getParentGeoFeatureGroup()
        body = owner is not None and owner.isDerivedFrom("PartDesign::Body")
    if shape is not None and not shape.isNull():
        body = body or bool(shape.Solids)
        if body:
            if element.startswith("Face"):
                return "Faces"
            if element.startswith("Edge"):
                return "Edges"
            if element.startswith("Vertex"):
                return "Vertices"
            return "Bodies"
        if shape.Faces:
            return "Surfaces"
        if element.startswith("Vertex") or not shape.Edges:
            return "Points"
        return "Curves"
    return "Bodies" if body else None


def allows(root, path):
    """Native Selection.cpp calls this before its independent command gate."""
    if parameters().GetBool("LayerVisibilityActive", False):
        from freecad.gui import DesignLayers
        obj, _, _ = resolve(root, path)
        if obj is not None and DesignLayers.eligible(obj) and not DesignLayers.visible(obj):
            return False
    if not active():
        return True
    mask = parameters().GetInt("Categories", ALL) & ALL
    if mask == ALL:
        return True
    kind = category(root, path)
    # Containers and constraint annotations remain subject to their native gate.
    return kind is None or bool(mask & (1 << CATEGORIES.index(kind)))


def _distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def connected_indices(segments, seed, tangent=False):
    """Traverse endpoint records (two (point,tangent) pairs or None for closed).

    Connected takes every branch. Tangent stops at junctions with more than two
    incident curves, including branches not tangent to the incoming curve.
    Closed periodic curves are isolated: their parameter seam is not a junction.
    """
    if seed not in segments:
        return []
    result, pending = {seed}, [seed]
    while pending:
        current = pending.pop()
        for point, direction in segments[current] or ():
            neighbors = []
            for index, ends in segments.items():
                if index == current:
                    continue
                for other, other_direction in ends or ():
                    if _distance(point, other) <= ENDPOINT_TOLERANCE:
                        neighbors.append((index, other_direction))
                        break
            if tangent and len(neighbors) != 1:
                continue
            for index, other_direction in neighbors:
                if tangent:
                    if direction is None or other_direction is None:
                        continue
                    dot = abs(sum(a * b for a, b in zip(direction, other_direction)))
                    if dot < math.cos(TANGENT_ANGLE):
                        continue
                if index not in result:
                    result.add(index)
                    pending.append(index)
    return sorted(result)


def _endpoint(edge, parameter):
    point = edge.valueAt(parameter)
    try:
        direction = edge.tangentAt(parameter)
        direction.normalize()
        tangent = tuple(direction)
    except (RuntimeError, ValueError):
        tangent = None
    return tuple(point), tangent


def chain_paths(root, path, mode):
    if mode == 0 or mode not in (1, 2):
        return [path]
    obj, prefix, element = resolve(root, path)
    match = re.fullmatch(r"Edge([1-9][0-9]*)", element)
    if obj is None or match is None or category(root, path) not in ("Curves", "Edges"):
        return [path]
    if obj.isDerivedFrom("Sketcher::SketchObject"):
        # Shape.Edges excludes construction geometry and is NOT a sketch index.
        edges = {}
        for index, geometry in enumerate(obj.Geometry, 1):
            shape = geometry.toShape()
            if shape.ShapeType == "Edge":
                edges[index] = shape
    else:
        edges = dict(enumerate(obj.Shape.Edges, 1))
    segments = {}
    for index, edge in edges.items():
        segments[index] = None if edge.isClosed() else (
            _endpoint(edge, edge.FirstParameter), _endpoint(edge, edge.LastParameter))
    token = "edge" if path.rpartition(".")[2].startswith("edge") else "Edge"
    return [prefix + token + "%d" % index for index in
            connected_indices(segments, int(match.group(1)), tangent=mode == 2)]
