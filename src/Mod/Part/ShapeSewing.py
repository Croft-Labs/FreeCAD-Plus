# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bounded snapshot sewing for the existing Shape Builder; native OCCT geometry."""
import math
import re

import FreeCAD as App
import Part
from BasicShapes.ShapeReferences import require_current


def review(doc, choices, tolerance=1e-6, refine=False, solid=False):
    """Compute from copied root geometry, without editing the document or sources."""
    tolerance = float(tolerance)
    if not math.isfinite(tolerance) or not 1e-7 <= tolerance <= 1:
        raise ValueError("Choose a sewing tolerance from 0.0000001 to 1 mm.")
    if not choices:
        raise ValueError("Select faces, or one whole shell for solid creation.")
    faces, seen, provenance = [], set(), []
    for name, subs in choices:
        obj = doc.getObject(name)
        if (obj is None or not obj.isDerivedFrom("Part::Feature")
                or obj.getParentGeoFeatureGroup() is not None):
            raise ValueError("Select root Part shapes or whole root Bodies; nested members and Links are not supported.")
        require_current(obj)
        if obj.Shape.isNull() or not obj.Shape.isValid():
            raise ValueError("Repair the invalid source shape before continuing.")
        if solid:
            if len(choices) != 1 or subs or obj.Shape.ShapeType != "Shell":
                raise ValueError("Select one whole shell for solid creation.")
            shape = obj.Shape.copy()
            if not shape.isClosed():
                raise ValueError("The shell is open. Sew or repair its free boundaries before creating a solid.")
            provenance.append(name)
            break
        for sub in subs or ["Face" + str(i + 1) for i in range(len(obj.Shape.Faces))]:
            if not re.fullmatch(r"Face[1-9][0-9]*", sub):
                raise ValueError("Select faces, not edges, vertices or nested paths.")
            if (name, sub) in seen:
                continue
            seen.add((name, sub))
            faces.append(obj.Shape.getElement(sub).copy())
            provenance.append(name + "." + sub)
            if len(faces) > 500:
                raise ValueError("This review supports at most 500 faces.")
    if solid:
        shape = Part.makeSolid(shape)
        if shape.isNull() or not shape.isValid() or len(shape.Solids) != 1 or shape.Volume <= 0:
            raise ValueError("The closed shell did not produce one valid positive-volume solid.")
    else:
        if len(faces) < 2:
            raise ValueError("Select at least two faces.")
        shape = Part.makeCompound(faces)
        shape.sewShape(tolerance)
    if refine:
        shape = shape.removeSplitter()
    if shape.isNull() or not shape.isValid():
        raise ValueError("The requested operation produced an invalid shape; sources are unchanged.")
    free = []
    for index, edge in enumerate(shape.Edges, 1):
        owners = shape.ancestorsOfType(edge, Part.Face)
        if len(owners) == 1 and not edge.isSeam(owners[0]) and edge.Length > 1e-12:
            free.append("Edge" + str(index))
    single_shell = shape.ShapeType == "Shell"
    kind = "Valid solid" if solid else (
        "Closed shell" if single_shell and shape.isClosed() and not free else
        "Open shell" if single_shell else "Disconnected sheets")
    return shape, {"kind": kind, "shells": len(shape.Shells), "faces": len(shape.Faces),
                   "free_edges": free, "tolerance": tolerance, "sources": provenance,
                   "max_tolerance": shape.getTolerance(1), "solid": solid}


def create(doc, choices, tolerance=1e-6, refine=False, solid=False):
    if App.ActiveDocument != doc or doc.HasPendingTransaction or App.getActiveTransaction():
        raise ValueError("Activate the source document and finish the pending edit transaction.")
    shape, report = review(doc, choices, tolerance, refine, solid)
    doc.openTransaction("Solid from shell" if solid else "Sew faces")
    try:
        result = doc.addObject("Part::Feature", "Solid" if solid else "Shell")
        result.Shape = shape
        result.addProperty("App::PropertyStringList", "SourceFaces", "Snapshot",
                           "Source names at creation; this independent snapshot does not update with them.")
        result.SourceFaces = report["sources"]
        result.setEditorMode("SourceFaces", 1)
        if not solid:
            result.addProperty("App::PropertyLength", "SewingTolerance", "Snapshot")
            result.SewingTolerance = tolerance
            result.setEditorMode("SewingTolerance", 1)
        result.Label = report["kind"]
        doc.recompute()
        doc.commitTransaction()
        return result, report
    except Exception:
        doc.abortTransaction()
        raise


def builder_action(create_result=False):
    """Bridge the existing native task controls to the same reviewed operation."""
    import FreeCADGui as Gui
    from PySide import QtWidgets
    task = Gui.Control.activeTaskDialog()
    panels = task.getDialogContent() if task else []
    panel = next((p for p in panels if p.findChild(QtWidgets.QLabel, "sewingStatus")), None)
    if panel is None:
        raise ValueError("Open Shape Builder first.")
    status = panel.findChild(QtWidgets.QLabel, "sewingStatus")
    try:
        widget = status.parentWidget()
        doc = App.getDocument(widget.property("ownerDocument"))
        if doc is None or doc != App.ActiveDocument:
            raise ValueError("Activate the document where Shape Builder was opened.")
        solid = panel.findChild(QtWidgets.QRadioButton, "radioButtonSolidFromShell").isChecked()
        all_faces = panel.findChild(QtWidgets.QCheckBox, "checkFaces").isChecked() and not solid
        choices = []
        for selected in Gui.Selection.getSelectionEx():
            if selected.DocumentName != doc.Name:
                raise ValueError("Select shapes from the active document only.")
            choices.append((selected.ObjectName, [] if all_faces else list(selected.SubElementNames)))
        tolerance = panel.findChild(QtWidgets.QDoubleSpinBox, "sewingTolerance").value()
        refine = panel.findChild(QtWidgets.QCheckBox, "checkRefine").isChecked()
        if create_result:
            result, report = create(doc, choices, tolerance, refine, solid)
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(result)
        else:
            _, report = review(doc, choices, tolerance, refine, solid)
        text = "{}: {} shell(s), {} face(s), {} free edge(s).".format(
            report["kind"], report["shells"], report["faces"], len(report["free_edges"]))
        if not solid:
            text += "\nRequested sewing tolerance: {:.7g} mm; result maximum tolerance: {:.7g} mm.".format(
                tolerance, report["max_tolerance"])
        if report["free_edges"]:
            text += "\nResult boundaries: " + ", ".join(report["free_edges"][:30])
            if len(report["free_edges"]) > 30:
                text += " ..."
        status.setText(text + "\nIndependent snapshot; source edits do not update this result.")
    except Exception as error:
        status.setText(str(error))
