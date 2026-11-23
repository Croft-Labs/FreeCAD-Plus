# SPDX-License-Identifier: LGPL-2.1-or-later
"""Shell collector: no model mutation until acceptance, no active Body authority."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from pivy import coin
from . import editing, extrude_task, hierarchy, modeling, planes, shell, task_visibility
from .plane_task import label, number
from .selection_list import SelectionList
from .task_status import TaskStatus


class ShellTask(extrude_task.ExtrudeTask):
    title = 'Shell'

    def __init__(self, feature=None):
        QtCore.QObject.__init__(self)
        self.doc = Gui.activeDocument().Document
        self.owner, self.path = modeling._context(self.doc)
        self.source_doc = self.owner.Document
        self.context = modeling._routing_context(self.doc, self.owner, self.path)
        self.feature = feature
        self.view = Gui.activeDocument().activeView()
        self.scene = self.view.getSceneGraph()
        self.overlay = self.target_overlay = self.tool_preview = self.profile_highlight = None
        self.hidden = self.showing_result = self.closed = self.ready = self.valid = False
        self.hidden_objects = []
        self.refs = []
        self.links = {}
        self.pick = 'profile'
        self.revisions = 0
        self.result_shape = None
        self.main = QtWidgets.QWidget()
        self.main.setWindowTitle('Shell')
        self.main.setWindowIcon(Gui.getIcon('PartDesign_Thickness'))
        layout = QtWidgets.QVBoxLayout(self.main)
        layout.addWidget(label('Component: ' + self.owner.Label))
        layout.addWidget(label('Faces to remove'))
        self.hint = label('')
        layout.addWidget(self.hint)
        self.faces = SelectionList()
        self.faces.setObjectName('listWidgetReferences')
        self.faces.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.faces.setToolTip('Click this list to add faces in the view. Delete removes highlighted rows.')
        layout.addWidget(self.faces)
        self.status = TaskStatus()
        layout.addWidget(self.status)
        actions = QtWidgets.QHBoxLayout()
        self.remove_button = QtWidgets.QPushButton('Remove')
        self.clear_button = QtWidgets.QPushButton('Clear faces')
        actions.addWidget(self.remove_button); actions.addWidget(self.clear_button)
        layout.addLayout(actions)
        self.thickness = number(layout, 'Thickness', feature.Value.Value if feature else 1)
        self.thickness.setObjectName('Value')
        self.thickness.setDecimals(6)
        if feature:self.thickness.setValue(feature.Value.Value)
        self.thickness.setMinimum(.001)
        self.value = self.thickness.value()
        self.mode_box = QtWidgets.QComboBox(); self.mode_box.addItems(['Skin', 'Pipe', 'Recto verso'])
        self.join_box = QtWidgets.QComboBox(); self.join_box.addItems(['Arc', 'Intersection'])
        for text, widget in [('Mode', self.mode_box), ('Join type', self.join_box)]:
            row = QtWidgets.QHBoxLayout(); row.addWidget(label(text)); row.addWidget(widget, 1); layout.addLayout(row)
        self.intersection = QtWidgets.QCheckBox('Intersection')
        self.reverse = QtWidgets.QCheckBox('Make thickness inwards')
        self.reverse.setChecked(True)
        layout.addWidget(self.intersection); layout.addWidget(self.reverse)
        self.preview = QtWidgets.QWidget(); self.preview.setWindowTitle('Preview')
        options = QtWidgets.QVBoxLayout(self.preview)
        self.final = QtWidgets.QCheckBox('Show final result')
        self.visible = QtWidgets.QCheckBox('Show preview overlay'); self.visible.setChecked(True)
        options.addWidget(self.final); options.addWidget(self.visible)
        self.form = [self.main, self.preview]
        entry_error = None
        if feature:
            self.refs = [(feature.Base[0], sub) for sub in feature.Base[1]]
            self.mode_box.setCurrentIndex(feature.getEnumerationsOfProperty('Mode').index(feature.Mode))
            self.join_box.setCurrentIndex(feature.getEnumerationsOfProperty('Join').index(feature.Join))
            self.intersection.setChecked(feature.Intersection)
            self.reverse.setChecked(feature.Reversed)
        else:
            selected = [(item.Object, sub) for item in Gui.Selection.getSelectionEx('', 0)
                        for sub in (item.SubElementNames or [''])]
            for ref in selected:
                try:
                    self.refs = shell.validate(self.owner, self.refs + [ref])
                except Exception as exc:
                    entry_error = str(exc)
        self.sync_list()
        Gui.Selection.clearSelection()
        self.presentation = task_visibility.ExtrudeDisplay(self)
        Gui.Selection.addObserver(self, 0)
        App.addDocumentObserver(self)
        editing.add_context_observer(self.context_changed)
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.remove_button.clicked.connect(self.remove)
        self.clear_button.clicked.connect(self.clear_faces)
        self.thickness.committed.connect(self.commit_value)
        for widget in (self.mode_box, self.join_box):widget.currentIndexChanged.connect(self.render)
        for widget in (self.intersection, self.reverse, self.final, self.visible):widget.toggled.connect(self.render)
        self.ready = True
        self.activate_list()
        self.entry_error = entry_error

    def mode(self):return 'Add'  # Shared presentation of the implicit source solid.
    def output(self):return 'Solid'
    def usable_geometry(self, obj, sheet=False):return hasattr(obj, 'Shape') and bool(obj.Shape.Solids)
    def isAllowedAlterSelection(self):return True
    def isAllowedAlterDocument(self):return False
    def isAllowedAlterView(self):return True

    def settings(self):
        return dict(Value=self.value, Mode=self.mode_box.currentIndex(), Join=self.join_box.currentIndex(),
                    Intersection=self.intersection.isChecked(), Reversed=self.reverse.isChecked())

    def commit_value(self):
        self.value = self.thickness.value()
        self.render()

    def eventFilter(self, watched, event):
        if watched in (self.faces, self.faces.viewport()):
            if event.type() in (QtCore.QEvent.FocusIn, QtCore.QEvent.MouseButtonPress):self.activate_list()
            if event.type() == QtCore.QEvent.ShortcutOverride and event.key() == QtCore.Qt.Key_Delete:
                event.accept(); return True
            if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Delete:
                self.remove(); event.accept(); return True
        elif event.type() == QtCore.QEvent.FocusIn and isinstance(watched, QtWidgets.QWidget):
            if watched not in (self.remove_button, self.clear_button) and (
                    self.main.isAncestorOf(watched) or self.preview.isAncestorOf(watched)):
                self.pick = None; self.update_hint()
        return False

    def activate_list(self):
        self.pick = 'profile'; self.update_hint()

    def update_hint(self):
        self.faces.setStyleSheet('QListWidget { border: 2px solid #347bb7; }' if self.pick else '')
        self.hint.setText('Click faces in the view to add them.' if self.pick else 'Click the face list to add more faces.')
        if self.ready and self.showing_result:
            hidden = [self.feature] if self.feature else []
            if not self.pick and self.refs:hidden.append(self.refs[0][0])
            self.hide_results(hidden)

    def sync_list(self):
        self.faces.clear()
        for obj, sub in self.refs:self.faces.addItem(obj.Label + ' - ' + sub)
        self.links = {'target': (self.refs[0][0], '')} if self.refs else {}

    def addSelection(self, doc, obj, sub, point=None):
        if self.closed or self.pick != 'profile':return
        try:
            self.check()
            candidate = planes.canonical(self.owner, [(App.getDocument(doc).getObject(obj), sub)])
            refs = shell.validate(self.owner, self.refs + candidate, self.feature)
            if refs != self.refs:
                self.refs = refs; self.sync_list(); self.faces.setCurrentRow(len(refs)-1)
                self.faces.scrollToItem(self.faces.currentItem())
                self.presentation.update_style(); self.render()
        except Exception as exc:
            self.status.setError(str(exc))
        finally:
            Gui.Selection.removeSelection(doc, obj, sub)

    def remove(self):
        rows = {self.faces.row(item) for item in self.faces.selectedItems()}
        self.refs = [ref for i, ref in enumerate(self.refs) if i not in rows]
        self.sync_list(); self.presentation.update_style(); self.render()

    def clear_faces(self):
        self.refs = []; self.sync_list(); self.activate_list()
        self.presentation.update_style(); self.render()

    def render(self, *args):
        if not self.ready or self.closed:return
        self.clear_overlay(); self.clear_target(); self.valid = False; self.result_shape = None
        try:
            self.check()
            result = shell.evaluate(self.owner, self.refs, self.settings(), self.feature)
            self.result_shape = result; self.valid = True; self.revisions += 1
            self.world = hierarchy.world_placement(self.doc, self.path) if self.path else App.Placement()
            self.overlay = coin.SoSeparator()
            pick = coin.SoPickStyle(); pick.style = coin.SoPickStyle.UNPICKABLE; self.overlay.addChild(pick)
            if self.visible.isChecked():
                self.showing_result = self.final.isChecked()
                self.add_shape(result, (.65,.68,.70) if self.showing_result else (.2,.45,.95),
                               0 if self.showing_result else .4)
                hidden = [self.feature] if self.feature else []
                if self.showing_result and not self.pick:hidden.append(self.refs[0][0])
                self.hide_results(hidden)
            self.scene.addChild(self.overlay)
            self.status.setText('Shell preview · one solid.')
        except Exception as exc:
            if self.refs:self.status.setError(str(exc))
            else:self.status.setText('Select faces to remove from one solid.')
        self.set_ok(self.valid); self.refresh_target()

    def refresh_visibility(self):
        if self.hidden:self.hide_results(self.hidden_objects)
        self.refresh_target()

    def accept(self):
        try:
            self.check(); self.thickness.interpretText(); self.value = self.thickness.value()
            shell.evaluate(self.owner, self.refs, self.settings(), self.feature)
            self.clear_overlay(); self.clear_target(); self.presentation.restore()
            self.result = shell.save(self.doc, self.refs, self.settings(), self.feature)
            self.reject(); return True
        except Exception as exc:
            self.presentation.apply(); self.render(); self.status.setError(str(exc)); return False

    def reject(self, document_closing=False):
        if self.closed:return True
        self.closed = True
        if extrude_task._active is self:extrude_task._active = None
        QtWidgets.QApplication.instance().removeEventFilter(self)
        Gui.Selection.removeObserver(self); App.removeDocumentObserver(self)
        editing.remove_context_observer(self.context_changed)
        self.presentation.restore()
        try:self.clear_overlay(); self.clear_target()
        except (RuntimeError, ReferenceError, ValueError):pass
        Gui.Control.closeDialog()
        from . import panel
        panel.end_feature_task(self)
        return True


def show(feature=None):
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first.')
    task = ShellTask(feature)
    extrude_task._active = task
    Gui.Control.showDialog(task)
    task.render()
    if task.entry_error:task.status.setError(task.entry_error)
    from . import panel
    panel.begin_feature_task(task)
    return task
