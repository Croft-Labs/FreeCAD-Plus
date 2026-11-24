import json, shutil, hashlib
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
previous=root/'validation/pattern-memory-repro-20261124'
current=root/'validation/pattern-label-allocation-20261124'
dest=repo/'ai-instructions/evidence/pattern-label-allocation-20261124'
dest.mkdir(parents=True,exist_ok=True)
for source,cases in ((previous,('exact-inches-owner','source-fixed-inches-owner','source-fixed-shown-owner','source-dense-regression','installed-fixed-inches-owner')),
                     (current,('installed','fresh-reopen','shortcut'))):
    for case in cases:
        folder=dest/case;folder.mkdir(exist_ok=True)
        for name in ('result.json','process.json','phases.jsonl','tests.txt','grid20-timing.json','fixed-line-grid12-task-timing.json'):
            path=source/case/name
            if path.exists():shutil.copy2(path,folder/name)
shutil.copy2(current/'install-manifest.json',dest/'install-manifest.json')
for item in json.loads((current/'install-manifest.json').read_text()):
    assert hashlib.sha256((root/'app/Mod/FreeCADPlus'/item['file']).read_bytes()).hexdigest()==item['sha256']
for case in ('installed','fresh-reopen','shortcut'):
    assert json.loads((current/case/'result.json').read_text())['ok'],case
assert json.loads((previous/'installed-fixed-inches-owner/result.json').read_text())['ok']
assert not json.loads((previous/'exact-inches-owner/result.json').read_text())['ok']
original=Path('C:/Users/dgium/Desktop/linear pattern test.FCStd')
digest=hashlib.sha256(original.read_bytes()).hexdigest()
assert digest==hashlib.sha256((previous/'exact-inches-owner/input.FCStd').read_bytes()).hexdigest()
(dest/'original-preserved.json').write_text(json.dumps(dict(unchanged=True,sha256=digest),indent=2))
scripts=dest/'harness';scripts.mkdir(exist_ok=True)
for name in ('probe.py','probe.FCMacro','fix-suite.py','run.FCMacro','install-fix.py','reopen-dense.py','reopen-dense.FCMacro','fix-shortcut.py','collect-fix.py'):
    (scripts/name).write_text(Path(__file__).with_name(name).read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8')
print(dest)
