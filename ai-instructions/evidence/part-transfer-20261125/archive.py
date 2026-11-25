import hashlib, json, shutil
from pathlib import Path
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/part-transfer-20261125')
repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
dest = repo/'ai-instructions/evidence/part-transfer-20261125'
dest.mkdir(parents=True, exist_ok=True)
for mode in ('source-final','source-import-final','source-reopen','installed','installed-screens','reopen','shortcut'):
    for name in ('result.json','tests.txt'):
        source = root/mode/name
        if source.exists(): shutil.copy2(source, dest/(mode+'-'+name))
for name, relative in {
    'installed-add-existing.png':'test_picker_open_and_batch_accept_real_native_widgets/add-existing.png',
    'installed-export-parts.png':'test_export_dialog_cancel_and_accept/export-parts.png',
    'installed-parts-menu.png':'test_parts_context_menu_exports_multiple_selected_parts/parts-menu.png',
}.items(): shutil.copy2(root/'installed'/relative, dest/name)
shutil.copy2(root/'installed-screens/test_picker_open_and_batch_accept_real_native_widgets/add-existing.png',
             dest/'installed-add-existing.png')
preview = root.parent/'part-transfer-preview-20261125'
for name in ('add-existing','export-parts','parts-menu'):
    shutil.copy2(preview/'candidate'/(name+'.png'),dest/('approved-'+name+'.png'))
shutil.copy2(preview/'baseline/add-existing.png', dest/'baseline-add-existing.png')
shutil.copy2(preview/'candidate/result.json', dest/'preview-result.json')
for name in ('run.py','run.FCMacro','reopen.FCMacro','install.py','shortcut.py','archive.py'):
    shutil.copy2(Path(__file__).with_name(name), dest/name)
shutil.copy2(root/'install-manifest.json', dest/'install-manifest.json')
manifest = json.loads((root/'install-manifest.json').read_text())
for entry in manifest:
    target = root.parent.parent/'app'/entry['file']
    assert hashlib.sha256(target.read_bytes()).hexdigest() == entry['sha256']
print(json.dumps({'archived_files':len(list(dest.iterdir())), 'installed_hashes_verified':len(manifest), 'evidence':str(dest)}))
