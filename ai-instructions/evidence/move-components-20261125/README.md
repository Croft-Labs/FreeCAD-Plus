# Move Components — installed November 25, 2026

The owner instructed “implement the move component workflow”, approving the
previously reviewed native Type/Method proposal. Companion review `f6ed77034205`
was inspected; its approval state was not changed on the owner's behalf.

## Delivered behavior

Assembly has a compact Move Components button beside its selector and the same
command on child-occurrence context menus. The task shows the fixed active assembly
and immediate parent, preserving independent Edit context. It accepts sibling
instances atomically, including unused and external assemblies. Root movement,
mixed parents, stale paths, scaled links, read-only/expression placements and
constrained children are refused.

- Move: normalized distance/vector, parent axes, picked straight axes, two points,
  point-to-point translation and dynamic arrows/planes.
- Rotate: located axis/angle, optional pivot, reverse and native rotation rings.
- Align: straight/circular/cylindrical axes, closest-point coincidence or parallel
  alignment, and coordinate systems including expanded origin/Z/X definitions.
- Native unit inputs, click-driven collectors, Delete/Remove/Clear, snapshots,
  optional preview, numeric handles, snapping and pivot-only relocation.
- Preview is scene-only. Apply writes native LinkPlacement values in the owning
  document in one Undo group. Shared-parent occurrences move consistently. Cancel
  discards pending motion; earlier Applies remain undoable. Handles and callbacks
  are removed on task/context/view/document exit.

Solver-driven movement of partially constrained components remains outside this
approved increment; edit the constraints. Clone and instance quantity/condensing
remain separate work. No native schema or C++ changes were needed.

## Direct screenshots of working functionality

These are captures of the installed native task using disposable real geometry,
not interactive simulations or the earlier UI-only mockup.

- [Distance and vector](vector-task.png)
- [Point to point](point-task.png)
- [Axis and angle](rotate-task.png)
- [Dynamic movement](dynamic-task.png)
- [Axis alignment](axes-task.png)
- [Coordinate systems](frames-task.png)
- [Native rotation handles](rotation-rings.png)

The capture exercise checks that previews preserve object identities, placements
and Undo history, and opens Move Components through the real right-click menu.

## Verification and remaining test limitation

- Final installed movement/reference/numeric acceptance: **22 applicable checks
  pass** in `installed-final-tests.txt`, including all 16 movement cases, circle
  and cylinder axes, native mouse arrows/rings, Escape, plane snapping, nested
  sharing, unused/external ownership, rollback, fixed root and Undo/Redo.
- Broader installed run: **60/61 pass**. The existing
  `test_selected_parent_and_child_are_initial_references` constraint test drops
  the parent reference in combined runs, also in the final 23-case run. It passes
  alone and immediately after the final source gesture check. A five-case
  comparison using preserved prior panel/movement modules also passes. Its
  order-dependent cause remains unresolved; this is **not** a claim that the
  entire regression suite passes or that the failure is proven preexisting.
  Native constraint creation/edit/solve, frame protection and the other broader
  assembly checks pass. No constraint implementation was changed here.
- Source checks: 22/22 affected checks and 16/16 movement checks pass at the
  recorded checkpoints; final native ring plus subsequent constraint check is 2/2.
  Earlier source combined run failed only an outdated Reference-versus-Excluded
  expectation, which was migrated to the current eligibility contract.
- Fresh installed reopening: domestic placements/fixed root survive; geometry
  remains editable with Undo. External links retain saved placement and subsequent
  movement/Undo stays in the source document without changing the host file.
- Existing shortcut: **4/4 pass**, including actual mouse translation/rotation,
  fixed root/collectors, saved group movement/Undo and Apply/OK/Cancel.
  The final shortcut run uses a fresh isolated Light profile. Earlier gesture
  checks inherited docking settings modified by the combined run and failed the
  projected ring hit; those failures are not counted as passing validation.
- Six installed method captures preserve geometry/Undo and the real context-menu
  command opens successfully. Python syntax and `git diff --check` pass.

Eleven Python files are installed in the existing owner payload, with retained
`.before-move-20261125` rollback copies for preexisting files. The manifest and
verification record confirm source/payload SHA-256 equality. The existing desktop
shortcut still targets `Launch FreeCAD Plus.bat`, with the same working directory,
and launches `app/bin/FreeCAD.exe`. Restart running sessions to load this update.

## Provenance and cleanup

`run.py`, macros, `install.py` and `shortcut.py` are local harness provenance,
not portable application code or release automation. Validation used separate
native processes, disposable documents and isolated user/system profiles under
`_temp builds/FreeCAD-Plus/validation/move-20261125`. Durable selected results and
screenshots are archived here; task-generated validation output was removed after
verification. The application, native build, owner settings/documents, rollback
copies and unrelated `project.previewfirst.json` were preserved.
