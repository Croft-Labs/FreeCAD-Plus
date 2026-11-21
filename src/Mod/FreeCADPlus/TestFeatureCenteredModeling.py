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
from PySide6 import QtCore, QtTest, QtWidgets

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


class TestFeatureCenteredCommands(unittest.TestCase):
    snapshot = TestFeatureCenteredModeling.snapshot
    circle = TestFeatureCenteredModeling.circle

    def setUp(self):
        Gui.Selection.clearSelection()
        QtTest.QTest.qWait(350)  # Drain delayed native tree selection before new fixtures.
        TestFeatureCenteredModeling.setUp(self)
        Gui.activateWorkbench('PartDesignWorkbench')

    def tearDown(self):
        if Gui.Control.activeDialog():
            self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        if App.getActiveTransaction():
            App.closeActiveTransaction(True)
        TestFeatureCenteredModeling.tearDown(self)

    def task_button(self, role):
        buttons = [box.button(role) for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)]
        button = next(b for b in buttons if b and b.isVisible())
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(200)

    def new_sketch_command(self, accept=True):
        definition = editing.context_path(self.doc)[0]
        Gui.Selection.clearSelection()
        seen, errors = [], []
        attempts = [0]
        def choose():
            dlg = QtWidgets.QApplication.activeModalWidget()
            attempts[0] += 1
            if dlg is None and attempts[0] < 100:
                QtCore.QTimer.singleShot(30, choose)
                return
            try:
                self.assertIsNotNone(dlg)
                self.assertIn('SketchOrientationDialog', dlg.metaObject().className())
                self.assertTrue(dlg.findChild(QtWidgets.QRadioButton, 'XY_radioButton').isChecked())
                self.assertIsNotNone(dlg.findChild(QtWidgets.QCheckBox, 'Reverse_checkBox'))
                offset = dlg.findChild(QtWidgets.QWidget, 'Offset_doubleSpinBox')
                self.assertIsNotNone(offset)
                offset.setProperty('rawValue', 2.0)
                seen.append(True)
                dlg.accept() if accept else dlg.reject()
            except BaseException as error:
                errors.append(error)
                if dlg: dlg.reject()
        QtCore.QTimer.singleShot(30, choose)
        Gui.runCommand('Sketcher_NewSketch')
        QtTest.QTest.qWait(200)
        if errors: raise errors[0]
        self.assertTrue(seen)
        if not accept: return
        sketch = Gui.getDocument(self.doc.Name).getInEdit().Object
        self.assertEqual(sketch.TypeId, 'Sketcher::SketchObject')
        self.assertEqual(sketch.getParentGeoFeatureGroup(), definition)
        return sketch

    def finish_sketch(self, sketch):
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        sketch.Document.recompute()
        Gui.runCommand('Sketcher_LeaveSketch')
        QtTest.QTest.qWait(200)
        self.assertIsNone(Gui.getDocument(self.doc.Name).getInEdit())

    def start_pad(self, sketch=None, sub=''):
        Gui.activateWorkbench('PartDesignWorkbench')
        Gui.Selection.clearSelection()
        if sketch: Gui.Selection.addSelection(sketch, sub)
        Gui.runCommand('PartDesign_Pad')
        QtTest.QTest.qWait(200)
        feature = Gui.getDocument(self.doc.Name).getInEdit().Object
        self.assertEqual(feature.TypeId, 'PartDesign::Pad')
        length = next(w for w in Gui.getMainWindow().findChildren(QtWidgets.QWidget)
                      if w.objectName() == 'lengthEdit' and w.isVisible())
        self.assertTrue(length.setProperty('rawValue', 5.0))
        QtTest.QTest.qWait(100)
        return feature

    def test_native_sketch_cancel_and_extrude_accept_undo(self):
        before = self.snapshot()
        self.new_sketch_command(False)
        self.assertEqual(self.snapshot(), before)
        sketch = self.new_sketch_command()
        self.assertFalse(any(o.TypeId == 'PartDesign::Body' for o in self.doc.Objects))
        self.finish_sketch(sketch)
        self.assertAlmostEqual(sketch.Placement.Base.z, 2)
        before = self.snapshot()
        feature = self.start_pad(sketch)
        name = feature.Name
        self.task_button(QtWidgets.QDialogButtonBox.Ok)
        self.assertFalse(Gui.Control.activeDialog())
        self.assertAlmostEqual(feature.Shape.Volume, 20 * math.pi)
        self.assertEqual(self.doc.UndoCount, before[-1] + 1)
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(self.snapshot(), before)
        self.doc.redo(); self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(name).Shape.Volume, 20 * math.pi)
        document.save_document(self.doc, self.output / 'Commands.cadprt')
        (self.output / 'expected.json').write_text(json.dumps({
            'ids': {o.Name: o.ID for o in self.doc.Objects}, 'feature': name, 'sketch': sketch.Name}))

    def test_native_extrude_cancel_restores_standalone_sketch(self):
        sketch = self.circle()
        for visible in (True, False):
            sketch.Visibility = visible
            before = self.snapshot()
            self.start_pad()  # Native command can find the single unconsumed profile.
            self.task_button(QtWidgets.QDialogButtonBox.Cancel)
            self.assertFalse(Gui.Control.activeDialog())
            self.assertEqual(self.snapshot(), before)
            self.assertEqual(sketch.getParentGeoFeatureGroup(), self.owner)
            self.assertFalse(App.getActiveTransaction())

    def test_native_face_attached_sketch_keeps_support_without_body(self):
        base = modeling.extrude_new_solid(self.doc, self.circle(), 5)
        bodies = [o.Name for o in self.doc.Objects if o.TypeId == 'PartDesign::Body']
        face = next('Face' + str(i) for i, f in enumerate(base.Shape.Faces, 1)
                    if isinstance(f.Surface, Part.Plane) and f.CenterOfMass.z > 4)
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(base, face)
        from TestComponentModeling import messages
        timer = QtCore.QTimer()
        def attachment_choice():
            dlg = QtWidgets.QApplication.activeModalWidget()
            if isinstance(dlg, QtWidgets.QInputDialog):
                dlg.accept()  # Keep the native suggested attachment mode.
        timer.timeout.connect(attachment_choice); timer.start(30)
        with messages() as errors:
            try:
                Gui.runCommand('Sketcher_NewSketch'); QtTest.QTest.qWait(200)
            finally:
                timer.stop(); timer.deleteLater()
        self.assertFalse(errors, errors)
        sketch = Gui.getDocument(self.doc.Name).getInEdit().Object
        self.assertEqual(sketch.getParentGeoFeatureGroup(), self.owner)
        self.assertEqual([o.Name for o in self.doc.Objects if o.TypeId == 'PartDesign::Body'], bodies)
        self.assertEqual(sketch.AttachmentSupport[0][0], base)
        self.finish_sketch(sketch)
        self.assertAlmostEqual(sketch.Placement.Base.z, 5)

    def test_native_selected_curve_and_invalid_task_cancel(self):
        sketch = self.circle()
        sketch.addGeometry(Part.Circle(App.Vector(12, 0, 0), App.Vector(0, 0, 1), 1), False)
        self.doc.recompute()
        before = self.snapshot()
        feature = self.start_pad(sketch, 'Edge1')
        self.assertEqual(list(feature.Profile[1]), ['Edge1'])
        self.assertAlmostEqual(feature.Shape.Volume, 20 * math.pi)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual(self.snapshot(), before)

        invalid = modeling.new_sketch(self.doc)
        invalid.addGeometry(Part.LineSegment(App.Vector(), App.Vector(2, 0, 0)), False)
        self.doc.recompute()
        before = self.snapshot()
        feature = self.start_pad(invalid)
        from TestComponentModeling import messages
        with messages() as errors:
            self.task_button(QtWidgets.QDialogButtonBox.Ok)
        self.assertTrue(errors)
        self.assertEqual(Gui.getDocument(self.doc.Name).getInEdit().Object, feature)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual(self.snapshot(), before)

    def test_native_multiple_profile_picker_cancel_and_accept(self):
        self.circle()
        second = self.circle(1)
        Gui.activateWorkbench('PartDesignWorkbench')
        Gui.Selection.clearSelection()
        before = self.snapshot()
        Gui.runCommand('PartDesign_Pad'); QtTest.QTest.qWait(200)
        self.assertIsNone(Gui.getDocument(self.doc.Name).getInEdit())
        self.assertIsNotNone(Gui.Control.activeDialog())
        self.assertEqual(self.snapshot(), before)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual(self.snapshot(), before)
        Gui.runCommand('PartDesign_Pad'); QtTest.QTest.qWait(200)
        listing = next(w for w in Gui.getMainWindow().findChildren(QtWidgets.QListWidget)
                       if w.objectName() == 'listWidget' and w.isVisible())
        self.assertEqual(listing.count(), 2)
        QtTest.QTest.mouseClick(listing.viewport(), QtCore.Qt.LeftButton,
                               pos=listing.visualItemRect(listing.item(1)).center())
        QtTest.QTest.mouseDClick(listing.viewport(), QtCore.Qt.LeftButton,
                                pos=listing.visualItemRect(listing.item(1)).center())
        QtTest.QTest.qWait(300)
        feature = Gui.getDocument(self.doc.Name).getInEdit().Object
        self.assertEqual(feature.Profile[0], second)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual(self.snapshot(), before)

    def test_external_native_sketch_and_pad_cancel_accept(self):
        document.save_document(self.doc, self.output / 'Assembly.cadprt')
        source = document.new_document('CommandSource')
        definition = hierarchy.create_definition(source, 'External command component')
        document.save_document(source, self.output / 'Source.cadprt')
        external.import_file(self.doc, source)
        App.setActiveDocument(self.doc.Name)
        editing.edit_unused(self.doc, definition)
        sketch = self.new_sketch_command()
        self.assertEqual(sketch.Document, source)
        self.finish_sketch(sketch)
        self.assertIn(sketch, Gui.Selection.getSelection('*'))
        before = self.snapshot(source)
        self.start_pad(sketch)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual(self.snapshot(source), before)
        feature = self.start_pad(sketch)
        self.task_button(QtWidgets.QDialogButtonBox.Ok)
        self.assertEqual(feature.Document, source)
        self.assertAlmostEqual(feature.Shape.Volume, 20 * math.pi)
        self.assertEqual(editing.context_path(self.doc), (definition, ()))
        document.save_document(source); document.save_document(self.doc)
        (self.output / 'expected.json').write_text(json.dumps({
            'source_ids': {o.Name: o.ID for o in source.Objects},
            'assembly_ids': {o.Name: o.ID for o in self.doc.Objects},
            'feature': feature.Name, 'sketch': sketch.Name}))


def verify_commands_fresh_process(output):
    output = Path(output)
    for test, filename in (
            ('test_native_sketch_cancel_and_extrude_accept_undo', 'Commands.cadprt'),
            ('test_external_native_sketch_and_pad_cancel_accept', 'Assembly.cadprt')):
        folder = output / test
        expected = json.loads((folder / 'expected.json').read_text())
        doc = document.open_document(folder / filename)
        source = doc
        if 'source_ids' in expected:
            source = next(d for d in App.listDocuments().values() if d != doc)
            assert {o.Name: o.ID for o in source.Objects} == expected['source_ids']
            assert {o.Name: o.ID for o in doc.Objects} == expected['assembly_ids']
        else:
            assert {o.Name: o.ID for o in doc.Objects} == expected['ids']
        feature = source.getObject(expected['feature'])
        assert feature.Profile[0] == source.getObject(expected['sketch'])
        assert feature.getParentGeoFeatureGroup().Tip == feature
        assert abs(feature.Shape.Volume - 20 * math.pi) < 1e-7
        feature.Length = 8; source.recompute(); doc.recompute()
        assert feature.Shape.isValid() and abs(feature.Shape.Volume - 32 * math.pi) < 1e-7
        document.validate(doc)
        App.closeDocument(doc.Name)
        if source != doc: App.closeDocument(source.Name)
