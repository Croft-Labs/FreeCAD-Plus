import os, sys, time, json, shutil, subprocess
from pathlib import Path
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out = root/'validation/instance-removal-20261125/shortcut'
out.mkdir(parents=True, exist_ok=True)
profile = out/'profile'; profile.mkdir(exist_ok=True); (profile/'data').mkdir(exist_ok=True)
shutil.copyfile(out.parent/'installed-final/profile/user.cfg', profile/'user.cfg')
os.environ.pop('PLUS_TEST_SOURCE', None)
os.environ.update(FREECAD_USER_DATA=str(profile/'data'), FREECAD_USER_TEMP=str(profile),
    PLUS_TEST_DIR=str(out), PYTHONDONTWRITEBYTECODE='1',
    PLUS_TEST_NAMES=','.join('TestInstanceRemoval.TestInstanceRemoval.'+name for name in (
        'test_native_menu_delete_cancel_and_ineligible_delete_routing',
        'test_constraints_opt_in_survivors_fixed_and_collector',
        'test_shared_parent_acknowledgement_and_entire_subassembly_preserved')))
macro = Path(__file__).with_name('run.FCMacro')
args = subprocess.list2cmdline(['-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(macro)])
(out/'result.json').unlink(missing_ok=True)
os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk','open',args,show_cmd=0)
deadline = time.monotonic()+150
while not (out/'result.json').exists():
    if time.monotonic()>deadline: raise RuntimeError('Shortcut verification exceeded deadline')
    time.sleep(.5)
result=json.loads((out/'result.json').read_text()); print(json.dumps(result,indent=2))
sys.exit(0 if result['ok'] else 1)
