# SPDX-License-Identifier: LGPL-2.1-or-later
"""Separate Plus ribbon widgets over Classic's native actions and menus.

Never move a Classic toolbar/widget or duplicate a command callback. In particular,
sharing the group QAction AND its QMenu preserves native last-action bookkeeping,
menu preparation, enablement, checked state, shortcuts and command dispatch.
"""
import re
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from . import toolbar_layout as layout

_controller = None


def preferences():
    return App.ParamGet('User parameter:BaseApp/Preferences/FreeCADPlus/Toolbars')


class ModeModel(QtCore.QAbstractListModel):
    """Own plain mode data without transient QStandardItem Python wrappers."""
    def __init__(self, parent):
        super().__init__(parent)
        self.entries = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return 0 if parent.isValid() else len(self.entries)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < len(self.entries):
            return None
        mode, owner, enabled = self.entries[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return mode
        if role == QtCore.Qt.UserRole:
            return (mode, owner)
        if role == QtCore.Qt.ToolTipRole and not enabled:
            return 'This workbench is not available in this build.'
        return None

    def flags(self, index):
        if not index.isValid() or not 0 <= index.row() < len(self.entries):
            return QtCore.Qt.NoItemFlags
        return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
                if self.entries[index.row()][2] else QtCore.Qt.NoItemFlags)

    def replace(self, modes, available):
        self.beginResetModel()
        self.entries = [(mode, owner, owner in available) for mode, owner in modes]
        self.endResetModel()


class ModeSelector(QtWidgets.QComboBox):
    def __init__(self, refresh):
        super().__init__()
        self._refresh = refresh
        self.mode_model = ModeModel(self)
        self.setModel(self.mode_model)

    def showPopup(self):
        # Include workbenches registered since the last tab/workbench change.
        self._refresh()
        super().showPopup()


class Ribbon(QtCore.QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.enabled = False
        self.refreshing = False
        self.sources = {}
        self.native = {}
        self.inventory_names = set()
        self.workbench = ''
        self.mode = 'Design'
        self.tab = 'Modeling'
        self.tabs = []
        self.bar = QtWidgets.QToolBar('Plus ribbon', window)
        self.bar.setObjectName('FreeCADPlusRibbon')
        self.bar.setMovable(False)
        self.bar.setFloatable(False)
        self.bar.toggleViewAction().setVisible(False)
        self.host = QtWidgets.QWidget()
        self.host.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        root = QtWidgets.QVBoxLayout(self.host)
        root.setContentsMargins(4, 2, 4, 2)
        root.setSpacing(2)
        self.top = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QHBoxLayout(self.top)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.selector = ModeSelector(self.refresh_modes)
        self.selector.setObjectName('PlusModeSelector')
        self.selector.setAccessibleName('Plus mode')
        self.selector.currentIndexChanged.connect(self.select_mode)
        self.top_layout.addWidget(self.selector)
        self.common = QtWidgets.QWidget()
        self.top_layout.addWidget(self.common)
        self.top_layout.addStretch()
        root.addWidget(self.top)
        self.tabbar = QtWidgets.QTabBar()
        self.tabbar.setObjectName('PlusRibbonTabs')
        self.tabbar.setExpanding(False)
        self.tabbar.setUsesScrollButtons(True)
        self.tabbar.currentChanged.connect(self.select_tab)
        root.addWidget(self.tabbar)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setMinimumHeight(137)
        root.addWidget(self.scroll)
        self.bar.addWidget(self.host)
        window.addToolBar(QtCore.Qt.TopToolBarArea, self.bar)
        self.bar.hide()
        QtWidgets.QApplication.instance().focusChanged.connect(self.observe_customization)

    def native_bars(self):
        # Customization can create a plain QToolBar before the next workbench
        # activation. Include only declared native groups, never nested Plus
        # controls or separate Draft status widgets.
        return [bar for bar in self.window.findChildren(QtWidgets.QToolBar)
                if bar is not self.bar and (bar.inherits('Gui::ToolBar')
                or bar.property('FreeCADPlusClassicVisible') is not None
                or (bar.parentWidget() == self.window and bar.objectName() in self.inventory_names))]

    def customization_opened(self):
        for dialog in self.window.findChildren(QtWidgets.QDialog):
            self.observe_customization(None, dialog)

    def observe_customization(self, previous, current):
        if current is None:
            return
        dialog = current.window()
        if (isinstance(dialog, QtWidgets.QDialog)
                and dialog.inherits('Gui::Dialog::DlgCustomizeImp')
                and not dialog.property('FreeCADPlusObserved')):
            dialog.setProperty('FreeCADPlusObserved', True)
            dialog.finished.connect(lambda result: QtCore.QTimer.singleShot(0, self.refresh))

    def apply(self, enabled):
        if self.enabled == enabled:
            if enabled:
                self.refresh()
            return
        self.enabled = enabled
        if enabled:
            self.refresh()
        else:
            self.bar.hide()
            for bar in self.native_bars():
                visible = bar.property('FreeCADPlusClassicVisible')
                available = bar.property('FreeCADPlusClassicAvailable')
                if visible is not None:
                    bar.setProperty('FreeCADPlusClassicVisible', None)
                    bar.setProperty('FreeCADPlusClassicAvailable', None)
                    bar.toggleViewAction().setVisible(available)
                    bar.setVisible(visible)

    def suppress_native(self, bar, visible):
        if self.enabled and visible and not bar.property('FreeCADPlusUpdatingNative'):
            bar.setProperty('FreeCADPlusClassicVisible', True)
            bar.toggleViewAction().setVisible(False)
            bar.hide()

    def _navigate(self, workbench):
        if not workbench or workbench == Gui.activeWorkbench().name():
            return True
        # Switching the backend during a live native task may cancel its workflow.
        doc = Gui.activeDocument()
        if Gui.Control.activeDialog() or (doc and doc.getInEdit()):
            self.window.statusBar().showMessage('Finish the active task before changing workbench.', 5000)
            return False
        try:
            Gui.activateWorkbench(workbench)
            return Gui.activeWorkbench().name() == workbench
        except Exception as exc:
            App.Console.PrintError('Plus toolbar: %s\n' % exc)
            return False

    def select_mode(self, index):
        if self.refreshing or index < 0:
            return
        mode, workbench = self.selector.itemData(index)
        if self._navigate(workbench):
            self.workbench = Gui.activeWorkbench().name()
            self.mode = mode
            self.tab = 'Modeling' if mode == 'Design' else 'Home'
        self.refresh()

    def select_tab(self, index):
        if self.refreshing or index < 0:
            return
        tab, workbench = self.tabs[index]
        if self._navigate(workbench):
            self.workbench = Gui.activeWorkbench().name()
            self.tab = tab
        self.refresh()

    def _modes(self, available):
        modes = [('Design', 'PartDesignWorkbench')] + list(layout.MODE_WORKBENCHES)
        mapped = {wb for _, wb in modes} | {wb for _, wb in layout.DESIGN_TABS}
        for name, wb in available.items():
            if name not in mapped:
                modes.append((str(wb.MenuText).replace('&', ''), name))
        return modes

    def refresh_modes(self):
        available = Gui.listWorkbenches()
        modes = self._modes(available)
        blocker = QtCore.QSignalBlocker(self.selector)
        self.selector.mode_model.replace(modes, available)
        self.selector.setCurrentIndex(next((i for i, (m, _) in enumerate(modes) if m == self.mode), 0))
        del blocker

    def refresh(self):
        if not self.enabled or self.refreshing:
            return
        self.refreshing = True
        try:
            wb = Gui.activeWorkbench()
            name = wb.name()
            available = Gui.listWorkbenches()
            modes = self._modes(available)
            if name != self.workbench:
                design = next((tab for tab, owner in layout.DESIGN_TABS if owner == name), None)
                self.mode = 'Design' if design else next((m for m, w in modes if w == name), 'Design')
                if design:
                    # PartDesign defaults to the specified Modeling tab.
                    self.tab = 'Modeling' if name == 'PartDesignWorkbench' else design
                else:
                    self.tab = 'Home'
                self.workbench = name
            self.refresh_modes()
            customize = Gui.Command.get('Std_DlgCustomize')
            for action in customize.getAction() if customize else ():
                if not action.property('FreeCADPlusObserved'):
                    action.triggered.connect(self.customization_opened)
                    action.setProperty('FreeCADPlusObserved', True)
            self.tabs = list(layout.DESIGN_TABS) if self.mode == 'Design' else [
                ('Home', name), ('Tools', name), ('View', None), ('All Tools', None)]
            while self.tabbar.count():
                self.tabbar.removeTab(0)
            for tab, owner in self.tabs:
                i = self.tabbar.addTab(tab)
                self.tabbar.setTabEnabled(i, owner is None or owner in available)
                if owner and owner not in available:
                    self.tabbar.setTabToolTip(i, 'This workbench is not available in this build.')
            self.tabbar.setCurrentIndex(next((i for i, (t, _) in enumerate(self.tabs) if t == self.tab), 0))
            items = wb.getToolbarItems()
            self.inventory_names = set(items)
            self.native = {bar.objectName(): bar for bar in self.native_bars()}
            self.sources = {}
            for bar_name, bar in self.native.items():
                for action in bar.actions():
                    key = action.data() or action.objectName()
                    if isinstance(key, str) and key != 'Separator':
                        self.sources[key] = (action, bar.widgetForAction(action))
                if not bar.property('FreeCADPlusObserved'):
                    bar.visibilityChanged.connect(lambda visible, b=bar: self.suppress_native(b, visible))
                    bar.setProperty('FreeCADPlusObserved', True)
                if bar.property('FreeCADPlusClassicVisible') is None:
                    bar.setProperty('FreeCADPlusClassicVisible', not bar.isHidden())
                    bar.setProperty('FreeCADPlusClassicAvailable', bar.toggleViewAction().isVisible())
                bar.toggleViewAction().setVisible(False)
                bar.hide()
            self._build_common(items)
            self._build_page(items)
            self.bar.show()
            self.bar.toggleViewAction().setVisible(False)
        finally:
            self.refreshing = False

    def _source(self, command):
        if command in self.sources:
            return self.sources[command]
        native = Gui.Command.get(command)
        if native is not None:
            actions = native.getAction()
            if len(actions) == 1:
                return actions[0], None
        return None

    def _native_control(self, command, parent):
        """Use the original factory for expanded groups and specialized widgets."""
        native = Gui.Command.get(command)
        if native is None:
            return None
        control = QtWidgets.QToolBar(parent)
        control.setObjectName('PlusControl_' + command)
        control.setProperty('PlusCommands', [command])
        control.setMovable(False)
        control.setFloatable(False)
        control.toggleViewAction().setVisible(False)
        native.addToToolbar(control)
        if not control.actions():
            control.deleteLater()
            return None
        return control

    def _spreadsheet_color(self, original, parent):
        import SpreadsheetGui
        control = QtWidgets.QToolBar(parent)
        control.setObjectName('PlusControl_Widget_' + original.objectName())
        control.setMovable(False)
        control.setFloatable(False)
        control.toggleViewAction().setVisible(False)
        SpreadsheetGui.copyColorPicker(original, control)
        copy = control.widgetForAction(control.actions()[0])
        copy.setObjectName('PlusWidget_' + original.objectName())
        return control

    def _button(self, command, parent):
        source = self._source(command)
        if source is None:
            return self._native_control(command, parent)
        action, original = source
        if isinstance(action, QtWidgets.QWidgetAction) and original and original.inherits('QtColorPicker'):
            return self._spreadsheet_color(original, parent)
        native = Gui.Command.get(command)
        expanded = (native is not None and len(native.getAction()) > 1
                    and isinstance(original, QtWidgets.QToolButton) and original.menu() is None)
        if isinstance(action, QtWidgets.QWidgetAction) or expanded:
            # Asking the native factory for a new control preserves live widgets
            # and expanded groups without moving Classic's single-widget actions.
            return self._native_control(command, parent)
        button = QtWidgets.QToolButton(parent)
        button.setObjectName('Plus_' + command)
        button.setProperty('PlusCommands', [command])
        button.setDefaultAction(action)
        button.setAutoRaise(True)
        button.setAccessibleName(action.text().replace('&', ''))
        if isinstance(original, QtWidgets.QToolButton):
            button.setIconSize(original.iconSize())
            button.setPopupMode(original.popupMode())
            if original.menu() is not None:
                button.setMenu(original.menu())
        elif action.menu() is not None:
            button.setMenu(action.menu())
            button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        return button

    def _split(self, commands, caption, parent):
        if len(commands) == 1:
            button = self._button(commands[0], parent)
            if button and commands[0] == 'PartDesign_CompPrimitiveAdditive' and button.menu():
                # Keep the owner-requested unfinished Tab visible without modifying
                # the Classic menu or its native group bookkeeping.
                original = button.menu()
                menu = QtWidgets.QMenu(button)
                menu.addActions(original.actions())
                menu.addSeparator()
                pending = menu.addAction('Tab')
                pending.setEnabled(False)
                pending.setToolTip('Tab is not implemented yet.')
                menu.aboutToShow.connect(original.aboutToShow.emit)
                menu.aboutToHide.connect(original.aboutToHide.emit)
                button.setMenu(menu)
            return button
        actions = [(c, self._source(c)) for c in commands]
        actions = [(c, s[0]) for c, s in actions if s is not None]
        if not actions:
            return None
        key = commands[0]
        selected = preferences().GetString(key, key)
        button = QtWidgets.QToolButton(parent)
        button.setObjectName('Plus_' + key)
        button.setAutoRaise(True)
        button.setAccessibleName(caption)
        menu = QtWidgets.QMenu(button)
        for command, action in actions:
            menu.addAction(action)
        button.setMenu(menu)
        button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        button.setDefaultAction(next((a for c, a in actions if c == selected), actions[0][1]))
        def remember(action):
            # Native actions can acquire a new Python wrapper after workbench
            # recreation. Persist their stable command data, not wrapper identity.
            command = action.data()
            if command in commands:
                preferences().SetString(key, command)
                button.setDefaultAction(action)
        menu.triggered.connect(remember)
        return button

    def _build_common(self, items):
        common = QtWidgets.QWidget()
        row = QtWidgets.QHBoxLayout(common)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(2)
        for name in layout.COMMON:
            for command in items.get(name, ()):
                button = self._button(command, common)
                if button:
                    row.addWidget(button)
            if name == 'File':
                button = self._button('Std_SaveAs', common)
                if button:
                    row.addWidget(button)
            self._divider(row)
        self.top_layout.replaceWidget(self.common, common)
        self.common.deleteLater()
        self.common = common

    @staticmethod
    def _divider(row):
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.VLine)
        divider.setStyleSheet('color: gray;')
        row.addWidget(divider)

    @staticmethod
    def _caption(text, width):
        """Keep complete captions on at most two lines, growing for long words."""
        label = QtWidgets.QLabel()
        label.setObjectName('PlusCaption')
        label.setTextFormat(QtCore.Qt.PlainText)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setAccessibleName(text)
        metrics = label.fontMetrics()
        lines = [text]
        if metrics.horizontalAdvance(text) > width:
            splits = [(text[:i], text[i + 1:]) for i, char in enumerate(text) if char == ' ']
            if splits:
                lines = min(splits, key=lambda pair: max(metrics.horizontalAdvance(t) for t in pair))
        label.setText('\n'.join(lines))
        # Explicit line breaks prevent Qt from squeezing a caption into three or
        # more rows. Its natural minimum width keeps even long words intact.
        return label

    def _group(self, row, title, entries):
        group = QtWidgets.QWidget()
        group.setObjectName('PlusGroup_' + title)
        box = QtWidgets.QVBoxLayout(group)
        box.setContentsMargins(5, 0, 5, 0)
        box.setSpacing(1)
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(2)
        column, slot = 0, 0
        for caption, size, commands in entries:
            if size == 'separator':
                column += 1
                slot = 0
                separator = QtWidgets.QFrame()
                separator.setFrameShape(QtWidgets.QFrame.VLine)
                grid.addWidget(separator, 0, column, 6, 1)
                column += 1
                continue
            button = self._split(commands, caption, group) if commands else None
            if button is None:
                button = QtWidgets.QToolButton(group)
                button.setEnabled(False)
                button.setProperty('PlusUnavailable', list(commands))
                button.setText(caption)
                button.setIcon(Gui.getIcon('forbidden'))
                button.setToolTip(caption + ' is not available in this build.')
                button.setAccessibleName(caption)
            span = {'large': 6, 'medium': 3, 'small': 2}[size]
            if slot + span > 6:
                column += 1
                slot = 0
            if size == 'large':
                cell = QtWidgets.QWidget()
                cell_box = QtWidgets.QVBoxLayout(cell)
                cell_box.setContentsMargins(0, 0, 0, 0)
                cell_box.setSpacing(1)
                button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
                button.setIconSize(QtCore.QSize(32, 32))
                button.setMinimumHeight(55)
                cell_box.addWidget(button)
                label = self._caption(caption, 82)
                label.setMinimumWidth(82)
                cell_box.addWidget(label)
                grid.addWidget(cell, slot, column, span, 1)
            else:
                button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
                pixels = 28 if size == 'medium' else 20
                button.setIconSize(QtCore.QSize(pixels, pixels))
                grid.addWidget(button, slot, column, span, 1)
            slot += span
        box.addLayout(grid)
        box.addStretch()
        label = self._caption(title, grid.minimumSize().width())
        box.addWidget(label)
        row.addWidget(group)
        self._divider(row)

    def _build_page(self, items):
        page = QtWidgets.QWidget()
        row = QtWidgets.QHBoxLayout(page)
        row.setContentsMargins(0, 2, 0, 0)
        row.setSpacing(0)
        if self.mode == 'Design' and self.tab == 'Modeling':
            for title, entries in layout.MODELING:
                self._group(row, title, entries)
        else:
            if self.tab == 'View':
                names = layout.VIEW
            elif self.tab == 'All Tools':
                names = list(items)
            elif self.tab == 'Tools':
                names = [n for n in items if n not in layout.COMMON and n not in layout.VIEW and n != 'Workbench']
            else:
                names = [n for n in items if n not in layout.STANDARD]
                # Home also retains native Structure/Macro/Help access.
                if self.tab == 'Home':
                    names += [n for n in ('Structure', 'Macro', 'Help') if n in items]
            for name in names:
                entries = [(None, 'separator', ()) if c == 'Separator' else
                           (re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', c.split('_', 1)[-1]),
                            'small', (c,)) for c in items.get(name, ())]
                native = self.native.get(name)
                if native:
                    # Spreadsheet appends its native color pickers after command
                    # setup. They have no command ID and are absent from items.
                    for index, action in enumerate(native.actions()):
                        if isinstance(action, QtWidgets.QWidgetAction) and not action.data():
                            original = native.widgetForAction(action)
                            key = '__widget_%s_%d' % (name, index)
                            self.sources[key] = (action, original)
                            entries.append((original.toolTip(), 'small', (key,)))
                if entries or self.tab == 'All Tools':
                    self._group(row, native.windowTitle() if native else name, entries)
        row.addStretch()
        old = self.scroll.takeWidget()
        self.scroll.setWidget(page)
        # Reserve the horizontal scrollbar without clipping the bottom captions.
        height = page.minimumSizeHint().height() + self.scroll.horizontalScrollBar().sizeHint().height()
        self.scroll.setMinimumHeight(max(137, height))
        if old:
            old.deleteLater()


def apply(mode):
    global _controller
    if _controller is None:
        if mode != 'Plus':
            return
        _controller = Ribbon(Gui.getMainWindow())
    _controller.apply(mode == 'Plus')
