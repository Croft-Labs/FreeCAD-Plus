# SPDX-License-Identifier: LGPL-2.1-or-later

"""Boolean switching on an extrusion must preserve its identity and geometry inputs."""

import os
import tempfile
import unittest

import FreeCAD as App
import Part


class TestExtrude(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("ExtrudeOperationTest")
        self.doc.UndoMode = 1

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def makeExtrude(self, type_id="PartDesign::Pad", reference=True):
        body = self.doc.addObject("PartDesign::Body", "Body")
        base = body.newObject("PartDesign::AdditiveBox", "Base")
        base.Length = base.Width = base.Height = 10
        sketch = body.newObject("Sketcher::SketchObject", "Profile")
        points = [(2, 2), (6, 2), (6, 6), (2, 6)]
        for start, end in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(App.Vector(*start, 0), App.Vector(*end, 0)))
        sketch.Placement.Base.z = 5
        self.doc.recompute()
        feature = body.newObject(type_id, "Extrusion")
        feature.Profile = sketch
        if reference:
            feature.ReferenceAxis = (sketch, ["N_Axis"])
        feature.setExpression("Length", "7 mm")
        self.doc.recompute()
        return feature

    def testSwitchOperationPreservesIdentityDirectionAndExpressions(self):
        for type_id in ("PartDesign::Pad", "PartDesign::Pocket"):
            for reference in (False, True):
                with self.subTest(type_id=type_id, reference=reference):
                    feature = self.makeExtrude(type_id, reference)
                    name = feature.Name
                    direction = feature.Direction
                    profile = feature.Profile
                    axis = feature.ReferenceAxis
                    expressions = feature.ExpressionEngine
                    dependent = self.doc.addObject("App::FeaturePython", "Dependent")
                    dependent.addProperty("App::PropertyLink", "Source")
                    dependent.Source = feature
                    for operation, volume in (("Subtraction", 920), ("Union", 1032), ("Common", 80)):
                        feature.Operation = operation
                        self.doc.recompute()
                        self.assertTrue(feature.isValid(), feature.getStatusString())
                        self.assertAlmostEqual(feature.Shape.Volume, volume)
                        self.assertLess((feature.Direction - direction).Length, 1e-9)
                        self.assertEqual(feature.Profile, profile)
                        self.assertEqual(feature.ReferenceAxis, axis)
                        self.assertEqual(feature.ExpressionEngine, expressions)
                        self.assertEqual(feature.TypeId, type_id)
                        self.assertEqual(feature.Name, name)
                        self.assertEqual(dependent.Source, feature)

    def testSwitchPreservesCustomDirectionAndSecondSide(self):
        feature = self.makeExtrude()
        feature.UseCustomVector = True
        feature.Direction = App.Vector(0, 0, 1)
        feature.SideType = "Two sides"
        feature.Length2 = 2
        self.doc.recompute()
        for operation in ("Subtraction", "Union"):
            feature.Operation = operation
            self.doc.recompute()
            self.assertTrue(feature.isValid(), feature.getStatusString())

            self.assertEqual(feature.Direction, App.Vector(0, 0, 1))
            self.assertEqual(feature.SideType, "Two sides")
            self.assertEqual(feature.Length2.Value, 2)

    def testThroughAllWithoutBaseFailsAndCanRecover(self):
        body = self.doc.addObject("PartDesign::Body", "EmptyBody")
        sketch = body.newObject("Sketcher::SketchObject", "Circle")
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        feature = body.newObject("PartDesign::Pad", "NoBase")
        feature.Profile = sketch
        feature.Type = "ThroughAll"
        self.doc.recompute()
        self.assertFalse(feature.isValid())
        feature.Type = "Length"
        self.doc.recompute()
        self.assertTrue(feature.isValid(), feature.getStatusString())

    def testExtentNamesRemainDistinctWithoutChangingLegacyIndices(self):
        for type_id, legacy in (("PartDesign::Pad", "UpToLast"), ("PartDesign::Pocket", "ThroughAll")):
            feature = self.makeExtrude(type_id)
            feature.Type = 1
            self.assertEqual(feature.Type, legacy)
            for extent in ("UpToLast", "ThroughAll"):
                feature.Type = extent
                for operation in ("Union", "Subtraction"):
                    feature.Operation = operation
                    self.doc.recompute()
                    self.assertEqual(feature.Type, extent)
                    self.assertTrue(feature.isValid(), feature.getStatusString())

    def testSubtractWithoutBaseFailsAndCanRecover(self):
        for type_id in ("PartDesign::Pad", "PartDesign::Pocket"):
            body = self.doc.addObject("PartDesign::Body", "EmptyBody")
            sketch = body.newObject("Sketcher::SketchObject", "Circle")
            sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
            feature = body.newObject(type_id, "NoBase")
            feature.Profile = sketch
            feature.Operation = "Subtraction"
            self.doc.recompute()
            self.assertFalse(feature.isValid())
            feature.Operation = "Union"
            self.doc.recompute()
            self.assertTrue(feature.isValid(), feature.getStatusString())

    def testOperationUndoRedo(self):
        feature = self.makeExtrude()
        self.doc.openTransaction("Change extrusion operation")
        feature.Operation = "Subtraction"
        self.doc.recompute()
        self.doc.commitTransaction()
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(feature.Operation, "Union")
        self.assertAlmostEqual(feature.Shape.Volume, 1032)
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(feature.Operation, "Subtraction")
        self.assertAlmostEqual(feature.Shape.Volume, 920)

    def roundTrip(self):
        with tempfile.TemporaryDirectory(prefix="freecad-plus-extrude-") as directory:
            path = os.path.join(directory, "extrude.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.doc.recompute()

    def testSwitchedOperationsSurviveSaveReopen(self):
        pad = self.makeExtrude()
        pocket = self.makeExtrude("PartDesign::Pocket")
        pad.Operation = "Subtraction"
        pocket.Operation = "Union"
        self.doc.recompute()
        names = pad.Name, pocket.Name
        self.roundTrip()
        for name, operation, volume in zip(names, ("Subtraction", "Union"), (920, 1032)):
            feature = self.doc.getObject(name)
            self.assertEqual(feature.Operation, operation)
            self.assertAlmostEqual(feature.Shape.Volume, volume)

    def testLegacyRestrictedOperationListsRestoreWithoutChangingMeaning(self):
        pad = self.makeExtrude()
        pocket = self.makeExtrude("PartDesign::Pocket")
        common = self.makeExtrude("PartDesign::Pocket")
        pad.Operation = ["Union"]
        for feature in (pocket, common):
            feature.Operation = ["Subtraction", "Common"]
        common.Operation = "Common"
        self.doc.recompute()
        expected = [(feature.Name, feature.Operation, feature.Shape.Volume)
                    for feature in (pad, pocket, common)]
        self.roundTrip()
        for name, operation, volume in expected:
            feature = self.doc.getObject(name)
            self.assertEqual(feature.Operation, operation)
            self.assertAlmostEqual(feature.Shape.Volume, volume)
            self.assertIn("Union", feature.getEnumerationsOfProperty("Operation"))
            self.assertIn("Subtraction", feature.getEnumerationsOfProperty("Operation"))
