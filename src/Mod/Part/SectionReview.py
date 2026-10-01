# SPDX-License-Identifier: LGPL-2.1-or-later
"""Review associative intersection curves using the native Part::Section feature."""
import hashlib
import FreeCAD as App
from BasicShapes.ShapeReferences import require_current
from freecad.gui.DependencyInspector import identity, resolve


def tr(text):
    return App.Qt.translate("SectionReview", text)


class Input:
    def __init__(self, obj):
        self.key = identity(obj)
        self.signature = snapshot(obj)
        self.label = "{} [{}]".format(obj.Label, obj.Name)

    def object(self):
        obj = resolve(self.key)
        if snapshot(obj) != self.signature:
            raise ValueError(tr("An input changed. Capture it again and preview the new intersection."))
        return obj


def snapshot(obj):
    if not obj.isDerivedFrom("Part::Feature") or obj.getParentGeoFeatureGroup() is not None:
        raise ValueError(tr("Select a whole root Part shape or whole root Body. Nested members and Links are not supported by this review."))
    require_current(obj)
    shape = obj.Shape
    if shape.isNull() or not shape.isValid() or not shape.Faces:
        raise ValueError(tr("Choose a valid shape containing faces; edges and empty shapes cannot define this section."))
    if len(shape.Faces) > 200:
        raise ValueError(tr("This review supports up to 200 faces per input."))
    return hashlib.sha256(shape.exportBrepToString().encode("utf-8")).hexdigest()


def ready(first, second):
    import FreeCADGui as Gui
    a, b = first.object(), second.object()
    if a == b or a.Document != b.Document:
        raise ValueError(tr("Choose two different shapes in the same document."))
    doc = a.Document
    if (App.ActiveDocument != doc or Gui.Control.activeDialog()
            or Gui.activeDocument().getInEdit() or doc.HasPendingTransaction or App.getActiveTransaction()):
        raise ValueError(tr("Activate the input document and finish its edit, task or transaction first."))
    return a, b


def probe(first, second, approximation=False):
    """Recompute native Section on copied BReps in a hidden temporary document."""
    a, b = ready(first, second)
    owner = a.Document
    scratch = App.newDocument("SectionReviewPreview", hidden=True, temp=True)
    try:
        copies = []
        for source in (a, b):
            clone = scratch.addObject("Part::Feature", "Operand")
            clone.Shape = source.Shape.copy()
            copies.append(clone)
        result = scratch.addObject("Part::Section", "Section")
        result.Base, result.Tool = copies
        result.Approximation = bool(approximation)
        scratch.recompute()
        if "Invalid" in result.State or "Touched" in result.State:
            raise ValueError(tr("Native section computation failed. No source objects were changed."))
        shape = result.Shape.copy()
        edges = len(shape.Edges) if not shape.isNull() else 0
        vertices = len(shape.Vertexes) if not shape.isNull() else 0
        return {"first": first, "second": second, "approximation": bool(approximation),
                "shape": shape, "edges": edges, "vertices": vertices,
                "length": shape.Length if edges else 0.}
    finally:
        App.closeDocument(scratch.Name)
        if App.ActiveDocument != owner:
            App.setActiveDocument(owner.Name)


def create(preview):
    if preview is None:
        raise ValueError(tr("Preview the intersection before creating it."))
    first, second = preview["first"], preview["second"]
    a, b = ready(first, second)
    checked = probe(first, second, preview["approximation"])
    if not checked["edges"]:
        raise ValueError(tr("No intersection curves were found. No feature was created."))
    doc = a.Document
    visibility = [(obj, obj.Visibility) for obj in (a, b)]
    doc.openTransaction(tr("Create reviewed intersection curves"))
    try:
        result = doc.addObject("Part::Section", "Section")
        result.Base, result.Tool = a, b
        result.Approximation = checked["approximation"]
        doc.recompute()
        if ("Invalid" in result.State or "Touched" in result.State or not result.Shape.Edges
                or len(result.Shape.Edges) != checked["edges"]
                or abs(result.Shape.Length - checked["length"]) > 1e-6):
            raise ValueError(tr("The created intersection did not match the preview."))
        result.Label = tr("Intersection curves")
        result.ViewObject.LineColor = (0.1, 0.85, 0.25)
        result.ViewObject.LineWidth = 4.
        # Native Boolean view providers hide operands as Base/Tool are assigned.
        # Restore their reviewed visibility inside the same creation transaction.
        for obj, visible in visibility:
            obj.Visibility = visible
        doc.commitTransaction()
        return result
    except Exception:
        doc.abortTransaction()
        for obj, visible in visibility:
            if obj.Visibility != visible:
                obj.Visibility = visible
        raise
