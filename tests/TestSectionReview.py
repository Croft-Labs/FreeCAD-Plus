# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Section review, geometry, persistence and user interaction checks."""
from pathlib import Path
import tempfile
import unittest
import re
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import SectionReview as Review
import SectionReviewGui as UI


def fixture(doc):
    box = doc.addObject("Part::Box", "Block")
    box.Length, box.Width, box.Height = 10, 8, 6
    plane = doc.addObject("Part::Feature", "CuttingSurface")
    plane.Shape = Part.makePlane(50, 30, App.Vector(-10, -10, 3))
    doc.recompute()
    return box, plane


class TestSectionReview(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("SectionReviewTest")
        self.doc.UndoMode = 1
        self.box, self.plane = fixture(self.doc)
        self.dialogs = []
        Gui.Selection.clearSelection()

    def tearDown(self):
        for dialog in self.dialogs:
            if not dialog.closed:
                dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def refs(self):
        return Review.Input(self.box), Review.Input(self.plane)

    def content(self):
        result = []
        for obj in self.doc.Objects:
            # Native Content is an XML fragment; property status includes transient flags.
            content = re.sub(r' status="[0-9]+"', '', obj.Content)
            result.append((obj.Name, content, obj.Visibility,
                           obj.Shape.exportBrepToString()))
        return result

    def launch(self, preselect=True):
        Gui.Selection.clearSelection()
        if preselect:
            Gui.Selection.addSelection(self.box)
            Gui.Selection.addSelection(self.plane)
        Gui.runCommand("Part_SectionReview")
        dialog = UI._dialogs[-1]
        self.dialogs.append(dialog)
        return dialog

    def test_preview_is_analytic_and_does_not_change_document(self):
        before, undo = self.content(), self.doc.UndoCount
        documents = set(App.listDocuments())
        report = Review.probe(*self.refs())
        self.assertEqual(report["edges"], 4)
        self.assertAlmostEqual(report["length"], 36)
        self.assertAlmostEqual(report["shape"].BoundBox.ZMin, 3)
        self.assertEqual(self.content(), before)
        self.assertEqual(self.doc.UndoCount, undo)
        self.assertEqual(set(App.listDocuments()), documents)
        self.assertEqual(App.ActiveDocument, self.doc)

    def test_placed_inputs_multiple_loops_and_approximation(self):
        other = Part.makeBox(4, 4, 6, App.Vector(20, 0, 0))
        compound = self.doc.addObject("Part::Feature", "TwoSolids")
        compound.Shape = Part.makeCompound([self.box.Shape, other])
        transform = App.Placement(App.Vector(12, 9, 7), App.Rotation(App.Vector(1, 1, 0), 30))
        compound.Placement = transform
        self.plane.Placement = transform
        self.doc.recompute()
        report = Review.probe(Review.Input(compound), Review.Input(self.plane), True)
        self.assertEqual(report["edges"], 8)
        self.assertAlmostEqual(report["length"], 52)
        self.assertEqual(len(Part.sortEdges(report["shape"].Edges)), 2)
        created = Review.create(report)
        self.assertTrue(created.Approximation)
        self.assertAlmostEqual(created.Shape.Length, 52)
        self.assertEqual(created.Base, compound)

    def test_disjoint_point_touch_and_coplanar_are_distinct(self):
        self.plane.Placement.Base.z = 20
        self.doc.recompute()
        report = Review.probe(*self.refs())
        self.assertEqual(report["edges"], 0)
        count = len(self.doc.Objects)
        with self.assertRaisesRegex(ValueError, "No intersection curves"):
            Review.create(report)
        self.assertEqual(len(self.doc.Objects), count)
        self.plane.Placement.Base.z = -3
        self.doc.recompute()
        coplanar = Review.probe(*self.refs())
        self.assertEqual(coplanar["edges"], 4)
        self.assertAlmostEqual(coplanar["length"], 36)
        touch = self.doc.addObject("Part::Box", "PointTouch")
        touch.Placement.Base = App.Vector(10, 8, 6)
        self.doc.recompute()
        point = Review.probe(Review.Input(self.box), Review.Input(touch))
        self.assertEqual(point["edges"], 0)
        self.assertGreater(point["vertices"], 0)

    def test_native_links_recompute_undo_redo_and_reopen(self):
        before = self.content()
        result = Review.create(Review.probe(*self.refs()))
        self.assertEqual(result.TypeId, "Part::Section")
        self.assertEqual((result.Base, result.Tool), (self.box, self.plane))
        self.assertEqual(self.content()[:2], before)
        self.doc.undo()
        self.assertIsNone(self.doc.getObject("Section"))
        self.doc.redo()
        result = self.doc.Section
        extrusion = self.doc.addObject("Part::Extrusion", "Downstream")
        extrusion.Base = result
        extrusion.Dir = App.Vector(0, 0, 2)
        extrusion.Solid = False
        self.doc.recompute()
        self.assertAlmostEqual(extrusion.Shape.Area, 72)
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "Section.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            self.box, self.plane = self.doc.Block, self.doc.CuttingSurface
            self.box.Length = 20
            self.doc.recompute()
            self.assertAlmostEqual(self.doc.Section.Shape.Length, 56)
            self.assertAlmostEqual(self.doc.Downstream.Shape.Area, 112)
            self.assertTrue(self.box.Visibility)
            self.assertTrue(self.plane.Visibility)

    def test_whole_body_retains_tip_and_sources(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        tip = body.newObject("PartDesign::Feature", "TipSolid")
        tip.Shape = self.box.Shape.copy()
        body.Tip = tip
        self.doc.recompute()
        before = body.Shape.exportBrepToString()
        result = Review.create(Review.probe(Review.Input(body), Review.Input(self.plane)))
        self.assertEqual(body.Tip, tip)
        self.assertEqual(body.Shape.exportBrepToString(), before)
        self.assertEqual(result.Base, body)
        self.assertAlmostEqual(result.Shape.Length, 36)

    def test_stale_context_and_unsupported_inputs_are_refused(self):
        refs = self.refs()
        self.box.Length = 12
        with self.assertRaises(ValueError):
            Review.probe(*refs)
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "changed"):
            Review.probe(*refs)
        with self.assertRaisesRegex(ValueError, "different"):
            Review.probe(Review.Input(self.box), Review.Input(self.box))
        link = self.doc.addObject("App::Link", "Occurrence")
        link.setLink(self.box)
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "whole root"):
            Review.Input(link)
        parent = self.doc.addObject("App::Part", "Container")
        parent.addObject(self.box)
        with self.assertRaisesRegex(ValueError, "whole root"):
            Review.Input(self.box)
        parent.removeObject(self.box)
        self.doc.recompute()
        refs = self.refs()
        self.doc.openTransaction("Owner edit")
        try:
            with self.assertRaisesRegex(ValueError, "transaction"):
                Review.probe(*refs)
        finally:
            self.doc.abortTransaction()

    def test_command_capture_preview_cancel_and_invalidation(self):
        before = self.content()
        dialog = self.launch(False)
        dialog.preview()
        self.assertFalse(dialog.createButton.isEnabled())
        for index, obj in enumerate((self.box, self.plane)):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
            dialog.capture(index)
        dialog.preview()
        self.assertTrue(dialog.createButton.isEnabled(), dialog.message.text())
        self.assertIsNotNone(dialog.ghost)
        self.assertEqual(self.content(), before)
        dialog.approximation.setChecked(True)
        self.assertIsNone(dialog.ghost)
        self.assertFalse(dialog.createButton.isEnabled())
        dialog.preview()
        dialog.reject()
        self.assertEqual(self.content(), before)
        second = self.launch()
        second.preview()
        self.box.Length = 15
        self.assertIsNone(second.ghost)
        self.assertFalse(second.createButton.isEnabled())
        self.doc.recompute()
        second.preview()
        self.assertIn("changed", second.message.text())
        self.assertFalse(second.createButton.isEnabled())

    def test_command_empty_result_and_explicit_create(self):
        dialog = self.launch()
        dialog.preview()
        dialog.commit()
        self.assertTrue(dialog.closed)
        self.assertEqual(dialog.result.TypeId, "Part::Section")
        self.assertEqual(dialog.result.Base, self.box)
        self.plane.Placement.Base.z = 20
        self.doc.recompute()
        second = self.launch()
        second.preview()
        self.assertIn("No intersection curves", second.message.text())
        self.assertFalse(second.createButton.isEnabled())
        self.assertIsNone(second.ghost)

    def test_failed_creation_rolls_back_without_orphans(self):
        preview = Review.probe(*self.refs())
        invalid = dict(preview, edges=preview["edges"] + 1)
        before = self.content()
        with patch.object(Review, "probe", return_value=invalid):
            with self.assertRaisesRegex(ValueError, "did not match"):
                Review.create(preview)
        self.assertEqual(self.content(), before)
        self.assertFalse(self.doc.HasPendingTransaction)
