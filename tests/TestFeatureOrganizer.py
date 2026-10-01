# SPDX-License-Identifier: LGPL-2.1-or-later
import math
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui import FeatureOrganizer as Organizer


def make_fixture():
    doc = App.newDocument("FeatureNotes")
    doc.UndoMode = 1
    stock = doc.addObject("Part::Box", "Stock")
    stock.Length, stock.Width, stock.Height = 30, 20, 10
    tool = doc.addObject("Part::Cylinder", "Drill")
    tool.Height = 10
    tool.setExpression("Radius", "Stock.Width / 10")
    tool.Placement.Base = App.Vector(10, 10, 0)
    hole = doc.addObject("Part::Cut", "MountingHole")
    hole.Base, hole.Tool = stock, tool
    hole.Label = "Mounting hole"
    hole.Label2 = "M4 clearance trial\nCheck before manufacture"
    link = doc.addObject("App::Link", "SecondBracket")
    link.setLink(hole)
    link.Placement.Base = App.Vector(40, 0, 0)
    doc.recompute()
    stock.Visibility = tool.Visibility = False
    return doc


class TestFeatureOrganizer(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()
        self.dialog = Organizer.OrganizerDialog(self.doc, Gui.getMainWindow())
        self.dialog.show()
        Gui.updateGui()

    def tearDown(self):
        for dialog in list(Organizer._dialogs):
            dialog.reject()
        if not self.dialog.closed:
            self.dialog.reject()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.Selection.clearSelection()
        Gui.updateGui()

    def row(self, name):
        for i in range(self.dialog.table.topLevelItemCount()):
            item = self.dialog.table.topLevelItem(i)
            if item.text(1) == name:
                self.dialog.table.setCurrentItem(item)
                return item
        self.fail("Missing row " + name)

    def testSearchTypesSortingAndExplicitSelectionPreserveModel(self):
        names = [obj.Name for obj in self.doc.Objects]
        visible = [obj.Visibility for obj in self.doc.Objects]
        Gui.Selection.clearSelection()
        self.dialog.query.setText("M4 manufacture")
        self.assertEqual(self.dialog.table.topLevelItemCount(), 1)
        self.row("MountingHole")
        self.assertEqual(Gui.Selection.getSelection(), [])
        self.dialog.selectButton.click()
        self.assertEqual(Gui.Selection.getSelection(), [self.doc.MountingHole])
        self.dialog.query.setText("")
        self.dialog.types.setCurrentIndex(self.dialog.types.findData("Part::Cylinder"))
        self.assertEqual(self.dialog.table.topLevelItemCount(), 1)
        self.row("Drill")
        self.dialog.table.sortByColumn(1, QtCore.Qt.DescendingOrder)
        self.assertEqual(names, [obj.Name for obj in self.doc.Objects])
        self.assertEqual(visible, [obj.Visibility for obj in self.doc.Objects])
        self.assertFalse(self.doc.HasPendingTransaction)

    def testMetadataApplyUndoRedoPersistenceAndDownstream(self):
        hole = self.doc.MountingHole
        identity = hole.ID
        volume = hole.Shape.Volume
        source_refs = (hole.Base, hole.Tool)
        self.row(hole.Name)
        self.dialog.label.setText("Bracket — mounting hole")
        self.dialog.description.setPlainText("Hole spacing review\nØ4 prototype")
        self.dialog.applyButton.click()
        self.assertIn("saved", self.dialog.message.text())
        self.assertEqual(hole.Label, "Bracket — mounting hole")
        self.assertEqual(hole.ID, identity)
        self.assertEqual((hole.Base, hole.Tool), source_refs)
        self.assertEqual(self.doc.SecondBracket.LinkedObject, hole)
        self.assertAlmostEqual(hole.Shape.Volume, volume)
        self.doc.undo()
        self.assertEqual(hole.Label, "Mounting hole")
        self.assertIn("M4", hole.Label2)
        self.doc.redo()
        self.assertEqual(hole.Label2, "Hole spacing review\nØ4 prototype")
        self.dialog.reject()
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "FeatureNotes.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.assertEqual(self.doc.MountingHole.Label2, "Hole spacing review\nØ4 prototype")
            self.doc.Stock.Width = 25
            self.doc.recompute()
            self.assertAlmostEqual(self.doc.Drill.Radius.Value, 2.5)
            self.assertAlmostEqual(self.doc.MountingHole.Shape.Volume, 7500 - math.pi * 2.5**2 * 10)
            self.assertEqual(self.doc.SecondBracket.LinkedObject, self.doc.MountingHole)

    def testCancelStagingAndOccurrenceMetadataIsolation(self):
        original = Organizer.record(self.doc.MountingHole)
        self.row("MountingHole")
        self.dialog.label.setText("Discard this")
        self.dialog.reject()
        self.assertEqual(Organizer.record(self.doc.MountingHole), original)
        self.dialog = Organizer.OrganizerDialog(self.doc, Gui.getMainWindow())
        self.row("SecondBracket")
        self.dialog.label.setText("Second bracket only")
        self.dialog.description.setPlainText("Local inspection note")
        self.dialog.commit()
        self.assertEqual(self.doc.SecondBracket.Label2, "Local inspection note")
        self.assertEqual(Organizer.record(self.doc.MountingHole), original)
        self.assertEqual(self.doc.SecondBracket.Placement.Base, App.Vector(40, 0, 0))

    def testStaleReplacementPendingAndReadonlyReject(self):
        self.row("MountingHole")
        self.doc.MountingHole.Label2 = "Changed elsewhere"
        self.assertFalse(self.dialog.applyButton.isEnabled())
        self.assertFalse(self.dialog.fresh)
        self.dialog.refresh()
        self.row("MountingHole")
        before = Organizer.record(self.doc.MountingHole)
        self.doc.openTransaction("Other edit")
        self.doc.Stock.Label = "Pending owner edit"
        with self.assertRaisesRegex(ValueError, "transaction"):
            Organizer.apply_metadata(self.doc, before, "New name", "New note")
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        self.doc.MountingHole.setPropertyStatus("Label2", "ReadOnly")
        with self.assertRaisesRegex(ValueError, "read-only"):
            Organizer.apply_metadata(self.doc, before, "New name", "New note")
        self.doc.MountingHole.setPropertyStatus("Label2", "-ReadOnly")
        with self.assertRaisesRegex(ValueError, "nonempty"):
            Organizer.apply_metadata(self.doc, before, " ", "New note")
        temp = self.doc.addObject("App::FeaturePython", "Replaceable")
        old = Organizer.record(temp)
        self.doc.removeObject(temp.Name)
        self.doc.addObject("App::FeaturePython", "Replaceable")
        with self.assertRaisesRegex(ValueError, "no longer available"):
            Organizer.apply_metadata(self.doc, old, "Replacement", "")
        self.assertEqual(Organizer.record(self.doc.MountingHole), before)

    def testNoopAndDocumentLifecycle(self):
        before = self.doc.UndoCount
        self.assertFalse(Organizer.apply_metadata(self.doc, Organizer.record(self.doc.Stock),
                                                 self.doc.Stock.Label, self.doc.Stock.Label2))
        self.assertEqual(self.doc.UndoCount, before)
        other = App.newDocument("OtherNotes")
        with self.assertRaisesRegex(ValueError, "Activate"):
            Organizer.apply_metadata(self.doc, Organizer.record(self.doc.Stock), "Changed", "")
        App.closeDocument(other.Name)
        App.closeDocument(self.doc.Name)
        self.assertTrue(self.dialog.closed)

    def testInstalledCommandAndBoundedSearchDisclosure(self):
        self.assertIn("Std_FeatureOrganizer", Gui.listCommands())
        self.dialog.reject()
        Gui.runCommand("Std_FeatureOrganizer")
        Gui.updateGui()
        self.assertTrue(Organizer._dialogs)
        self.assertEqual(Organizer._dialogs[-1].doc, self.doc)
        original_limit = Organizer.LIMIT
        try:
            Organizer.LIMIT = 2
            self.dialog = Organizer.OrganizerDialog(self.doc, Gui.getMainWindow())
            self.assertEqual(len(self.dialog.rows), 2)
            self.assertIn("Partial search", self.dialog.scope.text())
        finally:
            Organizer.LIMIT = original_limit
