import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/add-component-20261124';out.mkdir(parents=True,exist_ok=True)
manifest_path=out/'install-manifest.json'
prior={entry['file']:entry for entry in json.loads(manifest_path.read_text())} if manifest_path.exists() else {}
manifest=[]
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for relative in ('freecad_plus/component_add.py','freecad_plus/hierarchy.py','freecad_plus/external.py',
                 'freecad_plus/toolbars.py','TestAddComponent.py','TestPlusToolbars.py'):
    source=repo/'src/Mod/FreeCADPlus'/relative;target=root/'app/Mod/FreeCADPlus'/relative
    backup=out/'backups'/relative;backup.parent.mkdir(parents=True,exist_ok=True)
    if relative not in prior and target.exists():shutil.copy2(target,backup)
    shutil.copy2(source,target);assert digest(source)==digest(target)
    manifest.append(dict(file=relative,sha256=digest(target),backup_sha256=digest(backup) if backup.exists() else None))
manifest_path.write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
