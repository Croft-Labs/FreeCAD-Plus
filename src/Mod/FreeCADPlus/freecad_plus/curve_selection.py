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
        self.pending = set()
        self.gesture_previous = None
        self.gesture_active = False
        QtWidgets.QApplication.instance().installEventFilter(self)
        Gui.Selection.addObserver(self, 0)  # Keep the original occurrence path.

    def eventFilter(self, watched, event):
        from .selection_list import feature_picker_active, _INTENT
        if event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonRelease) and (self.active or feature_picker_active()):
            if event.button() == QtCore.Qt.LeftButton:
                widget = watched if isinstance(watched, QtWidgets.QWidget) else None
                while widget is not None:
                    if widget.inherits('Gui::View3DInventorViewer'):
                        app = QtWidgets.QApplication.instance()
                        if not self.gesture_active:
                            self.gesture_previous = app.property(_INTENT)
                            self.gesture_active = True
                        app.setProperty(_INTENT, bool(event.modifiers() & QtCore.Qt.ShiftModifier))
                        self.picking = True
                        QtCore.QTimer.singleShot(0, self.end_pick)
                        if event.modifiers() & QtCore.Qt.ShiftModifier and feature_picker_active():
                            # CAD navigation reserves Shift+left. Feature collectors
                            # own this gesture: ray-pick through the same native gate.
                            if event.type() == QtCore.QEvent.MouseButtonRelease:
                                self.remove_pick(watched, event.position().toPoint())
                            return True
                        break
                    widget = widget.parentWidget()
        return False

    def remove_pick(self, widget, position):
        try:
            gui = Gui.activeDocument()
            if not gui:return
            view = gui.activeView()
            viewport = view.graphicsView().viewport()
            position = viewport.mapFromGlobal(widget.mapToGlobal(position))
            ratio = viewport.devicePixelRatioF()
            x, y = round(position.x()*ratio), round((viewport.height()-1-position.y())*ratio)
            hit = view.getObjectInfo((x,y))
            if not hit:
                from . import extrude_task
                task = extrude_task._active
                if task is not None:task.pick_region_at(x,y,True)
                return
            root = hit.get('ParentObject')
            if root is not None:
                doc, name, sub = root.Document.Name, root.Name, hit['SubName']
            else:
                doc, name, sub = hit['Document'], hit['Object'], hit.get('Component','')
            Gui.Selection.addSelection(doc, name, sub)
        except (RuntimeError, ValueError, AttributeError, KeyError) as exc:
            App.Console.PrintWarning('Plus feature deselection: %s\n' % exc)

    def end_pick(self):
        if self.gesture_active:
            from .selection_list import _INTENT
            QtWidgets.QApplication.instance().setProperty(_INTENT, self.gesture_previous)
            self.gesture_active = False
            self.gesture_previous = None
        self.picking = False
        self.cache.clear()

    def addSelection(self, doc, name, sub, point):
        from .selection_list import removing
        remove = removing()
        mode = intent()
        if not self.active or not self.picking or self.busy or mode == INTENTS[0]:
            return
        document = App.getDocument(doc)
        root = document.getObject(name) if document else None
        if root is None:
            return
        try:
            import Part
            prefix, _, _ = Part.splitSubname(sub)
            _, _, element = Part.splitSubname(root.resolveSubElement(sub)[2])
            seed = prefix + element
            key = (doc, name, seed)
            if key in self.pending:
                return
            chain = candidates(root, sub, mode, self.cache)
            keys = {(doc, name, candidate) for candidate in chain} | {key}
            extra = [candidate for candidate in chain
                     if candidate != seed and (doc, name, candidate) not in self.pending]
            if not extra:
                return
            self.pending.update(keys)
            gui = Gui.activeDocument()
            editor = gui.getInEdit() if gui else None
            task = Gui.Control.activeDialog()
            # SelectionSingleton queues notifications made inside an observer.
            # A consuming task (Fillet, for example) clears each pick. Expanding
            # its queued picks again can therefore refill that queue forever.
            # Start after the seed notification drains, then deliver each extra
            # pick synchronously under the guard, retaining the native gate.
            QtCore.QTimer.singleShot(0, self, lambda: self.expand(root, extra, keys, gui, editor, task, remove))
        except (RuntimeError, ValueError, AttributeError) as exc:
            App.Console.PrintWarning('Plus curve selection: %s\n' % exc)

    def expand(self, root, extra, keys, gui, editor, task, remove=False):
        self.busy = True
        try:
            if (not self.active or Gui.activeDocument() != gui
                    or (gui and gui.getInEdit() != editor) or Gui.Control.activeDialog() != task):
                return
            from .selection_list import pick_intent
            with pick_intent(remove):
                for candidate in extra:
                    Gui.Selection.addSelection(root.Document.Name, root.Name, candidate)
        except (RuntimeError, ValueError, AttributeError, ReferenceError) as exc:
            App.Console.PrintWarning('Plus curve selection: %s\n' % exc)
        finally:
            self.busy = False
            self.pending.difference_update(keys)


def apply(active):
    global _controller
    if _controller is None:
        _controller = Controller()
    _controller.active = active
    if not active:
        _controller.end_pick()
