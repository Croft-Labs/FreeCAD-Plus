import os,shutil,hashlib,json
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/camera-activation27';runtime=out/'runtime'
def link_missing(source,target):
    if not Path(target).exists():os.link(source,target)
    return target
shutil.copytree(root/'app',runtime,copy_function=link_missing,dirs_exist_ok=True,
    ignore=shutil.ignore_patterns('__pycache__','*.pdb','*.obj','*.pre-*','*.before-*','*.mapped-before-*'))
source=root/'build/bin/FreeCADGui.dll';target=runtime/'bin/FreeCADGui.dll'
temporary=target.with_suffix('.new');shutil.copy2(source,temporary);os.replace(temporary,target)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(source)==digest(target)
(out/'stage-manifest.json').write_text(json.dumps({'FreeCADGui.dll':digest(target)},indent=2))
print('Staged native camera library; owner installation untouched.')
