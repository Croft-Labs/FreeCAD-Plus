# SPDX-License-Identifier: LGPL-2.1-or-later
"""Grouped native Body / explicit-result adapter experiments for 7.1.3."""
import math
import os
from pathlib import Path
import sys
import unittest
import FreeCAD as App
import Part
import Sketcher
from BasicShapes.ShapeReferences import linked_shape

# The prototype module must remain importable while its disposable documents are
# restored. It is deliberately absent from installed application/workbench paths.
sys.path.insert(0, str(Path(__file__).parent / "prototypes"))
import PartHistoryAdapters as adapters


class TestPartHistoryAdapters(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("HistoryAdapters")
        self.doc.UndoMode = 1
        self.part = self.doc.addObject("App::Part", "ModelPart")
        self.profile = self.doc.addObject("Sketcher::SketchObject", "Profile")
        self.part.addObject(self.profile)
        index = self.profile.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.profile.addConstraint(Sketcher.Constraint("Radius", index, 2))
        self.doc.recompute()

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def saveReopen(self, name):
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / (name + ".FCStd")
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.part = self.doc.ModelPart
        self.profile = self.doc.Profile
        for obj in self.doc.Objects:
            obj.touch()
        self.doc.recompute()

    def testTwoBodyAdaptersShareSourceWithoutCloningSketch(self):
        first, binder_a, pad_a = adapters.body_adapter(self.part, self.profile, "A", 3)
        second, binder_b, pad_b = adapters.body_adapter(self.part, self.profile, "B", 5, True)
        self.doc.recompute()
        self.assertEqual(first.Tip, pad_a)
        self.assertEqual(second.Tip, pad_b)
        self.assertEqual(self.profile.getParentGeoFeatureGroup(), self.part)
        self.assertEqual(binder_a.Support[0][0], self.profile)
        self.assertEqual(binder_b.Support[0][0], self.profile)
        self.assertEqual(sum(o.isDerivedFrom("Sketcher::SketchObject") for o in self.doc.Objects), 1)
        self.profile.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        self.assertAlmostEqual(first.Shape.Volume, math.pi * 9 * 3, places=6)
        self.assertAlmostEqual(second.Shape.Volume, math.pi * 9 * 5, places=6)
        self.saveReopen("BodyAdapterProof")
        self.assertEqual(self.doc.AProfile.Support[0][0], self.profile)
        self.assertEqual(self.doc.BProfile.Support[0][0], self.profile)
        self.assertAlmostEqual(self.doc.A.Shape.Volume, math.pi * 9 * 3, places=6)
        self.assertAlmostEqual(self.doc.B.Shape.Volume, math.pi * 9 * 5, places=6)

    def testExplicitResultRolesSurviveRenameRecomputeAndPersistence(self):
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        identities = [o.BodyIdentity for o in results]
        self.assertNotEqual(*identities)
        self.assertEqual(len(consumer.Shape.Solids), 2)
        self.assertAlmostEqual(results[1].Shape.BoundBox.XMin, 8, places=6)
        self.assertAlmostEqual(consumer.Shape.Volume, math.pi * 4 * 6, places=6)
        results[0].Label = "Renamed result"
        consumer.Sources = list(reversed(results))
        self.profile.setDatum(0, App.Units.Quantity("3 mm"))
        feature.Length = 4
        self.doc.recompute()
        self.assertAlmostEqual(consumer.Shape.Volume, math.pi * 9 * 8, places=6)
        self.assertEqual([o.BodyIdentity for o in results], identities)
        self.saveReopen("ExplicitResultProof")
        restored = [self.doc.LeftResult, self.doc.RightResult]
        self.assertEqual([o.BodyIdentity for o in restored], identities)
        self.assertEqual([o.OutputRole for o in restored], ["Left", "Right"])
        self.assertAlmostEqual(restored[0].Shape.BoundBox.XMin, -3, places=6)
        self.assertAlmostEqual(restored[1].Shape.BoundBox.XMin, 7, places=6)
        self.assertEqual(self.doc.ResultUnion.Sources, list(reversed(restored)))
        self.assertAlmostEqual(self.doc.ResultUnion.Shape.Volume, math.pi * 9 * 8, places=6)

    def testUnavailableResultCannotLeaveSuccessfulConsumer(self):
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        right_id = results[1].BodyIdentity
        feature.RightEnabled = False
        self.doc.recompute()
        self.assertEqual(results[1].ResultStatus, "Unavailable")
        self.assertTrue(results[1].Shape.isNull())
        self.assertEqual(consumer.ResultStatus, "Failed")
        self.assertTrue(consumer.Shape.isNull())
        feature.RightEnabled = True
        self.doc.recompute()
        self.assertEqual(results[1].BodyIdentity, right_id)
        self.assertEqual(consumer.ResultStatus, "Ready")
        self.assertEqual(len(consumer.Shape.Solids), 2)

    def testResultTransactionsRestoreIdentityAndGeometry(self):
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        ids = [o.BodyIdentity for o in results]
        original = consumer.Shape.Volume
        self.doc.openTransaction("Change prototype length")
        feature.Length = 6
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertAlmostEqual(consumer.Shape.Volume, 2 * original, places=6)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(consumer.Shape.Volume, original, places=6)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(consumer.Shape.Volume, 2 * original, places=6)
        self.doc.openTransaction("Cancel unavailable result")
        feature.RightEnabled = False
        self.doc.recompute()
        self.doc.abortTransaction()
        self.doc.recompute()
        self.assertEqual([o.BodyIdentity for o in results], ids)
        self.assertEqual(consumer.ResultStatus, "Ready")
        self.assertAlmostEqual(consumer.Shape.Volume, 2 * original, places=6)

    def testRotatedProfileAndPartPreserveOutputFrame(self):
        self.profile.Placement = App.Placement(App.Vector(4, 5, 6), App.Rotation(App.Vector(0, 1, 0), 45))
        self.part.Placement = App.Placement(App.Vector(50, 20, 10), App.Rotation(App.Vector(0, 0, 1), 30))
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        for result, offset in zip(results, (0, 10)):
            expected = Part.makeCylinder(2, 3)
            local = App.Placement(App.Vector(offset, 0, 0), App.Rotation()).multiply(self.profile.Placement)
            expected.Placement = self.part.Placement.multiply(local)
            actual = linked_shape((result, []))
            self.assertAlmostEqual(actual.Volume, expected.Volume, places=6)
            self.assertAlmostEqual(actual.common(expected).Volume, expected.Volume, places=6)
        self.saveReopen("TransformedResultProof")
        self.assertAlmostEqual(self.doc.ResultUnion.Shape.Volume, math.pi * 4 * 6, places=6)

    def testCrossPartSourceMoveInvalidatesResult(self):
        destination = self.doc.addObject("App::Part", "Destination")
        destination.Placement = App.Placement(App.Vector(0, 20, 0), App.Rotation())
        feature, results, consumer = adapters.part_results(destination, self.profile)
        self.part.Placement.Base = App.Vector(30, 0, 0)
        self.doc.recompute()
        self.assertAlmostEqual(linked_shape((results[0], [])).BoundBox.XMin, 28, places=6)
        self.doc.openTransaction("Move source part")
        self.part.Placement.Base = App.Vector(40, 0, 0)
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertAlmostEqual(linked_shape((results[0], [])).BoundBox.XMin, 38, places=6)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(linked_shape((results[0], [])).BoundBox.XMin, 28, places=6)

    def testAssemblyLocalCutDoesNotEditSharedResult(self):
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        assembly = self.doc.addObject("App::Part", "Assembly")
        assembly.Placement.Base = App.Vector(100, 0, 0)
        occurrences = []
        for x in (30, 60):
            link = self.doc.addObject("App::Link", "Occurrence")
            assembly.addObject(link)
            link.setLink(results[0])
            link.LinkPlacement.Base = App.Vector(x, 0, 0)
            occurrences.append(link)
        tool = self.doc.addObject("Part::Box", "LocalTool")
        assembly.addObject(tool)
        tool.Length, tool.Width, tool.Height = 10, 20, 20
        tool.Placement.Base = App.Vector(30, -10, -5)
        cut = self.doc.addObject("Part::Cut", "LocalCut")
        assembly.addObject(cut)
        cut.Base, cut.Tool = occurrences[0], tool
        self.doc.recompute()
        for radius in (2, 3):
            self.profile.setDatum(0, App.Units.Quantity(f"{radius} mm"))
            self.doc.recompute()
            full = math.pi * radius * radius * 3
            self.assertAlmostEqual(results[0].Shape.Volume, full, places=6)
            self.assertAlmostEqual(linked_shape((occurrences[1], [])).Volume, full, places=6)
            self.assertAlmostEqual(cut.Shape.Volume, full / 2, places=6)
            self.assertAlmostEqual(linked_shape((cut, [])).BoundBox.XMax, 130, places=6)
        self.saveReopen("AssemblyLocalProof")
        self.assertAlmostEqual(self.doc.LocalCut.Shape.Volume, math.pi * 9 * 3 / 2, places=6)

    def testDraftCloneClearsUnavailableResult(self):
        from draftmake.make_clone import make_clone
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        clone = make_clone(results[1], forcedraft=True)
        self.doc.recompute()
        self.assertAlmostEqual(clone.Shape.Volume, results[1].Shape.Volume, places=6)
        self.profile.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        self.assertAlmostEqual(clone.Shape.Volume, math.pi * 9 * 3, places=6)
        feature.RightEnabled = False
        self.doc.recompute()
        self.assertTrue(clone.Shape.isNull(), "Draft consumer retained unavailable result geometry")

    def testAttachedProfileFollowsPlaneAndUndo(self):
        plane = self.doc.addObject("Part::Plane", "SupportPlane")
        self.part.addObject(plane)
        plane.Length, plane.Width = 20, 20
        plane.Placement = App.Placement(App.Vector(0, 0, 5), App.Rotation(App.Vector(0, 1, 0), 30))
        self.profile.AttachmentSupport = [(plane, "Face1")]
        self.profile.MapMode = "FlatFace"
        self.profile.AttachmentOffset.Base = App.Vector(0, 0, 2)
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        original = linked_shape((results[0], [])).CenterOfMass
        original_id = results[0].BodyIdentity
        self.assertNotIn("Invalid", self.profile.State)
        self.assertAlmostEqual(results[0].Shape.Volume, math.pi * 4 * 3, places=6)
        self.doc.openTransaction("Move attachment support")
        plane.Placement.Base.z += 10
        self.doc.recompute()
        self.doc.commitTransaction()
        delta = linked_shape((results[0], [])).CenterOfMass - original
        self.assertAlmostEqual((delta - App.Vector(0, 0, 10)).Length, 0, places=6)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual((linked_shape((results[0], [])).CenterOfMass - original).Length, 0, places=6)
        self.doc.redo()
        self.doc.recompute()
        self.saveReopen("AttachedProfileProof")
        self.assertEqual(self.doc.LeftResult.BodyIdentity, original_id)
        self.assertEqual(self.profile.AttachmentSupport[0][0], self.doc.SupportPlane)
        self.assertEqual(self.profile.MapMode, "FlatFace")
        self.assertAlmostEqual((linked_shape((self.doc.LeftResult, [])).CenterOfMass
                                - original - App.Vector(0, 0, 10)).Length, 0, places=6)

    def testDeliberatePlanarReattachmentPreservesOffsetAndHistory(self):
        from SketchReattachment import reattach_planar
        old_plane = self.doc.addObject("Part::Plane", "OldSupport")
        new_plane = self.doc.addObject("Part::Plane", "NewSupport")
        for plane in (old_plane, new_plane):
            self.part.addObject(plane)
            plane.Length, plane.Width = 20, 20
        new_plane.Placement.Base.z = 10
        self.profile.AttachmentSupport = [(old_plane, "Face1")]
        self.profile.MapMode = "FlatFace"
        self.profile.AttachmentOffset.Base.z = 2
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        initial = linked_shape((results[0], [])).CenterOfMass
        identity = results[0].BodyIdentity
        reattach_planar(self.profile, new_plane, "Face1")
        self.assertAlmostEqual(self.profile.AttachmentOffset.Base.z, 2)
        self.assertAlmostEqual((linked_shape((results[0], [])).CenterOfMass
                                - initial - App.Vector(0, 0, 10)).Length, 0, places=6)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.profile.AttachmentSupport[0][0], old_plane)
        self.assertAlmostEqual((linked_shape((results[0], [])).CenterOfMass - initial).Length,
                               0, places=6)
        self.doc.redo()
        self.doc.recompute()
        self.saveReopen("ReattachedSketchProof")
        self.assertEqual(self.profile.AttachmentSupport[0][0], self.doc.NewSupport)
        self.assertAlmostEqual(self.profile.AttachmentOffset.Base.z, 2)
        self.assertEqual(self.doc.LeftResult.BodyIdentity, identity)
        self.assertAlmostEqual((linked_shape((self.doc.LeftResult, [])).CenterOfMass
                                - initial - App.Vector(0, 0, 10)).Length, 0, places=6)

    def testReattachmentRejectsMissingAndCurvedFacesWithoutMutation(self):
        from SketchReattachment import reattach_planar
        plane = self.doc.addObject("Part::Plane", "ValidSupport")
        sphere = self.doc.addObject("Part::Sphere", "CurvedSupport")
        self.profile.AttachmentSupport = [(plane, "Face1")]
        self.profile.MapMode = "FlatFace"
        self.profile.AttachmentOffset.Base.z = 2
        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        before = linked_shape((results[0], [])).CenterOfMass
        placement = self.profile.Placement
        for support, face in ((plane, "Face99"), (sphere, "Face1")):
            with self.assertRaisesRegex(ValueError, "unavailable|planar"):
                reattach_planar(self.profile, support, face)
            self.doc.recompute()
            self.assertEqual(self.profile.AttachmentSupport[0][0], plane)
            self.assertEqual(self.profile.Placement, placement)
            self.assertAlmostEqual(self.profile.AttachmentOffset.Base.z, 2)
            self.assertNotIn("Invalid", self.profile.State)
            self.assertAlmostEqual((linked_shape((results[0], [])).CenterOfMass - before).Length,
                                   0, places=6)

    def rotatedReattachmentFixture(self):
        self.part.Placement = App.Placement(App.Vector(30, 40, 50),
                                           App.Rotation(App.Vector(1, 0, 0), 25))
        planes = [self.doc.addObject("Part::Plane", name)
                  for name in ("OriginalPlane", "RotatedPlane")]
        for plane in planes:
            self.part.addObject(plane)
            plane.Length, plane.Width = 20, 20
        planes[1].Placement = App.Placement(App.Vector(4, 5, 10),
                                          App.Rotation(App.Vector(0, 1, 0), 60))
        self.profile.AttachmentSupport = [(planes[0], "Face1")]
        self.profile.MapMode = "FlatFace"
        self.profile.AttachmentOffset = App.Placement(App.Vector(1, 2, 3),
                                                     App.Rotation(App.Vector(0, 0, 1), 15))
        adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        return planes

    def assertPlacementNear(self, actual, expected):
        # Three basis directions plus origin check translation and full rotation.
        for point in (App.Vector(), App.Vector(1, 0, 0), App.Vector(0, 1, 0),
                      App.Vector(0, 0, 1)):
            self.assertAlmostEqual((actual.multVec(point) - expected.multVec(point)).Length,
                                   0, places=6)

    def testRotatedReattachmentPreservesLocalOffset(self):
        from SketchReattachment import reattach_planar
        old, new = self.rotatedReattachmentFixture()
        offset = self.profile.AttachmentOffset
        initial = self.profile.Placement
        reattach_planar(self.profile, new, "Face1", "preserve-local")
        self.assertPlacementNear(self.profile.AttachmentOffset, offset)
        self.assertGreater((self.profile.Placement.Base - initial.Base).Length, 1)
        self.assertPlacementNear(self.profile.Placement, new.Placement.multiply(initial))
        self.assertNotIn("Invalid", self.doc.LeftResult.State)
        self.assertAlmostEqual(self.doc.LeftResult.Shape.Volume, math.pi * 4 * 3, places=6)

    def testRotatedReattachmentPreservesWorldPlacementAndRestore(self):
        from SketchReattachment import reattach_planar
        old, new = self.rotatedReattachmentFixture()
        world = self.profile.getGlobalPlacement()
        center = linked_shape((self.doc.LeftResult, [])).CenterOfMass
        identity = self.doc.LeftResult.BodyIdentity
        offset = self.profile.AttachmentOffset
        reattach_planar(self.profile, new, "Face1", "preserve-world")
        self.assertPlacementNear(self.profile.getGlobalPlacement(), world)
        self.assertAlmostEqual((linked_shape((self.doc.LeftResult, [])).CenterOfMass
                                - center).Length, 0, places=6)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)
        self.assertPlacementNear(self.profile.AttachmentOffset, offset)
        self.doc.redo()
        self.doc.recompute()
        self.saveReopen("PreservedWorldReattachmentProof")
        self.assertEqual(self.profile.AttachmentSupport[0][0], self.doc.RotatedPlane)
        self.assertPlacementNear(self.profile.getGlobalPlacement(), world)
        self.assertEqual(self.doc.LeftResult.BodyIdentity, identity)
        self.assertAlmostEqual((linked_shape((self.doc.LeftResult, [])).CenterOfMass
                                - center).Length, 0, places=6)
        # The new support still drives the sketch after the compensating offset.
        self.doc.RotatedPlane.Placement.Base.z += 6
        self.doc.recompute()
        delta = self.profile.getGlobalPlacement().Base - world.Base
        self.assertAlmostEqual((delta - self.part.Placement.Rotation.multVec(
            App.Vector(0, 0, 6))).Length, 0, places=6)

    def testReattachmentRepairsMissingFaceWithExplicitLocalPolicy(self):
        from SketchReattachment import reattach_planar
        old, new = self.rotatedReattachmentFixture()
        identity = self.doc.LeftResult.BodyIdentity
        offset = self.profile.AttachmentOffset
        self.profile.AttachmentSupport = [(old, "Face99")]
        self.doc.recompute()
        self.assertIn("Invalid", self.profile.State)
        with self.assertRaisesRegex(ValueError, "valid recomputed"):
            reattach_planar(self.profile, new, "Face1", "preserve-world")
        self.assertEqual(self.profile.AttachmentSupport[0][1], ("Face99",))
        reattach_planar(self.profile, new, "Face1", "preserve-local")
        self.assertNotIn("Invalid", self.profile.State)
        self.assertPlacementNear(self.profile.AttachmentOffset, offset)
        self.assertAlmostEqual(self.doc.LeftResult.Shape.Volume, math.pi * 4 * 3, places=6)
        self.doc.undo()
        self.doc.recompute()
        self.assertIn("Invalid", self.profile.State)
        self.assertEqual(self.profile.AttachmentSupport[0][1], ("Face99",))
        self.doc.redo()
        self.doc.recompute()
        self.saveReopen("RepairedSupportProof")
        self.assertNotIn("Invalid", self.profile.State)
        self.assertNotIn("Invalid", self.doc.LeftResult.State)
        self.assertEqual(self.profile.AttachmentSupport[0][0], self.doc.RotatedPlane)
        self.assertEqual(self.doc.LeftResult.BodyIdentity, identity)
        self.assertPlacementNear(self.profile.AttachmentOffset, offset)

    def testReattachmentDoesNotCommitOrAbortCallerTransaction(self):
        from SketchReattachment import reattach_planar
        old, new = self.rotatedReattachmentFixture()
        label = self.profile.Label
        self.doc.openTransaction("Caller-owned edit")
        self.profile.Label = "Uncommitted caller edit"
        with self.assertRaisesRegex(ValueError, "current transaction"):
            reattach_planar(self.profile, new, "Face1")
        self.assertTrue(self.doc.HasPendingTransaction)
        self.assertEqual(self.profile.Label, "Uncommitted caller edit")
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)
        self.doc.abortTransaction()
        self.doc.recompute()
        self.assertEqual(self.profile.Label, label)
        reattach_planar(self.profile, new, "Face1")
        self.assertFalse(self.doc.HasPendingTransaction)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)

    def testReattachmentRejectsDerivedSupportCycleBeforeMutation(self):
        from SketchReattachment import reattach_planar
        old, new = self.rotatedReattachmentFixture()
        derived = self.doc.addObject("Part::Extrusion", "DerivedSupport")
        self.part.addObject(derived)
        derived.Base = self.profile
        derived.Dir = App.Vector(0, 0, 5)
        derived.Solid = True
        self.doc.recompute()
        self.assertNotIn("Invalid", derived.State)
        face_name = next("Face%d" % (i + 1) for i, face in enumerate(derived.Shape.Faces)
                         if isinstance(face.Surface, Part.Plane))
        before = self.profile.getGlobalPlacement()
        with self.assertRaisesRegex(ValueError, "cycle"):
            reattach_planar(self.profile, derived, face_name)
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)
        self.assertPlacementNear(self.profile.getGlobalPlacement(), before)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.doc.recompute()
        self.assertNotIn("Invalid", self.profile.State)
        self.assertNotIn("Invalid", derived.State)

    def testReattachmentRejectsStaleAndInvalidSupportThenRecovers(self):
        from SketchReattachment import reattach_planar
        old, new = self.rotatedReattachmentFixture()
        box = self.doc.addObject("Part::Box", "FailingSupport")
        self.part.addObject(box)
        self.doc.recompute()
        before = self.profile.getGlobalPlacement()
        new.touch()
        with self.assertRaisesRegex(ValueError, "valid and recomputed"):
            reattach_planar(self.profile, new, "Face1")
        self.doc.recompute()
        box.Length = 0
        self.doc.recompute()
        self.assertIn("Invalid", box.State)
        with self.assertRaisesRegex(ValueError, "valid and recomputed"):
            reattach_planar(self.profile, box, "Face1")
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)
        self.assertPlacementNear(self.profile.getGlobalPlacement(), before)
        self.assertFalse(self.doc.HasPendingTransaction)
        box.Length = 10
        self.doc.recompute()
        reattach_planar(self.profile, box, "Face1")
        self.assertEqual(self.profile.AttachmentSupport[0][0], box)
        self.assertNotIn("Invalid", self.profile.State)
        self.assertNotIn("Invalid", self.doc.LeftResult.State)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)
        self.assertPlacementNear(self.profile.getGlobalPlacement(), before)

    def testReattachmentPreviewMatchesBothCommittedPolicies(self):
        from SketchReattachment import preview_planar, reattach_planar
        old, new = self.rotatedReattachmentFixture()
        original = self.profile.getGlobalPlacement()
        offset = self.profile.AttachmentOffset
        center = linked_shape((self.doc.LeftResult, [])).CenterOfMass
        for policy in ("preserve-local", "preserve-world"):
            candidate, candidate_offset = preview_planar(self.profile, new, "Face1", policy)
            self.assertEqual(self.profile.AttachmentSupport[0][0], old)
            self.assertPlacementNear(self.profile.getGlobalPlacement(), original)
            self.assertPlacementNear(self.profile.AttachmentOffset, offset)
            self.assertAlmostEqual((linked_shape((self.doc.LeftResult, [])).CenterOfMass
                                    - center).Length, 0, places=6)
            self.assertFalse(self.doc.HasPendingTransaction)
            reattach_planar(self.profile, new, "Face1", policy)
            self.assertPlacementNear(self.profile.getGlobalPlacement(), candidate)
            self.assertPlacementNear(self.profile.AttachmentOffset, candidate_offset)
            self.doc.undo()
            self.doc.recompute()
            self.assertEqual(self.profile.AttachmentSupport[0][0], old)

    def testReattachmentPreviewLeavesExistingUndoHistoryIntact(self):
        from SketchReattachment import preview_planar
        old, new = self.rotatedReattachmentFixture()
        original_label = self.profile.Label
        self.doc.openTransaction("Existing user edit")
        self.profile.Label = "User label"
        self.doc.commitTransaction()
        self.doc.recompute()
        for policy in ("preserve-local", "preserve-world", "preserve-local"):
            preview_planar(self.profile, new, "Face1", policy)
        with self.assertRaisesRegex(ValueError, "unavailable"):
            preview_planar(self.profile, new, "Face99")
        self.assertEqual(self.profile.Label, "User label")
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.profile.Label, original_label)
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(self.profile.Label, "User label")
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)

    def testPreviewDoesNotChangeOrRecomputeOriginalDocument(self):
        from SketchReattachment import preview_planar
        old, new = self.rotatedReattachmentFixture()
        events = []
        original_doc = self.doc
        class Observer:
            def slotChangedObject(self, obj, prop):
                if obj.Document == original_doc:
                    events.append((obj.Name, prop))
            def slotRecomputedDocument(self, doc):
                if doc == original_doc:
                    events.append((doc.Name, "recomputed"))
        observer = Observer()
        documents = set(App.listDocuments())
        App.addDocumentObserver(observer)
        try:
            for policy in ("preserve-local", "preserve-world"):
                preview_planar(self.profile, new, "Face1", policy)
            self.assertEqual(events, [])
            self.assertEqual(set(App.listDocuments()), documents)
            self.assertEqual(App.ActiveDocument, self.doc)
        finally:
            App.removeDocumentObserver(observer)

    def testPreviewPreservesAlreadyPopulatedRedoStack(self):
        from SketchReattachment import preview_planar
        old, new = self.rotatedReattachmentFixture()
        label = self.profile.Label
        self.doc.openTransaction("Edit to redo after preview")
        self.profile.Label = "Redo must survive"
        self.doc.commitTransaction()
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.profile.Label, label)
        for policy in ("preserve-local", "preserve-world"):
            preview_planar(self.profile, new, "Face1", policy)
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(self.profile.Label, "Redo must survive")
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)

    def testReversedAttachmentPreviewMatchesCommitAndRestore(self):
        from SketchReattachment import preview_planar, reattach_planar
        old, new = self.rotatedReattachmentFixture()
        self.profile.MapReversed = True
        self.doc.recompute()
        original = self.profile.getGlobalPlacement()
        for policy in ("preserve-local", "preserve-world"):
            candidate, offset = preview_planar(self.profile, new, "Face1", policy)
            self.assertTrue(self.profile.MapReversed)
            self.assertPlacementNear(self.profile.getGlobalPlacement(), original)
            reattach_planar(self.profile, new, "Face1", policy)
            self.assertPlacementNear(self.profile.getGlobalPlacement(), candidate)
            self.assertPlacementNear(self.profile.AttachmentOffset, offset)
            self.assertTrue(self.profile.MapReversed)
            self.doc.undo()
            self.doc.recompute()
        reattach_planar(self.profile, new, "Face1", "preserve-world")
        self.saveReopen("ReversedAttachmentProof")
        self.assertTrue(self.profile.MapReversed)
        self.assertPlacementNear(self.profile.getGlobalPlacement(), original)
        self.assertNotIn("Invalid", self.doc.LeftResult.State)

    def testExpressionOffsetIsPreservedOrExplicitlyRejected(self):
        from SketchReattachment import preview_planar, reattach_planar
        old, new = self.rotatedReattachmentFixture()
        parameters = self.doc.addObject("App::FeaturePython", "AttachmentParameters")
        parameters.addProperty("App::PropertyLength", "Distance")
        parameters.Distance = 3
        self.profile.setExpression("AttachmentOffset.Base.z", "AttachmentParameters.Distance")
        self.doc.recompute()
        expression = self.profile.ExpressionEngine
        original = self.profile.getGlobalPlacement()
        for operation in (preview_planar, reattach_planar):
            with self.assertRaisesRegex(ValueError, "expression-driven", msg=repr(expression)):
                operation(self.profile, new, "Face1", "preserve-world")
            self.assertEqual(self.profile.ExpressionEngine, expression)
            self.assertEqual(self.profile.AttachmentSupport[0][0], old)
            self.assertPlacementNear(self.profile.getGlobalPlacement(), original)
            self.assertFalse(self.doc.HasPendingTransaction)
        candidate, offset = preview_planar(self.profile, new, "Face1", "preserve-local")
        reattach_planar(self.profile, new, "Face1", "preserve-local")
        self.assertEqual(self.profile.ExpressionEngine, expression)
        self.assertPlacementNear(self.profile.getGlobalPlacement(), candidate)
        self.assertPlacementNear(self.profile.AttachmentOffset, offset)
        self.saveReopen("ExpressionAttachmentProof")
        self.assertEqual(self.profile.ExpressionEngine, expression)
        self.doc.AttachmentParameters.Distance = 7
        self.doc.recompute()
        self.assertAlmostEqual(self.profile.AttachmentOffset.Base.z, 7)
        self.assertNotIn("Invalid", self.profile.State)
        self.assertNotIn("Invalid", self.doc.LeftResult.State)

    def testCrossPartSupportRejectedWithoutChangingEitherPart(self):
        from SketchReattachment import preview_planar, reattach_planar
        old, unused = self.rotatedReattachmentFixture()
        other = self.doc.addObject("App::Part", "SupportPart")
        other.Placement = App.Placement(App.Vector(-20, 10, 15),
                                        App.Rotation(App.Vector(0, 0, 1), 40))
        support = self.doc.addObject("Part::Plane", "CrossPartPlane")
        other.addObject(support)
        support.Placement = App.Placement(App.Vector(3, 4, 5),
                                          App.Rotation(App.Vector(0, 1, 0), 30))
        self.doc.recompute()
        original = self.profile.getGlobalPlacement()
        original_support = support.getGlobalPlacement()
        center = linked_shape((self.doc.LeftResult, [])).CenterOfMass
        documents = set(App.listDocuments())
        for policy in ("preserve-local", "preserve-world"):
            for operation in (preview_planar, reattach_planar):
                with self.assertRaisesRegex(ValueError, "reference adapter"):
                    operation(self.profile, support, "Face1", policy)
                self.assertPlacementNear(self.profile.getGlobalPlacement(), original)
                self.assertPlacementNear(support.getGlobalPlacement(), original_support)
                self.assertEqual(self.profile.AttachmentSupport[0][0], old)
                self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(set(App.listDocuments()), documents)
        self.assertAlmostEqual((linked_shape((self.doc.LeftResult, [])).CenterOfMass
                                - center).Length, 0, places=6)
        self.assertNotIn("Invalid", self.profile.State)
        self.assertNotIn("Invalid", support.State)

    def testOccurrenceSupportRejectedWithoutChangingDefinitionOrLinks(self):
        from SketchReattachment import preview_planar, reattach_planar
        old, support = self.rotatedReattachmentFixture()
        links = []
        for x in (20, 40):
            link = self.doc.addObject("App::Link", "SupportOccurrence")
            link.setLink(support)
            link.Placement.Base.x = x
            links.append(link)
        self.doc.recompute()
        original = self.profile.getGlobalPlacement()
        placements = [link.Placement for link in links]
        documents = set(App.listDocuments())
        for operation in (preview_planar, reattach_planar):
            with self.assertRaisesRegex(ValueError, "definition/occurrence policy"):
                operation(self.profile, links[0], "Face1")
        self.assertEqual(set(App.listDocuments()), documents)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(self.profile.AttachmentSupport[0][0], old)
        self.assertPlacementNear(self.profile.getGlobalPlacement(), original)
        for link, placement in zip(links, placements):
            self.assertEqual(link.LinkedObject, support)
            self.assertPlacementNear(link.Placement, placement)

    def testDrawingRadiusFollowsResultEditsUndoAndRestore(self):
        from PySide import QtCore
        import time

        def wait_for(predicate):
            deadline = time.monotonic() + 8
            while time.monotonic() < deadline:
                QtCore.QCoreApplication.processEvents()
                if predicate():
                    return
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(25, loop.quit)
                loop.exec_()
            self.fail("TechDraw did not produce the expected geometry/dimension in 8 seconds")

        feature, results, consumer = adapters.part_results(self.part, self.profile)
        self.doc.recompute()
        page = self.doc.addObject("TechDraw::DrawPage", "Page")
        template = self.doc.addObject("TechDraw::DrawSVGTemplate", "Template")
        template.Template = App.getResourceDir() + "Mod/TechDraw/Templates/ISO/A3_Landscape_blank.svg"
        page.Template = template
        view = self.doc.addObject("TechDraw::DrawViewPart", "ResultView")
        view.Source = [results[0]]
        view.Direction = App.Vector(0, 0, 1)
        page.addView(view)
        self.doc.recompute()
        wait_for(lambda: len(view.getVisibleEdges()) == 1)
        edge = view.getVisibleEdges()[0]
        self.assertIsInstance(edge.Curve, Part.Circle)
        self.assertAlmostEqual(edge.Curve.Radius, 2, places=6)
        dim = self.doc.addObject("TechDraw::DrawViewDimension", "RadiusDimension")
        dim.Type = "Radius"
        dim.MeasureType = "Projected"
        # This fixture has exactly one analytic circular projected edge; this is
        # not a general topology reference or edge-index identity assumption.
        dim.References2D = [(view, "Edge0")]
        page.addView(dim)
        self.doc.recompute()
        wait_for(lambda: abs(dim.getRawValue() - 2) < 1e-6)
        self.doc.openTransaction("Edit source radius")
        self.profile.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        self.doc.commitTransaction()
        wait_for(lambda: abs(dim.getRawValue() - 3) < 1e-6)
        self.assertAlmostEqual(view.getVisibleEdges()[0].Curve.Radius, 3, places=6)
        self.doc.undo()
        self.doc.recompute()
        wait_for(lambda: abs(dim.getRawValue() - 2) < 1e-6)
        self.doc.redo()
        self.doc.recompute()
        wait_for(lambda: abs(dim.getRawValue() - 3) < 1e-6)
        self.saveReopen("DrawingResultProof")
        dim = self.doc.RadiusDimension
        wait_for(lambda: abs(dim.getRawValue() - 3) < 1e-6)
        self.assertEqual(self.doc.ResultView.Source, [self.doc.LeftResult])
        self.assertEqual(dim.References2D[0][0], self.doc.ResultView)
        self.assertNotIn("Invalid", dim.State)
