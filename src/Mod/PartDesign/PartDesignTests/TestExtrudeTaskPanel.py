# SPDX-License-Identifier: LGPL-2.1-or-later

"""Shared Extrude task behavior; requires the rebuilt FreeCAD Plus GUI."""

import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtGui

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
