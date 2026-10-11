# SPDX-License-Identifier: LGPL-2.1-or-later
"""Imported catalogs and independent copies using native cross-document links.

No dialogs, implicit saves or label-based reference recovery. All entry points are
opt-in services for the later component panel.
"""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

import FreeCAD as App
from . import document


def add_properties(root):
    root.addProperty("App::PropertyXLinkList", "Imports", "Component document")
    root.addProperty("App::PropertyString", "ImportIdentities", "Component document")
    root.ImportIdentities = "[]"
    root.setEditorMode("Imports", 1)
    root.setEditorMode("ImportIdentities", 1)


def upgrade(doc):
    """Explicit undoable extension; opening old files does not migrate them."""
    root = document.validate(doc)
    if root.PlusSchema < 4:
        with document.transaction(doc, "Enable external component definitions"):
            if "Imports" not in root.PropertiesList:
                add_properties(root)
            root.PlusSchema = 4
    return root


def _root(doc):
    roots = [o for o in doc.Objects if "PlusFormat" in o.PropertiesList]
    if (len(roots) != 1 or roots[0].TypeId != "App::Part"
            or roots[0].PlusFormat != document.FORMAT
            or roots[0].PlusSchema not in document.SUPPORTED_SCHEMAS):
        raise ValueError("Unsupported component document format or schema")
    return roots[0]


def _imports(root):
    if root.PlusSchema < 4:
        if getattr(root, "Imports", []):
            raise ValueError("External definitions require explicit upgrade to schema 4")
        return []
    if ("Imports" not in root.PropertiesList or "ImportIdentities" not in root.PropertiesList
            or root.getTypeIdOfProperty("Imports") != "App::PropertyXLinkList"):
        raise ValueError("Missing external catalog metadata")
    imported = list(root.Imports)
    identities = json.loads(root.ImportIdentities)
    if (identities != [str(o.Document.Uid) for o in imported]
            or len(set(identities)) != len(identities)):
        raise ValueError("Missing or mismatched imported file identity")
    return imported


def available_definitions(root):
    """Caller validates first; nested file catalogs retain defining-file ownership."""
    result, seen = [], set()
    def visit(current):
        if current in seen:
            return
        seen.add(current)
        result.extend(current.Definitions)
        for imported in _imports(current):
            visit(imported)
    visit(root)
    return result


def validate_graph(doc):
    active, done, identities = set(), {}, {}
    def visit(current):
        if current in active:
            raise ValueError("Circular file imports are not allowed")
        if current in done:
            return done[current]
        uid = str(current.Uid)
        if uid in identities and identities[uid] != current:
            raise ValueError("Duplicate defining-file identity")
        identities[uid] = current
        root = _root(current)
        active.add(current)
        imports = _imports(root)
        external = []
        for imported in imports:
            target = visit(imported.Document)
            if target != imported:
                raise ValueError("Imported catalog must target the defining file root")
            external.extend(available_definitions(target))
        document._validate_local(current, external)
        # External dependencies are catalog entries or placed definition links,
        # never unpromoted cross-file modeling inputs.
        for obj in current.Objects:
            allowed = imports if obj == root else ([obj.LinkedObject] if obj.TypeId == "App::Link" else [])
            if any(target.Document != current and target not in allowed for target in obj.OutList):
                raise ValueError("Unsupported cross-file modeling reference")
        active.remove(current)
        done[current] = root
        return root
    return visit(doc)


def catalog(doc):
    """Nested projection: domestic definitions first; imports never place geometry."""
    root = document.validate(doc)
    def project(current):
        return {"document": current.Document, "definitions": tuple(current.Definitions),
                "imports": tuple(project(child) for child in _imports(current))}
    return project(root)


def qualified_label(definition, viewing_doc):
    if definition not in available_definitions(document.validate(viewing_doc)):
        raise ValueError("Definition is not available in this file")
    if definition.Document == viewing_doc:
        return definition.Label
    return f"{definition.Label} ({Path(definition.Document.FileName).stem})"


def _saved(doc):
    if not doc.FileName or not Path(doc.FileName).is_file():
        raise ValueError("Save both defining files as .cadprt before importing")
    graph = archive_graph(doc.FileName)
    if graph[Path(doc.FileName).resolve()]["uid"] != str(doc.Uid):
        raise ValueError("Saved file identity does not match the open document")
    return graph


def import_file(doc, source):
    """Register a saved source document's complete catalog, without placements."""
    root, target = document.validate(doc), document.validate(source)
    if root.PlusSchema < 4:
        raise ValueError("External definitions require explicit upgrade to schema 4")
    _saved(doc)
    _saved(source)
    todo, seen = [target], set()
    while todo:
        current = todo.pop()
        if current.Document == doc or str(current.Document.Uid) == str(doc.Uid):
            raise ValueError("Circular file imports are not allowed")
        if current in seen:
            continue
        seen.add(current)
        todo.extend(_imports(current))
    if target in _imports(root):
        return target
    with document.transaction(doc, "Import component catalog"):
        root.Imports = [*root.Imports, target]
        root.ImportIdentities = json.dumps([str(o.Document.Uid) for o in root.Imports])
    return target


def save_definition(definition):
    """Save the owning file, not whichever assembly tab supplied Edit context."""
    owner = definition.Document
    if definition not in document.validate(owner).Definitions:
        raise ValueError("Expected a defining-file component")
    return document.save_document(owner)


def archive_graph(filename):
    """Read native XLink paths and UUIDs before any FreeCAD restore can run.

    Missing/replaced/unsupported dependencies fail without opening documents.
    Recovery is restoring the original path/identity and retrying. Relocation UI
    and automatic path searching are deliberately not part of this service.
    """
    active, done, identities = set(), {}, {}
    def visit(filename):
        path = Path(filename).resolve()
        if path in active:
            raise ValueError("Circular file imports are not allowed")
        if path in done:
            return done[path]
        if path.suffix.lower() != ".cadprt":
            raise ValueError("Component documents require an exact .cadprt filename")
        if not path.is_file():
            raise ValueError(f"Missing defining file: {path}. Restore it and retry.")
        with zipfile.ZipFile(path) as archive:
            tree = ET.fromstring(archive.read("Document.xml"))
        roots = [o for o in tree.findall("./ObjectData/Object")
                 if o.find("./Properties/Property[@name='PlusFormat']") is not None]
        if len(roots) != 1:
            raise ValueError("Not a versioned component document; conversion is required")
        root = roots[0]
        def prop(name, tag):
            return root.find(f"./Properties/Property[@name='{name}']/{tag}")
        marker, schema = prop("PlusFormat", "String"), prop("PlusSchema", "Integer")
        if (marker is None or marker.get("value") != document.FORMAT or schema is None
                or schema.get("value") not in {str(v) for v in document.SUPPORTED_SCHEMAS}):
            raise ValueError("Unsupported component schema; the source was not changed")
        uid_node = tree.find("./Properties/Property[@name='Uid']/Uuid")
        if uid_node is None:
            raise ValueError("Missing defining-file identity")
        uid = uid_node.get("value")
        if uid in identities and identities[uid] != path:
            raise ValueError("Duplicate defining-file identity at different paths")
        identities[uid] = path
        active.add(path)
        imports = root.findall("./Properties/Property[@name='Imports']/XLinkSubList/XLink")
        if int(schema.get("value")) < 4 and imports:
            raise ValueError("External definitions require schema 4")
        recorded = prop("ImportIdentities", "String")
        ids = json.loads(recorded.get("value")) if recorded is not None else []
        if int(schema.get("value")) >= 4 and recorded is None:
            raise ValueError("Missing external catalog metadata")
        if len(ids) != len(imports) or len(set(ids)) != len(ids):
            raise ValueError("Missing or mismatched imported file identity")
        allowed = set()
        for link, expected in zip(imports, ids):
            child = (path.parent / link.get("file", "")).resolve()
            info = visit(child)
            if info["uid"] != expected or info["root"] != link.get("name"):
                raise ValueError(f"Imported file identity mismatch: {child}")
            allowed.update([child, *info["dependencies"]])
        # Check every native external XLink, including instance targets, against
        # the declared catalog. A missing definition never falls back to a label.
        for obj in tree.findall("./ObjectData/Object"):
            for property_node in obj.findall("./Properties/Property"):
                for link in property_node.findall(".//XLink"):
                    if not link.get("file"):
                        continue
                    target_path = (path.parent / link.get("file")).resolve()
                    if target_path not in allowed:
                        raise ValueError("External reference is outside the defining-file catalog")
                    target = done[target_path]
                    is_catalog = obj == root and property_node.get("name") == "Imports"
                    valid_names = [target["root"]] if is_catalog else target["definitions"]
                    if (not is_catalog and property_node.get("name") != "LinkedObject"
                            or link.get("name") not in valid_names):
                        raise ValueError("Missing or unsupported external definition target")
        definitions = [link.get("value") for link in root.findall(
            "./Properties/Property[@name='Definitions']/LinkList/Link")]
        info = {"uid": uid, "root": root.get("name"), "definitions": definitions,
                "dependencies": allowed}
        active.remove(path)
        done[path] = info
        return info
    visit(filename)
    return done


def check_saved_targets(root):
    """Saving an importer cannot serialize an unsaved source definition silently."""
    definitions = available_definitions(root)
    saved_paths = set()
    for imported in _imports(root):
        saved_paths.update(_saved(imported.Document))
    graphs = {}
    for obj in root.Document.Objects:
        if obj.TypeId != "App::Link" or obj.LinkedObject.Document == root.Document:
            continue
        target = obj.LinkedObject
        source = target.Document
        if Path(source.FileName).resolve() not in saved_paths:
            raise ValueError("Save the changed import catalog in its defining file first")
        if source not in graphs:
            graphs[source] = _saved(source)[Path(source.FileName).resolve()]
        if target not in definitions or target.Name not in graphs[source]["definitions"]:
            raise ValueError("Save the new definition in its defining file before saving this assembly")


def copy_definition(source, destination, label, *, placements_to_replace, child_labels=None):
    """Copy an independent native graph; replacement selection is always explicit.

    The future UI must obtain that selection from the owner. An empty tuple keeps
    every original placement. Nested definition labels must be unique in the target.
    Native deep-copy remaps internal features, expressions and shared child links.
    """
    root = document.validate(destination)
    if root.PlusSchema < 3:
        raise ValueError("Independent copies require hierarchy schema 3 or later")
    if source not in document.validate(source.Document).Definitions:
        raise ValueError("Expected a component definition")
    definitions, seen = [], set()
    def collect(current):
        if current in seen:
            return
        seen.add(current)
        definitions.append(current)
        for child in current.Group:
            if child.TypeId == "App::Link":
                collect(child.LinkedObject)
    collect(source)
    names = [label] + [(child_labels or {}).get(d, d.Label) for d in definitions[1:]]
    existing = {d.Label for d in root.Definitions}
    if any(not name.strip() or name in existing for name in names) or len(set(names)) != len(names):
        raise ValueError("Choose unique names for every copied definition in the destination file")
    replacements = tuple(placements_to_replace)
    owners = [root, *root.Definitions]
    for instance in replacements:
        if (instance.Document != destination or instance.TypeId != "App::Link"
                or instance.LinkedObject != source or not any(instance in o.Group for o in owners)):
            raise ValueError("Replacement placements must belong to the destination and target the source")
    before = set(destination.Objects)
    with document.transaction(destination, "Copy independent component definition"):
        copies = destination.copyObject(definitions, True)
        if len(copies) != len(definitions):
            raise ValueError("Native copy did not return the complete definition graph")
        created = set(destination.Objects) - before
        if any(target not in created for obj in created for target in obj.OutList):
            raise ValueError("Native copy retained a source dependency; copy was rolled back")
        for copied, name in zip(copies, names):
            copied.Label = name
            if App.GuiUp:
                copied.Visibility = False
        root.Definitions = [*root.Definitions, *copies]
        for instance in replacements:
            placement, transform = instance.LinkPlacement, instance.LinkTransform
            instance.setLink(copies[0])
            instance.LinkTransform = transform
            instance.LinkPlacement = placement
    return copies[0]
