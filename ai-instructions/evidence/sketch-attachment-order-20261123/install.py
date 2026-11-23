"""Install checked scripts/native outputs, retaining original and loaded-file backups."""
import hashlib,json,os,shutil
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
runtime=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=runtime/'validation/sketch-attachment-order-20261123';backup=out/'install-backup'
scripts=('freecad_plus/document.py','freecad_plus/geometry.py','TestPlaneHistoryWorkflow.py')
files={f'Mod/FreeCADPlus/{name}':repo/'src/Mod/FreeCADPlus'/name for name in scripts}
for name in ('bin/FreeCADBase.dll','bin/FreeCADApp.dll','bin/FreeCADGui.dll',
             'Mod/Material/Materials.pyd','Mod/Material/MatGui.pyd','Mod/Part/Part.pyd',
             'Mod/Part/PartGui.pyd','Mod/Sketcher/Sketcher.pyd','Mod/Sketcher/SketcherGui.pyd'):
    files[name]=None
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
previous={row['path']:row for row in json.loads((out/'install-manifest.json').read_text())} if (out/'install-manifest.json').exists() else {}
manifest=[]
for relative in files:
    installed=Path('lib')/Path(relative).name if relative.endswith('.pyd') else Path(relative)
    assert (runtime/'build'/relative).is_file(),relative
    assert (runtime/'app'/installed).is_file(),str(installed)
for relative,source in files.items():
    installed=Path('lib')/Path(relative).name if relative.endswith('.pyd') else Path(relative)
    built=runtime/'build'/relative;dest=runtime/'app'/installed;rollback=backup/installed
    assert built.is_file(),str(built)
    if source:assert digest(source)==digest(built),'Stale build script: '+relative
    assert dest.resolve().is_relative_to((runtime/'app').resolve())
    rollback.parent.mkdir(parents=True,exist_ok=True)
    prior=digest(rollback) if rollback.exists() else digest(dest)
    if dest.exists() and not rollback.exists():shutil.copy2(dest,rollback)
    if not dest.exists() or digest(dest)!=digest(built):
        staged=dest.with_name(dest.name+'.attachment-order-update')
        shutil.copy2(built,staged)
        loaded=backup/'loaded'/installed;loaded.parent.mkdir(parents=True,exist_ok=True)
        # Renaming retains the loaded image for an already-running owner process.
        # Do not overwrite a retained image or stop an owner application.
        if dest.exists():
            assert not loaded.exists(),'Retained image already exists: '+str(loaded)
            os.rename(dest,loaded)
        try:os.rename(staged,dest)
        except BaseException:
            if not dest.exists() and loaded.exists():os.rename(loaded,dest)
            raise
    assert digest(dest)==digest(built)
    manifest.append(dict(path=str(installed),build_path=relative,source_sha256=digest(source) if source else None,
                         built_sha256=digest(built),installed_sha256=digest(dest),
                         previous_sha256=prior,rollback=str(rollback),rollback_sha256=digest(rollback)))
    (out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(installed=len(manifest),manifest=str(out/'install-manifest.json'))))
