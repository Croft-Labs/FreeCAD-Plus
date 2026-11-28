# SPDX-License-Identifier: LGPL-2.1-or-later
"""Approved whole-shape transformation controls."""
from PySide6 import QtCore, QtWidgets
from .task_status import TaskStatus
from .selection_list import SelectionList
from .quantity_fields import QuantityNumber

KINDS=('Mirror','Linear pattern','Polar pattern','Multi-transform')

def label(text):
    item=QtWidgets.QLabel(text);item.setWordWrap(True);return item

def combo(values):
    item=QtWidgets.QComboBox();item.addItems(values);return item

def number(value,suffix='',minimum=-100000,maximum=100000,decimals=2):
    item=QuantityNumber() if suffix.strip()=='mm' else QtWidgets.QDoubleSpinBox()
    item.setDecimals(decimals);item.setRange(minimum,maximum)
    item.setSuffix(suffix);item.setValue(value);return item

class Step(QtWidgets.QGroupBox):
    def __init__(self,kind):
        super().__init__(kind+' settings');self.kind=kind
        layout=QtWidgets.QFormLayout(self);layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.reference=combo(['XY plane','XZ plane','YZ plane','Selected plane / planar face'] if kind=='Mirror' else
                             ['X axis','Y axis','Z axis','Selected straight edge / axis'])
        if kind=='Mirror':self.reference.setCurrentIndex(2)
        elif kind=='Polar pattern':self.reference.setCurrentIndex(2)
        layout.addRow('Mirror plane' if kind=='Mirror' else ('Direction' if kind=='Linear pattern' else 'Rotation axis'),self.reference)
        self.pick=QtWidgets.QLineEdit();self.pick.setReadOnly(True);self.pick.setPlaceholderText('Click here, then pick in the view')
        self.pick.setEnabled(False);layout.addRow('Reference',self.pick)
        self.reference.currentIndexChanged.connect(lambda i:self.pick.setEnabled(i==3))
        if kind=='Mirror':
            self.offset=number(30,' mm');layout.addRow('Plane offset',self.offset)
            layout.addRow(label('Includes the original and its mirrored copy.'))
        else:
            self.count=QtWidgets.QSpinBox();self.count.setRange(2,10000);self.count.setValue(3 if kind=='Linear pattern' else 6)
            layout.addRow('Occurrences',self.count)
            layout.addRow(label('Count includes the original.'))
            self.measure=combo(['Spacing','Overall length'] if kind=='Linear pattern' else ['Total angle','Angle between copies'])
            self.value=number(22 if kind=='Linear pattern' else 360,' mm' if kind=='Linear pattern' else '°',.01,100000 if kind=='Linear pattern' else 360)
            layout.addRow(self.measure,self.value)
            if kind=='Polar pattern':
                self.center=[]
                for axis in 'XYZ':
                    spin=number(0,' mm');layout.addRow('Axis origin '+axis,spin);self.center.append(spin)
                self.center_hint=label('Origin applies to component axes. A picked axis supplies its own position.')
                layout.addRow(self.center_hint)
                self.reference.currentIndexChanged.connect(lambda i:[spin.setEnabled(i!=3) for spin in self.center])
                layout.addRow(label('A full circle places each copy once.'))
            self.reverse=QtWidgets.QCheckBox('Reverse direction');layout.addRow(self.reverse)
        layout.addRow(label('References and distances use the active component.'))

    def length_fields(self):
        if self.kind=='Mirror':return {'offset':self.offset}
        if self.kind=='Linear pattern':return {'value':self.value}
        return dict(zip(('center_x','center_y','center_z'),self.center))

    def reset(self):
        for field in self.length_fields().values():field.setSuffix(' mm')
        self.reference.setCurrentIndex(0 if self.kind=='Mirror' else (2 if self.kind=='Polar pattern' else 0));self.pick.clear()
        if self.kind=='Mirror':self.offset.setValue(0)
        else:
            self.count.setValue(2);self.value.setValue(10 if self.kind=='Linear pattern' else 360)
            self.measure.setCurrentIndex(0);self.reverse.setChecked(False)
            if self.kind=='Polar pattern':
                for spin in self.center:spin.setValue(0)

class Form(QtWidgets.QGroupBox):
    def __init__(self,kind,owner):
        super().__init__();self.kind=kind;self.setWindowTitle(kind);self.setMinimumWidth(490);self.setAutoFillBackground(True)
        layout=QtWidgets.QVBoxLayout(self);layout.setContentsMargins(8,8,8,8);layout.setSpacing(7)
        title=label('Editing component: '+owner.Label);font=title.font();font.setBold(True);title.setFont(font);layout.addWidget(title)
        layout.addWidget(label('Select a body or sheet. A face or edge click selects its whole object.'))
        self.objects=SelectionList();self.objects.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.objects.setFixedHeight(100);self.objects.addItem('Organizer body  ·  finished shape')
        layout.addWidget(self.objects)
        buttons=QtWidgets.QHBoxLayout();self.remove=QtWidgets.QPushButton('Remove');self.clear=QtWidgets.QPushButton('Clear')
        buttons.addWidget(self.remove);buttons.addWidget(self.clear);buttons.addStretch();layout.addLayout(buttons)
        layout.addWidget(label('Click adds · Shift-click removes. The complete shape includes all prior cuts.'))
        self.steps=[]
        if kind=='Multi-transform':
            group=QtWidgets.QGroupBox('Transformations — applied in order');vertical=QtWidgets.QVBoxLayout(group)
            self.order=QtWidgets.QListWidget();self.order.setFixedHeight(75);vertical.addWidget(self.order)
            buttons=QtWidgets.QHBoxLayout();self.add=QtWidgets.QToolButton();self.add.setText('Add');self.add.setMinimumWidth(70);self.add.setPopupMode(QtWidgets.QToolButton.InstantPopup)
            menu=QtWidgets.QMenu(self.add)
            for name in KINDS[:3]:menu.addAction(name,lambda name=name:self.add_step(name))
            self.add.setMenu(menu);buttons.addWidget(self.add)
            self.delete=QtWidgets.QPushButton('Remove');self.up=QtWidgets.QPushButton('Up');self.down=QtWidgets.QPushButton('Down')
            for button in (self.delete,self.up,self.down):buttons.addWidget(button)
            vertical.addLayout(buttons);layout.addWidget(group)
            self.stack=QtWidgets.QStackedWidget();layout.addWidget(self.stack)
            self.order.currentRowChanged.connect(self.stack.setCurrentIndex)
            self.delete.clicked.connect(self.remove_step);self.up.clicked.connect(lambda:self.move_step(-1));self.down.clicked.connect(lambda:self.move_step(1))
        else:
            step=Step(kind);step.reset();self.steps.append(step);layout.addWidget(step)
        result=QtWidgets.QGroupBox('Result');form=QtWidgets.QVBoxLayout(result)
        self.merge=QtWidgets.QCheckBox('Merge into one result');self.merge.setChecked(True);form.addWidget(self.merge)
        self.hint=label('Touching copies fuse. Separated copies stay together in one body or sheet object.');form.addWidget(self.hint)
        self.merge.toggled.connect(lambda yes:self.hint.setText('Touching copies fuse. Separated copies stay together in one body or sheet object.' if yes else 'Create separate bodies or sheet objects for the copies.'))
        form.addWidget(label('Keeps an editable link to the complete source shape.'))
        layout.addWidget(result)
        group=QtWidgets.QGroupBox('Preview');self.preview_layout=QtWidgets.QVBoxLayout(group);layout.addWidget(group)
        self.preview=QtWidgets.QCheckBox('Show preview');self.preview.setChecked(True);self.preview_layout.addWidget(self.preview)
        self.status=TaskStatus('Ready. One editable History result.');layout.addWidget(self.status)
        footer=QtWidgets.QHBoxLayout();self.done=QtWidgets.QPushButton('Done');self.apply=QtWidgets.QPushButton('Apply');self.cancel=QtWidgets.QPushButton('Cancel')
        for button in (self.done,self.apply,self.cancel):footer.addWidget(button)
        layout.addLayout(footer);layout.addStretch()
    def add_step(self,kind):
        step=Step(kind);step.reset();self.steps.append(step);self.stack.addWidget(step);self.order.addItem(kind);self.order.setCurrentRow(self.order.count()-1)

    def remove_step(self):
        index=self.order.currentRow()
        if index<0:return
        step=self.steps.pop(index);self.stack.removeWidget(step);step.deleteLater();self.order.takeItem(index)

    def move_step(self,delta):
        index=self.order.currentRow();dest=index+delta
        if index<0 or dest<0 or dest>=len(self.steps):return
        item=self.order.takeItem(index);self.order.insertItem(dest,item)
        step=self.steps.pop(index);self.steps.insert(dest,step);self.stack.removeWidget(step);self.stack.insertWidget(dest,step);self.order.setCurrentRow(dest)

    def reset(self):
        self.objects.clear();self.merge.setChecked(True);self.preview.setChecked(True)
        if self.kind=='Multi-transform':
            while self.order.count():self.order.setCurrentRow(0);self.remove_step()
        else:self.steps[0].reset()
        self.status.setText('Select geometry for the next result.')
