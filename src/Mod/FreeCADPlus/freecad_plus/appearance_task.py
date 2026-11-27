# SPDX-License-Identifier: LGPL-2.1-or-later
"""Appearance task: deferred edits, source-owned Undo, checked face picks."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui
from . import appearance, panel
from .appearance_ui import AppearanceForm
from .selection_list import removing

_active = None


def selection_snapshot():
    return tuple((panel.identity(entry.Object), sub) for entry in Gui.Selection.getSelectionEx('*', 0)
                 for sub in entry.SubElementNames or ('',))


class AppearanceTask(QtCore.QObject):
    def __init__(self, owner, initial=None):
        super().__init__()
        self.closed = False;self.busy = False;self.collecting = True
        self.selection_epoch = 0;self.hover = None
        self.owner_ref = panel.identity(owner)
        self.host = App.ActiveDocument;self.view = Gui.activeDocument().activeView()
        self.edit_context = self.view.getActiveObject('PlusEdit', False)
        self.objects = {panel.identity(obj): obj for obj in appearance.results(owner)}
        self.shapes = {key: obj.Shape for key, obj in self.objects.items() if hasattr(obj, 'Shape')}
        catalog = {key: {'label': obj.Label, 'faces': ['Face'+str(i+1) for i in range(appearance.face_count(obj))]}
                   for key, obj in self.objects.items()}
        chosen = []
        for ref, sub in selection_snapshot() if initial is None else initial:
            try:
                obj, face = appearance.resolve_pick(owner, panel.lookup(ref), sub)
                chosen.append((panel.identity(obj), 'Face'+str(face) if face else None))
            except (ValueError, RuntimeError, ReferenceError):
                continue
        face_mode = any(face for key, face in chosen)
        targets = list(dict.fromkeys((key, face if face_mode else None) for key, face in chosen if face or not face_mode))
        if not targets: targets = [(key, None) for key in self.objects]
        self.form = AppearanceForm(owner.Label, catalog, targets)
        if face_mode:
            self.form.mode = 'face'
            self.form.face.setChecked(True);self.form.refresh_targets()
        self.alpha_changed = False
        self.form.targetsChanged.connect(self.load_values)
        self.form.targetsChanged.connect(self.collector_changed)
        self.form.value.valueChanged.connect(self.alpha_edited)
        self.form.apply.clicked.connect(self.apply)
        self.form.done.clicked.connect(self.accept)
        self.form.cancel.clicked.connect(self.reject)
        self.form.items.viewport().installEventFilter(self)
        self.form.items.setMouseTracking(True)
        self.pending = []
        self.pick_timer = QtCore.QTimer(self);self.pick_timer.setSingleShot(True);self.pick_timer.timeout.connect(self.deliver)
        from .appearance_highlight import Highlights, preferences
        self.highlights = Highlights(self);self.highlight_preferences = preferences()
        self.highlight_timer = QtCore.QTimer(self);self.highlight_timer.setSingleShot(True)
        self.highlight_timer.timeout.connect(self.refresh_highlights)
        self.preference_timer = QtCore.QTimer(self);self.preference_timer.setInterval(250)
        self.preference_timer.timeout.connect(self.check_preferences);self.preference_timer.start()
        Gui.Selection.addObserver(self, 0);App.addDocumentObserver(self)
        self.load_values()

    def collector_changed(self):
        self.selection_epoch += 1
        self.pending.clear();self.pick_timer.stop();self.hover = None
        from .selection_scope import changed
        changed();self.refresh_highlights()

    def check_preferences(self):
        from .appearance_highlight import preferences
        current = preferences()
        if current != self.highlight_preferences:
            self.highlight_preferences = current;self.refresh_highlights()

    def refresh_highlights(self):
        if self.closed:return
        try:self.highlights.update(self.check(), self.targets() if self.form.mode=='face' else (), self.hover)
        except (ValueError, RuntimeError, ReferenceError, IndexError):self.highlights.clear()

    def setPreselection(self, doc, name, sub, *args):
        if self.closed or self.form.mode != 'face':return
        try:
            obj, face = appearance.resolve_pick(self.check(), App.getDocument(doc).getObject(name), sub)
            self.hover = (obj, face) if face else None
        except (ValueError, RuntimeError, ReferenceError, AttributeError):self.hover = None
        self.highlight_timer.start(0)

    def removePreselection(self, *args):
        if not self.closed:self.hover = None;self.highlight_timer.start(0)

    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:self.collecting = True
        if event.type() == QtCore.QEvent.MouseMove and self.form.mode == 'face':
            item = self.form.items.itemAt(event.position().toPoint())
            self.hover = self.targets()[self.form.items.row(item)] if item else None
            self.highlight_timer.start(0)
        elif event.type() == QtCore.QEvent.Leave:self.removePreselection()
        return False

    def check(self):
        if self.closed: raise ValueError('This appearance task is closed')
        owner = panel.lookup(self.owner_ref)
        if (App.ActiveDocument != self.host or Gui.activeDocument().activeView() != self.view
                or self.view.getActiveObject('PlusEdit', False) != self.edit_context):
            raise ValueError('The active file or component changed. Cancel and reopen Appearance.')
        eligible = appearance.results(owner)
        for key, face in self.form.targets:
            obj = panel.lookup(key)
            if obj not in eligible:raise ValueError('A selected body changed. Cancel and reopen Appearance.')
            if key in self.shapes and not obj.Shape.isSame(self.shapes[key]):
                raise ValueError('The selected geometry changed. Cancel and select its faces again.')
        return owner

    def targets(self):
        return [(panel.lookup(key), int(face[4:]) if face else None) for key, face in self.form.targets]

    def error(self, error):
        self.form.status.setError(str(error));self.form.status.show()

    def alpha_edited(self, value):
        if not self.busy:self.alpha_changed = value >= 0

    def load_values(self):
        try:
            self.check();values = []
            for obj, face in self.targets():
                mats = appearance.materials(obj);values.extend([mats[face-1]] if face else mats)
            colors = {tuple(round(c, 6) for c in mat.DiffuseColor[:3]) for mat in values}
            alphas = {round(mat.Transparency*100) for mat in values}
            self.busy = True
            self.form.color_value = QtGui.QColor.fromRgbF(*next(iter(colors))) if len(colors)==1 else None
            self.form.color_changed = False;self.form.refresh_color()
            self.form.value.setValue(next(iter(alphas)) if len(alphas)==1 else -1)
            self.alpha_changed = False
            self.form.status.hide()
        except (ValueError, RuntimeError, ReferenceError, IndexError) as error:self.error(error)
        finally:self.busy = False
        self.refresh_highlights()

    def addSelection(self, doc, name, sub, *args):
        if self.closed or self.busy or not self.collecting:return
        try:
            self.pending.append((panel.identity(App.getDocument(doc).getObject(name)), sub, removing()))
            self.pick_timer.start(0)
        except (ValueError, RuntimeError, ReferenceError, AttributeError):pass

    def deliver(self):
        pending,self.pending = self.pending,[]
        for ref, sub, remove in pending:
            try:self.pick(panel.lookup(ref), sub, remove)
            except (ValueError, RuntimeError, ReferenceError, TypeError) as error:self.error(error)

    def pick(self, obj, sub='', remove=False):
        owner = self.check();target,face = appearance.resolve_pick(owner,obj,sub)
        if self.form.mode=='face' and face is None:
            raise ValueError('Pick a CAD face, or switch to Body for whole objects and meshes.')
        value = (panel.identity(target),'Face'+str(face) if self.form.mode=='face' else None)
        if remove:self.form.targets = [t for t in self.form.targets if t != value]
        elif value not in self.form.targets:self.form.targets.append(value)
        self.form.refresh_targets();self.load_values()
        self.busy = True
        try:Gui.Selection.removeSelection(obj,sub)
        finally:self.busy = False

    def apply(self):
        try:
            owner = self.check()
            color = self.form.color_value.getRgbF()[:3] if self.form.color_changed else None
            alpha = self.form.value.value() if self.alpha_changed else None
            appearance.apply(owner, self.targets(), color, alpha)
            self.reset_inputs();Gui.updateGui()
            return True
        except (ValueError, RuntimeError, ReferenceError, TypeError, IndexError) as error:
            self.error(error);return False

    def accept(self):
        if self.form.targets and not self.apply():return False
        self.finish();return True

    def reset_inputs(self):
        self.pick_timer.stop();self.pending.clear()
        self.busy = True
        try:
            Gui.Selection.clearSelection()
            self.form.targets = []
            self.form.body.setChecked(True)
            self.form.refresh_targets()
            self.form.color_value = QtGui.QColor('#b9c4cf')
            self.form.color_changed = False;self.form.refresh_color()
            self.form.value.setValue(0);self.alpha_changed = False
            self.form.status.hide();self.collecting = True
        finally:self.busy = False
        self.collector_changed()

    def reject(self):self.finish();return True

    def finish(self):
        global _active
        if self.closed:return
        self.closed = True;self.pick_timer.stop();self.pending.clear()
        self.highlight_timer.stop();self.preference_timer.stop();self.highlights.clear()
        Gui.Selection.removeObserver(self);App.removeDocumentObserver(self)
        if _active is self:_active = None;Gui.Control.closeDialog()
        from .selection_scope import changed
        changed()
        self.deleteLater()

    def slotDeletedDocument(self, doc):
        if doc == self.host or doc.Name == self.owner_ref[0]:self.finish()

    def schedule_highlights(self, *args):
        if not self.closed:self.highlight_timer.start(0)

    slotChangedObject = schedule_highlights
    slotRecomputedDocument = schedule_highlights
    slotUndoDocument = schedule_highlights
    slotRedoDocument = schedule_highlights

    def getStandardButtons(self):return 0
    def isAllowedAlterDocument(self):return False
    def isAllowedAlterSelection(self):return True
    def isAllowedAlterView(self):return True


def open_task(owner, initial=None):
    global _active
    if Gui.Control.activeDialog() or Gui.activeDocument().getInEdit():
        raise ValueError('Finish the current task before opening Appearance')
    if not appearance.results(owner):raise ValueError('This component has no bodies or meshes to color')
    task = AppearanceTask(owner,initial);_active = task
    try:Gui.Control.showDialog(task)
    except Exception:task.finish();raise
    return task
