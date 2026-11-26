import os, subprocess, time
from pathlib import Path

root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out = root / 'validation/thumbnails-outline-20261126'
out.mkdir(parents=True, exist_ok=True)
command = out / 'build.cmd'
command.write_text('@echo off\ncall "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Auxiliary\\Build\\vcvars64.bat"\n'
                   'if errorlevel 1 exit /b %errorlevel%\n'
                   f'"{root}/tools/cmake-3.31.6-windows-x86_64/bin/cmake.exe" --build "{root}/build" --target Start StartGui FreeCADMain FreeCADMainCmd FreeCADGuiPy --parallel 4\n'
                   'exit /b %errorlevel%\n')
env = dict(os.environ, TEMP=str(root/'temp'), TMP=str(root/'temp'))
log = out/'build.log'
startup = subprocess.STARTUPINFO()
startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startup.wShowWindow = 0
with log.open('w') as stream:
    process = subprocess.Popen(['cmd.exe','/c',str(command)], stdout=stream, stderr=subprocess.STDOUT, env=env, startupinfo=startup)
    print('Build PID', process.pid, flush=True)
    start = last = time.monotonic(); size = 0
    while process.poll() is None:
        time.sleep(2)
        current = log.stat().st_size
        if current != size:
            size = current; last = time.monotonic()
        if time.monotonic()-start > 1200 or time.monotonic()-last > 300:
            subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'], check=False)
            raise RuntimeError('Build exceeded hard/inactivity deadline')
print(log.read_text(errors='replace')[-5000:])
raise SystemExit(process.returncode)
