# SPDX-License-Identifier: LGPL-2.1-or-later

"""Associative Trim Body document feature. GUI is loaded only on demand."""

import FreeCAD as App
import Part
from . import TrimAPI


def makeTrimBody(document=None, name="TrimBody"):
    document = document or App.ActiveDocument
    if document is None:
        raise TrimAPI.TrimError("Open a document before creating a trim.")
    obj = document.addObject("Part::FeaturePython", name)
    obj.Label = "Trim Body"
    TrimBody(obj)
    if App.GuiUp:
        from .TrimGui import ViewProviderTrimBody

        ViewProviderTrimBody(obj.ViewObject)
    return obj


class TrimBody:
    def __init__(self, obj):
        obj.addProperty("App::PropertyLinkSub", "Target", "Trim", "Solid or sheet to trim")
        obj.addProperty("App::PropertyLinkSub", "Tool", "Trim", "Cutting plane, face, or sheet")
        obj.addProperty(
            "App::PropertyLinkList", "PlacementSupport", "Trim", "Placement dependency containers"
        )
        obj.setEditorMode("PlacementSupport", 2)
        obj.addProperty("App::PropertyBool", "Reversed", "Trim", "Keep the opposite side")
        obj.addProperty(
            "App::PropertyBool", "ExtendPlanar", "Trim", "Extend planar tools across the target"
        )
        obj.addProperty(
            "App::PropertyBool", "Refine", "Trim", "Remove redundant edges from the result"
        )
        obj.addProperty(
            "App::PropertyVector", "Direction", "Trim", "Normal pointing toward the kept side"
        )
        obj.addProperty(
            "App::PropertyVector", "ArrowOrigin", "Trim", "Point on the cutting boundary"
        )
        obj.addProperty(
            "App::PropertyString", "StatusMessage", "Trim", "Result or validation message"
        )
        obj.ExtendPlanar = True
        obj.Refine = True
        obj.setEditorMode("Direction", 1)
        obj.setEditorMode("ArrowOrigin", 2)
        obj.setEditorMode("StatusMessage", 1)
        obj.Proxy = self

    def onChanged(self, obj, prop):
        if prop in ("Target", "Tool") and "PlacementSupport" in obj.PropertiesList:
            self.updatePlacementSupport(obj)

    def updatePlacementSupport(self, obj):
        containers = []
        for link in (obj.Target, obj.Tool):
            if not link or not link[0]:
                continue
            parent = link[0].getParentGeoFeatureGroup()
            while parent:
                # A common parent of result and inputs already transforms the result.
                if parent not in obj.InListRecursive and parent not in containers:
                    containers.append(parent)
                parent = parent.getParentGeoFeatureGroup()
        if obj.PlacementSupport != containers:
            obj.PlacementSupport = containers

    def execute(self, obj):
        try:
            self.updatePlacementSupport(obj)
            for link in (obj.Target, obj.Tool):
                TrimAPI.validate_link(obj, link[0] if link else None)
            if obj.Target[0] == obj.Tool[0]:
                raise TrimAPI.TrimError("Use a separate object as the cutting tool.")
            target = TrimAPI.linked_shape(obj.Target)
            tool = TrimAPI.tool_shape(obj.Tool)
            result, point, direction = TrimAPI.trim(
                target, tool, obj.Reversed, obj.ExtendPlanar, obj.Refine
            )
            # Resolve inputs globally, then express the result in its parent's frame.
            parent = obj.getGlobalPlacement().multiply(obj.Placement.inverse())
            result.transformShape(parent.inverse().toMatrix())
            obj.Shape = result
            obj.Direction = direction
            obj.ArrowOrigin = point
            obj.StatusMessage = "Ready"
        except Exception as error:
            obj.Shape = Part.Shape()  # Invalid input must never leave an old preview to accept.
            obj.StatusMessage = str(error)
            raise

    def dumps(self):
        return None

    def loads(self, state):
        pass
