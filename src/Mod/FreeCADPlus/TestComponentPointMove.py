# SPDX-License-Identifier: LGPL-2.1-or-later
"""Point-to-point placement acceptance through the native Move Components task."""
import hashlib
import json
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, hierarchy, external, movement
import TestComponentMove as translate
import TestComponentRotate as rotate
import TestComponentPanel as fixtures
settle = fixtures.settle

class TestComponentPointMove(unittest.TestCase):
    setUp = fixtures.TestComponentPanel.setUp
    tearDown = translate.TestComponentMove.tearDown
    rows = fixtures.TestComponentPanel.rows
    occurrence = fixtures.TestComponentPanel.occurrence
    row = translate.TestComponentMove.row
    task = translate.TestComponentMove.task
    reference = rotate.TestComponentRotate.reference
    select = rotate.TestComponentRotate.select
    near = rotate.TestComponentRotate.near

    def pick(self, task, index, obj, element='Vertex1', top=None):
        self.select(obj, element, top)
        QtTest.QTest.mouseClick(task.point_buttons[index], QtCore.Qt.LeftButton)
        settle()
        self.assertIsNotNone(task.point_snapshots[index], task.message.text())

    def test_group_snapshot_apply_undo_and_persistence(self):
        source=self.reference('SourcePoint',Part.Vertex(App.Vector(3,2,1)))
        target=self.reference('TargetPoint',Part.Vertex(App.Vector(8,8,3)))
        hierarchy.move_instance(self.second,App.Placement(App.Vector(25,0,0),App.Rotation(App.Vector(1,0,0),30)))
        task=self.task((self.first,),(self.second,));task.workflow.setCurrentIndex(2)
        ids={o.Name:o.ID for o in self.doc.Objects};undo=self.doc.UndoCount
        original=[App.Placement(o.LinkPlacement) for o in (self.first,self.second)]
        self.pick(task,0,source);self.assertIn('both',task.message.text())
        with self.assertRaisesRegex(ValueError,'both'):task.apply()
        self.pick(task,1,target)
        self.near(task.motion().Base,(5,6,2));self.assertIn('Source',task.point_labels[0].text())
        self.assertIn('Destination',task.point_labels[1].text());self.assertIn('Distance',task.point_distance.text())
        for unused in range(3):task.update_preview()
        self.assertEqual(self.doc.UndoCount,undo);self.assertIsNotNone(task.overlay)
        for obj,placement in zip((self.first,self.second),original):self.assertTrue(obj.LinkPlacement.isSame(placement,1e-9))
        # A geometry edit does not turn the captured points into an association.
        target.Shape=Part.Vertex(App.Vector(100,0,0));self.doc.recompute();settle()
        self.near(task.motion().Base,(5,6,2))
        button=next(b for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
                    if box.isVisible() for b in box.buttons() if box.standardButton(b)==QtWidgets.QDialogButtonBox.Apply)
        QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton);settle()
        self.near(self.first.LinkPlacement.Base,(5,6,2));self.near(self.second.LinkPlacement.Base,(30,6,2))
        self.assertTrue(self.second.LinkPlacement.Rotation.isSame(original[1].Rotation,1e-9))
        self.assertEqual(task.point_snapshots,[None,None]);self.assertEqual(task.point_sources,[None,None])
        self.assertIsNone(task.overlay);self.assertEqual(len(task.paths),2);self.assertEqual(self.doc.UndoCount,undo+1)
        task.accept();settle();self.assertTrue(task.closed);self.assertEqual(self.doc.UndoCount,undo+1)
        self.doc.undo();self.doc.recompute();settle();self.near(self.second.LinkPlacement.Base,(25,0,0))
        self.doc.redo();self.doc.recompute();settle();self.near(self.second.LinkPlacement.Base,(30,6,2))
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        document.save_document(self.doc,self.output/'PointMove.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'first':self.first.Name,'second':self.second.Name,'pad':self.pad.Name}))

    def test_rotated_parent_shared_siblings_external_reference(self):
        hierarchy.move_instance(self.second,App.Placement(App.Vector(25,7,0),App.Rotation(App.Vector(0,0,1),90)))
        sibling=hierarchy.add_instance(self.parent,self.child,App.Placement(App.Vector(4,3,0),App.Rotation(App.Vector(1,0,0),40)))
        source=document.new_document('ReferenceFile');parent=document.validate(source).Definitions[0]
        point=source.addObject('PartDesign::Feature','OutsidePoint');parent.addObject(point);point.Shape=Part.Vertex(App.Vector(2,3,0));source.recompute()
        document.save_document(source,self.output/'Reference.cadprt');external.import_file(self.doc,source)
        imported=hierarchy.add_instance(self.root,parent,App.Placement(App.Vector(50,8,0),App.Rotation(App.Vector(0,0,1),90)))
        App.setActiveDocument(self.doc.Name);settle()
        local=self.reference('LocalPoint',Part.Vertex(App.Vector()))
        task=self.task((self.second,self.nested),(self.second,sibling));task.workflow.setCurrentIndex(2)
        relative=self.nested.LinkPlacement.inverse().multiply(sibling.LinkPlacement)
        self.pick(task,0,point,top=imported);self.near(task.point_snapshots[0],(3,-22,0))
        self.pick(task,1,local,top=self.second);self.near(task.point_snapshots[1],(0,0,0))
        task.apply();settle();self.near(self.nested.LinkPlacement.Base,(-3,22,0))
        self.assertTrue(self.nested.LinkPlacement.inverse().multiply(sibling.LinkPlacement).isSame(relative,1e-8))
        for top in (self.first,self.second):
            expected=hierarchy.world_placement(self.doc,(top,)).multVec(App.Vector(-3,22,0))
            self.assertLess((hierarchy.world_placement(self.doc,(top,self.nested)).Base-expected).Length,1e-7)
        self.near(point.Shape.Point,(2,3,0))

    def test_roles_circle_origin_coincidence_and_stale_reference(self):
        point=self.reference('ReferencePoint',Part.Vertex(App.Vector(5,2,0)))
        circle=self.reference('Circle',Part.makeCircle(3,App.Vector(5,2,0)))
        task=self.task((self.second,));task.workflow.setCurrentIndex(2);undo=self.doc.UndoCount
        self.pick(task,1,circle,'Edge1');self.assertIsNone(task.point_snapshots[0])
        self.pick(task,0,point);task.apply();settle();self.assertEqual(self.doc.UndoCount,undo)
        self.assertEqual(task.point_snapshots,[None,None])
        self.root.Origin.Visibility=True
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.doc.Name,self.root.Name,self.root.Origin.Name+'.')
        task.pick_point(0);self.near(task.point_snapshots[0],(0,0,0))
        self.pick(task,1,point);point.Visibility=False;settle()
        with self.assertRaisesRegex(ValueError,'unavailable'):task.apply()
        self.assertIsNone(task.overlay);point.Visibility=True;self.doc.removeObject(point.Name);self.doc.recompute();settle()
        with self.assertRaisesRegex(ValueError,'unavailable'):task.apply()
        self.assertEqual(self.doc.UndoCount,undo);self.near(self.second.LinkPlacement.Base,(25,0,0))
        task.reset_inputs()
        line=self.reference('NotAPoint',Part.makeLine(App.Vector(),App.Vector(1,2,3)))
        self.select(line,'Edge1')
        with self.assertRaisesRegex(ValueError,'vertex'):task.pick_point(0)
        self.assertEqual(task.point_snapshots,[None,None])

    def test_switch_cancel_successive_moves_and_selection(self):
        source=self.reference('SourcePoint',Part.Vertex(App.Vector()))
        target=self.reference('TargetPoint',Part.Vertex(App.Vector(3,4,0)))
        task=self.task((self.second,));undo=self.doc.UndoCount;task.workflow.setCurrentIndex(2)
        self.pick(task,0,source);self.pick(task,1,target)
        task.workflow.setCurrentIndex(1);settle();self.assertIsNone(task.overlay)
        self.assertEqual(task.point_snapshots,[None,None]);self.near(self.second.LinkPlacement.Base,(25,0,0))
        task.workflow.setCurrentIndex(2);self.pick(task,0,source);self.pick(task,1,target);task.apply()
        self.near(self.second.LinkPlacement.Base,(28,4,0));self.assertEqual(self.doc.UndoCount,undo+1)
        self.pick(task,0,target);self.pick(task,1,source);task.reject();settle()
        self.near(self.second.LinkPlacement.Base,(28,4,0));self.assertIsNone(task.overlay)
        task=self.task((self.second,));task.workflow.setCurrentIndex(2);task.persistent.setChecked(False)
        self.pick(task,0,source);self.pick(task,1,target);task.apply()
        self.near(self.second.LinkPlacement.Base,(31,8,0));self.assertEqual(task.paths,[])
        self.assertEqual(Gui.Selection.getSelection(),[]);task.accept();settle();self.assertTrue(task.closed)
        self.assertEqual(self.doc.UndoCount,undo+2)

    def test_external_parent_source_owned_save(self):
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        source=document.new_document('Hardware');root=document.validate(source);parent=root.Definitions[0]
        child=hierarchy.create_definition(source,'Pin');link=hierarchy.add_instance(parent,child,App.Placement(App.Vector(4,0,0),App.Rotation()))
        document.save_document(source,self.output/'Hardware.cadprt');external.import_file(self.doc,source)
        imported=hierarchy.add_instance(self.root,parent);document.save_document(self.doc)
        checksum=hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest()
        App.setActiveDocument(self.doc.Name);settle()
        a=self.reference('SourcePoint',Part.Vertex(App.Vector()));b=self.reference('DestinationPoint',Part.Vertex(App.Vector(2,3,0)))
        task=self.task((imported,link));task.workflow.setCurrentIndex(2);undo=source.UndoCount
        self.pick(task,0,a);self.pick(task,1,b);task.apply();task.accept();settle()
        self.near(link.LinkPlacement.Base,(6,3,0));self.assertEqual(source.UndoCount,undo+1)
        external.save_definition(parent);self.assertEqual(hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest(),checksum)
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in source.Objects},'link':link.Name,'uuid':source.Uid,'checksum':checksum}))

def verify_fresh_process(output):
    output=Path(output);before=set(App.listDocuments())
    try:
        folder=output/'test_group_snapshot_apply_undo_and_persistence'
        expected=json.loads((folder/'expected.json').read_text());doc=document.open_document(folder/'PointMove.cadprt')
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        assert (doc.getObject(expected['first']).LinkPlacement.Base-App.Vector(5,6,2)).Length<1e-7
        second=doc.getObject(expected['second']);assert (second.LinkPlacement.Base-App.Vector(30,6,2)).Length<1e-7
        assert second.LinkPlacement.Rotation.isSame(App.Rotation(App.Vector(1,0,0),30),1e-9)
        assert doc.getObject(expected['pad']).Length.Value==5
        folder=output/'test_external_parent_source_owned_save';expected=json.loads((folder/'expected.json').read_text())
        source=document.open_document(folder/'Hardware.cadprt')
        assert source.Uid==expected['uuid'] and {o.Name:o.ID for o in source.Objects}==expected['ids']
        assert (source.getObject(expected['link']).LinkPlacement.Base-App.Vector(6,3,0)).Length<1e-7
        App.closeDocument(source.Name)
        assembly=document.open_document(folder/'Assembly.cadprt')
        source=next(d for d in App.listDocuments().values() if d.Uid==expected['uuid'])
        assert {o.Name:o.ID for o in source.Objects}==expected['ids']
        assert (source.getObject(expected['link']).LinkPlacement.Base-App.Vector(6,3,0)).Length<1e-7
        assert hashlib.sha256(Path(assembly.FileName).read_bytes()).hexdigest()==expected['checksum']
    finally:
        for name in set(App.listDocuments())-before:App.closeDocument(name)
