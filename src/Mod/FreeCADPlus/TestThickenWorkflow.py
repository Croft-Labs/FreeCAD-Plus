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
        sheet=self.sheet();target=self.solid();before=self.snapshot()
        Gui.Selection.addSelection(sheet,'Face1');Gui.runCommand('PartDesign_Thickness')
        task=extrude_task._active
        self.assertTrue(Gui.Control.activeDialog());self.assertIn('Thicken',task.status.text())
        self.assertFalse(task.refs);self.assertFalse(self.doc.HasPendingTransaction)
        task.addSelection(self.doc.Name,target.Name,'Face6')
        self.assertTrue(task.valid,task.status.text());task.reject()
        self.assertEqual(before,self.snapshot())

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

    def test_shell_rejected_empty_task_has_no_transaction(self):
        Gui.activateWorkbench('PartDesignWorkbench');self.solid()
        before=self.snapshot();Gui.Selection.clearSelection();Gui.runCommand('PartDesign_Thickness')
        task=extrude_task._active
        self.assertFalse(task.accept());self.assertFalse(self.doc.HasPendingTransaction)
        task.reject();self.assertEqual(before,self.snapshot())

    def test_shell_selected_first_body_accept_and_undo(self):
        from TestComponentModeling import messages, accept_task
        Gui.activateWorkbench('PartDesignWorkbench')
        first=self.solid();second=self.solid();second.Placement.Base.x=20;self.doc.recompute()
        first_body=first.getParentGeoFeatureGroup();second_body=second.getParentGeoFeatureGroup()
        view=Gui.activeDocument().activeView();view.setActiveObject('pdbody',second_body)
        second_shape=second.Shape.copy();second_group=list(second_body.Group)
        Gui.Selection.clearSelection();Gui.Selection.addSelection(first,'Face6')
        with messages() as errors:Gui.runCommand('PartDesign_Thickness');QtTest.QTest.qWait(100)
        self.assertFalse(errors,errors);self.assertTrue(Gui.Control.activeDialog())
        task=extrude_task._active
        self.assertEqual(task.refs,[(first,'Face6')])
        self.assertEqual(view.getActiveObject('pdbody'),second_body)
        accept_task();self.assertFalse(Gui.Control.activeDialog());self.assertFalse(self.doc.HasPendingTransaction)
        feature=task.result;name=feature.Name
        self.assertEqual(feature.getParentGeoFeatureGroup(),first_body)
        self.assertTrue(feature.Shape.isValid());self.assertLess(feature.Shape.Volume,first.Shape.Volume)
        self.assertEqual(second_body.Tip,second);self.assertEqual(second_body.Group,second_group)
        self.assertAlmostEqual(second.Shape.Volume,second_shape.Volume)
        self.doc.undo();self.doc.recompute();self.assertIsNone(self.doc.getObject(name));self.assertEqual(first_body.Tip,first)
        self.doc.redo();self.doc.recompute();self.assertEqual(first_body.Tip.Name,name)
        document.save_document(self.doc,self.output/'TwoBodyShell.cadprt')

    def test_shell_selected_first_body_cancel_without_active_body(self):
        from TestComponentModeling import messages
        Gui.activateWorkbench('PartDesignWorkbench');first=self.solid();self.solid()
        view=Gui.activeDocument().activeView();view.setActiveObject('pdbody',None)
        before=self.snapshot();Gui.Selection.clearSelection();Gui.Selection.addSelection(first,'Face6')
        with messages() as errors:Gui.runCommand('PartDesign_Thickness');QtTest.QTest.qWait(100)
        self.assertFalse(errors,errors);self.assertTrue(Gui.Control.activeDialog())
        buttons=[box.button(QtWidgets.QDialogButtonBox.Cancel) for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)]
        button=next(b for b in buttons if b and b.isVisible());QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(100);self.assertEqual(before,self.snapshot())
        self.assertFalse(self.doc.HasPendingTransaction);self.assertIsNone(view.getActiveObject('pdbody'))

    def test_shell_empty_selection_never_uses_active_body(self):
        Gui.activateWorkbench('PartDesignWorkbench');first=self.solid();self.solid()
        Gui.activeDocument().activeView().setActiveObject('pdbody',first.getParentGeoFeatureGroup())
        Gui.Selection.clearSelection();before=self.snapshot();Gui.runCommand('PartDesign_Thickness')
        task=extrude_task._active
        self.assertFalse(task.refs);self.assertFalse(task.links)
        self.assertFalse(self.doc.HasPendingTransaction)
        task.reject();self.assertEqual(before,self.snapshot())

    def test_migrated_profile_commands_ignore_active_body_for_owned_sketches(self):
        from TestComponentModeling import messages
        Gui.activateWorkbench('PartDesignWorkbench');first=self.solid();second=self.solid()
        body=first.getParentGeoFeatureGroup();other=second.getParentGeoFeatureGroup()
        sketch=body.newObject('Sketcher::SketchObject','OlderSketch')
        sketch.addGeometry(Part.Circle(App.Vector(5,0,0),App.Vector(0,0,1),1),False)
        body.Tip=first;self.doc.recompute()
        view=Gui.activeDocument().activeView()
        for active in (other,None):
            view.setActiveObject('pdbody',active)
            for command,title in [('PartDesign_Pad','Extrude'),('PartDesign_Pocket','Extrude'),
                                  ('PartDesign_Revolution','Revolve'),('PartDesign_Groove','Revolve')]:
                before=self.snapshot();Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch)
                with messages() as errors:Gui.runCommand(command);QtTest.QTest.qWait(50)
                self.assertFalse(errors,errors);task=extrude_task._active
                self.assertIsNotNone(task);self.assertEqual(task.title,title);self.assertEqual(task.refs,[(sketch,'')])
                task.modes['Add'].click();self.assertNotIn('target',task.links)
                task.pick='target';task.addSelection(self.doc.Name,first.Name,'')
                self.assertEqual(task.links['target'][0],first)
                task.reject();self.assertEqual(before,self.snapshot());self.assertEqual(view.getActiveObject('pdbody'),active)
