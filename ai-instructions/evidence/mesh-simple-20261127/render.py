import json,os,subprocess,sys,time
from pathlib import Path
import xml.etree.ElementTree as ET
worktree,output=map(Path,sys.argv[1:3]);here=Path(__file__).parent
app=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
run=app/'validation/mesh-simple27'/worktree.name;run.mkdir(parents=True,exist_ok=True)
profile=run/'profile';profile.mkdir(exist_ok=True);(profile/'data').mkdir(exist_ok=True)
config=ET.parse(here.parent/'FreeCAD-Plus/src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs=config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod=ET.SubElement(prefs,'FCParamGroup',Name='Mod');start=ET.SubElement(mod,'FCParamGroup',Name='Start')
ET.SubElement(start,'FCBool',Name='ShowOnStartup',Value='0');ET.SubElement(start,'FCBool',Name='FirstStart2024',Value='0')
config.write(profile/'user.cfg',encoding='utf-8',xml_declaration=True)
env=dict(os.environ,FREECAD_USER_HOME=str(profile),FREECAD_USER_DATA=str(profile/'data'),FREECAD_USER_TEMP=str(profile),
         PLUS_PREVIEW_OUT=str(run),PLUS_PREVIEW_WORKTREE=str(worktree),PLUS_PREVIEW_IMAGE=str(output),PYTHONDONTWRITEBYTECODE='1')
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
with (run/'stdout.txt').open('w') as stdout,(run/'stderr.txt').open('w') as stderr:
    proc=subprocess.Popen([str(app/'app/bin/FreeCAD.exe'),'-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(here/'scene.FCMacro')],
                          env=env,stdout=stdout,stderr=stderr,startupinfo=startup)
    deadline=time.monotonic()+120
    while proc.poll() is None:
        if time.monotonic()>deadline:proc.kill();proc.wait();raise RuntimeError('Mesh from Shape preview timeout')
        time.sleep(.5)
result=json.loads((run/'result.json').read_text());print(json.dumps(result,indent=2))
if not result['ok'] or (worktree.name!='diagnose' and not output.exists()):raise RuntimeError(result)
