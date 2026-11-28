# SPDX-License-Identifier: LGPL-2.1-or-later
"""Name review for immediate commands; execution stays in the native command."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtWidgets
from . import document,editing,geometry,result_names
from .task_status import TaskStatus

BASES={'Part_Cut':'Cut','Part_Fuse':'Fusion','Part_Common':'Common','Part_Section':'Section',
       'Part_Compound':'Compound','Part_CompoundFilter':'CompoundFilter',
       'Part_JoinConnect':'Connect','Part_JoinEmbed':'Embed','Part_JoinCutout':'Cutout',
       'Part_Slice':'Slice','Part_SliceApart':'Slice','Part_BooleanFragments':'BooleanFragments',
       'Part_XOR':'XOR','Part_Defeaturing':'Defeatured','Part_ExplodeCompound':'Exploded'}
_active=None
_running=None


def dispatch(command):
    global _active
    if _running is not None:return False
    if Gui.Control.activeDialog():return False
    try:
        task=OperationTask(command)
    except (ValueError,RuntimeError,ReferenceError) as error:
        QtWidgets.QMessageBox.warning(Gui.getMainWindow(),'Ineligible geometry',str(error))
        return True
    _active=task;Gui.Control.showDialog(_active)
    return True


def completed(command):
    """Called before Command's outer AutoTransaction commits, including Python commands."""
    task=_running
    if task is None or command!=task.command:return
    try:finish(task)
    except Exception as error:
        task.error=str(error)
        raise


def finish(task):
    created=[o for o in task.owner.Document.Objects if o.ID not in task.before]
    # Compound tools historically group results at the root. Keep geometric
    # output in the component, as the existing Slice Apart adapter already does.
    groups=[o for o in created if o.TypeId=='App::DocumentObjectGroup']
    for group in groups:group.Group=[]
    for obj in created:
        if hasattr(obj,'Shape') and not document.owned_path(task.owner,obj):task.owner.addObject(obj)
    for group in groups:task.owner.Document.removeObject(group.Name)
    objects=[o for o in document.history(task.doc,task.owner) if o.ID not in task.before]
    if len(objects)!=len(task.labels):raise ValueError('The operation produced '+str(len(objects))+' results instead of '+str(len(task.labels))+'. Reopen it to review their names.')
    for obj,label in zip(objects,task.labels):result_names.assign(obj,label)
    task.owner.Document.recompute();document.validate(task.owner.Document)
    if any(hasattr(o,'Shape') and (o.Shape.isNull() or 'Invalid' in o.State) for o in objects):
        raise ValueError('The operation did not produce valid results. Correct the inputs and retry.')
    task.results=objects


class OperationTask:
    def __init__(self,command):
        self.command=command;self.doc=App.ActiveDocument;self.owner,self.path=editing.context_path(self.doc)
        self.selection=[(entry.Object,tuple(entry.SubElementNames)) for entry in Gui.Selection.getSelectionEx('',0)]
        geometry.require_part_boolean_inputs(self.doc,[(o,s) for o,subs in self.selection for s in subs or ('',)])
        self.objects=list(dict.fromkeys(o.getSubObject(sub,1) if sub else o
                                       for o,subs in self.selection for sub in subs or ('',)))
        self.before={o.ID for o in self.owner.Document.Objects}
        self.form=QtWidgets.QWidget();self.form.setWindowTitle(Gui.Command.get(command).getInfo()['menuText'].replace('&',''))
        layout=QtWidgets.QVBoxLayout(self.form);layout.addWidget(QtWidgets.QLabel('Component: '+self.owner.Label))
        sources=QtWidgets.QListWidget();sources.addItems([o.Label for o in self.objects]);sources.setMaximumHeight(130);layout.addWidget(sources)
        self.names=result_names.Names(layout,self.owner,section=True)
        labels=self.defaults();self.names.sync([(i,'Result name' if len(labels)==1 else 'Result '+str(i+1),name) for i,name in enumerate(labels)])
        self.status=TaskStatus('Ready. Names are saved with the operation in one Undo step.');layout.addWidget(self.status)
        layout.addStretch();self.results=[];self.closed=False

    def defaults(self):
        base=BASES[self.command]
        if self.command=='Part_ExplodeCompound':
            if len(self.objects)!=1:raise ValueError('Select one compound to explode.')
            return result_names.defaults(self.owner,[self.objects[0].Label+'.'+str(i) for i in range(len(self.objects[0].Shape.childShapes(False,False)))])
        if self.command=='Part_SliceApart':
            from BOPTools import SplitAPI
            if len(self.objects)<2:raise ValueError('Select a base and at least one slicing tool.')
            shape=SplitAPI.slice(self.objects[0].Shape,[o.Shape for o in self.objects[1:]],'Split')
            label=result_names.defaults(self.owner,[base])[0]
            return [label,*result_names.defaults(self.owner,[label+'.'+str(i) for i in range(len(shape.childShapes(False,False)))])]
        return result_names.defaults(self.owner,[base]*(len(self.objects) if self.command=='Part_Defeaturing' else 1))

    def accept(self):
        global _running
        try:
            if App.ActiveDocument!=self.doc or editing.context_path(self.doc)!=(self.owner,self.path):raise ValueError('The active component changed. Reopen the operation.')
            self.labels=self.names.values()
            self.before={o.ID for o in self.owner.Document.Objects};self.results=[];self.error=''
            Gui.Selection.clearSelection()
            for obj,subs in self.selection:
                for sub in subs or ('',):Gui.Selection.addSelection(obj,sub)
            _running=self
            Gui.runCommand(self.command)
            if not self.results:raise ValueError(self.error or 'The operation was not completed. Correct the inputs and retry.')
            return self.reject()
        except (ValueError,RuntimeError,ReferenceError) as error:
            self.status.setError(str(error));return False
        finally:_running=None

    def reject(self):
        global _active
        self.closed=True
        if _active is self:_active=None;Gui.Control.closeDialog()
        return True

    def getStandardButtons(self):return QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel
    def isAllowedAlterDocument(self):return False
