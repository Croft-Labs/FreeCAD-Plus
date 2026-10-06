# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native point mapping, shared-parent motion and task lifecycle regression."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from freecad.gui import MoveComponentsTask as UI
from TestMoveComponentsRotate import TestMoveComponentsRotate as Rotate


class TestMoveComponentsPoint(unittest.TestCase):
    setUp = Rotate.setUp
    tearDown = Rotate.tearDown
    session = Rotate.session
    vector = Rotate.vector
    rendered_center = Rotate.rendered_center
    pick = Rotate.pick

    def test_rigid_translation_shared_parents_and_undo(self):
        session = self.session()
        rotation = App.Rotation(self.first.LinkPlacement.Rotation)
        relative = self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement)
        descendant = App.Placement(self.descendant.LinkPlacement)
        source = session.world_point(App.Vector(3, 4, 5))
        target = session.world_point(App.Vector(11, -2, 9))
        session.source_point, session.destination_point = source, target
        before = [self.rendered_center(link) for link in (self.a, self.b)]
        from ComponentModel import _component_frame
        delta = session.point_to_point()
        self.vector(delta.multVec(source), target)
        self.assertTrue(session.commit(delta))
        self.assertTrue(rotation.isSame(self.first.LinkPlacement.Rotation, 1e-8))
        self.assertTrue(relative.isSame(self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement), 1e-8))
        self.assertTrue(descendant.isSame(self.descendant.LinkPlacement, 1e-8))
        for old, parent in zip(before, (self.a, self.b)):
            self.vector(self.rendered_center(parent)-old,
                        _component_frame(self.root, (parent.ObjectId,)).Rotation.multVec(target-source))
        self.doc.undo()
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))
        self.doc.redo()
        self.vector(self.first.LinkPlacement.Base, target-source)

    def test_coincidence_missing_nonfinite_and_baseline(self):
        session = self.session()
        with self.assertRaises(ValueError):
            session.point_to_point()
        session.source_point = session.destination_point = App.Vector(2, 3, 4)
        undo = self.doc.UndoCount
        self.assertFalse(session.commit(session.point_to_point()))
        self.assertEqual(undo, self.doc.UndoCount)
        session.destination_point = App.Vector(float('nan'), 0, 0)
        with self.assertRaises(ValueError):
            session.point_to_point()
        session.destination_point = App.Vector(5, 6, 7)
        signature = session.signature()
        for _ in range(5):
            session.preview_shapes(session.point_to_point())
        self.assertEqual(session.signature(), signature)
        self.assertEqual(undo, self.doc.UndoCount)

    def test_task_picks_reset_pending_cancel_and_ok_once(self):
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(2)
        task.source_pick.click()
        self.pick(task, self.line, 'Vertex1')
        self.assertFalse(task.apply())
        task.destination_pick.click()
        self.pick(task, self.line, 'Vertex2')
        self.assertEqual(task.session.paths, self.paths)
        self.assertTrue(task.ghosts)
        expected = task.delta()
        self.assertTrue(task.apply(), task.status.text())
        self.vector(self.first.LinkPlacement.Base, expected.Base)
        self.assertIsNone(task.session.source_point)
        self.assertIsNone(task.session.destination_point)
        self.assertFalse(task.reference_objects)
        undo = self.doc.UndoCount
        self.assertTrue(task.accept())
        self.assertEqual(undo, self.doc.UndoCount)

    def test_deleted_reference_refuses_commit(self):
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(2)
        task.source_pick.click()
        self.pick(task, self.line, 'Vertex1')
        task.destination_pick.click()
        self.pick(task, self.line, 'Vertex2')
        self.doc.removeObject(self.line.Name)
        self.assertFalse(task.apply())
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))
