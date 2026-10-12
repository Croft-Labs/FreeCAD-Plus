# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Qt acceptance for the independent Plus ribbon presentation."""
import os
import unittest
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtTest, QtWidgets
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
        self.tab('Modeling')
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

    def test_spreadsheet_native_color_widgets(self):
        Gui.activateWorkbench('SpreadsheetWorkbench')
        ui_modes.apply_modes()
        self.tab('All Tools')
        doc = App.newDocument('RibbonSheet')
        doc.UndoMode = 1
        sheet = doc.addObject('Spreadsheet::Sheet', 'Sheet')
        sheet.set('A1', 'Color test')
        doc.recompute()
        sheet.ViewObject.doubleClicked()
        settle()
        view = sheet.ViewObject.getView()
        view.select('A1', QtCore.QItemSelectionModel.SelectCurrent.value)
        view.setCurrentIndex('A1')
        settle()
        r = self.ribbon
        for suffix, color, read in (('ForegroundColor', QtGui.QColor('red'), sheet.getForeground),
                                    ('BackgroundColor', QtGui.QColor('yellow'), sheet.getBackground)):
            original = r.native['Spreadsheet'].findChild(QtWidgets.QPushButton, 'Spreadsheet_' + suffix)
            copy = r.scroll.widget().findChild(QtWidgets.QPushButton, 'PlusWidget_Spreadsheet_' + suffix)
            self.assertIsNotNone(copy)
            self.assertNotEqual(copy, original)
            self.assertEqual(copy.metaObject().className(), original.metaObject().className())
            parent = original.parentWidget()
            spy = QtTest.QSignalSpy(original.colorSet)
            undo = doc.UndoCount
            copy.setCurrentColor(color)
            settle()
            self.assertEqual(spy.count(), 1)
            self.assertEqual(doc.UndoCount, undo + 1)
            self.assertEqual(read('A1')[:3], (color.redF(), color.greenF(), color.blueF()))
            self.assertEqual(original.parentWidget(), parent)
            doc.undo()
            settle()
            self.assertEqual(doc.UndoCount, undo)
        r.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'ribbon-spreadsheet.png'))

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
            flags = r.selector.model().flags(r.selector.model().index(i, 0))
            self.assertEqual(bool(flags & QtCore.Qt.ItemIsEnabled), wb in available)
        with patch.object(r, '_build_page', wraps=r._build_page) as build:
            QtTest.QTest.qWait(500)
            self.assertEqual(build.call_count, 0)
        output = Path(os.environ['PLUS_TEST_DIR'])
        r.host.grab().save(str(output/'ribbon-view.png'))
        self.tab('Home')
        self.assertEqual(Gui.activeWorkbench().name(), 'PartDesignWorkbench')
        self.assertEqual(r.tab, 'Home')
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

    def test_native_widget_factory_and_all_tools(self):
        r = self.ribbon
        native = Gui.Command.get('Std_Workbench')
        with self.assertRaises(TypeError):
            native.addToToolbar(QtWidgets.QWidget())
        with self.assertRaises(TypeError):
            native.addToToolbar(None)
        original_bar = r.native['Workbench']
        original_action = original_bar.actions()[0]
        original_widget = original_bar.widgetForAction(original_action)
        self.tab('All Tools')
        control = r.scroll.widget().findChild(QtWidgets.QToolBar, 'PlusControl_Std_Workbench')
        self.assertIsNotNone(control)
        widget = control.widgetForAction(control.actions()[0])
        self.assertEqual(widget.metaObject().className(), original_widget.metaObject().className())
        self.assertNotEqual(widget, original_widget)
        self.assertEqual(original_bar.widgetForAction(original_action), original_widget)
        self.assertEqual(widget.count(), original_widget.count())
        self.assertTrue(widget.isEnabled())
        groups = [w.objectName() for w in r.scroll.widget().findChildren(QtWidgets.QWidget)
                  if w.objectName().startswith('PlusGroup_')]
        self.assertEqual(len(groups), len(Gui.activeWorkbench().getToolbarItems()))
        self.assertIn('PlusGroup_Macro', groups)
        self.assertIn('PlusGroup_Clipboard', groups)
        self.assertIn('PlusGroup_Workbench', groups)
        self.assertIn('PlusGroup_Help', groups)
        self.assertIn('PlusGroup_Individual Views', groups)

    def test_added_workbench_expanded_group_and_custom_toolbar(self):
        class ExpandedGroup:
            def GetResources(self):
                return {'MenuText': 'Expanded views', 'DropDownMenu': False}

            def GetCommands(self):
                return ('Std_ViewFront', 'Std_ViewRear')

            def IsActive(self):
                return True

        class PlusCoverageWorkbench(Gui.Workbench):
            MenuText = 'Coverage workbench'
            ToolTip = 'Isolated toolbar acceptance fixture'

            def Initialize(self):
                self.appendToolbar('Coverage expanded', ['PlusCoverageExpanded', 'Separator', 'Std_ViewTop'])
                self.appendToolbar('Coverage custom', ['Std_Save', 'Std_Copy', 'Std_Paste'])

            def GetClassName(self):
                return 'Gui::PythonWorkbench'

        custom = App.ParamGet('User parameter:BaseApp/Workbench/Global/Toolbar/PlusCoverage')
        custom.SetString('Name', 'Coverage global')
        custom.SetString('Std_ViewFront', 'FreeCADGui')
        custom.SetString('Std_ViewRear', 'FreeCADGui')
        Gui.addCommand('PlusCoverageExpanded', ExpandedGroup())
        Gui.addWorkbench(PlusCoverageWorkbench())
        try:
            self.ribbon.selector.showPopup()
            self.ribbon.selector.hidePopup()
            index = next(i for i in range(self.ribbon.selector.count())
                         if self.ribbon.selector.itemData(i)[1] == 'PlusCoverageWorkbench')
            self.ribbon.selector.setCurrentIndex(index)
            settle()
            self.assertEqual(Gui.activeWorkbench().name(), 'PlusCoverageWorkbench')
            self.tab('All Tools')
            control = self.ribbon.scroll.widget().findChild(QtWidgets.QToolBar, 'PlusControl_PlusCoverageExpanded')
            self.assertIsNotNone(control)
            children = Gui.Command.get('PlusCoverageExpanded').getAction()
            self.assertEqual(len(children), 2)
            self.assertEqual(control.actions(), children)
            self.assertTrue(self.ribbon.scroll.widget().findChild(QtWidgets.QWidget, 'PlusGroup_Coverage custom'))
            self.assertTrue(self.ribbon.scroll.widget().findChild(QtWidgets.QWidget, 'PlusGroup_Coverage global'))
            native = self.ribbon.native['Coverage expanded']
            before = native.actions()
            self.prefs.SetInt('ToolbarUIMode', 1)
            ui_modes.apply_modes()
            self.assertTrue(native.isVisible())
            self.assertEqual(native.actions(), before)
        finally:
            App.ParamGet('User parameter:BaseApp/Workbench/Global/Toolbar').RemGroup('PlusCoverage')
            Gui.activateWorkbench('PartDesignWorkbench')
            Gui.removeWorkbench('PlusCoverageWorkbench')

    def test_live_customization_refresh(self):
        window = Gui.getMainWindow()
        Gui.Command.get('Std_DlgCustomize').getAction()[0].trigger()
        settle()
        dialog = next(w for w in window.findChildren(QtWidgets.QDialog)
                      if w.inherits('Gui::Dialog::DlgCustomizeImp'))
        self.assertTrue(dialog.property('FreeCADPlusObserved'))
        custom = App.ParamGet('User parameter:BaseApp/Workbench/PartDesignWorkbench/Toolbar/PlusLiveCoverage')
        custom.SetString('Name', 'Coverage live')
        custom.SetString('Std_ViewFront', 'FreeCADGui')
        native = window.addToolBar('Coverage live')
        native.setObjectName('Coverage live')
        Gui.Command.get('Std_ViewFront').addToToolbar(native)
        native.show()
        settle()
        try:
            self.tab('All Tools')
            # Exercise dialog-close refresh after a further native customization.
            custom.SetString('Std_ViewRear', 'FreeCADGui')
            Gui.Command.get('Std_ViewRear').addToToolbar(native)
            dialog.close()
            settle()
            group = self.ribbon.scroll.widget().findChild(QtWidgets.QWidget, 'PlusGroup_Coverage live')
            self.assertIsNotNone(group)
            self.assertTrue(group.findChild(QtWidgets.QToolButton, 'Plus_Std_ViewRear'))
            self.assertTrue(native.isHidden())
            self.prefs.SetInt('ToolbarUIMode', 1)
            ui_modes.apply_modes()
            self.assertTrue(native.isVisible())
            self.assertEqual(len(native.actions()), 2)
        finally:
            App.ParamGet('User parameter:BaseApp/Workbench/PartDesignWorkbench/Toolbar').RemGroup('PlusLiveCoverage')
            window.removeToolBar(native)
            native.deleteLater()
            settle()

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

# The nineteen workbenches registered by the retained official 1.1.4 baseline.
# NoneWorkbench is its additional empty workbench; optional unregistered examples
# such as MeshPart/Import are not silently enabled or removed by Plus.
CLASSIC_WORKBENCHES = (
    'AssemblyWorkbench', 'BIMWorkbench', 'CAMWorkbench', 'DraftWorkbench',
    'FemWorkbench', 'InspectionWorkbench', 'MaterialWorkbench', 'MeshWorkbench',
    'OpenSCADWorkbench', 'PartDesignWorkbench', 'PartWorkbench', 'PointsWorkbench',
    'ReverseEngineeringWorkbench', 'RobotWorkbench', 'SketcherWorkbench',
    'SpreadsheetWorkbench', 'SurfaceWorkbench', 'TechDrawWorkbench', 'TestWorkbench',
    'NoneWorkbench',
)


def audit_workbench(workbench):
    """Compare Plus's realized controls to the current native toolbar inventory."""
    Gui.activateWorkbench(workbench)
    assert Gui.activeWorkbench().name() == workbench, (workbench, 'Native activation failed')
    ui_modes.apply_modes()
    settle()
    r = toolbars._controller
    index = next(i for i in range(r.tabbar.count()) if r.tabbar.tabText(i) == 'All Tools')
    r.tabbar.setCurrentIndex(index)
    settle()
    items = Gui.activeWorkbench().getToolbarItems()
    commands = set(Gui.listCommands())
    represented = set()
    placeholders = set()
    actual_actions = set()
    groups = r.scroll.widget().findChildren(QtWidgets.QWidget)
    for widget in groups:
        represented.update(widget.property('PlusCommands') or ())
        placeholders.update(widget.property('PlusUnavailable') or ())
        actual_actions.update(widget.actions())
        if isinstance(widget, QtWidgets.QToolButton) and widget.menu():
            actual_actions.update(widget.menu().actions())
    expected = {c for cmds in items.values() for c in cmds if c != 'Separator' and c in commands}
    missing = expected - represented
    assert not missing, (workbench, 'Missing native command controls', sorted(missing))
    assert not expected.intersection(placeholders), (workbench, 'Native commands replaced with placeholders')
    group_names = [w.objectName() for w in groups if w.objectName().startswith('PlusGroup_')]
    assert len(group_names) == len(items), (workbench, 'Toolbar group count differs')
    native_action_count = 0
    for name in items:
        bar = r.native.get(name)
        assert bar is not None, (workbench, 'Missing Classic toolbar', name)
        for action in bar.actions():
            if action.isSeparator():
                continue
            if isinstance(action, QtWidgets.QWidgetAction):
                original = bar.widgetForAction(action)
                command = action.data()
                identity = command or 'Widget_' + original.objectName()
                control = r.scroll.widget().findChild(QtWidgets.QToolBar, 'PlusControl_' + identity)
                assert control is not None, (workbench, name, 'Missing widget factory', identity)
                copies = [control.widgetForAction(a) for a in control.actions()]
                assert any(w is not None and w != original and
                           w.metaObject().className() == original.metaObject().className()
                           for w in copies), (workbench, name, 'Widget class differs')
            else:
                assert action in actual_actions, (workbench, name, action.objectName(), action.text())
                native_action_count += 1
    routed = {wb for _, wb in r.tabs if wb}
    routed.update(r.selector.itemData(i)[1] for i in range(r.selector.count()))
    routed.update(wb for _, wb in toolbars.layout.DESIGN_TABS if wb)
    assert set(Gui.listWorkbenches()) <= routed, (workbench, 'Omitted workbench route')
    # Every group remains reachable using the horizontal scrollbar on narrow screens.
    scroll = r.scroll.horizontalScrollBar()
    scroll.setValue(scroll.maximum())
    QtTest.QTest.qWait(50)
    if workbench in ('CAMWorkbench', 'FemWorkbench', 'DraftWorkbench', 'AssemblyWorkbench', 'TechDrawWorkbench'):
        r.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/(workbench+'-all-tools-end.png')))
        scroll.setValue(0)
        QtTest.QTest.qWait(50)
        r.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/(workbench+'-all-tools.png')))
    preserved = [(b, b.parentWidget(), b.actions(), b.property('FreeCADPlusClassicVisible'))
                 for b in r.native_bars()]
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
    prefs.SetInt('ToolbarUIMode', 1)
    ui_modes.apply_modes()
    settle()
    for bar, parent, actions, visible in preserved:
        assert bar.parentWidget() == parent and bar.actions() == actions, (workbench, 'Classic ownership changed')
        assert bar.isVisible() == visible, (workbench, bar.objectName(), 'Classic visibility differs')
    prefs.SetInt('ToolbarUIMode', 0)
    ui_modes.apply_modes()
    settle()
    assert all(b.isHidden() for b in r.native_bars()), (workbench, 'Classic/Plus overlap')
    return dict(workbench=workbench, toolbars=len(items), commands=len(expected),
                native_actions=native_action_count, unavailable_in_classic=sorted(placeholders),
                toolbar_names=list(items))
