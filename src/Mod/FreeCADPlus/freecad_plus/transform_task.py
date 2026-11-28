# SPDX-License-Identifier: LGPL-2.1-or-later
"""Whole-shape transformation collector; no active native Body is required."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from . import transforms, planes, modeling, editing, panel, document
from .transform_ui import Form
from .selection_list import removing, reference_key
from .shape_preview import ShapePreview

_active = None


class TransformTask(QtCore.QObject):
    reference_guidance = True

    def __init__(self, kind, feature=None):
        super().__init__()
        self.doc=Gui.activeDocument().Document;self.owner,self.path=modeling._context(self.doc)
        self.view=Gui.activeDocument().activeView();self.feature=feature;self.kind=kind
        self.closed=False;self.busy=False;self.pick_step=None;self.refs=[]
        self.form=Form(kind,self.owner);self.preview=ShapePreview(self.view)
        self.timer=QtCore.QTimer(self);self.timer.setSingleShot(True);self.timer.timeout.connect(self.refresh)
        self.form.objects.installEventFilter(self)
        self.form.objects.clicked.connect(lambda:self.choose_sources())
        self.form.remove.clicked.connect(self.remove);self.form.clear.clicked.connect(self.clear)
        self.form.done.clicked.connect(self.accept);self.form.apply.clicked.connect(self.apply);self.form.cancel.clicked.connect(self.reject)
        self.form.merge.toggled.connect(self.schedule);self.form.preview.toggled.connect(self.schedule)
        if kind=='Multi-transform':
            self.form.order.model().rowsInserted.connect(self.connect_steps)
            self.form.order.model().rowsRemoved.connect(self.schedule)
            self.form.up.clicked.connect(self.schedule);self.form.down.clicked.connect(self.schedule)
        if feature:
            self.refs=planes.flatten(feature.TransformSources);self.form.merge.setChecked(feature.MergeResults)
            self.form.name.setText(feature.Label)
            values=transforms.settings(feature)
            if kind=='Multi-transform':
                for value in values:self.form.add_step(value['kind'])
            for step,value in zip(self.form.steps,values):self.load_step(step,value)
        self.connect_steps();self.fields()
        Gui.Selection.addObserver(self,0);App.addDocumentObserver(self)
        editing.add_context_observer(self.schedule)

    def choose_sources(self):self.pick_step=None

    def connect_steps(self,*args):
        for step in self.form.steps:
            if getattr(step,'connected',False):continue
            step.connected=True;step.ref=getattr(step,'ref',None);step.pick.installEventFilter(self)
            for widget in step.findChildren(QtWidgets.QComboBox):widget.currentIndexChanged.connect(self.schedule)
            for widget in step.findChildren(QtWidgets.QAbstractSpinBox):widget.editingFinished.connect(self.schedule)
            for widget in step.findChildren(QtWidgets.QCheckBox):widget.toggled.connect(self.schedule)
        self.schedule()

    def load_step(self,step,value):
        step.reference.setCurrentIndex(value['axis']);step.ref=value.get('ref')
        if step.ref:step.pick.setText(step.ref[0].Label+'.'+step.ref[1])
        if step.kind=='Mirror':step.offset.setValue(value['offset'])
        else:
            step.count.setValue(value['count']);step.measure.setCurrentIndex(value['measure'])
            step.value.setValue(value['value']);step.reverse.setChecked(value['reverse'])
            if step.kind=='Polar pattern':
                for widget,number in zip(step.center,value['center']):widget.setValue(number)

    def settings(self):
        values=[]
        for step in self.form.steps:
            value=dict(kind=step.kind,axis=step.reference.currentIndex())
            if value['axis']==3:value['ref']=step.ref
            if step.kind=='Mirror':value['offset']=step.offset.value()
            else:
                value.update(count=step.count.value(),measure=step.measure.currentIndex(),value=step.value.value(),reverse=step.reverse.isChecked())
                if step.kind=='Polar pattern':value['center']=[w.value() for w in step.center]
            values.append(value)
        return values

    def eventFilter(self,watched,event):
        if self.closed or self.form is None:return False
        if event.type()==QtCore.QEvent.FocusIn:
            self.pick_step=next((step for step in self.form.steps if watched is step.pick),None)
        if watched is self.form.objects and event.type()==QtCore.QEvent.KeyPress and event.key()==QtCore.Qt.Key_Delete:
            self.remove();return True
        return False

    def check(self):
        if self.closed or Gui.activeDocument() is None or Gui.activeDocument().activeView()!=self.view:
            raise ValueError('The active file or component changed; reopen this task')
        owner,path=modeling._context(self.doc)
        if owner!=self.owner or tuple(path)!=tuple(self.path):raise ValueError('The active component changed; reopen this task')

    def fields(self):
        self.form.objects.clear()
        for obj,sub in self.refs:self.form.objects.addItem(obj.Label if obj else 'Missing source')

    def remove(self):
        for index in sorted((self.form.objects.row(i) for i in self.form.objects.selectedItems()),reverse=True):self.refs.pop(index)
        self.fields();self.schedule()

    def clear(self):self.refs=[];self.fields();self.schedule()

    def addSelection(self,doc,name,sub,*args):
        if self.closed or self.busy:return
        self.busy=True
        try:
            self.check();obj=App.getDocument(doc).getObject(name)
            if self.pick_step is not None and self.pick_step in self.form.steps:
                step=self.pick_step;ref=planes.canonical(self.owner,[(obj,sub)])[0]
                document.require_predecessors(self.owner,self.feature,[ref])
                kind=planes.describe(self.owner,ref)[0]
                if kind!=('plane' if step.kind=='Mirror' else 'line'):raise ValueError('Choose the indicated plane or straight axis')
                step.ref=ref;step.pick.setText(ref[0].Label+'.'+ref[1]);self.pick_step=None
            else:
                ref=transforms.source(self.owner,(obj,sub),self.feature)
                if removing():self.refs=[r for r in self.refs if reference_key(r)!=reference_key(ref)]
                elif ref not in self.refs:self.refs.append(ref)
                self.fields()
            Gui.Selection.removeSelection(doc,name,sub);self.schedule()
        except Exception as exc:self.form.status.setError(str(exc))
        finally:self.busy=False

    def schedule(self,*args):
        if not self.closed:self.timer.start(50)
    slotChangedObject=schedule
    slotRecomputedDocument=schedule

    def refresh(self):
        if self.closed or self.busy:return
        self.preview.clear()
        try:
            self.check()
            if not self.refs:self.form.status.setText('Select a body or sheet.');return
            shapes=transforms.evaluate(self.owner,self.refs,self.settings(),self.form.merge.isChecked(),self.feature)
            if self.form.preview.isChecked():self.preview.show(shapes,editing.world_placement(self.doc,self.path))
            self.form.status.setText('Ready. One Undo step.')
        except Exception as exc:self.form.status.setError(str(exc))

    def apply(self):
        if self.busy:return False
        try:
            self.check();self.busy=True;self.preview.clear()
            self.results=transforms.save(self.doc,self.refs,self.settings(),self.form.merge.isChecked(),self.kind,self.form.name.text().strip(),self.feature)
            self.feature=None;self.refs=[];self.form.reset()
            for step in self.form.steps:step.ref=None
            self.pick_step=None;self.fields();self.form.status.setText('Applied. Select geometry for the next result.')
            if panel._panel:panel._panel.refresh()
            return True
        except Exception as exc:self.form.status.setError(str(exc));return False
        finally:self.busy=False

    def accept(self):
        if self.refs and not self.apply():return False
        return self.reject()

    def reject(self):
        global _active
        if self.closed:return True
        self.closed=True;self.timer.stop();self.preview.close()
        Gui.Selection.removeObserver(self);App.removeDocumentObserver(self);editing.remove_context_observer(self.schedule)
        if _active is self:_active=None;Gui.Control.closeDialog()
        panel.end_feature_task(self);self.deleteLater();return True

    def slotDeletedDocument(self,doc):
        if doc in (self.doc,self.owner.Document):self.reject()
    def getStandardButtons(self):return 0
    def isAllowedAlterSelection(self):return True
    def isAllowedAlterView(self):return True
    def isAllowedAlterDocument(self):return False


def show(kind='Linear pattern',feature=None):
    global _active
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first')
    if feature:kind=feature.TransformKind
    initial=[(e.DocumentName,e.ObjectName,s) for e in Gui.Selection.getSelectionEx('*',0) for s in e.SubElementNames or ('',)]
    task=TransformTask(kind,feature);_active=task
    try:
        Gui.Control.showDialog(task);panel.begin_feature_task(task)
        if feature is None:
            for doc,name,sub in initial:task.addSelection(doc,name,sub)
        task.refresh()
    except Exception:task.reject();raise
    return task


def dispatch(kind):
    try:return show(kind)
    except Exception as exc:
        from .thicken_task import show_error
        show_error(kind,str(exc))
