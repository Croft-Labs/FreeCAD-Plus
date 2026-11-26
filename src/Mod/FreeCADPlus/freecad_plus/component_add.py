# SPDX-License-Identifier: LGPL-2.1-or-later
"""Add children to the active component within the chosen assembly."""
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from . import assembly, document, editing, external, hierarchy, panel, task_status


def target(*, allow_task=False):
    if (Gui.Control.activeDialog() and not allow_task) or any(Gui.getDocument(d.Name).getInEdit() for d in App.listDocuments().values()):
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


def active_assembly():
    """Resolve the current view's assembly without changing Edit or selection."""
    owner, path = editing.context_path(App.ActiveDocument)
    widget = panel.show_panel() if panel._panel is None else panel._panel
    return widget._assembly_context((App.ActiveDocument, Gui.activeDocument().activeView()), owner, path)[0]


def contains(assembly_owner, component):
    # Children are definition-owned: all repeated occurrences share additions.
    pending = [assembly_owner] if assembly_owner is not None else []
    visited = set()
    while pending:
        part = pending.pop()
        if part == component:
            return True
        ref = panel.identity(part)
        if ref in visited:
            continue
        visited.add(ref)
        pending.extend(link.LinkedObject for link in part.Group
                       if link.TypeId == 'App::Link' and link.LinkedObject is not None)
    return False


class ActiveAssemblyPrompt(QtWidgets.QMessageBox):
    def __init__(self, parent, component_label, assembly_label):
        super().__init__(parent)
        self.setWindowTitle('Add to active component')
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.setTextFormat(QtCore.Qt.PlainText)
        self.setText("The active component '" + component_label +
                     "' is not within the active assembly '" + assembly_label + "'.")
        self.setInformativeText("Make '" + component_label +
                                "' the active assembly and add components to it?")
        self.make_active = self.addButton('Make active assembly and add', QtWidgets.QMessageBox.AcceptRole)
        self.cancel = self.addButton(QtWidgets.QMessageBox.Cancel)
        self.setDefaultButton(self.cancel)
        self.setEscapeButton(self.cancel)


def ensure_destination(parent):
    owner, expected = target()
    current = active_assembly()
    if contains(current, owner):
        return True
    dialog = ActiveAssemblyPrompt(parent, assembly.label(owner, App.ActiveDocument),
                                  assembly.label(current, App.ActiveDocument) if current else 'None')
    try:
        dialog.exec_()
        if dialog.clickedButton() != dialog.make_active:
            return False
        if target()[1] != expected or active_assembly() != current:
            raise ValueError('The active component or assembly changed; reopen Add Component')
        path = tuple(panel.lookup(ref) for ref in expected[4])
        panel._panel.activate_assembly(owner, path or None)
        return True
    finally:
        dialog.deleteLater()


def add_selected(parent, definitions):
    definitions = tuple(definitions)
    if not definitions:
        raise ValueError('Select parts to add to the active component')
    owner, _ = target()
    from . import instance_patterns, instance_task
    instance_patterns.prepare(owner, definitions, None)
    if ensure_destination(parent):
        return instance_task.open_task(definitions)


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


def add_many(expected, definitions):
    owner, current = target()
    if current != expected:
        raise ValueError('The edited component or file tab changed; reopen Add Component')
    instances = hierarchy.add_children(owner, definitions)
    if owner.Document != App.ActiveDocument:
        App.ActiveDocument.recompute()
    if panel._panel is not None:
        panel._panel.refresh()
    return instances


class Picker(QtWidgets.QDialog):
    def __init__(self, parent, new_component=False):
        self.owner, self.expected = target()
        super().__init__(parent)
        self.new_component = new_component
        self.opened = set()
        self.setWindowTitle('Add new component' if new_component else 'Add existing component')
        self.setObjectName('AddComponentPicker')
        self.resize(520, 185 if new_component else 470)
        box = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel('Add to: ' + assembly.label(self.owner, App.ActiveDocument))
        font = title.font(); font.setBold(True); title.setFont(font)
        box.addWidget(title)
        note = QtWidgets.QLabel('Choose a name, then set the instance quantity and arrangement.' if new_component else
                               'Select parts, then set the instance quantity and arrangement.')
        note.setWordWrap(True); box.addWidget(note)
        self.choices = None
        self.name = None
        if new_component:
            form = QtWidgets.QFormLayout()
            from . import naming
            names = naming.reserved(self.owner.Document)
            index = 1
            while naming.key(f'Part{index:03d}') in names:
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
            open_row = QtWidgets.QHBoxLayout()
            open_row.addWidget(QtWidgets.QLabel('Current file and loaded files'))
            open_row.addStretch()
            self.open_file = QtWidgets.QPushButton('Open file…')
            self.open_file.setObjectName('OpenComponentFile')
            self.open_file.clicked.connect(self.open_source)
            open_row.addWidget(self.open_file); box.addLayout(open_row)
            self.choices = QtWidgets.QTreeWidget()
            self.choices.setObjectName('ComponentChoices')
            self.choices.setColumnCount(2)
            self.choices.setHeaderLabels(['Part', 'Components'])
            self.choices.header().setStretchLastSection(False)
            self.choices.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.choices.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            self.choices.setToolTip('Unavailable components explain the reason in their tooltip.')
            box.addWidget(self.choices)
            hint = QtWidgets.QLabel('Parts remain linked to their source file. Assemblies include their children.\nThe active component and its ancestors cannot be added.')
            hint.setWordWrap(True); box.addWidget(hint)
            self.populate()
        self.status = task_status.TaskStatus()
        self.status.hide(); box.addWidget(self.status)
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        self.submit = buttons.addButton('Next', QtWidgets.QDialogButtonBox.AcceptRole)
        box.addWidget(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        if self.name is not None:
            self.name.textChanged.connect(self.update_enabled)
            self.name.selectAll()
        else:
            self.choices.itemChanged.connect(self.update_enabled)
        self.update_enabled()

    def populate(self):
        catalogs = assembly.files(self.owner.Document)
        counts = assembly.counts([part for _, parts in catalogs for part in parts])
        available = set(external.available_definitions(document.validate(self.owner.Document)))
        for doc, parts in catalogs:
            group, file_reason = None, None
            if doc != self.owner.Document:
                group = QtWidgets.QTreeWidgetItem(self.choices, [Path(doc.FileName).name if doc.FileName else doc.Label, ''])
                group.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsAutoTristate)
                group.setCheckState(0, QtCore.Qt.Unchecked)
                group.setIcon(0, Gui.getIcon(':/icons/freecad-plus.svg'))
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
                if not reason:
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item.setCheckState(0, QtCore.Qt.Unchecked)
                if reason:
                    item.setFlags(QtCore.Qt.NoItemFlags)
                    item.setToolTip(0, reason)
                    item.setData(0, QtCore.Qt.AccessibleDescriptionRole, reason)
            if group is not None:
                group.setExpanded(False)
                if not any(group.child(i).flags() & QtCore.Qt.ItemIsEnabled for i in range(group.childCount())):
                    group.setFlags(QtCore.Qt.NoItemFlags)

    def checked_parts(self):
        selected = []
        it = QtWidgets.QTreeWidgetItemIterator(self.choices)
        while it.value():
            item = it.value()
            if (item.flags() & QtCore.Qt.ItemIsEnabled and item.data(0, QtCore.Qt.UserRole)
                    and item.checkState(0) == QtCore.Qt.Checked):
                selected.append(item.data(0, QtCore.Qt.UserRole))
            it += 1
        return selected

    def open_source(self):
        before = set(App.listDocuments())
        try:
            from .file_workflows import choose_source
            filename = choose_source(self, 'Open component file', 'add')
            if not filename:
                return
            if target()[1] != self.expected:
                raise ValueError('The edited component or file tab changed; reopen Add Component')
            external.open_catalog(self.owner.Document, filename)
            self.opened.update(set(App.listDocuments()) - before)
            selected = set(self.checked_parts())
            self.choices.blockSignals(True)
            try:
                self.choices.clear(); self.populate()
                it = QtWidgets.QTreeWidgetItemIterator(self.choices)
                while it.value():
                    item = it.value()
                    if item.data(0, QtCore.Qt.UserRole) in selected and item.flags() & QtCore.Qt.ItemIsEnabled:
                        item.setCheckState(0, QtCore.Qt.Checked)
                    it += 1
            finally:
                self.choices.blockSignals(False)
            self.update_enabled()
        except (ValueError, OSError, RuntimeError, ReferenceError) as error:
            self._close_unused(set(App.listDocuments()) - before)
            self.status.setError(str(error)); self.status.show()

    def _close_unused(self, names=None):
        remaining = set(self.opened if names is None else names)
        while remaining:
            closable = [name for name in remaining if name not in App.listDocuments()
                        or not App.getDocument(name).InList]
            if not closable:
                break
            for name in closable:
                if name in App.listDocuments():
                    App.closeDocument(name)
                remaining.discard(name); self.opened.discard(name)

    def reject(self):
        self._close_unused()
        super().reject()

    def update_enabled(self, *args):
        count = len(self.checked_parts()) if not self.new_component else 0
        self.submit.setEnabled(bool(self.name.text().strip()) if self.new_component else count > 0)
        if not self.new_component:
            self.submit.setText('Next')
        self.status.hide()

    def accept(self):
        try:
            if target()[1] != self.expected:
                raise ValueError('The edited component or file tab changed; reopen Add Component')
            from .instance_patterns import prepare
            self.selected_definitions = [] if self.new_component else [panel.lookup(ref) for ref in self.checked_parts()]
            self.new_label = self.name.text().strip() if self.new_component else None
            prepare(self.owner, self.selected_definitions, self.new_label)
        except (ValueError, OSError, RuntimeError, ReferenceError) as error:
            self.status.setError(str(error)); self.status.show()
            return
        super().accept()


def open_picker(parent, new_component=False, *, selected=(), label=None, opened=(), initial=None):
    try:
        if not ensure_destination(parent):
            return
        dialog = Picker(parent, new_component)
        dialog.opened.update(opened)
        if new_component and label is not None: dialog.name.setText(label)
        if not new_component:
            it = QtWidgets.QTreeWidgetItemIterator(dialog.choices)
            while it.value():
                item = it.value()
                if item.data(0, QtCore.Qt.UserRole) in selected and item.flags() & QtCore.Qt.ItemIsEnabled:
                    item.setCheckState(0, QtCore.Qt.Checked)
                it += 1
    except (ValueError, OSError, RuntimeError, ReferenceError) as error:
        QtWidgets.QMessageBox.warning(parent, 'Add Component', str(error))
        return
    result = dialog.exec_()
    task = None
    if result == QtWidgets.QDialog.Accepted:
        try:
            from .instance_task import open_task
            task = open_task(dialog.selected_definitions, dialog.new_label, dialog.opened, initial=initial)
            dialog.opened.clear()
        except (ValueError, OSError, RuntimeError, ReferenceError) as error:
            dialog._close_unused()
            QtWidgets.QMessageBox.warning(parent, 'Add Component', str(error))
    dialog.deleteLater()
    return task


def make_button(parent, window):
    button = QtWidgets.QToolButton(parent)
    button.setObjectName('Plus_AddComponent')
    button.setProperty('PlusCommands', ['Assembly_Insert'])
    button.setIcon(Gui.getIcon('Assembly_InsertLink'))
    button.setText('Add Component')
    button.setAccessibleName('Add Component')
    button.setToolTip('Add an existing or new component as a child of the active component')
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
