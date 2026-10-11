# SPDX-License-Identifier: LGPL-2.1-or-later
"""Rotate acceptance in the native shared Move Components task."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, hierarchy, editing, external, movement, panel
import TestComponentMove as translate
import TestComponentPanel as fixtures
settle = fixtures.settle

class TestComponentRotate(unittest.TestCase):
    setUp = fixtures.TestComponentPanel.setUp
    tearDown = translate.TestComponentMove.tearDown
    rows = fixtures.TestComponentPanel.rows
    occurrence = fixtures.TestComponentPanel.occurrence
    row = translate.TestComponentMove.row
    task = translate.TestComponentMove.task

    def rotate(self, task, axis=3, angle=90, reverse=False):
        if task.workflow.currentIndex()!=1: task.workflow.setCurrentIndex(1)
        task.axis.setCurrentIndex(axis);task.angle.setProperty('rawValue',float(angle));task.reverse.setChecked(reverse);settle()

    def reference(self, name, shape):
        obj=self.doc.addObject('PartDesign::Feature',name);self.parent.addObject(obj)
        obj.Shape=shape;obj.Visibility=True;self.doc.recompute();settle();return obj

    def select(self, obj, element='', top=None):
        Gui.Selection.clearSelection()
        sub=hierarchy.subname((top or self.first,))+obj.Name+'.'+element
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,sub)

    def near(self, vector, expected):self.assertLess((vector-App.Vector(*expected)).Length,1e-7)

    def test_nonorigin_pivot_rigid_group_apply_undo_and_persistence(self):
        point=self.reference('PivotPoint',Part.Vertex(App.Vector(5,2,0)))
        task=self.task((self.first,),(self.second,));task.workflow.setCurrentIndex(1)
        self.select(point,'Vertex1');QtTest.QTest.mouseClick(task.pivot_pick,QtCore.Qt.LeftButton)
        self.rotate(task)
        self.near(task.rotation_axis()[0],(5,2,0))
        ids={o.Name:o.ID for o in self.doc.Objects};undo=self.doc.UndoCount
        self.assertIsNotNone(task.overlay,task.message.text())
        for angle in (10,40,120,90):task.angle.setProperty('rawValue',float(angle))
        self.near(self.first.LinkPlacement.Base,(0,0,0));self.near(self.second.LinkPlacement.Base,(25,0,0))
        self.assertEqual(self.doc.UndoCount,undo)
        boxes=Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
        button=next(b for box in boxes if box.isVisible() for b in box.buttons() if box.standardButton(b)==QtWidgets.QDialogButtonBox.Apply)
        QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton);settle()
        self.near(self.first.LinkPlacement.Base,(7,-3,0));self.near(self.second.LinkPlacement.Base,(7,22,0))
        self.near(self.second.LinkPlacement.Rotation.multVec(App.Vector(1,0,0)),(0,1,0))
        self.assertEqual(self.doc.UndoCount,undo+1);self.assertIsNone(task.overlay)
        self.assertEqual(task.axis.currentIndex(),0);self.assertIsNone(task.pivot_snapshot)
        self.assertEqual(float(task.angle.property('rawValue')),0);self.assertFalse(task.reverse.isChecked())
        task.accept();settle();self.assertEqual(self.doc.UndoCount,undo+1)
        self.doc.undo();self.doc.recompute();settle();self.near(self.second.LinkPlacement.Base,(25,0,0))
        self.doc.redo();self.doc.recompute();settle();self.near(self.second.LinkPlacement.Base,(7,22,0))
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        document.save_document(self.doc,self.output/'Rotate.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'first':self.first.Name,'second':self.second.Name,'pad':self.pad.Name}))

    def test_located_world_line_under_rotated_shared_parent(self):
        line=self.reference('AxisLine',Part.makeLine(App.Vector(2,3,0),App.Vector(2,3,10)))
        hierarchy.move_instance(self.nested,App.Placement(App.Vector(4,0,0),App.Rotation()))
        sibling=hierarchy.add_instance(self.parent,self.child,App.Placement(App.Vector(0,6,0),App.Rotation(App.Vector(1,0,0),30)))
        hierarchy.move_instance(self.second,App.Placement(App.Vector(25,7,0),App.Rotation(App.Vector(0,0,1),90)));settle()
        task=self.task((self.second,self.nested),(self.second,sibling));task.workflow.setCurrentIndex(1)
        original=[App.Placement(link.LinkPlacement) for link in (self.nested,sibling)]
        relative=original[0].inverse().multiply(original[1])
        self.select(line,'Edge1');QtTest.QTest.mouseClick(task.axis_pick,QtCore.Qt.LeftButton)
        self.near(task.rotation_axis()[0],(-4,23,0));self.near(task.rotation_axis()[1],(0,0,1))
        self.rotate(task,4,90,True)
        self.assertEqual(len(task.paths),2)
        # Reference snapshots remain fixed if the reference's underlying shape changes.
        line.Shape=Part.makeLine(App.Vector(10,3,0),App.Vector(10,3,10));self.doc.recompute();settle()
        self.near(task.rotation_axis()[0],(-4,23,0))
        task.apply();settle()
        self.near(self.nested.LinkPlacement.Base,(-27,15,0))
        self.assertTrue(self.nested.LinkPlacement.inverse().multiply(sibling.LinkPlacement).isSame(relative,1e-8))
        for top in (self.first,self.second):
            expected=hierarchy.world_placement(self.doc,(top,)).multVec(App.Vector(-27,15,0))
            self.assertLess((hierarchy.world_placement(self.doc,(top,self.nested)).Base-expected).Length,1e-7)

    def test_two_points_antiparallel_circle_center_and_origin(self):
        points=self.reference('AxisPoints',Part.makeLine(App.Vector(0,0,4),App.Vector()))
        task=self.task((self.second,));task.workflow.setCurrentIndex(1)
        self.select(points,'Vertex1');task.pick_axis_point(0)
        with self.assertRaisesRegex(ValueError,'distinct'):task.pick_axis_point(1)
        self.select(points,'Vertex2');task.pick_axis_point(1)
        self.rotate(task,5,90);task.apply();self.near(self.second.LinkPlacement.Base,(0,-25,0))
        circle=self.reference('CircleReference',Part.makeCircle(3,App.Vector(5,2,1)))
        self.select(circle,'Edge1');task.pick_pivot();self.near(task.pivot_snapshot,(5,2,1))
        task.reset_pivot();self.assertIsNone(task.pivot_snapshot)
        self.root.Origin.Visibility=True
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.doc.Name,self.root.Name,self.root.Origin.Name+'.')
        task.pick_pivot();self.near(task.pivot_snapshot,(0,0,0))
        self.root.Origin.Visibility=False;settle()
        with self.assertRaisesRegex(ValueError,'visible'):task.pick_pivot()

    def test_successive_translate_rotate_method_switch_cancel_and_selection(self):
        task=self.task((self.second,));undo=self.doc.UndoCount
        translate.TestComponentMove.inputs(self,task,1,3);task.apply();self.near(self.second.LinkPlacement.Base,(28,0,0))
        self.rotate(task,3,45);baseline=App.Placement(self.second.LinkPlacement)
        task.workflow.setCurrentIndex(0);settle();self.assertIsNone(task.overlay)
        self.assertTrue(self.second.LinkPlacement.isSame(baseline,1e-9))
        self.rotate(task,3,90);task.apply();self.near(self.second.LinkPlacement.Base,(0,28,0))
        self.assertEqual(self.doc.UndoCount,undo+2)
        self.rotate(task,1,60);task.reject();settle();self.near(self.second.LinkPlacement.Base,(0,28,0))
        self.doc.undo();self.doc.recompute();settle();self.near(self.second.LinkPlacement.Base,(28,0,0))
        self.doc.undo();self.doc.recompute();settle();self.near(self.second.LinkPlacement.Base,(25,0,0))
        task=self.task((self.second,));task.persistent.setChecked(False);self.rotate(task);task.apply()
        self.assertEqual(task.paths,[]);self.assertEqual(Gui.Selection.getSelection(),[])
        undo=self.doc.UndoCount;task.accept();self.assertEqual(self.doc.UndoCount,undo)

    def test_invalid_angles_axis_and_atomic_failure(self):
        task=self.task((self.first,),(self.second,));self.rotate(task)
        undo=self.doc.UndoCount
        for text in ('bad angle','3 mm','-10 deg'):
            task.angle.setText(text);settle()
            self.assertIsNone(task.overlay)
            with self.assertRaisesRegex(ValueError,'angle'):task.apply()
        task.angle.setProperty('rawValue',30.0);task.axis.setCurrentIndex(0)
        with self.assertRaisesRegex(ValueError,'axis'):task.apply()
        self.rotate(task,3,90)
        real=document.validate;mutated=[]
        def fail(doc):
            if abs(self.second.LinkPlacement.Base.y)>1:
                mutated.append(True);raise ValueError('Controlled rotate failure')
            return real(doc)
        with patch.object(document,'validate',side_effect=fail):
            with self.assertRaisesRegex(ValueError,'Controlled'):task.apply()
        self.assertEqual(mutated,[True]);self.near(self.second.LinkPlacement.Base,(25,0,0))
        self.assertEqual(self.doc.UndoCount,undo)
        self.rotate(task,3,360);task.apply();self.assertEqual(self.doc.UndoCount,undo)
        self.widget.close();settle();self.assertTrue(task.closed);self.assertIsNone(task.overlay)

    def test_external_source_rotation_persistence(self):
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        source=document.new_document('Hardware');root=document.validate(source);parent=root.Definitions[0]
        child=hierarchy.create_definition(source,'Screw');link=hierarchy.add_instance(parent,child,App.Placement(App.Vector(4,0,0),App.Rotation()))
        document.save_document(source,self.output/'Hardware.cadprt');external.import_file(self.doc,source)
        imported=hierarchy.add_instance(self.root,parent,App.Placement(App.Vector(50,8,0),App.Rotation(App.Vector(1,0,0),30)))
        document.save_document(self.doc);checksum=hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest()
        App.setActiveDocument(self.doc.Name);settle();task=self.task((imported,link));undo=source.UndoCount
        self.rotate(task,3,90);task.apply();task.accept();self.near(link.LinkPlacement.Base,(0,4,0))
        self.assertEqual(source.UndoCount,undo+1);external.save_definition(parent)
        self.assertEqual(hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest(),checksum)
        (self.output/'expected.json').write_text(json.dumps({'uid':str(source.Uid),'ids':{o.Name:o.ID for o in source.Objects},'link':link.Name,'assembly_ids':{o.Name:o.ID for o in self.doc.Objects}}))


def verify_fresh_process(output):
    output=Path(output);folder=output/'test_nonorigin_pivot_rigid_group_apply_undo_and_persistence'
    expected=json.loads((folder/'expected.json').read_text());doc=document.open_document(folder/'Rotate.cadprt')
    assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
    for name,point in ((expected['first'],App.Vector(7,-3,0)),(expected['second'],App.Vector(7,22,0))):
        link=doc.getObject(name)
        assert (link.LinkPlacement.Base-point).Length<1e-8
        assert (link.LinkPlacement.Rotation.multVec(App.Vector(1,0,0))-App.Vector(0,1,0)).Length<1e-8
    assert doc.getObject(expected['pad']).Length.Value==5
    App.closeDocument(doc.Name)
    folder=output/'test_external_source_rotation_persistence';expected=json.loads((folder/'expected.json').read_text())
    source=document.open_document(folder/'Hardware.cadprt');link=source.getObject(expected['link'])
    assert {o.Name:o.ID for o in source.Objects}==expected['ids']
    assert (link.LinkPlacement.Base-App.Vector(0,4,0)).Length<1e-8
    assert (link.LinkPlacement.Rotation.multVec(App.Vector(1,0,0))-App.Vector(0,1,0)).Length<1e-8
    App.closeDocument(source.Name)
    doc=document.open_document(folder/'Assembly.cadprt')
    source=next(d for d in App.listDocuments().values() if str(d.Uid)==expected['uid'])
    assert {o.Name:o.ID for o in doc.Objects}==expected['assembly_ids']
    assert (source.getObject(expected['link']).LinkPlacement.Base-App.Vector(0,4,0)).Length<1e-8
    App.closeDocument(doc.Name);App.closeDocument(source.Name)
