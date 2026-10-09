# SPDX-License-Identifier: LGPL-2.1-or-later
"""Fixed creation and relationship review remain scoped to file Edit."""
import importlib
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
import ComponentModel as Model
Nav = importlib.import_module("freecad.gui.ComponentNavigator")


class TestComponentRelationshipsUI(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = Model.new_file_document("RelationsUI")
        self.root = Model.metadata(self.doc).RootComponent
        self.first = Model.children(self.root)[0]
        self.second = Model.add_component(self.root, label="Second")
        self.second.LinkPlacement = App.Placement(App.Vector(30, 4, 2), App.Rotation(20, 10, 5))
        self.panel = Nav.show(self.doc)
        Gui.updateGui()
        self.panel.activate_item(self.panel.structure.topLevelItem(0))
        self.panel.set_file_grounding(self.row(self.first), True)
        self.panel.refresh()

    def tearDown(self):
        for dialog in self.panel.findChildren(QtWidgets.QDialog):
            dialog.close()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()): App.closeDocument(name)
        QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def row(self, obj):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.panel.structure)
        while iterator.value():
            row = iterator.value()
            if any(value and value[0] == Nav.object_key(obj) for value in self.panel.members(row)):
                return row
            iterator += 1
        self.fail("Missing occurrence")

    def fixed_menu(self):
        self.panel.structure.clearSelection()
        self.row(self.first).setSelected(True)
        self.row(self.second).setSelected(True)
        menu = self.panel.build_menu(self.panel.structure, self.row(self.first))
        return menu, next(a for a in menu.actions() if a.objectName() == "fileCreateFixed")

    def create(self):
        menu, action = self.fixed_menu()
        self.assertTrue(action.isEnabled())
        with patch.object(QtWidgets.QMessageBox, "warning") as warning:
            action.trigger()
        warning.assert_not_called()
        return next(self.doc.getObject(entry["object"]) for entry in Model.assembly_record(self.doc)["joints"]
                    if hasattr(self.doc.getObject(entry["object"]), "JointType"))

    def select(self, dialog, joint):
        dialog.listing.clearSelection()
        for index in range(dialog.listing.count()):
            row = dialog.listing.item(index)
            if row.data(QtCore.Qt.UserRole) == joint.Name:
                row.setSelected(True)
                return
        self.fail("Missing relationship")

    def testCreatePreservesPositionsAndHistoryInCurrentTab(self):
        before = App.Placement(self.second.LinkPlacement)
        window = self.panel.mdi.activeSubWindow()
        joint = self.create()
        self.assertTrue(self.second.LinkPlacement.isSame(before, 1e-7))
        self.assertEqual(self.panel.active_key, Nav.object_key(self.root))
        self.assertEqual(self.panel.mdi.activeSubWindow(), window)
        self.assertEqual(self.root.ModelHistory, [])
        self.assertEqual(self.root.ResultObjects, [])
        self.assertEqual(joint.Reference1[0], self.first)
        self.assertEqual(joint.Reference2[0], self.second)

    def testReviewEditRemoveAndUndo(self):
        joint = self.create()
        dialog = Nav.FileRelationshipsDialog(self.panel, self.root)
        self.assertEqual(dialog.listing.count(), 2)
        self.select(dialog, joint)
        self.assertTrue(dialog.edit_button.isEnabled())
        self.assertTrue(dialog.remove_button.isEnabled())
        self.assertEqual(self.panel.active_key, Nav.object_key(self.root))
        self.assertTrue(Gui.Selection.getSelectionEx())
        relative = App.Placement(joint.Placement1)
        relative.Base.x += 12
        dialog.apply_offset(joint, relative)
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 42)
        self.doc.undo()
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 30)
        dialog.refresh()
        joint = self.doc.getObject(joint.Name)
        self.select(dialog, joint)
        name = joint.Name
        dialog.remove_selected()
        self.assertIsNone(self.doc.getObject(name))
        self.assertEqual(dialog.listing.count(), 1)
        self.doc.undo()
        self.assertIsNotNone(self.doc.getObject(name))
        dialog.close()

    def testOffsetDialogCancelDoesNotChangeUndoOrPlacement(self):
        joint = self.create()
        dialog = Nav.FileRelationshipsDialog(self.panel, self.root)
        self.select(dialog, joint)
        before = self.doc.UndoCount, App.Placement(self.second.LinkPlacement)
        def cancel():
            editor = dialog.findChild(QtWidgets.QDialog, "fileFixedOffsetDialog")
            editor.findChild(QtWidgets.QDoubleSpinBox, "fixedOffsetX").setValue(100)
            editor.reject()
        QtCore.QTimer.singleShot(0, cancel)
        dialog.edit_selected()
        self.assertEqual((self.doc.UndoCount, self.second.LinkPlacement), before)
        dialog.close()

    def testOffsetDialogAcceptAndUnchangedAcceptance(self):
        joint = self.create()
        dialog = Nav.FileRelationshipsDialog(self.panel, self.root)
        self.select(dialog, joint)
        dialog.show()
        Gui.updateGui()
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        dialog.grab().save(str(output / "relationships-dialog.png"))
        before = self.doc.UndoCount
        def accept_change():
            editor = dialog.findChild(QtWidgets.QDialog, "fileFixedOffsetDialog")
            editor.findChild(QtWidgets.QDoubleSpinBox, "fixedOffsetX").setValue(33)
            editor.grab().save(str(output / "fixed-offset-dialog.png"))
            editor.accept()
        QtCore.QTimer.singleShot(0, accept_change)
        dialog.edit_selected()
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 33)
        self.assertEqual(self.doc.UndoCount, before + 1)
        self.select(dialog, joint)
        def accept_unchanged():
            editor = next(d for d in dialog.findChildren(QtWidgets.QDialog)
                          if d.objectName() == "fileFixedOffsetDialog" and d.isVisible())
            editor.accept()
        QtCore.QTimer.singleShot(0, accept_unchanged)
        dialog.edit_selected()
        self.assertEqual(self.doc.UndoCount, before + 1)
        dialog.close()

    def testStaleMenuAndDialogRefuseChangedEditContext(self):
        menu, action = self.fixed_menu()
        dialog = Nav.FileRelationshipsDialog(self.panel, self.root)
        dialog.listing.item(0).setSelected(True)
        before = {o.Name for o in self.doc.Objects}
        self.panel.activate_item(self.row(self.first))
        with patch.object(QtWidgets.QMessageBox, "warning") as warning:
            action.trigger()
        warning.assert_called_once()
        with self.assertRaisesRegex(ValueError, "Edit the file"):
            dialog.remove_selected()
        self.assertEqual({o.Name for o in self.doc.Objects}, before)
        dialog.close()

    def testFileMenuOpensReviewAndStaleJointRefusesRemoval(self):
        joint = self.create()
        dialog = Nav.FileRelationshipsDialog(self.panel, self.root)
        self.select(dialog, joint)
        Model.remove_relationships(self.doc, [joint])
        before = {o.Name for o in self.doc.Objects}
        with self.assertRaisesRegex(ValueError, "Refresh"):
            dialog.remove_selected()
        self.assertEqual({o.Name for o in self.doc.Objects}, before)
        dialog.close()
        menu = self.panel.build_menu(self.panel.structure, self.panel.structure.topLevelItem(0))
        action = next(a for a in menu.actions() if a.objectName() == "fileRelationships")
        self.assertTrue(action.isEnabled())
        with patch.object(Nav.FileRelationshipsDialog, "exec", return_value=QtWidgets.QDialog.Rejected) as show:
            action.trigger()
        show.assert_called_once()
