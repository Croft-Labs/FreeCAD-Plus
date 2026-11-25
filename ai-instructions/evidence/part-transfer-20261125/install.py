"""Install this checked update into the existing owner payload, retaining rollback files."""
import hashlib,json,os,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/part-transfer-20261125';out.mkdir(parents=True,exist_ok=True)
entries=[]
for name in ('freecad_plus/component_add.py','freecad_plus/part_transfer.py',
             'freecad_plus/part_transfer_ops.py','freecad_plus/panel.py',
             'freecad_plus/hierarchy.py','freecad_plus/external.py',
             'freecad_plus/document_import.py','TestPartTransfer.py','TestAddComponent.py'):
    entries.append((repo/'src/Mod/FreeCADPlus'/name,'Mod/FreeCADPlus/'+name))

digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
manifest_path=out/'install-manifest.json'
prior={e['file']:e for e in json.loads(manifest_path.read_text())} if manifest_path.exists() else {}
manifest=[];installed=[]
for source,relative in entries:
    target=root/'app'/relative;backup=out/'backups'/relative;staged=out/'staged'/relative
    backup.parent.mkdir(parents=True,exist_ok=True);staged.parent.mkdir(parents=True,exist_ok=True)
    if relative not in prior and target.exists():shutil.copy2(target,backup)
    shutil.copy2(source,staged);assert digest(source)==digest(staged)
    manifest.append(dict(file=relative,source=str(source),sha256=digest(staged),
                         backup_sha256=digest(backup) if backup.exists() else None))
try:
    for entry in manifest:
        relative=entry['file'];target=root/'app'/relative;staged=out/'staged'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        temporary=target.with_name(target.name+'.part-transfer-update.tmp')
        shutil.copy2(staged,temporary);os.replace(temporary,target);installed.append(relative)
        assert digest(target)==entry['sha256']
except BaseException:
    for relative in reversed(installed):
        target=root/'app'/relative;backup=out/'backups'/relative
        if backup.exists():shutil.copy2(backup,target)
        else:target.unlink(missing_ok=True)
    raise
manifest_path.write_text(json.dumps(manifest,indent=2))
print(json.dumps({'installed':len(manifest),'manifest':str(manifest_path)},indent=2))
