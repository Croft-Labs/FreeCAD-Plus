"""Install only the checked Python payload; retain exact rollback copies."""
import hashlib,json,shutil,os,ast
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/extract-join27';backup=out/'rollback'
names=['Init.py','TestJoinedExtraction.py']+['freecad_plus/'+n+'.py' for n in ('clone_ui','clone_task','derived_geometry')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=list((root/'profiles/owner-test').glob('*.cfg'))+list((Path.home()/'Desktop').glob('*FreeCAD*.lnk'))
before={str(p):sha(p) for p in protected}
previous=json.loads((out/'install-manifest.json').read_text()) if (out/'install-manifest.json').exists() else None
previous_files={item['path']:item for item in previous['files']} if previous else {}
if previous:assert before==previous['protected']
manifest={'protected':before,'files':[]};done=[]
try:
    for name in names:
        src=repo/'src/Mod/FreeCADPlus'/name;built=root/'build/Mod/FreeCADPlus'/name
        ast.parse(src.read_text(encoding='utf-8'));assert sha(src)==sha(built)
        dst=root/'app/Mod/FreeCADPlus'/name;saved=backup/name
        assert dst.resolve().is_relative_to((root/'app/Mod/FreeCADPlus').resolve())
        old=previous_files.get('Mod/FreeCADPlus/'+name)
        entry={'path':'Mod/FreeCADPlus/'+name,'source':str(src),'before':old['before'] if old else (sha(dst) if dst.exists() else None)}
        if not old and dst.exists():saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,saved)
        temp=dst.with_suffix('.extract-install.tmp');shutil.copy2(src,temp);os.replace(temp,dst)
        done.append((dst,saved,entry));assert sha(src)==sha(dst)
        entry['installed']=sha(dst);manifest['files'].append(entry)
    assert before=={str(p):sha(p) for p in protected}
except Exception:
    for dst,saved,entry in reversed(done):
        if entry['before'] is None:dst.unlink(missing_ok=True)
        else:shutil.copy2(saved,dst)
    raise
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'installed':len(names),'hashes_match':True,'settings_and_shortcut_unchanged':True}))
