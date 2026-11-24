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
        self.task_prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.previous_task_mode = self.task_prefs.GetInt('TaskPanelUIMode', 0)
        self.task_prefs.SetInt('TaskPanelUIMode', 1)  # Explicit native compatibility coverage.
        Gui.activateWorkbench('PartDesignWorkbench')

    def tearDown(self):
        if Gui.Control.activeDialog():
            self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        if App.getActiveTransaction():
            App.closeActiveTransaction(True)
        self.task_prefs.SetInt('TaskPanelUIMode', self.previous_task_mode)
        TestFeatureCenteredModeling.tearDown(self)

    def task_button(self, role):
        buttons = [box.button(role) for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)]
        button = next(b for b in buttons if b and b.isVisible())
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(200)

    def new_sketch_command(self, accept=True):
        definition = editing.context_path(self.doc)[0]
        Gui.Selection.clearSelection()
        from freecad_plus import sketch_task
        Gui.runCommand('Sketcher_NewSketch')
        QtTest.QTest.qWait(100)
        task = sketch_task._active
        self.assertIsNotNone(task)
        task.choose('XY Plane')
        if not accept:
            task.reject()
            return
        self.assertTrue(task.accept())
        QtTest.QTest.qWait(200)
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
        length.clearFocus()  # Numerical inputs now commit when the field is left.
        QtTest.QTest.qWait(100)
        return feature

    def test_native_sketch_cancel_and_extrude_accept_undo(self):
        before = self.snapshot()
        self.new_sketch_command(False)
        self.assertEqual(self.snapshot(), before)
        sketch = self.new_sketch_command()
        self.assertFalse(any(o.TypeId == 'PartDesign::Body' for o in self.doc.Objects))
        self.finish_sketch(sketch)
        self.assertAlmostEqual(sketch.Placement.Base.z, 0)
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
        from freecad_plus import sketch_task
        Gui.runCommand('Sketcher_NewSketch'); QtTest.QTest.qWait(100)
        self.assertTrue(sketch_task._active.accept())
        QtTest.QTest.qWait(200)
        sketch = Gui.getDocument(self.doc.Name).getInEdit().Object
        self.assertEqual(sketch.getParentGeoFeatureGroup(), self.owner)
        self.assertEqual([o.Name for o in self.doc.Objects if o.TypeId == 'PartDesign::Body'], bodies)
        self.assertEqual(sketch.PlaneReferences[0][0], base)
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


class TestFeatureCenteredTargets(unittest.TestCase):
    setUp = TestFeatureCenteredCommands.setUp
    tearDown = TestFeatureCenteredCommands.tearDown
    circle = TestFeatureCenteredModeling.circle
    task_button = TestFeatureCenteredCommands.task_button

    def snapshot(self, doc=None):
        doc = doc or self.doc
        return (TestFeatureCenteredModeling.snapshot(self, doc),
                {o.Name: o.Tip.Name if o.Tip else None for o in doc.Objects if o.TypeId == 'PartDesign::Body'},
                {o.Name: tuple(o.Placement.Matrix.A) for o in doc.Objects if hasattr(o, 'Placement')},
                {o.Name: round(o.Shape.Volume, 9) for o in doc.Objects if hasattr(o, 'Shape')})

    def base(self, x=0):
        sketch = self.circle(3)
        sketch.Placement.Base = App.Vector(x, 0, 0)
        self.doc.recompute()
        return modeling.extrude_new_solid(self.doc, sketch, 10)

    def profile(self, radius=1, z=10, x=0):
        sketch = self.circle(radius)
        sketch.Placement.Base = App.Vector(x, 0, z)
        sketch.Document.recompute()
        return sketch

    def start(self, which, sketch, target=None, length=2):
        from TestComponentModeling import messages
        Gui.Selection.clearSelection()
        if target is not None: Gui.Selection.addSelection(target, 'Face1')
        Gui.Selection.addSelection(sketch)
        with messages() as errors:
            Gui.runCommand('PartDesign_' + which); QtTest.QTest.qWait(200)
        self.assertFalse(errors, errors)
        feature = Gui.getDocument(self.doc.Name).getInEdit().Object
        self.assertEqual(feature.TypeId, 'PartDesign::' + which)
        edit = next(w for w in Gui.getMainWindow().findChildren(QtWidgets.QWidget)
                    if w.objectName() == 'lengthEdit' and w.isVisible())
        self.assertTrue(edit.setProperty('rawValue', float(length)))
        QtTest.QTest.qWait(100)
        return feature

    def test_backend_add_subtract_chain_undo_and_save(self):
        base = self.base()
        body = base.getParentGeoFeatureGroup()
        add_sketch = self.profile(2)
        before = self.snapshot()
        add = modeling.extrude(self.doc, add_sketch, 4, operation='add', target=base)
        self.assertEqual(add.BaseFeature, base)
        self.assertEqual(body.Tip, add)
        self.assertAlmostEqual(add.Shape.Volume, 106 * math.pi)
        name = add.Name
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(self.snapshot(), before)
        self.doc.redo(); self.doc.recompute()
        add = self.doc.getObject(name)
        cut_sketch = self.profile(1, z=14)
        before = self.snapshot()
        cut = modeling.extrude(self.doc, cut_sketch, 3, operation='subtract', target=add)
        self.assertEqual(cut.BaseFeature, add)
        self.assertEqual(body.Tip, cut)
        self.assertAlmostEqual(cut.Shape.Volume, 103 * math.pi)
        name = cut.Name
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(self.snapshot(), before)
        self.doc.redo(); self.doc.recompute()
        cut = self.doc.getObject(name)
        self.assertEqual(len([o for o in self.owner.Group if o.TypeId == 'PartDesign::Body']), 1)
        document.save_document(self.doc, self.output / 'Targets.cadprt')
        (self.output / 'expected.json').write_text(json.dumps({
            'ids': {o.Name: o.ID for o in self.doc.Objects}, 'cut': name, 'add': add.Name,
            'base': base.Name, 'profile': cut_sketch.Name, 'body': body.Name}))

    def test_backend_failed_or_stale_target_is_atomic(self):
        base = self.base()
        sketch = self.profile(x=30)
        before = self.snapshot()
        with self.assertRaises(ValueError):
            modeling.extrude(self.doc, sketch, 2, operation='add', target=base)
        self.assertEqual(self.snapshot(), before)
        sketch.Placement.Base = App.Vector(0, 0, 10)
        self.doc.recompute()
        added = modeling.extrude(self.doc, sketch, 2, operation='add', target=base)
        fresh = self.profile(z=12)
        before = self.snapshot()
        for target in (base, self.owner, None):
            with self.assertRaises(ValueError):
                modeling.extrude(self.doc, fresh, 1, operation='subtract', target=target)
            self.assertEqual(self.snapshot(), before)
        other = hierarchy.create_definition(self.doc, 'Other target owner')
        editing.edit_unused(self.doc, other)
        foreign = self.base()
        editing.edit(self.root.Group[0])
        before = self.snapshot()
        with self.assertRaises(ValueError):
            modeling.extrude(self.doc, fresh, 1, operation='subtract', target=foreign)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(added.getParentGeoFeatureGroup().Tip, added)

    def test_target_body_placement_preserves_profile_position(self):
        base = self.base()
        body = base.getParentGeoFeatureGroup()
        body.Placement = App.Placement(App.Vector(20, 0, 0), App.Rotation(App.Vector(0, 0, 1), 35))
        self.doc.recompute()
        sketch = self.profile(x=20)
        original = sketch.getGlobalPlacement()
        before = self.snapshot()
        result = modeling.extrude(self.doc, sketch, 2, operation='subtract', target=base)
        self.assertLess((sketch.getGlobalPlacement().Base - original.Base).Length, 1e-7)
        self.assertLess(sketch.getGlobalPlacement().Rotation.Angle, 1e-7)
        self.assertAlmostEqual(result.Shape.Volume, 88 * math.pi)
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(self.snapshot(), before)

    def test_native_explicit_target_ignores_active_body(self):
        first = self.base()
        second = self.base(30)
        second_body = second.getParentGeoFeatureGroup()
        sketch = self.profile()
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject('pdbody'), second_body)
        before = self.snapshot()
        result = self.start('Pad', sketch, first)
        self.assertEqual(result.BaseFeature, first)
        self.assertEqual(result.getParentGeoFeatureGroup(), first.getParentGeoFeatureGroup())
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject('pdbody'),
                         first.getParentGeoFeatureGroup())
        self.task_button(QtWidgets.QDialogButtonBox.Ok)
        self.assertAlmostEqual(result.Shape.Volume, 92 * math.pi)
        self.assertAlmostEqual(second.Shape.Volume, 90 * math.pi)
        self.assertEqual(second_body.Tip, second)
        name = result.Name
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(self.snapshot(), before)
        self.doc.redo(); self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(name).Shape.Volume, 92 * math.pi)

    def test_attached_profile_keeps_target_support(self):
        target = self.base()
        sketch = self.circle(1)
        face = next('Face' + str(i) for i, f in enumerate(target.Shape.Faces, 1)
                    if isinstance(f.Surface, Part.Plane) and f.CenterOfMass.z > 9)
        sketch.AttachmentSupport = [(target, [face])]
        sketch.MapMode = 'FlatFace'
        self.doc.recompute()
        original = sketch.getGlobalPlacement()
        result = modeling.extrude(self.doc, sketch, 2, operation='add', target=target)
        self.assertEqual(sketch.AttachmentSupport[0][0], target)
        self.assertLess((sketch.getGlobalPlacement().Base - original.Base).Length, 1e-7)
        self.assertAlmostEqual(result.Shape.Volume, 92 * math.pi)

    def test_native_cancel_preserves_hidden_profile_and_target(self):
        target = self.base()
        sketch = self.profile()
        for which in ('Pad', 'Pocket'):
            sketch.Visibility = False
            target.Visibility = False
            before = self.snapshot()
            result = self.start(which, sketch, target)
            self.assertEqual(result.BaseFeature, target)
            self.task_button(QtWidgets.QDialogButtonBox.Cancel)
            self.assertEqual(self.snapshot(), before)
            self.assertFalse(App.getActiveTransaction())

    def test_native_unique_target_and_ambiguous_target_rejection(self):
        from TestComponentModeling import messages
        target = self.base()
        sketch = self.profile()
        result = self.start('Pocket', sketch)
        self.assertEqual(result.BaseFeature, target)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.base(30)
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(sketch)
        before = self.snapshot()
        with messages() as errors:
            Gui.runCommand('PartDesign_Pocket'); QtTest.QTest.qWait(150)
        self.assertTrue(any('target' in error for error in errors), errors)
        self.assertFalse(Gui.Control.activeDialog())
        self.assertEqual(self.snapshot(), before)

    def test_native_target_survives_profile_picker(self):
        target = self.base()
        self.base(30)
        self.profile(2)
        chosen = self.profile(1)
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(target)
        Gui.runCommand('PartDesign_Pocket'); QtTest.QTest.qWait(200)
        listing = next(w for w in Gui.getMainWindow().findChildren(QtWidgets.QListWidget)
                       if w.objectName() == 'listWidget' and w.isVisible())
        self.assertEqual(listing.count(), 2)
        QtTest.QTest.mouseClick(listing.viewport(), QtCore.Qt.LeftButton,
                               pos=listing.visualItemRect(listing.item(1)).center())
        self.task_button(QtWidgets.QDialogButtonBox.Ok)
        result = Gui.getDocument(self.doc.Name).getInEdit().Object
        self.assertEqual(result.Profile[0], chosen)
        self.assertEqual(result.BaseFeature, target)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)

    def test_target_occurrence_eligibility_is_checked_before_resolution(self):
        from freecad_plus import display
        from TestComponentModeling import messages
        target = self.base()
        sketch = self.profile()
        other = hierarchy.add_instance(self.root, self.owner)
        display.set_state(self.root, other, part_type='Reference')
        body = target.getParentGeoFeatureGroup()
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(sketch)
        Gui.Selection.addSelection(self.root, other.Name + '.' + body.Name + '.' + target.Name + '.Face1')
        before = self.snapshot()
        with messages() as errors:
            Gui.runCommand('PartDesign_Pocket'); QtTest.QTest.qWait(150)
        self.assertTrue(any('Reference' in error or 'Excluded' in error for error in errors), errors)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(Gui.Control.activeDialog())

    def test_native_picker_rechecks_edited_component(self):
        from TestComponentModeling import messages
        target = self.base()
        self.profile(1); self.profile(2)
        other = hierarchy.create_definition(self.doc, 'Other edit context')
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(target)
        Gui.runCommand('PartDesign_Pocket'); QtTest.QTest.qWait(200)
        listing = next(w for w in Gui.getMainWindow().findChildren(QtWidgets.QListWidget)
                       if w.objectName() == 'listWidget' and w.isVisible())
        editing.edit_unused(self.doc, other)
        before = self.snapshot()
        QtTest.QTest.mouseClick(listing.viewport(), QtCore.Qt.LeftButton,
                               pos=listing.visualItemRect(listing.item(0)).center())
        with messages() as errors:
            self.task_button(QtWidgets.QDialogButtonBox.Ok)
        self.assertTrue(any('changed' in error for error in errors), errors)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(Gui.Control.activeDialog())

    def test_external_target_operations_stay_in_defining_file(self):
        document.save_document(self.doc, self.output / 'Assembly.cadprt')
        source = document.new_document('TargetSource')
        definition = hierarchy.create_definition(source, 'External target')
        document.save_document(source, self.output / 'Source.cadprt')
        external.import_file(self.doc, source)
        App.setActiveDocument(self.doc.Name); editing.edit_unused(self.doc, definition)
        target = self.base()
        sketch = self.profile()
        before = self.snapshot(source)
        assembly_ids = {o.Name: o.ID for o in self.doc.Objects}
        cut = self.start('Pocket', sketch, target)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual(self.snapshot(source), before)
        cut = self.start('Pocket', sketch, target)
        self.task_button(QtWidgets.QDialogButtonBox.Ok)
        self.assertEqual(cut.Document, source)
        self.assertEqual(cut.BaseFeature, target)
        self.assertAlmostEqual(cut.Shape.Volume, 88 * math.pi)
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, assembly_ids)
        self.assertEqual(editing.context_path(self.doc), (definition, ()))
        cut_name = cut.Name
        source.undo(); source.recompute()
        self.assertEqual(self.snapshot(source), before)
        source.redo(); source.recompute()
        cut = source.getObject(cut_name)
        document.save_document(source); document.save_document(self.doc)
        (self.output / 'expected.json').write_text(json.dumps({
            'source_ids': {o.Name: o.ID for o in source.Objects}, 'assembly_ids': assembly_ids,
            'cut': cut.Name, 'target': target.Name}))


def verify_targets_fresh_process(output):
    output = Path(output)
    folder = output / 'test_backend_add_subtract_chain_undo_and_save'
    expected = json.loads((folder / 'expected.json').read_text())
    doc = document.open_document(folder / 'Targets.cadprt')
    assert {o.Name: o.ID for o in doc.Objects} == expected['ids']
    cut = doc.getObject(expected['cut'])
    assert cut.BaseFeature == doc.getObject(expected['add'])
    assert cut.Profile[0] == doc.getObject(expected['profile'])
    assert doc.getObject(expected['body']).Tip == cut
    assert abs(cut.Shape.Volume - 103 * math.pi) < 1e-7
    cut.Length = 4; doc.recompute()
    assert cut.Shape.isValid() and abs(cut.Shape.Volume - 102 * math.pi) < 1e-7
    App.closeDocument(doc.Name)
    folder = output / 'test_external_target_operations_stay_in_defining_file'
    expected = json.loads((folder / 'expected.json').read_text())
    doc = document.open_document(folder / 'Assembly.cadprt')
    source = next(d for d in App.listDocuments().values() if d != doc)
    assert {o.Name: o.ID for o in doc.Objects} == expected['assembly_ids']
    assert {o.Name: o.ID for o in source.Objects} == expected['source_ids']
    cut = source.getObject(expected['cut'])
    assert cut.BaseFeature == source.getObject(expected['target'])
    cut.Length = 4; source.recompute(); doc.recompute()
    assert cut.Shape.isValid() and abs(cut.Shape.Volume - 86 * math.pi) < 1e-7
    document.validate(doc)
    App.closeDocument(doc.Name); App.closeDocument(source.Name)


class TestSequentialHistory(unittest.TestCase):
    """Component-wide order and pre-mutation native input admission."""
    setUp = TestFeatureCenteredModeling.setUp
    tearDown = TestFeatureCenteredModeling.tearDown
    circle = TestFeatureCenteredModeling.circle
    snapshot = TestFeatureCenteredModeling.snapshot

    def chain(self):
        from freecad_plus import extrusion, revolution
        base = self.circle(4)
        first = extrusion.save(self.doc, [(base, '')], {}, dict(extrusion.DEFAULTS, length=6))
        profile = modeling.new_sketch(self.doc)
        profile.Placement = App.Placement(App.Vector(), App.Rotation(App.Vector(1,0,0),90))
        points = [(2,1),(5,1),(5,3),(2,3)]
        for i, p in enumerate(points):
            q = points[(i+1)%4]
            profile.addGeometry(Part.LineSegment(App.Vector(*p,0),App.Vector(*q,0)),False)
        self.doc.recompute()
        second = revolution.save(self.doc, [(profile,'')], {'target':(first,'')},
            dict(revolution.DEFAULTS, operation='Add', axis='Component Z axis', angle=90))
        last_profile = self.circle(2); last_profile.Placement.Base.z = 5; self.doc.recompute()
        third = extrusion.save(self.doc, [(last_profile,'')], {'target':(second,'')},
            dict(extrusion.DEFAULTS, operation='Add', length=5))
        return [base, first, profile, second, last_profile, third]

    def test_interleaved_bodies_undo_and_saved_order(self):
        from freecad_plus import extrusion
        chain = self.chain()
        names = [o.Name for o in chain]
        self.assertEqual(document.history(self.doc,self.owner),chain)
        before = self.snapshot(); volumes = [o.Shape.Volume for o in chain[1::2]]
        self.owner.Group = list(reversed(self.owner.Group))
        self.assertEqual(document.history(self.doc,self.owner),chain)
        self.assertEqual([o.Shape.Volume for o in chain[1::2]],volumes)
        self.assertEqual(self.snapshot()[0],before[0])
        extrusion.save(self.doc,[(chain[4],'')],{'target':(chain[3],'')},
            dict(extrusion.DEFAULTS,operation='Add',length=7),chain[5])
        self.assertEqual(document.history(self.doc,self.owner),chain)
        self.doc.undo(); self.doc.recompute()
        self.assertEqual([o.Name for o in document.history(self.doc,self.owner)],names)
        self.doc.redo(); self.doc.recompute()
        expected = {o.Name:o.ID for o in self.doc.Objects}
        owner_name = self.owner.Name
        path = document.save_document(self.doc,self.output/'Sequential.cadprt')
        App.closeDocument(self.doc.Name); self.doc = document.open_document(path)
        self.owner = self.doc.getObject(owner_name)
        self.assertEqual([o.Name for o in document.history(self.doc,self.owner)],names)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},expected)
        (self.output/'expected.json').write_text(json.dumps(dict(owner=owner_name,order=names,ids=expected)))

    def test_forward_profile_target_axis_and_limit_are_atomic(self):
        from freecad_plus import extrusion, revolution, planes
        chain = self.chain(); old = chain[1]; revolve = chain[3]
        later = self.circle(1)
        xy = next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        late_plane = planes.save(self.doc,[(xy,'')],10)
        late_axis = self.owner.newObject('PartDesign::Line','LaterAxis')
        late_target = extrusion.save(self.doc,[(later,'')],{},dict(extrusion.DEFAULTS,length=3))
        before = self.snapshot()
        cases = [
            lambda: extrusion.save(self.doc,[(later,'')],{},extrusion.settings(old),old),
            lambda: extrusion.save(self.doc,[(chain[0],'')],{'target':(late_target,'')},
                dict(extrusion.settings(old),operation='Add'),old),
            lambda: extrusion.save(self.doc,[(chain[0],'')],{'limit':(late_plane,'')},
                dict(extrusion.settings(old),end='Up to face'),old),
            lambda: revolution.save(self.doc,[(chain[2],'')],
                {'target':(old,''),'axis':(late_axis,'')},
                dict(revolution.settings(revolve),axis='Selected axis / line'),revolve)]
        for attempt in cases:
            with self.assertRaisesRegex(ValueError,'must precede'): attempt()
            self.assertEqual(self.snapshot(),before)
        self.assertEqual(old.ProfileReferences[0][0],chain[0])
        self.assertFalse(revolve.AxisReference)

    def test_sketch_plane_and_native_input_guards(self):
        from freecad_plus import planes, sketch_placement, geometry
        xy = next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        early_plane = planes.save(self.doc,[(xy,'')],1)
        sketch = sketch_placement.save(self.doc,[(early_plane,'')])
        late_plane = planes.save(self.doc,[(xy,'')],2)
        before = self.snapshot()
        for attempt in (
            lambda: sketch_placement.save(self.doc,[(late_plane,'')],feature=sketch),
            lambda: planes.save(self.doc,[(late_plane,'')],feature=early_plane),
            lambda: geometry.require_modeling_inputs(sketch,[(late_plane,'')])):
            with self.assertRaisesRegex(ValueError,'must precede'): attempt()
            self.assertEqual(self.snapshot(),before)
        geometry.require_modeling_inputs(sketch,[(early_plane,'')])
        geometry.require_modeling_inputs(sketch,[(xy,'')])

    def test_native_expression_and_body_result_dependencies(self):
        from freecad_plus import geometry
        early = self.owner.newObject('Part::Feature','Early')
        early.addProperty('App::PropertyLength','Value')
        source = self.owner.newObject('Part::Feature','Source')
        source.addProperty('App::PropertyLength','Value'); source.Value=4
        # A pre-existing legacy forward link is repaired in the projection, without
        # rewriting IDs/links or ownership. Expressions are native OutList edges.
        early.setExpression('Value','Source.Value * 2')
        before = self.snapshot()
        self.assertEqual(document.history(self.doc,self.owner),[source,early])
        self.assertEqual(self.snapshot(),before)
        geometry.require_modeling_inputs(early,[(source,'')])
        with self.assertRaisesRegex(ValueError,'must precede'):
            geometry.require_modeling_inputs(source,[(early,'')])
        sketch = self.circle()
        pad = modeling.extrude_new_solid(self.doc,sketch,4)
        result = self.owner.newObject('Part::Feature','Result')
        result.addProperty('App::PropertyLink','Input'); result.Input=pad.getParentGeoFeatureGroup()
        order = document.history(self.doc,self.owner)
        self.assertLess(order.index(sketch),order.index(pad))
        self.assertLess(order.index(pad),order.index(result))
        geometry.require_modeling_inputs(pad.getParentGeoFeatureGroup(),[(sketch,'')])

    def test_cycles_are_not_silently_ordered(self):
        a = self.owner.newObject('Part::Feature','A'); b = self.owner.newObject('Part::Feature','B')
        a.addProperty('App::PropertyLink','Input'); b.addProperty('App::PropertyLink','Input')
        a.Input=b; b.Input=a
        try:
            with self.assertRaisesRegex(ValueError,'Circular feature'):
                document.history(self.doc,self.owner)
        finally: b.Input=None
        self.assertEqual(document.history(self.doc,self.owner),[b,a])

    def test_native_compound_drop_rejects_future_input(self):
        first=self.owner.newObject('Part::Box','First')
        result=self.owner.newObject('Part::Compound','Compound');result.Links=[first]
        later=self.owner.newObject('Part::Box','Later');self.doc.recompute()
        before=self.snapshot()
        self.assertFalse(result.ViewObject.canDropObject(later))
        with self.assertRaisesRegex(Exception,'must precede'):
            result.ViewObject.dropObject(later)
        self.assertEqual(result.Links,[first]);self.assertEqual(self.snapshot(),before)

    def test_history_picker_rejects_later_profile(self):
        from freecad_plus import extrusion, extrude_task, panel
        chain = self.chain(); later = self.circle()
        task = extrude_task.show(chain[1])
        try:
            task.clear_profile(); task.pick='profile'
            Gui.Selection.clearSelection(); Gui.Selection.addSelection(later)
            QtTest.QTest.qWait(100)
            self.assertFalse(task.refs)
            self.assertIn('must precede',task.status.text())
            self.assertEqual(chain[1].ProfileReferences[0][0],chain[0])
        finally: task.reject()
        widget=panel.show_panel(); widget.tabs.setCurrentIndex(2); widget.refresh()
        rows=[widget.trees[2].topLevelItem(i).data(0,panel._ROLE).ref[2]
              for i in range(2,widget.trees[2].topLevelItemCount())]
        self.assertEqual(rows,[o.Name for o in document.history(self.doc,self.owner)])
        self.assertEqual(widget.trees[2].dragDropMode(),QtWidgets.QAbstractItemView.InternalMove)
        self.assertFalse(widget.trees[2].topLevelItem(0).flags() & QtCore.Qt.ItemIsDragEnabled)
        self.assertFalse(widget.trees[2].topLevelItem(1).flags() & QtCore.Qt.ItemIsDragEnabled)
        self.assertTrue(all(widget.trees[2].topLevelItem(i).flags() & QtCore.Qt.ItemIsDragEnabled
                            for i in range(2,widget.trees[2].topLevelItemCount())))
