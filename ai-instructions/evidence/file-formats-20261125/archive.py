import hashlib, json, shutil
from pathlib import Path
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/file-formats-20261125')
repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
dest = repo/'ai-instructions/evidence/file-formats-20261125'
dest.mkdir(parents=True, exist_ok=True)
for mode in ('source-accepted','source-context','installed','installed-final','reopen','shortcut'):
    for name in ('result.json','tests.txt'):
        path = root/mode/name
        if path.exists(): shutil.copy2(path, dest/(mode+'-'+name))
cases = {
    'installed-save-as.png': ('test_gui_save_as_plus_filter_and_filename', 'dialog-1.png'),
    'installed-classic-save.png': ('test_gui_save_copy_classic_filter', 'dialog-1.png'),
    'installed-open.png': ('test_gui_open_filters_keep_geometry_importers', 'dialog-1.png'),
    'installed-convert-open.png': ('test_native_open_command_converts_and_opens_plus', 'dialog-2.png'),
    'installed-convert-import.png': ('test_panel_import_converts_without_placing_children', 'dialog-1.png'),
    'installed-convert-add.png': ('test_add_existing_converts_without_changing_edit_context', 'dialog-1.png'),
}
for name,(case,image) in cases.items():
    directory = 'fw-'+hashlib.sha256(case.encode()).hexdigest()[:10]
    shutil.copy2(root/'installed-final'/directory/image, dest/name)
preview = root.parent/'file-formats-preview-20261125'
for name in ('open','save-as','classic-save','convert-open','convert-import','repair-extension','component-export'):
    shutil.copy2(preview/'candidate'/(name+'.png'), dest/('approved-'+name+'.png'))
for name in ('run.py','run.FCMacro','reopen.FCMacro','build.py','install.py','shortcut.py','archive.py'):
    shutil.copy2(Path(__file__).with_name(name), dest/name)
for name in ('build-verified.log','install-manifest.json'):
    shutil.copy2(root/name, dest/name)
manifest = json.loads((root/'install-manifest.json').read_text())
for entry in manifest:
    target = root.parent.parent/'app'/entry['file']
    assert hashlib.sha256(target.read_bytes()).hexdigest() == entry['sha256']
    assert hashlib.sha256(Path(entry['source']).read_bytes()).hexdigest() == entry['sha256']
print(json.dumps({'evidence':str(dest),'verified_installed_files':len(manifest)}))
