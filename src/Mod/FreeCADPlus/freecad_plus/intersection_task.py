# SPDX-License-Identifier: LGPL-2.1-or-later
"""Intersection collector embedded in the existing sketch edit task."""
import FreeCAD as App, FreeCADGui as Gui
from PySide6 import QtCore,QtWidgets
from . import intersections,derived_geometry,editing,panel
from .selection_list import SelectionList,removing
from .task_status import TaskStatus
from .shape_preview import ShapePreview

_active=None


class IntersectionTask(QtCore.QObject):
    reference_guidance=True
    def __init__(self,sketch,host):
        super().__init__(host);self.sketch=sketch;self.owner=derived_geometry.owner(sketch)
        self.view=Gui.activeDocument().activeView();self.doc=Gui.activeDocument().Document
        self.refs=[];self.closed=False;self.busy=False;self.preview=ShapePreview(self.view)
        self.form=QtWidgets.QGroupBox('Intersection curve',host);layout=QtWidgets.QVBoxLayout(self.form)
        def label(text):
            widget=QtWidgets.QLabel(text);widget.setWordWrap(True);layout.addWidget(widget)
        label('Component: '+self.owner.Label+'\nSketch: '+sketch.Label+'\nPlane: Current sketch plane')
        label('Select geometry from earlier History items in this component.')
        label('Sources');self.sources=SelectionList();self.sources.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection);layout.addWidget(self.sources)
        self.sources.installEventFilter(self)
        label('Click an edge or face in the view, or choose an earlier shape or sketch in History. Mix geometry types in this list. Shift-click or Delete removes.')
        row=QtWidgets.QHBoxLayout();self.remove=QtWidgets.QPushButton('Remove selected');self.clear=QtWidgets.QPushButton('Clear')
        row.addWidget(self.remove);row.addWidget(self.clear);layout.addLayout(row)
        self.visible=QtWidgets.QCheckBox('Preview intersections');self.visible.setChecked(True);layout.addWidget(self.visible)
        label('Results stay linked to their sources and update when the sources or sketch plane change.')
        self.status=TaskStatus('Select a source to begin.');layout.addWidget(self.status)
        label('Solid / face / surface → section curves\nEdge / sketch curve → points at every crossing')
        row=QtWidgets.QHBoxLayout();self.done=QtWidgets.QPushButton('Done');self.apply_button=QtWidgets.QPushButton('Apply');self.cancel=QtWidgets.QPushButton('Cancel')
        for button in (self.done,self.apply_button,self.cancel):row.addWidget(button)
        layout.addLayout(row);host.layout().insertWidget(0,self.form)
        self.remove.clicked.connect(self.remove_rows);self.clear.clicked.connect(self.clear_rows)
        self.visible.toggled.connect(self.refresh);self.done.clicked.connect(self.accept)
        self.apply_button.clicked.connect(self.apply);self.cancel.clicked.connect(self.reject)
        self.timer=QtCore.QTimer(self);self.timer.setInterval(200);self.timer.timeout.connect(self.check_edit);self.timer.start()
        Gui.Selection.addObserver(self,0);App.addDocumentObserver(self);self.fields()

    def check_edit(self):
        try:
            edit=Gui.activeDocument().getInEdit() if Gui.activeDocument() else None
            if edit is None or edit.Object!=self.sketch or Gui.activeDocument().activeView()!=self.view:self.reject()
        except (RuntimeError,ReferenceError):self.reject()

    def fields(self):
        self.sources.clear()
        for obj,sub in self.refs:self.sources.addItem(obj.Label+('.'+sub if sub else ''))
        self.apply_button.setEnabled(bool(self.refs));self.refresh()

    def eventFilter(self,obj,event):
        if self.closed:return False
        if obj is self.sources and event.type()==QtCore.QEvent.KeyPress and event.key()==QtCore.Qt.Key_Delete:
            self.remove_rows();return True
        return False
    def remove_rows(self):
        for i in sorted((self.sources.row(item) for item in self.sources.selectedItems()),reverse=True):self.refs.pop(i)
        self.fields()
    def clear_rows(self):self.refs=[];self.fields()

    def addSelection(self,doc,name,sub,*args):
        if self.busy or self.closed:return
        self.busy=True
        try:
            ref=intersections.canonical(self.owner,self.sketch,(App.getDocument(doc).getObject(name),sub))
            if removing():self.refs=[r for r in self.refs if r!=ref]
            elif ref not in self.refs:self.refs.append(ref)
            Gui.Selection.removeSelection(doc,name,sub);self.fields()
        except Exception as exc:self.status.setError(str(exc))
        finally:self.busy=False

    def refresh(self,*args):
        if self.closed:return
        self.preview.clear()
        try:
            if not self.refs:self.status.setText('Select a source to begin.');return
            shapes=intersections.section(self.owner,self.sketch,self.refs)
            if self.visible.isChecked():
                owner,path=editing.context_path(self.doc,allow_native=True)
                if owner!=self.owner:raise ValueError('The active component changed; reopen this task')
                self.preview.show(shapes,editing.world_placement(self.doc,path))
            self.status.setText(str(len(self.refs))+' linked sources selected.')
        except Exception as exc:self.status.setError(str(exc))
    def apply(self):
        try:
            intersections.apply(self.owner,self.sketch,self.refs)
            self.refs=[];self.visible.setChecked(True);self.fields();return True
        except Exception as exc:self.status.setError(str(exc));return False
    def accept(self):
        if not self.refs or self.apply():self.reject()
    def reject(self,*args,reset_handler=True):
        global _active
        if self.closed:return
        self.closed=True;self.timer.stop();self.preview.close();Gui.Selection.removeObserver(self);App.removeDocumentObserver(self)
        self.form.hide();self.form.deleteLater();_active=None
        if reset_handler and Gui.activeDocument() and Gui.activeDocument().getInEdit():Gui.runCommand('Sketcher_StopOperation')
        panel.end_feature_task(self);self.deleteLater()
    def slotDeletedDocument(self,doc):
        if doc in (self.doc,self.sketch.Document):self.reject()


def show():
    global _active
    if _active:return _active
    gui=Gui.activeDocument();edit=gui.getInEdit() if gui else None
    if edit is None or not edit.Object.isDerivedFrom('Sketcher::SketchObject'):raise ValueError('Edit a sketch first')
    dock=Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks')
    host=next((w for w in dock.findChildren(QtWidgets.QWidget) if w.inherits('Gui::TaskView::TaskPanel')),None)
    if host is None:raise ValueError('The sketch task panel is unavailable')
    initial=[(e.DocumentName,e.ObjectName,s) for e in Gui.Selection.getSelectionEx('*',0) for s in e.SubElementNames or ('',)]
    task=IntersectionTask(edit.Object,host);_active=task;panel.begin_feature_task(task)
    for doc,name,sub in initial:task.addSelection(doc,name,sub)
    return task


def handler_closed():
    task=_active
    if task is not None and not task.closed:
        QtCore.QTimer.singleShot(0,lambda:task.reject(reset_handler=False))
