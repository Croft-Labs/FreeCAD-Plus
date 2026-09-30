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
