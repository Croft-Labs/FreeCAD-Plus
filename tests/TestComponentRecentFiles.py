# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native recent-file cards, startup focus and component-open acceptance."""
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
from freecad.gui import ComponentNavigator as RuntimeNavigator

if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    spec = importlib.util.spec_from_file_location(
        "RecentOverlay", Path(__file__).with_name("TestComponentModelsPane.py"))
    overlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(overlay)

import ComponentModel as Model
from freecad.gui import ComponentNavigator as Navigator


class TestComponentRecentFiles(unittest.TestCase):
    def setUp(self):
        try:
            import StartGui
        except ImportError:
            self.skipTest("Native Start module unavailable; enable BUILD_START in the next owner-authorized build")
        self.window = Gui.getMainWindow()
        self.mdi = self.window.findChild(QtWidgets.QMdiArea)
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        self.close_start()
        self.prefs = App.ParamGet("User parameter:BaseApp/Preferences/RecentFiles")
        self.prefs.Clear()
        self.prefs.SetInt("RecentFiles", 10)
        start = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Start")
        start.SetBool("FirstStart2024", True)
        start.SetBool("ShowExamples", True)
        start.SetBool("ShowOnStartup", False)
        start.SetString("CustomFolder", str(self.output))
        Gui.activateWorkbench("PartDesignWorkbench")
        Navigator.show()
        RuntimeNavigator._dock = Navigator._dock

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        self.close_start()
        self.settle()

    @staticmethod
    def settle():
        Gui.updateGui()
        QtTest.QTest.qWait(350)

    def close_start(self):
        for sub in self.mdi.subWindowList():
            if sub.findChild(QtWidgets.QWidget, "StartView"):
                sub.close()
        self.settle()

    def page(self):
        Navigator.show_recent_files()
        self.settle()
        view = self.window.findChild(QtWidgets.QWidget, "StartView")
        self.assertIsNotNone(view)
        cards = [cards for cards in view.findChildren(QtWidgets.QListView)
                 if cards.model() and cards.model().metaObject().className() == "Start::RecentFilesModel"]
        self.assertEqual(len(cards), 1)
        return view, cards[0]

    def assert_recent_only(self, view):
        self.assertTrue(view.property("PlusRecentFilesOnly"))
        row = view.findChild(QtWidgets.QWidget, "CreateNewRow")
        self.assertIsNotNone(row)
        self.assertFalse(row.isVisibleTo(view))
        for cards in view.findChildren(QtWidgets.QListView):
            if cards.model() and cards.model().metaObject().className() in (
                    "Start::ExamplesModel", "Start::CustomFolderModel"):
                self.assertFalse(cards.isVisibleTo(view))
        for button in view.findChildren(QtWidgets.QPushButton):
            self.assertFalse(button.isVisibleTo(view))
        self.assertTrue(self.mdi.activeSubWindow().isAncestorOf(view))

    def fixture(self, name):
        doc = Model.new_document(name)
        path = self.output / (name + ".cadprt")
        doc.saveAs(str(path))
        App.closeDocument(doc.Name)
        return path

    def testStartupEmptyAndNoCreationOrExamples(self):
        startup = Navigator.StartupLayout(self.window)
        self.settle()
        self.assertTrue(startup.applied)
        view, cards = self.page()
        self.assert_recent_only(view)
        self.assertEqual(cards.model().rowCount(), 0)
        self.assertTrue(view.findChild(QtWidgets.QLabel, "RecentFilesEmpty").isVisibleTo(view))
        self.assertIsNone(App.ActiveDocument)
        self.assertFalse(App.ParamGet("User parameter:BaseApp/Preferences/Mod/Start").GetBool("ShowOnStartup"))
        view.grab().save(str(self.output / "empty.png"))
        startup.deleteLater()

    def testRecentOrderNativeCardsAndOpen(self):
        first, second = self.fixture("Bracket"), self.fixture("Assembly")
        self.prefs.SetString("MRU0", str(second))
        self.prefs.SetString("MRU1", str(first))
        view, cards = self.page()
        self.assert_recent_only(view)
        model = cards.model()
        paths = [model.index(i, 0).data(QtCore.Qt.UserRole + 10) for i in range(model.rowCount())]
        self.assertEqual(paths, [str(second), str(first)])
        self.assertFalse(view.findChild(QtWidgets.QLabel, "RecentFilesEmpty").isVisibleTo(view))
        view.grab().save(str(self.output / "recent.png"))
        rect = cards.visualRect(model.index(0, 0))
        self.assertFalse(rect.isEmpty())
        QtTest.QTest.mouseClick(cards.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, rect.center())
        self.settle()
        self.assertIsNotNone(App.ActiveDocument)
        self.assertEqual(Path(App.ActiveDocument.FileName), second)
        self.assertIsNotNone(Model.metadata(App.ActiveDocument).RootComponent)

    def testIdempotentAndKeepsOpenedFileActive(self):
        view, cards = self.page()
        Navigator.show_recent_files()
        self.assertEqual(len(self.window.findChildren(QtWidgets.QWidget, "StartView")), 1)
        self.assertEqual(len(view.findChildren(QtWidgets.QLabel, "RecentFilesEmpty")), 1)
        doc = Model.new_document()
        self.settle()
        active = self.mdi.activeSubWindow()
        Navigator.show_recent_files()
        self.assertIs(self.mdi.activeSubWindow(), active)
        self.close_start()
        Navigator.show_recent_files()
        self.assertIsNone(self.window.findChild(QtWidgets.QWidget, "StartView"))
        self.assertIs(App.ActiveDocument, doc)
