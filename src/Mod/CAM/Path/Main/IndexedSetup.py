# SPDX-License-Identifier: LGPL-2.1-or-later
"""Separate three-axis jobs for manually indexed sides of the same physical stock.

Models, stock and holding tabs share one associative setup transform. No rotary
machine moves are inferred: each job is posted separately after physical indexing.
"""

import FreeCAD as App
import Mesh
import Part
from Path.Main import Job, Stock, HoldingTab


class Frame:
    def __init__(self, obj, stock):
        obj.addProperty("App::PropertyLink", "SourceStock", "Setup")
        obj.SourceStock = stock
        obj.addProperty("App::PropertyEnumeration", "Axis", "Setup")
        obj.Axis = ["X", "Y", "Z"]
        obj.addProperty("App::PropertyAngle", "Angle", "Setup")
        obj.Angle = 180
        obj.addProperty("App::PropertyEnumeration", "Origin", "Setup")
        obj.Origin = ["Stock top center", "Stock top corner", "Custom"]
        obj.addProperty("App::PropertyVector", "CustomOrigin", "Setup",
                        "Work origin in rotated source coordinates")
        obj.addProperty("App::PropertyPlacement", "Transform", "Setup")
        obj.setEditorMode("Transform", 1)
        obj.Proxy = self

    def onChanged(self, obj, prop):
        if prop in ("SourceStock", "Axis", "Angle", "Origin", "CustomOrigin", "Transform"):
            HoldingTab.invalidate_consumers(obj)

    def execute(self, obj):
        if not obj.SourceStock or obj.SourceStock.Shape.isNull():
            raise ValueError("Indexed setup needs valid source stock")
        axis = {"X": App.Vector(1, 0, 0), "Y": App.Vector(0, 1, 0),
                "Z": App.Vector(0, 0, 1)}[obj.Axis]
        rotation = App.Rotation(axis, obj.Angle.Value)
        shape = obj.SourceStock.Shape.copy()
        shape.Placement = App.Placement(App.Vector(), rotation).multiply(shape.Placement)
        bb = shape.BoundBox
        origin = obj.CustomOrigin
        if obj.Origin == "Stock top center":
            origin = App.Vector(bb.Center.x, bb.Center.y, bb.ZMax)
        elif obj.Origin == "Stock top corner":
            origin = App.Vector(bb.XMin, bb.YMin, bb.ZMax)
        transform = App.Placement(-origin, rotation)
        if not (obj.Transform.Base.isEqual(transform.Base, 1e-10)
                and obj.Transform.Rotation.isSame(transform.Rotation, 1e-10)):
            obj.Transform = transform


class Geometry:
    def __init__(self, obj, source, frame):
        if "Objects" not in obj.PropertiesList:
            obj.addProperty("App::PropertyLinkList", "Objects", "Base")
        obj.Objects = [source]
        obj.addProperty("App::PropertyLink", "SetupFrame", "Setup")
        obj.SetupFrame = frame
        obj.setEditorMode("Placement", 1)
        obj.Proxy = self

    def execute(self, obj):
        if hasattr(obj, "Mesh"):
            obj.Mesh = Mesh.Mesh()
        else:
            obj.Shape = Part.Shape()
        if not obj.Objects or not obj.SetupFrame:
            if hasattr(obj, "Mesh"):
                obj.Mesh = Mesh.Mesh()
            else:
                obj.Shape = Part.Shape()
            raise ValueError("Indexed geometry has lost its source or setup frame")
        source = obj.Objects[0]
        frame = obj.SetupFrame
        # Re-evaluate the frame to prevent a previously valid transform surviving
        # a failed/missing stock input during direct API execution.
        frame.Proxy.execute(frame)
        if hasattr(obj, "Mesh"):
            mesh = source.Mesh.copy()
            mesh.Placement = frame.Transform.multiply(mesh.Placement)
            obj.Mesh = mesh
            obj.Placement = mesh.Placement
        else:
            shape = source.Shape.copy()
            shape.Placement = frame.Transform.multiply(shape.Placement)
            obj.Shape = shape
            obj.Placement = shape.Placement


def require_current_geometry(job):
    """Consume indexed inputs without rewriting already recomputed producers."""
    frame = job.IndexFrame
    geometry = list(job.Model.Group) + [job.Stock] + list(getattr(job, "HoldingTabs", []))
    for item in geometry:
        if not item or getattr(item, "SetupFrame", None) != frame:
            raise ValueError("Indexed models, stock and tabs must use the same setup frame")
    seen = set()
    for item in [frame] + geometry:
        for dependency in [item] + list(item.OutListRecursive):
            if dependency.Name in seen:
                continue
            seen.add(dependency.Name)
            if "Invalid" in dependency.State or "Touched" in dependency.State:
                raise ValueError("Indexed setup input needs recompute or repair: " + dependency.Label)
    if not frame.SourceStock or frame.SourceStock.Shape.isNull():
        raise ValueError("Indexed setup needs valid source stock")


def copy_geometry(source, frame, name):
    kind = "Mesh::FeaturePython" if hasattr(source, "Mesh") else "Part::FeaturePython"
    obj = source.Document.addObject(kind, name)
    Geometry(obj, source, frame)
    if App.GuiUp:
        obj.ViewObject.Proxy = 0
    obj.Label = source.Label + " (indexed)"
    obj.Proxy.execute(obj)
    return obj


def sync_tabs(job):
    """Add newly created source bridges to a dependent indexed setup."""
    source = job.SourceJob
    tabs = list(getattr(job, "HoldingTabs", []))
    existing = {tab.Objects[0] for tab in tabs if getattr(tab, "Objects", [])}
    for original in getattr(source, "HoldingTabs", []):
        if original in existing:
            continue
        tab = copy_geometry(original, job.IndexFrame, "IndexedTab")
        if App.GuiUp:
            from Path.Main.Gui.IndexedSetup import TabViewProvider

            TabViewProvider(tab.ViewObject)
            tab.ViewObject.ShapeColor = (1.0, 0.65, 0.1)
            tab.ViewObject.Transparency = 30
        tabs.append(tab)
    if not hasattr(job, "HoldingTabs"):
        job.addProperty("App::PropertyLinkList", "HoldingTabs", "Stock")
    job.HoldingTabs = tabs
    for op in job.Operations.Group:
        HoldingTab.bind_operation(op, job)
    for dependent in job.Document.Objects:
        if getattr(dependent, "SourceJob", None) == job:
            sync_tabs(dependent)


def create(source, axis="X", angle=180, origin="Stock top center", custom_origin=None):
    doc = source.Document
    if not source.Model.Group or not source.Stock:
        raise ValueError("Select a Job with models and stock")
    frame = doc.addObject("App::FeaturePython", "IndexFrame")
    Frame(frame, source.Stock)
    frame.Axis, frame.Angle, frame.Origin = axis, angle, origin
    if custom_origin is not None:
        frame.CustomOrigin = custom_origin
    frame.Proxy.execute(frame)
    if App.GuiUp:
        from Path.Main.Gui.IndexedSetup import FrameViewProvider

        FrameViewProvider(frame.ViewObject)
    job = Job.Create("IndexedJob", list(source.Model.Group))
    job.Label = source.Label + " - " + axis + " " + str(angle) + " deg"
    job.addProperty("App::PropertyLink", "SourceJob", "Setup")
    job.SourceJob = source
    job.addProperty("App::PropertyLink", "IndexFrame", "Setup")
    job.IndexFrame = frame
    for model, original in zip(job.Model.Group, source.Model.Group):
        # Keep Job resource identities and view providers; replace only cloning
        # behavior with a transform shared by stock and bridges.
        Geometry(model, original, frame)
        model.Proxy.execute(model)
    old_stock = job.Stock
    stock = copy_geometry(source.Stock, frame, "IndexedStock")
    stock.addProperty("App::PropertyString", "StockType")
    stock.StockType = Stock.StockType.Unknown
    stock.addProperty("App::PropertyString", "PathResource")
    stock.PathResource = "Stock"
    job.Stock = stock
    doc.removeObject(old_stock.Name)
    if App.GuiUp:
        from Path.Main.Gui import Job as JobGui

        job.ViewObject.Proxy = JobGui.ViewProvider(job.ViewObject)
        job.ViewObject.addExtension("Gui::ViewProviderGroupExtensionPython")
        job.ViewObject.Proxy.deleteOnReject = False
        Stock.ApplyStockViewDefaults(stock)
    if source.Tools.Group and job.Tools.Group:
        old, new = source.Tools.Group[0], job.Tools.Group[0]
        new.Tool = old.Tool
        for prop in ("HorizFeed", "VertFeed", "HorizRapid", "VertRapid", "SpindleSpeed"):
            if hasattr(old, prop) and hasattr(new, prop):
                setattr(new, prop, getattr(old, prop))
    sync_tabs(job)
    doc.recompute()
    return job
