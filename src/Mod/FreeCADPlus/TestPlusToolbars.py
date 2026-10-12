# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Qt acceptance for the independent Plus ribbon presentation."""
import os
import unittest
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import toolbars, ui_modes


def settle():
    QtTest.QTest.qWait(350)


class TestPlusToolbars(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Use an isolated native validation profile')
        self.before = set(App.listDocuments())
        self.prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.saved = [self.prefs.GetInt(key, 0) for key in ui_modes.KEYS]
        self.prefs.SetInt('ToolbarUIMode', 0)
        Gui.activateWorkbench('PartDesignWorkbench')
        ui_modes.apply_modes()
        self.ribbon = toolbars._controller
        Gui.getMainWindow().showMaximized()
        settle()

    def tearDown(self):
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        for key, value in zip(ui_modes.KEYS, self.saved):
            self.prefs.SetInt(key, value)
        ui_modes.apply_modes()
        settle()

    def tab(self, label):
        index = next(i for i in range(self.ribbon.tabbar.count())
                     if self.ribbon.tabbar.tabText(i) == label)
        self.ribbon.tabbar.setCurrentIndex(index)
        settle()

    def test_classic_restore_and_independent_preferences(self):
        r = self.ribbon
        self.assertTrue(r.bar.isVisible())
        self.assertTrue(all(b.isHidden() for b in r.native_bars()))
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        settle()
        self.assertTrue(r.bar.isHidden())
        file_bar = next(b for b in r.native_bars() if b.objectName() == 'File')
        self.assertTrue(file_bar.isVisible())
        file_bar.hide()
        original = [(b, b.parentWidget(), b.actions()) for b in r.native_bars()]
        self.prefs.SetInt('ToolbarUIMode', 0)
        self.prefs.SetInt('ModelPanelUIMode', 1)
        self.prefs.SetInt('TaskPanelUIMode', 1)
        ui_modes.apply_modes()
        settle()
        self.assertTrue(r.bar.isVisible())
        self.assertEqual(ui_modes.modes(), ('Classic', 'Plus', 'Classic'))
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        settle()
        self.assertTrue(file_bar.isHidden())
        for bar, parent, actions in original:
            self.assertEqual(bar.parentWidget(), parent)
            self.assertEqual(bar.actions(), actions)
        file_bar.show()

    def test_tabs_modes_and_idle(self):
        r = self.ribbon
        self.assertEqual(r.tab, 'Modeling')
        self.assertEqual([g.objectName() for g in r.scroll.widget().findChildren(QtWidgets.QWidget)
                          if g.objectName().startswith('PlusGroup_')],
                         ['PlusGroup_' + n for n in ('Sketch','Modeling','Dress-Up','Transformation','Primitives','Other')])
        primitive = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_PartDesign_CompPrimitiveAdditive')
        self.assertEqual(primitive.menu().actions()[-1].text(), 'Tab')
        self.assertFalse(primitive.menu().actions()[-1].isEnabled())
        self.assertNotIn('Tab', [a.text() for a in r.sources['PartDesign_CompPrimitiveAdditive'][1].menu().actions()])
        self.tab('Sketch')
        self.assertEqual(Gui.activeWorkbench().name(), 'SketcherWorkbench')
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertTrue(r.native['Sketcher'].isVisible())
        self.assertTrue(r.native['Geometries'].isHidden())
        self.prefs.SetInt('ToolbarUIMode', 0)
        ui_modes.apply_modes()
        self.assertTrue(r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_Sketcher_CompCreateArc'))
        self.tab('View')
        self.assertEqual(Gui.activeWorkbench().name(), 'SketcherWorkbench')
        self.assertTrue(r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_Std_ViewFitAll'))
        available = Gui.listWorkbenches()
        for i in range(r.selector.count()):
            _, wb = r.selector.itemData(i)
            self.assertEqual(r.selector.model().item(i).isEnabled(), wb in available)
        with patch.object(r, '_build_page', wraps=r._build_page) as build:
            QtTest.QTest.qWait(500)
            self.assertEqual(build.call_count, 0)
        output = Path(os.environ['PLUS_TEST_DIR'])
        r.host.grab().save(str(output/'ribbon-view.png'))
        self.tab('Modeling')
        r.host.grab().save(str(output/'ribbon-modeling.png'))

    def test_native_arc_split_and_last_used(self):
        r = self.ribbon
        self.tab('Sketch')
        doc = App.newDocument('RibbonArc')
        sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
        Gui.activeDocument().setEdit(sketch.Name)
        settle()
        button = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_Sketcher_CompCreateArc')
        native_action, native_button = r.sources['Sketcher_CompCreateArc']
        self.assertIsNot(button, native_button)
        self.assertEqual(button.defaultAction(), native_action)
        self.assertEqual(button.menu(), native_button.menu())
        self.assertEqual(button.popupMode(), QtWidgets.QToolButton.MenuButtonPopup)
        menu = button.menu()
        choices = menu.actions()
        self.assertGreaterEqual(len(choices), 2)
        selected = choices[1]
        child_spy = QtTest.QSignalSpy(selected.triggered)
        root_spy = QtTest.QSignalSpy(native_action.triggered)
        observed = []
        def choose():
            observed.append(menu.isVisible())
            QtTest.QTest.mouseClick(menu, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                   menu.actionGeometry(selected).center())
        QtCore.QTimer.singleShot(100, choose)
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                               QtCore.QPoint(button.width()-4, button.height()//2))
        settle()
        self.assertEqual(observed, [True])
        self.assertEqual(child_spy.count(), 1)
        self.assertEqual(root_spy.count(), 0)
        self.assertEqual(native_action.icon().cacheKey(), selected.icon().cacheKey())
        self.assertEqual(len(menu.actions()), len(choices))
        QtTest.QTest.keyClick(Gui.getMainWindow(), QtCore.Qt.Key_Escape)
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                               QtCore.QPoint(8, button.height()//2))
        settle()
        self.assertEqual(root_spy.count(), 1)
        self.assertFalse(menu.isVisible())
        # Same native action carries the last choice through Classic and tab rebuild.
        icon = native_action.icon().cacheKey()
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertEqual(native_button.icon().cacheKey(), icon)
        self.assertTrue(r.native['Geometries'].isVisible())
        self.assertTrue(r.native['Sketcher'].isHidden())
        self.prefs.SetInt('ToolbarUIMode', 0)
        ui_modes.apply_modes()
        self.assertEqual(native_action.icon().cacheKey(), icon)
        # A live sketch blocks a switch to another native workbench.
        self.tab('Modeling')
        self.assertEqual(Gui.activeWorkbench().name(), 'SketcherWorkbench')
        self.assertTrue(Gui.activeDocument().getInEdit())
        r.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'ribbon-sketch.png'))
        Gui.activeDocument().resetEdit()
        settle()
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertTrue(r.native['Sketcher'].isVisible())
        self.assertTrue(r.native['Geometries'].isHidden())

    def test_plus_group_last_choice_and_native_state(self):
        r = self.ribbon
        button = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_PartDesign_Pad')
        actions = button.menu().actions()
        self.assertEqual(actions, [Gui.Command.get(c).getAction()[0]
                                  for c in ('PartDesign_Pad', 'PartDesign_Pocket')])
        # Emit only the menu selection notification: native commands require a profile.
        # Actual native command dispatch is covered by the Sketcher mouse test.
        button.menu().triggered.emit(actions[1])
        self.assertEqual(button.defaultAction(), actions[1])
        self.tab('Home')
        self.tab('Modeling')
        button = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_PartDesign_Pad')
        self.assertEqual(button.defaultAction(), actions[1])
        self.assertEqual(button.isEnabled(), actions[1].isEnabled())
        self.assertEqual(button.icon().cacheKey(), actions[1].icon().cacheKey())
        toolbars.preferences().SetString('PartDesign_Pad', 'PartDesign_Pad')


def prepare_fresh_process():
    """Save an isolated profile through the normal shutdown path."""
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
    prefs.SetString('AutoloadModule', 'PartDesignWorkbench')
    prefs.SetInt('ToolbarUIMode', 1)
    Gui.activateWorkbench('PartDesignWorkbench')
    ui_modes.apply_modes()
    bars = {b.objectName(): b for b in toolbars._controller.native_bars()}
    bars['File'].hide()
    bars['Edit'].show()
    prefs.SetInt('ToolbarUIMode', 0)
    ui_modes.apply_modes()
    toolbars.preferences().SetString('PartDesign_Pad', 'PartDesign_Pocket')
    App.saveParameter()


def verify_fresh_process():
    """Verify independent restart, saved Plus choice and Classic visibility."""
    Gui.activateWorkbench('PartDesignWorkbench')
    ui_modes.apply_modes()
    settle()
    r = toolbars._controller
    assert r.bar.isVisible()
    assert all(b.isHidden() for b in r.native_bars())
    button = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_PartDesign_Pad')
    assert button.defaultAction() == Gui.Command.get('PartDesign_Pocket').getAction()[0]
    App.ParamGet('User parameter:BaseApp/Preferences/General').SetInt('ToolbarUIMode', 1)
    ui_modes.apply_modes()
    settle()
    assert r.native['File'].isHidden()
    assert r.native['Edit'].isVisible()
    assert r.bar.isHidden()
