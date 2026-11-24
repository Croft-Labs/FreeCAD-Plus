import os,sys,time,json,subprocess
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/sketch-symmetry-20261123/shortcut'
out.mkdir(parents=True,exist_ok=True)
profile=out/'profile';profile.mkdir(exist_ok=True)
(profile/'data').mkdir(exist_ok=True)
# Use explicit config arguments because the existing launcher sets its normal home.
import shutil
shutil.copyfile(root/'validation/sketch-symmetry-20261123/installed/profile/user.cfg',profile/'user.cfg')
os.environ.update(FREECAD_USER_DATA=str(profile/'data'),FREECAD_USER_TEMP=str(profile),
    PLUS_TEST_DIR=str(out),PYTHONDONTWRITEBYTECODE='1',
    PLUS_TEST_NAMES='TestSketchSymmetry.TestSketchSymmetry.test_real_viewport_click_and_shift')
macro=Path(__file__).with_name('run.FCMacro')
args=subprocess.list2cmdline(['-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(macro)])
os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk','open',args)
deadline=time.monotonic()+150
while not (out/'result.json').exists():
    if time.monotonic()>deadline:raise RuntimeError('Shortcut verification exceeded deadline')
    time.sleep(.5)
print((out/'result.json').read_text())
print((out/'tests.txt').read_text())
if not json.loads((out/'result.json').read_text())['ok']:sys.exit(1)