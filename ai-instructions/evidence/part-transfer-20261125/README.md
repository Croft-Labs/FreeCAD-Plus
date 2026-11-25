# Multi-part insertion and editable part export — November 25, 2026

The owner renewed the earlier cancelled request: “is there a workflow for adding a
set of parts from another file? or exporting a part or parts to another file from
the current file? if not, implement now”. After direct native screenshots for both
dialogs, the owner replied **“approved. implement”**.

The preview-first session was `559f7b2bb8d1`, based on production `9ef2bc87a0`, with
an isolated committed snapshot and exactly three UI files. The approved fingerprint
was `bbf8e628a56009d80e11c8ccc4b676ec35aed9598c83833d3869403d8d739540`.
Inspection confirmed a fresh capture and no scope violations. Chat approval is the
authority; companion approval controls were not modified. The preview actions were
simulated and did not transfer data. The screenshots prefixed `installed-` show the
working application, tested with real native document operations.

## Delivered behavior

- **Add Component > Add existing:** Open file, collapsed loaded-file groups,
  checkboxes and a selected-component count. Register necessary catalogs and place
  the entire batch beneath the edited component in one transaction/Undo. Preserve
  separate active-assembly selection and Add new/New Component behavior.
- **Parts > Export parts to file:** review the selected definitions and choose a
  new `.cadprt`. Native deep copy copies the union of all child graphs, including
  Reference/Excluded children, once per definition. Labels are unique in the output.
  Each explicitly selected root receives one occurrence at its component origin.
- Native bodies, sketches, feature history, expressions, placements, display states,
  shared links, solver-owner links and joint references remain editable and domestic.
  Validate the copied graph and serialized dependency graph before publication.
- A private sibling directory holds intermediate saves/backups. Publish atomically
  without replacing any existing file (including one created concurrently); remove
  intermediates on failure. Close the hidden output document and retain the user's
  current document/Edit context. Sources are never implicitly saved or replaced.
- File > Import `.cadprt` uses catalog-only import. Its empty native command wrapper
  is accepted; a transaction containing changes is rejected. Existing geometry-only
  File > Export remains unchanged.

## Verification

- Source affected suite: **73/73**, followed by a corrected native Import-wrapper
  check **1/1**. The separate geometry-export check passed **7/7**. Malformed archive
  errors and the native lazy transaction wrapper were corrected during development.
- Installed affected suite: **80/80**, including all 19 new transfer cases, 13 Add
  Component cases, external catalogs, catalog import, 30 assembly-constraint cases
  and seven geometry-export cases. Exact case lists are in `installed-tests.txt`.
- Real native UI tests cover opening a closed library, selecting its group, adding
  two components, selecting multiple Parts rows and invoking the actual context-menu
  export, Cancel, stale context, disabled self/ancestor rows and unchanged dropdown.
- Failure injection verifies atomic batch rollback, write-failure cleanup and a file
  created concurrently at the output path. Source graph/Undo/visibility snapshots,
  no-overwrite bytes, loaded-document sets and Edit context are asserted.
- Source and installed **fresh-process reopening pass**: 72 exported objects retain
  their saved IDs/UID, two nested collectors solve, an exported joint can be edited
  and undone, and a saved batch resolves its two external children to one source file.
- **Five existing desktop-shortcut checks pass**. A final screenshot-only test-harness
  adjustment waits for Qt's dynamic button sizing; its installed check passes **1/1**.
  No product behavior changed after the 80-case installed run.
- Final diff whitespace checks pass. No native module rebuild was needed.

## Delivery and preservation

Installed nine Python files into the existing owner payload at
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/app`.
`install-manifest.json` records source/installed SHA-256 hashes and rollback hashes.
All installed hashes were reverified after archiving the evidence. Rollback copies
remain under `validation/part-transfer-20261125/backups` in that same build root.

The existing `C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk` was checked before and
after installation. It still targets `Launch FreeCAD Plus.bat` in the same existing
build root, uses that root as its working directory and has no stored arguments.
Shortcut checks use isolated `-u/-s` profiles; owner files/preferences/processes and
the retained reference app/shortcut were not modified. Restart existing sessions to
load the Python update. Disposable validation files are removed after evidence is
archived; build payload and rollback files are retained.

This implements new-file editable export and linked batch placement for `.cadprt`.
It does not merge into an existing output file or change STEP/geometry export.
Publication uses the configured origin fork and standing commit/push authorization.
The pre-existing untracked `project.previewfirst.json` remains untouched.

## Direct screenshots

- [Approved Add existing](approved-add-existing.png)
- [Approved export](approved-export-parts.png)
- [Installed Add existing](installed-add-existing.png)
- [Installed export](installed-export-parts.png)
- [Installed Parts context menu](installed-parts-menu.png)
