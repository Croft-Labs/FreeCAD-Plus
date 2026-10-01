# SPDX-License-Identifier: LGPL-2.1-or-later
"""Review explicit input objects and reusable STL quality before manufacturing handoff."""
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
import ManufacturingExport as Export


def _tr(text):
    return App.Qt.translate("ManufacturingExport", text)


class ExportDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_tr("Manufacturing export - STL"))
        self.resize(680, 520)
        self.targets = ()
        layout = QtWidgets.QFormLayout(self)
        self.inputs = QtWidgets.QPlainTextEdit()
        self.inputs.setReadOnly(True)
        self.inputs.setMaximumHeight(125)
        self.useSelection = QtWidgets.QPushButton(_tr("Use current selection"))
        self.preset = QtWidgets.QComboBox()
        self.linear = QtWidgets.QDoubleSpinBox()
        self.linear.setDecimals(3)
        self.linear.setRange(0.001, 10)
        self.linear.setSuffix(" mm")
        self.angular = QtWidgets.QDoubleSpinBox()
        self.angular.setRange(1, 90)
        self.angular.setSuffix(_tr(" deg"))
        self.presetName = QtWidgets.QLineEdit()
        self.savePreset = QtWidgets.QPushButton(_tr("Save custom preset"))
        self.resetPresets = QtWidgets.QPushButton(_tr("Reset presets"))
        self.path = QtWidgets.QLineEdit()
        self.browse = QtWidgets.QPushButton(_tr("Choose file..."))
        self.status = QtWidgets.QLabel()
        self.status.setWordWrap(True)
        self.status.setTextFormat(QtCore.Qt.PlainText)
        self.exportButton = QtWidgets.QPushButton(_tr("Export STL"))
        self.closeButton = QtWidgets.QPushButton(_tr("Close"))
        layout.addRow(_tr("Inputs"), self.inputs)
        layout.addRow(self.useSelection)
        layout.addRow(_tr("Output"), QtWidgets.QLabel(_tr("STL - millimeters - world placement")))
        layout.addRow(_tr("Quality preset"), self.preset)
        layout.addRow(_tr("Linear deflection"), self.linear)
        layout.addRow(_tr("Angular deflection"), self.angular)
        layout.addRow(_tr("Custom preset name"), self.presetName)
        layout.addRow(self.savePreset, self.resetPresets)
        layout.addRow(_tr("Output file"), self.path)
        layout.addRow(self.browse)
        notice = QtWidgets.QLabel(_tr(
            "Exports current recomputed geometry of the listed objects. Selection changes do not "
            "replace these inputs until Use current selection. STL contains triangles only: no "
            "feature history, units metadata, colors or assembly identity. Import it as millimeters. "
            "Separate solids are not fused or checked for collisions."))
        notice.setWordWrap(True)
        layout.addRow(notice)
        layout.addRow(self.status)
        layout.addRow(self.exportButton, self.closeButton)
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setAutoDefault(False)
        self.useSelection.clicked.connect(self.captureSelection)
        self.preset.currentIndexChanged.connect(self.loadPreset)
        self.savePreset.clicked.connect(self.storePreset)
        self.resetPresets.clicked.connect(self.reset)
        self.browse.clicked.connect(self.chooseFile)
        self.exportButton.clicked.connect(self.export)
        self.closeButton.clicked.connect(self.reject)
        self.reloadPresets("Normal")
        self.captureSelection()

    def reloadPresets(self, selected="Normal"):
        self.preset.blockSignals(True)
        self.preset.clear()
        try:
            self.settings = Export.presets()
        except ValueError as error:
            self.settings = dict(Export.DEFAULTS)
            self.status.setText(str(error))
        self.preset.addItems(list(self.settings))
        self.preset.setCurrentText(selected)
        self.preset.blockSignals(False)
        self.loadPreset()

    def loadPreset(self, *args):
        linear, angular = self.settings[self.preset.currentText()]
        self.linear.setValue(linear)
        self.angular.setValue(angular)

    def storePreset(self):
        try:
            name = self.presetName.text().strip()
            Export.save_preset(name, self.linear.value(), self.angular.value())
            self.reloadPresets(name)
            self.status.setText(_tr("Preset saved. Inputs and output paths are never stored in presets."))
        except ValueError as error:
            self.status.setText(str(error))

    def reset(self):
        Export.reset_presets()
        self.reloadPresets()
        self.status.setText(_tr("Custom presets removed; built-in settings restored."))

    def captureSelection(self):
        self.targets = ()
        self.inputs.clear()
        self.exportButton.setEnabled(False)
        try:
            if Gui.Control.activeDialog():
                raise ValueError(_tr("Finish or cancel the active task before exporting."))
            entries = Gui.Selection.getSelectionEx("*", 0)
            objects = []
            for entry in entries:
                for subname in entry.SubElementNames or [""]:
                    if subname and not subname.endswith("."):
                        raise ValueError(_tr("Select whole objects in the tree, not faces or edges."))
                    path = entry.Object.getSubObjectList(subname)
                    if not path or any(obj.isDerivedFrom("App::Link") for obj in path[:-1]):
                        raise ValueError(_tr("Select a whole local occurrence, not a member inside a linked component."))
                    objects.append(path[-1])
            shapes = Export.collect_shapes(objects)
            self.targets = tuple(obj for obj, _ in shapes)
            rows = []
            for obj, shape in shapes:
                bounds = shape.BoundBox
                rows.append("{} / {} [{}]: {:.3f} x {:.3f} x {:.3f} mm".format(
                    obj.Document.Label, obj.Label, obj.Name,
                    bounds.XLength, bounds.YLength, bounds.ZLength))
            self.inputs.setPlainText("\n".join(rows))
            self.exportButton.setEnabled(True)
            self.status.setText(_tr("Ready. Review the inputs, quality and output path."))
        except Exception as error:
            self.status.setText(str(error))

    def chooseFile(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, _tr("Export STL"), self.path.text(), "STL (*.stl)",
            options=QtWidgets.QFileDialog.DontConfirmOverwrite)
        if filename:
            self.path.setText(filename if filename.lower().endswith(".stl") else filename + ".stl")

    def export(self):
        try:
            if Gui.Control.activeDialog():
                raise ValueError(_tr("Finish or cancel the active task before exporting."))
            filename = self.path.text().strip()
            overwrite = Path(filename).is_file()
            if overwrite and QtWidgets.QMessageBox.question(
                    self, _tr("Replace output?"), _tr("Replace the existing STL file?") + "\n" + filename,
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.No) != QtWidgets.QMessageBox.Yes:
                return
            report = Export.export_stl(self.targets, filename, self.linear.value(),
                                       self.angular.value(), overwrite=overwrite)
            self.status.setText(_tr("Exported %1 triangles; size %2 mm.\n%3")
                                .replace("%1", str(report["facets"]))
                                .replace("%2", " x ".join("{:.3f}".format(value) for value in report["size_mm"]))
                                .replace("%3", report["file"]))
        except Exception as error:
            self.status.setText(str(error))


_dialogs = []


class CommandExport:
    def GetResources(self):
        return {"MenuText": _tr("Manufacturing export..."),
                "ToolTip": _tr("Export selected whole solids to STL with explicit placement and reusable mesh quality")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        dialog = ExportDialog(Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Part_ManufacturingExport", CommandExport())
