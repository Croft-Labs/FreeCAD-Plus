import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/spacing-units-20261124'
manifest=json.loads((out/'install-manifest.json').read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for source,relative in [(root/'build/bin/FreeCADGui.dll','bin/FreeCADGui.dll'),
                        (repo/'src/Mod/FreeCADPlus/TestSpacingUnits.py','Mod/FreeCADPlus/TestSpacingUnits.py'),
                        (repo/'src/Mod/FreeCADPlus/freecad_plus/sketch_pattern.py','Mod/FreeCADPlus/freecad_plus/sketch_pattern.py')]:
    target=root/'app'/relative
    before=next(m for m in manifest if m['path']==relative)
    assert digest(target)==before['sha256']
    backup=out/'delivery-first'/relative
    backup.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(target,backup)
    shutil.copy2(source,target)
    assert digest(target)==digest(source)
    before['sha256']=digest(target)
    before['source']=str(source)
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Final native editor and regression test installed; original rollback preserved.')
