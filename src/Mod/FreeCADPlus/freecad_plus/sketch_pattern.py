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
    elif status != 0:
        raise ValueError('The pattern dimensions conflict with the sketch.')


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
        for transform in placements:
            mapping = {}
            for i in ids:
                mapping[i] = sketch.addGeometry(transformed(geometry(sketch, i), transform), sketch.getConstruction(i))
            _copy_constraints(sketch, source, mapping, transform)
            if sketch.solve() != 0: raise ValueError('The copied constraints could not be solved.')
            if dimensions: _dimension_copy(sketch, mapping, transform)
            result.extend(mapping.values())
        if sketch.solve() != 0: raise ValueError('The generated pattern could not be solved.')
        doc.recompute()
        doc.commitTransaction()
        return result
    except Exception:
        doc.abortTransaction()
        sketch.solve()
        raise
