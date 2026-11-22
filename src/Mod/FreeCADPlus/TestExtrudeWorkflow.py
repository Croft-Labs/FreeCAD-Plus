# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native acceptance for the shared feature-centered Extrude workflow."""
import json
import math
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, extrusion, extrude_task, external, hierarchy, modeling, planes
from TestFeatureCenteredModeling import TestFeatureCenteredModeling


class TestExtrudeWorkflow(TestFeatureCenteredModeling):
    def setUp(self):
        super().setUp()
        self.prefs=App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.previous_mode=self.prefs.GetInt('TaskPanelUIMode',0)
        self.prefs.SetInt('TaskPanelUIMode',0)
        Gui.activateWorkbench('PartDesignWorkbench')

    def tearDown(self):
        if extrude_task._active:extrude_task._active.reject()
        self.prefs.SetInt('TaskPanelUIMode',self.previous_mode)
        super().tearDown()

    def options(self,**kwargs):
        return dict(extrusion.DEFAULTS,**kwargs)

    def make(self,sketch=None,links=None,feature=None,**kwargs):
        return extrusion.save(self.doc,[(sketch or self.circle(),'')],links or {},self.options(**kwargs),feature)

    def target(self):
        sketch=self.circle(6)
        return modeling.extrude_new_solid(self.doc,sketch,6)

    def test_preview_is_read_only_and_new_result_is_associative(self):
        sketch=self.circle()
        before=self.snapshot();docs=set(App.listDocuments())
        result,tool,_=extrusion.evaluate(self.owner,[(sketch,'')],{},self.options(length=5))
        self.assertAlmostEqual(result.Volume,20*math.pi)
        self.assertEqual(self.snapshot(),before);self.assertEqual(set(App.listDocuments()),docs)
        feature=self.make(sketch,length=5)
        self.assertEqual(sketch.getParentGeoFeatureGroup(),self.owner)
        self.assertEqual(feature.getParentGeoFeatureGroup().Tip,feature)
        self.assertEqual(self.doc.UndoCount,before[-1]+1)
        identity=feature.ID;name=feature.Name
        self.doc.undo();self.doc.recompute();self.assertEqual(self.snapshot(),before)
        self.doc.redo();self.doc.recompute();feature=self.doc.getObject(name)
        self.assertEqual(feature.ID,identity)
        sketch.Placement.Base.z=4;self.doc.recompute()
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMin,4)
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMax,9)

    def test_add_subtract_identity_and_target_routing(self):
        target=self.target();sketch=self.circle(2);sketch.Placement.Base.z=6;self.doc.recompute()
        target.ViewObject.ShapeColor=(.2,.6,.4)
        feature=self.make(sketch,{'target':(target,'')},operation='Add',length=3)
        self.assertEqual(feature.ViewObject.ShapeColor,target.ViewObject.ShapeColor)
        self.assertAlmostEqual(feature.Shape.Volume,target.Shape.Volume+12*math.pi)
        identity=feature.ID
        self.make(sketch,{'target':(target,'')},feature,operation='Subtract',length=3,reverse=True)
        self.assertEqual(feature.ID,identity)
        self.assertAlmostEqual(feature.Shape.Volume,target.Shape.Volume-12*math.pi)
        self.assertEqual(feature.getParentGeoFeatureGroup(),target.getParentGeoFeatureGroup())
        self.doc.undo();self.doc.recompute();self.assertEqual(feature.Extrude_operation,'Add')
        self.doc.redo();self.doc.recompute();self.assertEqual(feature.Extrude_operation,'Subtract')

    def test_start_offsets_symmetric_and_independent_sides(self):
        sketch=self.circle()
        for options,low,high in ((dict(start='Offset',start_offset=2,length=5),2,7),
                                  (dict(sides='Symmetric',length=10),-5,5),
                                  (dict(sides='Two sides',length=8,length2=3),-3,8),
                                  (dict(start='Offset',start_offset=-2,length=4,reverse=True),-2,2)):
            shape,_,_=extrusion.evaluate(self.owner,[(sketch,'')],{},self.options(**options))
            self.assertAlmostEqual(shape.BoundBox.ZMin,low);self.assertAlmostEqual(shape.BoundBox.ZMax,high)

    def test_reference_start_end_and_saved_limit_follow(self):
        sketch=self.circle()
        start=self.owner.newObject('Part::Feature','Start');start.Shape=Part.makePlane(20,20,App.Vector(-10,-10,2))
        end=self.owner.newObject('Part::Feature','End');end.Shape=Part.makePlane(20,20,App.Vector(-10,-10,10))
        links={'start':(start,'Face1'),'limit':(end,'Face1')}
        feature=self.make(sketch,links,start='Reference',start_offset=1,end='Up to face',offset=1)
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMin,3)
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMax,11)
        end.Placement.Base.z=4;self.doc.recompute()
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMax,15)

    def test_through_all_first_last_and_shape(self):
        target=self.target();sketch=self.circle(2);sketch.Placement.Base.z=8;self.doc.recompute()
        for kind,expected in (('Through all',target.Shape.Volume-24*math.pi),('To last',target.Shape.Volume-24*math.pi)):
            shape,_,_=extrusion.evaluate(self.owner,[(sketch,'')],{'target':(target,'')},
                                         self.options(operation='Subtract',end=kind,reverse=True))
            self.assertAlmostEqual(shape.Volume,expected,places=5)
        shape,_,_=extrusion.evaluate(self.owner,[(sketch,'')],{'target':(target,'')},
                                     self.options(operation='Subtract',end='Through all',sides='Symmetric'))
        self.assertAlmostEqual(shape.Volume,target.Shape.Volume-24*math.pi,places=5)
        # A profile below the target reaches its near face, and up-to-shape
        # reaches the selected solid's outer boundary using the native solver.
        sketch.Placement.Base.z=-2;self.doc.recompute()
        shape,tool,_=extrusion.evaluate(self.owner,[(sketch,'')],{'target':(target,'')},self.options(operation='Add',end='To first'))
        self.assertAlmostEqual(tool.BoundBox.ZMax,0)
        self.assertGreater(shape.Volume,target.Shape.Volume)
        shape,tool,_=extrusion.evaluate(self.owner,[(sketch,'')],{'target':(target,''),'limit':(target,'')},self.options(operation='Add',end='Up to shape'))
        self.assertGreater(shape.Volume,target.Shape.Volume)

    def test_taper_and_custom_direction_measurement(self):
        sketch=self.circle(4)
        straight,_,_=extrusion.evaluate(self.owner,[(sketch,'')],{},self.options(length=5))
        tapered,_,_=extrusion.evaluate(self.owner,[(sketch,'')],{},self.options(length=5,taper=5))
        self.assertNotAlmostEqual(straight.Volume,tapered.Volume)
        axis=self.owner.newObject('Part::Feature','Axis');axis.Shape=Part.makeLine(App.Vector(),App.Vector(1,0,1))
        for measure,expected in (('Along direction',5/math.sqrt(2)),('Along profile normal',5)):
            shape,_,_=extrusion.evaluate(self.owner,[(sketch,'')],{'direction':(axis,'Edge1')},
                    self.options(length=5,direction='Selected axis / line',measure=measure))
            self.assertAlmostEqual(shape.BoundBox.ZMax,expected,places=5)

    def test_holes_curves_and_open_profile_errors(self):
        sketch=self.circle(5);sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False);self.doc.recompute()
        shape,_,_=extrusion.evaluate(self.owner,[(sketch,'')],{},self.options(length=3))
        self.assertAlmostEqual(shape.Volume,63*math.pi)
        shape,_,_=extrusion.evaluate(self.owner,[(sketch,'Edge2')],{},self.options(length=3))
        self.assertAlmostEqual(shape.Volume,12*math.pi)
        open_sketch=modeling.new_sketch(self.doc);open_sketch.addGeometry(Part.LineSegment(App.Vector(),App.Vector(4,0,0)),False);self.doc.recompute()
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'open'):self.make(open_sketch)
        self.assertEqual(self.snapshot(),before)

    def test_region_picker_keeps_holes_and_native_edge_references(self):
        sketch=self.circle(5);sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False);self.doc.recompute()
        ring=extrusion.region_references(self.owner,sketch,App.Vector(3,0,0))
        inner=extrusion.region_references(self.owner,sketch,App.Vector())
        self.assertEqual({sub for obj,sub in ring},{'Edge1','Edge2'})
        self.assertEqual(inner,[(sketch,'Edge2')])
        result,_,_=extrusion.evaluate(self.owner,ring,{},self.options(length=2))
        self.assertAlmostEqual(result.Volume,42*math.pi)

    def test_real_commands_and_in_place_accept(self):
        sketch=self.circle();Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch)
        before=self.snapshot();Gui.runCommand('PartDesign_Pad');QtTest.QTest.qWait(100)
        task=extrude_task._active;self.assertIsNotNone(task)
        self.assertEqual(task.refs,[(sketch,'')]);self.assertEqual(self.snapshot()[:2],before[:2])
        self.assertEqual(self.doc.UndoCount,before[-1])
        task.automatic.setChecked(False)
        task.end1['length'].setValue(9)
        self.assertTrue(task.accept())
        feature=task.result;identity=feature.ID
        self.assertAlmostEqual(feature.Shape.BoundBox.ZLength,9)
        task=editing.edit_feature(self.doc,feature)
        self.assertEqual(task.values[task.end1['length']],9)
        task.end1['length'].setValue(4)
        self.assertTrue(task.accept())
        self.assertEqual(feature.ID,identity);self.assertAlmostEqual(feature.Shape.BoundBox.ZLength,4)
        Gui.Selection.clearSelection();Gui.runCommand('PartDesign_Pocket');QtTest.QTest.qWait(100)
        task=extrude_task._active;self.assertEqual(task.mode(),'Subtract');self.assertFalse(task.valid)
        task.reject()

    def test_preview_result_does_not_change_visibility_or_undo(self):
        target=self.target();sketch=self.circle();sketch.Placement.Base.z=6;self.doc.recompute()
        Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch);Gui.Selection.addSelection(target)
        before=self.snapshot();task=extrude_task.show();QtTest.QTest.qWait(100)
        self.assertEqual(task.mode(),'Add');self.assertTrue(task.valid,task.status.text())
        task.modes['Subtract'].click();task.reverse.setChecked(True);task.end1['kind'].setCurrentText('Through all')
        task.display.setCurrentText('Result');QtTest.QTest.qWait(100)
        self.assertTrue(task.valid,task.status.text()+' scene='+repr([str(task.scene.getChild(i).getName()) for i in range(task.scene.getNumChildren())]))
        self.assertLess(task.result_shape.Volume,target.Shape.Volume)
        self.assertEqual(self.snapshot()[:2],before[:2]);self.assertEqual(self.doc.UndoCount,before[-1])
        task.reject();self.assertEqual(self.snapshot(),before)

    def test_task_cleanup_on_document_close(self):
        sketch=self.circle();Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch)
        task=extrude_task.show();App.closeDocument(self.doc.Name);QtTest.QTest.qWait(100)
        self.assertTrue(task.closed);self.assertIsNone(extrude_task._active)
        from freecad_plus import display
        self.assertFalse(display._task_hidden)

    def test_target_body_transform_and_native_pattern_polarity(self):
        target=self.target();body=target.getParentGeoFeatureGroup()
        body.Placement=App.Placement(App.Vector(20,3,0),App.Rotation(App.Vector(0,0,1),30))
        sketch=self.circle(1);sketch.Placement.Base=App.Vector(20,3,6);self.doc.recompute()
        feature=self.make(sketch,{'target':(target,'')},operation='Subtract',length=2,reverse=True)
        self.assertAlmostEqual(feature.Shape.Volume,target.Shape.Volume-2*math.pi)
        # Native consumers query the managed operation's polarity, not the
        # FeatureAddSubPython class's default additive value.
        pattern=body.newObject('PartDesign::LinearPattern','Pattern')
        pattern.Originals=[feature];pattern.Direction=(body.Origin.OriginFeatures[0],[''])
        pattern.Length=3;pattern.Occurrences=2
        self.doc.recompute()
        self.assertNotIn('Invalid',pattern.State)
        self.assertAlmostEqual(pattern.Shape.Volume,target.Shape.Volume-4*math.pi,places=5,
                               msg=repr([(o.Name,str(o.Placement),str(o.Shape.BoundBox)) for o in (body,target,feature,pattern)])+' tool='+str(feature.AddSubShape.BoundBox))

    def test_rejection_is_atomic(self):
        target=self.target();sketch=self.circle();sketch.Placement.Base=App.Vector(30,0,0);self.doc.recompute()
        before=self.snapshot()
        for opts in (dict(length=float('nan')),dict(length=-2),dict(operation='Subtract',length=2),dict(operation='Add',length=2)):
            with self.assertRaises(ValueError):self.make(sketch,{'target':(target,'')},**opts)
            self.assertEqual(self.snapshot(),before)

    def test_shared_task_prefill_blur_manual_and_cancel(self):
        sketch=self.circle();Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch)
        before=self.snapshot();task=extrude_task.show();QtTest.QTest.qWait(100)
        self.assertTrue(task.valid,task.status.text())
        self.assertTrue(all(isinstance(w,QtWidgets.QRadioButton) for w in task.modes.values()))
        field=task.end1['length'];field.setFocus();field.selectAll();revision=task.revisions
        QtTest.QTest.keyClicks(field,'12.5');QtTest.QTest.qWait(60)
        self.assertEqual(task.revisions,revision)
        task.refresh_button.setFocus();QtTest.QTest.qWait(100)
        self.assertEqual(task.values[field],12.5);self.assertEqual(task.revisions,revision+1)
        task.automatic.setChecked(False);field.setFocus();field.selectAll();QtTest.QTest.keyClicks(field,'7')
        task.profiles.setFocus();QtTest.QTest.qWait(60)
        self.assertEqual(task.revisions,revision+1)
        task.reject();self.assertEqual(self.snapshot(),before)
        feature=self.make(sketch,length=7,start='Offset',start_offset=2)
        before=self.snapshot();task=editing.edit_feature(self.doc,feature)
        self.assertEqual(task.values[task.end1['length']],7);self.assertEqual(task.values[task.start_offset],2)
        task.reject();self.assertEqual(self.snapshot(),before)

    def test_save_reopen_fixture_with_downstream(self):
        sketch=self.circle(5);feature=self.make(sketch,length=6)
        next_sketch=modeling.new_sketch(self.doc);next_sketch.Placement.Base.z=6
        next_sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False);self.doc.recompute()
        child=modeling.extrude(self.doc,next_sketch,3,operation='add',target=feature)
        self.make(sketch,feature=feature,length=7)
        self.assertTrue(child.Shape.isValid());self.assertNotIn('Invalid',child.State)
        document.save_document(self.doc,self.output/'Extrude.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'feature':feature.Name,'id':feature.ID,'child':child.Name,'sketch':sketch.Name}))

    def test_external_extrude_is_source_owned_and_persistent(self):
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        source=document.new_document('ExtrudeSource')
        definition=hierarchy.create_definition(source,'External extrusion')
        document.save_document(source,self.output/'Source.cadprt')
        external.import_file(self.doc,source);App.setActiveDocument(self.doc.Name)
        editing.edit_unused(self.doc,definition)
        sketch=self.circle();before=self.snapshot(source);assembly=self.snapshot()
        feature=self.make(sketch,length=7,start='Offset',start_offset=2)
        self.assertEqual(feature.Document,source);self.assertEqual(extrusion.owner(feature),definition)
        self.assertEqual(self.snapshot()[:-1],assembly[:-1])
        # Native cross-document transactions add a linked Undo record in the
        # assembly too, without changing its owned objects or hierarchy.
        self.assertEqual(self.doc.UndoCount,assembly[-1]+1)
        self.assertEqual(self.doc.UndoNames[0],'-> Extrude')
        self.assertEqual(source.UndoCount,before[-1]+1)
        name=feature.Name;identity=feature.ID
        source.undo();source.recompute();self.assertEqual(self.snapshot(source),before)
        source.redo();source.recompute();feature=source.getObject(name)
        task=editing.edit_feature(self.doc,feature)
        self.assertEqual(task.values[task.start_offset],2);task.reject()
        document.save_document(source);document.save_document(self.doc)
        (self.output/'expected.json').write_text(json.dumps({'feature':name,'id':identity,'definition':definition.Name}))

    def test_operation_rerouting_and_cycles_preserve_identity(self):
        target=self.target();sketch=self.circle();sketch.Placement.Base.z=6;self.doc.recompute()
        feature=self.make(sketch,{'target':(target,'')},operation='Add',length=3)
        identity=feature.ID;old_body=feature.getParentGeoFeatureGroup()
        self.make(sketch,feature=feature,length=3)
        self.assertEqual(feature.ID,identity);self.assertNotEqual(feature.getParentGeoFeatureGroup(),old_body)
        self.assertEqual(old_body.Tip,target);self.assertTrue(target.Visibility)
        self.assertAlmostEqual(feature.Shape.Volume,12*math.pi)
        self.make(sketch,{'target':(target,'')},feature,operation='Add',length=3)
        self.assertEqual(feature.ID,identity);self.assertEqual(feature.getParentGeoFeatureGroup(),old_body)
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'itself'):
            self.make(sketch,{'target':(feature,'')},feature,operation='Add',length=3)
        self.assertEqual(self.snapshot(),before)


def verify_fresh_process(output):
    folder=Path(output)/'test_save_reopen_fixture_with_downstream'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Extrude.cadprt')
    feature=doc.getObject(expected['feature']);sketch=doc.getObject(expected['sketch']);child=doc.getObject(expected['child'])
    assert extrusion.is_extrusion(feature) and feature.ID==expected['id']
    assert feature.Extrude_length==7 and feature.Shape.isValid()
    from freecad_plus import isolation
    definition=extrusion.owner(feature)
    occurrences=isolation.occurrences(doc,definition)
    if occurrences:editing.edit(occurrences[0])
    else:editing.edit_unused(doc,definition)
    task=editing.edit_feature(doc,feature)
    assert task.values[task.end1['length']]==7
    task.reject()
    top=next('Face'+str(i+1) for i,face in enumerate(feature.Shape.Faces)
             if isinstance(face.Surface,Part.Plane) and abs(face.CenterOfMass.z-7)<1e-7)
    plane=planes.save(doc,[(feature,top)])
    values=extrusion.settings(feature);values['length']=8
    extrusion.save(doc,planes.flatten(feature.ProfileReferences),extrusion.references(feature),values,feature)
    assert abs(plane.Placement.Base.z-8)<1e-7 and not plane.PlaneError
    sketch.setDatum(0,App.Units.Quantity('6 mm'));doc.recompute()
    assert feature.Shape.isValid() and child.Shape.isValid() and 'Invalid' not in child.State
    App.closeDocument(doc.Name)
    folder=Path(output)/'test_external_extrude_is_source_owned_and_persistent'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Assembly.cadprt')
    source=next(d for d in App.listDocuments().values() if d!=doc)
    feature=source.getObject(expected['feature']);definition=source.getObject(expected['definition'])
    assert feature.ID==expected['id'] and feature.Shape.isValid()
    assert abs(feature.Shape.BoundBox.ZMin-2)<1e-7 and abs(feature.Shape.BoundBox.ZMax-9)<1e-7
    editing.edit_unused(doc,definition)
    task=editing.edit_feature(doc,feature)
    assert task.values[task.start_offset]==2
    task.reject()
    App.closeDocument(doc.Name);App.closeDocument(source.Name)
