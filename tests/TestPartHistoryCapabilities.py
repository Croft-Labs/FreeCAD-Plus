# SPDX-License-Identifier: LGPL-2.1-or-later
"""Phase 7 design probes using existing native types, not a production history layer."""
import math
import os
from pathlib import Path
import unittest

import FreeCAD as App
import Part
import Sketcher
from BasicShapes.ShapeReferences import linked_shape


class TestPartHistoryCapabilities(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("PartHistoryCapabilities")
        self.doc.UndoMode = 1
        self.part = self.doc.addObject("App::Part", "ModelPart")

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def sketch(self, name, centers):
        sketch = self.doc.addObject("Sketcher::SketchObject", name)
        self.part.addObject(sketch)
        for x in centers:
            index = sketch.addGeometry(Part.Circle(App.Vector(x, 0, 0), App.Vector(0, 0, 1), 2))
            sketch.addConstraint(Sketcher.Constraint("Radius", index, 2))
        return sketch

    def extrude(self, name, sketch, length, reverse=False):
        feature = self.doc.addObject("Part::Extrusion", name)
        self.part.addObject(feature)
        feature.Base = sketch
        feature.DirMode = "Custom"
        feature.Dir = App.Vector(0, 0, 1)
        feature.LengthFwd = length
        feature.Solid = True
        feature.Reversed = reverse
        return feature

    def model(self):
        sketch = self.sketch("SharedSketch", [0])
        first = self.extrude("First", sketch, 3)
        second = self.extrude("Second", sketch, 5, True)
        twin = self.sketch("TwinSketch", [20, 30])
        multi = self.extrude("MultiResult", twin, 4)
        later = self.doc.addObject("Part::Compound", "CombinedResults")
        self.part.addObject(later)
        later.Links = [first, second, multi]
        self.doc.recompute()
        return sketch, first, second, multi, later

    def checkModel(self):
        self.assertFalse(any(o.isDerivedFrom("PartDesign::Body") for o in self.doc.Objects))
        sketch = self.doc.SharedSketch
        self.assertEqual(sketch.getParentGeoFeatureGroup(), self.doc.ModelPart)
        self.assertEqual(self.doc.First.Base, sketch)
        self.assertEqual(self.doc.Second.Base, sketch)
        self.assertEqual(len(self.doc.First.Shape.Solids), 1)
        self.assertEqual(len(self.doc.Second.Shape.Solids), 1)
        self.assertEqual(len(self.doc.MultiResult.Shape.Solids), 2)
        self.assertEqual(len(self.doc.CombinedResults.Shape.Solids), 4)
        self.assertTrue(self.doc.CombinedResults.Shape.isValid())
        expected = sum(o.Shape.Volume for o in
                       (self.doc.First, self.doc.Second, self.doc.MultiResult))
        self.assertAlmostEqual(self.doc.CombinedResults.Shape.Volume, expected, places=6)

    def testIndependentSharedSketchAndMultipleResults(self):
        sketch, first, second, multi, later = self.model()
        self.checkModel()
        sketch.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        self.assertAlmostEqual(first.Shape.Volume, math.pi * 9 * 3, places=6)
        self.assertAlmostEqual(second.Shape.Volume, math.pi * 9 * 5, places=6)
        self.assertAlmostEqual(multi.Shape.Volume, math.pi * 4 * 8, places=6)
        self.checkModel()

    def testRecomputeTransactionsAndNativePersistence(self):
        sketch, first, second, multi, later = self.model()
        original = later.Shape.Volume
        self.doc.openTransaction("Change shared radius")
        sketch.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        edited = later.Shape.Volume
        self.assertGreater(edited, original)
        self.doc.commitTransaction()
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(later.Shape.Volume, original, places=6)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(later.Shape.Volume, edited, places=6)
        self.doc.openTransaction("Canceled edit")
        sketch.setDatum(0, App.Units.Quantity("4 mm"))
        self.doc.recompute()
        self.doc.abortTransaction()
        self.doc.recompute()
        self.assertAlmostEqual(later.Shape.Volume, edited, places=6)
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "PartHistoryNativeProof.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.doc.recompute()
        self.checkModel()
        self.assertAlmostEqual(self.doc.CombinedResults.Shape.Volume, edited, places=6)

    def testNativeLinksKeepIndependentPlacements(self):
        sketch, first, second, multi, later = self.model()
        links = []
        for x in (40, 70):
            link = self.doc.addObject("App::Link", "Occurrence")
            link.setLink(first)
            link.LinkPlacement = App.Placement(App.Vector(x, 0, 0), App.Rotation())
            links.append(link)
        self.doc.recompute()
        sketch.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        for link, x in zip(links, (40, 70)):
            shape = linked_shape((link, []))
            self.assertAlmostEqual(shape.Volume, first.Shape.Volume, places=6)
            self.assertAlmostEqual(shape.BoundBox.XMin, x - 3, places=6)
        self.assertAlmostEqual(first.Shape.BoundBox.XMin, -3, places=6)

    def testBodyOwnershipCannotBeSharedByReparenting(self):
        sketch = self.sketch("OwnedSketch", [0])
        first = self.doc.addObject("PartDesign::Body", "BodyA")
        second = self.doc.addObject("PartDesign::Body", "BodyB")
        with self.assertRaisesRegex(RuntimeError, "single GeoFeatureGroup"):
            first.addObject(sketch)
        self.assertIn(sketch, self.part.Group)
        self.part.removeObject(sketch)
        first.addObject(sketch)
        self.assertIn(sketch, first.Group)
        # Depending on the native entry point, moving between Bodies can be
        # rejected or transfer ownership. Neither outcome provides shared ownership.
        try:
            second.addObject(sketch)
        except RuntimeError:
            self.assertIn(sketch, first.Group)
            self.assertNotIn(sketch, second.Group)
        else:
            self.assertNotIn(sketch, first.Group)
            self.assertIn(sketch, second.Group)
