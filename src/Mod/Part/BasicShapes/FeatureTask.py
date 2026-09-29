# SPDX-License-Identifier: LGPL-2.1-or-later

"""Shared edit lifecycle and direction annotation for Part feature tasks."""

import FreeCADGui as Gui
from pivy import coin


class TaskFeatureViewProvider:
    def __init__(self, view):
        view.Proxy = self

    def attach(self, view):
        self.Object = view.Object
        self.task = None

    def getIcon(self):
        return self.icon

    def doubleClicked(self, view):
        if Gui.Control.activeDialog():
            return False
        return bool(view.Document.setEdit(view.Object.Name))

    def setupContextMenu(self, view, menu):
        action = menu.addAction(self.editLabel)
        action.triggered.connect(lambda: self.doubleClicked(view))

    def setEdit(self, view, mode=0):
        if mode != 0:
            return False
        doc = view.Object.Document
        if not doc.HasPendingTransaction:
            doc.openTransaction(self.editLabel)
        self.task = self.makeTask(view.Object)
        Gui.Control.showDialog(self.task)
        return True

    def unsetEdit(self, view, mode=0):
        if self.task:
            if not self.task.finished:
                self.task.reject(reset_edit=False)
            self.task = None
        Gui.Control.closeDialog()
        return True

    def dumps(self):
        return None

    def loads(self, state):
        self.task = None


class SceneAnnotation:
    def __init__(self, view):
        self.scene = view.getSceneGraph()
        self.root = coin.SoAnnotation()
        pick = coin.SoPickStyle()
        pick.style = coin.SoPickStyle.UNPICKABLE
        self.root.addChild(pick)
        self.scene.addChild(self.root)

    def clear(self):
        self.root.removeAllChildren()

    def close(self):
        self.scene.removeChild(self.root)


class DirectionArrow(SceneAnnotation):
    def update(self, origin, direction, length):
        self.root.removeAllChildren()
        pick = coin.SoPickStyle()
        pick.style = coin.SoPickStyle.UNPICKABLE
        self.root.addChild(pick)
        material = coin.SoMaterial()
        material.diffuseColor = (0.15, 0.75, 0.25)
        self.root.addChild(material)
        transform = coin.SoTransform()
        transform.translation = tuple(origin)
        transform.rotation = coin.SbRotation(coin.SbVec3f(0, 1, 0), coin.SbVec3f(*direction))
        self.root.addChild(transform)
        shaft = coin.SoSeparator()
        move = coin.SoTranslation()
        move.translation = (0, length * 0.35, 0)
        shaft.addChild(move)
        cylinder = coin.SoCylinder()
        cylinder.radius = length * 0.035
        cylinder.height = length * 0.7
        shaft.addChild(cylinder)
        self.root.addChild(shaft)
        tip = coin.SoSeparator()
        move = coin.SoTranslation()
        move.translation = (0, length * 0.85, 0)
        tip.addChild(move)
        cone = coin.SoCone()
        cone.bottomRadius = length * 0.11
        cone.height = length * 0.3
        tip.addChild(cone)
        self.root.addChild(tip)


class CurveOverlay(SceneAnnotation):
    """Transient, unpickable highlight; the document retains the exact curve shape."""

    def update(self, shape):
        self.clear()
        pick = coin.SoPickStyle()
        pick.style = coin.SoPickStyle.UNPICKABLE
        self.root.addChild(pick)
        light = coin.SoLightModel()
        light.model = coin.SoLightModel.BASE_COLOR
        self.root.addChild(light)
        color = coin.SoBaseColor()
        color.rgb = (0.95, 0.15, 0.05)
        self.root.addChild(color)
        style = coin.SoDrawStyle()
        style.lineWidth = 3
        self.root.addChild(style)
        points, counts = [], []
        deflection = max(shape.BoundBox.DiagonalLength * 1e-4, 1e-4)
        for edge in shape.Edges:
            samples = edge.discretize(Deflection=deflection)
            counts.append(len(samples))
            points.extend(tuple(p) for p in samples)
        coordinates = coin.SoCoordinate3()
        coordinates.point.setValues(0, len(points), points)
        self.root.addChild(coordinates)
        lines = coin.SoLineSet()
        lines.numVertices.setValues(0, len(counts), counts)
        self.root.addChild(lines)
