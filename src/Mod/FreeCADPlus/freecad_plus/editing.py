# SPDX-License-Identifier: LGPL-2.1-or-later
"""Transient, per-view Edit routing for component occurrences, including external definitions.

The opt-in panel consumes these services through transient context notifications.
Selection alone never calls Edit; original workbench commands remain unchanged.
"""
import FreeCAD as App
import FreeCADGui as Gui
from .document import transaction, validate
from . import hierarchy, isolation

_KEY = "PlusEdit"
_context_observers = []


def add_context_observer(callback):
    if callback not in _context_observers:
        _context_observers.append(callback)


def remove_context_observer(callback):
    if callback in _context_observers:
        _context_observers.remove(callback)


def _notify_context():
    for callback in tuple(_context_observers):
        callback()



def _view(doc):
    if App.ActiveDocument != doc:
        raise ValueError("Activate this file's tab before editing")
    return Gui.activeDocument().activeView()


def edit(instance):
    path = tuple(instance) if isinstance(instance, (tuple, list)) else (instance,)
    if not path:
        raise ValueError("Edit requires an occurrence path")
    doc = path[0].Document
    root = validate(doc)
    definition, path = hierarchy.resolve(doc, path)
    view = _view(doc)
    if Gui.activeDocument().getInEdit():
        raise ValueError("Finish the native feature editor first")
    isolation.end(view)
    view.setActiveObject(_KEY, root, hierarchy.subname(path))
    view.setActiveObject("part", root, hierarchy.subname(path))
    bodies = [obj for obj in definition.Group if obj.TypeId == "PartDesign::Body"]
    if bodies:
        view.setActiveObject("pdbody", root, hierarchy.subname(path) + bodies[-1].Name + ".")
    else:
        view.setActiveObject("pdbody", None)
    _notify_context()
    return definition


def edit_file(doc):
    view = _view(doc)
    if Gui.activeDocument().getInEdit():
        raise ValueError("Finish the native feature editor first")
    root = validate(doc)
    isolation.end(view)
    view.setActiveObject(_KEY, root)
    view.setActiveObject("part", None)
    view.setActiveObject("pdbody", None)
    _notify_context()


def edit_unused(doc, definition):
    """Edit a catalog definition in this tab without adding a native occurrence."""
    view = _view(doc)
    if Gui.getDocument(doc.Name).getInEdit():
        raise ValueError("Finish the native feature editor first")
    if definition.Document != doc and not hasattr(view, "setDocumentContext"):
        raise ValueError("External unused editing requires the native document-context build")
    isolation.begin(doc, view, definition)
    if hasattr(view, "setDocumentContext"):
        view.setDocumentContext(validate(doc), definition)
    view.setActiveObject(_KEY, definition, "")
    view.setActiveObject("part", definition, "")
    bodies = [obj for obj in definition.Group if obj.TypeId == "PartDesign::Body"]
    if bodies:
        view.setActiveObject("pdbody", definition, bodies[-1].Name + ".")
    else:
        view.setActiveObject("pdbody", None)
    _notify_context()
    return definition


def unused_context(doc):
    session = isolation.current(_view(doc))
    return session.definition() if session else None


def _restore(doc, definition, path):
    if path:
        edit(path)
    else:
        edit_unused(doc, definition)


def context_path(doc):
    root = validate(doc)
    if Gui.getDocument(doc.Name).getInEdit():
        raise ValueError("Finish the native feature editor first")
    unused = unused_context(doc)
    if unused is not None:
        return unused, ()
    resolved, parent, subname = _view(doc).getActiveObject(_KEY, False)
    if parent != root or not subname:
        raise ValueError("Explicitly Edit a component before creating modeling geometry")
    definition, path = hierarchy.resolve(doc, subname.rstrip(".").split("."))
    if definition != resolved:
        raise ValueError("The component Edit context is stale")
    return definition, path


def context(doc):
    definition, path = context_path(doc)
    return definition, path[-1] if path else None


def new_sketch(doc):
    """Create/route the backend Body automatically; retain the native Sketch editor."""
    definition, occurrence = context_path(doc)
    with transaction(definition.Document, "Create component sketch"):
        bodies = [obj for obj in definition.Group if obj.TypeId == "PartDesign::Body"]
        body = bodies[-1] if bodies else definition.newObject("PartDesign::Body", "Body")
        sketch = body.newObject("Sketcher::SketchObject", "Sketch")
    _restore(doc, definition, occurrence)
    return sketch


def pad(doc, sketch, length):
    """Narrow native-feature adapter, without replacing PartDesign_Pad or its editor."""
    definition, occurrence = context_path(doc)
    bodies = [body for body in definition.Group if body.TypeId == "PartDesign::Body" and sketch in body.Group]
    if sketch.TypeId != "Sketcher::SketchObject" or len(bodies) != 1:
        raise ValueError("The sketch must belong to the explicitly edited component")
    with transaction(definition.Document, "Pad component sketch"):
        feature = bodies[0].newObject("PartDesign::Pad", "Pad")
        feature.Profile = sketch
        feature.Length = length
        definition.Document.recompute()
        if feature.Shape.isNull() or not feature.Shape.isValid() or "Invalid" in feature.State:
            raise ValueError("The native Pad could not produce valid geometry")
        sketch.Visibility = False
    _restore(doc, definition, occurrence)
    return feature


def edit_feature(doc, feature):
    """Open the native feature editor in the explicitly edited component/view."""
    from .document import history
    definition, path = context_path(doc)
    if feature not in history(doc, definition):
        raise ValueError("The feature must belong to the edited component")
    body = feature.getParentGeoFeatureGroup()
    subname = (body.Name + "." if body and body.TypeId == "PartDesign::Body" else "") + feature.Name + "."
    parent = validate(doc) if path else definition
    if path:
        subname = hierarchy.subname(path) + subname
    if App.getActiveTransaction() or any(owner.HasPendingTransaction for owner in App.listDocuments().values()):
        raise ValueError("Finish the current operation first")
    # Match native feature double-click: the dialog owns commit/cancel, and
    # mutations are recorded in the defining document even from another view.
    transaction_id = App.setActiveTransaction("Edit " + feature.Label)
    try:
        if not Gui.getDocument(doc.Name).setEdit(parent, 0, subname):
            raise ValueError("This item has no available native editor")
    except Exception:
        App.closeActiveTransaction(True, transaction_id)
        raise
