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

Before publishing, run model/task/CAM regressions against the payload, install the
actual `.exe` into an isolated directory, check installed file hashes, test launch
through FreeCADPlus.exe, and check uninstallation. Record limitations, source/build
identity, installer size and SHA256 in the roadmap/release notes. Publish only the
requested installer asset; a local build or draft release is not publication evidence.

Version 0.0.1 is the fork's distribution version. The upstream-derived engine version
can still be shown in About. This first package is unsigned and uses the focused
workbench configuration recorded in the release notes. The planned `.cadprt` format
and production part-history restructuring are not included.
