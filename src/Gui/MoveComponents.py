# SPDX-License-Identifier: LGPL-2.1-or-later
"""One-time, parent-owned component placement; references are transient snapshots."""
import math

import FreeCAD as App
import Part
import ComponentModel as Model
from freecad.gui import ComponentSelection as Selection

WORKFLOWS = ("Translate", "Rotate", "Point to Point", "Align Axes",
             "Align Coordinate Systems", "Interactive")


def unit(vector):
    vector = App.Vector(vector)
    if not all(math.isfinite(v) for v in vector) or vector.Length < 1e-12:
        raise ValueError("Choose a finite, nonzero direction.")
    return vector.normalize()


def review(link):
    """Retain the existing native movement guards, including relationship consumers."""
    parent = Model.owner(link)
    if (getattr(link, "ComponentRole", "") != "Occurrence"
            or link.TypeId != "App::Link" or not Model.is_component(parent)
            or not Model.is_component(link.LinkedObject)):
        raise ValueError("Select whole component instances in Part Tree. A root/model cannot be moved.")
    if (link.ExpressionEngine or link.ElementCount or link.Scale != 1
            or tuple(link.ScaleVector) != (1, 1, 1)
            or any("ReadOnly" in link.getPropertyStatus(prop) for prop in ("Placement", "LinkPlacement"))
            or getattr(link, "AttachmentSupport", None)
            or getattr(link, "Grounded", False)
            or any(obj != parent for obj in link.InList)):
        raise ValueError("Driven, constrained, referenced or read-only instances need their relationship editor.")
    if "Invalid" in link.State:
        raise ValueError("Resolve the invalid instance before moving it.")
    # Native joints may reference a root plus a deep subpath. Such a property
    # appears in the root's InList, not in the moving child's InList.
    for doc in App.listDocuments().values():
        for obj in doc.Objects:
            for prop in ("Reference1", "Reference2"):
                ref = getattr(obj, prop, None)
                if not ref or not isinstance(ref, tuple) or len(ref) != 2 or ref[0] is None:
                    continue
                base, names = ref
                for name in names:
                    parts = name.split(".")
                    if base == link or any(base.getSubObject(".".join(parts[:i]) + ".", 1) == link
                                           for i in range(1, len(parts))):
                        raise ValueError("This component participates in an assembly joint. Use its relationship editor.")
    return parent


def selection_paths(root, entries):
    paths = []
    for entry in entries:
        for subname in entry.SubElementNames or [""]:
            picks = Selection.resolve(root, entry.Object, subname)
            if len(picks) != 1 or not picks[0].ids or picks[0].item is not None:
                raise ValueError("Select whole, unambiguous Part Tree instances, not Models or geometry.")
            if picks[0].ids not in paths:
                paths.append(picks[0].ids)
    return paths


class Session:
    """The exact displayed parent path plus owning links, shared by all workflows."""
    def __init__(self, root):
        if not Model.is_component(root):
            raise ValueError("Open a component document first.")
        self.root = root
        self.parent = None
        self.parent_path = None
        self.paths = []
        self.direction = None
        self.reverse = False
        self.distance = 0.
        self.axis = self.pivot = None
        self.angle = 0.
        self.expected = None

    def add(self, paths):
        paths = [tuple(path) for path in paths]
        if not paths:
            return
        proposed = list(dict.fromkeys(self.paths + paths))
        parent_path = self.parent_path if self.parent_path is not None else proposed[0][:-1]
        if any(not path or path[:-1] != parent_path for path in proposed):
            raise ValueError("Choose siblings under the same displayed parent. No part of this selection was added.")
        links = [Model._path(self.root, path)[-1] for path in proposed]
        parents = [review(link) for link in links]
        if len(set(parents)) != 1:
            raise ValueError("All components must belong to one parent definition.")
        if parents[0].Document != self.root.Document:
            raise ValueError("Open the external parent in its owning file before moving its children.")
        self.parent, self.parent_path, self.paths = parents[0], parent_path, proposed
        self.reset()

    def links(self):
        return [Model._path(self.root, path)[-1] for path in self.paths]

    def frame(self):
        if self.parent is None:
            raise ValueError("Select components first.")
        return Model._component_frame(self.root, self.parent_path)

    def signature(self):
        return (tuple(self.frame().toMatrix().A), tuple(
            (link.ObjectId, link.LinkedObject.ObjectId, bool(link.LinkTransform),
             tuple(link.LinkPlacement.toMatrix().A)) for link in self.links()))

    def reset(self):
        self.direction, self.reverse, self.distance = None, False, 0.
        self.axis = self.pivot = None
        self.angle = 0.
        self.source_point = self.destination_point = None
        self.source_axis = self.target_axis = None
        self.coincident, self.reverse_target = True, False
        self.source_frame = self.target_frame = None
        self.interactive_delta = App.Placement()
        self.expected = self.signature() if self.parent is not None else None

    def world_direction(self, vector):
        # Rotation only: a direction is not a point and must ignore translation.
        return unit(self.frame().Rotation.inverted().multVec(unit(vector)))

    def world_point(self, point):
        point = App.Vector(point)
        if not all(math.isfinite(v) for v in point):
            raise ValueError("Choose a finite point.")
        return self.frame().inverse().multVec(point)

    def resolved_axis(self):
        if self.axis is None:
            raise ValueError("Choose an axis or pick two distinct points.")
        point, direction = self.axis
        point = App.Vector(self.pivot if self.pivot is not None else point)
        if not all(math.isfinite(v) for v in point):
            raise ValueError("Choose a finite pivot point.")
        return point, unit(direction)

    def rotation(self):
        if not math.isfinite(self.angle) or not 0 <= self.angle <= 360:
            raise ValueError("Angle must be a finite magnitude between 0 and 360 degrees.")
        if self.angle == 0:
            return App.Placement()
        point, direction = self.resolved_axis()
        return App.Placement(App.Vector(), App.Rotation(direction, -self.angle if self.reverse else self.angle), point)

    def translation(self):
        if not math.isfinite(self.distance) or self.distance < 0:
            raise ValueError("Distance must be a finite nonnegative length.")
        if self.distance == 0:
            return App.Placement()
        if self.direction is None:
            raise ValueError("Choose a parent axis or pick a straight direction reference.")
        vector = unit(self.direction) * self.distance * (-1 if self.reverse else 1)
        return App.Placement(vector, App.Rotation())

    def point_to_point(self):
        if self.source_point is None or self.destination_point is None:
            raise ValueError("Pick both Source and Destination points.")
        source, target = finite_point(self.source_point), finite_point(self.destination_point)
        return App.Placement(target - source, App.Rotation())

    def align_axes(self):
        if self.source_axis is None or self.target_axis is None:
            raise ValueError("Pick both Source and Target axes.")
        source, direction = self.source_axis
        target, target_direction = self.target_axis
        source, target = finite_point(source), finite_point(target)
        direction, target_direction = unit(direction), unit(target_direction)
        if self.reverse_target:
            target_direction = -target_direction
        rotation = minimal_rotation(direction, target_direction)
        anchor = source
        if self.coincident:
            anchor = target + target_direction * ((source - target).dot(target_direction))
        # Rotate about the source anchor; translate only to its closest target point.
        return App.Placement(anchor - rotation.multVec(source), rotation)

    def align_frames(self):
        if self.source_frame is None or self.target_frame is None:
            raise ValueError("Define complete Source and Target coordinate systems.")
        validate_rigid_frame(self.source_frame)
        validate_rigid_frame(self.target_frame)
        return self.target_frame.multiply(self.source_frame.inverse())

    def candidates(self, delta):
        if not self.paths:
            raise ValueError("Select components to move.")
        if self.expected != self.signature():
            raise ValueError("The components or parent frame changed. Reset movement inputs and review again.")
        links = self.links()
        for link in links:
            if review(link) != self.parent:
                raise ValueError("The owning parent changed. Reopen Move Components.")
        return [(link, delta.multiply(link.LinkPlacement)) for link in links]

    def commit(self, delta):
        candidates = self.candidates(delta)
        if all(target.isSame(link.LinkPlacement, 1e-9) for link, target in candidates):
            return False
        with Model.transaction(self.parent.Document, "Move Components"):
            for link, target in candidates:
                link.LinkPlacement = target
            Model.validate(self.parent.Document, allow_unresolved=True)
        self.reset()
        return True

    def preview_shapes(self, delta, parent_paths=None):
        """Only view geometry, transformed after evaluation; no document mutation."""
        from freecad.gui import DesignLayers
        self.candidates(delta)
        shapes = []

        def visit(component, path, world_delta):
            representation = Model.representation(self.root, path)
            if representation == "Hidden":
                return
            results = Model.finished_results(component)
            for item in component.Group:
                if getattr(item, "ComponentRole", "") == "Occurrence":
                    if item.Visibility and item.LinkedObject:
                        visit(item.LinkedObject, path + (item.ObjectId,), world_delta)
                elif hasattr(item, "Shape") and item.Visibility and DesignLayers.visible(item):
                    if representation == "Bodies Only" and item not in results:
                        continue
                    if getattr(item, "ComponentRole", "") in ("Internal", "Operation"):
                        continue
                    shape = Part.getShape(self.root, Selection.native_path(self.root, path, item),
                                          needSubElement=True, transform=True)
                    if not shape.isNull():
                        shape = shape.copy()
                        shape.transformShape(world_delta.toMatrix())
                        shapes.append(shape)
        # The definition-owned edit affects every displayed occurrence of the
        # parent, so preview all those effects in their respective native frames.
        for parent_path in (Selection.definition_paths(self.root, self.parent)
                            if parent_paths is None else parent_paths):
            chain = Model._path(self.root, parent_path)
            if any(not link.Visibility for link in chain):
                continue
            frame = Model._component_frame(self.root, parent_path)
            world_delta = frame.multiply(delta).multiply(frame.inverse())
            for link in self.links():
                if link.Visibility:
                    visit(link.LinkedObject, parent_path + (link.ObjectId,), world_delta)
        return shapes

    def group_pivot(self):
        bounds = App.BoundBox()
        for shape in self.preview_shapes(self.interactive_delta, [self.parent_path]):
            shape = shape.copy()
            shape.transformShape(self.frame().inverse().toMatrix())
            bounds.add(shape.BoundBox)
        if bounds.isValid():
            return bounds.Center
        points = [self.interactive_delta.multVec(link.LinkPlacement.Base) for link in self.links()]
        return sum(points, App.Vector()) / len(points) if points else App.Vector()


def reference(session, base, subname):
    """Resolve a displayed native reference without losing its occurrence transform."""
    from freecad.gui import DesignSelection
    picks = Selection.resolve(session.root, base, subname)
    if len(picks) > 1:
        raise ValueError("Pick the reference in the viewport with its exact component occurrence path.")
    if len(picks) == 1 and base != session.root and picks[0].item is not None:
        pick = picks[0]
        base = session.root
        if pick.item in pick.component.Origin.OriginFeatures:
            subname = (Selection.native_path(base, pick.ids, pick.component.Origin)
                       + pick.item.Name + "." + pick.element)
        else:
            subname = Selection.native_path(base, pick.ids, pick.item) + pick.element
    obj, prefix, element = DesignSelection.resolve(base, subname)
    if obj is None:
        raise ValueError("The selected reference is unavailable.")
    if "Invalid" in obj.State:
        raise ValueError("The selected reference is invalid.")
    frame = base.getSubObject(prefix, 3) if prefix else obj.getGlobalPlacement()
    if obj.isDerivedFrom("Sketcher::SketchObject"):
        # Lowercase names select native sketch geometry/point indices, including
        # construction items. Uppercase names can address the evaluated Shape.
        for token in ("Edge", "Vertex"):
            if element.startswith(token):
                element = token.lower() + element[len(token):]
                break
    return base, prefix + element, obj, element, frame


def reference_axis(session, base, subname):
    """A line has both a location and a direction; snapshot both in the parent."""
    base, subname, obj, element, frame = reference(session, base, subname)
    if not element and obj.isDerivedFrom("App::Line"):
        point, world = frame.Base, frame.Rotation.multVec(App.Vector(1, 0, 0))
    elif not element and obj.isDerivedFrom("Part::DatumLine"):
        point, world = frame.Base, frame.Rotation.multVec(App.Vector(0, 0, 1))
    else:
        shape = Part.getShape(base, subname, needSubElement=True, transform=True)
        if shape.ShapeType != "Edge":
            if len(shape.Edges) != 1 or shape.Faces:
                raise ValueError("Pick one straight edge, line or reference axis.")
            shape = shape.Edges[0]
        if not isinstance(shape.Curve, (Part.Line, Part.LineSegment)):
            raise ValueError("Curved edges do not define a straight axis.")
        point = shape.valueAt(shape.FirstParameter)
        world = shape.tangentAt(shape.FirstParameter)
    return session.world_point(point), session.world_direction(world)


def reference_direction(session, base, subname):
    return reference_axis(session, base, subname)[1]


def reference_point(session, base, subname, midpoint=False):
    """Native vertex/Sketcher point mapping and analytic circular centers only."""
    base, subname, obj, element, frame = reference(session, base, subname)
    if not element and (obj.isDerivedFrom("App::Origin") or obj.isDerivedFrom("App::Point")
                        or obj.isDerivedFrom("Part::DatumPoint")):
        world = frame.Base
    else:
        # Native getSubObject maps Sketcher vertices (including construction
        # geometry and RootPoint); Shape.Vertexes is not a sketch point index.
        shape = base.getSubObject(subname) if subname else Part.getShape(base, transform=True)
        if not isinstance(shape, Part.Shape) or shape.isNull():
            raise ValueError("Pick a vertex, point, origin or circular edge center.")
        if shape.ShapeType == "Vertex":
            world = shape.Point
        elif shape.ShapeType == "Edge" and isinstance(shape.Curve, Part.Circle):
            # Same exact analytic circle location used by native Assembly picks.
            world = shape.Curve.Location
        elif midpoint and shape.ShapeType == "Edge" and shape.Length > 1e-7:
            world = shape.valueAt(shape.getParameterByLength(shape.Length * .5))
        elif len(shape.Vertexes) == 1 and not shape.Edges:
            world = shape.Vertexes[0].Point
        else:
            raise ValueError("Pick a vertex, point, origin or circular edge center.")
    return session.world_point(world)


def axis_from_points(first, second):
    first, second = App.Vector(first), App.Vector(second)
    if not all(math.isfinite(v) for v in (*first, *second)) or (second - first).Length <= 1e-7:
        raise ValueError("Axis points must be distinct (more than 1e-7 mm apart).")
    return first, unit(second - first)


def finite_point(point):
    point = App.Vector(point)
    if not all(math.isfinite(value) for value in point):
        raise ValueError("Choose a finite point.")
    return point


def minimal_rotation(source, target):
    source, target = unit(source), unit(target)
    cosine = max(-1., min(1., source.dot(target)))
    normal = source.cross(target)
    if normal.Length < 1e-12:
        if cosine > 0:
            return App.Rotation()
        # Least-aligned parent basis (X wins ties), then source cross basis.
        basis = min((App.Vector(1, 0, 0), App.Vector(0, 1, 0), App.Vector(0, 0, 1)),
                    key=lambda axis: abs(source.dot(axis)))
        return App.Rotation(unit(source.cross(basis)), 180.)
    return App.Rotation(unit(normal), math.degrees(math.atan2(normal.Length, cosine)))


def frame_from_references(origin, z_direction, x_direction):
    origin = finite_point(origin)
    z = unit(z_direction)
    x = unit(x_direction)
    perpendicular = x - z * x.dot(z)
    if perpendicular.Length <= 1e-10:
        raise ValueError("X direction must not be parallel to Z. Pick a different reference.")
    x = unit(perpendicular)
    y = unit(z.cross(x))
    return App.Placement(origin, App.Rotation(x, y, z, "ZXY"))


def validate_rigid_frame(frame):
    matrix = frame.toMatrix() if hasattr(frame, "toMatrix") else frame
    x = App.Vector(matrix.A11, matrix.A21, matrix.A31)
    y = App.Vector(matrix.A12, matrix.A22, matrix.A32)
    z = App.Vector(matrix.A13, matrix.A23, matrix.A33)
    if (not all(math.isfinite(v) for v in matrix.A)
            or any(abs(v.Length - 1) > 1e-8 for v in (x, y, z))
            or any(abs(a.dot(b)) > 1e-8 for a,b in ((x,y), (y,z), (z,x)))
            or abs(x.cross(y).dot(z) - 1) > 1e-8
            or any(abs(v) > 1e-8 for v in (matrix.A41, matrix.A42, matrix.A43))
            or abs(matrix.A44 - 1) > 1e-8):
        raise ValueError("Coordinate systems must be rigid, unscaled and right-handed.")


def reference_frame(session, base, subname):
    base, name, obj, element, frame = reference(session, base, subname)
    if element or not (Model.is_component(obj) or obj.isDerivedFrom("App::Origin")
                       or obj.isDerivedFrom("PartDesign::CoordinateSystem")
                       or obj.isDerivedFrom("Part::DatumCoordinateSystem")):
        raise ValueError("Pick a component origin or native datum coordinate system, or define Origin/Z/X.")
    # Reject scaled occurrences before Placement conversion can discard scale.
    names = name.split(".")
    for i in range(1, len(names)):
        ancestor = base.getSubObject(".".join(names[:i]) + ".", 1)
        if ancestor and ancestor.isDerivedFrom("App::Link"):
            if ancestor.Scale != 1 or tuple(ancestor.ScaleVector) != (1, 1, 1):
                raise ValueError("A scaled occurrence cannot provide a rigid coordinate system.")
    validate_rigid_frame(frame)
    return session.frame().inverse().multiply(frame)


def frame_geometry(session, frames, size):
    axes = []
    for frame in frames:
        axes.extend((frame.Base, frame.Rotation.multVec(axis)) for axis in
                    (App.Vector(1, 0, 0), App.Vector(0, 1, 0), App.Vector(0, 0, 1)))
    return axis_geometry(session, axes, size)


def reference_alignment_axis(session, base, subname):
    resolved_base, resolved_name, obj, element, frame = reference(session, base, subname)
    shape = Part.getShape(resolved_base, resolved_name, needSubElement=True, transform=True)
    if shape.ShapeType == "Edge" and isinstance(shape.Curve, Part.Circle):
        return session.world_point(shape.Curve.Location), session.world_direction(shape.Curve.Axis)
    if shape.ShapeType == "Face" and isinstance(shape.Surface, Part.Cylinder):
        return session.world_point(shape.Surface.Center), session.world_direction(shape.Surface.Axis)
    return reference_axis(session, base, subname)


def axis_geometry(session, axes, size):
    size = max(1., size)
    pieces = []
    frame = session.frame()
    for anchor, direction in axes:
        point, direction = frame.multVec(finite_point(anchor)), frame.Rotation.multVec(unit(direction))
        end = point + direction * size
        across = unit(direction.cross(App.Vector(1, 0, 0) if abs(direction.x) < .8 else App.Vector(0, 1, 0)))
        pieces.extend((Part.makeLine(point-direction*size, end),
                       Part.makeLine(end, end-direction*size*.15+across*size*.07),
                       Part.makeLine(end, end-direction*size*.15-across*size*.07)))
    return Part.makeCompound(pieces)


def point_marker(session, points, size):
    pieces = []
    world = [session.frame().multVec(finite_point(point)) for point in points]
    for point in world:
        for axis in (App.Vector(1, 0, 0), App.Vector(0, 1, 0), App.Vector(0, 0, 1)):
            pieces.append(Part.makeLine(point - axis * size, point + axis * size))
    if len(world) == 2 and (world[1] - world[0]).Length > 1e-7:
        pieces.append(Part.makeLine(*world))
    return Part.makeCompound(pieces)


def axis_marker(session, size):
    """Non-document axis arrow and pivot cross in the selected display context."""
    point, direction = session.resolved_axis()
    frame = session.frame()
    point, direction = frame.multVec(point), frame.Rotation.multVec(direction)
    # Arrow follows the resolved positive axis; Reverse changes angle sign only.
    size = max(1., size)
    across = direction.cross(App.Vector(1, 0, 0) if abs(direction.x) < .8 else App.Vector(0, 1, 0))
    across.normalize()
    end = point + direction * size
    pieces = [Part.makeLine(point - direction * size, end),
              Part.makeLine(end, end - direction * size * .15 + across * size * .07),
              Part.makeLine(end, end - direction * size * .15 - across * size * .07)]
    for axis in (App.Vector(1, 0, 0), App.Vector(0, 1, 0), App.Vector(0, 0, 1)):
        pieces.append(Part.makeLine(point - axis * size * .04, point + axis * size * .04))
    return Part.makeCompound(pieces)
