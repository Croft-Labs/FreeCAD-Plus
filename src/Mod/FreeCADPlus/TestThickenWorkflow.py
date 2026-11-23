# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native offset, persistence, task lifecycle and Shell-entry regression checks."""
import math
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, extrusion, extrude_task, thicken, thicken_task, toolbar_layout, toolbars
from TestFeatureCenteredModeling import TestFeatureCenteredModeling


class TestThickenWorkflow(unittest.TestCase):
    setUp = TestFeatureCenteredModeling.setUp
    snapshot = TestFeatureCenteredModeling.snapshot

    def tearDown(self):
        if extrude_task._active:extrude_task._active.reject()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():Gui.activeDocument().resetEdit()
        if self.doc.HasPendingTransaction:self.doc.abortTransaction()
        TestFeatureCenteredModeling.tearDown(self)

    def sheet(self, shape=None):
        obj = self.owner.newObject('Part::Feature', 'Sheet')
        obj.Shape = shape if shape is not None else Part.makePlane(10, 8)
        self.doc.recompute();return obj

    def solid(self):
        body = self.owner.newObject('PartDesign::Body', 'Body')
        obj = body.newObject('PartDesign::Feature', 'Solid')
        obj.Shape = Part.makeBox(10, 8, 3, App.Vector(0, 0, -2))
        body.Tip = obj;self.doc.recompute();return obj

    def evaluate(self, sheet, links=None, **values):
        return thicken.evaluate(self.owner, [(sheet, '')], links or {}, dict(thicken.DEFAULTS, **values))

    def test_planar_directions_and_read_only_preview(self):
        sheet = self.sheet();before = self.snapshot()
        for direction, low, high in [('Along normal', 0, 2), ('Opposite normal', -2, 0), ('Symmetric', -1, 1)]:
            shape, tool, _ = self.evaluate(sheet, thickness=2, direction=direction)
            self.assertTrue(shape.isValid());self.assertEqual(len(shape.Solids), 1)
            self.assertAlmostEqual(shape.Volume, 160)
            self.assertAlmostEqual(shape.BoundBox.ZMin, low);self.assertAlmostEqual(shape.BoundBox.ZMax, high)
        self.assertEqual(self.snapshot(), before)

    def test_curved_sheet_and_connected_faces(self):
        curved = Part.makeLine(App.Vector(10,0,0), App.Vector(10,15,0)).revolve(App.Vector(), App.Vector(0,1,0), 270)
        sheet = self.sheet(curved)
        for join in ('Sharp', 'Rounded'):
            result, _, _ = self.evaluate(sheet, join=join)
            self.assertTrue(result.isValid());self.assertEqual(len(result.Solids), 1)
        curved_result = self.evaluate(sheet)[0]
        self.assertAlmostEqual(curved_result.Volume, 742.20126444, places=5)
        sheet.Shape = Part.makeShell(Part.makeBox(10,8,4).Faces[:2])
        self.doc.recompute()
        with self.assertRaises(ValueError):self.evaluate(sheet)
        sheet.Shape = Part.makeShell([Part.makeBox(10,8,4).Faces[i] for i in (0,2)])
        self.doc.recompute()
        result, _, _ = thicken.evaluate(self.owner, [(sheet,'Face1'),(sheet,'Face2')], {}, thicken.DEFAULTS)
        self.assertTrue(result.isValid());self.assertEqual(len(result.Solids), 1)

    def test_add_subtract_and_invalid_tool(self):
        sheet = self.sheet();target = self.solid();links = {'target':(target,'')}
        for mode, volume in [('Add',320),('Subtract',160)]:
            result, _, _ = self.evaluate(sheet, links, operation=mode, thickness=2)
            self.assertAlmostEqual(result.Volume, volume)
        sheet.Placement.Base.x = 50;self.doc.recompute()
        for mode in ('Add','Subtract'):
            with self.assertRaises(thicken.InvalidResult) as caught:self.evaluate(sheet, links, operation=mode)
            self.assertTrue(caught.exception.tool.isValid())

    def test_save_edit_undo_associativity_and_reopen(self):
        sheet = self.sheet()
        feature = thicken.save(self.doc, [(sheet,'')], {}, thicken.DEFAULTS)
        identity, name = feature.ID, feature.Name
        thicken.save(self.doc, [(sheet,'')], {}, dict(thicken.DEFAULTS, thickness=2), feature)
        self.assertEqual(feature.ID, identity);self.assertAlmostEqual(feature.Shape.Volume,160)
        self.doc.undo();self.doc.recompute();self.assertAlmostEqual(feature.Shape.Volume,80)
        self.doc.redo();self.doc.recompute();self.assertAlmostEqual(feature.Shape.Volume,160)
        sheet.Shape = Part.makePlane(20,8);self.doc.recompute();self.assertAlmostEqual(feature.Shape.Volume,320)
        order = document.history(self.doc,self.owner);self.assertLess(order.index(sheet),order.index(feature))
        path = self.output/'Thicken.cadprt';document.save_document(self.doc,path)
        App.closeDocument(self.doc.Name);self.doc = document.open_document(path)
        feature = self.doc.getObject(name);self.assertEqual(feature.ID,identity)
        feature.touch();self.doc.recompute();self.assertAlmostEqual(feature.Shape.Volume,320)

    def test_boolean_save_edit_keeps_predecessor(self):
        sheet = self.sheet();target = self.solid()
        feature = thicken.save(self.doc,[(sheet,'')],{'target':(target,'')},dict(thicken.DEFAULTS,operation='Add',thickness=2))
        self.assertEqual(feature.getParentGeoFeatureGroup(),target.getParentGeoFeatureGroup())
        thicken.save(self.doc,[(sheet,'')],{'target':(target,'')},dict(thicken.DEFAULTS,operation='Subtract'),feature)
        self.assertAlmostEqual(feature.Shape.Volume,160)
        self.assertEqual(thicken.references(feature)['target'][0],target)

    def test_invalid_inputs_and_sequential_edit_are_atomic(self):
        sheet = self.sheet();solid = self.solid();before = self.snapshot()
        for refs, values in [([(solid,'Face1')],{}), ([(sheet,'Edge1')],{}), ([(sheet,'')],{'thickness':0}),
                             ([(sheet,'')],{'thickness':float('nan')}), ([(sheet,'')],{'operation':'Subtract'})]:
            with self.assertRaises(ValueError):thicken.save(self.doc,refs,{},dict(thicken.DEFAULTS,**values))
        self.assertEqual(before,self.snapshot())
        feature = thicken.save(self.doc,[(sheet,'')],{},thicken.DEFAULTS);later = self.sheet()
        with self.assertRaises(ValueError):thicken.save(self.doc,[(later,'')],{},thicken.DEFAULTS,feature)
        self.assertAlmostEqual(feature.Shape.Volume,80)

    def test_task_create_edit_cancel_numeric_and_hidden_target(self):
        Gui.activateWorkbench('PartDesignWorkbench')
        sheet = self.sheet();target = self.solid();target.Visibility=False;before = self.snapshot()
        Gui.Selection.addSelection(sheet)
        task = thicken_task.show();QtTest.QTest.qWait(100)
        self.assertTrue(task.valid);self.assertEqual(task.refs,[(sheet,'')])
        task.modes['Add'].click();QtTest.QTest.qWait(100)
        self.assertEqual(task.links['target'][0],target)
        task.amount.setValue(2);task.commit_numbers();task.render()
        self.assertTrue(task.valid);self.assertIsNotNone(task.target_overlay)
        task.amount.setFocus();task.amount.selectAll()
        QtTest.QTest.keyClicks(task.amount.lineEdit(),'3');self.assertEqual(task.values[task.amount],2)
        task.normal.setFocus();QtTest.QTest.qWait(100);self.assertEqual(task.values[task.amount],3)
        task.reject();self.assertEqual(before,self.snapshot())
        Gui.Selection.addSelection(sheet);task = thicken_task.show();self.assertTrue(task.accept())
        feature = task.result;identity = feature.ID
        task = editing.edit_feature(self.doc,feature);self.assertEqual(task.refs,[(sheet,'')])
        task.amount.setValue(2);task.commit_numbers();self.assertTrue(task.accept())
        self.assertEqual(feature.ID,identity);self.assertAlmostEqual(feature.Shape.Volume,160)

    def test_sheet_face_collector_and_error_recovery(self):
        sheet = self.sheet();solid = self.solid()
        task = thicken_task.show()
        task.addSelection(self.doc.Name,solid.Name,'Face1');self.assertFalse(task.refs)
        self.assertIn('Shell',task.status.text())
        task.addSelection(self.doc.Name,sheet.Name,'Face1');self.assertTrue(task.valid)
        task.addSelection(self.doc.Name,sheet.Name,'Face1');self.assertFalse(task.refs)
        task.addSelection(self.doc.Name,sheet.Name,'');self.assertTrue(task.valid)
        task.modes['Subtract'].click();task.clear_reference('target')
        task.pick='profile';task.addSelection(self.doc.Name,sheet.Name,'Face1')
        self.assertEqual(task.pick,'target');self.assertFalse(task.target_ready())

    def test_shell_invalid_entry_and_valid_native_task(self):
        Gui.activateWorkbench('PartDesignWorkbench')
        # Sheet in the same native Body form as Extrude/Revolve Sheet outputs.
        body=self.owner.newObject('PartDesign::Body','Body')
        sheet=body.newObject('PartDesign::Feature','Sheet');sheet.Shape=Part.makePlane(10,8)
        body.Tip=sheet;self.doc.recompute();before=self.snapshot()
        Gui.activeDocument().activeView().setActiveObject('pdbody',body)
        unexpected=[]
        def dismiss_prompt():
            modal=QtWidgets.QApplication.activeModalWidget()
            if modal:
                unexpected.append(modal.windowTitle()+': '+ ' '.join(w.text() for w in modal.findChildren(QtWidgets.QLabel)))
                modal.reject()
        messages=[];original=thicken_task.show_error
        thicken_task.show_error=lambda title,message:messages.append((title,message))
        try:
            Gui.Selection.addSelection(sheet,'Face1')
            QtCore.QTimer.singleShot(200,dismiss_prompt);Gui.runCommand('PartDesign_Thickness')
        finally:thicken_task.show_error=original
        self.assertFalse(unexpected,unexpected)
        self.assertTrue(messages);self.assertIn('Thicken',messages[0][1])
        self.assertFalse(self.doc.HasPendingTransaction);self.assertFalse(Gui.Control.activeDialog())
        self.assertEqual(before,self.snapshot())
        Gui.Selection.clearSelection();target=self.solid()
        Gui.activeDocument().activeView().setActiveObject('pdbody',target.getParentGeoFeatureGroup())
        Gui.Selection.addSelection(target,'Face6')
        QtCore.QTimer.singleShot(200,dismiss_prompt)
        Gui.runCommand('PartDesign_Thickness');QtTest.QTest.qWait(250)
        self.assertFalse(unexpected,unexpected)
        self.assertTrue(Gui.Control.activeDialog());self.assertTrue(Gui.activeDocument().getInEdit())
        feature=target.getParentGeoFeatureGroup().Tip
        self.assertEqual(feature.TypeId,'PartDesign::Thickness');self.assertEqual(feature.Label,'Shell')
        Gui.activeDocument().resetEdit();self.doc.abortTransaction()

    def test_modeling_surface_layout_and_classic_native_access(self):
        from freecad_plus import ui_modes
        ui_modes.apply_modes();Gui.activateWorkbench('PartDesignWorkbench')
        ribbon=toolbars._controller;ribbon.tab='Modeling';ribbon.refresh()
        self.assertNotIn('Surface',[name for name,_ in toolbar_layout.DESIGN_TABS])
        entries=dict(toolbar_layout.MODELING)['Surface'];self.assertEqual(len(entries),7)
        for _,_,commands in entries:self.assertIsNotNone(Gui.Command.get(commands[0]))
        self.assertNotIn('SurfaceWorkbench',[owner for _,owner in ribbon._modes(Gui.listWorkbenches())])
        Gui.activateWorkbench('SurfaceWorkbench');ribbon.refresh()
        self.assertEqual(ribbon.tab,'Modeling');self.assertEqual(ribbon.mode_workbench,'PartDesignWorkbench')

    def test_shell_declined_editor_rolls_back_its_transaction(self):
        Gui.activateWorkbench('PartDesignWorkbench');target=self.solid()
        Gui.activeDocument().activeView().setActiveObject('pdbody',target.getParentGeoFeatureGroup())
        before=self.snapshot();original=Gui.getDocument
        class DeclinedEditor:
            def __init__(self,wrapped):self.wrapped=wrapped
            def __getattr__(self,name):return getattr(self.wrapped,name)
            def setEdit(self,*args):return False
        Gui.getDocument=lambda name:DeclinedEditor(original(name))
        try:
            Gui.Selection.addSelection(target,'Face6');Gui.runCommand('PartDesign_Thickness')
        finally:Gui.getDocument=original
        self.assertFalse(Gui.Control.activeDialog());self.assertFalse(self.doc.HasPendingTransaction)
        self.assertFalse(Gui.activeDocument().getInEdit());self.assertEqual(before,self.snapshot())
