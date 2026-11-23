# SPDX-License-Identifier: LGPL-2.1-or-later
"""Approved shared Extrude creation/editing task; no model writes before OK."""
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtWidgets
from pivy import coin
from freecad_plus import modeling, planes, extrusion, document, editing, hierarchy, isolation, display, task_visibility
from freecad_plus.plane_task import Section, label, number, buttons
from .task_status import TaskStatus
from freecad_plus.selection_list import SelectionList


_active = None


class ExtrudeTask(QtCore.QObject):
    engine = extrusion
    title = "Extrude"
    icon = "PartDesign_Pad"
    def __init__(self, feature=None, which='Pad'):
        super().__init__()
        self.doc = Gui.activeDocument().Document
        self.owner, self.path = modeling._context(self.doc)
        self.source_doc = self.owner.Document
        self.feature = feature
        self.context = modeling._routing_context(self.doc, self.owner, self.path)
        self.view = Gui.activeDocument().activeView()
        self.scene = self.view.getSceneGraph()
        self.overlay = None
        self.target_overlay = None
        self.tool_preview = None
        self.showing_result = False
        self.result_shape = None
        self.tool_shape = None
        self.closed = False
        self.ready = False
        self.revisions = 0
        self.valid = False
        self.pick = 'profile'
        self.refs = []
        self.links = {}
        self.target_mode = None
        self.automatic_target = None
        self.fields = {}
        self.numbers = []
        self.values = {}
        self.hidden = False
        self.presentation = None
        self.profile_highlight = None
        self.hidden_objects = []
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(self.title)
        self.form.setWindowIcon(Gui.getIcon(self.icon))
        layout = QtWidgets.QVBoxLayout(self.form)
        layout.setContentsMargins(6,4,6,4); layout.setSpacing(2)
        layout.addWidget(label('Component: ' + self.owner.Label))
        self.operation = self.section(layout, 'Operation')
        row = QtWidgets.QVBoxLayout()
        self.modes = {}
        self.group = QtWidgets.QButtonGroup(self)
        for name in ('New Solid','Add','Subtract'):
            button = QtWidgets.QRadioButton(name)
            self.group.addButton(button); self.modes[name] = button; row.addWidget(button)
            button.clicked.connect(self.changed)
        self.modes['New Solid'].setChecked(True)
        self.outputs = {}
        if self.engine is extrusion:
            self.modes['New Solid'].setText('New')
            columns = QtWidgets.QHBoxLayout(); output_row = QtWidgets.QVBoxLayout()
            self.output_group = QtWidgets.QButtonGroup(self)
            for name in ('Solid', 'Sheet'):
                button = QtWidgets.QRadioButton(name)
                button.setObjectName('ExtrudeOutput' + name)
                self.output_group.addButton(button); self.outputs[name] = button
                output_row.addWidget(button); button.clicked.connect(self.changed)
            self.outputs['Solid'].setChecked(True); output_row.addStretch()
            columns.addLayout(output_row, 1); columns.addLayout(row, 1)
            self.operation.layout.addLayout(columns)
        else:
            self.operation.layout.addLayout(row)
        self.target_row = self.reference(self.operation.layout,'Target solid','target','Pick the current solid to modify')
        self.target_hint = label('')
        self.target_row.layout().addWidget(self.target_hint)
        self.profile = self.section(layout, 'Profile')
        self.profile_hint = label('Select a sketch, closed sketch region, or face.')
        self.profile.layout.addWidget(self.profile_hint)
        self.profiles = SelectionList()
        self.profiles.installEventFilter(self); self.profile.layout.addWidget(self.profiles)
        buttons(self.profile.layout,[('Remove',self.remove_profile),('Clear',self.clear_profile),('Whole sketch',self.whole_profile)])
        self.start = self.section(layout, 'Start', False)
        self.start_type = self.combo(self.start.layout,'From',['Profile plane','Offset','Reference'])
        self.start_row = self.reference(self.start.layout,'Reference','start','Pick a start face or plane')
        self.start_offset_row, self.start_offset = self.numeric(self.start.layout,'Start offset',0)
        self.extent = self.section(layout, 'Extent')
        self.sides = self.combo(self.extent.layout,'Sides',['One side','Symmetric','Two sides'])
        self.end1 = self.end_controls(self.extent.layout, '')
        row = QtWidgets.QHBoxLayout(); self.direction_label = QtWidgets.QLabel('Direction: Profile normal'); row.addWidget(self.direction_label)
        self.reverse = QtWidgets.QPushButton('Reverse'); self.reverse.setCheckable(True)
        self.reverse.toggled.connect(self.changed); row.addWidget(self.reverse); self.extent.layout.addLayout(row)
        self.second = self.section(self.extent.layout,'Second side',True)
        self.end2 = self.end_controls(self.second.layout,'second')
        self.advanced = self.section(layout, 'Direction and taper', False)
        self.direction = self.combo(self.advanced.layout,'Direction',['Profile normal','Selected axis / line'])
        self.direction_row = self.reference(self.advanced.layout,'Axis / line','direction','Pick a straight edge or axis')
        self.measure = self.combo(self.advanced.layout,'Measure length',['Along direction','Along profile normal'])
        self.taper_row, self.taper = self.numeric(self.advanced.layout,'Taper angle',0,' °')
        self.taper2_row, self.taper2 = self.numeric(self.advanced.layout,'Side 2 taper',0,' °')
        self.taper.setRange(-89.99,89.99); self.taper2.setRange(-89.99,89.99)
        self.refine = QtWidgets.QCheckBox('Refine result'); self.refine.setChecked(True)
        self.advanced.layout.addWidget(self.refine); self.refine.toggled.connect(self.changed)
        self.preview = self.section(layout,'Preview')
        self.display = self.combo(self.preview.layout,'Show',['Tool volume','Result'])
        row = QtWidgets.QHBoxLayout()
        self.visible = QtWidgets.QCheckBox('Show preview'); self.visible.setChecked(True)
        self.automatic = QtWidgets.QCheckBox('Recompute on update'); self.automatic.setChecked(True)
        row.addWidget(self.visible); row.addWidget(self.automatic); self.preview.layout.addLayout(row)
        self.refresh_button = QtWidgets.QPushButton('Update preview'); self.preview.layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.render)
        self.visible.toggled.connect(self.changed)
        self.automatic.toggled.connect(self.changed)
        self.status = TaskStatus('Select a profile.'); layout.addWidget(self.status); layout.addStretch()
        self.configure_form()
        if feature is not None:
            self.load_feature(feature)
        else:
            raw = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('*',0) for sub in entry.SubElementNames or ('',)]
            for obj,sub in planes.canonical(self.owner,raw):
                obj,sub = self.engine.profile_reference((obj,sub))
                if (obj.isDerivedFrom('Sketcher::SketchObject') or Part.splitSubname(sub)[2].startswith('Face')
                        or (self.engine is extrusion and (Part.splitSubname(sub)[2].startswith('Edge')
                            or (obj.isDerivedFrom('Part::Feature') and obj.Shape.Edges and not obj.Shape.Faces)))):
                    if self.engine is extrusion and not obj.isDerivedFrom('Sketcher::SketchObject') and not Part.splitSubname(sub)[2].startswith('Face'):
                        self.engine.validate_profiles(self.owner, [(obj, sub)], 'Sheet')
                    else:
                        self.engine.validate_profiles(self.owner, [(obj, sub)])
                    self.refs.append((obj,sub))
                elif obj.TypeId == 'PartDesign::Body' or obj.isDerivedFrom('PartDesign::Feature'):
                    target = obj.Tip if obj.TypeId == 'PartDesign::Body' else obj
                    modeling._target_body(self.owner,target)
                    if 'target' in self.links and self.links['target'][0] != target:
                        raise ValueError('Select one target solid.')
                    self.links['target'] = (target,'')
            self.modes['Subtract' if which in ('Pocket','Groove') else 'Add' if 'target' in self.links else 'New Solid'].setChecked(True)
        Gui.Selection.clearSelection()
        Gui.Selection.addObserver(self,0)
        App.addDocumentObserver(self)
        editing.add_context_observer(self.context_changed)
        self.mouse_callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.pick_region)
        self.presentation = task_visibility.ExtrudeDisplay(self)
        QtWidgets.QApplication.instance().focusChanged.connect(self.focus_changed)
        self.ready = True
        self.refresh_fields()

    def configure_form(self):
        pass

    def check(self):
        if self.closed or Gui.activeDocument() is None or Gui.activeDocument().activeView() != self.view:
            raise ValueError('Return to the view where '+self.title+' was opened.')
        definition,path = modeling._context(self.doc)
        if modeling._routing_context(self.doc,definition,path) != self.context:
            raise ValueError('The edited component changed; start '+self.title+' again.')

    def context_changed(self):
        if self.closed:return
        try:self.check()
        except Exception:self.reject()

    def slotDeletedDocument(self,doc):
        if doc in (self.doc,self.source_doc):self.reject(document_closing=True)

    def slotStartSaveDocument(self,doc,*args):
        if doc==self.source_doc and not self.closed:
            self.presentation.restore()

    def slotFinishSaveDocument(self,doc,*args):
        if doc==self.source_doc and not self.closed:
            self.presentation.apply()

    def slotDeletedObject(self,obj):
        if obj==self.feature or any(obj==ref[0] for ref in self.refs+list(self.links.values())):
            # Document deletion tears down native views before all object
            # notifications finish. Let its document callback own that cleanup.
            QtCore.QTimer.singleShot(0,self.reject)

    def pick_region(self,callback):
        event=callback.getEvent()
        if (self.closed or self.pick!='profile' or not self.refs
                or event.getState()!=coin.SoButtonEvent.DOWN or event.getButton()!=coin.SoMouseButtonEvent.BUTTON1
                or event.wasCtrlDown() or event.wasShiftDown()):return
        try:
            self.check()
            if not self.require_target():return
            position=event.getPosition();x,y=int(position[0]),int(position[1])
            hit=self.view.getObjectInfo((x,y))
            if hit and str(hit.get('Component','')).startswith(('Edge','Vertex')):return
            sketch=self.refs[0][0]
            if not sketch.isDerivedFrom('Sketcher::SketchObject'):return
            frame=self.owner.getGlobalPlacement().inverse().multiply(sketch.getGlobalPlacement())
            world=hierarchy.world_placement(self.doc,self.path) if self.path else App.Placement()
            frame=world.multiply(frame)
            point=self.view.getPoint(x,y)
            camera=self.view.getCameraNode()
            if camera.isOfType(coin.SoPerspectiveCamera.getClassTypeId()):
                eye=App.Vector(*camera.position.getValue().getValue());direction=point-eye
            else:direction=self.view.getCameraOrientation().multVec(App.Vector(0,0,-1))
            normal=frame.Rotation.multVec(App.Vector(0,0,1));denominator=normal.dot(direction)
            if abs(denominator)<1e-9:return
            point += direction*((frame.Base-point).dot(normal)/denominator)
            refs=self.engine.region_references(self.owner,sketch,world.inverse().multVec(point))
            if refs:
                self.refs=refs;self.refresh_fields();self.changed();callback.setHandled()
        except (ValueError,RuntimeError):pass

    def load_feature(self,feature):
        self.refs = planes.flatten(feature.ProfileReferences)
        self.links = self.engine.references(feature)
        v = self.engine.settings(feature)
        if self.outputs:self.outputs[v.get('output', 'Solid')].setChecked(True)
        self.modes[v['operation']].setChecked(True)
        for widget,key in ((self.start_type,'start'),(self.sides,'sides'),(self.direction,'direction'),(self.measure,'measure'),
                           (self.end1['kind'],'end'),(self.end2['kind'],'end2')):
            widget.setCurrentText(v[key])
        for widget,key in ((self.start_offset,'start_offset'),(self.end1['length'],'length'),(self.end2['length'],'length2'),
                           (self.end1['offset'],'offset'),(self.end2['offset'],'offset2'),(self.taper,'taper'),(self.taper2,'taper2')):
            widget.setValue(v[key]);self.values[widget] = v[key]
        self.reverse.setChecked(v['reverse']);self.refine.setChecked(v['refine'])

    def settings(self):
        return dict(output=self.output(),operation=self.mode(),start=self.start_type.currentText(),start_offset=self.values[self.start_offset],
                    sides=self.sides.currentText(),end=self.end1['kind'].currentText(),end2=self.end2['kind'].currentText(),
                    length=self.values[self.end1['length']],length2=self.values[self.end2['length']],
                    offset=self.values[self.end1['offset']],offset2=self.values[self.end2['offset']],
                    reverse=self.reverse.isChecked(),direction=self.direction.currentText(),measure=self.measure.currentText(),
                    taper=self.values[self.taper],taper2=self.values[self.taper2],refine=self.refine.isChecked())

    def section(self, layout, title, expanded=True):
        section = Section(title,expanded); layout.addWidget(section)
        QtWidgets.QWidget.layout(section).setSpacing(1)
        QtWidgets.QWidget.layout(section).setContentsMargins(0,1,0,1)
        section.layout.setContentsMargins(6,0,0,2); section.layout.setSpacing(4)
        return section

    def combo(self, layout, title, options):
        row = QtWidgets.QHBoxLayout(); row.addWidget(QtWidgets.QLabel(title))
        widget = QtWidgets.QComboBox(); widget.addItems(options); row.addWidget(widget,1)
        layout.addLayout(row); widget.currentTextChanged.connect(self.changed)
        return widget

    def numeric(self, layout, title, value, suffix=' mm'):
        holder = QtWidgets.QWidget(); inner = QtWidgets.QVBoxLayout(holder); inner.setContentsMargins(0,0,0,0)
        field = number(inner,title,value,suffix); layout.addWidget(holder)
        self.numbers.append(field); self.values[field] = value
        field.committed.connect(self.commit_numbers)
        return holder, field

    def reference(self, layout, title, key, placeholder):
        holder = QtWidgets.QWidget(); box = QtWidgets.QVBoxLayout(holder); box.setContentsMargins(0,0,0,0); box.setSpacing(2)
        box.addWidget(QtWidgets.QLabel(title)); row = QtWidgets.QHBoxLayout()
        field = QtWidgets.QLineEdit(); field.setReadOnly(True); field.setPlaceholderText(placeholder)
        field.installEventFilter(self); self.fields[key] = field
        row.addWidget(field,1)
        clear = QtWidgets.QPushButton('Clear'); clear.clicked.connect(lambda: self.clear_reference(key)); row.addWidget(clear)
        box.addLayout(row); layout.addWidget(holder)
        return holder

    def end_controls(self, layout, key):
        end = self.combo(layout,'End',['Length','Up to face','Up to shape','To first','To last','Through all'])
        length_row, length = self.numeric(layout,'Length',8 if not key else 3)
        length.setMinimum(.01)
        limit_row = self.reference(layout,'Limit',key+'limit','Pick a limiting face, plane or shape')
        offset_row, offset = self.numeric(layout,'End offset',0)
        return dict(kind=end,length=length,length_row=length_row,limit_row=limit_row,offset_row=offset_row,offset=offset,key=key+'limit')

    def mode(self):
        return next(name for name,button in self.modes.items() if button.isChecked())

    def output(self):
        return 'Sheet' if self.outputs and self.outputs['Sheet'].isChecked() else 'Solid'

    def update_output(self):
        if not self.outputs:return
        sheet = self.output() == 'Sheet'
        switching = getattr(self, 'output_mode', None) != sheet
        self.output_mode = sheet
        if sheet:
            self.modes['New Solid'].setChecked(True)
            self.links.pop('target', None); self.automatic_target = None
            if self.pick == 'target':self.pick = 'profile'
        for button in self.modes.values():button.setEnabled(not sheet)
        self.profile_hint.setText('Select sketch curves or edges. Open curves create sheets.' if sheet else
                                  'Select a sketch, closed sketch region, or face.')
        with QtCore.QSignalBlocker(self.display):
            self.display.setItemText(0, 'Extrusion preview' if sheet else 'Tool volume')
        for end in (self.end1, self.end2):
            if sheet and end['kind'].currentIndex() >= 3:
                with QtCore.QSignalBlocker(end['kind']):end['kind'].setCurrentIndex(0)
            for index in (3, 4, 5):
                end['kind'].model().item(index).setEnabled(not sheet)
        if switching:self.refresh_fields()

    def eventFilter(self, obj, event):
        if event.type() in (QtCore.QEvent.FocusIn,QtCore.QEvent.MouseButtonPress):
            self.pick = next((key for key,field in self.fields.items() if obj is field),'profile')
            if self.presentation:self.presentation.update_style()
        if event.type() in (QtCore.QEvent.ShortcutOverride,QtCore.QEvent.KeyPress) and event.key()==QtCore.Qt.Key_Delete:
            event.accept()
            if event.type()==QtCore.QEvent.KeyPress:
                if obj is self.profiles:self.remove_profile()
                else:self.clear_reference(self.pick)
            return True
        return False

    def focus_changed(self, old, current):
        if self.closed or current is None or not self.form.isAncestorOf(current):return
        # Clicking the viewport/tree continues the active picker. Moving to any
        # other task control ends target picking, including the Length editor.
        self.pick = next((key for key,field in self.fields.items()
                          if current is field or field.isAncestorOf(current)), 'profile')
        self.presentation.update_style()

    def refresh_fields(self):
        self.profiles.clear()
        for obj,sub in self.refs:
            element = Part.splitSubname(sub)[2]
            self.profiles.addItem(obj.Label + ' · ' + (element or ('Whole sketch' if obj.isDerivedFrom('Sketcher::SketchObject') else 'All curves')))
        for key,field in self.fields.items():
            ref = self.links.get(key)
            field.setText(ref[0].Label+('.'+Part.splitSubname(ref[1])[2] if Part.splitSubname(ref[1])[2] else '') if ref else '')

    def clear_reference(self,key):
        self.links.pop(key,None)
        if key=='target':self.automatic_target=None
        self.refresh_fields();self.changed()
        if key=='target' and self.mode()!='New Solid':self.focus_target()

    def valid_target(self, target):
        """An edited feature may retain its saved predecessor inside its Body."""
        if target is None:return False
        try:
            document.require_predecessors(self.owner,self.feature,[(target,'')])
            saved=self.engine.references(self.feature).get('target',(None,''))[0] if self.feature else None
            if target==saved and target is not None:
                return (document.owned_path(self.owner,target) is not None
                        and not target.Shape.isNull() and target.Shape.isValid()
                        and len(target.Shape.Solids)==1 and 'Invalid' not in target.State)
            modeling._target_body(self.owner,target)
            return True
        except (ValueError,RuntimeError,ReferenceError,AttributeError):return False

    def target_candidates(self):
        # One result per Body; never count hidden historical stages as solids.
        return [body.Tip for body in self.owner.Group if body.TypeId=='PartDesign::Body'
                and body.Tip is not None and self.valid_target(body.Tip)]

    def focus_target(self):
        if self.closed or self.mode()=='New Solid':return
        self.fields['target'].setFocus()
        self.pick='target'
        self.presentation.update_style();self.refresh_target()

    def target_ready(self):
        return self.mode()=='New Solid' or self.valid_target(self.links.get('target',(None,''))[0])

    def require_target(self):
        if self.target_ready():return True
        self.update_target();self.focus_target();self.set_ok(False)
        return False

    def update_target(self):
        mode=self.mode();entering=mode!=self.target_mode;self.target_mode=mode
        self.target_row.setVisible(mode!='New Solid')
        if mode=='New Solid':
            if self.pick=='target':self.pick='profile'
            return
        target=self.links.get('target',(None,''))[0]
        if target is not None and not self.valid_target(target):
            self.links.pop('target',None);self.automatic_target=None;target=None
            self.refresh_fields()
        candidates=self.target_candidates() if target is None else []
        # Only operation entry selects automatically. Clear remains a deliberate
        # empty selection through numeric changes and preview refreshes.
        if entering and target is None and len(candidates)==1:
            target=candidates[0];self.links['target']=(target,'');self.automatic_target=target
            self.refresh_fields();self.profiles.setFocus();self.pick='profile'
        missing=target is None
        self.fields['target'].setStyleSheet(
            'QLineEdit { border: 2px solid #bd780b; border-radius: 3px; background: #fff3d6; }' if missing else '')
        self.target_hint.setText(('Choose a target solid before selecting curves.' if candidates else
                                 'No solid is available to modify. Create a new solid first.') if missing else
                                'Only solid selected automatically.' if target==self.automatic_target else '')
        self.target_hint.setStyleSheet('color: #875300;' if missing else 'color: #4d5965;')
        if entering and missing:QtCore.QTimer.singleShot(0,self.focus_target)

    def clear_profile(self):
        self.refs=[];self.refresh_fields();self.changed()

    def remove_profile(self):
        row=self.profiles.currentRow()
        if row>=0:self.refs.pop(row)
        self.refresh_fields();self.changed()

    def whole_profile(self):
        if self.refs and self.refs[0][0].isDerivedFrom('Sketcher::SketchObject'):
            self.refs=[(self.refs[0][0],'')]
        self.refresh_fields();self.changed()

    def addSelection(self,doc,name,sub,*args):
        if self.closed:return
        try:
            self.check()
            if self.pick=='profile' and not self.require_target():
                Gui.Selection.removeSelection(doc,name,sub)
                return
            obj=App.getDocument(doc).getObject(name)
            ref=planes.canonical(self.owner,[(obj,sub)])[0]
            document.require_predecessors(self.owner,self.feature,[ref])
            if self.pick=='profile':
                ref=self.engine.profile_reference(ref)
                if self.engine is extrusion:self.engine.validate_profiles(self.owner,[ref],self.output())
                else:self.engine.validate_profiles(self.owner,[ref])
                if ref in self.refs:self.refs.remove(ref)
                elif self.refs and (ref[0]!=self.refs[0][0] or (not ref[0].isDerivedFrom('Sketcher::SketchObject')
                                      and not (self.output()=='Sheet' and Part.splitSubname(ref[1])[2].startswith('Edge')
                                               and all(Part.splitSubname(old[1])[2].startswith('Edge') for old in self.refs)))):
                    raise ValueError('Use curves from one object or one face; clear the current profile first.' if self.output()=='Sheet' else
                                     'Use one sketch or one face; clear the current profile first.')
                else:
                    self.refs = [old for old in self.refs if old[1] and ref[1]]
                    self.refs.append(ref)
            else:
                if self.pick=='target':
                    target=ref[0].Tip if ref[0].TypeId=='PartDesign::Body' else ref[0]
                    if not self.valid_target(target):raise ValueError('Choose an eligible predecessor solid.')
                    self.automatic_target=None
                    ref=(target,'')
                self.links[self.pick]=ref
            self.refresh_fields();self.changed()
            Gui.Selection.removeSelection(obj,sub)
        except Exception as exc:self.status.setError(str(exc))

    def commit_numbers(self):
        changed=False
        for field in self.numbers:
            # A spin step commits its sender while focus remains in that field.
            if field.hasFocus() and field is not self.sender():continue
            value=field.value()
            if self.values[field]!=value:self.values[field]=value;changed=True
        if changed:self.changed()

    def changed(self,*args):
        if not self.ready or self.closed:return
        self.update_output()
        self.presentation.update_usable()
        self.update_target()
        self.presentation.update_style()
        two=self.sides.currentText()=='Two sides'
        self.second.setVisible(two);self.taper2_row.setVisible(two)
        self.start_row.setVisible(self.start_type.currentText()=='Reference')
        self.start_offset_row.setVisible(self.start_type.currentText()!='Profile plane')
        self.direction_row.setVisible(self.direction.currentIndex()==1)
        self.direction_label.setText('Direction: '+self.direction.currentText())
        self.measure.setEnabled(self.direction.currentIndex()==1)
        for end in (self.end1,self.end2):
            kind=end['kind'].currentText()
            end['length_row'].setVisible(kind=='Length')
            end['limit_row'].setVisible(kind in ('Up to face','Up to shape'))
            end['offset_row'].setVisible(kind in ('Up to face','Up to shape','To first','To last'))
        title=self.end1['length_row'].findChild(QtWidgets.QLabel)
        title.setText('Total length' if self.sides.currentText()=='Symmetric' else 'Length')
        self.start.header.setText('Start · '+self.start_type.currentText())
        if self.automatic.isChecked():self.render()
        else:
            # Retain the last evaluated shapes for callers, but do not display
            # a stale green/red volume for inputs waiting on Update preview.
            self.clear_overlay()
            self.status.setText('Preview needs update.')
            # OK revalidates current inputs even when automatic preview is off.
            self.set_ok(self.target_ready())
        self.refresh_target()

    def clear_overlay(self):
        self.tool_preview = None
        self.showing_result = False
        self.profile_highlight = None
        self.hidden_objects = []
        if self.overlay is not None:
            if self.scene.findChild(self.overlay)>=0:self.scene.removeChild(self.overlay)
            self.overlay=None
        if self.hidden:
            self.hidden=False
            display.task_hidden(self.view)
            try:
                session=isolation.current(self.view)
                if session:session._apply_display(self.owner)
                else:display.apply_hidden(self.view,document.validate(self.doc),display.hidden_paths(self.doc,self.owner,self.path))
            except (ValueError,RuntimeError,ReferenceError):
                if not self.closed:raise

    def hide_results(self,objects):
        self.hidden_objects = list(objects)
        paths=[]
        session=isolation.current(self.view)
        if session:
            root=self.owner;paths=list(display.unused_hidden_paths(root));prefix=''
        else:
            root=document.validate(self.doc)
            prefix=hierarchy.subname(self.path) if self.path else ''
            if root!=self.owner and not prefix:return
        for obj in objects:
            if (obj in self.presentation.manual and self.presentation.desired.get(obj)):
                continue
            if obj is not None and obj.Visibility:
                route=document.owned_path(self.owner,obj)
                paths.append(prefix+''.join(child.Name+'.' for child in route))
        self.hidden=True
        display.task_hidden(self.view,root,paths,preview=bool(session))
        if session:session._apply_display(self.owner)
        else:display.apply_hidden(self.view,root,display.hidden_paths(self.doc,self.owner,self.path))

    def clear_target(self):
        if self.target_overlay is not None:
            if self.scene.findChild(self.target_overlay)>=0:self.scene.removeChild(self.target_overlay)
            self.target_overlay=None

    def refresh_target(self):
        # Selection presentation is independent of History Visibility and of
        # tool recomputation/Show preview. No source property is revealed.
        if not self.ready or self.closed:return
        self.clear_target()
        try:
            self.check()
            self.hide_results(self.hidden_objects)
            target=self.links.get('target') if self.mode()!='New Solid' else None
            if target is None or self.showing_result:
                return
            route=document.owned_path(self.owner,target[0])
            if route is None:return
            # A visible target already has the selected material and remains
            # natively pickable for face/edge references. Supplement only hidden
            # routes instead of replacing their selectable representation.
            if all(member.Visibility for member in route):return
            shape=planes.shape(self.owner,target)
            if shape.isNull() or not shape.Solids:return
            self.world=hierarchy.world_placement(self.doc,self.path) if self.path else App.Placement()
            node=coin.SoSeparator();pick=coin.SoPickStyle();pick.style=coin.SoPickStyle.UNPICKABLE;node.addChild(pick)
            packed=App.ParamGet('User parameter:BaseApp/Preferences/View').GetUnsigned('SelectionColor',0x1CAD1CFF)
            color=tuple(((packed>>shift)&255)/255. for shift in (24,16,8))
            self.add_shape(shape,color,0 if self.pick=='target' else .65,parent=node)
            self.scene.addChild(node);self.target_overlay=node
        except (ValueError,RuntimeError,ReferenceError):
            pass  # Context/deletion cleanup owns closing the task.

    def show_tool(self, tool, valid):
        colors={'New Solid':(.2,.45,.95),
                'Add':(.15,.75,.3) if valid else (1.,.82,.08),
                'Subtract':(.95,.22,.22) if valid else (1.,.4,.7)}
        # Draw after transparent scene geometry so the selected target cannot
        # tint a red cut volume purple. Keep the native shaded volume.
        self.tool_preview=coin.SoAnnotation();self.overlay.addChild(self.tool_preview)
        self.add_shape(tool,colors[self.mode()],.4 if self.mode()=='New Solid' else .15,
                       True,parent=self.tool_preview)

    def add_shape(self,shape,color,transparency=0,top=False,parent=None):
        shape=shape.copy()
        shape.Placement=self.world.multiply(shape.Placement)
        branch=coin.SoSeparator()
        if top:
            depth=coin.SoDepthBuffer();depth.test=False;depth.write=False;branch.addChild(depth)
        # Declare solid winding so rear triangles cannot bleed through front faces.
        # Sort transparent triangles consistently, including the through-model tool overlay.
        hints=coin.SoShapeHints();hints.vertexOrdering=coin.SoShapeHints.COUNTERCLOCKWISE
        hints.shapeType=coin.SoShapeHints.SOLID if shape.Solids else coin.SoShapeHints.UNKNOWN_SHAPE_TYPE
        branch.addChild(hints)
        sorting=coin.SoTransparencyType()
        sorting.value=coin.SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND
        branch.addChild(sorting)
        material=coin.SoMaterial();material.diffuseColor=color;material.transparency=transparency;branch.addChild(material)
        vertices,faces=shape.tessellate(.2)
        coords=coin.SoCoordinate3();coords.point.setValues(0,len(vertices),[tuple(p) for p in vertices]);branch.addChild(coords)
        mesh=coin.SoIndexedFaceSet();indices=[i for face in faces for i in (*face,-1)]
        mesh.coordIndex.setValues(0,len(indices),indices);branch.addChild(mesh)
        (self.overlay if parent is None else parent).addChild(branch)

    def set_ok(self, enabled):
        for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox):
            button=box.button(QtWidgets.QDialogButtonBox.Ok)
            if button and button.isVisible():button.setEnabled(enabled)

    def highlight_profile(self):
        if self.profile_highlight is not None and self.overlay is not None:
            if self.overlay.findChild(self.profile_highlight)>=0:self.overlay.removeChild(self.profile_highlight)
            self.profile_highlight=None
        if not self.refs or self.overlay is None:return
        highlight=coin.SoSeparator()
        if self.feature:
            for ref in self.refs:
                if (not ref[0].isDerivedFrom('Sketcher::SketchObject')
                        and not (ref[0] in self.presentation.manual and not self.presentation.desired.get(ref[0]))):
                    self.add_shape(planes.shape(self.owner,ref),(.65,.68,.70),parent=highlight)
        depth=coin.SoDepthBuffer();depth.test=False;depth.write=False;highlight.addChild(depth)
        ink=coin.SoMaterial();ink.diffuseColor=(1,.6,.08);highlight.addChild(ink)
        style=coin.SoDrawStyle();style.lineWidth=3;highlight.addChild(style)
        for ref in self.refs:
            if ref[0] in self.presentation.manual and not self.presentation.desired.get(ref[0]):continue
            if not self.feature and not all(member.Visibility for member in document.owned_path(self.owner,ref[0])):
                continue
            for edge in planes.shape(self.owner,ref).Edges:
                points=edge.discretize(60)
                coords=coin.SoCoordinate3()
                coords.point.setValues(0,len(points),[tuple(self.world.multVec(p)) for p in points])
                highlight.addChild(coords)
                line=coin.SoLineSet();line.numVertices.setValue(len(points));highlight.addChild(line)
        self.overlay.addChild(highlight)
        self.profile_highlight=highlight

    def refresh_visibility(self):
        # Eye clicks update display only, including when automatic recompute is
        # off. They must not evaluate uncommitted/changed operation parameters.
        if self.hidden:self.hide_results(self.hidden_objects)
        self.highlight_profile()
        self.refresh_target()

    def render(self,*args):
        if self.closed:return
        self.update_output()
        self.update_target()
        self.clear_overlay();self.valid=False
        self.result_shape=None;self.tool_shape=None
        try:
            self.check()
            self.world=hierarchy.world_placement(self.doc,self.path) if self.path else App.Placement()
            self.overlay=coin.SoSeparator()
            pick=coin.SoPickStyle();pick.style=coin.SoPickStyle.UNPICKABLE;self.overlay.addChild(pick)
            self.highlight_profile()
            result,tool,_=self.engine.evaluate(self.owner,self.refs,self.links,self.settings(),self.feature)
            self.result_shape=result;self.tool_shape=tool
            self.valid=True;self.revisions+=1
            target=self.links.get('target',(None,''))[0] if self.mode()!='New Solid' else None
            self.status.setText(('Sheet preview · %d face%s, no thickness.' % (len(result.Faces), '' if len(result.Faces)==1 else 's'))
                                if self.output()=='Sheet' else 'Result preview · one solid.' if self.display.currentText()=='Result' else
                                'Tool volume · '+('creates a separate solid.' if target is None else
                                ('adds to ' if self.mode()=='Add' else 'removes from ')+target.Label+'.'))
            if self.visible.isChecked():
                hidden=[self.feature] if self.feature else []
                if self.display.currentText()=='Result':
                    hidden.append(target)
                    self.add_shape(result,(.65,.68,.70))
                    self.showing_result=True
                else:
                    self.show_tool(tool,True)
                for end in (self.end1,self.end2) if self.sides.currentText()=='Two sides' else (self.end1,):
                    if end['kind'].currentText() in ('Up to face','Up to shape') and end['key'] in self.links:
                        limit=planes.shape(self.owner,self.links[end['key']])
                        if limit.BoundBox.DiagonalLength<1e6:
                            self.add_shape(limit,(.65,.4,.85),.8)
                self.hide_results(hidden)
        except self.engine.InvalidResult as exc:
            self.tool_shape=exc.tool
            self.status.setError(str(exc))
            if self.visible.isChecked():
                self.show_tool(exc.tool,False)
                self.hide_results([self.feature] if self.feature else [])
        except Exception as exc:
            self.valid=False;self.status.setError(str(exc))
        if self.overlay is not None:self.scene.addChild(self.overlay)
        self.set_ok(self.valid)
        self.refresh_target()

    def getStandardButtons(self):return QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel
    def accept(self):
        try:
            self.check()
            self.update_output()
            if not self.require_target():return False
            for field in self.numbers:
                field.interpretText();self.values[field]=field.value()
            self.clear_overlay()
            self.clear_target()
            self.presentation.restore()
            self.result=self.engine.save(self.doc,self.refs,self.links,self.settings(),self.feature)
            self.reject()
            return True
        except Exception as exc:
            self.presentation.apply()
            self.render()
            self.status.setError(str(exc));return False

    def reject(self,document_closing=False):
        global _active
        if not self.closed:
            self.closed=True
            if _active is self:_active=None
            Gui.Selection.removeObserver(self)
            App.removeDocumentObserver(self)
            editing.remove_context_observer(self.context_changed)
            QtWidgets.QApplication.instance().focusChanged.disconnect(self.focus_changed)
            self.presentation.restore()
            if document_closing:
                display.task_hidden(self.view)
                self.hidden=False
            try:
                self.clear_overlay()
                self.clear_target()
            except (RuntimeError,ReferenceError,ValueError):pass
            if not document_closing:
                try:self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),self.mouse_callback)
                except (RuntimeError,ReferenceError):pass
            Gui.Control.closeDialog()
            from . import panel
            panel.end_feature_task(self)
        return True


def show(feature=None, which='Pad'):
    global _active
    if Gui.Control.activeDialog():
        raise ValueError('Finish the current task first.')
    if feature is not None and not extrusion.is_extrusion(feature):
        raise ValueError('This feature uses the native editor.')
    _active=ExtrudeTask(feature,which)
    Gui.Control.showDialog(_active);_active.changed()
    from . import panel
    panel.begin_feature_task(_active)
    return _active


def dispatch(which):
    # Component workflows are shared by both task presentations. Native
    # body-owned sketches retain their existing command compatibility.
    definition,_=modeling._context(Gui.activeDocument().Document)
    selected=Gui.Selection.getSelection('*')
    if any(obj.isDerivedFrom('Sketcher::SketchObject') and obj.getParentGeoFeatureGroup()!=definition
           for obj in selected):return False
    show(which=which)
    return True
