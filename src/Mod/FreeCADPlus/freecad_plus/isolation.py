# SPDX-License-Identifier: LGPL-2.1-or-later
"""Per-view unused-definition display; no document objects or visibility writes."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore
try:
    from PySide import QtWidgets
except ImportError:
    from PySide import QtGui as QtWidgets
from pivy import coin
from . import document, external

_sessions = []


def _identity(obj):
    return obj.Document.Name, str(obj.Document.Uid), obj.Name, obj.ID


def _resolve(ref):
    owner = App.listDocuments().get(ref[0])
    obj = owner.getObject(ref[2]) if owner and str(owner.Uid) == ref[1] else None
    if obj is None or obj.ID != ref[3]:
        raise ValueError('The unused definition is no longer available')
    return obj


def occurrences(doc, definition):
    result = []
    def visit(owner, path=()):
        for link in owner.Group:
            if link.TypeId != 'App::Link':
                continue
            route = (*path, link)
            if link.LinkedObject == definition:
                result.append(route)
            visit(link.LinkedObject, route)
    visit(document.validate(doc))
    return result


def current(view):
    return next((session for session in _sessions if session.view == view and not session.closed), None)


def begin(doc, view, definition):
    if definition not in external.available_definitions(document.validate(doc)):
        raise ValueError('The definition is not in this file catalog')
    if occurrences(doc, definition):
        raise ValueError('Edit a placed occurrence of this component')
    existing = current(view)
    if existing and existing.ref == _identity(definition):
        existing.refresh()
        return existing
    # Prepare the new preview before disturbing an existing context.
    preview = _preview(definition)
    end(view)
    session = Isolation(doc, view, definition, preview)
    _sessions.append(session)
    return session


def end(view):
    session = current(view)
    if session:
        session.close()


def close_all():
    for session in tuple(_sessions):
        session.close()


def _preview(definition):
    vp = definition.ViewObject
    original = vp.RootNode
    index = original.findChild(vp.SwitchNode)
    if index < 0 or vp.SwitchNode.getNumChildren() != 1:
        raise ValueError('This component display cannot be isolated safely')
    # Native Coin copying preserves native selection metadata, transforms,
    # appearances and nested geometry. Only this detached display switch is forced.
    result = original.copy(False)
    result.getChild(index).whichChild = 0
    return result


class Isolation:
    def __init__(self, doc, view, definition, preview):
        self.doc = doc
        self.view = view
        self.ref = _identity(definition)
        self.scene = view.getSceneGraph()
        self.preview = preview
        self.closed = False
        self.hidden = []
        self.timer = QtCore.QTimer(Gui.getMainWindow())
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.refresh)
        self.window = Gui.getMainWindow().findChild(QtWidgets.QMdiArea).activeSubWindow()
        nodes = [self.scene.getChild(i) for i in range(self.scene.getNumChildren())]
        if sum(str(node.getName()) == 'ObjectGroup' for node in nodes) != 1:
            self.timer.deleteLater()
            raise ValueError('The active view has no unique native object display group')
        for node in nodes:
            if str(node.getName()) not in ('ObjectGroup', 'GroupOnTop', 'RootDimensions'):
                continue
            switch = coin.SoSwitch()
            switch.whichChild = coin.SO_SWITCH_NONE
            switch.addChild(node)
            self.scene.replaceChild(node, switch)
            self.hidden.append((node, switch))
        self.scene.addChild(preview)
        self.window.destroyed.connect(self.close)
        App.addDocumentObserver(self)
        Gui.addDocumentObserver(self)

    def definition(self):
        definition = _resolve(self.ref)
        if definition not in external.available_definitions(document.validate(self.doc)):
            raise ValueError('The unused definition is no longer imported')
        return definition

    def schedule(self, *args):
        if not self.closed and not self.timer.isActive():
            self.timer.start(0)

    slotChangedObject = schedule
    slotCreatedObject = schedule
    slotDeletedObject = schedule
    slotRecomputedDocument = schedule
    slotCommitTransaction = schedule
    slotAbortTransaction = schedule
    slotUndoDocument = schedule
    slotRedoDocument = schedule
    slotInEdit = schedule
    slotResetEdit = schedule

    def slotDeletedDocument(self, doc):
        owner = getattr(doc, 'Document', doc)
        if owner == self.doc or owner.Name == self.ref[0]:
            self.close()

    def refresh(self):
        if self.closed:
            return
        if any(doc.HasPendingTransaction for doc in App.listDocuments().values()):
            return
        try:
            definition = self.definition()
            if occurrences(self.doc, definition):
                self.close()
                return
            preview = _preview(definition)
            self.scene.replaceChild(self.preview, preview)
            self.preview = preview
        except (ValueError, RuntimeError, ReferenceError):
            self.close()

    def close(self, *args):
        if self.closed:
            return
        self.closed = True
        self.timer.stop()
        self.timer.deleteLater()
        App.removeDocumentObserver(self)
        Gui.removeDocumentObserver(self)
        try:
            self.window.destroyed.disconnect(self.close)
        except (RuntimeError, TypeError):
            pass
        if self.scene.findChild(self.preview) >= 0:
            self.scene.removeChild(self.preview)
        for node, switch in self.hidden:
            if self.scene.findChild(switch) >= 0:
                self.scene.replaceChild(switch, node)
        if self in _sessions:
            _sessions.remove(self)
        # Do not leave a hidden definition active after its preview is gone.
        try:
            root = document.validate(self.doc)
            self.view.setActiveObject('PlusEdit', root)
            self.view.setActiveObject('part', None)
            self.view.setActiveObject('pdbody', None)
        except (ValueError, RuntimeError, ReferenceError):
            pass
        from .editing import _notify_context
        _notify_context()
