# Selected-solid Shell and Component-only routing — November 23, 2026

The owner reported Shell rejecting the first of two solids because the second Body
was active, then clarified: Plus has an active Component, no active Body; every
operation we modify must follow that rule. This is a correction to approved feature
routing, without a new layout. The durable migration rule lives in
[development guidelines](../../DEVELOPMENT_GUIDELINES.md#component-routing-without-an-active-body--november-23-2026).

## Changes and audit

- Shell resolves its backend Body from the selected solid before component/input
  admission. It does not require or change the globally active Body. Empty or
  ambiguous selection in Plus receives prominent guidance, never an implicit
  active-Body target. Existing invalid geometry and failed-editor rollback remain.
- Removed Extrude/Revolve's native fallback for older Body-owned sketches in Plus
  documents. These now use the same explicit New/Add/Subtract tasks as component
  sketches. Classic presentation in a Plus document shares this routing.
- Thicken already resolves explicit targets through the shared Component service.
  Plane/Sketch placement and component datum Line/Point creation resolve their
  owner directly. Native editor adapters can derive a backend Body from a resolved
  feature; ambient `pdbody` is not input authority. Ordinary legacy documents keep
  native access. Unmigrated feature families are not silently redesigned.
- Component/occurrence access, Reference/Excluded rejection, strict History,
  identity, geometry and the unrelated second solid are preserved.

## Checks

[31 build checks](build-regression.json) and [31 installed checks](installed-regression.json)
pass. They include Shell with the first solid selected and second Body active,
accept/Undo/Redo, no-active-Body Cancel, empty-selection rejection, older Body-owned
sketch command entry for Pad/Pocket/Revolution/Groove, explicit target selection,
native command/input restrictions and shared task entry. Existing Shell/Thicken
geometry, persistence and failed-entry checks also pass.

The independent [installed native audit](installed.json) confirms the first solid's
Shell is 240 cubic mm while the second remains 480 cubic mm. It also accepts new
Extrude/Revolve results from an older Body-owned sketch into independent backend
Bodies, and checks Plane, Sketch and datum Line/Point creation with a different or
absent active Body. An initial harness assertion used `owner` instead of the existing
Plane task's `definition`; corrected without changing application behavior.

[Fresh-process reopen/recompute](reopen.json) preserves Shell identity, ownership and
both volumes. [Existing shortcut check](shortcut.json) repeats the two-solid Shell
accept/Undo test with isolated settings. Four payload files were installed with
[hash verification and rollback copies](install-manifest.json). Owner sessions and
settings remain untouched; older running processes need restart to load new code.

Direct native captures: [selected-first-solid task](selected-first-shell-task.png),
[accepted first-shell and unchanged second solid](selected-first-shell-result.png).
