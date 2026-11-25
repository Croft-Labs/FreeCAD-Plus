# SPDX-License-Identifier: LGPL-2.1-or-later
"""Occurrence-aware Move Components. Preview never writes document geometry."""
import math
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtWidgets
from pivy import coin
from . import assembly, document, editing, external, hierarchy, isolation, task_status
from . import movement_math as rigid
from .movement_handles import AXES, Handles

METHODS = {'Move': ('Distance and vector', 'Point to point', 'Dynamic drag'),
           'Rotate': ('Axis and angle', 'Dynamic drag'),
           'Align': ('Axes', 'Coordinate systems')}
_active = None


class IncompleteInput(ValueError):
    """Ordinary collector guidance, rather than an invalid operation."""


def movable(link, owner):
    from .instance_patterns import check_independent
    check_independent(link)
    if link.TypeId != 'App::Link' or link not in owner.Group:
        raise ValueError('Select whole sibling component instances')
    if any(flag in link.getPropertyStatus('LinkPlacement') for flag in ('ReadOnly', 'Immutable')) or 'ReadOnly' in link.getEditorMode('LinkPlacement'):
        raise ValueError('This component placement is read-only')
    if any(any(part in ('Placement', 'LinkPlacement') for part in name.split('.'))
           for name, expression in link.ExpressionEngine):
        raise ValueError('This component placement is driven by an expression')
    for ref in link.InList:
        if ref != owner and (ref.TypeId.startswith('Assembly::') or
                            any(name in ref.PropertiesList for name in ('ObjectToGround', 'Reference1', 'Reference2'))):
            raise ValueError('This component is constrained; edit its assembly relationship first')


def visible_reference(obj, sub):
    if not obj.Visibility: return False
    chain = obj.getSubObjectList(sub)
    return all(parent.isElementVisible(child.Name) != 0 and
               (parent.isElementVisible(child.Name) >= 0 or child.Visibility)
               for parent, child in zip(chain, chain[1:]))


class Collector(QtWidgets.QListWidget):
    activated = QtCore.Signal()
    cleared = QtCore.Signal()

    def __init__(self, placeholder, multi=False):
        super().__init__()
        self.placeholder = placeholder
        self.setFixedHeight(70 if multi else 34)
        self.setToolTip('Click to pick in the tree or view. Delete removes the selected reference.')
        if multi: self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def mousePressEvent(self, event):
        self.activated.emit(); super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.cleared.emit(); event.accept()
        else: super().keyPressEvent(event)

    def event(self, event):
        if event.type() == QtCore.QEvent.ShortcutOverride and event.key() == QtCore.Qt.Key_Delete:
            event.accept(); return True
        return super().event(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.count():
            from PySide6 import QtGui
            painter = QtGui.QPainter(self.viewport())
            painter.setPen(self.palette().placeholderText().color())
            painter.drawText(self.viewport().rect().adjusted(5, 2, -4, -2), QtCore.Qt.AlignVCenter, self.placeholder)


class MoveTask(QtCore.QObject):
    def __init__(self, panel, rows):
        super().__init__(panel)
        from .panel import identity
        self.panel = panel
        self.doc, self.view = panel._binding; self.binding = panel._binding
        active, active_path = panel._context(*self.binding)
        chosen, path = panel._assembly_context(self.binding, active, active_path)
        if chosen is None: raise ValueError('Choose an active assembly first')
        self.assembly_ref = identity(chosen); self.assembly_path = tuple(identity(o) for o in path)
        self.edit_context = (identity(active) if active else None, tuple(identity(o) for o in active_path))
        self.paths = []; self.parent_path = None; self.parent_ref = None
        self.refs = {}; self.ref_widgets = {}; self.numeric = []
        self.pending = App.Placement(); self.pivot_snapshot = None; self.plane_direction = App.Vector(1, 0, 0)
        self.numeric_base = None; self.after_apply = False; self.drag_dirty = False
        self.collecting = 'components'; self.closed = False; self.busy = True; self.selecting = False
        self.overlay = None; self.handles = None; self.scene = self.view.getSceneGraph()
        self.form = QtWidgets.QWidget(); self.form.setWindowTitle('Move Components'); self.form.setMinimumWidth(300)
        self.form.setAutoFillBackground(True)
        layout = QtWidgets.QVBoxLayout(self.form); layout.setContentsMargins(8, 8, 8, 8)
        self.context = QtWidgets.QLabel(); self.context.setWordWrap(True); layout.addWidget(self.context)
        modes = QtWidgets.QFormLayout()
        self.kind = QtWidgets.QComboBox(); self.kind.addItems(METHODS); self.method = QtWidgets.QComboBox()
        modes.addRow('Type', self.kind); modes.addRow('Method', self.method); layout.addLayout(modes)
        group = QtWidgets.QGroupBox('Components'); box = QtWidgets.QVBoxLayout(group)
        self.components = Collector('Pick child component instances', multi=True)
        self.components.activated.connect(lambda: self.collect('components'))
        self.components.cleared.connect(lambda: self.run(self.remove_selected)); box.addWidget(self.components)
        hint = QtWidgets.QLabel('Click the list, then pick components in the tree or view.'); hint.setWordWrap(True); box.addWidget(hint)
        row = QtWidgets.QHBoxLayout()
        for label, callback in (('Remove', self.remove_selected), ('Clear', self.clear)):
            button = QtWidgets.QPushButton(label); button.clicked.connect(lambda checked=False, c=callback: self.run(c)); row.addWidget(button)
        box.addLayout(row)
        self.persistent = QtWidgets.QCheckBox('Keep selection after Apply'); self.persistent.setChecked(True)
        box.addWidget(self.persistent); layout.addWidget(group)
        self.method_host = QtWidgets.QWidget(); self.method_layout = QtWidgets.QVBoxLayout(self.method_host)
        self.method_layout.setContentsMargins(0, 0, 0, 0); layout.addWidget(self.method_host)
        self.auto = QtWidgets.QCheckBox('Automatic preview'); self.auto.setChecked(True)
        update = QtWidgets.QPushButton('Update preview'); update.clicked.connect(lambda: self.update_preview(force=True))
        self.auto.toggled.connect(self.update_preview)
        row = QtWidgets.QHBoxLayout(); row.addWidget(self.auto); row.addWidget(update); layout.addLayout(row)
        self.message = task_status.TaskStatus(); layout.addWidget(self.message); layout.addStretch()
        self.kind.currentTextChanged.connect(self.change_type); self.method.currentTextChanged.connect(self.change_method)
        self.change_type('Move'); self.busy = False
        try:
            if rows: self.add_rows(rows)
            else: self.refresh_list()
        except Exception:
            self.form.deleteLater(); self.deleteLater(); raise
        self.timer = QtCore.QTimer(self); self.timer.setSingleShot(True); self.timer.timeout.connect(self.check_lifecycle)
        self.pick_timer = QtCore.QTimer(self); self.pick_timer.setSingleShot(True); self.pick_timer.timeout.connect(lambda: self.run(self.consume_selection))
        App.addDocumentObserver(self); Gui.addDocumentObserver(self); Gui.Selection.addObserver(self, 0)
        panel._mdi.subWindowActivated.connect(self.schedule); Gui.getMainWindow().workbenchActivated.connect(self.finish)
        editing.add_context_observer(self.schedule); self.window = panel._state(self.binding).get('window')
        if self.window: self.window.destroyed.connect(self.finish)
        self.update_preview()

    def quantity(self, unit='mm', value=0.0, nonnegative=False):
        widget = Gui.UiLoader().createWidget('Gui::InputField'); widget.setProperty('unit', unit)
        if nonnegative: widget.setProperty('minimum', 0.0)
        widget.setProperty('rawValue', float(value))
        widget.valueChanged.connect(lambda *unused: widget.setProperty('moveParseError', ''))
        widget.valueChanged.connect(self.input_changed)
        def invalid(error):
            widget.setProperty('moveParseError', str(error)); self.input_changed()
        widget.parseError.connect(invalid); widget.installEventFilter(self); self.numeric.append(widget)
        return widget

    def value(self, widget):
        value = float(widget.property('rawValue'))
        if widget.property('moveParseError') or not widget.hasAcceptableInput() or not math.isfinite(value):
            raise ValueError('Enter a valid finite value with the required units')
        return value

    def combo(self, choices):
        widget = QtWidgets.QComboBox(); widget.addItems(choices); widget.currentIndexChanged.connect(self.input_changed)
        return widget

    def reference(self, key, placeholder):
        widget = Collector(placeholder); widget.activated.connect(lambda: self.collect(key))
        widget.cleared.connect(lambda: self.clear_reference(key)); self.ref_widgets[key] = widget
        return widget

    def collect(self, key):
        self.collecting = key; self.selecting = True
        try: Gui.Selection.clearSelection()
        finally: self.selecting = False
        for name, widget in {'components': self.components, **self.ref_widgets}.items():
            widget.setStyleSheet('QListWidget { border: 2px solid #2388cf; }' if name == key else '')

    def clear_reference(self, key):
        self.refs.pop(key, None); self.ref_widgets[key].clear()
        if key == 'pivot':
            self.pivot_snapshot = None; self.numeric_base = None; self.rebuild_handles()
        self.input_changed()

    def change_type(self, kind):
        self.method.blockSignals(True); self.method.clear(); self.method.addItems(METHODS[kind])
        self.method.blockSignals(False); self.change_method(self.method.currentText())

    def change_method(self, method):
        from .movement_ui import build_method
        was_busy = self.busy; self.busy = True
        self.close_handles(); self.clear_preview(); self.pending = App.Placement()
        self.numeric_base = None; self.after_apply = False; self.drag_dirty = False
        self.refs = {}; self.ref_widgets = {}; self.numeric = []; self.pivot_snapshot = None; self.collecting = 'components'
        while self.method_layout.count():
            item = self.method_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        build_method(self, method)
        self.busy = was_busy; self.collect('components')
        if not self.busy: self.update_preview(); self.rebuild_handles()

    def run(self, callback):
        try:
            callback(); return True
        except (ValueError, RuntimeError, ReferenceError) as error:
            self.show_error(error); return False

    def show_error(self, error):
        self.clear_preview(); self.message.setError(str(error)); self.enable_commit(False)

    def enable_commit(self, enabled, ok=None):
        if _active is not self: return
        for buttons in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox):
            if buttons.isVisible():
                for role in (QtWidgets.QDialogButtonBox.Apply, QtWidgets.QDialogButtonBox.Ok):
                    button = buttons.button(role)
                    if button: button.setEnabled((enabled if ok is None else ok) if role == QtWidgets.QDialogButtonBox.Ok else enabled)

    def check(self):
        from .panel import lookup, identity
        if self.closed or self.panel._closed or self.panel._current() != self.binding:
            raise ValueError('The active file tab changed; reopen Move Components')
        self.panel._clipboard_guard()
        anchor = lookup(self.assembly_ref)
        active, path = self.panel._context(*self.binding)
        chosen, route = self.panel._assembly_context(self.binding, active, path)
        if chosen != anchor or tuple(identity(o) for o in route) != self.assembly_path:
            raise ValueError('The active assembly changed; reopen Move Components')
        if (identity(active) if active else None, tuple(identity(o) for o in path)) != self.edit_context:
            raise ValueError('The editing context changed; reopen Move Components')
        owner = assembly.resolve(anchor, tuple(lookup(r) for r in (self.parent_path or ())))
        if self.parent_ref and identity(owner) != self.parent_ref:
            raise ValueError('The parent occurrence changed; reopen Move Components')
        links = []
        for refs in self.paths:
            path = tuple(lookup(r) for r in refs); assembly.resolve(anchor, path)
            for link in (*tuple(lookup(r) for r in self.assembly_path), *path):
                if (abs(getattr(link, 'Scale', 1.0) - 1) > 1e-12 or
                    (getattr(link, 'ScaleVector', App.Vector(1, 1, 1)) - App.Vector(1, 1, 1)).Length > 1e-12):
                    raise ValueError('Scaled component frames are not supported')
            movable(path[-1], owner); links.append(path[-1])
        return owner, links

    def available_rows(self):
        from .panel import lookup, projection
        roots = projection(self.doc, assembly_root=lookup(self.assembly_ref),
                           assembly_path=tuple(lookup(r) for r in self.assembly_path))[1]
        rows = []
        def visit(row):
            if row.kind in ('assembly', 'occurrence'): rows.append(row)
            for child in row.children: visit(child)
        for row in roots: visit(row)
        return rows

    def add_rows(self, rows):
        from .panel import lookup, identity
        self.check(); candidates = []; parent_path, parent_ref = self.parent_path, self.parent_ref
        available = {row.key: row for row in self.available_rows()}
        for row in rows:
            self.panel._checked(row)
            if row.kind != 'occurrence':
                raise ValueError('The active assembly is fixed; select its child component instances')
            if row.key not in available or available[row.key] != row:
                raise ValueError('Choose a child of the current active assembly')
            relative = row.path if row.anchor else row.path[len(self.assembly_path):]
            if not relative: raise ValueError('The active assembly is fixed')
            owner = assembly.resolve(lookup(self.assembly_ref), tuple(lookup(r) for r in relative[:-1]))
            movable(lookup(relative[-1]), owner)
            if parent_path is None: parent_path, parent_ref = relative[:-1], identity(owner)
            if relative[:-1] != parent_path or identity(owner) != parent_ref:
                raise ValueError('Select only siblings under the same parent occurrence; no components were added')
            if relative not in self.paths and relative not in candidates: candidates.append(relative)
        self.parent_path, self.parent_ref = parent_path, parent_ref; self.paths.extend(candidates)
        self.refresh_list(); self.update_preview(); self.rebuild_handles()

    def refresh_list(self):
        from .panel import lookup
        self.components.clear()
        for refs in self.paths:
            self.components.addItem(external.qualified_label(lookup(refs[-1]).LinkedObject, self.doc))
        owner = lookup(self.parent_ref) if self.parent_ref else None
        self.context.setText('Active assembly: ' + lookup(self.assembly_ref).Label + ' — fixed\nParent frame: ' +
                             (owner.Label if owner else 'Pick child components'))

    def add_selected(self):
        rows = []; available = self.available_rows()
        for entry in Gui.Selection.getSelectionEx('', 0):
            for sub in entry.SubElementNames or ('',):
                key = (entry.DocumentName, entry.ObjectName, sub)
                candidates = [r for r in available if r.selection[:2] == key[:2] and sub.startswith(r.selection[2])]
                if not candidates: raise ValueError('Pick component instances inside the active assembly')
                rows.append(max(candidates, key=lambda r: len(r.selection[2])))
        if not rows: return
        from .selection_list import removing
        if removing():
            keys = {r.path if r.anchor else r.path[len(self.assembly_path):] for r in rows}
            self.paths = [p for p in self.paths if p not in keys]; self.selection_changed()
        else: self.add_rows(rows)

    def addSelection(self, *args):
        if not self.closed and not self.selecting:
            from .selection_list import removing
            self.pick_remove = removing(); self.pick_timer.start(0)

    def setSelection(self, *args): self.addSelection()

    def consume_selection(self):
        if self.closed: return
        from .selection_list import pick_intent
        with pick_intent(getattr(self, 'pick_remove', False)):
            if self.collecting == 'components': self.add_selected()
            else: self.pick_reference(self.collecting)

    def remove_selected(self):
        indexes = {self.components.row(item) for item in self.components.selectedItems()}
        self.paths = [path for i, path in enumerate(self.paths) if i not in indexes]; self.selection_changed()

    def clear(self):
        self.paths.clear(); self.selection_changed()

    def selection_changed(self):
        self.pending = App.Placement(); self.pivot_snapshot = None
        if not self.paths:
            self.parent_path = self.parent_ref = None
            self.change_method(self.method.currentText())
        self.refresh_list(); self.collect('components'); self.update_preview(); self.rebuild_handles()

    def parent_frame(self):
        from .panel import lookup
        anchor = lookup(self.assembly_ref)
        route = tuple(lookup(r) for r in (*self.assembly_path, *(self.parent_path or ())))
        if self.assembly_path: return hierarchy.world_placement(self.doc, route)
        path = tuple(lookup(r) for r in (self.parent_path or ()))
        return anchor.getSubObject(hierarchy.subname(path), 3) if path else App.Placement(anchor.Placement)

    def selected_reference(self):
        self.check()
        selections = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('', 0)
                      for sub in entry.SubElementNames or ('',)]
        if len(selections) != 1: raise ValueError('Select exactly one visible reference')
        obj, sub = selections[0]
        from . import geometry
        from .panel import lookup
        anchor = lookup(self.assembly_ref)
        if not self.assembly_path and document.owned_path(anchor, obj) is not None:
            geometry.require_access(anchor.Document, obj, sub, active=anchor)
        else:
            geometry.require_access(self.doc, obj, sub, active=anchor,
                                    active_path=tuple(lookup(r) for r in self.assembly_path))
        if not visible_reference(obj, sub): raise ValueError('Choose a visible reference')
        return obj, sub

    def selected_line(self, allow_curved_axis=False):
        obj, sub = self.selected_reference(); shape = Part.getShape(obj, sub, needSubElement=True)
        if shape.ShapeType == 'Edge' and isinstance(shape.Curve, (Part.Line, Part.LineSegment)):
            point, vector = shape.valueAt(0.0), shape.tangentAt(0.0)
        elif allow_curved_axis and shape.ShapeType == 'Edge' and isinstance(shape.Curve, Part.Circle):
            point, vector = shape.Curve.Center, shape.Curve.Axis
        elif allow_curved_axis and shape.ShapeType == 'Face' and isinstance(shape.Surface, Part.Cylinder):
            point, vector = shape.Surface.Center, shape.Surface.Axis
        else:
            raise ValueError('Choose a straight line or axis, not a curved edge')
        frame = self.parent_frame()
        return (frame.inverse().multVec(point), rigid.direction(frame.Rotation.inverted().multVec(vector)))

    def selected_point(self):
        obj, sub = self.selected_reference(); target = obj.getSubObject(sub, 1) if sub else obj
        if target is not None and target.TypeId in ('App::Origin', 'App::Placement', 'PartDesign::CoordinateSystem'):
            point = obj.getSubObject(sub, 3).Base if sub else obj.Placement.Base
        else:
            shape = Part.getShape(obj, sub, needSubElement=True)
            if shape.ShapeType == 'Vertex': point = shape.Point
            elif shape.ShapeType == 'Edge' and isinstance(shape.Curve, Part.Circle): point = shape.Curve.Center
            else: raise ValueError('Choose a vertex, point, origin or circular edge center')
        return self.parent_frame().inverse().multVec(point)

    def selected_frame(self):
        obj, sub = self.selected_reference(); target = obj.getSubObject(sub, 1) if sub else obj
        if target is None or target.TypeId not in ('App::Origin', 'App::Placement', 'PartDesign::CoordinateSystem'):
            raise ValueError('Choose a coordinate system or define its origin, Z and X axes')
        world = obj.getSubObject(sub, 3) if sub else obj.Placement
        return self.parent_frame().inverse().multiply(world)

    def pick_reference(self, key):
        from .selection_list import removing
        if removing(): self.clear_reference(key); return
        if key in ('direction', 'axis', 'source_axis', 'target_axis') or key.endswith(('_x', '_z')):
            value = self.selected_line(allow_curved_axis=key in ('source_axis', 'target_axis'))
        elif key.endswith('_frame'): value = self.selected_frame()
        else: value = self.selected_point()
        obj, sub = self.selected_reference()
        self.after_apply = False
        chain = obj.getSubObjectList(sub)
        component = next((item.LinkedObject for item in reversed(chain) if item.TypeId == 'App::Link'), None)
        target = obj.getSubObject(sub, 1) if sub else obj
        label = ' · '.join(dict.fromkeys(item.Label for item in (component, target) if item is not None))
        element = Part.splitSubname(sub)[2] if sub else ''
        self.refs[key] = value; self.ref_widgets[key].clear()
        self.ref_widgets[key].addItem(label + (' · ' + element if element else ''))
        self.ref_widgets[key].item(0).setToolTip(' > '.join(item.Label for item in chain) + (' · ' + element if element else ''))
        if key == 'pivot': self.pivot_snapshot = value
        self.update_preview(); self.rebuild_handles()

    def reference_value(self, key):
        if key not in self.refs: raise IncompleteInput('Pick ' + key.replace('_', ' ') + ' before previewing')
        return self.refs[key]

    def rotation_axis(self):
        index = self.axis.currentIndex()
        if index < 3: point, vector = App.Vector(), AXES[index]
        elif index == 3: point, vector = self.reference_value('axis')
        else:
            point = self.reference_value('from'); vector = rigid.direction(self.reference_value('to') - point)
        return self.refs.get('pivot', point), vector

    def frame_value(self, name):
        if not self.advanced.isChecked(): return self.reference_value(name + '_frame')
        return rigid.frame(self.reference_value(name + '_o'), self.reference_value(name + '_z')[1], self.reference_value(name + '_x')[1])

    def motion(self):
        method = self.method.currentText()
        if method == 'Distance and vector':
            distance = self.value(self.distance)
            if distance < 0: raise ValueError('Distance must be nonnegative; use Reverse direction')
            index = self.direction.currentIndex()
            if index < 3: vector = AXES[index]
            elif index == 3: vector = self.reference_value('direction')[1]
            elif index == 4: vector = self.reference_value('to') - self.reference_value('from')
            else: vector = App.Vector(*(field.value() for field in self.vector_fields))
            return rigid.translation(vector, -distance if self.reverse.isChecked() else distance)
        if method == 'Point to point':
            return App.Placement(self.reference_value('to') - self.reference_value('from'), App.Rotation())
        if method == 'Axis and angle':
            angle = self.value(self.angle)
            if angle < 0: raise ValueError('Angle must be nonnegative; use Reverse rotation')
            return rigid.rotation(*self.rotation_axis(), -angle if self.reverse.isChecked() else angle)
        if method == 'Axes':
            return rigid.align_axes(self.reference_value('source_axis'), self.reference_value('target_axis'),
                                    bool(self.alignment.currentIndex()), self.reverse.isChecked())
        if method == 'Coordinate systems':
            return rigid.align_frames(self.frame_value('source'), self.frame_value('target'))
        self.value(self.drag_value); self.snapped(0.0)
        return App.Placement(self.pending)

    def dynamic_pivot(self):
        if self.pivot_snapshot is not None: return App.Vector(self.pivot_snapshot)
        owner, links = self.check(); bound = App.BoundBox()
        for link in links:
            shape = Part.getShape(link)
            if not shape.isNull(): bound.add(shape.BoundBox)
        return self.pending.multVec(bound.Center if bound.isValid() else App.Vector())

    def selection_size(self):
        owner, links = self.check()
        return max([Part.getShape(link).BoundBox.DiagonalLength for link in links if not Part.getShape(link).isNull()] or [20.0])

    def snapped(self, value):
        if self.snap.isChecked():
            step = self.value(self.increment)
            if step <= 0: raise ValueError('Snap increment must be greater than zero')
            return math.copysign(math.floor(abs(value) / step + .5) * step, value)
        return value

    def numeric_drag(self, *args, force=False):
        if self.busy or self.closed or (self.drag_value.hasFocus() and not force): return
        def update():
            self.check()
            if self.handles is None: self.rebuild_handles()
            if self.handles is None: return
            value = self.snapped(self.value(self.drag_value)); index = self.handle.currentIndex()
            if self.numeric_base is None:
                self.numeric_base = (App.Placement(self.handles.base_motion), App.Vector(self.handles.base_pivot))
            base, pivot = self.numeric_base
            if self.kind.currentText() == 'Rotate': delta = rigid.rotation(pivot, AXES[index], value)
            else: delta = rigid.translation(AXES[index] if index < 3 else self.plane_direction, value)
            if self.control.currentIndex() == 1: self.pivot_snapshot = pivot + delta.Base
            else: self.pending = delta.multiply(base)
            self.after_apply = False; self.drag_dirty = False
            self.handles.transform.translation = tuple(self.parent_frame().multVec(self.dynamic_pivot()))
            self.update_preview(force=True)
        self.run(update)

    def reset_numeric_drag(self, *args):
        if self.busy: return
        self.numeric_base = None
        self.drag_value.blockSignals(True); self.drag_value.setProperty('rawValue', 0.0); self.drag_value.blockSignals(False)
        index = self.handle.currentIndex()
        if index >= 3: self.plane_direction = AXES[(index - 3) % 3]
        self.rebuild_handles()

    def reset_pivot(self):
        self.pivot_snapshot = None; self.refs.pop('pivot', None); self.ref_widgets['pivot'].clear()
        self.rebuild_handles(); self.update_preview()

    def close_handles(self):
        if self.handles is not None: self.handles.close(); self.handles = None

    def rebuild_handles(self):
        if self.closed or self.busy: return
        self.close_handles()
        if self.method.currentText() == 'Dynamic drag' and self.paths:
            try: self.check(); self.handles = Handles(self)
            except (ValueError, RuntimeError, ReferenceError) as error: self.show_error(error)
        self.view.redraw()

    def clear_preview(self):
        if self.overlay is not None:
            if self.scene.findChild(self.overlay) >= 0: self.scene.removeChild(self.overlay)
            self.overlay = None

    def reference_guides(self, overlay):
        frame = self.parent_frame(); size = max(5., self.selection_size() * .7)
        def line(point, vector, color):
            node = coin.SoSeparator()
            material = coin.SoBaseColor(); material.rgb = color; node.addChild(material)
            draw = coin.SoDrawStyle(); draw.lineWidth = 2.5; draw.pointSize = 7; node.addChild(draw)
            points = [frame.multVec(point - vector * size), frame.multVec(point + vector * size)]
            coords = coin.SoCoordinate3(); coords.point.setValues(0, 2, [tuple(p) for p in points]); node.addChild(coords)
            shape = coin.SoLineSet(); shape.numVertices.setValue(2); node.addChild(shape)
            center = coin.SoCoordinate3(); center.point.setValue(tuple(frame.multVec(point))); node.addChild(center)
            marker = coin.SoPointSet(); marker.numPoints = 1; node.addChild(marker); overlay.addChild(node)
        method = self.method.currentText()
        if method == 'Axis and angle': line(*self.rotation_axis(), (1., .65, .05))
        elif method == 'Axes':
            for key, color in (('source_axis', (.2, .7, 1.)), ('target_axis', (1., .65, .05))):
                if key in self.refs: line(*self.refs[key], color)
        elif method == 'Point to point':
            for key, color in (('from', (.2, .7, 1.)), ('to', (1., .65, .05))):
                if key in self.refs: line(self.refs[key], App.Vector(), color)
        elif method == 'Coordinate systems':
            for name in ('source', 'target'):
                reference = self.frame_value(name)
                for axis, color in zip(AXES, ((.9, .2, .2), (.2, .8, .2), (.2, .4, 1.))):
                    line(reference.Base, reference.Rotation.multVec(axis) * .4, color)

    def input_changed(self, *args):
        if not self.busy:
            self.after_apply = False
            if not any(widget.hasFocus() for widget in self.numeric): self.update_preview()

    def eventFilter(self, watched, event):
        return super().eventFilter(watched, event)

    def update_preview(self, *args, force=False):
        if self.closed or self.busy: return
        self.clear_preview()
        try:
            owner, links = self.check()
            if not links:
                self.message.setText('Pick child components. The active assembly stays fixed.'); self.enable_commit(False); return
            motion = self.motion(); self.enable_commit(True)
            if not self.auto.isChecked() and not force:
                self.message.setText('Ready. Click Update preview to view the pending move.'); return
            overlay = coin.SoSeparator()
            pick = coin.SoPickStyle(); pick.style = coin.SoPickStyle.UNPICKABLE; overlay.addChild(pick)
            shapes = coin.SoSeparator(); overlay.addChild(shapes)
            style = coin.SoDrawStyle(); style.style = coin.SoDrawStyle.LINES; style.lineWidth = 2; style.setOverride(True); shapes.addChild(style)
            color = coin.SoBaseColor(); color.rgb = (.1, .8, 1.0); color.setOverride(True); shapes.addChild(color)
            root = document.validate(self.doc)
            parents = isolation.occurrences(self.doc, owner)
            scopes = [(root, parent, hierarchy.world_placement(self.doc, parent)) for parent in parents]
            isolated = isolation.current(self.view)
            if isolated is not None:
                definition = isolated.definition()
                def visit(current, route=()):
                    if current == owner:
                        frame = definition.getSubObject(hierarchy.subname(route), 3) if route else definition.Placement
                        scopes.append((definition, route, frame))
                    for link in current.Group:
                        if link.TypeId == 'App::Link': visit(link.LinkedObject, (*route, link))
                visit(definition)
            if not scopes:
                from .panel import lookup
                anchor = lookup(self.assembly_ref)
                scopes.append((anchor, tuple(lookup(r) for r in (self.parent_path or ())), self.parent_frame()))
            for base, parent, frame in scopes:
                transform = frame.multiply(motion).multiply(frame.inverse())
                for link in links:
                    sub = hierarchy.subname((*parent, link))
                    if base == root and not visible_reference(base, sub): continue
                    shape = Part.getShape(base, sub)
                    if shape.isNull(): continue
                    shape.Placement = transform.multiply(shape.Placement)
                    source = coin.SoInput(); source.setBuffer(shape.writeInventor()); shapes.addChild(coin.SoDB.readAll(source))
            self.reference_guides(overlay)
            self.scene.addChild(overlay); self.overlay = overlay
            note = ('Drag an arrow or plane.' if self.kind.currentText() == 'Move' else 'Drag a ring.') + ' Release keeps preview; Escape cancels the current drag.'
            self.message.setText(note if self.method.currentText() == 'Dynamic drag' else 'Preview only. Apply commits one group movement.')
        except IncompleteInput as error:
            self.message.setText(str(error)); self.enable_commit(False, ok=self.after_apply)
        except (ValueError, RuntimeError, ReferenceError) as error: self.show_error(error)

    def apply(self):
        owner, links = self.check()
        if not links: raise ValueError('Select sibling child component instances to move')
        if self.method.currentText() == 'Dynamic drag' and self.drag_dirty:
            self.numeric_drag(force=True)
        motion = self.motion()
        if motion.isSame(App.Placement(), 1e-12): return
        placements = [motion.multiply(link.LinkPlacement) for link in links]
        self.busy = True; self.clear_preview(); self.close_handles()
        try:
            with document.transaction(owner.Document, 'Move component instances'):
                for link, placement in zip(links, placements): link.LinkPlacement = placement
        finally: self.busy = False
        if not self.persistent.isChecked(): self.paths.clear(); self.parent_path = self.parent_ref = None
        self.refresh_list(); self.change_method(self.method.currentText())
        self.after_apply = True
        self.enable_commit(bool(self.paths) and self.method.currentText() not in ('Point to point', 'Axes', 'Coordinate systems'), ok=True)

    def getStandardButtons(self):
        return QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Apply

    def clicked(self, button):
        if button == QtWidgets.QDialogButtonBox.Apply: self.run(self.apply)

    def accept(self):
        if self.after_apply:
            if self.run(self.check): self.finish()
        elif self.run(self.apply): self.finish()
        return False

    def reject(self):
        self.finish(); return True

    def isAllowedAlterSelection(self): return True
    def isAllowedAlterView(self): return True
    def isAllowedAlterDocument(self): return False

    def schedule(self, *args):
        if not self.closed and not self.busy and not self.timer.isActive(): self.timer.start(0)

    slotChangedObject = schedule
    slotDeletedObject = schedule
    slotRecomputedDocument = schedule
    slotUndoDocument = schedule
    slotRedoDocument = schedule
    slotActivateDocument = schedule
    slotInEdit = schedule

    def slotDeletedDocument(self, doc):
        owner = getattr(doc, 'Document', doc)
        if owner == self.doc or owner.Name in {self.assembly_ref[0], self.parent_ref[0] if self.parent_ref else ''}: self.finish()

    def check_lifecycle(self):
        try: self.check(); self.update_preview()
        except (ValueError, RuntimeError, ReferenceError): self.finish()

    def finish(self, *args):
        global _active
        if self.closed: return
        self.closed = True; self.close_handles(); self.clear_preview(); self.timer.stop(); self.pick_timer.stop()
        App.removeDocumentObserver(self); Gui.removeDocumentObserver(self); Gui.Selection.removeObserver(self)
        self.panel._mdi.subWindowActivated.disconnect(self.schedule); Gui.getMainWindow().workbenchActivated.disconnect(self.finish)
        editing.remove_context_observer(self.schedule)
        if self.window:
            try: self.window.destroyed.disconnect(self.finish)
            except (RuntimeError, TypeError): pass
        if _active is self: _active = None; Gui.Control.closeDialog()
        self.deleteLater()


def open_task(panel, rows=()):
    global _active
    panel._clipboard_guard()
    if Gui.Control.activeDialog(): raise ValueError('Finish the current task first')
    task = MoveTask(panel, rows); _active = task
    try:
        Gui.Control.showDialog(task); QtCore.QTimer.singleShot(0, task.update_preview)
    except Exception:
        task.finish(); raise
    return task
