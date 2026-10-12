# SPDX-License-Identifier: LGPL-2.1-or-later
"""Plus Design selection controls; native tools own picking and geometry."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtWidgets
from . import curve_selection, category_selection


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
                          'Horizontal/Vertical, Parallel, Coincident, Point on Object,\n'
                          'Block and Symmetry. Other operations are not yet integrated.')

    def persistence_changed(checked):
        preferences().SetBool('Persistent', checked)
        apply(True)

    persistent.toggled.connect(persistence_changed)
    row.addWidget(persistent)


def append_curve_intent(row):
    button = QtWidgets.QToolButton()
    button.setObjectName('PlusCurveIntent')
    button.setAccessibleName('Curve intent')
    button.setAutoRaise(True)
    button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
    button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
    menu = QtWidgets.QMenu(button)
    group = QtGui.QActionGroup(button)
    group.setExclusive(True)
    for label, icon in zip(curve_selection.INTENTS,
                           ('edge-selection', 'Sketcher_CreatePolyline', 'Constraint_Tangent')):
        action = QtGui.QAction(Gui.getIcon(icon), label, button)
        action.setCheckable(True)
        action.setToolTip(label)
        group.addAction(action)
        menu.addAction(action)
        def choose(checked=False, action=action, label=label):
            preferences().SetString('CurveIntent', label)
            action.setChecked(True)
            button.setDefaultAction(action)
        action.triggered.connect(choose)
        if label == curve_selection.intent():
            action.setChecked(True)
            button.setDefaultAction(action)
    button.setMenu(menu)
    row.addWidget(button)
