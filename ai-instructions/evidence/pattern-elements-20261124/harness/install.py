import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/pattern-elements-20261124'
files=[(root/'build/Mod/Sketcher/SketcherGui.pyd','lib/SketcherGui.pyd')]
files += [(repo/'src/Mod/FreeCADPlus'/p,'Mod/FreeCADPlus/'+p) for p in
          ('TestPatternGroups.py','freecad_plus/sketch_pattern.py','freecad_plus/sketch_pattern_edit.py')]
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=[]
for source,relative in files:
    target=root/'app'/relative;backup=out/'backups'/relative
    previous=digest(target)
    backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists():shutil.copy2(target,backup)
    if target.suffix=='.pyd':
        retained=target.with_name(target.name+'.before-pattern-elements-20261124')
        if retained.exists():retained=target.with_name(target.name+'.before-pattern-elements-'+previous[:12])
        assert not retained.exists(),retained
        target.rename(retained)
    shutil.copy2(source,target)
    assert digest(source)==digest(target)
    manifest.append(dict(file=relative,sha256=digest(target),backup_sha256=digest(backup)))
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
