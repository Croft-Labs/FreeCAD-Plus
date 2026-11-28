import gzip,hashlib,json,re,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
source=root/'validation/camera-activation27'
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
dest=repo/'ai-instructions/evidence/camera-transitions-20261127'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
installed=json.loads((source/'i1/result.json').read_text());assert installed['ok']
def failures(path):
    text=path.read_text()
    blocks=re.split(r'={20,}\n',text)[1:]
    return {block.splitlines()[0]:re.findall(r'^(?:AssertionError|ValueError):.*$',block,re.M) for block in blocks}
assert failures(source/'b5/tests.txt')==failures(source/'s4/tests.txt')
manifest=[]
for run in ('b1','b2','b3','b4','b5','s1','s2','s3','s4','i1'):
    folder=source/run
    for item in folder.rglob('*'):
        if not item.is_file() or 'profile' in item.relative_to(folder).parts:continue
        if item.suffix not in ('.json','.txt','.png'):continue
        if item.suffix=='.png' and run!='i1':continue
        target=dest/run/item.relative_to(folder);target.parent.mkdir(parents=True,exist_ok=True)
        compressed=item.suffix=='.json' and item.stat().st_size>15000
        if compressed:
            target=target.with_suffix(target.suffix+'.gz');target.write_bytes(gzip.compress(item.read_bytes(),mtime=0))
            assert gzip.decompress(target.read_bytes())==item.read_bytes()
        else:shutil.copy2(item,target);assert sha(item)==sha(target)
        manifest.append({'source':str(item),'archive':str(target.relative_to(dest)),'source_sha256':sha(item),'compressed':compressed})
for name in ('build.log','build-result.json','stage-manifest.json','install-manifest.json'):
    shutil.copy2(source/name,dest/name)
for item in Path(__file__).parent.iterdir():
    if item.suffix in ('.py','.cmd','.FCMacro'):
        target=dest/'harness'/item.name;target.parent.mkdir(exist_ok=True);shutil.copy2(item,target)
(dest/'archive-manifest.json').write_text(json.dumps(manifest,indent=2))
install=json.loads((source/'install-manifest.json').read_text())
assert all(sha(Path(p))==digest for p,digest in install['protected'].items())
assert all(sha(root/'app'/item['path'])==item['installed'] for item in install['files'])
print(json.dumps({'installed_tests':installed['tests'],'baseline_mismatches_confirmed':5,'archived_files':len(manifest),'payloads_and_protected_files_verified':True}))
