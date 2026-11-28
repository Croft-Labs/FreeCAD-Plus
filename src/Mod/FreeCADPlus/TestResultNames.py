# SPDX-License-Identifier: LGPL-2.1-or-later
import os,unittest
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui,Part
from PySide6 import QtCore,QtWidgets,QtTest
from freecad_plus import (document,editing,modeling,extrusion,extrude_task,planes,plane_task,
                         result_names,derived_geometry,clone_task,transforms,transform_task,
                         mesh_shape,mesh_task,trim_task,trim_body,sketch_task)


class TestResultNames(unittest.TestCase):
    def setUp(self):
        self.before=set(App.listDocuments());Gui.Selection.clearSelection()
        self.doc=document.new_document('ResultNames');self.owner=document.validate(self.doc).Definitions[0]
        self.owner.Label='Bracket';editing.edit((document.validate(self.doc).Group[0],))
        with document.transaction(self.doc,'Fixture'):
            self.box=self.owner.newObject('Part::Feature','Box');self.box.Shape=Part.makeBox(20,15,10)
            self.sketch=self.owner.newObject('Sketcher::SketchObject','Profile')
            self.sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False)

    def tearDown(self):
        from freecad_plus import operation_task
        if operation_task._active:operation_task._active.reject()
        for module in (extrude_task,plane_task,sketch_task,clone_task,transform_task,mesh_task,trim_task):
            task=getattr(module,'_active',None)
            if task:task.reject()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():Gui.activeDocument().resetEdit()
        if Gui.Control.activeDialog():Gui.Control.closeDialog()
        for name in set(App.listDocuments())-self.before:App.closeDocument(name)
        QtTest.QTest.qWait(60)

    def type_name(self,field,value):
        field.setFocus();field.selectAll();QtTest.QTest.keyClicks(field,value)

    def test_default_preview_matches_native_allocation(self):
        for seed in ('Extrude','Revolve','Loft','Thicken','Plane','Sketch'):
            for i in range(2):
                expected=result_names.defaults(self.owner,[seed])[0]
                obj=self.owner.newObject('Part::Feature',seed)
                self.assertEqual(expected,obj.Label)

    def test_extrude_name_undo_edit_cancel_and_save(self):
        task=extrude_task.ExtrudeTask();task.refs=[(self.sketch,'')];task.changed()
        self.type_name(task.names.field,'Mounting boss');undo=self.doc.UndoCount
        self.assertTrue(task.accept(),task.status.text());obj=task.result;name=obj.Name
        self.assertEqual(obj.Label,'Mounting boss');self.assertEqual(self.doc.UndoCount,undo+1)
        self.doc.undo();self.assertIsNone(self.doc.getObject(name));self.doc.redo();obj=self.doc.getObject(name)
        identity=obj.ID;volume=obj.Shape.Volume
        task=extrude_task.ExtrudeTask(obj);self.assertEqual(task.names.value(),'Mounting boss')
        self.type_name(task.names.field,'Discard');task.reject();self.assertEqual(obj.Label,'Mounting boss')
        task=extrude_task.ExtrudeTask(obj);self.type_name(task.names.field,'Final boss');self.assertTrue(task.accept())
        self.assertEqual(obj.ID,identity);self.assertAlmostEqual(obj.Shape.Volume,volume)
        file=Path(os.environ['PLUS_TEST_DIR'])/'named.cadprt';document.save_document(self.doc,file)
        App.closeDocument(self.doc.Name);self.doc=document.open_document(file)
        self.assertEqual(self.doc.getObject(name).Label,'Final boss')

    def test_blank_name_rejects_without_transaction(self):
        task=extrude_task.ExtrudeTask();task.refs=[(self.sketch,'')];task.changed();task.names.field.clear()
        state=(len(self.doc.Objects),self.doc.UndoCount)
        self.assertFalse(task.accept());self.assertIn('result name',task.status.text())
        self.assertEqual(state,(len(self.doc.Objects),self.doc.UndoCount));task.reject()

    def test_mesh_prefix_sequence_and_custom_edit(self):
        settings=dict(method=0,parameters=dict(LinearDeflection=.1,AngularDeflection=.5,Relative=False))
        a=mesh_shape.save(self.doc,[(self.box,'')],settings)
        b=mesh_shape.save(self.doc,[(self.box,'')],settings)
        self.assertEqual([a.Label,b.Label],['Bracket_Mesh001','Bracket_Mesh002'])
        mesh_shape.save(self.doc,[(self.box,'')],settings,a,result_name='Export mesh')
        self.assertEqual(a.Label,'Export mesh');self.assertEqual(b.Label,'Bracket_Mesh002')

    def test_plane_and_sketch_name_fields(self):
        for cls,seed in ((plane_task.PlaneTask,'Plane'),(sketch_task.SketchPlacementTask,'Sketch')):
            task=cls();self.assertEqual(task.names.value(),result_names.defaults(self.owner,[seed])[0]);task.reject()
        support=self.owner.Origin.OriginFeatures[3]
        refs=[(next(o for o in self.owner.Origin.OriginFeatures if o.Name.startswith('XY_Plane')),'')]
        obj=planes.save(self.doc,refs,result_name='Work plane');identity=obj.ID
        planes.save(self.doc,refs,feature=obj,result_name='Offset plane')
        self.assertEqual(obj.Label,'Offset plane');self.assertEqual(obj.ID,identity)

    def test_multi_extract_names_follow_sources(self):
        task=clone_task.GeometryTask(True);task.form.join.setChecked(False)
        task.refs=[(self.box,'Face1'),(self.box,'Face2')];task.fields()
        self.assertEqual(task.names.values(),['extracted surface','extracted surface (2)'])
        self.type_name(task.names.fields[task.names.keys[1]],'Side wall')
        task.refs.reverse();task.fields();self.assertEqual(task.names.values()[0],'Side wall')
        undo=self.doc.UndoCount;self.assertTrue(task.accept(),task.form.status.text())
        self.assertEqual(task.results[0].Label,'Side wall');self.assertEqual(self.doc.UndoCount,undo+1)

    def test_transform_per_result_labels_and_apply_reset(self):
        task=transform_task.show('Linear pattern');task.refs=[(self.box,'')]
        task.form.merge.setChecked(False);task.form.steps[0].count.setValue(3);task.refresh()
        self.assertEqual(len(task.names.keys),3)
        for i,key in enumerate(task.names.keys):self.type_name(task.names.fields[key],'Copy '+str(i+1))
        task.refresh();self.assertEqual(task.names.values(),['Copy 1','Copy 2','Copy 3'])
        self.assertTrue(task.apply(),task.form.status.text());objects=task.results
        self.assertEqual([o.Label for o in objects],['Copy 1','Copy 2','Copy 3']);self.assertEqual(len(task.names.keys),1)
        task.reject();task=transform_task.show('Linear pattern',objects[0]);task.refresh()
        self.assertEqual(task.names.values(),['Copy 1','Copy 2','Copy 3']);task.reject()

    def test_trim_name_is_atomic_and_resets(self):
        task=trim_task.show();task.target=(self.box,'');task.form.mode.setCurrentIndex(1);task.form.offset.setValue(5)
        self.type_name(task.names.field,'Trimmed bracket');undo=self.doc.UndoCount
        self.assertTrue(task.apply(),task.form.status.text());self.assertEqual(task.result.Label,'Trimmed bracket')
        self.assertEqual(self.doc.UndoCount,undo+1);self.assertNotEqual(task.names.value(),'Trimmed bracket');task.reject()

    def test_native_fillet_field_accept_and_cancel(self):
        self.sketch.delGeometry(0)
        points=[App.Vector(0,0,0),App.Vector(20,0,0),App.Vector(20,15,0),App.Vector(0,15,0)]
        for i in range(4):self.sketch.addGeometry(Part.LineSegment(points[i],points[(i+1)%4]),False)
        self.doc.recompute()
        obj=extrusion.save(self.doc,[(self.sketch,'')],{},dict(extrusion.DEFAULTS,length=10))
        Gui.Selection.addSelection(obj,'Edge1');Gui.runCommand('PartDesign_Fillet');QtTest.QTest.qWait(160)
        dock=Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks')
        fields=dock.findChildren(QtWidgets.QLineEdit,'PlusResultName');self.assertEqual(len(fields),1)
        feature=Gui.activeDocument().getInEdit().Object;original=feature.Label
        self.type_name(fields[0],'Rounded boss');self.assertEqual(feature.Label,original)
        from TestComponentModeling import accept_task
        accept_task();self.assertEqual(feature.Label,'Rounded boss')
        Gui.activeDocument().setEdit(feature.Name);QtTest.QTest.qWait(160)
        field=dock.findChild(QtWidgets.QLineEdit,'PlusResultName');self.assertEqual(field.text(),'Rounded boss')
        self.type_name(field,'Discarded')
        box=next(b for b in dock.findChildren(QtWidgets.QDialogButtonBox) if b.isVisible() and b.button(QtWidgets.QDialogButtonBox.Cancel))
        box.button(QtWidgets.QDialogButtonBox.Cancel).click();QtTest.QTest.qWait(50)
        self.assertEqual(feature.Label,'Rounded boss')

    def test_native_immediate_boolean_review_and_undo(self):
        from freecad_plus import operation_task
        with document.transaction(self.doc,'Tool'):
            tool=self.owner.newObject('Part::Feature','Tool');tool.Shape=Part.makeBox(10,10,10,App.Vector(10,0,0))
        count=len(self.doc.Objects);undo=self.doc.UndoCount
        Gui.Selection.addSelection(self.box);Gui.Selection.addSelection(tool)
        Gui.runCommand('Part_Cut');QtTest.QTest.qWait(80)
        task=operation_task._active;self.assertIsNotNone(task)
        self.assertEqual(len(self.doc.Objects),count);self.assertEqual(task.names.value(),'Cut')
        self.type_name(task.names.field,'Pocketed bracket');self.assertTrue(task.accept())
        result=task.results[0];name=result.Name
        self.assertEqual(result.Label,'Pocketed bracket');self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertEqual(result.Base,self.box);self.assertEqual(result.Tool,tool)
        self.doc.undo();self.assertIsNone(self.doc.getObject(name));self.doc.redo()
        self.assertEqual(self.doc.getObject(name).Label,'Pocketed bracket')

    def test_native_boolean_dialog_names(self):
        tool=self.owner.newObject('Part::Feature','Tool');tool.Shape=Part.makeBox(10,10,10,App.Vector(10,0,0));self.doc.recompute()
        Gui.runCommand('Part_Boolean');QtTest.QTest.qWait(180)
        dock=Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks')
        field=dock.findChild(QtWidgets.QLineEdit,'PlusResultName');self.assertIsNotNone(field)
        self.assertEqual(field.text(),'Fusion')
        diff=dock.findChild(QtWidgets.QRadioButton,'diffButton');diff.setChecked(True)
        self.assertEqual(field.text(),'Cut');self.type_name(field,'Custom cut')
        dock.findChild(QtWidgets.QRadioButton,'unionButton').setChecked(True)
        self.assertEqual(field.text(),'Custom cut')
        for tree_name,obj in (('firstShape',self.box),('secondShape',tool)):
            tree=dock.findChild(QtWidgets.QTreeWidget,tree_name)
            iterator=QtWidgets.QTreeWidgetItemIterator(tree)
            while iterator.value():
                item=iterator.value()
                if item.data(0,QtCore.Qt.UserRole)==obj.Name:item.setCheckState(0,QtCore.Qt.Checked)
                iterator+=1
        undo=self.doc.UndoCount;ids={o.ID for o in self.doc.Objects}
        buttons=next(b for b in dock.findChildren(QtWidgets.QDialogButtonBox) if b.isVisible() and b.button(QtWidgets.QDialogButtonBox.Apply))
        buttons.button(QtWidgets.QDialogButtonBox.Apply).click();QtTest.QTest.qWait(70)
        result=next(o for o in self.doc.Objects if o.ID not in ids)
        self.assertEqual(result.Label,'Custom cut');self.assertTrue(result.Shape.isValid())
        self.assertEqual(self.doc.UndoCount,undo+1);self.assertEqual(field.text(),'Fusion001')
        Gui.Control.closeDialog()

    def test_native_primitive_name_create_and_reset(self):
        Gui.runCommand('Part_Primitives');QtTest.QTest.qWait(180)
        dock=Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks')
        combo=dock.findChild(QtWidgets.QComboBox,'PrimitiveTypeCB');self.assertIsNotNone(combo)
        combo.setCurrentIndex(1)
        field=dock.findChild(QtWidgets.QLineEdit,'PlusResultName');self.assertIsNotNone(field)
        self.assertEqual(field.text(),'Box001');self.type_name(field,'Base block')
        ids={o.ID for o in self.doc.Objects};undo=self.doc.UndoCount
        buttons=next(b for b in dock.findChildren(QtWidgets.QDialogButtonBox) if b.isVisible() and b.button(QtWidgets.QDialogButtonBox.Ok))
        buttons.button(QtWidgets.QDialogButtonBox.Ok).click();QtTest.QTest.qWait(80)
        result=next(o for o in self.doc.Objects if o.ID not in ids)
        self.assertEqual(result.Label,'Base block');self.assertTrue(result.Shape.isValid())
        self.assertIn(result,document.history(self.doc,self.owner));self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertEqual(field.text(),'Box002');Gui.Control.closeDialog()

    def test_datum_native_name_cancel(self):
        Gui.runCommand('FreeCADPlus_DatumPoint');QtTest.QTest.qWait(160)
        dock=Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks')
        field=dock.findChild(QtWidgets.QLineEdit,'PlusResultName');self.assertIsNotNone(field)
        self.assertTrue(field.text().startswith('DatumPoint'))
        feature=Gui.activeDocument().getInEdit().Object;name=feature.Name
        self.type_name(field,'Datum custom')
        box=next(b for b in dock.findChildren(QtWidgets.QDialogButtonBox) if b.isVisible() and b.button(QtWidgets.QDialogButtonBox.Cancel))
        box.button(QtWidgets.QDialogButtonBox.Cancel).click();QtTest.QTest.qWait(60)
        self.assertIsNone(self.doc.getObject(name))

    def test_immediate_commands_preserve_native_features(self):
        from freecad_plus import operation_task
        with document.transaction(self.doc,'Tools'):
            tool=self.owner.newObject('Part::Feature','Tool');tool.Shape=Part.makeBox(15,15,10,App.Vector(10,0,0))
            plane=self.owner.newObject('Part::Feature','ToolPlane');plane.Shape=Part.makePlane(50,50,App.Vector(-10,-10,5))
            compound=self.owner.newObject('Part::Compound','InputCompound');compound.Links=[self.box,tool]
        cases=[('Part_Fuse',[self.box,tool]),('Part_Common',[self.box,tool]),('Part_Compound',[self.box,tool]),
               ('Part_JoinConnect',[self.box,tool]),('Part_BooleanFragments',[self.box,tool]),
               ('Part_XOR',[self.box,tool]),('Part_Slice',[self.box,plane]),('Part_SliceApart',[self.box,plane]),
               ('Part_ExplodeCompound',[compound])]
        for index,(command,inputs) in enumerate(cases):
            with self.subTest(command=command):
                Gui.Selection.clearSelection()
                for obj in inputs:Gui.Selection.addSelection(obj)
                undo=self.doc.UndoCount;Gui.runCommand(command);QtTest.QTest.qWait(40)
                task=operation_task._active;self.assertIsNotNone(task)
                names=['Result '+str(index)+' '+str(i) for i in range(len(task.names.keys))]
                for key,label in zip(task.names.keys,names):self.type_name(task.names.fields[key],label)
                accepted=task.accept()
                self.assertTrue(accepted,task.status.text() if not accepted else '')
                self.assertEqual([o.Label for o in task.results],names)
                self.assertEqual(self.doc.UndoCount,undo+1);document.validate(self.doc)
