"""Archive compact, reproducible delivery evidence without owner profiles."""
import json, shutil
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
base=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/approved-ui27')
out=repo/'ai-instructions/evidence/assembly-selection-20261127'
out.mkdir(parents=True,exist_ok=True)
for run in base.iterdir():
    if not run.is_dir() or not (run/'result.json').exists():continue
    dest=out/run.name;dest.mkdir(exist_ok=True)
    for name in ('result.json','tests.txt','stderr.txt'):
        if (run/name).exists():shutil.copy2(run/name,dest/name)
    if run.name.startswith('i'):
        for image in run.glob('*.png'):shutil.copy2(image,out/image.name)
        for name in ('expanded-eyes.png','condensed-eyes.png','viewport-clone.png'):
            for image in run.rglob(name):shutil.copy2(image,out/name)
for name in ('build-result.json','build.log','install-manifest.json'):
    if (base/name).exists():shutil.copy2(base/name,out/name)
log=out/'build.log'
if log.exists():log.write_text('\n'.join(line.rstrip() for line in log.read_text().splitlines())+'\n')
for name in ('run.py','scene.FCMacro','build.py','build.cmd','install.py','archive.py'):
    shutil.copy2(Path(__file__).parent/name,out/name)
previews=Path('C:/Users/dgium/Documents/__Apps/_temp builds/app-render-companion/sessions')
for session,file,name in (
    ('a95f3284527c','candidate-86d56ad4.png','approved-assembly-eyes.png'),
    ('84bd54687009','candidate-bf8e7a71.png','approved-clone.png'),
    ('f07de651e58c','candidate-e7fec47a.png','approved-appearance-edges.png')):
    shutil.copy2(previews/session/file,out/name)
print(out)
