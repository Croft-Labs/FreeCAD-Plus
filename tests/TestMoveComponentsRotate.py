# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native parent-relative rotations and task reference collectors."""
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtWidgets
import ComponentModel as Model
from freecad.gui import MoveComponents as Move
from freecad.gui import MoveComponentsTask as UI
from freecad.gui import DesignSelection
from TestMoveComponents import TestMoveComponents as Foundation


class TestMoveComponentsRotate(unittest.TestCase):
    setUp = Foundation.setUp
    def tearDown(self):
        if UI._task:
            UI._task.reject()
        for doc in App.listDocuments().values():
            if Gui.getDocument(doc.Name).getInEdit():
                Gui.getDocument(doc.Name).resetEdit()
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        Foundation.tearDown(self)
    session = Foundation.session
    vector = Foundation.vector
    rendered_center = Foundation.rendered_center

    def test_offset_axis_group_shared_parent_and_reverse(self):
        session = self.session()
        baseline = [self.rendered_center(link) for link in (self.a, self.b)]
        frames = [Model._component_frame(self.root, (link.ObjectId,)) for link in (self.a, self.b)]
        relative = self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement)
        descendant = App.Placement(self.descendant.LinkPlacement)
        shape = self.box.Shape.hashCode()
        session.axis = (App.Vector(10, 0, 0), App.Vector(0, 0, 1))
        session.angle = 90
        delta = session.rotation()
        self.assertTrue(session.commit(delta))
        self.vector(self.first.LinkPlacement.Base, App.Vector(10, -10, 0))
        self.vector(self.first.LinkPlacement.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(0, 1, 0))
        for before, frame, link in zip(baseline, frames, (self.a, self.b)):
            expected = frame.multVec(delta.multVec(frame.inverse().multVec(before)))
            self.vector(self.rendered_center(link), expected)
        self.assertTrue(relative.isSame(self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement), 1e-8))
        self.assertTrue(descendant.isSame(self.descendant.LinkPlacement, 1e-8))
        self.assertEqual(shape, self.box.Shape.hashCode())
        session.axis = (App.Vector(10, 0, 0), App.Vector(0, 0, 1))
        session.angle, session.reverse = 90, True
        session.commit(session.rotation())
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))

    def test_picked_line_keeps_location_through_other_occurrence(self):
        line = self.doc.addObject("Part::Feature", "AxisReference")
        line.Shape = Part.makeLine(App.Vector(7, 8, 9), App.Vector(7, 8, -4))
        Model.register_object(self.first.LinkedObject, line)
        self.doc.recompute()
        session = self.session()
        path = self.b.Name + "." + self.first.Name + "." + line.Name + ".Edge1"
        edge = Part.getShape(self.root, path, needSubElement=True, transform=True)
        session.axis = Move.reference_axis(session, self.root, path)
        point, direction = session.axis
        self.vector(session.frame().multVec(point), edge.valueAt(edge.FirstParameter))
        self.vector(session.frame().Rotation.multVec(direction), edge.tangentAt(edge.FirstParameter))
        session.angle = 37
        world_delta = App.Placement(App.Vector(), App.Rotation(edge.tangentAt(edge.FirstParameter), 37),
                                    edge.valueAt(edge.FirstParameter))
        self.assertTrue(session.frame().multiply(session.rotation()).isSame(world_delta.multiply(session.frame()), 1e-8))
        session.pivot = App.Vector(2, 5, 8)
        self.vector(session.resolved_axis()[1], direction)
        self.vector(session.rotation().multVec(session.pivot), session.pivot)

    def test_native_point_origin_sketch_and_circle_sources(self):
        session = self.session()
        self.vector(session.frame().multVec(Move.reference_point(session, self.root.Origin, "")),
                    self.root.Origin.getGlobalPlacement().Base)
        self.vector(session.frame().multVec(Move.reference_point(session, self.line, "Vertex2")), App.Vector(5, 0, 0))
        circle = self.doc.addObject("Part::Feature", "Circle")
        circle.Shape = Part.makeCircle(3, App.Vector(4, 5, 6))
        Model.register_object(self.root, circle)
        self.vector(session.frame().multVec(Move.reference_point(session, circle, "Edge1")), App.Vector(4, 5, 6))
        sketch = self.doc.addObject("Sketcher::SketchObject", "Points")
        Model.register_object(self.root, sketch)
        sketch.Placement = App.Placement(App.Vector(8, 9, 10), App.Rotation(App.Vector(1, 0, 0), 30))
        sketch.addGeometry(Part.LineSegment(App.Vector(1, 2, 0), App.Vector(2, 3, 0)), True)
        self.doc.recompute()
        self.vector(session.frame().multVec(Move.reference_point(session, sketch, "vertex1")),
                    sketch.Placement.multVec(App.Vector(1, 2, 0)))
        self.vector(session.frame().multVec(Move.reference_point(session, sketch, "RootPoint")), sketch.Placement.Base)
        with self.assertRaises(ValueError):
            Move.reference_point(session, self.line, "Edge1")

    def test_two_points_antiparallel_degenerate_and_invalid_angles(self):
        session = self.session()
        session.axis = Move.axis_from_points(App.Vector(3, 4, 5), App.Vector(3, 4, -5))
        self.vector(session.axis[1], App.Vector(0, 0, -1))
        session.angle = 90
        negative = session.rotation()
        session.axis = (session.axis[0], -session.axis[1])
        session.reverse = True
        self.assertTrue(negative.isSame(session.rotation(), 1e-9))
        for second in (App.Vector(3, 4, 5), App.Vector(3, 4, 5 + 1e-8)):
            with self.assertRaises(ValueError):
                Move.axis_from_points(App.Vector(3, 4, 5), second)
        undo = self.doc.UndoCount
        for angle in (-1., 361., float("nan"), float("inf")):
            session.angle = angle
            with self.assertRaises(ValueError):
                session.rotation()
        session.axis, session.angle = (App.Vector(), App.Vector()), 30
        with self.assertRaises(ValueError):
            session.rotation()
        self.assertEqual(self.doc.UndoCount, undo)

    def test_preview_baseline_pivot_marker_and_noop(self):
        session = self.session()
        session.axis = (App.Vector(7, 2, 5), App.Vector(1, 2, 3))
        signature, undo = session.signature(), self.doc.UndoCount
        session.angle = 45
        expected = [placement for link, placement in session.candidates(session.rotation())]
        for angle in (45, 15, 180, 20, 270, 45):
            session.angle = angle
            self.assertEqual(len(session.preview_shapes(session.rotation())), 4)
            self.assertEqual(len(Move.axis_marker(session, 10).Edges), 6)
        for first, (link, last) in zip(expected, session.candidates(session.rotation())):
            self.assertTrue(first.isSame(last, 1e-12))
        self.assertEqual(signature, session.signature())
        self.assertEqual(undo, self.doc.UndoCount)
        session.angle = 360
        self.assertFalse(session.commit(session.rotation()))
        self.assertEqual(undo, self.doc.UndoCount)

    def test_successive_translate_rotate_undo_redo_and_reopen(self):
        session = self.session()
        session.direction, session.distance = App.Vector(1, 0, 0), 5.
        session.commit(session.translation())
        session.axis, session.angle = (App.Vector(1, 0, 0), App.Vector(0, 0, 1)), 90
        session.commit(session.rotation())
        self.vector(self.first.LinkPlacement.Base, App.Vector(1, 4, 0))
        self.doc.undo()
        self.vector(self.first.LinkPlacement.Base, App.Vector(5, 0, 0))
        self.doc.undo()
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))
        self.doc.redo()
        self.doc.redo()
        expected, name = App.Placement(self.first.LinkPlacement), self.first.Name
        files = []
        for extension in ("FCStd", "cadprt"):
            filename = str(Path(tempfile.gettempdir()) / ("rotate-roundtrip." + extension))
            self.doc.saveAs(filename)
            files.append(filename)
        App.closeDocument(self.doc.Name)
        for filename in files:
            document = App.openDocument(filename)
            self.assertTrue(document.getObject(name).LinkPlacement.isSame(expected, 1e-8))
            App.closeDocument(document.Name)

    def pick(self, task, obj, element):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(obj, element)
        task.collect()

    def test_task_reference_isolation_pivot_reset_apply_and_cancel(self):
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(1)
        task.axis_choice.setCurrentIndex(5)
        self.pick(task, self.line, "Vertex1")
        self.assertEqual(task.picking_reference, "second")
        self.pick(task, self.line, "Vertex2")
        self.assertEqual(task.session.paths, self.paths)
        original_direction = App.Vector(task.session.axis[1])
        task.pivot_pick.click()
        self.pick(task, self.line, "Vertex2")
        self.vector(task.session.axis[1], original_direction)
        task.angle.setProperty("rawValue", 30.)
        self.assertTrue(task.ghosts)
        self.assertIn("Parent-frame pivot", task.resolved.text())
        Gui.updateGui()
        task.form.grab().save(str(Path(tempfile.gettempdir()) / "rotate-task.png"))
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
        Gui.getMainWindow().grab().save(str(Path(tempfile.gettempdir()) / "rotate-preview.png"))
        self.assertTrue(task.apply(), task.status.text())
        committed = App.Placement(self.first.LinkPlacement)
        self.assertEqual(task.session.paths, self.paths)
        self.assertIsNone(task.session.axis)
        self.assertIsNone(task.session.pivot)
        self.assertEqual(task.axis_choice.currentIndex(), 0)
        self.assertEqual(task.angle.property("rawValue"), 0)
        self.assertFalse(task.reverse.isChecked())
        task.axis_choice.setCurrentIndex(3)
        task.angle.setProperty("rawValue", 50.)
        task.reject()
        self.assertTrue(self.first.LinkPlacement.isSame(committed, 1e-9))
        DesignSelection.parameters().SetBool("Persistent", False)
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(1)
        task.axis_choice.setCurrentIndex(2)
        task.angle.setProperty("rawValue", 10.)
        self.assertTrue(task.apply(), task.status.text())
        self.assertEqual(task.session.paths, [])
        self.assertFalse(Gui.Selection.getSelection())
        undo = self.doc.UndoCount
        self.assertTrue(task.accept())
        self.assertEqual(undo, self.doc.UndoCount)

    def test_task_line_axis_pending_pick_and_switch(self):
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(1)
        task.axis_choice.setCurrentIndex(4)
        self.pick(task, self.line, "Edge1")
        self.assertIsNotNone(task.session.axis)
        task.angle.setProperty("rawValue", 25.)
        baseline = App.Placement(self.first.LinkPlacement)
        editor = task.angle.findChild(QtWidgets.QLineEdit)
        editor.setText("not an angle")
        self.assertFalse(task.apply())
        self.assertTrue(self.first.LinkPlacement.isSame(baseline, 1e-8))
        task.angle.setProperty("rawValue", 25.)
        task.pivot_pick.click()
        self.assertFalse(task.apply())
        self.assertTrue(self.first.LinkPlacement.isSame(baseline, 1e-8))
        task.pivot_clear.click()
        self.assertTrue(task.ghosts)
        task.workflow.setCurrentIndex(0)
        self.assertFalse(task.ghosts)
        self.assertIsNone(task.session.axis)
        self.assertEqual(task.session.paths, self.paths)
        task.workflow.setCurrentIndex(1)
        task.axis_choice.setCurrentIndex(3)
        task.angle.setProperty("rawValue", 90.)
        expected = task.session.candidates(task.delta())[0][1]
        self.assertTrue(task.accept())
        self.assertTrue(self.first.LinkPlacement.isSame(expected, 1e-8))
