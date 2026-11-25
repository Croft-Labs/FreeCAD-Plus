# FreeCAD Plus icon B — installed

November 25, 2026. The owner selected **B** from the six direct screenshots:
the existing FreeCAD artwork with a green plus/white outline in the lower-right.
Their original request also specified the same selected icon for `.cadprt` files.
Review `f489ddbb8ff8` was inspected fresh without scope violations; fingerprint
`5bc42a1f80c29b43a7710dbe3f6f4af21f5950e02b91a5e9bcfc14a06f7fbec3`.
Chat selection authorizes implementation. Companion approval state was untouched.

## Artwork and native implementation

- [Selected icon](icon-b.png) and [the approved options sheet](approved-options.png).
- `src/Gui/Icons/freecad-plus.svg` exactly matches candidate `b.svg`; original
  FreeCAD artwork is retained under the single overlay group.
- `src/Tools/build_plus_icon.py` generates ten transparent Windows ICO frames:
  16, 20, 24, 32, 40, 48, 64, 96, 128 and 256 pixels. `src/Main/icon.ico` embeds
  them in the GUI/command executables and installs as `bin/FreeCADPlus.ico`.
- Main GUI and embedded GUI configuration select `freecad-plus`; QRC includes
  the SVG in ordinary and theme resource paths. Classic SVG/document icons stay
  unchanged. The Plus file chooser explicitly recognizes `.cadprt` case-insensitively;
  Plus catalog/file rows use the same icon.
- CMake tracks the ICO as an explicit RC object dependency and copies it with
  configure_file, so later icon changes rebuild executable resources reliably.

## Windows integration

`.cadprt` had no association or UserChoice override. The explicit
`Register-FreeCADPlus.ps1` script created current-user `.cadprt` and
`FreeCADPlus.Document` entries, sets the icon and a quoted single-instance open
command, and preserves the existing portable user configuration through --user-cfg.
It saves prior values and does not alter protected Windows UserChoice entries.
It follows Microsoft's [custom icon registration](https://learn.microsoft.com/en-us/windows/win32/shell/how-to-assign-a-custom-icon-to-a-file-type)
and [per-user file type / shell refresh](https://learn.microsoft.com/en-us/windows/win32/shell/fa-file-types)
mechanisms. The script ships beside the installed ICO for explicit registration;
this is not a new NSIS release or a rewrite of the upstream installer.

The existing `freecad plus 0.1.0.lnk` now explicitly uses `FreeCADPlus.ico,0`.
Its launch batch, arguments and working directory are unchanged, as recorded in
[before](shortcut-before.json) and [after](shortcut-after.json) snapshots.
The archived reference shortcut is untouched. `.FCStd` remains FreeCAD.Document,
with the original icon/open command in `C:/Program Files/FreeCAD 1.1.4`.

## Verification and delivery

- Native Release build passes; incremental resource-dependency build confirms both
  executable RC objects were compiled. Logs: [build](build.log),
  [resource dependencies](resource-dependencies.log).
- All **27 file workflow checks pass**. The initial 30-check set had one icon
  fixture failure: it selected a component row instead of an external file group.
  The corrected file-group check passes in the **3/3 focused icon run**.
- The existing desktop shortcut passes **3/3** with isolated test settings.
  Checks cover the actual application/window resource, executable resource,
  ICO frames, Windows file/shortcut provider, `.cadprt` association, Classic
  preservation, actual native Open dialog and component source catalog.
- [Installed icon samples](shortcut/installed-icons.png) come from the real app and
  Windows providers. [Open dialog](shortcut/open-file-icons.png) is an actual native
  file dialog. Samples requested at 96 px may show the app-window/Classic provider's
  lower native resolution; executable and `.cadprt` use the multi-resolution ICO.
- Ten installed files match [the SHA-256 manifest](install-manifest.json), with
  payload rollback copies retained. [Final checks](final-checks.json) also verify
  selected artwork and preserved Classic assets. The app needs a restart to load
  the new window resource. No settings profiles or user documents were replaced.

Association rollback data is in [association-backup.json](association-backup.json).
Validation helpers are in [helpers](helpers). The shortcut-launcher fixture initially
had an extra closing parenthesis, corrected before its successful run; this did not
affect production code. C++ files retain their existing CRLF endings; patch checks
treat CR-at-EOL as valid. No broad line-ending rewrite is included.

Durable evidence was retained before removing only the generated
`validation/plus-icon-20261125` directory. Useful app/build trees and rollback files
remain. The unrelated untracked `project.previewfirst.json` is preserved. Completed
changes are committed and pushed to the origin fork under standing authorization;
no upstream push, force-push or release is part of this task.
