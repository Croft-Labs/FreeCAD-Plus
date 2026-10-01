# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Validate Sketch candidate review and deliberate coincidence repair."""
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide import QtCore, QtWidgets


def make_fixture():
    doc = App.newDocument("SketchRepairReview")
    doc.UndoMode = 1
    sketch = doc.addObject("Sketcher::SketchObject", "Profile")
    points = [(0, 0), (20, 0), (20, 10), (0, 10), (0, 0.01)]
    for a, b in zip(points, points[1:]):
        sketch.addGeometry(Part.LineSegment(App.Vector(*a, 0), App.Vector(*b, 0)))
    for a, b in ((0, 1), (1, 2), (2, 3)):
        sketch.addConstraint(Sketcher.Constraint("Coincident", a, 2, b, 1))
    for kind, index in (("Horizontal", 0), ("Vertical", 1), ("Horizontal", 2), ("Vertical", 3)):
        sketch.addConstraint(Sketcher.Constraint(kind, index))
    sketch.addConstraint(Sketcher.Constraint("Distance", 0, 20))
    sketch.renameConstraint(7, "Width")
    sketch.addConstraint(Sketcher.Constraint("Distance", 1, 10))
    sketch.renameConstraint(8, "Height")
    doc.recompute()
    return doc


def make_conflict(doc):
    sketch = doc.addObject("Sketcher::SketchObject", "ConstrainedGap")
    for a, b in (((0, 0), (10, 0)), ((20.01, 0), (10.01, 0))):
        sketch.addGeometry(Part.LineSegment(App.Vector(*a, 0), App.Vector(*b, 0)))
    sketch.addConstraint([
        Sketcher.Constraint("Coincident", 0, 1, -1, 1),
        Sketcher.Constraint("Horizontal", 0), Sketcher.Constraint("Distance", 0, 10),
        Sketcher.Constraint("Horizontal", 1), Sketcher.Constraint("Distance", 1, 10),
        Sketcher.Constraint("DistanceX", 1, 1, 20.01),
        Sketcher.Constraint("DistanceY", 1, 1, 0)])
    doc.recompute()
    return sketch


class TestSketchRepairReview(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("SketcherWorkbench")
        self.doc = make_fixture()
        self.sketch = self.doc.Profile
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.sketch)
        Gui.runCommand("Sketcher_ValidateSketch")
        Gui.updateGui()
        self.tree = Gui.getMainWindow().findChild(QtWidgets.QTreeWidget, "coincidenceCandidates")
        self.assertIsNotNone(self.tree)
        self.panel = self.tree.parentWidget()
        self.status = self.panel.findChild(QtWidgets.QLabel, "coincidenceStatus")
        self.tolerance = self.panel.findChild(QtWidgets.QComboBox, "comboBoxTolerance")
        self.fix = self.panel.findChild(QtWidgets.QPushButton, "fixButton")
        self.find = self.panel.findChild(QtWidgets.QPushButton, "findButton")
        self.tolerance.setEditText("0.1")
        self.find.click()

    def checked(self, row=0):
        self.tree.topLevelItem(row).setCheckState(0, QtCore.Qt.Checked)

    def snapshot(self):
        return (self.sketch.GeometryCount, self.sketch.ConstraintCount,
                self.sketch.Shape.exportBrepToString(),
                [(c.Type, c.First, c.FirstPos, c.Second, c.SecondPos, c.Value)
                 for c in self.sketch.Constraints])

    def testFindReviewAndCloseAreReadOnly(self):
        before = self.snapshot()
        root = self.sketch.ViewObject.RootNode
        children = root.getNumChildren()
        self.launch()
        self.assertEqual(self.tree.topLevelItemCount(), 1)
        item = self.tree.topLevelItem(0)
        self.assertIn("Geometry", item.text(0))
        self.assertAlmostEqual(float(item.text(2)), 0.01, places=5)
        self.assertFalse(self.fix.isEnabled())
        self.tree.setCurrentItem(item)
        Gui.updateGui()
        self.assertEqual(root.getNumChildren(), children + 1)
        self.checked()
        self.assertTrue(self.fix.isEnabled())
        self.assertEqual(self.snapshot(), before)
        Gui.Control.closeDialog()
        Gui.updateGui()
        self.assertEqual(root.getNumChildren(), children)
        self.assertEqual(self.snapshot(), before)

    def testRepairUndoRedoPersistenceAndSolidResult(self):
        before = self.snapshot()
        self.launch()
        self.checked()
        self.fix.click()
        self.assertIn("Added 1", self.status.text())
        self.assertEqual(self.sketch.ConstraintCount, before[1] + 1)
        self.assertEqual(self.sketch.getDatum(7).Value, 20)
        self.assertEqual(self.sketch.getDatum(8).Value, 10)
        self.assertTrue(self.sketch.Shape.Wires[0].isClosed())
        self.assertFalse(self.doc.HasPendingTransaction)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.snapshot()[0:2], before[0:2])
        self.assertFalse(self.sketch.Shape.Wires[0].isClosed())
        self.doc.redo()
        self.doc.recompute()
        self.assertTrue(self.sketch.Shape.Wires[0].isClosed())
        Gui.Control.closeDialog()
        result = self.doc.addObject("Part::Extrusion", "Result")
        result.Base = self.sketch
        result.DirMode = "Normal"
        result.LengthFwd = 5
        result.Solid = True
        self.doc.recompute()
        self.assertTrue(result.Shape.isValid())
        self.assertAlmostEqual(result.Shape.Volume, 1000)
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Repaired.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.sketch = self.doc.Profile
            self.assertTrue(self.sketch.Shape.Wires[0].isClosed())
            self.assertAlmostEqual(self.doc.Result.Shape.Volume, 1000)
            self.sketch.setDatum(7, App.Units.Quantity("25 mm"))
            self.doc.recompute()
            self.assertAlmostEqual(self.doc.Result.Shape.Volume, 1250)

    def testToleranceAndConstructionChangesInvalidateCandidates(self):
        self.sketch.addGeometry(Part.LineSegment(App.Vector(40, 0, 0), App.Vector(45, 0, 0)), True)
        self.sketch.addGeometry(Part.LineSegment(App.Vector(45.02, 0, 0), App.Vector(50, 0, 0)), True)
        self.doc.recompute()
        self.launch()
        self.assertEqual(self.tree.topLevelItemCount(), 1)
        self.checked()
        ignore = self.panel.findChild(QtWidgets.QCheckBox, "checkBoxIgnoreConstruction")
        ignore.setChecked(False)
        self.assertEqual(self.tree.topLevelItemCount(), 0)
        self.assertFalse(self.fix.isEnabled())
        self.find.click()
        self.assertEqual(self.tree.topLevelItemCount(), 2)
        # Only repair the rectangle; the construction gap must remain.
        row = next(i for i in range(2) if float(self.tree.topLevelItem(i).text(2)) < 0.015)
        self.checked(row)
        self.fix.click()
        self.assertIn("Added 1", self.status.text())
        self.find.click()
        self.assertEqual(self.tree.topLevelItemCount(), 1)
        self.assertAlmostEqual(float(self.tree.topLevelItem(0).text(2)), 0.02, places=5)
        self.tolerance.setEditText("invalid")
        self.find.click()
        self.assertEqual(self.tree.topLevelItemCount(), 0)
        self.assertIn("tolerance", self.status.text())
        self.assertFalse(self.fix.isEnabled())
        self.tolerance.setEditText("0.001")
        self.find.click()
        self.assertIn("Other profile defects", self.status.text())

    def testSketchEditAndPendingTransactionDoNotApplyOldCandidates(self):
        other = self.doc.addObject("App::FeaturePython", "Other")
        self.doc.recompute()
        self.launch()
        self.checked()
        count = self.sketch.ConstraintCount
        self.doc.openTransaction("Other edit")
        other.Label = "Pending"
        self.fix.click()
        self.assertIn("transaction", self.status.text())
        self.assertEqual(self.sketch.ConstraintCount, count)
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        self.sketch.setDatum(7, App.Units.Quantity("22 mm"))
        self.assertEqual(self.tree.topLevelItemCount(), 0)
        self.assertFalse(self.fix.isEnabled())
        self.doc.recompute()
        self.find.click()
        expected = self.sketch.detectMissingPointOnPointConstraints(0.1, False)
        self.assertEqual(self.tree.topLevelItemCount(), expected)

    def testConflictingRepairRestoresOriginalConstraintsAndGeometry(self):
        self.doc.removeObject("Profile")
        self.sketch = make_conflict(self.doc)
        self.assertEqual(self.sketch.solve(), 0)
        before = self.snapshot()
        self.launch()
        self.assertEqual(self.tree.topLevelItemCount(), 1)
        self.checked()
        self.fix.click()
        self.assertIn("restored", self.status.text())
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertFalse(self.fix.isEnabled())
