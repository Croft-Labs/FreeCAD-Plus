"""Install the checked naming payload into the existing app, with exact rollback."""
import ast,hashlib,json,os,shutil,subprocess
from pathlib import Path
repo=Path(__file__).parents[1]/'FreeCAD-Plus'
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/result-names28'
run=Path(json.loads((out/'latest-stage.json').read_text())['path'])
assert json.loads((run/'result.json').read_text())['ok']
assert json.loads((out/'build-result.json').read_text())['exit_code']==0
changed=subprocess.check_output(['git','diff','--name-only'],cwd=repo,text=True).splitlines()
python=[p for p in changed if p.startswith('src/Mod/FreeCADPlus/') and p.endswith('.py')]
python+=['src/Mod/FreeCADPlus/'+p for p in ('TestResultNames.py','freecad_plus/result_names.py','freecad_plus/operation_task.py')]
# The preceding committed unit-persistence update was waiting for the owner app
# to close. This build includes it; deploy its dependencies with the naming UI.
pending=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','3cf7c1fa59'],cwd=repo,text=True).splitlines()
python=list(dict.fromkeys(python+[p for p in pending if p.startswith('src/Mod/FreeCADPlus/') and p.endswith('.py')]))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
entries=[]
for name in python:
    rel='Mod/FreeCADPlus/'+name.removeprefix('src/Mod/FreeCADPlus/')
    src=repo/name;built=root/'build'/rel;dst=root/'app'/rel
    ast.parse(src.read_text(encoding='utf-8'));assert sha(src)==sha(built),(name,'stale build')
    if dst.exists():
        baseline_ref='3cf7c1fa59^' if name in pending else 'HEAD'
        baseline=subprocess.check_output(['git','show',baseline_ref+':'+name],cwd=repo)
        assert dst.read_bytes().replace(b'\r\n',b'\n')==baseline.replace(b'\r\n',b'\n'), 'Concurrent installed change: '+name
    entries.append((rel,built,src))
entries.append(('bin/FreeCADGui.dll',root/'build/bin/FreeCADGui.dll',None))
entries.append(('lib/PartGui.pyd',root/'build/Mod/Part/PartGui.pyd',None))
assert all(built.is_file() for _,built,_ in entries)
protected=list((root/'profiles/owner-test').glob('*.cfg'))+list((Path.home()/'Desktop').glob('*FreeCAD*.lnk'))
before={str(p):sha(p) for p in protected};manifest={'protected':before,'files':[]};done=[]
try:
    for rel,built,src in entries:
        dst=root/'app'/rel;backup=out/'rollback'/rel
        assert dst.resolve().is_relative_to((root/'app').resolve())
        old=sha(dst) if dst.exists() else None
        if old:backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,backup)
        temp=dst.with_name(dst.name+'.result-names.tmp');shutil.copy2(built,temp);os.replace(temp,dst)
        done.append((dst,backup,old));assert sha(dst)==sha(built)
        manifest['files'].append(dict(path=rel,before=old,build=sha(built),installed=sha(dst),source=sha(src) if src else None))
    assert before=={str(p):sha(p) for p in protected}
except BaseException:
    for dst,backup,old in reversed(done):
        if old:shutil.copy2(backup,dst)
        else:dst.unlink(missing_ok=True)
    raise
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(installed=len(entries),hashes_match=True,settings_shortcuts_preserved=True)))
