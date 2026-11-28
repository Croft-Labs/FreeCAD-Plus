# SPDX-License-Identifier: LGPL-2.1-or-later
"""Disposable Coin preview with explicit surface triangles and true BRep edges."""
from PySide6 import QtCore, QtGui
from pivy import coin
import FreeCADGui as Gui


class ShapePreview:
    def __init__(self,view):
        self.view=view;self.scene=view.getSceneGraph();self.node=None;self.shapes=[];self.frame=None
        self.color=(.65,.68,.72);self.transparency=.5;self.style=None
        self.timer=QtCore.QTimer(Gui.getMainWindow());self.timer.setInterval(150)
        self.timer.timeout.connect(self.style_changed);self.timer.start()

    def draw_style(self):
        for suffix,mode in (('Wireframe','Wireframe'),('Points','Points'),('HiddenLine','Hidden Line'),
                            ('Shaded','Shaded'),('FlatLines','Flat Lines'),('NoShading','No Shading')):
            action=Gui.getMainWindow().findChild(QtGui.QAction,'Std_DrawStyle'+suffix)
            if action and action.isChecked():return mode
        return 'As Is'

    def style_changed(self):
        try:
            if self.shapes and self.draw_style()!=self.style:self.render()
        except (RuntimeError,ReferenceError):self.close()

    def clear(self):
        if self.node is not None and self.scene.findChild(self.node)>=0:self.scene.removeChild(self.node)
        self.node=None;self.shapes=[]

    def close(self):self.clear();self.timer.stop();self.timer.deleteLater()

    def show(self,shapes,frame,color=(.65,.68,.72),transparency=.5):
        self.clear();self.shapes=shapes;self.frame=frame;self.color=color;self.transparency=transparency;self.render()

    def render(self):
        if self.node is not None and self.scene.findChild(self.node)>=0:self.scene.removeChild(self.node)
        self.style=self.draw_style();node=coin.SoSeparator()
        pick=coin.SoPickStyle();pick.style=coin.SoPickStyle.UNPICKABLE;node.addChild(pick)
        for original in self.shapes:
            shape=original.copy();shape.Placement=self.frame.multiply(shape.Placement)
            if self.style not in ('Wireframe','Points'):
                faces=coin.SoSeparator();style=coin.SoDrawStyle();style.style=coin.SoDrawStyle.FILLED;style.setOverride(True);faces.addChild(style)
                hints=coin.SoShapeHints();hints.vertexOrdering=coin.SoShapeHints.COUNTERCLOCKWISE
                hints.shapeType=coin.SoShapeHints.SOLID if shape.Solids else coin.SoShapeHints.UNKNOWN_SHAPE_TYPE;faces.addChild(hints)
                material=coin.SoMaterial();material.diffuseColor=self.color
                material.transparency=self.transparency;material.setOverride(True);faces.addChild(material)
                sorting=coin.SoTransparencyType();sorting.value=coin.SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND;faces.addChild(sorting)
                vertices,triangles=shape.tessellate(.1)
                coords=coin.SoCoordinate3();coords.point.setValues(0,len(vertices),[tuple(v) for v in vertices]);faces.addChild(coords)
                mesh=coin.SoIndexedFaceSet();indices=[i for triangle in triangles for i in (*triangle,-1)]
                mesh.coordIndex.setValues(0,len(indices),indices);faces.addChild(mesh);node.addChild(faces)
            if self.style != 'Shaded' or not shape.Faces:
                edges=coin.SoSeparator();style=coin.SoDrawStyle();style.style=coin.SoDrawStyle.POINTS if self.style=='Points' else coin.SoDrawStyle.LINES
                style.lineWidth=1.5;style.pointSize=3;style.setOverride(True);edges.addChild(style)
                material=coin.SoMaterial();material.diffuseColor=(.12,.2,.25);material.transparency=0;material.setOverride(True);edges.addChild(material)
                light=coin.SoLightModel();light.model=coin.SoLightModel.BASE_COLOR;edges.addChild(light)
                points=[];counts=[]
                for edge in shape.Edges:
                    values=edge.discretize(Deflection=.1);points.extend(tuple(v) for v in values);counts.append(len(values))
                if not shape.Edges:
                    points=[tuple(v.Point) for v in shape.Vertexes]
                    style.style=coin.SoDrawStyle.POINTS;style.pointSize=6
                coords=coin.SoCoordinate3();coords.point.setValues(0,len(points),points);edges.addChild(coords)
                if counts:
                    lines=coin.SoLineSet();lines.numVertices.setValues(0,len(counts),counts);edges.addChild(lines)
                elif points:
                    points_node=coin.SoPointSet();points_node.numPoints=len(points);edges.addChild(points_node)
                node.addChild(edges)
        self.scene.addChild(node);self.node=node
