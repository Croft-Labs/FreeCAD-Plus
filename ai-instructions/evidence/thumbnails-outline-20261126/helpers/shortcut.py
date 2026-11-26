import json,os,shutil,subprocess,time
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/thumbnails-outline-20261126/shortcut'
out.mkdir(parents=True,exist_ok=True)
profile=out/'profile';profile.mkdir(exist_ok=True);(profile/'data').mkdir(exist_ok=True)
shutil.copyfile(out.parent/'installed/profile/user.cfg',profile/'user.cfg')
os.environ.update(FREECAD_USER_DATA=str(profile/'data'),FREECAD_USER_TEMP=str(profile),
                  PLUS_TEST_DIR=str(out),PYTHONDONTWRITEBYTECODE='1',
                  PLUS_TEST_NAMES='TestStartThumbnails.TestStartThumbnails,TestPlusIcon.TestPlusIcon,TestOwnerPreviews.TestOwnerPreviews')
args=subprocess.list2cmdline(['-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),
                             str(Path(__file__).with_name('run.FCMacro'))])
os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk','open',args,show_cmd=0)
deadline=time.monotonic()+180
while not (out/'result.json').exists():
    if time.monotonic()>deadline:raise RuntimeError('Shortcut test timeout')
    time.sleep(.5)
result=json.loads((out/'result.json').read_text());print(json.dumps(result,indent=2))
if not result['ok']:print((out/'tests.txt').read_text())
raise SystemExit(0 if result['ok'] else 1)
