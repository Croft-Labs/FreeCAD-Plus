import hashlib,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/pattern-elements-20261124'
dest=repo/'ai-instructions/evidence/pattern-elements-20261124'
for stage in ('build-acceptance','build-delete','installed','installed-final','fresh-reopen','shortcut'):
    result=json.loads((out/stage/'result.json').read_text());assert result['ok'],(stage,result)
    folder=dest/stage;folder.mkdir(parents=True,exist_ok=True)
    for name in ('result.json','tests.txt','elements-grid12.png','elements-grid20.png',
                 'fixed-line-grid12-task-timing.json','grid20-timing.json'):
        path=out/stage/name
        if path.exists():shutil.copy2(path,folder/name)
for item in json.loads((out/'install-manifest.json').read_text()):
    assert hashlib.sha256((root/'app'/item['file']).read_bytes()).hexdigest()==item['sha256']
shutil.copy2(out/'install-manifest.json',dest/'install-manifest.json')
shutil.copy2(out/'build8.log',dest/'build.log')
scripts=dest/'harness';scripts.mkdir(exist_ok=True)
for name in ('build.py','run.py','run.FCMacro','install.py','reopen.py','reopen.FCMacro','shortcut.py','collect.py'):
    (scripts/name).write_text(Path(__file__).with_name(name).read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8')
print(dest)
