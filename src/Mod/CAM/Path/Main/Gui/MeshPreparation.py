# SPDX-License-Identifier: LGPL-2.1-or-later
"""Mesh preparation review for direct-STL CAM inputs."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve
from Path.Main import MeshPreparation as Preparation

tr = Preparation.tr
_dialogs = []


class ReviewDialog(QtWidgets.QDialog):
    def __init__(self, source, parent=None):
        super().__init__(parent)
        self.key = identity(source)
        self.doc = source.Document
        self.expected = None
        self.closed = self.saving = False
        self.setWindowTitle(tr("Review CAM mesh"))
        self.resize(760, 630)
        layout = QtWidgets.QVBoxLayout(self)
        self.summary = QtWidgets.QLabel()
        self.summary.setTextFormat(QtCore.Qt.PlainText)
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)
        self.table = QtWidgets.QTreeWidget()
        self.table.setHeaderLabels([tr("Check"), tr("Finding")])
        self.table.setRootIsDecorated(False)
        self.table.setWordWrap(True)
        self.table.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table)
        info = QtWidgets.QLabel(tr("Dimensions are in mm as imported; STL does not declare units. Confirm the intended size. "
                                  "Self-intersections, machining accessibility and tool/stock clearance are not checked. "
                                  "This review does not generate or approve toolpaths."))
        info.setWordWrap(True)
        layout.addWidget(info)
        self.message = QtWidgets.QLabel()
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setWordWrap(True)
        layout.addWidget(self.message)
        buttons = QtWidgets.QHBoxLayout()
        refresh = QtWidgets.QPushButton(tr("Review again"))
        refresh.clicked.connect(self.review)
        self.copyButton = QtWidgets.QPushButton(tr("Create reversed-normal copy"))
        self.copyButton.clicked.connect(self.createCopy)
        close = QtWidgets.QPushButton(tr("Close"))
        close.clicked.connect(self.reject)
        for button in (refresh, self.copyButton, close):
            buttons.addWidget(button)
        layout.addLayout(buttons)
        App.addDocumentObserver(self)
        self.review()

    def review(self):
        self.expected = None
        self.copyButton.setEnabled(False)
        self.table.clear()
        try:
            source = resolve(self.key)
            report = Preparation.inspect(source)
            self.summary.setText(tr("Source: ") + source.Label + " — " + source.Document.Name + "." + source.Name)
            bounds = report["bounds"]
            rows = [(tr("Triangles / points"), f'{report["facets"]:,} / {report["points"]:,}'),
                    (tr("Size X × Y × Z (mm)"), " × ".join(f"{bounds[i+3]-bounds[i]:.6g}" for i in range(3))),
                    (tr("Minimum / maximum XYZ (mm)"), " / ".join(
                        ", ".join(f"{value:.6g}" for value in values) for values in (bounds[:3], bounds[3:]))),
                    (tr("Boundary / nonmanifold edges"), f'{report["boundary"]} / {report["nonmanifold"]}'),
                    (tr("Connected components"), str(report["components"])),
                    (tr("Inconsistent normal facets"), str(report["inconsistent"])),
                    (tr("Zero-area / duplicate triangles"), f'{report["degenerate"]} / {report["duplicate"]}'),
                    (tr("Closed topology / orientation"), (tr("Yes") if report["closed"] else tr("No")) + " / " + report["orientation"]),
                    (tr("Density"), tr("High: inspect detail and processing cost; no reduction applied") if report["dense"] else tr("Within this review's 200,000-triangle limit"))]
            defects = report["nonmanifold"] or report["inconsistent"] or report["degenerate"] or report["duplicate"]
            parallel = tr("Review mesh defects before generating paths") if defects else tr("Open surfaces may be usable; inspect coverage and cut side")
            waterline = tr("Open/defective mesh: inspect missing or broken contours") if defects or not report["closed"] else tr("Closed topology; inspect generated contours and cut side")
            rows.extend([(tr("Parallel finishing"), parallel), (tr("Waterline finishing"), waterline)])
            for label, value in rows:
                QtWidgets.QTreeWidgetItem(self.table, [label, value])
            self.table.resizeColumnToContents(0)
            self.expected = report
            self.copyButton.setEnabled(report["can_flip"])
            if report["can_flip"]:
                self.message.setText(tr("Inward normals: the copy will reverse every triangle, preserving coordinates and dimensions. "
                                        "The source stays unchanged. Existing jobs will not be relinked."))
            elif report["components"] > 1:
                self.message.setText(tr("Multiple pieces: confirm which pieces belong in the job. Per-piece orientation and repair are not available here."))
            else:
                self.message.setText(tr("Review only. Automatic hole filling, welding, smoothing and decimation are not applied."))
        except Exception as error:
            self.message.setText(str(error))

    def createCopy(self):
        self.saving = True
        try:
            result = Preparation.reversed_copy(resolve(self.key), self.expected)
            self.expected = None
            self.copyButton.setEnabled(False)
            self.message.setText(tr("Created independent copy: ") + result.Label + ". " +
                                 tr("Select it explicitly for a new CAM job. The source and existing jobs are unchanged. Undo removes the copy."))
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.saving = False

    def slotChangedObject(self, obj, prop):
        if obj.Document == self.doc and not self.closed and not self.saving:
            self.expected = None
            self.copyButton.setEnabled(False)
            self.table.clear()
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
            App.removeDocumentObserver(self)
        super().done(result)


class Command:
    def GetResources(self):
        return {"Pixmap": ":/icons/CAM_Job.svg", "MenuText": tr("Review CAM mesh..."),
                "ToolTip": tr("Inspect an imported mesh and optionally create an independent reversed-normal copy")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        selected = Gui.Selection.getSelectionEx()
        if len(selected) != 1 or selected[0].SubElementNames:
            QtWidgets.QMessageBox.information(Gui.getMainWindow(), tr("Review CAM mesh"), tr("Select one whole imported mesh in the tree."))
            return
        dialog = ReviewDialog(selected[0].Object, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


Gui.addCommand("CAM_MeshPreparation", Command())
