# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component panel foundation; rows project native ownership, never own it.

Placed and unused definitions share Edit and History. Temporary isolation is view-only;
component tabs reuse native views; other confirmed actions remain separate increments.
"""
from dataclasses import dataclass, replace
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui
try:
    from PySide import QtWidgets
except ImportError:
    QtWidgets = QtGui

from . import document, editing, external, hierarchy, isolation, display

_ROLE = QtCore.Qt.UserRole
_ACTIVE = _ROLE + 1
_EDITED = _ROLE + 2
_panel = None


def identity(obj):
    return (obj.Document.Name, str(obj.Document.Uid), obj.Name, obj.ID)


def lookup(ref):
    doc = App.listDocuments().get(ref[0])
    obj = doc.getObject(ref[2]) if doc and str(doc.Uid) == ref[1] else None
    if obj is None or obj.ID != ref[3]:
        raise ValueError("This item is no longer available; select it again")
    return obj


@dataclass(frozen=True)
class Row:
    key: tuple
    kind: str
    label: str
    ref: tuple
    path: tuple = ()
    selection: tuple = ()
    children: tuple = ()
    visible: object = None


def projection(doc, active=None, active_path=()):
    """Build immutable, identity-qualified rows from a validated component graph."""
    root = document.validate(doc)
    def models(group, ancestry=()):
        current = group['document']
        rows = [Row(('model', ancestry, identity(d)), 'model',
                    external.qualified_label(d, doc), identity(d)) for d in group['definitions']]
        for imported in group['imports']:
            other = imported['document']
            other_root = document.validate(other)
            branch = (*ancestry, str(other.Uid))
            rows.append(Row(('import', branch), 'import', Path(other.FileName).stem,
                            identity(other_root), children=tuple(models(imported, branch))))
        return rows
    def occurrences(owner, path=()):
        rows = []
        for link in owner.Group:
            if link.TypeId != 'App::Link':
                continue
            route = (*path, link)
            refs = tuple(identity(item) for item in route)
            target = link.LinkedObject
            rows.append(Row(('occurrence', refs), 'occurrence',
                            external.qualified_label(target, doc), identity(target), refs,
                            (doc.Name, root.Name, hierarchy.subname(route)),
                            tuple(occurrences(target, route))))
        return rows
    file_row = Row(('file', identity(root)), 'file', Path(doc.FileName).stem if doc.FileName else doc.Label,
                   identity(root), selection=(doc.Name, root.Name, ''),
                   children=tuple(occurrences(root)))
    if active is not None and not active_path:
        temporary = Row(('unused', identity(active)), 'unused',
                        external.qualified_label(active, doc) + ' (unused model)', identity(active),
                        selection=(active.Document.Name, active.Name, ''))
        file_row = Row(file_row.key, file_row.kind, file_row.label, file_row.ref,
                       selection=file_row.selection, children=(*file_row.children, temporary))
    def history_row(obj, label=None, children=()):
        if active is None:
            sub = root.Origin.Name + '.'
            if obj != root.Origin:
                sub += obj.Name + '.'
        else:
            sub = hierarchy.subname(active_path)
            sub += ''.join(member.Name + '.' for member in document.owned_path(active, obj))
        shown = history_visible(active, obj) if active is not None else bool(obj.Visibility)
        return Row(('history', identity(obj)), 'history', label or obj.Label, identity(obj),
                   selection=((doc.Name, root.Name, sub) if active is None or active_path
                              else (active.Document.Name, active.Name, sub)),
                   children=children, visible=shown)
    history = [history_row(obj) for obj in document.history(doc, active)]
    if active is not None:
        features = {obj.Role: obj for obj in active.Origin.OriginFeatures}
        roles = ('X_Axis', 'Y_Axis', 'Z_Axis', 'XY_Plane', 'XZ_Plane', 'YZ_Plane')
        def group(label, children):
            row = history_row(active.Origin, label, children)
            return replace(row, key=('history-group', identity(active.Origin), label),
                           kind='history_group', visible=aggregate_visibility(c.visible for c in children))
        point = next(obj for obj in features.values() if obj.TypeId == 'App::Point')
        axes = group('Axes', tuple(history_row(features[role], role.replace('_', ' ')) for role in roles[:3]))
        planes = group('Planes', tuple(history_row(features[role], role.replace('_', ' ')) for role in roles[3:]))
        history.insert(0, group('Coordinate System', (history_row(point, 'Origin'), axes, planes)))
    return (tuple(models(external.catalog(doc))), (file_row,), tuple(history))


def history_visible(definition, obj):
    """Visibility within the component, independent of catalog/occurrence hiding."""
    route = document.owned_path(definition, obj)
    return route is not None and all(member.Visibility for member in route)


def aggregate_visibility(states):
    states = tuple(states)
    return True if all(s is True for s in states) else False if all(s is False for s in states) else 'mixed'


def history_targets(definition, row):
    obj = lookup(row.ref)
    if row.kind == 'history':
        return (obj,)
    if (row.kind != 'history_group' or obj != definition.Origin
            or row.key != ('history-group', identity(obj), row.label)):
        raise ValueError('Choose an item in the edited component History')
    if row.label == 'Coordinate System':
        return (obj, *obj.OriginFeatures)
    types = {'Axes': 'App::Line', 'Planes': 'App::Plane'}
    if row.label not in types:
        raise ValueError('Unknown coordinate system group')
    return tuple(feature for feature in obj.OriginFeatures if feature.TypeId == types[row.label])


def history_row_visible(definition, row):
    targets = history_targets(definition, row)
    if row.kind == 'history_group' and row.label == 'Coordinate System':
        targets = targets[1:]
    return aggregate_visibility(history_visible(definition, obj) for obj in targets)


def history_eye_action(row, shown):
    if row.kind == 'history_group':
        return (('Hide all ' if shown is True else 'Show all ') + row.label
                + (' (partially visible)' if shown == 'mixed' else ''))
    return ('Hide ' if shown else 'Show ') + row.label


def _eye_icon(shown, color):
    pixmap = QtGui.QPixmap(24, 24)
    pixmap.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    color = QtGui.QColor(color)
    if not shown:
        color.setAlpha(145)
    painter.setPen(QtGui.QPen(color, 1.6))
    path = QtGui.QPainterPath()
    path.moveTo(3, 12)
    path.cubicTo(7, 5, 17, 5, 21, 12)
    path.cubicTo(17, 19, 7, 19, 3, 12)
    painter.drawPath(path)
    painter.setBrush(color)
    if shown == 'mixed':
        painter.drawLine(9, 12, 15, 12)
    else:
        painter.drawEllipse(QtCore.QPointF(12, 12), 2.5, 2.5)
    if not shown:
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        painter.setPen(QtGui.QPen(QtCore.Qt.transparent, 4))
        painter.drawLine(4, 20, 20, 4)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        painter.setPen(QtGui.QPen(color, 1.6))
        painter.drawLine(4, 20, 20, 4)
    painter.end()
    return QtGui.QIcon(pixmap)


class _Delegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        selected = bool(option.state & QtWidgets.QStyle.State_Selected)
        if index.data(_ACTIVE):
            option = QtWidgets.QStyleOptionViewItem(option)
            option.state &= ~QtWidgets.QStyle.State_Selected
        super().paint(painter, option, index)
        if selected or index.data(_EDITED):
            painter.save()
            pen = QtGui.QPen(option.palette.highlight().color(), 2)
            if not index.data(_EDITED):
                pen.setStyle(QtCore.Qt.DotLine)
            painter.setPen(pen)
            painter.drawRect(option.rect.adjusted(1, 1, -2, -2))
            painter.restore()


class ComponentPanel(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__('Components', parent)
        self.setObjectName('FreeCADPlusComponentPanel')
        self._closed = False
        self._binding = None
        self._states = []
        self._maps = [{}, {}, {}]
        self._updating = False
        self._selecting = False
        self._press = None
        self._clipboard = ()
        self._history_eyes = False
        self.refresh_count = 0
        self.tabs = QtWidgets.QTabWidget()
        self.trees = []
        for label in ('Models', 'Part Tree', 'History'):
            tree = QtWidgets.QTreeWidget()
            tree.setObjectName('Plus' + label.replace(' ', ''))
            tree.setHeaderHidden(True)
            if label == 'History':
                tree.setColumnCount(2)
                tree.header().setStretchLastSection(False)
                tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                tree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
                tree.setColumnWidth(1, 28)
                tree.header().moveSection(1, 0)
                tree.header().setSectionsMovable(False)
                tree.setTreePosition(0)
                tree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            tree.setUniformRowHeights(True)
            tree.setItemDelegate(_Delegate(tree))
            tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            tree.viewport().installEventFilter(self)
            tree.installEventFilter(self)
            tree.itemSelectionChanged.connect(lambda t=tree: self._selection_changed(t))
            tree.itemDoubleClicked.connect(lambda item, column: self._edit_clicked(item))
            tree.customContextMenuRequested.connect(lambda point, t=tree: self._menu(t, point))
            tree.itemChanged.connect(self._visibility_changed)
            self.tabs.addTab(tree, label)
            self.trees.append(tree)
        self.message = QtWidgets.QLabel()
        self.message.setWordWrap(True)
        self.message.hide()
        content = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tabs)
        layout.addWidget(self.message)
        self.setWidget(content)
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.refresh)
        self._mdi = parent.findChild(QtWidgets.QMdiArea)
        if self._mdi:
            self._mdi.subWindowActivated.connect(self.schedule)
        App.addDocumentObserver(self)
        Gui.addDocumentObserver(self)
        Gui.Selection.addObserver(self)
        editing.add_context_observer(self.schedule)
        self.refresh()

    def toggle_history_visibility(self, row):
        doc, obj = self._checked(row)
        definition, path = self._context(doc, self._binding[1])
        from . import sketch_task
        placement = sketch_task._active
        if placement is not None:
            placement.check()
            if placement.doc != doc or placement.definition != definition:
                raise ValueError('Use History for the component being edited')
        native = Gui.getDocument(doc.Name).getInEdit()
        drawing = (native is not None and native.Object.isDerivedFrom('Sketcher::SketchObject')
                   and document.owned_path(definition, native.Object) is not None)
        if placement is None and not drawing:
            self._clipboard_guard()
            if Gui.Control.activeDialog():
                raise ValueError('Finish the current task first')
        route = document.owned_path(definition, obj)
        if row.kind not in ('history', 'history_group') or not route:
            raise ValueError('Choose an item in the edited component History')
        sub = hierarchy.subname(path) + ''.join(member.Name + '.' for member in route)
        expected = ((doc.Name, document.validate(doc).Name, sub) if path
                    else (definition.Document.Name, definition.Name, sub))
        if row.selection != expected:
            raise ValueError('The edited component changed; select the item again')
        targets = history_targets(definition, row)
        routes = tuple(document.owned_path(definition, target) for target in targets)
        if any(not target_route for target_route in routes):
            raise ValueError('The edited component changed; select the item again')
        shown = history_row_visible(definition, row) is not True
        def change():
            for target_route in routes:
                if shown:
                    # Reveal native containers, never the definition/catalog or another occurrence.
                    for member in target_route[:-1]:
                        member.Visibility = True
                target_route[-1].Visibility = shown
        if placement is not None:
            placement.origin_visibility.toggle_many(routes, shown, row.label)
        elif drawing:
            # Join native Sketcher's current transaction. Never commit or replace
            # the operation merely to toggle a view property.
            change()
        else:
            with document.transaction(obj.Document, ('Show ' if shown else 'Hide ') + row.label):
                change()
        self._refresh_history_eyes(definition)
        self.refresh()

    def _refresh_history_eyes(self, definition):
        # Native drawing keeps a transaction open: update only existing eye
        # decorations, not the ownership tree while its graph is being edited.
        blocker = QtCore.QSignalBlocker(self.trees[2])
        for item in self._maps[2].values():
            row = item.data(0, _ROLE)
            try:
                shown = history_row_visible(definition, row)
            except (ValueError, RuntimeError, ReferenceError):
                continue
            item.setIcon(1, _eye_icon(shown, self.trees[2].palette().text().color()))
            action = history_eye_action(row, shown)
            item.setToolTip(1, action)
            item.setData(1, QtCore.Qt.AccessibleTextRole, action)

    def _toggle_history_eye(self, item):
        try:
            self.toggle_history_visibility(item.data(0, _ROLE))
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))

    def eventFilter(self, watched, event):
        if self._history_eyes and watched == self.trees[2].viewport():
            if event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonRelease,
                                QtCore.QEvent.MouseButtonDblClick):
                tree = self.trees[2]
                item = tree.itemAt(event.pos())
                if item and tree.columnAt(event.pos().x()) == 1:
                    if event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick) and event.button() == QtCore.Qt.LeftButton:
                        self._toggle_history_eye(item)
                    return True
        if self._history_eyes and watched == self.trees[2] and event.type() in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress):
            if event.key() == QtCore.Qt.Key_Space and self.trees[2].currentItem():
                event.accept()
                if event.type() == QtCore.QEvent.KeyPress and not event.isAutoRepeat():
                    self._toggle_history_eye(self.trees[2].currentItem())
                return True
        if not self._closed and event.type() == QtCore.QEvent.Paint:
            for _, state in self._states:
                if (watched == state.get('viewport') and state.get('fade_pending')
                        and not state.get('fade_retried')):
                    # One retry after native linked snapshots have had a draw.
                    # Further paints do not poll/rebuild the panel if still unavailable.
                    state['fade_retried'] = True
                    if not self._timer.isActive():
                        self._timer.start(0)
                    break
        if (len(self.trees) > 1 and watched in (self.trees[1], self.trees[1].viewport())
                and event.type() in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress)
                and (event.matches(QtGui.QKeySequence.Copy) or event.matches(QtGui.QKeySequence.Paste))):
            event.accept()  # Keep the native global document clipboard out of this tree action.
            if event.type() == QtCore.QEvent.KeyPress:
                try:
                    rows = tuple(item.data(0, _ROLE) for item in self.trees[1].selectedItems())
                    if event.matches(QtGui.QKeySequence.Copy):
                        self.copy_rows(rows)
                    elif len(rows) == 1:
                        self.paste_row(rows[0])
                    else:
                        raise ValueError('Select one file or component as the Paste destination')
                except (ValueError, RuntimeError, ReferenceError) as error:
                    self._message(str(error))
            return True
        if event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick):
            tree = next((t for t in self.trees if t.viewport() == watched), None)
            if tree and event.button() == QtCore.Qt.LeftButton:
                item = tree.itemAt(event.pos())
                row = item.data(0, _ROLE) if item else None
                token = (self._current(), row.key, row.ref) if row else None
                if event.type() == QtCore.QEvent.MouseButtonDblClick:
                    if token is None or token != self._press:
                        return True
                else:
                    self._press = token
        return super().eventFilter(watched, event)

    def schedule(self, *args):
        for _, state in self._states:
            state['fade_retried'] = False
        if not self._closed and not self._timer.isActive():
            self._timer.start(0)

    # Coalesce native bursts. No polling or rebuilding trees on paint/selection.
    slotCreatedObject = schedule
    slotDeletedObject = schedule
    slotChangedObject = schedule
    slotRecomputedDocument = schedule
    slotCommitTransaction = schedule
    slotAbortTransaction = schedule
    slotUndoDocument = schedule
    slotRedoDocument = schedule
    slotActivateDocument = schedule
    slotRelabelDocument = schedule
    slotChangedDocument = schedule
    slotResetEdit = schedule
    slotInEdit = schedule

    def slotDeletedDocument(self, doc):
        owner = getattr(doc, 'Document', doc)
        self._states = [(bound, state) for bound, state in self._states if bound[0] != owner]
        if self._binding and self._binding[0] == owner:
            self._binding = None
        self._press = None
        self.schedule()

    def addSelection(self, *args):
        self._sync_selection()

    removeSelection = addSelection
    setSelection = addSelection
    clearSelection = addSelection

    def _current(self):
        doc = App.ActiveDocument
        if doc is None or not any('PlusFormat' in obj.PropertiesList for obj in doc.Objects):
            return None
        return doc, Gui.getDocument(doc.Name).activeView()

    def _forget_view(self, binding):
        self._states = [(bound, state) for bound, state in self._states if bound != binding]
        if self._binding == binding:
            self._binding = None
        self._press = None
        self.schedule()

    def _state(self, binding):
        state = next((state for bound, state in self._states if bound == binding), None)
        if state is None:
            state = {'last': {}}
            self._states.append((binding, state))
        if self._mdi and 'window' not in state and binding == self._current():
            # Dock removal/layout changes can temporarily clear activeSubWindow
            # while the native document still owns a valid active view.
            window = self._mdi.activeSubWindow()
            if window is not None:
                state['window'] = window
                # Obtain the viewport through Qt's live child tree. The native
                # graphicsView wrapper may outlive its C++ widget during closure.
                viewport = None
                for child in window.widget().findChildren(QtWidgets.QWidget):
                    try:
                        if child.inherits('QOpenGLWidget'):
                            viewport = child
                            break
                    except RuntimeError:
                        continue  # A Qt wrapper queued for invalidation during teardown.
                if viewport is not None:
                    state['viewport'] = viewport
                    viewport.installEventFilter(self)
                state['component_window'] = bool(window.property('FreeCADPlusComponentWindow'))
                window.destroyed.connect(lambda *args: self._forget_view(binding))
        return state

    def _context(self, doc, view):
        root = document.validate(doc)
        unused = isolation.current(view)
        if unused is not None:
            return unused.definition(), ()
        resolved, parent, sub = view.getActiveObject('PlusEdit', False)
        if resolved == root and not sub:
            return None, ()
        if parent == root and sub:
            definition, path = hierarchy.resolve(doc, sub.rstrip('.').split('.'))
            if resolved == definition:
                return definition, path
        raise ValueError('Select Edit on the file or a component to establish an editing context')

    def refresh(self):
        if self._closed:
            return
        current = self._current()
        drawing = None
        if current:
            drawing = Gui.getDocument(current[0].Name).getInEdit()
            drawing = drawing is not None and drawing.Object.isDerivedFrom('Sketcher::SketchObject')
        if current and any(d.HasPendingTransaction for d in App.listDocuments().values()):
            if not drawing:
                return  # Other native operations may have an incomplete ownership graph.
        self._binding = current
        try:
            if current is None:
                rows = ((), (), ())
                active, path = None, ()
                self._message('Open a component document to use Components.')
            else:
                doc, view = current
                self._state(current)  # Own context cleanup for every visited view.
                if hasattr(view, 'setDocumentContext') and view.getActiveObject('SelectionContext') is None:
                    view.setDocumentContext(document.validate(doc))
                try:
                    active, path = self._context(doc, view)
                    self._message('')
                except ValueError as error:
                    active, path = None, ()
                    self._message(str(error))
                rows = projection(doc, active, path)
                state = self._state(current)
                if state.get('component_window'):
                    label = external.qualified_label(active, doc) if active else doc.Label
                    state['window'].widget().setWindowTitle(label + ' [*]')
                if active and path:
                    self._state(current)['last'][identity(active)] = tuple(identity(o) for o in path)
            self._history_eyes = active is not None
            self.trees[2].setColumnHidden(1, not self._history_eyes)
            self._updating = True
            self.setUpdatesEnabled(False)
            color = App.ParamGet('User parameter:BaseApp/Preferences/TreeView').GetUnsigned('TreeActiveColor', 1538528255)
            fill = QtGui.QColor((color >> 24) & 255, (color >> 16) & 255, (color >> 8) & 255, color & 255)
            target = tuple(identity(o) for o in path)
            for index, entries in enumerate(rows):
                self._reconcile(index, entries)
                for item in self._maps[index].values():
                    row = item.data(0, _ROLE)
                    is_active = bool(active and row.ref == identity(active) and row.kind in ('model', 'occurrence', 'unused'))
                    is_file = current and not active and row.kind == 'file'
                    font = item.font(0); font.setBold(bool(is_active or is_file)); item.setFont(0, font)
                    item.setData(0, _ACTIVE, bool(is_active or is_file))
                    item.setData(0, _EDITED, bool(target and row.kind == 'occurrence' and row.path == target))
                    item.setBackground(0, QtGui.QBrush(fill) if is_active or is_file else QtGui.QBrush())
                    dimmed = active is not None and not path and row.kind in ('file', 'occurrence')
                    item.setForeground(0, QtGui.QBrush(QtGui.QColor(128, 128, 128))
                                       if dimmed else QtGui.QBrush())
                    if index == 1 and row.kind in ('occurrence', 'unused'):
                        obj = lookup(row.path[-1]) if row.path else lookup(row.ref)
                        if row.path == target or row.kind == 'unused': obj = lookup(row.ref)
                        direct = row.kind == 'unused' or row.path == target or (row.path[:-1] == target)
                        part_type, shown = display.state(obj)
                        effective, visible = display.resolved(obj, direct=direct)
                        item.setToolTip(0, 'Part Type: ' + effective + (' (saved: ' + part_type + ')' if effective != part_type else '')
                                        + '\nVisibility: ' + ('Shown' if shown else 'Hidden')
                                        + ('\nExcluded cannot be shown or used as geometry.' if effective == 'Excluded' else '')
                                        + ('\nAdd Reference Feature before using this geometry.' if part_type == 'Reference' else ''))
            if not drawing:
                self._update_display_views()  # Sketcher owns its editing view overrides.
            self.refresh_count += 1
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))
            for index in range(3):
                self._reconcile(index, ())
        finally:
            self._updating = False
            self.setUpdatesEnabled(True)
        self._sync_selection()

    def _update_display_views(self):
        for (doc, view), state in self._states:
            try:
                supports_display = hasattr(view, 'setComponentHiddenPaths')
            except (RuntimeError, ReferenceError):
                # Native view destruction may precede the Qt window notification.
                self._forget_view((doc, view))
                continue
            if not supports_display:
                continue  # Earlier bounded native builds retain their original display.
            try:
                active, path = self._context(doc, view)
            except ValueError:
                # Match the panel's file projection after an uninitialized or deleted
                # Edit occurrence; never erase another view's rows for that context.
                active, path = None, ()
            hidden = display.hidden_paths(doc, active, path)
            # Native scene paths can change after recompute even with identical names.
            # Refresh is event-coalesced; there is no idle polling or property mutation.
            if isolation.current(view) is not None:
                view.setComponentHiddenPaths()
            else:
                display.apply_hidden(view, document.validate(doc), hidden)
            if hasattr(view, 'setComponentFade'):
                if path and isolation.current(view) is None:
                    state['fade_pending'] = not view.setComponentFade(
                        document.validate(doc), hierarchy.subname(path))
                else:
                    state['fade_pending'] = False
                    view.setComponentFade()

    def _reconcile(self, index, rows):
        tree, previous, current = self.trees[index], self._maps[index], {}
        def sync(parent, entries):
            for position, row in enumerate(entries):
                item = previous.get(row.key)
                fresh = item is None
                if fresh:
                    item = QtWidgets.QTreeWidgetItem()
                if (item.parent() or tree.invisibleRootItem()) != parent or parent.indexOfChild(item) != position:
                    old_parent = item.parent() or tree.invisibleRootItem()
                    old_index = old_parent.indexOfChild(item)
                    if old_index >= 0:
                        old_parent.takeChild(old_index)
                    parent.insertChild(position, item)
                item.setData(0, _ROLE, row)
                item.setText(0, row.label)
                obj = lookup(row.ref)
                item.setIcon(0, QtGui.QIcon(':/icons/freecad.svg') if row.kind in ('file', 'import') else obj.ViewObject.Icon)
                if row.kind == 'history_group' and row.label != 'Coordinate System':
                    item.setIcon(0, self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
                if index == 2 and obj.TypeId == 'App::Point':
                    item.setToolTip(0, 'Point (0, 0, 0) in component coordinates')
                flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
                if index == 2 and self._history_eyes:
                    shown = row.visible
                    item.setIcon(1, _eye_icon(shown, tree.palette().text().color()))
                    action = history_eye_action(row, shown)
                    item.setToolTip(1, action)
                    item.setData(1, QtCore.Qt.AccessibleTextRole, action)
                    item.setData(0, QtCore.Qt.CheckStateRole, None)
                elif row.visible is not None:
                    item.setIcon(1, QtGui.QIcon())
                    flags |= QtCore.Qt.ItemIsUserCheckable
                    item.setCheckState(0, QtCore.Qt.Checked if row.visible else QtCore.Qt.Unchecked)
                item.setFlags(flags)
                current[row.key] = item
                sync(item, row.children)
                if fresh:
                    item.setExpanded(True)
        blocker = QtCore.QSignalBlocker(tree)
        sync(tree.invisibleRootItem(), rows)
        for key, item in previous.items():
            if key not in current:
                parent = item.parent() or tree.invisibleRootItem()
                parent.takeChild(parent.indexOfChild(item))
        self._maps[index] = current
        del blocker

    def _message(self, text):
        self.message.setText(text)
        self.message.setVisible(bool(text))

    def _checked(self, row):
        if self._binding is None or self._current() != self._binding:
            raise ValueError('The active file tab changed; select the item again')
        obj = lookup(row.ref)
        doc = self._binding[0]
        document.validate(doc)
        if row.path:
            path = tuple(lookup(ref) for ref in row.path)
            definition, _ = hierarchy.resolve(doc, path)
            if definition != obj:
                raise ValueError('The selected occurrence changed; select it again')
        return doc, obj

    def _clipboard_guard(self):
        if any(Gui.getDocument(doc.Name).getInEdit() for doc in App.listDocuments().values()):
            raise ValueError('Finish the native feature editor first')
        if App.getActiveTransaction() or any(doc.HasPendingTransaction for doc in App.listDocuments().values()):
            raise ValueError('Finish the current operation first')

    def copy_rows(self, rows):
        self._clipboard_guard()
        rows = tuple(rows)
        if not rows or any(row.kind != 'occurrence' for row in rows):
            raise ValueError('Select placed component instances in Part Tree to Copy')
        for row in rows:
            self._checked(row)
        # A selected parent already includes its descendants through its definition.
        selected = {row.path for row in rows}
        snapshot = []
        seen = set()
        for row in rows:
            if row.path in seen or any(row.path[:n] in selected for n in range(1, len(row.path))):
                continue
            seen.add(row.path)
            instance = lookup(row.path[-1])
            snapshot.append((row.ref, tuple(instance.LinkPlacement.toMatrix().A),
                             bool(instance.LinkTransform), bool(instance.Visibility), display.state(instance)))
        self._clipboard = tuple(snapshot)
        self._message('Copied component instances. Select a destination and Paste.')

    def paste_row(self, row):
        self._clipboard_guard()
        doc, owner = self._checked(row)
        if row.kind not in ('file', 'occurrence'):
            raise ValueError('Select a file or placed component as the Paste destination')
        if not self._clipboard:
            raise ValueError('Copy component instances in Part Tree first')
        entries = [(lookup(ref), App.Placement(App.Matrix(*matrix)), transform, visible)
                   for ref, matrix, transform, visible, choice in self._clipboard]
        instances = hierarchy.add_instances(owner, entries, display_states=[entry[4] for entry in self._clipboard])
        # Keep Edit and History unchanged; select only the newly placed occurrences.
        self.refresh()
        root = document.validate(doc)
        parent_path = tuple(lookup(ref) for ref in row.path)
        self._selecting = True
        try:
            Gui.Selection.clearSelection()
            for instance in instances:
                Gui.Selection.addSelection(doc.Name, root.Name, hierarchy.subname((*parent_path, instance)))
        finally:
            self._selecting = False
        self._sync_selection()
        return instances

    def _model_route(self, row):
        options = [item.data(0, _ROLE).path for item in self._maps[1].values()
                   if item.data(0, _ROLE).kind == 'occurrence' and item.data(0, _ROLE).ref == row.ref]
        preferred = self._state(self._binding)['last'].get(row.ref)
        return preferred if preferred in options else (options[0] if options else ())

    def rename_row(self, row):
        self._clipboard_guard()
        if Gui.Control.activeDialog():
            raise ValueError('Finish the current task first')
        def target():
            doc, obj = self._checked(row)
            if (row.kind not in ('model', 'occurrence', 'unused') or
                    obj not in external.available_definitions(document.validate(doc))):
                raise ValueError('Choose an available component to rename')
            return obj
        definition = target()
        binding, previous = self._binding, definition.Label
        label, accepted = QtWidgets.QInputDialog.getText(
            self, 'Rename Component', 'Component name (all instances):',
            QtWidgets.QLineEdit.Normal, previous)
        if not accepted:
            return False
        self._clipboard_guard()
        if Gui.Control.activeDialog():
            raise ValueError('Finish the current task first')
        if self._current() != binding:
            raise ValueError('The active file tab changed; reopen Rename')
        target()
        if definition.Label != previous:
            raise ValueError('The component name changed; reopen Rename')
        changed = hierarchy.rename_definition(definition, label)
        self.refresh()
        return changed

    def open_row(self, row):
        doc, obj = self._checked(row)
        if row.kind not in ('model', 'occurrence', 'unused'):
            raise ValueError('Choose a component to open in a new window')
        route = row.path if row.kind == 'occurrence' else self._model_route(row)
        view = editing.open_component_view(doc, obj, tuple(lookup(ref) for ref in route))
        binding = (doc, view)
        self._mdi.activeSubWindow().setProperty('FreeCADPlusComponentWindow', True)
        state = self._state(binding)
        state['component_window'] = True
        self.refresh()
        self._select_context(doc)
        return view

    def edit_row(self, row):
        doc, obj = self._checked(row)
        if row.kind == 'file':
            editing.edit_file(doc)
        elif row.kind == 'occurrence':
            editing.edit(tuple(lookup(ref) for ref in row.path))
        elif row.kind == 'history':
            editing.edit_feature(doc, obj)
            return
        elif row.kind == 'unused':
            editing.edit_unused(doc, obj)
        elif row.kind == 'model':
            route = self._model_route(row)
            if not route:
                editing.edit_unused(doc, obj)
            else:
                editing.edit(tuple(lookup(ref) for ref in route))
        else:
            return
        self.refresh()
        # Entering Edit marks the exact occurrence separately from all active rows.
        if row.kind != 'file':
            self._select_context(doc)
            self.tabs.setCurrentIndex(2)

    def _select_context(self, doc):
        definition, route = editing.context_path(doc)
        root = document.validate(doc)
        self._selecting = True
        try:
            Gui.Selection.clearSelection()
            if route:
                Gui.Selection.addSelection(doc.Name, root.Name, hierarchy.subname(route))
            else:
                Gui.Selection.addSelection(definition.Document.Name, definition.Name)
        finally:
            self._selecting = False
        self._sync_selection()

    def _edit_clicked(self, item):
        try:
            self.edit_row(item.data(0, _ROLE))
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))

    def _display_target(self, row):
        doc, obj = self._checked(row)
        active, route = self._context(doc, self._binding[1])
        owner = active or document.validate(doc)
        refs = tuple(identity(o) for o in route)
        if row.kind in ('model', 'unused') and obj == active:
            return owner, None
        if row.kind == 'occurrence':
            if row.path == refs: return owner, None
            if row.path[:-1] == refs: return owner, lookup(row.path[-1])
        raise ValueError('Edit the component or its immediate parent to change this setting')

    def set_display(self, row, *, part_type=None, shown=None, expected=None):
        self._clipboard_guard()
        if Gui.Control.activeDialog(): raise ValueError('Finish the current task first')
        owner, child = self._display_target(row)
        current = (identity(owner), identity(child) if child is not None else None)
        if expected is not None and current != expected:
            raise ValueError('The editing context changed; reopen the menu')
        display.set_state(owner, child, part_type=part_type, shown=shown)
        self.refresh()

    def _import_target(self):
        self._clipboard_guard()
        if Gui.Control.activeDialog():
            raise ValueError('Finish the current task first')
        if self._binding is None or self._current() != self._binding:
            raise ValueError('Activate a component file before importing models')
        doc, view = self._binding
        active, route = self._context(doc, view)
        target = active.Document if active is not None else doc
        root = document.validate(target)
        return target, (self._binding, identity(root), identity(active) if active is not None else None)

    def import_models(self, row=None):
        target, expected = self._import_target()
        title = Path(target.FileName).stem if target.FileName else target.Label
        filename, selected_filter = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Import Models into ' + title, '', 'FreeCAD Plus component (*.cadprt)')
        if not filename:
            return None
        target, current = self._import_target()
        if current != expected:
            raise ValueError('The editing context changed; reopen Import Models')
        result = external.import_path(target, filename)
        self.refresh()
        return result

    def _menu(self, tree, point):
        item = tree.itemAt(point)
        row = item.data(0, _ROLE) if item else None
        component_row = row is not None and row.kind in ('file', 'model', 'occurrence', 'unused')
        if not component_row and tree != self.trees[0]:
            return
        menu = QtWidgets.QMenu(self)
        actions = {}
        if tree == self.trees[0]:
            actions[menu.addAction('Import Models from File')] = self.import_models
        if component_row:
            actions[menu.addAction('Edit')] = self.edit_row
            if row.kind != 'file':
                actions[menu.addAction('Open in new window')] = self.open_row
                actions[menu.addAction('Rename')] = self.rename_row
        if tree == self.trees[1]:
            selected = tuple(entry.data(0, _ROLE) for entry in tree.selectedItems()) if item.isSelected() else (row,)
            menu.addSeparator()
            if row.kind == 'occurrence':
                actions[menu.addAction('Copy')] = lambda unused: self.copy_rows(selected)
                actions[menu.addAction('Move Components')] = lambda unused: self.move_rows(selected)
            if row.kind in ('file', 'occurrence'):
                paste = menu.addAction('Paste')
                paste.setEnabled(bool(self._clipboard))
                actions[paste] = self.paste_row
        try:
            if not component_row:
                raise ValueError('No component setting for this row')
            owner, child = self._display_target(row)
        except ValueError:
            pass
        else:
            expected = (identity(owner), identity(child) if child is not None else None)
            part_type, shown = display.state(child if child is not None else owner)
            menu.addSeparator()
            types = menu.addMenu('Part Type')
            for title in display.TYPES:
                action = types.addAction(title); action.setCheckable(True); action.setChecked(title == part_type)
                actions[action] = lambda r, value=title: self.set_display(r, part_type=value, expected=expected)
            visibility = menu.addMenu('Visibility')
            for title, value in (('Shown', True), ('Hidden', False)):
                action = visibility.addAction(title); action.setCheckable(True); action.setChecked(value == shown)
                action.setEnabled(not (value and part_type == 'Excluded'))
                actions[action] = lambda r, value=value: self.set_display(r, shown=value, expected=expected)
        binding = self._binding
        # Capture a Python callback while the native action is alive. Qt may
        # replace nested QAction wrappers as the popup closes.
        chosen_callbacks = []
        for action, callback in actions.items():
            action.triggered.connect(lambda checked=False, callback=callback: chosen_callbacks.append(callback))
        menu.exec_(tree.viewport().mapToGlobal(point))
        if chosen_callbacks:
            try:
                if self._current() != binding:
                    raise ValueError('The active file tab changed; select the item again')
                chosen_callbacks[-1](row)
            except (ValueError, RuntimeError, ReferenceError) as error:
                self._message(str(error))
        menu.deleteLater()

    def move_rows(self, rows):
        from .movement import open_task
        return open_task(self, rows)

    def _selection_changed(self, tree):
        if self._updating or self._selecting or self._closed:
            return
        self._selecting = True
        try:
            selections = []
            for item in tree.selectedItems():
                row = item.data(0, _ROLE)
                if row.kind == 'history_group':
                    continue
                _, obj = self._checked(row)
                selections.append(row.selection or (obj.Document.Name, obj.Name, ''))
            Gui.Selection.clearSelection()
            for doc, name, sub in selections:
                Gui.Selection.addSelection(doc, name, sub)
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))
        finally:
            self._selecting = False

    def _sync_selection(self):
        if self._closed or self._selecting or self._updating or not self._binding:
            return
        selected = set()
        for entry in Gui.Selection.getSelectionEx('', 0):
            for sub in entry.SubElementNames or ('',):
                selected.add((entry.DocumentName, entry.ObjectName, sub))
        for tree, items in zip(self.trees, self._maps):
            blocker = QtCore.QSignalBlocker(tree)
            for item in items.values():
                row = item.data(0, _ROLE)
                selection = row.selection or (row.ref[0], row.ref[2], '')
                item.setSelected(row.kind != 'history_group' and selection in selected)
            del blocker

    def _visibility_changed(self, item, column):
        if self._updating or self._closed or self._history_eyes or column != 0:
            return
        row = item.data(0, _ROLE)
        if row.visible is None:
            return
        try:
            doc, obj = self._checked(row)
            if Gui.getDocument(doc.Name).getInEdit():
                raise ValueError('Finish the native feature editor first')
            with document.transaction(doc, 'Change origin visibility'):
                obj.Visibility = item.checkState(0) == QtCore.Qt.Checked
                root = document.validate(doc)
                if obj.Visibility and obj != root.Origin:
                    root.Origin.Visibility = True
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))
        self.schedule()

    def closeEvent(self, event):
        if getattr(self, '_ui_mode_managed', False):
            self.hide()
            event.ignore()
            return
        self.dispose()
        super().closeEvent(event)

    def dispose(self):
        if self._closed:
            return
        from . import movement
        if movement._active is not None and movement._active.panel is self:
            movement._active.finish()
        self._closed = True
        isolation.close_all()
        self._timer.stop()
        App.removeDocumentObserver(self)
        Gui.removeDocumentObserver(self)
        Gui.Selection.removeObserver(self)
        editing.remove_context_observer(self.schedule)
        if self._mdi:
            self._mdi.subWindowActivated.disconnect(self.schedule)
        for (doc, view), state in self._states:
            try:
                if hasattr(view, 'setComponentFade'):
                    view.setComponentFade()
                if hasattr(view, 'setComponentHiddenPaths'):
                    view.setComponentHiddenPaths()
                if hasattr(view, 'setDocumentContext'):
                    view.setDocumentContext()
            except (RuntimeError, ReferenceError):
                pass
        self._states.clear()
        self._clipboard = ()
        self._binding = None


def show_panel():
    """Create or show the shared panel; ui_modes controls normal presentation."""
    global _panel
    if _panel is None or _panel._closed:
        if _panel is not None:
            previous, _panel = _panel, None
            Gui.getMainWindow().removeDockWidget(previous)
            previous.deleteLater()
        _panel = ComponentPanel(Gui.getMainWindow())
        Gui.getMainWindow().addDockWidget(QtCore.Qt.LeftDockWidgetArea, _panel)
    _panel.show()
    _panel.raise_()
    _panel.schedule()
    return _panel
