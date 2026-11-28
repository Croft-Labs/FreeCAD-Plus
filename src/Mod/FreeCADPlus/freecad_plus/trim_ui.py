from PySide6 import QtCore, QtWidgets
from .task_status import TaskStatus
from .quantity_fields import QuantityNumber

# SPDX-License-Identifier: LGPL-2.1-or-later

class Form(QtWidgets.QGroupBox):
    def __init__(self,owner):
        super().__init__('Trim Body')
        self.setAutoFillBackground(True); self.setMinimumWidth(460)
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(14,18,14,14); root.setSpacing(12)
        def label(text, layout=root):
            item = QtWidgets.QLabel(text); item.setWordWrap(True); layout.addWidget(item)
            return item
        label('Editing component: '+owner.Label)
        label('Target body')
        row = QtWidgets.QHBoxLayout()
        self.target = QtWidgets.QLineEdit(); self.target.setReadOnly(True)
        self.target.setPlaceholderText('Click here, then pick a body')
        self.clear_target = QtWidgets.QPushButton('Clear')
        row.addWidget(self.target,1);row.addWidget(self.clear_target);root.addLayout(row)
        label('A face or edge pick selects its whole body.')
        row = QtWidgets.QHBoxLayout(); row.addWidget(QtWidgets.QLabel('Trimming tool'))
        self.mode = QtWidgets.QComboBox();self.mode.addItems(['Surfaces','Plane'])
        row.addWidget(self.mode,1);root.addLayout(row)
        self.surface_group = QtWidgets.QWidget();surface_layout = QtWidgets.QVBoxLayout(self.surface_group)
        surface_layout.setContentsMargins(0,0,0,0);surface_layout.setSpacing(9)
        self.surfaces = QtWidgets.QListWidget();self.surfaces.setMinimumHeight(135)
        self.surfaces.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        surface_layout.addWidget(self.surfaces)
        row = QtWidgets.QHBoxLayout()
        self.remove = QtWidgets.QPushButton('Remove selected');self.clear = QtWidgets.QPushButton('Clear surfaces')
        row.addWidget(self.remove);row.addWidget(self.clear);surface_layout.addLayout(row)
        label('Click the list to pick surfaces. Click adds; Shift-click removes.',surface_layout)
        label('Surfaces form one boundary and must extend past the body. A boundary ending inside the body is invalid.',surface_layout)
        root.addWidget(self.surface_group)
        self.plane_group = QtWidgets.QWidget();plane_layout = QtWidgets.QFormLayout(self.plane_group)
        plane_layout.setContentsMargins(0,0,0,0)
        self.plane = QtWidgets.QComboBox();self.plane.addItems(['XY plane','XZ plane','YZ plane','Selected datum plane'])
        self.reference = QtWidgets.QLineEdit();self.reference.setReadOnly(True)
        self.reference.setPlaceholderText('Click here, then pick a created plane')
        plane_layout.addRow('Plane',self.plane);plane_layout.addRow('Reference',self.reference)
        plane_note = QtWidgets.QLabel('Planes extend infinitely; their displayed rectangle does not limit the trim.')
        plane_note.setWordWrap(True);plane_layout.addRow(plane_note);root.addWidget(self.plane_group)
        row = QtWidgets.QFormLayout()
        self.offset = QuantityNumber();self.offset.setRange(-100000,100000);self.offset.setDecimals(2)
        self.offset.setSuffix(' mm');row.addRow('Offset',self.offset);root.addLayout(row)
        label('Positive offset follows the tool normal shown in the view.')
        self.reverse = QtWidgets.QCheckBox('Reverse — switch side to remove');root.addWidget(self.reverse)
        self.side = label('Remove the side indicated by the arrow.');self.reverse.toggled.connect(self.change_side)
        self.preview = QtWidgets.QCheckBox('Preview trim');self.preview.setChecked(True);root.addWidget(self.preview)
        label('Red translucent material will be removed. The retained body keeps its appearance.')
        self.status = TaskStatus('Select a target body and trimming surfaces.');root.addWidget(self.status)
        row = QtWidgets.QHBoxLayout()
        self.done=QtWidgets.QPushButton('Done');self.apply=QtWidgets.QPushButton('Apply');self.cancel=QtWidgets.QPushButton('Cancel')
        for button in (self.done,self.apply,self.cancel):row.addWidget(button)
        root.addLayout(row)
        self.mode.currentIndexChanged.connect(self.change_mode)
        self.plane.currentIndexChanged.connect(self.sync)
        self.target.textChanged.connect(self.sync);self.reference.textChanged.connect(self.sync)
        self.surfaces.model().rowsInserted.connect(self.sync);self.surfaces.model().rowsRemoved.connect(self.sync)
        self.surfaces.model().modelReset.connect(self.sync);self.surfaces.itemSelectionChanged.connect(self.sync)
        self.closed=None;self.valid_example=True;self.change_mode()

    def change_mode(self,*args):
        surfaces=self.mode.currentIndex()==0
        self.surface_group.setVisible(surfaces);self.plane_group.setVisible(not surfaces)
        self.sync();self.adjustSize()

    def sync(self,*args):
        if not hasattr(self,'valid_example'):return
        selected=self.plane.currentIndex()==3;self.reference.setEnabled(selected)
        tools=self.surfaces.count()>0 if self.mode.currentIndex()==0 else (not selected or bool(self.reference.text()))
        ready=bool(self.target.text()) and tools
        self.apply.setEnabled(ready and self.valid_example)
        self.done.setEnabled(self.valid_example)
        self.remove.setEnabled(bool(self.surfaces.selectedItems()));self.clear.setEnabled(self.surfaces.count()>0)
        if self.valid_example:self.status.setText('Ready. One linked Trim Body feature.' if ready else 'Select a target body and trimming tools.')

    def change_side(self,checked):
        self.side.setText('Remove the opposite side. Offset is unchanged.' if checked else 'Remove the side indicated by the arrow.')

    def add_surface(self,name,remove=False):
        matches=self.surfaces.findItems(name,QtCore.Qt.MatchExactly)
        if remove:
            for item in matches:self.surfaces.takeItem(self.surfaces.row(item))
        elif not matches:self.surfaces.addItem(name)
        self.sync()
    def remove_selected(self):
        for item in self.surfaces.selectedItems():self.surfaces.takeItem(self.surfaces.row(item))

    def invalid_example(self):
        self.valid_example=False
        self.status.setError('Trim invalid: the tool boundary ends inside the target body. Extend or replace the surfaces so the combined boundary passes completely through the body.')
        self.sync()

    def reset(self):
        self.valid_example=True;self.target.clear();self.surfaces.clear();self.mode.setCurrentIndex(0)
        self.plane.setCurrentIndex(0);self.reference.clear();self.offset.setSuffix(' mm');self.offset.setValue(0)
        self.reverse.setChecked(False);self.preview.setChecked(True);self.sync()
