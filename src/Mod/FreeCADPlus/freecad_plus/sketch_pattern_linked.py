# SPDX-License-Identifier: LGPL-2.1-or-later
"""Associative sketch patterns: recipes, dependency ordering and exact geometry.

The native sketch solver calls plan/generate synchronously on its working geometry.
No document observer, repeated solve callback or per-copy constraint is involved.
"""
import json
import uuid
import FreeCAD as App
import Part
from . import sketch_pattern as pattern
from . import sketch_pattern_edit as editing


def records(sketch):
    return {key:json.loads(value) for key,value in getattr(sketch,editing.PROPERTY,{}).items()}


def is_linked(record):return record.get('behavior')=='linked'


def active_options(options):
    """Unused draft pickers must not become persistent dependencies."""
    import copy
    result=copy.deepcopy(options);linear=result.get('pattern','Linear')=='Linear'
    if linear:result['center']=None
    for name in ('d1','d2','angular','radial'):
        extent=result.get(name,{})
        if linear and name in (('d1','d2') if result.get('directions')=='Two directions' else ('d1',)):
            method=extent.get('method','Axis or line')
            keep=() if method=='Vector' else ('start','end') if method=='Two points' else ('reference',)
        else:keep=('reference',) if not linear and name=='radial' and result.get('directions','Angular')!='Angular' else ()
        for key in ('reference','start','end'):
            if key in extent and key not in keep:extent[key]=None
    return result


def option_ids(options):
    refs=[]
    if options.get('pattern','Linear')=='Linear':
        names=('d1','d2') if options.get('directions')=='Two directions' else ('d1',)
        for name in names:
            extent=options.get(name,{})
            method=extent.get('method','Axis or line')
            keys=() if method=='Vector' else ('start','end') if method=='Two points' else ('reference',)
            refs.extend(extent.get(key) for key in keys)
    else:
        refs.append(options.get('center'))
        if options.get('directions','Angular')!='Angular':refs.append(options.get('radial',{}).get('reference'))
    for ref in refs:
        if ref and 'id' in ref:yield ref['id']


def plan(sketch):
    """Topologically ordered solve/generation phases; reject feedback constraints."""
    definitions={key:r for key,r in records(sketch).items() if is_linked(r)}
    index=editing.identities(sketch);count=sketch.GeometryCount
    owned={}
    for key,record in definitions.items():
        if record.get('version')!=1:raise ValueError('Unsupported linked pattern version')
        for tag in editing.owned(record):
            if tag not in index:raise ValueError('A linked pattern copy was deleted. Undo or edit the pattern.')
            if index[tag] in owned:raise ValueError('A curve belongs to more than one linked pattern')
            owned[index[tag]]=key
    flagged={i for i,f in enumerate(sketch.GeometryFacadeList) if f.testGeometryMode('PatternGenerated')}
    if flagged!=owned.keys():raise ValueError('The linked pattern geometry and its saved definition do not match. Undo the last change.')
    if not definitions:return []
    # Driving constraints connect editable curves into ordinary solver components.
    parent=list(range(count))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def geos(c):return {i for i in (c.First,c.Second,c.Third) if 0<=i<count}
    constraints=sketch.Constraints
    for c in constraints:
        if not c.IsActive or not c.Driving:continue
        editable=sorted(geos(c)-owned.keys())
        for a,b in zip(editable,editable[1:]):parent[root(b)]=root(a)
    nodes={root(i):set() for i in range(count) if i not in owned}
    nodes.update({key:set() for key in definitions})
    for key,record in definitions.items():
        for tag in set(record['inputs'])|set(option_ids(record['options'])):
            if tag not in index:raise ValueError('A linked pattern source or direction was deleted')
            i=index[tag];nodes[key].add(owned[i] if i in owned else root(i))
    for c in constraints:
        if not c.IsActive or not c.Driving:continue
        ids=geos(c);generated=ids & owned.keys();editable=ids-owned.keys()
        if generated and not editable:
            raise ValueError('Generated pattern curves cannot be independently constrained. Edit the source or make the pattern independent.')
        for i in editable:nodes[root(i)].update(owned[g] for g in generated)
    levels={};visiting=set()
    def level(node):
        if node in levels:return levels[node]
        if node in visiting:raise ValueError('A pattern copy cannot constrain its source or direction: this creates a dependency cycle.')
        visiting.add(node)
        levels[node]=max((level(n)+1 for n in nodes[node]),default=0)
        visiting.remove(node);return levels[node]
    for node in nodes:level(node)
    phases=[dict(geometry=[],constraints=[],generate=[]) for _ in range(max(levels.values(),default=0)+1)]
    for i in range(count):
        if i not in owned:phases[levels[root(i)]]['geometry'].append(i)
    for key in definitions:phases[levels[key]]['generate'].append(key)
    for i,c in enumerate(constraints):
        if not c.IsActive:continue
        ids=geos(c);editable=ids-owned.keys()
        at=max((levels[root(g)] for g in editable),default=0)
        at=max(at,max((levels[owned[g]] for g in ids & owned.keys()),default=0))
        phases[at]['constraints'].append(i)
    return [(p['geometry'],p['constraints'],p['generate']) for p in phases]


class WorkingSketch:
    def __init__(self,sketch,geometry):
        self.Geometry=geometry;self.GeometryCount=len(geometry);self.ExternalGeo=sketch.ExternalGeo
        self.sketch=sketch
    def getPoint(self,geo,pos):
        if geo<0:return self.sketch.getPoint(geo,pos)
        g=self.Geometry[geo]
        if isinstance(g,Part.Point):return App.Vector(g.X,g.Y,g.Z)
        if pos==3 and hasattr(g,'Center'):return g.Center
        if pos==1:return g.StartPoint if hasattr(g,'StartPoint') else g.value(g.FirstParameter)
        if pos==2:return g.EndPoint if hasattr(g,'EndPoint') else g.value(g.LastParameter)
        raise ValueError('Choose a supported point or curve center for the pattern')


def generate(sketch,geometry,groups):
    """Return replacements only; the native caller retains destination IDs/extensions."""
    definitions=records(sketch);index=editing.identities(sketch)
    working=WorkingSketch(sketch,list(geometry));result=[]
    for key in groups:
        record=definitions[key];options=editing.options_refs(sketch,active_options(record['options']),False)
        transforms=pattern.transforms(working,options)
        if len(transforms)!=len(record['instances']):raise ValueError('The linked pattern recipe has inconsistent instance counts')
        for transform,instance in zip(transforms,record['instances']):
            for source,target in instance['geometry'].items():
                if source not in index or target not in index:raise ValueError('A linked pattern source or copy is missing')
                g=pattern.transformed(working.Geometry[index[source]],transform)
                working.Geometry[index[target]]=g;result.append((index[target],g))
    return result


def write_records(sketch,definitions):
    if editing.PROPERTY not in sketch.PropertiesList:
        sketch.addProperty('App::PropertyMap',editing.PROPERTY,'Pattern','Saved sketch pattern definitions')
        sketch.setEditorMode(editing.PROPERTY,2)
    setattr(sketch,editing.PROPERTY,{key:json.dumps(value,separators=(',',':')) for key,value in definitions.items()})


def mark(sketch,ids,value):
    facades=sketch.GeometryFacadeList
    for i in ids:facades[i].setGeometryMode('PatternGenerated',value)
    sketch.GeometryFacadeList=facades


def guard_removal(sketch,removed,group):
    if not removed:return
    indexed=editing.identities(sketch);ids={indexed[t] for t in removed if t in indexed}
    for c in sketch.Constraints:
        if c.PatternGroup!=group and any(i in ids for i in (c.First,c.Second,c.Third)):
            raise ValueError('A removed pattern curve is referenced by another constraint. Keep it or remove that reference first.')
    for key,record in records(sketch).items():
        if key!=group and removed.intersection(set(record['inputs'])|set(option_ids(record['options']))):
            raise ValueError('Another pattern references a removed curve. Keep that instance or edit the dependent pattern first.')
    for obj in sketch.InList:
        for name in obj.PropertiesList:
            if 'LinkSub' not in obj.getTypeIdOfProperty(name):continue
            value=getattr(obj,name);links=[value] if isinstance(value,tuple) else value
            if any(isinstance(v,tuple) and len(v)==2 and v[0]==sketch and any(v[1]) for v in links or []):
                raise ValueError('A downstream feature references sketch elements. Keep their identities before removing copies.')


def prepare_delete(sketch,ids):
    """Validate native geometry deletion before it can erase dependency links."""
    definitions=records(sketch);facades=sketch.GeometryFacadeList
    removed={str(facades[i].Id) for i in ids}
    deleted=set()
    for key,record in definitions.items():
        if not is_linked(record):continue
        owned=editing.owned(record)
        if owned.intersection(removed):
            if not owned<=removed:
                raise ValueError('Select the entire linked pattern to delete it, or edit its instance count.')
            guard_removal(sketch,owned,key);deleted.add(key)
        elif removed.intersection(set(record['inputs'])|set(option_ids(record['options']))):
            raise ValueError('This geometry drives a linked pattern. Delete or make that pattern independent first.')
    if deleted:write_records(sketch,{key:r for key,r in definitions.items() if key not in deleted})


def save(sketch,ids,options,group=None,*,_transaction=True):
    ids=pattern.operation_geometry(sketch,ids);pattern.preview(sketch,ids,options)
    if sketch.solve()!=0:raise ValueError('Resolve the sketch before creating or editing a linked pattern')
    definitions=records(sketch);old=definitions.get(group) if group else None
    if old and not is_linked(old):return convert(sketch,group,ids,options)
    keys=[str(f.Id) for f in sketch.GeometryFacadeList];source_tags=[keys[i] for i in ids]
    if old and editing.owned(old).intersection(source_tags):raise ValueError('Choose source curves, not this pattern’s copies')
    encoded=editing.options_refs(sketch,active_options(options))
    if old and editing.owned(old).intersection(option_ids(encoded)):raise ValueError('A pattern cannot use its own copies as direction or center')
    placements=pattern.transforms(sketch,options);slots=editing.slots(options)
    previous={tuple(v['slot']):v['geometry'] for v in old['instances']} if old else {}
    keep={tag for slot in slots for src,tag in previous.get(slot,{}).items() if src in source_tags}
    removed=editing.owned(old)-keep if old else set();guard_removal(sketch,removed,group)
    doc=sketch.Document
    if _transaction:doc.openTransaction('Edit linked sketch pattern' if old else 'Linked sketch pattern')
    try:
        if old:
            definitions.pop(group);write_records(sketch,definitions)
            mark(sketch,[editing.identities(sketch)[t] for t in editing.owned(old)],False)
        if removed:sketch.delGeometries(sorted(editing.identities(sketch)[t] for t in removed),True)
        index=editing.identities(sketch);instances=[];generated=[];pending=[]
        for slot,transform in zip(slots,placements):
            mapping={}
            for src in source_tags:
                target=previous.get(slot,{}).get(src)
                if target not in keep:
                    i=index[src];g=pattern.transformed(sketch.Geometry[i],transform)
                    pending.append((mapping,src,g,sketch.getConstruction(i)))
                else:mapping[src]=target
            instances.append(dict(slot=list(slot),geometry=mapping))
        # Batch native insertion by construction state; avoid solving per curve.
        from itertools import groupby
        for construction,items in groupby(pending,key=lambda item:item[3]):
            items=list(items);first=sketch.GeometryCount
            sketch.addGeometry([item[2] for item in items],construction)
            facades=sketch.GeometryFacadeList
            for n,(mapping,src,_,_) in enumerate(items):mapping[src]=str(facades[first+n].Id)
        generated=[tag for instance in instances for tag in instance['geometry'].values()]
        key=group or uuid.uuid4().hex
        definitions[key]=dict(version=1,behavior='linked',inputs=source_tags,options=encoded,dimensions=False,
                              helpers=[],instances=instances,label=old.get('label','Pattern') if old else 'Pattern %d'%(len(definitions)+1))
        write_records(sketch,definitions);index=editing.identities(sketch)
        mark(sketch,[index[t] for t in generated],True);plan(sketch)
        if sketch.solve()!=0:raise ValueError('The linked pattern could not be solved')
        doc.recompute()
        if _transaction:doc.commitTransaction()
        return key
    except Exception:
        if _transaction:doc.abortTransaction();sketch.solve()
        raise


def convert(sketch,group,ids,options):
    """Explicit, guarded legacy conversion; preserve output curve identities."""
    definitions=records(sketch);old,_,_=editing.load(sketch,group)
    selected=[str(sketch.GeometryFacadeList[i].Id) for i in ids]
    members=[i for i,c in enumerate(sketch.Constraints) if c.PatternGroup==group]
    import re
    names={c.Name for c in sketch.Constraints if c.PatternGroup==group and c.Name}
    for path,expression in sketch.ExpressionEngine:
        text=str(path)+' '+str(expression)
        if any(int(i) in members for i in re.findall(r'Constraints\[(\d+)\]',text)) or any(name in text for name in names):
            raise ValueError('Remove expressions referencing pattern constraints before conversion')
    helpers=set(old['helpers']);guard_removal(sketch,helpers,group)
    index=editing.identities(sketch)
    helper_tags={pattern.spacing_tag(sketch.GeometryFacadeList[index[t]]) for t in helpers}
    doc=sketch.Document;doc.openTransaction('Convert sketch pattern to linked')
    try:
        if members:sketch.delConstraints(members,False,True)
        definitions[group]=dict(old,behavior='linked',helpers=[],dimensions=False)
        write_records(sketch,definitions)
        if helpers:sketch.delGeometries(sorted(editing.identities(sketch)[t] for t in helpers),True)
        if 'PatternSpacingTags' in sketch.PropertiesList:
            sketch.PatternSpacingTags=[t for t in sketch.PatternSpacingTags if t not in helper_tags]
        index=editing.identities(sketch);mark(sketch,[index[t] for t in editing.owned(definitions[group])],True)
        if sketch.solve()!=0:raise ValueError('Remove constraints that feed pattern copies back into their source before conversion')
        index=editing.identities(sketch)
        result=save(sketch,[index[tag] for tag in selected],options,group,_transaction=False)
        doc.commitTransaction();return result
    except Exception:doc.abortTransaction();sketch.solve();raise


def independent(sketch,group):
    definitions=records(sketch);record=definitions.get(group)
    if not record or not is_linked(record):raise ValueError('Choose a linked pattern to make independent')
    if sketch.solve()!=0:raise ValueError('Resolve the sketch before making the pattern independent')
    doc=sketch.Document;doc.openTransaction('Make sketch pattern independent')
    try:
        index=editing.identities(sketch);mark(sketch,[index[t] for t in editing.owned(record)],False)
        del definitions[group];write_records(sketch,definitions)
        if sketch.solve()!=0:raise ValueError('Independent pattern geometry could not be solved')
        doc.recompute();doc.commitTransaction()
    except Exception:doc.abortTransaction();sketch.solve();raise
