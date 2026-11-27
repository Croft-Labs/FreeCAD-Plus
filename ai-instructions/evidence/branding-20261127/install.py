from pathlib import Path
import hashlib,json,shutil,os,sys
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
source=root/'build/bin';target=root/'app/bin';base=root/'validation/branding27'
tag=sys.argv[1] if len(sys.argv)>1 else ''
backup=base/('rollback'+tag)
backup.mkdir(parents=True,exist_ok=True)
files=['FreeCAD.exe','FreeCADCmd.exe','FreeCAD.pyd','FreeCADGui.pyd','FreeCADBase.dll','FreeCADApp.dll','FreeCADGui.dll']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
protected=list((root/'profiles/owner-test').glob('*.cfg'))
before={str(p):sha(p) for p in protected};manifest={'files':[],'protected':before};done=[]
assert json.loads((base/('build-title' if tag else 'build-final')/'result.json').read_text())['ok']
try:
    for name in files:
        src=source/name;dst=target/name;saved=backup/name
        assert dst.resolve().is_relative_to(target.resolve())
        entry={'name':name,'before':sha(dst),'built':sha(src)}
        if entry['before']!=entry['built']:
            assert not saved.exists(),saved
            temp=target/(name+'.branding-install.tmp');shutil.copy2(src,temp)
            # Renaming preserves a running process's mapped old binary if present.
            dst.rename(saved);done.append((dst,saved));os.replace(temp,dst)
        assert sha(src)==sha(dst);entry['installed']=sha(dst);manifest['files'].append(entry)
    assert before=={str(p):sha(p) for p in protected}
except Exception:
    for dst,saved in reversed(done):
        if dst.exists():dst.unlink()
        saved.rename(dst)
    raise
(base/('install'+tag+'-manifest.json')).write_text(json.dumps(manifest,indent=2))
print(json.dumps({'verified':len(files),'replaced':len(done),'owner_settings_unchanged':True}))
