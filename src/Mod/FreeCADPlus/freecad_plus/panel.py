# SPDX-License-Identifier: LGPL-2.1-or-later
"""Opt-in component panel foundation; rows project native ownership, never own it.

Placed and unused definitions share Edit and History. Temporary isolation is view-only;
component tabs reuse native views; other confirmed actions remain separate increments.
"""
from dataclasses import dataclass
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui
try:
    from PySide import QtWidgets
except ImportError:
    QtWidgets = QtGui

from . import document, editing, external, hierarchy, isolation

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
    history = []
    for obj in document.history(doc, active):
        if active is None:
            sub = root.Origin.Name + '.'
            if obj != root.Origin:
                sub += obj.Name + '.'
        else:
            sub = hierarchy.subname(active_path)
            body = obj.getParentGeoFeatureGroup()
            if body and body.TypeId == 'PartDesign::Body':
                sub += body.Name + '.'
            sub += obj.Name + '.'
        history.append(Row(('history', identity(obj)), 'history', obj.Label, identity(obj),
                           selection=((doc.Name, root.Name, sub) if active is None or active_path
                                      else (active.Document.Name, active.Name, sub)),
                           visible=bool(obj.Visibility) if active is None else None))
    return (tuple(models(external.catalog(doc))), (file_row,), tuple(history))


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
        self.refresh_count = 0
        self.tabs = QtWidgets.QTabWidget()
        self.trees = []
        for label in ('Models', 'Part Tree', 'History'):
            tree = QtWidgets.QTreeWidget()
            tree.setObjectName('Plus' + label.replace(' ', ''))
            tree.setHeaderHidden(True)
            tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            tree.setUniformRowHeights(True)
            tree.setItemDelegate(_Delegate(tree))
            tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            tree.viewport().installEventFilter(self)
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

    def eventFilter(self, watched, event):
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
        for bound, state in self._states:
            if bound == binding:
                return state
        state = {'last': {}}
        if self._mdi and binding == self._current():
            window = self._mdi.activeSubWindow()
            state['window'] = window
            state['component_window'] = bool(window.property('FreeCADPlusComponentWindow'))
            window.destroyed.connect(lambda *args: self._forget_view(binding))
        self._states.append((binding, state))
        return state

    def _context(self, doc, view):
        root = document.validate(doc)
        unused = editing.unused_context(doc)
        if unused is not None:
            return unused, ()
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
        if current and any(d.HasPendingTransaction for d in App.listDocuments().values()):
            return  # Commit/abort observer will schedule once the graph is complete.
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
            self.refresh_count += 1
        except (ValueError, RuntimeError, ReferenceError) as error:
            self._message(str(error))
            for index in range(3):
                self._reconcile(index, ())
        finally:
            self._updating = False
            self.setUpdatesEnabled(True)
        self._sync_selection()

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
                flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
                if row.visible is not None:
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

    def _model_route(self, row):
        options = [item.data(0, _ROLE).path for item in self._maps[1].values()
                   if item.data(0, _ROLE).kind == 'occurrence' and item.data(0, _ROLE).ref == row.ref]
        preferred = self._state(self._binding)['last'].get(row.ref)
        return preferred if preferred in options else (options[0] if options else ())

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

    def _menu(self, tree, point):
        item = tree.itemAt(point)
        if item is None:
            return
        row = item.data(0, _ROLE)  # Immutable identity, not a pointer into mutable rows.
        if row.kind not in ('file', 'model', 'occurrence', 'unused'):
            return
        menu = QtWidgets.QMenu(self)
        actions = {menu.addAction('Edit'): self.edit_row}
        if row.kind != 'file':
            actions[menu.addAction('Open in new window')] = self.open_row
        binding = self._binding
        chosen = menu.exec_(tree.viewport().mapToGlobal(point))
        if chosen in actions:
            try:
                if self._current() != binding:
                    raise ValueError('The active file tab changed; select the item again')
                actions[chosen](row)
            except (ValueError, RuntimeError, ReferenceError) as error:
                self._message(str(error))
        menu.deleteLater()

    def _selection_changed(self, tree):
        if self._updating or self._selecting or self._closed:
            return
        self._selecting = True
        try:
            selections = []
            for item in tree.selectedItems():
                row = item.data(0, _ROLE)
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
                item.setSelected(selection in selected)
            del blocker

    def _visibility_changed(self, item, column):
        if self._updating or self._closed:
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
        self.dispose()
        super().closeEvent(event)

    def dispose(self):
        if self._closed:
            return
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
                if hasattr(view, 'setDocumentContext'):
                    view.setDocumentContext()
            except (RuntimeError, ReferenceError):
                pass
        self._states.clear()
        self._binding = None


def show_panel():
    """Explicit developer opt-in; never removes the native tree/workbenches."""
    global _panel
    if _panel is None or _panel._closed:
        if _panel is not None:
            Gui.getMainWindow().removeDockWidget(_panel)
            _panel.deleteLater()
        _panel = ComponentPanel(Gui.getMainWindow())
        Gui.getMainWindow().addDockWidget(QtCore.Qt.LeftDockWidgetArea, _panel)
    _panel.show()
    _panel.raise_()
    _panel.schedule()
    return _panel
