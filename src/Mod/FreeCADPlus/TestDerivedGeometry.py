# SPDX-License-Identifier: LGPL-2.1-or-later
import os, unittest
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, Part, Sketcher
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, hierarchy, editing, panel, display, derived_geometry as derived

class TestDerivedGeometry(unittest.TestCase):
    def setUp(self):
        self.before=set(App.listDocuments()); self.out=Path(os.environ['PLUS_TEST_DIR'])/self._testMethodName
        self.out.mkdir(exist_ok=True); Gui.Selection.clearSelection()
        self.doc=document.new_document('Derived'); self.root=document.validate(self.doc)
        self.owner=self.root.Definitions[0]; self.owner.Label='Assembly'
        self.child=hierarchy.create_definition(self.doc,'Child')
        self.link=hierarchy.add_instance(self.owner,self.child,App.Placement(App.Vector(40,10,5),App.Rotation(App.Vector(0,0,1),90)))
        with document.transaction(self.doc,'Source geometry'):
            self.body=self.child.newObject('PartDesign::Body','SourceBody')
            self.base=self.body.newObject('PartDesign::Feature','SourceSolid'); self.base.Shape=Part.makeBox(10,8,6)
            self.body.Placement.Base=App.Vector(3,4,5)
            self.sketch=self.child.newObject('Sketcher::SketchObject','SourceSketch')
            self.sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False)
            self.sketch.addConstraint(Sketcher.Constraint('Radius',0,3))
            self.sketch.Placement.Base=App.Vector(0,0,7)
            self.sheet=self.child.newObject('Part::Feature','SourceSheet'); self.sheet.Shape=Part.makePlane(15,12)
            self.plane=self.body.newObject('PartDesign::Plane','SourcePlane')
        self.top=self.root.Group[0]; editing.edit((self.top,))
        self.dock=panel.show_panel(); QtTest.QTest.qWait(80); self.dock.activate_assembly(self.owner,(self.top,))

    def tearDown(self):
        import sys
        task=sys.modules.get('freecad_plus.clone_task')
        if task and task._active: task._active.reject()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments())-self.before: App.closeDocument(name)
        QtTest.QTest.qWait(80)

    def ref(self,obj,link=None):
        link=link or self.link
        return link, ''.join(o.Name+'.' for o in document.owned_path(link.LinkedObject,obj))

    def test_whole_body_surface_sketch_plane(self):
        refs=[self.ref(o) for o in (self.body,self.sheet,self.sketch,self.plane)]
        before={o.Name:o.ID for o in self.doc.Objects}; undo=self.doc.UndoCount
        results=derived.save(self.doc,refs)
        self.assertEqual([o.Label for o in results],['cloned body','cloned surface','cloned sketch','cloned plane'])
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertEqual(results[0].TypeId,'PartDesign::FeaturePython')
        self.assertEqual(results[2].TypeId,'Sketcher::SketchObjectPython')
        self.assertEqual(results[2].ConstraintCount,0)
        self.assertEqual(results[2].GeometryCount,1)
        for result,ref in zip(results,refs):
            expected=Part.getShape(*ref,needSubElement=True)
            self.assertTrue(result.Shape.BoundBox.Center.isEqual(expected.BoundBox.Center,1e-6),(result.Label,result.Shape.BoundBox,expected.BoundBox))
            self.assertTrue(result.Shape.isValid())
        self.assertEqual(self.sketch.ConstraintCount,1)
        self.assertEqual(editing.context_path(self.doc),(self.owner,(self.top,)))
        self.doc.undo(); self.doc.recompute(); self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        self.doc.redo(); document.validate(self.doc)
        document.save_document(self.doc,self.out/'FourTypes.cadprt')

    def snapshot(self):
        return self.doc.UndoCount,[(o.Name,o.ID,str(getattr(o,'Placement',''))) for o in self.doc.Objects]

    def test_direct_child_whole_object_boundary(self):
        grand=hierarchy.create_definition(self.doc,'Grandchild')
        nested=hierarchy.add_instance(self.child,grand)
        box=grand.newObject('Part::Box','GrandBox');self.doc.recompute()
        bad=[(self.link,''),(self.link,self.ref(self.body)[1]+'Face1'),
             (self.link,self.ref(self.body)[1]+'Edge1'),
             (self.link,nested.Name+'.'+box.Name+'.'),(self.base,'')]
        before=self.snapshot()
        for ref in bad:
            with self.assertRaises(ValueError):derived.save(self.doc,[ref])
        self.assertEqual(self.snapshot(),before)
        display.set_state(self.owner,self.link,part_type='Reference')
        result=derived.save(self.doc,[self.ref(self.body)])[0]
        display.set_state(self.owner,self.link,part_type='Excluded')
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'Excluded'):derived.save(self.doc,[self.ref(self.sheet)])
        self.assertEqual(self.snapshot(),before)
        result.touch();self.doc.recompute();self.assertFalse(result.GeometryError)
        with self.assertRaisesRegex(ValueError,'parent-owned'):
            derived.save(self.doc,[(self.link,self.ref(self.body)[1]+'Face1')],'Extract')

    def test_instances_updates_extract_and_edit(self):
        second=hierarchy.add_instance(self.owner,self.child,App.Placement(App.Vector(100,0,0),App.Rotation()))
        clones=derived.save(self.doc,[self.ref(self.body),self.ref(self.body,second)])
        self.assertNotEqual(clones[0].Shape.BoundBox.Center,clones[1].Shape.BoundBox.Center)
        self.assertEqual(clones[0].SourceObject,clones[1].SourceObject)
        surfaces=derived.save(self.doc,[(clones[0],'Face1'),(clones[0],'Face2')],'Extract')
        self.assertEqual([o.Label for o in surfaces],['extracted surface','extracted surface (2)'])
        before=clones[0].Shape.BoundBox.Center
        with document.transaction(self.doc,'Move source'):
            self.link.Placement.Base+=App.Vector(0,20,0)
            self.base.Shape=Part.makeBox(12,8,6)
        self.assertAlmostEqual(clones[0].Shape.Volume,576)
        self.assertAlmostEqual(clones[1].Shape.Volume,576)
        self.assertAlmostEqual(clones[0].Shape.BoundBox.Center.y-before.y,21)
        self.assertTrue(surfaces[0].Shape.BoundBox.Center.isEqual(clones[0].Shape.Faces[0].BoundBox.Center,1e-6))
        identities=[o.ID for o in clones+surfaces]
        derived.save(self.doc,[self.ref(self.body,second)],feature=clones[0])
        self.assertEqual([o.ID for o in clones+surfaces],identities)
        self.assertTrue(clones[0].Shape.isSame(clones[1].Shape) or clones[0].Shape.BoundBox.Center.isEqual(clones[1].Shape.BoundBox.Center,1e-6))
        with self.assertRaisesRegex(ValueError,'another body'):
            derived.save(self.doc,[self.ref(self.sheet)],feature=clones[0])
        with self.assertRaisesRegex(ValueError,'downstream'):
            derived.save(self.doc,[(surfaces[0],'Face1')],'Extract',surfaces[0])
        document.save_document(self.doc,self.out/'Derived.cadprt')

    def test_native_features_and_dumb_sketch(self):
        from freecad_plus import modeling
        sketch=derived.save(self.doc,[self.ref(self.sketch)])[0]
        self.assertEqual(modeling.extrusion_request()['profiles'],[sketch])
        Gui.Selection.addSelection(sketch)
        self.assertEqual(modeling.extrusion_request()['profiles'],[sketch])
        Gui.Selection.clearSelection()
        pad=modeling.extrude(self.doc,sketch,9)
        self.assertAlmostEqual(pad.Shape.Volume,3.141592653589793*9*9,places=5)
        with document.transaction(self.doc,'Change child sketch'):self.sketch.setDatum(0,App.Units.Quantity('4 mm'))
        self.assertEqual(sketch.ConstraintCount,0)
        self.assertAlmostEqual(pad.Shape.Volume,3.141592653589793*16*9,places=5)
        cloned=derived.save(self.doc,[self.ref(self.body)])[0]
        with document.transaction(self.doc,'Parent fillet'):
            fillet=cloned.getParentGeoFeatureGroup().newObject('PartDesign::Fillet','Fillet')
            fillet.Base=(cloned,['Edge1']);fillet.Radius=.5
        self.assertTrue(fillet.Shape.isValid());self.assertFalse(fillet.Shape.isNull())
        self.assertLess(fillet.Shape.Volume,cloned.Shape.Volume)
        self.assertEqual(len(self.body.Group),len([self.base,self.plane]))
        self.assertAlmostEqual(self.base.Shape.Volume,480)
        document.validate(self.doc)
        document.save_document(self.doc,self.out/'NativeFeatures.cadprt')

    def test_missing_source_repair_and_schema_undo(self):
        self.root.PlusSchema=7
        result=derived.save(self.doc,[self.ref(self.sheet)])[0];name=result.Name
        self.assertEqual(self.root.PlusSchema,8)
        self.doc.undo();self.assertEqual(self.root.PlusSchema,7)
        self.doc.redo();result=self.doc.getObject(name)
        old_name=self.sheet.Name
        with document.transaction(self.doc,'Remove original source'):
            self.doc.removeObject(old_name)
            other=self.child.newObject('Part::Feature',old_name);other.Shape=Part.makePlane(30,12)
        self.assertTrue(result.GeometryError);self.assertTrue(result.Shape.isNull())
        document.validate(self.doc)
        derived.save(self.doc,[self.ref(other)],feature=result)
        self.assertFalse(result.GeometryError);self.assertAlmostEqual(result.Shape.Area,360)
        extracted=derived.save(self.doc,[(result,'Face1')],'Extract')[0]
        with document.transaction(self.doc,'Lose extracted face'):
            extracted.Source=(result,['Face999'])
        self.assertTrue(extracted.GeometryError);self.assertTrue(extracted.Shape.isNull())
        derived.save(self.doc,[(result,'Face1')],'Extract',extracted)
        self.assertFalse(extracted.GeometryError)

    def test_task_preview_selection_cancel_and_history_edit(self):
        from freecad_plus import clone_task, selection_list
        before=self.snapshot();task=clone_task.show()
        task.pick(self.owner,self.link.Name+'.'+self.ref(self.body)[1]);QtTest.QTest.qWait(80)
        self.assertFalse(task.form.status.error,task.form.status.text());self.assertIsNotNone(task.overlay)
        self.assertTrue(selection_list.feature_picker_active());self.assertEqual(self.snapshot(),before)
        task.form.grab().save(str(self.out/'clone-create.png'))
        task.pick(self.owner,self.link.Name+'.'+self.ref(self.body)[1],True)
        self.assertEqual(task.refs,[])
        task.pick(self.link,self.ref(self.body)[1]);task.form.objects.topLevelItem(0).setSelected(True)
        QtTest.QTest.keyClick(task.form.objects,QtCore.Qt.Key_Delete);self.assertEqual(task.refs,[])
        task.pick(self.link,self.ref(self.body)[1]);task.form.update.setChecked(False)
        self.assertIsNone(task.overlay);self.assertEqual(self.snapshot(),before);task.reject()
        self.assertEqual(self.snapshot(),before)
        task=clone_task.show();task.pick(self.link,self.ref(self.body)[1]);accepted=task.accept()
        self.assertTrue(accepted,task.form.status.text() if not accepted else '')
        result=task.results[0];task=editing.edit_feature(self.doc,result)
        QtTest.QTest.qWait(80);task.form.grab().save(str(self.out/'clone-edit.png'))
        before=self.snapshot();task.reject();self.assertEqual(self.snapshot(),before)
        task=clone_task.show(extract=True);task.pick(result,'Face1');QtTest.QTest.qWait(80)
        self.assertFalse(task.form.status.error,task.form.status.text())
        task.form.grab().save(str(self.out/'extract-create.png'))
        accepted=task.accept();self.assertTrue(accepted,task.form.status.text() if not accepted else '')
        extracted=task.results[0];task=editing.edit_feature(self.doc,extracted)
        self.assertTrue(task.extract);QtTest.QTest.qWait(80)
        task.form.grab().save(str(self.out/'extract-edit.png'));task.reject()

    def test_browser_exact_occurrence_and_no_grandchildren(self):
        from freecad_plus import clone_task
        second=hierarchy.add_instance(self.owner,self.child)
        grand=hierarchy.create_definition(self.doc,'Deep part');nested=hierarchy.add_instance(self.child,grand)
        grand.newObject('Part::Box','ForbiddenGrandBox');self.doc.recompute()
        task=clone_task.show();errors=[]
        def choose():
            try:
                dialog=QtWidgets.QApplication.activeModalWidget();tree=dialog.findChild(QtWidgets.QTreeWidget)
                it=QtWidgets.QTreeWidgetItemIterator(tree);found=[]
                while it.value():
                    item=it.value();data=item.data(0,QtCore.Qt.UserRole)
                    self.assertNotIn('ForbiddenGrandBox',item.text(0))
                    if data and data[0]==panel.identity(second) and data[1]==self.ref(self.body)[1]:
                        item.setCheckState(0,QtCore.Qt.Checked);found.append(item)
                    it+=1
                self.assertEqual(len(found),1)
                dialog.grab().save(str(self.out/'direct-child-browser.png'))
                dialog.findChild(QtWidgets.QDialogButtonBox).button(QtWidgets.QDialogButtonBox.Ok).click()
            except BaseException as error:errors.append(error);QtWidgets.QApplication.activeModalWidget().reject()
        QtCore.QTimer.singleShot(100,choose);task.browse()
        if errors:raise errors[0]
        self.assertEqual(task.refs,[self.ref(self.body,second)]);task.reject()

    def test_external_sources_export_and_raw_foreign_guard(self):
        from freecad_plus import external, part_transfer_ops, geometry
        document.save_document(self.doc,self.out/'Host.cadprt')
        lib=document.new_document('Library');part=document.validate(lib).Definitions[0];part.Label='External part'
        box=part.newObject('Part::Box','Box');box.Length=15;lib.recompute()
        document.save_document(lib,self.out/'Library.cadprt');undo=lib.UndoCount
        App.setActiveDocument(self.doc.Name);QtTest.QTest.qWait(80)
        link=hierarchy.add_children(self.owner,[part])[0]
        result=derived.save(self.doc,[self.ref(box,link)])[0]
        self.assertEqual(lib.UndoCount,undo);self.assertEqual(result.SourceObject,box)
        document.validate(self.doc)
        with self.assertRaises(ValueError):geometry.require_modeling_inputs(self.owner,[(box,'')])
        document.save_document(self.doc)
        path=self.out/'Exported.cadprt';part_transfer_ops.export_parts([self.owner],path)
        exported=document.open_document(path)
        copies=[o for o in exported.Objects if derived.is_derived(o)]
        self.assertEqual(len(copies),1);copy=copies[0]
        self.assertEqual(copy.SourceObject.Document,exported)
        self.assertEqual(derived.saved_ref(copy)[0].Document,exported)
        self.assertAlmostEqual(copy.Shape.Volume,1500)
        copy.SourceObject.Length=20;exported.recompute();self.assertAlmostEqual(copy.Shape.Volume,2000)
        self.assertAlmostEqual(box.Length.Value,15);document.validate(exported)

    def test_native_boolean_and_body_coordinate_frame(self):
        result=derived.save(self.doc,[self.ref(self.body)])[0]
        with document.transaction(self.doc,'Parent body Boolean'):
            parent=self.owner.newObject('PartDesign::Body','ParentBody')
            parent.Placement.Base=App.Vector(0,0,2)
            base=parent.newObject('PartDesign::Feature','ParentBase');base.Shape=Part.makeBox(100,100,30)
            boolean=parent.newObject('PartDesign::Boolean','Cut');boolean.Type=1
            tool=result.getParentGeoFeatureGroup();self.owner.removeObject(tool)
            boolean.Group=[tool]
        self.assertTrue(boolean.Shape.isValid());self.assertAlmostEqual(boolean.Shape.Volume,300000-480)
        self.assertAlmostEqual(self.base.Shape.Volume,480)
        self.base.Shape=Part.makeBox(12,8,6);self.doc.recompute()
        self.assertAlmostEqual(boolean.Shape.Volume,300000-576)
        document.validate(self.doc)
        sketch=derived.save(self.doc,[self.ref(self.sketch)])[0]
        with document.transaction(self.doc,'Consume sketch in moved body'):
            body=self.owner.newObject('PartDesign::Body','MovedBody');body.Placement.Base=App.Vector(0,0,20)
            self.owner.removeObject(sketch);body.addObject(sketch)
            self.sketch.setDatum(0,App.Units.Quantity('4 mm'))
        expected=Part.getShape(*self.ref(self.sketch),needSubElement=True)
        actual=Part.getShape(self.owner,''.join(o.Name+'.' for o in document.owned_path(self.owner,sketch)),needSubElement=True)
        self.assertTrue(actual.BoundBox.Center.isEqual(expected.BoundBox.Center,1e-6),(actual.BoundBox,expected.BoundBox))

    def test_origin_plane_and_multiple_whole_surfaces(self):
        origin=next(o for o in self.child.Origin.OriginFeatures if o.TypeId=='App::Plane')
        self.sheet.Shape=Part.makeCompound([Part.makePlane(10,5),Part.makePlane(4,3,App.Vector(0,0,3))]);self.doc.recompute()
        results=derived.save(self.doc,[self.ref(origin),self.ref(self.sheet)])
        self.assertEqual(results[0].Label,'cloned plane')
        self.assertEqual(len(results[1].Shape.Faces),2)
        self.assertAlmostEqual(results[1].Shape.Area,62)

    def test_real_commands_unresolved_picks_and_stale_task(self):
        from freecad_plus import clone_task, selection_list
        Gui.activateWorkbench('PartDesignWorkbench')
        display.set_state(self.owner,self.link,part_type='Reference');self.dock.refresh()
        from freecad_plus import toolbars
        ribbon=toolbars._controller
        ribbon.tabbar.setCurrentIndex(next(i for i in range(ribbon.tabbar.count()) if ribbon.tabbar.tabText(i)=='Modeling'))
        QtTest.QTest.qWait(100)
        clone_button=Gui.getMainWindow().findChild(QtWidgets.QToolButton,'Plus_Plus_Clone')
        self.assertIsNotNone(clone_button);self.assertTrue(clone_button.isEnabled());self.assertTrue(clone_button.isVisible())
        Gui.Selection.clearSelection();clone_button.click();QtTest.QTest.qWait(60)
        task=clone_task._active;self.assertIsNotNone(task)
        sub=hierarchy.subname((self.top,self.link))+self.ref(self.body)[1]
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,sub);QtTest.QTest.qWait(100)
        self.assertEqual(task.refs,[self.ref(self.body)])
        with selection_list.pick_intent(True):Gui.Selection.addSelection(self.doc.Name,self.root.Name,sub)
        QtTest.QTest.qWait(100);self.assertEqual(task.refs,[])
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,sub+'Face1');QtTest.QTest.qWait(100)
        self.assertEqual(task.refs,[]);self.assertTrue(task.form.status.error)
        task.pick(self.link,self.ref(self.body)[1]);before=self.snapshot()
        editing.edit((self.top,self.link));QtTest.QTest.qWait(80)
        self.assertFalse(task.accept());self.assertEqual(self.snapshot(),before);task.reject()
        editing.edit((self.top,));Gui.Selection.clearSelection();Gui.runCommand('Plus_ExtractGeometry')
        task=clone_task._active;self.assertTrue(task.extract);task.reject()
        from freecad_plus import toolbar_layout
        text=repr(toolbar_layout.__dict__)
        self.assertIn('Plus_Clone',text);self.assertIn('Plus_ExtractGeometry',text)
        self.dock.refresh();Gui.getMainWindow().findChild(QtWidgets.QWidget,'PlusGroup_Other').grab().save(str(self.out/'modeling-commands.png'))

    def test_external_parent_owns_results_and_cancel_is_clean(self):
        from freecad_plus import clone_task
        source=document.new_document('Subsystem');owner=document.validate(source).Definitions[0];owner.Label='External assembly'
        child=hierarchy.create_definition(source,'External child');box=child.newObject('Part::Box','Box')
        link=hierarchy.add_instance(owner,child);source.recompute()
        document.save_document(source,self.out/'Subsystem.cadprt')
        document.save_document(self.doc,self.out/'Host.cadprt')
        App.setActiveDocument(self.doc.Name);QtTest.QTest.qWait(80)
        instances=[hierarchy.add_children(self.owner,[owner])[0],hierarchy.add_children(self.owner,[owner])[0]]
        editing.edit((self.top,instances[0]))
        ids={o.Name:o.ID for o in self.doc.Objects};undo=source.UndoCount;count=len(source.Objects)
        task=clone_task.show();task.pick(link,box.Name+'.');task.reject()
        self.assertEqual(source.UndoCount,undo);self.assertEqual(len(source.Objects),count)
        task=clone_task.show();task.pick(link,box.Name+'.');accepted=task.accept()
        self.assertTrue(accepted,task.form.status.text() if not accepted else '')
        result=task.results[0];self.assertEqual(result.Document,source);self.assertEqual(derived.owner(result),owner)
        self.assertEqual(source.UndoCount,undo+1);self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        self.assertEqual(instances[0].LinkedObject,instances[1].LinkedObject)
        name=result.Name;source.undo();self.assertIsNone(source.getObject(name));source.redo();source.recompute()
        document.save_document(source);document.save_document(self.doc)

    def test_archive_rejects_unrelated_external_geometry(self):
        import zipfile,xml.etree.ElementTree as ET
        from freecad_plus import external
        document.save_document(self.doc,self.out/'Host.cadprt')
        lib=document.new_document('Library');part=document.validate(lib).Definitions[0];part.Label='External part'
        box=part.newObject('Part::Box','Box');other=part.newObject('Part::Box','OtherBox');lib.recompute()
        document.save_document(lib,self.out/'Library.cadprt')
        App.setActiveDocument(self.doc.Name);QtTest.QTest.qWait(60)
        link=hierarchy.add_children(self.owner,[part])[0];result=derived.save(self.doc,[self.ref(box,link)])[0]
        document.save_document(self.doc)
        with zipfile.ZipFile(self.doc.FileName) as z:entries={n:z.read(n) for n in z.namelist()}
        tree=ET.fromstring(entries['Document.xml'])
        node=tree.find("./ObjectData/Object[@name='"+result.Name+"']/Properties/Property[@name='SourceObject']/XLink")
        node.set('name',other.Name);entries['Document.xml']=ET.tostring(tree)
        path=self.out/'Tampered.cadprt'
        with zipfile.ZipFile(path,'w') as z:
            for name,data in entries.items():z.writestr(name,data)
        with self.assertRaisesRegex(ValueError,'unsupported external'):external.archive_graph(path)
