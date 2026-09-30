#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later
"""Compile the isolated-settings launcher and installer from a staged payload."""
import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("payload", type=Path)
parser.add_argument("compiler", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
scripts = Path(__file__).resolve().parent
subprocess.run([str(args.compiler), "/V2", f"/DOUTPUT={args.payload / 'FreeCADPlus.exe'}",
                str(scripts / "FreeCADPlus-launcher.nsi")], check=True, timeout=120)

def escaped(path):
    return str(path.relative_to(args.payload)).replace("$", "$$")

files = sorted(p for p in args.payload.rglob("*") if p.is_file())
directories = sorted((p for p in args.payload.rglob("*") if p.is_dir()),
                     key=lambda p: len(p.parts), reverse=True)
lines = [f'Delete "$INSTDIR\\{escaped(p)}"' for p in files]
lines += [f'RMDir "$INSTDIR\\{escaped(p)}"' for p in directories]
(args.payload / "uninstall-files.nsh").write_text("\n".join(lines), encoding="utf-8-sig")
subprocess.run([str(args.compiler), "/V2", f"/DPAYLOAD={args.payload}",
                f"/DOUTPUT={args.output}", str(scripts / "FreeCADPlus-installer.nsi")],
               check=True, timeout=1800)
