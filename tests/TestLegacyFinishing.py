# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native dress-up, transformation and Boolean conversion/History acceptance."""
import hashlib
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
import LegacyConversion
from TestLegacyExtrusions import TestLegacyExtrusions


class TestLegacyFinishing(unittest.TestCase):
    setUp = TestLegacyExtrusions.setUp
    tearDown = TestLegacyExtrusions.tearDown
    same = TestLegacyExtrusions.same
    open_row = TestLegacyExtrusions.open_row

    def containers(self):
        part = self.doc.addObject('App::Part', 'Part')
        part.Placement = App.Placement(App.Vector(20, 2, 1), App.Rotation(App.Vector(0, 1, 0), 35))
        body = self.doc.addObject('PartDesign::Body', 'Body'); part.addObject(body)
        box = body.newObject('PartDesign::AdditiveBox', 'Box')
        box.Length = box.Width = box.Height = 10
        for i, transform in enumerate((False, True)):
            link = self.doc.addObject('App::Link', 'Use' + str(i)); link.setLink(part)
            link.LinkTransform = transform; link.LinkPlacement.Base.x = 50 + 20 * i
        self.doc.recompute()
        return part, body, box

    def dress(self, kind='Fillet'):
        part, body, box = self.containers()
        feature = body.newObject('PartDesign::' + kind, kind)
        feature.Base = (box, ['Face1' if kind in ('Draft', 'Thickness') else 'Edge1'])
        if kind == 'Fillet': feature.Radius = 1
        elif kind == 'Chamfer': feature.Size = 1
        elif kind == 'Thickness': feature.Value = 1; feature.Reversed = True
        elif kind == 'Draft':
            feature.NeutralPlane = (self.doc.XY_Plane, [''])
            feature.PullDirection = (self.doc.Z_Axis, ['']); feature.Angle = 2
        body.Tip = feature; self.doc.recompute()
        self.assertNotIn('Invalid', feature.State); self.assertFalse(feature.Shape.isNull())
        return part, body, box, feature

    def pattern(self, kind='LinearPattern'):
        part, body, box = self.containers()
        feature = body.newObject('PartDesign::' + kind, kind); feature.Originals = [box]
        if kind == 'LinearPattern':
            feature.Direction = (self.doc.X_Axis, ['']); feature.Length = 5; feature.Occurrences = 2
        elif kind == 'PolarPattern':
            feature.Axis = (self.doc.Z_Axis, ['']); feature.Angle = 90; feature.Occurrences = 2
        elif kind == 'CircularPattern':
            feature.Axis = (self.doc.Z_Axis, [''])
            feature.RadialDistance = 2; feature.TangentialDistance = 5; feature.NumberCircles = 2
        elif kind == 'Mirrored': feature.MirrorPlane = (self.doc.YZ_Plane, [''])
        elif kind == 'Scaled': feature.Factor = 1.2; feature.Occurrences = 2
        body.Tip = feature; self.doc.recompute()
        self.assertNotIn('Invalid', feature.State); self.assertFalse(feature.Shape.isNull())
        return part, body, box, feature

    def boolean(self, mode='Fuse'):
        part, body, box = self.containers()
        toolbody = self.doc.addObject('PartDesign::Body', 'ToolBody'); part.addObject(toolbody)
        tool = toolbody.newObject('PartDesign::AdditiveBox', 'Tool')
        tool.Length = tool.Width = tool.Height = 10; tool.Placement.Base.x = 5
        feature = body.newObject('PartDesign::Boolean', 'Boolean'); feature.setObjects([toolbody])
        feature.Type = mode; body.Tip = feature; self.doc.recompute()
        self.assertNotIn('Invalid', feature.State); self.assertFalse(feature.Shape.isNull())
        return part, body, box, feature, toolbody, tool

    def alias(self, part, feature, family):
        obj = next(o for o in Model.history(part) if getattr(o, 'Legacy' + family + 'Source', None) == feature)
        self.assertEqual(obj.LinkedObject, feature); self.assertNotEqual(obj.ObjectId, feature.ObjectId)
        self.assertFalse(obj.Visibility); self.assertEqual(Model.retained_operation_source(obj), feature)
        self.assertLess(part.ModelHistory.index(obj.Name), part.ModelHistory.index(Model.owner(feature).Name))
        Model.validate(self.doc); return obj

    def new_case(self):
        App.closeDocument(self.doc.Name); self.doc = App.newDocument('Finishing'); self.doc.UndoMode = 1

    def test_four_dressup_native_references_identity_shared_frames_and_undo(self):
        for kind in ('Fillet', 'Chamfer', 'Draft', 'Thickness'):
            with self.subTest(kind=kind):
                part, body, box, feature = self.dress(kind)
                identities = [(o.Name, o.TypeId, o.ID, o.Label) for o in (body, box, feature)]
                group, tip, refs = list(body.Group), body.Tip, feature.Base
                shapes = {o.Name: Part.getShape(o).copy() for o in (part, body, self.doc.Use0, self.doc.Use1)}
                CadDocument.convert_legacy(self.doc); alias = self.alias(part, feature, 'DressUp')
                self.assertEqual(identities, [(o.Name, o.TypeId, o.ID, o.Label) for o in (body, box, feature)])
                self.assertEqual((list(body.Group), body.Tip, feature.Base), (group, tip, refs))
                for name, shape in shapes.items(): self.same(shape, Part.getShape(self.doc.getObject(name)))
                self.doc.undo(); self.doc.recompute(); self.assertEqual(body.Tip, tip)
                self.doc.redo(); self.doc.recompute(); self.alias(part, feature, 'DressUp')
                self.new_case()

    def test_pattern_transform_modes_originals_references_and_geometry(self):
        for kind in ('LinearPattern', 'PolarPattern', 'CircularPattern', 'Mirrored', 'Scaled'):
            with self.subTest(kind=kind):
                part, body, box, feature = self.pattern(kind)
                feature.TransformMode = 'Whole shape'; self.doc.recompute()
                before = body.Shape.copy(); originals = list(feature.Originals)
                identity = feature.Name, feature.TypeId, feature.ID, feature.Label
                CadDocument.convert_legacy(self.doc); self.alias(part, feature, 'Transform')
                self.assertEqual(identity, (feature.Name, feature.TypeId, feature.ID, feature.Label))
                self.assertEqual(feature.Originals, originals); self.assertEqual(feature.TransformMode, 'Whole shape')
                self.same(before, body.Shape); self.new_case()

    def test_boolean_fuse_cut_common_tools_frames_and_targets(self):
        for mode, volume in (('Fuse', 1500), ('Cut', 500), ('Common', 500)):
            with self.subTest(mode=mode):
                part, body, box, feature, toolbody, tool = self.boolean(mode)
                self.assertAlmostEqual(body.Shape.Volume, volume, places=7)
                before = body.Shape.copy(); tools = list(feature.Group); target = feature.BaseFeature
                compat = feature.UseLegacyBodyPlacement
                CadDocument.convert_legacy(self.doc); alias = self.alias(part, feature, 'Boolean')
                self.assertEqual(feature.Group, tools); self.assertEqual(feature.BaseFeature, target)
                self.assertEqual(alias.LegacyBooleanTarget, target); self.assertEqual(feature.Type, mode)
                self.assertEqual(feature.UseLegacyBodyPlacement, compat); self.same(before, body.Shape)
                self.assertEqual(toolbody.TypeId, 'PartDesign::Body'); self.new_case()

    def test_multitransform_order_and_mixed_family_history_order(self):
        part, body, box, fillet = self.dress()
        multi = body.newObject('PartDesign::MultiTransform', 'MultiTransform'); multi.Originals = [fillet]
        mirror = body.newObject('PartDesign::Mirrored', 'Mirror'); mirror.MirrorPlane = (self.doc.YZ_Plane, [''])
        linear = body.newObject('PartDesign::LinearPattern', 'Linear'); linear.Direction = (self.doc.X_Axis, [''])
        linear.Length = 5; linear.Occurrences = 2
        multi.Transformations = [mirror, linear]; body.Tip = multi; self.doc.recompute()
        self.assertNotIn('Invalid', multi.State); before = body.Shape.copy()
        members = list(body.Group); transforms = list(multi.Transformations)
        CadDocument.convert_legacy(self.doc); self.same(before, body.Shape)
        self.assertEqual(body.Group, members); self.assertEqual(multi.Transformations, transforms)
        aliases = [o for o in Model.history(part) if Model.retained_operation_source(o) in members
                   and o != Model.retained_operation_source(o)]
        indices = [members.index(Model.retained_operation_source(o)) for o in aliases]
        self.assertEqual(indices, sorted(indices)); self.alias(part, multi, 'Transform')

    def test_combined_pattern_keeps_inactive_settings_suppression_and_reopen(self):
        from PartDesignTests.TestPattern import TestPattern
        App.closeDocument(self.doc.Name); TestPattern.setUp(self)
        part = self.doc.addObject('App::Part', 'Part'); part.addObject(self.body)
        pattern, linear, circular = TestPattern.makePattern(self)
        pattern.PatternType = 'Circular'; circular.SuppressedIndices = [1]
        linear.setExpression('Length', 'Bump.Length * 5'); self.doc.recompute()
        before = self.body.Shape.copy(); settings = list(pattern.PatternSettings)
        CadDocument.convert_legacy(self.doc); alias = self.alias(part, pattern, 'Transform')
        self.assertEqual(pattern.PatternSettings, settings); self.assertEqual(circular.SuppressedIndices, [1])
        self.assertEqual(pattern.PatternType, 'Circular'); self.same(before, self.body.Shape)
        alias_name, oid = alias.Name, alias.ObjectId
        saved = self.output / 'CombinedPattern.cadprt'; self.doc.saveAs(str(saved)); App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(saved); self.assertEqual(self.doc.getObject(alias_name).ObjectId, oid)
        self.assertEqual(self.doc.Pattern.PatternType, 'Circular')
        self.assertEqual(self.doc.Pattern.PatternSettings[1].SuppressedIndices, [1])
        self.same(before, self.doc.Body.Shape)

    def test_actual_dressup_history_native_editor_close_preserves_inputs(self):
        part, body, box, feature = self.dress(); refs = feature.Base; value = feature.Radius.Value
        CadDocument.convert_legacy(self.doc); alias = self.alias(part, feature, 'DressUp')
        self.open_row(part, alias); self.assertEqual(Gui.getDocument(self.doc.Name).getInEdit().Object, feature)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute(); self.assertEqual(feature.Base, refs); self.assertEqual(feature.Radius.Value, value)

    def test_actual_pattern_history_native_editor_close_preserves_inputs(self):
        part, body, box, feature = self.pattern(); refs = feature.Direction; originals = list(feature.Originals)
        CadDocument.convert_legacy(self.doc); alias = self.alias(part, feature, 'Transform')
        self.open_row(part, alias); self.assertEqual(Gui.getDocument(self.doc.Name).getInEdit().Object, feature)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute(); self.assertEqual(feature.Direction, refs); self.assertEqual(feature.Originals, originals)

    def test_actual_native_radius_control_accept_cancel_and_undo(self):
        from PySide import QtWidgets
        part, body, box, feature = self.dress(); before = body.Shape.copy()
        CadDocument.convert_legacy(self.doc); alias = self.alias(part, feature, 'DressUp')
        self.open_row(part, alias)
        def radius():
            return next(w for panel in Gui.Control.activeTaskDialog().getDialogContent()
                        for w in panel.findChildren(QtWidgets.QAbstractSpinBox)
                        if w.objectName() == 'filletRadius')
        radius().setProperty('rawValue', 2.0); Gui.updateGui()
        Gui.Control.activeTaskDialog().accept(); Gui.updateGui(); self.doc.recompute()
        self.assertFalse(Gui.Control.activeDialog()); self.assertEqual(feature.Radius.Value, 2)
        changed = body.Shape.copy(); self.doc.undo(); self.doc.recompute(); self.same(before, body.Shape)
        self.doc.redo(); self.doc.recompute(); self.same(changed, body.Shape)
        self.open_row(part, alias); radius().setProperty('rawValue', 3.0); Gui.updateGui()
        Gui.Control.activeTaskDialog().reject(); Gui.updateGui(); self.doc.recompute()
        self.assertFalse(Gui.Control.activeDialog()); self.assertEqual(feature.Radius.Value, 2)
        self.same(changed, body.Shape)

    def test_actual_boolean_history_native_editor_close_preserves_inputs(self):
        part, body, box, feature, toolbody, tool = self.boolean(); tools = list(feature.Group)
        CadDocument.convert_legacy(self.doc); alias = self.alias(part, feature, 'Boolean')
        self.open_row(part, alias); self.assertEqual(Gui.getDocument(self.doc.Name).getInEdit().Object, feature)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute(); self.assertEqual(feature.Group, tools)

    def test_formula_edit_undo_original_bytes_and_cold_reopen(self):
        part, body, box, feature = self.dress(); feature.setExpression('Radius', '1 mm'); self.doc.recompute()
        original = self.output / 'Finishing.FCStd'; self.doc.saveAs(str(original)); digest = hashlib.sha256(original.read_bytes()).hexdigest()
        CadDocument.convert_legacy(self.doc); alias = self.alias(part, feature, 'DressUp'); oid = alias.ObjectId
        formulas = list(feature.ExpressionEngine)
        with Model.transaction(self.doc, 'Edit original radius formula'): feature.setExpression('Radius', '2 mm')
        changed = body.Shape.copy(); self.doc.undo(); self.doc.recompute(); self.assertEqual(list(feature.ExpressionEngine), formulas)
        self.doc.redo(); self.doc.recompute(); self.same(changed, body.Shape)
        alias_name = alias.Name
        saved = self.output / 'Finishing.cadprt'; self.doc.saveAs(str(saved)); App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(saved); self.assertEqual(self.doc.getObject(alias_name).ObjectId, oid)
        self.same(changed, self.doc.Body.Shape); self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)

    def test_prior_conversion_upgrade_three_versions_idempotent_missing_source(self):
        part, body, box, feature = self.dress()
        with patch.object(LegacyConversion, 'migrate_retained_features'): CadDocument.convert_legacy(self.doc)
        bid = body.ObjectId; saved = self.output / 'PreviousFinishing.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        part, body, feature = self.doc.Part, self.doc.Body, self.doc.Fillet
        self.assertEqual(body.ObjectId, bid); alias = self.alias(part, feature, 'DressUp')
        for family in LegacyConversion.RETAINED_FAMILIES: self.assertEqual(getattr(Model.metadata(self.doc), 'Legacy' + family + 'Version'), 1)
        count = len(self.doc.Objects); CadDocument.convert_legacy(self.doc); self.assertEqual(count, len(self.doc.Objects))
        alias.LegacyDressUpSource = None; self.assertEqual(Model.history_state(alias), 'Needs repair')

    def test_stale_native_output_reported_and_geometry_retained(self):
        part, body, box, feature = self.dress(); box.touch(); before = body.Shape.copy()
        CadDocument.convert_legacy(self.doc); self.alias(part, feature, 'DressUp'); self.same(before, body.Shape)
        self.assertTrue(any('unverified' in text for text in Model.metadata(self.doc).ConversionReport))

    def test_standalone_part_booleans_and_finishing_do_not_duplicate_outputs(self):
        part = self.doc.addObject('App::Part', 'Part')
        first = self.doc.addObject('Part::Box', 'First'); part.addObject(first)
        second = self.doc.addObject('Part::Box', 'Second'); part.addObject(second); second.Placement.Base.x = 5
        sources = []
        for kind in ('Cut', 'Fuse', 'Common'):
            feature = self.doc.addObject('Part::' + kind, kind); part.addObject(feature)
            feature.Base = first; feature.Tool = second; sources.append(feature)
        fillet = self.doc.addObject('Part::Fillet', 'Fillet'); part.addObject(fillet)
        fillet.Base = first; fillet.Edges = [(1, 1.0, 1.0)]; sources.append(fillet)
        chamfer = self.doc.addObject('Part::Chamfer', 'Chamfer'); part.addObject(chamfer)
        chamfer.Base = first; chamfer.Edges = [(1, 1.0, 1.0)]; sources.append(chamfer)
        self.doc.recompute(); before = Part.getShape(part).copy(); count = len(self.doc.Objects)
        CadDocument.convert_legacy(self.doc); self.same(before, Part.getShape(part))
        for source in sources:
            family = 'Boolean' if source.TypeId in ('Part::Cut', 'Part::Fuse', 'Part::Common') else 'DressUp'
            self.assertTrue(getattr(source, 'Legacy' + family + 'State'))
            self.assertFalse(any(getattr(o, 'Producer', None) == source for o in Model.history(part)))
