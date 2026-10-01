# SPDX-License-Identifier: LGPL-2.1-or-later
"""Exercise the native sketch-edit freedom controls and solver transitions."""
import tempfile
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide import QtCore, QtWidgets


def settle():
    Gui.updateGui()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(180, loop.quit)
    loop.exec_()


class TestSketchFreedom(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("SketcherWorkbench")
        self.doc = App.newDocument("SketchFreedom")
        self.doc.UndoMode = 1
        self.sketch = self.doc.addObject("Sketcher::SketchObject", "Profile")
        self.sketch.addGeometry(Part.Circle(App.Vector(3, 4, 0), App.Vector(0, 0, 1), 5))
        self.sketch.addConstraint(Sketcher.Constraint("Radius", 0, 5.))
        self.doc.recompute()

    def tearDown(self):
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()

    def edit(self):
        self.assertTrue(Gui.activeDocument().setEdit(self.sketch.Name))
        settle()
        window = Gui.getMainWindow()
        self.button = window.findChild(QtWidgets.QPushButton, "selectSketchFreedom")
        self.message = window.findChild(QtWidgets.QLabel, "sketchFreedomExplanation")
        self.assertIsNotNone(self.button)
        self.assertIsNotNone(self.message)
        return self.message.text()

    def refresh(self):
        self.sketch.solve()
        self.doc.recompute()
        settle()

    def test_selects_native_free_geometry_without_editing_model(self):
        self.sketch.addGeometry(Part.LineSegment(App.Vector(-10, 0, 0), App.Vector(-10, 8, 0)))
        self.sketch.addConstraint(Sketcher.Constraint("Block", 1))
        self.doc.recompute()
        self.edit()
        self.assertTrue(self.button.isEnabled())
        self.assertIn("coupled", self.message.text())
        self.assertIn("Construction", self.message.text())
        geometry = [g.toShape().exportBrepToString() for g in self.sketch.Geometry]
        constraints = [(c.Type, c.Value, c.Driving) for c in self.sketch.Constraints]
        undo = self.doc.UndoCount
        Gui.Selection.clearSelection()
        self.button.click()
        selection = Gui.Selection.getSelectionEx()
        self.assertTrue(selection)
        self.assertTrue(all(s.Object == self.sketch for s in selection))
        names = [n for s in selection for n in s.SubElementNames]
        self.assertTrue(names)
        self.assertNotIn("Edge2", names)
        self.assertEqual([g.toShape().exportBrepToString() for g in self.sketch.Geometry], geometry)
        self.assertEqual([(c.Type, c.Value, c.Driving) for c in self.sketch.Constraints], constraints)
        self.assertEqual(self.doc.UndoCount, undo)

    def test_constraint_transition_undo_redo_and_reopen(self):
        self.edit()
        self.doc.openTransaction("Locate circle")
        self.sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 3, -1, 1))
        self.doc.commitTransaction()
        self.refresh()
        self.assertFalse(self.button.isEnabled())
        self.assertIn("No remaining", self.message.text())
        self.assertTrue(self.sketch.FullyConstrained)
        self.doc.undo()
        self.doc.recompute()
        settle()
        self.assertTrue(self.button.isEnabled())
        self.doc.redo()
        self.doc.recompute()
        settle()
        self.assertFalse(self.button.isEnabled())
        self.assertTrue(self.sketch.FullyConstrained)
        Gui.activeDocument().resetEdit()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Freedom.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.sketch = self.doc.Profile
            self.edit()
            self.assertFalse(self.button.isEnabled())
            self.assertIn("Reference dimensions", self.message.text())

    def test_conflict_disables_freedom_until_repaired(self):
        self.edit()
        index = self.sketch.addConstraint(Sketcher.Constraint("Radius", 0, 7.))
        self.refresh()
        self.assertFalse(self.button.isEnabled())
        self.assertIn("solver issue", self.message.text())
        Gui.Selection.clearSelection()
        self.button.click()
        self.assertFalse(Gui.Selection.getSelection())
        self.sketch.delConstraint(index)
        self.refresh()
        self.assertTrue(self.button.isEnabled())

    def test_redundancy_is_not_presented_as_free_geometry(self):
        self.sketch.addConstraint(Sketcher.Constraint("Radius", 0, 5.))
        self.doc.recompute()
        self.edit()
        self.assertFalse(self.button.isEnabled())
        self.assertIn("solver issue", self.message.text())

    def test_reference_dimension_does_not_remove_construction_freedom(self):
        self.sketch.toggleConstruction(0)
        self.sketch.setDriving(0, False)
        self.doc.recompute()
        self.edit()
        self.assertTrue(self.button.isEnabled())
        self.assertFalse(self.sketch.Constraints[0].Driving)
        self.button.click()
        self.assertTrue(Gui.Selection.getSelectionEx())
        self.assertTrue(self.sketch.getConstruction(0))
        self.assertFalse(self.sketch.Constraints[0].Driving)

    def test_empty_sketch_explains_unavailable_selection(self):
        self.sketch.delGeometry(0)
        self.doc.recompute()
        self.edit()
        self.assertFalse(self.button.isEnabled())
        self.assertIn("Add geometry", self.message.text())

    def test_body_sketch_off_origin_preserves_placement(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        body.addObject(self.sketch)
        body.Placement.Base = App.Vector(10000, 20000, 0)
        self.sketch.Placement = App.Placement(App.Vector(2, 3, 4), App.Rotation(App.Vector(1, 0, 0), 35))
        self.doc.recompute()
        before = (body.Placement.toMatrix().A, self.sketch.Placement.toMatrix().A)
        self.edit()
        self.button.click()
        self.assertTrue(Gui.Selection.getSelectionEx())
        self.assertEqual((body.Placement.toMatrix().A, self.sketch.Placement.toMatrix().A), before)
