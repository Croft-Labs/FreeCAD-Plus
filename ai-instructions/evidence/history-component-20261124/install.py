import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/history-component-20261124';manifest=[]
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for relative in ('freecad_plus/panel.py','TestComponentRename.py','TestComponentPanel.py','TestPlaneHistoryWorkflow.py','TestFeatureCenteredModeling.py'):
    source=repo/'src/Mod/FreeCADPlus'/relative;target=root/'app/Mod/FreeCADPlus'/relative
    backup=out/'backups'/relative;backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists():shutil.copy2(target,backup)
    shutil.copy2(source,target);assert digest(source)==digest(target)
    manifest.append(dict(file=relative,sha256=digest(target),backup_sha256=digest(backup)))
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
