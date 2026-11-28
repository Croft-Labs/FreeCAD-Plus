import gzip, shutil
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
base=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/history-operation-colors27')
out=repo/'ai-instructions/evidence/history-operations-20261127';out.mkdir(parents=True,exist_ok=True)
for run in base.iterdir():
    if not run.is_dir() or not (run/'result.json').exists():continue
    dest=out/run.name;dest.mkdir(exist_ok=True)
    for name in ('result.json','tests.txt','stderr.txt'):
        if not (run/name).exists():continue
        data=(run/name).read_bytes()
        if name=='stderr.txt' and len(data)>16384:
            (dest/(name+'.gz')).write_bytes(gzip.compress(data,mtime=0))
            assert gzip.decompress((dest/(name+'.gz')).read_bytes())==data
            (dest/name).unlink(missing_ok=True)
        else:shutil.copy2(run/name,dest/name)
    if run.name.startswith('i'):
        shutil.copy2(run/'installed-history-operations.png',out/'installed-history-operations.png')
for name in ('build-result.json','build.log','install-manifest.json'):
    if (base/name).exists():shutil.copy2(base/name,out/name)
log=out/'build.log'
if log.exists():log.write_text('\n'.join(line.rstrip() for line in log.read_text().splitlines())+'\n')
for name in ('run.py','scene.FCMacro','build.py','build.cmd','install.py','archive.py'):
    shutil.copy2(Path(__file__).parent/name,out/name)
preview=Path('C:/Users/dgium/Documents/__Apps/_temp builds/app-render-companion/sessions/3bbe1c582151')
shutil.copy2(preview/'candidate-936a65e2.png',out/'approved-preview.png')
shutil.copy2(preview/'baseline-41b565e4.png',out/'baseline-preview.png')
print(out)
