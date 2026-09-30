# SPDX-License-Identifier: LGPL-2.1-or-later
import os
from pathlib import Path
import sys
import unittest
import FreeCAD as App
import Part
sys.path.insert(0, str(Path(__file__).parent / "prototypes"))
import ResultLineage as lineage


class TestResultLineage(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("LineageProof")
        self.part = self.doc.addObject("App::Part", "Model")
        self.source = self.doc.addObject("Part::Box", "Source")
        self.part.addObject(self.source)
        self.source.Length, self.source.Width, self.source.Height = 10, 4, 2
        self.source.addProperty("App::PropertyString", "BodyIdentity")
        self.source.BodyIdentity = "fixture-source-identity"
        self.feature, self.children = lineage.split(self.part, self.source)
        self.doc.recompute()

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def testSplitSidesKeepIdsThroughDisappearanceAndUndo(self):
        ids = [o.BodyIdentity for o in self.children]
        self.assertEqual(len(set(ids)), 2)
        self.assertNotIn(self.source.BodyIdentity, ids)
        for child in self.children:
            self.assertAlmostEqual(child.Shape.Volume, 40)
            self.assertEqual(child.ParentIdentity, self.source.BodyIdentity)
        self.doc.openTransaction("Move split outside source")
        self.feature.CutX = 12
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertTrue(self.children[1].Shape.isNull())
        self.assertEqual(self.children[1].ResultStatus, "Unavailable")
        self.assertAlmostEqual(self.children[0].Shape.Volume, 80)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual([o.BodyIdentity for o in self.children], ids)
        self.assertAlmostEqual(self.children[1].Shape.Volume, 40)
        self.feature.CutX = 3
        self.doc.recompute()
        self.assertAlmostEqual(self.children[0].Shape.Volume, 24)
        self.assertAlmostEqual(self.children[1].Shape.Volume, 56)
        self.assertEqual([o.BodyIdentity for o in self.children], ids)

    def testPrimaryAndNewMergeIdentitySurviveReorderAndRestore(self):
        primary = lineage.merge(self.part, self.children, self.children[1])
        fresh = lineage.merge(self.part, self.children)
        self.doc.recompute()
        fresh_id = fresh.BodyIdentity
        self.assertEqual(primary.BodyIdentity, self.children[1].BodyIdentity)
        self.assertNotIn(fresh_id, [c.BodyIdentity for c in self.children])
        for result in (primary, fresh):
            self.assertAlmostEqual(result.Shape.Volume, 80)
            result.Sources = list(reversed(result.Sources))
        self.children[0].Label = "Renamed child"
        self.feature.CutX = 3
        self.doc.recompute()
        self.assertEqual(primary.BodyIdentity, self.children[1].BodyIdentity)
        self.assertEqual(fresh.BodyIdentity, fresh_id)
        self.assertEqual(primary.ParentIdentities, sorted(c.BodyIdentity for c in self.children))
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "SplitMergeProof.FCStd"
        names = primary.Name, fresh.Name
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        for obj in self.doc.Objects:
            obj.touch()
        self.doc.recompute()
        primary, fresh = [self.doc.getObject(n) for n in names]
        self.assertEqual(primary.BodyIdentity, primary.Primary.BodyIdentity)
        self.assertEqual(fresh.BodyIdentity, fresh_id)
        self.assertAlmostEqual(primary.Shape.Volume, 80)
        self.assertAlmostEqual(fresh.Shape.Volume, 80)

    def testUnavailableChildClearsMergeAndRecovers(self):
        result = lineage.merge(self.part, self.children, self.children[0])
        self.doc.recompute()
        identity = result.BodyIdentity
        self.feature.CutX = 12
        self.doc.recompute()
        self.assertTrue(result.Shape.isNull())
        self.assertEqual(result.ResultStatus, "Failed")
        self.feature.CutX = 5
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 80)
        self.assertEqual(result.BodyIdentity, identity)

    def testAmbiguousIdentityAndReplacementFailWithoutRetargeting(self):
        result = lineage.merge(self.part, self.children, self.children[0])
        self.doc.recompute()
        self.doc.openTransaction("Duplicate identity")
        self.children[1].BodyIdentity = self.children[0].BodyIdentity
        self.doc.recompute()
        self.assertEqual(result.ResultStatus, "Failed")
        self.assertTrue(result.Shape.isNull())
        self.doc.abortTransaction()
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 80)
        self.source.BodyIdentity = "replacement-identity"
        self.doc.recompute()
        self.assertEqual(self.feature.ResultStatus, "Failed")
        self.assertIn("lineage changed", self.feature.ErrorMessage)
        self.assertTrue(all(child.Shape.isNull() for child in self.children))
        self.assertTrue(result.Shape.isNull())
        self.assertEqual(self.children[0].ParentIdentity, "fixture-source-identity")

    def testOneSideWithMultipleSolidsRequiresRepair(self):
        replacement = self.doc.addObject("Part::Feature", "RevisedSource")
        self.part.addObject(replacement)
        replacement.addProperty("App::PropertyString", "BodyIdentity")
        replacement.BodyIdentity = self.source.BodyIdentity
        # Connected U-shaped source; the left half contains two separate solids.
        lower = Part.makeBox(10, 1, 2)
        upper = Part.makeBox(10, 1, 2, App.Vector(0, 3, 0))
        bridge = Part.makeBox(2, 4, 2, App.Vector(8, 0, 0))
        replacement.Shape = lower.fuse([upper, bridge]).removeSplitter()
        self.assertEqual(len(replacement.Shape.Solids), 1)
        result = lineage.merge(self.part, self.children, self.children[0])
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 80)
        self.feature.Source = replacement
        self.doc.recompute()
        self.assertEqual(self.feature.ResultStatus, "Failed")
        self.assertIn("Multiple solids", self.feature.ErrorMessage)
        self.assertTrue(all(child.Shape.isNull() for child in self.children))
        self.assertTrue(result.Shape.isNull())
