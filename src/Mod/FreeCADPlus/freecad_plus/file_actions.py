# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit Parts file operations; preserve sources and existing placements."""
import os
import tempfile
from pathlib import Path
import FreeCAD as App
from . import document, external, hierarchy, naming


def unique_labels(host, definitions):
    used=naming.reserved(host); labels=[]
    for part in definitions:
        base=part.Label if hasattr(part,'Label') else str(part)
        name=base; suffix=2
        while naming.key(name) in used:
            name=f'{base} ({suffix})';suffix+=1
        used.add(naming.key(name));labels.append(name)
    return labels


def create_linked_file(host, filename):
    external._saved(host)
    if host.HasPendingTransaction or App.getActiveTransaction():
        raise ValueError('Finish the current operation first')
    path=Path(filename).expanduser().resolve()
    if path.suffix.lower()!='.cadprt':raise ValueError('Choose a .cadprt filename')
    if path.exists():raise ValueError('Choose a new filename; existing files are not replaced')
    if not path.parent.is_dir():raise ValueError('Choose an existing folder')
    previous=App.ActiveDocument;source=None;published=False
    try:
        with tempfile.TemporaryDirectory(prefix='.new-part-',dir=path.parent) as temporary:
            staged=Path(temporary)/path.name
            source=App.newDocument('NewPartFile',path.stem,hidden=True);source.UndoMode=1
            with document.transaction(source,'Create part file'):
                root=document.create_file_root(source)
                part=hierarchy._create_definition(root,unique_labels(host,[path.stem])[0])
                hierarchy._place_instance(root,part)
            document.save_document(source,staged)
            if os.name=='nt':os.rename(staged,path)
            else:os.link(staged,path)
            published=True;source.FileName=str(path)
            external.import_file(host,source)
        return source
    except Exception:
        if source is not None and not source.InList:
            App.closeDocument(source.Name)
            if published:path.unlink()
        raise
    finally:
        if previous and previous.Name in App.listDocuments():App.setActiveDocument(previous.Name)


def collect(definitions):
    """Follow native dependencies as well as nested component links."""
    selected=tuple(dict.fromkeys(definitions))
    if not selected:raise ValueError('This file has no parts to copy')
    pending=list(selected);found=[];seen=set();catalogs={}
    while pending:
        part=pending.pop(0)
        if part in seen:continue
        doc=part.Document
        if doc.HasPendingTransaction:raise ValueError('Finish source operations before copying')
        catalogs.setdefault(doc,tuple(document.validate(doc).Definitions))
        if part not in catalogs[doc]:raise ValueError('Choose component definitions')
        seen.add(part);found.append(part)
        for obj in (part,*part.OutListRecursive):
            source=obj.Document
            catalogs.setdefault(source,tuple(document.validate(source).Definitions))
            for owner in catalogs[source]:
                if owner not in seen and (obj==owner or document.owned_path(owner,obj) is not None):
                    pending.append(owner)
    return selected,found


def dependencies(definitions):
    selected,all_parts=collect(definitions)
    primary={part.Document for part in selected}
    return sorted({part.Document.FileName or part.Document.Label for part in all_parts if part.Document not in primary})


def _copy_material(source,target):
    if not App.GuiUp:return
    from . import appearance
    try:
        prop=appearance.material_property(target);values=appearance.materials(source)
        setattr(target.ViewObject,prop,values if prop=='ShapeAppearance' else values[0])
        for name in ('LineColor','PointColor','DisplayMode'):
            if name in source.ViewObject.PropertiesList and name in target.ViewObject.PropertiesList:
                setattr(target.ViewObject,name,getattr(source.ViewObject,name))
    except (AttributeError,ValueError,RuntimeError):
        pass


def _bake(source, destination, label):
    from . import appearance
    result=destination.addObject('App::Part','Component');result.Label=label
    def visit(part, transform, ancestry=()):
        if part in ancestry:raise ValueError('Circular component nesting')
        for obj in appearance.results(part):
            # Shapes carry the feature placement; replace it with the full owned
            # route so Body placement is included exactly once.
            route=document.owned_path(part,obj)
            sub=''.join(o.Name+'.' for o in route)
            local=App.Placement(part.getSubObject(sub,3))
            if obj.isDerivedFrom('Mesh::Feature'):
                target=destination.addObject('Mesh::Feature','Mesh');target.Mesh=obj.Mesh.copy()
            else:
                target=destination.addObject('Part::Feature','Shape');target.Shape=obj.Shape.copy()
            target.Placement=transform.multiply(local);target.Label=obj.Label
            result.addObject(target);_copy_material(obj,target)
        for link in part.Group:
            if link.TypeId=='App::Link':
                # Native subobject transform includes LinkTransform and source placement.
                frame=App.Placement(part.getSubObject(link.Name+'.',3))
                visit(link.LinkedObject,transform.multiply(frame),(*ancestry,part))
    visit(source,App.Placement())
    if App.GuiUp:result.Visibility=False
    return result


def copy_parts(host, definitions, *, bake=False):
    root=document.validate(host)
    selected,all_parts=collect(definitions)
    originals=selected if bake else all_parts
    labels=unique_labels(host,originals)
    before=set(host.Objects)
    with document.transaction(host,'Import independent parts'):
        if bake:
            copies=[_bake(part,host,label) for part,label in zip(originals,labels)]
        else:
            copies=host.copyObject(all_parts,True)
            if len(copies)!=len(all_parts):raise ValueError('Incomplete native dependency copy')
            for copied,label in zip(copies,labels):
                copied.Label=label
                if App.GuiUp:copied.Visibility=False
        created=set(host.Objects)-before
        if any(target not in created for obj in created for target in obj.OutList):
            raise ValueError('Copy retained an external dependency; no parts were imported')
        root.Definitions=[*root.Definitions,*copies]
    return tuple(copies)
