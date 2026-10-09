# SPDX-License-Identifier: LGPL-2.1-or-later
"""File Edit blocks modeling tasks but retains occurrence placement."""
import importlib
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
from unittest.mock import patch


def gui(name):
    return importlib.import_module('freecad.gui.' + name)


class TestComponentFileCommands(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_file_document()
        self.root = Model.metadata(self.doc).RootComponent
        self.link = Model.children(self.root)[0]
        self.part = self.link.LinkedObject
        self.panel = gui('ComponentNavigator').show(self.doc)
        Gui.updateGui()
        self.panel.activate_item(self.panel.structure.topLevelItem(0))

    def tearDown(self):
        for name in list(App.listDocuments()): App.closeDocument(name)

    def testFileRefusesAllSharedModelingLaunchersWithoutMutation(self):
        before = {obj.Name for obj in self.doc.Objects}
        undo = self.doc.UndoCount
        for name in ('Extrude', 'Revolve', 'Loft', 'Pipe', 'Helix', 'Primitive', 'Sketch', 'Plane'):
            with self.subTest(task=name):
                with self.assertRaisesRegex(ValueError, 'Edit or create a component'):
                    gui('Component' + name + 'Task').launch()
                self.assertFalse(Gui.Control.activeDialog())
                self.assertEqual({obj.Name for obj in self.doc.Objects}, before)
                self.assertEqual(self.doc.UndoCount, undo)
                self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(self.root.ModelHistory, [])
        self.assertEqual(self.root.ResultObjects, [])

    def testExplicitFileCannotBypassSketchOrPlaneGuard(self):
        for name in ('Sketch', 'Plane'):
            with patch.object(gui('ComponentNavigator'), 'TaskContext') as context:
                with self.assertRaisesRegex(ValueError, 'Edit or create a component'):
                    gui('Component' + name + 'Task').launch(self.root)
                context.assert_not_called()
        self.assertEqual(self.panel.active_key, gui('ComponentNavigator').object_key(self.root))

    def testDatumActionFollowsEditNotSelection(self):
        command = gui('ComponentSketchTask').DatumPlaneCommand()
        self.assertFalse(command.IsActive())
        Gui.Selection.addSelection(self.part)
        self.assertFalse(command.IsActive())
        self.panel.edit_model(self.panel.models.topLevelItem(0))
        self.assertTrue(command.IsActive())
        self.assertEqual(gui('ComponentExtrudeTask').active_component(), self.part)

    def testFileOccurrencePlacementUndoWithoutHistory(self):
        move = gui('MoveComponents')
        session = move.Session(self.root)
        session.add([(self.link.ObjectId,)])
        before = App.Placement(self.link.LinkPlacement)
        delta = App.Placement(App.Vector(12, 4, 2), App.Rotation())
        self.assertTrue(session.commit(delta))
        self.assertTrue(self.link.LinkPlacement.isSame(delta.multiply(before), 1e-9))
        self.assertTrue(self.root.Placement.isIdentity())
        self.assertEqual(self.root.ModelHistory, [])
        self.assertEqual(self.root.ResultObjects, [])
        self.doc.undo()
        self.assertTrue(self.link.LinkPlacement.isSame(before, 1e-9))
        self.doc.redo()
        self.assertTrue(self.link.LinkPlacement.isSame(delta.multiply(before), 1e-9))
        Model.validate(self.doc)

    def testDomesticSketchAndPlaneTasksStillOpenAndCancel(self):
        self.panel.edit_model(self.panel.models.topLevelItem(0))
        before = {obj.Name for obj in self.doc.Objects}
        for name in ('Sketch', 'Plane'):
            task_module = gui('Component' + name + 'Task')
            task_module.launch(self.part)
            self.assertTrue(Gui.Control.activeDialog())
            task_module._task.reject()
            Gui.updateGui()
            self.assertFalse(Gui.Control.activeDialog())
            self.assertEqual({obj.Name for obj in self.doc.Objects}, before)
            self.assertEqual(gui('ComponentExtrudeTask').active_component(), self.part)
