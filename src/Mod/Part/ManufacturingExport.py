# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit solid-to-STL handoff using the existing world-shape and mesh services."""
import json
import math
import os
from pathlib import Path
import shutil
import tempfile

import FreeCAD as App
from BasicShapes.ShapeReferences import linked_shape, require_current


DEFAULTS = {"Coarse": (0.5, 30.0), "Normal": (0.1, 15.0), "Fine": (0.02, 5.0)}
PREFS = "User parameter:BaseApp/Preferences/Mod/Part/ManufacturingExport"


def quality(linear, angular):
    linear, angular = float(linear), float(angular)
    if not math.isfinite(linear) or not 0.001 <= linear <= 10:
        raise ValueError("Linear deflection must be between 0.001 and 10 mm.")
    if not math.isfinite(angular) or not 1 <= angular <= 90:
        raise ValueError("Angular deflection must be between 1 and 90 degrees.")
    return linear, angular


def presets():
    result = dict(DEFAULTS)
    raw = App.ParamGet(PREFS).GetString("Presets", "{}")
    try:
        saved = json.loads(raw)
        for name, values in saved.items():
            if isinstance(name, str) and name and name not in DEFAULTS and len(values) == 2:
                result[name] = quality(*values)
    except (ValueError, TypeError, AttributeError):
        raise ValueError("Saved export presets are invalid. Use Reset presets to restore defaults.")
    return result


def save_preset(name, linear, angular):
    name = name.strip()
    if not name or len(name) > 80 or name in DEFAULTS:
        raise ValueError("Use a custom preset name of 1-80 characters; built-in names are reserved.")
    values = quality(linear, angular)
    saved = {key: value for key, value in presets().items() if key not in DEFAULTS}
    saved[name] = values
    App.ParamGet(PREFS).SetString("Presets", json.dumps(saved, sort_keys=True))


def reset_presets():
    App.ParamGet(PREFS).RemString("Presets")


def collect_shapes(objects):
    if not objects:
        raise ValueError("Select one or more whole solid objects or occurrences.")
    doc = objects[0].Document
    if doc.HasPendingTransaction:
        raise ValueError("Finish the pending edit transaction before exporting.")
    unique, result = set(), []
    for obj in objects:
        if obj.Document != doc:
            raise ValueError("Choose objects from one document.")
        if obj.Name in unique:
            continue
        unique.add(obj.Name)
        target = obj.getLinkedObject() if obj.isDerivedFrom("App::Link") else obj
        if not target.isDerivedFrom("Part::Feature"):
            raise ValueError("Select individual solids or Body results, not containers, sketches or meshes.")
        require_current(obj)
        parent = obj.getParentGeoFeatureGroup()
        while parent:
            require_current(parent)
            parent = parent.getParentGeoFeatureGroup()
        shape = linked_shape((obj, []))
        # The inherited resolver can extract solids from a mixed compound.
        # Check the source too, so loose geometry is disclosed before that reduction.
        pending = [target.Shape, shape]
        solid_only = True
        while pending:
            member = pending.pop()
            if member.ShapeType == "Compound":
                pending.extend(member.childShapes())
            elif member.ShapeType not in ("Solid", "CompSolid"):
                solid_only = False
                break
        if (shape.isNull() or not shape.isValid() or not shape.Solids
                or not solid_only
                or sum(len(solid.Faces) for solid in shape.Solids) != len(shape.Faces)):
            raise ValueError("{} is not a valid solid-only result.".format(obj.Label))
        result.append((obj, shape))
    return result


def export_stl(objects, filename, linear=0.1, angular=15.0, overwrite=False):
    """Export current recomputed geometry; STL coordinates are millimeters in world space."""
    import Mesh
    import MeshPart

    linear, angular = quality(linear, angular)
    path = Path(filename).expanduser()
    if path.suffix.lower() != ".stl":
        raise ValueError("Choose an output filename ending in .stl.")
    if not path.parent.is_dir():
        raise ValueError("The output folder does not exist.")
    if path.exists() and not overwrite:
        raise FileExistsError("The output already exists; choose another name or confirm replacement.")
    shapes = collect_shapes(objects)
    mesh = Mesh.Mesh()
    for obj, shape in shapes:
        item = MeshPart.meshFromShape(Shape=shape, LinearDeflection=linear,
                                     AngularDeflection=math.radians(angular), Relative=False)
        if item.CountFacets == 0 or not item.isSolid():
            raise ValueError("{} did not produce a closed mesh.".format(obj.Label))
        mesh.addMesh(item)
    if not mesh.isSolid():
        raise ValueError("The combined mesh is not closed. Export touching objects separately.")
    bounds = mesh.BoundBox
    report = {"file": str(path.resolve()), "format": "STL", "units": "mm",
              "frame": "World", "linear_mm": linear, "angular_deg": angular,
              "objects": [obj.Name for obj, _ in shapes], "facets": mesh.CountFacets,
              "size_mm": [bounds.XLength, bounds.YLength, bounds.ZLength],
              "losses": "Triangulated geometry only: no feature history, units metadata, colors or assembly identity."}
    handle, temporary = tempfile.mkstemp(prefix=".freecad-export-", suffix=".stl", dir=path.parent)
    os.close(handle)
    try:
        mesh.write(temporary)
        if overwrite:
            os.replace(temporary, path)
        else:
            # Exclusive creation protects a file that appeared after preflight.
            with path.open("xb") as output:
                try:
                    with open(temporary, "rb") as source:
                        shutil.copyfileobj(source, output)
                except BaseException:
                    output.close()
                    path.unlink()
                    raise
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return report
