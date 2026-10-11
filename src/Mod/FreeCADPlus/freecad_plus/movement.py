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
        layout.addWidget(QtWidgets.QLabel('Direction'))
        self.direction = QtWidgets.QComboBox()
        self.direction.addItems(('Choose direction', 'Parent X', 'Parent Y', 'Parent Z', 'Picked line / edge / axis'))
        layout.addWidget(self.direction)
        self.pick = QtWidgets.QPushButton('Use selected direction'); self.pick.clicked.connect(lambda: self.run(self.pick_direction))
        layout.addWidget(self.pick)
        layout.addWidget(QtWidgets.QLabel('Distance'))
        self.distance = Gui.UiLoader().createWidget('Gui::InputField')
        self.distance.setProperty('unit', 'mm'); self.distance.setProperty('minimum', 0.0)
        self.distance.setProperty('rawValue', 0.0)
        layout.addWidget(self.distance)
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

    def pick_direction(self):
        self.check()
        selections = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('', 0) for sub in entry.SubElementNames]
        if len(selections) != 1: raise ValueError('Select one visible straight edge, line or axis')
        obj, sub = selections[0]
        if not visible_reference(obj, sub):
            raise ValueError('Choose a visible reference')
        # Native shape extraction composes the full picked occurrence transform.
        shape = Part.getShape(obj, sub, needSubElement=True)
        if shape.ShapeType != 'Edge' or not isinstance(shape.Curve, (Part.Line, Part.LineSegment)):
            raise ValueError('Direction requires a straight line or axis, not a curved edge')
        # Native datum/origin axes are infinite edges without endpoint vertices.
        vector = shape.tangentAt(0.0)
        if vector.Length < 1e-12: raise ValueError('The selected direction has zero length')
        self.direction_snapshot = self.parent_frame().Rotation.inverted().multVec(vector).normalize()
        self.direction.setCurrentIndex(4); self.update_preview()

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
            delta = self.delta()
            if not links or delta.Length == 0:
                self.message.setText('Select components and set a direction and distance.'); return
            root = document.validate(self.doc)
            parents = isolation.occurrences(self.doc, owner) if owner != root else [()]
            overlay = coin.SoSeparator()
            pick = coin.SoPickStyle(); pick.style = coin.SoPickStyle.UNPICKABLE; overlay.addChild(pick)
            style = coin.SoDrawStyle(); style.style = coin.SoDrawStyle.LINES; style.lineWidth = 2; style.setOverride(True); overlay.addChild(style)
            material = coin.SoBaseColor(); material.rgb = (0.1, 0.8, 1.0); material.setOverride(True); overlay.addChild(material)
            for parent in parents:
                frame = hierarchy.world_placement(self.doc, parent) if parent else App.Placement()
                shift = frame.Rotation.multVec(delta)
                for link in links:
                    sub = hierarchy.subname((*parent, link))
                    if not visible_reference(root, sub): continue
                    shape = Part.getShape(root, sub)
                    if shape.isNull(): continue
                    shape.translate(shift)
                    source = coin.SoInput(); source.setBuffer(shape.writeInventor())
                    overlay.addChild(coin.SoDB.readAll(source))
            self.scene.addChild(overlay); self.overlay = overlay
            self.message.setText('Preview only. Apply commits one group movement.')
        except (ValueError, RuntimeError, ReferenceError) as error:
            self.message.setText(str(error))

    def reset_inputs(self, *args):
        self.busy = True
        self.direction_snapshot = None; self.direction.setCurrentIndex(0)
        self.distance.setProperty('rawValue', 0.0); self.reverse.setChecked(False)
        enabled = self.workflow.currentIndex() == 0
        for control in (self.direction, self.distance, self.reverse, self.pick): control.setEnabled(enabled)
        self.busy = False; self.update_preview()

    def apply(self):
        owner, links = self.check(); delta = self.delta()
        if delta.Length == 0: return
        if not links: raise ValueError('Select sibling component instances to move')
        placements = []
        for link in links:
            placement = App.Placement(link.LinkPlacement); placement.Base = placement.Base + delta
            placements.append(placement)
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
