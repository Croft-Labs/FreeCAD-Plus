# SPDX-License-Identifier: LGPL-2.1-or-later
"""Existing native Measure task: semantics, picked-point provenance and persistence."""
from datetime import datetime
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

import FreeCAD as App
import FreeCADGui as Gui
import Measure
import Part
from PySide import QtWidgets


def make_fixture():
    doc = App.newDocument("MeasurementWorkflow")
    doc.UndoMode = 1
    first = doc.addObject("Part::Feature", "CircleA")
    first.Shape = Part.makeCircle(5)
    second = doc.addObject("Part::Feature", "CircleB")
    second.Shape = Part.makeCircle(5)
    second.Placement.Base.x = 20
    doc.recompute()
    return doc


def widget(cls, name):
    return Gui.getMainWindow().findChild(cls, name)


def open_measure(doc, mode, selections=None):
    Gui.Selection.clearSelection()
    if selections is None:
        selections = [(doc.CircleA, "Edge1", (5, 0, 0)),
                      (doc.CircleB, "Edge1", (15, 0, 0))]
    for obj, sub, point in selections:
        Gui.Selection.addSelection(obj.Document.Name, obj.Name, sub, *point)
    Gui.runCommand("Std_Measure")
    Gui.updateGui()
    combo = widget(QtWidgets.QComboBox, "measureMode")
    if combo is None:
        raise AssertionError("Native Measure task did not open")
    combo.setCurrentIndex(combo.findData(mode))
    Gui.updateGui()
    return next(obj for obj in doc.Objects if obj.isDerivedFrom("Measure::MeasureBase"))


def task_button(kind):
    for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox):
        button = box.button(kind)
        if button and button.isVisible() and box.button(QtWidgets.QDialogButtonBox.Apply):
            return button
    raise AssertionError("Measure task button not found")


def close_measure():
    if Gui.Control.activeDialog():
        task_button(QtWidgets.QDialogButtonBox.Abort).click()
        Gui.updateGui()


class TestMeasurementContext(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()

    def tearDown(self):
        close_measure()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def testCircleCentreDistanceAndUnits(self):
        measure = open_measure(self.doc, "DISTANCE")
        self.assertEqual(measure.TypeId, "Measure::MeasureDistance")
        self.assertAlmostEqual(measure.Distance.Value, 20)
        # The actual edge clearance is 10; the native circle measurement uses centres.
        self.assertAlmostEqual(self.doc.CircleA.Shape.distToShape(self.doc.CircleB.Shape)[0], 10)
        meaning = widget(QtWidgets.QLabel, "measureMeaning").text()
        self.assertIn("circle/arc centres", meaning)
        self.assertIn("World frame", meaning)
        operands = widget(QtWidgets.QLabel, "measureOperands").text()
        self.assertIn("CircleA.Edge1", operands)
        self.assertIn("CircleB.Edge1", operands)
        units = widget(QtWidgets.QComboBox, "measureUnit")
        units.setCurrentIndex(units.findData("in"))
        self.assertEqual(measure.DisplayUnit, "in")
        self.assertIn("in", widget(QtWidgets.QLineEdit, "measureResult").text())
        self.assertAlmostEqual(measure.Distance.Value, 20)

    def testSnapshotSaveMoveUndoAndReopen(self):
        measure = open_measure(self.doc, "DISTANCEFREE")
        self.assertEqual(measure.TypeId, "Measure::MeasureDistanceDetached")
        self.assertAlmostEqual(measure.Distance.Value, 10)
        self.assertIn("Point snapshot", widget(QtWidgets.QLabel, "measureMeaning").text())
        self.assertIn("not minimum", widget(QtWidgets.QLabel, "measureMeaning").text())
        captured, sources = measure.CaptureTime, list(measure.CaptureSources)
        self.assertIsNotNone(datetime.fromisoformat(captured.replace("Z", "+00:00")).tzinfo)
        self.assertEqual(len(sources), 2)
        self.assertTrue(sources[0].endswith("CircleA.Edge1"))
        self.assertIn("does not follow", measure.UpdatePolicy)
        name = measure.Name
        task_button(QtWidgets.QDialogButtonBox.Apply).click()
        close_measure()
        measure = self.doc.getObject(name)
        self.assertIsNotNone(measure)
        self.assertEqual(measure.OutList, [])
        self.doc.CircleB.Placement.Base.x = 40
        self.doc.recompute()
        self.assertAlmostEqual(measure.Distance.Value, 10)
        self.assertEqual(measure.CaptureTime, captured)
        self.doc.openTransaction("Edit snapshot point")
        measure.Position2 = App.Vector(25, 0, 0)
        self.doc.commitTransaction()
        self.assertEqual(measure.CaptureTime, "")
        self.assertEqual(measure.CaptureSources, [])
        self.assertAlmostEqual(measure.Distance.Value, 20)
        self.doc.undo()
        self.assertEqual(measure.CaptureTime, captured)
        self.assertEqual(measure.CaptureSources, sources)
        self.assertAlmostEqual(measure.Distance.Value, 10)
        self.doc.redo()
        self.assertEqual(measure.CaptureTime, "")
        self.doc.undo()
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Snapshot.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            restored = self.doc.getObject(name)
            self.assertEqual(restored.CaptureTime, captured)
            self.assertEqual(restored.CaptureSources, sources)
            self.assertEqual(restored.OutList, [])
            self.assertAlmostEqual(restored.Distance.Value, 10)

    def testAssociativeDistanceSaveTracksSourceMove(self):
        measure = open_measure(self.doc, "DISTANCE")
        name = measure.Name
        task_button(QtWidgets.QDialogButtonBox.Apply).click()
        close_measure()
        self.doc.CircleB.Placement.Base.x = 30
        self.doc.recompute()
        measure = self.doc.getObject(name)
        self.assertNotIn("Invalid", measure.State)
        self.assertAlmostEqual(measure.Distance.Value, 30)
        self.assertEqual({o.Name for o in measure.OutList}, {"CircleA", "CircleB"})

    def testCancelDiscardsPreviewAndClearsOperands(self):
        original = {obj.Name for obj in self.doc.Objects}
        open_measure(self.doc, "DISTANCEFREE")
        Gui.Selection.clearSelection()
        Gui.updateGui()
        self.assertIn("Select geometry", widget(QtWidgets.QLabel, "measureOperands").text())
        self.assertNotIn("Captured (UTC)", widget(QtWidgets.QLabel, "measureMeaning").text())
        self.assertFalse(task_button(QtWidgets.QDialogButtonBox.Apply).isEnabled())
        close_measure()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, original)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testOccurrenceWorldPointsAndUnsignedDeltas(self):
        link = self.doc.addObject("App::Link", "PlacedCircle")
        link.setLink(self.doc.CircleA)
        link.LinkPlacement.Base = App.Vector(20, 10, 0)
        self.doc.recompute()
        measure = open_measure(self.doc, "DISTANCEFREE", [
            (self.doc.CircleA, "Edge1", (5, 0, 0)), (link, "Edge1", (25, 10, 0))])
        self.assertAlmostEqual(measure.Distance.Value, 500 ** 0.5)
        self.assertAlmostEqual(measure.DistanceX.Value, 20)
        self.assertAlmostEqual(measure.DistanceY.Value, 10)
        self.assertIn("PlacedCircle.Edge1", widget(QtWidgets.QLabel, "measureOperands").text())
        self.assertTrue(any("PlacedCircle.Edge1" in source for source in measure.CaptureSources))

    def testGeometricCentreExplainsDensityAndOldCaptureIsUnknown(self):
        box = self.doc.addObject("Part::Box", "Box")
        box.Length, box.Width, box.Height = 10, 20, 30
        box.Placement.Base = App.Vector(100, 0, 0)
        self.doc.recompute()
        measure = open_measure(self.doc, "CENTEROFMASS", [(box, "", (100, 0, 0))])
        self.assertAlmostEqual(measure.CenterOfMass.x, 105)
        self.assertAlmostEqual(measure.CenterOfMass.y, 10)
        self.assertIn("does not apply material density", widget(QtWidgets.QLabel, "measureMeaning").text())
        close_measure()
        snapshot = self.doc.addObject("Measure::MeasureDistanceDetached", "Uncaptured")
        snapshot.Position1, snapshot.Position2 = App.Vector(), App.Vector(3, 4, 0)
        self.doc.recompute()
        self.assertEqual(snapshot.CaptureTime, "")
        self.assertEqual(snapshot.CaptureSources, [])
        self.assertAlmostEqual(snapshot.Distance.Value, 5)
        # Simulate a legacy native file whose detached measurement predates provenance fields.
        with tempfile.TemporaryDirectory() as directory:
            current = Path(directory) / "Current.FCStd"
            legacy = Path(directory) / "Legacy.FCStd"
            self.doc.saveAs(str(current))
            with zipfile.ZipFile(current) as source, zipfile.ZipFile(legacy, "w") as target:
                for entry in source.infolist():
                    payload = source.read(entry.filename)
                    if entry.filename == "Document.xml":
                        xml = ET.fromstring(payload)
                        for props in xml.iter("Properties"):
                            for prop in list(props):
                                if prop.get("name") in ("UpdatePolicy", "CaptureTime", "CaptureSources"):
                                    props.remove(prop)
                            if "Count" in props.attrib:
                                props.set("Count", str(sum(child.tag == "Property" for child in props)))
                        payload = ET.tostring(xml, encoding="utf-8", xml_declaration=True)
                    target.writestr(entry, payload)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(str(legacy))
            restored = self.doc.Uncaptured
            self.assertEqual(restored.CaptureTime, "")
            self.assertEqual(restored.CaptureSources, [])
            self.assertIn("does not follow", restored.UpdatePolicy)
            self.assertAlmostEqual(restored.Distance.Value, 5)
