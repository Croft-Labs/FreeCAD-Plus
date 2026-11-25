# Condensed/expanded instances: installed

November 25, 2026. The owner's renewed implementation request approved the
[prepared native layout](../instance-display-proposal-20261125/README.md).
Companion review `1339cd788f26` was still fresh and within scope, fingerprint
`b97aa8298195bd804b0de852dacca11fa8524fe0c183480ecd9f7930f2bf3639`.
Approval is the chat instruction; no companion approval state was modified.

## Delivered behavior

- Assembly has an **Instances: Expanded / Condensed** selector below the active
  assembly controls. Expanded is the initial default; the preference persists
  across files and application restarts.
- Expanded numbers repeated siblings `Motor (1)`, `Motor (2)`, `Motor (3)`.
  Condensed shows `Motor ×3`, initially collapsed, with those same instances inside.
  Singletons retain their names. Imported components retain source-file labels.
- Groups use shared definition identity within the immediate parent occurrence.
  Equal text never merges different identities; repeated subassemblies get
  separate nested groups. Native object/link IDs and selection paths stay intact.
- Selection survives mode changes. Selecting a hidden occurrence reveals its
  containing groups. Reused rows retain their subtree fold state; ordinary
  refreshes respect a manual collapse. A quantity dropping to one removes only
  its presentation group. Rename and Undo refresh the labels and counts.
- Groups are presentation collectors with no native object selection, visibility
  eye or implicit Edit/Open/Rename/Copy/Paste target. Expand one and use an individual
  occurrence's existing actions. No definition, placement, constraint, active
  assembly/Edit context, or Undo entry is changed by switching modes.
- Constraint collectors remain first under actual parents/occurrences and start
  collapsed. A grouping collector does not become an assembly or solver owner.

Implemented in panel.py with an immutable presentation transformation and existing
row reconciliation. Init.py and CMakeLists register TestInstanceDisplay. Three
Python payload files were installed with matching source hashes and retained
rollback copies. No native rebuild was needed. Restart FreeCAD Plus.

## Native evidence

- [Expanded](expanded.png), [Condensed](condensed.png), [opened groups](individuals.png).
- [Fresh-process imported group and selected occurrence](reopened.png).

These screenshots are working installed controls, with production actions wired.
The fresh-process screenshot uses a larger validation window/dock to show the
tree; no production dock sizing rule was changed.

## Checks and limitations

- Initial source grouping suite: **8/8 passed**.
- Final installed focused suite: **9/9 passed**, including the eight grouping
  cases and the existing projection/ownership check. Tests cover actual mouse
  selection and double-click Edit, individual Copy/Paste, Move command routing,
  nested constraints, multi-selection, row identity, visibility/placement/model
  preservation, count/singleton changes and Undo, imported labels and preference.
- Fresh application process: saved preference, imported groups, stable document
  and object IDs, selection reveal, unchanged Edit/model/Undo all pass.
- Existing desktop shortcut: **3/3 passed** against the installed payload. Target
  remains the existing `Launch FreeCAD Plus.bat` in `_temp builds/FreeCAD-Plus`.
- Three final installed files were rehashed against source after all edits.

The broader initial run passed **41/47**. Five failures are reproduced with the
unchanged baseline panel: three old clipboard assumptions about a file-root tree,
and two import fixtures that conflict with the already-installed name uniqueness
rule (`Part001` or `Shared child`). Those existing tests/workflows were not modified
in this display task. The sixth failure is a viewport rotation-ring mouse-picking
check: it fails in the combined suite and passes alone on both baseline and final
installed code. Its suite-order sensitivity remains unresolved; do not describe
the broad regression suite as fully passing.

The intermediate installed-final run reports 38/40: the same combined ring failure
plus one mistyped harness test name. The intended projection test was corrected
and passed in the final 9/9 run. An initial fresh-process harness attempted to
activate the assembly before the host tab settled after external files loaded;
explicit host activation/event settling fixed the harness, and final reopening
passes. These intermediate results are retained alongside final results.

Visual inspection caught Qt losing subtree expansion when a reused item changes
parent. Reconciliation now explicitly retains it, with a native regression check.
Automatic reveal is restricted to Assembly; Parts and History behavior is retained.

Validation uses disposable CAD files and isolated profiles. Logs, screenshots,
runner sources and the installation manifest are archived here; generated profiles
and fixtures are removed afterward. The owner payload, useful build tree, rollback
copies, desktop shortcut and unrelated project.previewfirst.json are preserved.
Quantity/pattern creation, Remove instance and Clone remain separately pending.
