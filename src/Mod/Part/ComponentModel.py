# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component ownership and evaluated-result services for FreeCAD Plus.

Native objects, links, transactions and geometry remain the storage/compute engine.
History ordering is metadata: it must not introduce reverse dependency edges.
"""
from contextlib import contextmanager
import json
from pathlib import Path
import uuid

import FreeCAD as App
import Part

SCHEMA = 1
TYPES = ("Full Component", "Bodies Only", "Hidden")


def _property(obj, kind, name, value, readonly=False):
    obj.addProperty("App::Property" + kind, name, "Component")
    setattr(obj, name, value)
    if readonly:
        obj.setEditorMode(name, 1)


def _identity(obj, role):
    _property(obj, "String", "ObjectId", str(uuid.uuid4()), True)
    _property(obj, "String", "ComponentRole", role, True)


@contextmanager
def transaction(doc, label):
    if doc.HasPendingTransaction:
        raise ValueError("Finish the active edit before changing component structure.")
    doc.openTransaction(label)
    try:
        yield
        doc.recompute()
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


def metadata(doc):
    items = [o for o in doc.Objects if getattr(o, "ComponentRole", "") == "Document"]
    if len(items) != 1:
        raise ValueError("A component document requires exactly one metadata object.")
    return items[0]


def is_component(obj):
    return obj is not None and getattr(obj, "ComponentRole", "") == "Definition"


def definitions(doc):
    return [o for o in doc.Objects if is_component(o)]


def _definition(doc, label):
    obj = doc.addObject("App::Part", "Component")
    obj.Label = label
    _identity(obj, "Definition")
    _property(obj, "StringList", "ModelHistory", [], True)
    _property(obj, "StringList", "ResultObjects", [], True)
    _property(obj, "String", "RepresentationOverrides", "{}", True)
    if App.GuiUp:
        obj.Visibility = False
    return obj


def new_document(label="Component"):
    doc = App.newDocument()
    doc.Label = label
    doc.UndoMode = 1
    initialize(doc, label)
    doc.recompute()
    return doc


def initialize(doc, label):
    if any(getattr(o, "ComponentRole", "") == "Document" for o in doc.Objects):
        raise ValueError("This document already has component metadata.")
    meta = doc.addObject("App::FeaturePython", "ComponentDocument")
    _identity(meta, "Document")
    _property(meta, "Integer", "SchemaVersion", SCHEMA, True)
    _property(meta, "Link", "RootComponent", _definition(doc, label), True)
    _property(meta, "String", "LegacySource", "", True)
    _property(meta, "StringList", "ConversionReport", [], True)
    if App.GuiUp:
        meta.RootComponent.Visibility = True
        meta.ViewObject.Visibility = False
        meta.ViewObject.ShowInTree = False
    return meta


def create_definition(doc, label):
    metadata(doc)
    with transaction(doc, "Create component definition"):
        obj = _definition(doc, label)
    return obj


def children(component):
    if not is_component(component):
        raise ValueError("Select a component definition.")
    return [o for o in component.Group if getattr(o, "ComponentRole", "") == "Occurrence"]


def owner(obj):
    return obj.getParentGeoFeatureGroup()


def _reachable(start, target, visited=None):
    if start == target:
        return True
    visited = set() if visited is None else visited
    key = (start.Document.Name, start.Name)
    if key in visited:
        return False
    visited.add(key)
    return any(child.LinkedObject and _reachable(child.LinkedObject, target, visited)
               for child in children(start))


def add_component(parent, definition=None, label=None, placement=None):
    if not is_component(parent) or (definition is not None and not is_component(definition)):
        raise ValueError("Both parent and source must be component definitions.")
    if definition is not None and _reachable(definition, parent):
        raise ValueError("A component cannot contain itself, directly or indirectly.")
    if definition is not None and definition.Document != parent.Document and not definition.Document.FileName.lower().endswith(".cadprt"):
        raise ValueError("Save an external component as .cadprt before adding it.")
    if definition is not None and definition.Document != parent.Document and not parent.Document.FileName.lower().endswith(".cadprt"):
        raise ValueError("Save the parent as .cadprt before adding an external component.")
    with transaction(parent.Document, "Add Component"):
        if definition is None:
            definition = _definition(parent.Document, label or "Component")
        link = parent.Document.addObject("App::Link", "ComponentInstance")
        link.setLink(definition)
        parent.addObject(link)
        link.Label = label or definition.Label
        _identity(link, "Occurrence")
        peers = [obj for obj in children(parent) if obj != link and obj.LinkedObject == definition]
        for index, peer in enumerate(peers, 1):
            if not hasattr(peer, "InstanceNumber"):
                _property(peer, "Integer", "InstanceNumber", index, True)
        _property(link, "Integer", "InstanceNumber", max([obj.InstanceNumber for obj in peers] or [0]) + 1, True)
        _property(link, "String", "DefinitionId", definition.ObjectId, True)
        _property(link, "Enumeration", "Representation", list(TYPES))
        link.Representation = "Bodies Only"
        _property(link, "Bool", "IncludeInBOM", True)
        _property(link, "Bool", "IncludeInMass", True)
        if App.GuiUp:
            link.Visibility = True
        if placement is not None:
            link.LinkPlacement = placement
    return link


def register_object(component, obj, role="Object", result=False):
    if not is_component(component) or component.Document != obj.Document:
        raise ValueError("An object and its component must belong to the same file.")
    if owner(obj) not in (None, component):
        raise ValueError("An object cannot belong to two components.")
    if not hasattr(obj, "ObjectId"):
        _identity(obj, role)
    elif obj.ComponentRole != role:
        raise ValueError("The object's existing role cannot be changed implicitly.")
    component.addObject(obj)
    if obj.Name not in component.ModelHistory:
        component.ModelHistory = list(component.ModelHistory) + [obj.Name]
    if result and obj.Name not in component.ResultObjects:
        component.ResultObjects = list(component.ResultObjects) + [obj.Name]
    return obj


def history(component):
    return [component.Document.getObject(name) for name in component.ModelHistory
            if component.Document.getObject(name) is not None]


def _shape_kind(shape, sketch=False):
    if shape.isNull() or not shape.isValid():
        raise ValueError("The source has no valid evaluated geometry.")
    if len(shape.Solids) == 1:
        return "Body"
    if len(shape.Solids) > 1:
        raise ValueError("Publish separate identified body results before referencing this compound.")
    if shape.Faces:
        return "Sheet"
    if shape.Edges:
        return "Dumb Sketch" if sketch else "Curve"
    raise ValueError("Select a body, sheet, sketch or curve.")


def geometry_dependencies(obj):
    """Follow geometry inputs without treating component ownership as an input.

    A reference's SourceOccurrence establishes placement/context. Traversing its
    whole definition would incorrectly depend on every unrelated history branch.
    SourceObject supplies the actual geometry dependency instead.
    """
    found, pending = set(), list(obj.OutList)
    while pending:
        dep = pending.pop()
        if dep == obj or dep in found:
            continue
        if getattr(dep, "ComponentRole", "") in ("Definition", "Occurrence", "Document"):
            continue
        found.add(dep)
        pending.extend(dep.OutList)
    return list(found)


def current_shape(obj):
    """Never certify stale native caches as evaluated component results."""
    for dep in [obj] + geometry_dependencies(obj):
        if "Invalid" in dep.State or "Touched" in dep.State:
            raise ValueError("Geometry requires update or repair: " + dep.Label)
        if getattr(dep, "UserSuppressed", False) or getattr(dep, "ResultStatus", "Ready") != "Ready":
            raise ValueError("Geometry is unavailable: " + dep.Label)
    if obj.Shape.isNull():
        raise ValueError("The selected object has no evaluated geometry.")
    return obj.Shape.copy()


class PersistentProxy:
    def dumps(self):
        return None

    def loads(self, state):
        pass


class ResultProxy(PersistentProxy):
    def execute(self, obj):
        if getattr(obj, "UserSuppressed", False):
            if not obj.Frozen:
                obj.Shape = Part.Shape()
            obj.ResultStatus = "Suppressed"
            return
        if obj.Frozen:
            obj.ResultStatus = "Ready" if not obj.Shape.isNull() else "Unavailable"
            return
        obj.Shape = Part.Shape()
        obj.ResultStatus = "Unavailable"
        source = obj.Producer
        if source is None or "Invalid" in source.State:
            return
        if getattr(source, "UserSuppressed", False) or any(
                getattr(dep, "ResultStatus", "Ready") != "Ready" or getattr(dep, "UserSuppressed", False)
                for dep in [source] + geometry_dependencies(source)):
            return
        shape = getattr(source, obj.OutputProperty, None)
        if shape is None or shape.isNull():
            return
        obj.GeometryKind = _shape_kind(shape)
        obj.Placement = shape.Placement
        obj.Shape = shape.copy()
        obj.ResultStatus = "Ready"


def publish_result(component, operation, label="Body", output_property="Shape"):
    if owner(operation) != component:
        raise ValueError("The operation must belong to the active component.")
    shape = getattr(operation, output_property)
    kind = _shape_kind(shape)
    result = component.Document.addObject("Part::FeaturePython", "Result")
    result.Label = label
    register_object(component, result, "Result", True)
    _property(result, "Link", "Producer", operation, True)
    _property(result, "String", "OutputProperty", output_property, True)
    _property(result, "Bool", "Frozen", False, True)
    _property(result, "String", "GeometryKind", kind, True)
    _property(result, "String", "ResultStatus", "Unavailable", True)
    result.Proxy = ResultProxy()
    destructive = {"Part::Cut", "Part::Fuse", "Part::MultiFuse", "Part::Common",
                   "Part::MultiCommon", "Part::Fillet", "Part::Chamfer"}
    if operation.TypeId in destructive and not hasattr(operation, "ConsumedResults"):
        sources = [o for o in operation.OutList if owner(o) == component
                   and getattr(o, "ComponentRole", "") in ("Result", "Reference", "Object")
                   and o.Name in component.ResultObjects]
        _property(operation, "LinkList", "ConsumedResults", sources, True)
        _property(operation, "String", "PreviousVisibility",
                  json.dumps({o.ObjectId: _observer.previous_visibility(o) for o in sources}), True)
        for source in sources:
            source.Visibility = False
    if App.GuiUp:
        result.ViewObject.Proxy = 0
        result.Visibility = True
        operation.Visibility = False
    return result


def extrude(component, profile, length, label="Extrude"):
    if owner(profile) != component:
        raise ValueError("Add a local sketch or a direct-child reference before extruding.")
    if length <= 0:
        raise ValueError("Extrusion length must be positive.")
    with transaction(component.Document, "Extrude"):
        operation = component.Document.addObject("Part::Extrusion", "Extrude")
        operation.Label = label
        register_object(component, operation, "Operation")
        operation.Base = profile
        operation.DirMode = "Normal"
        operation.LengthFwd = length
        operation.Solid = True
        component.Document.recompute()
        if "Invalid" in operation.State:
            raise ValueError("Extrusion failed; repair the profile.")
        result = publish_result(component, operation)
        if App.GuiUp:
            profile.Visibility = False
    return operation, result


def _reference_source(parent, occurrence, source):
    if occurrence not in children(parent) or occurrence.LinkedObject is None:
        raise ValueError("Select an instance directly under the active component.")
    definition = occurrence.LinkedObject
    if occurrence.Scale != 1 or tuple(occurrence.ScaleVector) != (1, 1, 1):
        raise ValueError("Scaled component references require explicit scale support.")
    if owner(source) != definition or source not in definition.Group:
        raise ValueError("Reference objects must belong to that direct child, not a grandchild.")
    if getattr(source, "ComponentRole", "") in ("Occurrence", "Definition", "Operation"):
        raise ValueError("Select an evaluated object, not a component or generating operation.")
    if _reachable(definition, parent):
        raise ValueError("The reference would create a dependency cycle.")
    shape = current_shape(source)
    kind = _shape_kind(shape, source.isDerivedFrom("Sketcher::SketchObject")
                       or getattr(source, "GeometryKind", "") == "Dumb Sketch")
    # Source.Shape includes its local placement. The instance places the definition
    # in the parent's coordinates; do not apply the definition placement twice.
    placement = occurrence.LinkPlacement
    if occurrence.LinkTransform:
        placement = placement.multiply(definition.Placement)
    shape.transformShape(placement.toMatrix())
    return shape, kind


def _reference_status(obj, status, message=""):
    if not hasattr(obj, "ReferenceError"):
        _property(obj, "String", "ReferenceError", "", True)
    obj.ResultStatus = status
    obj.ReferenceError = message


def _invalidate_reference(obj, status, message):
    obj.Shape = Part.Shape()
    _reference_status(obj, status, message)
    # Native failures can skip result proxies. Clear their caches immediately.
    for consumer in obj.InListRecursive:
        if getattr(consumer, "ComponentRole", "") == "Result" and not consumer.Frozen:
            consumer.Shape = Part.Shape()
            consumer.ResultStatus = "Unavailable"


class ReferenceProxy(PersistentProxy):
    def execute(self, obj):
        # Pending snapshots are never accepted by current_shape consumers.
        if getattr(obj, "UserSuppressed", False):
            _invalidate_reference(obj, "Suppressed", "")
        elif obj.SourceOccurrence is None or obj.SourceObject is None:
            _invalidate_reference(obj, "Missing source", "Choose a replacement object from a direct child component.")
        else:
            _reference_status(obj, "Pending")


def add_reference(parent, occurrence, source):
    shape, kind = _reference_source(parent, occurrence, source)
    with transaction(parent.Document, "Add Reference Object"):
        obj = parent.Document.addObject("Part::FeaturePython", "ReferenceObject")
        obj.Label = source.Label + " reference"
        register_object(parent, obj, "Reference", kind in ("Body", "Sheet"))
        _property(obj, "Link", "SourceOccurrence", occurrence, True)
        _property(obj, "XLink", "SourceObject", source, True)
        _property(obj, "String", "SourceObjectId", source.ObjectId, True)
        _property(obj, "String", "GeometryKind", kind, True)
        _property(obj, "String", "ResultStatus", "Pending", True)
        _property(obj, "String", "ReferenceError", "", True)
        obj.Proxy = ReferenceProxy()
        if App.GuiUp:
            obj.ViewObject.Proxy = 0
        obj.Placement = shape.Placement
        obj.Shape = shape
    activate(parent, strict=False)
    return obj


def activate(component, strict=True):
    """Refresh all independent references before reporting any broken branches."""
    doc = component.Document
    doc.recompute()
    issues = []
    for obj in history(component):
        if getattr(obj, "ComponentRole", "") != "Reference":
            continue
        if getattr(obj, "UserSuppressed", False):
            _invalidate_reference(obj, "Suppressed", "")
            obj.purgeTouched()
            continue
        try:
            if obj.SourceOccurrence is None or obj.SourceObject is None:
                raise ValueError("The source is missing. Choose an object from a direct child component.")
            if obj.SourceObject.ObjectId != obj.SourceObjectId:
                raise ValueError("The source identity changed; repair the reference.")
            shape, kind = _reference_source(component, obj.SourceOccurrence, obj.SourceObject)
            if kind != obj.GeometryKind:
                raise ValueError("The source geometry kind changed. Review the reference and its dependent operations.")
            obj.Placement = shape.Placement
            obj.Shape = shape
            _reference_status(obj, "Ready")
            obj.purgeTouched()
            for consumer in obj.InListRecursive:
                if consumer != component and hasattr(consumer, "Shape"):
                    consumer.touch()
        except Exception as error:
            status = "Missing source" if obj.SourceOccurrence is None or obj.SourceObject is None else "Needs repair"
            _invalidate_reference(obj, status, str(error))
            obj.purgeTouched()
            issues.append((obj, str(error)))
    doc.recompute()
    if strict and issues:
        raise ValueError("\n".join(obj.Label + ": " + message for obj, message in issues))
    return issues


def _check_reference_rebind(reference):
    consumers = [obj for obj in reference.InList if obj != owner(reference)]
    for obj in [reference] + consumers:
        if obj.ExpressionEngine:
            raise ValueError("Expression-driven consumers need an explicit reference-remapping review.")
        for name in obj.PropertiesList:
            if "LinkSub" not in obj.getTypeIdOfProperty(name):
                continue
            value = getattr(obj, name)
            values = (value or []) if "List" in obj.getTypeIdOfProperty(name) else [value]
            if any(binding[0] == reference and any(binding[1]) for binding in values if binding and binding[0]):
                raise ValueError("Face or edge consumers need an explicit reference-remapping review before changing this source.")


def _check_reference_dependents(reference):
    for obj in reference.InListRecursive:
        if not hasattr(obj, "Shape") or getattr(obj, "UserSuppressed", False):
            continue
        dependencies = geometry_dependencies(obj)
        if reference not in dependencies:
            continue
        blocked = any(getattr(dep, "UserSuppressed", False)
                      or (getattr(dep, "ComponentRole", "") == "Reference" and dep.ResultStatus != "Ready")
                      for dep in dependencies)
        if not blocked and ("Invalid" in obj.State or getattr(obj, "ResultStatus", "Ready") != "Ready"):
            raise ValueError("A dependent operation could not use the replacement geometry: " + obj.Label)


def repair_reference(parent, reference, occurrence, source):
    """Retarget whole evaluated geometry while preserving the reference identity."""
    if owner(reference) != parent or getattr(reference, "ComponentRole", "") != "Reference":
        raise ValueError("Select a reference object in the active component.")
    shape, kind = _reference_source(parent, occurrence, source)
    if kind != reference.GeometryKind:
        raise ValueError("Choose the same geometry kind as the reference: " + reference.GeometryKind + ".")
    if source == reference or reference in source.OutListRecursive:
        raise ValueError("The selected source would introduce a dependency cycle.")
    changed_source = (reference.SourceObject != source or reference.SourceOccurrence != occurrence
                      or reference.SourceObjectId != source.ObjectId)
    if changed_source:
        _check_reference_rebind(reference)
    try:
        with transaction(parent.Document, "Repair Reference Object"):
            reference.SourceOccurrence = occurrence
            reference.SourceObject = source
            reference.SourceObjectId = source.ObjectId
            reference.Placement = shape.Placement
            reference.Shape = shape
            activate(parent, strict=False)
            _check_reference_dependents(reference)
    except Exception:
        activate(parent, strict=False)
        raise
    return reference


def _path(root, ids):
    node = root
    chain = []
    for ident in ids:
        matches = [c for c in children(node) if c.ObjectId == ident]
        if len(matches) != 1 or matches[0].LinkedObject is None:
            raise ValueError("The occurrence path is missing or ambiguous.")
        link = matches[0]
        chain.append(link)
        node = link.LinkedObject
    return chain


def representation_overrides(root, updates):
    overrides = json.loads(root.RepresentationOverrides)
    for ids, value in updates:
        if not _path(root, ids) or (value is not None and value not in TYPES):
            raise ValueError("Select a component path and a valid representation.")
        key = "/".join(ids)
        if value is None:
            overrides.pop(key, None)
        else:
            overrides[key] = value
    return overrides


def set_representations(root, updates, show=False):
    """Apply a reviewed group of occurrence-path changes in one undo transaction."""
    updates = list(updates)
    overrides = representation_overrides(root, updates)
    with transaction(root.Document, "Component representation"):
        root.RepresentationOverrides = json.dumps(overrides, sort_keys=True)
        if show and App.GuiUp:
            for ids, unused in updates:
                for link in _path(root, ids):
                    # Never change an external definition's stored view properties.
                    # Its inherited Hidden ancestors still govern representation.
                    if link.Document == root.Document:
                        link.Visibility = True


def set_representation(root, ids, value=None):
    set_representations(root, [(ids, value)])


def representation(root, ids, root_overrides=None):
    chain = _path(root, ids)
    for depth, link in enumerate(chain):
        value = str(link.Representation)
        # Closest definition's rule first; outer edit-context rules override it.
        for start in range(depth, -1, -1):
            context = root if start == 0 else chain[start - 1].LinkedObject
            key = "/".join(ids[start:depth + 1])
            overrides = root_overrides if start == 0 and root_overrides is not None else json.loads(context.RepresentationOverrides)
            value = overrides.get(key, value)
        if value == "Hidden":
            return value
    return value if chain else "Full Component"


def extract_dumb(component, source):
    if owner(source) != component:
        raise ValueError("Select an object in the active component.")
    shape = current_shape(source)
    kind = _shape_kind(shape, source.isDerivedFrom("Sketcher::SketchObject")
                       or getattr(source, "GeometryKind", "") == "Dumb Sketch")
    with transaction(component.Document, "Extract Dumb Body"):
        obj = component.Document.addObject("Part::Feature", "DumbObject")
        obj.Label = source.Label + " copy"
        register_object(component, obj, "Object", kind in ("Body", "Sheet"))
        _property(obj, "String", "GeometryKind", kind, True)
        obj.Placement = shape.Placement
        obj.Shape = shape
    return obj


def delete_parameters(component, result):
    proxy = getattr(result, "Proxy", None)
    if owner(result) != component or not isinstance(proxy, (ResultProxy, ReferenceProxy)):
        raise ValueError("Select a published body or sheet result in the active component.")
    shape = current_shape(result)
    _shape_kind(shape)
    is_reference = isinstance(proxy, ReferenceProxy)
    producer = None if is_reference else result.Producer
    candidates = set([producer] + list(producer.OutListRecursive)) if producer else set()
    candidates = {o for o in candidates if owner(o) == component}
    # Only delete an upstream object when all its engineering consumers are also
    # deleted. Component grouping is ownership, not a consumer. Shared producers
    # (including their other output roles) therefore remain intact.
    removable = set(candidates)
    while True:
        blocked = {o for o in removable if any(
            consumer not in removable and consumer not in (result, component)
            for consumer in o.InList)}
        if not blocked:
            break
        removable -= blocked
    if any(o.ExpressionEngine for o in [result] + list(removable)):
        raise ValueError("Expression references need an explicit conversion review before deleting parameters.")
    with transaction(component.Document, "Delete Parameters"):
        if is_reference:
            result.SourceObject = None
            result.SourceOccurrence = None
            _property(result, "Link", "Producer", None, True)
            _property(result, "String", "OutputProperty", "Shape", True)
            _property(result, "Bool", "Frozen", True, True)
            result.ComponentRole = "Result"
            result.Proxy = ResultProxy()
        result.Frozen = True
        result.Producer = None
        result.Placement = shape.Placement
        result.Shape = shape
        result.ResultStatus = "Ready"
        removed_names = {o.Name for o in removable}
        component.ModelHistory = [n for n in component.ModelHistory if n not in removed_names]
        component.ResultObjects = [n for n in component.ResultObjects if n not in removed_names]
        for name in removed_names:
            component.Document.removeObject(name)
    return result


def _copy_override_plan(occurrence):
    """Find path segments owned by the definition being separated, before relinking."""
    plan = []
    for doc in App.listDocuments().values():
        for component in definitions(doc):
            values = json.loads(component.RepresentationOverrides)
            affected = {}
            for key in values:
                ids = key.split("/")
                if occurrence.ObjectId not in ids[:-1]:
                    continue
                chain = _path(component, ids)
                if occurrence not in chain[:-1]:
                    continue
                if doc != occurrence.Document:
                    raise ValueError("Another open file has nested display overrides for this instance. "
                                     "Reset those overrides before copying the part: " + doc.Label)
                affected[key] = chain.index(occurrence) + 1
            if affected:
                plan.append((component, values, affected))
    return plan


def make_independent(occurrence, label=None):
    """Copy one definition's owned objects; child definitions stay shared."""
    parent = owner(occurrence)
    if not is_component(parent) or occurrence not in children(parent):
        raise ValueError("Select a direct component instance.")
    source = occurrence.LinkedObject
    if not is_component(source):
        raise ValueError("Locate the missing component file before copying this instance.")
    members = list(source.Group)
    if any(o.ExpressionEngine for o in [source] + members):
        raise ValueError("Expression-driven definition copies require reviewed expression remapping.")
    override_plan = _copy_override_plan(occurrence)
    references = [obj for obj in history(parent)
                  if getattr(obj, "ComponentRole", "") == "Reference" and obj.SourceOccurrence == occurrence]
    for reference in references:
        if (reference.SourceObject is None or reference.SourceObject not in members
                or reference.SourceObjectId != reference.SourceObject.ObjectId):
            raise ValueError("Repair this instance's reference objects before copying the part: " + reference.Label)
        _check_reference_rebind(reference)
    with transaction(parent.Document, "Copy to New Part"):
        originals = [source] + members + [source.Origin] + list(source.Origin.OriginFeatures)
        copied = parent.Document.copyObject(originals, False)
        mapping = {old.Name: new for old, new in zip(originals, copied)}
        definition = mapping[source.Name]
        definition.Label = label or source.Label + " copy"
        for obj in copied:
            if hasattr(obj, "ObjectId"):
                obj.ObjectId = str(uuid.uuid4())
        definition.ModelHistory = [mapping[name].Name for name in source.ModelHistory]
        definition.ResultObjects = [mapping[name].Name for name in source.ResultObjects]
        id_map = {old.ObjectId: mapping[old.Name].ObjectId for old in members if hasattr(old, "ObjectId")}
        definition.RepresentationOverrides = json.dumps({
            "/".join(id_map.get(part, part) for part in key.split("/")): value
            for key, value in json.loads(source.RepresentationOverrides).items()})
        for old in members:
            new = mapping[old.Name]
            if getattr(old, "ComponentRole", "") == "Occurrence":
                new.setLink(old.LinkedObject)
            if getattr(new, "ComponentRole", "") == "Reference" and new.SourceObject:
                new.SourceObjectId = new.SourceObject.ObjectId
            if hasattr(new, "PreviousVisibility"):
                new.PreviousVisibility = json.dumps({id_map.get(key, key): value
                    for key, value in json.loads(old.PreviousVisibility).items()})
        for component, values, affected in override_plan:
            remapped = {}
            for key, value in values.items():
                ids = key.split("/")
                if key in affected:
                    index = affected[key]
                    ids[index] = id_map[ids[index]]
                remapped["/".join(ids)] = value
            component.RepresentationOverrides = json.dumps(remapped, sort_keys=True)
        placement = App.Placement(occurrence.LinkPlacement)
        occurrence.setLink(definition)
        occurrence.DefinitionId = definition.ObjectId
        if hasattr(occurrence, "InstanceNumber"):
            occurrence.InstanceNumber = 1
        occurrence.LinkPlacement = placement
        for reference in references:
            reference.SourceObject = mapping[reference.SourceObject.Name]
            reference.SourceObjectId = reference.SourceObject.ObjectId
        # Refresh copied associative objects before their new parent consumers.
        activate(definition, strict=False)
        if references:
            activate(parent, strict=False)
            for reference in references:
                if not suppression_sources(reference) and reference.ResultStatus != "Ready":
                    raise ValueError("The copied reference could not be refreshed: " + reference.Label)
                _check_reference_dependents(reference)
        validate(parent.Document)
    return definition


def suppression_sources(obj):
    """Authored flags, including upstream flags, independent of cached shapes."""
    return [dep for dep in [obj] + geometry_dependencies(obj)
            if getattr(dep, "UserSuppressed", False)]


def _consumed_results(items, blocked):
    return {source for operation in items if not blocked[operation]
            for source in getattr(operation, "ConsumedResults", [])}


def set_items_suppressed(items, suppressed):
    """Change explicit flags together; dependent inactivity is always derived."""
    items = list(dict.fromkeys(items))
    if not items:
        return
    component = owner(items[0])
    if (not is_component(component)
            or any(owner(obj) != component or obj not in history(component) for obj in items)):
        raise ValueError("Select items from the active component's Model History.")
    items = [obj for obj in items if bool(getattr(obj, "UserSuppressed", False)) != bool(suppressed)]
    if not items:
        return
    doc = component.Document
    # Reference/result consumers in other local definitions also need invalidation.
    members = [obj for definition in definitions(doc) for obj in history(definition)]
    before = {obj: bool(suppression_sources(obj)) for obj in members}
    consumed_before = _consumed_results(members, before)
    with transaction(doc, "Suppress items" if suppressed else "Unsuppress items"):
        for obj in items:
            if not hasattr(obj, "UserSuppressed"):
                _property(obj, "Bool", "UserSuppressed", False)
            obj.UserSuppressed = bool(suppressed)
        after = {obj: bool(suppression_sources(obj)) for obj in members}
        consumed_after = _consumed_results(members, after)
        for obj in members:
            if before[obj] == after[obj]:
                continue
            if App.GuiUp:
                if after[obj]:
                    if not hasattr(obj, "SuppressionVisibility"):
                        _property(obj, "Bool", "SuppressionVisibility", bool(obj.Visibility), True)
                    obj.SuppressionVisibility = bool(obj.Visibility)
                    obj.Visibility = False
                else:
                    obj.Visibility = getattr(obj, "SuppressionVisibility", False)
            if hasattr(obj, "Shape"):
                # Native failure may prevent downstream proxies from executing.
                if after[obj] and getattr(obj, "ComponentRole", "") == "Result" and not obj.Frozen:
                    obj.Shape = Part.Shape()
                    obj.ResultStatus = "Unavailable"
                obj.touch()
        if App.GuiUp:
            all_consumed = {source for operation in members
                            for source in getattr(operation, "ConsumedResults", [])}
            restored = {obj for obj in members if before[obj] and not after[obj]}
            for source in (consumed_before | (restored & all_consumed)) - consumed_after:
                # Multiple consumers may have recorded different visibility as
                # they were created. Restore only when the last active one ends.
                was_visible = any(json.loads(operation.PreviousVisibility).get(source.ObjectId, False)
                                  for operation in members
                                  if source in getattr(operation, "ConsumedResults", []))
                if not after.get(source, False):
                    source.Visibility = was_visible
            for source in (consumed_after - consumed_before) | (restored & consumed_after):
                source.Visibility = False
        # Refresh associative snapshots within the same Undo transaction, after
        # eligibility changes. This also restores consumers across definitions.
        if not suppressed:
            for definition in definitions(doc):
                if any(getattr(obj, "ComponentRole", "") == "Reference"
                       and before[obj] and not after[obj] for obj in history(definition)):
                    activate(definition, strict=False)


def set_suppressed(operation, suppressed):
    set_items_suppressed([operation], suppressed)


def history_detail(obj):
    sources = suppression_sources(obj)
    if sources:
        if sources[0] == obj:
            return "Suppressed explicitly. Unsuppress this item to enable it when its inputs are available."
        return "Inactive because these inputs are suppressed: " + ", ".join(dep.Label for dep in sources)
    return getattr(obj, "ReferenceError", "")


def history_state(obj):
    """Keep authored suppression distinct from unavailable inputs and failures."""
    if getattr(obj, "UserSuppressed", False):
        return "Suppressed"
    if any(getattr(dep, "UserSuppressed", False)
           or getattr(dep, "ResultStatus", "Ready") != "Ready" for dep in geometry_dependencies(obj)):
        return "Inactive — dependency"
    if "Invalid" in obj.State:
        return "Needs repair"
    if hasattr(obj, "ResultStatus"):
        return obj.ResultStatus
    if "Touched" in obj.State:
        return "Needs update"
    return "Ready"


def finished_results(component):
    items = history(component)
    consumed = _consumed_results(items, {obj: bool(suppression_sources(obj)) for obj in items})
    results = [component.Document.getObject(name) for name in component.ResultObjects]
    return [obj for obj in results if obj is not None and obj not in consumed
            and history_state(obj) == "Ready" and not obj.Shape.isNull()]


def externalize(definition, filename):
    """Move an embedded definition closure, retaining shared identities and links."""
    doc = definition.Document
    if metadata(doc).RootComponent == definition:
        raise ValueError("Use Save As for a root component.")
    if not doc.FileName.lower().endswith(".cadprt"):
        raise ValueError("Save the owning component document before externalizing a definition.")
    destination = Path(filename).resolve()
    if destination.suffix.lower() != ".cadprt" or destination.exists():
        raise ValueError("Choose a new .cadprt file; externalization never overwrites another definition.")
    closure = []
    def collect(component):
        if component in closure:
            return
        closure.append(component)
        for child in children(component):
            if not is_component(child.LinkedObject):
                raise ValueError("Repair missing components before externalizing.")
            if child.LinkedObject.Document == doc:
                collect(child.LinkedObject)
    collect(definition)
    originals = []
    for component in closure:
        originals.extend([component] + list(component.Group) + [component.Origin]
                         + list(component.Origin.OriginFeatures))
    originals = list(dict.fromkeys(originals))
    own = set(originals)
    external_inputs = {dep for obj in originals for dep in obj.OutList if dep not in own}
    if (any(o.ExpressionEngine for o in originals)
            or any(dep.Document == doc or not dep.Document.FileName.lower().endswith(".cadprt")
                   for dep in external_inputs)):
        raise ValueError("Resolve external expressions and save external component dependencies first.")
    occurrences = [o for o in doc.Objects if o not in own
                   and getattr(o, "ComponentRole", "") == "Occurrence" and o.LinkedObject in closure]
    references = [o for o in doc.Objects if o not in own
                  and getattr(o, "ComponentRole", "") == "Reference" and o.SourceObject in own]
    allowed = own | set(occurrences) | set(references)
    if any(consumer not in allowed for obj in originals for consumer in obj.InList):
        raise ValueError("Other consumers must be remapped explicitly before externalizing this definition.")
    external = new_document(definition.Label)
    try:
        empty = metadata(external).RootComponent
        copied = external.copyObject(originals, False)
        mapping = {old.Name: new for old, new in zip(originals, copied)}
        new_root = mapping[definition.Name]
        for component in closure:
            copied_component = mapping[component.Name]
            copied_component.ModelHistory = [mapping[name].Name for name in component.ModelHistory]
            copied_component.ResultObjects = [mapping[name].Name for name in component.ResultObjects]
        metadata(external).RootComponent = new_root
        external.removeObject(empty.Name)
        if App.GuiUp:
            new_root.Visibility = True
        external.recompute()
        external.saveAs(str(destination))
        with transaction(doc, "Externalize Component"):
            for occurrence in occurrences:
                placement = App.Placement(occurrence.LinkPlacement)
                occurrence.setLink(mapping[occurrence.LinkedObject.Name])
                occurrence.LinkPlacement = placement
            for reference in references:
                reference.SourceObject = mapping[reference.SourceObject.Name]
            names = [o.Name for o in originals]
            for name in names:
                if doc.getObject(name):
                    doc.removeObject(name)
            validate(doc)
        return new_root
    except Exception:
        App.closeDocument(external.Name)
        raise


def validate(doc, allow_unresolved=False):
    meta = metadata(doc)
    if meta.SchemaVersion != SCHEMA or not is_component(meta.RootComponent):
        raise ValueError("Unsupported component schema or missing root component.")
    ids = [o.ObjectId for o in doc.Objects if hasattr(o, "ObjectId")]
    if len(ids) != len(set(ids)) or any(not value for value in ids):
        raise ValueError("Duplicate or missing component object identities.")
    for component in definitions(doc):
        members = {o.Name for o in component.Group}
        if (len(component.ModelHistory) != len(set(component.ModelHistory))
                or not set(component.ModelHistory) <= members
                or not set(component.ResultObjects) <= members):
            raise ValueError("Invalid component history/result membership.")
        for child in children(component):
            if not is_component(child.LinkedObject):
                if allow_unresolved and child.LinkedObject is None:
                    continue
                raise ValueError("Unresolved component: " + child.Label)
            if hasattr(child, "DefinitionId") and child.DefinitionId != child.LinkedObject.ObjectId:
                raise ValueError("The linked component definition identity changed; repair is required.")
            if _reachable(child.LinkedObject, component):
                raise ValueError("Cyclic component structure.")
        for key, value in json.loads(component.RepresentationOverrides).items():
            if not allow_unresolved:
                _path(component, key.split("/"))
            if value not in TYPES:
                raise ValueError("Unsupported representation override.")
    return meta


def repair_component(parent, occurrence, filename):
    if occurrence not in children(parent):
        raise ValueError("Select a direct component instance to repair.")
    import CadDocument
    source = CadDocument.open(filename)
    matches = [d for d in definitions(source) if d.ObjectId == occurrence.DefinitionId]
    if len(matches) != 1:
        raise ValueError("That file does not contain the saved component definition identity.")
    definition = matches[0]
    if _reachable(definition, parent):
        raise ValueError("Repair would introduce a component cycle.")
    with transaction(parent.Document, "Repair Component"):
        placement = App.Placement(occurrence.LinkPlacement)
        occurrence.setLink(definition)
        occurrence.LinkPlacement = placement
        for obj in history(parent):
            if getattr(obj, "ComponentRole", "") != "Reference" or obj.SourceOccurrence != occurrence:
                continue
            candidates = [o for o in definition.Group if getattr(o, "ObjectId", "") == obj.SourceObjectId]
            if len(candidates) != 1:
                raise ValueError("A saved reference object is missing or ambiguous in the selected component.")
            obj.SourceObject = candidates[0]
        activate(parent)
    return definition


class ComponentObserver:
    """Adopt completed native commands inside their existing undo transaction."""
    def __init__(self):
        self.busy = False
        self.visibility = {}

    def slotOpenTransaction(self, doc, label):
        self.visibility[doc.Name] = {o.ObjectId: bool(o.Visibility) for o in doc.Objects
                                     if hasattr(o, "ObjectId") and hasattr(o, "Visibility")}

    def slotCommitTransaction(self, doc):
        self.visibility.pop(doc.Name, None)

    def slotAbortTransaction(self, doc):
        self.visibility.pop(doc.Name, None)

    def slotDeletedDocument(self, doc):
        self.visibility.pop(doc.Name, None)

    def previous_visibility(self, obj):
        return self.visibility.get(obj.Document.Name, {}).get(obj.ObjectId, bool(obj.Visibility))

    def slotBeforeCloseTransaction(self, abort):
        if abort or self.busy:
            return
        self.busy = True
        try:
            for doc in list(App.listDocuments().values()):
                if not doc.HasPendingTransaction:
                    continue
                if not any(getattr(o, "ComponentRole", "") == "Document" for o in doc.Objects):
                    continue
                changed = False
                for component in definitions(doc):
                    members = {o.Name for o in component.Group}
                    ordered = [n for n in component.ModelHistory if n in members]
                    results = [n for n in component.ResultObjects if n in members]
                    if ordered != list(component.ModelHistory):
                        component.ModelHistory = ordered
                    if results != list(component.ResultObjects):
                        component.ResultObjects = results
                    for obj in list(component.Group):
                        if not hasattr(obj, "Shape") or hasattr(obj, "ComponentRole"):
                            continue
                        plain = obj.TypeId == "Part::Feature" or obj.isDerivedFrom("Sketcher::SketchObject")
                        register_object(component, obj, "Object" if plain else "Operation")
                        changed = True
                        if obj.Shape.isNull() or not obj.Shape.isValid():
                            continue
                        if obj.Shape.Solids or obj.Shape.Faces:
                            if plain:
                                component.ResultObjects = list(component.ResultObjects) + [obj.Name]
                            elif len(obj.Shape.Solids) <= 1:
                                publish_result(component, obj, obj.Label + " result")
                if changed:
                    doc.recompute()
        finally:
            self.busy = False


_observer = ComponentObserver()
App.addDocumentObserver(_observer)
