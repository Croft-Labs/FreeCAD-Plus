from pathlib import Path
import hashlib, json, shutil

repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
app = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
evidence = repo/'ai-instructions/evidence/placement-workflow-20261126'
validation = app/'validation/pw26'
for source in (validation, app/'validation/placement-workflow-20261126'):
    for run in source.iterdir():
        if not run.is_dir() or run.name == 'staged': continue
        target = evidence/'logs'/run.name
        target.mkdir(parents=True, exist_ok=True)
        for name in ('result.json', 'tests.txt', 'stdout.txt', 'stderr.txt'):
            file = run/name
            if file.exists():
                text = file.read_text(encoding='utf-8', errors='replace')
                normalized = '\n'.join(line.rstrip() for line in text.splitlines()).rstrip()
                (target/name).write_text(normalized+'\n' if normalized else '', encoding='utf-8')
manifest = json.loads((validation/'install-manifest.json').read_text())
for entry in manifest:
    for file in (Path(entry['source']), app/'app'/entry['file']):
        assert hashlib.sha256(file.read_bytes()).hexdigest() == entry['sha256'], file
shutil.copy2(validation/'install-manifest.json', evidence/'install-manifest.json')
images = evidence/'installed-styles'; images.mkdir(exist_ok=True)
for image in (validation/'installed/test_all_native_styles_refresh_translucent_copy_without_source_writes').glob('*.png'):
    shutil.copy2(image, images/image.name)
for folder, name in (('placement-style-preview', 'approved-placement.png'),
                     ('active-component-add-preview', 'approved-workflow.png')):
    shutil.copy2(repo.parent/folder/'proposed.png', evidence/name)
print('Archived native logs, screenshots and five verified installed hashes')
