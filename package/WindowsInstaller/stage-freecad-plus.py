#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later
"""Stage an existing Release build without running absolute CMake install rules."""
import argparse
import json
import shutil
import subprocess
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("build", type=Path)
parser.add_argument("payload", type=Path)
parser.add_argument("--libpack", type=Path, required=True)
args = parser.parse_args()
source = Path(__file__).resolve().parents[2]
if args.payload.exists() and any(args.payload.iterdir()):
    raise SystemExit("Payload must be a new or empty directory")
args.payload.mkdir(parents=True, exist_ok=True)
started = last_report = time.monotonic()
copied = 0
excluded_suffixes = {".pdb", ".lib", ".exp", ".obj", ".ilk", ".pyc"}
executables = {"freecad.exe", "freecadcmd.exe", "python.exe", "pythonw.exe",
               "qtwebengineprocess.exe"}
for folder in ("bin", "data", "doc", "Ext", "Mod"):
    for item in (args.build / folder).rglob("*"):
        if not item.is_file():
            continue
        relative = item.relative_to(args.build)
        if "__pycache__" in relative.parts or item.suffix.lower() in excluded_suffixes:
            continue
        if folder == "bin" and len(relative.parts) > 2 and relative.parts[1] in (
            "Include", "include", "libs", "Tools"):
            continue
        if item.suffix.lower() == ".exe" and item.name.lower() not in executables:
            continue
        destination = args.payload / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, destination)
        copied += 1
        now = time.monotonic()
        if now - started > 1800:
            raise SystemExit("Staging exceeded 30 minutes; inspect the partial payload")
        if now - last_report > 15:
            print(f"Staged {copied} files ({folder})", flush=True)
            last_report = now
shutil.copy2(source / "LICENSE", args.payload / "LICENSE")
# Include dependency licensing material, including Python package dist-info copied above.
for folder in ("licenses", "Licenses", "share/licenses"):
    location = args.libpack / folder
    if location.is_dir():
        shutil.copytree(location, args.payload / "dependency-licenses", dirs_exist_ok=True)
for name in ("COPYING", "LICENSE_LGPL_21.txt", "OCCT_LGPL_EXCEPTION.txt", "manifest.json"):
    if (args.libpack / name).is_file():
        destination = args.payload / "dependency-licenses" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.libpack / name, destination)
if (args.libpack / "sbom").is_dir():
    shutil.copytree(args.libpack / "sbom", args.payload / "dependency-licenses" / "sbom")
revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
(args.payload / "release-info.json").write_text(json.dumps({
    "product": "FreeCAD Plus", "release": "0.0.2", "source_commit": revision,
    "source": "https://github.com/Croft-Labs/FreeCAD-Plus",
    "configuration": "Windows x64 Release; see GitHub release notes for workbenches",
}, indent=2), encoding="utf-8")
files = [p for p in args.payload.rglob("*") if p.is_file()]
print(f"Staged {len(files)} files, {sum(p.stat().st_size for p in files):,} bytes")
