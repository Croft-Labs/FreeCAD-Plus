# SPDX-License-Identifier: LGPL-2.1-or-later
"""Linked solid trim by one complete, finite surface boundary or infinite plane."""
from . import result_names
import json
import math
import FreeCAD as App
import Part
from BOPTools import SplitAPI
from . import document,planes,modeling,derived_geometry


def evaluate(owner,target,refs,settings,consumer=None):
    planes.canonical(owner,[target]);document.require_predecessors(owner,consumer,[target,*refs])
    body=planes.shape(owner,target)
    if not body.Solids or not body.isValid():raise ValueError('Select a valid target body')
    offset=float(settings.get('offset',0))
    if not math.isfinite(offset):raise ValueError('Offset must be finite')
    if settings.get('mode',0)==1:
        axis=settings.get('plane',0)
        if axis==3:
            if len(refs)!=1:raise ValueError('Select a datum plane')
            kind,point,normal=planes.describe(owner,refs[0])
            if kind!='plane':raise ValueError('Select a datum plane')
        else:
            normal=App.Vector(*((0,0,1),(0,1,0),(1,0,0))[axis]);point=App.Vector()
        point=point+normal*offset
        # Use the unbounded geometric plane, not its displayed rectangle.
        tool=Part.Face(Part.Plane(point,normal))
    else:
        if not refs:raise ValueError('Select trimming surfaces')
        faces=[]
        for ref in refs:
            planes.canonical(owner,[ref]);shape=planes.shape(owner,ref)
            if shape.Solids or not shape.Faces:raise ValueError('Choose individual faces or sheets for the boundary')
            faces.extend(shape.Faces)
        tool=derived_geometry.joined_surface(faces)
        if offset:tool=tool.makeOffsetShape(offset,1e-7,fill=False)
        if tool.isNull() or not tool.isValid():raise ValueError('The offset does not produce a valid boundary')
        # Sewing shares internal seams. Only exterior tool edges must lie
        # outside the target; reject even when a partial cut happens to split it.
        boundary=[edge for edge in tool.Edges if sum(any(edge.isSame(e) for e in face.Edges) for face in tool.Faces)==1]
        if not boundary:raise ValueError('Use an open trimming boundary, not a closed shell')
        for edge in boundary:
            if edge.common(body).Vertexes:
                raise ValueError('Trim invalid: the tool boundary ends inside the target body. Extend the surfaces past its periphery.')
    retained=[];removed=[]
    for solid in body.Solids:
        parts=SplitAPI.slice(solid,[tool],'Split').Solids
        if len(parts)<2:raise ValueError('The combined boundary must fully cross the target body')
        for part in parts:
            sample=part.CenterOfMass
            candidates=[]
            for face in tool.Faces:
                distance,points,_=face.distToShape(Part.Vertex(sample))
                p=points[0][0];u,v=face.Surface.parameter(p);n=face.normalAt(u,v)
                candidates.append((distance,(sample-p).dot(n)))
            sign=min(candidates,key=lambda value:value[0])[1]
            if abs(sign)<1e-7:raise ValueError('Cannot determine a consistent side of this boundary')
            remove=sign>0
            if settings.get('reverse',False):remove=not remove
            (removed if remove else retained).append(part)
    if not retained or not removed:raise ValueError('The boundary must separate a retained side and a removed side')
    keep=Part.makeCompound(retained) if len(retained)>1 else retained[0]
    waste=Part.makeCompound(removed) if len(removed)>1 else removed[0]
    if not keep.isValid() or not waste.isValid():raise ValueError('Trim produced invalid geometry')
    if abs(keep.Volume+waste.Volume-body.Volume)>max(1e-6,body.Volume*1e-7):raise ValueError('Trim did not preserve the target volume partition')
    return keep,waste


class Trim:
    def __init__(self,obj):
        for kind,name in (('LinkSubGlobal','TrimTarget'),('LinkSubListGlobal','TrimTools'),('String','TrimSettings'),('String','GeometryError')):
            obj.addProperty('App::Property'+kind,name,'Trim body');obj.setEditorMode(name,1 if name=='GeometryError' else 2)
        obj.Proxy=self
    def execute(self,obj):
        try:
            owner=derived_geometry.owner(obj);base,subs=obj.TrimTarget
            shape,_=evaluate(owner,(base,subs[0] if subs else ''),planes.flatten(obj.TrimTools),json.loads(obj.TrimSettings))
            body=obj.getParentGeoFeatureGroup();body.AllowCompound=len(shape.Solids)>1
            shape.Placement=body.getGlobalPlacement().inverse().multiply(owner.getGlobalPlacement()).multiply(shape.Placement)
            obj.Shape=shape;obj.GeometryError=''
        except Exception as exc:obj.Shape=Part.Shape();obj.GeometryError=str(exc);raise
    def dumps(self):return None
    def loads(self,state):pass


class ViewTrim:
    def __init__(self,view):view.Proxy=self
    def getIcon(self):return ':/icons/Part_Cut.svg'
    def doubleClicked(self,view):
        from .trim_task import show
        show(view.Object);return True
    def dumps(self):return None
    def loads(self,state):pass


def save(doc,target,refs,settings,feature=None,result_name=None):
    owner,_=modeling._context(doc)
    if feature and derived_geometry.owner(feature)!=owner:raise ValueError('Edit a trim in the active component')
    evaluate(owner,target,refs,settings,feature)
    creating=feature is None
    with document.transaction(owner.Document,'Edit trim body' if feature else 'Trim body'):
        if feature is None:
            body=owner.newObject('PartDesign::Body','Body');body.AllowCompound=True
            feature=body.newObject('PartDesign::FeaturePython','TrimBody');Trim(feature);ViewTrim(feature.ViewObject)
            feature.Label='Trim body'
        result_names.assign(feature,result_name)
        feature.TrimTarget=(target[0],[target[1]]);feature.TrimTools=planes.links(refs);feature.TrimSettings=json.dumps(settings)
        feature.touch();owner.Document.recompute()
        if feature.GeometryError:raise ValueError(feature.GeometryError)
        if creating:
            from .appearance import clone,materials
            authored=materials(target[0]);original=planes.shape(owner,target)
            result=planes.shape(owner,(feature,''));colors=[]
            for face in result.Faces:
                index=next((i for i,source in enumerate(original.Faces)
                            if abs(face.common(source).Area-face.Area)<max(1e-7,face.Area*1e-7)),0)
                colors.append(clone(authored[index]))
            feature.ViewObject.ShapeAppearance=colors
        target[0].Visibility=False
        parent=target[0].getParentGeoFeatureGroup()
        if parent and parent.TypeId=='PartDesign::Body':parent.Visibility=False
    return feature
