# SPDX-License-Identifier: LGPL-2.1-or-later
"""Projected plane origin and X/Z directions using native attachment and task picking."""
import hashlib
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
from freecad.gui import ComponentSketchTask as Task
from freecad.gui import ComponentNavigator as Navigator
from PySide import QtCore
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestComponentPlaneFrame(unittest.TestCase):
    def setUp(self):
        for module, relative in ((Sketch, 'src/Mod/Part/ComponentSketch.py'), (Task, 'src/Gui/ComponentSketchTask.py')):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((Path(os.environ['FREECAD_PLUS_SOURCE']) / relative).read_bytes()).digest())
        self.doc = Model.new_document('Plane frames')
        self.part = Model.metadata(self.doc).RootComponent
        self.panel = Navigator.show(self.doc)
        self.box = self.doc.addObject('Part::Box', 'Surface')
        Model.register_object(self.part, self.box, 'Object', True)
        self.box.Placement.Base = App.Vector(12, 18, 7)
        self.doc.recompute()
        self.output = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            gui = Gui.getDocument(doc.Name)
            if gui.getInEdit():
                gui.resetEdit()
        self.settle()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        self.settle()

    def settle(self):
        Gui.updateGui()
        QtTest.QTest.qWait(150)

    def near(self, actual, expected):
        self.assertLess((actual - expected).Length, 1e-6, (actual, expected))

    def create(self, **frame):
        return Sketch.create_plane(self.part, 'Selected planar face', support=(self.box, 'Face6'), frame=frame)

    def point(self, name, position):
        obj = self.doc.addObject('Part::Feature', name)
        obj.Shape = Part.Vertex(App.Vector(*position))
        Model.register_object(self.part, obj)
        self.doc.recompute()
        return obj

    def testDefaultOriginAndAxesIgnoreSurfaceUVOrigin(self):
        plane = self.create()
        self.assertEqual(plane.TypeId, 'PartDesign::Plane')
        self.near(plane.Placement.Base, App.Vector(0, 0, 17))
        self.near(plane.Placement.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(1, 0, 0))
        self.near(plane.Placement.Rotation.multVec(App.Vector(0, 0, 1)), App.Vector(0, 0, 1))
        self.assertEqual(Model.history(self.part), [self.box, plane])
        self.assertTrue(all(not obj.Visibility for obj in (plane.ProjectedFrame, plane.ProjectedFrame.Surface)))

    def testTiltedSurfaceClosestAxisAndIndependentReversals(self):
        self.box.Placement = App.Placement(App.Vector(12, 18, 7), App.Rotation(App.Vector(1, 0, 0), 30))
        self.doc.recompute()
        normal = self.box.Placement.Rotation.multVec(App.Vector(0, 0, 1))
        anchor = self.box.Placement.multVec(App.Vector(0, 0, 10))
        expected_origin = normal * anchor.dot(normal)
        for rz, rx in ((False, False), (True, False), (False, True), (True, True)):
            plane = self.create(reverse_z=rz, reverse_x=rx)
            self.near(plane.Placement.Base, expected_origin)
            self.near(plane.Placement.Rotation.multVec(App.Vector(0, 0, 1)), -normal if rz else normal)
            self.near(plane.Placement.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(-1 if rx else 1, 0, 0))
        plane = Sketch.create_plane(self.part, 'YZ plane', offset=6, frame={})
        self.near(plane.Placement.Base, App.Vector(6, 0, 0))
        self.near(plane.Placement.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(0, 1, 0))

    def testSymmetricNormalUsesStableXAxisTieBreak(self):
        normal = App.Vector(1, 1, 1);normal.normalize()
        surface = App.Placement(App.Vector(2, 3, 4), App.Rotation(App.Vector(0, 0, 1), normal))
        frame = Sketch.projected_frame(self.part, surface)
        expected = App.Vector(1, 0, 0) - normal * normal.x
        expected.normalize()
        self.near(frame.Rotation.multVec(App.Vector(1, 0, 0)), expected)

    def testPointEdgeAndTwoPointsProjectAndFollowSources(self):
        point = self.point('OriginPoint', (3, 4, 99))
        other = self.point('DirectionPoint', (7, 9, 120))
        frame = dict(origin_reference=(point, ['Vertex1']), axis_references=[(point, ['Vertex1']), (other, ['Vertex1'])])
        plane = self.create(**frame)
        self.near(plane.Placement.Base, App.Vector(3, 4, 17))
        expected = App.Vector(4, 5, 0); expected.normalize()
        self.near(plane.Placement.Rotation.multVec(App.Vector(1, 0, 0)), expected)
        sketch = Sketch.create(self.part, 'User plane', support=plane)
        point.Placement.Base = App.Vector(5, 0, 0)
        self.box.Height = 20
        self.doc.recompute()
        self.near(plane.Placement.Base, App.Vector(8, 4, 27))
        self.near(sketch.Placement.Base, plane.Placement.Base)
        edge = self.doc.addObject('Part::Feature', 'DirectionEdge')
        edge.Shape = Part.makeLine(App.Vector(0, 0, 0), App.Vector(2, 3, 7))
        Model.register_object(self.part, edge)
        self.doc.recompute()
        plane2 = self.create(axis_references=[(edge, ['Edge1'])])
        expected = App.Vector(2, 3, 0);expected.normalize()
        self.near(plane2.Placement.Rotation.multVec(App.Vector(1, 0, 0)), expected)

    def testMovedComponentUsesItsOwnOriginAndAxes(self):
        self.part.Placement = App.Placement(App.Vector(100, 200, 300), App.Rotation(App.Vector(0, 0, 1), 40))
        self.doc.recompute()
        plane = self.create()
        self.near(plane.Placement.Base, App.Vector(0, 0, 17))
        self.near(plane.getGlobalPlacement().Base, self.part.Placement.multVec(App.Vector(0, 0, 17)))
        point = self.point('PickedPoint', (4, 5, 80))
        other = self.create(origin_reference=(point, ['Vertex1']))
        self.near(other.Placement.Base, App.Vector(4, 5, 17))

    def testDegenerateProjectionRollsBackWithoutObjects(self):
        a, b = self.point('PointA', (3, 4, 9)), self.point('PointB', (3, 4, 99))
        before = [o.Name for o in self.doc.Objects]
        with self.assertRaises(ValueError):
            self.create(axis_references=[(a, ['Vertex1']), (b, ['Vertex1'])])
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testUndoRedoSaveReopenRetainsReferences(self):
        point = self.point('Point', (3, 4, 77))
        before = [o.Name for o in self.doc.Objects]
        plane = self.create(origin_reference=(point, ['Vertex1']), reverse_z=True)
        name, identity = plane.Name, plane.ObjectId
        self.doc.undo()
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        self.doc.redo();self.doc.recompute()
        plane = self.doc.getObject(name)
        self.assertEqual(plane.ObjectId, identity)
        path = self.output / 'ProjectedPlane.cadprt'
        self.doc.saveAs(str(path))
        point_name = point.Name
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        plane = self.doc.getObject(name)
        self.doc.getObject(point_name).Placement.Base = App.Vector(2, 0, 0)
        self.doc.recompute()
        self.near(plane.Placement.Base, App.Vector(5, 4, 17))
        self.near(plane.Placement.Rotation.multVec(App.Vector(0, 0, 1)), App.Vector(0, 0, -1))

    def testTaskSequencePickingAndReverseButtons(self):
        point, other = self.point('PickedOrigin', (3, 4, 70)), self.point('SecondPoint', (8, 5, 90))
        task = Task.launch(self.part, datum_only=True)
        self.assertEqual([s.title() for s in task.sections], ['Define Surface', 'Z Direction', 'Sketch Origin', 'X Direction'])
        self.assertEqual(task.orientation_mode.currentData(), 'Projected references')
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.box, 'Face6')
        self.assertEqual(task.base.currentData(), 'Selected planar face')
        task.origin_pick.click();Gui.Selection.addSelection(point, 'Vertex1')
        self.assertEqual(task.origin_reference[0], point)
        task.x_source.setCurrentIndex(2)
        Gui.Selection.addSelection(point, 'Vertex1');Gui.Selection.addSelection(other, 'Vertex1')
        self.assertEqual(len(task.axis_references), 2)
        task.reverse_z.click();task.reverse_x.click()
        self.settle()
        task.form.grab().save(str(self.output / 'projected-plane-task.png'))
        if not task.accept():self.fail(task.status.text())
        self.near(task.result.Placement.Base, App.Vector(3, 4, 17))
        expected = App.Vector(-5, -1, 0);expected.normalize()
        self.near(task.result.Placement.Rotation.multVec(App.Vector(1, 0, 0)), expected)
        self.near(task.result.Placement.Rotation.multVec(App.Vector(0, 0, 1)), App.Vector(0, 0, -1))

    def testCurvedEdgeUsesProjectedMidpointTangentAndHelpersDeleteWithPlane(self):
        edge = self.doc.addObject('Part::Feature', 'CurvedEdge')
        edge.Shape = Part.makeCircle(3)
        Model.register_object(self.part, edge)
        self.doc.recompute()
        plane = self.create(axis_references=[(edge, ['Edge1'])])
        tangent = edge.Shape.Edges[0].tangentAt(3.141592653589793)
        self.near(plane.Placement.Rotation.multVec(App.Vector(1, 0, 0)), tangent)
        names = [plane.Name, plane.ProjectedFrame.Name, plane.ProjectedFrame.Surface.Name]
        with Model.transaction(self.doc, 'Delete plane'):
            self.doc.removeObject(plane.Name)
        self.assertTrue(all(self.doc.getObject(name) is None for name in names))
        self.doc.undo();self.doc.recompute()
        self.assertTrue(all(self.doc.getObject(name) is not None for name in names))
