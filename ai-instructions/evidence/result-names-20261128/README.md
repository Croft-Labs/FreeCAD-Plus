# Feature result names — November 28, 2026

Owner request: editable resulting-object names in Preview for every feature operation
that contributes to component History. Preserve existing automatic naming, except
mesh defaults use `<owning part label>_Mesh001`, `002`, and so on.

## Approval and visual evidence

The owner explicitly approved the direct screenshots in chat: “approved, implement
it for all feature operations”. See [approval](owner-approval.json),
[before](preview-current.png), [approved proposal](preview-proposed.png), and
[implemented native panels](implemented.png). The first two are isolated native Qt
UI snapshots; the last runs the actual implementation, with actual allocated defaults.
The companion's historical `approved: false` is preserved; chat approval is recorded
separately, never impersonated through tool approval state.

Preview source was `c7d6d188c6`, companion `7010d6170aa0`, fingerprint
`06f01b3b959576fcecd3a7f4ff1ced1fca9d09866071c02a0320f2d12f03f410`.
Implementation incorporates the intervening committed unit fixes through
`3cf7c1fa59`; those changes and the unrelated untracked preview configuration are
preserved. The final native screenshot verifies the integrated layout.

## Implementation

`result_names` owns draft fields, automatic allocation and label validation.
Extrude/Revolve/Loft/Thicken share their existing task/save adapters. Plane, sketch
placement, Shell, Mesh From Shape, Trim Body, reference image, Clone/Extract and
whole-shape transforms have the same field in Preview. Multiple outputs expose one
field each; source-keyed drafts survive collector reorder and recalculation.
Editing preloads saved labels. Apply prepares the next defaults; Cancel discards
draft changes. Internal names, persistent IDs and geometry references do not change.

The TaskView bridge provides fields to native component History feature editors,
including dress-ups, datum features and Part Design tasks. Native Boolean and
primitive creation apply labels inside their original transaction. Immediate Cut,
Fuse, Common, Section, Compound, Compound Filter, Explode Compound, Join tools,
Slice/Slice Apart, Boolean Fragments, XOR and Defeaturing first review result names,
then replay their native command. Native geometry/services remain authoritative.
New split/explode output containers are normalized into component ownership.
Legacy documents retain their original commands and dialogs.

This covers the component History workflows; it does not add unsupported workbench
operations to component documents or rename existing features retroactively.

## Verification

Native `FreeCADGui`, `PartGui` and `FreeCADPlusScripts` targets built successfully.
The naming suite exercises default allocation, custom labels, empty validation,
save/reopen, Undo/redo, edit/Cancel, per-source fields and Apply reset; native Fillet,
datum, Boolean, primitive and immediate-command paths run against compiled binaries.
Boolean ownership regressions were updated to confirm the new review step while
retaining assertions for geometry, identity, eligibility, persistence and Undo.

The broad 170-check run had 165 passes, two keyboard-focus failures and three import
fixture errors. Both keyboard cases pass when rerun without competing GUI processes.
The three import errors reproduce in the unchanged installed app: the old external
Extrude, Revolve and Loft fixtures create duplicate component label `Part001`.
They remain a documented baseline limitation; this task does not modify those fixtures.

The 41-check native run exposed four missing warning-dialog compatibility cases and
one test using Apply instead of the primitive dialog's Create button. These were
corrected; all 18 focused final checks pass. In the installed app, all 53 naming,
ownership, mesh and transformation checks pass. That invocation also had one loader
error from a nonexistent unit-test class name; correcting the invocation runs all
five unit-persistence checks successfully. Thus all 58 executed installed checks
pass. The final screenshot is captured from the installed app, not the staged build.

## Installation

Thirty verified files were installed into the existing development app. The payload
includes the preceding already-committed unit-persistence update, whose installation
had been waiting for the owner session to close. Source/build/app Python hashes and
built/installed native hashes match. Owner profiles and desktop shortcuts are unchanged.
The installed app runs with isolated test profiles; no owner documents are modified.
See [manifest](install-manifest.json) for exact file hashes and protected settings.

Runtime and build trees use the established `dgium/Documents/__Apps/_temp builds`
location; the older `GAMING-PC` paths in AGENTS are unavailable on this machine.
Committed scripts and logs make validation reproducible. These are local development
app changes, not a release or packaging claim.
