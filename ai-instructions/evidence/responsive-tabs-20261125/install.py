import hashlib, json, os, shutil
from pathlib import Path
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
source = repo/'src/Mod/FreeCADPlus/freecad_plus/panel.py'
target = root/'app/Mod/FreeCADPlus/freecad_plus/panel.py'
out = root/'validation/responsive-tabs-20261125'
backup = out/'backups/panel.py'; backup.parent.mkdir(parents=True, exist_ok=True)
if not backup.exists(): shutil.copy2(target, backup)
temporary = target.with_name('panel.py.tab-sizing.tmp')
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
shutil.copy2(source, temporary)
assert digest(temporary) == digest(source)
try:
    os.replace(temporary, target)
    assert digest(target) == digest(source)
except BaseException:
    shutil.copy2(backup, target)
    raise
result = {'source':str(source), 'target':str(target), 'sha256':digest(target),
          'backup':str(backup), 'backup_sha256':digest(backup)}
(out/'install-manifest.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
