# SPDX-License-Identifier: LGPL-2.1-or-later
"""Mixed, earlier local sources for native linked sketch intersections."""
import FreeCAD as App
import Part
from . import document, planes, derived_geometry


def canonical(owner, sketch, ref):
    obj,sub=planes.canonical(owner,[ref])[0]
    if obj.TypeId=='PartDesign::Body':
        history=document.history(owner.Document,owner)
        earlier=set(history[:history.index(sketch)])
        obj=next((o for o in reversed(obj.Group) if o in earlier and hasattr(o,'Shape') and not o.Shape.isNull()),None)
        if obj is None:raise ValueError('Choose geometry before this sketch in History')
    route=document.owned_path(owner,obj)
    if not route or any(o.TypeId=='App::Link' for o in route):
        raise ValueError('Choose geometry owned by this component')
    history=document.history(owner.Document,owner)
    if obj not in history or sketch not in history or history.index(obj)>=history.index(sketch):
        raise ValueError('Choose an earlier History item in this component')
    document.require_predecessors(owner,sketch,[(obj,sub)])
    if obj==sketch or sketch in obj.OutListRecursive:raise ValueError('An intersection cannot depend on its own sketch')
    shape=planes.shape(owner,(obj,sub))
    if not shape.Faces and not shape.Edges:raise ValueError('Choose a solid, sheet, face, edge or earlier sketch curve')
    return obj,sub


def section(owner,sketch,refs):
    frame=owner.getGlobalPlacement().inverse().multiply(sketch.getGlobalPlacement())
    values=[]
    for ref in refs:
        ref=canonical(owner,sketch,ref);shape=planes.shape(owner,ref)
        local=shape.copy();local.Placement=frame.inverse().multiply(local.Placement)
        if not local.Faces and abs(local.BoundBox.ZMin)<1e-7 and abs(local.BoundBox.ZMax)<1e-7:
            raise ValueError('The curve lies in the sketch plane; select a curve that crosses it')
        size=max(1,local.BoundBox.DiagonalLength,abs(local.BoundBox.XMin),abs(local.BoundBox.XMax),abs(local.BoundBox.YMin),abs(local.BoundBox.YMax))*4
        plane=Part.makePlane(size*2,size*2,App.Vector(-size,-size,0))
        result=local.section(plane)
        if result.isNull() or not result.Vertexes:raise ValueError(ref[0].Label+' does not cross the sketch plane')
        if not local.Faces and result.Edges:raise ValueError('A curve overlaps the sketch plane; choose discrete crossings')
        result.Placement=frame.multiply(result.Placement);values.append(result)
    return values


def apply(owner,sketch,refs):
    refs=list(dict.fromkeys(canonical(owner,sketch,ref) for ref in refs))
    if not refs:raise ValueError('Select one or more sources')
    section(owner,sketch,refs)
    doc=sketch.Document
    # Match native sketch tools: finish the preceding edit operation and give
    # this Apply its own transaction while the outer sketch stays in edit.
    doc.openTransaction('Intersection curve')
    try:
        if 'PlusIntersectionSources' not in sketch.PropertiesList:
            sketch.addProperty('App::PropertyLinkSubListGlobal','PlusIntersectionSources','Intersection curve')
            sketch.setEditorMode('PlusIntersectionSources',2)
        saved=planes.flatten(sketch.PlusIntersectionSources)
        for obj,sub in refs:
            if (obj,sub) in saved:continue
            sketch.addExternal(obj.Name,sub,True,True)
            saved.append((obj,sub))
        sketch.PlusIntersectionSources=planes.links(saved);doc.recompute();sketch.solve()
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction();doc.recompute();raise
