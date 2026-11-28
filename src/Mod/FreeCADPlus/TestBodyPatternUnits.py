# SPDX-License-Identifier: LGPL-2.1-or-later
"""Real keyboard quantity entry, resulting geometry, saved recipes and Undo."""
import json,os,unittest
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui
from PySide6 import QtCore,QtWidgets,QtTest
from freecad_plus import document,editing,transforms,transform_task
from freecad_plus.quantity_fields import QuantityNumber
from TestShapeTransforms import TestShapeTransforms as Fixtures


class TestBodyPatternUnits(unittest.TestCase):
    setUp=Fixtures.setUp
    tearDown=Fixtures.tearDown

    def open(self,kind='Linear pattern',source=None):
        Gui.Selection.clearSelection()
        task=transform_task.show(kind)
        task.addSelection(self.doc.Name,(source or self.source).Name,'')
        Gui.getMainWindow().showNormal();Gui.getMainWindow().resize(1600,1200)
        QtTest.QTest.qWait(80)
        return task

    def type_length(self,task,field,text,expected):
        before=field.value();field.setFocus();field.selectAll();QtTest.QTest.keyClicks(field,text)
        self.assertEqual(field.value(),before,'Typing must not update preview values before commit')
        self.assertIn(text,field.text());self.assertTrue(field.hasAcceptableInput(),field.text())
        task.form.name.setFocus();QtTest.QTest.qWait(80)
        self.assertAlmostEqual(field.value(),expected,places=9)

    def test_linear_keyboard_precision_geometry_and_reset(self):
        task=self.open();step=task.form.steps[0]
        for text,expected in (('0.5 in',12.7),('0.03125 in',.79375),('2.54 cm',25.4),('0.5 in',12.7)):
            self.type_length(task,step.value,text,expected)
        step.count.setValue(3);undo=self.doc.UndoCount
        task.form.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'linear-inches.png'))
        self.assertTrue(task.apply(),task.form.status.text());result=task.results[0]
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertAlmostEqual(result.Shape.BoundBox.XLength,35.4,places=6)
        self.assertEqual(transforms.settings(result)[0]['units']['value'],'in')
        self.assertFalse(task.refs);self.assertEqual(step.value.value(),10);self.assertEqual(step.value.suffix(),' mm')
        task.reject();name=result.Name
        self.doc.undo();self.assertIsNone(self.doc.getObject(name));self.doc.redo()
        self.assertAlmostEqual(self.doc.getObject(name).Shape.BoundBox.XLength,35.4,places=6)

    def test_overall_length_sheet_and_immediate_apply(self):
        task=self.open(source=self.sheet);step=task.form.steps[0]
        step.measure.setCurrentIndex(1);step.count.setValue(3)
        # Apply also validates/commits a pending quantity when invoked without blur.
        step.value.setFocus();step.value.selectAll();QtTest.QTest.keyClicks(step.value,'1 in')
        self.assertTrue(task.apply(),task.form.status.text())
        self.assertFalse(task.results[0].Shape.Solids)
        self.assertAlmostEqual(task.results[0].Shape.BoundBox.XLength,35.4,places=6)

    def test_saved_units_reopen_edit_and_cancel(self):
        task=self.open();step=task.form.steps[0]
        self.type_length(task,step.value,'0.5 in',12.7)
        self.assertTrue(task.apply(),task.form.status.text());name=task.results[0].Name;task.reject()
        path=Path(os.environ['PLUS_TEST_DIR'])/'PatternInches.cadprt';document.save_document(self.doc,path)
        App.closeDocument(self.doc.Name);self.doc=document.open_document(path)
        self.owner=document.validate(self.doc).Definitions[0]
        editing.edit((document.validate(self.doc).Group[0],))
        feature=self.doc.getObject(name);saved=feature.TransformSteps;undo=self.doc.UndoCount
        task=transform_task.show(feature=feature);step=task.form.steps[0]
        self.assertEqual(step.value.suffix(),' in');self.assertAlmostEqual(step.value.value(),12.7)
        self.type_length(task,step.value,'0.25 in',6.35);task.reject()
        self.assertEqual(feature.TransformSteps,saved);self.assertEqual(self.doc.UndoCount,undo)
        task=transform_task.show(feature=feature);self.type_length(task,task.form.steps[0].value,'1 in',25.4)
        self.assertTrue(task.apply(),task.form.status.text());self.assertEqual(task.results[0],feature)
        self.assertAlmostEqual(feature.Shape.BoundBox.XLength,35.4,places=6)
        task.reject();self.doc.undo();self.assertEqual(feature.TransformSteps,saved)

    def test_mirror_polar_and_multi_transform_units_follow_steps(self):
        task=self.open('Mirror');self.type_length(task,task.form.steps[0].offset,'-0.25 in',-6.35)
        self.assertAlmostEqual(task.settings()[0]['offset'],-6.35);task.reject()
        task=self.open('Polar pattern');step=task.form.steps[0]
        for field,text,expected in zip(step.center,('1 in','-0.25 in','0.5 in'),(25.4,-6.35,12.7)):
            self.type_length(task,field,text,expected)
        self.assertNotIsInstance(step.value,QuantityNumber);self.assertEqual(step.value.value(),360)
        self.assertEqual(task.settings()[0]['center'],[25.4,-6.35,12.7]);task.reject()
        task=self.open('Multi-transform')
        task.form.add_step('Linear pattern');linear=task.form.steps[0]
        self.type_length(task,linear.value,'0.5 in',12.7)
        task.form.add_step('Mirror');mirror=task.form.steps[1]
        self.type_length(task,mirror.offset,'1 in',25.4)
        task.form.move_step(-1)
        values=task.settings();self.assertEqual(values[0]['kind'],'Mirror');self.assertEqual(values[1]['value'],12.7)
        self.assertEqual(values[0]['units'],{'offset':'in'});self.assertEqual(values[1]['units'],{'value':'in'})
        self.assertTrue(task.apply(),task.form.status.text());feature=task.results[0];task.reject()
        task=transform_task.show(feature=feature)
        self.assertEqual([next(iter(s.length_fields().values())).suffix() for s in task.form.steps],[' in',' in'])

    def test_invalid_units_do_not_create_result_and_legacy_recipes_load(self):
        task=self.open();field=task.form.steps[0].value;count=len(self.doc.Objects);undo=self.doc.UndoCount
        field.setFocus();field.selectAll();QtTest.QTest.keyClicks(field,'10 deg')
        self.assertFalse(field.hasAcceptableInput());self.assertFalse(task.apply())
        self.assertEqual(len(self.doc.Objects),count);self.assertEqual(self.doc.UndoCount,undo)
        field.selectAll();QtTest.QTest.keyClicks(field,'0.5 in');self.assertTrue(task.apply(),task.form.status.text())
        feature=task.results[0];task.reject()
        values=json.loads(feature.TransformSteps);values[0].pop('units');feature.TransformSteps=json.dumps(values)
        task=transform_task.show(feature=feature)
        self.assertEqual(task.form.steps[0].value.suffix(),' mm');self.assertAlmostEqual(task.form.steps[0].value.value(),12.7)
