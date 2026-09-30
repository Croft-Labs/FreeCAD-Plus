# SPDX-License-Identifier: LGPL-2.1-or-later

"""Combined Pattern command and task controls; requires the rebuilt GUI."""

import unittest

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui

from PartDesignTests.TestPattern import TestPattern


class TestPatternTaskPanel(unittest.TestCase):
    def setUp(self):
        TestPattern.setUp(self)
        Gui.activateWorkbench("PartDesignWorkbench")
        Gui.activeDocument().activeView().setActiveObject("pdbody", self.body)
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)

    def widget(self, cls, name):
        for panel in Gui.Control.activeTaskDialog().getDialogContent():
            widget = panel.findChild(cls, name)
            if widget is not None:
                return widget
        self.fail("Missing task widget: " + name)

    def start(self, preselect=True):
        if preselect:
            Gui.Selection.addSelection(self.bump)
        Gui.runCommand("PartDesign_Pattern")
        Gui.updateGui()
        self.assertTrue(Gui.Control.activeDialog())
        pattern = self.doc.Pattern
        linear, circular = pattern.PatternSettings
        self.widget(QtGui.QAbstractSpinBox, "spinExtent").setProperty("rawValue", 10.0)
        self.setOccurrences(3)
        circular.Occurrences = 4
        self.doc.recompute()
        return pattern

    def setOccurrences(self, count):
        # UIntSpinBox remaps QSpinBox's signed storage. Invoke its uint slot;
        # calling the Python QSpinBox.setValue wrapper can request billions of copies.
        widget = self.widget(QtGui.QSpinBox, "spinOccurrences")
        self.assertTrue(QtCore.QMetaObject.invokeMethod(
            widget, "setValue", QtCore.Qt.DirectConnection, QtCore.Q_ARG("uint", count)))

    def switch(self, index):
        self.widget(QtGui.QComboBox, "patternType").setCurrentIndex(index)
        Gui.updateGui()

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertFalse(Gui.Control.activeDialog())

    def requestDirectionPick(self):
        combo = self.widget(QtGui.QComboBox, "comboDirection")
        index = next(i for i in range(combo.count()) if combo.itemText(i).startswith("Select reference"))
        combo.setCurrentIndex(index)
        combo.activated[int].emit(index)
        Gui.updateGui()

    def testOriginalsFeedbackTracksPicksModesAndReopen(self):
        pattern = self.start(False)
        status = self.widget(QtGui.QLabel, "patternOriginalsStatus")
        clear = self.widget(QtGui.QPushButton, "patternClearOriginals")
        self.assertIn("Originals: 0", status.text())
        self.assertIn("Accepts: additive/subtractive features", status.text())
        self.assertIn("Picking: add original feature", status.text())
        self.assertFalse(clear.isEnabled())
        Gui.Selection.addSelection(self.bump, "Face1")
        self.assertIn("Originals: 1", status.text())
        self.assertIn("Originals picking inactive", status.text())
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        Gui.Selection.addSelection(self.bump)
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertIn("Originals: 1", status.text())
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        self.widget(QtGui.QPushButton, "buttonRemoveFeature").click()
        self.assertIn("Picking: remove original feature", status.text())
        Gui.Selection.addSelection(self.bump)
        self.assertIn("Originals: 0", status.text())
        self.assertFalse(clear.isEnabled())
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        Gui.Selection.addSelection(self.bump)
        self.widget(QtGui.QRadioButton, "radioTransformBody").click()
        self.assertIn("Originals: 1", status.text())
        self.assertIn("Whole body; selected features are retained", status.text())
        self.assertFalse(clear.isEnabled())
        self.widget(QtGui.QRadioButton, "radioTransformToolShapes").click()
        self.assertTrue(clear.isEnabled())
        self.accept()
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.assertIn("Originals: 1", self.widget(QtGui.QLabel, "patternOriginalsStatus").text())

    def testClearOriginalsLeavesRecoverableTaskAndPreservesSettings(self):
        pattern = self.start()
        linear, circular = pattern.PatternSettings
        direction = linear.Direction
        settings = (linear.Length.Value, linear.Occurrences, circular.Occurrences)
        self.requestDirectionPick()
        self.widget(QtGui.QPushButton, "patternClearOriginals").click()
        self.assertEqual(pattern.Originals, [])
        self.assertEqual(self.widget(QtGui.QListWidget, "listWidgetFeatures").count(), 0)
        self.assertTrue(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        self.assertFalse(self.widget(QtGui.QPushButton, "patternClearOriginals").isEnabled())
        self.switch(1)
        self.switch(0)
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        Gui.Selection.addSelection(self.bump, "Face1")
        self.assertEqual(linear.Direction, direction)
        self.assertEqual((linear.Length.Value, linear.Occurrences, circular.Occurrences), settings)
        self.assertEqual(pattern.PatternSettings, [linear, circular])
        self.accept()
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)

    def testClearOriginalsCancelAndReplacementUndoRedo(self):
        pattern = self.start()
        self.accept()
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.widget(QtGui.QPushButton, "patternClearOriginals").click()
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertEqual(self.body.Tip, pattern)
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.widget(QtGui.QPushButton, "patternClearOriginals").click()
        Gui.Selection.addSelection(self.bump)
        self.setOccurrences(4)
        self.accept()
        self.assertAlmostEqual(pattern.Shape.Volume, 8032)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(pattern.Shape.Volume, 8032)

    def testOriginalAndDirectionRolesAreExclusiveBothWays(self):
        pattern = self.start(False)
        linear = pattern.PatternSettings[0]
        self.requestDirectionPick()
        self.assertFalse(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        self.assertIn("Originals picking inactive", self.widget(QtGui.QLabel, "patternOriginalsStatus").text())
        Gui.Selection.addSelection(self.base, "Edge1")
        self.assertEqual(pattern.Originals, [])
        self.assertEqual(linear.Direction[0], self.base)
        self.assertEqual(linear.Direction[1], ["Edge1"])
        self.requestDirectionPick()
        direction = linear.Direction
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        self.assertTrue(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        Gui.Selection.addSelection(self.bump, "Face1")
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertEqual(linear.Direction, direction)

    def testRemoveOriginalsEndsDirectionPicking(self):
        pattern = self.start()
        linear = pattern.PatternSettings[0]
        direction = linear.Direction
        self.requestDirectionPick()
        self.widget(QtGui.QPushButton, "buttonRemoveFeature").click()
        self.assertTrue(self.widget(QtGui.QPushButton, "buttonRemoveFeature").isChecked())
        Gui.Selection.addSelection(self.bump, "Face1")
        self.assertEqual(pattern.Originals, [])
        self.assertEqual(linear.Direction, direction)
        self.assertIn("Originals: 0", self.widget(QtGui.QLabel, "patternOriginalsStatus").text())

    def testFirstFieldThenFeaturePickingWithoutPreselection(self):
        pattern = self.start(False)
        combo = self.widget(QtGui.QComboBox, "patternType")
        self.assertEqual([combo.itemText(i) for i in range(combo.count())], ["Linear", "Circular"])
        header = self.widget(QtGui.QWidget, "patternTypeHeader")
        container = header.parentWidget()
        self.assertEqual(container.layout().itemAt(0).widget(), header)
        self.assertEqual(pattern.Originals, [])
        self.assertTrue(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        self.switch(1)
        self.assertTrue(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        Gui.Selection.addSelection(self.bump, "Face1")
        Gui.updateGui()
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertEqual(self.widget(QtGui.QListWidget, "listWidgetFeatures").count(), 1)
        self.assertAlmostEqual(pattern.Shape.Volume, 8032)
        self.switch(0)
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)
        self.switch(1)
        self.assertAlmostEqual(pattern.Shape.Volume, 8032)
        self.accept()

    def testCreateEditCancelAndUndoRedo(self):
        pattern = self.start()
        self.switch(1)
        self.accept()
        self.assertTrue(pattern.ViewObject.doubleClicked())
        Gui.updateGui()
        self.assertEqual(self.widget(QtGui.QComboBox, "patternType").currentIndex(), 1)
        self.switch(0)
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertEqual(pattern.PatternType, "Circular")
        self.assertAlmostEqual(pattern.Shape.Volume, 8032)
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.switch(0)
        self.accept()
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(pattern.PatternType, "Circular")
        self.assertAlmostEqual(pattern.Shape.Volume, 8032)
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(pattern.PatternType, "Linear")
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)

    def testCancelCreationRemovesBothSettingsAndRestoresTip(self):
        objects = {obj.Name for obj in self.doc.Objects}
        self.start()
        self.switch(1)
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, objects)
        self.assertEqual(self.body.Tip, self.bump)

    def testRemoveLastFeatureBlocksAcceptThenRecovers(self):
        pattern = self.start()
        self.widget(QtGui.QPushButton, "buttonRemoveFeature").click()
        Gui.Selection.addSelection(self.bump)
        Gui.updateGui()
        self.assertEqual(pattern.Originals, [])
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        Gui.Selection.addSelection(self.bump)
        Gui.updateGui()
        self.accept()

    def testCancelRestoresEditedParameterValues(self):
        pattern = self.start()
        self.accept()
        linear = pattern.PatternSettings[0]
        self.assertEqual(linear.Occurrences, 3)
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.setOccurrences(5)
        self.widget(QtGui.QAbstractSpinBox, "spinExtent").setProperty("rawValue", 8.0)
        self.assertEqual(linear.Occurrences, 5)
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertEqual(linear.Occurrences, 3)
        self.assertAlmostEqual(linear.Length.Value, 10)
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)

    def testDirectionAxisSpacingAndExpressionsInSamePane(self):
        pattern = self.start()
        linear, circular = pattern.PatternSettings
        direction = self.widget(QtGui.QComboBox, "comboDirection")
        index = direction.findText("Base Y-axis")
        self.assertGreaterEqual(index, 0)
        direction.setCurrentIndex(index)
        direction.activated[int].emit(index)
        self.assertEqual(linear.Direction[0], self.body.Origin.OriginFeatures[1])
        self.switch(1)
        mode = self.widget(QtGui.QComboBox, "comboMode")
        mode.setCurrentIndex(1)
        mode.activated[int].emit(1)
        self.widget(QtGui.QAbstractSpinBox, "spinSpacing").setProperty("rawValue", 90.0)
        self.setOccurrences(4)
        self.accept()
        self.assertEqual(circular.Mode, "Spacing")
        self.assertAlmostEqual(circular.Offset.Value, 90)
        self.assertAlmostEqual(pattern.Shape.Volume, 8032)
        linear.setExpression("Length", "Bump.Length * 5")
        self.doc.recompute()
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.switch(0)
        self.switch(1)
        self.assertEqual(linear.ExpressionEngine, [("Length", "Bump.Length * 5")])
        self.accept()

    def testFeatureSelectionRejectsOtherBodyAndDependentObjects(self):
        otherBody = self.doc.addObject("PartDesign::Body", "OtherBody")
        other = otherBody.newObject("PartDesign::AdditiveBox", "OtherFeature")
        self.doc.recompute()
        pattern = self.start(False)
        Gui.Selection.addSelection(other)
        self.assertEqual(pattern.Originals, [])
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(pattern)
        self.assertEqual(pattern.Originals, [])
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.bump)
        self.assertEqual(pattern.Originals, [self.bump])
        self.accept()
        dependent = self.body.newObject("PartDesign::AdditiveBox", "Dependent")
        dependent.Placement.Base = App.Vector(0, 0, 5)
        self.doc.recompute()
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(dependent)
        self.assertEqual(pattern.Originals, [self.bump])

    def testFeatureRemovalUsesIdentityRatherThanLabelOrHistoryOrder(self):
        self.base.Label = self.bump.Label
        pattern = self.start()
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        Gui.Selection.addSelection(self.base)
        features = self.widget(QtGui.QListWidget, "listWidgetFeatures")
        self.assertEqual(features.count(), 2)
        # The clicked order differs from sorted Body history, and labels collide.
        features.setCurrentRow(1)
        features.actions()[0].trigger()
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertEqual(features.count(), 1)
        self.assertEqual(features.item(0).data(QtCore.Qt.UserRole), self.bump.Name)
        self.accept()

    def testAcceptRecomputesWhenLivePreviewIsDisabled(self):
        pattern = self.start()
        self.accept()
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.widget(QtGui.QCheckBox, "checkBoxUpdateView").setChecked(False)
        self.setOccurrences(5)
        wait = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(650, wait.quit)  # Exceed the preview debounce interval.
        wait.exec()
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)
        self.accept()
        self.assertAlmostEqual(pattern.Shape.Volume, 8040)

    def testWholeBodyToggleRestoresFeatureList(self):
        pattern = self.start()
        self.widget(QtGui.QRadioButton, "radioTransformBody").click()
        self.assertEqual(self.widget(QtGui.QListWidget, "listWidgetFeatures").count(), 0)
        self.widget(QtGui.QRadioButton, "radioTransformToolShapes").click()
        self.assertEqual(self.widget(QtGui.QListWidget, "listWidgetFeatures").count(), 1)
        self.assertEqual(pattern.Originals, [self.bump])
        self.accept()

    def testMultiTransformEmbeddedPatternStillEdits(self):
        multi = self.body.newObject("PartDesign::MultiTransform", "MultiTransform")
        linear = self.body.newObject("PartDesign::LinearPattern", "LinearSettings")
        multi.Originals = [self.bump]
        linear.Direction = (self.body.Origin.OriginFeatures[0], [""])
        linear.Length = 10
        linear.Occurrences = 3
        multi.Transformations = [linear]
        self.body.Tip = multi
        self.doc.recompute()
        self.assertTrue(multi.ViewObject.doubleClicked())
        transforms = self.widget(QtGui.QListWidget, "listTransformFeatures")
        transforms.setCurrentRow(0)
        transforms.activated.emit(transforms.model().index(0, 0))
        self.setOccurrences(4)
        self.accept()
        self.doc.recompute()
        self.assertEqual(linear.Occurrences, 4)
        self.assertAlmostEqual(multi.Shape.Volume, 8032)

    def testOneToolbarButtonAndLegacyCommandsRemainAvailable(self):
        commands = []
        for toolbar in Gui.getMainWindow().findChildren(QtGui.QToolBar):
            commands.extend(action.objectName() for action in toolbar.actions())
        self.assertEqual(commands.count("PartDesign_Pattern"), 1)
        self.assertNotIn("PartDesign_LinearPattern", commands)
        self.assertNotIn("PartDesign_PolarPattern", commands)
        for command, typeId in [("PartDesign_LinearPattern", "PartDesign::LinearPattern"),
                                ("PartDesign_PolarPattern", "PartDesign::PolarPattern")]:
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(self.bump)
            Gui.runCommand(command)
            Gui.updateGui()
            self.assertEqual(self.body.Tip.TypeId, typeId)
            self.assertIsNotNone(self.widget(QtGui.QListWidget, "listWidgetFeatures"))
            Gui.Control.activeTaskDialog().reject()
