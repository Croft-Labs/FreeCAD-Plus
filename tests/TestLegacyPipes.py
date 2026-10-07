# SPDX-License-Identifier: LGPL-2.1-or-later
"""Legacy native Pipe references, history, editing and persistence acceptance."""
import hashlib
import importlib
import math
from unittest.mock import patch
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import CadDocument
import ComponentModel as Model
import ComponentPipe as Pipe
import LegacyConversion
from TestLegacyExtrusions import TestLegacyExtrusions


class TestLegacyPipes(unittest.TestCase):
    setUp = TestLegacyExtrusions.setUp
    same = TestLegacyExtrusions.same
    open_row = TestLegacyExtrusions.open_row

    def tearDown(self):
        task = importlib.import_module('freecad.gui.ComponentPipeTask')
        if task._task:
            task._task.reject()
        TestLegacyExtrusions.tearDown(self)

    def circle(self, owner, name, radius=4, z=0):
        obj = self.doc.addObject('Sketcher::SketchObject', name)
        owner.addObject(obj)
        obj.Placement.Base.z = z
        obj.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), radius), False)
        obj.addConstraint(Sketcher.Constraint('Radius', 0, radius))
        if Model.is_component(owner):
            label = obj.Label
            Model.register_object(owner, obj, 'Object')
            obj.Label = label
        return obj

    def path(self, owner, name, x=0):
        obj = self.doc.addObject('Sketcher::SketchObject', name)
        owner.addObject(obj)
        obj.Placement = App.Placement(App.Vector(x, 0, 0), App.Rotation(App.Vector(1, 0, 0), 90))
        obj.addGeometry(Part.LineSegment(App.Vector(), App.Vector(0, 10, 0)), False)
        obj.addConstraint(Sketcher.Constraint('Distance', 0, 10.0))
        return obj

    def build(self, retained=False, orientation='Standard', multisection=False):
        part = self.doc.addObject('App::Part', 'Part')
        part.Placement = App.Placement(App.Vector(20, 2, 1), App.Rotation(App.Vector(0, 1, 0), 35))
        body = self.doc.addObject('PartDesign::Body', 'Body'); part.addObject(body)
        profile = self.circle(body, 'Profile')
        path = self.path(body, 'Path')
        auxiliary = self.path(body, 'Auxiliary', 5) if orientation == 'Auxiliary' else None
        added = body.newObject('PartDesign::AdditivePipe', 'AdditivePipe')
        added.Profile = (profile, []); added.Spine = (path, ['Edge1'])
        added.Mode = orientation; added.Binormal = App.Vector(1, 0, 0)
        if auxiliary: added.AuxiliarySpine = (auxiliary, ['Edge1'])
        if multisection:
            end = self.circle(body, 'End', 4, 10)
            added.Sections = [(end, [''])]; added.Transformation = 'Multisection'
        cutprofile = self.circle(body, 'CutProfile', 1)
        cut = body.newObject('PartDesign::SubtractivePipe', 'SubtractivePipe')
        cut.Profile = (cutprofile, []); cut.Spine = (path, ['Edge1']); body.Tip = cut
        if retained: body.Placement.Base.x = 7
        for i, transform in enumerate((False, True)):
            link = self.doc.addObject('App::Link', 'Use' + str(i)); link.setLink(part)
            link.LinkTransform = transform; link.LinkPlacement.Base.x = 50 + i * 20
        self.doc.recompute()
        self.assertNotIn('Invalid', body.State)
        self.assertFalse(body.Shape.isNull())
        return part, body, profile, path, added, cutprofile, cut

    def mapped(self, part, body, added, cut):
        self.assertEqual(body.LegacyHistoryState, 'Mapped native pipe chain', str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(added.PipeMode, 'New Body'); self.assertEqual(cut.PipeMode, 'Subtract')
        self.assertEqual(cut.BaseFeature.Producer, added)
        self.assertEqual(cut.ConsumedResults, [cut.BaseFeature]); self.assertEqual(body.Producer, cut)
        self.assertEqual(Model.finished_results(part), [body]); Model.validate(self.doc)

    def test_identity_paths_shared_frames_and_conversion_undo(self):
        part, body, profile, path, added, cp, cut = self.build(multisection=True)
        originals = list(body.Group)
        ids = [(o.Name, o.TypeId, o.ID, o.Label) for o in originals + [body]]
        refs = added.Profile, list(added.Sections), added.Spine, added.AuxiliarySpine, cut.Spine
        shapes = {o.Name: Part.getShape(o).copy() for o in (part, body, self.doc.Use0, self.doc.Use1)}
        CadDocument.convert_legacy(self.doc); self.mapped(part, body, added, cut)
        self.assertEqual(ids, [(o.Name, o.TypeId, o.ID, o.Label) for o in originals + [body]])
        self.assertEqual(refs, (added.Profile, list(added.Sections), added.Spine, added.AuxiliarySpine, cut.Spine))
        self.assertLess(part.ModelHistory.index(path.Name), part.ModelHistory.index(added.Name))
        self.assertEqual(list(part.ModelHistory).count(path.Name), 1)
        for name, shape in shapes.items(): self.same(shape, Part.getShape(self.doc.getObject(name)))
        self.doc.undo(); self.doc.recompute(); self.assertEqual(body.Group, originals); self.assertEqual(body.Tip, cut)
        self.doc.redo(); self.doc.recompute(); self.mapped(part, body, added, cut)

    def test_all_orientations_and_native_options_preview(self):
        for orientation in Pipe.ORIENTATIONS:
            with self.subTest(orientation=orientation):
                part, body, profile, path, added, cp, cut = self.build(orientation=orientation)
                added.Refine = False; added.FuzzyTolerance = 1e-6
                added.SpineTangent = True; added.AuxiliarySpineTangent = True
                added.AuxiliaryCurvilinear = False; self.doc.recompute()
                before = body.Shape.copy(); CadDocument.convert_legacy(self.doc)
                self.mapped(part, body, added, cut); self.same(before, body.Shape)
                sections, mode, target, options = Pipe.read(added)
                self.assertEqual(options['orientation'], orientation)
                self.assertTrue(options['spine_tangent']); self.assertTrue(options['auxiliary_tangent'])
                self.assertFalse(options['curvilinear']); self.assertFalse(options['refine'])
                if orientation != 'Auxiliary': self.assertIsNone(options['auxiliary'])
                self.same(Pipe.preview(part, sections, mode, target, options), added.Shape)
                App.closeDocument(self.doc.Name); self.doc = App.newDocument('LegacyPipes'); self.doc.UndoMode = 1

    def test_modes_preserve_original_subtractive_type_and_common(self):
        part, body, profile, path, added, cp, cut = self.build()
        CadDocument.convert_legacy(self.doc); self.mapped(part, body, added, cut)
        identity = cut.Name, cut.TypeId, cut.ID, cut.ObjectId
        sections, mode, target, options = Pipe.read(cut)
        newpath = self.path(part, 'LongPath'); Model.register_object(part, newpath, 'Object')
        newpath.setDatum(0, App.Units.Quantity('12 mm')); self.doc.recompute()
        options['spine'] = (newpath, ['Edge1'])
        Pipe.edit(cut, sections, 'Add', target, options)
        self.assertEqual(identity, (cut.Name, cut.TypeId, cut.ID, cut.ObjectId))
        self.assertEqual(cut.Operation, 'Union')
        self.doc.undo(); self.doc.recompute(); self.assertEqual(cut.PipeMode, 'Subtract')
        self.doc.redo(); self.doc.recompute()
        Pipe.edit(cut, sections, 'New Body', options=options)
        self.assertIsNone(cut.BaseFeature); self.assertEqual(cut.ConsumedResults, [])
        options['boolean'] = 'Common'
        Pipe.edit(cut, sections, 'Subtract', target, options)
        self.assertEqual(cut.Operation, 'Common'); self.assertAlmostEqual(body.Shape.Volume, 10 * math.pi, places=6)
        self.assertEqual(identity, (cut.Name, cut.TypeId, cut.ID, cut.ObjectId))
        saved = self.output / 'PipeBooleanPresets.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        restored = self.doc.getObject(identity[0])
        self.assertEqual(restored.Operation, 'Common'); self.assertEqual(restored.TypeId, identity[1])
        Pipe.edit(restored, Pipe.read(restored)[0], 'Subtract', restored.BaseFeature,
                  dict(Pipe.read(restored)[3], boolean='Subtraction'))
        self.assertEqual(restored.Operation, 'Subtraction')

    def test_formula_cycle_and_failed_edit_preserve_parameters(self):
        part, body, profile, path, added, cp, cut = self.build()
        added.setExpression('Refine', '1 == 1'); self.doc.recompute()
        formulas = list(added.ExpressionEngine); CadDocument.convert_legacy(self.doc)
        self.mapped(part, body, added, cut); self.assertEqual(formulas, list(added.ExpressionEngine))
        with self.assertRaisesRegex(ValueError, 'expressions'): Pipe.edit(added, Pipe.read(added)[0], 'New Body')
        with self.assertRaises(ValueError): Pipe.edit(cut, Pipe.read(cut)[0], 'Subtract', body)
        before = body.Shape.copy(); refs = cut.Spine, cut.Profile, cut.BaseFeature
        bad = dict(Pipe.read(cut)[3], spine=(path, ['Edge999']))
        with self.assertRaises(ValueError): Pipe.edit(cut, Pipe.read(cut)[0], 'Subtract', cut.BaseFeature, bad)
        self.assertEqual(refs, (cut.Spine, cut.Profile, cut.BaseFeature)); self.same(before, body.Shape)
        distant = self.circle(part, 'Distant', 1); distant.Placement.Base.x = 20
        self.doc.recompute(); count = len(self.doc.Objects)
        with self.assertRaises(ValueError):
            Pipe.edit(cut, [(distant, None)], 'Subtract', cut.BaseFeature)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertEqual(refs, (cut.Spine, cut.Profile, cut.BaseFeature)); self.same(before, body.Shape)

    def test_original_bytes_cadprt_reopen_and_path_recompute(self):
        part, body, profile, path, added, cp, cut = self.build()
        original = self.output / 'Pipes.FCStd'; self.doc.saveAs(str(original))
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        CadDocument.convert_legacy(self.doc); self.mapped(part, body, added, cut)
        oid = added.ObjectId; saved = self.output / 'Pipes.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        self.assertEqual(self.doc.AdditivePipe.ObjectId, oid)
        self.mapped(self.doc.Part, self.doc.Body, self.doc.AdditivePipe, self.doc.SubtractivePipe)
        self.doc.Path.setDatum(0, App.Units.Quantity('12 mm')); self.doc.recompute()
        self.assertAlmostEqual(self.doc.Body.Shape.Volume, 180 * math.pi, places=6)
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)

    def test_native_retention_editor_missing_source_and_idempotence(self):
        part, body, profile, path, added, cp, cut = self.build(retained=True)
        before = body.Shape.copy(); refs = cut.Spine, cut.Profile, cut.BaseFeature
        CadDocument.convert_legacy(self.doc)
        alias = next(o for o in Model.history(part) if getattr(o, 'LegacyPipeSource', None) == cut)
        self.assertEqual(Model.owner(cut), body); self.same(before, body.Shape)
        self.open_row(part, alias); self.assertEqual(Gui.getDocument(self.doc.Name).getInEdit().Object, cut)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute(); self.assertEqual(refs, (cut.Spine, cut.Profile, cut.BaseFeature))
        count = len(self.doc.Objects); CadDocument.convert_legacy(self.doc); self.assertEqual(count, len(self.doc.Objects))
        alias.LegacyPipeSource = None
        self.assertEqual(Model.history_state(alias), 'Needs repair')

    def test_older_file_upgrade_preserves_input_and_access_identities(self):
        part, body, profile, path, added, cp, cut = self.build()
        with patch.object(LegacyConversion, 'migrate_pipes'): CadDocument.convert_legacy(self.doc)
        aliases = [o for o in Model.history(part) if getattr(o, 'LegacySketchSource', None)]
        ids = {o.Name: o.ObjectId for o in aliases + [profile, path, cp]}
        saved = self.output / 'PreviousPipes.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        for name, oid in ids.items(): self.assertEqual(self.doc.getObject(name).ObjectId, oid)
        self.mapped(self.doc.Part, self.doc.Body, self.doc.AdditivePipe, self.doc.SubtractivePipe)
        self.assertEqual(Model.metadata(self.doc).LegacyPipeVersion, 1)

    def test_actual_shared_history_preview_accept_cancel_and_undo(self):
        part, body, profile, path, added, cp, cut = self.build()
        CadDocument.convert_legacy(self.doc); self.mapped(part, body, added, cut)
        Task = importlib.import_module('freecad.gui.ComponentPipeTask')
        self.open_row(part, added); task = Task._task; self.assertIsNotNone(task)
        self.assertTrue(task.preview(), task.status.text())
        task.form.grab().save(str(self.output / 'legacy-pipe-task.png'))
        self.assertTrue(task.accept())
        self.doc.undo(); self.doc.recompute(); self.doc.redo(); self.doc.recompute()
        refs = added.Profile, added.Spine, added.AuxiliarySpine
        self.open_row(part, added); Task._task.reject()
        self.assertEqual(refs, (added.Profile, added.Spine, added.AuxiliarySpine))

    def test_standalone_sweep_solid_sheet_and_native_settings(self):
        part = self.doc.addObject('App::Part', 'Part')
        profile = self.circle(part, 'Profile', 2); path = self.path(part, 'Path')
        for solid in (True, False):
            sweep = self.doc.addObject('Part::Sweep', 'SolidSweep' if solid else 'SheetSweep'); part.addObject(sweep)
            sweep.Sections = [profile]; sweep.Spine = (path, ['Edge1'])
            sweep.Solid = solid; sweep.Frenet = False; sweep.Transition = 'Round corner'; sweep.Linearize = True
        self.doc.recompute(); before = self.doc.SolidSweep.Shape.copy()
        CadDocument.convert_legacy(self.doc); self.same(before, self.doc.SolidSweep.Shape)
        self.assertFalse(self.doc.SolidSweep.Frenet); self.assertTrue(self.doc.SolidSweep.Linearize)
        self.assertEqual(self.doc.SolidSweep.Sections, [profile]); self.assertEqual(self.doc.SolidSweep.Spine, (path, ['Edge1']))
        self.assertTrue(any(getattr(o, 'Producer', None) == self.doc.SolidSweep for o in Model.history(part)))
        self.assertFalse(self.doc.SheetSweep.Shape.Solids); self.assertTrue(self.doc.SheetSweep.LegacyPipeState)

    def test_native_transitions_multisection_and_reference_order(self):
        for transition in Pipe.TRANSITIONS:
            with self.subTest(transition=transition):
                part, body, profile, path, added, cp, cut = self.build(multisection=True)
                added.Transition = transition; self.doc.recompute()
                refs = list(added.Sections), added.Spine
                before = body.Shape.copy(); CadDocument.convert_legacy(self.doc)
                self.mapped(part, body, added, cut); self.same(before, body.Shape)
                self.assertEqual(refs, (list(added.Sections), added.Spine))
                inputs, mode, target, options = Pipe.read(added)
                self.assertEqual(options['transformation'], 'Multisection')
                self.assertEqual(options['transition'], transition)
                self.same(Pipe.preview(part, inputs, mode, target, options), added.Shape)
                App.closeDocument(self.doc.Name); self.doc = App.newDocument('LegacyPipes'); self.doc.UndoMode = 1

    def test_attached_and_whole_sketch_edge_semantics_retained(self):
        for attached in (True, False):
            with self.subTest(attached=attached):
                part, body, profile, path, added, cp, cut = self.build()
                if attached:
                    plane = body.newObject('PartDesign::Plane', 'DatumPlane')
                    profile.AttachmentSupport = [(plane, '')]; profile.MapMode = 'ObjectXY'; body.Tip = cut
                else:
                    added.Profile = (profile, ['Edge1'])
                self.doc.recompute(); before = body.Shape.copy(); ref = added.Profile
                CadDocument.convert_legacy(self.doc)
                self.assertEqual(Model.owner(added), body); self.assertEqual(added.Profile, ref)
                self.same(before, body.Shape)
                self.assertTrue(any(getattr(o, 'LegacyPipeSource', None) == added for o in Model.history(part)))
                App.closeDocument(self.doc.Name); self.doc = App.newDocument('LegacyPipes'); self.doc.UndoMode = 1

    def test_stale_and_native_common_are_retained(self):
        for stale in (True, False):
            with self.subTest(stale=stale):
                part, body, profile, path, added, cp, cut = self.build()
                if stale: path.touch()
                else: cut.Operation = 'Common'; self.doc.recompute()
                CadDocument.convert_legacy(self.doc)
                self.assertEqual(Model.owner(cut), body)
                self.assertTrue(any(getattr(o, 'LegacyPipeSource', None) == cut for o in Model.history(part)))
                if stale: self.assertTrue(any('unverified' in text for text in Model.metadata(self.doc).ConversionReport))
                else: self.assertEqual(cut.Operation, 'Common')
                App.closeDocument(self.doc.Name); self.doc = App.newDocument('LegacyPipes'); self.doc.UndoMode = 1

    def test_mixed_pad_pipe_targets_and_original_additive_mode_edit(self):
        part = self.doc.addObject('App::Part', 'Part')
        body = self.doc.addObject('PartDesign::Body', 'Body'); part.addObject(body)
        base = self.circle(body, 'Base', 4)
        pad = body.newObject('PartDesign::Pad', 'Pad'); pad.Profile = base; pad.Length = 5
        section = self.circle(body, 'Section', 4, 5); path = self.path(body, 'Path'); path.Placement.Base.z = 5
        pipe = body.newObject('PartDesign::AdditivePipe', 'AdditivePipe')
        pipe.Profile = section; pipe.Spine = (path, ['Edge1']); body.Tip = pipe
        self.doc.recompute(); before = body.Shape.copy(); self.assertNotIn('Invalid', body.State)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.LegacyHistoryState, 'Mapped native pipe chain', str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(pipe.BaseFeature.Producer, pad); self.assertEqual(pipe.PipeMode, 'Add')
        self.same(before, body.Shape)
        identity = pipe.Name, pipe.TypeId, pipe.ID, pipe.ObjectId
        larger = self.circle(part, 'Larger', 5, 5); self.doc.recompute()
        operation, target = Pipe.create(part, [(larger, None)], options=dict(Pipe.defaults(), spine=(path, ['Edge1'])))
        Model.reorder_history(part, [operation], 0)
        Pipe.edit(pipe, Pipe.read(pipe)[0], 'Subtract', target)
        self.assertEqual(identity, (pipe.Name, pipe.TypeId, pipe.ID, pipe.ObjectId))
        self.assertEqual(pipe.Operation, 'Subtraction'); self.assertAlmostEqual(body.Shape.Volume, 90 * math.pi, places=6)
