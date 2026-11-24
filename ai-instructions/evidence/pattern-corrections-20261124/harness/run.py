import os,sys,subprocess,json,time
from pathlib import Path
import xml.etree.ElementTree as ET
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
stage=sys.argv[1]
out=root/'validation'/'pattern-corrections-20261124'/stage
out.mkdir(parents=True,exist_ok=True)
(out/'result.json').unlink(missing_ok=True)
profile=out/'profile';profile.mkdir(exist_ok=True)
(profile/'data').mkdir(exist_ok=True)
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
config=ET.parse(repo/'src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg')
prefs=config.getroot().find(".//FCParamGroup[@Name='Preferences']")
mod=ET.SubElement(prefs,'FCParamGroup',Name='Mod')
start=ET.SubElement(mod,'FCParamGroup',Name='Start')
ET.SubElement(start,'FCBool',Name='ShowOnStartup',Value='0')
ET.SubElement(start,'FCBool',Name='FirstStart2024',Value='0')
config.write(profile/'user.cfg',encoding='utf-8',xml_declaration=True)
env=os.environ.copy()
env.update(FREECAD_USER_HOME=str(profile),FREECAD_USER_DATA=str(profile/'data'),FREECAD_USER_TEMP=str(profile),
           PLUS_TEST_DIR=str(out),PYTHONDONTWRITEBYTECODE='1',
           PLUS_TEST_NAMES=sys.argv[2] if len(sys.argv)>2 else 'TestSketchPattern')
if stage.startswith('build') or stage.startswith('source'):env['PLUS_TEST_SOURCE']=str(repo/'src/Mod/FreeCADPlus')
exe=root/('build' if stage.startswith('build') else 'app')/'bin/FreeCAD.exe'
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr:
    proc=subprocess.Popen([str(exe),'-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),
                           str(Path(__file__).with_name('run.FCMacro'))],env=env,stdout=stdout,stderr=stderr,startupinfo=startup)
    try:proc.wait(timeout=300)
    except subprocess.TimeoutExpired:
        proc.kill();proc.wait();raise
print((out/'result.json').read_text())
print((out/'tests.txt').read_text())
if not json.loads((out/'result.json').read_text())['ok']:sys.exit(1)
