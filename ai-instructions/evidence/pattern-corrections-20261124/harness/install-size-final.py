import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/pattern-corrections-20261124'
manifest=json.loads((out/'install-manifest.json').read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for relative in ('Mod/FreeCADPlus/freecad_plus/sketch_pattern.py','Mod/FreeCADPlus/TestPatternCorrections.py'):
    target=root/'app'/relative;source=repo/'src'/relative
    record=next(m for m in manifest if m['path']==relative)
    assert digest(target)==record['sha256']
    backup=out/'first-installed'/relative;backup.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(target,backup);shutil.copy2(source,target)
    assert digest(target)==digest(source)
    record['sha256']=digest(target)
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Installed final size handling; original rollback retained.')
