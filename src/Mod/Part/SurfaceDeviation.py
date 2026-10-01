# SPDX-License-Identifier: LGPL-2.1-or-later
"""Read-only, one-way face sampling using native OCCT point-to-face distances."""
import math
import re

import FreeCAD as App
import Part
from BasicShapes.ShapeReferences import require_current


class FaceReference:
    """An explicit face snapshot. Changed topology requires deliberate recapture."""
    def __init__(self, obj, sub):
        if (not obj.isDerivedFrom("Part::Feature")
                or obj.getParentGeoFeatureGroup() is not None):
            raise ValueError("Select a face on a root Part shape or whole root Body; Links and nested members are not supported.")
        require_current(obj)
        if not sub and obj.Shape.ShapeType == "Face":
            sub = "Face1"
        if not re.fullmatch(r"Face[1-9][0-9]*", sub):
            raise ValueError("Select exactly one face for this role.")
        shape = obj.Shape
        if shape.isNull() or not shape.isValid():
            raise ValueError("Repair the invalid source shape first.")
        face = shape.getElement(sub)
        if face.ShapeType != "Face" or face.Area <= 0:
            raise ValueError("Select a nonempty face.")
        self.key = (obj.Document.Name, obj.Name, obj.ID, sub)
        self.label = "{} ({}.{})".format(obj.Label, obj.Name, sub)
        self._snapshot = shape.exportBrepToString()

    def face(self):
        doc = App.listDocuments().get(self.key[0])
        obj = doc.getObject(self.key[1]) if doc else None
        if obj is None or obj.ID != self.key[2]:
            raise ValueError("An input was removed. Capture both face roles again.")
        require_current(obj)
        if (obj.getParentGeoFeatureGroup() is not None
                or obj.Shape.exportBrepToString() != self._snapshot):
            raise ValueError("Input geometry or placement changed. Capture the affected face again.")
        return obj.Shape.getElement(self.key[3]).copy()


def settings(grid, scale):
    if isinstance(grid, bool) or int(grid) != grid or not 3 <= grid <= 25:
        raise ValueError("Choose 3-25 samples per UV direction.")
    scale = float(scale)
    if not math.isfinite(scale) or not 1e-6 <= scale <= 1e6:
        raise ValueError("Choose a color scale from 0.000001 to 1000000 mm.")
    return int(grid), scale


def color(distance, scale):
    """Blue at zero, yellow at half scale, red at/above full scale."""
    ratio = max(0., min(1., distance / scale))
    return (2 * ratio, 2 * ratio, 1 - 2 * ratio) if ratio <= .5 else (1., 2 - 2 * ratio, 0.)


def inspect(sampled, reference, grid=11, scale=1.):
    """Grid cell centers in UV; trimmed-out and unresolved points are reported.

    Distances are unsigned nearest distances to the finite reference face, including
    its boundary. Statistics are over samples only, not area weighted or certified
    extrema. There is no alignment, normal projection, or reverse-direction pass.
    """
    grid, scale = settings(grid, scale)
    if sampled.key[0] != reference.key[0] or sampled.key == reference.key:
        raise ValueError("Choose two distinct faces from the same document.")
    doc = App.listDocuments().get(sampled.key[0])
    if doc is None or doc.HasPendingTransaction or App.getActiveTransaction():
        raise ValueError("Finish the pending edit transaction before checking.")
    source, target = sampled.face(), reference.face()
    u0, u1, v0, v1 = source.ParameterRange
    if not all(math.isfinite(x) for x in (u0, u1, v0, v1)) or u1 <= u0 or v1 <= v0:
        raise ValueError("This face has no finite, nonempty UV sampling domain.")
    report = {"points": [], "distances": [], "colors": [], "outside": 0,
              "unresolved": 0, "errors": [], "grid": grid, "scale": scale,
              "sampled": sampled.label, "reference": reference.label}
    # Geometric membership tolerance is independent of the display scale.
    membership = max(1e-7, source.getTolerance(1))
    for i in range(grid):
        for j in range(grid):
            u, v = u0 + (i + .5) * (u1 - u0) / grid, v0 + (j + .5) * (v1 - v0) / grid
            try:
                point = source.valueAt(u, v)
                if not all(math.isfinite(x) for x in (point.x, point.y, point.z)):
                    raise ValueError("Non-finite surface point")
                if not source.isInside(point, membership, True):
                    report["outside"] += 1
                    continue
                # Singular parameter locations must not masquerade as regular samples.
                source.normalAt(u, v)
                distance = Part.Vertex(point).distToShape(target)[0]
                if not math.isfinite(distance) or distance < 0:
                    raise ValueError("Unresolved native distance")
                report["points"].append((point.x, point.y, point.z))
                report["distances"].append(distance)
                report["colors"].append(color(distance, scale))
            except Exception as error:
                report["unresolved"] += 1
                if len(report["errors"]) < 3:
                    report["errors"].append(str(error))
    values = report["distances"]
    if not values:
        raise ValueError("No usable samples: {} outside the trimmed face; {} singular/failed. {}".format(
            report["outside"], report["unresolved"], "; ".join(report["errors"])))
    report.update(minimum=min(values), maximum=max(values), mean=sum(values) / len(values),
                  saturated=sum(value >= scale for value in values))
    return report


def load_settings():
    params = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/SurfaceDeviation")
    try:
        return settings(params.GetInt("Grid", 11), params.GetFloat("Scale", 1.))
    except (ValueError, OverflowError):
        return 11, 1.


def save_settings(grid, scale):
    grid, scale = settings(grid, scale)
    params = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/SurfaceDeviation")
    params.SetInt("Grid", grid)
    params.SetFloat("Scale", scale)
