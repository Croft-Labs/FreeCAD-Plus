import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/pattern-batching-20261124'
previous=json.loads((root/'validation/pattern-corrections-20261124/install-manifest.json').read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=[]
for relative in ('Mod/FreeCADPlus/freecad_plus/sketch_pattern.py','Mod/FreeCADPlus/TestPatternBatching.py'):
    source=repo/'src'/relative;target=root/'app'/relative
    backup=out/'install-backup'/relative
    assert not backup.exists(),str(backup)
    if target.exists():
        record=next(m for m in previous if m['path']==relative)
        assert digest(target)==record['sha256'],'Installed baseline changed'
        backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,backup)
    manifest.append(dict(path=relative,source=str(source),previous_sha256=digest(target) if target.exists() else None,
                         rollback=str(backup) if target.exists() else None,sha256=digest(source)))
    shutil.copy2(source,target)
    assert digest(target)==digest(source)
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Installed batching service and acceptance tests; original service backed up; hashes verified.')
