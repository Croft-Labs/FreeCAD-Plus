# SPDX-License-Identifier: LGPL-2.1-or-later
"""Parent-owned instance patterns. Members remain ordinary shared native links."""
import json
import math
import FreeCAD as App
from . import document, external, hierarchy

MARKER = 'FreeCADPlus.InstancePattern.1'
LIMIT = 10000


def number(value):
    value = float(value)
    if not math.isfinite(value): raise ValueError('Enter finite pattern values')
    return value


def vector(value):
    if len(value) != 3: raise ValueError('Enter X, Y, Z values')
    return App.Vector(*(number(v) for v in value))


def direction(value):
    result = vector(value)
    if result.Length < 1e-9: raise ValueError('A direction cannot be zero')
    return result.normalize()


def count(value):
    if isinstance(value, bool) or int(value) != value or not 1 <= value <= LIMIT:
        raise ValueError('Use a whole-number instance count from 1 to 10000')
    return int(value)


def placements(config):
    """Deterministic coordinates in the destination definition's frame."""
    mode = config['mode']; start = vector(config.get('position', (0, 0, 0)))
    n = count(config.get('count', 1))
    if mode == 'Quantity': return [App.Placement(start, App.Rotation()) for _ in range(n)]
    if mode == 'Linear':
        axis = direction(config['direction']); spacing = number(config['spacing'])
        if spacing <= 0: raise ValueError('Spacing must be greater than zero')
        if config.get('reverse', False): axis = -axis
        return [App.Placement(start + axis * (i * spacing), App.Rotation()) for i in range(n)]
    if mode == 'Grid':
        columns, rows = count(config['columns']), count(config['rows'])
        count(columns * rows)
        x, y = direction(config['direction']), direction(config['row_direction'])
        if x.cross(y).Length < 1e-8: raise ValueError('Grid directions must not be parallel')
        sx, sy = number(config['spacing']), number(config['row_spacing'])
        if min(sx, sy) <= 0: raise ValueError('Grid spacings must be greater than zero')
        return [App.Placement(start + x * (c * sx) + y * (r * sy), App.Rotation())
                for r in range(rows) for c in range(columns)]
    if mode != 'Circular': raise ValueError('Choose Quantity, Linear, Grid or Circular')
    axis = direction(config['direction']); radius = number(config['radius'])
    if radius <= 0: raise ValueError('Radius must be greater than zero')
    angle = number(config.get('angle', 0))
    step = 360.0 / n if config.get('full', True) else number(config['angular_spacing'])
    if not config.get('full', True) and (abs(step) < 1e-9 or abs(step) * (n - 1) >= 360 - 1e-9):
        raise ValueError('Angular spacing must be nonzero and span less than 360 degrees')
    radial = App.Vector(1, 0, 0) - axis * axis.x
    if radial.Length < 1e-8: radial = App.Vector(0, 1, 0) - axis * axis.y
    radial.normalize()
    result = []
    for i in range(n):
        rotation = App.Rotation(axis, angle + i * step)
        result.append(App.Placement(start + rotation.multVec(radial) * radius,
                      rotation if config.get('rotate', False) else App.Rotation()))
    return result


def is_pattern(obj):
    return getattr(obj, 'InstancePatternFormat', None) == MARKER


def owner_of(pattern):
    return next((o for o in pattern.InList if o.TypeId == 'App::Part' and pattern in o.Group), None)


def controller(link):
    return next((o for o in link.InList if is_pattern(o) and link in o.Members), None)


def check_independent(link):
    if controller(link) is not None:
        raise ValueError('This instance is controlled by a pattern; use Edit instance pattern')


def reference_direction(owner, ref, members=()):
    """Only native references owned by this parent; linked children retain their route."""
    import Part
    from . import display
    obj, subs = ref
    if obj is None or len(subs) != 1 or obj not in [owner.Origin, *owner.Group]:
        raise ValueError('Choose an edge or axis within the destination component')
    if obj in members or any(member in obj.OutListRecursive for member in members):
        raise ValueError('A pattern cannot use its own members as direction references')
    for item in obj.getSubObjectList(subs[0]):
        if item.TypeId == 'App::Link' and display.state(item)[0] in ('Reference', 'Excluded'):
            raise ValueError('Reference or excluded geometry cannot drive an instance pattern')
    shape = Part.getShape(obj, subs[0], needSubElement=True)
    if shape.ShapeType != 'Edge' or not isinstance(shape.Curve, (Part.Line, Part.LineSegment)):
        raise ValueError('Choose a straight edge or axis')
    return direction(tuple(shape.tangentAt(shape.FirstParameter)))


def resolved_config(owner, config, refs=(), members=()):
    result = dict(config)
    keys = result.get('reference_keys', [])
    if len(keys) != len(refs) or len(set(keys)) != len(keys) or any(k not in ('direction', 'row_direction') for k in keys):
        raise ValueError('Repair the pattern direction references')
    for key, ref in zip(keys, refs):
        result[key] = tuple(reference_direction(owner, ref, members))
    return result


def prepare(owner, definitions=(), label=None):
    root = document.validate(owner.Document)
    if owner not in root.Definitions: raise ValueError('Edit the destination component first')
    if label is not None:
        from . import naming
        naming.check_name(owner.Document, label)
        if definitions: raise ValueError('Choose existing components or a new component')
        return root, (), ()
    definitions = tuple(dict.fromkeys(definitions))
    if not definitions: raise ValueError('Choose at least one component')
    available = set(external.available_definitions(root)); imports = []
    for definition in definitions:
        if definition not in document.validate(definition.Document).Definitions:
            raise ValueError('The source component is no longer available')
        hierarchy.check_nesting(owner, definition)
        if definition not in available:
            _, imported = external.prepare_import(owner.Document, definition.Document)
            imports.append(imported); available.update(external.available_definitions(imported))
    from . import naming
    naming.check_imports(owner.Document, imports)
    return root, definitions, imports


def create(owner, definitions, config, *, label=None, refs=()):
    root, definitions, imports = prepare(owner, definitions, label)
    values = placements(resolved_config(owner, config, refs))
    count(len(values) * (len(definitions) or 1))
    with document.transaction(owner.Document, 'Create component instances'):
        if imports:
            root.Imports = [*root.Imports, *imports]
            root.ImportIdentities = json.dumps([str(o.Document.Uid) for o in root.Imports])
        if label is not None: definitions = (hierarchy._create_definition(root, label.strip()),)
        members = [hierarchy._place_instance(owner, part, value) for part in definitions for value in values]
        pattern = None
        if config['mode'] != 'Quantity':
            root.PlusSchema = max(root.PlusSchema, 7)
            pattern = owner.Document.addObject('App::FeaturePython', 'InstancePattern')
            pattern.addProperty('App::PropertyString', 'InstancePatternFormat', 'Instance pattern')
            pattern.InstancePatternFormat = MARKER
            pattern.addProperty('App::PropertyString', 'Configuration', 'Instance pattern')
            pattern.addProperty('App::PropertyLinkList', 'Members', 'Instance pattern')
            pattern.addProperty('App::PropertyLinkList', 'Seeds', 'Instance pattern')
            pattern.addProperty('App::PropertyLinkSubList', 'References', 'Instance pattern')
            owner.addObject(pattern)
            pattern.Configuration = json.dumps(config)
            pattern.Members = members
            pattern.Seeds = members[::len(values)]
            pattern.References = refs
            pattern.Label = config['mode'] + ' instance pattern'
            pattern.Proxy = Pattern()
            for prop in ('InstancePatternFormat', 'Configuration', 'Members', 'Seeds', 'References'):
                pattern.setEditorMode(prop, 1)
            if App.GuiUp: pattern.Visibility = False
            for member in members: member.setEditorMode('LinkPlacement', 1)
        return members, pattern


def check_edit(pattern, config, refs=()):
    owner = owner_of(pattern)
    if owner is None or not is_pattern(pattern): raise ValueError('The pattern is no longer available')
    document.validate(owner.Document)
    if config['mode'] == 'Quantity': raise ValueError('Use a pattern arrangement when editing a pattern')
    values = placements(resolved_config(owner, config, refs, pattern.Members))
    count(len(values) * len(pattern.Seeds))
    old_count = len(pattern.Members) // len(pattern.Seeds)
    removed = []
    for index in range(len(pattern.Seeds)):
        members = pattern.Members[index * old_count:(index + 1) * old_count]
        removed.extend(members[len(values):])
    for member in pattern.Members:
        for dependent in member.InList:
            if dependent in (owner, pattern): continue
            if member in removed or dependent.TypeId.startswith('Assembly::') or 'JointType' in dependent.PropertiesList:
                raise ValueError('Cannot change this pattern: ' + member.Label + ' is used by ' + dependent.Label)
    # LinkSub consumers can refer through a parent/assembly rather than directly
    # to the member. Resolve those native paths before removing any instance.
    removed_set = set(removed)
    if removed_set:
        if App.GuiUp:
            from . import panel
            if panel._panel:
                for (doc, view), _ in panel._panel._states:
                    try: _, path = panel._panel._context(doc, view)
                    except (ValueError, RuntimeError, ReferenceError): continue
                    if removed_set.intersection(path):
                        raise ValueError('Edit the parent component before removing an instance being edited')
        for doc in App.listDocuments().values():
            for dependent in doc.Objects:
                if dependent == pattern: continue
                for name in dependent.PropertiesList:
                    kind = dependent.getTypeIdOfProperty(name)
                    if 'LinkSub' not in kind: continue
                    value = getattr(dependent, name)
                    references = value if 'List' in kind else [value]
                    for reference in references:
                        if not reference or reference[0] is None: continue
                        base, subs = reference
                        for sub in ([subs] if isinstance(subs, str) else subs):
                            if removed_set.intersection(base.getSubObjectList(sub)):
                                raise ValueError('Cannot reduce this pattern: an instance is used by ' + dependent.Label)
    return owner, values, old_count, removed


def update(pattern, config, refs=()):
    owner, values, old_count, removed = check_edit(pattern, config, refs)
    with document.transaction(owner.Document, 'Edit instance pattern'):
        members = []
        for index, seed in enumerate(pattern.Seeds):
            previous = pattern.Members[index * old_count:(index + 1) * old_count]
            for i, placement in enumerate(values):
                member = previous[i] if i < len(previous) else hierarchy._place_instance(owner, seed.LinkedObject)
                member.LinkPlacement = placement; member.setEditorMode('LinkPlacement', 1)
                members.append(member)
        pattern.Configuration = json.dumps(config); pattern.References = refs; pattern.Members = members
        for member in removed: owner.Document.removeObject(member.Name)
        pattern.touch()
    return members


def validate_pattern(owner, pattern):
    if pattern.TypeId != 'App::FeaturePython' or not is_pattern(pattern) or owner_of(pattern) != owner:
        raise ValueError('Invalid instance pattern ownership')
    members, seeds = list(pattern.Members), list(pattern.Seeds)
    if not seeds or not members or len(members) % len(seeds) or len(set(members)) != len(members):
        raise ValueError('Invalid instance pattern membership')
    config = json.loads(pattern.Configuration)
    if config['mode'] == 'Quantity': raise ValueError('Quantity placements must be independent')
    values = placements(resolved_config(owner, config, pattern.References, members))
    n = len(values)
    if len(members) != n * len(seeds): raise ValueError('Pattern quantity does not match its members')
    for i, seed in enumerate(seeds):
        if seed != members[i * n]: raise ValueError('Invalid pattern source seed')
        for member in members[i * n:(i + 1) * n]:
            if member not in owner.Group or member.TypeId != 'App::Link' or member.LinkedObject != seed.LinkedObject:
                raise ValueError('Pattern members must share their original component definition')


class Pattern:
    def execute(self, obj):
        owner = owner_of(obj)
        if owner is None: return
        config = resolved_config(owner, json.loads(obj.Configuration), obj.References, obj.Members)
        values = placements(config)
        if len(obj.Members) != len(values) * len(obj.Seeds):
            raise ValueError('Edit instance pattern to change its quantity')
        for i, member in enumerate(obj.Members):
            value = values[i % len(values)]
            if not member.LinkPlacement.isSame(value, 1e-9): member.LinkPlacement = value

    def dumps(self): return None
    def loads(self, state): pass
