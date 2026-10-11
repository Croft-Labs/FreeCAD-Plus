# SPDX-License-Identifier: LGPL-2.1-or-later
"""Export placed external component geometry through its original occurrence."""
import json
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad_plus import document, display, editing, hierarchy, geometry
from TestComponentPanel import TestComponentPanel, settle
from TestComponentExport import TestComponentExport, native_export
from TestUnusedModels import TestUnusedModels, visibility


class TestComponentExternalExport(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentPanel.tearDown
    external_fixture = TestUnusedModels.external_fixture
    select = TestComponentExport.select

    def fixture(self):
        self.source, self.definition = self.external_fixture()
        self.shape = self.source.addObject('Part::Box', 'ExternalBox')
        self.shape.Length = 2; self.shape.Width = 3; self.shape.Height = 4
        self.definition.addObject(self.shape)
        self.source.recompute()
        self.a = hierarchy.add_instance(self.root, self.definition)
        self.b = hierarchy.add_instance(self.root, self.definition,
            App.Placement(App.Vector(30, 0, 0), App.Rotation()))
        document.save_document(self.source)
        editing.edit_file(self.doc); settle()

    def route(self, link):
        return link.Name + '.' + self.shape.Name + '.'

    def test_external_occurrence_export_and_persistence(self):
        self.fixture()
        display.set_state(self.root, self.a, part_type='Reference'); settle()
        ids = [{o.Name:o.ID for o in d.Objects} for d in (self.doc, self.source)]
        undo = [d.UndoCount for d in (self.doc, self.source)]
        vis = [visibility(d) for d in (self.doc, self.source)]
        self.select(self.root, self.route(self.b))
        result = native_export(self.output / 'allowed.g1export')
        self.assertEqual(result['error'], '')
        self.assertEqual(result['calls'], ['options', 'writer'])
        shape = Part.Shape(); shape.read(str(self.output / 'allowed.g1export.brep'))
        self.assertTrue(shape.isValid()); self.assertAlmostEqual(shape.Volume, 24)
        self.select(self.root, self.route(self.a))
        result = native_export(self.output / 'reference.g1export')
        self.assertIn('Reference', result['error']); self.assertEqual(result['calls'], [])
        self.assertFalse((self.output / 'reference.g1export.brep').exists())
        self.assertEqual([{o.Name:o.ID for o in d.Objects} for d in (self.doc,self.source)], ids)
        self.assertEqual([d.UndoCount for d in (self.doc,self.source)], undo)
        self.assertEqual([visibility(d) for d in (self.doc,self.source)], vis)
        document.save_document(self.doc)
        (self.output / 'expected.json').write_text(json.dumps({'ids':ids,
            'allowed':self.route(self.b),'blocked':self.route(self.a)}))

    def test_mixed_external_occurrences_reject_before_writer(self):
        self.fixture()
        display.set_state(self.root, self.a, part_type='Excluded'); settle()
        self.select(self.root, self.route(self.b))
        Gui.Selection.addSelection(self.doc.Name, self.root.Name, self.route(self.a))
        result = native_export(self.output / 'mixed.g1export')
        self.assertIn('Excluded', result['error']); self.assertEqual(result['calls'], [])
        self.assertFalse((self.output / 'mixed.g1export.brep').exists())

    def test_source_payload_deduplication_and_no_catalog_fallback(self):
        self.fixture()
        self.select(self.root, self.route(self.a))
        Gui.Selection.addSelection(self.doc.Name, self.root.Name, self.route(self.b))
        self.assertEqual(geometry.export_objects(self.source), [self.shape])
        Gui.Selection.clearSelection()
        with self.assertRaisesRegex(ValueError, 'Select a component'):
            geometry.export_objects(self.source)
        # Selecting the raw source while viewing its assembly loses the occurrence.
        self.select(self.shape)
        with self.assertRaisesRegex(ValueError, 'component occurrence'):
            geometry.export_objects(self.source)


def verify_fresh_process(output):
    folder = Path(output) / 'test_external_occurrence_export_and_persistence'
    expected = json.loads((folder / 'expected.json').read_text())
    doc = document.open_document(folder / 'Assembly.cadprt')
    try:
        root = document.validate(doc); editing.edit_file(doc)
        source = root.getSubObject(expected['allowed'], 1).Document
        assert {o.Name:o.ID for o in source.Objects} == expected['ids'][1]
        assert {o.Name:o.ID for o in doc.Objects} == expected['ids'][0]
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(doc.Name,root.Name,expected['blocked'])
        result = native_export(folder / 'reopened-blocked.g1export')
        assert 'Reference' in result['error'] and not result['calls'], result
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(doc.Name,root.Name,expected['allowed'])
        result = native_export(folder / 'reopened-allowed.g1export')
        assert not result['error'] and result['calls'] == ['options','writer'], result
        shape = Part.Shape(); shape.read(str(folder / 'reopened-allowed.g1export.brep'))
        assert shape.isValid() and abs(shape.Volume-24) < 1e-8
    finally:
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()): App.closeDocument(name)
