import ctypes,json,os,subprocess,sys,time
from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
stage=sys.argv[1];kind=sys.argv[2] if len(sys.argv)>2 else 'line'
out=root/'validation/pattern-memory-20261124'/stage;out.mkdir(parents=True,exist_ok=True)
class Memory(ctypes.Structure):
    _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(x,ctypes.c_ulonglong) for x in ('totalPhys','availPhys','totalPage','availPage','totalVirtual','availVirtual','availExtended')]
class Counters(ctypes.Structure):
    _fields_=[('cb',ctypes.c_ulong),('faults',ctypes.c_ulong)]+[(x,ctypes.c_size_t) for x in ('peakWS','ws','peakPaged','paged','peakNonpaged','nonpaged','pagefile','peakPagefile','private')]
memory=Memory();memory.length=ctypes.sizeof(memory);ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
limit=min(6*1024**3,int(memory.availPage/3));peak=0
(out/'host-memory.json').write_text(json.dumps(dict(physical=memory.totalPhys,available=memory.availPhys,availableCommit=memory.availPage,testMemoryLimit=limit)))
profile=out/'profile';profile.mkdir(exist_ok=True)
env=os.environ.copy();env.update(FREECAD_USER_HOME=str(profile),FREECAD_USER_DATA=str(profile),FREECAD_USER_TEMP=str(profile),PLUS_TEST_DIR=str(out),PLUS_GEOMETRY=kind,PLUS_COUNT=sys.argv[3] if len(sys.argv)>3 else '20',PYTHONDONTWRITEBYTECODE='1')
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
for name in ('result.json','phases.jsonl'):(out/name).unlink(missing_ok=True)
with (out/'console.txt').open('w') as stream:
    executable=root/('build' if stage.startswith('build') else 'app')/'bin/FreeCAD.exe'
    process=subprocess.Popen([str(executable),'-u',str(profile/'user.cfg'),'-s',str(profile/'system.cfg'),str(Path(__file__).with_name('probe.FCMacro'))],env=env,stdout=stream,stderr=subprocess.STDOUT,startupinfo=startup)
    start=time.monotonic();reason=None
    while process.poll() is None:
        counters=Counters();counters.cb=ctypes.sizeof(counters)
        ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(int(process._handle)),ctypes.byref(counters),ctypes.sizeof(counters))
        peak=max(peak,counters.private)
        if peak>limit or time.monotonic()-start>150:
            reason='memory guard' if peak>limit else '150 second deadline';process.kill();process.wait();break
        time.sleep(.2)
(out/'process.json').write_text(json.dumps(dict(peakPrivateBytes=peak,exit_code=process.returncode,stopped=reason)))
print((out/'process.json').read_text())
if (out/'result.json').exists():print((out/'result.json').read_text())
print((out/'phases.jsonl').read_text()[-3500:] if (out/'phases.jsonl').exists() else 'No phases')
