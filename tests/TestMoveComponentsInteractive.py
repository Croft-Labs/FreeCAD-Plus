# SPDX-License-Identifier: LGPL-2.1-or-later
import unittest
import os
import tempfile
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
        widget, point = self.handle_pixel(task)
        view = Gui.activeDocument().activeView()
        camera = view.getCamera()
        pivot = App.Placement(task.manipulator.pivot)
        start = QtCore.QPoint(round(widget.width()*.6), round(widget.height()*.12))
        end = start + QtCore.QPoint(45, 25)
        QtTest.QTest.mouseMove(widget, start)
        QtTest.QTest.mousePress(widget, QtCore.Qt.MiddleButton, QtCore.Qt.NoModifier, start)
        self.drag_motion(widget, start, end, QtCore.Qt.MiddleButton)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.MiddleButton, QtCore.Qt.NoModifier, end)
        settle(100)
        self.assertNotEqual(view.getCamera(), camera, "Native camera navigation must remain available")
        self.assertEqual(before, task.session.signature())
        self.assertTrue(task.manipulator.pivot.isSame(pivot, 1e-8))
        self.assertTrue(task.session.interactive_delta.isIdentity())

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
        viewport = view.getViewer().getSoRenderManager().getViewportRegion()
        target = task.manipulator.node.getPart(handle, False)
        pivot = task.session.frame().multVec(task.manipulator.pivot.Base)
        cx,cy = view.getPointOnScreen(pivot)
        # Center the active handles in unobscured canvas at small/high-DPI sizes.
        # This changes only the view camera, never the pivot or component delta.
        camera = view.getCameraNode()
        height = camera.height.getValue()
        orientation = camera.orientation.getValue()
        right = orientation.multVec(coin.SbVec3f(1,0,0))
        up = orientation.multVec(coin.SbVec3f(0,1,0))
        offset_x = (cx/(widget.width()*ratio)-0.25)*height*widget.width()/widget.height()
        offset_y = (cy/(widget.height()*ratio)-0.5)*height
        camera.position.setValue(camera.position.getValue()+right*offset_x+up*offset_y)
        settle(100)
        cx,cy = view.getPointOnScreen(pivot)
        # Pick the actual native handle in its rendered Coin graph, then send Qt events.
        for radius in range(10,150,5):
            perimeter = [(offset,sign*radius) for offset in range(-radius,radius+1,5) for sign in (-1,1)]
            perimeter += [(sign*radius,offset) for offset in range(-radius,radius+1,5) for sign in (-1,1)]
            for dx,dy in perimeter:
                sx,sy = round(cx+dx*ratio), round(cy+dy*ratio)
                point = QtCore.QPoint(round(sx/ratio),widget.height()-round(sy/ratio)-1)
                if not widget.rect().contains(point):
                    continue
                global_point = widget.mapToGlobal(point)
                if not widget.screen().availableGeometry().contains(global_point):
                    continue
                if any(dock.isVisible() and QtCore.QRect(dock.mapToGlobal(QtCore.QPoint()),dock.size()).contains(global_point)
                       for dock in Gui.getMainWindow().findChildren(QtWidgets.QDockWidget)):
                    continue
                action = coin.SoRayPickAction(viewport)
                action.setPoint(coin.SbVec2s(sx,sy))
                action.setRadius(0.)
                # The user scene excludes the camera; use the full renderer root.
                action.apply(view.getViewer().getSoRenderManager().getSceneGraph())
                picked = action.getPickedPoint()
                if picked and picked.getPath().containsNode(target):
                    # A near-edge tolerance hit can miss after Qt/DPR rounding.
                    # Require a small interior patch of the actual native part.
                    interior = True
                    for ox, oy in ((-1,-1),(-1,1),(1,-1),(1,1)):
                        action.setPoint(coin.SbVec2s(sx+ox,sy+oy))
                        action.apply(view.getViewer().getSoRenderManager().getSceneGraph())
                        point_pick = action.getPickedPoint()
                        if not point_pick or not point_pick.getPath().containsNode(target):
                            interior = False
                            break
                    if not interior:
                        continue
                    QtTest.QTest.mouseMove(widget, point + QtCore.QPoint(8, 8))
                    settle(25)
                    QtTest.QTest.mouseMove(widget, point)
                    settle(60)
                    # Each case is a distinct single drag, not the viewer's
                    # double-click candidate (which defers the next press).
                    settle(QtWidgets.QApplication.doubleClickInterval() + 80)
                    return widget, point
        self.fail("No rendered native handle pick found; handle GUI acceptance did not pass.")

    def axis_drag_end(self, task, widget, start):
        view = Gui.activeDocument().activeView()
        pivot = task.session.frame().multiply(task.manipulator.pivot)
        x0, y0 = view.getPointOnScreen(pivot.Base)
        x1, y1 = view.getPointOnScreen(pivot.multVec(App.Vector(10, 0, 0)))
        dx, dy = x1-x0, y0-y1
        length = (dx*dx+dy*dy)**.5
        self.assertGreater(length, 1., "Native X handle must have a usable screen projection")
        return start + QtCore.QPoint(round(45*dx/length), round(45*dy/length))

    def drag_motion(self, widget, start, end, button=QtCore.Qt.LeftButton):
        # A real drag supplies a motion stream, including threshold activation.
        for fraction in (.33, .66, 1.):
            point = start + QtCore.QPoint(round((end.x()-start.x())*fraction),
                                         round((end.y()-start.y())*fraction))
            QtTest.QTest.mouseMove(widget, point)
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(point),
                                     QtCore.QPointF(widget.mapToGlobal(point)), QtCore.Qt.NoButton,
                                     button, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget, event)
            settle(25)

    def test_actual_native_handle_press_drag_release_and_escape(self):
        task = self.task()
        widget, start = self.handle_pixel(task)
        before, undo = task.session.signature(), self.doc.UndoCount
        end = self.axis_drag_end(task, widget, start)
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, start)
        settle(20)
        self.drag_motion(widget, start, end)
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
        end = self.axis_drag_end(task, widget, start)
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, start)
        settle(30)
        self.assertTrue(task.manipulator.dragging, repr({"start": (start.x(),start.y()), "ratio": widget.devicePixelRatioF(), "size": (widget.width(),widget.height()), "pivot": str(task.manipulator.pivot), "status": task.status.text()}))
        self.drag_motion(widget, start, end)
        released_preview = App.Placement(task.session.interactive_delta)
        self.assertFalse(released_preview.isIdentity(), "Second native drag did not update its preview")
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,end)
        settle(60)
        self.assertFalse(task.manipulator.dragging)
        self.assertFalse(task.session.interactive_delta.isIdentity())
        self.assertTrue(task.session.interactive_delta.isSame(released_preview, 1e-8))
        self.assertEqual(before,task.session.signature())
        self.assertEqual(undo,self.doc.UndoCount)
        # Exercise native plane/ring picking as well as the axis handle. Each
        # release composes preview only, with no placement writes or Undo item.
        for handle in ("xyPlanarTranslatorDragger", "zRotatorDragger.dragger"):
            previous = App.Placement(task.session.interactive_delta)
            widget, start = self.handle_pixel(task, handle)
            end = start + QtCore.QPoint(28, -19)
            QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, start)
            self.drag_motion(widget, start, end)
            QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, end)
            settle(60)
            self.assertFalse(task.manipulator.dragging)
            self.assertFalse(task.session.interactive_delta.isSame(previous, 1e-8))
            self.assertEqual(before, task.session.signature())
            self.assertEqual(undo, self.doc.UndoCount)
        retained = App.Placement(task.session.interactive_delta)
        pivot = App.Placement(task.manipulator.pivot)
        task.pivot_mode.setCurrentIndex(1)
        widget, start = self.handle_pixel(task)
        end = self.axis_drag_end(task, widget, start)
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,start)
        self.drag_motion(widget, start, end)
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
        self.assertTrue(task.session.interactive_delta.isIdentity())
        self.vector(task.manipulator.pivot.Base, task.session.group_pivot())
        self.assertTrue(task.manipulator.pivot.Rotation.isSame(App.Rotation(), 1e-8))
        names = (self.first.Name, self.second.Name, self.descendant.Name)
        placements = [App.Placement(self.doc.getObject(name).LinkPlacement) for name in names]
        applied_undo = self.doc.UndoCount
        self.assertTrue(task.accept())
        self.assertEqual(self.doc.UndoCount, applied_undo)
        self.doc.undo()
        self.assertTrue(self.first.LinkPlacement.isSame(App.Placement(), 1e-8))
        self.doc.redo()
        files = []
        for extension in ("FCStd", "cadprt"):
            filename = str(Path(tempfile.gettempdir()) / ("interactive-event-roundtrip." + extension))
            self.doc.saveAs(filename)
            files.append(filename)
        App.closeDocument(self.doc.Name)
        for filename in files:
            document = App.openDocument(filename)
            for name, placement in zip(names, placements):
                self.assertTrue(document.getObject(name).LinkPlacement.isSame(placement, 1e-8))
            App.closeDocument(document.Name)
