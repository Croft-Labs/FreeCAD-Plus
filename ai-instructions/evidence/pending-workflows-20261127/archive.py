from pathlib import Path
import ast, hashlib, json, shutil

repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
base=root/'validation/pending27'
out=repo/'ai-instructions/evidence/pending-workflows-20261127'
out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((base/'install-manifest.json').read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for entry in manifest['files']:
    assert sha(root/'app'/entry['path'])==entry['installed']==sha(Path(entry['source'])),entry['path']
    if entry['source'].endswith('.py'):ast.parse(Path(entry['source']).read_text(encoding='utf-8-sig'))
for path,value in manifest['protected'].items():assert sha(Path(path))==value,path
for path in manifest['removed_shadow_modules']:assert not (root/'app'/path).exists()
verified={'installed_hashes':len(manifest['files']),'source_hashes_match':True,
          'protected_unchanged':True,'shadow_modules_absent':True,'python_ast':'passed'}
(out/'verification.json').write_text(json.dumps(verified,indent=2))
for run in ('s1','s2','s3','s4','s5','i1','i2','i3','i4'):
    for name in ('tests.txt','result.json','stderr.txt','stdout.txt'):
        source=base/run/name
        if source.exists() and source.stat().st_size:shutil.copy2(source,out/(run+'-'+name))
for name in ('install-manifest.json','install-initial-layout.json','build.log','build-result.json'):
    shutil.copy2(base/name,out/name)
for name in ('appearance-selected.png','appearance-preselected.png','appearance-task.png',
             'surface-control.png','symmetry-ready.png','symmetry-applied.png','pattern-circular.png'):
    source=base/'i3'/name
    if source.exists():shutil.copy2(source,out/name)
for source in (base/'i3').glob('m-*/dynamic-task.png'):shutil.copy2(source,out/'move-components.png')
for name in ('run.py','scene.FCMacro','build.py','build.cmd','install.py','archive.py'):
    shutil.copy2(Path(__file__).parent/name,out/name)
print(json.dumps(verified))
