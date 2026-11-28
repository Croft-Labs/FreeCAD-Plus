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
             'Click a body, surface or sketch in a direct child component.')
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
        self.join=None
        if extract:
            note('To extract a child component’s face, first clone its whole object into '+definition.Label+'.')
            self.join=QtWidgets.QCheckBox('Join surfaces')
            self.join.setChecked(bool(getattr(feature,'JoinSurfaces',False)) if feature else True)
            layout.addWidget(self.join)
            self.join.setToolTip('Create one surface from faces connected by shared edges. Clear to create a separate History result for each face.')
            self.join_hint=note('')
            self.join.toggled.connect(self.update_join_hint)
            self.update_join_hint()
        else:
            note('Clicking a face or edge selects its whole source object. Use Extract geometry for individual faces.')
            note('Source construction history stays in the child. Parent features can modify the cloned result or combine it with a parent body.')
        group=QtWidgets.QGroupBox('Preview');self.preview_layout=QtWidgets.QVBoxLayout(group);layout.addWidget(group)
        self.preview=QtWidgets.QCheckBox('Show preview');self.preview.setChecked(True);self.preview_layout.addWidget(self.preview)
        self.update=QtWidgets.QCheckBox('Recompute on update');self.update.setChecked(True);self.preview_layout.addWidget(self.update)
        self.update.setToolTip('Automatically refresh the preview. Saved results always retain their source association.')
        note('Updates from the selected faces on the parent-owned object.' if extract else
             'Updates from the source in the parent coordinate system.')
        self.status=TaskStatus();layout.addWidget(self.status)
        self.summary=note('');layout.addStretch()

    def update_join_hint(self,*args):
        self.join_hint.setText('Creates one extracted surface. Selected faces must form a connected set sharing edges.' if self.join.isChecked() else
                              'Creates one extracted surface per face, each with its own History entry. Faces do not need to touch.')
