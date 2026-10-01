# SPDX-License-Identifier: LGPL-2.1-or-later
"""Search existing commands without changing their identity or execution contract."""

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets


def _tr(text):
    return App.Qt.translate("CommandSearch", text)


# name: (display name, familiar terms, workbench, intent/context guidance)
# These are entry presets into existing editors, not new modeling operations.
ALIASES = {
    "PartDesign_Extrude": (
        "Extrude", "extrusion", "PartDesignWorkbench",
        "Open a document. Choose a profile in the Extrude editor and review Add/Subtract."),
    "PartDesign_Pad": (
        "Pad (Extrude: Add)", "pad;extruded boss;extruded boss/base;boss-extrude;additive extrude",
        "PartDesignWorkbench", "Open a document. Extrude a profile to add material."),
    "PartDesign_Pocket": (
        "Pocket (Extrude: Subtract)", "pocket;cut;extruded cut;cut-extrude;subtractive extrude",
        "PartDesignWorkbench", "Open a document with a target Body. Choose a profile to remove material."),
    "PartDesign_Revolution": (
        "Revolution (Add)", "revolve;revolved boss;revolved boss/base", "PartDesignWorkbench",
        "Open a document and select a profile. Revolve it to add material."),
    "PartDesign_Groove": (
        "Groove (Revolved Cut)", "groove;revolved cut;revolve cut", "PartDesignWorkbench",
        "Open a document with a target Body and select a profile. Revolve it to remove material."),
    "PartDesign_Pattern": (
        "Pattern (Linear / Circular)", "linear pattern;circular pattern;polar pattern",
        "PartDesignWorkbench", "Open a document with a Body and choose features to repeat."),
    "Part_NamedParameters": (
        "Named parameters", "parameters;expressions;variables", "PartWorkbench",
        "Select one native Part or its marked parameter set, with no pending edit transaction."),
    "Assembly_Insert": (
        "Insert Component", "assembly;insert component", "AssemblyWorkbench",
        "Create or activate an Assembly in the document, then insert a component."),
}


def catalog():
    """Snapshot labels/shortcuts; availability is checked live only for the selected row."""
    rows = []
    for name in set(Gui.Command.listAll()).union(ALIASES):
        if name == "Std_CommandSearch":
            continue
        command = Gui.Command.get(name)
        info = command.getInfo() if command else {}
        title = info.get("menuText", name).replace("&", "")
        aliases, workbench, guidance = "", "", info.get("toolTip", "")
        if name in ALIASES:
            title, aliases, workbench, guidance = ALIASES[name]
            title, guidance = _tr(title), _tr(guidance)
        else:
            actions = command.getAction() if command else []
            if actions:
                title = actions[0].text().replace("&", "") or title
        shortcut = command.getShortcut() if command else ""
        rows.append((name, title, aliases, workbench, guidance, shortcut))
    return sorted(rows, key=lambda row: (row[1].casefold(), row[0]))


def matching_rows(rows, query):
    terms = query.casefold().split()
    matches = [row for row in rows if all(
        term in " ".join((row[0], row[1], row[2], row[5])).casefold() for term in terms)]
    # An exact legacy command or familiar alias should precede incidental matches.
    exact = query.strip().casefold()
    return sorted(matches, key=lambda row: (
        not (exact and exact in (row[0].casefold(), row[0].split("_", 1)[-1].casefold())),
        not (exact and exact in row[2].casefold().split(";")),
        exact != row[1].casefold(),
        row[1].casefold(), row[0]))


def availability(row):
    name, _, _, workbench, guidance, _ = row
    if Gui.Control.activeDialog():
        return False, _tr("Finish or cancel the active task, then search again.")
    if workbench and Gui.activeWorkbench().name() != workbench:
        target = Gui.listWorkbenches().get(workbench)
        if target is None:
            return False, _tr("The required workbench is not installed.")
        return False, _tr("Switch workbench to continue:") + " " + target.MenuText
    command = Gui.Command.get(name)
    if command is None:
        return False, _tr("This command is not loaded in this installation.")
    try:
        if command.isActive():
            return True, _tr("Available")
    except Exception as error:
        return False, str(error)
    return False, guidance or _tr("Unavailable in the current context. Check the active document and selection.")


class CommandSearchDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CommandSearchDialog")
        self.setWindowTitle(_tr("Command search"))
        self.resize(760, 510)
        layout = QtWidgets.QVBoxLayout(self)
        self.query = QtWidgets.QLineEdit()
        self.query.setAccessibleName(_tr("Search commands"))
        self.query.setPlaceholderText(_tr("Search names, aliases or shortcuts (e.g. Pocket, Cut-Extrude)"))
        layout.addWidget(self.query)
        self.results = QtWidgets.QTreeWidget()
        self.results.setHeaderLabels([_tr("Command"), _tr("Shortcut")])
        self.results.setRootIsDecorated(False)
        self.results.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.results.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.results)
        self.detail = QtWidgets.QLabel()
        self.detail.setWordWrap(True)
        self.detail.setTextFormat(QtCore.Qt.PlainText)
        self.detail.setMinimumHeight(85)
        layout.addWidget(self.detail)
        buttons = QtWidgets.QHBoxLayout()
        self.runButton = QtWidgets.QPushButton(_tr("Run command"))
        self.switchButton = QtWidgets.QPushButton(_tr("Switch workbench"))
        self.refreshButton = QtWidgets.QPushButton(_tr("Refresh"))
        self.closeButton = QtWidgets.QPushButton(_tr("Close"))
        for button in (self.runButton, self.switchButton, self.refreshButton, self.closeButton):
            button.setAutoDefault(False)
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.query.textChanged.connect(self.filter)
        self.results.currentItemChanged.connect(self.describe)
        self.results.itemActivated.connect(lambda *args: self.runSelected())
        self.runButton.clicked.connect(self.runSelected)
        self.switchButton.clicked.connect(self.switchWorkbench)
        self.refreshButton.clicked.connect(self.refresh)
        self.closeButton.clicked.connect(self.reject)
        self.query.installEventFilter(self)
        self.results.installEventFilter(self)
        self.refresh()

    def refresh(self):
        self.rows = catalog()
        self.filter()

    def filter(self, *args):
        self.results.clear()
        for row in matching_rows(self.rows, self.query.text()):
            item = QtWidgets.QTreeWidgetItem([row[1], row[5]])
            item.setData(0, QtCore.Qt.UserRole, row[0])
            self.results.addTopLevelItem(item)
        self.results.setCurrentItem(self.results.topLevelItem(0))
        self.describe()

    def selected(self):
        item = self.results.currentItem()
        name = item.data(0, QtCore.Qt.UserRole) if item else None
        return next((row for row in self.rows if row[0] == name), None)

    def describe(self, *args):
        row = self.selected()
        active, reason = availability(row) if row else (False, _tr("No matching commands."))
        self.runButton.setEnabled(active)
        self.switchButton.setEnabled(bool(row and row[3]
            and row[3] in Gui.listWorkbenches()
            and Gui.activeWorkbench().name() != row[3]
            and not Gui.Control.activeDialog()))
        self.detail.setText("\n".join((row[1], row[4], reason)) if row else reason)

    def switchWorkbench(self):
        row = self.selected()
        if not row or not self.switchButton.isEnabled():
            return
        try:
            Gui.activateWorkbench(row[3])
            name = row[0]
            self.refresh()
            for index in range(self.results.topLevelItemCount()):
                item = self.results.topLevelItem(index)
                if item.data(0, QtCore.Qt.UserRole) == name:
                    self.results.setCurrentItem(item)
                    break
        except Exception as error:
            self.detail.setText(str(error))
        self.query.setFocus()

    def runSelected(self):
        row = self.selected()
        if not row:
            return
        active, _ = availability(row)
        if not active:
            self.describe()
            return
        # Release focus before opening the existing task/editor. Its native command
        # owns transactions, selection validation, undo and macro recording.
        self.hide()
        try:
            Gui.runCommand(row[0], 0)
        except Exception as error:
            self.show()
            self.detail.setText(str(error))

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                self.runSelected()
                return True
            if obj is self.query and event.key() in (QtCore.Qt.Key_Down, QtCore.Qt.Key_Up):
                current = self.results.indexOfTopLevelItem(self.results.currentItem())
                step = 1 if event.key() == QtCore.Qt.Key_Down else -1
                index = max(0, min(self.results.topLevelItemCount() - 1, current + step))
                self.results.setCurrentItem(self.results.topLevelItem(index))
                return True
        return super().eventFilter(obj, event)


_dialog = None


class CommandSearch:
    def GetResources(self):
        return {"MenuText": _tr("Command search..."), "Accel": "Ctrl+K",
                "ToolTip": _tr("Find commands by name, familiar alias or shortcut")}

    def IsActive(self):
        return True

    def Activated(self):
        global _dialog
        if _dialog is None:
            _dialog = CommandSearchDialog(Gui.getMainWindow())
        else:
            _dialog.refresh()
        _dialog.show()
        _dialog.raise_()
        _dialog.activateWindow()
        _dialog.query.setFocus()
        _dialog.query.selectAll()


def registerCommand():
    Gui.addCommand("Std_CommandSearch", CommandSearch())
