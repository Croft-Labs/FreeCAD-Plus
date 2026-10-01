# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit operand capture and view-only native Section preview."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.OccurrenceMove import Ghost
import SectionReview as Review

tr = Review.tr
_dialogs = []


class SectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.doc = App.ActiveDocument
        self.inputs = [None, None]
        self.previewed = self.ghost = self.result = None
        self.closed = self.busy = False
        self.setWindowTitle(tr("Review intersection curves"))
        self.resize(640, 380)
        layout = QtWidgets.QVBoxLayout(self)
        note = QtWidgets.QLabel(tr(
            "Find the common boundary curves of two shapes using native Section. "
            "This intersects their surfaces; it does not project curves or cut material. "
            "Choose whole root Part shapes or whole root Bodies (up to 200 faces each)."))
        note.setWordWrap(True)
        layout.addWidget(note)
        form = QtWidgets.QFormLayout()
        self.labels, self.captureButtons = [], []
        for index, text in enumerate(("Capture first shape", "Capture second shape")):
            button = QtWidgets.QPushButton(tr(text))
            label = QtWidgets.QLabel(tr("Not captured"))
            label.setWordWrap(True)
            label.setTextFormat(QtCore.Qt.PlainText)
            button.clicked.connect(lambda _checked=False, i=index: self.capture(i))
            self.labels.append(label)
            self.captureButtons.append(button)
            form.addRow(button, label)
        layout.addLayout(form)
        self.approximation = QtWidgets.QCheckBox(tr("Approximate output curves (native Section option)"))
        self.approximation.toggled.connect(self.invalidate)
        layout.addWidget(self.approximation)
        self.message = QtWidgets.QLabel(tr("Capture both shapes, then preview."))
        self.message.setWordWrap(True)
        self.message.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.message)
        note = QtWidgets.QLabel(tr(
            "The colored preview adds no document geometry. Create saves an associative Section with "
            "Base and Tool links; source shapes and visibility are preserved. Coincident surfaces "
            "can produce boundary edges rather than a unique intersection curve."))
        note.setWordWrap(True)
        layout.addWidget(note)
        buttons = QtWidgets.QHBoxLayout()
        self.previewButton = QtWidgets.QPushButton(tr("Preview curves"))
        self.createButton = QtWidgets.QPushButton(tr("Create intersection"))
        self.cancelButton = QtWidgets.QPushButton(tr("Cancel"))
        for button in (self.previewButton, self.createButton, self.cancelButton):
            button.setAutoDefault(False)
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.previewButton.clicked.connect(self.preview)
        self.createButton.clicked.connect(self.commit)
        self.cancelButton.clicked.connect(self.reject)
        self.createButton.setEnabled(False)
        selection = Gui.Selection.getSelectionEx("*", 0)
        if len(selection) == 2:
            for index, entry in enumerate(selection):
                self.set_input(index, entry)
        App.addDocumentObserver(self)

    def invalidate(self, *args):
        if self.ghost is not None:
            self.ghost.remove()
            self.ghost = None
        self.previewed = None
        self.createButton.setEnabled(False)
        self.message.setText(tr("No current preview. Capture changed inputs again, then preview."))

    def set_input(self, index, entry):
        self.inputs[index] = None
        self.labels[index].setText(tr("Not captured"))
        try:
            if entry.Object.Document != self.doc or entry.SubElementNames:
                raise ValueError(tr("Select one whole shape in this document, using the tree."))
            ref = Review.Input(entry.Object)
            self.inputs[index] = ref
            self.labels[index].setText(ref.label)
        except Exception as error:
            self.message.setText(str(error))

    def capture(self, index):
        self.invalidate()
        self.inputs[index] = None
        self.labels[index].setText(tr("Not captured"))
        selected = Gui.Selection.getSelectionEx("*", 0)
        if len(selected) != 1:
            self.message.setText(tr("Select one whole shape in this document, using the tree."))
            return
        self.set_input(index, selected[0])

    def preview(self):
        self.invalidate()
        self.busy = True
        try:
            if any(ref is None for ref in self.inputs):
                raise ValueError(tr("Capture both shapes before previewing."))
            result = Review.probe(*self.inputs, self.approximation.isChecked())
            if result["edges"]:
                self.ghost = Ghost(result["shape"])
                self.previewed = result
                self.createButton.setEnabled(True)
                self.message.setText(tr("Preview: {edges} edges; total length {length:.9g} mm. Sources unchanged.").format(**result))
            else:
                self.message.setText(tr("No intersection curves: {vertices} isolated vertices. The shapes may be disjoint, contained, or only touch at points. No feature will be created.").format(**result))
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.busy = False

    def commit(self):
        self.busy = True
        try:
            self.result = Review.create(self.previewed)
            self.accept()
        except Exception as error:
            self.invalidate()
            self.message.setText(str(error))
        finally:
            self.busy = False

    def slotChangedObject(self, obj, prop):
        if obj.Document == self.doc and not self.busy and not self.closed:
            self.invalidate()

    def slotDeletedObject(self, obj):
        if obj.Document == self.doc and not self.closed:
            self.invalidate()

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def slotActivateDocument(self, doc):
        if doc != self.doc and not self.busy and not self.closed:
            self.invalidate()

    def done(self, result):
        if not self.closed:
            self.closed = True
            self.invalidate()
            App.removeDocumentObserver(self)
        super().done(result)


class Command:
    def GetResources(self):
        return {"MenuText": tr("Review intersection curves..."),
                "ToolTip": tr("Preview and create associative Section curves from two explicit shapes"),
                "Pixmap": "Part_Section"}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        dialog = SectionDialog(Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _r: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Part_SectionReview", Command())
