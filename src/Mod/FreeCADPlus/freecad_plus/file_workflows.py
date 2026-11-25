# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit Classic-to-Plus conversion, shared by Open and component import."""
from pathlib import Path
from contextlib import contextmanager
import hashlib
import os
import uuid
import xml.etree.ElementTree as ET
import zipfile

import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from . import document, conversion, task_status

PLUS_FILTER = 'FreeCAD Plus document (*.cadprt)'
CLASSIC_FILTER = 'FreeCAD Classic document (*.FCStd)'
NATIVE_FILTER = 'FreeCAD documents (*.cadprt *.FCStd)'
SOURCE_FILTERS = NATIVE_FILTER + ';;' + PLUS_FILTER + ';;' + CLASSIC_FILTER


@contextmanager
def _cursor(shape):
    """Balance our override without discarding a caller's native busy cursor."""
    QtWidgets.QApplication.setOverrideCursor(shape)
    try:
        yield
    finally:
        QtWidgets.QApplication.restoreOverrideCursor()


def archive_kind(filename):
    """Determine format from metadata before opening or mutating documents."""
    path = Path(filename)
    if path.suffix.lower() not in ('.cadprt', '.fcstd'):
        raise ValueError('Choose a .cadprt or .FCStd document')
    try:
        with zipfile.ZipFile(path) as archive:
            tree = ET.fromstring(archive.read('Document.xml'))
        if tree.find('./Objects') is None:
            raise ValueError('The file is not a native FreeCAD document')
        markers = tree.findall("./ObjectData/Object/Properties/Property[@name='PlusFormat']/String")
        if markers:
            if len(markers) != 1 or markers[0].get('value') != 'FreeCADPlus.ComponentDocument':
                raise ValueError('Unrecognized FreeCAD Plus document format')
            return 'plus'
        return 'classic'
    except (OSError, zipfile.BadZipFile, ET.ParseError, KeyError) as error:
        raise ValueError('Cannot read document: ' + str(error)) from error


def repair_copy(source, destination):
    """Save mislabelled Plus data to a new cadprt; retain source and live edits."""
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if source.suffix.lower() != '.fcstd' or archive_kind(source) != 'plus':
        raise ValueError('Expected FreeCAD Plus data in a .FCStd file')
    if destination.suffix.lower() != '.cadprt':
        raise ValueError('Choose a .cadprt destination')
    if destination.exists():
        raise FileExistsError('The destination already exists. Choose a new filename.')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    previous = App.ActiveDocument
    before = set(App.listDocuments())
    repaired = App.newDocument('CorrectedComponentFile')
    try:
        repaired.FileName = str(source)
        repaired.restore()
        repaired.FileName = ''
        repaired.Uid = str(uuid.uuid4())
        document.validate(repaired)
        if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
            raise ValueError('The source changed during repair; retry from its current version')
        # Same directory preserves relative external links when the staged file is published.
        staging = destination.parent / ('.cadprt-repair-' + uuid.uuid4().hex + '.cadprt')
        try:
            saved = document.save_document(repaired, staging, label=destination.stem)
            os.link(saved, destination)
        finally:
            staging.unlink(missing_ok=True)
        repaired.FileName = str(destination)
        Gui.getDocument(repaired.Name).Modified = False
        return repaired
    except Exception:
        for name in set(App.listDocuments()) - before:
            App.closeDocument(name)
        if previous and previous.Name in App.listDocuments():
            App.setActiveDocument(previous.Name)
        raise


class ConversionDialog(QtWidgets.QDialog):
    def __init__(self, parent, source, purpose='open', repair=False):
        super().__init__(parent)
        self.source = str(Path(source).resolve())
        self.repair = repair
        self.choice = None
        self.result_path = None
        self.setWindowTitle('Correct FreeCAD Plus file extension' if repair else 'Open FreeCAD Classic file')
        self.setObjectName('ComponentFileConversion')
        self.resize(580, 285)
        box = QtWidgets.QVBoxLayout(self)
        heading = QtWidgets.QLabel('This file contains FreeCAD Plus data.' if repair else
                                  'This is a FreeCAD Classic document (.FCStd).')
        font = heading.font(); font.setBold(True); heading.setFont(font); box.addWidget(heading)
        form = QtWidgets.QFormLayout()
        label = QtWidgets.QLabel(self.source); label.setWordWrap(True); form.addRow('Source', label)
        self.destination = QtWidgets.QLineEdit(str(Path(source).with_suffix('.cadprt')))
        row = QtWidgets.QHBoxLayout(); row.addWidget(self.destination, 1)
        browse = QtWidgets.QPushButton('Browse…'); browse.clicked.connect(self.browse)
        row.addWidget(browse); form.addRow('New Plus file', row); box.addLayout(form)
        note = QtWidgets.QLabel('Save a corrected .cadprt copy to use this as a FreeCAD Plus document.' if repair else
            'Convert a copy to .cadprt to use its parts in FreeCAD Plus.\nEditable features are preserved where supported.')
        note.setWordWrap(True); box.addWidget(note)
        box.addWidget(QtWidgets.QLabel('The original .FCStd file stays unchanged.'))
        if any(d.FileName and Path(d.FileName).resolve() == Path(self.source)
               and Gui.getDocument(d.Name).Modified for d in App.listDocuments().values()):
            saved = QtWidgets.QLabel('Conversion uses the saved file; unsaved source edits are not included.')
            saved.setWordWrap(True); box.addWidget(saved)
        self.status = task_status.TaskStatus(); self.status.hide(); box.addWidget(self.status)
        box.addStretch()
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        self.primary = buttons.addButton('Save .cadprt copy' if repair else
            {'open': 'Convert and open', 'import': 'Convert and import', 'add': 'Convert and select parts'}[purpose],
            QtWidgets.QDialogButtonBox.AcceptRole)
        self.primary.setDefault(True)
        if purpose == 'open' and not repair:
            classic = buttons.addButton('Open Classic', QtWidgets.QDialogButtonBox.ActionRole)
            classic.clicked.connect(self.open_classic)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject); box.addWidget(buttons)

    def exec(self):
        # Native Open/Import hold a WaitCursor while dispatching to this dialog.
        # Waiting for a choice is idle; retain that caller's cursor underneath.
        with _cursor(QtCore.Qt.ArrowCursor):
            return super().exec()

    def browse(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save FreeCAD Plus document',
            self.destination.text(), PLUS_FILTER, options=QtWidgets.QFileDialog.DontConfirmOverwrite)
        if filename:
            self.destination.setText(filename if Path(filename).suffix else filename + '.cadprt')

    def open_classic(self):
        self.choice = 'classic'
        super().accept()

    def accept(self):
        with _cursor(QtCore.Qt.WaitCursor):
            self._convert()

    def _convert(self):
        previous = App.ActiveDocument
        before = set(App.listDocuments())
        created = None
        try:
            if (Gui.Control.activeDialog() or any(d.HasPendingTransaction for d in App.listDocuments().values())
                    or any(Gui.getDocument(d.Name).getInEdit() for d in App.listDocuments().values())):
                raise ValueError('Finish the current operation before converting a file')
            path = Path(self.destination.text()).resolve()
            if path.suffix.lower() != '.cadprt':
                raise ValueError('Choose a new .cadprt filename')
            created = repair_copy(self.source, path) if self.repair else conversion.convert_file(self.source, path)[0]
            self.result_path = str(path)
            self.choice = 'plus'
        except (ValueError, OSError, RuntimeError) as error:
            self.status.setError(str(error)); self.status.show()
            return
        finally:
            # Source choosers must not replace Edit/assembly context or leak a new view.
            remaining = set(App.listDocuments()) - before
            while remaining:
                closable = [name for name in remaining if not App.getDocument(name).InList]
                if not closable:
                    break
                for name in closable:
                    App.closeDocument(name); remaining.remove(name)
            if previous and previous.Name in App.listDocuments():
                App.setActiveDocument(previous.Name)
        super().accept()


def prepare_source(filename, parent=None, purpose='import'):
    """Return a Plus path, the explicit Classic choice, or None on Cancel."""
    path = Path(filename).resolve()
    kind = archive_kind(path)
    if path.suffix.lower() == '.cadprt':
        if kind != 'plus':
            raise ValueError('This .cadprt contains Classic data. Restore its .FCStd extension before converting it.')
        document.inspect_archive(path)
        return str(path)
    dialog = ConversionDialog(parent or Gui.getMainWindow(), path, purpose, repair=kind == 'plus')
    try:
        if not dialog.exec():
            return None
        return str(path) if dialog.choice == 'classic' else dialog.result_path
    finally:
        dialog.deleteLater()


def choose_source(parent, title, purpose):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent, title, '', SOURCE_FILTERS)
    try:
        return prepare_source(filename, parent, purpose) if filename else None
    except (ValueError, OSError, RuntimeError) as error:
        prefix = 'Cannot import component file: ' if purpose == 'import' else 'Cannot open component file: '
        raise ValueError(prefix + str(error)) from error


def open_file(filename):
    path = prepare_source(filename, purpose='open')
    if not path:
        return None
    if Path(path).suffix.lower() == '.cadprt':
        result = document.open_document(path)
        App.setActiveDocument(result.Name)
        return result
    for existing in App.listDocuments().values():
        if existing.FileName and Path(existing.FileName).resolve() == Path(path):
            Gui.reload(existing.Name)
            return existing
    return App.openDocument(path)
