# SPDX-License-Identifier: LGPL-2.1-or-later
"""Finalize a compatible Python-only owner payload with explicit native identity.

Usage: python tools/FinalizeOwnerBuild.py <audit-root> <validated-baseline-payload>
Run after packaged acceptance and the verified owner-shortcut update.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import zipfile

source = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1]).resolve()
baseline = Path(sys.argv[2]).resolve()
payload = root / "FreeCAD-Plus-2026-10-02"
started = last_progress = time.monotonic()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def progress(message):
    global last_progress
    now = time.monotonic()
    if now - started > 1800:
        raise RuntimeError("Owner package exceeded thirty-minute deadline")
    if now - last_progress > 15:
        print(message, flush=True)
        last_progress = now


revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
subprocess.run(["git", "diff", "--quiet", "--", "src"], cwd=source, check=True)
base_manifest = read(baseline / "BUILD-MANIFEST.json")
native_revision = base_manifest["source_commit"]
phases = ("feedback", "sketch", "sketch-cold", "panes-tree-startup", "ribbon-complete",
          "owner-launcher/bootstrap", "owner-launcher/plus", "owner-launcher/classic")
reports = {phase: read(root / "acceptance" / phase / "results.json") for phase in phases}
for phase, report in reports.items():
    assert report["passed"] and not report["source_overlay"], phase
    assert not report["unexpected_gui_diagnostics"], phase
    assert report["version"][7] == native_revision, phase
    assert Path(report["application"]).resolve() == payload.resolve(), phase
    assert all(not suite["failures"] and not suite["errors"] and not suite["skipped"]
               for suite in report["suites"]), phase
assert reports["feedback"]["payload_verified"]
assert all(entry["matches_source"] and entry["in_build"]
           for entry in reports["ribbon-complete"]["runtime_modules"].values())
shortcut = read(root / "shortcut-verification.json")
assert shortcut["verified"] and Path(shortcut["target"]).resolve() == payload / "FreeCADPlus.exe"
updates = {"Ext/freecad/gui/PlusRibbon.py": source / "src/Gui/PlusRibbon.py",
           "Ext/freecad/gui/ComponentNavigator.py": source / "src/Gui/ComponentNavigator.py"}
base_files = {entry["path"]: entry for entry in base_manifest["files"]}
for name, expected in updates.items():
    assert digest(payload / name) == digest(expected), name
summary = {"application_source_commit": revision, "native_source_commit": native_revision,
           "native_rebuilt": False, "python_only_updates": {name: digest(payload / name) for name in updates},
           "tests_executed": sum(report["tests_run"] for report in reports.values()),
           "phases": {phase: report["tests_run"] for phase, report in reports.items()},
           "source_overlays": False, "owner_launcher_cold_restarts": True,
           "shortcut_verified": shortcut, "baseline_validation": str(baseline / "BUILD-VALIDATION.json"),
           "baseline_validation_rerun": False}
(root / "build-validation-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
(payload / "BUILD-VALIDATION.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
info = read(payload / "release-info.json")
info.update(source_commit=revision, application_source_commit=revision, native_source_commit=native_revision,
            build_label="2026-10-02 audit", distribution="local portable test build; unsigned")
(payload / "release-info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
(payload / "README.txt").write_text(
    "FreeCAD Plus - October 2, 2026 audit build\n\nRun FreeCADPlus.exe. Keep this entire folder together.\n"
    "The desktop FreeCADPlus.exe - Shortcut points here. Earlier 10/2 folders are preserved.\n"
    "Includes the compact Plus ribbon, common File/Edit/Clipboard bar above it, medium Home icons,\n"
    "Design Assembly tab, complete Home groups, and an independent New Component model action.\n"
    "Plus UI, Blender and Imperial Decimal are defaults; saved explicit choices are preserved.\n\n"
    f"Application sources: {revision}\nNative engine reused: {native_revision}\n"
    "Only the two GUI Python modules listed in BUILD-VALIDATION.json differ from the validated baseline.\n"
    f"Packaged acceptance: {summary['tests_executed']} passing executions, no source overlays.\n"
    "See BUILD-VALIDATION.json for phase evidence and BUILD-MANIFEST.json for exact file hashes.\n"
    "FEM is disabled; printing modes require installed addons. Physical owner acceptance remains separate.\n"
    "This is an unsigned local test build, not an installer or published release.\n", encoding="utf-8")
files = sorted(path for path in payload.rglob("*") if path.is_file()
               and "__pycache__" not in path.parts and path.suffix != ".pyc"
               and path.name != "BUILD-MANIFEST.json")
entries = []
for number, path in enumerate(files, 1):
    relative = path.relative_to(payload).as_posix()
    sha = digest(path)
    if relative.split("/")[0] in ("bin", "Mod", "Ext", "data", "doc") and relative not in updates:
        assert relative in base_files and sha == base_files[relative]["sha256"], relative
    entries.append({"path": relative, "size": path.stat().st_size, "sha256": sha})
    progress(f"Verified {number}/{len(files)} payload files")
manifest = {"source_commit": revision, "application_source_commit": revision,
            "native_source_commit": native_revision, "files": entries}
(payload / "BUILD-MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
files.append(payload / "BUILD-MANIFEST.json")
archive = root / "FreeCAD-Plus-2026-10-02-Audit-Windows-x64.zip"
assert not archive.exists(), "Preserve existing archives; use a fresh audit root"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as package:
    for number, path in enumerate(files, 1):
        package.write(path, arcname=path.relative_to(root))
        progress(f"Archived {number}/{len(files)} payload files")
with zipfile.ZipFile(archive) as package:
    assert len(package.infolist()) == len(files)
    assert package.testzip() is None
artifact = {"archive": str(archive), "size": archive.stat().st_size, "sha256": digest(archive),
            "application_source_commit": revision, "native_source_commit": native_revision,
            "unchanged_runtime_matches_validated_baseline": True, "zip_crc_verified": True}
(root / "artifact-result.json").write_text(json.dumps(artifact, indent=2), encoding="utf-8")
print(json.dumps({"validation": summary, "artifact": artifact}, indent=2), flush=True)
