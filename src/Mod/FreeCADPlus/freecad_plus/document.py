# SPDX-License-Identifier: LGPL-2.1-or-later
"""Versioned native document, definition catalog, and shared component hierarchies.

Legacy conversion is explicitly handled by conversion.py, never by ordinary open.
Native object names qualified by Document.Uid supply persistent identity.
"""
from contextlib import contextmanager
from pathlib import Path

import FreeCAD as App

FORMAT = "FreeCADPlus.ComponentDocument"
SCHEMA = 4
SUPPORTED_SCHEMAS = (1, 2, 3, 4)


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
        if obj.TypeId in ("App::Part", "PartDesign::Body"):
            collect(obj.Origin)
            for child in obj.Group:
                collect(child)
        elif obj.TypeId == "App::Origin":
            for child in obj.OriginFeatures:
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


def new_document(name="Unnamed"):
    """Create once; opening an existing document never calls this initializer."""
    doc = App.newDocument(name)
    doc.UndoMode = 1
    try:
        with transaction(doc, "New component document"):
            root = create_file_root(doc)
            definition = doc.addObject("App::Part", "Part001")
            root.Definitions = [definition]
            instance = doc.addObject("App::Link", "Part001Instance")
            instance.setLink(definition)
            instance.LinkTransform = False
            root.addObject(instance)
            if App.GuiUp:
                definition.Visibility = False
                instance.Visibility = True
        if App.GuiUp:
            from . import editing
            editing.edit(instance)
        return doc
    except Exception:
        App.closeDocument(doc.Name)
        raise


def history(doc, definition=None):
    """Projection only: file frame or native sketch/feature sequence, no Body rows."""
    root = validate(doc)
    if definition is None:
        return [root.Origin] + [o for o in root.Origin.OriginFeatures if o.TypeId == "App::Plane"]
    from .external import available_definitions
    if definition not in available_definitions(root):
        raise ValueError("Definition does not belong to this file")
    return [feature for obj in definition.Group
            for feature in (obj.Group if obj.TypeId == "PartDesign::Body" else [obj])
            if obj.TypeId != "App::Link"]


def inspect_archive(filename):
    """Preflight the complete dependency graph before native restoration."""
    from .external import archive_graph
    archive_graph(filename)
    return Path(filename).resolve()


def open_document(filename):
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
        doc = App.openDocument(str(path))
        validate(doc)
        if App.GuiUp:
            from . import editing
            editing.edit_file(doc)
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
