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

    def selectionPaths(self):
        return [(s.DocumentName, s.ObjectName, tuple(s.SubElementNames))
                for s in Gui.Selection.getSelectionEx("*", 0)]

    def testOriginalRowsHighlightByIdentityAndAllWithoutMutation(self):
        self.base.Label = self.bump.Label = "Same label"
        pattern = self.start()
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        Gui.Selection.addSelection(self.base)
        originals = list(pattern.Originals)
        linear, circular = pattern.PatternSettings
        definition = (originals, linear.Direction, circular.Axis, pattern.Shape.Volume)
        entries = self.widget(QtGui.QListWidget, "listWidgetFeatures")
        self.assertEqual(entries.count(), 2)
        self.base.ViewObject.Visibility = False
        self.bump.ViewObject.Visibility = False
        for obj in (self.base, self.bump):
            row = next(i for i in range(entries.count()) if entries.item(i).data(QtCore.Qt.UserRole) == obj.Name)
            entries.setCurrentRow(row)
            self.assertEqual(Gui.Selection.getSelection(), [obj])
            self.assertTrue(obj.ViewObject.Visibility)
            self.assertEqual((list(pattern.Originals), linear.Direction, circular.Axis,
                              pattern.Shape.Volume), definition)
        entries.clearSelection()
        self.widget(QtGui.QPushButton, "patternHighlightOriginals").click()
        self.assertEqual(set(Gui.Selection.getSelection()), set(originals))
        self.assertEqual(pattern.Originals, originals)
        self.assertFalse(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        self.assertFalse(self.widget(QtGui.QPushButton, "buttonRemoveFeature").isChecked())

    def testOriginalInspectionEndsDirectionPickingAndRestoresOnTypeSwitch(self):
        pattern = self.start()
        linear, circular = pattern.PatternSettings
        direction = linear.Direction
        self.requestDirectionPick()
        self.widget(QtGui.QListWidget, "listWidgetFeatures").setCurrentRow(0)
        self.assertEqual(Gui.Selection.getSelection(), [self.bump])
        self.assertEqual(linear.Direction, direction)
        self.assertEqual(pattern.Originals, [self.bump])
        # Type changes must finish inspection before rebuilding the embedded editor.
        self.switch(1)
        axis = circular.Axis
        self.widget(QtGui.QPushButton, "patternHighlightOriginals").click()
        self.assertEqual(circular.Axis, axis)
        self.assertEqual(pattern.Originals, [self.bump])
        self.accept()
        self.assertFalse(self.bump.ViewObject.Visibility)
        self.assertTrue(pattern.ViewObject.Visibility)

    def testOriginalInspectionVisibilityRestoresOnCancelAndAccept(self):
        pattern = self.start()
        self.accept()
        self.assertFalse(self.bump.ViewObject.Visibility)
        for accept in (False, True):
            original = (self.bump.ViewObject.Visibility, pattern.ViewObject.Visibility)
            self.assertTrue(pattern.ViewObject.doubleClicked())
            self.widget(QtGui.QPushButton, "patternHighlightOriginals").click()
            self.assertTrue(self.bump.ViewObject.Visibility)
            self.assertFalse(pattern.ViewObject.Visibility)
            if accept:
                self.accept()
            else:
                Gui.Control.activeTaskDialog().reject()
                Gui.updateGui()
            self.assertEqual((self.bump.ViewObject.Visibility, pattern.ViewObject.Visibility), original)
            self.assertEqual(pattern.Originals, [self.bump])
            self.assertAlmostEqual(pattern.Shape.Volume, 8024)

    def testCancelCreationRestoresOriginalSubelementSelectionAfterInspection(self):
        Gui.Selection.addSelection(self.bump, "Face1")
        selection = self.selectionPaths()
        objects = {obj.Name for obj in self.doc.Objects}
        pattern = self.start(False)
        self.widget(QtGui.QPushButton, "patternHighlightOriginals").click()
        self.widget(QtGui.QPushButton, "patternClearOriginals").click()
        self.assertFalse(self.widget(QtGui.QPushButton, "patternHighlightOriginals").isEnabled())
        Gui.Control.activeTaskDialog().reject()
        Gui.updateGui()
        self.assertEqual(self.selectionPaths(), selection)
        self.assertEqual(self.body.Tip, self.bump)
        self.assertEqual({obj.Name for obj in self.doc.Objects}, objects)

    def testCancelEditRestoresSelectionAndOriginalsAfterInspection(self):
        pattern = self.start()
        self.accept()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(pattern, "Face1")
        selection = self.selectionPaths()
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.widget(QtGui.QPushButton, "patternHighlightOriginals").click()
        self.widget(QtGui.QPushButton, "patternClearOriginals").click()
        self.setOccurrences(4)
        Gui.Control.activeTaskDialog().reject()
        Gui.updateGui()
        self.assertEqual(self.selectionPaths(), selection)
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertEqual(self.body.Tip, pattern)
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)

    def testPreselectionAndLaterPicksAgreeForBothPatternTypes(self):
        other = self.body.newObject("PartDesign::AdditiveBox", "OtherBump")
        other.Length = other.Width = other.Height = 2
        other.Placement.Base = App.Vector(-5, 0, 5)
        self.doc.recompute()
        for mode in (0, 1):
            definitions = []
            shapes = []
            for preselect in (True, False):
                Gui.Selection.clearSelection()
                if preselect:
                    # Multiple subelements denote one original; input order is not history order.
                    Gui.Selection.addSelection(other, "Face1")
                    Gui.Selection.addSelection(self.bump, "Face1")
                    Gui.Selection.addSelection(self.bump, "Face2")
                pattern = self.start(False)
                if not preselect:
                    Gui.Selection.addSelection(self.bump, "Face1")
                    self.widget(QtGui.QPushButton, "buttonAddFeature").click()
                    Gui.Selection.addSelection(other, "Face1")
                self.switch(mode)
                self.accept()
                self.assertTrue(pattern.isValid(), pattern.getStatusString())
                linear, circular = pattern.PatternSettings
                definitions.append((sorted(obj.Name for obj in pattern.Originals), pattern.PatternType,
                                    linear.Direction, linear.Length.Value, linear.Occurrences,
                                    circular.Axis, circular.Occurrences, pattern.Shape.Volume))
                shapes.append(pattern.Shape.copy())
                self.assertTrue(pattern.ViewObject.doubleClicked())
                self.assertEqual(self.widget(QtGui.QListWidget, "listWidgetFeatures").count(), 2)
                Gui.Control.activeTaskDialog().reject()
                self.doc.undo()
                self.doc.recompute()
                self.assertIsNone(self.doc.getObject("Pattern"))
                self.assertEqual(self.body.Tip, other)
            self.assertEqual(definitions[0][:-1], definitions[1][:-1])
            self.assertAlmostEqual(definitions[0][-1], definitions[1][-1])
            # Originals membership is unordered input; native evaluation uses Body history.
            self.assertAlmostEqual(shapes[0].cut(shapes[1]).Volume, 0, places=6)
            self.assertAlmostEqual(shapes[1].cut(shapes[0]).Volume, 0, places=6)

    def testMixedPreselectionKeepsValidOriginalAndExplainsRejections(self):
        sketch = self.body.newObject("Sketcher::SketchObject", "UnusedSketch")
        other_body = self.doc.addObject("PartDesign::Body", "OtherBody")
        other = other_body.newObject("PartDesign::AdditiveBox", "OtherFeature")
        self.doc.recompute()
        Gui.activeDocument().activeView().setActiveObject("pdbody", self.body)
        for obj in (other, sketch, self.bump):
            Gui.Selection.addSelection(obj)
        selection = self.selectionPaths()
        pattern = self.start(False)
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertIn(pattern, self.body.Group)
        hint = self.widget(QtGui.QLabel, "patternOriginalsHint")
        self.assertIn("OtherFeature", hint.text())
        self.assertIn("active body", hint.text())
        self.assertIn("UnusedSketch", hint.text())
        self.assertIn("additive or subtractive", hint.text())
        self.assertFalse(hint.isHidden())
        self.assertFalse(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        Gui.Control.activeTaskDialog().reject()
        Gui.updateGui()
        self.assertEqual(self.selectionPaths(), selection)
        self.assertIsNone(self.doc.getObject("Pattern"))

    def testInvalidOnlyPreselectionLeavesUsefulTaskAndRecovers(self):
        Gui.Selection.addSelection(self.body)
        pattern = self.start(False)
        self.assertEqual(pattern.Originals, [])
        hint = self.widget(QtGui.QLabel, "patternOriginalsHint")
        self.assertFalse(hint.isHidden())
        self.assertTrue(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        # A failed OK ends picking; restart it explicitly if needed.
        if not self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked():
            self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        Gui.Selection.addSelection(self.bump, "Face1")
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertTrue(hint.isHidden())
        self.accept()
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)

    def testCrossDocumentPreselectionAndLaterPickUseSameRejection(self):
        foreign = App.newDocument("ForeignPatternInputs")
        try:
            body = foreign.addObject("PartDesign::Body", "Body")
            feature = body.newObject("PartDesign::AdditiveBox", "ForeignFeature")
            foreign.recompute()
            App.setActiveDocument(self.doc.Name)
            Gui.activeDocument().activeView().setActiveObject("pdbody", self.body)
            Gui.Selection.addSelection(feature)
            pattern = self.start(False)
            hint = self.widget(QtGui.QLabel, "patternOriginalsHint")
            self.assertIn("this document", hint.text())
            self.assertEqual(pattern.Originals, [])
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(feature)
            self.assertIn("this document", hint.text())
            self.assertEqual(pattern.Originals, [])
            Gui.Selection.addSelection(self.bump)
            self.assertEqual(pattern.Originals, [self.bump])
            self.assertTrue(hint.isHidden())
            self.accept()
        finally:
            App.closeDocument(foreign.Name)

    def testRejectedLaterPicksExplainScopeDependencyAndRecover(self):
        pattern = self.start()
        self.accept()
        downstream = self.body.newObject("PartDesign::AdditiveBox", "Downstream")
        downstream.Length = downstream.Width = downstream.Height = 2
        downstream.Placement.Base = App.Vector(0, 0, 5)
        other_body = self.doc.addObject("PartDesign::Body", "OtherBody")
        other = other_body.newObject("PartDesign::AdditiveBox", "OtherFeature")
        self.doc.recompute()
        Gui.activeDocument().activeView().setActiveObject("pdbody", self.body)
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        hint = self.widget(QtGui.QLabel, "patternOriginalsHint")
        for obj, reason in ((other, "active body"), (pattern, "depending on"),
                            (downstream, "depending on"), (self.bump, "already an original")):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
            self.assertIn(reason, hint.text())
            self.assertEqual(pattern.Originals, [self.bump])
            self.assertTrue(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        self.widget(QtGui.QPushButton, "patternClearOriginals").click()
        self.assertTrue(hint.isHidden())
        Gui.Selection.addSelection(self.bump)
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertTrue(hint.isHidden())
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertEqual(self.body.Tip, downstream)

    def testRemoveUnlistedFeatureExplainsAndKeepsPickerActive(self):
        pattern = self.start()
        self.widget(QtGui.QPushButton, "buttonRemoveFeature").click()
        Gui.Selection.addSelection(self.base)
        hint = self.widget(QtGui.QLabel, "patternOriginalsHint")
        self.assertIn("not in Originals", hint.text())
        self.assertTrue(self.widget(QtGui.QPushButton, "buttonRemoveFeature").isChecked())
        self.assertEqual(pattern.Originals, [self.bump])
        Gui.Selection.addSelection(self.bump)
        self.assertEqual(pattern.Originals, [])
        self.assertTrue(hint.isHidden())

    def referenceCombo(self, secondary=False):
        status = self.widget(QtGui.QLabel, "patternReferenceStatus2" if secondary else "patternReferenceStatus")
        parent = status.parentWidget()
        combo = parent.findChild(QtGui.QComboBox, "comboDirection")
        # Keep intermediate PySide wrappers alive while using their child controls.
        self._referenceWidgets = getattr(self, "_referenceWidgets", []) + [status, parent, combo]
        return combo

    def pickReference(self, secondary=False):
        combo = self.referenceCombo(secondary)
        index = next(i for i in range(combo.count()) if combo.itemText(i).startswith("Select reference"))
        combo.setCurrentIndex(index)
        combo.activated[int].emit(index)
        Gui.updateGui()

    def enableSecondDirection(self):
        status = self.widget(QtGui.QLabel, "patternReferenceStatus2")
        parent = status.parentWidget()
        root = parent.parentWidget()
        check = root.findChild(QtGui.QCheckBox, "enableCheckbox")
        self.assertIsNotNone(check)
        self._referenceWidgets = getattr(self, "_referenceWidgets", []) + [status, parent, root, check]
        if not check.isChecked():
            check.click()

    def horizontalBaseEdge(self):
        return next("Edge" + str(i + 1) for i, edge in enumerate(self.base.Shape.Edges)
                    if len(edge.Vertexes) == 2
                    and abs((edge.Vertexes[1].Point - edge.Vertexes[0].Point).x) > 1)

    def testReferenceFeedbackTracksPrimarySecondaryAndAxisRoles(self):
        pattern = self.start()
        status = self.widget(QtGui.QLabel, "patternReferenceStatus")
        status2 = self.widget(QtGui.QLabel, "patternReferenceStatus2")
        self.assertIn("References: 1", status.text())
        self.assertIn("References: 1", status2.text())
        self.pickReference()
        self.assertIn("Picking reference", status.text())
        self.assertIn("picking inactive", status2.text())
        self.enableSecondDirection()
        self.pickReference(True)
        self.assertIn("Picking reference", status2.text())
        self.assertIn("picking inactive", status.text())
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        self.assertIn("picking inactive", status2.text())
        self.switch(1)
        self.assertIn("References: 1", self.widget(QtGui.QLabel, "patternReferenceStatus").text())
        self.pickReference()
        self.assertIn("Picking reference", self.widget(QtGui.QLabel, "patternReferenceStatus").text())
        self.assertEqual(pattern.Originals, [self.bump])

    def testReferenceHighlightKeepsSubelementIdentityAndOriginals(self):
        pattern = self.start()
        linear, circular = pattern.PatternSettings
        self.pickReference()
        edge = self.horizontalBaseEdge()
        Gui.Selection.addSelection(self.base, edge)
        selected_path = self.selectionPaths()
        self.doc.recompute()
        self.assertTrue(pattern.isValid(), pattern.getStatusString())
        definition = (linear.Direction, linear.Direction2, circular.Axis,
                      list(pattern.Originals), pattern.Shape.Volume)
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        self.base.ViewObject.Visibility = False
        self.widget(QtGui.QPushButton, "patternHighlightReference").click()
        reference, subs = linear.Direction
        self.assertEqual(self.selectionPaths(), selected_path)
        resolved = [(item.DocumentName, item.ObjectName, tuple(item.SubElementNames))
                    for item in Gui.Selection.getSelectionEx("*")]
        self.assertEqual(resolved, [(reference.Document.Name, reference.Name, tuple(subs))])
        self.assertTrue(self.base.ViewObject.Visibility)
        self.assertFalse(pattern.ViewObject.Visibility)
        self.assertFalse(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        self.assertEqual((linear.Direction, linear.Direction2, circular.Axis,
                          list(pattern.Originals), pattern.Shape.Volume), definition)
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        self.assertFalse(self.base.ViewObject.Visibility)

    def testReferenceInspectionEndsOtherReferencePickerWithoutMutation(self):
        pattern = self.start()
        linear = pattern.PatternSettings[0]
        definition = (linear.Direction, linear.Direction2, list(pattern.Originals))
        self.enableSecondDirection()
        self.pickReference(True)
        self.widget(QtGui.QPushButton, "patternHighlightReference").click()
        self.assertEqual(Gui.Selection.getSelection(), [linear.Direction[0]])
        self.assertIn("picking inactive", self.widget(QtGui.QLabel, "patternReferenceStatus2").text())
        self.widget(QtGui.QPushButton, "patternHighlightReference2").click()
        self.assertEqual(Gui.Selection.getSelection(), [linear.Direction2[0]])
        self.assertEqual((linear.Direction, linear.Direction2, list(pattern.Originals)), definition)
        self.accept()
        self.assertEqual((linear.Direction, linear.Direction2, list(pattern.Originals)), definition)

    def testReferenceInspectionRestoresVisibilityOnTypeSwitchAndExit(self):
        pattern = self.start()
        self.pickReference()
        Gui.Selection.addSelection(self.base, self.horizontalBaseEdge())
        self.accept()
        self.base.ViewObject.Visibility = False
        axes_visibility = [(obj, obj.ViewObject.Visibility) for obj in self.body.Origin.OriginFeatures]
        for accept in (False, True):
            self.assertTrue(pattern.ViewObject.doubleClicked())
            self.widget(QtGui.QPushButton, "patternHighlightReference").click()
            self.assertTrue(self.base.ViewObject.Visibility)
            self.switch(1)
            self.assertFalse(self.base.ViewObject.Visibility)
            axis = pattern.PatternSettings[1].Axis
            self.widget(QtGui.QPushButton, "patternHighlightReference").click()
            self.assertEqual(Gui.Selection.getSelection(), [axis[0]])
            self.switch(0)
            self.widget(QtGui.QPushButton, "patternHighlightReference").click()
            if accept:
                self.accept()
            else:
                Gui.Control.activeTaskDialog().reject()
                Gui.updateGui()
            self.assertFalse(self.base.ViewObject.Visibility)
            self.assertTrue(pattern.ViewObject.Visibility)
            self.assertEqual(pattern.Originals, [self.bump])
            self.assertEqual([(obj, obj.ViewObject.Visibility) for obj, _ in axes_visibility], axes_visibility)

    def testEmptyReferenceFeedbackRecoversWithoutAssigningOtherRoles(self):
        pattern = self.start()
        linear = pattern.PatternSettings[0]
        second = linear.Direction2
        linear.Direction = None
        self.setOccurrences(4)
        status = self.widget(QtGui.QLabel, "patternReferenceStatus")
        highlight = self.widget(QtGui.QPushButton, "patternHighlightReference")
        self.assertIn("References: 0", status.text())
        self.assertFalse(highlight.isEnabled())
        self.pickReference()
        Gui.Selection.addSelection(self.base, self.horizontalBaseEdge())
        self.assertIn("References: 1", status.text())
        self.assertTrue(highlight.isEnabled())
        self.assertIn("picking inactive", status.text())
        self.assertEqual(linear.Direction2, second)
        self.assertEqual(pattern.Originals, [self.bump])

    def testReferenceInspectionCancelRestoresInitialSelection(self):
        Gui.Selection.addSelection(self.bump, "Face1")
        initial = self.selectionPaths()
        pattern = self.start(False)
        self.widget(QtGui.QPushButton, "patternHighlightReference").click()
        Gui.Control.activeTaskDialog().reject()
        Gui.updateGui()
        self.assertEqual(self.selectionPaths(), initial)
        self.assertEqual(self.body.Tip, self.bump)
        self.assertIsNone(self.doc.getObject("Pattern"))

    def referenceDefinition(self, pattern):
        linear, circular = pattern.PatternSettings
        return (linear.Direction, linear.Direction2, circular.Axis, list(pattern.Originals))

    def prepareSecondReference(self):
        self.enableSecondDirection()
        combo = self.referenceCombo(True)
        group = combo.parentWidget()
        extent = group.findChild(QtGui.QAbstractSpinBox, "spinExtent")
        self._referenceWidgets.extend([group, extent])
        extent.setProperty("rawValue", 10.0)

    def undoCreatedPattern(self):
        self.doc.undo()
        self.doc.recompute()
        self.assertIsNone(self.doc.getObject("Pattern"))
        self.assertEqual(self.body.Tip, self.bump)

    def testPendingReferenceOriginalsTransitionsPreserveLinksOnOK(self):
        for action in ("buttonAddFeature", "buttonRemoveFeature", "patternClearOriginals"):
            with self.subTest(action=action):
                pattern = self.start()
                if action == "patternClearOriginals":
                    self.switch(1)
                secondary = action == "buttonRemoveFeature"
                if secondary:
                    self.prepareSecondReference()
                definition = self.referenceDefinition(pattern)
                self.pickReference(secondary)
                self.widget(QtGui.QPushButton, action).click()
                status = self.widget(QtGui.QLabel, "patternReferenceStatus2" if secondary else "patternReferenceStatus")
                self.assertIn("picking inactive", status.text())
                self.assertFalse(self.referenceCombo(secondary).currentText().startswith("Select reference"))
                if action == "patternClearOriginals":
                    Gui.Selection.addSelection(self.bump)
                else:
                    self.widget(QtGui.QPushButton, action).click()
                self.accept()
                self.assertEqual(self.referenceDefinition(pattern), definition)
                self.undoCreatedPattern()

    def testPendingReferenceOKKeepsPrimarySecondaryAndAxis(self):
        for role in ("primary", "secondary", "axis"):
            with self.subTest(role=role):
                pattern = self.start()
                if role == "axis":
                    self.switch(1)
                elif role == "secondary":
                    self.prepareSecondReference()
                definition = self.referenceDefinition(pattern)
                self.pickReference(role == "secondary")
                self.accept()
                self.assertEqual(self.referenceDefinition(pattern), definition)
                self.assertTrue(pattern.isValid(), pattern.getStatusString())
                self.undoCreatedPattern()

    def testPendingReferenceTypeSwitchRetainsBothDefinitions(self):
        pattern = self.start()
        definition = self.referenceDefinition(pattern)
        self.pickReference()
        self.switch(1)
        self.assertEqual(self.referenceDefinition(pattern), definition)
        self.pickReference()
        self.switch(0)
        self.assertEqual(self.referenceDefinition(pattern), definition)
        self.accept()
        self.assertEqual(self.referenceDefinition(pattern), definition)

    def testScopeChangeEndsReferencePickingAndDoesNotConsumeLaterPick(self):
        pattern = self.start()
        definition = self.referenceDefinition(pattern)
        self.pickReference()
        self.widget(QtGui.QRadioButton, "radioTransformBody").click()
        self.assertIn("picking inactive", self.widget(QtGui.QLabel, "patternReferenceStatus").text())
        Gui.Selection.addSelection(self.base, self.horizontalBaseEdge())
        self.assertEqual(self.referenceDefinition(pattern), definition)
        self.widget(QtGui.QRadioButton, "radioTransformToolShapes").click()
        self.accept()
        self.assertEqual(self.referenceDefinition(pattern), definition)

    def testOriginalsTypeRejectionsArePreciseBeforeAndAfterStartup(self):
        sketch = self.body.newObject("Sketcher::SketchObject", "UnusedSketch")
        self.doc.recompute()
        Gui.Selection.addSelection(self.body)
        pattern = self.start(False)
        hint = self.widget(QtGui.QLabel, "patternOriginalsHint")
        self.assertIn("not a body, sketch or datum", hint.text())
        for obj in (self.body, sketch, self.body.Origin.OriginFeatures[0]):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
            self.assertIn("not a body, sketch or datum", hint.text())
            self.assertNotIn("depending on", hint.text())
            self.assertEqual(pattern.Originals, [])
            self.assertTrue(self.widget(QtGui.QPushButton, "buttonAddFeature").isChecked())
        Gui.Selection.addSelection(self.bump)
        self.assertEqual(pattern.Originals, [self.bump])
        self.assertTrue(hint.isHidden())
        self.accept()

    def testPendingReferenceRoleChangeAndEditCancelRestoresState(self):
        pattern = self.start()
        self.accept()
        definition = self.referenceDefinition(pattern)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(pattern, "Face1")
        initial = self.selectionPaths()
        self.assertTrue(pattern.ViewObject.doubleClicked())
        self.pickReference()
        self.widget(QtGui.QPushButton, "buttonAddFeature").click()
        self.setOccurrences(4)
        Gui.Control.activeTaskDialog().reject()
        Gui.updateGui()
        self.assertEqual(self.referenceDefinition(pattern), definition)
        self.assertEqual(self.selectionPaths(), initial)
        self.assertEqual(self.body.Tip, pattern)
        self.assertAlmostEqual(pattern.Shape.Volume, 8024)

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
