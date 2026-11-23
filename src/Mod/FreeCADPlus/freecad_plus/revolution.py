# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative Revolve: native Revolution tools, shared feature persistence."""
import math
import sys
import FreeCAD as App
import Part
from . import document, extrusion, modeling, planes

NAME = 'Revolve'
VERSION = 'PlusRevolveVersion'
PREFIX = 'Revolve_'
ERROR = 'RevolveError'
MODES = extrusion.MODES
AXES = ('Sketch vertical axis', 'Sketch horizontal axis', 'Component X axis',
        'Component Y axis', 'Component Z axis', 'Selected axis / line')
ENDS = ('Angle', 'Up to face', 'Through all')
LINKS = {'target': 'Target', 'start': 'StartReference', 'limit': 'EndReference',
         'secondlimit': 'SecondEndReference', 'axis': 'AxisReference'}
DEFAULTS = dict(output='Solid', operation='New Solid', start='Profile plane', start_offset=0.,
                sides='One side', end='Angle', angle=360., offset=0.,
                end2='Angle', angle2=45., offset2=0., reverse=False,
                axis='Sketch vertical axis', refine=True)
InvalidResult = extrusion.InvalidResult
profile_reference = extrusion.profile_reference
validate_profiles = extrusion.validate_profiles
region_references = extrusion.region_references
owner = extrusion.owner


def is_revolution(obj):
    return getattr(obj, VERSION, 0) == 1


def settings(feature):
    return {key: getattr(feature, PREFIX + key, default) for key, default in DEFAULTS.items()}


def references(feature):
    return {key: planes.flatten(getattr(feature, prop))[0]
            for key, prop in LINKS.items() if getattr(feature, prop)}


def validate(definition, refs, links, values, feature=None):
    v = dict(DEFAULTS, **values)
    for key in ('start_offset', 'angle', 'angle2', 'offset', 'offset2'):
        v[key] = float(v[key])
        if not math.isfinite(v[key]) or abs(v[key]) > 360:
            raise ValueError('Angles must be finite and within 360 degrees.')
    for key, choices in (('output', ('Solid', 'Sheet')), ('operation', MODES), ('start', ('Profile plane', 'Offset', 'Reference')),
                         ('sides', ('One side', 'Symmetric', 'Two sides')), ('end', ENDS),
                         ('end2', ENDS), ('axis', AXES)):
        if v[key] not in choices:
            raise ValueError('Unsupported Revolve setting: ' + key)
    refs = [profile_reference(ref) for ref in planes.canonical(definition, refs)]
    validate_profiles(definition, refs, v['output'])
    if v['output'] == 'Sheet':
        v['operation'] = 'New Solid'
        links = {key: ref for key, ref in links.items() if key != 'target'}
    links = {key: planes.canonical(definition, [ref])[0] for key, ref in links.items() if key in LINKS}
    if feature is not None:
        if not is_revolution(feature) or owner(feature) != definition:
            raise ValueError('Edit a Revolve owned by this component.')
        if any(obj == feature or obj in feature.InListRecursive for obj, _ in refs + list(links.values())):
            raise ValueError('Revolve cannot depend on itself or a downstream feature.')
    if v['operation'] == 'New Solid':
        links.pop('target', None)
    else:
        if 'target' not in links:
            raise ValueError('Select the target solid to modify.')
        target = links['target'][0]
        if feature and target == references(feature).get('target', (None, ''))[0]:
            if target.Shape.isNull() or not target.Shape.isValid() or len(target.Shape.Solids) != 1:
                raise ValueError('The saved target is no longer one valid solid.')
        else:
            modeling._target_body(definition, target)
        links['target'] = (target, '')
    for key, needed in (('axis', v['axis'] == 'Selected axis / line'), ('start', v['start'] == 'Reference')):
        if not needed:
            links.pop(key, None)
        elif key not in links:
            raise ValueError('Pick a rotation axis.' if key == 'axis' else 'Pick a start face or plane.')
    for suffix, key in (('', 'limit'), ('2', 'secondlimit')):
        if suffix and v['sides'] != 'Two sides':
            links.pop(key, None)
            continue
        if v['end' + suffix] == 'Angle' and v['angle' + suffix] <= 0:
            raise ValueError('Rotation angle must be greater than zero.')
        if v['end' + suffix] == 'Up to face':
            if key not in links:
                raise ValueError('Pick a limiting face or plane.')
        else:
            links.pop(key, None)
    if v['sides'] == 'Symmetric' and v['end'] != 'Angle':
        raise ValueError('Symmetric rotation requires an Angle end condition.')
    if v['sides'] == 'Two sides' and (v['end'] == 'Through all' or v['end2'] == 'Through all'):
        raise ValueError('Through all is a single full revolution.')
    if v['sides'] == 'Two sides' and v['end'] == v['end2'] == 'Angle' and v['angle'] + v['angle2'] > 360:
        raise ValueError('The two rotation angles must total at most 360 degrees.')
    document.require_predecessors(definition, feature, refs + list(links.values()))
    return refs, links, v


def rotation_axis(definition, refs, links, v):
    if v['axis'] == 'Selected axis / line':
        line = planes.describe(definition, links['axis'])
        if line[0] != 'line':
            raise ValueError('Rotation requires a straight edge or axis.')
        base, direction = line[1], line[2]
    elif v['axis'].startswith('Component'):
        base = App.Vector()
        direction = App.Vector(*{'Component X axis': (1, 0, 0), 'Component Y axis': (0, 1, 0),
                                'Component Z axis': (0, 0, 1)}[v['axis']])
    else:
        obj = refs[0][0]
        if not obj.isDerivedFrom('Sketcher::SketchObject'):
            raise ValueError('For a face profile, select a component axis or a straight reference.')
        frame = definition.getGlobalPlacement().inverse().multiply(obj.getGlobalPlacement())
        base = frame.Base
        direction = frame.Rotation.multVec(App.Vector(0, 1, 0) if v['axis'] == AXES[0] else App.Vector(1, 0, 0))
    return base, direction / direction.Length


def evaluate(definition, refs, links, values, feature=None):
    refs, links, v = validate(definition, refs, links, values, feature)
    if v['output'] == 'Sheet':
        return evaluate_sheet(definition, refs, links, v, feature)
    face, frame, edges = extrusion.profile_shape(definition, refs)
    base, direction = rotation_axis(definition, refs, links, v)
    normal = frame.Rotation.multVec(App.Vector(0, 0, 1))
    if abs(direction.dot(normal)) > 1e-7 or abs((base - frame.Base).dot(normal)) > 1e-6:
        raise ValueError('The rotation axis must lie in the profile plane.')
    start = 0.
    if v['start'] == 'Reference':
        reference = planes.describe(definition, links['start'])
        if (reference[0] != 'plane' or abs(reference[2].dot(direction)) > 1e-7
                or abs((base - reference[1]).dot(reference[2])) > 1e-6):
            raise ValueError('The start plane must contain the rotation axis.')
        start = math.degrees(math.atan2(direction.dot(normal.cross(reference[2])), normal.dot(reference[2])))
    if v['start'] != 'Profile plane':
        start += v['start_offset']
    face.rotate(base, direction, start)
    target = planes.shape(definition, links['target']) if 'target' in links else None
    sweep = -direction if v['reverse'] and v['sides'] != 'Symmetric' else direction
    with extrusion.kernel_document() as scratch:
        body = scratch.addObject('PartDesign::Body', 'EvaluationBody');body.AllowCompound = True
        axis = body.newObject('PartDesign::Feature', 'AxisSnapshot')
        axis.Shape = Part.makeLine(base, base + sweep)
        profile = body.newObject('PartDesign::Feature', 'ProfileSnapshot');profile.BaseFeature = None
        profile.Shape = extrusion.kernel_snapshot(face)
        rev = body.newObject('PartDesign::Revolution', 'Evaluation')
        rev.BaseFeature = None;rev.Profile = (profile, [])
        rev.ReferenceAxis = (axis, ['Edge1']);rev.Refine = v['refine']
        def angle_for(suffix, key, axis_direction):
            kind = v['end' + suffix]
            if kind == 'Through all':return 360.
            if kind == 'Angle':return v['angle' + suffix]
            limit = planes.describe(definition, links[key])
            if (limit[0] != 'plane' or abs(limit[2].dot(axis_direction)) > 1e-7
                    or abs((base - limit[1]).dot(limit[2])) > 1e-6):
                raise ValueError('The angular limit must be a plane containing the rotation axis.')
            current_normal = face.Faces[0].normalAt(0, 0)
            angle = math.degrees(math.atan2(axis_direction.dot(current_normal.cross(limit[2])),
                                           current_normal.dot(limit[2]))) % 180.
            if angle < 1e-7:raise ValueError('The start and limit planes coincide; specify a rotation angle.')
            angle += v['offset' + suffix]
            if not 1e-7 < angle <= 360:raise ValueError('The limit and offset must produce an angle between 0 and 360 degrees.')
            return angle
        first = angle_for('', 'limit', sweep)
        second = angle_for('2', 'secondlimit', -sweep) if v['sides'] == 'Two sides' else 0.
        if first + second > 360 + 1e-7:raise ValueError('The two rotation angles must total at most 360 degrees.')
        rev.Type = 'TwoAngles' if v['sides'] == 'Two sides' else 'Angle'
        rev.Angle = first;rev.Angle2 = second
        rev.Midplane = v['sides'] == 'Symmetric'
        scratch.recompute()
        tool = rev.AddSubShape.copy();tool.Placement = rev.Placement.multiply(tool.Placement)
        if tool.isNull() or not tool.isValid() or not tool.Solids:
            raise ValueError('The revolution cannot be constructed; check the axis and profile.')
        tool = extrusion.name_tool(tool, refs, feature, target, 'PlusRevolve1')
    try:
        result = tool if target is None else target.fuse(tool) if v['operation'] == 'Add' else target.cut(tool)
        if v['refine']:result = result.removeSplitter()
        if result.isNull() or not result.isValid() or len(result.Solids) != 1:
            raise ValueError('The operation must produce one solid; check profile and target contact.')
        if target is not None and abs(result.Volume - target.Volume) < max(1e-7, target.Volume * 1e-10):
            raise ValueError('No material is ' + ('added.' if v['operation'] == 'Add' else 'removed.'))
    except Exception as exc:
        raise InvalidResult(str(exc), tool) from exc
    return result, tool, edges


def evaluate_sheet(definition, refs, links, v, feature):
    """Revolve native wires without filling the profile or capping the result."""
    obj = refs[0][0]
    selected = [planes.shape(definition, ref) for ref in refs]
    if obj.isDerivedFrom('Sketcher::SketchObject') and any(not sub for _, sub in refs):
        selected = [planes.shape(definition, (obj, ''))]
    edges = []
    for shape in selected:
        for edge in shape.Edges:
            if not any(edge.isSame(old) for old in edges):edges.append(edge)
    if not edges:raise ValueError('The profile contains no curves.')
    profile = Part.makeCompound([Part.Wire(group) for group in Part.sortEdges(edges)])
    base, axis = rotation_axis(definition, refs, links, v)
    if obj.isDerivedFrom('Sketcher::SketchObject'):
        frame = definition.getGlobalPlacement().inverse().multiply(obj.getGlobalPlacement())
        origin, normal = frame.Base, frame.Rotation.multVec(App.Vector(0, 0, 1))
    else:
        plane = profile.findPlane()
        if plane is not None:
            origin, normal = plane.Position, plane.Axis
        else:
            origin = profile.Vertexes[0].Point
            normal = (origin - base).cross(axis)
            if normal.Length < 1e-7:
                normal = next(((vertex.Point - base).cross(axis) for vertex in profile.Vertexes
                               if (vertex.Point - base).cross(axis).Length > 1e-7), App.Vector())
            if normal.Length < 1e-7:raise ValueError('The curves lie on the rotation axis and cannot create a sheet.')
            normal.normalize()
            projected = profile.copy()
            projected.Placement = App.Placement(App.Vector(), App.Rotation(normal, App.Vector(0, 0, 1))).multiply(projected.Placement)
            if projected.BoundBox.ZLength > 1e-6:
                raise ValueError('The curves and rotation axis must share one plane.')
    if abs(axis.dot(normal)) > 1e-7 or abs((base - origin).dot(normal)) > 1e-6:
        raise ValueError('The rotation axis must lie in the profile plane.')
    start = 0.
    if v['start'] == 'Reference':
        reference = planes.describe(definition, links['start'])
        if (reference[0] != 'plane' or abs(reference[2].dot(axis)) > 1e-7
                or abs((base - reference[1]).dot(reference[2])) > 1e-6):
            raise ValueError('The start plane must contain the rotation axis.')
        start = math.degrees(math.atan2(axis.dot(normal.cross(reference[2])), normal.dot(reference[2])))
    if v['start'] != 'Profile plane':start += v['start_offset']
    profile.rotate(base, axis, start)
    normal = App.Rotation(axis, start).multVec(normal)
    sweep = -axis if v['reverse'] and v['sides'] != 'Symmetric' else axis
    def angle_for(suffix, key, direction):
        kind = v['end' + suffix]
        if kind == 'Through all':return 360.
        if kind == 'Angle':return v['angle' + suffix]
        limit = planes.describe(definition, links[key])
        if (limit[0] != 'plane' or abs(limit[2].dot(direction)) > 1e-7
                or abs((base - limit[1]).dot(limit[2])) > 1e-6):
            raise ValueError('The angular limit must be a plane containing the rotation axis.')
        angle = math.degrees(math.atan2(direction.dot(normal.cross(limit[2])), normal.dot(limit[2]))) % 180.
        if angle < 1e-7:raise ValueError('The start and limit planes coincide; specify a rotation angle.')
        angle += v['offset' + suffix]
        if not 1e-7 < angle <= 360:raise ValueError('The limit and offset must produce an angle between 0 and 360 degrees.')
        return angle
    first = angle_for('', 'limit', sweep)
    second = angle_for('2', 'secondlimit', -sweep) if v['sides'] == 'Two sides' else 0.
    if first + second > 360 + 1e-7:raise ValueError('The two rotation angles must total at most 360 degrees.')
    if v['sides'] == 'Symmetric':profile.rotate(base, sweep, -first / 2)
    elif second:profile.rotate(base, sweep, -second)
    result = extrusion.kernel_snapshot(profile).revolve(base, sweep, first + second)
    if v['refine']:result = result.removeSplitter()
    if result.isNull() or not result.isValid() or not result.Faces or result.Solids or result.Area < 1e-9:
        raise ValueError('The sheet revolution is degenerate; check the curves and rotation axis.')
    result = extrusion.name_tool(result, refs, feature, namespace='PlusRevolveSheet1')
    return result, result.copy(), edges


class Revolve(extrusion.Extrude):
    @staticmethod
    def engine():
        return sys.modules[__name__]


class ViewRevolve(extrusion.ViewExtrude):
    def getIcon(self):
        return ':/icons/PartDesign_Revolution.svg'

    def doubleClicked(self, view):
        from . import revolve_task
        revolve_task.show(view.Object)
        return True


Feature = Revolve
ViewFeature = ViewRevolve


def save(doc, refs, links, values, feature=None):
    return extrusion.save_feature(doc, refs, links, values, feature, sys.modules[__name__])
