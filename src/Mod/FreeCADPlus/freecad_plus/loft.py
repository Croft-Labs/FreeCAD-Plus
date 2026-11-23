# SPDX-License-Identifier: LGPL-2.1-or-later
"""Ordered component Loft sections, native solid/sheet kernels and shared persistence."""
import sys
import Part
from . import document, extrusion, modeling, planes

NAME = 'Loft'
VERSION = 'PlusLoftVersion'
PREFIX = 'Loft_'
ERROR = 'LoftError'
LINKS = {'target': 'Target'}
DEFAULTS = dict(output='Solid', operation='New Solid', ruled=False, closed=False, refine=True)
InvalidResult = extrusion.InvalidResult
owner = extrusion.owner


def is_loft(obj):
    return getattr(obj, VERSION, 0) == 1


def settings(feature):
    return {key: getattr(feature, PREFIX + key, default) for key, default in DEFAULTS.items()}


def references(feature):
    return {'target': planes.flatten(feature.Target)[0]} if feature.Target else {}


def profile_reference(ref):
    obj, sub = ref
    if obj.TypeId == 'PartDesign::Body' and Part.splitSubname(sub)[2].startswith('Vertex'):
        picked = obj.Shape.getElement(sub)
        index = next(i for i, vertex in enumerate(obj.Shape.Vertexes) if vertex.isSame(picked))
        return obj.Tip, 'Vertex' + str(index + 1)
    obj, sub = extrusion.profile_reference(ref)
    # Like native Loft, sketch edge picks select its complete section; a vertex
    # pick remains a point section. Other edge picks retain their exact geometry.
    if obj.isDerivedFrom('Sketcher::SketchObject') and not Part.splitSubname(sub)[2].startswith('Vertex'):
        sub = ''
    return obj, sub


def section_shapes(definition, ref, output):
    obj, sub = ref
    if (not obj.isDerivedFrom('Part::Feature') or obj.TypeId.startswith('Part::Datum')
            or obj.TypeId in ('PartDesign::Plane', 'PartDesign::Line', 'PartDesign::Point')):
        raise ValueError('Select a sketch, profile face, curves or a vertex endpoint.')
    shape = planes.shape(definition, ref)
    if shape.ShapeType == 'Vertex':return [shape]
    if shape.Solids or (shape.Faces and shape.ShapeType != 'Face'):
        raise ValueError('Select a section face or curves, not an entire solid or sheet.')
    if shape.ShapeType == 'Face' and not isinstance(shape.Surface, Part.Plane):
        raise ValueError('Loft section faces must be planar.')
    wires = list(shape.Wires)
    free = [edge for edge in shape.Edges if not any(edge.isSame(member) for wire in wires for member in wire.Edges)]
    wires.extend(Part.Wire(group) for group in Part.sortEdges(free))
    if not wires or any(not wire.isValid() or wire.Length < 1e-9 for wire in wires):
        raise ValueError('The section contains no valid curves.')
    if output == 'Solid':
        if any(not wire.isClosed() for wire in wires):
            raise ValueError('Solid Loft requires closed sections. Choose Sheet for open curves.')
        face = Part.makeFace(wires, 'Part::FaceMakerBullseye')
        if face.isNull() or not face.isValid() or len(face.Faces) != 1:
            raise ValueError('Each solid section must enclose one valid planar region, optionally with holes.')
        # Native face wire order consistently places the outer loop before holes.
        wires = list(face.Wires)
    return wires


def validate_profiles(definition, refs, output='Solid'):
    for ref in refs:section_shapes(definition, ref, output)


def validate(definition, refs, links, values, feature=None, *, stored=False):
    v = dict(DEFAULTS, **values)
    if v['output'] not in ('Solid', 'Sheet') or v['operation'] not in extrusion.MODES:
        raise ValueError('Unsupported Loft output or operation.')
    def canonical(items):
        if not stored:return planes.canonical(definition, items)
        if any(obj == definition or document.owned_path(definition, obj) is None for obj, _ in items):
            raise ValueError('Loft references must belong to their component.')
        return items
    refs = [profile_reference(ref) for ref in canonical(refs)]
    if len(refs) < 2:raise ValueError('Select at least two section profiles in loft order.')
    if len(set(refs)) != len(refs):raise ValueError('Use each section once; use Closed to return to the first section.')
    if feature is not None and (not is_loft(feature) or owner(feature) != definition):
        raise ValueError('Edit a Loft owned by this component.')
    validate_profiles(definition, refs, v['output'])
    if v['output'] == 'Sheet':v['operation'] = 'New Solid'
    links = {key: canonical([ref])[0] for key, ref in links.items() if key in LINKS}
    if v['operation'] == 'New Solid':links.clear()
    else:
        target = links.get('target', (None, ''))[0]
        if target is None:raise ValueError('Select the target solid before selecting sections.')
        if target.TypeId == 'PartDesign::Body':target = target.Tip
        if feature and target == references(feature).get('target', (None, ''))[0]:
            if target.Shape.isNull() or not target.Shape.isValid() or len(target.Shape.Solids) != 1:
                raise ValueError('The saved target is no longer one valid solid.')
        else:modeling._target_body(definition, target)
        links['target'] = (target, '')
    document.require_predecessors(definition, feature, refs + list(links.values()))
    return refs, links, v


def evaluate(definition, refs, links, values, feature=None, *, stored=False):
    refs, links, v = validate(definition, refs, links, values, feature, stored=stored)
    sections = [section_shapes(definition, ref, v['output']) for ref in refs]
    count = len(sections[0])
    if any(len(section) != count for section in sections):
        raise ValueError('Sections must have the same number of wires or vertices.')
    if any(shape.ShapeType == 'Vertex' for section in sections[1:-1] for shape in section):
        raise ValueError('A vertex section is only allowed at either end of the loft.')
    if v['closed'] and len(sections) < 3:raise ValueError('Closed Loft requires at least three sections.')
    if v['closed'] and any(shape.ShapeType == 'Vertex' for section in sections for shape in section):
        raise ValueError('Closed Loft cannot have vertex endpoints.')
    shapes = [Part.makeCompound(section) if len(section) > 1 else section[0] for section in sections]
    if v['output'] == 'Solid':
        with extrusion.kernel_document() as scratch:
            body = scratch.addObject('PartDesign::Body', 'EvaluationBody');body.AllowCompound = True
            profiles = []
            for shape in shapes:
                profile = body.newObject('PartDesign::Feature', 'SectionSnapshot');profile.BaseFeature = None
                profile.Shape = extrusion.kernel_snapshot(shape);profiles.append(profile)
            native = body.newObject('PartDesign::AdditiveLoft', 'Evaluation');native.BaseFeature = None
            native.Profile = (profiles[0], [])
            native.Sections = [(profile, ['']) for profile in profiles[1:]]
            native.Ruled = v['ruled'];native.Closed = v['closed'];native.Refine = v['refine']
            scratch.recompute()
            tool = native.AddSubShape.copy();tool.Placement = native.Placement.multiply(tool.Placement)
            if tool.isNull() or not tool.isValid() or len(tool.Solids) != 1:
                raise ValueError('Cannot construct a solid Loft. Check the section order, closure and intersections. ' + native.getStatusString())
    else:
        sheets = [Part.makeLoft([extrusion.kernel_snapshot(section[i]) for section in sections],
                               False, v['ruled'], v['closed']) for i in range(count)]
        tool = sheets[0] if count == 1 else Part.makeCompound(sheets)
        if tool.isNull() or not tool.isValid() or not tool.Faces or tool.Solids or tool.Area < 1e-9:
            raise ValueError('Cannot construct a valid sheet Loft from these sections.')
    target = planes.shape(definition, links['target']) if 'target' in links else None
    # Include all ordered source identities so section reorder invalidates names.
    namespace = 'PlusLoft1_' + '_'.join(str(obj.ID) for obj, _ in refs)
    tool = extrusion.name_tool(tool, refs, feature, target, namespace)
    try:
        result = tool if target is None else target.fuse(tool) if v['operation'] == 'Add' else target.cut(tool)
        if v['refine']:result = result.removeSplitter()
        if result.isNull() or not result.isValid() or (v['output'] == 'Solid' and len(result.Solids) != 1):
            raise ValueError('The operation must produce one valid solid. Check the loft and target contact.')
        if target is not None and abs(result.Volume - target.Volume) < max(1e-7, target.Volume * 1e-10):
            raise ValueError('No material is ' + ('added. Check loft and target contact.' if v['operation'] == 'Add' else
                                                'removed. The loft must intersect the target solid.'))
    except Exception as exc:raise InvalidResult(str(exc), tool) from exc
    return result, tool, [edge for shape in shapes for edge in shape.Edges]


class Loft(extrusion.Extrude):
    @staticmethod
    def engine():return sys.modules[__name__]

    def evaluated(self, obj, definition):
        return evaluate(definition, planes.flatten(obj.ProfileReferences), references(obj), settings(obj), obj, stored=True)


class ViewLoft(extrusion.ViewExtrude):
    def getIcon(self):return ':/icons/PartDesign_AdditiveLoft.svg'

    def doubleClicked(self, view):
        from . import loft_task
        loft_task.show(view.Object)
        return True


Feature = Loft
ViewFeature = ViewLoft


def save(doc, refs, links, values, feature=None):
    return extrusion.save_feature(doc, refs, links, values, feature, sys.modules[__name__])
