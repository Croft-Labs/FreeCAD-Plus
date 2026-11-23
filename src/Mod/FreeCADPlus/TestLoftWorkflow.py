# SPDX-License-Identifier: LGPL-2.1-or-later
"""Loft geometry, task routing, persistence and independent-solid acceptance."""
import math
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, extrude_task, loft, loft_task, modeling, ui_modes
from TestFeatureCenteredModeling import TestFeatureCenteredModeling


class TestLoftWorkflow(unittest.TestCase):
    setUp = TestFeatureCenteredModeling.setUp
    snapshot = TestFeatureCenteredModeling.snapshot

    def tearDown(self):
        if extrude_task._active:extrude_task._active.reject()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():Gui.activeDocument().resetEdit()
        if self.doc.HasPendingTransaction:self.doc.abortTransaction()
        TestFeatureCenteredModeling.tearDown(self)

    def sections(self, sheet=False, holes=False):
        refs = []
        for z in (0, 10, 20):
            sketch = modeling.new_sketch(self.doc);sketch.Placement.Base.z = z
            sketch.addGeometry(Part.LineSegment(App.Vector(0,0,0), App.Vector(4,0,0)) if sheet else
                               Part.Circle(App.Vector(),App.Vector(0,0,1),4),False)
            if holes:sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
            refs.append((sketch,''))
        self.doc.recompute();return refs

    def solid(self, x=0):
        body = self.owner.newObject('PartDesign::Body','Body')
        solid = body.newObject('PartDesign::Feature','Solid')
        solid.Shape = Part.makeBox(20,20,10,App.Vector(x-10,-10,-5));body.Tip=solid
        self.doc.recompute();return solid

    def test_solid_ruled_holes_and_read_only_preview(self):
        for holes in (False,True):
            refs=self.sections(holes=holes);before=self.snapshot()
            for ruled in (False,True):
                result,tool,_=loft.evaluate(self.owner,refs,{},dict(loft.DEFAULTS,ruled=ruled))
                self.assertTrue(result.isValid());self.assertEqual(len(result.Solids),1)
                self.assertAlmostEqual(result.Volume,math.pi*(12 if holes else 16)*20,places=4)
                self.assertTrue(tool.isValid());self.assertEqual(self.snapshot(),before)

    def test_open_and_closed_sheet_profiles(self):
        for open_curve in (True,False):
            refs=self.sections(sheet=open_curve)
            shape,_,_=loft.evaluate(self.owner,refs,{},dict(loft.DEFAULTS,output='Sheet',operation='Subtract'))
            self.assertTrue(shape.isValid());self.assertFalse(shape.Solids)
            self.assertAlmostEqual(shape.Area,80 if open_curve else 160*math.pi,places=4)
            if open_curve:
                with self.assertRaisesRegex(ValueError,'closed'):loft.evaluate(self.owner,refs,{},loft.DEFAULTS)

    def test_planar_face_sections_and_vertex_endpoint(self):
        refs=[]
        for z in (0,10):
            obj=self.owner.newObject('Part::Feature','Sheet');obj.Shape=Part.makePlane(4,4,App.Vector(0,0,z))
            refs.append((obj,'Face1'))
        self.doc.recompute();shape,_,_=loft.evaluate(self.owner,refs,{},loft.DEFAULTS)
        self.assertAlmostEqual(shape.Volume,160)
        point=self.owner.newObject('Part::Feature','Point');point.Shape=Part.Vertex(App.Vector(2,2,20));self.doc.recompute()
        shape,_,_=loft.evaluate(self.owner,[refs[0],(point,'Vertex1')],{},loft.DEFAULTS)
        self.assertAlmostEqual(shape.Volume,320/3,places=4)
        with self.assertRaisesRegex(ValueError,'either end'):
            loft.evaluate(self.owner,[refs[0],(point,'Vertex1'),refs[1]],{},loft.DEFAULTS)
        feature=loft.save(self.doc,[refs[0],(point,'Vertex1')],{},loft.DEFAULTS)
        task=loft_task.show(feature);self.assertTrue(task.valid)
        from pivy import coin
        search=coin.SoSearchAction();search.setType(coin.SoPointSet.getClassTypeId());search.apply(task.profile_highlight)
        self.assertIsNotNone(search.getPath());task.reject()

    def test_add_subtract_invalid_contact_and_active_body_independence(self):
        refs=self.sections();first=self.solid();second=self.solid(60)
        before=self.snapshot();links={'target':(first,'')}
        for active in (second.getParentGeoFeatureGroup(),None):
            Gui.activeDocument().activeView().setActiveObject('pdbody',active)
            for mode,expected in [('Add',4000+240*math.pi),('Subtract',4000-80*math.pi)]:
                shape,_,_=loft.evaluate(self.owner,refs,links,dict(loft.DEFAULTS,operation=mode))
                # Native smooth lofts are B-spline surfaces; volume integration
                # across Boolean splits is numerical (one part per million).
                self.assertAlmostEqual(shape.Volume,expected,delta=expected*1e-6)
            self.assertEqual(Gui.activeDocument().activeView().getActiveObject('pdbody'),active)
        for mode in ('Add','Subtract'):
            with self.assertRaises(loft.InvalidResult) as error:
                loft.evaluate(self.owner,refs,{'target':(second,'')},dict(loft.DEFAULTS,operation=mode))
            self.assertTrue(error.exception.tool.isValid())
        self.assertEqual(self.snapshot(),before)

    def test_save_edit_undo_recompute_and_reopen(self):
        refs=self.sections();feature=loft.save(self.doc,refs,{},loft.DEFAULTS)
        identity,name=feature.ID,feature.Name
        self.assertTrue(all(not obj.Visibility for obj,_ in refs))
        self.assertTrue(all(document.history(self.doc,self.owner).index(obj)<document.history(self.doc,self.owner).index(feature) for obj,_ in refs))
        loft.save(self.doc,refs,{},dict(loft.DEFAULTS,output='Sheet',ruled=True),feature)
        self.assertEqual(feature.ID,identity);self.assertFalse(feature.Shape.Solids)
        self.doc.undo();self.doc.recompute();self.assertEqual(len(feature.Shape.Solids),1)
        self.doc.redo();self.doc.recompute();self.assertFalse(feature.Shape.Solids)
        refs[-1][0].Placement.Base.z=30;self.doc.recompute();self.assertAlmostEqual(feature.Shape.Area,240*math.pi,places=4)
        path=self.output/'Loft.cadprt';document.save_document(self.doc,path)
        App.closeDocument(self.doc.Name);self.doc=document.open_document(path)
        feature=self.doc.getObject(name);self.assertEqual(feature.ID,identity)
        feature.touch();self.doc.recompute();self.assertFalse(feature.Shape.Solids)
        self.assertAlmostEqual(feature.Shape.Area,240*math.pi,places=4)

    def test_boolean_edit_preserves_target_identity_and_other_solid(self):
        refs=self.sections();first=self.solid();second=self.solid(60)
        Gui.activeDocument().activeView().setActiveObject('pdbody',second.getParentGeoFeatureGroup())
        feature=loft.save(self.doc,refs,{'target':(first,'')},dict(loft.DEFAULTS,operation='Add'))
        identity=feature.ID;self.assertEqual(feature.getParentGeoFeatureGroup(),first.getParentGeoFeatureGroup())
        loft.save(self.doc,refs,{'target':(first,'')},dict(loft.DEFAULTS,operation='Subtract'),feature)
        self.assertEqual(feature.ID,identity);self.assertAlmostEqual(feature.Shape.Volume,4000-80*math.pi,delta=.004)
        self.assertEqual(second.getParentGeoFeatureGroup().Tip,second);self.assertAlmostEqual(second.Shape.Volume,4000)

    def test_invalid_input_and_later_reference_are_atomic(self):
        refs=self.sections();before=self.snapshot()
        for sources,settings in [(refs[:1],{}),(refs[:2],{'closed':True})]:
            with self.assertRaises(ValueError):loft.save(self.doc,sources,{},dict(loft.DEFAULTS,**settings))
        self.assertEqual(self.snapshot(),before)
        feature=loft.save(self.doc,refs,{},loft.DEFAULTS);later=self.sections();before=self.snapshot()
        with self.assertRaises(ValueError):loft.save(self.doc,later,{},loft.DEFAULTS,feature)
        self.assertEqual(self.snapshot(),before)

    def test_task_output_order_edit_cancel_and_manual_preview(self):
        refs=self.sections();Gui.Selection.clearSelection()
        for obj,_ in refs:Gui.Selection.addSelection(obj)
        before=self.snapshot();task=loft_task.show();self.assertTrue(task.valid)
        self.assertEqual(task.refs,refs);task.profiles.setCurrentRow(1);task.move_section(-1)
        self.assertEqual(task.refs[0],refs[1]);task.move_section(1);self.assertEqual(task.refs,refs)
        task.outputs['Sheet'].click();self.assertTrue(task.valid);self.assertFalse(task.result_shape.Solids)
        self.assertTrue(task.modes['New Solid'].isChecked());self.assertTrue(all(not b.isEnabled() for b in task.modes.values()))
        task.outputs['Solid'].click();self.assertTrue(task.valid)
        task.automatic.setChecked(False);task.ruled.setChecked(True);self.assertIsNone(task.tool_preview)
        task.reject();self.assertEqual(self.snapshot(),before)
        Gui.Selection.clearSelection()
        for obj,_ in refs:Gui.Selection.addSelection(obj)
        task=loft_task.show();self.assertTrue(task.accept());feature=task.result;identity=feature.ID
        task=editing.edit_feature(self.doc,feature);self.assertEqual(task.refs,refs)
        task.outputs['Sheet'].click();self.assertTrue(task.accept());self.assertEqual(feature.ID,identity)
        self.assertFalse(feature.Shape.Solids)

    def test_hidden_target_valid_invalid_colors_and_cancel(self):
        refs=self.sections();first=self.solid();second=self.solid(60);first.Visibility=False;before=self.snapshot()
        task=loft_task.show();task.modes['Add'].click();QtTest.QTest.qWait(50)
        self.assertNotIn('target',task.links);self.assertIn('#bd780b',task.fields['target'].styleSheet())
        task.addSelection(self.doc.Name,first.Name,'');self.assertEqual(task.links['target'][0],first)
        task.pick='profile'
        for obj,_ in refs:task.addSelection(self.doc.Name,obj.Name,'')
        self.assertTrue(task.valid);self.assertIsNotNone(task.target_overlay)
        self.assertFalse(first.Visibility);self.assertEqual(first.ViewObject.Transparency,65)
        task.pick='target';task.presentation.update_style();self.assertEqual(first.ViewObject.Transparency,0)
        task.addSelection(self.doc.Name,second.Name,'');self.assertFalse(task.valid);self.assertIsNotNone(task.tool_preview)
        task.modes['Subtract'].click();self.assertFalse(task.valid);self.assertIsNotNone(task.tool_preview)
        task.outputs['Sheet'].click();self.assertTrue(task.valid);self.assertNotIn('target',task.links)
        task.reject();self.assertEqual(self.snapshot(),before)

    def test_section_picking_error_recovery_and_sole_target(self):
        refs=self.sections(sheet=True);first=self.solid()
        task=loft_task.show();task.modes['Add'].click();self.assertEqual(task.links['target'][0],first)
        task.pick='profile';task.addSelection(self.doc.Name,refs[0][0].Name,'')
        self.assertEqual(task.refs,[])
        task.outputs['Sheet'].click()
        for obj,_ in refs:task.addSelection(self.doc.Name,obj.Name,'')
        self.assertTrue(task.valid);self.assertEqual(task.refs,refs)
        task.profiles.setCurrentRow(1);task.remove_profile();self.assertEqual(task.refs,[refs[0],refs[2]])
        task.reject()

    def test_native_and_plus_command_dispatch_no_active_body(self):
        Gui.activateWorkbench('PartDesignWorkbench');refs=self.sections();first=self.solid();second=self.solid(60)
        for active in (second.getParentGeoFeatureGroup(),None):
            Gui.activeDocument().activeView().setActiveObject('pdbody',active)
            for command,mode in [('FreeCADPlus_Loft','New Solid'),('PartDesign_AdditiveLoft','Add'),('PartDesign_SubtractiveLoft','Subtract')]:
                Gui.Selection.clearSelection()
                for obj,_ in refs:Gui.Selection.addSelection(obj)
                before=self.snapshot();Gui.runCommand(command);QtTest.QTest.qWait(60)
                task=extrude_task._active;self.assertIsInstance(task,loft_task.LoftTask)
                self.assertEqual(task.mode(),mode);self.assertEqual(task.refs,refs)
                if mode!='New Solid':self.assertNotIn('target',task.links)
                task.reject();self.assertEqual(before,self.snapshot())
                self.assertEqual(Gui.activeDocument().activeView().getActiveObject('pdbody'),active)

    def test_profile_reference_retains_section_order_same_object(self):
        obj=self.owner.newObject('Part::Feature','Profiles')
        obj.Shape=Part.makeCompound([Part.Wire(Part.makeCircle(4,App.Vector(0,0,z))) for z in (0,10,20)])
        self.doc.recompute();refs=[(obj,'Edge1'),(obj,'Edge2'),(obj,'Edge3')]
        feature=loft.save(self.doc,refs,{},loft.DEFAULTS)
        from freecad_plus import planes
        self.assertEqual(planes.flatten(feature.ProfileReferences),refs)
        self.assertAlmostEqual(feature.Shape.Volume,320*math.pi,places=4)

    def test_closed_sheet_sequence(self):
        refs=[]
        for x,y in ((0,0),(10,0),(0,10)):
            obj=self.owner.newObject('Part::Feature','Section')
            obj.Shape=Part.makeLine(App.Vector(x,y,0),App.Vector(x,y,4));refs.append((obj,''))
        self.doc.recompute()
        shape,_,_=loft.evaluate(self.owner,refs,{},dict(loft.DEFAULTS,output='Sheet',closed=True,ruled=True))
        self.assertTrue(shape.isValid());self.assertFalse(shape.Solids);self.assertEqual(len(shape.Faces),3)
        self.assertAlmostEqual(shape.Area,4*(20+math.sqrt(200)),places=5)

    def test_other_component_sources_and_targets_rejected(self):
        from freecad_plus import hierarchy
        refs=self.sections();other=hierarchy.create_definition(self.doc,'Other')
        source=other.newObject('Part::Feature','Profile');source.Shape=Part.makePlane(4,4,App.Vector(0,0,30))
        body=other.newObject('PartDesign::Body','Body');target=body.newObject('PartDesign::Feature','Solid')
        target.Shape=Part.makeBox(20,20,10);body.Tip=target;self.doc.recompute();before=self.snapshot()
        with self.assertRaises(ValueError):loft.save(self.doc,[refs[0],(source,'Face1')],{},loft.DEFAULTS)
        with self.assertRaises(ValueError):loft.save(self.doc,refs,{'target':(target,'')},dict(loft.DEFAULTS,operation='Subtract'))
        self.assertEqual(before,self.snapshot())

    def test_external_component_recompute_outside_edit_context(self):
        from freecad_plus import external
        document.save_document(self.doc,self.output/'Host.cadprt')
        source=document.new_document('LoftSource');owner=document.validate(source).Definitions[0]
        document.save_document(source,self.output/'Source.cadprt');external.import_file(self.doc,source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc,owner);self.owner=owner
        refs=self.sections();source.recompute();feature=loft.save(self.doc,refs,{},loft.DEFAULTS)
        self.assertEqual(feature.Document,source);identity=feature.ID
        task=loft_task.show(feature);self.assertTrue(task.valid);task.reject()
        editing.edit_file(self.doc)
        refs[-1][0].Placement.Base.z=30;source.recompute()
        self.assertEqual(feature.ID,identity);self.assertTrue(feature.Shape.isValid())
        self.assertAlmostEqual(feature.Shape.Volume,480*math.pi,places=4)

    def test_transformed_target_and_downstream_face_reference(self):
        from freecad_plus import extrusion,planes
        refs=self.sections();target=self.solid();body=target.getParentGeoFeatureGroup()
        body.Placement=App.Placement(App.Vector(1,0,0),App.Rotation(App.Vector(0,0,1),15));self.doc.recompute()
        values=dict(loft.DEFAULTS,operation='Add');links={'target':(target,'')}
        expected=loft.evaluate(self.owner,refs,links,values)[0]
        feature=loft.save(self.doc,refs,links,values)
        actual=planes.shape(self.owner,(feature,''))
        self.assertAlmostEqual(actual.Volume,expected.Volume,places=5)
        self.assertLess((actual.Solids[0].CenterOfMass-expected.Solids[0].CenterOfMass).Length,1e-6)
        face=next('Face'+str(i+1) for i,f in enumerate(feature.Shape.Faces)
                  if isinstance(f.Surface,Part.Plane) and f.CenterOfMass.z>19)
        downstream=extrusion.save(self.doc,[(feature,face)],{'target':(feature,'')},dict(extrusion.DEFAULTS,operation='Add',length=3))
        identity=feature.ID
        loft.save(self.doc,refs,links,dict(values,ruled=True),feature)
        self.assertEqual(feature.ID,identity);self.assertTrue(downstream.Shape.isValid())
        with self.assertRaises(ValueError):loft.save(self.doc,refs,{},dict(loft.DEFAULTS,output='Sheet'),feature)

    def test_classic_and_plus_task_entries_for_multiple_sections(self):
        from TestTaskEntryWorkflows import action_boxes,settle
        Gui.activateWorkbench('PartDesignWorkbench');refs=self.sections()
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/General')
        original=prefs.GetInt('TaskPanelUIMode',0)
        try:
            for mode in (0,1):
                prefs.SetInt('TaskPanelUIMode',mode);Gui.Selection.clearSelection()
                for obj,_ in refs:Gui.Selection.addSelection(obj)
                settle();labels=[label for _,items in action_boxes() for label in items]
                if mode==0:
                    self.assertEqual(labels.count('Loft'),1);self.assertNotIn('Additive Loft',labels);self.assertNotIn('Subtractive Loft',labels)
                else:
                    self.assertIn('Additive Loft',labels);self.assertIn('Subtractive Loft',labels);self.assertNotIn('Loft',labels)
        finally:prefs.SetInt('TaskPanelUIMode',original)
