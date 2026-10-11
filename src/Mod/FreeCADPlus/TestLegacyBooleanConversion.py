# SPDX-License-Identifier: LGPL-2.1-or-later
"""Preserve native Boolean tool ownership during isolated legacy conversion."""
import hashlib
import json
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad_plus import document
from freecad_plus.conversion import convert_file, ConversionError
from TestLegacyConversion import TestLegacyConversion


class TestLegacyBooleanConversion(unittest.TestCase):
    setUp = TestLegacyConversion.setUp
    tearDown = TestLegacyConversion.tearDown
    source = TestLegacyConversion.source

    def fixture(self, name, hierarchy=False, scripted=False):
        doc, source, target = self.source(name)
        parent = doc.addObject('App::Part', 'LegacyPart') if hierarchy else None
        tool = doc.addObject('PartDesign::Body', 'ToolBody')
        body = doc.addObject('PartDesign::Body', 'ResultBody')
        if parent:
            parent.addObject(tool); parent.addObject(body)
        box = tool.newObject('PartDesign::FeaturePython' if scripted else
                             'PartDesign::AdditiveBox', 'ToolBox')
        if scripted:
            box.Shape = Part.makeBox(2, 2, 2)
        else:
            box.addProperty('App::PropertyLength', 'DesignLength')
            box.DesignLength = 2
            box.setExpression('Length', 'DesignLength')
            box.Width = 2; box.Height = 2
        box.Placement.Base = App.Vector(9, 1, 1)
        base = body.newObject('PartDesign::AdditiveBox', 'BaseBox')
        base.Length = 10; base.Width = 6; base.Height = 4
        doc.recompute()
        fusion = body.newObject('PartDesign::Boolean', 'Fusion')
        fusion.addObjects([tool])
        doc.recompute()
        self.assertEqual(list(fusion.Group), [tool])
        self.assertTrue(fusion.Shape.isValid())
        self.assertAlmostEqual(fusion.Shape.Volume, 244)
        if parent:
            parent.Placement = App.Placement(App.Vector(12, 8, 4),
                                            App.Rotation(App.Vector(0, 0, 1), 25))
            link = doc.addObject('App::Link', 'SharedPart')
            link.setLink(parent); link.LinkTransform = True
            link.LinkPlacement.Base = App.Vector(30, 0, 0)
        doc.recompute(); doc.saveAs(str(source))
        return doc, source, target

    def check_conversion(self, name, hierarchy):
        doc, source, target = self.fixture(name, hierarchy)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        identities = {o.Name: [o.ID, o.TypeId, o.Label] for o in doc.Objects}
        frame = list(doc.ToolBox.getGlobalPlacement().toMatrix().A)
        # A live unsaved edit must neither be converted nor overwritten.
        doc.ToolBox.DesignLength = 7; doc.recompute()
        converted, report = convert_file(source, target)
        root = document.validate(converted); definition = root.Definitions[0]
        self.assertEqual(report['result'], 'native-preserved')
        self.assertEqual(report['warnings'], [])
        self.assertEqual(doc.ToolBox.DesignLength.Value, 7)
        self.assertTrue(Gui.getDocument(doc.Name).Modified)
        for original, identity in identities.items():
            obj = converted.getObject(original)
            self.assertEqual([obj.ID, obj.TypeId, obj.Label], identity)
        self.assertEqual(list(converted.Fusion.Group), [converted.ToolBody])
        self.assertEqual(converted.ToolBody.Tip, converted.ToolBox)
        self.assertEqual(converted.ResultBody.Tip, converted.Fusion)
        self.assertEqual(list(converted.ToolBox.ExpressionEngine), [('Length', 'DesignLength')])
        self.assertEqual(list(converted.ToolBox.getGlobalPlacement().toMatrix().A), frame)
        self.assertNotIn(converted.ToolBody, definition.Group)
        history = document.history(converted, definition)
        self.assertEqual(history, [converted.BaseBox, converted.ToolBox, converted.Fusion])
        if hierarchy:
            self.assertEqual(definition, converted.LegacyPart)
            self.assertEqual(converted.SharedPart.LinkedObject, definition)
            self.assertEqual(len(root.Group), 2)
        with document.transaction(converted, 'Edit converted Boolean tool'):
            converted.ToolBox.DesignLength = 3
        self.assertAlmostEqual(converted.Fusion.Shape.Volume, 248)
        converted.undo(); converted.recompute()
        self.assertAlmostEqual(converted.Fusion.Shape.Volume, 244)
        converted.redo(); converted.recompute()
        self.assertAlmostEqual(converted.Fusion.Shape.Volume, 248)
        document.save_document(converted)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
        (self.output / (name + '-expected.json')).write_text(json.dumps({
            'ids': {o.Name: o.ID for o in converted.Objects}, 'definition': definition.Name,
            'history': [o.Name for o in history], 'frame': frame, 'source_sha256': digest,
            'hierarchy': hierarchy, 'volume': converted.Fusion.Shape.Volume}))

    def test_standalone_boolean_preserves_editable_graph(self):
        self.check_conversion('LegacyBoolean', False)

    def test_part_shared_link_preserves_boolean_graph(self):
        self.check_conversion('LegacyPartBoolean', True)

    def test_nested_scripted_tool_is_refused_without_output(self):
        for hierarchy in (False, True):
            doc, source, target = self.fixture('ScriptedBoolean' + str(hierarchy), hierarchy, True)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ConversionError, 'Scripted Body'):
                convert_file(source, target, allow_geometry_fallback=True)
            self.assertFalse(target.exists())
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
            self.assertIn(doc.Name, App.listDocuments())

    def test_unowned_dependency_and_independent_body_are_refused(self):
        for hierarchy in (False, True):
            doc, source, target = self.fixture('UnownedBoolean' + str(hierarchy), hierarchy)
            orphan = doc.addObject('Part::Feature', 'Unowned')
            orphan.Shape = Part.makeBox(1, 1, 1)
            doc.Fusion.addProperty('App::PropertyLink', 'OtherDependency')
            doc.Fusion.OtherDependency = orphan
            doc.recompute(); doc.save()
            with self.assertRaises(ConversionError): convert_file(source, target)
            self.assertFalse(target.exists())
        doc, source, target = self.fixture('IndependentBody')
        independent = doc.addObject('PartDesign::Body', 'Independent')
        independent.newObject('PartDesign::AdditiveBox', 'SeparateBox')
        doc.recompute(); doc.save()
        with self.assertRaises(ConversionError): convert_file(source, target)
        self.assertFalse(target.exists())


def verify_fresh_process(output):
    output = Path(output)
    for name in ('LegacyBoolean', 'LegacyPartBoolean'):
        expected = json.loads((output / (name + '-expected.json')).read_text())
        doc = document.open_document(output / (name + '.cadprt'))
        try:
            assert {o.Name: o.ID for o in doc.Objects} == expected['ids']
            definition = doc.getObject(expected['definition'])
            assert list(doc.Fusion.Group) == [doc.ToolBody]
            assert doc.ResultBody.Tip == doc.Fusion and doc.ToolBody.Tip == doc.ToolBox
            assert [o.Name for o in document.history(doc, definition)] == expected['history']
            assert list(doc.ToolBox.getGlobalPlacement().toMatrix().A) == expected['frame']
            assert list(doc.ToolBox.ExpressionEngine) == [('Length', 'DesignLength')]
            assert abs(doc.Fusion.Shape.Volume - expected['volume']) < 1e-7
            if expected['hierarchy']:
                assert doc.SharedPart.LinkedObject == definition
                assert len(document.validate(doc).Group) == 2
            doc.ToolBox.DesignLength = 4; doc.recompute(); document.validate(doc)
            assert doc.Fusion.Shape.isValid() and 'Invalid' not in doc.Fusion.State
            assert abs(doc.Fusion.Shape.Volume - expected['volume'] - 4) < 1e-7
            assert hashlib.sha256((output / (name + '.FCStd')).read_bytes()).hexdigest() == expected['source_sha256']
        finally:
            App.closeDocument(doc.Name)
