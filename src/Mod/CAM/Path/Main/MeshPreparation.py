# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bounded, non-mutating mesh review and explicit independent orientation copies."""
from collections import Counter
import hashlib
import math
import struct

import FreeCAD as App
from BasicShapes.ShapeReferences import require_current
from freecad.gui.DependencyInspector import identity

MAX_FACETS = 200000
DENSE_FACETS = 100000


def tr(text):
    return App.Qt.translate("MeshPreparation", text)


def inspect(source):
    if (source.TypeId != "Mesh::Feature" or source.getParentGeoFeatureGroup() is not None):
        raise ValueError(tr("Select a root imported mesh. Links, generated meshes and nested meshes are not supported here."))
    require_current(source)
    mesh = source.Mesh
    if not mesh.CountFacets:
        raise ValueError(tr("The mesh has no triangles."))
    if mesh.CountFacets > MAX_FACETS:
        raise ValueError(tr("This review supports up to 200,000 triangles. Use the Mesh workbench for larger inputs; no reduction was applied."))
    vertices, faces = mesh.Topology
    if not vertices or not faces:
        raise ValueError(tr("The mesh has incomplete triangle data."))
    digest = hashlib.sha256()
    for vertex in vertices:
        if not all(math.isfinite(value) for value in vertex):
            raise ValueError(tr("The mesh contains non-finite coordinates."))
        digest.update(struct.pack("<3d", *vertex))
    edges = Counter()
    triangles = set()
    duplicate = degenerate = 0
    volumes = []
    origin = vertices[0]
    for face in faces:
        if len(face) != 3 or any(index < 0 or index >= len(vertices) for index in face):
            raise ValueError(tr("The mesh contains invalid triangle indices."))
        digest.update(struct.pack("<3Q", *face))
        key = tuple(sorted(face))
        duplicate += key in triangles
        triangles.add(key)
        a, b, c = (vertices[index] for index in face)
        # A numerical zero-area threshold, not a repair/welding tolerance.
        cross = (b - a).cross(c - a)
        degenerate += cross.Length <= 1e-12
        volumes.append((a - origin).dot((b - origin).cross(c - origin)) / 6.0)
        for first, second in zip(face, (face[1], face[2], face[0])):
            edges[tuple(sorted((first, second)))] += 1
    boundary = sum(count == 1 for count in edges.values())
    nonmanifold = sum(count > 2 for count in edges.values())
    components = mesh.countComponents()
    inconsistent = mesh.countNonUniformOrientedFacets()
    closed = not boundary and not nonmanifold and mesh.isSolid()
    signed_volume = math.fsum(volumes)
    simple_closed = closed and components == 1 and not (inconsistent or degenerate or duplicate)
    orientation = (tr("Inward") if signed_volume < 0 else tr("Outward")) if simple_closed and signed_volume else tr("Undetermined")
    bounds = mesh.BoundBox
    return {"key": identity(source), "digest": digest.hexdigest(),
            "placement": tuple(source.Placement.toMatrix().A),
            "facets": len(faces), "points": len(vertices), "boundary": boundary,
            "nonmanifold": nonmanifold, "components": components,
            "inconsistent": inconsistent, "degenerate": degenerate, "duplicate": duplicate,
            "closed": closed, "signed_volume": signed_volume,
            "orientation": orientation, "can_flip": simple_closed and signed_volume < 0,
            "dense": len(faces) >= DENSE_FACETS,
            "bounds": (bounds.XMin, bounds.YMin, bounds.ZMin, bounds.XMax, bounds.YMax, bounds.ZMax)}


def reversed_copy(source, expected):
    """Reverse only a reviewed, uniformly inward single closed component; never relink jobs."""
    import FreeCADGui as Gui
    doc = source.Document
    if (App.ActiveDocument != doc or Gui.Control.activeDialog() or doc.HasPendingTransaction
            or App.getActiveTransaction()):
        raise ValueError(tr("Activate this document and finish the current task or edit transaction first."))
    report = inspect(source)
    if report != expected:
        raise ValueError(tr("The mesh changed. Review it again before creating a copy."))
    if not report["can_flip"]:
        raise ValueError(tr("Reversal is available only for one closed component with consistent inward normals and no degenerate or duplicate triangles."))
    mesh = source.Mesh.copy()
    mesh.flipNormals()
    doc.openTransaction(tr("Create reversed-normal mesh copy"))
    try:
        result = doc.addObject("Mesh::Feature", "OrientedMesh")
        result.Label = source.Label + tr(" (normals reversed)")
        result.Label2 = tr("Independent mesh snapshot; normals reversed. Existing CAM jobs still use their original model.")
        result.Mesh = mesh
        doc.recompute()
        verified = inspect(result)
        if (verified["signed_volume"] <= 0 or verified["facets"] != report["facets"]
                or verified["bounds"] != report["bounds"]):
            raise ValueError(tr("The reversed copy failed its dimension/orientation check."))
        doc.commitTransaction()
        return result
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise
