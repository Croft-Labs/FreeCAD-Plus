# SPDX-License-Identifier: LGPL-2.1-or-later
"""#26300: tolerance-controlled freeform silhouettes, without exact HLR."""
import math
import unittest
from unittest.mock import Mock, patch
import FreeCAD as App
import Part
from Path.Base.Generator import surface_common as common


class TestFreeformBoundary(unittest.TestCase):
    def project(self, faces, offset=0, tolerance=0.01):
        with patch.object(common, "_boundary_via_area", side_effect=AssertionError("Exact HLR used")):
            result = common.create_boundary_face(faces, offset, tolerance)
        self.assertTrue(result.isValid())
        self.assertGreater(result.Area, 0)
        return result

    def testSharedSeamOffsetAppliedAfterUnion(self):
        faces = [Part.makePlane(10, 10, App.Vector(x, 0, 3)).toNurbs().Faces[0]
                 for x in (0, 10)]
        result = self.project(faces, -1)
        expected = Part.makePlane(18, 8, App.Vector(1, 1, 0))
        self.assertAlmostEqual(result.Area, expected.Area, places=4)
        self.assertAlmostEqual(result.common(expected).Area, expected.Area, places=4)

    def testOverlappingReversedFacesUnionInsteadOfCancel(self):
        first = Part.makePlane(10, 10).toNurbs().Faces[0]
        second = Part.makePlane(10, 10, App.Vector(5, 0, 4)).toNurbs().Faces[0]
        second.reverse()
        result = self.project([first, second])
        self.assertAlmostEqual(result.Area, 150, places=4)

    def testDisconnectedRegionsPreserved(self):
        faces = [Part.makePlane(10, 10, App.Vector(x, 0, 3)).toNurbs().Faces[0]
                 for x in (0, 30)]
        result = self.project(faces, -1)
        self.assertEqual(len(result.Faces), 2)
        self.assertAlmostEqual(result.Area, 128, places=4)

    def testSphereSilhouetteIncludesInteriorExtrema(self):
        sphere = Part.makeSphere(10).toNurbs()
        result = self.project(sphere.Faces)
        self.assertAlmostEqual(result.Area, math.pi * 100, delta=1)
        for i in range(72):
            angle = i * math.pi / 36
            point = App.Vector(9.95 * math.cos(angle), 9.95 * math.sin(angle), 0)
            self.assertTrue(result.isInside(point, 1e-5, True))
        self.assertLessEqual(result.BoundBox.XLength, 20.001)
        self.assertLessEqual(result.BoundBox.YLength, 20.001)

    def testCuttingOutlineFillsHolesButExplicitAvoidanceRemains(self):
        hole = Part.makePlane(4, 4, App.Vector(8, 8, 0))
        ring = Part.makePlane(20, 20).cut(hole).toNurbs().Faces[0]
        result = self.project([ring])
        self.assertAlmostEqual(result.Area, 400, places=4)
        mask = common.generate_pattern_mask(False, None, [ring], hole, 0, 0, 0.01)
        self.assertAlmostEqual(mask.common(hole).Area, 0, places=5)

    def testEmptyMeshDoesNotRestoreBoundingBoxOrExactProjection(self):
        shape = Mock()
        shape.Faces = [shape]
        shape.tessellate.return_value = ([], [])
        with self.assertRaisesRegex(ValueError, "Failed to mesh"):
            common._boundary_via_mesh(shape, 0, 0.01)

    def testPartialMeshDoesNotDropFailedFace(self):
        failed = Mock()
        failed.tessellate.return_value = ([], [])
        shape = Mock()
        shape.Faces = [Part.makePlane(10, 10), failed]
        with self.assertRaisesRegex(ValueError, "Failed to mesh"):
            common._boundary_via_mesh(shape, 0, 0.01)

    def testEdgeOnFacesHaveNoMachiningArea(self):
        face = Part.makePlane(10, 10, App.Vector(), App.Vector(1, 0, 0)).toNurbs()
        with self.assertRaisesRegex(ValueError, "no projected area"):
            common._boundary_via_mesh(face, 0, 0.01)

    def testInvalidToleranceRejected(self):
        for tolerance in (0, -1, math.nan, math.inf):
            with self.subTest(tolerance=tolerance):
                with self.assertRaisesRegex(ValueError, "tolerance"):
                    common._boundary_via_mesh(Mock(), 0, tolerance)
