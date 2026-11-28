# SPDX-License-Identifier: LGPL-2.1-or-later
"""Keyboard inch-entry audit of Plus tasks and their native quantity controls."""
import json
import os
import unittest
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, trim_task
from freecad_plus.quantity_fields import QuantityNumber
from TestMeshSettings import TestMeshSettings as Fixtures


class TestWorkflowUnits(unittest.TestCase):
    setUp = Fixtures.setUp
    tearDown = Fixtures.tearDown

    def enter(self, field, text, expected):
        field.setFocus()
        edit = field if isinstance(field, QtWidgets.QLineEdit) else field.findChild(QtWidgets.QLineEdit)
        edit.selectAll()
        QtTest.QTest.keyClicks(edit, text)
        self.assertTrue(field.hasAcceptableInput(), text + ': ' + edit.text())
        # Some task sections remain collapsed until their mode is selected;
        # explicitly commit their actual widget to audit all available fields.
        if isinstance(field, QuantityNumber): field.interpretText()
        QtTest.QTest.keyClick(edit, QtCore.Qt.Key_Tab)
        QtTest.QTest.qWait(10)
        value = field.property('rawValue') if field.metaObject().indexOfProperty('rawValue') >= 0 else field.value()
        self.assertAlmostEqual(float(value), expected, places=9)

    def test_trim_offset_geometry_reset_undo_and_saved_edit(self):
        task = trim_task.show()
        task.addSelection(self.doc.Name, self.box.Name, '')
        task.form.mode.setCurrentIndex(1)
        self.enter(task.form.offset, '0.25 in', 6.35)
        task.form.grab().save(str(self.out / 'trim-inches.png'))
        before = self.doc.UndoCount
        self.assertTrue(task.apply(), task.form.status.text())
        feature = task.result
        self.assertAlmostEqual(feature.Shape.BoundBox.ZLength, 6.35)
        self.assertEqual(self.doc.UndoCount, before + 1)
        self.assertEqual(task.form.offset.value(), 0)
        self.assertEqual(task.form.offset.suffix(), ' mm')
        task.reject()
        name = feature.Name
        self.doc.undo()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo()
        path = self.out / 'TrimInches.cadprt'
        document.save_document(self.doc, path)
        App.closeDocument(self.doc.Name)
        self.doc = document.open_document(path)
        feature = self.doc.getObject(name)
        editing.edit((document.validate(self.doc).Group[0],))
        saved = feature.TrimSettings
        task = trim_task.show(feature)
        self.assertEqual(task.form.offset.suffix(), ' in')
        self.enter(task.form.offset, '0.125 in', 3.175)
        task.reject()
        self.assertEqual(feature.TrimSettings, saved)
        task = trim_task.show(feature)
        self.enter(task.form.offset, '0.125 in', 3.175)
        self.assertTrue(task.apply(), task.form.status.text())
        self.assertIs(task.result, feature)
        self.assertAlmostEqual(feature.Shape.BoundBox.ZLength, 3.175)

    def test_trim_pending_input_validation_and_legacy_settings(self):
        task = trim_task.show()
        task.addSelection(self.doc.Name, self.box.Name, '')
        task.form.mode.setCurrentIndex(1)
        field = task.form.offset
        before = (len(self.doc.Objects), self.doc.UndoCount)
        field.setFocus(); field.selectAll(); QtTest.QTest.keyClicks(field, '4 deg')
        self.assertFalse(task.apply())
        self.assertEqual((len(self.doc.Objects), self.doc.UndoCount), before)
        field.selectAll(); QtTest.QTest.keyClicks(field, '0.25 in')
        self.assertTrue(task.apply(), task.form.status.text())
        feature = task.result; task.reject()
        values = json.loads(feature.TrimSettings); values.pop('offset_unit')
        feature.TrimSettings = json.dumps(values)
        task = trim_task.show(feature)
        self.assertEqual(task.form.offset.suffix(), ' mm')
        self.assertAlmostEqual(task.form.offset.value(), 6.35)

    def test_modeling_and_plane_task_length_controls(self):
        from freecad_plus import extrude_task, plane_task, sketch_task, shell_task, thicken_task
        factories = (extrude_task.ExtrudeTask, plane_task.PlaneTask,
                     sketch_task.SketchPlacementTask, shell_task.ShellTask, thicken_task.ThickenTask)
        for factory in factories:
            with self.subTest(workflow=factory.__name__):
                task = factory()
                forms = task.form if isinstance(task.form, list) else [task.form]
                try:
                    for form in forms: form.show()
                    fields = [w for form in forms for w in form.findChildren(QuantityNumber)
                              if w._dimension == App.Units.Quantity('1 mm').Unit]
                    self.assertTrue(fields)
                    for field in fields:
                        field.show()
                        self.enter(field, '0.125 in', 3.175)
                finally:
                    task.reject()
                    for form in forms: form.hide()

    def test_reference_image_and_sketch_pattern_fields(self):
        from freecad_plus import reference_image_ui, sketch_pattern_task
        form = reference_image_ui.Form(self.owner); form.show()
        try:
            form.aspect.setChecked(False)
            fields = [w for w in form.findChildren(QuantityNumber)
                      if w._dimension == App.Units.Quantity('1 mm').Unit]
            self.assertGreaterEqual(len(fields), 6)
            for field in fields:
                field.show(); self.enter(field, '0.03125 in', .79375)
        finally: form.close()
        field = sketch_pattern_task.amount(20); field.show()
        try: self.enter(field, '0.5 in', 12.7)
        finally: field.close()

    def test_instance_positions_spacing_radius_and_movement_parser(self):
        from freecad_plus.instance_quantity_ui import InstanceForm
        form = InstanceForm(self.owner, ['Child']); form.show()
        try:
            checked = set()
            for index in range(4):
                form.mode.setCurrentIndex(index)
                for key, field in form.units.items():
                    if field.isVisible() and key not in ('angle', 'angular_spacing'):
                        self.enter(field, '0.5 in', 12.7)
                        self.assertAlmostEqual(form.value(field), 12.7)
                        checked.add(key)
            self.assertEqual(checked, set(form.units) - {'angle', 'angular_spacing'})
        finally: form.close()
        # The movement task uses the same native InputField with mm dimensionality.
        field = Gui.UiLoader().createWidget('Gui::InputField')
        field.setProperty('unit', 'mm'); field.show()
        try: self.enter(field, '-0.5 in', -12.7)
        finally: field.close()

    def test_mesh_main_and_advanced_linear_fields(self):
        task = Fixtures.task(self); form = task.form
        self.enter(form.controls['spinSurfaceDeviation'], '0.001 in', .0254)
        self.assertAlmostEqual(task.settings()['parameters']['LinearDeflection'], .0254)
        task.addSelection(self.doc.Name, self.box.Name, '')
        self.assertTrue(task.apply(), form.status.text())
        self.assertAlmostEqual(json.loads(task.result.MeshSettings)['parameters']['LinearDeflection'], .0254)
        for index, names in ((0, ('spinSurfaceDeviation',)), (1, ('spinMaximumEdgeLength',)),
                             (3, ('minSize', 'maxSize'))):
            with self.subTest(mesher=index):
                self.assertTrue(form.radios[index].isEnabled())
                form.open_advanced(); form.radios[index].click()
                if index == 1: form.native('checkMaximumEdgeLength').setChecked(True)
                for name in names: self.enter(form.native(name), '0.01 in', .254)
                form.accept_advanced()
                self.assertFalse(form.advanced_dialog.isVisible(), form.advanced_status.text())
                for name in names:
                    self.enter(form.controls[name], '0.02 in', .508)
                    self.assertAlmostEqual(task.number(name), .508)


if __name__ == '__main__': unittest.main()
