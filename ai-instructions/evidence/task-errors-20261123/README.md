# Prominent task errors — installed November 23, 2026

The owner approved the [native proposal](../task-error-preview-20261123/README.md)
in chat. Implementation used preview session `16176df60dd2`, fingerprint
`4f5aa46a46bf63433fa196c22609ad24163c52d38805f2ac1a0544c6c4581511`.
Chat approval is authoritative; the companion approval flag was not changed.

## Implemented behavior

Plane/Sketch placement and Extrude/Revolve now use shared `TaskStatus` feedback
for selection, validation, preview/result and acceptance errors. Errors use the
approved amber border/background, wrapped semibold plain text and padding.
New or changed errors scroll into view without taking focus. A bounded follow-up
handles native task-group layout changes. Repeated identical errors do not keep
scrolling; long errors reveal their beginning. Ordinary guidance and successful
recovery clear the error styling. Queued callbacks tolerate a closed task.

The shared widget is the documented standard for future inline task errors.
Existing native modal errors retain their presentation. This change does not alter
geometry, reference admission, History, visibility, schema or acceptance behavior.

## Verification

- `build-widget.json/txt`: three focused native widget tests passed.
- `installed-regression.json/txt`: all 122 installed regression checks passed.
- `installed-startup.json/txt`: five fresh-process startup checks passed.
- `visual.json`: four installed native selection-error/recovery cases passed.
  Errors were fully visible; valid recovery cleared highlighting; rejected
  references, native dependencies, IDs and saved visibility remained unchanged.
- `approved-comparison.json`: all four installed detail images are byte-identical
  to their approved screenshots. Installed Sketch and Extrude images were also
  visually inspected.
- `shortcut.json` and `shortcut-target.json`: launch through the existing desktop
  shortcut succeeded using an isolated profile and installed modules.

Installed screenshots: [Sketch](sketch-error.png), [Plane](plane-error.png),
[Extrude](extrude-error.png), [Revolve](revolve-error.png).

## Build, installation and reproducibility

Only `FreeCADPlusScripts` was built; no native rebuild was needed (`build.log`).
`install.py` installed five Python files and verified source/build/app hashes:
`task_status.py`, `plane_task.py`, `sketch_task.py`, `extrude_task.py` and
`TestTaskStatus.py`. `install-manifest.json` records hashes and original rollback
paths. CMake registers the shared module and test for subsequent builds/installs.

`run-validation.py` runs `regression.FCMacro` or `visual.FCMacro` in fresh isolated
profiles. Use `regression --repair` for the focused build check,
`regression --installed` for the installed suite, `visual --installed` for native
visual checks, and `regression --installed --ui-modes` for startup checks.
`restart-shortcut.ps1` and `shortcut.FCMacro` check the installed shortcut launch.

Runtime output lives under
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/task-errors-20261123`.
`cleanup.ps1` validates resolved direct-child paths before removing generated
fixtures and archived images; `cleanup.json` records removal. Original rollback
files and the active shortcut profile are retained. Existing owner sessions were
not closed or modified; save and restart those sessions to load cached Python
module changes.
