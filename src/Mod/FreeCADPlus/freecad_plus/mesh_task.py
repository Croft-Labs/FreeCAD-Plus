# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native mesher controls with a post-open mixed source collector."""
import math
import FreeCAD as App,FreeCADGui as Gui
from PySide6 import QtCore,QtWidgets
from . import document,modeling,planes,transforms,mesh_shape,panel,selection_scope
from .selection_list import removing
from .mesh_ui import MeshForm
_active=None
_edit=None


class MeshTask(QtCore.QObject):
    reference_guidance=True
    def __init__(self,tess,feature=None):
        super().__init__();self.doc=Gui.activeDocument().Document;self.owner,self.path=modeling._context(self.doc)
        self.view=Gui.activeDocument().activeView();self.feature=feature;self.refs=planes.flatten(feature.MeshSources) if feature else []
        self.closed=False;self.busy=False;self.cancelled=False;self.form=MeshForm(tess)
        self.form.destination.setText('Add to: '+self.owner.Label);self.form.sources.installEventFilter(self)
        self.form.remove.clicked.connect(self.remove);self.form.clear.clicked.connect(self.clear)
        self.form.done.clicked.connect(self.accept);self.form.apply.clicked.connect(self.apply);self.form.cancel.clicked.connect(self.reject)
        self.form.surface.toggled.connect(self.domain)
        self.form.tess.findChild(QtWidgets.QPushButton,'killButton').clicked.connect(self.cancel_mesh)
        if feature:
            import json
            self.restore_settings(json.loads(feature.MeshSettings))
        Gui.Selection.addObserver(self,0);App.addDocumentObserver(self);self.fields();self.domain()

    def widget(self,name):return self.form.tess.findChild(QtWidgets.QWidget,name)
    def number(self,name):
        value=self.widget(name).property('value')
        return float(value.Value if hasattr(value,'Value') else value)
    def checked(self,name):return self.widget(name).isChecked()

    def settings(self):
        method=self.form.method.currentIndex();p={}
        if method==0:
            p=dict(LinearDeflection=self.number('spinSurfaceDeviation'),AngularDeflection=math.radians(self.number('spinAngularDeviation')),Relative=self.checked('relativeDeviation'))
        elif method==1:p=dict(MaxLength=self.number('spinMaximumEdgeLength') if self.widget('spinMaximumEdgeLength').isEnabled() else 0)
        elif method==2:
            index=self.widget('comboFineness').currentIndex()
            p=dict(SecondOrder=self.checked('checkSecondOrder'),Optimize=self.checked('checkOptimizeSurface'),AllowQuad=self.checked('checkQuadDominated'))
            if index<=4:p['Fineness']=index
            else:p.update(GrowthRate=self.number('doubleGrading'),SegPerEdge=self.number('spinEdgeElements'),SegPerRadius=self.number('spinCurvatureElements'))
        settings=dict(method=method,parameters=p,colors=self.checked('meshShapeColors'),group_colors=self.checked('groupsFaceColors'))
        if method==3:
            settings.update(executable=self.widget('fileChooser').property('fileName'),algorithm=int(self.widget('method').currentData()),min_size=self.number('minSize'),max_size=self.number('maxSize'))
        # Preserve every native control, including inactive engine settings,
        # to reopen this same task without silently changing the recipe.
        state={}
        for w in self.form.tess.findChildren(QtWidgets.QWidget):
            if isinstance(w,QtWidgets.QCheckBox):state[w.objectName()]=['checked',w.isChecked()]
            elif isinstance(w,QtWidgets.QComboBox):state[w.objectName()]=['currentIndex',w.currentIndex()]
            elif isinstance(w,QtWidgets.QAbstractSpinBox):state[w.objectName()]=['value',self.number(w.objectName())]
        settings['controls']=state
        return settings

    def restore_settings(self,settings):
        for name,(prop,value) in settings.get('controls',{}).items():
            widget=self.widget(name)
            if widget:widget.setProperty(prop,value)
        self.form.method.setCurrentIndex(settings['method'])
        if settings.get('executable'):self.widget('fileChooser').setProperty('fileName',settings['executable'])

    def domain(self,*args):
        self.form.sources.setProperty('FreeCADPlusPickDomain','surface' if self.form.surface.isChecked() else None)
        selection_scope.changed()
    def fields(self):
        self.form.sources.clear()
        for obj,sub in self.refs:self.form.sources.addItem(obj.Label+('.'+sub if sub else ''))
        self.form.apply.setEnabled(bool(self.refs));self.form.status.setText('Ready to create one combined mesh.' if self.refs else 'Select one or more solids, sheets or faces to mesh.')
    def remove(self):
        for index in sorted((self.form.sources.row(i) for i in self.form.sources.selectedItems()),reverse=True):self.refs.pop(index)
        self.fields()
    def clear(self):self.refs=[];self.fields()
    def eventFilter(self,obj,event):
        if self.closed or self.form is None:return False
        if obj is self.form.sources and event.type()==QtCore.QEvent.KeyPress and event.key()==QtCore.Qt.Key_Delete:self.remove();return True
        return False
    def check(self):
        if self.closed or not Gui.activeDocument() or Gui.activeDocument().activeView()!=self.view:raise ValueError('The active file changed; reopen this task')
        owner,path=modeling._context(self.doc)
        if owner!=self.owner or tuple(path)!=tuple(self.path):raise ValueError('The active component changed; reopen this task')
    def addSelection(self,doc,name,sub,*args):
        if self.busy or self.closed:return
        self.busy=True
        try:
            self.check();ref=(App.getDocument(doc).getObject(name),sub)
            ref=planes.canonical(self.owner,[ref])[0] if self.form.surface.isChecked() else transforms.source(self.owner,ref,self.feature)
            shape=planes.shape(self.owner,ref)
            if not shape.Faces:raise ValueError('Choose geometry with faces')
            if self.form.solid.isChecked() and not shape.Solids:raise ValueError('Switch to Surface to add a sheet or face')
            if self.form.surface.isChecked() and shape.Solids:raise ValueError('Choose an individual face or a whole sheet')
            document.require_predecessors(self.owner,self.feature,[ref])
            if removing():self.refs=[r for r in self.refs if r!=ref]
            elif ref not in self.refs:self.refs.append(ref)
            Gui.Selection.removeSelection(doc,name,sub);self.fields()
        except Exception as exc:self.form.status.setError(str(exc))
        finally:self.busy=False
    def cancel_mesh(self):self.cancelled=True
    def apply(self):
        if self.busy:return False
        try:
            self.check();self.busy=True;self.cancelled=False
            self.widget('killButton').setEnabled(self.form.method.currentIndex()==3)
            self.form.status.setText('Meshing selected geometry…')
            self.result=mesh_shape.save(self.doc,self.refs,self.settings(),self.feature,lambda:self.cancelled or self.closed)
            self.feature=None;self.refs=[];self.form.reset();self.fields();self.domain()
            self.form.status.setText('Mesh created. Select sources for another mesh.')
            if panel._panel:panel._panel.refresh()
            return True
        except Exception as exc:
            if not self.closed:self.form.status.setError(str(exc))
            return False
        finally:
            self.busy=False
            if not self.closed:self.widget('killButton').setEnabled(False)
            if self.cancelled:self.reject()
    def accept(self):
        if not self.refs or self.apply():return self.reject()
        return False
    def reject(self):
        global _active
        if self.busy:self.cancelled=True;return False
        if self.closed:return True
        self.closed=True;Gui.Selection.removeObserver(self);App.removeDocumentObserver(self)
        self.form.sources.setProperty('FreeCADPlusPickDomain',None)
        if _active is self:_active=None;Gui.Control.closeDialog()
        panel.end_feature_task(self);selection_scope.changed();self.deleteLater();return True
    def slotDeletedDocument(self,doc):
        if doc in (self.doc,self.owner.Document):self.reject()
    def getStandardButtons(self):return 0
    def isAllowedAlterSelection(self):return True
    def isAllowedAlterView(self):return True
    def isAllowedAlterDocument(self):return False


def dispatch():
    global _active,_edit
    tess=Gui.getMainWindow().findChild(QtWidgets.QWidget,'PlusMeshParameters')
    feature,_edit=_edit,None
    try:
        initial=[(e.DocumentName,e.ObjectName,s) for e in Gui.Selection.getSelectionEx('*',0) for s in e.SubElementNames or ('',)]
        task=MeshTask(tess,feature);_active=task;Gui.Control.showDialog(task);panel.begin_feature_task(task)
        if feature is None:
            for doc,name,sub in initial:task.addSelection(doc,name,sub)
        return task
    except Exception:
        if _active:_active.reject()
        elif tess:tess.deleteLater()
        raise


def show(feature=None):
    global _edit
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first')
    import MeshPartGui
    _edit=feature
    try:Gui.runCommand('MeshPart_Mesher')
    finally:_edit=None
    return _active
