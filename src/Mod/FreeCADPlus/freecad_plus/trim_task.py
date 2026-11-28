# SPDX-License-Identifier: LGPL-2.1-or-later
import json
import FreeCAD as App,FreeCADGui as Gui
from PySide6 import QtCore,QtWidgets
from . import document,modeling,editing,planes,transforms,trim_body,panel
from .selection_list import removing
from .shape_preview import ShapePreview
from .trim_ui import Form
_active=None


class TrimTask(QtCore.QObject):
    reference_guidance=True
    def __init__(self,feature=None):
        super().__init__();self.doc=Gui.activeDocument().Document;self.owner,self.path=modeling._context(self.doc)
        self.view=Gui.activeDocument().activeView();self.feature=feature;self.target=None;self.refs=[];self.plane_ref=None
        self.closed=False;self.busy=False;self.pick='target';self.form=Form(self.owner)
        self.preview=ShapePreview(self.view);self.waste=ShapePreview(self.view)
        self.timer=QtCore.QTimer(self);self.timer.setSingleShot(True);self.timer.timeout.connect(self.refresh)
        for widget in (self.form.target,self.form.reference,self.form.surfaces):widget.installEventFilter(self)
        self.form.clear_target.clicked.connect(self.clear_target);self.form.clear.clicked.connect(self.clear)
        self.form.remove.clicked.connect(self.remove);self.form.done.clicked.connect(self.accept)
        self.form.apply.clicked.connect(self.apply);self.form.cancel.clicked.connect(self.reject)
        self.form.preview.toggled.connect(self.schedule);self.form.reverse.toggled.connect(self.schedule)
        self.form.mode.currentIndexChanged.connect(self.schedule);self.form.plane.currentIndexChanged.connect(self.schedule)
        self.form.offset.editingFinished.connect(self.schedule)
        self.form.offset.committed.connect(self.schedule)
        if feature:
            obj,subs=feature.TrimTarget;self.target=(obj,subs[0] if subs else '')
            values=json.loads(feature.TrimSettings);refs=planes.flatten(feature.TrimTools)
            self.form.mode.setCurrentIndex(values['mode']);self.form.plane.setCurrentIndex(values['plane'])
            self.form.offset.setValue(values['offset']);self.form.reverse.setChecked(values['reverse'])
            unit=values.get('offset_unit','mm')
            try:
                if App.Units.Quantity('1 '+unit).Unit==self.form.offset._dimension:self.form.offset.setSuffix(unit)
            except (ValueError,TypeError,RuntimeError):pass
            if values['mode']==1:self.plane_ref=refs[0] if refs else None
            else:self.refs=refs
            self.pick='tools'
        Gui.Selection.addObserver(self,0);App.addDocumentObserver(self);editing.add_context_observer(self.schedule);self.fields()

    def fields(self):
        self.form.target.setText(self.target[0].Label if self.target else '')
        self.form.reference.setText(self.plane_ref[0].Label if self.plane_ref else '')
        self.form.surfaces.clear()
        for obj,sub in self.refs:self.form.surfaces.addItem(obj.Label+('.'+sub if sub else ''))
        self.schedule()
    def clear_target(self):self.target=None;self.pick='target';self.fields()
    def clear(self):self.refs=[];self.fields()
    def remove(self):
        for i in sorted((self.form.surfaces.row(w) for w in self.form.surfaces.selectedItems()),reverse=True):self.refs.pop(i)
        self.fields()
    def eventFilter(self,obj,event):
        if self.closed or self.form is None:return False
        if event.type() in (QtCore.QEvent.FocusIn,QtCore.QEvent.MouseButtonPress):
            self.pick='target' if obj is self.form.target else 'plane' if obj is self.form.reference else 'tools'
        if obj is self.form.surfaces and event.type()==QtCore.QEvent.KeyPress and event.key()==QtCore.Qt.Key_Delete:self.remove();return True
        return False
    def check(self):
        if self.closed or not Gui.activeDocument() or Gui.activeDocument().activeView()!=self.view:raise ValueError('The active file changed; reopen this task')
        owner,path=modeling._context(self.doc)
        if owner!=self.owner or tuple(path)!=tuple(self.path):raise ValueError('The active component changed; reopen this task')
    def addSelection(self,doc,name,sub,*args):
        if self.busy or self.closed:return
        self.busy=True
        try:
            self.check();raw=(App.getDocument(doc).getObject(name),sub)
            if self.pick=='target':
                ref=transforms.source(self.owner,raw,self.feature)
                if not planes.shape(self.owner,ref).Solids:raise ValueError('Choose a solid target')
                self.target=None if removing() else ref;self.pick='tools'
            else:
                ref=planes.canonical(self.owner,[raw])[0];document.require_predecessors(self.owner,self.feature,[ref])
                if self.pick=='plane':
                    if planes.describe(self.owner,ref)[0]!='plane':raise ValueError('Choose a datum plane')
                    self.plane_ref=ref
                else:
                    shape=planes.shape(self.owner,ref)
                    if not shape.Faces or shape.Solids:raise ValueError('Choose a face or sheet')
                    if removing():self.refs=[r for r in self.refs if r!=ref]
                    elif ref not in self.refs:self.refs.append(ref)
            Gui.Selection.removeSelection(doc,name,sub);self.fields()
        except Exception as exc:self.form.status.setError(str(exc))
        finally:self.busy=False
    def settings(self,commit=False):
        if commit:
            if not self.form.offset.hasAcceptableInput():raise ValueError('Enter a valid offset length, such as 0.25 in.')
            self.form.offset.interpretText()
        return dict(mode=self.form.mode.currentIndex(),plane=self.form.plane.currentIndex(),offset=self.form.offset.value(),
                    offset_unit=self.form.offset._unit,reverse=self.form.reverse.isChecked())
    def tools(self):return ([self.plane_ref] if self.plane_ref else []) if self.form.mode.currentIndex()==1 else self.refs
    def schedule(self,*args):
        if not self.closed:self.timer.start(60)
    slotChangedObject=schedule
    slotRecomputedDocument=schedule
    def refresh(self):
        if self.closed or self.busy:return
        self.preview.clear();self.waste.clear()
        try:
            self.check()
            if not self.target:return
            retained,removed=trim_body.evaluate(self.owner,self.target,self.tools(),self.settings(),self.feature)
            if self.form.preview.isChecked():
                frame=editing.world_placement(self.doc,self.path)
                self.preview.show([retained],frame,transparency=0)
                self.waste.show([removed],frame,(.9,.15,.12),.5)
            self.form.status.setText('Ready. One linked Trim Body feature.');self.form.apply.setEnabled(True)
        except Exception as exc:self.form.status.setError(str(exc));self.form.apply.setEnabled(False)
    def apply(self):
        try:
            self.check();self.busy=True;self.preview.clear();self.waste.clear()
            if self.target is None:raise ValueError('Choose a target body')
            self.result=trim_body.save(self.doc,self.target,self.tools(),self.settings(commit=True),self.feature)
            self.feature=None;self.target=None;self.refs=[];self.plane_ref=None;self.pick='target';self.form.reset();self.fields()
            if panel._panel:panel._panel.refresh()
            return True
        except Exception as exc:self.form.status.setError(str(exc));return False
        finally:self.busy=False
    def accept(self):
        if not self.target or self.apply():return self.reject()
        return False
    def reject(self):
        global _active
        if self.closed:return True
        self.closed=True;self.timer.stop();self.preview.close();self.waste.close()
        Gui.Selection.removeObserver(self);App.removeDocumentObserver(self);editing.remove_context_observer(self.schedule)
        if _active is self:_active=None;Gui.Control.closeDialog()
        panel.end_feature_task(self);self.deleteLater();return True
    def slotDeletedDocument(self,doc):
        if doc in (self.doc,self.owner.Document):self.reject()
    def getStandardButtons(self):return 0
    def isAllowedAlterSelection(self):return True
    def isAllowedAlterView(self):return True
    def isAllowedAlterDocument(self):return False


def show(feature=None):
    global _active
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first')
    initial=[(e.DocumentName,e.ObjectName,s) for e in Gui.Selection.getSelectionEx('*',0) for s in e.SubElementNames or ('',)]
    task=TrimTask(feature);_active=task;Gui.Control.showDialog(task);panel.begin_feature_task(task)
    if feature is None:
        for doc,name,sub in initial:task.addSelection(doc,name,sub)
    return task


class Command:
    def GetResources(self):return dict(MenuText='Trim Body',ToolTip='Trim a body to a complete surface boundary or plane',Pixmap='Part_Cut')
    def IsActive(self):
        if not Gui.activeDocument() or Gui.Control.activeDialog():return False
        try:modeling._context(Gui.activeDocument().Document);return True
        except (ValueError,RuntimeError):return False
    def Activated(self):
        try:show()
        except Exception as exc:
            from .thicken_task import show_error
            show_error('Trim Body',str(exc))


def install():Gui.addCommand('Plus_TrimBody',Command())
