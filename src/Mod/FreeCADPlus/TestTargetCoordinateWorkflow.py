# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native target guidance and structural coordinate frame regression checks."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, extrude_task, revolve_task, extrusion, modeling, panel
from TestFeatureCenteredModeling import TestFeatureCenteredModeling


class TestTargetCoordinateWorkflow(unittest.TestCase):
    circle = TestFeatureCenteredModeling.circle
    snapshot = TestFeatureCenteredModeling.snapshot

    def setUp(self):
        TestFeatureCenteredModeling.setUp(self)
        Gui.activateWorkbench('PartDesignWorkbench')

    def tearDown(self):
        if extrude_task._active:extrude_task._active.reject()
        TestFeatureCenteredModeling.tearDown(self)

    def target(self):
        return modeling.extrude_new_solid(self.doc,self.circle(6),6)

    def open(self,kind='extrude',feature=None,which=None):
        Gui.Selection.clearSelection()
        module=extrude_task if kind=='extrude' else revolve_task
        task=module.show(feature,which=which or ('Pad' if kind=='extrude' else 'Revolution'))
        QtTest.QTest.qWait(100)
        return task

    def test_hidden_sole_target_both_tools_both_operations_and_cancel(self):
        target=self.target();target.Visibility=False
        sketch=self.circle(2);before=self.snapshot()
        for kind in ('extrude','revolve'):
            for mode in ('Add','Subtract'):
                with self.subTest(kind=kind,mode=mode):
                    task=self.open(kind);task.refs=[(sketch,'')]
                    task.modes[mode].click();QtTest.QTest.qWait(80)
                    self.assertEqual(task.links['target'],(target,''))
                    self.assertEqual(task.refs,[(sketch,'')])
                    self.assertEqual(task.pick,'profile')
                    self.assertIn('automatically',task.target_hint.text())
                    self.assertFalse(target.Visibility)
                    self.assertIsNotNone(task.target_overlay)
                    self.assertEqual(task.target_candidates(),[target])
                    task.reject();self.assertEqual(self.snapshot(),before)

    def test_zero_and_multiple_targets_highlight_without_popup(self):
        sketch=self.circle()
        for count in (0,2):
            if count:
                self.target();self.target()
            for kind in ('extrude','revolve'):
                for mode in ('Add','Subtract'):
                    with self.subTest(count=count,kind=kind,mode=mode):
                        task=self.open(kind);task.modes[mode].click();QtTest.QTest.qWait(80)
                        self.assertNotIn('target',task.links)
                        self.assertEqual(task.pick,'target')
                        self.assertIn('#bd780b',task.fields['target'].styleSheet())
                        self.assertIn('No solid' if not count else 'Choose a target',task.target_hint.text())
                        self.assertIsNone(QtWidgets.QApplication.activeModalWidget())
                        task.pick='profile';task.addSelection(self.doc.Name,sketch.Name,'')
                        self.assertEqual(task.refs,[]);self.assertEqual(task.pick,'target')
                        task.automatic.setChecked(False)
                        self.assertFalse(task.accept());self.assertFalse(task.closed)
                        task.reject()

    def test_clear_does_not_reselect_until_operation_entry(self):
        target=self.target()
        for kind in ('extrude','revolve'):
            task=self.open(kind);task.modes['Add'].click()
            task.clear_reference('target');task.changed();task.render()
            self.assertNotIn('target',task.links)
            self.assertIn('#bd780b',task.fields['target'].styleSheet())
            task.modes['Subtract'].click()
            self.assertEqual(task.links['target'],(target,''))
            task.reject()

    def test_direct_subtractive_launch_and_existing_selection(self):
        first=self.target()
        for kind,which in (('extrude','Pocket'),('revolve','Groove')):
            task=self.open(kind,which=which)
            self.assertEqual(task.mode(),'Subtract')
            self.assertEqual(task.links['target'],(first,''));task.reject()
        second=self.target()
        for kind in ('extrude','revolve'):
            Gui.Selection.clearSelection();Gui.Selection.addSelection(first)
            task=(extrude_task if kind=='extrude' else revolve_task).show()
            task.modes['Subtract'].click();self.assertEqual(task.links['target'],(first,''))
            self.assertNotIn('automatically',task.target_hint.text())
            task.pick='target';task.addSelection(self.doc.Name,second.Name,'')
            self.assertEqual(task.links['target'],(second,''));task.reject()

    def test_edit_keeps_saved_predecessor_and_excludes_self_and_later(self):
        target=self.target();sketch=self.circle();sketch.Placement.Base.z=6;self.doc.recompute()
        feature=extrusion.save(self.doc,[(sketch,'')],{'target':(target,'')},dict(extrusion.DEFAULTS,operation='Add'))
        later=self.target()
        task=self.open(feature=feature)
        self.assertEqual(task.links['target'],(target,''))
        self.assertTrue(task.valid_target(target))
        self.assertNotIn(feature,task.target_candidates());self.assertNotIn(later,task.target_candidates())
        task.clear_reference('target');task.modes['Subtract'].click()
        self.assertNotIn('target',task.links);task.reject()

    def test_invalid_target_clears_and_deleted_target_closes_safely(self):
        target=self.target();shape=target.Shape.copy();task=self.open();task.modes['Add'].click()
        target.Shape=Part.Shape();task.changed()
        self.assertNotIn('target',task.links);self.assertIn('No solid',task.target_hint.text())
        target.Shape=shape;task.modes['Subtract'].click();self.assertIn('target',task.links)
        self.doc.removeObject(target.Name);QtTest.QTest.qWait(150)
        self.assertTrue(task.closed)

    def test_native_frame_deletion_is_atomic_and_reopen_keeps_ids(self):
        target=self.target();body=target.getParentGeoFeatureGroup()
        frames=[self.root.Origin,self.owner.Origin,body.Origin]
        before=self.snapshot()
        for origin in frames:
            for obj in [origin,*origin.OriginFeatures]:
                with self.subTest(obj=obj.Name):
                    with self.assertRaisesRegex(RuntimeError,'base coordinate system'):
                        self.doc.removeObject(obj.Name)
                    self.assertEqual(self.snapshot(),before)
        path=document.save_document(self.doc,self.output/'Protected.cadprt')
        ids={o.Name:o.ID for o in self.doc.Objects};App.closeDocument(self.doc.Name)
        self.doc=App.openDocument(str(path))
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        owner=document.validate(self.doc).Definitions[0]
        with self.assertRaisesRegex(RuntimeError,'base coordinate system'):
            self.doc.removeObject(owner.Origin.Name)

    def test_owner_cascade_undo_redo_abort_and_custom_datums(self):
        self.doc.openTransaction('Create component')
        owner=self.doc.addObject('App::Part','TemporaryPart')
        names=[owner.Name,owner.Origin.Name,*[o.Name for o in owner.Origin.OriginFeatures]]
        self.doc.commitTransaction();self.doc.undo()
        self.assertTrue(all(self.doc.getObject(name) is None for name in names))
        self.doc.redo();owner=self.doc.getObject(names[0])
        self.doc.openTransaction('Delete component');self.doc.removeObject(owner.Name);self.doc.commitTransaction()
        self.assertTrue(all(self.doc.getObject(name) is None for name in names))
        self.doc.undo();self.assertTrue(all(self.doc.getObject(name) is not None for name in names))
        self.doc.redo();self.assertTrue(all(self.doc.getObject(name) is None for name in names))
        self.doc.openTransaction('Abandoned component')
        owner=self.doc.addObject('App::Part','AbandonedPart');name=owner.Origin.Name
        self.doc.abortTransaction();self.assertIsNone(self.doc.getObject(name))
        for typeid in ('App::Plane','App::Line','App::Point','App::LocalCoordinateSystem'):
            obj=self.owner.newObject(typeid,'CustomDatum');name=obj.Name
            self.doc.removeObject(name);self.assertIsNone(self.doc.getObject(name))
        legacy=App.newDocument('LegacyFrame');part=legacy.addObject('App::Part','Part')
        name=part.Origin.Name;legacy.removeObject(name);self.assertIsNone(legacy.getObject(name))

    def test_history_delete_preserves_native_frame_and_visibility_controls(self):
        widget=panel.show_panel();widget.tabs.setCurrentIndex(2);widget.refresh()
        tree=widget.trees[2];tree.expandAll();QtTest.QTest.qWait(100)
        ids={o.Name:o.ID for o in self.doc.Objects}
        frame=self.owner.Origin
        for obj in [frame,*frame.OriginFeatures]:
            item=next(i for i in widget._maps[2].values() if i.data(0,panel._ROLE).ref==panel.identity(obj))
            tree.scrollToItem(item);QtTest.QTest.qWait(40)
            QtTest.QTest.mouseClick(tree.viewport(),QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,tree.visualItemRect(item).center())
            Gui.runCommand('Std_Delete',0);QtTest.QTest.qWait(50)
            self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        frame.Visibility=False;self.assertFalse(frame.Visibility)
        frame.Visibility=True;self.assertTrue(frame.Visibility)
