# SPDX-License-Identifier: LGPL-2.1-or-later
"""Reopen actual tasks after saving mixed-unit recipes and native documents."""
import json
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtWidgets, QtTest
from freecad_plus import document, editing, mesh_task, reference_image_task, instance_task, sketch_task, sketch_placement
from TestWorkflowUnits import TestWorkflowUnits
from TestMeshSettings import TestMeshSettings
from TestReferenceImage import TestReferenceImage
from TestInstanceQuantity import TestInstanceQuantity


def reopen(test, name, filename):
    path = test.out / filename
    document.save_document(test.doc, path)
    App.closeDocument(test.doc.Name)
    test.doc = document.open_document(path)
    test.owner = document.validate(test.doc).Definitions[0]
    editing.edit((document.validate(test.doc).Group[0],))
    return test.doc.getObject(name)


class TestMeshUnits(unittest.TestCase):
    setUp = TestMeshSettings.setUp
    tearDown = TestMeshSettings.tearDown
    enter = TestWorkflowUnits.enter

    def test_mesh_recipe_defaults_and_equal_value_unit_edit(self):
        task = TestMeshSettings.task(self); form = task.form
        field = form.controls['spinSurfaceDeviation']
        field.setProperty('rawValue', 2.54)
        self.enter(field, '0.1 in', 2.54)
        task.addSelection(self.doc.Name, self.box.Name, '')
        self.assertTrue(task.apply(), form.status.text()); feature = task.result
        self.assertEqual(json.loads(feature.MeshSettings)['units']['spinSurfaceDeviation'], 'in')
        task.reject()
        feature = reopen(self, feature.Name, 'MeshUnitRecipe.cadprt')
        task = editing.edit_feature(self.doc, feature)
        form = task.form; field = form.controls['spinSurfaceDeviation']
        self.assertEqual(field.property('presentationUnit'), 'in')
        self.assertIn('0.100 in', field.findChild(QtWidgets.QLineEdit).text())
        before = feature.MeshSettings; undo = self.doc.UndoCount
        form.open_advanced()
        self.assertEqual(form.native('spinSurfaceDeviation').property('presentationUnit'), 'in')
        self.enter(form.native('spinSurfaceDeviation'), '3 mm', 3)
        form.advanced_dialog.reject()
        self.assertEqual(form.controls['spinSurfaceDeviation'].property('presentationUnit'), 'in')
        form.open_advanced(); self.enter(form.native('spinSurfaceDeviation'), '0.05 in', 1.27)
        form.accept_advanced()
        self.assertEqual(json.loads(self.prefs.GetString('Defaults'))['units']['spinSurfaceDeviation'], 'in')
        task.reject(); self.assertEqual(feature.MeshSettings, before); self.assertEqual(self.doc.UndoCount, undo)
        task = TestMeshSettings.task(self)
        self.assertEqual(task.form.controls['spinSurfaceDeviation'].property('presentationUnit'), 'in')
        self.assertAlmostEqual(task.number('spinSurfaceDeviation'), 1.27)

    def test_advanced_length_models_keep_units_and_legacy_is_readable(self):
        task = TestMeshSettings.task(self); form = task.form
        for index, names in ((1, ('spinMaximumEdgeLength',)), (3, ('minSize','maxSize'))):
            form.open_advanced(); form.radios[index].click()
            if index == 1: form.native('checkMaximumEdgeLength').setChecked(True)
            for name in names: self.enter(form.native(name), '0.25 in', 6.35)
            form.accept_advanced(); state = form.state()
            for name in names: self.assertEqual(form.controls[name].property('presentationUnit'), 'in')
            task.restore_settings(json.loads(json.dumps(state)))
            for name in names:
                self.assertEqual(form.controls[name].property('presentationUnit'), 'in')
                self.assertAlmostEqual(task.number(name), 6.35)
            state.pop('units'); task.restore_settings(state)
            for name in names:
                self.assertNotEqual(form.controls[name].property('presentationUnit'), 'in')
                self.assertAlmostEqual(task.number(name), 6.35)


class TestImageUnits(unittest.TestCase):
    setUp = TestReferenceImage.setUp
    tearDown = TestReferenceImage.tearDown
    enter = TestWorkflowUnits.enter

    def test_image_size_position_calibration_reopen_cancel_and_edit(self):
        task = reference_image_task.show(); task.set_file(str(self.file))
        task.form.aspect.setChecked(False)
        values = {'width': ('2 in',50.8), 'height': ('3 cm',30), 'known': ('0.5 in',12.7),
                  'x': ('0.25 in',6.35), 'y': ('2 mm',2), 'z': ('-0.125 in',-3.175)}
        for name,(text,value) in values.items(): self.enter(task.length_fields()[name],text,value)
        self.assertTrue(task.apply(),task.form.status.text()); feature = task.result
        self.assertAlmostEqual(feature.XSize.Value,50.8)
        self.assertTrue(all(f._unit == 'mm' for f in task.length_fields().values()))
        task.reject()
        feature = reopen(self,feature.Name,'ImageUnitRecipe.cadprt')
        before = feature.ImageSettings; undo = self.doc.UndoCount
        task = reference_image_task.show(feature)
        for name,(text,value) in values.items():
            field = task.length_fields()[name]
            self.assertEqual(field._unit,text.split()[-1]); self.assertAlmostEqual(field.value(),value)
        self.enter(task.form.width,'1 in',25.4); task.reject()
        self.assertEqual(feature.ImageSettings,before); self.assertEqual(self.doc.UndoCount,undo)
        task = reference_image_task.show(feature); self.enter(task.form.width,'1 in',25.4)
        self.assertTrue(task.apply(),task.form.status.text()); self.assertIs(task.result,feature)
        self.assertAlmostEqual(feature.XSize.Value,25.4); task.reject()
        self.doc.undo(); self.assertEqual(feature.ImageSettings,before)


class TestInstanceUnits(unittest.TestCase):
    setUp = TestInstanceQuantity.setUp
    tearDown = TestInstanceQuantity.tearDown
    enter = TestWorkflowUnits.enter

    def test_component_pattern_recipe_reopen_and_cancel(self):
        task = instance_task.open_task([self.part]); f = task.form
        f.mode.setCurrentText('Grid'); f.columns.setValue(2); f.rows.setValue(2)
        values = {'gridX': ('0.5 in',12.7), 'gridY': ('1 cm',10), 'gridZ': ('2 mm',2),
                  'column_spacing': ('1 in',25.4), 'row_spacing': ('0.25 in',6.35)}
        for name,(text,value) in values.items(): self.enter(f.units[name],text,value)
        self.assertTrue(task.accept()); feature = task.created_pattern
        self.assertAlmostEqual(feature.Members[-1].LinkPlacement.Base.x,38.1)
        feature = reopen(self,feature.Name,'InstanceUnitRecipe.cadprt')
        saved = feature.Configuration; undo = self.doc.UndoCount
        task = instance_task.open_task(pattern=feature)
        for name,(text,value) in values.items():
            field = task.form.units[name]
            self.assertEqual(field.property('presentationUnit'),text.split()[-1])
            self.assertAlmostEqual(float(field.property('rawValue')),value)
        self.enter(task.form.units['column_spacing'],'0.5 in',12.7); task.reject()
        self.assertEqual(feature.Configuration,saved); self.assertEqual(self.doc.UndoCount,undo)


class TestSketchOffsetUnits(unittest.TestCase):
    setUp = TestMeshSettings.setUp
    enter = TestWorkflowUnits.enter

    def tearDown(self):
        if sketch_task._active: sketch_task._active.reject()
        TestMeshSettings.tearDown(self)

    def test_sketch_offset_task_save_reopen_and_undo(self):
        xy = next(o for o in self.owner.Origin.OriginFeatures if o.Role == 'XY_Plane')
        feature = sketch_placement.save(self.doc,[(xy,'')],offset=1)
        task = sketch_task.SketchPlacementTask(feature)
        self.enter(task.offset,'0.25 in',6.35)
        self.assertTrue(task.accept(),task.status.text())
        self.assertEqual(feature.QuantityPresentationUnits['SketchPlaneOffset'],'in')
        feature = reopen(self,feature.Name,'SketchOffsetUnits.cadprt')
        task = sketch_task.SketchPlacementTask(feature)
        self.assertEqual(task.offset._unit,'in'); self.assertAlmostEqual(task.offset.value(),6.35)
        before = self.doc.UndoCount
        self.enter(task.offset,'2 cm',20); self.assertTrue(task.accept(),task.status.text())
        self.assertEqual(self.doc.UndoCount,before+1)
        self.assertEqual(feature.QuantityPresentationUnits['SketchPlaneOffset'],'cm')
        self.doc.undo(); self.assertEqual(feature.QuantityPresentationUnits['SketchPlaneOffset'],'in')
        self.assertAlmostEqual(feature.SketchPlaneOffset.Value,6.35)
