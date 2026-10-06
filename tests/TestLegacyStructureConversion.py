# SPDX-License-Identifier: LGPL-2.1-or-later
import hashlib
import os
from pathlib import Path
import sys
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src/Mod/Part"))
    sys.modules.pop("CadDocument", None)
import CadDocument
import ComponentModel as Model


class TestLegacyStructureConversion(unittest.TestCase):
    def setUp(self):
        self.names = set(App.listDocuments())
        self.doc = App.newDocument("LegacyStructure")
        self.doc.UndoMode = 1
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        for name in set(App.listDocuments()) - self.names:
            App.closeDocument(name)

    def frame(self, x, angle=0):
        return App.Placement(App.Vector(x, 3, 0), App.Rotation(App.Vector(0, 0, 1), angle))

    def build(self):
        assembly = self.doc.addObject("App::Part", "Assembly")
        assembly.Placement = self.frame(10, 30)
        part = self.doc.addObject("App::Part", "Part")
        assembly.addObject(part)
        part.Placement = self.frame(8, 20)
        body = self.doc.addObject("PartDesign::Body", "Body")
        part.addObject(body)
        sketch = body.newObject("Sketcher::SketchObject", "Sketch")
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        pad = body.newObject("PartDesign::Pad", "Pad")
        pad.Profile = sketch
        pad.Length = 5
        body.Tip = pad
        for index, transform in enumerate((False, True)):
            link = self.doc.addObject("App::Link", "Use" + str(index))
            assembly.addObject(link)
            link.setLink(part)
            link.LinkTransform = transform
            link.LinkPlacement = self.frame(40 + index * 20, 15)
        self.doc.recompute()
        return assembly, part, body, sketch, pad

    def shape(self, obj):
        return Part.getShape(obj, "", needSubElement=False).copy()

    def same(self, before, after):
        self.assertAlmostEqual(before.Volume, after.Volume, places=8)
        self.assertAlmostEqual(before.cut(after).Volume, 0, places=8)
        self.assertAlmostEqual(after.cut(before).Volume, 0, places=8)

    def test_nested_frames_links_native_history_undo_and_reopen(self):
        assembly, part, body, sketch, pad = self.build()
        shapes = {obj.Name: self.shape(obj) for obj in (assembly, self.doc.Use0, self.doc.Use1)}
        body_frame = body.getGlobalPlacement()
        path = self.output / "Original.FCStd"
        self.doc.saveAs(str(path))
        original = hashlib.sha256(path.read_bytes()).hexdigest()
        CadDocument.convert_legacy(self.doc)
        root = Model.metadata(self.doc).RootComponent
        self.assertEqual(set(Model.definitions(self.doc)), {root, assembly, part})
        self.assertEqual(self.doc.Use0.LinkedObject, part)
        self.assertEqual(self.doc.Use1.LinkedObject, part)
        self.assertEqual(Model.owner(self.doc.Use0), assembly)
        self.assertEqual(body.LegacyBodyHistory, [sketch.Name, pad.Name])
        self.assertEqual(body.LegacyTip, pad)
        self.assertEqual(body.Tip.Producer, pad)
        self.assertTrue(body.getGlobalPlacement().isSame(body_frame, 1e-9))
        self.assertEqual(Model.instance_counts(root)[part], 3)
        for obj in (assembly, self.doc.Use0, self.doc.Use1):
            self.same(shapes[obj.Name], self.shape(obj))
        Model.validate(self.doc)
        count = len(self.doc.Objects)
        self.assertIs(CadDocument.convert_legacy(self.doc), self.doc)
        self.assertEqual(len(self.doc.Objects), count)
        self.doc.undo()
        self.assertFalse(any(getattr(o, "ComponentRole", "") == "Document" for o in self.doc.Objects))
        self.assertEqual(Model.owner(part), assembly)
        self.doc.redo()
        self.same(shapes["Assembly"], self.shape(self.doc.Assembly))
        target = self.output / "Converted.cadprt"
        self.doc.saveAs(str(target))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), original)
        name = self.doc.Name
        App.closeDocument(name)
        self.doc = CadDocument.open(target)
        self.same(shapes["Assembly"], self.shape(self.doc.Assembly))
        self.assertEqual(self.doc.Body.LegacyTip.Name, "Pad")
        self.assertEqual(self.doc.Body.LegacyBodyHistory, ["Sketch", "Pad"])
        self.assertEqual(self.doc.Body.Group, [self.doc.Body.Tip])

    def test_standalone_body_shared_wrapper(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        feature = body.newObject("PartDesign::Feature", "Solid")
        feature.Shape = Part.makeBox(2, 3, 4)
        body.Tip = feature
        body.Placement = self.frame(9, 25)
        for index, mode in enumerate((False, True)):
            link = self.doc.addObject("App::Link", "Use" + str(index))
            link.setLink(body)
            link.LinkTransform = mode
            link.LinkPlacement = self.frame(30 + index * 20, 10)
        self.doc.recompute()
        before = {o.Name: self.shape(o) for o in (self.doc.Use0, self.doc.Use1)}
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(self.doc.Use0.LinkedObject, self.doc.Use1.LinkedObject)
        self.assertEqual(self.doc.Body, body)
        self.assertEqual(body.Tip, feature)
        for link in (self.doc.Use0, self.doc.Use1):
            self.same(before[link.Name], self.shape(link))

    def test_external_source_converts_in_memory_and_save_order(self):
        source = App.newDocument("Source")
        box = source.addObject("Part::Box", "Box")
        source.recompute()
        original = self.output / "External.FCStd"
        source.saveAs(str(original))
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        self.doc.saveAs(str(self.output / "Parent.FCStd"))
        link = self.doc.addObject("App::Link", "ExternalUse")
        link.setLink(box)
        self.doc.recompute()
        before = self.shape(link)
        CadDocument.convert_legacy(self.doc)
        self.assertTrue(Model.is_component(link.LinkedObject))
        self.assertEqual(link.LinkedObject.Document, source)
        self.same(before, self.shape(link))
        with self.assertRaises(Exception):
            self.doc.saveAs(str(self.output / "TooEarly.cadprt"))
        source.saveAs(str(self.output / "External.cadprt"))
        self.doc.saveAs(str(self.output / "Parent.cadprt"))
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)

    def test_models_and_part_tree_use_native_converted_definitions(self):
        assembly, part, *_ = self.build()
        CadDocument.convert_legacy(self.doc)
        from freecad.gui import ComponentNavigator
        panel = ComponentNavigator.show(self.doc)
        Gui.updateGui()
        self.assertEqual(panel.models.topLevelItemCount(), 3)
        root = Model.metadata(self.doc).RootComponent
        self.assertEqual(panel.models.topLevelItem(0).data(0, 256), ComponentNavigator.object_key(root))
        self.assertEqual(panel.structure.topLevelItem(0).data(0, 256)[0], ComponentNavigator.object_key(root))
        self.assertTrue(Model.children(assembly))

    def test_arrays_recover_geometry_and_retain_native_payload(self):
        box = self.doc.addObject("Part::Box", "Box")
        link = self.doc.addObject("App::Link", "Array")
        link.setLink(box)
        link.ElementCount = 3
        self.doc.recompute()
        before = self.shape(link)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(link.LinkedObject, box)
        definition = next(d for d in Model.definitions(self.doc) if getattr(d, "LegacyDefinitionSource", None) == link)
        self.same(before, self.shape(definition))
        self.assertTrue(any("dumb array" in message for message in Model.metadata(self.doc).ConversionReport))

    def test_missing_instance_is_reported_and_save_requires_repair(self):
        link = self.doc.addObject("App::Link", "Missing")
        CadDocument.convert_legacy(self.doc)
        root = Model.metadata(self.doc).RootComponent
        self.assertIn(link, Model.children(root))
        self.assertIsNone(link.LinkedObject)
        self.assertTrue(any("unresolved" in m for m in Model.metadata(self.doc).ConversionReport))
        with self.assertRaises(ValueError):
            CadDocument.manifest(self.doc)

    def test_standard_gui_open_converts_source(self):
        from TestInstalledComponentDocument import TestInstalledComponentDocument
        TestInstalledComponentDocument.testStandardOpenConvertsLegacyWithoutChangingOriginal(self)

    def test_uniform_scaled_instance_preserves_native_geometry(self):
        self.build()
        link = self.doc.Use1
        link.Scale = 2
        self.doc.recompute()
        before = self.shape(link)
        CadDocument.convert_legacy(self.doc)
        self.same(before, self.shape(link))
        self.assertAlmostEqual(link.Scale, 2)

    def test_internal_body_reference_keeps_owner_and_native_history(self):
        assembly, part, body, sketch, pad = self.build()
        link = self.doc.addObject("App::Link", "InternalUse")
        assembly.addObject(link)
        link.setLink(body)
        link.LinkPlacement = self.frame(70, 5)
        self.doc.recompute()
        before = self.shape(link)
        CadDocument.convert_legacy(self.doc)
        self.same(before, self.shape(link))
        self.assertEqual(Model.owner(body), part)
        self.assertEqual(body.LegacyBodyHistory, [sketch.Name, pad.Name])
        self.assertEqual(body.Tip.Producer, pad)

    def test_root_primitive_legacy_recompute_save_reopen(self):
        from TestComponentDocument import TestComponentDocument
        TestComponentDocument.testLegacyConversionPreservesOriginalAndEditableFeatures(self)

    def test_failed_frame_adapter_recovers_dumb_output_and_keeps_native_payload(self):
        assembly, part, body, sketch, pad = self.build()
        part.setExpression("Placement.Base.x", "8 mm")
        self.doc.recompute()
        before = self.shape(assembly)
        CadDocument.convert_legacy(self.doc)
        root = Model.metadata(self.doc).RootComponent
        outputs = Model.finished_results(root)
        self.assertTrue(outputs, Model.metadata(self.doc).ConversionReport)
        self.same(before, outputs[0].Shape)
        self.assertEqual(Model.owner(part), assembly)
        self.assertEqual(body.Group, [sketch, pad])
        self.assertTrue(part.ExpressionEngine)
        self.assertTrue(any("dumb geometry" in m for m in Model.metadata(self.doc).ConversionReport))
        self.doc.saveAs(str(self.output / "Recovered.cadprt"))

    def test_local_frame_expression_consumer_is_preserved_by_recovery(self):
        assembly, part, *_ = self.build()
        box = self.doc.addObject("Part::Box", "Consumer")
        box.setExpression("Length", "<<Part>>.Placement.Base.x")
        self.doc.recompute()
        before = self.shape(box)
        CadDocument.convert_legacy(self.doc)
        root = Model.metadata(self.doc).RootComponent
        recovered = next(o for o in Model.finished_results(root) if o.LegacyRecovery.startswith("Consumer:"))
        self.same(before, recovered.Shape)
        self.assertTrue(box.ExpressionEngine)
        self.assertEqual(Model.owner(part), assembly)
