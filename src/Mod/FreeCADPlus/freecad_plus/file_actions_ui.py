# SPDX-License-Identifier: LGPL-2.1-or-later
"""Parts file menus and approved native file/search controls."""
from pathlib import Path
from PySide6 import QtCore, QtWidgets


def subfile_menu(panel, tree, point, row):
    from .panel import lookup
    source=lookup(row.ref).Document
    binding=panel._binding
    menu=QtWidgets.QMenu(panel);actions={};missing=not Path(source.FileName).is_file()
    action=menu.addAction('Open file in new window');action.setEnabled(not missing);actions[action]='open'
    menu.addSeparator()
    actions[menu.addAction('Create new part file\u2026')]='create'
    action=menu.addAction('Import models to file\u2026');action.setEnabled(not missing);actions[action]='copy'
    menu.addSeparator()
    if missing:actions[menu.addAction('Locate file\u2026')]='locate'
    actions[menu.addAction('Search folders\u2026')]='search'
    chosen=menu.exec_(tree.viewport().mapToGlobal(point))
    if chosen in actions:
        try:
            if panel._current()!=binding:raise ValueError('The active file changed; reopen the menu')
            run_action(panel,actions[chosen],row)
        except (ValueError,OSError,RuntimeError,ReferenceError) as error:panel._message(str(error))
    menu.deleteLater()


def native_save(parent):
    return QtWidgets.QFileDialog.getSaveFileName(parent,'Create new part file','','FreeCAD Plus document (*.cadprt)')[0]


def native_locate(parent, expected):
    return QtWidgets.QFileDialog.getOpenFileName(parent,'Locate missing file',expected,'FreeCAD Plus document (*.cadprt)')[0]


class SearchFoldersForm(QtWidgets.QWidget):
    def __init__(self, filename, expected, folders, choose_folder=None):
        super().__init__();self.setWindowTitle('Search folders');self.setMinimumWidth(340)
        self.choose_folder=choose_folder or (lambda:QtWidgets.QFileDialog.getExistingDirectory(self,'Add search folder'))
        box=QtWidgets.QVBoxLayout(self);box.setSpacing(10)
        top=QtWidgets.QHBoxLayout();self.done=QtWidgets.QPushButton('Done');self.cancel=QtWidgets.QPushButton('Cancel')
        top.addWidget(self.done);top.addWidget(self.cancel);box.addLayout(top)
        name=QtWidgets.QLabel(filename);font=name.font();font.setBold(True);name.setFont(font);box.addWidget(name)
        # Allow a long native path to wrap at directory/name boundaries.
        wrapped=expected
        for separator in ('\\','/','_','.'):
            wrapped=wrapped.replace(separator,separator+'\u200b')
        label=QtWidgets.QLabel('Expected: '+wrapped);label.setWordWrap(True)
        label.setTextFormat(QtCore.Qt.PlainText);label.setToolTip(expected)
        self.expected_label=label;box.addWidget(label)
        box.addWidget(QtWidgets.QLabel('Search locations'))
        self.folders=QtWidgets.QListWidget();self.folders.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.folders.setMinimumHeight(110);self.folders.setMaximumHeight(135);self.folders.addItems(folders);box.addWidget(self.folders)
        row=QtWidgets.QHBoxLayout();self.add=QtWidgets.QPushButton('Add folder\u2026');self.remove=QtWidgets.QPushButton('Remove');self.clear=QtWidgets.QPushButton('Clear')
        for b in (self.add,self.remove,self.clear):row.addWidget(b)
        box.addLayout(row)
        self.recursive=QtWidgets.QCheckBox('Include subfolders');self.recursive.setChecked(True);box.addWidget(self.recursive)
        self.remember=QtWidgets.QCheckBox('Remember these locations for this file');self.remember.setChecked(True);box.addWidget(self.remember)
        row=QtWidgets.QHBoxLayout();self.search=QtWidgets.QPushButton('Search');self.stop=QtWidgets.QPushButton('Stop');self.stop.setEnabled(False)
        row.addWidget(self.search);row.addWidget(self.stop);box.addLayout(row)
        from .task_status import TaskStatus
        self.status=TaskStatus('Ready to search.');box.addWidget(self.status)
        box.addWidget(QtWidgets.QLabel('Results'))
        self.results=QtWidgets.QTreeWidget();self.results.setHeaderLabels(['File','Status'])
        self.results.setRootIsDecorated(False);self.results.setMinimumHeight(125);self.results.setMaximumHeight(155)
        self.results.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.results.header().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents);box.addWidget(self.results)
        self.use=QtWidgets.QPushButton('Use selected file');self.use.setEnabled(False);box.addWidget(self.use)
        note=QtWidgets.QLabel('Select a verified match to restore the file reference. Search does not change links.');note.setWordWrap(True);box.addWidget(note)
        box.addStretch()
        self.add.clicked.connect(self.add_folder);self.remove.clicked.connect(self.remove_folders);self.clear.clicked.connect(self.folders.clear)
        self.results.itemSelectionChanged.connect(self.update_use)

    def add_folder(self):
        path=self.choose_folder()
        if path and str(Path(path).resolve()).casefold() not in [self.folders.item(i).text().casefold() for i in range(self.folders.count())]:
            self.folders.addItem(str(Path(path).resolve()))

    def resizeEvent(self,event):
        super().resizeEvent(event)
        width=max(100,self.width()-self.layout().contentsMargins().left()-self.layout().contentsMargins().right())
        self.expected_label.setMinimumHeight(max(1,self.expected_label.heightForWidth(width)))

    def remove_folders(self):
        for item in self.folders.selectedItems():self.folders.takeItem(self.folders.row(item))

    def set_results(self, entries):
        self.results.clear()
        for path,verified in entries:
            item=QtWidgets.QTreeWidgetItem(self.results,[path,'Verified match' if verified else 'Different file'])
            item.setToolTip(0,path);item.setData(0,QtCore.Qt.UserRole,verified)
        self.status.setText(str(len(entries))+' candidate files found.')

    def update_use(self):
        item=self.results.currentItem();self.use.setEnabled(bool(item and item.data(0,QtCore.Qt.UserRole)))


class DependenciesDialog(QtWidgets.QDialog):
    def __init__(self, source, destination, dependencies, parent=None):
        super().__init__(parent);self.setWindowTitle('Copy parts with dependencies');self.setMinimumWidth(430)
        box=QtWidgets.QVBoxLayout(self);box.setSpacing(12)
        for text in ('Import models from: '+source,'Copy into: '+destination,'These parts depend on other files:'):
            label=QtWidgets.QLabel(text);label.setWordWrap(True);box.addWidget(label)
        items=QtWidgets.QListWidget();items.addItems(dependencies);items.setMaximumHeight(100);box.addWidget(items)
        self.copy=QtWidgets.QRadioButton('Copy dependent parts');self.copy.setChecked(True);box.addWidget(self.copy)
        note=QtWidgets.QLabel('Bring all required parts into this file, preserving history. Shared dependencies are copied once.');note.setWordWrap(True);box.addWidget(note)
        self.bake=QtWidgets.QRadioButton('Convert to dumb geometry');box.addWidget(self.bake)
        note=QtWidgets.QLabel('Copy final shapes and meshes only, including child geometry. Remove feature history and file links.');note.setWordWrap(True);box.addWidget(note)
        note=QtWidgets.QLabel('Original files stay unchanged.');box.addWidget(note)
        self.buttons=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        self.submit=self.buttons.addButton('Copy parts',QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttons.accepted.connect(self.accept);self.buttons.rejected.connect(self.reject);box.addWidget(self.buttons)


class MissingFileDialog(QtWidgets.QDialog):
    def __init__(self, expected,parent=None):
        super().__init__(parent);self.setWindowTitle('Missing referenced file');self.setMinimumWidth(430)
        box=QtWidgets.QVBoxLayout(self)
        for text in ('This assembly needs a file that could not be found:',expected,'Locate it or search your folders to continue opening the assembly.'):
            label=QtWidgets.QLabel(text);label.setWordWrap(True);box.addWidget(label)
        row=QtWidgets.QHBoxLayout();self.locate=QtWidgets.QPushButton('Locate file\u2026');self.search=QtWidgets.QPushButton('Search folders\u2026');self.cancel=QtWidgets.QPushButton('Cancel')
        for b in (self.locate,self.search,self.cancel):row.addWidget(b)
        self.cancel.clicked.connect(self.reject);box.addLayout(row)


def host_context(panel):
    import FreeCADGui as Gui
    panel._clipboard_guard()
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first')
    binding=panel._current()
    if binding is None or binding!=panel._binding:raise ValueError('Select the active file again')
    return binding[0]


def run_action(panel, action, row=None):
    import FreeCAD as App
    import FreeCADGui as Gui
    from . import document, file_actions, file_recovery, external
    from .panel import lookup
    host=host_context(panel);binding=panel._binding
    source=lookup(row.ref).Document if row is not None and row.kind=='import' else None
    def guard():
        if panel._current()!=binding:raise ValueError('The active file changed; reopen the menu')
        if source is not None and lookup(row.ref).Document!=source:raise ValueError('The source changed')
    if action=='create':
        filename=native_save(panel)
        if not filename:return
        if not Path(filename).suffix:filename+='.cadprt'
        guard();file_actions.create_linked_file(host,filename);panel.refresh()
    elif action=='open':
        if not Path(source.FileName).is_file():raise ValueError('Locate the missing file first')
        guard();App.setActiveDocument(source.Name)
        Gui.getDocument(source.Name).createView('Gui::View3DInventor')
        from . import editing
        editing.edit_file(source);panel.refresh()
    elif action=='copy':
        if not Path(source.FileName).is_file():raise ValueError('Locate the missing file first')
        parts=tuple(document.validate(source).Definitions);dependencies=file_actions.dependencies(parts)
        bake=False
        if dependencies:
            dialog=DependenciesDialog(source.Label,host.Label,dependencies,panel)
            try:
                if not dialog.exec():return
                bake=dialog.bake.isChecked()
            finally:dialog.deleteLater()
        guard();file_actions.copy_parts(host,parts,bake=bake);panel.refresh()
    elif action in ('locate','search'):
        missing=external.MissingReference(source.FileName,str(source.Uid),[obj.Name for obj in source.Objects])
        def use(filename):
            guard();file_recovery.relocate_loaded(source,filename);panel.refresh()
        if action=='locate':
            filename=native_locate(panel,source.FileName)
            if filename:use(filename)
        else:
            from .file_search_task import open_task
            open_task(missing,use,host=host,guard=guard)
