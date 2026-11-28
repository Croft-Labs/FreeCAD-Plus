# SPDX-License-Identifier: LGPL-2.1-or-later
import json,math,os,unittest
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui,Part
from PySide6 import QtWidgets,QtTest
from freecad_plus import document,editing,mesh_task,mesh_ui,mesh_shape,transforms,transform_task,trim_body,trim_task,hierarchy,derived_geometry,appearance


class TestMeshSettings(unittest.TestCase):
    def setUp(self):
        self.before=set(App.listDocuments());Gui.Selection.clearSelection()
        self.prefs=App.ParamGet(mesh_ui.PREFERENCES);self.old_defaults=self.prefs.GetString('Defaults');self.prefs.RemString('Defaults')
        self.doc=document.new_document('MeshSettings');self.owner=document.validate(self.doc).Definitions[0]
        editing.edit((document.validate(self.doc).Group[0],))
        with document.transaction(self.doc,'Fixture'):
            self.box=self.owner.newObject('Part::Feature','Box');self.box.Shape=Part.makeBox(20,14,10)
            self.sheet=self.owner.newObject('Part::Feature','Sheet');self.sheet.Shape=Part.makePlane(8,6,App.Vector(30,0,0))
        self.out=Path(os.environ['PLUS_TEST_DIR'])

    def tearDown(self):
        for module in (mesh_task,transform_task,trim_task):
            if module._active:module._active.reject()
        self.prefs.SetString('Defaults',self.old_defaults)
        for name in set(App.listDocuments())-self.before:App.closeDocument(name)
        QtTest.QTest.qWait(40)

    def task(self):
        import MeshPartGui
        Gui.runCommand('MeshPart_Mesher');self.assertIsNotNone(mesh_task._active);return mesh_task._active

    def test_mixed_exact_sources_and_duplicate_coverage(self):
        task=self.task();self.assertFalse(hasattr(task.form,'solid'))
        task.addSelection(self.doc.Name,self.box.Name,'Face1');task.addSelection(self.doc.Name,self.sheet.Name,'')
        self.assertEqual(task.refs,[(self.box,'Face1'),(self.sheet,'')])
        task.addSelection(self.doc.Name,self.box.Name,'');self.assertEqual(task.refs,[(self.box,''),(self.sheet,'')])
        task.addSelection(self.doc.Name,self.box.Name,'Face2');self.assertEqual(len(task.refs),2)
        self.assertTrue(task.apply(),task.form.status.text());self.assertEqual(task.result.Mesh.CountFacets,14)
        self.assertIn(task.result,document.history(self.doc,self.owner));document.validate(self.doc)
        self.assertEqual(task.refs,[])

    def test_defaults_cancel_apply_and_new_task(self):
        task=self.task();f=task.form
        self.assertEqual(set(f.controls),{'spinSurfaceDeviation','spinAngularDeviation'})
        f.open_advanced();QtTest.QTest.qWait(60)
        f.native('spinSurfaceDeviation').setProperty('rawValue',.04);f.radios[1].click();f.advanced_dialog.reject()
        self.assertEqual(f.method.currentIndex(),0);self.assertEqual(self.prefs.GetString('Defaults'),'')
        f.open_advanced();f.native('spinSurfaceDeviation').setProperty('rawValue',.08);f.native('spinAngularDeviation').setProperty('rawValue',12)
        f.accept_advanced();self.assertFalse(f.advanced_dialog.isVisible(),f.advanced_status.text())
        f.controls['spinSurfaceDeviation'].setProperty('rawValue',.025)
        task.addSelection(self.doc.Name,self.box.Name,'');self.assertTrue(task.apply(),f.status.text())
        saved=json.loads(task.result.MeshSettings);self.assertAlmostEqual(saved['parameters']['LinearDeflection'],.025)
        self.assertAlmostEqual(saved['parameters']['AngularDeflection'],math.radians(12))
        self.assertAlmostEqual(task.number('spinSurfaceDeviation'),.08);self.assertFalse(task.refs)
        task.reject();task=self.task();self.assertAlmostEqual(task.number('spinSurfaceDeviation'),.08)

    def test_nonstandard_fields_and_defaults_reset(self):
        task=self.task();f=task.form
        for index,field in ((1,'spinMaximumEdgeLength'),(2,'comboFineness'),(3,'minSize')):
            if not f.radios[index].isEnabled():continue
            f.open_advanced();f.radios[index].click();f.accept_advanced()
            self.assertIn(field,f.controls);self.assertNotIn('spinSurfaceDeviation',f.controls)
            if index==1:
                f.controls[field].setProperty('rawValue',1.5);task.addSelection(self.doc.Name,self.sheet.Name,'')
                self.assertTrue(task.apply(),f.status.text());self.assertEqual(f.method.currentIndex(),1)
            if index==2:
                f.controls[field].setCurrentIndex(5);self.assertTrue(f.controls['doubleGrading'].isEnabled())
            f.reset();self.assertEqual(f.method.currentIndex(),index)
        f.open_advanced();f.radios[0].click();f.accept_advanced();task.addSelection(self.doc.Name,self.box.Name,'Face1')
        QtTest.QTest.qWait(100);f.grab().save(str(self.out/'mesh-main.png'))
        f.open_advanced();QtTest.QTest.qWait(100);f.advanced_dialog.grab().save(str(self.out/'mesh-advanced.png'))
        f.advanced_dialog.reject()

    def test_saved_recipe_reopens_in_history_without_overwriting_defaults(self):
        task=self.task();f=task.form
        f.controls['spinSurfaceDeviation'].setProperty('rawValue',.035);f.controls['spinAngularDeviation'].setProperty('rawValue',9)
        task.addSelection(self.doc.Name,self.box.Name,'');self.assertTrue(task.apply(),f.status.text());feature=task.result;name=feature.Name
        task.reject();path=self.out/'mesh-settings.cadprt';document.save_document(self.doc,path)
        App.closeDocument(self.doc.Name);self.doc=document.open_document(path);feature=self.doc.getObject(name)
        task=editing.edit_feature(self.doc,feature)
        self.assertIs(task,mesh_task._active);self.assertAlmostEqual(task.number('spinSurfaceDeviation'),.035)
        self.assertAlmostEqual(task.number('spinAngularDeviation'),9);self.assertEqual(self.prefs.GetString('Defaults'),'')
        before=feature.MeshSettings;undo=self.doc.UndoCount
        task.form.controls['spinSurfaceDeviation'].setProperty('rawValue',.2);task.reject()
        self.assertEqual(feature.MeshSettings,before);self.assertEqual(self.doc.UndoCount,undo)

    def test_old_quantity_recipe_and_invalid_saved_control(self):
        task=self.task();settings=task.settings()
        settings['controls']['spinSurfaceDeviation']=['value',.065]
        task.restore_settings(settings);self.assertAlmostEqual(task.number('spinSurfaceDeviation'),.065)
        settings['controls']['spinSurfaceDeviation']=['enabled',False]
        with self.assertRaises(ValueError):task.restore_settings(settings)

    def test_transformation_and_trim_history_edit_routing(self):
        result=transforms.save(self.doc,[(self.box,'')],[dict(kind='Linear pattern',axis=0,count=3,value=25)])[0]
        task=editing.edit_feature(self.doc,result);self.assertIs(task,transform_task._active);task.reject()
        result=trim_body.save(self.doc,(self.box,''),[],dict(mode=1,plane=0,offset=5,reverse=False))
        task=editing.edit_feature(self.doc,result);self.assertIs(task,trim_task._active);task.reject()

    def test_modeling_ribbon_buttons_open_whole_shape_tasks(self):
        from freecad_plus import toolbars,ui_modes
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/General');mode=prefs.GetInt('ToolbarUIMode',0)
        try:
            prefs.SetInt('ToolbarUIMode',0);ui_modes.apply_modes();QtTest.QTest.qWait(120)
            ribbon=toolbars._controller;ribbon.select_tab(next(i for i,(name,_) in enumerate(ribbon.tabs) if name=='Modeling'))
            QtTest.QTest.qWait(150)
            for command,kind in zip(('Mirrored','LinearPattern','PolarPattern','MultiTransform'),transforms.KINDS):
                button=ribbon.scroll.widget().findChild(QtWidgets.QToolButton,'Plus_PartDesign_'+command)
                self.assertIsNotNone(button);Gui.Selection.clearSelection();Gui.Selection.addSelection(self.box)
                Gui.updateGui();QtTest.QTest.qWait(200)
                self.assertTrue(button.isEnabled(),command+' is disabled')
                button.click();QtTest.QTest.qWait(80)
                self.assertIsNotNone(transform_task._active,command);self.assertEqual(transform_task._active.kind,kind)
                transform_task._active.reject()
        finally:prefs.SetInt('ToolbarUIMode',mode);ui_modes.apply_modes()

    def test_promoted_sheet_preserves_face_material_and_transparency(self):
        child=hierarchy.create_definition(self.doc,'Child');link=hierarchy.add_instance(self.owner,child)
        with document.transaction(self.doc,'Colored sheet'):
            sheet=child.newObject('Part::Feature','SourceSheet');sheet.Shape=Part.makePlane(8,6)
            sheet.ViewObject.ShapeAppearance=[App.Material(DiffuseColor=(.2,.4,.7),Transparency=.4,Shininess=.6)]
        result=derived_geometry.save(self.doc,[(link,sheet.Name+'.')])[0]
        a=appearance.materials(sheet)[0];b=appearance.materials(result)[0]
        self.assertEqual(a.DiffuseColor,b.DiffuseColor);self.assertAlmostEqual(a.Transparency,b.Transparency)
        self.assertAlmostEqual(a.Shininess,b.Shininess)
