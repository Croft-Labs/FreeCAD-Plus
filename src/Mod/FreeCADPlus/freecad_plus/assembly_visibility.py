# SPDX-License-Identifier: LGPL-2.1-or-later
"""Inline Assembly eyes, occurrence-owned visibility and protected assembly roots."""
from PySide6 import QtCore, QtGui, QtWidgets
from . import assembly, display, document, hierarchy


def protection(doc, view):
    from .panel import _panel, lookup
    if _panel is None:return None, ()
    state = next((s for binding, s in _panel._states if binding == (doc, view)), {})
    try:
        owner = lookup(state['assembly']) if state.get('assembly') else None
        path = tuple(lookup(ref) for ref in state.get('assembly_path', ()))
        if path and hierarchy.resolve(doc, path)[0] != owner:return None, ()
        return owner, path
    except (ValueError, RuntimeError, ReferenceError):return None, ()


def protected(panel, row):
    from .panel import lookup
    if panel._binding is None:return False
    owner, _ = panel._assembly_context(panel._binding)
    return owner is not None and lookup(row.ref) == owner


def guard(panel, row, *, shown=None, part_type=None):
    if (shown is False or part_type == 'Excluded') and protected(panel, row):
        raise ValueError('The active assembly must remain visible')


def target(panel, row, *, check=True):
    """Validate the full route and use the child's actual defining parent."""
    from .panel import lookup, identity
    doc, obj = panel._checked(row) if check else (panel._binding[0], lookup(row.ref))
    if row.kind == 'assembly':return obj, None
    if row.kind != 'occurrence':return panel._display_target(row)
    active, active_path = (panel._context(doc, panel._binding[1]) if check else
                           getattr(panel, '_assembly_eye_context', (None, ())))
    if row.path == tuple(identity(o) for o in active_path) and active_path:
        return active, None  # Match the established active-component display setting.
    path = tuple(lookup(ref) for ref in row.path)
    if not path:raise ValueError('Choose an available child occurrence')
    if row.anchor:
        owner = path[-2].LinkedObject if len(path) > 1 else lookup(row.anchor)
        from . import isolation
        session = isolation.current(panel._binding[1])
        if session and session.ref == row.anchor and session.edit_path == row.path:
            return active, None
    else:
        owner = path[-2].LinkedObject if len(path) > 1 else document.validate(doc)
    return owner, path[-1]


def details(panel, row, *, check=True):
    rows = row.children if row.kind == 'instance_group' else (row,)
    values = [display.state(child if child is not None else owner)
              for owner, child in (target(panel, member, check=check) for member in rows)]
    from .panel import aggregate_visibility
    shown = aggregate_visibility(kind != 'Excluded' and visible for kind, visible in values)
    enabled = shown is True or all(kind != 'Excluded' for kind, visible in values)
    if not enabled:tip = 'Change Part Type before showing an Excluded component'
    elif row.kind == 'instance_group':
        tip = ('Hide all instances' if shown is True else 'Show all instances')
        if shown == 'mixed':tip += ' (partially visible)'
    else:tip = ('Hide ' if shown is True else 'Show ') + row.label
    return shown, enabled, tip


def refresh_item(panel, item, row):
    from .panel import _ROLE
    value = None
    if row.kind in ('occurrence', 'instance_group'):
        try:value = details(panel, row, check=False)
        except (ValueError, RuntimeError, ReferenceError):value = (False, False, 'This instance is no longer available')
    item.setData(0, _ROLE + 4, value)


def eye_rect(tree, item):
    from .panel import _ROLE
    if item is None or item.data(0, _ROLE + 4) is None:return None
    rect = tree.visualItemRect(item)
    return QtCore.QRect(rect.left(), rect.top(), 26, rect.height())


def toggle(panel, row):
    from .panel import _ROLE
    item = panel._maps[1].get(row.key)
    if item is None or item.data(0, _ROLE) != row:
        raise ValueError('The assembly changed; choose the instance again')
    if row.kind not in ('occurrence', 'instance_group'):return
    shown, enabled, tip = details(panel, row)
    if not enabled:raise ValueError(tip)
    if row.kind == 'instance_group':
        from .assembly_ui import group_display
        group_display(panel, row, shown=shown is not True)
    else:panel.set_display(row, shown=shown is not True)


def add_menu(panel, menu, actions, row):
    from .assembly_ui import group_display
    try:
        is_root = protected(panel, row)
        shown, enabled, tip = (True, False, 'The active assembly must remain visible') if is_root else details(panel, row)
    except (ValueError, RuntimeError, ReferenceError):return
    menu.addSeparator();submenu = menu.addMenu('Visibility')
    for title, value in (('Shown', True), ('Hidden', False)):
        action = submenu.addAction(title);action.setCheckable(True);action.setChecked(shown is value)
        action.setEnabled(not is_root and (not value or enabled))
        if row.kind == 'instance_group':
            actions[action] = lambda unused, value=value: group_display(panel, row, shown=value)
        else:actions[action] = lambda unused, value=value: panel.set_display(row, shown=value)


def event(panel, watched, event):
    from .panel import _ROLE
    tree = panel.trees[1];kind = event.type()
    if watched == tree and kind in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress):
        if event.key() == QtCore.Qt.Key_Space:
            event.accept()
            if kind == QtCore.QEvent.KeyPress and not event.isAutoRepeat() and tree.currentItem():
                try:toggle(panel, tree.currentItem().data(0, _ROLE))
                except (ValueError, RuntimeError, ReferenceError) as error:panel._message(str(error))
            return True
    if watched != tree.viewport():return False
    if kind == QtCore.QEvent.ToolTip:
        item = tree.itemAt(event.pos());rect = eye_rect(tree, item)
        if rect is not None and rect.contains(event.pos()):
            QtWidgets.QToolTip.showText(event.globalPos(), item.data(0, _ROLE + 4)[2], tree)
            return True
    if kind not in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonRelease,
                    QtCore.QEvent.MouseButtonDblClick) or event.button() != QtCore.Qt.LeftButton:return False
    item = tree.itemAt(event.pos());rect = eye_rect(tree, item)
    pending = getattr(panel, '_assembly_eye_press', None)
    inside = rect is not None and rect.contains(event.pos())
    if kind == QtCore.QEvent.MouseButtonRelease and pending:
        panel._assembly_eye_press = None
        if inside and pending == (panel._current(), item.data(0, _ROLE)):
            try:toggle(panel, item.data(0, _ROLE))
            except (ValueError, RuntimeError, ReferenceError) as error:panel._message(str(error))
        return True
    if inside:
        panel._assembly_eye_press = (panel._current(), item.data(0, _ROLE)) if kind == QtCore.QEvent.MouseButtonPress else None
        return True
    return False


def install_delegate(tree):
    from .panel import _Delegate, _ROLE, _eye_icon
    class Delegate(_Delegate):
        def paint(self, painter, option, index):
            value = index.data(_ROLE + 4) if index.column() == 0 else None
            if value is None:return super().paint(painter, option, index)
            shifted = QtWidgets.QStyleOptionViewItem(option);shifted.rect.adjust(26, 0, 0, 0)
            super().paint(painter, shifted, index)
            rect = QtCore.QRect(option.rect.left(), option.rect.top(), 26, option.rect.height())
            if option.state & QtWidgets.QStyle.State_Selected:painter.fillRect(rect, option.palette.highlight())
            color = option.palette.text().color()
            if not value[1]:color.setAlpha(130)
            _eye_icon(value[0], color).paint(painter, QtCore.QRect(rect.left()+5, rect.center().y()-8, 16, 16))

        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            if index.column() == 0 and index.data(_ROLE + 4) is not None:size.setWidth(size.width()+26)
            return size
    tree.setItemDelegate(Delegate(tree))
