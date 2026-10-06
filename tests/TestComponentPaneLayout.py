# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native docking acceptance for the initial Components/Attributes workspace."""
import importlib.util
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest

if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    spec = importlib.util.spec_from_file_location(
        "LayoutOverlay", Path(__file__).with_name("TestComponentModelsPane.py"))
    overlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(overlay)

import ComponentModel as Model
from freecad.gui import ComponentNavigator as Navigator


class TestComponentPaneLayout(unittest.TestCase):
    def setUp(self):
        self.window = Gui.getMainWindow()
        self.window.resize(1280, 1200)
        self.panel = Navigator.show()
        self.attributes = self.window.findChild(QtWidgets.QDockWidget, "Model")
        self.assertIsNotNone(self.attributes)
        self.layout = None

    def tearDown(self):
        self.window.show()
        if self.layout:
            self.window.removeEventFilter(self.layout)
            self.layout.deleteLater()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        self.settle()

    @staticmethod
    def settle():
        Gui.updateGui()
        QtTest.QTest.qWait(200)

    def start(self, preserve=False):
        if self.layout:
            self.window.removeEventFilter(self.layout)
            self.layout.deleteLater()
        self.window.hide()
        self.layout = Navigator.StartupLayout(self.window)
        self.layout.saved_state = "saved" if preserve else ""
        self.window.show()
        self.settle()

    def assert_layout(self):
        for dock in (self.panel, self.attributes):
            self.assertFalse(dock.isFloating())
            self.assertTrue(dock.isVisibleTo(self.window))
            self.assertEqual(self.window.dockWidgetArea(dock), QtCore.Qt.LeftDockWidgetArea)
        self.assertEqual(self.panel.x(), self.attributes.x())
        self.assertEqual(self.panel.width(), self.attributes.width())
        self.assertLess(self.panel.geometry().bottom(), self.attributes.y())
        self.assertNotIn(self.attributes, self.window.tabifiedDockWidgets(self.panel))
        total = self.panel.height() + self.attributes.height()
        self.assertAlmostEqual(self.panel.height() / total, 2 / 3, delta=0.04)
        self.assertEqual(self.attributes.windowTitle(), "Attributes")

    def testEmptyStartupAndNewDocument(self):
        self.assertIsNone(App.ActiveDocument)
        self.panel.hide()
        self.attributes.hide()
        self.start()
        self.assert_layout()
        doc = Model.new_document()
        Navigator.show(doc)
        self.settle()
        self.assert_layout()
        self.panel.refresh()
        self.assertEqual(self.panel.structure.topLevelItem(0).text(0), "Part001")
        self.window.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "workspace.png"))

    def testPreviouslyFloatingAndTabifiedDocks(self):
        self.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.panel)
        self.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.attributes)
        self.window.tabifyDockWidget(self.panel, self.attributes)
        self.start(preserve=True)
        self.assertEqual(self.window.dockWidgetArea(self.panel), QtCore.Qt.RightDockWidgetArea)
        self.assertIn(self.attributes, self.window.tabifiedDockWidgets(self.panel))
        self.panel.setFloating(True)
        self.attributes.setFloating(True)
        self.start(preserve=True)
        self.assertTrue(self.panel.isFloating())
        self.assertTrue(self.attributes.isFloating())

    def testUserResizeSurvivesSubsequentShows(self):
        self.start()
        self.assert_layout()
        self.window.resizeDocks([self.panel, self.attributes], [350, 350], QtCore.Qt.Vertical)
        self.settle()
        heights = (self.panel.height(), self.attributes.height())
        self.assertAlmostEqual(heights[0] / sum(heights), 0.5, delta=0.04)
        Navigator.show()
        self.window.hide()
        self.window.show()
        self.settle()
        self.assertEqual((self.panel.height(), self.attributes.height()), heights)

    def testCommandRegistrationInitializesLayoutOnce(self):
        previous = Navigator._startup_layout
        Navigator._startup_layout = None
        try:
            self.panel.hide()
            self.attributes.hide()
            Navigator.registerCommands()
            self.layout = Navigator._startup_layout
            self.layout.saved_state = ""
            self.assertIsNotNone(self.layout)
            Navigator.registerCommands()
            self.assertIs(Navigator._startup_layout, self.layout)
            self.settle()
            self.assert_layout()
        finally:
            Navigator._startup_layout = previous
