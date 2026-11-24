# SPDX-License-Identifier: LGPL-2.1-or-later
"""Recover an older grouped pattern from its connected native spacing geometry.

Older groups did not retain pitch-vs-total or symmetric-vs-balanced-two-sided
authoring choices. Recover an equivalent current layout, never guessed geometry.
"""
import math
import re
import FreeCAD as App
import Part
from . import sketch_pattern as p


def extent(values,angular=False):
    values=sorted(set(round(v,8) for v in values));negative=sorted(-v for v in values if v<-p.EPS)
    positive=[v for v in values if v>p.EPS]
    def pitch(side):
        if not side:return 0.
        d=side[0]
        if any(abs(value-(i+1)*d)>1e-5 for i,value in enumerate(side)):
            raise ValueError('The older pattern no longer has uniform spacing. Restore its spacing before editing.')
        return d
    a,b=pitch(positive),pitch(negative)
    e=dict(mode='One dimension',spacing='Angular pitch' if angular else 'Pitch',
           count=len(positive or negative)+1,value=a or b,reverse=not positive,
           unit='deg' if angular else 'mm')
    if positive and negative:
        e.update(mode='Two dimensions',count=len(positive)+1,value=a,count2=len(negative)+1,
                 value2=b,spacing2=e['spacing'],unit2=e['unit'],reverse=False)
    return e


def recover_definition(sketch,group):
    from .sketch_pattern_edit import options_refs
    constraints=[c for c in sketch.Constraints if c.PatternGroup==group]
    label=constraints[0].PatternLabel
    geometries=sketch.Geometry
    facades=sketch.GeometryFacadeList
    keys=[str(f.Id) for f in facades]
    spacing=set(getattr(sketch,'PatternSpacingTags',[]))
    mentioned={g for c in constraints for g in (c.First,c.Second,c.Third) if g>=0}
    helpers={i for i in mentioned if p.spacing_tag(facades[i]) in spacing}
    if not helpers:raise ValueError('This older pattern has no connected spacing chain from which to recover its definition.')
    endpoints={i:{} for i in helpers};centers=[]
    for c in constraints:
        if c.Type!='Coincident':continue
        for helper,pos,geo,point in ((c.First,c.FirstPos,c.Second,c.SecondPos),(c.Second,c.SecondPos,c.First,c.FirstPos)):
            if helper in helpers and geo not in helpers:
                endpoints[helper][pos]=(geo,point)
                if pos==3:centers.append((geo,point))
    edges=[];graph={}
    for i,ends in endpoints.items():
        if 1 not in ends or 2 not in ends:continue
        a,b=ends[1][0],ends[2][0]
        if a<0 or b<0:continue
        angle=math.degrees(geometries[i].LastParameter-geometries[i].FirstParameter) if isinstance(geometries[i],Part.ArcOfCircle) else 0.
        edges.append((a,b,angle,i))
        graph.setdefault(a,[]).append((b,angle));graph.setdefault(b,[]).append((a,-angle))
    if not graph:raise ValueError('The older pattern spacing topology cannot be recovered safely.')
    components=[];angles={};remaining=set(graph)
    while remaining:
        root=min(remaining);todo=[root];angles[root]=0.;component=set()
        while todo:
            a=todo.pop()
            if a in component:continue
            component.add(a)
            for b,delta in graph[a]:
                if b not in component:
                    angles[b]=angles[a]+delta;todo.append(b)
        remaining-=component;components.append((root,component))
    drivers=[c for c in constraints if c.PatternDriver]
    circular=any(c.PatternDriver.startswith(('Angular','Radial')) for c in drivers)
    angular=any(isinstance(geometries[i],Part.ArcOfCircle) for i in helpers)
    radial=any(c.PatternDriver.startswith('Radial') for c in drivers)
    def axis(title):
        candidates=[c for c in drivers if c.PatternDriver.startswith(title)]
        if not candidates:return None,None
        c=next((c for c in candidates if '(−)' not in c.PatternDriver),candidates[0]);i=c.First
        if not isinstance(geometries[i],Part.LineSegment):raise ValueError('The older pitch does not reference a spacing line.')
        vector=geometries[i].EndPoint-geometries[i].StartPoint
        vector.normalize()
        for relation in constraints:
            if relation.Type=='Parallel' and relation.Second==i and relation.First not in helpers:
                try:return p.direction(sketch,dict(reference=(relation.First,0))),dict(method='Axis or line',reference=(relation.First,0))
                except (ValueError,RuntimeError):pass
        if '(−)' in c.PatternDriver:vector=-vector
        return vector,dict(method='Vector',x=vector.x,y=vector.y)
    center=None;radial_vector=None
    if circular:
        if angular:
            if not centers:raise ValueError('The older circular pattern center cannot be recovered.')
            center_ref=centers[0];center,_=p.point_reference(sketch,center_ref)
            if any((p.point_reference(sketch,r)[0]-center).Length>1e-5 for r in centers):
                raise ValueError('The older pattern uses different rotation centers.')
        else:
            # A radial-only result has no stored rotation center. Recover its
            # exact linear layout instead of inventing a circular reference.
            circular=False
    if circular and radial:
        c=next(c for c in drivers if c.PatternDriver.startswith('Radial'))
        a=endpoints[c.First][1][0]
        vector=geometries[c.First].EndPoint-geometries[c.First].StartPoint
        radial_vector=App.Rotation(App.Vector(0,0,1),-angles[a]).multVec(vector);radial_vector.normalize()
        if '(−)' in c.PatternDriver:radial_vector=-radial_vector
        # Locate a real reference with this radial direction; no synthetic point.
        radial_ref=None
        for root,_ in components:
            for pos in p._positions(geometries[root]):
                v=sketch.getPoint(root,pos)-center
                if v.Length>p.EPS and v.cross(radial_vector).Length/v.Length<1e-5 and v.dot(radial_vector)>0:
                    radial_ref=(root,pos);break
            if radial_ref:break
        if radial_ref is None:raise ValueError('The older radial direction has no recoverable center/reference pair.')
    if not circular:
        d1,ref1=axis('Direction 1' if not radial else 'Radial');d2,ref2=axis('Direction 2')
        if d1 is None:raise ValueError('The older pattern has no recoverable pitch direction.')
    def coordinates(root,node):
        pos=p._positions(geometries[root])[0]
        original=sketch.getPoint(root,pos);point=sketch.getPoint(node,pos)
        if circular:
            angle=angles[node];back=App.Rotation(App.Vector(0,0,1),-angle).multVec(point-center)+center-original
            distance=back.dot(radial_vector) if radial else 0.
            residual=back-(radial_vector*distance if radial else App.Vector())
            if residual.Length>1e-5:raise ValueError('The older circular instances do not match their spacing chain.')
            return round(angle,8),round(distance,8)
        delta=point-original
        if d2 is None:
            a=delta.dot(d1);b=0.;residual=delta-d1*a
        else:
            det=d1.x*d2.y-d1.y*d2.x
            if abs(det)<p.EPS:raise ValueError('The older grid directions are parallel.')
            a=(delta.x*d2.y-delta.y*d2.x)/det;b=(d1.x*delta.y-d1.y*delta.x)/det
            residual=delta-d1*a-d2*b
        if residual.Length>1e-5:raise ValueError('The older instances do not match their spacing chain.')
        return round(a,8),round(b,8)
    root,nodes=components[0];coordinates0={node:coordinates(root,node) for node in nodes}
    av=sorted({a for a,b in coordinates0.values()});bv=sorted({b for a,b in coordinates0.values()})
    if len(av)*len(bv)!=len(nodes):raise ValueError('Some older pattern instances were removed or overlap.')
    expected=[int(v) for v in re.findall(r'\d+',label.split(' — ')[-1])]
    if expected and math.prod(expected)!=len(nodes):raise ValueError('The older group no longer matches its saved instance count.')
    if circular:
        options=dict(pattern='Circular',directions='Angular + radial' if radial else 'Angular',center=center_ref,angular=extent(av,True))
        if radial:options['radial']=dict(extent(bv),reference=radial_ref)
    else:
        options=dict(pattern='Linear',directions='Two directions' if d2 is not None else 'One direction',d1=dict(extent(av),**ref1))
        if d2 is not None:options['d2']=dict(extent(bv),**ref2)
    # Preserve explicit pitch units even though pitch/total authoring mode was not stored.
    for c in drivers:
        name='angular' if c.PatternDriver.startswith('Angular') else 'radial' if circular else 'd2' if c.PatternDriver.startswith('Direction 2') else 'd1'
        if name in options and c.PresentationUnit:options[name]['unit2' if '(−)' in c.PatternDriver else 'unit']=c.PresentationUnit
    options['hide_spacing']=any(p.visual_layer(facades[i])==2 for i in helpers)
    ordered_a=p.extent_values(options['angular'],True) if circular else p.extent_values(options['d1'])
    ordered_b=p.extent_values(options['radial']) if circular and radial else p.extent_values(options['d2']) if not circular and d2 is not None else [0.]
    ai={round(value,8):i-ordered_a.index(0.) for i,value in enumerate(ordered_a)}
    bi={round(value,8):i-ordered_b.index(0.) for i,value in enumerate(ordered_b)}
    instances={}
    for root,nodes in components:
        if len(nodes)!=len(coordinates0):raise ValueError('The older pattern has incomplete source geometry.')
        for node in nodes:
            a,b=coordinates(root,node)
            if a not in ai or b not in bi:raise ValueError('The older pattern has inconsistent instance positions.')
            slot=(ai[a],bi[b])
            if slot!=(0,0):instances.setdefault(slot,{})[keys[root]]=keys[node]
    return dict(version=1,recovered=True,inputs=[keys[root] for root,_ in components],
                options=options_refs(sketch,options),dimensions=True,helpers=[keys[i] for i in sorted(helpers)],
                instances=[dict(slot=list(slot),geometry=mapping) for slot,mapping in sorted(instances.items())])
