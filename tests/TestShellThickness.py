# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native shell task: face collection, signed thickness and recoverable edits."""
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets


def settle():
    Gui.updateGui()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(150, loop.quit)
    loop.exec_()
    QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)


class TestShellThickness(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("ShellThickness")
        self.doc.UndoMode = 1
        self.source = self.doc.addObject("Part::Box", "Enclosure")
        self.source.Length, self.source.Width, self.source.Height = 30, 20, 15
        self.doc.recompute()
        self.original = self.source.Shape.exportBrepToString()

    def tearDown(self):
        if Gui.Control.activeTaskDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()

    def launch(self, result=None):
        if result is None:
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(self.source, "Face6")
            Gui.runCommand("Part_Thickness")
        else:
            result.ViewObject.doubleClicked()
        settle()
        self.result = self.doc.Thickness
        self.panel = next(p for p in Gui.Control.activeTaskDialog().getDialogContent()
                          if p.findChild(QtWidgets.QLabel, "resultStatus"))

    def control(self, name, cls=QtWidgets.QWidget):
        return self.panel.findChild(cls, name)

    def value(self, value):
        self.control("spinOffset").setProperty("rawValue", value)
        settle()

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        settle()

    def testSignedSideSourceIsolationAndRecovery(self):
        self.launch()
        self.assertIn("Enclosure", self.control("labelFaces", QtWidgets.QLabel).text())
        self.assertIn("Face6", self.control("labelFaces", QtWidgets.QLabel).text())
        self.assertIn("Positive", self.control("sideHelp", QtWidgets.QLabel).text())
        self.value(-2.)
        self.assertIn("Valid result", self.control("resultStatus", QtWidgets.QLabel).text())
        self.assertAlmostEqual(self.result.Shape.Volume, 9000 - 26 * 16 * 13, places=5)
        self.assertAlmostEqual(self.result.Shape.BoundBox.XMin, 0.)
        self.control("reverseSide", QtWidgets.QPushButton).click()
        settle()
        self.assertEqual(self.result.Value, 2.)
        self.assertAlmostEqual(self.result.Shape.BoundBox.XMin, -2.)
        self.assertEqual(self.source.Shape.exportBrepToString(), self.original)
        self.value(0.)
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        self.assertIsNotNone(self.doc.getObject("Thickness"))
        self.assertIn("Cannot accept", self.control("resultStatus", QtWidgets.QLabel).text())
        self.value(-2.)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertTrue(self.doc.Thickness.Shape.isValid())
        self.assertEqual(self.source.Shape.exportBrepToString(), self.original)

    def testInvalidNewCancelRemovesFeatureAndRestoresVisibility(self):
        self.launch()
        self.value(0.)
        self.accept()
        Gui.Control.activeTaskDialog().reject()
        settle()
        self.assertIsNone(self.doc.getObject("Thickness"))
        self.assertTrue(self.source.Visibility)
        self.assertEqual(self.source.Shape.exportBrepToString(), self.original)

    def testExistingFailedEditCancelRestoresGeometryAndParameters(self):
        self.launch()
        self.value(-1.)
        self.accept()
        original = self.doc.Thickness.Shape.exportBrepToString()
        undo = self.doc.UndoCount
        self.launch(self.doc.Thickness)
        self.value(0.)
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        Gui.Control.activeTaskDialog().reject()
        settle()
        self.doc.recompute()
        self.assertEqual(self.doc.Thickness.Value, -1.)
        self.assertEqual(self.doc.Thickness.Shape.exportBrepToString(), original)
        self.assertEqual(self.doc.UndoCount, undo)

    def testFaceCollectorRetainsChangesAndClearsExplicitly(self):
        self.launch()
        button = self.control("facesButton", QtWidgets.QPushButton)
        button.click()
        settle()
        self.assertEqual(Gui.Selection.getSelectionEx()[0].SubElementNames, ("Face6",))
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.source, "Face1")
        button.click()
        settle()
        self.assertEqual(self.result.Faces, (self.source, ["Face1"]))
        self.assertIn("Face1", self.control("labelFaces", QtWidgets.QLabel).text())
        button.click()
        Gui.Selection.clearSelection()
        button.click()
        settle()
        self.assertEqual(self.result.Faces, (self.source, []))
        self.assertIn("none", self.control("labelFaces", QtWidgets.QLabel).text())
        Gui.Control.activeTaskDialog().reject()
        self.assertIsNone(self.doc.getObject("Thickness"))

    def testDeferredPreviewAndExpressionArePreserved(self):
        self.launch()
        self.control("updateView", QtWidgets.QCheckBox).setChecked(False)
        old = self.result.Shape.Volume
        self.value(-1.)
        self.assertIn("pending", self.control("resultStatus", QtWidgets.QLabel).text())
        self.assertEqual(self.result.Shape.Volume, old)
        self.accept()
        self.assertAlmostEqual(self.doc.Thickness.Shape.Volume, 9000 - 28 * 18 * 14, places=5)
        self.doc.Thickness.setExpression("Value", "-Enclosure.Height / 15")
        self.doc.recompute()
        self.launch(self.doc.Thickness)
        self.assertFalse(self.control("reverseSide", QtWidgets.QPushButton).isEnabled())
        self.accept()
        self.assertEqual(self.doc.Thickness.ExpressionEngine, [("Value", "-Enclosure.Height / 15")])

    def testUndoRedoReopenAndDownstreamUpdate(self):
        undo = self.doc.UndoCount
        self.launch()
        self.value(-2.)
        self.accept()
        self.assertEqual(self.doc.UndoCount, undo + 1)
        volume = self.doc.Thickness.Shape.Volume
        self.doc.undo()
        self.assertIsNone(self.doc.getObject("Thickness"))
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.Thickness.Shape.Volume, volume, places=5)
        self.assertEqual(self.doc.Thickness.Faces, (self.source, ["Face6"]))
        consumer = self.doc.addObject("Part::Refine", "Consumer")
        consumer.Source = self.doc.Thickness
        self.doc.recompute()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Shell.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.doc.Enclosure.Length = 40
            self.doc.recompute()
            expected = 40 * 20 * 15 - 36 * 16 * 13
            self.assertAlmostEqual(self.doc.Thickness.Shape.Volume, expected, places=5)
            self.assertAlmostEqual(self.doc.Consumer.Shape.Volume, expected, places=5)
            self.assertTrue(self.doc.Consumer.Shape.isValid())

    def testKernelFailureKeepsSourceAndCanRetry(self):
        self.launch()
        self.value(-10.)
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        self.assertEqual(self.source.Shape.exportBrepToString(), self.original)
        self.value(-1.)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertTrue(self.doc.Thickness.Shape.isValid())
