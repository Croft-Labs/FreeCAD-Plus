# SPDX-License-Identifier: LGPL-2.1-or-later
import unittest
import os
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest
from pivy import coin
from freecad.gui import MoveComponentsTask as UI
from freecad.gui import DesignSelection
from TestMoveComponentsRotate import TestMoveComponentsRotate as Rotate
from TestConstraintPalette import settle


class TestMoveComponentsInteractive(unittest.TestCase):
    setUp, tearDown = Rotate.setUp, Rotate.tearDown
    session, vector, pick = Rotate.session, Rotate.vector, Rotate.pick

    def task(self):
        task = UI.open_task(self.root, self.paths)
        task.workflow.setCurrentIndex(5)
        self.assertIsNotNone(task.manipulator)
        return task

    def test_numeric_composition_nonorigin_rotation_and_apply_undo(self):
        task = self.task()
        signature = task.session.signature()
        task.handle_distance.setProperty("rawValue", 3.)
        task.numeric_gesture()
        first = App.Placement(task.session.interactive_delta)
        pivot = App.Vector(task.manipulator.pivot.Base)
        task.active_handle.setCurrentIndex(8)
        task.handle_angle.setProperty("rawValue", 90.)
        task.numeric_gesture()
        expected = App.Placement(App.Vector(), App.Rotation(App.Vector(0,0,1),90),pivot).multiply(first)
        self.assertTrue(task.session.interactive_delta.isSame(expected, 1e-8))
        self.assertEqual(signature, task.session.signature())
        self.assertTrue(task.apply(), task.status.text())
        self.assertTrue(self.first.LinkPlacement.isSame(expected, 1e-8))
        self.assertTrue(task.session.interactive_delta.isIdentity())
        self.doc.undo()
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))
        self.doc.redo()
        self.assertTrue(self.first.LinkPlacement.isSame(expected, 1e-8))

    def test_inactive_plane_input_does_not_block_axis_numeric_gesture(self):
        task = self.task()
        task.active_handle.setCurrentIndex(3)
        editor = task.handle_secondary.findChild(QtWidgets.QLineEdit)
        self.assertIsNotNone(editor)
        editor.setText("invalid distance")
        self.assertFalse(task.handle_secondary.hasAcceptableInput())
        task.active_handle.setCurrentIndex(0)
        self.assertFalse(task.handle_secondary.isEnabled())
        self.assertFalse(task.handle_angle.isEnabled())
        task.handle_distance.setProperty("rawValue",3.)
        task.numeric_gesture()
        self.vector(task.session.interactive_delta.Base,App.Vector(3,0,0))
        task.active_handle.setCurrentIndex(8)
        self.assertFalse(task.handle_distance.isEnabled())
        self.assertTrue(task.handle_angle.isEnabled())

    def test_pivot_only_and_native_midpoint_pick(self):
        task = self.task()
        before, undo = task.session.signature(), self.doc.UndoCount
        task.pivot_mode.setCurrentIndex(1)
        task.handle_distance.setProperty("rawValue", 7.)
        task.numeric_gesture()
        self.assertTrue(task.session.interactive_delta.isIdentity())
        self.assertEqual(before, task.session.signature())
        self.assertEqual(undo, self.doc.UndoCount)
        task.interactive_pivot_pick.click()
        self.pick(task, self.line, "Edge1")
        self.vector(task.session.frame().multVec(task.manipulator.pivot.Base), App.Vector(2.5,0,0))
        self.assertEqual(before, task.session.signature())
        task.pivot_reset.click()
        self.vector(task.manipulator.pivot.Base, task.session.group_pivot())

    def test_snapping_off_defaults_and_persistence_cleanup(self):
        task = self.task()
        self.assertFalse(task.translation_snap.isChecked())
        self.assertFalse(task.rotation_snap.isChecked())
        self.assertEqual(task.manipulator.node.getField("translationIncrement").getValue(), 0.)
        task.translation_snap.setChecked(True)
        task.snap_distance.setProperty("rawValue", 2.)
        task.handle_distance.setProperty("rawValue", 3.1)
        task.numeric_gesture()
        self.vector(task.session.interactive_delta.Base, App.Vector(4,0,0))
        DesignSelection.parameters().SetBool("Persistent", False)
        self.assertTrue(task.apply())
        self.assertEqual(task.session.paths, [])
        self.assertIsNone(task.manipulator)

    def handle_pixel(self, task, handle="xTranslatorDragger.dragger"):
        view = Gui.activeDocument().activeView()
        view.viewAxonometric()
        view.fitAll()
        settle(150)
        widgets = [w for w in task.window.findChildren(QtWidgets.QWidget)
                   if "GL" in w.metaObject().className() and w.width()>100 and w.height()>100]
        widget = max(widgets, key=lambda w:w.width()*w.height())
        ratio = widget.devicePixelRatioF()
        viewport = coin.SbViewportRegion(round(widget.width()*ratio), round(widget.height()*ratio))
        target = task.manipulator.node.getPart(handle, False)
        pivot = task.session.frame().multVec(task.manipulator.pivot.Base)
        cx,cy = view.getPointOnScreen(pivot)
        # Pick the actual native handle in its rendered Coin graph, then send Qt events.
        for radius in range(10,150,5):
            perimeter = [(offset,sign*radius) for offset in range(-radius,radius+1,5) for sign in (-1,1)]
            perimeter += [(sign*radius,offset) for offset in range(-radius,radius+1,5) for sign in (-1,1)]
            for dx,dy in perimeter:
                sx,sy = round(cx+dx*ratio), round(cy+dy*ratio)
                action = coin.SoRayPickAction(viewport)
                action.setPoint(coin.SbVec2s(sx,sy))
                action.setRadius(3.)
                # The user scene excludes the camera; use the full renderer root.
                action.apply(view.getViewer().getSoRenderManager().getSceneGraph())
                picked = action.getPickedPoint()
                if picked and picked.getPath().containsNode(target):
                    return widget, QtCore.QPoint(round(sx/ratio),widget.height()-round(sy/ratio)-1)
        self.fail("No rendered native handle pick found; handle GUI acceptance did not pass.")

    def test_actual_native_handle_press_drag_release_and_escape(self):
        task = self.task()
        widget, start = self.handle_pixel(task)
        before, undo = task.session.signature(), self.doc.UndoCount
        end = start + QtCore.QPoint(32,-18)
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, start)
        settle(20)
        event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(end),
                                 QtCore.QPointF(widget.mapToGlobal(end)), QtCore.Qt.NoButton,
                                 QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget, event)
        settle(60)
        self.assertTrue(task.manipulator.dragging)
        self.assertFalse(task.session.interactive_delta.isIdentity())
        self.assertTrue(task.ghosts)
        evidence = os.environ.get("FREECAD_PLUS_VALIDATION_DIR")
        if evidence:
            Gui.getMainWindow().grab().save(str(Path(evidence)/"interactive-native-drag.png"))
        self.assertEqual(before, task.session.signature())
        QtTest.QTest.keyClick(widget, QtCore.Qt.Key_Escape)
        settle(60)
        self.assertFalse(task.manipulator.dragging)
        self.assertTrue(task.session.interactive_delta.isIdentity())
        self.assertEqual(task.session.paths, self.paths)
        self.assertEqual(undo, self.doc.UndoCount)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, end)
        widget, start = self.handle_pixel(task)
        end = start + QtCore.QPoint(28,-12)
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, start)
        event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(end),
                                 QtCore.QPointF(widget.mapToGlobal(end)), QtCore.Qt.NoButton,
                                 QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget,event)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,end)
        settle(60)
        self.assertFalse(task.manipulator.dragging)
        self.assertFalse(task.session.interactive_delta.isIdentity())
        self.assertEqual(before,task.session.signature())
        self.assertEqual(undo,self.doc.UndoCount)
        retained = App.Placement(task.session.interactive_delta)
        pivot = App.Placement(task.manipulator.pivot)
        task.pivot_mode.setCurrentIndex(1)
        widget, start = self.handle_pixel(task)
        end = start + QtCore.QPoint(24,-15)
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,start)
        event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(end),
                                 QtCore.QPointF(widget.mapToGlobal(end)), QtCore.Qt.NoButton,
                                 QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget,event)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,end)
        settle(60)
        self.assertFalse(task.manipulator.pivot.isSame(pivot,1e-8))
        self.assertTrue(task.session.interactive_delta.isSame(retained,1e-8))
        self.assertEqual(before,task.session.signature())
        self.assertEqual(undo,self.doc.UndoCount)
        task.pivot_mode.setCurrentIndex(0)
        if evidence:
            Gui.getMainWindow().grab().save(str(Path(evidence)/"interactive-native-pivot.png"))
        self.assertTrue(task.apply(),task.status.text())
