# Unified Loft acceptance — November 23, 2026

Owner approved the amended [Solid/Sheet native proposal](../loft-workflow-preview-20261123/README.md)
in chat: **"Approved. Implement"**. Its session/fingerprint were re-inspected as
fresh/in scope before implementation; tool approval state remains untouched.
The [task specification](../../ui-ux-specs/TASK_PANEL.md#unified-loft--november-23-2026)
owns intended behavior, and [architecture](../../ARCHITECTURE.md#unified-loft--november-23-2026)
owns kernel, persistence and routing details.

## Implemented

- Shared Loft creation/editing with Solid default, Sheet forcing/locking New,
  New/Add/Subtract, ordered five-row section collector, Up/Down/drag/Remove/Clear,
  Ruled surface, Closed and Refine result. Sheet creates uncapped geometry.
- Native solid construction including holes and vertex endpoints; sheet construction
  from open/closed sections. Invalid input fails before saved mutation; invalid
  Boolean results retain the tool for yellow/pink display and disable acceptance.
- Shared target selection and hidden-target display, selection color/translucency,
  valid green/red and invalid yellow/pink previews, manual preview, task error style,
  History navigation/restoration and usable tree eyes. Point sections remain visible
  as highlighted points while editing even if donor geometry is hidden.
- Explicit Component/source/target ownership; no Classic active-Body dependency.
  Source references remain predecessors. All consumed sketches hide on acceptance
  without being moved into the result's backend Body.
- One Plus Loft entry for single/multiple sketches and both binder types; Classic
  retains Additive/Subtractive Loft labels routed to shared Add/Subtract in component
  documents. Plus ribbon primary Loft starts New; its dropdown keeps native aliases.
  Unrelated binder commands retain their original entries. Existing native Loft
  features and ordinary legacy documents keep native properties/editors.

## Verification

- Native PartDesignGui and script build passed. Broad build suite: **118 checks**;
  expanded focused build suite: **17 checks**, including external recompute outside
  Edit and a transformed target with downstream face consumption.
- Installed broad suite: **120 checks**, zero failures/errors. Final **17 Loft checks**
  rerun after the vertex-highlight correction, zero failures/errors.
- Installed command/UI audit: real Plus/Classic commands, Solid/Sheet and target
  changes, internal-move model path used by section drag/drop, acceptance, same-ID
  editing, hidden target display, and exact Coin material colors for all four Boolean
  validity states. The second solid's Tip/geometry remain unchanged.
- Independent fresh process: saved sheet ID **743**, area **672.3225851241233 mm²**,
  and subtractive result **3620.851705978902 mm³** reopen/recompute unchanged.
- Separate binder watcher audit confirms one Plus Loft entry and Classic additive/
  subtractive entries for both ShapeBinder and SubShapeBinder, preserving other tools.
- The original desktop shortcut is verified separately in `shortcut.json`; its
  target/arguments/working directory are retained in `shortcut-target.json`.

Screenshots were visually inspected against the approved proposal:
[Solid](loft-solid-task.png), [Sheet](loft-sheet-task.png),
[single selection](modeling-single.png), [multiple selection](modeling-multiple.png),
[missing target](loft-add-target.png), [invalid feedback](loft-subtract-invalid.png).
Actual native geometry: [Add valid](loft-add-valid-geometry.png),
[Add invalid](loft-add-invalid-geometry.png),
[Subtract valid](loft-subtract-valid-geometry.png),
[Subtract invalid](loft-subtract-invalid-geometry.png).
These are working installed features, not the earlier disabled-OK prototype.

## Delivery and limits

Ten checked payload files are installed with SHA256 verification and rollback copies;
see `install-manifest.json`. Rollback copies remain in the runtime's
`validation/loft-20261123/install-backup`. Tests use isolated profiles and synthetic
documents; owner sessions/settings and unrelated `project.previewfirst.json` are
preserved. Generated validation output is archived here, then removed except for
rollback/manifest and the live shortcut validation profile. Original harness locations
are recorded in scripts; relative script inputs describe those workspace locations.

Initial smooth-Loft Boolean volume assertions were tighter than native B-spline
integration accuracy; analytic expectations now use one-part-per-million tolerance.
A transformed-shape assertion was corrected to inspect the one contained solid's
center of mass. The installed audit initially asserted an irrelevant Classic active
Body pointer after acceptance; Plus's normal context restoration clears it, so the
audit checks correct result ownership and preservation of the other solid instead.
These harness corrections did not alter geometry. A stale queued selection-list resize
was fixed by binding the callback to its Qt owner; final logs show no deleted-widget
callback errors. Earlier preview files remain historical evidence, not acceptance.
