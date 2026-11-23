# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native plane collection/persistence and dependency-safe manual History."""
import os
from pathlib import Path
import unittest
import FreeCAD as App,FreeCADGui as Gui,Part
from PySide6 import QtCore,QtGui,QtWidgets,QtTest
from freecad_plus import document,planes,plane_task,sketch_task,sketch_placement,extrusion,panel,editing,external,hierarchy
from TestComponentPlanes import TestComponentPlanes
from TestComponentModeling import messages


class TestPlaneHistoryWorkflow(unittest.TestCase):
    setUp=TestComponentPlanes.setUp
    feature=TestComponentPlanes.feature

    def tearDown(self):
        if sketch_task._active:sketch_task._active.reject()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit();App.closeActiveTransaction()
        TestComponentPlanes.tearDown(self)

    def frame_refs(self):
        line=self.feature(Part.makeLine(App.Vector(),App.Vector(0,0,20)))
        point=self.feature(Part.Vertex(App.Vector(4,5,7)))
        return (line,'Edge1'),(point,'Vertex1')

    def native_attach(self, sketch, plane):
        Gui.Selection.clearSelection();Gui.Selection.addSelection(plane,'Face1')
        dialogs=[];timer=QtCore.QTimer()
        def answer():
            dialog=QtWidgets.QApplication.activeModalWidget()
            if not isinstance(dialog,QtWidgets.QInputDialog):return
            dialogs.append(dialog.windowTitle())
            combo=dialog.findChild(QtWidgets.QComboBox)
            if dialog.windowTitle()=='Select Sketch':
                combo.setCurrentText(sketch.Label)
            else:
                index=next((i for i in range(combo.count()) if '(suggested)' in combo.itemText(i)), -1)
                if index<0:dialog.reject();return
                combo.setCurrentIndex(index)
            dialog.accept()
        timer.timeout.connect(answer);timer.start(25)
        try:
            with messages() as errors:Gui.runCommand('Sketcher_MapSketch');QtTest.QTest.qWait(100)
        finally:timer.stop()
        return errors,dialogs

    def test_attach_sketch_command_rejects_later_plane_then_reorder_retry(self):
        with document.transaction(self.doc,'Native sketch fixture'):
            sketch=self.owner.newObject('Sketcher::SketchObject','NativeSketch')
            sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False)
        plane=planes.save(self.doc,[(self.xy,'')],7)
        before=(sketch.Placement,sketch.MapMode,list(sketch.AttachmentSupport),self.doc.UndoCount)
        errors,dialogs=self.native_attach(sketch,plane)
        self.assertTrue(any('Reorder History' in error and 'try again' in error for error in errors),errors)
        self.assertNotIn('Sketch Attachment',dialogs)
        self.assertEqual(document.history(self.doc,self.owner),[sketch,plane])
        self.assertTrue(sketch.Placement.isSame(before[0],1e-7))
        self.assertEqual((sketch.MapMode,list(sketch.AttachmentSupport),self.doc.UndoCount),before[1:])
        document.reorder_history(self.doc,self.owner,plane,0)
        errors,dialogs=self.native_attach(sketch,plane)
        self.assertFalse(errors,errors);self.assertIn('Sketch Attachment',dialogs)
        self.assertEqual(sketch.AttachmentSupport[0][0],plane)
        self.assertAlmostEqual(sketch.Placement.Base.z,7)
        self.doc.undo();self.doc.recompute();self.assertFalse(sketch.AttachmentSupport)
        self.doc.redo();self.doc.recompute();self.assertEqual(sketch.AttachmentSupport[0][0],plane)

    def test_managed_attach_sketch_command_rejects_later_pick(self):
        sketch=sketch_placement.save(self.doc,[(self.xy,'')])
        plane=planes.save(self.doc,[(self.xy,'')],7)
        Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch)
        Gui.runCommand('Sketcher_MapSketch');QtTest.QTest.qWait(80)
        task=sketch_task._active;self.assertIsNotNone(task)
        before=list(task.refs);self.pick(task,(plane,''))
        self.assertEqual(task.refs,before)
        self.assertIn('Reorder History',task.status.text());self.assertIn('try again',task.status.text())
        task.reject()

    def test_native_attach_sketch_legacy_document_remains_supported(self):
        legacy=App.newDocument('LegacyAttachOrder')
        sketch=legacy.addObject('Sketcher::SketchObject','LegacySketch')
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False)
        plane=legacy.addObject('Part::Plane','LaterPlane');plane.Placement.Base.z=7;legacy.recompute()
        errors,dialogs=self.native_attach(sketch,plane)
        self.assertFalse(errors,errors);self.assertIn('Sketch Attachment',dialogs)
        self.assertEqual(sketch.AttachmentSupport[0][0],plane)

    def test_sketch_support_property_rejects_later_reference(self):
        from TestPartBooleanInputs import TestPartBooleanInputs
        with document.transaction(self.doc,'Native sketch fixture'):
            sketch=self.owner.newObject('Sketcher::SketchObject','NativeSketch')
        plane=planes.save(self.doc,[(self.xy,'')],7)
        def select(obj):
            Gui.Selection.clearSelection();Gui.Selection.addSelection(obj)
        self.select=select
        dialog=TestPartBooleanInputs.open_compound_links(self,sketch,'Attachment Support')
        TestPartBooleanInputs.choose_compound_links(self,dialog,[plane])
        before=self.doc.UndoCount
        with messages() as errors:dialog.accept();QtTest.QTest.qWait(100)
        self.assertTrue(any('Reorder History' in error for error in errors),errors)
        self.assertTrue(dialog.isVisible());self.assertFalse(sketch.AttachmentSupport)
        self.assertEqual(self.doc.UndoCount,before)
        self.assertEqual(document.history(self.doc,self.owner),[sketch,plane])
        dialog.reject()

    def pick(self,task,ref):
        task.pick_target='plane';Gui.Selection.clearSelection();Gui.Selection.addSelection(*ref)
        QtTest.QTest.qWait(25)

    def test_replacement_and_equivalent_face_in_both_tasks(self):
        xz=next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XZ_Plane')
        face=self.feature(Part.makePlane(12,15,App.Vector(0,0,8)))
        for module in (plane_task,sketch_task):
            task=module.show()
            self.pick(task,(self.xy,''));self.pick(task,(xz,''))
            self.assertEqual(task.refs,[(xz,'')]);self.assertTrue(task.valid,task.status.text())
            self.pick(task,(face,'Face1'))
            self.assertEqual(task.refs,[(face,'Face1')]);self.assertTrue(task.valid,task.status.text())
            self.assertAlmostEqual(task.placement().Base.z,8)
            task.reject()

    def test_coplanar_parallel_skew_and_incomplete_points(self):
        a=self.feature(Part.makeLine(App.Vector(),App.Vector(10,0,0)))
        b=self.feature(Part.makeLine(App.Vector(0,4,0),App.Vector(10,4,0)))
        skew=self.feature(Part.makeLine(App.Vector(0,0,5),App.Vector(0,10,5)))
        points=[self.feature(Part.Vertex(App.Vector(*p))) for p in ((0,0,3),(5,0,3),(0,5,3))]
        for module in (plane_task,sketch_task):
            task=module.show();self.pick(task,(a,'Edge1'));self.assertFalse(task.valid)
            self.pick(task,(b,'Edge1'));self.assertEqual(len(task.refs),2);self.assertTrue(task.valid)
            task.clear();self.pick(task,(a,'Edge1'));self.pick(task,(skew,'Edge1'))
            self.assertEqual(task.refs,[(skew,'Edge1')]);self.assertFalse(task.valid)
            task.clear()
            for i,p in enumerate(points):
                self.pick(task,(p,'Vertex1'));self.assertEqual(len(task.refs),i+1)
                self.assertEqual(task.valid,i==2)
            self.assertAlmostEqual(task.placement().Base.z,3);task.reject()

    def test_normal_line_point_both_orders_accept_edit_and_recompute(self):
        edge,vertex=self.frame_refs()
        datum_line=self.owner.newObject('PartDesign::Line','Axis')
        datum_point=self.owner.newObject('PartDesign::Point','Point');datum_point.Placement.Base=App.Vector(4,5,7)
        self.doc.recompute()
        for refs in ([edge,vertex],[vertex,edge],[(datum_line,''),(datum_point,'')]):
            for module in (plane_task,sketch_task):
                feature=planes.save(self.doc,[(self.xy,'')]) if module==plane_task else sketch_placement.save(self.doc,[(self.xy,'')])
                task=module.show(feature);task.clear()
                for ref in refs:self.pick(task,ref)
                self.assertEqual(task.refs,refs);self.assertTrue(task.valid,task.status.text())
                self.assertIn('defining point',task.origin_hint.text())
                self.assertTrue(task.placement().Base.isEqual(App.Vector(4,5,7),1e-7))
                self.assertTrue(task.placement().Rotation.multVec(App.Vector(0,0,1)).isEqual(App.Vector(0,0,1),1e-7))
                self.assertTrue(task.accept());self.assertTrue(feature.NormalToLine)
        feature=sketch_placement.save(self.doc,[edge,vertex]);vertex[0].Placement.Base.z=9;self.doc.recompute()
        self.assertAlmostEqual(feature.Placement.Base.z,16)

    def test_legacy_line_containing_plane_survives_open_edit_and_cancel(self):
        edge,vertex=self.frame_refs()
        old=planes.save(self.doc,[edge,vertex],normal_to_line=False)
        old.removeProperty('NormalToLine');self.doc.recompute();before=old.Placement
        task=plane_task.show(old);self.assertFalse(task.normal_to_line)
        self.assertTrue(task.placement().isSame(before,1e-7));task.reject()
        self.assertNotIn('NormalToLine',old.PropertiesList)
        task=plane_task.show(old);self.assertTrue(task.accept())
        self.assertFalse(old.NormalToLine);self.assertTrue(old.Placement.isSame(before,1e-7))
        self.doc.undo();self.doc.recompute();self.assertNotIn('NormalToLine',old.PropertiesList)
        path=Path(os.environ['PLUS_TEST_DIR'])/'OldPlane.cadprt';document.save_document(self.doc,path)
        name=old.Name;App.closeDocument(self.doc.Name);self.doc=document.open_document(path)
        self.assertTrue(self.doc.getObject(name).Placement.isSame(before,1e-7))

    def test_invalid_or_later_picks_do_not_discard_valid_refs(self):
        early=planes.save(self.doc,[(self.xy,'')]);sketch=sketch_placement.save(self.doc,[(early,'')])
        later=planes.save(self.doc,[(self.xy,'')],5)
        curved=self.feature(Part.makeCircle(5))
        for module,feature in ((plane_task,early),(sketch_task,sketch)):
            task=module.show(feature);before=list(task.refs)
            self.pick(task,(later,'Face1'));self.assertEqual(task.refs,before)
            self.assertIn('must precede',task.status.text())
            self.pick(task,(curved,'Edge1'));self.assertEqual(task.refs,before)
            task.reject()

    def test_new_sketch_from_two_refs_enters_drawing_and_undo(self):
        refs=self.frame_refs();task=sketch_task.show()
        for ref in refs:self.pick(task,ref)
        self.assertTrue(task.accept());QtTest.QTest.qWait(180)
        sketch=task.result;name=sketch.Name
        self.assertEqual(Gui.activeDocument().getInEdit().Object,sketch)
        self.assertTrue(sketch.NormalToLine)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();self.doc.recompute()
        self.doc.undo();self.assertIsNone(self.doc.getObject(name))
        self.doc.redo();self.doc.recompute();self.assertTrue(self.doc.getObject(name).NormalToLine)

    def chain(self):
        support=planes.save(self.doc,[(self.xy,'')],4)
        sketch=sketch_placement.save(self.doc,[(support,'')])
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False);self.doc.recompute()
        solid=extrusion.save(self.doc,[(sketch,'')],{},dict(extrusion.DEFAULTS,length=5))
        independent=planes.save(self.doc,[(self.xy,'')],-2)
        return support,sketch,solid,independent

    def test_history_clamps_both_directions_and_preserves_native_graph(self):
        p,s,f,i=self.chain();before={o.Name:(o.ID,tuple(x.Name for x in o.OutList)) for o in self.doc.Objects}
        self.assertEqual(document.reorder_history(self.doc,self.owner,i,1),'')
        self.assertEqual(document.history(self.doc,self.owner),[p,i,s,f])
        message=document.reorder_history(self.doc,self.owner,p,4)
        self.assertIn(s.Label,message);self.assertIn('cannot be moved after',message)
        self.assertEqual(document.history(self.doc,self.owner),[i,p,s,f])
        message=document.reorder_history(self.doc,self.owner,f,0)
        self.assertIn('cannot be moved before',message)
        self.assertEqual(document.history(self.doc,self.owner),[i,p,s,f])
        self.assertEqual({o.Name:(o.ID,tuple(x.Name for x in o.OutList)) for o in self.doc.Objects},before)
        self.assertAlmostEqual(f.Shape.Volume,45*3.141592653589793)
        with self.assertRaises(ValueError):document.reorder_history(self.doc,self.owner,self.owner.Origin,1)

    def test_history_undo_redo_save_new_deleted_and_reused_names(self):
        p,s,f,i=self.chain();names=[o.Name for o in (p,s,f,i)]
        document.reorder_history(self.doc,self.owner,i,0)
        order=[i,p,s,f];self.assertEqual(document.history(self.doc,self.owner),order)
        self.doc.undo();self.assertEqual(document.history(self.doc,self.owner),[p,s,f,i])
        self.doc.redo();self.assertEqual(document.history(self.doc,self.owner),order)
        oldname=i.Name
        with document.transaction(self.doc,'Replace deleted fixture'):
            self.doc.removeObject(oldname)
            new=self.owner.newObject('Part::Feature',oldname);new.Shape=Part.makePlane(5,5)
        self.assertEqual(document.history(self.doc,self.owner),[p,s,f,new])
        document.reorder_history(self.doc,self.owner,new,0)
        path=Path(os.environ['PLUS_TEST_DIR'])/'Ordered.cadprt';document.save_document(self.doc,path)
        owner_name=self.owner.Name;new_name=new.Name;App.closeDocument(self.doc.Name);self.doc=document.open_document(path)
        self.owner=self.doc.getObject(owner_name)
        self.assertEqual([o.Name for o in document.history(self.doc,self.owner)],[new_name,*names[:3]])

    def test_history_multiple_consumers_and_pending_transaction(self):
        p,s,f,i=self.chain();second=sketch_placement.save(self.doc,[(p,'')])
        document.reorder_history(self.doc,self.owner,second,1)
        self.assertEqual(document.history(self.doc,self.owner),[p,second,s,f,i])
        message=document.reorder_history(self.doc,self.owner,p,5)
        self.assertIn(second.Label,message)
        self.assertEqual(document.history(self.doc,self.owner)[0],p)
        before=list(getattr(self.owner,'PlusHistoryOrder',[]))
        self.doc.openTransaction('Unfinished operation')
        try:
            with self.assertRaisesRegex(ValueError,'Finish'):document.reorder_history(self.doc,self.owner,i,0)
        finally:self.doc.abortTransaction()
        self.assertEqual(list(self.owner.PlusHistoryOrder),before)

    def test_external_history_order_is_source_owned(self):
        folder=Path(os.environ['PLUS_TEST_DIR'])
        document.save_document(self.doc,folder/'HostOrder.cadprt')
        source=document.new_document('SourceOrder');owner=document.validate(source).Definitions[0]
        xy=next(o for o in owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        first=planes.save(source,[(xy,'')]);second=planes.save(source,[(xy,'')],3)
        document.save_document(source,folder/'SourceOrder.cadprt')
        external.import_file(self.doc,source)
        occurrence=hierarchy.add_instance(document.validate(self.doc),owner)
        App.setActiveDocument(self.doc.Name);editing.edit((occurrence,))
        host_undo=self.doc.UndoCount;source_undo=source.UndoCount
        host_properties={o.Name+'.'+prop:repr(getattr(o,prop)) for o in self.doc.Objects for prop in o.PropertiesList}
        document.reorder_history(self.doc,owner,second,0)
        self.assertEqual(document.history(self.doc,owner),[second,first])
        changed={o.Name+'.'+prop:(host_properties.get(o.Name+'.'+prop),repr(getattr(o,prop))) for o in self.doc.Objects for prop in o.PropertiesList
                 if host_properties.get(o.Name+'.'+prop)!=repr(getattr(o,prop))}
        self.assertEqual(changed,{})
        # Native Document::_openTransaction mirrors a source transaction into
        # the active host, with the same transaction ID for coordinated Undo.
        self.assertEqual(self.doc.UndoCount,host_undo+1)
        self.assertEqual(source.UndoCount,source_undo+1)
        self.assertNotIn('PlusHistoryOrder',self.owner.PropertiesList)
        source.undo();self.assertEqual(document.history(self.doc,owner),[first,second])

    def test_panel_real_drop_path_popup_fixed_frame_and_stale_payload(self):
        p,s,f,i=self.chain();widget=panel.show_panel();widget.tabs.setCurrentIndex(2);widget.refresh();QtTest.QTest.qWait(100)
        tree=widget.trees[2]
        def row(obj):return widget._maps[2][('history',panel.identity(obj))]
        def locked(item):return not bool(item.flags()&QtCore.Qt.ItemIsDragEnabled) and all(locked(item.child(j)) for j in range(item.childCount()))
        self.assertTrue(locked(tree.topLevelItem(0)))
        payload=widget.prepare_history_move(row(i).data(0,panel._ROLE))
        document.reorder_history(self.doc,self.owner,i,1)
        with self.assertRaisesRegex(ValueError,'changed'):widget.move_history(payload,0)
        widget.refresh();tree.payload=widget.prepare_history_move(row(p).data(0,panel._ROLE))
        mime=QtCore.QMimeData();mime.setData(tree.mime_type,b'feature')
        class Drop(QtGui.QDropEvent):
            def source(self):return tree
        event=Drop(QtCore.QPointF(tree.visualItemRect(row(f)).bottomLeft()+QtCore.QPoint(80,-1)),
                   QtCore.Qt.MoveAction,mime,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier)
        messages=[];timer=QtCore.QTimer()
        def close_popup():
            for box in Gui.getMainWindow().findChildren(QtWidgets.QMessageBox):
                if box.isVisible():
                    messages.append(box.text());self.assertEqual(document.history(self.doc,self.owner),[i,p,s,f]);box.accept()
        timer.timeout.connect(close_popup);timer.start(20)
        try:tree.dropEvent(event);QtTest.QTest.qWait(140)
        finally:timer.stop();tree.payload=None
        self.assertTrue(event.isAccepted());self.assertTrue(messages);self.assertIn(s.Label,messages[0])
        self.assertEqual(tree.topLevelItem(0).text(0),'Coordinate System')
