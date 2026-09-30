# SPDX-License-Identifier: LGPL-2.1-or-later

import math
import tempfile
import unittest
from pathlib import Path
import FreeCAD as App
import Part
from BasicShapes import Isocline


def spline(bowl=False):
    surface = Part.BSplineSurface()
    poles = [
        [App.Vector(x, y, z + (zy if bowl else 0)) for y, zy in ((-10, 5), (0, -5), (10, 5))]
        for x, z in ((-10, 5), (0, -5), (10, 5))
    ]
    surface.buildFromPolesMultsKnots(poles, [3, 3], [3, 3], [0, 1], [0, 1], False, False, 2, 2)
    return surface.toShape()


class TestIsocline(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("IsoclineTest")
        self.doc.UndoMode = 1

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def feature(self):
        source = self.doc.addObject("Part::Sphere", "Source")
        source.Radius = 10
        obj = Isocline.makeIsocline(self.doc)
        obj.Faces = [(source, ["Face1"])]
        self.doc.recompute()
        return obj, source

    def checkCurve(self, face, direction, angle, shape):
        self.assertTrue(shape.Edges)
        self.assertTrue(shape.isValid())
        direction = App.Vector(direction)
        direction.normalize()
        for edge in shape.Edges:
            for point in edge.discretize(81):
                self.assertLess(Part.Vertex(point).distToShape(face)[0], 5e-5)
                u, v = face.Surface.parameter(point)
                self.assertAlmostEqual(
                    face.normalAt(u, v).dot(direction), math.sin(math.radians(angle)), delta=1e-5
                )

    def testSphereDraftAnglesAndReversedFace(self):
        face = Part.makeSphere(10).Faces[0]
        for angle in (0, 15, 30, 60, 85):
            for direction in (App.Vector(0, 0, 1), App.Vector(0, 0, -1), App.Vector(1, 2, 3)):
                with self.subTest(angle=angle, direction=direction):
                    result = Part.makeIsocline(face, direction, angle)
                    self.checkCurve(face, direction, angle, result)
                    self.assertAlmostEqual(
                        result.Length, 20 * math.pi * math.cos(math.radians(angle)), places=5
                    )
        face.reverse()
        self.checkCurve(
            face, App.Vector(0, 0, 1), 30, Part.makeIsocline(face, App.Vector(0, 0, 1), 30)
        )

    def testCylinderAndNinetyDegreeLimit(self):
        face = Part.makeCylinder(10, 20).Faces[0]
        for angle, count in ((0, 2), (30, 2), (90, 1)):
            result = Part.makeIsocline(face, App.Vector(1, 0, 0), angle)
            self.checkCurve(face, App.Vector(1, 0, 0), angle, result)
            self.assertAlmostEqual(result.Length, count * 20)
        with self.assertRaises(ValueError):
            Part.makeIsocline(face, App.Vector(0, 0, 1), 0)

    def testSplineAndTrimmedHole(self):
        face = spline()
        for angle in (0, 15, 30, 45):
            result = Part.makeIsocline(face, App.Vector(1, 0, 0), angle)
            self.checkCurve(face, App.Vector(1, 0, 0), angle, result)
            self.assertAlmostEqual(result.Length, 20, places=5)
        face = face.cut(Part.makeCylinder(2, 20, App.Vector(0, 0, -5))).Faces[0]
        result = Part.makeIsocline(face, App.Vector(1, 0, 0), 0)
        self.checkCurve(face, App.Vector(1, 0, 0), 0, result)
        self.assertAlmostEqual(result.Length, 16, places=4)
        self.assertEqual(len(result.Edges), 2)

    def testFreeformClosedContour(self):
        face = spline(True)
        result = Part.makeIsocline(face, App.Vector(0, 0, 1), 60)
        self.checkCurve(face, App.Vector(0, 0, 1), 60, result)
        radius = 10 / math.tan(math.radians(60))
        self.assertAlmostEqual(result.Length, 2 * math.pi * radius, delta=1e-3)

    def testEmptyNonUniqueAndInvalidParameters(self):
        face = Part.makePlane(10, 10)
        with self.assertRaises(ValueError):
            Part.makeIsocline(face, App.Vector(1, 0, 0), 0)
        self.assertFalse(Part.makeIsocline(face, App.Vector(0, 0, 1), 30).Edges)
        self.assertFalse(
            Part.makeIsocline(Part.makeSphere(10).Faces[0], App.Vector(0, 0, 1), 90).Edges
        )
        for angle in (-1, 91, float("nan")):
            with self.assertRaises(ValueError):
                Part.makeIsocline(face, App.Vector(0, 0, 1), angle)
        with self.assertRaises(ValueError):
            Part.makeIsocline(face, App.Vector(), 0)

    def testToleranceLimitsUnitsAndModelRecovery(self):
        obj, source = self.feature()
        obj.Angle = 30
        for tolerance in (1e-7, 1e-5, 0.01):
            obj.Tolerance = tolerance
            self.doc.recompute()
            self.assertTrue(obj.isValid(), obj.StatusMessage)
            self.checkCurve(source.Shape.Faces[0], App.Vector(0, 0, 1), 30, obj.Shape)
        for tolerance in (0, 1e-8, 0.02):
            obj.Tolerance = tolerance
            self.doc.recompute()
            self.assertFalse(obj.isValid())
            self.assertTrue(obj.Shape.isNull())
            self.assertIn("Curve tolerance", obj.StatusMessage)
        for tolerance in (float("nan"), float("inf"), -1, 0, 1e-8, 0.02):
            with self.assertRaises(ValueError):
                Part.makeIsocline(source.Shape.Faces[0], App.Vector(0, 0, 1), 30, tolerance)
        obj.Tolerance = Isocline.curve_tolerance("0.000001 m")
        self.doc.recompute()
        self.assertTrue(obj.isValid(), obj.StatusMessage)
        self.assertAlmostEqual(obj.Tolerance.Value, 0.001)
        self.checkCurve(source.Shape.Faces[0], App.Vector(0, 0, 1), 30, obj.Shape)

    def testOrientedFaceAndPullReversalThroughFeatureRecompute(self):
        source = self.doc.addObject("Part::Feature", "OrientedSphere")
        face = Part.makeSphere(10).Faces[0]
        face.reverse()
        source.Shape = face
        obj = Isocline.makeIsocline(self.doc)
        obj.Faces = [(source, ["Face1"])]
        obj.Angle = 30
        self.doc.recompute()
        self.checkCurve(source.Shape.Faces[0], App.Vector(0, 0, 1), 30, obj.Shape)
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.z, -5)
        self.doc.openTransaction("Reverse pull")
        obj.Reversed = True
        self.doc.recompute()
        self.doc.commitTransaction()
        self.checkCurve(source.Shape.Faces[0], App.Vector(0, 0, -1), 30, obj.Shape)
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.z, 5)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.z, -5)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.z, 5)

    def testAssociativeParametersAndInvalidRecovery(self):
        obj, source = self.feature()
        obj.Angle = 30
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.z, 5)
        source.Radius = 20
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.z, 10)
        obj.Reversed = True
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.z, -10)
        obj.Faces = []
        self.doc.recompute()
        self.assertTrue(obj.Shape.isNull())
        obj.Faces = [(source, ["Face1"])]
        self.doc.recompute()
        self.assertTrue(obj.isValid())

    def testDirectionReferencesAndPlacements(self):
        import PartDesign

        obj, source = self.feature()
        parent = self.doc.addObject("App::Part", "Container")
        parent.addObject(source)
        parent.Placement.Base = App.Vector(30, 0, 0)
        plane = self.doc.addObject("PartDesign::Plane", "ReferencePlane")
        obj.DirectionMode = "Reference"
        obj.DirectionReference = (plane, [])
        obj.Angle = 30
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.x, 30, places=5)
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.z, 5, places=5)
        parent.Placement.Base.x = 40
        plane.Placement.Rotation = App.Rotation(App.Vector(0, 1, 0), 90)
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.optimalBoundingBox(False).Center.x, 45, places=5)
        axis = self.doc.addObject("PartDesign::Line", "Axis")
        obj.DirectionReference = (axis, [])
        self.doc.recompute()
        self.assertAlmostEqual(obj.Direction.z, 1)
        line = self.doc.addObject("Part::Feature", "Line")
        line.Shape = Part.makeLine(App.Vector(), App.Vector(0, 10, 0))
        obj.DirectionReference = (line, ["Edge1"])
        self.doc.recompute()
        self.assertAlmostEqual(obj.Direction.y, 1)

    def testMultiFacePersistenceAndUndo(self):
        obj, source = self.feature()
        second = self.doc.addObject("Part::Sphere", "Second")
        second.Radius = 10
        second.Placement.Base.x = 30
        obj.Faces = [(source, ["Face1"]), (second, ["Face1"])]
        self.doc.recompute()
        self.assertEqual(len(obj.Shape.Wires), 2)
        self.doc.openTransaction("Angle")
        obj.Angle = 30
        self.doc.recompute()
        self.doc.commitTransaction()
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(obj.Angle.Value, 0)
        self.doc.redo()
        self.doc.recompute()
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Isocline.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            obj = self.doc.getObject("IsoclineCurve")
            obj.touch()
            self.doc.recompute()
            self.assertTrue(obj.isValid(), obj.StatusMessage)
            self.assertEqual(len(obj.Shape.Wires), 2)
            self.assertAlmostEqual(obj.Angle.Value, 30)

    def testSelfDependentAndCustomDirection(self):
        obj, source = self.feature()
        obj.DirectionMode = "Custom vector"
        obj.CustomDirection = App.Vector(1, 2, 3)
        self.doc.recompute()
        self.assertAlmostEqual(obj.Direction.Length, 1)
        obj.CustomDirection = App.Vector()
        self.doc.recompute()
        self.assertTrue(obj.Shape.isNull())
        with self.assertRaises(ValueError):
            Isocline.validate_link(obj, obj)
        dependent = self.doc.addObject("Part::Feature", "Dependent")
        dependent.addProperty("App::PropertyLink", "Input")
        dependent.Input = obj
        with self.assertRaises(ValueError):
            Isocline.validate_link(obj, dependent)
