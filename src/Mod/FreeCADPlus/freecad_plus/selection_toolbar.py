# SPDX-License-Identifier: LGPL-2.1-or-later
"""Plus Design selection controls; native tools own picking and geometry."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets


def preferences():
    return App.ParamGet('User parameter:BaseApp/Preferences/FreeCADPlus/Selection')


def apply(active):
    # None removes the transient property, restoring native Classic behavior.
    value = preferences().GetBool('Directional', True) if active else None
    Gui.getMainWindow().setProperty('FreeCADPlusDirectionalSelection', value)


def append_controls(row, active):
    apply(active)
    if not active:
        return
    label = QtWidgets.QLabel('Selection')
    label.setObjectName('PlusSelectionLabel')
    row.addWidget(label)
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
