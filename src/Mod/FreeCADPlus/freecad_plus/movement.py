# SPDX-License-Identifier: LGPL-2.1-or-later
"""Parent-owned component movement; preview lives only in the originating view."""
import math
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui
try:
    from PySide import QtWidgets
except ImportError:
    QtWidgets = QtGui
from pivy import coin
from . import document, editing, external, hierarchy, isolation

WORKFLOWS = ('Translate', 'Rotate', 'Point to Point', 'Align Axes',
             'Align Coordinate Systems', 'Interactive')
_active = None


def movable(link, owner):
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
    for parent, child in zip(chain, chain[1:]):
        visible = parent.isElementVisible(child.Name)
        if visible == 0 or (visible < 0 and not child.Visibility): return False
    return True


class MoveTask(QtCore.QObject):
    def __init__(self, panel, rows):
        super().__init__(panel)
        self.panel = panel
        self.doc, self.view = panel._binding
        self.binding = panel._binding
        self.paths = []
        self.parent_path = None
        self.parent_ref = None
        self.direction_snapshot = None
        self.axis_snapshot = None
        self.axis_points = [None, None]
        self.pivot_snapshot = None
        self.angle_error = None
        self.closed = False
        self.busy = False
        self.overlay = None
        self.scene = self.view.getSceneGraph()
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle('Move Components')
        layout = QtWidgets.QVBoxLayout(self.form)
        layout.addWidget(QtWidgets.QLabel('Workflow'))
        self.workflow = QtWidgets.QComboBox(); self.workflow.addItems(WORKFLOWS)
        layout.addWidget(self.workflow)
        layout.addWidget(QtWidgets.QLabel('Components'))
        self.components = QtWidgets.QListWidget()
        self.components.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.components.installEventFilter(self)
        layout.addWidget(self.components)
        buttons = QtWidgets.QHBoxLayout()
        for label, callback in (('Add selected', self.add_selected), ('Remove', self.remove_selected), ('Clear', self.clear)):
            button = QtWidgets.QPushButton(label); button.clicked.connect(lambda checked=False, c=callback: self.run(c)); buttons.addWidget(button)
        layout.addLayout(buttons)
        self.persistent = QtWidgets.QCheckBox('Persistent Selection'); self.persistent.setChecked(True)
        layout.addWidget(self.persistent)
        self.translate_form = QtWidgets.QWidget()
        translate_layout = QtWidgets.QVBoxLayout(self.translate_form)
        translate_layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.translate_form)
        translate_layout.addWidget(QtWidgets.QLabel('Direction'))
        self.direction = QtWidgets.QComboBox()
        self.direction.addItems(('Choose direction', 'Parent X', 'Parent Y', 'Parent Z', 'Picked line / edge / axis'))
        translate_layout.addWidget(self.direction)
        self.pick = QtWidgets.QPushButton('Use selected direction'); self.pick.clicked.connect(lambda: self.run(self.pick_direction))
        translate_layout.addWidget(self.pick)
        translate_layout.addWidget(QtWidgets.QLabel('Distance'))
        self.distance = Gui.UiLoader().createWidget('Gui::InputField')
        self.distance.setProperty('unit', 'mm'); self.distance.setProperty('minimum', 0.0)
        self.distance.setProperty('rawValue', 0.0)
        translate_layout.addWidget(self.distance)
        self.rotate_form = QtWidgets.QWidget()
        rotate_layout = QtWidgets.QVBoxLayout(self.rotate_form)
        rotate_layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.rotate_form)
        rotate_layout.addWidget(QtWidgets.QLabel('Axis'))
        self.axis = QtWidgets.QComboBox()
        self.axis.addItems(('Choose axis', 'Parent X', 'Parent Y', 'Parent Z', 'Picked line / edge / axis', 'Two points'))
        rotate_layout.addWidget(self.axis)
        self.axis_pick = QtWidgets.QPushButton('Use selected line / axis')
        self.axis_pick.clicked.connect(lambda: self.run(self.pick_axis))
        rotate_layout.addWidget(self.axis_pick)
        points = QtWidgets.QHBoxLayout()
        for index, title in enumerate(('Use selected first point', 'Use selected second point')):
            button = QtWidgets.QPushButton(title)
            button.clicked.connect(lambda checked=False, i=index: self.run(lambda: self.pick_axis_point(i)))
            points.addWidget(button)
        rotate_layout.addLayout(points)
        pivot = QtWidgets.QHBoxLayout()
        self.pivot_pick = QtWidgets.QPushButton('Use selected pivot')
        self.pivot_pick.clicked.connect(lambda: self.run(self.pick_pivot))
        pivot.addWidget(self.pivot_pick)
        self.pivot_clear = QtWidgets.QPushButton('Reset pivot')
        self.pivot_clear.clicked.connect(self.reset_pivot)
        pivot.addWidget(self.pivot_clear); rotate_layout.addLayout(pivot)
        self.resolved_axis = QtWidgets.QLabel('Choose an axis.'); self.resolved_axis.setWordWrap(True)
        rotate_layout.addWidget(self.resolved_axis)
        rotate_layout.addWidget(QtWidgets.QLabel('Angle'))
        self.angle = Gui.UiLoader().createWidget('Gui::InputField')
        self.angle.setProperty('unit', 'deg'); self.angle.setProperty('minimum', 0.0)
        self.angle.setProperty('rawValue', 0.0); rotate_layout.addWidget(self.angle)
        rotate_layout.addWidget(QtWidgets.QLabel('Positive follows the axis arrow by the right-hand rule.'))
        self.rotate_form.hide()
        self.reverse = QtWidgets.QCheckBox('Reverse'); layout.addWidget(self.reverse)
        self.message = QtWidgets.QLabel(); self.message.setWordWrap(True); layout.addWidget(self.message)
        layout.addWidget(QtWidgets.QLabel('Preview is a temporary wire outline; existing geometry remains selectable.'))
        self.workflow.currentIndexChanged.connect(self.reset_inputs)
        self.direction.currentIndexChanged.connect(self.update_preview)
        self.distance_error = None
        self.distance.valueChanged.connect(self.valid_distance)
        self.distance.parseError.connect(self.invalid_distance)
        self.distance.textChanged.connect(self.update_preview)
        self.reverse.toggled.connect(self.update_preview)
        self.axis.currentIndexChanged.connect(self.update_preview)
        self.angle.valueChanged.connect(self.valid_angle)
        self.angle.parseError.connect(self.invalid_angle)
        self.angle.textChanged.connect(self.update_preview)
        try:
            self.add_rows(rows)
        except Exception:
            self.form.deleteLater(); self.deleteLater()
            raise
        self.timer = QtCore.QTimer(self); self.timer.setSingleShot(True); self.timer.timeout.connect(self.check_lifecycle)
        App.addDocumentObserver(self)
        Gui.addDocumentObserver(self)
        panel._mdi.subWindowActivated.connect(self.schedule)
        Gui.getMainWindow().workbenchActivated.connect(self.finish)
        editing.add_context_observer(self.schedule)
        self.window = panel._state(self.binding).get('window')
        if self.window: self.window.destroyed.connect(self.finish)

    def run(self, callback):
        try:
            callback()
        except (ValueError, RuntimeError, ReferenceError) as error:
            self.clear_preview(); self.message.setText(str(error))
            return False
        return True

    def check(self):
        if self.closed or self.panel._closed or self.panel._current() != self.binding:
            raise ValueError('The active file tab changed; reopen Move Components')
        self.panel._clipboard_guard()
        from .panel import lookup
        root = document.validate(self.doc)
        owner = lookup(self.parent_ref) if self.parent_ref else root
        if self.parent_path:
            resolved, path = hierarchy.resolve(self.doc, tuple(lookup(r) for r in self.parent_path))
            if resolved != owner: raise ValueError('The parent occurrence changed')
        if self.parent_ref:
            current, route = self.panel._context(self.doc, self.view)
            if (current or root) != owner or tuple(route) != tuple(lookup(r) for r in self.parent_path):
                raise ValueError('The editing context changed; reopen Move Components')
        links = []
        for refs in self.paths:
            _, path = hierarchy.resolve(self.doc, tuple(lookup(r) for r in refs))
            if any(abs(getattr(link, 'Scale', 1.0) - 1.0) > 1e-12 or
                   (getattr(link, 'ScaleVector', App.Vector(1,1,1))-App.Vector(1,1,1)).Length > 1e-12 for link in path):
                raise ValueError('Scaled component frames are not supported by this movement task')
            movable(path[-1], owner); links.append(path[-1])
        return owner, links

    def add_rows(self, rows):
        from .panel import lookup, identity
        rows = tuple(rows)
        if not rows: raise ValueError('Select placed component instances in Part Tree')
        # Validate every supplied row before establishing or changing any context.
        candidates = []
        parent_path, parent_ref = self.parent_path, self.parent_ref
        for row in rows:
            self.panel._checked(row)
            if row.kind != 'occurrence': raise ValueError('Select whole placed component instances')
            path = tuple(lookup(r) for r in row.path)
            owner = hierarchy.resolve(self.doc, path[:-1])[0] if len(path) > 1 else document.validate(self.doc)
            movable(path[-1], owner)
            if parent_path is None: parent_path, parent_ref = row.path[:-1], identity(owner)
            if row.path[:-1] != parent_path or identity(owner) != parent_ref:
                raise ValueError('Select only siblings under the same parent occurrence; no components were added')
            if row.path not in self.paths and row.path not in candidates: candidates.append(row.path)
        self.panel._clipboard_guard()
        if self.parent_path is None:
            if parent_path: editing.edit(tuple(lookup(r) for r in parent_path))
            else: editing.edit_file(self.doc)
            self.parent_path, self.parent_ref = parent_path, parent_ref
        self.paths.extend(candidates)
        self.refresh_list(); self.select_components(); self.update_preview()

    def add_selected(self):
        from .panel import projection
        rows = []
        available = {}
        def visit(row):
            if row.kind == 'occurrence': available[row.selection] = row
            for child in row.children: visit(child)
        visit(projection(self.doc)[1][0])
        for entry in Gui.Selection.getSelectionEx('', 0):
            for sub in entry.SubElementNames or ('',):
                row = available.get((entry.DocumentName, entry.ObjectName, sub))
                if row is None: raise ValueError('Select whole sibling instances in Part Tree')
                rows.append(row)
        self.check(); self.add_rows(rows)

    def refresh_list(self):
        from .panel import lookup
        self.components.clear()
        for refs in self.paths:
            self.components.addItem(external.qualified_label(lookup(refs[-1]).LinkedObject, self.doc))

    def select_components(self):
        from .panel import lookup
        Gui.Selection.clearSelection()
        root = document.validate(self.doc)
        for path in self.paths:
            Gui.Selection.addSelection(self.doc.Name, root.Name, hierarchy.subname(tuple(lookup(r) for r in path)))

    def remove_selected(self):
        indexes = {self.components.row(item) for item in self.components.selectedItems()}
        self.paths = [path for i, path in enumerate(self.paths) if i not in indexes]
        self.refresh_list(); self.select_components(); self.update_preview()

    def clear(self):
        self.paths.clear(); self.refresh_list(); Gui.Selection.clearSelection(); self.update_preview()

    def eventFilter(self, watched, event):
        if watched == self.components and event.type() in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress) and event.key() == QtCore.Qt.Key_Delete:
            event.accept()
            if event.type() == QtCore.QEvent.KeyPress: self.run(self.remove_selected)
            return True
        return super().eventFilter(watched, event)

    def parent_frame(self):
        from .panel import lookup
        return hierarchy.world_placement(self.doc, tuple(lookup(r) for r in self.parent_path)) if self.parent_path else App.Placement()

    def selected_reference(self):
        self.check()
        selections = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('', 0)
                      for sub in entry.SubElementNames or ('',)]
        if len(selections) != 1: raise ValueError('Select exactly one visible reference')
        obj, sub = selections[0]
        if not visible_reference(obj, sub): raise ValueError('Choose a visible reference')
        return obj, sub

    def selected_line(self):
        obj, sub = self.selected_reference()
        shape = Part.getShape(obj, sub, needSubElement=True)
        if shape.ShapeType != 'Edge' or not isinstance(shape.Curve, (Part.Line, Part.LineSegment)):
            raise ValueError('Choose a straight line or axis, not a curved edge')
        vector = shape.tangentAt(0.0)
        if vector.Length < 1e-12: raise ValueError('The selected direction has zero length')
        frame = self.parent_frame()
        # Infinite native axes have no vertices. Position and direction need
        # different transforms; translation must never affect a direction.
        return (frame.inverse().multVec(shape.valueAt(0.0)),
                frame.Rotation.inverted().multVec(vector).normalize())

    def selected_point(self):
        obj, sub = self.selected_reference()
        target = obj.getSubObject(sub, 1) if sub else obj
        if target is not None and target.TypeId in ('App::Origin', 'App::Placement', 'PartDesign::CoordinateSystem'):
            point = obj.getSubObject(sub, 3).Base if sub else obj.Placement.Base
        else:
            shape = Part.getShape(obj, sub, needSubElement=True)
            if shape.ShapeType == 'Vertex': point = shape.Point
            elif shape.ShapeType == 'Edge' and isinstance(shape.Curve, Part.Circle): point = shape.Curve.Center
            else: raise ValueError('Choose a vertex, point, origin or circular edge center')
        return self.parent_frame().inverse().multVec(point)

    def pick_direction(self):
        self.direction_snapshot = self.selected_line()[1]
        self.direction.setCurrentIndex(4); self.update_preview()

    def pick_axis(self):
        self.axis_snapshot = self.selected_line()
        self.axis.setCurrentIndex(4); self.update_preview()

    def pick_axis_point(self, index):
        point = self.selected_point()
        other = self.axis_points[1-index]
        if other is not None and (point-other).Length < 1e-9:
            raise ValueError('Axis points must be distinct')
        self.axis_points[index] = point
        self.axis.setCurrentIndex(5); self.update_preview()

    def pick_pivot(self):
        self.pivot_snapshot = self.selected_point(); self.update_preview()

    def reset_pivot(self):
        self.pivot_snapshot = None; self.update_preview()

    def rotation_axis(self):
        index = self.axis.currentIndex()
        if index in (1,2,3):
            point, vector = App.Vector(), (App.Vector(1,0,0),App.Vector(0,1,0),App.Vector(0,0,1))[index-1]
        elif index == 4 and self.axis_snapshot is not None:
            point, vector = self.axis_snapshot
        elif index == 5 and all(p is not None for p in self.axis_points):
            point, second = self.axis_points
            vector = second-point
            if vector.Length < 1e-9: raise ValueError('Axis points must be distinct')
            vector.normalize()
        else: raise ValueError('Choose a complete rotation axis')
        return (self.pivot_snapshot if self.pivot_snapshot is not None else point), vector

    def valid_angle(self, *args):
        self.angle_error = None; self.update_preview()

    def invalid_angle(self, error):
        self.angle_error = error; self.update_preview()

    def motion(self):
        if self.workflow.currentIndex() == 0:
            return App.Placement(self.delta(), App.Rotation())
        if self.workflow.currentIndex() != 1:
            raise ValueError('This movement workflow awaits its next implementation increment')
        if self.angle_error or not self.angle.hasAcceptableInput():
            raise ValueError('Enter a valid nonnegative angle')
        angle = float(self.angle.property('rawValue'))
        if not math.isfinite(angle) or angle < 0: raise ValueError('Enter a valid nonnegative angle')
        if angle == 0: return App.Placement()
        point, vector = self.rotation_axis()
        rotation = App.Rotation(vector, -angle if self.reverse.isChecked() else angle)
        return App.Placement(point-rotation.multVec(point), rotation)

    def axis_preview(self, overlay, links):
        try:
            point, vector = self.rotation_axis()
        except ValueError as error:
            self.resolved_axis.setText(str(error)); return
        units = lambda value: App.Units.Quantity(value, App.Units.Length).UserString
        self.resolved_axis.setText('Pivot (parent): ' + ', '.join(units(v) for v in (point.x,point.y,point.z))
                                  + '\nAxis (parent): ' + ', '.join(f'{v:.4g}' for v in (vector.x,vector.y,vector.z)))
        frame = self.parent_frame()
        anchor = frame.multVec(point); direction = frame.Rotation.multVec(vector)
        length = 10.0
        for link in links:
            shape = Part.getShape(link)
            if not shape.isNull(): length = max(length, shape.BoundBox.DiagonalLength)
        side = direction.cross(App.Vector(0,0,1))
        if side.Length < 1e-6: side = direction.cross(App.Vector(0,1,0))
        side.normalize(); end = anchor + direction*length
        points = [anchor-direction*length, end, end-direction*(length*0.18)+side*(length*0.08),
                  end, end-direction*(length*0.18)-side*(length*0.08)]
        node = coin.SoSeparator()
        color = coin.SoBaseColor(); color.rgb=(1.0,0.65,0.0); color.setOverride(True); node.addChild(color)
        coords = coin.SoCoordinate3(); coords.point.setValues(0,len(points),[tuple(p) for p in points]); node.addChild(coords)
        lines = coin.SoLineSet(); lines.numVertices.setValue(5); node.addChild(lines)
        pivot = coin.SoSeparator(); coordinate=coin.SoCoordinate3();coordinate.point.setValue(tuple(anchor));pivot.addChild(coordinate)
        size=coin.SoDrawStyle();size.pointSize=9;size.setOverride(True);pivot.addChild(size)
        pivot.addChild(coin.SoPointSet());node.addChild(pivot);overlay.addChild(node)

    def valid_distance(self, *args):
        self.distance_error = None
        self.update_preview()

    def invalid_distance(self, error):
        self.distance_error = error
        self.update_preview()

    def delta(self):
        if self.workflow.currentIndex() != 0:
            raise ValueError('This movement workflow awaits its next implementation increment')
        if self.distance_error or not self.distance.hasAcceptableInput():
            raise ValueError('Enter a valid nonnegative length')
        distance = float(self.distance.property('rawValue'))
        if not math.isfinite(distance) or distance < 0: raise ValueError('Distance must be a nonnegative length')
        if distance == 0: return App.Vector()
        index = self.direction.currentIndex()
        vector = (None, App.Vector(1,0,0), App.Vector(0,1,0), App.Vector(0,0,1), self.direction_snapshot)[index]
        if vector is None: raise ValueError('Choose a direction before moving')
        return vector * (-distance if self.reverse.isChecked() else distance)

    def clear_preview(self):
        if self.overlay is not None:
            if self.scene.findChild(self.overlay) >= 0: self.scene.removeChild(self.overlay)
            self.overlay = None

    def update_preview(self, *args):
        if self.closed or self.busy: return
        self.clear_preview()
        try:
            owner, links = self.check()
            motion = self.motion()
            rotating = self.workflow.currentIndex() == 1
            if rotating: self.rotation_axis()
            if not links or (motion.isSame(App.Placement(),1e-12) and not rotating):
                self.message.setText('Select components and set a direction and distance.'); return
            root = document.validate(self.doc)
            parents = isolation.occurrences(self.doc, owner) if owner != root else [()]
            overlay = coin.SoSeparator()
            pick = coin.SoPickStyle(); pick.style = coin.SoPickStyle.UNPICKABLE; overlay.addChild(pick)
            style = coin.SoDrawStyle(); style.style = coin.SoDrawStyle.LINES; style.lineWidth = 2; style.setOverride(True); overlay.addChild(style)
            material = coin.SoBaseColor(); material.rgb = (0.1, 0.8, 1.0); material.setOverride(True); overlay.addChild(material)
            for parent in parents:
                frame = hierarchy.world_placement(self.doc, parent) if parent else App.Placement()
                transform = frame.multiply(motion).multiply(frame.inverse())
                for link in links:
                    sub = hierarchy.subname((*parent, link))
                    if not visible_reference(root, sub): continue
                    shape = Part.getShape(root, sub)
                    if shape.isNull(): continue
                    shape.Placement = transform.multiply(shape.Placement)
                    source = coin.SoInput(); source.setBuffer(shape.writeInventor())
                    overlay.addChild(coin.SoDB.readAll(source))
            if rotating: self.axis_preview(overlay, links)
            self.scene.addChild(overlay); self.overlay = overlay
            self.message.setText('Preview only. Apply commits one group movement.')
        except (ValueError, RuntimeError, ReferenceError) as error:
            self.message.setText(str(error))

    def reset_inputs(self, *args):
        self.busy = True
        self.direction_snapshot = None; self.direction.setCurrentIndex(0)
        self.distance.setProperty('rawValue', 0.0); self.reverse.setChecked(False)
        self.axis_snapshot = None; self.axis_points = [None,None]; self.pivot_snapshot = None
        self.axis.setCurrentIndex(0); self.angle.setProperty('rawValue',0.0)
        self.resolved_axis.setText('Choose an axis.')
        method = self.workflow.currentIndex()
        self.translate_form.setVisible(method == 0); self.rotate_form.setVisible(method == 1)
        self.reverse.setEnabled(method in (0,1))
        self.busy = False; self.update_preview()

    def apply(self):
        owner, links = self.check(); motion = self.motion()
        if motion.isSame(App.Placement(),1e-12):
            self.reset_inputs(); return
        if not links: raise ValueError('Select sibling component instances to move')
        placements = []
        for link in links:
            placements.append(motion.multiply(link.LinkPlacement))
        self.busy = True
        self.clear_preview()
        try:
            with document.transaction(owner.Document, 'Move component instances'):
                for link, placement in zip(links, placements): link.LinkPlacement = placement
        finally:
            self.busy = False
        if not self.persistent.isChecked(): self.clear()
        else: self.select_components()
        self.reset_inputs()

    def getStandardButtons(self):
        return QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Apply

    def clicked(self, button):
        if button == QtWidgets.QDialogButtonBox.Apply: self.run(self.apply)

    def accept(self):
        if self.run(self.apply): self.finish()
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
        if owner == self.doc or (self.parent_ref and owner.Name == self.parent_ref[0]): self.finish()

    def check_lifecycle(self):
        try:
            self.check()
            self.update_preview()
        except (ValueError, RuntimeError, ReferenceError): self.finish()

    def finish(self, *args):
        global _active
        if self.closed: return
        self.closed = True; self.clear_preview(); self.timer.stop()
        App.removeDocumentObserver(self); Gui.removeDocumentObserver(self)
        self.panel._mdi.subWindowActivated.disconnect(self.schedule)
        Gui.getMainWindow().workbenchActivated.disconnect(self.finish)
        editing.remove_context_observer(self.schedule)
        if self.window:
            try: self.window.destroyed.disconnect(self.finish)
            except (RuntimeError, TypeError): pass
        if _active is self:
            _active = None; Gui.Control.closeDialog()
        # Native TaskPanel owns and clears form when closeDialog destroys it.
        self.deleteLater()


def open_task(panel, rows):
    global _active
    panel._clipboard_guard()
    if Gui.Control.activeDialog(): raise ValueError('Finish the current task first')
    task = MoveTask(panel, rows)
    _active = task
    try: Gui.Control.showDialog(task)
    except Exception:
        task.finish(); raise
    return task
