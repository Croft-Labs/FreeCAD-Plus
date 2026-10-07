# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bounded native Helix and primitive migration, editors and recovery."""
import hashlib
import importlib
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
import ComponentHelix as Helix
import ComponentPrimitive as Primitive
import LegacyConversion
from TestLegacyExtrusions import TestLegacyExtrusions


class TestLegacyHelixPrimitives(unittest.TestCase):
    setUp = TestLegacyExtrusions.setUp
    same = TestLegacyExtrusions.same
    open_row = TestLegacyExtrusions.open_row

    def tearDown(self):
        for name in ('ComponentHelixTask', 'ComponentPrimitiveTask'):
            task = importlib.import_module('freecad.gui.' + name)
            if task._task: task._task.reject()
        TestLegacyExtrusions.tearDown(self)

    def containers(self):
        part = self.doc.addObject('App::Part', 'Part')
        part.Placement = App.Placement(App.Vector(20, 2, 1), App.Rotation(App.Vector(0, 1, 0), 35))
        body = self.doc.addObject('PartDesign::Body', 'Body'); part.addObject(body)
        for i, transform in enumerate((False, True)):
            link = self.doc.addObject('App::Link', 'Use' + str(i)); link.setLink(part)
            link.LinkTransform = transform; link.LinkPlacement.Base.x = 50 + 20 * i
        return part, body

    def helix(self, subtract=False, retained=False, mode='pitch-height-angle'):
        part, body = self.containers()
        if subtract:
            box = body.newObject('PartDesign::AdditiveBox', 'BaseBox')
            box.Length = box.Width = box.Height = 10
            box.Placement.Base = App.Vector(-5, -1, -5)
        sketch = body.newObject('Sketcher::SketchObject', 'Profile')
        points = [App.Vector(2, 0, 0), App.Vector(3, 0, 0), App.Vector(3, 1, 0), App.Vector(2, 1, 0)]
        for a, b in zip(points, points[1:] + points[:1]): sketch.addGeometry(Part.LineSegment(a, b), False)
        feature = body.newObject('PartDesign::SubtractiveHelix' if subtract else 'PartDesign::AdditiveHelix', 'Helix')
        feature.Profile = sketch; feature.ReferenceAxis = (sketch, ['V_Axis'])
        feature.Mode = mode; feature.Pitch = 3; feature.Height = 6; feature.Turns = 2
        feature.HasBeenEdited = True; body.Tip = feature
        if retained: body.Placement.Base.x = 7
        self.doc.recompute(); self.assertNotIn('Invalid', body.State); self.assertFalse(body.Shape.isNull())
        return part, body, sketch, feature

    def primitives(self, kind='Box', retained=False, chain=True):
        part, body = self.containers()
        added = body.newObject('PartDesign::Additive' + kind, 'Primitive')
        cut = None
        if chain:
            cut = body.newObject('PartDesign::SubtractiveBox', 'Cut')
            cut.Length = 2; cut.Width = 2; cut.Height = 12; cut.Placement.Base = App.Vector(1, 1, 0)
        body.Tip = cut or added
        if retained: body.Placement.Base.x = 7
        self.doc.recompute(); self.assertNotIn('Invalid', body.State); self.assertFalse(body.Shape.isNull())
        return part, body, added, cut

    def verify(self, part, body, feature):
        self.assertEqual(body.Producer, feature, str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(Model.owner(feature), part)
        self.assertEqual(Model.finished_results(part), [body]); Model.validate(self.doc)

    def test_helix_all_parameter_modes_identity_axis_preview_shared_instances(self):
        for mode in Helix.INPUT_MODES:
            with self.subTest(mode=mode):
                part, body, sketch, feature = self.helix(mode=mode)
                feature.LeftHanded = True; feature.Reversed = True; feature.Refine = False
                self.doc.recompute(); before = {o.Name: Part.getShape(o).copy() for o in (body, part, self.doc.Use0, self.doc.Use1)}
                identity = feature.Name, feature.TypeId, feature.ID, feature.Label
                axis = feature.ReferenceAxis; CadDocument.convert_legacy(self.doc); self.verify(part, body, feature)
                self.assertEqual(identity, (feature.Name, feature.TypeId, feature.ID, feature.Label)); self.assertEqual(axis, feature.ReferenceAxis)
                self.assertLess(part.ModelHistory.index(sketch.Name), part.ModelHistory.index(feature.Name))
                for name, shape in before.items(): self.same(shape, Part.getShape(self.doc.getObject(name)))
                inputs, kind, target, options = Helix.read(feature)
                self.assertEqual(options['input_mode'], mode); self.assertTrue(options['left']); self.assertTrue(options['reversed'])
                self.same(Helix.preview(part, inputs, kind, target, options), feature.Shape)
                App.closeDocument(self.doc.Name); self.doc = App.newDocument('LegacyHelix'); self.doc.UndoMode = 1

    def test_eight_primitive_kinds_native_dimensions_placement_preview(self):
        for kind in Primitive.PARAMETERS:
            with self.subTest(kind=kind):
                part, body, feature, _ = self.primitives(kind, chain=False)
                feature.Placement = App.Placement(App.Vector(2, 3, 1), App.Rotation(App.Vector(0, 0, 1), 20))
                self.doc.recompute(); before = body.Shape.copy()
                identity = feature.Name, feature.TypeId, feature.ID, feature.Label
                dims = {name: float(getattr(feature, name)) for name in Primitive.PARAMETERS[kind]}
                CadDocument.convert_legacy(self.doc); self.verify(part, body, feature)
                self.assertEqual(identity, (feature.Name, feature.TypeId, feature.ID, feature.Label)); self.same(before, body.Shape)
                inputs, mode, target, options = Primitive.read(feature)
                self.assertEqual(options['kind'], kind); self.assertEqual(options['dimensions'], dims)
                self.same(Primitive.preview(part, inputs, mode, target, options), feature.Shape)
                App.closeDocument(self.doc.Name); self.doc = App.newDocument('LegacyPrimitives'); self.doc.UndoMode = 1

    def test_primitive_chain_modes_original_type_consumption_undo_cold_reopen(self):
        part, body, added, cut = self.primitives(); original = list(body.Group); before = body.Shape.copy()
        CadDocument.convert_legacy(self.doc); self.verify(part, body, cut)
        self.assertEqual(cut.BaseFeature.Producer, added); identity = cut.Name, cut.TypeId, cut.ID, cut.ObjectId
        self.doc.undo(); self.doc.recompute(); self.assertEqual(body.Group, original); self.same(before, body.Shape)
        self.doc.redo(); self.doc.recompute()
        target = cut.BaseFeature; options = Primitive.read(cut)[3]
        Primitive.edit(cut, [], 'Add', target, options)
        self.assertEqual(cut.Operation, 'Union'); self.assertEqual(identity, (cut.Name, cut.TypeId, cut.ID, cut.ObjectId))
        Primitive.edit(cut, [], 'New Body', options=options)
        self.assertIsNone(cut.BaseFeature); self.assertEqual(cut.ConsumedResults, [])
        Primitive.edit(cut, [], 'Subtract', target, dict(options, boolean='Common'))
        saved = self.output / 'PrimitiveModes.cadprt'; self.doc.saveAs(str(saved)); App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(saved); cut = self.doc.getObject(identity[0])
        self.assertEqual(cut.Operation, 'Common'); self.assertEqual(cut.ObjectId, identity[3])
        Primitive.edit(cut, [], 'Subtract', cut.BaseFeature, dict(Primitive.read(cut)[3], boolean='Subtraction'))
        self.same(before, self.doc.Body.Shape)

    def test_helix_subtractive_target_original_type_and_cold_reopen(self):
        part, body, sketch, feature = self.helix(subtract=True); before = body.Shape.copy()
        original = self.output / 'Helix.FCStd'; self.doc.saveAs(str(original)); digest = hashlib.sha256(original.read_bytes()).hexdigest()
        CadDocument.convert_legacy(self.doc); self.verify(part, body, feature)
        self.assertEqual(feature.HelixMode, 'Subtract'); self.assertEqual(feature.BaseFeature.Producer, self.doc.BaseBox)
        oid = feature.ObjectId; inputs, mode, target, options = Helix.read(feature)
        Helix.edit(feature, inputs, 'New Body', options=options)
        self.assertEqual(feature.TypeId, 'PartDesign::SubtractiveHelix'); self.assertEqual(feature.ObjectId, oid)
        Helix.edit(feature, inputs, 'Subtract', target, options); self.same(before, body.Shape)
        saved = self.output / 'Helix.cadprt'; self.doc.saveAs(str(saved)); App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(saved); self.assertEqual(self.doc.Helix.ObjectId, oid); self.same(before, self.doc.Body.Shape)
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)
        self.doc.Helix.Height = 7; self.doc.recompute(); self.assertNotIn('Invalid', self.doc.Body.State)

    def test_formulas_shape_switch_cycle_and_failed_geometry_rollback(self):
        part, body, added, cut = self.primitives(); added.setExpression('Length', '12 mm'); self.doc.recompute()
        formulas = list(added.ExpressionEngine); CadDocument.convert_legacy(self.doc); self.verify(part, body, cut)
        self.assertEqual(formulas, list(added.ExpressionEngine))
        with self.assertRaisesRegex(ValueError, 'expressions'): Primitive.edit(added, [], 'New Body')
        with self.assertRaisesRegex(ValueError, 'separate primitive'): Primitive.edit(cut, [], 'Subtract', cut.BaseFeature, Primitive.defaults('Cylinder'))
        with self.assertRaises(ValueError): Primitive.edit(cut, [], 'Subtract', body)
        before = body.Shape.copy(); identity = cut.Name, cut.TypeId, cut.ObjectId; count = len(self.doc.Objects)
        bad = dict(Primitive.read(cut)[3], placement=App.Placement(App.Vector(100, 0, 0), App.Rotation()))
        with self.assertRaises(ValueError): Primitive.edit(cut, [], 'Subtract', cut.BaseFeature, bad)
        self.assertEqual(count, len(self.doc.Objects)); self.assertEqual(identity, (cut.Name, cut.TypeId, cut.ObjectId)); self.same(before, body.Shape)

    def test_retained_native_editors_sources_and_stale_output(self):
        for family in ('Helix', 'Primitive'):
            if family == 'Helix': part, body, sketch, feature = self.helix(retained=True)
            else: part, body, feature, _ = self.primitives(retained=True, chain=False)
            before = body.Shape.copy(); CadDocument.convert_legacy(self.doc)
            alias = next(o for o in Model.history(part) if getattr(o, 'Legacy' + family + 'Source', None) == feature)
            self.assertEqual(Model.owner(feature), body); self.same(before, body.Shape)
            self.open_row(part, alias); self.assertEqual(Gui.getDocument(self.doc.Name).getInEdit().Object, feature)
            Gui.getDocument(self.doc.Name).resetEdit()
            if Gui.Control.activeDialog(): Gui.Control.closeDialog()
            self.doc.recompute(); setattr(alias, 'Legacy' + family + 'Source', None)
            self.assertEqual(Model.history_state(alias), 'Needs repair')
            App.closeDocument(self.doc.Name); self.doc = App.newDocument('Retained'); self.doc.UndoMode = 1
        part, body, added, cut = self.primitives(); added.touch(); CadDocument.convert_legacy(self.doc)
        self.assertEqual(Model.owner(cut), body); self.assertTrue(any('unverified' in entry for entry in Model.metadata(self.doc).ConversionReport))

    def test_actual_shared_history_preview_accept_cancel(self):
        for family in ('Helix', 'Primitive'):
            if family == 'Helix': part, body, sketch, feature = self.helix()
            else: part, body, feature, _ = self.primitives(chain=False)
            CadDocument.convert_legacy(self.doc); self.verify(part, body, feature)
            Task = importlib.import_module('freecad.gui.Component' + family + 'Task')
            self.open_row(part, feature); self.assertIsNotNone(Task._task)
            self.assertTrue(Task._task.preview(), Task._task.status.text())
            Task._task.form.grab().save(str(self.output / ('legacy-' + family.lower() + '-task.png')))
            self.assertTrue(Task._task.accept()); self.doc.undo(); self.doc.recompute(); self.doc.redo(); self.doc.recompute()
            before = body.Shape.copy(); self.open_row(part, feature); Task._task.reject(); self.same(before, body.Shape)
            App.closeDocument(self.doc.Name); self.doc = App.newDocument('History'); self.doc.UndoMode = 1

    def test_previous_file_upgrade_identity_idempotence(self):
        part, body, sketch, feature = self.helix()
        with patch.object(LegacyConversion, 'migrate_helixes'): CadDocument.convert_legacy(self.doc)
        oid = sketch.ObjectId; aliases = {o.Name: o.ObjectId for o in Model.history(part) if getattr(o, 'LegacySketchSource', None)}
        saved = self.output / 'PreviousHelix.cadprt'; self.doc.saveAs(str(saved)); App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(saved); self.verify(self.doc.Part, self.doc.Body, self.doc.Helix)
        self.assertEqual(self.doc.Profile.ObjectId, oid)
        for name, value in aliases.items(): self.assertEqual(self.doc.getObject(name).ObjectId, value)
        count = len(self.doc.Objects); CadDocument.convert_legacy(self.doc); self.assertEqual(count, len(self.doc.Objects))

    def test_standalone_native_primitives_and_helix_curve(self):
        part = self.doc.addObject('App::Part', 'Part')
        originals = []
        for kind in Primitive.PARAMETERS:
            obj = self.doc.addObject('Part::' + kind, kind); part.addObject(obj); originals.append(obj)
        helix = self.doc.addObject('Part::Helix', 'Curve'); part.addObject(helix)
        helix.Pitch = 3; helix.Height = 6; helix.Radius = 2
        self.doc.recompute(); shapes = {o.Name: o.Shape.copy() for o in originals}
        CadDocument.convert_legacy(self.doc)
        for obj in originals:
            self.same(shapes[obj.Name], obj.Shape)
            self.assertTrue(obj.LegacyPrimitiveState)
            self.assertIn(obj.Name, part.ResultObjects)
            self.assertFalse(any(getattr(o, 'Producer', None) == obj for o in Model.history(part)))
        self.assertTrue(helix.LegacyHelixState); self.assertTrue(helix.Shape.Edges); self.assertFalse(helix.Shape.Solids)

    def test_attached_primitive_and_external_helix_axis_retained(self):
        part, body, added, _ = self.primitives(chain=False)
        plane = body.newObject('PartDesign::Plane', 'DatumPlane'); plane.Placement.Base.z = 2
        added.AttachmentSupport = [(plane, '')]; added.MapMode = 'ObjectXY'; body.Tip = added
        self.doc.recompute(); support = list(added.AttachmentSupport); before = body.Shape.copy()
        CadDocument.convert_legacy(self.doc); self.assertEqual(Model.owner(added), body)
        self.assertEqual(list(added.AttachmentSupport), support); self.same(before, body.Shape)
        App.closeDocument(self.doc.Name); self.doc = App.newDocument('ReferenceAxis'); self.doc.UndoMode = 1
        part, body, sketch, feature = self.helix()
        axis = body.newObject('PartDesign::Line', 'Axis')
        axis.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), -90)
        feature.ReferenceAxis = (axis, ['']); body.Tip = feature; self.doc.recompute()
        self.assertNotIn('Invalid', body.State); before = body.Shape.copy(); ref = feature.ReferenceAxis
        CadDocument.convert_legacy(self.doc); self.assertEqual(Model.owner(feature), body)
        self.assertEqual(ref, feature.ReferenceAxis); self.same(before, body.Shape)

    def test_previous_primitive_upgrade_and_original_additive_type_edit(self):
        part, body, added, _ = self.primitives(chain=False)
        with patch.object(LegacyConversion, 'migrate_primitives'): CadDocument.convert_legacy(self.doc)
        bid = body.ObjectId; saved = self.output / 'PreviousPrimitive.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        part, body, added = self.doc.Part, self.doc.Body, self.doc.Primitive
        self.verify(part, body, added); self.assertEqual(body.ObjectId, bid)
        identity = added.Name, added.TypeId, added.ID, added.ObjectId
        options = Primitive.defaults('Box'); options['dimensions'] = dict(Length=12, Width=12, Height=12)
        options['placement'].Base = App.Vector(-1, -1, -1)
        operation, target = Primitive.create(part, options=options); Model.reorder_history(part, [operation], 0)
        Primitive.edit(added, [], 'Subtract', target)
        self.assertEqual(identity, (added.Name, added.TypeId, added.ID, added.ObjectId))
        self.assertEqual(added.Operation, 'Subtraction'); self.assertAlmostEqual(body.Shape.Volume, 728, places=6)
