# Active assembly selector — November 24, 2026

The selected part now heads Assembly, replacing the filename row. Choose it using
the Assembly button or **Parts > right-click > Make active assembly**. The chooser
lists all domestic parts directly, alongside total nested component-instance
counts. Other loaded Plus files are collapsed groups containing their parts and
counts. Hidden instances count; Reference and Excluded branches do not. Repeated
instances count individually. Cancel leaves the current choice unchanged.

Double-click Edit still activates the component and History independently of the
assembly root. Editing unused parts no longer adds a temporary Assembly row.
The far-left active component heading and right-click Rename in History are retained.

## Approval and preview

The owner approved the revised selector with **"Approved"** in chat after requesting
flat current-file parts with counts and expandable, initially collapsed loaded-file
groups. [Approved native preview](approved-preview.png), [baseline](baseline.png).

Product baseline: `ce2fc9b305015d41da901096b447cde397a95373`.
Clean preview snapshot: `fcfd5cfde0e68a6517e9f41219ad76d007b65a43`.
Companion session: `b6174e6103b6`; allowlist: `panel.py`.
Approved fingerprint:
`d65adda6e31456441d6f4ba1a017cd276fbd33135aead85e7fc89d7c1744c9c0`.
Reinspection found valid fingerprints and no scope violations. Chat approval is
authoritative; tool approval state was not altered. Preview data was simulated;
the installed screenshots and tests below use actual native document graphs.

## Implementation and bounds

`freecad_plus.assembly` owns loaded-catalog discovery, memoized recursive counts
and the last explicit choice in local workspace preferences. Panel state holds one
assembly per native view, separately from Edit. Initial state recalls a valid
choice or uses the initially edited part. Closed/deleted roots clear safely.
No document schema, native file container, object IDs, placement or membership is
rewritten when selecting an assembly. The choice does not create an Undo entry.

Placed roots retain native routes; unplaced roots use validated definition-relative
routes. Their children edit through explicit detached isolation so another placed
instance cannot be mistaken for the chosen route. The same applies to Open in new
window. Parts editing still searches the complete file graph. Copy/Paste into an
unused selected assembly uses the existing transactional placement service.

The selector includes loaded, unimported Plus catalogs without implicitly importing
or placing them. Editing such a part activates its source file tab. Native viewport
display continues to follow existing Edit/isolation rules: assembly selection is
tree/navigation state. The remembered choice is a local workspace preference,
not a portable default embedded in the part file. Sorting/count ranking is not added.

## Native checks and known baseline failures

- [Final source run](source-tests.txt): 13/13 pass (nine assembly cases and four
  native New File/New Part cases).
- [Installed affected suite](installed-tests.txt): **68/75 pass**, seven failures,
  no errors. Assembly selection/counts, loaded-file groups, Cancel, stale guards,
  clipboard/Undo, detached child editing/windows, per-view independence, renaming,
  History eyes/order and component creation all pass.
- [Fresh process](reopen.json): remembered choice, selected-part root, native object
  IDs and geometry volume survive saved reopening with the isolated profile.
- [Existing shortcut](shortcut-tests.txt): 14/14 assembly, History rename and native
  creation checks pass through the actual installed launcher.
- [Install manifest](install-manifest.json): source/payload SHA-256 matches; prior
  Python files retained in rollback copies. CMake registers the new module/test.

The [prior installed baseline](baseline-tests.txt) reproduces all seven remaining
failure assertions: two expect cleared `SelectionContext`, two expect the older
scene-graph layout/restoration, two concern unused external picking/display rays,
and one expects closing the managed panel to destroy isolation. The renamed
`test_editing_unused_keeps_assembly_root_and_restores_display` maps to the baseline
`test_temporary_row_is_not_an_instance_and_restores_display`; their failing
scene-restoration assertion is identical. These are recorded unresolved, not
skipped or counted as passing.

Baseline also had an obsolete exact-History-row expectation, corrected to compare
feature rows. Component window tests now compare camera pose/scale while allowing
Coin's automatic near/far clipping updates; the [baseline comparison](baseline-window.json)
passes with that correction. An intermediate combined test run exposed a leftover
test window; the new detached-window test now explicitly closes its window.
The final installed window/pose check passes. The earlier broad source log is
retained as [diagnostic evidence](source-broad-tests.txt), not final acceptance.

Actual installed UI: [Assembly](installed-assembly.png),
[Parts context menu](installed-parts-menu.png),
[collapsed selector](installed-selector-collapsed.png),
[expanded selector](installed-selector-expanded.png),
[reopened assembly](reopened-assembly.png).
Visual inspection confirms the approved layout. Native Qt events exercise the
real menus and dialogs; these checks do not claim manual OS mouse testing.

## Delivery

The existing `C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk` retains its target
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/Launch FreeCAD Plus.bat`
and the same working directory. The shortcut is exercised with explicit isolated
configuration arguments; owner documents/profiles and other sessions are untouched.
Restart existing FreeCAD Plus sessions to load the update. No native build was needed.

Bounded validation scripts are retained here. Generated fixtures/profiles used
`validation/active-assembly-20261124` under the current development runtime, as in
recent local tasks. Rollback copies are retained there; disposable test documents
and profiles were removed after archiving these results. Unrelated
`project.previewfirst.json` is not included in the change.
