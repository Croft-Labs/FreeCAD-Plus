# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative sheet-to-solid offsets, sharing feature ownership and Boolean rules."""
import math
import sys
import Part
from . import document, extrusion, modeling, planes

NAME = 'Thicken'
VERSION = 'PlusThickenVersion'
PREFIX = 'Thicken_'
ERROR = 'ThickenError'
LINKS = {'target': 'Target'}
DEFAULTS = dict(operation='New Solid', thickness=1., direction='Along normal', join='Sharp')
InvalidResult = extrusion.InvalidResult
owner = extrusion.owner


def is_thicken(obj):
    return getattr(obj, VERSION, 0) == 1


def settings(feature):
    return {key: getattr(feature, PREFIX + key, default) for key, default in DEFAULTS.items()}


def references(feature):
    return {key: planes.flatten(getattr(feature, prop))[0]
            for key, prop in LINKS.items() if getattr(feature, prop)}


def profile_reference(ref):
    obj, sub = extrusion.profile_reference(ref)
    if obj.TypeId == 'PartDesign::Body' and not sub:
        if obj.Tip is None:
            raise ValueError('Select a sheet with faces.')
        obj = obj.Tip
    return obj, sub


def validate_profiles(definition, refs):
    if not refs:
        raise ValueError('Select a sheet or connected faces from one sheet.')
    obj = refs[0][0]
    if (not obj.isDerivedFrom('Part::Feature') or obj.isDerivedFrom('PartDesign::Plane')
            or obj.TypeId.startswith('Part::Datum') or not obj.Shape.Faces):
        raise ValueError('Select a sheet or its faces to thicken.')
    if obj.Shape.Solids:
        raise ValueError('Thicken requires a sheet. Use Shell to hollow a solid.')
    if any(other != obj for other, _ in refs):
        raise ValueError('Select connected faces from one sheet; clear the current selection first.')
    for ref in refs:
        shape = planes.shape(definition, ref)
        if not shape.Faces or (ref[1] and shape.ShapeType != 'Face'):
            raise ValueError('Select a sheet or faces, not edges or vertices.')


def validate(definition, refs, links, values, feature=None, *, stored=False):
    v = dict(DEFAULTS, **values)
    v['thickness'] = float(v['thickness'])
    if not math.isfinite(v['thickness']) or v['thickness'] <= 0:
        raise ValueError('Total thickness must be greater than zero and finite.')
    for key, choices in (('operation', extrusion.MODES),
                         ('direction', ('Along normal', 'Opposite normal', 'Symmetric')),
                         ('join', ('Sharp', 'Rounded'))):
        if v[key] not in choices:
            raise ValueError('Unknown Thicken setting: ' + key)
    def canonical(refs):
        if not stored:return planes.canonical(definition, refs)
        # Recompute consumes already-owned saved references, independent of the
        # currently edited view. Interactive intake still checks occurrence access.
        if any(obj == definition or document.owned_path(definition, obj) is None for obj, _ in refs):
            raise ValueError('Thicken references must belong to their component.')
        return refs
    refs = list(dict.fromkeys(profile_reference(ref) for ref in canonical(refs)))
    validate_profiles(definition, refs)
    links = {key: canonical([ref])[0] for key, ref in links.items() if key in LINKS}
    if feature is not None and (not is_thicken(feature) or owner(feature) != definition):
        raise ValueError('Edit a Thicken owned by this component.')
    if v['operation'] == 'New Solid':
        links.clear()
    else:
        target = links.get('target', (None, ''))[0]
        if target is None:
            raise ValueError('Select the target solid before selecting sheets.')
        if target.TypeId == 'PartDesign::Body':
            target = target.Tip
        if feature and target == references(feature).get('target', (None, ''))[0]:
            if target.Shape.isNull() or not target.Shape.isValid() or len(target.Shape.Solids) != 1:
                raise ValueError('The saved target is no longer one valid solid.')
        else:
            modeling._target_body(definition, target)
        links['target'] = (target, '')
    document.require_predecessors(definition, feature, refs + list(links.values()))
    return refs, links, v


def sheet_shape(definition, refs):
    # The whole-sheet reference subsumes individual faces. Sew shared edges;
    # disconnected islands are rejected before the native offset call.
    whole = next((ref for ref in refs if not ref[1]), None)
    faces = [face for ref in ([whole] if whole else refs) for face in planes.shape(definition, ref).Faces]
    connected = {0}
    while True:
        adjacent = {i for i, face in enumerate(faces) if i not in connected
                    and any(edge.isSame(other) or edge.common(other).Length > 1e-7
                            for j in connected for edge in face.Edges for other in faces[j].Edges)}
        if not adjacent:break
        connected.update(adjacent)
    sheet = faces[0] if len(faces) == 1 else Part.makeShell(faces)
    if not sheet.isValid() or len(connected) != len(faces):
        raise ValueError('Select connected faces forming one valid sheet.')
    return sheet


def evaluate(definition, refs, links, values, feature=None, *, stored=False):
    refs, links, v = validate(definition, refs, links, values, feature, stored=stored)
    sheet = sheet_shape(definition, refs)
    join = 2 if v['join'] == 'Sharp' else 0
    distance = v['thickness']
    def offset(amount):
        return sheet.makeOffsetShape(amount, 1e-7, False, False, 0, join, True)
    try:
        if v['direction'] == 'Symmetric':
            tool = offset(distance / 2).fuse(offset(-distance / 2)).removeSplitter()
        else:
            tool = offset(distance if v['direction'] == 'Along normal' else -distance)
        if tool.isNull() or not tool.isValid() or len(tool.Solids) != 1:
            raise ValueError('The offset must produce one valid solid.')
    except Exception as exc:
        raise ValueError('Cannot thicken this sheet at the requested thickness. ' + str(exc)) from exc
    target = planes.shape(definition, links['target']) if 'target' in links else None
    tool = extrusion.name_tool(tool, refs, feature, target, 'PlusThicken1')
    try:
        result = tool if target is None else target.fuse(tool) if v['operation'] == 'Add' else target.cut(tool)
        result = result.removeSplitter()
        if result.isNull() or not result.isValid() or len(result.Solids) != 1:
            raise ValueError('The operation must produce one solid; check sheet and target contact.')
        if target is not None and abs(result.Volume - target.Volume) < max(1e-7, target.Volume * 1e-10):
            raise ValueError('No material is ' + ('added.' if v['operation'] == 'Add' else 'removed.'))
    except Exception as exc:
        raise InvalidResult(str(exc), tool) from exc
    return result, tool, sheet.Edges


class Thicken(extrusion.Extrude):
    @staticmethod
    def engine():
        return sys.modules[__name__]

    def evaluated(self, obj, definition):
        return evaluate(definition, planes.flatten(obj.ProfileReferences), references(obj), settings(obj), obj, stored=True)


class ViewThicken(extrusion.ViewExtrude):
    def getIcon(self):
        return ':/icons/Part_Offset.svg'

    def doubleClicked(self, view):
        from . import thicken_task
        thicken_task.show(view.Object)
        return True


Feature = Thicken
ViewFeature = ViewThicken


def save(doc, refs, links, values, feature=None):
    return extrusion.save_feature(doc, refs, links, values, feature, sys.modules[__name__])
