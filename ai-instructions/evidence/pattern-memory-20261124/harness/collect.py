import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
source=root/'validation/pattern-memory-20261124'
dest=repo/'ai-instructions/evidence/pattern-memory-20261124'
stages=('baseline-circle20-gui','installed-circle20-gui','installed-free-circle20',
        'build-regression','installed','fresh-reopen','shortcut','native')
for stage in stages:
    result=json.loads((source/stage/'result.json').read_text())
    assert result.get('ok',result.get('exit_code')==0),stage
    target=dest/stage;target.mkdir(parents=True,exist_ok=True)
    for name in ('result.json','tests.txt','process.json','host-memory.json','phases.jsonl',
                 'grid20-timing.json','grid12-edit-timing.json','fixed-line-grid12-task-timing.json'):
        path=source/stage/name
        if path.exists():shutil.copy2(path,target/name)
manifest=json.loads((source/'install-manifest.json').read_text())
for item in manifest:
    for path in (Path(item['source']),root/'app'/item['path']):
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
shutil.copy2(source/'install-manifest.json',dest/'install-manifest.json')
for name in ('native-memory.log','native-memory-final.log','native-memory-bounded.log'):
    text=(source/name).read_text(encoding='utf-8')
    (dest/name).write_text('\n'.join(line.rstrip() for line in text.splitlines())+'\n',encoding='utf-8')
harness=dest/'harness';harness.mkdir(exist_ok=True)
for path in Path(__file__).parent.iterdir():
    if path.suffix not in ('.py','.FCMacro'):continue
    text=path.read_text(encoding='utf-8-sig')
    (harness/path.name).write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip()+'\n',encoding='utf-8')
print(json.dumps(dict(verified_files=len(manifest),stages=list(stages))))
