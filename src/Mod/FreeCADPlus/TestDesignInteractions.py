# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native acceptance of approved Design task and numeric interaction refinements."""
import os
import unittest
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtWidgets, QtTest, QtGui
from freecad_plus import document, editing, modeling, panel, sketch_task, plane_task, idle_tasks, extrusion, extrude_task, external, hierarchy


def settle():
    QtTest.QTest.qWait(100)


def arrow(field, up):
    option=QtWidgets.QStyleOptionSpinBox();option.initFrom(field)
    option.rect=field.rect();option.frame=True
    option.stepEnabled=QtWidgets.QAbstractSpinBox.StepUpEnabled|QtWidgets.QAbstractSpinBox.StepDownEnabled
    control=QtWidgets.QStyle.SC_SpinBoxUp if up else QtWidgets.QStyle.SC_SpinBoxDown
    rect=field.style().subControlRect(QtWidgets.QStyle.CC_SpinBox,option,control,field)
    QtTest.QTest.mouseClick(field,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,rect.center());settle()


class TestDesignInteractions(unittest.TestCase):
    maxDiff = None
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:self.skipTest('Requires an isolated native profile')
        self.before=set(App.listDocuments());self.doc=document.new_document('DesignInteractions')
        self.owner=document.validate(self.doc).Definitions[0]
        self.prefs=App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.previous=self.prefs.GetInt('TaskPanelUIMode',0);self.prefs.SetInt('TaskPanelUIMode',0)
        Gui.activateWorkbench('PartDesignWorkbench')
        self.panel=panel.show_panel();self.panel.tabs.setCurrentIndex(2);self.panel.refresh();settle()
        QtWidgets.QApplication.setActiveWindow(Gui.getMainWindow())

    def tearDown(self):
        for module in (sketch_task,plane_task,extrude_task):
            if module._active:module._active.reject()
        if Gui.Control.activeDialog():self.dialog(QtWidgets.QDialogButtonBox.Cancel)
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():Gui.activeDocument().resetEdit()
        if App.getActiveTransaction():App.closeActiveTransaction(True)
        self.prefs.SetInt('TaskPanelUIMode',self.previous)
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments())-self.before:App.closeDocument(name)
        settle()

    def dialog(self,which):
        settle()
        button=next(box.button(which) for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
                    if box.isVisible() and box.button(which) and box.button(which).isVisible())
        # Unattached native datums deliberately ask whether to keep placement.
        # Confirm that exact native prompt; never dismiss unrelated dialogs.
        def confirm_unattached():
            modal = QtWidgets.QApplication.activeModalWidget()
            if isinstance(modal, QtWidgets.QMessageBox) and modal.windowTitle() == 'Incompatible Reference Set':
                for choice in modal.buttons():
                    if modal.buttonRole(choice) == QtWidgets.QMessageBox.YesRole:
                        choice.click()
        timer = QtCore.QTimer();timer.timeout.connect(confirm_unattached);timer.start(30)
        try:
            QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton);settle()
        finally:timer.stop()

    def snapshot(self,doc=None):
        doc=doc or self.doc
        return ({o.Name:o.ID for o in doc.Objects},{o.Name:o.Visibility for o in doc.Objects if hasattr(o,'Visibility')},doc.UndoCount)

    def circle(self):
        sketch=modeling.new_sketch(self.doc);sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False)
        self.doc.recompute();return sketch

    def eye(self,obj):
        self.panel.refresh();tree=self.panel.trees[2];tree.expandAll();settle()
        item=next(item for item in self.panel._maps[2].values() if panel.lookup(item.data(0,panel._ROLE).ref)==obj)
        tree.scrollToItem(item);settle();rect=tree.visualItemRect(item)
        pos=QtCore.QPoint(tree.columnViewportPosition(1)+tree.columnWidth(1)//2,rect.center().y())
        calls=[];original=self.panel.toggle_history_visibility
        def toggle(row):
            try:
                original(row);calls.append(('ok',row.label))
            except Exception as error:
                calls.append(('error',str(error)));raise
        self.panel.toggle_history_visibility=toggle
        try:
            QtTest.QTest.mouseClick(tree.viewport(),QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,pos);settle()
        finally:self.panel.toggle_history_visibility=original
        self.assertEqual(calls,[('ok',item.data(0,panel._ROLE).label)])
        self.assertIn(('Show ' if not panel.history_visible(self.owner,obj) else 'Hide '),item.toolTip(1))

    def test_automatic_planes_cancel_preserves_saved_visibility_and_dirty_state(self):
        self.owner.Origin.Visibility=False
        features=self.owner.Origin.OriginFeatures
        for obj in features:obj.Visibility=obj.Role.endswith('_Axis')
        before=self.snapshot();Gui.activeDocument().Modified=False
        task=sketch_task.show();settle()
        for obj in features:self.assertEqual(panel.history_visible(self.owner,obj),obj.Role.endswith('_Plane'))
        self.assertFalse(Gui.activeDocument().Modified)
        task.reject();self.assertEqual(self.snapshot(),before);self.assertFalse(Gui.activeDocument().Modified)

    def test_history_eyes_keep_task_and_support_then_persist_intent(self):
        solid=modeling.extrude_new_solid(self.doc,self.circle(),5)
        self.owner.Origin.Visibility=False
        for obj in self.owner.Origin.OriginFeatures:obj.Visibility=False
        task=sketch_task.show();task.choose('XY Plane');refs=list(task.refs)
        self.eye(solid);self.assertFalse(solid.Visibility);self.assertFalse(task.closed);self.assertEqual(task.refs,refs)
        self.assertFalse(App.getActiveTransaction());self.assertFalse(self.doc.HasPendingTransaction)
        xy=next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        self.eye(xy);self.assertFalse(xy.Visibility)
        self.eye(xy);self.assertTrue(xy.Visibility)
        task.reject();self.assertFalse(solid.Visibility);self.assertTrue(xy.Visibility)
        self.assertTrue(self.owner.Origin.Visibility)
        self.doc.undo();self.doc.recompute();self.assertFalse(xy.Visibility)
        self.doc.redo();self.doc.recompute();self.assertTrue(xy.Visibility)

    def test_drawing_history_eyes_do_not_finish_transaction(self):
        solid=modeling.extrude_new_solid(self.doc,self.circle(),5)
        task=sketch_task.show();task.choose('XY Plane');self.dialog(QtWidgets.QDialogButtonBox.Ok)
        sketch=task.result;self.assertEqual(Gui.activeDocument().getInEdit().Object,sketch)
        transaction=App.getActiveTransaction();undo=self.doc.UndoCount
        self.eye(solid);self.assertFalse(solid.Visibility)
        self.assertEqual(App.getActiveTransaction(),transaction);self.assertEqual(self.doc.UndoCount,undo)
        self.assertEqual(Gui.activeDocument().getInEdit().Object,sketch)
        self.eye(solid);self.assertTrue(solid.Visibility)
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();self.doc.recompute()
        name=sketch.Name;self.doc.undo();self.assertIsNone(self.doc.getObject(name))
        self.assertTrue(solid.Visibility)

    def test_context_change_and_document_close_restore_planes(self):
        before=self.snapshot();task=sketch_task.show();editing.edit_file(self.doc);settle()
        self.assertTrue(task.closed);self.assertEqual(self.snapshot(),before)
        editing.edit((document.validate(self.doc).Group[0],));task=sketch_task.show();App.closeDocument(self.doc.Name);settle()
        self.assertTrue(task.closed);self.assertIsNone(sketch_task._active)

    def test_idle_actions_and_native_datum_create_cancel_edit(self):
        Gui.Selection.clearSelection();settle();self.assertTrue(idle_tasks.eligible())
        for kind in ('Line','Point'):
            before=self.snapshot();Gui.runCommand('FreeCADPlus_Datum'+kind);settle()
            datum=next(o for o in self.owner.Group if o.TypeId=='PartDesign::'+kind)
            self.assertTrue(Gui.Control.activeDialog());self.assertFalse(idle_tasks.eligible())
            self.dialog(QtWidgets.QDialogButtonBox.Cancel);self.assertEqual(self.snapshot(),before)
            datum=idle_tasks.create_datum(kind);settle();self.dialog(QtWidgets.QDialogButtonBox.Ok)
            name,identity=datum.Name,datum.ID
            self.assertEqual(datum.getParentGeoFeatureGroup(),self.owner)
            self.assertFalse(any(o.TypeId=='PartDesign::Body' for o in self.doc.Objects))
            editing.edit_feature(self.doc,datum);settle();self.assertTrue(Gui.Control.activeDialog())
            self.dialog(QtWidgets.QDialogButtonBox.Cancel);self.assertEqual(datum.ID,identity)
            self.doc.undo();self.assertIsNone(self.doc.getObject(name))
            self.doc.redo();self.assertEqual(self.doc.getObject(name).ID,identity)
        self.prefs.SetInt('TaskPanelUIMode',1);self.assertFalse(idle_tasks.eligible())

    def test_external_source_planes_and_datum_ownership(self):
        folder=Path(os.environ['PLUS_TEST_DIR'])/'design-external';folder.mkdir(exist_ok=True)
        document.save_document(self.doc,folder/'Assembly.cadprt')
        source=document.new_document('DesignSource');owner=document.validate(source).Definitions[0]
        document.save_document(source,folder/'Source.cadprt')
        external.import_file(self.doc,source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc,owner)
        original={o.Name:o.Visibility for o in source.Objects if hasattr(o,'Visibility')};undo=source.UndoCount
        task=sketch_task.show();self.assertTrue(all(o.Visibility for o in owner.Origin.OriginFeatures if o.Role.endswith('_Plane')))
        task.reject();self.assertEqual({o.Name:o.Visibility for o in source.Objects if hasattr(o,'Visibility')},original)
        self.assertEqual(source.UndoCount,undo)
        datum=idle_tasks.create_datum('Line');settle();self.dialog(QtWidgets.QDialogButtonBox.Ok)
        self.assertEqual(datum.Document,source);self.assertEqual(datum.getParentGeoFeatureGroup(),owner)
        document.save_document(source,folder/'Source.cadprt')

    def test_extrude_and_plane_arrows_commit_while_typing_waits(self):
        feature=extrusion.save(self.doc,[(self.circle(),'')],{},dict(extrusion.DEFAULTS))
        before=self.snapshot();task=extrude_task.show(feature);settle()
        field=task.end1['length'];field.setFocus();field.selectAll();revision=task.revisions
        QtTest.QTest.keyClicks(field,'12');settle();self.assertEqual(task.revisions,revision)
        arrow(field,True);self.assertTrue(field.hasFocus());self.assertEqual(task.values[field],13)
        self.assertAlmostEqual(task.tool_shape.BoundBox.ZLength,13)
        arrow(field,False);self.assertEqual(task.values[field],12)
        revision=task.revisions;task.profiles.setFocus();settle();self.assertEqual(task.revisions,revision)
        task.automatic.setChecked(False);field.setFocus();arrow(field,True)
        self.assertEqual(task.revisions,revision);task.reject();self.assertEqual(self.snapshot(),before)
        task=plane_task.show();task.choose('XY Plane');settle();field=task.offset
        field.setFocus();field.selectAll();QtTest.QTest.keyClicks(field,'4');settle()
        self.assertEqual(task.preview_offset,0);arrow(field,True);self.assertEqual(task.preview_offset,5)
        task.reject()

    def test_ordinary_and_native_numeric_arrows(self):
        form=QtWidgets.QWidget();layout=QtWidgets.QVBoxLayout(form);other=QtWidgets.QLineEdit()
        editors=[QtWidgets.QDoubleSpinBox(),QtWidgets.QSpinBox(),Gui.UiLoader().createWidget('Gui::QuantitySpinBox')]
        for field in editors:
            if field.inherits('Gui::QuantitySpinBox'):field.setProperty('unit','mm');field.setProperty('rawValue',8.)
            else:field.setValue(8)
            layout.addWidget(field)
        layout.addWidget(other);form.show();form.activateWindow();settle();QtWidgets.QApplication.setActiveWindow(form)
        try:
            for field in editors:
                with self.subTest(editor=field.metaObject().className()):
                    values=[];callback=lambda value:values.append(value)
                    native=field.inherits('Gui::QuantitySpinBox')
                    if native:QtCore.QObject.connect(field,QtCore.SIGNAL('valueChanged(double)'),callback)
                    else:field.valueChanged.connect(callback)
                    field.setFocus();field.selectAll();QtTest.QTest.keyClicks(field,'12');settle();self.assertEqual(values,[])
                    arrow(field,True);self.assertTrue(field.hasFocus());self.assertEqual(values,[13.])
                    arrow(field,False);self.assertEqual(values,[13.,12.])
                    other.setFocus();settle();self.assertEqual(values,[13.,12.])
                    if native:QtCore.QObject.disconnect(field,QtCore.SIGNAL('valueChanged(double)'),callback)
                    else:field.valueChanged.disconnect(callback)
        finally:form.close()
    def render_visibility(self, objects):
        # LinkVisibility controls the rendered occurrences independently of the
        # persisted Visibility flags displayed by History.
        return {obj.Name:(bool(obj.Visibility),bool(obj.ViewObject.LinkVisibility)) for obj in objects}

    def test_new_sketch_preserves_existing_render_visibility(self):
        profile=self.circle();solid=extrusion.save(self.doc,[(profile,'')],{},dict(extrusion.DEFAULTS))
        profile.Visibility=True;solid.Visibility=True
        hidden=self.circle();hidden.Visibility=False
        old=list(self.doc.Objects);before=self.render_visibility(old)
        task=sketch_task.show();task.choose('XY Plane');self.dialog(QtWidgets.QDialogButtonBox.Ok)
        self.assertEqual(self.render_visibility(old),before)
        self.assertTrue(Gui.activeDocument().getInEdit().Object==task.result)
        self.assertTrue(task.result.ViewObject.HideDependent)  # No preference/property rewriting.
        self.eye(solid);self.assertFalse(solid.Visibility)
        self.assertTrue(self.owner.ViewObject.LinkVisibility)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle()
        expected=dict(before);expected[solid.Name]=(False,before[solid.Name][1])
        self.assertEqual(self.render_visibility(old),expected)
        self.doc.undo();settle();self.assertEqual(self.render_visibility(old),before)

    def test_existing_sketch_preserves_hidden_support_links_and_visible_dependents(self):
        support=self.owner.newObject('Part::Feature','HiddenSupport');support.Shape=Part.makeBox(12,12,2)
        linked=self.owner.newObject('Part::Feature','HiddenReference');linked.Shape=Part.makeBox(2,2,2,App.Vector(20,0,0))
        profile=self.circle();profile.AttachmentSupport=(support,['Face6']);profile.MapMode='FlatFace'
        profile.addExternal(linked.Name,'Edge1');self.doc.recompute()
        solid=extrusion.save(self.doc,[(profile,'')],{},dict(extrusion.DEFAULTS))
        support.Visibility=False;linked.Visibility=False;solid.Visibility=True
        old=[o for o in self.doc.Objects if o!=profile];before=self.render_visibility(old)
        editing.edit_feature(self.doc,profile);settle()
        self.assertEqual(self.render_visibility(old),before)
        self.assertTrue(profile.ViewObject.ShowSupport);self.assertTrue(profile.ViewObject.ShowLinks)
        self.eye(solid);self.assertFalse(solid.Visibility)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle()
        expected=dict(before);expected[solid.Name]=(False,before[solid.Name][1])
        self.assertEqual(self.render_visibility(old),expected)

    def test_external_sketch_preserves_source_and_host_render_visibility(self):
        folder=Path(os.environ['PLUS_TEST_DIR'])/'sketch-visibility-external';folder.mkdir(exist_ok=True)
        document.save_document(self.doc,folder/'Assembly.cadprt')
        source=document.new_document('SketchVisibilitySource');owner=document.validate(source).Definitions[0]
        document.save_document(source,folder/'Source.cadprt');external.import_file(self.doc,source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc,owner);self.owner=owner
        profile=self.circle();solid=extrusion.save(self.doc,[(profile,'')],{},dict(extrusion.DEFAULTS))
        profile.Visibility=False;solid.Visibility=True
        old=list(source.Objects);before=self.render_visibility(old);host_before=self.render_visibility(self.doc.Objects)
        task=sketch_task.show();task.choose('XY Plane');self.dialog(QtWidgets.QDialogButtonBox.Ok)
        self.assertEqual(self.render_visibility(old),before)
        self.assertEqual(self.render_visibility(self.doc.Objects),host_before)
        self.eye(solid);self.assertFalse(solid.Visibility);self.eye(solid);self.assertTrue(solid.Visibility)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle()
        self.assertEqual(self.render_visibility(old),before)
        self.assertEqual(self.render_visibility(self.doc.Objects),host_before)

    def test_classic_sketch_keeps_native_visibility_automation(self):
        classic=App.newDocument('ClassicVisibility');body=classic.addObject('PartDesign::Body','Body')
        sketch=body.newObject('Sketcher::SketchObject','Sketch')
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False)
        pad=body.newObject('PartDesign::Pad','Pad');pad.Profile=sketch;pad.Length=5;classic.recompute()
        sketch.Visibility=False;pad.Visibility=True;settle()
        before=self.render_visibility([body,pad])
        Gui.activeDocument().setEdit(sketch.Name);settle()
        self.assertTrue(sketch.ViewObject.HideDependent)
        self.assertFalse(pad.Visibility)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle()
        self.assertEqual(self.render_visibility([body,pad]),before)


class TestSketchCoordinateVisibility(unittest.TestCase):
    setUp = TestDesignInteractions.setUp
    dialog = TestDesignInteractions.dialog
    circle = TestDesignInteractions.circle
    eye = TestDesignInteractions.eye

    def tearDown(self):
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit();settle()
        TestDesignInteractions.tearDown(self)

    def frame(self, owner=None):
        origin=(owner or self.owner).Origin
        return [origin,*origin.OriginFeatures]

    def switches(self, objects):
        return {o.Name:o.ViewObject.SwitchNode.whichChild.getValue() for o in objects}

    def assert_hidden(self, objects):
        self.assertTrue(all(value==-1 for value in self.switches(objects).values()),self.switches(objects))
        for obj in self.frame():self.assertFalse(panel.history_visible(self.owner,obj))

    def leave(self):
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle()

    def test_existing_default_mixed_and_hidden_restore_without_property_edits(self):
        sketch=self.circle()
        for mode in ('default','mixed','hidden'):
            with self.subTest(mode=mode):
                for index,obj in enumerate(self.frame()):obj.Visibility=mode=='default' or (mode=='mixed' and index%2==0)
                flags={o.Name:bool(o.Visibility) for o in self.frame()};before=self.switches(self.frame())
                undo=self.doc.UndoCount
                Gui.activeDocument().setEdit(sketch.Name);settle()
                self.assert_hidden(self.frame())
                self.assertEqual({o.Name:bool(o.Visibility) for o in self.frame()},flags)
                self.doc.recompute();self.panel.refresh();settle();self.assert_hidden(self.frame())
                self.leave();self.assertEqual(self.switches(self.frame()),before)
                self.assertEqual(self.doc.UndoCount,undo)

    def test_mask_does_not_dirty_document_or_join_native_transaction(self):
        from freecad_plus.sketch_visibility import Drawing
        sketch=self.circle();editing.edit_feature(self.doc,sketch);settle()
        self.panel._restore_sketch_coordinates()
        before=self.switches(self.frame());undo=self.doc.UndoCount
        pending=self.doc.HasPendingTransaction;transaction=App.getActiveTransaction()
        Gui.activeDocument().Modified=False
        drawing=Drawing(self.owner,sketch,self.panel._current())
        self.assertTrue(all(value==-1 for value in self.switches(self.frame()).values()))
        drawing.apply();drawing.restore()
        self.assertEqual(self.switches(self.frame()),before)
        self.assertFalse(Gui.activeDocument().Modified)
        self.assertEqual(self.doc.UndoCount,undo);self.assertEqual(self.doc.HasPendingTransaction,pending)
        self.assertEqual(App.getActiveTransaction(),transaction)
        self.leave()

    def test_new_sketch_plane_selection_then_drawing_and_undo(self):
        before=self.switches(self.frame());flags={o.Name:o.Visibility for o in self.frame()}
        self.panel.tabs.setCurrentIndex(1)
        task=sketch_task.show();settle()
        self.assertTrue(all(o.ViewObject.isVisible() for o in self.frame() if o.TypeId=='App::Plane'))
        task.choose('XY Plane');self.dialog(QtWidgets.QDialogButtonBox.Ok)
        self.assert_hidden(self.frame());self.assertEqual(self.panel.tabs.currentIndex(),2)
        self.leave();self.assertEqual(self.switches(self.frame()),before)
        self.assertEqual(self.panel.tabs.currentIndex(),1)
        name=task.result.Name;self.doc.undo();settle();self.assertIsNone(self.doc.getObject(name))
        self.assertEqual({o.Name:o.Visibility for o in self.frame()},flags)
        self.doc.redo();settle();self.assertIsNotNone(self.doc.getObject(name))
        self.assertEqual(self.switches(self.frame()),before)

    def test_individual_eye_accept_abort_and_undo_redo(self):
        sketch=self.circle();axis=next(o for o in self.frame() if getattr(o,'Role','')=='X_Axis')
        editing.edit_feature(self.doc,sketch);settle();self.assert_hidden(self.frame())
        self.eye(axis);self.assertTrue(axis.ViewObject.isVisible())
        self.assertTrue(panel.history_visible(self.owner,axis))
        self.assertTrue(all(not o.ViewObject.isVisible() for o in self.frame()[1:] if o!=axis))
        self.eye(axis);self.assertFalse(axis.Visibility)
        self.leave();self.assertFalse(axis.Visibility)
        self.doc.undo();settle();self.assertTrue(axis.Visibility);self.assertTrue(axis.ViewObject.isVisible())
        self.doc.redo();settle();self.assertFalse(axis.Visibility)
        editing.edit_feature(self.doc,sketch);settle();self.eye(axis);self.assertTrue(axis.Visibility)
        App.closeActiveTransaction(True);settle()
        self.assertFalse(axis.Visibility)
        self.leave();self.assertFalse(axis.Visibility)

    def test_save_during_edit_reopens_persistent_visibility(self):
        sketch=self.circle();self.frame()[2].Visibility=False
        flags={o.Name:bool(o.Visibility) for o in self.frame()}
        filename=Path(os.environ['PLUS_TEST_DIR'])/'Coordinates.cadprt'
        document.save_document(self.doc,filename)
        editing.edit_feature(self.doc,sketch);settle();self.assert_hidden(self.frame())
        # Plus Save guards unfinished operations; the native save API must also
        # serialize persistent flags if invoked during native sketch editing.
        self.doc.save();settle();self.assert_hidden(self.frame())
        self.leave();App.closeDocument(self.doc.Name);settle()
        self.doc=App.openDocument(str(filename));self.owner=document.validate(self.doc).Definitions[0];settle()
        self.assertEqual({o.Name:bool(o.Visibility) for o in self.frame()},flags)
        for obj in self.frame():self.assertEqual(obj.ViewObject.isVisible(),flags[obj.Name])

    def test_body_owned_sketch_and_dispose_restore(self):
        body=self.owner.newObject('PartDesign::Body','Body');sketch=body.newObject('Sketcher::SketchObject','Sketch')
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False);self.doc.recompute()
        objects=self.frame()+self.frame(body);before=self.switches(objects)
        editing.edit_feature(self.doc,sketch);settle();self.assert_hidden(objects)
        self.panel.dispose();self.assertEqual(self.switches(objects),before)
        self.leave();self.panel=panel.show_panel();settle()

    def test_external_source_frame_and_host_context_cleanup(self):
        folder=Path(os.environ['PLUS_TEST_DIR'])/'coordinate-external';folder.mkdir(exist_ok=True)
        document.save_document(self.doc,folder/'Host.cadprt');host=self.owner
        source=document.new_document('CoordinateSource');owner=document.validate(source).Definitions[0]
        document.save_document(source,folder/'Source.cadprt');external.import_file(self.doc,source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc,owner);self.owner=owner
        sketch=self.circle();source.recompute();objects=self.frame();before=self.switches(objects)
        host_before=self.switches(self.frame(host))
        editing.edit_feature(self.doc,sketch);settle();self.assert_hidden(objects)
        self.assertEqual(self.switches(self.frame(host)),host_before)
        self.leave();self.assertEqual(self.switches(objects),before)
        editing.edit_feature(self.doc,sketch);settle();self.assert_hidden(objects)
        App.closeDocument(self.doc.Name);settle()
        self.assertIsNone(self.panel._sketch_drawing)
        self.assertEqual(self.switches(objects),before)


class TestSketchExitFit(unittest.TestCase):
    setUp = TestDesignInteractions.setUp
    tearDown = TestSketchCoordinateVisibility.tearDown
    dialog = TestDesignInteractions.dialog
    circle = TestDesignInteractions.circle

    def rectangle(self, sketch):
        points=[(-65,-35),(75,-35),(75,45),(-65,45)]
        for index,p in enumerate(points):
            q=points[(index+1)%4]
            sketch.addGeometry(Part.LineSegment(App.Vector(*p,0),App.Vector(*q,0)),False)
        sketch.Document.recompute()
        return [App.Vector(*p,0) for p in points]

    def camera(self):
        view=Gui.activeDocument().activeView();view.setAnimationEnabled(False);view.viewTop()
        view.getCameraNode().height.setValue(40)
        return view

    def assert_framed(self, view, points):
        widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        for point in points:
            screen=view.getPointOnScreen(point)
            self.assertTrue(0<=screen[0]<widget.width()*ratio and 0<=screen[1]<widget.height()*ratio,
                            (point,screen,widget.size()))

    def test_existing_native_exit_routes_preserve_orientation_visibility_and_selection(self):
        sketch=modeling.new_sketch(self.doc);points=self.rectangle(sketch)
        solid=self.owner.newObject('Part::Feature','VisibleSolid');solid.Shape=Part.makeBox(10,10,10,App.Vector(120,0,0))
        self.doc.recompute();view=self.camera()
        for exit_kind in ('command','close','reset'):
            with self.subTest(exit=exit_kind):
                view.getCameraNode().height.setValue(40)
                if exit_kind=='close':view.viewAxonometric()
                rotation=view.getCameraOrientation()
                flags={o.Name:o.Visibility for o in [solid,self.owner.Origin,*self.owner.Origin.OriginFeatures]}
                self.panel.tabs.setCurrentIndex(1);editing.edit_feature(self.doc,sketch);settle()
                view.getCameraNode().height.setValue(150)
                if exit_kind=='command':Gui.runCommand('Sketcher_LeaveSketch')
                elif exit_kind=='close':
                    button=next(box.button(QtWidgets.QDialogButtonBox.Close) for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
                                if box.isVisible() and box.button(QtWidgets.QDialogButtonBox.Close))
                    button.click()
                else:Gui.activeDocument().resetEdit()
                App.closeActiveTransaction()
                undo=self.doc.UndoCount;modified=Gui.activeDocument().Modified
                selection=Gui.Selection.getSelection()
                settle();self.assert_framed(view,points+[App.Vector(130,10,10)])
                self.assertTrue(view.getCameraOrientation().isSame(rotation,1e-7))
                self.assertEqual({o.Name:self.doc.getObject(o.Name).Visibility for o in [solid,self.owner.Origin,*self.owner.Origin.OriginFeatures]},flags)
                self.assertEqual(self.panel.tabs.currentIndex(),1)
                self.assertEqual(self.doc.UndoCount,undo);self.assertEqual(Gui.activeDocument().Modified,modified)
                self.assertEqual(Gui.Selection.getSelection(),selection)

    def test_new_sketch_exit_fits_and_creation_still_undoes(self):
        view=self.camera();task=sketch_task.show();task.choose('XY Plane')
        self.dialog(QtWidgets.QDialogButtonBox.Ok);points=self.rectangle(task.result)
        view.getCameraNode().height.setValue(150)
        Gui.runCommand('Sketcher_LeaveSketch');App.closeActiveTransaction();settle()
        self.assert_framed(view,points)
        name=task.result.Name;self.doc.undo();settle();self.assertIsNone(self.doc.getObject(name))
        self.doc.redo();settle();self.assertIsNotNone(self.doc.getObject(name))

    def test_empty_sketch_and_cancelled_placement_do_not_fit(self):
        view=self.camera();before=view.getCameraNode().position.getValue().getValue()
        task=sketch_task.show();task.reject();settle()
        self.assertAlmostEqual(view.getCameraNode().height.getValue(),40)
        self.assertEqual(view.getCameraNode().position.getValue().getValue(),before)
        sketch=modeling.new_sketch(self.doc);editing.edit_feature(self.doc,sketch);settle()
        view.getCameraNode().height.setValue(150)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle()
        self.assertAlmostEqual(view.getCameraNode().height.getValue(),40)

    def test_new_editor_cancels_queued_exit_fit(self):
        sketch=modeling.new_sketch(self.doc);self.rectangle(sketch);other=self.circle();view=self.camera()
        editing.edit_feature(self.doc,sketch);settle()
        Gui.activeDocument().resetEdit();App.closeActiveTransaction()
        editing.edit_feature(self.doc,other)
        view.getCameraNode().height.setValue(73);settle()
        self.assertEqual(Gui.activeDocument().getInEdit().Object,other)
        self.assertAlmostEqual(view.getCameraNode().height.getValue(),73)

    def test_deleted_sketch_and_closed_document_skip_queued_fit(self):
        sketch=modeling.new_sketch(self.doc);self.rectangle(sketch);view=self.camera()
        editing.edit_feature(self.doc,sketch);settle()
        Gui.activeDocument().resetEdit();App.closeActiveTransaction()
        self.doc.removeObject(sketch.Name);self.doc.recompute();self.doc.commitTransaction()
        view.getCameraNode().height.setValue(63);settle()
        self.assertAlmostEqual(view.getCameraNode().height.getValue(),63)
        sketch=self.circle();editing.edit_feature(self.doc,sketch);settle()
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();App.closeDocument(self.doc.Name)
        other=document.new_document('OtherView');other_view=Gui.activeDocument().activeView()
        other_view.getCameraNode().height.setValue(81);settle()
        self.assertAlmostEqual(other_view.getCameraNode().height.getValue(),81)

    def test_body_owned_sketch_fits(self):
        body=self.owner.newObject('PartDesign::Body','Body');sketch=body.newObject('Sketcher::SketchObject','Sketch')
        points=self.rectangle(sketch);view=self.camera()
        editing.edit_feature(self.doc,sketch);settle()
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle();self.assert_framed(view,points)

    def test_external_source_fits_host_view(self):
        folder=Path(os.environ['PLUS_TEST_DIR'])/'fit-external';folder.mkdir(exist_ok=True)
        document.save_document(self.doc,folder/'Host.cadprt')
        source=document.new_document('FitSource');owner=document.validate(source).Definitions[0]
        document.save_document(source,folder/'Source.cadprt');external.import_file(self.doc,source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc,owner);self.owner=owner
        sketch=modeling.new_sketch(self.doc);points=self.rectangle(sketch);view=self.camera()
        editing.edit_feature(self.doc,sketch);settle()
        Gui.getDocument(self.doc.Name).resetEdit();App.closeActiveTransaction();settle()
        self.assert_framed(view,points);self.assertEqual(sketch.Document,source)


class TestSketchCreationAndTaskTabs(unittest.TestCase):
    setUp = TestDesignInteractions.setUp
    tearDown = TestDesignInteractions.tearDown
    dialog = TestDesignInteractions.dialog
    circle = TestDesignInteractions.circle

    def draw(self, command, points, first_value=None):
        view=Gui.activeDocument().activeView();widget=view.graphicsView().viewport()
        Gui.runCommand(command);settle()
        for index,(x,y) in enumerate(points):
            p=view.getPointOnScreen(App.Vector(x,y,0));ratio=widget.devicePixelRatioF()
            pos=QtCore.QPoint(round(p[0]/ratio),widget.height()-1-round(p[1]/ratio))
            event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(pos),
                QtCore.QPointF(widget.mapToGlobal(pos)),QtCore.Qt.NoButton,QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget,event);settle()
            QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,pos);settle()
            if index==0 and first_value is not None:
                field=QtWidgets.QApplication.focusWidget()
                self.assertTrue(field.inherits('Gui::QuantitySpinBox'),field.metaObject().className())
                field.selectAll();QtTest.QTest.keyClicks(field,str(first_value))
                QtTest.QTest.keyClick(field,QtCore.Qt.Key_Tab);settle()
        QtTest.QTest.keyClick(widget,QtCore.Qt.Key_Escape);settle()

    def test_mouse_only_tools_do_not_dimension(self):
        sketch=modeling.new_sketch(self.doc);self.doc.recompute()
        modeling._enter_editor(self.doc,self.owner,(document.validate(self.doc).Group[0],),sketch);settle()
        view=Gui.activeDocument().activeView();view.setAnimationEnabled(False);view.viewTop()
        view.getCameraNode().height.setValue(100);settle()
        cases=[('Sketcher_CreateRectangle',[(-18,-10),(14,11)],4),
               ('Sketcher_CreateCircle',[(26,22),(31,22)],1),
               ('Sketcher_CreateLine',[(-30,23),(-15,23)],1),
               ('Sketcher_CreateArc',[(25,-20),(32,-20),(25,-13)],1)]
        dimensional={'Distance','DistanceX','DistanceY','Radius','Diameter','Angle','AngleViaPoint'}
        for command,points,count in cases:
            with self.subTest(tool=command):
                before=sketch.GeometryCount;self.draw(command,points)
                self.assertEqual(sketch.GeometryCount,before+count)
                self.assertFalse([c.Type for c in sketch.Constraints if c.Type in dimensional])
        self.assertGreaterEqual(sum(c.Type=='Coincident' for c in sketch.Constraints),4)
        self.assertGreaterEqual(sum(c.Type=='Horizontal' for c in sketch.Constraints),3)
        # Explicit dimensions remain valid and undoable, and survive edit entry.
        import Sketcher
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();self.doc.recompute()
        with document.transaction(self.doc,'Explicit width'):
            sketch.addConstraint(Sketcher.Constraint('Distance',0,30.))
        self.doc.undo();self.assertFalse([c.Type for c in sketch.Constraints if c.Type in dimensional])
        self.doc.redo()
        expected=list(sketch.Constraints);editing.edit_feature(self.doc,sketch);settle()
        self.assertEqual([c.Type for c in sketch.Constraints],[c.Type for c in expected])
        Gui.activeDocument().resetEdit();App.closeActiveTransaction()

    def test_signal_blocked_values_do_not_escape_on_focus_leave(self):
        form=QtWidgets.QWidget();layout=QtWidgets.QVBoxLayout(form)
        field=Gui.UiLoader().createWidget('Gui::QuantitySpinBox');other=QtWidgets.QLineEdit()
        field.setProperty('unit','mm');layout.addWidget(field);layout.addWidget(other)
        values=[];callback=lambda value:values.append(value)
        QtCore.QObject.connect(field,QtCore.SIGNAL('valueChanged(double)'),callback)
        form.show();form.activateWindow();QtWidgets.QApplication.setActiveWindow(form);settle()
        try:
            field.setFocus();settle()
            for value in (12.1234,18.6543,22.5555):
                with QtCore.QSignalBlocker(field):field.setProperty('rawValue',value)
            other.setFocus();settle();self.assertEqual(values,[])
            field.setFocus();field.selectAll();QtTest.QTest.keyClicks(field,'37');settle()
            self.assertEqual(values,[]);other.setFocus();settle();self.assertEqual(values,[37.])
        finally:
            QtCore.QObject.disconnect(field,QtCore.SIGNAL('valueChanged(double)'),callback);form.close()

    def test_deliberate_onview_entry_still_adds_dimension(self):
        sketch=modeling.new_sketch(self.doc);self.doc.recompute()
        modeling._enter_editor(self.doc,self.owner,(document.validate(self.doc).Group[0],),sketch);settle()
        view=Gui.activeDocument().activeView();view.setAnimationEnabled(False);view.viewTop()
        view.getCameraNode().height.setValue(80);settle()
        self.draw('Sketcher_CreateRectangle',[(-18,-10),(14,11)],first_value=25)
        dimensions=[c for c in sketch.Constraints if c.Type in ('Distance','DistanceX','DistanceY')]
        self.assertEqual(len(dimensions),1);self.assertAlmostEqual(dimensions[0].Value,25.)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle()

    def test_custom_tasks_restore_each_previous_tab_and_allow_browsing(self):
        profile=self.circle()
        for previous in range(3):
            for show in (sketch_task.show,plane_task.show,extrude_task.show):
                with self.subTest(tab=previous,task=show.__module__):
                    Gui.Selection.clearSelection();Gui.Selection.addSelection(profile)
                    self.panel.tabs.setCurrentIndex(previous);task=show();settle()
                    self.assertEqual(self.panel.tabs.currentIndex(),2)
                    self.panel.tabs.setCurrentIndex(0);self.panel.refresh();settle()
                    self.assertEqual(self.panel.tabs.currentIndex(),0)
                    task.reject();settle();self.assertEqual(self.panel.tabs.currentIndex(),previous)

    def test_sketch_handoff_and_existing_native_edit_restore_original_tab(self):
        self.panel.tabs.setCurrentIndex(1);task=sketch_task.show();task.choose('XY Plane')
        self.assertEqual(self.panel.tabs.currentIndex(),2)
        self.dialog(QtWidgets.QDialogButtonBox.Ok)
        sketch=task.result;self.assertEqual(Gui.activeDocument().getInEdit().Object,sketch)
        self.assertEqual(self.panel.tabs.currentIndex(),2)
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();self.doc.recompute();settle()
        self.assertEqual(self.panel.tabs.currentIndex(),1)
        self.panel.tabs.setCurrentIndex(0);editing.edit_feature(self.doc,sketch);settle()
        self.assertEqual(self.panel.tabs.currentIndex(),2)
        Gui.activeDocument().resetEdit();App.closeActiveTransaction();settle()
        self.assertEqual(self.panel.tabs.currentIndex(),0)

    def test_extrude_accept_edit_and_native_datums(self):
        profile=self.circle();Gui.Selection.clearSelection();Gui.Selection.addSelection(profile)
        self.panel.tabs.setCurrentIndex(1);task=extrude_task.show();settle()
        self.assertEqual(self.panel.tabs.currentIndex(),2);self.assertTrue(task.accept())
        self.assertEqual(self.panel.tabs.currentIndex(),1)
        task=editing.edit_feature(self.doc,task.result);settle();self.assertEqual(self.panel.tabs.currentIndex(),2)
        task.reject();self.assertEqual(self.panel.tabs.currentIndex(),1)
        for kind in ('Line','Point'):
            idle_tasks.create_datum(kind);settle();self.assertEqual(self.panel.tabs.currentIndex(),2)
            self.dialog(QtWidgets.QDialogButtonBox.Cancel);self.assertEqual(self.panel.tabs.currentIndex(),1)

    def test_context_close_and_failed_sketch_handoff_restore(self):
        self.panel.tabs.setCurrentIndex(0);task=plane_task.show();editing.edit_file(self.doc);settle()
        self.assertTrue(task.closed);self.assertEqual(self.panel.tabs.currentIndex(),0)
        editing.edit((document.validate(self.doc).Group[0],));self.panel.tabs.setCurrentIndex(1)
        task=sketch_task.show();task.choose('XY Plane')
        original=modeling._enter_editor
        def fail(*args):raise ValueError('Expected test entry failure')
        modeling._enter_editor=fail
        try:self.assertTrue(task.accept());settle();self.assertEqual(self.panel.tabs.currentIndex(),1)
        finally:modeling._enter_editor=original
        task=plane_task.show();App.closeDocument(self.doc.Name);settle()
        self.assertTrue(task.closed);self.assertEqual(self.panel.tabs.currentIndex(),1)

    def test_external_native_task_restores_host_tab(self):
        folder=Path(os.environ['PLUS_TEST_DIR'])/'tabs-external';folder.mkdir(exist_ok=True)
        document.save_document(self.doc,folder/'Host.cadprt')
        source=document.new_document('TabSource');owner=document.validate(source).Definitions[0]
        document.save_document(source,folder/'Source.cadprt');external.import_file(self.doc,source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc,owner)
        sketch=self.circle();source.recompute();self.panel.tabs.setCurrentIndex(1)
        editing.edit_feature(self.doc,sketch);settle();self.assertEqual(self.panel.tabs.currentIndex(),2)
        Gui.getDocument(self.doc.Name).resetEdit();App.closeActiveTransaction();settle()
        self.assertEqual(self.panel.tabs.currentIndex(),1)

    def test_part_creation_dialog_without_native_editor(self):
        Gui.activateWorkbench('PartWorkbench');self.panel.tabs.setCurrentIndex(1)
        Gui.runCommand('Part_Primitives');settle()
        self.assertTrue(Gui.Control.activeDialog());self.assertIsNone(Gui.activeDocument().getInEdit())
        self.assertEqual(self.panel.tabs.currentIndex(),2)
        self.panel.tabs.setCurrentIndex(0);self.panel.refresh();settle()
        self.assertEqual(self.panel.tabs.currentIndex(),0)
        self.dialog(QtWidgets.QDialogButtonBox.Close);settle()
        self.assertEqual(self.panel.tabs.currentIndex(),1)
