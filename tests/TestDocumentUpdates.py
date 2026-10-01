# SPDX-License-Identifier: LGPL-2.1-or-later
import math
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore
from freecad.gui import DocumentUpdates as Updates
import ManufacturingExport as Export


def settle():
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(250, loop.quit)
    loop.exec_()
    Gui.updateGui()


def make_fixture():
    doc = App.newDocument("DocumentUpdates")
    doc.UndoMode = 1
    blank = doc.addObject("Part::Box", "Blank")
    blank.Length, blank.Width, blank.Height = 20, 12, 8
    bore = doc.addObject("Part::Cylinder", "Bore")
    bore.Radius, bore.Height = 2, 8
    bore.Placement.Base = App.Vector(5, 5, 0)
    cut = doc.addObject("Part::Cut", "Bracket")
    cut.Base, cut.Tool = blank, bore
    link = doc.addObject("App::Link", "Occurrence")
    link.setLink(cut)
    link.LinkPlacement.Base = App.Vector(35, 0, 0)
    doc.recompute()
    blank.Visibility = bore.Visibility = False
    doc.recompute()
    return doc


class TestDocumentUpdates(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()

    def tearDown(self):
        for dialog in list(Updates._dialogs):
            dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self):
        Gui.runCommand("Std_DocumentUpdates")
        Gui.updateGui()
        return Updates._dialogs[-1]

    def testDeferredEditsExplicitUpdateAndNativeMode(self):
        dialog = self.launch()
        self.assertEqual(dialog.table.topLevelItemCount(), 0)
        old = self.doc.Bracket.Shape.Volume
        dialog.deferred.click()
        self.assertTrue(self.doc.RecomputesFrozen)
        self.doc.Blank.Length = 25
        self.doc.Blank.Width = 15
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.Bracket.Shape.Volume, old)
        settle()
        self.assertGreater(dialog.table.topLevelItemCount(), 0)
        with self.assertRaises(ValueError):
            Export.collect_shapes([self.doc.Occurrence])
        dialog.updateButton.click()
        self.assertTrue(self.doc.RecomputesFrozen)
        self.assertEqual(dialog.table.topLevelItemCount(), 0, dialog.message.text())
        self.assertAlmostEqual(self.doc.Bracket.Shape.Volume, 25 * 15 * 8 - math.pi * 4 * 8)
        Export.collect_shapes([self.doc.Occurrence])
        dialog.deferred.click()
        self.assertFalse(self.doc.RecomputesFrozen)
        self.doc.Blank.Length = 30
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.Bracket.Shape.Volume, 30 * 15 * 8 - math.pi * 4 * 8)

    def testNativeFailureCascadeSelectionAndRepair(self):
        dialog = self.launch()
        self.doc.Bracket.Tool = None
        Updates.recompute_now(self.doc)
        dialog.refresh()
        report = Updates.snapshot(self.doc)
        self.assertGreater(report["failed"], 0)
        self.assertIn("Bracket", [row["key"][1] for row in report["rows"]])
        row = next(row for row in report["rows"] if row["key"][1] == "Occurrence")
        self.assertEqual(row["cause"][1], "Bracket")
        index = dialog.rows.index(row)
        dialog.table.setCurrentItem(dialog.table.topLevelItem(index))
        dialog.inputButton.click()
        self.assertEqual(Gui.Selection.getSelection(), [self.doc.Bracket])
        self.assertTrue(self.doc.Bracket.Visibility)
        with self.assertRaises(ValueError):
            Export.collect_shapes([self.doc.Occurrence])
        self.doc.Bracket.Tool = self.doc.Bore
        dialog.updateButton.click()
        self.assertEqual(Updates.snapshot(self.doc)["rows"], [])
        self.assertAlmostEqual(self.doc.Bracket.Shape.Volume, 20 * 12 * 8 - math.pi * 4 * 8)

    def testOwnerTransactionAndActiveDocumentGuards(self):
        self.doc.openTransaction("Owner dimensions")
        self.doc.Blank.Length = 21
        with self.assertRaisesRegex(ValueError, "transaction"):
            Updates.recompute_now(self.doc)
        with self.assertRaisesRegex(ValueError, "transaction"):
            Updates.set_deferred(self.doc, True)
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        other = App.newDocument("OtherUpdates")
        with self.assertRaisesRegex(ValueError, "Activate"):
            Updates.recompute_now(self.doc)
        with self.assertRaisesRegex(ValueError, "Activate"):
            Updates.set_deferred(self.doc, True)
        App.closeDocument(other.Name)

    def testUndoRedoNotReplacedByInspectionOrUpdate(self):
        Updates.set_deferred(self.doc, True)
        self.doc.openTransaction("Change width")
        self.doc.Blank.Width = 18
        self.doc.commitTransaction()
        count = self.doc.UndoCount
        Updates.snapshot(self.doc)
        Updates.recompute_now(self.doc)
        self.assertEqual(self.doc.UndoCount, count)
        self.doc.undo()
        redo = self.doc.RedoCount
        Updates.recompute_now(self.doc)
        self.assertEqual(self.doc.RedoCount, redo)
        self.assertEqual(self.doc.Blank.Width.Value, 12)
        self.doc.redo()
        Updates.recompute_now(self.doc)
        self.assertEqual(self.doc.Blank.Width.Value, 18)

    def testSessionModeReopenAndLifecycle(self):
        dialog = self.launch()
        Updates.set_deferred(self.doc, True)
        settle()
        dialog.reject()
        self.assertTrue(self.doc.RecomputesFrozen)
        self.doc.Blank.Length = 27
        Updates.recompute_now(self.doc)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Updates.FCStd")
            self.doc.saveAs(path)
            dialog = self.launch()
            App.closeDocument(self.doc.Name)
            self.assertTrue(dialog.closed)
            self.doc = App.openDocument(path)
            self.assertFalse(self.doc.RecomputesFrozen)
            self.assertEqual(Updates.snapshot(self.doc)["rows"], [])
            self.assertEqual(self.doc.Blank.Length.Value, 27)

    def testCyclesAndInspectionLimit(self):
        with self.assertRaisesRegex(ValueError, "2000"):
            Updates.snapshot(self.doc, limit=2)
        first = self.doc.addObject("App::FeaturePython", "CycleA")
        second = self.doc.addObject("App::FeaturePython", "CycleB")
        first.addProperty("App::PropertyLink", "Input")
        second.addProperty("App::PropertyLink", "Input")
        first.Input, second.Input = second, first
        report = Updates.snapshot(self.doc)
        self.assertTrue(report["rows"])
        with self.assertRaises(Exception):
            Updates.recompute_now(self.doc)
        first.Input = None
        Updates.recompute_now(self.doc)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testLoadedExternalInputAndDeletedIdentity(self):
        remote = App.newDocument("UpdateSource")
        box = remote.addObject("Part::Box", "RemoteBox")
        remote.recompute()
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        remote.saveAs(str(Path(folder.name) / "Source.FCStd"))
        App.setActiveDocument(self.doc.Name)
        self.doc.saveAs(str(Path(folder.name) / "Consumer.FCStd"))
        link = self.doc.addObject("App::Link", "External")
        link.setLink(box)
        self.doc.recompute()
        box.Length = 15
        report = Updates.snapshot(self.doc)
        row = next(row for row in report["rows"] if row["key"][1] == "External")
        self.assertEqual(row["cause"], Updates.identity(box))
        dialog = self.launch()
        index = dialog.rows.index(row)
        dialog.table.setCurrentItem(dialog.table.topLevelItem(index))
        self.doc.removeObject("External")
        dialog.selectButton.click()
        self.assertIn("no longer available", dialog.message.text())
        self.assertEqual(Gui.Selection.getSelection(), [])
