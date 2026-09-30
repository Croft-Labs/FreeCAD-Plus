# SPDX-License-Identifier: LGPL-2.1-or-later
"""A recomputed operation must not retain generated paths after invalid inputs."""
import FreeCAD as App
import Part
from CAMTests.PathTestUtils import PathTestWithAssets
from Path.Main import Job
from Path.Op import PlanarSurface
from Path.Post.PostList import buildPostList
from Path.Post.CAMErrors import CAMValueError


class FailingModel:
    def execute(self, obj):
        if obj.Fail:
            raise RuntimeError("Deliberate model failure")
        obj.Shape = Part.makeBox(20, 20, 4)


class TestCAMInvalidInputs(PathTestWithAssets):
    def postList(self):
        from types import SimpleNamespace
        return buildPostList(SimpleNamespace(
            _job=self.job, _operations=[self.op], _machine=None, values={}))

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

    def testReplacingModelContainerRebindsAndRecovers(self):
        previous = self.job.Model
        replacement = self.doc.addObject("App::DocumentObjectGroup", "ReplacementModel")
        self.job.Model = replacement
        self.assertEqual(len(self.op.Path.Commands), 0)
        self.doc.recompute()
        self.assertEqual(self.op.ModelDependencies, [replacement])
        self.assertNotIn(previous, self.op.OutList)
        models = list(previous.Group)
        previous.Group = []
        replacement.Group = models
        self.doc.recompute()
        self.assertTrue(any(c.Name == "G1" for c in self.op.Path.Commands))

    def testRemovingModelContainerClearsAndRecovers(self):
        previous = self.job.Model
        self.job.Model = None
        self.assertEqual(len(self.op.Path.Commands), 0)
        self.doc.recompute()
        self.assertEqual(self.op.ModelDependencies, [])
        self.assertEqual(len(self.op.Path.Commands), 0)
        self.job.Model = previous
        self.doc.recompute()
        self.assertIn(previous, self.op.ModelDependencies)
        self.assertTrue(any(c.Name == "G1" for c in self.op.Path.Commands))

    def testWaitCursorCoversGenerationAndIsRestoredOnFailure(self):
        from PySide import QtCore, QtGui
        from unittest.mock import patch

        previous = QtGui.QApplication.overrideCursor()
        previous_shape = previous.shape() if previous else None

        def fail_generation(obj):
            self.assertEqual(QtGui.QApplication.overrideCursor().shape(), QtCore.Qt.WaitCursor)
            raise RuntimeError("generation failed")

        with patch.object(self.op.Proxy, "opExecute", side_effect=fail_generation):
            with self.assertRaisesRegex(RuntimeError, "generation failed"):
                self.op.Proxy.execute(self.op)
        current = QtGui.QApplication.overrideCursor()
        self.assertEqual(current.shape() if current else None, previous_shape)
        self.assertEqual(len(self.op.Path.Commands), 0)

    def testPostRejectsDirtyOperationAndRecovers(self):
        self.doc.recompute()
        self.assertTrue(self.postList())
        self.op.StepOver = 40
        self.assertTrue(self.op.Path.Commands)
        with self.assertRaisesRegex(CAMValueError, "needs recompute"):
            self.postList()
        self.doc.recompute()
        self.assertTrue(self.postList())

    def testPostRejectsDirtySourceEvenWithCleanOperation(self):
        self.doc.recompute()
        self.source.Shape = Part.makeBox(30, 20, 4)
        self.op.purgeTouched()
        with self.assertRaisesRegex(CAMValueError, "needs recompute"):
            self.postList()
        self.doc.recompute()
        self.assertTrue(self.postList())

    def testPostRejectsFailedProducerWithCachedPathAndRecovers(self):
        producer = self.doc.addObject("PartDesign::FeaturePython", "FailingProducer")
        producer.addProperty("App::PropertyBool", "Fail")
        producer.Proxy = FailingModel()
        # Add a real upstream dependency without changing the baseline job model.
        self.source.addProperty("App::PropertyLink", "Producer")
        self.source.Producer = producer
        self.doc.recompute()
        self.assertTrue(self.postList())
        producer.Fail = True
        self.doc.recompute()
        self.assertIn("Invalid", producer.State)
        self.assertTrue(self.op.Path.Commands, "Fixture must retain a cached path")
        self.op.purgeTouched()
        with self.assertRaisesRegex(CAMValueError, "FailingProducer"):
            self.postList()
        producer.Fail = False
        self.doc.recompute()
        self.assertTrue(self.postList())

    def makeBoundary(self):
        from Path.Dressup import Boundary
        dressup = Boundary.Create(self.op)
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)
        return dressup

    def testBoundaryClippingFailureClearsCachedPathAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup import Boundary
        dressup = self.makeBoundary()
        with patch.object(Boundary.PathBoundary, "execute",
                          side_effect=RuntimeError("Deliberate clipping failure")):
            with self.assertRaisesRegex(RuntimeError, "Deliberate clipping failure"):
                dressup.Proxy.execute(dressup)
        self.assertFalse(dressup.Path.Commands)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)

    def testBoundaryOffsetFailureClearsCachedPathAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup import Boundary
        dressup = self.makeBoundary()
        dressup.Offset = 1
        with patch.object(Boundary.Path.Geom, "uncompound",
                          side_effect=RuntimeError("Deliberate offset failure")):
            with self.assertRaisesRegex(RuntimeError, "Deliberate offset failure"):
                dressup.Proxy.execute(dressup)
        self.assertFalse(dressup.Path.Commands)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)

    def testEmptyBoundaryRejectsBothModesAndRecovers(self):
        from Path.Post.PostList import _wrap_op
        dressup = self.makeBoundary()
        stock = dressup.Stock
        empty = self.doc.addObject("Part::Feature", "EmptyBoundary")
        dressup.Stock = empty
        for inside in (True, False):
            dressup.Inside = inside
            self.doc.recompute()
            self.assertFalse(dressup.Path.Commands)
            self.assertIn("Invalid", dressup.State)
            with self.assertRaises(CAMValueError):
                _wrap_op(dressup)
        dressup.Stock = stock
        dressup.Inside = True
        self.doc.recompute()
        self.assertNotIn("Invalid", dressup.State)
        self.assertTrue(dressup.Path.Commands)
        self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testMissingBoundaryBaseClearsAndRecovers(self):
        dressup = self.makeBoundary()
        dressup.Base = None
        self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        self.assertNotIn("Invalid", dressup.State)
        dressup.Base = self.op
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)
