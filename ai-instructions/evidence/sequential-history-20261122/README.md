# Strict sequential component History

Owner approval: **"approved, implement strict sequential history and prevent sketches
or other inputs from being ordered after the features that use them"**.
The approved [native presentation preview](../sequential-history-preview-20261122/README.md)
was inspected fresh with no scope violations: session f56b79f8df59, fingerprint
3fe344aa83245ac2eced333283b2f48c059239923e9719d9be8ae1961aeea944.

History now topologically orders native feature/input dependencies across backend
Body membership, with native creation IDs as the stable tie break. Body references
resolve to the visible Tip; native expression links participate. Coordinate frames
remain first and child components have independent histories. Ownership, identities,
geometry, authored visibility and schema are not rewritten. Cycles report an error.

The shared predecessor check rejects later/self references before supported editor
mutations. It covers Extrude/Revolve profiles, targets, directions/axes and limits;
sketch placement; plane preview/save; and native geometry-admission paths including
attachment, sketch external geometry, sweeps, dress-ups, transformed features,
Compound drops and supported property editors. Component/Body command-start admission
remains creation. No drag-reorder control is added. Arbitrary Python assignments and
native recompute are not global mutation hooks; existing native dependencies are
always projected in dependency order, including previously misordered saved files.

Validation:

- [Development checks](build-regression.json), [log](build-regression.txt): 28 passed.
- [Aggregate installed acceptance](acceptance.json): all 165 unique native tests passed.
  The [160-case run](installed-regression.json), [log](installed-regression.txt) had
  154 passes and six conversion fixture collisions (existing output destinations).
  [All nine conversion tests passed](legacy-regression.json) in a fresh directory:
  [retry log](legacy-regression.txt). [Five UI-mode tests passed](ui-regression.json)
  in a separate startup process: [UI log](ui-regression.txt). The included summarizer
  verifies that every original failed test has a passing retry and none is unresolved.
- [Actual History click](visual.json) rejected a later sketch while editing an
  earlier Extrude, retaining its original profile. The reviewed
  [installed screenshot](history.png) matches the approved sequence.
- [Fresh reopen](reopen.json) preserved sequence, identities and solid volumes.
- [Existing shortcut](shortcut.json), [target](shortcut-target.json) launched a
  separate isolated updated instance. The owner's unsaved window stayed open.
- [Cleanup](cleanup.json) removed disposable fixtures and inactive profiles,
  retaining rollback copies, durable evidence and the active shortcut profile.
- [Installation](install-manifest.json): source/build/app hashes match for 8 product
  modules and 7 test modules. Original rollback hashes are recorded separately from
  the prior copy on each installation pass; backups remain in task install-backup.

The new seven-case sequential suite checks interleaved feature chains, independent
ownership-list reordering, native expressions and Body result references, cycles,
rejected future profile/target/axis/limit/sketch/plane inputs without mutation,
actual History selection and native Compound drop, Undo/Redo, and saved identities.
Existing fixture changes create target/limit/filter inputs before consumers; the
legacy Boolean test now expects native creation order for its independent sources.
The empty-selection command test explicitly picks its profile in the shared task.
The UI-mode fixture compares persistent native toolbars, excluding the already-approved
Plus-only split-button controls that intentionally disappear in Classic mode.

Initial test runs exposed those old nonsequential fixtures, a fixture transaction,
and startup-visibility tests run after other fixtures deliberately closed the dock.
Fixtures were corrected; UI-mode checks run in their own fresh process. The harness
also excludes imported helper test classes to avoid unintentionally repeating suites.
Product ordering logic did not need weakening to accommodate these fixtures.

Runtime: C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus.
All checks use isolated profiles. The already-open owner window has an unsaved
Unnamed document and is left untouched. The existing shortcut launches a separate
isolated updated instance; the owner's older process needs a restart after saving.
Rollback backups and the active isolated profile are retained; disposable fixtures
are removed after final acceptance. Unrelated project.previewfirst.json is preserved.
