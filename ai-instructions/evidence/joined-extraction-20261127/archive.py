from pathlib import Path
import hashlib,json,shutil
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
run=root/'validation/extract-join27'
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=repo/'ai-instructions/evidence/joined-extraction-20261127';out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((run/'install-manifest.json').read_text())
for entry in manifest['files']:
    assert sha(Path(entry['source']))==entry['installed']==sha(root/'app'/entry['path'])
assert all(sha(Path(path))==value for path,value in manifest['protected'].items())
(out/'verification.json').write_text(json.dumps({'installed_hashes':len(manifest['files']),
    'source_build_installed_match':True,'protected_unchanged':True},indent=2))
for name in ('install-manifest.json','build-result.json','build.log'):
    shutil.copy2(run/name,out/name)
for phase in ('s1','s2','s3','s4','i1','i2','i3'):
    for name in ('tests.txt','result.json','stdout.txt','stderr.txt'):
        source=run/phase/name
        if source.exists() and source.stat().st_size:shutil.copy2(source,out/(phase+'-'+name))
shots=run/'i2/test_task_default_error_recovery_gestures_and_no_preview_writes'
for name in ('joined.png','separate.png','disconnected.png'):shutil.copy2(shots/name,out/name)
preview=root.parent/'app-render-companion/sessions/af9bee845167'
shutil.copy2(preview/'candidate-2f0cc736.png',out/'approved-preview.png')
for name in ('run.py','scene.FCMacro','build.py','build.cmd','install.py','archive.py'):
    source=Path(__file__).parent/name
    (out/name).write_text(source.read_text().rstrip()+'\n',encoding='utf-8')
print(json.dumps({'archived':str(out),'installed_hashes':len(manifest['files']),'protected_unchanged':True}))
