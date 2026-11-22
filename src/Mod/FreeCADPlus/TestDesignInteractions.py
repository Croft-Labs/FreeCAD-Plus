# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native acceptance of approved Design task and numeric interaction refinements."""
import os
import unittest
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtWidgets, QtTest
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
