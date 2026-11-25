# SPDX-License-Identifier: LGPL-2.1-or-later
"""Review selected parts before exporting an independent native component file."""
from pathlib import Path
from PySide6 import QtCore, QtWidgets
from . import assembly, part_transfer_ops, task_status

class ExportDialog(QtWidgets.QDialog):
    def __init__(self, parent, parts, guard=lambda: None):
        super().__init__(parent)
        self.definitions = tuple(dict.fromkeys(parts))
        self.guard = guard
        parts = self.definitions
        part_transfer_ops.collect(parts)
        self.setWindowTitle('Export parts to file')
        self.setObjectName('ExportPartsDialog')
        self.resize(550, 435)
        box = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel(f'{len(parts)} selected parts')
        font = title.font(); font.setBold(True); title.setFont(font); box.addWidget(title)
        self.parts = QtWidgets.QTreeWidget()
        self.parts.setHeaderLabels(['Part', 'Components'])
        self.parts.header().setStretchLastSection(False)
        self.parts.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.parts.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        counts = assembly.counts(parts)
        for part in parts:
            item = QtWidgets.QTreeWidgetItem(self.parts, [part.Label, str(counts[part])])
            item.setIcon(0, part.ViewObject.Icon)
            item.setTextAlignment(1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        box.addWidget(self.parts)
        info = QtWidgets.QLabel('Creates independent, editable copies including child parts, history, '
                               'and assembly constraints. Shared child parts are copied once.')
        info.setWordWrap(True); box.addWidget(info)
        box.addWidget(QtWidgets.QLabel('Original parts and source files stay unchanged.'))
        box.addSpacing(8)
        box.addWidget(QtWidgets.QLabel('New component file'))
        row = QtWidgets.QHBoxLayout()
        self.filename = QtWidgets.QLineEdit()
        self.filename.setPlaceholderText('Choose a new .cadprt file')
        self.browse = QtWidgets.QPushButton('Browse…')
        self.browse.clicked.connect(self.choose_file)
        row.addWidget(self.filename, 1); row.addWidget(self.browse); box.addLayout(row)
        box.addWidget(QtWidgets.QLabel('Existing files will not be replaced.'))
        self.status = task_status.TaskStatus(); self.status.hide(); box.addWidget(self.status)
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        self.submit = buttons.addButton('Export parts', QtWidgets.QDialogButtonBox.AcceptRole)
        self.submit.setEnabled(False)
        self.filename.textChanged.connect(self.update_enabled)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject)
        box.addWidget(buttons)

    def choose_file(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export parts to a new file', '',
                    'FreeCAD Plus component (*.cadprt)', options=QtWidgets.QFileDialog.DontConfirmOverwrite)
        if filename:
            if not Path(filename).suffix:
                filename += '.cadprt'
            self.filename.setText(filename)

    def update_enabled(self, text):
        self.submit.setEnabled(text.lower().endswith('.cadprt'))
        self.status.hide()

    def accept(self):
        try:
            self.guard()
            self.exported_path = part_transfer_ops.export_parts(self.definitions, self.filename.text())
        except (ValueError, OSError, RuntimeError, ReferenceError) as error:
            self.status.setError(str(error)); self.status.show()
            return
        super().accept()
