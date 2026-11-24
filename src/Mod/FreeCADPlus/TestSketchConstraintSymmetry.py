# SPDX-License-Identifier: LGPL-2.1-or-later
"""Solver regressions for compatible symmetry redundancy (native Sketcher)."""
import os
from pathlib import Path
import unittest
import FreeCAD as App
import Part
import Sketcher


class TestSketchConstraintSymmetry(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument('ConstraintSymmetryTest')
        self.doc.UndoMode = 1
        self.sketch = self.doc.addObject('Sketcher::SketchObject', 'Sketch')

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def rectangle(self, vertical=False, centered=False):
        points = [(-10 if centered else 5, 3), (10 if centered else 25, 3),
                  (10 if centered else 25, 13), (-10 if centered else 5, 13)]
        if vertical:
            points = [(y, x) for x, y in points]
        for i, a in enumerate(points):
            b = points[(i + 1) % 4]
            self.sketch.addGeometry(Part.LineSegment(App.Vector(*a, 0), App.Vector(*b, 0)))
        for i in range(4):
            self.sketch.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % 4, 1))
            kind = 'Horizontal' if (i % 2 == 0) != vertical else 'Vertical'
            self.sketch.addConstraint(Sketcher.Constraint(kind, i))
        self.assertEqual(self.sketch.solve(), 0)

    def symmetry(self, axis=-2):
        return self.sketch.addConstraint(Sketcher.Constraint('Symmetric', 0, 1, 0, 2, axis))

    def assertSymmetric(self, vertical=False):
        self.assertEqual(self.sketch.solve(), 0)
        self.assertEqual(self.sketch.RedundantConstraints, [])
        self.assertEqual(self.sketch.PartiallyRedundantConstraints, [])
        a, b = self.sketch.Geometry[0].StartPoint, self.sketch.Geometry[0].EndPoint
        self.assertAlmostEqual(a.y + b.y if vertical else a.x + b.x, 0, places=6)
        self.assertAlmostEqual(a.x - b.x if vertical else a.y - b.y, 0, places=6)
        self.assertGreater((a - b).Length, 1)
        self.doc.recompute()
        self.assertNotIn('Invalid', self.sketch.State)
        self.assertTrue(self.sketch.Shape.isValid())

    def test_horizontal_rectangle_vertical_axis(self):
        self.rectangle()
        self.symmetry()
        self.assertSymmetric()
        self.assertEqual(self.sketch.ConstraintCount, 9)

    def test_native_symmetry_command(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Requires an isolated GUI profile')
        import FreeCADGui as Gui
        self.rectangle()
        self.doc.recompute()
        Gui.activateWorkbench('SketcherWorkbench')
        Gui.activeDocument().setEdit(self.sketch.Name)
        try:
            Gui.Selection.clearSelection()
            for name in ('Vertex1', 'Vertex2', 'V_Axis'):
                Gui.Selection.addSelection(self.doc.Name, self.sketch.Name, name)
            Gui.runCommand('Sketcher_ConstrainSymmetric')
            self.assertEqual(self.sketch.ConstraintCount, 9)
            self.assertEqual(self.sketch.Constraints[-1].Type, 'Symmetric')
            self.assertSymmetric()
        finally:
            Gui.Selection.clearSelection()
            Gui.activeDocument().resetEdit()

    def test_vertical_rectangle_horizontal_axis(self):
        self.rectangle(vertical=True)
        self.symmetry(-1)
        self.assertSymmetric(vertical=True)

    def test_two_sides_and_two_axes(self):
        self.rectangle()
        self.symmetry()
        self.sketch.addConstraint(Sketcher.Constraint('Symmetric', 2, 1, 2, 2, -2))
        self.sketch.addConstraint(Sketcher.Constraint('Symmetric', 0, 1, 2, 2, -1))
        self.assertSymmetric()
        a = self.sketch.Geometry[0].StartPoint
        b = self.sketch.Geometry[2].EndPoint
        self.assertAlmostEqual(a.y + b.y, 0, places=6)

    def test_constrained_construction_line_reference(self):
        self.rectangle()
        axis = self.sketch.addGeometry(Part.LineSegment(App.Vector(0, -20, 0), App.Vector(0, 20, 0)), True)
        self.sketch.addConstraint(Sketcher.Constraint('Vertical', axis))
        self.sketch.addConstraint(Sketcher.Constraint('DistanceX', axis, 1, 0.0))
        self.symmetry(axis)
        self.assertSymmetric()

    def test_symmetry_before_horizontal_and_duplicate_symmetry(self):
        self.rectangle()
        self.sketch.delConstraint(7)
        self.sketch.delConstraint(5)
        self.sketch.delConstraint(3)
        self.sketch.delConstraint(1)
        self.symmetry()
        for i in range(4):
            self.sketch.addConstraint(Sketcher.Constraint('Horizontal' if i % 2 == 0 else 'Vertical', i))
        self.symmetry()
        self.assertSymmetric()

    def test_fully_constrained_compatible_and_conflicting_symmetry(self):
        self.rectangle(centered=True)
        for c in (Sketcher.Constraint('Distance', 0, 20.0),
                  Sketcher.Constraint('Distance', 1, 10.0),
                  Sketcher.Constraint('DistanceX', 0, 1, -10.0),
                  Sketcher.Constraint('DistanceY', 0, 1, 3.0)):
            self.sketch.addConstraint(c)
        self.assertEqual(self.sketch.solve(), 0)
        self.assertTrue(self.sketch.FullyConstrained)
        self.symmetry()
        self.assertSymmetric()
        self.assertTrue(self.sketch.FullyConstrained)
        with self.assertRaises(ValueError):
            self.sketch.setDatum(8, App.Units.Quantity('18 mm'))
        self.assertSymmetric()
        self.sketch.addConstraint(Sketcher.Constraint('DistanceX', 0, 2, 12.0))
        self.assertNotEqual(self.sketch.solve(), 0)

    def test_unrelated_redundancy_remains_an_error(self):
        self.rectangle()
        self.symmetry()
        self.assertSymmetric()
        self.sketch.addConstraint(Sketcher.Constraint('Distance', 1, 10.0))
        self.sketch.addConstraint(Sketcher.Constraint('Distance', 1, 10.0))
        self.assertNotEqual(self.sketch.solve(), 0)

    def test_point_symmetry_duplicate(self):
        self.rectangle(centered=True)
        center = self.sketch.addGeometry(Part.Point(App.Vector(0, 8, 0)))
        constraint = Sketcher.Constraint('Symmetric', 0, 1, 2, 1, center, 1)
        self.sketch.addConstraint(constraint)
        self.sketch.addConstraint(constraint)
        self.assertEqual(self.sketch.solve(), 0)
        a, b = self.sketch.Geometry[0].StartPoint, self.sketch.Geometry[2].StartPoint
        midpoint = self.sketch.getPoint(center, 1)
        self.assertLess(((a + b) * 0.5 - midpoint).Length, 1e-6)

    def test_oblique_axis_preserves_both_symmetry_equations(self):
        self.sketch.addGeometry(Part.LineSegment(App.Vector(-10, 0, 0), App.Vector(0, 10, 0)))
        axis = self.sketch.addGeometry(Part.LineSegment(App.Vector(-20, -20, 0), App.Vector(20, 20, 0)), True)
        self.sketch.addConstraint(Sketcher.Constraint('Block', axis))
        self.symmetry(axis)
        self.symmetry(axis)
        self.assertEqual(self.sketch.solve(), 0)
        self.sketch.addConstraint(Sketcher.Constraint('DistanceX', 0, 1, -15.0))
        self.assertEqual(self.sketch.solve(), 0)
        a, b = self.sketch.Geometry[0].StartPoint, self.sketch.Geometry[0].EndPoint
        self.assertAlmostEqual(a.x, b.y, places=6)
        self.assertAlmostEqual(a.y, b.x, places=6)

    def test_dimension_edit_delete_symmetry_and_undo_redo(self):
        self.rectangle()
        self.doc.openTransaction('Symmetry')
        index = self.symmetry()
        self.assertSymmetric()
        self.doc.commitTransaction()
        self.doc.undo()
        self.assertEqual(self.sketch.ConstraintCount, 8)
        self.doc.redo()
        self.assertSymmetric()
        width = self.sketch.addConstraint(Sketcher.Constraint('Distance', 0, 30.0))
        self.assertSymmetric()
        self.sketch.setDatum(width, App.Units.Quantity('40 mm'))
        self.assertSymmetric()
        self.assertAlmostEqual(self.sketch.Geometry[0].length(), 40, places=6)
        self.sketch.delConstraint(index)
        self.assertEqual(self.sketch.solve(), 0)
        self.assertEqual(sum(c.Type == 'Horizontal' for c in self.sketch.Constraints), 2)

    def test_save_reopen_and_downstream_extrusion(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Requires isolated output directory')
        self.rectangle()
        self.sketch.addConstraint(Sketcher.Constraint('Distance', 0, 20.0))
        self.sketch.addConstraint(Sketcher.Constraint('Distance', 1, 10.0))
        self.symmetry()
        self.assertSymmetric()
        extrusion = self.doc.addObject('Part::Extrusion', 'Extrusion')
        extrusion.Base = self.sketch
        extrusion.Dir = App.Vector(0, 0, 5)
        extrusion.Solid = True
        self.doc.recompute()
        self.assertTrue(extrusion.Shape.isValid())
        self.assertAlmostEqual(extrusion.Shape.Volume, 1000, places=5)
        path = str(Path(os.environ['PLUS_TEST_DIR']) / 'constraint-symmetry.FCStd')
        self.doc.saveAs(path)
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(path)
        self.sketch = self.doc.getObject('Sketch')
        self.assertSymmetric()
        self.assertAlmostEqual(self.doc.getObject('Extrusion').Shape.Volume, 1000, places=5)
