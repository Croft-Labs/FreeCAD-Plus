# SPDX-License-Identifier: LGPL-2.1-or-later
import unittest
from pathlib import Path
import tempfile
import FreeCAD as App
from freecad.gui import MoveComponents as Move
from freecad.gui import MoveComponentsTask as UI
from TestMoveComponentsRotate import TestMoveComponentsRotate as Rotate


class TestMoveComponentsFrames(unittest.TestCase):
    setUp, tearDown = Rotate.setUp, Rotate.tearDown
    session, vector, pick = Rotate.session, Rotate.vector, Rotate.pick

    def test_complete_mapping_including_roll_and_group(self):
        session = self.session()
        source = App.Placement(App.Vector(3, 4, 5), App.Rotation(App.Vector(1, 2, 3), 37))
        target = App.Placement(App.Vector(-2, 8, 4), App.Rotation(App.Vector(3, 1, -2), 121))
        session.source_frame, session.target_frame = source, target
        delta = session.align_frames()
        self.assertTrue(delta.multiply(source).isSame(target, 1e-8))
        relative = self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement)
        descendant = App.Placement(self.descendant.LinkPlacement)
        signature = session.signature()
        session.preview_shapes(delta)
        self.assertEqual(signature, session.signature())
        self.assertTrue(session.commit(delta))
        self.assertTrue(relative.isSame(self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement), 1e-8))
        self.assertTrue(descendant.isSame(self.descendant.LinkPlacement, 1e-8))

    def test_basis_projection_rejects_parallel_nonfinite_reflection_scale(self):
        frame = Move.frame_from_references(App.Vector(2, 3, 4), App.Vector(0, 0, 2), App.Vector(3, 0, 7))
        self.vector(frame.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(1, 0, 0))
        self.vector(frame.Rotation.multVec(App.Vector(0, 1, 0)), App.Vector(0, 1, 0))
        for z,x in ((App.Vector(), App.Vector(1,0,0)), (App.Vector(0,0,1), App.Vector(0,0,2)),
                    (App.Vector(0,0,1), App.Vector(float('nan'),0,0))):
            with self.assertRaises(ValueError):
                Move.frame_from_references(App.Vector(), z, x)
        for value in (-1., 2.):
            matrix = App.Matrix()
            matrix.A11 = value
            with self.assertRaises(ValueError):
                Move.validate_rigid_frame(matrix)

    def test_parent_target_reset_and_undo_roundtrip(self):
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(4)
        task.session.source_frame = App.Placement(App.Vector(3,4,5), App.Rotation(App.Vector(0,0,1),45))
        task.parent_frame("target")
        expected = task.delta()
        self.assertTrue(task.apply(), task.status.text())
        self.assertTrue(self.first.LinkPlacement.isSame(expected, 1e-8))
        self.assertIsNone(task.session.source_frame)
        self.assertIsNone(task.session.target_frame)
        task.accept()
        self.doc.undo()
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))
        self.doc.redo()
        name = self.first.Name
        files = []
        for extension in ("FCStd", "cadprt"):
            path = str(Path(tempfile.gettempdir()) / ("frame-roundtrip."+extension))
            self.doc.saveAs(path)
            files.append(path)
        App.closeDocument(self.doc.Name)
        for path in files:
            doc = App.openDocument(path)
            self.assertTrue(doc.getObject(name).LinkPlacement.isSame(expected, 1e-8))
            App.closeDocument(doc.Name)

    def test_partial_input_and_invalid_frame_do_not_commit(self):
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(4)
        task.frame_parts["source"]["origin"] = App.Vector(2,3,4)
        self.assertFalse(task.apply())
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))
        task.reset()
        task.session.source_frame = App.Placement()
        task.session.target_frame = App.Placement()
        undo = self.doc.UndoCount
        self.assertTrue(task.apply())
        self.assertEqual(self.doc.UndoCount, undo)
