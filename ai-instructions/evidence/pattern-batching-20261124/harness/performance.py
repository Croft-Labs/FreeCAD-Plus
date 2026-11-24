import os,sys,subprocess,json
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
stage=sys.argv[1];n=sys.argv[2];spacing=sys.argv[3]
out=root/'validation'/'pattern-performance-20261124'/stage
out.mkdir(parents=True,exist_ok=True)
profile=out/'profile';profile.mkdir(exist_ok=True)
(profile/'data').mkdir(exist_ok=True)
env=os.environ.copy()
env.update(FREECAD_USER_HOME=str(profile),FREECAD_USER_DATA=str(profile/'data'),FREECAD_USER_TEMP=str(profile),PLUS_PERF_DIR=str(out),PLUS_PERF_N=n,PLUS_PERF_SPACING=spacing,PYTHONDONTWRITEBYTECODE='1')
env['PLUS_PERF_KIND']=sys.argv[4] if len(sys.argv)>4 else 'circle'
if stage.startswith('source'):
    env['PLUS_TEST_SOURCE']='C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus/src/Mod/FreeCADPlus'
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr:
    proc=subprocess.Popen([str(root/'app/bin/FreeCAD.exe'),'-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(Path(__file__).with_name('performance.FCMacro'))],env=env,stdout=stdout,stderr=stderr,startupinfo=startup)
    try:proc.wait(timeout=100)
    except subprocess.TimeoutExpired:
        proc.kill();proc.wait()
        print('Stopped isolated benchmark at 100-second deadline.')
        print((out/'progress.json').read_text() if (out/'progress.json').exists() else 'No progress file')
        sys.exit(2)
print((out/'result.json').read_text())
print((out/'profile.txt').read_text() if (out/'profile.txt').exists() else '')
