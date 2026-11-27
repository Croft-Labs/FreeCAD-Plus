# Appearance task — installed November 27, 2026

Owner approved the revised native task/menu preview with “implement the appearance
workflow.” Companion review `7d416ef7065b` remained fresh with exact-file scope and
fingerprint `9e4700faddc26d192990be560c449565927f8d279fbda8127ebbcd96f134e3bc`.
Chat approval was used; tool approval state was not edited.

## Delivery

- Parts component context menus use the requested three groups. Appearance opens
  a native task with Body/Face targets, color chooser, linked transparency slider
  and number field, and Done/Apply/Cancel.
- Switching modes expands all CAD faces or deduplicates owning results. Eligible
  face selections survive the Parts right-click; viewport/History collection uses
  the existing click/Shift-click pattern. Remove, Clear and Delete edit the list.
- Whole components target their own result geometry. Body tips replace historical
  features; meshes support whole-object appearance. Child components, sketches,
  placements, geometry and identities are preserved. Mesh facets are not CAD faces.
- Only edited color/transparency fields change. Per-face materials retain other
  fields. Mixed selections remain unchanged until the corresponding field is edited.
- Apply commits one native Undo operation and stays open. Done applies and closes.
  Cancel discards unapplied edits. Imported definitions update their source and use
  FreeCAD's linked source/host Undo; Undo from the host restores the source colors.
- Stale context/geometry and wrong-component face picks fail before changing colors.

## Verification

The final source regression run passes **43/43**: Appearance, active assembly,
part transfer and component import. Installed runtime passes **11/11** Appearance
checks, including right-click selection retention, body/face switching, mixed
values, slider synchronization, whole/face/mesh/Body-tip materials, Cancel/Apply/
Done, source-owned edits, linked Undo, geometry identity, and native save/reopen.
Native color persistence has the existing 8-bit color quantization; reopening is
checked within 1/255 per channel.

The menu regression exposed an inaccessible display-settings target blocking the
entire popup. It is corrected: the menu opens, and unavailable display submenus
are disabled. Initial harness reruns also exposed reused export destinations and
overlong Windows temporary paths; the final run uses a fresh short directory.
Test label expectations were updated for the approved Import/Export menu labels.

`task-panel.png` is the installed task; `colored-body.png` is the native renderer's
actual Body result after whole-blue and selected-top-face-gold Apply operations.
These are working runtime evidence, unlike the separate approved preview image.
The native screenshot also confirms that editing the Body tip affects its visible
result. No native C++ build was needed for these Python-only changes.

## Installation and preservation

Eight installed Python/test files have matching source and payload hashes in
`install-manifest.json`. Prior files are backed up under external
`validation/appearance27/rollback`; new files are marked with no prior hash.
Owner profile CFG files and existing desktop shortcut retain their recorded hashes.
The shortcut still targets the existing `Launch FreeCAD Plus.bat`, with its original
working directory; the launcher targets `app/bin/FreeCAD.exe` and the owner profile.
Only isolated profiles and synthetic CAD files were used for testing. No owner CAD
file was edited, and no running owner session was closed. Restart an already-open
FreeCAD Plus process to load the updated modules.

The separate navigation/History retention and saved active-assembly persistence
proposal remains pending and is not included in this delivery. Existing unrelated
`project.previewfirst.json` was preserved and excluded from the commit.

Durable test logs, result JSON, approved/installed screenshots, validation macro
and install hashes are archived here. Disposable validation documents/profiles are
removed after archival; rollback files and the manifest remain outside the repo.
Publication is verified against the configured origin branch after commit.
