# SPDX-License-Identifier: LGPL-2.1-or-later
"""Transient, unpickable appearance highlights; source materials stay untouched."""
import FreeCAD as App
import Part
from pivy import coin
from . import document, display, hierarchy, isolation


def preferences():
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/View')
    return (prefs.GetBool('EnableSelection', True), prefs.GetUnsigned('SelectionColor', 0x1cad1cff),
            prefs.GetBool('EnablePreselection', True), prefs.GetUnsigned('HighlightColor', 0xe1e114ff))


def routes(task, owner, obj, face):
    owned = document.owned_path(owner, obj)
    if owned is None or any(not child.Visibility for child in owned):return
    session = isolation.current(task.view)
    if session:
        root = session.anchor_definition()
        paths = []
        def visit(part, path=()):
            if part == owner:paths.append(path)
            for link in part.Group:
                if link.TypeId == 'App::Link':visit(link.LinkedObject, (*path, link))
        visit(root)
        hidden = display.unused_hidden_paths(root)
    else:
        root = document.validate(task.host)
        paths = isolation.occurrences(task.host, owner)
        try:
            active, path = task.view.getActiveObject('PlusEdit'), ()
            from .editing import context_path
            active, path = context_path(task.host)
        except ValueError:active = None
        from .assembly_visibility import protection
        _, protected_path = protection(task.host, task.view)
        hidden = display.hidden_paths(task.host, active, path, protected_path=protected_path)
    for path in paths:
        if any(not link.Visibility for link in path):continue
        sub = hierarchy.subname((*path, *owned)) + 'Face' + str(face)
        if any(sub.startswith(prefix) for prefix in hidden):continue
        yield root, sub


def outline(shape, packed):
    """Draw true face boundaries with contrast, without exposing triangle edges."""
    rgb = tuple((packed >> shift & 255) / 255. for shift in (24, 16, 8))
    linear = tuple(c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb)
    luminance = sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))
    color = (0., 0., 0.) if luminance > .179 else (1., 1., 1.)
    points, counts = [], []
    tolerance = max(shape.BoundBox.DiagonalLength * .0005, .0001)
    for edge in shape.Edges:
        if edge.Length <= 0:continue
        vertices = edge.discretize(Deflection=tolerance)
        if len(vertices) < 2:continue
        points.extend(tuple(v) for v in vertices);counts.append(len(vertices))
    node = coin.SoSeparator();node.setName('FreeCADPlusAppearanceBoundary')
    depth = coin.SoDepthBuffer();depth.test = True;depth.write = False
    depth.function = coin.SoDepthBuffer.LEQUAL
    depth.range = (0., .999999);node.addChild(depth)
    material = coin.SoMaterial();material.diffuseColor = color
    material.setOverride(True);node.addChild(material)
    style = coin.SoDrawStyle();style.lineWidth = 2.;style.setOverride(True);node.addChild(style)
    coords = coin.SoCoordinate3();coords.point.setValues(0, len(points), points);node.addChild(coords)
    lines = coin.SoLineSet();lines.numVertices.setValues(0, len(counts), counts);node.addChild(lines)
    return node

class Highlights:
    def __init__(self, task):
        self.task = task
        self.scene = task.view.getSceneGraph()
        self.node = None

    def clear(self):
        if self.node is not None and self.scene.findChild(self.node) >= 0:self.scene.removeChild(self.node)
        self.node = None

    def update(self, owner, targets, hover=None):
        self.clear()
        selected, color, preselected, hover_color = preferences()
        values = [(obj, face, color, False) for obj, face in targets if face is not None] if selected else []
        if hover and preselected:values.append((*hover, hover_color, True))
        if not values:return
        node = coin.SoSeparator();node.setName('FreeCADPlusAppearanceHighlight')
        pick = coin.SoPickStyle();pick.style = coin.SoPickStyle.UNPICKABLE;node.addChild(pick)
        light = coin.SoLightModel();light.model = coin.SoLightModel.BASE_COLOR;node.addChild(light)
        boundaries = []
        for obj, face, packed, hovered in values:
            for root, sub in routes(self.task, owner, obj, face):
                shape = Part.getShape(root, sub, needSubElement=True)
                if shape.isNull() or shape.ShapeType != 'Face':continue
                branch = coin.SoSeparator()
                depth = coin.SoDepthBuffer();depth.write = False;branch.addChild(depth)
                offset = coin.SoPolygonOffset();offset.factor = -2 if hovered else -1
                offset.units = -2 if hovered else -1;branch.addChild(offset)
                material = coin.SoMaterial()
                material.diffuseColor = tuple((packed >> shift & 255)/255. for shift in (24,16,8))
                material.setOverride(True);branch.addChild(material)
                source = coin.SoInput();source.setBuffer(shape.writeInventor())
                branch.addChild(coin.SoDB.readAll(source));node.addChild(branch)
                boundaries.append(outline(shape, packed))
        for boundary in boundaries:node.addChild(boundary)
        self.scene.addChild(node);self.node = node
