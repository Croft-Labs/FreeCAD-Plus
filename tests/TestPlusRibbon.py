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
        return self.ribbon.scroll.widget().findChild(QtWidgets.QToolButton, "Ribbon_" + command)

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
        self.assertEqual(self.button("Std_NewComponentDocument").text(), "New file")
        self.assertEqual(self.button("Std_Part").text(), "Add part")
        for name in ("Std_Open", "Std_Save", "Std_Undo", "Std_Part", "PartDesign_NewSketch",
                     "Sketcher_MapSketch", "Sketcher_EditSketch", "PartDesign_AddReferenceObject"):
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
        for tab, workbench in (("Surface", "SurfaceWorkbench"), ("Sketch", "SketcherWorkbench"), ("Mesh", "MeshWorkbench")):
            self.tab(tab)
            self.assertEqual(Gui.activeWorkbench().name(), workbench)
            expected = [(name, commands) for name, commands in Gui.activeWorkbench().getToolbarItems().items()
                        if name not in UI.STANDARD]
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
                if bar != self.ribbon.toolbar and bar.toggleViewAction().isVisible()]
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
        self.tab("Home")
        window = Gui.getMainWindow()
        window.resize(650, 800)
        settle()
        scroll = self.ribbon.scroll.horizontalScrollBar()
        self.assertGreater(scroll.maximum(), 0)
        scroll.setValue(scroll.maximum())
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-narrow.png"))
        self.tab("Modeling")
        button = self.button("PartDesign_CompPrimitiveAdditive")
        self.assertIsNotNone(button.menu())
        self.assertEqual(button.menu().actions(), Gui.Command.get("PartDesign_CompPrimitiveAdditive").getAction())
        self.assertIsNotNone(self.button("PartDesign_Fillet"))

    def testCompactPrimaryAndSecondaryGrid(self):
        self.tab("Modeling")
        for name in ("PartDesign_Extrude", "PartDesign_Revolution"):
            button = self.button(name)
            self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonTextUnderIcon)
            self.assertEqual(button.width(), UI.PRIMARY_WIDTH)
            self.assertEqual(button.height(), UI.GRID_HEIGHT)
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
                    self.assertEqual((row, rows, columns), (0, 3, 1))
                else:
                    self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonIconOnly)
                    self.assertEqual((button.width(), button.height()), (24, 24))
                    self.assertLess(row, 3)
                    self.assertEqual((rows, columns), (1, 1))
                self.assertEqual(button.isEnabled(), button.defaultAction().isEnabled())
                self.assertLessEqual(button.geometry().bottom(), group.height())
        self.assertLess(self.ribbon.toolbar.height(), 170)
        for name in ("PartDesign_SubtractiveLoft", "PartDesign_SubtractivePipe", "PartDesign_SubtractiveHelix"):
            self.assertIsNone(self.button(name), "Rare variants belong in the family menu")
        self.assertIn(Gui.Command.get("PartDesign_SubtractiveLoft").getAction()[0],
                      self.button("PartDesign_AdditiveLoft").menu().actions())

    def testAutoDimensionChoicesAndSharedNativeStates(self):
        self.tab("Sketch")
        button = self.button("Sketcher_Dimension")
        self.assertIsNotNone(button)
        self.assertEqual(button.defaultAction(), Gui.Command.get("Sketcher_Dimension").getAction()[0])
        self.assertEqual(button.text().replace("\n", " "), "Auto dimension")
        self.assertEqual(button.popupMode(), QtWidgets.QToolButton.MenuButtonPopup)
        expected = [Gui.Command.get(name).getAction()[0] for name in UI.DIMENSION_CHOICES]
        self.assertEqual(button.menu().actions(), expected)
        for name in UI.DIMENSION_CHOICES[1:]:
            self.assertIsNone(self.button(name), "Specific dimensions are menu choices")
        action = button.defaultAction()
        native_text = action.text()
        Gui.Command.update()
        self.assertEqual(button.text().replace("\n", " "), "Auto dimension")
        self.assertEqual(action.text(), native_text, "Ribbon captions must not rename native menus")
        self.assertEqual(button.isEnabled(), action.isEnabled())
        self.ribbon.toolbar.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ribbon-sketch.png"))

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
