import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
source=root/'validation/pattern-edit-20261124'
dest=repo/'ai-instructions/evidence/pattern-edit-20261124'
for stage in ('installed','fresh-reopen','shortcut','native'):
    result=json.loads((source/stage/'result.json').read_text())
    assert result.get('ok',result.get('exit_code')==0),stage
    target=dest/stage;target.mkdir(parents=True,exist_ok=True)
    for name in ('result.json','tests.txt','grid12-edit-timing.json','fixed-line-grid12-task-timing.json',
                 'pattern-edit-panel.png','pattern-edit-preview.png'):
        path=source/stage/name
        if path.exists():shutil.copy2(path,target/name)
manifest=json.loads((source/'install-manifest.json').read_text())
for item in manifest:
    assert hashlib.sha256((root/'app'/item['path']).read_bytes()).hexdigest()==item['sha256']
    assert hashlib.sha256(Path(item['source']).read_bytes()).hexdigest()==item['sha256']
shutil.copy2(source/'install-manifest.json',dest/'install-manifest.json')
build_log=(source/'build-final.log').read_text(encoding='utf-8')
(dest/'build.log').write_text('\n'.join(line.rstrip() for line in build_log.splitlines())+'\n',encoding='utf-8')
harness=dest/'harness';harness.mkdir(exist_ok=True)
for path in Path(__file__).parent.iterdir():
    if path.suffix not in ('.py','.FCMacro'):continue
    text=path.read_text(encoding='utf-8')
    (harness/path.name).write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip()+'\n',encoding='utf-8')
preview=dest/'preview';preview.mkdir(exist_ok=True)
session=root.parent/'app-render-companion/sessions/f191f8a6d7c9'
for name,target in [('baseline-1c21b1ca.png','baseline.png'),('candidate-e2e1bbc6.png','proposed.png')]:
    shutil.copy2(session/name,preview/target)
print(json.dumps(dict(installed=json.loads((source/'installed/result.json').read_text()),
    edit_seconds=json.loads((source/'installed/grid12-edit-timing.json').read_text()),verified_files=len(manifest))))
