# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native profile collector with five complete rows at any current font/DPI."""
from contextlib import contextmanager
from PySide6 import QtCore, QtWidgets


# Shared with native TaskDressUpParameters. An override carries the original
# gesture across delayed chain expansion even after the user releases Shift.
_INTENT = 'FreeCADPlusSelectionRemove'


def reference_key(ref):
    """Compare native mapped and ordinary element names without dropping saved maps."""
    import Part
    obj, sub = ref
    return obj, Part.splitSubname(sub)[2]


def removing():
    app = QtWidgets.QApplication.instance()
    value = app.property(_INTENT)
    return bool(QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ShiftModifier) if value is None else bool(value)


@contextmanager
def pick_intent(remove):
    app = QtWidgets.QApplication.instance()
    previous = app.property(_INTENT)
    app.setProperty(_INTENT, bool(remove))
    try:
        yield
    finally:
        app.setProperty(_INTENT, previous)


def feature_picker_active():
    """Only feature collectors own History clicks; ordinary trees stay native."""
    import FreeCADGui as Gui
    from . import extrude_task, plane_task, sketch_task, clone_task, appearance_task
    if any(task is not None and not task.closed for task in
           (extrude_task._active, plane_task._active, sketch_task._active, clone_task._active, appearance_task._active)):
        return True
    # Native component dress-up collectors expose this control only in Plus docs.
    return any(widget.isVisible() for widget in
               Gui.getMainWindow().findChildren(QtWidgets.QPushButton, 'clearReferences'))


class SelectionList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerItem)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.horizontalScrollBar().rangeChanged.connect(self.resize_rows)
        self.model().rowsInserted.connect(self.resize_rows)
        self.model().rowsRemoved.connect(self.resize_rows)
        self.resize_rows()

    def resize_rows(self, *args):
        height = max(self.sizeHintForRow(0), self.fontMetrics().height() + 4)
        scroll = self.style().pixelMetric(QtWidgets.QStyle.PixelMetric.PM_ScrollBarExtent)
        self.setFixedHeight(5 * height + 2 * self.frameWidth() +
                            (scroll if self.horizontalScrollBar().maximum() else 0))
        for i in range(self.count()):
            self.item(i).setToolTip(self.item(i).text())

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QtCore.QEvent.FontChange, QtCore.QEvent.StyleChange):
            QtCore.QTimer.singleShot(0, self, self.resize_rows)
