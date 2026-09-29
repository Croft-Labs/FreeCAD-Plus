# SPDX-License-Identifier: LGPL-2.1-or-later
"""Job-level stock bridges for three-axis Parallel and Waterline operations."""

import math

import FreeCAD
import Part
import Path


def invalidate_consumers(obj):
    """Remove old paths immediately, including when recompute later fails."""
    for consumer in obj.InListRecursive:
        if hasattr(consumer, "Path"):
            consumer.Path = Path.Path()


def bind_operation(op, job):
    tabs = list(getattr(job, "HoldingTabs", []))
    if tabs and not hasattr(op, "HoldingTabs"):
        op.addProperty("App::PropertyLinkList", "HoldingTabs", "Stock",
                       "Stock bridges preserved by supported operations")
        op.setEditorMode("HoldingTabs", 1)
    if hasattr(op, "HoldingTabs") and list(op.HoldingTabs) != tabs:
        op.HoldingTabs = tabs


class HoldingTab:
    def __init__(self, obj):
        for name, value in (("Length", 10), ("Width", 5), ("Height", 2)):
            obj.addProperty("App::PropertyLength", name, "Tab")
            setattr(obj, name, value)
        obj.Proxy = self

    def onChanged(self, obj, prop):
        if prop in ("Length", "Width", "Height", "Placement", "Shape"):
            invalidate_consumers(obj)

    def execute(self, obj):
        if min(obj.Length.Value, obj.Width.Value, obj.Height.Value) <= 0:
            obj.Shape = Part.Shape()
            raise ValueError("Tab length, width and height must be positive")
        placement = obj.Placement
        obj.Shape = Part.makeBox(obj.Length.Value, obj.Width.Value, obj.Height.Value,
                                 FreeCAD.Vector(-obj.Length.Value / 2,
                                                -obj.Width.Value / 2, 0))
        obj.Placement = placement


def create(job, point=None):
    if getattr(job, "SourceJob", None):
        raise ValueError("Create shared holding tabs in the original source Job")
    obj = job.Document.addObject("Part::FeaturePython", "HoldingTab")
    obj.Label = FreeCAD.Qt.translate("CAM", "Holding tab")
    HoldingTab(obj)
    bb = job.Proxy.modelBoundBox(job)
    stock = job.Stock.Shape.BoundBox
    if point is None:
        point = FreeCAD.Vector((bb.XMax + stock.XMax) / 2, bb.Center.y, stock.ZMin)
    obj.Length = max(10, stock.XMax - bb.XMax + 4)
    obj.Placement.Base = point
    if not hasattr(job, "HoldingTabs"):
        job.addProperty("App::PropertyLinkList", "HoldingTabs", "Stock",
                        "Stock bridges for Parallel and Waterline machining")
    job.HoldingTabs = list(job.HoldingTabs) + [obj]
    for op in job.Operations.Group:
        bind_operation(op, job)
    if FreeCAD.GuiUp:
        from Path.Main.Gui.HoldingTab import ViewProvider

        ViewProvider(obj.ViewObject)
        obj.ViewObject.ShapeColor = (1.0, 0.65, 0.1)
        obj.ViewObject.Transparency = 30
    job.Document.recompute()
    from Path.Main.IndexedSetup import sync_tabs

    for dependent in job.Document.Objects:
        if getattr(dependent, "SourceJob", None) == job:
            sync_tabs(dependent)
    return obj


def rectangles(tabs, radius):
    """Conservative cutter envelopes in each tab's local XY frame.

    Expanding the rectangle by the full tool radius also protects ball-end
    tools. It leaves extra stock at corners rather than risking a bridge.
    The protected column extends downwards, preserving the tab's foundation.
    """
    result = []
    for tab in tabs:
        if getattr(tab, "SetupFrame", None):
            if tab.Shape.isNull() or not getattr(tab, "Objects", []):
                raise ValueError("An indexed holding tab has lost its source geometry")
            # A tilted bridge is protected conservatively by its XY envelope.
            # Its actual solid is retained for display and propagation; never
            # rotate just the model while leaving tab protection in another frame.
            bb = tab.Shape.BoundBox
            inverse = FreeCAD.Placement(
                FreeCAD.Vector(bb.Center.x, bb.Center.y, 0), FreeCAD.Rotation()
            ).inverse()
            result.append((inverse, bb.XLength / 2 + radius + 0.05,
                           bb.YLength / 2 + radius + 0.05, bb.ZMax + 0.05))
            continue
        axis = tab.Placement.Rotation.multVec(FreeCAD.Vector(0, 0, 1))
        if (axis - FreeCAD.Vector(0, 0, 1)).Length > 1e-7:
            raise ValueError("Holding tabs must be parallel to the XY machining plane")
        if tab.Shape.isNull() or min(tab.Length.Value, tab.Width.Value, tab.Height.Value) <= 0:
            raise ValueError("A holding tab has invalid dimensions")
        margin = radius + 0.05
        result.append((tab.Placement.inverse(), tab.Length.Value / 2 + margin,
                       tab.Width.Value / 2 + margin,
                       tab.Placement.Base.z + tab.Height.Value + 0.05))
    return result


def interval(a, b, rect):
    """Exact segment/expanded rectangular prism intersection, in [0,1]."""
    inverse, half_x, half_y, top = rect
    p, q = inverse.multVec(a), inverse.multVec(b)
    lo, hi = 0.0, 1.0
    # XY only: below/above the tab is checked separately in protect().
    for start, end, half in ((p.x, q.x, half_x), (p.y, q.y, half_y)):
        delta = end - start
        if abs(delta) < 1e-12:
            if abs(start) > half:
                return None
        else:
            x, y = sorted(((-half - start) / delta, (half - start) / delta))
            lo, hi = max(lo, x), min(hi, y)
            if lo > hi:
                return None
    return lo, hi


def protect(commands, tabs, radius, safe_z, vertical_feed):
    """Lift linear cutting/linking moves around solid stock bridges.

    Split at analytical cutter-envelope intersections, not sampled path points.
    Keep the nominal input position separate from the lifted output position so
    consecutive moves inside a tab never plunge back into it. Unsupported motion
    fails closed; a caller must discard stale paths when this raises.
    """
    if not tabs:
        return commands
    if not math.isfinite(radius) or radius <= 0 or vertical_feed <= 0:
        raise ValueError("Tab protection needs a valid milling tool and plunge feed")
    rects = rectangles(tabs, radius)
    top = max(r[3] for r in rects)
    if safe_z <= top:
        raise ValueError("Safe and clearance heights must be above every holding tab")
    nominal = {"X": None, "Y": None, "Z": None}
    actual = dict(nominal)
    output = []
    cutting_feed = None

    def emit(name, point, feed=None):
        values = dict(zip(("X", "Y", "Z"), point))
        if values == actual:
            return
        actual.update(values)
        if feed is not None:
            values["F"] = feed
        generated = Path.Command(name, values)
        generated.Annotations = cmd.Annotations
        output.append(generated)

    for cmd in commands:
        name, params = cmd.Name, dict(cmd.Parameters)
        if name not in ("G0", "G00", "G1", "G01"):
            if name.startswith("G") or any(k in params for k in "XYZABCUVW"):
                raise ValueError("Holding tabs currently support linear three-axis paths only")
            output.append(cmd)
            continue
        if any(k in params for k in "ABCUVW"):
            raise ValueError("Holding tabs do not support rotary motion")
        if name in ("G1", "G01") and "F" in params:
            cutting_feed = params["F"]
        end = {k: params.get(k, nominal[k]) for k in nominal}
        if any(v is not None and not math.isfinite(v) for v in end.values()):
            raise ValueError("Non-finite toolpath coordinate")
        if any(v is None for v in nominal.values()):
            # The initial retract/position sequence must establish a safe Z
            # before XY motion; never invent an unknown starting location.
            if "Z" in params:
                params["Z"] = max(params["Z"], safe_z)
            if any(k in params for k in ("X", "Y")) and (
                actual["Z"] is None or actual["Z"] < safe_z
            ):
                raise ValueError("Tab protection requires an initial safe Z retract")
            generated = Path.Command(name, params)
            generated.Annotations = cmd.Annotations
            output.append(generated)
            nominal.update(end)
            actual.update({k: v for k, v in params.items() if k in actual})
            continue
        a, b = FreeCAD.Vector(*nominal.values()), FreeCAD.Vector(*end.values())
        spans = [(span, rect[3]) for rect in rects if (span := interval(a, b, rect))]
        breaks = sorted({0.0, 1.0, *(t for span, _ in spans for t in span)})
        for start, finish in zip(breaks, breaks[1:]):
            p, q = a + (b - a) * start, a + (b - a) * finish
            mid = (start + finish) / 2
            blocked = any(lo <= mid <= hi and min(p.z, q.z) < height
                          for (lo, hi), height in spans)
            if blocked:
                p.z = max(p.z, safe_z)
                q.z = max(q.z, safe_z)
            # The segment before a bridge ends at the expanded boundary.
            # Retract there; resume with a feed plunge only after exiting it.
            if abs(actual["Z"] - p.z) > 1e-9:
                emit("G0" if p.z > actual["Z"] else "G1", p,
                     None if p.z > actual["Z"] else vertical_feed)
            emit(name, q, cutting_feed if name in ("G1", "G01") else params.get("F"))
        nominal.update(end)
    return output
