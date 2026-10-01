# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native shared-definition copies through the existing Move/Copy workflow."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad.gui import OccurrenceMove as Move
from freecad.gui import OccurrenceAppearance as Appearance
from TestOccurrenceMove import make_fixture


class TestOccurrenceCopy(unittest.TestCase):
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

    def shape(self, link):
        return Part.getShape(self.doc.Assembly, "Nested." + link.Name + ".",
                             needSubElement=True, transform=True)

    def sameShape(self, first, second):
        self.assertAlmostEqual(first.Volume, second.Volume, places=6)
        self.assertAlmostEqual(first.common(second).Volume, second.Volume, places=6)

    def copy(self, vector=(15, 0, 0), label="Copied bracket"):
        return Move.copy_occurrence(self.doc.First, Move.review(self.doc.First), label,
                                    "Translate", "World", vector)

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.First)
        Gui.runCommand("Std_MoveOccurrenceOnce")
        Gui.updateGui()
        dialog = Move._dialogs[-1]
        dialog.action.setCurrentIndex(1)
        return dialog

    def test_nested_copy_preserves_source_identity_and_original_placements(self):
        before = {obj.Name for obj in self.doc.Objects}
        placements = [App.Placement(o.Placement) for o in (self.doc.First, self.doc.Second, self.doc.Bracket)]
        expected = self.shape(self.doc.First)
        expected.translate(App.Vector(15, 0, 0))
        copied = self.copy()
        self.assertEqual({obj.Name for obj in self.doc.Objects} - before, {copied.Name})
        self.assertNotEqual(copied.ID, self.doc.First.ID)
        self.assertEqual(copied.LinkedObject, self.doc.Bracket)
        self.assertEqual(copied.getParentGeoFeatureGroup(), self.doc.Nested)
        self.assertEqual([o.Placement for o in (self.doc.First, self.doc.Second, self.doc.Bracket)], placements)
        self.sameShape(self.shape(copied), expected)

    def test_rotation_preview_and_native_source_transform_policies(self):
        for transform in (False, True):
            self.doc.First.LinkTransform = transform
            self.doc.recompute()
            reviewed = Move.review(self.doc.First)
            args = ("Rotate", "World", (1, 2, 3), 35, (4, 2, 1))
            _, ghost, _ = Move.candidate(self.doc.First, reviewed, *args)
            oracle = self.shape(self.doc.First)
            oracle.rotate(App.Vector(4, 2, 1), App.Vector(1, 2, 3), 35)
            copied = Move.copy_occurrence(self.doc.First, reviewed, "Rotated", *args)
            self.assertEqual(copied.LinkTransform, transform)
            self.sameShape(self.shape(copied), oracle)
            self.sameShape(self.shape(copied), ghost)

    def test_appearance_visibility_and_shared_definition_remain_native(self):
        link = self.doc.First
        Appearance.apply(link, Appearance.state(link), False, True, (.2, .6, .8), 40)
        self.doc.recompute()
        expected = Appearance.state(link)
        copied = self.copy()
        actual = Appearance.state(copied)
        for key in ("source", "visible", "override", "material", "source_materials"):
            self.assertEqual(actual[key], expected[key], key)
        self.assertFalse(self.doc.Bracket.Visibility)
        self.assertTrue(self.doc.Second.Visibility)

    def test_copy_ui_preview_cancel_and_commit(self):
        from freecad.gui import CommandSearch as Search
        self.assertEqual(Search.matching_rows(Search.catalog(), "copy component")[0][0],
                         "Std_MoveOccurrenceOnce")
        self.assertIn("sharing its definition", Search.HELP["Std_MoveOccurrenceOnce"])
        count, undo = len(self.doc.Objects), self.doc.UndoCount
        before = App.Placement(self.doc.First.LinkPlacement)
        dialog = self.launch()
        self.assertTrue(dialog.copyLabel.isEnabled())
        self.assertIn("copy", dialog.moveButton.text())
        dialog.offset[0].setValue(18)
        dialog.preview()
        self.assertIsNotNone(dialog.ghost, dialog.message.text())
        self.assertEqual(len(self.doc.Objects), count)
        self.assertEqual(self.doc.UndoCount, undo)
        dialog.reject()
        self.assertIsNone(dialog.ghost)
        self.assertEqual(self.doc.First.LinkPlacement, before)
        dialog = self.launch()
        dialog.copyLabel.setText("Owner copy")
        dialog.offset[0].setValue(18)
        dialog.preview()
        dialog.moveButton.click()
        self.assertTrue(dialog.closed, dialog.message.text())
        self.assertEqual(len(self.doc.Objects), count + 1)
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.assertEqual(self.doc.First.LinkPlacement, before)
        self.assertEqual(len([o for o in self.doc.Objects if o.Label == "Owner copy"]), 1)

    def test_undo_redo_reopen_and_source_edit_updates_all_copies(self):
        copied = self.copy()
        name = copied.Name
        expected = self.shape(copied)
        self.doc.undo()
        self.doc.recompute()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo()
        self.doc.recompute()
        self.sameShape(self.shape(self.doc.getObject(name)), expected)
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "LinkedCopy.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            copied = self.doc.getObject(name)
            self.assertEqual(copied.LinkedObject, self.doc.Bracket)
            self.sameShape(self.shape(copied), expected)
            self.doc.Bracket.Length = 15
            self.doc.recompute()
            for link in (copied, self.doc.First, self.doc.Second):
                self.assertAlmostEqual(self.shape(link).Volume, 15 * 7 * 5)

    def test_invalid_label_stale_frame_and_booked_transaction_refused(self):
        count = len(self.doc.Objects)
        for label in ("  ", "bad\x00label"):
            with self.assertRaises(ValueError):
                self.copy(label=label)
        expected = Move.review(self.doc.First)
        self.doc.Nested.Placement.Base.x += 1
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "changed"):
            Move.copy_occurrence(self.doc.First, expected, "Copy", "Translate", "World", (1, 0, 0))
        App.setActiveTransaction("Unrelated owner edit")
        try:
            with self.assertRaisesRegex(ValueError, "transaction"):
                self.copy()
        finally:
            App.closeActiveTransaction(True)
        self.assertEqual(len(self.doc.Objects), count)
        # Zero displacement is a deliberate coincident copy, not a move no-op.
        copied = self.copy((0, 0, 0))
        self.sameShape(self.shape(copied), self.shape(self.doc.First))

    def test_failed_copy_rolls_back_added_link_and_parent_membership(self):
        names = {o.Name for o in self.doc.Objects}
        members = list(self.doc.Nested.Group)
        original = Move.review
        def fail_copy(link):
            if link.Name not in names:
                raise ValueError("Injected copied-result failure")
            return original(link)
        with patch.object(Move, "review", side_effect=fail_copy):
            with self.assertRaisesRegex(ValueError, "Injected"):
                self.copy()
        self.assertEqual({o.Name for o in self.doc.Objects}, names)
        self.assertEqual(list(self.doc.Nested.Group), members)
        self.assertFalse(self.doc.HasPendingTransaction)
