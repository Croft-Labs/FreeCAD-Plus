# SPDX-License-Identifier: LGPL-2.1-or-later
"""Plus Design selection controls; native tools own picking and geometry."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtWidgets
from . import curve_selection, category_selection, selection_scope, surface_selection

_watcher = None


class ScopeWatcher(QtCore.QObject):
    def __init__(self):
        super().__init__(Gui.getMainWindow())
        self.buttons = []
        self.timer = QtCore.QTimer(self);self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.refresh)
        QtWidgets.QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.DynamicPropertyChange:
            if bytes(event.propertyName()) == b'FreeCADPlusPickDomain':self.refresh()
        elif event.type() in (QtCore.QEvent.Show, QtCore.QEvent.Hide, QtCore.QEvent.FocusIn, QtCore.QEvent.MouseButtonRelease):
            if not self.timer.isActive():self.timer.start(0)
        return False

    def refresh(self):
        domain, _ = selection_scope.current()
        for button in tuple(self.buttons):
            try:
                rebuild_intent(button, domain)
            except RuntimeError:
                self.buttons.remove(button)


def rebuild_intent(button, domain):
    source = surface_selection if domain == 'surface' else curve_selection
    current = source.intent()
    if button.property('selectionDomain') == domain:
        for action in button.menu().actions():
            action.setChecked(action.text() == current)
            if action.isChecked():button.setIcon(action.icon())
        button.setText(current);button.setToolTip(current)
        return
    button.setProperty('selectionDomain', domain)
    button.setAccessibleName('Surface intent' if domain == 'surface' else 'Curve intent')
    old = button.menu()
    menu = QtWidgets.QMenu(button)
    group = QtGui.QActionGroup(menu);group.setExclusive(True)
    icons = ('face-selection', 'PartDesign_SubShapeBinder', 'Constraint_Tangent') if domain == 'surface' else (
        'edge-selection', 'Sketcher_CreatePolyline', 'Constraint_Tangent')
    for label, icon in zip(source.INTENTS, icons):
        action = QtGui.QAction(Gui.getIcon(icon), label, menu)
        action.setCheckable(True);group.addAction(action);menu.addAction(action)
        def choose(checked=False, action=action, label=label):
            preferences().SetString('SurfaceIntent' if domain == 'surface' else 'CurveIntent', label)
            action.setChecked(True);button.setText(label);button.setIcon(action.icon());button.setToolTip(label)
        action.triggered.connect(choose)
        if label == current:
            action.setChecked(True);button.setText(label);button.setIcon(action.icon());button.setToolTip(label)
    button.setMenu(menu)
    if old is not None:old.deleteLater()


def preferences():
    return App.ParamGet('User parameter:BaseApp/Preferences/FreeCADPlus/Selection')


def apply(active):
    curve_selection.apply(active)
    category_selection.apply(active)
    # None removes the transient property, restoring native Classic behavior.
    value = preferences().GetBool('Directional', True) if active else None
    Gui.getMainWindow().setProperty('FreeCADPlusDirectionalSelection', value)
    persistent = preferences().GetBool('Persistent', True) if active else None
    Gui.getMainWindow().setProperty('FreeCADPlusPersistentSelection', persistent)


def append_controls(row, active):
    apply(active)
    if not active:
        return
    label = QtWidgets.QLabel('Selection')
    label.setObjectName('PlusSelectionLabel')
    row.addWidget(label)
    append_curve_intent(row)
    category_selection.append_controls(row)
    button = QtWidgets.QToolButton()
    button.setObjectName('PlusDirectionalSelection')
    button.setAccessibleName('Directional Selection')
    button.setText('Directional Selection')
    button.setIcon(Gui.getIcon('edit-select-box'))
    button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
    button.setAutoRaise(True)
    button.setCheckable(True)
    button.setChecked(preferences().GetBool('Directional', True))
    button.setToolTip('Directional Selection\nOn: left-to-right encloses; right-to-left crosses.\n'
                      'Off: both directions require full enclosure.')

    def changed(checked):
        preferences().SetBool('Directional', checked)
        apply(True)

    button.toggled.connect(changed)
    row.addWidget(button)
    persistent = QtWidgets.QToolButton()
    persistent.setObjectName('PlusPersistentSelection')
    persistent.setAccessibleName('Persistent Selection')
    persistent.setText('Persistent Selection')
    persistent.setIcon(Gui.getIcon('edit-select-all'))
    persistent.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
    persistent.setAutoRaise(True)
    persistent.setCheckable(True)
    persistent.setChecked(preferences().GetBool('Persistent', True))
    persistent.setToolTip('Persistent Selection\nKeep sketch selection after Construction, Equal,\n'
                          'Horizontal/Vertical, Parallel, Tangent, Perpendicular,\n'
                          'Coincident, Point on Object, Block, Symmetry and\n'
                          'preselected dimensions (including contextual Dimension).\n'
                          'Also keep inputs after Refraction, constraint state toggles,\n'
                          'and B-spline degree increase. Keep surviving geometry after\n'
                          'Delete All Constraints.\n'
                          'Continuous dimension tools and other operations retain native cleanup.')

    def persistence_changed(checked):
        preferences().SetBool('Persistent', checked)
        apply(True)

    persistent.toggled.connect(persistence_changed)
    row.addWidget(persistent)


def append_curve_intent(row):
    global _watcher
    button = QtWidgets.QToolButton()
    button.setObjectName('PlusCurveIntent')
    button.setAccessibleName('Curve intent')
    button.setAutoRaise(True)
    button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
    if _watcher is None:_watcher = ScopeWatcher()
    _watcher.buttons.append(button)
    rebuild_intent(button, selection_scope.current()[0])
    row.addWidget(button)
