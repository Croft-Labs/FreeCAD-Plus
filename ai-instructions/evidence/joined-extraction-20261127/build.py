import subprocess,time,json
from pathlib import Path
here=Path(__file__).parent
out=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/extract-join27');out.mkdir(parents=True,exist_ok=True)
with (out/'build.log').open('w') as log:
    proc=subprocess.Popen(['cmd.exe','/d','/c',str(here/'build.cmd')],stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    start=time.monotonic();last=start;length=0
    while proc.poll() is None:
        time.sleep(2)
        current=(out/'build.log').stat().st_size
        if current!=length:last=time.monotonic();length=current
        if time.monotonic()-start>1800 or time.monotonic()-last>300:
            subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True)
            raise RuntimeError('Build deadline/inactivity timeout')
    (out/'build-result.json').write_text(json.dumps({'exit_code':proc.returncode,'seconds':time.monotonic()-start}))
    print((out/'build.log').read_text(errors='replace')[-2000:])
    raise SystemExit(proc.returncode)
