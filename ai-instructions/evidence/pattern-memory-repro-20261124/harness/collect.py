import json, shutil
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
source=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/pattern-memory-repro-20261124')
dest=repo/'ai-instructions/evidence/pattern-memory-repro-20261124'
dest.mkdir(parents=True,exist_ok=True)
for case in ('pictured-construction','pictured-owner','pictured-plus-owner','pictured-unsaved-owner','source-diagnostics','installed-diagnostics','shortcut'):
    folder=dest/case;folder.mkdir(exist_ok=True)
    for name in ('result.json','process.json','phases.jsonl','tests.txt'):
        path=source/case/name
        if path.exists():shutil.copy2(path,folder/name)
shutil.copy2(source/'install-manifest.json',dest/'install-manifest.json')
scripts=dest/'harness';scripts.mkdir(exist_ok=True)
for name in ('probe.py','probe.FCMacro','run.py','run.FCMacro','install.py','shortcut.py','collect.py'):
    (scripts/name).write_text(Path(__file__).with_name(name).read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8')
# Deliberately omit copied owner preferences, user launch log and document snapshots.
print(dest)
