# SPDX-License-Identifier: LGPL-2.1-or-later
"""Document layers without group membership, dependency links or visibility snapshots.

Native properties provide transactions and persistence. Layer IDs are document-local;
component occurrences display their definition's layers, never copy its ownership.
"""
from contextlib import contextmanager
import json
import uuid

import FreeCAD as App

BASE = "base"
PROPERTY = "DesignLayer"
_busy = False
_installed = False


def origin(obj):
    return (obj.isDerivedFrom("App::Origin") or obj.isDerivedFrom("App::OriginFeature")
            or any(obj in container.OriginFeatures for container in obj.Document.Objects
                   if container.isDerivedFrom("App::Origin")))


def eligible(obj):
    if obj is None or hasattr(obj, "DesignLayerData"):
        return False
    if getattr(obj, "ComponentRole", "") in ("Document", "Definition", "Occurrence", "Internal"):
        return False
    if obj.isDerivedFrom("App::Link") or obj.isDerivedFrom("App::Part"):
        return False
    return (origin(obj) or hasattr(obj, "Shape") or obj.isDerivedFrom("App::DatumElement")
            or getattr(obj, "ComponentRole", "") in ("Object", "Operation", "Result", "Reference"))


def independent(obj):
    return (origin(obj) or obj.isDerivedFrom("Sketcher::SketchObject")
            or obj.isDerivedFrom("Part::Datum") or obj.isDerivedFrom("App::DatumElement"))


def units(doc):
    """Map each indivisible history object to its assignment owner.

    Only native Body membership and explicit component result/consumption links
    join units. Arbitrary OutList recursion would incorrectly swallow sketches.
    """
    objects = list(doc.Objects)
    parent = {obj: obj for obj in objects if eligible(obj)}
    rank = {obj: i for i, obj in enumerate(objects)}

    def root(obj):
        while parent[obj] != obj:
            parent[obj] = parent[parent[obj]]
            obj = parent[obj]
        return obj

    def join(a, b):
        if a not in parent or b not in parent or independent(a) or independent(b):
            return
        a, b = root(a), root(b)
        # A native Body owns its operations, even if imported after those features.
        key = lambda obj: (not obj.isDerivedFrom("PartDesign::Body"), rank[obj])
        if key(a) > key(b):
            a, b = b, a
        parent[b] = a

    for obj in parent:
        body = obj.getParentGeoFeatureGroup()
        if body and body.isDerivedFrom("PartDesign::Body"):
            join(body, obj)
        if getattr(obj, "ComponentRole", "") == "Result" and not getattr(obj, "Frozen", False):
            join(obj, getattr(obj, "Producer", None))
        if getattr(obj, "ComponentRole", "") == "Operation":
            for consumed in getattr(obj, "ConsumedResults", []):
                join(obj, consumed)
    return {obj: root(obj) for obj in parent}


def manager(doc):
    return next((obj for obj in doc.Objects if hasattr(obj, "DesignLayerData")), None)


class _Metadata:
    def dumps(self):
        return None

    def loads(self, state):
        pass

    def onDocumentRestored(self, obj):
        if App.GuiUp:
            from freecad.gui.DesignLayersGui import schedule
            schedule()


def state(doc):
    obj = manager(doc)
    if obj is None:
        return {"version": 1, "active": BASE,
                "layers": [{"id": BASE, "name": "Base", "visible": True}]}
    data = json.loads(obj.DesignLayerData)
    if data.get("version") != 1:
        raise ValueError("This document uses an unsupported layer format.")
    return data


def _store(doc, data):
    manager(doc).DesignLayerData = json.dumps(data, ensure_ascii=False, sort_keys=True)


def _assign(obj, layer):
    if PROPERTY not in obj.PropertiesList:
        obj.addProperty("App::PropertyString", PROPERTY, "Design Layers",
                        "Document layer ID; edit with the Layers task", 8)  # NoRecompute
        obj.setEditorMode(PROPERTY, 1)
    if obj.DesignLayer != layer:
        obj.DesignLayer = layer


def initialize(doc, new=False):
    """Migrate missing assignments to Base; never replace document objects."""
    global _busy
    if _busy or doc.Restoring:
        return
    _busy = True
    try:
        meta = manager(doc)
        if meta is None:
            data = state(doc)
            meta = doc.addObject("App::FeaturePython", "DesignLayers")
            meta.addProperty("App::PropertyString", "DesignLayerData", "Design Layers", "Layer schema", 8)
            meta.DesignLayerData = json.dumps(data)
            meta.setEditorMode("DesignLayerData", 2)
            meta.Proxy = _Metadata()
        data = state(doc)
        ids = {layer["id"] for layer in data["layers"]}
        owners = units(doc)
        for obj, owner in owners.items():
            layer = getattr(owner, PROPERTY, data["active"] if new else BASE)
            if origin(obj) or layer not in ids:
                layer = BASE
            _assign(obj, layer)
        if App.GuiUp and meta.ViewObject:
            meta.ViewObject.ShowInTree = False
            if meta.ViewObject.Visibility:
                meta.ViewObject.Visibility = False
    finally:
        _busy = False


def layer_of(obj, owners=None):
    if origin(obj):
        return BASE
    owners = units(obj.Document) if owners is None else owners
    return getattr(owners.get(obj, obj), PROPERTY, BASE)


def visible(obj, owners=None):
    layer = layer_of(obj, owners)
    return next((row["visible"] for row in state(obj.Document)["layers"] if row["id"] == layer), True)


def targets(doc, objects):
    owners = units(doc)
    return list(dict.fromkeys(owners[obj] for obj in objects
                             if obj in owners and not origin(obj)))


@contextmanager
def transaction(doc, title):
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current edit before changing layers.")
    initialize(doc)
    doc.openTransaction(title)
    try:
        yield
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        raise
    finally:
        if App.GuiUp:
            from freecad.gui.DesignLayersGui import schedule
            schedule()


def _row(data, layer):
    return next(row for row in data["layers"] if row["id"] == layer)


def _name(data, name, excluding=None):
    name = name.strip()
    if not name or "\x00" in name:
        raise ValueError("Enter a layer name.")
    if any(row["id"] != excluding and row["name"].casefold() == name.casefold() for row in data["layers"]):
        raise ValueError("A layer with that name already exists.")
    return name


def create(doc, name):
    data = state(doc)
    name = _name(data, name)
    layer = str(uuid.uuid4())
    with transaction(doc, "Create layer"):
        data["layers"].append({"id": layer, "name": name, "visible": True})
        _store(doc, data)
    return layer


def rename(doc, layer, name):
    if layer == BASE:
        raise ValueError("Base cannot be renamed.")
    data = state(doc)
    name = _name(data, name, layer)
    with transaction(doc, "Rename layer"):
        _row(data, layer)["name"] = name
        _store(doc, data)


def activate(doc, layer):
    data = state(doc)
    _row(data, layer)
    with transaction(doc, "Change active layer"):
        data["active"] = layer
        _store(doc, data)


def set_visible(doc, layer, value):
    data = state(doc)
    with transaction(doc, "Change layer visibility"):
        _row(data, layer)["visible"] = bool(value)
        _store(doc, data)


def move(doc, objects, layer):
    _row(state(doc), layer)
    selected = targets(doc, objects)
    if not selected:
        return False
    with transaction(doc, "Move to layer"):
        for obj, owner in units(doc).items():
            if owner in selected:
                _assign(obj, layer)
    return True


def delete(doc, layer):
    if layer == BASE:
        raise ValueError("Base cannot be deleted.")
    data = state(doc)
    _row(data, layer)
    with transaction(doc, "Delete layer"):
        # Assignments are metadata only. No removeObject or group edits occur.
        for obj in doc.Objects:
            if getattr(obj, PROPERTY, None) == layer:
                _assign(obj, BASE)
        data["layers"] = [row for row in data["layers"] if row["id"] != layer]
        if data["active"] == layer:
            data["active"] = BASE
        _store(doc, data)


class _Observer:
    def slotCreatedObject(self, obj):
        if _busy or obj.Document.Restoring or not eligible(obj):
            return
        initialize(obj.Document, new=True)

    def slotChangedObject(self, obj, prop):
        if not _busy and not obj.Document.Restoring and prop in (
                "Group", "OriginFeatures", "Producer", "ConsumedResults", "ComponentRole"):
            initialize(obj.Document)

    def slotBeforeCloseTransaction(self, abort):
        if not abort and not _busy:
            for doc in App.listDocuments().values():
                if doc.HasPendingTransaction:
                    initialize(doc)

    def slotStartSaveDocument(self, doc, filename):
        initialize(doc)


_observer = _Observer()


def install():
    global _installed
    if not _installed:
        App.addDocumentObserver(_observer)
        _installed = True
