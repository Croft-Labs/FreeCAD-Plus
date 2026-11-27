# Approved pending workflows — November 27, 2026

The owner approved all six pending groups with “implement all changes in progress.”
They subsequently confirmed “Saved and closed” before replacing native binaries.
The existing FreeCAD Plus installation is updated and can be reopened.

## Delivered behavior

1. Parts/Assembly menus offer **Edit within assembly** and **Edit in isolation**.
   Double-clicking a member uses assembly context. Editing retains the fixed active
   assembly and exact placed occurrence. Unplaced roots and externally defined
   assemblies resolve their correct source/frame without importing an extra copy.
2. A file with one local part defaults to that part as active assembly, unless a
   valid saved/manual assembly choice exists. Imported catalogs and body features
   do not count as local parts; the existing saved bookmark persists the choice.
3. Sketcher Symmetry defaults to creating constraints. Source points on the line
   axis receive Coincident constraints with their counterparts; other line-axis
   points retain Symmetric constraints. Point-centered symmetry is unchanged.
4. Toolbar tabs reuse the Components tab sizing rules: equal preferred widths,
   equal shrinking to text-safe minimum, then scrolling when necessary.
5. Appearance, Move, Sketch Pattern and Sketch Symmetry place Done/Apply/Cancel
   below fields. Successful Apply clears target/reference lists, pending picks,
   previews and handles and restores defaults. Invalid input stays available for
   correction; Done with an empty reset form closes it. Appearance highlights use
   enabled selection/preselection preference colors through unpickable overlays,
   without modifying saved materials or Undo state.
6. Face-only collectors show Single surface, Connected surfaces and Tangent
   surfaces; curve and surface intents are remembered independently. Appearance
   Face, Extract, Shell/Thicken face fields and native dress-up face lists declare
   their domain explicitly. Mixed Draft line/plane fields restore curve context.
   Connected traversal uses shared native edges; Tangent uses native OCCT face
   continuity via the readonly `Face.isTangentAt` API. Exact owner/occurrence,
   native selection gates, Shift removal and deferred stale-context checks remain.

## Native screenshots

These are captures of the installed working application with disposable documents:

- [Appearance task and bottom buttons](appearance-task.png)
- [Selected-face preference color](appearance-selected.png)
- [Preselected-face preference color](appearance-preselected.png)
- [Contextual surface toolbar](surface-control.png)
- [Symmetry task](symmetry-ready.png)
- [Pattern task](pattern-circular.png)
- [Move task](move-components.png)

## Verification

All runs use isolated profiles/documents. The owner's model was not used or saved.
The native build completed successfully; retained `build.log` is the final
incremental target verification, not a full clean-build transcript.

| Run | Scope/result |
| --- | --- |
| s1 | Initial integration: 45 cases, 4 failures and 4 errors from outdated retained-selection/default expectations; corrected fixtures and implementation followed. |
| s2 | Focused integration: 41/41 pass. |
| s3 | Broader integration: 93 cases, 8 failures and 1 error. Fixed unimported-assembly routing and restored test preference isolation; compared legacy failures against baseline. |
| i1 | Unchanged installed baseline: 13 cases, reproducing the same six legacy isolation failures; curve viewport case passes. |
| s4 | Final focused source integration: 53/53 pass, including actual viewport face click and Shift removal. |
| s5 | Final default-assembly/source-routing check: 2/2 pass. |
| i2 | Launch failed before tests due to incorrect installed native-module directory; corrected as described below. |
| i3 | Installed broad verification: 89/91 pass. Two synthetic viewport interactions missed Edge1/V_Axis; other checks pass. |
| i4 | Fresh installed gesture rerun: 3/3 pass, including both i3 cases and the surface gesture. |

All 91 distinct installed checks were verified across i3/i4. This is not a claim
of a single uninterrupted 91/91 run. Logs and JSON results are retained beside
this document, including intermediate failures.

The six pre-existing `TestUnusedModels` failures reproduce on the unchanged app:
`test_editing_unused_keeps_assembly_root_and_restores_display`,
`test_external_context_is_per_view_and_rechecks_removed_import`,
`test_external_isolation_close_source_and_panel_cleanup`,
`test_external_unused_selection_edit_undo_save`,
`test_isolation_is_per_view_and_panel_close_cleans_up`, and
`test_unused_filters_do_not_leak_into_placed_view`.
They cover direct ObjectGroup/SelectionContext/source-selection/ray assertions;
the whole legacy suite is not reported as clean.

## Installation and preservation

The final manifest records 25 Python/test files and six native binaries:
`bin/FreeCADGui.dll`, and `lib/Part.pyd`, `lib/PartGui.pyd`, `lib/Sketcher.pyd`,
`lib/SketcherGui.pyd`, `lib/PartDesignGui.pyd`.

The initial installer used the build tree's `Mod/...` paths for the five `.pyd`
files. Those shadowed the installed `lib` modules and caused an isolated launch
failure. Only those newly created files were removed after exact path/hash checks;
the installer now maps `.pyd` files to `lib`. The initial and corrected manifests
are retained. Installed launches and all i3/i4 checks use the corrected layout.

`verification.json` confirms all 31 installed hashes match source/build,
Python AST checks pass, shadow modules are absent, and owner profile CFG files
and the desktop shortcut retain their original hashes. Rollback binaries remain at
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/pending27/rollback`.
The manifest records source/target paths and before/after hashes.

## Approved preview references

Approval was supplied in chat; no companion approval state was changed on the
owner's behalf. Screenshots above are the direct delivery, not dashboard links.

| Group | Session | Fingerprint |
| --- | --- | --- |
| Edit modes | 5826d20f99b1 | 03fda706509a442b0c616aa334b6b8f154c2275a62a119f7f8e1a1eccd98bc68 |
| Single-part assembly | d0576002b876 | 933887abfd78249de12709583618948322801c23e486f0a4a9b338aadf282f0c |
| Symmetry | c495f9aec28c | beae1b3da1fb8ad6712e70b1a0f81969a3b43988e097c4c630b81aedc7bb242c |
| Tabs | 4d4c136c60b0 | 620e51c63f9653c8b18d7b168802330fe1018b686b1bfda6dc38607a5639432f |
| Apply/reset/highlights | df6b40e0dcba | 0e6d78f641f4c66a0fac04965f0bcf36370ff037ff71d638040151e3b9d50dbe |
| Surface selection | 5591e6b566f9 | 04f8b4f9dd1c2e70090d705849370d40876dcebc509be142a8a033c938a4f1f4 |
