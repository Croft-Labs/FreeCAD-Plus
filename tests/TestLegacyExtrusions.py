# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native extrusion chain conversion, targets, extents and retained engines."""
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
import ComponentExtrude as Extrude
import ComponentExtent as Extent
import LegacyConversion
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestLegacyExtrusions(unittest.TestCase):
    def setUp(self):
        self.names = set(App.listDocuments())
        self.doc = App.newDocument('LegacyExtrusions')
        self.doc.UndoMode = 1
        self.output = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])

    def tearDown(self):
        Task = importlib.import_module('freecad.gui.ComponentExtrudeTask')
        if Task._task: Task._task.reject()
        for name in set(App.listDocuments()) - self.names:
            gui = Gui.getDocument(name)
            if gui.getInEdit(): gui.resetEdit()
            if Gui.Control.activeDialog(): Gui.Control.closeDialog()
            App.closeDocument(name)
        Gui.updateGui()

    def build(self, retained=False, third=False):
        part = self.doc.addObject('App::Part','Part')
        part.Placement = App.Placement(App.Vector(20,2,1),App.Rotation(App.Vector(0,1,0),35))
        body = self.doc.addObject('PartDesign::Body','Body'); part.addObject(body)
        def sketch(name,radius,z,x=0):
            obj = body.newObject('Sketcher::SketchObject',name)
            obj.Placement.Base.z = z
            obj.addGeometry(Part.Circle(App.Vector(x,0,0),App.Vector(0,0,1),radius),False)
            obj.addConstraint(Sketcher.Constraint('Radius',0,radius))
            return obj
        first = sketch('Sketch',4,0)
        pad = body.newObject('PartDesign::Pad','Pad'); pad.Profile = first; pad.Length = 10
        second = sketch('CutSketch',1,10)
        pocket = body.newObject('PartDesign::Pocket','Pocket'); pocket.Profile = second; pocket.Length = 3
        body.Tip = pocket
        if third:
            third_sketch = sketch('AddSketch',1,10,2)
            added = body.newObject('PartDesign::Pad','AddPad'); added.Profile = third_sketch; added.Length = 2
            body.Tip = added
        if retained:
            plane = body.newObject('PartDesign::Plane','DatumPlane'); plane.Placement.Base.z = 10
            second.AttachmentSupport = [(plane,'')]; second.MapMode = 'ObjectXY'
            body.Tip = pocket
            body.Placement = App.Placement(App.Vector(7,3,2),App.Rotation(App.Vector(0,1,0),25))
        for i,transform in enumerate((False,True)):
            link = self.doc.addObject('App::Link','Use'+str(i)); link.setLink(part)
            link.LinkTransform = transform; link.LinkPlacement.Base.x = 50+i*20
        self.doc.recompute()
        self.assertNotIn('Invalid',body.State)
        self.assertAlmostEqual(pad.Shape.Volume,math.pi*16*10,places=7)
        self.assertAlmostEqual(pocket.Shape.Volume,math.pi*(160-3),places=7)
        return part,body,first,pad,second,pocket

    def same(self,a,b):
        self.assertAlmostEqual(a.Volume,b.Volume,places=8)
        self.assertAlmostEqual(a.cut(b).Volume,0,places=8)
        self.assertAlmostEqual(b.cut(a).Volume,0,places=8)

    def mapped(self,part,body,pad,pocket):
        self.assertEqual(body.LegacyHistoryState,'Mapped native extrusion chain',str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(Model.owner(pad),part); self.assertEqual(Model.owner(pocket),part)
        self.assertEqual(pad.ExtrudeMode,'New Body'); self.assertEqual(pocket.ExtrudeMode,'Subtract')
        target = pocket.BaseFeature
        self.assertEqual(target.Producer,pad); self.assertEqual(pocket.ConsumedResults,[target])
        self.assertEqual(body.Producer,pocket); self.assertEqual(body.Tip.Producer,pocket)
        self.assertEqual(Model.finished_results(part),[body])
        self.assertLess(part.ModelHistory.index(pad.Name),part.ModelHistory.index(target.Name))
        self.assertLess(part.ModelHistory.index(target.Name),part.ModelHistory.index(pocket.Name))
        Model.validate(self.doc)

    def test_chain_identities_explicit_results_shared_geometry_and_conversion_undo(self):
        part,body,first,pad,second,pocket = self.build()
        identities = [(o.Name,o.TypeId,o.ID) for o in (body,first,pad,second,pocket)]
        group = list(body.Group)
        shapes = {o.Name:Part.getShape(o).copy() for o in (part,body,self.doc.Use0,self.doc.Use1)}
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,pad,pocket)
        self.assertEqual(identities,[(o.Name,o.TypeId,o.ID) for o in (body,first,pad,second,pocket)])
        for name,shape in shapes.items(): self.same(shape,Part.getShape(self.doc.getObject(name)))
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(body.Group,group); self.assertEqual(body.Tip,pocket)
        self.doc.redo(); self.doc.recompute(); self.mapped(part,body,pad,pocket)

    def test_shared_editor_pocket_direction_parameters_undo_and_reopen(self):
        part,body,first,pad,second,pocket = self.build()
        original = self.output/'Extrusions.FCStd'; self.doc.saveAs(str(original))
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,pad,pocket)
        ids = {o.Name:o.ObjectId for o in (part,body,first,pad,second,pocket,pocket.BaseFeature)}
        self.assertTrue(Extrude.reversed_direction(pocket))
        Extrude.edit(pocket,second,4,Extrude.reversed_direction(pocket))
        self.assertFalse(pocket.Reversed); self.assertAlmostEqual(body.Shape.Volume,math.pi*156,places=7)
        self.doc.undo(); self.doc.recompute(); self.assertAlmostEqual(body.Shape.Volume,math.pi*157,places=7)
        self.doc.redo(); self.doc.recompute()
        saved = self.output/'Extrusions.cadprt'; self.doc.saveAs(str(saved))
        self.assertEqual(digest,hashlib.sha256(original.read_bytes()).hexdigest())
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        for name,identity in ids.items(): self.assertEqual(self.doc.getObject(name).ObjectId,identity)
        Extrude.edit(self.doc.Pocket,self.doc.CutSketch,5,True)
        self.assertAlmostEqual(self.doc.Body.Shape.Volume,math.pi*155,places=7)

    def test_additive_subtractive_chain_preserves_modes_and_extents(self):
        part,body,first,pad,second,pocket = self.build(third=True)
        before = body.Shape.copy()
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.LegacyHistoryState,'Mapped native extrusion chain',str(Model.metadata(self.doc).ConversionReport))
        added = self.doc.AddPad
        self.assertEqual(added.ExtrudeMode,'Add')
        self.assertEqual(added.BaseFeature.Producer,pocket)
        self.assertEqual(added.ConsumedResults,[added.BaseFeature])
        self.same(before,body.Shape)
        Extrude.edit(added,self.doc.AddSketch,3)
        self.assertAlmostEqual(body.Shape.Volume,math.pi*160,places=7)
        original_id = pocket.ObjectId
        Extrude.edit(pocket,second,3,True,mode='Add',target=pocket.BaseFeature)
        self.assertEqual(pocket.ExtrudeMode,'Add'); self.assertEqual(pocket.ObjectId,original_id)
        self.assertEqual(pocket.TypeId,'PartDesign::Pocket')
        self.assertAlmostEqual(body.Shape.Volume,math.pi*163,places=7)
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(pocket.ExtrudeMode,'Subtract')

    def test_native_through_all_and_expression_extent_preserved(self):
        part,body,first,pad,second,pocket = self.build()
        pocket.Type = 'ThroughAll'; pad.setExpression('Length','Sketch.Constraints[0] * 2.5')
        self.doc.recompute(); shape = body.Shape.copy(); expression = list(pad.ExpressionEngine)
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,pad,pocket)
        self.same(shape,body.Shape)
        self.assertEqual(pocket.Type,'ThroughAll'); self.assertEqual(list(pad.ExpressionEngine),expression)
        with self.assertRaisesRegex(ValueError,'expressions'): Extrude.edit(pad,first,12)
        with Model.transaction(self.doc,'Edit original expression input'):
            first.setDatum(0,App.Units.Quantity('5 mm'))
        # The independent cut profile remains at z=10. Native ThroughAll cuts
        # backward from that plane; growing Pad above it must retain the cap.
        self.assertAlmostEqual(body.Shape.Volume,math.pi*(25*12.5-10),places=7)

    def test_retained_attachments_frames_native_parameters_and_target(self):
        part,body,first,pad,second,pocket = self.build(retained=True)
        group,tip = list(body.Group),body.Tip
        shape = Part.getShape(self.doc.Use0).copy(); support = list(second.AttachmentSupport)
        CadDocument.convert_legacy(self.doc)
        aliases = [o for o in Model.history(part) if getattr(o,'LegacyExtrudeSource',None)]
        self.assertEqual({o.LegacyExtrudeSource for o in aliases},{pad,pocket})
        self.assertEqual((body.Group,body.Tip),(group,tip))
        self.assertEqual(list(second.AttachmentSupport),support)
        alias = next(o for o in aliases if o.LegacyExtrudeSource==pocket)
        self.assertEqual(alias.LegacyExtrudeTarget,pad)
        self.assertTrue(alias.LinkPlacement.isSame(body.Placement.multiply(pocket.Placement),1e-8))
        self.same(shape,Part.getShape(self.doc.Use0))
        with Model.transaction(self.doc,'Edit native retained pocket'):
            pocket.Length = 4
        self.assertAlmostEqual(body.Shape.Volume,math.pi*156,places=7)

    def test_older_file_upgrade_and_missing_native_operation(self):
        part,body,first,pad,second,pocket = self.build(retained=True)
        with patch.object(LegacyConversion,'migrate_extrusions'):
            CadDocument.convert_legacy(self.doc)
        saved = self.output/'PreviousExtrusions.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        self.assertEqual(Model.metadata(self.doc).LegacyExtrudeVersion,1)
        count = len(self.doc.Objects); CadDocument.convert_legacy(self.doc)
        self.assertEqual(count,len(self.doc.Objects))
        alias = next(o for o in self.doc.Objects if getattr(o,'LegacyExtrudeSource',None)==self.doc.Pocket)
        with Model.transaction(self.doc,'Delete native pocket'):
            self.doc.removeObject(self.doc.Pocket.Name)
        self.assertEqual(Model.history_state(alias),'Needs repair')
        self.assertIn('missing',Model.history_detail(alias))

    def open_row(self,part,obj):
        Navigator = importlib.import_module('freecad.gui.ComponentNavigator')
        # Undo/Redo's deferred native view restoration must settle before the
        # owner opens a component tab and double-clicks its current History row.
        Gui.updateGui(); QtTest.QTest.qWait(250)
        panel = Navigator.show(self.doc)
        panel.open_component_tab(Navigator.object_key(part)); panel.tabs.setCurrentWidget(panel.history)
        panel.setFloating(True); panel.resize(850,650); panel.show()
        Gui.getMainWindow().show(); Gui.updateGui(); QtTest.QTest.qWait(200); panel.refresh()
        row = next((panel.history.topLevelItem(i) for i in range(panel.history.topLevelItemCount())
                   if panel.history.topLevelItem(i).data(0,QtCore.Qt.UserRole)==Navigator.object_key(obj)),None)
        self.assertIsNotNone(row,str((panel.root_key,panel.active_key,list(part.ModelHistory),
            [(panel.history.topLevelItem(i).text(2),panel.history.topLevelItem(i).data(0,QtCore.Qt.UserRole))
             for i in range(panel.history.topLevelItemCount())])))
        panel.history.scrollToItem(row)
        Gui.updateGui(); QtTest.QTest.qWait(100)
        rect = panel.history.visualItemRect(row)
        point = QtCore.QPoint(panel.history.header().sectionViewportPosition(2)+18,rect.center().y())
        QtTest.QTest.mouseClick(panel.history.viewport(),QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,point)
        panel.refresh()
        row = next(panel.history.topLevelItem(i) for i in range(panel.history.topLevelItemCount())
                   if panel.history.topLevelItem(i).data(0,QtCore.Qt.UserRole)==Navigator.object_key(obj))
        rect = panel.history.visualItemRect(row)
        point = QtCore.QPoint(panel.history.header().sectionViewportPosition(2)+18,rect.center().y())
        self.assertEqual(panel.history.indexAt(point).column(),2)
        self.assertEqual(panel.history.itemAt(point).data(0,QtCore.Qt.UserRole),Navigator.object_key(obj))
        QtTest.QTest.mouseDClick(panel.history.viewport(),QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,point)
        Gui.updateGui(); QtTest.QTest.qWait(200)

    def test_actual_shared_pocket_task_accept_cancel_and_undo(self):
        Task = importlib.import_module('freecad.gui.ComponentExtrudeTask')
        part,body,first,pad,second,pocket = self.build()
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,pad,pocket)
        self.open_row(part,pocket)
        loaded = Path(Task.__file__).resolve()
        expected = Path(os.environ['FREECAD_PLUS_SOURCE']).resolve() / 'src/Gui/ComponentExtrudeTask.py'
        self.assertEqual(hashlib.sha256(loaded.read_bytes()).digest(),
                         hashlib.sha256(expected.read_bytes()).digest())
        if os.environ.get('FREECAD_PLUS_PROFILE_SOURCE') != '1':
            self.assertTrue(loaded.is_relative_to(Path(App.ConfigGet('AppHomePath')).resolve()))
        self.assertIsNotNone(Task._task)
        task = Task._task
        self.assertTrue(task.reverse.isChecked()); self.assertEqual(task.target.currentData(),pocket.BaseFeature.Name)
        task.length.setProperty('rawValue',4.)
        self.assertTrue(task.accept())
        self.assertAlmostEqual(body.Shape.Volume,math.pi*156,places=7)
        self.doc.undo(); self.doc.recompute(); self.assertAlmostEqual(body.Shape.Volume,math.pi*157,places=7)
        self.doc.redo(); self.doc.recompute()
        self.open_row(part,pocket); self.assertIsNotNone(Task._task)
        Task._task.length.setProperty('rawValue',8.); Task._task.reject()
        self.assertAlmostEqual(body.Shape.Volume,math.pi*156,places=7)

    def test_actual_retained_native_pocket_editor_close(self):
        part,body,first,pad,second,pocket = self.build(retained=True)
        CadDocument.convert_legacy(self.doc)
        alias = next(o for o in Model.history(part) if getattr(o,'LegacyExtrudeSource',None)==pocket)
        target,length,support = pocket.BaseFeature,pocket.Length.Value,list(second.AttachmentSupport)
        self.open_row(part,alias)
        edit = Gui.getDocument(self.doc.Name).getInEdit()
        self.assertIsNotNone(edit); self.assertEqual(edit.Object,pocket)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute()
        self.assertEqual(pocket.BaseFeature,target); self.assertEqual(pocket.Length.Value,length)
        self.assertEqual(list(second.AttachmentSupport),support)

    def test_explicit_retarget_preserves_operation_and_final_body(self):
        part,body,first,pad,second,pocket = self.build()
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,pad,pocket)
        original_target = pocket.BaseFeature
        added,target = Extrude.create(part,first,9)
        Model.reorder_history(part,[added],0)
        pocket_id,body_id = pocket.ObjectId,body.ObjectId
        Extrude.edit(pocket,second,4,True,mode='Subtract',target=target)
        self.assertEqual(pocket.BaseFeature,target); self.assertEqual(pocket.ConsumedResults,[target])
        self.assertEqual(pocket.ObjectId,pocket_id); self.assertEqual(body.ObjectId,body_id)
        self.assertAlmostEqual(body.Shape.Volume,math.pi*(16*9-3),places=7)
        self.doc.undo(); self.doc.recompute(); self.assertEqual(pocket.BaseFeature,original_target)

    def test_two_sided_native_lengths_and_taper_remain_unchanged(self):
        part,body,first,pad,second,pocket = self.build()
        pad.SideType = 'Two sides'; pad.Length2 = 2; pad.TaperAngle = 2
        self.doc.recompute(); before = body.Shape.copy(); parameters = Extent.read(pad)
        self.assertNotIn('Invalid',body.State)
        CadDocument.convert_legacy(self.doc); self.mapped(part,body,pad,pocket)
        self.assertEqual(Extent.read(pad),parameters); self.same(before,body.Shape)

    def test_standalone_native_extrusion_published_and_custom_output_retained(self):
        part = self.doc.addObject('App::Part','Part')
        sketch = self.doc.addObject('Sketcher::SketchObject','Sketch'); part.addObject(sketch)
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
        normal = self.doc.addObject('Part::Extrusion','NormalExtrusion'); part.addObject(normal)
        normal.Base = sketch; normal.DirMode = 'Normal'; normal.LengthFwd = 5; normal.Solid = True
        custom = self.doc.addObject('Part::Extrusion','CustomExtrusion'); part.addObject(custom)
        custom.Base = sketch; custom.Dir = App.Vector(0,0,7); custom.Solid = True
        self.doc.recompute()
        before = custom.Shape.copy(); identity = normal.Name,normal.TypeId,normal.ID
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(identity,(normal.Name,normal.TypeId,normal.ID))
        self.assertEqual(normal.OperationKind,'Extrude')
        result = next(o for o in Model.history(part) if getattr(o,'Producer',None)==normal)
        self.assertIn(result.Name,part.ResultObjects); self.assertNotIn(normal.Name,part.ResultObjects)
        Extrude.edit(normal,sketch,6)
        self.assertAlmostEqual(result.Shape.Volume,math.pi*4*6,places=7)
        self.assertEqual(custom.LegacyExtrudeState,'Retained native standalone extrusion')
        self.same(before,custom.Shape)

    def test_new_body_mode_preserves_native_pocket_and_clears_consumed_target(self):
        part,body,first,pad,second,pocket = self.build()
        CadDocument.convert_legacy(self.doc)
        identity = pocket.Name,pocket.TypeId,pocket.ID,pocket.ObjectId
        Extrude.edit(pocket,second,3,True,mode='New Body')
        self.assertEqual(identity,(pocket.Name,pocket.TypeId,pocket.ID,pocket.ObjectId))
        self.assertIsNone(pocket.BaseFeature); self.assertEqual(pocket.ConsumedResults,[])
        self.assertAlmostEqual(body.Shape.Volume,math.pi*3,places=7)
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(pocket.ExtrudeMode,'Subtract'); self.assertTrue(pocket.ConsumedResults)

    def test_custom_pocket_vector_retains_native_engine_and_parameter_edit(self):
        part,body,first,pad,second,pocket = self.build()
        pocket.UseCustomVector = True; pocket.Direction = App.Vector(0,0,-1)
        pocket.AlongSketchNormal = False; self.doc.recompute()
        self.assertAlmostEqual(body.Shape.Volume,math.pi*157,places=7)
        self.assertEqual(pocket.Direction,App.Vector(0,0,-1))
        before = body.Shape.copy()
        group,tip = list(body.Group),body.Tip
        CadDocument.convert_legacy(self.doc)
        self.assertEqual((body.Group,body.Tip),(group,tip))
        self.same(before,body.Shape)
        alias = next(o for o in Model.history(part) if getattr(o,'LegacyExtrudeSource',None)==pocket)
        self.assertEqual(alias.LinkedObject,pocket)
        with Model.transaction(self.doc,'Edit retained custom vector pocket'):
            pocket.Length = 4
        self.assertFalse(pocket.Reversed)
        self.assertEqual(pocket.Direction,App.Vector(0,0,-1))
        self.assertAlmostEqual(body.Shape.Volume,math.pi*156,places=7)

    def test_older_retained_chain_promotes_original_sketch_and_alias_identities(self):
        part,body,first,pad,second,pocket = self.build()
        with patch.object(LegacyConversion,'migrate_extrusions'):
            CadDocument.convert_legacy(self.doc)
        aliases = [o for o in Model.history(part) if getattr(o,'LegacySketchSource',None)]
        ids = {o.Name:o.ObjectId for o in (first,second)+tuple(aliases)}
        labels = {o.Name:o.Label for o in (first,pad,second,pocket)}
        saved = self.output/'PreviousChain.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        self.mapped(self.doc.Part,self.doc.Body,self.doc.Pad,self.doc.Pocket)
        for name,identity in ids.items(): self.assertEqual(self.doc.getObject(name).ObjectId,identity)
        for name,label in labels.items(): self.assertEqual(self.doc.getObject(name).Label,label)
