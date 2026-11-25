from pathlib import Path
import hashlib, json, shutil
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
source=root/'validation/instance-quantity-20261125'
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
dest=repo/'ai-instructions/evidence/instance-quantity-20261125'
for folder in source.iterdir():
    if not folder.is_dir() or folder.name=='staged': continue
    target=dest/'logs'/folder.name; target.mkdir(parents=True,exist_ok=True)
    for name in ('result.json','tests.txt','stderr.txt','stdout.txt'):
        if (folder/name).exists(): shutil.copy2(folder/name,target/name)
shutil.copy2(source/'install-manifest.json',dest/'install-manifest.json')
for file in Path(__file__).parent.iterdir():
    if file.is_file(): shutil.copy2(file,dest/'helpers'/file.name)
for item in json.loads((source/'install-manifest.json').read_text()):
    assert hashlib.sha256((root/'app'/item['file']).read_bytes()).hexdigest()==item['sha256']
    assert hashlib.sha256(Path(item['source']).read_bytes()).hexdigest()==item['sha256']
print('Final evidence and hashes verified')
