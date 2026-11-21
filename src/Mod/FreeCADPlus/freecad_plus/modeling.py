# SPDX-License-Identifier: LGPL-2.1-or-later
"""Feature-centered services and transaction adapters for existing native commands.

Sketches start in the edited component. A solid-producing operation supplies its
native Body internally, in the same transaction as the feature. The first adapter
creates independent extruded solids; joining/cutting existing results is separate.
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
    definition, path = _context(doc)
    _require_profile(definition, sketch)
    length = float(length)
    if not math.isfinite(length) or length <= 0:
        raise ValueError('Extrusion length must be finite and greater than zero')

    with document.transaction(definition.Document, 'Extrude component sketch'):
        feature = _create_extrusion(definition, sketch, length)
        if (feature.Shape.isNull() or not feature.Shape.isValid()
                or len(feature.Shape.Solids) != 1 or 'Invalid' in feature.State):
            raise ValueError('The extrusion must produce one valid solid')
        sketch.Visibility = False
    editing._restore(doc, definition, path)
    return feature


def _require_profile(definition, sketch):
    if (sketch not in definition.Group or sketch.TypeId != 'Sketcher::SketchObject'
            or sketch.getParentGeoFeatureGroup() != definition):
        raise ValueError('Use an unconsumed sketch owned by the edited component')
    geometry.require_modeling_inputs(definition, [(sketch, '')])


def _create_extrusion(definition, sketch, length, subelements=()):
    """Native mutations shared by atomic API calls and dialog-owned transactions."""
    body = definition.newObject('PartDesign::Body', 'Body')
    body.AllowCompound = False
    # The profile must share the native Body scope; retain its original identity.
    definition.removeObject(sketch)
    body.addObject(sketch)
    feature = body.newObject('PartDesign::Pad', 'Pad')
    feature.Profile = (sketch, list(subelements))
    feature.Length = length
    feature.ReferenceAxis = (sketch, ['N_Axis'])
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


def extrusion_candidates():
    """Return component sketches, or None for an existing native feature chain."""
    doc = Gui.activeDocument().Document
    definition, _ = _context(doc)
    geometry.require_modeling_inputs(definition)
    selected = Gui.Selection.getSelection('*')
    if selected:
        if len(selected) != 1:
            raise ValueError('Select one sketch or profile')
        obj = selected[0]
        if document.owned_path(definition, obj) is None:
            raise ValueError('The profile must belong to the edited component')
        if obj.TypeId == 'Sketcher::SketchObject' and obj in definition.Group:
            return [obj]
        return None  # Existing body-centered chains retain native routing.
    sketches = [obj for obj in definition.Group if obj.TypeId == 'Sketcher::SketchObject']
    if sketches:
        return sketches
    if any(obj.TypeId == 'PartDesign::Body' for obj in definition.Group):
        return None
    return []


def begin_extrusion(sketch):
    """Start the existing Pad task; OK/Cancel commits/aborts Body and feature together."""
    doc = Gui.activeDocument().Document
    definition, path = _context(doc)
    _require_profile(definition, sketch)
    subelements = [sub for entry in Gui.Selection.getSelectionEx('*')
                   if entry.Object == sketch for sub in entry.SubElementNames]
    transaction_id = App.setActiveTransaction('Extrude component sketch')
    try:
        feature = _create_extrusion(definition, sketch, 10, subelements)
        sketch.Visibility = False
        _enter_editor(doc, definition, path, feature)
        return feature
    except Exception:
        App.closeActiveTransaction(True, transaction_id)
        editing._restore(doc, definition, path)
        raise
