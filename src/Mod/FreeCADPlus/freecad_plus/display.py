# SPDX-License-Identifier: LGPL-2.1-or-later
"""Saved component display choices; resolution is read-only and view-independent.

Path resolution drives per-view filtering; it never grants reference eligibility.
"""
from . import document

TYPES = ('Full Component', 'Bodies Only', 'Reference', 'Excluded')
SELF = ('PlusSelfPartType', 'PlusSelfShown')
CHILD = ('PlusChildPartType', 'PlusChildShown')


def _names(obj):
    return CHILD if obj.TypeId == 'App::Link' else SELF


def state(obj):
    """Missing optional metadata has defaults; never migrate merely by reading."""
    part, shown = _names(obj)
    return (getattr(obj, part, 'Bodies Only' if obj.TypeId == 'App::Link' else 'Full Component'),
            bool(getattr(obj, shown, True)))


def validate_local(root, definitions, instances):
    for obj in [*definitions, *instances]:
        names = _names(obj)
        present = [name in obj.PropertiesList for name in names]
        if not any(present): continue
        if root.PlusSchema < 5 or not all(present):
            raise ValueError('Incomplete or unsupported component display metadata')
        if (obj.getTypeIdOfProperty(names[0]) != 'App::PropertyEnumeration' or
                obj.getTypeIdOfProperty(names[1]) != 'App::PropertyBool' or
                tuple(obj.getEnumerationsOfProperty(names[0])) != TYPES or state(obj)[0] not in TYPES):
            raise ValueError('Invalid component display metadata')


def write_state(obj, value):
    """Internal helper; caller owns one defining-file transaction and schema upgrade."""
    part_type, shown = value
    if part_type not in TYPES or type(shown) is not bool:
        raise ValueError('Choose a valid Part Type and Shown/Hidden state')
    part, visibility = _names(obj)
    if part not in obj.PropertiesList:
        obj.addProperty('App::PropertyEnumeration', part, 'Component display')
        setattr(obj, part, list(TYPES))
        obj.addProperty('App::PropertyBool', visibility, 'Component display')
        for name in (part, visibility):
            obj.setEditorMode(name, 2)
            obj.setPropertyStatus(name, 'NoRecompute')
    setattr(obj, part, part_type); setattr(obj, visibility, shown)


def enable(root):
    if root.PlusSchema < 4:
        from .external import add_properties
        if 'Imports' not in root.PropertiesList: add_properties(root)
    root.PlusSchema = 5


def set_state(owner, child=None, *, part_type=None, shown=None):
    """Store a self/direct-child choice in the parent's defining file, atomically."""
    root = document.validate(owner.Document)
    if owner not in [root, *root.Definitions] or (child is None and owner == root):
        raise ValueError('Choose a component or a direct child of the active context')
    if child is not None and (child.TypeId != 'App::Link' or child not in owner.Group):
        raise ValueError('Only a direct child belongs to this component setting')
    obj = child if child is not None else owner
    old_type, old_shown = state(obj)
    value = (old_type if part_type is None else part_type, old_shown if shown is None else shown)
    if value[0] not in TYPES or type(value[1]) is not bool:
        raise ValueError('Choose a valid Part Type and Shown/Hidden state')
    if shown is True and value[0] == 'Excluded':
        raise ValueError('Change Part Type before showing an Excluded component')
    for name in _names(obj):
        if name in obj.PropertiesList and any(flag in obj.getPropertyStatus(name) for flag in ('ReadOnly','Immutable')):
            raise ValueError('This component display setting is read-only')
        if any(prop == name for prop, expression in obj.ExpressionEngine):
            raise ValueError('This component display setting is expression-driven')
    if value == (old_type, old_shown): return False
    with document.transaction(owner.Document, 'Change component display setting'):
        enable(root); write_state(obj, value)
    return True


def resolved(obj, *, direct=True):
    """Reference becomes Excluded below the active owner's direct-child level."""
    part_type, shown = state(obj)
    effective = 'Excluded' if part_type == 'Reference' and not direct else part_type
    return effective, shown and effective != 'Excluded'


def hidden_paths(doc, active=None, active_path=()):
    """Resolve explicit Hidden/Excluded and nested Reference for placed occurrences.

    Bodies Only hides construction/history content through the same native paths.
    The route into Edit takes precedence over an ancestor's saved child override.
    """
    from . import hierarchy
    root = document.validate(doc)
    active_path = tuple(active_path)
    if active_path and hierarchy.resolve(doc, active_path)[0] != active:
        raise ValueError('The active component occurrence changed')
    if active is not None and not active_path:
        return ()  # Unused-definition isolation owns its separate borrowed display.
    return _hidden_paths(root, active, active_path)


def unused_hidden_paths(definition):
    """Use the same saved child choices in a temporary unused-definition display."""
    if definition not in document.validate(definition.Document).Definitions:
        raise ValueError('Choose a component definition')
    return _hidden_paths(definition, None, ())


def _hidden_paths(root, active, active_path):
    from . import hierarchy
    hidden = []
    def visit(owner, path=(), kind='Full Component'):
        if kind == 'Bodies Only':
            hidden.extend(_construction_paths(owner, hierarchy.subname(path)))
        for link in owner.Group:
            if link.TypeId != 'App::Link': continue
            route = (*path, link)
            if active_path and active_path[:len(route)] == route:
                kind, visible = resolved(active) if route == active_path else ('Full Component', True)
            else:
                kind, visible = resolved(link, direct=(path == active_path))
            if not visible:
                hidden.append(hierarchy.subname(route))
            else:
                visit(link.LinkedObject, route, kind)
    visit(root, kind=resolved(root)[0] if active is None and not hasattr(root, 'PlusFormat') else 'Full Component')
    return tuple(hidden)


def _construction_paths(owner, prefix):
    """Whole-object display paths only; retain native Body Tips and face-bearing results.

    Component links are traversed separately with their own saved types. Filtering
    never creates proxy geometry or changes an object's persistent Visibility.
    """
    result = []
    def hide(obj, base):
        # Invisible providers need no override and may have no native scene path.
        if obj is not None and obj.Visibility:
            result.append(base + obj.Name + '.')
    hide(owner.Origin, prefix)
    for obj in owner.Group:
        if obj.TypeId == 'App::Link':
            continue
        if obj.TypeId == 'PartDesign::Body':
            body_prefix = prefix + obj.Name + '.'
            hide(obj.Origin, body_prefix)
            for feature in obj.Group:
                if feature != obj.Tip:
                    hide(feature, body_prefix)
        elif not hasattr(obj, 'Shape') or not obj.Shape.Faces:
            hide(obj, prefix)
    return result


def apply_hidden(view, root, paths, *, preview=False):
    """Apply view-local paths, synchronizing queued native link snapshots once.

    LinkInfo rebuilds child snapshots through Coin's delayed sensors. A Qt paint
    can precede that queue. Retry only this specific transient condition after
    draining it once; invalid paths and persistent failures still propagate.
    There is no polling, event-loop wait or recurring retry.
    """
    method = view.setComponentPreviewHiddenPaths if preview else view.setComponentHiddenPaths
    try:
        method(root, paths)
    except ValueError as error:
        if str(error) != 'A component display path is temporarily unavailable':
            raise
        from pivy import coin
        coin.SoDB.getSensorManager().processDelayQueue(True)
        method(root, paths)
