"""Install the checked scripts/native outputs; retain original and loaded images."""
import hashlib,json,os,shutil
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
runtime=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=runtime/'validation/shell-routing-20261123';backup=out/'install-backup'
scripts=('freecad_plus/extrude_task.py','freecad_plus/revolve_task.py','TestThickenWorkflow.py')
files={f'Mod/FreeCADPlus/{name}':repo/'src/Mod/FreeCADPlus'/name for name in scripts}
files['Mod/PartDesign/PartDesignGui.pyd']=None



def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
previous={row['path']:row for row in json.loads((out/'install-manifest.json').read_text())} if (out/'install-manifest.json').exists() else {}
manifest=[]
for relative,source in files.items():
    installed=Path('lib')/Path(relative).name if relative.endswith('.pyd') else Path(relative)
    built=runtime/'build'/relative;dest=runtime/'app'/installed;rollback=backup/installed
    assert built.is_file(),str(built)
    if source:assert digest(source)==digest(built),'Stale build script: '+relative
    assert dest.resolve().is_relative_to((runtime/'app').resolve())
    rollback.parent.mkdir(parents=True,exist_ok=True)
    prior=previous.get(str(installed),{}).get('previous_sha256',digest(dest) if dest.exists() else None)
    if dest.exists() and not rollback.exists():shutil.copy2(dest,rollback)
    if not dest.exists() or digest(dest)!=digest(built):
        staged=dest.with_name(dest.name+'.task-update');shutil.copy2(built,staged)
        loaded=backup/'loaded'/installed;loaded.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():
            if loaded.exists():
                loaded=loaded.with_name(loaded.name+'.'+digest(dest)[:12])
            assert not loaded.exists(),'Retained image already exists: '+str(loaded)
            os.rename(dest,loaded)
        try:os.rename(staged,dest)
        except BaseException:
            if not dest.exists() and loaded.exists():os.rename(loaded,dest)
            raise
    assert digest(dest)==digest(built)
    manifest.append(dict(path=str(installed),build_path=relative,source_sha256=digest(source) if source else None,
                         built_sha256=digest(built),installed_sha256=digest(dest),previous_sha256=prior,
                         rollback=str(rollback) if rollback.exists() else None))
    (out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(installed=len(manifest),manifest=str(out/'install-manifest.json'))))
