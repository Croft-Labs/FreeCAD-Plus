import json, os, subprocess, sys, time, shutil
from pathlib import Path
import xml.etree.ElementTree as ET
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
mode=sys.argv[1] if len(sys.argv)>1 else 'source'
out=root/'validation/clone-extract-20261125'/mode
out.mkdir(parents=True,exist_ok=True)
profile=out/'profile';profile.mkdir(exist_ok=True);(profile/'data').mkdir(exist_ok=True)
config=ET.parse(repo/'src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs=config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod=ET.SubElement(prefs,'FCParamGroup',Name='Mod');start=ET.SubElement(mod,'FCParamGroup',Name='Start')
ET.SubElement(start,'FCBool',Name='ShowOnStartup',Value='0')
ET.SubElement(start,'FCBool',Name='FirstStart2024',Value='0')
config.write(profile/'user.cfg',encoding='utf-8',xml_declaration=True)
if mode.endswith('reopen') and (out.parent/'installed/profile/user.cfg').exists():
    shutil.copyfile(out.parent/'installed/profile/user.cfg',profile/'user.cfg')
env=os.environ.copy();env.update(FREECAD_USER_HOME=str(profile),FREECAD_USER_DATA=str(profile/'data'),
    FREECAD_USER_TEMP=str(profile),PLUS_TEST_DIR=str(out),PYTHONDONTWRITEBYTECODE='1')
if mode.startswith('source'):env['PLUS_TEST_SOURCE']=str(repo/'src/Mod/FreeCADPlus')
else:env.pop('PLUS_TEST_SOURCE',None)
macro='reopen' if mode.endswith('reopen') else 'run'
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr:
    proc=subprocess.Popen([str(root/('build/bin/FreeCAD.exe' if mode.startswith('source') else 'app/bin/FreeCAD.exe')),'-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(Path(__file__).with_name(macro+'.FCMacro'))],env=env,stdout=stdout,stderr=stderr,startupinfo=startup)
    print('PID',proc.pid,flush=True);deadline=time.monotonic()+420;last=time.monotonic();size=-1
    while proc.poll() is None:
        progress=out/'tests.txt';current=progress.stat().st_size if progress.exists() else 0
        if current!=size:size=current;last=time.monotonic()
        if time.monotonic()>deadline or time.monotonic()-last>120:
            proc.kill();proc.wait();raise RuntimeError('Validation deadline/inactivity limit exceeded')
        time.sleep(.5)
result=json.loads((out/'result.json').read_text());print(json.dumps(result,indent=2))
if not result['ok']:print((out/'tests.txt').read_text() if (out/'tests.txt').exists() else (out/'stderr.txt').read_text())
sys.exit(0 if result['ok'] and proc.returncode==0 else 1)
