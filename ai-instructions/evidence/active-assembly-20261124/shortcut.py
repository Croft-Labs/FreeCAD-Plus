import os,sys,time,json,shutil
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/active-assembly-20261124/shortcut';out.mkdir(parents=True,exist_ok=True)
(out/'result.json').unlink(missing_ok=True)
profile=out/'profile';profile.mkdir(exist_ok=True);(profile/'data').mkdir(exist_ok=True)
shutil.copyfile(out.parent/'installed/profile/user.cfg',profile/'user.cfg')
os.environ.pop('PLUS_TEST_SOURCE',None);os.environ.pop('PLUS_TEST_CASE_SOURCE',None)
os.environ.update(FREECAD_USER_DATA=str(profile/'data'),FREECAD_USER_TEMP=str(profile),
    PLUS_TEST_DIR=str(out),PYTHONDONTWRITEBYTECODE='1',
    PLUS_TEST_NAMES='TestActiveAssembly.TestActiveAssembly,TestComponentRename.TestComponentRename.test_history_heading_context_menu_rename_undo_and_save,TestComponentPanel.TestNativeComponentCreation')
macro=Path(__file__).with_name('run.FCMacro')
import subprocess
args=subprocess.list2cmdline(['-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(macro)])
os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk','open',args)
deadline=time.monotonic()+150
while not (out/'result.json').exists():
    if time.monotonic()>deadline:raise RuntimeError('Shortcut verification exceeded deadline')
    time.sleep(.5)
print((out/'result.json').read_text())
if not json.loads((out/'result.json').read_text())['ok']:
    print((out/'tests.txt').read_text());sys.exit(1)
