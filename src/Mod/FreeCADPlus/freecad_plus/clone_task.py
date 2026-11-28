# SPDX-License-Identifier: LGPL-2.1-or-later
"""Occurrence-aware native Clone/Extract task; previews never mutate documents."""
import FreeCAD as App, FreeCADGui as Gui, Part
from PySide6 import QtCore, QtWidgets
from pivy import coin
from . import document, editing, hierarchy, modeling, panel, derived_geometry as derived
from .clone_ui import GeometryForm
from .selection_list import removing
_active=None


class GeometryTask(QtCore.QObject):
    reference_guidance=True
    def __init__(self,extract=False,feature=None):
        super().__init__()
        self.doc=Gui.activeDocument().Document
        self.definition,self.path=modeling._context(self.doc)
        self.owner_doc=self.definition.Document
        if any(Gui.getDocument(d.Name).getInEdit() for d in App.listDocuments().values()):
            raise ValueError('Finish the native feature editor first')
        self.view=Gui.activeDocument().activeView();self.scene=self.view.getSceneGraph()
        self.context=(self.doc,self.view,panel.identity(self.definition),tuple(panel.identity(o) for o in self.path))
        self.feature=feature;self.feature_ref=panel.identity(feature) if feature else None
        self.operation=feature.DerivedOperation if feature else ('Extract' if extract else 'Clone')
        self.extract=self.operation=='Extract'
        if feature and (not derived.is_derived(feature) or derived.owner(feature)!=self.definition):
            raise ValueError('Edit a derived result owned by this component')
        self.revision=derived.revision(feature) if feature else None
        self.refs=derived.saved_refs(feature) if feature else []
        self.closed=False;self.busy=False;self.collecting=True;self.overlay=None;self.pending=[]
        self.form=GeometryForm(self.definition,self.extract,feature)
        self.timer=QtCore.QTimer(self);self.timer.setSingleShot(True);self.timer.timeout.connect(self.refresh)
        self.pick_timer=QtCore.QTimer(self);self.pick_timer.setSingleShot(True);self.pick_timer.timeout.connect(self.deliver_picks)
        self.form.objects.activated.connect(self.activate)
        self.form.objects.removeRequested.connect(self.remove_inputs)
        self.form.remove.clicked.connect(self.remove_inputs);self.form.clear.clicked.connect(self.clear_inputs)
        self.form.preview.toggled.connect(self.refresh);self.form.update.toggled.connect(self.refresh)
        if self.form.join:self.form.join.toggled.connect(self.change_join)
        if self.form.browse:self.form.browse.clicked.connect(self.browse)
        self.initial=[(e.Object,s) for e in Gui.Selection.getSelectionEx('*',0) for s in e.SubElementNames or ('',)]
        Gui.Selection.addObserver(self,0);App.addDocumentObserver(self)
        editing.add_context_observer(self.schedule)
        self.mdi=Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        if self.mdi:self.mdi.subWindowActivated.connect(self.schedule)
        self.fields()

    def check(self):
        if self.closed:raise ValueError('The geometry task is closed')
        if Gui.activeDocument() is None:raise ValueError('The file was closed')
        definition,path=modeling._context(Gui.activeDocument().Document)
        context=(Gui.activeDocument().Document,Gui.activeDocument().activeView(),
                 panel.identity(definition),tuple(panel.identity(o) for o in path))
        if context!=self.context:raise ValueError('The edited component or file tab changed. Cancel and reopen this task.')
        if self.feature_ref:
            feature=panel.lookup(self.feature_ref)
            if derived.revision(feature)!=self.revision:
                raise ValueError('The derived source changed. Cancel and reopen its editor.')

    def title(self,ref):
        obj,sub=ref
        if self.extract:return obj.Label+' / '+Part.splitSubname(sub)[2] if obj else 'Missing source'
        source=derived.target(ref)
        siblings=[o for o in self.definition.Group if o.TypeId=='App::Link' and o.LinkedObject==obj.LinkedObject]
        return obj.LinkedObject.Label+' ('+str(siblings.index(obj)+1)+') / '+source.Label

    def fields(self):
        self.form.objects.clear()
        names={o.Label for o in self.owner_doc.Objects};joined=self.extract and self.form.join.isChecked()
        first_name=self.feature.Label if self.feature else None
        for index,ref in enumerate(self.refs):
            try:
                source=derived.target(ref)
                kind='surface' if self.extract else derived.object_kind(source)
                title=self.title(ref)
                if self.feature and (index==0 or joined):name=self.feature.Label
                elif joined and first_name:name=first_name
                else:
                    base=derived.label_for(kind,self.operation);name=base;n=2
                    while name in names:name=base+' ('+str(n)+')';n+=1
                    names.add(name)
                if index==0:first_name=name
            except (ValueError,RuntimeError,ReferenceError):
                title='Missing source — remove this entry and choose a replacement';name=self.feature.Label if self.feature else ''
            item=QtWidgets.QTreeWidgetItem(self.form.objects,[title,name]);item.setToolTip(0,title)
        self.summary()

    def summary(self):
        joined=self.extract and self.form.join.isChecked()
        count=1 if joined and self.refs else len(self.refs)
        new=max(0,count-(1 if self.feature else 0))
        summary=('Update existing result'+(' + '+str(new)+' new result'+('s' if new!=1 else '') if new else '')) if self.feature else str(new)+' new result'+('s' if new!=1 else '')
        self.form.summary.setText(summary+' · One Undo step')

    def change_join(self,*args):
        self.fields();self.refresh()

    def activate(self):
        self.collecting=True
        self.form.status.setText('Pick faces on parent-owned geometry.' if self.extract else 'Click geometry in a direct child to select its whole source object.')

    def remove_inputs(self):
        indexes=sorted((self.form.objects.indexOfTopLevelItem(i) for i in self.form.objects.selectedItems()),reverse=True)
        for index in indexes:self.refs.pop(index)
        self.fields();self.refresh()

    def clear_inputs(self):
        self.refs=[];self.fields();self.refresh()

    def addSelection(self,doc,name,sub,*args):
        if self.closed or self.busy or not self.collecting:return
        try:
            obj=App.getDocument(doc).getObject(name)
            self.pending.append((panel.identity(obj),sub,removing()))
            self.pick_timer.start(0)
        except (ValueError,RuntimeError,ReferenceError):pass

    def deliver_picks(self):
        pending,self.pending=self.pending,[]
        for identity,sub,remove in pending:
            try:self.pick(panel.lookup(identity),sub,remove)
            except (ValueError,RuntimeError,ReferenceError,TypeError) as error:self.form.status.setError(str(error))

    def pick(self,obj,sub,remove=False):
        self.check()
        ref=derived.canonical(self.doc,self.definition,self.path,obj,sub,self.extract)
        derived.evaluate(self.definition,ref,self.operation,feature=self.feature)
        if remove:self.refs=[r for r in self.refs if r!=ref]
        elif self.feature and not self.extract:self.refs=[ref]
        elif ref not in self.refs:self.refs.append(ref)
        self.fields();self.refresh()
        self.busy=True
        try:Gui.Selection.removeSelection(obj,sub)
        finally:self.busy=False

    def browse(self):
        try:self.check()
        except (ValueError,RuntimeError,ReferenceError) as error:self.form.status.setError(str(error));return
        dialog=QtWidgets.QDialog(self.form);dialog.setWindowTitle('Whole objects from direct children');dialog.resize(530,350)
        layout=QtWidgets.QVBoxLayout(dialog)
        note=QtWidgets.QLabel('Choose objects owned by the direct child occurrences of '+self.definition.Label+'.');note.setWordWrap(True);layout.addWidget(note)
        tree=QtWidgets.QTreeWidget();tree.setHeaderLabels(['Child / object','Geometry']);layout.addWidget(tree)
        counts={}
        for link in self.definition.Group:
            if link.TypeId!='App::Link':continue
            counts[link.LinkedObject]=counts.get(link.LinkedObject,0)+1
            group=QtWidgets.QTreeWidgetItem(tree,[link.LinkedObject.Label+' — occurrence '+str(counts[link.LinkedObject]),''])
            group.setFlags(QtCore.Qt.ItemIsEnabled);group.setExpanded(True)
            def visit(obj,path):
                if obj.TypeId=='App::Link':return
                try:
                    kind=derived.object_kind(obj)
                    ref=(link,''.join(o.Name+'.' for o in path))
                    derived.whole_source(self.definition,ref)
                except (ValueError,RuntimeError,ReferenceError):pass
                else:
                    item=QtWidgets.QTreeWidgetItem(group,[' / '.join(o.Label for o in path),kind.capitalize()])
                    item.setData(0,QtCore.Qt.UserRole,(panel.identity(link),ref[1]))
                    item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)
                    item.setCheckState(0,QtCore.Qt.Checked if ref in self.refs else QtCore.Qt.Unchecked)
                for child in document.owned_children(obj):visit(child,[*path,child])
            for obj in document.owned_children(link.LinkedObject):visit(obj,[obj])
        tree.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        note=QtWidgets.QLabel('Reference children are eligible. Excluded children and deeper component levels are unavailable.');note.setWordWrap(True);layout.addWidget(note)
        from .task_status import TaskStatus
        status=TaskStatus();status.hide();layout.addWidget(status)
        buttons=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel);layout.addWidget(buttons)
        selected=[]
        def accept():
            try:
                self.check();refs=[]
                iterator=QtWidgets.QTreeWidgetItemIterator(tree)
                while iterator.value():
                    item=iterator.value();data=item.data(0,QtCore.Qt.UserRole)
                    if data and item.checkState(0)==QtCore.Qt.Checked:
                        ref=(panel.lookup(data[0]),data[1]);derived.evaluate(self.definition,ref,self.operation,feature=self.feature);refs.append(ref)
                    iterator+=1
                if self.feature and len(refs)!=1:raise ValueError('Choose one whole source object when editing '+self.feature.Label+'.')
                selected.extend(refs);dialog.accept()
            except (ValueError,RuntimeError,ReferenceError,TypeError) as error:status.setError(str(error));status.show()
        buttons.accepted.connect(accept);buttons.rejected.connect(dialog.reject)
        if dialog.exec()==QtWidgets.QDialog.Accepted:
            self.refs=selected;self.fields();self.refresh()
        dialog.deleteLater()

    def clear_preview(self):
        if self.overlay is not None:
            if self.scene.findChild(self.overlay)>=0:self.scene.removeChild(self.overlay)
            self.overlay=None

    def extraction_ready(self,ready):
        if not self.extract:return
        dock=Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks')
        if dock:
            for box in dock.findChildren(QtWidgets.QDialogButtonBox):
                button=box.button(QtWidgets.QDialogButtonBox.Ok)
                if button:button.setEnabled(ready)

    def refresh(self,*args):
        if self.closed or self.busy:return
        self.clear_preview()
        self.extraction_ready(False)
        try:
            self.check()
            self.summary()
            if not self.refs:
                self.form.status.setText('Click the list to pick faces.' if self.extract else 'Click the list or browse direct children to choose whole objects.')
                return
            values=[derived.evaluate(self.definition,r,self.operation,feature=self.feature) for r in self.refs]
            if self.extract and self.form.join.isChecked():
                shape=derived.joined_surface([value[2] for value in values])
                values=[(values[0][0],'surface',shape)]
            if self.feature and values[0][1]!=self.feature.GeometryKind:raise ValueError('Choose another '+self.feature.GeometryKind+' for this existing result')
            self.extraction_ready(True)
            self.form.status.setText('Ready. One Undo step.' if self.form.update.isChecked() else 'Preview is paused. OK recomputes the result.')
            if not self.form.preview.isChecked() or not self.form.update.isChecked():return
            overlay=coin.SoSeparator();style=coin.SoDrawStyle();style.style=coin.SoDrawStyle.LINES;style.setOverride(True);overlay.addChild(style)
            pick=coin.SoPickStyle();pick.style=coin.SoPickStyle.UNPICKABLE;overlay.addChild(pick)
            color=coin.SoBaseColor();color.rgb=(.1,.8,1);color.setOverride(True);overlay.addChild(color)
            frame=editing.world_placement(self.doc,self.path)
            for _,_,shape in values:
                shape=shape.copy();shape.Placement=frame.multiply(shape.Placement)
                source=coin.SoInput();source.setBuffer(shape.writeInventor());overlay.addChild(coin.SoDB.readAll(source))
            self.scene.addChild(overlay);self.overlay=overlay
        except (ValueError,RuntimeError,ReferenceError,TypeError,Part.OCCError) as error:
            self.form.status.setError(str(error))
            self.form.summary.setText('No result until the selection is corrected')

    def schedule(self,*args):
        if not self.closed and not self.busy:self.timer.start(0)
    slotChangedObject=schedule
    slotDeletedObject=schedule
    slotRecomputedDocument=schedule
    slotActivateDocument=schedule
    def slotDeletedDocument(self,doc):
        if doc==self.doc or doc==self.owner_doc:self.reject()

    def accept(self):
        try:
            self.check();self.busy=True
            self.results=derived.save(self.doc,self.refs,self.operation,self.feature,
                                      join=self.extract and self.form.join.isChecked())
            if self.definition.Document!=self.doc:self.doc.recompute()
        except (ValueError,RuntimeError,ReferenceError,TypeError,Part.OCCError) as error:
            self.form.status.setError(str(error));return False
        finally:self.busy=False
        self.reject()
        if panel._panel:panel._panel.refresh()
        return True

    def reject(self):
        global _active
        if self.closed:return True
        self.closed=True;self.timer.stop();self.pick_timer.stop();self.clear_preview()
        Gui.Selection.removeObserver(self);App.removeDocumentObserver(self);editing.remove_context_observer(self.schedule)
        if self.mdi:
            try:self.mdi.subWindowActivated.disconnect(self.schedule)
            except RuntimeError:pass
        if _active is self:_active=None;Gui.Control.closeDialog()
        if not getattr(self,'_continue_history',False):panel.end_feature_task(self)
        self.deleteLater();return True
    def getStandardButtons(self):return (QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel).value
    def isAllowedAlterDocument(self):return False
    def isAllowedAlterSelection(self):return True
    def isAllowedAlterView(self):return True


def show(feature=None,extract=False):
    global _active
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first')
    task=GeometryTask(extract,feature);_active=task
    try:
        Gui.Control.showDialog(task);panel.begin_feature_task(task);task.refresh()
        if not feature:
            for obj,sub in task.initial:
                if obj.getSubObject(sub,1)==task.definition:continue
                try:task.pick(obj,sub)
                except (ValueError,RuntimeError,ReferenceError) as error:task.form.status.setError(str(error))
    except Exception:task.reject();raise
    return task


class Command:
    def __init__(self,extract=False):self.extract=extract
    def GetResources(self):
        return dict(MenuText='Extract geometry' if self.extract else 'Clone',
            ToolTip='Extract faces from parent-owned geometry' if self.extract else 'Clone whole objects from direct children',
            Pixmap='PartDesign_SubShapeBinder' if self.extract else 'PartDesign_Clone')
    def IsActive(self):
        doc=App.ActiveDocument
        return doc is not None and not Gui.Control.activeDialog() and any('PlusFormat' in o.PropertiesList for o in doc.Objects)
    def Activated(self):
        try:show(extract=self.extract)
        except (ValueError,RuntimeError,ReferenceError) as error:
            from .thicken_task import show_error
            show_error('Extract geometry' if self.extract else 'Clone',str(error))


def install():
    Gui.addCommand('Plus_Clone',Command());Gui.addCommand('Plus_ExtractGeometry',Command(True))
