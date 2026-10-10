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
BASE_CAPABILITIES = ("components-v1", "native-objects-v1", "evaluated-references-v1")
CAPABILITIES = BASE_CAPABILITIES + ("component-file-imports-v1", "component-file-container-v1",
                                    "component-file-assembly-v1", "component-part-types-v1")


def manifest(document, filename=None):
    """Called before native save opens its temporary output file."""
    meta = Model.validate(document)
    destination = filename or document.FileName
    if destination:
        target = Path(destination).resolve()
        # Save As temporarily changes document.FileName before this preflight.
        # Compare the actual output against other documents, never that old path.
        if any(other != document and other.FileName
               and Path(other.FileName).resolve() == target
               for other in App.listDocuments().values()):
            raise ValueError("Another open document owns this file. Choose a different save location.")
    if (meta.LegacySource and destination
            and Path(meta.LegacySource).resolve() == Path(destination).resolve()):
        raise ValueError("Save converted content to a new .cadprt file; the legacy original is protected.")
    definitions = []
    dependencies = {}
    for source in Model.external_documents(document):
        path = source.FileName
        if not path or Path(path).suffix.lower() != ".cadprt":
            raise ValueError("External components must be saved as .cadprt.")
        try:
            relative = os.path.relpath(path, Path(destination).parent) if destination else path
        except ValueError:
            relative = path  # Different Windows drives cannot be relative.
        dependencies[Model.metadata(source).ObjectId] = relative
    for component in Model.definitions(document):
        occurrences = []
        for link in Model.children(component):
            source = link.LinkedObject
            occurrences.append({"id": link.ObjectId, "object": link.Name,
                                "definition": source.ObjectId,
                                "external": source.Document != document})
            if "PartType" in link.PropertiesList:
                occurrences[-1]["part_type"] = Model.part_type(component, link)
        definitions.append({"id": component.ObjectId, "object": component.Name,
                            "history": list(component.ModelHistory),
                            "results": list(component.ResultObjects),
                            "occurrences": occurrences})
    imports = [{"id": record.ObjectId, "object": record.Name,
                "document": record.DocumentId} for record in Model.file_imports(document)]
    data = {"format": FORMAT, "version": Model.SCHEMA,
            "required": list(BASE_CAPABILITIES), "document": meta.ObjectId,
            "root": meta.RootComponent.ObjectId,
            "definitions": definitions, "dependencies": dependencies}
    if any("part_type" in link for item in definitions for link in item["occurrences"]):
        data["required"].append("component-part-types-v1")
    if Model.is_file_container(meta.RootComponent):
        data["file_container"] = meta.RootComponent.ObjectId
        data["required"].append("component-file-container-v1")
    if imports:
        data["imports"] = imports
        data["required"].append("component-file-imports-v1")
    assembly = Model.assembly_record(document)
    if assembly is not None:
        data["assembly"] = assembly
        data["required"].append("component-file-assembly-v1")
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2)


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
    if not set(BASE_CAPABILITIES) <= set(required):
        raise ValueError("Missing component document capability declarations.")
    has_container = "component-file-container-v1" in required
    if (("file_container" in data) != has_container
            or (has_container and data["file_container"] != data.get("root"))):
        raise ValueError("Invalid file container capability or identity.")
    has_assembly = "component-file-assembly-v1" in required
    if (("assembly" in data) != has_assembly or (has_assembly and not has_container)):
        raise ValueError("Invalid file assembly capability declaration.")
    dependencies = data.get("dependencies")
    if (not isinstance(dependencies, dict)
            or any(not isinstance(key, str) or not key or not isinstance(value, str) or not value
                   for key, value in dependencies.items())):
        raise ValueError("Invalid component file dependency records.")
    imports = data.get("imports", [])
    if not isinstance(imports, list) or any(not isinstance(item, dict) for item in imports):
        raise ValueError("Invalid component file imports.")
    if bool(imports) != ("component-file-imports-v1" in required):
        raise ValueError("Component file imports require their reader capability.")
    for field in ("id", "object", "document"):
        values = [item.get(field) for item in imports]
        if (any(not isinstance(value, str) or not value for value in values)
                or len(values) != len(set(values))):
            raise ValueError("Duplicate or missing component file import identities.")
    if any(item["document"] not in dependencies or item["document"] == data.get("document")
           for item in imports):
        raise ValueError("Invalid imported component file dependency.")
    definitions = data.get("definitions")
    if not isinstance(definitions, list) or not definitions:
        raise ValueError("Missing component definitions.")
    def strings(values):
        return (isinstance(values, list)
                and all(isinstance(value, str) and value for value in values)
                and len(values) == len(set(values)))
    if any(not isinstance(item, dict)
           or any(not isinstance(item.get(key), str) or not item[key] for key in ("id", "object"))
           or not strings(item.get("history")) or not strings(item.get("results"))
           or not isinstance(item.get("occurrences"), list) for item in definitions):
        raise ValueError("Invalid component definition records.")
    occurrences = [instance for item in definitions for instance in item["occurrences"]]
    if any(not isinstance(item, dict)
           or any(not isinstance(item.get(key), str) or not item[key]
                  for key in ("id", "object", "definition"))
           or type(item.get("external")) is not bool for item in occurrences):
        raise ValueError("Invalid component occurrence records.")
    if (any("part_type" in item and item["part_type"] not in Model.PART_TYPES
            for item in occurrences)
            or any("part_type" in item for item in occurrences)
            != ("component-part-types-v1" in required)):
        raise ValueError("Invalid component part type capability or value.")
    if (not strings([item["object"] for item in definitions])
            or any(not strings([item[key] for item in occurrences]) for key in ("id", "object"))):
        raise ValueError("Duplicate component definition or occurrence records.")
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
        linked = obj.find('./Properties/Property[@name="LinkedObject"]/XLink')
        saved[obj.get("name")] = {"id": value("ObjectId", "String"),
                                  "role": value("ComponentRole", "String"),
                                  "part_type": value("PartType", "String"),
                                  "file_container": value("FileContainer", "Bool") == "true",
                                  "root": value("RootComponent", "Link"),
                                  "assembly_root": value("ComponentRoot", "Link"),
                                  "ground": value("ObjectToGround", "Link"),
                                  "references": [
                                      (ref.get("name"), ref.get("file")) if ref is not None else None
                                      for ref in [obj.find(
                                          './Properties/Property[@name="%s"]/XLink' % name)
                                          for name in ("Reference1", "Reference2")]],
                                  "version": value("SchemaVersion", "Integer"),
                                  "document": value("DocumentId", "String"),
                                  "definition": value("DefinitionId", "String"),
                                  "group": [link.get("value") for link in obj.findall(
                                      './Properties/Property[@name="Group"]/LinkList/Link')],
                                  "external": bool(linked is not None and linked.get("file"))}
    documents = [o for o in saved.values() if o["role"] == "Document"]
    if (len(documents) != 1 or documents[0]["id"] != data["document"]
            or documents[0]["version"] != str(Model.SCHEMA)
            or saved.get(documents[0]["root"], {}).get("id") != data["root"]):
        raise ValueError("Component metadata differs from its format manifest.")
    if {name: o["id"] for name, o in saved.items() if o["role"] == "Definition"} != {
            item["object"]: item["id"] for item in definitions}:
        raise ValueError("Component definitions differ from the format manifest.")
    containers = [item for item in saved.values() if item["file_container"]]
    if (len(containers) != int(has_container)
            or (containers and (containers[0]["role"] != "Definition"
                                or containers[0]["id"] != data["root"]))):
        raise ValueError("Native file container differs from its format manifest.")
    saved_occurrences = {name: item for name, item in saved.items() if item["role"] == "Occurrence"}
    if set(saved_occurrences) != {item["object"] for item in occurrences}:
        raise ValueError("Component occurrences differ from the format manifest.")
    for definition in definitions:
        native = saved[definition["object"]]
        if {name for name in native["group"] if name in saved_occurrences} != {
                item["object"] for item in definition["occurrences"]}:
            raise ValueError("Component occurrence ownership differs from the format manifest.")
    for instance in occurrences:
        native = saved_occurrences[instance["object"]]
        if native["part_type"] != instance.get("part_type"):
            raise ValueError("Native component part type differs from its manifest.")
        if (native["id"] != instance["id"] or native["external"] != instance["external"]
                or (native["definition"] is not None and native["definition"] != instance["definition"])):
            raise ValueError("Component occurrence identity differs from the format manifest.")
    saved_imports = {name: (item["id"], item["document"]) for name, item in saved.items()
                     if item["role"] == "FileImport"}
    if saved_imports != {item["object"]: (item["id"], item["document"]) for item in imports}:
        raise ValueError("Component file imports differ from their format manifest.")
    contexts = [(name, item) for name, item in saved.items() if item["role"] == "AssemblyContext"]
    if len(contexts) != int(has_assembly):
        raise ValueError("File assembly context differs from its manifest.")
    if contexts:
        name, native = contexts[0]
        types = {obj.get("name"): obj.get("type") for obj in xml.findall("./Objects/Object")}
        groups = [child for child in native["group"] if types.get(child) == "Assembly::JointGroup"]
        if (types.get(name) != "Assembly::AssemblyObject" or len(groups) != 1
                or native["assembly_root"] != documents[0]["root"]):
            raise ValueError("Invalid native file assembly ownership.")
        group = groups[0]
        joints = []
        root_members = saved[native["assembly_root"]]["group"]
        for child in saved[group]["group"]:
            joint = saved.get(child, {})
            if joint.get("ground"):
                endpoints = [joint["ground"]]
            else:
                refs = joint.get("references", [])
                if len(refs) != 2 or any(ref is None or ref[1] for ref in refs):
                    raise ValueError("Invalid native file relationship endpoints.")
                endpoints = [ref[0] for ref in refs]
            if (len(set(endpoints)) != len(endpoints)
                    or any(endpoint not in root_members or endpoint not in saved_occurrences
                           for endpoint in endpoints)):
                raise ValueError("File relationship endpoint is not a direct occurrence.")
            joints.append({"object": child, "endpoints": endpoints})
        record = {"id": native["id"], "object": name, "root": native["assembly_root"],
                  "group": group, "joints": sorted(joints, key=lambda item: item["object"])}
        if record != data["assembly"]:
            raise ValueError("File assembly relationships differ from their manifest.")
    return data


def open(filename, _opening=None):
    """Restore a file graph without leaving partial loads after a failed open."""
    if _opening is not None:
        return _open(filename, _opening)
    existing = set(App.listDocuments())
    active = App.ActiveDocument.Name if App.ActiveDocument else ""
    try:
        return _open(filename)
    except Exception:
        # Include native auto-loaded documents, not just explicit recursive opens.
        # Previously open dependencies and unsaved user documents remain untouched.
        for name in reversed(list(App.listDocuments())):
            if name not in existing:
                App.closeDocument(name)
        App.setActiveDocument(active)
        raise


def _open(filename, _opening=None):
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
        meta = Model.validate(doc, allow_unresolved=True)
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
        if Model.assembly_record(doc) != expected.get("assembly"):
            raise ValueError("Restored file relationships differ from their manifest.")
        # Broken reference geometry remains editable; format/identity failures above still refuse restore.
        import LegacyConversion
        LegacyConversion.upgrade_datum_frames(doc)
        # Verify the saved graph above before adding the file-only root. Keep the
        # original definition and every reference target; only the in-memory file
        # gains a container until the owner explicitly saves it.
        if not Model.is_file_container(meta.RootComponent):
            Model.ensure_file_container(doc)
            # This is an open-time upgrade, not an editable assembly operation.
            # Undo must never remove the pinned file root of a newly opened file.
            doc.clearUndos()
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
    """Map definitions/instances, retaining native features and usable outputs."""
    import LegacyConversion
    if any(getattr(o, "ComponentRole", "") == "Document" for o in document.Objects):
        return LegacyConversion.upgrade_datum_frames(document)
    shapes = LegacyConversion.recovery_shapes(document)
    try:
        return LegacyConversion.convert_structure(document)
    except (ValueError, RuntimeError) as error:
        return LegacyConversion.recover_structure(document, shapes, error)



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
