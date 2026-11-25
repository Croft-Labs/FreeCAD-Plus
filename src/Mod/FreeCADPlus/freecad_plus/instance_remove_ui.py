# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native review for one instance; acceptance revalidates the displayed plan."""
from PySide6 import QtCore, QtWidgets
from . import instance_remove, panel
from .task_status import TaskStatus


class RemoveDialog(QtWidgets.QDialog):
    def __init__(self, dock, row):
        super().__init__(dock)
        self.dock = dock
        self.plan = instance_remove.plan(dock, row)
        self.setWindowTitle('Remove instance')
        self.resize(530, 300)
        layout = QtWidgets.QVBoxLayout(self)
        def note(text, bold=False):
            label = QtWidgets.QLabel(text); label.setTextFormat(QtCore.Qt.PlainText)
            label.setWordWrap(True)
            if bold:
                font = label.font(); font.setBold(True); label.setFont(font)
            layout.addWidget(label); return label
        owner = panel.lookup(self.plan.owner); definition = panel.lookup(self.plan.definition)
        total = len(self.plan.siblings); position = self.plan.siblings.index(self.plan.link) + 1
        title = definition.Label + ' (' + str(position) + ' of ' + str(total) + ')'
        note('Remove ' + title + ' from ' + owner.Label + '?', True)
        table = QtWidgets.QTreeWidget(); table.setHeaderLabels(['Parent assembly', 'Selected instance'])
        table.setRootIsDecorated(False); table.setMaximumHeight(88)
        table.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTreeWidgetItem(table, [instance_remove.qualified(owner), title])
        item.setToolTip(0, owner.Document.FileName or owner.Document.Label)
        item.setToolTip(1, panel.lookup(self.plan.link).Name)
        layout.addWidget(table)
        note(str(total - 1) + ' ' + definition.Label + ' instance' + ('' if total == 2 else 's')
             + ' will remain in ' + owner.Label + '.')
        note(definition.Label + ' stays in Parts with its geometry and history.'
             + ('' if self.plan.shared else ' Other placements remain.'))
        self.constraints = None; self.shared = None
        if self.plan.constraints:
            note('Assembly constraints using this instance', True)
            affected = QtWidgets.QListWidget(); affected.setMaximumHeight(90)
            affected.addItems([instance_remove.qualified(owner) + ' / ' + panel.lookup(ref).Label
                               for ref in self.plan.constraints])
            layout.addWidget(affected)
            self.constraints = QtWidgets.QCheckBox('Also remove the listed assembly constraints')
            layout.addWidget(self.constraints)
            note('Removal is unavailable until these constraints are included or their references are changed.')
        if self.plan.shared:
            note(owner.Label + ' is a shared assembly.', True)
            note('Removing this child changes ' + owner.Label + ' wherever it is used, including other files. '
                 'Removing an entire ' + owner.Label + ' instance instead leaves its children intact.')
            self.shared = QtWidgets.QCheckBox('Remove this child from the shared ' + owner.Label + ' assembly')
            layout.addWidget(self.shared)
        self.status = TaskStatus(); layout.addWidget(self.status)
        if self.plan.blocked: self.status.setError('\n'.join(self.plan.blocked))
        else: self.status.hide()
        note('Undo restores the instance and any listed constraints removed with it.')
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        self.remove = buttons.addButton('Remove instance', QtWidgets.QDialogButtonBox.AcceptRole)
        self.remove.setAutoDefault(False)
        cancel = buttons.button(QtWidgets.QDialogButtonBox.Cancel)
        cancel.setDefault(True); cancel.setFocus()
        buttons.rejected.connect(self.reject); buttons.accepted.connect(self.accept); layout.addWidget(buttons)
        for check in (self.constraints, self.shared):
            if check is not None: check.toggled.connect(self.refresh)
        self.refresh()

    def refresh(self, *args):
        self.remove.setEnabled(not self.plan.blocked and all(
            check is None or check.isChecked() for check in (self.constraints, self.shared)))

    def accept(self):
        if not self.remove.isEnabled(): return
        try:
            instance_remove.remove(self.dock, self.plan,
                include_constraints=self.constraints is not None and self.constraints.isChecked(),
                acknowledge_shared=self.shared is not None and self.shared.isChecked())
        except (ValueError, RuntimeError, ReferenceError) as error:
            self.status.setError(str(error)); self.status.show()
            return
        super().accept()


def open_dialog(dock, row):
    dialog = RemoveDialog(dock, row)
    try: return dialog.exec()
    finally: dialog.deleteLater()
