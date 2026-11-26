# Mesh import ownership repair — November 26, 2026

The owner reported that importing a mesh blanked Parts, Assembly and History, and
clarified that an imported mesh belongs in the active component's History.
This repairs intake/validation behind the existing panel; no panel layout, controls,
icons or selection workflow were redesigned.

## Cause and correction

The saved model contained a native Mesh::Feature outside component ownership.
Native mesh readers create document-level objects. Both File > Import and Mesh >
Import Mesh previously left them there. Component validation rejected the orphan;
the panel's existing invalid-document path cleared all three projections. Attaching
the object alone was insufficient: the validator also omitted Mesh::Feature from
its accepted component content.

- Schema-8 components now accept native mesh features as owned history content.
- The module I/O boundary routes Mesh inserts into the explicit active component,
  including nested and externally defined components, through the native reader.
- Mesh Import uses that same boundary. Classic documents retain native import.
- Mesh creation and ownership share one defining-file transaction. Missing Edit,
  live tasks and pending edits are guarded. Reader failures and native cancellation
  roll back partial objects; ordinary Undo/Redo restores ownership with geometry.
- No schema rewrite, mesh-to-solid conversion or automatic orphan reassignment is
  performed. Arbitrary scripted object creation and other mesh modeling commands
  remain outside this file-import correction.

## Verification

- Native baseline reproduced zero rows in all three tabs and the exact error
  `Document contains content outside component ownership`.
- Native MeshGui target build completed successfully. Only MeshGui.pyd from that
  build was installed; its rebuilt core dependencies were not deployed.
- Source and installed focused suites: **26/26 passed** each, including nine mesh
  cases, native File/Mesh import dialogs, child and external ownership, native-body
  independence, cancellation/failed-reader cleanup, pending-edit preservation,
  save/reopen, native Undo/Redo, component-file imports and sequential History.
- Fresh installed process reopened the repaired file, verified all three tabs,
  and imported the original STL into component History: 52,242 vertices and
  104,492 triangles. MeshKernel.bms and both serialized sketch shapes match the
  original archive byte-for-byte. File UID, object IDs and mesh placement survive.
- The original model remains unchanged. A separately named repaired copy was
  delivered beside it. Owner CAD files and screenshots remain local, outside Git.
- Six installed files have matching hashes and rollback copies. Owner CFG hashes
  are unchanged; the existing desktop shortcut still targets the same launcher,
  working directory and icon. The owner's running session was not closed/edited.

The initial broad discovery run also loaded imported test classes: 60 total with
7 failures and 11 errors. The unchanged installed baseline ran the same 52 older
tests and reproduced the identical 18 failing test names. These existing native
editor/isolation test failures were not changed in this repair. One subsequent
focused rerun reused old fixture files and hit an imported-file UID mismatch;
fresh fixture directories produced the final 26/26 results. The final fresh-process
check also waits for normal panel binding before selecting the active assembly.

See [source results](source-tests.txt), [installed results](installed-tests.txt),
[fresh-process checks](fresh-result.json), and [installed hashes](install-manifest.json).
The native build log and rollback files are retained under `validation/mesh26`;
the task harness and archived local results are in the sibling
`mesh-import-validation`. Disposable profiles and test CAD fixtures were removed
after archiving results and delivering the verified repaired model.

## Delivery

Restart FreeCAD Plus before opening the separately delivered repaired copy. The
original invalid file was intentionally not overwritten. No release/package was
published. The unrelated untracked `project.previewfirst.json` is preserved.
The separately previewed Save All button and Hidden line correction remain pending
their own approvals and are not included in this change.
