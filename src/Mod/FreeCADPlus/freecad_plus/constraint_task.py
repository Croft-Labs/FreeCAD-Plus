# SPDX-License-Identifier: LGPL-2.1-or-later
"""The native joint editor, scoped to the selected component assembly."""
import FreeCAD as App
import FreeCADGui as Gui
import JointObject
import UtilsAssembly
from . import constraints, document, panel
from .task_status import TaskStatus


def refresh_panel():
    if panel._panel is not None:
        panel._panel.refresh()


class ConstraintTask(JointObject.TaskAssemblyCreateJoint):
    def __init__(self, owner, binding, solver, index, joint=None):
        self.owner, self.binding = owner, binding
        self.owner_ref = panel.identity(owner)
        self.status = TaskStatus('Select two references within this assembly.')
        self.error = None
        super().__init__(index, joint, assembly=solver, view=binding[1], transaction=False)
        self.form.layout().addWidget(self.status)
        self.jForm.setWindowTitle('Assembly constraint — ' + owner.Label)

    def handleInitialSelection(self):
        self.refs = []
        for selected in Gui.Selection.getSelectionEx('*', 0):
            for sub in selected.SubElementNames or ('',):
                obj, relative = constraints.component_reference(self.assembly, selected.Object, sub)
                if obj is not None and all(ref[0] != obj for ref in self.refs):
                    self.refs.append((obj, [relative, relative]))
        if len(self.refs) > 2:
            self.refs = []
        self.updateJoint()

    def updateJointList(self):
        self.jForm.featureList.clear()
        for obj, subs in self.refs:
            if obj == self.owner.Origin:
                label = self.owner.Label + ' — Origin'
            elif obj.TypeId == 'App::Link':
                label = obj.LinkedObject.Label
            else:
                label = obj.Label
            element = UtilsAssembly.getElementName(subs[0]) if subs else ''
            self.jForm.featureList.addItem(label + ('.' + element if element else ''))

    def updateJoint(self):
        placements = [(o, App.Placement(o.Placement)) for o in self.owner.Group
                      if hasattr(o, 'Placement')]
        try:
            if len(self.refs) == 2:
                constraints.validate_refs(self.owner, self.refs)
            super().updateJoint()
            if len(self.refs) == 2 and self.assembly.solve() != 0:
                raise ValueError('These assembly constraints could not be solved. Change the references or values.')
            self.error = None
            self.status.setText('' if len(self.refs) == 2 else 'Select two references within this assembly.')
        except (ValueError, RuntimeError, AttributeError) as error:
            for obj, placement in placements:
                obj.Placement = placement
            self.error = str(error)
            self.status.setError(self.error)
        refresh_panel()

    def accept(self):
        try:
            if panel.lookup(self.owner_ref) != self.owner or panel._panel._current() != self.binding:
                raise ValueError('The assembly view changed. Cancel and reopen the constraint.')
            constraints.validate_refs(self.owner, self.refs)
            self.updateJoint()
            if self.error:
                return False
            document.validate(self.doc)
            self.doc.recompute()
            if self.assembly.solve() != 0:
                raise ValueError('These assembly constraints could not be solved.')
            self.joint.Visibility = self.visibilityBackup
            self.deactivate()
            App.closeActiveTransaction()
            refresh_panel()
            return True
        except (ValueError, RuntimeError, ReferenceError) as error:
            self.status.setError(str(error))
            return False

    def reject(self):
        # The first constraint may have created the solver; abort deletes it too.
        self.deactivate()
        App.closeActiveTransaction(True)
        if self.doc.Name in App.listDocuments():
            self.doc.recompute()
        refresh_panel()
        return True


def open_task(index=0, joint=None):
    if Gui.Control.activeDialog() or App.getActiveTransaction():
        raise ValueError('Finish the current task before editing assembly constraints')
    if joint is None:
        owner, binding, _ = constraints.active_context()
    else:
        solver = joint.Proxy.getAssembly(joint)
        owner = constraints.owner_of(solver) if solver is not None else None
        if owner is None or joint not in constraints.joints(owner):
            raise ValueError('The assembly constraint is no longer available')
        binding = panel._panel._current() if panel._panel else None
        if binding is None:
            raise ValueError('Open the component assembly before editing its constraints')
        index = JointObject.JointTypes.index(joint.JointType)
    document.validate(owner.Document)
    if owner.Document.HasPendingTransaction:
        raise ValueError('Finish the current operation first')
    transaction = App.setActiveTransaction('Edit assembly constraint' if joint else 'Create assembly constraint')
    task = None
    try:
        solver = constraints.ensure_solver(owner)
        task = ConstraintTask(owner, binding, solver, index, joint)
        dialog = Gui.Control.showDialog(task)
        if dialog is not None:
            dialog.setAutoCloseOnTransactionChange(True)
            dialog.setAutoCloseOnDeletedDocument(True)
            dialog.setDocumentName(owner.Document.Name)
        refresh_panel()
        return task
    except Exception:
        if task is not None:
            task.deactivate()
        JointObject.activeTask = None
        App.closeActiveTransaction(True, transaction)
        raise
