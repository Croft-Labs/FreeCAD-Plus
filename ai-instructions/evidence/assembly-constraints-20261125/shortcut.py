import os,sys,time,json,shutil,subprocess
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/assembly-constraints-20261125/shortcut';out.mkdir(parents=True,exist_ok=True)
(out/'result.json').unlink(missing_ok=True)
profile=out/'profile';profile.mkdir(exist_ok=True);(profile/'data').mkdir(exist_ok=True)
shutil.copyfile(out.parent/'installed/profile/user.cfg',profile/'user.cfg')
os.environ.pop('PLUS_TEST_SOURCE',None)
os.environ.update(FREECAD_USER_DATA=str(profile/'data'),FREECAD_USER_TEMP=str(profile),
    PLUS_TEST_DIR=str(out),PYTHONDONTWRITEBYTECODE='1',
    PLUS_TEST_NAMES=','.join('TestAssemblyConstraints.TestAssemblyConstraints.'+name for name in (
        'test_native_command_and_live_selection_create_real_joint',
        'test_nested_collectors_first_collapsed_and_independent',
        'test_editor_accept_edit_cancel_and_accept_in_place',
        'test_atomic_first_create_undo_redo_and_schema_upgrade',
        'test_equal_padded_tabs_left_aligned'))+
        ',TestAddComponent.TestAddComponent.test_ribbon_always_dropdown_both_real_add_paths_and_cancel')
macro=Path(__file__).with_name('run.FCMacro')
args=subprocess.list2cmdline(['-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(macro)])
os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk','open',args)
deadline=time.monotonic()+150
while not (out/'result.json').exists():
    if time.monotonic()>deadline:raise RuntimeError('Shortcut verification exceeded deadline')
    time.sleep(.5)
result=json.loads((out/'result.json').read_text());print(json.dumps(result,indent=2))
sys.exit(0 if result['ok'] else 1)
