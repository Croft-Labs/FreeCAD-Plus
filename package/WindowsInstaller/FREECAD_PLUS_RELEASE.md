# FreeCAD Plus Windows pre-release packaging

The fork installer uses `FreeCADPlus-installer.nsi`, not the upstream installer.
It installs per user, uses a distinct uninstall key and Start-menu shortcut, leaves
file associations unchanged and retains user preferences/documents on uninstall.
The `FreeCADPlus.exe` launcher gives the application its own FreeCADPlus user-data
and temporary directories. Native FreeCAD executable and document identities remain.

Build Release with the project's existing CMake/LibPack configuration first.
Keep the build, payload, installer, test installation and logs outside Google Drive.
Do not run generated CMake install scripts that contain absolute upstream install
paths. From the repository root, with absolute paths substituted:

```powershell
python package/WindowsInstaller/stage-freecad-plus.py <build> <new-payload> --libpack <libpack>
python package/WindowsInstaller/package-freecad-plus.py <payload> <NSIS-makensis.exe> <output.exe>
```

The packager uses NSIS 3 and has finite compiler timeouts. Staging excludes developer
artifacts and non-runtime executables, retains Python sources, and includes available
dependency licensing metadata. The uninstaller uses an explicit installed-file list
and removes directories only when empty. Increment the version in the installer
and stage metadata for future releases.

For a new local test build, run `tests/BuildComponentDocument.ps1 -AllTargets`
with the existing CMake/build paths and a fresh evidence directory. This builds
every enabled target and stages the required Show helpers. Stage with
`--build-label 2026-10-02` (use the current build date); the payload metadata then
identifies a local test build and includes its CMake configuration without
assigning a release version. Validate the staged executable before delivering it.
Check that its native `App.Version()` commit agrees with the payload metadata;
an incremental build can retain an older Version.cpp object despite a current
generated header. The development guide documents a focused compile/relink when
that mismatch is demonstrated; revalidate the final staged bytes afterward.
For compatible Python-only updates, the development guide permits synchronization
without a native rebuild. Record `native_source_commit` separately from
`application_source_commit` and the synchronized module hashes; `App.Version()`
must match the native identity. Do not describe reused native acceptance as rerun.
Every owner build must also pass the mandatory desktop-shortcut delivery gate in
root AGENTS.md and the development guide before it is reported ready.

Before publishing, run model/task/CAM regressions against the payload, install the
actual `.exe` into an isolated directory, check installed file hashes, test launch
through FreeCADPlus.exe, and check uninstallation. Record limitations, source/build
identity, installer size and SHA256 in the roadmap/release notes. Publish only the
requested installer asset; a local build or draft release is not publication evidence.

The published 0.0.2 distribution predates the `.cadprt` component migration and
part-history restructuring. Dated local builds include the implementation recorded
in `ai-instructions/WORK_STATE.md`; their metadata and CMake configuration identify
the actual payload. About can still show the upstream-derived engine version.
Published packages remain unsigned unless their release notes state otherwise.
