# SPDX-License-Identifier: LGPL-2.1-or-later
"""Review and place an independent constrained sketch copy."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve
from freecad.gui.OccurrenceMove import Ghost
import SketchReuse as Reuse

tr = Reuse.tr
_dialogs = []


class CopyDialog(QtWidgets.QDialog):
    def __init__(self, sketch, parent=None):
        super().__init__(parent)
        self.key, self.doc = identity(sketch), sketch.Document
        self.expected = self.ghost = None
        self.closed = self.saving = False
        self.setWindowTitle(tr("Copy reusable sketch"))
        self.resize(670, 410)
        layout = QtWidgets.QVBoxLayout(self)
        self.summary = QtWidgets.QLabel()
        self.summary.setWordWrap(True)
        self.summary.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.summary)
        form = QtWidgets.QFormLayout()
        self.name = QtWidgets.QLineEdit(sketch.Label + tr(" (copy)"))
        form.addRow(tr("New sketch name"), self.name)
        self.offset = []
        for axis in "XYZ":
            field = QtWidgets.QDoubleSpinBox()
            field.setRange(-1e6, 1e6)
            field.setDecimals(4)
            field.setSuffix(" mm")
            field.valueChanged.connect(self.clearPreview)
            self.offset.append(field)
            form.addRow(tr("Offset in source sketch axes") + " " + axis, field)
        self.angle = QtWidgets.QDoubleSpinBox()
        self.angle.setRange(-360, 360)
        self.angle.setDecimals(4)
        self.angle.setSuffix(" deg")
        self.angle.valueChanged.connect(self.clearPreview)
        form.addRow(tr("Rotation about source normal"), self.angle)
        layout.addLayout(form)
        note = QtWidgets.QLabel(tr("Copies the whole sketch with its internal constraints and construction geometry. "
                                  "Rotate about the source sketch origin, then offset in its X/Y/Z axes. "
                                  "The result is independent and remains editable. External references and expressions are refused."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.message = QtWidgets.QLabel()
        self.message.setWordWrap(True)
        self.message.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.message)
        buttons = QtWidgets.QHBoxLayout()
        refresh = QtWidgets.QPushButton(tr("Review again"))
        refresh.clicked.connect(self.review)
        self.previewButton = QtWidgets.QPushButton(tr("Preview"))
        self.previewButton.clicked.connect(self.preview)
        self.copyButton = QtWidgets.QPushButton(tr("Create independent copy"))
        self.copyButton.clicked.connect(self.createCopy)
        cancel = QtWidgets.QPushButton(tr("Cancel"))
        cancel.clicked.connect(self.reject)
        for button in (refresh, self.previewButton, self.copyButton, cancel):
            buttons.addWidget(button)
        layout.addLayout(buttons)
        App.addDocumentObserver(self)
        self.review()

    def clearPreview(self, *args):
        if self.ghost is not None:
            self.ghost.remove()
            self.ghost = None
        self.message.clear()

    def review(self):
        self.clearPreview()
        self.expected = None
        self.previewButton.setEnabled(False)
        self.copyButton.setEnabled(False)
        try:
            sketch = resolve(self.key)
            self.expected = Reuse.review(sketch)
            self.summary.setText(sketch.Label + " [" + sketch.Name + "] — " +
                                 tr("Geometry: {0}; constraints: {1}; degrees of freedom: {2}").format(
                                     self.expected["geometry"], self.expected["constraints"], self.expected["dof"]))
            self.previewButton.setEnabled(True)
            self.copyButton.setEnabled(True)
        except Exception as error:
            self.message.setText(str(error))

    def values(self):
        return tuple(field.value() for field in self.offset), self.angle.value()

    def preview(self):
        self.clearPreview()
        try:
            if App.ActiveDocument != self.doc or Gui.Control.activeDialog():
                raise ValueError(tr("Activate this document and finish the current task before previewing."))
            placement, shape = Reuse.candidate(resolve(self.key), self.expected, *self.values())
            self.ghost = Ghost(shape)
            # Native Fit All uses document view providers and omits this view-only
            # overlay. Frame the whole scene so an offset preview is actually visible.
            from pivy import coin
            view = Gui.activeDocument().activeView()
            view.getCameraNode().viewAll(view.getSceneGraph(), coin.SbViewportRegion(*view.getSize()))
            self.message.setText(tr("Copy origin in world coordinates (mm): ") +
                                 ", ".join(f"{value:.6g}" for value in placement.Base))
        except Exception as error:
            self.clearPreview()
            self.message.setText(str(error))

    def createCopy(self):
        self.saving = True
        self.clearPreview()
        try:
            Reuse.create_copy(resolve(self.key), self.expected, self.name.text(), *self.values())
            self.accept()
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.saving = False

    def slotChangedObject(self, obj, prop):
        if obj.Document == self.doc and not self.closed and not self.saving:
            self.clearPreview()
            self.expected = None
            self.previewButton.setEnabled(False)
            self.copyButton.setEnabled(False)
            self.message.setText(tr("The document changed. Recompute if needed, then Review again."))

    def slotDeletedObject(self, obj):
        if identity(obj) == self.key:
            self.reject()

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def done(self, result):
        if not self.closed:
            self.closed = True
            self.clearPreview()
            App.removeDocumentObserver(self)
        super().done(result)


class Command:
    def GetResources(self):
        return {"MenuText": tr("Copy reusable sketch..."),
                "ToolTip": tr("Place an independent whole-sketch copy while preserving its internal constraints")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        selected = Gui.Selection.getSelectionEx()
        if len(selected) != 1 or selected[0].SubElementNames:
            QtWidgets.QMessageBox.information(Gui.getMainWindow(), tr("Copy reusable sketch"), tr("Select one whole sketch in the tree."))
            return
        dialog = CopyDialog(selected[0].Object, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Sketcher_CopyReusable", Command())
