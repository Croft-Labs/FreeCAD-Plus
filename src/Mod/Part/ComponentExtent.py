# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component adapter for the existing native Pad/Pocket extent engine."""
import FreeCAD as App
import ComponentModel as Model

TYPES = (("Dimension", "Length"), ("To last", "UpToLast"), ("To first", "UpToFirst"),
         ("Up to surface", "UpToFace"), ("Up to shape", "UpToShape"), ("Through all", "ThroughAll"))


def defaults():
    return dict(sides="One side", extent="Length", extent2="Length", length2=10.,
                offset=0., offset2=0., start="Profile plane", start_offset=0.,
                start_reference=None, limit=None, limit2=None, taper=0., taper2=0.,
                custom=False, direction=(0., 0., 1.), along_normal=True, refine=True)


def read(tool):
    values = defaults()
    if tool.TypeId not in ("PartDesign::Pad", "PartDesign::Pocket"):
        return values
    values.update(sides=tool.SideType, extent=tool.Type, extent2=tool.Type2,
                  length2=tool.Length2.Value, offset=tool.Offset.Value, offset2=tool.Offset2.Value,
                  start=tool.StartType, start_offset=tool.StartOffset.Value,
                  taper=tool.TaperAngle.Value, taper2=tool.TaperAngle2.Value,
                  custom=tool.UseCustomVector, direction=tuple(tool.Direction),
                  along_normal=tool.AlongSketchNormal, refine=tool.Refine)
    for key, value in (("limit", tool.UpToFace if tool.Type != "UpToShape" else tool.UpToShape),
                       ("limit2", tool.UpToFace2 if tool.Type2 != "UpToShape" else tool.UpToShape2),
                       ("start_reference", tool.StartReference)):
        if key in ("limit", "limit2") and values["extent" + ("2" if key == "limit2" else "")] == "UpToShape":
            if len(value) > 1:
                raise ValueError("This Up to shape uses several references. Edit its native properties to preserve them.")
            value = value[0] if value else None
        if value and value[0] is not None:
            values[key] = (value[0], list(value[1]))
    return values


def reference(component, text):
    if not text.strip():
        return None
    name, separator, element = text.strip().partition(".")
    obj = component.Document.getObject(name)
    if obj is None:
        raise ValueError("The reference object is unavailable: " + name)
    return obj, [element] if separator and element else []


def reference_text(value):
    return value[0].Name + ("." + value[1][0] if value[1] else "") if value else ""


def validate(component, profile, length, mode, target, values, operation=None):
    if values["sides"] not in ("One side", "Two sides", "Symmetric"):
        raise ValueError("Choose one dimension, two dimensions or symmetric.")
    active = [("extent", "limit", length, values["taper"])]
    if values["sides"] == "Two sides":
        active.append(("extent2", "limit2", values["length2"], values["taper2"]))
    for extent, limit, span, taper in active:
        kind = values[extent]
        if kind not in dict(TYPES).values():
            raise ValueError("Choose a supported extent type.")
        if kind == "Length" and span <= 0:
            raise ValueError("Each dimensional length must be positive.")
        if abs(taper) >= 90:
            raise ValueError("Taper must be between -90 and 90 degrees.")
        if kind in ("UpToFace", "UpToShape") and not values[limit]:
            raise ValueError("Select the limiting surface or shape.")
        suffix = "2" if extent == "extent2" else ""
        if kind == "UpToShape" and values[limit] and abs(values["offset" + suffix]) > 1e-9:
            obj, subs = values[limit]
            if len(subs) != 1 and not (hasattr(obj, "Shape") and obj.Shape.ShapeType == "Face"):
                raise ValueError("An end offset needs one limiting face. Select a face or set Offset to zero for a whole shape.")
        if kind in ("UpToFirst", "UpToLast", "ThroughAll") and target is None:
            raise ValueError("This extent needs an explicit target body. Choose Add or Subtract and a target.")
    if values["start"] not in ("Profile plane", "Offset", "Reference"):
        raise ValueError("Choose a start plane, offset or reference.")
    if values["start"] == "Reference" and not values["start_reference"]:
        raise ValueError("Select the start reference.")
    if values["custom"] and App.Vector(*values["direction"]).Length < 1e-9:
        raise ValueError("The custom direction cannot be zero.")
    used = [values[limit] for extent, limit, span, taper in active
            if values[extent] in ("UpToFace", "UpToShape")]
    if values["start"] == "Reference":
        used.append(values["start_reference"])
    for obj, subs in used:
        local = Model.owner(obj) == component or obj in component.Origin.OriginFeatures
        if obj.Document != component.Document or not local:
            raise ValueError("Use a reference owned by the active component.")
        if obj == profile or (operation and (obj == operation or operation in obj.OutListRecursive)):
            raise ValueError("The reference cannot be the profile or a downstream result of this Extrude.")
        if hasattr(obj, "Shape") and not obj.Shape.isNull():
            Model.current_shape(obj)
        for sub in subs:
            if not sub.startswith("Face") or not sub[4:].isdigit():
                raise ValueError("Choose a limiting face, plane or whole shape.")
            obj.Shape.getElement(sub)


def configure(tool, profile, length, mode, target, reverse, values):
    tool.Profile = (profile, [])
    tool.BaseFeature = target
    tool.Operation = "Subtraction" if mode == "Subtract" else "Union"
    tool.SideType = values["sides"]
    tool.Type, tool.Type2 = values["extent"], values["extent2"]
    tool.Length, tool.Length2 = length, values["length2"]
    tool.Reversed = bool(reverse)
    tool.StartType, tool.StartOffset = values["start"], values["start_offset"]
    tool.StartReference = values["start_reference"] or (None, [])
    for index, suffix in ((1, ""), (2, "2")):
        kind = values["extent" + suffix]
        setattr(tool, "UpToFace" + suffix, (values["limit" + suffix] or (None, [])) if kind == "UpToFace" else (None, []))
        limit = values["limit" + suffix]
        # Native whole-shape clipping opens a shell. A lone face must instead
        # use the native single-face path, retaining an associative subelement.
        if kind == "UpToShape" and limit and not limit[1] and hasattr(limit[0], "Shape") and limit[0].Shape.ShapeType == "Face":
            limit = (limit[0], ["Face1"])
        setattr(tool, "UpToShape" + suffix, [limit] if kind == "UpToShape" and limit else [])
        setattr(tool, "Offset" + suffix, values["offset" + suffix])
        setattr(tool, "TaperAngle" + suffix, values["taper" + suffix])
    tool.UseCustomVector = values["custom"]
    if values["custom"]:
        tool.Direction = App.Vector(*values["direction"])
    tool.AlongSketchNormal, tool.Refine = values["along_normal"], values["refine"]


def copy_references(scratch, values, copies):
    values = dict(values)
    for key in ("limit", "limit2", "start_reference"):
        value = values[key]
        if not value:
            continue
        obj, subs = value
        if obj not in copies:
            if hasattr(obj, "Shape") and not obj.Shape.isNull():
                copied = scratch.addObject("Part::Feature", "Limit")
                copied.Shape = Model.current_shape(obj)
            else:
                copied = scratch.addObject("PartDesign::Plane", "LimitPlane")
                copied.Placement = obj.Placement
            copies[obj] = copied
        values[key] = copies[obj], subs
    return values
