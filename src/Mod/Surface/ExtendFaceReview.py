# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bounded review and native associative Surface::Extend creation."""
import hashlib
import math
import re

import FreeCAD as App
from BasicShapes.ShapeReferences import require_current
from freecad.gui.DependencyInspector import identity, resolve


def tr(text):
    return App.Qt.translate("ExtendFaceReview", text)


class Input:
    def __init__(self, obj, face):
        self.key, self.face = identity(obj), face
        self.signature = self.snapshot(obj)
        self.label = "{} [{}#{}.{}]".format(obj.Label, obj.Document.Name, obj.Name, face)

    def snapshot(self, obj):
        if (not obj.isDerivedFrom("Part::Feature") or obj.getParentGeoFeatureGroup() is not None
                or not re.fullmatch(r"Face[1-9][0-9]*", self.face)):
            raise ValueError(tr("Select one face on a root Part shape or Body. Nested paths and Links are not supported."))
        require_current(obj)
        shape = obj.Shape
        if shape.isNull() or not shape.isValid() or len(shape.Faces) > 200:
            raise ValueError(tr("Choose a valid source with at most 200 faces."))
        face = shape.getElement(self.face)
        if face.ShapeType != "Face":
            raise ValueError(tr("Select one face."))
        return hashlib.sha256(shape.exportBrepToString().encode("utf-8")).hexdigest()

    def object(self):
        obj = resolve(self.key)
        if self.snapshot(obj) != self.signature:
            raise ValueError(tr("The source changed. Close this review and select the face again."))
        return obj


def ready(ref):
    import FreeCADGui as Gui
    source = ref.object()
    if (source.Document != App.ActiveDocument or Gui.Control.activeDialog()
            or Gui.activeDocument().getInEdit() or source.Document.HasPendingTransaction
            or App.getActiveTransaction()):
        raise ValueError(tr("Activate the source document and finish its edit, task or transaction first."))
    return source


def settings(values):
    values = dict(values)
    for prop in ("ExtendUNeg", "ExtendUPos", "ExtendVNeg", "ExtendVPos"):
        value = float(values[prop])
        if not math.isfinite(value) or not -0.5 <= value <= 10:
            raise ValueError(tr("Extension must be between -50% and 1000% of the source parameter span."))
        values[prop] = value
    for direction in ("U", "V"):
        if 1 + values["Extend" + direction + "Neg"] + values["Extend" + direction + "Pos"] <= 0:
            raise ValueError(tr("The extended U and V domains must remain nonempty."))
    values["Tolerance"] = float(values["Tolerance"])
    if not math.isfinite(values["Tolerance"]) or not 1e-7 <= values["Tolerance"] <= 10:
        raise ValueError(tr("Fitting tolerance must be between 0.0000001 and 10 mm."))
    for prop in ("SampleU", "SampleV"):
        if isinstance(values[prop], bool) or int(values[prop]) != values[prop] or not 4 <= values[prop] <= 64:
            raise ValueError(tr("This review supports 4 to 64 samples per direction."))
        values[prop] = int(values[prop])
    return {prop: values[prop] for prop in (
        "ExtendUNeg", "ExtendUPos", "ExtendVNeg", "ExtendVPos", "Tolerance", "SampleU", "SampleV")}


def configure(result, source, face, values):
    result.Face = (source, [face])
    result.ExtendUSymetric = result.ExtendVSymetric = False
    for prop, value in values.items():
        setattr(result, prop, value)


def checked_shape(result):
    shape = result.Shape
    if ("Invalid" in result.State or "Touched" in result.State or shape.isNull()
            or not shape.isValid() or len(shape.Faces) != 1 or shape.Solids):
        raise ValueError(tr("Native surface extension failed. Reduce the extension or revise the fitting settings; no result was accepted."))
    return shape.copy()


def probe(ref, values):
    source = ready(ref)
    values = settings(values)
    owner = source.Document
    scratch = App.newDocument("ExtendFacePreview", hidden=True, temp=True)
    try:
        clone = scratch.addObject("Part::Feature", "Source")
        clone.Shape = source.Shape.copy()
        result = scratch.addObject("Surface::Extend", "Extend")
        configure(result, clone, ref.face, values)
        scratch.recompute()
        return {"input": ref, "values": values, "shape": checked_shape(result)}
    finally:
        App.closeDocument(scratch.Name)
        if App.ActiveDocument != owner:
            App.setActiveDocument(owner.Name)


def create(preview):
    if preview is None:
        raise ValueError(tr("Preview the surface before creating it."))
    ref = preview["input"]
    source = ready(ref)
    checked = probe(ref, preview["values"])
    doc = source.Document
    visible = source.Visibility
    doc.openTransaction(tr("Create reviewed extended surface"))
    try:
        result = doc.addObject("Surface::Extend", "Extend")
        configure(result, source, ref.face, checked["values"])
        doc.recompute()
        shape = checked_shape(result)
        if abs(shape.Area - checked["shape"].Area) > 1e-6 * max(1., shape.Area):
            raise ValueError(tr("The created surface did not match the preview."))
        result.Label = tr("Extended surface")
        source.Visibility = visible
        doc.commitTransaction()
        return result
    except Exception:
        doc.abortTransaction()
        if source.Visibility != visible:
            source.Visibility = visible
        raise
