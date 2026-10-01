# SPDX-License-Identifier: LGPL-2.1-or-later
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad.gui import OccurrenceMove as Move
from BasicShapes.ShapeReferences import linked_shape


def make_fixture():
    doc = App.newDocument("OccurrenceMove")
    doc.UndoMode = 1
    source = doc.addObject("Part::Box", "Bracket")
    source.Length, source.Width, source.Height = 10, 7, 5
    source.Placement = App.Placement(App.Vector(3, 2, 1), App.Rotation(App.Vector(0, 0, 1), 10))
    assembly = doc.addObject("App::Part", "Assembly")
    assembly.Placement = App.Placement(App.Vector(20, 5, 0), App.Rotation(App.Vector(0, 0, 1), 90))
    nested = doc.addObject("App::Part", "Nested")
    assembly.addObject(nested)
    nested.Placement = App.Placement(App.Vector(8, 0, 0), App.Rotation(App.Vector(0, 0, 1), 30))
    for name, x in (("First", 0), ("Second", 20)):
        link = doc.addObject("App::Link", name)
        nested.addObject(link)
        link.setLink(source)
        link.LinkPlacement = App.Placement(App.Vector(x, 0, 0), App.Rotation(App.Vector(0, 0, 1), 20))
    doc.recompute()
    source.Visibility = False
    doc.recompute()
    return doc


class TestOccurrenceMove(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()

    def tearDown(self):
        for dialog in list(Move._dialogs):
            dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.First)
        self.assertEqual(Move.selected_occurrence(), self.doc.First)
        Gui.runCommand("Std_MoveOccurrenceOnce")
        Gui.updateGui()
        return Move._dialogs[-1]

    def shape(self):
        # Independent native assembly-path oracle; do not test the resolver against itself.
        return Part.getShape(self.doc.Assembly, "Nested.First.", needSubElement=True, transform=True)

    def assertVector(self, actual, expected):
        self.assertLess((actual - expected).Length, 1e-6)

    def assertShape(self, first, second):
        self.assertAlmostEqual(first.Volume, second.Volume, places=6)
        self.assertAlmostEqual(first.common(second).Volume, second.Volume, places=6)

    def testNestedWorldAndOccurrenceTranslations(self):
        self.assertShape(linked_shape((self.doc.First, [])), self.shape())
        initial = self.shape().CenterOfMass
        source = App.Placement(self.doc.Bracket.Placement)
        other = App.Placement(self.doc.Second.LinkPlacement)
        Move.move(self.doc.First, Move.review(self.doc.First), "Translate", "Occurrence", (10, 0, 0))
        delta = App.Vector(10 * math.cos(math.radians(140)), 10 * math.sin(math.radians(140)), 0)
        self.assertVector(self.shape().CenterOfMass, initial + delta)
        Move.move(self.doc.First, Move.review(self.doc.First), "Translate", "World", (10, 0, 0))
        self.assertVector(self.shape().CenterOfMass, initial + delta + App.Vector(10, 0, 0))
        self.assertEqual(self.doc.Bracket.Placement, source)
        self.assertEqual(self.doc.Second.LinkPlacement, other)
        self.assertEqual(self.doc.First.LinkedObject, self.doc.Bracket)

    def testArbitraryAxisPivotAndSourceTransform(self):
        for transform in (False, True):
            self.doc.First.LinkTransform = transform
            self.doc.recompute()
            expected = self.shape()
            expected.rotate(App.Vector(4, 2, 1), App.Vector(1, 2, 3), 35)
            Move.move(self.doc.First, Move.review(self.doc.First), "Rotate", "World", (1, 2, 3), 35, (4, 2, 1))
            self.assertShape(self.shape(), expected)
        world = self.doc.Nested.getGlobalPlacement().multiply(self.doc.First.LinkPlacement)
        expected = self.shape()
        expected.rotate(world.multVec(App.Vector(2, 1, 0)), world.Rotation.multVec(App.Vector(0, 0, 1)), 45)
        Move.move(self.doc.First, Move.review(self.doc.First), "Rotate", "Occurrence", (0, 0, 1), 45, (2, 1, 0))
        self.assertShape(self.shape(), expected)

    def testPreviewMatchesCommitWithoutDocumentMutation(self):
        names = {obj.Name for obj in self.doc.Objects}
        before = App.Placement(self.doc.First.LinkPlacement)
        undo = self.doc.UndoCount
        dialog = self.launch()
        self.assertTrue(dialog.moveButton.isEnabled(), dialog.message.text())
        dialog.offset[0].setValue(12)
        _, expected, world = Move.candidate(self.doc.First, dialog.expected, *dialog.values())
        root = Gui.activeDocument().activeView().getSceneGraph()
        count = root.getNumChildren()
        dialog.previewButton.click()
        self.assertIsNotNone(dialog.ghost, dialog.message.text())
        self.assertEqual(root.getNumChildren(), count + 1)
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        self.assertEqual(self.doc.First.LinkPlacement, before)
        self.assertEqual(self.doc.UndoCount, undo)
        dialog.moveButton.click()
        self.assertTrue(dialog.closed, dialog.message.text())
        self.assertEqual(root.getNumChildren(), count)
        self.assertShape(self.shape(), expected)
        self.assertEqual(self.doc.UndoCount, undo + 1)

    def testCancelStalePreviewAndDeleteCleanup(self):
        before = App.Placement(self.doc.First.LinkPlacement)
        dialog = self.launch()
        dialog.offset[0].setValue(10)
        dialog.preview()
        self.assertIsNotNone(dialog.ghost)
        dialog.reject()
        self.assertIsNone(dialog.ghost)
        self.assertEqual(self.doc.First.LinkPlacement, before)
        dialog = self.launch()
        dialog.preview()
        self.doc.Nested.Placement.Base.x += 3
        self.assertIsNone(dialog.ghost)
        self.assertFalse(dialog.moveButton.isEnabled())
        self.doc.recompute()
        dialog.refresh()
        self.assertTrue(dialog.moveButton.isEnabled())
        dialog.preview()
        App.closeDocument(self.doc.Name)
        self.assertTrue(dialog.closed)
        self.assertIsNone(dialog.ghost)

    def testUndoRedoAndReopenSharedSource(self):
        old = self.shape()
        Move.move(self.doc.First, Move.review(self.doc.First), "Translate", "World", (8, 3, 2))
        moved = self.shape()
        self.doc.undo()
        self.doc.recompute()
        self.assertShape(self.shape(), old)
        self.doc.redo()
        self.doc.recompute()
        self.assertShape(self.shape(), moved)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Moved.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.assertShape(self.shape(), moved)
            self.doc.Bracket.Length = 15
            self.doc.recompute()
            self.assertAlmostEqual(self.shape().Volume, 15 * 7 * 5)
            self.assertAlmostEqual(linked_shape((self.doc.Second, [])).Volume, 15 * 7 * 5)

    def testInvalidInputContextAndNoop(self):
        expected = Move.review(self.doc.First)
        undo = self.doc.UndoCount
        self.assertFalse(Move.move(self.doc.First, expected, "Translate", "World", (0, 0, 0)))
        self.assertEqual(self.doc.UndoCount, undo)
        for mode, vector in (("Rotate", (0, 0, 0)), ("Translate", (float("nan"), 0, 0))):
            with self.assertRaises(ValueError):
                Move.move(self.doc.First, expected, mode, "World", vector, 20)
        self.doc.openTransaction("Owner edit")
        self.doc.Second.Label = "Owner occurrence"
        with self.assertRaisesRegex(ValueError, "transaction"):
            Move.move(self.doc.First, expected, "Translate", "World", (1, 0, 0))
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        consumer = self.doc.addObject("App::FeaturePython", "Mate")
        consumer.addProperty("App::PropertyLink", "Input")
        consumer.Input = self.doc.First
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "relationship"):
            Move.review(self.doc.First)

    def testFailureRollbackAndFreshFrameRequired(self):
        before = App.Placement(self.doc.First.LinkPlacement)
        expected = Move.review(self.doc.First)
        original = Move.review
        calls = []
        def fail_after_update(link):
            calls.append(link)
            if len(calls) == 2:
                raise ValueError("Injected post-move failure")
            return original(link)
        with patch.object(Move, "review", side_effect=fail_after_update):
            with self.assertRaisesRegex(ValueError, "Injected"):
                Move.move(self.doc.First, expected, "Translate", "World", (10, 0, 0))
        self.assertEqual(self.doc.First.LinkPlacement, before)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.doc.Assembly.Placement.Base.x += 2
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "changed"):
            Move.move(self.doc.First, expected, "Translate", "World", (1, 0, 0))
