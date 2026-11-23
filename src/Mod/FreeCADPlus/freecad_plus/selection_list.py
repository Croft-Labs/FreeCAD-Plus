# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native profile collector with five complete rows at any current font/DPI."""
from PySide6 import QtCore, QtWidgets


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
            QtCore.QTimer.singleShot(0, self.resize_rows)
