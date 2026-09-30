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

    def selectionPaths(self):
        return [(s.DocumentName, s.ObjectName, tuple(s.SubElementNames))
                for s in Gui.Selection.getSelectionEx("*", 0)]

    def definition(self, feature):
        return (feature.TypeId, feature.Profile, feature.ReferenceAxis,
                feature.Operation, feature.Type, feature.SideType,
                feature.Length.Value, feature.Length2.Value, feature.StartOffset.Value,
                feature.Reversed, feature.AlongSketchNormal, tuple(feature.Direction),
                feature.Shape.Volume,
                tuple(tuple(solid.CenterOfMass) for solid in feature.Shape.Solids))

    def testPreselectionMatchesCommandFirstForExtrudeAndAliases(self):
        for command in ("PartDesign_Extrude", "PartDesign_Pad", "PartDesign_Pocket"):
            for operation in ("Union", "Subtraction"):
                definitions = []
                for preselect in (True, False):
                    with self.subTest(command=command, operation=operation, preselect=preselect):
                        Gui.Selection.clearSelection()
                        feature = self.start(command, preselect=preselect)
                        if not preselect:
                            Gui.Selection.addSelection(self.sketch)
                        self.selectOperation(operation)
                        self.quantity("lengthEdit", 8.0)
                        self.accept()
                        definitions.append(self.definition(feature))
                        self.assertEqual(feature.Profile[0], self.sketch)
                        self.assertEqual(self.body.Tip, feature)
                        self.assertAlmostEqual(feature.Shape.Volume, 1048 if operation == "Union" else 920)
                        self.doc.undo()
                        self.doc.recompute()
                self.assertEqual(definitions[0], definitions[1])

    def testMixedSolidAndProfilePreselectionIsIndependentOfOrder(self):
        for target in (self.base, self.body):
            for profileFirst in (True, False):
                Gui.Selection.clearSelection()
                for obj in ((self.sketch, target) if profileFirst else (target, self.sketch)):
                    Gui.Selection.addSelection(obj)
                feature = self.start()
                self.assertEqual(feature.Profile[0], self.sketch)
                self.assertEqual(feature.getParentGeoFeatureGroup(), self.body)
                self.assertIn("Ignored preselection", self.widget(QtGui.QLabel, "extrudePreselectionHint").text())
                self.selectOperation("Subtraction")
                self.accept()
                self.assertAlmostEqual(feature.Shape.Volume, 920)
                self.doc.undo()
                self.doc.recompute()

    def testAmbiguousProfilesOpenCollectorAndCanBeChosenExplicitly(self):
        other = self.body.newObject("Sketcher::SketchObject", "OtherProfile")
        other.addGeometry(Part.Circle(App.Vector(4, 4, 5), App.Vector(0, 0, 1), 1))
        self.doc.recompute()
        for reverse in (False, True):
            Gui.Selection.clearSelection()
            for obj in ((other, self.sketch) if reverse else (self.sketch, other)):
                Gui.Selection.addSelection(obj)
            feature = self.start()
            self.assertIsNone(feature.Profile)
            self.assertTrue(self.widget(QtGui.QPushButton, "padSelectProfile").isChecked())
            self.assertIn("Several profile objects", self.widget(QtGui.QLabel, "extrudePreselectionHint").text())
            Gui.Selection.addSelection(self.sketch)
            self.assertEqual(feature.Profile[0], self.sketch)
            self.accept()
            self.doc.undo()
            self.doc.recompute()

    def testInvalidPreselectionLeavesRecoverableTaskWithoutChangingBody(self):
        foreign = self.doc.addObject("PartDesign::Body", "OtherBody")
        sketch = foreign.newObject("Sketcher::SketchObject", "ForeignProfile")
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 1))
        self.doc.recompute()
        for obj, sub in ((self.base, ""), (self.sketch, "Vertex1"), (sketch, "")):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj, sub)
            feature = self.start()
            self.assertIsNone(feature.Profile)
            self.assertIn("Ignored preselection", self.widget(QtGui.QLabel, "extrudePreselectionHint").text())
            self.assertEqual(feature.getParentGeoFeatureGroup(), self.body)
            Gui.Selection.addSelection(self.sketch)
            self.accept()
            self.doc.undo()
            self.doc.recompute()

    def testCancelRestoresOriginalSelectionAndBodyTipOnCreateAndEdit(self):
        for command in ("PartDesign_Extrude", "PartDesign_Pad", "PartDesign_Pocket"):
            Gui.Selection.addSelection(self.base, "Face6")
            original = self.selectionPaths()
            tip = self.body.Tip
            feature = self.start(command)
            Gui.Control.activeTaskDialog().reject()
            Gui.updateGui()
            self.assertIsNone(self.doc.getObject("Pocket" if command == "PartDesign_Pocket" else "Pad"))
            self.assertEqual(self.body.Tip, tip)
            self.assertEqual(self.selectionPaths(), original)
            Gui.Selection.clearSelection()
            feature = self.start(command, preselect=True)
            self.accept()
            Gui.Selection.addSelection(feature, "Face1")
            original = self.selectionPaths()
            self.assertTrue(feature.ViewObject.doubleClicked())
            self.widget(QtGui.QPushButton, "padClearProfile").click()
            Gui.Control.activeTaskDialog().reject()
            Gui.updateGui()
            self.assertEqual(feature.Profile[0], self.sketch)
            self.assertEqual(self.body.Tip, feature)
            self.assertEqual(self.selectionPaths(), original)
            Gui.Selection.clearSelection()
            self.doc.undo()
            self.doc.recompute()

    def testProfileFeedbackTracksEntriesPickingAndReopen(self):
        feature = self.start()
        status = self.widget(QtGui.QLabel, "padProfileStatus")
        highlight = self.widget(QtGui.QPushButton, "padHighlightProfile")
        self.assertIn("Entries: 0", status.text())
        self.assertIn("Accepts: sketch, curves or faces", status.text())
        self.assertIn("Picking: Profile", status.text())
        self.assertFalse(highlight.isEnabled())
        for i in range(1, 5):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(self.sketch, "Edge%d" % i)
            self.assertIn("Entries: %d" % i, status.text())
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.sketch, "Edge1")
        self.assertIn("Entries: 4", status.text())
        self.widget(QtGui.QListWidget, "padProfileList").item(0).setSelected(True)
        self.widget(QtGui.QPushButton, "padRemoveProfile").click()
        self.assertIn("Entries: 3", status.text())
        self.widget(QtGui.QPushButton, "padClearProfile").click()
        self.assertIn("Entries: 0", status.text())
        self.assertFalse(highlight.isEnabled())
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.sketch)
        self.assertIn("Entries: 1", status.text())  # Whole profile, not its four edges.
        self.widget(QtGui.QPushButton, "padSelectProfile").click()
        self.assertIn("Profile picking inactive", status.text())
        self.accept()
        self.assertTrue(feature.ViewObject.doubleClicked())
        self.assertIn("Entries: 1", self.widget(QtGui.QLabel, "padProfileStatus").text())
        self.assertTrue(self.widget(QtGui.QPushButton, "padHighlightProfile").isEnabled())

    def testProfileRowAndAllHighlightDoNotChangeDefinition(self):
        feature = self.start()
        for i in range(1, 5):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(self.sketch, "Edge%d" % i)
        original = self.definition(feature)
        entries = self.widget(QtGui.QListWidget, "padProfileList")
        entries.item(1).setSelected(True)
        selected = Gui.Selection.getSelectionEx()
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].Object, self.sketch)
        self.assertEqual(selected[0].SubElementNames, ("Edge2",))
        entries.item(3).setSelected(True)
        self.assertEqual(set(Gui.Selection.getSelectionEx()[0].SubElementNames), {"Edge2", "Edge4"})
        entries.clearSelection()
        self.widget(QtGui.QPushButton, "padHighlightProfile").click()
        self.assertEqual(set(Gui.Selection.getSelectionEx()[0].SubElementNames),
                         {"Edge1", "Edge2", "Edge3", "Edge4"})
        self.assertEqual(self.definition(feature), original)
        self.assertEqual(entries.count(), 4)

    def testProfileInspectionCannotFillStartReference(self):
        feature = self.start(preselect=True)
        self.widget(QtGui.QComboBox, "startMode").setCurrentIndex(2)
        reference = self.widget(QtGui.QPushButton, "buttonStartReference")
        if not reference.isChecked():
            reference.click()
        original = (feature.Profile, feature.ReferenceAxis, feature.StartReference)
        self.widget(QtGui.QListWidget, "padProfileList").item(0).setSelected(True)
        self.assertFalse(reference.isChecked())
        self.assertTrue(self.widget(QtGui.QPushButton, "padSelectProfile").isChecked())
        self.assertIn("Picking: Profile", self.widget(QtGui.QLabel, "padProfileStatus").text())
        self.assertEqual((feature.Profile, feature.ReferenceAxis, feature.StartReference), original)
        self.assertEqual(Gui.Selection.getSelection(), [self.sketch])

    def testProfileInspectionVisibilityRestoresOnCancelAndAccept(self):
        for command in ("PartDesign_Extrude", "PartDesign_Pocket"):
            Gui.Selection.clearSelection()
            feature = self.start(command, preselect=True)
            self.accept()
            self.assertFalse(self.sketch.ViewObject.Visibility)
            original = self.definition(feature)
            Gui.Selection.addSelection(feature, "Face1")
            selected = self.selectionPaths()
            self.assertTrue(feature.ViewObject.doubleClicked())
            self.widget(QtGui.QPushButton, "padHighlightProfile").click()
            self.assertTrue(self.sketch.ViewObject.Visibility)
            self.assertEqual(self.definition(feature), original)
            Gui.Control.activeTaskDialog().reject()
            Gui.updateGui()
            self.assertFalse(self.sketch.ViewObject.Visibility)
            self.assertEqual(self.selectionPaths(), selected)
            self.assertTrue(feature.ViewObject.doubleClicked())
            self.widget(QtGui.QPushButton, "padHighlightProfile").click()
            self.accept()
            self.assertFalse(self.sketch.ViewObject.Visibility)
            self.assertEqual(self.definition(feature), original)

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

    def makeLimit(self, z):
        limit = self.doc.addObject("Part::Feature", "Limit")
        limit.Shape = Part.makePlane(20, 20)
        limit.Placement.Base.z = z
        self.doc.recompute()
        return limit

    def typeFaceText(self, name, text):
        field = self.widget(QtGui.QLineEdit, name)
        field.setText(text)
        field.textEdited.emit(text)
        Gui.updateGui()

    def editFaceText(self, name, limit):
        self.typeFaceText(name, limit.Label + ":Face1")

    def startTwoFaceLimits(self, command="PartDesign_Extrude"):
        upper, lower = self.makeLimit(14), self.makeLimit(1)
        feature = self.start(command, preselect=True)
        self.selectOperation("Union")
        self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(1)
        self.widget(QtGui.QComboBox, "changeMode").setCurrentIndex(3)
        self.editFaceText("lineFaceName", upper)
        self.widget(QtGui.QComboBox, "changeMode2").setCurrentIndex(3)
        self.editFaceText("lineFaceName2", lower)
        self.assertTrue(feature.isValid(), feature.getStatusString())
        return feature, upper, lower

    def makeDatumLimit(self, z):
        plane = self.body.newObject("PartDesign::Plane", "DatumLimit")
        plane.Placement.Base.z = z
        self.doc.recompute()
        return plane

    def testClearedAndMalformedFaceTextInvalidatesOnlyEditedSide(self):
        for command in ("PartDesign_Extrude", "PartDesign_Pocket"):
            feature, upper, lower = self.startTwoFaceLimits(command)
            for field, prop, limit, other, otherLimit in (
                ("lineFaceName", "UpToFace", upper, "UpToFace2", lower),
                ("lineFaceName2", "UpToFace2", lower, "UpToFace", upper),
            ):
                for text in ("", "MissingLimit:Face1", limit.Label + ":Fac", limit.Label + ":Face1:extra"):
                    with self.subTest(command=command, field=field, text=text):
                        self.typeFaceText(field, text)
                        self.assertIsNone(getattr(feature, prop))
                        self.assertEqual(getattr(feature, other), (otherLimit, ["Face1"]))
                        self.assertFalse(feature.isValid())
                        self.assertEqual(feature.Type, "UpToFace")
                        self.assertEqual(feature.Type2, "UpToFace")
                        self.assertTrue(Gui.Control.activeDialog())
                        self.editFaceText(field, limit)
                        self.assertTrue(feature.isValid(), feature.getStatusString())
            Gui.Control.activeTaskDialog().reject()
            Gui.Selection.clearSelection()

    def testMissingFaceNumberRetainsErrorAndCanBeCorrected(self):
        feature, upper, lower = self.startTwoFaceLimits()
        for field, prop, limit in (("lineFaceName", "UpToFace", upper),
                                   ("lineFaceName2", "UpToFace2", lower)):
            with self.subTest(field=field):
                self.typeFaceText(field, limit.Label + ":Face99999")
                self.assertEqual(getattr(feature, prop), (limit, ["Face99999"]))
                self.assertFalse(feature.isValid())
                self.editFaceText(field, limit)
                self.assertTrue(feature.isValid(), feature.getStatusString())

    def testInvalidFaceOKStaysOpenAndEditCancelRestoresLinks(self):
        feature, upper, lower = self.startTwoFaceLimits()
        self.accept()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.typeFaceText("lineFaceName2", "")
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertFalse(feature.isValid())
        Gui.Control.activeTaskDialog().reject()
        self.doc.recompute()
        self.assertEqual(feature.UpToFace, (upper, ["Face1"]))
        self.assertEqual(feature.UpToFace2, (lower, ["Face1"]))
        self.assertTrue(feature.isValid(), feature.getStatusString())
        self.assertEqual(self.body.Tip, feature)
        self.assertAlmostEqual(feature.Shape.Volume, 1064)

    def testDisabledPreviewChecksClearedLimitOnOKThenRepairs(self):
        feature, upper, lower = self.startTwoFaceLimits()
        self.widget(QtGui.QCheckBox, "checkBoxUpdateView").setChecked(False)
        self.typeFaceText("lineFaceName", "")
        self.assertIsNone(feature.UpToFace)
        self.assertEqual(feature.UpToFace2, (lower, ["Face1"]))
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertFalse(feature.isValid())
        self.editFaceText("lineFaceName", upper)
        self.accept()
        self.assertTrue(feature.isValid(), feature.getStatusString())
        self.assertEqual(feature.UpToFace, (upper, ["Face1"]))

    def testTypedDatumAndOriginPlanesUpdatePreviewBeforeOK(self):
        datum = self.makeDatumLimit(16)
        origin = next(obj for obj in self.body.Origin.OriginFeatures if obj.Name.startswith("XY_Plane"))
        for command in ("PartDesign_Extrude", "PartDesign_Pocket"):
            feature, upper, lower = self.startTwoFaceLimits(command)
            self.typeFaceText("lineFaceName", datum.Label)
            self.assertEqual(feature.UpToFace, (datum, [""]))
            self.assertEqual(feature.UpToFace2, (lower, ["Face1"]))
            self.assertTrue(feature.isValid(), feature.getStatusString())
            self.assertAlmostEqual(feature.Shape.Volume, 1096)
            self.typeFaceText("lineFaceName2", origin.Label)
            self.assertEqual(feature.UpToFace2, (origin, [""]))
            self.assertEqual(feature.UpToFace, (datum, [""]))
            self.assertTrue(feature.isValid(), feature.getStatusString())
            self.accept()
            self.assertEqual(feature.UpToFace, (datum, [""]))
            self.assertEqual(feature.UpToFace2, (origin, [""]))
            self.doc.undo()
            self.doc.recompute()
            Gui.Selection.clearSelection()

    def testTypedPlaneRepairUndoRedoAndSaveReopen(self):
        datum = self.makeDatumLimit(16)
        feature, upper, lower = self.startTwoFaceLimits()
        self.accept()
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.typeFaceText("lineFaceName", "MissingLimit")
        self.assertFalse(feature.isValid())
        self.typeFaceText("lineFaceName", datum.Label)
        self.assertTrue(feature.isValid(), feature.getStatusString())
        self.accept()
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(feature.UpToFace, (upper, ["Face1"]))
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(feature.UpToFace, (datum, [""]))
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "TypedPlane.FCStd")
            self.doc.saveCopy(path)
            restored = App.openDocument(path)
            try:
                recovered = restored.getObject(feature.Name)
                self.assertEqual(recovered.UpToFace[0].Name, datum.Name)
                self.assertEqual(recovered.UpToFace2[0].Name, lower.Name)
                recovered.UpToFace[0].Placement.Base.z = 17
                restored.recompute()
                self.assertTrue(recovered.isValid(), recovered.getStatusString())
                self.assertAlmostEqual(recovered.Shape.Volume, 1112)
            finally:
                App.closeDocument(restored.Name)

    def testExtentLabelsDescribeMeasuredLengthsForBothFeatureTypes(self):
        self.doc.removeObject(self.base.Name)
        for command in ("PartDesign_Extrude", "PartDesign_Pocket"):
            with self.subTest(command=command):
                feature = self.start(command, preselect=True)
                self.selectOperation("Union")
                self.quantity("lengthEdit", 6.0)
                self.quantity("lengthEdit2", 2.0)
                self.quantity("startOffsetEdit", 1.0)
                for mode, label, low, high in ((0, "Length", 6, 12),
                                              (1, "Side 1 length", 4, 12),
                                              (2, "Total length", 3, 9)):
                    self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(mode)
                    self.assertEqual(self.widget(QtGui.QLabel, "labelLength").text(), label)
                    self.assertEqual(self.widget(QtGui.QLabel, "labelLength2").text(), "Side 2 length")
                    self.assertTrue(feature.isValid(), feature.getStatusString())
                    # Pocket retains its opposite default axis around the sketch at z=5.
                    if command == "PartDesign_Pocket":
                        low, high = 10 - high, 10 - low
                    self.assertAlmostEqual(feature.Shape.BoundBox.ZMin, low)
                    self.assertAlmostEqual(feature.Shape.BoundBox.ZMax, high)
                    if mode == 2:
                        self.assertIn("half on each side", self.widget(QtGui.QWidget, "lengthEdit").toolTip())
                self.accept()
                self.assertTrue(feature.ViewObject.doubleClicked())
                Gui.updateGui()
                self.assertEqual(self.widget(QtGui.QLabel, "labelLength").text(), "Total length")
                Gui.Control.activeTaskDialog().reject()
                self.doc.undo()
                self.doc.recompute()
                Gui.Selection.clearSelection()

    def testTypedSecondFaceChangesOnlyItsOwnSideAndCancelRestoresIt(self):
        for command in ("PartDesign_Extrude", "PartDesign_Pocket"):
            with self.subTest(command=command):
                upper, lower, replacement = self.makeLimit(14), self.makeLimit(1), self.makeLimit(2)
                feature = self.start(command, preselect=True)
                self.selectOperation("Union")
                self.widget(QtGui.QComboBox, "sidesMode").setCurrentIndex(1)
                self.widget(QtGui.QComboBox, "changeMode").setCurrentIndex(3)
                self.editFaceText("lineFaceName", upper)
                self.widget(QtGui.QComboBox, "changeMode2").setCurrentIndex(3)
                self.editFaceText("lineFaceName2", lower)
                self.assertEqual(feature.UpToFace, (upper, ["Face1"]))
                self.assertEqual(feature.UpToFace2, (lower, ["Face1"]))
                self.assertTrue(feature.isValid(), feature.getStatusString())
                self.accept()
                self.assertTrue(feature.ViewObject.doubleClicked())
                Gui.updateGui()
                self.editFaceText("lineFaceName2", replacement)
                self.assertEqual(feature.UpToFace, (upper, ["Face1"]))
                self.assertEqual(feature.UpToFace2, (replacement, ["Face1"]))
                Gui.Control.activeTaskDialog().reject()
                self.doc.recompute()
                self.assertEqual(feature.UpToFace, (upper, ["Face1"]))
                self.assertEqual(feature.UpToFace2, (lower, ["Face1"]))
                self.doc.undo()
                self.doc.recompute()
                Gui.Selection.clearSelection()

    def testRemovedLimitingFaceCanBeRepairedInExistingEditor(self):
        feature = self.start(preselect=True)
        self.accept()
        limit = self.makeLimit(14)
        feature.Type = "UpToFace"
        feature.UpToFace = (limit, ["Face1"])
        self.doc.recompute()
        self.assertTrue(feature.isValid(), feature.getStatusString())
        self.doc.removeObject(limit.Name)
        self.doc.recompute()
        self.assertFalse(feature.isValid())
        replacement = self.makeLimit(16)
        self.assertTrue(feature.ViewObject.doubleClicked())
        Gui.updateGui()
        self.assertEqual(self.widget(QtGui.QComboBox, "changeMode").currentIndex(), 3)
        self.editFaceText("lineFaceName", replacement)
        self.assertEqual(feature.Type, "UpToFace")
        self.assertTrue(feature.isValid(), feature.getStatusString())
        self.accept()
        self.assertEqual(feature.UpToFace, (replacement, ["Face1"]))
        self.assertAlmostEqual(feature.Shape.Volume, 1096)
        replacement.Placement.Base.z = 17
        self.doc.recompute()
        self.assertAlmostEqual(feature.Shape.Volume, 1112)

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
