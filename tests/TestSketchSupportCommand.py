# SPDX-License-Identifier: LGPL-2.1-or-later
"""Owner-facing sketch support workflow using native, portable fixtures."""
import math
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide import QtWidgets
import SketchSupportGui as Editor
from BasicShapes.ShapeReferences import linked_shape


def make_fixture():
    doc = App.newDocument("SketchSupportWorkflow")
    doc.UndoMode = 1
    part = doc.addObject("App::Part", "Design")
    part.Placement = App.Placement(App.Vector(10, 20, 30), App.Rotation(App.Vector(1, 0, 0), 25))
    original = doc.addObject("Part::Plane", "OriginalPlane")
    replacement = doc.addObject("Part::Plane", "ReplacementPlane")
    for plane in (original, replacement):
        part.addObject(plane)
        plane.Length = plane.Width = 20
    replacement.Placement = App.Placement(App.Vector(4, 5, 10), App.Rotation(App.Vector(0, 1, 0), 60))
    sketch = doc.addObject("Sketcher::SketchObject", "Profile")
    part.addObject(sketch)
    geometry = sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
    sketch.addConstraint(Sketcher.Constraint("Radius", geometry, 2))
    sketch.AttachmentSupport = [(original, "Face1")]
    sketch.MapMode = "FlatFace"
    sketch.AttachmentOffset = App.Placement(App.Vector(1, 2, 3), App.Rotation(App.Vector(0, 0, 1), 15))
    result = doc.addObject("Part::Extrusion", "Result")
    part.addObject(result)
    result.Base = sketch
    result.DirMode = "Normal"
    result.LengthFwd = 5
    result.Solid = True
    doc.recompute()
    return doc


class TestSketchSupportCommand(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("SketcherWorkbench")
        self.doc = make_fixture()
        self.sketch = self.doc.Profile
        self.support = self.doc.ReplacementPlane
        Gui.Selection.clearSelection()

    def tearDown(self):
        for dialog in list(Editor._dialogs):
            dialog.close()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.sketch)
        Gui.runCommand("Sketcher_InspectSupport")
        Gui.updateGui()
        return Editor._dialogs[-1]

    def choose(self, dialog, support=None, face="Face1"):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(support or self.support, face)
        dialog.pick.click()

    def assertPlacementNear(self, first, second):
        for point in (App.Vector(), App.Vector(1, 0, 0), App.Vector(0, 1, 0), App.Vector(0, 0, 1)):
            self.assertLess((first.multVec(point) - second.multVec(point)).Length, 1e-6)

    def testMenuPreviewAndCloseLeaveModelUntouched(self):
        actions = [action for menu in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                   for action in menu.actions()]
        self.assertTrue(any("Inspect and change sketch support" in action.text() for action in actions))
        original = self.sketch.getGlobalPlacement()
        documents = set(App.listDocuments())
        dialog = self.launch()
        self.assertIn("OriginalPlane", dialog.current.text())
        self.choose(dialog)
        for index in (0, 1):
            dialog.policy.setCurrentIndex(index)
            dialog.previewButton.click()
            self.assertTrue(dialog.applyButton.isEnabled(), dialog.result.text())
            self.assertIn("Candidate world placement", dialog.result.text())
            self.assertPlacementNear(self.sketch.getGlobalPlacement(), original)
            self.assertEqual(self.sketch.AttachmentSupport[0][0], self.doc.OriginalPlane)
            self.assertEqual(set(App.listDocuments()), documents)
        dialog.close()
        self.assertPlacementNear(self.sketch.getGlobalPlacement(), original)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testWorldCommitUndoRedoAndReopen(self):
        original = self.sketch.getGlobalPlacement()
        center = linked_shape((self.doc.Result, [])).CenterOfMass
        dialog = self.launch()
        self.choose(dialog)
        dialog.policy.setCurrentIndex(1)
        dialog.previewButton.click()
        self.assertTrue(dialog.applyButton.isEnabled(), dialog.result.text())
        dialog.applyButton.click()
        self.assertIn("Reattached", dialog.result.text())
        self.assertEqual(self.sketch.AttachmentSupport[0][0], self.support)
        self.assertPlacementNear(self.sketch.getGlobalPlacement(), original)
        self.assertLess((linked_shape((self.doc.Result, [])).CenterOfMass - center).Length, 1e-6)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.sketch.AttachmentSupport[0][0], self.doc.OriginalPlane)
        self.doc.redo()
        self.doc.recompute()
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "SketchSupport.FCStd")
            self.doc.saveAs(filename)
            dialog.close()
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            self.assertEqual(self.doc.Profile.AttachmentSupport[0][0], self.doc.ReplacementPlane)
            self.assertAlmostEqual(self.doc.Result.Shape.Volume, math.pi * 4 * 5, places=5)
            self.assertPlacementNear(self.doc.Profile.getGlobalPlacement(), original)

    def testLocalRepairAndInvalidFaceRecovery(self):
        self.sketch.AttachmentSupport = [(self.doc.OriginalPlane, "Face99")]
        self.doc.recompute()
        offset = self.sketch.AttachmentOffset
        dialog = self.launch()
        self.choose(dialog)
        dialog.face.setText("Face99")
        dialog.previewButton.click()
        self.assertFalse(dialog.applyButton.isEnabled())
        self.assertIn("unavailable", dialog.result.text())
        dialog.face.setText("Face1")
        dialog.previewButton.click()
        self.assertTrue(dialog.applyButton.isEnabled(), dialog.result.text())
        dialog.applyButton.click()
        self.assertNotIn("Invalid", self.sketch.State)
        self.assertNotIn("Invalid", self.doc.Result.State)
        self.assertEqual(self.sketch.AttachmentSupport[0][0], self.support)
        self.assertPlacementNear(self.sketch.AttachmentOffset, offset)

    def testStalePreviewRequiresExplicitRefresh(self):
        dialog = self.launch()
        self.choose(dialog)
        dialog.previewButton.click()
        self.assertTrue(dialog.applyButton.isEnabled(), dialog.result.text())
        self.support.Placement.Base.z += 2
        self.doc.recompute()
        dialog.applyButton.click()
        self.assertFalse(dialog.applyButton.isEnabled())
        self.assertIn("Preview again", dialog.result.text())
        self.assertEqual(self.sketch.AttachmentSupport[0][0], self.doc.OriginalPlane)
        dialog.previewButton.click()
        self.assertTrue(dialog.applyButton.isEnabled(), dialog.result.text())
        dialog.applyButton.click()
        self.assertEqual(self.sketch.AttachmentSupport[0][0], self.support)

    def testCycleOccurrenceAndDocumentLifetime(self):
        dialog = self.launch()
        self.choose(dialog, self.doc.Result)
        dialog.previewButton.click()
        self.assertFalse(dialog.applyButton.isEnabled())
        self.assertIn("cycle", dialog.result.text())
        link = self.doc.addObject("App::Link", "Occurrence")
        link.setLink(self.support)
        self.doc.recompute()
        self.choose(dialog, link)
        self.assertIn("linked occurrence", dialog.result.text())
        self.choose(dialog)
        self.doc.removeObject(self.support.Name)
        self.assertIsNone(dialog.support)
        self.assertFalse(dialog.applyButton.isEnabled())
        App.closeDocument(self.doc.Name)
        self.assertTrue(dialog._closed)
        self.assertNotIn(dialog, Editor._dialogs)
