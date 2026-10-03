# SPDX-License-Identifier: LGPL-2.1-or-later
"""Independent native sketches owned by a component, with explicit support."""
import FreeCAD as App
import math
import Part
import Sketcher  # Registers the native sketch type.
import ComponentModel as Model

ORIGIN_PLANES = ("XY plane", "XZ plane", "YZ plane")
PLANES = ORIGIN_PLANES + ("Selected planar face", "User plane", "Create new plane")


def user_planes(component):
    return [obj for obj in Model.history(component)
            if obj.isDerivedFrom("PartDesign::Plane") or obj.isDerivedFrom("Part::Plane")
            or obj.isDerivedFrom("Part::DatumPlane")]


def check_plane(component, plane):
    if plane not in user_planes(component):
        raise ValueError("Select a user plane in the active component.")
    if "Invalid" in plane.State:
        raise ValueError("Repair the selected plane before using it.")
    if not plane.isDerivedFrom("Part::DatumPlane"):
        check_support(component, (plane, "Face1"))
    return plane


def origin_plane(component, name):
    role = name.split()[0] + "_Plane"
    return next(obj for obj in component.Origin.OriginFeatures if obj.Role == role)


def _attach(obj, component, plane, offset, support=None):
    if plane in ORIGIN_PLANES:
        obj.AttachmentSupport = [(origin_plane(component, plane), "")]
        obj.MapMode = "ObjectXY"
    elif plane == "User plane":
        obj.AttachmentSupport = [(check_plane(component, support), "")]
        obj.MapMode = "ObjectXY"
    elif plane == "Selected planar face":
        source, name = check_support(component, support)
        obj.AttachmentSupport = [(source, name)]
        obj.MapMode = "FlatFace"
    else:
        raise ValueError("Choose a base plane or planar face.")
    obj.AttachmentOffset = App.Placement(App.Vector(0, 0, offset), App.Rotation())


def plane_rotation(angles, directions=None):
    if directions is None:
        return App.Rotation(App.Vector(0, 0, 1), angles[2]).multiply(
            App.Rotation(App.Vector(0, 1, 0), angles[1])).multiply(
            App.Rotation(App.Vector(1, 0, 0), angles[0]))
    axis, direction, normal = directions
    if axis not in ("X", "Y") or not all(math.isfinite(v) for v in (*direction, *normal)):
        raise ValueError("Choose finite X-axis or Y-axis and Z-axis directions.")
    along, z = App.Vector(*direction), App.Vector(*normal)
    if along.Length < 1e-9 or z.Length < 1e-9:
        raise ValueError("Axis directions must be nonzero.")
    along.normalize()
    z.normalize()
    if along.cross(z).Length < 1e-9:
        raise ValueError("The in-plane direction must not be parallel to the Z-axis direction.")
    # Z defines the normal; project the selected X/Y direction onto the plane.
    return App.Rotation(along if axis == "X" else App.Vector(),
                        along if axis == "Y" else App.Vector(), z,
                        "ZXY" if axis == "X" else "ZYX")


def _new_plane(component, base, offset, support, angles, origin=(0.0, 0.0), directions=None):
    rotation = plane_rotation(angles, directions)
    # Reuse the native datum and attachment engine without introducing a Body.
    import PartDesign  # Registers PartDesign::Plane.
    plane = component.Document.addObject("PartDesign::Plane", "Plane")
    Model.register_object(component, plane)
    plane.Label = Model.next_label(component, "Plane", plane)
    _attach(plane, component, base, offset, support)
    plane.AttachmentOffset = App.Placement(App.Vector(origin[0], origin[1], offset), rotation)
    component.Document.recompute()
    if "Invalid" in plane.State:
        raise ValueError("The new plane could not attach to that support.")
    return plane


def create_plane(component, base="XY plane", offset=0.0, support=None,
                 angles=(0.0, 0.0, 0.0), origin=(0.0, 0.0), directions=None):
    if not Model.is_component(component):
        raise ValueError("Choose a component for the datum plane.")
    Model.activate(component, strict=False)
    with Model.transaction(component.Document, "New Datum Plane"):
        return _new_plane(component, base, offset, support, angles, origin, directions)


def check_support(component, support):
    if not support or len(support) != 2:
        raise ValueError("Select one planar face in the active component.")
    source, name = support
    if Model.owner(source) != component or getattr(source, "ComponentRole", "") not in ("Object", "Result", "Reference"):
        raise ValueError("Use a local object, or Add Reference Object before attaching to another component.")
    if not name.startswith("Face"):
        raise ValueError("Select one planar face.")
    face = Model.current_shape(source).getElement(name)
    if face.ShapeType != "Face" or not isinstance(face.Surface, Part.Plane):
        raise ValueError("Sketch support must be a planar face.")
    return source, name


def create(component, plane="XY plane", offset=0.0, support=None,
           new_plane_base="XY plane", angles=(0.0, 0.0, 0.0), origin=(0.0, 0.0), directions=None):
    if not Model.is_component(component) or plane not in PLANES:
        raise ValueError("Choose a component and a sketch plane.")
    Model.activate(component, strict=False)
    with Model.transaction(component.Document, "New Sketch"):
        if plane == "Create new plane":
            support = _new_plane(component, new_plane_base, offset, support, angles, origin, directions)
            plane, offset = "User plane", 0.0
        sketch = component.Document.addObject("Sketcher::SketchObject", "Sketch")
        Model.register_object(component, sketch)
        sketch.Label = Model.next_label(component, "Sketch", sketch)
        _attach(sketch, component, plane, offset, support)
        component.Document.recompute()
        if "Invalid" in sketch.State:
            raise ValueError("The sketch could not attach to that support.")
    return sketch
