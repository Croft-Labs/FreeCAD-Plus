from pathlib import Path
import hashlib,json,shutil,os
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
source=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus/src/Mod/FreeCADPlus')
target=root/'app/Mod/FreeCADPlus';backup=root/'validation/instance-views27/rollback';backup.mkdir(parents=True,exist_ok=True)
files=['freecad_plus/'+name+'.py' for name in ('assembly_ui','panel')]
files += [name+'.py' for name in ('TestInstanceDisplay',)]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
protected=list((root/'profiles/owner-test').glob('*.cfg'))+list((Path.home()/'Desktop').glob('*freecad*.lnk'))
before={str(p):sha(p) for p in protected};manifest={'files':[],'protected':before}
done=[]
try:
    for rel in files:
        src=source/rel;dst=target/rel;saved=backup/rel
        assert dst.resolve().is_relative_to(target.resolve())
        entry={'path':rel,'before':sha(dst) if dst.exists() else None}
        if dst.exists():
            saved.parent.mkdir(parents=True,exist_ok=True)
            if not saved.exists():shutil.copy2(dst,saved)
        temp=dst.with_suffix('.components-install.tmp');shutil.copy2(src,temp);os.replace(temp,dst);done.append((dst,saved,entry))
        assert sha(src)==sha(dst);entry['installed']=sha(dst);manifest['files'].append(entry)
    assert before=={str(p):sha(p) for p in protected}
except Exception:
    for dst,saved,entry in reversed(done):
        if entry['before'] is None:dst.unlink(missing_ok=True)
        else:shutil.copy2(saved,dst)
    raise
(backup.parent/'install-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'installed':len(files),'protected_unchanged':True,'manifest':str(backup.parent/'install-manifest.json')}))
