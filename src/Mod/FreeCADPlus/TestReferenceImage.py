# SPDX-License-Identifier: LGPL-2.1-or-later
import json,os,unittest,zipfile
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui
from PySide6 import QtCore,QtGui,QtTest,QtWidgets
from freecad_plus import document,editing,planes,panel,hierarchy,external
from freecad_plus import reference_image as images,reference_image_task as tasks


class TestReferenceImage(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:self.skipTest('Requires isolated native profile')
        self.before=set(App.listDocuments());self.out=Path(os.environ['PLUS_TEST_DIR'])
        self.doc=document.new_document('ImageTest');self.owner=document.validate(self.doc).Definitions[0]
        self.xy=next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        self.file=self.out/(self.id().split('.')[-1]+'.png')
        image=QtGui.QImage(300,200,QtGui.QImage.Format_RGB32);image.fill(QtGui.QColor('#83aabd'))
        painter=QtGui.QPainter(image);painter.setPen(QtGui.QPen(QtGui.QColor('#123456'),4));painter.drawRect(20,20,260,160);painter.drawEllipse(80,60,50,50);painter.end()
        assert image.save(str(self.file))

    def tearDown(self):
        if tasks._active:tasks._active.reject()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments())-self.before:App.closeDocument(name)
        QtTest.QTest.qWait(30)

    def make(self,support=True,state=None):
        return images.save(self.doc,str(self.file),self.xy if support is True else support,120,80,state or images.defaults(),35)

    def settle(self):Gui.updateGui();QtTest.QTest.qWait(100)

    def test_native_attachment_recompute_and_embedded_save(self):
        plane=planes.save(self.doc,[(self.xy,'')],10)
        state=images.defaults();state['position']=[3,4,7];state['rotation'][2]=12.35
        feature=self.make(plane,state);name=feature.Name
        self.assertEqual(feature.TypeId,'Image::ImagePlane')
        self.assertAlmostEqual(feature.Placement.Base.z,17)
        plane.Offset=20;self.doc.recompute();self.assertAlmostEqual(feature.Placement.Base.z,27)
        self.assertIn(feature,document.history(self.doc,self.owner))
        path=self.out/'reference-image.cadprt';document.save_document(self.doc,path)
        with zipfile.ZipFile(path) as archive:self.assertTrue(any(n.lower().endswith('.png') for n in archive.namelist()))
        self.file.unlink();App.closeDocument(self.doc.Name)
        restored=document.open_document(path);feature=restored.getObject(name)
        self.assertEqual(images.settings(feature),state)
        self.assertFalse(images.read_image(feature.ImageFile).isNull())
        self.assertAlmostEqual(feature.Placement.Base.z,27)
        self.assertEqual(feature.ViewObject.Transparency,35)
        self.assertEqual(document.validate(restored).PlusSchema,9)

    def test_anchor_fixed_resize_rotate_all_nine_and_custom(self):
        for u in (0,.5,1,.23):
            for v in (0,.5,1,.71):
                state=images.defaults();state.update(anchor=[u,v],position=[13,-7,4],rotation=[0,0,12.35])
                for width,height,angle in ((120,80,12.35),(240,160,-25.75)):
                    state['rotation'][2]=angle
                    p=images.placement(self.owner,self.xy,width,height,state)
                    self.assertTrue(images.anchor_position(p,width,height,[u,v]).isEqual(App.Vector(13,-7,4),1e-8))

    def test_fundamental_planes_and_free_xyz(self):
        state=images.defaults();state['position']=[1,2,3];state['rotation']=[1.25,-2.5,12.35]
        for support in images.supports(self.owner)+[None]:
            feature=self.make(support,state)
            expected=images.placement(self.owner,support,120,80,state)
            self.assertTrue(feature.Placement.isSame(expected,1e-7),str(feature.Placement)+' / '+str(expected))
        self.assertEqual(feature.MapMode,'Deactivated')

    def test_schema_upgrade_transaction_undo_and_delete(self):
        root=document.validate(self.doc);root.PlusSchema=8;self.doc.clearUndos()
        feature=self.make();name=feature.Name
        self.assertEqual(self.doc.UndoCount,1);self.assertEqual(root.PlusSchema,9)
        self.doc.undo();self.doc.recompute();self.assertIsNone(self.doc.getObject(name));self.assertEqual(root.PlusSchema,8)
        self.doc.redo();self.doc.recompute();feature=self.doc.getObject(name)
        images.remove(self.doc,feature);self.assertIsNone(self.doc.getObject(name))
        self.doc.undo();self.doc.recompute();document.validate(self.doc);self.assertIsNotNone(self.doc.getObject(name))

    def test_preview_cancel_keeps_document_and_undo(self):
        feature=self.make();self.doc.clearUndos();before=(len(self.doc.Objects),feature.ImageSettings,str(feature.Placement),feature.ViewObject.Transparency,feature.Visibility,self.doc.UndoCount)
        task=tasks.show(feature);task.form.angle.setValue(23.45);task.form.alpha.setValue(65);task.refresh()
        self.assertIsNotNone(task.overlay,task.form.status.text())
        self.assertEqual(task.form.angle.textFromValue(23.45),'23.45 °')
        task.form.angle.stepUp();self.assertAlmostEqual(task.form.angle.value(),23.46)
        self.assertEqual(task.form.slider.value(),65)
        task.reject()
        self.assertEqual(before,(len(self.doc.Objects),feature.ImageSettings,str(feature.Placement),feature.ViewObject.Transparency,feature.Visibility,self.doc.UndoCount))

    def test_apply_resets_and_edit_reuses_identity(self):
        task=tasks.show();task.set_file(str(self.file));task.form.angle.setValue(12.35);task.refresh()
        self.assertTrue(task.apply(),task.form.status.text());feature=task.result;identity=feature.ID
        self.assertEqual(task.filename,'');self.assertEqual(task.form.points.count(),0);self.assertEqual(task.form.alpha.value(),0)
        self.assertEqual(task.form.angle.value(),0);self.assertFalse(task.form.done.isEnabled())
        task.reject();task=editing.edit_feature(self.doc,feature)
        self.assertAlmostEqual(task.form.angle.value(),12.35)
        task.form.alpha.setValue(50);self.assertTrue(task.accept())
        self.assertEqual(feature.ID,identity);self.assertEqual(feature.ViewObject.Transparency,50)
        self.assertEqual(len([o for o in self.owner.Group if images.is_image(o)]),1)

    def test_picked_anchor_no_jump_and_calibration(self):
        task=tasks.show();task.set_file(str(self.file));task.form.angle.setValue(12.35);task.refresh()
        before=task.world_placement();task.form.custom.setChecked(True);task.start_pick('anchor')
        point=before.multVec(App.Vector(-25,10,0));task.pick_world(point)
        self.assertTrue(task.world_placement().isSame(before,1e-7))
        anchor=images.anchor_position(before,task.form.width.value(),task.form.height.value(),task.anchor)
        task.form.width.setValue(200);task.refresh()
        self.assertTrue(images.anchor_position(task.world_placement(),task.form.width.value(),task.form.height.value(),task.anchor).isEqual(anchor,1e-7))
        task.start_pick('calibration');placement=task.world_placement()
        task.pick_world(placement.multVec(App.Vector(-50,0,0)));task.pick_world(placement.multVec(App.Vector(50,0,0)))
        task.form.known.setValue(50);task.calibrate();self.assertAlmostEqual(task.form.width.value(),100)
        task.form.known.setValue(75);task.calibrate();self.assertAlmostEqual(task.form.width.value(),150)
        self.assertEqual(task.form.points.count(),2)

    def test_bad_input_is_atomic_and_retains_fields(self):
        count=len(self.doc.Objects);undo=self.doc.UndoCount
        state=images.defaults();state['anchor']=[2,0]
        with self.assertRaises(ValueError):self.make(state=state)
        foreign=document.new_document('Foreign');foreign_owner=document.validate(foreign).Definitions[0]
        foreign_plane=next(o for o in foreign_owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        App.setActiveDocument(self.doc.Name)
        with self.assertRaises(ValueError):self.make(foreign_plane)
        self.assertEqual(len(self.doc.Objects),count);self.assertEqual(self.doc.UndoCount,undo)
        task=tasks.show();task.set_file(str(self.file));task.points=[[.5,.5],[.5,.5]];task.calibrate()
        self.assertEqual(task.filename,str(self.file));self.assertEqual(task.form.width.value(),100)

    def test_nonzero_component_placement_and_transformed_occurrence(self):
        self.owner.Placement=App.Placement(App.Vector(3,4,5),App.Rotation(App.Vector(0,0,1),32))
        root=document.validate(self.doc);root.Group[0].Placement=App.Placement(App.Vector(40,50,60),App.Rotation(App.Vector(1,0,0),20))
        plane=planes.save(self.doc,[(self.xy,'')],12)
        feature=self.make(plane)
        expected=images.placement(self.owner,plane,120,80,images.defaults())
        self.assertTrue(feature.Placement.isSame(expected,1e-7),str(feature.Placement)+' / '+str(expected))
        task=tasks.show(feature);task.refresh();self.assertIsNotNone(task.overlay,task.form.status.text())

    def test_imported_component_edits_own_file_and_copy_is_independent(self):
        from freecad_plus import part_transfer_ops
        document.save_document(self.doc,self.out/'image-source.cadprt')
        assembly=document.new_document('ImageAssembly');root=document.validate(assembly)
        root.Definitions[0].Label='Image assembly'
        document.save_document(assembly,self.out/'image-assembly.cadprt')
        external.import_file(assembly,self.doc)
        child=hierarchy.add_instance(root.Definitions[0],self.owner,App.Placement(App.Vector(20,30,40),App.Rotation()))
        App.setActiveDocument(assembly.Name);editing.edit((root.Group[0],child))
        count=len(assembly.Objects);task=tasks.show();task.set_file(str(self.file));self.assertTrue(task.accept())
        feature=task.result;self.assertEqual(feature.Document,self.doc);self.assertEqual(len(assembly.Objects),count)
        name=feature.Name;self.doc.undo();self.doc.recompute();self.assertIsNone(self.doc.getObject(name))
        self.doc.redo();self.doc.recompute();feature=self.doc.getObject(name)
        copied=part_transfer_ops.export_parts([self.owner],self.out/'image-copy.cadprt')
        reopened=document.open_document(copied);other=next(o for o in reopened.Objects if images.is_image(o))
        self.assertNotEqual(other,feature);self.assertFalse(images.read_image(other.ImageFile).isNull())
        owner=document.validate(reopened).Definitions[0];self.assertIn(other.AttachmentSupport[0][0],images.supports(owner))

    def test_missing_plane_can_be_replaced_without_losing_panel(self):
        plane=planes.save(self.doc,[(self.xy,'')],10);feature=self.make(plane)
        with document.transaction(self.doc,'Remove plane'):self.doc.removeObject(plane.Name)
        document.validate(self.doc);self.assertIn(feature,document.history(self.doc,self.owner))
        task=tasks.show(feature);task.form.plane.setCurrentIndex(0);task.refresh();self.assertTrue(task.accept())
        self.assertEqual(feature.AttachmentSupport[0][0],self.xy)

    def test_context_change_blocks_apply_without_document_changes(self):
        task=tasks.show();task.set_file(str(self.file));count=len(self.doc.Objects)
        other=document.new_document('OtherImageContext');task.refresh()
        self.assertFalse(task.apply());self.assertEqual(len(self.doc.Objects),count)
        self.assertEqual(task.filename,str(self.file))

    def test_native_mouse_anchor_in_orthographic_and_perspective(self):
        task=tasks.show();task.set_file(str(self.file));task.form.custom.setChecked(True)
        view=task.view;view.setAnimationEnabled(False);view.viewTop();view.fitAll();self.settle()
        for mode in ('Orthographic','Perspective'):
            view.setCameraType(mode);view.viewTop();view.fitAll();self.settle()
            before=task.world_placement();target=before.multVec(App.Vector(-20,12,0))
            viewport=view.graphicsView().viewport();ratio=viewport.devicePixelRatioF()
            screen=view.getPointOnScreen(target)
            point=QtCore.QPoint(round(screen[0]/ratio),viewport.height()-1-round(screen[1]/ratio))
            task.start_pick('anchor')
            QtTest.QTest.mouseClick(viewport,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,point);self.settle()
            self.assertIsNone(task.pick_mode,mode+' '+task.form.status.text())
            self.assertAlmostEqual(task.anchor[0],.3,delta=.015)
            self.assertAlmostEqual(task.anchor[1],.68,delta=.015)
            self.assertTrue(task.world_placement().isSame(before,1e-7))

    def test_native_history_menu_edit_visibility_delete(self):
        feature=self.make();widget=panel.show_panel()
        def choose(label):
            widget.refresh();widget.tabs.setCurrentIndex(2);self.settle();tree=widget.trees[2]
            item=next(i for i in widget._maps[2].values() if i.data(0,panel._ROLE).ref==panel.identity(feature))
            point=tree.visualItemRect(item).center();point.setX(80)
            seen=[]
            def click():
                menu=QtWidgets.QApplication.activePopupWidget()
                if menu is None:return
                seen.extend(a.text() for a in menu.actions() if not a.isSeparator())
                action=next(a for a in menu.actions() if a.text()==label)
                QtTest.QTest.mouseClick(menu,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,menu.actionGeometry(action).center())
            QtCore.QTimer.singleShot(100,click);widget._menu(tree,point);self.settle()
            return seen
        self.assertEqual(choose('Hide'),['Edit reference image…','Hide','Delete']);self.assertFalse(feature.Visibility)
        choose('Show');self.assertTrue(feature.Visibility)
        choose('Edit reference image…');self.assertEqual(tasks._active.feature,feature);tasks._active.reject()
        name=feature.Name;choose('Delete');self.assertIsNone(self.doc.getObject(name))
        self.doc.undo();self.doc.recompute();self.assertIsNotNone(self.doc.getObject(name))

    def test_gui_capture_history_and_entry(self):
        tasks.install();self.assertTrue(Gui.Command.get('Plus_ReferenceImage').isActive())
        if os.environ.get('PLUS_TEST_PHASE')=='installed':
            from TestTaskEntryWorkflows import action_boxes
            Gui.Selection.clearSelection();self.settle()
            box=next(w for w,labels in action_boxes() if 'Reference image' in labels)
            next(a for a in box.actions() if a.text().replace('&','')=='Reference image').trigger()
        else:Gui.runCommand('Plus_ReferenceImage')
        task=tasks._active;self.assertIsNotNone(task)
        task.set_file(str(self.file));task.form.angle.setValue(12.35);task.form.alpha.setValue(35);task.refresh();self.settle()
        self.assertIsNotNone(task.overlay,task.form.status.text())
        view=Gui.activeDocument().activeView();view.viewTop();view.fitAll();self.settle()
        from pivy import coin
        box=coin.SoGetBoundingBoxAction(coin.SbViewportRegion(1000,700));box.apply(task.overlay)
        (self.out/'scene-debug.txt').write_text(str(box.getBoundingBox())+'\n'+view.getCamera())
        view.saveImage(str(self.out/'reference-preview.png'),1000,700,'White')
        task.form.grab().save(str(self.out/'reference-task.png'))
        self.assertTrue(task.accept())
        widget=panel.show_panel();widget.refresh();widget.tabs.setCurrentIndex(2)
        self.assertIn(task.result,document.history(self.doc,self.owner));self.settle()
        widget.grab().save(str(self.out/'reference-history.png'))
