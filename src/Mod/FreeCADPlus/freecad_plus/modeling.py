# SPDX-License-Identifier: LGPL-2.1-or-later
"""Feature-centered modeling services; no command or UI registration.

Sketches start in the edited component. A solid-producing operation supplies its
native Body internally, in the same transaction as the feature. The first adapter
creates independent extruded solids; joining/cutting existing results is separate.
"""
import math

import FreeCAD as App

from . import document, editing, geometry


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
    if (sketch not in definition.Group or sketch.TypeId != 'Sketcher::SketchObject'
            or sketch.getParentGeoFeatureGroup() != definition):
        raise ValueError('Use an unconsumed sketch owned by the edited component')
    geometry.require_modeling_inputs(definition, [(sketch, '')])
    length = float(length)
    if not math.isfinite(length) or length <= 0:
        raise ValueError('Extrusion length must be finite and greater than zero')

    with document.transaction(definition.Document, 'Extrude component sketch'):
        body = definition.newObject('PartDesign::Body', 'Body')
        # Native profile links require the same Body scope. Move the original
        # sketch, preserving its identity, placement, constraints and references.
        # Native transaction rollback restores component ownership on failure.
        definition.removeObject(sketch)
        body.addObject(sketch)
        feature = body.newObject('PartDesign::Pad', 'Pad')
        feature.Profile = sketch
        feature.Length = length
        definition.Document.recompute()
        if (feature.Shape.isNull() or not feature.Shape.isValid()
                or len(feature.Shape.Solids) != 1 or 'Invalid' in feature.State):
            raise ValueError('The extrusion must produce one valid solid')
        sketch.Visibility = False
    editing._restore(doc, definition, path)
    return feature
