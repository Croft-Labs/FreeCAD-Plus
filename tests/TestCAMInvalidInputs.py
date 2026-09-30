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
        self.source = source
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

    def testSourceEditAutomaticallyRegeneratesPath(self):
        def max_cut_x():
            return max(c.Parameters["X"] for c in self.op.Path.Commands
                       if c.Name == "G1" and "X" in c.Parameters)
        before = max_cut_x()
        self.source.Shape = Part.makeBox(30, 20, 4)
        self.doc.recompute()
        self.assertGreater(max_cut_x(), before + 5,
                           "Document recompute retained a path for the old model width")

    def testEmptySourceClearsOperationPath(self):
        self.doc.recompute()
        self.assertTrue(any(c.Name == "G1" for c in self.op.Path.Commands))
        self.source.Shape = Part.Shape()
        self.doc.recompute()
        self.assertTrue(self.job.Model.Group[0].Shape.isNull())
        self.assertEqual(len(self.op.Path.Commands), 0)
        self.source.Shape = Part.makeBox(20, 20, 4)
        self.doc.recompute()
        self.assertTrue(any(c.Name == "G1" for c in self.op.Path.Commands))

    def testModelDependenciesRestoreForLegacyOperation(self):
        import os
        from pathlib import Path
        names = self.source.Name, self.op.Name, self.job.Name
        self.op.removeProperty("ModelDependencies")
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "CAMDependencyRestore.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.source, self.op, self.job = [self.doc.getObject(n) for n in names]
        self.assertTrue(hasattr(self.op, "ModelDependencies"))
        self.assertIn(self.job.Model, self.op.ModelDependencies)
        self.doc.recompute()
        self.source.Shape = Part.Shape()
        self.doc.recompute()
        self.assertEqual(len(self.op.Path.Commands), 0)
