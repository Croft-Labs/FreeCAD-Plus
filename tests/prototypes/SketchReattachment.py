# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only cross-part reference adapter; direct reattachment uses the installed core."""
import FreeCAD as App
import Part
from BasicShapes.ShapeReferences import linked_shape, update_placement_support, validate_link
from SketchSupport import reattach_planar, preview_planar, _validate, _reattach_planar


class PlanarSupport:
    """Test-only associative world-to-local reference; module needed on restore."""

    def __init__(self, obj, source):
        obj.addProperty("App::PropertyLinkSub", "Source", "Prototype")
        obj.addProperty("App::PropertyLinkList", "PlacementSupport", "Prototype")
        obj.Source = source
        obj.Proxy = self

    def execute(self, obj):
        obj.Shape = Part.Shape()
        update_placement_support(obj, [obj.Source])
        if not obj.Source or not obj.Source[0]:
            raise ValueError("Planar reference source is missing; select a replacement")
        validate_link(obj, obj.Source[0])
        shape = linked_shape(obj.Source)
        if len(shape.Faces) != 1 or not isinstance(shape.Faces[0].Surface, Part.Plane):
            raise ValueError("Reference requires one planar face")
        parent = obj.getGlobalPlacement().multiply(obj.Placement.inverse())
        shape.transformShape(parent.inverse().toMatrix())
        obj.Placement = shape.Placement
        obj.Shape = shape

    def dumps(self):
        return None

    def loads(self, state):
        pass


def reattach_with_reference(sketch, source, face_name, policy="preserve-local"):
    """Create an explicit reference and reattach as one native undo transaction."""
    _validate(sketch, source, face_name, policy, allow_cross=True)
    doc = sketch.Document
    parent = sketch.getParentGeoFeatureGroup()
    doc.openTransaction("Create planar reference and reattach sketch")
    try:
        reference = doc.addObject("Part::FeaturePython", "PlanarReference")
        if parent:
            parent.addObject(reference)
        PlanarSupport(reference, (source, [face_name]))
        doc.recompute()
        _reattach_planar(sketch, reference, "Face1", policy, own_transaction=False)
        doc.commitTransaction()
        return reference
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise
