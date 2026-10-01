# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit pair results and selection navigation for native solid inspection."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
import InterferenceCheck as Check


def _tr(text):
    return App.Qt.translate("InterferenceCheck", text)


class InspectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.document = App.ActiveDocument
        self.references = []
        self.checked = []
        self.rows = []
        self._closed = False
        self.setWindowTitle(_tr("Interference and clearance"))
        self.resize(980, 650)
        layout = QtWidgets.QVBoxLayout(self)
        note = QtWidgets.QLabel(_tr(
            "Check 2-12 explicitly selected whole solids or direct occurrences. Hidden inputs are "
            "included. Uncheck an input to exclude it deliberately. Distances are in world mm; "
            "overlap volume is mm³. Contact includes gaps within the stated tolerance. "
            "This checks only the included set, not the entire assembly."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.inputs = QtWidgets.QListWidget()
        self.inputs.setMaximumHeight(150)
        layout.addWidget(self.inputs)
        self.useSelection = QtWidgets.QPushButton(_tr("Replace inputs with current selection"))
        layout.addWidget(self.useSelection)
        form = QtWidgets.QFormLayout()
        self.clearance = QtWidgets.QDoubleSpinBox()
        self.clearance.setDecimals(6)
        self.clearance.setRange(0.000001, 1000000)
        self.clearance.setValue(1)
        self.clearance.setSuffix(" mm")
        self.tolerance = QtWidgets.QDoubleSpinBox()
        self.tolerance.setDecimals(6)
        self.tolerance.setRange(0.000001, 1)
        self.tolerance.setValue(0.000001)
        self.tolerance.setSuffix(" mm")
        form.addRow(_tr("Required clearance"), self.clearance)
        form.addRow(_tr("Contact tolerance"), self.tolerance)
        layout.addLayout(form)
        self.checkButton = QtWidgets.QPushButton(_tr("Check included pairs"))
        layout.addWidget(self.checkButton)
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([_tr(t) for t in
            ("First input", "Second input", "Result", "Distance (mm)", "Overlap (mm³)", "Details")])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        self.status = QtWidgets.QLabel()
        self.status.setWordWrap(True)
        self.status.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.status)
        self.selectPair = QtWidgets.QPushButton(_tr("Select result pair"))
        self.selectPair.setEnabled(False)
        close = QtWidgets.QPushButton(_tr("Close"))
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(self.selectPair)
        buttons.addWidget(close)
        layout.addLayout(buttons)
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setAutoDefault(False)
        self.useSelection.clicked.connect(self.capture)
        self.checkButton.clicked.connect(self.check)
        self.selectPair.clicked.connect(self.select)
        self.inputs.itemChanged.connect(self.invalidate)
        self.clearance.valueChanged.connect(self.invalidate)
        self.tolerance.valueChanged.connect(self.invalidate)
        close.clicked.connect(self.reject)
        self.capture()
        App.addDocumentObserver(self)

    def invalidate(self, *args):
        self.rows = []
        self.checked = []
        self.table.setRowCount(0)
        self.selectPair.setEnabled(False)
        self.status.setText(_tr("Results are not current. Check included pairs again."))

    def capture(self):
        self.invalidate()
        try:
            refs, keys = [], set()
            for entry in Gui.Selection.getSelectionEx("*", 0):
                if entry.Object.Document != self.document:
                    raise ValueError(_tr("Choose inputs from this inspection's document."))
                for sub in entry.SubElementNames or [""]:
                    ref = Check.Reference(entry.Object, sub)
                    if ref.key not in keys:
                        refs.append(ref)
                        keys.add(ref.key)
            if not 2 <= len(refs) <= Check.MAX_INPUTS:
                raise ValueError(_tr("Select 2-12 whole inputs, then replace the input list."))
            self.references = refs
            self.inputs.blockSignals(True)
            self.inputs.clear()
            for ref in refs:
                item = QtWidgets.QListWidgetItem(ref.label)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked)
                self.inputs.addItem(item)
            self.inputs.blockSignals(False)
            self.status.setText(_tr("Review the explicit inputs and exclusions, then check pairs."))
        except Exception as error:
            self.status.setText(str(error))

    def check(self):
        self.invalidate()
        try:
            if App.ActiveDocument != self.document or Gui.Control.activeDialog():
                raise ValueError(_tr("Activate this document and finish the current task before checking."))
            included = [ref for i, ref in enumerate(self.references)
                        if self.inputs.item(i).checkState() == QtCore.Qt.Checked]
            rows = Check.inspect(included, self.clearance.value(), self.tolerance.value())
            self.checked, self.rows = included, rows
            self.table.setRowCount(len(rows))
            counts = {}
            for i, row in enumerate(rows):
                counts[row["status"]] = counts.get(row["status"], 0) + 1
                values = [included[row["a"]].label, included[row["b"]].label, _tr(row["status"]),
                          "—" if row["distance"] is None else "{:.9g}".format(row["distance"]),
                          "—" if row["volume"] is None else "{:.9g}".format(row["volume"]), row["detail"]]
                for j, value in enumerate(values):
                    item = QtWidgets.QTableWidgetItem(value)
                    item.setToolTip(value)
                    self.table.setItem(i, j, item)
            self.table.resizeColumnsToContents()
            self.selectPair.setEnabled(bool(rows))
            excluded = len(self.references) - len(included)
            summary = "; ".join(_tr(key) + ": " + str(value) for key, value in counts.items())
            self.status.setText((_tr("Incomplete check. ") if counts.get("Unresolved") else "") +
                _tr("Included pairs: %1; excluded inputs: %2. ").replace("%1", str(len(rows)))
                .replace("%2", str(excluded)) + summary)
        except Exception as error:
            self.status.setText(str(error))

    def select(self):
        row = self.table.currentRow()
        if not 0 <= row < len(self.rows):
            self.status.setText(_tr("Choose a result row first."))
            return
        try:
            pair = self.rows[row]
            refs = [self.checked[pair[key]] for key in ("a", "b")]
            resolved = [(ref, ref.resolve()[0]) for ref in refs]
            Gui.Selection.clearSelection()
            for ref, root in resolved:
                Gui.Selection.addSelection(root, ref.sub)
        except Exception as error:
            self.invalidate()
            self.status.setText(str(error))

    def slotChangedObject(self, obj, prop):
        if obj.Document == self.document:
            self.invalidate()

    def slotDeletedObject(self, obj):
        if obj.Document == self.document:
            self.invalidate()

    def slotDeletedDocument(self, doc):
        if doc == self.document:
            self.reject()

    def done(self, result):
        if not self._closed:
            self._closed = True
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class CommandCheck:
    def GetResources(self):
        return {"MenuText": _tr("Interference and clearance..."),
                "ToolTip": _tr("Inspect selected solid pairs for overlap, contact and minimum clearance")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        dialog = InspectionDialog(Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Part_InterferenceCheck", CommandCheck())
