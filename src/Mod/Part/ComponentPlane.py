# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative datum-plane definitions using native datum and attachment objects."""
import math
import FreeCAD as App
import Part
import ComponentModel as Model
import ComponentSketch as Sketch


class UnderDefined(ValueError):
    pass


def geometry(component, reference, operation=None):
    """Return a plane, edge, axis or point in component coordinates."""
    obj, element = reference
    if obj is None:
        raise ValueError("A selected reference is missing.")
    origins = component.Origin.OriginFeatures
    if obj != component.Origin and obj not in origins and Model.owner(obj) != component:
        raise ValueError("Choose geometry in the active component.")
    if operation and (obj == operation or operation in obj.OutListRecursive):
        raise ValueError("A plane cannot depend on itself or its downstream features.")
    if "Invalid" in obj.State:
        raise ValueError("Repair the selected reference first.")
    if obj == component.Origin:
        return "point", App.Vector()
    transform = component.getGlobalPlacement().inverse().multiply(obj.getGlobalPlacement())
    if not element:
        if obj.isDerivedFrom("App::Plane") or obj.isDerivedFrom("Part::DatumPlane"):
            return "plane", transform
        if obj.isDerivedFrom("App::Line"):
            return "line", (transform.Base, transform.Rotation.multVec(App.Vector(1, 0, 0)))
        if obj.isDerivedFrom("App::Point"):
            return "point", transform.Base
    shape = Model.current_shape(obj)
    shape = shape.getElement(element) if element else shape
    if shape.ShapeType not in ("Face", "Edge", "Vertex"):
        if len(shape.Vertexes) == 1 and not shape.Edges:
            shape = shape.Vertexes[0]
        elif len(shape.Edges) == 1 and not shape.Faces:
            shape = shape.Edges[0]
        elif len(shape.Faces) == 1:
            shape = shape.Faces[0]
        else:
            raise ValueError("Pick a face, edge, plane, axis or point rather than a whole body.")
    shape = shape.copy()
    shape.transformShape(transform.multiply(obj.Placement.inverse()).toMatrix())
    if shape.ShapeType == "Face":
        if not isinstance(shape.Surface, Part.Plane):
            raise ValueError("The selected face must be flat.")
        normal = shape.normalAt(0, 0)
        return "plane", App.Placement(shape.CenterOfMass, App.Rotation(App.Vector(0, 0, 1), normal))
    if shape.ShapeType == "Vertex":
        return "point", shape.Point
    return "edge", shape


def unit(vector):
    vector = App.Vector(vector)
    if not all(math.isfinite(v) for v in (vector.x, vector.y, vector.z)) or vector.Length < 1e-9:
        raise ValueError("Enter a finite, nonzero direction vector.")
    vector.normalize()
    return vector


def line(value):
    kind, data = value
    if kind == "line":
        return data[0], unit(data[1])
    if kind == "edge" and isinstance(data.Curve, (Part.Line, Part.LineSegment)):
        return data.valueAt(data.FirstParameter), unit(data.tangentAt(data.FirstParameter))
    return None


def surface(component, references, operation=None):
    """Classify incomplete inputs separately from contradictory geometry."""
    items = [geometry(component, ref, operation) for ref in references]
    if not items:
        raise UnderDefined("Select a plane/face, two coplanar lines, three points, or a line and point.")
    if len(items) == 1 and items[0][0] == "plane":
        return items[0][1]
    if any(kind == "plane" for kind, data in items):
        raise ValueError("Use a plane or flat face by itself.")
    if len(items) == 1:
        raise UnderDefined("Add another line or point to define the plane.")
    points = []
    if all(kind == "point" for kind, data in items):
        if len(items) < 3:
            raise UnderDefined("Select a third non-collinear point.")
        if len(items) != 3:
            raise ValueError("Use exactly three points.")
        points = [data for kind, data in items]
    elif len(items) == 2:
        for item in items:
            along = line(item)
            if along:
                anchor, direction = along
                points.extend((anchor, anchor + direction))
            elif item[0] == "point":
                points.append(item[1])
            elif item[0] == "edge":
                # Curves are allowed only when their complete geometry is planar.
                points.extend(item[1].discretize(Number=17))
            else:
                raise ValueError("Choose two coplanar edges/lines, or a line and a point.")
    else:
        raise ValueError("Use a plane/face, two edges/lines, three points, or a line and point.")
    anchor = points[0]
    vectors = [p - anchor for p in points[1:] if (p - anchor).Length > 1e-8]
    normal = next((vectors[0].cross(v) for v in vectors[1:]
                   if vectors[0].cross(v).Length > 1e-8), None) if vectors else None
    if normal is None:
        raise ValueError("The selected geometry is coincident or collinear.")
    normal = unit(normal)
    if any(abs((point - anchor).dot(normal)) > 1e-7 for point in points):
        raise ValueError("The selected geometry is not coplanar.")
    # Check complete curved-edge geometry against the plane, not just endpoints.
    for kind, data in items:
        if kind == "edge" and line((kind, data)) is None:
            # Native findPlane checks the underlying curves for planarity.
            if Part.makeCompound([data, Part.makeLine(anchor, anchor + vectors[0])]).findPlane() is None:
                raise ValueError("The selected curve does not lie in the defined plane.")
    return App.Placement(anchor, App.Rotation(App.Vector(0, 0, 1), normal))


def axis(component, references, normal, operation=None):
    items = [geometry(component, ref, operation) for ref in references]
    if not items:
        axes = [App.Vector(1, 0, 0), App.Vector(0, 1, 0), App.Vector(0, 0, 1)]
        lengths = [(v - normal * v.dot(normal)).Length for v in axes]
        along = next(v for v, length in zip(axes, lengths) if length >= max(lengths) - 1e-12)
    elif len(items) == 2 and all(kind == "point" for kind, data in items):
        along = items[1][1] - items[0][1]
    elif len(items) == 1:
        kind, data = items[0]
        if kind == "point":
            raise UnderDefined("Select a second point for the X direction.")
        if kind == "line":
            along = data[1]
        elif kind == "edge":
            along = data.tangentAt((data.FirstParameter + data.LastParameter) / 2.)
        else:
            raise ValueError("Select one edge/axis or two points for X.")
    else:
        raise ValueError("Select one edge/axis or two points for X.")
    projected = along - normal * along.dot(normal)
    if projected.Length < 1e-9:
        raise ValueError("The X direction projects to zero on this plane.")
    return unit(projected)


def evaluate(component, values, operation=None):
    if values['mode'] == 'Enter values':
        position = App.Vector(*values['position'])
        if not all(math.isfinite(v) for v in values['position']):
            raise ValueError("Enter finite offsets.")
        normal = unit(App.Vector(*values['normal']))
        base = App.Placement(position, App.Rotation(App.Vector(0, 0, 1), normal))
    else:
        base = surface(component, values['references'], operation)
        normal = unit(base.Rotation.multVec(App.Vector(0, 0, 1)))
    if values['reverse_normal']:
        normal = -normal
    distance = values['offset']
    if not math.isfinite(distance):
        raise ValueError("Enter a finite offset distance.")
    anchor = base.Base + normal * distance
    reference = values.get('origin')
    if reference:
        kind, point = geometry(component, reference, operation)
        if kind != 'point':
            raise ValueError("Select the origin, a point or an edge endpoint.")
    else:
        point = App.Vector(*(values.get('stored_origin') or (0., 0., 0.)))
    projected = point - normal * ((point - anchor).dot(normal))
    along = axis(component, values['axis'], normal, operation)
    if not values['axis'] and values.get('stored_axis'):
        saved = App.Vector(*values['stored_axis'])
        along = unit(saved - normal * saved.dot(normal))
    if values['reverse_axis']:
        along = -along
    return App.Placement(projected, App.Rotation(along, normal.cross(along), normal, 'ZXY'))


def defaults():
    return dict(mode='Select geometry', references=[], position=(0., 0., 0.), normal=(0., 0., 1.),
                reverse_normal=False, offset=0., axis=[], reverse_axis=False, origin=None,
                stored_origin=None, stored_axis=None)


def links(references):
    return [(obj, [name]) for obj, name in references]


def references(links):
    return [(obj, names[0] if names else '') for obj, names in links]


def read(plane):
    helper = getattr(plane, 'ProjectedFrame', None)
    if helper and hasattr(helper, 'DefinitionMode'):
        return dict(mode=helper.DefinitionMode, references=references(helper.PlaneReferences),
                    position=tuple(helper.Position), normal=tuple(helper.Normal),
                    reverse_normal=helper.ReverseNormal, offset=helper.Distance.Value,
                    axis=references(helper.AxisReferences), reverse_axis=helper.ReverseAxis,
                    stored_origin=tuple(helper.StoredOrigin) if helper.UseStoredOrigin else None,
                    stored_axis=tuple(helper.StoredAxis) if helper.UseStoredAxis else None,
                    origin=references([helper.OriginReference])[0] if helper.OriginReference and helper.OriginReference[0] else None)
    values = defaults()
    if helper and hasattr(helper, 'Surface'):
        # Import the previous projected workflow while retaining its associations.
        support = references(helper.Surface.AttachmentSupport)
        # The legacy offset was applied before Z reversal; preserve that surface.
        distance = helper.Surface.AttachmentOffset.Base.z * (-1 if helper.ReverseZ else 1)
        values.update(references=support, offset=distance,
                      reverse_normal=helper.ReverseZ, axis=references(helper.AxisReferences),
                      reverse_axis=helper.ReverseX,
                      origin=references([helper.OriginReference])[0] if helper.OriginReference and helper.OriginReference[0] else None)
        if helper.Surface.AttachmentOffset.Rotation.Angle < 1e-9:
            return values
    # Legacy arbitrary attachment rotations can always be edited without a jump.
    values.update(mode='Enter values', position=tuple(plane.Placement.Base),
                  normal=tuple(plane.Placement.Rotation.multVec(App.Vector(0, 0, 1))),
                  stored_origin=tuple(plane.Placement.Base),
                  stored_axis=tuple(plane.Placement.Rotation.multVec(App.Vector(1, 0, 0))),
                  references=[], offset=0., reverse_normal=False, axis=[], reverse_axis=False, origin=None)
    return values


class PlaneDefinition(Model.PersistentProxy):
    def execute(self, helper):
        values = dict(mode=helper.DefinitionMode, references=references(helper.PlaneReferences),
                      position=tuple(helper.Position), normal=tuple(helper.Normal), reverse_normal=helper.ReverseNormal,
                      offset=helper.Distance.Value, axis=references(helper.AxisReferences), reverse_axis=helper.ReverseAxis,
                      stored_origin=tuple(helper.StoredOrigin) if helper.UseStoredOrigin else None,
                      stored_axis=tuple(helper.StoredAxis) if helper.UseStoredAxis else None,
                      origin=references([helper.OriginReference])[0] if helper.OriginReference and helper.OriginReference[0] else None)
        try:
            placement = evaluate(Model.owner(helper), values)
        except Exception:
            helper.Shape = Part.Shape()
            raise
        helper.Shape = Part.makePlane(1, 1)
        helper.Placement = placement


def apply(component, values, plane=None):
    placement = evaluate(component, values, plane)
    doc = component.Document
    with Model.transaction(doc, 'Edit Datum Plane' if plane else 'New Datum Plane'):
        old = getattr(plane, 'ProjectedFrame', None) if plane else None
        helper = old if old and hasattr(old, 'DefinitionMode') else doc.addObject('Part::FeaturePython', 'PlaneDefinition')
        if helper != old:
            component.addObject(helper)
            Model._identity(helper, 'Internal')
        fields = (('String', 'DefinitionMode', values['mode']), ('LinkSubList', 'PlaneReferences', links(values['references'])),
                  ('Vector', 'Position', App.Vector(*values['position'])),
                  ('Vector', 'Normal', unit(App.Vector(*values['normal'])) if values['mode'] == 'Enter values' else App.Vector(0, 0, 1)),
                  ('Bool', 'ReverseNormal', values['reverse_normal']), ('Distance', 'Distance', values['offset']),
                  ('LinkSubList', 'AxisReferences', links(values['axis'])), ('Bool', 'ReverseAxis', values['reverse_axis']),
                  ('Bool', 'UseStoredOrigin', bool(values.get('stored_origin'))),
                  ('Vector', 'StoredOrigin', App.Vector(*(values.get('stored_origin') or (0., 0., 0.)))),
                  ('Bool', 'UseStoredAxis', bool(values.get('stored_axis'))),
                  ('Vector', 'StoredAxis', App.Vector(*(values.get('stored_axis') or (1., 0., 0.)))),
                  ('LinkSub', 'OriginReference', links([values['origin']])[0] if values['origin'] else (None, [])))
        for kind, name, value in fields:
            if name in helper.PropertiesList:
                setattr(helper, name, value)
            else:
                Model._property(helper, kind, name, value)
        helper.Proxy = PlaneDefinition()
        if plane is None:
            import PartDesign
            plane = doc.addObject('PartDesign::Plane', 'Plane')
            Model.register_object(component, plane)
            plane.Label = Model.next_label(component, 'Plane', plane)
        if 'ProjectedFrame' in plane.PropertiesList:
            plane.ProjectedFrame = helper
        else:
            Model._property(plane, 'Link', 'ProjectedFrame', helper, True)
        plane.AttachmentSupport = [(helper, '')]
        plane.MapMode = 'ObjectXY'
        plane.AttachmentOffset = App.Placement()
        doc.recompute()
        if 'Invalid' in plane.State or 'Invalid' in helper.State:
            raise ValueError('The plane definition could not recompute.')
        if App.GuiUp:
            helper.Visibility = False
            helper.ViewObject.ShowInTree = False
        if old and old != helper:
            old_surface = getattr(old, 'Surface', None)
            if not any(obj != component for obj in old.InList):
                doc.removeObject(old.Name)
                if old_surface and not any(obj != component for obj in old_surface.InList):
                    doc.removeObject(old_surface.Name)
    return plane
