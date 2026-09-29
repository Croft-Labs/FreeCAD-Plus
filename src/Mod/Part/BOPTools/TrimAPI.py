# SPDX-License-Identifier: LGPL-2.1-or-later

"""Trim solids or sheets by an oriented plane, face, or connected sheet."""

import FreeCAD as App
import Part
from . import SplitAPI


class TrimError(ValueError):
    pass


def linked_shape(link):
    if not link or not link[0]:
        raise TrimError("Select a target and a cutting tool.")
    obj, subs = link
    if len(subs) > 1:
        raise TrimError("Select one object or one face for each field.")
    sub = subs[0] if subs else ""
    shape = Part.getShape(obj, sub, needSubElement=True, transform=True)
    # getShape includes the object's placement, but not its enclosing App::Part/Body.
    if hasattr(obj, "getGlobalPlacement") and hasattr(obj, "Placement"):
        parent = obj.getGlobalPlacement().multiply(obj.Placement.inverse())
        shape = shape.copy()
        shape.transformShape(parent.toMatrix())
    return shape


def tool_shape(link):
    if not link or not link[0]:
        raise TrimError("Select a cutting plane, face, or sheet.")
    obj, subs = link
    if not subs or not subs[0]:
        if obj.TypeId in ("PartDesign::Plane", "App::Plane"):
            face = Part.makePlane(2, 2, App.Vector(-1, -1, 0))
            face.transformShape(obj.getGlobalPlacement().toMatrix())
            return face
    shape = linked_shape(link)
    if shape.isNull() or not shape.Faces or shape.Solids:
        raise TrimError("Select a face of the tool solid, a datum plane, or a sheet body.")
    return shape


def validate_link(feature, obj):
    if obj is None or obj.Document != feature.Document:
        raise TrimError("Select an object in this document.")
    if obj == feature or obj in feature.InListRecursive:
        raise TrimError("A trim cannot reference itself or a dependent feature.")


def frame(tool, target):
    """Return a point on the oriented boundary and its normal, for half-space/arrow use."""
    faces = sorted(tool.Faces, key=lambda face: face.Area, reverse=True)
    for face in faces:
        u0, u1, v0, v1 = face.ParameterRange
        for fu in (0.5, 0.25, 0.75, 0.125, 0.875):
            for fv in (0.5, 0.25, 0.75, 0.125, 0.875):
                u, v = u0 + fu * (u1 - u0), v0 + fv * (v1 - v0)
                point = face.valueAt(u, v)
                if face.isInside(point, 1e-7, True):
                    normal = face.normalAt(u, v)
                    if normal.Length > 1e-12:
                        normal.normalize()
                        plane = tool.findPlane()
                        if plane is not None:
                            center = target.CenterOfMass
                            point = center - normal * (center - point).dot(normal)
                        return point, normal
    raise TrimError("Cannot determine a regular normal on the cutting surface.")


def trim(target, tool, reversed=False, extend_planar=True, refine=True):
    """Return (kept shape, arrow origin, keep direction); reject incomplete separations."""
    if target.isNull() or not target.Faces or not target.isValid():
        raise TrimError("The target must be a valid solid or sheet body.")

    def dimensions(shape):
        if shape.ShapeType in ("Solid", "CompSolid"):
            return {3}
        if shape.ShapeType in ("Face", "Shell"):
            return {2}
        if shape.ShapeType == "Compound":
            return set().union(*(dimensions(child) for child in shape.childShapes()))
        return {0}

    if dimensions(target) not in ({2}, {3}):
        raise TrimError("Use a solid body or sheet body, without loose edges or mixed geometry.")
    if tool.isNull() or not tool.Faces or tool.Solids or not tool.isValid():
        raise TrimError("The cutting tool must be a valid face or sheet.")
    solid_target = bool(target.Solids)
    measure = (lambda shape: abs(shape.Volume)) if solid_target else (lambda shape: shape.Area)
    total = measure(target)
    if total <= 1e-12:
        raise TrimError("The target has no usable volume or surface area.")
    epsilon = max(total * 1e-8, 1e-9)
    point, normal = frame(tool, target)
    plane = tool.findPlane()
    regions = []
    if plane is not None and extend_planar:
        boundary = Part.Face(Part.Plane(point, normal))
    else:
        # A finite curved sheet must actually separate the target. A half-space alone
        # could otherwise silently use geometry beyond the selected patch's edges.
        split = SplitAPI.slice(target, [tool], "Split")
        regions = split.Solids if solid_target else split.Faces
        count_before = len(target.Solids) if solid_target else len(target.Faces)
        count_after = len(split.Solids) if solid_target else len(split.Faces)
        if count_after <= count_before:
            raise TrimError("The cutting surface must extend fully through the target.")
        if len(tool.Faces) == 1:
            boundary = tool.Faces[0]
        else:
            sewn = Part.makeCompound(tool.Faces)
            sewn.sewShape()
            if len(sewn.Shells) != 1:
                raise TrimError("The tool faces must form one connected sheet.")
            boundary = sewn.Shells[0]
        if not boundary.isValid():
            raise TrimError("The tool faces must form one valid connected sheet.")
    direction = -normal if reversed else normal
    distance = max(target.BoundBox.DiagonalLength * 1e-5, 1e-5)
    halfspace = boundary.makeHalfSpace(point + direction * distance)
    for region in regions:
        region_size = measure(region)
        inside = measure(region.common(halfspace))
        if epsilon * 10 < inside < region_size - epsilon * 10:
            raise TrimError("The cutting surface must extend fully through every trimmed region.")
    kept = target.common(halfspace)
    removed = target.cut(halfspace)
    kept_size, removed_size = measure(kept), measure(removed)
    if kept_size <= epsilon or removed_size <= epsilon:
        raise TrimError("The tool must divide the target into two non-empty sides.")
    if abs(kept_size + removed_size - total) > epsilon * 10:
        raise TrimError("The cutting surface did not produce a complete separation.")
    if refine:
        kept = kept.removeSplitter()
    if kept.isNull() or not kept.isValid():
        raise TrimError("The trim did not produce valid geometry.")
    if solid_target and (not kept.Solids or any(not s.isClosed() for s in kept.Solids)):
        raise TrimError("The trimmed solid could not be closed.")
    return kept, point, direction
