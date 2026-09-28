# SPDX-License-Identifier: LGPL-2.1-or-later

"""Pad creation and editing through the task panel (requires a GUI build)."""

import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtGui


class TestPadTaskPanel(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("PadTaskPanelTest")
        self.body = self.doc.addObject("PartDesign::Body", "Body")
        Gui.activateWorkbench("PartDesignWorkbench")
        Gui.activeDocument().activeView().setActiveObject("pdbody", self.body)
        self.sketch = self.makeSketch("Profile", 10)
        self.other = self.makeSketch("OtherProfile", 5)
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)

    def makeSketch(self, name, width):
        sketch = self.body.newObject("Sketcher::SketchObject", name)
        points = [(0, 0), (width, 0), (width, 10), (0, 10)]
        for start, end in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(App.Vector(*start, 0), App.Vector(*end, 0)))
        self.doc.recompute()
        return sketch

    def widget(self, cls, name):
        widget = Gui.getMainWindow().findChild(cls, name)
        self.assertIsNotNone(widget, name)
        return widget

    def button(self, name):
        return self.widget(QtGui.QPushButton, name)

    def profileList(self):
        return self.widget(QtGui.QListWidget, "padProfileList")

    def startPad(self, preselect=False):
        if preselect:
            Gui.Selection.addSelection(self.sketch)
        Gui.runCommand("PartDesign_Pad")
        Gui.updateGui()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIsNotNone(self.doc.getObject("Pad"))
        self.profileList()  # Creation must open the parameter editor, not a picker.
        return self.doc.Pad

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertFalse(Gui.Control.activeDialog())

    def testCreateWithoutPreselectionAndUndo(self):
        pad = self.startPad()
        self.assertIsNone(pad.Profile)
        self.assertEqual(self.profileList().count(), 0)
        self.assertTrue(self.button("padSelectProfile").isChecked())
        Gui.Selection.addSelection(self.sketch)
        self.assertEqual(pad.Profile[0], self.sketch)
        self.assertEqual(self.profileList().count(), 1)
        self.assertAlmostEqual(pad.Shape.Volume, 1000)
        self.accept()
        self.doc.undo()
        self.assertIsNone(self.doc.getObject("Pad"))
        self.doc.redo()
        self.assertAlmostEqual(self.doc.Pad.Shape.Volume, 1000)

    def testPreselectionAndEditUseSameProfileControls(self):
        pad = self.startPad(preselect=True)
        self.assertEqual(self.profileList().count(), 1)
        self.accept()
        Gui.activeDocument().setEdit(pad.Name)
        Gui.updateGui()
        self.assertEqual(self.profileList().count(), 1)
        self.button("padClearProfile").click()
        self.assertIsNone(pad.Profile)
        Gui.Selection.addSelection(self.other)
        self.assertEqual(pad.Profile[0], self.other)
        self.assertAlmostEqual(pad.Shape.Volume, 500)
        self.accept()
        self.doc.undo()
        self.assertEqual(pad.Profile[0], self.sketch)
        self.assertAlmostEqual(pad.Shape.Volume, 1000)

    def testAccumulateAndRemoveIndividualCurves(self):
        pad = self.startPad()
        for index in range(1, 5):
            # Normal viewport clicks clear global selection. Already collected
            # curves must remain in the task list until explicitly removed.
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(self.sketch, "Edge%d" % index)
        self.assertEqual(set(pad.Profile[1]), {"Edge1", "Edge2", "Edge3", "Edge4"})
        self.assertEqual(self.profileList().count(), 4)
        self.assertAlmostEqual(pad.Shape.Volume, 1000)
        self.profileList().item(0).setSelected(True)
        self.button("padRemoveProfile").click()
        self.assertEqual(self.profileList().count(), 3)
        self.assertNotIn("Edge1", pad.Profile[1])
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.sketch, "Edge1")
        self.assertAlmostEqual(pad.Shape.Volume, 1000)
        self.accept()

    def testCancelNewPadRestoresBodyTip(self):
        previous_tip = self.body.Tip
        self.startPad()
        Gui.Control.activeTaskDialog().reject()
        self.assertIsNone(self.doc.getObject("Pad"))
        self.assertEqual(self.body.Tip, previous_tip)

    def testCancelEditRestoresProfileAndVisibility(self):
        pad = self.startPad(preselect=True)
        self.accept()
        self.other.ViewObject.Visibility = False
        Gui.activeDocument().setEdit(pad.Name)
        self.button("padClearProfile").click()
        Gui.Selection.addSelection(self.other)
        self.assertTrue(self.other.ViewObject.Visibility)
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual(pad.Profile[0], self.sketch)
        self.assertAlmostEqual(pad.Shape.Volume, 1000)
        self.assertFalse(self.other.ViewObject.Visibility)

    def testEmptyProfileCannotBeAccepted(self):
        pad = self.startPad()
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIsNone(pad.Profile)
        self.assertTrue(self.button("padSelectProfile").isChecked())

    def testNoSketchStillOpensPadEditor(self):
        self.doc.removeObject(self.sketch.Name)
        self.doc.removeObject(self.other.Name)
        self.doc.recompute()
        pad = self.startPad()
        self.assertIsNone(pad.Profile)
        Gui.Control.activeTaskDialog().reject()
        self.assertIsNone(self.doc.getObject("Pad"))

    def testIncompleteCurveCannotBeAccepted(self):
        pad = self.startPad()
        Gui.Selection.addSelection(self.sketch, "Edge1")
        self.assertEqual(self.profileList().count(), 1)
        Gui.Control.activeTaskDialog().accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertFalse(pad.isValid())

    def testDuplicateSelectionDoesNotDuplicateProfileItems(self):
        self.startPad()
        Gui.Selection.addSelection(self.sketch, "Edge1")
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.sketch, "Edge1")
        self.assertEqual(self.profileList().count(), 1)

    def testFaceSelectionFromExistingSolid(self):
        base = self.body.newObject("PartDesign::AdditiveBox", "Base")
        base.Length = 10
        base.Width = 10
        base.Height = 5
        self.doc.recompute()
        top_index, _ = max(
            enumerate(base.Shape.Faces, 1), key=lambda item: item[1].CenterOfMass.z
        )
        pad = self.startPad()
        Gui.Selection.addSelection(base, "Face%d" % top_index)
        self.assertEqual(pad.Profile[0], base)
        self.assertEqual(self.profileList().count(), 1)
        self.assertGreater(pad.Shape.Volume, base.Shape.Volume)
        self.accept()

    def testDifferentProfileRequiresExplicitClear(self):
        pad = self.startPad()
        Gui.Selection.addSelection(self.sketch)
        Gui.Selection.addSelection(self.other)
        self.assertEqual(pad.Profile[0], self.sketch)
        self.button("padClearProfile").click()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.other)
        self.assertEqual(pad.Profile[0], self.other)

    def testDependentFeatureCannotBecomeProfile(self):
        pad = self.startPad(preselect=True)
        self.accept()
        dependent = self.body.newObject("PartDesign::AdditiveBox", "Dependent")
        dependent.Length = 2
        dependent.Width = 2
        dependent.Height = 2
        self.doc.recompute()
        self.assertEqual(dependent.BaseFeature, pad)
        Gui.activeDocument().setEdit(pad.Name)
        self.button("padClearProfile").click()
        Gui.Selection.addSelection(dependent, "Face1")
        self.assertIsNone(pad.Profile)

    def testRejectOtherBodyAndSelfReferences(self):
        other_body = self.doc.addObject("PartDesign::Body", "OtherBody")
        foreign = other_body.newObject("Sketcher::SketchObject", "ForeignProfile")
        foreign.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        pad = self.startPad()
        Gui.Selection.addSelection(foreign)
        Gui.Selection.addSelection(pad)
        self.assertIsNone(pad.Profile)
        Gui.Selection.addSelection(self.sketch)
        self.assertEqual(pad.Profile[0], self.sketch)

    def testSwitchBetweenProfileAndReferenceSelection(self):
        self.startPad()
        Gui.Selection.addSelection(self.sketch)
        start_mode = self.widget(QtGui.QComboBox, "startMode")
        start_mode.setCurrentIndex(2)  # Reference start
        reference = self.widget(QtGui.QToolButton, "buttonStartReference")
        if not reference.isChecked():
            reference.click()
        self.assertFalse(self.button("padSelectProfile").isChecked())
        self.button("padSelectProfile").click()
        self.assertFalse(reference.isChecked())
        self.assertTrue(self.button("padSelectProfile").isChecked())
