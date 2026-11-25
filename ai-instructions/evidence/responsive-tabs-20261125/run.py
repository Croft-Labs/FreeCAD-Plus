import json, os, subprocess, sys, time
from pathlib import Path
import xml.etree.ElementTree as ET

root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
mode = sys.argv[1]
run = root/'validation/responsive-tabs-20261125'/mode
run.mkdir(parents=True, exist_ok=True)
(run/'result.json').unlink(missing_ok=True)
profile = run/'profile'; profile.mkdir(exist_ok=True); (profile/'data').mkdir(exist_ok=True)
config = ET.parse(repo/'src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs = config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod = ET.SubElement(prefs, 'FCParamGroup', Name='Mod')
start = ET.SubElement(mod, 'FCParamGroup', Name='Start')
ET.SubElement(start, 'FCBool', Name='ShowOnStartup', Value='0')
ET.SubElement(start, 'FCBool', Name='FirstStart2024', Value='0')
config.write(profile/'user.cfg', encoding='utf-8', xml_declaration=True)
worktree = (repo/'src/Mod/FreeCADPlus/freecad_plus' if mode == 'source'
            else root/'app/Mod/FreeCADPlus/freecad_plus')
env = os.environ.copy()
env.update(FREECAD_USER_HOME=str(profile), FREECAD_USER_DATA=str(profile/'data'),
           FREECAD_USER_TEMP=str(profile), PLUS_PREVIEW_WORKTREE=str(worktree),
           PLUS_PREVIEW_OUT=str(run), PLUS_PREVIEW_IMAGE=str(run/'tabs.png'), PYTHONDONTWRITEBYTECODE='1')
args = ['-u', str(profile/'user.cfg'), '-s', str(profile/'system.cfg'), str(Path(__file__).with_name('scene.FCMacro'))]
startup = subprocess.STARTUPINFO(); startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW; startup.wShowWindow = 0
with (run/'stdout.txt').open('w') as stdout, (run/'stderr.txt').open('w') as stderr:
    proc = None
    if mode == 'shortcut':
        os.environ.update(env)
        os.startfile('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk', 'open', subprocess.list2cmdline(args))
    else:
        proc = subprocess.Popen([str(root/'app/bin/FreeCAD.exe'), *args], env=env, stdout=stdout, stderr=stderr, startupinfo=startup)
    deadline = time.monotonic()+120
    while (proc.poll() is None if proc else not (run/'result.json').exists()):
        if time.monotonic()>deadline:
            if proc: proc.kill(); proc.wait()
            raise RuntimeError('Native tab check exceeded 120 seconds')
        time.sleep(.5)
result = json.loads((run/'result.json').read_text())
print(json.dumps(result, indent=2))
sys.exit(0 if result['ok'] else 1)
