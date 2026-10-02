# SPDX-License-Identifier: LGPL-2.1-or-later
"""Optional ribbon projection of native workbench command actions."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets

PARAM = "User parameter:BaseApp/Preferences/General"
DESIGN_TABS = ("Home", "Modeling", "Surface", "Sketch", "Mesh", "View")
DESIGN_WORKBENCHES = {
    "Home": "PartDesignWorkbench", "Modeling": "PartDesignWorkbench",
    "Surface": "SurfaceWorkbench", "Sketch": "SketcherWorkbench", "Mesh": "MeshWorkbench",
}
STANDARD = {"File", "Edit", "Clipboard", "Workbench", "Macro", "View", "Individual Views", "Structure", "Help"}
SMALL_BUTTON_SIZE = 24
GRID_SPACING = 2
GRID_ROWS = 3
PRIMARY_WIDTH = GRID_HEIGHT = GRID_ROWS * SMALL_BUTTON_SIZE + (GRID_ROWS - 1) * GRID_SPACING
# Presentation priority only: every operation still uses its native QAction.
PRIMARY_COMMANDS = {
    "Std_NewComponentDocument", "Std_Open", "Std_Save", "Std_Part",
    "PartDesign_NewSketch", "Sketcher_NewSketch", "Sketcher_EditSketch",
    "PartDesign_Extrude", "PartDesign_Revolution", "PartDesign_Pattern", "PartDesign_Fillet",
    "Sketcher_CreatePolyline", "Sketcher_CompLine", "Sketcher_CreateRectangle",
    "Sketcher_CompCreateRectangles", "Sketcher_Dimension",
    "Std_ViewFitAll", "Draft_Line", "Draft_Wire", "Path_Job", "CAM_Job",
    "TechDraw_NewPageDefault", "Surface_ExtendFace", "Mesh_Import",
}
DIMENSION_CHOICES = (
    "Sketcher_Dimension", "Sketcher_ConstrainDistanceY", "Sketcher_ConstrainDistanceX",
    "Sketcher_ConstrainAngle", "Sketcher_ConstrainRadius", "Sketcher_ConstrainDiameter",
    "Sketcher_ConstrainDistance", "Sketcher_ConstrainRadiam", "Sketcher_ConstrainLock",
    "Sketcher_ConstrainSnellsLaw",
)
COMMAND_FAMILIES = (
    ("Sketcher_Dimension",
     DIMENSION_CHOICES + ("Sketcher_CompDimensionTools", "Sketcher_CompConstrainRadDia"), DIMENSION_CHOICES),
    ("PartDesign_AdditiveLoft", ("PartDesign_AdditiveLoft", "PartDesign_SubtractiveLoft"),
     ("PartDesign_AdditiveLoft", "PartDesign_SubtractiveLoft")),
    ("PartDesign_AdditivePipe", ("PartDesign_AdditivePipe", "PartDesign_SubtractivePipe"),
     ("PartDesign_AdditivePipe", "PartDesign_SubtractivePipe")),
    ("PartDesign_AdditiveHelix", ("PartDesign_AdditiveHelix", "PartDesign_SubtractiveHelix"),
     ("PartDesign_AdditiveHelix", "PartDesign_SubtractiveHelix")),
)
_ribbon = None


def projected_commands(commands):
    """Collapse related choices without changing native toolbar preferences."""
    emitted = set()
    for name in commands:
        if name == "Separator":
            continue
        family = next((item for item in COMMAND_FAMILIES if name in item[1]), None)
        root, choices = (family[0], family[2]) if family else (name, None)
        if root not in emitted:
            emitted.add(root)
            yield root, choices


def native_actions(name):
    command = Gui.Command.get(name)
    return command.getAction() if command else []


class RibbonButton(QtWidgets.QToolButton):
    """Keep a presentation caption separate from the shared native action text."""
    def __init__(self, caption=None, parent=None):
        super().__init__(parent)
        self.caption = caption

    def setDefaultAction(self, action):
        super().setDefaultAction(action)
        self.restore_caption()

    def restore_caption(self):
        if self.caption:
            self.setText(self.caption)
            self.setAccessibleName(self.caption.replace("\n", " "))

    def actionEvent(self, event):
        super().actionEvent(event)
        if self.caption and event.type() in (QtCore.QEvent.ActionAdded, QtCore.QEvent.ActionChanged):
            self.restore_caption()


def tr(text):
    return App.Qt.translate("PlusRibbon", text)


def available_modes():
    """Installed/registered workbenches, including addons, regardless of selector filtering."""
    workbenches = Gui.listWorkbenches()
    modes = [("Design", "PartDesignWorkbench")] if "PartDesignWorkbench" in workbenches else []
    combined = set(DESIGN_WORKBENCHES.values()) | {"NoneWorkbench", "StartWorkbench"}
    aliases = {"DraftWorkbench": "Draft", "CAMWorkbench": "CAM", "PathWorkbench": "CAM",
               "FemWorkbench": "FEM", "FEMWorkbench": "FEM", "AssemblyWorkbench": "Assembly",
               "TechDrawWorkbench": "Drawing"}
    for name, wb in workbenches.items():
        if name in combined:
            continue
        label = aliases.get(name, getattr(wb, "MenuText", name.removesuffix("Workbench"))).replace("&", "")
        if "print" in (name + label).lower() and "3" in name + label:
            label = "3D Printing"
        modes.append((label, name))
    return modes


class Ribbon(QtCore.QObject):
    def __init__(self):
        super().__init__(Gui.getMainWindow())
        self.window = Gui.getMainWindow()
        self.enabled = False
        self.changing = False
        self.render_timer = QtCore.QTimer(self)
        self.render_timer.setSingleShot(True)
        self.render_timer.timeout.connect(self.render)
        self.saved_bars = {}
        self.mode_name = "Design"
        self.toolbar = QtWidgets.QToolBar(tr("Plus Ribbon"), self.window)
        self.toolbar.setObjectName("FreeCADPlusRibbon")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("PlusRibbonContents")
        layout = QtWidgets.QVBoxLayout(self.widget)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(2)
        header = QtWidgets.QHBoxLayout()
        self.modes = QtWidgets.QComboBox()
        self.modes.setObjectName("PlusRibbonMode")
        self.modes.setAccessibleName(tr("Mode"))
        self.modes.setToolTip(tr("Choose a workflow mode"))
        self.modes.setMinimumWidth(150)
        header.addWidget(self.modes)
        self.tabs = QtWidgets.QTabBar()
        self.tabs.setObjectName("PlusRibbonTabs")
        self.tabs.setExpanding(False)
        self.tabs.setDrawBase(False)
        self.tabs.setUsesScrollButtons(True)
        header.addWidget(self.tabs, 1)
        layout.addLayout(header)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setMinimumWidth(0)
        self.scroll.setFixedHeight(GRID_HEIGHT + self.widget.fontMetrics().height() + 6
                                   + self.widget.style().pixelMetric(QtWidgets.QStyle.PM_ScrollBarExtent))
        layout.addWidget(self.scroll)
        self.widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.toolbar.addWidget(self.widget)
        self.window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.toolbar.toggleViewAction().setVisible(False)
        self.toolbar.hide()
        self.modes.currentIndexChanged.connect(self.mode_changed)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.window.workbenchActivated.connect(self.workbench_changed)

    def current_tab(self):
        return self.tabs.tabData(self.tabs.currentIndex())

    def apply(self):
        params = App.ParamGet(PARAM)
        if not params.GetString("ToolbarUIStyle", ""):
            # Initialize the choice so older native General pages also display
            # the new default consistently. Preserve an explicit Classic choice.
            params.SetString("ToolbarUIStyle", "Plus")
        plus = params.GetString("ToolbarUIStyle", "Plus") == "Plus"
        if plus == self.enabled:
            return
        self.enabled = plus
        if plus:
            if Gui.activeWorkbench().name() in ("NoneWorkbench", "StartWorkbench"):
                self.activate("PartDesignWorkbench")
            self.workbench_changed(Gui.activeWorkbench().name())
            self.toolbar.show()
        else:
            self.toolbar.hide()
            self.restore_bars()

    def hide_bars(self):
        wb = Gui.activeWorkbench().name()
        saved = self.saved_bars.setdefault(wb, {})
        for bar in self.window.findChildren(QtWidgets.QToolBar):
            if bar == self.toolbar or not bar.toggleViewAction().isVisible():
                continue
            saved[bar.objectName()] = not bar.isHidden()
            # Native ToolBarManager.saveState skips unavailable toggle actions,
            # preserving Classic visibility preferences during workbench switches.
            bar.toggleViewAction().setVisible(False)
            bar.hide()

    def restore_bars(self):
        saved = self.saved_bars.get(Gui.activeWorkbench().name(), {})
        for bar in self.window.findChildren(QtWidgets.QToolBar):
            if bar.objectName() in saved:
                bar.toggleViewAction().setVisible(True)
                bar.setVisible(saved[bar.objectName()])

    def configure(self, mode, tab="Home"):
        self.changing = True
        try:
            self.mode_name = mode
            self.modes.clear()
            for label, name in available_modes():
                self.modes.addItem(tr(label), (label, name))
            self.modes.setCurrentIndex(next((i for i in range(self.modes.count())
                                            if self.modes.itemData(i)[0] == mode), 0))
            while self.tabs.count():
                self.tabs.removeTab(0)
            labels = DESIGN_TABS if mode == "Design" else ("Home", "Tools", "View")
            for label in labels:
                index = self.tabs.addTab(tr(label))
                self.tabs.setTabData(index, label)
                required = DESIGN_WORKBENCHES.get(label) if mode == "Design" else None
                if required and required not in Gui.listWorkbenches():
                    self.tabs.setTabEnabled(index, False)
            self.tabs.setCurrentIndex(labels.index(tab) if tab in labels else 0)
        finally:
            self.changing = False

    def activate(self, workbench):
        if workbench == Gui.activeWorkbench().name():
            return True
        if Gui.Control.activeDialog():
            return False
        self.restore_bars()
        self.changing = True
        try:
            Gui.activateWorkbench(workbench)
        finally:
            self.changing = False
        return Gui.activeWorkbench().name() == workbench

    def mode_changed(self, index):
        if self.changing or index < 0:
            return
        mode, wb = self.modes.itemData(index)
        if not self.activate(wb):
            self.configure(self.mode_name, self.current_tab())
            self.modes.setToolTip(tr("Finish the current task before changing modes."))
            return
        self.configure(mode)
        self.render()

    def tab_changed(self, index):
        if self.changing or index < 0:
            return
        tab = self.current_tab()
        wb = DESIGN_WORKBENCHES.get(tab) if self.mode_name == "Design" else None
        if wb and wb in Gui.listWorkbenches() and not self.activate(wb):
            # View is still available while a native task owns another workbench.
            self.configure(self.mode_name, "View")
        self.render()

    def workbench_changed(self, name):
        if not self.enabled or self.changing:
            return
        if name in set(DESIGN_WORKBENCHES.values()):
            tab = {"SurfaceWorkbench": "Surface", "SketcherWorkbench": "Sketch", "MeshWorkbench": "Mesh",
                   }.get(name, "Home")
            self.configure("Design", tab)
        else:
            mode = next((label for label, wb in available_modes() if wb == name), "Design")
            self.configure(mode)
        self.render()

    def groups(self):
        bars = Gui.activeWorkbench().getToolbarItems()
        tab = self.current_tab()
        if tab == "Home":
            groups = [(name, bars.get(name, [])) for name in ("File", "Edit", "Clipboard", "Structure")]
            groups[0] = ("File", ["Std_NewComponentDocument", "Std_Open", "Std_Save", "Std_SaveAs", "Std_Import", "Std_Export"])
            groups[1] = ("Edit", ["Std_Undo", "Std_Redo", "Std_Delete", "Std_Refresh", "Std_DlgPreferences"])
            groups[3] = ("Structure", ["Std_ComponentStructure", "Std_Part", "Std_Group", "Std_LinkActions", "PartDesign_AddReferenceObject"])
            if self.mode_name == "Design":
                groups.append(("Sketch", ["PartDesign_NewSketch", "Sketcher_MapSketch", "Sketcher_EditSketch", "Sketcher_ValidateSketch"]))
                groups.append(("Tools", ["Std_CommandSearch", "Std_Measure", "Std_MassProperties"]))
            groups.append(("Help", bars.get("Help", [])))
            return groups
        if tab == "View":
            groups = [(name, commands) for name, commands in bars.items()
                      if name in ("View", "Individual Views")]
            groups.append(("Display", ["Std_EntitySelectionFilter", "Std_ToolBarMenu", "Std_DockViewMenu", "Std_ViewStatusBar"]))
            return groups
        if self.mode_name == "Design" and tab == "Modeling":
            order = ("Part Design Modeling Features", "Part Design Transformation Features",
                     "Part Design Dress-Up Features", "Part Design Helper Features")
            return [(name, bars[name]) for name in order if name in bars]
        return [(name, commands) for name, commands in bars.items() if name not in STANDARD]

    def render(self):
        if not self.enabled:
            return
        try:
            Gui.activeWorkbench().name()
        except AttributeError:
            # Native Sketcher activation can emit workbenchActivated before the
            # Python workbench wrapper receives its __Workbench__ handle.
            self.render_timer.start(100)
            return
        self.hide_bars()
        page = QtWidgets.QWidget(self.scroll)
        layout = QtWidgets.QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for title, commands in self.groups():
            group = QtWidgets.QWidget(page)
            group.setObjectName("PlusRibbonGroup")
            group_layout = QtWidgets.QVBoxLayout(group)
            group_layout.setContentsMargins(5, 2, 5, 2)
            group_layout.setSpacing(2)
            grid = QtWidgets.QGridLayout()
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setSpacing(GRID_SPACING)
            grid.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
            buttons = []
            for command_name, choices in projected_commands(commands):
                actions = native_actions(command_name)
                if not actions:
                    continue
                captions = {"Std_NewComponentDocument": tr("New file"),
                            "Std_Part": tr("Add part"), "Sketcher_Dimension": tr("Auto\ndimension")}
                button = RibbonButton(captions.get(command_name), group)
                button.setObjectName("Ribbon_" + command_name)
                button.setAutoRaise(True)
                button.setDefaultAction(actions[0])
                primary = command_name in PRIMARY_COMMANDS
                button.setProperty("ribbonPriority", "primary" if primary else "secondary")
                button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon if primary else QtCore.Qt.ToolButtonIconOnly)
                button.setIconSize(QtCore.QSize(32, 32) if primary else QtCore.QSize(20, 20))
                if primary:
                    button.setFixedSize(PRIMARY_WIDTH, GRID_HEIGHT)
                else:
                    button.setFixedSize(SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE)
                if choices:
                    actions = []
                    for name in choices:
                        available = native_actions(name)
                        if available:
                            actions.append(available[0])
                if len(actions) > 1:
                    menu = QtWidgets.QMenu(button)
                    for action in actions:
                        menu.addAction(action)
                    button.setMenu(menu)
                    button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
                buttons.append((button, primary))
            if title == "Help" and buttons:
                # Rare help operations share one icon; choices retain native states.
                menu_button = QtWidgets.QToolButton(group)
                menu_button.setObjectName("Ribbon_Group_Help")
                menu_button.setAutoRaise(True)
                menu_button.setText(tr("Help"))
                menu_button.setToolTip(tr("Help"))
                menu_button.setIcon(buttons[0][0].icon())
                menu_button.setIconSize(QtCore.QSize(20, 20))
                menu_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
                menu_button.setFixedSize(SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE)
                menu_button.setProperty("ribbonPriority", "secondary")
                menu = QtWidgets.QMenu(menu_button)
                for button, _ in buttons:
                    menu.addAction(button.defaultAction())
                    if button.menu():
                        for action in button.menu().actions():
                            if action not in menu.actions():
                                menu.addAction(action)
                    button.deleteLater()
                menu_button.setMenu(menu)
                menu_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
                buttons = [(menu_button, False)]
            if not buttons:
                group.deleteLater()
                continue
            primaries = [button for button, primary in buttons if primary]
            secondary = [button for button, primary in buttons if not primary]
            for column, button in enumerate(primaries):
                grid.addWidget(button, 0, column, GRID_ROWS, 1)
            for index, button in enumerate(secondary):
                grid.addWidget(button, index % GRID_ROWS, len(primaries) + index // GRID_ROWS)
            for row in range(GRID_ROWS):
                grid.setRowMinimumHeight(row, SMALL_BUTTON_SIZE)
            group_layout.addLayout(grid)
            caption = {"Part Design Modeling Features": "Modeling", "Part Design Transformation Features": "Transformation",
                       "Part Design Dress-Up Features": "Dress-Up", "Part Design Helper Features": "Helpers"}.get(title, title)
            label = QtWidgets.QLabel(tr(caption) if caption != title else App.Qt.translate("Workbench", title), group)
            label.setToolTip(label.text())
            caption_width = max(grid.sizeHint().width(),
                                min(PRIMARY_WIDTH, label.fontMetrics().horizontalAdvance(label.text()) + 2))
            label.setText(label.fontMetrics().elidedText(label.text(), QtCore.Qt.ElideRight, caption_width))
            label.setFixedHeight(label.fontMetrics().height())
            label.setAlignment(QtCore.Qt.AlignCenter)
            group_layout.addWidget(label)
            group.setFixedHeight(GRID_HEIGHT + label.fontMetrics().height() + 6)
            layout.addWidget(group, 0, QtCore.Qt.AlignTop)
            separator = QtWidgets.QFrame(page)
            separator.setFrameShape(QtWidgets.QFrame.VLine)
            separator.setFixedHeight(group.height())
            layout.addWidget(separator, 0, QtCore.Qt.AlignTop)
        layout.addStretch()
        old = self.scroll.takeWidget()
        self.scroll.setWidget(page)
        if old:
            old.deleteLater()
        Gui.Command.update()


def apply_preferences():
    global _ribbon
    if _ribbon is None:
        _ribbon = Ribbon()
    _ribbon.apply()


def install():
    QtCore.QTimer.singleShot(0, apply_preferences)
