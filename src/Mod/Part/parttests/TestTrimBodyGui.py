# SPDX-License-Identifier: LGPL-2.1-or-later

import math
import tempfile
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui


class TestTrimBodyGui(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("TrimBodyGuiTest")
        self.doc.UndoMode = 1
        self.target = self.doc.addObject("Part::Box", "Target")
        self.target.Length = self.target.Width = self.target.Height = 10
        self.tool = self.doc.addObject("Part::Feature", "Tool")
        self.tool.Shape = Part.makePlane(2, 2, App.Vector(4, 4, 4))
        self.doc.recompute()
        Gui.activateWorkbench("PartDesignWorkbench")
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)

    def start(self, preselect=False):
        if preselect:
            Gui.Selection.addSelection(self.target)
            Gui.Selection.addSelection(self.tool)
        Gui.runCommand("Part_TrimBody")
        Gui.updateGui()
        self.assertTrue(Gui.Control.activeDialog())
        self.obj = self.doc.getObject("TrimBody")
        self.assertIsNotNone(self.obj)
        self.task = self.obj.ViewObject.Proxy.task
        return self.obj

    def pick(self):
        Gui.Selection.addSelection(self.target)
        Gui.Selection.addSelection(self.tool)
        Gui.updateGui()

    def widget(self, cls, name):
        widget = self.task.form.findChild(cls, name)
        self.assertIsNotNone(widget, name)
        return widget

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertFalse(Gui.Control.activeDialog())

    def reopen(self):
        self.assertTrue(self.obj.ViewObject.doubleClicked())
        Gui.updateGui()
        self.task = self.obj.ViewObject.Proxy.task

    def testFailedStartupRollsBackAndAllowsRetry(self):
        from unittest.mock import patch, Mock
        import BOPTools.TrimGui as module
        before = {obj.Name for obj in self.doc.Objects}
        factory = module.TrimFeatures.makeTrimBody
        def fail_after_creation(doc):
            factory(doc)
            raise RuntimeError("Injected factory failure")
        with patch.object(module.TrimFeatures, "makeTrimBody", side_effect=fail_after_creation):
            with self.assertRaisesRegex(RuntimeError, "Injected factory"):
                module.CommandTrimBody().Activated()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)
        self.assertFalse(self.doc.HasPendingTransaction)
        with patch.object(module.Gui, "getDocument", return_value=Mock(setEdit=Mock(return_value=False))):
            with self.assertRaisesRegex(RuntimeError, "Could not open"):
                module.CommandTrimBody().Activated()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertFalse(Gui.Control.activeDialog())
        self.start(preselect=True)
        self.accept()

    def testCreateWithoutPreselectionAndArrowCleanup(self):
        self.start()
        self.assertEqual(self.task.mode, "Target")
        self.assertEqual(self.task.form.layout().itemAt(0).widget().objectName(), "trimTargetGroup")
        self.assertEqual(self.task.form.layout().itemAt(1).widget().objectName(), "trimToolGroup")
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.pick()
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.assertFalse(self.target.Visibility)
        self.assertTrue(self.obj.Visibility)
        arrow = self.task.arrow
        self.assertGreaterEqual(arrow.scene.findChild(arrow.root), 0)
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual(arrow.scene.findChild(arrow.root), -1)
        self.assertIsNone(self.doc.getObject("TrimBody"))
        self.assertTrue(self.target.Visibility)
        self.assertTrue(self.tool.Visibility)

    def testFailedSourceBlocksPreviewAndAcceptUntilRepaired(self):
        self.start(preselect=True)
        self.assertFalse(self.obj.Shape.isNull())
        self.target.Length = 0
        self.assertFalse(self.task.updatePreview(force=True))
        self.assertIn("not current", self.task.status.text())
        self.assertFalse(self.obj.Visibility)
        self.assertFalse(self.task.accept())
        self.assertTrue(Gui.Control.activeDialog())
        self.target.Length = 10
        self.assertTrue(self.task.updatePreview(force=True))
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.accept()

    def testFailedReplacementPreservesTargetAndTool(self):
        self.start(preselect=True)
        candidate = self.doc.addObject("Part::Box", "FailedCandidate")
        candidate.Length = candidate.Width = candidate.Height = 10
        self.doc.recompute()
        candidate.Length = 0
        self.doc.recompute()
        self.assertIn("Invalid", candidate.State)
        target, tool = self.obj.Target, self.obj.Tool
        for mode, sub in (("Target", ""), ("Tool", "Face1")):
            self.task.select(mode)
            self.task.addSelection(self.doc.Name, candidate.Name, sub, None)
            self.assertIn("not current", self.task.status.text())
            self.assertEqual(self.obj.Target, target)
            self.assertEqual(self.obj.Tool, tool)
            self.assertEqual(self.task.mode, mode)
        candidate.Length = 10
        self.doc.recompute()
        self.task.select("Target")
        self.task.addSelection(self.doc.Name, candidate.Name, "", None)
        self.assertEqual(self.obj.Target[0], candidate)
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.accept()

    def testFailedPreselectedTargetIsSkippedAndCanBeRepaired(self):
        self.target.Length = 0
        self.doc.recompute()
        self.assertIn("Invalid", self.target.State)
        self.start(preselect=True)
        self.assertFalse(self.obj.Target)
        self.assertEqual(self.obj.Tool[0], self.tool)
        self.assertTrue(Gui.Control.activeDialog())
        self.target.Length = 10
        self.doc.recompute()
        self.task.select("Target")
        self.task.addSelection(self.doc.Name, self.target.Name, "", None)
        self.assertEqual(self.obj.Target[0], self.target)
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.accept()

    def testReverseEditCancelUndoRedo(self):
        self.start(preselect=True)
        self.accept()
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.reopen()
        self.widget(QtGui.QToolButton, "trimReverse").click()
        self.assertAlmostEqual(self.obj.Shape.Volume, 400)
        self.assertLess(self.obj.Direction.z, 0)
        self.accept()
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(self.obj.Shape.Volume, 400)
        self.reopen()
        self.widget(QtGui.QPushButton, "trimClearTool").click()
        self.assertTrue(self.obj.Shape.isNull())
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        Gui.Selection.addSelection(self.tool)
        self.assertAlmostEqual(self.obj.Shape.Volume, 400)
        self.widget(QtGui.QToolButton, "trimReverse").click()
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertAlmostEqual(self.obj.Shape.Volume, 400)
        self.assertTrue(self.obj.Visibility)
        self.assertFalse(self.target.Visibility)
        self.assertFalse(self.tool.Visibility)

    def testInvalidToolCannotBeAcceptedAndRecovers(self):
        self.tool.Placement.Base.z = 20
        self.doc.recompute()
        self.start(preselect=True)
        self.assertTrue(self.obj.Shape.isNull())
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.tool.Placement.Base.z = 0
        self.task.updatePreview()
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.accept()

    def testPausedPreviewRecomputesOnAccept(self):
        self.start(preselect=True)
        self.widget(QtGui.QCheckBox, "trimPreview").setChecked(False)
        self.widget(QtGui.QToolButton, "trimReverse").click()
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.accept()
        self.assertAlmostEqual(self.obj.Shape.Volume, 400)

    def testFacePreselectionFromSolidTool(self):
        self.tool.Shape = Part.makeBox(2, 2, 2, App.Vector(4, 4, 2))
        self.doc.recompute()
        top = max(
            range(len(self.tool.Shape.Faces)), key=lambda i: self.tool.Shape.Faces[i].CenterOfMass.z
        )
        Gui.Selection.addSelection(self.target)
        Gui.Selection.addSelection(self.tool, "Face%d" % (top + 1))
        self.start()
        self.assertEqual(self.obj.Tool[1], ["Face%d" % (top + 1)])
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)
        self.accept()

    def testRejectSelfDependentAndEdgeSelections(self):
        self.start()
        Gui.Selection.addSelection(self.obj)
        self.assertIsNone(self.obj.Target)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.target)
        Gui.Selection.addSelection(self.tool, "Edge1")
        self.assertIsNone(self.obj.Tool)
        dependent = self.doc.addObject("Part::Feature", "Dependent")
        dependent.addProperty("App::PropertyLink", "Source")
        dependent.Source = self.obj
        dependent.Shape = Part.makePlane(20, 20, App.Vector(-5, -5, 5))
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(dependent)
        self.assertIsNone(self.obj.Tool)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.tool)
        self.assertAlmostEqual(self.obj.Shape.Volume, 600)

    def testCurvedFaceAndReverse(self):
        self.target.Height = 2
        self.target.Placement.Base = App.Vector(-5, -5, 0)
        self.tool.Shape = Part.makeCylinder(4, 6, App.Vector(0, 0, -2))
        self.doc.recompute()
        face = next(
            i
            for i, face in enumerate(self.tool.Shape.Faces)
            if isinstance(face.Surface, Part.Cylinder)
        )
        self.start()
        Gui.Selection.addSelection(self.target)
        Gui.Selection.addSelection(self.tool, "Face%d" % (face + 1))
        self.assertAlmostEqual(self.obj.Shape.Volume, 200 - 32 * math.pi, places=6)
        self.widget(QtGui.QToolButton, "trimReverse").click()
        self.assertAlmostEqual(self.obj.Shape.Volume, 32 * math.pi, places=6)
        self.accept()

    def testSheetTargetAndDatumPlane(self):
        import PartDesign

        self.doc.removeObject(self.target.Name)
        self.target = self.doc.addObject("Part::Feature", "SheetTarget")
        self.target.Shape = Part.makePlane(10, 10)
        self.doc.removeObject(self.tool.Name)
        self.tool = self.doc.addObject("PartDesign::Plane", "CutPlane")
        self.tool.Placement = App.Placement(
            App.Vector(3, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)
        )
        self.doc.recompute()
        self.start(preselect=True)
        self.assertAlmostEqual(self.obj.Shape.Area, 70)
        self.widget(QtGui.QToolButton, "trimReverse").click()
        self.assertAlmostEqual(self.obj.Shape.Area, 30)
        self.accept()

    def testSavedFeatureReopensInSameTask(self):
        self.start(preselect=True)
        self.accept()
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "TrimGui.FCStd")
            name = self.obj.Name
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.obj = self.doc.getObject(name)
            self.reopen()
            self.assertEqual(self.widget(QtGui.QLineEdit, "trimTarget").text(), "Target")
            self.assertAlmostEqual(self.obj.Shape.Volume, 600)
            self.widget(QtGui.QToolButton, "trimReverse").click()
            self.assertAlmostEqual(self.obj.Shape.Volume, 400)
            self.accept()

    def testCommandAvailableInBothWorkbenches(self):
        for workbench, toolbar in (
            ("PartWorkbench", "Boolean Tools"),
            ("PartDesignWorkbench", "Part Design Modeling Features"),
        ):
            Gui.activateWorkbench(workbench)
            Gui.updateGui()
            self.assertIn("Part_TrimBody", Gui.listCommands())
            bar = Gui.getMainWindow().findChild(QtGui.QToolBar, toolbar)
            self.assertIsNotNone(bar, workbench)
            # Users may hide toolbars; command availability must preserve that preference.
            self.assertTrue(bar.toggleViewAction().isVisible(), workbench)
            actions = [action for action in bar.actions() if action.objectName() == "Part_TrimBody"]
            self.assertEqual(len(actions), 1, workbench)
            Gui.Selection.addSelection(self.target)
            Gui.Selection.addSelection(self.tool)
            # MainWindow refreshes command enablement on a 150 ms timer.
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(350, loop.quit)
            loop.exec()
            self.assertTrue(actions[0].isEnabled(), workbench)
            actions[0].trigger()
            Gui.updateGui()
            self.assertTrue(Gui.Control.activeDialog())
            self.assertAlmostEqual(self.doc.getObject("TrimBody").Shape.Volume, 600)
            Gui.Control.activeTaskDialog().reject()
