# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native known-distance fixtures and nonmutating inspection lifecycle."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import SurfaceDeviation as Check
import SurfaceDeviationGui as UI


def planes(doc):
    sample = doc.addObject("Part::Feature", "SampledFace")
    sample.Shape = Part.makePlane(10, 10)
    reference = doc.addObject("Part::Feature", "ReferenceFace")
    reference.Shape = Part.makePlane(30, 30, App.Vector(-10, -10, -2))
    doc.recompute()
    return sample, reference


class TestSurfaceDeviation(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("DeviationTest")
        self.doc.UndoMode = 1
        Gui.Selection.clearSelection()
        self.dialogs = []

    def tearDown(self):
        for dialog in self.dialogs:
            if not dialog._closed:
                dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def refs(self, a, b):
        return Check.FaceReference(a, "Face1"), Check.FaceReference(b, "Face1")

    def dialog(self, a, b):
        dialog = UI.DeviationDialog(Gui.getMainWindow())
        self.dialogs.append(dialog)
        for obj, role in ((a, "sampled"), (b, "reference")):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj, "Face1")
            dialog.capture(role)
        return dialog

    def testKnownPlanarOffsetAndPlacement(self):
        a, b = planes(self.doc)
        for obj in (a, b):
            obj.Placement = App.Placement(App.Vector(13, -4, 7), App.Rotation(App.Vector(1, 1, 0), 38)).multiply(obj.Placement)
        self.doc.recompute()
        originals = [obj.Shape.exportBrepToString() for obj in (a, b)]
        count, undo = len(self.doc.Objects), self.doc.UndoCount
        report = Check.inspect(*self.refs(a, b), grid=7, scale=4)
        self.assertEqual(len(report["points"]), 49)
        self.assertEqual((report["outside"], report["unresolved"]), (0, 0))
        for value in report["distances"]:
            self.assertAlmostEqual(value, 2, places=7)
        point = App.Vector(*report["points"][0])
        self.assertLess(Part.Vertex(point).distToShape(a.Shape)[0], 1e-7)
        self.assertEqual(originals, [obj.Shape.exportBrepToString() for obj in (a, b)])
        self.assertEqual((len(self.doc.Objects), self.doc.UndoCount), (count, undo))

    def testCurvedOffsetAndDirectionIsExplicit(self):
        a, b = planes(self.doc)
        a.Shape = Part.makeCylinder(10, 10).Faces[0]
        b.Shape = Part.makeCylinder(12, 10).Faces[0]
        self.doc.recompute()
        report = Check.inspect(*self.refs(a, b), grid=9, scale=1)
        self.assertEqual(report["saturated"], 81)
        for value in report["distances"]:
            self.assertAlmostEqual(value, 2, places=7)
        a.Shape = Part.makePlane(10, 10)
        b.Shape = Part.makePlane(2, 2, App.Vector(4, 4, 0))
        self.doc.recompute()
        forward = Check.inspect(*self.refs(a, b), grid=5)
        reverse = Check.inspect(*self.refs(b, a), grid=5)
        self.assertGreater(forward["maximum"], 4)
        self.assertAlmostEqual(reverse["maximum"], 0, places=7)

    def testTiltAndTrimmedHole(self):
        a, b = planes(self.doc)
        b.Shape = Part.makePlane(40, 40, App.Vector(-10, -10, 0))
        a.Placement = App.Placement(App.Vector(), App.Rotation(App.Vector(0, 1, 0), 20))
        self.doc.recompute()
        report = Check.inspect(*self.refs(a, b), grid=7, scale=4)
        self.assertGreater(report["maximum"] - report["minimum"], 2)
        for point, value in zip(report["points"], report["distances"]):
            self.assertAlmostEqual(value, abs(point[2]), places=7)
        a.Placement = App.Placement()
        a.Shape = Part.makePlane(10, 10).cut(Part.makePlane(4, 4, App.Vector(3, 3, 0)))
        self.doc.recompute()
        report = Check.inspect(*self.refs(a, b), grid=5)
        self.assertGreater(report["outside"], 0)
        self.assertEqual(len(report["points"]) + report["outside"], 25)
        self.assertEqual(report["unresolved"], 0)

    def testIncompleteNativeSamplingIsReported(self):
        a, b = planes(self.doc)
        vertex = Part.Vertex
        calls = [0]
        def intermittent(point):
            calls[0] += 1
            if calls[0] == 1:
                raise RuntimeError("Injected distance failure")
            return vertex(point)
        with patch.object(Check.Part, "Vertex", side_effect=intermittent):
            report = Check.inspect(*self.refs(a, b), grid=3)
        self.assertEqual(report["unresolved"], 1)
        self.assertEqual(len(report["points"]), 8)
        self.assertIn("Injected distance failure", report["errors"][0])

    def testInputAndSettingsGuards(self):
        a, b = planes(self.doc)
        refs = self.refs(a, b)
        for options in ((2, 1), (26, 1), (4.5, 1), (True, 1), (5, 0), (5, float("nan"))):
            with self.subTest(options=options), self.assertRaises(ValueError):
                Check.inspect(*refs, *options)
        with self.assertRaises(ValueError):
            Check.inspect(refs[0], refs[0])
        with self.assertRaises(ValueError):
            Check.FaceReference(a, "Edge1")
        link = self.doc.addObject("App::Link", "LinkedFace")
        link.setLink(a)
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Check.FaceReference(link, "Face1")
        parent = self.doc.addObject("App::Part", "Parent")
        parent.addObject(a)
        self.doc.recompute()
        with self.assertRaises(ValueError):
            refs[0].face()
        with self.assertRaises(ValueError):
            Check.FaceReference(a, "Face1")

    def testChangedRemovedAndPendingInputs(self):
        a, b = planes(self.doc)
        refs = self.refs(a, b)
        a.Placement.Base.z = 1
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "changed"):
            Check.inspect(*refs)
        refs = self.refs(a, b)
        App.setActiveTransaction("Pending owner edit")
        try:
            with self.assertRaisesRegex(ValueError, "transaction"):
                Check.inspect(*refs)
        finally:
            App.closeActiveTransaction(True)
        self.doc.removeObject(a.Name)
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "removed"):
            Check.inspect(*refs)

    def testMapCancelChangeAndSettings(self):
        a, b = planes(self.doc)
        dialog = self.dialog(a, b)
        scene = Gui.activeDocument().activeView().getSceneGraph()
        baseline, count, undo = scene.getNumChildren(), len(self.doc.Objects), self.doc.UndoCount
        dialog.grid.setValue(7)
        dialog.scale.setValue(4)
        dialog.check()
        self.assertIsNotNone(dialog.report, dialog.status.text())
        self.assertEqual(scene.getNumChildren(), baseline + 1)
        self.assertIn("Sample maximum: 2 mm", dialog.results.toPlainText())
        dialog.save()
        self.assertEqual(Check.load_settings(), (7, 4))
        dialog.scale.setValue(3)
        self.assertIsNone(dialog.overlay)
        self.assertEqual(scene.getNumChildren(), baseline)
        dialog.check()
        a.Placement.Base.z = 1
        self.doc.recompute()
        self.assertIsNone(dialog.overlay)
        dialog.check()
        self.assertIsNone(dialog.report)
        self.assertIn("changed", dialog.status.text())
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(a, "Face1")
        dialog.capture("sampled")
        dialog.check()
        self.assertIsNotNone(dialog.overlay, dialog.status.text())
        dialog.reject()
        self.assertEqual(scene.getNumChildren(), baseline)
        self.assertEqual((len(self.doc.Objects), self.doc.UndoCount), (count, undo))

    def testNativeCommandDocumentCloseAndReopen(self):
        a, b = planes(self.doc)
        Gui.runCommand("Part_SurfaceDeviation")
        self.assertTrue(UI._dialogs)
        dialog = UI._dialogs[-1]
        self.assertEqual(dialog.windowTitle(), "Sampled face deviation")
        dialog.reject()
        dialog = self.dialog(a, b)
        dialog.check()
        self.assertIsNotNone(dialog.overlay, dialog.status.text())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Surfaces.FCStd"
            self.doc.saveAs(str(path))
            App.closeDocument(self.doc.Name)
            self.assertTrue(dialog._closed)
            self.assertIsNone(dialog.overlay)
            self.doc = App.openDocument(str(path))
            a, b = self.doc.SampledFace, self.doc.ReferenceFace
            report = Check.inspect(*self.refs(a, b), grid=3)
            self.assertAlmostEqual(report["maximum"], 2)
            self.assertEqual(len(self.doc.Objects), 2)
            self.assertFalse(any("Deviation" in obj.Name for obj in self.doc.Objects))

    def testWholeBodyResultAndActiveDocumentGuard(self):
        a, b = planes(self.doc)
        body = self.doc.addObject("PartDesign::Body", "Body")
        tip = body.newObject("PartDesign::Feature", "TipShape")
        tip.Shape = Part.makeBox(10, 10, 5)
        self.doc.recompute()
        top = max(range(1, 7), key=lambda i: body.Shape.Faces[i - 1].CenterOfMass.z)
        report = Check.inspect(Check.FaceReference(body, "Face" + str(top)),
                               Check.FaceReference(b, "Face1"), grid=3, scale=10)
        self.assertAlmostEqual(report["minimum"], 7)
        self.assertEqual(body.Tip, tip)
        dialog = self.dialog(a, b)
        dialog.check()
        self.assertIsNotNone(dialog.overlay, dialog.status.text())
        other = App.newDocument("Other")
        Gui.updateGui()
        self.assertIsNone(dialog.overlay)
        dialog.check()
        self.assertIsNone(dialog.report)
        self.assertIn("Activate", dialog.status.text())
        foreign, _ = planes(other)
        with self.assertRaisesRegex(ValueError, "same document"):
            Check.inspect(Check.FaceReference(a, "Face1"), Check.FaceReference(foreign, "Face1"))
