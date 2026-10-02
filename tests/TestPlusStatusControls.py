# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native notifications/navigation/units menus and Plus defaults acceptance."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest

source = Path(os.environ["FREECAD_PLUS_SOURCE"])
if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    spec = importlib.util.spec_from_file_location("PlusDefaultsOverlay", source / "src/Gui/PlusDefaults.py")
    Defaults = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(Defaults)
    resources = os.environ.get("FREECAD_PLUS_TUX_RESOURCES")
    if resources:
        sys.path.insert(0, resources)
    sys.path.insert(0, str(source / "src/Mod/Tux"))
else:
    from freecad.gui import PlusDefaults as Defaults

import NavigationIndicatorGui as Navigation


class TestPlusStatusControls(unittest.TestCase):
    def setUp(self):
        if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") != "1":
            runtime = Path(App.ConfigGet("AppHomePath")).resolve()
            for module in (Defaults, Navigation):
                self.assertTrue(Path(module.__file__).resolve().is_relative_to(runtime),
                                "Status acceptance must use packaged modules: " + str(module.__file__))
        self.window = Gui.getMainWindow()
        self.window.resize(1280, 900)
        self.window.statusBar().show()
        self.view_params = App.ParamGet("User parameter:BaseApp/Preferences/View")
        self.unit_params = App.ParamGet("User parameter:BaseApp/Preferences/Units")
        self.view_params.RemString("NavigationStyle")
        self.unit_params.RemInt("UserSchema")
        Defaults.initialize()
        Navigation.setCurrent()
        self.settle()

    def tearDown(self):
        for menu in self.window.findChildren(QtWidgets.QMenu):
            menu.close()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        self.settle()

    @staticmethod
    def settle():
        Gui.updateGui()
        QtTest.QTest.qWait(250)

    def button(self, kind):
        matches = [button for button in self.window.statusBar().findChildren(QtWidgets.QPushButton)
                   if (button.metaObject().className().split("::")[-1] == kind.split("::")[-1]
                       or (kind == "Gui::NotificationArea" and button.windowTitle() == "Notifications"))]
        self.assertEqual(len(matches), 1,
                         str([(b.metaObject().className(), b.text()) for b in
                              self.window.statusBar().findChildren(QtWidgets.QPushButton)]))
        self.assertTrue(matches[0].isVisibleTo(self.window))
        return matches[0]

    def select(self, button, action):
        menu = button.menu()
        self.assertIsNotNone(menu)
        menu.popup(button.mapToGlobal(button.rect().bottomLeft()))
        self.settle()
        self.assertTrue(menu.isVisible())
        self.assertTrue(action.isEnabled())
        rect = menu.actionGeometry(action)
        self.assertFalse(rect.isEmpty())
        QtTest.QTest.mouseClick(menu, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, rect.center())
        self.settle()
        self.assertFalse(menu.isVisible())

    def testDefaultUnitsAndBlenderAndPreservedChoices(self):
        imperial = App.Units.listSchemas().index("ImperialDecimal")
        self.assertEqual(self.view_params.GetString("NavigationStyle"), "Gui::BlenderNavigationStyle")
        self.assertEqual(self.unit_params.GetInt("UserSchema"), imperial)
        self.assertEqual(App.Units.getSchema(), imperial)
        self.assertIn("in", App.Units.Quantity("25.4 mm").UserString)
        doc = App.newDocument("Defaults")
        self.assertEqual(doc.UnitSystem, App.Units.listSchemas(imperial))
        self.assertEqual(Gui.activeDocument().activeView().getNavigationType(), "Gui::BlenderNavigationStyle")
        self.view_params.SetString("NavigationStyle", "Gui::CADNavigationStyle")
        self.unit_params.SetInt("UserSchema", 0)
        App.Units.setSchema(0)
        Defaults.initialize()
        self.assertEqual(self.view_params.GetString("NavigationStyle"), "Gui::CADNavigationStyle")
        self.assertEqual(self.unit_params.GetInt("UserSchema"), 0)
        self.assertEqual(App.Units.getSchema(), 0)

    def testAllThreeNativeButtonsAndNotificationMenu(self):
        notifications = self.button("Gui::NotificationArea")
        units = self.button("Gui::DimensionWidget")
        self.assertIsNotNone(units.menu())
        self.assertTrue(Navigation.indicator.isVisibleTo(self.window))
        self.assertFalse(Navigation.indicator.icon().isNull())
        self.assertIn("Blender", Navigation.indicator.text())
        prefs = App.ParamGet("User parameter:BaseApp/Preferences/NotificationArea")
        prefs.SetBool("PreventNonIntrusiveNotificationsWhenWindowNotActive", False)
        prefs.SetBool("HideNonIntrusiveNotificationsWhenWindowDeactivated", False)
        App.Console.PrintWarning("Status control acceptance notification\n")
        self.settle()
        QtTest.QTest.qWait(1200)  # Notification delivery is debounced by its native timer.
        self.assertGreaterEqual(int(notifications.text()), 1)
        menu = notifications.menu()
        self.assertIsNotNone(menu)
        menu.popup(notifications.mapToGlobal(notifications.rect().bottomLeft()))
        self.settle()
        self.assertTrue(menu.isVisible())
        self.assertEqual(notifications.text(), "0")
        trees = menu.findChildren(QtWidgets.QTreeWidget)
        self.assertTrue(trees)
        self.assertTrue(any(tree.topLevelItemCount() > 0 for tree in trees))
        menu.close()
        self.settle()
        self.window.statusBar().grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "status-bar.png"))

    def testNavigationMenuChangesCurrentViewer(self):
        doc = App.newDocument("Navigation")
        self.settle()
        view = Gui.activeDocument().activeView()
        self.select(Navigation.indicator, Navigation.a2)
        self.assertEqual(view.getNavigationType(), "Gui::CADNavigationStyle")
        self.assertEqual(self.view_params.GetString("NavigationStyle"), "Gui::CADNavigationStyle")
        self.select(Navigation.indicator, Navigation.a1)
        self.assertEqual(view.getNavigationType(), "Gui::BlenderNavigationStyle")
        self.assertTrue(Navigation.a1.isChecked())

    def testUnitsMenuGlobalAndDocumentScope(self):
        button = self.button("Gui::DimensionWidget")
        actions = button.menu().actions()
        imperial = App.Units.listSchemas().index("ImperialDecimal")
        self.assertTrue(actions[imperial].isChecked())
        self.select(button, actions[0])
        self.assertEqual(self.unit_params.GetInt("UserSchema"), 0)
        self.assertEqual(App.Units.getSchema(), 0)
        self.select(button, actions[imperial])
        doc = App.newDocument("Unit choice")
        self.assertEqual(doc.UnitSystem, App.Units.listSchemas(imperial))
        self.select(button, actions[0])
        self.assertEqual(doc.UnitSystem, App.Units.listSchemas(0))
        self.assertEqual(self.unit_params.GetInt("UserSchema"), imperial)
        self.assertEqual(App.Units.getSchema(), 0)
        self.select(button, actions[imperial])
        self.assertEqual(doc.UnitSystem, App.Units.listSchemas(imperial))
        self.assertIn("in", App.Units.Quantity("25.4 mm").UserString)
