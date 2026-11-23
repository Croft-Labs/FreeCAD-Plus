import os,sys,subprocess,time,json
from pathlib import Path
import xml.etree.ElementTree as ET
root=Path(__file__).parent
runtime=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
case=sys.argv[1] if len(sys.argv)>1 else 'Edge1'
out=root/('run-'+case+('-body' if '--body' in sys.argv else '')+('-build' if '--build' in sys.argv else ''))
out.mkdir(exist_ok=True);profile=out/'profile';profile.mkdir(exist_ok=True);(profile/'data').mkdir(exist_ok=True)
config=ET.parse(root.parent/'FreeCAD-Plus/src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs=config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod=ET.SubElement(prefs,'FCParamGroup',Name='Mod');start=ET.SubElement(mod,'FCParamGroup',Name='Start')
ET.SubElement(start,'FCBool',Name='ShowOnStartup',Value='0');ET.SubElement(start,'FCBool',Name='FirstStart2024',Value='0')
config.write(profile/'user.cfg',encoding='utf-8',xml_declaration=True)
env=os.environ.copy();env.update(FREECAD_USER_HOME=str(profile),FREECAD_USER_DATA=str(profile/'data'),FREECAD_USER_TEMP=str(profile),PLUS_TEST_DIR=str(out),FILLET_CASE=case,FILLET_BODY='1' if '--body' in sys.argv else '0',PYTHONDONTWRITEBYTECODE='1')
for n in ('progress.txt','result.json'):(out/n).unlink(missing_ok=True)
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr:
    p=subprocess.Popen([str(runtime/('build/bin/FreeCAD.exe' if '--build' in sys.argv else 'app/bin/FreeCAD.exe')),'-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(root/'repro.FCMacro')],env=env,stdout=stdout,stderr=stderr,startupinfo=startup)
    print('PID',p.pid,flush=True);deadline=time.monotonic()+60
    while p.poll() is None and time.monotonic()<deadline:time.sleep(.5)
    if p.poll() is None:p.kill();p.wait();print('TIMEOUT',flush=True)
for n in ('progress.txt','result.json','stderr.txt'):
    if (out/n).exists():print(n,(out/n).read_text()[-6000:])
