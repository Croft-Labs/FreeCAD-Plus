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

from . import document, editing, external, hierarchy, isolation, display, assembly, constraints

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
    anchor: tuple = ()


def instance_rows(rows, condensed=False, parent_key=()):
    """Present repeated siblings without changing occurrence keys or selection routes."""
    siblings = {}
    for row in rows:
        if row.kind == 'occurrence':
            siblings.setdefault(row.ref, []).append(row)
    numbered, emitted, result = {}, set(), []
    for row in rows:
        members = siblings.get(row.ref, ()) if row.kind == 'occurrence' else ()
        if len(members) > 1:
            if (condensed.get((parent_key, row.ref), condensed.get(None, False)) if isinstance(condensed, dict) else condensed):
                if row.ref in emitted:
                    continue
                emitted.add(row.ref)
                children = tuple(replace(member, label=member.label + ' (' + str(index) + ')',
                                         children=instance_rows(member.children, condensed, member.key))
                                 for index, member in enumerate(members, 1))
                result.append(Row(('instance_group', parent_key, row.ref), 'instance_group',
                                  row.label + ' \u00d7' + str(len(members)), row.ref, children=children))
                continue
            numbered[row.ref] = numbered.get(row.ref, 0) + 1
            row = replace(row, label=row.label + ' (' + str(numbered[row.ref]) + ')')
        result.append(replace(row, children=instance_rows(row.children, condensed, row.key)))
    return tuple(result)


def projection(doc, active=None, active_path=(), assembly_root=None, assembly_path=(), condensed=False):
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
    def occurrences(owner, path=(), anchor=None):
        rows = []
        members = constraints.joints(owner)
        if members:
            refs = tuple(identity(item) for item in path)
            group = constraints.group_for(constraints.solver_for(owner))
            children = tuple(Row(('constraint', identity(joint), refs), 'constraint',
                                 joint.Label, identity(joint)) for joint in members)
            rows.append(Row(('constraints', identity(owner), refs), 'constraints',
                            'Assembly constraints', identity(group), children=children))
        for link in owner.Group:
            if link.TypeId != 'App::Link':
                continue
            route = (*path, link)
            refs = tuple(identity(item) for item in route)
            target = link.LinkedObject
            rows.append(Row(('occurrence', refs), 'occurrence',
                            assembly.label(target, doc), identity(target), refs,
                            ((anchor.Document.Name, anchor.Name, hierarchy.subname(route)) if anchor
                             else (doc.Name, root.Name, hierarchy.subname(route))),
                            tuple(occurrences(target, route, anchor)),
                            anchor=identity(anchor) if anchor else ()))
        return rows
    assembly_rows = ()
    if assembly_root is not None:
        anchor = None if assembly_path else assembly_root
        assembly_rows = (Row(('assembly', identity(assembly_root)), 'assembly',
                             assembly.label(assembly_root, doc), identity(assembly_root),
                             tuple(identity(item) for item in assembly_path),
                             (doc.Name, root.Name, hierarchy.subname(assembly_path)) if assembly_path
                             else (assembly_root.Document.Name, assembly_root.Name, ''),
                             tuple(occurrences(assembly_root, assembly_path, anchor))),)
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
        history.insert(0, Row(('history-component', identity(active)), 'history_component',
                              external.qualified_label(active, doc), identity(active),
                              tuple(identity(item) for item in active_path)))
    return (tuple(models(external.catalog(doc))), instance_rows(assembly_rows, condensed), tuple(history))


def history_visible(definition, obj):
    """Visibility within the component, independent of catalog/occurrence hiding."""
    route = document.owned_path(definition, obj)
    drawing = _panel._sketch_drawing if _panel is not None else None
    return route is not None and all(member.Visibility and not (
        drawing is not None and drawing.definition == definition and drawing.hides(member)) for member in route)


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


class ComponentTabBar(QtWidgets.QTabBar):
    def minimumTabSizeHint(self, index):
        size = self.tabSizeHint(index)
        selected_font = QtGui.QFont(self.font())
        selected_font.setBold(True)
        metrics = (self.fontMetrics(), QtGui.QFontMetrics(selected_font))
        width = max((metric.horizontalAdvance(self.tabText(i))
                     for metric in metrics for i in range(self.count())), default=0)
        option = QtWidgets.QStyleOptionTab()
        option.initFrom(self)
        option.shape = self.shape()
        option.rect = QtCore.QRect(QtCore.QPoint(), size)
        text_rect = self.style().subElementRect(QtWidgets.QStyle.SE_TabBarTabText, option, self)
        padding = max(0, size.width() - text_rect.width())
        size.setWidth(width + padding)
        return size

    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        width = max((self.fontMetrics().horizontalAdvance(self.tabText(i))
                     for i in range(self.count())), default=0)
        size.setWidth(width + 40)
        return size


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


class HistoryTree(QtWidgets.QTreeWidget):
    """Same-tree, single-feature insertion; native ownership is never dragged."""
    mime_type = 'application/x-freecad-plus-history'

    def __init__(self, panel):
        super().__init__()
        self.panel=panel;self.payload=None
        self.setDragEnabled(True);self.setAcceptDrops(True);self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)

    def drawRow(self, painter, option, index):
        row = index.siblingAtColumn(0).data(_ROLE)
        if row is not None and row.kind == 'history_component':
            # Only the component identity spans the eye and name columns.
            option = QtWidgets.QStyleOptionViewItem(option)
            option.rect.setLeft(0)
            option.rect.setRight(self.viewport().width() - 1)
            self.itemDelegate().paint(painter, option, index.siblingAtColumn(0))
            return
        super().drawRow(painter, option, index)

    def mimeTypes(self):return [self.mime_type]

    def startDrag(self, actions):
        items=self.selectedItems()
        if len(items)!=1:return
        item=items[0]
        if item.parent() is not None or not item.flags() & QtCore.Qt.ItemIsDragEnabled:return
        try:
            self.payload=self.panel.prepare_history_move(item.data(0,_ROLE))
            mime=QtCore.QMimeData();mime.setData(self.mime_type,b'feature')
            drag=QtGui.QDrag(self);drag.setMimeData(mime)
            drag.setPixmap(self.viewport().grab(self.visualItemRect(item)))
            drag.exec_(QtCore.Qt.MoveAction)
        except (ValueError,RuntimeError,ReferenceError) as error:self.panel._message(str(error))
        finally:self.payload=None

    def accepts_move(self,event):
        return event.source() is self and self.payload is not None and event.mimeData().hasFormat(self.mime_type)

    def dragEnterEvent(self,event):
        if self.accepts_move(event):super().dragEnterEvent(event)
        else:event.ignore()

    def dragMoveEvent(self,event):
        if self.accepts_move(event):super().dragMoveEvent(event)
        else:event.ignore()

    def dropEvent(self,event):
        if not self.accepts_move(event):event.ignore();return
        target=self.itemAt(event.position().toPoint())
        while target is not None and target.parent() is not None:target=target.parent()
        index=self.indexOfTopLevelItem(target) if target is not None else self.topLevelItemCount()
        if target is not None and event.position().y()>self.visualItemRect(target).center().y():index+=1
        try:
            # Component identity and coordinate rows are outside the feature list.
            position=sum(self.topLevelItem(i).data(0,_ROLE).kind == 'history' for i in range(index))
            message=self.panel.move_history(self.payload,position)
            event.acceptProposedAction()
            if message:
                QtCore.QTimer.singleShot(0,lambda: QtWidgets.QMessageBox.information(self.panel,'History order',message)
                                         if not self.panel._closed else None)
        except (ValueError,RuntimeError,ReferenceError) as error:
            event.ignore();self.panel._message(str(error))
        finally:
            self.setState(QtWidgets.QAbstractItemView.NoState);self.viewport().update()


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
        self._feature_scope = None
        self._sketch_drawing = None
        self._sketch_exit_fit = None
        self.refresh_count = 0
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabBar(ComponentTabBar())
        self.tabs.tabBar().setExpanding(False)
        self.tabs.setStyleSheet('QTabWidget::tab-bar { alignment: left; }')
        self.trees = []
        for label in ('Models', 'Part Tree', 'History'):
            tree = HistoryTree(self) if label == 'History' else QtWidgets.QTreeWidget()
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
            if label == 'Part Tree':
                # Double-click edits a component; only the disclosure arrow
                # changes its expansion. Condensed groups are handled below.
                tree.setExpandsOnDoubleClick(False)
                page = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout(page)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(4)
                from . import assembly_ui
                assembly_ui.configure(self, page, tree)
                layout.addWidget(tree)
                self.tabs.addTab(page, 'Assembly')
            else:
                self.tabs.addTab(tree, 'Parts' if label == 'Models' else label)
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
        # Some Part creation dialogs have no native getInEdit object. Listen to
        # the existing task-view signal as well, without polling every GUI tick.
        self._task_views = [widget for widget in parent.findChildren(QtWidgets.QWidget)
                            if widget.inherits('Gui::TaskView::TaskView')]
        for widget in self._task_views:
            QtCore.QObject.connect(widget, QtCore.SIGNAL('taskUpdate()'), self._part_dialog_updated)
        self.refresh()

    def toggle_history_visibility(self, row):
        doc, obj = self._checked(row)
        definition, path = self._context(doc, self._binding[1])
        from . import sketch_task, plane_task, extrude_task
        placement = sketch_task._active or plane_task._active
        extrude = extrude_task._active
        if placement is not None:
            placement.check()
            if placement.doc != doc or placement.definition != definition:
                raise ValueError('Use History for the component being edited')
        if extrude is not None:
            extrude.check()
            if extrude.doc != doc or extrude.owner != definition:
                raise ValueError('Use History for the component being edited')
        native = Gui.getDocument(doc.Name).getInEdit()
        if native is not None and document.owned_path(definition, native.Object) is None:
            raise ValueError('Use History for the component being edited')
        if placement is None and extrude is None and native is None and not Gui.Control.activeDialog():
            self._clipboard_guard()
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
        elif extrude is not None:
            extrude.presentation.toggle_many(routes, shown, row.label)
            extrude.refresh_visibility()
        elif self._sketch_drawing is not None:
            self._sketch_drawing.toggle_many(routes, shown, row.label)
        else:
            with document.visibility_transaction(obj.Document, ('Show ' if shown else 'Hide ') + row.label):
                change()
        self._refresh_history_eyes(definition)
        self.refresh()

    def _refresh_history_eyes(self, definition):
        # Native drawing keeps a transaction open: update only existing eye
        # decorations, not the ownership tree while its graph is being edited.
        blocker = QtCore.QSignalBlocker(self.trees[2])
        for item in self._maps[2].values():
            row = item.data(0, _ROLE)
            if row.kind == 'history_component':
                continue
            try:
                shown = history_row_visible(definition, row)
            except (ValueError, RuntimeError, ReferenceError):
                continue
            item.setIcon(1, _eye_icon(shown, self.trees[2].palette().text().color()))
            action = history_eye_action(row, shown)
            item.setToolTip(1, action)
            item.setData(1, QtCore.Qt.AccessibleTextRole, action)

    def _toggle_history_eye(self, item):
        if item.data(0, _ROLE).kind == 'history_component':
            return
        try:
            self.toggle_history_visibility(item.data(0, _ROLE))
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))

    def eventFilter(self, watched, event):
        if len(self.trees) > 1 and watched in (self.trees[1], self.trees[1].viewport()):
            from .assembly_visibility import event as assembly_eye_event
            if assembly_eye_event(self, watched, event):return True
        if (self.trees and watched in [tree.viewport() for tree in self.trees[::2]]
                and event.type() == QtCore.QEvent.MouseButtonPress
                and event.button() == QtCore.Qt.RightButton):
            # Capture viewport faces before Qt selects the clicked catalog row.
            from .appearance_task import selection_snapshot
            self._appearance_selection = selection_snapshot()
        if (len(self.trees) > 1 and watched in (self.trees[1], self.trees[1].viewport())
                and event.type() in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress)
                and event.key() == QtCore.Qt.Key_Delete):
            event.accept()  # Never fall through to native definition deletion in Assembly.
            if event.type() == QtCore.QEvent.KeyPress and not event.isAutoRepeat():
                try:
                    rows = tuple(item.data(0, _ROLE) for item in self.trees[1].selectedItems())
                    if len(rows) != 1:
                        raise ValueError('Select one individual child instance to remove')
                    self.remove_instance(rows[0])
                except (ValueError, RuntimeError, ReferenceError) as error:
                    self._message(str(error))
            return True
        if self._history_eyes and watched == self.trees[2].viewport():
            if event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonRelease,
                                QtCore.QEvent.MouseButtonDblClick):
                tree = self.trees[2]
                item = tree.itemAt(event.pos())
                component_row = item is not None and item.data(0, _ROLE).kind == 'history_component'
                if item and not component_row and tree.columnAt(event.pos().x()) == 1:
                    if event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick) and event.button() == QtCore.Qt.LeftButton:
                        self._toggle_history_eye(item)
                    return True
                if (item and not component_row and event.button() == QtCore.Qt.LeftButton
                        and tree.columnAt(event.pos().x()) == 0
                        and event.pos().x() >= tree.visualItemRect(item).left()):
                    from .selection_list import feature_picker_active, pick_intent
                    if feature_picker_active():
                        if event.type() == QtCore.QEvent.MouseButtonPress:
                            row = item.data(0, _ROLE)
                            if row.kind != 'history_group':
                                try:
                                    _, obj = self._checked(row)
                                    with pick_intent(bool(event.modifiers() & QtCore.Qt.ShiftModifier)):
                                        Gui.Selection.clearSelection()
                                        Gui.Selection.addSelection(*(row.selection or (obj.Document.Name, obj.Name, '')))
                                except (ValueError, RuntimeError, ReferenceError) as error:
                                    self._message(str(error))
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

    def begin_feature_task(self, token):
        self._sketch_exit_fit = None
        # Overlapping placement/native stages share one saved tab. Refreshes
        # never force it again, so users can browse other tabs during a task.
        current = self._current()
        if current is None or self._closed:
            return
        self._sync_feature_scope(current)
        if self._feature_scope is None:
            self._feature_scope = (current, self.tabs.currentIndex(), set())
            self.tabs.setCurrentIndex(2)
        self._feature_scope[2].add(token)

    def end_feature_task(self, token):
        if self._feature_scope is None or token not in self._feature_scope[2]:
            return
        self._feature_scope[2].discard(token)
        if not self._feature_scope[2]:
            self._restore_feature_tab()

    def _restore_feature_tab(self):
        if self._feature_scope is not None:
            previous = self._feature_scope[1]
            self._feature_scope = None
            self.tabs.setCurrentIndex(previous)

    def _sync_feature_scope(self, current):
        if self._sketch_drawing is not None:
            drawing = self._sketch_drawing
            try:
                matches = (current == drawing.binding and
                           self._context(*current)[0] == drawing.definition)
            except (ValueError, RuntimeError, ReferenceError):
                matches = False
            if not matches:
                self._restore_sketch_coordinates()
            else:
                drawing.apply()
        if self._feature_scope is not None and self._feature_scope[0] != current:
            self._restore_feature_tab()

    def _restore_sketch_coordinates(self):
        drawing = self._sketch_drawing
        self._sketch_drawing = None
        if drawing is not None:
            drawing.restore()

    def slotInEdit(self, view):
        if view.Object.isDerivedFrom('Part::Feature'):
            self.begin_feature_task(view.Object)
        current = self._current()
        if current is not None and view.Object.isDerivedFrom('Sketcher::SketchObject'):
            try:
                definition, _ = self._context(*current)
                if definition is not None and document.owned_path(definition, view.Object) is not None:
                    from .sketch_visibility import Drawing
                    self._restore_sketch_coordinates()
                    self._sketch_drawing = Drawing(definition, view.Object, current)
            except (ValueError, RuntimeError, ReferenceError):
                self._restore_sketch_coordinates()
        self.schedule()

    def slotResetEdit(self, view):
        drawing = self._sketch_drawing
        if self._sketch_drawing is not None and self._sketch_drawing.sketch == view.Object:
            self._restore_sketch_coordinates()
        else:
            drawing = None
        self.end_feature_task(view.Object)
        self.schedule()
        if drawing is not None:
            try:
                context = self._context(*drawing.binding)
                if context[0] != drawing.definition:
                    return
                token = (drawing.binding, context, identity(drawing.sketch))
                self._sketch_exit_fit = token
                # Native resetEdit still owns its viewer and transaction here.
                # Fit after camera restoration, coordinate restoration and layout.
                QtCore.QTimer.singleShot(0, lambda: self._fit_exited_sketch(token))
            except (ValueError, RuntimeError, ReferenceError):
                pass

    def _fit_exited_sketch(self, token):
        if self._closed or self._sketch_exit_fit is not token:
            return
        self._sketch_exit_fit = None
        binding, context, ref = token
        try:
            if (self._current() != binding or self._context(*binding) != context
                    or Gui.getDocument(binding[0].Name).getInEdit() is not None
                    or Gui.Control.activeDialog()):
                return
            sketch = lookup(ref)
            if (document.owned_path(context[0], sketch) is not None
                    and sketch.GeometryCount and not sketch.Shape.isNull()):
                binding[1].fitAll()
        except (ValueError, RuntimeError, ReferenceError):
            pass  # The sketch or its view may have closed before the queued fit.

    def _part_dialog_updated(self):
        # Control updates its active-dialog pointer after TaskView emits this
        # signal. Inspect only after that native show/remove call has unwound.
        QtCore.QTimer.singleShot(0, self._sync_part_dialog)

    def _sync_part_dialog(self):
        if self._closed:
            return
        dialog = Gui.Control.activeTaskDialog()
        widgets = dialog.getDialogContent() if dialog is not None else ()
        feature = any(child.metaObject().className().startswith(('PartGui::', 'PartDesignGui::'))
                      for widget in widgets for child in [widget, *widget.findChildren(QtWidgets.QWidget)])
        if feature:
            self.begin_feature_task('native-part-dialog')
        else:
            self.end_feature_task('native-part-dialog')

    def slotDeletedDocument(self, doc):
        owner = getattr(doc, 'Document', doc)
        if self._sketch_exit_fit is not None:
            binding, _, ref = self._sketch_exit_fit
            if owner == binding[0] or owner.Name == ref[0]:
                self._sketch_exit_fit = None
        if self._sketch_drawing is not None and owner in (
                self._sketch_drawing.binding[0], self._sketch_drawing.definition.Document):
            self._restore_sketch_coordinates()
        if self._feature_scope is not None and self._feature_scope[0][0] == owner:
            self._restore_feature_tab()
        self._states = [(bound, state) for bound, state in self._states if bound[0] != owner]
        if self._binding and self._binding[0] == owner:
            self._binding = None
        self._press = None
        self.schedule()

    def addSelection(self, *args):
        self._sync_selection(reveal=True)

    removeSelection = addSelection
    setSelection = addSelection
    clearSelection = addSelection

    def _current(self):
        doc = App.ActiveDocument
        if doc is None or not any('PlusFormat' in obj.PropertiesList for obj in doc.Objects):
            return None
        return doc, Gui.getDocument(doc.Name).activeView()

    def _forget_view(self, binding):
        if self._sketch_exit_fit is not None and self._sketch_exit_fit[0] == binding:
            self._sketch_exit_fit = None
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
        self._sync_feature_scope(current)
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
                    # Old documents remain navigable so conflicting definitions
                    # can be renamed; saving cannot preserve the conflict.
                    from . import naming
                    try:
                        naming.validate_for_save(doc)
                    except ValueError as error:
                        self._message(str(error))
                except ValueError as error:
                    active, path = None, ()
                    self._message(str(error))
                state = self._state(current)
                owner, owner_path = self._assembly_context(current, active, path)
                from .assembly_ui import state as instance_state
                rows = projection(doc, active, path, owner, owner_path, instance_state(self))
                if state.get('component_window'):
                    label = external.qualified_label(active, doc) if active else doc.Label
                    state['window'].widget().setWindowTitle(label + ' [*]')
                if active and path:
                    self._state(current)['last'][identity(active)] = tuple(identity(o) for o in path)
            self._assembly_eye_context = active, path
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
                    is_active = bool(active and row.ref == identity(active) and row.kind in ('model', 'occurrence', 'unused', 'history_component', 'assembly'))
                    is_file = current and not active and row.kind == 'file'
                    font = item.font(0); font.setBold(bool(is_active or is_file or row.kind == 'assembly')); item.setFont(0, font)
                    item.setData(0, _ACTIVE, bool(is_active or is_file))
                    item.setData(0, _EDITED, bool(target and row.kind in ('occurrence', 'assembly') and row.path == target))
                    item.setBackground(0, QtGui.QBrush(fill) if is_active or is_file else QtGui.QBrush())
                    dimmed = (active is not None and not path and
                              (row.kind == 'file' or (row.kind == 'occurrence' and not row.anchor)))
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
                                        + ('\nClone the whole object before using this geometry.' if part_type == 'Reference' else ''))
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

    def _assembly_context(self, binding, active=None, active_path=()):
        doc, view = binding
        state = self._state(binding)
        if 'assembly' not in state:
            definitions = document.validate(doc).Definitions
            chosen = assembly.recalled(doc)
            if chosen is None:
                chosen = definitions[0] if len(definitions) == 1 else active
            state['assembly'] = identity(chosen) if chosen is not None else None
            state['assembly_path'] = tuple(identity(o) for o in assembly.recalled_path(doc, chosen))
        try:
            owner = lookup(state['assembly']) if state['assembly'] else None
            if owner is not None and owner not in document.validate(owner.Document).Definitions:
                owner = None
        except (ValueError, RuntimeError, ReferenceError):
            owner = None
        if owner is None:
            definitions = document.validate(doc).Definitions
            owner = assembly.recalled(doc)
            if owner is None and len(definitions) == 1:
                owner = definitions[0]
            state['assembly'] = identity(owner) if owner is not None else None
            state['assembly_path'] = tuple(identity(o) for o in assembly.recalled_path(doc, owner))
        try:
            if owner is None:
                return None, ()
            paths = isolation.occurrences(doc, owner)
            preferred = state.get('assembly_path', ())
            path = next((p for p in paths if tuple(identity(o) for o in p) == preferred), None)
            if path is None:
                path = next((p for p in paths if tuple(active_path[:len(p)]) == p), paths[0] if paths else ())
            state['assembly_path'] = tuple(identity(o) for o in path)
            return owner, path
        except (ValueError, RuntimeError, ReferenceError):
            state['assembly'] = None
            state['assembly_path'] = ()
            return None, ()

    def _assembly_guard(self):
        self._clipboard_guard()
        if Gui.Control.activeDialog():
            raise ValueError('Finish the current task before changing the active assembly')
        current = self._current()
        if current is None or current != self._binding:
            raise ValueError('The active file tab changed; reopen the assembly selector')
        return current

    def activate_assembly(self, definition, path=None):
        binding = self._assembly_guard()
        if definition not in document.validate(definition.Document).Definitions:
            raise ValueError('Choose an available part as the active assembly')
        if path is not None and hierarchy.resolve(binding[0], path)[0] != definition:
            raise ValueError('The assembly occurrence changed; select it again')
        state = self._state(binding)
        state['assembly'] = identity(definition)
        state['assembly_path'] = tuple(identity(o) for o in path) if path else ()
        self.refresh()
        owner, route = self._assembly_context(binding)
        assembly.remember(binding[0], owner, route)

    def slotStartSaveDocument(self, doc, *args):
        # Save the current view's choice, including when the last explicit choice
        # was made in a different view of this file. Other files keep their bookmark.
        current = self._current()
        if current and current[0] == doc:
            owner, route = self._assembly_context(current)
            if owner is not None:
                assembly.remember(doc, owner, route)

    def make_active_assembly(self, row):
        self._assembly_guard()
        _, obj = self._checked(row)
        if row.kind != 'model':
            raise ValueError('Choose a part in Parts')
        self.activate_assembly(obj)

    def choose_assembly(self):
        try:
            binding = self._assembly_guard()
            catalog = assembly.files(binding[0])
            counts = assembly.counts([part for _, parts in catalog for part in parts])
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))
            return
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Choose active assembly')
        dialog.resize(420, 360)
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(QtWidgets.QLabel('Choose a part to show at the top of Assembly.'))
        choices = QtWidgets.QTreeWidget()
        choices.setColumnCount(2)
        choices.setHeaderLabels(['Part', 'Components'])
        choices.header().setStretchLastSection(False)
        choices.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        choices.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        choices.headerItem().setToolTip(1, 'Component instances at all assembly levels; excludes reference-only and excluded components.')
        choices.setRootIsDecorated(True)
        layout.addWidget(choices)
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        apply = buttons.addButton('Make active assembly', QtWidgets.QDialogButtonBox.AcceptRole)
        apply.setEnabled(False)
        layout.addWidget(buttons)
        current = self._state(binding).get('assembly')
        for doc, parts in catalog:
            group = None
            if doc != binding[0]:
                name = Path(doc.FileName).name if doc.FileName else doc.Label
                group = QtWidgets.QTreeWidgetItem(choices, [name, ''])
                group.setFlags(QtCore.Qt.ItemIsEnabled)
                group.setIcon(0, QtGui.QIcon(':/icons/freecad-plus.svg'))
            for definition in parts:
                ref = identity(definition)
                item = QtWidgets.QTreeWidgetItem(group if group is not None else choices,
                                                [definition.Label, str(counts[definition])])
                item.setIcon(0, definition.ViewObject.Icon)
                item.setData(0, _ROLE, ref)
                item.setTextAlignment(1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                if ref == current and group is None:
                    choices.setCurrentItem(item); apply.setEnabled(True)
            if group is not None:
                group.setExpanded(False)
        choices.currentItemChanged.connect(lambda item, previous: apply.setEnabled(bool(item and item.data(0, _ROLE))))
        def accept():
            item = choices.currentItem()
            if item is None or not item.data(0, _ROLE):
                return
            try:
                if self._current() != binding:
                    raise ValueError('The active file tab changed; reopen the assembly selector')
                self.activate_assembly(lookup(item.data(0, _ROLE)))
                dialog.accept()
            except (ValueError, RuntimeError, ReferenceError) as error:
                self._message(str(error))
                dialog.reject()
        buttons.accepted.connect(accept)
        buttons.rejected.connect(dialog.reject)
        dialog.exec_()
        dialog.deleteLater()

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
            from .assembly_visibility import protection
            _, protected_path = protection(doc, view)
            hidden = display.hidden_paths(doc, active, path, protected_path=protected_path)
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
        def sync(parent, entries, coordinate_branch=False):
            for position, row in enumerate(entries):
                item = previous.get(row.key)
                fresh = item is None
                expanded = item.isExpanded() if item is not None else False
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
                item.setIcon(0, QtGui.QIcon(':/icons/freecad-plus.svg') if row.kind in ('file', 'import') else obj.ViewObject.Icon)
                if index == 2 and row.kind == 'history':
                    from .history_operations import presentation
                    text, icon = presentation(obj, row.label, item.icon(0))
                    item.setText(0, text)
                    item.setIcon(0, icon)
                if row.kind == 'history_group' and row.label in ('Axes', 'Planes') and row.children:
                    item.setIcon(0, lookup(row.children[0].ref).ViewObject.Icon)
                if index == 2 and obj.TypeId == 'App::Point':
                    item.setToolTip(0, 'Point (0, 0, 0) in component coordinates')
                flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
                if index == 2 and row.kind == 'history_component':
                    item.setIcon(1, QtGui.QIcon())
                    item.setToolTip(0, 'Active component - right-click to rename')
                elif index == 2 and self._history_eyes:
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
                if index == 2 and self._history_eyes and not coordinate_branch and row.kind == 'history':
                    flags |= QtCore.Qt.ItemIsDragEnabled
                item.setFlags(flags)
                if index == 1:
                    from .assembly_visibility import refresh_item
                    refresh_item(self, item, row)
                if row.kind == 'instance_group':
                    item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicator)
                    item.setToolTip(0, 'Right-click for Expand instances or component actions')
                else:
                    item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicatorWhenChildless)
                current[row.key] = item
                coordinate_row = coordinate_branch or (index == 2 and row.kind == 'history_group'
                                                        and row.label == 'Coordinate System')
                sync(item, row.children, coordinate_row)
                if row.kind == 'instance_group':
                    item.setExpanded(False)
                elif fresh:
                    item.setExpanded(not coordinate_row and row.kind not in ('constraints', 'instance_group'))
                else:
                    # Qt clears expansion when a reused occurrence changes parent.
                    item.setExpanded(expanded)
        blocker = QtCore.QSignalBlocker(tree)
        sync(tree.invisibleRootItem(), rows)
        for key, item in previous.items():
            if key not in current:
                parent = item.parent() or tree.invisibleRootItem()
                parent.takeChild(parent.indexOfChild(item))
        self._maps[index] = current
        if index == 1:
            from .assembly_ui import attach
            attach(self, tree)
        del blocker

    def prepare_history_move(self, row):
        current=self._current()
        if current is None or current!=self._binding:raise ValueError('The view changed; drag the feature again.')
        if Gui.Control.activeDialog():raise ValueError('Finish the current feature task before reordering History.')
        doc,view=current;owner,path=self._context(doc,view)
        if owner is None:raise ValueError('Edit a component before reordering History.')
        ordered=document.history(doc,owner)
        if row.kind!='history' or lookup(row.ref) not in ordered:
            raise ValueError('The fundamental coordinate system cannot be reordered.')
        return (current,identity(owner),tuple(identity(o) for o in path),row.ref,tuple(identity(o) for o in ordered))

    def move_history(self,payload,position):
        binding,owner_ref,path_refs,feature_ref,expected=payload
        feature=lookup(feature_ref)
        row=Row(('history',feature_ref),'history',feature.Label,feature_ref)
        if self.prepare_history_move(row)!=payload:
            raise ValueError('History changed during the drag; try again.')
        message=document.reorder_history(binding[0],lookup(owner_ref),feature,position)
        self.refresh()
        tree=self.trees[2];item=self._maps[2].get(row.key)
        if item is not None:
            tree.setCurrentItem(item);tree.scrollToItem(item)
        return message

    def _message(self, text):
        self.message.setText(text)
        self.message.setVisible(bool(text))

    def _checked(self, row):
        if row.kind == 'instance_group':
            raise ValueError('Expand the group and choose an individual instance')
        if self._binding is None or self._current() != self._binding:
            raise ValueError('The active file tab changed; select the item again')
        obj = lookup(row.ref)
        doc = self._binding[0]
        document.validate(doc)
        if row.path:
            path = tuple(lookup(ref) for ref in row.path)
            definition = assembly.resolve(lookup(row.anchor), path) if row.anchor else hierarchy.resolve(doc, path)[0]
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
        if not rows or any(row.kind not in ('occurrence', 'assembly') or not row.path for row in rows):
            raise ValueError('Select placed component instances in Assembly to Copy')
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
        if row.kind not in ('file', 'occurrence', 'assembly'):
            raise ValueError('Select a file or placed component as the Paste destination')
        if not self._clipboard:
            raise ValueError('Copy component instances in Assembly first')
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
                anchor = lookup(row.anchor) if row.anchor else (owner if row.kind == 'assembly' and not row.path else root)
                Gui.Selection.addSelection(anchor.Document.Name, anchor.Name, hierarchy.subname((*parent_path, instance)))
        finally:
            self._selecting = False
        self._sync_selection()
        return instances

    def _model_route(self, row):
        options = [tuple(identity(link) for link in path) for path in isolation.occurrences(self._binding[0], lookup(row.ref))]
        preferred = self._state(self._binding)['last'].get(row.ref)
        return preferred if preferred in options else (options[0] if options else ())

    def rename_row(self, row):
        self._clipboard_guard()
        if Gui.Control.activeDialog():
            raise ValueError('Finish the current task first')
        def target():
            doc, obj = self._checked(row)
            available = (document.validate(obj.Document).Definitions if row.kind == 'assembly' or row.anchor
                         else external.available_definitions(document.validate(doc)))
            if (row.kind not in ('model', 'occurrence', 'unused', 'history_component', 'assembly') or obj not in available):
                raise ValueError('Choose an available component to rename')
            if row.kind == 'history_component':
                active, path = self._context(doc, self._binding[1])
                if active != obj or tuple(identity(item) for item in path) != row.path:
                    raise ValueError('The active component changed; reopen Rename')
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
        if row.kind not in ('model', 'occurrence', 'unused', 'assembly'):
            raise ValueError('Choose a component to open in a new window')
        if obj not in external.available_definitions(document.validate(doc)):
            self._clipboard_guard()
            App.setActiveDocument(obj.Document.Name)
            doc = obj.Document
            self._binding = self._current()
        route = () if row.anchor else (row.path if row.kind in ('occurrence', 'assembly') else self._model_route(row))
        view = editing.open_component_view(doc, obj, tuple(lookup(ref) for ref in route), detached=bool(row.anchor))
        binding = (doc, view)
        self._mdi.activeSubWindow().setProperty('FreeCADPlusComponentWindow', True)
        state = self._state(binding)
        state['component_window'] = True
        self.refresh()
        self._select_context(doc)
        return view

    def _assembly_edit_row(self, row):
        """Find an exact occurrence in the fixed assembly, or a catalog member's first use."""
        doc, obj = self._checked(row)
        active, path = self._context(*self._binding)
        anchor, route = self._assembly_context(self._binding, active, path)
        if anchor is None:return None
        rows = projection(doc, assembly_root=anchor, assembly_path=route)[1]
        def visit(entries):
            for entry in entries:
                if entry.kind in ('assembly', 'occurrence') and entry.ref == row.ref:
                    if row.kind not in ('assembly','occurrence') or (entry.path == row.path and entry.anchor == row.anchor):
                        return entry
                found = visit(entry.children)
                if found is not None:return found
        return visit(rows)

    def add_edit_actions(self, menu, actions, row):
        action = menu.addAction('Edit within assembly')
        try:action.setEnabled(self._assembly_edit_row(row) is not None)
        except (ValueError, RuntimeError, ReferenceError):action.setEnabled(False)
        actions[action] = lambda r: self.edit_row(r, mode='assembly')
        actions[menu.addAction('Edit in isolation')] = lambda r: self.edit_row(r, mode='isolation')

    def edit_row(self, row, mode=None):
        doc, obj = self._checked(row)
        if row.kind == 'constraint':
            constraints.open_task(joint=obj)
            return
        member = self._assembly_edit_row(row) if row.kind in ('model','unused','assembly','occurrence') else None
        if mode == 'assembly' and member is None:
            raise ValueError('This component is outside the active assembly')
        if member is not None and mode != 'isolation':
            anchor = lookup(member.anchor) if member.anchor else (obj if not member.path else None)
            if anchor is not None:
                if anchor not in external.available_definitions(document.validate(doc)):
                    App.setActiveDocument(anchor.Document.Name);doc = anchor.Document;self._binding = self._current()
                editing.edit_in_assembly(doc, anchor, tuple(lookup(ref) for ref in member.path))
            else:
                editing.edit(tuple(lookup(ref) for ref in member.path))
        elif mode == 'isolation':
            if obj not in external.available_definitions(document.validate(doc)):
                App.setActiveDocument(obj.Document.Name);doc = obj.Document;self._binding = self._current()
            editing.edit_unused(doc, obj, detached=True)
        elif row.kind == 'file':
            editing.edit_file(doc)
        elif row.kind in ('occurrence', 'assembly') and row.path and not row.anchor:
            editing.edit(tuple(lookup(ref) for ref in row.path))
        elif row.kind == 'history':
            editing.edit_feature(doc, obj)
            return
        elif row.kind == 'unused':
            editing.edit_unused(doc, obj)
        elif row.kind in ('model', 'assembly', 'occurrence'):
            if obj not in external.available_definitions(document.validate(doc)):
                # A loaded, unimported file remains independent. Edit in its own tab.
                App.setActiveDocument(obj.Document.Name)
                doc = obj.Document
                self._binding = self._current()
            route = () if row.anchor else self._model_route(row)
            if not route:
                editing.edit_unused(doc, obj, detached=bool(row.anchor))
            else:
                editing.edit(tuple(lookup(ref) for ref in route))
        else:
            return
        self.refresh()
        # Entering Edit marks the exact occurrence separately from all active rows.
        if row.kind != 'file':
            self._select_context(doc)

    def _select_context(self, doc):
        definition, route = editing.context_path(doc)
        root = document.validate(doc)
        self._selecting = True
        try:
            Gui.Selection.clearSelection()
            if route:
                Gui.Selection.addSelection(doc.Name, root.Name, hierarchy.subname(route))
            else:
                session = isolation.current(self._binding[1])
                if session and session.edit_path:
                    anchor = session.anchor_definition()
                    Gui.Selection.addSelection(anchor.Document.Name, anchor.Name,
                                               hierarchy.subname(tuple(isolation._resolve(ref) for ref in session.edit_path)))
                else:
                    Gui.Selection.addSelection(definition.Document.Name, definition.Name)
        finally:
            self._selecting = False
        self._sync_selection()

    def _edit_clicked(self, item):
        if item.data(0, _ROLE) is None:
            return
        row = item.data(0, _ROLE)
        if row.kind == 'instance_group':
            row = row.children[0]
        try:
            self.edit_row(row)
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))

    def _display_target(self, row):
        doc, obj = self._checked(row)
        active, route = self._context(doc, self._binding[1])
        owner = active or document.validate(doc)
        refs = tuple(identity(o) for o in route)
        if row.kind in ('model', 'unused', 'assembly') and obj == active:
            return owner, None
        if row.kind == 'occurrence':
            if row.anchor:
                anchor = lookup(row.anchor)
                parent = assembly.resolve(anchor, tuple(lookup(ref) for ref in row.path[:-1]))
                if parent == active:
                    return owner, lookup(row.path[-1])
                raise ValueError('Edit the component or its immediate parent to change this setting')
            if row.path == refs: return owner, None
            if row.path[:-1] == refs: return owner, lookup(row.path[-1])
        raise ValueError('Edit the component or its immediate parent to change this setting')

    def set_display(self, row, *, part_type=None, shown=None, expected=None):
        if part_type is not None:
            self._clipboard_guard()
            if Gui.Control.activeDialog(): raise ValueError('Finish the current task first')
        from .assembly_visibility import guard, target
        guard(self, row, shown=shown, part_type=part_type)
        owner, child = target(self, row) if shown is not None else self._display_target(row)
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
        from .file_workflows import choose_source
        filename = choose_source(self, 'Import Models into ' + title, 'import')
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
        if tree == self.trees[2] and row is not None and row.kind in ('history_component', 'history'):
            from .history_appearance_ui import history_menu
            try:history_menu(self, tree, point, row)
            except (ValueError, RuntimeError, ReferenceError) as error:self._message(str(error))
            return
        if row is not None and row.kind == 'constraint':
            menu = QtWidgets.QMenu(self)
            edit = menu.addAction('Edit')
            delete = menu.addAction('Delete')
            chosen = menu.exec_(tree.viewport().mapToGlobal(point))
            try:
                _, obj = self._checked(row)
                if chosen == edit:
                    constraints.open_task(joint=obj)
                elif chosen == delete:
                    self._clipboard_guard()
                    constraints.remove(obj)
                    self.refresh()
            except (ValueError, RuntimeError, ReferenceError) as error:
                self._message(str(error))
            menu.deleteLater()
            return
        group = row if row is not None and row.kind == 'instance_group' else None
        if group is not None:
            from .assembly_ui import choose_member
            row = group.children[0]
        component_row = row is not None and row.kind in ('file', 'model', 'occurrence', 'unused', 'assembly')
        history_component = row is not None and row.kind == 'history_component'
        if tree == self.trees[0] and row is not None and row.kind == 'import':
            from .file_actions_ui import subfile_menu
            return subfile_menu(self, tree, point, row)
        if tree == self.trees[0] and row is not None and row.kind == 'model':
            from .appearance_ui import parts_menu
            return parts_menu(self, tree, point, item, row)
        if not component_row and not history_component and tree != self.trees[0]:
            return
        menu = QtWidgets.QMenu(self)
        actions = {}
        if history_component:
            actions[menu.addAction('Rename')] = self.rename_row
        if tree == self.trees[0]:
            from .file_actions_ui import run_action
            actions[menu.addAction('Create new part file\u2026')] = lambda row: run_action(self, 'create', row)
            actions[menu.addAction('Import Models from File')] = self.import_models
            if row is not None and row.kind == 'model':
                actions[menu.addAction('Make active assembly')] = self.make_active_assembly
                selected = tuple(entry.data(0, _ROLE) for entry in tree.selectedItems()) if item.isSelected() else (row,)
                actions[menu.addAction('Add to active component…')] = lambda unused: self.add_component_rows(selected)
                actions[menu.addAction('Export parts to file…')] = lambda unused: self.export_rows(selected)
        if component_row:
            if row.kind == 'occurrence':
                from .instance_patterns import controller
                if controller(lookup(row.path[-1])) is not None:
                    from .instance_task import edit_row
                    actions[menu.addAction('Edit instance pattern')] = (lambda unused: choose_member(self, group, edit_row)) if group else edit_row
            if row.kind == 'file':
                actions[menu.addAction('Edit')] = self.edit_row
            else:
                self.add_edit_actions(menu, actions, row)
            if row.kind != 'file':
                actions[menu.addAction('Open in new window')] = self.open_row
                actions[menu.addAction('Rename')] = self.rename_row
        if tree == self.trees[1]:
            from .assembly_ui import members
            selected = members(tuple(entry.data(0, _ROLE) for entry in tree.selectedItems()) if item.isSelected() else (group or row,))
            menu.addSeparator()
            if row.kind == 'occurrence':
                actions[menu.addAction('Copy')] = lambda unused: self.copy_rows(selected)
                actions[menu.addAction('Move Components')] = lambda unused: self.move_rows(selected)
                actions[menu.addAction('Remove instance…')] = (lambda unused: choose_member(self, group, self.remove_instance)) if group else self.remove_instance
            elif row.kind == 'assembly' and row.path:
                actions[menu.addAction('Copy')] = lambda unused: self.copy_rows(selected)
            if row.kind in ('file', 'occurrence', 'assembly'):
                paste = menu.addAction('Paste')
                paste.setEnabled(bool(self._clipboard))
                actions[paste] = self.paste_row
        has_visibility = False
        try:
            if not component_row:
                raise ValueError('No component setting for this row')
            owner, child = self._display_target(row)
        except ValueError:
            pass
        else:
            expected = (identity(owner), identity(child) if child is not None else None)
            part_type, shown = display.state(child if child is not None else owner)
            from .assembly_visibility import protected
            is_root = protected(self, row)
            if is_root:shown = True
            if group is not None:
                from .assembly_ui import group_display
                try:
                    group_states = [display.state(c if c is not None else o)
                                    for o, c in (self._display_target(member) for member in group.children)]
                except ValueError:
                    group_states = []
            menu.addSeparator()
            types = menu.addMenu('Part Type')
            if group is not None:
                types.setEnabled(bool(group_states))
            for title in display.TYPES:
                action = types.addAction(title); action.setCheckable(True); action.setChecked(title == part_type)
                action.setEnabled(not (is_root and title == 'Excluded'))
                actions[action] = lambda r, value=title: self.set_display(r, part_type=value, expected=expected)
                if group is not None:
                    action.setChecked(all(kind == title for kind, visible in group_states))
                    actions[action] = lambda unused, value=title: group_display(self, group, part_type=value)
            visibility = menu.addMenu('Visibility')
            has_visibility = True
            if group is not None:
                visibility.setEnabled(bool(group_states))
            for title, value in (('Shown', True), ('Hidden', False)):
                action = visibility.addAction(title); action.setCheckable(True); action.setChecked(value == shown)
                action.setEnabled(not ((value and part_type == 'Excluded') or (not value and is_root)))
                actions[action] = lambda r, value=value: self.set_display(r, shown=value, expected=expected)
                if group is not None:
                    action.setChecked(all(visible == value for kind, visible in group_states))
                    action.setEnabled(not value or all(kind != 'Excluded' for kind, visible in group_states))
                    actions[action] = lambda unused, value=value: group_display(self, group, shown=value)
        if tree == self.trees[1] and not has_visibility and row is not None and row.kind in ('occurrence', 'assembly'):
            from .assembly_visibility import add_menu
            add_menu(self, menu, actions, group or row)
        if tree == self.trees[1] and row is not None and row.kind == 'occurrence':
            from .assembly_ui import add_group_action
            add_group_action(self, item, menu, actions)
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
                if group is not None:
                    current_group = self._maps[1].get(group.key)
                    if current_group is None or current_group.data(0, _ROLE).children != group.children:
                        raise ValueError('The group changed; reopen its menu')
                chosen_callbacks[-1](row)
            except (ValueError, RuntimeError, ReferenceError) as error:
                self._message(str(error))
        menu.deleteLater()

    def remove_instance(self, row):
        from .instance_remove_ui import open_dialog
        return open_dialog(self, row)

    def add_component_rows(self, rows):
        from .component_add import add_selected
        parts = [self._checked(row)[1] for row in rows if row.kind == 'model']
        return add_selected(self, parts)

    def export_rows(self, rows):
        from .part_transfer import ExportDialog
        _, expected = self._import_target()
        parts = [self._checked(row)[1] for row in rows if row.kind == 'model']
        def guard():
            if self._import_target()[1] != expected:
                raise ValueError('The editing context changed; reopen Export parts')
            for row in rows:
                if row.kind == 'model':
                    self._checked(row)
        dialog = ExportDialog(self, parts, guard)
        dialog.exec_()
        dialog.deleteLater()

    def move_rows(self, rows):
        from .movement import open_task
        return open_task(self, rows)

    def move_selected(self):
        try:
            rows = [item.data(0, _ROLE) for item in self.trees[1].selectedItems()]
            from .assembly_ui import members
            self.move_rows([row for row in members(rows) if row.kind == 'occurrence'])
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))

    def _selection_changed(self, tree):
        if self._updating or self._selecting or self._closed:
            return
        self._selecting = True
        try:
            selections = []
            for item in tree.selectedItems():
                row = item.data(0, _ROLE)
                if row.kind in ('history_group', 'history_component', 'constraints', 'instance_group'):
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

    def _sync_selection(self, reveal=False):
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
                chosen = (row.kind not in ('history_group', 'history_component', 'constraints', 'instance_group')
                          and selection in selected)
                newly_selected = chosen and not item.isSelected()
                item.setSelected(chosen)
                if tree is self.trees[1] and chosen and (reveal or newly_selected):
                    parent = item.parent()
                    while parent is not None:
                        # Preserve exact native selection without turning a condensed
                        # presentation group into an expandable assembly branch.
                        if parent.data(0, _ROLE).kind != 'instance_group':
                            parent.setExpanded(True)
                        parent = parent.parent()
            del blocker

    def _visibility_changed(self, item, column):
        if self._updating or self._closed or self._history_eyes or column != 0:
            return
        row = item.data(0, _ROLE)
        if row.visible is None:
            return
        try:
            doc, obj = self._checked(row)
            with document.visibility_transaction(doc, 'Change origin visibility'):
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
        from . import file_search_task
        if file_search_task._active is not None:
            file_search_task._active.reject()
        from . import appearance_task
        if appearance_task._active is not None:
            appearance_task._active.reject()
        if self._closed:
            return
        self._sketch_exit_fit = None
        self._restore_sketch_coordinates()
        self._restore_feature_tab()
        from . import movement
        if movement._active is not None and movement._active.panel is self:
            movement._active.finish()
        from . import instance_task
        if instance_task._active is not None:
            instance_task._active.finish()
        from . import clone_task
        if clone_task._active is not None:
            clone_task._active.reject()
        self._closed = True
        isolation.close_all()
        self._timer.stop()
        App.removeDocumentObserver(self)
        Gui.removeDocumentObserver(self)
        Gui.Selection.removeObserver(self)
        editing.remove_context_observer(self.schedule)
        for widget in self._task_views:
            try:
                QtCore.QObject.disconnect(widget, QtCore.SIGNAL('taskUpdate()'), self._part_dialog_updated)
            except RuntimeError:
                pass
        self._task_views.clear()
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


def show_created_component(doc, definition, path=()):
    """Creation-only navigation; factories/imports do not change the active part."""
    if path:
        editing.edit(path)
    else:
        editing.edit_unused(doc, definition)
    from . import ui_modes
    ui_modes.apply_modes()
    widget = _panel
    if widget is not None and not widget._closed:
        widget.refresh()
        widget._select_context(doc)
        widget.tabs.setCurrentIndex(2)
        Gui.Selection.clearSelection()
        widget._sync_selection()
        if ui_modes.modes()[0] == 'Plus':
            widget.show()
            widget.raise_()


def begin_feature_task(task):
    if _panel is not None and not _panel._closed:
        task._history_panel = _panel
        _panel.begin_feature_task(task)


def end_feature_task(task):
    owner = getattr(task, '_history_panel', None)
    if owner is not None:
        owner.end_feature_task(task)
        task._history_panel = None


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
