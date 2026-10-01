# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit planar support inspection, placement preview and undoable reattachment."""
import hashlib
import math
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from SketchSupport import preview_planar, reattach_planar


def _tr(text):
    return App.Qt.translate("SketchSupport", text)


def selected_sketch():
    objects = Gui.Selection.getSelection()
    if len(objects) != 1 or not objects[0].isDerivedFrom("Sketcher::SketchObject"):
        raise ValueError(_tr("Select one sketch outside edit mode."))
    return objects[0]


def _placement(placement):
    origin, rotation = placement.Base, placement.Rotation
    return ("XYZ: {:.3f}, {:.3f}, {:.3f} mm; axis: {:.4f}, {:.4f}, {:.4f}; angle: {:.3f} deg"
            .format(origin.x, origin.y, origin.z, rotation.Axis.x, rotation.Axis.y,
                    rotation.Axis.z, math.degrees(rotation.Angle)))


class SupportDialog(QtWidgets.QDialog):
    def __init__(self, sketch, parent=None):
        super().__init__(parent)
        self.sketch, self.doc = sketch, sketch.Document
        self.support = None
        self.previewState = None
        self._closed = False
        self.setWindowTitle(_tr("Sketch support") + " - " + sketch.Label)
        self.resize(760, 410)
        layout = QtWidgets.QFormLayout(self)
        self.current = QtWidgets.QLabel()
        self.current.setWordWrap(True)
        self.current.setTextFormat(QtCore.Qt.PlainText)
        self.target = QtWidgets.QLineEdit()
        self.target.setReadOnly(True)
        self.face = QtWidgets.QLineEdit()
        self.pick = QtWidgets.QPushButton(_tr("Use selected planar face"))
        self.policy = QtWidgets.QComboBox()
        self.policy.addItem(_tr("Preserve local attachment offset (follow new support)"), "preserve-local")
        self.policy.addItem(_tr("Preserve world placement (solve a new offset)"), "preserve-world")
        self.previewButton = QtWidgets.QPushButton(_tr("Preview placement"))
        self.applyButton = QtWidgets.QPushButton(_tr("Apply reattachment"))
        self.closeButton = QtWidgets.QPushButton(_tr("Close"))
        self.result = QtWidgets.QLabel()
        self.result.setWordWrap(True)
        self.result.setTextFormat(QtCore.Qt.PlainText)
        layout.addRow(_tr("Current support"), self.current)
        layout.addRow(_tr("Replacement object"), self.target)
        layout.addRow(_tr("Face"), self.face)
        layout.addRow(self.pick)
        layout.addRow(_tr("Placement policy"), self.policy)
        note = QtWidgets.QLabel(_tr(
            "Select a planar face in the same native container, then preview. Preview reports "
            "placement only; it does not simulate constraints or downstream solids. Apply is "
            "undoable. Check dependent features afterward. Linked occurrence supports and "
            "cross-container references are not supported in this pilot."))
        note.setWordWrap(True)
        layout.addRow(note)
        layout.addRow(self.result)
        layout.addRow(self.previewButton, self.applyButton)
        layout.addRow(self.closeButton)
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setAutoDefault(False)
        self.face.textChanged.connect(self.invalidate)
        self.policy.currentIndexChanged.connect(self.invalidate)
        self.pick.clicked.connect(self.captureFace)
        self.previewButton.clicked.connect(self.preview)
        self.applyButton.clicked.connect(self.apply)
        self.closeButton.clicked.connect(self.reject)
        self.refreshCurrent()
        self.invalidate()
        App.addDocumentObserver(self)

    def refreshCurrent(self):
        entries = []
        for obj, subs in self.sketch.AttachmentSupport:
            entries.append((obj.Label if obj else _tr("Missing object")) + ": " + ", ".join(subs))
        self.current.setText(("; ".join(entries) or _tr("Unattached")) + "\n" +
                             _tr("World placement: ") + _placement(self.sketch.getGlobalPlacement()))

    def invalidate(self, *args):
        self.previewState = None
        self.applyButton.setEnabled(False)
        self.result.setText(_tr("Choose a replacement face and preview before applying."))

    def context(self):
        if self._closed:
            raise ValueError(_tr("This sketch editor is closed."))
        if App.ActiveDocument != self.doc:
            raise ValueError(_tr("Activate the sketch's document before continuing."))
        if Gui.Control.activeDialog():
            raise ValueError(_tr("Finish or cancel the active task before reattaching."))
        if self.support is None:
            raise ValueError(_tr("Select a replacement planar face."))

    def signature(self):
        def shape_signature(obj):
            brep = "" if obj.Shape.isNull() else obj.Shape.exportBrepToString()
            return (obj.ID, hashlib.sha256(brep.encode()).hexdigest(),
                    tuple(obj.getGlobalPlacement().toMatrix().A), tuple(obj.State))
        return (shape_signature(self.sketch), shape_signature(self.support),
                tuple(self.sketch.AttachmentOffset.toMatrix().A), self.sketch.MapMode,
                self.sketch.MapReversed, tuple(self.sketch.ExpressionEngine),
                tuple((obj.ID if obj else None, tuple(subs)) for obj, subs in self.sketch.AttachmentSupport),
                self.face.text().strip(), self.policy.currentData())

    def captureFace(self):
        self.invalidate()
        self.support = None
        self.target.clear()
        self.face.clear()
        try:
            selections = Gui.Selection.getSelectionEx("*", 0)
            if len(selections) != 1 or len(selections[0].SubElementNames) != 1:
                raise ValueError(_tr("Select exactly one planar face."))
            entry = selections[0]
            subname = entry.SubElementNames[0]
            path = entry.Object.getSubObjectList(subname)
            if not path or any(obj.isDerivedFrom("App::Link") for obj in path):
                raise ValueError(_tr("Select a native support face, not a linked occurrence."))
            self.support = path[-1]
            self.target.setText(self.support.Label + " [" + self.support.Name + "]")
            self.face.setText(subname.rsplit(".", 1)[-1])
        except Exception as error:
            self.result.setText(str(error))

    def preview(self):
        self.invalidate()
        try:
            self.context()
            before = self.signature()
            placement, offset = preview_planar(self.sketch, self.support, self.face.text().strip(),
                                                self.policy.currentData())
            if self.signature() != before:
                raise ValueError(_tr("The inputs changed during preview. Preview again."))
            self.previewState = before
            self.applyButton.setEnabled(True)
            self.result.setText(_tr("Candidate world placement: ") + _placement(placement) + "\n" +
                                _tr("Candidate attachment offset: ") + _placement(offset))
        except Exception as error:
            self.result.setText(str(error))

    def apply(self):
        try:
            self.context()
            if self.previewState is None or self.signature() != self.previewState:
                raise ValueError(_tr("Inputs changed or no preview is available. Preview again before applying."))
            reattach_planar(self.sketch, self.support, self.face.text().strip(), self.policy.currentData())
            self.refreshCurrent()
            self.invalidate()
            self.result.setText(_tr("Reattached. Check downstream results; Undo restores the previous support."))
        except Exception as error:
            self.previewState = None
            self.applyButton.setEnabled(False)
            self.result.setText(str(error))

    def slotDeletedObject(self, obj):
        if obj == self.sketch:
            self.reject()
        elif obj == self.support:
            self.support = None
            self.target.clear()
            self.invalidate()
            self.result.setText(_tr("The replacement support was deleted. Select another face."))

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def done(self, result):
        if not self._closed:
            self._closed = True
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class CommandSupport:
    def GetResources(self):
        return {"MenuText": _tr("Inspect and change sketch support..."),
                "ToolTip": _tr("Preview preserve-local or preserve-world planar sketch reattachment")}

    def IsActive(self):
        try:
            return not Gui.Control.activeDialog() and not selected_sketch().Document.HasPendingTransaction
        except ValueError:
            return False

    def Activated(self):
        dialog = SupportDialog(selected_sketch(), Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Sketcher_InspectSupport", CommandSupport())
