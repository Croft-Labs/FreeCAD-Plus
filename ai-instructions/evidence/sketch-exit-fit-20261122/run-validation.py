import json, os, subprocess, sys, time
from pathlib import Path
import xml.etree.ElementTree as ET
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
out=root/'validation/sketch-exit-fit-20261122'
out.mkdir(parents=True,exist_ok=True)
profile=out/('profile-'+('installed' if '--installed' in sys.argv else 'build'))
profile.mkdir(exist_ok=True)
(profile/'data').mkdir(exist_ok=True)
config=ET.parse(repo/'src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs=config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod=ET.SubElement(prefs,'FCParamGroup',Name='Mod');start=ET.SubElement(mod,'FCParamGroup',Name='Start')
ET.SubElement(start,'FCBool',Name='ShowOnStartup',Value='0')
ET.SubElement(start,'FCBool',Name='FirstStart2024',Value='0')
config.write(profile/'user.cfg',encoding='utf-8',xml_declaration=True)
env=os.environ.copy();env.update(FREECAD_USER_HOME=str(profile),FREECAD_USER_DATA=str(profile/'data'),
    FREECAD_USER_TEMP=str(profile),PLUS_TEST_DIR=str(out),PYTHONDONTWRITEBYTECODE='1',
    PLUS_TEST_SCOPE='broad' if '--broad' in sys.argv else 'focused',PLUS_SOURCE_CHECK='1' if '--source' in sys.argv else '0')
macro=sys.argv[1];env['PLUS_TEST_RUN']=macro
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
exe=root/('app/bin/FreeCAD.exe' if '--installed' in sys.argv or '--source' in sys.argv else 'build/bin/FreeCAD.exe')
with (out/(macro+'-stdout.txt')).open('w') as stdout,(out/(macro+'-stderr.txt')).open('w') as stderr:
    process=subprocess.Popen([str(exe),'-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),
        str(Path(__file__).with_name(macro+'.FCMacro'))],env=env,stdout=stdout,stderr=stderr,startupinfo=startup)
    print('PID',process.pid,flush=True);deadline=time.monotonic()+420;last=time.monotonic();size=-1
    while process.poll() is None:
        progress=out/(macro+'.txt')
        current=progress.stat().st_size if progress.exists() else 0
        if current!=size:size=current;last=time.monotonic()
        if time.monotonic()>deadline or time.monotonic()-last>120:
            process.kill();process.wait();raise RuntimeError('Validation exceeded its bounded deadline/inactivity limit')
        time.sleep(.5)
result=json.loads((out/(macro+'.json')).read_text());print(json.dumps(result,indent=2))
if not result['ok']:print((out/(macro+'.txt')).read_text() if (out/(macro+'.txt')).exists() else (out/(macro+'-stderr.txt')).read_text())
sys.exit(0 if result['ok'] and process.returncode==0 else 1)
