# SPDX-License-Identifier: LGPL-2.1-or-later
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide import QtCore
import ConstraintRepair as Repair
import ConstraintRepairGui as UI
from SketchReuse import constraint_signature


def fixture(doc, name="Profile", conflicting=False):
    sketch = doc.addObject("Sketcher::SketchObject", name)
    sketch.addGeometry(Part.Circle(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 5))
    sketch.addConstraint(Sketcher.Constraint("Radius", 0, 5.))
    sketch.addConstraint(Sketcher.Constraint("Radius", 0, 7. if conflicting else 5.))
    sketch.renameConstraint(0, "DesignRadius")
    sketch.renameConstraint(1, "ExtraRadius")
    doc.recompute()
    return sketch


class TestConstraintRepair(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("SketcherWorkbench")
        self.doc = App.newDocument("ConstraintRepairTest")
        self.doc.UndoMode = 1
        self.sketch = fixture(self.doc)
        self.dialogs = []
        Gui.Selection.clearSelection()

    def tearDown(self):
        for dialog in self.dialogs + list(UI._dialogs):
            if not dialog.closed:
                dialog.reject()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def preview(self, indices=(1,)):
        return Repair.probe(self.sketch, Repair.snapshot(self.sketch), indices)

    def dialog(self):
        dialog = UI.RepairDialog(self.sketch, Gui.getMainWindow())
        self.dialogs.append(dialog)
        return dialog

    def testRedundantPreviewPreservesSourceAndDocumentContext(self):
        original, constraints = self.sketch.Content, constraint_signature(self.sketch)
        docs, undo, objects = set(App.listDocuments()), self.doc.UndoCount, len(self.doc.Objects)
        result = self.preview()
        self.assertIn("Redundant", result["before"]["state"])
        self.assertTrue(result["after"]["ok"], result)
        self.assertEqual(result["after"]["dof"], 2)
        self.assertEqual(result["after"]["state"], "Underconstrained")
        self.assertAlmostEqual(result["shape"].Edges[0].Curve.Radius, 5)
        self.assertEqual(self.sketch.Content, original)
        self.assertEqual(constraint_signature(self.sketch), constraints)
        self.assertEqual(set(App.listDocuments()), docs)
        self.assertEqual((self.doc.UndoCount, len(self.doc.Objects)), (undo, objects))
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(Gui.activeDocument().Document, self.doc)

    def testConflictingPreviewAndFailedSubset(self):
        self.sketch = fixture(self.doc, "Conflict", conflicting=True)
        result = self.preview()
        self.assertFalse(result["before"]["ok"])
        self.assertTrue(result["before"]["groups"]["Conflicting"], result["before"])
        self.assertTrue(result["after"]["ok"])
        self.assertAlmostEqual(result["shape"].Edges[0].Curve.Radius, 5)
        untouched = self.preview(())
        self.assertFalse(untouched["after"]["ok"])
        with self.assertRaises(ValueError):
            Repair.apply(self.sketch, untouched)

    def testApplyUndoRedoReopenAndDownstream(self):
        preview = self.preview()
        sketch_id = self.sketch.ID
        names = [c.Name for c in self.sketch.Constraints]
        count = self.doc.UndoCount
        Repair.apply(self.sketch, preview)
        self.assertEqual(self.doc.UndoCount, count + 1)
        self.assertEqual(self.sketch.ID, sketch_id)
        self.assertEqual([c.Name for c in self.sketch.Constraints], names)
        self.assertTrue(self.sketch.Constraints[0].IsActive)
        self.assertFalse(self.sketch.Constraints[1].IsActive)
        self.assertEqual(self.sketch.ConstraintCount, 2)
        self.doc.undo()
        self.doc.recompute()
        self.assertTrue(self.sketch.Constraints[1].IsActive)
        self.doc.redo()
        self.doc.recompute()
        self.assertFalse(self.sketch.Constraints[1].IsActive)
        solid = self.doc.addObject("Part::Extrusion", "Extrusion")
        solid.Base = self.sketch
        solid.Dir = App.Vector(0, 0, 4)
        solid.Solid = True
        self.doc.recompute()
        self.assertTrue(solid.Shape.isValid())
        self.assertAlmostEqual(solid.Shape.Volume, 100 * 3.141592653589793, places=6)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Repaired.FCStd"
            self.doc.saveAs(str(path))
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(str(path))
            self.sketch = self.doc.Profile
            self.assertFalse(self.sketch.Constraints[1].IsActive)
            self.sketch.setDatum(0, App.Units.Quantity("6 mm"))
            self.doc.recompute()
            self.assertAlmostEqual(self.doc.Extrusion.Shape.Volume, 144 * 3.141592653589793, places=6)

    def testChoiceCanReleaseFreedomWithoutDeletingDimensions(self):
        result = self.preview((0, 1))
        self.assertTrue(result["after"]["ok"])
        self.assertEqual(result["after"]["dof"], 3)
        Repair.apply(self.sketch, result)
        self.assertEqual([c.IsActive for c in self.sketch.Constraints], [False, False])
        self.assertEqual([c.Value for c in self.sketch.Constraints], [5., 5.])

    def testUiExplicitSelectionPreviewCancelAndApply(self):
        self.sketch.Placement.Base.x = 10000
        self.doc.recompute()
        Gui.Selection.addSelection(self.sketch)
        Gui.runCommand("Sketcher_ReviewConstraintRepair")
        dialog = UI._dialogs[-1]
        self.assertEqual(dialog.table.rowCount(), 2, dialog.message.text())
        self.assertEqual(dialog.selected(), ())
        self.assertFalse(dialog.applyButton.isEnabled())
        dialog.table.selectRow(1)
        dialog.select()
        self.assertEqual(Gui.Selection.getSelectionEx()[0].SubElementNames, ("Edge1",))
        dialog.table.item(1, 0).setCheckState(QtCore.Qt.Checked)
        dialog.preview()
        self.assertTrue(dialog.applyButton.isEnabled(), dialog.message.text())
        self.assertIsNotNone(dialog.ghost)
        view = Gui.activeDocument().activeView()
        width, height = view.getSize()
        for point in (App.Vector(9995, 0, 0), App.Vector(10005, 0, 0)):
            x, y = view.getPointOnScreen(point)
            self.assertTrue(0 <= x <= width and 0 <= y <= height, (x, y, width, height))
        dialog.reject()
        self.assertTrue(self.sketch.Constraints[1].IsActive)
        dialog = self.dialog()
        dialog.table.item(1, 0).setCheckState(QtCore.Qt.Checked)
        dialog.preview()
        dialog.commit()
        self.assertTrue(dialog.closed, dialog.message.text())
        self.assertFalse(self.sketch.Constraints[1].IsActive)

    def testStalePreviewAndOwnerTransactionGuards(self):
        preview = self.preview()
        self.sketch.Label = "Changed profile"
        with self.assertRaisesRegex(ValueError, "changed"):
            Repair.apply(self.sketch, preview)
        self.doc.openTransaction("Owner edit")
        try:
            with self.assertRaisesRegex(ValueError, "transaction"):
                self.preview()
        finally:
            self.doc.abortTransaction()
        for selected in ((20,), (-1,), (True,)):
            with self.assertRaises(ValueError):
                self.preview(selected)
        parent = self.doc.addObject("App::Part", "Part")
        parent.addObject(self.sketch)
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Repair.snapshot(self.sketch)

    def testRollbackAfterSourceSolveFailure(self):
        preview = self.preview()
        original = constraint_signature(self.sketch)
        solver = Repair.solver_info
        def fail_source(sketch):
            if sketch.Document == self.doc:
                raise RuntimeError("Injected source solve failure")
            return solver(sketch)
        with patch.object(Repair, "solver_info", side_effect=fail_source):
            with self.assertRaisesRegex(RuntimeError, "Injected"):
                Repair.apply(self.sketch, preview)
        self.assertEqual(constraint_signature(self.sketch), original)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(set(App.listDocuments()), {self.doc.Name})

    def testDialogInvalidationAndDocumentClose(self):
        dialog = self.dialog()
        dialog.table.item(1, 0).setCheckState(QtCore.Qt.Checked)
        dialog.preview()
        self.assertIsNotNone(dialog.ghost, dialog.message.text())
        self.sketch.Placement.Base.x = 4
        self.doc.recompute()
        self.assertIsNone(dialog.ghost)
        self.assertFalse(dialog.applyButton.isEnabled())
        dialog.review()
        self.assertEqual(dialog.selected(), ())
        App.closeDocument(self.doc.Name)
        self.assertTrue(dialog.closed)
