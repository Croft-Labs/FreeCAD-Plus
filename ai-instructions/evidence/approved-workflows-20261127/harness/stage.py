import os,shutil,hashlib,json
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
source=Path(__file__).resolve().parents[1]/'FreeCAD-Plus'
out=root/'validation/approved-batch27';runtime=out/'runtime'
def link_missing(source,target):
    if not Path(target).exists():os.link(source,target)
    return target
shutil.copytree(root/'app',runtime,copy_function=link_missing,dirs_exist_ok=True,
    ignore=shutil.ignore_patterns('__pycache__','*.pdb','*.obj','*.pre-*','*.before-*','*.mapped-before-*'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
previous=out/'install-manifest.json'
manifest={row['path']:digest(runtime/row['path']) for row in json.loads(previous.read_text())['files']} if previous.exists() else {}
def stage(src,rel):
    target=runtime/rel;target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists() or digest(src)!=digest(target):
        temporary=target.with_suffix(target.suffix+'.new');shutil.copy2(src,temporary);os.replace(temporary,target)
    assert digest(src)==digest(target)
    if not (root/'app'/rel).exists() or digest(target)!=digest(root/'app'/rel):manifest[rel.as_posix()]=digest(target)
for src in (root/'build/bin').glob('*.dll'):
    if (root/'app/bin'/src.name).exists():stage(src,Path('bin')/src.name)
for mod in ('PartDesign','Sketcher','MeshPart','Mesh','Part','Material'):
    for src in (root/'build/Mod'/mod).glob('*.pyd'):
        if (root/'app/lib'/src.name).exists():stage(src,Path('lib')/src.name)
        elif (root/'app/bin'/src.name).exists():stage(src,Path('bin')/src.name)
        elif (root/'app/Mod'/mod/src.name).exists():stage(src,Path('Mod')/mod/src.name)
for src in (source/'src/Mod/FreeCADPlus').glob('*.py'):stage(src,Path('Mod/FreeCADPlus')/src.name)
for src in (source/'src/Mod/FreeCADPlus/freecad_plus').glob('*.py'):stage(src,Path('Mod/FreeCADPlus/freecad_plus')/src.name)
(out/'stage-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'changed_files':len(manifest),'native':[p for p in manifest if p.endswith(('.dll','.pyd'))]},indent=2))
