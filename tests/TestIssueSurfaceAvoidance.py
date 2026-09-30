# SPDX-License-Identifier: LGPL-2.1-or-later
"""CAM #27751/#27950: failed avoidance must never enable unrestricted cutting."""
import unittest
from unittest.mock import Mock, patch
import FreeCAD as App
import Part
import Path
from CAMTests.PathTestUtils import PathTestWithAssets
from Path.Main import Job
from Path.Op import PlanarSurface
from Path.Base.Generator import surface_common, surface_pattern


class TestSurfaceAvoidanceFailure(unittest.TestCase):
    def setUp(self):
        self.face = Part.makePlane(30, 30)
        self.avoid = Part.makePlane(10, 10, App.Vector(10, 10, 0))

    def testBooleanFailureStopsGeneration(self):
        boundary = Mock()
        boundary.cut.side_effect = Part.OCCError("Synthetic kernel failure")
        with self.assertRaisesRegex(ValueError, "avoid"):
            surface_common.generate_pattern_mask(
                True, boundary, [self.face], self.avoid, 1, 0, 0.01)

    def testNullBooleanResultStopsGeneration(self):
        boundary = Mock()
        boundary.cut.return_value = Part.Shape()
        with self.assertRaisesRegex(ValueError, "avoid"):
            surface_common.generate_pattern_mask(
                True, boundary, [self.face], self.avoid, 1, 0, 0.01)

    def testFailedAvoidBoundaryStopsGeneration(self):
        with patch.object(surface_common, "build_optimized_boundary", return_value=None):
            with self.assertRaisesRegex(ValueError, "avoid"):
                surface_common.build_avoid_boundary([self.avoid], 1, 0.01)

    def testUnresolvedAvoidFaceIsNotDropped(self):
        with patch.object(surface_common, "_classify_and_cap_faces",
                          return_value=([self.face], [self.avoid])):
            with patch.object(surface_common, "build_optimized_boundary", return_value=None):
                with self.assertRaisesRegex(ValueError, "avoid"):
                    surface_common.build_avoid_boundary([self.face, self.avoid], 1, 0.01)

    def testPartialAvoidanceProjectionStopsGeneration(self):
        second = Part.makePlane(5, 5, App.Vector(40, 40, 0))
        # Real grouping finds two isolated faces; only the second projection fails.
        with patch.object(surface_common, "create_boundary_face", side_effect=[self.avoid, None]):
            with self.assertRaisesRegex(ValueError, "boundary"):
                surface_common.build_avoid_boundary([self.avoid, second], 1, 0.01)

    def testConnectedAvoidanceProjectionStopsGeneration(self):
        with patch.object(surface_common, "_separate_touching_faces",
                          return_value=([[self.face, self.avoid]], [])):
            with patch.object(surface_common, "create_boundary_face", return_value=None):
                with self.assertRaisesRegex(ValueError, "boundary"):
                    surface_common.build_optimized_boundary([self.face, self.avoid], 1, avoids=True)

    def testAvoidanceMergeFailureDoesNotReturnFirstRegion(self):
        first = Mock()
        first.isNull.return_value = False
        first.isValid.return_value = True
        first.fuse.side_effect = Part.OCCError("Synthetic region union failure")
        with patch.object(surface_common, "_separate_touching_faces",
                          return_value=([], [self.face, self.avoid])):
            with patch.object(surface_common, "create_boundary_face", side_effect=[first, self.avoid]):
                with self.assertRaisesRegex(ValueError, "boundary"):
                    surface_common.build_optimized_boundary([self.face, self.avoid], 1, avoids=True)

    def testDisconnectedAvoidanceRegionsBothPreserved(self):
        second = Part.makePlane(5, 5, App.Vector(40, 40, 0))
        boundary = surface_common.build_avoid_boundary([self.avoid, second], 1, 0.01)
        self.assertTrue(boundary.isValid())
        self.assertAlmostEqual(boundary.common(self.avoid).Area, self.avoid.Area, places=5)
        self.assertAlmostEqual(boundary.common(second).Area, second.Area, places=5)

    def testFullyAvoidedAreaDoesNotRestoreCuttingRegion(self):
        covering = Part.makePlane(40, 40, App.Vector(-5, -5, 0))
        result = surface_common.generate_pattern_mask(
            True, self.face, [self.face], covering, 1, 0, 0.01)
        self.assertAlmostEqual(result.Area, 0)

    def testExternalOpenFaceUsesModernBoundaryPipeline(self):
        doc = App.newDocument("ExternalAvoidFace")
        try:
            model = doc.addObject("Part::Feature", "Model")
            model.Shape = self.face
            external = doc.addObject("Part::Feature", "ExternalOpenSurface")
            external.Shape = self.avoid
            cutting, avoided = surface_pattern.split_selected_features(
                [(model, ["Face1"]), (external, ["Face1"])], 1)
            self.assertEqual((len(cutting), len(avoided)), (1, 1))
            boundary = surface_common.build_avoid_boundary(avoided, 1, 0.01)
            mask = surface_common.generate_pattern_mask(
                True, self.face, cutting, boundary, 1, 0, 0.01)
            self.assertGreater(mask.Area, 700)
            self.assertAlmostEqual(mask.common(self.avoid).Area, 0, places=6)
        finally:
            App.closeDocument(doc.Name)


class TestSurfaceAvoidanceOperation(PathTestWithAssets):
    def setUp(self):
        super().setUp()
        self.doc = App.newDocument("AvoidanceOperation")
        model = self.doc.addObject("Part::Feature", "Model")
        model.Shape = Part.makeBox(30, 30, 5)
        self.job = Job.Create("Job", [model])
        self.job.Tools.Group[0].Tool = self.assets.get("toolbit://5mm_Endmill").attach_to_doc(doc=self.doc)
        self.external = self.doc.addObject("Part::Feature", "ExternalOpenSurface")
        self.external.Shape = Part.makePlane(10, 10, App.Vector(10, 10, 5))
        self.doc.recompute()

    def tearDown(self):
        App.closeDocument(self.doc.Name)
        super().tearDown()

    def operation(self):
        model = self.job.Model.Group[0]
        top = max(enumerate(model.Shape.Faces, 1), key=lambda p: p[1].CenterOfMass.z)[0]
        op = PlanarSurface.Create("Surface", parentJob=self.job)
        op.Base = [(model, [f"Face{top}"]), (self.external, ["Face1"])]
        op.AvoidLastX_Faces = 1
        op.CutPattern = "Line"
        op.SampleInterval = 1
        op.StepOver = 50
        return op

    def testExternalCurvedSurfaceAvoidedWithoutLosingCoverage(self):
        # Exercise a non-planar open face without requiring the optional Surface module.
        surface = Part.BSplineSurface()
        poles = [[App.Vector(x, y, z) for y in (10, 20)]
                 for x, z in ((10, 5), (15, 11), (20, 5))]
        surface.buildFromPolesMultsKnots(
            poles, [3, 3], [2, 2], [0, 1], [0, 1], False, False, 2, 1)
        self.external.Shape = surface.toShape()
        self.doc.recompute()
        self.assertTrue(self.external.Shape.isValid())
        self.assertGreater(self.external.Shape.BoundBox.ZLength, 1)
        self.checkAvoidanceCoverage()

    def testExternalOpenSurfaceAvoidedWithoutLosingCoverage(self):
        self.checkAvoidanceCoverage()

    def checkAvoidanceCoverage(self):
        self.assertNotIn(self.external, self.job.Model.Group)
        op = self.operation()
        op.Proxy.execute(op)
        points = []
        position = App.Vector()
        forbidden = Part.makePlane(10, 10, App.Vector(10, 10, 5)).extrude(App.Vector(0, 0, 1))
        forbidden.translate(App.Vector(0, 0, -0.5))
        for command in op.Path.Commands:
            current = App.Vector(*(command.Parameters.get(axis, getattr(position, axis.lower()))
                                   for axis in "XYZ"))
            if command.Name == "G1" and ("X" in command.Parameters or "Y" in command.Parameters):
                if current.z <= 5.000001 and position.z <= 5.000001:
                    points.append(current)
                    if (current - position).Length > 1e-7:
                        segment = Part.makeLine(position, current)
                        self.assertAlmostEqual(segment.common(forbidden).Length, 0, places=6)
            position = current
        self.assertTrue(points, "No cutting moves")
        for axis in ("x", "y"):
            self.assertLess(min(getattr(p, axis) for p in points), 8)
            self.assertGreater(max(getattr(p, axis) for p in points), 22)

    def testPartialAvoidanceFailureClearsOldPath(self):
        op = self.operation()
        extra = self.doc.addObject("Part::Feature", "SecondAvoidFace")
        extra.Shape = Part.makePlane(5, 5, App.Vector(22, 22, 5))
        op.Base = list(op.Base) + [(extra, ["Face1"])]
        op.AvoidLastX_Faces = 2
        op.Path = Path.Path([Path.Command("G1", {"X": 24, "Y": 24, "Z": 5})])
        project = surface_common.create_boundary_face
        def fail_second(faces, *args, **kwargs):
            if faces[0].BoundBox.XMin >= 22:
                return None
            return project(faces, *args, **kwargs)
        with patch.object(surface_common, "create_boundary_face", side_effect=fail_second):
            with self.assertRaisesRegex(ValueError, "boundary"):
                op.Proxy.execute(op)
        self.assertEqual(len(op.Path.Commands), 0, "Stale cutting path remained")

    def testAvoidanceFailureClearsOldPathForBothStrategies(self):
        op = self.operation()
        for strategy in ("SurfaceScan", "Waterline"):
            with self.subTest(strategy=strategy):
                op.Strategy = strategy
                op.Path = Path.Path([Path.Command("G1", {"X": 15, "Y": 15, "Z": 5})])
                with patch.object(surface_common, "build_optimized_boundary", return_value=None):
                    with self.assertRaisesRegex(ValueError, "avoid"):
                        op.Proxy.execute(op)
                self.assertEqual(len(op.Path.Commands), 0, "Stale cutting path remained")
