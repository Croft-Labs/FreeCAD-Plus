# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native backend acceptance, without replacing commands, tasks or presentation."""
import json
import math
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide6 import QtTest

from freecad_plus import document, editing, external, hierarchy, modeling


class TestFeatureCenteredModeling(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Use an isolated native profile')
        self.before = set(App.listDocuments())
        self.output = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.output.mkdir(exist_ok=True)
        self.doc = document.new_document('FeatureCentered')
        self.root = document.validate(self.doc)
        self.owner = self.root.Definitions[0]

    def tearDown(self):
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        QtTest.QTest.qWait(100)

    def circle(self, radius=2):
        sketch = modeling.new_sketch(self.doc)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), radius), False)
        sketch.addConstraint(Sketcher.Constraint('Radius', 0, radius))
        sketch.Document.recompute()
        return sketch

    def snapshot(self, doc=None):
        doc = doc or self.doc
        return ({o.Name: o.ID for o in doc.Objects},
                {o.Name: [child.Name for child in o.Group] for o in doc.Objects if hasattr(o, 'Group')},
                {o.Name: o.Visibility for o in doc.Objects if hasattr(o, 'Visibility')}, doc.UndoCount)

    def test_sketch_without_body_and_undo(self):
        before = self.snapshot()
        sketch = modeling.new_sketch(self.doc)
        name = sketch.Name
        self.assertEqual(sketch.getParentGeoFeatureGroup(), self.owner)
        self.assertFalse(any(o.TypeId == 'PartDesign::Body' for o in self.doc.Objects))
        self.assertEqual(document.history(self.doc, self.owner), [sketch])
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(self.snapshot(), before)
        self.doc.redo(); self.doc.recompute()
        self.assertEqual(self.doc.getObject(name).getParentGeoFeatureGroup(), self.owner)
        document.save_document(self.doc, self.output / 'SketchOnly.cadprt')

    def test_extrusion_creates_body_atomically_and_recomputes(self):
        sketch = self.circle()
        sketch.Placement.Base = App.Vector(3, 4, 5)
        self.doc.recompute()
        before = self.snapshot()
        sketch_id = sketch.ID
        placement = sketch.Placement
        feature = modeling.extrude_new_solid(self.doc, sketch, 5)
        name = feature.Name
        body = feature.getParentGeoFeatureGroup()
        self.assertEqual(body.TypeId, 'PartDesign::Body')
        self.assertEqual(body.Tip, feature)
        self.assertEqual(body.getParentGeoFeatureGroup(), self.owner)
        self.assertEqual(sketch.ID, sketch_id)
        self.assertEqual(sketch.Placement, placement)
        self.assertAlmostEqual(feature.Shape.Volume, 20 * math.pi)
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMin, 5)
        self.assertEqual(document.history(self.doc, self.owner), [sketch, feature])
        self.assertEqual(self.doc.UndoCount, before[-1] + 1)
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(self.snapshot(), before)
        self.doc.redo(); self.doc.recompute()
        feature = self.doc.getObject(name)
        self.assertAlmostEqual(feature.Shape.Volume, 20 * math.pi)
        sketch.setDatum(0, App.Units.Quantity('3 mm'))
        self.doc.recompute()
        self.assertAlmostEqual(feature.Shape.Volume, 45 * math.pi)
        document.save_document(self.doc, self.output / 'Extruded.cadprt')
        (self.output / 'expected.json').write_text(json.dumps({
            'ids': {o.Name: o.ID for o in self.doc.Objects}, 'feature': feature.Name,
            'sketch': sketch.Name, 'body': feature.getParentGeoFeatureGroup().Name,
            'volume': feature.Shape.Volume}))

    def test_invalid_geometry_and_lengths_leave_no_body(self):
        sketch = modeling.new_sketch(self.doc)
        sketch.addGeometry(Part.LineSegment(App.Vector(), App.Vector(2, 0, 0)), False)
        self.doc.recompute()
        before = self.snapshot()
        for length in (0, -1, float('nan'), float('inf'), 5):
            with self.assertRaises(ValueError):
                modeling.extrude_new_solid(self.doc, sketch, length)
            self.assertEqual(self.snapshot(), before)
            self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(sketch.getParentGeoFeatureGroup(), self.owner)

    def test_context_and_pending_transaction_rejection(self):
        sketch = self.circle()
        other = hierarchy.create_definition(self.doc, 'Other')
        editing.edit_unused(self.doc, other)
        before = self.snapshot()
        with self.assertRaises(ValueError): modeling.extrude_new_solid(self.doc, sketch, 5)
        self.assertEqual(self.snapshot(), before)
        editing.edit_file(self.doc)
        with self.assertRaises(ValueError): modeling.new_sketch(self.doc)
        with self.assertRaises(ValueError): modeling.extrude_new_solid(self.doc, sketch, 5)
        editing.edit(self.root.Group[0])
        self.doc.openTransaction('Caller operation')
        self.owner.Label = 'Caller change'
        try:
            with self.assertRaises(ValueError): modeling.new_sketch(self.doc)
            with self.assertRaises(ValueError): modeling.extrude_new_solid(self.doc, sketch, 5)
            self.assertTrue(self.doc.HasPendingTransaction)
        finally: self.doc.abortTransaction()
        self.assertEqual(self.snapshot(), before)

    def test_independent_results_do_not_reuse_active_body(self):
        first = modeling.extrude_new_solid(self.doc, self.circle(), 5)
        old_body = first.getParentGeoFeatureGroup()
        second_sketch = self.circle(1)
        second_sketch.Placement.Base = App.Vector(20, 0, 0)
        self.doc.recompute()
        self.assertEqual(second_sketch.getParentGeoFeatureGroup(), self.owner)
        second = modeling.extrude_new_solid(self.doc, second_sketch, 4)
        self.assertNotEqual(second.getParentGeoFeatureGroup(), old_body)
        self.assertEqual(old_body.Tip, first)
        self.assertAlmostEqual(first.Shape.Volume, 20 * math.pi)
        self.assertAlmostEqual(second.Shape.Volume, 4 * math.pi)
        before = self.snapshot()
        with self.assertRaises(ValueError): modeling.extrude_new_solid(self.doc, second_sketch, 6)
        self.assertEqual(self.snapshot(), before)

    def test_external_unused_result_is_owned_and_undone_in_source(self):
        document.save_document(self.doc, self.output / 'Assembly.cadprt')
        source = document.new_document('FeatureSource')
        definition = hierarchy.create_definition(source, 'External feature component')
        document.save_document(source, self.output / 'Source.cadprt')
        external.import_file(self.doc, source)
        App.setActiveDocument(self.doc.Name)
        editing.edit_unused(self.doc, definition)
        context = editing.context_path(self.doc)
        sketch = self.circle()
        source_before = self.snapshot(source)
        assembly_ids = {o.Name: o.ID for o in self.doc.Objects}
        feature = modeling.extrude_new_solid(self.doc, sketch, 7)
        self.assertEqual(feature.Document, source)
        self.assertEqual(feature.getParentGeoFeatureGroup().getParentGeoFeatureGroup(), definition)
        self.assertEqual(editing.context_path(self.doc), context)
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, assembly_ids)
        name = feature.Name
        source.undo(); source.recompute()
        # Native cross-document Undo may also record entries in the assembly.
        self.assertEqual(self.snapshot(source), source_before)
        self.assertEqual(sketch.getParentGeoFeatureGroup(), definition)
        source.redo(); source.recompute()
        self.assertAlmostEqual(source.getObject(name).Shape.Volume, 28 * math.pi)
        document.save_document(source)
        document.save_document(self.doc)
        (self.output / 'expected.json').write_text(json.dumps({
            'source': source.Name, 'definition': definition.Name, 'feature': name,
            'source_ids': {o.Name: o.ID for o in source.Objects}, 'assembly_ids': assembly_ids}))


def verify_fresh_process(output):
    output = Path(output)
    folder = output / 'test_sketch_without_body_and_undo'
    doc = document.open_document(folder / 'SketchOnly.cadprt')
    assert not any(o.TypeId == 'PartDesign::Body' for o in doc.Objects)
    assert len(document.history(doc, document.validate(doc).Definitions[0])) == 1
    App.closeDocument(doc.Name)
    folder = output / 'test_extrusion_creates_body_atomically_and_recomputes'
    expected = json.loads((folder / 'expected.json').read_text())
    doc = document.open_document(folder / 'Extruded.cadprt')
    assert {o.Name: o.ID for o in doc.Objects} == expected['ids']
    feature = doc.getObject(expected['feature'])
    assert feature.Profile[0] == doc.getObject(expected['sketch'])
    assert doc.getObject(expected['body']).Tip == feature
    assert abs(feature.Shape.Volume - expected['volume']) < 1e-7
    feature.Length = 8; doc.recompute()
    assert feature.Shape.isValid() and abs(feature.Shape.Volume - 72 * math.pi) < 1e-7
    App.closeDocument(doc.Name)
    folder = output / 'test_external_unused_result_is_owned_and_undone_in_source'
    expected = json.loads((folder / 'expected.json').read_text())
    doc = document.open_document(folder / 'Assembly.cadprt')
    source = next(d for d in App.listDocuments().values() if d != doc)
    assert {o.Name: o.ID for o in doc.Objects} == expected['assembly_ids']
    assert {o.Name: o.ID for o in source.Objects} == expected['source_ids']
    feature = source.getObject(expected['feature'])
    feature.Length = 9; source.recompute(); doc.recompute()
    assert feature.Shape.isValid() and abs(feature.Shape.Volume - 36 * math.pi) < 1e-7
    document.validate(doc)
    App.closeDocument(doc.Name); App.closeDocument(source.Name)
