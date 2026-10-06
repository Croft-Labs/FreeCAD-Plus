# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native command, task handoff and idle-state acceptance."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as RuntimeNavigator
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest

if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    spec = importlib.util.spec_from_file_location(
        "StartOverlay", Path(__file__).with_name("TestComponentModelsPane.py"))
    overlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(overlay)

import ComponentModel as Model
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSketchTask as SketchTask
from freecad.gui import ComponentPlaneTask as PlaneTask


class TestComponentStartActions(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartDesignWorkbench")
        self.window = Gui.getMainWindow()
        Navigator.show()
        if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
            # Existing native Python commands retain their imported module globals.
            # Share the source panel instead of creating a second runtime panel.
            RuntimeNavigator._dock = Navigator._dock
        Navigator.install_startup_layout()
        Navigator.install_start_actions()
        self.actions = Navigator._start_actions
        self.settle()  # Let native startup attach the Tasks overlay host first.
        # No-document startup assertions require docked Tasks. With the owner's
        # overlay preset its host is hidden on the Start page (also in baseline).
        dock = self.window.findChild(QtWidgets.QDockWidget, "Tasks")
        if dock and dock.parentWidget() != self.window:
            Gui.runCommand("Std_DockOverlayAll")
        self.messages = []
        self.watchdog = QtCore.QTimer()
        self.watchdog.timeout.connect(self.dismiss_dialogs)
        self.watchdog.start(25)
        self.settle()

    def dismiss_dialogs(self):
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, QtWidgets.QMessageBox) and widget.isVisible():
                self.messages.append(widget.text())
                widget.done(QtWidgets.QMessageBox.No)

    def tearDown(self):
        if PlaneTask._task:
            PlaneTask._task.reject()
        if SketchTask._task:
            SketchTask._task.reject()
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        for doc in list(App.listDocuments().values()):
            if Gui.getDocument(doc.Name).getInEdit():
                Gui.getDocument(doc.Name).resetEdit()
            App.closeDocument(doc.Name)
        Gui.Selection.clearSelection()
        self.settle()
        self.watchdog.stop()
        self.assertEqual(self.messages, [], "Unexpected modal warning")

    def settle(self):
        Gui.updateGui()
        QtTest.QTest.qWait(350)

    def pane(self):
        panes = [pane for pane in self.window.findChildren(QtWidgets.QWidget, "ComponentStartActions")
                 if pane.isVisibleTo(self.window)]
        self.assertTrue(panes)
        return panes[0]

    def labels(self):
        pane = self.pane()
        return [button.text() for button in pane.findChildren(QtWidgets.QToolButton)
                if button.isVisibleTo(pane)]

    def click(self, name):
        App.Console.PrintMessage("Start action: " + name + "\n")
        button = self.pane().findChild(QtWidgets.QToolButton, name)
        self.assertIsNotNone(button)
        self.assertTrue(button.isEnabled())
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        self.settle()

    def new_file(self):
        self.click("Std_New")
        self.assertEqual(App.ActiveDocument.Label, "untitled001")
        self.assertEqual(Model.metadata(App.ActiveDocument).RootComponent.Label, "Part001")
        self.assertEqual(self.labels(), ["New Sketch", "Coordinate System", "Datum Plane", "Add Component"])
        self.assertEqual(len(self.window.findChildren(QtWidgets.QDockWidget, "ComponentNavigator")), 1)
        self.assertEqual(Navigator._dock.active_key,
                         Navigator.object_key(Model.metadata(App.ActiveDocument).RootComponent))

    def testNewFileAndSketchTaskHandoff(self):
        self.assertEqual(self.labels(), ["New File", "Open"])
        self.window.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "startup.png"))
        self.new_file()
        self.window.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "new-file.png"))
        self.click("PartDesign_NewSketch")
        self.assertIsNotNone(Gui.Control.activeDialog())
        self.assertFalse(any(p.isVisibleTo(self.window) for p in self.window.findChildren(
            QtWidgets.QWidget, "ComponentStartActions")))
        self.assertIsNotNone(SketchTask._task)
        SketchTask._task.reject()
        self.settle()
        self.assertEqual(len(self.labels()), 4)

    def testNativeActionsAndOpenBinding(self):
        for name, caption in Navigator.StartActions.FILE:
            button = self.pane().findChild(QtWidgets.QToolButton, name)
            self.assertIn(button.defaultAction(), Gui.Command.get(name).getAction())
        self.assertEqual(self.pane().findChild(QtWidgets.QToolButton, "Std_Open").text(), "Open")
        self.new_file()
        for name, caption in Navigator.StartActions.COMPONENT:
            button = self.pane().findChild(QtWidgets.QToolButton, name)
            self.assertIn(button.defaultAction(), Gui.Command.get(name).getAction())

    def testDatumCommandsAndAddComponent(self):
        self.new_file()
        root = Model.metadata(App.ActiveDocument).RootComponent
        for command, kind in (("Part_CoordinateSystem", "Part::LocalCoordinateSystem"),
                              ("Std_ComponentDatumPlane", "PartDesign::Plane")):
            self.click(command)
            self.assertIsNotNone(Gui.Control.activeDialog())
            if command == "Std_ComponentDatumPlane":
                self.assertEqual([section.title() for section in PlaneTask._task.sections],
                                 ['1. Plane orientation and location', '2. Orientation',
                                  '3. Origin selection', '4. Preview'])
                PlaneTask._task.plane_collector.basic.menu().actions()[0].trigger()
            boxes = [box for box in self.window.findChildren(QtWidgets.QDialogButtonBox)
                     if box.isVisibleTo(self.window) and box.button(QtWidgets.QDialogButtonBox.Ok)]
            self.assertTrue(boxes)
            QtTest.QTest.mouseClick(boxes[0].button(QtWidgets.QDialogButtonBox.Ok), QtCore.Qt.LeftButton)
            self.settle()
            self.assertFalse(Gui.Control.activeDialog())
            self.assertFalse(App.ActiveDocument.HasPendingTransaction)
            created = [obj for obj in App.ActiveDocument.Objects if obj.isDerivedFrom(kind)]
            self.assertTrue(created)
            self.assertIn(created[-1], root.Group)
        with patch.object(QtWidgets.QInputDialog, "getItem",
                          side_effect=lambda *args: (args[3][0], True)), \
                patch.object(QtWidgets.QInputDialog, "getText", return_value=("Part002", True)):
            self.click("Std_Part")
        self.assertEqual(len(Model.definitions(App.ActiveDocument)), 2)

    def testStartupBeforeWorkbenchAndReturnAfterClose(self):
        Gui.activateWorkbench("NoneWorkbench")
        self.settle()
        self.assertEqual(self.labels(), ["New File", "Open"])
        self.new_file()
        App.closeDocument(App.ActiveDocument.Name)
        self.settle()
        self.assertEqual(self.labels(), ["New File", "Open"])

    def testDatumPlaneInOverlayTasksAfterNewFile(self):
        Gui.runCommand("Std_DockOverlayAll")
        try:
            # New File is always available in the common toolbar, including
            # while the overlay host is hidden on the no-document Start page.
            Gui.runCommand("Std_New")
            self.settle()
            self.click("Std_ComponentDatumPlane")
            task = PlaneTask._task
            self.assertIsInstance(task, PlaneTask.PlaneTask)
            self.assertEqual([s.title() for s in task.sections],
                             ['1. Plane orientation and location', '2. Orientation',
                              '3. Origin selection', '4. Preview'])
            task.plane_collector.basic.menu().actions()[0].trigger()
            Gui.Control.activeTaskDialog().accept()
            self.settle()
            root = Model.metadata(App.ActiveDocument).RootComponent
            self.assertEqual(len(Model.history(root)), 1)
            self.assertEqual(Model.history(root)[0].TypeId, "PartDesign::Plane")
            self.assertFalse(Gui.Control.activeDialog())
        finally:
            Gui.runCommand("Std_DockOverlayAll")

    def testNativeWatchersPreservedOutsideComponentDesign(self):
        doc = App.newDocument("Legacy")
        self.settle()
        self.assertFalse(any(p.isVisibleTo(self.window) for p in self.window.findChildren(
            QtWidgets.QWidget, "ComponentStartActions")))
        views = [view for view in self.window.findChildren(QtWidgets.QStackedWidget)
                 if view.metaObject().className() == "Gui::TaskView::TaskView"]
        self.assertTrue(any(view.widget(0).findChild(QtWidgets.QScrollArea).isVisibleTo(self.window)
                            for view in views))
        Gui.activateWorkbench("DraftWorkbench")
        self.settle()
        self.assertFalse(any(p.isVisibleTo(self.window) for p in self.window.findChildren(
            QtWidgets.QWidget, "ComponentStartActions")))
        App.closeDocument(doc.Name)
        self.settle()
        self.assertEqual(self.labels(), ["New File", "Open"])
        self.new_file()
        self.assertEqual(Gui.activeWorkbench().name(), "PartDesignWorkbench")
