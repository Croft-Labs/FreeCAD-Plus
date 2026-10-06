# SPDX-License-Identifier: LGPL-2.1-or-later
"""View-owned native arrows, planes and rings; never an object's placement editor."""
import math
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui import MoveComponents as Move

HANDLES = ("Translate X", "Translate Y", "Translate Z", "Translate XY",
           "Translate YZ", "Translate ZX", "Rotate X", "Rotate Y", "Rotate Z")
PARTS = ("xTranslatorDragger", "yTranslatorDragger", "zTranslatorDragger",
         "xyPlanarTranslatorDragger", "yzPlanarTranslatorDragger", "zxPlanarTranslatorDragger",
         "xRotatorDragger", "yRotatorDragger", "zRotatorDragger")


class Manipulator(QtCore.QObject):
    def __init__(self, task):
        super().__init__(task.form)
        self.task, self.session = task, task.session
        self.view = Gui.activeDocument().activeView()
        self.scene = self.view.getSceneGraph()
        self.closed = self.dragging = self.block = False
        self.pivot = App.Placement(self.session.group_pivot(), App.Rotation())
        self.node = self.view.createTransformDragger()
        self.callbacks = []
        self.widgets = []
        try:
            for name, callback in (("addStartCallback", self.start), ("addMotionCallback", self.motion),
                                   ("addFinishCallback", self.finish)):
                self.callbacks.append((name, self.view.addDraggerCallback(self.node, name, callback)))
            # Scope Escape to this native viewport; camera input elsewhere is untouched.
            subwindow = task.window
            if subwindow:
                for widget in subwindow.findChildren(QtWidgets.QWidget):
                    if ("View3DInventor" in widget.metaObject().className()
                            or "GL" in widget.metaObject().className()):
                        widget.installEventFilter(self)
                        self.widgets.append(widget)
            self.write()
            self.configure_snap()
        except Exception:
            self.close()
            raise

    def read(self):
        position = self.node.getField("translation").getValue()
        quaternion = self.node.getField("rotation").getValue().getValue()
        return App.Placement(App.Vector(*position), App.Rotation(*quaternion))

    def write(self):
        world = self.session.frame().multiply(self.pivot)
        self.block = True
        try:
            self.node.getField("translation").setValue(*world.Base)
            self.node.getField("rotation").setValue(*world.Rotation.Q)
            for axis in ("X", "Y", "Z"):
                self.node.getField("translationIncrementCount"+axis).setValue(0)
                self.node.getField("rotationIncrementCount"+axis).setValue(0)
        finally:
            self.block = False

    def configure_snap(self):
        task = self.task
        if not task.snap_distance.hasAcceptableInput() or not task.snap_angle.hasAcceptableInput():
            raise ValueError("Enter valid positive snapping increments.")
        distance = float(task.snap_distance.property("rawValue"))
        angle = float(task.snap_angle.property("rawValue"))
        if not math.isfinite(distance) or not math.isfinite(angle) or distance <= 0 or angle <= 0:
            raise ValueError("Snapping increments must be finite and positive.")
        self.node.getField("translationIncrement").setValue(distance if task.translation_snap.isChecked() else 0.)
        self.node.getField("rotationIncrement").setValue(math.radians(angle) if task.rotation_snap.isChecked() else 0.)

    def start(self, node):
        if self.closed or self.block:
            return
        self.configure_snap()
        self.start_world = self.read()
        self.before_delta = App.Placement(self.session.interactive_delta)
        self.before_pivot = App.Placement(self.pivot)
        self.dragging = True
        for index, name in enumerate(PARTS):
            part = self.node.getPart(name if "Planar" in name else name+".dragger", False)
            if part and part.getField("isActive").getValue():
                self.task.active_handle.setCurrentIndex(index)
                break

    def motion(self, node):
        if self.closed or self.block or not self.dragging:
            return
        try:
            current = self.read()
            parent = self.session.frame()
            delta = parent.inverse().multiply(current.multiply(self.start_world.inverse())).multiply(parent)
            if self.task.pivot_mode.currentIndex() == 0:
                self.session.interactive_delta = delta.multiply(self.before_delta)
            self.pivot = parent.inverse().multiply(current)
            self.task.update_preview()
        except Exception as error:
            self.cancel_drag()
            self.task.status.setText(str(error))

    def finish(self, node):
        if self.closed or self.block or not self.dragging:
            return
        self.motion(node)
        self.dragging = False
        self.write()
        self.task.status.setText("Gesture preview retained. Apply commits; Edit Pivot alone never moves components.")

    def cancel_drag(self):
        if not self.dragging:
            return
        self.session.interactive_delta = App.Placement(self.before_delta)
        self.pivot = App.Placement(self.before_pivot)
        self.dragging = False
        # Release Coin's capture so cancellation also restores camera navigation.
        try:
            action = self.view.getViewer().getSoEventManager().getHandleEventAction()
            action.releaseGrabber()
        except (RuntimeError, ReferenceError):
            pass  # The view may already be being destroyed during document close.
        self.write()
        if not self.task.closed:
            self.task.update_preview()

    def eventFilter(self, watched, event):
        if (self.dragging and event.type() == QtCore.QEvent.KeyPress
                and event.key() == QtCore.Qt.Key_Escape):
            self.cancel_drag()
            event.accept()
            return True
        return False

    def numeric(self):
        if self.dragging:
            raise ValueError("Finish or cancel the current drag before numeric entry.")
        task = self.task
        index = task.active_handle.currentIndex()
        widget = task.handle_angle if index >= 6 else task.handle_distance
        if not widget.hasAcceptableInput() or not task.handle_secondary.hasAcceptableInput():
            raise ValueError("Enter valid handle values.")
        value = float(widget.property("rawValue"))
        secondary = float(task.handle_secondary.property("rawValue"))
        if not all(math.isfinite(v) for v in (value, secondary)):
            raise ValueError("Enter finite handle values.")
        self.configure_snap()
        if index >= 6:
            if task.rotation_snap.isChecked():
                step = float(task.snap_angle.property("rawValue"))
                value = round(value/step)*step
            axis = self.pivot.Rotation.multVec(App.Vector(*((1,0,0),(0,1,0),(0,0,1))[index-6]))
            delta = App.Placement(App.Vector(), App.Rotation(axis, value), self.pivot.Base)
        else:
            if task.translation_snap.isChecked():
                step = float(task.snap_distance.property("rawValue"))
                value, secondary = round(value/step)*step, round(secondary/step)*step
            axes = ((0,), (1,), (2,), (0,1), (1,2), (2,0))[index]
            vector = App.Vector()
            for axis, amount in zip(axes, (value, secondary)):
                vector += self.pivot.Rotation.multVec(App.Vector(*((1,0,0),(0,1,0),(0,0,1))[axis])) * amount
            delta = App.Placement(vector, App.Rotation())
        if task.pivot_mode.currentIndex() == 0:
            self.session.interactive_delta = delta.multiply(self.session.interactive_delta)
        self.pivot = delta.multiply(self.pivot)
        self.write()
        self.task.update_preview()
        for widget in (task.handle_distance, task.handle_secondary, task.handle_angle):
            widget.setProperty("rawValue", 0.)

    def close(self):
        if self.closed:
            return
        self.cancel_drag()
        self.closed = True
        for widget in self.widgets:
            try:
                widget.removeEventFilter(self)
            except RuntimeError:
                pass
        for name, callback in self.callbacks:
            try:
                self.view.removeDraggerCallback(self.node, name, callback)
            except (RuntimeError, ReferenceError):
                pass
        self.callbacks.clear()
        try:
            if self.scene.findChild(self.node) >= 0:
                self.scene.removeChild(self.node)
        except (RuntimeError, ReferenceError):
            pass
        self.node = None
