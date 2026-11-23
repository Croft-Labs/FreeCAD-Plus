import subprocess,time
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/thicken-20261123';out.mkdir(parents=True,exist_ok=True)
cmd='call "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Auxiliary\\Build\\vcvars64.bat" && "'+str(root/'tools/cmake-3.31.6-windows-x86_64/bin/cmake.exe')+'" --build "'+str(root/'build')+'" --target FreeCADPlusScripts PartDesignGui --parallel 6'
log=out/'build.txt'
with log.open('w') as stream:
    p=subprocess.Popen('cmd.exe /d /c C:/Users/dgium/Documents/__Apps/FreeCAD/thicken-validation/build-target.cmd',stdout=stream,stderr=subprocess.STDOUT)
    deadline=time.monotonic()+900;last=time.monotonic();size=-1
    while p.poll() is None:
        current=log.stat().st_size
        if current!=size:size=current;last=time.monotonic()
        if time.monotonic()>deadline or time.monotonic()-last>180:
            p.kill();raise RuntimeError('Build deadline/inactivity limit reached')
        time.sleep(1)
print(log.read_text()[-6500:]);raise SystemExit(p.returncode)
