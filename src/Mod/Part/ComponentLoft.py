# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Loft with ordered associative sections and native add/subtract engines."""
import json
import math
import FreeCAD as App
import ComponentModel as Model
import ComponentProfile as Profile
from ComponentExtrude import MODES


def defaults():
    return dict(ruled=False, closed=False, refine=True, fuzzy=0.)


def read(operation):
    sections = []
    for obj, elements in [operation.Profile] + list(operation.Sections):
        if hasattr(obj, "ProfileSource"):
            obj, elements = obj.ProfileSource
            sections.append((obj, list(elements)))
        else:
            sections.append((obj, list(elements) if any(elements) else None))
    return sections, operation.LoftMode, operation.BaseFeature, dict(
        ruled=operation.Ruled, closed=operation.Closed, refine=operation.Refine,
        fuzzy=operation.FuzzyTolerance)


def section_shape(component, source, elements, operation=None):
    if source is None or Model.owner(source) != component or getattr(source, "ComponentRole", "") not in ("Object", "Reference", "Result"):
        raise ValueError("Choose sections owned by the active component.")
    if operation and (source == operation or operation in source.OutListRecursive):
        raise ValueError("Loft cannot depend on its own downstream result.")
    shape = Model.current_shape(source)
    if elements is not None:
        if len(elements) == 1 and elements[0].startswith("Vertex"):
            shape = shape.getElement(elements[0])
        else:
            shape = Profile.face(source, elements)
    if shape.Solids or not (shape.Edges or len(shape.Vertexes) == 1):
        raise ValueError("Choose a closed profile, selected closed sketch curves, or an end vertex.")
    return shape


def validate(component, sections, mode, target, options, operation=None):
    if not Model.is_component(component) or mode not in MODES:
        raise ValueError("Choose an active component and a Loft operation.")
    if not math.isfinite(options.get("fuzzy", 0.)) or not -1. <= options.get("fuzzy", 0.) <= 1.:
        raise ValueError("Fuzzy tolerance must be between -1 and 1 mm; zero uses the native default and negative values request automatic tolerance.")
    if len(sections) < 2:
        raise ValueError("Loft needs at least two ordered sections.")
    if options["closed"] and len(sections) < 3:
        raise ValueError("A closed Loft needs at least three sections.")
    keys = [(obj.Name if obj else None, tuple(elements) if elements is not None else None) for obj, elements in sections]
    if len(set(keys)) != len(keys):
        raise ValueError("Do not repeat a section; use Closed to connect last to first.")
    for index, (obj, elements) in enumerate(sections):
        shape = section_shape(component, obj, elements, operation)
        if not shape.Edges and (options["closed"] or index not in (0, len(sections) - 1)):
            raise ValueError("A vertex is supported only at an open Loft's first or last section.")
    if mode == "New Body":
        if target is not None:
            raise ValueError("New Body does not use a target body.")
    else:
        if target is None or Model.owner(target) != component or target.Name not in component.ResultObjects:
            raise ValueError("Choose an explicit target body in the active component.")
        if len(Model.current_shape(target).Solids) != 1:
            raise ValueError("The target must be one current solid body.")
        if operation and (target == operation or operation in target.OutListRecursive):
            raise ValueError("Loft cannot target its own downstream result.")


def feature(doc, mode):
    import PartDesign
    return doc.addObject("PartDesign::SubtractiveLoft" if mode == "Subtract" else "PartDesign::AdditiveLoft", "Loft")


def configure(operation, sections, target, options):
    operation.Profile = sections[0]
    operation.Sections = sections[1:]
    operation.BaseFeature = target
    operation.Ruled, operation.Closed, operation.Refine = options["ruled"], options["closed"], options["refine"]
    operation.FuzzyTolerance = options.get("fuzzy", 0.)


def evaluate(doc, operation, mode, target):
    doc.recompute()
    if "Invalid" in operation.State or operation.Shape.isNull() or Model._shape_kind(operation.Shape) != "Body":
        raise ValueError("Loft requires one valid solid. Check section order, compatible contours and target contact.")
    if mode != "New Body" and abs(operation.Shape.Volume - Model.current_shape(target).Volume) < 1e-9:
        raise ValueError("Loft adds or removes no material from the selected target.")
    return operation.Shape.copy()


def preview(component, sections, mode="New Body", target=None, options=None, volume_only=False):
    options = options or defaults()
    validate(component, sections, mode, target, options)
    scratch = App.newDocument("ComponentLoftPreview", hidden=True, temp=True)
    try:
        copied = []
        for source, elements in sections:
            obj = scratch.addObject("Part::Part2DObjectPython" if source.isDerivedFrom("Part::Part2DObject") else "Part::Feature", "Section")
            # Loft consumes placed section shapes. Normalizing a copied sketch's
            # local frame would collapse sections whose shape already carries placement.
            obj.Shape = section_shape(component, source, elements)
            copied.append((obj, [""]))
        base = None
        if target:
            base = scratch.addObject("Part::Feature", "Target")
            base.Shape = Model.current_shape(target)
        operation = feature(scratch, mode)
        configure(operation, copied, base, options)
        result = evaluate(scratch, operation, mode, base)
        return (base.Shape.cut(result) if mode == "Subtract" else result.cut(base.Shape)) if volume_only and base else result
    finally:
        App.closeDocument(scratch.Name)
        App.setActiveDocument(component.Document.Name)


def bind(component, sections):
    return [(source, elements) if elements and len(elements) == 1 and elements[0].startswith("Vertex")
            else (Profile.bind(component, source, elements), [""]) for source, elements in sections]


def metadata(component, operation, mode):
    Model.register_object(component, operation, "Operation")
    Model._property(operation, "String", "OperationKind", "Loft", True)
    Model._property(operation, "String", "LoftMode", mode, True)
    Model._property(operation, "LinkList", "ConsumedResults", [], True)
    Model._property(operation, "String", "PreviousVisibility", "{}", True)


def create(component, sections, mode="New Body", target=None, options=None):
    options = options or defaults()
    validate(component, sections, mode, target, options)
    Model.activate(component, strict=False)
    doc = component.Document
    with Model.transaction(doc, "Loft"):
        operation = feature(doc, mode)
        metadata(component, operation, mode)
        operation.Label = Model.next_label(component, "Loft", operation)
        configure(operation, bind(component, sections), target, options)
        operation.ConsumedResults = [target] if target else []
        operation.PreviousVisibility = json.dumps({target.ObjectId: bool(target.Visibility)}) if target else "{}"
        evaluate(doc, operation, mode, target)
        result = Model.publish_result(component, operation)
        for source, elements in sections:
            source.Visibility = False
        if target:
            target.Visibility = False
    return operation, result


def edit(operation, sections, mode, target=None, options=None):
    component, doc = Model.owner(operation), operation.Document
    options = options or read(operation)[3]
    validate(component, sections, mode, target, options, operation)
    if operation.ExpressionEngine:
        raise ValueError("This Loft uses expressions. Edit its properties to preserve the formulas.")
    if operation.Operation not in ("Union", "Subtraction"):
        raise ValueError("This Loft uses a different native Boolean operation. Edit its properties to preserve that operation.")
    results = [obj for obj in operation.InList if getattr(obj, "Producer", None) == operation]
    replace = (mode == "Subtract") != (operation.LoftMode == "Subtract")
    if replace and any(obj not in results + [component] for obj in operation.InList):
        raise ValueError("Use the published result for downstream references before changing operation type.")
    old_profiles = {obj for obj, elements in [operation.Profile] + list(operation.Sections) if hasattr(obj, "ProfileSource")}
    if any(obj not in (component, operation) for profile in old_profiles for obj in profile.InList):
        raise ValueError("A selected-curve section has another consumer.")
    previous, consumed = json.loads(operation.PreviousVisibility), list(operation.ConsumedResults)
    target_visibility = previous.get(target.ObjectId, bool(target.Visibility)) if target else None
    Model.activate(component, strict=False)
    with Model.transaction(doc, "Edit Loft"):
        bound = bind(component, sections)
        if replace:
            old, ordered = operation, list(component.ModelHistory)
            operation = feature(doc, mode)
            metadata(component, operation, mode)
            operation.ObjectId, operation.Label = old.ObjectId, old.Label
            Model._property(operation, "Bool", "UserSuppressed", getattr(old, "UserSuppressed", False))
            configure(operation, bound, target, options)
            evaluate(doc, operation, mode, target)
            for result in results:
                result.Producer = operation
                result.touch()
            old_name = old.Name
            doc.removeObject(old_name)
            component.ModelHistory = [operation.Name if name == old_name else name for name in ordered]
        configure(operation, bound, target, options)
        operation.LoftMode = mode
        operation.ConsumedResults = [target] if target else []
        operation.PreviousVisibility = json.dumps({target.ObjectId: target_visibility}) if target else "{}"
        for profile in old_profiles:
            doc.removeObject(profile.Name)
        evaluate(doc, operation, mode, target)
        for source, elements in sections:
            source.Visibility = False
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
