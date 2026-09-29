# SPDX-License-Identifier: LGPL-2.1-or-later

"""Shared Extrude task behavior; requires the rebuilt FreeCAD Plus GUI."""

import unittest
import tempfile
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui

# Reopen via ViewObject.doubleClicked() to include the UI edit transaction.


class TestExtrudeTaskPanel(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("ExtrudeTaskPanelTest")
        self.doc.UndoMode = 1
        self.body = self.doc.addObject("PartDesign::Body", "Body")
        self.base = self.body.newObject("PartDesign::AdditiveBox", "Base")
        self.base.Length = self.base.Width = self.base.Height = 10
        self.sketch = self.body.newObject("Sketcher::SketchObject", "Profile")
        points = [(2, 2), (6, 2), (6, 6), (2, 6)]
        for start, end in zip(points, points[1:] + points[:1]):
            self.sketch.addGeometry(Part.LineSegment(App.Vector(*start, 0), App.Vector(*end, 0)))
        self.sketch.Placement.Base.z = 5
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
        # Closed task widgets can await deferred deletion during a test run.
        # Only inspect the currently active editor.
        dialog = Gui.Control.activeTaskDialog()
        self.assertIsNotNone(dialog)
        for panel in dialog.getDialogContent():
            widget = panel.findChild(cls, name)
            if widget is not None:
                return widget
        self.fail("Missing task widget: " + name)

    def operation(self):
        return self.widget(QtGui.QComboBox, "comboOperation")

    def selectOperation(self, operation):
        combo = self.operation()
        index = combo.findData(operation)
        self.assertGreaterEqual(index, 0)
        combo.setCurrentIndex(index)
        combo.activated[int].emit(index)
        Gui.updateGui()

    def start(self, command="PartDesign_Extrude", preselect=False):
        if preselect:
            Gui.Selection.addSelection(self.sketch)
        Gui.runCommand(command)
        Gui.updateGui()
        self.assertTrue(Gui.Control.activeDialog())
        name = "Pocket" if command == "PartDesign_Pocket" else "Pad"
        feature = self.doc.getObject(name)
        self.assertIsNotNone(feature)
        return feature

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertFalse(Gui.Control.activeDialog())

    def testOperationIsFirstFieldAndProfileCanBeSelectedAfterStarting(self):
        feature = self.start()
        combo = self.operation()
        self.assertEqual([combo.itemText(i) for i in range(combo.count())], ["Add", "Subtract"])
        self.assertEqual(combo.currentData(), "Union")
        group = self.widget(QtGui.QGroupBox, "padProfileGroup")
        # Keep the parent wrapper alive while inspecting its layout.
        container = group.parentWidget()
        layout = container.layout()
        self.assertEqual(layout.itemAt(0).layout().itemAt(1).widget(), combo)
        self.assertEqual(layout.itemAt(1).widget(), group)
        self.assertIsNone(feature.Profile)
        self.selectOperation("Subtraction")
        Gui.Selection.addSelection(self.sketch)
        self.assertEqual(feature.Profile[0], self.sketch)
        self.assertAlmostEqual(feature.Shape.Volume, 920)
        self.accept()

    def checkKeyboardLengthCommit(self, operation, initial):
        """#32718/#32717: native editor events update both create and edit tasks."""
        feature = self.start(preselect=True)
        self.selectOperation(operation)

        def check(value):
            Gui.updateGui()
            self.assertAlmostEqual(feature.Length.Value, value)
            expected = 1000 + 16 * (value - 5) if operation == "Union" else 1000 - 16 * value
            self.assertAlmostEqual(feature.Shape.Volume, expected, places=6)

        for reopened in (False, True):
            if reopened:
                self.assertTrue(feature.ViewObject.doubleClicked())
                Gui.updateGui()
            spin = self.widget(QtGui.QWidget, "lengthEdit")
            spin.setProperty("singleStep", 1.0)
            editor = spin.findChild(QtGui.QLineEdit)
            spin.setFocus()
            editor.selectAll()
            value = initial + int(reopened)
            for char in f"{value} mm":
                for kind in (QtCore.QEvent.KeyPress, QtCore.QEvent.KeyRelease):
                    QtGui.QApplication.sendEvent(
                        editor, QtGui.QKeyEvent(kind, 0, QtCore.Qt.NoModifier, char)
                    )
            self.widget(QtGui.QWidget, "startOffsetEdit").setFocus()
            QtGui.QApplication.sendEvent(spin, QtGui.QFocusEvent(QtCore.QEvent.FocusOut))
            check(value)
            spin.setFocus()
            for kind in (QtCore.QEvent.KeyPress, QtCore.QEvent.KeyRelease):
                QtGui.QApplication.sendEvent(
                    spin, QtGui.QKeyEvent(kind, QtCore.Qt.Key_Up, QtCore.Qt.NoModifier)
                )
            self.widget(QtGui.QWidget, "startOffsetEdit").setFocus()
            QtGui.QApplication.sendEvent(spin, QtGui.QFocusEvent(QtCore.QEvent.FocusOut))
            check(value + 1)
            self.accept()
            check(value + 1)

    def testAddKeyboardEditsUpdateModelOnCreateAndReopen(self):
        self.checkKeyboardLengthCommit("Union", 12)

    def testSubtractKeyboardEditsUpdateModelOnCreateAndReopen(self):
        self.checkKeyboardLengthCommit("Subtraction", 2)

    def testSwitchCreateThenReopenAndCancel(self):
        feature = self.start(preselect=True)
        original = feature.Shape.Volume
        direction = feature.Direction
        self.selectOperation("Subtraction")
        self.assertAlmostEqual(feature.Shape.Volume, 920)
        self.assertEqual(feature.Direction, direction)
        self.accept()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.assertEqual(self.operation().currentData(), "Subtraction")
        self.selectOperation("Union")
        self.assertAlmostEqual(feature.Shape.Volume, original)
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertEqual(feature.Operation, "Subtraction")
        self.assertAlmostEqual(feature.Shape.Volume, 920)

    def testLegacyPocketUsesSharedProfileControlsAndCanBecomeAdditive(self):
        feature = self.start("PartDesign_Pocket")
        self.assertEqual(self.operation().currentData(), "Subtraction")
        Gui.Selection.addSelection(self.sketch)
        profile_list = self.widget(QtGui.QListWidget, "padProfileList")
        self.assertEqual(profile_list.count(), 1)
        self.selectOperation("Union")
        self.assertEqual(feature.TypeId, "PartDesign::Pocket")
        self.assertEqual(feature.Profile[0], self.sketch)
        self.accept()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.assertEqual(self.operation().currentData(), "Union")
        self.widget(QtGui.QPushButton, "padClearProfile").click()
        self.assertIsNone(feature.Profile)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.sketch)
        self.assertEqual(feature.Profile[0], self.sketch)

    def testExtentChoiceIsPreservedByNameOnBothFeatureTypes(self):
        for command in ("PartDesign_Extrude", "PartDesign_Pocket"):
            with self.subTest(command=command):
                feature = self.start(command, preselect=True)
                mode = self.widget(QtGui.QComboBox, "changeMode")
                mode.setCurrentIndex(1)  # To last, including on a legacy Pocket.
                self.assertEqual(feature.Type, "UpToLast")
                self.selectOperation("Subtraction")
                self.assertEqual(feature.Type, "UpToLast")
                mode.setCurrentIndex(5)  # Through all, including on a stored Pad.
                self.assertEqual(feature.Type, "ThroughAll")
                self.accept()
                self.assertEqual(feature.Type, "ThroughAll")
                self.doc.undo()
                Gui.Selection.clearSelection()

    def testExistingCommonRemainsEditable(self):
        feature = self.body.newObject("PartDesign::Pocket", "ExistingPocket")
        feature.Profile = self.sketch
        feature.Length = 7
        feature.Operation = "Common"
        self.doc.recompute()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.assertEqual(self.operation().currentData(), "Common")
        self.assertAlmostEqual(feature.Shape.Volume, 80)
        self.accept()
        self.assertEqual(feature.Operation, "Common")

    def testAcceptedOperationEditCanUndoRedo(self):
        feature = self.start(preselect=True)
        self.accept()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.selectOperation("Subtraction")
        self.accept()
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(feature.Operation, "Union")
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(feature.Operation, "Subtraction")

    def testNoBaseSubtractCannotBeAcceptedAndRecoversInSameTask(self):
        self.doc.removeObject(self.base.Name)
        self.doc.recompute()
        feature = self.start(preselect=True)
        self.selectOperation("Subtraction")
        self.assertFalse(feature.isValid())
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.selectOperation("Union")
        self.assertTrue(feature.isValid(), feature.getStatusString())
        self.accept()

    def quantity(self, name, value):
        self.widget(QtGui.QWidget, name).setProperty("rawValue", value)
        Gui.updateGui()

    def testOffsetIsVisibleAndZeroInEveryDirectionMode(self):
        feature = self.start(preselect=True)
        for mode in range(3):
            self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(mode)
            self.assertEqual(feature.StartOffset.Value, 0)
            self.assertTrue(self.widget(QtGui.QWidget, "startOffsetEdit").isVisible())
            self.assertTrue(self.widget(QtGui.QToolButton, "buttonReverseOffset").isVisible())
            self.assertEqual(self.widget(QtGui.QToolButton, "buttonReverse").isEnabled(), mode != 2)
            self.assertEqual(self.widget(QtGui.QToolButton, "buttonReverse2").isVisible(), mode == 1)
        panels = Gui.Control.activeTaskDialog().getDialogContent()
        self.assertFalse(any(p.findChild(QtGui.QCheckBox, "checkBoxReversed") for p in panels))

    def testSignedOffsetGeometryInAllDirectionModes(self):
        self.doc.removeObject(self.base.Name)
        feature = self.start(preselect=True)
        self.quantity("lengthEdit", 6.0)
        self.quantity("lengthEdit2", 2.0)
        for mode, low, high in [(0, 0, 6), (1, -2, 6), (2, -3, 3)]:
            with self.subTest(mode=mode):
                self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(mode)
                self.quantity("startOffsetEdit", 2.0)
                self.assertEqual(feature.StartType, "Offset")
                self.assertTrue(feature.isValid(), feature.getStatusString())
                self.assertAlmostEqual(feature.Shape.BoundBox.ZMin, 7 + low)
                self.assertAlmostEqual(feature.Shape.BoundBox.ZMax, 7 + high)
                self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
                self.assertAlmostEqual(feature.StartOffset.Value, -2)
                self.assertAlmostEqual(feature.Shape.BoundBox.ZMin, 3 + low)
                self.assertAlmostEqual(feature.Shape.BoundBox.ZMax, 3 + high)
        self.accept()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.assertEqual(self.widget(QtGui.QWidget, "startOffsetEdit").property("rawValue"), -2)
        self.assertEqual(self.widget(QtGui.QComboBox, "sidesMode").currentIndex(), 2)

    def testBothLengthButtonsReverseTheExistingTwoSidedAxis(self):
        self.doc.removeObject(self.base.Name)
        feature = self.start(preselect=True)
        self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(1)
        self.quantity("lengthEdit", 6.0)
        self.quantity("lengthEdit2", 2.0)
        self.quantity("startOffsetEdit", 1.0)
        first = self.widget(QtGui.QToolButton, "buttonReverse")
        second = self.widget(QtGui.QToolButton, "buttonReverse2")
        first.click()
        self.assertTrue(feature.Reversed)
        self.assertTrue(second.isChecked())
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMin, -2)
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMax, 6)
        second.click()
        self.assertFalse(feature.Reversed)
        self.assertFalse(first.isChecked())
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMin, 4)
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMax, 12)
        self.assertEqual(feature.Length.Value, 6)
        self.assertEqual(feature.Length2.Value, 2)

    def testSubtractOffsetAndLegacyPocket(self):
        for command in ("PartDesign_Extrude", "PartDesign_Pocket"):
            with self.subTest(command=command):
                feature = self.start(command, preselect=True)
                self.selectOperation("Subtraction")
                # Legacy Pocket starts in the opposite direction.
                if feature.Reversed:
                    self.widget(QtGui.QToolButton, "buttonReverse").click()
                # Pocket Direction includes its legacy convention; normalize via the model.
                if feature.Direction.z < 0:
                    self.widget(QtGui.QToolButton, "buttonReverse").click()
                self.quantity("lengthEdit", 4.0)
                self.quantity("startOffsetEdit", 2.0)
                self.assertAlmostEqual(feature.Shape.Volume, 952)
                self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
                self.assertAlmostEqual(feature.Shape.Volume, 936)
                self.accept()
                self.doc.undo()
                self.doc.recompute()
                Gui.Selection.clearSelection()

    def testOffsetExpressionFlipAndReopen(self):
        self.doc.removeObject(self.base.Name)
        feature = self.start(preselect=True)
        self.quantity("lengthEdit", 6.0)
        self.quantity("startOffsetEdit", 2.0)
        self.accept()
        feature.setExpression("StartOffset", "Length / 3")
        self.doc.recompute()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
        self.assertAlmostEqual(feature.StartOffset.Value, -2)
        self.accept()
        self.assertIn("Length", dict(feature.ExpressionEngine)["StartOffset"])
        feature.Length = 9
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, -3)
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.assertAlmostEqual(self.widget(QtGui.QWidget, "startOffsetEdit").property("rawValue"), -3)

    def testOffsetAndReverseCancelUndoRedo(self):
        feature = self.start(preselect=True)
        self.accept()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.quantity("startOffsetEdit", 2.0)
        self.widget(QtGui.QToolButton, "buttonReverse").click()
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, 0)
        self.assertFalse(feature.Reversed)
        self.assertEqual(feature.StartType, "Profile plane")
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.quantity("startOffsetEdit", -2.0)
        self.accept()
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, 0)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, -2)
        self.assertEqual(feature.StartType, "Offset")

    def testReverseRemainsAvailableWithoutDimensionAndProfilePlaneResetsOffset(self):
        feature = self.start(preselect=True)
        self.selectOperation("Subtraction")
        self.quantity("startOffsetEdit", 2.0)
        self.widget(QtGui.QComboBox, "startMode").setCurrentIndex(0)
        self.assertEqual(feature.StartType, "Profile plane")
        self.assertAlmostEqual(feature.StartOffset.Value, 0)
        self.widget(QtGui.QComboBox, "changeMode").setCurrentIndex(5)
        reverse = self.widget(QtGui.QToolButton, "buttonReverse")
        self.assertTrue(reverse.isVisible())
        self.assertTrue(reverse.isEnabled())
        self.assertFalse(self.widget(QtGui.QWidget, "lengthEdit").isVisible())
        reverse.click()
        self.assertTrue(feature.Reversed)
        self.assertTrue(feature.isValid(), feature.getStatusString())

    def testOffsetSaveReopenAndExpressionCancel(self):
        feature = self.start(preselect=True)
        self.quantity("startOffsetEdit", -2.0)
        self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(1)
        self.quantity("lengthEdit", 6.0)
        self.quantity("lengthEdit2", 2.0)
        self.accept()
        feature.setExpression("StartOffset", "-Length / 3")
        self.doc.recompute()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
        self.assertAlmostEqual(feature.StartOffset.Value, 2)
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertAlmostEqual(feature.StartOffset.Value, -2)
        with tempfile.TemporaryDirectory() as folder:
            name = feature.Name
            path = str(Path(folder) / "Offset.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            feature = self.doc.getObject(name)
            self.assertEqual(feature.SideType, "Two sides")
            self.assertAlmostEqual(feature.StartOffset.Value, -2)
            self.assertIn("Length", dict(feature.ExpressionEngine)["StartOffset"])
            self.assertTrue(feature.ViewObject.doubleClicked())
            Gui.updateGui()
            self.assertAlmostEqual(self.widget(QtGui.QWidget, "startOffsetEdit").property("rawValue"), -2)
            self.accept()

    def testReferenceStartOffsetStillFlipsInSamePane(self):
        feature = self.start(preselect=True)
        self.quantity("lengthEdit", 6.0)
        self.accept()
        # Use the base top plane, with Subtract pointing back into the base solid.
        top = max(range(len(self.base.Shape.Faces)), key=lambda i: self.base.Shape.Faces[i].CenterOfMass.z)
        feature.Operation = "Subtraction"
        feature.Reversed = True
        feature.StartReference = (self.base, ["Face%d" % (top + 1)])
        feature.StartType = "Reference"
        self.doc.recompute()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.quantity("startOffsetEdit", 2.0)
        self.assertEqual(feature.StartType, "Reference")
        self.assertAlmostEqual(feature.Shape.Volume, 904)
        self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
        self.assertEqual(feature.StartType, "Reference")
        self.assertAlmostEqual(feature.Shape.Volume, 936)
        self.assertEqual(feature.StartReference[0], self.base)

    def testAddSubtractOffsetGeometryMatrix(self):
        """Check actual solids against an independent box oracle, through real task controls."""
        for command, normal in (("PartDesign_Extrude", 1), ("PartDesign_Pocket", -1)):
            feature = self.start(command, preselect=True)
            self.quantity("lengthEdit", 12.0)
            self.quantity("lengthEdit2", 4.0)

            def check_geometry(operation, mode, reverse, offset):
                sign = normal * (-1 if reverse else 1)
                origin = 5 + sign * offset
                first, second = ((0, 12), (-4, 12), (-6, 6))[mode]
                low, high = sorted((origin + sign * first, origin + sign * second))
                tool = Part.makeBox(4, 4, high - low, App.Vector(2, 2, low))
                base = Part.makeBox(10, 10, 10)
                overlap = max(0, min(10, high) - max(0, low))
                if operation == "Union":
                    expected = base.fuse(tool)
                    volume = 1000 + 16 * (high - low - overlap)
                else:
                    expected = base.cut(tool)
                    volume = 1000 - 16 * overlap
                self.assertTrue(feature.isValid(), feature.getStatusString())
                self.assertTrue(feature.Shape.isValid())
                self.assertEqual(len(feature.Shape.Solids), 1)
                self.assertAlmostEqual(feature.StartOffset.Value, offset)
                self.assertAlmostEqual(feature.Shape.Volume, volume, places=6)
                # Equal volume alone cannot detect a cut/addition on the wrong side.
                self.assertAlmostEqual(feature.Shape.cut(expected).Volume, 0, places=6)
                self.assertAlmostEqual(expected.cut(feature.Shape).Volume, 0, places=6)
                for extent in ("XMin", "XMax", "YMin", "YMax", "ZMin", "ZMax"):
                    self.assertAlmostEqual(
                        getattr(feature.Shape.BoundBox, extent),
                        getattr(expected.BoundBox, extent), places=6
                    )

            for reverse in (False, True):
                self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(0)
                button = self.widget(QtGui.QToolButton, "buttonReverse")
                if button.isChecked() != reverse:
                    button.click()
                for mode in range(3):
                    self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(mode)
                    for operation in ("Union", "Subtraction"):
                        self.selectOperation(operation)
                        for offset in (0.0, 2.0, -2.0):
                            with self.subTest(command=command, operation=operation,
                                              mode=mode, reverse=reverse, offset=offset):
                                if offset == -2:
                                    self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
                                else:
                                    self.quantity("startOffsetEdit", offset)
                                check_geometry(operation, mode, reverse, offset)

            self.accept()
            self.assertTrue(feature.ViewObject.doubleClicked())
            Gui.updateGui()
            check_geometry("Subtraction", 2, True, -2)
            self.widget(QtGui.QToolButton, "buttonReverseOffset").click()
            check_geometry("Subtraction", 2, True, 2)
            Gui.Control.activeTaskDialog().reject()
            self.doc.recompute()
            check_geometry("Subtraction", 2, True, -2)
            name = feature.Name
            self.doc.undo()
            self.doc.recompute()
            self.assertIsNone(self.doc.getObject(name))
            Gui.Selection.clearSelection()
