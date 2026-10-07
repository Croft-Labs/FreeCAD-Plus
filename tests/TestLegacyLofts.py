# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native legacy Loft sections, identity, Boolean targets and GUI/persistence."""
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
import ComponentLoft as Loft
import LegacyConversion
from TestLegacyExtrusions import TestLegacyExtrusions


class TestLegacyLofts(unittest.TestCase):
    setUp = TestLegacyExtrusions.setUp
    same = TestLegacyExtrusions.same
    open_row = TestLegacyExtrusions.open_row

    def tearDown(self):
        Task=importlib.import_module('freecad.gui.ComponentLoftTask')
        if Task._task: Task._task.reject()
        TestLegacyExtrusions.tearDown(self)

    def circle(self,owner,name,z,radius):
        obj=self.doc.addObject('Sketcher::SketchObject',name); owner.addObject(obj)
        obj.Placement.Base.z=z
        obj.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),radius),False)
        obj.addConstraint(Sketcher.Constraint('Radius',0,radius))
        if Model.is_component(owner):
            label=obj.Label
            Model.register_object(owner,obj,'Object'); obj.Label=label
        return obj

    def build(self,retained=False,third=False):
        part=self.doc.addObject('App::Part','Part')
        part.Placement=App.Placement(App.Vector(20,2,1),App.Rotation(App.Vector(0,1,0),35))
        body=self.doc.addObject('PartDesign::Body','Body'); part.addObject(body)
        first=self.circle(body,'Bottom',0,4); last=self.circle(body,'Top',10,4)
        extra=[self.circle(body,'Middle',5,4.5)] if third else []
        added=body.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
        added.Profile=(first,[]); added.Sections=[(o,['']) for o in extra+[last]]
        bottom=self.circle(body,'CutBottom',2,1); top=self.circle(body,'CutTop',10,1)
        cut=body.newObject('PartDesign::SubtractiveLoft','SubtractiveLoft')
        cut.Profile=(bottom,[]); cut.Sections=[(top,[''])]; body.Tip=cut
        if retained:
            plane=body.newObject('PartDesign::Plane','DatumPlane'); plane.Placement.Base.z=2
            bottom.AttachmentSupport=[(plane,'')]; bottom.MapMode='ObjectXY'
            body.Placement=App.Placement(App.Vector(7,3,2),App.Rotation(App.Vector(1,0,0),25))
            body.Tip=cut
        for i,transform in enumerate((False,True)):
            link=self.doc.addObject('App::Link','Use'+str(i)); link.setLink(part)
            link.LinkTransform=transform; link.LinkPlacement.Base.x=50+i*20
        self.doc.recompute(); self.assertNotIn('Invalid',body.State)
        if not third: self.assertAlmostEqual(body.Shape.Volume,152*math.pi,places=7)
        return part,body,first,last,added,bottom,top,cut

    def mapped(self,part,body,added,cut):
        self.assertEqual(body.LegacyHistoryState,'Mapped native loft chain',str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(Model.owner(added),part); self.assertEqual(Model.owner(cut),part)
        self.assertEqual(added.LoftMode,'New Body'); self.assertEqual(cut.LoftMode,'Subtract')
        self.assertEqual(cut.BaseFeature.Producer,added); self.assertEqual(cut.ConsumedResults,[cut.BaseFeature])
        self.assertEqual(body.Producer,cut); self.assertEqual(body.Tip.Producer,cut)
        self.assertEqual(Model.finished_results(part),[body]); Model.validate(self.doc)

    def test_original_identities_section_order_shared_geometry_and_conversion_undo(self):
        part,body,first,last,added,bottom,top,cut=self.build(third=True)
        originals=list(body.Group); identities=[(o.Name,o.TypeId,o.ID,o.Label) for o in originals+[body]]
        refs={o:(o.Profile,list(o.Sections)) for o in (added,cut)}
        shapes={o.Name:Part.getShape(o).copy() for o in (part,body,self.doc.Use0,self.doc.Use1)}
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,added,cut)
        self.assertEqual(identities,[(o.Name,o.TypeId,o.ID,o.Label) for o in originals+[body]])
        for o,links in refs.items(): self.assertEqual((o.Profile,list(o.Sections)),links)
        self.assertLess(part.ModelHistory.index(self.doc.Middle.Name),part.ModelHistory.index(added.Name))
        for name,shape in shapes.items(): self.same(shape,Part.getShape(self.doc.getObject(name)))
        self.doc.undo(); self.doc.recompute(); self.assertEqual(body.Group,originals); self.assertEqual(body.Tip,cut)
        self.doc.redo(); self.doc.recompute(); self.mapped(part,body,added,cut)

    def test_shared_modes_targets_original_type_and_new_body(self):
        part,body,first,last,added,bottom,top,cut=self.build(); CadDocument.convert_legacy(self.doc)
        self.mapped(part,body,added,cut); target=cut.BaseFeature; sections=Loft.read(cut)[0]
        identity=cut.Name,cut.TypeId,cut.ID,cut.ObjectId
        with Model.transaction(self.doc,'Extend original tool for a meaningful additive edit'): top.Placement.Base.z=12
        Loft.edit(cut,sections,'Add',target)
        self.assertEqual(identity,(cut.Name,cut.TypeId,cut.ID,cut.ObjectId))
        self.assertEqual(cut.Operation,'Union'); self.assertEqual(cut.LoftMode,'Add')
        self.assertAlmostEqual(body.Shape.Volume,162*math.pi,places=7)
        self.doc.undo(); self.doc.recompute(); self.assertEqual(cut.LoftMode,'Subtract')
        self.doc.redo(); self.doc.recompute()
        Loft.edit(cut,sections,'New Body')
        self.assertIsNone(cut.BaseFeature); self.assertEqual(cut.ConsumedResults,[])
        self.assertAlmostEqual(body.Shape.Volume,10*math.pi,places=7)
        Loft.edit(cut,sections,'Subtract',target)
        self.assertEqual(identity,(cut.Name,cut.TypeId,cut.ID,cut.ObjectId))
        self.assertAlmostEqual(body.Shape.Volume,152*math.pi,places=7)

    def test_reorder_upstream_edit_preview_options_and_retarget(self):
        part,body,first,last,added,bottom,top,cut=self.build(third=True)
        added.Ruled=True; added.Refine=False; added.FuzzyTolerance=1e-6
        self.doc.recompute(); before=body.Shape.copy()
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,added,cut); self.same(before,body.Shape)
        sections,mode,target,options=Loft.read(added)
        self.assertEqual(options,dict(ruled=True,closed=False,refine=False,fuzzy=1e-6))
        Loft.edit(added,list(reversed(sections)),mode,target,options)
        self.assertEqual(Loft.read(added)[0],list(reversed(sections)))
        self.same(Loft.preview(part,list(reversed(sections)),options=options),added.Shape)
        with Model.transaction(self.doc,'Edit original top radius'): last.setDatum(0,App.Units.Quantity('5 mm'))
        self.assertGreater(body.Shape.Volume,before.Volume)
        original=cut.BaseFeature
        operation,result=Loft.create(part,[(first,None),(last,None)])
        Model.reorder_history(part,[operation],0)
        Loft.edit(cut,Loft.read(cut)[0],'Subtract',result)
        self.assertEqual(cut.ConsumedResults,[result]); self.assertEqual(cut.BaseFeature,result)
        self.doc.undo(); self.doc.recompute(); self.assertEqual(cut.BaseFeature,original)

    def test_formula_preservation_cycle_guard_and_failed_edit_rollback(self):
        part,body,first,last,added,bottom,top,cut=self.build()
        added.setExpression('Refine','1 == 1'); self.doc.recompute()
        expressions=list(added.ExpressionEngine); CadDocument.convert_legacy(self.doc)
        self.mapped(part,body,added,cut); self.assertEqual(list(added.ExpressionEngine),expressions)
        with self.assertRaisesRegex(ValueError,'expressions'): Loft.edit(added,Loft.read(added)[0],'New Body')
        with self.assertRaises(ValueError): Loft.edit(cut,Loft.read(cut)[0],'Subtract',body)
        before=body.Shape.copy(); count=len(self.doc.Objects); sections=Loft.read(cut)[0]
        distant=[(self.circle(part,'Distant'+str(i),z,1),None) for i,z in enumerate((20,30))]
        self.doc.recompute(); count=len(self.doc.Objects)
        with self.assertRaises(ValueError): Loft.edit(cut,distant,'Subtract',cut.BaseFeature)
        self.assertEqual(len(self.doc.Objects),count); self.same(before,body.Shape)
        self.assertEqual(Loft.read(cut)[0],sections)

    def test_original_bytes_cold_cadprt_reopen_and_further_edits(self):
        part,body,first,last,added,bottom,top,cut=self.build()
        original=self.output/'Lofts.FCStd'; self.doc.saveAs(str(original))
        digest=hashlib.sha256(original.read_bytes()).hexdigest(); CadDocument.convert_legacy(self.doc)
        self.mapped(part,body,added,cut)
        ids={o.Name:o.ObjectId for o in (part,body,first,last,added,bottom,top,cut,cut.BaseFeature)}
        with Model.transaction(self.doc,'Edit original cut height'): bottom.Placement.Base.z=3
        self.assertAlmostEqual(body.Shape.Volume,153*math.pi,places=7)
        self.doc.undo(); self.doc.recompute(); self.assertAlmostEqual(body.Shape.Volume,152*math.pi,places=7)
        self.doc.redo(); self.doc.recompute(); shape=body.Shape.copy()
        saved=self.output/'Lofts.cadprt'; self.doc.saveAs(str(saved))
        self.assertEqual(digest,hashlib.sha256(original.read_bytes()).hexdigest())
        App.closeDocument(self.doc.Name); self.doc=CadDocument.open(saved)
        for name,identity in ids.items(): self.assertEqual(self.doc.getObject(name).ObjectId,identity)
        self.same(shape,self.doc.Body.Shape)
        with Model.transaction(self.doc,'Extend original saved tool'): self.doc.CutTop.Placement.Base.z=12
        Loft.edit(self.doc.SubtractiveLoft,Loft.read(self.doc.SubtractiveLoft)[0],'Add',self.doc.SubtractiveLoft.BaseFeature)
        self.assertAlmostEqual(self.doc.Body.Shape.Volume,162*math.pi,places=7)
        # Native custom enumerations must restore the new Boolean mode too.
        self.doc.saveAs(str(saved)); App.closeDocument(self.doc.Name); self.doc=CadDocument.open(saved)
        self.assertEqual(self.doc.SubtractiveLoft.Operation,'Union')
        self.assertEqual(self.doc.SubtractiveLoft.ObjectId,ids['SubtractiveLoft'])
        self.assertAlmostEqual(self.doc.Body.Shape.Volume,162*math.pi,places=7)

    def test_retained_attachment_frames_targets_sections_and_missing_source(self):
        part,body,first,last,added,bottom,top,cut=self.build(retained=True)
        group=list(body.Group); tip=body.Tip; links=cut.Profile,list(cut.Sections)
        support=list(bottom.AttachmentSupport); before=Part.getShape(self.doc.Use0).copy()
        CadDocument.convert_legacy(self.doc)
        alias=next(o for o in Model.history(part) if getattr(o,'LegacyLoftSource',None)==cut)
        self.assertEqual((body.Group,body.Tip),(group,tip)); self.assertEqual((cut.Profile,list(cut.Sections)),links)
        self.assertEqual(list(bottom.AttachmentSupport),support); self.assertEqual(alias.LegacyLoftTarget,added)
        self.assertTrue(alias.LinkPlacement.isSame(body.Placement.multiply(cut.Placement),1e-8))
        self.same(before,Part.getShape(self.doc.Use0))
        with Model.transaction(self.doc,'Edit original retained sections'): top.Placement.Base.z=9
        self.assertNotIn('Invalid',body.State)
        with Model.transaction(self.doc,'Delete retained native loft'): self.doc.removeObject(cut.Name)
        self.assertEqual(Model.history_state(alias),'Needs repair'); self.assertIn('missing',Model.history_detail(alias))

    def test_legacy_sketch_edge_means_whole_profile_stays_native(self):
        part,body,first,last,added,bottom,top,cut=self.build()
        added.Profile=(first,['Edge1'])
        self.doc.recompute(); self.assertNotIn('Invalid',body.State); before=body.Shape.copy()
        links=added.Profile,list(added.Sections)
        CadDocument.convert_legacy(self.doc)
        self.assertFalse(getattr(body,'Producer',None)); self.assertEqual((added.Profile,list(added.Sections)),links)
        self.same(before,body.Shape)
        self.assertTrue(any(getattr(o,'LegacyLoftSource',None)==cut for o in Model.history(part)))

    def test_native_common_boolean_stays_editable_and_retained(self):
        part,body,first,last,added,bottom,top,cut=self.build()
        cut.Operation='Common'; self.doc.recompute(); before=body.Shape.copy()
        self.assertNotIn('Invalid',body.State); group=list(body.Group)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(cut.Operation,'Common'); self.assertEqual(body.Group,group)
        self.assertFalse(getattr(body,'Producer',None)); self.same(before,body.Shape)
        self.assertTrue(any(getattr(o,'LegacyLoftSource',None)==cut for o in Model.history(part)))

    def test_unverified_source_does_not_promote_stale_loft(self):
        part,body,first,last,added,bottom,top,cut=self.build()
        cut.Ruled=True; group=list(body.Group)
        CadDocument.convert_legacy(self.doc)
        self.assertFalse(getattr(body,'Producer',None)); self.assertEqual(body.Group,group)
        self.assertTrue(any('unverified' in entry for entry in Model.metadata(self.doc).ConversionReport))

    def test_older_file_upgrade_preserves_section_and_access_link_uuids(self):
        part,body,first,last,added,bottom,top,cut=self.build()
        with patch.object(LegacyConversion,'migrate_lofts'): CadDocument.convert_legacy(self.doc)
        aliases=[o for o in Model.history(part) if getattr(o,'LegacySketchSource',None)]
        ids={o.Name:o.ObjectId for o in aliases+[first,last,bottom,top]}
        labels={o.Name:o.Label for o in (first,last,bottom,top,added,cut)}
        saved=self.output/'PreviousLofts.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc=CadDocument.open(saved)
        for name,identity in ids.items(): self.assertEqual(self.doc.getObject(name).ObjectId,identity)
        for name,label in labels.items(): self.assertEqual(self.doc.getObject(name).Label,label)
        self.mapped(self.doc.Part,self.doc.Body,self.doc.AdditiveLoft,self.doc.SubtractiveLoft)
        self.assertEqual(Model.metadata(self.doc).LegacyLoftVersion,1)
        count=len(self.doc.Objects); CadDocument.convert_legacy(self.doc); self.assertEqual(count,len(self.doc.Objects))

    def test_actual_shared_history_task_order_preview_accept_cancel_and_undo(self):
        part,body,first,last,added,bottom,top,cut=self.build(third=True); CadDocument.convert_legacy(self.doc)
        Task=importlib.import_module('freecad.gui.ComponentLoftTask')
        self.open_row(part,added)
        loaded = Path(Task.__file__).resolve()
        expected = Path(os.environ['FREECAD_PLUS_SOURCE']).resolve() / 'src/Gui/ComponentLoftTask.py'
        self.assertEqual(hashlib.sha256(loaded.read_bytes()).digest(),
                         hashlib.sha256(expected.read_bytes()).digest())
        if os.environ.get('FREECAD_PLUS_PROFILE_SOURCE') != '1':
            self.assertTrue(loaded.is_relative_to(Path(App.ConfigGet('AppHomePath')).resolve()))
        self.assertIsNotNone(Task._task); task=Task._task; task.auto_preview.setChecked(False)
        sections=task.values()[0]; task.reverse_sections()
        self.assertEqual(task.values()[0],list(reversed(sections)))
        self.assertTrue(task.preview(),task.status.text())
        task.form.grab().save(str(self.output/'legacy-loft-task.png'))
        self.assertTrue(task.accept()); self.assertEqual(Loft.read(added)[0],list(reversed(sections)))
        self.doc.undo(); self.doc.recompute(); self.assertEqual(Loft.read(added)[0],sections)
        self.doc.redo(); self.doc.recompute()
        self.open_row(part,added); self.assertIsNotNone(Task._task)
        Task._task.reverse_sections(); Task._task.reject()
        self.assertEqual(Loft.read(added)[0],list(reversed(sections)))

    def test_actual_retained_native_loft_editor_close(self):
        part,body,first,last,added,bottom,top,cut=self.build(retained=True); CadDocument.convert_legacy(self.doc)
        alias=next(o for o in Model.history(part) if getattr(o,'LegacyLoftSource',None)==cut)
        refs=cut.Profile,list(cut.Sections),cut.BaseFeature
        self.open_row(part,alias); edit=Gui.getDocument(self.doc.Name).getInEdit()
        self.assertIsNotNone(edit); self.assertEqual(edit.Object,cut)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute(); self.assertEqual((cut.Profile,list(cut.Sections),cut.BaseFeature),refs)

    def test_standalone_part_loft_preserves_degree_linearization_and_sheet(self):
        part=self.doc.addObject('App::Part','Part')
        sections=[self.circle(part,'Section'+str(i),z,2) for i,z in enumerate((0,5,10))]
        solid=self.doc.addObject('Part::Loft','NativeLoft'); part.addObject(solid)
        solid.Sections=sections; solid.Solid=True; solid.Ruled=True; solid.MaxDegree=3; solid.Linearize=True
        sheet=self.doc.addObject('Part::Loft','NativeSheet'); part.addObject(sheet)
        sheet.Sections=sections; sheet.Solid=False; sheet.Ruled=False
        self.doc.recompute(); before=solid.Shape.copy(); identity=solid.Name,solid.TypeId,solid.ID
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(identity,(solid.Name,solid.TypeId,solid.ID)); self.same(before,solid.Shape)
        self.assertEqual(solid.Sections,sections); self.assertEqual(solid.MaxDegree,3); self.assertTrue(solid.Linearize)
        result=next(o for o in Model.history(part) if getattr(o,'Producer',None)==solid)
        self.assertIn(result.Name,part.ResultObjects); self.assertNotIn(solid.Name,part.ResultObjects)
        self.assertEqual(sheet.LegacyLoftState,'Retained native standalone loft'); self.assertEqual(len(sheet.Shape.Solids),0)
        with Model.transaction(self.doc,'Edit native Part Loft sections'): solid.Sections=list(reversed(sections))
        self.same(solid.Shape,result.Shape)

    def test_mixed_pad_loft_chain_preserves_inputs_and_previous_result(self):
        part=self.doc.addObject('App::Part','Part'); body=self.doc.addObject('PartDesign::Body','Body'); part.addObject(body)
        first=self.circle(body,'Base',0,4); pad=body.newObject('PartDesign::Pad','Pad'); pad.Profile=first; pad.Length=10
        bottom=self.circle(body,'Bottom',10,4); top=self.circle(body,'Top',15,3)
        loft=body.newObject('PartDesign::AdditiveLoft','AdditiveLoft'); loft.Profile=bottom; loft.Sections=[(top,[''])]; body.Tip=loft
        self.doc.recompute(); self.assertNotIn('Invalid',body.State); before=body.Shape.copy()
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.LegacyHistoryState,'Mapped native loft chain',str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(loft.BaseFeature.Producer,pad); self.assertEqual(loft.ConsumedResults,[loft.BaseFeature])
        self.assertEqual(loft.LoftMode,'Add'); self.assertEqual(pad.ExtrudeMode,'New Body'); self.same(before,body.Shape)
        self.assertFalse(any(getattr(o,'LegacyExtrudeSource',None)==pad for o in Model.history(part)))
        Model.validate(self.doc)

    def test_native_vertex_end_section_keeps_exact_subelement(self):
        part=self.doc.addObject('App::Part','Part'); body=self.doc.addObject('PartDesign::Body','Body'); part.addObject(body)
        base=self.circle(body,'Base',0,2); end=self.circle(body,'End',10,1)
        loft=body.newObject('PartDesign::AdditiveLoft','AdditiveLoft'); loft.Profile=base; loft.Sections=[(end,['Vertex1'])]; body.Tip=loft
        self.doc.recompute(); self.assertNotIn('Invalid',body.State); before=body.Shape.copy(); refs=list(loft.Sections)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.LegacyHistoryState,'Mapped native loft chain',str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(list(loft.Sections),refs); self.same(before,body.Shape)
        sections,mode,target,options=Loft.read(loft)
        self.assertEqual(sections[-1],(end,['Vertex1']))
        self.same(Loft.preview(part,sections,mode,target,options),loft.Shape)

    def test_closed_native_sections_and_placed_frames(self):
        part=self.doc.addObject('App::Part','Part'); body=self.doc.addObject('PartDesign::Body','Body'); part.addObject(body)
        sections=[]
        for i,(yz,x) in enumerate(((False,-40),(True,-40),(False,40),(True,40))):
            sketch=self.doc.addObject('Sketcher::SketchObject','ClosedSection'+str(i)); body.addObject(sketch)
            sketch.Placement.Rotation=(App.Rotation(App.Vector(0,1,0),App.Vector(0,0,1),App.Vector(1,0,0),'ZXY')
                                      if yz else App.Rotation(App.Vector(1,0,0),90))
            sketch.addGeometry(Part.Circle(App.Vector(x,0,0),App.Vector(0,0,1),10),False)
            sections.append(sketch)
        loft=body.newObject('PartDesign::AdditiveLoft','ClosedLoft'); loft.Profile=sections[0]
        loft.Sections=[(o,['']) for o in sections[1:]]; loft.Closed=True; body.Tip=loft
        self.doc.recompute(); self.assertNotIn('Invalid',body.State); before=body.Shape.copy(); frames=[o.Placement for o in sections]
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.LegacyHistoryState,'Mapped native loft chain',str(Model.metadata(self.doc).ConversionReport))
        self.assertTrue(loft.Closed); self.same(before,body.Shape)
        for obj,frame in zip(sections,frames): self.assertTrue(obj.Placement.isSame(frame,1e-9))
        inputs,mode,target,options=Loft.read(loft)
        self.same(Loft.preview(part,inputs,mode,target,options),body.Shape)

    def test_original_additive_type_can_subtract_without_replacement(self):
        part,body,first,last,added,bottom,top,cut=self.build(); CadDocument.convert_legacy(self.doc)
        sections=[(self.circle(part,'Larger'+str(i),z,5),None) for i,z in enumerate((0,10))]
        self.doc.recompute(); operation,target=Loft.create(part,sections)
        Model.reorder_history(part,[operation],0)
        identity=added.Name,added.TypeId,added.ID,added.ObjectId
        Loft.edit(added,Loft.read(added)[0],'Subtract',target)
        self.assertEqual(identity,(added.Name,added.TypeId,added.ID,added.ObjectId))
        self.assertEqual(added.Operation,'Subtraction'); self.assertEqual(added.LoftMode,'Subtract')
        self.assertAlmostEqual(added.Shape.Volume,90*math.pi,places=7)
        self.assertEqual(added.ConsumedResults,[target])
        self.doc.undo(); self.doc.recompute(); self.assertEqual(added.Operation,'Union')
        self.assertEqual(added.LoftMode,'New Body')

    def test_native_no_material_shared_sections_keep_original_consumers(self):
        part,body,first,last,added,bottom,top,cut=self.build()
        # A valid native no-op uses the SAME section sources as the first Loft.
        body.removeObject(cut); body.removeObject(bottom); body.removeObject(top)
        self.doc.removeObject(cut.Name); self.doc.removeObject(bottom.Name); self.doc.removeObject(top.Name)
        repeated=body.newObject('PartDesign::AdditiveLoft','RepeatedLoft')
        repeated.Profile=first; repeated.Sections=[(last,[''])]; body.Tip=repeated
        self.doc.recompute(); self.assertNotIn('Invalid',body.State); before=body.Shape.copy(); group=list(body.Group)
        self.assertAlmostEqual(added.Shape.Volume,repeated.Shape.Volume)
        CadDocument.convert_legacy(self.doc)
        self.assertFalse(getattr(body,'Producer',None)); self.assertEqual(body.Group,group)
        self.assertEqual(repeated.Profile[0],first); self.assertEqual(repeated.Sections[0][0],last)
        self.assertEqual(added.Profile[0],first); self.assertEqual(added.Sections[0][0],last)
        self.same(before,body.Shape)
        self.assertTrue(any('no-material' in entry for entry in Model.metadata(self.doc).ConversionReport))
