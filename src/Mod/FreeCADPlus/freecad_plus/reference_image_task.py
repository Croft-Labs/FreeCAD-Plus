# SPDX-License-Identifier: LGPL-2.1-or-later
"""Reference image task. Coin previews are independent of saved document objects."""
import json
import math
import tempfile
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets, QtGui
from pivy import coin
from . import document, editing, modeling, panel, reference_image as images
from .reference_image_ui import Form
from .quantity_fields import units, restore_units

_active=None


class ImageTask(QtCore.QObject):
    def __init__(self,feature=None):
        super().__init__()
        self.doc=Gui.activeDocument().Document
        self.owner,self.path=modeling._context(self.doc)
        if feature and (not images.is_image(feature) or feature not in self.owner.Group):
            raise ValueError('Edit an image owned by the active component')
        self.view=Gui.activeDocument().activeView();self.scene=self.view.getSceneGraph()
        self.context=(self.doc,self.view,panel.identity(self.owner),tuple(panel.identity(o) for o in self.path))
        self.feature=feature;self.feature_id=panel.identity(feature) if feature else None
        self.revision=self.feature_revision() if feature else None
        self.closed=False;self.busy=True;self.overlay=None;self.pick_mode=None;self.points=[]
        self.anchor=[.5,.5];self.filename='';self.image=None;self.old_placement=None
        self.temp=tempfile.TemporaryDirectory(prefix='freecad-plus-image-')
        self.texture=None;self.mask=None
        self.form=Form(self.owner)
        self.timer=QtCore.QTimer(self);self.timer.setSingleShot(True);self.timer.timeout.connect(self.refresh)
        self.populate_planes()
        self.form.browse.clicked.connect(self.browse)
        self.form.plane.currentIndexChanged.connect(self.change_support)
        self.form.anchor_buttons.idClicked.connect(self.change_anchor_preset)
        self.form.pick_anchor.clicked.connect(lambda:self.start_pick('anchor'))
        self.form.pick_points.clicked.connect(lambda:self.start_pick('calibration'))
        self.form.known.committed.connect(self.calibrate)
        self.form.custom.toggled.connect(self.change_anchor_mode)
        self.form.calibrate.toggled.connect(self.stop_pick)
        for field in [self.form.width,self.form.height,*self.form.positions,self.form.angle,*self.form.rotations]:
            field.valueChanged.connect(self.schedule)
        for field in (self.form.alpha,self.form.flip,self.form.aspect,self.form.preview):
            (field.valueChanged if isinstance(field,QtWidgets.QSpinBox) else field.toggled).connect(self.schedule)
        self.form.done.clicked.connect(self.accept);self.form.apply.clicked.connect(self.apply);self.form.cancel.clicked.connect(self.reject)
        if feature:
            try:self.load(feature)
            except Exception:self.temp.cleanup();raise
            self.mask=(feature.ViewObject.SwitchNode,feature.ViewObject.SwitchNode.whichChild.getValue())
            self.mask[0].whichChild=-1
        self.callback=self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),self.click)
        App.addDocumentObserver(self);editing.add_context_observer(self.schedule)
        self.mdi=Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        if self.mdi:self.mdi.subWindowActivated.connect(self.schedule)
        self.busy=False

    def feature_revision(self):
        o=self.feature
        return (o.ImageSettings,str(o.ImageFile),o.XSize.Value,o.YSize.Value,o.ViewObject.Transparency,
                str(o.AttachmentSupport),str(o.AttachmentOffset),str(o.MapMode))

    def populate_planes(self):
        self.form.plane.clear()
        for obj in images.supports(self.owner):
            title=obj.Role.replace('_',' ')+' (component)' if obj.TypeId=='App::Plane' else obj.Label
            self.form.plane.addItem(title,panel.identity(obj))
        self.form.plane.addItem('Free placement',None)
        self.form.mode_changed(self.form.plane.currentIndex())

    def support(self):
        ref=self.form.plane.currentData()
        if ref=='missing':raise ValueError('The attached plane was removed. Choose another plane or Free placement.')
        return panel.lookup(ref) if ref else None

    def length_fields(self):
        return dict(width=self.form.width,height=self.form.height,known=self.form.known,
                    **dict(zip(('x','y','z'),self.form.positions)))

    def state(self):
        free=self.support() is None
        return dict(anchor=list(self.anchor),custom=self.form.custom.isChecked(),
                    position=[f.value() for f in self.form.positions],
                    rotation=[f.value() for f in self.form.rotations] if free else [0.,0.,self.form.angle.value()],
                    flip=self.form.flip.isChecked(),aspect=self.form.aspect.isChecked(),
                    units=units(self.length_fields()),calibration_distance=self.form.known.value())

    def load(self,feature):
        state=images.settings(feature)
        self.set_file(str(feature.ImageFile),resize=False)
        self.form.file.setText(feature.ImageName)
        support=feature.AttachmentSupport[0][0] if feature.MapMode!='Deactivated' and feature.AttachmentSupport else None
        wanted=panel.identity(support) if support else None
        index=next((i for i in range(self.form.plane.count())
                    if (tuple(self.form.plane.itemData(i)) if self.form.plane.itemData(i) else None)==wanted),-1)
        if feature.MapMode!='Deactivated' and support is None:
            self.form.plane.addItem('Missing plane — choose a replacement','missing');index=self.form.plane.count()-1
        self.form.plane.setCurrentIndex(index)
        if index<0:raise ValueError('The attached plane is unavailable')
        self.form.aspect.setChecked(False)
        self.form.width.setValue(feature.XSize.Value);self.form.height.setValue(feature.YSize.Value)
        self.form.aspect.setChecked(state['aspect']);self.form.flip.setChecked(state['flip'])
        for f,v in zip(self.form.positions,state['position']):f.setValue(v)
        for f,v in zip(self.form.rotations,state['rotation']):f.setValue(v)
        self.form.angle.setValue(state['rotation'][2]);self.anchor=state['anchor']
        self.form.known.setValue(state.get('calibration_distance',100))
        restore_units(self.length_fields(),state.get('units',{}))
        self.form.custom.setChecked(state['custom']);self.form.preset.setChecked(not state['custom'])
        self.form.alpha.setValue(feature.ViewObject.Transparency)
        index=int(round((1-self.anchor[1])*2))*3+int(round(self.anchor[0]*2))
        self.form.anchor_buttons.button(index).setChecked(True)
        self.anchor_label()
        self.form.setWindowTitle('Edit reference image')

    def check(self):
        if self.closed:raise ValueError('This task is closed')
        if not Gui.activeDocument():raise ValueError('The file was closed')
        owner,path=modeling._context(Gui.activeDocument().Document)
        current=(Gui.activeDocument().Document,Gui.activeDocument().activeView(),panel.identity(owner),tuple(panel.identity(o) for o in path))
        if current!=self.context:raise ValueError('The active component or view changed. Cancel and reopen this task.')
        if self.feature_id and (panel.lookup(self.feature_id)!=self.feature or self.feature_revision()!=self.revision):
            raise ValueError('This image changed outside the task. Cancel and reopen its editor.')

    def set_file(self,filename,resize=True):
        image=images.read_image(filename)
        self.filename=str(filename);self.image=image
        self.form.file.setText(Path(filename).name);self.form.file.setToolTip(str(filename))
        self.form.ratio=image.width()/image.height()
        if resize:
            self.form.aspect.setChecked(False)
            self.form.width.setValue(100);self.form.height.setValue(100/self.form.ratio)
            self.form.aspect.setChecked(True)
        # Normalize supported Qt image formats for Coin, including embedded image paths.
        png=Path(self.temp.name)/('image-'+str(len(list(Path(self.temp.name).glob('*.png'))))+'.png')
        if not image.save(str(png)):raise ValueError('Could not prepare the image preview')
        self.texture=coin.SoTexture2();self.texture.filename=str(png);self.texture.model=coin.SoTexture2.MODULATE
        self.points=[];self.form.points.clear();self.schedule()

    def browse(self):
        filters='Images ('+' '.join('*.'+bytes(f).decode() for f in QtGui.QImageReader.supportedImageFormats())+');;All files (*)'
        filename,_=QtWidgets.QFileDialog.getOpenFileName(self.form,'Choose reference image','',filters)
        if filename:
            try:self.check();self.set_file(filename)
            except (ValueError,RuntimeError) as error:self.form.status.setError(str(error))

    def anchor_label(self):
        self.form.anchor_point.setText(f'Image point: {self.anchor[0]*100:.2f}%, {self.anchor[1]*100:.2f}%')

    def set_anchor(self,anchor):
        before=images.local_placement(self.form.width.value(),self.form.height.value(),self.state(),self.support() is not None)
        self.anchor=list(anchor)
        position=images.anchor_position(before,self.form.width.value(),self.form.height.value(),self.anchor)
        self.busy=True
        for field,value in zip(self.form.positions,(position.x,position.y,position.z)):field.setValue(value)
        self.busy=False;self.anchor_label();self.refresh()

    def change_anchor_preset(self,index):
        try:self.set_anchor([(index%3)*.5,1-(index//3)*.5])
        except (ValueError,RuntimeError) as error:self.form.status.setError(str(error))

    def change_anchor_mode(self,custom):
        if self.busy:return
        self.stop_pick()
        if not custom:self.change_anchor_preset(self.form.anchor_buttons.checkedId())
        else:self.anchor_label()

    def change_support(self,*args):
        if self.busy:return
        self.stop_pick();self.schedule()

    def stop_pick(self,*args):
        self.pick_mode=None

    def start_pick(self,mode):
        try:
            self.check()
            if not self.image:raise ValueError('Choose an image first')
            if not self.form.preview.isChecked():raise ValueError('Enable Show preview before picking image points')
            self.pick_mode=mode
            if mode=='calibration':self.points=[];self.form.points.clear()
            self.form.status.setText('Click the anchor point on the image.' if mode=='anchor' else 'Click two image points, then enter their known distance.')
        except (ValueError,RuntimeError) as error:self.form.status.setError(str(error))

    def pick_world(self,world):
        self.check()
        p=self.world_placement().inverse().multVec(world)
        uv=[p.x/self.form.width.value()+.5,p.y/self.form.height.value()+.5]
        if any(v<0 or v>1 for v in uv):raise ValueError('Pick a point inside the image')
        if self.pick_mode=='anchor':self.set_anchor(uv);self.pick_mode=None
        elif self.pick_mode=='calibration':
            self.points.append(uv);self.form.points.addItem(f'Point {len(self.points)}: {uv[0]*100:.2f}%, {uv[1]*100:.2f}%')
            if len(self.points)==2:self.pick_mode=None;self.calibrate()

    def click(self,callback):
        if self.closed or not self.pick_mode:return
        event=callback.getEvent()
        if event.getState()!=coin.SoButtonEvent.DOWN or event.getButton()!=coin.SoMouseButtonEvent.BUTTON1:return
        callback.setHandled()
        try:
            self.check();x,y=event.getPosition().getValue()
            origin=self.view.getPoint(int(x),int(y));camera=self.view.getCameraNode()
            direction=self.view.getCameraOrientation().multVec(App.Vector(0,0,-1))
            if isinstance(camera,coin.SoPerspectiveCamera):
                c=App.Vector(*camera.position.getValue().getValue());direction=origin-c;origin=c
            placement=self.world_placement();normal=placement.Rotation.multVec(App.Vector(0,0,1))
            divisor=normal.dot(direction)
            if abs(divisor)<1e-10:raise ValueError('Turn the view toward the image before picking a point')
            distance=normal.dot(placement.Base-origin)/divisor
            self.pick_world(origin+direction*distance)
        except (ValueError,RuntimeError,ReferenceError) as error:self.form.status.setError(str(error))

    def calibrate(self,*args):
        if self.busy or len(self.points)!=2:return
        try:
            self.check();a,b=self.points
            distance=math.hypot((a[0]-b[0])*self.form.width.value(),(a[1]-b[1])*self.form.height.value())
            if distance<1e-9:raise ValueError('Choose two distinct image points')
            factor=self.form.known.value()/distance
            self.busy=True;locked=self.form.aspect.isChecked();self.form.aspect.setChecked(False)
            self.form.width.setValue(self.form.width.value()*factor);self.form.height.setValue(self.form.height.value()*factor)
            self.form.aspect.setChecked(locked);self.busy=False;self.refresh()
        except (ValueError,RuntimeError) as error:self.busy=False;self.form.status.setError(str(error))

    def world_placement(self):
        local=images.placement(self.owner,self.support(),self.form.width.value(),self.form.height.value(),self.state())
        return editing.world_placement(self.doc,self.path).multiply(local)

    def clear_preview(self):
        if self.overlay:
            self.scene.removeChild(self.overlay);self.overlay=None

    def refresh(self):
        if self.closed or self.busy:return
        self.clear_preview()
        try:
            self.check()
            ready=bool(self.filename)
            self.form.done.setEnabled(ready);self.form.apply.setEnabled(ready)
            if not ready:self.form.status.setText('Choose an image.');return
            placement=self.world_placement()
            self.form.status.setText('Ready. One Undo step.')
            if not self.form.preview.isChecked():return
            root=coin.SoSeparator();pick=coin.SoPickStyle();pick.style=coin.SoPickStyle.UNPICKABLE;root.addChild(pick)
            transform=coin.SoTransform();transform.translation=tuple(placement.Base);transform.rotation=tuple(placement.Rotation.Q);root.addChild(transform)
            style=coin.SoDrawStyle();style.style=coin.SoDrawStyle.FILLED;style.setOverride(True);root.addChild(style)
            light=coin.SoLightModel();light.model=coin.SoLightModel.BASE_COLOR;root.addChild(light)
            material=coin.SoMaterial();material.diffuseColor=(1,1,1);material.transparency=self.form.alpha.value()/100.;root.addChild(material)
            root.addChild(self.texture)
            coords=coin.SoCoordinate3();w=self.form.width.value()/2;h=self.form.height.value()/2
            coords.point.setValues(0,4,[(-w,-h,0),(w,-h,0),(w,h,0),(-w,h,0)]);root.addChild(coords)
            uv=coin.SoTextureCoordinate2();uv.point.setValues(0,4,[(0,0),(1,0),(1,1),(0,1)]);root.addChild(uv)
            face=coin.SoFaceSet();face.numVertices=4;root.addChild(face)
            # A separate marker is visible while locating the fixed scale/rotation anchor.
            marker=coin.SoSeparator();empty=coin.SoTexture2();marker.addChild(empty)
            color=coin.SoBaseColor();color.rgb=(.95,.25,.05);marker.addChild(color)
            style=coin.SoDrawStyle();style.pointSize=9;marker.addChild(style)
            point=coin.SoCoordinate3();point.point.set1Value(0,(self.anchor[0]-.5)*w*2,(self.anchor[1]-.5)*h*2,.002)
            marker.addChild(point);marker.addChild(coin.SoPointSet());root.addChild(marker)
            self.scene.addChild(root);self.overlay=root
            if self.mask:self.mask[0].whichChild=-1
        except (ValueError,RuntimeError,ReferenceError,TypeError) as error:
            self.form.done.setEnabled(False);self.form.apply.setEnabled(False);self.form.status.setError(str(error))

    def schedule(self,*args):
        if not self.closed and not self.busy:self.timer.start(0)
    slotChangedObject=schedule
    slotRecomputedDocument=schedule
    slotDeletedObject=schedule
    def slotDeletedDocument(self,doc):
        if doc in (self.doc,self.owner.Document):self.reject()

    def restore_mask(self):
        if self.mask:
            try:self.mask[0].whichChild=self.mask[1]
            except (RuntimeError,ReferenceError):pass
            self.mask=None

    def commit(self):
        self.check()
        if not self.filename:raise ValueError('Choose an image first')
        for field in self.length_fields().values():
            if not field.hasAcceptableInput():raise ValueError('Enter a valid length, such as 0.25 in.')
            field.interpretText()
        self.busy=True
        try:
            result=images.save(self.doc,self.filename,self.support(),self.form.width.value(),self.form.height.value(),self.state(),self.form.alpha.value(),self.feature)
            self.restore_mask()
            if self.owner.Document!=self.doc:self.doc.recompute()
            return result
        finally:self.busy=False

    def apply(self):
        try:
            self.result=self.commit();self.clear_preview();self.stop_pick();self.busy=True
            self.feature=None;self.feature_id=None;self.revision=None;self.filename='';self.image=None;self.texture=None
            self.anchor=[.5,.5];self.points=[];self.form.points.clear();self.form.anchor_point.clear();self.form.file.clear();self.form.file.setToolTip('')
            self.populate_planes();self.form.aspect.setChecked(False);self.form.ratio=1
            for field in self.length_fields().values():field.setSuffix('mm')
            self.form.width.setValue(100);self.form.height.setValue(100);self.form.aspect.setChecked(True)
            for field in [*self.form.positions,self.form.angle,*self.form.rotations]:field.setValue(0)
            self.form.flip.setChecked(False);self.form.preset.setChecked(True);self.form.anchor_buttons.button(4).setChecked(True)
            self.form.alpha.setValue(0);self.form.preview.setChecked(True);self.form.calibrate.setChecked(False);self.form.known.setValue(100)
            self.form.setWindowTitle('Reference image');self.busy=False;self.refresh()
            if panel._panel:panel._panel.refresh()
            return True
        except (ValueError,RuntimeError,ReferenceError,TypeError) as error:
            self.busy=False;self.form.status.setError(str(error));return False

    def accept(self):
        try:self.result=self.commit()
        except (ValueError,RuntimeError,ReferenceError,TypeError) as error:self.form.status.setError(str(error));return False
        self.reject();return True

    def reject(self):
        global _active
        if self.closed:return True
        self.closed=True;self.timer.stop();self.clear_preview();self.restore_mask()
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),self.callback)
        App.removeDocumentObserver(self);editing.remove_context_observer(self.schedule)
        if self.mdi:
            try:self.mdi.subWindowActivated.disconnect(self.schedule)
            except RuntimeError:pass
        self.texture=None;self.temp.cleanup()
        if _active is self:_active=None;Gui.Control.closeDialog()
        panel.end_feature_task(self)
        if panel._panel:panel._panel.refresh()
        self.deleteLater();return True

    def getStandardButtons(self):return 0
    def isAllowedAlterDocument(self):return False
    def isAllowedAlterSelection(self):return True
    def isAllowedAlterView(self):return True


def show(feature=None):
    global _active
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first')
    task=ImageTask(feature);_active=task
    try:Gui.Control.showDialog(task);panel.begin_feature_task(task);task.refresh()
    except Exception:task.reject();raise
    return task


class Command:
    def GetResources(self):return dict(MenuText='Reference image',ToolTip='Add an image on a fundamental or created plane',Pixmap='image-plane')
    def IsActive(self):
        from .idle_tasks import eligible
        return eligible()
    def Activated(self):
        try:show()
        except (ValueError,RuntimeError,ReferenceError) as error:
            from .thicken_task import show_error
            show_error('Reference image',str(error))


def install():Gui.addCommand('Plus_ReferenceImage',Command())


def history_menu(widget,tree,point,row):
    doc,obj=widget._checked(row);binding=widget._binding
    menu=QtWidgets.QMenu(widget)
    edit=menu.addAction('Edit reference image…');visibility=menu.addAction('Hide' if obj.Visibility else 'Show')
    menu.addSeparator();delete=menu.addAction('Delete')
    chosen=menu.exec_(tree.viewport().mapToGlobal(point));menu.deleteLater()
    if not chosen:return
    if widget._current()!=binding:raise ValueError('The active file changed; reopen the menu')
    widget._checked(row)
    if chosen==edit:show(obj)
    elif chosen==visibility:widget.toggle_history_visibility(row)
    elif chosen==delete:
        if Gui.Control.activeDialog():raise ValueError('Finish the current task before deleting the image')
        images.remove(doc,obj);widget.refresh()
