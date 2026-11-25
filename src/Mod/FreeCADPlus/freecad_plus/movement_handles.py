# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Coin arrows, planes and rings. Callbacks change only task preview state."""
import math
import FreeCAD as App
from pivy import coin
from PySide6 import QtCore
from . import movement_math as motion

AXES = (App.Vector(1, 0, 0), App.Vector(0, 1, 0), App.Vector(0, 0, 1))


class Handles:
    def __init__(self, task):
        self.task = task
        self.node = coin.SoSeparator()
        self.callbacks = []
        self.entries = []
        self.dragging = False
        self.closed = False
        self.ignore = False
        self.base_motion = App.Placement(task.pending)
        self.base_pivot = App.Vector(task.dynamic_pivot())
        frame = task.parent_frame()
        transform = coin.SoTransform(); self.transform = transform
        transform.translation = tuple(frame.multVec(self.base_pivot))
        transform.rotation = tuple(frame.Rotation.Q)
        self.node.addChild(transform)
        rotating = task.kind.currentText() == 'Rotate'
        size = max(5.0, task.selection_size() * .45)
        for index in range(3 if rotating else 6):
            branch = coin.SoSeparator()
            orient = coin.SoRotation()
            if rotating:
                rotate = App.Rotation(App.Vector(0, 0, 1), AXES[index])
                dragger = coin.SoRotateDiscDragger()
                self.visual(dragger, 'rotator', size, index)
            elif index < 3:
                rotate = App.Rotation(App.Vector(1, 0, 0), AXES[index])
                dragger = coin.SoTranslate1Dragger()
                self.visual(dragger, 'translator', size, index)
            else:
                # XY, YZ, ZX plane normals. The local plane is XY.
                rotate = App.Rotation(App.Vector(0, 0, 1), AXES[(index - 1) % 3])
                dragger = coin.SoTranslate2Dragger()
                self.visual(dragger, 'translator', size * .28, (index - 1) % 3)
            orient.rotation = tuple(rotate.Q)
            branch.addChild(orient)
            branch.addChild(dragger)
            self.node.addChild(branch)
            self.entries.append((dragger, rotate))
            for name, fn in (('Start', self.start), ('Motion', self.changed), ('Finish', self.end)):
                callback = lambda *args, i=index, f=fn: f(i)
                task.view.addDraggerCallback(dragger, 'add' + name + 'Callback', callback)
                self.callbacks.append((dragger, name, callback))
        self.keyboard = self.key
        task.view.addEventCallbackPivy(coin.SoKeyboardEvent.getClassTypeId(), self.keyboard)
        task.scene.addChild(self.node)

    def visual(self, dragger, part, size, axis):
        colors = ((.9, .25, .2), (.25, .8, .3), (.25, .5, 1.0))
        for suffix in ('', 'Active'):
            original = dragger.getPart(part + suffix, True)
            if original is None:
                continue
            visual = coin.SoSeparator()
            color = coin.SoMaterial()
            color.diffuseColor = (1.0, .8, .2) if suffix else colors[axis]
            color.transparency = 0.0
            color.setOverride(True)
            visual.addChild(color)
            if part == 'rotator':
                # A narrow tube gives each ring a reliable pick surface at high
                # DPI. Filled default discs obscure the other axes; thin Coin
                # lines depend on the view's subpixel picking tolerance.
                segments, sides = 96, 8
                points = []
                for i in range(segments):
                    angle = i * math.tau / segments
                    for j in range(sides):
                        section = j * math.tau / sides
                        radius = size * (1 + .035 * math.cos(section))
                        points.append((radius * math.cos(angle), radius * math.sin(angle), size * .035 * math.sin(section)))
                coords = coin.SoCoordinate3(); coords.point.setValues(0, len(points), points); visual.addChild(coords)
                indices = []
                for i in range(segments):
                    for j in range(sides):
                        indices.extend((i * sides + j, ((i + 1) % segments) * sides + j,
                                        ((i + 1) % segments) * sides + (j + 1) % sides,
                                        i * sides + (j + 1) % sides, -1))
                ring = coin.SoIndexedFaceSet(); ring.coordIndex.setValues(0, len(indices), indices); visual.addChild(ring)
            elif isinstance(dragger, coin.SoTranslate2Dragger):
                color.transparency = .4
                coords = coin.SoCoordinate3()
                coords.point.setValues(0, 4, [(size * x, size * y, 0) for x, y in ((.4, .4), (1.2, .4), (1.2, 1.2), (.4, 1.2))])
                visual.addChild(coords)
                face = coin.SoFaceSet(); face.numVertices.setValue(4); visual.addChild(face)
            else:
                scale = coin.SoScale(); scale.scaleFactor = (size, size, size); visual.addChild(scale)
                visual.addChild(original)
            dragger.setPart(part + suffix, visual)

    def start(self, index):
        if self.closed or self.ignore:
            return
        self.dragging = True
        self.base_motion = App.Placement(self.task.pending)
        self.base_pivot = App.Vector(self.task.dynamic_pivot())
        self.task.numeric_base = (App.Placement(self.base_motion), App.Vector(self.base_pivot))
        self.task.drag_dirty = False
        self.task.handle.blockSignals(True)
        self.task.handle.setCurrentIndex(index)
        self.task.handle.blockSignals(False)
        self.task.drag_value.blockSignals(True)
        self.task.drag_value.setProperty('rawValue', 0.0)
        self.task.drag_value.blockSignals(False)

    def changed(self, index):
        if self.closed or self.ignore:
            return
        task = self.task
        try:
            task.check()
            dragger, orient = self.entries[index]
            if task.kind.currentText() == 'Rotate':
                axis, radians = dragger.rotation.getValue().getAxisAngle()
                angle = math.degrees(radians) * (1 if axis[2] >= 0 else -1)
                angle = task.snapped(angle)
                delta = motion.rotation(self.base_pivot, AXES[index], angle)
                value = angle
                vector = App.Vector()
            else:
                vector = orient.multVec(App.Vector(*dragger.translation.getValue().getValue()))
                if index < 3:
                    value = task.snapped(vector.dot(AXES[index]))
                    vector = AXES[index] * value
                else:
                    # Plane snapping is independent on both parent axes.
                    vector = App.Vector(*(task.snapped(v) for v in vector))
                    value = vector.Length
                    if value > 1e-9:
                        task.plane_direction = App.Vector(vector).normalize()
                delta = App.Placement(vector, App.Rotation())
            task.drag_value.blockSignals(True)
            task.drag_value.setProperty('rawValue', value)
            task.drag_value.blockSignals(False)
            if task.control.currentIndex() == 1:
                if task.kind.currentText() == 'Rotate':
                    raise ValueError('Use Move / Dynamic drag to relocate the pivot')
                task.pivot_snapshot = self.base_pivot + vector
            else:
                task.pending = delta.multiply(self.base_motion)
            task.update_preview(force=True)
        except (ValueError, RuntimeError, ReferenceError) as error:
            task.show_error(error)

    def end(self, index):
        if self.closed or self.ignore:
            return
        self.dragging = False
        QtCore.QTimer.singleShot(0, self.task.rebuild_handles)

    def key(self, callback):
        event = callback.getEvent()
        if (self.dragging and coin.SoKeyboardEvent.isKeyPressEvent(event, coin.SoKeyboardEvent.ESCAPE)):
            self.ignore = True
            self.task.pending = App.Placement(self.base_motion)
            self.task.pivot_snapshot = App.Vector(self.base_pivot)
            self.task.numeric_base = None
            self.task.drag_value.blockSignals(True)
            self.task.drag_value.setProperty('rawValue', 0.0)
            self.task.drag_value.blockSignals(False)
            callback.setHandled()
            callback.getAction().releaseGrabber()
            self.dragging = False
            self.task.update_preview(force=True)
            QtCore.QTimer.singleShot(0, self.task.rebuild_handles)

    def close(self):
        if self.closed:
            return
        self.closed = True
        for dragger, name, callback in self.callbacks:
            self.task.view.removeDraggerCallback(dragger, 'add' + name + 'Callback', callback)
        self.task.view.removeEventCallbackPivy(coin.SoKeyboardEvent.getClassTypeId(), self.keyboard)
        if self.task.scene.findChild(self.node) >= 0:
            self.task.scene.removeChild(self.node)
        self.callbacks.clear()
