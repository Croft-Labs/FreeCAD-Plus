# SPDX-License-Identifier: LGPL-2.1-or-later
"""Independent native sketches owned by a component, with explicit support."""
import FreeCAD as App
import Part
import Sketcher  # Registers the native sketch type.
import ComponentModel as Model

PLANES = ("XY plane", "XZ plane", "YZ plane", "Selected planar face")


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


def create(component, plane="XY plane", offset=0.0, support=None):
    if not Model.is_component(component) or plane not in PLANES:
        raise ValueError("Choose a component and a sketch plane.")
    Model.activate(component, strict=False)
    if plane == "Selected planar face":
        support = check_support(component, support)
    with Model.transaction(component.Document, "New Sketch"):
        sketch = component.Document.addObject("Sketcher::SketchObject", "Sketch")
        Model.register_object(component, sketch)
        if plane == "Selected planar face":
            sketch.AttachmentSupport = [(support[0], support[1])]
            sketch.MapMode = "FlatFace"
            sketch.AttachmentOffset = App.Placement(App.Vector(0, 0, offset), App.Rotation())
        else:
            rotation = {"XY plane": App.Rotation(),
                        "XZ plane": App.Rotation(App.Vector(1, 0, 0), 90),
                        "YZ plane": App.Rotation(App.Vector(0, 1, 0), 90)}[plane]
            normal = rotation.multVec(App.Vector(0, 0, 1))
            sketch.Placement = App.Placement(normal * offset, rotation)
        component.Document.recompute()
        if "Invalid" in sketch.State:
            raise ValueError("The sketch could not attach to that support.")
    return sketch
