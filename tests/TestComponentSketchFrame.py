# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native sketch frames follow valid references and survive missing or failed supports."""
import hashlib
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
from freecad.gui import ComponentSketchTask as Task

class TestComponentSketchFrame(unittest.TestCase):
    def setUp(self):
        for module, relative in ((Sketch, 'src/Mod/Part/ComponentSketch.py'), (Model, 'src/Mod/Part/ComponentModel.py'), (Task, 'src/Gui/ComponentSketchTask.py')):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(), hashlib.sha256((Path(os.environ['FREECAD_PLUS_SOURCE']) / relative).read_bytes()).digest())
        self.doc = Model.new_document('Sketch frames')
        self.component = Model.metadata(self.doc).RootComponent
        self.box = self.doc.addObject('Part::Box', 'Support')
        Model.register_object(self.component, self.box)
        self.doc.recompute()

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            gui = Gui.getDocument(doc.Name)
            if gui.getInEdit():
                gui.resetEdit()
            App.closeDocument(doc.Name)
        Gui.Selection.clearSelection()

    def same(self, actual, expected):
        self.assertTrue(actual.isSame(expected, 1e-7), (actual, expected))

    def sketch(self, **kwargs):
        return Sketch.create(self.component, 'Selected planar face', support=(self.box, 'Face6'), offset=2, **kwargs)

    def rectangle(self, sk):
        points = [App.Vector(x,y,0) for x,y in ((0,0),(3,0),(3,4),(0,4))]
        sk.addGeometry([Part.LineSegment(points[i], points[(i+1)%4]) for i in range(4)], False)
        self.doc.recompute()

    def testIndependentAndCopiedFrames(self):
        sk = Sketch.create(self.component, 'Independent plane', offset=9, origin=(3,5), directions=('X',(1,1,0),(0,0,1)))
        self.same(sk.Placement, App.Placement(App.Vector(3,5,9), App.Rotation(App.Vector(0,0,1),45)))
        self.assertFalse(sk.AttachmentSupport)
        self.assertEqual(sk.MapMode, 'Deactivated')
        self.assertEqual(Model.history(self.component), [self.box,sk])
        copied = self.sketch(follow_support=False)
        old = App.Placement(copied.Placement)
        self.box.Height = 25
        self.doc.recompute()
        self.same(copied.Placement, old)
        self.rectangle(sk)
        self.assertFalse(Model.current_shape(sk).isNull())

    def testFollowingFailureRepairAndDownstream(self):
        sk = self.sketch()
        self.rectangle(sk)
        operation, result = Extrude.create(self.component, sk, 5)
        self.box.Height = 20
        self.doc.recompute()
        self.assertAlmostEqual(sk.Placement.Base.z,22)
        self.assertAlmostEqual(Model.current_shape(result).BoundBox.ZMin,22)
        saved = App.Placement(sk.Placement)
        self.box.Height = -1
        self.doc.recompute()
        self.assertIn('Invalid', self.box.State)
        self.same(sk.Placement, saved)
        self.assertNotIn('Invalid', sk.State)
        self.assertTrue(sk.FrameSupportStatus.startswith('Saved frame'))
        sk.addGeometry(Part.LineSegment(App.Vector(8,0,0), App.Vector(9,0,0)), True)
        self.doc.recompute()
        self.assertFalse(Model.current_shape(sk).isNull())
        self.assertAlmostEqual(Model.current_shape(result).Volume,60)
        self.box.Height = 30
        self.doc.recompute()
        self.assertAlmostEqual(sk.Placement.Base.z,32)
        self.assertAlmostEqual(Model.current_shape(result).BoundBox.ZMin,32)
        self.assertEqual(sk.FrameSupportStatus,'Following support')

    def testDeletionUndoRedoAndReopen(self):
        sk = self.sketch()
        self.rectangle(sk)
        saved = App.Placement(sk.Placement)
        name = sk.Name
        with Model.transaction(self.doc,'Delete support'):
            self.doc.removeObject(self.box.Name)
        self.doc.recompute()
        self.same(sk.Placement,saved)
        self.assertFalse(sk.FrameSupport)
        self.assertFalse(Model.current_shape(sk).isNull())
        self.doc.undo();self.doc.recompute()
        sk = self.doc.getObject(name)
        self.assertTrue(sk.FrameSupport)
        source = sk.FrameSupport[0][0]
        source.Height = 17;self.doc.recompute()
        self.assertAlmostEqual(sk.Placement.Base.z,19)
        with Model.transaction(self.doc,'Delete again'):
            self.doc.removeObject(source.Name)
        self.doc.recompute();self.doc.undo();self.doc.redo();self.doc.recompute()
        sk=self.doc.getObject(name)
        saved=App.Placement(sk.Placement)
        path=Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])/'detached.cadprt'
        self.doc.saveAs(str(path));App.closeDocument(self.doc.Name)
        self.doc=App.openDocument(str(path));self.doc.recompute()
        sk=self.doc.getObject(name)
        self.same(sk.Placement,saved)
        self.assertFalse(Model.current_shape(sk).isNull())
        replacement=self.doc.addObject('Part::Box','Support');self.doc.recompute()
        replacement.Height=50;self.doc.recompute()
        self.same(sk.Placement,saved)

    def testUserPlaneUpstreamFailureAndMotion(self):
        plane=Sketch.create_plane(self.component, 'Selected planar face', support=(self.box,'Face6'), offset=3, frame={})
        sk=Sketch.create(self.component, 'User plane', support=plane)
        self.rectangle(sk)
        self.box.Height=20;self.doc.recompute()
        self.assertAlmostEqual(sk.Placement.Base.z,23)
        saved=App.Placement(sk.Placement)
        self.box.Height=-1;self.doc.recompute()
        self.assertNotIn('Touched',sk.State, str([(o.Name,o.State,[x.Name for x in o.OutList]) for o in self.doc.Objects]) + sk.FrameSupportStatus)
        self.same(sk.Placement,saved)
        self.assertFalse(Model.current_shape(sk).isNull())
        self.box.Height=25;self.doc.recompute()
        self.assertAlmostEqual(sk.Placement.Base.z,28)
        self.doc.removeObject(plane.Name);self.doc.recompute()
        self.assertAlmostEqual(sk.Placement.Base.z,28)
        self.assertFalse(Model.current_shape(sk).isNull())

    def testTwoEdgesMotionAndInvalidPairs(self):
        pairs=[(self.box,'Edge1'),(self.box,'Edge2')]
        sk=Sketch.create(self.component,'Selected two edges',support=pairs)
        before=App.Placement(sk.Placement)
        self.box.Placement=App.Placement(App.Vector(10,20,30),App.Rotation(App.Vector(1,2,3),37))
        self.doc.recompute()
        self.same(sk.Placement,self.box.Placement.multiply(before))
        self.rectangle(sk)
        saved=App.Placement(sk.Placement)
        self.doc.removeObject(self.box.Name);self.doc.recompute()
        self.same(sk.Placement,saved)
        self.assertFalse(Model.current_shape(sk).isNull())
        with self.assertRaises(ValueError):
            Sketch.two_edge_frame(self.component,[(sk,'Edge1'),(sk,'Edge1')])

    def testTaskIndependentFieldsAndTwoEdgePicking(self):
        task=Task.SketchTask(self.component)
        task.plane.setCurrentIndex(task.plane.findData('Independent plane'))
        self.assertFalse(task.follow_support.isEnabled())
        self.assertFalse(task.origins[0].isHidden())
        self.assertFalse(task.rotations[0].isHidden())
        self.assertEqual(task.offset_label.text(),'Origin Z')
        task.offset.setProperty('rawValue',8)
        task.origins[0].setProperty('rawValue',3)
        values=task.plane_values()
        sk=Sketch.create(self.component,task.plane.currentData(),offset=values['offset'],origin=values['origin'],angles=values['angles'])
        self.same(sk.Placement,App.Placement(App.Vector(3,0,8),App.Rotation()))
        task.capture_face([(self.box,'Edge1'),(self.box,'Edge2')])
        self.assertEqual(task.plane.currentData(),'Selected two edges')
        self.assertTrue(task.follow_support.isEnabled())
        task.form.resize(330,800);task.form.show();Gui.updateGui()
        task.form.grab().save(str(Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])/'two-edges-task.png'))
        task.form.close()

    def testRotatedComponentOffsetMissingFaceAndRepair(self):
        self.component.Placement=App.Placement(App.Vector(20,30,40),App.Rotation(App.Vector(1,2,3),29))
        self.box.Placement=App.Placement(App.Vector(2,3,4),App.Rotation(App.Vector(1,0,0),31))
        self.doc.recompute()
        sk=self.sketch()
        expected=self.box.Placement.multiply(App.Placement(App.Vector(0,0,12),App.Rotation()))
        self.same(sk.Placement,expected)
        sk.AttachmentOffset.Base=App.Vector(1,2,5);self.doc.recompute()
        expected=self.box.Placement.multiply(App.Placement(App.Vector(1,2,15),App.Rotation()))
        self.same(sk.Placement,expected)
        self.rectangle(sk)
        sk.FrameSupport=[(self.box,['Face99'])];self.doc.recompute()
        self.same(sk.Placement,expected)
        self.assertTrue(sk.FrameSupportStatus.startswith('Saved frame'))
        self.assertFalse(Model.current_shape(sk).isNull())
        sk.FrameSupport=[(self.box,['Face6'])];self.box.Height=15;self.doc.recompute()
        self.same(sk.Placement,self.box.Placement.multiply(App.Placement(App.Vector(1,2,20),App.Rotation())))
        fixture=Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])/'following.cadprt'
        self.doc.saveAs(str(fixture))

    def testReattachPreservesWorldThenFollowsNewSupport(self):
        import SketchSupport
        import SketchSupportGui
        sk=self.sketch();self.rectangle(sk)
        saved=App.Placement(sk.Placement)
        second=self.doc.addObject('Part::Box','Replacement');Model.register_object(self.component,second)
        second.Placement=App.Placement(App.Vector(10,20,30),App.Rotation(App.Vector(0,1,0),37));self.doc.recompute()
        SketchSupport.reattach_planar(sk,second,'Face6','preserve-world')
        self.same(sk.Placement,saved)
        self.assertEqual(sk.FrameSupport[0][0],second)
        second.Placement.Base=second.Placement.Base+App.Vector(0,0,10);self.doc.recompute()
        self.same(sk.Placement,App.Placement(saved.Base+App.Vector(0,0,10),saved.Rotation))
        self.doc.removeObject(second.Name);self.doc.recompute()
        self.assertFalse(Model.current_shape(sk).isNull())

    def testHistoryCannotCrossFrameReferences(self):
        sk=self.sketch();self.rectangle(sk)
        op,result=Extrude.create(self.component,sk,5)
        Model.reorder_history(self.component,[sk],0)
        history=Model.history(self.component)
        self.assertLess(history.index(self.box),history.index(sk))
        Model.reorder_history(self.component,[self.box],len(history))
        history=Model.history(self.component)
        self.assertLess(history.index(self.box),history.index(sk))
        self.assertLess(history.index(sk),history.index(op))

    def testRejectCollinearNoncoplanarAndForeignEdgesAtomically(self):
        shape=self.doc.addObject('Part::Feature','Lines');Model.register_object(self.component,shape)
        shape.Shape=Part.makeCompound([Part.makeLine(App.Vector(0,0,0),App.Vector(1,0,0)),
                                      Part.makeLine(App.Vector(2,0,0),App.Vector(3,0,0)),
                                      Part.makeLine(App.Vector(0,1,1),App.Vector(0,2,1))])
        self.doc.recompute()
        count=len(self.doc.Objects)
        for names in [('Edge1','Edge2'),('Edge1','Edge3')]:
            with self.assertRaises(ValueError):
                Sketch.create(self.component,'Selected two edges',support=[(shape,n) for n in names])
            self.assertEqual(len(self.doc.Objects),count)
        with self.assertRaises(ValueError):
            Sketch.create(self.component,'Selected two edges',support=[(shape,'Edge1'),(self.box,'Edge1')])

    def testLiveTwoEdgeSelectionAndIndependentEditor(self):
        from PySide import QtCore
        from PySide6 import QtTest
        task=Task.launch(self.component)
        Gui.Selection.addSelection(self.box,'Edge1');Gui.Selection.addSelection(self.box,'Edge2')
        self.assertEqual(task.plane.currentData(),'Selected two edges')
        task.plane.setCurrentIndex(task.plane.findData('Independent plane'))
        task.origins[0].setProperty('rawValue',4)
        task.offset.setProperty('rawValue',7)
        task.form.resize(330,800);task.form.show();Gui.updateGui()
        task.form.grab().save(str(Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])/'independent-task.png'))
        self.assertTrue(task.accept())
        QtTest.QTest.qWait(250);Gui.updateGui()
        sk=task.result
        self.assertTrue(Gui.getDocument(self.doc.Name).getInEdit())
        self.assertFalse(sk.AttachmentSupport)
        self.assertAlmostEqual(sk.Placement.Base.x,4)
        self.assertAlmostEqual(sk.Placement.Base.z,7)
        Gui.getDocument(self.doc.Name).resetEdit()
