# SPDX-License-Identifier: LGPL-2.1-or-later
"""Approved shared Extrude creation/editing task; no model writes before OK."""
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtWidgets
from pivy import coin
from freecad_plus import modeling, planes, extrusion, document, editing, hierarchy, isolation, display
from freecad_plus.plane_task import Section, label, number, buttons


_active = None


class ExtrudeTask(QtCore.QObject):
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
        self.closed = False
        self.ready = False
        self.revisions = 0
        self.valid = False
        self.pick = 'profile'
        self.refs = []
        self.links = {}
        self.fields = {}
        self.numbers = []
        self.values = {}
        self.hidden = False
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle('Extrude')
        self.form.setWindowIcon(Gui.getIcon('PartDesign_Pad'))
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
        self.operation.layout.addLayout(row)
        self.target_row = self.reference(self.operation.layout,'Target solid','target','Pick the current solid to modify')
        self.profile = self.section(layout, 'Profile')
        self.profile.layout.addWidget(label('Select a sketch, curves, or a closed region.'))
        self.profiles = QtWidgets.QListWidget(); self.profiles.setFixedHeight(36)
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
        self.status = label('Select a profile.'); layout.addWidget(self.status); layout.addStretch()
        if feature is not None:
            self.load_feature(feature)
        else:
            raw = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('*',0) for sub in entry.SubElementNames or ('',)]
            for obj,sub in planes.canonical(self.owner,raw):
                if obj.isDerivedFrom('Sketcher::SketchObject'):
                    self.refs.append((obj,sub))
                elif obj.TypeId == 'PartDesign::Body' or obj.isDerivedFrom('PartDesign::Feature'):
                    target = obj.Tip if obj.TypeId == 'PartDesign::Body' else obj
                    modeling._target_body(self.owner,target)
                    if 'target' in self.links and self.links['target'][0] != target:
                        raise ValueError('Select one target solid.')
                    self.links['target'] = (target,'')
            self.modes['Subtract' if which == 'Pocket' else 'Add' if 'target' in self.links else 'New Solid'].setChecked(True)
        Gui.Selection.clearSelection()
        Gui.Selection.addObserver(self,0)
        App.addDocumentObserver(self)
        editing.add_context_observer(self.context_changed)
        self.mouse_callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.pick_region)
        self.ready = True
        self.refresh_fields()

    def check(self):
        if self.closed or Gui.activeDocument() is None or Gui.activeDocument().activeView() != self.view:
            raise ValueError('Return to the view where Extrude was opened.')
        definition,path = modeling._context(self.doc)
        if modeling._routing_context(self.doc,definition,path) != self.context:
            raise ValueError('The edited component changed; start Extrude again.')

    def context_changed(self):
        if self.closed:return
        try:self.check()
        except Exception:self.reject()

    def slotDeletedDocument(self,doc):
        if doc in (self.doc,self.source_doc):self.reject(document_closing=True)

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
            position=event.getPosition();x,y=int(position[0]),int(position[1])
            hit=self.view.getObjectInfo((x,y))
            if hit and str(hit.get('Component','')).startswith(('Edge','Vertex')):return
            sketch=self.refs[0][0]
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
            refs=extrusion.region_references(self.owner,sketch,world.inverse().multVec(point))
            if refs:
                self.refs=refs;self.refresh_fields();self.changed();callback.setHandled()
        except (ValueError,RuntimeError):pass

    def load_feature(self,feature):
        self.refs = planes.flatten(feature.ProfileReferences)
        self.links = extrusion.references(feature)
        v = extrusion.settings(feature)
        self.modes[v['operation']].setChecked(True)
        for widget,key in ((self.start_type,'start'),(self.sides,'sides'),(self.direction,'direction'),(self.measure,'measure'),
                           (self.end1['kind'],'end'),(self.end2['kind'],'end2')):
            widget.setCurrentText(v[key])
        for widget,key in ((self.start_offset,'start_offset'),(self.end1['length'],'length'),(self.end2['length'],'length2'),
                           (self.end1['offset'],'offset'),(self.end2['offset'],'offset2'),(self.taper,'taper'),(self.taper2,'taper2')):
            widget.setValue(v[key]);self.values[widget] = v[key]
        self.reverse.setChecked(v['reverse']);self.refine.setChecked(v['refine'])

    def settings(self):
        return dict(operation=self.mode(),start=self.start_type.currentText(),start_offset=self.values[self.start_offset],
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

    def eventFilter(self, obj, event):
        if event.type() in (QtCore.QEvent.FocusIn,QtCore.QEvent.MouseButtonPress):
            self.pick = next((key for key,field in self.fields.items() if obj is field),'profile')
        if event.type() in (QtCore.QEvent.ShortcutOverride,QtCore.QEvent.KeyPress) and event.key()==QtCore.Qt.Key_Delete:
            event.accept()
            if event.type()==QtCore.QEvent.KeyPress:
                if obj is self.profiles:self.remove_profile()
                else:self.clear_reference(self.pick)
            return True
        return False

    def refresh_fields(self):
        self.profiles.clear()
        for obj,sub in self.refs:
            element = Part.splitSubname(sub)[2]
            self.profiles.addItem(obj.Label + (' · '+element if element else ' · Whole sketch'))
        for key,field in self.fields.items():
            ref = self.links.get(key)
            field.setText(ref[0].Label+('.'+Part.splitSubname(ref[1])[2] if Part.splitSubname(ref[1])[2] else '') if ref else '')

    def clear_reference(self,key):
        self.links.pop(key,None);self.refresh_fields();self.changed()

    def clear_profile(self):
        self.refs=[];self.refresh_fields();self.changed()

    def remove_profile(self):
        row=self.profiles.currentRow()
        if row>=0:self.refs.pop(row)
        self.refresh_fields();self.changed()

    def whole_profile(self):
        if self.refs:self.refs=[(self.refs[0][0],'')]
        self.refresh_fields();self.changed()

    def addSelection(self,doc,name,sub,*args):
        if self.closed:return
        try:
            self.check()
            obj=App.getDocument(doc).getObject(name)
            ref=planes.canonical(self.owner,[(obj,sub)])[0]
            if self.pick=='profile':
                if not ref[0].isDerivedFrom('Sketcher::SketchObject'):raise ValueError('Select a sketch or its closed curves.')
                if ref in self.refs:self.refs.remove(ref)
                elif self.refs and ref[0]!=self.refs[0][0]:raise ValueError('Use curves from one sketch.')
                else:
                    self.refs = [old for old in self.refs if old[1] and ref[1]]
                    self.refs.append(ref)
            else:
                if self.pick=='target':
                    target=ref[0].Tip if ref[0].TypeId=='PartDesign::Body' else ref[0]
                    saved=extrusion.references(self.feature).get('target',(None,''))[0] if self.feature else None
                    if target!=saved:modeling._target_body(self.owner,target)
                    ref=(target,'')
                self.links[self.pick]=ref
            self.refresh_fields();self.changed()
            Gui.Selection.removeSelection(obj,sub)
        except Exception as exc:self.status.setText(str(exc))

    def commit_numbers(self):
        changed=False
        for field in self.numbers:
            if field.hasFocus():continue
            value=field.value()
            if self.values[field]!=value:self.values[field]=value;changed=True
        if changed:self.changed()

    def changed(self,*args):
        if not self.ready or self.closed:return
        self.target_row.setVisible(self.mode()!='New Solid')
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
            if not self.visible.isChecked():self.clear_overlay()
            self.status.setText('Preview needs update.')
            # OK revalidates current inputs even when automatic preview is off.
            self.set_ok(True)

    def clear_overlay(self):
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
        paths=[]
        session=isolation.current(self.view)
        if session:
            root=self.owner;paths=list(display.unused_hidden_paths(root));prefix=''
        else:
            root=document.validate(self.doc)
            prefix=hierarchy.subname(self.path) if self.path else ''
            if root!=self.owner and not prefix:return
        for obj in objects:
            if obj is not None and obj.Visibility:
                route=document.owned_path(self.owner,obj)
                paths.append(prefix+''.join(child.Name+'.' for child in route))
        self.hidden=True
        display.task_hidden(self.view,root,paths,preview=bool(session))
        if session:session._apply_display(self.owner)
        else:display.apply_hidden(self.view,root,display.hidden_paths(self.doc,self.owner,self.path))

    def add_shape(self,shape,color,transparency=0,top=False):
        shape=shape.copy()
        shape.Placement=self.world.multiply(shape.Placement)
        branch=coin.SoSeparator()
        if top:
            depth=coin.SoDepthBuffer();depth.test=False;depth.write=False;branch.addChild(depth)
        material=coin.SoMaterial();material.diffuseColor=color;material.transparency=transparency;branch.addChild(material)
        vertices,faces=shape.tessellate(.2)
        coords=coin.SoCoordinate3();coords.point.setValues(0,len(vertices),[tuple(p) for p in vertices]);branch.addChild(coords)
        mesh=coin.SoIndexedFaceSet();indices=[i for face in faces for i in (*face,-1)]
        mesh.coordIndex.setValues(0,len(indices),indices);branch.addChild(mesh)
        self.overlay.addChild(branch)

    def set_ok(self, enabled):
        for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox):
            button=box.button(QtWidgets.QDialogButtonBox.Ok)
            if button and button.isVisible():button.setEnabled(enabled)

    def highlight_profile(self):
        if not self.refs or self.overlay is None:return
        highlight=coin.SoSeparator()
        depth=coin.SoDepthBuffer();depth.test=False;depth.write=False;highlight.addChild(depth)
        ink=coin.SoMaterial();ink.diffuseColor=(1,.6,.08);highlight.addChild(ink)
        style=coin.SoDrawStyle();style.lineWidth=3;highlight.addChild(style)
        for ref in self.refs:
            for edge in planes.shape(self.owner,ref).Edges:
                points=edge.discretize(60)
                coords=coin.SoCoordinate3()
                coords.point.setValues(0,len(points),[tuple(self.world.multVec(p)) for p in points])
                highlight.addChild(coords)
                line=coin.SoLineSet();line.numVertices.setValue(len(points));highlight.addChild(line)
        self.overlay.addChild(highlight)

    def render(self,*args):
        if self.closed:return
        self.clear_overlay();self.valid=False
        try:
            self.check()
            self.world=hierarchy.world_placement(self.doc,self.path) if self.path else App.Placement()
            if self.visible.isChecked():
                self.overlay=coin.SoSeparator()
                pick=coin.SoPickStyle();pick.style=coin.SoPickStyle.UNPICKABLE;self.overlay.addChild(pick)
                self.highlight_profile()
            result,tool,_=extrusion.evaluate(self.owner,self.refs,self.links,self.settings(),self.feature)
            self.result_shape=result;self.tool_shape=tool
            self.valid=True;self.revisions+=1
            target=self.links.get('target',(None,''))[0] if self.mode()!='New Solid' else None
            self.status.setText('Result preview · one solid.' if self.display.currentText()=='Result' else
                                'Tool volume · '+('creates a separate solid.' if target is None else
                                ('adds to ' if self.mode()=='Add' else 'removes from ')+target.Label+'.'))
            if self.overlay is not None:
                hidden=[self.feature] if self.feature else []
                if self.display.currentText()=='Result':
                    hidden.append(target)
                    self.add_shape(result,(.65,.68,.70))
                else:
                    self.add_shape(tool,{'New Solid':(.2,.45,.95),'Add':(.15,.75,.3),'Subtract':(.95,.22,.22)}[self.mode()],.4,True)
                for end in (self.end1,self.end2) if self.sides.currentText()=='Two sides' else (self.end1,):
                    if end['kind'].currentText() in ('Up to face','Up to shape') and end['key'] in self.links:
                        limit=planes.shape(self.owner,self.links[end['key']])
                        if limit.BoundBox.DiagonalLength<1e6:
                            self.add_shape(limit,(.65,.4,.85),.8)
                self.hide_results(hidden)
        except Exception as exc:
            self.valid=False;self.status.setText(str(exc))
        if self.overlay is not None:self.scene.addChild(self.overlay)
        self.set_ok(self.valid)

    def getStandardButtons(self):return QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel
    def accept(self):
        try:
            self.check()
            for field in self.numbers:
                field.interpretText();self.values[field]=field.value()
            self.clear_overlay()
            self.result=extrusion.save(self.doc,self.refs,self.links,self.settings(),self.feature)
            self.reject()
            return True
        except Exception as exc:
            self.status.setText(str(exc));return False

    def reject(self,document_closing=False):
        global _active
        if not self.closed:
            self.closed=True
            if _active is self:_active=None
            Gui.Selection.removeObserver(self)
            App.removeDocumentObserver(self)
            editing.remove_context_observer(self.context_changed)
            if document_closing:
                display.task_hidden(self.view)
                self.hidden=False
            try:self.clear_overlay()
            except (RuntimeError,ReferenceError,ValueError):pass
            if not document_closing:
                try:self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),self.mouse_callback)
                except (RuntimeError,ReferenceError):pass
            Gui.Control.closeDialog()
        return True


def show(feature=None, which='Pad'):
    global _active
    if Gui.Control.activeDialog():
        raise ValueError('Finish the current task first.')
    if feature is not None and not extrusion.is_extrusion(feature):
        raise ValueError('This feature uses the native editor.')
    _active=ExtrudeTask(feature,which)
    Gui.Control.showDialog(_active);_active.changed()
    return _active


def dispatch(which):
    # Only Plus tasks in component documents enter this workflow. Native
    # body-owned sketches retain their existing command compatibility.
    from . import ui_modes
    if ui_modes.modes()[2]!='Plus':return False
    definition,_=modeling._context(Gui.activeDocument().Document)
    selected=Gui.Selection.getSelection('*')
    if any(obj.isDerivedFrom('Sketcher::SketchObject') and obj.getParentGeoFeatureGroup()!=definition
           for obj in selected):return False
    show(which=which)
    return True
