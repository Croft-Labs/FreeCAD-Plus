# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native task, parent-frame placement, transient preview and persistence checks."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, external, hierarchy, movement, panel
import TestComponentPanel as fixtures
import TestComponentClipboard as clipboard_tests

settle = fixtures.settle

class TestComponentMove(unittest.TestCase):
    setUp = fixtures.TestComponentPanel.setUp
    rows = fixtures.TestComponentPanel.rows
    occurrence = fixtures.TestComponentPanel.occurrence
    click = fixtures.TestComponentPanel.click
    menu = clipboard_tests.TestComponentClipboard.menu

    def tearDown(self):
        if movement._active: movement._active.finish()
        fixtures.TestComponentPanel.tearDown(self)

    def row(self, path): return self.occurrence(path).data(0, panel._ROLE)

    def task(self, *paths):
        task = self.widget.move_rows([self.row(p) for p in paths]); settle()
        self.assertFalse(task.closed)
        for i, path in enumerate(paths):
            self.assertEqual(task.components.item(i).text(),self.row(path).label)
        return task

    def inputs(self, task, axis=1, distance=6, reverse=False):
        task.direction.setCurrentIndex(axis); task.distance.setProperty('rawValue', float(distance))
        task.reverse.setChecked(reverse); settle()

    def test_menu_preview_apply_ok_atomic_undo_and_save(self):
        before = {o.Name:o.ID for o in self.doc.Objects}; undo = self.doc.UndoCount
        self.click(1,self.occurrence((self.first,)))
        self.click(1,self.occurrence((self.second,)),modifier=QtCore.Qt.ControlModifier)
        self.menu(self.occurrence((self.first,)), 'Move Components')
        task = movement._active
        self.assertIsNotNone(task)
        self.assertEqual(task.workflow.count(),6)
        self.assertEqual(self.widget._context(self.doc,task.view),(None,()))
        self.inputs(task)
        self.assertIsNotNone(task.overlay,task.message.text())
        self.assertEqual(self.first.LinkPlacement.Base.x,0)
        self.assertEqual(self.second.LinkPlacement.Base.x,25)
        self.assertEqual(self.doc.UndoCount,undo)
        button=next(b for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
                    if box.isVisible() for b in box.buttons() if box.standardButton(b)==QtWidgets.QDialogButtonBox.Apply)
        QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton); settle()
        self.assertEqual(self.first.LinkPlacement.Base.x,6)
        self.assertEqual(self.second.LinkPlacement.Base.x,31)
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertEqual(len(task.paths),2)
        self.assertEqual(task.direction.currentIndex(),0)
        self.assertEqual(float(task.distance.property('rawValue')),0)
        self.assertFalse(task.reverse.isChecked())
        task.accept();settle()
        self.assertTrue(task.closed);self.assertEqual(self.doc.UndoCount,undo+1)
        self.doc.undo();self.doc.recompute();settle();self.assertEqual(self.first.LinkPlacement.Base.x,0)
        self.doc.redo();self.doc.recompute();settle();self.assertEqual(self.first.LinkPlacement.Base.x,6)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        document.save_document(self.doc,self.output/'Move.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':before,'first':self.first.Name,'second':self.second.Name,'pad':self.pad.Name}))

    def test_nested_rotated_parent_group_reverse_cancel_and_noop(self):
        sibling=hierarchy.add_instance(self.parent,self.child,App.Placement(App.Vector(4,2,0),App.Rotation(App.Vector(1,0,0),15)))
        hierarchy.move_instance(self.second,App.Placement(App.Vector(25,7,0),App.Rotation(App.Vector(0,0,1),90)));settle()
        original = App.Placement(sibling.LinkPlacement)
        task=self.task((self.second,self.nested),(self.second,sibling))
        self.assertEqual(editing.context_path(self.doc),(self.parent,(self.second,)))
        undo=self.doc.UndoCount
        self.inputs(task,2,3,True)
        self.assertIsNotNone(task.overlay,task.message.text())
        self.assertEqual(self.nested.LinkPlacement.Base.y,0)
        shown=task.overlay.getNumChildren()
        self.first.Visibility=False;settle()
        self.assertEqual(task.overlay.getNumChildren(),shown-2)
        self.first.Visibility=True;settle()
        self.assertEqual(task.overlay.getNumChildren(),shown)
        task.apply();settle()
        self.assertEqual(self.nested.LinkPlacement.Base.y,-3)
        self.assertEqual(sibling.LinkPlacement.Base.y,-1)
        self.assertTrue(sibling.LinkPlacement.Rotation.isSame(original.Rotation,1e-9))
        for top in (self.first,self.second):
            expected=hierarchy.world_placement(self.doc,(top,)).multVec(App.Vector(0,-3,0))
            self.assertLess((hierarchy.world_placement(self.doc,(top,self.nested)).Base-expected).Length,1e-8)
        task.apply();self.assertEqual(self.doc.UndoCount,undo+1)
        self.inputs(task,1,9);task.reject();settle()
        self.assertEqual(self.nested.LinkPlacement.Base.x,0)
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.doc.undo();self.doc.recompute();settle();self.assertEqual(self.nested.LinkPlacement.Base.y,0)

    def test_picked_direction_snapshot_in_rotated_frame_and_invalid_curve(self):
        hierarchy.move_instance(self.second,App.Placement(App.Vector(25,7,0),App.Rotation(App.Vector(0,0,1),90)));settle()
        task=self.task((self.second,self.nested))
        body=self.pad.getParentGeoFeatureGroup()
        prefix=hierarchy.subname((self.first,self.nested))+body.Name+'.'+self.pad.Name+'.'
        straight=next(i+1 for i,e in enumerate(self.pad.Shape.Edges) if isinstance(e.Curve,Part.Line))
        curve=next(i+1 for i,e in enumerate(self.pad.Shape.Edges) if isinstance(e.Curve,Part.Circle))
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.doc.Name,self.root.Name,prefix+'Edge'+str(straight))
        task.pick_direction();snap=App.Vector(task.direction_snapshot)
        self.assertAlmostEqual(abs(snap.z),1)
        self.inputs(task,4,4);self.assertIsNotNone(task.overlay,task.message.text())
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.doc.Name,self.root.Name,prefix+'Edge'+str(curve))
        with self.assertRaisesRegex(ValueError,'straight'):task.pick_direction()
        self.assertLess((task.direction_snapshot-snap).Length,1e-9)
        task.apply();self.assertAlmostEqual(abs(self.nested.LinkPlacement.Base.z),4)
        # A horizontal reference on a differently translated/rotated occurrence.
        edge=self.doc.addObject('PartDesign::Feature','ReferenceLine');self.parent.addObject(edge)
        edge.Shape=Part.makeLine(App.Vector(),App.Vector(5,0,0));self.doc.recompute();settle()
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.doc.Name,self.root.Name,hierarchy.subname((self.first,))+edge.Name+'.Edge1')
        task.pick_direction()
        self.assertLess((task.direction_snapshot-App.Vector(0,-1,0)).Length,1e-8)
        task.distance.setProperty('rawValue',2.0);task.apply()
        self.assertAlmostEqual(self.nested.LinkPlacement.Base.y,-2)
        axis=next(o for o in self.root.Origin.OriginFeatures if o.Role=='X_Axis')
        self.root.Origin.Visibility=True;axis.Visibility=True;settle()
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.doc.Name,self.root.Name,self.root.Origin.Name+'.'+axis.Name+'.')
        task.pick_direction()
        self.assertLess((task.direction_snapshot-App.Vector(0,-1,0)).Length,1e-8)
        axis.Visibility=False;settle()
        with self.assertRaisesRegex(ValueError,'visible'):task.pick_direction()

    def test_sibling_rejection_selection_remove_clear_and_method_reset(self):
        with self.assertRaisesRegex(ValueError,'siblings'):
            self.widget.move_rows([self.row((self.first,)),self.row((self.first,self.nested))])
        self.assertIsNone(movement._active)
        task=self.task((self.first,))
        before=list(task.paths)
        with self.assertRaisesRegex(ValueError,'siblings'):task.add_rows([self.row((self.second,self.nested))])
        self.assertEqual(task.paths,before)
        self.inputs(task)
        task.workflow.setCurrentIndex(2);settle()
        self.assertIsNone(task.overlay);self.assertEqual(task.paths,before)
        self.assertIn('awaits',task.message.text())
        task.workflow.setCurrentIndex(0)
        self.inputs(task)
        task.distance.setText('bad length');settle()
        self.assertIsNone(task.overlay)
        with self.assertRaisesRegex(ValueError,'valid'):task.apply()
        task.distance.setText('2 deg');settle()
        with self.assertRaisesRegex(ValueError,'valid'):task.apply()
        task.distance.setProperty('rawValue',0.0)
        self.click(1,self.occurrence((self.second,)));task.add_selected()
        self.assertEqual(len(task.paths),2)
        task.components.item(0).setSelected(True)
        QtTest.QTest.keyClick(task.components,QtCore.Qt.Key_Delete);self.assertEqual(len(task.paths),1)
        task.persistent.setChecked(False);self.inputs(task);task.apply();settle()
        self.assertEqual(task.paths,[]);self.assertEqual(Gui.Selection.getSelection(),[])
        self.assertEqual(self.second.LinkPlacement.Base.x,31)
        task.reject()

    def test_guards_rollback_and_lifecycle_cleanup(self):
        self.first.setPropertyStatus('LinkPlacement','ReadOnly')
        with self.assertRaisesRegex(ValueError,'read-only'):self.widget.move_rows([self.row((self.first,))])
        self.first.setPropertyStatus('LinkPlacement','-ReadOnly')
        self.first.setExpression('LinkPlacement.Base.x','3')
        with self.assertRaisesRegex(ValueError,'expression'):self.widget.move_rows([self.row((self.first,))])
        self.first.setExpression('LinkPlacement.Base.x',None)
        self.first.LinkPlacement=App.Placement();self.doc.recompute();settle()
        task=self.task((self.first,),(self.second,));self.inputs(task)
        undo=self.doc.UndoCount
        native_validate=document.validate
        failed_after_mutation=[]
        def validate_after_mutation(doc):
            if self.first.LinkPlacement.Base.x != 0:
                failed_after_mutation.append(True)
                raise ValueError('Controlled validation failure')
            return native_validate(doc)
        with patch.object(document,'validate',side_effect=validate_after_mutation):
            with self.assertRaisesRegex(ValueError,'Controlled'):task.apply()
        self.assertEqual(self.first.LinkPlacement.Base.x,0);self.assertEqual(self.second.LinkPlacement.Base.x,25)
        self.assertEqual(self.doc.UndoCount,undo)
        self.assertEqual(failed_after_mutation,[True])
        task.update_preview();self.assertIsNotNone(task.overlay)
        self.widget.close();settle();self.assertTrue(task.closed);self.assertIsNone(task.overlay)
        self.widget=panel.show_panel();settle()
        task=self.task((self.first,));self.inputs(task)
        other=document.new_document('OtherMoveFile');settle()
        self.assertTrue(task.closed);self.assertIsNone(task.overlay)
        self.assertEqual(self.first.LinkPlacement.Base.x,0)
        App.setActiveDocument(self.doc.Name);settle()
        task=self.task((self.first,));self.inputs(task)
        editing.edit((self.first,));settle()
        self.assertTrue(task.closed);self.assertIsNone(task.overlay)

    def test_external_parent_source_owned_save_and_standalone_reopen(self):
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        source=document.new_document('Hardware');source_root=document.validate(source);parent=source_root.Definitions[0]
        child=hierarchy.create_definition(source,'Screw');link=hierarchy.add_instance(parent,child)
        document.save_document(source,self.output/'Hardware.cadprt');external.import_file(self.doc,source)
        imported=hierarchy.add_instance(self.root,parent,App.Placement(App.Vector(60,0,0),App.Rotation(App.Vector(0,0,1),90)))
        document.save_document(self.doc)
        checksum=hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest()
        App.setActiveDocument(self.doc.Name);settle()
        task=self.task((imported,link));self.inputs(task,1,8)
        ids={o.Name:o.ID for o in source.Objects};undo=source.UndoCount
        task.apply();settle();self.assertEqual(source.UndoCount,undo+1)
        self.assertEqual(link.LinkPlacement.Base.x,8);task.reject()
        external.save_definition(parent)
        self.assertEqual(hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest(),checksum)
        (self.output/'expected.json').write_text(json.dumps({'uid':str(source.Uid),'ids':ids,'link':link.Name,'parent':parent.Name,'assembly_ids':{o.Name:o.ID for o in self.doc.Objects}}))


def verify_fresh_process(output):
    output=Path(output)
    folder=output/'test_menu_preview_apply_ok_atomic_undo_and_save'
    expected=json.loads((folder/'expected.json').read_text());doc=document.open_document(folder/'Move.cadprt')
    assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
    assert doc.getObject(expected['first']).LinkPlacement.Base.x==6
    assert doc.getObject(expected['second']).LinkPlacement.Base.x==31
    assert doc.getObject(expected['pad']).Length.Value==5
    App.closeDocument(doc.Name)
    folder=output/'test_external_parent_source_owned_save_and_standalone_reopen'
    expected=json.loads((folder/'expected.json').read_text())
    source=document.open_document(folder/'Hardware.cadprt')
    assert {o.Name:o.ID for o in source.Objects}==expected['ids']
    assert source.getObject(expected['link']).LinkPlacement.Base.x==8
    App.closeDocument(source.Name)
    doc=document.open_document(folder/'Assembly.cadprt')
    source=next(d for d in App.listDocuments().values() if str(d.Uid)==expected['uid'])
    assert source.getObject(expected['link']).LinkPlacement.Base.x==8
    assert {o.Name:o.ID for o in doc.Objects}==expected['assembly_ids']
    checksum=hashlib.sha256(Path(doc.FileName).read_bytes()).hexdigest()
    hierarchy.move_instance(source.getObject(expected['link']),App.Placement(App.Vector(9,0,0),App.Rotation()))
    external.save_definition(source.getObject(expected['parent']))
    assert hashlib.sha256(Path(doc.FileName).read_bytes()).hexdigest()==checksum
    App.closeDocument(doc.Name);App.closeDocument(source.Name)
    doc=document.open_document(folder/'Assembly.cadprt')
    source=next(d for d in App.listDocuments().values() if str(d.Uid)==expected['uid'])
    assert source.getObject(expected['link']).LinkPlacement.Base.x==9
    App.closeDocument(doc.Name);App.closeDocument(source.Name)
