# SPDX-License-Identifier: LGPL-2.1-or-later
"""Single-occurrence replacement against native link geometry and persistence."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtWidgets
from freecad.gui import OccurrenceReplace as Replace
from freecad.gui import OccurrenceAppearance as Appearance
from TestOccurrenceMove import make_fixture


def fixture():
    doc = make_fixture()
    target = doc.addObject("Part::Box", "Replacement")
    target.Length, target.Width, target.Height = 16, 4, 7
    target.Placement = App.Placement(App.Vector(-4, 3, 2), App.Rotation(App.Vector(0, 1, 0), 25))
    target.Visibility = False
    doc.recompute()
    return doc


class TestOccurrenceReplace(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = fixture()

    def tearDown(self):
        for dialog in list(Replace._dialogs):
            dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def shape(self, name="First"):
        return Part.getShape(self.doc.Assembly, "Nested." + name + ".", needSubElement=True, transform=True)

    def assertShape(self, actual, expected):
        self.assertAlmostEqual(actual.Volume, expected.Volume, places=6)
        self.assertAlmostEqual(actual.common(expected).Volume, expected.Volume, places=6)

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.First)
        Gui.runCommand("Std_ReplaceOccurrenceSource")
        Gui.updateGui()
        dialog = Replace._dialogs[-1]
        index = next((i for i in range(dialog.sources.count())
                      if tuple(dialog.sources.itemData(i)) == Replace.identity(self.doc.Replacement)), -1)
        self.assertGreaterEqual(index, 0)
        dialog.sources.setCurrentIndex(index)
        return dialog

    def testNativePlacementPreviewAndOtherOccurrenceIsolation(self):
        for transform in (False, True):
            with self.subTest(transform=transform):
                self.doc.First.LinkTransform = transform
                self.doc.recompute()
                source = self.doc.First.LinkedObject
                source_brep = source.Shape.exportBrepToString()
                before = (self.doc.First.ID, self.doc.First.Label, self.doc.First.LinkPlacement)
                other = self.shape("Second")
                expected = Replace.review(self.doc.First, self.doc.Replacement)
                preview = Replace.candidate(self.doc.First, self.doc.Replacement, expected)
                Replace.replace(self.doc.First, self.doc.Replacement, expected)
                self.assertShape(self.shape(), preview)
                self.assertShape(self.shape("Second"), other)
                self.assertEqual(self.doc.First.LinkedObject, self.doc.Replacement)
                self.assertEqual(self.doc.Second.LinkedObject, self.doc.Bracket)
                self.assertEqual(before, (self.doc.First.ID, self.doc.First.Label, self.doc.First.LinkPlacement))
                self.assertEqual(source.Shape.exportBrepToString(), source_brep)
                self.doc.undo()
                self.doc.recompute()
                self.assertEqual(self.doc.First.LinkedObject, source)

    def testWholeBodyReplacementAndNativeTip(self):
        body = self.doc.addObject("PartDesign::Body", "NewBody")
        tip = body.newObject("PartDesign::AdditiveBox", "Tip")
        tip.Length, tip.Width, tip.Height = 12, 6, 3
        body.Placement = App.Placement(App.Vector(5, 4, 3), App.Rotation(App.Vector(1, 0, 0), 20))
        self.doc.recompute()
        self.doc.First.LinkTransform = True
        self.doc.recompute()
        expected = Replace.review(self.doc.First, body)
        preview = Replace.candidate(self.doc.First, body, expected)
        Replace.replace(self.doc.First, body, expected)
        self.assertShape(self.shape(), preview)
        self.assertEqual(body.Tip, tip)
        self.assertAlmostEqual(self.shape().Volume, 216)

    def testUniformAppearanceVisibilityAndInheritedAppearance(self):
        link = self.doc.First
        Appearance.apply(link, Appearance.state(link), False, True, (.8, .2, .1), 35)
        values = Appearance._material_values(link.ViewObject.ShapeAppearance[0])
        expected = Replace.review(link, self.doc.Replacement)
        Replace.replace(link, self.doc.Replacement, expected)
        self.assertFalse(link.Visibility)
        self.assertTrue(link.ViewObject.OverrideMaterial)
        self.assertEqual(Appearance._material_values(link.ViewObject.ShapeAppearance[0]), values)
        self.doc.undo()
        self.doc.recompute()
        Appearance.apply(link, Appearance.state(link), True, False, (0, 0, 0), 0)
        Replace.replace(link, self.doc.Replacement, Replace.review(link, self.doc.Replacement))
        self.assertFalse(link.ViewObject.OverrideMaterial)
        self.assertTrue(link.Visibility)

    def testPreviewCancelAndStaleDocumentCleanup(self):
        dialog = self.launch()
        self.assertTrue(dialog.replaceButton.isEnabled(), dialog.message.text())
        objects, undo = list(self.doc.Objects), self.doc.UndoCount
        root = Gui.activeDocument().activeView().getSceneGraph()
        count = root.getNumChildren()
        dialog.previewButton.click()
        self.assertIsNotNone(dialog.ghost, dialog.message.text())
        self.assertEqual(root.getNumChildren(), count + 1)
        self.assertEqual((list(self.doc.Objects), self.doc.UndoCount), (objects, undo))
        dialog.cancelButton.click()
        self.assertEqual(root.getNumChildren(), count)
        self.assertEqual(self.doc.First.LinkedObject, self.doc.Bracket)
        dialog = self.launch()
        dialog.preview()
        self.doc.Replacement.Length = 20
        self.assertIsNone(dialog.ghost)
        self.assertFalse(dialog.replaceButton.isEnabled())
        self.doc.recompute()
        dialog.reviewButton.click()
        self.assertTrue(dialog.replaceButton.isEnabled(), dialog.message.text())
        dialog.preview()
        App.closeDocument(self.doc.Name)
        self.assertTrue(dialog.closed)
        self.assertIsNone(dialog.ghost)

    def testNativeCommandCommitUndoRedoReopen(self):
        dialog = self.launch()
        before = self.shape()
        undo = self.doc.UndoCount
        dialog.preview()
        dialog.replaceButton.click()
        self.assertTrue(dialog.closed, dialog.message.text())
        self.assertIsNone(dialog.ghost)
        self.assertEqual(self.doc.UndoCount, undo + 1)
        replaced = self.shape()
        self.doc.undo()
        self.doc.recompute()
        self.assertShape(self.shape(), before)
        self.doc.redo()
        self.doc.recompute()
        self.assertShape(self.shape(), replaced)
        with tempfile.TemporaryDirectory() as directory:
            filename = str(Path(directory) / "Replacement.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            self.doc.recompute()
            self.assertEqual(self.doc.First.LinkedObject, self.doc.Replacement)
            self.assertEqual(self.doc.Second.LinkedObject, self.doc.Bracket)
            self.assertShape(self.shape(), replaced)
            other = self.shape("Second")
            self.doc.Replacement.Length = 22
            self.doc.recompute()
            self.assertAlmostEqual(self.shape().Volume, 22 * 4 * 7)
            self.assertShape(self.shape("Second"), other)

    def testConsumersAndUnsupportedInputsAreRefused(self):
        link, target = self.doc.First, self.doc.Replacement
        before = link.LinkedObject
        with self.assertRaises(ValueError):
            Replace.review(link, before)
        consumer = self.doc.addObject("Part::Feature", "Consumer")
        consumer.addProperty("App::PropertyLink", "Input")
        consumer.Input = link
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "consumed"):
            Replace.review(link, target)
        self.doc.removeObject(consumer.Name)
        link.Scale = 2
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Replace.review(link, target)
        link.Scale = 1
        self.doc.recompute()
        parent = self.doc.addObject("App::Part", "SourceContainer")
        parent.addObject(target)
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Replace.review(link, target)
        self.assertEqual(link.LinkedObject, before)

    def testStaleIdentityOwnerTransactionAndRollback(self):
        link, target = self.doc.First, self.doc.Replacement
        expected = Replace.review(link, target)
        self.doc.openTransaction("Owner")
        with self.assertRaises(ValueError):
            Replace.replace(link, target, expected)
        self.doc.abortTransaction()
        target.Width = target.Width.Value + 1
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Replace.replace(link, target, expected)
        expected = Replace.review(link, target)
        original_review = Replace.Move.review
        def fail_after_relink(obj):
            if obj.LinkedObject == target:
                raise ValueError("Injected post-relink validation failure")
            return original_review(obj)
        before = (link.LinkedObject, link.LinkPlacement, self.doc.UndoCount)
        with patch.object(Replace.Move, "review", side_effect=fail_after_relink):
            with self.assertRaisesRegex(ValueError, "post-relink"):
                Replace.replace(link, target, expected)
        self.assertEqual(before, (link.LinkedObject, link.LinkPlacement, self.doc.UndoCount))
        self.assertFalse(self.doc.HasPendingTransaction)

    def testSourceDeletedAndEmptyPickerRecovery(self):
        dialog = self.launch()
        self.doc.removeObject(self.doc.Replacement.Name)
        self.doc.recompute()
        self.assertFalse(dialog.replaceButton.isEnabled())
        dialog.refresh()
        self.assertIn("No other root solid", dialog.message.text())
        self.assertFalse(dialog.previewButton.isEnabled())
        dialog.reject()
        command = Gui.Command.get("Std_ReplaceOccurrenceSource")
        self.assertIsNotNone(command)
        actions = [action for menu in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                   for action in menu.actions()]
        self.assertTrue(any("Replace occurrence source" in action.text() for action in actions))
