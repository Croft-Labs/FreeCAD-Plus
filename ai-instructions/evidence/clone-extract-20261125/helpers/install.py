import hashlib, json, os, shutil
from pathlib import Path
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out = root / 'validation/clone-extract-20261125'
files = [(repo/'src/Mod/FreeCADPlus'/name, 'Mod/FreeCADPlus/'+name) for name in ['Init.py', 'InitGui.py', 'TestDerivedGeometry.py', 'TestComponentBooleanInputs.py', 'TestComponentEligibility.py', 'TestFeatureCenteredModeling.py', 'TestComponentDisplay.py', 'freecad_plus/document.py', 'freecad_plus/external.py', 'freecad_plus/display.py', 'freecad_plus/derived_geometry.py', 'freecad_plus/clone_task.py', 'freecad_plus/clone_ui.py', 'freecad_plus/editing.py', 'freecad_plus/modeling.py', 'freecad_plus/selection_list.py', 'freecad_plus/panel.py', 'freecad_plus/geometry.py', 'freecad_plus/toolbar_layout.py']]

digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = []
previous = {item['file']: item for item in json.loads((out/'install-manifest.json').read_text())} if (out/'install-manifest.json').exists() else {}
for source, relative in files:
    target = root/'app'/relative
    staged = out/'staged'/relative
    staged.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, staged)
    assert digest(staged) == digest(source)
    retained = target.with_name(target.name+'.before-clone-extract-20261125')
    if relative not in previous and target.exists() and not retained.exists(): shutil.copy2(target, retained)
    manifest.append(dict(file=relative, source=str(source), sha256=digest(source),
                         rollback=str(retained) if retained.exists() else None))
installed = []
try:
    for entry in manifest:
        target = root/'app'/entry['file']; staged = out/'staged'/entry['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and digest(target) == entry['sha256']:
            continue
        try: os.replace(staged, target)
        except PermissionError:
            # Loaded Windows DLLs can be renamed while mapped by the owner's old process.
            parked = target.with_name(target.name+'.mapped-before-clone-extract-20261125')
            target.rename(parked)
            try: os.replace(staged, target)
            except BaseException:
                parked.rename(target); raise
        installed.append(entry)
        assert digest(target) == entry['sha256']
except BaseException:
    for entry in reversed(installed):
        target = root/'app'/entry['file']
        if entry['rollback']: shutil.copy2(entry['rollback'], target)
        else: target.unlink(missing_ok=True)
    raise
(out/'install-manifest.json').write_text(json.dumps(manifest, indent=2))
print(json.dumps({'installed':len(manifest),'verified':True}))
