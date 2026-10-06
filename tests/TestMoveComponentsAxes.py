# SPDX-License-Identifier: LGPL-2.1-or-later
import unittest
import FreeCAD as App
import Part
from freecad.gui import MoveComponents as Move
from freecad.gui import MoveComponentsTask as UI
from TestMoveComponentsRotate import TestMoveComponentsRotate as Rotate


class TestMoveComponentsAxes(unittest.TestCase):
    setUp, tearDown = Rotate.setUp, Rotate.tearDown
    session, vector, pick = Rotate.session, Rotate.vector, Rotate.pick

    def test_skew_closest_point_and_parallel_anchor(self):
        session = self.session()
        source, target = App.Vector(2, 3, 4), App.Vector(10, 8, 7)
        session.source_axis = (source, App.Vector(1, 0, 0))
        session.target_axis = (target, App.Vector(0, 0, 1))
        delta = session.align_axes()
        self.vector(delta.multVec(source), App.Vector(10, 8, 4))
        self.vector(delta.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(0, 0, 1))
        session.coincident = False
        self.vector(session.align_axes().multVec(source), source)

    def test_antiparallel_reverse_noop_and_degenerate(self):
        session = self.session()
        source = App.Vector(3, 4, 5)
        session.source_axis = (source, App.Vector(1, 0, 0))
        session.target_axis = (source, App.Vector(-1, 0, 0))
        first = session.align_axes()
        self.vector(first.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(-1, 0, 0))
        self.assertTrue(first.isSame(session.align_axes(), 1e-12))
        session.reverse_target = True
        undo = self.doc.UndoCount
        self.assertFalse(session.commit(session.align_axes()))
        self.assertEqual(undo, self.doc.UndoCount)
        session.target_axis = (source, App.Vector())
        with self.assertRaises(ValueError):
            session.align_axes()

    def test_circle_cylinder_and_displayed_reference(self):
        session = self.session()
        circle = self.doc.addObject("Part::Feature", "AxisCircle")
        circle.Shape = Part.makeCircle(3, App.Vector(4, 5, 6), App.Vector(0, 1, 0))
        Move.Model.register_object(self.root, circle)
        anchor, direction = Move.reference_alignment_axis(session, circle, "Edge1")
        self.vector(session.frame().multVec(anchor), App.Vector(4, 5, 6))
        self.vector(session.frame().Rotation.multVec(direction), App.Vector(0, 1, 0))
        cylinder = self.doc.addObject("Part::Feature", "AxisCylinder")
        cylinder.Shape = Part.makeCylinder(2, 10, App.Vector(7, 8, 9))
        Move.Model.register_object(self.root, cylinder)
        self.doc.recompute()
        index = next(i for i, face in enumerate(cylinder.Shape.Faces, 1) if isinstance(face.Surface, Part.Cylinder))
        anchor, direction = Move.reference_alignment_axis(session, cylinder, "Face%d" % index)
        self.vector(session.frame().Rotation.multVec(direction), App.Vector(0, 0, 1))
        self.assertLess((session.frame().multVec(anchor)-App.Vector(7, 8, 9)).cross(App.Vector(0, 0, 1)).Length, 1e-7)

    def test_group_preview_commit_undo_redo(self):
        session = self.session()
        relative = self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement)
        session.source_axis = (App.Vector(4, 5, 6), App.Vector(1, 2, 3))
        session.target_axis = (App.Vector(8, 2, 4), App.Vector(3, -2, 1))
        delta = session.align_axes()
        before = session.signature()
        self.assertEqual(len(session.preview_shapes(delta)), 4)
        self.assertEqual(before, session.signature())
        self.assertTrue(session.commit(delta))
        expected = App.Placement(self.first.LinkPlacement)
        self.assertTrue(relative.isSame(self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement), 1e-8))
        self.doc.undo()
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))
        self.doc.redo()
        self.assertTrue(self.first.LinkPlacement.isSame(expected, 1e-8))

    def test_task_reference_isolation_and_reset(self):
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(3)
        task.source_axis_pick.click()
        self.pick(task, self.line, "Edge1")
        self.assertFalse(task.apply())
        task.target_axis_pick.click()
        self.pick(task, self.line, "Edge1")
        task.target_reverse.setChecked(True)
        self.assertEqual(task.session.paths, self.paths)
        self.assertTrue(task.apply(), task.status.text())
        self.assertIsNone(task.session.source_axis)
        self.assertIsNone(task.session.target_axis)
        self.assertFalse(task.target_reverse.isChecked())
        self.assertEqual(task.alignment_policy.currentIndex(), 0)
        undo = self.doc.UndoCount
        self.assertTrue(task.accept())
        self.assertEqual(self.doc.UndoCount, undo)
