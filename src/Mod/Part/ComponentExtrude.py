# SPDX-License-Identifier: LGPL-2.1-or-later
"""Body-independent component Extrude using native extrusion and Boolean features."""
import json
import FreeCAD as App
import ComponentModel as Model
import ComponentProfile as Profile
import ComponentExtent as Extent

MODES = ("New Body", "Add", "Subtract")


def inputs(component, profile, length, mode, target=None, operation=None, elements=None):
    if not Model.is_component(component) or Model.owner(profile) != component:
        raise ValueError("Choose a profile owned by the active component.")
    if mode not in MODES or length <= 0:
        raise ValueError("Choose an operation and a positive extrusion length.")
    if getattr(profile, "ComponentRole", "") not in ("Object", "Reference", "Result"):
        raise ValueError("Choose a sketch or evaluated curve object.")
    shape = Model.current_shape(profile)
    if shape.Solids or not shape.Edges:
        raise ValueError("Choose a closed planar profile, not a solid body.")
    if elements is not None:
        Profile.face(profile, elements)
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


def preview(component, profile, length, mode="New Body", target=None, reversed_direction=False, elements=None,
            options=None, volume_only=False, tool_only=False):
    # Overlay geometry is independent of the Boolean and its target. A target
    # is retained only when it defines a requested first/last/through extent.
    if tool_only:
        mode = "New Body"
        bounded = options and any(options[key] in ("UpToFirst", "UpToLast", "ThroughAll")
                                  for key in (("extent", "extent2") if options["sides"] == "Two sides" else ("extent",)))
        if not bounded:
            target = None
    inputs(component, profile, length, mode, None if tool_only else target, elements=elements)
    if options is not None:
        Extent.validate(component, profile, length, mode, target, options)
    scratch = App.newDocument("ComponentExtrudePreview", hidden=True, temp=True)
    try:
        copied = scratch.addObject("Part::Part2DObjectPython" if profile.isDerivedFrom("Sketcher::SketchObject") else "Part::Feature", "Profile")
        shape = Profile.face(profile, elements) if elements is not None else Model.current_shape(profile)
        Profile.assign_shape(copied, profile, shape)
        base = None
        if target is not None:
            base = scratch.addObject("Part::Feature", "Target")
            base.Shape = Model.current_shape(target)
        if options is not None:
            import PartDesign
            tool = scratch.addObject("PartDesign::Pad", "Extrusion")
            copies = {profile: copied}
            if target:
                copies[target] = base
            Extent.configure(tool, copied, length, mode, base, reversed_direction,
                             Extent.copy_references(scratch, options, copies))
            if tool_only:
                scratch.recompute()
                if tool.AddSubShape.isNull():
                    raise ValueError("Cannot preview this extrusion. Check the profile and extent references.")
                return tool.AddSubShape.copy()
            result = evaluate(scratch, tool, mode, base)
            if volume_only and base:
                return base.Shape.cut(result) if mode == "Subtract" else result.cut(base.Shape)
            return result
        tool = scratch.addObject("Part::Extrusion", "Extrusion")
        configure(tool, copied, length, reversed_direction)
        operation = tool
        if mode != "New Body":
            operation = scratch.addObject("Part::Fuse" if mode == "Add" else "Part::Cut", "Extrude")
            operation.Base, operation.Tool = base, tool
        result = evaluate(scratch, operation, mode, base)
        if volume_only and base:
            return base.Shape.cut(result) if mode == "Subtract" else result.cut(base.Shape)
        return result
    finally:
        App.closeDocument(scratch.Name)
        App.setActiveDocument(component.Document.Name)


def create(component, profile, length, mode="New Body", target=None, reversed_direction=False, elements=None,
           options=None):
    Model.activate(component, strict=False)
    inputs(component, profile, length, mode, target, elements=elements)
    if options is not None:
        Extent.validate(component, profile, length, mode, target, options)
    doc = component.Document
    target_visibility = bool(target.Visibility) if target is not None else None
    with Model.transaction(doc, "Extrude"):
        if options is not None:
            import PartDesign
        tool = doc.addObject("PartDesign::Pad" if options is not None else "Part::Extrusion", "Extrude")
        bound = Profile.bind(component, profile, elements)
        if options is None:
            configure(tool, bound, length, reversed_direction)
        else:
            Extent.configure(tool, bound, length, mode, target, reversed_direction, options)
        operation = tool
        if mode != "New Body" and options is None:
            component.addObject(tool)
            Model._identity(tool, "Internal")
            tool.Label = "Extrude profile"
            operation = doc.addObject("Part::Fuse" if mode == "Add" else "Part::Cut", "Extrude")
            operation.Base, operation.Tool = target, tool
            Model._property(operation, "Link", "ExtrusionTool", tool, True)
        Model.register_object(component, operation, "Operation")
        operation.Label = Model.next_label(component, "Extrude", operation)
        Model._property(operation, "String", "OperationKind", "Extrude", True)
        Model._property(operation, "String", "ExtrudeMode", mode, True)
        if options is not None and target:
            Model._property(operation, "LinkList", "ConsumedResults", [target], True)
            Model._property(operation, "String", "PreviousVisibility",
                            json.dumps({target.ObjectId: target_visibility}), True)
        evaluate(doc, operation, mode, target)
        result = Model.publish_result(component, operation)
        if App.GuiUp:
            profile.Visibility = False
            if tool != operation:
                tool.Visibility = False
            if target:
                target.Visibility = False
    return operation, result


def parameters(operation):
    if getattr(operation, "OperationKind", "") == "Extrude":
        mode = operation.ExtrudeMode
        tool = getattr(operation, "ExtrusionTool", operation)
    elif operation.TypeId == "Part::Extrusion" and getattr(operation, "ComponentRole", "") == "Operation":
        mode, tool = "New Body", operation
    else:
        raise ValueError("Select a component Extrude operation.")
    target = operation.BaseFeature if tool.TypeId == "PartDesign::Pad" else operation.Base
    return tool, mode, target if mode != "New Body" else None


def edit(operation, profile, length, reversed_direction=False, mode=None, target=None, elements=None, options=None):
    component = Model.owner(operation)
    Model.activate(component, strict=False)
    tool, old_mode, old_target = parameters(operation)
    if mode is None:
        mode, target = old_mode, old_target
    if getattr(operation, "LegacyMigration", "") == "Sketch-Pad pilot" and mode != "New Body":
        raise ValueError("This retained legacy Body supports parameter edits. Operation/target conversion awaits the full extrusion adapter.")
    inputs(component, profile, length, mode, target, operation, elements)
    if options is None and tool.TypeId == "PartDesign::Pad":
        options = Extent.read(tool)
    if options is not None:
        Extent.validate(component, profile, length, mode, target, options, operation)
    base_profile = tool.Profile[0] if tool.TypeId == "PartDesign::Pad" else tool.Base
    old_profile = base_profile if hasattr(base_profile, "ProfileSource") else None
    replace = mode != old_mode or (options is not None and tool.TypeId != "PartDesign::Pad")
    if old_profile and any(obj not in (component, tool) for obj in old_profile.InList):
        raise ValueError("The selected-curve profile has another consumer. Review it before editing.")
    if tool.ExpressionEngine or operation.ExpressionEngine:
        raise ValueError("This extrusion uses expressions. Edit them in the property editor to preserve the formulas.")
    doc = component.Document
    results = [obj for obj in operation.InList if getattr(obj, "Producer", None) == operation]
    if replace:
        allowed = set(results + [component])
        if any(obj not in allowed for obj in operation.InList):
            raise ValueError("Other objects reference this operation directly. Use its published result before changing the operation type.")
        if tool != operation and any(obj not in (component, operation) for obj in tool.InList):
            raise ValueError("The extrusion tool has another consumer; its operation type cannot be changed safely.")
    previous = json.loads(getattr(operation, "PreviousVisibility", "{}"))
    consumed = list(getattr(operation, "ConsumedResults", []))
    target_visibility = previous.get(target.ObjectId, bool(target.Visibility)) if target else None
    with Model.transaction(doc, "Edit Extrude"):
        bound = Profile.bind(component, profile, elements, old_profile)
        if replace:
            ordered = list(component.ModelHistory)
            old_name, old_id, label = operation.Name, operation.ObjectId, operation.Label
            old_tool_name = tool.Name if tool != operation else None
            suppressed = getattr(operation, "UserSuppressed", False)
            if options is not None:
                import PartDesign
            replacement_tool = doc.addObject("PartDesign::Pad" if options is not None else "Part::Extrusion", "Extrude")
            if options is None:
                configure(replacement_tool, bound, length, reversed_direction)
            else:
                Extent.configure(replacement_tool, bound, length, mode, target, reversed_direction, options)
            replacement = replacement_tool
            if mode != "New Body" and options is None:
                component.addObject(replacement_tool)
                Model._identity(replacement_tool, "Internal")
                replacement = doc.addObject("Part::Fuse" if mode == "Add" else "Part::Cut", "Extrude")
                replacement.Base, replacement.Tool = target, replacement_tool
                Model._property(replacement, "Link", "ExtrusionTool", replacement_tool, True)
            Model.register_object(component, replacement, "Operation")
            replacement.ObjectId, replacement.Label = old_id, label
            Model._property(replacement, "String", "OperationKind", "Extrude", True)
            Model._property(replacement, "String", "ExtrudeMode", mode, True)
            Model._property(replacement, "Bool", "UserSuppressed", suppressed)
            evaluate(doc, replacement, mode, target)
            for result in results:
                result.Producer = replacement
                result.touch()
            doc.removeObject(old_name)
            if old_tool_name:
                doc.removeObject(old_tool_name)
            component.ModelHistory = [replacement.Name if name == old_name else name for name in ordered]
            operation, tool = replacement, replacement_tool
        else:
            if options is None:
                configure(tool, bound, length, reversed_direction)
            else:
                Extent.configure(tool, bound, length, mode, target, reversed_direction, options)
            if mode != "New Body" and options is None:
                operation.Base = target
        if mode != "New Body":
            if not hasattr(operation, "ConsumedResults"):
                Model._property(operation, "LinkList", "ConsumedResults", [], True)
                Model._property(operation, "String", "PreviousVisibility", "{}", True)
            operation.ConsumedResults = [target]
            operation.PreviousVisibility = json.dumps({target.ObjectId: target_visibility})
        evaluate(doc, operation, mode, target)
        if old_profile and old_profile != bound:
            doc.removeObject(old_profile.Name)
        if App.GuiUp:
            profile.Visibility = False
            if tool != operation:
                tool.Visibility = False
            if results:
                import ComponentResultView
                for result in results:
                    ComponentResultView.sync(result)
            if target:
                target.Visibility = target_visibility if getattr(operation, "UserSuppressed", False) else False
            for source in consumed:
                if source != target and not any(source in getattr(other, "ConsumedResults", [])
                       and not getattr(other, "UserSuppressed", False) for other in Model.history(component)):
                    source.Visibility = previous.get(source.ObjectId, True)
    return operation
