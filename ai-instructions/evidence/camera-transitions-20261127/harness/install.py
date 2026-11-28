"""Install the checked native camera library and regression test, with rollback."""
import ast,hashlib,json,os,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/camera-activation27';backup=out/'rollback'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((out/'build-result.json').read_text())['exit_code']==0
assert sha(root/'build/bin/FreeCADGui.dll')==json.loads((out/'stage-manifest.json').read_text())['FreeCADGui.dll']
test=repo/'src/Mod/FreeCADPlus/TestCameraTransitions.py';ast.parse(test.read_text())
assert sha(test)==sha(root/'build/Mod/FreeCADPlus/TestCameraTransitions.py')
protected=list((root/'profiles/owner-test').glob('*.cfg'))+list((Path.home()/'Desktop').glob('*FreeCAD*.lnk'))
before={str(p):sha(p) for p in protected}
files=[(root/'build/bin/FreeCADGui.dll','bin/FreeCADGui.dll'),(test,'Mod/FreeCADPlus/TestCameraTransitions.py')]
manifest={'protected':before,'files':[]};done=[]
if (out/'install-manifest.json').exists():raise RuntimeError('Inspect existing installation manifest before reinstalling')
try:
    for source,relative in files:
        target=root/'app'/relative;saved=backup/relative
        assert target.resolve().is_relative_to((root/'app').resolve())
        old=sha(target) if target.exists() else None
        if old:saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
        temp=target.with_name(target.name+'.camera-install.tmp');shutil.copy2(source,temp)
        os.replace(temp,target);done.append((target,saved,old))
        assert sha(target)==sha(source)
        manifest['files'].append({'path':relative,'before':old,'installed':sha(target)})
    assert before=={str(p):sha(p) for p in protected}
except BaseException:
    for target,saved,old in reversed(done):
        if old:shutil.copy2(saved,target)
        else:target.unlink(missing_ok=True)
    raise
(out/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'installed':len(files),'hashes_match':True,'owner_settings_and_shortcut_preserved':True}))
