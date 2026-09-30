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

    def testMissingOrNonGeometricBoundaryBlocksExportAndRecovers(self):
        from Path.Post.PostList import _wrap_op
        dressup = self.makeBoundary()
        stock = dressup.Stock
        nongeometric = self.doc.addObject("App::FeaturePython", "NonGeometricBoundary")
        for replacement in (None, nongeometric):
            dressup.Stock = replacement
            self.doc.recompute()
            self.assertFalse(dressup.Path.Commands)
            self.assertIn("Invalid", dressup.State)
            with self.assertRaises(CAMValueError):
                _wrap_op(dressup)
            dressup.Stock = stock
            self.doc.recompute()
            self.assertNotIn("Invalid", dressup.State)
            self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testCollapsedOffsetBlocksClippingAndRecovers(self):
        from unittest.mock import patch, Mock
        from Path.Dressup import Boundary
        from Path.Post.PostList import _wrap_op
        dressup = self.makeBoundary()
        collapsed = Mock()
        collapsed.makeOffsetShape.return_value = Part.Shape()
        for pieces in ([], [collapsed]):
            for inside in (True, False):
                dressup.Inside = inside
                dressup.Offset = 1
                dressup.touch()
                with patch.object(Boundary.Path.Geom, "uncompound", return_value=pieces):
                    with patch.object(Boundary.PathBoundary, "execute") as clip:
                        self.doc.recompute()
                        clip.assert_not_called()
                self.assertFalse(dressup.Path.Commands)
                self.assertIn("Invalid", dressup.State)
                with self.assertRaises(CAMValueError):
                    _wrap_op(dressup)
                dressup.Offset = 0
                dressup.Inside = True
                self.doc.recompute()
                self.assertNotIn("Invalid", dressup.State)
                self.assertTrue(_wrap_op(dressup).Path.Commands)

    def makeArray(self):
        from Path.Dressup import Array
        dressup = Array.Create(self.op)
        dressup.Copies = 1
        dressup.Offset = App.Vector(25, 0, 0)
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)
        return dressup

    def testArrayMissingBaseClearsAndRecovers(self):
        dressup = self.makeArray()
        dressup.Base = None
        self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        dressup.Base = self.op
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)

    def testArrayEmptyBaseClearsAndRecovers(self):
        dressup = self.makeArray()
        self.source.Shape = Part.Shape()
        self.doc.recompute()
        self.assertFalse(self.op.Path.Commands)
        # A failed producer can cause native recompute to skip the dressup.
        # The export guard must reject that cache before explicit execution.
        from Path.Post.PostList import _wrap_op
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.Proxy.execute(dressup)
        self.assertFalse(dressup.Path.Commands)
        self.source.Shape = Part.makeBox(20, 20, 4)
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)

    def testArrayGenerationFailureClearsAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup import Array
        from Path.Post.PostList import _wrap_op
        dressup = self.makeArray()
        with patch.object(Array.PathArray, "getPath",
                          side_effect=RuntimeError("Deliberate array failure")):
            dressup.touch()
            self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        self.assertIn("Invalid", dressup.State)
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testDogboneFailureClearsPathAndCornerCachesAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup import DogboneII
        from Path.Post.PostList import _wrap_op
        dressup = DogboneII.Create(self.op)
        self.job.Proxy.addOperation(dressup, self.op, True)
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)
        # SurfaceScan is not a corner fixture; seed caches to expose stale state.
        dressup.Proxy.bones = [object()]
        dressup.Proxy.boneTips = [App.Vector(1, 2, 3)]
        with patch.object(DogboneII.PathUtils, "getPathWithPlacement",
                          side_effect=RuntimeError("Deliberate dogbone failure")):
            dressup.touch()
            self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        self.assertEqual(dressup.Proxy.bones, [])
        self.assertIsNone(dressup.Proxy.boneTips)
        self.assertFalse(dressup.Proxy.maneuver.toPath().Commands)
        self.assertIn("Invalid", dressup.State)
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(_wrap_op(dressup).Path.Commands)

    def makeMirror(self):
        from Path.Dressup.Gui import Mirror
        dressup = self.doc.addObject("Path::FeaturePython", "Mirror")
        Mirror.ObjectDressup(dressup, self.op)
        self.job.Proxy.addOperation(dressup, self.op, True)
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)
        return dressup

    def testMirrorDisabledPreservesPlacedBaseAndDoesNotModifySource(self):
        from PathScripts import PathUtils
        dressup = self.makeMirror()
        self.op.Placement = App.Placement(App.Vector(11, 7, 3),
                                          App.Rotation(App.Vector(0, 0, 1), 30))
        dressup.MirrorAxis = "None"
        self.doc.recompute()
        source = self.op.Path.toGCode()
        expected = PathUtils.getPathWithPlacement(self.op).toGCode()
        self.assertNotEqual(source, expected, "Fixture must exercise placement")
        self.assertEqual(dressup.Path.toGCode(), expected)
        self.assertEqual(self.op.Path.toGCode(), source)

    def testMirrorCombinedOutputPreservesBaseAndSource(self):
        from PathScripts import PathUtils
        dressup = self.makeMirror()
        for translation in (App.Vector(), App.Vector(11, 7, 3)):
            self.op.Placement = App.Placement(translation, App.Rotation())
            dressup.KeepBasePath = False
            self.doc.recompute()
            mirrored = dressup.Path.Commands
            original = self.op.Path.toGCode()
            expected = PathUtils.getPathWithPlacement(self.op).copy()
            expected.addCommands(mirrored)
            dressup.KeepBasePath = True
            self.doc.recompute()
            self.assertEqual(dressup.Path.toGCode(), expected.toGCode())
            self.assertEqual(self.op.Path.toGCode(), original)
            self.assertNotIn("Touched", self.op.State)

    def testMirrorGenerationFailureClearsAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup.Gui import Mirror
        from Path.Post.PostList import _wrap_op
        dressup = self.makeMirror()
        for keep in (False, True):
            dressup.KeepBasePath = keep
            self.doc.recompute()
            self.assertTrue(dressup.Path.Commands)
            with patch.object(Mirror.PathUtils, "getPathWithPlacement",
                              side_effect=RuntimeError("Deliberate mirror failure")):
                dressup.touch()
                self.doc.recompute()
            self.assertFalse(dressup.Path.Commands)
            self.assertIn("Invalid", dressup.State)
            with self.assertRaises(CAMValueError):
                _wrap_op(dressup)
            dressup.touch()
            self.doc.recompute()
            self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testMirrorAssemblyFailureDoesNotPublishPartialBase(self):
        from unittest.mock import patch, Mock
        from Path.Dressup.Gui import Mirror
        from PathScripts import PathUtils
        dressup = self.makeMirror()
        dressup.KeepBasePath = True
        self.doc.recompute()
        placed = PathUtils.getPathWithPlacement(self.op)
        incomplete = Mock()
        incomplete.copy.return_value = incomplete
        incomplete.addCommands.side_effect = RuntimeError("Deliberate assembly failure")
        with patch.object(Mirror.PathUtils, "getPathWithPlacement",
                          side_effect=[placed, incomplete]):
            with self.assertRaisesRegex(RuntimeError, "Deliberate assembly failure"):
                dressup.Proxy.execute(dressup)
        self.assertFalse(dressup.Path.Commands)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)

    def makeAxisMap(self):
        from Path.Dressup.Gui import AxisMap
        dressup = self.doc.addObject("Path::FeaturePython", "AxisMap")
        AxisMap.ObjectDressup(dressup)
        dressup.Base = self.op
        self.job.Proxy.addOperation(dressup, self.op, True)
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)
        return dressup

    def testAxisMapInvalidRadiusBlocksExportAndRecovers(self):
        from Path.Post.PostList import _wrap_op
        dressup = self.makeAxisMap()
        for radius in (0, -10):
            dressup.Radius = radius
            self.doc.recompute()
            self.assertFalse(dressup.Path.Commands)
            self.assertIn("Invalid", dressup.State)
            with self.assertRaises(CAMValueError):
                _wrap_op(dressup)
            dressup.Radius = 45
            self.doc.recompute()
            self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testAxisMapGenerationFailureClearsAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup.Gui import AxisMap
        from Path.Post.PostList import _wrap_op
        dressup = self.makeAxisMap()
        with patch.object(AxisMap.PostUtils, "splitArcs",
                          side_effect=RuntimeError("Deliberate arc conversion failure")):
            dressup.touch()
            self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        self.assertIn("Invalid", dressup.State)
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testAxisMapMappingAndReversePreserveSource(self):
        import math
        from PathScripts import PathUtils
        dressup = self.makeAxisMap()
        self.doc.recompute()
        original = self.op.Path.toGCode()
        source = PathUtils.getPathWithPlacement(self.op).Commands
        for mapping in ("X->A", "Y->A", "X->B", "Y->B", "X->C", "Y->C"):
            for reverse in (False, True):
                dressup.AxisMap = mapping
                dressup.Reverse = reverse
                self.doc.recompute()
                result = dressup.Path.Commands
                self.assertEqual(len(result), len(source))
                checked = 0
                for before, after in zip(source, result):
                    if mapping[0] in before.Parameters:
                        expected = math.degrees(before.Parameters[mapping[0]] / 45)
                        self.assertAlmostEqual(after.Parameters[mapping[3]],
                                               -expected if reverse else expected)
                        self.assertNotIn(mapping[0], after.Parameters)
                        checked += 1
                self.assertGreater(checked, 0)
                self.assertEqual(self.op.Path.toGCode(), original)

    def makeZCorrect(self):
        import os
        from pathlib import Path as FilePath
        from Path.Dressup.Gui import ZCorrect
        probe = FilePath(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "zcorrect-probe.txt"
        probe.write_text("-10 -10 0.5\n40 -10 0.5\n-10 40 0.5\n40 40 0.5\n")
        dressup = self.doc.addObject("Path::FeaturePython", "ZCorrect")
        ZCorrect.ObjectDressup(dressup)
        dressup.Base = self.op
        dressup.probefile = str(probe)
        self.job.Proxy.addOperation(dressup, self.op, True)
        self.doc.recompute()
        self.assertNotIn("Invalid", dressup.State)
        self.assertTrue(dressup.Path.Commands)
        self.assertFalse(dressup.interpSurface.isNull())
        self.assertTrue(any(c.Name == "G1" and abs(c.Parameters.get("Z", -99) - 4.5) < 1e-6
                            for c in dressup.Path.Commands))
        return dressup, probe

    def testZCorrectMissingProbeClearsSurfaceAndRecovers(self):
        from Path.Post.PostList import _wrap_op
        dressup, probe = self.makeZCorrect()
        original = dressup.Path.toGCode()
        dressup.probefile = str(probe) + ".missing"
        self.doc.recompute()
        self.assertTrue(dressup.interpSurface.isNull())
        self.assertFalse(dressup.Path.Commands)
        self.assertIn("Invalid", dressup.State)
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.probefile = str(probe)
        self.doc.recompute()
        self.assertEqual(_wrap_op(dressup).Path.toGCode(), original)

    def testZCorrectInvalidProbeAndOutsideAreaBlockOutput(self):
        from Path.Post.PostList import _wrap_op
        dressup, probe = self.makeZCorrect()
        original_data = probe.read_text()
        # Insufficient input, unusable collinear grid, and a valid but too-small grid.
        for data in ("0 0 0\n", "0 0 0\n1 0 0\n2 0 0\n",
                     "0 0 0\n1 0 0\n0 1 0\n1 1 0\n"):
            probe.write_text(data)
            dressup.touch()
            self.doc.recompute()
            self.assertIn("Invalid", dressup.State)
            self.assertFalse(dressup.Path.Commands)
            with self.assertRaises(CAMValueError):
                _wrap_op(dressup)
            probe.write_text(original_data)
            dressup.touch()
            self.doc.recompute()
            self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testZCorrectInterpolationFailureClearsAndRecovers(self):
        from unittest.mock import patch
        from Path.Post.PostList import _wrap_op
        dressup, probe = self.makeZCorrect()
        with patch.object(dressup.Proxy, "_bilinearInterpolate",
                          side_effect=RuntimeError("Deliberate interpolation failure")):
            dressup.touch()
            self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        self.assertIn("Invalid", dressup.State)
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testZCorrectClearingProbeUsesUncorrectedPlacedBase(self):
        from PathScripts import PathUtils
        dressup, probe = self.makeZCorrect()
        self.op.Placement = App.Placement(App.Vector(1, 2, 3), App.Rotation())
        dressup.probefile = ""
        self.doc.recompute()
        self.assertNotIn("Invalid", dressup.State)
        self.assertTrue(dressup.interpSurface.isNull())
        self.assertEqual(dressup.Path.toGCode(),
                         PathUtils.getPathWithPlacement(self.op).toGCode())

    def testZCorrectNonFiniteProbeCoordinatesRejectAndRecover(self):
        from Path.Post.PostList import _wrap_op
        dressup, probe = self.makeZCorrect()
        original_data = probe.read_text()
        for axis in range(3):
            for invalid in ("nan", "inf", "-inf"):
                row = ["-10", "-10", "0.5"]
                row[axis] = invalid
                probe.write_text(" ".join(row) + "\n" + original_data)
                dressup.touch()
                self.doc.recompute()
                self.assertFalse(dressup.Path.Commands)
                self.assertTrue(dressup.interpSurface.isNull())
                self.assertIn("Invalid", dressup.State)
                with self.assertRaises(CAMValueError):
                    _wrap_op(dressup)
                probe.write_text(original_data)
                dressup.touch()
                self.doc.recompute()
                self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testZCorrectNonPositiveInterpolationRejectsAndRecovers(self):
        from Path.Post.PostList import _wrap_op
        dressup, probe = self.makeZCorrect()
        for name in ("ArcInterpolate", "SegInterpolate"):
            original = getattr(dressup, name).Value
            for invalid in (0, -1):
                setattr(dressup, name, invalid)
                self.doc.recompute()
                self.assertFalse(dressup.Path.Commands)
                self.assertIn("Invalid", dressup.State)
                with self.assertRaises(CAMValueError):
                    _wrap_op(dressup)
                setattr(dressup, name, original)
                self.doc.recompute()
                self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testZCorrectLinearSubdivisionHonorsMaximumLength(self):
        import Path
        import math
        dressup, probe = self.makeZCorrect()
        base = self.doc.addObject("Path::Feature", "StraightPath")
        dressup.Base = base
        dressup.SegInterpolate = 1
        for length in (0.5, 1, 1.01, 2, 2.5):
            base.Path = Path.Path([Path.Command("G0", {"X": 0, "Y": 0, "Z": 4}),
                                   Path.Command("G1", {"X": length, "Y": 0, "Z": 4})])
            self.doc.recompute()
            self.assertNotIn("Invalid", dressup.State)
            xs = [c.Parameters["X"] for c in dressup.Path.Commands
                  if c.Name == "G1" and c.Parameters.get("X", 0) > 0]
            self.assertEqual(len(xs), math.ceil(length))
            self.assertAlmostEqual(xs[-1], length)
            for start, end in zip([0] + xs, xs):
                self.assertLessEqual(end - start, 1 + 1e-9)

    def makeEntryDressup(self, kind):
        from Path.Dressup.Gui import Dragknife, RampEntry
        dressup = self.doc.addObject("Path::FeaturePython", kind)
        if kind == "Dragknife":
            Dragknife.ObjectDressup(dressup)
            dressup.Base = self.op
            dressup.offset = 1
            dressup.pivotheight = 1
            dressup.filterAngle = 30
        else:
            self.op.ToolController.HorizFeed = 100
            self.op.ToolController.VertFeed = 50
            self.op.ToolController.RampFeed = 50
            RampEntry.ObjectDressup(dressup, self.op)
            dressup.Proxy.setup(dressup)
        self.job.Proxy.addOperation(dressup, self.op, True)
        self.doc.recompute()
        self.assertNotIn("Invalid", dressup.State)
        self.assertTrue(dressup.Path.Commands)
        return dressup

    def testDragknifeMissingAndEmptyBaseClearAndRecover(self):
        dressup = self.makeEntryDressup("Dragknife")
        empty = self.doc.addObject("Path::Feature", "EmptyDragknifeBase")
        for base in (None, empty):
            dressup.Base = base
            self.doc.recompute()
            self.assertFalse(dressup.Path.Commands)
            dressup.Base = self.op
            self.doc.recompute()
            self.assertTrue(dressup.Path.Commands)

    def testDragknifeGenerationFailureClearsAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup.Gui import Dragknife
        from Path.Post.PostList import _wrap_op
        dressup = self.makeEntryDressup("Dragknife")
        with patch.object(Dragknife.PathUtils, "getPathWithPlacement",
                          side_effect=RuntimeError("Deliberate dragknife failure")):
            dressup.touch()
            self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        self.assertIn("Invalid", dressup.State)
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testRampGenerationFailureClearsAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup.Gui import RampEntry
        from Path.Post.PostList import _wrap_op
        dressup = self.makeEntryDressup("RampEntry")
        with patch.object(RampEntry.RampEntry, "generate",
                          side_effect=RuntimeError("Deliberate ramp failure")):
            dressup.touch()
            self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        self.assertIn("Invalid", dressup.State)
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(_wrap_op(dressup).Path.Commands)

    def makePlunge(self):
        from Path.Dressup.Gui import PlungeMilling
        self.op.ToolController.VertFeed = 50
        dressup = self.doc.addObject("Path::FeaturePython", "DressupPlungeMilling")
        PlungeMilling.ObjectDressup(dressup, self.op)
        self.job.Proxy.addOperation(dressup, self.op, True)
        self.doc.recompute()
        self.assertNotIn("Invalid", dressup.State)
        self.assertTrue(any(c.Name == "G1" for c in dressup.Path.Commands))
        return dressup

    def testPlungeGenerationFailureClearsAndRecovers(self):
        from unittest.mock import patch
        from Path.Dressup.Gui import PlungeMilling
        from Path.Post.PostList import _wrap_op
        dressup = self.makePlunge()
        with patch.object(PlungeMilling.Path.Geom, "edgeForCmd",
                          side_effect=RuntimeError("Deliberate plunge failure")):
            dressup.touch()
            self.doc.recompute()
        self.assertFalse(dressup.Path.Commands)
        self.assertIn("Invalid", dressup.State)
        with self.assertRaises(CAMValueError):
            _wrap_op(dressup)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testPlungeInvalidStepoverBlocksExportAndRecovers(self):
        from Path.Post.PostList import _wrap_op
        dressup = self.makePlunge()
        dressup.setExpression("StepOver", None)
        for value in (0, -1):
            dressup.StepOver = value
            self.doc.recompute()
            self.assertFalse(dressup.Path.Commands)
            self.assertIn("Invalid", dressup.State)
            with self.assertRaises(CAMValueError):
                _wrap_op(dressup)
            dressup.StepOver = 1
            self.doc.recompute()
            self.assertTrue(_wrap_op(dressup).Path.Commands)

    def testCustomNamedNestedDressupsResolveOperationAndTool(self):
        from Path.Dressup import Array, Utils
        from Path.Dressup.Gui import Mirror
        inner = Array.Create(self.op, "RepeatedPath")
        outer = self.doc.addObject("Path::FeaturePython", "ReflectedPath")
        Mirror.ObjectDressup(outer, inner)
        self.job.Proxy.addOperation(outer, inner, True)
        self.doc.recompute()
        self.assertTrue(outer.Path.Commands)
        self.assertEqual(Utils.baseOp(outer), self.op)
        self.assertEqual(Utils.toolController(outer), self.op.ToolController)
        inner.Base = None
        self.assertIsNone(Utils.baseOp(outer))
        sentinel = object()
        self.assertIs(Utils.toolController(outer, sentinel), sentinel)
        inner.Base = self.op
        self.doc.recompute()
        self.assertEqual(Utils.baseOp(outer), self.op)
        self.assertTrue(outer.Path.Commands)

    def testLegacyDressupAndOrdinaryGeometryLinksStayDistinct(self):
        from Path.Dressup import Utils
        legacy = self.doc.addObject("Path::FeaturePython", "DressupLegacy")
        legacy.addProperty("App::PropertyLink", "Base")
        legacy.Base = self.op
        self.assertEqual(Utils.baseOp(legacy), self.op)
        ordinary = self.doc.addObject("Path::FeaturePython", "DressupNamedOperation")
        ordinary.addProperty("App::PropertyLinkSubList", "Base")
        ordinary.Base = [(self.source, ["Face1"])]
        self.assertEqual(Utils.baseOp(ordinary), ordinary)
        ordinary.Proxy = self.op.Proxy
        self.assertEqual(Utils.baseOp(ordinary), ordinary)

    def testCustomNamedDressupsRestoreLookup(self):
        import os
        from pathlib import Path
        from Path.Dressup import Array, Utils
        inner = Array.Create(self.op, "RepeatedPath")
        self.doc.recompute()
        names = inner.Name, self.op.Name
        filename = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "DressupLookup.FCStd"
        self.doc.saveAs(str(filename))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(filename))
        restored, operation = [self.doc.getObject(name) for name in names]
        self.doc.recompute()
        self.assertEqual(Utils.baseOp(restored), operation)
        self.assertEqual(Utils.toolController(restored), operation.ToolController)
        self.assertTrue(restored.Path.Commands)

    def testDressupLookupRejectsCyclesAndHandlesDeepChains(self):
        from types import SimpleNamespace
        from Path.Dressup import Utils
        proxy = type("TestDressup", (), {"__module__": "Path.Dressup.TestFixture"})()
        terminal = SimpleNamespace(Name="Operation")
        chain = terminal
        for index in range(1500):
            chain = SimpleNamespace(Name=str(index), Proxy=proxy, Base=chain)
        self.assertIs(Utils.baseOp(chain), terminal)
        first = SimpleNamespace(Name="First", Proxy=proxy)
        second = SimpleNamespace(Name="Second", Proxy=proxy, Base=first)
        first.Base = second
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            Utils.baseOp(first)
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            Utils.toolController(first)

    def testOperationPropertyOverridesDefaultsAndDeepChain(self):
        from types import SimpleNamespace
        from Path.Base import Util
        terminal = SimpleNamespace(ToolController="tool", CoolantMode="Flood", Active=True)
        chain = terminal
        for index in range(1500):
            chain = SimpleNamespace(Base=chain)
        self.assertEqual(Util.toolControllerForOp(chain), "tool")
        self.assertEqual(Util.coolantModeForOp(chain), "Flood")
        override = SimpleNamespace(Base=chain, Active=False, ToolController=None)
        self.assertFalse(Util.activeForOp(override))
        self.assertIsNone(Util.toolControllerForOp(override))
        self.assertEqual(Util.coolantModeForOp(SimpleNamespace(Base=None)), "None")
        self.assertTrue(Util.activeForOp(SimpleNamespace(Base=[])))
        first = SimpleNamespace()
        second = SimpleNamespace(Base=first)
        first.Base = second
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            Util.toolControllerForOp(first)

    def testJobTraversalSharedNativeBasesKeepOrder(self):
        from Path.Dressup import Array
        first = Array.Create(self.op, "RepeatedFirst")
        second = Array.Create(self.op, "RepeatedSecond")
        self.job.Operations.Group = [first, second]
        self.doc.recompute()
        self.assertEqual(self.job.Proxy.allOperations(), [first, self.op, second])
        previous = self.job.Model
        self.job.Model = None
        self.assertTrue(all(not op.Path.Commands for op in (first, self.op, second)))
        self.job.Model = previous
        self.doc.recompute()
        self.assertTrue(all(op.Path.Commands for op in (first, self.op, second)))

    def testJobTraversalDeepSharedAndCyclicGraph(self):
        from types import SimpleNamespace
        from Path.Main.Job import ObjectJob
        terminal = SimpleNamespace(TypeId="Path::FeaturePython", Base=[])
        chain = terminal
        for index in range(1500):
            chain = SimpleNamespace(TypeId="Path::FeaturePython", Base=chain)
        group = SimpleNamespace(TypeId="Path::FeatureCompoundPython", Group=[])
        group.Group = [chain, terminal, group]
        job = SimpleNamespace(obj=SimpleNamespace(Operations=SimpleNamespace(Group=[group, chain])))
        operations = ObjectJob.allOperations(job)
        self.assertEqual(len(operations), 1502)
        self.assertIs(operations[0], group)
        self.assertIs(operations[1], chain)
        self.assertIs(operations[-1], terminal)
        self.assertEqual(len({id(op) for op in operations}), len(operations))
        self.assertEqual(ObjectJob.allOperations(SimpleNamespace(obj=SimpleNamespace())), [])
