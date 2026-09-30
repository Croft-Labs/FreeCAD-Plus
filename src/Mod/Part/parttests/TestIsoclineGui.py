# SPDX-License-Identifier: LGPL-2.1-or-later

import math
import tempfile
import unittest
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui


class TestIsoclineGui(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("IsoclineGuiTest")
        self.doc.UndoMode = 1
        self.source = self.doc.addObject("Part::Sphere", "Source")
        self.source.Radius = 10
        self.doc.recompute()
        Gui.activateWorkbench("PartDesignWorkbench")
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)

    def start(self, preselect=True):
        if preselect:
            Gui.Selection.addSelection(self.source, "Face1")
        Gui.runCommand("Part_IsoclineCurve")
        Gui.updateGui()
        self.obj = self.doc.getObject("IsoclineCurve")
        self.assertTrue(Gui.Control.activeDialog())
        self.task = self.obj.ViewObject.Proxy.task

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertFalse(Gui.Control.activeDialog())

    def reopen(self):
        self.assertTrue(self.obj.ViewObject.doubleClicked())
        Gui.updateGui()
        self.task = self.obj.ViewObject.Proxy.task

    def selectionPaths(self):
        return [(s.DocumentName, s.ObjectName, tuple(s.SubElementNames))
                for s in Gui.Selection.getSelectionEx("*", 0)]

    def testCollectorEntryCountsAndActiveRoleFollowEdits(self):
        self.start(False)
        self.assertIn("Selected entries: 0", self.task.facesHint.text())
        self.assertIn("whole objects (all faces)", self.task.facesHint.text())
        self.assertEqual(self.task.activeCollector.text(), "Picking: Target faces")
        Gui.Selection.addSelection(self.source, "Face1")
        self.assertIn("Selected entries: 1", self.task.facesHint.text())
        Gui.Selection.addSelection(self.source, "Face1")
        self.assertIn("Selected entries: 1", self.task.facesHint.text())
        self.task.clearFaces()
        self.assertIn("Selected entries: 0", self.task.facesHint.text())
        Gui.Selection.addSelection(self.source)
        self.assertIn("Selected entries: 1", self.task.facesHint.text(), self.task.status.text())
        self.assertIn("all faces", self.task.faces.item(0).text())
        self.task.direction.setCurrentIndex(3)
        self.assertEqual(self.task.activeCollector.text(), "Picking: Direction reference")
        self.assertIn("0/1", self.task.referenceHint.text())
        self.task.direction.setCurrentIndex(2)
        self.assertEqual(self.task.activeCollector.text(), "Picking: none")
        self.accept()
        self.reopen()
        self.assertIn("Selected entries: 1", self.task.facesHint.text())

    def testMixedFaceEdgePreselectionReportsIgnoredEdgeAndMatchesLaterPicks(self):
        Gui.Selection.addSelection(self.source, "Face1")
        Gui.Selection.addSelection(self.source, "Edge1")
        self.start(False)
        definition = (self.obj.Faces, self.obj.Shape.Length)
        self.assertEqual(self.task.faces.count(), 1)
        self.assertIn("Edge1", self.task.preselectionFeedback.text())
        self.assertIn("Select faces", self.task.preselectionFeedback.text())
        self.assertNotIn("Face1", self.task.preselectionFeedback.text())
        self.assertFalse(self.task.preselectionFeedback.isHidden())
        Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        self.start(False)
        Gui.Selection.addSelection(self.source, "Face1")
        Gui.Selection.addSelection(self.source, "Edge1")
        self.assertEqual((self.obj.Faces, self.obj.Shape.Length), definition)
        self.assertIn("Select faces", self.task.status.text())
        self.assertEqual(self.task.activeCollector.text(), "Picking: Target faces")
        self.accept()

    def testInvalidWholeObjectPreselectionExplainsRecovery(self):
        wire = self.doc.addObject("Part::Feature", "Wire")
        wire.Shape = Part.makeLine(App.Vector(), App.Vector(0, 0, 10))
        self.doc.recompute()
        Gui.Selection.addSelection(wire)
        self.start(False)
        self.assertEqual(self.task.faces.count(), 0)
        self.assertIn("Wire", self.task.preselectionFeedback.text())
        self.assertIn("Select faces", self.task.preselectionFeedback.text())
        self.assertEqual(self.task.mode, "Faces")
        Gui.Selection.addSelection(self.source, "Face1")
        self.accept()
        self.reopen()
        self.assertTrue(self.task.preselectionFeedback.isHidden())
        self.assertEqual(self.task.faces.count(), 1)

    def testMultiplePreselectedFacesFromOneObjectMatchInteractiveGeometry(self):
        compound = self.doc.addObject("Part::Feature", "TwoSpheres")
        compound.Shape = Part.makeCompound([
            Part.makeSphere(10), Part.makeSphere(10, App.Vector(30, 0, 0))])
        self.doc.recompute()
        Gui.Selection.addSelection(compound, "Face1")
        Gui.Selection.addSelection(compound, "Face2")
        self.start(False)
        self.assertEqual(self.task.faces.count(), 2)
        self.assertIn("Selected entries: 2", self.task.facesHint.text())
        self.assertTrue(self.task.preselectionFeedback.isHidden())
        self.assertAlmostEqual(self.obj.Shape.Length, 40 * math.pi)
        definition = self.obj.Faces
        Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        self.start(False)
        Gui.Selection.addSelection(compound, "Face1")
        Gui.Selection.addSelection(compound, "Face2")
        self.assertEqual(self.obj.Faces, definition)
        self.assertAlmostEqual(self.obj.Shape.Length, 40 * math.pi)
        self.accept()

    def testWholeObjectSurvivesRowRemovalUndoAndSaveReopen(self):
        second = self.doc.addObject("Part::Sphere", "Second")
        second.Radius = 10
        second.Placement.Base.x = 30
        self.doc.recompute()
        Gui.Selection.addSelection(self.source)
        self.start(False)
        self.assertEqual(self.task.entries(), [(self.source, "")])
        self.assertTrue(self.task.preselectionFeedback.isHidden())
        self.task.select("Faces")
        Gui.Selection.addSelection(second, "Face1")
        self.accept()
        self.assertAlmostEqual(self.obj.Shape.Length, 40 * math.pi)
        self.reopen()
        self.task.faces.item(1).setSelected(True)
        self.task.removeFaces()
        self.assertEqual(self.task.entries(), [(self.source, "")])
        self.accept()
        self.assertAlmostEqual(self.obj.Shape.Length, 20 * math.pi)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.obj.Shape.Length, 40 * math.pi)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(self.obj.Shape.Length, 20 * math.pi)
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "WholeObject.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.obj = self.doc.getObject("IsoclineCurve")
            self.source = self.doc.getObject("Source")
            self.source.Radius = 12
            self.doc.recompute()
            self.assertAlmostEqual(self.obj.Shape.Length, 24 * math.pi)
            self.reopen()
            self.assertEqual(self.task.entries(), [(self.source, "")])
            self.assertIn("Selected entries: 1", self.task.facesHint.text())
            self.accept()

    def testCancelRestoresOccurrenceSelectionForCreationAndEdit(self):
        occurrence = self.doc.addObject("App::Link", "Occurrence")
        occurrence.setLink(self.source)
        self.doc.recompute()
        Gui.Selection.addSelection(occurrence, "Face1")
        original = self.selectionPaths()
        self.start(False)
        Gui.Control.activeTaskDialog().reject()
        self.assertIsNone(self.doc.getObject("IsoclineCurve"))
        self.assertEqual(self.selectionPaths(), original)
        Gui.Selection.clearSelection()
        self.start()
        self.accept()
        Gui.Selection.addSelection(occurrence, "Face1")
        original = self.selectionPaths()
        self.reopen()
        self.task.clearFaces()
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual(self.selectionPaths(), original)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testFailedStartupRestoresPreselection(self):
        from unittest.mock import patch, Mock
        import BasicShapes.IsoclineGui as module
        Gui.Selection.addSelection(self.source, "Face1")
        original = self.selectionPaths()
        with patch.object(module.Gui, "getDocument", return_value=Mock(setEdit=Mock(return_value=False))):
            with self.assertRaisesRegex(RuntimeError, "Could not open"):
                module.CommandIsocline().Activated()
        self.assertEqual(self.selectionPaths(), original)
        self.assertIsNone(self.doc.getObject("IsoclineCurve"))
        self.assertFalse(self.doc.HasPendingTransaction)

    def testInspectFacesAndReferenceDoesNotFillAnotherRole(self):
        self.start()
        self.task.direction.setCurrentIndex(3)
        self.assertEqual(self.task.mode, "Reference")
        self.task.faces.item(0).setSelected(True)
        self.assertEqual(self.selectionPaths(), [(self.doc.Name, self.source.Name, ("Face1",))])
        self.assertFalse(self.obj.DirectionReference)
        self.assertEqual(self.task.mode, "Reference")
        axis = self.doc.addObject("Part::Feature", "Axis")
        axis.Shape = Part.makeLine(App.Vector(0, 0, 0), App.Vector(0, 0, 10))
        axis.Visibility = False
        self.doc.recompute()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(axis, "Edge1")
        self.task.select("Faces")
        original = self.obj.Faces
        self.task.highlightRef.click()
        self.assertEqual(self.selectionPaths(), [(self.doc.Name, axis.Name, ("Edge1",))])
        self.assertEqual(self.obj.Faces, original)
        self.assertEqual(self.task.mode, "Faces")
        self.assertTrue(axis.Visibility)
        self.assertTrue(self.task.accept())
        self.assertFalse(axis.Visibility)

    def testClearDirectionReferenceRejectsAcceptAndCanBeReplaced(self):
        axis = self.doc.addObject("Part::Feature", "Axis")
        axis.Shape = Part.makeLine(App.Vector(0, 0, 0), App.Vector(0, 0, 10))
        self.doc.recompute()
        self.start()
        self.task.direction.setCurrentIndex(3)
        Gui.Selection.addSelection(axis, "Edge1")
        self.assertIn("1/1", self.task.referenceHint.text())
        self.accept()
        self.reopen()
        self.task.preview.setChecked(False)
        self.task.clearRef.click()
        self.assertFalse(self.obj.DirectionReference)
        self.assertIn("0/1", self.task.referenceHint.text())
        self.assertEqual(self.obj.DirectionMode, "Reference")
        self.assertEqual(self.task.mode, "Reference")
        self.assertFalse(self.obj.Visibility)
        self.assertFalse(self.task.highlightRef.isEnabled())
        self.assertFalse(self.task.clearRef.isEnabled())
        self.assertFalse(self.task.accept())
        self.assertTrue(Gui.Control.activeDialog())
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual(self.obj.DirectionReference[0], axis)
        self.assertTrue(self.obj.isValid())
        self.reopen()
        self.task.clearRef.click()
        Gui.Selection.addSelection(axis, "Edge1")
        self.assertTrue(self.task.clearRef.isEnabled())
        self.accept()
        self.assertTrue(self.obj.isValid())

    def testUnrelatedTransactionIsPreservedByEditAndCreate(self):
        import BasicShapes.IsoclineGui as module
        self.start()
        self.accept()
        before = {obj.Name for obj in self.doc.Objects}
        original = self.obj.Label
        self.doc.openTransaction("Unrelated user edit")
        self.obj.Label = "Pending caller label"
        with self.assertRaisesRegex(RuntimeError, "current transaction"):
            self.obj.ViewObject.Proxy.setEdit(self.obj.ViewObject)
        with self.assertRaisesRegex(RuntimeError, "current transaction"):
            module.CommandIsocline().Activated()
        self.assertTrue(self.doc.HasPendingTransaction)
        self.assertEqual(self.obj.Label, "Pending caller label")
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)
        self.assertIsNone(self.obj.ViewObject.Proxy.task)
        self.assertFalse(Gui.Control.activeDialog())
        self.doc.abortTransaction()
        self.doc.recompute()
        self.assertEqual(self.obj.Label, original)
        self.reopen()
        self.accept()

    def testSecondaryCleanupFailurePreservesPrimaryErrorAndContinues(self):
        from unittest.mock import patch, Mock
        from BasicShapes import FeatureTask
        import BasicShapes.IsoclineGui as module
        self.start()
        self.accept()
        provider = self.obj.ViewObject.Proxy
        scene = Gui.activeDocument().activeView().getSceneGraph()
        children = scene.getNumChildren()
        visible = self.obj.Visibility
        close = FeatureTask.DirectionArrow.close
        def close_then_fail(annotation):
            close(annotation)
            close(annotation)  # Repeated removal must be harmless.
            raise RuntimeError("Secondary cleanup failure")
        failures = (
            patch.object(module.IsoclineTask, "updatePreview", side_effect=RuntimeError("Primary task failure")),
            patch.object(module.Gui, "Control", Mock(wraps=Gui.Control,
                         showDialog=Mock(side_effect=RuntimeError("Primary task failure")))),
        )
        for failure in failures:
            with failure, patch.object(FeatureTask.DirectionArrow, "close", close_then_fail):
                with self.assertRaisesRegex(RuntimeError, "Primary task failure"):
                    provider.setEdit(self.obj.ViewObject)
            self.assertEqual(scene.getNumChildren(), children)
            self.assertEqual(self.obj.Visibility, visible)
            self.assertFalse(self.doc.HasPendingTransaction)
            self.assertFalse(Gui.Control.activeDialog())
            self.assertIsNone(provider.task)
        self.reopen()
        self.accept()

    def testTaskConstructionAndDisplayFailureCleanUpForRetry(self):
        from unittest.mock import patch, Mock
        import BasicShapes.IsoclineGui as module
        self.start()
        self.accept()
        provider = self.obj.ViewObject.Proxy
        scene = Gui.activeDocument().activeView().getSceneGraph()
        children = scene.getNumChildren()
        visible = self.obj.Visibility
        failures = (
            patch.object(module.IsoclineTask, "updatePreview", side_effect=RuntimeError("Injected task failure")),
            patch.object(module.Gui, "Control", Mock(wraps=Gui.Control,
                         showDialog=Mock(side_effect=RuntimeError("Injected task failure")))),
        )
        for failure in failures:
            with failure:
                with self.assertRaisesRegex(RuntimeError, "Injected task failure"):
                    provider.setEdit(self.obj.ViewObject)
            self.assertIsNone(provider.task)
            self.assertFalse(self.doc.HasPendingTransaction)
            self.assertFalse(Gui.Control.activeDialog())
            self.assertEqual(scene.getNumChildren(), children)
            self.assertEqual(self.obj.Visibility, visible)
        self.reopen()
        self.accept()

    def testFailedStartupRollsBackAndAllowsRetry(self):
        from unittest.mock import patch, Mock
        import BasicShapes.IsoclineGui as module
        before = {obj.Name for obj in self.doc.Objects}
        factory = module.Isocline.makeIsocline
        def fail_after_creation(doc):
            factory(doc)
            raise RuntimeError("Injected factory failure")
        with patch.object(module.Isocline, "makeIsocline", side_effect=fail_after_creation):
            with self.assertRaisesRegex(RuntimeError, "Injected factory"):
                module.CommandIsocline().Activated()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)
        self.assertFalse(self.doc.HasPendingTransaction)
        with patch.object(module.Gui, "getDocument", return_value=Mock(setEdit=Mock(return_value=False))):
            with self.assertRaisesRegex(RuntimeError, "Could not open"):
                module.CommandIsocline().Activated()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertFalse(Gui.Control.activeDialog())
        self.start()
        self.accept()

    def testNoPreselectionFaceListAndCancel(self):
        self.start(False)
        self.assertEqual(
            self.task.form.layout().itemAt(0).widget().objectName(), "isoclineFacesGroup"
        )
        self.assertEqual(self.task.mode, "Faces")
        self.assertEqual(self.task.angle.value(), 0)
        self.assertEqual(self.task.angle.suffix(), " \u00b0")
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        Gui.Selection.addSelection(self.source, "Face1")
        Gui.Selection.addSelection(self.source, "Face1")
        self.assertEqual(self.task.faces.count(), 1)
        self.assertAlmostEqual(self.obj.Shape.Length, 20 * math.pi)
        self.assertTrue(self.source.Visibility)
        arrow = self.task.arrow
        highlight = self.task.curveHighlight
        self.assertGreater(highlight.root.getNumChildren(), 1)
        self.assertGreater(arrow.root.getNumChildren(), 1)
        Gui.Control.activeTaskDialog().reject()
        self.assertIsNone(self.doc.getObject("IsoclineCurve"))
        self.assertEqual(arrow.scene.findChild(arrow.root), -1)
        self.assertEqual(highlight.scene.findChild(highlight.root), -1)
        self.assertTrue(self.source.Visibility)

    def testFailedSourceBlocksPreviewAndAcceptUntilRepaired(self):
        self.start()
        self.assertFalse(self.obj.Shape.isNull())
        self.source.Radius = 0
        self.assertFalse(self.task.updatePreview(force=True))
        self.assertIn("not current", self.task.status.text())
        self.assertFalse(self.obj.Visibility)
        self.assertFalse(self.task.accept())
        self.assertTrue(Gui.Control.activeDialog())
        self.source.Radius = 10
        self.assertTrue(self.task.updatePreview(force=True))
        self.assertAlmostEqual(self.obj.Shape.Length, 20 * math.pi)
        self.accept()

    def testFailedReplacementPreservesFacesAndDirectionReference(self):
        self.start()
        candidate = self.doc.addObject("Part::Box", "FailedCandidate")
        self.doc.recompute()
        candidate.Length = 0
        self.doc.recompute()
        self.assertIn("Invalid", candidate.State)
        faces, reference = self.obj.Faces, self.obj.DirectionReference
        for mode in ("Faces", "Reference"):
            self.task.select(mode)
            self.task.addSelection(self.doc.Name, candidate.Name, "Face1", None)
            self.assertIn("not current", self.task.status.text())
            self.assertEqual(self.obj.Faces, faces)
            self.assertEqual(self.obj.DirectionReference, reference)
            self.assertEqual(self.task.mode, mode)
        candidate.Length = 10
        self.doc.recompute()
        self.task.select("Reference")
        self.task.addSelection(self.doc.Name, candidate.Name, "Face1", None)
        self.assertEqual(self.obj.DirectionReference[0], candidate)
        self.assertEqual(self.obj.Faces, faces)
        self.accept()

    def testMixedPreselectionSkipsFailedFacesAndRetainsValidFaces(self):
        valid = self.doc.addObject("Part::Sphere", "ValidSource")
        valid.Radius = 10
        valid.Placement.Base.x = 30
        self.doc.recompute()
        self.source.Radius = 0
        self.doc.recompute()
        self.assertIn("Invalid", self.source.State)
        Gui.Selection.addSelection(self.source, "Face1")
        Gui.Selection.addSelection(valid, "Face1")
        self.start(False)
        self.assertEqual([obj for obj, names in self.obj.Faces], [valid])
        self.assertIn("not current", self.task.preselectionFeedback.text())
        self.assertIn(self.source.Label, self.task.preselectionFeedback.text())
        self.assertAlmostEqual(self.obj.Shape.Length, 20 * math.pi)
        self.source.Radius = 10
        self.doc.recompute()
        self.task.select("Faces")
        self.task.addSelection(self.doc.Name, self.source.Name, "Face1", None)
        self.assertEqual({obj.Name for obj, names in self.obj.Faces},
                         {valid.Name, self.source.Name})
        self.assertAlmostEqual(self.obj.Shape.Length, 40 * math.pi)
        self.accept()

    def testAngleReverseEditUndoAndCancel(self):
        self.start()
        self.task.angle.setValue(30)
        self.assertAlmostEqual(self.obj.Shape.optimalBoundingBox(False).Center.z, 5)
        self.task.reverse.click()
        self.assertAlmostEqual(self.obj.Shape.optimalBoundingBox(False).Center.z, -5)
        self.accept()
        self.reopen()
        self.assertEqual(self.task.angle.value(), 30)
        self.task.angle.setValue(60)
        Gui.Control.activeTaskDialog().reject()
        self.assertAlmostEqual(self.obj.Shape.optimalBoundingBox(False).Center.z, -5)
        self.reopen()
        self.task.reverse.click()
        self.accept()
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.obj.Shape.optimalBoundingBox(False).Center.z, -5)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(self.obj.Shape.optimalBoundingBox(False).Center.z, 5)

    def testDirectionPlaneEdgeAndCustomVector(self):
        import PartDesign

        plane = self.doc.addObject("PartDesign::Plane", "Plane")
        plane.Placement.Rotation = App.Rotation(App.Vector(0, 1, 0), 90)
        self.doc.recompute()
        self.start()
        self.task.angle.setValue(30)
        self.task.direction.setCurrentIndex(3)
        self.assertEqual(self.task.mode, "Reference")
        Gui.Selection.addSelection(plane)
        self.assertAlmostEqual(self.obj.Shape.optimalBoundingBox(False).Center.x, 5)
        self.task.direction.setCurrentIndex(4)
        for field, value in zip(self.task.components, (0, 1, 0)):
            field.setValue(value)
        self.assertAlmostEqual(self.obj.Shape.optimalBoundingBox(False).Center.y, 5)
        self.accept()

    def testMultipleFacesRemoveClearAndInvalidPicks(self):
        second = self.doc.addObject("Part::Sphere", "Second")
        second.Radius = 10
        second.Placement.Base.x = 30
        self.doc.recompute()
        self.start(False)
        Gui.Selection.addSelection(self.source, "Face1")
        Gui.Selection.addSelection(second, "Face1")
        self.assertEqual(self.task.faces.count(), 2)
        self.assertEqual(len(self.obj.Shape.Wires), 2)
        self.task.faces.item(1).setSelected(True)
        self.task.removeFaces()
        self.assertEqual(self.task.faces.count(), 1)
        Gui.Selection.addSelection(self.source, "Edge1")
        self.assertEqual(self.task.faces.count(), 1)
        Gui.Selection.addSelection(self.obj)
        self.assertEqual(self.task.faces.count(), 1)
        self.task.clearFaces()
        self.assertTrue(self.obj.Shape.isNull())
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        Gui.Selection.addSelection(self.source, "Face1")
        self.accept()

    def testEmptyAngleRejectAndPausedPreview(self):
        self.start()
        self.task.angle.setValue(90)
        self.assertTrue(self.obj.Shape.isNull())
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.task.preview.setChecked(False)
        self.task.angle.setValue(30)
        self.assertFalse(self.obj.Visibility)
        self.accept()
        self.assertAlmostEqual(self.obj.Shape.optimalBoundingBox(False).Center.z, 5)

    def testSavedFeatureReopensSamePane(self):
        self.start()
        self.task.angle.setValue(30)
        self.accept()
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "IsoclineGui.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.obj = self.doc.getObject("IsoclineCurve")
            self.reopen()
            self.assertEqual(self.task.faces.count(), 1)
            self.assertEqual(self.task.angle.value(), 30)
            self.task.angle.setValue(15)
            self.accept()
            self.assertAlmostEqual(
                self.obj.Shape.optimalBoundingBox(False).Center.z, 10 * math.sin(math.radians(15))
            )

    def testToolbarInBothWorkbenches(self):
        for workbench, toolbar in (
            ("PartWorkbench", "Part Tools"),
            ("PartDesignWorkbench", "Part Design Modeling Features"),
        ):
            Gui.activateWorkbench(workbench)
            Gui.updateGui()
            bar = Gui.getMainWindow().findChild(QtGui.QToolBar, toolbar)
            self.assertIsNotNone(bar)
            self.assertTrue(bar.toggleViewAction().isVisible())
            actions = [a for a in bar.actions() if a.objectName() == "Part_IsoclineCurve"]
            self.assertEqual(len(actions), 1)
            Gui.Selection.addSelection(self.source, "Face1")
            # MainWindow refreshes command enablement on a 150 ms timer.
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(350, loop.quit)
            loop.exec()
            self.assertTrue(actions[0].isEnabled(), workbench)
            actions[0].trigger()
            Gui.updateGui()
            self.assertTrue(Gui.Control.activeDialog())
            self.assertAlmostEqual(self.doc.getObject("IsoclineCurve").Shape.Length, 20 * math.pi)
            Gui.Control.activeTaskDialog().reject()
