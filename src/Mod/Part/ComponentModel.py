# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component ownership and evaluated-result services for FreeCAD Plus.

Native objects, links, transactions and geometry remain the storage/compute engine.
History ordering is metadata: it must not introduce reverse dependency edges.
"""
from contextlib import contextmanager
import json
import re
from pathlib import Path
import uuid

import FreeCAD as App
import Part

# Runtime-only History rollback. Authored suppression and saved document data stay intact.
_edit_rollbacks = {}


def edit_suppressed(obj):
    return any(obj in items for items in _edit_rollbacks.values())


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
    items = [o for o in doc.Objects if is_component(o)]
    roots = [o.RootComponent for o in doc.Objects
             if getattr(o, "ComponentRole", "") == "Document"]
    return [o for o in roots if o in items] + [o for o in items if o not in roots]


def tree_roots(doc):
    """Master first, followed by independent unused definition assemblies.

    These extra roots are inventory contexts, never new links in the master.
    An unused assembly's descendants appear beneath it rather than twice.
    """
    master = metadata(doc).RootComponent
    covered = set()
    def visit(component):
        if component in covered:
            return
        covered.add(component)
        for link in children(component):
            if is_component(link.LinkedObject):
                visit(link.LinkedObject)
    visit(master)
    unused = [o for o in definitions(doc) if o not in covered]
    nested = {link.LinkedObject for o in unused for link in children(o)}
    roots = [master]
    for component in [o for o in unused if o not in nested] + unused:
        if component not in covered:
            roots.append(component)
            visit(component)
    return roots


def next_part_label(doc):
    """Reserve visible part names throughout this component document."""
    labels = {obj.Label.casefold() for obj in doc.Objects}
    labels.update(obj.LinkedObject.Label.casefold() for obj in doc.Objects
                  if getattr(obj, "ComponentRole", "") == "Occurrence" and obj.LinkedObject)
    number = 1
    while f"Part{number:03d}".casefold() in labels:
        number += 1
    return f"Part{number:03d}"


def _definition(doc, label=None):
    label = label or next_part_label(doc)
    obj = doc.addObject("App::Part", "Component")
    obj.Label = label
    _identity(obj, "Definition")
    _property(obj, "StringList", "ModelHistory", [], True)
    _property(obj, "StringList", "ResultObjects", [], True)
    _property(obj, "String", "RepresentationOverrides", "{}", True)
    if App.GuiUp:
        obj.Visibility = False
    return obj


def new_document(label=None):
    if label is None:
        occupied = {value.casefold() for existing in App.listDocuments().values()
                    for value in (existing.Name, existing.Label, Path(existing.FileName).stem)}
        number = 1
        while "untitled" + f"{number:03d}" in occupied:
            number += 1
        doc = App.newDocument("untitled" + f"{number:03d}")
        doc.Label = "untitled" + f"{number:03d}"
        label = next_part_label(doc)
    else:
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


def create_definition(doc, label=None):
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


def instance_counts(root):
    """Count placed occurrences, expanding repeated parents without counting definitions."""
    counts = {}
    def visit(component, ancestors):
        key = (component.Document.Name, component.ObjectId)
        if key in ancestors:
            return
        for link in children(component):
            definition = link.LinkedObject
            if definition is not None:
                counts[definition] = counts.get(definition, 0) + 1
                visit(definition, ancestors | {key})
    visit(root, set())
    return counts


def remove_instances(occurrences):
    """Remove only owning links; retain models, geometry and reference identities."""
    occurrences = list(dict.fromkeys(occurrences))
    if not occurrences:
        return
    doc = occurrences[0].Document
    if any(obj.Document != doc or getattr(obj, "ComponentRole", "") != "Occurrence"
           or not is_component(owner(obj)) for obj in occurrences):
        raise ValueError("Select linked instances from one owning file.")
    ids = {obj.ObjectId for obj in occurrences}
    with transaction(doc, "Delete assembly instances"):
        for component in definitions(doc):
            overrides = json.loads(component.RepresentationOverrides)
            component.RepresentationOverrides = json.dumps(
                {path: value for path, value in overrides.items() if not ids.intersection(path.split("/"))})
        for obj in occurrences:
            doc.removeObject(obj.Name)
        # References keep their own identity, but no longer have a placed source.
        for component in definitions(doc):
            activate(component, strict=False)


def _component_frame(root, ids):
    """Native occurrence frame, including linked definition and Part placements."""
    chain = _path(root, ids)
    component = chain[-1].LinkedObject if chain else root
    path = "".join(link.Name + "." for link in chain) + component.Origin.Name + "."
    frame = root.getSubObject(path, 3)
    if frame is None:
        raise ValueError("The component placement context is unavailable.")
    return frame


def move_instances(root, paths, destination_ids=(), before=None):
    """Reorder/reparent existing links atomically; never recreate model identities."""
    paths = [tuple(path) for path in paths]
    destination_ids = tuple(destination_ids)
    if not paths or any(not path for path in paths):
        raise ValueError("Select linked instances; the top-level part cannot be moved.")
    if any(path[:len(other)] == other for path in paths for other in paths if path != other):
        raise ValueError("Move a parent or its children, not both together.")
    chain = _path(root, destination_ids)
    destination = chain[-1].LinkedObject if chain else root
    doc = root.Document
    links = [_path(root, path)[-1] for path in paths]
    if len(set(links)) != len(links):
        raise ValueError("Select each owning instance only once.")
    if destination.Document != doc or any(link.Document != doc for link in links):
        raise ValueError("Rearrange instances in their owning file; external models must be edited in their own tab.")
    if before is not None and (before not in children(destination) or before in links):
        raise ValueError("Choose a sibling outside the moved selection.")
    placements = {}
    reparented = [link for link in links if owner(link) != destination]
    if reparented:
        destination_frame = _component_frame(root, destination_ids)
        for link, path in zip(links, paths):
            if link not in reparented:
                continue
            if _reachable(link.LinkedObject, destination):
                raise ValueError("A part cannot be moved into itself or its descendants.")
            if (link.ExpressionEngine or link.ElementCount or link.Scale != 1
                    or tuple(link.ScaleVector) != (1, 1, 1)
                    or "ReadOnly" in link.getPropertyStatus("LinkPlacement")):
                raise ValueError("Driven, scaled or read-only instances need their relationship editor.")
            if any(consumer != owner(link) for consumer in link.InList):
                raise ValueError("This instance has references or assembly relationships. Reorder it within its parent or repair those relationships before moving it.")
            # Explicit path overrides cannot silently become invalid or apply to
            # another occurrence when a shared definition changes ownership.
            if any(link.ObjectId in key.split("/") for component in definitions(doc)
                   for key in json.loads(component.RepresentationOverrides)):
                raise ValueError("Reset this instance's path display overrides before moving it to another parent.")
            placements[link] = destination_frame.inverse().multiply(
                _component_frame(root, path[:-1])).multiply(link.LinkPlacement)
    groups = {owner(link): list(owner(link).Group) for link in links}
    groups.setdefault(destination, list(destination.Group))
    for component in groups:
        groups[component] = [obj for obj in groups[component] if obj not in links]
    index = groups[destination].index(before) if before else len(groups[destination])
    groups[destination][index:index] = links
    if not reparented and all(list(component.Group) == group for component, group in groups.items()):
        return False
    with transaction(doc, "Rearrange Part Tree"):
        for link in reparented:
            owner(link).removeObject(link)
        for component, group in groups.items():
            component.Group = group
        for link, placement in placements.items():
            link.LinkPlacement = placement
        # Preserve existing persistent numbers unless the new parent has a clash.
        used = {}
        for link in children(destination):
            if link in reparented:
                continue
            used.setdefault(link.LinkedObject, set()).add(link.InstanceNumber)
        for link in reparented:
            peers = used.setdefault(link.LinkedObject, set())
            number = link.InstanceNumber
            if number in peers:
                number = max(peers) + 1
                link.InstanceNumber = number
            peers.add(number)
        validate(doc, allow_unresolved=True)
    return True


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
            definition = _definition(parent.Document, label)
        link = parent.Document.addObject("App::Link", "ComponentInstance")
        parent.addObject(link)
        _identity(link, "Occurrence")
        link.setLink(definition)
        link.Label = label or definition.Label
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


def next_label(component, base, exclude=None):
    """Allocate a default label within one definition, independent of its file."""
    labels = {obj.Label for obj in component.Group if obj != exclude}
    number = 1
    while f"{base}{number:03d}" in labels:
        number += 1
    return f"{base}{number:03d}"


def register_object(component, obj, role="Object", result=False):
    if not is_component(component) or component.Document != obj.Document:
        raise ValueError("An object and its component must belong to the same file.")
    if owner(obj) not in (None, component):
        raise ValueError("An object cannot belong to two components.")
    automatic = not hasattr(obj, "ObjectId") and obj.Label == obj.Name
    if not hasattr(obj, "ObjectId"):
        _identity(obj, role)
    elif obj.ComponentRole != role:
        raise ValueError("The object's existing role cannot be changed implicitly.")
    component.addObject(obj)
    if automatic:
        obj.Label = next_label(component, re.sub(r"\d+$", "", obj.Name), obj)
    if obj.Name not in component.ModelHistory:
        component.ModelHistory = list(component.ModelHistory) + [obj.Name]
    if result and obj.Name not in component.ResultObjects:
        component.ResultObjects = list(component.ResultObjects) + [obj.Name]
    return obj


def history(component):
    return [component.Document.getObject(name) for name in component.ModelHistory
            if component.Document.getObject(name) is not None]


def history_move_order(component, items, index):
    """Plan a nearest legal insertion in visible History without changing links."""
    original = history(component)
    fixed = {component.Origin, *component.Origin.OriginFeatures}
    visible = [obj for obj in original if obj not in fixed and not background_result(obj)]
    selected = set(items)
    if not selected or not selected <= set(visible):
        raise ValueError("Select movable history items in the active component; the origin is fixed.")
    moving = [obj for obj in visible if obj in selected]
    index = max(0, min(int(index), len(visible)))
    # Published background results travel with their visible producer. Transitive
    # inputs include profile binders, expressions and hidden result links.
    predecessors = {obj: {display_object(dep) for dep in geometry_dependencies(obj)} & set(visible)
                    for obj in visible}
    remaining = [obj for obj in visible if obj not in selected]
    slot = sum(obj not in selected for obj in visible[:index])
    lower = [max((i + 1 for i, other in enumerate(remaining) if other in predecessors[obj]), default=0)
             for obj in moving]
    upper = [min((i for i, other in enumerate(remaining) if obj in predecessors[other]), default=len(remaining))
             for obj in moving]
    # Selected items retain their relative order, even when an unselected
    # predecessor must remain between them. Propagate those ordering bounds,
    # then clamp each insertion to the requested gap in the unselected sequence.
    for i in range(1, len(moving)):
        lower[i] = max(lower[i], lower[i - 1])
    for i in range(len(moving) - 2, -1, -1):
        upper[i] = min(upper[i], upper[i + 1])
    if any(lo > hi for lo, hi in zip(lower, upper)) or any(
            later in predecessors[obj] for i, obj in enumerate(moving) for later in moving[i:]):
        raise ValueError("The existing dependency order has no valid insertion position.")
    slots = [max(lo, min(slot, hi)) for lo, hi in zip(lower, upper)]
    ordered = []
    for gap in range(len(remaining) + 1):
        ordered.extend(obj for obj, position in zip(moving, slots) if position == gap)
        if gap < len(remaining):
            ordered.append(remaining[gap])
    if ordered == visible:
        return list(component.ModelHistory)
    groups = {obj: [obj.Name] for obj in visible}
    for obj in original:
        if background_result(obj):
            producer = display_object(obj)
            if producer not in groups:
                raise ValueError("Repair the history item's missing producer before reordering.")
            groups[producer].append(obj.Name)
    return [obj.Name for obj in original if obj in fixed] + [
        name for obj in ordered for name in groups[obj]]


def reorder_history(component, items, index):
    """Commit a dependency-clamped order as one undoable metadata change."""
    if component.Document.HasPendingTransaction:
        raise ValueError("Finish the active edit before reordering history.")
    ordered = history_move_order(component, items, index)
    if ordered != list(component.ModelHistory):
        with transaction(component.Document, "Reorder model history"):
            component.ModelHistory = ordered
    return ordered


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
        if edit_suppressed(dep) or getattr(dep, "UserSuppressed", False) or getattr(dep, "ResultStatus", "Ready") != "Ready":
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
        try:
            self.update_result(obj)
        finally:
            if App.GuiUp:
                import ComponentResultView
                ComponentResultView.sync(obj)

    def update_result(self, obj):
        if edit_suppressed(obj):
            return  # Keep cached geometry for native links; exclude it from available results.
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


def background_result(obj):
    return (getattr(obj, "ComponentRole", "") == "Result"
            and getattr(obj, "BackgroundResult", False) and not getattr(obj, "Frozen", False))


def display_object(obj):
    return obj.Producer if background_result(obj) and obj.Producer is not None else obj


def result_for_operation(obj):
    if getattr(obj, "ComponentRole", "") != "Operation":
        return obj
    results = [candidate for candidate in obj.InList
               if getattr(candidate, "ComponentRole", "") == "Result"
               and getattr(candidate, "Producer", None) == obj and background_result(candidate)]
    return results[0] if len(results) == 1 else obj


def prepare_result_display(component):
    """Adopt existing published bodies without replacing their reference identities."""
    if not App.GuiUp:
        return
    import ComponentResultView
    for obj in history(component):
        if (getattr(obj, "ComponentRole", "") == "Result" and hasattr(obj, "Producer")
                and obj.Producer is not None and not obj.Frozen and obj.GeometryKind == "Body"
                and obj.OutputProperty == "Shape"):
            if not hasattr(obj, "BackgroundResult"):
                _property(obj, "Bool", "BackgroundResult", True, True)
            ComponentResultView.install(obj)


def publish_result(component, operation, label="Body", output_property="Shape"):
    if owner(operation) != component:
        raise ValueError("The operation must belong to the active component.")
    shape = getattr(operation, output_property)
    kind = _shape_kind(shape)
    result = component.Document.addObject("Part::FeaturePython", "Result")
    register_object(component, result, "Result", True)
    result.Label = next_label(component, "Body", result) if label == "Body" else label
    _property(result, "Link", "Producer", operation, True)
    _property(result, "String", "OutputProperty", output_property, True)
    _property(result, "Bool", "Frozen", False, True)
    _property(result, "String", "GeometryKind", kind, True)
    _property(result, "String", "ResultStatus", "Unavailable", True)
    _property(result, "Bool", "BackgroundResult", kind == "Body" and output_property == "Shape", True)
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
        if background_result(result):
            import ComponentResultView
            ComponentResultView.install(result)
        else:
            operation.Visibility = False
    return result


def extrude(component, profile, length, label="Extrude"):
    if owner(profile) != component:
        raise ValueError("Add a local sketch or a direct-child reference before extruding.")
    if length <= 0:
        raise ValueError("Extrusion length must be positive.")
    with transaction(component.Document, "Extrude"):
        operation = component.Document.addObject("Part::Extrusion", "Extrude")
        register_object(component, operation, "Operation")
        operation.Label = next_label(component, "Extrude", operation) if label == "Extrude" else label
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
        if edit_suppressed(obj):
            return
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
        if edit_suppressed(obj) or getattr(obj, "ComponentRole", "") != "Reference":
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


def set_bom_inclusion(occurrences, included):
    """Change actual occurrence ownership, independently of display/path overrides."""
    occurrences = list(dict.fromkeys(occurrences))
    if not occurrences or any(getattr(obj, "ComponentRole", "") != "Occurrence" for obj in occurrences):
        raise ValueError("Select component instances to change BOM participation.")
    doc = occurrences[0].Document
    if any(obj.Document != doc for obj in occurrences):
        raise ValueError("Change BOM participation in one owning file at a time.")
    with transaction(doc, "Component BOM participation"):
        for obj in occurrences:
            obj.IncludeInBOM = bool(included)


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


def parameter_removal_plan(component, result):
    """Read-only review of exclusive history; component ownership is never pruned."""
    proxy = getattr(result, "Proxy", None)
    if owner(result) != component or not isinstance(proxy, (ResultProxy, ReferenceProxy)):
        raise ValueError("Select a published body or sheet result in the active component.")
    shape = current_shape(result)
    if _shape_kind(shape) not in ("Body", "Sheet"):
        raise ValueError("Delete Parameters applies to bodies and sheets. Use Extract Dumb Body for other geometry.")
    if getattr(result, "Frozen", False):
        raise ValueError("This object already has independent geometry.")
    is_reference = isinstance(proxy, ReferenceProxy)
    producer = None if is_reference else result.Producer
    candidates = set([producer] + geometry_dependencies(producer)) if producer else set()
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
    ordered = [obj for obj in component.Document.Objects if obj in candidates]
    return {"shape": shape, "remove": [obj for obj in ordered if obj in removable],
            "retain": [obj for obj in ordered if obj not in removable], "reference": is_reference}


def delete_parameters(component, result):
    plan = parameter_removal_plan(component, result)
    shape, is_reference = plan["shape"], plan["reference"]
    removable = plan["remove"]
    with transaction(component.Document, "Delete Parameters"):
        if is_reference:
            result.SourceObject = None
            result.SourceOccurrence = None
            result.SourceObjectId = ""
            if hasattr(result, "ReferenceError"):
                result.ReferenceError = ""
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
        if App.GuiUp:
            import ComponentResultView
            ComponentResultView.install(result)
        removed_names = {o.Name for o in removable}
        component.ModelHistory = [n for n in component.ModelHistory if n not in removed_names]
        component.ResultObjects = [n for n in component.ResultObjects if n not in removed_names]
        for obj in reversed(removable):
            component.Document.removeObject(obj.Name)
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
            if edit_suppressed(dep) or getattr(dep, "UserSuppressed", False)]


def _consumed_results(items, blocked):
    return {source for operation in items if not blocked[operation]
            for source in getattr(operation, "ConsumedResults", [])}


def set_items_suppressed(items, suppressed):
    """Change explicit flags together; dependent inactivity is always derived."""
    items = list(dict.fromkeys(items))
    if not items:
        return
    if any(edit_suppressed(obj) for obj in items):
        raise ValueError("Finish the current edit before changing later History items.")
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
    if edit_suppressed(obj):
        return "Temporarily suppressed while an earlier History item is being edited."
    sources = suppression_sources(obj)
    if sources:
        if sources[0] == obj:
            return "Suppressed explicitly. Unsuppress this item to enable it when its inputs are available."
        return "Inactive because these inputs are suppressed: " + ", ".join(dep.Label for dep in sources)
    if getattr(obj, "Frozen", False):
        return "Independent geometry. Generating parameters have been removed; downstream references retain this object."
    return getattr(obj, "ReferenceError", "")


def history_state(obj):
    """Keep authored suppression distinct from unavailable inputs and failures."""
    if edit_suppressed(obj):
        return "Suppressed during edit"
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
    # Refuse before creating a document or writing a destination file.
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current edit before saving a component to an external file.")
    if metadata(doc).RootComponent == definition:
        raise ValueError("Use Save As for a root component.")
    if not doc.FileName.lower().endswith(".cadprt"):
        raise ValueError("Save the owning component document before externalizing a definition.")
    destination = Path(filename).resolve()
    if destination.suffix.lower() != ".cadprt" or destination.exists():
        raise ValueError("Choose a new .cadprt file; externalization never overwrites another definition.")
    closure = []
    refresh_order = []
    def collect(component):
        if component in closure:
            return
        closure.append(component)
        for child in children(component):
            if not is_component(child.LinkedObject):
                raise ValueError("Repair missing components before externalizing.")
            if child.LinkedObject.Document == doc:
                collect(child.LinkedObject)
        refresh_order.append(component)
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
    affected = list(dict.fromkeys(owner(reference) for reference in references))
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
        # Native copying may restore an occurrence before its definition and
        # disambiguate the definition's label. Release occurrence labels first,
        # then restore definitions/members before their duplicate-allowed links.
        linked = [obj for obj in originals if getattr(obj, "ComponentRole", "") == "Occurrence"]
        for obj in linked:
            mapping[obj.Name].Label = mapping[obj.Name].Name
        for obj in originals:
            if getattr(obj, "ComponentRole", "") and obj not in linked:
                mapping[obj.Name].Label = obj.Label
        for obj in linked:
            mapping[obj.Name].Label = obj.Label
        if App.GuiUp:
            new_root.Visibility = True
        external.recompute()
        # Native copying touches reference features. Evaluate children first so
        # the saved file contains current geometry throughout the moved closure.
        for component in refresh_order:
            activate(mapping[component.Name], strict=False)
        validate(external)
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
            for component in affected:
                activate(component, strict=False)
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
    """Locate a saved definition and restore its unresolved instances in this file."""
    if occurrence not in children(parent):
        raise ValueError("Select a direct component instance to repair.")
    import CadDocument
    source = CadDocument.open(filename)
    matches = [d for d in definitions(source) if d.ObjectId == occurrence.DefinitionId]
    if len(matches) != 1:
        raise ValueError("That file does not contain the saved component definition identity.")
    definition = matches[0]
    doc = parent.Document
    targets = [link for component in definitions(doc) for link in children(component)
               if link == occurrence or (link.LinkedObject is None
                   and getattr(link, "DefinitionId", "") == occurrence.DefinitionId)]
    if any(_reachable(definition, owner(link)) for link in targets):
        raise ValueError("Repair would introduce a component cycle.")
    sources = {}
    for obj in definition.Group:
        ident = getattr(obj, "ObjectId", "")
        if ident:
            sources.setdefault(ident, []).append(obj)
    affected = list(dict.fromkeys(owner(link) for link in targets))
    with transaction(doc, "Locate Component File"):
        for link in targets:
            placement = App.Placement(link.LinkPlacement)
            link.setLink(definition)
            link.LinkPlacement = placement
        for component in affected:
            for obj in history(component):
                if getattr(obj, "ComponentRole", "") != "Reference" or obj.SourceOccurrence not in targets:
                    continue
                candidates = sources.get(obj.SourceObjectId, [])
                # Keep missing/ambiguous geometry repairable without undoing the
                # recovered component or binding a different object by its label.
                obj.SourceObject = candidates[0] if len(candidates) == 1 else None
            activate(component, strict=False)
    return definition


class ComponentObserver:
    """Adopt completed native commands inside their existing undo transaction."""
    def __init__(self):
        self.busy = False
        self.visibility = {}
        self.deleted_extrudes = {}

    def slotOpenTransaction(self, doc, label):
        self.visibility[doc.Name] = {o.ObjectId: bool(o.Visibility) for o in doc.Objects
                                     if hasattr(o, "ObjectId") and hasattr(o, "Visibility")}

    def slotCommitTransaction(self, doc):
        self.visibility.pop(doc.Name, None)

    def slotAbortTransaction(self, doc):
        self.visibility.pop(doc.Name, None)
        self.deleted_extrudes.pop(doc.Name, None)

    def slotDeletedDocument(self, doc):
        self.visibility.pop(doc.Name, None)
        self.deleted_extrudes.pop(doc.Name, None)

    def slotDeletedObject(self, obj):
        if not obj.Document.HasPendingTransaction or getattr(obj, "OperationKind", "") != "Extrude":
            return
        # Snapshot dependencies while native deletion still retains the links.
        # Apply cleanup before commit so delete/undo remains one transaction.
        dependencies = geometry_dependencies(obj)
        self.deleted_extrudes.setdefault(obj.Document.Name, []).append((
            [dep.Name for dep in dependencies if getattr(dep, "ComponentRole", "") == "Internal"],
            [dep.Name for dep in dependencies if dep.isDerivedFrom("Sketcher::SketchObject")]))

    def cleanup_extrudes(self, doc):
        for internal_names, sketch_names in self.deleted_extrudes.pop(doc.Name, []):
            pending = set(internal_names)
            while pending:
                removed = set()
                for name in pending:
                    obj = doc.getObject(name)
                    if obj is None:
                        removed.add(name)
                    elif not any(consumer != owner(obj) for consumer in obj.InList):
                        doc.removeObject(name)
                        removed.add(name)
                if not removed:
                    break  # Preserve internal inputs still used by another feature.
                pending -= removed
            for name in sketch_names:
                sketch = doc.getObject(name)
                if sketch and not any(getattr(obj, "ComponentRole", "") == "Operation"
                                      for obj in sketch.InListRecursive):
                    sketch.Visibility = True

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
                self.cleanup_extrudes(doc)
                changed = False
                for component in definitions(doc):
                    for obj in list(component.Group):
                        if (background_result(obj) and obj.Producer is None
                                and not any(consumer != component for consumer in obj.InList)):
                            doc.removeObject(obj.Name)
                            changed = True
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
