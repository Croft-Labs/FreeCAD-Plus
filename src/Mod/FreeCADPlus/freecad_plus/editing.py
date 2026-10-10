# SPDX-License-Identifier: LGPL-2.1-or-later
"""Transient, per-view Edit routing for the single-component pilot.

No selection observer, command replacement, or new toolbar placement. The full
Models/Part Tree/History panel will consume these services in its own stage.
"""
import FreeCAD as App
import FreeCADGui as Gui
from .document import transaction, validate

_KEY = "PlusEdit"


def _view(doc):
    if App.ActiveDocument != doc:
        raise ValueError("Activate this file's tab before editing")
    return Gui.activeDocument().activeView()


def edit(instance):
    doc = instance.Document
    root = validate(doc)
    if instance not in root.Group:
        raise ValueError("Edit requires a placed component in this file")
    view = _view(doc)
    if Gui.activeDocument().getInEdit():
        raise ValueError("Finish the native feature editor first")
    definition = instance.LinkedObject
    view.setActiveObject(_KEY, root, instance.Name + ".")
    view.setActiveObject("part", definition)
    bodies = [obj for obj in definition.Group if obj.TypeId == "PartDesign::Body"]
    view.setActiveObject("pdbody", bodies[-1] if bodies else None)
    return definition


def edit_file(doc):
    view = _view(doc)
    if Gui.activeDocument().getInEdit():
        raise ValueError("Finish the native feature editor first")
    view.setActiveObject(_KEY, validate(doc))
    view.setActiveObject("part", None)
    view.setActiveObject("pdbody", None)


def context(doc):
    root = validate(doc)
    if Gui.getDocument(doc.Name).getInEdit():
        raise ValueError("Finish the native feature editor first")
    resolved, parent, subname = _view(doc).getActiveObject(_KEY, False)
    occurrences = [o for o in root.Group if subname == o.Name + "."]
    if parent != root or len(occurrences) != 1 or resolved != occurrences[0].LinkedObject:
        raise ValueError("Explicitly Edit a component before creating modeling geometry")
    return resolved, occurrences[0]


def new_sketch(doc):
    """Create/route the backend Body automatically; retain the native Sketch editor."""
    definition, occurrence = context(doc)
    with transaction(doc, "Create component sketch"):
        bodies = [obj for obj in definition.Group if obj.TypeId == "PartDesign::Body"]
        body = bodies[-1] if bodies else definition.newObject("PartDesign::Body", "Body")
        sketch = body.newObject("Sketcher::SketchObject", "Sketch")
    edit(occurrence)
    return sketch


def pad(doc, sketch, length):
    """Narrow native-feature adapter, without replacing PartDesign_Pad or its editor."""
    definition, occurrence = context(doc)
    bodies = [body for body in definition.Group if body.TypeId == "PartDesign::Body" and sketch in body.Group]
    if sketch.TypeId != "Sketcher::SketchObject" or len(bodies) != 1:
        raise ValueError("The sketch must belong to the explicitly edited component")
    with transaction(doc, "Pad component sketch"):
        feature = bodies[0].newObject("PartDesign::Pad", "Pad")
        feature.Profile = sketch
        feature.Length = length
        doc.recompute()
        if feature.Shape.isNull() or not feature.Shape.isValid() or "Invalid" in feature.State:
            raise ValueError("The native Pad could not produce valid geometry")
        sketch.Visibility = False
    edit(occurrence)
    return feature
