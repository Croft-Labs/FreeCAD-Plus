# SPDX-License-Identifier: LGPL-2.1-or-later
from PySide6 import QtCore, QtWidgets
from . import sketch_pattern as pattern
from freecad_plus.task_status import TaskStatus
from .quantity_fields import QuantityNumber


def combo(items):
    w=QtWidgets.QComboBox(); w.addItems(items); return w
def count(value):
    w=QtWidgets.QSpinBox(); w.setRange(2,999); w.setValue(value); return w
def amount(value, angular=False):
    w=QuantityNumber(); w.setRange(.000001,360 if angular else 100000)
    w.setSuffix('deg' if angular else 'mm'); w.setValue(value); return w
def reference(text):
    w=QtWidgets.QLineEdit(); w.setReadOnly(True); w.setPlaceholderText(text); w.setClearButtonEnabled(True); return w

class Extent(QtWidgets.QGroupBox):
    def __init__(self,title,owner,kind='linear'):
        super().__init__(title); self.owner=owner; self.kind=kind
        layout=QtWidgets.QVBoxLayout(self); layout.setSpacing(5); layout.setContentsMargins(8,10,8,8)
        self.reference=None
        if kind=='linear':
            row=QtWidgets.QHBoxLayout(); self.method=combo(['Axis or line','Two points','Vector'])
            self.method.setMaximumWidth(125); row.addWidget(self.method)
            self.picks=QtWidgets.QStackedWidget(); row.addWidget(self.picks,1)
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
        self.forward=QtWidgets.QLabel(); self.backward=QtWidgets.QLabel()
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
        if self.extent.currentIndex()==2 and self.count.value()%2==0: return False
        if self.kind=='angular': return True
        if self.kind=='radial': return bool(self.reference.text())
        if self.method.currentIndex()==0: return bool(self.reference.text())
        if self.method.currentIndex()==1: return bool(self.start.text() and self.end.text() and self.start.text()!=self.end.text())
        return bool(self.x.value() or self.y.value())

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
        layout=QtWidgets.QVBoxLayout(self); layout.setContentsMargins(0,0,0,0); layout.setSpacing(6)
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
        self.summary=QtWidgets.QLabel(); self.summary.setWordWrap(True); layout.addWidget(self.summary)
        self.status=TaskStatus(); layout.addWidget(self.status)
        row=QtWidgets.QHBoxLayout(); self.apply=QtWidgets.QPushButton('Apply'); self.done=QtWidgets.QPushButton('Done')
        row.addWidget(self.apply); row.addWidget(self.done); layout.addLayout(row)


        self.mode.currentIndexChanged.connect(self.change_mode); self.layout_mode.currentIndexChanged.connect(self.sync)
        self.center.textChanged.connect(self.sync); self.items.installEventFilter(self)
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


class PatternTask(PatternControls):
    """Controls owned by the native sketch tool; picks arrive through that tool."""
    def __init__(self, host, sketch, ids):
        self.host = host
        self.sketch = sketch
        self.closed = False
        self.references = {}
        self.active_pick = None
        self._preview = []
        self.ready = False
        super().__init__(host)
        self.setObjectName('SketchPatternPanel')
        host.setProperty('patternGeometryPicking', True)
        self.active_pick = self.items
        fields = [self.center, self.radial.reference]
        for extent in (self.d1, self.d2):
            fields.extend((extent.reference, extent.start, extent.end))
        for field in fields:
            self.references[field] = None
            field.installEventFilter(self)
        self.items.viewport().installEventFilter(self)
        for spin in self.findChildren(QtWidgets.QAbstractSpinBox):
            spin.setKeyboardTracking(False)
        for child in self.findChildren(QtWidgets.QWidget):
            child.installEventFilter(self)
        self.apply.clicked.connect(self.apply_pattern)
        self.done.clicked.connect(lambda: self.notify('finish'))
        for index in ids:
            if 0 <= index < sketch.GeometryCount:
                self.add_geometry('Edge' + str(index + 1))
        self.ready = True
        self.hide_spacing.setChecked(pattern.chain_is_hidden(sketch))
        self.hide_spacing.toggled.connect(self.toggle_spacing)
        self.activate_pick(self.items)
        self.sync()

    def notify(self, action):
        if self.closed: return
        self.host.setProperty('patternAction', action)
        self.host.setProperty('patternSerial', int(self.host.property('patternSerial') or 0) + 1)

    def toggle_spacing(self, hidden):
        if getattr(self.sketch, 'PatternSpacingTags', []):
            self.sketch.Document.openTransaction('Hide pattern spacing chain' if hidden else 'Show pattern spacing chain')
            try:
                pattern.set_chain_hidden(self.sketch, hidden)
                self.sketch.Document.commitTransaction()
            except Exception:
                self.sketch.Document.abortTransaction()
                raise

    def activate_pick(self, field):
        if self.active_pick is not None:
            self.active_pick.setStyleSheet('')
        self.active_pick = field
        field.setStyleSheet('border: 2px solid #408bc9;')
        self.host.setProperty('patternGeometryPicking', field is self.items)

    def eventFilter(self, obj, event):
        if event.type() in (QtCore.QEvent.KeyPress, QtCore.QEvent.KeyRelease) and event.key() == QtCore.Qt.Key_Escape:
            if event.type() == QtCore.QEvent.KeyPress: self.notify('finish')
            return True
        if event.type() in (QtCore.QEvent.FocusIn, QtCore.QEvent.MouseButtonPress):
            if obj in self.references:
                self.activate_pick(obj)
            elif obj in (self.items, self.items.viewport()):
                self.activate_pick(self.items)
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Delete:
            if obj in (self.items, self.items.viewport()):
                self.remove_rows(); return True
            if obj in self.references:
                self.references[obj] = None; obj.clear(); return True
        return False

    def geometry_ids(self):
        return [int(self.items.item(i).text()[4:]) - 1 for i in range(self.items.count())]

    def pick(self, geo, pos, remove=False):
        if self.closed or geo == pattern.UNDEFINED: return
        if self.active_pick is self.items:
            if 0 <= geo < self.sketch.GeometryCount:
                self.add_geometry('Edge' + str(geo + 1), remove)
            return
        field = self.active_pick
        if field not in self.references or not field.isVisible(): return
        ref = (geo, pos)
        try:
            if field in (self.d1.reference, self.d2.reference):
                pattern.direction(self.sketch, {'reference': ref})
            else:
                _, ref = pattern.point_reference(self.sketch, ref)
            if remove:
                if self.references[field] == ref:
                    self.references[field] = None; field.clear(); self.sync()
                return
            self.references[field] = ref
            geo, pos = ref
            label = ('Origin' if pos else 'X axis') if geo == -1 else ('Y axis' if geo == -2 else ('External ' + str(-geo - 2) if geo < -2 else 'Edge' + str(geo + 1)))
            if geo != -1 and pos: label += ' · ' + ('center' if pos == 3 else 'point ' + str(pos))
            field.setText(label)
            self.sync()
        except (ValueError, RuntimeError) as error:
            self.apply.setEnabled(False)
            self._preview = []; self.notify('preview')
            self.status.setError(str(error)); self.status.show()

    def pick_constraint(self, name, remove=False):
        try:
            c = self.sketch.Constraints[int(name[10:]) - 1]
            if c.Type in ('Radius', 'Diameter'):
                self.pick(c.First, 3, remove)
        except (ValueError, IndexError): pass

    def extent_options(self, extent):
        values = dict(mode=extent.extent.currentText(), reverse=extent.reverse.isChecked(),
                      spacing=extent.spacing.currentText(), value=extent.value.value(), count=extent.count.value(),
                      spacing2=extent.spacing2.currentText(), value2=extent.value2.value(), count2=extent.count2.value())
        values.update(unit=extent.value._unit, unit2=extent.value2._unit)
        if extent.kind == 'linear':
            values.update(method=extent.method.currentText(), x=extent.x.value(), y=extent.y.value(),
                          reference=self.references.get(extent.reference),
                          start=self.references.get(extent.start), end=self.references.get(extent.end))
        elif extent.kind == 'radial': values['reference'] = self.references.get(extent.reference)
        return values

    def options(self):
        return dict(pattern=self.mode.currentText(), directions=self.layout_mode.currentText(), hide_spacing=self.hide_spacing.isChecked(),
                    center=self.references.get(self.center), d1=self.extent_options(self.d1),
                    d2=self.extent_options(self.d2), angular=self.extent_options(self.angular),
                    radial=self.extent_options(self.radial))

    def sync(self, *args):
        if not self.ready or self.closed: return
        for field in self.references:
            if not field.text(): self.references[field] = None
        super().sync()
        self._preview = []
        if self.apply.isEnabled():
            try:
                ids, options = self.geometry_ids(), self.options()
                self._preview = pattern.preview(self.sketch, ids, options)
                total = len(pattern.transforms(self.sketch, options)) + 1
                self.summary.setText(str(total) + ' instances, including the original.')
            except Exception as error:
                self.apply.setEnabled(False)
                self.status.setError(str(error)); self.status.show()
        self.notify('preview')

    def get_preview(self): return self._preview

    def apply_pattern(self):
        if not self.apply.isEnabled() or self.closed: return
        try:
            pattern.apply(self.sketch, self.geometry_ids(), self.options(), self.lock.isChecked())
            import FreeCADGui as Gui
            Gui.Selection.clearSelection()
            self.clear_geometry()
            self.activate_pick(self.items)
        except Exception as error:
            self.status.setError(str(error)); self.status.show()

    def reset_inputs(self):
        if self.closed: return
        self.items.clear()
        for field in self.references:
            self.references[field] = None; field.clear()
        self.activate_pick(self.items)
        self.sync()

    def detach(self):
        self.closed = True
        self._preview = []


def create(host, sketch, ids):
    layout = QtWidgets.QVBoxLayout(host)
    layout.setContentsMargins(0, 0, 0, 0)
    panel = PatternTask(host, sketch, ids)
    layout.addWidget(panel)
    return panel
