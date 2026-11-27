from pathlib import Path
import hashlib, json, shutil, os

root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
target=root/'app';backup=root/'validation/pending27/rollback'
backup.mkdir(parents=True,exist_ok=True)
prefix='src/Mod/FreeCADPlus/'
modules=('appearance_task','appearance_ui','clone_task','curve_selection','editing','extrude_task',
         'geometry','isolation','movement','panel','plane_task','selection_toolbar','shell_task',
         'sketch_pattern_task','thicken_task','toolbars','appearance_highlight','selection_scope','surface_selection')
tests=('TestAppearance','TestInstanceDisplay','TestMoveWorkflow','TestSketchPattern','TestSketchSymmetry','TestPendingWorkflows')
names=['freecad_plus/'+name+'.py' for name in modules]+[name+'.py' for name in tests]
files=[(repo/prefix/name,'Mod/FreeCADPlus/'+name) for name in names]
native=('bin/FreeCADGui.dll','Mod/Part/Part.pyd','Mod/Part/PartGui.pyd',
        'Mod/Sketcher/Sketcher.pyd','Mod/Sketcher/SketcherGui.pyd','Mod/PartDesign/PartDesignGui.pyd')
files.extend((root/'build'/name,'lib/'+Path(name).name if name.startswith('Mod/') else name) for name in native)
assert len(files)==len(set(name for _,name in files))

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
previous_path=backup.parent/'install-manifest.json'
previous=json.loads(previous_path.read_text()) if previous_path.exists() else {'files':[]}
previous_files={entry['path']:entry for entry in previous['files']}
# CMake installs native extension modules into lib, not the build's Mod folders.
# Remove only verified files introduced by this run at the incorrect shadow paths.
removed=[]
for name in native:
    entry=previous_files.get(name)
    if not name.startswith('Mod/') or entry is None:continue
    dst=target/name
    assert entry['before'] is None and dst.resolve().is_relative_to(target.resolve())
    assert sha(dst)==entry['installed']
    dst.unlink();removed.append(name)
protected=list((root/'profiles/owner-test').glob('*.cfg'))+list((Path.home()/'Desktop').glob('*FreeCAD*.lnk'))
before={str(p):sha(p) for p in protected}
manifest={'files':[],'protected':before,'removed_shadow_modules':removed};done=[]
if previous_path.exists() and not (backup.parent/'install-initial-layout.json').exists():
    shutil.copy2(previous_path,backup.parent/'install-initial-layout.json')
try:
    for src,rel in files:
        dst=target/rel;saved=backup/rel
        assert dst.resolve().is_relative_to(target.resolve())
        assert saved.resolve().is_relative_to(backup.resolve())
        assert src.is_file()
        original=previous_files[rel]['before'] if rel in previous_files else (sha(dst) if dst.exists() else None)
        entry={'path':rel,'source':str(src),'before':original}
        if dst.exists():
            saved.parent.mkdir(parents=True,exist_ok=True)
            if not saved.exists():shutil.copy2(dst,saved)
        temp=dst.with_suffix('.pending-install.tmp')
        shutil.copy2(src,temp);os.replace(temp,dst);done.append((dst,saved,entry))
        assert sha(src)==sha(dst)
        entry['installed']=sha(dst);manifest['files'].append(entry)
    assert before=={str(p):sha(p) for p in protected}
except Exception:
    for dst,saved,entry in reversed(done):
        if entry['before'] is None:dst.unlink(missing_ok=True)
        else:shutil.copy2(saved,dst)
    raise
(backup.parent/'install-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'installed':len(files),'protected_unchanged':True,'manifest':str(backup.parent/'install-manifest.json')}))
