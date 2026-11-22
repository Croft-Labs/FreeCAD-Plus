import json, os, subprocess, sys
from pathlib import Path
import xml.etree.ElementTree as ET
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out = root / 'validation/coordinate-history-20261122/final'
profile = out / 'profile'
profile.mkdir(parents=True,exist_ok=True)
config = ET.parse(repo / 'src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs = config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod = ET.SubElement(prefs,'FCParamGroup',Name='Mod')
start = ET.SubElement(mod,'FCParamGroup',Name='Start')
ET.SubElement(start,'FCBool',Name='ShowOnStartup',Value='0')
ET.SubElement(start,'FCBool',Name='FirstStart2024',Value='0')
if '--reuse' not in sys.argv: config.write(profile/'user.cfg',encoding='utf-8',xml_declaration=True)
env = os.environ.copy()
env.update(FREECAD_USER_HOME=str(profile), FREECAD_USER_DATA=str(profile/'data'),
    FREECAD_USER_TEMP=str(profile), PLUS_TEST_DIR=str(out), PYTHONDONTWRITEBYTECODE='1')
startup = subprocess.STARTUPINFO()
startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startup.wShowWindow = 0
macro = sys.argv[1]
with (out/(macro+'-stdout.txt')).open('w') as stdout, (out/(macro+'-stderr.txt')).open('w') as stderr:
    process = subprocess.Popen([str(root/('build/bin/FreeCAD.exe' if '--build' in sys.argv else 'app/bin/FreeCAD.exe')),'-u',str(profile/'user.cfg'),
        '-s',str(profile/'system.cfg'),str(Path(__file__).with_name(macro+'.FCMacro'))],
        env=env, stdout=stdout, stderr=stderr, startupinfo=startup)
    print('PID',process.pid,flush=True)
    try: process.wait(timeout=360)
    except subprocess.TimeoutExpired:
        process.kill();process.wait();raise
print('exit',process.returncode)
print((out/(macro+'-stderr.txt')).read_text())
if macro == 'probe_feature': print((out/'probe.json').read_text())
else:
    result = json.loads((out/(macro+'.json')).read_text())
    print(json.dumps(result,indent=2))
    log = out/(macro+'.txt')
    if log.exists(): print(log.read_text())
    if not result['ok']: sys.exit(1)
sys.exit(process.returncode)
