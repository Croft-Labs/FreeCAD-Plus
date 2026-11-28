# SPDX-License-Identifier: LGPL-2.1-or-later
from PySide6 import QtCore, QtWidgets
from freecad_plus import sketch_pattern as pattern
from freecad_plus.task_status import TaskStatus
from freecad_plus.quantity_fields import QuantityNumber


def combo(items):
    w=QtWidgets.QComboBox(); w.addItems(items); w.setMinimumContentsLength(8); w.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon); w.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Fixed); return w
def count(value):
    w=QtWidgets.QSpinBox(); w.setRange(2,999); w.setValue(value); w.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Fixed); return w
def amount(value, angular=False):
    w=QuantityNumber(); w.setRange(.000001,360 if angular else 100000)
    w.setSuffix('deg' if angular else 'mm'); w.setValue(value); w.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Fixed); return w
def reference(text):
    w=QtWidgets.QLineEdit(); w.setReadOnly(True); w.setPlaceholderText(text); w.setClearButtonEnabled(True); w.setMinimumWidth(0); w.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Fixed); return w

class Extent(QtWidgets.QGroupBox):
    def __init__(self,title,owner,kind='linear'):
        super().__init__(title); self.owner=owner; self.kind=kind; self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Maximum)
        layout=QtWidgets.QVBoxLayout(self); layout.setSpacing(5); layout.setContentsMargins(8,10,8,8)
        self.reference=None
        if kind=='linear':
            row=QtWidgets.QVBoxLayout(); self.method=combo(['Axis or line','Two points','Vector'])
            row.addWidget(self.method)
            self.picks=QtWidgets.QStackedWidget(); self.picks.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Preferred); row.addWidget(self.picks)
            self.reference=reference('Select an axis or straight line'); self.picks.addWidget(self.reference)
            points=QtWidgets.QWidget(); pts=QtWidgets.QVBoxLayout(points); pts.setSpacing(4); pts.setContentsMargins(0,0,0,0)
            self.start=reference('From point'); self.end=reference('To point'); pts.addWidget(self.start); pts.addWidget(self.end)
            self.picks.addWidget(points)
            vector=QtWidgets.QWidget(); vec=QtWidgets.QHBoxLayout(vector); vec.setContentsMargins(0,0,0,0)
            self.x=QtWidgets.QDoubleSpinBox(); self.y=QtWidgets.QDoubleSpinBox()
            for label,spin in [('X',self.x),('Y',self.y)]:
                spin.setDecimals(6)
                spin.setRange(-10000,10000); vec.addWidget(QtWidgets.QLabel(label)); vec.addWidget(spin); spin.valueChanged.connect(owner.sync)
            self.x.setValue(1); self.picks.addWidget(vector); layout.addLayout(row)
            self.method.currentIndexChanged.connect(self.change_method); self.change_method(0)
            for ref in (self.reference,self.start,self.end): ref.textChanged.connect(owner.sync)
        elif kind=='radial':
            self.reference=reference('Pick a point, circle, or arc away from the center')
            form=QtWidgets.QFormLayout(); form.addRow('Radial reference',self.reference); layout.addLayout(form)
            self.reference.setToolTip('The vector from the rotation center to this point or circle/arc center defines outward. Copy size stays unchanged.')
            self.reference.textChanged.connect(owner.sync)
        row=QtWidgets.QHBoxLayout(); row.addWidget(QtWidgets.QLabel('Extent'))
        self.extent=combo(['One dimension','Two dimensions','Symmetric']); row.addWidget(self.extent,1)
        self.reverse=QtWidgets.QCheckBox('Reverse'); row.addWidget(self.reverse); layout.addLayout(row)
        grid=QtWidgets.QGridLayout(); self.grid=grid; grid.setHorizontalSpacing(8); grid.setVerticalSpacing(4)
        self.forward=QtWidgets.QLabel(); self.backward=QtWidgets.QLabel(); self.forward.setWordWrap(True); self.backward.setWordWrap(True)
        grid.addWidget(self.forward,0,1); grid.addWidget(self.backward,0,2)
        choices=['Angular pitch','Total angle'] if kind=='angular' else ['Pitch','Total distance']
        self.spacing=combo(choices); self.spacing2=combo(choices)
        self.value=amount(45 if kind=='angular' else 20,kind=='angular')
        self.value2=amount(30 if kind=='angular' else 10,kind=='angular')
        self.count=count(5); self.count2=count(3)
        for i,(label,a,b) in enumerate([('Spacing',self.spacing,self.spacing2),('Value',self.value,self.value2),('Instances',self.count,self.count2)],1):
            grid.addWidget(QtWidgets.QLabel(label),i,0); grid.addWidget(a,i,1); grid.addWidget(b,i,2)
        grid.setColumnStretch(1,1); grid.setColumnStretch(2,1); layout.addLayout(grid)
        self.note=QtWidgets.QLabel(); self.note.setWordWrap(True); layout.addWidget(self.note)
        for w in (self.extent,self.spacing,self.spacing2): w.currentIndexChanged.connect(owner.sync)
        for w in (self.value,self.value2,self.count,self.count2): w.valueChanged.connect(owner.sync)
        self.reverse.toggled.connect(owner.sync)

    def change_method(self,index):
        self.picks.setCurrentIndex(index)
        for i in range(self.picks.count()):
            self.picks.widget(i).setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Preferred if i==index else QtWidgets.QSizePolicy.Ignored)
        self.picks.setFixedHeight(self.picks.currentWidget().sizeHint().height()); self.owner.sync()

    def total(self): return self.count.value()+self.count2.value()-1 if self.extent.currentIndex()==1 else self.count.value()
    def valid(self):
        fields=(self.value,self.count,self.value2,self.count2) if self.extent.currentIndex()==1 else (self.value,self.count)
        if any(not field.hasAcceptableInput() for field in fields): return False
        if self.extent.currentIndex()==2 and self.count.value()%2==0: return False
        if self.kind=='angular': return True
        if self.kind=='radial': return bool(self.reference.text())
        if self.method.currentIndex()==0: return bool(self.reference.text())
        if self.method.currentIndex()==1: return bool(self.start.text() and self.end.text() and self.start.text()!=self.end.text())
        return self.x.hasAcceptableInput() and self.y.hasAcceptableInput() and bool(self.x.value() or self.y.value())

    def sync(self):
        two=self.extent.currentIndex()==1; symmetric=self.extent.currentIndex()==2
        for w in (self.backward,self.spacing2,self.value2,self.count2): w.setVisible(two)
        self.grid.setColumnStretch(2,1 if two else 0)
        self.reverse.setEnabled(not symmetric)
        labels={'linear':('Forward (+)','Backward (−)'), 'angular':('Counterclockwise','Clockwise'), 'radial':('Outward','Inward')}[self.kind]
        if self.reverse.isChecked(): labels=labels[::-1]
        self.forward.setText('Both sides' if symmetric else labels[0]); self.backward.setText(labels[1])
        if self.kind=='angular' and not two and self.spacing.currentIndex()==1 and self.value.value()==360:
            self.note.setText('Full circle: evenly spaced instances, with no duplicate at 360°.')
        elif two: self.note.setText(f'{self.count.value()} + {self.count2.value()} − 1 = {self.total()} instances. Both counts include the original.')
        elif symmetric: self.note.setText('Original in the middle. Use an odd count; total spans both sides.')
        else: self.note.setText('Instances include the original. Total spans original to last.')

class PatternControls(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent); self.building=True
        layout=QtWidgets.QVBoxLayout(self); layout.setContentsMargins(0,0,0,0); layout.setSpacing(6); layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(QtWidgets.QLabel('Geometry — click adds; Shift-click removes'))
        self.items=QtWidgets.QListWidget(); self.items.setFixedHeight(60)
        self.items.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection); layout.addWidget(self.items)
        row=QtWidgets.QHBoxLayout(); self.remove=QtWidgets.QPushButton('Remove'); self.clear=QtWidgets.QPushButton('Clear')
        row.addWidget(self.remove); row.addWidget(self.clear); layout.addLayout(row)
        self.remove.clicked.connect(self.remove_rows); self.clear.clicked.connect(self.clear_geometry)
        form=QtWidgets.QFormLayout(); self.mode=combo(['Linear','Circular']); self.layout_mode=combo(['One direction','Two directions'])
        form.addRow('Pattern',self.mode); form.addRow('Directions',self.layout_mode); layout.addLayout(form)
        self.center_row=QtWidgets.QWidget(); center_form=QtWidgets.QFormLayout(self.center_row); center_form.setContentsMargins(0,0,0,0)
        self.center=reference('Select a point, circle, or arc'); center_form.addRow('Rotation center',self.center); layout.addWidget(self.center_row)
        self.d1=Extent('Direction 1',self); self.d2=Extent('Direction 2',self)
        self.angular=Extent('Angular direction',self,'angular'); self.radial=Extent('Radial direction',self,'radial')
        for w in (self.d1,self.d2,self.angular,self.radial): layout.addWidget(w)
        self.lock=QtWidgets.QCheckBox('Create spacing constraints'); layout.addWidget(self.lock)
        self.lock.setChecked(True)
        self.lock.setToolTip('Constrain the pattern spacing and placement relative to the original geometry.')
        self.hide_spacing=QtWidgets.QCheckBox('Hide spacing chain'); layout.addWidget(self.hide_spacing)
        self.lock.toggled.connect(self.hide_spacing.setEnabled)
        self.lock.toggled.connect(self.sync); self.hide_spacing.toggled.connect(self.sync)
        self.summary=QtWidgets.QLabel(); self.summary.setWordWrap(True); layout.addWidget(self.summary)
        self.status=TaskStatus(); layout.addWidget(self.status)
        row=QtWidgets.QHBoxLayout(); self.apply=QtWidgets.QPushButton('Apply'); self.done=QtWidgets.QPushButton('Done')
        self.cancel=QtWidgets.QPushButton('Cancel')
        row.addWidget(self.done); row.addWidget(self.apply); row.addWidget(self.cancel); layout.addLayout(row)


        self.mode.currentIndexChanged.connect(self.change_mode); self.layout_mode.currentIndexChanged.connect(self.sync)
        self.center.textChanged.connect(self.sync); self.items.installEventFilter(self)
        for hint in self.findChildren(QtWidgets.QLabel): hint.setWordWrap(True)
        self.building=False; self.sync()

    def change_mode(self):
        self.layout_mode.blockSignals(True); self.layout_mode.clear()
        self.layout_mode.addItems(['Angular','Radial','Angular + radial'] if self.mode.currentIndex() else ['One direction','Two directions'])
        self.layout_mode.blockSignals(False); self.sync()

    def active_extents(self):
        if not self.mode.currentIndex(): return [self.d1,self.d2] if self.layout_mode.currentIndex()==1 else [self.d1]
        return [[self.angular],[self.radial],[self.angular,self.radial]][self.layout_mode.currentIndex()]

    def eventFilter(self,obj,event):
        if event.type()==QtCore.QEvent.KeyPress and event.key()==QtCore.Qt.Key_Delete:
            self.remove_rows(); return True
        return False
    def add_geometry(self,name,shift=False):
        found=self.items.findItems(name,QtCore.Qt.MatchExactly)
        if shift:
            for item in found: self.items.takeItem(self.items.row(item))
        elif not found: self.items.addItem(name)
        self.sync()
    def remove_rows(self):
        for item in self.items.selectedItems(): self.items.takeItem(self.items.row(item))
        self.sync()
    def clear_geometry(self): self.items.clear(); self.sync()
    def sync(self,*args):
        if self.building: return
        active=self.active_extents(); circular=bool(self.mode.currentIndex())
        self.center_row.setVisible(circular)
        for e in (self.d1,self.d2,self.angular,self.radial): e.setVisible(e in active); e.sync()
        odd_error=any(e.extent.currentIndex()==2 and e.count.value()%2==0 for e in active)
        ready=bool(self.items.count()) and all(e.valid() for e in active) and (not circular or bool(self.center.text()))
        total=1
        for e in active: total*=e.total()
        dimensions=' × '.join(str(e.total()) for e in active)
        self.summary.setText((dimensions+' = ' if len(active)>1 else '')+str(total)+' instances, including the original.')
        if odd_error: self.status.setError('Symmetric requires an odd count, with the original in the middle.')
        elif not self.items.count(): self.status.setText('Select the geometry to pattern.')
        elif not ready: self.status.setText('Choose the direction and center references.')
        else: self.status.setText('Ready to create the pattern.')
        self.status.setVisible(not ready)
        self.apply.setEnabled(ready)
        complete=[e for e in active if e.valid()]
        if self.items.count() and complete and not ready and (not circular or self.center.text()):
            n=1
            for e in complete:n*=e.total()
            self.summary.setText(str(n)+' instances previewed.')
            self.status.setText('Complete the remaining direction to preview and apply the full pattern.')



InstalledPatternControls = PatternControls

class PatternControls(InstalledPatternControls):
    """UI-only prototype; no geometry or solver mutation."""
    linked_preview = True

    def __init__(self,parent):
        super().__init__(parent)
        self.linked=True;self.editing=False;self.independent=False
        self.options_dialog=QtWidgets.QDialog(self)
        self.options_dialog.setWindowTitle('Pattern options');self.options_dialog.setModal(True)
        layout=QtWidgets.QVBoxLayout(self.options_dialog)
        group=QtWidgets.QGroupBox('Pattern behavior');choices=QtWidgets.QVBoxLayout(group)
        self.linked_radio=QtWidgets.QRadioButton('Linked pattern')
        self.constraint_radio=QtWidgets.QRadioButton('Constraint-based pattern')
        choices.addWidget(self.linked_radio)
        label=QtWidgets.QLabel('Copies follow the original geometry. Edit the original or the pattern to change them.')
        label.setWordWrap(True);choices.addWidget(label)
        choices.addWidget(self.constraint_radio)
        label=QtWidgets.QLabel('Copies use sketch constraints. Retains the previous pattern behavior.')
        label.setWordWrap(True);choices.addWidget(label);layout.addWidget(group)
        self.legacy=QtWidgets.QGroupBox('Constraint options');options=QtWidgets.QVBoxLayout(self.legacy)
        self.layout().removeWidget(self.lock);self.layout().removeWidget(self.hide_spacing)
        options.addWidget(self.lock);options.addWidget(self.hide_spacing);layout.addWidget(self.legacy)
        self.constraint_radio.toggled.connect(self.legacy.setEnabled)
        self.options_actions=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        self.options_actions.accepted.connect(self.accept_options)
        self.options_actions.rejected.connect(self.options_dialog.reject)
        self.options_dialog.rejected.connect(self.cancel_options)
        layout.addWidget(self.options_actions)
        self.mode_note=QtWidgets.QLabel();self.mode_note.setWordWrap(True)
        self.advanced=QtWidgets.QPushButton('Advanced options…');self.advanced.clicked.connect(self.open_options)
        self.make_independent=QtWidgets.QPushButton('Make independent…')
        self.make_independent.clicked.connect(self.confirm_independent)
        at=self.layout().indexOf(self.summary)
        for offset,widget in enumerate((self.mode_note,self.advanced,self.make_independent)):
            self.layout().insertWidget(at+offset,widget)
        self.refresh_behavior()

    def set_editing(self,linked=True):
        self.editing=True;self.linked=linked;self.refresh_behavior()

    def refresh_behavior(self):
        self.mode_note.setText('Linked pattern · copies follow the original.' if self.linked else 'Constraint-based pattern · uses sketch constraints.')
        self.make_independent.setVisible(self.editing and self.linked)

    def open_options(self):
        self.draft=(self.linked,self.lock.isChecked(),self.hide_spacing.isChecked())
        self.linked_radio.setChecked(self.linked);self.constraint_radio.setChecked(not self.linked)
        self.legacy.setEnabled(not self.linked)
        self.options_dialog.resize(420,330);self.options_dialog.open()

    def accept_options(self):
        self.linked=self.linked_radio.isChecked();self.refresh_behavior();self.options_dialog.accept()

    def cancel_options(self):
        self.linked,locked,hidden=self.draft
        self.lock.setChecked(locked);self.hide_spacing.setChecked(hidden);self.refresh_behavior()

    def confirm_independent(self):
        dialog=QtWidgets.QDialog(self);dialog.setWindowTitle('Make pattern independent');dialog.setModal(True)
        layout=QtWidgets.QVBoxLayout(dialog)
        text=QtWidgets.QLabel('Convert all copies in this pattern into ordinary editable sketch curves?\n\nThe curves keep their current positions and stop following the original. No constraints are added. The original geometry is kept.')
        text.setWordWrap(True);layout.addWidget(text)
        buttons=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        make=buttons.addButton('Make independent',QtWidgets.QDialogButtonBox.AcceptRole)
        make.clicked.connect(dialog.accept);buttons.rejected.connect(dialog.reject)
        dialog.accepted.connect(lambda:setattr(self,'independent',True))
        layout.addWidget(buttons);self.independent_dialog=dialog;dialog.resize(430,230);dialog.open()

    def reset_preview(self):
        self.items.clear();self.linked=True;self.editing=False
        self.mode.setCurrentIndex(0);self.layout_mode.setCurrentIndex(0)
        self.lock.setChecked(True);self.hide_spacing.setChecked(False)
        for e in (self.d1,self.d2,self.angular,self.radial):
            e.extent.setCurrentIndex(0);e.reverse.setChecked(False)
            e.spacing.setCurrentIndex(0);e.spacing2.setCurrentIndex(0)
            e.count.setValue(5);e.count2.setValue(3)
            e.value.setValue(45 if e.kind=='angular' else 20);e.value2.setValue(30 if e.kind=='angular' else 10)
            if e.reference:e.reference.clear()
            if e.kind=='linear':
                e.method.setCurrentIndex(0);e.start.clear();e.end.clear();e.x.setValue(1);e.y.setValue(0)
        self.center.clear();self.refresh_behavior();self.sync()
