# SPDX-License-Identifier: LGPL-2.1-or-later
"""Sketch pattern geometry and constraints. All persisted output is native Sketcher data."""
import math
import FreeCAD as App
import Part
import Sketcher

EPS = 1e-7
UNDEFINED = -2000


def extent_values(extent, angular=False):
    """Include zero exactly once. Counts include the shared original."""
    mode = extent.get('mode', 'One dimension')
    n = int(extent.get('count', 2))
    if n != extent.get('count', 2) or not 2 <= n <= 999:
        raise ValueError('Instances must be a whole number from 2 to 999.')
    def step(value, spacing, number, full_circle=False):
        if not math.isfinite(value) or value <= 0:
            raise ValueError('Pattern spacing must be greater than zero.')
        total = spacing in ('Total distance', 'Total angle')
        return value / (number if full_circle else number - 1) if total else value
    value = float(extent.get('value', 10))
    spacing = extent.get('spacing', 'Angular pitch' if angular else 'Pitch')
    closed = angular and spacing == 'Total angle' and abs(value - 360) < EPS
    if mode == 'Symmetric':
        if n % 2 == 0:
            raise ValueError('Symmetric requires an odd instance count, with the original in the middle.')
        pitch = step(value, spacing, n, closed)
        values = [i * pitch for i in range(-(n // 2), n // 2 + 1)]
    elif mode == 'One dimension':
        values = [i * step(value, spacing, n, closed) for i in range(n)]
    elif mode == 'Two dimensions':
        n2 = int(extent.get('count2', 2))
        if n2 != extent.get('count2', 2) or not 2 <= n2 <= 999:
            raise ValueError('Instances must be a whole number from 2 to 999.')
        pitch = step(value, spacing, n)
        pitch2 = step(float(extent.get('value2', 10)), extent.get('spacing2', spacing), n2)
        values = [-i * pitch2 for i in range(n2 - 1, 0, -1)] + [i * pitch for i in range(n)]
    else:
        raise ValueError('Choose One dimension, Two dimensions, or Symmetric.')
    if extent.get('reverse') and mode != 'Symmetric':
        values = [-v for v in values]
    if angular:
        if max(values) - min(values) > 360 + EPS:
            raise ValueError('The angular extents must fit within one full turn.')
        keys = [round(angle % 360, 7) % 360 for angle in values]
        if len(set(keys)) != len(keys):
            raise ValueError('The angular extents overlap. Use a 360° total angle for an evenly spaced full circle.')
    return values


def geometry(sketch, geo):
    if geo >= 0:
        if geo >= sketch.GeometryCount: raise ValueError('A selected sketch element no longer exists.')
        return sketch.Geometry[geo]
    if -geo > len(sketch.ExternalGeo): raise ValueError('The external reference no longer exists.')
    return sketch.ExternalGeo[-geo - 1]


def point_reference(sketch, ref):
    if ref is None: raise ValueError('Choose a point, circle, or arc center.')
    geo, pos = ref
    if geo == -1 and pos == 1: return App.Vector(0, 0, 0), ref
    g = geometry(sketch, geo)
    if pos:
        p = sketch.getPoint(geo, pos)
        return p, ref
    if isinstance(g, (Part.Circle, Part.ArcOfCircle, Part.Ellipse, Part.ArcOfEllipse)):
        return g.Center, (geo, 3)
    if isinstance(g, Part.Point): return App.Vector(g.X, g.Y, g.Z), (geo, 1)
    raise ValueError('Select a point, circle, or arc for this reference.')


def direction(sketch, values):
    method = values.get('method', 'Axis or line')
    if method == 'Vector':
        x, y = float(values.get('x', 1)), float(values.get('y', 0))
        if not all(map(math.isfinite, (x, y))): raise ValueError('Enter a finite direction vector.')
        vector = App.Vector(x, y, 0)
    elif method == 'Two points':
        a, _ = point_reference(sketch, values.get('start'))
        b, _ = point_reference(sketch, values.get('end'))
        vector = b - a
    else:
        ref = values.get('reference')
        if ref is None: raise ValueError('Choose an axis or straight line for each direction.')
        geo, pos = ref
        if pos: raise ValueError('Select a straight line or sketch axis, not a vertex.')
        if geo == -1: return App.Vector(1, 0, 0)
        if geo == -2: return App.Vector(0, 1, 0)
        g = geometry(sketch, geo)
        if not isinstance(g, Part.LineSegment): raise ValueError('A direction requires a straight line.')
        vector = g.EndPoint - g.StartPoint
    if vector.Length <= EPS: raise ValueError('A direction requires two distinct points or a nonzero vector.')
    return vector / vector.Length


def transforms(sketch, options):
    """Return rotations and translations in sketch coordinates, excluding identity."""
    result = []
    if options.get('pattern', 'Linear') == 'Linear':
        d1 = direction(sketch, options['d1'])
        a = extent_values(options['d1'])
        if options.get('directions') == 'Two directions':
            d2 = direction(sketch, options['d2']); b = extent_values(options['d2'])
            if d1.cross(d2).Length < EPS: raise ValueError('The two grid directions must not be parallel.')
        else: d2, b = App.Vector(), [0.0]
        if len(a) * len(b) > 1000: raise ValueError('Use at most 1,000 total pattern instances.')
        for x in a:
            for y in b:
                delta = d1 * x + d2 * y
                if delta.Length > EPS: result.append((0.0, delta, None, App.Vector()))
    else:
        center, center_ref = point_reference(sketch, options.get('center'))
        layout = options.get('directions', 'Angular')
        angles = extent_values(options['angular'], True) if layout != 'Radial' else [0.0]
        radii = extent_values(options['radial']) if layout != 'Angular' else [0.0]
        radial = App.Vector()
        if layout != 'Angular':
            anchor, _ = point_reference(sketch, options['radial'].get('reference'))
            radial = anchor - center
            radius = radial.Length
            if radius <= EPS: raise ValueError('The radial reference must be away from the rotation center.')
            if radius + min(radii) <= EPS: raise ValueError('The inward extent reaches or crosses the rotation center.')
            radial /= radius
        if len(angles) * len(radii) > 1000: raise ValueError('Use at most 1,000 total pattern instances.')
        for angle in angles:
            rotation = App.Rotation(App.Vector(0, 0, 1), angle)
            for distance in radii:
                if abs(angle % 360) < EPS and abs(distance) < EPS: continue
                shift = radial * distance
                delta = center - rotation.multVec(center) + rotation.multVec(shift)
                result.append((angle, delta, center_ref, shift))
    if not result: raise ValueError('The pattern must contain a distinct copy of the original.')
    return result


def operation_geometry(sketch, ids):
    result = list(dict.fromkeys(ids))
    if not result: raise ValueError('Select the geometry to pattern.')
    if any(not isinstance(i, int) or i < 0 or i >= sketch.GeometryCount for i in result):
        raise ValueError('Select internal geometry belonging to this sketch.')
    for c in sketch.Constraints:
        if c.Type == 'InternalAlignment' and c.Second in result and c.First not in result:
            result.append(c.First)
    return result


def transformed(g, transform):
    angle, delta, _, _ = transform
    copy = g.copy()
    copy.transform(App.Placement(delta, App.Rotation(App.Vector(0, 0, 1), angle)).toMatrix())
    return copy


def preview(sketch, ids, options):
    ids = operation_geometry(sketch, ids)
    placements = transforms(sketch, options)
    if len(ids) * len(placements) > 10000: raise ValueError('Use at most 10,000 generated geometry elements.')
    return [transformed(geometry(sketch, i), transform) for transform in placements for i in ids]


def _copy_constraints(sketch, source, mapping, transform):
    angle = transform[0]
    copied = []
    for blob in source:
        c = Sketcher.Constraint(); c.restoreContent(blob)
        if c.First not in mapping: continue
        if any(i != UNDEFINED and i not in mapping for i in (c.Second, c.Third)): continue
        if c.Type in ('DistanceX', 'DistanceY') and c.Second == UNDEFINED:
            # Absolute coordinates are not transferable to a new instance.
            continue
        if abs(angle) > EPS and c.Type in ('Horizontal', 'Vertical', 'Angle') and c.Second == UNDEFINED and (not c.Driving or not c.IsActive):
            # Replacing this with a driving absolute angle would lock a source
            # degree of freedom when relative placement dimensions are added.
            continue
        if abs(angle) > EPS and c.Type in ('Horizontal', 'Vertical', 'DistanceX', 'DistanceY'):
            if c.Type in ('Horizontal', 'Vertical') and c.Second == UNDEFINED and isinstance(geometry(sketch, mapping[c.First]), Part.LineSegment):
                g = geometry(sketch, mapping[c.First]); v = g.EndPoint - g.StartPoint
                c = Sketcher.Constraint('Angle', mapping[c.First], math.atan2(v.y, v.x))
                copied.append(c)
            continue
        if abs(angle) > EPS and c.Type == 'Angle' and c.Second == UNDEFINED:
            c = Sketcher.Constraint('Angle', mapping[c.First], c.Value + math.radians(angle))
            copied.append(c); continue
        c.First = mapping[c.First]
        if c.Second in mapping: c.Second = mapping[c.Second]
        if c.Third in mapping: c.Third = mapping[c.Third]
        c.Name = ''
        copied.append(c)
    if copied: sketch.addConstraint(copied)


def _independent(sketch, c):
    """Only remove our just-added equation if existing equations already imply it."""
    index = sketch.addConstraint(c)
    status = sketch.solve()
    if status == -2 or sketch.PartiallyRedundantConstraints:
        sketch.delConstraint(index)
        if sketch.solve() != 0: raise ValueError('The pattern constraints could not be solved.')
        return None
    elif status != 0:
        raise ValueError('The pattern dimensions conflict with the sketch.')
    return index


def _offset_point(sketch, source, target, delta):
    for axis, value, zero in [('DistanceX', delta.x, 'Vertical'), ('DistanceY', delta.y, 'Horizontal')]:
        args = (source[0], source[1], target[0], target[1])
        _independent(sketch, Sketcher.Constraint(zero, *args) if abs(value) < EPS else Sketcher.Constraint(axis, *args, value))


def _ray(sketch, center, endpoint):
    a = sketch.getPoint(*center); b = sketch.getPoint(*endpoint)
    if (b - a).Length <= EPS: raise ValueError('Dimensioned rotation requires a point away from its center.')
    line = sketch.addGeometry(Part.LineSegment(a, b), True)
    _offset_point(sketch, center, (line, 1), App.Vector())
    _offset_point(sketch, endpoint, (line, 2), App.Vector())
    return line


def _transform_point(sketch, source, target, transform):
    angle, delta, center, radial = transform
    if abs(angle % 360) < EPS:
        _offset_point(sketch, source, target, delta); return
    if source == center and radial.Length < EPS:
        _offset_point(sketch, source, target, App.Vector()); return
    start = source
    if radial.Length > EPS:
        p = sketch.getPoint(*source) + radial
        start = (sketch.addGeometry(Part.Point(p), True), 1)
        _offset_point(sketch, source, start, radial)
    if (sketch.getPoint(*start) - sketch.getPoint(*center)).Length <= EPS:
        # Offset both endpoints consistently when the radius would be zero.
        # This keeps the rotation equation defined without fixing the source.
        offset = App.Vector(10, 0, 0)
        rotated = App.Rotation(App.Vector(0, 0, 1), angle).multVec(offset)
        extra_start = (sketch.addGeometry(Part.Point(sketch.getPoint(*start) + offset), True), 1)
        extra_target = (sketch.addGeometry(Part.Point(sketch.getPoint(*target) + rotated), True), 1)
        _offset_point(sketch, start, extra_start, offset)
        _offset_point(sketch, target, extra_target, rotated)
        start, target = extra_start, extra_target
    ray1 = _ray(sketch, center, start); ray2 = _ray(sketch, center, target)
    _independent(sketch, Sketcher.Constraint('Equal', ray1, ray2))
    radians = math.radians(angle % 360)
    if abs(radians - math.pi) < EPS:
        _independent(sketch, Sketcher.Constraint('Parallel', ray1, ray2))
    else:
        _independent(sketch, Sketcher.Constraint('Angle', ray1, ray2, radians))


def _dimension_copy(sketch, mapping, transform):
    for source, target in mapping.items():
        g = geometry(sketch, source)
        if isinstance(g, Part.LineSegment): positions = (1, 2)
        elif isinstance(g, Part.Point): positions = (1,)
        elif isinstance(g, Part.Circle): positions = (3,)
        elif isinstance(g, (Part.ArcOfCircle, Part.ArcOfEllipse)): positions = (3, 1, 2)
        elif isinstance(g, Part.Ellipse): positions = (3,)
        elif isinstance(g, Part.BSplineCurve): positions = () # Native aligned poles define the curve.
        else: raise ValueError('Dimensions are not supported for this geometry type.')
        for pos in positions: _transform_point(sketch, (source, pos), (target, pos), transform)
        if isinstance(g, Part.Circle): _independent(sketch, Sketcher.Constraint('Equal', source, target))


def _positions(g):
    if isinstance(g, Part.LineSegment): return (1, 2)
    if isinstance(g, Part.Point): return (1,)
    if isinstance(g, (Part.Circle, Part.Ellipse)): return (3,)
    if isinstance(g, (Part.ArcOfCircle, Part.ArcOfEllipse)): return (3, 1, 2)
    if isinstance(g, Part.BSplineCurve): return ()
    raise ValueError('Spacing constraints are not supported for this geometry type.')


def visual_layer(facade):
    try:
        return facade.getExtensionOfType('SketcherGui::ViewProviderSketchGeometryExtension').VisualLayerId
    except (ValueError, RuntimeError):
        return 0


def spacing_tag(facade):
    # Part's runtime geometry Tag is remapped across processes. Persist our own
    # identity on the geometry so deletion/reordering and file reopening are safe.
    try:
        return facade.getExtensionOfName('FreeCADPlusPatternSpacing').Value
    except (ValueError, RuntimeError):
        return facade.Tag


def chain_is_hidden(sketch):
    tags = set(getattr(sketch, 'PatternSpacingTags', []))
    return any(visual_layer(f) == 2 for f in sketch.GeometryFacadeList if spacing_tag(f) in tags)


def set_chain_hidden(sketch, hidden):
    """Use stable native geometry tags, not indices that change after deletion."""
    tags = set(getattr(sketch, 'PatternSpacingTags', []))
    facades = sketch.GeometryFacadeList
    helpers = set()
    for i, facade in enumerate(facades):
        if spacing_tag(facade) in tags:
            if App.GuiUp:
                import SketcherGui
                try:
                    extension = facade.getExtensionOfType('SketcherGui::ViewProviderSketchGeometryExtension')
                except (ValueError, RuntimeError):
                    extension = SketcherGui.ViewProviderSketchGeometryExtension(0)
                extension.VisualLayerId = 2 if hidden else 0
                facade.setExtension(extension)
            helpers.add(i)
    if helpers:
        sketch.GeometryFacadeList = facades
        sketch.solve()
        for i, c in enumerate(sketch.Constraints):
            if c.Type not in ('Distance', 'Angle', 'Radius', 'Diameter', 'DistanceX', 'DistanceY'):
                if any(g in helpers for g in (c.First, c.Second, c.Third)):
                    sketch.setVisibility(i, not hidden)


class SpacingChains:
    """Connected helper geometry with one editable master per independent pitch."""
    def __init__(self, sketch):
        self.sketch = sketch
        self.masters = {}
        self.helpers = []
        self.units = {}

    def add(self, geometry):
        index = self.sketch.addGeometry(geometry, True)
        self.helpers.append(index)
        return index

    def constrain(self, kind, *args):
        return _independent(self.sketch, Sketcher.Constraint(kind, *args))

    def connect(self, source, target):
        self.constrain('Coincident', *source, *target)

    def line(self, source, target, key, vector, reference=None):
        s = self.sketch
        a, b = s.getPoint(*source), s.getPoint(*target)
        line = self.add(Part.LineSegment(a, b))
        self.connect(source, (line, 1)); self.connect(target, (line, 2))
        if key in self.masters:
            self.constrain('Equal', self.masters[key], line)
            self.constrain('Parallel', self.masters[key], line)
        else:
            self.masters[key] = line
            c = Sketcher.Constraint('Distance', line, (b-a).Length)
            if hasattr(c, 'PresentationUnit'): c.PresentationUnit = self.units.get(key, '')
            _independent(s, c)
            if reference is not None:
                self.constrain('Parallel', reference, line)
            elif abs(vector.y) < EPS: self.constrain('Horizontal', line)
            elif abs(vector.x) < EPS: self.constrain('Vertical', line)
            else: self.constrain('Angle', line, math.atan2(vector.y, vector.x))

    def arc(self, source, target, center, angle, key):
        s = self.sketch
        a, b, c = s.getPoint(*source), s.getPoint(*target), s.getPoint(*center)
        if (a-c).Length < EPS:
            # A zero-radius arc is singular. Retain the established nonsingular
            # relative-rotation construction for this exceptional anchor.
            rotation = App.Rotation(App.Vector(0, 0, 1), angle)
            first = s.GeometryCount
            _transform_point(s, source, target, (angle, c-rotation.multVec(c), center, App.Vector()))
            self.helpers.extend(range(first, s.GeometryCount))
            return
        start = math.atan2((a-c).y, (a-c).x)
        if angle < 0:
            start += math.radians(angle)
            source, target = target, source
        arc = self.add(Part.ArcOfCircle(Part.Circle(c, App.Vector(0, 0, 1), (a-c).Length),
                                      start, start + math.radians(abs(angle))))
        self.connect(center, (arc, 3))
        self.connect(source, (arc, 1)); self.connect(target, (arc, 2))
        c = Sketcher.Constraint('Angle', arc, math.radians(abs(angle)))
        if hasattr(c, 'PresentationUnit'): c.PresentationUnit = self.units.get(key, '')
        datum = _independent(s, c)
        if datum is not None:
            if key in self.masters:
                # Equal arc radii do not imply equal angular spans. A native
                # expression shares the one angular driver across all radii.
                s.setExpression('Constraints[%d]' % datum, 'Constraints[%d]' % self.masters[key])
                s.setVisibility(datum, False)
            else: self.masters[key] = datum

    def finish(self, hidden):
        s = self.sketch
        if 'PatternSpacingTags' not in s.PropertiesList:
            s.addProperty('App::PropertyStringList', 'PatternSpacingTags', 'Pattern',
                          'Stable identities of pattern construction helpers')
            s.setEditorMode('PatternSpacingTags', 2)
        facades = s.GeometryFacadeList
        for i in self.helpers:
            facades[i].setExtension(Part.GeometryStringExtension(facades[i].Tag, 'FreeCADPlusPatternSpacing'))
        s.PatternSpacingTags = list(s.PatternSpacingTags) + [facades[i].Tag for i in self.helpers]
        s.GeometryFacadeList = facades
        set_chain_hidden(s, hidden)


def _spacing_chains(sketch, ids, instances, options):
    chain = SpacingChains(sketch)
    circular = options.get('pattern') == 'Circular'
    if circular:
        layout = options.get('directions', 'Angular')
        xs = extent_values(options['angular'], True) if layout != 'Radial' else [0.0]
        ys = extent_values(options['radial']) if layout != 'Angular' else [0.0]
        center, center_ref = point_reference(sketch, options.get('center'))
        radial = direction(sketch, {'method':'Two points', 'start':center_ref,
                                   'end':options['radial']['reference']}) if len(ys)>1 else App.Vector()
        extents = (options.get('angular', {}), options.get('radial', {}))
        vectors = (None, radial)
    else:
        xs = extent_values(options['d1'])
        ys = extent_values(options['d2']) if options.get('directions') == 'Two directions' else [0.0]
        extents = (options['d1'], options.get('d2', {}))
        vectors = (direction(sketch, options['d1']), direction(sketch, options['d2']) if len(ys)>1 else App.Vector())
    # Match the generation order, preserving original at (0,0).
    nodes = {(0.0, 0.0): {i:i for i in ids}}
    generated = iter(instances)
    for x in xs:
        for y in ys:
            if abs(x)<EPS and abs(y)<EPS: continue
            nodes[(x,y)] = next(generated)
    for axis, values in enumerate((xs, ys)):
        if len(values) == 1: continue
        extent = extents[axis]
        reference = None
        if circular and axis == 1:
            first = sketch.GeometryCount
            reference = _ray(sketch, center_ref, point_reference(sketch, extent['reference'])[1])
            chain.helpers.extend(range(first, sketch.GeometryCount))
        elif not circular:
            if extent.get('method') == 'Two points':
                first = sketch.GeometryCount
                reference = _ray(sketch, point_reference(sketch, extent['start'])[1], point_reference(sketch, extent['end'])[1])
                chain.helpers.extend(range(first, sketch.GeometryCount))
            elif extent.get('method', 'Axis or line') == 'Axis or line':
                reference = extent['reference'][0]
        for sign in (1, -1):
            side = sorted((v for v in values if v*sign>EPS), key=abs)
            previous = 0.0
            for value in side:
                # Spanning tree: radial/grid second direction only at x=0;
                # first direction at every y. Avoid redundant grid loops.
                cross_values = ys if axis == 0 else [0.0]
                for cross in cross_values:
                    p = (previous,cross) if axis == 0 else (cross,previous)
                    q = (value,cross) if axis == 0 else (cross,value)
                    key = (axis, sign if extent.get('mode') == 'Two dimensions' else 0)
                    forward = sign == (-1 if extent.get('reverse') else 1)
                    chain.units[key] = extent.get('unit' if forward or extent.get('mode') != 'Two dimensions' else 'unit2', '')
                    for source in ids:
                        for pos in _positions(geometry(sketch, source)):
                            a, b = (nodes[p][source],pos), (nodes[q][source],pos)
                            if circular and axis == 0:
                                chain.arc(a,b,center_ref,value-previous,key)
                            else:
                                chain.line(a,b,key,vectors[axis]*sign,reference)
                previous = value
    for mapping in instances:
        for source, target in mapping.items():
            if isinstance(geometry(sketch, source), Part.Circle):
                chain.constrain('Equal', source, target)
    chain.finish(options.get('hide_spacing', False))


def apply(sketch, ids, options, dimensions=False):
    """Apply atomically; no new feature/property schema, source deletion or fixed source."""
    ids = operation_geometry(sketch, ids)
    placements = transforms(sketch, options)
    preview(sketch, ids, options) # Validate bounds and geometry before opening a transaction.
    if sketch.solve() != 0: raise ValueError('Resolve the existing sketch constraints before applying a pattern.')
    doc = sketch.Document
    doc.openTransaction('Sketch Pattern')
    try:
        if dimensions:
            for i in list(ids):
                if isinstance(geometry(sketch, i), (Part.Ellipse, Part.ArcOfEllipse, Part.BSplineCurve)):
                    sketch.exposeInternalGeometry(i)
            ids = operation_geometry(sketch, ids)
            if len(ids) * len(placements) > 10000:
                raise ValueError('Including internal geometry, the pattern exceeds 10,000 generated elements.')
        source = [c.dumpContent() for c in sketch.Constraints]
        result = []
        instances = []
        for transform in placements:
            mapping = {}
            for i in ids:
                mapping[i] = sketch.addGeometry(transformed(geometry(sketch, i), transform), sketch.getConstruction(i))
            _copy_constraints(sketch, source, mapping, transform)
            if sketch.solve() != 0: raise ValueError('The copied constraints could not be solved.')
            instances.append(mapping)
            result.extend(mapping.values())
        if dimensions: _spacing_chains(sketch, ids, instances, options)
        if sketch.solve() != 0: raise ValueError('The generated pattern could not be solved.')
        doc.recompute()
        doc.commitTransaction()
        return result
    except Exception:
        doc.abortTransaction()
        sketch.solve()
        raise
