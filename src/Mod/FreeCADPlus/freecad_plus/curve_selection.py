# SPDX-License-Identifier: LGPL-2.1-or-later
"""Expand user viewport edge picks within one native geometry owner."""
import itertools
import math
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets

INTENTS = ('Single Curve', 'Connected Curves', 'Tangent Curves')
_controller = None


def intent():
    from .selection_toolbar import preferences
    value = preferences().GetString('CurveIntent', INTENTS[0])
    return value if value in INTENTS else INTENTS[0]


def _graph(edges, tangent=False, topology=False):
    """Return native edge indices; closed periodic edges have no junction seam.

    Native edge tolerances govern endpoint matching. Solid edges additionally
    require shared native vertices, so coincident independent solids stay separate.
    Tangent traversal stops at branches and uses normalized native endpoint tangents.
    """
    endpoints = []
    for index, edge in edges.items():
        if edge.isClosed():
            continue
        for parameter in (edge.FirstParameter, edge.LastParameter):
            point = edge.valueAt(parameter)
            vertex = min(edge.Vertexes, key=lambda v: (v.Point-point).Length)
            endpoints.append((index, parameter, point, vertex, max(edge.Tolerance, vertex.Tolerance)))
    if not endpoints:
        return {index: set() for index in edges}
    cell = max(e[4] for e in endpoints)
    cell = max(cell, 1e-7)  # OCCT's standard linear confusion tolerance.
    buckets = {}
    neighbors = [[] for _ in endpoints]
    for i, (index, parameter, point, vertex, tolerance) in enumerate(endpoints):
        key = tuple(math.floor(value/cell) for value in point)
        for offset in itertools.product((-1, 0, 1), repeat=3):
            nearby = tuple(a+b for a, b in zip(key, offset))
            for j in buckets.get(nearby, ()):
                other = endpoints[j]
                if index == other[0] or (topology and not vertex.isSame(other[3])):
                    continue
                if (point-other[2]).Length <= max(tolerance, other[4], 1e-7):
                    neighbors[i].append(j)
                    neighbors[j].append(i)
        buckets.setdefault(key, []).append(i)
    graph = {index: set() for index in edges}
    for i, matches in enumerate(neighbors):
        if tangent and len(matches) != 1:
            continue
        for j in matches:
            if tangent:
                if len(neighbors[j]) != 1:
                    continue
                a, b = endpoints[i], endpoints[j]
                try:
                    t1 = edges[a[0]].tangentAt(a[1]).normalize()
                    t2 = edges[b[0]].tangentAt(b[1]).normalize()
                    if t1.cross(t2).Length > 1e-7:
                        continue
                except (RuntimeError, ValueError):
                    continue  # An undefined endpoint tangent is not a continuation.
            graph[endpoints[i][0]].add(endpoints[j][0])
    return graph


def _walk(graph, seed):
    if seed not in graph:
        return []
    seen, pending = set(), [seed]
    while pending:
        index = pending.pop()
        if index not in seen:
            seen.add(index)
            pending.extend(graph[index]-seen)
    return sorted(seen)


def connected(edges, seed, tangent=False, topology=False):
    return _walk(_graph(edges, tangent, topology), seed)


def candidates(root, subname, mode, cache=None):
    import Part
    prefix, _, _ = Part.splitSubname(subname)
    # Native Sketcher clicks use mapped names (for example ;g1.edge1).
    _, _, element = Part.splitSubname(root.resolveSubElement(subname)[2])
    if not element.startswith('Edge') or not element[4:].isdigit():
        return []
    key = (root.Document.Name, root.Name, prefix, mode)
    if cache is None:
        cache = {}
    if key not in cache:
        owner = root.getSubObject(prefix, 1) if prefix else root
        if owner is None:
            return []
        owner = owner.getLinkedObject(True)
        gui_doc = Gui.activeDocument()
        editing = gui_doc.getInEdit() if gui_doc else None
        if owner.isDerivedFrom('Sketcher::SketchObject') and getattr(editing, 'Object', None) == owner:
            # Geometry indices include construction items, unlike the displayed Shape.
            edges = {}
            for i, geometry in enumerate(owner.Geometry):
                shape = geometry.toShape()
                if shape.ShapeType == 'Edge':
                    edges[i+1] = shape
            topology = False
        elif hasattr(owner, 'Shape'):
            edges = dict(enumerate(owner.Shape.Edges, 1))
            topology = bool(owner.Shape.Solids)
        else:
            return []
        cache[key] = _graph(edges, mode == INTENTS[2], topology)
    return [prefix+'Edge'+str(i) for i in _walk(cache[key], int(element[4:]))]



class Controller(QtCore.QObject):
    def __init__(self):
        super().__init__(Gui.getMainWindow())
        self.active = False
        self.picking = False
        self.busy = False
        self.cache = {}
        QtWidgets.QApplication.instance().installEventFilter(self)
        Gui.Selection.addObserver(self, 0)  # Keep the original occurrence path.

    def eventFilter(self, watched, event):
        if self.active and event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonRelease):
            if event.button() == QtCore.Qt.LeftButton:
                widget = watched if isinstance(watched, QtWidgets.QWidget) else None
                while widget is not None:
                    if widget.inherits('Gui::View3DInventorViewer'):
                        self.picking = True
                        QtCore.QTimer.singleShot(0, self.end_pick)
                        break
                    widget = widget.parentWidget()
        return False

    def end_pick(self):
        self.picking = False
        self.cache.clear()

    def addSelection(self, doc, name, sub, point):
        mode = intent()
        if not self.active or not self.picking or self.busy or mode == INTENTS[0]:
            return
        document = App.getDocument(doc)
        root = document.getObject(name) if document else None
        if root is None:
            return
        self.busy = True
        try:
            for candidate in candidates(root, sub, mode, self.cache):
                if candidate != sub:
                    # Never replace a command's gate or bypass native admission.
                    Gui.Selection.addSelection(doc, name, candidate)
        except (RuntimeError, ValueError, AttributeError) as exc:
            App.Console.PrintWarning('Plus curve selection: %s\n' % exc)
        finally:
            self.busy = False


def apply(active):
    global _controller
    if _controller is None:
        _controller = Controller()
    _controller.active = active
    if not active:
        _controller.end_pick()
