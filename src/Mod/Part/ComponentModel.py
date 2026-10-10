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
PART_TYPES = ("Full Component", "Bodies Only", "Excluded", "Reference")


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


def is_file_container(obj):
    """File roots retain native definition storage but are not part models."""
    return is_component(obj) and bool(getattr(obj, "FileContainer", False))


def assembly_context(doc):
    """Return the unique file solver context without creating or solving anything."""
    items = [o for o in doc.Objects if getattr(o, "ComponentRole", "") == "AssemblyContext"]
    if len(items) > 1:
        raise ValueError("A file can own only one assembly relationship context.")
    return items[0] if items else None


def ensure_assembly_context(doc):
    """Create a native joint owner without moving file-owned occurrences."""
    meta = validate(doc)
    root = meta.RootComponent
    if not is_file_container(root):
        raise ValueError("Assembly relationships require a file container.")
    existing = assembly_context(doc)
    if existing:
        return existing
    with transaction(doc, "Create file relationships"):
        context = _create_assembly_context(doc)
    return context


def _create_assembly_context(doc):
    """Join the caller's transaction, including creation of the first joint."""
    context = doc.addObject("Assembly::AssemblyObject", "FileRelationships")
    _property(context, "Link", "ComponentRoot", metadata(doc).RootComponent, True)
    _identity(context, "AssemblyContext")
    context.setEditorMode("Placement", 1)
    context.newObject("Assembly::JointGroup", "FileJoints")
    if App.GuiUp:
        context.ViewObject.ShowInTree = False
    assembly_record(doc)
    return context


def _relationship_members(doc, occurrences):
    root = validate(doc).RootComponent
    if not is_file_container(root) or any(obj not in children(root) for obj in occurrences):
        raise ValueError("Select direct occurrences in the owning file for relationships.")
    if any(obj.LinkedObject is None for obj in occurrences):
        raise ValueError("Repair missing component definitions before creating relationships.")


def _relationship_group(context):
    return next(obj for obj in context.Group if obj.isDerivedFrom("Assembly::JointGroup"))


def _solve_file_relationships(context):
    grounded = {obj: App.Placement(obj.LinkPlacement)
                for obj in children(context.ComponentRoot)
                if "ReadOnly" in obj.getPropertyStatus("LinkPlacement")}
    status = context.solve()
    if status != 0:
        raise ValueError("The assembly relationship could not be solved (status %s)." % status)
    if any(not obj.LinkPlacement.isSame(placement, 1e-7) for obj, placement in grounded.items()):
        raise ValueError("The assembly relationship could not be solved without moving a grounded occurrence.")
    validate(context.Document)
    # Native success alone does not establish that fixed connectors coincide.
    # Verify the accepted fixed-frame contract against the resulting geometry.
    import UtilsAssembly
    for joint in _relationship_group(context).Group:
        if (str(getattr(joint, "JointType", "")) == "Fixed"
                and joint.Detach1 and joint.Detach2 and not getattr(joint, "Suppressed", False)):
            first = UtilsAssembly.getJcsGlobalPlc(joint.Placement1, joint.Reference1)
            second = UtilsAssembly.getJcsGlobalPlc(joint.Placement2, joint.Reference2)
            if not first.isSame(second, 1e-7):
                raise ValueError("The fixed relationship could not be solved: connector frames differ.")


def ground_occurrence(occurrence):
    """Create an explicit native ground in one undo step, without moving geometry."""
    import JointObject
    doc = occurrence.Document
    _relationship_members(doc, [occurrence])
    context = assembly_context(doc)
    if context:
        for joint in _relationship_group(context).Group:
            if getattr(joint, "ObjectToGround", None) == occurrence:
                return joint
    with transaction(doc, "Ground component occurrence"):
        context = context or _create_assembly_context(doc)
        # Native context setup can materialize an existing placement lock as a ground.
        existing = next((obj for obj in _relationship_group(context).Group
                         if getattr(obj, "ObjectToGround", None) == occurrence), None)
        if existing:
            return existing
        joint = _relationship_group(context).newObject("App::FeaturePython", "GroundedJoint")
        JointObject.GroundedJoint(joint, occurrence)
        if App.GuiUp:
            JointObject.ViewProviderGroundedJoint(joint.ViewObject)
        _solve_file_relationships(context)
    return joint


def create_fixed_relationship(first, second, placement1=None, placement2=None):
    """Join local occurrence connector frames using the native Fixed joint engine."""
    import JointObject
    doc = first.Document
    _relationship_members(doc, [first, second])
    if first == second:
        raise ValueError("A relationship must join two different occurrences.")
    frame1, frame2 = App.Placement(placement1 or App.Placement()), App.Placement(placement2 or App.Placement())
    with transaction(doc, "Create fixed component relationship"):
        context = assembly_context(doc) or _create_assembly_context(doc)
        joint = _relationship_group(context).newObject("App::FeaturePython", "FixedJoint")
        JointObject.Joint(joint, JointObject.JointTypes.index("Fixed"))
        if App.GuiUp:
            JointObject.ViewProviderJoint(joint.ViewObject)
        joint.Detach1 = True
        joint.Detach2 = True
        joint.Reference1 = (first, ["", ""])
        joint.Reference2 = (second, ["", ""])
        joint.Placement1, joint.Placement2 = frame1, frame2
        if not context.isPartConnected(first) or not context.isPartConnected(second):
            raise ValueError("Connect the relationship to a grounded occurrence first.")
        _solve_file_relationships(context)
    return joint


def edit_fixed_relationship(joint, placement1, placement2):
    """Edit only detached Fixed connector frames; preserve joint and endpoint identities."""
    doc = joint.Document
    record = assembly_record(doc)
    if (not record or joint.Name not in {item["object"] for item in record["joints"]}
            or str(getattr(joint, "JointType", "")) != "Fixed"
            or not joint.Detach1 or not joint.Detach2):
        raise ValueError("Select a file-owned fixed relationship with explicit connector frames.")
    frame1, frame2 = App.Placement(placement1), App.Placement(placement2)
    with transaction(doc, "Edit fixed component relationship"):
        joint.Placement1, joint.Placement2 = frame1, frame2
        _solve_file_relationships(assembly_context(doc))


def remove_relationships(doc, joints):
    """Delete reviewed native relationships, releasing ground locks in the same undo step."""
    joints = list(dict.fromkeys(joints))
    if not joints:
        return
    record = assembly_record(doc)
    if not record or any(joint.Document != doc or joint.Name not in
                         {item["object"] for item in record["joints"]} for joint in joints):
        raise ValueError("Select relationships from one owning file.")
    with transaction(doc, "Remove component relationships"):
        for joint in joints:
            if hasattr(joint, "ObjectToGround"):
                # Native onBeforeChange releases both Placement and LinkPlacement.
                joint.ObjectToGround = None
            doc.removeObject(joint.Name)
        _solve_file_relationships(assembly_context(doc))


def assembly_record(doc):
    """Validate native joint ownership and return its persistence identity record.

    Endpoints are local occurrences even when their definitions are external.
    Native joint parameters and connectors remain native properties.
    """
    context = assembly_context(doc)
    if context is None:
        return None
    root = metadata(doc).RootComponent
    if (not context.isDerivedFrom("Assembly::AssemblyObject")
            or not getattr(context, "ObjectId", "")
            or not is_file_container(root)
            or getattr(context, "ComponentRoot", None) != root
            or not context.Placement.isIdentity()
            or any(context in getattr(obj, "Group", []) for obj in doc.Objects)):
        raise ValueError("Invalid file assembly context ownership or placement.")
    groups = [o for o in context.Group if o.isDerivedFrom("Assembly::JointGroup")]
    if len(groups) != 1:
        raise ValueError("File relationships require one native joint group.")
    group = groups[0]
    joints = list(group.Group)
    if any(group in getattr(obj, "Group", []) for obj in doc.Objects if obj != context):
        raise ValueError("The file joint group cannot have another owner.")
    if any(o not in [context.Origin, group] + joints for o in context.Group):
        raise ValueError("The file relationship context cannot own geometry.")
    members = set(children(root))
    records = []
    for joint in joints:
        if any(joint in getattr(obj, "Group", []) for obj in doc.Objects
               if obj not in (context, group)):
            raise ValueError("A file relationship cannot have another owner.")
        if hasattr(joint, "ObjectToGround"):
            endpoints = [joint.ObjectToGround]
        elif hasattr(joint, "Reference1") and hasattr(joint, "Reference2"):
            endpoints = [ref[0] if ref else None for ref in (joint.Reference1, joint.Reference2)]
            if endpoints[0] == endpoints[1]:
                raise ValueError("A relationship must join two different occurrences.")
        else:
            raise ValueError("Unsupported file relationship object.")
        if any(obj not in members or obj.Document != doc for obj in endpoints):
            raise ValueError("File relationships must reference direct occurrences in this file.")
        records.append({"object": joint.Name, "endpoints": [obj.Name for obj in endpoints]})
    return {"id": context.ObjectId, "object": context.Name, "root": root.Name,
            "group": group.Name, "joints": sorted(records, key=lambda item: item["object"])}


def _guard_relationship_removal(doc, occurrences):
    record = assembly_record(doc)
    names = {obj.Name for obj in occurrences}
    if record and any(names.intersection(joint["endpoints"]) for joint in record["joints"]):
        raise ValueError("Remove assembly relationships before removing or reparenting these occurrences.")


def ensure_file_container(doc):
    """Undoable migration; preserve the original root and all native links.

    Creation/open callers manage bootstrap undo. Never nest inside a transaction.
    """
    meta = validate(doc, allow_unresolved=True)
    previous = meta.RootComponent
    if is_file_container(previous):
        return previous
    with transaction(doc, "Create file container"):
        return _wrap_file_container(doc)


def _wrap_file_container(doc):
    """Join the caller's structural transaction; never create a second undo step."""
    # Native transactions are lazy: HasPendingTransaction may stay false until
    # the first mutation. Callers establish the transaction before entering here.
    meta = validate(doc, allow_unresolved=True)
    previous = meta.RootComponent
    if is_file_container(previous):
        return previous
    root = _definition(doc)
    _property(root, "Bool", "FileContainer", True, True)
    # The navigator displays doc.Label; native object labels remain unique.
    root.Label = "File"
    root.setEditorMode("Placement", 1)
    occurrence = _add_occurrence(root, previous, placement=App.Placement(previous.Placement))
    occurrence.Representation = "Full Component"
    meta.RootComponent = root
    if App.GuiUp:
        root.Visibility = True
    validate(doc, allow_unresolved=True)
    return root


def definitions(doc):
    items = [o for o in doc.Objects if is_component(o)]
    roots = [getattr(o, "RootComponent", None) for o in doc.Objects
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


def file_imports(doc):
    """Explicit file references, independent of placed component instances."""
    return [obj for obj in doc.Objects if getattr(obj, "ComponentRole", "") == "FileImport"]


def external_documents(doc, allow_unresolved=False):
    """Direct imported files, including references authored by older readers.

    Do not infer imports from unrelated open documents or transitive definitions.
    Existing occurrence-only documents remain readable without a write migration.
    """
    sources = []
    for record in file_imports(doc):
        source = record.Source
        if source is None:
            if allow_unresolved:
                continue
            raise ValueError("Locate the missing imported component file: " + record.Label)
        if not is_component(source) or metadata(source.Document).ObjectId != record.DocumentId:
            raise ValueError("The imported file identity changed; repair is required.")
        sources.append(source.Document)
    sources.extend(link.LinkedObject.Document for component in definitions(doc)
                   for link in children(component)
                   if is_component(link.LinkedObject) and link.LinkedObject.Document != doc)
    return list(dict.fromkeys(sources))


def validate_file_graph(doc, allow_unresolved=False):
    """Reject file cycles even when their component occurrence graph is acyclic."""
    complete = set()
    identities = {}

    def visit(current, ancestors):
        ident = metadata(current).ObjectId
        if ident in identities and identities[ident] != current:
            raise ValueError("Two loaded files claim the same component document identity.")
        identities[ident] = current
        if current in ancestors:
            raise ValueError("Circular component file reference: " + current.Label)
        if current in complete:
            return
        for source in external_documents(current, allow_unresolved):
            visit(source, ancestors | {current})
        complete.add(current)

    visit(doc, set())
    return identities


def _check_file_import(doc, source, allow_unresolved=False):
    metadata(doc)
    metadata(source)
    if source == doc:
        raise ValueError("A file cannot import itself.")
    if any(not item.FileName.lower().endswith(".cadprt") for item in (doc, source)):
        raise ValueError("Save both component files as .cadprt before importing.")
    current_files = validate_file_graph(doc, allow_unresolved)
    incoming_files = validate_file_graph(source)
    if any(ident in current_files and current_files[ident] != incoming
           for ident, incoming in incoming_files.items()):
        raise ValueError("Two loaded files claim the same component document identity.")
    pending = [source]
    seen = set()
    while pending:
        current = pending.pop()
        if current == doc or metadata(current).ObjectId == metadata(doc).ObjectId:
            raise ValueError("Import would introduce a circular component file reference.")
        if current not in seen:
            seen.add(current)
            pending.extend(external_documents(current))


def _import_file(doc, source):
    """Register a preflighted import inside the caller's native transaction."""
    for record in file_imports(doc):
        if record.DocumentId == metadata(source).ObjectId:
            if record.Source is None or record.Source.Document != source:
                raise ValueError("The imported file identity is already assigned to another file.")
            return record
    record = doc.addObject("App::FeaturePython", "ComponentFileImport")
    _identity(record, "FileImport")
    _property(record, "XLink", "Source", metadata(source).RootComponent, True)
    _property(record, "String", "DocumentId", metadata(source).ObjectId, True)
    record.Label = Path(source.FileName).stem
    if App.GuiUp:
        record.ViewObject.Visibility = False
        record.ViewObject.ShowInTree = False
    return record


def import_file(doc, source):
    """Import every definition in a file without placing any of them."""
    _check_file_import(doc, source)
    for record in file_imports(doc):
        if record.Source is not None and record.Source.Document == source:
            return record
    with transaction(doc, "Import component file"):
        record = _import_file(doc, source)
    return record


def available_definitions(doc):
    """Domestic definitions followed by all definitions in direct imported files."""
    return definitions(doc) + [component for source in external_documents(doc, True)
                               for component in definitions(source)]

def _restore_file_imports(doc, source):
    for record in file_imports(doc):
        if record.DocumentId == metadata(source).ObjectId:
            record.Source = metadata(source).RootComponent


def repair_file_import(record, filename):
    """Restore an unused file import by its saved file identity, never its name."""
    import CadDocument
    source = CadDocument.open(filename)
    if metadata(source).ObjectId != record.DocumentId:
        raise ValueError("That file does not have the saved imported file identity.")
    doc = record.Document
    _check_file_import(doc, source, allow_unresolved=True)
    # Placed components also need their original object/reference bindings restored.
    matches = {component.ObjectId: component for component in definitions(source)}
    unresolved = [link for component in definitions(doc) for link in children(component)
                  if link.LinkedObject is None and getattr(link, "DefinitionId", "") in matches]
    representatives = {link.DefinitionId: link for link in unresolved}
    plans = [_component_repair_plan(owner(link), link, source)
             for link in representatives.values()]
    with transaction(doc, "Locate imported component file"):
        _apply_component_repairs(doc, source, plans)
    return source


def component_label(component, context_document):
    if component.Document == context_document:
        return component.Label
    filename = Path(component.Document.FileName).stem or component.Document.Label
    # Same filename in different directories must not produce indistinguishable picks.
    matches = [doc for doc in App.listDocuments().values()
               if doc.FileName and Path(doc.FileName).stem.casefold() == filename.casefold()]
    if len(matches) > 1:
        filename = str(Path(component.Document.FileName))
    return component.Label + " (" + filename + ")"


def definition_label(doc, label, exclude=None):
    label = label.strip()
    if not label:
        raise ValueError("Enter a component name.")
    if any(obj != exclude and not is_file_container(obj)
           and obj.Label.casefold() == label.casefold() for obj in definitions(doc)):
        raise ValueError("A domestic component already has this name. Choose a unique name.")
    return label


def next_part_label(doc):
    """Reserve visible part names throughout this component document."""
    labels = {obj.Label.casefold() for obj in definitions(doc) if not is_file_container(obj)}
    number = 1
    while f"Part{number:03d}".casefold() in labels:
        number += 1
    return f"Part{number:03d}"


def _definition(doc, label=None):
    label = definition_label(doc, label or next_part_label(doc))
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


def new_file_document(label=None):
    """User-facing New File; internal copy/conversion initializers stay separate."""
    doc = new_document()
    try:
        if label is not None:
            doc.Label = label
        ensure_file_container(doc)
        # Bootstrap is not an editing action: Undo must never unpin the file root.
        doc.clearUndos()
        return doc
    except Exception:
        App.closeDocument(doc.Name)
        raise


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


def definition_deletion_plan(component):
    """Review owned objects only; linked definitions and external consumers survive."""
    if not is_component(component):
        raise ValueError("Select a component definition.")
    doc = component.Document
    if is_file_container(component) or metadata(doc).RootComponent == component:
        raise ValueError("The file root cannot be deleted.")
    owned = set()
    def collect(obj):
        if obj in owned:
            return
        if obj.Document != doc:
            raise ValueError("Component ownership crosses a file boundary.")
        if obj != component and is_component(obj):
            raise ValueError("Separate nested definitions before deleting this component.")
        owned.add(obj)
        # Follow native ownership, never Link targets or feature dependencies.
        if getattr(obj, "ComponentRole", "") == "Occurrence" or obj.isDerivedFrom("App::Link"):
            return
        for child in getattr(obj, "Group", []):
            collect(child)
        origin = getattr(obj, "Origin", None)
        if origin is not None:
            collect(origin)
        if obj.isDerivedFrom("App::Origin"):
            for feature in obj.OriginFeatures:
                collect(feature)
    collect(component)
    consumers = {consumer for obj in owned for consumer in obj.InList if consumer not in owned}
    if consumers:
        labels = ", ".join(sorted({obj.Document.Label + ": " + obj.Label for obj in consumers}))
        raise ValueError("Remove component occurrences and outside references before deleting: " + labels)
    return [obj for obj in doc.Objects if obj in owned]


def delete_definition(component):
    """Delete an unused, unreferenced definition and its owned payload atomically."""
    doc = component.Document
    objects = definition_deletion_plan(component)
    names = [obj.Name for obj in objects]
    with transaction(doc, "Delete component definition"):
        # Delete the container first so native group cleanup cannot strand children.
        doc.removeObject(component.Name)
        for name in reversed(names):
            if doc.getObject(name) is not None:
                doc.removeObject(name)
        validate(doc, allow_unresolved=True)


def remove_instances(occurrences):
    """Remove only owning links; retain models, geometry and reference identities."""
    occurrences = list(dict.fromkeys(occurrences))
    if not occurrences:
        return
    doc = occurrences[0].Document
    if any(obj.Document != doc or getattr(obj, "ComponentRole", "") != "Occurrence"
           or not is_component(owner(obj)) for obj in occurrences):
        raise ValueError("Select linked instances from one owning file.")
    _guard_relationship_removal(doc, occurrences)
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
        _guard_relationship_removal(doc, reparented)
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
    if is_file_container(definition):
        raise ValueError("Select component models; a file cannot be an occurrence.")
    if not is_component(parent) or (definition is not None and not is_component(definition)):
        raise ValueError("Both parent and source must be component definitions.")
    if definition is not None and _reachable(definition, parent):
        raise ValueError("A component cannot contain itself, directly or indirectly.")
    if definition is not None and definition.Document != parent.Document and not definition.Document.FileName.lower().endswith(".cadprt"):
        raise ValueError("Save an external component as .cadprt before adding it.")
    if definition is not None and definition.Document != parent.Document and not parent.Document.FileName.lower().endswith(".cadprt"):
        raise ValueError("Save the parent as .cadprt before adding an external component.")
    if definition is not None and definition.Document != parent.Document:
        _check_file_import(parent.Document, definition.Document)
    with transaction(parent.Document, "Add Component"):
        if definition is not None and definition.Document != parent.Document:
            _import_file(parent.Document, definition.Document)
        if definition is None:
            definition = _definition(parent.Document, label)
        link = _add_occurrence(parent, definition, label, placement)
    return link


def _add_occurrence(parent, definition, label=None, placement=None):
    """Create a native occurrence inside the caller's transaction."""
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
    if is_file_container(component):
        raise ValueError("Edit a component before creating modeling geometry.")
    if not is_component(component) or component.Document != obj.Document:
        raise ValueError("An object and its component must belong to the same file.")
    if owner(obj) not in (None, component):
        raise ValueError("An object cannot belong to two components.")
    automatic = not hasattr(obj, "ObjectId") and obj.Label == obj.Name
    if not hasattr(obj, "ObjectId"):
        _identity(obj, role)
    elif obj.ComponentRole != role:
        raise ValueError("The object's existing role cannot be changed implicitly.")
    if owner(obj) != component:
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
    predecessors = {obj: {display_object(dep) for dep in geometry_dependencies(obj, include_frames=True)} & set(visible)
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


def geometry_dependencies(obj, include_frames=False):
    """Follow geometry inputs without treating component ownership as an input.

    A reference's SourceOccurrence establishes placement/context. Traversing its
    whole definition would incorrectly depend on every unrelated history branch.
    SourceObject supplies the actual geometry dependency instead.
    """
    def inputs(item):
        refs = [source for source, names in getattr(item, "FrameSupport", ()) if source] if include_frames else []
        return list(item.OutList) + refs
    found, pending = set(), inputs(obj)
    while pending:
        dep = pending.pop()
        if dep == obj or dep in found:
            continue
        if getattr(dep, "ComponentRole", "") in ("Definition", "Occurrence", "Document"):
            continue
        found.add(dep)
        pending.extend(inputs(dep))
    return list(found)


def require_geometry_access(obj, subname="", component=None, aggregate=True):
    """Guard native occurrence paths before a consumer reads their geometry.

    Explicit reference features are owned inputs; their source links are not
    recursively treated as direct use. A bare foreign definition member has lost
    its occurrence path, so a component consumer must first create an owned
    reference instead of guessing a placement or a permitted instance.
    """
    if obj is None:
        raise ValueError("Select an input object.")
    path = list(obj.getSubObjectList(subname)) if subname else [obj]
    if not path:
        raise ValueError("The selected geometry path is unavailable.")
    for item in path:
        if getattr(item, "ComponentRole", "") == "Occurrence":
            parent = owner(item)
            if part_type(parent, item) in ("Reference", "Excluded"):
                raise ValueError("Add Reference Feature before using Reference component geometry; "
                                 "Excluded components cannot supply direct geometry.")
    target = path[-1]
    if component is not None and is_component(component):
        target_owner = owner(target)
        if (is_component(target_owner) and target_owner != component
                and getattr(target, "ComponentRole", "") != "Occurrence"):
            raise ValueError("Add Reference Feature to the active component before using child geometry.")
    # A whole container/link shape also contains its descendants. Do not return
    # an unfiltered native aggregate with Reference or Excluded geometry inside.
    definition = target.LinkedObject if getattr(target, "ComponentRole", "") == "Occurrence" else target
    seen = set()
    def check_children(parent):
        if not is_component(parent) or parent in seen:
            return
        seen.add(parent)
        for child in children(parent):
            if part_type(parent, child) in ("Reference", "Excluded"):
                raise ValueError("The component contains Reference or Excluded geometry. "
                                 "Use an owned result instead of its whole native shape.")
            check_children(child.LinkedObject)
    if aggregate:
        check_children(definition)


def require_geometry_inputs(obj):
    """Reject unpromoted native dependency chains at the evaluated-result boundary.

    An owned Reference is the explicit source boundary. Do not follow its source
    links as if they were raw modeling inputs. Ordinary legacy objects outside
    component ownership retain their existing native dependency behavior.
    """
    component = owner(obj)
    if not is_component(component):
        return
    seen = set()
    def visit(item):
        if item in seen:
            return
        seen.add(item)
        if getattr(item, "ComponentRole", "") == "Reference" and owner(item) == component:
            return
        for source in item.OutList:
            if getattr(source, "ComponentRole", "") == "Document":
                continue
            require_geometry_access(source, component=component)
            visit(source)
    visit(obj)


def current_shape(obj):
    """Never certify stale native caches as evaluated component results."""
    require_geometry_access(obj)
    require_geometry_inputs(obj)
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
        try:
            require_geometry_inputs(source)
        except ValueError:
            return  # The result was cleared above; never publish a forbidden cache.
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
    require_geometry_inputs(operation)
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
    if is_file_container(component):
        # The file has no History of its own, but its displayed assembly must
        # refresh child reference snapshots before their domestic consumers.
        # Each shared definition is refreshed once; external files own their edits.
        seen, issues = set(), []
        def refresh(definition):
            if definition in seen or definition.Document != doc:
                return
            seen.add(definition)
            for link in children(definition):
                if is_component(link.LinkedObject):
                    refresh(link.LinkedObject)
            if definition != component:
                issues.extend(activate(definition, strict=False))
        refresh(component)
        doc.recompute()
        if strict and issues:
            raise ValueError("\n".join(obj.Label + ": " + message for obj, message in issues))
        return issues
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


def part_type(parent, child):
    """Authored type of a direct occurrence, owned by its parent definition.

    The optional native property is additive. Older files retain their original
    display registries; only a direct legacy rule supplies the initial value.
    Nested legacy path overrides are not silently migrated into shared children.
    """
    if not is_component(parent) or child not in children(parent):
        raise ValueError("Select a direct child of the owning component.")
    if "PartType" in child.PropertiesList:
        value = child.PartType
    else:
        value = json.loads(parent.RepresentationOverrides).get(
            child.ObjectId, str(child.Representation))
        value = "Excluded" if value == "Hidden" else value
    if value not in PART_TYPES:
        raise ValueError("Unsupported component part type.")
    return value


def set_part_types(parent, updates):
    """Save direct-child types atomically without changing visibility or sources.

    None resets to Bodies Only. Types belong to occurrence objects owned by the
    parent, so all uses of that parent share them, while other parents do not.
    This backend does not enable the pending Part Tree UI integration.
    """
    updates = list(updates)
    for child, value in updates:
        part_type(parent, child)
        if value is not None and value not in PART_TYPES:
            raise ValueError("Unsupported component part type.")
    if not updates:
        return
    with transaction(parent.Document, "Component part types"):
        for child, value in updates:
            if "PartType" not in child.PropertiesList:
                _property(child, "String", "PartType", "Bodies Only", True)
                child.setEditorMode("PartType", 2)
            child.PartType = value or "Bodies Only"


def effective_part_type(root, ids, active_ids=()):
    """Resolve editing display policy without mutating authored child types.

    An active component is Full Component even if an ancestor excludes it.
    Reference is visible only under its directly active owner; elsewhere it is
    Excluded. An excluded branch cannot be revealed by native visibility.
    """
    ids, active_ids = tuple(ids), tuple(active_ids)
    chain = _path(root, ids)
    _path(root, active_ids)
    if ids == active_ids or not ids:
        return "Full Component"
    start = len(active_ids) if ids[:len(active_ids)] == active_ids else 0
    value = "Full Component"
    for depth in range(start, len(chain)):
        parent = root if depth == 0 else chain[depth - 1].LinkedObject
        value = part_type(parent, chain[depth])
        if value == "Reference" and ids[:depth] != active_ids:
            value = "Excluded"
        if value == "Excluded":
            return value
    return value


def part_type_allows_geometry(root, ids):
    """Policy gate for unpromoted occurrence geometry, independent of editing.

    An explicit reference feature is a separate owned object and is not tested
    through its source occurrence here. Consumers must integrate this gate before
    the new types are exposed by the UI.
    """
    chain = _path(root, ids)
    return all(part_type(root if depth == 0 else chain[depth - 1].LinkedObject, link)
               not in ("Reference", "Excluded") for depth, link in enumerate(chain))


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


def copy_definition(source, destination, label=None):
    """Independent domestic hierarchy copy; existing external children stay shared.

    Native copyObject remaps native properties. Semantic IDs are regenerated and
    their string registries remapped explicitly. No existing placement is changed.
    """
    metadata(destination)
    label = definition_label(destination, label or source.Label + " copy")
    closure = []
    def collect(component):
        if component in closure:
            return
        closure.append(component)
        for link in children(component):
            if not is_component(link.LinkedObject):
                raise ValueError("Repair missing components before copying.")
            if link.LinkedObject.Document == source.Document:
                collect(link.LinkedObject)
    collect(source)
    originals = []
    def owned(obj):
        if obj in originals:
            return
        originals.append(obj)
        if getattr(obj, "ComponentRole", "") == "Occurrence":
            return
        for member in getattr(obj, "Group", []):
            owned(member)
        origin = getattr(obj, "Origin", None)
        if origin:
            owned(origin)
            for feature in origin.OriginFeatures:
                owned(feature)
    for component in closure:
        owned(component)
    if any(obj.ExpressionEngine for obj in originals):
        raise ValueError("Expression-driven copies require reviewed expression remapping.")
    external_children = {link.LinkedObject for component in closure for link in children(component)
                         if link.LinkedObject not in closure}
    if any(dep not in originals and dep not in external_children
           for obj in originals for dep in obj.OutList):
        raise ValueError("This component has inputs outside its owned hierarchy. Copy or repair those dependencies first.")
    for child in external_children:
        if child.Document != destination:
            _check_file_import(destination, child.Document)
    with transaction(destination, "Copy domestic component"):
        copied = destination.copyObject(originals, False)
        mapping = dict(zip(originals, copied))
        ids = {}
        for old, new in mapping.items():
            if hasattr(old, "ObjectId"):
                new.ObjectId = str(uuid.uuid4())
                ids[old.ObjectId] = new.ObjectId
        for old, new in mapping.items():
            if is_component(old):
                # Child names are unique in the destination; the requested top name
                # is reserved before assigning generated names to copied children.
                new.Label = label if old == source else (old.Label if not any(
                    other != new and other.Label.casefold() == old.Label.casefold()
                    for other in definitions(destination)) else next_part_label(destination))
                new.ModelHistory = [mapping[old.Document.getObject(name)].Name for name in old.ModelHistory]
                new.ResultObjects = [mapping[old.Document.getObject(name)].Name for name in old.ResultObjects]
                new.RepresentationOverrides = json.dumps({
                    "/".join(ids.get(part, part) for part in key.split("/")): value
                    for key, value in json.loads(old.RepresentationOverrides).items()})
            if getattr(old, "ComponentRole", "") == "Occurrence":
                target = mapping.get(old.LinkedObject, old.LinkedObject)
                new.setLink(target)
                new.DefinitionId = target.ObjectId
            if getattr(old, "ComponentRole", "") == "Reference" and new.SourceObject:
                new.SourceObjectId = new.SourceObject.ObjectId
            if hasattr(old, "PreviousVisibility"):
                new.PreviousVisibility = json.dumps({ids.get(key, key): value
                    for key, value in json.loads(old.PreviousVisibility).items()})
        for child in external_children:
            if child.Document != destination:
                _import_file(destination, child.Document)
        for component in reversed(closure):
            activate(mapping[component], strict=False)
        validate(destination)
    return mapping[source]


def replace_instances(source, replacement, occurrences):
    """Replace reviewed owning placements, preserving transforms and link identities.

    Consumer/path remapping needs a relationship editor; refuse before mutation
    rather than silently changing the meaning of a subelement reference.
    """
    doc = replacement.Document
    occurrences = list(dict.fromkeys(occurrences))
    for link in occurrences:
        if (link.Document != doc or link.LinkedObject != source or not is_component(owner(link))):
            raise ValueError("Choose placements in the domestic file using the original definition.")
        if _reachable(replacement, owner(link)):
            raise ValueError("Replacement would introduce circular component nesting.")
        if (link.ExpressionEngine or link.ElementCount or link.Scale != 1
                or tuple(link.ScaleVector) != (1, 1, 1)
                or any(consumer != owner(link) for consumer in link.InList)):
            raise ValueError("This placement has driven geometry or downstream references requiring explicit repair.")
        if any(link.ObjectId in key.split("/") for component in definitions(doc)
               for key in json.loads(component.RepresentationOverrides)):
            raise ValueError("Reset placement display overrides before replacing this component.")
    if not occurrences:
        return
    with transaction(doc, "Replace with domestic component"):
        for link in occurrences:
            placement = App.Placement(link.LinkPlacement)
            link.setLink(replacement)
            link.DefinitionId = replacement.ObjectId
            link.LinkPlacement = placement
            peers = [other.InstanceNumber for other in children(owner(link))
                     if other != link and other.LinkedObject == replacement]
            link.InstanceNumber = max(peers or [0]) + 1
        validate(doc)


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
        definition.Label = definition_label(parent.Document, label or source.Label + " copy", definition)
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


RETAINED_OPERATION_FAMILIES = ("DressUp", "Transform", "Boolean", "Helix", "Primitive",
                              "Pipe", "Loft", "Revolve", "Extrude", "Sketch", "Datum")


def retained_operation_source(obj):
    """Resolve native History access by explicit saved family/source identity."""
    for family in RETAINED_OPERATION_FAMILIES:
        if getattr(obj, "Legacy" + family + "State", ""):
            return getattr(obj, "Legacy" + family + "Source", obj)
    return obj


def history_detail(obj):
    for family in ("DressUp", "Transform", "Boolean"):
        if getattr(obj, "Legacy" + family + "State", ""):
            if retained_operation_source(obj) is None:
                return "Retained native operation is missing. Repair its source before editing."
            return "Retained native " + family + ". Edit the original topology references, ordered inputs and parameters without replacing their identities."
    if getattr(obj, "LegacyHelixState", ""):
        if getattr(obj, "LegacyHelixSource", obj) is None:
            return "Retained native helix is missing. Repair its source before editing."
        return "Retained native helix. Edit the original profile, axis, parameter laws and target without replacing their identities."
    if getattr(obj, "LegacyPrimitiveState", ""):
        if getattr(obj, "LegacyPrimitiveSource", obj) is None:
            return "Retained native primitive is missing. Repair its source before editing."
        return "Retained native primitive. Edit the original shape dimensions, attachment and target without replacing their identities."
    if getattr(obj, "LegacyPipeState", ""):
        if getattr(obj, "LegacyPipeSource", obj) is None:
            return "Retained native pipe is missing. Repair its source before editing."
        return "Retained native pipe. Edit the original profiles, paths, orientation and target without replacing their identities."
    if getattr(obj, "LegacyLoftState", ""):
        if getattr(obj, "LegacyLoftSource", obj) is None:
            return "Retained native loft is missing. Repair its source before editing."
        return "Retained native loft. Edit the original ordered sections, references and target without replacing their identities."
    if getattr(obj, "LegacyRevolveState", ""):
        if getattr(obj, "LegacyRevolveSource", obj) is None:
            return "Retained native revolution is missing. Repair its source before editing."
        return "Retained native revolution. Edit the original axis, angles, source and target without replacing their references."
    if getattr(obj, "LegacyExtrudeState", ""):
        if getattr(obj, "LegacyExtrudeSource", obj) is None:
            return "Retained native extrusion is missing. Repair its source before editing."
        return "Retained native extrusion. Edit the original extent, profile and target without replacing their references."
    if getattr(obj, "LegacySketchState", "") == "Linked native sketch":
        if getattr(obj, "LegacySketchSource", None) is None:
            return "Retained native sketch is missing. Repair its source before editing or using it."
        return "Linked native sketch. Edit the original constraints, expressions and attachments shared by its consumers."
    if getattr(obj, "LegacyDatumState", "") == "Linked native attachment":
        if getattr(obj, "LegacyDatumSource", None) is None:
            return "Retained native datum is missing. Repair its source before using this frame."
        return "Linked native datum. Edit its original attachment without replacing support references."
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
    for family in ("DressUp", "Transform", "Boolean"):
        if getattr(obj, "Legacy" + family + "State", "") and "Legacy" + family + "Source" in obj.PropertiesList:
            source = retained_operation_source(obj)
            if source is None or obj.LinkedObject != source or "Invalid" in source.State:
                return "Needs repair"
    if (getattr(obj, "LegacyHelixState", "")
            and "LegacyHelixSource" in obj.PropertiesList
            and (getattr(obj, "LegacyHelixSource", None) is None
                 or obj.LinkedObject != obj.LegacyHelixSource
                 or "Invalid" in obj.LegacyHelixSource.State)):
        return "Needs repair"
    if (getattr(obj, "LegacyPrimitiveState", "")
            and "LegacyPrimitiveSource" in obj.PropertiesList
            and (getattr(obj, "LegacyPrimitiveSource", None) is None
                 or obj.LinkedObject != obj.LegacyPrimitiveSource
                 or "Invalid" in obj.LegacyPrimitiveSource.State)):
        return "Needs repair"
    if (getattr(obj, "LegacyPipeState", "")
            and "LegacyPipeSource" in obj.PropertiesList
            and (getattr(obj, "LegacyPipeSource", None) is None
                 or obj.LinkedObject != obj.LegacyPipeSource
                 or "Invalid" in obj.LegacyPipeSource.State)):
        return "Needs repair"
    if (getattr(obj, "LegacyLoftState", "")
            and "LegacyLoftSource" in obj.PropertiesList
            and (getattr(obj, "LegacyLoftSource", None) is None
                 or obj.LinkedObject != obj.LegacyLoftSource
                 or "Invalid" in obj.LegacyLoftSource.State)):
        return "Needs repair"
    if (getattr(obj, "LegacyRevolveState", "")
            and "LegacyRevolveSource" in obj.PropertiesList
            and (getattr(obj, "LegacyRevolveSource", None) is None
                 or obj.LinkedObject != obj.LegacyRevolveSource
                 or "Invalid" in obj.LegacyRevolveSource.State)):
        return "Needs repair"
    if (getattr(obj, "LegacyExtrudeState", "")
            and "LegacyExtrudeSource" in obj.PropertiesList
            and (getattr(obj, "LegacyExtrudeSource", None) is None
                 or obj.LinkedObject != obj.LegacyExtrudeSource
                 or "Invalid" in obj.LegacyExtrudeSource.State)):
        return "Needs repair"
    if (getattr(obj, "LegacySketchState", "") == "Linked native sketch"
            and (getattr(obj, "LegacySketchSource", None) is None
                 or obj.LinkedObject != obj.LegacySketchSource
                 or "Invalid" in obj.LegacySketchSource.State)):
        return "Needs repair"
    if (getattr(obj, "LegacyDatumState", "") == "Linked native attachment"
            and (getattr(obj, "LegacyDatumSource", None) is None
                 or obj.LinkedObject != obj.LegacyDatumSource
                 or "Invalid" in obj.LegacyDatumSource.State)):
        return "Needs repair"
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


def output_shapes(component):
    """Return placed finished geometry, independent of display visibility.

    Native sub-object resolution retains occurrence transforms/scales. Traverse
    owned results rather than native container compounds so construction geometry
    and Reference/Excluded branches cannot leak into exchange output.
    """
    root = component
    if getattr(root, "ComponentRole", "") == "Occurrence":
        require_geometry_access(root, aggregate=False)
        component = root.LinkedObject
    if not is_component(component):
        raise ValueError("Select a component definition or occurrence.")
    paths = []
    def collect(parent, prefix, ancestors):
        if parent in ancestors:
            raise ValueError("Cyclic component output.")
        items = history(parent)
        consumed = _consumed_results(items, {obj: bool(suppression_sources(obj)) for obj in items})
        for name in parent.ResultObjects:
            result = parent.Document.getObject(name)
            if result is None:
                raise ValueError("A component output is missing; repair it before exporting.")
            if result in consumed or suppression_sources(result):
                continue
            current_shape(result)
            paths.append(prefix + result.Name + ".")
        for child in children(parent):
            if part_type(parent, child) in ("Reference", "Excluded"):
                continue
            if not is_component(child.LinkedObject):
                raise ValueError("Repair missing component output before exporting.")
            collect(child.LinkedObject, prefix + child.Name + ".", ancestors | {parent})
    collect(component, "", set())
    from BasicShapes.ShapeReferences import linked_shape
    return [linked_shape((root, [path])) for path in paths]


@contextmanager
def export_objects(objects):
    """Provide native writers with disposable evaluated component output objects.

    Source documents, visibility and identities are never changed. Ordinary
    objects are passed through. The caller must keep this context alive for the
    entire synchronous native writer call.
    """
    objects = list(objects)
    prepared = []
    seen = set()
    for obj in objects:
        if isinstance(obj, tuple):
            if len(obj) == 2 and getattr(obj[0], "ComponentRole", ""):
                raise ValueError("Export component results without explicit face-color tuples.")
            prepared.append((obj, None))
            continue
        if obj in seen:
            continue
        seen.add(obj)
        role = getattr(obj, "ComponentRole", "")
        if role == "Definition":
            shapes = output_shapes(obj)
        elif role == "Occurrence":
            shapes = output_shapes(obj)
        elif is_component(owner(obj)) and hasattr(obj, "Shape"):
            current_shape(obj)
            from BasicShapes.ShapeReferences import linked_shape
            shapes = [linked_shape((obj, []))]
        else:
            prepared.append((obj, None))
            continue
        if not shapes:
            raise ValueError("The selected component has no exportable finished geometry.")
        prepared.append((obj, shapes))
    scratch = None
    previous = App.ActiveDocument
    try:
        output = []
        for source, shapes in prepared:
            if shapes is None:
                output.append(source)
                continue
            if scratch is None:
                scratch = App.newDocument("ComponentExchange", hidden=True, temp=True)
            for index, shape in enumerate(shapes):
                result = scratch.addObject("Part::Feature", "ComponentOutput")
                result.Label = source.Label if len(shapes) == 1 else source.Label + " " + str(index + 1)
                result.Shape = shape
                output.append(result)
        if scratch is not None:
            scratch.recompute()
        yield output
    finally:
        if scratch is not None:
            App.closeDocument(scratch.Name)
        if previous is not None and previous.Name in App.listDocuments():
            App.setActiveDocument(previous.Name)


def copy_to_external_file(definition, filename):
    """Write a new independent file, leaving original definitions and uses intact."""
    destination = Path(filename).resolve()
    if destination.suffix.lower() != ".cadprt" or destination.exists():
        raise ValueError("Choose a new .cadprt file for the independent copy.")
    if definition.Document.HasPendingTransaction:
        raise ValueError("Finish the active edit before copying a component.")
    external = new_document("Copy destination " + str(uuid.uuid4()))
    try:
        # Cross-file native links require the destination to have a filename.
        external.saveAs(str(destination))
        empty = metadata(external).RootComponent
        copied = copy_definition(definition, external, definition.Label)
        metadata(external).RootComponent = copied
        external.removeObject(empty.Name)
        if App.GuiUp:
            copied.Visibility = True
        external.recompute()
        ensure_file_container(external)
        external.clearUndos()
        validate(external)
        external.save()
        return copied
    except Exception:
        App.closeDocument(external.Name)
        # This destination was verified absent before this operation; never remove
        # an existing user file. Failed creation must not leave an empty component.
        if destination.is_file():
            destination.unlink()
        raise


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
            part_type(component, child)
            if is_file_container(child.LinkedObject):
                raise ValueError("A file container cannot be a component occurrence.")
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
        ensure_file_container(external)
        external.clearUndos()
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
    validate_file_graph(doc, allow_unresolved)
    meta = metadata(doc)
    if meta.SchemaVersion != SCHEMA or not is_component(meta.RootComponent):
        raise ValueError("Unsupported component schema or missing root component.")
    containers = [o for o in doc.Objects if getattr(o, "FileContainer", False)]
    if containers and containers != [meta.RootComponent]:
        raise ValueError("The file container must be the unique document root.")
    if containers:
        root = containers[0]
        if (root.ModelHistory or root.ResultObjects
                or not root.Placement.isIdentity()
                or any(obj != root.Origin and getattr(obj, "ComponentRole", "") != "Occurrence"
                       for obj in root.Group)):
            raise ValueError("The file container owns only its global origin and occurrences.")
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
            part_type(component, child)
            if is_file_container(child.LinkedObject):
                raise ValueError("A file container cannot be a component occurrence.")
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
    assembly_record(doc)
    return meta


def _component_repair_plan(parent, occurrence, source):
    """Validate recovery without changing native links or reference bindings."""
    if occurrence not in children(parent):
        raise ValueError("Select a direct component instance to repair.")
    matches = [d for d in definitions(source) if d.ObjectId == occurrence.DefinitionId]
    if len(matches) != 1:
        raise ValueError("That file does not contain the saved component definition identity.")
    definition = matches[0]
    doc = parent.Document
    targets = [link for component in definitions(doc) for link in children(component)
               if link == occurrence or (link.LinkedObject is None
                   and getattr(link, "DefinitionId", "") == occurrence.DefinitionId)]
    if definition.Document != doc:
        _check_file_import(doc, definition.Document, allow_unresolved=True)
    if any(_reachable(definition, owner(link)) for link in targets):
        raise ValueError("Repair would introduce a component cycle.")
    sources = {}
    for obj in definition.Group:
        ident = getattr(obj, "ObjectId", "")
        if ident:
            sources.setdefault(ident, []).append(obj)
    return definition, targets, sources


def _apply_component_repairs(doc, source, plans):
    """Apply preflighted bindings inside the caller's single transaction."""
    _restore_file_imports(doc, source)
    affected = []
    for definition, targets, sources in plans:
        for link in targets:
            placement = App.Placement(link.LinkPlacement)
            link.setLink(definition)
            link.LinkPlacement = placement
        for component in dict.fromkeys(owner(link) for link in targets):
            if component not in affected:
                affected.append(component)
            for obj in history(component):
                if getattr(obj, "ComponentRole", "") != "Reference" or obj.SourceOccurrence not in targets:
                    continue
                candidates = sources.get(obj.SourceObjectId, [])
                # Missing/ambiguous geometry stays repairable without rebinding by label.
                obj.SourceObject = candidates[0] if len(candidates) == 1 else None
    # All definitions must be rebound before dependent geometry is refreshed.
    for component in affected:
        activate(component, strict=False)


def repair_component(parent, occurrence, filename):
    """Locate a saved definition and restore its unresolved instances in this file."""
    if occurrence not in children(parent):
        raise ValueError("Select a direct component instance to repair.")
    import CadDocument
    source = CadDocument.open(filename)
    plan = _component_repair_plan(parent, occurrence, source)
    with transaction(parent.Document, "Locate Component File"):
        _apply_component_repairs(parent.Document, source, [plan])
    return plan[0]


class ComponentObserver:
    """Adopt completed native commands inside their existing undo transaction."""
    def __init__(self):
        self.busy = False
        self.visibility = {}
        self.deleted_extrudes = {}

    def slotBeforeRecomputeDocument(self, doc):
        if any(hasattr(obj, "FrameSupport") for obj in doc.Objects):
            import ComponentSketch
            ComponentSketch.sync_supports(doc)

    def slotRecomputedObject(self, obj):
        if any(hasattr(item, "FrameSupport") for item in obj.Document.Objects):
            import ComponentSketch
            ComponentSketch.sync_supports(obj.Document, obj)

    def slotRecomputedDocument(self, doc):
        if any(hasattr(obj, "FrameSupport") for obj in doc.Objects):
            import ComponentSketch
            ComponentSketch.sync_supports(doc)

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
        if not obj.Document.HasPendingTransaction:
            return
        if getattr(obj, "ProjectedFrame", None):
            self.deleted_extrudes.setdefault(obj.Document.Name, []).append((
                [dep.Name for dep in geometry_dependencies(obj)
                 if getattr(dep, "ComponentRole", "") == "Internal"], []))
            return
        if getattr(obj, "OperationKind", "") != "Extrude":
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
