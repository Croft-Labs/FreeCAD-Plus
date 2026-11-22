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
        if event.type() == QtCore.QEvent.KeyPress and event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
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
