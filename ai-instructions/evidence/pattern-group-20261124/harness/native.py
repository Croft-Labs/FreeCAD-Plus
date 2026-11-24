import json
import os
from pathlib import Path
import subprocess

root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out = root/'validation/pattern-group-20261124/native'
out.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env.update(FREECAD_USER_HOME=str(out), FREECAD_USER_DATA=str(out), FREECAD_USER_TEMP=str(out),
           PYTHONDONTWRITEBYTECODE='1')
env['PATH'] = ';'.join(str(p) for p in [root/'build/bin', root/'dependencies/LibPack-1.1.0-v3.1.1.3-Release/bin',
                                     *list((root/'build/Mod').iterdir())] if p.is_dir()) + ';' + env['PATH']
with (out/'tests.txt').open('w') as stream:
    result = subprocess.run([str(root/'build/bin/Sketcher_tests_run.exe')], cwd=root/'build',
                            env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=180)
print((out/'tests.txt').read_text(errors='replace')[-4500:])
(out/'result.json').write_text(json.dumps({'exit_code': result.returncode}))
raise SystemExit(result.returncode)
