# SPDX-License-Identifier: LGPL-2.1-or-later
"""External catalogs, defining-file edits/copies and failure/recovery acceptance."""
import hashlib
import json
import os
from pathlib import Path
import unittest
import zipfile
import xml.etree.ElementTree as ET

import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad_plus import document as component, hierarchy, editing, external


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rewrite_archive(path, change):
    with zipfile.ZipFile(path) as archive:
        entries = {name: archive.read(name) for name in archive.namelist()}
    tree = ET.fromstring(entries['Document.xml'])
    change(tree)
    entries['Document.xml'] = ET.tostring(tree)
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in entries.items():
            archive.writestr(name, data)


class TestExternalDefinitions(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Set PLUS_TEST_DIR to an isolated validation directory')
        self.output = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.output.mkdir(exist_ok=True)
        self.before = set(App.listDocuments())

    def tearDown(self):
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)

    def file(self, name):
        doc = component.new_document(name)
        component.save_document(doc, self.output / (name + '.cadprt'))
        return doc, component.validate(doc)

    def files(self):
        child, cr = self.file('Fasteners')
        source, sr = self.file('Hardware')
        external.import_file(source, child)
        nested = hierarchy.add_instance(sr.Definitions[0], cr.Definitions[0],
                                        App.Placement(App.Vector(10, 0, 0), App.Rotation()))
        component.save_document(source)
        assembly, ar = self.file('Assembly')
        external.import_file(assembly, source)
        return assembly, ar, source, sr, child, cr, nested

    def test_nested_catalog_is_not_placement_and_file_cycles_preflight(self):
        assembly, ar, source, sr, child, cr, nested = self.files()
        self.assertEqual(len(ar.Group), 1)
        model = external.catalog(assembly)
        self.assertEqual(model['imports'][0]['imports'][0]['definitions'], tuple(cr.Definitions))
        self.assertEqual(external.qualified_label(ar.Definitions[0], assembly), 'Part001')
        self.assertEqual(external.qualified_label(sr.Definitions[0], assembly), 'Part001 (Hardware)')
        self.assertNotEqual(ar.Definitions[0], sr.Definitions[0])
        count, undo = len(child.Objects), child.UndoCount
        with self.assertRaisesRegex(ValueError, 'Circular file'):
            external.import_file(child, assembly)
        self.assertEqual((len(child.Objects), child.UndoCount), (count, undo))
        with self.assertRaises(ValueError):
            hierarchy.add_instance(sr.Definitions[0], ar.Definitions[0])
        with self.assertRaisesRegex(ValueError, 'Circular'):
            hierarchy.add_instance(cr.Definitions[0], cr.Definitions[0])
        assembly.undo()
        self.assertEqual(external.catalog(assembly)['imports'], ())
        assembly.redo()
        self.assertEqual(ar.Imports, [sr])
        component.save_document(assembly)

    def test_external_edit_stays_in_tab_and_saves_defining_file(self):
        assembly, ar, source, sr, child, cr, nested = self.files()
        top = hierarchy.add_instance(ar, sr.Definitions[0])
        second = hierarchy.add_instance(ar, sr.Definitions[0],
                                        App.Placement(App.Vector(25, 0, 0), App.Rotation()))
        component.save_document(assembly)
        App.setActiveDocument(assembly.Name)
        editing.edit((second, nested))
        self.assertEqual(App.ActiveDocument, assembly)
        before_count = len(assembly.Objects)
        sketch = editing.new_sketch(assembly)
        self.assertEqual(sketch.Document, child)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        child.recompute()
        pad = editing.pad(assembly, sketch, 5)
        self.assertEqual(len(assembly.Objects), before_count)
        # Native cross-document transactions may add dependent-document undo entries.
        # Geometry and the feature transaction still belong to the defining file.
        self.assertEqual(editing.context_path(assembly), (cr.Definitions[0], (second, nested)))
        self.assertEqual(component.history(assembly, cr.Definitions[0]), [sketch, pad])
        pad_name = pad.Name
        child.undo(); child.recompute()
        self.assertIsNone(child.getObject(pad_name))
        child.redo(); child.recompute(); pad = child.getObject('Pad')
        old_hash = digest(child.FileName)
        component.save_document(assembly)
        self.assertEqual(digest(child.FileName), old_hash)
        external.save_definition(cr.Definitions[0])
        self.assertNotEqual(digest(child.FileName), old_hash)
        self.assertEqual(App.ActiveDocument, assembly)
        body = pad.getParentGeoFeatureGroup()
        suffix = body.Name + '.' + pad.Name + '.'
        for instance in (top, second):
            shape = ar.getSubObject(hierarchy.subname((instance, nested)) + suffix, 0)
            self.assertAlmostEqual(shape.Volume, 20 * 3.141592653589793)
        (self.output / 'expected.json').write_text(json.dumps({
            'uid': str(child.Uid), 'pad': pad.Name, 'source': Path(child.FileName).name,
            'paths': [[top.Name, nested.Name], [second.Name, nested.Name]],
            'suffix': suffix, 'definition': cr.Definitions[0].Name,
            'ids': {o.Name: o.ID for o in child.Objects}}))

    def test_independent_nested_copy_and_explicit_replacements_undo(self):
        assembly, ar, source, sr, child, cr, nested = self.files()
        with component.transaction(child, 'Native child geometry'):
            box = cr.Definitions[0].newObject('Part::Box', 'Box')
            box.Length = 2; box.Width = 3; box.Height = 4
        external.save_definition(cr.Definitions[0])
        selected = hierarchy.add_instance(ar, sr.Definitions[0],
                                          App.Placement(App.Vector(7, 8, 9), App.Rotation()))
        kept = hierarchy.add_instance(ar, sr.Definitions[0])
        place = selected.LinkPlacement
        copied = external.copy_definition(sr.Definitions[0], assembly, 'Independent',
                    placements_to_replace=(selected,), child_labels={cr.Definitions[0]: 'Independent child'})
        copied_name = copied.Name
        self.assertEqual(selected.LinkedObject, copied)
        self.assertEqual(kept.LinkedObject, sr.Definitions[0])
        self.assertTrue(selected.LinkPlacement.isSame(place, 1e-9))
        copy_child = next(o for o in copied.Group if o.TypeId == 'App::Link').LinkedObject
        copy_box = next(o for o in copy_child.Group if o.TypeId == 'Part::Box')
        self.assertEqual(copy_child.Document, assembly)
        self.assertNotEqual(copy_box, box)
        copy_box.Length = 6; assembly.recompute()
        self.assertEqual(box.Length.Value, 2)
        assembly.undo(); assembly.recompute()
        self.assertEqual(selected.LinkedObject, sr.Definitions[0])
        self.assertIsNone(assembly.getObject(copied_name))
        assembly.redo(); assembly.recompute()
        self.assertEqual(selected.LinkedObject.Name, copied_name)
        component.save_document(assembly)
        exported, er = self.file('IndependentStorage')
        external.copy_definition(ar.Definitions[0], exported, 'Domestic copied outward', placements_to_replace=())
        self.assertEqual(len(er.Definitions), 2)
        self.assertEqual(er.Imports, [])
        component.save_document(exported)

    def test_missing_wrong_future_and_missing_target_fail_then_recover(self):
        assembly, ar, source, sr, child, cr, nested = self.files()
        hierarchy.add_instance(ar, sr.Definitions[0])
        component.save_document(assembly)
        ap, sp, cp = map(Path, (assembly.FileName, source.FileName, child.FileName))
        original = cp.read_bytes()
        for name in list(set(App.listDocuments()) - self.before): App.closeDocument(name)
        before = set(App.listDocuments())
        cp.rename(cp.with_suffix('.missing'))
        try:
            with self.assertRaisesRegex(ValueError, 'Missing defining file'):
                component.open_document(ap)
            self.assertEqual(set(App.listDocuments()), before)
        finally:
            cp.with_suffix('.missing').rename(cp)
        rewrite_archive(cp, lambda tree: tree.find("./Properties/Property[@name='Uid']/Uuid").set('value', '00000000-0000-0000-0000-000000000000'))
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            component.open_document(ap)
        cp.write_bytes(original)
        rewrite_archive(cp, lambda tree: tree.find("./ObjectData/Object/Properties/Property[@name='PlusSchema']/Integer").set('value', '999'))
        with self.assertRaisesRegex(ValueError, 'Unsupported component schema'):
            component.open_document(ap)
        cp.write_bytes(original)
        original_source = sp.read_bytes()
        rewrite_archive(sp, lambda tree: tree.find("./ObjectData/Object/Properties/Property[@name='LinkedObject']/XLink[@file='Fasteners.cadprt']").set('name', 'MissingDefinition'))
        with self.assertRaisesRegex(ValueError, 'Missing or unsupported external definition'):
            component.open_document(ap)
        self.assertEqual(set(App.listDocuments()), before)
        sp.write_bytes(original_source)
        reopened = component.open_document(ap)
        self.assertEqual(len(external.catalog(reopened)['imports'][0]['imports']), 1)
        self.assertEqual(cp.read_bytes(), original)

    def test_unsaved_source_target_and_failed_save_are_recoverable(self):
        assembly, ar, source, sr, child, cr, nested = self.files()
        new = hierarchy.create_definition(source, 'Unsaved definition')
        hierarchy.add_instance(ar, new)
        original = Path(assembly.FileName).read_bytes()
        with self.assertRaisesRegex(ValueError, 'Save the new definition'):
            component.save_document(assembly)
        self.assertEqual(Path(assembly.FileName).read_bytes(), original)
        external.save_definition(new)
        component.save_document(assembly)
        before_name, before_label = source.FileName, sr.Label
        with self.assertRaises(ValueError):
            component.save_document(source, self.output / 'Relocated.cadprt')
        self.assertEqual((source.FileName, sr.Label), (before_name, before_label))
        source_path = Path(source.FileName)
        saved = source_path.read_bytes()
        new.Label = 'Edited name'
        source_path.rename(source_path.with_suffix('.held'))
        source_path.mkdir()
        try:
            with self.assertRaises(Exception): external.save_definition(new)
            self.assertTrue(Gui.getDocument(source.Name).Modified)
        finally:
            source_path.rmdir()
            source_path.with_suffix('.held').rename(source_path)
        self.assertEqual(source_path.read_bytes(), saved)
        external.save_definition(new)

    def test_unsaved_nested_import_cannot_publish_unresolvable_assembly(self):
        source, sr = self.file('Hardware')
        assembly, ar = self.file('Assembly')
        external.import_file(assembly, source)
        component.save_document(assembly)
        child, cr = self.file('LaterCatalog')
        external.import_file(source, child)  # Intentionally not saved yet.
        hierarchy.add_instance(ar, cr.Definitions[0])
        before = digest(assembly.FileName)
        with self.assertRaisesRegex(ValueError, 'Save the changed import catalog'):
            component.save_document(assembly)
        self.assertEqual(digest(assembly.FileName), before)
        component.save_document(source)
        component.save_document(assembly)

    def test_explicit_schema_upgrade_and_unsaved_import_preflight(self):
        source, sr = self.file('Old')
        sr.removeProperty('Imports'); sr.removeProperty('ImportIdentities'); sr.PlusSchema = 3
        component.save_document(source)
        child, cr = self.file('Child')
        with self.assertRaisesRegex(ValueError, 'explicit upgrade'):
            external.import_file(source, child)
        external.upgrade(source)
        self.assertEqual(sr.PlusSchema, 4)
        source.undo(); self.assertEqual(sr.PlusSchema, 3)
        source.redo(); self.assertEqual(sr.PlusSchema, 4)
        external.import_file(source, child)
        unsaved = component.new_document('Unsaved')
        count, undo = len(unsaved.Objects), unsaved.UndoCount
        with self.assertRaisesRegex(ValueError, 'Save both'):
            external.import_file(unsaved, child)
        self.assertEqual((len(unsaved.Objects), unsaved.UndoCount), (count, undo))


def verify_fresh_process(output):
    output = Path(output) / 'test_external_edit_stays_in_tab_and_saves_defining_file'
    expected = json.loads((output / 'expected.json').read_text())
    assembly = component.open_document(output / 'Assembly.cadprt')
    root = component.validate(assembly)
    definition, path = hierarchy.resolve(assembly, expected['paths'][1])
    source = definition.Document
    assert str(source.Uid) == expected['uid']
    assert {o.Name: o.ID for o in source.Objects} == expected['ids']
    editing.edit(path)
    assert App.ActiveDocument == assembly
    pad = source.getObject(expected['pad'])
    assert pad.Length.Value == 5
    before = digest(assembly.FileName)
    with component.transaction(source, 'Saved external edit'): pad.Length = 8
    external.save_definition(definition)
    assert digest(assembly.FileName) == before
    for occurrence in expected['paths']:
        assert abs(root.getSubObject('.'.join(occurrence) + '.' + expected['suffix'], 0).Volume - 32 * 3.141592653589793) < 1e-8
    for name in list(App.listDocuments()): App.closeDocument(name)
    assembly = component.open_document(output / 'Assembly.cadprt')
    definition, _ = hierarchy.resolve(assembly, expected['paths'][0])
    assert definition.Document.getObject(expected['pad']).Length.Value == 8
