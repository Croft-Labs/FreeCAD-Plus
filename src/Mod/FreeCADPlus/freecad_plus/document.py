# SPDX-License-Identifier: LGPL-2.1-or-later
"""Schema 1: native document, definition catalog, and a single placed component.

This deliberately bounded pilot is not a converter for legacy or archived Plus files.
Native object names qualified by Document.Uid supply persistent identity.
"""
from contextlib import contextmanager
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

import FreeCAD as App

FORMAT = "FreeCADPlus.ComponentDocument"
SCHEMA = 1


@contextmanager
def transaction(doc, label):
    """Do not consume or commit a caller's pending transaction."""
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current operation first")
    doc.openTransaction(label)
    try:
        yield
        doc.recompute()
        validate(doc)
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise
    else:
        doc.commitTransaction()


def validate(doc):
    """Return the unique root, rejecting unsupported or inconsistent ownership."""
    if doc.Partial:
        raise ValueError("A partially loaded component document cannot be edited or saved")
    if doc.OutList:
        raise ValueError("External definitions require a later schema and migration")
    roots = [o for o in doc.Objects if "PlusFormat" in o.PropertiesList]
    if len(roots) != 1:
        raise ValueError("Expected exactly one component file root")
    root = roots[0]
    if (root.TypeId != "App::Part" or root.PlusFormat != FORMAT
            or getattr(root, "PlusSchema", None) != SCHEMA):
        raise ValueError("Unsupported component document format or schema")
    if not root.Placement.isSame(App.Placement(), 1e-9):
        raise ValueError("The file coordinate frame must remain fixed")
    definitions = list(root.Definitions)
    instances = list(root.Group)
    if len(definitions) > 1 or len(instances) > 1:
        raise ValueError("Schema 1 pilot supports at most one definition and occurrence")
    if len(set(definitions)) != len(definitions):
        raise ValueError("Duplicate component identity")
    for definition in definitions:
        if definition.Document != doc or definition.TypeId != "App::Part" or definition == root:
            raise ValueError("Invalid domestic definition")
        if not definition.Placement.isSame(App.Placement(), 1e-9):
            raise ValueError("Place the occurrence, not the stored definition")
        if any(o.TypeId != "PartDesign::Body" for o in definition.Group):
            raise ValueError("Pilot modeling content must use native backend Bodies")
    for instance in instances:
        if (instance.TypeId != "App::Link" or instance.Document != doc
                or instance.LinkedObject not in definitions or instance.LinkTransform
                or instance.LinkCopyOnChange != "Disabled" or instance.ElementCount):
            raise ValueError("Invalid shared component occurrence")
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


def new_document(name="Unnamed"):
    """Create once; opening an existing document never calls this initializer."""
    doc = App.newDocument(name)
    doc.UndoMode = 1
    try:
        with transaction(doc, "New component document"):
            root = doc.addObject("App::Part", "File")
            root.Label = doc.Label
            root.addProperty("App::PropertyString", "PlusFormat", "Component document")
            root.PlusFormat = FORMAT
            root.addProperty("App::PropertyInteger", "PlusSchema", "Component document")
            root.PlusSchema = SCHEMA
            root.addProperty("App::PropertyLinkList", "Definitions", "Component document")
            for prop in ("PlusFormat", "PlusSchema", "Definitions", "Placement"):
                root.setEditorMode(prop, 1)
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
    if definition not in root.Definitions:
        raise ValueError("Definition does not belong to this file")
    return [feature for body in definition.Group for feature in body.Group]


def inspect_archive(filename):
    """Refuse unknown schemas before FreeCAD restores any objects from the file."""
    path = Path(filename)
    if path.suffix.lower() != ".cadprt":
        raise ValueError("Component documents require an exact .cadprt filename")
    with zipfile.ZipFile(path) as archive:
        tree = ET.fromstring(archive.read("Document.xml"))
    markers = tree.findall("./ObjectData/Object/Properties/Property[@name='PlusFormat']")
    if len(markers) != 1 or markers[0].find("String").get("value") != FORMAT:
        raise ValueError("Not a versioned component document; conversion is required")
    roots = [o for o in tree.findall("./ObjectData/Object")
             if o.find("./Properties/Property[@name='PlusFormat']") is not None]
    version = roots[0].find("./Properties/Property[@name='PlusSchema']/Integer")
    if version is None or version.get("value") != str(SCHEMA):
        raise ValueError("Unsupported component schema; the source was not changed")
    return path.resolve()


def open_document(filename):
    path = inspect_archive(filename)
    # Never close or replace a document the caller already has open on validation failure.
    for existing in App.listDocuments().values():
        if existing.FileName and Path(existing.FileName).resolve() == path:
            validate(existing)
            return existing
    doc = App.openDocument(str(path))
    try:
        validate(doc)
        if App.GuiUp:
            from . import editing
            editing.edit_file(doc)
        return doc
    except Exception:
        App.closeDocument(doc.Name)
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
