# SPDX-License-Identifier: LGPL-2.1-or-later
from PySide6 import QtCore, QtWidgets
from . import sketch_pattern as pattern
from freecad_plus.task_status import TaskStatus
from .quantity_fields import QuantityNumber


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


class PatternTask(PatternControls):
    """Controls owned by the native sketch tool; picks arrive through that tool."""
    def __init__(self, host, sketch, ids, group=''):
        self.host = host
        self.sketch = sketch
        self.closed = False
        self.references = {}
        self.active_pick = None
        self._preview = []
        self._helper_preview=[]
        self._helper_root=None
        self._helper_node=None
        self.ready = False
        self.edit_group=group
        self.edit_record=None
        self.edit_error=''
        self.updating=False
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
        self.done.clicked.connect(self.finish_pattern)
        self.cancel.clicked.connect(lambda: self.notify('finish'))
        for index in ids:
            if 0 <= index < sketch.GeometryCount:
                self.add_geometry('Edge' + str(index + 1))
        self.ready = True
        self.hide_spacing.setChecked(pattern.chain_is_hidden(sketch))
        self.hide_spacing.toggled.connect(self.toggle_spacing)
        for spin in self.findChildren(QtWidgets.QAbstractSpinBox):
            spin.lineEdit().textEdited.connect(self.sync)
        self.activate_pick(self.items)
        if group:
            try:
                from . import sketch_pattern_edit as editing
                self.edit_record,ids,options=editing.load(sketch,group)
                self.load_inputs(ids,options,self.edit_record['dimensions'])
            except (ValueError,RuntimeError) as error:self.edit_error=str(error)
        self.sync()

    def load_inputs(self,ids,options,dimensions):
        self.ready=False
        self.items.clear()
        for i in ids:self.items.addItem('Edge'+str(i+1))
        self.mode.setCurrentText(options.get('pattern','Linear'))
        self.layout_mode.setCurrentText(options.get('directions','One direction'))
        def set_reference(field,value):
            self.references[field]=value
            if value is None:field.clear();return
            geo,pos=value
            text=('Origin' if pos else 'X axis') if geo==-1 else 'Y axis' if geo==-2 else 'External '+str(-geo-2) if geo<0 else 'Edge'+str(geo+1)
            if geo>=0 and pos:text+=' · '+('center' if pos==3 else 'point '+str(pos))
            field.setText(text)
        set_reference(self.center,options.get('center'))
        for name in ('d1','d2','angular','radial'):
            e=getattr(self,name);values=options.get(name,{})
            if not values:continue
            e.extent.setCurrentText(values.get('mode','One dimension'))
            e.reverse.setChecked(values.get('reverse',False))
            for suffix in ('','2'):
                getattr(e,'spacing'+suffix).setCurrentText(values.get('spacing'+suffix,'Angular pitch' if name=='angular' else 'Pitch'))
                getattr(e,'count'+suffix).setValue(values.get('count'+suffix,3))
                value=getattr(e,'value'+suffix);value.setSuffix(values.get('unit'+suffix,'deg' if name=='angular' else 'mm'))
                value.setValue(values.get('value'+suffix,10))
            if e.kind=='linear':
                e.method.setCurrentText(values.get('method','Axis or line'))
                e.x.setValue(values.get('x',1));e.y.setValue(values.get('y',0))
                for key in ('reference','start','end'):set_reference(getattr(e,key),values.get(key))
            elif e.kind=='radial':set_reference(e.reference,values.get('reference'))
        self.lock.setChecked(dimensions);self.hide_spacing.setChecked(options.get('hide_spacing',False))
        self.ready=True

    def get_hidden_geometry(self):
        if not self.edit_record or self.updating:return []
        from .sketch_pattern_edit import owned
        hidden=owned(self.edit_record)
        return [i for i,f in enumerate(self.sketch.GeometryFacadeList) if str(f.Id) in hidden]

    def get_edit_group(self):return self.edit_group if not self.updating and not self.edit_error else ''

    def notify(self, action):
        if self.closed: return
        self.host.setProperty('patternAction', action)
        self.host.setProperty('patternSerial', int(self.host.property('patternSerial') or 0) + 1)

    def toggle_spacing(self, hidden):
        # Pending controls affect only the preview. With no pending geometry the
        # checkbox can still show/hide existing saved chains.
        if self.ready and not self.edit_group and not self.items.count() and getattr(self.sketch, 'PatternSpacingTags', []):
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
            self._helper_preview=[];self.clear_helpers()
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

    def preview_options(self):
        options=self.options()
        active=self.active_extents()
        if options['pattern']=='Circular' and not options['center']: return None
        complete=[]
        for extent in active:
            if not extent.valid(): continue
            candidate=dict(options)
            if extent.kind=='linear':
                candidate.update(directions='One direction',d1=self.extent_options(extent))
            else: candidate['directions']='Angular' if extent.kind=='angular' else 'Radial'
            try: pattern.transforms(self.sketch,candidate)
            except (ValueError,RuntimeError): continue
            complete.append((extent,candidate))
        if len(complete)==len(active): return options
        if complete: return complete[0][1]
        return None

    def sync(self, *args):
        if not self.ready or self.closed: return
        if self.edit_error:
            self.apply.setEnabled(False);self.status.setError(self.edit_error);self.status.show();return
        for field in self.references:
            if not field.text(): self.references[field] = None
        super().sync()
        self._preview = []
        self._helper_preview=[]
        if self.apply.isEnabled():
            try: pattern.transforms(self.sketch,self.options())
            except Exception as error:
                self.apply.setEnabled(False);self.status.setError(str(error));self.status.show()
        options=self.preview_options() if self.items.count() else None
        if options is not None:
            try:
                ids = self.geometry_ids()
                self._preview = pattern.preview(self.sketch, ids, options, self.lock.isChecked(),self._helper_preview)
                total = len(pattern.transforms(self.sketch, options)) + 1
                self.summary.setText(str(total) + (' instances, including the original.' if self.apply.isEnabled() else ' instances previewed.'))
            except Exception as error:
                self._preview=[];self._helper_preview=[]
                self.apply.setEnabled(False)
                self.status.setError(str(error)); self.status.show()
        self.update_helpers()
        if self.edit_group and self.apply.isEnabled():
            self.status.setText('Editing existing pattern. Changes replace its generated instances.')
            self.status.show()
        self.notify('preview')

    def get_preview(self): return self._preview

    def update_helpers(self):
        self.clear_helpers()
        if not self._helper_preview:return
        import FreeCAD as App, FreeCADGui as Gui
        from pivy import coin
        root=Gui.activeDocument().activeView().getSceneGraph()
        node=coin.SoSeparator();node.setName('FreeCADPlusPatternSpacingPreview')
        pick=coin.SoPickStyle();pick.style=coin.SoPickStyle.UNPICKABLE;node.addChild(pick)
        color=coin.SoBaseColor()
        packed=App.ParamGet('User parameter:BaseApp/Preferences/Mod/Sketcher').GetUnsigned('ConstructionColor',0x0000ffff)
        color.rgb=((packed>>24&255)/255.,(packed>>16&255)/255.,(packed>>8&255)/255.);node.addChild(color)
        style=coin.SoDrawStyle();style.lineWidth=1.5;style.linePattern=0xf0f0;node.addChild(style)
        placement=self.sketch.getGlobalPlacement()
        points=[];counts=[]
        for g in self._helper_preview:
            shape=g.toShape()
            if not shape.Edges:continue
            vertices=shape.discretize(Number=65) if hasattr(g,'Radius') else [g.StartPoint,g.EndPoint]
            counts.append(len(vertices))
            points.extend(tuple(placement.multVec(v)) for v in vertices)
        coords=coin.SoCoordinate3();coords.point.setValues(0,len(points),points);node.addChild(coords)
        lines=coin.SoLineSet();lines.numVertices.setValues(0,len(counts),counts);node.addChild(lines)
        root.addChild(node);self._helper_root=root;self._helper_node=node

    def clear_helpers(self):
        if self._helper_node is not None:
            self._helper_root.removeChild(self._helper_node)
        self._helper_root=None;self._helper_node=None

    def apply_pattern(self):
        if not self.apply.isEnabled() or self.closed: return False
        try:
            if self.edit_group:
                from . import sketch_pattern_edit as editing
                self.updating=True;self.notify('preview')
                editing.update(self.sketch,self.edit_group,self.geometry_ids(),self.options(),self.lock.isChecked())
            else:pattern.apply(self.sketch, self.geometry_ids(), self.options(), self.lock.isChecked())
            import FreeCADGui as Gui
            Gui.Selection.clearSelection()
            self.reset_inputs()
            return True
        except Exception as error:
            # Keep the originating operation (and any rollback exception) in
            # the application log. The short task message alone cannot locate
            # native allocation failures reported by the pattern service.
            try:
                import traceback
                import FreeCAD as App
                App.Console.PrintError('Sketch Pattern Apply failed:\n' + traceback.format_exc())
            except Exception:
                pass  # Logging must not prevent recovery under memory pressure.
            self.updating=False;self.notify('preview')
            self.status.setError(str(error)); self.status.show()
            return False

    def finish_pattern(self):
        if self.closed: return
        if not self.items.count(): self.notify('finish')
        elif self.apply.isEnabled():
            if self.apply_pattern(): self.notify('finish')
        else:
            self.status.setError('Complete the pattern inputs before choosing Done, or Cancel to discard them.')
            self.status.show()

    def reset_inputs(self):
        if self.closed: return
        self.ready=False; self.building=True
        self.edit_group='';self.edit_record=None;self.edit_error='';self.updating=False
        self.items.clear()
        for field in self.references:
            self.references[field] = None; field.clear()
        self.mode.setCurrentIndex(0); self.change_mode(); self.layout_mode.setCurrentIndex(0)
        self.lock.setChecked(True); self.hide_spacing.setChecked(False)
        for extent in (self.d1,self.d2,self.angular,self.radial):
            extent.extent.setCurrentIndex(0); extent.reverse.setChecked(False)
            extent.spacing.setCurrentIndex(0); extent.spacing2.setCurrentIndex(0)
            extent.value.setValue(45 if extent.kind=='angular' else 20)
            extent.value2.setValue(30 if extent.kind=='angular' else 10)
            extent.count.setValue(5); extent.count2.setValue(3)
            if extent.kind=='linear':
                extent.method.setCurrentIndex(0); extent.x.setValue(1); extent.y.setValue(0)
        self.activate_pick(self.items)
        self.ready=True; self.building=False
        self.sync()

    def detach(self):
        self.clear_helpers()
        self.closed = True
        self._preview = []
        self._helper_preview=[]


def create(host, sketch, ids, group=''):
    layout = QtWidgets.QVBoxLayout(host)
    layout.setContentsMargins(0, 0, 0, 0)
    panel = PatternTask(host, sketch, ids, group)
    layout.addWidget(panel)
    return panel
