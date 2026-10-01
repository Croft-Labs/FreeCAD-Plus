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
import SketchReuse as Reuse
import SketchReuseGui as UI


def make_fixture():
    doc = App.newDocument("SketchReuse")
    doc.UndoMode = 1
    sketch = doc.addObject("Sketcher::SketchObject", "Slot")
    v = App.Vector
    sketch.addGeometry([
        Part.LineSegment(v(0, -3, 0), v(20, -3, 0)),
        Part.ArcOfCircle(Part.Circle(v(20, 0, 0), v(0, 0, 1), 3), -math.pi/2, math.pi/2),
        Part.LineSegment(v(20, 3, 0), v(0, 3, 0)),
        Part.ArcOfCircle(Part.Circle(v(0, 0, 0), v(0, 0, 1), 3), math.pi/2, 3*math.pi/2)])
    sketch.addConstraint([
        Sketcher.Constraint("Tangent", 0, 2, 1, 1),
        Sketcher.Constraint("Tangent", 1, 2, 2, 1),
        Sketcher.Constraint("Tangent", 2, 2, 3, 1),
        Sketcher.Constraint("Tangent", 3, 2, 0, 1),
        Sketcher.Constraint("Horizontal", 0), Sketcher.Constraint("Horizontal", 2),
        Sketcher.Constraint("Distance", 0, 20.), Sketcher.Constraint("Radius", 1, 3.),
        Sketcher.Constraint("DistanceX", 3, 3, 0.), Sketcher.Constraint("DistanceY", 3, 3, 0.)])
    sketch.renameConstraint(6, "StraightLength")
    sketch.renameConstraint(7, "EndRadius")
    # A construction datum must survive reuse without entering the solid profile.
    index = sketch.addGeometry(Part.LineSegment(v(0, 0, 0), v(20, 0, 0)), True)
    sketch.addConstraint(Sketcher.Constraint("Block", index))
    sketch.Placement = App.Placement(v(10, 7, 2), App.Rotation(v(1, 0, 0), 25))
    doc.recompute()
    return doc, sketch


class TestSketchReuse(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("SketcherWorkbench")
        self.doc, self.sketch = make_fixture()
        self.dialogs = []

    def tearDown(self):
        for dialog in self.dialogs + list(UI._dialogs):
            if not dialog.closed:
                dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def test_slot_constraints_construction_transform_and_independent_edits(self):
        self.assertEqual(self.sketch.DoF, 0)
        expected = Reuse.review(self.sketch)
        original = Reuse.constraint_signature(self.sketch)
        placement = App.Placement(self.sketch.Placement)
        result = Reuse.create_copy(self.sketch, expected, "Second slot", (40, 10, 5), 90)
        self.assertEqual(Reuse.constraint_signature(result), original)
        self.assertTrue(result.getConstruction(4))
        self.assertEqual(result.OutList, [])
        point = self.sketch.Placement.multVec(App.Vector(40, 10, 5))
        self.assertTrue(result.Placement.Base.isEqual(point, 1e-7))
        direction = self.sketch.Placement.Rotation.multVec(App.Vector(0, 1, 0))
        self.assertTrue(result.Placement.Rotation.multVec(App.Vector(1, 0, 0)).isEqual(direction, 1e-7))
        self.assertTrue(self.sketch.Placement.isSame(placement, 1e-9))
        result.setDatum(7, App.Units.Quantity("4 mm"))
        self.doc.recompute()
        self.assertEqual(result.DoF, 0)
        self.assertAlmostEqual(result.getDatum(7).Value, 4)
        self.assertAlmostEqual(self.sketch.getDatum(7).Value, 3)
        self.assertEqual(len(result.Shape.Wires), 1)
        self.assertTrue(result.Shape.Wires[0].isClosed())

    def test_undo_redo_reopen_and_downstream_solid(self):
        undo = self.doc.UndoCount
        result = Reuse.create_copy(self.sketch, Reuse.review(self.sketch), "Slot copy", (40, 0, 0), 45)
        name = result.Name
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.doc.undo()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo()
        self.doc.recompute()
        extrusion = self.doc.addObject("Part::Extrusion", "CopySolid")
        extrusion.Base = self.doc.getObject(name)
        extrusion.DirMode = "Normal"
        extrusion.LengthFwd = 5
        extrusion.Solid = True
        self.doc.recompute()
        self.assertTrue(extrusion.Shape.isValid())
        self.assertAlmostEqual(extrusion.Shape.Volume, (120 + math.pi * 9) * 5, places=4)
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "CopiedSlot.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            copied = self.doc.getObject(name)
            copied.setDatum(7, App.Units.Quantity("4 mm"))
            self.doc.recompute()
            self.assertAlmostEqual(self.doc.CopySolid.Shape.Volume, (160 + math.pi * 16) * 5, places=4)
            self.assertAlmostEqual(self.doc.Slot.getDatum(7).Value, 3)

    def test_preview_and_commit_agree_without_preview_model_mutation(self):
        dialog = UI.CopyDialog(self.sketch)
        self.dialogs.append(dialog)
        dialog.offset[0].setValue(40)
        dialog.angle.setValue(90)
        state = (len(self.doc.Objects), self.doc.UndoCount, Reuse.review(self.sketch))
        view = Gui.activeDocument().activeView()
        view.fitAll()
        camera = view.getCamera()
        root = view.getSceneGraph()
        count = root.getNumChildren()
        dialog.preview()
        self.assertIsNotNone(dialog.ghost, dialog.message.text())
        self.assertNotEqual(view.getCamera(), camera)
        self.assertEqual(root.getNumChildren(), count + 1)
        ghost = dialog.ghost
        placement, shape = Reuse.candidate(self.sketch, dialog.expected, *dialog.values())
        self.assertEqual(state, (len(self.doc.Objects), self.doc.UndoCount, Reuse.review(self.sketch)))
        dialog.createCopy()
        self.assertTrue(dialog.closed, dialog.message.text())
        self.assertEqual(root.findChild(ghost.node), -1)
        copy = self.doc.Objects[-1]
        self.assertTrue(copy.Placement.isSame(placement, 1e-7))
        self.assertAlmostEqual(copy.Shape.distToShape(shape)[0], 0, places=7)
        self.assertEqual(len(copy.Shape.Vertexes), len(shape.Vertexes))
        for actual, predicted in zip(copy.Shape.Vertexes, shape.Vertexes):
            self.assertTrue(actual.Point.isEqual(predicted.Point, 1e-7))

    def test_cancel_changes_invalidate_and_document_close_cleans_preview(self):
        dialog = UI.CopyDialog(self.sketch)
        self.dialogs.append(dialog)
        dialog.preview()
        self.assertIsNotNone(dialog.ghost)
        dialog.offset[0].setValue(25)
        self.assertIsNone(dialog.ghost)
        dialog.preview()
        self.sketch.setDatum(7, App.Units.Quantity("4 mm"))
        self.assertIsNone(dialog.ghost)
        self.assertFalse(dialog.copyButton.isEnabled())
        self.doc.recompute()
        dialog.review()
        self.assertTrue(dialog.copyButton.isEnabled(), dialog.message.text())
        dialog.reject()
        self.assertEqual(len(self.doc.Objects), 1)
        dialog = UI.CopyDialog(self.sketch)
        self.dialogs.append(dialog)
        dialog.preview()
        App.closeDocument(self.doc.Name)
        self.assertTrue(dialog.closed)
        self.assertIsNone(dialog.ghost)

    def test_external_expression_support_and_nested_inputs_are_explicitly_refused(self):
        self.sketch.setExpression("Constraints.EndRadius", "2 mm + 1 mm")
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "references"):
            Reuse.review(self.sketch)
        self.sketch.setExpression("Constraints.EndRadius", None)
        box = self.doc.addObject("Part::Box", "Support")
        self.doc.recompute()
        self.sketch.addExternal(box.Name, "Edge1")
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "references"):
            Reuse.review(self.sketch)
        self.sketch.delExternal(0)
        self.sketch.AttachmentSupport = [(box, ["Face1"])]
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "references"):
            Reuse.review(self.sketch)
        self.sketch.AttachmentSupport = None
        body = self.doc.addObject("PartDesign::Body", "Body")
        body.addObject(self.sketch)
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "root sketch"):
            Reuse.review(self.sketch)

    def test_stale_empty_transaction_and_failure_rollback(self):
        expected = Reuse.review(self.sketch)
        self.sketch.renameConstraint(7, "NewRadius")
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "changed"):
            Reuse.create_copy(self.sketch, expected, "Copy", (0, 0, 0), 0)
        expected = Reuse.review(self.sketch)
        self.doc.openTransaction("Owner edit")
        with self.assertRaisesRegex(ValueError, "transaction"):
            Reuse.create_copy(self.sketch, expected, "Copy", (0, 0, 0), 0)
        self.assertEqual(App.getActiveTransaction()[0], "Owner edit")
        self.doc.abortTransaction()
        before = (len(self.doc.Objects), self.doc.UndoCount)
        native = Reuse.review
        def fail(obj):
            if obj != self.sketch:
                raise ValueError("Injected copied result failure")
            return native(obj)
        with patch.object(Reuse, "review", side_effect=fail), self.assertRaises(ValueError):
            Reuse.create_copy(self.sketch, expected, "Copy", (0, 0, 0), 0)
        self.assertEqual(before, (len(self.doc.Objects), self.doc.UndoCount))
        self.assertEqual(expected, Reuse.review(self.sketch))

    def test_installed_command_and_invalid_numeric_input(self):
        self.assertIn("Sketcher_CopyReusable", Gui.listCommands())
        Gui.Selection.addSelection(self.sketch)
        Gui.runCommand("Sketcher_CopyReusable", 0)
        dialog = UI._dialogs[-1]
        self.assertTrue(dialog.copyButton.isEnabled(), dialog.message.text())
        dialog.reject()
        for offset, angle in (((float("nan"), 0, 0), 0), ((0, 0, 0), float("inf"))):
            with self.assertRaises(ValueError):
                Reuse.candidate(self.sketch, Reuse.review(self.sketch), offset, angle)
