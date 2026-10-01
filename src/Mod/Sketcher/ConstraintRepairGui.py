# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit constraint review, isolated solve preview and undoable deactivation."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve
from freecad.gui.OccurrenceMove import Ghost
import ConstraintRepair as Repair

tr = Repair.tr
_dialogs = []


class RepairDialog(QtWidgets.QDialog):
    def __init__(self, sketch, parent=None):
        super().__init__(parent)
        self.key, self.doc = identity(sketch), sketch.Document
        self.expected = self.previewed = self.ghost = None
        self.closed = self.busy = False
        self.setWindowTitle(tr("Review sketch constraint repair"))
        self.resize(850, 620)
        layout = QtWidgets.QVBoxLayout(self)
        self.summary = QtWidgets.QLabel()
        self.summary.setWordWrap(True)
        self.summary.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.summary)
        note = QtWidgets.QLabel(tr(
            "Check the active constraints you want to deactivate, then preview. Solver groups are "
            "candidate sets, not a unique diagnosis. Nothing is selected for repair automatically. "
            "Deactivation retains constraint numbers, names and values so you can re-enable them later."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([tr(s) for s in ("Deactivate", "Constraint", "Type", "Value", "State", "Geometry")])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        self.message = QtWidgets.QLabel()
        self.message.setWordWrap(True)
        self.message.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.message)
        buttons = QtWidgets.QHBoxLayout()
        self.refresh = QtWidgets.QPushButton(tr("Review again"))
        self.highlight = QtWidgets.QPushButton(tr("Select row geometry"))
        self.previewButton = QtWidgets.QPushButton(tr("Preview deactivation"))
        self.applyButton = QtWidgets.QPushButton(tr("Apply deactivation"))
        self.cancel = QtWidgets.QPushButton(tr("Cancel"))
        for button in (self.refresh, self.highlight, self.previewButton, self.applyButton, self.cancel):
            button.setAutoDefault(False)
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.refresh.clicked.connect(self.review)
        self.highlight.clicked.connect(self.select)
        self.previewButton.clicked.connect(self.preview)
        self.applyButton.clicked.connect(self.commit)
        self.cancel.clicked.connect(self.reject)
        self.table.itemChanged.connect(self.clear_preview)
        App.addDocumentObserver(self)
        self.review()

    def clear_preview(self, *args):
        if self.ghost is not None:
            self.ghost.remove()
            self.ghost = None
        self.previewed = None
        self.applyButton.setEnabled(False)
        self.message.setText(tr("Choose constraints and preview their deactivation."))

    def review(self):
        self.clear_preview()
        self.expected = None
        self.table.setRowCount(0)
        self.previewButton.setEnabled(False)
        self.highlight.setEnabled(False)
        self.busy = True
        try:
            sketch = resolve(self.key)
            expected = Repair.snapshot(sketch)
            info = Repair.probe(sketch, expected)["before"]
            self.expected = expected
            self.summary.setText("{} [{}]\n{}; {}".format(sketch.Label, sketch.Name, tr(info["state"]),
                tr("degrees of freedom: %1").replace("%1", str(info["dof"])) if info["ok"] else
                tr("freedom count is not a valid movement diagnosis until the solve succeeds")))
            self.table.blockSignals(True)
            self.table.setRowCount(sketch.ConstraintCount)
            for index, constraint in enumerate(sketch.Constraints):
                item = QtWidgets.QTableWidgetItem()
                if constraint.IsActive:
                    item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setFlags(QtCore.Qt.NoItemFlags)
                self.table.setItem(index, 0, item)
                roles = [name for name, ids in info["groups"].items() if index + 1 in ids]
                state = ", ".join(tr(s) for s in roles) or tr("Active" if constraint.IsActive else "Inactive")
                try:
                    value = str(sketch.getDatum(index))
                    if not constraint.Driving:
                        state += tr("; reference")
                except TypeError:
                    value = "-"
                geos = self.geometry_indices(constraint, sketch.GeometryCount)
                values = (str(index + 1) + (" / " + constraint.Name if constraint.Name else ""),
                          constraint.Type, value, state, ", ".join("Edge" + str(i + 1) for i in geos) or tr("Axes/origin"))
                for column, value in enumerate(values, 1):
                    self.table.setItem(index, column, QtWidgets.QTableWidgetItem(value))
            self.table.resizeColumnsToContents()
            self.previewButton.setEnabled(True)
            self.highlight.setEnabled(True)
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.table.blockSignals(False)
            self.busy = False

    @staticmethod
    def geometry_indices(constraint, count):
        return sorted({getattr(constraint, name) for name in ("First", "Second", "Third")
                       if 0 <= getattr(constraint, name) < count})

    def selected(self):
        return tuple(i for i in range(self.table.rowCount())
                     if self.table.item(i, 0).checkState() == QtCore.Qt.Checked)

    def select(self):
        try:
            sketch = resolve(self.key)
            Repair.ready(sketch)
            if Repair.snapshot(sketch) != self.expected:
                raise ValueError(tr("The sketch changed. Review again."))
            row = self.table.currentRow()
            if row < 0:
                raise ValueError(tr("Choose a constraint row first."))
            Gui.Selection.clearSelection()
            for index in self.geometry_indices(sketch.Constraints[row], sketch.GeometryCount):
                Gui.Selection.addSelection(sketch, "Edge" + str(index + 1))
        except Exception as error:
            self.message.setText(str(error))

    def preview(self):
        self.clear_preview()
        self.busy = True
        try:
            chosen = self.selected()
            if not chosen:
                raise ValueError(tr("Check at least one active constraint to preview."))
            result = Repair.probe(resolve(self.key), self.expected, chosen)
            after = result["after"]
            if after["ok"]:
                self.ghost = Ghost(result["shape"])
                # Failed source sketches may have no view-provider bounding box.
                # Frame the temporary result through the scene graph, as SketchReuse does.
                from pivy import coin
                view = Gui.activeDocument().activeView()
                view.getCameraNode().viewAll(view.getSceneGraph(), coin.SbViewportRegion(*view.getSize()))
                self.previewed = result
                self.applyButton.setEnabled(True)
                self.message.setText(tr("Preview: %1; degrees of freedom: %2. Source unchanged. Apply updates downstream geometry.")
                    .replace("%1", tr(after["state"])).replace("%2", str(after["dof"])))
            else:
                self.message.setText(tr("Preview still fails: %1. Choose a different set; no repair can be applied.")
                                     .replace("%1", tr(after["state"])))
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.busy = False

    def commit(self):
        self.busy = True
        try:
            Repair.apply(resolve(self.key), self.previewed)
            self.accept()
        except Exception as error:
            self.clear_preview()
            self.message.setText(str(error))
        finally:
            self.busy = False

    def slotChangedObject(self, obj, prop):
        if obj.Document == self.doc and not self.busy and not self.closed:
            self.clear_preview()
            self.expected = None
            self.previewButton.setEnabled(False)
            self.message.setText(tr("The document changed. Review again before choosing a repair."))

    def slotDeletedObject(self, obj):
        if identity(obj) == self.key:
            self.reject()

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def done(self, result):
        if not self.closed:
            self.closed = True
            self.clear_preview()
            App.removeDocumentObserver(self)
        super().done(result)


class Command:
    def GetResources(self):
        return {"MenuText": tr("Review constraint repair..."),
                "ToolTip": tr("Preview selected constraint deactivation on a temporary native sketch copy")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        selection = Gui.Selection.getSelectionEx()
        if len(selection) != 1 or selection[0].SubElementNames:
            App.Console.PrintError(tr("Select one whole root sketch in the tree.\n"))
            return
        dialog = RepairDialog(selection[0].Object, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _r: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Sketcher_ReviewConstraintRepair", Command())
