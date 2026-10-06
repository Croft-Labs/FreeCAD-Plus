# SPDX-License-Identifier: LGPL-2.1-or-later
"""Legacy inventory, structural migration and explicit evaluated recovery."""
import hashlib
from pathlib import Path

import FreeCAD as App


def _key(obj):
    return obj.Document.Name + ":" + obj.Name


def _references(value):
    if hasattr(value, "Document") and hasattr(value, "Name"):
        return [value]
    if isinstance(value, (tuple, list)):
        return [obj for item in value for obj in _references(item)]
    return []


def _frame(placement):
    return list(placement.toMatrix().A)


def _own_identity(obj):
    # App::Link forwards target properties. A definition UUID must never be
    # mistaken for an occurrence's own UUID.
    try:
        return obj.getPropertyByName("ObjectId", 1) is not None
    except AttributeError:
        return False


class BodyOutputProxy:
    """Native Body Tip bridge; the editable producer lives in component History."""

    def execute(self, obj):
        import Part
        obj.Shape = Part.Shape()
        producer = obj.Producer
        if producer is not None and "Invalid" not in producer.State:
            obj.Placement = producer.Shape.Placement
            obj.Shape = producer.Shape.copy()

    def dumps(self):
        return None

    def loads(self, state):
        pass


def body_history_plan(body, component, source_ready):
    """Admit only the proven independent Sketch -> first Pad pilot."""
    import ComponentModel as Model
    if not body.Placement.isSame(App.Placement(), 1e-9):
        return None, "Body frame mapping awaits the attachment/frame adapter"
    pad = body.Tip
    if pad is None or pad.TypeId != "PartDesign::Pad":
        return None, "native Tip feature family awaits its adapter"
    sketch = pad.Profile[0]
    if sketch is None or not sketch.isDerivedFrom("Sketcher::SketchObject"):
        return None, "Pad profile is not an independent sketch"
    if set(body.Group) not in ({sketch, pad}, {pad}) or pad.BaseFeature is not None:
        return None, "multi-feature native Body history awaits its adapters"
    if Model.owner(sketch) not in (body, component):
        return None, "profile belongs to another native owner"
    if (str(sketch.MapMode) != "Deactivated" or sketch.AttachmentSupport
            or sketch.ExternalGeometry or pad.Profile[1]):
        return None, "attached/external/subelement sketch inputs await their adapter"
    if (str(pad.Type) != "Length" or str(pad.SideType) != "One side"
            or pad.UseCustomVector or float(pad.TaperAngle) != 0
            or str(pad.StartType) != "Profile plane"):
        return None, "Pad extent semantics await the full extrusion adapter"
    if any(obj.ExpressionEngine for obj in (body, sketch)):
        return None, "frame/sketch expressions await dependency-aware migration"
    if not source_ready or any("Invalid" in obj.State for obj in (body, pad, sketch)):
        return None, "native history needs recompute or repair; cached output is unverified"
    if body.Shape.isNull() or not body.Shape.isValid() or len(body.Shape.Solids) != 1:
        return None, "native output needs repair; no solid output is fabricated"
    return (sketch, pad), ""


def migrate_body_histories(document, report, readiness):
    """Flatten proven histories, retaining other native histories and final outputs.

    Called inside the structural transaction; no new document or feature identities
    replace legacy objects. Body's native child-scoped Tip uses an internal bridge.
    """
    import ComponentModel as Model
    for component in Model.definitions(document):
        bodies = [obj for obj in Model.history(component) if obj.TypeId == "PartDesign::Body"]
        for body in bodies:
            plan, reason = body_history_plan(body, component, readiness.get(body, False))
            if plan is None:
                Model._property(body, "String", "LegacyHistoryState", "Retained native: " + reason, True)
                report.append(body.Label + ": editable native Body history and available final output retained; " + reason + ".")
                continue
            sketch, pad = plan
            before = body.Shape.copy()
            names = list(component.ModelHistory)
            original_group = [obj.Name for obj in body.Group]
            for obj, role in ((sketch, "Object"), (pad, "Operation")):
                if Model.owner(obj) == body:
                    body.removeObject(obj)
                Model.register_object(component, obj, role)
            Model._property(pad, "String", "OperationKind", "Extrude", True)
            Model._property(pad, "String", "ExtrudeMode", "New Body", True)
            Model._property(pad, "String", "LegacyMigration", "Sketch-Pad pilot", True)
            bridge = body.newObject("PartDesign::FeaturePython", "LegacyBodyOutput")
            Model._identity(bridge, "Internal")
            Model._property(bridge, "LinkGlobal", "Producer", pad, True)
            bridge.Proxy = BodyOutputProxy()
            bridge.Label = body.Label + " native output bridge"
            body.Tip = bridge
            # Explicit migration of the existing semantic role, never replacement
            # of the native Body name/type/ObjectId or its downstream references.
            body.ComponentRole = "Result"
            Model._property(body, "Link", "Producer", pad, True)
            Model._property(body, "Bool", "Frozen", False, True)
            Model._property(body, "String", "GeometryKind", "Body", True)
            Model._property(body, "String", "OutputProperty", "Shape", True)
            Model._property(body, "Bool", "BackgroundResult", False, True)
            Model._property(body, "StringList", "LegacyBodyHistory", original_group, True)
            Model._property(body, "Link", "LegacyTip", pad, True)
            Model._property(body, "String", "LegacyHistoryState", "Mapped Sketch-Pad pilot", True)
            ordered = []
            for name in names:
                if name in (sketch.Name, pad.Name):
                    continue
                ordered.extend([sketch.Name, pad.Name, body.Name] if name == body.Name else [name])
            component.ModelHistory = ordered
            component.ResultObjects = [name for name in component.ResultObjects
                                       if name not in (sketch.Name, pad.Name)]
            if App.GuiUp:
                bridge.Visibility = sketch.Visibility = pad.Visibility = False
                bridge.ViewObject.ShowInTree = False
            document.recompute()
            if "Invalid" in body.State or body.Shape.isNull() or not body.Shape.isValid():
                raise ValueError("Migrated native Body output failed; retain payloads through evaluated recovery.")
            if (abs(before.Volume - body.Shape.Volume) > 1e-8
                    or before.cut(body.Shape).Volume > 1e-8
                    or body.Shape.cut(before).Volume > 1e-8):
                raise ValueError("Migrated Body geometry changed; retain native payloads through evaluated recovery.")
            report.append(body.Label + ": Sketch and Pad precede the original Body result in component History; editable native identities retained.")


def recovery_shapes(document):
    """Capture native top-level output before structural edits, for recovery."""
    import Part
    result, hidden = [], []
    for obj in document.Objects:
        if obj.TypeId == "App::Origin" or obj.getParentGeoFeatureGroup() is not None:
            continue
        if not (obj.TypeId == "App::Part" or obj.isDerivedFrom("Part::Feature")
                or obj.isDerivedFrom("App::Link")):
            continue
        try:
            shape = Part.getShape(obj, "", needSubElement=False).copy()
            if not shape.isNull() and shape.isValid():
                bucket = hidden if App.GuiUp and not obj.ViewObject.Visibility else result
                stale = any(flag in ("Touched", "Invalid")
                            for dep in [obj] + list(obj.OutListRecursive) for flag in dep.State)
                bucket.append((obj.Name, shape, stale))
        except (RuntimeError, ValueError):
            pass  # Conversion report below explicitly identifies unavailable output.
    return result or hidden


def recover_structure(document, shapes, error):
    """Retain native payloads and present validated frozen outputs on failure."""
    import ComponentModel as Model
    filename = document.FileName
    originals = list(document.Objects)
    with Model.transaction(document, "Recover legacy evaluated component outputs"):
        meta = Model.initialize(document, document.Label)
        meta.LegacySource = filename
        report = ["Structural adapter could not complete: " + str(error),
                  "Explicit dumb geometry recovery; native feature payloads retained. Parametric component migration is incomplete."]
        for name, shape, stale in shapes:
            obj = document.addObject("Part::Feature", "RecoveredLegacyOutput")
            obj.Label = name + " recovered geometry"
            obj.Shape = shape
            Model.register_object(meta.RootComponent, obj, "Object", True)
            Model._property(obj, "String", "LegacyRecovery", name + ": validated evaluated geometry; parametric history not converted.", True)
            if stale:
                obj.LegacyRecovery = name + ": unverified cached geometry; source requires repair; parametric history not converted."
                report.append(name + ": recovered cached geometry is unverified; original source dependencies require repair.")
        if not shapes:
            report.append("No valid top-level evaluated output was available; native payloads retained for repair.")
        for obj in originals:
            if App.GuiUp:
                obj.ViewObject.Visibility = False
        meta.ConversionReport = report
    document.FileName = ""
    return document


def inventory(document):
    """Snapshot an already-open legacy document without recompute or mutation.

    Keys use native document/object names; no UUIDs are assigned. External
    documents are identified, not opened, saved or converted. Geometry is the
    existing evaluated cache: availability is separate from trusted freshness.
    """
    if any(getattr(o, "ComponentRole", "") == "Document" for o in document.Objects):
        raise ValueError("Inventory the legacy document before component conversion.")
    objects = list(document.Objects)
    local = {_key(o): o for o in objects}
    issues, records, dependencies, native_dependencies = [], {}, {}, {}

    def issue(obj, stage, error):
        issues.append({"object": _key(obj), "stage": stage, "message": str(error)})

    for obj in objects:
        key = _key(obj)
        record = {"name": obj.Name, "label": obj.Label, "type": obj.TypeId,
                  "object_id": getattr(obj, "ObjectId", None), "state": list(obj.State),
                  "properties": {}, "links": {}, "geometry": None,
                  "fallback": {"kind": None, "status": "unavailable"}}
        records[key] = record
        for prop in obj.PropertiesList:
            try:
                kind = obj.getTypeIdOfProperty(prop)
                if prop not in ("Shape", "Proxy"):
                    data = bytes(obj.dumpPropertyContent(prop, 0))
                    record["properties"][prop] = {"type": kind,
                        "sha256": hashlib.sha256(data).hexdigest()}
                if "Link" in kind:
                    record["links"][prop] = [_key(o) for o in _references(getattr(obj, prop))]
            except Exception as error:
                issue(obj, "property:" + prop, error)
        try:
            parent = obj.getParentGeoFeatureGroup()
            record["owner"] = _key(parent) if parent else None
            record["group"] = [_key(o) for o in getattr(obj, "Group", [])]
            record["tip"] = _key(obj.Tip) if getattr(obj, "Tip", None) else None
            if hasattr(obj, "Placement"):
                record["placement"] = _frame(obj.Placement)
                record["world_placement"] = (_frame(obj.getGlobalPlacement())
                    if hasattr(obj, "getGlobalPlacement") else None)
            if hasattr(obj, "LinkPlacement"):
                record["link_placement"] = _frame(obj.LinkPlacement)
                record["link_transform"] = bool(obj.LinkTransform)
                record["link_scale"] = float(obj.Scale)
                record["link_scale_vector"] = list(obj.ScaleVector)
                record["element_count"] = int(obj.ElementCount)
            record["expressions"] = [list(x) for x in getattr(obj, "ExpressionEngine", [])]
            record["visibility"] = bool(obj.Visibility) if hasattr(obj, "Visibility") else None
        except Exception as error:
            issue(obj, "ownership/frame", error)
        try:
            # The synthetic .Shape accessor on Parts/Links can create caches,
            # and native feature access can lazily evaluate touched geometry.
            # Read only the stored property; never invoke that accessor.
            shape = obj.getPropertyByName("Shape") if "Shape" in obj.PropertiesList else None
            if shape is not None and not shape.isNull():
                brep = shape.exportBrepToString()
                valid = shape.isValid()
                record["geometry"] = {"brep_sha256": hashlib.sha256(brep.encode()).hexdigest(),
                    "valid": valid, "solids": len(shape.Solids), "faces": len(shape.Faces),
                    "edges": len(shape.Edges), "vertices": len(shape.Vertexes),
                    "volume": shape.Volume, "area": shape.Area,
                    "bounds": [shape.BoundBox.XMin, shape.BoundBox.YMin, shape.BoundBox.ZMin,
                               shape.BoundBox.XMax, shape.BoundBox.YMax, shape.BoundBox.ZMax]}
                kind = ("dumb_body" if shape.Solids else "dumb_sheet" if shape.Faces
                        else "dumb_curve" if shape.Edges else "dumb_point")
                stale = any(s in ("Touched", "Invalid") for s in obj.State)
                record["fallback"] = {"kind": kind, "status": "invalid" if not valid
                    else "cached_unverified" if stale else "available_cached",
                    "source": key, "preserves_parametrics": False}
        except Exception as error:
            issue(obj, "geometry", error)
        # Ownership links must not turn every Body/Part into a false cycle.
        inputs = {dep for prop, values in record["links"].items()
                  if prop not in ("Group", "Origin", "OriginFeatures", "_Body") for dep in values}
        # OutList includes expression dependencies, including cross-document ones.
        structural = set(record.get("group", []))
        for prop in ("Origin", "OriginFeatures", "_Body"):
            structural.update(record["links"].get(prop, []))
        try:
            native_dependencies[key] = list(obj.OutList)
            inputs.update(_key(o) for o in native_dependencies[key] if _key(o) not in structural)
        except Exception as error:
            native_dependencies[key] = []
            issue(obj, "dependencies", error)
        dependencies[key] = sorted(inputs)

    # Deterministic Kahn order; unresolved nodes are blocked, never silently sorted.
    remaining = {k: set(v) & local.keys() for k, v in dependencies.items()}
    order = []
    while remaining:
        ready = sorted(k for k, v in remaining.items() if not v)
        if not ready:
            break
        order.extend(ready)
        for key in ready:
            del remaining[key]
        for values in remaining.values():
            values.difference_update(ready)
    for key in remaining:
        issues.append({"object": key, "stage": "dependency_order",
                       "message": "Cyclic dependency or dependent on a cycle; conversion blocked."})

    parts = {k for k, o in local.items() if o.TypeId == "App::Part"}
    bodies = {k for k, o in local.items() if o.TypeId == "PartDesign::Body"}

    def enclosing_part(key):
        seen = set()
        while key in records and key not in seen:
            seen.add(key)
            key = records[key].get("owner")
            if key in parts:
                return key
        return None

    boundaries = parts | {k for k in bodies if enclosing_part(k) is None}
    links = {k for k, o in local.items() if o.isDerivedFrom("App::Link")}
    for key in links:
        targets = records[key]["links"].get("LinkedObject", [])
        for target in targets:
            if target in local and target not in links and not records[target].get("owner"):
                boundaries.add(target)
            elif target in local and target not in boundaries and target not in links:
                issues.append({"object": key, "stage": "definition_boundary",
                    "message": "Link targets an internal feature; retain native link until ownership is resolved."})
        if not targets:
            issues.append({"object": key, "stage": "definition_boundary",
                           "message": "Unresolved native link; no target geometry is certified."})

    master = document.Name + ":@master"

    def definition_for(key):
        seen = set()
        while key in records and key not in seen:
            seen.add(key)
            if key in boundaries:
                return key
            key = records[key].get("owner")
        return master

    definitions = [{"source": k, "parent": definition_for(records[k].get("owner")),
                    "policy": "preserve_native_definition_identity"} for k in sorted(boundaries)]
    occurrences = [{"source": k, "definition": k, "parent": d["parent"],
                    "policy": "proposed_instance_from_container_placement"}
                   for d in definitions for k in [d["source"]] if k not in links]
    occurrences.extend({"source": k, "targets": records[k]["links"].get("LinkedObject", []),
                        "parent": definition_for(records[k].get("owner")),
                        "policy": "preserve_native_link_and_placement"} for k in sorted(links))
    external = sorted({dep for deps in dependencies.values() for dep in deps if dep not in local})
    external_files = {}
    for key, deps in native_dependencies.items():
        for dep in deps:
            if _key(dep) in external:
                try:
                    external_files[_key(dep)] = dep.Document.FileName
                except Exception as error:
                    issue(local[key], "external_file", error)
    # Freshness of dependent geometry is not established by its own State alone.
    stale = {k for k, r in records.items() if any(s in ("Touched", "Invalid") for s in r["state"])}
    stale.update(_key(dep) for deps in native_dependencies.values() for dep in deps
                 if any(s in ("Touched", "Invalid") for s in dep.State))
    while True:
        downstream = {k for k, deps in dependencies.items() if stale.intersection(deps)}
        if downstream <= stale:
            break
        stale.update(downstream)
    for key in stale | set(remaining):
        if key in records and records[key]["fallback"]["status"] == "available_cached":
            records[key]["fallback"]["status"] = "cached_unverified"
    source = Path(document.FileName) if document.FileName else None
    source_hash = None
    try:
        if source and source.is_file():
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    except OSError as error:
        issues.append({"object": None, "stage": "source_file", "message": str(error)})
    return {"plan_version": 1, "read_only": True, "document": document.Name,
            "source_file": str(source) if source else None,
            "source_sha256": source_hash,
            "master": master, "objects": records, "dependencies": dependencies,
            "dependency_order": order, "blocked_objects": sorted(remaining),
            "definitions": definitions, "occurrences": occurrences,
            "history_owner": {k: definition_for(k) for k in records if k not in links},
            "external_objects": external, "external_files": external_files,
            "issues": issues,
            "recovery_policy": ["convert_with_feature_adapter", "retain_editable_native_feature",
                                "recover_valid_evaluated_dumb_geometry", "report_unavailable_output"],
            "fallback_requires": "Explicit loss-of-parametrics report; validate cached geometry and placements. Never replace failed features during inventory."}


def convert_structure(document, extra_targets=(), visiting=None):
    """Convert definition/occurrence ownership, retaining native feature payloads.

    Each file is one native transaction. External dependencies convert in memory
    first; saving them to new cadprt files remains an explicit owner action.
    """
    import ComponentModel as Model
    if any(getattr(o, "ComponentRole", "") == "Document" for o in document.Objects):
        return document
    visiting = set() if visiting is None else visiting
    if document.Name in visiting:
        raise ValueError("Cyclic legacy external files cannot be mapped to component instances.")
    visiting.add(document.Name)
    try:
        plan = inventory(document)
        originals = list(document.Objects)
        links = [o for o in originals if o.isDerivedFrom("App::Link")]
        # Keep a native target/frame snapshot before any source is reparented.
        snapshots = {}
        external = {}
        arrays = {}
        for link in links:
            target = link.LinkedObject
            if target is None:
                continue
            if link.ElementCount:
                import Part
                shape = Part.getShape(link, "", needSubElement=False).copy()
                if shape.isNull() or not shape.isValid() or "Invalid" in link.State:
                    raise ValueError("Legacy link array has no validated recoverable output.")
                arrays[link] = shape
                continue
            snapshots[link] = (target, App.Placement(link.LinkPlacement), bool(link.LinkTransform),
                               App.Placement(target.Placement) if hasattr(target, "Placement") else App.Placement())
            if target.Document != document:
                external.setdefault(target.Document, []).append(target)
        for source, targets in external.items():
            convert_structure(source, targets, visiting)

        parts = [o for o in originals if o.TypeId == "App::Part"]
        boundaries = {document.getObject(d["source"].split(":", 1)[1]) for d in plan["definitions"]}
        boundaries.update(extra_targets)
        boundaries.update(arrays)
        boundaries.update(target for target, _, _, _ in snapshots.values() if target.Document == document)
        boundaries.discard(None)
        # Definition frames are captured in the old ownership hierarchy.
        world = {o: App.Placement(o.getGlobalPlacement()) for o in parts}
        for part in parts:
            if any(prop.lstrip(".").startswith("Placement") for prop, _ in part.ExpressionEngine):
                raise ValueError("Expression-driven Part frames require explicit frame-expression mapping; native source is retained.")
            if not part.Placement.isSame(world[part], 1e-9):
                names = (part.Name + ".Placement", "<<" + part.Label + ">>.Placement")
                if any(any(name in expression for name in names)
                       for obj in originals for _, expression in getattr(obj, "ExpressionEngine", [])):
                    raise ValueError("An expression consumes the legacy local Part frame; preserve native formulas through explicit evaluated recovery.")
        parents = {o: Model.owner(o) for o in originals}
        readiness = {o: not any(flag in ("Invalid", "Touched")
                               for dep in [o] + Model.geometry_dependencies(o) for flag in dep.State)
                     for o in originals if o.TypeId == "PartDesign::Body"}
        local_frames = {o: App.Placement(o.Placement) for o in parts}
        labels = {o: o.Label for o in originals}
        old_filename = document.FileName
        mapping, report = {}, []

        def annotate_definition(obj):
            if _own_identity(obj):
                Model._property(obj, "String", "ComponentRole", "Definition", True)
            else:
                Model._identity(obj, "Definition")
            Model._property(obj, "StringList", "ModelHistory", [], True)
            Model._property(obj, "StringList", "ResultObjects", [], True)
            Model._property(obj, "String", "RepresentationOverrides", "{}", True)

        def register(component, obj, role, result=False):
            target = obj.LinkedObject if obj.isDerivedFrom("App::Link") else None
            if target is not None:
                obj.setLink(None)
            if _own_identity(obj) and not hasattr(obj, "ComponentRole"):
                Model._property(obj, "String", "ComponentRole", role, True)
            elif not _own_identity(obj):
                Model._identity(obj, role)
            if target is not None:
                obj.setLink(target)
            # Native addObject expands local-scope dependencies. Legacy consumers
            # may already cross Parts; do not steal their source Body/feature into
            # the consumer's new definition. Set explicit membership instead.
            if Model.owner(obj) is None:
                component.Group = list(component.Group) + [obj]
            Model.register_object(component, obj, role, result)
            if obj in labels:
                obj.Label = labels[obj]

        def occurrence(parent, link, definition):
            parent.addObject(link)
            placement = App.Placement(link.LinkPlacement)
            transform, scale, vector = link.LinkTransform, link.Scale, App.Vector(link.ScaleVector)
            link.setLink(None)
            if _own_identity(link):
                Model._property(link, "String", "ComponentRole", "Occurrence", True)
            else:
                Model._identity(link, "Occurrence")
            link.setLink(definition)
            link.LinkTransform = transform
            link.LinkPlacement = placement
            link.Scale = scale
            link.ScaleVector = vector
            Model._property(link, "String", "DefinitionId", definition.ObjectId if definition else "legacy-unresolved:" + link.Name, True)
            Model._property(link, "Integer", "InstanceNumber", sum(c.LinkedObject == definition for c in Model.children(parent)), True)
            Model._property(link, "Enumeration", "Representation", list(Model.TYPES))
            link.Representation = "Bodies Only"
            Model._property(link, "Bool", "IncludeInBOM", True)
            Model._property(link, "Bool", "IncludeInMass", True)

        with Model.transaction(document, "Convert legacy component structure"):
            meta = Model.initialize(document, document.Label)
            root = meta.RootComponent
            meta.LegacySource = old_filename
            for part in parts:
                annotate_definition(part)
                mapping[part] = part
            for obj in sorted(boundaries - set(parts), key=lambda x: x.Name):
                definition = Model._definition(document, labels[obj])
                Model._property(definition, "Link", "LegacyDefinitionSource", obj, True)
                mapping[obj] = definition
                if obj in arrays:
                    if not _own_identity(obj):
                        Model._identity(obj, "LegacyPayload")
                    for element in obj.ElementList:
                        if element.TypeId == "App::LinkElement":
                            Model._identity(element, "LegacyPayload")
                    frozen = document.addObject("Part::Feature", "RecoveredArray")
                    frozen.Shape = arrays[obj]
                    frozen.Label = obj.Label + " recovered geometry"
                    register(definition, frozen, "Object", True)
                    Model._property(frozen, "String", "LegacyRecovery", "Dumb evaluated array; native array retained; parametric instance mapping pending.", True)
                    if parents[obj]:
                        parents[obj].removeObject(obj)
                    if App.GuiUp:
                        obj.Visibility = False
                    report.append(obj.Label + ": recovered as explicit dumb array geometry; native array identity retained outside component History.")
                elif parents[obj] is None and not obj.isDerivedFrom("App::Link"):
                    register(definition, obj, "Object" if obj.TypeId == "Part::Feature"
                             or obj.isDerivedFrom("Sketcher::SketchObject") else "Operation")
                else:
                    # Internal features keep their native Body/Part ownership.
                    helper = document.addObject("App::Link", "LegacyGeometry")
                    helper.setLink(obj)
                    helper.LinkTransform = True
                    register(definition, helper, "Object", True)
                    report.append(obj.Label + ": native feature ownership retained through a geometry link.")
            for part in parts:
                if parents[part]:
                    parents[part].removeObject(part)
                part.Placement = world[part]

            def component_for(parent):
                while parent is not None:
                    if parent in mapping:
                        return mapping[parent]
                    parent = parents.get(parent)
                return root

            for source, definition in mapping.items():
                # A real legacy container is also a placed use. Additional
                # native Links remain additional uses of the same definition.
                if source in parts or source in arrays or parents[source] is None:
                    parent = component_for(parents[source])
                    link = document.addObject("App::Link", "ComponentInstance")
                    link.setLink(definition)
                    link.LinkTransform = False
                    link.LinkPlacement = local_frames[source] if source in parts else App.Placement()
                    link.Label = labels[source]
                    occurrence(parent, link, definition)
            for link, (target, placement, transform, old_target_frame) in snapshots.items():
                if target.Document == document:
                    definition = mapping[target]
                elif Model.is_component(target):
                    definition = target
                else:
                    candidates = [d for d in Model.definitions(target.Document)
                                  if getattr(d, "LegacyDefinitionSource", None) == target]
                    if len(candidates) != 1:
                        raise ValueError("External legacy target has no unique converted definition.")
                    definition = candidates[0]
                parent = component_for(parents[link])
                if parents[link]:
                    parents[link].removeObject(link)
                # A native Part is now in its original world frame. A wrapper
                # retains its source's local frame. Compensate, never normalize
                # silently or change shared source geometry.
                if target in parts or (target.Document != document and Model.is_component(target)):
                    if transform:
                        delta = old_target_frame.multiply(definition.Placement.inverse())
                    else:
                        delta = App.Placement()
                elif not transform:
                    delta = old_target_frame.inverse()
                else:
                    delta = App.Placement()
                scale = App.Matrix()
                vector = App.Vector(link.ScaleVector)
                if link.Scale != 1:
                    vector = App.Vector(link.Scale, link.Scale, link.Scale)
                scale.A11, scale.A22, scale.A33 = vector.x, vector.y, vector.z
                matrix = placement.toMatrix().multiply(scale).multiply(delta.toMatrix()).multiply(scale.inverse())
                placement = App.Placement(matrix)
                if max(abs(a - b) for a, b in zip(matrix.A, placement.toMatrix().A)) > 1e-9:
                    raise ValueError("Nonuniform scaled frame compensation requires affine recovery; native payload is retained.")
                link.setLink(definition)
                link.LinkTransform = transform
                link.LinkPlacement = placement
                link.Label = labels[link]
                occurrence(parent, link, definition)

            for link in links:
                if link in arrays or link in snapshots:
                    continue
                parent = component_for(parents[link])
                if parents[link]:
                    parents[link].removeObject(link)
                occurrence(parent, link, None)
                report.append(link.Label + ": unresolved native target retained as a missing Part Tree instance; repair required before saving.")

            for obj in originals:
                if obj in parts or obj in links or hasattr(obj, "ComponentRole"):
                    continue
                owner = Model.owner(obj)
                if obj.TypeId == "App::Origin" or any(obj in p.Origin.OriginFeatures for p in parts):
                    continue
                if owner is None or Model.is_component(owner):
                    component = owner or root
                    if "Shape" in obj.PropertiesList:
                        register(component, obj, "Object" if obj.TypeId == "Part::Feature"
                                 or obj.isDerivedFrom("Sketcher::SketchObject") else "Operation")
            for definition in Model.definitions(document):
                for obj in Model.history(definition):
                    if "Shape" not in obj.PropertiesList:
                        continue
                    shape = obj.getPropertyByName("Shape")
                    if shape.isNull() or not shape.isValid():
                        report.append(obj.Label + ": native payload retained; evaluated output needs repair.")
                    else:
                        # Structural migration must not duplicate the source
                        # shape in a native Part compound. Task three owns the
                        # operation/result-layer migration; use the retained
                        # editable native output directly in this milestone.
                        definition.ResultObjects = list(definition.ResultObjects) + [obj.Name]
                    if obj.TypeId == "PartDesign::Body":
                        report.append(obj.Label + ": native Body Tip and sketch/feature history retained; feature adapters pending.")
            migrate_body_histories(document, report, readiness)
            meta.ConversionReport = report + ["Models and linked Part Tree instances converted; native features retained.",
                "Recovery policy: retained editable native features before explicit validated dumb geometry; no fallback created in this structural step."]
            if external:
                meta.ConversionReport = list(meta.ConversionReport) + ["Save converted external files as new .cadprt files before saving this parent; legacy originals remain protected."]
            Model.validate(document, allow_unresolved=True)
        # Native external-link relocation needs an owner-file reference base
        # while dependencies are saved first. The manifest's LegacySource guard
        # prohibits writing this legacy path; Save As must choose a new cadprt.
        document.FileName = old_filename if external or extra_targets else ""
        return document
    finally:
        visiting.remove(document.Name)
