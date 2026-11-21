# SPDX-License-Identifier: LGPL-2.1-or-later
"""Commit ordinary Qt numeric editors on focus leave throughout the application.

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
            widget.setKeyboardTracking(False)
            widget.setProperty('_plusCommitInitial', widget.value())
            widget.setProperty('_plusCommitWasBlocked', widget.signalsBlocked())
            widget.setProperty('_plusCommitActive', True)
            widget.blockSignals(True)
        elif event.type() == QtCore.QEvent.FocusOut and widget.property('_plusCommitActive'):
            widget.interpretText()
            initial, value = widget.property('_plusCommitInitial'), widget.value()
            was_blocked = bool(widget.property('_plusCommitWasBlocked'))
            widget.setProperty('_plusCommitActive', False)
            widget.blockSignals(was_blocked)
            if value != initial and not was_blocked:
                widget.valueChanged.emit(value)
        return False


def install():
    global _filter
    if _filter is None:
        app = QtWidgets.QApplication.instance()
        _filter = NumericCommitFilter(app)
        app.installEventFilter(_filter)
