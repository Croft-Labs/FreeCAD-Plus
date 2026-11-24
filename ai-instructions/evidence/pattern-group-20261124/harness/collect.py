import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
source=root/'validation/pattern-group-20261124'
dest=repo/'ai-instructions/evidence/pattern-group-20261124'
for stage in ('installed','installed-mirror','fresh-reopen','shortcut','native'):
    result=json.loads((source/stage/'result.json').read_text())
    assert result.get('ok',result.get('exit_code')==0),stage
    target=dest/stage;target.mkdir(parents=True,exist_ok=True)
    for name in ('result.json','tests.txt','grid12-timing.json','grid12-task-timing.json',
                 'fixed-line-grid12-timing.json','fixed-line-grid12-task-timing.json',
                 'pattern-shown.png','pattern-hidden.png','pattern-list.png'):
        path=source/stage/name
        if path.exists():shutil.copy2(path,target/name)
manifest=json.loads((source/'install-manifest.json').read_text())
for item in manifest:
    assert hashlib.sha256((root/'app'/item['path']).read_bytes()).hexdigest()==item['sha256']
    assert hashlib.sha256(Path(item['source']).read_bytes()).hexdigest()==item['sha256']
shutil.copy2(source/'install-manifest.json',dest/'install-manifest.json')
shutil.copy2(source/'final-build.log',dest/'build.log')
harness=dest/'harness';harness.mkdir(exist_ok=True)
for name in ('run.py','run.FCMacro','install.py','reopen.py','reopen.FCMacro','shortcut.py','native.py','build.py','collect.py'):
    text=Path(__file__).with_name(name).read_text(encoding='utf-8')
    (harness/name).write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip()+'\n',encoding='utf-8')
benchmark=root/'validation/pattern-performance-20261124/source-grid12-line-rigid'
target=dest/'initial-profile';target.mkdir(exist_ok=True)
for name in ('result.json','profile.txt','solves.jsonl'):
    if (benchmark/name).exists():shutil.copy2(benchmark/name,target/name)
timing=json.loads((source/'shortcut/fixed-line-grid12-task-timing.json').read_text())
print(json.dumps(dict(installed_tests=79,native_tests=88,shortcut_tests=2,
                     shortcut_line_seconds=timing['seconds'],verified_installed_files=len(manifest))))
