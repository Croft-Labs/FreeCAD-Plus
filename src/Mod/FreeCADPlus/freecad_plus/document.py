# SPDX-License-Identifier: LGPL-2.1-or-later
"""Versioned native document, definition catalog, and shared component hierarchies.

Legacy conversion is explicitly handled by conversion.py, never by ordinary open.
Native object names qualified by Document.Uid supply persistent identity.
"""
from contextlib import contextmanager
from pathlib import Path

import FreeCAD as App

FORMAT = "FreeCADPlus.ComponentDocument"
SCHEMA = 5
SUPPORTED_SCHEMAS = (1, 2, 3, 4, 5)


@contextmanager
def visibility_transaction(doc, label):
    """An eye click joins a live editor without committing its transaction."""
    if doc.HasPendingTransaction or App.getActiveTransaction():
        yield
    else:
        with transaction(doc, label):
            yield


@contextmanager
def transaction(doc, label):
    """Do not consume or commit a caller's pending transaction."""
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current operation first")
    doc.openTransaction(label)
    try:
        yield
        validate(doc)
        doc.recompute()
        validate(doc)
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise
    else:
        doc.commitTransaction()


def validate(doc):
    """Validate the complete imported-file DAG and each file's owned graph."""
    from .external import validate_graph
    return validate_graph(doc)


def owned_children(obj):
    """Native ownership only, never general feature dependencies or linked definitions."""
    if obj.TypeId in ("App::Part", "PartDesign::Body"):
        return [obj.Origin, *obj.Group]
    if obj.TypeId == "App::Origin":
        return list(obj.OriginFeatures)
    if obj.TypeId == "PartDesign::Boolean":
        # Boolean is a native GeoFeatureGroup: its tools move into its ownership.
        return list(obj.Group)
    return []


def owned_path(owner, target, ancestors=()):
    if owner == target:
        return ()
    if owner in ancestors:
        raise ValueError("Cyclic component ownership")
    for child in owned_children(owner):
        found = owned_path(child, target, (*ancestors, owner))
        if found is not None:
            return (child, *found)
    return None


def _validate_local(doc, external_definitions=()):
    """Check ownership separately from imported definition availability."""
    if doc.Partial:
        raise ValueError("A partially loaded component document cannot be edited or saved")
    roots = [o for o in doc.Objects if "PlusFormat" in o.PropertiesList]
    if len(roots) != 1:
        raise ValueError("Expected exactly one component file root")
    root = roots[0]
    if (root.TypeId != "App::Part" or root.PlusFormat != FORMAT
            or getattr(root, "PlusSchema", None) not in SUPPORTED_SCHEMAS):
        raise ValueError("Unsupported component document format or schema")
    if not root.Placement.isSame(App.Placement(), 1e-9):
        raise ValueError("The file coordinate frame must remain fixed")
    definitions = list(root.Definitions)
    instances = list(root.Group)
    if root.PlusSchema < 3 and (len(definitions) > 1 or len(instances) > 1):
        raise ValueError("The current pilot supports at most one definition and occurrence")
    if len(set(definitions)) != len(definitions):
        raise ValueError("Duplicate component identity")
    for definition in definitions:
        if definition.Document != doc or definition.TypeId != "App::Part" or definition == root:
            raise ValueError("Invalid domestic definition")
        if root.PlusSchema < 3 and not definition.Placement.isSame(App.Placement(), 1e-9):
            raise ValueError("Place the occurrence, not the stored definition")
        for obj in definition.Group:
            if root.PlusSchema >= 3 and obj.TypeId == "App::Link":
                instances.append(obj)
                continue
            if obj.TypeId == "PartDesign::Body":
                continue
            if root.PlusSchema >= 2 and obj.isDerivedFrom("Part::Feature"):
                continue
            raise ValueError("Unsupported component modeling content for this schema")
    for instance in instances:
        if (instance.TypeId != "App::Link" or instance.Document != doc
                or instance.LinkedObject not in [*definitions, *external_definitions]
                or (root.PlusSchema < 3 and instance.LinkTransform)
                or instance.LinkCopyOnChange != "Disabled" or instance.ElementCount):
            raise ValueError("Invalid shared component occurrence")
        if instance.Scale != 1 or not instance.ScaleVector.isEqual(App.Vector(1, 1, 1), 1e-9):
            raise ValueError("Scaled component links require a separate migration case")
    from .display import validate_local
    validate_local(root, definitions, instances)
    # Detect cycles across definitions, including unused catalog entries, before
    # native recompute traverses links. Shared DAG branches are visited only once.
    visited, active = set(), set()
    def visit(definition):
        if definition in active:
            raise ValueError("Circular component nesting is not allowed")
        if definition in visited:
            return
        active.add(definition)
        for child in definition.Group:
            if child.TypeId == "App::Link":
                visit(child.LinkedObject)
        active.remove(definition)
        visited.add(definition)
    for definition in definitions:
        visit(definition)
    # Follow ownership only, never general dependency links (which could hide orphans).
    owned = set()
    def collect(obj):
        if obj in owned:
            raise ValueError("Cyclic or multiply owned component content")
        owned.add(obj)
        for child in owned_children(obj):
            collect(child)
    collect(root)
    for definition in definitions:
        collect(definition)
    if owned != set(doc.Objects):
        raise ValueError("Document contains content outside component ownership")
    return root


def create_file_root(doc):
    """Create metadata/frame only; conversion must not insert a default Part001."""
    root = doc.addObject("App::Part", "File")
    root.Label = doc.Label
    root.addProperty("App::PropertyString", "PlusFormat", "Component document")
    root.PlusFormat = FORMAT
    root.addProperty("App::PropertyInteger", "PlusSchema", "Component document")
    root.PlusSchema = SCHEMA
    root.addProperty("App::PropertyLinkList", "Definitions", "Component document")
    from .external import add_properties
    add_properties(root)
    for prop in ("PlusFormat", "PlusSchema", "Definitions", "Placement"):
        root.setEditorMode(prop, 1)
    return root


def show_new_component_frame(definition):
    """Creation-only default; opening/importing/copying never resets saved visibility."""
    if App.GuiUp:
        definition.Origin.Visibility = True
        for feature in definition.Origin.OriginFeatures:
            feature.Visibility = True


def new_document(name="Unnamed"):
    """Create once; opening an existing document never calls this initializer."""
    doc = App.newDocument(name)
    doc.UndoMode = 1
    try:
        with transaction(doc, "New component document"):
            root = create_file_root(doc)
            definition = doc.addObject("App::Part", "Part001")
            show_new_component_frame(definition)
            root.Definitions = [definition]
            instance = doc.addObject("App::Link", "Part001Instance")
            instance.setLink(definition)
            instance.LinkTransform = False
            root.addObject(instance)
            if App.GuiUp:
                definition.Visibility = False
                instance.Visibility = True
        if App.GuiUp:
            from . import panel
            panel.show_created_component(doc, definition, (instance,))
        return doc
    except Exception:
        App.closeDocument(doc.Name)
        raise


def history(doc, definition=None):
    """Dependency sequence across Bodies, respecting saved preferred order."""
    root = validate(doc)
    if definition is None:
        return [root.Origin] + [o for o in root.Origin.OriginFeatures if o.TypeId == "App::Plane"]
    from .external import available_definitions
    if definition not in available_definitions(root):
        raise ValueError("Definition does not belong to this file")
    def features(obj):
        if obj.TypeId == "App::Link":
            return  # A child component has its own History.
        if obj.TypeId == "PartDesign::Body":
            for child in obj.Group:
                yield from features(child)
        else:
            if obj.TypeId == "PartDesign::Boolean":
                for tool in owned_children(obj):
                    yield from features(tool)
            yield obj
    nodes = list(dict.fromkeys(feature for obj in definition.Group for feature in features(obj)))
    dependencies = _history_dependencies(definition, nodes)
    # String identities do not add native dependency links. Deleted/reused names
    # cannot acquire a previous object's rank; unmatched new objects append.
    ranks = {key:i for i,key in enumerate(getattr(definition, 'PlusHistoryOrder', []))}
    def priority(obj):return (ranks.get(_history_key(obj),len(ranks)),obj.ID,obj.Name,obj)
    import heapq
    ready = [priority(obj) for obj in nodes if not dependencies[obj]]
    heapq.heapify(ready)
    followers = {obj: [] for obj in nodes}
    for obj, inputs in dependencies.items():
        for source in inputs:
            followers[source].append(obj)
    ordered = []
    while ready:
        _, _, _, obj = heapq.heappop(ready)
        ordered.append(obj)
        for follower in followers[obj]:
            dependencies[follower].remove(obj)
            if not dependencies[follower]:
                heapq.heappush(ready, priority(follower))
    if len(ordered) != len(nodes):
        raise ValueError('Circular feature dependencies prevent sequential History')
    return ordered


def _history_key(obj):
    return f'{obj.Name}:{obj.ID}'


def reorder_history(doc, definition, feature, position):
    """Move one visible feature, clamped between all inputs and consumers.

    Position is an insertion slot in the original feature-only sequence. The
    coordinate frame is structural and never participates in this sequence.
    """
    from . import modeling
    active, _ = modeling._context(doc)
    if active != definition:raise ValueError('The edited component changed; drag the feature again.')
    if definition.Document.HasPendingTransaction or App.getActiveTransaction():
        raise ValueError('Finish the current operation before reordering History.')
    ordered = history(doc, definition)
    if feature not in ordered:raise ValueError('Only modeling features can be reordered.')
    if not isinstance(position,int) or not 0 <= position <= len(ordered):
        raise ValueError('Invalid History insertion position.')
    dependencies = _history_dependencies(definition, ordered)
    def ancestors(obj):
        found=set();pending=list(dependencies[obj])
        while pending:
            source=pending.pop()
            if source not in found:
                found.add(source);pending.extend(dependencies[source])
        return found
    inputs=ancestors(feature)
    consumers={obj for obj in ordered if feature in ancestors(obj)}
    old=ordered.index(feature);remaining=[obj for obj in ordered if obj != feature]
    requested=position-(position>old)
    lower=max((i+1 for i,obj in enumerate(remaining) if obj in inputs),default=0)
    upper=min((i for i,obj in enumerate(remaining) if obj in consumers),default=len(remaining))
    actual=max(lower,min(requested,upper));message=''
    if requested>upper:
        blocker=remaining[upper]
        message=(f'"{feature.Label}" cannot be moved after "{blocker.Label}" because that feature depends on it.\n\n'
                 f'It has been placed immediately before "{blocker.Label}".')
    elif requested<lower:
        blocker=remaining[lower-1]
        message=(f'"{feature.Label}" cannot be moved before "{blocker.Label}" because it depends on that feature.\n\n'
                 f'It has been placed immediately after "{blocker.Label}".')
    result=remaining[:actual]+[feature]+remaining[actual:]
    if result != ordered:
        with transaction(definition.Document,'Reorder feature History'):
            if 'PlusHistoryOrder' not in definition.PropertiesList:
                definition.addProperty('App::PropertyStringList','PlusHistoryOrder','History')
                definition.setEditorMode('PlusHistoryOrder',2)
            definition.PlusHistoryOrder=[_history_key(obj) for obj in result]
    return message


def _history_inputs(definition, nodes, objects):
    """Resolve hidden native inputs to visible producers without crossing components.

    OutList includes native geometry links and expression dependencies. A Body used
    as a result reference means its Tip, not its ownership Group. Coordinate frames
    are implicit predecessors and child component occurrences have their own History.
    """
    visible, found, visited = set(nodes), set(), set()
    pending = list(objects)
    while pending:
        obj = pending.pop()
        if obj is None or obj in visited:
            continue
        visited.add(obj)
        if obj in visible:
            found.add(obj)
        elif obj.TypeId == 'PartDesign::Body' and owned_path(definition, obj) is not None:
            pending.append(obj.Tip)
        elif (obj.TypeId not in ('App::Part', 'App::Link', 'App::Origin')
              and owned_path(definition, obj) is not None):
            pending.extend(obj.OutList)
    return found


def _history_dependencies(definition, nodes):
    return {obj: _history_inputs(definition, nodes, obj.OutList) for obj in nodes}


def require_predecessors(definition, consumer, inputs):
    """Reject a new forward reference before an editor mutates native links.

    A new operation validates with its component as consumer and is appended after
    its inputs. Existing operations use their current dependency-correct History
    position, including repaired legacy order, rather than changing that position
    to accommodate a newly selected later input.
    """
    # Native command-start admission passes the Body before a feature exists.
    if consumer is None or consumer == definition or consumer.TypeId == 'PartDesign::Body':
        return
    ordered = history(definition.Document, definition)
    if consumer not in ordered:
        raise ValueError('The edited feature is no longer in component History')
    position = {obj: index for index, obj in enumerate(ordered)}
    objects = [obj.getSubObject(sub, 1) if sub else obj for obj, sub in inputs]
    for source in _history_inputs(definition, ordered, objects):
        if position[source] >= position[consumer]:
            raise ValueError(f'"{source.Label}" must precede "{consumer.Label}" in History; '
                             'Reorder History to put the input before this feature, then try again.')


def inspect_archive(filename):
    """Preflight the complete dependency graph before native restoration."""
    from .external import archive_graph
    archive_graph(filename)
    return Path(filename).resolve()


def open_document(filename, *, hidden=False):
    from .external import archive_graph
    graph = archive_graph(filename)
    path = Path(filename).resolve()
    before = set(App.listDocuments())
    # Native restore otherwise silently regenerates duplicate UUIDs. Never let an
    # already-open different file masquerade as a saved dependency (or vice versa).
    for existing in App.listDocuments().values():
        existing_path = Path(existing.FileName).resolve() if existing.FileName else None
        for saved_path, info in graph.items():
            if ((existing_path == saved_path and str(existing.Uid) != info["uid"])
                    or (str(existing.Uid) == info["uid"] and existing_path != saved_path)):
                raise ValueError("An open document conflicts with the saved file identity")
    previous = App.ActiveDocument
    try:
        for existing in App.listDocuments().values():
            if existing.FileName and Path(existing.FileName).resolve() == path:
                validate(existing)
                return existing
        doc = App.openDocument(str(path), hidden=hidden)
        validate(doc)
        if App.GuiUp and not hidden:
            from . import editing
            editing.edit_file(doc)
        if hidden and previous and previous.Name in App.listDocuments():
            App.setActiveDocument(previous.Name)
        return doc
    except Exception:
        for name in set(App.listDocuments()) - before:
            App.closeDocument(name)
        if previous and previous.Name in App.listDocuments():
            App.setActiveDocument(previous.Name)
        raise


def save_document(doc, filename=None):
    """Save the native archive at the exact path without changing CheckExtension.

    Native save() provides temporary-file replacement and backups. saveAs() cannot
    be used here because upstream appends .FCStd to unrecognized extensions.
    """
    root = validate(doc)
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current operation before saving")
    path = Path(filename or doc.FileName)
    if path.suffix.lower() != ".cadprt":
        raise ValueError("Choose a .cadprt filename")
    path = path.resolve()
    if doc.InList and doc.FileName and path != Path(doc.FileName).resolve():
        raise ValueError("A referenced defining file cannot change location during Save")
    from .external import check_saved_targets
    check_saved_targets(root)
    prefs = App.ParamGet("User parameter:BaseApp/Preferences/Document")
    if not prefs.GetBool("BackupPolicy", True):
        raise ValueError("Enable native safe-save BackupPolicy before saving a component file")
    if path.exists():
        inspect_archive(path)  # Do not overwrite foreign or future-schema files.
    gui_doc = None
    if App.GuiUp:
        import FreeCADGui as Gui
        gui_doc = Gui.getDocument(doc.Name)
    old_filename, old_label = doc.FileName, root.Label
    try:
        doc.FileName = str(path)
        root.Label = path.stem
        doc.recompute()
        doc.save()
        inspect_archive(path)
    except Exception:
        doc.FileName, root.Label = old_filename, old_label
        if gui_doc:
            gui_doc.Modified = True
        raise
    if gui_doc:
        gui_doc.Modified = False
    return path
