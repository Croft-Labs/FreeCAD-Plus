# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Part commands dispatch to component tasks without legacy fallback."""
import importlib
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
from PySide import QtCore, QtWidgets

ROUTES = (('Part_Primitives', 'Primitive'), ('Part_Extrude', 'Extrude'),
          ('Part_Revolve', 'Revolve'), ('Part_Loft', 'Loft'), ('Part_Sweep', 'Pipe'))


def module(name):
    return importlib.import_module('freecad.gui.Component' + name + 'Task')


class TestComponentNativePartRouting(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench('PartWorkbench')
        self.doc = Model.new_file_document()
        self.root = Model.metadata(self.doc).RootComponent
        self.part = Model.children(self.root)[0].LinkedObject
        self.nav = importlib.import_module('freecad.gui.ComponentNavigator')
        self.panel = self.nav.show(self.doc)
        Gui.updateGui()

    def tearDown(self):
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()): App.closeDocument(name)

    def testNativeDispatchAndFileRefusal(self):
        self.panel.activate_item(self.panel.structure.topLevelItem(0))
        names = {obj.Name for obj in self.doc.Objects}
        undo = self.doc.UndoCount
        for command, task in ROUTES:
            with self.subTest(command=command):
                timer = QtCore.QTimer()
                def dismiss_refusal():
                    for widget in QtWidgets.QApplication.topLevelWidgets():
                        if isinstance(widget, QtWidgets.QMessageBox):
                            widget.accept()
                timer.timeout.connect(dismiss_refusal)
                timer.start(50)
                try:
                    with patch.object(module(task), 'launch', wraps=module(task).launch) as launch:
                        Gui.runCommand(command, 0)
                        launch.assert_called_once_with()
                finally:
                    timer.stop()
                self.assertFalse(Gui.Control.activeDialog())
                self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
                self.assertEqual(self.doc.UndoCount, undo)
                self.assertFalse(self.doc.HasPendingTransaction)

    def testNativeCommandsOpenDomesticTaskAndCancel(self):
        self.panel.edit_model(self.panel.models.topLevelItem(0))
        names = {obj.Name for obj in self.doc.Objects}
        for command, task in ROUTES:
            with self.subTest(command=command):
                target = module(task)
                with patch.object(target, 'launch', wraps=target.launch) as launch:
                    Gui.runCommand(command, 0)
                    launch.assert_called_once_with()
                self.assertTrue(Gui.Control.activeDialog())
                self.assertEqual(target._task.component, self.part)
                target._task.reject()
                Gui.updateGui()
                self.assertFalse(Gui.Control.activeDialog())
                self.assertEqual({obj.Name for obj in self.doc.Objects}, names)

    def testLegacyPrimitiveKeepsNativeDialog(self):
        App.closeDocument(self.doc.Name)
        legacy = App.newDocument('LegacyPartRouting')
        with patch.object(module('Primitive'), 'launch') as launch:
            Gui.runCommand('Part_Primitives', 0)
            launch.assert_not_called()
        self.assertTrue(Gui.Control.activeDialog())
        Gui.Control.closeDialog()
        self.assertEqual(legacy.Objects, [])
