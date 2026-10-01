# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native filled 3D Offset: geometry, task controls and edit lifecycle."""
import math
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtWidgets


def sheet(doc, curved=False, reversed_normal=False):
    obj = doc.addObject("Part::Feature", "Sheet")
    if curved:
        shape = next(f for f in Part.makeCylinder(5, 10).Faces
                     if isinstance(f.Surface, Part.Cylinder))
    else:
        shape = Part.makePlane(10, 8)
    if reversed_normal:
        shape.reverse()
    obj.Shape = shape
    doc.recompute()
    return obj


def offset(doc, source, value=1., fill=True):
    result = doc.addObject("Part::Offset", "Offset")
    result.Source = source
    result.Value = value
    result.Fill = fill
    doc.recompute()
    return result


def task(source=None, result=None):
    if result is None:
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(source)
        Gui.runCommand("Part_Offset")
        result = source.Document.getObject("Offset")
    else:
        Gui.activeDocument().setEdit(result.Name)
    Gui.updateGui()
    panels = Gui.Control.activeTaskDialog().getDialogContent()
    panel = next(p for p in panels if p.findChild(QtWidgets.QLabel, "resultStatus"))
    return result, panel


def distance(panel, value):
    panel.findChild(QtWidgets.QWidget, "spinOffset").setProperty("rawValue", value)
    Gui.updateGui()


class TestSheetThickening(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("ThickenTest")
        self.doc.UndoMode = 1

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def assertSolid(self, obj, volume):
        self.assertNotIn("Invalid", obj.State, obj.State)
        self.assertEqual(len(obj.Shape.Solids), 1)
        if obj.TypeId == "Part::Offset":
            self.assertEqual(obj.Shape.ShapeType, "Solid")
        self.assertTrue(obj.Shape.isValid())
        self.assertTrue(obj.Shape.Solids[0].isClosed())
        self.assertAlmostEqual(obj.Shape.Volume, volume, places=5)

    def testPlanarBothSidesNormalsAndOpenShell(self):
        for reverse in (False, True):
            source = sheet(self.doc, reversed_normal=reverse)
            before = source.Shape.exportBrepToString()
            for value in (2., -2.):
                result = offset(self.doc, source, value)
                self.assertSolid(result, 160)
                direction = -value if reverse else value
                self.assertAlmostEqual(result.Shape.BoundBox.ZMin, min(0, direction))
                self.assertAlmostEqual(result.Shape.BoundBox.ZMax, max(0, direction))
            self.assertEqual(before, source.Shape.exportBrepToString())
        source.Shape = Part.makeShell([Part.makePlane(10, 8)])
        self.doc.recompute()
        self.assertSolid(offset(self.doc, source, 1.), 80)

    def testCurvedBothSidesAndExcessiveInwardThickness(self):
        source = sheet(self.doc, curved=True)
        before = source.Shape.exportBrepToString()
        result = offset(self.doc, source, 1.)
        self.assertSolid(result, 110 * math.pi)
        result.Value = -1.
        self.doc.recompute()
        self.assertSolid(result, 90 * math.pi)
        previous = result.Shape.exportBrepToString()
        result.Value = -6.
        self.doc.recompute()
        self.assertIn("Invalid", result.State)
        self.assertEqual(previous, result.Shape.exportBrepToString())
        self.assertEqual(before, source.Shape.exportBrepToString())
        result.Value = 2.
        self.doc.recompute()
        self.assertSolid(result, 240 * math.pi)

    def testZeroFailureRetainsResultAndUnfilledRemainsSheet(self):
        source = sheet(self.doc)
        result = offset(self.doc, source)
        for value in (0., float("inf"), float("nan")):
            with self.subTest(value=value):
                result.Value = value
                self.doc.recompute()
                self.assertIn("Invalid", result.State)
                self.assertAlmostEqual(result.Shape.Volume, 80)
        result.Value = 2.
        result.Fill = False
        self.doc.recompute()
        self.assertNotIn("Invalid", result.State)
        self.assertEqual(len(result.Shape.Solids), 0)
        self.assertAlmostEqual(result.Shape.Area, 80)
        self.assertAlmostEqual(result.Shape.BoundBox.ZMin, 2)

    def testNativeControlsReverseDeferredPreviewAndCancel(self):
        source = sheet(self.doc)
        before = source.Shape.exportBrepToString()
        result, panel = task(source)
        status = panel.findChild(QtWidgets.QLabel, "resultStatus")
        self.assertIn("Offset sheet result", status.text())
        panel.findChild(QtWidgets.QCheckBox, "fillOffset").setChecked(True)
        distance(panel, 2.)
        self.assertIn("1 solid", status.text())
        panel.findChild(QtWidgets.QPushButton, "reverseSide").click()
        self.assertEqual(result.Value, -2.)
        self.assertSolid(result, 160)
        self.assertAlmostEqual(result.Shape.BoundBox.ZMin, -2)
        update = panel.findChild(QtWidgets.QCheckBox, "updateView")
        update.setChecked(False)
        distance(panel, 3.)
        self.assertIn("Preview pending", status.text())
        update.setChecked(True)
        self.assertSolid(result, 240)
        Gui.Control.activeTaskDialog().reject()
        self.assertIsNone(self.doc.getObject("Offset"))
        self.assertEqual(before, source.Shape.exportBrepToString())

    def testFailedAcceptAllowsCorrectionAndUndoRedo(self):
        source = sheet(self.doc, curved=True)
        result, panel = task(source)
        panel.findChild(QtWidgets.QCheckBox, "fillOffset").setChecked(True)
        distance(panel, -6.)
        self.assertIn("Offset failed", panel.findChild(QtWidgets.QLabel, "resultStatus").text())
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIs(self.doc.getObject("Offset"), result)
        self.assertIn("Cannot accept", panel.findChild(QtWidgets.QLabel, "resultStatus").text())
        distance(panel, -1.)
        Gui.Control.activeTaskDialog().accept()
        self.assertFalse(Gui.Control.activeDialog())
        self.assertSolid(result, 90 * math.pi)
        self.doc.undo()
        self.assertIsNone(self.doc.getObject("Offset"))
        self.doc.redo()
        self.assertSolid(self.doc.Offset, 90 * math.pi)

    def testFailedEditCancelRestoresCommittedFeature(self):
        source = sheet(self.doc)
        result = offset(self.doc, source, 2.)
        before = result.Shape.exportBrepToString()
        _, panel = task(result=result)
        distance(panel, 0.)
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertEqual(result.Value, 2.)
        self.assertEqual(before, result.Shape.exportBrepToString())
        self.assertSolid(result, 160)

    def testExpressionPreservedAndTwoDControlsUnchanged(self):
        source = sheet(self.doc)
        result = offset(self.doc, source)
        result.setExpression("Value", "2")
        self.doc.recompute()
        _, panel = task(result=result)
        reverse = panel.findChild(QtWidgets.QPushButton, "reverseSide")
        self.assertFalse(reverse.isEnabled())
        reverse.click()
        self.assertEqual(result.ExpressionEngine, [("Value", "2")])
        Gui.Control.activeTaskDialog().reject()
        two = self.doc.addObject("Part::Offset2D", "Offset2D")
        two.Source = source
        self.doc.recompute()
        _, panel = task(result=two)
        self.assertTrue(panel.findChild(QtWidgets.QPushButton, "reverseSide").isHidden())
        self.assertTrue(panel.findChild(QtWidgets.QLabel, "resultStatus").isHidden())
        self.assertEqual(panel.findChild(QtWidgets.QCheckBox, "fillOffset").text(), "Fill offset")
        Gui.Control.activeTaskDialog().reject()
        self.assertNotIn("Invalid", two.State)

    def testSharedSolidThicknessKeepsFaceSelectionControls(self):
        source = self.doc.addObject("Part::Box", "Box")
        self.doc.recompute()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(source, "Face6")
        Gui.runCommand("Part_Thickness")
        Gui.updateGui()
        panels = Gui.Control.activeTaskDialog().getDialogContent()
        panel = next(p for p in panels if p.findChild(QtWidgets.QPushButton, "facesButton"))
        self.assertFalse(panel.findChild(QtWidgets.QPushButton, "facesButton").isHidden())
        self.assertFalse(panel.findChild(QtWidgets.QPushButton, "reverseSide").isHidden())
        self.assertFalse(panel.findChild(QtWidgets.QLabel, "resultStatus").isHidden())
        self.assertEqual(panel.findChild(QtWidgets.QLabel, "labelOffset").text(), "Signed thickness")
        self.assertTrue(self.doc.Thickness.Shape.isValid())
        Gui.Control.activeTaskDialog().accept()
        self.assertFalse(Gui.Control.activeDialog())
        self.assertEqual(self.doc.Thickness.Faces, (source, ["Face6"]))
        self.assertEqual(len(self.doc.Thickness.Shape.Solids), 1)

    def testAssociativeSourceDownstreamAndReopen(self):
        source = sheet(self.doc)
        result = offset(self.doc, source, 2.)
        tool = self.doc.addObject("Part::Box", "Tool")
        tool.Length = 5
        tool.Width = 8
        tool.Height = 2
        cut = self.doc.addObject("Part::Cut", "Downstream")
        cut.Base = result
        cut.Tool = tool
        self.doc.recompute()
        self.assertSolid(cut, 80)
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Thickened.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.doc.Sheet.Shape = Part.makePlane(12, 8)
            self.doc.recompute()
            self.assertEqual(self.doc.Offset.Source, self.doc.Sheet)
            self.assertSolid(self.doc.Offset, 192)
            self.assertSolid(self.doc.Downstream, 112)
