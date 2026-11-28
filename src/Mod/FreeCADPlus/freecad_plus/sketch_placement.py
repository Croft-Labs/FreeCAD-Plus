# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative placement on native sketches; no auxiliary feature or Body."""
from . import result_names
import math
import FreeCAD as App
from . import document, planes


def is_managed(obj):
    return getattr(obj, 'PlusSketchPlacementVersion', None) == 1


def plane_object(refs):
    if len(refs) != 1:
        return None
    obj = refs[0][0]
    return obj if planes.is_plane(obj) or obj.TypeId in ('App::Plane', 'PartDesign::Plane') else None


def saved_offset(feature):
    """Version-1 sketches written before offset support remain on their support."""
    return feature.SketchPlaneOffset.Value if 'SketchPlaneOffset' in feature.PropertiesList else 0.0


def solve(definition, refs, origin_refs=(), axis_refs=(), axis='X', flipped=False, offset=0,
          normal_to_line=True):
    offset = float(offset)
    if not math.isfinite(offset):
        raise ValueError('Offset must be finite')
    if len(refs) != 1 or planes.describe(definition, refs[0])[0] != 'plane':
        return planes.solve(definition, refs, offset, origin_refs, axis_refs, axis, flipped,
                            normal_to_line=normal_to_line)
    support = plane_object(refs)
    if support is not None:
        frame = definition.getGlobalPlacement().inverse().multiply(support.getGlobalPlacement())
        normal = frame.Rotation.multVec(App.Vector(0, 0, 1))
        origin = frame.Base
        default_x = frame.Rotation.multVec(App.Vector(1, 0, 0))
    else:
        anchor, normal = planes.base_plane(definition, refs)
        origin = normal * anchor.dot(normal)
        default_x = App.Vector(1, 0, 0) - normal * normal.x
    if origin_refs:
        if len(origin_refs) != 1:
            raise ValueError('Select one origin point')
        item = planes.describe(definition, origin_refs[0])
        if item[0] != 'point':
            raise ValueError('Origin accepts a point only')
        origin = item[1] - normal * (item[1] - origin).dot(normal)
    # Displace along the support normal before optional sketch-normal reversal.
    # Projecting an override onto the support and translating is equivalent to
    # projecting it directly onto the parallel offset sketch plane.
    origin = origin + normal * offset
    if axis not in ('X', 'Y'):
        raise ValueError('Choose X or Y')
    if axis_refs:
        items = [planes.describe(definition, ref) for ref in axis_refs]
        if len(items) == 1 and items[0][0] == 'line':
            direction = items[0][2]
        elif len(items) == 2 and all(item[0] == 'point' for item in items):
            direction = items[1][1] - items[0][1]
        else:
            raise ValueError('Select a line, edge, or two points for the axis.')
    else:
        if default_x.Length < planes.EPS:
            raise ValueError('Part X is perpendicular to this face. Select an axis direction.')
        default_x = planes.unit(default_x)
        direction = default_x if axis == 'X' else normal.cross(default_x)
    direction = planes.unit(direction - normal * direction.dot(normal))
    if flipped:
        normal = -normal
    x, y = (direction, normal.cross(direction)) if axis == 'X' else (direction.cross(normal), direction)
    return App.Placement(origin, App.Rotation(x, y, normal, 'ZXY'))


def validate(definition, refs, origin_refs=(), axis_refs=(), axis='X', flipped=False, feature=None, offset=0,
             normal_to_line=True):
    refs, origin_refs, axis_refs = [planes.canonical(definition, r) for r in (refs, origin_refs, axis_refs)]
    if feature is not None:
        if not feature.isDerivedFrom('Sketcher::SketchObject') or document.owned_path(definition, feature) is None:
            raise ValueError('Edit a sketch owned by this component')
        if any(obj == feature or obj in feature.InListRecursive for obj, _ in refs + origin_refs + axis_refs):
            raise ValueError('A sketch cannot depend on itself or a downstream feature')
    document.require_predecessors(definition, feature, refs + origin_refs + axis_refs)
    solve(definition, refs, origin_refs, axis_refs, axis, flipped, offset, normal_to_line)
    return refs, origin_refs, axis_refs


def configure(feature, refs, origin_refs=(), axis_refs=(), axis='X', flipped=False, offset=0,
              normal_to_line=None, quantity_units=None):
    if normal_to_line is None:
        normal_to_line = planes.saved_normal_to_line(feature) if is_managed(feature) else True
    offset = float(offset)
    if not math.isfinite(offset):
        raise ValueError('Offset must be finite')
    if not is_managed(feature):
        feature.addProperty('App::PropertyInteger', 'PlusSketchPlacementVersion', 'Sketch placement')
        for name in ('PlaneReferences', 'OriginPoint', 'AxisReferences'):
            feature.addProperty('App::PropertyLinkSubListGlobal', name, 'Sketch placement')
        feature.addProperty('App::PropertyEnumeration', 'DefinedAxis', 'Sketch placement').DefinedAxis = ['X', 'Y']
        feature.addProperty('App::PropertyBool', 'FlipNormal', 'Sketch placement')
        for name in ('PlusSketchPlacementVersion', 'PlaneReferences', 'OriginPoint', 'AxisReferences',
                     'DefinedAxis', 'FlipNormal'):
            feature.setEditorMode(name, 2)
        feature.PlusSketchPlacementVersion = 1
    if 'SketchPlaneOffset' not in feature.PropertiesList:
        feature.addProperty('App::PropertyDistance', 'SketchPlaneOffset', 'Sketch placement')
        feature.setEditorMode('SketchPlaneOffset', 2)
    feature.SketchPlaneOffset = offset
    feature.MapMode = 'Deactivated'
    feature.AttachmentSupport = None
    feature.PlaneReferences = planes.links(refs)
    feature.OriginPoint = planes.links(origin_refs)
    feature.AxisReferences = planes.links(axis_refs)
    feature.DefinedAxis = axis
    feature.FlipNormal = flipped
    if 'NormalToLine' not in feature.PropertiesList:
        feature.addProperty('App::PropertyBool', 'NormalToLine', 'Sketch placement')
        feature.setEditorMode('NormalToLine', 2)
    feature.NormalToLine = normal_to_line
    from .quantity_fields import save as save_units
    save_units(feature, quantity_units)
    recompute(feature)


def recompute(feature):
    """Called by native SketchObject::execute before solving geometry/constraints."""
    if not is_managed(feature):
        raise ValueError('Unsupported sketch placement version')
    owner = feature.getParentGeoFeatureGroup()
    definition = owner
    while definition is not None and definition.TypeId != 'App::Part':
        definition = definition.getParentGeoFeatureGroup()
    if definition is None:
        raise ValueError('The sketch no longer belongs to a component')
    placement = solve(definition, planes.flatten(feature.PlaneReferences),
                      planes.flatten(feature.OriginPoint), planes.flatten(feature.AxisReferences),
                      feature.DefinedAxis, feature.FlipNormal, saved_offset(feature),
                      planes.saved_normal_to_line(feature))
    # After Extrude, the native sketch belongs to its result Body. Store in that
    # frame while evaluating all defaults and references in component coordinates.
    placement = owner.getGlobalPlacement().inverse().multiply(definition.getGlobalPlacement()).multiply(placement)
    if not feature.Placement.isSame(placement, 1e-10):
        feature.Placement = placement


def save(doc, refs, origin_refs=(), axis_refs=(), axis='X', flipped=False, feature=None, offset=0,
         normal_to_line=None, result_name=None, quantity_units=None):
    from . import modeling
    definition, _ = modeling._context(doc)
    if normal_to_line is None:normal_to_line = planes.saved_normal_to_line(feature)
    refs, origin_refs, axis_refs = validate(definition, refs, origin_refs, axis_refs, axis, flipped, feature, offset, normal_to_line)
    with document.transaction(definition.Document, 'Edit sketch placement' if feature else 'Create sketch'):
        if feature is None:
            feature = definition.newObject('Sketcher::SketchObject', 'Sketch')
        result_names.assign(feature,result_name)
        configure(feature, refs, origin_refs, axis_refs, axis, flipped, offset, normal_to_line, quantity_units)
        definition.Document.recompute()
        if 'Invalid' in feature.State:
            raise ValueError('The sketch could not be recomputed')
    return feature
