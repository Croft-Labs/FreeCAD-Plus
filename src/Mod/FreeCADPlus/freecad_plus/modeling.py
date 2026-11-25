# SPDX-License-Identifier: LGPL-2.1-or-later
"""Feature-centered services and transaction adapters for existing native commands.

Sketches start in the edited component. A solid-producing operation supplies its
native Body internally, in the same transaction as the feature. Add/Subtract
resolve an owned result feature; they never infer a target from the active Body.
"""
import math

import FreeCAD as App
import FreeCADGui as Gui

from . import document, editing, geometry, hierarchy


def _context(doc):
    definition, path = editing.context_path(doc)
    if App.getActiveTransaction() or any(owner.HasPendingTransaction
                                         for owner in App.listDocuments().values()):
        raise ValueError('Finish the current operation first')
    return definition, path


def new_sketch(doc):
    """Create a component-owned sketch without requiring or creating a Body."""
    definition, path = _context(doc)
    with document.transaction(definition.Document, 'Create feature-centered sketch'):
        sketch = definition.newObject('Sketcher::SketchObject', 'Sketch')
    editing._restore(doc, definition, path)
    return sketch


def extrude_new_solid(doc, sketch, length):
    """Extrude an unconsumed component sketch by a positive length in millimeters.

    Return the native Pad feature. Its internal Body and profile ownership are
    committed together, or rolled back together on failure/Undo. Existing native
    body-centered chains are never adopted or modified by this entry point.
    """
    return extrude(doc, sketch, length)


def extrude(doc, sketch, length, *, operation='new', target=None):
    """Create a new solid, or add/subtract against an explicit current result."""
    definition, path = _context(doc)
    _require_profile(definition, sketch)
    _require_operation(definition, operation, target)
    length = float(length)
    if not math.isfinite(length) or length <= 0:
        raise ValueError('Extrusion length must be finite and greater than zero')

    with document.transaction(definition.Document, 'Extrude component sketch'):
        feature = _create_extrusion(definition, sketch, length, operation=operation, target=target)
        if (feature.Shape.isNull() or not feature.Shape.isValid()
                or not feature.Shape.Solids or 'Invalid' in feature.State
                or (not feature.getParentGeoFeatureGroup().AllowCompound
                    and len(feature.Shape.Solids) != 1)):
            raise ValueError('The extrusion must produce one valid solid')
        sketch.Visibility = False
    editing._restore(doc, definition, path)
    return feature


def _require_profile(definition, sketch):
    if (sketch not in definition.Group or not sketch.isDerivedFrom('Sketcher::SketchObject')
            or sketch.getParentGeoFeatureGroup() != definition):
        raise ValueError('Use an unconsumed sketch owned by the edited component')
    geometry.require_modeling_inputs(definition, [(sketch, '')])


def _target_body(definition, target):
    if target is None or document.owned_path(definition, target) is None:
        raise ValueError('Select a result owned by the edited component')
    body = target.getParentGeoFeatureGroup()
    if (not target.isDerivedFrom('PartDesign::Feature') or body is None
            or body.TypeId != 'PartDesign::Body' or body not in definition.Group
            or body.Tip != target):
        raise ValueError('Select the current solid result, not an earlier feature or a Boolean tool')
    geometry.require_modeling_inputs(definition, [(target, '')])
    if ('Invalid' in target.State or target.Shape.isNull() or not target.Shape.isValid()
            or len(target.Shape.Solids) != 1):
        raise ValueError('The selected target must be one valid solid')
    return body


def _require_operation(definition, operation, target):
    if operation not in ('new', 'add', 'subtract'):
        raise ValueError('Unknown extrusion operation')
    if operation == 'new':
        if target is not None:
            raise ValueError('A new solid does not use a target')
    else:
        _target_body(definition, target)


def _create_extrusion(definition, sketch, length, subelements=(), *, operation='new', target=None):
    """Native mutations shared by atomic API calls and dialog-owned transactions."""
    body = _target_body(definition, target) if target is not None else None
    placement = None
    if body is None:
        body = definition.newObject('PartDesign::Body', 'Body')
        body.AllowCompound = False
    elif sketch.MapMode == 'Deactivated':
        # Keep the sketch in the same component-space position when the target's
        # internal Body has a nonidentity placement. Attached sketches recompute
        # their placement through the native attachment engine instead.
        placement = body.getGlobalPlacement().inverse().multiply(sketch.getGlobalPlacement())
    # The profile must share the native Body scope; retain its original identity.
    definition.removeObject(sketch)
    body.addObject(sketch)
    if placement is not None:
        sketch.Placement = placement
    kind = 'Pocket' if operation == 'subtract' else 'Pad'
    feature = body.newObject('PartDesign::' + kind, kind)
    feature.Profile = (sketch, list(subelements))
    feature.Length = length
    feature.ReferenceAxis = (sketch, ['N_Axis'])
    if target is not None:
        for prop in ('ShapeAppearance', 'LineColor', 'PointColor', 'Transparency', 'DisplayMode'):
            setattr(feature.ViewObject, prop, getattr(target.ViewObject, prop))
    definition.Document.recompute()
    return feature


def preflight_sketch():
    """Validate original selection before native attachment selection resolves it."""
    definition, _ = _context(Gui.activeDocument().Document)
    geometry.require_modeling_inputs(definition)


def _enter_editor(doc, definition, path, feature):
    editing._restore(doc, definition, path)
    route = ''.join(obj.Name + '.' for obj in document.owned_path(definition, feature))
    parent = definition
    if path:
        parent = document.validate(doc)
        route = hierarchy.subname(path) + route
    body = feature.getParentGeoFeatureGroup()
    if body is not None and body.TypeId == 'PartDesign::Body':
        # Native task reference collectors also consult the active Body. Point
        # them at this result, even when it is not the component's last Body.
        body_route = route[:-(len(feature.Name) + 1)]
        Gui.getDocument(doc.Name).activeView().setActiveObject('pdbody', parent, body_route)
    if not Gui.getDocument(doc.Name).setEdit(parent, 0, route):
        raise ValueError('The native feature editor could not be opened')
    Gui.Selection.clearSelection()


def begin_sketch(placement=None, map_mode='Deactivated', support=None):
    """Use the existing Sketcher dialog choices; its native editor owns completion."""
    doc = Gui.activeDocument().Document
    definition, path = _context(doc)
    geometry.require_modeling_inputs(definition)
    transaction_id = App.setActiveTransaction('Create a new sketch')
    try:
        sketch = definition.newObject('Sketcher::SketchObject', 'Sketch')
        if placement is not None:
            sketch.Placement = placement
        if support is not None:
            sketch.AttachmentSupport = support
        sketch.MapMode = map_mode
        definition.Document.recompute()
        _enter_editor(doc, definition, path, sketch)
        return sketch
    except Exception:
        App.closeActiveTransaction(True, transaction_id)
        editing._restore(doc, definition, path)
        raise


def _routing_context(doc, definition, path):
    return repr((str(doc.Uid), str(definition.Document.Uid), definition.ID,
                 tuple(obj.ID for obj in path)))


def validate_extrusion_context(expected):
    doc = Gui.activeDocument().Document
    definition, path = _context(doc)
    if _routing_context(doc, definition, path) != expected:
        raise ValueError('The edited component changed; start the operation again')


def extrusion_request(which='Pad'):
    """Resolve profile/target before any mutation; retain it through profile picking."""
    if which not in ('Pad', 'Pocket'):
        raise ValueError('Unknown extrusion command')
    doc = Gui.activeDocument().Document
    definition, path = _context(doc)
    geometry.require_modeling_inputs(definition)
    selected = Gui.Selection.getSelection('*')
    standalone = [obj for obj in definition.Group if obj.isDerivedFrom('Sketcher::SketchObject')]
    if len(selected) == 1 and not standalone:
        if document.owned_path(definition, selected[0]) is None:
            raise ValueError('The profile must belong to the edited component')
        return None  # Retain native face/profile entry on existing body-centered chains.
    profiles, targets = [], []
    for obj in selected:
        if document.owned_path(definition, obj) is None:
            raise ValueError('Profiles and targets must belong to the edited component')
        if obj.isDerivedFrom('Sketcher::SketchObject') and obj in definition.Group:
            profiles.append(obj)
        elif obj.TypeId == 'PartDesign::Body' or obj.isDerivedFrom('PartDesign::Feature'):
            target = obj.Tip if obj.TypeId == 'PartDesign::Body' else obj
            _target_body(definition, target)
            if target not in targets:
                targets.append(target)
        elif len(selected) == 1:
            return None  # Existing body-owned profile chains keep native routing.
        else:
            raise ValueError('Select one component sketch and one current result')
    if len(profiles) > 1 or len(targets) > 1:
        raise ValueError('Select one component sketch and one current result')
    sketches = profiles or standalone
    if not sketches and not targets and any(obj.TypeId == 'PartDesign::Body' for obj in definition.Group):
        return None
    target = targets[0] if targets else None
    if sketches and which == 'Pocket' and target is None:
        eligible = []
        for body in definition.Group:
            if body.TypeId != 'PartDesign::Body' or body.Tip is None:
                continue
            try:
                _target_body(definition, body.Tip)
            except ValueError:
                continue
            eligible.append(body.Tip)
        if len(eligible) != 1:
            raise ValueError('Select the sketch and its target result before subtracting')
        target = eligible[0]
    return {'profiles': sketches, 'target': target,
            'context': _routing_context(doc, definition, path)}


def extrusion_candidates():
    request = extrusion_request()
    return None if request is None else request['profiles']


def begin_extrusion(sketch, which='Pad', target=None):
    """Start the native Pad/Pocket task with an already resolved result target."""
    if which not in ('Pad', 'Pocket'):
        raise ValueError('Unknown extrusion command')
    operation = 'subtract' if which == 'Pocket' else ('add' if target is not None else 'new')
    doc = Gui.activeDocument().Document
    definition, path = _context(doc)
    _require_profile(definition, sketch)
    _require_operation(definition, operation, target)
    subelements = [sub for entry in Gui.Selection.getSelectionEx('*')
                   if entry.Object == sketch for sub in entry.SubElementNames]
    transaction_id = App.setActiveTransaction('Extrude component sketch')
    try:
        feature = _create_extrusion(definition, sketch, 5 if which == 'Pocket' else 10,
                                    subelements, operation=operation, target=target)
        sketch.Visibility = False
        _enter_editor(doc, definition, path, feature)
        return feature
    except Exception:
        App.closeActiveTransaction(True, transaction_id)
        editing._restore(doc, definition, path)
        raise
