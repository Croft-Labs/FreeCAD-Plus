# History Appearance and face highlighting — installed November 27, 2026

The owner approved implementation of the History menu and staged face-highlighting
correction. The [owning specification](../../ui-ux-specs/COMPONENT_PANEL.md#history-appearance--approved-november-27-2026)
records the exact chat approval and fresh companion fingerprint. Companion approval
state was not modified. [Approved preview](approved-preview.png) used native menus
and task controls with a read-only historical-feature fixture; the installed
implementation below performs real native material edits.

## Delivered behavior

- History's part header offers Rename and Appearance. Its Appearance action keeps
  eligible bodies/faces selected before right-click; no prior selection stays empty.
- A geometric History feature offers Appearance with that exact feature selected,
  including historical Body features. Materials are edited on that object without
  substituting its Body tip, changing visibility or creating geometry/history nodes.
- Body containers still resolve their tip. Child components, sketches and coordinate
  groups are excluded. Newly created geometry requires reopening the task; stale
  selected geometry/context is rejected before any material change.
- Initial hover/edge/vertex input cannot target the whole part. Face overlays call
  `Part.getShape(..., needSubElement=True)` and admit only a Face shape. Previously,
  the default ignored the face suffix and returned the entire solid.
- Existing Body/Face conversion, bottom buttons, Apply/reset, preference colors,
  material field preservation, native Undo and imported-source ownership remain.

## Verification

| Run | Result |
| --- | --- |
| s1 | 21/21 source checks: existing Appearance suite, new History checks, native selected/preselected rendering and connected-surface picking. |
| s2 | 2/2 additional checks: imported historical-feature menu with linked Undo and native screenshot capture. |
| i1 | 22/22 installed-app checks, including the imported case. |

The tests exercise actual native right presses and popup actions, prior face/body
selection retention, no-selection defaults, exact hidden historical-feature
targeting, per-face and whole-object edits, source/host Undo, Cancel, reset, saved
materials, stale geometry, child rejection and unchanged visibility/identities.
The highlight regression checks that every extracted overlay shape contains exactly
one face, rather than merely detecting some highlight-colored pixels.

Installed rendering: [one selected face](history-face.png), [preserved face target
in the task](history-face-task.png), and [historical Pad target](history-feature-task.png).
Only the top face is blue; the two other visible faces retain gray. Native
`saveImage` captures the 3D view because QWidget.grab does not reliably capture its
OpenGL surface. The task captures use the actual dock widget. Selected/preselected
preference-color captures are also retained. No images were retouched.

`FreeCADPlusScripts` builds successfully; no native binary changes were needed.
Seven installed Python/test files match source and build SHA-256 values in
`install-manifest.json`. Owner CFG/shortcut hashes remain unchanged. The existing
`FreeCAD Plus 2.0.0.lnk` still targets `Launch FreeCAD Plus.bat`, with empty arguments
and the original FreeCAD-Plus working directory. That launcher still uses the
owner profile and `app/bin/FreeCAD.exe`.

Testing used isolated profiles and synthetic documents only. No owner model was
opened/saved and no owner process was closed. Rollback copies and the manifest are
retained under the external `validation/history-appearance-fix27` directory.
Disposable run documents/profiles are removed after archiving these logs/screenshots.
Restart any already-running app to load the new modules. The separately previewed
active-part persistence change is not included. Unrelated `project.previewfirst.json`
is preserved and excluded from commits.

Source changes, tests, specifications and this evidence are committed and pushed
to the configured origin branch; remote HEAD is checked after publication.
