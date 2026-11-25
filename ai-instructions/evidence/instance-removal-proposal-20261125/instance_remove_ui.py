"""UI-only removal review using explicit fixture data; no removal implementation."""
from PySide6 import QtCore, QtWidgets
from freecad_plus.task_status import TaskStatus


class RemoveDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, scenario='simple'):
        super().__init__(parent)
        self.setWindowTitle('Remove instance')
        self.resize(530, 260)
        box=QtWidgets.QVBoxLayout(self)
        def note(text):
            label=QtWidgets.QLabel(text); label.setWordWrap(True);box.addWidget(label);return label
        shared=scenario=='shared'
        component,owner,position,total=('Bolt','Gearbox',1,2) if shared else ('Motor','Machine',2,3)
        note('<b>Remove '+component+' ('+str(position)+' of '+str(total)+') from '+owner+'?</b>')
        table=QtWidgets.QTreeWidget();table.setHeaderLabels(['Parent assembly','Selected instance'])
        table.setRootIsDecorated(False);table.setMaximumHeight(88)
        table.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        QtWidgets.QTreeWidgetItem(table,[owner,component+' ('+str(position)+' of '+str(total)+')'])
        box.addWidget(table)
        note(str(total-1)+' '+component+' instance'+('s' if total>2 else '')+' will remain in '+owner+'.')
        note(component+' stays in Parts with its geometry and history.' + ('' if shared else ' Other placements of '+component+' remain.'))
        self.constraints=None;self.shared=None
        if scenario=='constraints':
            note('<b>Assembly constraints using this instance</b>')
            affected=QtWidgets.QListWidget();affected.addItem('Machine / Motor fixed to Machine');affected.setMaximumHeight(72);box.addWidget(affected)
            self.constraints=QtWidgets.QCheckBox('Also remove the listed assembly constraint')
            box.addWidget(self.constraints)
            note('Removal is unavailable until this constraint is included or its reference is changed.')
        if shared:
            note('<b>Gearbox is a shared assembly.</b>')
            note('Removing this child changes Gearbox wherever it is used, including other files. Removing an entire Gearbox instance instead leaves its children intact.')
            self.shared=QtWidgets.QCheckBox('Remove this child from the shared Gearbox assembly')
            box.addWidget(self.shared)
        self.blocked=scenario=='blocked'
        if self.blocked:
            status=TaskStatus();status.setError('Cannot remove this instance: Machine / Pad uses it as a geometry reference. Edit or remove that reference first.');box.addWidget(status)
        note('Undo restores the instance and any listed constraints removed with it.')
        buttons=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        self.remove=buttons.addButton('Remove instance',QtWidgets.QDialogButtonBox.AcceptRole)
        self.remove.setAutoDefault(False)
        cancel=buttons.button(QtWidgets.QDialogButtonBox.Cancel);cancel.setDefault(True);cancel.setFocus()
        buttons.rejected.connect(self.reject);buttons.accepted.connect(self.accept);box.addWidget(buttons)
        for check in (self.constraints,self.shared):
            if check:check.toggled.connect(self.refresh)
        self.refresh()

    def refresh(self,*args):
        self.remove.setEnabled(not self.blocked and all(check is None or check.isChecked() for check in (self.constraints,self.shared)))

    def accept(self):
        # Intentionally no link/constraint deletion in this layout preview.
        if self.remove.isEnabled():super().accept()
