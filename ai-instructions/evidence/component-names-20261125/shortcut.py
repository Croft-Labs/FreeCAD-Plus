import os, sys, time, json, shutil, subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out = root/'validation/naming-20261125/shortcut'
out.mkdir(parents=True, exist_ok=True)
profile = out/'profile'; profile.mkdir(exist_ok=True); (profile/'data').mkdir(exist_ok=True)
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
config=ET.parse(repo/'src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs=config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod=ET.SubElement(prefs,'FCParamGroup',Name='Mod');start=ET.SubElement(mod,'FCParamGroup',Name='Start')
ET.SubElement(start,'FCBool',Name='ShowOnStartup',Value='0')
ET.SubElement(start,'FCBool',Name='FirstStart2024',Value='0')
config.write(profile/'user.cfg',encoding='utf-8',xml_declaration=True)
os.environ.pop('PLUS_TEST_SOURCE', None)
os.environ.update(FREECAD_USER_DATA=str(profile/'data'), FREECAD_USER_TEMP=str(profile),
    PLUS_TEST_DIR=str(out), PYTHONDONTWRITEBYTECODE='1',
    PLUS_TEST_NAMES=','.join('TestComponentNames.TestComponentNames.'+name for name in (
        'test_import_collision_reports_both_files_before_mutation',
        'test_native_label_edit_is_rejected_and_valid_rename_shared',
        'test_generated_new_name_reserves_imports',
        'test_legacy_conflict_is_repairable_but_native_saves_refuse_it'))+
        ',TestComponentRename.TestComponentRename.test_external_model_rename_belongs_to_source_file')
macro = Path(__file__).with_name('run.FCMacro')
args = subprocess.list2cmdline(['-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(macro)])
os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk','open',args,show_cmd=0)
deadline = time.monotonic()+150
while not (out/'result.json').exists():
    if time.monotonic()>deadline: raise RuntimeError('Shortcut verification exceeded deadline')
    time.sleep(.5)
result=json.loads((out/'result.json').read_text()); print(json.dumps(result,indent=2))
sys.exit(0 if result['ok'] else 1)
