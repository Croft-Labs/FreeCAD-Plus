# SPDX-License-Identifier: LGPL-2.1-or-later
"""Versioned component document envelope over native FreeCAD persistence."""
import json
import os
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

import FreeCAD as App
import ComponentModel as Model

FORMAT = "org.freecad-plus.component-document"
MANIFEST = "ComponentManifest.json"
CAPABILITIES = ("components-v1", "native-objects-v1", "evaluated-references-v1")


def manifest(document, filename=None):
    """Called before native save opens its temporary output file."""
    meta = Model.validate(document)
    destination = filename or document.FileName
    if (meta.LegacySource and destination
            and Path(meta.LegacySource).resolve() == Path(destination).resolve()):
        raise ValueError("Save converted content to a new .cadprt file; the legacy original is protected.")
    definitions = []
    dependencies = {}
    for component in Model.definitions(document):
        occurrences = []
        for link in Model.children(component):
            source = link.LinkedObject
            external = source.Document != document
            if external:
                path = source.Document.FileName
                if not path or Path(path).suffix.lower() != ".cadprt":
                    raise ValueError("External components must be saved as .cadprt.")
                try:
                    relative = os.path.relpath(path, Path(destination).parent) if destination else path
                except ValueError:
                    relative = path  # Different Windows drives cannot be relative.
                dependencies[Model.metadata(source.Document).ObjectId] = relative
            occurrences.append({"id": link.ObjectId, "object": link.Name,
                                "definition": source.ObjectId, "external": external})
        definitions.append({"id": component.ObjectId, "object": component.Name,
                            "history": list(component.ModelHistory),
                            "results": list(component.ResultObjects),
                            "occurrences": occurrences})
    return json.dumps({"format": FORMAT, "version": Model.SCHEMA,
                       "required": list(CAPABILITIES), "document": meta.ObjectId,
                       "root": meta.RootComponent.ObjectId,
                       "definitions": definitions, "dependencies": dependencies},
                      ensure_ascii=False, sort_keys=True, indent=2)


def preflight(filename):
    """Refuse unknown required schema before native objects/proxies are restored."""
    with zipfile.ZipFile(filename) as archive:
        names = archive.namelist()
        if names.count(MANIFEST) != 1 or names.count("Document.xml") != 1:
            raise ValueError("Not a component document: required entries are missing or duplicated.")
        entry = archive.getinfo(MANIFEST)
        if entry.file_size > 16 * 1024 * 1024:
            raise ValueError("Component manifest exceeds the supported size.")
        data = json.loads(archive.read(MANIFEST))
    if (not isinstance(data, dict) or data.get("format") != FORMAT
            or type(data.get("version")) is not int or data["version"] != Model.SCHEMA):
        raise ValueError("Unsupported component document format/version.")
    required = data.get("required")
    if not isinstance(required, list) or any(c not in CAPABILITIES for c in required):
        raise ValueError("This component document requires unsupported reader capabilities.")
    if not set(CAPABILITIES) <= set(required):
        raise ValueError("Missing component document capability declarations.")
    definitions = data.get("definitions")
    if not isinstance(definitions, list) or not definitions:
        raise ValueError("Missing component definitions.")
    ids = [item["id"] for item in definitions]
    if len(ids) != len(set(ids)) or data.get("root") not in ids or not data.get("document"):
        raise ValueError("Invalid root or duplicate component identities.")
    with zipfile.ZipFile(filename) as archive:
        with archive.open("Document.xml") as stream:
            xml = ET.parse(stream)
    saved = {}
    for obj in xml.findall("./ObjectData/Object"):
        properties = {p.get("name"): p for p in obj.findall("./Properties/Property")}
        def value(name, tag):
            prop = properties.get(name)
            child = prop.find(tag) if prop is not None else None
            return child.get("value") if child is not None else None
        saved[obj.get("name")] = {"id": value("ObjectId", "String"),
                                  "role": value("ComponentRole", "String"),
                                  "root": value("RootComponent", "Link"),
                                  "version": value("SchemaVersion", "Integer")}
    documents = [o for o in saved.values() if o["role"] == "Document"]
    if (len(documents) != 1 or documents[0]["id"] != data["document"]
            or documents[0]["version"] != str(Model.SCHEMA)
            or saved.get(documents[0]["root"], {}).get("id") != data["root"]):
        raise ValueError("Component metadata differs from its format manifest.")
    if {o["id"] for o in saved.values() if o["role"] == "Definition"} != set(ids):
        raise ValueError("Component definitions differ from the format manifest.")
    return data


def open(filename, _opening=None):
    filename = str(Path(filename).resolve())
    for existing in App.listDocuments().values():
        if existing.FileName and Path(existing.FileName).resolve() == Path(filename):
            return existing
    opening = set() if _opening is None else _opening
    if filename in opening:
        raise ValueError("Cyclic external component files.")
    expected = preflight(filename)
    opening = opening | {filename}
    missing = []
    # Native links can partially load a definition without its document metadata.
    # Open required component files as full documents before native link restore.
    for document_id, dependency in expected.get("dependencies", {}).items():
        path = Path(dependency)
        if not path.is_absolute():
            path = Path(filename).parent / path
        try:
            source = open(path, opening)
        except FileNotFoundError:
            missing.append(str(path))
            continue
        if Model.metadata(source).ObjectId != document_id:
            raise ValueError("External file identity differs from the saved component dependency.")
    doc = App.openDocument(filename)
    try:
        meta = Model.validate(doc, allow_unresolved=bool(missing))
        if meta.ObjectId != expected["document"] or meta.RootComponent.ObjectId != expected["root"]:
            raise ValueError("The component manifest does not match the saved native objects.")
        for record in expected["definitions"]:
            definition = doc.getObject(record["object"])
            if (not Model.is_component(definition) or definition.ObjectId != record["id"]
                    or list(definition.ModelHistory) != record["history"]
                    or list(definition.ResultObjects) != record["results"]):
                raise ValueError("The saved component history differs from its manifest.")
            for instance in record["occurrences"]:
                occurrence = doc.getObject(instance["object"])
                if occurrence is None or occurrence.ObjectId != instance["id"]:
                    raise ValueError("An occurrence differs from its saved manifest.")
                if not hasattr(occurrence, "DefinitionId"):
                    Model._property(occurrence, "String", "DefinitionId", instance["definition"], True)
                elif occurrence.DefinitionId != instance["definition"]:
                    raise ValueError("An occurrence definition differs from its saved manifest.")
        # Broken reference geometry remains editable; format/identity failures above still refuse restore.
        Model.activate(meta.RootComponent, strict=False)
        if App.GuiUp and _opening is None:
            from freecad.gui.ComponentNavigator import show
            show(doc)
        return doc
    except Exception:
        App.closeDocument(doc.Name)
        raise


def insert(filename, docname):
    source = open(filename)
    target = App.getDocument(docname)
    return Model.add_component(Model.metadata(target).RootComponent,
                               Model.metadata(source).RootComponent)


def export(objects, filename):
    if not objects or any(o.Document != objects[0].Document for o in objects):
        raise ValueError("Save one complete component document; selected-object export is not supported.")
    document = objects[0].Document
    manifest(document)
    document.saveCopy(str(filename))


def legacy_plan(document):
    """Return a read-only inventory and proposed legacy conversion boundaries."""
    import LegacyConversion
    return LegacyConversion.inventory(document)


def convert_legacy(document):
    """Adopt compatible native geometry; preserve/report the remaining payloads."""
    if any(getattr(o, "ComponentRole", "") == "Document" for o in document.Objects):
        return document
    source_path = document.FileName
    originals = list(document.Objects)
    eligible = [o for o in originals if hasattr(o, "Shape") and Model.owner(o) is None
                and o.TypeId != "App::Link" and not hasattr(o, "ComponentRole")]
    with Model.transaction(document, "Convert legacy component document"):
        meta = Model.initialize(document, document.Label)
        meta.LegacySource = source_path
        root = meta.RootComponent
        report = []
        for obj in eligible:
            plain = obj.TypeId == "Part::Feature" or obj.isDerivedFrom("Sketcher::SketchObject")
            Model.register_object(root, obj, "Object" if plain else "Operation")
            if not obj.Shape.isNull() and obj.Shape.isValid():
                if obj.Shape.Solids or obj.Shape.Faces:
                    if plain:
                        root.ResultObjects = list(root.ResultObjects) + [obj.Name]
                    elif len(obj.Shape.Solids) <= 1:
                        Model.publish_result(root, obj, obj.Label + " result")
                    else:
                        report.append(obj.Label + ": native multi-solid payload retained; separate result mapping pending.")
            elif not obj.isDerivedFrom("Sketcher::SketchObject"):
                report.append(obj.Label + ": native history retained, but evaluated geometry needs repair.")
            if obj.TypeId == "PartDesign::Body":
                report.append(obj.Label + ": editable legacy Body history retained behind its evaluated result.")
        adopted = {o for obj in eligible for o in [obj] + list(obj.OutListRecursive)}
        unsupported = [o for o in originals if o not in adopted]
        report.extend(o.Label + " (" + o.TypeId + "): native payload retained; component/history mapping unavailable."
                      for o in unsupported)
        meta.ConversionReport = report or ["Native root geometry and editable inputs adopted; original file preserved."]
    # Never let ordinary Save overwrite the legacy original after conversion.
    document.FileName = ""
    return document


def open_legacy(filename):
    path = Path(filename).resolve()
    for existing in App.listDocuments().values():
        metas = [o for o in existing.Objects if getattr(o, "ComponentRole", "") == "Document"]
        if metas and metas[0].LegacySource and Path(metas[0].LegacySource).resolve() == path:
            App.setActiveDocument(existing.Name)
            return existing
    doc = App.openDocument(str(filename))
    try:
        return convert_legacy(doc)
    except Exception:
        App.closeDocument(doc.Name)
        raise
