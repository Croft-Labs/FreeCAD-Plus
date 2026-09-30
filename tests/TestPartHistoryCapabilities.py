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

    def testMixedDefinitionGeometryAndChildOccurrences(self):
        own = self.doc.addObject("Part::Box", "OwnSolid")
        self.part.addObject(own)
        own.Length, own.Width, own.Height = 2, 2, 2
        child = self.doc.addObject("App::Part", "ChildDefinition")
        child_box = self.doc.addObject("Part::Box", "ChildSolid")
        child.addObject(child_box)
        child_box.Length, child_box.Width, child_box.Height = 1, 1, 1
        nested = self.doc.addObject("App::Link", "ChildOccurrence")
        self.part.addObject(nested)
        nested.setLink(child)
        nested.LinkPlacement.Base = App.Vector(5, 0, 0)
        assemblies = [self.doc.addObject("App::Part", "Assembly") for _ in range(2)]
        occurrences = []
        for assembly, x in ((assemblies[0], 20), (assemblies[0], 40), (assemblies[1], 60)):
            link = self.doc.addObject("App::Link", "MixedOccurrence")
            assembly.addObject(link)
            link.setLink(self.part)
            link.LinkPlacement.Base = App.Vector(x, 0, 0)
            occurrences.append(link)
        self.doc.recompute()
        for length in (2, 3):
            own.Length = length
            self.doc.recompute()
            for link, x in zip(occurrences, (20, 40, 60)):
                shape = linked_shape((link, []))
                self.assertAlmostEqual(shape.Volume, length * 4 + 1)
                self.assertAlmostEqual(shape.BoundBox.XMin, x)
                self.assertAlmostEqual(shape.BoundBox.XMax, x + 6)
            self.assertEqual(nested.LinkedObject, child)
            self.assertIn(own, self.part.Group)
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "MixedDefinitionProof.FCStd"
        names = [o.Name for o in occurrences]
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.doc.recompute()
        for name in names:
            self.assertAlmostEqual(linked_shape((self.doc.getObject(name), [])).Volume, 13)

    def testUniqueDefinitionRemapsInputsAndPreservesOtherOccurrences(self):
        import sys
        import uuid
        sys.path.insert(0, str(Path(__file__).parent / "prototypes"))
        from UniqueDefinition import make_unique
        sketch = self.sketch("UniqueSketch", [0])
        extrusion = self.extrude("UniqueExtrusion", sketch, 3)
        for obj in (self.part, sketch, extrusion):
            obj.addProperty("App::PropertyString", "SemanticIdentity", "Prototype")
            obj.SemanticIdentity = str(uuid.uuid4())
        links = []
        for x in (20, 40):
            link = self.doc.addObject("App::Link", "SharedOccurrence")
            link.setLink(self.part)
            link.LinkPlacement.Base = App.Vector(x, 0, 0)
            links.append(link)
        self.doc.recompute()
        copied = make_unique(links[0])
        copied_name = copied.Name
        copied_sketch = next(o for o in copied.Group if o.isDerivedFrom("Sketcher::SketchObject"))
        copied_extrude = next(o for o in copied.Group if o.isDerivedFrom("Part::Extrusion"))
        self.assertEqual(copied_extrude.Base, copied_sketch)
        self.assertNotEqual(copied_sketch, sketch)
        old_ids = {o.SemanticIdentity for o in (self.part, sketch, extrusion)}
        new_ids = {o.SemanticIdentity for o in [copied] + list(copied.Group)}
        self.assertFalse(old_ids & new_ids)
        self.assertEqual({o.SourceIdentity for o in [copied] + list(copied.Group)}, old_ids)
        self.assertEqual(links[1].LinkedObject, self.part)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(links[0].LinkedObject, self.part)
        self.assertIsNone(self.doc.getObject(copied_name))
        self.doc.redo()
        self.doc.recompute()
        copied = links[0].LinkedObject
        self.assertEqual({o.SemanticIdentity for o in [copied] + list(copied.Group)}, new_ids)
        sketch.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        self.assertAlmostEqual(linked_shape((links[0], [])).Volume, math.pi * 4 * 3, places=6)
        self.assertAlmostEqual(linked_shape((links[1], [])).Volume, math.pi * 9 * 3, places=6)
        self.assertAlmostEqual(links[0].LinkPlacement.Base.x, 20)
        saved_identity = copied.SemanticIdentity
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "UniqueDefinitionProof.FCStd"
        names = [o.Name for o in links]
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.doc.recompute()
        first, second = [self.doc.getObject(n) for n in names]
        self.assertNotEqual(first.LinkedObject, second.LinkedObject)
        self.assertEqual(first.LinkedObject.SemanticIdentity, saved_identity)
        self.assertAlmostEqual(linked_shape((first, [])).Volume, math.pi * 4 * 3, places=6)
        self.assertAlmostEqual(linked_shape((second, [])).Volume, math.pi * 9 * 3, places=6)

    def testUniqueRejectsUnsupportedDefinitionWithoutMutation(self):
        import sys
        sys.path.insert(0, str(Path(__file__).parent / "prototypes"))
        from UniqueDefinition import make_unique
        box = self.doc.addObject("Part::Box", "UnsupportedMember")
        self.part.addObject(box)
        occurrence = self.doc.addObject("App::Link", "UnchangedOccurrence")
        occurrence.setLink(self.part)
        self.doc.recompute()
        before = {o.Name for o in self.doc.Objects}
        with self.assertRaisesRegex(ValueError, "one independent sketch"):
            make_unique(occurrence)
        self.assertEqual({o.Name for o in self.doc.Objects}, before)
        self.assertEqual(occurrence.LinkedObject, self.part)

    def parameterModel(self):
        parameters = self.doc.addObject("App::FeaturePython", "Parameters")
        self.part.addObject(parameters)
        parameters.addProperty("App::PropertyLength", "Width", "Dimensions")
        parameters.addProperty("App::PropertyAngle", "Tilt", "Dimensions")
        parameters.Width = "1 in"
        parameters.Tilt = "30 deg"
        first = self.doc.addObject("Part::Box", "ParameterizedBase")
        second = self.doc.addObject("Part::Box", "ParameterizedLid")
        self.part.addObject(first)
        self.part.addObject(second)
        from prototypes.NamedParameters import set_length_expression
        set_length_expression(first, "Length", "Parameters.Width")
        set_length_expression(second, "Length", "Parameters.Width + 2 mm")
        self.doc.recompute()
        return parameters, first, second

    def testNamedUnitAwareParameterDrivesMultipleFeatures(self):
        parameters, first, second = self.parameterModel()
        self.assertAlmostEqual(first.Length.Value, 25.4)
        self.assertAlmostEqual(second.Length.Value, 27.4)
        self.assertAlmostEqual(first.Shape.BoundBox.XLength, 25.4)
        occurrence = self.doc.addObject("App::Link", "ParameterOccurrence")
        occurrence.setLink(self.part)
        occurrence.Placement.Base = App.Vector(100, 0, 0)
        self.doc.recompute()
        self.doc.openTransaction("Change named width and parameter label")
        parameters.Label = "Enclosure dimensions"
        parameters.Width = "30 mm"
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertAlmostEqual(first.Length.Value, 30)
        self.assertAlmostEqual(second.Length.Value, 32)
        self.assertEqual(occurrence.LinkedObject, self.part)
        self.assertEqual(occurrence.Placement.Base, App.Vector(100, 0, 0))
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(first.Length.Value, 25.4)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(first.Length.Value, 30)
        filename = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "NamedParameterProof.FCStd"
        self.doc.saveAs(str(filename))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(filename))
        self.doc.recompute()
        self.doc.Parameters.Width = "2 in"
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.ParameterizedBase.Length.Value, 50.8)
        self.assertAlmostEqual(self.doc.ParameterizedLid.Shape.BoundBox.XLength, 52.8)
        self.assertEqual(self.doc.ParameterOccurrence.LinkedObject, self.doc.ModelPart)
        self.assertEqual(self.doc.ParameterOccurrence.Placement.Base, App.Vector(100, 0, 0))

    def testParameterExpressionFailuresAbortWithoutLosingValidModel(self):
        parameters, first, second = self.parameterModel()
        original = first.ExpressionEngine
        for target, prop, expression in (
            (first, "Length", "Parameters.Tilt"),
            (parameters, "Width", "ParameterizedBase.Length"),
        ):
            self.doc.openTransaction("Invalid parameter expression")
            from prototypes.NamedParameters import set_length_expression
            with self.assertRaises(Exception) as caught:
                set_length_expression(target, prop, expression)
            self.assertRegex(str(caught.exception), "(?i)length|cyclic|cycle")
            self.doc.abortTransaction()
            self.doc.recompute()
            self.assertEqual(first.ExpressionEngine, original)
            self.assertTrue(all("Invalid" not in obj.State for obj in (parameters, first, second)))
            self.assertAlmostEqual(first.Shape.BoundBox.XLength, 25.4)
            self.assertAlmostEqual(second.Length.Value, 27.4)
        parameters.Width = "40 mm"
        self.doc.recompute()
        self.assertAlmostEqual(first.Length.Value, 40)
        self.assertAlmostEqual(second.Length.Value, 42)

    def testParameterDependenciesDistinguishMatchingLabelsAcrossParts(self):
        parameters, first, second = self.parameterModel()
        other_part = self.doc.addObject("App::Part", "OtherPart")
        other_parameters = self.doc.addObject("App::FeaturePython", "OtherParameters")
        other_parameters.addProperty("App::PropertyLength", "Width", "Dimensions")
        other_parameters.Width = "12 mm"
        other_part.addObject(other_parameters)
        parameters.Label = other_parameters.Label = "Dimensions"
        other_box = self.doc.addObject("Part::Box", "OtherBox")
        other_part.addObject(other_box)
        from prototypes.NamedParameters import set_length_expression
        set_length_expression(other_box, "Length", "OtherParameters.Width")
        self.doc.recompute()
        # Native object-level dependency lookup is a candidate index for where-used,
        # not proof of property-level references or implicit part-local name lookup.
        self.assertIn(first, parameters.InList)
        self.assertIn(second, parameters.InList)
        self.assertNotIn(other_box, parameters.InList)
        self.assertIn(other_box, other_parameters.InList)
        parameters.Width = "40 mm"
        self.doc.recompute()
        self.assertAlmostEqual(first.Length.Value, 40)
        self.assertAlmostEqual(second.Length.Value, 42)
        self.assertAlmostEqual(other_box.Length.Value, 12)
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ParameterScopeProof.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.doc.recompute()
        self.doc.OtherParameters.Width = "18 mm"
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.OtherBox.Shape.BoundBox.XLength, 18)
        self.assertAlmostEqual(self.doc.ParameterizedBase.Shape.BoundBox.XLength, 40)
        self.assertIn(self.doc.OtherBox, self.doc.OtherParameters.InList)
        self.assertNotIn(self.doc.OtherBox, self.doc.Parameters.InList)

    def testInvalidParameterGeometryRecoversAfterAbortAndUndo(self):
        parameters, first, second = self.parameterModel()
        original_expression = first.ExpressionEngine
        self.doc.openTransaction("Invalid shared dimension")
        parameters.Width = "0 mm"
        self.doc.recompute()
        # A dimension can be unit-correct but geometrically invalid. Consumers must
        # inspect recompute state rather than assuming a retained Shape is current.
        self.assertIn("Invalid", first.State)
        self.doc.abortTransaction()
        self.doc.recompute()
        self.assertAlmostEqual(parameters.Width.Value, 25.4)
        self.assertEqual(first.ExpressionEngine, original_expression)
        for obj, length in ((first, 25.4), (second, 27.4)):
            self.assertNotIn("Invalid", obj.State)
            self.assertAlmostEqual(obj.Shape.BoundBox.XLength, length)
        self.doc.openTransaction("Valid shared dimension")
        parameters.Width = "35 mm"
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertAlmostEqual(first.Shape.BoundBox.XLength, 35)
        self.assertAlmostEqual(second.Shape.BoundBox.XLength, 37)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(first.Shape.BoundBox.XLength, 25.4)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(first.Shape.BoundBox.XLength, 35)
        self.assertNotIn("Invalid", first.State)

    def testNamedAngleExpressionUnitsAndRecovery(self):
        from prototypes.NamedParameters import set_angle_expression
        parameters, first, second = self.parameterModel()
        wedge = self.doc.addObject("Part::Cylinder", "AngularConsumer")
        self.part.addObject(wedge)
        set_angle_expression(wedge, "Angle", "Parameters.Tilt * 2")
        self.doc.recompute()
        self.assertAlmostEqual(wedge.Angle.Value, 60)
        self.assertAlmostEqual(wedge.Shape.Volume, math.pi * wedge.Radius.Value ** 2 * wedge.Height.Value / 6)
        original = wedge.ExpressionEngine
        for expression in ("Parameters.Width", "42", "MissingParameter.Angle"):
            with self.assertRaises(Exception):
                set_angle_expression(wedge, "Angle", expression)
            self.assertEqual(wedge.ExpressionEngine, original)
            self.assertAlmostEqual(wedge.Angle.Value, 60)
        with self.assertRaisesRegex(ValueError, "angle properties"):
            set_angle_expression(first, "Length", "Parameters.Tilt")
        self.doc.openTransaction("Change named angle")
        parameters.Tilt = "1 rad"
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertAlmostEqual(wedge.Angle.Value, 360 / math.pi)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(wedge.Angle.Value, 60)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(wedge.Angle.Value, 360 / math.pi)
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "AngularParameterProof.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.doc.Parameters.Tilt = "45 deg"
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.AngularConsumer.Angle.Value, 90)
        self.assertNotIn("Invalid", self.doc.AngularConsumer.State)

    def testNativeParameterRenamePropagatesToConsumers(self):
        parameters, first, second = self.parameterModel()
        self.doc.openTransaction("Rename shared width")
        parameters.renameProperty("Width", "PanelWidth")
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertIn("PanelWidth", parameters.PropertiesList)
        for obj in (first, second):
            self.assertNotIn("Invalid", obj.State)
            self.assertIn("Parameters.PanelWidth", str(obj.ExpressionEngine))
        self.doc.undo()
        self.doc.recompute()
        self.assertIn("Width", parameters.PropertiesList)
        for obj in (first, second):
            self.assertNotIn("Invalid", obj.State)
            self.assertIn("Parameters.Width", str(obj.ExpressionEngine))
        self.doc.redo()
        self.doc.recompute()
        self.assertIn("PanelWidth", parameters.PropertiesList)
        parameters.PanelWidth = "31 mm"
        self.doc.recompute()
        self.assertAlmostEqual(first.Length.Value, 31)
        self.assertAlmostEqual(second.Length.Value, 33)
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "RenamedParameterProof.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.doc.Parameters.PanelWidth = "36 mm"
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.ParameterizedBase.Shape.BoundBox.XLength, 36)
        self.assertAlmostEqual(self.doc.ParameterizedLid.Shape.BoundBox.XLength, 38)
        for obj in (self.doc.ParameterizedBase, self.doc.ParameterizedLid):
            self.assertNotIn("Invalid", obj.State)
            self.assertIn("Parameters.PanelWidth", str(obj.ExpressionEngine))

    def testParameterRenameFailuresPreserveOwnedExpressionAndCallerTransaction(self):
        from prototypes.NamedParameters import rename_parameter, set_length_expression
        parameters, first, second = self.parameterModel()
        set_length_expression(parameters, "Width", "10 mm + 15.4 mm")
        self.doc.recompute()
        original = parameters.ExpressionEngine
        consumers = [obj.ExpressionEngine for obj in (first, second)]
        for name in ("Tilt", "Invalid name", ""):
            with self.assertRaises(Exception):
                rename_parameter(parameters, "Width", name)
            self.assertEqual(parameters.ExpressionEngine, original)
            self.assertEqual([obj.ExpressionEngine for obj in (first, second)], consumers)
            self.assertFalse(self.doc.HasPendingTransaction)
            self.assertAlmostEqual(first.Shape.BoundBox.XLength, 25.4)
            self.assertNotIn("Invalid", first.State)
        old_label = parameters.Label
        self.doc.openTransaction("Unrelated caller edit")
        parameters.Label = "Pending caller edit"
        with self.assertRaisesRegex(ValueError, "current transaction"):
            rename_parameter(parameters, "Width", "PanelWidth")
        self.assertTrue(self.doc.HasPendingTransaction)
        self.assertEqual(parameters.Label, "Pending caller edit")
        self.assertEqual(parameters.ExpressionEngine, original)
        self.doc.abortTransaction()
        self.doc.recompute()
        self.assertEqual(parameters.Label, old_label)
        rename_parameter(parameters, "Width", "PanelWidth")
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertIn("PanelWidth", str(parameters.ExpressionEngine))
        self.assertAlmostEqual(first.Length.Value, 25.4)

    def testParameterRenameTracksLabelReferencesAndOwnedFormula(self):
        from prototypes.NamedParameters import rename_parameter, set_length_expression
        parameters, first, second = self.parameterModel()
        parameters.Label = "Enclosure dimensions"
        set_length_expression(parameters, "Width", "10 mm + 15.4 mm")
        set_length_expression(first, "Length", "<<Enclosure dimensions>>.Width")
        self.doc.recompute()
        rename_parameter(parameters, "Width", "PanelWidth")
        self.assertIn("PanelWidth", str(parameters.ExpressionEngine))
        for obj in (first, second):
            self.assertIn("PanelWidth", str(obj.ExpressionEngine))
            self.assertNotIn("Invalid", obj.State)
        self.doc.undo()
        self.doc.recompute()
        self.assertIn("Width", parameters.PropertiesList)
        self.assertAlmostEqual(first.Length.Value, 25.4)
        self.doc.redo()
        self.doc.recompute()
        parameters.Label = "Renamed dimensions"
        self.doc.recompute()
        self.assertNotIn("Invalid", first.State)
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "LabelParameterRenameProof.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        set_length_expression(self.doc.Parameters, "PanelWidth", "40 mm")
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.ParameterizedBase.Shape.BoundBox.XLength, 40)
        self.assertAlmostEqual(self.doc.ParameterizedLid.Shape.BoundBox.XLength, 42)
        self.assertNotIn("Invalid", self.doc.ParameterizedBase.State)
