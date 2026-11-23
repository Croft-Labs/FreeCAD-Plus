import json, os, subprocess, sys, time
from pathlib import Path
import xml.etree.ElementTree as ET

worktree, output = map(Path, sys.argv[1:3])
root = Path(__file__).parent
run = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/extrude-surface-preview-20261123') / worktree.name
run.mkdir(parents=True, exist_ok=True)
profile = run / 'profile'
profile.mkdir(exist_ok=True)
(profile/'data').mkdir(exist_ok=True)
repo = root.parent / 'FreeCAD-Plus'
config = ET.parse(repo / 'src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs = config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod = ET.SubElement(prefs, 'FCParamGroup', Name='Mod')
start = ET.SubElement(mod, 'FCParamGroup', Name='Start')
ET.SubElement(start, 'FCBool', Name='ShowOnStartup', Value='0')
ET.SubElement(start, 'FCBool', Name='FirstStart2024', Value='0')
config.write(profile / 'user.cfg', encoding='utf-8', xml_declaration=True)
env = os.environ.copy()
env.update(FREECAD_USER_HOME=str(profile), FREECAD_USER_DATA=str(profile/'data'),
           FREECAD_USER_TEMP=str(profile), PLUS_PREVIEW_WORKTREE=str(worktree),
           PLUS_PREVIEW_OUT=str(run), PLUS_PREVIEW_IMAGE=str(output), PYTHONDONTWRITEBYTECODE='1')
startup = subprocess.STARTUPINFO()
startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startup.wShowWindow = 0
exe = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/app/bin/FreeCAD.exe')
with (run/'stdout.txt').open('w') as stdout, (run/'stderr.txt').open('w') as stderr:
    proc = subprocess.Popen([str(exe), '-u', str(profile/'user.cfg'), '-s', str(profile/'system.cfg'), str(root/'scene.FCMacro')], env=env, stdout=stdout, stderr=stderr, startupinfo=startup)
    deadline = time.monotonic()+140
    while proc.poll() is None:
        if time.monotonic()>deadline:
            proc.kill(); proc.wait(); raise RuntimeError('Native preview exceeded 140 seconds')
        time.sleep(.5)
result = json.loads((run/'result.json').read_text())
print(json.dumps(result, indent=2))
if not result['ok'] or not output.exists():
    print((run/'stderr.txt').read_text()); sys.exit(1)
