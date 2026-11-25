# SPDX-License-Identifier: LGPL-2.1-or-later
"""Add a child to Edit's component, independently of assembly navigation."""
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from . import assembly, document, editing, external, hierarchy, panel, task_status


def target():
    if Gui.Control.activeDialog() or any(Gui.getDocument(d.Name).getInEdit() for d in App.listDocuments().values()):
        raise ValueError('Finish the current task before adding a component')
    if App.getActiveTransaction() or any(d.HasPendingTransaction for d in App.listDocuments().values()):
        raise ValueError('Finish the current operation before adding a component')
    doc = App.ActiveDocument
    if doc is None or not any('PlusFormat' in o.PropertiesList for o in doc.Objects):
        raise ValueError('Open a component file and Edit the intended parent component')
    owner, path = editing.context_path(doc)
    token = (doc.Name, str(doc.Uid), Gui.activeDocument().activeView(), panel.identity(owner),
             tuple(panel.identity(o) for o in path))
    return owner, token


def add(expected, definition=None, *, label=None):
    owner, current = target()
    if current != expected:
        raise ValueError('The edited component or file tab changed; reopen Add Component')
    instance = hierarchy.add_child(owner, definition, label=label)
    if owner.Document != App.ActiveDocument:
        App.ActiveDocument.recompute()
    if panel._panel is not None:
        panel._panel.refresh()
    return instance


class Picker(QtWidgets.QDialog):
    def __init__(self, parent, new_component=False):
        self.owner, self.expected = target()
        super().__init__(parent)
        self.new_component = new_component
        self.setWindowTitle('Add new component' if new_component else 'Add existing component')
        self.setObjectName('AddComponentPicker')
        self.resize(460, 185 if new_component else 420)
        box = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel('Add to: ' + assembly.label(self.owner, App.ActiveDocument))
        font = title.font(); font.setBold(True); title.setFont(font)
        box.addWidget(title)
        box.addWidget(QtWidgets.QLabel('Add one child component at the parent origin.'))
        self.choices = None
        self.name = None
        if new_component:
            form = QtWidgets.QFormLayout()
            names = {p.Label for p in document.validate(self.owner.Document).Definitions}
            index = 1
            while f'Part{index:03d}' in names:
                index += 1
            self.name = QtWidgets.QLineEdit(f'Part{index:03d}')
            self.name.setObjectName('NewComponentName')
            form.addRow('Name', self.name)
            location = QtWidgets.QLabel(Path(self.owner.Document.FileName).name or self.owner.Document.Label)
            location.setWordWrap(True); form.addRow('Create in', location)
            note = QtWidgets.QLabel('Creates a new component and adds it as a child of ' + self.owner.Label + '.')
            note.setWordWrap(True); form.addRow(note)
            box.addLayout(form)
        else:
            self.choices = QtWidgets.QTreeWidget()
            self.choices.setObjectName('ComponentChoices')
            self.choices.setColumnCount(2)
            self.choices.setHeaderLabels(['Part', 'Components'])
            self.choices.header().setStretchLastSection(False)
            self.choices.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.choices.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            self.choices.setToolTip('Unavailable components explain the reason in their tooltip.')
            box.addWidget(self.choices)
            hint = QtWidgets.QLabel('The active component and its ancestors cannot be added.')
            hint.setWordWrap(True); box.addWidget(hint)
            self.populate()
        self.status = task_status.TaskStatus()
        self.status.hide(); box.addWidget(self.status)
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        self.submit = buttons.addButton('Create and add' if new_component else 'Add component',
                                        QtWidgets.QDialogButtonBox.AcceptRole)
        box.addWidget(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        if self.name is not None:
            self.name.textChanged.connect(self.update_enabled)
            self.name.selectAll()
        else:
            self.choices.currentItemChanged.connect(self.update_enabled)
        self.update_enabled()

    def populate(self):
        catalogs = assembly.files(self.owner.Document)
        counts = assembly.counts([part for _, parts in catalogs for part in parts])
        available = set(external.available_definitions(document.validate(self.owner.Document)))
        for doc, parts in catalogs:
            group, file_reason = None, None
            if doc != self.owner.Document:
                group = QtWidgets.QTreeWidgetItem(self.choices, [Path(doc.FileName).name if doc.FileName else doc.Label, ''])
                group.setFlags(QtCore.Qt.ItemIsEnabled)
                group.setIcon(0, Gui.getIcon(':/icons/freecad.svg'))
                if any(p not in available for p in parts):
                    try:
                        external.prepare_import(self.owner.Document, doc)
                    except (ValueError, OSError, RuntimeError, ReferenceError) as error:
                        file_reason = str(error)
            for part in parts:
                item = QtWidgets.QTreeWidgetItem(group if group is not None else self.choices,
                                                [part.Label, str(counts[part])])
                item.setIcon(0, part.ViewObject.Icon)
                item.setTextAlignment(1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                item.setData(0, QtCore.Qt.UserRole, panel.identity(part))
                reason = file_reason if part not in available else None
                try:
                    hierarchy.check_nesting(self.owner, part)
                except ValueError:
                    reason = ('A component cannot be its own child.' if part == self.owner else
                              part.Label + ' contains ' + self.owner.Label + '. Adding it would create a cycle.')
                if reason:
                    item.setFlags(QtCore.Qt.NoItemFlags)
                    item.setToolTip(0, reason)
                    item.setData(0, QtCore.Qt.AccessibleDescriptionRole, reason)
            if group is not None:
                group.setExpanded(False)

    def update_enabled(self, *args):
        item = self.choices.currentItem() if self.choices is not None else None
        enabled = (bool(self.name.text().strip()) if self.new_component else
                   bool(item and item.flags() & QtCore.Qt.ItemIsEnabled and item.data(0, QtCore.Qt.UserRole)))
        self.submit.setEnabled(enabled)
        self.status.hide()

    def accept(self):
        try:
            if self.new_component:
                add(self.expected, label=self.name.text().strip())
            else:
                item = self.choices.currentItem()
                if not item or not item.flags() & QtCore.Qt.ItemIsEnabled or not item.data(0, QtCore.Qt.UserRole):
                    raise ValueError('Choose an available component to add')
                add(self.expected, panel.lookup(item.data(0, QtCore.Qt.UserRole)))
        except (ValueError, OSError, RuntimeError, ReferenceError) as error:
            self.status.setError(str(error)); self.status.show()
            return
        super().accept()


def open_picker(parent, new_component=False):
    try:
        dialog = Picker(parent, new_component)
    except (ValueError, OSError, RuntimeError, ReferenceError) as error:
        QtWidgets.QMessageBox.warning(parent, 'Add Component', str(error))
        return
    dialog.exec_()
    dialog.deleteLater()


def make_button(parent, window):
    button = QtWidgets.QToolButton(parent)
    button.setObjectName('Plus_AddComponent')
    button.setProperty('PlusCommands', ['Assembly_Insert'])
    button.setIcon(Gui.getIcon('Assembly_InsertLink'))
    button.setText('Add Component')
    button.setAccessibleName('Add Component')
    button.setToolTip('Add an existing or new component as a child of the component being edited')
    menu = QtWidgets.QMenu(button)
    existing = menu.addAction(Gui.getIcon('Assembly_InsertLink'), 'Add existing')
    create = menu.addAction(Gui.Command.get('Std_Part').getAction()[0].icon(), 'Add new')
    existing.triggered.connect(lambda: open_picker(window, False))
    create.triggered.connect(lambda: open_picker(window, True))
    def update():
        reason = ''
        try:
            target()
        except (ValueError, RuntimeError, ReferenceError) as error:
            reason = str(error)
        for action in (existing, create):
            action.setEnabled(not reason)
            action.setToolTip(reason)
        menu.setToolTipsVisible(True)
    menu.aboutToShow.connect(update)
    button.setMenu(menu)
    button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
    return button
