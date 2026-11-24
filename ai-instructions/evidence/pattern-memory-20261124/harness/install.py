import hashlib,json,shutil,subprocess
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/pattern-memory-20261124'
native=[('Mod/Sketcher/SketcherGui.pyd','lib/SketcherGui.pyd'),('Mod/Sketcher/Sketcher.pyd','lib/Sketcher.pyd')]
files=[(root/'build'/source,dest) for source,dest in native]
changed=subprocess.check_output(['git','diff','--name-only'],cwd=repo,text=True).splitlines()
changed+=['src/Mod/FreeCADPlus/'+name for name in ('TestPatternEditing.py','freecad_plus/sketch_pattern_edit.py','freecad_plus/sketch_pattern_legacy.py')]
for name in sorted(set(changed)):
    if name.startswith('src/Mod/FreeCADPlus/') and name.endswith('.py'):
        files.append((repo/name,name[4:]))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest_path=out/'install-manifest.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else []
for source,relative in files:
    target=root/'app'/relative
    assert source.is_file(),source
    backup=out/'install-backup'/relative
    previous=digest(target) if target.exists() else None
    if previous==digest(source):continue
    entry=next((item for item in manifest if item['path']==relative),None)
    if target.exists() and entry is None:
        assert not backup.exists(),backup
        backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,backup)
        retained=target.with_name(target.name+'.before-pattern-memory-20261124')
        assert not retained.exists(),retained
        target.rename(retained)
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    assert digest(source)==digest(target)
    if entry is not None:entry['sha256']=digest(target)
    else:manifest.append(dict(source=str(source),path=relative,previous_sha256=previous,
                             sha256=digest(target),rollback=str(backup) if previous else None))
    (out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(installed=len(manifest),paths=[m['path'] for m in manifest]),indent=2))
