# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component-owned, associative construction planes, without an internal Body."""
import math

import FreeCAD as App
import Part

from . import document, geometry, modeling

EPS = 1e-7


class IncompletePlane(ValueError):
    """Valid partial input that needs another reference, rather than correction."""


def unit(vector):
    if vector.Length < EPS:
        raise ValueError('The selected direction has zero length')
    return vector / vector.Length


def flatten(values):
    return [(obj, sub) for obj, subs in values for sub in subs or ('',)]


def links(refs):
    return [(obj, [sub]) for obj, sub in refs]


def canonical(definition, refs):
    """Validate original occurrence paths before reducing to owned source links."""
    geometry.require_modeling_inputs(definition, refs)
    result = []
    for obj, sub in refs:
        target = obj.getSubObject(sub, 1) if sub else obj
        if target is None or target == definition or document.owned_path(definition, target) is None:
            raise ValueError('Use geometry owned by the edited component; add reference geometry first')
        # Native parser handles mapped topology names, which may contain dots.
        _, mapped, element = Part.splitSubname(sub)
        element = Part.joinSubname('', mapped, element)
        pair = (target, element)
        if pair not in result:
            result.append(pair)
    return result


def shape(definition, ref):
    obj, sub = ref
    path = document.owned_path(definition, obj)
    if path is None:
        raise ValueError('A plane reference is no longer owned by this component')
    route = ''.join(child.Name + '.' for child in path) + sub
    # getShape includes the definition Placement; remove that outer frame.
    value = Part.getShape(definition, route, needSubElement=True)
    if value.isNull():
        raise ValueError('A plane reference is missing or no longer has geometry')
    value = value.copy()
    value.Placement = definition.Placement.inverse().multiply(value.Placement)
    return value


def describe(definition, ref):
    value = shape(definition, ref)
    if value.ShapeType == 'Vertex':
        return ('point', value.Point)
    if value.ShapeType == 'Edge' and isinstance(value.Curve, (Part.Line, Part.LineSegment)):
        # Datum lines can have infinite parameter bounds. Any point on their
        # underlying straight line defines the same support without overflow.
        return ('line', value.valueAt(0), unit(value.tangentAt(0)))
    if value.ShapeType == 'Face' and isinstance(value.Surface, Part.Plane):
        # Fundamental planes can have effectively infinite UV bounds. Sampling
        # a bound amplifies roundoff after rotations; (0, 0) is always on the
        # underlying plane even when it lies outside a trimmed face boundary.
        return ('plane', value.valueAt(0, 0), unit(value.normalAt(0, 0)))
    raise ValueError('Select a planar face, plane, straight edge, line or point')


def base_plane(definition, refs, normal_to_line=True):
    items = [describe(definition, ref) for ref in refs]
    kinds = [item[0] for item in items]
    if kinds == ['plane']:
        return items[0][1:]
    if 'plane' in kinds:
        raise ValueError('Use a plane or planar face by itself; remove the other references.')
    if not kinds:
        raise IncompletePlane('Choose a plane or planar face, or start with points or straight lines.')
    if kinds == ['point']:
        raise IncompletePlane('1 point selected — pick two more points or a line / straight edge.')
    if kinds == ['point', 'point']:
        if (items[1][1] - items[0][1]).Length < EPS:
            raise ValueError('The points coincide; choose distinct points.')
        raise IncompletePlane('2 points selected — pick a third point off their line.')
    if kinds == ['line']:
        raise IncompletePlane('1 line selected — pick a point / vertex or another coplanar line.')
    if kinds == ['point', 'point', 'point']:
        a, b, c = [item[1] for item in items]
        if (b-a).cross(c-a).Length < EPS:
            raise ValueError('The points are collinear or coincident; choose three noncollinear points.')
        return a, unit((b-a).cross(c-a))
    if sorted(kinds) == ['line', 'point']:
        line = next(item for item in items if item[0] == 'line')
        point = next(item[1] for item in items if item[0] == 'point')
        if normal_to_line:
            return point, line[2]
        if line[2].cross(point-line[1]).Length < EPS:
            raise ValueError('The point lies on the line; choose an off-line point.')
        return line[1], unit(line[2].cross(point-line[1]))
    if kinds == ['line', 'line']:
        a, b = items
        cross = a[2].cross(b[2])
        if cross.Length < EPS:
            cross = a[2].cross(b[1]-a[1])
        if cross.Length < EPS:
            raise ValueError('The lines coincide; choose distinct coplanar lines.')
        normal = unit(cross)
        if abs((b[1]-a[1]).dot(normal)) > EPS:
            raise ValueError('Skew lines do not define a plane')
        return a[1], normal
    raise ValueError('Select one plane/planar face, three points, a line and point, or two coplanar lines')


def collect(definition, refs, ref):
    """Keep supported partial/complete combinations; replace geometric conflicts.

    Callers admit the new reference before collecting it. Offset/frame errors
    are deliberately excluded from this decision.
    """
    describe(definition, ref)
    combined = list(refs) + [ref]
    try:
        base_plane(definition, combined)
    except IncompletePlane:
        pass
    except ValueError:
        return [ref]
    return combined


def saved_normal_to_line(feature):
    # Absence identifies the historical line-containing-plane construction.
    return getattr(feature, 'NormalToLine', False) if feature is not None else True


def solve(definition, refs, offset=0, origin_refs=(), axis_refs=(), axis='X', flipped=False,
          reversed_axis=False, normal_to_line=True):
    offset = float(offset)
    if not math.isfinite(offset):
        raise ValueError('Offset must be finite')
    anchor, base_normal = base_plane(definition, refs, normal_to_line)
    anchor = anchor + base_normal * offset
    normal = -base_normal if flipped else base_normal
    # Universal origin expressed in the stored component coordinate frame.
    point = definition.getGlobalPlacement().inverse().multVec(App.Vector())
    if normal_to_line and sorted(describe(definition, r)[0] for r in refs) == ['line', 'point']:
        point = anchor
    if origin_refs:
        if len(origin_refs) != 1:
            raise ValueError('Select one origin point')
        item = describe(definition, origin_refs[0])
        if item[0] != 'point':
            raise ValueError('Origin accepts a point only')
        point = item[1]
    origin = point - normal * (point-anchor).dot(normal)
    direction = None
    if axis_refs:
        items = [describe(definition, ref) for ref in axis_refs]
        if len(items) == 1 and items[0][0] == 'line':
            direction = items[0][2]
        elif len(items) == 2 and all(item[0] == 'point' for item in items):
            direction = items[1][1] - items[0][1]
        elif len(items) == 1 and items[0][0] == 'point':
            raise IncompletePlane('1 axis point selected — pick a second distinct point.')
        else:
            raise ValueError('Select one line/straight edge or two distinct points for the axis')
    if axis not in ('X', 'Y'):
        raise ValueError('Choose X or Y')
    if direction is None:
        candidates = [App.Vector(1,0,0), App.Vector(0,1,0), App.Vector(0,0,1)]
        if axis == 'Y':
            candidates[0], candidates[1] = candidates[1], candidates[0]
        direction = next(v for v in candidates if v.cross(normal).Length > EPS)
    direction = unit(direction - normal * direction.dot(normal))
    if reversed_axis:
        direction = -direction
    x, y = (direction, normal.cross(direction)) if axis == 'X' else (direction.cross(normal), direction)
    return App.Placement(origin, App.Rotation(x, y, normal, 'ZXY'))


def is_plane(obj):
    return getattr(obj, 'PlusPlaneVersion', None) == 1


def bounds(axis, flipped, reversed_axis=False):
    # Reversing Z preserves the displayed rectangle as well as its infinite plane.
    u, v = (-50 if flipped and axis == 'Y' else -10,
            -35 if flipped and axis == 'X' else -10)
    # Reversing the in-plane axes also preserves the finite display footprint.
    return (-60-u, -45-v) if reversed_axis else (u, v)


class Plane:
    def __init__(self, obj):
        obj.addProperty('App::PropertyInteger', 'PlusPlaneVersion', 'Plane').PlusPlaneVersion = 1
        obj.setEditorMode('PlusPlaneVersion', 2)
        for name in ('PlaneReferences', 'OriginPoint', 'AxisReferences'):
            # Body-owned feature faces are legal component inputs. Native Local
            # links would incorrectly restrict them to the same internal Body.
            obj.addProperty('App::PropertyLinkSubListGlobal', name, 'Plane')
        obj.addProperty('App::PropertyDistance', 'Offset', 'Plane')
        obj.addProperty('App::PropertyEnumeration', 'DefinedAxis', 'Plane').DefinedAxis = ['X', 'Y']
        obj.addProperty('App::PropertyBool', 'FlipNormal', 'Plane')
        obj.addProperty('App::PropertyBool', 'ReverseAxis', 'Plane')
        obj.addProperty('App::PropertyString', 'PlaneError', 'Plane')
        obj.setEditorMode('PlaneError', 1)
        obj.Proxy = self

    def execute(self, obj):
        owner = obj.getParentGeoFeatureGroup()
        try:
            placement = solve(owner, flatten(obj.PlaneReferences), obj.Offset.Value,
                              flatten(obj.OriginPoint), flatten(obj.AxisReferences),
                              obj.DefinedAxis, obj.FlipNormal, getattr(obj, 'ReverseAxis', False),
                              saved_normal_to_line(obj))
            u, v = bounds(obj.DefinedAxis, obj.FlipNormal, getattr(obj, 'ReverseAxis', False))
            obj.Shape = Part.makePlane(60, 45, App.Vector(u,v,0))
            obj.Placement = placement
            obj.PlaneError = ''
        except Exception as exc:
            obj.Shape = Part.Shape()
            obj.PlaneError = str(exc)
            raise

    def dumps(self):
        return None

    def loads(self, state):
        pass


class ViewPlane:
    def __init__(self, view):
        view.Proxy = self
        view.ShapeColor = (0.65, 0.40, 0.85)
        view.Transparency = 65

    def getIcon(self):
        return ':/icons/PartDesign_Plane.svg'

    def doubleClicked(self, view):
        from . import plane_task
        plane_task.show(view.Object)
        return True

    def dumps(self):
        return None

    def loads(self, state):
        pass


def save(doc, refs, offset=0, origin_refs=(), axis_refs=(), axis='X', flipped=False, feature=None,
         reversed_axis=False, normal_to_line=None, quantity_units=None):
    if normal_to_line is None:normal_to_line = saved_normal_to_line(feature)
    definition, path = modeling._context(doc)
    refs, origin_refs, axis_refs = [canonical(definition, values) for values in (refs, origin_refs, axis_refs)]
    if feature is not None:
        if not is_plane(feature) or feature not in definition.Group:
            raise ValueError('Edit a plane owned by this component')
        if any(obj == feature or obj in feature.InListRecursive for obj, _ in refs+origin_refs+axis_refs):
            raise ValueError('A plane cannot depend on itself or a downstream feature')
    document.require_predecessors(definition, feature, refs + origin_refs + axis_refs)
    solve(definition, refs, offset, origin_refs, axis_refs, axis, flipped, reversed_axis, normal_to_line)
    with document.transaction(definition.Document, 'Edit plane' if feature else 'Create plane'):
        if feature is None:
            feature = definition.newObject('Part::FeaturePython', 'Plane')
            Plane(feature)
            ViewPlane(feature.ViewObject)
        feature.PlaneReferences = links(refs)
        feature.OriginPoint = links(origin_refs)
        feature.AxisReferences = links(axis_refs)
        feature.Offset = offset
        from .quantity_fields import save as save_units
        save_units(feature, quantity_units)
        feature.DefinedAxis = axis
        feature.FlipNormal = flipped
        # Older version-1 planes acquire the additive property only on acceptance.
        if 'ReverseAxis' not in feature.PropertiesList:
            feature.addProperty('App::PropertyBool', 'ReverseAxis', 'Plane')
        feature.ReverseAxis = reversed_axis
        if 'NormalToLine' not in feature.PropertiesList:
            feature.addProperty('App::PropertyBool', 'NormalToLine', 'Plane')
            feature.setEditorMode('NormalToLine', 2)
        feature.NormalToLine = normal_to_line
        definition.Document.recompute()
        if feature.PlaneError or feature.Shape.isNull():
            raise ValueError(feature.PlaneError or 'Plane creation failed')
    return feature
