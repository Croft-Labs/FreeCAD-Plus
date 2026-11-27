# SPDX-License-Identifier: LGPL-2.1-or-later
"""Appearance of owned results, using native view-provider materials."""
import FreeCAD as App
import Part
from . import document

FIELDS = ('DiffuseColor', 'AmbientColor', 'SpecularColor', 'EmissiveColor', 'Shininess', 'Transparency')


def clone(material):
    return App.Material(**{key: getattr(material, key) for key in FIELDS})


def results(owner, include_history=False):
    """Catalog owned geometry; historical features require explicit selection."""
    found = []
    for obj in owner.Group:
        if obj.TypeId == 'App::Link' or obj.TypeId == 'App::Part':
            continue
        if obj.TypeId == 'PartDesign::Body':
            obj = obj.Tip
        if obj is None or obj.isDerivedFrom('Sketcher::SketchObject'):
            continue
        if obj.isDerivedFrom('Mesh::Feature') or (obj.isDerivedFrom('Part::Feature') and not obj.Shape.isNull()):
            found.append(obj)
    if include_history:
        def visit(parent):
            for child in document.owned_children(parent):
                if child.TypeId in ('App::Link', 'App::Part'):
                    continue
                if child.TypeId != 'PartDesign::Body' and not child.isDerivedFrom('Sketcher::SketchObject'):
                    if (child.isDerivedFrom('Mesh::Feature') or
                            (child.isDerivedFrom('Part::Feature') and bool(child.Shape.Faces))):
                        found.append(child)
                visit(child)
        visit(owner)
    return tuple(dict.fromkeys(found))


def face_count(obj):
    return len(obj.Shape.Faces) if hasattr(obj, 'Shape') else 0


def material_property(obj):
    view = obj.ViewObject
    if 'ShapeAppearance' in view.PropertiesList:
        return 'ShapeAppearance'
    if 'ShapeMaterial' in view.PropertiesList:
        return 'ShapeMaterial'
    raise ValueError('This geometry does not support appearance editing')


def materials(obj):
    prop = material_property(obj)
    value = getattr(obj.ViewObject, prop)
    values = list(value) if prop == 'ShapeAppearance' else [value]
    if not values:
        raise ValueError('This geometry has no appearance material')
    return [clone(values[i] if i < len(values) else values[0]) for i in range(max(1, face_count(obj)))]


def resolve_pick(owner, obj, sub):
    target = obj.getSubObject(sub, 1) if sub else obj
    if target is None:
        raise ValueError('The selected geometry is no longer available')
    if target.TypeId == 'App::Link':
        target = target.LinkedObject
    if target.TypeId == 'PartDesign::Body':
        target = target.Tip
    if target not in results(owner, include_history=True):
        raise ValueError('Choose geometry owned by ' + owner.Label + ', not a child component')
    element = Part.splitSubname(sub)[2] if sub else ''
    face = int(element[4:]) if element.startswith('Face') and element[4:].isdigit() else None
    if face is not None and not 1 <= face <= face_count(target):
        raise ValueError('The selected face is no longer available')
    return target, face


def apply(owner, targets, color=None, transparency=None):
    """Preflight all targets; change only edited fields in one owning-file Undo."""
    if owner not in document.validate(owner.Document).Definitions:
        raise ValueError('The component is no longer available')
    if not targets:
        raise ValueError('Select bodies or faces to change')
    if color is None and transparency is None:
        return False
    if transparency is not None and not 0 <= transparency <= 100:
        raise ValueError('Transparency must be between 0 and 100 percent')
    eligible = results(owner, include_history=True); grouped = {}
    for obj, face in targets:
        if obj not in eligible:
            raise ValueError('The selected body is no longer owned by this component')
        if face is not None and not 1 <= face <= face_count(obj):
            raise ValueError('The selected face is no longer available')
        grouped.setdefault(obj, set()).add(face)
    updates = []
    for obj, faces in grouped.items():
        prop = material_property(obj)
        if any(flag in obj.ViewObject.getPropertyStatus(prop) for flag in ('ReadOnly', 'Immutable')):
            raise ValueError('Appearance is read-only for ' + obj.Label)
        values = materials(obj)
        for index in (range(len(values)) if None in faces else [face - 1 for face in faces]):
            if color is not None: values[index].DiffuseColor = tuple(float(c) for c in color)
            if transparency is not None: values[index].Transparency = transparency / 100.0
        updates.append((obj, prop, values if prop == 'ShapeAppearance' else values[0]))
    with document.transaction(owner.Document, 'Change appearance'):
        for obj, prop, value in updates:
            setattr(obj.ViewObject, prop, value)
    return True
