import hashlib,json,shutil
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
run=root/'validation/assembly-constraints-20261125'
dest=repo/'ai-instructions/evidence/assembly-constraints-20261125';dest.mkdir(parents=True,exist_ok=True)
for mode in ('source-regressions','installed','prior-runtime','shortcut'):
    for name,ext in (('tests','txt'),('result','json')):
        shutil.copy2(run/mode/(name+'.'+ext),dest/(mode+'-'+name+'.'+ext))
for mode in ('source-reopen','reopen'):
    shutil.copy2(run/mode/'result.json',dest/(mode+'.json'))
shutil.copy2(run/'install-manifest.json',dest/'install-manifest.json')
shutil.copy2(root/'logs/assembly-constraints-build-20261125.log',dest/'native-build.txt')
for name in ('run.py','run.FCMacro','reopen.FCMacro','install.py','shortcut.py','archive.py'):
    shutil.copy2(Path(__file__).with_name(name),dest/name)
shutil.copy2(repo.parent/'assembly-constraints-preview/build.cmd',dest/'build.cmd')
images={
    'installed-collectors.png':run/'installed/test_nested_collectors_first_collapsed_and_independent/nested-collectors.png',
    'installed-tabs.png':run/'installed/test_equal_padded_tabs_left_aligned/tabs.png',
    'shortcut-collectors.png':run/'shortcut/test_nested_collectors_first_collapsed_and_independent/nested-collectors.png'}
sessions=Path('C:/Users/dgium/Documents/__Apps/_temp builds/app-render-companion/sessions')
images.update({
    'approved-collectors.png':sessions/'d3e7fa96f6e8/candidate-042bef1d.png',
    'approved-tabs.png':sessions/'7c7ae1e16791/candidate-5f23f45d.png',
    'baseline.png':sessions/'d3e7fa96f6e8/baseline-fd4713ef.png'})
for name,path in images.items():shutil.copy2(path,dest/name)
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
manifest=json.loads((run/'install-manifest.json').read_text())
assert all(digest(root/'app'/e['file'])==e['sha256']==digest(Path(e['source'])) for e in manifest)
(dest/'delivery.json').write_text(json.dumps(dict(
    installed_files=len(manifest),all_source_payload_hashes_match=True,
    native_source_sha256=digest(repo/'src/Mod/Assembly/App/AssemblyObject.cpp'),
    executable=str(root/'app/bin/FreeCAD.exe'),shortcut='C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk',
    shortcut_target=str(root/'Launch FreeCAD Plus.bat'),shortcut_working_directory=str(root)),indent=2))
print('Archived evidence; all 11 source/payload hashes match.')
