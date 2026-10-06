# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native command ribbon, mode/tab routing and reversible Classic UI."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets

source = Path(os.environ["FREECAD_PLUS_SOURCE"])
if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    spec = importlib.util.spec_from_file_location("RibbonOverlay", source / "tests/TestComponentModelsPane.py")
    overlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(overlay)
    name = "freecad.gui.PlusRibbon"
    previous = sys.modules.get(name)
    old_ribbon = getattr(previous, "_ribbon", None)
    if old_ribbon:
        old_ribbon.enabled = False
        old_ribbon.render_timer.stop()
        old_ribbon.restore_bars()
        old_ribbon.window.workbenchActivated.disconnect(old_ribbon.workbench_changed)
        old_ribbon.window.removeToolBar(old_ribbon.common)
        old_ribbon.common.deleteLater()
        old_ribbon.window.removeToolBar(old_ribbon.toolbar)
        old_ribbon.toolbar.deleteLater()
        old_ribbon.deleteLater()
    spec = importlib.util.spec_from_file_location(name, source / "src/Gui/PlusRibbon.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    import freecad.gui
    freecad.gui.PlusRibbon = module

from freecad.gui import PlusRibbon as UI
from freecad.gui import ComponentNavigator as Navigator
import ComponentModel as Model
from freecad.gui import ComponentSketchTask as SketchTask


def settle():
    Gui.Command.update()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(600, loop.quit)
    loop.exec()


class TestPlusRibbon(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartDesignWorkbench")
        if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
            Navigator.registerCommands()
        self.params = App.ParamGet(UI.PARAM)
        self.params.SetString("ToolbarUIStyle", "Classic")
        UI.apply_preferences()
        self.ribbon = UI._ribbon
        self.doc = Model.new_document()
        Navigator.show(self.doc)
        self.params.SetString("ToolbarUIStyle", "Plus")
        UI.apply_preferences()
        settle()

    def tearDown(self):
        if SketchTask._task:
            SketchTask._task.reject()
        self.params.SetString("ToolbarUIStyle", "Classic")
        UI.apply_preferences()
        Gui.Selection.clearSelection()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def button(self, command):
        return (self.ribbon.common.findChild(QtWidgets.QToolButton, "Ribbon_" + command)
                or self.ribbon.scroll.widget().findChild(QtWidgets.QToolButton, "Ribbon_" + command))

    def testCommonToolbarAndMediumHomeAcrossTabs(self):
        for tab in UI.DESIGN_TABS:
            self.tab(tab)
            self.assertFalse(self.ribbon.common.isHidden())
            for group, commands in UI.COMMON_GROUPS:
                for name in commands:
                    button = self.ribbon.common.findChild(QtWidgets.QToolButton, "Ribbon_" + name)
                    self.assertIsNotNone(button, name)
                    self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonIconOnly)
                    self.assertEqual(button.defaultAction(), Gui.Command.get(name).getAction()[0])
                    self.assertIsNone(self.ribbon.scroll.widget().findChild(QtWidgets.QToolButton, "Ribbon_" + name))
        self.tab("Home")
        for name in ("Std_NewComponent", "Std_Part", "PartDesign_NewSketch", "Part_CoordinateSystem"):
            button = self.button(name)
            self.assertIsNotNone(button, name)
            self.assertEqual(button.property("ribbonSize"), "medium")
            self.assertEqual(button.iconSize().width(), UI.MEDIUM_ICON_SIZE)
            self.assertEqual(button.height(), UI.MEDIUM_HEIGHT)
            self.assertLessEqual(button.width(), UI.PRIMARY_WIDTH)
        for group, commands in UI.HOME_GROUPS:
            for name in commands:
                self.assertIsNotNone(self.button(name), name)
        self.assertEqual([action.objectName() for action in self.button("Part_CoordinateSystem").menu().actions()],
                         list(UI.COORDINATE_CHOICES))
        self.ribbon.window.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-full-window.png"))

    def testNewModelCreatesNoExtraAssemblyInstance(self):
        root = Model.metadata(self.doc).RootComponent
        self.button("Std_NewComponent").click()
        settle()
        models = Model.definitions(self.doc)
        self.assertEqual(len(models), 2)
        created = next(model for model in models if model != root)
        self.assertEqual(created.Label, "Part002")
        self.assertEqual(Model.children(root), [])
        self.assertEqual(Model.instance_counts(root).get(created, 0), 0)
        self.assertEqual(Navigator._dock.active_key, Navigator.object_key(created))
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-new-model.cadprt"
        self.doc.saveAs(str(path))
        self.doc.undo()
        self.assertEqual(len(Model.definitions(self.doc)), 1)
        self.doc.redo()
        self.assertEqual(len(Model.definitions(self.doc)), 2)
        App.closeDocument(self.doc.Name)
        import CadDocument
        reopened = CadDocument.open(str(path))
        self.assertEqual(len(Model.definitions(reopened)), 2)
        self.assertEqual(Model.children(Model.metadata(reopened).RootComponent), [])

    def testCommonCommandsRemainAvailableInEveryInstalledMode(self):
        for mode, workbench in UI.available_modes():
            if mode == "Design":
                continue
            index = next(i for i in range(self.ribbon.modes.count())
                         if self.ribbon.modes.itemData(i)[0] == mode)
            self.ribbon.modes.setCurrentIndex(index)
            settle()
            self.assertEqual(Gui.activeWorkbench().name(), workbench)
            for tab in range(self.ribbon.tabs.count()):
                self.ribbon.tabs.setCurrentIndex(tab)
                settle()
                self.assertFalse(self.ribbon.common.isHidden(), mode)
                self.assertFalse(self.ribbon.toolbar.isHidden(), mode)
                page = self.ribbon.scroll.widget()
                groups = page.findChildren(QtWidgets.QWidget, "PlusRibbonGroup")
                self.assertEqual(len(page.findChildren(QtWidgets.QFrame, "RibbonGroupDivider")), max(0, len(groups) - 1))
                for group in groups:
                    label = group.findChildren(QtWidgets.QLabel)[-1]
                    self.assertEqual(label.text().replace("\n", " "), label.toolTip())
                    for button in group.findChildren(QtWidgets.QToolButton):
                        if button.property("ribbonSize") != "full":
                            self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonIconOnly)
                self.assertLess(self.ribbon.common.geometry().bottom(), self.ribbon.toolbar.geometry().top())
                for group, commands in UI.COMMON_GROUPS:
                    for name in commands:
                        button = self.button(name)
                        self.assertEqual(button.defaultAction(), Gui.Command.get(name).getAction()[0])
                        self.assertEqual(button.isEnabled(), button.defaultAction().isEnabled())
                self.assertTrue(all(bar.isHidden() for bar in self.ribbon.window.findChildren(QtWidgets.QToolBar)
                                    if bar not in self.ribbon.plus_bars()))

    def testCommonCommandsInDraftCamPartAndDrawing(self):
        modes = [(label, name) for label, name in UI.available_modes()
                 if label in ("Design", "Draft", "CAM", "Part", "Drawing")]
        self.assertEqual({label for label, name in modes}, {"Design", "Draft", "CAM", "Part", "Drawing"})
        # Explicit subset for payloads whose separately registered BIM workbench
        # cannot initialize without its optional Addon Manager dependency.
        with patch.object(UI, "available_modes", return_value=modes):
            self.testCommonCommandsRemainAvailableInEveryInstalledMode()

    def testWorkbenchInitializationDefersRendering(self):
        incomplete = type("InitializingWorkbench", (), {
            "name": lambda self: (_ for _ in ()).throw(AttributeError("__Workbench__"))})()
        with patch.object(Gui, "activeWorkbench", return_value=incomplete):
            self.ribbon.workbench_changed("SketcherWorkbench")
            self.assertTrue(self.ribbon.render_timer.isActive())
        Gui.activateWorkbench("SketcherWorkbench")
        settle()
        self.assertFalse(self.ribbon.render_timer.isActive())
        self.assertEqual(self.ribbon.current_tab(), "Sketch")
        self.assertIsNotNone(self.ribbon.scroll.widget())

    def tab(self, name):
        self.ribbon.tabs.setCurrentIndex(UI.DESIGN_TABS.index(name))
        settle()

    def testHomeCommandsAndNativeEnablement(self):
        self.assertEqual([self.ribbon.tabs.tabData(i) for i in range(self.ribbon.tabs.count())], list(UI.DESIGN_TABS))
        self.assertTrue(self.ribbon.enabled)
        self.assertFalse(self.ribbon.toolbar.isHidden())
        self.assertEqual(self.button("Std_New").text(), "New File")
        self.assertEqual(self.button("Std_Part").text(), "Add Component")
        for name in ("Std_New", "Std_Open", "Std_Save", "Std_Undo", "Std_Part", "PartDesign_NewSketch",
                     "Std_NewComponent", "PartDesign_Extrude", "PartDesign_Revolution", "PartDesign_Fillet", "Part_CoordinateSystem"):
            button = self.button(name)
            self.assertIsNotNone(button, name)
            self.assertEqual(button.defaultAction(), Gui.Command.get(name).getAction()[0])
            self.assertEqual(button.isEnabled(), button.defaultAction().isEnabled())
        with patch.object(QtWidgets.QInputDialog, "getItem", side_effect=lambda *args: (args[3][0], True)), \
                patch.object(QtWidgets.QInputDialog, "getText", return_value=("RibbonPart", True)):
            self.button("Std_Part").click()
        settle()
        self.assertEqual(len(Model.children(Model.metadata(self.doc).RootComponent)), 1)
        self.button("PartDesign_NewSketch").click()
        self.assertIsNotNone(SketchTask._task)
        SketchTask._task.reject()
        Gui.updateGui()
        Gui.getMainWindow().resize(1440, 1000)
        settle()
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-home.png"))

    def testDesignTabRoutingAndNativeToolbarSections(self):
        self.tab("Modeling")
        for name in ("PartDesign_Extrude", "PartDesign_Fillet", "PartDesign_Mirrored"):
            self.assertIsNotNone(self.button(name), name)
        for tab, workbench in (("Surface", "SurfaceWorkbench"), ("Sketch", "SketcherWorkbench"),
                               ("Assembly", "AssemblyWorkbench"), ("Mesh", "MeshWorkbench")):
            self.tab(tab)
            self.assertEqual(Gui.activeWorkbench().name(), workbench)
            expected = [(name, commands) for name, commands in Gui.activeWorkbench().getToolbarItems().items()
                        if name not in UI.STANDARD]
            if tab == "Sketch":
                expected = list(UI.SKETCH_GROUPS)
            elif tab == "Assembly":
                expected = list(UI.ASSEMBLY_GROUPS)
            self.assertEqual(self.ribbon.groups(), expected)
            self.assertTrue(self.ribbon.scroll.widget().findChildren(QtWidgets.QToolButton))
        self.tab("View")
        self.assertIsNotNone(self.button("Std_ViewFitAll"))
        self.tab("Modeling")
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-modeling.png"))

    def testClassicVisibilityAcrossWorkbenchSwitches(self):
        self.params.SetString("ToolbarUIStyle", "Classic")
        UI.apply_preferences()
        bars = [bar for bar in Gui.getMainWindow().findChildren(QtWidgets.QToolBar)
                if bar not in self.ribbon.plus_bars() and bar.toggleViewAction().isVisible()]
        first = next(bar for bar in bars if not bar.isHidden())
        first.hide()
        before = {bar.objectName(): bar.isHidden() for bar in bars}
        self.params.SetString("ToolbarUIStyle", "Plus")
        UI.apply_preferences()
        self.assertTrue(all(bar.isHidden() for bar in bars))
        self.tab("Surface")
        self.tab("Modeling")
        self.params.SetString("ToolbarUIStyle", "Classic")
        UI.apply_preferences()
        self.assertTrue(self.ribbon.toolbar.isHidden())
        self.assertEqual({bar.objectName(): bar.isHidden() for bar in bars}, before)
        self.assertTrue(all(bar.toggleViewAction().isVisible() for bar in bars))

    def testLateClassicShowsAndNewToolbarStayHiddenInPlus(self):
        window = Gui.getMainWindow()
        bars = [bar for bar in window.findChildren(QtWidgets.QToolBar)
                if bar not in self.ribbon.plus_bars()]
        self.assertTrue(bars)
        for bar in bars:
            bar.show()
            self.assertTrue(bar.isHidden(), bar.objectName())
        late = QtWidgets.QToolBar("Late native toolbar", window)
        late.setObjectName("PlusTestLateToolbar")
        window.addToolBar(late)
        late.show()
        self.assertTrue(late.isHidden())
        settle()
        self.assertFalse(self.ribbon.toolbar.isHidden())
        self.assertTrue(all(bar.isHidden() for bar in bars))
        self.params.SetString("ToolbarUIStyle", "Classic")
        UI.apply_preferences()
        self.assertTrue(self.ribbon.toolbar.isHidden())
        self.assertFalse(late.isHidden())
        window.removeToolBar(late)
        late.deleteLater()

    def testSavedLayoutCannotDisplayBothStyles(self):
        window = Gui.getMainWindow()
        self.params.SetString("ToolbarUIStyle", "Classic")
        UI.apply_preferences()
        classic_state = window.saveState()
        self.params.SetString("ToolbarUIStyle", "Plus")
        UI.apply_preferences()
        self.assertTrue(window.restoreState(classic_state))
        settle()
        self.assertFalse(self.ribbon.toolbar.isHidden())
        self.assertTrue(all(bar.isHidden() for bar in window.findChildren(QtWidgets.QToolBar)
                            if bar not in self.ribbon.plus_bars()))
        UI.apply_preferences()  # Applying the same choice must enforce it too.
        self.assertFalse(self.ribbon.toolbar.isHidden())
        self.params.SetString("ToolbarUIStyle", "Classic")
        UI.apply_preferences()
        self.ribbon.toolbar.show()
        self.assertTrue(self.ribbon.toolbar.isHidden())

    def testExternalWorkbenchRestoresCannotReshowClassicBars(self):
        for workbench in ("SketcherWorkbench", "DraftWorkbench", "PartDesignWorkbench"):
            Gui.activateWorkbench(workbench)
            settle()
            for bar in Gui.getMainWindow().findChildren(QtWidgets.QToolBar):
                if bar not in self.ribbon.plus_bars():
                    bar.show()
            settle()
            self.assertFalse(self.ribbon.toolbar.isHidden())
            self.assertTrue(all(bar.isHidden() for bar in Gui.getMainWindow().findChildren(QtWidgets.QToolBar)
                                if bar not in self.ribbon.plus_bars()))

    def testAvailableModesTaskGuardAndExternalActivation(self):
        modes = dict(UI.available_modes())
        (Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-modes.json").write_text(
            json.dumps(modes, indent=2), encoding="utf-8")
        self.assertIn("Design", modes)
        self.assertIn("Draft", modes)
        self.assertIn("CAM", modes)
        if "FemWorkbench" in Gui.listWorkbenches():
            self.assertEqual(modes["FEM"], "FemWorkbench")
        with patch.object(Gui, "listWorkbenches", return_value={**Gui.listWorkbenches(),
                          "3DPrintingWorkbench": type("Printing", (), {"MenuText": "3D Printing"})()}):
            self.assertEqual(dict(UI.available_modes())["3D Printing"], "3DPrintingWorkbench")
        self.button("PartDesign_NewSketch").click()
        self.assertIsNotNone(SketchTask._task)
        original = Gui.activeWorkbench().name()
        draft = next(i for i in range(self.ribbon.modes.count()) if self.ribbon.modes.itemData(i)[0] == "Draft")
        self.ribbon.modes.setCurrentIndex(draft)
        self.assertEqual(Gui.activeWorkbench().name(), original)
        SketchTask._task.reject()
        Gui.updateGui()
        Gui.activateWorkbench("DraftWorkbench")
        Gui.updateGui()
        self.assertEqual(self.ribbon.mode_name, "Draft")
        self.assertEqual([self.ribbon.tabs.tabData(i) for i in range(3)], ["Home", "Tools", "View"])
        self.ribbon.tabs.setCurrentIndex(1)
        self.assertTrue(self.ribbon.scroll.widget().findChildren(QtWidgets.QToolButton))

    def testNarrowWindowAndNativeDropdownAction(self):
        self.tab("Modeling")
        window = Gui.getMainWindow()
        window.resize(360, 800)
        settle()
        scroll = self.ribbon.scroll.horizontalScrollBar()
        self.assertGreater(scroll.maximum(), 0)
        scroll.setValue(scroll.maximum())
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-narrow.png"))
        self.tab("Modeling")
        button = self.button("Primitives")
        self.assertIsNotNone(button.menu())
        self.assertEqual([action.text() for action in button.menu().actions()], list(UI.PRIMITIVE_LABELS) + ["Tab"])
        self.assertIsNotNone(self.button("PartDesign_Fillet"))

    def testCompactPrimaryAndSecondaryGrid(self):
        self.tab("Modeling")
        for name in ("PartDesign_Extrude", "PartDesign_Revolution"):
            button = self.button(name)
            self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonTextUnderIcon)
            self.assertEqual(button.width(), UI.PRIMARY_WIDTH)
            self.assertGreaterEqual(button.height(), UI.GRID_HEIGHT)
        first = self.button("PartDesign_Extrude")
        second = self.button("PartDesign_Revolution")
        self.assertEqual(first.y(), second.y())
        groups = self.ribbon.scroll.widget().findChildren(QtWidgets.QWidget, "PlusRibbonGroup")
        for group in groups:
            grid = group.layout().itemAt(0).layout()
            for i in range(grid.count()):
                button = grid.itemAt(i).widget()
                row, column, rows, columns = grid.getItemPosition(i)
                if button.property("ribbonPriority") == "primary":
                    self.assertEqual((row, rows, columns), (0, UI.GRID_ROWS, 1))
                else:
                    self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonIconOnly)
                    expected_size = (UI.PRIMARY_WIDTH, UI.MEDIUM_HEIGHT) if button.property("ribbonSize") == "medium" else (24, 24)
                    self.assertEqual((button.width(), button.height()), expected_size)
                    self.assertLess(row, UI.GRID_ROWS)
                    self.assertEqual((rows, columns), (3 if button.property("ribbonSize") == "medium" else 2, 1))
                self.assertEqual(button.isEnabled(), button.defaultAction().isEnabled())
                self.assertLessEqual(button.geometry().bottom(), group.height())
        self.assertGreaterEqual(self.ribbon.scroll.viewport().height(), max(group.height() for group in groups))
        for name in ("PartDesign_SubtractiveLoft", "PartDesign_SubtractivePipe", "PartDesign_SubtractiveHelix"):
            self.assertIsNone(self.button(name), "Rare variants belong in the family menu")
        self.assertIsNone(self.button("PartDesign_AdditiveLoft").menu())
        self.assertIsNone(self.button("PartDesign_AdditivePipe"))
        self.assertIsNone(self.button("PartDesign_AdditiveHelix").menu())

    def testAutoDimensionChoicesAndSharedNativeStates(self):
        self.tab("Sketch")
        button = self.button("Sketcher_CompDimensionTools")
        self.assertEqual(button.text(), "Dimension Tools")
        self.assertEqual(button.popupMode(), QtWidgets.QToolButton.InstantPopup)
        self.assertEqual([action.objectName() for action in button.menu().actions()],
                         [name for name, label in UI.SKETCH_MENUS["Sketcher_CompDimensionTools"]])
        # The owner explicitly requires independent dimension buttons as well.
        for name in ("Sketcher_Dimension", "Sketcher_ConstrainDistanceX", "Sketcher_ConstrainDistanceY", "Sketcher_ConstrainDistance", "Sketcher_ConstrainAngle", "Sketcher_ConstrainLock"):
            individual = self.button(name)
            self.assertIsNotNone(individual)
            self.assertEqual(individual.defaultAction(), Gui.Command.get(name).getAction()[0])
            self.assertIsNone(individual.menu())
        self.assertEqual(self.button("Sketcher_Dimension").text(), "Dimension")
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-sketch.png"))

    def testExactOwnerDesignSketchLayout(self):
        requirement = json.loads((source / "tests/fixtures/PlusRibbonSketch.json").read_text(encoding="utf-8"))
        self.tab("Sketch")
        expected = [(title, tuple(name for name, label in items)) for title, items in requirement["groups"]]
        self.assertEqual(self.ribbon.groups(), expected)
        groups = self.ribbon.scroll.widget().findChildren(QtWidgets.QWidget, "PlusRibbonGroup")
        self.assertEqual(len(groups), 7)
        for group, (title, items) in zip(groups, requirement["groups"]):
            buttons = group.findChildren(QtWidgets.QToolButton)
            self.assertEqual([button.objectName() for button in buttons], ["Ribbon_" + name for name, label in items])
            for button, (name, label) in zip(buttons, items):
                self.assertEqual(button.text(), label)
                native = Gui.Command.get(name).getAction()[0]
                self.assertEqual(button.defaultAction(), native)
                self.assertEqual(button.isEnabled(), native.isEnabled())
                if name not in requirement["menus"]:
                    self.assertIsNone(button.menu(), name)
        for name, choices in requirement["menus"].items():
            button = self.button(name)
            self.assertEqual(button.popupMode(), QtWidgets.QToolButton.InstantPopup)
            self.assertEqual([(action.objectName(), action.text()) for action in button.menu().actions()], [tuple(choice) for choice in choices])
        self.assertIsNone(self.button("Sketcher_ConstrainSnellsLaw"))
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "sketch-exact.png"))

    def testSketchMenusUseNativeEditStatesAndRouting(self):
        self.tab("Sketch")
        body = self.doc.addObject("PartDesign::Body", "RibbonSketchBody")
        sketch = body.newObject("Sketcher::SketchObject", "RibbonSketch")
        self.doc.recompute()
        Gui.activeDocument().setEdit(sketch.Name)
        settle()
        self.tab("Sketch")
        try:
            routed = 0
            for name, choices in UI.SKETCH_MENUS.items():
                menu = self.button(name).menu()
                menu.aboutToShow.emit()
                for proxy, (command, caption) in zip(menu.actions(), choices):
                    native = Gui.Command.get(command).getAction()[0]
                    self.assertEqual(proxy.isEnabled(), native.isEnabled(), command)
                    self.assertEqual(proxy.isChecked(), native.isChecked(), command)
                    text = native.text()
                    with patch.object(native, "trigger") as trigger:
                        proxy.trigger()
                        self.assertEqual(trigger.call_count, int(native.isEnabled()), command)
                        routed += int(native.isEnabled())
                    self.assertEqual(native.text(), text)
            self.assertGreater(routed, 30)
            self.assertTrue(self.button("Sketcher_CreateLine").isEnabled())
            self.assertTrue(self.button("Sketcher_CreatePolyline").isEnabled())
            self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "sketch-edit.png"))
        finally:
            Gui.activeDocument().resetEdit()
            settle()

    def testExactOwnerDesignAssemblyLayout(self):
        requirement = json.loads((source / "tests/fixtures/PlusRibbonAssembly.json").read_text(encoding="utf-8"))
        self.tab("Assembly")
        expected = [(title, tuple(name for name, label in items)) for title, items in requirement["groups"]]
        self.assertEqual(self.ribbon.groups(), expected)
        groups = self.ribbon.scroll.widget().findChildren(QtWidgets.QWidget, "PlusRibbonGroup")
        self.assertEqual(len(groups), 2)
        for group, (title, items) in zip(groups, requirement["groups"]):
            buttons = group.findChildren(QtWidgets.QToolButton)
            self.assertEqual([button.objectName() for button in buttons], ["Ribbon_" + name for name, label in items])
            for button, (name, label) in zip(buttons, items):
                native = Gui.Command.get(name).getAction()[0]
                self.assertEqual(button.text(), label)
                self.assertEqual(button.defaultAction(), native)
                self.assertEqual(button.isEnabled(), native.isEnabled())
                if name not in requirement["menus"]:
                    self.assertIsNone(button.menu(), name)
        for name, choices in requirement["menus"].items():
            button = self.button(name)
            self.assertEqual(button.popupMode(), QtWidgets.QToolButton.InstantPopup)
            self.assertEqual([(action.objectName(), action.text()) for action in button.menu().actions()],
                             [tuple(choice) for choice in choices])
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "assembly-exact.png"))

    def testAssemblyMenusUseNativeContextStatesAndRouting(self):
        self.tab("Assembly")
        # Execute the actual ribbon button, then check each menu in assembly
        # context and after context is cleared. Routing probes avoid creating
        # unrelated arrays/joints while testing their native action bindings.
        self.assertTrue(self.button("Assembly_CreateAssembly").isEnabled())
        self.button("Assembly_CreateAssembly").click()
        settle()
        assemblies = [obj for obj in self.doc.Objects if obj.isDerivedFrom("Assembly::AssemblyObject")]
        self.assertEqual(len(assemblies), 1)
        component = self.doc.addObject("Part::Box", "RibbonAssemblyBox")
        link = assemblies[0].newObject("App::Link", "RibbonAssemblyLink")
        link.setLink(component)
        self.doc.recompute()
        try:
            checked = 0
            for selected in (False, True):
                Gui.Selection.clearSelection()
                if selected:
                    Gui.Selection.addSelection(link)
                settle()
                for name, choices in UI.ASSEMBLY_MENUS.items():
                    menu = self.button(name).menu()
                    menu.aboutToShow.emit()
                    for proxy, (command, caption) in zip(menu.actions(), choices):
                        native = Gui.Command.get(command).getAction()[0]
                        self.assertEqual(proxy.isEnabled(), native.isEnabled(), command)
                        self.assertEqual(proxy.isChecked(), native.isChecked(), command)
                        text = native.text()
                        with patch.object(native, "trigger") as trigger:
                            proxy.trigger()
                            self.assertEqual(trigger.call_count, int(native.isEnabled()), command)
                            checked += int(native.isEnabled())
                        self.assertEqual(native.text(), text)
            self.assertGreaterEqual(checked, 9)
            self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "assembly-active.png"))
        finally:
            Gui.Selection.clearSelection()
            Gui.activeDocument().resetEdit()
            settle()
        import UtilsAssembly
        self.assertIsNone(UtilsAssembly.activeAssembly())
        for name, choices in UI.ASSEMBLY_MENUS.items():
            menu = self.button(name).menu()
            menu.aboutToShow.emit()
            for proxy, (command, caption) in zip(menu.actions(), choices):
                self.assertEqual(proxy.isEnabled(), Gui.Command.get(command).getAction()[0].isEnabled())
        # Stop native Assembly watchers before the fixture document is destroyed.
        self.tab("Home")

    def testOwnerViewLayoutAndNativeDisplayActions(self):
        self.tab("View")
        groups = self.ribbon.scroll.widget().findChildren(QtWidgets.QWidget, "PlusRibbonGroup")
        self.assertEqual([title for title, commands in self.ribbon.groups()], ["View", "Individual Views"])
        expected = [
            ["Fit All", "Fit Selection", "Standard Views", "Align to Selection", "Draw Style", "Measure", "Mass Properties"],
            ["Isometric", "Front", "Top", "Right", "Rear", "Bottom", "Left"],
        ]
        self.assertEqual(len(groups), 2)
        for group, captions in zip(groups, expected):
            self.assertEqual([button.text() for button in group.findChildren(QtWidgets.QToolButton)], captions)
        views = self.button("Std_ViewGroup")
        styles = self.button("Std_DrawStyle")
        for button in (views, styles):
            self.assertEqual(button.popupMode(), QtWidgets.QToolButton.InstantPopup)
        self.assertEqual([action.text() for action in views.menu().actions()], expected[1])
        self.assertEqual([action.text() for action in styles.menu().actions()],
                         ["As Is", "Points", "Wireframe", "Hidden Line", "No Shading", "Shaded", "Flat Lines"])
        box = self.doc.addObject("Part::Box", "ViewBox")
        self.doc.recompute()
        Gui.Selection.addSelection(box)
        settle()
        for action in views.menu().actions():
            action.trigger()
            settle()
            menu_rotation = Gui.activeDocument().activeView().getCameraOrientation()
            # An independent button must produce the same real camera result.
            Gui.activeDocument().activeView().viewIsometric()
            self.button(action.objectName()).click()
            settle()
            self.assertTrue(menu_rotation.isSame(Gui.activeDocument().activeView().getCameraOrientation(), 1e-10))
            self.assertIsNone(self.button(action.objectName()).menu())
        for action, mode in zip(styles.menu().actions(),
                                ["As Is", "Points", "Wireframe", "Hidden Line", "No Shading", "Shaded", "Flat Lines"]):
            self.assertIn(action, Gui.Command.get("Std_DrawStyle").getAction())
            action.trigger()
            settle()
            self.assertTrue(action.isChecked(), mode)
        styles.menu().actions()[0].trigger()
        for group in groups:
            for button in group.findChildren(QtWidgets.QToolButton):
                self.assertEqual(button.isEnabled(), button.defaultAction().isEnabled())
                self.assertFalse(button.icon().isNull())
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "view-exact.png"))

    def testRareHelpCommandsRemainAccessible(self):
        self.tab("Home")
        button = self.button("Group_Help")
        if not button:
            return  # A workbench may expose no Help toolbar commands.
        self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonIconOnly)
        self.assertEqual(button.popupMode(), QtWidgets.QToolButton.InstantPopup)
        commands = dict(self.ribbon.groups())["Help"]
        for name in commands:
            if name != "Separator" and Gui.Command.get(name):
                actions = Gui.Command.get(name).getAction()
                if actions:
                    self.assertIn(actions[0], button.menu().actions())

    def testAuditStructureAndMacroAccess(self):
        self.tab("Home")
        datums = self.button("Part_CoordinateSystem")
        self.assertIsNotNone(datums.menu())
        self.assertEqual([action.objectName() for action in datums.menu().actions()], list(UI.COORDINATE_CHOICES))
        Gui.activateWorkbench("DraftWorkbench")
        settle()
        variables = self.button("Std_VarSet")
        self.assertEqual(variables.defaultAction(), Gui.Command.get("Std_VarSet").getAction()[0])
        variables.click()
        self.assertTrue(any(obj.isDerivedFrom("App::VarSet") for obj in self.doc.Objects))
        macro = self.button("Group_Macro")
        self.assertEqual(macro.popupMode(), QtWidgets.QToolButton.InstantPopup)
        for name in dict(self.ribbon.groups())["Macro"]:
            if name != "Separator":
                self.assertIn(Gui.Command.get(name).getAction()[0], macro.menu().actions())

    def testAuditIconsAndDrawingPagePriority(self):
        Gui.activateWorkbench("DraftWorkbench")
        settle()
        button = self.button("Std_CommandSearch")
        native = button.defaultAction()
        native_icon = native.icon().cacheKey()
        Gui.Command.update()
        settle()
        self.assertFalse(button.icon().isNull())
        self.assertEqual(native.icon().cacheKey(), native_icon)
        self.tab("View")
        for name in UI.ICON_FALLBACKS:
            button = self.button(name)
            if button:
                self.assertFalse(button.icon().isNull(), name)
        Gui.activateWorkbench("TechDrawWorkbench")
        settle()
        self.ribbon.tabs.setCurrentIndex(1)
        settle()
        page = self.button("TechDraw_PageDefault")
        self.assertEqual(page.property("ribbonPriority"), "primary")
        self.assertGreaterEqual(page.width(), UI.PRIMARY_WIDTH)
        self.assertEqual(page.defaultAction(), Gui.Command.get("TechDraw_PageDefault").getAction()[0])
        for button in self.ribbon.scroll.widget().findChildren(QtWidgets.QToolButton):
            self.assertFalse(button.icon().isNull(), button.objectName())
            if button.menu():
                self.assertFalse(any(action.isSeparator() for action in button.menu().actions()))

    def testExactOwnerDesignModelingLayout(self):
        self.tab("Modeling")
        expected = [("Sketch", ("PartDesign_NewSketch", "Sketcher_EditSketch", "Sketcher_MapSketch", "Part_CoordinateSystem")),
                    ("Modeling", ("PartDesign_Extrude", "PartDesign_Revolution", "PartDesign_AdditiveLoft", "PartDesign_AdditiveHelix")),
                    ("Dress-Up", ("PartDesign_Fillet", "PartDesign_Draft", "PartDesign_Thickness")),
                    ("Transformation", ("PartDesign_Mirrored", "PartDesign_LinearPattern", "PartDesign_CircularPattern", "PartDesign_MultiTransform")),
                    ("Primitives", ("PartDesign_CompPrimitiveAdditive",)),
                    ("Other", ("PartDesign_Defeaturing", "PartDesign_AddReferenceObject"))]
        self.assertEqual(self.ribbon.groups(), expected)
        groups = self.ribbon.scroll.widget().findChildren(QtWidgets.QWidget, "PlusRibbonGroup")
        self.assertEqual(len(groups), 6)
        for group, (title, commands) in zip(groups, expected):
            buttons = group.findChildren(QtWidgets.QToolButton)
            ids = ["Ribbon_Primitives"] if title == "Primitives" else ["Ribbon_" + name for name in commands]
            self.assertEqual([button.objectName() for button in buttons], ids)
            for button, name in zip(buttons, commands):
                self.assertEqual(button.defaultAction(), Gui.Command.get(name).getAction()[0])
                self.assertEqual(button.isEnabled(), button.defaultAction().isEnabled())
        for name, caption in (("Sketcher_MapSketch", "Attach Sketch"), ("PartDesign_AdditiveLoft", "Loft"),
                              ("PartDesign_AdditiveHelix", "Helix"),
                              ("PartDesign_Thickness", "Shell/Thickness"), ("PartDesign_Defeaturing", "Delete Face/Defeaturing")):
            self.assertEqual(self.button(name).text(), caption)
        for name in ("PartDesign_Groove", "PartDesign_SubtractiveLoft", "PartDesign_SubtractiveHelix", "PartDesign_CompPrimitiveSubtractive"):
            self.assertIsNone(self.button(name))
        self.assertIsNone(self.button("PartDesign_CompPrimitiveAdditive"))
        menu = self.button("Primitives").menu()
        self.assertEqual([action.text() for action in menu.actions()], ["Box", "Cylinder", "Sphere", "Cone", "Ellipsoid", "Torus", "Prism", "Wedge", "Tab"])
        self.assertFalse(menu.actions()[-1].isEnabled())
        # An active Body enables real native choices; menu proxies must route each
        # choice once and refresh their states whenever the menu opens.
        body = self.doc.addObject("PartDesign::Body", "PrimitiveMenuBody")
        Gui.activeDocument().activeView().setActiveObject("pdbody", body)
        Gui.Command.update()
        menu.aboutToShow.emit()
        for proxy, native in zip(menu.actions(), Gui.Command.get("PartDesign_CompPrimitiveAdditive").getAction()):
            self.assertEqual(proxy.objectName(), native.objectName())
            self.assertEqual(proxy.isEnabled(), native.isEnabled())
            self.assertTrue(proxy.isEnabled())
            with patch.object(native, "trigger") as trigger:
                proxy.trigger()
                trigger.assert_called_once()
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "modeling-exact.png"))

    def testReadableCaptionsAndGrayDividers(self):
        for tab in UI.DESIGN_TABS:
            self.tab(tab)
            page = self.ribbon.scroll.widget()
            groups = page.findChildren(QtWidgets.QWidget, "PlusRibbonGroup")
            dividers = page.findChildren(QtWidgets.QFrame, "RibbonGroupDivider")
            self.assertEqual(len(dividers), len(groups) - 1, tab)
            for divider in dividers:
                self.assertEqual(divider.width(), 1)
                image = divider.grab().toImage()
                self.assertEqual(image.pixelColor(image.width() // 2, image.height() // 2).name(), "#808080")
            for group in groups:
                label = group.findChildren(QtWidgets.QLabel)[-1]
                self.assertEqual(label.text().replace("\n", " "), label.toolTip())
                self.assertLessEqual(len(label.text().splitlines()), 2)
                for line in label.text().splitlines():
                    self.assertLessEqual(label.fontMetrics().horizontalAdvance(line), label.width())
                for button in group.findChildren(QtWidgets.QToolButton):
                    if button.property("ribbonSize") == "full":
                        self.assertEqual(button.caption_text.replace("\n", " "), button.text().replace("&", "").replace("\n", " "))
                        self.assertLessEqual(len(button.caption_text.splitlines()), 2)
                        for line in button.caption_text.splitlines():
                            self.assertLessEqual(button.fontMetrics().horizontalAdvance(line), button.width() - (24 if button.menu() else 12))
                        self.assertGreaterEqual(button.height() - UI.FULL_ICON_SIZE - 8, 2 * button.fontMetrics().height())
                        image = button.grab().toImage()
                        ratio = image.devicePixelRatio()
                        face_width = button.width() - (12 if button.menu() else 0)
                        left = (face_width - button.iconSize().width()) // 2
                        pixels = {image.pixelColor(round(x * ratio), round(y * ratio)).rgba()
                                  for x in range(left + 2, left + button.iconSize().width() - 2, 3)
                                  for y in range(6, 4 + button.iconSize().height() - 2, 3)}
                        self.assertGreater(len(pixels), 1, button.objectName() + " icon must be painted")
                    else:
                        self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonIconOnly)
            self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / ("ribbon-" + tab + ".png")))
        self.tab("Modeling")
        self.assertEqual(self.button("Part_CoordinateSystem").property("ribbonSize"), "small")
        self.assertEqual([a.text() for a in self.button("Part_CoordinateSystem").menu().actions()], ["Coordinate System", "Plane", "Axis", "Point"])
        self.assertEqual([a.objectName() for a in self.button("PartDesign_Fillet").menu().actions()], ["PartDesign_Fillet", "PartDesign_Chamfer"])
        self.assertEqual(self.button("Primitives").property("ribbonSize"), "full")

    def testDefaultBoxRibbonPointerAndCancel(self):
        try:
            from PySide6 import QtTest
        except ImportError:
            from PySide2 import QtTest
        from freecad.gui import ComponentPrimitiveTask as PrimitiveTask
        self.tab("Modeling")
        button = self.button("Primitives")
        self.assertTrue(button.isEnabled())
        before = {obj.Name for obj in self.doc.Objects}
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                               QtCore.QPoint(button.width() // 3, button.height() // 3))
        settle()
        try:
            self.assertIsNotNone(PrimitiveTask._task)
            self.assertEqual(PrimitiveTask._task.kind.currentData(), "Box")
            self.assertEqual(PrimitiveTask._task.component, Model.metadata(self.doc).RootComponent)
        finally:
            if PrimitiveTask._task:
                PrimitiveTask._task.reject()
        settle()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)

    def testExactOwnerDesignHomeLayout(self):
        self.tab("Home")
        expected = [("Main", ("Std_NewComponent", "Std_Part")),
                    ("Modeling", ("PartDesign_Extrude", "PartDesign_Revolution", "PartDesign_Fillet")),
                    ("Sketch", ("PartDesign_NewSketch", "Part_CoordinateSystem"))]
        self.assertEqual(self.ribbon.groups(), expected)
        groups = self.ribbon.scroll.widget().findChildren(QtWidgets.QWidget, "PlusRibbonGroup")
        self.assertEqual(len(groups), 3)
        for group, (title, commands) in zip(groups, expected):
            self.assertEqual([button.objectName() for button in group.findChildren(QtWidgets.QToolButton)],
                             ["Ribbon_" + command for command in commands])
        fillet = self.button("PartDesign_Fillet")
        self.assertEqual(fillet.text(), "Fillet/Chamfer")
        self.assertEqual(fillet.menu().actions(),
                         [Gui.Command.get(name).getAction()[0] for name in ("PartDesign_Fillet", "PartDesign_Chamfer")])
        for action in fillet.menu().actions():
            self.assertEqual(action.isEnabled(), Gui.Command.get(action.objectName()).getAction()[0].isEnabled())
        coordinate = self.button("Part_CoordinateSystem").menu()
        self.assertEqual([action.text() for action in coordinate.actions()], ["Coordinate System", "Plane", "Axis", "Point"])
        coordinate.aboutToShow.emit()
        for action in coordinate.actions():
            native = Gui.Command.get(action.objectName()).getAction()[0]
            self.assertEqual(action.isEnabled(), native.isEnabled())
            with patch.object(native, "trigger") as trigger:
                action.trigger()
                self.assertEqual(trigger.call_count, int(action.isEnabled()))
        self.assertIsNone(self.button("PartDesign_Chamfer"))
        self.assertIsNone(self.button("Sketcher_EditSketch"))
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "home-exact.png"))

    @unittest.skipIf(os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1", "Restored native pattern bindings require grouped build")
    def testRestoredNativePatternBindings(self):
        self.tab("Modeling")
        # The owner's exact Modeling outline exposes Linear/Circular directly.
        # Keep coverage of the other native bindings without requiring the old menu.
        self.assertIsNone(self.button("PartDesign_Pattern"))
        for name in ("PartDesign_LinearPattern", "PartDesign_CircularPattern"):
            self.assertEqual(self.button(name).defaultAction(), Gui.Command.get(name).getAction()[0])
        expected = ("PartDesign_Pattern", "PartDesign_CircularPattern", "PartDesign_PathPattern", "PartDesign_PointPattern")
        for name in expected:
            self.assertIsNotNone(Gui.Command.get(name))
        body = self.doc.addObject("PartDesign::Body", "AuditPatternBody")
        base = body.newObject("PartDesign::AdditiveBox", "AuditPatternBase")
        self.doc.recompute()
        Gui.activeDocument().activeView().setActiveObject("pdbody", body)
        for name in expected[1:]:
            with self.subTest(command=name):
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(base)
                Gui.runCommand(name)
                Gui.updateGui()
                self.assertTrue(Gui.Control.activeDialog())
                created = [obj for obj in body.Group if obj.TypeId == "PartDesign::" + name.removeprefix("PartDesign_")]
                self.assertEqual(len(created), 1)
                self.assertTrue(created[0].ViewObject.TypeId.endswith(name.removeprefix("PartDesign_") ))
                Gui.Control.activeTaskDialog().reject()
                Gui.updateGui()
                self.assertFalse(Gui.Control.activeDialog())
                self.assertIsNotNone(self.doc.getObject(base.Name))

    @unittest.skipIf(os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1", "Native General preference requires grouped build")
    def testNativeGeneralPreferenceApplyAndCancel(self):
        self.assertTrue(Path(UI.__file__).resolve().is_relative_to(Path(App.ConfigGet("AppHomePath")).resolve()))
        errors = []
        def interact():
            dialog = QtWidgets.QApplication.activeModalWidget()
            try:
                combo = Gui.getMainWindow().findChild(QtWidgets.QComboBox, "toolbarUIStyle")
                self.assertIsNotNone(combo)
                self.assertEqual([combo.itemText(i) for i in range(combo.count())], ["Plus UI", "Classic UI"])
                dialog.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-preferences.png"))
                combo.setCurrentIndex(1)
                box = dialog.findChild(QtWidgets.QDialogButtonBox)
                box.button(QtWidgets.QDialogButtonBox.Apply).click()
                self.assertFalse(self.ribbon.enabled)
                self.assertEqual(self.params.GetString("ToolbarUIStyle"), "Classic")
                combo.setCurrentIndex(0)
                dialog.reject()
                self.assertFalse(self.ribbon.enabled, "Cancel must not apply Plus")
            except Exception as exc:
                errors.append(exc)
                if dialog:
                    dialog.reject()
        QtCore.QTimer.singleShot(800, interact)
        Gui.runCommand("Std_DlgPreferences")
        if errors:
            raise errors[0]
