# SPDX-License-Identifier: LGPL-2.1-or-later
"""Initial FCStd conversion. Never mutate an open source document or overwrite a file."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import uuid
import xml.etree.ElementTree as ET
import zipfile

import FreeCAD as App
from . import document as component


class ConversionError(ValueError):
    def __init__(self, message, report):
        super().__init__(message)
        self.report = report


def _inventory(doc):
    return [dict(name=obj.Name, label=obj.Label, type=obj.TypeId, id=obj.ID,
                 dependencies=[o.Name for o in obj.OutList],
                 expressions=list(obj.ExpressionEngine),
                 placement=list(obj.Placement.toMatrix().A) if "Placement" in obj.PropertiesList else None)
            for obj in doc.Objects]


def _body_objects(body):
    return {body, body.Origin, *body.Origin.OriginFeatures, *body.Group}


def _choose_content(doc, report, allow_geometry_fallback):
    if doc.Partial or doc.OutList or any("PlusFormat" in obj.PropertiesList for obj in doc.Objects):
        raise ConversionError("Expected a complete, domestic legacy FCStd document", report)
    if not doc.Objects:
        return None, False
    bodies = [obj for obj in doc.Objects if obj.TypeId == "PartDesign::Body"]
    if len(bodies) == 1 and _body_objects(bodies[0]) == set(doc.Objects):
        if any("Invalid" in obj.State or "Error" in obj.State for obj in doc.Objects):
            raise ConversionError("Repair the legacy feature errors before conversion", report)
        # Scripted features need their own migration, not an implicit claim of editability.
        if any("Python" in obj.TypeId for obj in bodies[0].Group):
            raise ConversionError("Scripted Body features require a later conversion case", report)
        return bodies[0], False
    if len(doc.Objects) == 1:
        obj = doc.Objects[0]
        if obj.TypeId in ("Part::Box", "Part::Feature"):
            return obj, False
        if (allow_geometry_fallback and obj.isDerivedFrom("Part::Feature")
                and not obj.OutList and "Shape" in obj.PropertiesList
                and not obj.Shape.isNull() and obj.Shape.isValid()):
            return obj, True
    raise ConversionError(
        "Unsupported legacy structure: no output written. Hierarchies, links and other "
        "feature graphs require later conversion cases; standalone shape fallback is explicit.", report)


def convert_file(source, destination, *, allow_geometry_fallback=False):
    """Return (converted document, report); the on-disk FCStd is always the source.

    Supported: empty files, one native Body with its owned features, or one Box/static
    Part feature. An explicitly requested standalone shape fallback discards its
    parametric behavior only in the new file and records this loss persistently.
    The destination must not exist. Native save is staged beside it, then published
    without replacement via an atomic hard link (failure leaves the source intact).
    """
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if source.suffix.lower() != ".fcstd" or destination.suffix.lower() != ".cadprt":
        raise ValueError("Choose an existing .FCStd source and a separate .cadprt destination")
    if not source.is_file():
        raise FileNotFoundError(source)
    if destination.exists():
        raise FileExistsError("Conversion never overwrites an existing destination")
    if not destination.parent.is_dir():
        raise FileNotFoundError(destination.parent)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    with zipfile.ZipFile(source) as archive:
        tree = ET.fromstring(archive.read("Document.xml"))
    uid = tree.find("./Properties/Property[@name='Uid']/Uuid")
    label = tree.find("./Properties/Property[@name='Label']/String")
    archived_objects = {o.get("name"): o.get("type") for o in tree.findall("./Objects/Object")}
    if uid is None or not archived_objects and tree.find("./Objects") is None:
        raise ValueError("This legacy archive version requires another conversion case")
    report = dict(source=source.name, source_sha256=digest, source_uid=uid.get("value"),
                  inventory=[], warnings=[], result="pending")
    previous = App.ActiveDocument.Name if App.ActiveDocument else None
    doc = App.newDocument("LegacyConversion")
    try:
        # restore() reads into a separate native document even if the source is open.
        # Never use openDocument(), which may return the user's live source document.
        doc.FileName = str(source)
        doc.restore()
        doc.FileName = ""
        doc.Label = label.get("value") if label is not None else source.stem
        # The retained source and its independently saved conversion are distinct files.
        doc.Uid = str(uuid.uuid4())
        report["converted_uid"] = str(doc.Uid)
        if {o.Name: o.TypeId for o in doc.Objects} != archived_objects:
            raise ConversionError("Native restore could not retain every archived object", report)
        doc.UndoMode = 1
        report["inventory"] = _inventory(doc)
        content, fallback = _choose_content(doc, report, allow_geometry_fallback)
        with component.transaction(doc, "Convert legacy component"):
            if fallback:
                name, label, shape = content.Name, content.Label, content.Shape.copy()
                placement = content.Placement
                color = content.ViewObject.ShapeColor if App.GuiUp else None
                visible = content.Visibility if App.GuiUp else True
                original_type = content.TypeId
                doc.removeObject(name)
                content = doc.addObject("Part::Feature", name)
                content.Label, content.Shape, content.Placement = label, shape, placement
                if App.GuiUp:
                    content.ViewObject.ShapeColor = color
                    content.Visibility = visible
                content.addProperty("App::PropertyString", "ConversionSourceType", "Conversion")
                content.ConversionSourceType = original_type
                report["warnings"].append(
                    f"{name}: preserved final geometry only; {original_type} parameters, "
                    "expressions and native object ID are not retained in the converted copy.")
            root = component.create_file_root(doc)
            if content:
                definition = doc.addObject("App::Part", "Component")
                definition.Label = content.Label
                definition.addObject(content)
                root.Definitions = [definition]
                instance = doc.addObject("App::Link", "ComponentInstance")
                instance.setLink(definition)
                instance.LinkTransform = False
                root.addObject(instance)
                if App.GuiUp:
                    definition.Visibility = False
                    instance.Visibility = True
            report["result"] = "geometry-only" if fallback else "native-preserved"
            root.addProperty("App::PropertyString", "ConversionReport", "Conversion")
            root.ConversionReport = json.dumps(report, ensure_ascii=False)
            root.setEditorMode("ConversionReport", 1)
        for item in report["inventory"]:
            obj = doc.getObject(item["name"])
            if not obj or obj.Label != item["label"]:
                raise ConversionError("Conversion changed an original name or label", report)
            if not fallback:
                if obj.TypeId != item["type"] or obj.ID != item["id"]:
                    raise ConversionError("Conversion changed a native object identity", report)
                if list(obj.ExpressionEngine) != item["expressions"]:
                    raise ConversionError("Conversion changed a native expression", report)
                if not set(item["dependencies"]).issubset({o.Name for o in obj.OutList}):
                    raise ConversionError("Conversion lost a native dependency", report)
            if item["placement"] is not None and any(
                    abs(a-b) > 1e-9 for a, b in zip(item["placement"], obj.Placement.toMatrix().A)):
                raise ConversionError("Conversion changed an authored placement", report)
            if "Invalid" in obj.State or "Error" in obj.State:
                raise ConversionError("Conversion produced an invalid native feature", report)
        if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
            raise ConversionError("The source changed during conversion; retry from its current version", report)
        with tempfile.TemporaryDirectory(prefix=".cadprt-convert-", dir=destination.parent) as staging:
            saved = component.save_document(doc, Path(staging) / destination.name)
            os.link(saved, destination)  # Atomic, exclusive publication; never replaces another file.
        doc.FileName = str(destination)
        if App.GuiUp:
            import FreeCADGui as Gui
            from . import editing
            editing.edit_file(doc)
            Gui.getDocument(doc.Name).Modified = False
        return doc, report
    except Exception:
        App.closeDocument(doc.Name)
        if previous in App.listDocuments():
            App.setActiveDocument(previous)
        raise
