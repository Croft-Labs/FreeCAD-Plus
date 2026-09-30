# SPDX-License-Identifier: LGPL-2.1-or-later
"""Empty native clone sources invalidate cached geometry without losing placement."""
import unittest
import FreeCAD as App
import Part
from draftmake.make_clone import make_clone


class TestDraftCloneInvalidation(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("CloneInvalidation")
        self.source = self.doc.addObject("Part::Feature", "Source")
        self.source.Shape = Part.makeBox(2, 3, 4)
        self.clone = make_clone(self.source, forcedraft=True)
        self.clone.Placement.Base = App.Vector(20, 0, 0)
        self.doc.recompute()

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def testEmptySourceClearsThenRestoresAtClonePlacement(self):
        self.assertAlmostEqual(self.clone.Shape.Volume, 24)
        self.source.Shape = Part.Shape()
        self.doc.recompute()
        self.assertTrue(self.clone.Shape.isNull())
        self.assertAlmostEqual(self.clone.Placement.Base.x, 20)
        self.source.Shape = Part.makeBox(3, 3, 4)
        self.doc.recompute()
        self.assertAlmostEqual(self.clone.Shape.Volume, 36)
        self.assertAlmostEqual(self.clone.Shape.BoundBox.XMin, 20)

    def testClearingSourceListClearsCachedShape(self):
        self.clone.Objects = []
        self.doc.recompute()
        self.assertTrue(self.clone.Shape.isNull())
        self.clone.Objects = [self.source]
        self.doc.recompute()
        self.assertAlmostEqual(self.clone.Shape.Volume, 24)

    def testCAMJobModelClearsWhenNativeSourceBecomesEmpty(self):
        from Path.Main import Job
        job = Job.Create("Job", [self.source])
        self.doc.recompute()
        model = job.Model.Group[0]
        self.assertAlmostEqual(model.Shape.Volume, 24)
        self.source.Shape = Part.Shape()
        self.doc.recompute()
        self.assertTrue(model.Shape.isNull(), "CAM job retained stale model geometry")
        self.source.Shape = Part.makeBox(3, 3, 4)
        self.doc.recompute()
        self.assertAlmostEqual(model.Shape.Volume, 36)
