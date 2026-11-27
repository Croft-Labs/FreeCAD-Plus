# SPDX-License-Identifier: LGPL-2.1-or-later
"""Read-only search and explicit identity-checked native file relocation."""
import json
import os
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import FreeCAD as App
from . import document, external

FOLDERS='FreeCADPlus.SearchFolders'
_relocations={}


class _Observer:
    def slotDeletedDocument(self, doc):
        _relocations.pop(doc,None)


_observer=_Observer()
App.addDocumentObserver(_observer)


def pending(doc):
    return _relocations.get(doc,{})


def verify(filename, missing):
    path=Path(filename).resolve()
    if path.suffix.lower()!='.cadprt' or not path.is_file():return False
    try:
        with zipfile.ZipFile(path) as archive:tree=ET.fromstring(archive.read('Document.xml'))
        uid=tree.find("./Properties/Property[@name='Uid']/Uuid")
        names={obj.get('name') for obj in tree.findall('./Objects/Object')}
        return (uid is not None and uid.get('value')==missing.uid
                and set(missing.names)<=names)
    except (OSError,KeyError,ValueError,zipfile.BadZipFile,ET.ParseError):return False


def search(folders, missing, recursive=True, stopped=lambda:False, error=lambda path,message:None):
    """Yield candidate paths without following junctions/symlinks or opening CAD docs."""
    seen=set()
    for folder in folders:
        if stopped():return
        def onerror(exc):error(str(getattr(exc,'filename',folder)),str(exc))
        for parent,dirs,files in os.walk(folder,followlinks=False,onerror=onerror):
            if stopped():return
            dirs[:]=[name for name in dirs if not Path(parent,name).is_symlink()
                     and not (hasattr(Path(parent,name),'is_junction') and Path(parent,name).is_junction())]
            for name in files:
                if stopped():return
                if Path(name).suffix.lower()!='.cadprt':continue
                path=Path(parent,name).resolve()
                if path in seen:continue
                seen.add(path)
                verified=verify(path,missing)
                if verified or name.casefold()==missing.path.name.casefold():yield str(path),verified
            if not recursive:break


def remembered(doc):
    try:return list(json.loads(doc.Meta.get(FOLDERS,'[]')))
    except (ValueError,TypeError):return []


def remember(doc,folders):
    meta=dict(doc.Meta);meta[FOLDERS]=json.dumps(list(dict.fromkeys(folders)));doc.Meta=meta


def relocate_loaded(source, filename):
    """Relocate the loaded defining document; its native object links stay intact."""
    missing=external.MissingReference(source.FileName,str(source.Uid),[o.Name for o in source.Objects])
    path=Path(filename).resolve()
    if not verify(path,missing):raise ValueError('Choose the same file identity with all required objects')
    external.archive_graph(path)
    if any(other!=source and other.FileName and Path(other.FileName).resolve()==path for other in App.listDocuments().values()):
        raise ValueError('That path is already open as another document')
    old=source.FileName
    references=[]
    def refers(value):
        if hasattr(value,'Document'):return value.Document==source
        return isinstance(value,(tuple,list)) and any(refers(v) for v in value)
    for doc in App.listDocuments().values():
        for obj in doc.Objects:
            for name in obj.PropertiesList:
                kind=obj.getTypeIdOfProperty(name)
                if 'XLink' not in kind:continue
                value=getattr(obj,name)
                if refers(value):
                    if 'Immutable' in obj.getPropertyStatus(name):
                        raise ValueError('A reference is read-only; relocation was not applied')
                    references.append((doc,obj,name,kind,value))
    changed_docs={doc for doc,obj,name,kind,value in references}
    try:
        source.FileName=str(path)
        # Native XLinks cache a DocInfo keyed by the old path. Reassign the
        # same targets to refresh that cache without replacing object identities.
        for doc,obj,name,kind,value in references:
            setattr(obj,name,[] if 'List' in kind else None)
            setattr(obj,name,value)
        document.validate(source)
        for doc in changed_docs:
            document.validate(doc)
            _relocations.setdefault(doc,{})[Path(old).resolve()]=path
        if App.GuiUp:
            import FreeCADGui as Gui
            for doc in [source,*source.InList]:
                gui=Gui.getDocument(doc.Name)
                if gui:gui.Modified=True
    except Exception:
        source.FileName=old
        for doc,obj,name,kind,value in references:
            setattr(obj,name,[] if 'List' in kind else None);setattr(obj,name,value)
        raise


def open_resolved(filename, replacements, *, hidden=False):
    """Validate first, restore private archive copies, keep originals untouched.

    Only XLink file attributes change in staging. Native restore retains UUIDs,
    object IDs, shape streams and normal link resolution. Changes become durable
    only on the user's next normal save of affected documents.
    """
    path=Path(filename).resolve()
    replacements={Path(a).resolve():Path(b).resolve() for a,b in replacements.items()}
    graph=external.archive_graph(path,replacements)
    before=set(App.listDocuments());previous=App.ActiveDocument
    for saved,info in graph.items():
        for doc in App.listDocuments().values():
            actual=Path(doc.FileName).resolve() if doc.FileName else None
            if (actual==saved)!=(str(doc.Uid)==info['uid']):
                raise ValueError('An open file conflicts with a recovered file identity')
    opened={}
    try:
        with tempfile.TemporaryDirectory(prefix='freecad-recovery-') as temporary:
            # archive_graph insertion order is dependency first.
            for index,(saved,info) in enumerate(graph.items()):
                existing=next((d for d in App.listDocuments().values() if str(d.Uid)==info['uid']),None)
                if existing:opened[saved]=existing;continue
                with zipfile.ZipFile(saved) as source:
                    tree=ET.fromstring(source.read('Document.xml'))
                    changed=False
                    for link in tree.findall('.//XLink'):
                        if link.get('file'):
                            old=(saved.parent/link.get('file')).resolve()
                            target=replacements.get(old,old)
                            changed |= target!=old
                            link.set('file',str(target))
                    staged=Path(temporary)/(str(index)+'.cadprt')
                    with zipfile.ZipFile(staged,'w',compression=zipfile.ZIP_DEFLATED) as output:
                        for item in source.infolist():
                            output.writestr(item,ET.tostring(tree,encoding='utf-8',xml_declaration=True)
                                            if item.filename=='Document.xml' else source.read(item.filename))
                doc=App.openDocument(str(staged),hidden=True)
                doc.FileName=str(saved);document.validate(doc);opened[saved]=doc
                if changed:_relocations[doc]=dict(replacements)
                if App.GuiUp:
                    import FreeCADGui as Gui
                    gui=Gui.getDocument(doc.Name)
                    if gui:gui.Modified=changed
            result=opened[path]
            if App.GuiUp and not hidden:
                import FreeCADGui as Gui
                App.setActiveDocument(result.Name)
                Gui.getDocument(result.Name).createView('Gui::View3DInventor')
                from . import editing
                editing.initialize_document(result)
            return result
    except Exception:
        for name in reversed(list(App.listDocuments())):
            if name not in before:App.closeDocument(name)
        raise
    finally:
        if hidden and previous and previous.Name in App.listDocuments():App.setActiveDocument(previous.Name)
