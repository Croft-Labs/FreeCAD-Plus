# SPDX-License-Identifier: LGPL-2.1-or-later
"""Optional ribbon projection of native workbench command actions."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets

PARAM = "User parameter:BaseApp/Preferences/General"
DESIGN_TABS = ("Home", "Modeling", "Surface", "Sketch", "Assembly", "Mesh", "View")
DESIGN_WORKBENCHES = {
    "Home": "PartDesignWorkbench", "Modeling": "PartDesignWorkbench",
    "Surface": "SurfaceWorkbench", "Sketch": "SketcherWorkbench", "Mesh": "MeshWorkbench",
    "Assembly": "AssemblyWorkbench",
}
STANDARD = {"File", "Edit", "Clipboard", "Workbench", "Macro", "View", "Individual Views", "Structure", "Help"}
SMALL_BUTTON_SIZE = 24
GRID_SPACING = 2
GRID_ROWS = 6  # Two cells per small button, three per medium button.
PRIMARY_WIDTH = GRID_HEIGHT = 3 * SMALL_BUTTON_SIZE + 2 * GRID_SPACING
MEDIUM_HEIGHT = GRID_HEIGHT // 2
FULL_ICON_SIZE = 40
MEDIUM_ICON_SIZE = FULL_ICON_SIZE // 2
SMALL_ICON_SIZE = 16
COMMON_GROUPS = (
    ("File", ("Std_New", "Std_Open", "Std_Save", "Std_SaveAs")),
    ("Edit", ("Std_Undo", "Std_Redo", "Std_Refresh")),
    ("Clipboard", ("Std_Cut", "Std_Copy", "Std_Paste")),
)
HOME_GROUPS = (
    ("Main", ("Std_NewComponent", "Std_Part")),
    ("Modeling", ("PartDesign_Extrude", "PartDesign_Revolution", "PartDesign_Fillet")),
    ("Sketch", ("PartDesign_NewSketch", "Part_CoordinateSystem")),
)
COORDINATE_CHOICES = ("Part_CoordinateSystem", "Part_DatumPlane", "Part_DatumLine", "Part_DatumPoint")
# Presentation priority only: every operation still uses its native QAction.
PRIMARY_COMMANDS = {
    "Std_New", "Std_Open", "Std_Save", "Std_Part",
    "PartDesign_NewSketch", "Sketcher_NewSketch", "Sketcher_EditSketch",
    "PartDesign_Extrude", "PartDesign_Revolution", "PartDesign_Pattern", "PartDesign_Fillet",
    "Sketcher_CreatePolyline", "Sketcher_CompLine", "Sketcher_CreateRectangle",
    "Sketcher_CompCreateRectangles", "Sketcher_Dimension",
    "Std_ViewFitAll", "Draft_Line", "Draft_Wire", "Path_Job", "CAM_Job",
    "TechDraw_PageDefault", "Surface_ExtendFace", "Mesh_Import",
}
ICON_FALLBACKS = {
    "Std_CommandSearch": "zoom-in.svg",
    "Std_EntitySelectionFilter": "view-select.svg",
    "Std_ToolBarMenu": "preferences-workbenches.svg",
    "Std_DockViewMenu": "Std_ToggleBottomPanels.svg",
    "Std_ViewStatusBar": "info.svg",
}
COLLAPSED_GROUPS = {"Help", "Macro"}
DIMENSION_CHOICES = (
    "Sketcher_Dimension", "Sketcher_ConstrainDistanceY", "Sketcher_ConstrainDistanceX",
    "Sketcher_ConstrainAngle", "Sketcher_ConstrainRadius", "Sketcher_ConstrainDiameter",
    "Sketcher_ConstrainDistance", "Sketcher_ConstrainRadiam", "Sketcher_ConstrainLock",
    "Sketcher_ConstrainSnellsLaw",
)
COMMAND_FAMILIES = (
    ("Part_CoordinateSystem", ("Part_CoordinateSystem",), COORDINATE_CHOICES),
    ("Assembly_CreateJointFixed", ("Assembly_CreateJointFixed",),
     ("Assembly_CreateJointRigidGroup", "Assembly_CreateJointFixed", "Assembly_CreateJointRevolute",
      "Assembly_CreateJointCylindrical", "Assembly_CreateJointSlider", "Assembly_CreateJointBall",
      "Assembly_CreateJointDistance", "Assembly_CreateJointParallel", "Assembly_CreateJointPerpendicular",
      "Assembly_CreateJointAngle", "Assembly_CreateJointRackPinion", "Assembly_CreateJointScrew",
      "Assembly_CreateJointGears", "Assembly_CreateJointBelt")),
    ("PartDesign_Pattern",
     ("PartDesign_Pattern", "PartDesign_CircularPattern", "PartDesign_PathPattern", "PartDesign_PointPattern"),
     ("PartDesign_Pattern", "PartDesign_CircularPattern", "PartDesign_PathPattern", "PartDesign_PointPattern")),
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
    def __init__(self, caption=None, parent=None, fallback="preferences-general.svg"):
        super().__init__(parent)
        self.caption = caption
        self.fallback = fallback

    def setDefaultAction(self, action):
        super().setDefaultAction(action)
        self.restore_caption()

    def restore_caption(self):
        action = self.defaultAction()
        if action and action.icon().isNull():
            self.setIcon(Gui.getIcon(self.fallback))
        if self.caption:
            self.setText(self.caption)
            self.setAccessibleName(self.caption.replace("\n", " "))

    def actionEvent(self, event):
        super().actionEvent(event)
        if event.type() in (QtCore.QEvent.ActionAdded, QtCore.QEvent.ActionChanged):
            self.restore_caption()


def tr(text):
    return App.Qt.translate("PlusRibbon", text)


def available_modes():
    """Installed/registered workbenches, including addons, regardless of selector filtering."""
    workbenches = Gui.listWorkbenches()
    modes = [("Design", "PartDesignWorkbench")] if "PartDesignWorkbench" in workbenches else []
    combined = (set(DESIGN_WORKBENCHES.values()) - {"AssemblyWorkbench"}) | {"NoneWorkbench", "StartWorkbench"}
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
        self.saved_toggles = {}
        self.home_initialized = False
        self.placing = False
        self.workbench_name = Gui.activeWorkbench().name()
        self.mode_name = "Design"
        self.common = QtWidgets.QToolBar(tr("Plus Common"), self.window)
        self.common.setObjectName("FreeCADPlusCommon")
        self.common.setMovable(False)
        self.common.setFloatable(False)
        self.common.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.common.setIconSize(QtCore.QSize(SMALL_ICON_SIZE, SMALL_ICON_SIZE))
        for title, commands in COMMON_GROUPS:
            if self.common.actions():
                self.common.addSeparator()
            for name in commands:
                button = self.make_button(name, self.common, size="small")
                if button:
                    self.common.addWidget(button)
        self.window.addToolBar(QtCore.Qt.TopToolBarArea, self.common)
        self.common.toggleViewAction().setVisible(False)
        self.common.hide()
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
        QtWidgets.QApplication.instance().installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched == self.window and event.type() == QtCore.QEvent.Show and self.enabled:
            self.render_timer.start(0)
        if (watched in self.plus_bars() and event.type() == QtCore.QEvent.Hide
                and self.enabled and not self.changing):
            QtCore.QTimer.singleShot(0, self.ensure_plus_visible)
        if (event.type() == QtCore.QEvent.Show and isinstance(watched, QtWidgets.QToolBar)
                and self.window.isAncestorOf(watched)):
            if watched in self.plus_bars():
                if not self.enabled:
                    watched.hide()
                else:
                    self.hide_bars()
            elif self.enabled and not (self.changing and self.toolbar.isHidden()):
                self.hide_bar(watched)
        return False

    def ensure_plus_visible(self):
        if self.enabled and not self.changing and self.window.isVisible():
            self.hide_bars()
            self.place_plus_bars()

    def plus_bars(self):
        return (self.common, self.toolbar) if hasattr(self, "toolbar") else (self.common,)

    def place_plus_bars(self):
        """Keep the common bar above a full-width ribbon after saved-state restores."""
        if self.placing:
            return
        self.placing = True
        try:
            for bar in self.plus_bars():
                self.window.removeToolBarBreak(bar)
            self.window.addToolBar(QtCore.Qt.TopToolBarArea, self.common)
            self.window.addToolBarBreak(QtCore.Qt.TopToolBarArea)
            self.window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
            self.common.setVisible(self.enabled)
            self.toolbar.setVisible(self.enabled)
        finally:
            self.placing = False

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
            if plus:
                self.hide_bars()
                self.place_plus_bars()
            else:
                self.toolbar.hide()
                self.common.hide()
            return
        self.enabled = plus
        if plus:
            self.saved_bars.pop(Gui.activeWorkbench().name(), None)
            if Gui.activeWorkbench().name() in ("NoneWorkbench", "StartWorkbench"):
                self.activate("PartDesignWorkbench")
            self.workbench_changed(Gui.activeWorkbench().name())
            self.place_plus_bars()
        else:
            self.toolbar.hide()
            self.common.hide()
            self.restore_bars()

    def hide_bars(self):
        for bar in self.window.findChildren(QtWidgets.QToolBar):
            if bar not in self.plus_bars():
                self.hide_bar(bar)

    def hide_bar(self, bar):
        saved = self.saved_bars.setdefault(self.workbench_name, {})
        name = bar.objectName()
        if bar.toggleViewAction().isVisible():
            # Capture only unsuppressed native intent; repeated Show events must
            # not overwrite the Classic layout with our forced hidden state.
            saved.setdefault(name, not bar.isHidden())
        elif name not in saved and not bar.isHidden():
            saved[name] = True
        self.saved_toggles.setdefault(name, bar.toggleViewAction().isVisible())
        # Native ToolBarManager.saveState skips unavailable toggle actions,
        # preserving Classic visibility preferences during workbench switches.
        bar.toggleViewAction().setVisible(False)
        bar.hide()

    def restore_bars(self):
        saved = self.saved_bars.get(Gui.activeWorkbench().name(), {})
        for bar in self.window.findChildren(QtWidgets.QToolBar):
            if bar.objectName() in self.saved_toggles:
                bar.toggleViewAction().setVisible(self.saved_toggles[bar.objectName()])
            if bar.objectName() in saved:
                bar.toggleViewAction().setVisible(True)
                bar.setVisible(saved[bar.objectName()])
        self.saved_toggles.clear()

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
        self.changing = True
        try:
            # Restore native state for its outgoing-workbench save with the
            # ribbon hidden, so even the transition displays only one style.
            self.toolbar.hide()
            self.common.hide()
            self.restore_bars()
            Gui.activateWorkbench(workbench)
        finally:
            self.workbench_name = Gui.activeWorkbench().name()
            if self.enabled:
                self.hide_bars()
            self.changing = False
            self.toolbar.setVisible(self.enabled)
            self.common.setVisible(self.enabled)
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
        self.workbench_name = name
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
            if self.mode_name == "Design":
                return list(HOME_GROUPS)
            groups = list(HOME_GROUPS) if self.mode_name == "Design" else [
                ("Main", ("Std_Part", "Std_ComponentStructure")),
                ("Frequent operations", [command for title, commands in bars.items()
                                         if title not in STANDARD for command in commands if command != "Separator"][:3])]
            groups.append(("Structure", ["Std_ComponentStructure", "Std_Group", "Std_LinkActions", "Std_VarSet", "PartDesign_AddReferenceObject"]))
            groups.append(("Utilities", ["Std_Import", "Std_Export", "Std_DlgPreferences", "Std_CommandSearch",
                                         "Std_Measure", "Std_MassProperties", "Std_Delete"]))
            groups.append(("Help", bars.get("Help", [])))
            groups.append(("Macro", bars.get("Macro", [])))
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

    def initialize_home(self):
        if self.home_initialized or Gui.Control.activeDialog() or not self.window.isVisible():
            return
        original = Gui.activeWorkbench().name()
        mode, tab = self.mode_name, self.current_tab()
        # Native actions from the specialist tabs must be registered before Home
        # projects them. Initialize after the window is shown: native setup saves
        # isVisible(), which would erase Classic visibility with a hidden parent.
        # Initialize each installed workbench once, then restore it.
        for name in dict.fromkeys((*DESIGN_WORKBENCHES.values(), "PartWorkbench")):
            if name in Gui.listWorkbenches():
                self.activate(name)
        self.activate(original)
        self.configure(mode, tab)
        self.home_initialized = True

    def make_button(self, command_name, parent, choices=None, size=None):
        actions = native_actions(command_name)
        if not actions:
            return None
        captions = {"Std_New": tr("New File"), "Std_Part": tr("Add Component"),
                    "Sketcher_Dimension": tr("Auto dimension"), "Part_DatumLine": tr("Datum Axis")}
        if command_name == "PartDesign_Fillet" and self.mode_name == "Design" and self.current_tab() == "Home":
            captions["PartDesign_Fillet"] = tr("Fillet/Chamfer")
        button = RibbonButton(captions.get(command_name), parent,
                              ICON_FALLBACKS.get(command_name, "preferences-general.svg"))
        button.setObjectName("Ribbon_" + command_name)
        button.setAutoRaise(True)
        button.setDefaultAction(actions[0])
        if size is None:
            if self.current_tab() == "Home" and command_name not in ("PartDesign_Extrude", "PartDesign_Revolution"):
                size = "medium" if any(command_name in commands for title, commands in HOME_GROUPS) else "small"
            else:
                size = "full" if command_name in PRIMARY_COMMANDS else "small"
        button.setProperty("ribbonSize", size)
        button.setProperty("ribbonPriority", "primary" if size == "full" else "secondary")
        button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly if size == "small" else QtCore.Qt.ToolButtonTextUnderIcon)
        pixels = {"full": FULL_ICON_SIZE, "medium": MEDIUM_ICON_SIZE, "small": SMALL_ICON_SIZE}[size]
        button.setIconSize(QtCore.QSize(pixels, pixels))
        width, height = (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE) if size == "small" else (
            PRIMARY_WIDTH, GRID_HEIGHT if size == "full" else MEDIUM_HEIGHT)
        button.setFixedSize(width, height)
        if choices:
            actions = [available[0] for name in choices if (available := native_actions(name))]
        if len(actions) > 1:
            menu = QtWidgets.QMenu(button)
            for action in actions:
                if not action.isSeparator():
                    labels = dict(zip(COORDINATE_CHOICES, ("Coordinate System", "Plane", "Axis", "Point")))
                    if command_name == "Part_CoordinateSystem" and self.mode_name == "Design" and self.current_tab() == "Home":
                        # Keep the short Home captions local; native toolbar actions
                        # retain their names and remain responsible for execution.
                        proxy = menu.addAction(action.icon(), tr(labels[action.objectName()]))
                        proxy.setObjectName(action.objectName())
                        proxy.setEnabled(action.isEnabled())
                        proxy.triggered.connect(lambda checked=False, native=action: native.trigger())
                        menu.aboutToShow.connect(lambda native=action, item=proxy: item.setEnabled(native.isEnabled()))
                    else:
                        menu.addAction(action)
            button.setMenu(menu)
            button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        return button

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
        if self.current_tab() == "Home" and self.mode_name == "Design":
            self.initialize_home()
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
            grid.setVerticalSpacing(0)
            grid.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
            buttons = []
            for command_name, choices in projected_commands(commands):
                if self.mode_name == "Design" and self.current_tab() == "Home" and command_name == "PartDesign_Fillet":
                    choices = ("PartDesign_Fillet", "PartDesign_Chamfer")
                size = "medium" if self.current_tab() == "Home" and title in ("Main", "Frequent operations") else None
                button = self.make_button(command_name, group, choices, size)
                if button is None:
                    continue
                buttons.append((button, button.property("ribbonSize") == "full"))
            if title in COLLAPSED_GROUPS and buttons:
                # Rare help operations share one icon; choices retain native states.
                menu_button = QtWidgets.QToolButton(group)
                menu_button.setObjectName("Ribbon_Group_" + title)
                menu_button.setAutoRaise(True)
                menu_button.setText(tr(title))
                menu_button.setToolTip(tr(title))
                menu_button.setIcon(buttons[0][0].icon())
                menu_button.setIconSize(QtCore.QSize(SMALL_ICON_SIZE, SMALL_ICON_SIZE))
                menu_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
                menu_button.setFixedSize(SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE)
                menu_button.setProperty("ribbonPriority", "secondary")
                menu_button.setProperty("ribbonSize", "small")
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
            column, row = len(primaries), 0
            for button in secondary:
                span = 3 if button.property("ribbonSize") == "medium" else 2
                if row + span > GRID_ROWS:
                    column, row = column + 1, 0
                grid.addWidget(button, row, column, span, 1)
                row += span
            for row in range(GRID_ROWS):
                grid.setRowMinimumHeight(row, SMALL_BUTTON_SIZE // 2)
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
