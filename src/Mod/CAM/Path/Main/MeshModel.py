# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative mesh job models, without converting every STL facet to a CAD face."""

import FreeCAD
import Mesh


class MeshModel:
    def __init__(self, obj, source):
        obj.addProperty("App::PropertyLinkList", "Objects", "Base")
        obj.Objects = [source]
        obj.Placement = source.Placement
        obj.Proxy = self

    def execute(self, obj):
        placement = obj.Placement
        if not obj.Objects or not hasattr(obj.Objects[0], "Mesh"):
            obj.Mesh = Mesh.Mesh()
            raise ValueError("The CAM mesh model has no source mesh")
        source = obj.Objects[0]
        mesh = source.Mesh.copy()
        # Mesh coordinates already contain the source placement. Keep job setup
        # placement independent, just as for a Draft model clone.
        mesh.Placement = source.Placement.inverse().multiply(mesh.Placement)
        obj.Mesh = mesh
        obj.Placement = placement


def create(doc, source):
    obj = doc.addObject("Mesh::FeaturePython", "ModelMesh")
    MeshModel(obj, source)
    return obj
