# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative, feature-centered Extrude, using the native extrusion kernel.

The evaluator owns a hidden, temporary document, never a transaction or an object
in the user's document. Preview and execution use exactly the same evaluator.
Saved references are native links; the result retains its identity across edits.
"""
import math
import sys
from contextlib import contextmanager

import FreeCAD as App
import Part

from . import document, editing, modeling, planes

NAME = 'Extrude'
VERSION = 'PlusExtrudeVersion'
PREFIX = 'Extrude_'
ERROR = 'ExtrudeError'

MODES = ('New Solid', 'Add', 'Subtract')
ENDS = ('Length', 'Up to face', 'Up to shape', 'To first', 'To last', 'Through all')
LINKS = {'target': 'Target', 'start': 'StartReference', 'limit': 'EndReference',
         'secondlimit': 'SecondEndReference', 'direction': 'DirectionReference'}
DEFAULTS = dict(output='Solid', operation='New Solid', start='Profile plane', start_offset=0.,
                sides='One side', end='Length', length=8., offset=0.,
                end2='Length', length2=3., offset2=0., reverse=False,
                direction='Profile normal', measure='Along direction',
                taper=0., taper2=0., refine=True)


def is_extrusion(obj):
    return getattr(obj, 'PlusExtrudeVersion', 0) == 1


def settings(feature):
    return {key: getattr(feature, 'Extrude_' + key, default) for key, default in DEFAULTS.items()}


def references(feature):
    return {key: planes.flatten(getattr(feature, prop))[0]
            for key, prop in LINKS.items() if getattr(feature, prop)}


def owner(feature):
    body = feature.getParentGeoFeatureGroup()
    return body.getParentGeoFeatureGroup()


def validate(definition, refs, links, values, feature=None):
    values = dict(DEFAULTS, **values)
    for key in ('start_offset', 'length', 'length2', 'offset', 'offset2', 'taper', 'taper2'):
        values[key] = float(values[key])
        if not math.isfinite(values[key]):
            raise ValueError('Extrude values must be finite')
    for key, choices in (('output', ('Solid', 'Sheet')), ('operation', MODES), ('start', ('Profile plane', 'Offset', 'Reference')),
                         ('sides', ('One side', 'Symmetric', 'Two sides')), ('end', ENDS), ('end2', ENDS),
                         ('direction', ('Profile normal', 'Selected axis / line')),
                         ('measure', ('Along direction', 'Along profile normal'))):
        if values[key] not in choices:
            raise ValueError('Unknown Extrude setting: ' + key)
    if not refs:
        raise ValueError('Select a sketch or a closed region to extrude.')
    refs = planes.canonical(definition, refs)
    refs = [profile_reference(ref) for ref in refs]
    validate_profiles(definition, refs, values['output'])
    if values['output'] == 'Sheet':
        values['operation'] = 'New Solid'  # Keep the saved operation identifier compatible.
        links = {key: ref for key, ref in links.items() if key != 'target'}
    links = {key: planes.canonical(definition, [ref])[0] for key, ref in links.items()}
    if feature is not None:
        if not is_extrusion(feature) or owner(feature) != definition:
            raise ValueError('Edit an Extrude owned by this component.')
        if any(obj == feature or obj in feature.InListRecursive for obj, sub in refs + list(links.values())):
            raise ValueError('Extrude cannot depend on itself or a downstream feature.')
    if values['operation'] != 'New Solid':
        if 'target' not in links:
            raise ValueError('Select the target solid to modify.')
        target = links['target'][0]
        if feature is not None and target == references(feature).get('target', (None, ''))[0]:
            # The saved predecessor is intentionally no longer the Body Tip.
            if target.Shape.isNull() or not target.Shape.isValid() or len(target.Shape.Solids) != 1:
                raise ValueError('The saved target is no longer one valid solid.')
        else:
            modeling._target_body(definition, target)
        links['target'] = (target, '')
    else:
        links.pop('target', None)
    if values['start'] != 'Reference':
        links.pop('start', None)
    elif 'start' not in links:
        raise ValueError('Pick a start face or plane.')
    if values['direction'] == 'Profile normal':
        links.pop('direction', None)
    elif 'direction' not in links:
        raise ValueError('Pick a straight edge or axis for the direction.')
    for suffix, key in (('', 'limit'), ('2', 'secondlimit')):
        if suffix and values['sides'] != 'Two sides':
            links.pop(key, None)
            continue
        kind = values['end' + suffix]
        if kind == 'Length' and values['length' + suffix] <= 0:
            raise ValueError('Length must be greater than zero.')
        if abs(values['taper' + suffix]) >= 90:
            raise ValueError('Taper must be between -90 and 90 degrees.')
        if kind in ('Up to face', 'Up to shape'):
            if key not in links:
                raise ValueError('Pick a limiting face, plane or shape.')
        else:
            links.pop(key, None)
        if kind in ('To first', 'To last', 'Through all') and 'target' not in links:
            raise ValueError('This end condition needs an explicit target solid.')
        if kind != 'Length' and values['taper' + suffix]:
            raise ValueError('Taper requires a Length end condition.')
    document.require_predecessors(definition, feature, refs + list(links.values()))
    return refs, links, values


def profile_reference(ref):
    obj, sub = ref
    if obj.TypeId == 'PartDesign::Body' and Part.splitSubname(sub)[2].startswith(('Face', 'Edge')):
        if obj.Tip is None:
            raise ValueError('The selected body has no result face.')
        # The Body adds its own topology-name prefix. Resolve that mapped pick
        # on the Body first, then store the corresponding Tip face reference.
        # Keeping the Body prefix on the Tip produces a missing subelement.
        shape = obj.Shape
        picked = shape.getElement(sub)
        kind = picked.ShapeType
        elements = shape.Faces if kind == 'Face' else shape.Edges
        index = next((i for i, element in enumerate(elements) if element.isSame(picked)), None)
        if index is None:
            raise ValueError('The selected result face is no longer available.')
        return (obj.Tip, kind + str(index + 1))
    return ref


def validate_profiles(definition, refs, output='Solid'):
    """Sketch curves or one real face; datum faces are reference geometry only."""
    if not refs:
        raise ValueError('Select a sketch, closed sketch region, or face.')
    obj, sub = refs[0]
    if obj.isDerivedFrom('Sketcher::SketchObject'):
        if any(other != obj or (element and not Part.splitSubname(element)[2].startswith('Edge'))
               for other, element in refs):
            raise ValueError('Select a whole sketch or closed curves from one sketch.')
    elif output == 'Sheet':
        if (not obj.isDerivedFrom('Part::Feature') or obj.TypeId in (
                'PartDesign::Plane', 'PartDesign::Line', 'PartDesign::Point',
                'Part::DatumPlane', 'Part::DatumLine', 'Part::DatumPoint')
                or any(other != obj for other, _ in refs)):
            raise ValueError('Select sketch curves, edges or a face from one object for Sheet.')
        for ref in refs:
            shape = planes.shape(definition, ref)
            if not shape.Edges or (shape.Faces and (len(refs) != 1 or shape.ShapeType != 'Face')):
                raise ValueError('Select curves or a face boundary, not an entire solid or sheet.')
    elif (len(refs) != 1 or not obj.isDerivedFrom('Part::Feature')
          or obj.isDerivedFrom('PartDesign::Plane')
          or not Part.splitSubname(sub)[2].startswith('Face')
          or planes.shape(definition, refs[0]).ShapeType != 'Face'):
        raise ValueError('Select a sketch or a face of a solid or sheet.')


def profile_shape(definition, refs):
    sketch = refs[0][0]
    if not sketch.isDerivedFrom('Sketcher::SketchObject'):
        face = planes.shape(definition, refs[0])
        if not isinstance(face.Surface, Part.Plane):
            raise ValueError('Select a planar profile face.')
        normal = face.normalAt(0, 0)
        placement = App.Placement(face.CenterOfMass, App.Rotation(App.Vector(0, 0, 1), normal))
        return face, placement, face.Edges
    placement = definition.getGlobalPlacement().inverse().multiply(sketch.getGlobalPlacement())
    if any(not sub for _, sub in refs):
        edges = planes.shape(definition, (sketch, '')).Edges
    else:
        edges = []
        for ref in refs:
            for edge in planes.shape(definition, ref).Edges:
                if not any(edge.isSame(existing) for existing in edges):
                    edges.append(edge)
    if not edges:
        raise ValueError('The profile contains no curves.')
    wires = [Part.Wire(group) for group in Part.sortEdges(edges)]
    if any(not wire.isClosed() for wire in wires):
        raise ValueError('The selected curves are open; choose Sheet or complete a closed region.')
    face = Part.makeFace(wires, 'Part::FaceMakerBullseye')
    if face.isNull() or not face.isValid() or not face.Faces:
        raise ValueError('The profile must enclose valid planar regions without self-intersections.')
    normal = placement.Rotation.multVec(App.Vector(0, 0, 1))
    if any(abs(abs(f.normalAt(0, 0).dot(normal)) - 1) > 1e-7 for f in face.Faces):
        raise ValueError('The selected curves must lie on the sketch plane.')
    return face, placement, edges


def region_references(definition, sketch, point):
    """Return native edge links for the bounded sketch region under a point.

    Nested loops partition the sketch into a ring and its inner region. Store
    the actual boundary references, not a transient face index or a mouse point.
    Open curves are ignored here and remain selectable through the curve picker.
    """
    planes.canonical(definition, [(sketch, '')])
    shape = planes.shape(definition, (sketch, ''))
    wires = [Part.Wire(group) for group in Part.sortEdges(shape.Edges)]
    loops = [(wire, Part.Face(wire)) for wire in wires if wire.isClosed()]
    containers = [(wire, face) for wire, face in loops if face.isInside(point, 1e-7, True)]
    if not containers:
        raise ValueError('Click inside a closed sketch region.')
    outer, face = min(containers, key=lambda item: item[1].Area)
    inner = [(wire, candidate) for wire, candidate in loops if candidate.Area < face.Area
             and face.common(candidate).Area >= candidate.Area - 1e-7]
    holes = [wire for wire, candidate in inner if not any(
        other.Area > candidate.Area and other.common(candidate).Area >= candidate.Area - 1e-7
        for _, other in inner)]
    boundary = [edge for wire in [outer, *holes] for edge in wire.Edges]
    return [(sketch, 'Edge' + str(index + 1)) for index, edge in enumerate(shape.Edges)
            if any(edge.isSame(bound) for bound in boundary)]


@contextmanager
def kernel_document():
    active = App.ActiveDocument
    scratch = App.newDocument('ExtrudeEvaluation', hidden=True, temp=True)
    scratch.UndoMode = 0
    try:
        yield scratch
    finally:
        App.closeDocument(scratch.Name)
        if active is not None and active.Name in App.listDocuments() and App.ActiveDocument != active:
            App.setActiveDocument(active.Name)


def shape_limit_face(profile, limit, direction):
    """Find the first boundary cut by the footprint, ignoring side walls.

Passing an entire closed solid to native UpToShape can leave a closed shell
which OCC cannot extend to. Resolve its forward boundary geometrically, then
let the native until-face solver construct and validate the cap.
    """
    span = max((limit.BoundBox.getPoint(i) - profile.CenterOfMass).dot(direction) for i in range(8))
    if span <= 1e-7:
        raise ValueError('The limiting shape is behind the profile; reverse direction.')
    probe = profile.extrude(direction * (span + max(1., limit.BoundBox.DiagonalLength * .01)))
    candidates = []
    for face in limit.Faces:
        contact = face.common(probe)
        if contact.Area > 1e-7:
            distance = (contact.CenterOfMass - profile.CenterOfMass).dot(direction)
            if distance > 1e-7:
                candidates.append((distance, face))
    if not candidates:
        raise ValueError('The profile does not reach the limiting shape.')
    return min(candidates, key=lambda item: item[0])[1]


def kernel_snapshot(shape):
    # Scratch inputs are geometry snapshots, not cross-document named links.
    # Do not mix the owning document's element-name table with scratch IDs.
    # A plain copy retains cached child maps even after clearing the root map.
    # The native BRep round trip retains exact geometry and placements while
    # dropping all temporary naming metadata, including cached child maps.
    result = Part.Shape()
    result.importBrepFromString(shape.exportBrepToString())
    return Part.cast_to_shape(result)


def name_tool(tool, refs, feature, target=None, namespace='PlusExtrude1'):
    """Publish names independent of temporary document/object IDs.

    Native Boolean history then propagates these tool names and the target's
    existing names. Include the profile selection and topology layout so an
    incompatible profile/topology change invalidates references instead of
    reusing names from a different layout. Dimensional changes keep the names.
    """
    sketch = refs[0][0]
    tool = kernel_snapshot(tool)
    tool.Hasher = target.Hasher if target is not None and target.Hasher is not None else sketch.Shape.Hasher
    tool.Tag = feature.ID if feature else sketch.ID
    selection = '_'.join(Part.splitSubname(sub)[2] or 'Whole' for _, sub in refs)
    layout = '_'.join(type(face.Surface).__name__ + str(len(face.Edges)) + 'w' + str(len(face.Wires))
                      for face in tool.Faces)
    prefix = '%s_%s_%s_%s_%s_' % (namespace, sketch.ID, selection, len(tool.Vertexes), layout)
    tool.ElementMap = {prefix + kind + str(i + 1): kind + str(i + 1)
                       for kind, elements in (('Face', tool.Faces), ('Edge', tool.Edges), ('Vertex', tool.Vertexes))
                       for i in range(len(elements))}
    return tool


class InvalidResult(ValueError):
    """A constructible native tool whose final operation is invalid."""
    def __init__(self, message, tool):
        super().__init__(message)
        self.tool = tool


def evaluate(definition, refs, links, values, feature=None):
    refs, links, v = validate(definition, refs, links, values, feature)
    if v['output'] == 'Sheet':
        return evaluate_sheet(definition, refs, links, v, feature)
    face, placement, edges = profile_shape(definition, refs)
    normal = placement.Rotation.multVec(App.Vector(0, 0, 1))
    direction = normal
    if 'direction' in links:
        line = planes.describe(definition, links['direction'])
        if line[0] != 'line':
            raise ValueError('Direction requires a straight edge or axis.')
        direction = line[2]
    if v['reverse']:
        direction = -direction
    factor = abs(normal.dot(direction))
    if factor < 1e-7:
        raise ValueError('The direction must leave the profile plane.')
    shift = 0.
    if v['start'] == 'Reference':
        start = planes.describe(definition, links['start'])
        if start[0] != 'plane' or abs(abs(start[2].dot(normal)) - 1) > 1e-7:
            raise ValueError('Choose a start face or plane parallel to the profile.')
        shift = (start[1] - placement.Base).dot(start[2]) / direction.dot(start[2])
    if v['start'] != 'Profile plane':
        shift += v['start_offset']
    face.translate(direction * shift)
    target = planes.shape(definition, links['target']) if 'target' in links else None
    with kernel_document() as scratch:
        body = scratch.addObject('PartDesign::Body', 'EvaluationBody')
        body.AllowCompound = True
        base = None
        if target is not None:
            base = body.newObject('PartDesign::Feature', 'TargetSnapshot')
            base.Shape = kernel_snapshot(target)
        profile = body.newObject('PartDesign::Feature', 'ProfileSnapshot')
        profile.BaseFeature = None
        profile.Shape = kernel_snapshot(face)
        # Native Pad accepts a planar face profile and computes its normal.
        pad = body.newObject('PartDesign::Pad', 'Evaluation')
        pad.BaseFeature = base
        pad.Profile = (profile, [])
        pad.UseCustomVector = True
        pad.Direction = direction
        pad.AlongSketchNormal = v['measure'] == 'Along profile normal'
        pad.SideType = v['sides']
        pad.Refine = v['refine']
        for suffix, key in (('', 'limit'), ('2', 'secondlimit')):
            if suffix and v['sides'] != 'Two sides':
                continue
            kind = v['end' + suffix]
            length = v['length' + suffix]
            if kind == 'Through all':
                # Native Pad lacks Pocket's ThroughAll enum. Bound the prism
                # with the target's corners in the actual chosen direction.
                axis = -direction if suffix else direction
                distances = [(target.BoundBox.getPoint(i) - face.CenterOfMass).dot(axis) for i in range(8)]
                length = max(distances) + max(1., target.BoundBox.DiagonalLength * .01)
                if v['sides'] == 'Symmetric':
                    length = 2 * (max(abs(distance) for distance in distances)
                                  + max(1., target.BoundBox.DiagonalLength * .01))
                if length <= 0:
                    raise ValueError('The target is behind the extrusion; reverse direction.')
                if v['measure'] == 'Along profile normal':
                    length *= factor
                kind = 'Length'
            setattr(pad, 'Type' + suffix, {'Up to face': 'UpToFace', 'Up to shape': 'UpToShape',
                                          'To first': 'UpToFirst', 'To last': 'UpToLast'}.get(kind, kind))
            setattr(pad, 'Length' + suffix, length)
            setattr(pad, 'Offset' + suffix, v['offset' + suffix])
            setattr(pad, 'TaperAngle' + suffix, v['taper' + suffix])
            if key in links:
                limit = body.newObject('PartDesign::Feature', 'LimitSnapshot')
                limit.BaseFeature = None
                limit.Shape = kernel_snapshot(planes.shape(definition, links[key]))
                if kind == 'Up to shape' and limit.Shape.Solids:
                    limit.Shape = shape_limit_face(kernel_snapshot(face), limit.Shape, -direction if suffix else direction)
                    kind = 'Up to face'
                    setattr(pad, 'Type' + suffix, 'UpToFace')
                if kind == 'Up to face':
                    if len(limit.Shape.Faces) != 1:
                        raise ValueError('Select one limiting face or plane.')
                    setattr(pad, 'UpToFace' + suffix, (limit, ['Face1']))
                else:
                    setattr(pad, 'UpToShape' + suffix, [(limit, [''])])
        body.Tip = pad
        scratch.recompute()
        # Native Pad writes its tool before fusion. We evaluate the selected
        # Boolean ourselves, so a failed additive fuse is irrelevant to a cut.
        tool = pad.AddSubShape.copy()
        tool.Placement = pad.Placement.multiply(tool.Placement)
        if tool.isNull() or not tool.isValid() or not tool.Solids:
            raise ValueError('The extrusion cannot reach its end. Check profile, direction, limit and taper.')
        tool = name_tool(tool, refs, feature, target)
    try:
        result = tool if target is None else (target.fuse(tool) if v['operation'] == 'Add' else target.cut(tool))
        if v['refine']:
            result = result.removeSplitter()
        if result.isNull() or not result.isValid() or len(result.Solids) != 1:
            raise ValueError('The operation must produce one solid; check profile and target contact.')
        if target is not None and abs(result.Volume - target.Volume) < max(1e-7, target.Volume * 1e-10):
            raise ValueError('No material is ' + ('added.' if v['operation'] == 'Add' else 'removed.'))
    except Exception as exc:
        # Preserve this evaluation's tool for display, never a successful result
        # or a second evaluation with different operation/limit inputs.
        raise InvalidResult(str(exc), tool) from exc
    return result, tool, edges


def evaluate_sheet(definition, refs, links, v, feature):
    """Extrude uncapped wires with the native Part kernel, never a thin solid."""
    obj = refs[0][0]
    selected = [planes.shape(definition, ref) for ref in refs]
    if obj.isDerivedFrom('Sketcher::SketchObject') and any(not sub for _, sub in refs):
        selected = [planes.shape(definition, (obj, ''))]
    edges = []
    for shape in selected:
        for edge in shape.Edges:
            if not any(edge.isSame(old) for old in edges):
                edges.append(edge)
    if not edges:
        raise ValueError('The profile contains no curves.')
    wires = [Part.Wire(group) for group in Part.sortEdges(edges)]
    if (v['taper'] or (v['sides'] == 'Two sides' and v['taper2'])) and any(not wire.isClosed() for wire in wires):
        raise ValueError('Sheet taper requires closed profile curves; use zero taper for open curves.')
    profile = Part.makeCompound(wires)
    normal = None
    if obj.isDerivedFrom('Sketcher::SketchObject'):
        placement = definition.getGlobalPlacement().inverse().multiply(obj.getGlobalPlacement())
        normal = placement.Rotation.multVec(App.Vector(0, 0, 1))
        origin = placement.Base
    else:
        plane = profile.findPlane()
        if plane is not None:
            normal = plane.Axis
        origin = profile.BoundBox.Center
    direction = normal
    if 'direction' in links:
        line = planes.describe(definition, links['direction'])
        if line[0] != 'line':
            raise ValueError('Direction requires a straight edge or axis.')
        direction = line[2]
    if direction is None:
        raise ValueError('Choose a selected axis / line direction for this standalone curve.')
    direction = App.Vector(direction); direction.normalize()
    if v['reverse']:
        direction = -direction
    factor = abs(normal.dot(direction)) if normal is not None else 1.
    if normal is not None and factor < 1e-7:
        raise ValueError('The direction must leave the profile plane.')
    if normal is None and (v['measure'] == 'Along profile normal' or v['start'] == 'Reference'):
        raise ValueError('This profile has no unique plane; use Along direction and a start offset.')
    shift = 0.
    if v['start'] == 'Reference':
        start = planes.describe(definition, links['start'])
        if start[0] != 'plane' or abs(abs(start[2].dot(normal)) - 1) > 1e-7:
            raise ValueError('Choose a start face or plane parallel to the profile.')
        shift = (start[1] - origin).dot(start[2]) / direction.dot(start[2])
    if v['start'] != 'Profile plane':
        shift += v['start_offset']
    profile.translate(direction * shift)
    pieces = []
    with kernel_document() as scratch:
        source = scratch.addObject('Part::Feature', 'SheetProfile')
        source.Shape = kernel_snapshot(profile)
        for suffix in ('', '2') if v['sides'] == 'Two sides' else ('',):
            axis = -direction if suffix else direction
            kind = v['end' + suffix]
            extrusion = scratch.addObject('Part::Extrusion', 'SheetEvaluation')
            extrusion.Base = source; extrusion.DirMode = 'Custom'; extrusion.Dir = axis
            extrusion.Solid = False
            if kind == 'Length':
                length = v['length' + suffix] / factor if v['measure'] == 'Along profile normal' else v['length' + suffix]
                extrusion.LengthFwd = length
                extrusion.Symmetric = v['sides'] == 'Symmetric'
                extrusion.TaperAngle = v['taper' + suffix]
                if extrusion.Symmetric:
                    extrusion.TaperAngleRev = v['taper' + suffix]
                scratch.recompute()
                piece = extrusion.Shape.copy()
            else:
                if v['sides'] == 'Symmetric':
                    raise ValueError('Use One side or Two sides for a Sheet with a limiting face.')
                limit = planes.shape(definition, links['secondlimit' if suffix else 'limit'])
                candidates = []
                for face in limit.Faces:
                    if not isinstance(face.Surface, Part.Plane):
                        continue
                    n = face.normalAt(0, 0); denominator = axis.dot(n)
                    if abs(denominator) < 1e-7:
                        continue
                    projected = profile.copy()
                    projected.Placement = App.Placement(App.Vector(), App.Rotation(n, App.Vector(0, 0, 1))).multiply(projected.Placement)
                    distances = [(face.CenterOfMass.dot(n) - height) / denominator
                                 for height in (projected.BoundBox.ZMin, projected.BoundBox.ZMax)]
                    if min(distances) + v['offset' + suffix] <= 1e-7:
                        continue
                    cap = face.copy(); cap.translate(axis * v['offset' + suffix])
                    extrusion.LengthFwd = max(distances) + abs(v['offset' + suffix]) + max(1., profile.BoundBox.DiagonalLength)
                    scratch.recompute()
                    probe = extrusion.Shape.copy()
                    if probe.isNull():
                        continue
                    piece = probe.common(cap.makeHalfSpace(profile.Vertexes[0].Point))
                    # A finite face must span the whole end boundary, not just
                    # cross part of the profile. Infinite datum planes remain usable.
                    end = probe.section(cap)
                    if end.isNull() or not end.Edges:
                        continue
                    full_end = probe.section(cap.Surface.toShape())
                    if full_end.Length - end.Length > max(1e-7, full_end.Length * 1e-7):
                        continue
                    candidates.append((min(distances), piece))
                if not candidates:
                    raise ValueError('Sheet end requires a forward planar limiting face reached by the curves.')
                piece = min(candidates, key=lambda item: item[0])[1]
            if piece.isNull() or not piece.isValid() or not piece.Faces or piece.Solids or piece.Area < 1e-9:
                raise ValueError('The sheet extrusion is degenerate; check the curves, direction and taper.')
            pieces.append(piece)
    result = pieces[0] if len(pieces) == 1 else pieces[0].fuse(pieces[1])
    if v['refine']:
        result = result.removeSplitter()
    if result.isNull() or not result.isValid() or not result.Faces or result.Solids:
        raise ValueError('The extrusion must produce valid uncapped sheets.')
    result = name_tool(result, refs, feature, namespace='PlusExtrudeSheet1')
    return result, result.copy(), edges


class Extrude:
    @staticmethod
    def engine():
        return sys.modules[__name__]

    def __init__(self, obj):
        engine = self.engine()
        obj.addProperty('App::PropertyInteger', engine.VERSION, engine.NAME)
        setattr(obj, engine.VERSION, 1)
        obj.addProperty('App::PropertyLinkSubListGlobal', 'ProfileReferences', engine.NAME)
        for name in engine.LINKS.values():
            obj.addProperty('App::PropertyLinkSubListGlobal', name, engine.NAME)
        for key, default in engine.DEFAULTS.items():
            kind = 'Bool' if isinstance(default, bool) else 'String' if isinstance(default, str) else 'Float'
            obj.addProperty('App::Property' + kind, engine.PREFIX + key, engine.NAME)
            setattr(obj, engine.PREFIX + key, default)
        obj.addProperty('App::PropertyString', engine.ERROR, engine.NAME)
        for prop in [engine.VERSION, 'ProfileReferences', *engine.LINKS.values(),
                     *[engine.PREFIX + key for key in engine.DEFAULTS]]:
            obj.setEditorMode(prop, 2)
        obj.setEditorMode(engine.ERROR, 1)
        obj.Proxy = self

    def execute(self, obj):
        engine = self.engine()
        try:
            definition = owner(obj)
            result, tool, _ = engine.evaluate(definition, planes.flatten(obj.ProfileReferences),
                                       engine.references(obj), engine.settings(obj), obj)
            body = obj.getParentGeoFeatureGroup()
            transform = body.getGlobalPlacement().inverse().multiply(definition.getGlobalPlacement())
            # PartDesign synchronizes Placement with BaseFeature after execute.
            # Bake the coordinate conversion into geometry so that synchronization
            # cannot discard the Body transform. AddSubShape is feature-local.
            placement = obj.BaseFeature.Placement if obj.BaseFeature else App.Placement()
            local = placement.inverse().multiply(transform).toMatrix()
            result.transformShape(local, True)
            result.Placement = placement
            obj.Shape = result
            tool.transformShape(local, True)
            obj.AddSubShape = tool
            setattr(obj, engine.ERROR, '')
        except Exception as exc:
            obj.Shape = Part.Shape()
            obj.AddSubShape = Part.Shape()
            setattr(obj, engine.ERROR, str(exc))
            raise

    def dumps(self):
        return None

    def loads(self, state):
        pass


class ViewExtrude:
    def __init__(self, view):
        view.Proxy = self

    def getIcon(self):
        return ':/icons/PartDesign_Pad.svg'

    def doubleClicked(self, view):
        from . import extrude_task
        extrude_task.show(view.Object)
        return True

    def dumps(self):
        return None

    def loads(self, state):
        pass


def save(doc, refs, links, values, feature=None):
    return save_feature(doc, refs, links, values, feature, sys.modules[__name__])


def save_feature(doc, refs, links, values, feature, engine):
    definition, path = modeling._context(doc)
    refs, links, values = engine.validate(definition, refs, links, values, feature)
    engine.evaluate(definition, refs, links, values, feature)
    target = links.get('target', (None, ''))[0]
    old_body = feature.getParentGeoFeatureGroup() if feature else None
    body = target.getParentGeoFeatureGroup() if target else None
    if feature and target is None and not engine.references(feature).get('target'):
        body = old_body
    if feature and body != old_body and old_body.Tip != feature:
        raise ValueError('Change the target before adding downstream features; this edit would move a feature chain.')
    with document.transaction(definition.Document, 'Edit '+engine.NAME if feature else engine.NAME):
        if body is None:
            body = definition.newObject('PartDesign::Body', 'Body')
            body.AllowCompound = False
        if feature is None:
            feature = body.newObject('PartDesign::FeatureAddSubPython', engine.NAME)
            engine.Feature(feature)
            engine.ViewFeature(feature.ViewObject)
            if target:
                for prop in ('ShapeAppearance', 'LineColor', 'PointColor', 'Transparency', 'DisplayMode'):
                    setattr(feature.ViewObject, prop, getattr(target.ViewObject, prop))
        elif body != old_body:
            predecessor = engine.references(feature).get('target', (None, ''))[0]
            old_body.removeObject(feature)
            old_body.Tip = predecessor
            if predecessor:
                predecessor.Visibility = True
            body.addObject(feature)
        if 'output' in engine.DEFAULTS and engine.PREFIX + 'output' not in feature.PropertiesList:
            feature.addProperty('App::PropertyString', engine.PREFIX + 'output', engine.NAME)
            feature.setEditorMode(engine.PREFIX + 'output', 2)
        feature.ProfileReferences = planes.links(refs)
        for key, prop in engine.LINKS.items():
            setattr(feature, prop, planes.links([links[key]]) if key in links else [])
        for key, value in values.items():
            setattr(feature, engine.PREFIX + key, value)
        definition.Document.recompute()
        if getattr(feature, engine.ERROR) or feature.Shape.isNull() or 'Invalid' in feature.State:
            raise ValueError(getattr(feature, engine.ERROR) or engine.NAME+' failed to recompute.')
        # Consuming a face must not hide its entire donor solid/sheet.
        if refs[0][0].isDerivedFrom('Sketcher::SketchObject'):
            refs[0][0].Visibility = False
        if target:
            target.Visibility = False
        feature.Visibility = body.Tip == feature
    editing._restore(doc, definition, path)
    return feature


Feature = Extrude
ViewFeature = ViewExtrude
