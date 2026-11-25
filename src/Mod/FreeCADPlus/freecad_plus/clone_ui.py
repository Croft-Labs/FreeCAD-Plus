# SPDX-License-Identifier: LGPL-2.1-or-later
"""Shared native Clone/Extract creation and editing form."""
from PySide6 import QtCore, QtWidgets
from .task_status import TaskStatus


class SourceList(QtWidgets.QTreeWidget):
    activated = QtCore.Signal()
    removeRequested = QtCore.Signal()
    def __init__(self):
        super().__init__()
        self.setColumnCount(2); self.setRootIsDecorated(False)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.header().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
        self.setMinimumHeight(5 * (self.fontMetrics().height()+8) + self.header().sizeHint().height()+6)
        self.setMaximumHeight(self.minimumHeight()+30)
        self.setToolTip('Click the list to pick. Click adds; Shift-click removes. Delete removes selected inputs.')
    def mousePressEvent(self,event):
        self.activated.emit(); super().mousePressEvent(event)
    def keyPressEvent(self,event):
        if event.key() in (QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace):
            self.removeRequested.emit(); event.accept()
        else: super().keyPressEvent(event)


class GeometryForm(QtWidgets.QGroupBox):
    def __init__(self,definition,extract=False,feature=None):
        super().__init__()
        self.setWindowTitle('Extract geometry' if extract else 'Clone')
        layout=QtWidgets.QVBoxLayout(self); layout.setContentsMargins(6,6,6,6)
        def note(text,bold=False):
            label=QtWidgets.QLabel(text); label.setWordWrap(True); label.setTextFormat(QtCore.Qt.PlainText)
            if bold:
                font=label.font();font.setBold(True);label.setFont(font)
            layout.addWidget(label);return label
        note('Editing component: '+definition.Label,True)
        if feature: note('Editing: '+feature.Label)
        note('Select faces on an object owned by '+definition.Label+'.' if extract else
             'Select whole objects from direct child components.')
        header=QtWidgets.QHBoxLayout();header.addWidget(QtWidgets.QLabel('Faces' if extract else 'Whole objects'));header.addStretch()
        self.browse=None
        if not extract:
            self.browse=QtWidgets.QPushButton('Browse direct children…');header.addWidget(self.browse)
        layout.addLayout(header)
        self.objects=SourceList()
        self.objects.setHeaderLabels(['Source face' if extract else 'Source object','Result name'])
        layout.addWidget(self.objects)
        actions=QtWidgets.QHBoxLayout();self.remove=QtWidgets.QPushButton('Remove');self.clear=QtWidgets.QPushButton('Clear')
        actions.addWidget(self.remove);actions.addWidget(self.clear);actions.addStretch();layout.addLayout(actions)
        if extract:
            note('To extract a child component’s face, first clone its whole object into '+definition.Label+'.')
            note('Creates a separate extracted surface. The cloned body remains available.')
        else:
            note('Bodies, surfaces, sketches and planes are cloned as complete objects. Faces, edges and vertices are not Clone inputs.')
            note('Source construction history stays in the child. Parent features can modify the cloned result or combine it with a parent body.')
        self.preview=QtWidgets.QCheckBox('Show preview');self.preview.setChecked(True);layout.addWidget(self.preview)
        self.update=QtWidgets.QCheckBox('Recompute on update');self.update.setChecked(True);layout.addWidget(self.update)
        self.update.setToolTip('Automatically refresh the preview. Saved results always retain their source association.')
        note('Updates from the selected faces on the parent-owned object.' if extract else
             'Updates from the source in the parent coordinate system.')
        self.status=TaskStatus();layout.addWidget(self.status)
        self.summary=note('');layout.addStretch()
