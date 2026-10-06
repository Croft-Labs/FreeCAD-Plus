# SPDX-License-Identifier: LGPL-2.1-or-later
"""Read-only legacy inventory. Plans are evidence, never conversion commands."""
import hashlib
from pathlib import Path


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
