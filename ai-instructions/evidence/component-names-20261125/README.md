# Assembly-wide component names — delivered November 25, 2026

Implemented and installed in the existing FreeCAD Plus owner payload. Restart
FreeCAD Plus to load the native save guard. No new layout was needed: the existing
source-qualified labels and existing dialog/panel error feedback implement the
owner's convention. No pending instance-display/quantity/removal preview was
treated as approved or installed by this change.

## Behavior

Distinct definitions must have unique names throughout a file's domestic and
transitively imported catalog, including unused parts. Repeated instances and
diamond imports of the same definition remain valid. Names compare case-insensitively,
ignoring surrounding whitespace and normalizing Unicode. Unrelated open files can
reuse names until an import would put their definitions into one scope.

Local tree rows have no filename suffix. Every imported row names its actual
defining file, including children belonging to a third file inside an imported
subassembly. See [installed tree](qualified-tree.png) after a source rename and
[existing collision feedback](conflict-feedback.png). The exact original tree
labels from the owner's example also pass native projection assertions.

Create/Rename/Add existing/Add new, batch import, independent copy, suggested new
names and native property-editor definition labels enforce the same scope. Loaded
reverse importers protect a source edit against names used in its host assemblies.
Conflicting operations identify both files and refuse before creating/importing
objects; they never silently rename or merge shared definitions. Independent
export retains its existing detached-copy behavior with unique destination labels.

Native Save/Save As/Save Copy and Plus saves reject unresolved collisions. Save As
checks before changing document filename/label; Classic saves bypass this guard.
Older conflicts remain navigable and can be repaired incrementally through Rename.
Restore/Undo/Redo retain native history; if they restore a conflict, saving is
blocked until repair. Closed importers cannot constrain a source edit until loaded;
reopening detects the conflict and reports it without silently rewriting files.

## Verification

- Final native App/scripts build passes (`build-verified.log`).
- Final installed affected acceptance: **81/81**, including 12 new naming cases,
  Add Component, part transfer, native rename menus, external definitions, native
  formats and Classic conversion (`installed-tests.txt`, `installed-result.json`).
- Final source focused acceptance: **15/15** after updating legacy fixtures to
  the new naming policy (`source-verified-*`). Earlier broader source runs exposed
  old fixtures that explicitly expected duplicate imported names; these were
  changed to check refusal/recovery and unique-name ownership instead.
- Fresh installed reopen: reverse-import rename refusal, real rename Undo/Redo,
  source save and second reopen, shared label propagation, persistent source UUID
  and component ID. Final `verified-reopen-result.json` passes.
- Existing desktop shortcut: **5/5**, including actual imported Rename menu UI,
  import refusal, native label edit, generated names, and Save/As/Copy refusal.
  Target, arguments and working directory remain unchanged (`shortcut-target.json`).
- An additional installed movement run passed **16/16** (`reopen-final-*`). That
  run resulted from the runner's original mode dispatch and is not fresh-reopen
  evidence; the dedicated verified-reopen run above supplies that evidence.
- All **16 installed file hashes** match source/build (`install-verification.json`).
  Two native DLLs and fourteen Python/test files were installed with retained
  `.before-naming-20261125` rollback copies; no separate app clone was created.
- `git diff --check` passes. Unrelated project.previewfirst.json is preserved.

The initial build was interrupted by a DLL lock from an early isolated validation
process. That process finished, builds and native validation were then serialized,
and the final build passed. Initial reopen harness path/binding assumptions were
corrected; no production changes were needed for those harness corrections.
Native logs include expected rejected operations and existing copy/UUID diagnostics;
the complete final tests report no failures/errors. This does not claim the entire
project test suite passed or resolve unrelated previously recorded constraint tests.

Helpers, final screenshots, installation manifest and relevant logs are archived.
Disposable test documents/profiles are removed after archiving. Existing payload,
development build, rollback files and owner shortcut remain intact. Helper paths
record their original local runtime; adapt those paths if replaying elsewhere.
