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
