"""Install verified staged payloads atomically, preserving owner settings and rollback."""
import hashlib,json,os,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/mesh-settings27';app=root/'app';runtime=out/'runtime'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((out/'build-result.json').read_text())['exit_code']==0
run=Path(json.loads((out/'latest-stage.json').read_text())['path'])
result=json.loads((run/'result.json').read_text())
assert result['ok'] and result['tests']>=8 and Path(result['runtime']).resolve()==runtime.resolve()
files=json.loads((out/'stage-manifest.json').read_text())
assert files
protected=list((root/'profiles/owner-test').glob('*.cfg'))+list((Path.home()/'Desktop').glob('*FreeCAD*.lnk'))
before={str(p):sha(p) for p in protected}
previous=out/'install-manifest.json'
prior=json.loads(previous.read_text()) if previous.exists() else None
if prior:
    assert prior['protected']==before
    for row in prior['files']:assert sha(app/row['path'])==row['installed']
manifest={'verified_run':str(run),'protected':before,'files':[]};done=[]
for relative,expected in files.items():
    assert (app/relative).resolve().is_relative_to(app.resolve())
    assert sha(runtime/relative)==expected
try:
    for relative,expected in files.items():
        target=app/relative;saved=out/('rollback-final' if prior else 'rollback')/relative
        old=sha(target) if target.exists() else None
        if old:saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
        target.parent.mkdir(parents=True,exist_ok=True)
        temporary=target.with_name(target.name+'.approved-install.tmp')
        shutil.copy2(runtime/relative,temporary);os.replace(temporary,target)
        done.append((target,saved,old))
        assert sha(target)==expected
        original=next((row['before'] for row in prior['files'] if row['path']==relative),old) if prior else old
        manifest['files'].append({'path':relative,'before':original,'installed':expected})
    assert before=={str(p):sha(p) for p in protected}
except BaseException:
    for target,saved,old in reversed(done):
        if old:
            temporary=target.with_name(target.name+'.rollback.tmp');shutil.copy2(saved,temporary);os.replace(temporary,target)
        else:target.unlink(missing_ok=True)
    raise
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'installed':len(files),'hashes_match':True,'owner_settings_and_shortcuts_preserved':True}))
