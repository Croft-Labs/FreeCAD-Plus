# SPDX-License-Identifier: LGPL-2.1-or-later

import math
import tempfile
import unittest
from pathlib import Path
import FreeCAD as App
import Part
from BOPTools import TrimAPI, TrimFeatures


class TestTrimBody(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("TrimBodyModelTest")
        self.doc.UndoMode = 1

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def shape(self, name, shape):
        obj = self.doc.addObject("Part::Feature", name)
        obj.Shape = shape
        return obj

    def feature(self):
        target = self.doc.addObject("Part::Box", "Target")
        target.Length = target.Width = target.Height = 10
        tool = self.shape("Tool", Part.makePlane(2, 2, App.Vector(4, 4, 4)))
        obj = TrimFeatures.makeTrimBody(self.doc)
        obj.Target = (target, [])
        obj.Tool = (tool, [])
        self.doc.recompute()
        return obj, target, tool

    def testPlaneSidesCloseAndRecompute(self):
        obj, target, tool = self.feature()
        self.assertTrue(obj.isValid(), obj.getStatusString())
        self.assertAlmostEqual(obj.Shape.Volume, 600)
        self.assertTrue(obj.Shape.Solids[0].isClosed())
        obj.Reversed = True
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.Volume, 400)
        tool.Placement.Base.z = 2
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.Volume, 600)
        target.Height = 12
        obj.Reversed = False
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.Volume, 600)

    def testSheetTarget(self):
        target = Part.makePlane(10, 10)
        tool = Part.makePlane(2, 2, App.Vector(3, 4, -1), App.Vector(1, 0, 0))
        kept, _, _ = TrimAPI.trim(target, tool)
        other, _, _ = TrimAPI.trim(target, tool, True)
        self.assertAlmostEqual(kept.Area, 70)
        self.assertAlmostEqual(other.Area, 30)
        self.assertFalse(kept.Solids)
        self.assertTrue(kept.isValid())

    def testCurvedCylinderFace(self):
        target = Part.makeBox(10, 10, 2, App.Vector(-5, -5, 0))
        cylinder = Part.makeCylinder(4, 6, App.Vector(0, 0, -2))
        face = next(face for face in cylinder.Faces if isinstance(face.Surface, Part.Cylinder))
        outside, _, _ = TrimAPI.trim(target, face)
        inside, _, _ = TrimAPI.trim(target, face, True)
        self.assertAlmostEqual(outside.Volume, 200 - 32 * math.pi, places=6)
        self.assertAlmostEqual(inside.Volume, 32 * math.pi, places=6)
        self.assertTrue(outside.Solids[0].isClosed())
        self.assertTrue(inside.Solids[0].isClosed())

    def testCurvedBSplineSheet(self):
        surface = Part.BSplineSurface()
        # Exact quadratic z = 4 + .02 * (x - 5)^2, linear in y.
        poles = [
            [App.Vector(x, y, z) for y in (-2, 12)] for x, z in ((-2, 4.98), (5, 3.02), (12, 4.98))
        ]
        surface.buildFromPolesMultsKnots(poles, [3, 3], [2, 2], [0, 1], [0, 1], False, False, 2, 1)
        target = Part.makeBox(10, 10, 10)
        top, _, _ = TrimAPI.trim(target, surface.toShape())
        bottom, _, _ = TrimAPI.trim(target, surface.toShape(), True)
        self.assertAlmostEqual(top.Volume + bottom.Volume, 1000, delta=1e-4)
        self.assertAlmostEqual(bottom.Volume, 1250 / 3, delta=1e-4)
        self.assertTrue(top.isValid())
        self.assertTrue(bottom.isValid())

    def testRejectInsufficientToolAndNonIntersection(self):
        target = Part.makeBox(10, 10, 10)
        small = Part.makePlane(2, 2, App.Vector(4, 4, 4))
        with self.assertRaises(TrimAPI.TrimError):
            TrimAPI.trim(target, small, extend_planar=False)
        distant = Part.makePlane(20, 20, App.Vector(-5, -5, 20))
        with self.assertRaises(TrimAPI.TrimError):
            TrimAPI.trim(target, distant)
        with self.assertRaises(TrimAPI.TrimError):
            TrimAPI.trim(target, Part.makeBox(5, 5, 5))

    def testInvalidEditClearsOldShape(self):
        obj, target, tool = self.feature()
        self.assertFalse(obj.Shape.isNull())
        tool.Placement.Base.z = 20
        self.doc.recompute()
        self.assertTrue(obj.Shape.isNull())
        self.assertFalse(obj.isValid())
        tool.Placement.Base.z = 0
        self.doc.recompute()
        self.assertTrue(obj.isValid())
        self.assertAlmostEqual(obj.Shape.Volume, 600)

    def testDependencyRejection(self):
        obj, _, _ = self.feature()
        dependent = self.doc.addObject("Part::FeaturePython", "Dependent")
        dependent.addProperty("App::PropertyLink", "Source")
        dependent.Source = obj
        with self.assertRaises(TrimAPI.TrimError):
            TrimAPI.validate_link(obj, dependent)
        with self.assertRaises(TrimAPI.TrimError):
            TrimAPI.validate_link(obj, obj)

    def testSaveReopenAndUndoRedo(self):
        obj, target, tool = self.feature()
        self.doc.openTransaction("Reverse trim")
        obj.Reversed = True
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertAlmostEqual(obj.Shape.Volume, 400)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.Volume, 600)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.Volume, 400)
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Trim.FCStd")
            name = obj.Name
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            obj = self.doc.getObject(name)
            obj.Tool[0].Placement.Base.z = 2
            self.doc.recompute()
            self.assertTrue(obj.isValid(), obj.getStatusString())
            self.assertAlmostEqual(obj.Shape.Volume, 600)

    def testDatumPlaneAndGlobalPlacements(self):
        import PartDesign

        group = self.doc.addObject("App::Part", "Assembly")
        target = self.doc.addObject("Part::Box", "Target")
        target.Length = target.Width = target.Height = 10
        plane = self.doc.addObject("PartDesign::Plane", "CutPlane")
        plane.Placement.Base.z = 4
        group.addObject(target)
        group.addObject(plane)
        group.Placement.Base = App.Vector(20, 30, 40)
        obj = TrimFeatures.makeTrimBody(self.doc)
        obj.Target, obj.Tool = (target, []), (plane, [])
        self.doc.recompute()
        self.assertTrue(obj.isValid(), obj.getStatusString())
        self.assertAlmostEqual(obj.Shape.Volume, 600)
        self.assertAlmostEqual(obj.Shape.BoundBox.XMin, 20)
        self.assertAlmostEqual(obj.Shape.BoundBox.YMin, 30)
        self.assertAlmostEqual(obj.Shape.BoundBox.ZMin, 44)
        group.Placement.Base.z = 50
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.BoundBox.ZMin, 54)

    def testConnectedMultiFaceSheet(self):
        faces = []
        for x0, z0, x1, z1 in ((-2, 2.2, 5, 5), (5, 5, 12, 2.2)):
            points = [
                App.Vector(x0, -2, z0),
                App.Vector(x1, -2, z1),
                App.Vector(x1, 12, z1),
                App.Vector(x0, 12, z0),
            ]
            faces.append(Part.Face(Part.makePolygon(points + points[:1])))
        target = Part.makeBox(10, 10, 10)
        tool = Part.makeCompound(faces)
        top, _, _ = TrimAPI.trim(target, tool)
        bottom, _, _ = TrimAPI.trim(target, tool, True)
        self.assertAlmostEqual(top.Volume, 600, places=6)
        self.assertAlmostEqual(bottom.Volume, 400, places=6)
        self.assertTrue(top.Solids[0].isClosed())
        self.assertTrue(bottom.Solids[0].isClosed())

    def testCurvedToolOnSheetTarget(self):
        target = Part.makePlane(10, 10, App.Vector(-5, -5, 1))
        cylinder = Part.makeCylinder(4, 6, App.Vector(0, 0, -2))
        tool = next(face for face in cylinder.Faces if isinstance(face.Surface, Part.Cylinder))
        outside, _, _ = TrimAPI.trim(target, tool)
        inside, _, _ = TrimAPI.trim(target, tool, True)
        self.assertAlmostEqual(outside.Area, 100 - 16 * math.pi, places=6)
        self.assertAlmostEqual(inside.Area, 16 * math.pi, places=6)
        self.assertFalse(outside.Solids)

    def testInsufficientCurvedToolRejected(self):
        target = Part.makeBox(10, 10, 2, App.Vector(-5, -5, 0))
        cylinder = Part.makeCylinder(4, 1, App.Vector(0, 0, 0.5))
        face = next(face for face in cylinder.Faces if isinstance(face.Surface, Part.Cylinder))
        with self.assertRaises(TrimAPI.TrimError):
            TrimAPI.trim(target, face)

    def testCurvedToolParameterChangeRecomputes(self):
        target = self.shape("Target", Part.makeBox(10, 10, 2, App.Vector(-5, -5, 0)))
        tool = self.doc.addObject("Part::Cylinder", "CylinderTool")
        tool.Radius, tool.Height = 4, 6
        tool.Placement.Base.z = -2
        self.doc.recompute()
        face = next(
            i for i, face in enumerate(tool.Shape.Faces) if isinstance(face.Surface, Part.Cylinder)
        )
        obj = TrimFeatures.makeTrimBody(self.doc)
        obj.Target, obj.Tool = (target, []), (tool, ["Face%d" % (face + 1)])
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.Volume, 200 - 32 * math.pi, places=6)
        tool.Radius = 3
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.Volume, 200 - 18 * math.pi, places=6)

    def testPartDesignBodyTarget(self):
        import PartDesign

        body = self.doc.addObject("PartDesign::Body", "Body")
        block = body.newObject("PartDesign::AdditiveBox", "Block")
        block.Length = block.Width = block.Height = 10
        tool = self.shape("Tool", Part.makePlane(2, 2, App.Vector(4, 4, 4)))
        obj = TrimFeatures.makeTrimBody(self.doc)
        obj.Target, obj.Tool = (body, []), (tool, [])
        self.doc.recompute()
        self.assertTrue(obj.isValid(), obj.getStatusString())
        self.assertAlmostEqual(obj.Shape.Volume, 600)
        body.Placement.Base = App.Vector(2, 3, 4)
        tool.Placement.Base.z = 4
        self.doc.recompute()
        self.assertAlmostEqual(obj.Shape.Volume, 600)
        self.assertAlmostEqual(obj.Shape.BoundBox.ZMin, 8)
        self.assertEqual(body.Tip, block)
