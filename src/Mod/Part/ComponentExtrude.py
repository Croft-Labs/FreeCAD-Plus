# SPDX-License-Identifier: LGPL-2.1-or-later
"""Body-independent component Extrude using native extrusion and Boolean features."""
import FreeCAD as App
import ComponentModel as Model

MODES = ("New Body", "Add", "Subtract")


def inputs(component, profile, length, mode, target=None, operation=None):
    if not Model.is_component(component) or Model.owner(profile) != component:
        raise ValueError("Choose a profile owned by the active component.")
    if mode not in MODES or length <= 0:
        raise ValueError("Choose an operation and a positive extrusion length.")
    if getattr(profile, "ComponentRole", "") not in ("Object", "Reference", "Result"):
        raise ValueError("Choose a sketch or evaluated curve object.")
    shape = Model.current_shape(profile)
    if shape.Solids or not shape.Edges:
        raise ValueError("Choose a closed planar profile, not a solid body.")
    if mode != "New Body":
        if target is None or Model.owner(target) != component or target.Name not in component.ResultObjects:
            raise ValueError("Choose an explicit body in the active component.")
        if len(Model.current_shape(target).Solids) != 1:
            raise ValueError("The selected target must be one current solid body.")
    elif target is not None:
        raise ValueError("New Body does not use a target body.")
    if operation and any(operation == obj or operation in obj.OutListRecursive
                         for obj in (profile, target) if obj is not None):
        raise ValueError("An extrusion cannot depend on its own downstream result.")


def configure(tool, profile, length, reversed_direction):
    tool.Base = profile
    tool.DirMode = "Normal"
    tool.LengthFwd = length
    tool.LengthRev = 0
    tool.Solid = True
    tool.Reversed = bool(reversed_direction)


def evaluate(doc, operation, mode, target):
    doc.recompute()
    if "Invalid" in operation.State or operation.Shape.isNull():
        raise ValueError("Extrude failed. Check the profile, direction and target.")
    if Model._shape_kind(operation.Shape) != "Body":
        raise ValueError("This Extrude requires one solid result. Check closed profiles and target contact.")
    if mode == "Subtract" and abs(operation.Shape.Volume - target.Shape.Volume) < 1e-9:
        raise ValueError("The extrusion removes no material from the selected target.")
    return operation.Shape.copy()


def preview(component, profile, length, mode="New Body", target=None, reversed_direction=False):
    inputs(component, profile, length, mode, target)
    scratch = App.newDocument("ComponentExtrudePreview", hidden=True, temp=True)
    try:
        copied = scratch.addObject("Part::Feature", "Profile")
        copied.Shape = Model.current_shape(profile)
        tool = scratch.addObject("Part::Extrusion", "Extrusion")
        configure(tool, copied, length, reversed_direction)
        operation = tool
        base = None
        if mode != "New Body":
            base = scratch.addObject("Part::Feature", "Target")
            base.Shape = Model.current_shape(target)
            operation = scratch.addObject("Part::Fuse" if mode == "Add" else "Part::Cut", "Extrude")
            operation.Base, operation.Tool = base, tool
        return evaluate(scratch, operation, mode, base)
    finally:
        App.closeDocument(scratch.Name)
        App.setActiveDocument(component.Document.Name)


def create(component, profile, length, mode="New Body", target=None, reversed_direction=False):
    Model.activate(component)
    inputs(component, profile, length, mode, target)
    doc = component.Document
    with Model.transaction(doc, "Extrude"):
        tool = doc.addObject("Part::Extrusion", "Extrude")
        configure(tool, profile, length, reversed_direction)
        operation = tool
        if mode != "New Body":
            component.addObject(tool)
            Model._identity(tool, "Internal")
            tool.Label = "Extrude profile"
            operation = doc.addObject("Part::Fuse" if mode == "Add" else "Part::Cut", "Extrude")
            operation.Base, operation.Tool = target, tool
            Model._property(operation, "Link", "ExtrusionTool", tool, True)
        operation.Label = "Extrude"
        Model.register_object(component, operation, "Operation")
        Model._property(operation, "String", "OperationKind", "Extrude", True)
        Model._property(operation, "String", "ExtrudeMode", mode, True)
        evaluate(doc, operation, mode, target)
        result = Model.publish_result(component, operation)
        if App.GuiUp:
            profile.Visibility = False
            tool.Visibility = False
    return operation, result


def parameters(operation):
    if getattr(operation, "OperationKind", "") == "Extrude":
        mode = operation.ExtrudeMode
        tool = getattr(operation, "ExtrusionTool", operation)
    elif operation.TypeId == "Part::Extrusion" and getattr(operation, "ComponentRole", "") == "Operation":
        mode, tool = "New Body", operation
    else:
        raise ValueError("Select a component Extrude operation.")
    return tool, mode, operation.Base if mode != "New Body" else None


def edit(operation, profile, length, reversed_direction=False):
    component = Model.owner(operation)
    Model.activate(component)
    tool, mode, target = parameters(operation)
    inputs(component, profile, length, mode, target, operation)
    if tool.ExpressionEngine:
        raise ValueError("This extrusion uses expressions. Edit them in the property editor to preserve the formulas.")
    with Model.transaction(component.Document, "Edit Extrude"):
        configure(tool, profile, length, reversed_direction)
        evaluate(component.Document, operation, mode, target)
        if App.GuiUp:
            profile.Visibility = False
    return operation
