# SPDX-License-Identifier: LGPL-2.1-or-later
"""Focused G1.3 fixtures; run inside FreeCAD with PLUS_TEST_DIR set."""
import hashlib
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad_plus import document as component, editing
from freecad_plus.conversion import convert_file, ConversionError


class TestLegacyConversion(unittest.TestCase):
    def setUp(self):
        if "PLUS_TEST_DIR" not in os.environ:
            self.skipTest("Set PLUS_TEST_DIR to an isolated validation directory")
        self.output = Path(os.environ["PLUS_TEST_DIR"])
        self.before = set(App.listDocuments())

    def tearDown(self):
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)

    def source(self, name):
        doc = App.newDocument(name)
        doc.UndoMode = 1
        return doc, self.output / (name + ".FCStd"), self.output / (name + ".cadprt")

    def test_native_body_preserves_editability_and_live_source(self):
        doc, source, target = self.source("LegacyBody")
        body = doc.addObject("PartDesign::Body", "PlateBody")
        body.Placement = App.Placement(App.Vector(12, 8, 4), App.Rotation(App.Vector(0, 0, 1), 25))
        sketch = body.newObject("Sketcher::SketchObject", "BaseSketch")
        plane = next(o for o in body.Origin.OriginFeatures if o.Name.startswith("XY_Plane"))
        sketch.AttachmentSupport = [(plane, ("",))]
        sketch.MapMode = "FlatFace"
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 3), False)
        pad = body.newObject("PartDesign::Pad", "Extrusion")
        pad.Profile = sketch
        pad.addProperty("App::PropertyLength", "DesignLength")
        pad.DesignLength = 5
        pad.setExpression("Length", "DesignLength * 2")
        doc.recompute()
        sketch.Visibility = False
        doc.saveAs(str(source))
        identities = {o.Name: [o.TypeId, o.ID, o.Label] for o in doc.Objects}
        matrix = list(body.getGlobalPlacement().toMatrix().A)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        # Deliberately leave a different unsaved edit open; conversion reads disk.
        pad.DesignLength = 9
        doc.recompute()
        converted, report = convert_file(source, target)
        self.assertEqual(report["result"], "native-preserved")
        self.assertEqual(report["warnings"], [])
        self.assertEqual(pad.DesignLength.Value, 9)
        self.assertTrue(Gui.getDocument(doc.Name).Modified)
        self.assertEqual(doc.FileName, str(source))
        root = component.validate(converted)
        self.assertEqual(root.PlusSchema, 2)
        self.assertEqual(len(root.Definitions), 1)
        self.assertIsNone(converted.getObject("Part001"))
        self.assertNotEqual(str(doc.Uid), str(converted.Uid))
        self.assertEqual(report["source_uid"], str(doc.Uid))
        self.assertEqual(report["converted_uid"], str(converted.Uid))
        for name, expected in identities.items():
            obj = converted.getObject(name)
            self.assertEqual([obj.TypeId, obj.ID, obj.Label], expected)
        self.assertEqual(converted.Extrusion.Profile[0], converted.BaseSketch)
        self.assertEqual(converted.BaseSketch.AttachmentSupport[0][0].Name, plane.Name)
        self.assertEqual(converted.BaseSketch.MapMode, "FlatFace")
        self.assertEqual(list(converted.PlateBody.getGlobalPlacement().toMatrix().A), matrix)
        self.assertAlmostEqual(converted.Extrusion.Length.Value, 10)
        self.assertAlmostEqual(converted.Extrusion.Shape.Volume, 90 * 3.141592653589793)
        self.assertEqual(component.history(converted, root.Definitions[0]), [converted.BaseSketch, converted.Extrusion])
        with component.transaction(converted, "Edit converted expression input"):
            converted.Extrusion.DesignLength = 7
        self.assertAlmostEqual(converted.Extrusion.Length.Value, 14)
        converted.undo(); converted.recompute()
        self.assertAlmostEqual(converted.Extrusion.Length.Value, 10)
        converted.redo(); converted.recompute()
        self.assertAlmostEqual(converted.Extrusion.Length.Value, 14)
        component.save_document(converted)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
        (self.output / "conversion-expected.json").write_text(json.dumps(dict(
            uid=str(converted.Uid), identities=identities, matrix=matrix, source_sha256=digest)))

    def test_native_primitive_static_curve_and_empty(self):
        for name, kind in [("LegacyBox", "Part::Box"), ("LegacyCurve", "Part::Feature"), ("LegacyEmpty", None)]:
            doc, source, target = self.source(name)
            if kind:
                obj = doc.addObject(kind, "Original")
                if kind == "Part::Feature":
                    obj.Shape = Part.makeLine(App.Vector(1, 2, 3), App.Vector(7, 2, 3))
                obj.Placement.Base = App.Vector(2, 3, 4)
            doc.recompute(); doc.saveAs(str(source))
            converted, report = convert_file(source, target)
            root = component.validate(converted)
            self.assertEqual(len(root.Definitions), int(kind is not None))
            self.assertEqual(report["warnings"], [])
            if kind:
                self.assertEqual(converted.Original.TypeId, kind)
                self.assertTrue(converted.Original.Shape.isValid())
                self.assertEqual(component.history(converted, root.Definitions[0]), [converted.Original])
                if kind == "Part::Box":
                    converted.Original.Length = 20; converted.recompute()
                    self.assertAlmostEqual(converted.Original.Shape.Volume, 2000)
                    editing.edit(root.Group[0])
                    sketch = editing.new_sketch(converted)
                    self.assertEqual(sketch.getParentGeoFeatureGroup().TypeId, "PartDesign::Body")

    def test_fallback_is_explicit_and_persistently_reported(self):
        doc, source, target = self.source("LegacyFallback")
        obj = doc.addObject("Part::FeaturePython", "UnsupportedFeature")
        obj.Shape = Part.makeBox(2, 3, 4)
        obj.Placement = App.Placement(App.Vector(7, 6, 5), App.Rotation(App.Vector(0, 0, 1), 30))
        doc.recompute(); doc.saveAs(str(source))
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        with self.assertRaises(ConversionError): convert_file(source, target)
        self.assertFalse(target.exists())
        converted, report = convert_file(source, target, allow_geometry_fallback=True)
        result = converted.UnsupportedFeature
        self.assertEqual(report["result"], "geometry-only")
        self.assertIn("parameters", report["warnings"][0])
        self.assertEqual(result.TypeId, "Part::Feature")
        self.assertEqual(result.ConversionSourceType, "Part::FeaturePython")
        self.assertAlmostEqual(result.Shape.Volume, 24)
        self.assertTrue(result.Placement.isSame(obj.Placement, 1e-9))
        self.assertEqual(json.loads(component.validate(converted).ConversionReport), report)
        name = converted.Name; App.closeDocument(name)
        reopened = component.open_document(target)
        self.assertEqual(json.loads(component.validate(reopened).ConversionReport), report)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)

    def test_rejection_save_failure_and_exclusive_destination(self):
        doc, source, target = self.source("LegacyUnsupported")
        doc.addObject("Part::Box", "One"); doc.addObject("Part::Box", "Two")
        doc.recompute(); doc.saveAs(str(source))
        before = set(App.listDocuments())
        with self.assertRaises(ConversionError) as error: convert_file(source, target)
        self.assertEqual(len(error.exception.report["inventory"]), 2)
        self.assertEqual(set(App.listDocuments()), before)
        self.assertFalse(target.exists())
        doc.removeObject("Two"); doc.recompute(); doc.save()
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        with patch("freecad_plus.conversion.component.save_document", side_effect=OSError("injected save failure")):
            with self.assertRaises(OSError): convert_file(source, target)
        self.assertFalse(target.exists())
        self.assertEqual(set(App.listDocuments()), before)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
        target.write_bytes(b"existing owner data")
        with self.assertRaises(FileExistsError): convert_file(source, target)
        self.assertEqual(target.read_bytes(), b"existing owner data")
        self.assertFalse(list(self.output.glob(".cadprt-convert-*")))

    def test_schema_one_remains_readable_without_implicit_upgrade(self):
        doc = component.new_document("SchemaOne")
        component.validate(doc).PlusSchema = 1
        path = component.save_document(doc, self.output / "schema-one.cadprt")
        App.closeDocument(doc.Name)
        reopened = component.open_document(path)
        self.assertEqual(component.validate(reopened).PlusSchema, 1)
        component.save_document(reopened)
        self.assertEqual(component.validate(reopened).PlusSchema, 1)


def verify_fresh_process(output):
    output = Path(output)
    expected = json.loads((output / "conversion-expected.json").read_text())
    doc = component.open_document(output / "LegacyBody.cadprt")
    assert str(doc.Uid) == expected["uid"]
    for name, values in expected["identities"].items():
        obj = doc.getObject(name)
        assert [obj.TypeId, obj.ID, obj.Label] == values
    assert all(abs(a-b) < 1e-9 for a,b in zip(doc.PlateBody.getGlobalPlacement().toMatrix().A, expected["matrix"]))
    assert doc.BaseSketch.AttachmentSupport and doc.BaseSketch.MapMode == "FlatFace"
    assert doc.Extrusion.Profile[0] == doc.BaseSketch
    assert abs(doc.Extrusion.Length.Value - 14) < 1e-9
    with component.transaction(doc, "Fresh converted edit"):
        doc.Extrusion.DesignLength = 8
    assert abs(doc.Extrusion.Length.Value - 16) < 1e-9 and doc.Extrusion.Shape.isValid()
    component.save_document(doc, output / "LegacyBody-edited.cadprt")
    assert hashlib.sha256((output / "LegacyBody.FCStd").read_bytes()).hexdigest() == expected["source_sha256"]
    App.closeDocument(doc.Name)
