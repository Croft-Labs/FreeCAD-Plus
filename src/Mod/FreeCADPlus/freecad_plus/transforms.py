# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative transformations of complete, component-owned solids and sheets."""
from . import result_names
import json
import math
import uuid

import FreeCAD as App
import Part
from . import document, planes, modeling, derived_geometry

KINDS = ('Mirror', 'Linear pattern', 'Polar pattern', 'Multi-transform')
ICONS = ('PartDesign_Mirrored', 'PartDesign_LinearPattern', 'PartDesign_PolarPattern', 'PartDesign_MultiTransform')


def source(owner, ref, consumer=None):
    obj, _ = planes.canonical(owner, [ref])[0]
    # A Body is a convenience pick. Store its finished feature rather than a
    # changing Tip link which could later become a dependency on this result.
    if obj.TypeId == 'PartDesign::Body':
        obj = obj.Tip
    elif obj.getParentGeoFeatureGroup() and obj.getParentGeoFeatureGroup().TypeId == 'PartDesign::Body':
        body = obj.getParentGeoFeatureGroup()
        if consumer is None:
            obj = body.Tip
    if obj is None:
        raise ValueError('Choose a finished body or sheet')
    if derived_geometry.object_kind(obj) not in ('body','surface'):
        raise ValueError('Choose a finished body or sheet, not a datum or sketch')
    route = document.owned_path(owner, obj)
    if not route or any(o.TypeId == 'App::Link' for o in route):
        raise ValueError('Choose a body or sheet owned by the active component')
    document.require_predecessors(owner, consumer, [(obj, '')])
    shape = planes.shape(owner, (obj, ''))
    if not shape.Faces or not shape.isValid():
        raise ValueError('Choose a valid body or sheet')
    return obj, ''


def evaluate(owner, refs, steps, merge, consumer=None):
    if not refs:
        raise ValueError('Select a body or sheet to transform')
    if not steps:
        raise ValueError('Add at least one transformation')
    shapes = []
    for ref in refs:
        # Saved references remain on the exact finished source, even if another
        # operation is subsequently appended to its native Body.
        planes.canonical(owner, [ref]); document.require_predecessors(owner, consumer, [ref])
        shape = planes.shape(owner, ref)
        if not shape.Faces or not shape.isValid():
            raise ValueError('A source is missing or no longer a valid body or sheet')
        shapes.append(shape)
    if merge and len({bool(s.Solids) for s in shapes}) > 1:
        raise ValueError('Merge bodies and sheets separately')
    for step in steps:
        kind = step['kind']; axis = int(step.get('axis', 0))
        if kind not in KINDS[:3] or axis not in range(4):
            raise ValueError('Invalid transformation settings')
        ref = step.get('ref')
        origin = App.Vector(*step.get('center', (0, 0, 0)))
        if axis == 3:
            if not ref:
                raise ValueError('Select a plane or axis reference')
            planes.canonical(owner, [ref]); document.require_predecessors(owner, consumer, [ref])
            description = planes.describe(owner, ref)
            if description[0] != ('plane' if kind == 'Mirror' else 'line'):
                raise ValueError('Choose a planar face/plane' if kind == 'Mirror' else 'Choose a straight edge/axis')
            _, origin, direction = description
        else:
            axes = ((0,0,1), (0,1,0), (1,0,0)) if kind == 'Mirror' else ((1,0,0), (0,1,0), (0,0,1))
            direction = App.Vector(*axes[axis])
        if kind == 'Mirror':
            if len(shapes)*2>10000:raise ValueError('This transformation exceeds 10,000 copies; reduce the steps')
            offset = float(step.get('offset', 0))
            if not math.isfinite(offset):raise ValueError('Offset must be finite')
            point = origin + direction * offset
            # Native mirror preserves analytic circles/cylinders. A general
            # geometry transform converts them to approximated B-splines.
            mirrored = [s.mirror(point, direction) for s in shapes]
            shapes = shapes + mirrored
        else:
            count = int(step.get('count', 2)); value = float(step.get('value', 10))
            if not 2 <= count <= 10000 or not math.isfinite(value) or value <= 0:
                raise ValueError('Use at least two occurrences and a positive finite spacing or angle')
            if len(shapes) * count > 10000:
                raise ValueError('This transformation exceeds 10,000 copies; reduce the counts')
            if kind == 'Linear pattern':
                spacing = value / (count-1) if step.get('measure', 0) else value
            else:
                spacing = value if step.get('measure', 0) else value / (count if abs(value-360)<1e-7 else count-1)
            if step.get('reverse'):spacing = -spacing
            copies = []
            for i in range(count):
                for shape in shapes:
                    copy = shape.copy()
                    if kind == 'Linear pattern':copy.translate(direction * (spacing*i))
                    else:copy.rotate(origin, direction, spacing*i)
                    copies.append(copy)
            shapes = copies
    if merge:
        result = shapes[0].multiFuse(shapes[1:]).removeSplitter() if len(shapes)>1 else shapes[0]
        shapes = [result]
    if any(s.isNull() or not s.isValid() for s in shapes):
        raise ValueError('These settings do not produce valid geometry')
    return shapes


def settings(feature):
    steps = json.loads(feature.TransformSteps)
    refs = planes.flatten(feature.TransformReferences)
    for step in steps:
        index = step.pop('reference_index', None)
        if index is not None:step['ref'] = refs[index]
    return steps


class Transform:
    def __init__(self, obj):
        for typename, name in (('String','TransformKind'), ('String','TransformSteps'),
                               ('String','TransformGroup'), ('Integer','TransformIndex'),
                               ('Bool','MergeResults'), ('LinkSubListGlobal','TransformSources'),
                               ('LinkSubListGlobal','TransformReferences'), ('String','GeometryError')):
            obj.addProperty('App::Property'+typename, name, 'Transformation')
            obj.setEditorMode(name, 1 if name == 'GeometryError' else 2)
        obj.Proxy = self

    def execute(self, obj):
        try:
            owner = derived_geometry.owner(obj)
            shapes = evaluate(owner, planes.flatten(obj.TransformSources), settings(obj), obj.MergeResults)
            shape = shapes[obj.TransformIndex]
            parent = obj.getParentGeoFeatureGroup()
            if parent.TypeId == 'PartDesign::Body':
                frame = parent.getGlobalPlacement().inverse().multiply(owner.getGlobalPlacement())
                shape.Placement = frame.multiply(shape.Placement)
                parent.AllowCompound = len(shape.Solids) > 1
            obj.Shape = shape; obj.GeometryError = ''
        except Exception as exc:
            obj.Shape = Part.Shape(); obj.GeometryError = str(exc)
            raise

    def dumps(self):return None
    def loads(self, state):pass


class ViewTransform:
    def __init__(self, view):view.Proxy = self
    def attach(self, view):self.obj = view.Object
    def getIcon(self):return ':/icons/'+ICONS[KINDS.index(self.obj.TransformKind)]+'.svg'
    def doubleClicked(self, view):
        from .transform_task import show
        show(feature=view.Object);return True
    def dumps(self):return None
    def loads(self, state):pass


def save(doc, refs, steps, merge=True, kind='Linear pattern', label=None, feature=None, result_labels=None):
    owner, _ = modeling._context(doc)
    if feature and derived_geometry.owner(feature) != owner:
        raise ValueError('Edit a transformation in the active component')
    shapes = evaluate(owner, refs, steps, merge, feature)
    if result_labels is not None and len(result_labels)!=len(shapes):raise ValueError('Review the name of each result.')
    old = sorted((o for o in owner.Document.Objects if feature and
                  getattr(o, 'TransformGroup', None) == feature.TransformGroup and
                  derived_geometry.owner(o) == owner), key=lambda o:o.TransformIndex)
    for obj in old[len(shapes):]:
        if any(o not in old and o != obj.getParentGeoFeatureGroup() for o in obj.InList):
            raise ValueError('A removed copy has dependent features; keep that occurrence')
    encoded = []; references = []
    for step in steps:
        value = dict(step); ref = value.pop('ref', None)
        if ref:
            value['reference_index'] = len(references);references.append(ref)
        encoded.append(value)
    results = []; group = feature.TransformGroup if feature else str(uuid.uuid4())
    with document.transaction(owner.Document, 'Edit transformation' if feature else kind):
        for i, shape in enumerate(shapes):
            obj = old[i] if i < len(old) else None
            if obj is None:
                if shape.Solids:
                    body = owner.newObject('PartDesign::Body', 'Body');body.AllowCompound = len(shape.Solids)>1
                    obj = body.newObject('PartDesign::FeaturePython', 'Transform')
                else:obj = owner.newObject('Part::FeaturePython', 'Transform')
                Transform(obj);ViewTransform(obj.ViewObject)
            elif bool(obj.Shape.Solids) != bool(shape.Solids):
                raise ValueError('Keep the original result type when editing')
            obj.TransformKind=kind;obj.TransformGroup=group;obj.TransformIndex=i
            obj.TransformSources=planes.links(refs);obj.TransformReferences=planes.links(references)
            obj.TransformSteps=json.dumps(encoded);obj.MergeResults=merge
            if result_labels is not None:result_names.assign(obj,result_labels[i])
            else:obj.Label=label or kind
            obj.touch();results.append(obj)
        for obj in old[len(shapes):]:
            parent=obj.getParentGeoFeatureGroup();owner.Document.removeObject(obj.Name)
            if parent.TypeId=='PartDesign::Body':owner.Document.removeObject(parent.Name)
        owner.Document.recompute()
        for obj in results:
            if obj.GeometryError or obj.Shape.isNull():raise ValueError(obj.GeometryError or 'Transformation failed')
        for obj, _ in refs:
            obj.Visibility=False
            parent=obj.getParentGeoFeatureGroup()
            if parent and parent.TypeId=='PartDesign::Body':parent.Visibility=False
    return results
