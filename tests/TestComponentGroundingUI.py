# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part Tree grounding follows file Edit, occurrence ownership and stable menu identity."""
import importlib
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
import ComponentModel as Model
Nav = importlib.import_module("freecad.gui.ComponentNavigator")


class TestComponentGroundingUI(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = Model.new_file_document("GroundingUI")
        self.root = Model.metadata(self.doc).RootComponent
        self.occurrence = Model.children(self.root)[0]
        self.part = self.occurrence.LinkedObject
        self.panel = Nav.show(self.doc)
        Gui.updateGui()
        self.panel.activate_item(self.panel.structure.topLevelItem(0))

    def tearDown(self):
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def row(self, occurrence=None, individual=False):
        key = Nav.object_key(occurrence or self.occurrence)
        iterator = QtWidgets.QTreeWidgetItemIterator(self.panel.structure)
        while iterator.value():
            row = iterator.value()
            if ((not individual or len(self.panel.members(row)) == 1)
                    and any(value and value[0] == key for value in self.panel.members(row))):
                return row
            iterator += 1
        self.fail("Occurrence not found")

    def action(self, row=None):
        menu = self.panel.build_menu(self.panel.structure, row or self.row())
        action = next(a for a in menu.actions() if a.objectName() in
                      ("fileGroundOccurrence", "fileUngroundOccurrence"))
        return menu, action

    def testMenuGroundUngroundKeepsFileEditHistoryAndTab(self):
        window = self.panel.mdi.activeSubWindow()
        count = len(self.panel.mdi.subWindowList())
        placement = App.Placement(self.occurrence.LinkPlacement)
        menu, action = self.action()
        self.assertTrue(action.isEnabled())
        action.trigger()
        self.assertIn("ReadOnly", self.occurrence.getPropertyStatus("LinkPlacement"))
        self.assertEqual(self.panel.active_key, Nav.object_key(self.root))
        self.assertEqual(self.panel.mdi.activeSubWindow(), window)
        self.assertEqual(len(self.panel.mdi.subWindowList()), count)
        self.assertEqual(self.occurrence.LinkPlacement, placement)
        self.assertNotIn("ReadOnly", self.part.getPropertyStatus("Placement"))
        self.assertEqual(self.root.ModelHistory, [])
        self.assertEqual(self.root.ResultObjects, [])
        self.assertEqual(self.panel.history.topLevelItemCount(), 1)
        menu, action = self.action()
        self.assertEqual(action.objectName(), "fileUngroundOccurrence")
        action.trigger()
        self.assertNotIn("ReadOnly", self.occurrence.getPropertyStatus("LinkPlacement"))
        self.doc.undo()
        self.assertIn("ReadOnly", self.occurrence.getPropertyStatus("LinkPlacement"))
        self.doc.redo()
        self.assertNotIn("ReadOnly", self.occurrence.getPropertyStatus("LinkPlacement"))

    def testEditContextRecheckedWhenMenuFires(self):
        menu, action = self.action()
        self.panel.activate_item(self.row())
        before = {o.Name for o in self.doc.Objects}
        with patch.object(QtWidgets.QMessageBox, "warning") as warning:
            action.trigger()
        warning.assert_called_once()
        self.assertEqual({o.Name for o in self.doc.Objects}, before)
        menu, action = self.action()
        self.assertFalse(action.isEnabled())
        self.panel.structure.topLevelItem(0).setSelected(True)
        self.panel.select_structure()
        self.assertEqual(self.panel.active_key, Nav.object_key(self.part))
        with self.assertRaisesRegex(ValueError, "Edit the file"):
            self.panel.set_file_grounding(self.row(), True)

    def testMenuSurvivesRefreshAndRejectsDeletedTarget(self):
        menu, action = self.action()
        self.panel.refresh()
        action.trigger()
        self.assertIn("ReadOnly", self.occurrence.getPropertyStatus("LinkPlacement"))
        menu, action = self.action()
        self.panel.set_file_grounding(self.row(), False)
        Model.remove_instances([self.occurrence])
        self.panel.refresh()
        before = {o.Name for o in self.doc.Objects}
        with patch.object(QtWidgets.QMessageBox, "warning") as warning:
            action.trigger()
        warning.assert_called_once()
        self.assertEqual({o.Name for o in self.doc.Objects}, before)

    def testGroupedNestedAndMultipleRowsAreRefused(self):
        second = Model.add_component(self.root, self.part)
        nested = Model.add_component(self.part, label="Nested")
        self.panel.refresh()
        menu, action = self.action()
        self.assertFalse(action.isEnabled())
        self.assertIn("Expand", action.toolTip())
        self.panel.toggle_instances(self.row())
        self.panel.refresh()
        menu, action = self.action(self.row(nested))
        self.assertFalse(action.isEnabled())
        other = Model.add_component(self.root, label="Other")
        self.panel.refresh()
        individual = self.row(individual=True)
        menu, action = self.action(individual)
        self.assertTrue(action.isEnabled())
        individual.setSelected(True)
        self.row(other).setSelected(True)
        menu, action = self.action(individual)
        self.assertFalse(action.isEnabled())
        self.assertIsNone(Model.assembly_context(self.doc))

    def testExistingPlacementLockCanBecomeAnExplicitGround(self):
        self.occurrence.setEditorMode("LinkPlacement", 1)
        menu, action = self.action()
        self.assertEqual(action.objectName(), "fileGroundOccurrence")
        action.trigger()
        record = Model.assembly_record(self.doc)
        grounds = [self.doc.getObject(entry["object"]) for entry in record["joints"]]
        self.assertEqual(sum(getattr(joint, "ObjectToGround", None) == self.occurrence
                             for joint in grounds), 1)
        menu, action = self.action()
        self.assertEqual(action.objectName(), "fileUngroundOccurrence")
        action.trigger()
        self.assertNotIn("ReadOnly", self.occurrence.getPropertyStatus("LinkPlacement"))

    def testPendingTransactionRefusesWithoutMutation(self):
        self.doc.openTransaction("Unfinished")
        self.root.Label = "Pending"
        before = {o.Name for o in self.doc.Objects}
        try:
            menu, action = self.action()
            self.assertFalse(action.isEnabled())
            with self.assertRaisesRegex(ValueError, "Finish the current task"):
                self.panel.set_file_grounding(self.row(), True)
            self.assertEqual({o.Name for o in self.doc.Objects}, before)
        finally:
            self.doc.abortTransaction()
