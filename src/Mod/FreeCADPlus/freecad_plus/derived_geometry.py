# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative whole-object promotion and parent-owned face extraction."""
import FreeCAD as App
import Part
from . import document, display, hierarchy

MARKER = 'FreeCADPlus.DerivedGeometry.1'
EXTRACT_MARKER = 'FreeCADPlus.DerivedGeometry.2'
KINDS = ('body', 'surface', 'sketch', 'plane', 'curve', 'point')


def is_derived(obj):
    return getattr(obj, 'DerivedGeometryFormat', None) in (MARKER, EXTRACT_MARKER)


def owner(obj):
    current = obj
    while current is not None:
        current = current.getParentGeoFeatureGroup()
        if current is not None and current.TypeId == 'App::Part': return current
    raise ValueError('The derived geometry no longer belongs to a component')


def target(ref):
    base, sub = ref
    if base is None: raise ValueError('The source is missing. Edit this feature to choose a source.')
    result = base.getSubObject(sub, 1) if sub else base
    if result is None: raise ValueError('The source object or topology is missing. Edit this feature to repair it.')
    return result


def object_kind(obj, shape=None):
    if obj.isDerivedFrom('Sketcher::SketchObject'): return 'sketch'
    if (obj.TypeId in ('App::Plane', 'PartDesign::Plane', 'Part::Plane')
            or getattr(obj, 'PlusPlaneVersion', 0) == 1
            or (is_derived(obj) and obj.GeometryKind == 'plane')): return 'plane'
    if obj.TypeId in ('App::Part', 'App::Link', 'App::Origin') or obj.TypeId.startswith('Assembly::'):
        raise ValueError('Choose a whole geometric object, not a component or collector')
    shape = shape if shape is not None else getattr(obj, 'Shape', None)
    if shape is None or shape.isNull(): raise ValueError('The selected object has no geometric result')
    if shape.Solids: return 'body'
    if shape.Faces: return 'surface'
    if shape.Edges: return 'curve'
    if shape.Vertexes: return 'point'
    raise ValueError('The selected object has no supported geometric result')


def whole_source(definition, ref, *, admission=True):
    link, sub = ref
    if link is None or link.TypeId != 'App::Link' or link not in definition.Group:
        raise ValueError('Clone accepts objects from direct child occurrences only')
    if any(Part.splitSubname(sub)[1:]):
        raise ValueError('Clone accepts whole objects only. Clone the body, then use Extract geometry for faces.')
    if admission and display.state(link)[0] == 'Excluded':
        raise ValueError('Excluded children cannot supply new Clone inputs')
    obj = target(ref)
    route = document.owned_path(link.LinkedObject, obj)
    if not route or any(o.TypeId == 'App::Link' for o in route):
        raise ValueError('Choose an object owned by a direct child, not a grandchild or whole component')
    canonical = ''.join(o.Name + '.' for o in route)
    if sub.rstrip('.') != canonical.rstrip('.'):
        raise ValueError('The source occurrence path changed; choose the whole object again')
    if 'Invalid' in obj.State or getattr(obj, 'GeometryError', ''):
        raise ValueError('Repair the source object before cloning its geometry')
    return obj


def face_source(definition, ref):
    obj = target(ref)
    base, sub = ref
    route = document.owned_path(definition, obj)
    if not route or any(o.TypeId == 'App::Link' for o in route):
        raise ValueError('Extract faces from parent-owned geometry. Clone the child object first.')
    if base != obj or Part.splitSubname(sub)[0]:
        raise ValueError('Choose a face on an object owned by the edited component')
    if not Part.splitSubname(sub)[2].startswith('Face'):
        raise ValueError('Extract geometry requires a face')
    if 'Invalid' in obj.State or getattr(obj, 'GeometryError', ''):
        raise ValueError('Repair the source object before extracting its faces')
    return obj


def canonical(doc, definition, edit_path, obj, sub, extract=False):
    """Convert an unresolved native pick to an exact local occurrence or object."""
    if obj == document.validate(doc) and edit_path:
        prefix = hierarchy.subname(edit_path)
        if not sub.startswith(prefix): raise ValueError('Choose geometry within the edited component')
        local = sub[len(prefix):]
    elif obj == definition: local = sub
    else:
        from . import editing, isolation
        session = isolation.current(editing._view(doc))
        if session and obj == session.anchor_definition() and session.definition() == definition:
            prefix = hierarchy.subname(tuple(isolation._resolve(ref) for ref in session.edit_path))
            if not sub.startswith(prefix):raise ValueError('Choose geometry within the edited component')
            return canonical(doc, definition, edit_path, definition, sub[len(prefix):], extract)
        route = document.owned_path(definition, obj)
        if route is None: raise ValueError('Select the source through its component occurrence')
        local = ''.join(o.Name + '.' for o in route) + sub
    if not extract:
        name, _, tail = local.partition('.')
        link = next((o for o in definition.Group if o.Name == name), None)
        object_path, mapped, element = Part.splitSubname(tail)
        if element or mapped:
            if not element.startswith(('Face', 'Edge', 'Vertex')):
                raise ValueError('Pick geometry on a whole source object')
            if link is None or link.TypeId != 'App::Link':
                raise ValueError('Clone accepts objects from direct child occurrences only')
            # Validate the actual picked topology before dropping its suffix.
            picked = Part.getShape(link, tail, needSubElement=True)
            if picked.isNull():raise ValueError('The picked source geometry is no longer available')
            source = whole_source(definition, (link, object_path))
            body = source.getParentGeoFeatureGroup()
            if body is not None and body.TypeId == 'PartDesign::Body' and body.Tip == source:
                object_path = ''.join(o.Name + '.' for o in document.owned_path(link.LinkedObject, body))
            tail = object_path
        ref = (link, tail); whole_source(definition, ref)
        return ref
    resolved = definition.getSubObject(local, 1)
    _, mapped, element = Part.splitSubname(local)
    ref = (resolved, Part.joinSubname('', mapped, element))
    face_source(definition, ref)
    return ref


def evaluate(definition, ref, operation='Clone', *, feature=None, admission=True):
    source = whole_source(definition, ref, admission=admission) if operation == 'Clone' else face_source(definition, ref)
    if feature is not None:
        if (source == feature or feature in source.OutListRecursive
                or feature == ref[0] or feature in ref[0].OutListRecursive):
            raise ValueError('A derived feature cannot use itself or a downstream source')
        document.require_predecessors(definition, feature, [ref])
    if operation == 'Extract':
        from .planes import shape as local_shape
        shape = local_shape(definition, ref)
        if shape.ShapeType != 'Face': raise ValueError('The selected face is missing or no longer a face')
        return source, 'surface', shape
    kind = object_kind(source)
    link, sub = ref
    if kind == 'plane':
        # Preserve an explicit plane frame, including native datum/origin planes.
        frame = link.getSubObject(sub, 3)
        if source.TypeId == 'App::Plane':
            shape = Part.makePlane(60, 45, App.Vector(-10,-10,0)); shape.Placement = frame
        else:
            shape = Part.getShape(link, sub, needSubElement=True)
            if shape.isNull():
                shape = Part.makePlane(60,45,App.Vector(-10,-10,0)); shape.Placement = frame
    else: shape = Part.getShape(link, sub, needSubElement=True)
    if shape.isNull() or not shape.isValid(): raise ValueError('The source has no valid complete geometry')
    return source, kind, shape.copy()


def structural_check(obj):
    if (not is_derived(obj) or obj.DerivedOperation not in ('Clone','Extract')
            or obj.GeometryKind not in KINDS
            or obj.getTypeIdOfProperty('Source') != 'App::PropertyLinkSubGlobal'
            or obj.getTypeIdOfProperty('SourceObject') != 'App::PropertyXLink'):
        raise ValueError('Invalid derived geometry metadata')
    expected = ('PartDesign::FeaturePython' if obj.GeometryKind == 'body' else
                'Sketcher::SketchObjectPython' if obj.GeometryKind == 'sketch' else 'Part::FeaturePython')
    if obj.TypeId != expected or (obj.DerivedOperation == 'Extract' and obj.GeometryKind != 'surface'):
        raise ValueError('Invalid derived geometry result type')
    if obj.DerivedGeometryFormat == EXTRACT_MARKER:
        if (obj.DerivedOperation != 'Extract'
                or obj.getTypeIdOfProperty('ExtractSources') != 'App::PropertyLinkSubListGlobal'
                or obj.getTypeIdOfProperty('ExtractSourceObjects') != 'App::PropertyLinkListGlobal'
                or obj.getTypeIdOfProperty('ExtractFaceCount') != 'App::PropertyInteger'
                or obj.getTypeIdOfProperty('JoinSurfaces') != 'App::PropertyBool'):
            raise ValueError('Invalid extracted surface metadata')


def external_source(obj):
    """The only permitted foreign dependency is the explicitly promoted object."""
    structural_check(obj)
    source = obj.SourceObject
    if source is None or source.Document == obj.Document: return []
    definition = owner(obj); ref = saved_ref(obj)
    link = ref[0]
    if (obj.DerivedOperation != 'Clone' or link is None or link not in definition.Group
            or link.TypeId != 'App::Link'
            or not document.owned_path(link.LinkedObject, source)):
        raise ValueError('Unsupported cross-file derived geometry source')
    return [source]


def saved_ref(obj):
    base, subs = obj.Source if obj.Source else (None, [])
    return base, subs[0] if subs else ''


def saved_refs(obj):
    if obj.DerivedGeometryFormat == EXTRACT_MARKER:
        refs = [(base, sub) for base, subs in obj.ExtractSources for sub in subs]
        # Link-list properties may drop deleted objects. Keep missing inputs
        # visible and invalid until explicitly repaired instead of shrinking a shell.
        return refs + [(None, '')] * max(0, obj.ExtractFaceCount - len(refs))
    return [saved_ref(obj)]


def joined(obj):
    return obj is not None and obj.DerivedGeometryFormat == EXTRACT_MARKER and obj.JoinSurfaces


def revision(obj):
    """Capture all saved sources/options, including their original target identities."""
    return (tuple(saved_refs(obj)), saved_ref(obj), obj.SourceObject,
            tuple(obj.ExtractSourceObjects) if obj.DerivedGeometryFormat == EXTRACT_MARKER else (),
            joined(obj))


def joined_surface(faces):
    if not faces:
        raise ValueError('Choose at least one face')
    if len(faces) == 1:
        return faces[0]
    if any(face.common(other).Area > 1e-10
           for i, face in enumerate(faces) for other in faces[:i]):
        raise ValueError('Cannot join overlapping surfaces. Remove duplicate or overlapping faces, '
                         'or clear Join surfaces to extract them separately.')
    # Part.getShape returns copies in the component frame. Edges from distinct
    # copies/objects can coincide without sharing a native TShape identity.
    reached = {0}
    while True:
        adjacent = {i for i, face in enumerate(faces) if i not in reached
                    and any(edge.isSame(other) or edge.common(other).Length > 1e-7
                            for j in reached for edge in face.Edges for other in faces[j].Edges)}
        if not adjacent:
            break
        reached.update(adjacent)
    if len(reached) != len(faces):
        raise ValueError('Cannot join these surfaces: the selection contains disconnected groups. '
                         'Select faces connected by shared edges, or clear Join surfaces to extract them separately.')
    # Native shell construction sews copied coincident boundaries when needed.
    # Keep a shell even if all faces of a closed solid were selected.
    result = Part.makeShell(faces)
    if (result.ShapeType != 'Shell' or not result.isValid() or result.Solids
            or len(result.Faces) != len(faces)):
        raise ValueError('These faces cannot form one valid joined surface. '
                         'Remove overlapping or branching faces, or clear Join surfaces.')
    return result


def evaluate_extract(definition, refs, join, feature=None):
    values = [evaluate(definition, ref, 'Extract', feature=feature) for ref in refs]
    if not values:
        raise ValueError('Choose at least one face')
    return values, joined_surface([value[2] for value in values]) if join else None


def set_extract_sources(obj, refs, sources, join):
    for kind, name in (('App::PropertyLinkSubListGlobal', 'ExtractSources'),
                       ('App::PropertyLinkListGlobal', 'ExtractSourceObjects'),
                       ('App::PropertyInteger', 'ExtractFaceCount'),
                       ('App::PropertyBool', 'JoinSurfaces')):
        if name not in obj.PropertiesList:
            obj.addProperty(kind, name, 'Derived geometry')
        obj.setEditorMode(name, 2)
    obj.ExtractSources = [(base, [sub]) for base, sub in refs]
    obj.ExtractSourceObjects = list(dict.fromkeys(sources))
    obj.ExtractFaceCount = len(refs)
    obj.JoinSurfaces = join
    obj.DerivedGeometryFormat = EXTRACT_MARKER


def label_for(kind, operation='Clone'):
    return ('cloned ' if operation == 'Clone' else 'extracted ') + kind


def allocate_label(definition, name):
    names = {o.Label for o in definition.Document.Objects}
    if name not in names: return name
    index = 2
    while name + ' (' + str(index) + ')' in names: index += 1
    return name + ' (' + str(index) + ')'


class Derived:
    def __init__(self, obj, operation, kind):
        obj.addProperty('App::PropertyString', 'DerivedGeometryFormat', 'Derived geometry').DerivedGeometryFormat = MARKER
        obj.addProperty('App::PropertyString', 'DerivedOperation', 'Derived geometry').DerivedOperation = operation
        obj.addProperty('App::PropertyString', 'GeometryKind', 'Derived geometry').GeometryKind = kind
        obj.addProperty('App::PropertyLinkSubGlobal', 'Source', 'Derived geometry')
        obj.addProperty('App::PropertyXLink', 'SourceObject', 'Derived geometry')
        obj.addProperty('App::PropertyString', 'GeometryError', 'Derived geometry')
        for name in ('DerivedGeometryFormat','DerivedOperation','GeometryKind','Source','SourceObject'):
            obj.setEditorMode(name, 2)
        obj.setEditorMode('GeometryError',1); obj.setEditorMode('Placement',1)
        obj.Proxy = self

    def execute(self, obj):
        try:
            definition = owner(obj)
            if obj.DerivedGeometryFormat == EXTRACT_MARKER:
                structural_check(obj)
                refs = saved_refs(obj)
                if not refs or refs[0] != saved_ref(obj):
                    raise ValueError('The original source is missing or changed. Edit this feature to repair it.')
                if not obj.JoinSurfaces and len(refs) != 1:
                    raise ValueError('A separate extracted surface must have exactly one source face')
                values, shell = evaluate_extract(definition, refs, obj.JoinSurfaces)
                sources = list(dict.fromkeys(value[0] for value in values))
                if sources != list(obj.ExtractSourceObjects):
                    raise ValueError('An original source is missing or replaced. Edit this feature to repair it.')
                source, kind, shape = values[0]
                if obj.JoinSurfaces:shape = shell
            else:
                source, kind, shape = evaluate(definition, saved_ref(obj), obj.DerivedOperation, admission=False)
            if source != obj.SourceObject:
                raise ValueError('The original source is missing or replaced. Edit this feature to repair it.')
            if kind != obj.GeometryKind:
                raise ValueError('The source geometry type changed. Choose another ' + obj.GeometryKind + '.')
            if kind == 'sketch':
                geometry = [g.copy() for i,g in enumerate(source.Geometry) if not source.getConstruction(i)]
                # No source constraints, expressions or construction operations are copied.
                obj.Geometry = geometry
                container = obj.getParentGeoFeatureGroup()
                frame = container.getGlobalPlacement().inverse().multiply(definition.getGlobalPlacement())
                obj.Placement = frame.multiply(saved_ref(obj)[0].getSubObject(saved_ref(obj)[1],3))
                obj.solve()
            else:
                if kind == 'body':
                    body = obj.getParentGeoFeatureGroup()
                    transform = body.getGlobalPlacement().inverse().multiply(definition.getGlobalPlacement())
                    placement = obj.BaseFeature.Placement if obj.BaseFeature else App.Placement()
                    source_frame = App.Placement(shape.Placement)
                    shape.Placement = App.Placement()
                    shape = shape.transformGeometry(placement.inverse().multiply(transform).multiply(source_frame).toMatrix())
                    shape.Placement = placement
                frame = App.Placement(shape.Placement)
                obj.Shape = shape
                obj.Placement = frame
            obj.GeometryError = ''
            if kind == 'sketch': return False  # Native Sketcher builds the shape from unconstrained geometry.
        except Exception as exc:
            if obj.GeometryKind == 'sketch':
                obj.Geometry = []
            obj.Shape = Part.Shape()
            obj.GeometryError = str(exc)
            raise

    def dumps(self): return None
    def loads(self, state): pass


class ViewDerived:
    def __init__(self, view): view.Proxy = self
    def getIcon(self): return ':/icons/PartDesign_ShapeBinder.svg'
    def doubleClicked(self, view):
        from .clone_task import show
        show(feature=view.Object)
        return True
    def dumps(self): return None
    def loads(self, state): pass


def save(doc, refs, operation='Clone', feature=None, *, join=False):
    from . import modeling
    definition, _ = modeling._context(doc)
    refs = list(dict.fromkeys(refs))
    if not refs or (feature is not None and operation != 'Extract' and len(refs) != 1):
        raise ValueError('Choose one source when editing' if feature else 'Choose at least one source')
    if feature is not None:
        if not is_derived(feature) or owner(feature) != definition or feature.DerivedOperation != operation:
            raise ValueError('Edit a derived result owned by this component')
    values = [evaluate(definition, ref, operation, feature=feature) for ref in refs]
    if operation == 'Extract' and join:
        joined_surface([value[2] for value in values])  # Reject before opening an Undo transaction.
    if feature is not None and values[0][1] != feature.GeometryKind:
        raise ValueError('Choose another ' + feature.GeometryKind + ' to preserve this result and its references')
    result = []
    with document.transaction(definition.Document, ('Edit ' if feature else '') + operation + ' geometry'):
        root = document.validate(definition.Document); root.PlusSchema = max(root.PlusSchema,8)
        batches = [(refs, values)] if operation == 'Extract' and join else [([ref], [value]) for ref, value in zip(refs, values)]
        for index, (batch_refs, batch_values) in enumerate(batches):
            ref = batch_refs[0];source, kind, shape = batch_values[0]
            obj = feature if index == 0 else None
            if obj is None:
                if kind == 'body':
                    body = definition.newObject('PartDesign::Body','Body'); body.AllowCompound = len(shape.Solids)>1
                    obj = body.newObject('PartDesign::FeaturePython','Clone')
                else:
                    typename = 'Sketcher::SketchObjectPython' if kind == 'sketch' else 'Part::FeaturePython'
                    obj = definition.newObject(typename,'Extract' if operation=='Extract' else 'Clone')
                Derived(obj,operation,kind); ViewDerived(obj.ViewObject)
                obj.Label = allocate_label(definition,label_for(kind,operation))
            obj.Source = (ref[0],[ref[1]]); obj.SourceObject = source; obj.touch()
            if operation == 'Extract':
                set_extract_sources(obj, batch_refs, [value[0] for value in batch_values], join)
            result.append(obj)
        definition.Document.recompute()
        for obj in result:
            if obj.GeometryError or obj.Shape.isNull() or 'Invalid' in obj.State:
                raise ValueError(obj.GeometryError or obj.Label + ' failed to recompute: ' + str(obj.State))
    return result
