import hashlib, json, shutil
from pathlib import Path
repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out = root/'validation/pattern-label-allocation-20261124'
manifest = []
for name in ('freecad_plus/sketch_pattern.py', 'TestPatternGroups.py'):
    source = repo/'src/Mod/FreeCADPlus'/name
    target = root/'app/Mod/FreeCADPlus'/name
    backup = out/'backups'/name
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists(): shutil.copy2(target, backup)
    shutil.copy2(source, target)
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest(source) == digest(target)
    manifest.append(dict(file=name, sha256=digest(target), backup_sha256=digest(backup)))
(out/'install-manifest.json').write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))
