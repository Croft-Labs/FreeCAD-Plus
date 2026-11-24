import os
from pathlib import Path
import subprocess
import sys
import time

root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out = root / 'validation' / 'spacing-units-20261124'
out.mkdir(parents=True, exist_ok=True)
stage = sys.argv[1] if len(sys.argv) > 1 else 'build'
targets = 'FreeCADGui Sketcher SketcherGui Sketcher_tests_run PartDesign PartDesignGui FreeCADPlusScripts'
command = out / (stage + '.cmd')
command.write_text('@echo off\ncall "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Auxiliary\\Build\\vcvars64.bat"\n'
                   'if errorlevel 1 exit /b %errorlevel%\n'
                   f'"{root}/tools/cmake-3.31.6-windows-x86_64/bin/cmake.exe" --build "{root}/build" --target {targets} --parallel 3\n'
                   'exit /b %errorlevel%\n')
env = os.environ.copy()
env.update(TEMP=str(root/'temp'), TMP=str(root/'temp'))
log = out / (stage + '.log')
startup = subprocess.STARTUPINFO()
startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startup.wShowWindow = 0
with log.open('w') as stream:
    process = subprocess.Popen(['cmd.exe', '/c', str(command)], stdout=stream, stderr=subprocess.STDOUT, env=env, startupinfo=startup)
    start = last = time.monotonic()
    size = 0
    while process.poll() is None:
        time.sleep(2)
        current = log.stat().st_size
        if current != size:
            size = current
            last = time.monotonic()
        if time.monotonic()-start > 1200 or time.monotonic()-last > 300:
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], check=False)
            raise RuntimeError('Build exceeded hard/inactivity deadline')
print(log.read_text(errors='replace')[-5000:])
raise SystemExit(process.returncode)
