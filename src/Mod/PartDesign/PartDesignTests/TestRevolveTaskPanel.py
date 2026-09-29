# SPDX-License-Identifier: LGPL-2.1-or-later

"""Angular start offsets in the shared Revolution/Groove GUI task."""

import math
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtGui


class TestRevolveTaskPanel(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("RevolveTaskPanelTest")
        self.doc.UndoMode = 1
        self.body = self.doc.addObject("PartDesign::Body", "Body")
        self.base = self.body.newObject("PartDesign::AdditiveCylinder", "Base")
        self.base.Radius = 4
        self.base.Height = 4
        self.base.Placement.Base.z = -1
        self.sketch = self.body.newObject("Sketcher::SketchObject", "Profile")
        points = [(2, 0), (5, 0), (5, 2), (2, 2)]
        for start, end in zip(points, points[1:] + points[:1]):
            self.sketch.addGeometry(Part.LineSegment(App.Vector(*start, 0), App.Vector(*end, 0)))
        self.sketch.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), 90)
        self.doc.recompute()
        Gui.activateWorkbench("PartDesignWorkbench")
        Gui.activeDocument().activeView().setActiveObject("pdbody", self.body)
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)

    def widget(self, cls, name):
        dialog = Gui.Control.activeTaskDialog()
        self.assertIsNotNone(dialog)
        for panel in dialog.getDialogContent():
            widget = panel.findChild(cls, name)
            if widget is not None:
                return widget
        self.fail("Missing task widget: " + name)

    def quantity(self, name, value):
        self.widget(QtGui.QWidget, name).setProperty("rawValue", value)
        Gui.updateGui()

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertFalse(Gui.Control.activeDialog())

    def start(self, command):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.sketch)
        Gui.runCommand(command)
        Gui.updateGui()
        self.assertTrue(Gui.Control.activeDialog())
        name = "Groove" if command == "PartDesign_Groove" else "Revolution"
        feature = self.doc.getObject(name)
        self.assertIsNotNone(feature)
        axis = self.widget(QtGui.QComboBox, "axis")
        index = axis.findText("Vertical sketch axis")
        self.assertGreaterEqual(index, 0)
        axis.setCurrentIndex(index)
        axis.activated[int].emit(index)
        Gui.updateGui()
        self.assertAlmostEqual(feature.Axis.z, 1)
        self.assertAlmostEqual(feature.Axis.x, 0)
        self.assertAlmostEqual(feature.Axis.y, 0)
        reverse = self.widget(QtGui.QToolButton, "buttonReverse")
        if reverse.isChecked():
            reverse.click()
        self.quantity("revolveAngle", 60.0)
        self.quantity("revolveAngle2", 30.0)
        return feature

    def assertGeometry(self, feature, mode, reverse, offset):
        sign = -1 if reverse else 1
        first, second = ((0, 60), (-30, 60), (-30, 30))[mode]
        low, high = sorted((sign * (offset + first), sign * (offset + second)))
        span = high - low
        # Independent cylindrical-sector solid, not the feature's revolution output.
        tool = Part.makeCylinder(5, 2, App.Vector(), App.Vector(0, 0, 1), span)
        tool = tool.cut(Part.makeCylinder(2, 2))
        tool.rotate(App.Vector(), App.Vector(0, 0, 1), low)
        base = Part.makeCylinder(4, 4, App.Vector(0, 0, -1))
        if feature.TypeId == "PartDesign::Revolution":
            expected = base.fuse(tool)
            volume = 64 * math.pi + 18 * math.pi * span / 360
        else:
            expected = base.cut(tool)
            volume = 64 * math.pi - 24 * math.pi * span / 360
        self.assertTrue(feature.isValid(), feature.getStatusString())
        self.assertTrue(feature.Shape.isValid())
        self.assertEqual(len(feature.Shape.Solids), 1)
        self.assertAlmostEqual(feature.StartOffset.Value, offset)
        self.assertAlmostEqual(feature.Shape.Volume, volume, places=6)
        # Bounds and both differences detect rotation errors hidden by equal volumes.
        # Rendering attaches triangulation; use exact geometry bounds after reopening.
        actual_bounds = feature.Shape.optimalBoundingBox(False)
        expected_bounds = expected.optimalBoundingBox(False)
        for extent in ("XMin", "XMax", "YMin", "YMax", "ZMin", "ZMax"):
            self.assertAlmostEqual(getattr(actual_bounds, extent),
                                   getattr(expected_bounds, extent), places=6)
        self.assertAlmostEqual(feature.Shape.cut(expected).Volume, 0, places=6)
        self.assertAlmostEqual(expected.cut(feature.Shape).Volume, 0, places=6)

    def testAddSubtractOffsetGeometryMatrix(self):
        for command in ("PartDesign_Revolution", "PartDesign_Groove"):
            feature = self.start(command)
            for reverse in (False, True):
                self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(0)
                button = self.widget(QtGui.QToolButton, "buttonReverse")
                if button.isChecked() != reverse:
                    button.click()
                for mode in range(3):
                    self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(mode)
                    for offset in (0.0, 45.0, -45.0, 180.0, -180.0, 360.0, -360.0):
                        with self.subTest(command=command, reverse=reverse,
                                          mode=mode, offset=offset):
                            if offset < 0:
                                self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
                            else:
                                self.quantity("startOffsetEdit", offset)
                            self.assertGeometry(feature, mode, reverse, offset)
            self.accept()
            self.assertTrue(feature.ViewObject.doubleClicked())
            Gui.updateGui()
            self.assertGeometry(feature, 2, True, -360)
            self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
            self.assertGeometry(feature, 2, True, 360)
            Gui.Control.activeTaskDialog().reject()
            self.doc.recompute()
            self.assertGeometry(feature, 2, True, -360)
            name = feature.Name
            self.doc.undo()
            self.doc.recompute()
            self.assertIsNone(self.doc.getObject(name))

    def testDefaultVisibilityAndInclusiveRange(self):
        for command in ("PartDesign_Revolution", "PartDesign_Groove"):
            feature = self.start(command)
            for mode in range(3):
                self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(mode)
                self.assertEqual(feature.StartOffset.Value, 0)
                self.assertTrue(self.widget(QtGui.QWidget, "startOffsetEdit").isVisible())
                self.assertTrue(self.widget(QtGui.QToolButton, "buttonReverseOffset").isVisible())
                self.assertEqual(self.widget(QtGui.QToolButton, "buttonReverse").isEnabled(), mode != 2)
                self.assertEqual(self.widget(QtGui.QToolButton, "buttonReverse2").isVisible(), mode == 1)
            self.quantity("startOffsetEdit", 361.0)
            self.assertEqual(feature.StartOffset.Value, 360)
            self.quantity("startOffsetEdit", -361.0)
            self.assertEqual(feature.StartOffset.Value, -360)
            self.widget(QtGui.QComboBox, "startMode").setCurrentIndex(0)
            self.assertEqual(feature.StartOffset.Value, 0)
            self.assertEqual(feature.StartType, "Profile plane")
            panels = Gui.Control.activeTaskDialog().getDialogContent()
            self.assertFalse(any(p.findChild(QtGui.QCheckBox, "checkBoxReversed") for p in panels))
            Gui.Control.activeTaskDialog().reject()

    def testBothAngleButtonsAndReopenCancel(self):
        for command in ("PartDesign_Revolution", "PartDesign_Groove"):
            feature = self.start(command)
            self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(1)
            self.quantity("startOffsetEdit", 45.0)
            first = self.widget(QtGui.QToolButton, "buttonReverse")
            second = self.widget(QtGui.QToolButton, "buttonReverse2")
            first.click()
            self.assertTrue(second.isChecked())
            self.assertGeometry(feature, 1, True, 45)
            second.click()
            self.assertFalse(first.isChecked())
            self.assertGeometry(feature, 1, False, 45)
            self.assertEqual(feature.Angle.Value, 60)
            self.assertEqual(feature.Angle2.Value, 30)
            self.accept()
            self.assertTrue(feature.ViewObject.doubleClicked())
            Gui.updateGui()
            self.widget(QtGui.QToolButton, "buttonReverse2").click()
            self.assertGeometry(feature, 1, True, 45)
            Gui.Control.activeTaskDialog().reject()
            self.doc.recompute()
            self.assertGeometry(feature, 1, False, 45)
            self.doc.undo()
            self.doc.recompute()

    def checkExpressionPersistence(self, command):
        feature = self.start(command)
        self.quantity("startOffsetEdit", 20.0)
        self.accept()
        feature.setExpression("StartOffset", "Angle / 3")
        self.doc.recompute()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
        self.assertAlmostEqual(feature.StartOffset.Value, -20)
        self.accept()
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, 20)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, -20)
        feature.Angle = 90
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, -30)
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.widget(QtGui.QComboBox, "startMode").setCurrentIndex(0)
        self.assertEqual(feature.StartOffset.Value, 0)
        self.assertNotIn("StartOffset", dict(feature.ExpressionEngine))
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, -30)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "AngularOffset.FCStd")
            name = feature.Name
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            feature = self.doc.getObject(name)
            self.assertAlmostEqual(feature.StartOffset.Value, -30)
            self.assertIn("Angle", dict(feature.ExpressionEngine)["StartOffset"])
            self.assertTrue(feature.ViewObject.doubleClicked())
            Gui.updateGui()
            self.assertAlmostEqual(self.widget(QtGui.QWidget, "startOffsetEdit").property("rawValue"), -30)
            self.accept()

    def testAddExpressionPersistence(self):
        self.checkExpressionPersistence("PartDesign_Revolution")

    def testSubtractExpressionPersistence(self):
        self.checkExpressionPersistence("PartDesign_Groove")
