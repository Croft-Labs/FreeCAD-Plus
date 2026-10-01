# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit face roles and disposable sampled-deviation markers."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
import SurfaceDeviation as Check


def _tr(text):
    return App.Qt.translate("SurfaceDeviation", text)


class PointMap:
    def __init__(self, view, report):
        from pivy import coin
        self.scene = view.getSceneGraph()
        self.node = coin.SoAnnotation()
        pick = coin.SoPickStyle()
        pick.style = coin.SoPickStyle.UNPICKABLE
        self.node.addChild(pick)
        style = coin.SoDrawStyle()
        style.pointSize = 7
        self.node.addChild(style)
        binding = coin.SoMaterialBinding()
        binding.value = coin.SoMaterialBinding.PER_VERTEX
        self.node.addChild(binding)
        colors = coin.SoBaseColor()
        colors.rgb.setValues(0, len(report["colors"]), report["colors"])
        self.node.addChild(colors)
        coords = coin.SoCoordinate3()
        coords.point.setValues(0, len(report["points"]), report["points"])
        self.node.addChild(coords)
        points = coin.SoPointSet()
        points.numPoints = len(report["points"])
        self.node.addChild(points)
        self.scene.addChild(self.node)

    def remove(self):
        if self.node is not None:
            self.scene.removeChild(self.node)
            self.node = None


class DeviationDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.document = App.ActiveDocument
        self.sampled = self.reference = self.overlay = self.report = None
        self._closed = False
        self.setWindowTitle(_tr("Sampled face deviation"))
        self.resize(720, 600)
        layout = QtWidgets.QVBoxLayout(self)
        note = QtWidgets.QLabel(_tr(
            "Select one face, then capture its role below. Root Part shapes and whole root Bodies "
            "are supported. The map measures unsigned nearest distance from sampled face to finite "
            "reference face, including reference boundaries, in world millimeters. No alignment is applied."))
        note.setWordWrap(True)
        layout.addWidget(note)
        form = QtWidgets.QFormLayout()
        self.sampleLabel = QtWidgets.QLabel(_tr("Not captured"))
        self.referenceLabel = QtWidgets.QLabel(_tr("Not captured"))
        for label in (self.sampleLabel, self.referenceLabel):
            label.setWordWrap(True)
            label.setTextFormat(QtCore.Qt.PlainText)
        self.sampleButton = QtWidgets.QPushButton(_tr("Capture sampled face"))
        self.referenceButton = QtWidgets.QPushButton(_tr("Capture reference face"))
        form.addRow(self.sampleButton, self.sampleLabel)
        form.addRow(self.referenceButton, self.referenceLabel)
        self.grid = QtWidgets.QSpinBox()
        self.grid.setRange(3, 25)
        self.scale = QtWidgets.QDoubleSpinBox()
        self.scale.setDecimals(6)
        self.scale.setRange(.000001, 1000000)
        self.scale.setSuffix(" mm")
        grid, scale = Check.load_settings()
        self.grid.setValue(grid)
        self.scale.setValue(scale)
        form.addRow(_tr("Samples per UV direction"), self.grid)
        form.addRow(_tr("Full color scale"), self.scale)
        layout.addLayout(form)
        self.legend = QtWidgets.QLabel()
        layout.addWidget(self.legend)
        self.checkButton = QtWidgets.QPushButton(_tr("Check and show map"))
        layout.addWidget(self.checkButton)
        self.results = QtWidgets.QPlainTextEdit()
        self.results.setReadOnly(True)
        layout.addWidget(self.results)
        caveat = QtWidgets.QLabel(_tr(
            "Markers are drawn on top of geometry. Grid cell centers sample the UV domain; holes and "
            "trimmed-out regions are excluded. Statistics are not area weighted. Narrow defects and "
            "boundary extrema can be missed. This one-way sampled display is not a maximum-deviation, "
            "continuity or tolerance certification. Singular/failed samples are reported separately."))
        caveat.setWordWrap(True)
        layout.addWidget(caveat)
        self.status = QtWidgets.QLabel()
        self.status.setWordWrap(True)
        self.status.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.status)
        self.saveButton = QtWidgets.QPushButton(_tr("Save sampling settings"))
        self.clearButton = QtWidgets.QPushButton(_tr("Clear map"))
        self.closeButton = QtWidgets.QPushButton(_tr("Close"))
        buttons = QtWidgets.QHBoxLayout()
        for button in (self.saveButton, self.clearButton, self.closeButton):
            buttons.addWidget(button)
        layout.addLayout(buttons)
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setAutoDefault(False)
        self.sampleButton.clicked.connect(lambda: self.capture("sampled"))
        self.referenceButton.clicked.connect(lambda: self.capture("reference"))
        self.checkButton.clicked.connect(self.check)
        self.grid.valueChanged.connect(self.invalidate)
        self.scale.valueChanged.connect(self.invalidate)
        self.clearButton.clicked.connect(self.invalidate)
        self.closeButton.clicked.connect(self.reject)
        self.saveButton.clicked.connect(self.save)
        self.invalidate()
        App.addDocumentObserver(self)

    def invalidate(self, *args):
        if self.overlay is not None:
            self.overlay.remove()
            self.overlay = None
        self.report = None
        self.results.clear()
        scale = self.scale.value()
        self.legend.setText(_tr("Blue: 0 mm | Yellow: %1 mm | Red: %2 mm or greater")
                            .replace("%1", "{:.6g}".format(scale / 2))
                            .replace("%2", "{:.6g}".format(scale)))
        self.status.setText(_tr("No current result. Capture face roles and check again."))

    def ready(self):
        if App.ActiveDocument != self.document or Gui.Control.activeDialog():
            raise ValueError(_tr("Activate this document and finish the current task first."))

    def capture(self, role):
        self.invalidate()
        setattr(self, role, None)
        label = self.sampleLabel if role == "sampled" else self.referenceLabel
        label.setText(_tr("Not captured"))
        try:
            self.ready()
            selected = Gui.Selection.getSelectionEx("*", 0)
            if (len(selected) != 1 or selected[0].Object.Document != self.document
                    or len(selected[0].SubElementNames) > 1):
                raise ValueError(_tr("Select exactly one face in this document."))
            entry = selected[0]
            ref = Check.FaceReference(entry.Object, entry.SubElementNames[0] if entry.SubElementNames else "")
            setattr(self, role, ref)
            label.setText(ref.label)
        except Exception as error:
            self.status.setText(str(error))

    def check(self):
        self.invalidate()
        try:
            self.ready()
            if self.sampled is None or self.reference is None:
                raise ValueError(_tr("Capture both face roles before checking."))
            report = Check.inspect(self.sampled, self.reference, self.grid.value(), self.scale.value())
            self.overlay = PointMap(Gui.activeDocument().activeView(), report)
            self.report = report
            self.results.setPlainText(_tr(
                "Sampled: {sampled}\nReference: {reference}\n"
                "Grid: {grid} x {grid} UV cell centers; usable: {count}\n"
                "Outside trimmed face: {outside}; singular/failed: {unresolved}\n"
                "Sample minimum: {minimum:.9g} mm\nSample maximum: {maximum:.9g} mm\n"
                "Sample mean: {mean:.9g} mm\nAt/above full color scale: {saturated}")
                .format(count=len(report["points"]), **report))
            self.status.setText(_tr("Incomplete sampling: ") + "; ".join(report["errors"])
                                if report["unresolved"] else _tr("Sampled map ready; no model changes."))
        except Exception as error:
            self.invalidate()
            self.status.setText(str(error))

    def save(self):
        Check.save_settings(self.grid.value(), self.scale.value())
        self.status.setText(_tr("Sampling and scale saved for later sessions. Face references and results are not saved."))

    def slotChangedObject(self, obj, prop):
        if obj.Document == self.document:
            self.invalidate()

    def slotDeletedObject(self, obj):
        if obj.Document == self.document:
            self.invalidate()

    def slotDeletedDocument(self, doc):
        if doc == self.document:
            self.reject()

    def slotActivateDocument(self, doc):
        if doc != self.document:
            self.invalidate()

    def done(self, result):
        if not self._closed:
            self._closed = True
            self.invalidate()
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class CommandDeviation:
    def GetResources(self):
        return {"MenuText": _tr("Sampled face deviation..."),
                "ToolTip": _tr("Compare two explicit faces with a temporary one-way distance map")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        dialog = DeviationDialog(Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Part_SurfaceDeviation", CommandDeviation())
