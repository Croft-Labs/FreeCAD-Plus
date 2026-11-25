import os, sys, time, json, shutil, subprocess
from pathlib import Path
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out = root/'validation/move-20261125/shortcut-final3'
out.mkdir(parents=True, exist_ok=True)
profile = out/'profile'; profile.mkdir(exist_ok=True); (profile/'data').mkdir(exist_ok=True)
import xml.etree.ElementTree as ET
config=ET.parse(Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus/src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg'))
prefs=config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod=ET.SubElement(prefs,'FCParamGroup',Name='Mod');start=ET.SubElement(mod,'FCParamGroup',Name='Start')
ET.SubElement(start,'FCBool',Name='ShowOnStartup',Value='0')
ET.SubElement(start,'FCBool',Name='FirstStart2024',Value='0')
config.write(profile/'user.cfg',encoding='utf-8',xml_declaration=True)
os.environ.pop('PLUS_TEST_SOURCE', None)
os.environ.update(FREECAD_USER_DATA=str(profile/'data'), FREECAD_USER_TEMP=str(profile),
    PLUS_TEST_DIR=str(out), PYTHONDONTWRITEBYTECODE='1',
    PLUS_TEST_NAMES=','.join('TestMoveWorkflow.TestMoveWorkflow.'+name for name in (
        'test_actual_viewport_arrow_release_escape_and_ring',
        'test_fixed_root_toolbar_and_click_collectors',
        'test_vector_group_parent_frame_apply_undo_redo_cancel_save',
        'test_preview_toggle_method_reset_apply_then_ok_and_clear')))
macro = Path(__file__).with_name('run.FCMacro')
args = subprocess.list2cmdline(['-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(macro)])
os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk','open',args,show_cmd=0)
deadline = time.monotonic()+150
while not (out/'result.json').exists():
    if time.monotonic()>deadline: raise RuntimeError('Shortcut verification exceeded deadline')
    time.sleep(.5)
result=json.loads((out/'result.json').read_text()); print(json.dumps(result,indent=2))
sys.exit(0 if result['ok'] else 1)
