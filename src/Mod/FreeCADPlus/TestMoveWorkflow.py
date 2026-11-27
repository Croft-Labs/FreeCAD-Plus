# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native occurrence movement, collectors, Coin handles and persistence."""
import hashlib
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtGui, QtTest, QtWidgets
from pivy import coin
from freecad_plus import document, hierarchy, editing, panel, movement, constraints
from freecad_plus import movement_math as rigid


def settle(): QtTest.QTest.qWait(90)


class TestMoveWorkflow(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ: self.skipTest('Isolated validation directory required')
        self.before = set(App.listDocuments())
        self.output = Path(os.environ['PLUS_TEST_DIR']) / ('m-' + hashlib.sha256(self._testMethodName.encode()).hexdigest()[:8])
        self.output.mkdir(exist_ok=True)
        Gui.Selection.clearSelection(); settle()
        self.doc = document.new_document('MoveFixture'); self.root = document.validate(self.doc)
        self.parent = self.root.Definitions[0]; self.parent.Label = 'Machine'
        self.child = hierarchy.create_definition(self.doc, 'Motor')
        with document.transaction(self.doc, 'Geometry'):
            self.solid = self.child.newObject('Part::Box', 'Solid')
            self.solid.Length = 4; self.solid.Width = 3; self.solid.Height = 2
        self.first = hierarchy.add_instance(self.parent, self.child)
        self.second = hierarchy.add_instance(self.parent, self.child, App.Placement(App.Vector(15, 4, 0), App.Rotation(App.Vector(0, 0, 1), 20)))
        self.top = self.root.Group[0]
        self.top.LinkPlacement = App.Placement(App.Vector(30, 10, 5), App.Rotation(App.Vector(0, 0, 1), 90))
        self.doc.recompute()
        editing.edit((self.top,))
        self.dock = panel.show_panel(); self.dock.activate_assembly(self.parent, (self.top,))
        self.dock.tabs.setCurrentIndex(1); settle()
        self.view = Gui.activeDocument().activeView(); self.view.viewAxonometric(); self.view.fitAll()

    def tearDown(self):
        if movement._active: movement._active.finish()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before: App.closeDocument(name)
        settle()

    def row(self, *path):
        refs = tuple(panel.identity(o) for o in (self.top, *path))
        return next(item.data(0, panel._ROLE) for item in self.dock._maps[1].values()
                    if item.data(0, panel._ROLE).path == refs)

    def task(self, *links):
        task = self.dock.move_rows([self.row(link) for link in links]); settle()
        self.assertFalse(task.closed); return task

    def close_enough(self, value, expected): self.assertLess((value - expected).Length, 1e-6)

    def pick(self, task, key, obj, sub):
        QtTest.QTest.mouseClick(task.ref_widgets[key].viewport(), QtCore.Qt.LeftButton)
        Gui.Selection.addSelection(obj.Document.Name, obj.Name, sub); settle()
        self.assertIn(key, task.refs, task.message.text())

    def test_vector_group_parent_frame_apply_undo_redo_cancel_save(self):
        context = self.dock._context(self.doc, self.view); top = App.Placement(self.top.LinkPlacement)
        start = App.Placement(self.second.LinkPlacement); undo = self.doc.UndoCount
        task = self.task(self.first, self.second)
        task.direction.setCurrentIndex(5)
        for field, value in zip(task.vector_fields, (3, 4, 0)): field.setValue(value)
        task.distance.setProperty('rawValue', 10.0); task.update_preview(); settle()
        self.assertIsNotNone(task.overlay, task.message.text()); self.assertEqual(self.doc.UndoCount, undo)
        self.close_enough(self.first.LinkPlacement.Base, App.Vector())
        task.apply(); settle()
        self.close_enough(self.first.LinkPlacement.Base, App.Vector(6, 8, 0))
        self.close_enough(self.second.LinkPlacement.Base, start.Base + App.Vector(6, 8, 0))
        self.assertTrue(self.second.LinkPlacement.Rotation.isSame(start.Rotation, 1e-8))
        self.assertTrue(self.top.LinkPlacement.isSame(top, 1e-8)); self.assertEqual(self.doc.UndoCount, undo + 1)
        self.assertEqual(self.dock._context(self.doc, self.view), context)
        self.assertFalse(task.paths);self.assertFalse(task.apply_button.isEnabled())
        self.assertEqual(task.kind.currentText(),'Move');self.assertEqual(task.method.currentText(),'Distance and vector')
        self.assertEqual(self.doc.UndoCount, undo + 1)
        task.distance.setProperty('rawValue', 99.0); task.reject(); settle()
        self.close_enough(self.first.LinkPlacement.Base, App.Vector(6, 8, 0))
        self.doc.undo(); self.doc.recompute(); settle(); self.close_enough(self.first.LinkPlacement.Base, App.Vector())
        self.doc.redo(); self.doc.recompute(); settle(); self.close_enough(self.first.LinkPlacement.Base, App.Vector(6, 8, 0))
        document.save_document(self.doc, self.output / 'Moved.cadprt')
        (self.output / 'expected.json').write_text(json.dumps({'file': self.doc.FileName, 'first': self.first.Name, 'top': self.top.Name,
            'placement': list(self.first.LinkPlacement.toMatrix().A), 'topPlacement': list(top.toMatrix().A)}))

    def test_fixed_root_toolbar_and_click_collectors(self):
        with self.assertRaisesRegex(ValueError, 'fixed'): self.dock.move_rows([self.row()])
        QtTest.QTest.mouseClick(self.dock.move_button, QtCore.Qt.LeftButton); settle()
        task = movement._active; self.assertIsNotNone(task); self.assertEqual(task.paths, [])
        Gui.Selection.addSelection(*self.row(self.first).selection); settle()
        self.assertEqual(len(task.paths), 1, task.message.text())
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(*self.row(self.second).selection); settle()
        self.assertEqual(len(task.paths), 2, task.message.text())
        task.components.item(0).setSelected(True); QtTest.QTest.keyClick(task.components, QtCore.Qt.Key_Delete)
        self.assertEqual(len(task.paths), 1)
        task.clear(); self.assertEqual(task.paths, [])

    def test_point_picks_and_orientation_preserved(self):
        task = self.task(self.first); task.method.setCurrentText('Point to point'); settle()
        prefix = hierarchy.subname((self.top, self.first)) + self.solid.Name + '.'
        self.pick(task, 'from', self.root, prefix + 'Vertex1')
        self.pick(task, 'to', self.root, hierarchy.subname((self.top,)) + self.parent.Origin.Name + '.')
        delta = task.refs['to'] - task.refs['from']; rotation = App.Rotation(self.first.LinkPlacement.Rotation)
        task.apply(); self.close_enough(self.first.LinkPlacement.Base, delta)
        self.assertTrue(self.first.LinkPlacement.Rotation.isSame(rotation, 1e-8))

    def test_rotate_two_points_pivot_reverse(self):
        task = self.task(self.first, self.second); task.kind.setCurrentText('Rotate'); settle()
        task.axis.setCurrentIndex(4); task.refs.update({'from': App.Vector(1, 2, 0), 'to': App.Vector(1, 2, 4), 'pivot': App.Vector(5, 3, 0)})
        task.angle.setProperty('rawValue', 90.0); task.reverse.setChecked(True)
        before = App.Placement(self.second.LinkPlacement); expected = rigid.rotation(App.Vector(5, 3, 0), App.Vector(0, 0, 1), -90)
        task.apply(); self.assertTrue(self.second.LinkPlacement.isSame(expected.multiply(before), 1e-7))

    def test_axes_coincident_parallel_reverse(self):
        with document.transaction(self.doc, 'Axis references'):
            shaft = self.parent.newObject('Part::Cylinder', 'Shaft')
        task = self.task(self.first); task.kind.setCurrentText('Align')
        prefix = hierarchy.subname((self.top,)) + shaft.Name + '.'
        circle = next(i + 1 for i, edge in enumerate(shaft.Shape.Edges) if isinstance(edge.Curve, Part.Circle))
        cylinder = next(i + 1 for i, face in enumerate(shaft.Shape.Faces) if isinstance(face.Surface, Part.Cylinder))
        self.pick(task, 'source_axis', self.root, prefix + 'Edge' + str(circle))
        self.pick(task, 'target_axis', self.root, prefix + 'Face' + str(cylinder))
        self.close_enough(task.refs['source_axis'][1], App.Vector(0, 0, 1))
        self.assertAlmostEqual(abs(task.refs['target_axis'][1].z), 1.0)
        self.close_enough(task.refs['target_axis'][1].cross(App.Vector(0, 0, 1)), App.Vector())
        source = (App.Vector(4, 0, 2), App.Vector(0, 0, 1)); target = (App.Vector(9, 8, 7), App.Vector(1, 0, 0))
        task.refs.update(source_axis=source, target_axis=target); task.reverse.setChecked(True)
        move = task.motion(); self.close_enough(move.multVec(source[0]), App.Vector(4, 8, 7)); self.close_enough(move.Rotation.multVec(source[1]), -target[1])
        task.alignment.setCurrentIndex(1); move = task.motion(); self.close_enough(move.multVec(source[0]), source[0])
        task.apply(); self.assertTrue(self.first.LinkPlacement.isSame(move, 1e-8))

    def test_frames_roll_and_degenerate_axes(self):
        task = self.task(self.first); task.kind.setCurrentText('Align'); task.method.setCurrentText('Coordinate systems')
        source = App.Placement(App.Vector(1, 2, 3), App.Rotation(App.Vector(1, 0, 0), 25))
        target = App.Placement(App.Vector(8, 7, 6), App.Rotation(App.Vector(0, 0, 1), 73))
        task.refs.update(source_frame=source, target_frame=target)
        self.assertTrue(task.motion().multiply(source).isSame(target, 1e-7))
        task.advanced.setChecked(True)
        for name, frame in (('source', source), ('target', target)):
            task.refs[name + '_o'] = frame.Base
            for axis, vector in (('x', App.Vector(1, 0, 0)), ('z', App.Vector(0, 0, 1))):
                task.refs[name + '_' + axis] = (frame.Base, frame.Rotation.multVec(vector))
        self.assertTrue(task.motion().multiply(source).isSame(target, 1e-7))
        task.refs['source_x'] = task.refs['source_z']
        with self.assertRaisesRegex(ValueError, 'parallel'): task.apply()

    def test_dynamic_native_handles_numeric_snap_pivot_and_cleanup(self):
        task = self.task(self.first); scene = task.scene; count = scene.getNumChildren()
        task.method.setCurrentText('Dynamic drag'); settle()
        self.assertIsNotNone(task.handles, task.message.text()); self.assertEqual(len(task.handles.entries), 6)
        undo = self.doc.UndoCount; task.snap.setChecked(True); task.increment.setProperty('rawValue', 2.0)
        task.components.setFocus(); task.drag_value.setText('5.1 mm'); task.numeric_drag(); settle()
        self.assertFalse(task.message.error, task.message.text()); self.close_enough(task.motion().Base, App.Vector(6, 0, 0))
        self.assertEqual(self.doc.UndoCount, undo); self.close_enough(self.first.LinkPlacement.Base, App.Vector())
        task.control.setCurrentIndex(1); pivot = task.dynamic_pivot(); task.drag_value.setText('3 mm'); task.numeric_drag()
        self.close_enough(task.dynamic_pivot(), pivot + App.Vector(4, 0, 0)); self.close_enough(task.motion().Base, App.Vector(6, 0, 0))
        handles = task.handles
        task.control.setCurrentIndex(0); task.apply(); self.close_enough(self.first.LinkPlacement.Base, App.Vector(6, 0, 0))
        self.assertIsNone(task.handles)
        task.reject(); settle(); self.assertTrue(handles.closed); self.assertLess(scene.getNumChildren(), count + 1)

    def test_dynamic_native_translation_and_rotation_callbacks(self):
        task = self.task(self.first); task.method.setCurrentText('Dynamic drag'); settle()
        handles = task.handles; handles.start(1)
        handles.entries[1][0].translation.setValue(7, 0, 0); handles.changed(1)
        self.close_enough(task.motion().Base, App.Vector(0, 7, 0)); self.close_enough(self.first.LinkPlacement.Base, App.Vector())
        handles.end(1); settle(); self.assertTrue(handles.closed)
        task.kind.setCurrentText('Rotate'); task.method.setCurrentText('Dynamic drag'); settle()
        self.assertIsNotNone(task.handles, task.message.text()); self.assertEqual(len(task.handles.entries), 3)
        handles = task.handles; handles.start(2)
        handles.entries[2][0].rotation.setValue(coin.SbVec3f(0, 0, 1), 1.5707963267948966); handles.changed(2)
        self.close_enough(task.motion().Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(0, 1, 0))
        task.apply(); self.close_enough(self.first.LinkPlacement.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(0, 1, 0))

    def test_invalid_values_readonly_expression_constraint_and_scale(self):
        self.first.setPropertyStatus('LinkPlacement', 'ReadOnly')
        with self.assertRaisesRegex(ValueError, 'read-only'): self.task(self.first)
        self.first.setPropertyStatus('LinkPlacement', '-ReadOnly')
        self.first.setExpression('LinkPlacement.Base.x', '3')
        with self.assertRaisesRegex(ValueError, 'expression'): self.task(self.first)
        self.first.setExpression('LinkPlacement.Base.x', None); self.first.LinkPlacement = App.Placement()
        task = self.task(self.first); task.direction.setCurrentIndex(5)
        for field in task.vector_fields: field.setValue(0)
        with self.assertRaisesRegex(ValueError, 'nonzero'): task.apply()
        task.direction.setCurrentIndex(0); task.distance.setText('2 deg')
        with self.assertRaisesRegex(ValueError, 'valid'): task.apply()
        task.reject(); settle()
        joint = constraints.create(self.parent, 'Fixed', [(self.parent.Origin, ['', '']), (self.first, ['', ''])]); settle()
        with self.assertRaisesRegex(ValueError, 'constrained'): self.task(self.first)
        constraints.remove(joint); settle(); task = self.task(self.first)
        self.first.Scale = 2
        with self.assertRaisesRegex(ValueError, 'Scaled'): task.apply()
        self.first.Scale = 1

    def test_atomic_failure_context_and_view_cleanup(self):
        task = self.task(self.first, self.second); task.distance.setProperty('rawValue', 5.0)
        before = App.Placement(self.second.LinkPlacement); undo = self.doc.UndoCount; validate = document.validate
        def fail(doc):
            if self.first.LinkPlacement.Base.x != 0: raise ValueError('Injected validation failure')
            return validate(doc)
        with patch.object(document, 'validate', side_effect=fail):
            with self.assertRaisesRegex(ValueError, 'Injected'): task.apply()
        self.assertEqual(self.doc.UndoCount, undo); self.close_enough(self.first.LinkPlacement.Base, App.Vector())
        self.assertTrue(self.second.LinkPlacement.isSame(before, 1e-8))
        task.method.setCurrentText('Dynamic drag'); settle(); handles = task.handles
        editing.edit((self.top, self.first)); settle(); self.assertTrue(task.closed); self.assertTrue(handles.closed)

    def test_actual_viewport_arrow_release_escape_and_ring(self):
        task = self.task(self.first); task.method.setCurrentText('Dynamic drag'); settle()
        widget = self.view.graphicsView().viewport(); self.view.viewTop(); self.view.fitAll(); settle()
        def screen(point):
            pixel = self.view.getPointOnScreen(task.parent_frame().multVec(point)); ratio = widget.devicePixelRatioF()
            return QtCore.QPoint(round(pixel[0] / ratio), widget.height() - 1 - round(pixel[1] / ratio))
        def gesture(start, end, escape=False):
            self.view.redraw(); QtTest.QTest.qWait(120)
            first, last = screen(start), screen(end)
            self.assertTrue(widget.rect().contains(first), (first, widget.rect()))
            hover = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(first), QtCore.QPointF(widget.mapToGlobal(first)),
                                     QtCore.Qt.NoButton, QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget, hover); settle()
            handles = task.handles
            QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, first); settle()
            self.assertTrue(handles.dragging, 'The viewport did not grab the native handle')
            for step in range(1, 6):
                pos = first + (last - first) * (step / 5)
                event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos), QtCore.QPointF(widget.mapToGlobal(pos)),
                                         QtCore.Qt.NoButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
                QtWidgets.QApplication.sendEvent(widget, event); QtTest.QTest.qWait(20)
            if escape: QtTest.QTest.keyClick(widget, QtCore.Qt.Key_Escape)
            QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, last); settle()
        pivot = task.dynamic_pivot(); size = max(5., task.selection_size() * .45)
        gesture(pivot + App.Vector(size * .9, 0, 0), pivot + App.Vector(size * .9 + 5, 0, 0))
        self.assertGreater(task.motion().Base.x, 4); self.close_enough(self.first.LinkPlacement.Base, App.Vector())
        first_move = task.motion()
        pivot = task.dynamic_pivot()
        (self.output / 'drag.json').write_text(json.dumps({'pivot': list(pivot), 'handlePivot': list(task.handles.base_pivot),
            'pending': list(first_move.Base), 'handleCount': task.scene.getNumChildren(), 'message': task.message.text()}))
        gesture(pivot + App.Vector(size * .9, 0, 0), pivot + App.Vector(size * .9 + 3, 0, 0), escape=True)
        self.assertTrue(task.motion().isSame(first_move, 1e-6))
        task.form.grab().save(str(self.output / 'dynamic-task.png'))
        task.apply(); self.assertGreater(self.first.LinkPlacement.Base.x, 4)
        task.add_rows([self.row(self.first)])
        task.kind.setCurrentText('Rotate'); task.method.setCurrentText('Dynamic drag'); settle()
        pivot = task.dynamic_pivot(); size = max(5., task.selection_size() * .45)
        gesture(pivot + App.Vector(size * .707, size * .707, 0), pivot + App.Vector(-size * .707, size * .707, 0))
        self.assertAlmostEqual(task.motion().Rotation.Angle, 1.5707963267948966, delta=.08,
                               msg=(task.handle.currentIndex(), task.message.text(), task.drag_value.text()))
        self.view.saveImage(str(self.output / 'rings.png'), 1000, 700, 'Current')
        task.reject()

    def test_nested_shared_parent_mixed_parent_rejection(self):
        grand = hierarchy.create_definition(self.doc, 'Pin')
        pin = hierarchy.add_instance(self.child, grand, App.Placement(App.Vector(2, 0, 0), App.Rotation()))
        self.doc.recompute(); settle()
        task = self.dock.move_rows([self.row(self.second, pin)]); settle()
        self.assertEqual(task.check()[0], self.child)
        with self.assertRaisesRegex(ValueError, 'siblings'): task.add_rows([self.row(self.first, pin)])
        with self.assertRaisesRegex(ValueError, 'siblings'): task.add_rows([self.row(self.first)])
        frame = hierarchy.world_placement(self.doc, (self.top, self.second))
        self.assertTrue(task.parent_frame().isSame(frame, 1e-7))
        task.direction.setCurrentIndex(1); task.distance.setProperty('rawValue', 8.0); task.apply()
        self.close_enough(pin.LinkPlacement.Base, App.Vector(2, 8, 0))
        for link in (self.first, self.second):
            world = hierarchy.world_placement(self.doc, (self.top, link, pin))
            expected = hierarchy.world_placement(self.doc, (self.top, link)).multVec(App.Vector(2, 8, 0))
            self.close_enough(world.Base, expected)

    def test_unused_assembly_anchor_and_reference_eligibility(self):
        from freecad_plus import display
        unused = hierarchy.create_definition(self.doc, 'Unused assembly')
        one = hierarchy.add_instance(unused, self.child)
        settle()
        self.dock.edit_row(next(item.data(0, panel._ROLE) for item in self.dock._maps[0].values() if item.data(0, panel._ROLE).ref == panel.identity(unused)))
        self.dock.activate_assembly(unused); settle()
        row = next(item.data(0, panel._ROLE) for item in self.dock._maps[1].values() if item.data(0, panel._ROLE).kind == 'occurrence')
        self.assertTrue(row.anchor)
        task = self.dock.move_rows([row]); settle(); task.distance.setProperty('rawValue', 7.0); task.update_preview()
        self.assertIsNotNone(task.overlay); task.apply(); self.close_enough(one.LinkPlacement.Base, App.Vector(7, 0, 0)); task.reject()
        display.set_state(unused, one, part_type='Reference'); settle()
        task = self.dock.move_rows([row]); task.method.setCurrentText('Point to point'); settle()
        task.collect('from'); Gui.Selection.addSelection(unused.Document.Name, unused.Name, one.Name + '.' + self.solid.Name + '.Vertex1')
        settle(); self.assertNotIn('from', task.refs); self.assertIn('Reference', task.message.text())

    def test_external_parent_owns_move_and_source_persistence(self):
        from freecad_plus import external
        document.save_document(self.doc, self.output / 'Host.cadprt')
        source = document.new_document('Source'); root = document.validate(source); owner = root.Definitions[0]
        child = hierarchy.create_definition(source, 'Imported pin'); instance = hierarchy.add_instance(owner, child)
        document.save_document(source, self.output / 'Source.cadprt'); external.import_file(self.doc, source)
        link = hierarchy.add_instance(self.parent, owner)
        document.save_document(self.doc); checksum = hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest()
        App.setActiveDocument(self.doc.Name); settle(); self.dock.activate_assembly(self.parent, (self.top,)); settle()
        task = self.dock.move_rows([self.row(link, instance)]); settle(); undo = source.UndoCount
        task.distance.setProperty('rawValue', 9.0); task.apply(); task.reject()
        self.assertEqual(source.UndoCount, undo + 1); self.close_enough(instance.LinkPlacement.Base, App.Vector(9, 0, 0))
        external.save_definition(owner)
        self.assertEqual(hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest(), checksum)

    def test_preview_toggle_method_reset_apply_then_ok_and_clear(self):
        task = self.task(self.first); undo = self.doc.UndoCount
        task.distance.setText('4 mm'); task.auto.setChecked(False); task.update_preview()
        self.assertIsNone(task.overlay); task.update_preview(force=True); self.assertIsNotNone(task.overlay)
        task.method.setCurrentText('Point to point'); self.assertEqual(self.doc.UndoCount, undo)
        task.refs.update({'from': App.Vector(), 'to': App.Vector(0, 5, 0)})
        task.apply(); settle(); self.assertEqual(self.doc.UndoCount, undo + 1)
        task.accept(); settle(); self.assertTrue(task.closed); self.assertEqual(self.doc.UndoCount, undo + 1)
        task = self.task(self.first); task.distance.setText('2 mm'); task.apply()
        self.assertEqual(task.paths, []); task.accept(); self.assertTrue(task.closed)

    def test_native_frame_pick_and_dynamic_plane_snap(self):
        task = self.task(self.first); task.kind.setCurrentText('Align'); task.method.setCurrentText('Coordinate systems')
        origin = hierarchy.subname((self.top,)) + self.parent.Origin.Name + '.'
        self.pick(task, 'source_frame', self.root, origin)
        self.pick(task, 'target_frame', self.root, origin)
        self.assertTrue(task.motion().isSame(App.Placement(), 1e-7))
        task.kind.setCurrentText('Move'); task.method.setCurrentText('Dynamic drag'); settle()
        handles = task.handles; task.snap.setChecked(True); task.increment.setText('2 mm')
        handles.start(3); handles.entries[3][0].translation.setValue(3.1, 4.8, 0); handles.changed(3)
        self.close_enough(task.motion().Base, App.Vector(4, 4, 0))
        handles.end(3); settle(); task.handle.setCurrentIndex(0); task.components.setFocus(); task.drag_value.setText('2 mm')
        self.close_enough(task.motion().Base, App.Vector(6, 4, 0))
        task.drag_value.setText('4 mm'); self.close_enough(task.motion().Base, App.Vector(8, 4, 0))
        task.apply(); self.close_enough(self.first.LinkPlacement.Base, App.Vector(8, 4, 0))
