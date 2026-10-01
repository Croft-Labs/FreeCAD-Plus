# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native fitted face extension, review recovery and persistence (F066)."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import ExtendFaceReview as Review
import ExtendFaceGui as UI
from PySide import QtCore


def settle():
    Gui.updateGui()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(150, loop.quit)
    loop.exec_()


def values(**changes):
    result = dict(ExtendUNeg=0.05, ExtendUPos=0.05, ExtendVNeg=0.05,
                  ExtendVPos=0.05, Tolerance=0.001, SampleU=16, SampleV=16)
    result.update(changes)
    return result


class TestExtendFaceReview(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("SurfaceWorkbench")
        self.doc = App.newDocument("ExtendReviewTest")
        self.doc.UndoMode = 1
        self.source = self.doc.addObject("Part::Feature", "Sheet")
        self.source.Shape = Part.makePlane(10, 8)
        self.doc.recompute()
        self.dialogs = []

    def tearDown(self):
        for dialog in self.dialogs:
            if not dialog.closed:
                dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()

    def ref(self):
        return Review.Input(self.source, "Face1")

    def snapshot(self):
        return (self.source.Shape.exportBrepToString(), tuple(self.source.Placement.toMatrix().A),
                self.source.Visibility, self.doc.UndoCount, tuple(obj.Name for obj in self.doc.Objects))

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.source, "Face1")
        Gui.runCommand("Surface_ExtendFace")
        settle()
        dialog = UI._dialogs[-1]
        self.dialogs.append(dialog)
        return dialog

    def testPlanarPreviewIsReadOnlyAndUsesParameterPercentages(self):
        self.source.Placement.Base = App.Vector(10, 20, 30)
        self.doc.recompute()
        before = self.snapshot()
        documents = set(App.listDocuments())
        preview = Review.probe(self.ref(), values())
        shape = preview["shape"]
        self.assertAlmostEqual(shape.Area, 96.8, places=5)
        for value, expected in ((shape.BoundBox.XMin, 9.5), (shape.BoundBox.XMax, 20.5),
                                (shape.BoundBox.YMin, 19.6), (shape.BoundBox.YMax, 28.4),
                                (shape.BoundBox.ZMin, 30)):
            self.assertAlmostEqual(value, expected, places=5)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(documents, set(App.listDocuments()))

    def testCurvedQuarterCylinderFit(self):
        self.source.Shape = Part.makeCylinder(5, 10, App.Vector(), App.Vector(0, 0, 1), 90)
        self.doc.recompute()
        original = self.source.Shape.exportBrepToString()
        shape = Review.probe(self.ref(), values(Tolerance=0.0001))["shape"]
        self.assertTrue(shape.isValid())
        self.assertEqual(len(shape.Faces), 1)
        self.assertFalse(shape.Solids)
        self.assertAlmostEqual(shape.Area, 5 * 10 * 3.141592653589793 / 2 * 1.21, delta=0.1)
        self.assertEqual(original, self.source.Shape.exportBrepToString())

    def testTrimLoopsAreNotRetainedByRectangularFit(self):
        hole = Part.Face(Part.Wire([Part.makeCircle(1, App.Vector(5, 4, 0))]))
        self.source.Shape = self.source.Shape.cut(hole)
        self.doc.recompute()
        self.assertEqual(len(self.source.Shape.Faces[0].Wires), 2)
        shape = Review.probe(self.ref(), values(ExtendUNeg=0, ExtendUPos=0, ExtendVNeg=0, ExtendVPos=0))["shape"]
        self.assertEqual(len(shape.Faces[0].Wires), 1)
        self.assertAlmostEqual(shape.Area, 80, places=5)
        self.assertEqual(len(self.source.Shape.Faces[0].Wires), 2)

    def testNativeCommandPreviewCorrectionAndCancel(self):
        before = self.snapshot()
        dialog = self.launch()
        dialog.fields["ExtendUNeg"].setValue(-50)
        dialog.fields["ExtendUPos"].setValue(-50)
        dialog.previewButton.click()
        self.assertIn("nonempty", dialog.message.text())
        self.assertFalse(dialog.createButton.isEnabled())
        self.assertEqual(before, self.snapshot())
        dialog.fields["ExtendUPos"].setValue(5)
        dialog.previewButton.click()
        self.assertTrue(dialog.createButton.isEnabled(), dialog.message.text())
        self.assertIsNotNone(dialog.ghost)
        dialog.cancelButton.click()
        self.assertIsNone(dialog.ghost)
        self.assertEqual(before, self.snapshot())

    def testAcceptedNativeFeatureUndoRedoSourceEditAndReopen(self):
        dialog = self.launch()
        dialog.previewButton.click()
        self.assertTrue(dialog.createButton.isEnabled(), dialog.message.text())
        dialog.createButton.click()
        result = dialog.result
        self.assertIsNotNone(result, dialog.message.text())
        self.assertEqual(result.TypeId, "Surface::Extend")
        self.assertEqual(result.Face, (self.source, ["Face1"]))
        self.assertTrue(self.source.Visibility)
        name = result.Name
        self.doc.undo()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo()
        result = self.doc.getObject(name)
        self.assertAlmostEqual(result.Shape.Area, 96.8, places=5)
        consumer = self.doc.addObject("Part::Extrusion", "Downstream")
        consumer.Base = result
        consumer.Dir = App.Vector(0, 0, 2)
        consumer.Solid = True
        self.source.Shape = Part.makePlane(20, 8)
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Area, 193.6, places=5)
        self.assertAlmostEqual(consumer.Shape.Volume, 387.2, places=4)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Extended.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.assertEqual(self.doc.Extend.Face[0].Name, "Sheet")
            self.assertAlmostEqual(self.doc.Extend.Shape.Area, 193.6, places=5)
            self.assertAlmostEqual(self.doc.Downstream.Shape.Volume, 387.2, places=4)

    def testChangedSourceAndSettingsInvalidateReview(self):
        dialog = self.launch()
        dialog.previewButton.click()
        self.assertTrue(dialog.createButton.isEnabled(), dialog.message.text())
        dialog.fields["ExtendVPos"].setValue(10)
        self.assertFalse(dialog.createButton.isEnabled())
        dialog.previewButton.click()
        preview = dialog.previewed
        self.source.Placement.Base = App.Vector(5, 0, 0)
        self.doc.recompute()
        self.assertFalse(dialog.createButton.isEnabled())
        with self.assertRaisesRegex(ValueError, "source changed"):
            Review.create(preview)
        dialog.previewButton.click()
        self.assertIn("source changed", dialog.message.text())
        self.assertEqual(len(self.doc.Objects), 1)

    def testInvalidNativeDomainAndToleranceRecover(self):
        result = self.doc.addObject("Surface::Extend", "Extend")
        Review.configure(result, self.source, "Face1", values())
        result.Tolerance = 0
        self.doc.recompute()
        self.assertIn("Invalid", result.State)
        result.Tolerance = 0.001
        result.ExtendUNeg = result.ExtendUPos = -0.5
        self.doc.recompute()
        self.assertIn("Invalid", result.State)
        result.ExtendUPos = 0.1
        self.doc.recompute()
        self.assertNotIn("Invalid", result.State)
        self.assertTrue(result.Shape.isValid())
        result.SampleU = 12
        result.SampleV = 14
        self.doc.recompute()
        self.assertNotIn("Touched", result.State)

    def testUnsupportedInputsAndInvalidSettingsRefused(self):
        with self.assertRaises(ValueError):
            Review.Input(self.source, "Edge1")
        parent = self.doc.addObject("App::Part", "Container")
        parent.addObject(self.source)
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "Nested"):
            self.ref()
        for changed in (dict(Tolerance=0), dict(Tolerance=float("nan")), dict(SampleU=3),
                        dict(SampleV=65), dict(ExtendUPos=float("inf"))):
            with self.assertRaises(ValueError):
                Review.settings(values(**changed))

    def testFailedCommitRollsBackAndKeepsReviewRecoverable(self):
        dialog = self.launch()
        dialog.previewButton.click()
        self.assertTrue(dialog.createButton.isEnabled(), dialog.message.text())
        before = self.snapshot()
        original = Review.checked_shape

        def fail_owner_result(result):
            if result.Document == self.doc:
                raise ValueError("Injected post-creation failure")
            return original(result)

        with patch.object(Review, "checked_shape", side_effect=fail_owner_result):
            dialog.createButton.click()
        self.assertFalse(dialog.closed)
        self.assertIn("post-creation failure", dialog.message.text())
        self.assertEqual(before, self.snapshot())
        dialog.previewButton.click()
        dialog.createButton.click()
        self.assertIsNotNone(dialog.result, dialog.message.text())
