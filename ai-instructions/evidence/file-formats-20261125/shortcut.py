import os, sys, time, json, shutil, subprocess
from pathlib import Path
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out = root/'validation/file-formats-20261125/shortcut'
out.mkdir(parents=True, exist_ok=True)
profile = out/'profile'; profile.mkdir(exist_ok=True); (profile/'data').mkdir(exist_ok=True)
shutil.copyfile(out.parent/'installed/profile/user.cfg', profile/'user.cfg')
os.environ.pop('PLUS_TEST_SOURCE', None)
os.environ.update(FREECAD_USER_DATA=str(profile/'data'), FREECAD_USER_TEMP=str(profile),
    PLUS_TEST_DIR=str(out), PYTHONDONTWRITEBYTECODE='1',
    PLUS_TEST_NAMES=','.join('TestFileWorkflows.TestFileWorkflows.'+name for name in (
        'test_native_open_command_converts_and_opens_plus',
        'test_gui_save_as_plus_filter_and_filename',
        'test_gui_save_all_uses_document_specific_extensions',
        'test_save_on_close_uses_cadprt')))
macro = Path(__file__).with_name('run.FCMacro')
args = subprocess.list2cmdline(['-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(macro)])
os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk','open',args,show_cmd=0)
deadline = time.monotonic()+150
while not (out/'result.json').exists():
    if time.monotonic()>deadline: raise RuntimeError('Shortcut verification exceeded deadline')
    time.sleep(.5)
result=json.loads((out/'result.json').read_text()); print(json.dumps(result,indent=2))
sys.exit(0 if result['ok'] else 1)
