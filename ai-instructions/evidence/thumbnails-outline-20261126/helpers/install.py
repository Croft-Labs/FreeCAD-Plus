"""Install only rebuilt native dependencies/resources; retain rollback copies."""
import ctypes, hashlib, json, os, shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/thumbnails-outline-20261126'
files=[(root/'build/bin'/name,'bin/'+name) for name in
       ('FreeCADBase.dll','FreeCADApp.dll','FreeCADGui.dll','FreeCAD.exe','FreeCADCmd.exe','FreeCADGui.pyd')]
files += [(root/'build/Mod/Start'/name,'lib/'+name) for name in ('Start.pyd','StartGui.pyd')]
files += [(repo/'src/Main/icon.ico','bin/FreeCADPlus.ico')]
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=[]
for source,relative in files:
    target=root/'app'/relative; staged=out/'staged'/relative
    staged.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,staged)
    assert digest(source)==digest(staged)
    backup=target.with_name(target.name+'.before-thumbnails-outline-20261126')
    assert target.exists()
    if not backup.exists():shutil.copy2(target,backup)
    manifest.append(dict(file=relative,source=str(source),sha256=digest(source),rollback=str(backup)))
installed=[]
try:
    for entry in manifest:
        target=root/'app'/entry['file'];staged=out/'staged'/entry['file']
        if digest(target)==entry['sha256']:continue
        try:os.replace(staged,target)
        except PermissionError:
            parked=target.with_name(target.name+'.mapped-before-thumbnails-outline-20261126')
            target.rename(parked)
            try:os.replace(staged,target)
            except BaseException:
                parked.rename(target);raise
        installed.append(entry)
        assert digest(target)==entry['sha256']
except BaseException:
    for entry in reversed(installed):shutil.copy2(entry['rollback'],root/'app'/entry['file'])
    raise
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
ctypes.windll.shell32.SHChangeNotify(0x08000000,0,None,None)
print(json.dumps(dict(installed=len(manifest),verified=True)))
