# SPDX-License-Identifier: LGPL-2.1-or-later
"""Face-owned Shell requests, persisted as native PartDesign Thickness features."""
from . import result_names
from . import document, editing, modeling, planes


def validate(owner, refs, feature=None):
    refs = planes.canonical(owner, refs)
    if not refs:
        raise ValueError('Select faces to remove from one solid.')
    base = refs[0][0]
    for obj, sub in refs:
        if planes.shape(owner, (obj, sub)).ShapeType != 'Face':
            raise ValueError('Select faces of a solid. Curves cannot define a shell.')
        if len(obj.Shape.Solids) != 1:
            raise ValueError('Shell requires solid faces. Use Thicken to give a sheet thickness.')
        if obj != base:
            raise ValueError('Select faces from one solid. Clear faces before choosing a different solid.')
    body = base.getParentGeoFeatureGroup()
    if body is None or body.TypeId != 'PartDesign::Body':
        raise ValueError('Select faces of a modeled solid in this component.')
    document.require_predecessors(owner, feature, refs)
    if feature is None and body.Tip != base:
        raise ValueError('Select faces of the latest result of this solid.')
    if feature and body != feature.getParentGeoFeatureGroup() and feature.getParentGeoFeatureGroup().Tip != feature:
        raise ValueError('Change the solid before adding downstream features.')
    return refs


def evaluate(owner, refs, values, feature=None):
    refs = validate(owner, refs, feature)
    if values['Value'] <= 0:
        raise ValueError('Enter a thickness greater than zero.')
    shape = planes.shape(owner, (refs[0][0], ''))
    # The removed faces must belong to this exact copied solid, not separate
    # copies of its faces (OpenCascade matches their topology identities).
    faces = [shape.getElement(sub) for _, sub in refs]
    result = shape.makeThickness(faces, (-1 if values['Reversed'] else 1) * values['Value'],
                                 1e-7, values['Intersection'], False,
                                 values['Mode'], 2 if values['Join'] else 0)
    if result.isNull() or not result.isValid() or len(result.Solids) != 1:
        raise ValueError('Shell could not produce a valid solid. Adjust the faces or thickness.')
    return result


def save(doc, refs, values, feature=None, result_name=None):
    unit_values = values.get('_units', {})
    values = {k:v for k,v in values.items() if k != '_units'}
    owner, path = modeling._context(doc)
    refs = validate(owner, refs, feature)
    evaluate(owner, refs, values, feature)
    base = refs[0][0]
    body = base.getParentGeoFeatureGroup()
    with document.transaction(owner.Document, 'Edit Shell' if feature else 'Shell'):
        if feature is None:
            feature = body.newObject('PartDesign::Thickness', 'Thickness')
            feature.Label = 'Shell'
            for prop in ('ShapeAppearance', 'LineColor', 'PointColor', 'Transparency', 'DisplayMode'):
                setattr(feature.ViewObject, prop, getattr(base.ViewObject, prop))
        elif feature.getParentGeoFeatureGroup() != body:
            previous = feature.Base[0]
            old_body = feature.getParentGeoFeatureGroup()
            old_body.removeObject(feature)
            old_body.Tip = previous
            previous.Visibility = True
            body.addObject(feature)
        result_names.assign(feature,result_name)
        feature.Base = (base, [sub for _, sub in refs])
        for key, value in values.items():
            setattr(feature, key, value)
        from .quantity_fields import save as save_units
        save_units(feature, unit_values)
        owner.Document.recompute()
        if feature.Shape.isNull() or not feature.Shape.isValid() or 'Invalid' in feature.State:
            raise ValueError('Shell failed to recompute. Adjust the faces or thickness.')
        base.Visibility = False
        feature.Visibility = body.Tip == feature
    editing._restore(doc, owner, path)
    return feature
