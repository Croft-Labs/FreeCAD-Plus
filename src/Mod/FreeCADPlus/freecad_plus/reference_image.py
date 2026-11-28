# SPDX-License-Identifier: LGPL-2.1-or-later
"""Embedded native image planes with versioned Plus task state and native attachment."""
from . import result_names
import json
import math
from pathlib import Path
import FreeCAD as App
from PySide6 import QtGui
from . import document, modeling, planes


def is_image(obj):
    return obj.TypeId == 'Image::ImagePlane' and 'PlusImageVersion' in obj.PropertiesList


def supports(owner):
    result = [o for o in owner.Origin.OriginFeatures if o.TypeId == 'App::Plane']
    def visit(parent):
        for obj in document.owned_children(parent):
            if planes.is_plane(obj) or obj.TypeId in ('PartDesign::Plane', 'Part::DatumPlane'):
                result.append(obj)
            if obj.TypeId == 'PartDesign::Body': visit(obj)
    visit(owner)
    return result


def defaults():
    return dict(anchor=[.5,.5], custom=False, position=[0.,0.,0.], rotation=[0.,0.,0.],
                flip=False, aspect=True)


def checked_state(state):
    state = dict(state)
    for key, count in (('anchor',2),('position',3),('rotation',3)):
        values = state.get(key)
        if not isinstance(values,(list,tuple)) or len(values)!=count or any(
                not isinstance(v,(int,float)) or not math.isfinite(v) for v in values):
            raise ValueError('Invalid reference image '+key)
    if any(v<0 or v>1 for v in state['anchor']): raise ValueError('Pick a point inside the image')
    for key in ('custom','flip','aspect'):
        if not isinstance(state.get(key),bool): raise ValueError('Invalid reference image '+key)
    return state


def settings(feature):
    if feature.PlusImageVersion!=1: raise ValueError('Unsupported reference image version')
    try:return checked_state(json.loads(feature.ImageSettings))
    except (TypeError,KeyError,json.JSONDecodeError) as error:raise ValueError('Invalid reference image settings') from error


def read_image(filename):
    image = QtGui.QImage(str(filename))
    if image.isNull() or image.width()<1 or image.height()<1:
        raise ValueError('Choose a readable image file')
    return image


def local_placement(width,height,state,attached):
    state=checked_state(state)
    if not all(math.isfinite(v) and v>0 for v in (width,height)):
        raise ValueError('Image width and height must be positive')
    x,y,z=state['rotation']
    rotation=App.Rotation(App.Vector(0,0,1),z) if attached else App.Rotation(z,y,x)
    if attached and state['flip']:rotation=rotation.multiply(App.Rotation(App.Vector(1,0,0),180))
    anchor=App.Vector((state['anchor'][0]-.5)*width,(state['anchor'][1]-.5)*height,0)
    return App.Placement(App.Vector(*state['position'])-rotation.multVec(anchor),rotation)


def support_placement(owner,support):
    if support is None:return App.Placement()
    if support not in supports(owner):raise ValueError('Choose a fundamental or created plane in this component')
    if getattr(support,'PlaneError','') or 'Invalid' in support.State:
        raise ValueError('The selected plane is invalid; repair it or choose another plane')
    return owner.getGlobalPlacement().inverse().multiply(support.getGlobalPlacement())


def placement(owner,support,width,height,state):
    return support_placement(owner,support).multiply(local_placement(width,height,state,support is not None))


def anchor_position(placement,width,height,anchor):
    return placement.multVec(App.Vector((anchor[0]-.5)*width,(anchor[1]-.5)*height,0))


def structural_check(owner,feature):
    if not is_image(feature):raise ValueError('Use the Reference image task to add images to a component')
    settings(feature)
    if not feature.hasExtension('Part::AttachExtension'):
        raise ValueError('Reference image attachment data is missing')
    refs=feature.AttachmentSupport
    if feature.MapMode!='Deactivated':
        if feature.MapMode!='ObjectXY' or len(refs)>1:
            raise ValueError('Invalid reference image attachment mode')
        # A deleted support must not hide the entire Components panel. Keep the
        # native feature invalid and allow its task to choose a replacement.
        if refs and refs[0][0] is not None and refs[0][0] not in supports(owner):
            raise ValueError('Reference image support is outside its component')
        if refs and any(refs[0][1]):raise ValueError('Reference images attach to whole planes')


def save(doc,filename,support,width,height,state,transparency=0,feature=None,result_name=None):
    owner,path=modeling._context(doc)
    root=document.validate(owner.Document)
    read_image(filename);state=checked_state(state)
    if not isinstance(transparency,int) or not 0<=transparency<=100:raise ValueError('Transparency must be between 0 and 100')
    placement(owner,support,width,height,state)
    if feature is not None and (not is_image(feature) or feature not in owner.Group):
        raise ValueError('Edit an image owned by this component')
    document.require_predecessors(owner,feature,[(support,'')] if support else [])
    with document.transaction(owner.Document,'Edit reference image' if feature else 'Create reference image'):
        root.PlusSchema=max(root.PlusSchema,9)
        if feature is None:
            feature=owner.newObject('Image::ImagePlane','ReferenceImage')
            feature.Label='Reference image'
            feature.addExtension('Part::AttachExtensionPython')
            feature.addProperty('App::PropertyInteger','PlusImageVersion','Reference image').PlusImageVersion=1
            feature.addProperty('App::PropertyString','ImageSettings','Reference image')
            feature.addProperty('App::PropertyString','ImageName','Reference image')
        result_names.assign(feature,result_name)
        if str(feature.ImageFile)!=str(filename):
            feature.ImageFile=str(filename);feature.ImageName=Path(filename).name
        feature.XSize=width;feature.YSize=height
        feature.ImageSettings=json.dumps(state,sort_keys=True)
        feature.MapMode='Deactivated'
        feature.AttachmentSupport=[(support,[''])] if support else []
        local=local_placement(width,height,state,support is not None)
        feature.AttachmentOffset=local
        if support:
            feature.MapMode='ObjectXY';feature.positionBySupport()
        else:feature.Placement=local
        feature.ViewObject.Transparency=transparency
        feature.ViewObject.DisplayMode='No shading'
        for name in ('PlusImageVersion','ImageSettings','ImageName'):feature.setEditorMode(name,2)
        for name in ('XSize','YSize','ImageFile','Placement','AttachmentOffset','AttachmentSupport','MapMode'):
            feature.setEditorMode(name,1)
        owner.Document.recompute()
        if 'Invalid' in feature.State:raise ValueError('The image attachment could not be recomputed')
    return feature


def remove(doc,feature):
    owner,path=modeling._context(doc)
    if feature not in owner.Group or not is_image(feature):raise ValueError('Choose an image in this component')
    consumers=[o for o in feature.InList if o!=owner]
    if consumers:raise ValueError('Remove dependent features before deleting this image')
    with document.transaction(owner.Document,'Delete reference image'):
        owner.Document.removeObject(feature.Name)
