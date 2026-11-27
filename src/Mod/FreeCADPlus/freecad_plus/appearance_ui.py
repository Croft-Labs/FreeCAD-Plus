# SPDX-License-Identifier: LGPL-2.1-or-later
"""Shared appearance task controls and Parts menu presentation."""
from PySide6 import QtCore, QtGui, QtWidgets


def parts_menu(panel, tree, point, item, row):
    from .panel import _ROLE, identity
    from . import display
    menu = QtWidgets.QMenu(panel)
    menu.setSeparatorsCollapsible(False)
    actions = {}
    selected = tuple(entry.data(0, _ROLE) for entry in tree.selectedItems()) if item.isSelected() else (row,)
    menu.addSeparator()
    panel.add_edit_actions(menu, actions, row)
    actions[menu.addAction('Make active assembly')] = panel.make_active_assembly
    actions[menu.addAction('Add to active component\u2026')] = lambda unused: panel.add_component_rows(selected)
    actions[menu.addAction('Open in new window')] = panel.open_row
    actions[menu.addAction('Rename')] = panel.rename_row
    menu.addSeparator()
    initial = getattr(panel, '_appearance_selection', None)
    panel._appearance_selection = None
    def appearance(row):
        from .appearance_task import open_task
        _, owner = panel._checked(row)
        open_task(owner, initial)
    actions[menu.addAction(QtGui.QIcon(':/icons/Std_SetAppearance.svg'), 'Appearance\u2026')] = appearance
    types = menu.addMenu('Part Type')
    visibility = menu.addMenu('Visibility')
    try:
        owner, child = panel._display_target(row)
        expected = (identity(owner), identity(child) if child is not None else None)
        part_type, shown = display.state(child if child is not None else owner)
    except ValueError as error:
        for submenu in (types, visibility):
            submenu.setEnabled(False);submenu.setToolTip(str(error))
    else:
        for title in display.TYPES:
            action = types.addAction(title); action.setCheckable(True); action.setChecked(title == part_type)
            actions[action] = lambda r, value=title: panel.set_display(r, part_type=value, expected=expected)
        for title, value in (('Shown', True), ('Hidden', False)):
            action = visibility.addAction(title); action.setCheckable(True); action.setChecked(value == shown)
            action.setEnabled(not (value and part_type == 'Excluded'))
            actions[action] = lambda r, value=value: panel.set_display(r, shown=value, expected=expected)
    menu.addSeparator()
    from .file_actions_ui import run_action
    actions[menu.addAction('Create new part file\u2026')] = lambda row: run_action(panel, 'create', row)
    actions[menu.addAction('Import\u2026')] = panel.import_models
    actions[menu.addAction('Export\u2026')] = lambda unused: panel.export_rows(selected)
    menu.addSeparator()
    binding = panel._binding; chosen = []
    for action, callback in actions.items():
        action.triggered.connect(lambda checked=False, callback=callback: chosen.append(callback))
    menu.exec_(tree.viewport().mapToGlobal(point))
    if chosen:
        try:
            if panel._current() != binding:
                raise ValueError('The active file tab changed; select the item again')
            chosen[-1](row)
        except (ValueError, RuntimeError, ReferenceError) as error:
            panel._message(str(error))
    menu.deleteLater()


class AppearanceForm(QtWidgets.QWidget):
    targetsChanged = QtCore.Signal()
    def __init__(self, component, catalog, targets, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Appearance')
        self.setWindowIcon(QtGui.QIcon(':/icons/Std_SetAppearance.svg'))
        self.catalog = catalog
        self.targets = list(targets)
        self.mode = 'body'
        self.color_value = QtGui.QColor('#b9c4cf')
        self.color_changed = False
        self.setMinimumWidth(330)
        layout = QtWidgets.QVBoxLayout(self); layout.setSpacing(10)
        buttons = QtWidgets.QHBoxLayout()
        self.done = QtWidgets.QPushButton('Done')
        self.apply = QtWidgets.QPushButton('Apply')
        self.cancel = QtWidgets.QPushButton('Cancel')
        for button in (self.done, self.apply, self.cancel): buttons.addWidget(button)
        title = QtWidgets.QLabel(component); font = title.font();font.setBold(True);title.setFont(font)
        layout.addWidget(title)
        modes = QtWidgets.QHBoxLayout()
        self.body = QtWidgets.QRadioButton('Body');self.face = QtWidgets.QRadioButton('Face')
        self.body.setChecked(True)
        modes.addWidget(self.body);modes.addWidget(self.face);modes.addStretch()
        layout.addLayout(modes)
        self.count = QtWidgets.QLabel();layout.addWidget(self.count)
        self.items = QtWidgets.QListWidget()
        self.items.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.items.setMinimumHeight(165);self.items.setMaximumHeight(190)
        self.items.setAccessibleName('Selected bodies or faces')
        layout.addWidget(self.items)
        tools = QtWidgets.QHBoxLayout()
        self.remove = QtWidgets.QPushButton('Remove');self.clear = QtWidgets.QPushButton('Clear')
        tools.addWidget(self.remove);tools.addWidget(self.clear);tools.addStretch();layout.addLayout(tools)
        self.hint = QtWidgets.QLabel('Click the list, then pick bodies in the 3D view. Shift-click removes an item.')
        self.hint.setWordWrap(True);layout.addWidget(self.hint)
        group = QtWidgets.QGroupBox('Appearance');props = QtWidgets.QVBoxLayout(group)
        color_row = QtWidgets.QHBoxLayout();color_row.addWidget(QtWidgets.QLabel('Color'))
        self.color = QtWidgets.QPushButton();self.color.setMinimumHeight(30);color_row.addWidget(self.color,1)
        props.addLayout(color_row);self.refresh_color()
        props.addWidget(QtWidgets.QLabel('Transparency'))
        alpha = QtWidgets.QHBoxLayout()
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal);self.slider.setRange(0,100)
        self.value = QtWidgets.QSpinBox();self.value.setRange(-1,100);self.value.setSpecialValueText('Mixed');self.value.setSuffix(' %')
        self.slider.setAccessibleName('Transparency');self.value.setAccessibleName('Transparency percent')
        self.slider.valueChanged.connect(self.value.setValue)
        self.value.valueChanged.connect(lambda value: self.slider.setValue(value) if value >= 0 else None)
        alpha.addWidget(self.slider,1);alpha.addWidget(self.value);props.addLayout(alpha);layout.addWidget(group)
        self.scope = QtWidgets.QLabel();self.scope.setWordWrap(True);layout.addWidget(self.scope)
        shared = QtWidgets.QLabel('Changes affect all instances of this component.');shared.setWordWrap(True);layout.addWidget(shared)
        help = QtWidgets.QLabel('Apply keeps this task open. Cancel discards unapplied changes.');help.setWordWrap(True);layout.addWidget(help)
        from .task_status import TaskStatus
        self.status = TaskStatus();self.status.hide();layout.addWidget(self.status)
        layout.addLayout(buttons)
        layout.addStretch()
        self.body.toggled.connect(lambda checked: self.switch('body') if checked else None)
        self.face.toggled.connect(lambda checked: self.switch('face') if checked else None)
        self.remove.clicked.connect(self.remove_selected);self.clear.clicked.connect(self.clear_targets)
        self.delete = QtGui.QShortcut(QtGui.QKeySequence.Delete, self.items)
        self.delete.activated.connect(self.remove_selected)
        self.color.clicked.connect(self.choose_color)
        self.refresh_targets()

    def switch(self, mode):
        if mode == self.mode: return
        if mode == 'face':
            self.targets = [(body, face) for body, unused in self.targets for face in self.catalog[body]['faces']]
        else:
            self.targets = list(dict.fromkeys((body, None) for body, face in self.targets))
        self.mode = mode;self.refresh_targets()
        self.targetsChanged.emit()

    def refresh_targets(self):
        self.items.clear()
        for body, face in self.targets:
            text = self.catalog[body]['label'] + (' / '+face if face else '')
            self.items.addItem(text)
        self.count.setText(('Selected bodies' if self.mode == 'body' else 'Selected faces')+' ('+str(len(self.targets))+')')
        self.hint.setText('Click the list, then pick '+('bodies' if self.mode == 'body' else 'faces')+' in the 3D view. Shift-click removes an item.')
        self.scope.setText('A new color replaces face colors on the listed bodies. Child components keep their colors.' if self.mode == 'body' else 'Only the listed faces change. Other faces keep their appearance.')
        self.done.setEnabled(True);self.apply.setEnabled(bool(self.targets))

    def remove_selected(self):
        rows = {self.items.row(item) for item in self.items.selectedItems()}
        self.targets = [target for i,target in enumerate(self.targets) if i not in rows];self.refresh_targets()
        self.targetsChanged.emit()

    def clear_targets(self):
        self.targets = [];self.refresh_targets()
        self.targetsChanged.emit()

    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor(self.color_value or QtGui.QColor('#b9c4cf'), self, 'Choose color')
        if color.isValid(): self.color_value = color;self.color_changed = True;self.refresh_color()

    def refresh_color(self):
        if self.color_value is None:
            self.color.setIcon(QtGui.QIcon());self.color.setText('Mixed - choose color\u2026');return
        pix = QtGui.QPixmap(24,16);pix.fill(self.color_value)
        self.color.setIcon(QtGui.QIcon(pix));self.color.setText(self.color_value.name().upper()+'  Change\u2026')
