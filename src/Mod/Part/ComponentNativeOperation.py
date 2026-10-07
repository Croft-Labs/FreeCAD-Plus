# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native component section operations: binding, transactions and stable result identities.

Operation adapters own geometry configuration and validation. This module owns
their common component lifecycle; native features still own recompute and persistence.
"""
import json
import FreeCAD as App
import ComponentModel as Model
import ComponentProfile as Profile


def section_links(operation):
    return ([operation.Profile] if hasattr(operation, "Profile") else []) + list(getattr(operation, "Sections", []))


def read_sections(operation):
    sections = []
    for obj, elements in section_links(operation):
        if hasattr(obj, "ProfileSource"):
            obj, elements = obj.ProfileSource
            sections.append((obj, list(elements)))
        else:
            sections.append((obj, list(elements) if any(elements) else None))
    return sections


def section_shape(component, source, elements, operation=None):
    if source is None or Model.owner(source) != component or getattr(source, "ComponentRole", "") not in ("Object", "Reference", "Result"):
        raise ValueError("Choose sections owned by the active component.")
    if operation and (source == operation or operation in source.OutListRecursive):
        raise ValueError("An operation cannot depend on its own downstream result.")
    shape = Model.current_shape(source)
    if elements is not None:
        if len(elements) == 1 and elements[0].startswith("Vertex"):
            shape = shape.getElement(elements[0])
        else:
            shape = Profile.face(source, elements)
    if shape.Solids or not (shape.Edges or len(shape.Vertexes) == 1):
        raise ValueError("Choose a closed profile, selected closed sketch curves, or an end vertex.")
    return shape


def bind(component, sections):
    return [(source, elements) if elements and len(elements) == 1 and elements[0].startswith("Vertex")
            else (Profile.bind(component, source, elements), [""]) for source, elements in sections]


def metadata(adapter, component, operation, mode):
    Model.register_object(component, operation, "Operation")
    Model._property(operation, "String", "OperationKind", adapter.NAME, True)
    Model._property(operation, "String", adapter.MODE_PROPERTY, mode, True)
    Model._property(operation, "LinkList", "ConsumedResults", [], True)
    Model._property(operation, "String", "PreviousVisibility", "{}", True)


def create(adapter, component, sections, mode="New Body", target=None, options=None):
    options = options or adapter.defaults()
    adapter.validate(component, sections, mode, target, options)
    Model.activate(component, strict=False)
    doc = component.Document
    with Model.transaction(doc, adapter.NAME):
        operation = adapter.feature(doc, mode, options)
        metadata(adapter, component, operation, mode)
        operation.Label = Model.next_label(component, adapter.NAME, operation)
        adapter.configure(operation, bind(component, sections), target, options)
        operation.ConsumedResults = [target] if target else []
        operation.PreviousVisibility = json.dumps({target.ObjectId: bool(target.Visibility)}) if target else "{}"
        adapter.evaluate(doc, operation, mode, target)
        result = Model.publish_result(component, operation)
        for source in adapter.input_objects(sections, options):
            source.Visibility = False
        if target:
            target.Visibility = False
    return operation, result


def edit(adapter, operation, sections, mode, target=None, options=None):
    component, doc = Model.owner(operation), operation.Document
    options = options or adapter.read(operation)[3]
    adapter.validate(component, sections, mode, target, options, operation)
    if operation.ExpressionEngine:
        raise ValueError("This operation uses expressions. Edit its properties to preserve the formulas.")
    if operation.Operation not in adapter.BOOLEANS:
        raise ValueError("This operation uses a different native Boolean operation. Edit its properties to preserve that operation.")
    results = [obj for obj in operation.InList if getattr(obj, "Producer", None) == operation]
    replace = (mode == "Subtract") != (getattr(operation, adapter.MODE_PROPERTY) == "Subtract")
    legacy_loft = adapter.NAME == "Loft" and getattr(operation, "LegacyMigration", "") == "Native loft chain"
    if legacy_loft:
        replace = False  # Native Loft's Boolean engine can preserve its original type/ID.
    if hasattr(adapter, "needs_replacement"):
        replace = replace or adapter.needs_replacement(operation, options)
    if replace and any(obj not in results + [component] for obj in operation.InList):
        raise ValueError("Use the published result for downstream references before changing operation type.")
    old_profiles = {obj for obj, elements in section_links(operation) if hasattr(obj, "ProfileSource")}
    if hasattr(adapter, "internal_inputs"):
        old_profiles.update(adapter.internal_inputs(operation))
    if any(obj not in {component, operation} | old_profiles for profile in old_profiles for obj in profile.InList):
        raise ValueError("A selected-curve section has another consumer.")
    previous, consumed = json.loads(operation.PreviousVisibility), list(operation.ConsumedResults)
    target_visibility = previous.get(target.ObjectId, bool(target.Visibility)) if target else None
    Model.activate(component, strict=False)
    with Model.transaction(doc, "Edit " + adapter.NAME):
        bound = bind(component, sections)
        if replace:
            old, ordered = operation, list(component.ModelHistory)
            operation = adapter.feature(doc, mode, options)
            metadata(adapter, component, operation, mode)
            operation.ObjectId, operation.Label = old.ObjectId, old.Label
            Model._property(operation, "Bool", "UserSuppressed", getattr(old, "UserSuppressed", False))
            adapter.configure(operation, bound, target, options)
            adapter.evaluate(doc, operation, mode, target)
            for result in results:
                result.Producer = operation
                result.touch()
            old_name = old.Name
            doc.removeObject(old_name)
            component.ModelHistory = [operation.Name if name == old_name else name for name in ordered]
        adapter.configure(operation, bound, target, options)
        if legacy_loft:
            # Loft constructors restrict the visible presets to their native
            # additive/subtractive type. The common kernel supports both;
            # persist the expanded enumeration with this original feature.
            operation.Operation = ["Union", "Subtraction", "Common"]
            operation.Operation = "Subtraction" if mode == "Subtract" else "Union"
        setattr(operation, adapter.MODE_PROPERTY, mode)
        operation.ConsumedResults = [target] if target else []
        operation.PreviousVisibility = json.dumps({target.ObjectId: target_visibility}) if target else "{}"
        for profile in old_profiles:
            doc.removeObject(profile.Name)
        adapter.evaluate(doc, operation, mode, target)
        for source in adapter.input_objects(sections, options):
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
