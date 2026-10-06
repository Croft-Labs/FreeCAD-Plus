# SPDX-License-Identifier: LGPL-2.1-or-later
"""Validated sketch-curve subsets and associative internal extrusion profiles."""
import FreeCAD as App
import Part
import ComponentModel as Model

TOLERANCE = 1e-7


def wires(sketch, elements):
    if not sketch.isDerivedFrom("Sketcher::SketchObject"):
        raise ValueError("Select curves from one sketch.")
    shape = Model.current_shape(sketch)
    names = list(dict.fromkeys(elements))
    if not names:
        raise ValueError("Select curves forming a closed region in one sketch.")
    edges = []
    for name in names:
        if not name.startswith("Edge") or not name[4:].isdigit():
            raise ValueError("Select sketch curves, not vertices or other objects.")
        try:
            edge = shape.getElement(name)
        except Exception as error:
            raise ValueError("A selected sketch curve is missing. Select its replacement.") from error
        if edge.ShapeType != "Edge":
            raise ValueError("Select sketch curves.")
        edges.append(edge)
    loops = [Part.Wire(group) for group in Part.sortEdges(edges)]
    if sum(len(loop.Edges) for loop in loops) != len(edges):
        raise ValueError("The selected curves contain duplicate or ambiguous edges.")
    for loop in loops:
        if not loop.isClosed() or not loop.isValid():
            raise ValueError("Every selected contour must be closed and non-intersecting.")
        loop.check(True)
        face = Part.Face(loop)
        if not face.isValid() or face.Area <= TOLERANCE ** 2:
            raise ValueError("The selected contour crosses itself or encloses no area.")
        face.check(True)
    for index, loop in enumerate(loops):
        if any(loop.distToShape(other)[0] <= TOLERANCE for other in loops[index + 1:]):
            raise ValueError("Selected contours must not cross or touch each other.")
    return names, loops


def face(sketch, elements):
    _, loops = wires(sketch, elements)
    result = Part.makeFace(loops, "Part::FaceMakerBullseye")
    if len(result.Faces) != 1 or not result.isValid():
        raise ValueError("Select one connected region, with optional holes.")
    result.check(True)
    return result


def region(sketch, point):
    """Return the enclosing contour and its immediate hole contours at a sketch-plane point."""
    shape = Model.current_shape(sketch)
    closed = [Part.Wire(group) for group in Part.sortEdges(shape.Edges) if Part.Wire(group).isClosed()]
    loops = closed
    faces = [Part.Face(loop) for loop in loops]
    containing = [i for i, candidate in enumerate(faces) if candidate.isInside(point, TOLERANCE, False)]
    if not containing:
        raise ValueError("Click inside a closed sketch region.")
    outer = min(containing, key=lambda i: faces[i].Area)
    children = []
    for index, loop in enumerate(loops):
        if index == outer or not faces[outer].isInside(loop.Vertexes[0].Point, TOLERANCE, False):
            continue
        if not any(i not in (outer, index) and faces[i].Area < faces[outer].Area
                   and faces[i].isInside(loop.Vertexes[0].Point, TOLERANCE, False)
                   for i in range(len(loops))):
            children.append(index)
    boundaries = [loops[outer]] + [loops[i] for i in children]
    if not Part.makeFace(boundaries, "Part::FaceMakerBullseye").isInside(point, TOLERANCE, False):
        raise ValueError("Click inside a closed sketch region, away from its boundary.")
    selected = ["Edge" + str(index + 1) for index, edge in enumerate(shape.Edges)
                if any(edge.isSame(candidate) for loop in boundaries for candidate in loop.Edges)]
    face(sketch, selected)
    return selected


class ProfileProxy(Model.PersistentProxy):
    def execute(self, obj):
        obj.Shape = Part.Shape()
        source, elements = obj.ProfileSource
        if source is None or Model.owner(source) != Model.owner(obj):
            raise ValueError("The selected sketch is missing or belongs to another component.")
        assign_shape(obj, source, face(source, elements))


def assign_shape(obj, sketch, shape):
    """Keep the sketch's signed normal, not a face builder's arbitrary plane axis."""
    if obj.isDerivedFrom("Part::Part2DObject"):
        shape = shape.copy()
        shape.transformShape(sketch.Placement.inverse().toMatrix(), True)
        obj.Shape = shape
        obj.Placement = sketch.Placement
    else:
        obj.Shape = shape


def selection(tool):
    base = tool.Profile[0] if tool.TypeId in ("PartDesign::Pad", "PartDesign::Pocket", "PartDesign::Revolution", "PartDesign::Groove") else tool.Base
    if hasattr(base, "ProfileSource") and getattr(base, "ComponentRole", "") == "Internal":
        sketch, elements = base.ProfileSource
        return sketch, list(elements)
    return base, None


def bind(component, sketch, elements, previous=None):
    if elements is None:
        return sketch
    shape = face(sketch, elements)
    bound = previous if previous is not None and previous.isDerivedFrom("Part::Part2DObject") and hasattr(previous, "ProfileSource") else None
    if bound is None:
        bound = component.Document.addObject("Part::Part2DObjectPython", "ExtrudeProfile")
        component.addObject(bound)
        Model._identity(bound, "Internal")
        Model._property(bound, "LinkSub", "ProfileSource", (sketch, list(elements)))
        bound.Proxy = ProfileProxy()
        if App.GuiUp:
            bound.ViewObject.Proxy = 0
            bound.ViewObject.ShowInTree = False
            bound.Visibility = False
    else:
        bound.ProfileSource = (sketch, list(elements))
    assign_shape(bound, sketch, shape)
    return bound
