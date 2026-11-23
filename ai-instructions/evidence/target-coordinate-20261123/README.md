# Target selection and persistent coordinate systems — November 23, 2026

Owner authorization: "make it so that the base coordinate system created with each part
cannot be deleted" and "then implement both the target selection and the coordinate system
persistence". This approves the revised inline-highlight/sole-solid proposal, not the
superseded popup. Baseline: `f8826fdd2d78d72225e71186baef5f726fa96d22`.

## Implemented behavior

Shared Extrude/Revolve target handling counts eligible current Body results in the edited
component. Add/Subtract automatically choose exactly one candidate on operation entry,
including direct Pocket/Groove startup. Existing valid targets survive mode switches and
editing; self/later results cannot be chosen. Missing targets receive the approved amber
field and inline guidance before profile/region selection. Clear remains empty through
ordinary updates. Invalid targets are cleared; deletion of an active input closes the task
through its existing deferred cleanup. Hidden selected targets keep their native History
eyes and temporary selected presentation. No modal target prompt is introduced.

The native document removal path now rejects independent deletion of owned App::Origin
objects and their native datum children in Plus documents before transaction/reference
mutation. The native GUI deletion veto remains in place. The file, component and backend
Body frames are protected. Existing files need no schema migration, new properties or
replacement objects. Whole-owner removal, Undo/Redo, transaction abort, custom datum
deletion and ordinary legacy document behavior remain supported.

## Preview and implementation evidence

Approved revised preview: session `ac148f57d8fe`, fingerprint
`b53ce972452a4bfb803940133c9713795dea855d781661e1b2618c254b3f55be`,
snapshot baseline `e56d5fefc6411a151d5656af4782266c6315ed93`. Its fixture candidate
lists were replaced with production eligibility and intake handling here.

These are screenshots of the **installed working application**, with real candidate
enumeration: [multiple solids](multiple-solids.png), [sole hidden solid](sole-solid.png),
[no solid](no-solid.png), [Revolve Subtract](revolve-target.png). Screenshots were visually
reviewed. The [12-case result](visual.json) confirms both tools, both modes, all candidate
counts, target focus, no popups and unchanged native IDs/visibility after Cancel.

## Build and verification

- Native `FreeCADApp` and `FreeCADPlusScripts` build succeeded: [build log](build.log).
- All **16 focused build tests** passed: [result](build-focused.json), [test log](build-focused.txt).
- All **202 installed regression tests** passed: [result](installed-broad.json),
  [test log](installed-broad.txt). Includes the nine new target/frame tests, strict sequential
  History, Extrude/Revolve, visibility, sketches, panel controls, native feature inputs,
  Boolean operations and legacy conversion.
- All **5 startup tests** passed in a separate fresh process:
  [result](installed-startup.json), [test log](installed-startup.txt).
- A separate installed process reopened the saved fixture and rejected **24** individual
  frame-object deletion attempts, preserving all IDs and visibility: [result](reopen.json).
- [Installation manifest](install-manifest.json) records source/build/install hashes and
  retained rollback copies for the two native libraries, two shared task modules and new
  regression module. [Shortcut verification](shortcut.json) confirms installed module paths
  and isolated settings. [Shortcut target](shortcut-target.json) records the existing launcher.

Validation used only isolated profiles under the development runtime's
`validation/target-coordinate-20261123`. Before installation no owner-profile FreeCAD
process was running. The existing desktop shortcut was launched with explicit isolated
configuration arguments. No owner profile, unrelated shortcut or `project.previewfirst.json`
was changed. Reproducible build, regression, visual, reopen, install, shortcut and bounded
cleanup scripts are retained here. Runtime cleanup preserves rollback copies and the
currently launched isolated profile.

## Publication

Implementation, specifications and this evidence are committed together on
`codex/freecad-1.1.4-baseline` under the standing commit/push authorization. Push/remote
verification is recorded in the final handoff; this document does not imply a release.
