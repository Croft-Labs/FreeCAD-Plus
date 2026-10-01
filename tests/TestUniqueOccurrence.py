# SPDX-License-Identifier: LGPL-2.1-or-later
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide import QtCore
from BasicShapes.ShapeReferences import linked_shape
from freecad.gui import UniqueDefinition as Unique


def make_fixture():
    doc = App.newDocument("UniqueOccurrence")
    doc.UndoMode = 1
    definition = doc.addObject("App::Part", "Spacer")
    sketch = doc.addObject("Sketcher::SketchObject", "Profile")
    definition.addObject(sketch)
    for radius in (5, 2):
        index = sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), radius), False)
        sketch.addConstraint(Sketcher.Constraint("Radius", index, radius))
    extrusion = doc.addObject("Part::Extrusion", "Extrusion")
    definition.addObject(extrusion)
    extrusion.Base = sketch
    extrusion.DirMode = "Normal"
    extrusion.LengthFwd = 3
    extrusion.Solid = True
    definition.Placement = App.Placement(App.Vector(3, 2, 0), App.Rotation(App.Vector(0, 0, 1), 20))
    assembly = doc.addObject("App::Part", "Assembly")
    assembly.Placement = App.Placement(App.Vector(10, 4, 0), App.Rotation(App.Vector(0, 0, 1), 30))
    for name, x in (("First", 20), ("Second", 40)):
        link = doc.addObject("App::Link", name)
        link.setLink(definition)
        assembly.addObject(link)
        link.LinkPlacement.Base = App.Vector(x, 0, 0)
    doc.recompute()
    sketch.Visibility = False
    definition.Visibility = False
    doc.recompute()
    return doc


class TestUniqueOccurrence(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()
        self.dialog = None

    def tearDown(self):
        if self.dialog is not None and not self.dialog.closed:
            self.dialog.reject()
        for dialog in list(Unique._dialogs):
            dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.First)
        self.assertEqual(Unique.selected_occurrence(), self.doc.First)
        Gui.runCommand("Std_MakeOccurrenceUnique")
        Gui.updateGui()
        self.assertTrue(Unique._dialogs)
        self.dialog = Unique._dialogs[-1]
        return self.dialog

    def assertSameShape(self, first, second):
        self.assertAlmostEqual(first.Volume, second.Volume, places=6)
        self.assertAlmostEqual(first.common(second).Volume, second.Volume, places=6)

    def testInstalledReviewCopiesInputsAndPreservesPlacement(self):
        before = linked_shape((self.doc.First, []))
        placement = self.doc.First.LinkPlacement
        old_ids = {obj.ID for obj in self.doc.Objects}
        self.launch()
        self.assertTrue(self.dialog.createButton.isEnabled(), self.dialog.message.text())
        self.assertEqual(self.dialog.members.topLevelItemCount(), 2)
        self.dialog.name.setText("Independent spacer")
        self.dialog.createButton.click()
        self.assertTrue(self.dialog.closed, self.dialog.message.text())
        copied = self.doc.First.LinkedObject
        self.assertNotEqual(copied, self.doc.Spacer)
        self.assertEqual(copied.Label, "Independent spacer")
        self.assertEqual(self.doc.Second.LinkedObject, self.doc.Spacer)
        self.assertEqual(self.doc.First.LinkPlacement, placement)
        self.assertTrue(self.doc.First.Visibility)
        self.assertFalse(copied.Visibility)
        self.assertTrue(all(obj.ID not in old_ids for obj in [copied] + list(copied.Group)))
        sketch = next(obj for obj in copied.Group if obj.TypeId == "Sketcher::SketchObject")
        extrusion = next(obj for obj in copied.Group if obj.TypeId == "Part::Extrusion")
        self.assertEqual(extrusion.Base, sketch)
        self.assertSameShape(linked_shape((self.doc.First, [])), before)
        sketch.setDatum(1, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        self.assertAlmostEqual(linked_shape((self.doc.First, [])).Volume, 48 * math.pi)
        self.assertAlmostEqual(linked_shape((self.doc.Second, [])).Volume, 63 * math.pi)

    def testUndoRedoAndReopenKeepIndependentHistories(self):
        before_names = {obj.Name for obj in self.doc.Objects}
        Unique.make_unique(self.doc.First, Unique.review(self.doc.First), "New spacer")
        copied_name = self.doc.First.LinkedObject.Name
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before_names)
        self.assertEqual(self.doc.First.LinkedObject, self.doc.Spacer)
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(self.doc.First.LinkedObject.Name, copied_name)
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Unique.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.doc.Profile.setDatum(1, App.Units.Quantity("3 mm"))
            self.doc.recompute()
            self.assertAlmostEqual(linked_shape((self.doc.Second, [])).Volume, 48 * math.pi)
            self.assertAlmostEqual(linked_shape((self.doc.First, [])).Volume, 63 * math.pi)
            self.assertEqual(self.doc.First.LinkedObject.Name, copied_name)

    def testCancelStaleReviewAndPendingTransaction(self):
        names = {obj.Name for obj in self.doc.Objects}
        self.launch()
        self.dialog.name.setText("Not committed")
        self.dialog.reject()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        self.launch()
        self.doc.Profile.setDatum(1, App.Units.Quantity("2.5 mm"))
        self.assertFalse(self.dialog.createButton.isEnabled())
        self.doc.recompute()
        self.dialog.refresh()
        self.assertTrue(self.dialog.createButton.isEnabled(), self.dialog.message.text())
        expected = self.dialog.expected
        self.doc.openTransaction("Owner edit")
        self.doc.Second.Label = "Owner's second occurrence"
        with self.assertRaisesRegex(ValueError, "transaction"):
            Unique.make_unique(self.doc.First, expected, "Blocked")
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)

    def testUnsupportedInputsAndConsumersLeaveNoCopy(self):
        names = {obj.Name for obj in self.doc.Objects}
        self.doc.Extrusion.setExpression("LengthFwd", "3 mm")
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "Expression"):
            Unique.review(self.doc.First)
        self.doc.Extrusion.setExpression("LengthFwd", None)
        self.doc.recompute()
        self.doc.First.Scale = 2
        with self.assertRaisesRegex(ValueError, "unscaled"):
            Unique.review(self.doc.First)
        self.doc.First.Scale = 1
        self.doc.recompute()
        consumer = self.doc.addObject("App::FeaturePython", "Consumer")
        consumer.addProperty("App::PropertyLink", "Input")
        consumer.Input = self.doc.First
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "consumers"):
            Unique.review(self.doc.First)
        self.doc.removeObject(consumer.Name)
        self.doc.recompute()
        extra = self.doc.addObject("Part::Box", "Extra")
        self.doc.Spacer.addObject(extra)
        self.doc.recompute()
        self.launch()
        self.assertFalse(self.dialog.createButton.isEnabled())
        self.assertIn("one independent sketch", self.dialog.message.text())
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names | {extra.Name})
        self.assertEqual(self.doc.First.LinkedObject, self.doc.Spacer)

    def testFailureRollsBackAndCanRetry(self):
        names = {obj.Name for obj in self.doc.Objects}
        expected = Unique.review(self.doc.First)
        # A failure after native copy/relink must restore all objects and the link.
        with patch.object(Unique, "next", side_effect=RuntimeError("injected validation failure"), create=True):
            with self.assertRaisesRegex(RuntimeError, "injected"):
                Unique.make_unique(self.doc.First, expected, "Failed copy")
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        self.assertEqual(self.doc.First.LinkedObject, self.doc.Spacer)
        self.assertFalse(self.doc.HasPendingTransaction)
        with self.assertRaisesRegex(ValueError, "nonempty"):
            Unique.make_unique(self.doc.First, expected, " ")
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        self.launch()
        self.doc.removeObject("First")
        self.assertTrue(self.dialog.closed)

    def testSourceChangeRequiresFreshReview(self):
        expected = Unique.review(self.doc.First)
        self.doc.Extrusion.LengthFwd = 5
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "changed"):
            Unique.make_unique(self.doc.First, expected, "Stale")
        Unique.make_unique(self.doc.First, Unique.review(self.doc.First), "Fresh")
        self.assertNotEqual(self.doc.First.LinkedObject, self.doc.Spacer)
