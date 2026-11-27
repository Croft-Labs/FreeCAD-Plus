# SPDX-License-Identifier: LGPL-2.1-or-later
"""Cancellable read-only file search; explicit verified selection performs recovery."""
from pathlib import Path
import FreeCADGui as Gui
from PySide6 import QtCore
from . import file_recovery
from .file_actions_ui import SearchFoldersForm

_active=None
_retiring=[]


class SearchWorker(QtCore.QThread):
    found=QtCore.Signal(str,bool)
    problem=QtCore.Signal(str)
    def __init__(self,folders,missing,recursive):
        super().__init__();self.folders=folders;self.missing=missing;self.recursive=recursive

    def run(self):
        try:
            for path,verified in file_recovery.search(self.folders,self.missing,self.recursive,
                    self.isInterruptionRequested,lambda path,error:self.problem.emit(path+': '+error)):
                self.found.emit(path,verified)
        except Exception as error:self.problem.emit(str(error))


class SearchTask(QtCore.QObject):
    def __init__(self,missing,use,host=None,guard=lambda:None,close_on_use=False):
        super().__init__()
        self.missing=missing;self.use_callback=use;self.host=host;self.guard=guard
        self.close_on_use=close_on_use;self.closed=False;self.worker=None;self.entries=[];self.errors=[]
        self.form=SearchFoldersForm(missing.path.name,str(missing.path),file_recovery.remembered(host) if host else [])
        self.form.search.clicked.connect(self.search);self.form.stop.clicked.connect(self.stop)
        self.form.use.clicked.connect(self.use);self.form.done.clicked.connect(self.accept);self.form.cancel.clicked.connect(self.reject)

    def getStandardButtons(self):return 0
    def isAllowedAlterDocument(self):return False
    def isAllowedAlterSelection(self):return False
    def isAllowedAlterView(self):return True
    def folders(self):return [self.form.folders.item(i).text() for i in range(self.form.folders.count())]

    def search(self):
        if self.worker is not None:return
        try:self.guard()
        except (ValueError,RuntimeError,ReferenceError) as error:self.form.status.setError(str(error));return
        if not self.folders():self.form.status.setError('Add at least one search folder.');return
        self.entries=[];self.errors=[];self.form.set_results([]);self.form.use.setEnabled(False)
        worker=SearchWorker(self.folders(),self.missing,self.form.recursive.isChecked());self.worker=worker
        self.form.search.setEnabled(False);self.form.stop.setEnabled(True);self.form.status.setText('Searching…')
        worker.found.connect(self.found);worker.problem.connect(self.problem);worker.finished.connect(self.finished)
        worker.start()

    def found(self,path,verified):
        if self.closed:return
        self.entries.append((path,verified));self.form.set_results(self.entries)

    def problem(self,message):
        if not self.closed:self.errors.append(message)

    def finished(self):
        worker=self.worker
        if worker is None:return
        stopped=worker.isInterruptionRequested();self.worker=None;worker.deleteLater()
        if self.closed:return
        self.form.search.setEnabled(True);self.form.stop.setEnabled(False)
        if self.errors:self.form.status.setError('\n'.join(self.errors))
        else:self.form.status.setText(('Stopped. ' if stopped else 'Search complete. ')+str(len(self.entries))+' candidate files found.')

    def stop(self):
        if self.worker:self.worker.requestInterruption()

    def use(self):
        item=self.form.results.currentItem()
        if item is None or not item.data(0,QtCore.Qt.UserRole):return
        try:
            self.guard();filename=item.text(0)
            if not file_recovery.verify(filename,self.missing):raise ValueError('That file changed; search again')
            if self.close_on_use:
                folders=self.folders() if self.form.remember.isChecked() else None
                self.finish();self.use_callback(filename,folders)
            else:
                self.use_callback(filename);self.form.status.setText('File reference updated. Save the file to keep this change.')
        except (ValueError,OSError,RuntimeError,ReferenceError) as error:
            self.form.status.setError(str(error))

    def accept(self):
        try:
            self.guard()
            if self.host is not None and self.form.remember.isChecked():file_recovery.remember(self.host,self.folders())
        except (ValueError,RuntimeError,ReferenceError) as error:self.form.status.setError(str(error));return False
        self.finish();return True

    def reject(self):self.finish();return True

    def finish(self):
        global _active
        if self.closed:return
        self.closed=True
        if self.worker:
            worker=self.worker;self.worker=None;worker.requestInterruption()
            worker.found.disconnect(self.found);worker.problem.disconnect(self.problem);worker.finished.disconnect(self.finished)
            _retiring.append(worker)
            def retired():
                if worker in _retiring:_retiring.remove(worker)
                worker.deleteLater()
            worker.finished.connect(retired)
            if worker.isFinished():retired()
        if _active is self:_active=None
        Gui.Control.closeDialog()


def open_task(missing,use,**kwargs):
    global _active
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first')
    _active=SearchTask(missing,use,**kwargs);Gui.Control.showDialog(_active)
    return _active


def recover_open(filename,replacements=None,folders=None):
    """Resume opening after each explicit Locate/Search decision, never by basename."""
    from . import external,document
    from .file_actions_ui import MissingFileDialog,native_locate
    replacements=dict(replacements or {})
    try:
        external.archive_graph(filename,replacements)
    except external.MissingReference as missing:
        if missing.uid is None:raise
        dialog=MissingFileDialog(str(missing.path),Gui.getMainWindow());choice=[]
        dialog.locate.clicked.connect(lambda:(choice.append('locate'),dialog.accept()))
        dialog.search.clicked.connect(lambda:(choice.append('search'),dialog.accept()))
        try:
            if not dialog.exec():return None
        finally:dialog.deleteLater()
        if choice==['locate']:
            selected=native_locate(Gui.getMainWindow(),str(missing.path))
            if not selected:return None
            if not file_recovery.verify(selected,missing):raise ValueError('Selected file identity or required objects do not match')
            replacements[missing.path]=Path(selected).resolve()
            return recover_open(filename,replacements,folders)
        expected=missing  # Exception variables are cleared after the except block.
        def use(selected,locations):
            replacements[expected.path]=Path(selected).resolve()
            try:recover_open(filename,replacements,locations)
            except (ValueError,OSError,RuntimeError) as error:
                from PySide6 import QtWidgets
                QtWidgets.QMessageBox.warning(Gui.getMainWindow(),'Cannot open file',str(error))
        open_task(expected,use,close_on_use=True)
        return None
    result=file_recovery.open_resolved(filename,replacements)
    if folders is not None:file_recovery.remember(result,folders)
    return result
