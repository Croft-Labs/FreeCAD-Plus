# SPDX-License-Identifier: LGPL-2.1-or-later
"""Defer typed numeric input; native spin steps publish immediately.

Native unit-aware InputField/QuantitySpinBox implement the same rule in C++.
Keep text editing and validation native; defer only the public value notification.
"""
from PySide6 import QtCore, QtWidgets

_filter = None


class NumericCommitFilter(QtCore.QObject):
    def eventFilter(self, widget, event):
        ordinary = isinstance(widget, (QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox))
        numeric = ordinary or (isinstance(widget, QtWidgets.QWidget) and
                               (widget.inherits('Gui::QuantitySpinBox') or widget.inherits('Gui::InputField')))
        if not numeric:
            return False
        if isinstance(widget, QtWidgets.QDoubleSpinBox) and event.type() in (QtCore.QEvent.Polish, QtCore.QEvent.FocusIn):
            if widget.decimals() < 6:
                widget.setDecimals(6)
        if event.type() == QtCore.QEvent.KeyPress and event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            dialog = widget.window()
            if (isinstance(dialog, QtWidgets.QDialog)
                    and dialog.objectName() in ('SketcherGui__InsertDatum', 'SketcherGui::InsertDatum')
                    and widget.objectName() == 'labelEdit'):
                # Validate before blur: native focus-out restores the last valid
                # value for invalid text, which must not silently accept it.
                if event.isAutoRepeat() or not widget.property('acceptableInput'):
                    return True
                box = dialog.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
                button = box.button(QtWidgets.QDialogButtonBox.Ok) if box else None
                if button and button.isVisible() and button.isEnabled():
                    widget.focusNextChild()  # Publish the native pending quantity first.
                    button.click()          # Retain native validation and transaction handling.
                return True
            widget.focusNextChild()
            return True
        if not ordinary:
            return False
        if event.type() == QtCore.QEvent.FocusIn:
            # Qt already distinguishes text editing from explicit spin steps.
            # Blocking all signals here also blocked arrow clicks and autorepeat.
            widget.setKeyboardTracking(False)
        return False


def install():
    global _filter
    if _filter is None:
        app = QtWidgets.QApplication.instance()
        _filter = NumericCommitFilter(app)
        app.installEventFilter(_filter)
