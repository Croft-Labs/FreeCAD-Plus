# SPDX-License-Identifier: LGPL-2.1-or-later
"""Legacy native revolution axes, result chains, editing and persistence."""
import hashlib
import importlib
import math
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import CadDocument
import ComponentModel as Model
import ComponentRevolve as Revolve
import LegacyConversion
from TestLegacyExtrusions import TestLegacyExtrusions


class TestLegacyRevolutions(unittest.TestCase):
    setUp = TestLegacyExtrusions.setUp
    same = TestLegacyExtrusions.same
    open_row = TestLegacyExtrusions.open_row

    def tearDown(self):
        Task = importlib.import_module('freecad.gui.ComponentRevolveTask')
        if Task._task: Task._task.reject()
        TestLegacyExtrusions.tearDown(self)

    def rectangle(self, owner, name, left=2, right=4):
        obj = self.doc.addObject('Sketcher::SketchObject', name); owner.addObject(obj)
        points = [App.Vector(left,0,0),App.Vector(right,0,0),App.Vector(right,3,0),App.Vector(left,3,0)]
        for a,b in zip(points,points[1:]+points[:1]): obj.addGeometry(Part.LineSegment(a,b),False)
        return obj

    def build(self, retained=False, construction=False):
        part = self.doc.addObject('App::Part','Part')
        part.Placement = App.Placement(App.Vector(20,2,1),App.Rotation(App.Vector(0,1,0),35))
        body = self.doc.addObject('PartDesign::Body','Body'); part.addObject(body)
        first = self.rectangle(body,'Sketch')
        rev = body.newObject('PartDesign::Revolution','Revolution'); rev.Profile = first
        rev.ReferenceAxis = (first,['V_Axis']); rev.Angle = 360
        cut = self.rectangle(body,'CutSketch',2,3)
        groove = body.newObject('PartDesign::Groove','Groove'); groove.Profile = cut
        groove.ReferenceAxis = (cut,['V_Axis']); groove.Angle = 90
        body.Tip = groove
        if construction:
            cut.addGeometry(Part.LineSegment(App.Vector(0,-1,0),App.Vector(0,4,0)),True)
            groove.ReferenceAxis = (cut,['Axis0'])
        if retained:
            plane = body.newObject('PartDesign::Plane','DatumPlane')
            cut.AttachmentSupport = [(plane,'')]; cut.MapMode = 'ObjectXY'
            body.Placement = App.Placement(App.Vector(7,3,2),App.Rotation(App.Vector(1,0,0),25))
            body.Tip = groove
        for i,transform in enumerate((False,True)):
            link = self.doc.addObject('App::Link','Use'+str(i)); link.setLink(part)
            link.LinkTransform = transform; link.LinkPlacement.Base.x = 50+i*20
        self.doc.recompute()
        self.assertNotIn('Invalid',body.State)
        self.assertAlmostEqual(rev.Shape.Volume,36*math.pi,places=7)
        return part,body,first,rev,cut,groove

    def mapped(self,part,body,rev,groove):
        self.assertEqual(body.LegacyHistoryState,'Mapped native revolve chain',str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(Model.owner(rev),part); self.assertEqual(Model.owner(groove),part)
        self.assertEqual(rev.RevolveMode,'New Body'); self.assertEqual(groove.RevolveMode,'Subtract')
        self.assertEqual(groove.BaseFeature.Producer,rev)
        self.assertEqual(groove.ConsumedResults,[groove.BaseFeature])
        self.assertEqual(body.Producer,groove); self.assertEqual(body.Tip.Producer,groove)
        self.assertEqual(Model.finished_results(part),[body]); Model.validate(self.doc)

    def test_native_identities_geometry_sharing_and_conversion_undo(self):
        part,body,first,rev,cut,groove = self.build()
        identities = [(o.Name,o.TypeId,o.ID,o.Label) for o in (body,first,rev,cut,groove)]
        group = list(body.Group)
        shapes = {o.Name:Part.getShape(o).copy() for o in (part,body,self.doc.Use0,self.doc.Use1)}
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,rev,groove)
        self.assertEqual(identities,[(o.Name,o.TypeId,o.ID,o.Label) for o in (body,first,rev,cut,groove)])
        for name,shape in shapes.items(): self.same(shape,Part.getShape(self.doc.getObject(name)))
        Navigator=importlib.import_module('freecad.gui.ComponentNavigator')
        panel=Navigator.show(self.doc); panel.open_component_tab(Navigator.object_key(part))
        self.doc.undo(); self.doc.recompute(); self.assertEqual(body.Group,group); self.assertEqual(body.Tip,groove)
        panel.refresh(); self.assertIsNone(panel.active_key)
        self.doc.redo(); self.doc.recompute(); self.mapped(part,body,rev,groove)

    def test_angles_sides_signed_offsets_reverse_and_rotated_sketch(self):
        part,body,first,rev,cut,groove = self.build()
        # Rotate both inputs together around the common native vertical axis.
        for obj in (first,cut): obj.Placement.Rotation = App.Rotation(App.Vector(0,1,0),30)
        groove.SideType = 'Two sides'; groove.Angle2 = 45; groove.Reversed = True
        groove.StartType = 'Offset'; groove.StartOffset = -35; groove.ProjectAxis = True
        self.doc.recompute(); before = body.Shape.copy(); values = Revolve.read(groove)
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,rev,groove)
        self.assertEqual(Revolve.read(groove),values); self.same(before,body.Shape)
        for sides in ('One side','Two sides','Symmetric'):
            for offset in (-360,-45,0,45,360):
                options = Revolve.read(groove); options.update(sides=sides,start='Offset',start_offset=offset)
                Revolve.edit(groove,cut,90,'Subtract',groove.BaseFeature,True,options=options)
                preview = Revolve.preview(part,cut,90,'Subtract',groove.BaseFeature,True,options=options)
                self.same(preview,body.Shape)
                self.assertEqual(groove.StartOffset.Value,offset)

    def test_construction_axis_native_preview_and_shared_edit(self):
        part,body,first,rev,cut,groove = self.build(construction=True)
        before = body.Shape.copy(); CadDocument.convert_legacy(self.doc)
        self.mapped(part,body,rev,groove); self.same(before,body.Shape)
        axis = groove.ReferenceAxis
        options = Revolve.read(groove)
        self.same(Revolve.preview(part,cut,120,'Subtract',groove.BaseFeature,options=options),
                  Revolve.edit(groove,cut,120,'Subtract',groove.BaseFeature,options=options).Shape)
        self.assertEqual(groove.ReferenceAxis,axis)

    def test_formula_preservation_edit_refusal_and_recompute(self):
        part,body,first,rev,cut,groove = self.build()
        cut.addConstraint(Sketcher.Constraint('Distance',0,1.))
        groove.setExpression('Angle','CutSketch.Constraints[0] * 90')
        self.doc.recompute(); expressions = list(groove.ExpressionEngine); before = body.Shape.copy()
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,rev,groove)
        self.assertEqual(list(groove.ExpressionEngine),expressions); self.same(before,body.Shape)
        with self.assertRaisesRegex(ValueError,'expressions'):
            Revolve.edit(groove,cut,120,'Subtract',groove.BaseFeature)
        with Model.transaction(self.doc,'Edit retained angular formula'): groove.setExpression('Angle','120')
        self.assertAlmostEqual(groove.Angle.Value,120)
        self.assertNotIn('Invalid',body.State)

    def test_target_edits_type_guard_downstream_guard_and_new_body(self):
        part,body,first,rev,cut,groove = self.build(); CadDocument.convert_legacy(self.doc)
        target = groove.BaseFeature; identity = groove.Name,groove.TypeId,groove.ID,groove.ObjectId
        with self.assertRaisesRegex(ValueError,'identity'): Revolve.edit(groove,cut,90,'Add',target)
        with self.assertRaises(ValueError): Revolve.edit(groove,cut,90,'Subtract',body)
        added,result = Revolve.create(part,first,360)
        Model.reorder_history(part,[added],0)
        Revolve.edit(groove,cut,120,'Subtract',result)
        self.assertEqual(groove.ConsumedResults,[result]); self.assertEqual(groove.BaseFeature,result)
        self.assertEqual(identity,(groove.Name,groove.TypeId,groove.ID,groove.ObjectId))
        self.doc.undo(); self.doc.recompute(); self.assertEqual(groove.BaseFeature,target)
        # Same native additive type can change New Body/Add without replacement.
        Revolve.edit(added,first,360,'Add',target)
        self.assertEqual(added.ConsumedResults,[target])
        Revolve.edit(added,first,360,'New Body')
        self.assertIsNone(added.BaseFeature); self.assertEqual(added.ConsumedResults,[])

    def test_native_through_all_and_horizontal_axis(self):
        part,body,first,rev,cut,groove = self.build()
        for sketch in (first,cut):
            geometry=list(sketch.Geometry)
            for i in reversed(range(sketch.GeometryCount)): sketch.delGeometry(i)
            for geom in geometry:
                sketch.addGeometry(Part.LineSegment(App.Vector(geom.StartPoint.y,geom.StartPoint.x,0),App.Vector(geom.EndPoint.y,geom.EndPoint.x,0)),False)
        rev.ReferenceAxis=(first,['H_Axis']); groove.ReferenceAxis=(cut,['H_Axis']); groove.Type='ThroughAll'
        self.doc.recompute(); before=body.Shape.copy()
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,rev,groove)
        self.assertEqual(groove.Type,'ThroughAll'); self.same(before,body.Shape)

    def test_original_bytes_cold_cadprt_reopen_and_further_edits(self):
        part,body,first,rev,cut,groove = self.build()
        original=self.output/'Revolutions.FCStd'; self.doc.saveAs(str(original))
        digest=hashlib.sha256(original.read_bytes()).hexdigest()
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,rev,groove)
        ids={o.Name:o.ObjectId for o in (part,body,first,rev,cut,groove,groove.BaseFeature)}
        Revolve.edit(groove,cut,120,'Subtract',groove.BaseFeature)
        self.doc.undo(); self.doc.recompute(); self.assertEqual(groove.Angle.Value,90)
        self.doc.redo(); self.doc.recompute(); shape=body.Shape.copy()
        saved=self.output/'Revolutions.cadprt'; self.doc.saveAs(str(saved))
        self.assertEqual(digest,hashlib.sha256(original.read_bytes()).hexdigest())
        App.closeDocument(self.doc.Name); self.doc=CadDocument.open(saved)
        for name,identity in ids.items(): self.assertEqual(self.doc.getObject(name).ObjectId,identity)
        self.same(shape,self.doc.Body.Shape)
        Revolve.edit(self.doc.Groove,self.doc.CutSketch,150,'Subtract',self.doc.Groove.BaseFeature)
        self.assertNotIn('Invalid',self.doc.Body.State)

    def test_retained_attachments_frames_target_and_missing_source(self):
        part,body,first,rev,cut,groove=self.build(retained=True)
        group,tip,support=list(body.Group),body.Tip,list(cut.AttachmentSupport)
        before=Part.getShape(self.doc.Use0).copy(); CadDocument.convert_legacy(self.doc)
        alias=next(o for o in Model.history(part) if getattr(o,'LegacyRevolveSource',None)==groove)
        self.assertEqual((body.Group,body.Tip),(group,tip)); self.assertEqual(list(cut.AttachmentSupport),support)
        self.assertEqual(alias.LegacyRevolveTarget,rev)
        self.assertTrue(alias.LinkPlacement.isSame(body.Placement.multiply(groove.Placement),1e-8))
        self.same(before,Part.getShape(self.doc.Use0))
        with Model.transaction(self.doc,'Edit retained angular input'): groove.Angle=120
        self.assertNotIn('Invalid',body.State)
        with Model.transaction(self.doc,'Delete retained native source'): self.doc.removeObject(groove.Name)
        self.assertEqual(Model.history_state(alias),'Needs repair'); self.assertIn('missing',Model.history_detail(alias))

    def test_origin_axis_and_reference_start_remain_native(self):
        part,body,first,rev,cut,groove=self.build()
        axis=next(o for o in body.Origin.OriginFeatures if o.Role=='Y_Axis')
        groove.ReferenceAxis=(axis,[''])
        reference=body.newObject('PartDesign::Plane','StartPlane')
        reference.Placement=App.Placement(App.Vector(),App.Rotation(App.Vector(0,1,0),-30))
        groove.StartType='Reference'; groove.StartReference=(reference,['']); groove.StartOffset=15
        body.Tip=groove; self.doc.recompute()
        self.assertNotIn('Invalid',groove.State)
        before=body.Shape.copy(); parameters=Revolve.read(groove); group=list(body.Group)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(Revolve.read(groove),parameters); self.assertEqual(body.Group,group)
        self.same(before,body.Shape)
        self.assertTrue(any(getattr(o,'LegacyRevolveSource',None)==groove for o in Model.history(part)))

    def test_unverified_source_retains_native_output_without_promotion(self):
        part,body,first,rev,cut,groove=self.build()
        groove.Angle=120  # The saved cache is now stale; conversion must not admit it.
        group=list(body.Group)
        CadDocument.convert_legacy(self.doc)
        self.assertFalse(getattr(body,'Producer',None)); self.assertEqual(body.Group,group)
        self.assertTrue(any('unverified' in line for line in Model.metadata(self.doc).ConversionReport))

    def test_upgrade_previous_file_preserves_input_and_access_link_identities(self):
        part,body,first,rev,cut,groove=self.build()
        with patch.object(LegacyConversion,'migrate_revolutions'): CadDocument.convert_legacy(self.doc)
        aliases=[o for o in Model.history(part) if getattr(o,'LegacySketchSource',None)]
        ids={o.Name:o.ObjectId for o in aliases+[first,cut]}
        saved=self.output/'PreviousRevolutions.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc=CadDocument.open(saved)
        for name,identity in ids.items(): self.assertEqual(self.doc.getObject(name).ObjectId,identity)
        self.assertEqual(Model.metadata(self.doc).LegacyRevolveVersion,1)
        self.mapped(self.doc.Part,self.doc.Body,self.doc.Revolution,self.doc.Groove)
        count=len(self.doc.Objects); CadDocument.convert_legacy(self.doc); self.assertEqual(count,len(self.doc.Objects))

    def test_actual_shared_history_task_accept_cancel_and_undo(self):
        part,body,first,rev,cut,groove=self.build(); CadDocument.convert_legacy(self.doc)
        Task=importlib.import_module('freecad.gui.ComponentRevolveTask')
        self.open_row(part,groove)
        loaded = Path(Task.__file__).resolve()
        expected = Path(os.environ['FREECAD_PLUS_SOURCE']).resolve() / 'src/Gui/ComponentRevolveTask.py'
        self.assertEqual(hashlib.sha256(loaded.read_bytes()).digest(),
                         hashlib.sha256(expected.read_bytes()).digest())
        if os.environ.get('FREECAD_PLUS_PROFILE_SOURCE') != '1':
            self.assertTrue(loaded.is_relative_to(Path(App.ConfigGet('AppHomePath')).resolve()))
        self.assertIsNotNone(Task._task)
        task=Task._task; task.auto_preview.setChecked(False)
        self.assertEqual(task.target.currentData(),groove.BaseFeature.Name)
        task.angle.setProperty('rawValue',120.)
        self.assertTrue(task.preview(),task.status.text()); self.assertTrue(task.accept())
        self.assertEqual(groove.Angle.Value,120)
        self.doc.undo(); self.doc.recompute(); self.assertEqual(groove.Angle.Value,90)
        self.doc.redo(); self.doc.recompute()
        self.open_row(part,groove); self.assertIsNotNone(Task._task)
        Task._task.angle.setProperty('rawValue',150.); Task._task.reject()
        self.assertEqual(groove.Angle.Value,120)

    def test_actual_retained_native_groove_editor(self):
        part,body,first,rev,cut,groove=self.build(retained=True); CadDocument.convert_legacy(self.doc)
        alias=next(o for o in Model.history(part) if getattr(o,'LegacyRevolveSource',None)==groove)
        target,axis,angle=groove.BaseFeature,groove.ReferenceAxis,groove.Angle.Value
        self.open_row(part,alias)
        edit=Gui.getDocument(self.doc.Name).getInEdit(); self.assertIsNotNone(edit); self.assertEqual(edit.Object,groove)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute(); self.assertEqual((groove.BaseFeature,groove.ReferenceAxis,groove.Angle.Value),(target,axis,angle))

    def test_standalone_signed_axis_solid_and_sheet_retention(self):
        part=self.doc.addObject('App::Part','Part'); sketch=self.rectangle(part,'Sketch')
        solid=self.doc.addObject('Part::Revolution','NativeRevolve'); part.addObject(solid)
        solid.Source=sketch; solid.Axis=App.Vector(0,1,0); solid.Angle=-180; solid.Symmetric=True; solid.Solid=True
        sheet=self.doc.addObject('Part::Revolution','NativeSheet'); part.addObject(sheet)
        sheet.Source=sketch; sheet.Axis=App.Vector(0,1,0); sheet.Angle=90; sheet.Solid=False
        self.doc.recompute(); before=solid.Shape.copy(); identity=solid.Name,solid.TypeId,solid.ID
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(identity,(solid.Name,solid.TypeId,solid.ID)); self.same(before,solid.Shape)
        self.assertEqual(solid.Angle,-180); self.assertTrue(solid.Symmetric)
        result=next(o for o in Model.history(part) if getattr(o,'Producer',None)==solid)
        self.assertIn(result.Name,part.ResultObjects); self.assertNotIn(solid.Name,part.ResultObjects)
        self.assertEqual(sheet.LegacyRevolveState,'Retained native standalone revolution')
        self.assertEqual(len(sheet.Shape.Solids),0)
        with Model.transaction(self.doc,'Edit native signed angle'): solid.Angle=-120
        self.same(solid.Shape,result.Shape)

    def test_mixed_pad_revolution_chain_reuses_target_publishing(self):
        part=self.doc.addObject('App::Part','Part')
        body=self.doc.addObject('PartDesign::Body','Body'); part.addObject(body)
        base=body.newObject('Sketcher::SketchObject','BaseSketch')
        base.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),4),False)
        pad=body.newObject('PartDesign::Pad','Pad'); pad.Profile=base; pad.Length=10
        profile=self.rectangle(body,'RingSketch',2,4)
        profile.Placement=App.Placement(App.Vector(0,0,10),App.Rotation(App.Vector(1,0,0),90))
        rev=body.newObject('PartDesign::Revolution','Revolution'); rev.Profile=profile
        rev.ReferenceAxis=(profile,['V_Axis']); rev.Angle=360; body.Tip=rev
        self.doc.recompute(); self.assertNotIn('Invalid',body.State); before=body.Shape.copy()
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.LegacyHistoryState,'Mapped native revolve chain',str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(rev.BaseFeature.Producer,pad); self.assertEqual(rev.RevolveMode,'Add')
        self.assertEqual(pad.ExtrudeMode,'New Body'); self.same(before,body.Shape)
        self.assertFalse(any(getattr(o,'LegacyExtrudeSource',None)==pad for o in Model.history(part)))
        Model.validate(self.doc)
