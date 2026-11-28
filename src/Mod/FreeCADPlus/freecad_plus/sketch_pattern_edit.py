# SPDX-License-Identifier: LGPL-2.1-or-later
"""Versioned pattern recipes and atomic edits retaining surviving geometry identities."""
import copy
import json
import math
import re
import FreeCAD as App
import Part
import Sketcher
from . import sketch_pattern as pattern

PROPERTY='PatternDefinitions'


def identities(sketch):
    # Native SketchGeometryExtension IDs are serialized; Part geometry Tags are not.
    return {str(f.Id):i for i,f in enumerate(sketch.GeometryFacadeList)}


def reference(sketch, value, encode=True):
    if value is None:return None
    if encode:
        geo,pos=value
        if geo>=0:return dict(id=str(sketch.GeometryFacadeList[geo].Id),pos=pos)
        if geo>=-2:return dict(axis=geo,pos=pos)
        # LinkSubList combines references to the same object and is not indexed
        # like ExternalGeo. Use the native persistent external geometry identity.
        facade=Sketcher.ExternalGeometryFacade(sketch.ExternalGeo[-geo-1])
        return dict(external_id=facade.Id,pos=pos)
    if 'id' in value:
        geo=identities(sketch).get(value['id'])
        if geo is None:raise ValueError('A saved pattern reference was deleted. Restore it before editing this pattern.')
    elif 'axis' in value:geo=value['axis']
    else:
        matches=[-i-1 for i,g in enumerate(sketch.ExternalGeo) if i>=2
                 and Sketcher.ExternalGeometryFacade(g).Id==value['external_id']
                 and not Sketcher.ExternalGeometryFacade(g).testFlag('Missing')]
        if len(matches)!=1:raise ValueError('A saved external pattern reference is no longer available.')
        geo=matches[0]
    return (geo,value['pos'])


def options_refs(sketch, options, encode=True):
    result=copy.deepcopy(options)
    if 'center' in result:result['center']=reference(sketch,result['center'],encode)
    for axis in ('d1','d2','angular','radial'):
        for key in ('reference','start','end'):
            if key in result.get(axis,{}):result[axis][key]=reference(sketch,result[axis][key],encode)
    return result


def slots(options):
    circular=options.get('pattern')=='Circular';layout=options.get('directions')
    if circular:
        a=pattern.extent_values(options['angular'],True) if layout!='Radial' else [0.]
        b=pattern.extent_values(options['radial']) if layout!='Angular' else [0.]
    else:
        a=pattern.extent_values(options['d1'])
        b=pattern.extent_values(options['d2']) if layout=='Two directions' else [0.]
    zeroa=next(i for i,v in enumerate(a) if abs(v)<pattern.EPS)
    zerob=next(i for i,v in enumerate(b) if abs(v)<pattern.EPS)
    return [(i-zeroa,j-zerob) for i,x in enumerate(a) for j,y in enumerate(b)
            if abs(x)>pattern.EPS or abs(y)>pattern.EPS]


def save_definition(sketch,group,ids,options,dimensions,instances,helpers):
    keys=[str(f.Id) for f in sketch.GeometryFacadeList]
    record=dict(version=1,inputs=[keys[i] for i in ids],options=options_refs(sketch,options),
                dimensions=bool(dimensions),helpers=[keys[i] for i in helpers],
                instances=[dict(slot=list(slot),geometry={keys[i]:keys[j] for i,j in mapping.items()})
                           for slot,mapping in zip(slots(options),instances)])
    if PROPERTY not in sketch.PropertiesList:
        sketch.addProperty('App::PropertyMap',PROPERTY,'Pattern','Saved sketch pattern definitions')
        sketch.setEditorMode(PROPERTY,2)
    definitions=dict(getattr(sketch,PROPERTY))
    previous=json.loads(definitions[group]) if group in definitions else {}
    record['label']=next((c.PatternLabel.split(' — ')[0] for c in sketch.Constraints if c.PatternGroup==group),
                         previous.get('label','Pattern %d'%(len(definitions)+1)))
    definitions[group]=json.dumps(record,separators=(',',':'))
    setattr(sketch,PROPERTY,definitions)


def owned(record):
    return set(record['helpers'])|{tag for instance in record['instances'] for tag in instance['geometry'].values()}


def driver_field(title,options):
    if title.startswith('Angular'):axis='angular'
    elif title.startswith('Radial'):axis='radial'
    elif title.startswith('Direction 1'):axis='d1'
    elif title.startswith('Direction 2'):axis='d2'
    else:return None
    extent=options.get(axis)
    if not extent:return None
    suffix='2' if '(−)' in title else ''
    return axis,suffix


def current_options(sketch,group,record):
    options=options_refs(sketch,record['options'],False)
    for c in sketch.Constraints:
        if c.PatternGroup!=group or not c.PatternDriver:continue
        field=driver_field(c.PatternDriver,options)
        if not field:continue
        axis,suffix=field;e=options[axis]
        pitch=math.degrees(c.Value) if axis=='angular' else c.Value
        spacing=e.get('spacing'+suffix,'Pitch');n=e.get('count'+suffix,2)
        divisor=n if axis=='angular' and spacing=='Total angle' and abs(e.get('value'+suffix,0)-360)<pattern.EPS else n-1
        e['value'+suffix]=pitch*divisor if spacing in ('Total distance','Total angle') else pitch
        if c.PresentationUnit:e['unit'+suffix]=c.PresentationUnit
    helper_tags=set(record['helpers'])
    options['hide_spacing']=any(pattern.visual_layer(f)==2 for f in sketch.GeometryFacadeList if str(f.Id) in helper_tags)
    return options


def load(sketch,group):
    raw=getattr(sketch,PROPERTY,{}).get(group)
    if not raw and not any(c.PatternGroup==group for c in sketch.Constraints):
        raise ValueError('This pattern group no longer exists. Undo its deletion before editing it.')
    record=json.loads(raw) if raw else recover(sketch,group)
    if record.get('version')!=1:raise ValueError('This pattern was saved by an unsupported recipe version.')
    indexed=identities(sketch)
    if any(t not in indexed for t in record['inputs']):raise ValueError('The original pattern geometry was deleted.')
    if any(t not in indexed for t in owned(record)):
        raise ValueError('Some pattern instances or spacing helpers were deleted. Undo that deletion before editing the pattern.')
    return record,[indexed[t] for t in record['inputs']],current_options(sketch,group,record)


def placement(transform):
    return App.Placement(transform[1],App.Rotation(App.Vector(0,0,1),transform[0]))


def update(sketch,group,ids,options,dimensions):
    record,_,old_options=load(sketch,group)
    ids=pattern.operation_geometry(sketch,ids)
    indexed=identities(sketch);facades=sketch.GeometryFacadeList
    input_tags=[str(facades[i].Id) for i in ids]
    all_owned=owned(record)
    if any(t in all_owned for t in input_tags):raise ValueError('Choose original geometry, not instances generated by this pattern.')
    new_options=options_refs(sketch,options)
    for axis in ('d1','d2','angular','radial'):
        for key in ('reference','start','end'):
            ref=new_options.get(axis,{}).get(key)
            if ref and ref.get('id') in all_owned:raise ValueError('A pattern direction cannot depend on its own generated geometry.')
    center=new_options.get('center')
    if center and center.get('id') in all_owned:raise ValueError('The rotation center cannot depend on this pattern\'s generated geometry.')
    transforms=pattern.transforms(sketch,options);new_slots=slots(options)
    old_transforms=dict(zip(slots(old_options),pattern.transforms(sketch,old_options)))
    previous={tuple(i['slot']):i['geometry'] for i in record['instances']}
    keep={tag for slot in new_slots for source,tag in previous.get(slot,{}).items() if source in input_tags}
    removed=all_owned-keep
    removed_ids={indexed[t] for t in removed}
    removed_spacing_tags={pattern.spacing_tag(facades[i]) for i in removed_ids}
    members=[i for i,c in enumerate(sketch.Constraints) if c.PatternGroup==group]
    cs=sketch.Constraints
    if any(c.PatternGroup!=group and any(g in removed_ids for g in (c.First,c.Second,c.Third)) for c in cs):
        raise ValueError('Removed instances or spacing helpers are used by other constraints. Remove those dependencies or keep their instance counts.')
    # Native expressions can depend on individual member indices/names. Never
    # silently discard authored expressions when rebuilding their equations.
    member_names={c.Name for c in cs if c.PatternGroup==group and c.Name}
    for path,expression in sketch.ExpressionEngine:
        match=re.fullmatch(r'Constraints\[(\d+)\]',str(path))
        if match and int(match[1]) in members:
            if cs[int(match[1])].PatternDriver:
                raise ValueError('This pitch has an expression. Remove its expression before changing the pattern definition.')
            continue
        if any(int(i) in members for i in re.findall(r'Constraints\[(\d+)\]',str(expression))) or any(name in str(expression) for name in member_names):
            raise ValueError('Another expression uses a pattern constraint. Remove that dependency before editing its definition.')
    # Explicit subelement consumers cannot be silently retargeted by deleting a
    # generated edge. Whole-sketch consumers (e.g. extrusion) remain supported.
    if removed_ids:
        for obj in sketch.InList:
            for name in obj.PropertiesList:
                if 'LinkSub' not in obj.getTypeIdOfProperty(name):continue
                value=getattr(obj,name);links=[value] if isinstance(value,tuple) else value
                for link in links or []:
                    if not isinstance(link,tuple) or len(link)!=2 or link[0]!=sketch:continue
                    if any(link[1]):raise ValueError('A downstream feature references individual sketch elements. Keep those references intact before removing pattern instances.')
    label=next((c.PatternLabel for c in cs if c.PatternGroup==group),record.get('label','Pattern'))
    doc=sketch.Document;doc.openTransaction('Edit Sketch Pattern')
    try:
        if record.get('behavior')=='linked':
            from . import sketch_pattern_linked as linked
            linked.mark(sketch,[indexed[tag] for tag in all_owned],False)
        if members:sketch.delConstraints(members,False,True)
        # Apply only relative rigid motion, retaining every surviving native tag.
        facades=sketch.GeometryFacadeList
        for slot,new_transform in zip(new_slots,transforms):
            if slot not in old_transforms:continue
            delta=placement(new_transform).multiply(placement(old_transforms[slot]).inverse()).toMatrix()
            for source,tag in previous.get(slot,{}).items():
                if tag in keep:facades[indexed[tag]].transform(delta)
        sketch.GeometryFacadeList=facades
        if removed_ids:sketch.delGeometries(sorted(removed_ids),True)
        if 'PatternSpacingTags' in sketch.PropertiesList:
            sketch.PatternSpacingTags=[t for t in sketch.PatternSpacingTags if t not in removed_spacing_tags]
        indexed=identities(sketch);ids=[indexed[t] for t in input_tags]
        reuse={n:{indexed[source]:indexed[tag] for source,tag in previous.get(slot,{}).items() if tag in keep}
               for n,slot in enumerate(new_slots)}
        options=options_refs(sketch,new_options,False)
        result=pattern.apply(sketch,ids,options,dimensions,_reuse=reuse,_identity=group,_label=label,_transaction=False)
        doc.commitTransaction();return result
    except Exception:
        doc.abortTransaction();sketch.solve();raise


def recover(sketch,group):
    from .sketch_pattern_legacy import recover_definition
    return recover_definition(sketch,group)
