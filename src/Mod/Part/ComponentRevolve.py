# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component-owned Revolve backed by native Revolution and Groove features."""
import json
import FreeCAD as App
import ComponentModel as Model
import ComponentProfile as Profile
import ComponentExtent as Extent
import ComponentExtrude as Extrude

MODES = Extrude.MODES


def defaults():
    return dict(sides="One side", extent="Angle", extent2="Angle", angle2=90.,
                axis="V_Axis", axis_reference=None, project=False, start="Profile plane",
                start_offset=0., start_reference=None, limit=None, limit2=None, refine=True)


def read(operation):
    values = defaults()
    values.update(sides=operation.SideType, extent=operation.Type, extent2=operation.Type2,
                  angle2=operation.Angle2.Value, project=operation.ProjectAxis,
                  start=operation.StartType, start_offset=operation.StartOffset.Value,
                  refine=operation.Refine)
    for key, value in (("axis_reference", operation.ReferenceAxis), ("limit", operation.UpToFace),
                       ("limit2", operation.UpToFace2), ("start_reference", operation.StartReference)):
        values[key] = (value[0], list(value[1])) if value and value[0] else None
    axis = values["axis_reference"]
    values["axis"] = axis[1][0] if axis and axis[0] == operation.Profile[0] and axis[1] in (["V_Axis"], ["H_Axis"]) else "Reference"
    return values


def validate(component, profile, angle, mode, target, values, operation=None, elements=None):
    Extrude.inputs(component, profile, 1., mode, target, operation, elements)
    if values["sides"] not in ("One side", "Two sides", "Symmetric"):
        raise ValueError("Choose one angle, two angles or symmetric.")
    types = ("Angle", "ThroughAll" if mode == "Subtract" else "UpToLast", "UpToFirst", "UpToFace")
    references = []
    for suffix, span in (("", angle), ("2", values["angle2"])):
        if suffix and values["sides"] != "Two sides":
            continue
        kind = values["extent" + suffix]
        if kind not in types or (kind == "Angle" and not 0 < span <= 360):
            raise ValueError("Choose a supported type and an angle greater than zero and at most 360 degrees.")
        if kind in ("UpToLast", "UpToFirst", "ThroughAll") and target is None:
            raise ValueError("This extent requires an explicit target body.")
        if kind == "UpToFace":
            references.append(values["limit" + suffix])
    if values["start"] not in ("Profile plane", "Offset", "Reference") or abs(values["start_offset"]) > 360:
        raise ValueError("Choose a start definition and an offset between -360 and 360 degrees.")
    if values["start"] == "Reference":
        references.append(values["start_reference"])
    if values["axis"] == "Reference":
        references.append(values["axis_reference"])
    elif values["axis"] not in ("V_Axis", "H_Axis"):
        raise ValueError("Choose a sketch axis or reference axis.")
    for ref in references:
        if not ref or not ref[0]:
            raise ValueError("Select the required axis or limiting reference.")
        obj, subs = ref
        if obj.Document != component.Document or not (Model.owner(obj) == component or obj in component.Origin.OriginFeatures):
            raise ValueError("Choose a reference owned by the active component.")
        if operation and (obj == operation or operation in obj.OutListRecursive):
            raise ValueError("Revolve cannot reference its own downstream result.")
        if hasattr(obj, "Shape") and not obj.Shape.isNull():
            Model.current_shape(obj)
            for sub in subs:
                if sub:
                    if (obj == profile and obj.isDerivedFrom("Sketcher::SketchObject")
                            and sub.startswith("Axis") and (not sub[4:] or sub[4:].isdigit())):
                        # Native sketch construction axes are not Shape edges.
                        # The native feature validates the axis index/geometry.
                        index = int(sub[4:] or "0")
                        if index >= obj.AxisCount:
                            raise ValueError("The sketch construction axis is unavailable.")
                        continue
                    obj.Shape.getElement(sub)


def configure(tool, bound, angle, target, reverse, values):
    tool.Profile, tool.BaseFeature = (bound, []), target
    tool.SideType = values["sides"]
    tool.Type, tool.Type2 = values["extent"], values["extent2"]
    tool.Angle, tool.Angle2 = angle, values["angle2"]
    tool.Reversed = bool(reverse)
    tool.ReferenceAxis = (bound, [values["axis"]]) if values["axis"] != "Reference" else values["axis_reference"]
    tool.ProjectAxis, tool.Refine = values["project"], values["refine"]
    tool.StartType, tool.StartOffset = values["start"], values["start_offset"]
    tool.StartReference = values["start_reference"] or (None, [])
    tool.UpToFace, tool.UpToFace2 = values["limit"] or (None, []), values["limit2"] or (None, [])


def evaluate(doc, operation, mode, target):
    doc.recompute()
    if "Invalid" in operation.State or operation.Shape.isNull() or Model._shape_kind(operation.Shape) != "Body":
        raise ValueError("Revolve requires one valid solid. Check the profile, axis, extents and target contact.")
    if mode == "Subtract" and abs(operation.Shape.Volume - Model.current_shape(target).Volume) < 1e-9:
        raise ValueError("The revolution removes no material from the selected target.")
    return operation.Shape.copy()


def feature(doc, mode):
    import PartDesign
    return doc.addObject("PartDesign::Groove" if mode == "Subtract" else "PartDesign::Revolution", "Revolve")


def preview(component, profile, angle, mode="New Body", target=None, reverse=False, elements=None, options=None, volume_only=False, tool_only=False):
    values = options or defaults()
    if tool_only:
        values = dict(values)
        active_extents = ("extent", "extent2") if values["sides"] == "Two sides" else ("extent",)
        # Native Through All is a full turn, including when either side requests
        # it. Up To Last instead derives an angular bound from the target.
        if any(values[key] == "ThroughAll" for key in active_extents):
            values.update(sides="One side", extent="Angle", extent2="Angle")
            angle = 360.
            active_extents = ("extent",)
        bounded = any(values[key] in ("UpToFirst", "UpToLast")
                      for key in active_extents)
        if not bounded:
            target = None
            mode = "New Body"
    validate(component, profile, angle, mode, target, values, elements=elements)
    scratch = App.newDocument("ComponentRevolvePreview", hidden=True, temp=True)
    try:
        if elements is None and profile.isDerivedFrom("Sketcher::SketchObject"):
            # A shape-only Part2D helper loses the native sketch angular frame
            # and construction axes. Copy evaluated internal geometry, without
            # constraints or cross-document links, into a temporary native sketch.
            copied = scratch.addObject("Sketcher::SketchObject", "Profile")
            for index, geometry in enumerate(profile.Geometry):
                copied.addGeometry(geometry, profile.getConstruction(index))
            copied.Placement = profile.Placement
            scratch.recompute()
        else:
            copied = scratch.addObject("Part::Part2DObjectPython", "Profile")
            Profile.assign_shape(copied, profile, Profile.face(profile, elements) if elements is not None else Model.current_shape(profile))
        base = None
        copies = {profile: copied}
        if target:
            base = scratch.addObject("Part::Feature", "Target")
            base.Shape = Model.current_shape(target)
            copies[target] = base
        values = Extent.copy_references(scratch, values, copies)
        if values["axis"] == "Reference" and values["axis_reference"][0] == profile and copied.isDerivedFrom("Sketcher::SketchObject"):
            values = dict(values, axis_reference=(copied, list(values["axis_reference"][1])))
        elif values["axis"] == "Reference":
            obj, subs = values["axis_reference"]
            # An edge copy also represents datum/origin axes without cross-document links.
            axis = scratch.addObject("Part::Feature", "Axis")
            if hasattr(obj, "Shape") and not obj.Shape.isNull():
                axis.Shape = obj.Shape.copy()
            else:
                import Part
                frame = obj.Placement
                direction = App.Vector(1, 0, 0) if obj.isDerivedFrom("App::Line") else App.Vector(0, 0, 1)
                axis.Shape = Part.makeLine(frame.Base, frame.Base + frame.Rotation.multVec(direction))
                subs = ["Edge1"]
            values["axis_reference"] = (axis, subs or ["Edge1"])
        operation = feature(scratch, mode)
        configure(operation, copied, angle, base, reverse, values)
        if tool_only:
            scratch.recompute()
            if operation.AddSubShape.isNull():
                raise ValueError("Cannot preview this revolution. Check the profile, axis and extent references.")
            return operation.AddSubShape.copy()
        result = evaluate(scratch, operation, mode, base)
        return (base.Shape.cut(result) if mode == "Subtract" else result.cut(base.Shape)) if volume_only and base else result
    finally:
        App.closeDocument(scratch.Name)
        App.setActiveDocument(component.Document.Name)


def create(component, profile, angle, mode="New Body", target=None, reverse=False, elements=None, options=None):
    values = options or defaults()
    Model.activate(component, strict=False)
    validate(component, profile, angle, mode, target, values, elements=elements)
    doc = component.Document
    with Model.transaction(doc, "Revolve"):
        operation = feature(doc, mode)
        configure(operation, Profile.bind(component, profile, elements), angle, target, reverse, values)
        Model.register_object(component, operation, "Operation")
        operation.Label = Model.next_label(component, "Revolve", operation)
        Model._property(operation, "String", "OperationKind", "Revolve", True)
        Model._property(operation, "String", "RevolveMode", mode, True)
        Model._property(operation, "LinkList", "ConsumedResults", [target] if target else [], True)
        Model._property(operation, "String", "PreviousVisibility", json.dumps({target.ObjectId: bool(target.Visibility)}) if target else "{}", True)
        evaluate(doc, operation, mode, target)
        result = Model.publish_result(component, operation)
        profile.Visibility = False
        if target:
            target.Visibility = False
    return operation, result


def edit(operation, profile, angle, mode, target=None, reverse=False, elements=None, options=None):
    component, doc = Model.owner(operation), operation.Document
    values = options or read(operation)
    validate(component, profile, angle, mode, target, values, operation, elements)
    if operation.ExpressionEngine:
        raise ValueError("This Revolve uses expressions. Edit its properties to preserve the formulas.")
    results = [obj for obj in operation.InList if getattr(obj, "Producer", None) == operation]
    replace = (mode == "Subtract") != (operation.RevolveMode == "Subtract")
    if replace and getattr(operation, "LegacyMigration", "") == "Native revolve chain":
        raise ValueError("Preserve this native Revolution/Groove identity. Create a separate Revolve to change its additive/subtractive type.")
    if replace and any(obj not in results + [component] for obj in operation.InList):
        raise ValueError("Use the published result for downstream references before changing operation type.")
    old_profile = operation.Profile[0] if hasattr(operation.Profile[0], "ProfileSource") else None
    if old_profile and any(obj not in (operation, component) for obj in old_profile.InList):
        raise ValueError("The selected-curve profile has another consumer.")
    previous = json.loads(operation.PreviousVisibility)
    consumed = list(operation.ConsumedResults)
    target_visibility = previous.get(target.ObjectId, bool(target.Visibility)) if target else None
    with Model.transaction(doc, "Edit Revolve"):
        bound = Profile.bind(component, profile, elements, old_profile)
        if replace:
            old = operation
            ordered = list(component.ModelHistory)
            operation = feature(doc, mode)
            Model.register_object(component, operation, "Operation")
            operation.ObjectId, operation.Label = old.ObjectId, old.Label
            Model._property(operation, "String", "OperationKind", "Revolve", True)
            Model._property(operation, "String", "RevolveMode", mode, True)
            Model._property(operation, "LinkList", "ConsumedResults", [], True)
            Model._property(operation, "String", "PreviousVisibility", "{}", True)
            Model._property(operation, "Bool", "UserSuppressed", getattr(old, "UserSuppressed", False))
            configure(operation, bound, angle, target, reverse, values)
            evaluate(doc, operation, mode, target)
            for result in results:
                result.Producer = operation
                result.touch()
            old_name = old.Name
            doc.removeObject(old_name)
            component.ModelHistory = [operation.Name if name == old_name else name for name in ordered]
        configure(operation, bound, angle, target, reverse, values)
        operation.RevolveMode = mode
        operation.ConsumedResults = [target] if target else []
        operation.PreviousVisibility = json.dumps({target.ObjectId: target_visibility}) if target else "{}"
        evaluate(doc, operation, mode, target)
        if old_profile and old_profile != bound:
            doc.removeObject(old_profile.Name)
        profile.Visibility = False
        if App.GuiUp:
            import ComponentResultView
            for result in results:
                ComponentResultView.sync(result)
        if target:
            target.Visibility = target_visibility if getattr(operation, "UserSuppressed", False) else False
        for source in consumed:
            if source != target and not any(source in getattr(other, "ConsumedResults", []) and not getattr(other, "UserSuppressed", False) for other in Model.history(component)):
                source.Visibility = previous.get(source.ObjectId, True)
    return operation
