# SPDX-License-Identifier: LGPL-2.1-or-later
import os
import unittest
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, Part
from PySide6 import QtTest
from freecad_plus import document, editing, transforms, transform_task


class TestShapeTransforms(unittest.TestCase):
    def setUp(self):
        self.before=set(App.listDocuments());self.doc=document.new_document('TransformTests')
        self.owner=document.validate(self.doc).Definitions[0]
        editing.edit((document.validate(self.doc).Group[0],))
        with document.transaction(self.doc,'Fixture'):
            self.source=self.owner.newObject('Part::Feature','CutBody')
            self.source.Shape=Part.makeBox(10,8,6).cut(Part.makeCylinder(1,6,App.Vector(3,3,0)))
            self.sheet=self.owner.newObject('Part::Feature','Sheet');self.sheet.Shape=Part.makePlane(10,8)
        self.refs=[(self.source,'')]

    def tearDown(self):
        if transform_task._active:transform_task._active.reject()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments())-self.before:App.closeDocument(name)

    def test_all_four_shapes(self):
        linear=dict(kind='Linear pattern',axis=0,count=3,value=15,measure=0)
        polar=dict(kind='Polar pattern',axis=2,count=4,value=360,measure=0,center=[30,0,0])
        mirror=dict(kind='Mirror',axis=2,offset=20)
        for steps,count in [([linear],3),([polar],4),([mirror],2),([linear,dict(mirror,offset=60)],6)]:
            result=transforms.evaluate(self.owner,self.refs,steps,True)[0]
            self.assertEqual(len(result.Solids),count)
            self.assertAlmostEqual(result.Volume,self.source.Shape.Volume*count,5)
            self.assertTrue(result.isValid())
        result=transforms.evaluate(self.owner,[(self.sheet,'')],[mirror],True)[0]
        self.assertEqual(len(result.Faces),2);self.assertFalse(result.Solids)

    def test_touching_fuses_and_undo_edit_save(self):
        step=dict(kind='Linear pattern',axis=0,count=3,value=10,measure=0)
        undo=self.doc.UndoCount
        result=transforms.save(self.doc,self.refs,[step])[0]
        self.assertEqual(result.getTypeIdOfProperty('TransformSources'),'App::PropertyLinkSubListGlobal')
        self.assertEqual(len(result.Shape.Solids),1);self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertIn(result,document.history(self.doc,self.owner))
        self.doc.undo();self.doc.redo();self.doc.recompute();document.validate(self.doc)
        result=self.doc.getObject(result.Name)
        step['value']=15
        updated=transforms.save(self.doc,self.refs,[step],feature=result)[0]
        self.assertEqual(updated,result);self.assertEqual(len(result.Shape.Solids),3)
        self.source.Shape=Part.makeBox(5,8,6);self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume,720,5)
        filename=Path(os.environ['PLUS_TEST_DIR'])/'Transform.cadprt'
        document.save_document(self.doc,filename)
        name=result.Name;App.closeDocument(self.doc.Name)
        self.doc=document.open_document(filename);result=self.doc.getObject(name)
        self.assertEqual(len(result.Shape.Solids),3);self.assertEqual(result.GeometryError,'')

    def test_task_empty_preselection_apply_and_cancel(self):
        Gui.Selection.clearSelection();before=len(self.doc.Objects);undo=self.doc.UndoCount
        task=transform_task.show('Linear pattern');self.assertEqual(task.refs,[])
        task.addSelection(self.doc.Name,self.source.Name,'Face1');QtTest.QTest.qWait(80)
        self.assertEqual(task.refs,self.refs);self.assertEqual(len(self.doc.Objects),before)
        self.assertTrue(task.apply());self.assertEqual(task.refs,[]);self.assertEqual(task.form.steps[0].count.value(),2)
        self.assertEqual(self.doc.UndoCount,undo+1);task.reject();document.validate(self.doc)
        Gui.Selection.addSelection(self.source)
        task=transform_task.show('Mirror');self.assertEqual(task.refs,self.refs)
        task.reject();self.assertEqual(self.doc.UndoCount,undo+1)

    def test_separate_results_and_invalid_input(self):
        step=dict(kind='Linear pattern',axis=0,count=3,value=15)
        results=transforms.save(self.doc,self.refs,[step],False)
        self.assertEqual(len(results),3)
        self.assertEqual(len({o.TransformGroup for o in results}),1)
        with self.assertRaises(ValueError):transforms.evaluate(self.owner,[*self.refs,(self.sheet,'')],[step],True)
        with self.assertRaises(ValueError):transforms.evaluate(self.owner,self.refs,[],True)
        with self.assertRaises(ValueError):transforms.source(self.owner,(self.owner,''))
