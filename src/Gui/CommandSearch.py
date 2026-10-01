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
    "Sketcher_CopyReusable": (
        "Copy reusable sketch", "copy sketch;reuse profile", "SketcherWorkbench",
        "Select one whole, free root sketch with internal constraints only."),
    "Std_MoveOccurrenceOnce": (
        "Move or copy occurrence", "move component;copy component;duplicate occurrence;translate;rotate component", "",
        "Select one whole unconstrained Link occurrence in the tree."),
    "Std_DocumentUpdates": (
        "Document updates", "defer;recompute;failed;pending", "",
        "Open a document to review native update state and affected objects."),
    "Part_ManufacturingExport": (
        "Manufacturing export", "export stl;mesh export", "PartWorkbench",
        "Select current solid objects or supported whole occurrences for STL export."),
    "CAM_MeshPreparation": (
        "Review CAM mesh", "mesh normals;mesh preparation", "CAMWorkbench",
        "Select one whole imported root Mesh feature to review its dimensions and topology."),
}


# Bundled plain-text guidance: available offline, without executing commands or
# loading workbenches. These are workflow hints, not a second eligibility engine.
HELP = {
    "PartDesign_Extrude": (
        "Choose a profile in the editor. Review Add or Subtract, the target Body, direction and extent. "
        "Preview the result before OK. Cancel abandons the active task; Undo reverses an accepted feature. "
        "A visible preview does not prove that a changed upstream profile will recompute successfully."),
    "PartDesign_Pad": (
        "Pad opens the shared Extrude editor with Add selected. Choose a profile and review the target Body, "
        "extent and direction. Check the preview before OK; Cancel abandons the task. "
        "Use Undo after acceptance. The profile and Body rules are checked by the existing editor."),
    "PartDesign_Pocket": (
        "Pocket opens the shared Extrude editor with Subtract selected. Choose a profile and a Body with "
        "material to cut. Review extent and direction so the cut intersects the intended material. "
        "Check the preview before OK; Cancel abandons the task. Use Undo after acceptance."),
    "PartDesign_Revolution": (
        "Choose a profile and revolution axis. Review angle, signed start offset and direction in the "
        "existing editor. This entry adds material. Check the preview before OK; Cancel abandons the task. "
        "Use Undo after acceptance. Invalid profiles or self-intersections still require repair."),
    "PartDesign_Groove": (
        "Choose a profile, target Body and revolution axis. Review angle, signed start offset and direction. "
        "This entry removes material. Check the preview before OK; Cancel abandons the task. "
        "Use Undo after acceptance. The cut must intersect the intended material."),
    "PartDesign_Pattern": (
        "Choose features in the Body, then Linear or Circular in the combined Pattern editor. "
        "Review direction or axis, spacing or angle, and occurrence count. Inspect the preview before OK. "
        "Cancel abandons the task; Undo reverses acceptance. Invalid transformed geometry remains an error."),
    "Part_NamedParameters": (
        "Select a native Part or its marked parameter set. Define length or angle values with valid names "
        "and native expressions. Review units and dependents before changing or renaming a parameter. "
        "Use Undo for committed changes. Cross-document publication and configuration management are not included."),
    "Assembly_Insert": (
        "Create or activate an Assembly first, then use the native insertion editor to choose a component. "
        "Review its source document and placement. Keep referenced source files available when reopening. "
        "This search entry does not create an Assembly or substitute for the insertion editor's validation."),
    "Sketcher_CopyReusable": (
        "Select one whole free sketch at the document root. Attached sketches, Body members, external geometry "
        "and expressions are outside this copy workflow. Set offsets in source sketch axes and rotation about "
        "its normal. Preview, then create the independent copy. Internal constraints and construction roles "
        "are preserved. Cancel creates nothing; Undo removes the accepted copy. Partial copying is not included."),
    "Std_MoveOccurrenceOnce": (
        "Select a whole unconstrained same-document Link to a solid or Body, then choose world or occurrence axes. "
        "Choose Translate with offsets, or Rotate with an axis, angle and pivot. Move changes the selected "
        "placement; Copy creates one new occurrence in the same container sharing its definition, appearance "
        "and visibility. Source edits affect both copies. Review and preview before confirming. Cancel creates "
        "nothing; Undo reverses one action. Independent definitions, constrained motion and snapping are not included."),
    "Std_DocumentUpdates": (
        "Review pending and failed objects and their loaded dependencies. Select a listed object to locate it. "
        "Deferring updates leaves results potentially stale; Update document explicitly recomputes the document. "
        "Repair failed inputs and update again before export. This panel does not identify a guaranteed first "
        "cause or repair references automatically. Closing the panel does not reverse a completed update."),
    "Part_ManufacturingExport": (
        "Select current supported solids or whole occurrences. Review the explicit export list and mesh quality, "
        "then choose the destination. The pilot writes STL in millimetres using world coordinates. Repair and "
        "recompute stale or failed inputs first. Export does not change model geometry. Written files are not "
        "removed by document Undo. Other formats and unit conversions are outside this workflow."),
    "CAM_MeshPreparation": (
        "Select a whole plain root Mesh feature with at most 200,000 triangles. Review millimetre dimensions, "
        "boundary/nonmanifold edges, components and normals. A single closed consistently inward mesh can be "
        "copied with reversed normals. The source and existing jobs stay unchanged; Undo removes the copy. "
        "Closing review makes no repair. Self-intersections, welding and unit conversion are not checked here."),
}


def help_text(row):
    """Return local guidance, including an honest fallback for uncurated commands."""
    text = HELP.get(row[0])
    return _tr(text) if text else _tr(
        "No extended local guide is bundled for this command. The command's own description is shown above. "
        "Its editor owns input validation. Review its task controls before accepting changes.")


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
            return True, _tr("Available to open. The command checks its inputs when run.")
    except Exception as error:
        return False, str(error)
    return False, guidance or _tr("Unavailable in the current context. Check the active document and selection.")


class CommandSearchDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CommandSearchDialog")
        self.setWindowTitle(_tr("Command search"))
        self.resize(760, 600)
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
        self.results.setAccessibleName(_tr("Matching commands"))
        self.results.setAccessibleDescription(_tr("Use Up and Down to select; Enter runs the selected command."))
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.results)
        self.detail = QtWidgets.QTextBrowser()
        self.detail.setAccessibleName(_tr("Command guidance and availability"))
        self.detail.setOpenLinks(False)
        self.detail.setOpenExternalLinks(False)
        self.detail.setTabChangesFocus(True)
        self.detail.setMinimumSize(0, 0)
        self.splitter.addWidget(self.detail)
        self.splitter.setChildrenCollapsible(False)
        layout.addWidget(self.splitter, 1)
        buttons = QtWidgets.QGridLayout()
        self.runButton = QtWidgets.QPushButton(_tr("&Run command"))
        self.switchButton = QtWidgets.QPushButton(_tr("&Switch workbench"))
        self.refreshButton = QtWidgets.QPushButton(_tr("Re&fresh"))
        self.helpButton = QtWidgets.QPushButton(_tr("Local &help (F1)"))
        self.helpButton.setCheckable(True)
        self.resetButton = QtWidgets.QPushButton(_tr("Reset &layout"))
        self.closeButton = QtWidgets.QPushButton(_tr("&Close"))
        controls = (self.runButton, self.switchButton, self.refreshButton,
                    self.helpButton, self.resetButton, self.closeButton)
        for index, button in enumerate(controls):
            button.setAutoDefault(False)
            buttons.addWidget(button, index // 3, index % 3)
        layout.addLayout(buttons)
        self.query.textChanged.connect(self.filter)
        self.results.currentItemChanged.connect(self.describe)
        self.results.itemActivated.connect(lambda *args: self.runSelected())
        self.runButton.clicked.connect(self.runSelected)
        self.switchButton.clicked.connect(self.switchWorkbench)
        self.refreshButton.clicked.connect(self.refresh)
        self.closeButton.clicked.connect(self.reject)
        self.helpButton.toggled.connect(self.showHelp)
        self.resetButton.clicked.connect(self.resetLayout)
        self.query.setAccessibleDescription(_tr("Search names, aliases or shortcuts. F1 opens local help; Ctrl+L returns here."))
        order = (self.query, self.results, self.detail) + controls
        for first, second in zip(order, order[1:]):
            self.setTabOrder(first, second)
        for widget in order + (self, self.detail.viewport(), self.results.viewport()):
            widget.installEventFilter(self)
        self.contextTimer = QtCore.QTimer(self)
        self.contextTimer.setInterval(750)
        self.contextTimer.timeout.connect(self.describe)
        self.refresh()
        self.splitter.setSizes([260, 180])

    def showEvent(self, event):
        super().showEvent(event)
        self.contextTimer.start()

    def hideEvent(self, event):
        self.contextTimer.stop()
        super().hideEvent(event)

    def focusSearch(self):
        self.query.setFocus()
        self.query.selectAll()

    def showHelp(self, checked):
        self.describe()
        if checked:
            self.detail.setFocus()
        else:
            self.focusSearch()

    def resetLayout(self):
        # Recover this window only; never reset global fonts, shortcuts or model state.
        self.helpButton.setChecked(False)
        screen = self.screen() or QtWidgets.QApplication.primaryScreen()
        area = screen.availableGeometry()
        self.resize(min(760, area.width()), min(600, area.height()))
        self.move(area.center() - self.rect().center())
        self.splitter.setSizes([260, 180])
        self.focusSearch()

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
        text = reason
        if row:
            document = App.ActiveDocument
            context = _tr("Active document:") + " " + (document.Label if document else _tr("None"))
            text = "\n\n".join((row[1], row[4], reason, context))
            if row[5]:
                text += "\n" + _tr("Current shortcut:") + " " + row[5]
            if self.helpButton.isChecked():
                text += "\n\n" + _tr("Local workflow guide") + "\n" + help_text(row)
                text += "\n\n" + _tr("Keyboard: F1 toggles help; Ctrl+L returns to search. "
                    "Tab moves between controls. Use arrows or Page Up/Down in this pane to read. Escape closes search.")
        # Preserve reading/selection position when periodic context checks find no change.
        if self.detail.toPlainText() != text:
            self.detail.setPlainText(text)

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
            self.detail.setPlainText(str(error))
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
            self.detail.setPlainText(str(error))

    def eventFilter(self, obj, event):
        if event.type() in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress):
            help_key = event.key() == QtCore.Qt.Key_F1 and event.modifiers() == QtCore.Qt.NoModifier
            search_key = event.key() == QtCore.Qt.Key_L and event.modifiers() == QtCore.Qt.ControlModifier
            if help_key or search_key:
                # Own these keys only inside this palette, ahead of main-window
                # help/navigation bindings; no global shortcut customization.
                event.accept()
                if event.type() == QtCore.QEvent.KeyPress:
                    self.helpButton.toggle() if help_key else self.focusSearch()
                return True
        if event.type() == QtCore.QEvent.KeyPress:
            if obj in (self.query, self.results) and event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
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
