# Plane/Sketch placement and History ordering — November 23, 2026

The owner approved both direct screenshot proposals with: "implement the plane and
sketch placement as well as the reordering of the history tab". This is production
implementation evidence, following the plane-selection and history-reorder preview
folders. Preview tool approval state was not changed on the owner's behalf.

## Installed behavior

- Datum Plane and Sketch placement share compatible reference collection. Conflicts
  replace the defining set with the newest supported pick. Unsupported, foreign,
  self or later geometry does not discard earlier selections.
- Planes/flat faces, lines/straight edges and points/vertices are equivalent. Two
  distinct coplanar lines and three noncollinear points remain supported. Line+point
  in either order defines a plane through the point, normal to the line.
- Hidden `NormalToLine` preserves the historical containing-plane construction when
  absent/false. Open, recompute and Cancel do not migrate saved geometry. New/changed
  reference sets opt into normal-through-point; unchanged old feature edits preserve
  their original construction. Explicit origin/axis overrides retain their meanings.
- History keeps Coordinate System fixed first, allows one-feature drags and stores
  preferred independent order on the source component as hidden `PlusHistoryOrder`
  string identities. All native dependencies remain topologically ordered. Invalid
  moves clamp before the first consumer or after the last predecessor and show a
  naming popup. No ownership, links, IDs, visibility or solid geometry are rewritten.
- Active tasks/transactions and stale context/identity sequences prevent reordering.
  Source Undo/Redo and save/reopen preserve order. FreeCAD's native coordinated Undo
  marker also appears in an active external host; host properties remain unchanged
  (`src/App/Document.cpp`, `Document::_openTransaction`).

## Verification

- `build-focused.json/txt`: 62/62 build-native checks passed before the external
  ownership test was added. `initial-focused.txt` retains the two initial failures:
  a fixture left a transaction open, and a previous test expected all drag flags off.
- `installed-broad.json/txt`: 212/213 passed. The one error was a nonexistent import
  helper in the new external-source test fixture, corrected to the established
  `external.import_file` and `hierarchy.add_instance` APIs.
- `installed-repair.json/txt`: corrected external-source test passed. An intermediate
  diagnostic proved there were zero host-property changes; its Undo-count assertion
  was corrected for FreeCAD's native coordinated transaction marker. No product
  change was needed for either external fixture correction. Total broad coverage:
  **213/213**, across the broad run and targeted repair.
- `installed-focused.json/txt`: 63/63 final focused checks passed after correcting the
  point-origin helper text to reflect the actual plane origin.
- `installed-startup.json/txt`: 5/5 startup/UI-mode checks passed in a separate fresh
  installed process.
- `live.json`: installed Qt drop-handler fixture verifies independent move, dependent
  clamp/popup, unchanged native graph/visibility/volume and actual native selection
  observer input into both placement tasks. It uses Qt drop events, not OS mouse input.
- `reopen.json`: a separate installed process reopens the saved model and verifies
  exact preferred order, object IDs, new plane/sketch origin and normal, legacy
  containing-plane geometry and solid volume.
- `shortcut.json` and `shortcut-target.json`: existing desktop shortcut launches the
  installed runtime using explicit isolated user/system/data paths.
- `install-manifest.json`: source/build/app SHA256 matching for all nine changed
  Python files; original rollback files retained in the runtime validation folder.
  Only the FreeCADPlusScripts target was required; no native binary changes.

**Mouse verification limitation:** the computer-use `sky` API and `cua_repl` both
listed the isolated FreeCAD window, then rejected its exact returned handle with a
window-owner mismatch (identical displayed application IDs). No OS mouse drag was
performed or claimed. Native Qt drop handling, order correction, persistence and
the popup were verified in the installed app. The fixture was then completed using
explicit Qt drop events, with no production preview callbacks.

## Screenshots and reproducibility

- [Installed corrected History](installed-history.png)
- [Installed dependency popup](installed-popup.png)
- [Installed Plane selection](installed-plane-selection.png)
- [Installed Sketch selection](installed-sketch-selection.png)

The task-widget captures have transparent backgrounds; use a light background to
view their black text. These are actual installed widgets, not interactive mockups.

`run-validation.py` runs `regression` (focused by default, `--broad`, `--repair`, or
`--ui-modes`) and `reopen` with `--installed`. `run-live.py --installed` runs the
installed Qt/drop and saved-model fixture. All launches set isolated settings and
bounded deadlines. The fixture generates `PlaneHistory.cadprt` under
`<runtime>/validation/plane-history-20261123`; no owner document/profile was used.
After results were archived here, temporary models/screenshots/profiles were removed
by the resolved-path-checked `cleanup.ps1` (see `cleanup.json`). Run the live fixture
again before rerunning reopen.

Original rollback data and the shortcut profile remain under that validation folder.
Unrelated untracked `project.previewfirst.json` was preserved. Installation and test
artifacts do not change the owner profile or the existing shortcut.
