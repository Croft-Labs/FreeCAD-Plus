# SPDX-License-Identifier: LGPL-2.1-or-later
"""One associative mesh of owned solid/surface references."""
import json
import math
import subprocess
import tempfile
from pathlib import Path
import FreeCAD as App
import Part,Mesh,MeshPart
from . import document,planes,modeling,derived_geometry


def compute(owner,refs,settings,cancel=None):
    if not refs:raise ValueError('Select solids, sheets or faces to mesh')
    shapes=[];colors=[]
    from .appearance import materials
    for ref in refs:
        planes.canonical(owner,[ref]);shape=planes.shape(owner,ref)
        if not shape.Faces or not shape.isValid():raise ValueError('Each input must have valid faces')
        shapes.append(shape)
        obj,sub=ref
        values=materials(obj.Tip if obj.TypeId=='PartDesign::Body' else obj)
        element=Part.splitSubname(sub)[2]
        colors.extend([values[int(element[4:])-1].DiffuseColor] if element.startswith('Face') else [v.DiffuseColor for v in values])
    shape=shapes[0] if len(shapes)==1 else Part.makeCompound(shapes);method=settings['method']
    if method==3:
        mesh=gmsh(shape,settings,cancel)
    else:
        kwargs=dict(settings['parameters']);kwargs['Shape']=shape
        if settings.get('colors') and method==0:
            kwargs['Segments']=True
            if settings.get('group_colors'):
                kwargs['GroupColors']=colors
        if method in (1,2):
            # Native Mefisto/Netgen mesh one shape at a time. Merge their
            # kernels afterwards, preserving the one-result user operation.
            mesh=Mesh.Mesh()
            for item in shapes:
                kwargs['Shape']=item
                value=MeshPart.meshFromShape(**kwargs)
                if not value.CountFacets:raise ValueError('The mesher could not tessellate an input')
                mesh.addMesh(value)
        else:mesh=MeshPart.meshFromShape(**kwargs)
    if mesh.CountFacets==0:raise ValueError('Meshing produced no facets')
    return mesh,colors


def gmsh(shape,settings,cancel=None):
    algorithm=int(settings['algorithm']);minimum=float(settings['min_size']);maximum=float(settings['max_size'])
    if algorithm not in (1,2,5,6,7,8,9,11) or any(not math.isfinite(v) or v<0 for v in (minimum,maximum)):
        raise ValueError('Invalid Gmsh meshing settings')
    with tempfile.TemporaryDirectory(prefix='FreeCADPlus-mesh-') as directory:
        root=Path(directory);brep=root/'source.brep';geo=root/'mesh.geo';output=root/'mesh.stl'
        shape.exportBrep(str(brep))
        geo.write_text('Merge "'+brep.as_posix()+'";\n'+
                       'Mesh.CharacteristicLengthMax = '+str(maximum or 1e22)+';\n'+
                       'Mesh.CharacteristicLengthMin = '+str(minimum)+';\n'+
                       'Mesh.Algorithm = '+str(algorithm)+';\n'+
                       'Mesh.Optimize = 1;\nMesh.ElementOrder = 2;\nMesh.SecondOrderLinear = 1;\nGeometry.Tolerance = 1e-6;\nMesh 2;\nCoherence Mesh;\n')
        with (root/'output.log').open('w') as log:
            executable=settings.get('executable') or App.ParamGet('User parameter:BaseApp/Preferences/Mod/Mesh/Meshing').GetString('gmshExe') or 'gmsh'
            try:
                proc=subprocess.Popen([executable,'-','-bin','-2',str(geo),'-o',str(output)],
                                      stdout=log,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            except OSError as exc:raise ValueError('Choose a valid Gmsh executable in the meshing settings') from exc
            import time
            deadline=time.monotonic()+180
            try:
                while proc.poll() is None:
                    if cancel:
                        from PySide6 import QtWidgets
                        QtWidgets.QApplication.processEvents()
                        if cancel():raise ValueError('Meshing cancelled')
                    if time.monotonic()>deadline:raise ValueError('Gmsh did not finish within three minutes')
                    time.sleep(.02)
                if proc.returncode or not output.exists():raise ValueError('Gmsh failed. Check its executable and meshing settings.')
            finally:
                if proc.poll() is None:proc.kill();proc.wait()
        mesh=Mesh.Mesh(str(output));mesh.harmonizeNormals();return mesh


class Meshed:
    def __init__(self,obj):
        obj.addProperty('App::PropertyLinkSubListGlobal','MeshSources','Meshing')
        obj.addProperty('App::PropertyString','MeshSettings','Meshing')
        obj.addProperty('App::PropertyString','GeometryError','Meshing')
        for name in ('MeshSources','MeshSettings'):obj.setEditorMode(name,2)
        obj.setEditorMode('GeometryError',1);obj.Proxy=self;self.pending=None
    def execute(self,obj):
        try:
            settings=json.loads(obj.MeshSettings)
            settings.pop('executable',None)  # A document must not choose a local executable.
            value=self.pending or compute(derived_geometry.owner(obj),planes.flatten(obj.MeshSources),settings)
            self.pending=None;obj.Mesh=value[0];obj.GeometryError=''
            if settings.get('colors') and settings['method']==0:
                colors=list(dict.fromkeys(value[1])) if settings.get('group_colors') else value[1]
                if obj.Mesh.countSegments()==len(colors):
                    if 'FaceColors' not in obj.PropertiesList:obj.addProperty('App::PropertyColorList','FaceColors','Meshing')
                    faces=[(0.8,0.8,0.8)]*obj.Mesh.CountFacets
                    for index,color in enumerate(colors):
                        for facet in obj.Mesh.getSegment(index):faces[facet]=color
                    obj.FaceColors=faces
                    obj.ViewObject.Coloring=False;obj.ViewObject.Coloring=True
            elif 'FaceColors' in obj.PropertiesList:
                obj.ViewObject.Coloring=False
                obj.removeProperty('FaceColors')
        except Exception as exc:
            obj.Mesh=Mesh.Mesh();obj.GeometryError=str(exc);raise
    def dumps(self):return None
    def loads(self,state):self.pending=None


class ViewMeshed:
    def __init__(self,view):view.Proxy=self
    def getIcon(self):return ':/icons/Mesh_Mesh.svg'
    def doubleClicked(self,view):
        from .mesh_task import show
        show(view.Object);return True
    def dumps(self):return None
    def loads(self,state):pass


def save(doc,refs,settings,feature=None,cancel=None):
    import MeshGui  # Register the native mesh view provider before creation.
    owner,_=modeling._context(doc)
    if feature and derived_geometry.owner(feature)!=owner:raise ValueError('Edit a mesh in the active component')
    document.require_predecessors(owner,feature,refs)
    value=compute(owner,refs,settings,cancel)
    current,_=modeling._context(doc)
    if current!=owner:raise ValueError('The active component changed; mesh was not added')
    with document.transaction(owner.Document,'Edit mesh' if feature else 'Mesh from shape'):
        root=document.validate(owner.Document);root.PlusSchema=max(root.PlusSchema,8)
        if feature is None:
            feature=owner.newObject('Mesh::FeaturePython','Mesh');Meshed(feature);ViewMeshed(feature.ViewObject)
        persisted=dict(settings);persisted.pop('executable',None)
        feature.MeshSources=planes.links(refs);feature.MeshSettings=json.dumps(persisted)
        feature.Proxy.pending=value;feature.touch();owner.Document.recompute()
        if feature.GeometryError or feature.Mesh.CountFacets==0:raise ValueError(feature.GeometryError or 'Mesh creation failed')
    return feature
