"""Focused development installation with retained rollback copies and hashes."""
import hashlib,json,shutil
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
runtime=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=runtime/'validation/target-coordinate-20261123';backup=out/'install-backup'
source_files=['src/Mod/FreeCADPlus/freecad_plus/extrude_task.py',
              'src/Mod/FreeCADPlus/freecad_plus/revolve_task.py']

source_files.append('src/Mod/FreeCADPlus/TestTargetCoordinateWorkflow.py')
files={'bin/FreeCADApp.dll':None,'bin/FreeCADBase.dll':None}
for name in source_files:
    if name.startswith('src/Mod/FreeCADPlus/') and name.endswith('.py'):
        files[name[4:]]=repo/name
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=[]
for relative,source in sorted(files.items()):
    built=runtime/'build'/relative;dest=runtime/'app'/relative;rollback=backup/relative
    assert built.is_file(),str(built)
    if source:assert digest(source)==digest(built),'Build copy is stale: '+relative
    rollback.parent.mkdir(parents=True,exist_ok=True)
    prior=digest(dest) if dest.exists() else None
    if dest.exists() and not rollback.exists():shutil.copy2(dest,rollback)
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(built,dest)
    assert digest(dest)==digest(built)
    manifest.append(dict(path=relative,source_sha256=digest(source) if source else None,
                         built_sha256=digest(built),installed_sha256=digest(dest),previous_sha256=prior,
                         rollback=str(rollback) if rollback.exists() else None,
                         rollback_sha256=digest(rollback) if rollback.exists() else None))
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(installed=len(manifest),manifest=str(out/'install-manifest.json'))))
