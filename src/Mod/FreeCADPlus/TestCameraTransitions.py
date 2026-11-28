# SPDX-License-Identifier: LGPL-2.1-or-later
"""Camera ownership and stable component fits with native animation enabled."""
import json
import math
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest
from freecad_plus import document, editing, panel
import TestComponentPanel as fixtures


def frame(view):
    camera = view.getCameraNode()
    return dict(position=list(camera.position.getValue().getValue()),
                rotation=list(camera.orientation.getValue().getValue()),
                focal=float(camera.focalDistance.getValue()),
                scale=float((camera.height if hasattr(camera, 'height') else camera.heightAngle).getValue()))


class TestCameraTransitions(unittest.TestCase):
    tearDown = fixtures.TestComponentPanel.tearDown
    rows = fixtures.TestComponentPanel.rows
    model = fixtures.TestComponentPanel.model
    occurrence = fixtures.TestComponentPanel.occurrence
    click = fixtures.TestComponentPanel.click

    def setUp(self):
        fixtures.TestComponentPanel.setUp(self)
        self.view = Gui.activeDocument().activeView()
        self.view.setAnimationEnabled(False)
        self.view.viewAxonometric(); self.view.fitAll(); QtTest.QTest.qWait(100)
        self.view.setAnimationEnabled(True)

    def same_frame(self, actual, expected, tolerance=1e-4):
        for key in ('position', 'rotation'):
            for a, b in zip(actual[key], expected[key]):
                self.assertAlmostEqual(a, b, delta=tolerance, msg=key)
        for key in ('focal', 'scale'):
            self.assertAlmostEqual(actual[key], expected[key], delta=tolerance, msg=key)

    def record(self, name, action, duration=550):
        frames = []
        def sample():
            frames.append(frame(Gui.activeDocument().activeView()))
        timer = QtCore.QTimer(); timer.timeout.connect(sample); timer.start(5)
        try:
            sample(); action(); sample(); QtTest.QTest.qWait(duration); sample()
        finally:
            timer.stop()
        (self.output / (name + '.json')).write_text(json.dumps(frames, indent=2))
        return frames

    def test_restore_camera_cancels_old_rotation(self):
        saved = self.view.getCamera(); expected = frame(self.view)
        self.record('restore', lambda: (self.view.viewBottom(), self.view.setCamera(saved)), 650)
        self.same_frame(frame(self.view), expected)
        self.assertTrue(self.view.isAnimationEnabled())

    def test_fit_has_no_nested_event_loop_and_reaches_one_target(self):
        editing.edit_unused(self.doc, self.child, detached=True)
        QtTest.QTest.qWait(100)
        self.view.setAnimationEnabled(False); self.view.fitAll(); QtTest.QTest.qWait(100)
        expected = frame(self.view); saved = self.view.getCamera()
        camera = self.view.getCameraNode(); camera.height = expected['scale'] * 4
        self.view.setAnimationEnabled(True)
        callback = []
        QtCore.QTimer.singleShot(0, lambda: callback.append(True))
        self.view.fitAll()
        self.assertFalse(callback, 'Fit must not process unrelated activation/display callbacks reentrantly')
        frames = self.record('fit', lambda: None)
        self.same_frame(frames[-1], expected, 2e-3)
        for before, after in zip(frames, frames[1:]):
            self.assertLessEqual(after['scale'], before['scale'] + 1e-4)
            self.assertGreaterEqual(after['scale'], expected['scale'] - 1e-4)
        self.view.setCamera(saved)

    def test_screen_sized_origins_do_not_change_fit_scale(self):
        editing.edit_unused(self.doc, self.child, detached=True); QtTest.QTest.qWait(100)
        self.view.setAnimationEnabled(False)
        scales = []
        for _ in range(3):
            self.view.fitAll(); QtTest.QTest.qWait(100); scales.append(frame(self.view)['scale'])
        self.assertLess(max(scales) - min(scales), 1e-4, scales)
        visibility = {obj.Name: obj.Visibility for obj in self.child.Origin.OriginFeatures}
        self.assertTrue(any(visibility.values()))
        self.view.setAnimationEnabled(True); self.view.fitAll(); QtTest.QTest.qWait(300)
        self.assertEqual(visibility, {obj.Name: obj.Visibility for obj in self.child.Origin.OriginFeatures})
        self.view.saveImage(str(self.output/'origin-visible-after-fit.png'), 800, 600, 'Current')

    def test_orientation_and_fit_share_final_pose_in_both_projections(self):
        for camera_type in ('Orthographic', 'Perspective'):
            with self.subTest(camera_type=camera_type):
                self.view.setAnimationEnabled(False); self.view.setCameraType(camera_type)
                self.view.viewTop(); self.view.fitAll(); QtTest.QTest.qWait(100)
                expected = frame(self.view)
                self.view.viewAxonometric(); self.view.fitAll(); QtTest.QTest.qWait(100)
                self.view.setAnimationEnabled(True)
                frames = self.record(camera_type, lambda: (self.view.viewTop(), self.view.fitAll()))
                self.same_frame(frames[-1], expected, 2e-3)
                self.assertTrue(all(math.isfinite(v) for f in frames for v in (*f['position'], f['scale'], f['focal'])))

    def test_restore_interrupts_pending_fit_without_later_snap(self):
        saved = self.view.getCamera(); expected = frame(self.view)
        self.view.getCameraNode().height = expected['scale'] * 3
        self.view.fitAll(); QtTest.QTest.qWait(50); self.view.setCamera(saved)
        frames = self.record('interrupt-fit', lambda: None)
        for current in frames:self.same_frame(current, expected)

    def test_scaled_fit_supersedes_pending_fit(self):
        self.view.getCameraNode().height = 150
        self.view.fitAll(); QtTest.QTest.qWait(40)
        self.view.fitAll(1.4)
        expected = frame(self.view)
        for current in self.record('scaled-fit', lambda: None):self.same_frame(current, expected)

    def test_projection_switch_stops_old_fit(self):
        self.view.getCameraNode().height = 150
        self.view.fitAll(); QtTest.QTest.qWait(40)
        self.view.setCameraType('Perspective')
        expected = frame(self.view)
        for current in self.record('projection-switch', lambda: None):self.same_frame(current, expected)

    def test_parts_and_assembly_double_click_preserve_camera(self):
        expected = frame(self.view); undo = self.doc.UndoCount
        for index, item in ((0, self.model(self.parent)), (0, self.model(self.child)),
                            (1, self.occurrence((self.second, self.nested)))):
            frames = self.record('activate-' + str(index) + '-' + item.text(0),
                                 lambda i=index, row=item: self.click(i, row, double=True))
            for current in frames:self.same_frame(current, expected)
        self.assertEqual(self.doc.UndoCount, undo)

    def test_new_component_view_has_stable_fit_and_preserves_source(self):
        original = self.view; expected = frame(original); undo = self.doc.UndoCount
        frames = self.record('new-view', lambda: editing.open_component_view(self.doc, self.child, detached=True))
        new = Gui.activeDocument().activeView(); self.assertNotEqual(new, original)
        self.same_frame(frame(original), expected)
        settled = frame(new); new.fitAll(); QtTest.QTest.qWait(300)
        self.same_frame(frame(new), settled, 2e-3)
        self.assertEqual(self.doc.UndoCount, undo)

    def test_gui_reopen_keeps_saved_camera_and_active_part(self):
        sole = document.new_document('CameraFile'); part = document.validate(sole).Definitions[0]
        import Part
        result = part.newObject('Part::Feature', 'Solid'); result.Shape = Part.makeBox(40,25,12)
        sole.recompute(); view = Gui.activeDocument().activeView()
        view.setAnimationEnabled(False); view.viewAxonometric(); view.fitAll(); QtTest.QTest.qWait(100)
        view.getCameraNode().height = 135
        expected = frame(view); path = self.output/'camera.cadprt'; document.save_document(sole,path)
        App.closeDocument(sole.Name)
        Gui.loadFile(str(path),'freecad_plus.document_import'); QtTest.QTest.qWait(650)
        current = App.ActiveDocument
        self.same_frame(frame(Gui.activeDocument().activeView()), expected, 2e-3)
        self.assertEqual(editing.context_path(current)[0], document.validate(current).Definitions[0])
        self.assertEqual(current.UndoCount, 0)
        self.assertFalse(Gui.getDocument(current.Name).Modified)
