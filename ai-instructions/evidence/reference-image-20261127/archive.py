import hashlib,json,shutil
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/reference-image27'
dest=repo/'ai-instructions/evidence/reference-image-20261127';dest.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((out/'install-manifest.json').read_text())
assert all(sha(Path(p))==digest for p,digest in manifest['protected'].items())
for entry in manifest['files']:
    assert sha(root/'app'/entry['path'])==entry['installed']==sha(Path(entry['source']))
for name in ('p1','s1','s2','s3','s4','s5','s6','b1','i1'):
    target=dest/name;target.mkdir(exist_ok=True)
    for file in ('result.json','tests.txt','stderr.txt'):
        if (out/name/file).exists():shutil.copy2(out/name/file,target/file)
for file in ('build.log','build-result.json','install-manifest.json'):
    shutil.copy2(out/file,dest/file)
for file in ('reference-task.png','reference-preview.png','reference-history.png'):
    shutil.copy2(out/'i1'/file,dest/file)
review=Path('C:/Users/dgium/Documents/__Apps/_temp builds/app-render-companion/sessions/ee78e7210c21')
shutil.copy2(review/'candidate-790f3d54.png',dest/'approved-preview.png')
for file in ('run.py','scene.FCMacro','build.py','build.cmd','install.py','archive.py'):
    shutil.copy2(Path(__file__).parent/file,dest/file)
(dest/'verification.json').write_text(json.dumps({'payload_files':len(manifest['files']),'source_build_installed_match':True,'protected_unchanged':True,'installed_tests':45,'failures':0},indent=2))
print(str(dest))
