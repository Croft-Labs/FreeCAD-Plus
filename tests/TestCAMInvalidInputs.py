# SPDX-License-Identifier: LGPL-2.1-or-later
"""A recomputed operation must not retain generated paths after invalid inputs."""
import FreeCAD as App
import Part
from CAMTests.PathTestUtils import PathTestWithAssets
from Path.Main import Job
from Path.Op import PlanarSurface


class TestCAMInvalidInputs(PathTestWithAssets):
    def setUp(self):
        super().setUp()
        self.doc = App.newDocument("CAMInvalidInputs")
        source = self.doc.addObject("Part::Feature", "Model")
        source.Shape = Part.makeBox(20, 20, 4)
        self.job = Job.Create("Job", [source])
        tool = self.assets.get("toolbit://5mm_Endmill").attach_to_doc(doc=self.doc)
        self.job.Tools.Group[0].Tool = tool
        self.op = self.doc.addObject("Path::FeaturePython", "Surface")
        proxy = PlanarSurface.ObjectSurface(self.op, "Surface")
        proxy.initOperation(self.op)
        self.op.Strategy = "SurfaceScan"
        self.op.CutPattern = "Line"
        self.op.StepOver = 50
        self.job.Operations.addObject(self.op)
        self.doc.recompute()
        proxy.execute(self.op)
        self.assertTrue(any(c.Name == "G1" for c in self.op.Path.Commands))

    def tearDown(self):
        App.closeDocument(self.doc.Name)
        super().tearDown()

    def testMissingJobModelClearsGeneratedPathAndRecovers(self):
        models = self.job.Model.Group
        self.job.Model.Group = []
        self.op.Proxy.execute(self.op)
        self.assertEqual(len(self.op.Path.Commands), 0, "Missing model retained machining commands")
        self.job.Model.Group = models
        self.doc.recompute()
        self.op.Proxy.execute(self.op)
        self.assertTrue(any(c.Name == "G1" for c in self.op.Path.Commands))

    def testMissingToolControllerClearsGeneratedPathAndRecovers(self):
        controller = self.op.ToolController
        self.op.ToolController = None
        self.op.Proxy.execute(self.op)
        self.assertEqual(len(self.op.Path.Commands), 0, "Missing tool retained machining commands")
        self.op.ToolController = controller
        self.doc.recompute()
        self.op.Proxy.execute(self.op)
        self.assertTrue(any(c.Name == "G1" for c in self.op.Path.Commands))
