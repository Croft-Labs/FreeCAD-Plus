# SPDX-License-Identifier: LGPL-2.1-or-later

"""Associative draft-angle curves on oriented, trimmed faces."""

import math
import FreeCAD as App
import Part
from .ShapeReferences import linked_shape, validate_link, update_placement_support, ReferenceError


def curve_tolerance(value):
    """Return millimetres, using the existing Part.makeIsocline distance limits."""
    quantity = App.Units.Quantity(value)
    if quantity.Unit not in (App.Units.Unit(), App.Units.Quantity("1 mm").Unit):
        raise ReferenceError("Curve tolerance must be a length (bare numbers are millimetres).")
    tolerance = quantity.Value
    if not math.isfinite(tolerance) or not 1e-7 <= tolerance <= 0.01:
        raise ReferenceError("Curve tolerance must be between 0.0000001 mm and 0.01 mm.")
    return tolerance


def reference_direction(link):
    if not link or not link[0]:
        raise ReferenceError("Select a direction plane, planar face, straight edge, or datum axis.")
    obj, subs = link
    if (not subs or not subs[0]) and obj.TypeId in (
        "PartDesign::Plane",
        "App::Plane",
        "PartDesign::Line",
        "App::Line",
    ):
        return obj.getGlobalPlacement().Rotation.multVec(App.Vector(0, 0, 1))
    shape = linked_shape(link)
    if shape.ShapeType == "Face" and shape.findPlane() is not None:
        u0, u1, v0, v1 = shape.ParameterRange
        return shape.normalAt((u0 + u1) / 2, (v0 + v1) / 2)
    if shape.ShapeType == "Edge" and isinstance(shape.Curve, (Part.Line, Part.LineSegment)):
        return shape.tangentAt(shape.FirstParameter)
    raise ReferenceError("Use a planar face or straight edge, or select a datum plane/axis.")


def resolved_direction(obj):
    if obj.DirectionMode == "Reference":
        validate_link(obj, obj.DirectionReference[0] if obj.DirectionReference else None)
        direction = reference_direction(obj.DirectionReference)
    elif obj.DirectionMode == "Custom vector":
        direction = App.Vector(obj.CustomDirection)
    else:
        direction = {
            "X axis": App.Vector(1, 0, 0),
            "Y axis": App.Vector(0, 1, 0),
            "Z axis": App.Vector(0, 0, 1),
        }[obj.DirectionMode]
    if not all(math.isfinite(v) for v in direction) or direction.Length < 1e-12:
        raise ReferenceError("The direction vector must be finite and nonzero.")
    direction.normalize()
    return -direction if obj.Reversed else direction


def selected_faces(obj):
    faces = []
    for source, names in obj.Faces:
        validate_link(obj, source)
        for name in names or [""]:
            shape = linked_shape((source, [name] if name else []))
            if name and shape.ShapeType != "Face":
                raise ReferenceError("Select faces, not edges or vertices.")
            if not shape.Faces:
                raise ReferenceError("The selected object has no faces.")
            faces.extend(shape.Faces)
    if not faces:
        raise ReferenceError("Select at least one target face.")
    return faces


def makeIsocline(document=None):
    document = document or App.ActiveDocument
    if document is None:
        raise ReferenceError("Open a document first.")
    obj = document.addObject("Part::FeaturePython", "IsoclineCurve")
    obj.Label = "Isocline Curve"
    IsoclineCurve(obj)
    if App.GuiUp:
        from .IsoclineGui import ViewProviderIsocline

        ViewProviderIsocline(obj.ViewObject)
        obj.ViewObject.LineColor = (0.95, 0.15, 0.05)
        obj.ViewObject.LineWidth = 4
    return obj


class IsoclineCurve:
    def __init__(self, obj):
        obj.addProperty("App::PropertyLinkSubList", "Faces", "Isocline", "Faces to trace")
        obj.addProperty("App::PropertyEnumeration", "DirectionMode", "Isocline")
        obj.DirectionMode = ["X axis", "Y axis", "Z axis", "Reference", "Custom vector"]
        obj.DirectionMode = "Z axis"
        obj.addProperty("App::PropertyLinkSub", "DirectionReference", "Isocline")
        obj.addProperty("App::PropertyVector", "CustomDirection", "Isocline")
        obj.CustomDirection = App.Vector(0, 0, 1)
        obj.addProperty("App::PropertyBool", "Reversed", "Isocline")
        obj.addProperty(
            "App::PropertyAngle", "Angle", "Isocline", "Draft angle: 0 is silhouette, 90 faces pull"
        )
        obj.addProperty(
            "App::PropertyLength", "Tolerance", "Isocline", "3D curve approximation tolerance"
        )
        obj.Tolerance = 1e-5
        obj.addProperty(
            "App::PropertyVector", "Direction", "Isocline", "Resolved world pull direction"
        )
        obj.addProperty("App::PropertyString", "StatusMessage", "Isocline")
        obj.addProperty("App::PropertyLinkList", "PlacementSupport", "Isocline")
        obj.setEditorMode("PlacementSupport", 2)
        obj.setEditorMode("Direction", 1)
        obj.setEditorMode("StatusMessage", 1)
        obj.Proxy = self

    def onChanged(self, obj, prop):
        if prop in ("Faces", "DirectionReference") and "PlacementSupport" in obj.PropertiesList:
            self.dependencies(obj)

    def dependencies(self, obj):
        update_placement_support(obj, list(obj.Faces) + [obj.DirectionReference])

    def execute(self, obj):
        try:
            self.dependencies(obj)
            angle = obj.Angle.Value
            if not math.isfinite(angle) or not 0 <= angle <= 90:
                raise ReferenceError("Draft angle must be between 0 and 90 degrees.")
            tolerance = curve_tolerance(obj.Tolerance.Value)
            direction = resolved_direction(obj)
            edges = []
            for face in selected_faces(obj):
                edges.extend(Part.makeIsocline(face, direction, angle, tolerance).Edges)
            if not edges:
                raise ReferenceError(
                    "No isocline curve at this angle. The solution may be empty or an isolated point."
                )
            result = Part.makeCompound([Part.Wire(group) for group in Part.sortEdges(edges)])
            if not result.isValid():
                raise ReferenceError("The contour did not produce valid curve geometry.")
            parent = obj.getGlobalPlacement().multiply(obj.Placement.inverse())
            result.transformShape(parent.inverse().toMatrix())
            obj.Shape = result
            obj.Direction = direction
            obj.StatusMessage = "Ready"
        except Exception as error:
            obj.Shape = Part.Shape()
            obj.StatusMessage = str(error)
            raise

    def dumps(self):
        return None

    def loads(self, state):
        pass
