# FreeCAD Plus: Build validation handoff

## October 9 external destination file roots

7.8.13d2b1 wraps independent Copy to External File destinations, the retained
externalize compatibility service and New Component/new external file destinations
in the validated file container before final save. Each contains one occurrence of
the intended definition, with its placement preserved and no extra Part001. Return
values and source assembly links still refer to component definitions, not the file
container. Destination bootstrap undo is cleared; original-file edits/undo remain
separate. The identity-moving compatibility service is not newly exposed in the UI.

New tests cover independent identity/source retention, placements, destination
save/reopen, retained identity-moving consumers and named external creation without
adding an instance to the host assembly. External-copy UI acceptance now resolves
the copied definition beneath its file container. Add Component workflow unchanged.
Owner DOCX creation/copy requirements updated; pages 68-70 rendered/reviewed, native
numbering preserved, and the affected Make Sub-Link heading kept with its text.
No native build, owner payload or shortcut update.

Validation: the corrected source-overlay run passes 78 of 79 checks (eight file
container, nine workspace, three externalization, 32 hierarchy and 27 core cases).
All destination-specific checks pass. The initial run left the installed navigator
observers alive and additionally lost New File activation; removing those observers
eliminated that overlap. One existing core GUI check still fails reproducibly in a
fresh process: testNavigatorRootIsComponentAndHistoryIsSeparate encounters a native
access violation/break signal when replacing the scene for an isolated component tab
after editing a published result with contextual transparency. Retaining the new
view's original scene did not fix it; restoring the existing context scene also
failed. Both attempted changes were removed. This is not a clean grouped acceptance
or an owner-ready build. The already-recorded Layers close callback diagnostic also
recurs. Generated test/render files are removed after this summary.

Immediate next task: 13f1 repair and regress the isolated-tab/context-scene transition
before resuming older-file migration. New-file and copy destinations are implemented;
Open in new window integration is not accepted as complete.

Next: 13d2b2 migrate existing .cadprt opens and legacy conversions after verifying
saved identities, preserving placements/references and conversion undo semantics.
Definition deletion, complete file-level command/assembly guards and grouped owner
delivery remain outstanding. No existing files are automatically migrated by this step.


## October 9 New File and pinned Part Tree workspace

7.8.13d2a connects native New to new_file_document. It creates the file container,
ordinary Part001 and one occurrence, clears bootstrap undo, and binds the exact
occurrence as the active part in the current tab. Models excludes marked file roots,
including imports. Part Tree shows the document label/FreeCAD icon above Part001;
file renaming changes the document label independently of component names. Removing
the initial occurrence keeps its definition and a valid empty tree; Undo restores it.
Native Delete filters file-root selections before generic deletion.

File Edit displays the global Origin and planes and hides History modeling actions.
The shared active_component resolver rejects a file for modeling, with explicit
allow_file for component-structure commands. Full modeling-command/assembly guard
qualification remains 13e. Internal new_document/initialize callers are unchanged:
existing-file migration, legacy conversion and copy/external destinations remain
13d2b. The Add Component workflow is still deferred.

Validation: 30 native source-overlay checks pass (seven workspace, six migration,
nine prior active-editing and eight display-context cases). The final native Delete
guard passes as an eighth workspace case in a focused follow-up run (31 distinct
checks passed across runs). Native Delete emits its expected definition-protection
message; the source adapter also removes the protected file selection. Native New testing
updates the already-registered Python command implementation because FreeCAD ignores
duplicate registrations; the installed executable/owner payload is not changed.
Part Tree/Models captures reviewed: file icon and pinned label, active green/bold
Part001 and Models occurrence count are correct. Owner DOCX pages 1, 65 and 66
rendered/reviewed; native numbering XML unchanged. No new build or shortcut update.

The grouped run emitted one queued DesignLayers.initialize callback NameError for
an already closed untitled001 document. Functional tests passed; this close-boundary
diagnostic remains for 13f rather than being reported as a clean installed run.
Next task: 13d2b existing-file/legacy migration and copy/external destination wiring.


## October 9 file-container migration foundation

7.8.13d1 adds an opt-in migration service, not automatic UI migration. It wraps the
old root in one native occurrence under a marked identity-frame file container;
old geometry, history, object identities and external links stay intact. The wrapper
copies the previous placement explicitly and uses Full Component representation,
preserving the former root's display scope. Existing add-component creation shares
the same internal occurrence builder without changing its workflow.

Migrated archives require component-file-container-v1 and cross-check the root UUID
against the native FileContainer marker. Older readers refuse the capability;
removing its declaration is rejected. Backend validation rejects multiple/non-root
containers, file-owned geometry/history, moved file frames and container instances.
Normal documents retain their existing schema and behavior until explicitly migrated.

Validation: six new native migration checks plus all 27 core component regressions
pass with ComponentModel/CadDocument source overlays on the October 9 relocation
runtime. Covers exact geometry bounds, identity preservation, external consumer
save/reopen, undo/redo, injected failure rollback, unfinished edits, empty files,
and capability tampering. An additional focused six-case run checks the final
Full Component wrapper default. Initial tests found the missing placement copy;
fixed and geometry bounds rechecked. A reused test-output directory caused expected
no-overwrite fixture failures; final regression run used a fresh directory.

No interface changes or owner DOCX changes in this backend step. No native build,
owner payload or shortcut update. Next: 7.8.13d2 New/Open/legacy and copy-destination
integration, ordinary active Part001, pinned file name/icon and Models filtering.
File Edit guards/origin-only History remain 13e; grouped owner delivery remains 13f.
Add Component workflow stays deferred.


## October 9 context transparency renderer

Roadmap 7.8.13c2 adds a per-window native LinkView scene with transparency-only Coin
material overrides. Each visible item outside the exact edited occurrence/descendants
uses max(authored material transparency, 0.75); colors and document appearance are
untouched. The outermost occurrence material override is honored. Root Edit removes
the context scene, and unused-model entry switches to its existing isolated view.
The original scene is retained with paired native references, and scene changes
preserve camera state. Appearance property notifications schedule refresh.

Native picking is retained by an invisible original-scene branch; temporary display
links are unpickable. This corrected an integration failure where a visually correct
snapshot had no native occurrence pick. The viewport test verifies a ray pick on the
faded second occurrence, placement bounds, restoration and camera values. Coin-level
checks verify transparency-only overrides preserve color; per-face arrays preserve
90 percent transparency alongside the 75 percent floor. Existing editing/unused-model
checks remain included. Broad multi-window/native task qualification remains 13f.

Final validation: 17 checks pass (eight context-display/Coin checks and nine
active-editing checks), zero failures/errors/skips, process exit 0 and empty stderr.
Camera comparison permits 1e-5 serialization normalization, while retaining position,
orientation, clipping and zoom values. Validation is source-overlay GUI evidence
against the October 9 relocation runtime, not installed delivery. Live framebuffer and owner DOCX pages 66-67 reviewed; DOCX
native numbering retained and the following heading kept with its text. No new native
build, owner payload or shortcut change. Next task: 7.8.13d pinned file container,
ordinary automatically activated Part001 occurrence, and existing-file migration.
Add Component workflow remains deferred.


## October 9 context transparency planning prerequisite

7.8.13c1: ComponentNavigator.display_items is now the shared traversal behind
visible_paths and context_display_plan. The plan retains native paths/source objects
and classifies the chosen occurrence plus descendants with floor 0, all other visible
items with floor 0.75. Hidden branches stay excluded, invalid active paths are
rejected rather than silently fading a different branch, and root context has no fade.
No source material, color, geometry or transparency is changed by the planner.

Fourteen native GUI source-overlay tests pass: five new TestComponentContextDisplayPlan
cases plus nine TestComponentActiveEditing regressions; no failures/errors/skips.
The actual viewport fade is NOT implemented yet. LinkView.setMaterial overrides
both diffuse color and transparency (ViewProviderLink.cpp), so applying a single
material would lose per-face colors. Next task is 7.8.13c2: a per-view renderer that
consumes the plan while preserving individual materials, greater transparency,
picking, placements and context restoration. Keep 7.8.13c unchecked until that passes.
This is backend-only work; the existing owner DOCX transparency requirements remain
unchanged. No owner payload, shortcut, or native build update; grouped delivery is 13f.


## October 9 unused-model editing task two

Roadmap 7.8.13b adds a per-window temporary LinkView for unused definitions.
Models Edit keeps the current file tab, appends the qualified (unused model) root,
grays/hides the permanent assembly in that view, and supports its child editing.
Ordinary unused definitions no longer appear as permanent extra assembly roots.
The temporary root cannot be dragged/dropped or used through assembly-occurrence
context actions. Hidden assembly visibility controls are blocked; authored document
visibility is untouched, so save/reopen retains geometry but no temporary occurrence.
External source closure restores the owner view; task return preserves that view.

Validation: nine source-overlay native GUI tests (five earlier placed-edit checks
plus four unused-model workflows), no failures/errors/skips in the final run.
Save/reopen retains edited geometry and zero instances of the unused definition.
The initial runs exposed an unretained native scene on restoration, now fixed by
explicit paired Coin references; test fixture view readiness and numeric tolerance
were also corrected. Native captures reviewed for gray permanent rows and active
unused entry. Owner UI DOCX updated with unchanged native numbering, rendered,
affected pages 66-67 checked. Source checks remain distinct from owner delivery;
no native rebuild or owner payload/shortcut change. Prior master/unused-root GUI
fixtures need reconciliation in the grouped 7.8.13f acceptance pass.

Next task: 7.8.13c per-view transparency of at least 75 percent outside the chosen
active occurrence and descendants, preserving authored appearance and selection
context. File container and geometry guards remain 13d/e; Add Component stays deferred.


## October 9 active editing task one

Roadmap 7.8.13a is implemented in ComponentNavigator and covered by five focused
native GUI checks in TestComponentActiveEditing. Placed Models Edit stays in the
current file tab, remembers a valid last occurrence per tab, falls back to the first
nested occurrence after deletion, and highlights every active-definition row using
TreeActiveColor plus bold text. Both menus offer Open in new window. Add Component
workflow is unchanged. Existing selection behavior remains separate from Edit.

Validation: the first harness incorrectly exercised the installed navigator rather
than the changed source; corrected by explicitly injecting the loaded module into
the test fixture. A subsequent stale-row test error was fixed by resolving each row
after menu-triggered refresh. Final five-case run passes without failures/errors/skips.
This is source-overlay GUI evidence against the verified October 9 relocation
runtime, not a new installed build. Owner payload/shortcut remain unchanged; batch
installation is deferred to 7.8.13f. Native captures of Models and expanded repeated Part Tree rows also show the expected
green active fill and bold names. Owner DOCX updated preserving native numbering,
rendered, affected pages 65-66 visually checked. No claim of complete file-container
or unused-model behavior. Next task: 7.8.13b temporary unused-model editing.


## October 9 native relocation delivered

**Implementation/build:** 7.8.12g/h now have a matching full Release
default/ALL_BUILD in test-builds/freecad_plus_2026-10-06_recovered_workload.
Native source ec104817c69085d94b2676f219f85a4b46c1bbf8; acceptance/source snapshot
c333146dbed7d4b02422caecf9fe068709460040. The build passed on the first run, using the
existing pinned LibPack 26.3.0-v3.5.3 and full configured workbench set (FEM off).
Base::Writer and all dependent runtime modules were rebuilt consistently.
Dependency deprecation warnings remain; no build failure or install-script use.
Runtime version is 27.1.0 dev R49468.

**Behavior:** component saves refuse paths owned by another open document before
writing. Save As/Copy external native links are serialized relative to the final
archive destination, matching the manifest without mutating live bindings.
Both formerly failing relocation cases now pass with evaluated-reference geometry,
nested imports and a directory containing spaces and a non-English character.

**Installed acceptance:** 93 final accepted checks, no source overlays: 32 hierarchy,
27 core, three each file recovery/save routing/undo routing/externalization, 20
legacy integration/extrusion, one cold reopen and one actual saved-shortcut reopen.
The two focused relocation checks also passed before the broader batch and are
not added again to the 93 total. The initial externalization suite had two stale
UI expectations for identity-moving externalization. Its corrected three-case run
verifies independent-copy identities/geometry, original placements/edit context,
unfinished-edit refusal, overwrite refusal and cancellation; internal legacy-service
coverage remains. Only those superseded failures are excluded from final acceptance.
All other broader-batch suites passed unchanged. Accepted suites have no failures,
errors, skips or unexpected GUI diagnostics; every process exited zero. Loaded
module/source hashes match. General repeated-session qualification is not implied.

**Delivery:** a fresh native payload was staged from the complete build directories:
test-builds/freecad_plus_2026-10-09_hierarchy_relocation_payload.
The full inventory contains 15,625 files; all
1564 native DLL/PYD/EXE files match the rebuilt
runtime byte-for-byte. Native and application identities are separate in
release-info.json/payload-manifest.json. The unchanged owner launcher SHA256 is
05c3a107c9ce1e0e370367a4e84e2ac8afe7a9e8e92cdb7543bc3db9a2547518.
The existing FreeCADPlus.exe - Shortcut.lnk targets this payload; its saved target
and working directory were reopened and verified, and an actual launch passed.
The preceding hierarchy_import_repair_payload is retained as fallback.
No new UI controls/defaults; the synchronized owner UI DOCX remains applicable.

**Limits/publication:** earlier grouped-sketch inactivity timeouts remain unresolved
(16.6c); they were not rerun in this relocation batch. FEM remains unavailable.
No release or upstream publication. Acceptance milestone
c333146dbed7d4b02422caecf9fe068709460040 and delivery evidence
48f15e0109e93d460d3ee33c6504c3c7fe996c7d were pushed to origin/main and remote
hashes verified. All six task validation directories were deleted after recording
results. The superseded file_hierarchy_payload and hierarchy_recovery_payload were
removed after re-verifying the saved shortcut. Current hierarchy_relocation_payload,
preceding hierarchy_import_repair_payload fallback, native build and dependencies
are retained. No task FreeCAD/FreeCADPlus processes remained at cleanup.

## October 9 save destination protection and native relocation (build pending)

**Implementation:** 7.8.12g adds CadDocument manifest preflight rejecting a final
output path owned by another open document. It runs before native output is opened.
Save As failure restores the prior location/label; Save Copy must not overwrite
direct or nested imported files. Backend save validation only; no new UI controls,
defaults or schema, and the synchronized owner UI DOCX remains applicable.

**New native gap / source fix:** relocation to another directory exposed correct
manifest dependencies but stale native XLink paths (Hardware.cadprt instead of
../Hardware.cadprt). Both Save As and Save Copy reopen with missing links in the
current native runtime. 7.8.12h source adds a final-document destination to
Base::Writer, sets it from Document::saveToFile's canonical destination, and uses
it in PropertyXLink::Save to recalculate external paths. Serialization does not
mutate live links. Export behavior and writers without document context retain
their existing paths. This native change is implemented but not compiled or
runtime-validated; it must not be described as delivered.

**Validation:** two overwrite regressions fail before the Python guard and pass
afterward with file bytes and document location/label preserved. Thirty selected
hierarchy cases pass in the final source-overlay run, no failures/errors/skips or
unexpected GUI diagnostics, exit zero. The preceding run passes all 27 core cases
but has the newly exposed relocation error. A focused baseline run confirms both
Save As and Save Copy relocation fail on the unchanged native runtime. Those two
cases are explicitly excluded from the passing 30-case run, not silently skipped
or treated as passing. Source diff checks pass. Runtime base:
test-builds/freecad_plus_2026-10-09_hierarchy_import_repair_payload,
native 40f1698230ccbbac5b4f44fc0ba8124a0ee08c60.

**Build/delivery handoff:** follow DEVELOPMENT_GUIDE build batching. No new native
build, owner payload or shortcut change this round. Writer's class layout changed:
perform a consistent full AllTargets native rebuild before packaging; never drop
one rebuilt DLL into the old payload. Run both relocation cases and unfiltered
hierarchy/core checks against that build, then cold reopen, full payload inventory
and actual saved-shortcut delivery. Include CadDocument.py in the same batch.
Keep the existing verified owner payload until those gates pass.

**Publication/cleanup:** source milestone 02d919e5d294b736d82437083a08d6897597aa7f
was pushed to origin/main and the remote hash verified, with native build/runtime
gates explicitly pending. The four task validation directories were removed after
recording their results. Owner/development payloads and shortcut are unchanged.

## October 9 atomic imported-file recovery batch delivered

**Implementation:** source 1a4f4692f9bb4d8132f424e31ee45b58ffd0f586 adds roadmap 7.8.12f.
Imported-file recovery preflights all matching definitions, restores import,
placement and evaluated-reference bindings in one owning-document transaction,
then refreshes affected components. Single-component recovery shares the same
planning/binding helpers. One Undo reverses the whole repair; a refresh failure
rolls back all definitions. Missing geometry remains separately repairable.
This batch also delivers the pending 7.8.12e combined import-identity guard.
No schema, controls or defaults change; the owner UI DOCX remains applicable.

**Validation:** both new native regressions failed before the fix: one Undo and
a later refresh failure left earlier repairs applied. Source-overlay acceptance
then passed all 28 hierarchy plus 27 core cases. One older recovery-suite
assertion still used the former Save to External File caption; it now checks
the approved Copy to External File action without changing the application UI.
Final installed acceptance passes all 58 cases (28 hierarchy, 27 core, three
file-recovery), plus one fresh-process cold hierarchy reopen and one through
the actual saved desktop shortcut: 60 installed checks total. No failures,
errors, skips, source overlays or unexpected GUI diagnostics; all exit zero.
Loaded module hashes match source. Repair Undo/Redo, full failure rollback,
identities, placements, reference geometry and save/reopen are covered.

**Build/delivery:** compatible Python-only owner payload:
test-builds/freecad_plus_2026-10-09_hierarchy_import_repair_payload.
Native source remains 40f1698230ccbbac5b4f44fc0ba8124a0ee08c60. No native or
launcher recompilation. Complete SHA256 inventory verifies 15,583 files;
only Mod/Part/ComponentModel.py and release-info.json differ from the verified
hierarchy_recovery_payload baseline. The regenerated payload-manifest.json
records separate application/native identities. Launcher SHA256 remains
05c3a107c9ce1e0e370367a4e84e2ac8afe7a9e8e92cdb7543bc3db9a2547518.
The existing desktop FreeCADPlus.exe - Shortcut.lnk targets this payload;
its saved target/working directory and actual launch are verified. The preceding
owner payload is retained for rollback.

**Limits:** broader native baseline qualification was not repeated for this
single-module update. The earlier grouped-sketch inactivity timeouts remain
unconfirmed (16.6c); this is not exhaustive repeated-session qualification.
No release or upstream publication.

**Publication/cleanup:** implementation 1a4f4692f9bb4d8132f424e31ee45b58ffd0f586
and delivery evidence 8203b3e4c3faf303ff28e075a784f69be2ef7f88 were pushed
to origin/main with remote hashes verified. All six task validation directories
were deleted after recording these results. No FreeCAD/FreeCADPlus validation
processes remain. Useful owner/development payloads and dependencies are retained.

## October 9 import-graph identity preflight

**Implementation:** roadmap 7.8.12e reuses the identity maps from file-graph
validation to check the combined destination/incoming graphs before an import
transaction. Distinct loaded files claiming the same document identity now refuse
even when the collision is below different import branches. Reusing one loaded
file through a diamond stays valid. The shared guard also serves external
placement, copy preflight and recovery. No schema, controls or defaults change;
the synchronized owner UI DOCX remains applicable.

**Validation:** the new native Save Copy fixture reproduced acceptance of a
conflicting direct import and a resulting invalid destination before the fix.
The final fixture isolates direct and nested incoming aliases in separate
destinations and checks refusal, unchanged objects/imports and no pending
transaction. All 26 hierarchy and 27 core cases pass (53 total), no failures,
errors, skips or unexpected GUI diagnostics, exit zero. This is source-overlay
validation using the verified hierarchy_recovery_payload native runtime;
loaded source hashes match.

**Build/delivery:** no native rebuild or owner payload was created for this
isolated backend change, following DEVELOPMENT_GUIDE build batching. The current
desktop shortcut continues to target hierarchy_recovery_payload. At the next
related batch, synchronize Mod/Part/ComponentModel.py, verify installed hierarchy
checks and hashes, regenerate the inventory and repeat saved-shortcut delivery.
Do not describe this patch as already installed in the owner payload.

**Publication/cleanup:** milestone 7b44c41accd3366c941649c9273438bbb92ef10a
was pushed to origin/main and the remote hash verified. Both task validation
directories were deleted after recording the results. Owner/development payloads
and their inventories remain unchanged.

## October 9 hierarchy recovery batch delivered

**Implementation:** application source 7cc78638bc28a43576368e0d3fa23aaf8cf06103 adds roadmap 7.8.12d
native-archive/manifest consistency checks before restoration: record shapes,
unique definition/occurrence identifiers, exact occurrence membership, saved
definition identity and external-file designation. This batch also delivers
7.8.12c failed-open rollback. Schema/version and valid-file behavior are unchanged.
This is backend persistence work; the synchronized owner UI DOCX remains applicable.

**Validation:** the two corruption tests first reproduced seven failures and one
incidental TypeError. Corrected source-overlay acceptance passed 25 hierarchy plus
27 core cases. Final installed acceptance (including incorrect external designation
and definition-name corruption) passed all 52 cases with no source overlays,
failures, errors, skips or unexpected GUI diagnostics. A fresh-process hierarchy
reopen passed once directly and once through the actual saved desktop shortcut:
54 installed checks total, all processes exit zero. Loaded module/source hashes
match. Nested unused imports, shared external edits, independent domestic copies,
failed-open cleanup and recoverable missing references are covered.

**Build/delivery:** compatible Python-only update in
test-builds/freecad_plus_2026-10-09_hierarchy_recovery_payload, based on the
verified October 9 file_hierarchy_payload. Native source remains
40f1698230ccbbac5b4f44fc0ba8124a0ee08c60; no native compilation or launcher
compilation was repeated. Complete SHA256 comparison verifies 15,583 payload
files; only Mod/Part/CadDocument.py and release-info.json differ from the baseline.
The regenerated payload-manifest.json records the inventory and separate native
and application source identities. Launcher SHA256 remains
05c3a107c9ce1e0e370367a4e84e2ac8afe7a9e8e92cdb7543bc3db9a2547518.
The existing desktop FreeCADPlus.exe - Shortcut.lnk targets this payload; saved
target/working directory and an actual shortcut launch are verified. The previous
payload is retained for rollback.

**Limits:** broader native baseline acceptance was not rerun for this single-module
update. The prior grouped-sketch inactivity timeouts remain unconfirmed; this
batch does not close roadmap 16.6c or exhaustive repeated-session qualification.
No UI/default changes, releases or upstream publication.

**Publication/cleanup:** implementation 7cc78638bc28a43576368e0d3fa23aaf8cf06103
and acceptance c05ac9b81c6a7159398a59820c1b70ad907a666f were pushed to
origin/main, with remote hashes verified. All six hierarchy-manifest/recovery task
validation directories were removed after recording results. No validation
FreeCAD/FreeCADPlus processes remain. Useful owner/development builds and the prior
owner payload are retained.

## October 9 failed nested-open rollback

Roadmap 7.8.12c adds an outer restore boundary in CadDocument.open. Recursive/native
loads are included in failure cleanup; documents open before the call and their
unsaved work remain, and the previous active document is restored. The native
serialization, schema, identity checks and recoverable missing-file behavior are
unchanged. This is backend failure cleanup; no UI controls/defaults or owner DOCX
requirements changed.

Before the fix, the nested identity-mismatch regression left Hardware and/or its
Coatings dependency open. The post-root failure fixture initially compared differently
formatted paths, so its injection did not trigger; the corrected test normalizes
paths and verifies root/dependency cleanup. After the fix, 23 hierarchy plus 27 core
cases pass, no failures/errors/skips or unexpected GUI diagnostics, exit zero.
Validation uses explicit source overlays on the verified October 9 native payload.
A focused final rerun passes both rollback cases after preserving source line endings,
with matching loaded module hashes and exit zero. Milestone
`3b8851a8407e8cf82e0163a401145cc9c97879e9` was pushed to origin/main and its remote
hash verified. The three task validation directories were deleted after recording
these results. No owner payload or shortcut was changed.

Delivery remains batched per DEVELOPMENT_GUIDE: the current desktop shortcut and
15,583-file owner payload still contain the prior CadDocument.py. No new native
build or owner payload was created for this isolated backend change. At the next
related batch, synchronize this compatible Python module, verify installed hashes
and failed-open cases, update the payload inventory, and repeat shortcut delivery.

## October 9 hierarchy native build and owner delivery

Implementation remains native/application source
`40f1698230ccbbac5b4f44fc0ba8124a0ee08c60`, incorporating hierarchy milestone
`be18640254d44c9a99ca789dd6140457e2bcc580`. This continuation changes acceptance
tests and documentation only. The previously synchronized and rendered 92-page
owner UI DOCX remains applicable; no new UI requirement or application edit.

**Build:** matching Windows Release AllTargets passed in
`test-builds/freecad_plus_2026-10-06_recovered_workload`, with pinned LibPack
26.3.0-v3.5.3 and Coin 50e37f04e7027661ea2318d0425b7836ac819568. The first full
pass failed when Assembly's CMake autogen process exited -1073741819; an incremental
AllTargets retry passed without source changes. Generated install scripts contain
absolute Program Files/FreeCAD paths and were not run. Runtime directories were
copied into the independent owner payload below. FEM remains disabled.

**Installed acceptance:** 250 final cases pass, no failures/errors/skips or
unexpected captured GUI diagnostics, no source overlays, and successful launcher
exits. Loaded application module hashes match the checkout. Breakdown:

- 71 hierarchy/Models/core/create/Save/Undo (21/14/27/3/3/3).
- One fresh-process hierarchy test after relocating the related files together:
  nested unused imports, stable document/definition/occurrence identities, retained
  placement, external edits shared by two assemblies, and a same-name domestic
  copy that remains independent through another saved source edit and reopen.
- 12 installed document/preview cases (6/6), including native camera/view closing,
  standard New/Open/Save As/Save Copy, legacy conversion and nested Models traversal.
- Eight Pattern cases (three task-dialog and five suppression/persistence), plus
  one native removeSplitter geometry case.
- 123 CAM cases: 23 workplane-frame, 82 invalid-input/recovery and 18 surface-avoidance.
- All 33 sketch workflow cases in independent fresh processes.
- One additional cold hierarchy case launched through the actual saved desktop shortcut.

Acceptance test repairs remove an accidental source-navigator overlay, update the
Models traversal and its QtWidgets import, and replace obsolete datum-plane test
controls with the adopted numeric controls. PlaneTask cleanup prevents a failing
test from leaving a selection observer attached. This fixes the initial cascading
selection failures. Subsequent grouped sketch runs still reached the inactivity
guard at differing cases. Their cause is unconfirmed; individual cases all pass.
Do not treat the incomplete grouped runs as acceptance or claim exhaustive repeated
GUI-session stability. Physical owner feedback remains separate.

**Owner delivery:**
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_plus_2026-10-09_file_hierarchy_payload/FreeCADPlus.exe`.
The existing desktop `FreeCADPlus.exe - Shortcut.lnk` was retargeted, saved and
reopened to verify target and working directory. An actual shortcut launch used
that payload, passed the relocated cold hierarchy case and exited zero. No task
native process remains. The accepted October 6 payload is retained as rollback.
The launcher is reused, not recompiled: SHA256
`05c3a107c9ce1e0e370367a4e84e2ac8afe7a9e8e92cdb7543bc3db9a2547518`.
The payload contains release-info.json with per-suite hashes/results and a complete
15,583-file SHA256 payload-manifest.json. This is a local owner build, not a release.
General expression copying and unreviewed consumer/path remapping still refuse.

**Publication and cleanup:** acceptance milestone
`1b31a9ae78501469029703a9e59757d047e88d42` was pushed to origin/main and the remote
branch hash verified. All 47 task validation directories were removed after the
canonical summary was committed. No task native process remains. The useful native
build tree, dependencies, new owner payload and previous rollback payload remain.
This documentation closeout is separate from application source and the native build.

## October 9 domestic/external file hierarchy

Implementation commit `be18640254d44c9a99ca789dd6140457e2bcc580` was pushed to
origin/main and the remote branch hash verified. No release or owner build was
published. All 20 task validation directories were removed after recording the
results below; no task native process remains.

Roadmap 7.8.12 implements the owner-approved hierarchy in ComponentModel,
CadDocument and ComponentNavigator. File imports persist without placements,
Models lists domestic definitions before recursively grouped imported files, and
external labels identify their defining file. New Component supports domestic,
new external and existing external storage. Active defining-file inventory controls
insertion. Component/file cycles refuse before mutation. Missing unused imports
can be repaired by original file identity.

Independent copies regenerate the domestic definition closure's identities and
retain already-external children as explicit shared imports. The domestic-copy
prompt defaults to no placement replacement; Cancel retains both the new copy and
original links. Selected replacement retains placement and occurrence identity.
The normal UI no longer invokes identity-moving externalization. Expressions,
outside-owned copy inputs and unreviewed replacement consumers/path overrides are
explicitly refused. Cross-file creation is not a distributed undo transaction.

The owner UI DOCX was read, surgically updated, rendered to 92 pages and visually
reviewed at changed sections and reflowed pages. ZIP comparison confirms only
word/document.xml changed: styles, relationships and native numbering are retained.
Canonical component contract, ADR 003, UI specification and programming summary are
synchronized. Tests/ComponentFileHierarchy.md records the validation boundary.

Validation uses explicit source Python overlays on the October 6 native engine,
revision 8746c1076071a7b9decff07577b6a163a0f76ee9, from the existing
legacy_integration_payload. This is not rebuilt October 7 C++ acceptance. No new
owner payload or shortcut delivery is claimed. Batch the matching native build
and installed/shortcut checks with roadmap 16.6b and 7.8.12b; preserve the current
owner payload until that delivery passes.

Earlier trial runs exposed fixture encoding/import selection and stale flat-tree
expectations. Mixed UI runs also retained registered commands bound to the installed
navigator namespace; the source-overlay fixture now retires the installed observer
and reloads that namespace in place. The old runner also timed out idle launchers
while native child tests were still progressing; it now watches log timestamps and
cleans up its own matching child on timeout. A real Origin Planes regression from
the file-header key guard was corrected to retain extended row keys.
Failed/timed-out trials are not acceptance.

Final grouped run hierarchy-regression-18 passes all 64 cases: 20 hierarchy,
three Add Component command, 14 Models pane and 27 core component document checks.
Zero failures/errors/skips, zero unexpected GUI diagnostics, launcher exit zero.
The source-overlay loader verifies the changed core module hashes; the runtime
report confirms the source navigator and model. Seven changed Python modules pass
AST syntax checks, the PowerShell runner parses, and git diff --check passes.
The Models capture confirms domestic-first inventory with Hardware and nested
Coatings groups. Raw task validation files are removed after recording these results.

## October 7 upstream integration handoff

Current source incorporates upstream `e326ee2f07df04d4293035d65a98c96c3eb23380`
from clean fork `d49cab5745`, retaining all 126 upstream history commits.
The [canonical compatibility audit](DEVELOPMENT_ROADMAP.md#october-7-upstream-integration)
records 105 automatic and seven adapted non-merge commits, the 13 conflict
files, preserved Plus behavior and excluded unsafe fallback hunks.
Rollback branch: `codex/pre-upstream-2026-10-07`. No push was performed.

All 126 distinct source-overlay CAM regressions have passing evidence after
two fixture corrections; 108 changed Python files pass syntax checks. This
uses the existing native engine and is not rebuilt C++/Coin validation. The
owner Word requirements are synchronized and revised pages visually checked.

Next action is roadmap 16.6b: batch one matching native rebuild, then validate
changed GUI task/document lifetimes, Sketcher edit/selection, Part refinement,
pattern suppression with Update View off, external-link reopen, native CAM
parameter/arc APIs, TechDraw and Coin rendering. Preserve the October 6 owner
payload and saved shortcut until a new payload passes delivery gates. The
current executable still uses the previously accepted native sources.

## Final owner-requested legacy import/conversion audit

Entry main was clean at e4d8086c9040aae65908f8e23567c9bbe7d771a0.
All 135 migration-family cases have passing native installed results: 132 unaffected
cases in the broad run, then three corrected shared Pocket/Revolve/Loft GUI checks.
Six archived files additionally pass conversion and cadprt save/reopen: Crank,
EngineBlock, ModelFromV021, PadTest, PartDesignExample and PocketTest. Across those
files, 123 original native object identities, 89 evaluated physical shapes and 28
datum global frames are checked. Names/types/native IDs/labels survive conversion;
persisted ObjectIds survive restore. Original and copied FCStd hashes are unchanged.
Physical checks include topology, volume/area/length, exact geometry-derived bounds,
bidirectional solid differences and sampled curve distances in both directions.
These are native recomputed baselines, not certification of every original cache.

Initial broad run executed 141 cases and exited zero but had 29 archived subtest
failures plus three fixture errors; it is not whole-run acceptance. Three errors
used a nonexistent FreeCAD path API in new test assertions. Archive failures used
triangulation-dependent cached bounds or infinite datum display shapes. Source
TopoShapePyImp.cpp confirms optimalBoundingBox(False, False) uses geometry-derived
AddOptimal bounds; datum frames are checked separately. Corrected nine-case run
passes with zero failures/errors/skips and 45 application module paths/hashes inside
the delivered payload matching source. A separate fresh native process passes nine
restore cases (six archives plus mixed, relocated external and explicit recovery),
with 29 verified installed application modules, zero failures/errors/skips. Both
launcher/native exits are zero. Test application source overlays are disabled.
An additional one-case installed PadTest run passes the new explicit invalid-source
repair-report assertion, with 29 verified installed modules and native exit zero.

PadTest already has Invalid Pad002 and a touched Body before conversion; its
available evaluated geometry survives, and the conversion report explicitly asks
for repair/recompute. This is preservation of a broken source, not successful repair
or freshness certification. Other touched DesignLayers entries are recorded in the
raw audit while it exists. All compared baseline physical shapes are geometrically
valid. Standalone native retention and unsupported/custom histories remain bounded
compatibility paths; conversion does not physically flatten every native feature.
FEM remains unavailable (BUILD_FEM=OFF), and exhaustive custom workbench/toolpath/
drawing-topology/physical-owner qualification remains open as recorded below.

No production migration source or native application binaries changed. Reuse the
existing legacy_integration_payload and its previous complete inventory. Launcher
SHA256 remains 05c3a107c9ce1e0e370367a4e84e2ac8afe7a9e8e92cdb7543bc3db9a2547518.
Existing desktop shortcut target and working directory were reopened/verified,
with empty arguments, against that useful payload. UI/UX did not change; owner DOCX
is unchanged at SHA256 7935a0d2ab3a2c144505896983d799b2c4b327a3d535014b7ec41c7cfe9b557f.
Regression fixtures/contracts are tracked in tests/TestLegacyArchivedFiles.py and
tests/LegacyIntegration.md. AST checks and git diff --check pass. Cleanup removed
132 raw validation files, 732 generated payload bytecode files (preserving the
manifest inventory) and 16 source/test bytecode files. validation/legacy-final-audit
is absent; no audit FreeCAD/FreeCADPlus process remains. Payload manifest SHA256 is
unchanged at b10af57ceab8681c0e64d096a0ef5c3d453d869417b1ee3d09ecee9f31355b0d.
Useful builds, source archives, owner settings/document and desktop link remain.
Next step: no migration implementation is automatically queued. Future owner-file
qualification or a FEM-enabled native environment requires its explicit scope.
Final reporting must retain these boundaries rather than universal compatibility.

## Legacy migration task twelve — grouped integration and owner delivery complete

Owner authorized task twelve. Entry main was clean at 75cbeb9954. Bounded whole-file
acceptance combines mapped Sketch/Pad and retained Fillet/Linear Pattern histories,
nested/shared placements and independent siblings, external definitions/relocation,
source protection, actual GUI Open/History events, Draft/CAM/TechDraw consumers and
explicit evaluated dumb recovery. Original names/types/IDs/UUIDs, native owners,
geometry, formulas and FCStd bytes survive the tested paths. Native editable
retention is not physical flattening or a universal legacy conversion guarantee.
Technical contract: tests/LegacyIntegration.md.

Grouped installed run passes 37 checks: whole-file 6, finishing 13, structure 12,
shared previews 6. All 47 recorded application module paths/hashes match source and
reside inside the payload, without source overlays. Fresh-process startup/restore
passes four checks with 29 verified installed modules. Both launcher/native process
exits zero. Actual saved desktop shortcut passes 17 checks: startup 1, cold restore
3, finishing 13, with 32 verified installed modules and observed DPR 2.25 (requested
QT_SCALE_FACTOR=1.5 on the host's scaling). All failures/errors/skips zero. Native
26.3.0devR49296, revision 8746c1076071a7b9decff07577b6a163a0f76ee9. Saved-link process
7040 is no longer running; its exit status was not separately captured. The managed
launcher forwards native exit status, verified in the grouped and cold launches.

The initial isolated Open attempt was interrupted; diagnostic fixture sets the
correct directory and bounds unexpected dialogs. First completed six-case attempt
had one fixture error: native external links require the parent document to be saved
first. Corrected saved-parent fixture passes, protecting both originals. Failed
attempts are not acceptance. No production migration source changed in task twelve;
tests and delivery tooling qualified the earlier adapters. No owner process or
duplicate worker was stopped/created. Native warnings include inherited stylesheet,
hasher/scope, transient null-tool/no-base and deliberately missing-source diagnostics;
this is not warning-free editing or generated CAM toolpath qualification.

Useful grouped payload:
C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_plus_2026-10-06_legacy_integration_payload
Compatible Python modules are synchronized onto the verified palette payload;
application native binaries are reused unchanged. tools/FreeCADPlusLauncher.cs was
compiled with the fork icon and forwards exact quoted arguments. Actual runtime
imports prove installed modules, rather than source overlays. The exact desktop
FreeCADPlus.exe - Shortcut.lnk targets this payload's FreeCADPlus.exe, working
directory is the payload root, and original shortcut arguments were restored and
reopened/verified. Owner settings and unrelated shortcuts remain intact.

UI-only DOCX rendered 91 pages: pages 1–90 pixel-identical, changed page 91 inspected;
other ZIP entries/native automatic numbering unchanged. SHA256:
7935a0d2ab3a2c144505896983d799b2c4b327a3d535014b7ec41c7cfe9b557f.
New tests pass AST checks; launcher compilation and git diff --check pass.

Native FEM probe is unavailable and BUILD_FEM=OFF in the configured native tree.
FEM constraint/mesh/solver acceptance remains a separate explicit unavailable gate.
Custom Path/Point editors, exhaustive mixed-family permutations, drawing topology/
dimensions through arbitrary changes, generated toolpaths and physical owner
feedback remain wider qualification work. No fake FEM substitute or skipped test
is claimed as acceptance. The approved twelve-task sequence stops after this bounded
integration/owner delivery; do not expand deferred feature families automatically.

Source milestone 309ba5bcf8016b663d4d7f1688a512741c86b511 was pushed to origin/main
without force and git ls-remote verified the exact branch. Complete payload inventory
passes all 15,122 file sizes/hashes; 1,324 inherited native binary files match the
prior accepted inventory byte-for-byte. Fourteen inherited files changed: eleven
Part Python modules, two GUI modules and the managed launcher. LegacyConversion.py
is added. release-info.json separates source/native/launcher identities and actual
acceptance; payload-manifest.json contains the verified complete inventory.
Manifest SHA256: b10af57ceab8681c0e64d096a0ef5c3d453d869417b1ee3d09ecee9f31355b0d.
Launcher SHA256: 05c3a107c9ce1e0e370367a4e84e2ac8afe7a9e8e92cdb7543bc3db9a2547518.
715 generated payload bytecode files were removed before inventory; the inherited
inventory contained no pyc files. Useful palette rollback payload, native compilation
tree and required dependencies/toolchain remain. No release/deployment is claimed.

Cleanup removed 276 raw task-validation files and nine source/test bytecode files;
the earlier 715 payload bytecode removals make 724 generated bytecode files removed
in total. validation/legacy-integration is absent. Final saved desktop target and
working directory were reopened/verified again after cleanup. Owner documents,
settings, source archives, useful rollback/native builds and toolchains are retained.
The authorized twelve-task sequence stops at this delivered bounded milestone.
Follow-up qualification requires a separate prompt; native FEM and wider
custom/physical acceptance remain explicitly pending above and in roadmap 12.FEM.

## Legacy migration task eleven — bounded finishing adapters

Task eleven is complete in source and native source-mode acceptance. Three
independently versioned compatibility adapters expose original dress-up,
pattern/transformation and Boolean operations in component History. Native owners,
Origins/Group/Tip, topology references, Originals/Transformations/settings,
suppression, Boolean targets/tools and placement compatibility remain intact.
Standalone Part outputs remain direct, avoiding duplicated compound geometry.
These are native editable adapters, not physical flattening into independent shared
operations. Technical contract: tests/LegacyFinishing.md.

Hidden access links have distinct UUIDs and complete native frames; History resolves
the original editor. Input dependencies precede consumers, with authored order for
compatible operations and mutually connected native transformation helpers. Separate
LegacyDressUpVersion/LegacyTransformVersion/LegacyBooleanVersion=1 upgrades recognized
older conversions after manifest validation. Original source bytes, identities,
formulas, evaluated geometry and shared instance placements remain protected.
Native editability precedes the existing explicit dumb body/sheet/curve/point
structural recovery ladder; stale/missing output remains reported for repair.

Initial ten-check attempt failed a CircularPattern fixture using unsupported Angle;
evidence serialization also failed, and isolated process 5556 required termination
after graceful close timed out. This was not acceptance. Corrected twelve-check
focused run passed and process 8104 exited normally. The first combined run passed
128 of 129 checks but found a real sketch-order regression: strict Body Group sorting
moved a later-created external sketch source after its consumer. That run is failed
evidence; process 9064 exited normally. Dependency-aware ordering fixes the defect.
Unchanged geometry engines were not broadly repeated after this bounded fix.

Corrected final batch: 55 checks in ten suites — finishing 13, structure 12, Body
history 9, datum 8, sketch 8, and one retained native editor check each for extrusion,
revolution, Loft, Pipe and Helix/primitives. Failures/errors/skips all zero; native
exit 0. Native 26.3.0devR49296, revision
8746c1076071a7b9decff07577b6a163a0f76ee9. All 34 recorded module/test paths and hashes
match unchanged final source. Process 11008 exited normally. Actual Qt History
Double-clicks open original Fillet, Linear Pattern and Boolean editors; native radius
control Accept/Cancel/Undo/Redo passes. Four dress-ups, five transformations,
ordered MultiTransform, combined Pattern inactive settings/suppression, all three
Boolean modes/tools, placed shared geometry, formulas, conversion/edit Undo/Redo,
protected FCStd bytes, cold cadprt restore, upgrades, missing sources and stale
output pass. All earlier retained editor families and the backward sketch-reference
regression pass on corrected source. No owner process or duplicate worker was used.

Native stderr retains stylesheet/hasher, scope, transient no-base/tool-shape and
recursive recompute messages, plus deliberate missing-source/BREP fixture diagnostics.
This is not warning-free installed editing. Custom Path/Point variants, physical/
high-DPI owner editing, broader whole-file/external consumer acceptance and packaging
remain integration gates. Task twelve is separate and has not started. No new native
build/payload or desktop shortcut change; owner delivery remains batched.

UI-only DOCX rendered: 91 pages; pages 1–89 pixel-identical to the 90-page baseline;
changed page 90 and new page 91 inspected. Corrected dependency-order text re-rendered
and inspected. Other ZIP entries and native automatic numbering unchanged.
DOCX SHA256: 9bad3d834ba42d004d5119eb42d92f457c05763fc088cdcc172254d665c3a4cf.
Four changed Python AST checks and git diff --check pass. Technical documentation
remains in Markdown. Cleanup removed 358 raw task files and 333 generated bytecode
files; validation/legacy-finishing is absent. The 15,121 inventoried payload files,
useful builds/dependencies, settings and source/documents remain protected.
Publication: milestone 89943b9d73feb08c08e8b39d3792ed5cfc0e1044 was pushed to
origin/main without force. git ls-remote verified that exact remote branch and the
milestone working tree was clean. This is source publication, not installed owner
delivery. Task eleven stops at this completed milestone.
Task twelve (whole-file mixed-history/external/shared consumer
and recovery qualification, with grouped owner packaging) requires its separate
owner prompt. Do not replay the recovery queue or start another worker.

## Legacy migration task ten — bounded Helix and primitive adapters

Task ten is complete in source and native source-mode acceptance. Both
families reuse the shared native chain publisher and retained editor links, with
separate qualification and family-version upgrades. Helix retains authored parameter
laws/profile/axis; eight primitives retain native dimensions and placement. Original
feature/final Body identities, geometry and shared instance frames survive. Shared
mode changes retain native types; converted primitive shape changes require a
separate operation. Attached/unsupported/stale/native Common histories retain native
ownership and editors; standalone Part Helix curves and primitives remain native.
Technical contract: tests/LegacyHelixPrimitives.md.

Initial native checks pass actual shared/native History events, Preview/Accept/Cancel,
all Helix parameter modes and eight placed primitives, geometry/previews, explicit
targets, original-type modes, undo/cold persistence, FCStd bytes, formulas/refusal,
failed geometry rollback, stale output, prior-file upgrade and standalone controls.
The first seventeen-suite attempt passed task-ten's eleven checks and shared
Helix/Primitive/Pipe/Loft/prior operation checks, but external structure failed:
publishing a standalone primitive carrier duplicated its native compound volume.
That attempt is not acceptance and exited normally. Standalone primitives now
retain their original native finished outputs directly; no duplicate carrier is
created. The corrected final batch passes external geometry/save-order/original
bytes and native root primitive persistence, alongside all feature checks. Failed
attempts are not acceptance. All isolated processes exited normally; no owner
process or duplicate worker was stopped or created.

Final batch: 178 checks in seventeen suites — structure 12, Helix/primitive migration
11, shared Helix 9, shared Primitive 7, Pipe migration 13, shared Pipe 8, Loft migration
18, shared Loft 9, revolution migration 15, extrusion migration 14, shared Revolve 7,
inventory 8, Body history 9, datum 8, sketch 8, editor rollback 10, curve profiles 12.
All unittest failures/errors/skips zero; native exit 0. Native 26.3.0devR49296,
revision 8746c1076071a7b9decff07577b6a163a0f76ee9. All 41 recorded loaded module/test
paths and hashes match unchanged final source. Actual Qt History events cover
shared and retained editors; Preview/Accept/Cancel, undo/redo, cold persistence,
further recompute, original types/IDs/UUIDs, all four Helix parameter laws and eight
primitive kinds, targets/presets, attachments/axes, formulas/refusal, rollback,
stale/native retention, external/shared/dumb recovery and prior-file upgrades pass.

Stderr retains stylesheet/hasher, native Refine fallback, transient no-base
Helix/Primitive/Pocket/Pipe, scope and recursive recompute messages, deliberate
missing-source/BREP fixture diagnostics and native TempoVis restoration warnings
after a document-closing fixture. Valid native outputs do not establish successful
splitter removal or warning-free installed editing. Owner packaging, broader
whole-file/external consumer qualification and physical/high-DPI acceptance remain
integration gates. This is source-mode acceptance, not installed delivery.

UI-only owner DOCX rendered: 90 pages; pages 1–89 pixel-identical to baseline;
changed page 90 inspected. Other ZIP entries and native numbering unchanged.
DOCX SHA256: 33a4ea6e26655332d18ddf28fd33bfadba81bfed04b0eff629d876c159476df1.
Both isolated shared task captures inspected; narrow test styling is not owner
theme/layout acceptance. Five final Python AST checks and git diff --check pass.
No new native build/payload/desktop shortcut change; installed delivery remains
batched with later migration integration. Task eleven has not started.

Cleanup removed 335 raw task files and 305 generated bytecode files. The task's
legacy-helix-primitives validation directory is absent; the accepted 15,121-file
payload inventory, useful builds/dependencies, owner settings and source/documents
remain. Publication: milestone 73445a60b06272dcaf73a918fa0508e2c8036b0f was
pushed to origin/main without force; git ls-remote verified that exact remote
branch and the milestone working tree was clean. This is source publication,
not installed owner-build delivery. Task ten stops at this completed milestone.
Task eleven (bounded dress-up, pattern/transformation and Boolean adapters)
requires its separate owner prompt.

Final changed source/test SHA256:
LegacyConversion: ffe71a4464ff2c5d567723ffab2080ca3a327fdd3ae46182dcbf71e262f860c5
ComponentNativeOperation: 959271bfefe034a327a0d50606020b1e737a80d86d7ce1acd5eaaef8715a3d8e
ComponentModel: 2d04904f02f3318c7688018ff58b9aa73786ac0e176e024ce8c007d4f7d06e3f
freecad.gui.ComponentNavigator: 4f39bbc6103e530c5b7bb8e2d278bdc446454f07da55794a70c4e59ef04e6b0f
TestLegacyHelixPrimitives: 93b43d72fba45bd6e3e90fcb5073d5864713f92ce9f09c9e4cc92b91e64cb596

## Legacy migration task nine — Pipe profiles, paths and orientation

Task nine is complete in source and native source-mode acceptance. Qualified
independent native Pipe chains reuse the shared publisher, including mixed prior
families. Original names/types/native IDs/UUIDs/labels, profile/ordered sections,
Spine/AuxiliarySpine picks, orientation/transition/transformation, flags/formulas
and placements remain. Inputs appear once before their first consuming operation.
Intermediate results give explicit targets; the original final Body keeps its
Origin/view provider and child-scoped native Tip bridge. Every mapped feature and
final Body passes volume and bidirectional solid differences. Converted shared
Pipe mode/target edits retain original native types via persisted Boolean presets.
Nullable auxiliary paths read correctly; unavailable selected edges give a repair
message instead of an uncaught index exception.

Attached/dependent/non-sketch/reference-expression/point/whole-sketch-edge,
unsupported transformation, native Common/no-material and invalid/unverified
histories keep original owners, settings, available geometry and native editors.
Distinct-UUID complete-frame History access links report missing/mismatched/invalid
sources as Needs repair. Standalone Part Sweep keeps Solid/Frenet/Transition/
Linearize and exact sections/path; verified solids gain a published result, sheets
remain native. LegacyPipeVersion=1 upgrades recognized earlier converted files,
preserving prior input/access-link UUIDs and labels. Shared evaluated dumb recovery
remains the last structural fallback with stale/unavailable output explicitly
reported. Broader physical frame/non-sketch promotion remains separate scope.

Thirteen focused Pipe migration tests pass,
including actual shared/native History editor events, Preview/Accept/Cancel,
conversion/edit Undo/Redo, original identities/references and shared geometry,
all orientations/corner transitions, Multisection, mixed Pad/Pipe targets, original
additive/subtractive type-preserving mode edits, cold-restored Common presets,
path constraints/recompute, FCStd bytes/cadprt reopen, formulas/refusal, missing-edge
repair, failed geometry rollback, native attached/Common/stale retention,
standalone solid/sheet Sweep and previous-file UUID-preserving upgrades.

Final native batch: 151 checks in fourteen suites — Pipe migration 13, shared Pipe
8, Loft migration 18, shared Loft 9, revolution migration 15, extrusion migration
14, shared Revolve 7, inventory 8, structure 12, Body history 9, datum 8, sketch 8,
edit rollback 10, curve profile 12. All unittest errors/failures/skips zero; native
exit 0. Native 26.3.0devR49296, revision
8746c1076071a7b9decff07577b6a163a0f76ee9. All 34 recorded loaded module/test paths
and hashes match unchanged final source. Full shared Pipe/Loft native command routing
passes. Prior external/shared/frame/dumb recovery regressions remain passing.

The initial focused run exposed missing-edge IndexError handling and two invalid
fixture method calls; the path repair handler and dimensional-constraint fixtures
correct those failures. Failed runs are not acceptance. All isolated processes
exited normally; no owner process, duplicate worker or new native build occurred.
Stderr includes native stylesheet/hasher, transient no-base SubtractivePipe/Pocket,
recursive recompute, scope and deliberate missing-source diagnostics, plus native
TempoVis restoration messages after a document-closing fixture. This is not
warning-free installed acceptance. Owner payload and saved desktop shortcut remain
the accepted palette-dismissal delivery. Packaging, warning-free installed editing,
broader whole-file/external consumer qualification and physical feedback remain
integration gates; task ten has not started.

Six changed Python AST checks and git diff --check pass. UI-only DOCX rendered:
90 pages, first 89 pixel-identical to baseline; changed page
90 visually inspected. Other ZIP entries and native numbering unchanged. Actual
isolated shared Pipe task capture inspected; narrow profile styling is not owner
theme/layout acceptance. Backend contracts remain in tests/LegacyPipes.md.
DOCX SHA256: 1c7e7570d558519ef38af8941055944b7f198b5cf17727ca63dae2e4b9499485.

Cleanup removed 274 raw task files and 302 generated bytecode files; the designated
legacy-pipes task directory is absent. The accepted 15,121-file payload inventory,
useful builds/dependencies, owner settings and source/documents remain.
Publication: milestone a9f3dbb552883704f183917f2520308bc56c82c8 was pushed to
origin/main without force; git ls-remote verified that exact remote branch and the
milestone working tree was clean. This is source publication, not installed owner
build delivery. Task nine stops at this completed milestone.
The next feature task is ten, bounded Helix/primitive adapters, only after its
separate owner prompt. Installed owner delivery remains batched with integration.

Final changed source/test SHA256:
LegacyConversion: 34394f94c7183401765c473c19d7d0f123b828afa854cc013ee3952d63a71696
ComponentNativeOperation: 803e4207cdacbd1275d42f965eedb3e47e6759e3736b54bd262ac7a08e85cdc2
ComponentPipe: 0924cb35f51bcb6125ce34055762fe357007a82dec6b7d8084763a2f7f6d27eb
ComponentModel: c792c8f9e34eb1394f1cbdce314c063796794ad21f3dc4917c345bb1c04e2f41
freecad.gui.ComponentNavigator: 1fafd854cfffba7e13c6e42c6a82c2c5710f85ea6a28eb4a85751f7b0cf84eb6
TestLegacyPipes: 6de6d051f12463a69c2aed454ab03abb11be049c143814d0a96db3604768b7b2

## Legacy migration task eight — ordered Loft sections and Boolean targets

Task eight is complete in source and native source-mode acceptance. Native Loft
chains with independent sketches reuse map_native_chain, including qualified mixed
Pad/Pocket/Revolution/Groove inputs. Original names/types/native IDs/UUIDs/labels,
ordered Profile/Sections and exact subreferences, constraints/formulas, placements
and direct consumers remain. Every section input precedes its operation in History.
Intermediate published results give explicit BaseFeature/ConsumedResults targets;
the original final Body retains its Origin/view provider and native Tip bridge.
Every mapped feature/final Body passes volume and bidirectional solid differences.

Smooth/Ruled, Closed, Refine, supported fuzzy tolerance, placed sections and native
vertex endpoints remain. Shared Loft reorder/preview/parameter/target edits preserve
original converted feature/type/ID. Native Loft's common Boolean maker supports
Add/Subtract/New Body; converted edits persist expanded Union/Subtraction/Common
presets before choosing the requested mode. Native custom-enumeration cold restore
and both original additive/subtractive types pass. New Plus feature replacement
behavior is retained. Formulas use properties; self/downstream targets and invalid/
ineffective edits fail without changing saved parameters. New Body clears consumption.

Body-attached/dependent/non-sketch/reference-formula/unsupported/mixed-family cases,
Common and native no-material histories retain native owners, parameters and output.
Legacy Part2D edge picks consume the whole sketch in the native engine; these remain
native rather than being rewritten as shared subset helpers. Shared section sources
are not duplicated. retain_native_operation now serves Extrude/Revolve/Loft with
hidden distinct-UUID complete-frame History links and original native editors.
LegacyLoftTarget is a conversion-time BaseFeature snapshot; original targets stay
authoritative. Missing/mismatched/invalid sources show Needs repair.

Standalone native Part Loft preserves ordered Sections, Solid, MaxDegree, Linearize,
Ruled/Closed and its native editor. Verified solids gain a published result; sheet/
curve/invalid/unverified output remains retained and reported. LegacyLoftVersion=1
upgrades recognized older converted files after manifest/identity validation, keeping
section/sketch and previous access-link UUIDs/labels. Promoted earlier links become
hidden Internal references. Ordinary new component files are excluded. Original
FCStd bytes remain protected; shared explicit evaluated dumb body/sheet/curve/point
recovery remains the last structural fallback and reports stale/unavailable output.
This is bounded physical mapping/native retention, not universal frame promotion.
Technical contract/procedure: tests/LegacyLofts.md.

Final native GUI batch: 130 checks in twelve suites — Loft migration 18, shared Loft
9, revolution migration 15, extrusion migration 14, shared Revolve 7, inventory 8,
structure 12, Body history 9, datum 8, sketch 8, edit rollback 10, curve profile 12.
All unittest errors/failures/skips zero; native exit 0. Native 26.3.0devR49296,
revision 8746c1076071a7b9decff07577b6a163a0f76ee9. All 30 recorded loaded module/test
paths and hashes match final source. Actual Qt History double-clicks cover retained
native Loft editor close and shared ordered sections, Preview/Accept/Cancel and
reopening after Undo/Redo. Geometry/sharing, exact section references, modes/targets,
closed/placed/vertex sections, native presets/cold persistence, expressions/refusal,
meaningful invalid-edit rollback, original bytes, cadprt reopen/further edits,
previous-file upgrades, no-op shared inputs, stale source retention, standalone
solid/sheet settings and prior external/shared/dumb recovery regressions pass.

Earlier native preset restrictions required a persisted custom enumeration; one
new fixture needed component section registration. Those failed runs are not
acceptance. No process was stopped; all isolated runs exited normally. No owner
process, duplicate worker, new native build or payload/shortcut change occurred.
Stderr includes old installed Navigator callbacks under payload Ext, stylesheet/
hasher and recursive native recompute warnings during retained editing, plus deliberate
missing-source fixture diagnostics. This is not installed or warning-free acceptance.
Owner payload/shortcut remain the accepted palette-dismissal delivery. Packaging,
warning-free installed editing, arbitrary frame/non-sketch/other-family promotion,
external/cross-workbench whole-file qualification and physical feedback remain
integration gates. Task nine has not started.

Five changed Python AST checks and git diff --check pass. UI-only owner DOCX final
render has 90 pages: previous 89 pages pixel-identical; new page 90 visually inspected.
Other ZIP parts and native numbering unchanged; DOCX SHA256
71559565f5c6347ee78468ca53aa46a3bec3eeaef24eb56da88fac1fcaa66d2e.
The actual shared legacy Loft task capture was inspected in its narrow isolated
profile; this is not owner-theme/layout qualification. Technical/backend/evidence
information stays in Markdown. Cleanup removed 257 raw task files and 300 generated bytecode files; the task
validation directory is absent. Accepted 15,121-file build inventory, useful
builds/dependencies, owner settings and source/documents remain. Publication: milestone
42e6afe0a360b39ce520a63280ca47818fc10121 was pushed to origin/main without force.
git ls-remote verified that exact remote branch; the milestone working tree was
clean. This receipt records publication, not installed owner-build delivery.
Exact next task: nine, Pipe profiles, paths and orientation, only after its separate
owner prompt. Native owner-build delivery remains batched.

Final changed source/test SHA256:
LegacyConversion: 18c7f01680dfbd0b0cef8996972f7397c67679748c72b8a2b7b32f392ff08dd8
ComponentNativeOperation: 469edf94f787772cb48aafa595b68a49cdc27fcd0aa1224cdb7da0edb4452d6b
ComponentModel: 3c652e04f918ddbe50a3b74c21961cf75e318faa6c0e2936eb8bf1d3d25eb95c
freecad.gui.ComponentNavigator: 6392a99744fd8c7829d49b62e132af7bc37b928bcdb80fdbdba55063b73cf24c
TestLegacyLofts: 53b6663cb78ac659f776280ce800d2a6174a36c477c9a3b3b1c41f4f4afdce9a


## Legacy migration task seven — Revolution/Groove axes, angles and targets

Task seven is complete in source and native source-mode acceptance. The extracted
map_native_chain serves qualified Pad/Pocket and Revolution/Groove histories, with
original native names/types/IDs/UUIDs/labels, independent sketches and final Body
preserved. Intermediate published results provide explicit BaseFeature/ConsumedResults
links. The original Body retains its Origin/view provider and hidden native Tip
bridge. Each feature/final Body passes volume and bidirectional solid differences.
Mixed independent Pad/Revolution histories reuse this same publisher.

Native sketch vertical/horizontal/construction axes, one/two/symmetric angles,
reverse/project/refine, signed start offsets and Groove ThroughAll remain intact.
Shared Revolve edits supported parameters/targets in place; formulas use native
properties and downstream/self targets fail before mutation. Converted native
Revolution/Groove additive/subtractive type switches are refused to preserve native
identity; create a separate Revolve for that change. New Plus operation type changes
retain their existing behavior. Whole-sketch scratch previews now use temporary
native evaluated sketch geometry/Placement/construction flags, fixing rotated angular
frames and Axis-zero references without copying formulas or cross-document links.

Body-attached/expressed/reference-frame and other-family histories retain original
engines, ownership, parameters and available output. Hidden complete-frame History
links open original native Revolution/Groove editors; missing/invalid sources need
repair. Native Part Revolutions keep vector/linked axes, signed Angle, Symmetric and
native editor; verified solids gain published results and sheet/curve output remains
retained. Shared evaluated dumb recovery remains the final structural fallback;
stale/unavailable output is explicit. This is bounded mapping/native retention,
not a claim of universal physical promotion. Contract: tests/LegacyRevolutions.md.

LegacyRevolveVersion=1 upgrades recognized prior converted files after manifest
validation, preserving original sketch and older access-link UUIDs. Promoted earlier
links become hidden Internal references. Conversion Undo restores native ownership;
Navigator ignores Parts that lost their component identity, including view snapshots,
until conversion/view reopening restores it. Original FCStd bytes remain protected.

Final native GUI run passes 103 checks in ten suites: revolution 15, extrusion 14,
existing Revolve 7, inventory 8, structure 12, Body history 9, datum 8, sketch 8,
edit rollback 10, curve profile 12. All unittest errors/failures/skips are zero;
native exit 0, version 26.3.0devR49296, revision
8746c1076071a7b9decff07577b6a163a0f76ee9. All 23 recorded loaded module/test paths
and hashes match final source. Actual Qt History double-clicks cover shared Groove
Preview/Accept/Cancel/reopen after Undo/Redo and retained native Groove editor close.
Geometry/sharing, modes/targets/type guards, formulas, rotated/construction/horizontal
axes, signed offset boundaries, original bytes, cold cadprt reopen/further edits,
older-file upgrades, stale source retention and original reference-start/datum axes
pass. Prior external/shared structural conversion and dumb geometry recovery pass.

Earlier preview/axis failures and the non-existent fixture setGeometry call were
corrected; an intermediate Undo regression found the second stale view-snapshot path.
Failed isolated test PID 4456 was stopped before rerunning. The final accepted native
run exited normally. No owner process was stopped, duplicate worker started or new
native build produced. Stderr still includes callbacks from the older installed
Navigator under payload Ext, native stylesheet/hasher warnings and deliberately
missing-source fixture diagnostics; this is not installed or warning-free acceptance.
Current source Undo paths pass. Owner payload/desktop shortcut remain the accepted
palette-dismissal delivery, unchanged; source-mode does not qualify that payload.
Packaging stays batched. Arbitrary frame promotion, external/cross-workbench mixed
histories and physical owner feedback remain later integration gates.

Five changed Python AST checks and git diff --check pass. Owner DOCX is UI/UX only;
final 89-page render differs only on page 89, visually inspected. Other ZIP parts
and native numbering remain unchanged. Final DOCX SHA256
2cc8e5148dd731b17ade64e1c9099ca36b1cc6035fc9cfc3181489ada7ad97d2.
Native shared Revolve task capture was inspected; it uses an isolated test profile,
not an owner-theme qualification. Technical/backend/evidence documentation remains
Markdown. Cleanup removed 347 raw task files and 297 generated bytecode files; the task
validation directory is absent. Accepted 15,121-file build inventory, useful
builds/dependencies, owner settings and source/documents are preserved. Publication: milestone
7882c0c871d094777017904b2bef54df95f96857 was pushed to origin/main without force.
git ls-remote verified that exact remote branch; the milestone working tree was
clean. This receipt records publication, not installed owner-build delivery.
Exact next task: eight, Loft sections and additive/subtractive targets, only after
its separate owner prompt. Tasks eight onward have not started.

Final changed source/test SHA256:
LegacyConversion: 2329a29300f0fb2892cab56d4753674d9e4b8c90b185018dc1c03905a1c762b5
ComponentModel: 313b4717de5efe2d3fc2d56e19bcf92081f35bb66d4d4a11320b7d09dcc2efa0
ComponentRevolve: d338acd43481bc2fe571193307abacbd89f970266ad6339f2e5d974ac28ae8ff
freecad.gui.ComponentNavigator: 155c17eced8e93a4952b6b5b531b9d1b1a0ba644c867621717549a90f3380865
TestLegacyRevolutions: 8def5614ba5cb23d9515dcd794bada4ce904d34c53aa139e116cf78809ace665


## Legacy migration task six — extrusion parameters, targets and result chains

Authorized task six only. `LegacyConversion.extrusion_chain_plan` /
`migrate_extrusions` map qualified independent native Pad/Pocket chains inside the
existing native transaction. Original names/types/native IDs/UUIDs/labels, native
extent parameters/formulas, sketch inputs and downstream feature references stay.
Intermediate published results become explicit BaseFeature/ConsumedResults targets;
the original final Body remains the Result with its Origin/view provider and hidden
child-scoped Tip bridge. Every mapped operation/final Body passes volume and
bidirectional solid differences. Normal one-sided solid Part Extrusions retain their
native producer and gain a published result; other native outputs remain retained.

The shared Extrude editor reads native Pocket extents/profile and normalizes its
legacy inverse normal. Pad/Pocket Add/Subtract/New Body and explicit target edits
retain the native object/type; New Body clears consumption. Self/downstream targets
and formula overwrites fail before mutation. Standalone Part Extrusion retains its
operation kind instead of silently replacing its native identity. Native frame,
attachment, mixed-family, axis/custom-vector, referenced extent, signed-length and
unverified cases retain original engines, parameters, ownership and available output.
Hidden complete-frame History links open original editors; missing sources require
repair. This is native retention, not a claim of full physical promotion of those
histories. The evaluated dumb recovery order and protected original files remain.
Full contract/procedure: tests/LegacyExtrusions.md.

LegacyExtrudeVersion=1 is idempotent. Recognized older converted files upgrade after
manifest/identity verification in the existing transaction; original sketch UUIDs
and earlier access-link identities survive promotion. Old access links become hidden
Internal references following their independent source. Explicit definition reopening
rebinds a reused window after Undo restores master context, fixing actual History
editor reopening without modifying model ownership or placement. The earlier pilot
also now retains original input/operation labels during registration.

Native source-mode acceptance comprises an 80-check combined pass (13 extrusion,
45 prior migration, 10 edit rollback and 12 curve profile), then a final guarded-source
35-check pass (14 extrusion, 9 Body history, 12 curve profile), with 34 repeated checks:
81 distinct checks. Both accepted runs have no errors/failures/skips and native exit 0.
Native version 26.3.0 revision 8746c1076071a7b9decff07577b6a163a0f76ee9. Actual Qt
History double-clicks exercise shared Pocket Accept/Cancel/reopening after Undo/Redo
and retained native Pocket editor close. Geometry/sharing, mode/target edits,
through-all, two-sided taper, expression edits/refusal, Undo/Redo, original bytes,
cold cadprt reopen/further edits, prior-file UUID/label upgrades, standalone extrusion
and custom-vector native preservation/editing pass. Prior origin/datum/sketch/frame,
structure/inventory, rollback/save-during-edit and profile/preview regressions pass.

The final guard adds custom-vector histories to native retention; experiments showed
the shared scratch preview lost an elevated profile frame. Failed experiments are
not acceptance and were removed. Further custom-frame promotion remains an explicit
integration gate. Earlier failed attempts corrected nullable axis handling, existing
history metadata, source-overlay GUI package attributes and reused-window context.
No fake geometry, duplicate worker, owner-process stop or native build was used.
Installed owner payload/shortcut remain the accepted palette-dismissal delivery;
packaging is batched, source-mode tests do not qualify installed migration behavior.
Mixed-feature/external/cross-workbench acceptance remains task twelve.

Nine AST checks and git diff --check pass. The 80-check run records 19 loaded paths;
only LegacyConversion and the extrusion test changed for the final custom guard.
All 14 final follow-up module/test paths/hashes match final source. Changed source:
LegacyConversion 031947c4da9a649a02ac5c0dac3ac81701185328371ee542bb2744bd29712898;
ComponentModel 5b33d4d0e01954ad7b5668fecf0fa791d7552d543588c41cd007be854e184a83;
ComponentProfile ebdc2295cba1a3f0042efcd68fab9142ba4c8de6df29a59eb9357e68ce1dfd95;
ComponentExtent 152b22179cb7c751e5762848877294aeb76d8d002801f078871808f5889fd85a;
ComponentExtrude b6c9661abf64b4eca75e4501db2d05ea52488fd23c168a6b30077e4dd693b14d;
ComponentNavigator adccbe0890e0f43676f773c6eef46960daaa5e4fac241803eae431d7bae0c920;
ComponentExtrudeTask ee23a09761ab0d6e06004c8454c8ce916391f5d43bbcf245d8f772021f71219c;
extrusion tests 10cc858346afadb1aa249f240bdc8315bbe4d80013d158cc02feceb54aaa7287;
Body tests f8fa01488eca7756cf5721d2693c03206f4f63bf18fc40eb0cee07fbcb85fb73.

Owner DOCX contains only affected History/mode/target/editor/repair interactions.
Final render remains 89 pages; only page 89 changes and is visually inspected.
Other ZIP parts and native numbering remain unchanged. DOCX SHA256
ce734eea266191873f5b696077506aa93b3982d505025ec3c1cabf79130f4516.
Validation profiles/logs/captures/fixtures/renders were deleted after recording
evidence: 393 raw task files and 295 generated bytecode files removed; task validation
directory is absent. Accepted build inventory, useful builds/dependencies, owner
settings and source/documents remain. Publication: milestone
5693d99a9de25f9c7d9dd323ed7714350baca25e was pushed to origin/main without force;
git ls-remote verified that exact remote branch. Working tree was clean after the
milestone push. This receipt is documentation, not installed owner-build delivery.
Exact next task is seven: Revolution/Groove/Revolve axes, angles and targets. Preserve
original identities/geometry, retained attachments/native engines, explicit result
chains, shared/parent-owned placements, original files and recovery. Do not start it
without the separate owner prompt.

## Legacy migration task five — native sketch inputs and shared consumers

Authorized task five only. `LegacyConversion.migrate_sketch_inputs` retains original
native sketch names/types/IDs, constraints, expressions, external geometry, supports,
offsets and consumers. Component-owned sketches remain independent Object inputs.
Retained Body-owned sketches have distinct-UUID hidden History input links before
their Body, ordered by sketch dependencies, with a native complete-frame expression
Body.Placement * Sketch.Placement and LinkTransform=False. Original Body Group/Tip
and sketch owners remain intact for feature families awaiting adapters. No sketch
copies per instance or frozen replacements of valid parametric inputs are created.

The narrow first-Pad pilot now admits dimensional constraint expressions and external
inputs independent of its Body. Native attachments, Body-history/frame dependencies,
frame/property expressions, nonidentity Body frames and unsupported extents remain
editable native histories with explicit reports. This is deliberate preservation,
not a claim of physical promotion of all attached Body features; task six owns the
full extrusion adapter. Native History double-click edits the original sketch;
missing/mismatched/invalid sources show Needs repair. LegacySketchVersion=1 is
idempotent. Recognized older converted files upgrade through the existing single
native transaction only after manifest/identity verification. Existing original
FCStd protection and evaluated dumb recovery remain in place. Contract/procedure:
tests/LegacySketchInputs.md.

Final native source-mode acceptance: 45/45 distinct checks, no errors/failures/skips,
native exit 0, version 26.3.0 revision 8746c1076071a7b9decff07577b6a163a0f76ee9.
Suites: sketch inputs 8; datum frames 8; Body history 9; structure 12; inventory 8.
Actual Qt History double-click opens/closes the original native sketch. Native
constraints/formulas/support/external reference identities, complete rotated frames,
shared LinkTransform geometry, expression source/frame edits, shared Pad/Part-Extrusion
updates, sketch dependency order, Undo/Redo, protected original bytes, cold cadprt
reopen/further edits and undoable previous-file upgrade pass. Prior native Body
edit task Accept/Cancel, datum editor, original geometry and explicit dumb recovery
regressions pass. Four AST checks and git diff --check pass. Eight loaded source
module paths/hashes match final source; changed modules/tests:
LegacyConversion 1dca70aa12e0bcd5701ec2ea159fd1a33d580663074f2f9dd3caa04bdafeb8a6;
ComponentModel 2b5e11ea5d724e26f1e3720a3fdb47372e1106ae13ebd39ff7139c8ece07a366;
ComponentNavigator 0a7710e293e197c16766761eb9b8a046e12c1824217947736dcc90c09c4f0ff7;
sketch tests 7e3c2fa4d319488574f495d958b9ceb0919f238d3172f54a6b483a2692b144e3.

Earlier attempts are not acceptance: external references must obey native Body/Part
scope, and the initial two-Body shared-profile fixture produced invalid native
geometry. Corrected fixtures use a legal Body-owned reference or independent sketch,
and a valid shared native Pad/Part Extrusion. The final combined run passes on the
final source. No owner process was stopped, duplicate worker or native build created.
Source-mode acceptance does not qualify installed migration behavior. Owner payload
and shortcut remain the accepted palette-dismissal delivery; packaging stays batched.
Mixed-feature/external consumer qualification remains task twelve.

Owner DOCX changes only affected sketch History/edit/repair UI. Final render remains
89 pages; only page 89 changed and is visually inspected. Other ZIP parts and all
2783 native automatic-numbering references are unchanged. DOCX SHA256
16bff01df0375cacab288683a79b0de80429fc6d8b579db8012223ea419c9e8c.
Task validation profiles/logs/fixtures/renders were deleted after recording evidence:
233 raw files and 274 generated bytecode files removed, validation directory absent.
Accepted build inventory, useful builds/dependencies, owner settings and source are
preserved. Publication: milestone e17b0cf34c59f169b2222c09fcc3f196ee10411d
was pushed to origin/main without force; git ls-remote verified the exact remote
branch matched it. Working tree was clean after that milestone push.
Exact next task is six: Pad/Pocket/Extrude parameters, targets and result chains.
Preserve retained native attachments, sketch/feature identities, shared inputs,
original geometry/files and explicit recovery. Do not start it without its separate
owner prompt.

## Legacy migration task four — Origins and retained datum attachment frames

Authorized task four only. `LegacyConversion.migrate_datum_frames` retains native
Origins/OriginFeatures, datum planes/axes/points/coordinate systems, Body membership,
supports, offsets, reversals and expressions. Existing names/types/native IDs remain;
missing component UUIDs are allocated without replacing native objects. Direct datums
are Object construction inputs and excluded from physical ResultObjects. Body-owned
datums remain native; History exposes distinct-UUID links to their original sources.
LinkTransform=False and the complete native expression Body.Placement * Datum.Placement
preserve offsets/rotations and follow source/frame edits. New links are hidden by
default; infinite datum display faces must not compound into physical results.

History double-click opens the original native attachment editor; missing sources
show Needs repair, while invalid native sources remain editable for repair. The new
PlaneDefinition API refuses destructive redefinition of retained attachments/formulas.
Linked planes are available to new component sketches; native and managed support
frames follow their complete frame. Plane geometry resolves native plane/axis/point
inputs in component coordinates. These are retained editable native datum definitions,
not flattened native Body feature histories; task five owns further input promotion.
Nonstandard nested owners remain native with explicit reports. The existing evaluated
dumb recovery policy and original-source protections remain in place.

LegacyFrameVersion=1 is idempotent. `upgrade_datum_frames` upgrades recognized older
converted cadprt content after manifest/identity checks, including prior conversions
of unsaved native documents identified by their structural conversion report. Ordinary
new component files remain outside that upgrade. In-memory upgrade is one native
Undo transaction; subsequent saves use the normal manifest guard. Full contract and
procedure: tests/LegacyDatumFrames.md.

Final native source-mode acceptance: 64/64 distinct checks, no errors/failures/skips,
actual native exit 0, version 26.3.0 revision 8746c1076071a7b9decff07577b6a163a0f76ee9.
Suites: datum frames 8; legacy Body 9, structure 12 and inventory 8; plane frame 9,
plane task 12 and background result 6. Native datum/Origin identities, Body Group/Tip,
supports and formulas, rotated nested frames, shared LinkTransform geometry, coordinate
systems, offset/Body-placement edits, Undo/Redo, cold cadprt reopen/further edits,
older-file upgrade, associative new sketches, missing-source refusal and actual Qt
History double-click/native attachment editor close pass. Existing plane controls,
source-file byte protection, explicit dumb recovery and background results regressions
pass. Solid differences validate default physical geometry; broad drawing/CAM/FEM/Draft
consumer and arbitrary visible construction-shape qualification remain task twelve.
Seven AST checks and git diff --check pass. Final recorded runtime hashes match source:
LegacyConversion 6e1661519214a7962cd7a95a19d39fa2418adc69ba5496b51c1c81f7f8ec2e98;
CadDocument 11ea9ad31ca0109c6d608461853541542f612808f8d954a3f503d16a58cfc90c;
ComponentModel 7893a809672648b24d9e31a637afbf107621c823b9367558aefd8f2a3f6bc060;
ComponentSketch 834fc1ffbc533142cf1715f6c72f3af30df89ae791f9c0b05d271063f169351a;
ComponentPlane f09edeb32e28f21f23babcaf84549743eb8681902b4b36d2f2872ef195966fd6;
ComponentNavigator 84a999db4d08bd67ae8c22661b3868370e0f3d584233fe7a946c3093abe5482a;
datum tests 8f666c45aa371c6a5e7b7ca0c79e55a241d9e7c3db4ec78826cce63e5216bf4d.

Earlier attempts are not acceptance: native PartDesign datum type matching, infinite
construction-face compounding and attachment engines ignoring target placement were
corrected. A fresh combined suite completed on the final source; no owner process was
stopped, no duplicate worker created and no native build made. Installed owner payload
and desktop shortcut remain the accepted palette-dismissal delivery. Source-mode
acceptance does not qualify installed migration behavior; packaging remains batched.

Owner DOCX contains only affected datum History/edit/repair and New Sketch interactions.
Final render remains 89 pages; only page 89 changes and is visually inspected.
Other ZIP parts and native automatic numbering are unchanged.
DOCX SHA256 000f8c4c35faa394596e24ebbab67a1a4983cc0312b9eb4de530bee7c622b723.
Task validation profiles/logs/CAD fixtures/captures/renders and 281 generated bytecode
files were deleted after recording evidence. Useful builds, owner settings and tracked
source/documents were retained. Publication: milestone
47ecac13907ebcb5322b2cd1cbf9541e8f7cffd4 was pushed to origin/main without force;
git ls-remote verified the exact remote branch matched it. Working tree was clean.
Exact next task is five: Sketch ownership, attachments, constraints, expressions
and shared inputs. Preserve retained datum/native identities, frames, source originals,
shared definitions and explicit recovery. Do not run it without its separate owner prompt.

## Legacy migration task three — Body history and editable Sketch/Pad pilot

Authorized task three only. `LegacyConversion.body_history_plan` /
`migrate_body_histories` run inside structural conversion's native transaction.
The narrow pilot keeps original Sketch/Pad/Body names, types, labels, native IDs
and downstream references. Component History orders Sketch, Pad, Body; the original
Body becomes its final Result carrier. Its native child-scoped Tip points to a hidden
internal PartDesign::FeaturePython bridge with a global producer link to the Pad.
Producer placement is copied explicitly, retaining nonzero sketch offsets. Native
Origins/view providers remain intact; LegacyTip/LegacyBodyHistory record the original
history. Existing scalar/shared definitions and parent-owned occurrence frames remain
unchanged. The full contract and retained boundaries are in tests/LegacyBodyHistory.md.

Registration is idempotent for existing ownership; native group addition must not
steal a Pad when re-registering its independent sketch. Explicit legacy membership
also preserves source owners of pre-existing cross-Part consumers. Native Body views
without a Python Proxy are supported. A simple identity-frame, independent sketch /
first one-sided length Pad is admitted; other Body frames, attachments, mixed feature
histories and unverified caches remain native with explicit reports. Pad length
expressions stay editable through their original inputs/property editor; the task
refuses overwriting formulas and unsupported operation/target mode conversion.
Pre-edit freshness is captured before structural touches. Admitted output is checked
by volume and bidirectional solid differences before commit. Failures retain native
payloads through the existing explicit dumb geometry recovery; no geometry is fabricated.

Final acceptance: 35/35 distinct native source-mode checks, no skips/errors/failures,
native process exit 0, version 26.3.0 revision 8746c1076071a7b9decff07577b6a163a0f76ee9.
Suites: TestLegacyBodyHistory 9, TestLegacyStructureConversion 12,
TestLegacyConversionPlan 8, TestComponentBackgroundResult 6. Actual Qt History
single/double-click events open Sketcher and the shared Extrude task, including a
row refresh between clicks. Task Accept/Cancel, native Std_Undo/Std_Redo, structural
Undo/Redo followed by recompute, shared/placed geometry, independent inputs, native
length expressions, downstream Cut Body references, original-byte protection,
cadprt cold reopen and subsequent upstream edits pass. Retained mixed/placed Body
histories and explicit dumb recovery pass. Six AST checks and git diff --check pass.
Loaded final source hashes:
LegacyConversion 465f89ac90255ca6bc00d9ae98d39ab6197e4d477ee33166516998e8e799b8cd;
ComponentModel 5a9a7a76e045a80ba501d4ab5bdf67f49a85a44c7fab1683b95e0e3a361e0b42;
ComponentExtrude 998541f1da57f63e09460af8b3d6d62343a979257e9698ac73870eb32305249f;
ComponentResultView 4e1f99c35d2423bf62f8f4390bb0f790cafb044772e5769bb6d2f1a362ed9dc7;
pilot test 59936c63ceaf4fdf5a0095e73b70d8f5b15d89b6a0ade5c5c090f9600dda320a;
CadDocument b9801930595b64864d8992f77e46c20fbd17dd1f4d9518f33cd21aa3e104b0b6.

Earlier attempts are not acceptance: direct Tip-outside-Body experiment showed scope
warnings, then the child-scoped bridge was adopted; AttachmentSupport mapping,
transaction touches versus source freshness, re-registration ownership, bridge
placement and native view handling were corrected. GUI fixtures use PySide6 QtTest
and reject/reset tasks on teardown; reading a deleted status QLabel after successful
Accept was fixed. One owned timed-out exploratory process and one owned GUI test
process were stopped; no owner process was stopped. A temporary macro rewrite
encountered a release-time file lock; a distinct final macro and fresh isolated
process completed the final acceptance. Pre-existing stylesheet/cross-Part native
scope diagnostics in the fixtures are separate from test acceptance; broader
whole-file consumer/topological repair qualification remains task twelve.

Owner DOCX changes only History/edit interactions; all technical details/evidence
remain Markdown. Final render has 89 pages versus 88 before; only pages 88/89 change
and are visually inspected. All other ZIP parts and native numbering are unchanged.
DOCX SHA256 f97bebc832302173fb336d10600828ca13de439d99f278ffe5d1a4c8bf87a911.
No native rebuild or new owner payload is made. Source-mode results do not qualify
the installed palette-dismissal payload or desktop shortcut for migration changes.
Owner packaging and broader integration acceptance remain batched.

Task validation profiles/logs/renders/fixtures and 275 generated bytecode files were
removed after recording evidence; tracked files, useful builds and owner settings
were retained. Publication: milestone 0452871bfacbb96298836f1add275ecad8515f86
was pushed to origin/main without force; git ls-remote verified the exact remote
branch matched that source/native milestone. The working tree was clean afterward.
Exact next task is four: origins and datum
geometry/attachment frames. Preserve native payloads, reference identities, geometry,
shared instances and explicit recovery; do not run it without its separate owner prompt.

## Legacy migration task two — Models and Part Tree structural conversion

Authorized boundary: task two, retaining native feature history and the task-one
read-only inventory. CadDocument.convert_legacy / standard GUI File Open now use
LegacyConversion.convert_structure. Existing Parts become definitions; placed
containers become occurrences, existing scalar Links retain their own identities
and share definitions, and the permanent master remains separate. Standalone and
internally referenced geometry use wrappers; internal Body/Sketch/Tip ownership
remains native. Direct native outputs avoid duplicate Part compound geometry.

Original definition world frames, container local frames and displayed Link geometry
are preserved with explicit frame compensation and native transform/scale handling.
Occurrence numeric placement may change to compensate the new definition frame;
this is not an occurrence override added to a shared parent. Native Link forwarding
must not duplicate definition UUIDs on instances. Every file has its own transaction;
external dependency conversions commit independently in memory. Protected legacy
paths may remain native reference bases until new child cadprt files are saved, then
the parent; manifest guards prohibit overwriting legacy originals and premature
external-parent saves. Unresolved Links remain reported missing instances and must
be repaired before strict save acceptance.

Arrays retain native payloads/element identities and may present explicitly labelled
frozen evaluated output. They are not qualified as parametric component arrays.
If safe frame mapping fails (e.g. an expression-driven Part or nonrigid compensated
frame), validated captured top-level geometry is presented as dumb output while the
native hierarchy and features remain retained. Visible outputs are preferred; hidden
outputs are used if no visible output is available. Touched/invalid dependency caches
remain explicitly unverified. Missing geometry is reported, not fabricated.
See tests/LegacyStructureConversion.md for implementation and limitations.

Final acceptance: 20/20 distinct native source-mode checks (12 structural plus eight
inventory), FREECAD_PLUS_PROFILE_SOURCE=1, native revision 8746. This is not installed
owner-payload acceptance. Actual standard Open dialog, Models/Part Tree/root order,
rotated nesting, both LinkTransform modes, shared/scale-aware geometry, internal Body
links, Body Group/Tip/sketch retention, idempotence, Undo/Redo, cadprt reopen, primitive
recompute, original bytes, external save order, missing references, arrays and failed
frame recovery and preserved local-frame expression consumers pass. Native bidirectional solid differences validate geometry and
placement. Four syntax checks pass. Loaded source hashes:
CadDocument b9801930595b64864d8992f77e46c20fbd17dd1f4d9518f33cd21aa3e104b0b6;
LegacyConversion e1ff7468880c5784a4e5a5a14f971c040a850d923c07df56ada0adfa23708e02;
structural test fa20f1a38929a9a2fd4a70b47e52609aeaaf2392ed00b088e051a5843243aef3;
inventory test 0d28665e820ffa8dff2f8b7d819fa0ed279964697a5812764fab3414c1c8d390.
Earlier attempts are not acceptance: duplicated published geometry, forwarded UUIDs,
missing external native reference bases, scale compensation and native leading-dot
expression paths were corrected and the final combined suite rerun. The targeted
approval-review timeout was retried once successfully; it is not an application error.

Owner clarification is adopted in AGENTS.md: editable DOCX is UI/UX only; algorithms,
contracts and validation/build/publication evidence belong in Markdown. Task-one
backend prose was removed from DOCX and retained in the existing contract/testing
Markdown; task-two DOCX describes Models, Part Tree, recovery labels, Review conversion,
missing-instance repair and save interactions only. Final 88-page render changes only
page 88, visually inspected; other ZIP parts/native numbering are preserved.
DOCX SHA256 16fb2d39ecc345b4c0c960caf9c4bd3b19b2556bbc1d90a8e7c5c5167f4cc806.

Task validation profiles/logs/render output/fixtures and generated bytecode are
removed after recording these summaries. No new owner test build or native rebuild
is created; packaging is batched with subsequent integration. Current useful owner
payload and desktop shortcut remain the accepted palette-dismissal delivery. Physical
owner/installed consumer qualification is not claimed. Publication: source milestone
9124bd24e973a2f88a360942b6aec89532ed2e4f was pushed to origin/main without force;
git ls-remote confirmed the remote branch matched that commit before handoff.

Exact next task is three: Body history/results foundation and a narrow editable
Sketch → Pad pilot, preserving geometry/native identities, inputs and downstream
references through Undo/recompute/cadprt reopen. Preserve native/dumb recovery reports
and source originals. Do not run later tasks without their separate owner request.

## Legacy migration task one — read-only inventory and recovery planning

Authorized boundary: task one only. CadDocument.legacy_plan(document) delegates to
LegacyConversion.inventory for an already-open legacy document. It does not convert,
recompute, assign identities, change ownership, save or create fallback geometry.
Existing automatic legacy conversion remains unchanged. CMake registers the module
for the next packaged build. Current owner payload/desktop shortcut remain the
accepted palette-dismissal payload; no new owner build is delivered for this API.

Inventory records native keys/existing ObjectIds, property fingerprints, Body
Group/Tip, ownership, placements, native links/scale/array metadata, expressions,
external sources and dependency order. Native structural _Body backlinks are
excluded from computational ordering; cycles and dependent nodes remain blocked.
Parts propose definitions; standalone Bodies propose definitions, while Bodies
inside Parts remain part history/results. Shared links retain targets and placements.
Link world frames lacking a native accessor are explicit nulls; local/parent/target
frames are retained for native occurrence resolution in task two.

Recovery planning follows mapped feature → retained editable native feature →
validated dumb body/sheet/curve/point → reported unavailable output. Valid cached
geometry is a candidate, not a freshness guarantee. Touched/invalid dependencies
or blocked cycles make cached output unverified. No failed property snapshot may
silently discard a valid body. This policy applies to every subsequent feature task.

Acceptance: final eight native checks pass with FREECAD_PLUS_PROFILE_SOURCE=1 in
native revision 8746, not installed/payload or new GUI acceptance. Tests verify
nested Parts, Body/Sketch/Pad order, attached sketch/datum references, repeated and
external Links, untouched source bytes/ownership/Undo/property states, deterministic
repeated planning, expressions/cycles, missing links/unmapped objects, all fallback
kinds, touched caches, partial fingerprint failure and FCStd reopen. Reopened Body
Group/Tip/sketch constraints remain; native bidirectional solid differences are zero.
Three Python syntax checks pass. Loaded CadDocument SHA256:
6cab834e58623c6df899f2b8f0c1f4f3ece92d1578b839cc8ef1d98cd4a9e72e;
LegacyConversion SHA256:
f195b3c21d398224e9d090464715f66ac02edc3b50e5d3c8f50929ecd5e4e683;
test SHA256: 0d28665e820ffa8dff2f8b7d819fa0ed279964697a5812764fab3414c1c8d390.
Earlier attempts are not acceptance: synthetic Shape access created caches,
_Body produced an artificial cycle, App::Link lacked getGlobalPlacement, fixture
Box parameters recomputed immediately, and BREP reopen bytes differed despite
identical geometry. Final checks address each with raw stored Shape reads,
structural-link filtering, explicit local link metadata, touch fixtures and actual
geometric comparison. No assertions are skipped.

Owner DOCX remains 88 pages; only final page 88 changes and is visually inspected.
Other ZIP parts and native numbering remain unchanged. DOCX SHA256:
d472ab8b02d1e7cfe5b9770896c870c928fcfc41b24aa011f113c81998d45c8e.
Task profiles/logs/captures/render output/fixtures and 240 generated bytecode files
are removed after these summaries. Native builds and installed GUI validation are batched
with later integration, not claimed here. Source milestone d73a45c1345b4332aca173b9fe479112f4bbd85c is committed,
pushed without force to origin/main and exact remote branch verified. The final
documentation receipt is published separately; no release or owner build is created.

Exact next task: use the recorded proposed boundaries to convert Models definitions
and Part Tree occurrences, preserving the permanent master, native/shared identities,
all local/world placements, nested/external definitions and legacy originals.
Keep fallback candidates and failures visible; do not execute tasks 2–12 without
their subsequent owner task request. See tests/LegacyConversionPlan.md and the
canonical roadmap's twelve-task sequence.

## October 6 constraint palette lingering tooltip fix

The current delivered payload reproduces a native tooltip still visible on entry
into constraint execution. ConstraintPaletteGui now hides its native tooltip
synchronously before solving, on action refresh and on close; old buttons hide
before deferred deletion. Qt retains tooltip ownership, native icon/text behavior,
and the separate one-second pointer-travel grace remains unchanged.

Final installed native palette suite passes 19/19 without source overlays,
including actual Qt tooltip/button events, persistence on/off, immediate close,
retired buttons, Undo, native viewport picks/drag, and save/reopen. The first full
attempt is not acceptance: its new persistence-off fixture used a wrong preference
accessor, corrected before the passing final suite. The preceding payload fails
the immediate-hide regression. Both Python syntax checks pass. The owner DOCX
remains 88 pages; only page 82 changes, visually inspected, with all non-document
ZIP parts and native numbering retained.

Increased-scale immediate-hide/corridor checks pass 2/2 at DPR 3.0. Three native
checks launched through the actual saved desktop shortcut pass, including native
viewport click/Escape/empty/drag and icon/tooltip parity. Its target and working
directory are saved/reopened and verified to the useful owner payload:
`C:\Users\GAMING-PC\Documents\_temp\freecad\test-builds\freecad_plus_2026-10-06_palette_dismissal_payload`.
This is compatible Python staging; compiled native revision 8746 is unchanged.
All 15,121 prior inventory files are hashed; only ConstraintPaletteGui.py differs.
Durable release-info/payload-manifest retain source/native provenance and the
historical preceding acceptance. Generated bytecode (258 files and the source
fixture cache) is removed. The unused preceding medium-ribbon payload is deleted
after a process audit. Raw task validation is removed after these summaries.
Owner physical feedback remains separate. Coherent source milestone and verified
origin/main publication are recorded in payload release-info.json. No unrelated
feature or broader unqualified viewport acceptance is claimed.

## October 6 larger medium ribbon icons

Current owner payload:
`C:\Users\GAMING-PC\Documents\_temp\freecad\test-builds\freecad_plus_2026-10-06_medium_ribbon_icons_payload`.
PlusRibbon medium icons grow from 20 to 32 logical pixels and medium buttons from
38 to 42 pixels high; the shared grid minimum is 86 pixels for two medium rows.
Large/small icon sizes, icon-only medium/small presentation, native action icons,
tooltips, enablement, accessibility and user toolbar/dock state remain retained.
Large captions/group dividers keep complete fitting and scrolling behavior.
This is compatible Python staging on the unchanged native 8746 engine; no costly
native rebuild is performed for this presentation change.

Five installed checks pass: actual medium icon painting, all seven Design tab
captions/dividers, exact Modeling layout, common/Home actions and actual native
Box pointer/Cancel with object identity preservation. Two increased-scale checks
pass at DPR 3.0; two checks launched through the actual saved desktop shortcut pass.
No application overlays are used. Normal painted bounds grow from 20.67x16.67 to
26.67x25.33 logical pixels (native artwork retains its transparent margins); the
requested icon slot is 32x32 and fits the 76x42 button. DPR 3.0 painted bounds are
26.67x25.67 versus the previous 19.67x16.0. Native captures of all seven tabs at both
scales are inspected. Earlier width-only threshold attempts are not acceptance;
QIcon reports the correct 32px size, and final paint checks prove increased area,
growth on both axes and unclipped bounds. The preserved native artwork is not cropped.

The existing desktop shortcut is saved/reopened with the new FreeCADPlus.exe target
and payload working directory, then actually launched for the accepted checks.
Complete prior payload inventory is verified: all 15,121 existing files hashed,
only Ext/freecad/gui/PlusRibbon.py differs, and all native binaries are unchanged.
Owner DOCX requirements/actual acceptance are synchronized; its final 88-page
render changes only pages 56 and 88, both visually inspected. All other ZIP parts,
native numbering and surrounding pagination are retained. Durable release-info
and payload-manifest record actual checks, UI hash e0f87561d830a383b84b4f622f9c1f124eb7fade948cd407facb0900befc3a0b,
source/native provenance and final origin/main publication. Raw task validation,
267 runtime bytecode files and the source-test cache are removed. The preceding
unused sketch-selection payload is deleted after an owner-process audit; current
payload, native build and useful dependencies/toolchain remain. Preserve earlier
sketch/quiet-probe and broader GUI limits below; no deferred family is qualified.

## October 6 sketch point selection and quiet feasibility probes — native delivery

Both reported defects reproduce on the preceding Modeling payload. Two actual
plain point clicks retain Vertex3 and Vertex4, and repeated hypothetical coincident
endpoints print geometry failures and invalid-solution warnings without any applied
constraint. Source milestone 8746c1076071a7b9decff07577b6a163a0f76ee9 is committed,
pushed to origin/main and remote-verified.

Plus Design native plain picks now replace selection; Ctrl/Shift retain native
multiselection, plain empty clicks clear and modified empty clicks retain it.
Repeated plain clicks keep the one selected item. Persistent Selection still
controls operation retention. Drag, box, context picks and Classic remain scoped
separately. Only the cloned diagnostic Sketch is quiet; hypothetical failures keep
their native status while actual invalid operations still report diagnostics.
No persisted property/document identity or geometry algorithm is changed.

One grouped incremental Release/x64 ALL_BUILD is complete. Its first wrapper hit
the 90-minute deadline before SketcherGui/PartDesignGui finished; process/timestamp
audits rejected that run as acceptance. No original workers remained. Continuing
the same tree with retained objects and a 120-minute guard passed ALL_BUILD; this
was not a clean rebuild or duplicate concurrent build. Native compiled App.Version
identifies 8746c1076071a7b9decff07577b6a163a0f76ee9. All 66 changed native binaries,
including core and Sketcher consumers, are staged with verified copy hashes.

Current owner test payload:
`C:\Users\GAMING-PC\Documents\_temp\freecad\test-builds\freecad_plus_2026-10-06_sketch_selection_payload`.
It retains the preceding Python/UI configuration, including startup/layout,
plane highlighting, palette icons and revised Modeling ribbon. Acceptance uses
installed application modules, with FREECAD_PLUS_PROFILE_SOURCE=0:

- Focused native click/quiet-probe/point-drag checks: 3/3.
- Complete TestConstraintPaletteNative suite: 18/18 distinct checks.
- The same three focused checks at QT_SCALE_FACTOR=2: 3/3.
- Actual saved desktop-shortcut launch of the three focused checks: 3/3.

Actual native mouse events cover sequential and repeated picks, Ctrl/Shift,
modified/plain empty clicks, point press/move/release, Escape and palette clicks.
Selection/probe checks preserve geometry, constraints, UndoCount and solver state.
Native drag and constraint operations cover Undo/Redo and FCStd save/reopen with
retained Sketch identity. The invalid-operation fixture deliberately prints live
solver errors, proving they remain enabled. Native action icon/tooltip parity and
the captured palette are verified; no global console suppression is used.

Broader Design-selection audit: 18/19 checks pass. The unobscured-viewport check
cannot locate a widget at its pick point (666,611), although its viewport, window
and screen bounds contain it and the window is visible/exposed at DPR 1.5.
Visible-window, screen-bounded and foreground attempts remain unsuccessful, not
acceptance. Experimental fixture changes were removed; original assertions remain.
The first audit also exposed a sibling-test import failure; the native harness now
adds selected test directories, not application overlays. Exact remaining step:
rerun TestDesignSelectionNative.test_actual_sketch_click_single_connected_tangent_escape_and_empty_space
in a desktop session where QWidget.widgetAt identifies the unobscured viewport.
Do not infer broader workbench or physical owner acceptance from this delivery.

The existing desktop FreeCADPlus.exe - Shortcut.lnk is saved, reopened and verified
with target `<payload>\FreeCADPlus.exe` and working directory `<payload>`, then
actually launched for the accepted tests. Owner DOCX is synchronized, rendered to
88 pages and page 88 visually inspected; only word/document.xml changes, with all
other ZIP parts, owner structure and automatic numbering retained. Canonical DOCX
matches the inspected proposal byte-for-byte. UI_UX_SPEC and regression procedure
retain the source requirements and native validation contracts.

Full inventory verification hashes all 15,121 prior files and confirms exactly
66 expected native changes, no missing files and no other application changes.
All current Python UI hashes are retained. Runtime-generated bytecode (1,020
candidate files and four source-test caches) is removed. Raw sketch-selection
validation is deleted after durable summaries. The two obsolete Modeling/palette
payloads are removed after checking no owner process uses them. Useful candidate,
incremental native build, dependencies and toolchain remain in test-builds.

Durable release-info.json and payload-manifest.json in the current payload record
actual native/test/DOCX/shortcut hashes, inventory and cleanup, plus the final
acceptance milestone's commit and origin/main publication result. Native source
8746 is already origin-verified. Final acceptance/documentation form one coherent
milestone; this is a local owner test build, not a release or deployment. Known BIM,
legacy sketch and protected Windows Temp limitations below remain separate.

## October 6 Modeling ribbon and complete captions

Current owner payload:
`C:\Users\GAMING-PC\Documents\_temp\freecad\test-builds\freecad_plus_2026-10-06_modeling_ribbon_payload`.
PlusRibbon now has the requested Sketch / Modeling / Dress-Up / Transformation /
Primitives / Other groups. New Sketch, Extrude, Revolve, Fillet and Chamfer and
Primitives are large; Sketch secondary buttons are small; other secondary buttons
are medium. Coordinate System defaults to Coordinate System with Plane/Axis/Point
choices. Fillet and Chamfer defaults to Fillet, and Primitives defaults to Box.
Tab remains disabled/unimplemented. Pipe stays available through native commands.

Every tab uses gray #808080 one-logical-pixel dividers between adjacent groups.
Medium/small buttons are icon-only, retaining native tooltips/accessibility and
action state. Large buttons paint their native icons and complete fitted captions
on up to two lines; labels expand rather than elide. Group captions also retain
complete text. Font/style/language changes refresh layout; scroll height grows
with full caption content and horizontal scrolling retains narrow-window access.
Native action routing, geometry, identity, transactions and Classic preferences
remain unchanged. Assembly's preexisting Move Components is restored to its
stale acceptance fixture, without a new Assembly UI change.

Accepted installed checks: ten native ribbon/layout/menu/common-action checks,
three increased-DPI checks (QT_SCALE_FACTOR=2), and three checks launched through
the actual saved desktop shortcut. Default Box uses actual Qt mouse events,
opens the native component primitive task and Cancel restores object identities.
The existing embedded-model check covers Undo/Redo and cadprt save/reopen.
Native captures of all seven Design tabs are visually inspected at both scales;
pixel checks verify gray dividers and rendered large icons, geometry checks prove
caption fit and unclipped vertical viewport. No source overlays are used.

Earlier candidate failures are not acceptance: a stale Assembly fixture lacked
Move Components; the old fixed 170px toolbar assertion conflicted with complete
caption sizing; a test-only QtTest import needed the actual PySide6/2 package.
Visual QA caught the QStyleOption icon alias and it is explicitly copied before
native frame painting. Final accepted checks cover these corrections. The broad
all-installed-mode audit blocks in inherited BIM initialization because
addonmanager_utilities is absent; only its task-owned process is stopped. Do not
claim BIM or every registered workbench qualifies; separately test the explicit
ready Draft/CAM/Part/Drawing subset. Deferred families remain deferred.
The explicit Draft/CAM/Part/Drawing all-tab and Drawing-icon checks pass 2/2;
their mode selector is deliberately restricted in the fixture and is not proof
of the unavailable BIM workbench. Ordinary native application stylesheet parse
warnings remain in these runs; inspected ribbon paint/caption checks pass.

All 15,121 stable preceding payload files are hashed; the only application change
is Ext/freecad/gui/PlusRibbon.py, SHA-256
6679aace81c5072699e19279a00f543b5b4aeda11e7711a5c9be45d007aeaf30.
Native binaries retain embedded revision edf2e742ac92a92005bc3c612980659fbd5be158
and GUI source snapshot e29d2e5; no native compilation was performed. The durable
release-info/manifest records this Python-only delivery separately. The exact
desktop FreeCADPlus.exe - Shortcut.lnk target/workdir is saved/reopened and verified.
The preceding palette payload is retained while the owner's existing process
still uses it; remove it once that session has closed and it is no longer useful.
Do not terminate owner sessions to clean old builds.

Owner DOCX outline, affected native command locations and shared presentation
rules are synchronized. Other ZIP parts/styles/native numbering are retained.
The canonical 88-page render has affected catalog pages 24-26 and presentation /
outline pages 56-59 visually inspected. UI_UX_SPEC and TOOLBARS are synchronized.
Raw task profiles/logs/captures/scripts and DOCX QA are deleted after canonical
summary per owner policy. Push the coherent milestone to origin/main and verify
its remote ref; next owner use is a restart through the updated desktop shortcut.

## October 6 Design Mode toolbar outline

Owner DOCX section 2.1.2.1 now documents the installed Design ribbon using nested
Tab / group / Large Button or Medium/Small Button Cluster / button / dropdown
choice lists. Seven tabs, 168 rendered buttons and 24 dropdowns were read from
the actual installed PlusRibbon Qt grid with isolated settings. Installed
PlusRibbon.py bytes match current source. List order follows visible columns
left to right and cluster rows top to bottom. Modeling's current small clusters,
separate Fillet/Chamfer, Pipe, duplicate Primitive entry and lack of Other group
are recorded accurately; this documentation task does not change application UI.
Assembly now includes the previously omitted Move Components. Tab primitive
remains explicitly disabled/unimplemented. Native action/geometry contracts and
common toolbar placement are retained.

Only the section's outline paragraphs change; preceding/following OOXML content,
all other ZIP parts, styles and numbering definitions remain unchanged. Native
automatic heading and bullet numbering are retained. Canonical DOCX renders to
87 pages (previously 86); outline pages 56-64 and later reflow pages 65-71 are
visually inspected. Prior pages 1-55 and sixteen later pages match the baseline
render exactly. Temporary native inventory, scripts and before/after render QA
are deleted at completion under the owner storage policy. Commit/push this
documentation milestone to origin/main; no new build or desktop retarget is
needed, and all prior product acceptance limitations remain unchanged.

## October 6 artifact relocation and end-of-task cleanup

Owner policy supersedes earlier artifact paths below. Current useful payload:
`C:\Users\GAMING-PC\Documents\_temp\freecad\test-builds\freecad_plus_2026-10-06_constraint_palette_icons_payload`.
The native development tree `freecad_plus_2026-10-06_recovered_workload`, extracted
LibPack under `dependencies`, and NSIS under `toolchain` are retained in the same
test-builds root. CMake configure/generate succeeds after relocating its cache
and dependency paths; no native compilation was performed for this storage task.
Original payload source revision remains 5e12817f8e7210418fab547fdc0de93869bf9c23;
native GUI source snapshot e29d2e5 and embedded native revision edf2e742 remain
unchanged. Durable payload release-info/manifest describe relocation separately.
All 15,121 stable payload manifest entries match their pre-relocation hashes;
only the durable build metadata is then updated to record the new location.

The exact existing desktop FreeCADPlus.exe - Shortcut.lnk was saved, reopened and
its target/working directory verified against the new payload. A real launch
through that shortcut passes three native palette presentation/hover/pointer
tests, without source overlays. Installed module SHA-256 remains
eaa77531e440532eec56870d233cd545ded48e8a33f8efda978ac0a24a4bd502;
Qt DPR 1.5, logical palette 248 by 88, native icons 24 by 24, twenty presentation
mappings. Prior broad-suite limitations and physical owner acceptance remain
separate; relocation does not establish new feature acceptance.

Ten ignored checkout build/validation directories and task-generated Codex
visualization output were moved to the requested validation root for review.
Raw output is discarded after this canonical summary per owner instruction.
Removed four obsolete AppData payload/build directories, empty checkout tmp,
redundant LibPack archive and generated source bytecode caches. Original owner
prompt/context archives, tracked tests, owner documents and preferences remain.
Three known generated fixtures could not be removed: Windows denies enumeration,
ACL reads and deletion even in the approved elevated cleanup. Exact remaining
paths are `C:\Users\GAMING-PC\AppData\Local\Temp\layers_adxj6v8g`,
`C:\Users\GAMING-PC\AppData\Local\Temp\layers_bfsr0rll` and
`C:\Users\GAMING-PC\AppData\Local\Temp\palette_sx6go1wk`.
Do not claim these three directories were deleted or modify unrelated Temp data.

Shared runner output paths are confined to the prescribed roots; TEMP/TMP point
to the validation task and Python bytecode writes are disabled for GUI runners.
PowerShell parsing and path escape/sibling rejection checks pass.
The updated shared runner also passes one native constraint conversion/Undo/
save-reopen case (process exit 0); its palette_ fixture is created inside the
validation task directory and no source bytecode cache is left in the checkout.
Owner DOCX requirement is synchronized: 86 rendered pages, changed pages 70-76 inspected,
all other package parts and automatic numbering retained. Raw validation and
render artifacts are deleted at task completion. Source policy/tools/docs form
one coherent milestone; push only origin/main and verify its remote ref.

Next steps: owner feedback uses the relocated shortcut; future tasks create a
fresh subdirectory of `validation`, summarize results here and remove their raw
output before handoff. Reuse the retained development build for batched native
changes. The three Windows-protected fixtures above need an account with access.

## October 6 constraint palette icons and native tooltips

Active owner change: replace sketch-edit contextual palette word buttons with
native toolbar icons and identical native hover tooltips. ConstraintPaletteGui
copies the registered native QAction icon/full rich tooltip and follows its
presentation changes through a widget-owned Qt slot. Native activation and
native enabled state are not rebound: existing eligibility, batch constraints,
dimension dialogs, construction and separate Driving/Reference semantics remain.
Icon rows wrap in logical pixels using the native main-window icon size. Retain
accessible names; disabled reasons remain accessible and appear in the status
bar while their hover tooltip stays identical to the native toolbar.

Accepted installed evidence: packaged-presentation 2/2, packaged-native full
TestConstraintPaletteNative 15/15, scaled GUI presentation/hover/pointer 3/3 with
QT_SCALE_FACTOR=2. Actual desktop shortcut first smoke 3/3, including native
sketch pointer events, icon/tooltip parity, Equal click and Undo, persistence,
disabled reason hover, narrow viewport wrapping and native presentation refresh.
Final shortcut smoke passes 3/3 and records the actual installed module under
the new payload, matching source hash, Qt DPR 1.5, logical palette 248 by 88
and 24 by 24 icons. Twenty independent native-command presentation mappings
match, including shared native toggle icons and the concentric center constraint.
The scaled capture is 744 by 264 versus normal 372 by 132; its three checks pass.

Owner DOCX is synchronized. Its 86-page canonical render matches the inspected
proposal; only page 81 changes from the prior accepted render. All other DOCX
ZIP parts/styles/automatic numbering are unchanged. An existing normal Writer
session briefly locked the document; it was preserved, the lock cleared, and
canonical bytes were checked against HEAD before replacement to avoid losing
intervening owner edits. No owner session was terminated.

Compatible Python owner payload:
C:\Users\GAMING-PC\AppData\Local\FreeCADPlus\freecad_plus_2026-10-06_constraint_palette_icons_payload
All 15,121 prior stable manifest entries were hashed: only the installed
ConstraintPaletteGui.py changed, hash
eaa77531e440532eec56870d233cd545ded48e8a33f8efda978ac0a24a4bd502.
Native binaries remain unchanged, with embedded revision
edf2e742ac92a92005bc3c612980659fbd5be158 and native GUI source snapshot e29d2e5.
The prior plane-selection/startup fixes are retained. Desktop exact name
FreeCADPlus.exe - Shortcut.lnk is saved/reopened and target/workdir verified.

Exact current source/publication revision and final inventory are recorded in
the new payload release-info.json and build-palette-icons/delivery-summary.json.
Commit this coherent milestone and push origin/main without force; verify its
remote ref before handoff. Next product acceptance is physical owner feedback
through the updated desktop shortcut. Physical owner feedback
remains separate; previous failed legacy sketch-suite qualification is unchanged
and is not relabeled as current acceptance. Deferred families remain deferred.

## October 6 New Sketch origin plane picking

Active owner request: clicking an origin plane must select/highlight only that
plane. Native reproduction on the previous startup payload resolves viewport
hits to Component/Origin. instead of Origin/XY_Plane.; all siblings highlight.
The Layers gate wrapped the coordinate-system child Group and broke native
getElementPicked/getDetailPath identity checks. DesignLayersGui now retains
that native container, removes an earlier gate if present, and gates its
individual descendants. No geometry, placement, ownership or identities change.

Accepted packaged-plane-picks5: all six actual Qt viewport picks (XY/XZ/YZ in
both New Sketch commands), exact leaf selection, task selector update, Cancel
object/visibility restoration and Base layer datum hiding. Captures inspected.
A native regression on the previous payload fails at XY leaf hit resolution.
The broad packaged-regression run is NOT acceptance: its legacy Datum Plane
fixture accesses missing PlaneTask.orientation_mode and leaves a task open,
with cascading sketch/selection errors. Clean-process focused acceptance passes 10/10, including native attachment,
Cancel, Undo/Redo, save/reopen and Plus New File/Sketch viewport curves. The
same PlaneTask.orientation_mode error reproduces on the unchanged previous
startup payload in legacy-baseline-old; it predates this correction.

Owner DOCX requirement updated, all other ZIP parts retained. Render remains
86 pages; changed/repaginated pages 67-75 visually inspected, all others exactly
match the prior accepted render. Compatible Python correction staged in a new
plane_selection_payload; no C++ changes or new native compilation required.

Stable inventory verification hashes all 15,121 prior manifest entries: only
Ext/freecad/gui/DesignLayersGui.py differs. Desktop target/workdir are saved,
reopened and verified for the new payload. Actual shortcut plane/Layers
acceptance passes 11/11 in actual-shortcut-interior, with strict zero-radius
interior pick patches, isolated preferences and no source overlays. All six
plane captures were inspected; siblings retain normal colors. Ten focused
sketch checks plus eleven shortcut checks cover 20 distinct methods. The first
tolerance-dependent shortcut fixture remains as failed evidence. No application
change was required for that fixture repair. No native GUI Python exceptions
were found in the accepted shortcut log; inherited stylesheet warnings remain.

Delivered launcher:
C:\Users\GAMING-PC\AppData\Local\FreeCADPlus\freecad_plus_2026-10-06_plane_selection_payload\FreeCADPlus.exe
Desktop FreeCADPlus.exe - Shortcut.lnk was saved/reopened and its exact target
and working directory verified, then actually launched through ShellExecute.
Native embedded revision remains edf2e742ac92a92005bc3c612980659fbd5be158; native
GUI DLLs are reused from the e29d2e5 startup snapshot. The changed Python module
hash is 8341d4685cc4f81205936625b247a2b8fb8bb5a344c4fe71508c8283bba747b1.
Exact current source/publication revision and final manifest are recorded in the
new payload release-info.json; build-plane-highlight/delivery-summary.json
records acceptance and limits. Push this coherent milestone to origin/main and
verify its ref before handoff, without force. Previous startup payload remains
available unchanged.

Next product acceptance: physical owner feedback using the updated shortcut.
Full legacy workflow qualification still needs migration/cleanup of its stale
Datum Plane test fixture; the failed 43-check run is not accepted or concealed.

## October 6 startup and workspace correction

Authorized objective: remove visible startup theme/workbench transitions, restore
idle New File/Open and central recent-file cards, default Tasks to the right and
retain user-customized panel/toolbar locations across restarts.

Source: StartupProcess seeds native theme/docking defaults before native managers
read them, removes only Tasks from old overlay memberships once and exposes the
window after configured background workbenches. ComponentNavigator registers its
named dock before restore and applies the initial split only without saved state.
PlusRibbon installs synchronously, imports only Part/PartDesign for Home and
updates visibility without relocating toolbars. All Plus bars are movable and
floatable. The Selection event filter ignores non-widget layout objects.

Completed evidence: incremental FreeCADGui compile and two concrete native
startup repair retries exit 0. Real cold startup, customize/save and cold reopen
pass on the native build without --hidden or source overlays. Final native
startup actions/recent files/docking regression: 13/13, including real card
opening and valid datum-plane OK events. Selected Home/tab/Classic/native
General regression: 6/6. Three packaged Plus/Classic preference cold phases pass.
Packaged fresh startup, isolated actual-owner-profile migration, custom-layout
save and actual desktop shortcut cold reopen all pass. The latter restores Tasks
on the customized left, Components on the customized right, floating Attributes,
and Common/Selection/Layers toolbars at their saved areas. All five changed
installed modules and three rebuilt native DLLs match their tested source/build
hashes. Build labels, logs, captures and limits: build-startup-fix/delivery-summary.json.

Owner DOCX requirements are synchronized. Its 86-page render preserves exact
PNG content on pages 1-63; affected/repaginated pages 64-86 were visually
inspected, including requirement pages 64, 70 and 71. Other DOCX ZIP parts,
styles and native numbering are retained.

Delivered launcher:
C:\Users\GAMING-PC\AppData\Local\FreeCADPlus\freecad_plus_2026-10-06_startup_workspace_payload\FreeCADPlus.exe
Desktop: C:\Users\GAMING-PC\Desktop\FreeCADPlus.exe - Shortcut.lnk
Standard helper saved/reopened and verified exact target/working directory;
the saved .lnk was actually launched through Windows ShellExecute. The old
recovered workload payload remains available for rollback. Native embedded
version revision remains edf2e742ac92a92005bc3c612980659fbd5be158; it is not
relabeled as this later startup-source commit. Current source/native hashes,
manifest and origin publication receipt are recorded in the new payload.

Earlier failed runs remain available and are not counted as acceptance.
Existing stylesheet parse warnings remain visible in native logs. Recorded
cold-process elapsed times include validation and shutdown, so they do not
establish a controlled comparative speed benchmark. Eager specialist activation
was removed and final light startup/recent-file/Tasks captures were reviewed.
The earlier recovery 89/55/26 qualification remains historical to its payload;
this startup delivery uses focused acceptance. Geometry, identities, parent
placements and deferred families are unchanged. Next action: physical owner
startup and layout feedback using the updated shortcut.

## Owner requested archive publication

The owner requested logical commits and origin publication of the remaining
untracked files. The original October 3 workload archive contains ten prompt
backups and three JSON receipts; JSON parsing and all recorded prompt SHA-256
checks pass. Original files are preserved byte-for-byte, with a README clarifying
historical receipt limits and preventing duplicate execution or enqueueing.
The owner DOCX records this administrative status; its affected final page is
rendered and visually reviewed before publication. This commit changes no
implementation or build. The delivered test payload remains the validated
b75ba0252f19e904d436236602dcfe8a9a2d12de source snapshot. Publication uses
origin/main without force, followed by exact remote branch verification.

## Recovery item 7 completed grouped test-build delivery

Selection, Design Layers, Contextual Constraint Palette and all six Move
workflows pass final native packaged acceptance. Earlier source milestones are
now integrated and delivered through the final individual owner prompt; earlier
queue entries are not represented as submitted by the originating conversation.

| Gate | Actual evidence |
| --- | --- |
| Native build | Retained fresh ALL_BUILD: exit 0, 6212.578s; required GUI capture repair/retry: exit 0. No native .cpp/.h/.pyi changes since 8890fd91a3. |
| Incremental preparation | FreeCADGui_Resources exit 0; exact current packaged Python/resources. This item reuses the grouped engine, not a second fresh compile. |
| Packaged full | packaged-delivery-final-full-accepted: 89/89, system DPR 1.5. |
| High DPI | packaged-delivery-final-high-dpi-accepted: 55/55, measured DPR 3.0. |
| Saved desktop link | shortcut-delivery-accepted: 26/26, launched the saved .lnk through Windows ShellExecute. Runtime AppHome and working directory are the exact payload. |
| Native/runtime identity | Both Sketcher diagnostic/driving APIs available. Twelve app modules inside AppHome match source hashes; no application overlays, skipped suites or harness errors. |
| Visual review | All six 360-logical-pixel compact Tasks views, real axis/plane/ring/pivot captures and opaque framebuffer reviewed; final owner DOCX affected pages rendered and inspected. |
| Shortcut verification | Existing standard procedure executed, saved .lnk reopened; exact TargetPath and WorkingDirectory match the launcher/payload. |

Payload/launcher:
C:\Users\GAMING-PC\AppData\Local\FreeCADPlus\freecad_plus_2026-10-06_recovered_workload_payload\FreeCADPlus.exe
Desktop link:
C:\Users\GAMING-PC\Desktop\FreeCADPlus.exe - Shortcut.lnk
Launcher SHA-256: 65f9ece602e348bb6fa1a3684686758f09934b65ea50206a11c20351332bf1eb.
Embedded compiled revision: edf2e742ac92a92005bc3c612980659fbd5be158;
native source/capture snapshot: 8890fd91a3bf6fbadf31511107cd087f7d77c9ef.
App.Version: 26.3.0dev, Git count 49278; Qt 6.11.1, Python 3.14.6.
Native FreeCADGui.dll SHA-256:
d6dc8084d56d847389a52e94d83d455716050a9b69b921c0a9d14b6d996e9051.
Final Python/source/document commit and full stable file inventory are recorded
separately in payload release-info.json/payload-manifest.json. The compiled
version is not relabeled with a later Python/document commit.

Final repairs: guarded 100ms Escape checkpoint clears late native reselection;
subsequent viewport/tree/palette/control clicks invalidate it. Native fixtures
settle workbench/edit/MDI activation, dismiss an intercepting notification via
actual clicks, assert an unobscured receiver and unchanged sketch geometry,
and pick handles at Quarter's exact rounded Qt-to-Coin device pixels. Camera
only exposes the Z ring; no direct placement/pivot write substitutes interaction.
Actual tests cover sibling-only parent editing, both shared occurrences,
implicit descendants, outside-parent references, native safeguards, no-op,
Apply/OK non-repetition, Cancel, real gestures, Undo/Redo and FCStd/cadprt reopen.
Unsuccessful finish/cancellation hypotheses were removed; retained manipulator
application behavior is unchanged. Failed diagnostic/earlier snapshot runs remain
in build-recovery-delivery/acceptance and are not counted as final acceptance.

Evidence is retained in build-recovery-delivery (ignored artifacts), copied into
payload validation, and identified in the payload manifest. Owner DOCX numbering,
styles and all non-document XML ZIP parts are preserved. Publication is origin/main
only, without force; exact final commit and remote branch verification are in
payload validation/publication-receipt.json and release-info.json. Earlier pushed
milestones through e0981cc1ce328bbf7814ee8dde47c982bcd228ae remain published.
This is a local incremental grouped test build, not a release/deployment.
At item 7 delivery, ai-instructions/queue was preserved and excluded from commits.
The subsequent owner-requested archive publication above supersedes that status.

No implementation/build/DOCX/shortcut gate remains for these seven recovered
items. Next action is physical owner feedback using this shortcut on real work;
it is separate from the completed automated native event acceptance. Copy,
Sketch Freedom/Constraint Repair, Interactive Feature Handles, Broken Reference
Repair and other selection families remain deferred; do not start them or rerun
completed recovery prompts automatically.

## Earlier item 6 integration reconciliation

All four groups and six Move workflows are implemented; no placeholders or new
feature families are introduced. Audit covers native Selection/preselection/box
and command-gate intersection, Design-only lifecycle, layer metadata/visibility
and independent sketches, pointer corridor/one-second timer/disabled tooltips,
cloned solver diagnostics and committed-invalid driving batch semantics, exact
Move frames, shared-parent edits, guards, previews, reset and native event paths.
Native CMake sources, SketchObject.pyi bindings/header/implementation and Python
consumers are linked; the prior native build and packaged tests establish their
then-current snapshot. No native API is claimed from a source-only fallback.

Reconcile the four pending feature-related files: Selection Escape toolbar,
palette/native Selection/window fixtures. A nested deferred-clear race is repaired
in DesignSelection.py: the final queued clear must check the originating toolbar
lifecycle/event generation, not just its outer callback. Native cancellation is
not consumed and active Move drags keep their own Escape priority. Add a native
regression for superseding click/mode exit; it remains unexecuted until item 7.
Quick Python callback ordering checks pass 4/4 (valid, later click, mode exit,
changed document) and syntax passes eight affected Python files. These checks
use a controlled scheduler and are not Qt/native input acceptance.

Exact item 7 plan is tests/RecoveredWorkload.md: full 89 checks, high-DPI subset
55, source application hashes/no overlays, native API availability, six compact
Tasks, real axis/plane/ring/pivot/collector events, owning-file guards, geometry/
identity/parent invariants, Undo/Redo and FCStd/cadprt, cleanup, DOCX and actual
saved desktop shortcut launch (Selection+integration smoke 26). Retain prior
packaged-final 88/88 evidence and failed/partial runs; do not count them as passes
of the new assertion snapshot. No slow build, packaged suite or shortcut runs here.

Owner DOCX integration note and canonical requirements/summary are synchronized;
numbering/styles/other DOCX package parts are preserved. Rendered affected pages
are reviewed under build-recovery-integration/owner-docx-review. The untracked
queue is preserved/excluded. Exact next step: await item 7 prompt; inspect source,
existing build/payload and evidence before grouped acceptance/delivery. Maintain
batching and report compiled revision separately from later Python/docs commits.

## Earlier item 5 Interactive/pivot source milestone

Execute this individual item only; preceding Move milestones remain retained.
Native view-owned arrows/planes/rings and scoped viewport Escape filtering provide
real gesture input. Default axes/pivot are parent-aligned and group-centered;
Edit Pivot never changes component placements/Undo. Movement previews compose
against baseline and release does not commit. Apply uses shared atomic sibling
placement guards and resets/recreates or removes the manipulator per persistence.
Numeric active-handle input and explicit snap-off defaults remain intact.

Earlier packaged-final passes Interactive 5/5. The focused packaged-high-dpi-pivot-
retest passes 5/5 at DPR 3.0, including actual native mouse press/move/release,
Escape and pivot-edit events. Current Move core/task/manipulator application hashes
match the accepted payload. The pre-existing Interactive fixture correction is
included in this item: pan camera only, ray-pick actual unobscured in-screen
handles and dispatch real Qt events; never substitute direct placement writes.
Its successful native event captures are visually reviewed.

This item extends the same five cases with actual plane/ring gestures, default
pivot recreation, OK-after-Apply without repeat and sibling/descendant native
Undo/Redo plus FCStd/cadprt round trips after actual events. Syntax checks pass;
NEW ASSERTIONS HAVE NOT RUN NATIVELY. Defer their runtime execution and costly
build/packaged/high-DPI acceptance to item 7. The earlier 5/5 runs are evidence
for their then-current tests, not the added assertions. Owner DOCX is synchronized,
with other ZIP parts/numbering/styles preserved; affected rendered pages are
visually reviewed under build-recovery-interactive/owner-docx-review.

Preserve remaining pre-existing Selection Escape source, palette/Selection/window
fixtures and untracked queue. No new build or shortcut delivery is made. Exact next
step: await item 6 integration reconciliation; review preserved dirty changes and
native evidence before edits. Item 7 must repeat all updated Move suites and real
axis/plane/ring/pivot events, camera/cleanup, persistence, save/reopen and final
high-DPI/shortcut acceptance. Deferred feature families remain outside scope.

## Earlier item 4 Align Coordinate Systems source milestone

The individual frame-alignment prompt authorizes this item only. Preceding
Rotate/Point workflows and the item 3 Align Axes source milestone are retained;
do not replay them or run later items without individual follow-up prompts.

The retained shared task offers existing origins/datums, explicit Parent frames
and expandable Origin/Z/X definitions. The core projects X perpendicular to Z,
derives a right-handed basis and applies Target * inverse Source as one rigid
parent-relative group delta. Native reference paths preserve displayed transforms;
scaled/reflected/nonfinite/incomplete inputs are rejected. Triads/resolved values,
baseline previews and shared Apply/OK/Cancel/persistence/guards remain intact.

Earlier packaged-final evidence passes TestMoveComponentsFrames 5/5 without source
application overlays/skips. Current Move core/task hashes match that accepted
payload. Installed frame task captures are visually reviewed. Five existing cases
now additionally check repeated baseline previews, both displayed parent frames,
OK after Apply without repeat, all siblings/descendants in both FCStd/cadprt round
trips and preview/Cancel without mutation. Syntax checks pass; these new assertions
have NOT run natively. Defer changed-test native/runtime acceptance and the costly
build/packaged delivery to item 7. Earlier 5/5 is not new-assertion acceptance.

The owner DOCX frame paragraph is synchronized; all other DOCX parts, numbering
and styles are preserved. Affected pages are rendered/visually inspected under
build-recovery-frames/owner-docx-review. Preserve pre-existing dirty Selection
Escape/palette/Interactive fixture files and the untracked queue. No new build,
desktop shortcut or owner-ready delivery is claimed. Exact next step: await item 5
Interactive/pivot, inspect existing source and native event evidence before edits.
Item 7 must run both strengthened Axes/Frames suites plus all integration gates.

## Earlier item 3 Align Axes source milestone

The individual Align Axes prompt is authorized; stop at its coherent commit/push.
Rotate is verified complete. Point to Point already exists from the earlier
omnibus-authorized preparation, and packaged-final reports 4/4 passing checks;
its source hash matches the accepted Move core/task modules. Do not replay either
prerequisite or start items 4–7. Their individual follow-up prompts are required.

Align Axes uses the existing shared task, baseline located-axis snapshots,
minimal rotation, closest Target point / fixed Source anchor policy and explicit
Target reversal. Native line/circle/cylinder extraction preserves occurrence paths;
parent-relative sibling commit, repeated parent previews and driven guards remain.
The earlier packaged-final suite passed 5/5 Align Axes checks, with no source
application overlays/skips. Existing installed task captures are reviewed.

This item adds assertions to those same five tests for parallel/coincident no-op,
stable antiparallel roll, repeated baseline previews and FCStd/cadprt round trips
of both siblings and their implicit descendant. Syntax and accepted application
module hashes pass quick checks. The changed test assertions have NOT run in a
native runtime; defer that acceptance and the costly build to item 7 explicitly.
Owner DOCX preserves other ZIP parts/numbering/styles; affected rendered pages
are visually reviewed under build-recovery-axes/owner-docx-review.

Preserve the five pre-existing dirty Selection/palette/Interactive fixtures and
Selection Escape source change listed below, and the untracked queue directory.
No build, desktop shortcut or final delivery is made by this item. Exact next
step: await item 4 Align Coordinate Systems; inspect existing source/evidence
before any changes. Item 7 must run updated TestMoveComponentsAxes (five cases)
including both round trips and all combined native/packaged/high-DPI gates.

## Earlier scope handoff: recovery item 1

The owner superseded the omnibus execution instruction: stop after Rotate and
await separate prompts for items 2–7. Rotate was already implemented; it has not
been replayed. Native and packaged-final evidence passes all 8 updated Rotate
checks and all 12 Translate checks, with actual task controls, shared-parent
placements, Undo/Redo and FCStd/cadprt reopen. AppHome/module hashes are verified,
with no application source overlays or skips. Installed Rotate top/bottom task
captures are visually reviewed. The owner DOCX Rotate acceptance paragraph is
updated without changing numbering/styles or other package parts; affected pages
are rendered and inspected in build-recovery-rotate/owner-docx-review. The renderer
produced 84 pages; pages 82–83 are visually reviewed. Current Move core/task
SHA-256 values match the accepted packaged-final payload.

Evidence root: C:/Users/GAMING-PC/.codex/visualizations/2026/10/06/
01a10f79-1a93-7be0-a261-96a6b7e9c425/acceptance. packaged-final/results.json
reports all 88 checks passing, including Rotate 8/8 and Translate 12/12.
The later packaged-accepted rerun has no final results/validation.done; its
progress records Rotate 8/8 and Translate 12/12 plus earlier suites. Its runner
session no longer exists and no FreeCAD.exe process is present at the stop audit.
Do not count that incomplete rerun as final acceptance or restart later suites.

Earlier omnibus-authorized preparation, native build and staged payload are
preserved. Later uncommitted Selection Escape and test-fixture changes remain in
DesignSelectionToolbar.py, TestConstraintPalette.py, TestDesignSelection.py,
TestMoveComponentsInteractive.py and TestWindowSelection.py. ai-instructions/queue
is preserved and excluded. No owner desktop shortcut or final manifest has been
delivered. No final build readiness claim is made.

Exact next step: wait for the owner's item 2 prompt; verify existing Point to Point
source/evidence before any changes. Subsequent integration/final delivery still
needs reconciliation of the preserved dirty fixes, final combined high-DPI suite,
DOCX final acceptance and verified actual desktop shortcut launch. Execute those
only when the corresponding individual prompt is supplied. Historical continuation
notes below describe the earlier plan and do not authorize resuming it.

## Earlier recovery gate: native acceptance repairs, October 6

The new grouped Windows x64 Release ALL_BUILD completed successfully in
6212.578 seconds (configure 588.953 seconds). Build and configure logs/results
are under visualization task `01a10f79-1a93-7be0-a261-96a6b7e9c425`.
Actual build home is `C:/Users/GAMING-PC/AppData/Local/FreeCADPlus/freecad_plus_2026-10-06_recovered_workload`.
Runtime version identifies compiled revision `edf2e742ac92a92005bc3c612980659fbd5be158`;
later Python fixes are refreshed through FreeCADGui_Resources and checked by SHA-256.

The initial installed 86-check run exposed native mapped sketch token handling,
dialog deletion lifecycle, fixture mode/ray-picking/vertex/width assumptions and
an incorrect solver equality-cycle redundancy oracle. These are repaired.
Focused native evidence: `native-events-retest` passes Selection 18/18 and
Interactive 5/5, including real rendered handle mouse/Escape/pivot events.
`native-integration-palette-fix` passes palette 14/14 and integration 5/5,
including outside-parent viewport point picks, six task layouts at 360 logical
pixels, external-parent owning-file enforcement and owning-document deletion.
No application source overlays or skips; launched AppHomePath and module hashes
match the actual build. System DPR is 1.5. Earlier failed logs are retained.

The graphics blocker is resolved: Qt paintGL called the inherited asynchronous
redraw scheduler when it needed to fill a capture framebuffer synchronously.
QuarterWidget now paints that framebuffer immediately, preserving the ordinary
frame-rate scheduling and restoring automatic-redraw state with a scope guard.
The unsuccessful overlay/background hypotheses were removed. Native regression
checks the actual Qt framebuffer's face pixels, not saveImage's separate action.
`native-capture-and-entry-retest` passes all seven integration checks, including
real Assembly tab/button events and Part Tree Move action; the clean screenshot
is visually inspected. The full repaired 88-check installed run initially passes
87/88; a palette mouse fixture fitted its camera before queued layout and projected
the click to (0, 0). After waiting for layout it passes 14/14. A second full run
passes the other 70 checks but the Selection click fixture searches GL widgets
across inactive tabs. That fixture now waits for layout, targets the active MDI
document and asserts its projected click is inside the viewport. The focused
Selection rerun is running; full packaged acceptance will repeat all 88 checks.
Native repair build initially hit MSVC C1001 in generated qrc_translation.cpp;
the unchanged resource retry with CL_MPCount=1 passed in 51.859 seconds.
All diagnostic-only captures and failed build/test logs are retained. Windows
Computer Use app approval timed out, but native Qt evidence now passes directly.
The staged test payload is now
`C:/Users/GAMING-PC/AppData/Local/FreeCADPlus/freecad_plus_2026-10-06_recovered_workload_payload`.
Its repository NSIS launcher was compiled successfully; staging copied 15034 files,
1,636,583,721 bytes. `packaged-final` passes all 88 native checks at DPR 1.5 through
FreeCADPlus.exe, with exact AppHomePath, payload working directory and module SHA
verification. That predates the further Escape repair below; final rerun is active.

At DPR 3.0 the first run passes 53/54; the box fixture did not establish actual
Design mode and requested an offscreen window. Fixtures now activate Design,
wait for real layout, target the active MDI and fit the physical screen. The next
run exposes native Sketcher Escape reselecting its parent after initial clearing,
and an Edit Pivot gesture ray-picked behind a small-screen task overlay. Selection
now clears the native cancellation result on the next event turn, guarded against
later clicks/other documents. The drag fixture pans only the camera and picks
unobscured, in-screen native handles; it never writes pivot/component properties.
Focused DPR 3.0 reruns pass palette 14/14 and Interactive 5/5 (real pivot events).
The complete final DPR 1.5 run is active, followed by all 54 DPR 3.0 checks and
the actual desktop .lnk launch. No desktop shortcut has been delivered yet.

Next steps: finish the full installed suites; reconcile/render/inspect
owner DOCX and commit/push the native fixes; stage the new payload and existing
NSIS launcher; run packaged/high-DPI acceptance; create/update and reopen the exact
owner desktop link, then launch that saved .lnk and verify the runtime home and
working directory. Update this section and roadmap with actual final evidence.
Preserve untracked ai-instructions/queue and deferred feature families.

The notes below are chronological source-preparation history, superseded by the
latest gate above where they describe builds/tests as pending.

## October 6 recovery sequence resumed in the owner-requested conversation

Current gate: grouped native compilation, then exact-class installed regression
and packaged GUI acceptance.

Pending reference cleanup now discards superseded direction/pivot guards, cancels
pivot picks on mode/reset changes, and blocks numeric gestures while a pick is
pending. Axis markers remain visible for zero-size references. The integration
fixture preserves its static settle method and checks scene-node removal by count.
These source changes parse and pass whitespace checks; native execution is pending.
Reference review also found that a bare selected component occurrence bypassed
native path normalization. It now resolves through its exact root path, retaining
the displayed frame and scale guards. A native frame regression is prepared.
Whole-component picks normalize to their displayed native Origin, including
linked-definition placement; directly linked datum picks retain the base placement
and direct scaled links fail rigid-frame validation. Interactive GUI evidence now
includes an actual Edit Pivot drag and screenshot capture. An integration test
switches the active document and closes the owning document with handles present.
All of these new checks are still unexecuted, and the final DOCX validation-status
update/render remains part of the same grouped delivery gate.
Additional acceptance now uses real sketch clicks for Single/Connected/Tangent,
Escape and empty-space clearing, plus native Point-to-Point collector clicks on
visible points outside the active parent. The recovered box fixture already drives
the native box commands with Qt press/move/release events. These tests are unrun.
Interactive numeric fields now enable only the active arrow/plane/ring inputs;
an inactive plane value is not validated or read for axis/ring gestures. A native
invalid-plane-to-axis switching regression is prepared; execution and final owner
DOCX validation-status reconciliation remain pending the grouped runtime gate.

The active build log confirms links for FreeCADBase/FreeCADApp/FreeCADGui,
FreeCAD.exe, Part/PartGui, Sketcher App, PartDesign App and AssemblyGui; no full
build outcome or runtime pass is established. After ALL_BUILD finishes, refresh
only `FreeCADGui_Resources` if script hashes differ, then run `run_acceptance.py`
against this build's bin/FreeCAD.exe. Use fresh evidence directories and require
the launched AppHomePath and shipped module hashes; no source application overlays.
Release configuration completed successfully in
588.953 seconds; BUILD_GUI/ASSEMBLY/PART/PART_DESIGN/SKETCHER/START/TUX/CAM are ON,
FEM/ADDONMGR are OFF. One ALL_BUILD is running under the finite monitored wrapper.
Do not launch another build while it is alive. Exact PID/command are in
`build-process.json` beside `build.log`; build outcome has not been established.
The revised owner DOCX rendered again to 83 pages; affected pages 78–83 are
visually verified with no clipping/overlap or damaged numbering. The initial
render blocker is resolved for this revision, not a new native acceptance claim.

Prepared three additional integration checks: all six Tasks at 360 logical pixels,
mode-exit handle cleanup and external-parent owning-file refusal/standalone movement.
The handle ray-pick fixture scans its rendered perimeter rather than assuming an
axis screen direction. Deleted-document drag cleanup removes native callbacks
even when its prior placement frame is no longer accessible. These checks/fixes
are awaiting the installed runtime; all current tests remain unexecuted on this PC.

Portable NSIS 3.11 compiler is available for the existing repository launcher;
the official ZIP SHA-256 matches
`c7d27f780ddb6cffb4730138cd1591e841f4b7edb155856901cdf5f214394fa1`.
No launcher/payload/desktop shortcut has yet been built or changed.

Move/source integration published to origin/main at
`85900f48d48cd68aea9925360333743b1f1cd6cb`; ls-remote matched HEAD after push.
Thirteen affected Python modules parse and the GUI CMake script inventory includes
them. Native execution is still pending. The foundation's old Point placeholder
expectation now checks its real Source prompt. Post-reset labels follow each method.

Grouped Release configuration is running in
`C:/Users/GAMING-PC/AppData/Local/FreeCADPlus/freecad_plus_2026-10-06_recovered_workload`.
This is a new application build directory, not the toolchain smoke sample and
not an incremental/copy payload. The initial prebuilt Coin/Pivy setting failed
because LibPack 3.5.3 has no prebuilt Coin config; corrected to this fork's
bundled Coin/Pivy as required by UseLibPack3. Existing submodule source is retained.
Configure/build wrapper and logs are in this conversation's visualization folder
`01a10f79-1a93-7be0-a261-96a6b7e9c425`; no duplicate build is running.

DOCX rendering is recovered: the saved LibreOffice MSI was administratively
extracted into a new isolated `dependencies/native/libreoffice` directory under
the resolved workspace runtime. No desktop renderer was used/modified. The
Documents plugin's named render_docx.py helper is absent in this installed package;
the documented manual isolated-profile conversion plus bundled pypdfium2 produces
all 83 page PNGs. Affected pages 78–83 were inspected at full page resolution:
no clipping/overlap or broken numbering. Six obsolete status paragraphs were then
targeted for reconciliation; every other package part is unchanged. The revised
document is being rendered again before this visual gate is recorded as passed.

Interactive source uses the fork's SoTransformDragger through a new view-only
createTransformDragger binding. Native arrows, planes and rotation rings remain
the existing services; zero increments now explicitly mean unsnapped linear/
planar/rotational dragging, with native status values retained. Existing positive
increment behavior is unchanged. No document object or property owns the handles.
Command-local default pivot uses selected parent-frame geometry bounds (or mean
instance origin fallback); Edit Pivot, native midpoint picks, explicit frame/axis
orientation and Reset Pivot do not move geometry or add undo records. Gestures
compose against unchanged placements; release retains preview. View-scoped
Escape releases native capture and restores the current gesture's baseline.
Selection's broader Escape clearing defers to an active manipulator drag.

Four TestMoveComponentsInteractive cases are prepared, including a rendered
Coin handle pick followed by Qt press/move/release/Escape events. They have NOT
run. Parsing passes for the nine Move source/test modules. Integration/native
compile and actual event/packaged acceptance remain required. Next: reconcile
native services, prepare grouped test harness, then configure/build this fork once.

Align Coordinate Systems source is prepared with existing native origin/datum
frame picks, explicit Parent and expandable Origin/Z/X definitions. Orthonormal
right-handed construction rejects parallel/zero input; matrix validation rejects
scale/reflection/shear, including scaled native occurrence ancestors before
Placement conversion. Source/Target triads and origins preview complete rigid
alignment with roll. Four tests in TestMoveComponentsFrames await native execution.
Next: Interactive native manipulator and pivot; do not substitute numeric-only UI.

Published source milestones (origin/main verified by ls-remote matching HEAD):
Selection `3f7e7d3ec14962a08e25ccfa49a587559c7112d1`;
Layers/palette `6fdfac99a1da2530eb28bf47d7cf7132c8f32582`.
These preserve recovered code with syntax/staged whitespace checks, not new native
acceptance. Shared ribbon/package wiring and consolidated owner documentation are
in the subsequent Move/integration group, because those recovered edits couple
all four feature families. Untracked prompt archives are not staged.

Align Axes source is prepared: native line/circle/cylinder extraction,
minimal-angle rotation, deterministic antiparallel basis, closest-point Coincident,
fixed-anchor Parallel, Reverse Target, transient direction markers and reset.
Five native checks in TestMoveComponentsAxes await the grouped build. Next source
item is Align Coordinate Systems, followed by genuine Interactive handles.

Point to Point source now uses the existing Session candidates/commit and shared
task, with separate Source/Destination pick roles, native point resolution,
finite point validation, labeled markers/vector/distance, reference deletion
guards and Apply reset. Four native regressions were added in
`TestMoveComponentsPoint`; they have not run yet because no Plus runtime exists
on this replacement host. No mock runtime is used as native evidence.

Read all seven saved prompts, context/audit, queue manifest and the complete
recovered owner conversation. Actual source confirms Selection/Layers/palette/
Translate preparation and interrupted Rotate. Preserve all recovered modifications;
the untracked `ai-instructions/queue` is an execution archive, not a new worker queue.
No duplicate chats/workers or native queue submissions were created.

Rotate source and all eight updated checks were inspected. Ten affected Python
modules pass parsing on this host. Historical 12 Translate + 8 Rotate results are
not newly rerun results: the old Office-PC runtime is absent. The current local
`freecad_plus_2026-10-06_toolchain_smoke` directory is a toolchain sample, not this
application. MSVC BuildTools 2022, CMake and LibPack 26.3.0-v3.5.3 are available.
All runtime/GUI/Undo/save-reopen evidence must be rerun after the single grouped
native build. Owner DOCX was read before edits; Rotate requirement/status appended
without changing other package parts. Document visual review remains pending.

Next: Point to Point, then Align Axes, Align Coordinate Systems, Interactive,
integration reconciliation and one grouped native build/package/shortcut delivery.
Complete these in order; do not stop or claim delivery at Rotate source review.
No new owner build, shortcut change, source publication or acceptance is claimed
by this entry. Later entries must record exact actual commits/pushes and tests.

## October 4 Move Components foundation and Translate source preparation

Authorized prompt 4 is implemented in source. `MoveComponents.py` owns reviewed
component paths, parent-frame direction snapshots, transient geometry evaluation
and atomic placement commits. `MoveComponentsTask.py` provides the single Tasks
panel, shared collector controls, unit-aware translation, reset/recovery and native
Apply/OK/Cancel routing. Design Assembly and the Part Tree context menu expose
`Std_MoveComponents`. No Copy control or deferred repair/feature-handle work was added.
Rotate through Interactive remain explicitly awaiting prompts 5–9; no backup was
enqueued and no native rebuild, owner payload, shortcut change or publication is claimed.

The task activates only the selected instances' immediate parent definition and
retains its exact displayed path. Only direct siblings in that context are accepted.
Each commit writes their existing LinkPlacement values once; descendants are implicit
and source definitions, ownership, geometry and identities remain intact. The preview
shows every displayed occurrence of that shared parent, each in its own native frame.
Native joint Reference1/Reference2 paths are checked in addition to direct consumers,
driven/grounded/read-only guards. External parents require opening their owning file.

Final evidence: **12 distinct Move checks pass**, native process exit 0, in
`D:/Temp/Office-PC/freecad_plus_2026-10-04_move_source/source-results.json` and
`policy-tests.log` (8.400 seconds). They use explicit Python source overlays on the
unchanged `freecad_plus_2026-10-03_theme_inheritance/app/bin/FreeCAD.exe`, not a rebuilt
or newly packaged executable. Covered: differently transformed shared parent uses,
standalone parent tab, native shape-path output, implicit descendants, group-relative
transforms, native axis/edge direction snapshots, reverse, safeguards and rollback,
native Undo/Redo and FCStd/cadprt reopen, collectors, workflow switches, document
cleanup and persistence on/off. The actual task-panel Apply and OK buttons pass;
Cancel discards a pending move while earlier Apply transactions remain undoable.
Syntax checks and git diff whitespace checks pass; the stylesheet warning is inherited.

Verification repairs: the first round-trip fixture reopened an already-open document
and then closed that original; it now closes before reopening each saved format.
Native selection rejects a bare hidden source Link, so ambiguity is tested using an
explicit input record and command routing uses a real root-qualified native selection.
Bare Origin axes require their native Origin prefix when qualified through a component.
Actual Apply-button testing found Qt6 sends a StandardButton enum; the handler now
accepts that enum as well as integer values. No failure is reported as a passing check.

`move-task.png` and `move-preview.png` were inspected: the live task has the required
field order and native buttons, unit-aware Distance and teal previews in both parent
uses. The isolated source-overlay harness retains the original Navigator dock while
loading the changed module, so its full-window screenshot contains an extra Components
dock. This is not packaged UI evidence. Native filtered viewport picking, high-DPI
and clean installed-startup acceptance remain deferred to prompt 10.

Owner DOCX read and updated with six requirement paragraphs; all 2,798 earlier
paragraphs are byte-preserved at XML paragraph level and every package part except
document.xml remains unchanged, including headings/styles/native numbering. SHA-256:
`b3a6ffbf1f6cbfd03116ab1522d41351c0a87a0a217b338ddfb79b9b4923e8e0`.
The packaged Documents renderer was attempted on this revision and again fails at
`_resolve_soffice`: `LibreOffice soffice.exe was not found on PATH`. No DOCX page PNGs
or visual pass exist. Resolve the renderer and inspect affected pages before delivery.

Next: implement Rotate on this same Session/MoveTask machinery in prompt 5. Preserve
the owning-parent/path contract, rigid group delta, source-free preview, atomic commit,
shared persistence and post-Apply reset. Prompt 10 runs the installed Move suite and
all six workflows alongside native Selection/Layers/palette checks, then packaged
entry points/reference picking, task/mode transitions, owner payload and shortcut.
Source preparation is not owner-ready delivery or physical acceptance.

## October 4 Layers and Contextual Constraint Palette source preparation

Prompts 2 and 3 are implemented in source. Prompt 2's first runtime launch was
interrupted; its tests, repairs and documentation were completed alongside prompt 3.
No prompt backup was enqueued or replayed. No native rebuild, owner payload, shortcut
change, commit/push or release is claimed for this step.

`DesignLayers.py` owns document-local layer IDs, Base protection, native NoRecompute
assignment properties and transactions. Native Body membership and Plus
Producer/ConsumedResults links resolve indivisible bodies; sketches remain independent.
`DesignLayersGui.py` supplies the task, fixed-label menus and Coin display-branch gates.
It leaves individual Visibility unchanged and keeps the Body Group scene traversable.
FCStd and cadprt round trips use the existing native document storage. No new geometry
groups, ownership links or dependency edges are introduced.

`ConstraintPalette.py` uses native Sketcher constraints and transactions. The GUI
controller opens only after viewport clicks, keeps a viewport-clamped travel region,
cancels the one-second outside timer on reentry, and exposes disabled tooltips.
Construction conversion is normal-first for mixed selections. Driving conversion
retains invalid committed states and reports native solver diagnostics. Making a
dimension reference can remove one conflict while another remains; expression-driven
reference conversion is protected from native expression deletion. There is no repair UI.

New native `diagnoseConstraintAdditions` clones geometry and constraints into the
existing Sketch solver, leaving saved data and the live solver untouched. New
`setDrivingBatch` validates all input indices/expression safeguards before changes and
solves once after the batch. These new C++ APIs are **source-prepared, not built or
runtime-verified**. Python source-overlay compatibility uses the existing APIs and is
not a substitute for their grouped-build acceptance.

Prerequisite fixes from runtime evidence: native NoResolve sketch picks can contain
lowercase edge/vertex names; semantic resolution now recognizes these without changing
occurrence prefixes. A visible palette consumes its Escape dismissal so a second
native action cannot exit sketch edit and select the sketch. The ordinary toolbar
defers explicit deselection until native Escape handling finishes. Layers fixes include
origin-feature membership recognition, destroyed-toolbar observer cleanup and Qt6
standard-button conversion. Native geometry comparisons use tolerance after serialization.

Final quick evidence: **35 distinct checks pass** (13 Selection policy/toolbar,
10 Layers, 12 palette) in
`D:/Temp/Office-PC/freecad_plus_2026-10-04_design_source/source-results.json` and
`policy-tests.log`; the native process exits 0. These are explicit Python source overlays on the unchanged
`freecad_plus_2026-10-03_theme_inheritance/app/bin/FreeCAD.exe`, not a rebuilt or
newly packaged executable. Qt mouse events traverse the real active sketch viewport;
the one-second timer/reentry, Escape with and without a palette, empty click, drag
suppression and disabled tooltip paths pass. Both native-document formats pass.
Python syntax and `git diff --check` pass. The isolated stylesheet warning is inherited;
redundant-constraint diagnostics in stderr are expected from the intentional invalid
driving/partial-reference fixtures. The first pointer fixture found deferred-deletion
widgets from earlier documents; it now targets only the active MDI view and delivers
hover events before clicks. No physical pointer or high-DPI owner acceptance is claimed.

Owner DOCX: nine requirement paragraphs added, all 2,789 previous paragraphs retained
unchanged, and all package parts other than document.xml unchanged. SHA-256:
`61f2de1f6808f9b2e97f7d8254cac41819de80298a444549371bc9cfd854705c`.
The bundled Documents renderer was run again on this revision and fails at
`_resolve_soffice` with `LibreOffice soffice.exe was not found on PATH`. The prior
runtime inventory found no bundled Windows LibreOffice. No page PNGs or visual pass
exist for these edits. This remains an explicit owner-document delivery blocker.

Prompt 10 must compile FreeCADGui and Sketcher App/Gui together, run
`TestDesignSelectionNative`, `TestDesignSelectionBoxes`, `TestDesignLayers` and
`TestConstraintPaletteNative`, verify native layer gates/collector intersections,
external and repeated component rendering, dimension dialogs, DPI and task transitions,
then verify the packaged payload and existing owner shortcut. Resolve the DOCX renderer
and inspect affected pages before calling any of this owner-ready. Physical owner
acceptance remains separate.

## October 3 Selection toolbar source preparation

Workload prompt 1 adds `DesignSelection.py`, `DesignSelectionToolbar.py` and the
PlusRibbon top-row integration. Semantic categories distinguish drawing geometry
from body subelements, preserve occurrence paths and intersect native command gates.
Connected chains include construction curves without remapping their indices;
tangent chains stop at branches. Native Selection now exposes completion-only
persistence and directional policy; Sketcher constraint/construction completion
uses it without intercepting explicit clearSelection or replaying stale indices.
Both 3D and Sketcher box logic honor the directional toggle. Sketcher curve crossing
also checks sampled segments, including the final endpoint; element boxes collect
the enabled category union. Native changes are NOT built in this step.

13 distinct focused checks pass in
`D:/Temp/Office-PC/freecad_plus_2026-10-03_selection_source/source-results.json`:
11 real-geometry policy checks and two toolbar/lifecycle checks. This uses explicit
Python source overlays on the unchanged theme_inheritance Plus binary; it is not
a packaged owner acceptance run. Final native process exit is 0. The first harness
attempt used the FreeCADGui alias as a package path; the corrected harness loads
the explicit source modules. A subsequent harness exit-code query was corrected
to retain the process handle; the final result is clean. The pre-existing isolated
application stylesheet parse warning remains in stderr and is not attributed to
the new toolbar. Python syntax and git diff whitespace checks pass.

Owner DOCX: six new requirements paragraphs, all 2,783 pre-existing paragraphs
unchanged; all package parts except document.xml unchanged, including numbering.
SHA-256 `a4d73fd20dfc266004da4907718aa7788bd8bf1d5a9fc400624fbdec0b94f32c`.
The sandbox denied replacing the protected DOCX; the same prepared patch succeeded
with narrow approved access. Packaged `render_docx.py --emit_pdf --verbose` fails
at `_resolve_soffice`: soffice.exe is not on PATH and the dependency runtime has no
bundled Windows LibreOffice. Document visual QA remains BLOCKED, not passed.

Required prompt-10 gates: resolve document rendering and inspect affected pages;
compile FreeCADGui and SketcherGui plus dependent targets together; run
TestDesignSelectionNative and TestDesignSelectionBoxes along with relevant prior
selection/Sketcher/ribbon regressions; verify native clicks, gates, preselection,
Escape/empty click, curve-intent event paths, persistence on/off, delete/undo/reopen
and collector isolation. Then deliver the coherent owner payload, update/reopen/
verify the existing desktop shortcut and record source publication separately.
Current owner payload/shortcut remain theme_inheritance. This step is source-prepared,
not owner-ready, not a fresh build and not a release. No deferred feature group started.

## October 3 inherited task colors

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_theme_inheritance/app`.
Python-only incremental staging from datum_plane; native files are unchanged from
the preceding grouped build at `c9663bf39c`. Removed the three remaining copied
form palettes in ComponentTaskWidgets, ComponentSketchTask and ComponentPlaneTask.
The prior broad task stylesheets were already removed. Source audit finds no
setStyleSheet or setPalette calls in the Plus Python task modules. Native and
inherited task styles were inspected; control-specific state/layout styling is
retained, since it does not force palette colors on every descendant.

All eight Plus tasks inherit Qt and active-theme colors. The development guide
now prohibits task-wide forced foreground/background rules and frozen form
palettes. Qt's application stylesheet may itself set WA_SetPalette when polishing;
the updated native check compares a task with an ordinary sibling widget instead
of requiring a copy of the main-window palette or an unset internal Qt flag.

21 distinct native checks pass: nine shared task-width checks in validation/theme
and twelve final plane/inheritance/popup checks in validation/final, through the
owner launcher without source overlays or unexpected GUI diagnostics. Earlier
palette-copy and Qt-flag expectations in failed suites are superseded by final;
they are retained as diagnostic evidence. Narrow light-theme fields and dropdowns
remain readable. This is not a new native compilation or published release.

The Word document changed one requirement paragraph; all other 2782 paragraphs,
styles, headings, numbering and other package parts remain unchanged. All 78 pages
rendered; changed pages 72-76 were reviewed and the other 73 are pixel-identical
to the preceding review. SHA-256:
`d540f2066e411f1e9bb4868500dde3751c77a9a71295957e8b0953d93d38939a`.
The desktop shortcut target/working directory and payload provenance are recorded
in validation/shortcut-verification.json and BUILD-VALIDATION.json. Source
publication is recorded in Git history and the payload manifest.

## October 3 datum-plane create and edit

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_datum_plane/app`.
Grouped incremental native build from the existing configured compiler tree;
not a clean rebuild. Core GUI, Part, PartDesign, Sketcher and their dependencies
passed the focused build, and twelve rebuilt native files were staged alongside
the source Python modules. The inherited executable version string still names
`03a6f66644488e2b710f94e828155b9b12c23c60`; it is a base stamp, not the new build's
source identity. BUILD-MANIFEST and BUILD-VALIDATION record the application commit,
compiled source hashes and staged native hashes separately. No published release.

The standalone Plane action, native component-document Datum Plane command and
History editor open the new four-section task. Plane geometry supports origin or
user planes, planar faces, coplanar non-collinear edges/lines, axis plus line,
three points, and line plus point; planar curves may participate. Enter values
accepts XYZ offsets and a nonzero normal normalized on acceptance. Orientation
projects an edge/axis or two points onto the plane, with closest component axis
as default. Origin selection projects a point/endpoint or the part origin.
Separate normal, signed-offset and X-direction reversals remain independent.
Purple preview and automatic recompute default on; previews are transient and
non-pickable. Disabling automatic updates clears stale preview until refreshed.

ReferenceCollector extends the same CurveCollector used by modeling operations,
including focus, latest-row highlight, toggle deselection and Delete. Its mixed
geometry lists add basic plane/axis menus and Under-defined/Defined/Invalid status.
Native plane identities, association, undo/redo, helper cleanup and persistence
are retained; importing old projected planes accounts for their former offset/Z
reversal order. Arbitrary legacy frames retain stored origin and X direction.
Existing embedded sketch-plane creation and independent/support sketch behavior
remain available. Native App::Line directions now correctly use their X base axis.

Task forms use the active palette instead of forced dark colors. Ribbon pages
refresh on palette/style changes, fixing a startup color retained from an older
palette. Both origin planes and axes, plus the origin point, are shown at twice
normal scale during plane/sketch placement; finish/cancel restores size/visibility.

62 distinct native checks passed without source overlays or unexpected GUI errors:
- `validation/delivery`: 12 final plane checks through the owner launcher, covering
  requested combinations, invalid/under-defined inputs, actual viewport face picks,
  toggle/Delete, basic-menu focus, 360-pixel vertical scrolling, popup contrast,
  live palette changes, purple preview, normalization, native command/History entry,
  edit/cancel, legacy migration, atomic failure, undo/redo, save/reopen and scale restore.
- `validation/plane-native-2`: nine legacy plane checks and nine shared task-width
  checks. Its nine earlier plane-task checks were superseded by delivery above.
- `validation/regression`: 32 curve-picker, modeling-preview and sketch-frame checks,
  including tilted viewport edge picks across five modeling operations.

Early failed probes are retained for diagnosis and are not acceptance evidence.
Light task fields, popup text, purple overlay, origin geometry and narrow panel
captures were reviewed. A pointer probe overlapping the native origin planes picked
that plane; the body-face toggle test uses separated geometry to avoid ambiguity.
Physical pointer/high-DPI owner acceptance remains separate.

The Word specification changed only five plane paragraphs, preserving its other
2778 paragraphs and every other OOXML package part. All 78 pages rendered;
changed pages 66-76 were reviewed, with the remaining 67 pixel-identical to the
previous reviewed document. Headings, styles, automatic numbering and Classic
where-used child bullets remain intact. Word SHA-256:
`4f1f0d54f68a115a3a85943bd4a92cf1f03ba956dbc2ec1b4ad1cd81c88535ab`.

The existing desktop shortcut was saved and reopened; target and working directory
match this payload (`validation/shortcut-verification.json`). Source publication
and full payload integrity are recorded in the delivery manifest and Git history.

## October 3 follow-up temp-folder cleanup

Removed 310 confirmed empty folder trees and ten obsolete folders from
`D:/Temp/Office-PC`: six superseded owner payloads (combined_modeling,
modeling_previews, component_double_click, history_order, history_edit and
plane_frame), three old SketchSolverTest fixture directories and MSBuildTemp.
Deleted 10,248,148,956 bytes; the retained 486,955,144-byte evidence archive leaves
9,761,193,812 bytes (9.091 GiB) reclaimed, excluding filesystem allocation effects.

Preserved 932 evidence files, manifests, scripts and CAD fixtures in
`freecad_plus_2026-10-03_curve_picker/cleanup/obsolete-evidence.zip`, with paths
relative to the temp root. Existing historical archives are included intact.
ZIP CRC and every archived entry's SHA-256 pass; archive SHA-256 is
`b3221113d91359d8df06d9e83bd2907217f997f7f5b2bc72417a2331a053ecc9`.
`archive-verification.json` and `cleanup-result.json` in that same folder record
exact scope. Earlier evidence paths within removed builds are recoverable there.

Retained curve_picker (current shortcut target), sketch_frame (immediate rollback),
the configured compiler/dependencies, and the still-running October 2 audit build
(PID 17424 at cleanup). Current/rollback launcher and native executable hashes
still match their manifests. Resolved deletion paths stayed under the requested
root; reparse points and running application folders were excluded. Non-recursive
empty-directory deletion rejected folders that became nonempty or were locked.
Two empty directories remain: `collab_low` is in use and `hsperfdata_Office-PC`
returns access denied. No application was stopped and no permissions changed.
Other nonempty folders with uncertain ownership/obsolescence were retained.

The Word specification's existing cleanup paragraph now covers this follow-up.
Its 2782 other paragraphs and all other package parts remain unchanged. All 78
pages render; page 77 was reviewed, and the other 77 are pixel-identical to the
previously reviewed document. No application code or build changed in this step.

## October 3 shared curve picker and modeling controls

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_curve_picker/app`.
Python-only incremental staging from sketch-frame, with nine GUI modules
including the new installed `ComponentTaskWidgets.py`. No native rebuild,
installer or published release. Native identity remains
`03a6f66644488e2b710f94e828155b9b12c23c60`; application source is recorded separately
in the payload manifest and validation report.

Reproduced five incorrect selections in 36 native viewport edge clicks on the
previous payload (`validation/reproduce-recorded`). At tilted angles the picked
edge could lie slightly behind the cursor's sketch-plane intersection. Region
handling collected all four edges before the native observer toggled the clicked
edge off. The shared controller now gives same-sketch edge/vertex hits precedence
before depth filtering. Interior regions and solid occlusion retain their rules.
Focus is assigned before list highlighting so a repeat-click removal cannot
silently select the first remaining row.

`ComponentTaskWidgets` owns one configurable source/list/action `CurveCollector`
for Extrude, Revolve, Helix, Loft/Pipe sections and both Pipe path roles. It also
owns the selection/display lifecycle, toggle policy, preview controls/timer,
operation/target choices, compact layouts, reference/quantity fields, common
refinement/fuzzy options and status controls. Existing operation backends retain
native geometry, validation, transactions, identities and persistence. The former
Extrude widget imports remain compatible for existing consumers.

86 distinct native checks pass without source overlays or unexpected GUI errors:
- `validation/selection-final`: 42 checks. The five-operation viewport probe
  records 170 native edge clicks at 0/35/65 degree views with no wrong collectors.
  Sequential/repeated picks, interior regions, Delete, persistent highlights,
  section and path roles, six preview workflows, occlusion and 360-pixel vertical
  task scrolling pass. Narrow Extrude/Pipe captures were visually reviewed.
- `validation/operations-final`: all 40 Revolve/Helix/Loft/Pipe/Primitive checks
  pass, including create/edit/undo/persistence and native command routing.
  Its TaskContext suite exposed an obsolete native MapMode assertion from before
  resilient sketch frames. The updated assertion verifies the actual face
  reference, mode and following status; all four checks pass in
  `validation/context-final`, including native Sketcher and component return.
- `validation/launcher-final`: the actual owner launcher repeats the tilted
  Extrude regression successfully after final whitespace cleanup (87 passing
  executions across the accepted reports, 86 distinct checks).
- Earlier reports retain the UTF-8 staging issue and viewport fixture repairs.
  Origin axes overlap the rectangle's bottom/left edges, so deterministic
  sequential probes use the unobstructed edges; origin handling remains covered.
  The final selection report includes the focus-order product correction.

The canonical Word specification changes only two existing requirement paragraphs;
2781 other paragraphs and every other package part are unchanged. All 78 pages
render; pages 1-75 are pixel-identical to the reviewed baseline, and pages 76-78
were visually reviewed. Headings, owner edits and automatic numbering remain.
SHA-256: `48a82326d2f3e7ea4c81e7da56f2c58c322bdcbce7c5840f5890de2a40005412`.
Evidence: task visual folder `curve-picker-doc/verification.json` and `render`.

The existing desktop shortcut was updated, reopened and verified for both target
and working directory (`validation/shortcut-verification.json`). Build provenance,
module hashes and source revision are recorded in `BUILD-VALIDATION.json` and
`BUILD-MANIFEST.json`; source publication is to the authorized `origin/main`.
Physical owner acceptance remains separate from the injected native GUI checks.

## October 3 Classic toolbar mapping bullet correction

In the canonical UI & UX Word document, section 2.1.1 now places each
where-used location in a native bullet exactly one level below its operation.
Converted 1,245 inline location lines under 644 operations; retained the two
already-correct Pad/Extrude child bullets. All text and existing paragraph
properties are preserved. Other package parts, including styles and numbering
definitions, are byte-identical. All 78 rendered pages were visually reviewed.
Document SHA-256: `1aa217fd42c533f095a6bb8cb75a74129dfbaa85a2fb89e66ff1b3b36f57b791`.
Evidence: local visualization folder `toolbar-child-bullets/verification.json`
and `toolbar-child-bullets/render`. This is documentation-only; no application
build, GUI behavior change, shortcut change or release is included.

## October 3 independent and resilient sketch frames

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_sketch_frame/app`.
Python-only incremental staging from plane-frame; seven installed modules changed.
No native rebuild, installer or published release. Native identity remains
`03a6f66644488e2b710f94e828155b9b12c23c60`; BUILD-VALIDATION and release-info record
application source and baseline provenance separately.

New Sketch offers Independent plane (component-local XYZ and rotation angles or
axis/normal vectors), origin/user planes, planar faces and two coplanar edges
from one body. Follow support defaults on for referenced choices; disabling it
copies the frame once. Independent sketches create no attachment object.
Native face/user-plane attacher math and a deterministic two-edge frame update
native Sketcher objects. Persistent hidden references avoid a failed upstream
feature blocking the sketch; last valid support and sketch placements preserve
origin/axes on deletion, missing faces or upstream errors. Repaired/undo-restored
supports resume following; same-name replacements never reattach automatically.
Cache/status properties are outputs, so failure diagnostics do not dirty valid
sketch geometry. Native offsets, solver, support replacement and editor remain.
History predecessor checks include soft frame references; validity checks do not
reject an intentionally retained frame because its support is unavailable.

78 distinct native checks pass in the staged application without source overlays:
- `validation/sketch-final`: 36 checks, covering frame creation, direct/indirect
  failure and repair, movement/rotation, offsets, missing faces, deletion/undo/redo,
  save/reopen, downstream extrusion, live two-edge picking, independent Sketcher
  entry, atomic invalid-input rejection, datum planes, History and support editor.
- `validation/sketch-regressions`: all 32 existing SketchWorkflow checks and one
  separate-process saved-frame restore check pass. Its width suite initially
  expected scrolling even when the shorter independent form fit the available
  height; this fixture assumption is corrected in the following report.
- `validation/sketch-widths`: all nine checks pass. Independent numeric and vector
  frames fit 360 logical pixels and scroll vertically at 400 pixels high. Every
  visible field remains inside the horizontal viewport and vertically reachable.
- Native GUI captures were reviewed, including the narrow independent frame modes.
  Earlier failures exposed the cached-status touch flag, single-item picker and
  old native-only region support lookup; all three product issues are corrected.
  Early filtered-suite invocation errors remain in their original reports.

The Word specification updates five existing paragraphs, preserving the owner's
other 1533 paragraphs, paragraph/run formatting, headings, automatic numbering,
headers/footers and all other package parts. Seventy-seven pages render; pages
1-66 are pixel-identical to the prior reviewed delivery and changed pages 67-77
were visually inspected. A final wording correction changed only page 71 and was
re-rendered/reviewed. Evidence: task visual root `sketch-frame-doc/verification.json`.
Final Word SHA256: `4954fd0d5c8746c899e541f3e99382d470961b004049903969a952ae230a5ed5`.

The existing desktop shortcut was saved, reopened and target/working-directory
verified (`validation/shortcut-verification.json`). BUILD-MANIFEST verifies staged
source, critical binaries and inherited baseline payload; publication.json records
matching commit/origin identity after the coherent source commit is pushed.
Physical owner pointer/high-DPI acceptance remains separate from automated checks.

## October 3 projected datum-plane frame workflow

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_plane_frame/app`.
Python-only incremental staging from history-edit; changed modules are
ComponentSketch, ComponentSketchTask and ComponentModel. No native rebuild,
installer or published release. Native About remains
`03a6f66644488e2b710f94e828155b9b12c23c60`; release-info and BUILD-VALIDATION record
the newer application source and inherited baseline provenance.

The default four-step task defines surface, Z normal/reverse, projected sketch
origin and projected X/reverse. Origin defaults to the component origin; X defaults
to the most parallel component axis with stable X/Y/Z tie-breaking. Optional
vertex/datum-point, edge or two-point references remain associative. Curved edges
use midpoint tangents. Native datum/attachment engines define the base surface;
a hidden frame proxy projects references and supplies the public PartDesign plane's
ObjectXY attachment. Sketches keep native attachments. Invalid projections roll
back; deletion cleans unused helpers in the same transaction. Explicit legacy
numeric frame modes and existing scripted plane calls retain prior semantics.

55 distinct checks pass. Evidence under the build parent's `validation` folder:
- `plane-verified`: final projected-frame cases, including symmetric-axis ties,
  translated/tilted surfaces, moved components, independent reversals, point/edge/
  two-point picking, source updates, helper cleanup, Undo/Redo and save/reopen.
- `plane-final`: projected cases and all width/context/History checks pass; its
  six StartActions cases failed in fixture logging because a detached Windows GUI
  has no stderr file descriptor. The logger now uses App.Console.PrintMessage.
- `start-actions`: all six command/startup checks pass with the corrected fixture.
- `sketch-planes`: all 17 selected plane/sketch regressions pass, including legacy
  directions, atomic plane+sketch creation, attachments, pending tasks and Extrude.
  The tilted-surface task assertion now checks the requested projected origin.
- Native module hashes match staged source; no source overlays or unexpected GUI
  diagnostics. The projected and legacy task modes fit 360-pixel panels with
  vertical-only scrolling. See reports for exact counts and retained first runs.
- `shortcut-verification.json` records the existing desktop shortcut saved,
  reopened and verified; `publication.json` records matching source/origin identity.

Word updates five affected requirement paragraphs while preserving the owner's
concurrent save, other paragraph XML, package members and native automatic numbering.
All existing paragraph properties, heading structure and list levels are retained.
The Classic Toolbars section annotates all 873 operation/dropdown entries against
the staged Plus ribbon: 647 mapped, 224 missing from the current ribbon/build and
two intentionally replaced controls. Existing owner Pad/New Body examples are
preserved. Plain-text mapping lines use existing paragraphs and native numbering;
styles, headers, footers and all other package parts are unchanged. The runtime
command/location audit is in `validation/toolbar-locations/locations.json`; its
one audit execution passes. Final render review and exhaustive mapping/OOXML
verification are recorded under `plane-frame-doc` in the task visual root. All
77 rendered pages were visually reviewed; four final caption-only page changes
were re-rendered and reviewed again. BUILD-MANIFEST records
changed/critical-file hashes and verified inherited files. Physical owner pointer/
high-DPI acceptance remains separate from automated native GUI checks.

## October 3 temporary suppression of later History items during edits

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_history_edit/app`.
Python-only incremental staging from the verified history-order payload. Updated
modules: ComponentModel, ComponentNavigator and all six modeling task launchers.
Native About retains `03a6f66644488e2b710f94e828155b9b12c23c60`; BUILD-VALIDATION and
release-info identify the newer application source. No native rebuild or release.

TaskContext owns the temporary history tail and reuses native TempoVis for display
restoration/save handling. Authored UserSuppressed flags and Undo history remain
unchanged. The model excludes later items from evaluated inputs/results and shows
Suppressed during edit. Published-result caches remain intact for native links,
then refresh at edit completion or before save. Native geometry links and engines
are preserved. This is temporary component availability, not a native recompute
engine freeze. Earlier/edited items and native Origin remain available. Cancel,
accepted edits, startup failure and document close clear rollback; validation
failure keeps it active. All six modeling launchers share the context, alongside
native feature and Sketcher editors; reference/BOM entry points also use it.

Validation evidence in the build parent's `validation` folder:
- `edit-save-final`: all 46 native checks pass, including 37 existing panel/context,
  suppression, History ordering and modeling preview regressions.
- `edit-save-resilience`: all 10 focused lifecycle checks pass on the final module,
  including save failure before the finish notification and fresh downstream
  geometry when saving an unfinished edit. Together 47 distinct checks pass, with
  source-matched installed modules, no overlays and no unexpected GUI diagnostics.
- `edit-verified`: eight focused checks pass, including all six modeling editors,
  feature 5 of 10, reordered History, preexisting suppression/visibility choices,
  edited geometry with dependent mirroring/expressions, Undo/Redo, save/reopen,
  native Sketcher, failed validation/startup and document close.
- Earlier `edit-1` and `edit-final` retain fixture failures: legacy extrusion
  conversion with a direct expression consumer, a Pipe path/profile fixture and
  accessing the deleted task label after successful Accept. Corrected fixtures
  pass without weakening application validation.
- `shortcut-verification.json` records saving and reopening the existing desktop
  shortcut with its verified target/working directory; `publication.json` records
  the source commit and matching origin/main identity.

Word preserves all 1535 existing paragraphs and package members except document.xml.
Original pages 1-46 match the preceding render; new page 47 was inspected in
`history-edit-doc/render-final` under the task visual root. The payload manifest
inherits verified unchanged baseline hashes after size/timestamp checks and
rehashes changed files and critical binaries. Native Qt automation is separate
from physical owner pointer/high-DPI acceptance, which remains pending.

## October 3 dependency-safe Model History ordering

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_history_order/app`.
Python-only incremental staging from the verified component-double-click payload;
ComponentModel and ComponentNavigator change. No native rebuild, installer or
published release. Native About retains `03a6f66644488e2b710f94e828155b9b12c23c60`;
release-info and BUILD-VALIDATION identify the application source commit.

Drag History names/icons/status to reorder within the active component. Invalid
drops clamp after the latest predecessor or before the earliest dependent, using
transitive geometry/expression inputs including hidden binders/results. Origin
stays first and cannot move; its planes are protected. Multiple selected and
unselected items preserve relative order, with intervening dependencies retained.
The allowed insertion line and edge autoscroll guide the drop. One undoable
ModelHistory transaction preserves geometry, ownership, links and identities.
Cross-component, stale and active-task/edit moves are refused.

Evidence in the build parent's `validation` folder:
- `history-order-verified`: all 11 new checks pass against source-matching installed
  modules, including 441 insertion plans, native Qt drag/drop/mouse initiation,
  origin constraints, expression inputs, real sketch/Extrude hidden binder/results,
  multiselection, stale identities, edge scrolling, Undo/Redo and .cadprt reopen.
- `history-order-final`: all 29 existing panel, Part Tree move, History and task
  context regressions pass. Ten new checks also passed; the expression fixture
  used reserved unit name A as an unquoted object identifier. The corrected
  label expression passes in the verified run. Earlier fixture evidence is retained.
- Forty distinct native checks pass overall. No source overlays or unexpected GUI
  diagnostics. Final installed modules are verified by source hashes.
- `shortcut-verification.json`: existing desktop shortcut saved, reopened and
  verified against this launcher and app working directory.
- `publication.json`: committed source and matching origin/main identity.

Word preserves all 1534 existing paragraph XML nodes and all package members
except document.xml. Pages 1-45 match the preceding render; changed page 46 was
visually reviewed in `history-order-doc/render` under the task visual root.
BUILD-MANIFEST inherits unchanged verified baseline hashes after size/timestamp
checks, rehashing changed files and critical binaries. Physical owner pointer/
high-DPI acceptance remains separate from the native Qt automation.

## October 3 Components double-click editing

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_component_double_click/app`.
Python-only incremental staging from the modeling-previews payload; only the
installed ComponentNavigator module changes. All previous modeling preview fixes
remain included. Native About retains `03a6f66644488e2b710f94e828155b9b12c23c60`;
release-info and BUILD-VALIDATION identify the newer application source commit.
No native rebuild, installer or published release.

History double-clicks on name/icon or status open the existing operation/feature
editor; sketches enter Sketcher directly. The native viewport event resolves the
current row identity and defers edit startup, avoiding stale pressed indexes when
History is rebuilt between clicks. Dedicated visibility/suppression controls,
single-click selection, component navigation and context-menu Edit are unchanged.

Evidence in the build parent's `validation` folder:
- `before`: reproduces both original failures (status-area operation edit and
  sketch double-click after a row refresh).
- `after`: all 20 checks pass: 13 native panel interactions, four component task
  context cases and three History cases. Includes native Part Box editing,
  sketch edit/reset, Extrude edit/cancel, visibility/suppression/undo, component
  navigation, shared occurrence restoration and save/reopen. No source overlays
  or unexpected GUI diagnostics; the installed module matches source.
- `shortcut-verification.json`: existing desktop shortcut saved, reopened and
  verified against the new launcher and working directory.
- `publication.json`: committed source and matching origin/main identity.

The owner Word document preserves all 1533 existing paragraphs and package
members except document.xml, appending the double-click contract with native
numbering/styles intact. Pages 1-45 match the previous render; changed page 46
was inspected under the task visual root's `component-double-click-doc/render`.
BUILD-MANIFEST records unchanged hashes inherited from the verified baseline
following size/timestamp checks, with changed files and critical binaries
rehashed. Physical owner pointer/high-DPI acceptance remains separate.

## October 3 full modeling overlays and normal result previews

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_modeling_previews/app`.
Python-only incremental staging from the verified combined-modeling payload;
no native rebuild. Native About remains `03a6f66644488e2b710f94e828155b9b12c23c60`.
BUILD-VALIDATION and release-info record the newer application source commit.

Extrude, Revolve, Loft, Pipe, Helix and Primitive use None/Overlay/Result, with
Overlay default. Full native tool geometry is blue/green/red for New Body/Add/
Subtract, independent of missing targets or Boolean contact. A 127 mm subtract
extrusion is untrimmed through a 25.4 mm target; Result shows the evaluated cut
with normal body color/transparency. Extent references remain geometric inputs.
OK, native feature identities, undo and persistence retain their strict contracts.
Shared preview cleanup restores visibility/transparency after switches, errors,
edit and Cancel, while independent curve emphasis is retained.

Validation in the build parent's `validation` folder:
- `preview-final`: six focused cases and seven Revolve regressions pass, covering
  native full-turn Through All overlays as well as six tool backends, missing and
  disjoint targets, full tool shape/volume, automatic colors, all dropdowns,
  dimensional offsets, normal Result appearance and create/edit cancellation.
- `regressions`: 68 of 69 pass on the first run. The only failure is the old
  Extrude New Body expectation of green; source correctly produces requested blue.
- `blue-default`: that corrected case passes, including automatic Through All
  preview and display restoration. The 75 distinct functional checks now pass.
- Existing operation suites cover native geometry/routing, edit, undo and
  persistence; all curve display/selection and 360-pixel task-width checks pass.
- `capture-window` supplies a separate framed overlay/result and dropdown visual
  probe; first capture evidence is retained. No source overlays or unexpected GUI
  diagnostics. Physical owner pointer/high-DPI acceptance remains separate.

The existing desktop shortcut has been saved, reopened and verified against this
launcher and its app working directory. The canonical Word document updates the
preview labels and full-tool requirement, preserves native numbering and other
package members, and adds the shared preview contract. Seven changed/new pages
(35, 37, 38, 41, 42, 43, 46) were inspected; other rendered pages match the prior
document. Evidence: `modeling-preview-doc/render-final` under the task visual root.
The payload manifest inherits unchanged verified baseline hashes after file size/
timestamp checks and rehashes changed files and critical native binaries; the
method is recorded explicitly. `validation/publication.json` records the origin
commit and verified remote branch. No installer or published release.

## October 3 combined native build and temp cleanup

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_combined_modeling/app`.
All enabled Release targets pass using the existing configured compiler tree;
this is an incremental native rebuild with new portable staging, not a clean
compilation. Application and native About identity both match `03a6f6664448`.
Version.cpp was explicitly recompiled and FreeCADBase relinked after regenerating
the version header. The configured workbench scope is retained. The Plus launcher
is newly compiled; installed upstream FreeCAD is not used.

Runtime verification passes 61 distinct checks: 56 combined modeling/UI checks,
the native/source identity check, grid-default check and three cold starts. It
covers all recent curve-list/display, History, compact task, sketch-region,
combined-operation routing/edit/persistence and startup changes. All 37 checked
GUI/component Python modules match source. The first combined run's only failure
was the fixture expecting more than 50 modules; actual hashes and native identity
already matched. The corrected identity-only rerun passes. Keep that original
report alongside the final identity evidence; no application change was needed.
No source overlays or unexpected GUI diagnostics. Curve-list and ribbon captures
were inspected. Physical owner acceptance remains separate.

The existing desktop shortcut targets the new launcher; its saved target and
working directory were reopened and verified. BUILD-VALIDATION records the
individual reports, and BUILD-MANIFEST hashes every packaged file. Build logs,
runtime evidence and `validation/publication.json` are in the parent build folder.
The manifest covers 14,715 files (1,618,295,193 bytes), SHA-256
`ccbc25737eca44047755a68a7a6c79fc277c8c708f423b33fb70c554928349e3`.
Word retains all 1531 previous paragraphs and other package members; pages 1-44
match the prior render, and changed page 45 was inspected (`combined-build-doc`).
No installer or published release.

Requested cleanup removed 742 obsolete entries totaling 36,235,286,833 bytes
(33.747 GiB), including the superseded portable payloads and old validation runs.
`cleanup-summary.json` records exact scope. Historical reports, scripts and CAD
fixtures remain in three CRC-verified, SHA-256-recorded archives: `cleanup`,
`cleanup-build-evidence` and `cleanup-previous` each contain `historical-evidence.zip`.
Archive entries retain paths relative to D:/Temp/Office-PC, so older references
below can be recovered there. Preserve the current compiler tree, LibPack/NSIS
and formatting tools under `freecad-plus-validation-20260928`, the running
`freecad-plus-build-20261002-audit` application (PID 17424 during cleanup), and its
small runtime cache/lock. Unrelated temp files were not removed. All planned
obsolete deletions completed with resolved-path and running-process checks.

## October 3 curve-list selection and Delete

Extrude, Revolve, Helix, Loft and Pipe automatically highlight and scroll to the
latest picked curve in their task lists. A repeated pick removes that curve and
clears list selection. Native picked edges are released after collection so the
same edge can be clicked again without Ctrl; task-owned viewport emphasis remains.
The collector receives keyboard focus so Delete immediately removes highlighted
entries. Its ShortcutOverride prevents document deletion; no selected row means
no action. Pipe spine/auxiliary lists share the behavior, including an empty path
after removing the last edge. Redundant Add selected/Use selected buttons are gone.

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_curve_list`.
Python-only incremental staging from operation_history updates four GUI modules;
no native rebuild. Native About identity remains `f8a4d5c408`. Evidence under
`validation/curve-list-1` passes ten curve-display/list checks, and
`validation/curve-list-regressions` passes 21 profile, operation and context checks.
The focused `validation/curve-list-capture` rerun also passes after waiting for the
viewport repaint and asserting persistent emphasis: 31 distinct checks, 32 passing
executions, no source overlays or unexpected GUI diagnostics. The final capture
shows the highlighted list row and edge, with other sketches gray and unfilled.
Preselection, region boundaries, edit/preview/accept/cancel and source geometry
remain covered. Physical owner acceptance is separate.

The existing desktop shortcut is updated and reopened to verify target/working
directory. BUILD-VALIDATION/BUILD-MANIFEST record inherited native provenance;
`validation/publication.json` records origin/main publication. Word preserves all
1530 prior paragraphs and other package parts; pages 1-44 match the previous render
and the edited page 45 was inspected (`curve-list-doc`). No installer or release.

## October 3 operation entry opens History

Shared component task entry selects History and reveals the Components panel as
Sketch, Extrude, Revolve, Loft, Pipe, Helix or Primitive opens. Preselection and
component/occurrence context remain intact. Four native task-context checks pass,
including twelve operation/tab combinations, hidden-panel Extrude entry, Sketch
editing, previews, accept/cancel and isolated History editing. Evidence is
`D:/Temp/Office-PC/freecad_plus_2026-10-03_operation_history/validation/history-acceptance`;
there are no source overlays or unexpected GUI diagnostics.

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_operation_history`.
Python-only incremental staging from the curve-selection payload changes only
ComponentNavigator; no native rebuild. Native About identity remains `f8a4d5c408`.
The existing desktop shortcut is retargeted and reopened to verify target and
working directory. BUILD-VALIDATION/BUILD-MANIFEST retain inherited provenance;
`validation/publication.json` records origin/main publication separately.
Word preserves all 1529 prior paragraphs and other package members. Its appended
requirement is rendered and inspected in the task's `operation-history-doc` folder.
Physical owner acceptance remains separate; no installer or published release.

## October 3 persistent curve-selection feedback

Component Extrude, Revolve, Helix, Loft and Pipe retain collected-curve highlighting
through selection clearing, field focus, operation editing and solid previews.
Coin annotation overlays reuse the existing non-pickable Ghost renderer. The first
collected input dims other sketches to RGB (0.65, 0.65, 0.65) using scene-only material
overrides and removes their transient region fill. The active profile alone keeps
blue regions when enabled. Ordered Loft sections and Pipe spine/enabled auxiliary
paths retain highlights together. Remove/Clear, source/role changes and OK/Cancel
update or remove emphasis. Original LineColor/PointColor, persisted appearance and
model geometry are not modified by the temporary display.

Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_curve_selection`.
Python-only incremental staging from the grid-default build updates three GUI
modules; no native rebuild. Native About identity remains `f8a4d5c408`, with exact
source and inherited native provenance in BUILD-VALIDATION/BUILD-MANIFEST.
Final evidence: `validation/curve-acceptance` passes 24 cases without source overlays:
seven display cases, twelve profile/extent/selection regressions and five shared
task regressions. Native checks cover one-edge selection, focus/selection clearing,
all shared collectors, Loft sections, Pipe paths, preview/accept/edit/cancel,
placed-component coordinates, clearing and save/reopen without persisted dimming.
Single-edge and solid-preview captures were inspected. The initial display run's
only error was test code reading a QLabel after successful Accept destroyed it;
that assertion was corrected before the final run. Earlier reports are retained.

The existing owner shortcut is updated and reopened to verify the new launcher
and working directory (`validation/shortcut-verification.json`). Word preserves
all 1528 prior paragraphs and other package members; the appended requirement is
rendered and inspected. Document QA is in the task's `curve-display-doc` folder.
Source publication on origin/main is recorded in `validation/publication.json`.
Physical owner acceptance remains separate; no release or installer.

## October 3 Sketcher grid default

`PlusDefaults.py` now seeds native `Mod/Sketcher/General/ShowGrid` to false.
New sketches start with the grid hidden; explicit preferences and saved sketch
visibility remain intact. The native grid toggle and spacing are retained.
Owner payload: `D:/Temp/Office-PC/freecad_plus_2026-10-03_sketch_grid`.
This Python-only incremental update copies the compact-Tasks payload and changes
only PlusDefaults; no native rebuild. Native About identity remains `f8a4d5c408`.
The isolated owner-launcher probe in `validation/acceptance` checks startup
seeding, native sketch edit with grid off, manual grid toggle, the next sketch's
default and preservation of an explicit saved preference. Its capture is reviewed.
The existing desktop shortcut is retargeted and reopened to verify its target
and working directory; evidence is `validation/shortcut-verification.json`.
BUILD-VALIDATION/BUILD-MANIFEST record source and inherited native identities.
Word retains its previous paragraphs, numbering and other package parts; the
edited page is rendered and inspected. Physical owner acceptance remains separate.
Source publication is verified on origin/main; no release or installer.

## October 3 compact Tasks panels

Owner clarified vertical scrolling only. Component Extrude, Revolve, Loft, Pipe,
Helix, Primitive and Sketch/Datum Plane forms now wrap long rows, bound dropdown
size hints, stack vector components and arrange collection actions in short rows.
Reference fields retain usable width with Pick/Clear below; curve lists elide
long text and expose it on hover without horizontal scrolling. The native Tasks
scroller and dynamic Primitive height constraints are retained.

Evidence root: `D:/Temp/Office-PC/freecad-plus-compact-tasks-20261003`.
The incremental Python-only payload copies the prior sketch-feedback owner build
and updates six GUI modules; no native rebuild was needed. Native About identity
remains `f8a4d5c408`; the inherited SketcherGui/PartDesignGui fixes remain intact.
BUILD-VALIDATION and BUILD-MANIFEST record exact application source/module hashes.
Final `acceptance` runs 17 checks through the staged owner launcher without source
overlays: seven native Tasks width/vertical-reachability cases and ten focused
create/edit/preview/selection/sketch regressions. Captures were inspected at
360 logical-pixel dock width. Initial failures identified reference-field sizing
and a test focus-proxy scrolling assertion; both were corrected. Sketch regression
logging now uses App.Console because the GUI launcher has no stderr descriptor.
Earlier failed reports are retained. Physical owner acceptance remains separate.

Word preserves all 1524 prior paragraphs and every other package member unchanged,
adding the narrow-panel requirements and acceptance contract. All 44 pages render;
pages 1-43 match the prior reviewed render byte-for-byte and page 44 was inspected.
Document QA: `C:/Users/Office-PC/.codex/visualizations/2026/10/03/01a101a6-1dcd-7341-88a5-a100bae38e72/compact-tasks-doc`.
The existing desktop shortcut targets
`D:/Temp/Office-PC/freecad-plus-compact-tasks-20261003/FreeCAD-Plus-2026-10-03/FreeCADPlus.exe`;
`shortcut-verification.json` records the reopened target and working directory.
`publication.json` records verified origin/main publication separately. Earlier
owner payloads and unrelated toolbar/document relocations are preserved. No release.

## October 3 ribbon and sketch/Extrude feedback

Source fixes the ribbon's stale dark child palette after tab/workbench changes,
using the current main-window panel color for each regenerated group page.
Native sketches default to unfilled outlines. Component profile tasks enable a
transient light-blue region display; an interior viewport click can choose its
sketch and populate the curve list. Closing the task removes the display, and
save/reopen does not retain it. Extrude deletion removes unconsumed internal
helpers and reveals its sketch when no operation still consumes it; shared
profiles and delete/undo/redo remain intact.

Evidence root: `D:/Temp/Office-PC/freecad-plus-sketch-feedback-20261003`.
The grouped incremental build passes (`build`), including rebuilt SketcherGui
and dependent PartDesignGui. Candidate payload is copied from the prior fresh
owner build, updates those two native modules plus ComponentModel and the four
GUI Python modules, and retains the prior native About identity `f8a4d5c408`.
Exact current source and module hashes are recorded in BUILD-VALIDATION and
BUILD-MANIFEST; the old About identity alone does not identify these changes.

Final focused `acceptance` passes 18 curve-profile/background-result cases through
the owner launcher. `shared-acceptance` passes five Revolve/Loft/Pipe/Helix task
checks (and two earlier ribbon checks). `ribbon-delivery` owns final ribbon
tab/resize checks. No source overlays. Native viewport Qt mouse events select all
four rectangle edges from an initially empty profile; blue-region and unfilled
captures were reviewed. Deleted operations can be recreated from the source,
and shared profiles survive deletion of one consumer. Preserve earlier failed
reports: native property registration order was corrected within the grouped
build, test-only Qt imports/transaction setup were corrected, and palette-only
ribbon attempts were superseded after visual review found stale dark colors.
Physical owner/high-DPI acceptance remains separate; existing Refine/topology
and stylesheet warnings remain in the logs.

Word retains all 1522 prior paragraphs and all other package parts unchanged,
with two owner-requirement paragraphs appended. Rendered 44 pages: pages 1-43
are byte-identical to the prior reviewed render; page 44 was visually inspected.
Evidence: `C:/Users/Office-PC/.codex/visualizations/2026/10/03/01a101a6-1dcd-7341-88a5-a100bae38e72/sketch-feedback-doc`.
The unrelated toolbar/icon relocations and untracked owner material are preserved.

All 25 distinct selected checks pass: 18 profile/result, five shared-task and two
final ribbon checks. The existing desktop `FreeCADPlus.exe - Shortcut.lnk` now
targets `D:/Temp/Office-PC/freecad-plus-sketch-feedback-20261003/FreeCAD-Plus-2026-10-03/FreeCADPlus.exe`;
the saved link was reopened and both target and working directory verified in
`shortcut-verification.json`. Source publication is separate from local owner
delivery: `publication.json` records the verified origin/main identity. Earlier
owner payloads remain intact. No release or installer.

## October 3 fresh all-target owner build

Owner explicitly requested a new build and desktop-shortcut update. Built all
currently enabled Release targets with `tests/BuildComponentDocument.ps1 -AllTargets`
in the existing external build directory, then staged a fresh payload with
`package/WindowsInstaller/stage-freecad-plus.py`. FEM remains disabled in the
existing configuration. No application source was changed for this build request.

Owner payload and verified shortcut target:
`D:/Temp/Office-PC/freecad-plus-owner-20261003-refresh/FreeCAD-Plus-2026-10-03/FreeCADPlus.exe`.
The existing desktop `FreeCADPlus.exe - Shortcut.lnk` was updated and reopened;
target and working directory (the launcher's parent) both match. Evidence root:
`D:/Temp/Office-PC/freecad-plus-owner-20261003-refresh`.

Source and native runtime identity:
`f8a4d5c4083ab09e71f0b45c55e1c5b1064a21bc`. The all-target build initially retained
the old Version.cpp object despite a refreshed generated header. A focused
Version.cpp compile and FreeCADBase relink corrected it; `identity-relink` records
success and the native version. The staged GUI reports the same current commit.
`build` records ALL_BUILD success; `staging.log` records fresh staging. The unchanged
Plus launcher was copied from the prior verified owner payload and its hash matches.

New staged acceptance: smoke passes 12 selected modeling cases (native routing,
create/edit task, downstream/undo/save/reopen for Loft/Pipe/Helix/Primitive), three
recent-file cases and four status-control cases. Bootstrap/Plus/Classic launcher
cold starts each pass: 22 passing executions total, no failures/errors/skips and
no source overlays. Runtime module hashes match source. `selected-test-sources.json`
records the exact selected existing test methods and source hashes. Prior full
modeling acceptance in the preceding build is retained, not counted as rerun.
Native recompute/Refine/topology and stylesheet diagnostics remain in logs;
physical pointer/high-DPI acceptance and the older sketch drawing report stay pending.

BUILD-VALIDATION and BUILD-MANIFEST identify the current source/native commit,
verification phases, shortcut and exact payload file hashes. The manifest contains
14,715 files (1,618,280,238 bytes); manifest SHA256:
`ba3ed6ae8f2cce5b2d7c9379d90d0613a45a5f94123bd6a2258f2b011dd8068c`.
This is an unsigned
local portable build; no installer or release publication was requested.
Word was read first, retains all 1521 previous paragraphs exactly as XML and all
other package parts, and adds one build-validation note. SHA256:
`266d07bb28c955b4e816429f48e38a1beae70e54a8c665e1f639c23c74c54b89`.
Word preservation/render evidence is under
`C:/Users/Office-PC/.codex/visualizations/2026/10/03/01a0ffe3-14ce-75e0-9c71-b39d69d25490/owner-refresh/doc`.
Final render-compact has 43 pages: pages 1-42 exactly match the prior reviewed
render and page 43 was visually inspected. The initial trailing-page draft was
shortened only in the newly appended note; all prior content remains unchanged.

## October 3 Primitive and grouped native build

Primitive now combines all eight native additive/subtractive shape pairs in one
component task under REQ-014e/UI-003e. Shared Native lifecycle supports no-profile
operations and shape replacement. All 16 aliases route to this task in component
documents; Classic Body tasks remain. See tests/ComponentPrimitive.md.

Built PartDesignGui once in the existing external build directory, compiling the
Loft/Pipe/Helix and Primitive adapters. Evidence root:
`D:/Temp/Office-PC/freecad-plus-primitives-20261003`; native-build records success.
The Helix candidate chain was copied and updated with ComponentPrimitive,
ComponentNativeOperation, ComponentLoft/Pipe/Helix, ComponentPrimitiveTask,
ComponentNavigator and rebuilt PartDesignGui. All prior batch modules remain.
Native engine identity stays 6be8eda4246a15590664ba17772a92ec63aaa448.
Candidate was renamed to `FreeCAD-Plus-2026-10-03` under that evidence root for
owner-launcher checks. Prior candidate paths in reports refer to the same bytes.

Final suite selections: native-acceptance Loft 9, Pipe 8 and Helix 9; Primitive in
that initial grouped report failed and is superseded by primitive-verified:
Primitive 7 and inherited Primitive 8. task-layout adds 2 passing final task cases
following the dynamic Wedge minimum-height repair; ribbon 2 and shared-revolve 2
pass. Thus 45 distinct cases / 47 passing final executions before launcher checks.
No source overlays; corresponding module hashes match tested source. Preserve
pilot, native-acceptance and primitive-final failures for diagnosis. Fixes: missing
Deactivated attachment choice, duplicate origin-container pick, compressed Wedge
rows. Fixtures corrected datum role and prism intersection; ellipsoid compares
native Classic geometry because independent Part Boolean integration differs.
Native Refine/topology/stylesheet warnings remain. Valid solids do not certify
successful splitter removal. No physical pointer/high-DPI acceptance is claimed.

Normal Wedge and expanded Cylinder task captures were reviewed; final Wedge rows
are readable. Word preserves all 1518 existing paragraphs exactly as XML and all
package parts except document.xml; three Primitive notes appended. SHA256:
`0e0f5e576f61bfd621552798a27fcd2881c39e1c6864713e86e144cdd944d24d`.
Evidence: `C:/Users/Office-PC/.codex/visualizations/2026/10/03/01a0ffe3-14ce-75e0-9c71-b39d69d25490/primitives/doc`.
Rendered 43 pages; pages 1-42 are byte-identical to Helix render, page 43 visually
reviewed. Three owner-launcher cold restarts (Bootstrap/Plus/Classic) also pass,
bringing the final suite selections to 50 passing executions. Existing desktop
`FreeCADPlus.exe - Shortcut.lnk` is updated and reopened for verification: target
`D:/Temp/Office-PC/freecad-plus-primitives-20261003/FreeCAD-Plus-2026-10-03/FreeCADPlus.exe`,
working directory its parent. `shortcut-verification.json` records success.

Application source: `0eeec1e0e1fb3f61307289a51f6d07379a57e1eb`. The payload
contains 14 changed/new Python modules versus the Revolve owner baseline and one
rebuilt command module. PartDesignGui SHA256:
`e101d821d451138c43d8fd1214466772082949747f16c22d9941cd317de76044`.
BUILD-VALIDATION records the selected passing suites and superseded failures;
BUILD-MANIFEST records exact files and native/application identities. This is an
unsigned local portable owner build, not a release or installer. Earlier dated
source-only build/routing deferrals are superseded by
this grouped validation. Physical input checks and the earlier sketch drawing
report remain pending. Preserve unrelated toolbar/icon relocation, reviews/Archive.

## October 3 unified Helix — source ready for grouped build

`ComponentHelix.py` / `ComponentHelixTask.py` now combine native additive/subtractive
Helix in a component task. Single ribbon action, History/native command routes and
CMake script lists are updated. `ComponentNativeOperation` accepts a single profile
and adapter-owned internal inputs; `ComponentOperationTask` now shares the single
profile collector and reference picking with Revolve. See REQ-014d/UI-003d and
`tests/ComponentHelix.md` for contracts and acceptance procedure.

Candidate: `D:/Temp/Office-PC/freecad-plus-helix-20261003/candidate`, copied from the
Pipe candidate. Added/replaced Part modules: ComponentHelix, ComponentNativeOperation.
GUI modules: ComponentHelixTask, ComponentOperationTask, ComponentRevolveTask,
ComponentNavigator, PlusRibbon. Other runtime provenance remains the Pipe/Loft
candidate chain and verified Revolve owner payload: native engine 6be8eda424 and
the Revolve-built PartDesignGui. This candidate is not an owner delivery.

Evidence beneath `D:/Temp/Office-PC/freecad-plus-helix-20261003`:
`acceptance` passes eight compatible Helix cases. `shared-loft` passes three,
`shared-pipe` three, `shared-revolve` two, `ribbon-final` two. `task-axes` passes
two final task cases after adding direct component X/Y/Z choices and a picked-axis
assertion. Total final evidence: 18 distinct cases, 20 passing executions, zero
failures/errors/skips in these runs, without source overlays. Module hashes match
the respective tested sources. Only HelixTask and PlusRibbon changed after the full
Helix run; their final changes are covered by task-axes and ribbon-final. Normal and
expanded task captures were inspected, including the final reference-axis state.

Retain failed/diagnostic `pilot`, `extended`, `axes`, `final-helix`, `construction`
and `shared-ribbon`, plus passing `placed-axes`. Repairs: whole-sketch preview
placement was being applied twice; native Axis0 links canonicalize to Axis and
must be normalized for editing; selected profiles need an associative construction
axis helper with separate Link/String metadata; the Modeling ribbon had a specific
legacy Helix-menu override. Fixture repairs added missing target/edge recomputes
and used Sketcher constraints instead of the unavailable movePoint API. Native
construction-axis versus explicit-line approximation differed by 1.31e-6 cubic mm;
the volume comparison now uses five decimal places. Native Refine fallback and
startup stylesheet warnings remain recorded; valid solids do not prove splitter
removal. No physical pointer/high-DPI acceptance is claimed.

Word update retains all 1515 previous paragraphs exactly as XML and all package
parts except document.xml; three Helix notes appended. SHA256:
`c3afc5663d68a3248006548a86fdaafd84941f137343075a18ae8671be7e8f1b`.
Evidence: `C:/Users/Office-PC/.codex/visualizations/2026/10/03/01a0ffe3-14ce-75e0-9c71-b39d69d25490/helix/doc`.
Rendered 43 pages: pages 1–41 exactly match the reviewed Pipe render; affected pages
42–43 were visually inspected. The sibling update_doc.py records preservation.

Next grouped build must compile Loft/Pipe/Helix native command adapters and install
all new/shared Python modules. Run full TestComponentHelix (nine cases),
TestComponentPipe (eight) and TestComponentLoft (nine), including native routing;
then deliver and verify the existing desktop shortcut. Batch remaining related
owner requests before this build. Physical pointer/high-DPI and the prior sketch
drawing report remain pending. Preserve unrelated toolbar/icon relocation, reviews
and Archive. Three local Helix catalog descriptions in already-untracked
`ui/TOOLBARS.md` remain with that relocation and outside the source commit.

## October 3 unified Pipe — source ready for grouped build

`ComponentPipe.py` / `ComponentPipeTask.py` provide the unified component Pipe
operation, with single Modeling ribbon action, native command adapters and History
routing. `ComponentNativeOperation.py` extracts Loft/Pipe binding and transactions;
`ComponentSectionTask.py` extracts their ordered section collectors. CMake install
lists include all new modules. See REQ-014c/UI-003c and `tests/ComponentPipe.md`.

Isolated candidate: `D:/Temp/Office-PC/freecad-plus-pipe-20261003/candidate`, copied
from the previous Loft candidate. Updated Part modules: ComponentPipe,
ComponentNativeOperation, ComponentLoft. Updated GUI modules: ComponentPipeTask,
ComponentSectionTask, ComponentLoftTask, ComponentNavigator, PlusRibbon. All other
files retain the previous candidate provenance, including native engine 6be8eda424
and the Revolve-built PartDesignGui. This is not an owner payload or shortcut delivery.

Evidence beneath `D:/Temp/Office-PC/freecad-plus-pipe-20261003`:
`final-pipe` passes seven compatible cases; `path-association` passes the extended
mode-edit/downstream/undo/reopen case after changing the linked path length;
`shared-loft` passes all eight compatible Loft cases; `ribbon` passes two. Total:
17 distinct cases, 18 passing executions, zero failures/errors/skips in these runs,
matching source hashes and no overlays. Only the path-association test changed
after final-pipe; production source did not change. Task captures in final-pipe
were inspected at normal and expanded Auxiliary states.

Preserve `pilot`, `extended`, `native-diagnostics`: initial empty AuxiliarySpine
read failed and was repaired. Native Auxiliary approximates the analytic circle;
Transformed corners have different native volume semantics from Right/Round.
Tests now verify appropriate geometry without changing the engine. Vertex-ended
Pipe fails in the inherited native face reader despite dormant point branches;
the task rejects it clearly. Loft's working vertex binding remains unchanged.
Native scaling laws beyond Constant/Multisection and tangent expansion are still
unimplemented; existing tangent flags persist. Baseline stylesheet/topology
warnings remain in retained logs; no claim of clean stderr or physical acceptance.

Word update retained all 1512 previous paragraphs byte-for-byte as XML and all
package parts except document.xml; three Pipe notes were appended. SHA256:
`d9a505300bbd815a2469ac54799039db472796111d2943f24166dfe3a20676b6`.
Evidence: `C:/Users/Office-PC/.codex/visualizations/2026/10/03/01a0ffe3-14ce-75e0-9c71-b39d69d25490/pipe/doc`.
Render has 42 pages: pages 1–41 exactly match the reviewed Loft render; page 42
was visually inspected. The sibling update_doc.py records the preservation check.

Next grouped build must compile both Loft and Pipe command adapters and install
the new shared modules, then run the full TestComponentPipe (eight cases) and
TestComponentLoft (nine cases), including native routing. Batch remaining
owner-requested operations before this build, then deliver and verify the existing
desktop shortcut. Physical pointer/high-DPI checks and the prior sketch-drawing
report remain separate unresolved gates. Do not repeat passing runtime checks
unless the final sources/runtime change. Preserve the unrelated toolbar/icon
relocation, reviews and Archive. Three local Pipe catalog updates in already
untracked `ui/TOOLBARS.md` remain with that relocation, outside this source commit.

## October 3 unified Loft — source ready for grouped build

`ComponentLoft.py` and `ComponentLoftTask.py` combine native AdditiveLoft and
SubtractiveLoft in a component-owned create/edit task. `ComponentOperationTask.py`
now shares section layout and transient previews with Revolve. Native command
adapters, History routing, single Loft ribbon action and CMake installation lists
are updated. See REQ-014b/UI-003b and `tests/ComponentLoft.md`.

Isolated candidate: `D:/Temp/Office-PC/freecad-plus-loft-20261003/candidate`.
Copied from the verified Revolve owner payload; only ComponentLoft, ComponentLoftTask,
ComponentOperationTask, ComponentRevolveTask, ComponentNavigator and PlusRibbon
Python modules are replaced/added. Native engine/PartDesignGui remain from that
payload. This candidate is not an owner delivery and has no shortcut update.

Evidence beneath `D:/Temp/Office-PC/freecad-plus-loft-20261003`:
`final-loft` passes all eight compatible Loft cases; `shared-revolve` passes two
shared layout/preview cases; `ribbon` passes two layout/action cases. Module hashes
match source and overlays are disabled. Retain earlier `pilot`, `frames`,
`acceptance`, `task-placed`, and `extended` diagnostics: copied whole-sketch frames
initially collapsed preview sections; direct placed-shape copies fixed it. The
first task check accessed a deleted status label after OK; subsequent checks pass.
Stderr contains native topology-hasher warnings also seen in Revolve plus baseline
stylesheet warnings; no assertion failures or skips in the final runs.

Word update preserves all 1509 original paragraphs and every DOCX package part
except document.xml, appending three Loft notes. Document and visual evidence:
`C:/Users/Office-PC/.codex/visualizations/2026/10/03/01a0ffe3-14ce-75e0-9c71-b39d69d25490/loft/doc`.
The revised task screenshot is in `final-loft/loft-task.png` and was reviewed.
The final Word render remains 41 pages: pages 1–40 match the previous reviewed
render exactly; page 41 was visually inspected. SHA256:
`123ff6c86c1546ae36f6d9538d1e4462b20e0c55cc6c6754e7afa1bf4fac7cac`.

Next grouped build must compile PartDesignGui's Loft command adapters and install
the new Python modules, run all nine TestComponentLoft cases (including native
command routing), then deliver/verify the existing desktop shortcut. Batch this
with the transferred owner requests as they arrive. Do not repeat the already
passing geometry suite unless final sources/runtime change. Physical pointer and
high-DPI acceptance remain separate; the prior sketch-drawing issue is unresolved.
Preserve the pre-existing toolbar-catalog/icon relocation and reviews/Archive files;
only this task's files belong in its implementation commit.
The relocated, already-untracked `ui/TOOLBARS.md` has three local Loft-description
updates; its larger owner relocation remains outside the implementation commit.

## October 3 unified Revolve owner delivery

Implemented unified component Revolution/Groove creation and editing in
`ComponentRevolve.py` and `ComponentRevolveTask.py`, with native command/history
routing and the shared associative curve collector. See UI-003 and REQ-014a.

Delivered build and evidence root: `D:/Temp/Office-PC/freecad-plus-revolve-20261003`.
Payload: `FreeCAD-Plus-2026-10-03`. It incorporates the pending datum modules from
the previous candidate, new Revolve modules, ComponentProfile/ComponentNavigator
updates and rebuilt `Mod/PartDesign/PartDesignGui.pyd`. Other native runtime files
remain from the validated October 2 owner payload (engine version `6be8eda424`).
Incremental `PartDesignGui` build passed; `native-build/result.json` and `build.log`
record the external CMake build. App.Version identifies the reused engine, not the
new command module; the package manifest records these separately. Application and
command-module source commit: `0ba687c954bdc7e7454440db0f0fbcaf62806b4a`.

Packaged acceptance: `acceptance-revolve` 7, `legacy-regression` 8 (including the
84-case angular matrix), `task-final` 1, `extrude-routing` 2, `extrude-profile` 3,
`datum-final` 2. All pass without source overlays. The full Revolve suite precedes
only the final start-reset/palette changes, covered by `task-final`. Original
`pilot`, `extended`, `references` and `shared-regression` failures are preserved:
fixture/status-lifetime corrections and per-file test-filter misuse are documented
by subsequent passing runs. Final task screenshot is readable and reviewed.

Owner DOCX requirements updated with all original paragraphs and native numbering
preserved. Rendered 41 pages; pages 1–40 match the previous reviewed render exactly;
page 41 reviewed. Evidence is in the task visualization folder
`revolve-20261003/doc`. Three further launcher cold starts (`launcher/bootstrap`,
`launcher/plus`, `launcher/classic`) pass: 26 passing test executions in this batch.
The existing desktop `FreeCADPlus.exe - Shortcut.lnk` now targets this payload's
`FreeCADPlus.exe`; saved target and working directory were reopened and verified.
`shortcut-verification.json` records the handoff. All retained runtime files match
the previous owner manifest except the six listed Python modules and rebuilt
PartDesignGui module. `BUILD-MANIFEST.json` and `BUILD-VALIDATION.json` record hashes
and the mixed native/source identities.

Archive: `FreeCAD-Plus-2026-10-03-Revolve-Windows-x64.zip`, 662,203,052 bytes.
SHA-256: `6bfe424cf8a966a26fba0f412a241cc915945a9bd6545e57e76a7d3afde03261`.
ZIP CRC verification passes. This is a local unsigned portable owner build, not a
published release. Implementation and delivery records are separate coherent
commits for the authorized origin/main push; remote verification follows the push.
Physical pointer/high-DPI acceptance remains separate.

## October 2 datum plane — incorporated in October 3 delivery

Runtime modules incorporated above: `src/Gui/ComponentSketchTask.py`,
`src/Gui/ComponentNavigator.py`, and `src/Mod/Part/ComponentSketch.py`.
The shared editor serves new-file Tasks and New Sketch; see the roadmap milestone
and UI specification for behavior. No new native type or persistent schema was added.

Isolated candidate: `D:/Temp/Office-PC/freecad-plus-datum-20261002/FreeCAD-Plus-2026-10-02`.
It copies the preceding delivered payload with only those three Python modules
replaced; source overlays are disabled. Acceptance beneath the same root:
`sketch-all` passes 32 tests; `start-actions-settled` passes six. Earlier focused
`datum` passes four checks. Final `datum-layout` checks the settled controls and
invalid-direction recovery after a wording-only task update. Source/runtime hashes
are retained in results.json. The full sketch suite predates only that wording
update and an event-settle addition before its screenshot; targeted final checks
cover both. Preserve these checks rather than repeating unrelated qualification.

Initial startup failures were baseline overlay-host behavior on the no-document
Start page (`pane-baseline`, `pane-probe`). `new-file-probe` confirms Tasks becomes
visible with a document. The test suite now explicitly exercises docked startup
and overlay new-file entry, with native event settling before switching layout.
This does not claim to fix the baseline no-document overlay limitation.

Canonical Word retains all 1505 original paragraphs and adds one workflow note;
headings, automatic numbering and other package parts are unchanged. Render has
41 pages: pages 1–39 match the previous PNGs; pages 40–41 were visually checked.
SHA256: `e409d3f790a39ae3d305c852f393e3bbc2930e9a2bf447e4e393020fc04ef804`.
Document/render evidence: visualization workspace `datum-plane-20261002`.

This is source/runtime validation for the next grouped delivery, not a new owner
build. The existing owner shortcut and verified archive below remain unchanged.
Physical acceptance and the earlier sketch drawing report remain separate.

## October 2 latest batched owner build

The latest batch incorporates every completed runtime change through application
source `4cbb196bee7e985cb11ab36f78c5380acc9af1a5`. The verified native engine remains
`6be8eda4246a15590664ba17772a92ec63aaa448`; this is a compatible Python update,
not a new native compilation. The only runtime changes from the audit payload are
PlusRibbon, PlusDefaults, ComponentNavigator, ComponentModel and UtilsAssembly.
All five hashes match source. Exact Home/Modeling/Sketch/Assembly/View, master-first
trees/unused assemblies and screenshot defaults are now incorporated. Later queued
feature requests are not represented as implemented by this delivery.

Delivery root: `D:/Temp/Office-PC/freecad-plus-build-20261002-batch`.
Launcher: `FreeCAD-Plus-2026-10-02/FreeCADPlus.exe` beneath that root.
The existing desktop `FreeCADPlus.exe - Shortcut.lnk` was retargeted and reopened:
target is that launcher; working directory is its containing payload folder.
`shortcut-verification.json` records both verified values. Earlier builds remain intact.

Archive: `FreeCAD-Plus-2026-10-02-Batch-Windows-x64.zip` beneath the delivery root,
662,190,500 bytes. SHA256:
`c2e805877416da93c54bef1ca00a0d11ddf8740a79728d7fc23fbb55773d83bd`.
All 14,703 archived entries passed ZIP CRC verification. `BUILD-MANIFEST.json`
records file hashes; every unchanged runtime file matches the preceding validated
audit payload. `artifact-result.json` records completed archive verification.

Acceptance: 57 passing checks without application source overlays or unexpected GUI
diagnostics. The full ribbon run retained 25 successes; its old Pattern-dropdown
assertion failed, was corrected to the exact owner layout and passed in
`acceptance/ribbon-pattern`. Component models/tree moves/display passed 26 checks.
`acceptance/sketch-menus` passes New File/New Sketch/OK, line/circle/arc/rectangle,
solver and `.cadprt` save/reopen. The first sketch run expected native QAction
identity instead of the captioned menu proxy; the test now triggers the actual menu
entry. Both original failed reports are preserved. Defaults preserve explicit saved
choices and support preset overwrite; three actual launcher cold starts pass
Bootstrap/Plus/Classic preference persistence. `build-validation-summary.json`
and each `acceptance/*/results.json` retain exact hashes, paths and test provenance.

The reported physical sketch drawing failure is still unresolved. Native Qt input
acceptance is separate from physical pointer acceptance; the earlier capture/input
tool limitation is not an app fix. The previous audit's 131 checks and native
baseline qualification are retained evidence, not rerun claims for this batch.

Canonical Word update preserves 1504 original paragraphs except the targeted View
validation sentence and appends one delivery note; headings, automatic numbering
and all other DOCX parts are unchanged. Render remains 40 pages: only pages 32 and
40 changed and were visually checked; the other 38 PNGs match the previous render.
Word SHA256: `bf23a9f5cc86c65140d01838d39495376b6c2d40a6bf3feb11e6b91c0c64915f`.
Evidence/scripts: visualization workspace `build-batch-20261002`.

This latest delivery supersedes historical pending-incorporation notes below.
Focused commits and origin milestone pushes remain required. Existing unrelated
toolbar-catalog/icon relocation changes are preserved outside this delivery commit.

## October 2 Plus sketch drawing investigation — unresolved

Owner reports that New File / New Sketch opens the line task but viewport drawing
fails. No application fix is claimed: the failure did not reproduce in native Qt
input tests. Added `TestComponentSketchWorkflow.test_plus_new_file_sketch_and_viewport_curves`
covering actual Plus New File/New Sketch/OK controls, ribbon curve actions, viewport
hit testing, line/circle/arc/rectangle creation, solver and `.cadprt` save/reopen,
without forcing the camera or directly entering edit mode.

The new regression passed once against the audit payload without application source
overlays, and once with only latest PlusRibbon source loaded. Separate line probes
passed with fresh preferences and a copy of the saved FreeCADPlus profile. Existing
owner preferences remain unchanged. Evidence: visualization workspace
`sketch-drawing-20261002` (`full-path`, `source-ribbon`, `qt-hit-test`, `owner-profile`).
The first probe used global widgetAt while the app was not foreground and found no
receiver; it is not evidence of an application drawing failure.

Physical pointer validation remains blocked: Computer Use approval initially timed
out; a later launch resolved to the separately installed Plus app and was excluded
from validation. The verified audit executable was then launched directly with an
isolated profile. Its graphics capture failed (`FrameArrived timed out`), and its
accessibility-click attempt failed (`coordinate input geometry is unavailable`).
No app input or drawing acceptance was inferred from these failures. Await owner
clarification of whether axes/preview were visible when drawing failed. Do not mark
this issue fixed or use this regression as a substitute for the reported failure.

Canonical Word validation note updated without changing existing paragraphs,
headings or numbering. No new owner build, shortcut change or release.

## October 2 exact Design View ribbon — source ready

Design View now has exactly View and Individual Views: 14 buttons, with the
requested seven Standard Views and seven Draw Style choices in order. Native
camera actions, draw-style checks, shortcuts and enablement are retained. Other
modes retain their existing View presentation. Owner DOCX and UI references agree.

Five focused native GUI tests passed with only PlusRibbon loaded from source,
including all seven real camera orientations, native draw-style action checks,
narrow-window access, tab routing and Classic/Plus visibility. Process exit was
zero and final stderr empty. Evidence: visualization workspace
`view-layout-20261002`; the first isolated launch failed before tests because its
IPC cache directory was missing, corrected with the documented isolated temp path.
Word retains all 1502 original paragraphs, headings, numbering and other ZIP parts;
40 pages rendered, pages 1–31 unchanged and affected pages 32–40 visually checked.
Next batched owner payload incorporation and physical owner acceptance remain
pending; this milestone does not deliver a new executable or change the shortcut.

## October 2 exact Design Assembly ribbon — source ready

Assembly has exactly Assembly and Assembly Joints: 22 buttons and three dropdowns
with nine ordered choices. Individual joints remain exposed; Belt Join invokes the
native Belt Joint. Local captions preserve native actions and state. The shared
menu helper now serves both Sketch and Assembly. An Assembly edit-exit guard
prevents task watchers calling a missing method on a retiring view provider.

Sixteen selected source-overlay ribbon checks passed against the packaged engine;
the two affected Assembly checks then passed on final source with empty stderr,
including actual Create Assembly, selection/context states and dropdown routing.
Evidence: visualization workspace `assembly-layout-20261002`, final `guard-verified`.
Canonical Word outline updated, all original paragraphs/heading/numbering and other
package parts preserved; 40-page render checked, changed pages 30–31 inspected.
Owner toolbar/UI references synchronized. Next batched build and physical acceptance
remain pending; existing owner executable, ZIP and shortcut are unchanged.

## October 2 exact Design Sketch ribbon — source ready

Sketch now has exactly Sketcher, Edit Mode, Geometries, Constraints, Tools,
B-Spline and Helpers, with all 66 listed buttons and 16 dropdowns (57 menu choices).
Individual line/dimension/coincident/point-on-object/horizontal/vertical options
are retained alongside menus. Text is Experimental; Group Constraint is Development
preview. Each menu preserves the requested captions/order and native action
execution, enabled/checked states. No solver, geometry, task-field or Classic
preference changes. Existing shortcuts remain native.

Fourteen focused packaged-engine GUI checks with explicit PlusRibbon source overlay
pass without failures/errors/skips: exact buttons/groups/menu choices, edit-mode
routing and native states, dimension options, Home/Modeling regressions, compact grid
and Plus/Classic exclusion. Native actions are exercised through routing probes;
this is ribbon evidence, not a new geometry-workflow acceptance claim. Evidence:
`sketch-layout-20261002` under the visualization workspace. Owner toolbar/UI/Word
requirements synchronized; original DOCX paragraphs/headings/numbering preserved
and affected rendered pages reviewed. Next batched build and physical acceptance
remain pending; existing owner executable, ZIP and shortcut are unchanged.


## October 2 exact Design Modeling layout — source ready

Sketch, Modeling, Dress-Up and Transformation groups now match the owner list;
Primitives is one dropdown with Box, Cylinder, Sphere, Cone, Ellipsoid, Torus,
Prism, Wedge and disabled Tab (no native creation binding yet). Loft/Helix retain
native Add/Subtract menu choices behind one icon until combined workflows exist.
Linear/Circular Pattern are separate native buttons. Primitive uses the native
default additive primitive. No geometry or task-field changes.

Eleven focused packaged-engine GUI checks with explicit PlusRibbon source overlay
pass without failures/errors/skips, including exact groups/buttons, labels, enabled
states, every primitive choice routing, preserved Home, compact grid and exclusive
Plus/Classic styles. Source provenance asserted in `modeling-layout-20261002`
under the visualization workspace. Toolbar/UI references and canonical Word
requirements updated; original paragraphs, headings and numbering preserved,
rendered pages reviewed. Existing owner executable, ZIP and shortcut unchanged.
Next batched build and physical acceptance remain pending.


## October 2 exact Design Home layout — source ready

Home now contains only Main (New Component, Add Component), Modeling (Extrude,
Revolve, Fillet/Chamfer) and Sketch (New Sketch, Coordinate System), in that order.
Fillet/Chamfer shares a split button. Coordinate System offers Coordinate System,
Plane, Axis and Point with local captions and native execution/enablement.
Ten focused packaged-engine GUI tests with explicit PlusRibbon source overlay pass.
Common toolbar and specialist tabs remain. Word owner content/headings/automatic
numbering are preserved; rendered changed pages reviewed. Evidence: visualization
workspace `home-layout-20261002`. Source awaits the next batched build; existing
owner executable, ZIP and shortcut unchanged.

## October 2 master component convention — source ready

Owner reauthorized the previously deferred tree convention. `ComponentModel`
orders definitions by permanent RootComponent identity and supplies master-first
tree roots with unused assemblies below it. `ComponentNavigator` keeps that tree
independent of editing/view roots and routes selection, visibility, instance
deletion and moves through each row's assembly context. No extra master instances
are created. New File's existing automatic master and native Delete guards remain.

The final isolated packaged-engine run with explicit source overlays passes
26 Models/Part Tree/display-context tests with no failures/errors/skips. It covers
New File and master deletion protection, stable ordering while editing, unused
assemblies/children, selection, deletion, Cut/Paste, Undo/Redo and save/reopen.
Evidence: `master-tree-20261002/acceptance-final/results.json` and `tests.log`
under `C:/Users/Office-PC/.codex/visualizations/2026/10/01/01a0f9bd-b85a-7aa3-a6b7-cb05c64fdabd`.
Source provenance is asserted in the harness; existing native command callbacks
share the source panel in this test process. Earlier harness failures are retained.

Contract/UI specification and programming index are synchronized. The canonical Word
specification now includes the convention, merged against the latest owner version
during the Home-layout task. Original paragraphs, headings and automatic numbering
are preserved; rendered affected pages reviewed.

Source changes await the next batched owner build; the existing runtime, ZIP and
shortcut remain unchanged, and physical owner acceptance is pending.

## October 2 screenshot preferences and Word specification

The closed owner audit build's isolated `AppData/Roaming/FreeCADPlus/user.cfg`
now contains the 71 requested preferences for General, Selection, Display Colors
and Sketcher Appearance. Native profile reload verifies every value; separate
native checks verify fresh defaults, preserving saved choices and explicit reset.
`src/Gui/PlusDefaults.py` seeds this preset for future builds. The existing runtime
payload and ZIP are unchanged; incorporation and GUI preference-page acceptance
remain for the next packaged build. Existing build/shortcut evidence below is retained.

Root AGENTS.md now requires updating `ai-instructions/ui/FreeCAD Plus UI & UX.docx`
for every owner change while preserving owner edits, headings and automatic numbering.
Its Defaults section contains the screenshot preset and maintenance rule; the
33-page render is checked (pages 1–31 unchanged, revised 32–33 visually inspected).
Backups and native verification reports are in task output `default-settings-20261002`
under `C:/Users/Office-PC/.codex/visualizations/2026/10/01/01a0f9bd-b85a-7aa3-a6b7-cb05c64fdabd`.
The separately installed FreeCAD profile was not changed. The component-tree
convention was deferred during that settings task and implemented in the later
source milestone above after the owner reauthorized it.

## October 2: conversation audit — owner build ready

The owner opened the earlier source `52495b0cb2` payload, which lacks the compact
grid. Both earlier folders remain intact. Use the audit payload:

- Launcher: `D:\Temp\Office-PC\freecad-plus-build-20261002-audit\FreeCAD-Plus-2026-10-02\FreeCADPlus.exe`
- ZIP: `D:\Temp\Office-PC\freecad-plus-build-20261002-audit\FreeCAD-Plus-2026-10-02-Audit-Windows-x64.zip`
- Application sources: `ca244c0335d95bf4e2127d8d77aa107cd535a838`.
- Native engine reused: `6be8eda4246a15590664ba17772a92ec63aaa448`; no C++ rebuild is claimed.
- ZIP bytes: **662,182,921**; SHA256:
  `4b5df882b1f419c432b3c92b6d44efa981a80d49b48a57a03ef8e3a56bcf78e8`.
- Desktop `FreeCADPlus.exe - Shortcut.lnk` target and working directory are saved
  and reopened/verified against this launcher. Mandatory delivery gate is in
  AGENTS.md/DEVELOPMENT_GUIDE; the update tool preserves other shortcut settings.

**Implemented:** common small File/Edit/Clipboard bar above the ribbon; 40/20/16px
full/medium/small icon hierarchy; medium Home Main and curated domain groups;
Design Assembly tab; Coordinate System dropdown; Std_NewComponent creates an
embedded definition with zero occurrences and opens its editing tab. Native
Isometric binding corrects the invalid draft alias. Specialist actions initialize
only after the main window is visible, preserving Classic visibility at cold start.
The [conversation audit](DEVELOPMENT_ROADMAP.md#october-2-conversation-and-payload-audit)
records each requested UI/workflow change. Toolbar governance is regenerated from
this payload: 644 command IDs, 616 native PNGs, 11px reference icons and valid local
links/anchors. Python/PowerShell syntax and whitespace checks pass.

**Packaged acceptance:** **131 passing executions**, no failures/errors/skips or
source overlays in accepted reports: ribbon/all-installed-mode 19; component
feedback 44; sketch workflow 27; component pane/tree/layout/Tasks/status/recent 35;
cold sketch reopen 3; three owner-launcher startup processes. Fresh Plus/Blender/
Imperial defaults and saved Plus/Classic visibility persist. New-model creation,
Undo/Redo and save/reopen pass. The native launcher is the same FreeCADPlus.exe
that the owner shortcut targets. Captures come from the actual packaged Qt UI.

**Integrity:** all 14,702 non-cache payload files are hashed; only PlusRibbon.py
and ComponentNavigator.py differ in runtime folders from the validated 6be8eda
baseline. All other runtime hashes match that baseline. Source module hashes and
loaded payload provenance are recorded; final ribbon/launcher checks use final
GUI bytes. The 14,703-entry ZIP includes the manifest and passes CRC verification.
Metadata separates application/native source identity and marks native rebuild as
false. Earlier native Pattern geometry and ALL_BUILD evidence are retained,
not described as rerun. Evidence: audit root's `acceptance`, `toolbar-reference`,
`build-validation-summary.json`, `shortcut-verification.json`, `artifact-result.json`;
payload BUILD-VALIDATION/BUILD-MANIFEST/release-info.

Failed ribbon draft (invalid Std_ViewAxonometric), two cold-start attempts and a
detached-launcher harness attempt remain in evidence, excluded from accepted
counts. Corrected command, visible-window initialization and detached-aware runner
pass. No upstream patch import, installer, signing or publication occurs. The
recorded upstream compatibility review answers the earlier check request;
candidate integration is separate. FEM/printing-addon execution and physical
owner acceptance remain conditional/separate as documented in the audit.

## October 2: toolbar document revision (historical; superseded by audit build)

[TOOLBARS.md](details/ui/TOOLBARS.md) now separates Classic toolbar inventory,
proposed Plus mode/tab/group placement, consolidations and the final function
catalog. Classic rows contain one command each with 11px reference icons. The
owner's common toolbar above the ribbon and medium/half-size treatment are
recorded; the incomplete outline is filled with proposed native command groups,
including Design Assembly while retaining Sketch. New Component remains a
proposed entry with binding pending under the component contract.

Validation: all 638 prior catalog command IDs remain in the 644-command catalog;
615 referenced native PNGs, local links and button anchors resolve. Generator
syntax, section ordering and whitespace checks pass. These are documentation
checks. No application source, runtime payload or packaged acceptance is changed;
the revised layout awaits implementation and native GUI acceptance.

## October 2: updated owner build completed

The owner-authorized update incorporates all queued application changes through
`6be8eda4246a15590664ba17772a92ec63aaa448`. The earlier October 2 runtime/ZIP at
application source `52495b0cb2` remain intact. The updated local test build is:

- Launcher: `D:\Temp\Office-PC\freecad-plus-build-20261002-update\FreeCAD-Plus-2026-10-02\FreeCADPlus.exe`
- Portable ZIP: `D:\Temp\Office-PC\freecad-plus-build-20261002-update\FreeCAD-Plus-2026-10-02-Windows-x64.zip`
- ZIP bytes: **662,180,525**; SHA256:
  `67e73d17a4dee6d03f60da2ce83e4da0254167c5dcae0b228f3821c4b727feeb`.
- Evidence: the update root's `native-build`, corrective native compile/relink
  directories, `final-acceptance`, `toolbar-reference`, `build-validation-summary.json`
  and `artifact-result.json`; packaged `BUILD-VALIDATION.json`/`BUILD-MANIFEST.json`.

**Implementation:** compact primary/secondary/dropdown ribbon hierarchy; New File
native icon/caption; exclusive Plus/Classic toolbars; audit Datums/Variable Set/
Macro access, fallback icons and Drawing page priority; restored native Circular/
Path/Point Pattern commands; startup Components above Attributes at 2:1; idle
Tasks actions; recent-only native Start; status controls; Blender/Imperial Decimal
fresh defaults with saved choices preserved. Acceptance also corrected Circular
Pattern registration after its Polar parent, native Start/PySide wrapper lifetime
and empty-view focus, hidden first-run setup construction, signal emission while
populating native Start unit/navigation controls, and full-ray region picking
through origin helpers. Foreground solids block picks; geometry behind the
sketch does not. Runner phases reset Feedback-only state and reject both native
C++ exception diagnostic types.

**Native build:** ALL_BUILD passes in the existing Windows x64 Release cache,
with `BUILD_START=ON` and `BUILD_TUX=ON`; other configured modules are retained.
Focused corrective compiles/relinks are recorded separately. A version-only
refresh follows functional acceptance and stamps native 26.3.0 / 49231 Git,
branch main, commit `6be8eda4246a15590664ba17772a92ec63aaa448`; final launcher
verification confirms this identity. No separately installed upstream FreeCAD is
used. FEM remains disabled in this configuration.

**Packaged behavioral/GUI validation:** 138 executions / 136 distinct checks pass
without source overlays, failures, errors, skips or unexpected GUI exception
diagnostics. Selected phases: component feedback 44; component tab input/lifecycle
10; Part Tree rearrangement 9; sketch workflow 27; cold sketch reopen 3; ribbon 16;
three preference-persistence startup processes; recent cards/open/empty/focus 3;
status controls 4; startup dock layout 4; idle Tasks actions 5; native Circular/
Path/Point geometry 10. Module provenance is verified. The final version-stamped
launcher passes native imports and save/reopen. Recent-files and ribbon captures
are reviewed. All 14,702 non-cache staged files are hashed; runtime folders match
build bytes, and ZIP entries pass CRC verification. The unchanged launcher is
reused from the earlier owner payload; its source has not changed.

The governing toolbar reference is refreshed from this executable: 638 command
IDs, 608 native PNG icon renders, and all three restored Pattern bindings. This
inventory does not claim functional acceptance of every inherited command.

**Delivery/publication:** local portable test build ready for owner testing;
no installer, GitHub release or publication is performed. Physical owner acceptance,
broader topology coverage and the earlier intentional inherited solver skip remain
separate gates. Failed diagnostic attempts remain in the evidence folders with
corrective outcomes above; they are not counted as final accepted phases.

The queued-source entries below are historical and superseded by this completed
build checkpoint.

## October 2: toolbar audit corrections queued in source

Audit follow-through restores Datums and Variable Set to Home Structure and Macro
to one compact Home dropdown. Drawing's primary-page ID is corrected from absent
TechDraw_NewPageDefault to native TechDraw_PageDefault. Ribbon-only fallback icons
prevent icon-only buttons from rendering blank when native actions lack artwork;
native QAction icons and state remain unchanged. Native compound-menu separators
are omitted from selectable choice lists.

Circular/Path/Point pattern geometry and task support already exist, but their
commands, view-provider files, module registration and CMake entries had been
removed. The upstream command blocks and six view-provider source/header files
are restored exactly (normalized newline comparison against b9609745048b), with
module/CMake registration and Classic menu/toolbar entries. Plus places these
variants in the primary Pattern dropdown and retains unified linear/circular,
Mirrored and MultiTransform. No geometry implementation is changed.

Fourteen native Qt/source-overlay ribbon checks pass with no failures/errors/skips
and clean runner diagnostics in
`D:\Temp\Office-PC\freecad-plus-toolbar-audit-fixes-20261002\complete`.
The ten existing native Circular/Path/Point geometry checks also pass in the sibling
pattern-core directory. These prove existing kernel behavior, not restored GUI
bindings. Source equality, Python syntax and document links/anchors are checked.
The refreshed governing toolbar reference identifies pending native bindings.

No native target, owner runtime or ZIP was rebuilt/changed. Next authorized build
must compile/package the restored files and run testRestoredNativePatternBindings
plus the complete packaged ribbon suite and Pattern geometry suites. Follow the
owner procedure for native variant acceptance, Undo/Redo and save/reopen; preserve
the existing native General preference and cold-start acceptance gates.

## October 2: toolbar governance and visual catalog

The owner requested a governing Markdown reference by workbench. The
[toolbar reference](details/ui/TOOLBARS.md) records shared desktop groups and 20
workbench sections, Classic upstream groups, Plus changes/consolidations, Plus
tab/section placement and a final function catalog (638 command IDs, with native
compound choices expanded). It embeds 605 native-rendered PNG icons and links to
source SVGs for source-only commands. UI_UX_SPEC owns shared interaction/sizing;
the new reference owns detailed toolbar placement and points back to those rules.

Metadata was exported from the existing fork executable in an isolated hidden
session to `D:\Temp\Office-PC\freecad-plus-toolbar-reference-20261002`.
Twelve workbenches were registered; eight additional workbench definitions were
read from source and clearly marked unvalidated/not packaged. Classic definitions
use recorded upstream revision `b9609745048b`, with native default branches for
unchanged Python/Sketcher groups. Current source PlusRibbon supplies projection.
The document distinguishes missing newer upstream Pattern commands from actual
linear/circular unification, and keeps Part's separate mode/Tools routing clear.

Source export/generation tools are under tools/. All document links, icon paths
and command anchors resolve; every catalog row has a function description. Both
tools parse successfully. This is documentation/inventory validation, not a new
functional command test or build. The owner runtime/ZIP remains unchanged.

## October 2: mutually exclusive toolbar styles queued in source

Owner screenshot shows native Classic bars alongside the Plus ribbon. Previous
suppression ran only during rendering and skipped bars whose toggle actions were
already hidden, allowing later native Show/layout events to reveal them again.
PlusRibbon now guards toolbar Show events, hides native bars even when their
toggle actions are unavailable, and restores the Plus ribbon after a saved layout
hides it. Classic rejects attempts to show the ribbon. Same-choice Apply also
enforces the selected style. Workbench transitions hide the ribbon while restoring
outgoing native state, then suppress native bars before showing Plus again.
Per-workbench Classic visibility is retained independently of forced suppression.

Twelve native Qt/source-overlay ribbon checks pass with no failures/errors/skips
in `D:\Temp\Office-PC\freecad-plus-ui-exclusive-20261002\complete`.
New regressions cover late native Show events, newly created toolbars, restoring
a Classic saved layout while Plus is selected, attempts to show Plus in Classic,
and external Sketcher/Draft/Part Design activation. Existing checks cover command
states, mode/tab routing, dropdowns, compact grids and Classic visibility recovery.
Initial runs exposed restoration errors; corrected source passes the complete
batch. Evidence is retained. Native General Apply/Cancel and cold-start packaged
acceptance remain deferred to incorporation; no owner runtime or ZIP was changed.

## October 2: status controls and defaults queued in source

The supplied screenshot shows Notifications (blue icon/unread count), the upstream
Tux navigation indicator and the native Dimension/Unit System menu. Notifications
and Units already exist in the current fork runtime; navigation was omitted by
`BUILD_TUX=OFF`. DEVELOPMENT_GUIDE now enables Tux and removes it from disabled
modules. Existing caches must explicitly use `-DBUILD_TUX=ON` on the next authorized
build and package generated Tux_rc resources and Python modules.

New PlusDefaults initializes unset navigation to Gui::BlenderNavigationStyle and
unset units to the native ImperialDecimal schema (currently 3). FreeCADGuiInit
calls it before module initialization, and CMake packages it. Explicit saved
choices remain unchanged. Native viewer/preferences/Start-setup/info fallback
defaults also change from CAD to Blender; the Tux indicator uses Blender fallback.
Unit formatting uses the existing native service; internal geometry identities,
millimeter storage and saved document UnitSystem overrides are unchanged.

Four native/source-overlay Qt checks pass with zero failures/errors/skips and a
clean process exit in
`D:\Temp\Office-PC\freecad-plus-status-controls-20261002\complete`.
Checks confirm all three visible menus/icons, native notification delivery/menu
opening/unread reset, Blender/CAD menu changes applied to the actual viewer,
Imperial Decimal defaults on new documents, inch formatting, global versus
document unit changes, and preservation of explicit user choices. The status-bar
capture was reviewed and matches the supplied controls. Initial test assumptions
about the generic notification QPushButton, unit enumeration labels and notification
tree/timer were corrected; earlier evidence is retained.

The source Tux navigation module was loaded with isolated generated Python icon
resources (`resources/Tux_rc.py`, generated by the pinned LibPack rcc). No native
target was built and no owner runtime/ZIP file was changed. Native C++ fallback
compilation and automatic early initialization/full Tux packaging are still pending.
During the next authorized build, run `-StatusControlsSmoke` without overlays and
check fresh-profile defaults plus preference reset in the staged application.

## October 2: recent-only startup prepared; native acceptance pending

StartupLayout queues a native Start-page presentation after the dock layout.
`show_recent_files` reuses Start_Start/StartView, its RecentFilesModel, card
delegate, metadata/thumbnails and native opening handler. It selects the Documents
page and hides New File creation choices, examples, custom-folder cards and setup
footer controls. New File/Open remain in Tasks. Recent files preserve native order;
an empty list gets a message. Repeated calls are idempotent and do not take focus
from a file opened by startup arguments/scripts. Recent-list model signals queue
the empty state after the native refresh finishes changing visibility.

The delivered October 2 runtime and configured development cache have
`BUILD_START=OFF`. No StartGui module is available to validate native cards, so the
initial attempt reported ModuleNotFoundError. The startup helper now reports that
missing build dependency and preserves independent startup workflows. Updated
DEVELOPMENT_GUIDE explicitly enables Start and removes it from disabled modules.
During the next authorized build, reconfigure the existing cache with
`-DBUILD_START=ON` and package the Start App/Gui modules/resources.

Evidence: `D:\Temp\Office-PC\freecad-plus-recent-files-20261002`.
`adjacent` passes all five existing Tasks source-overlay checks with no
failures/errors/skips and clean process exit. `native-unavailable` records three
explicit skips for the missing native module; the runner correctly rejects this
as acceptance. Tests cover recent-only/empty startup even with conflicting old
preferences, native card order and opening a `.cadprt` fixture, idempotence and
preserving an already-open file's focus. Run `-RecentFilesSmoke` on the next
staged build and require all three to pass without skips. No recent-page visual
or native opening acceptance is claimed now. No runtime/ZIP was rebuilt or staged;
the owner's explicit incorporation instruction remains outstanding.

## October 2: idle Tasks actions queued in source

Startup Tasks shows New File and Open with no active document, regardless of the
saved workbench. Clicking New File runs native Std_New and enters Design; idle
component Tasks then shows New Sketch, Coordinate System, Datum Plane and Add
Component, in that order. Compact buttons share native QActions, icons and states.
The idle panel lives in the native watcher page without replacing its watchers or
the native task-dialog stack. Editing shows the existing native operation dialog;
legacy documents and other modes retain their native watcher tools.

Five source-overlay native Qt checks pass, zero failures/errors/skips and clean
process exit, under
`D:\Temp\Office-PC\freecad-plus-start-actions-20261002\final-state`.
Covers exact initial/new-file captions, untitled001/Part001 creation, native action
identity (including Open), New Sketch handoff/cancel, coordinate-system and datum
creation/ownership/native OK, Add Component, no-workbench/saved-Draft startup and
return after closing files, native legacy/Draft watcher visibility, and a single
active Components panel. Open's native file-picker interaction is not automated.
Initial test runs exposed unfinished datum test transactions, an unhandled test
name prompt and mixed runtime/source navigator globals; those harness issues were
corrected. Earlier evidence is retained. Startup/new-file captures were reviewed.
The four existing dock-layout checks also pass under `layout-regression` beside
that evidence. The older ribbon in these screenshots belongs to the untouched
October 2 executable; the compact ribbon source remains queued separately.

No runtime/ZIP files were staged or rebuilt. Packaged cold-start acceptance and
owner visual acceptance remain for the next explicitly authorized build update.

## October 2: component startup layout queued in source

Components initializes when commands register, without needing an open document.
A one-time main-window Show callback runs after native saved-layout restoration,
places Components above Attributes in the left dock column, makes both visible,
and sizes their available height in a 2:1 split. Previously floating, hidden or
tabbed layouts are corrected. Subsequent document/panel shows preserve user resizing.

Four native Qt source-overlay checks pass with zero failures/errors/skips and a
clean process exit in `D:\Temp\Office-PC\freecad-plus-pane-layout-20261002\final`:
empty startup/new document, prior floating/tabbed placement, user resizing and
idempotent command registration. The workspace capture confirms the arrangement.
The source callback is exercised against the October 2 fork executable with isolated
preferences. Full packaged cold-start acceptance remains for the next build.
No runtime, launcher or portable ZIP was modified; incorporation into the October
2 build remains deferred until the owner requests it.

## October 2: compact ribbon source changes awaiting owner incorporation

Owner explicitly directs that new changes be made in source and incorporated into
the October 2 build only when requested. PlusRibbon now uses a single row of large
primary buttons spanning three small-icon rows. Primary buttons are 76 x 76 logical
pixels with 32-pixel icons and bounded captions; secondary buttons are 24 x 24
with icon-only presentation. Commands align in three-row grids, retaining section
labels and horizontal overflow. Clear primary captions include New File, Add part
and Auto Dimension without renaming shared native menu actions.

Extrude/Revolve, Pattern/Fillet and selected common workflow actions have priority.
Specific dimensions share an Auto Dimension menu, including vertical, horizontal,
angle, radius and diameter, with other native dimension choices retained. Additive
and subtractive Loft/Pipe/Helix variants share secondary dropdowns; rare Help
commands share a menu. Existing native compound menus and QAction state/shortcuts
are preserved. The action hierarchy is recorded as a standing rule for every new
or modified interface in UI_UX_SPEC and DEVELOPMENT_GUIDELINES.

Nine source-overlay Qt checks pass, zero failures/errors/skips and process exit
zero: `D:\Temp\Office-PC\freecad-plus-ribbon-compact-20261002\final-caption`.
Covers grid positions/sizes, bounded height, native action identity/state, dimension
and rare-choice menus, actual Home commands, mode/tab/task routing, workbench
initialization, narrow-window scrolling and Classic visibility restoration.
Final Home/Modeling/Sketch captures were reviewed.
Visual review found an initial Qt caption override; the final button class restores
its separate caption after default-action assignment and native action changes.
Explicit New File/Add part label checks now pass, and inherited fonts are measured
after parenting controls. The native preference-page
payload test is deliberately excluded from this source-only run; it remains part
of the next owner-authorized build validation. No native build or runtime staging.
The October 2 launcher, ribbon runtime file and portable ZIP remain unchanged.
Physical gestures, themes and broader DPI acceptance remain separate.

Follow-up owner request: the ribbon now uses native `Std_New` (the standard
`document-new` icon) with the exact caption **New File**, replacing the component
icon presentation. Native Std_New already dispatches Std_NewComponentDocument, so
the component-document workflow and Ctrl+N are preserved. This remains a source
change queued for owner-authorized October 2 build incorporation.
The focused Home/native-action check passes in `new-file-icon` beside the ribbon
evidence above; the capture confirms the document-with-plus icon and New File
caption. No build files were changed.

## October 2: new owner test build

All implemented application changes through `52495b0cb2` are incorporated in a
separate Windows x64 Release runtime:
`D:\Temp\Office-PC\freecad-plus-build-20261002\FreeCAD-Plus-2026-10-02`.
Run `FreeCADPlus.exe`; no installation is required. The launcher uses the fork's
FreeCADPlus user-data folder. Includes the component naming/inventory/occurrence
changes, Part Tree/History/Attributes, protected background results, selected-region
Extrude, Plus/Classic UI and the complete New Sketch plane workflow.

The existing configured build was incrementally rebuilt with **ALL_BUILD**, covering
every enabled native target, Python script and resource. Show visibility helpers
are staged for this configuration. `native-build/build-result.json` records exit
zero. Staging uses the established runtime-only packager with a local build label
and CMake configuration; no release version or GitHub release was assigned.

The generated version header identified the current source, but the cached native
version object still reported `802e19d648`. A focused Version.cpp compile and
FreeCADBase relink corrected that metadata. The final staged launcher now reports
`49218 (Git)`, branch main and hash `52495b0cb2bdbfe1a8c47cb2e7336761b93f3a2c`.
Compile/link evidence is under `version-refresh`; initial evidence is retained.

Final staged-copy acceptance: **103 passing executions, 101 distinct tests**,
zero failures/errors/skips, nine clean GUI process exits and no source overlays.
Under `final-acceptance`: feedback 44 (current Python hashes/native Attributes),
sketch 27, sketch-cold 3, pane interactions 10, Part Tree moves 9, ribbon 7, and
three successive one-test startup phases (fresh Plus default, persisted Plus,
persisted Classic/toolbars). The launcher separately passes native workbench
imports, save/reopen and exact runtime/revision checks using isolated configuration
files. Final feedback has no TopoShape hasher-mismatch diagnostics; prior warnings
remain recorded, without assigning a cause or closing general topology gates.
Plus History/Part Tree and Classic Models captures were inspected for requested
tab labels, component inventory and the protected hidden Origin Planes child.

`build-validation-summary.json`, payload `BUILD-VALIDATION.json` and
`BUILD-MANIFEST.json` identify this checkpoint. Portable artifact integrity is
recorded separately in `artifact-result.json`; the archive is
`FreeCAD-Plus-2026-10-02-Windows-x64.zip` beside the runtime folder.
All 14,688 non-cache staged files are manifested; every staged runtime file matches
the rebuilt output. The ZIP contains 14,689 files including that manifest, passes
CRC verification, and is 661,552,451 bytes. SHA-256:
`3b118311f131feee9248806b3e5613a7fbd3c7883138a863620557f9006daf36`.
Owner documents/preferences and installed upstream FreeCAD were not modified.
FEM remains disabled in this established configuration. Physical owner acceptance,
general topology qualification and the earlier intentional inherited solver skip
remain separate; this acceptance subset has no skips. No installer or publication.

## October 2: complete sketch workflow regression batch

Owner requested rigorous sketch creation, attachment, active/reference curves,
active/reference dimensions and geometric constraints, plus plane creation inside
New Sketch. The task now offers User plane and Create new plane beside native
origin-plane and planar-face choices. Creating a plane exposes origin/face/user
base, signed offset and X/Y/Z rotations; OK creates a component-owned native datum
plane and attached sketch in one creation transaction, then enters Sketcher.
Cancel creates neither. Plane001 numbering is local to each component. New origin
and user-plane sketches use native ObjectXY attachment; face sketches use FlatFace.
Existing detached sketches are unchanged. See UI-011 and
[the reproducible sketch procedure](../tests/SketchWorkflow.md).

Also fixed origin-plane preselection and support-plane region picking: a visible
plane supporting a sketch had blocked its Extrude interior-region clicks. The
picker now permits that support helper; unrelated solid occlusion still rejects.
The native viewport test records an actual Plane hit, selects Edge1 and accepts a
5 mm extrusion at its 7 mm support offset. Existing occlusion checks still pass.
Two profile fixtures now change AttachmentOffset rather than the evaluated
Placement of their newly attached sketches.

Final evidence: **173 distinct passing checks in 22 test modules**, one intentional
inherited solver skip, zero assertion failures/errors. Six GUI processes exit zero;
no source overlays or unexpected GUI lifecycle diagnostics. Repeated component
panel/task suites are counted once. Beneath
`D:\Temp\Office-PC\freecad-plus-sketch-rigorous-20261002`:
- `final-workflow`: 27, including native Qt drawing of line/arc/rectangle and
  construction circle; five saved curve families, six dimension kinds on active
  and construction geometry, native driving/reference creation and conversion,
  radius value-dialog Accept/Cancel, eight native geometric constraint commands,
  tangent/symmetry, unit expressions, external projection and support recovery.
- `final-cold`: three, including standard Open, saved reference/constraint flags,
  native editor entry, moved-plane downstream recompute/Undo/Redo and plane reuse.
- `final-feedback`: 44; `final-regression`: 44; `final-core`: 39. Covers owning-file
  task return, geometry/history/ownership, support and constraint repair, native
  Validate Sketch, freedom guidance, reuse, Trim mouse gestures and persistence.
- `final-solver`: 24 attempted, 23 pass. The inherited driving circle-to-line
  secant test is explicitly skipped because support remains under discussion.
  The strict runner correctly marks this run incomplete rather than suppressing
  the skip. All other assertions pass; the application process exits zero.

A fully constrained rectangle with a construction diagonal/reference dimension
updates its Extrude volume from 1000 to 1500 mm3, measured diagonal and Undo/Redo,
then preserves semantic identities and attachment through `.cadprt` reopen.
The cold process moves its saved plane and verifies the solid follows. Screenshots
`new-plane-options.png` and `constrained-reference-sketch.png` reviewed: support
controls, fully constrained status, green active curves, construction diagonal and
blue reference dimension are visible.

Native first-dimension autoscaling creates separate Add radius constraint and
Scale geometries Undo entries. Both Undo/Redo steps and Cancel are verified; this
existing native behavior is preserved. Earlier fixture/API mistakes and a hidden
standard-Open dialog timeout are retained. Corrected hidden-dialog attributes and
deferred-widget cleanup allow the three final cold checks to finish normally.

Three TopoShape hasher-mismatch diagnostics are retained in final-feedback stderr.
No tested identity, geometry or link assertion failed. Focused result deletion/Undo
and nonmutating preview audits passed without reproducing those messages; their
cause remains unproven. General topology-naming qualification remains open under
7.8.5b. Deliberate conflict/redundancy and protected-delete fixture diagnostics are
expected. `sketch-validation-summary.json` records all outcomes without hiding the
skip or these kernel messages.

Three Python modules synchronized into the existing September 28 build:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Native binaries are unchanged; no native rebuild needed. Runtime paths/hashes
match source, and the desktop shortcut target is unchanged. Final SHA-256:
- ComponentSketch.py: `1A3868CB704B2E3B357613D1CFDBFFECDBA9A731EBDB64FBA1C1823045EBC354`
- ComponentSketchTask.py: `FAF2527F12880A7AD5509F9AC00F696D295A95933283D0D5FA928EACBAEC88EE`
- ComponentExtrudeTask.py: `073189DCD774F4BC8F196BEE337F864A2329FCC1CB1B26D65A1BBA5F75B2B132`
- FreeCADGui.dll unchanged: `CA6554BCE9C5168A2B2344472134BE5759B3E8CDB6A425C66693F4880E604949`

Owner documents/preferences and installed upstream FreeCAD were untouched.
Automated Qt/native command coverage is separate from physical gestures, other
DPI/themes and exhaustive combinations of every Sketcher tool. No installer,
tag or release publication. Creation and the requested automated validation are
complete; remaining topology/physical acceptance gates are explicitly separate.

## October 2: rigorous Components pane regression validation

Models, Part Tree and History pass **139 distinct automated checks in 25 test
modules**, across seven clean native GUI processes with source overlays disabled.
Coverage includes model inventory/counts, root/occurrence ordering and deletion,
rename and isolated editing, visibility, suppression, references, conversion,
clipboard/drop rearrangement, Undo/Redo, shared/external definitions, `.cadprt`
save/reopen, task transitions and close/reopen lifecycle. Ten focused interaction
workflows use Qt mouse events, deferred context actions, 60 refresh/tab cycles,
24 shared nested uses, unused definitions and narrow Plus/Classic captures.
See [the reproducible procedure](../tests/ComponentPaneValidation.md).

Six application defects found and corrected:
- Active Origin axes/planes intercepted viewport Extrude region picking; helper
  hits now permit sketch projection while actual occluding geometry still blocks.
- Models root editing could change context while a task was open; it now refuses.
- Closing the last document retained stale navigator context; keys/path reset.
- Deferred refresh invalidated context-menu row objects; actions resolve stable
  row identities and reject changed document contexts when triggered.
- Sketcher activation could render Plus Ribbon before its Python workbench handle
  existed; rendering is deferred until initialization completes.
- Detached MDI views retained enabled document/camera commands during deferred
  destruction, causing camera exceptions and an access violation; capabilities
  now reject detached views and camera-less renderers.

Incorporated in the existing September 28 build at
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The desktop shortcut target is unchanged. Grouped App/Gui/resources/PartGui/
PartDesignGui/SketcherGui/PartScripts build and subsequent GUI detached-view repair
both succeeded. The native General-page Plus default fallback is now compiled.
Build evidence is in `native-build` and `native-build-detached-view` beneath
`D:\Temp\Office-PC\freecad-plus-pane-rigorous-20261002`.

Final test directories beneath that evidence root:
- `native-feedback`: 44; `native-integration`: 24; `native-core`: 39.
- `native-movement`: nine; `native-input`: ten; `native-ribbon`: seven.
- `native-cold-fixed`: six, including standard New/Open and detached-view commands.

`pane-validation-summary.json` aggregates the seven runs: no failures, errors or
skips; every process exited zero. Runtime modules load from this build and match
source hashes. The runner now rejects unhandled camera exceptions, uninitialized
workbench handles and deleted Qt row diagnostics rather than accepting assertions
alone. Earlier failing runs are retained; deliberate missing-file, protected-delete
and inactive-geometry fixture messages are expected. Screenshots were reviewed
for readable Models/Part Tree/History layouts and protected Origin Planes hierarchy.

Final SHA-256:
- FreeCADGui.dll: `CA6554BCE9C5168A2B2344472134BE5759B3E8CDB6A425C66693F4880E604949`
- PartGui.pyd: `49BD0C13A727C74D4AFE09F6835F521864A0DE1A53301B9BA75C1C465951F4E2`
- PartDesignGui.pyd: `BE85C06A3FA2CAB968BA0CD49F4A6C7C2B8D046BEDED68AA2FFCB03DD346AD32`
- SketcherGui.pyd: `C09C763F03894D7A415B88CBD8AAC9FEE84BD29891C7B8B5DD053BBDDD8DF399`
- ComponentNavigator.py: `208DEEDB278BEA675142145B084E16DD35B7C1189E19E38F05A7C4F0A10EAE72`
- ComponentExtrudeTask.py: `94A8051C87C8F7377872E9B6B66DBEC6B6A92B581D853A48F48CC598FD14DEF8`
- PlusRibbon.py: `E98486A6C71AACC282B83D128CDA3872901BD70B8B321E67A852E36CCBD0E297`

Owner documents/preferences and installed upstream FreeCAD were untouched. Qt
input/native drop events establish automated coverage; physical desktop gestures,
other DPI/themes and very large assemblies remain separate acceptance. Existing
physical owner milestones remain open. No installer, tag or release publication.

## October 2 follow-up: Plus UI is the default

Owner requests Plus UI by default. The startup service initializes an absent/empty
ToolbarUIStyle setting to Plus and preserves explicit Classic choices. Initialization
also makes the existing native General page display Plus consistently without
requiring another C++ rebuild. Its source fallback is changed to Plus for the next
grouped native build. Updated PlusRibbon.py synchronized into the closed 9/28 build;
no owner preference file changed and no native rebuild required for this behavior.
Three native cold processes pass in `D:\Temp\Office-PC\freecad-plus-default-cold-20261002`
(Bootstrap, Plus, Classic): fresh Plus default, persisted Plus and retained Classic
with prior toolbar visibility. The previous grouped build evidence remains valid
for unchanged binaries; the script default is superseded by this update.

## October 1-2 grouped update: Plus UI / Classic UI and queued component feedback

Owner-authorized ribbon UI is implemented and incorporated into the existing
September 28 build, together with 7.8.7v/w/x/y root ordering, Part Tree/History,
reference operation, Cut/Paste/drag/drop and Origin Planes/deletion protection.
Edit > Preferences > General > UI style offers Plus UI and Classic UI. Classic
remains the default until selected; Apply/OK switches immediately and persists.
Plus adds the mode selector and Design Home/Modeling/Surface/Sketch/Mesh/View
ribbon tabs, grouped native commands and horizontal scrolling. Non-Design modes
reuse Home/Tools/View plus their workbench sections. Installed modes are discovered
from registered workbenches, including conditional FEM and printing addons.
Current payload modes: Design, Assembly, CAM, Draft, Material, Part, Spreadsheet,
Drawing and Test Framework. BUILD_FEM is off and no printing addon is registered;
no empty placeholders or new addon installation. Native QAction ownership,
enablement, checked states, dropdowns and command lifecycle are retained. Native
getAction now initializes actions lazily for commands not previously presented.
Classic toolbar visibility is preserved across workbench switches and cold restart.

Grouped incremental App/Gui/resources/PartGui/PartDesignGui/SketcherGui/PartScripts
build succeeded in `D:\Temp\Office-PC\freecad-plus-ribbon-build-fixed-20261001`.
The initial build in `freecad-plus-ribbon-build-20261001` exposed a const-pointer
error in the previously queued Origin guard; corrected before resuming the same
directory. Initial overlay smoke fixtures used activeDialog as an object and did
not wait for native delayed action updates; corrected. A modal Add Component test
process was stopped and replaced with controlled input-dialog answers. Failed
evidence retained. Four initial overlay workflows passed before native validation.
Final mode mapping was synchronized after the resource target; exact hashes agree.

62 distinct native checks pass without source overlays:
- Six ribbon command/mode/tab/Classic/task/narrow/dropdown/native General Apply/
  Cancel checks in `freecad-plus-ribbon-final-20261002` (prior same six pass in
  `freecad-plus-ribbon-native-20261002`; final repeats add settled preference captures).
- Three successive cold processes in `freecad-plus-ribbon-cold-20261002`:
  Bootstrap, Plus and Classic preserve style and previous hidden toolbar state.
- 44 navigator/context checks in `freecad-plus-ribbon-components-20261002`, including
  the compiled Origin/plane Delete guard with Python routing bypassed and mixed
  selections, reference command, sketch display/Cancel, context, save/Undo and recovery.
- Nine movement checks in `freecad-plus-ribbon-tree-move-20261002` cover native
  clipboard/drop events, grouped/multiple moves, placement, Undo/Redo and persistence.

Home/Modeling/narrow and native General captures reviewed. Runtime module evidence
reports matching source hashes and paths within this build, including PlusRibbon.
The desktop `FreeCAD.exe - Shortcut.lnk` still targets this build's bin executable;
use the same shortcut. No owner preference file was changed: tests used isolated
configurations. Physical keyboard/theme/DPI and owner workflow acceptance remain
pending; no installer, tag or release publication.

Payload SHA-256:
- FreeCADGui.dll: `60854FFAA3BF37068DE40EB53F02664F9175D52193A978FDC9C8ED8A402C7F7B`
- PartGui.pyd: `1D231AE3A425507EFEF4828B729FFCDF1FAC0E175E6E2DFA0C91F585759D2463`
- PartDesignGui.pyd: `164262752BED3CAEC984366356375ADBA97E4C6602F8F181C457E612833DD898`
- PlusRibbon.py: `A070A57C0B2D10CCC9F0DFD2F79964AD50D99A116FE2B55720749B95EBC147CE`

## October 1 follow-up: Origin Planes and permanent datum protection (7.8.7y)

History now expands Origin to an Origin Planes child row controlling the existing
native XY/XZ/YZ planes together. Component entry keeps Origin visible and planes
hidden; manual changes persist through refresh. Showing planes reveals the parent
as needed. Visibility is transactional and undoable. The child is a view projection
with a distinct row key, not a new document object or reference identity. Both
rows remain always active and have no suppression, rename or deletion actions.
The native Delete command filters component-owned origins and their datum children
before dependency/force deletion. Its existing occurrence adapter also clears
protected native and occurrence-path selections before generic deletion.

44 source-overlay navigator/context checks pass in
`D:\Temp\Office-PC\freecad-origin-planes-final-20261001`, including two new checks
for child visibility, native plane grouping, Undo/Redo, manual-show refresh,
permanent menus, direct origin/plane selection protection and standard/key Delete.
Existing New Sketch plane display/picking/Cancel, external editing, display and
save/Undo workflows pass. The initial run's only failure was an erroneous test
fixture call to a missing root_row helper, removed before the final run; initial
evidence retained. Python syntax and whitespace checks pass. Native CommandDoc.cpp
guard compilation and forced-dependency acceptance remain pending.
Ten focused pane checks also pass in `freecad-origin-planes-pane-20261001` after
selecting History for the pane capture; Origin/Origin Planes nesting was reviewed.

Owner-running 9/28 payload remains unchanged (PID 8140). Batch Gui/native plus
scripts/resources with 7.8.7v/w/x when closed, then run AssemblyStructureSmoke
without source overlays and check forced native deletion and visible child row.
No build staging, installer or publication performed for this follow-up.

## October 1 follow-up: Part Tree Cut/Paste and drag/drop (7.8.7x)

Source adds Part Tree context-menu Cut/Paste, Ctrl+X/Ctrl+V and viewport drag/drop
with row-edge insertion indicators. Cut stages stable occurrence paths without
deleting links; Paste/drop moves the existing links in one transaction. Drop onto
a part reparents, above/below inserts siblings, empty space appends at the root.
Root remains fixed; grouped/multiple selections move without duplicate models.
Native occurrence-frame transforms preserve placement in the chosen context;
existing destination instance numbers are reserved. Active moved descendants stay
in edit context. Shared definition child changes apply to all uses, as before.
Preflight refuses stale/cross-file selection, cycles, driven/scaled links, consumer
relationships and path display overrides for reparenting. Ordering within the same
parent remains permitted with references/overrides; general relationship remapping
is not claimed. Source contract, UI, tests and summary synchronized.

Seven initial focused checks passed twice after changing refresh to take Python
ownership of rows before disposal. Earlier repeated native tree.clear() rebuilds
crashed with PyGILState_Release errors; native-widget/event-filter and deferred
refresh changes alone did not fix that. Failed evidence retained in the earlier
freecad-tree-move-* directories. Final nine focused checks pass in
`D:\Temp\Office-PC\freecad-tree-move-complete-20261001`, including sixteen repeated
reparent operations, existing-number collisions, clipboard keys, native drag/drop
events, above/below/empty-space routing, grouped moves, world placement, active descendants, reference/override/
cycle/stale refusal, Undo/Redo and save/reopen. The broader 42 source-overlay checks
pass in `D:\Temp\Office-PC\freecad-tree-move-regression-20261001`.

The owner-running 9/28 executable remains PID 8140 at final inspection. No payload
replacement, native build, installer or release occurred. Batch script/resource
staging with 7.8.7v/w while closed; run TreeMoveSmoke and AssemblyStructureSmoke
without source overlays against that payload. Physical drag gestures and acceptance
remain pending; synthetic native events are automated GUI evidence only.

## October 1 follow-up: Part Tree/History, reference operation and origin (7.8.7w)

Owner requests Models / Part Tree / History tab names, Add Reference Object as an
operation button rather than a right-click creation action, and the active origin
visible by default in History. Source registers PartDesign_AddReferenceObject
through the existing GUI startup registration; native Part Design and Part menus/
toolbars place it beside Extrude. It reuses direct-child evaluated-source picking
and transactional creation, supports Cancel and is blocked during another task.
Repair/change-source actions for existing references remain. Native object/property,
dock, command and Python member identities retained (structure/history internally).

Origin becomes visible on component/occurrence context entry, including root,
isolated tabs and document reopen. Refresh preserves a deliberate eye hide until
re-entry. Native Full Component projection includes the visible origin; Bodies Only
continues to use its existing geometry-filter contract. Source UI/contract/ADR and
owner tests synchronized. The owner-running 9/28 app is untouched (PID 8140).

Source-overlay validation: eight focused Models/root/reference/origin checks pass
in `D:\Temp\Office-PC\freecad-part-tree-history-focused-20261001`; 42 navigator/
context workflows pass in `freecad-part-tree-history-final-20261001`. Tests exercise
real registered command invocation, Cancel, task blocking, source ownership,
origin default/manual hide/re-entry, tab names and absent context creation, plus
linked selection/task/display/save/Undo/externalization/recovery/BOM behavior.
Initial attempt to mock the extension Control.activeDialog raised an unsupported
setattr error and that validation process crashed; replaced with a real task dialog.
Repeated panel/combined workflows pass. Failed evidence retained. Pane captures
reviewed; native toolbar compilation and physical acceptance remain pending.

Batch with 7.8.7v when the app is closed: native PartGui/PartDesignGui plus GUI
resources/scripts; verify the reference button in both workbenches, run
AssemblyStructureSmoke without overlay and feedback checks against that payload.
No installer/release or running-build update.

## October 1 follow-up: Assembly Structure root restored (7.8.7v)

Owner requests the top-level part as the first Assembly Structure component.
Source now displays the view's root (Part001 by default, custom labels retained)
as the permanent first row, with linked instances beneath it. It starts expanded;
subsequent user expansion state is retained. Edit returns to the root path.
Root Delete/instance menu actions cannot remove the definition; linked instance
counts are unchanged. Empty assemblies retain the root row. Contract/UI/ADR and
existing row-based regression fixtures updated for this hierarchy.

The owner has reopened the 9/28 executable (PID 8140 at inspection). No running
payload files were replaced and no native rebuild/staging occurred. Source-only
isolated fork tests with FREECAD_PLUS_PROFILE_SOURCE=1 pass: 41 navigator/context
checks in `D:\Temp\Office-PC\freecad-assembly-root-context-20261001` and seven
focused Models/root tests in `freecad-assembly-root-expanded-20261001`. Root-first,
custom rename, empty state, root editing/Delete, linked deletion/Undo/reopen,
selection, display, tasks, file/save/Undo routing, BOM and Add Component exercised.
Native Attributes/Delete compiled behavior remains the preceding build's evidence;
these checks do not establish the new root projection in the owner-running payload.
Next grouped script/resource staging while closed: run AssemblyStructureSmoke
without overlay, including the root/context regression. Physical acceptance pending.

## October 1: pending feedback incorporated into the closed 9/28 build

The owner closed FreeCAD and authorized incorporation/testing. The existing
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build` now contains all
pending component feedback, including 7.8.7k and 7.8.7m-u. The desktop
`FreeCAD.exe - Shortcut.lnk` target and working directory were verified to point
to this build's `bin\FreeCAD.exe` and `bin`; use that same shortcut. Owner
preferences were preserved; validation used hidden fork processes and isolated
user/system settings. No installer, release or publication was performed.

Grouped native App/Gui/PartDesignGui/SketcherGui/resource/PartScripts/AssemblyGui/
AssemblyTests build completed. The initial 30-minute wrapper deadline expired
while dependencies were still compiling, without a compiler error; all child
processes exited before resuming the same incremental directory. The build runner
now accepts bounded `-TimeoutMinutes`; completion with 45 minutes passed in
`D:\Temp\Office-PC\freecad-feedback-build-20261001-completion`. Subsequent
script/resource staging passed in `freecad-feedback-build-20261001-title-fix`,
`freecad-feedback-build-20261001-integration-fixes`, and
`freecad-feedback-build-20261001-closed-view-fix` under that same temp parent.
The configuration has BUILD_SHOW off; the runner stages its required Python
visibility helpers. Source checkout and binary cache source agree.

Native validation (no source overlay):
- `freecad-feedback-validation-20261001-final`: 39 feedback checks, exact runtime
  payload hashes/paths for all eleven loaded changed modules, and compiled native
  Attributes title/hidden tree verification. Covers actual New Sketch/OK commands,
  three origin planes, numbering/local duplicate-label permission, selected curves/
  connected regions with holes, native extrusion limits/offsets, colored previews,
  protected background results, Models/Assembly deletion, task and selection context.
- `freecad-feedback-integration-20261001-final`: all 24 display/edit/externalization/
  file/reference-recovery/save/Undo/BOM checks pass.
- `freecad-feedback-core-20261001-verified`: all 39 ownership/geometry/conversion/
  suppression/copy/persistence and Draft/CAM/TechDraw consumer checks pass. Loaded
  backend/GUI modules verified in the build and equal source; TestComponentDocument
  no longer unconditionally puts repository Python ahead of built modules.

Validation found and fixed native document title digit stripping (explicit Label),
wrong-window isolated-view context assignment, closed-view cache reuse after native
name reuse, and copied definition labels colliding with copied occurrences. The
reference-error expectation follows its numbered label; conversion tests explicitly
refresh delayed reference snapshots before publishing downstream evaluated geometry.
The final 102 automated checks pass with process exit zero. Expected refusal/broken-
fixture/suppression diagnostics are retained; no unresolved callback exceptions.
Compiled UI captures for origin planes, flat Models and green/red Extrude volumes
were reviewed. Physical owner acceptance and broader unscoped workflows remain
separate; roadmap acceptance boxes stay open. Native validation evidence/logs and
failed intermediate directories remain under `D:\Temp\Office-PC`.

SHA256 payload identities:
- FreeCAD.exe: `784D47E370F6E25EBC4674AB630C044DE665E19B8EE83D0041F066742DAD7AB6`
- FreeCADApp.dll: `2F7F705F89AAB1449DF9BA192512AB0EE30469FA4F7A58A83142608EA84B3F3C`
- FreeCADGui.dll: `96C60B1F008599588D18A6116AEE8CB9F369AF319A07C3881E2E9B5F7894FAEC`
- PartDesignGui.pyd: `27CBD3A92F86A55FB21F9ED78AFB269637FAE41B822EAACA161856AA137713D5`
- SketcherGui.pyd: `CF370F118D1C2CF2CC108CBC66620B500B118D61EC97AA9842721178D44652DA`

## Earlier source-only feedback evidence (superseded by incorporation above)

Pending owner feedback 7.8.7u replaces the duplicate public definition/occurrence
hierarchy. Components tabs: Models (flat, first), Assembly Structure (linked rows
only, no root model row), Model History. Models retains owning-file unused models
and referenced external definitions; counts expand linked nested uses from the file
root (root context itself has zero instances). Edit opens unused models; Add Instance
reuses them in the active model. Attributes retains the native View/Data editors;
ComboView keeps only hidden native tree infrastructure, with existing identifiers
preserved for saved layouts. Native Std_Delete routes precise occurrence selections
through ComponentNavigator.delete_selected_instances and refuses definition deletion.
Context/key deletion is source-validated: remove owning links, retain definitions/
geometry/UUIDs, clean owning-file representation overrides, invalidate local missing
references, restore nearest active parent. Shared-parent child deletion applies to
all parent uses, as before. Six ModelsPaneSmoke source-overlay workflows pass,
exit 0/empty stderr in `D:\Temp\Office-PC\freecad-models-pane-20261001-undo`:
one-add/one-row, flat inventory/counts, Attributes tabs/hidden tree, all-instance
deletion/Undo/reopen/reuse, nested counts/reference missing-source Undo/Redo,
keyboard deletion, active fallback, unused editing and standard-delete Python adapter.
Models/Assembly screenshots reviewed. Four BackgroundResultSmoke checks also pass
in `D:\Temp\Office-PC\freecad-models-background-20261001` (expected deletion warning).
Prior navigator tests updated for root-row removal; syntax/whitespace checks pass.
No staging/build/publication. Next grouped Gui/resource build must validate native
ComboView/Attributes, Std_Delete adapter/definition guard, then ModelsPaneSmoke,
selection/display/context/task/save/recovery suites without overlay. Broader external
deletion/representation/consumer acceptance remains pending; running payload unchanged.

Pending owner feedback 7.8.7t: generated solid Body results are protected background
objects, hidden in native Model/Model History. The producing operation renders the
solid and supplies public visibility/edit/delete controls. Stable result geometry,
UUIDs, lineage and reference targets remain intact; operation picks map to results.
Existing results adopt display; frozen dumb Bodies remain public. Deleting an
operation cleans unused results in the same Undo transaction; referenced results
retain unavailable identity for repair. Python GUI deletion veto tested; native
Std_Delete also filters forced internal-result deletion before dependency prompts.
Four source-overlay BackgroundResultSmoke checks pass in
`D:\Temp\Office-PC\freecad-background-result-20261001-final4`: actual Std_Delete,
Undo, hidden rows/paths, visibility, adoption, conversion, suppression, downstream
Subtract and .cadprt reopen. Expected deletion warning only; no callback exceptions.
Ten CurveProfileSmoke regressions pass in
`D:\Temp\Office-PC\freecad-background-result-parity-20261001-final` (empty stderr).
Native guard unbuilt/unverified: include ComponentResultView.py in the grouped
update, run both suites without overlay and check linked/copy/externalized display.
No staging/publication; owner-running build unchanged.

Pending owner feedback 7.8.7s: root default Part001; embedded/nested definitions
use the next available Part002/003/etc. within the document. Add Component's Name
prompt is pre-filled and remains editable. Open/saved labels, external definition
labels and custom names are reserved. Occurrences reuse the definition label;
native duplicate-label permission now also covers marked component-owned
Occurrences, assigned before linking/naming so they do not acquire a new part
number. Existing labels/identities are not migrated. Source-only native New/Add
command checks, nested/gap/reserved/custom numbering and .cadprt identity reopen
pass in `D:\Temp\Office-PC\freecad-default-part-names-20261001-overlay`.
That isolated old-engine check enabled duplicate labels only in its test profile
to simulate the pending native occurrence permission; it does not validate the
compiled narrow permission. LocalNameSmoke adds a default-preference regression
for definitions/repeated occurrences/legacy uniqueness. Native App build, that
regression and AddComponentSmoke remain pending the grouped update. No staging
or publication; owner preferences and running build remain unchanged.

Pending owner feedback 7.8.7r: new-document default basename/title untitled001,
then untitled002, etc., reserving open native names, labels and saved basenames
case-insensitively. Explicit labels and root component labels remain separate.
Actual Std_New twice passes with repository ComponentModel loaded only in an
isolated process; both native names/titles match, FileName remains empty and a
custom Bracket label remains. Evidence: `D:\Temp\Office-PC\freecad-untitled-default-20261001`.
No staging/build/publication; queued for the same feedback batch.

Pending owner feedback 7.8.7q restores component Extrude parity. The task uses the
existing native PartDesign::Pad extrusion engine directly in the component (no
PartDesign::Body container), exposing one/two dimensions, symmetric total length,
Dimension/To first/To last/Up to surface/Up to shape/Through all, independent
second-side extents, signed start/end offsets, start reference, taper, numeric
custom direction, normal-length measurement, refinement and automatic preview.
Filled green previews show added volume; red previews show removed material,
with temporary target transparency restored on change/Cancel/OK. Existing simple
Part::Extrusion and Boolean operations remain readable; reviewed editing migrates
to the native engine while preserving operation/result UUIDs and Undo/Redo.
Selected profiles are native Part2DObjectPython helpers retaining the sketch's
signed normal/local frame through exact rigid transforms; earlier face-only
helpers could invert an XZ sketch normal. Ten source-overlay CurveProfileSmoke
workflows pass, exit 0 and empty stderr, including placement/center/volume checks,
all extent types, surface movement, offsets, custom direction/taper, edit migration,
Undo/Redo, save/reopen, actual native OK, automatic preview colors and appearance
cleanup. Evidence: `D:\Temp\Office-PC\freecad-extrude-parity-20261001-frame3`;
green/red captures reviewed. Syntax/whitespace checks pass. No build staging or
publication; owner-running payload unchanged. Next grouped build must include
ComponentExtent.py/ComponentProfile.py and GUI resources, then rerun without
source overlay and perform relevant selection/history/copy/externalization checks.
Physical acceptance and downstream face-reference/copy behavior remain pending.

Pending owner feedback batch also includes 7.8.7p: selected sketch curves for
component Extrude. The task lists curves with Add selected curves, Remove, Clear
and Use all; clicking a filled sketch region collects its outer and hole contours.
All selected contours must belong to one sketch, be closed/non-self-intersecting,
and describe one connected region with optional holes (owner clarification).
An internal native LinkSub profile retains the subset through recompute/edit/save.
Four source-overlay CurveProfileSmoke workflows pass against the September 28
fork engine, including native mapped edge picks, filled-region hits, rotated
sketch/component placement, actual task OK, volume/parameter updates, invalid
contours, Undo/Redo and .cadprt reopen. Process exit 0, empty stderr; evidence:
`D:\Temp\Office-PC\freecad-curve-profile-source-20261001-final`.
This loads repository Python only in an isolated test process; no running-build
staging or native build occurred. Rerun CurveProfileSmoke without the source
overlay after the grouped build, alongside LocalNameSmoke and relevant component
selection/copy/externalization checks. Installed payload and physical owner
acceptance remain pending. No publication.

Pending owner feedback batch: 7.8.7o, component-local labels. Source displays
Origin without the native document suffix and allocates default Sketch001,
Body001, Extrude001 and registered-object names within their owning component.
Native duplicate-label permission is limited to marked component-owned members;
global label preference, unique native names/UUIDs and user labels are preserved.
Run LocalNameSmoke after the next grouped App/script build, together with relevant
copy/externalization checks. New DocumentObject declaration requires dependent
native targets to rebuild. Three regression workflows are prepared; syntax and
whitespace pass. No staging/build/runtime or publication yet; the running owner
copy is unchanged. Earlier saved non-Origin labels are not bulk-renamed.

OWNER FEEDBACK UPDATE READY (2026-10-01): 7.8.7m/n are incorporated into the
existing September 28 development build, at the owner's explicit request.
No FreeCAD process was running before the update. Grouped native GUI/script build
passed; four panel workflows and three external task-context workflows pass,
zero failures/errors/skips, both processes exit 0 and empty stderr. Actual native
OK-button acceptance enters Sketcher without the close-task confirmation and
creates one sketch. Both New Sketch commands show native XY/XZ/YZ planes, accept
plane picks and restore visibility on Cancel. Origin-plane captures reviewed.
Evidence: `D:\Temp\Office-PC\freecad-plus-sketch-feedback-20261001` (`build/`,
`panel-final/`, `task-context/`, `build-identity.json`). Three runtime Python modules
match source; source HEAD `937cf0d8a5` plus local feedback changes and binary hashes
identify this update. About retains an older stamp. Launch with the existing
desktop shortcut; executable path remains the September 28 build below.
Physical owner acceptance and broader qualification remain pending. No installer
or publication. Preserve this copy while the owner tests and batch new feedback.

Built feedback batch includes 7.8.7n: the owner reproduced New Sketch OK
opening a close-task confirmation. TaskView defers removal while its accept
callback runs. Source queues Sketcher entry after that callback returns, checks
the owning-file task is closed and restores context on failure. Panel and
external task-context regressions now use the actual native OK-button path;
the panel test detects/dismisses unexpected modal prompts. Earlier direct accept
tests missed this case. The native button path now passes in the updated build;
physical owner acceptance remains pending.

Built feedback batch: 7.8.7m, New Sketch origin planes. Source now shows the
active component's native XY/XZ/YZ planes and labels through a small binding to
the existing coordinate-system temporary visibility service. Picking a native
plane sets the task orientation. OK/Cancel restore prior origin/datum visibility
and remove the selection observer. Panel and external-context regressions
pass in PanelSmoke and TaskContextSmoke. FreeCADGui and the Python task were updated
together with the matching ViewProvider binding. Syntax, binding generation and
whitespace checks pass; physical viewport picking remains pending.

OWNER FEEDBACK BUILD READY (2026-10-01): the owner explicitly requested a fresh
build. No FreeCAD process was running before the grouped incremental build.
The established development copy now includes the pending 7.8.7k/l changes below.
Build and three AddComponentSmoke workflows passed, zero failures/errors/skips,
process exit 0 and empty stderr. All three changed Python runtime modules match
source. Evidence: `D:\Temp\Office-PC\freecad-plus-owner-build-20261001`, including
`build/`, `smoke/` and `build-identity.json` (source HEAD `937cf0d8a5` plus local
feedback changes and runtime hashes). Native About retains an older version stamp.
Launch with the existing desktop `FreeCAD.exe - Shortcut`, targeting
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Ready for owner testing; broad regressions and physical GUI acceptance remain
pending. No installer, release or publication. Preserve this feedback copy while
the owner tests; batch further source changes until the next agreed update.

Built feedback: roadmap 7.8.7l, Origin first in Model History.
Source prepends the existing native component Origin without changing persisted
feature lists/identities. Empty/root/child/isolated histories retain the row; its eye
controls visibility, selection keeps the occurrence path, and suppression/conversion
actions omit the permanent origin. Full Component permits its normally visible
origin. Origin checks are folded into TestComponentAddCommand's workflows;
older history-row assertions account for the new first row. Built/staged and
covered by the three passing workflows above; owner acceptance remains pending.

Built feedback batch: roadmap 7.8.7k, Add Part/Add Component ownership.
Std_Part still created an unregistered App::Part and changed the native active
binding. Source now routes standard and Assembly New Part through the component
service (Add Component wording). Root/child/external ownership follows the native
active component; the intended parent remains active. File insertion now restores
the original window, root and occurrence binding on success, cancellation or error.
Open tasks/unresolved parents are refused before mutation.
Python syntax and whitespace checks pass. `TestComponentAddCommand.py` passed
all three focused cases via `RunComponentDocument.ps1 -AddComponentSmoke` after
the requested grouped native GUI/Assembly script build. Owner documents were
untouched; no broad qualification or publication was performed.

Last validated batch follows.

Current feedback batch: roadmap 7.8.7j, native component BOM integration.
Native BOMs count component occurrences, excluding owned history/geometry, honor
IncludeInBOM independently of Part View/mass flags and use their owning component
as scope. Component Structure exposes grouped Include/Exclude with one Undo. Model
History creates/edits native reports with owning-file task context and return to the
original occurrence. Whole-instance selections work in the report's exclusion picker;
opening the editor explicitly refreshes counts. Component wording hides legacy-only
scope controls and uses Include nested components.

Evidence: `D:\Temp\Office-PC\freecad-plus-component-bom-20261001`.
Grouped native Assembly/script build passed (`build/`). Initial checks exposed use
of ordinary-group lookup instead of GeoFeatureGroup ownership; the narrow correction
passed `build-scope-fix/`. The same three workflows pass in `feedback/`, zero failures,
errors or skips, process exit 0 and empty stderr. Python selection/refresh/wording
refinements were staged directly. Final BOM editor capture reviewed. Checks include
legacy Part-container counting, grouped Undo/Redo, independent policies, external
task OK/Cancel/history editing and .cadprt reopen. No broad regression run.
Feedback fixture: `feedback/testBOMPolicyReopenAndPerReportExclusions/Assembly.cadprt`.
Mass consumers, automatic cross-file report invalidation, general missing-file/array/
custom-column behavior and per-report exclusions of children stored outside the
BOM's owning file remain open. No schema-version change, installer or release.
Implementation `bc12172def` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records three matching Python modules, five runtime
artifacts, the native BOM source and final build/check/fixture/capture evidence.

Previous feedback batch follows.

Current feedback batch: roadmap 7.8.7i, component display contexts.
Loaded definitions' native LinkViews and isolated snapshots now refresh even when
their assembly window is inactive. Inherited child settings and outer path overrides
remain separate. Full Component includes normally visible view providers and uses
the same unavailable-item rules as Model History. Part View menus indicate effective
choices and reset availability; expanded instances highlight only the active path.

Evidence: `D:\Temp\Office-PC\freecad-plus-display-context-20261001`.
One grouped script/resource build passed (`build/`). The first focused run passed
two workflows but reached its bounded deadline on close/reopen after App objects
outlived their GUI providers. A guard for that transition was staged directly; the same
three workflows pass in `smoke-ready/`, zero failures/errors/skips and process exit 0.
One `QMdiArea::setActiveSubWindow: window is not inside workspace` diagnostic remains.
Two captures reviewed: isolated geometry and exact active occurrence in the tree.
Feedback fixture:
`smoke-ready/testBackgroundAssemblyAndIsolatedInheritance/Assembly.cadprt`.
No schema or native C++ change, installer or release. Engineering shape, source
visibility and participation flags are preserved in the focused fixture. General
construction providers, task-time display and large-assembly performance remain open;
keep broad validation deferred for owner feedback.
Implementation `57ece03afe` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records three matching Python modules, reused native
artifacts and the final build/check/fixture/capture evidence.

Previous feedback batch follows.

Current feedback batch: roadmap 7.8.5f, owning-file Undo/Redo.
Native Undo/Redo execution, enabled states and toolbar history lists follow the
active component's owner, preserving the displayed occurrence context. A multi-step
external history selection stays in that owning file for the whole range. Model
History defers refresh until native restoration finishes and active editing ends.
Embedded components share their containing file's history; ordinary documents retain
their existing ownership behavior.

Evidence: `D:\Temp\Office-PC\freecad-plus-undo-routing-20261001`.
One grouped native/script build passed (`build/`); `smoke/` passes three workflows
on the first runtime pass, zero failures/errors/skips, process exit 0 and empty stderr.
Checks cover external operation/suppression restoration, enabled states/menu ranges,
independent parent history, embedded isolation and ordinary-document fallback.
One final Model History capture reviewed. Feedback fixture:
`smoke/testExternalOperationUndoRedoAndAvailability/Assembly.cadprt`.
No schema, geometry-model, installer or release changes. Native grouped-transaction
checks remain in use; mixed-file prompts, close-during-Undo and broad task-editor
acceptance remain open. Keep broad testing deferred for owner feedback.
Implementation `79972d9bd5` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching Python modules, nine native
artifacts, three changed native sources and the final build/check/fixture/capture evidence.

Previous feedback batch follows.

Current feedback batch: roadmap 7.8.3d, owning-file Save routing.
Native Save, Save As and Save a Copy resolve the active component's owning document
from the native occurrence binding, retaining the assembly/isolated view. Embedded
components save their entire containing file. Backup Save As routing follows the
same owner; component save-dialog titles identify the owning file.

Evidence: `D:\Temp\Office-PC\freecad-plus-save-routing-20261001`.
One grouped native build passed (`build/`). `smoke-ready/` passes three workflows,
zero failures/errors/skips, process exit 0 and empty stderr. Checks cover external Save
leaving an independently dirty parent untouched (with reopen), external Save As/Copy/
Cancel and view context, and isolated embedded first-save ownership. Only the test's
Windows path-separator assumption needed correction; no additional build. One final
panel capture reviewed; file-dialog captions and filters checked at runtime.
Feedback fixture:
`smoke-ready/testExternalSaveCopyCancelAndSaveAsPreserveContext/Assembly.cadprt`.
No schema version, geometry model, installer or release changes. Broader Save All,
close/recovery dialogs, task-time saves and native Undo/Redo ownership routing remain
separate acceptance work; keep broad testing deferred for owner feedback.
Implementation `67a2f3d460` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching Python modules, nine native
artifacts, four changed native sources and final build/check/fixture/capture evidence.

Previous feedback batch follows.

Current feedback batch: roadmap 7.8.7h, component modeling task transitions.
Extrude and New Sketch capture the originating component view/path before entering
the owning document. Extrude OK/Cancel, sketch-plane Cancel and native sketch/history
editor reset restore that context. Instance-picked profiles and planar faces resolve
to definition-local inputs. Isolated-tab Extrude history editing retains the tab and
result identity; preview overlays are removed on completion/cancellation.

Evidence: `D:\Temp\Office-PC\freecad-plus-task-context-20261001`.
One grouped script/resource staging pass succeeded (`build/`); native binaries reused.
`smoke-ready/` passes three focused workflows, zero failures/errors/skips, process
exit 0 and empty stderr. Initial assertions read deleted task labels after success;
only the test fixture needed correction. No additional build. Two final Model History
captures reviewed. Feedback fixture:
`smoke-ready/testExtrudePreselectionPreviewCancelAndAccept/Assembly.cadprt`.
No schema version, native source, installer or release change. Keep broader testing
deferred for owner feedback. Active-definition save routing, general native editors,
close-during-task and multi-tab display acceptance remain open.
Implementation `613cd31707` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching Python modules, nine unchanged
native artifacts, build/check results and reviewed fixture/capture identities.

Previous feedback batch follows.

Current feedback batch: roadmap 7.8.7g, cross-file component editing.
Edit retains the assembly view and binds the selected occurrence, including external
definitions. Model History/native selection, tab switching and Copy/Undo/Redo retain
the correct definition/path. A missing active link falls back to the nearest available
component. Isolated titles update after rename/Save As. Closing GUI documents are
guarded, and instance expansion state is cleared before native document-name reuse.

Evidence: `D:\Temp\Office-PC\freecad-plus-edit-context-20261001`.
One grouped script/resource staging pass succeeded (`build/`), native binaries reused.
The first check was stopped at a close-time modal error. Focused fixes were staged
directly; no extra build. `smoke-final/` passes three checks, zero failures/errors/skips,
process exit 0. Only three expected broken-link messages from the deliberate missing
link appear in stderr; no Python traceback. Two final panel captures reviewed.
Feedback fixture:
`smoke-final/testIsolatedTabsRestoreNestedContextAndOwningFileTitle/Assembly.cadprt`.
Keep broad tests deferred for owner feedback. Native task entry/exit across files,
save routing and general multi-tab display remain open; no schema, native source,
installer or release change.
Implementation `eb206eccf2` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching Python modules, nine unchanged
native artifacts, build/check results and final fixture/capture identities.

Previous feedback batch follows.

Current feedback batch: roadmap 7.8.8d, Save to External File.
The moved embedded hierarchy retains component names and evaluates reference
geometry before saving. Parent references and downstream history refresh after
relinking. Pending edits are rejected before creating a file; already external
components disable this menu action. Active occurrence and parent-view context are
restored with the native occurrence path. Close isolated tabs for the moved component
and embedded children first; live tab migration is not yet supported.

Evidence: `D:\Temp\Office-PC\freecad-plus-externalization-20261001`.
One grouped script/resource staging pass succeeded (`build/`); native binaries reused.
Focused feedback exposed the native activation path and copied-label suffix, corrected
by direct Python staging without another build. `smoke-final/` passes three workflows,
zero failures/errors/skips, process exit 0, empty stderr. Two final captures reviewed.
Checks cover shared hierarchy/reference geometry, Undo/Redo/reopen, preflight and
menu/edit context. Feedback fixture:
`smoke-final/testSharedHierarchyReferencesUndoAndReopen/Parent.cadprt`.
No schema version, native source, installer or release changes. Keep broader testing
deferred for owner feedback; other-file consumers and atomic multi-file crash recovery
remain open. Saving the parent persists its new external links; Undo leaves the newly
created external file on disk.
Implementation `3a325840f6` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching Python modules, nine unchanged
native artifacts, the build and the final checks/captures/fixtures.

Previous feedback batch follows.

Current feedback batch: roadmap 7.8.3c, moved/missing component recovery.
Component Structure groups missing instances by saved definition identity, keeps
numbered expansion available and disables geometry-dependent actions. Add Instance
refuses an unresolved source instead of creating a new definition. Locate Component
File restores matching unresolved instances in the same file together, preserving
placements and references in one Undo. Missing source geometry stays repairable;
healthy references and modeling can continue. Failed locate restores parent context.

Evidence: `D:\Temp\Office-PC\freecad-plus-file-recovery-20261001`.
Initial grouped script staging and three focused recovery workflows passed. Log review
found an MDI close callback race and native PropertyXLink None-to-None clearing that
retained an unresolved filename. Python cleanup attempts were discarded because they
did not preserve property/Undo semantics. The native setter now distinguishes an
empty link from an unresolved saved target; the property itself remains intact.
`build-native/` completes the additional grouped native build, exit 0.
`smoke-native/` passes the same three workflows, zero failures/errors/skips and
process exit 0. The saved XML no longer contains the obsolete source filename after
partial recovery and Undo/Redo. Two final captures were reviewed. Stderr contains
the expected missing-file/broken-link diagnostics from deliberate fixture failures,
with no Python traceback; all three missing-file reports precede repair.
Feedback file: `smoke-native/testGroupedLocateUndoAndReopen/Recovery-Parent.cadprt`.
The sibling partial-recovery fixture preserves a missing body for further repair.

Keep checks limited to the three feedback workflows: grouped locate/Undo/Redo/reopen,
partial geometry recovery/independent modeling/saved-link inspection, and wrong-file
identity refusal with parent-context preservation. Deliberately missing files produce
native missing-file and broken-link diagnostics before recovery; retain those logs.
No schema version, installer or release change. General multi-owning-file recovery,
automatic dependency searches, crash/backup/schema matrix, native suppression,
multi-output lineage and solver/BOM/mass integration remain open.
Implementation `c539d4ea4b` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching Python modules, nine native
artifacts, native source, both builds and reviewed recovery evidence.

Previous feedback batch:
Current feedback batch: roadmap 7.8.6c, reviewed geometry conversion.
Convert to Dumb Object now shows the existing dropdown with a read-only review of
removed versus retained shared history. Delete Parameters follows geometry inputs,
never component ownership, preserves the result identity/downstream links, and
clears obsolete reference metadata when freezing a reference. Model History explains
independent geometry. Extract Dumb Body defaults for already independent objects;
curves/dumb sketches use extraction, with body/sheet-only parameter deletion.

Evidence: `D:\Temp\Office-PC\freecad-plus-conversion-20261001`.
One grouped script/resource build passed. `smoke-accepted/` passes three focused
workflows, zero failures/errors/skips, process exit 0. The conversion review capture
was reviewed. Checks cover exclusive upstream pruning without losing a child,
downstream native Mirror identity/geometry, Undo/Redo/reopen, shared sketch retention,
review Cancel/extraction and independent dumb-sketch geometry. The initial three
checks passed; the same workflows were repeated only to assert current downstream
geometry after Undo/reference refresh. No additional build was needed.
Two native `DownstreamMirror: Cannot mirror empty shape` messages remain during
reference restoration; current geometry after activation and final geometry pass.
Native reference/recompute scheduling remains a separate open integration issue.

Feedback files in `smoke-accepted/`: `Component-Converted-Body.cadprt`,
`Component-Shared-History.cadprt`, `Component-Dumb-Sketch.cadprt`.
No schema change, broad suite, installer or release update. Continue component
migration. Real multi-body edge-treatment contribution detachment, general topology/
expression preservation, native suppression scheduling and solver/BOM/mass remain
open; this review and the shared-sketch check do not complete those gates.
Implementation `bc5ddabe9d` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching modules, six unchanged native
artifacts, fixture hashes, reviewed capture and native diagnostics.

Previous feedback batch:
Current feedback batch: roadmap 7.8.8c, instance copy/reference continuity.
Copy to New Part keeps parent references on the selected occurrence, remaps their
source identities and nested display overrides, retains placement and shared child
definitions, and checks ambiguous face/edge/expression consumers before mutation.
Model History follows the active occurrence after Copy/Undo/Redo and refreshes its
references. Readiness/suppression checks follow geometry dependencies instead of
all unrelated history reached through component ownership links.

Evidence: `D:\Temp\Office-PC\freecad-plus-instances-20261001`.
One grouped script/resource staging build passed. `smoke-ready/` passes three
focused workflows, zero failures/errors/skips, process exit 0 and empty stderr;
the final Component Structure capture was reviewed. Checks include parent native
Mirror/result updates, copy Undo/Redo, child sharing, nested display overrides,
.cadprt reopen, external-to-embedded copy and ambiguous face-reference refusal.
Initial checks exposed unset native LinkSub handling and ownership traversal that
blocked a valid parent result; both were corrected in Python without another build.
Fixture transaction/API corrections are recorded in the evidence directories.

Feedback fixtures in `smoke-ready/`: `Component-Independent-References.cadprt`,
`Component-Independent-Assembly.cadprt`, `Component-Embedded-Copy.cadprt`.
No schema change, broad validation or installer/release update. Continue component
migration: native suppression scheduling, multi-output lineage, solver/BOM/mass,
deep copies and general expression/topology/external-file remapping remain open.
Other open files' nested overrides are refused before copy because they require
multi-document transaction handling. Unloaded ancestor files remain a broader gate.
Implementation `b2d1dd6425` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching modules, six unchanged native
artifacts, fixture hashes and the reviewed capture.

Previous feedback batch:
Current feedback batch: roadmap 7.8.5e, Model History branch restoration.
Suppression now derives dependent inactivity separately from explicit flags, restores
eligible earlier results and releases shared inputs only after their last active
consumer stops. Manual visibility remains independent. Selected history items can
be suppressed/unsuppressed in one Undo; dependency tooltips name suppressed inputs.

Evidence: `D:\Temp\Office-PC\freecad-plus-history-20261001`.
One grouped script/resource build passed; unchanged native C++ was not rebuilt.
`smoke-final/` passes three focused workflows with no test failures/errors/skips,
process exit 0. A readable Model History capture was reviewed. Early fixture creation
needed native command transactions to capture visibility; later Python refinements
were restaged without further builds. Eight native `SecondCut: Base shape is null`
messages remain when suppression empties its input. Published results stay empty,
Model History shows dependency inactivity, and unsuppression recovers the geometry.
Native recompute scheduling is still open; this is not full suppression qualification.

Feedback fixtures: `smoke-final/Component-History-Suppressed.cadprt` and
`smoke-final/Component-History-Restored.cadprt`. Continue the component migration,
including native recompute integration, multi-output lineage, assembly solver and
BOM/mass consumers. Preserve the owner's limited feedback-first validation boundary.
No schema lock-in, broad suite, installer or release update.
Implementation `19285590d8` was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching modules, six unchanged native
artifacts, both fixtures and the known native stderr diagnostics.

Previous feedback batch:
Current feedback batch: roadmap 7.8.4a, component reference recovery. Missing
reference geometry no longer closes a structurally valid .cadprt or blocks independent
reference refresh/local sketch and Extrude work. Model History Edit and Repair /
Change Reference Source preserve reference identity, history position, valid whole-
object consumers and authored suppression. Refresh References, repair notice and
error tooltip expose the state. Kind/face/edge/expression remapping guards remain.

Evidence: `D:\Temp\Office-PC\freecad-plus-reference-recovery-20261001`.
One grouped script/resource build passed. `smoke-accepted/` passes three focused
checks, process exit 0, empty stderr; two captures reviewed. The initial checks
passed; capture review corrected the missing-source eye icon and a fixture scope
warning. Only Python was restaged, with no extra build. Feedback fixtures in that
folder: `Component-Broken-Reference.cadprt`, `Component-Repaired-Reference.cadprt`.
Implementation 6b12567f01 was pushed to origin/main and verified remotely.
`acceptance-identities.json` records seven matching modules, six unchanged native
artifacts and fixture hashes. No schema lock-in, broad validation or installer update.

Continue component migration rather than unrelated feature rotation. Whole-object
recovery does not establish arbitrary topology/expression remapping, all missing-file
recovery, native editor parity, solver/BOM/mass or engineering-consumer acceptance.
Preserve the owner's request for batched implementation and limited feedback checks.

Previous feedback batch:
Current feedback batch: roadmap 7.8.7f. Native occurrence-path selection is now
synchronized with Component Structure / active Model History; precise nested picks
reveal the instance without changing the edited definition. Add Reference Object
preselects a direct-child object only when the incoming native path is unambiguous,
with explicit whole-object review. Grouped Part View and show/reset changes use one
Undo. Reopening an isolated component focuses its existing tab; switching tabs
restores the component and occurrence being edited.

Evidence: `D:\Temp\Office-PC\freecad-plus-component-selection-20261001`.
`build-corrected/` stages the Python batch successfully; native C++ was unchanged.
Initial staging reached a missing Show target (BUILD_SHOW disabled); the helper now
handles that configuration with existing Python support staging. `smoke-accepted/`
passes three focused checks, exit 0 and empty stderr; two captures reviewed. Native
addSelection may canonicalize a bare object to an occurrence; the mapper's ambiguous
bare-input guard is checked separately, and the dialog reviews the received path.
Use `Component-Selection-Feedback.cadprt` from that folder in the local fork build.
Implementation 1ffb7a9df2 was pushed to origin/main and verified remotely.
`acceptance-identities.json` records module/fixture identities and confirms all six
native artifacts are unchanged. No installer/release update or broad qualification.

Continue component migration integration rather than unrelated feature rotation.
Full mouse/native-editor parity, external-view matrix, expression/multi-result lineage,
solver, BOM/mass and broader recovery/consumer gates remain open. Keep the owner's
feedback-first validation boundary; do not run the full suites simply to close this batch.

Previous feedback batch:
Current feedback batch: 7.8.5d/7.8.7e. Standalone sketch routing and Extrude
mode/target editing are implemented, together with the owner's latest panel
revision: grouped/numbered instances, active highlight/visibility protection,
Edit/Instances/Part View menus, no filename/path or creation buttons, and history
checkbox/visibility controls. The native tree and panel share document objects;
complete native command/picking parity remains a gate, not a completed claim.

Evidence: `D:\Temp\Office-PC\freecad-plus-component-panels-20261001`.
The initial `build/` process was interrupted without completion or surviving
processes. The same grouped batch completed in `build-resumed/`, exit 0.
`smoke-accepted/` passes three focused workflow checks, process exit 0, empty stderr;
four rendered captures reviewed. Corrections stayed in Python. The existing Show
Python package needed by native Sketcher was staged and added to the build helper.
No broad suite was run; retain the owner's feedback-first validation boundary.
Use `Component-Panel-Feedback.cadprt` and `Component-Edit-Feedback.cadprt` from that
folder in the local fork build. The owner/test procedure describes `-PanelSmoke`.

Implementation 5ecd62c941 was pushed to origin/main and verified remotely.
`acceptance-identities.json` records source/runtime/fixture hashes. No installer or
release update. Continue the component migration after feedback: native command/picking parity, expression and multi-result
lineage, solver, BOM/mass consumers and broader format/recovery qualification remain
open. Do not infer completion of the whole architecture from this feedback batch.

Previous feedback batch:
Current feedback batch: roadmap 7.8.5c/7.8.7d. Component-context Extrude/Pad/Pocket
now use a Body-independent native extrusion/Boolean task with explicit New Body,
Add or Subtract, profile/target, length/direction and view-only preview. Model History
opens its producer for editing, distinguishes suppression/dependent inactivity and
retains selection/expansion on refresh. Embedded Add Component is a single Undo.

One grouped native Release build passed. Three small workflow checks pass under
`D:\Temp\Office-PC\freecad-plus-component-iteration-20261001\smoke-accepted`;
two GUI captures reviewed. Corrections stayed in Python; no second native build.
Final ready/preview wording was source-reviewed/staged after those checks. The owner
explicitly wants feedback and iteration before extensive file-format validation.
Do not run a full component/cross-workbench qualification pass merely to close this
batch. Open `Component-Feedback.cadprt` from that folder in the fork build to review.
Full Part Design sketch routing, mode/target edit changes, expressions, multi-solid
lineage and the broader gates below remain pending. No installer or release update.
Implementation 7630012c25 was pushed to origin/main and verified remotely.

Previous foundation batch:
Latest owner priority: component document migration, roadmap 7.8 (2026-10-01).
[Approved contract](architecture/COMPONENT_DOCUMENT_CONTRACT.md),
[architecture decision](architecture/ADR_003_COMPONENT_DOCUMENT.md), and
[owner/test procedure](../tests/ComponentDocument.md) route the work.

The native `.cadprt` envelope, embedded/external definitions, evaluated results and
references, Component Structure/Model History, standard File command integration,
independent copies and assembly externalization are implemented. The top row is the
root component with the native Part icon. Native serialization, object identities,
geometry, transactions and links are retained. FCStd converts supported root content
on GUI opening, preserving the source and reporting unmapped native payloads.

Evidence root: `D:\Temp\Office-PC\freecad-plus-components-20261001`.
`model-21`: 27 passing checks including Draft/CAM/TechDraw consumers and reviewed
navigator/isolated-view captures. `cold-05`: five passing fresh-process installed
module and native File command checks including the format/name-collision guard.
Builds 01-05 passed; final native runtime hashes and source/module identities are
in acceptance-identities.json. Implementation d1a7a73be1 was pushed to origin/main
and verified remotely; roadmap 7.8 records the full publication identity. No installer or release update.

Continue 7.8's outstanding integration tasks: native multi-result task migration,
lineage, assembly solver, BOM/mass consumers, deep copies/expression remapping,
broader recovery, selection and consumer acceptance. FEM remains disabled in this
local build. This explicit owner priority supersedes the older rotation advice below.
Do not describe the entire component migration as complete on the basis of the
persistence and result-layer pilot. Source/build/runtime/publication stay separate.

Previous batch: F096 CAM setup reuse, phase 14 tasks 14.4a/b. Existing Export Template
and New Job now add named revision metadata, compatibility preflight and a visible
settings review. Exact accepted settings feed the existing native creation services;
known incompatible inputs fail before resource creation, and native GUI transaction
rollback handles later instantiation failure. Post selection uses enum choices,
not substring matching against the selected value. Model-bound stock adapts to the
new model; tool and setup objects remain independent and editable.

14.4a/b evidence (2026-10-01):
Both tasks preceded one grouped PathScripts build/staging pass, exit 0. Compatible
Python changes use the existing native fork; no native C++ rebuild was needed.
Evidence: `D:\Temp\Office-PC\freecad-plus-setup-templates-20261001`.
`grouped/` passes eight new template checks plus eight existing setup-sheet checks.
After clearer stock-margin/default labels and restoration of an existing UTF-8 log
message, only affected Python files were restaged; `template-verified/` passes all
eight template checks. **16 distinct selected passes**, zero failures/errors/skips,
native process exits 0. Six final `visual-accepted/` captures reviewed: export
metadata, settings/tools, unavailable post, changed-file review and reopened reuse.
`job_metric_fixture.json` and `Reused-Setup.FCStd` are owner fixtures in that folder.
A 12 mm model with X margins 2/3 mm produces 17 mm stock; applying the same template
to a 30 mm model produces 35 mm stock with independent tools/setup and no operations.
Native exact post selection, 600 mm/min feed, metadata, portable setup-sheet
expression rebinding, known-incompatible-input refusal, GUI rollback, Undo/Redo,
save/reopen and later source growth pass. Template edits do not alter created jobs.
The fixture uses an available legacy post and no configured machine; no posted output
or physical machine motion is validated. Full machine compatibility remains open.
validated-identities.json and acceptance-summary.json identify exact source/staged
modules and unchanged native runtime; historical About metadata is not source identity.
No installer/release update. Full F096 remains open for operation sequences and
collector remapping, complete machine/tool asset compatibility, broader reference
repair, localization/high-DPI and owner acceptance. Stop here and rotate.
[Owner procedure](../tests/SetupTemplates.md).

Previous batch: F067 sheet thickening, phase 13 tasks 13.1c/d. Existing native 3D
Offset now exposes signed one-sided thickness, formula-preserving numeric reversal,
solid/sheet status and recoverable failed acceptance. Kernel inputs are deep copies
with native element maps. Cancel aborts before resetEdit's implicit commit; direct
setEdit also gets an edit transaction. The shared solid-shell Thickness form keeps
its face-selection controls and the 2D geometry implementation is unchanged.

13.1c/d evidence (2026-10-01):
Both tasks preceded the first grouped PartGui/PartScripts Release build. Four build
attempts were needed for demonstrated defects: the initial compile exposed the
shared solid-shell Thickness form and a shape API type; later native tests exposed
kernel mutation of shared source data, feature-recompute status and resetEdit's
implicit commit before Cancel. Final build exit 0; earlier logs/results retained.
Evidence: `D:\Temp\Office-PC\freecad-plus-sheet-thickening-20261001`.
`grouped-corrected/` passes eight existing sewing checks; after the final Cancel
ordering fix, `thicken-verified/` passes all nine sheet-thickening checks.
**17 distinct selected passes**, zero failures/errors/skips in accepted suites;
native process exits 0. Initial failed aggregates are not acceptance evidence.
Six `visual/` captures reviewed: offset sheet, planar positive/opposite thickness,
curved inward thickness, excessive-thickness refusal and reopened results.
Sheet-Thickening-Sources.FCStd / Sheet-Thickening-Results.FCStd are owner fixtures.
Planar 10 x 8 x 2 mm results measure 160 mm^3 on either side; radius-5/height-10
cylindrical sheet offsets +1/-1 mm produce 110*pi/90*pi mm^3. Inward -6 mm is
refused. Deep native shape copies preserve source BRep data and element maps.
Failed OK remains editable, Cancel restores/removes the native feature correctly,
and Undo/Redo, formula preservation, deferred preview, 2D and solid-shell Thickness
controls pass. Reopened source growth updates the thickened solid and downstream cut.
Part SHA256: `53C9A44F356F8CD8912ED297813A5DA17BEC9636919F14FDB955B73192AD9C72`.
PartGui SHA256: `008DAA38E031E59809DA177CD2A7A66D8063ABD9DD760665158ED434266F8255`.
validated-identities.json and acceptance-summary.json identify exact source/runtime;
the historical About stamp is not this source identity. No installer/release update.
Full F067/13.1 stays open for symmetric/two-sided thickness, graphical normals,
Boolean target collection, compound-sheet filling, broader high-curvature diagnostics,
localization and physical owner acceptance. Stop here for owner testing and rotate.
[Owner procedure](../tests/SheetThickening.md).

Previous batch: F048 sketch constraint repair, phase 11 tasks 11.4a/b. The Sketch
command diagnoses a hidden temporary native copy, previews explicit deactivation
choices and applies a successful proposal transactionally. Native solver, copying,
constraint signatures, identity and wireframe services are reused. Source sketches
may be invalid; authored geometry/constraints are diagnosed instead of cached Shape.

Both implementation tasks preceded one SketcherGui/SketcherScripts Release build,
exit 0. Evidence: `D:\Temp\Office-PC\freecad-plus-constraint-repair-20261001`.
`grouped/` passes eight repair checks and seven existing sketch-reuse checks. A final
UI correction frames the temporary overlay automatically because native Fit All
excludes it; only ConstraintRepairGui.py was restaged, without a second native build.
`repair-verified/` passes all eight repair checks, including a 10,000 mm off-origin
preview. **15 distinct selected passes**, zero failures/errors/skips in accepted
suites, native exits 0. Six final `visual-accepted/` captures were reviewed: redundant
and conflicting diagnoses, failed choice, successful proposal, preview wireframe
and reopened inactive constraint. Earlier `visual/` used harness framing and is
retained separately. Constraint-Repair-Source.FCStd / Constraint-Repair-Result.FCStd
are owner fixtures; the unselected redundant profile intentionally remains unrepaired.
Native diagnostics distinguish equal-radius redundancy from unequal-radius conflict.
Preview preserves source content, constraints, object count, Undo and active document.
Choice/Cancel, retained dimension identity/values, transaction/stale guards, rollback,
Undo/Redo and save/reopen pass. A repaired radius-5 profile extrudes 4 mm to 100*pi
mm^3; changing the surviving radius to 6 after reopen updates it to 144*pi mm^3.
Sketcher SHA256: `0525D3CA7E6DB90B2830C504F9BC99DB1A092D6D72268E5A18D70C15F2EED0D6`.
SketcherGui SHA256: `1B375C675DBABA3373565643D0D493CA9E8EA58CE9A4E3FC09A09DF17D11E5D4`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted evidence; the historical About stamp is not this source identity.
No installer/release update. Full F048/11.4 remains open for Body/attached/external
and expression-driven sketches, constraint replacement, consumer-wide previews,
movement-direction diagnosis, macro recording, localization and physical acceptance.
Stop here for owner workflow testing and rotate to another item family.
tests/ConstraintRepair.md is the owner procedure.

Previous batch: F037 Select Other, phase 10 tasks 10.5c/d. Existing native Clarify
Selection now deduplicates by document/root/full subpath and displays occurrence
context. Full whole-object paths survive repeated instances; command gates filter
candidate roles and are rechecked at hover/accept. Empty filtered lists explain the
cause; deleted/recreated roots cannot redirect selection. No new picker/service.

Both implementation tasks preceded one FreeCADGui/FreeCADGui_Resources Release
build, exit 0. Evidence: `D:\Temp\Office-PC\freecad-plus-clarify-selection-20261001`.
Initial `grouped/` stopped before any tests because the PySide compatibility wrapper
has no QtTest export. The test now imports the bundled PySide6 QtTest (PySide2 fallback);
no implementation change or second build was needed. `grouped-native/` passes all
seven native Clarify Selection checks and nine temporary-display regressions:
**16 selected passes**, zero failures/errors/skips, native exit 0. Five `visual/`
captures were reviewed: equal-label face choices, rear-face highlight, face-only
filter, all-filtered explanation and distinct repeated occurrence paths.
Overlapping-Equal-Labels.FCStd and Overlapping-Occurrences.FCStd are owner fixtures.
The native picker exposes Front/Rear Face5/Face6 separately and Assembly.First. /
Assembly.Second. as separate whole occurrences. Exact hover/accept, additive
selection, Escape preservation, face/object/reject gates, changed-gate refusal,
deleted/recreated-name protection and native Link save/reopen pass.
FreeCADGui SHA256: `19FE903A46ABEFC2A34F0AECBA86F2BAA6C331A2663685C0DD797032A1EF80C8`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted evidence; the historical About stamp is not this source identity.
No installer/release update. Full F037 remains open for broader topology/live-menu
changes and physical/high-DPI/navigation-preset acceptance. Global filter controls
(F035), new selection scopes (F036) and depth ranking are separate work.
Stop at this functional checkpoint for owner testing and rotate to another family.
tests/ClarifySelection.md is the owner procedure.

Previous batch: F071 sampled face deviation, phase 15 tasks 15.2a/b. The Part command
uses explicit sampled/reference face roles, native unsigned point-to-face distances,
UV cell-center sampling and a non-pickable on-top color map. Millimeter scale,
sample statistics and excluded/failed counts are visible. Settings persist only by
explicit request; references/results are temporary. No geometry or appearance edits.

Both tasks preceded one PartGui/PartScripts Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-surface-deviation-20261001`.
`grouped/` passes nine new deviation checks and seven existing interference checks:
**16 selected passes**, zero failures/errors/skips, native exit 0. Six `visual/`
captures were reviewed: known offset, tilted report/map, changed-face refusal,
reopened report and trimmed-hole report. Known-Offset.FCStd and Tilted-Surfaces.FCStd
are the owner fixtures. Planar and cylindrical fixtures report 2 mm; the tilted
11 x 11 grid reports 0.155463702-3.264737732 mm. The trimmed fixture excludes 25
of 121 UV centers and reports 96 usable samples. Native whole Body results,
world placement, one-way finite-face differences, incomplete native sampling,
source/Undo isolation, saved settings, transaction/stale/context guards, map cleanup,
command activation and save/reopen pass.
Part SHA256: `93D8BCB643EEB020AB1466333DEA84F14BA934C0EF00C2043566111E5AFC8C66`.
PartGui SHA256: `5025C3E75A2D150FEC54B939C6C5DD49510517FF2BCD8AB6C8255F4049BC995A`.
validated-identities.json and acceptance-summary.json identify source/runtime and
accepted evidence; the historical About stamp is not this source identity.
Original tracked newline conventions were restored after build without changing
compiled semantics; InitGui.py was restaged before native command capture.
No installer/release update. Whole F071/15.2 remains open for zebra/reflection lines,
curvature combs, continuity, broader subjects, adaptive/bidirectional or certified
global deviation, reference/report persistence and physical/high-DPI acceptance.
Stop at this functional checkpoint for owner feedback and rotate to another family.
tests/SurfaceDeviation.md is the owner procedure.

Previous batch: F022 occurrence replacement, phase 12 tasks 12.6a/b. Standard Tools
command reuses one same-document root solid/Body for a free native Link, preserving
identity, placement/source-placement setting, visibility and uniform appearance
policy. Existing identity/selection, movement and appearance services are reused;
preview is view-only. Consumers/relationships and unsupported scopes are refused.

Both tasks preceded one FreeCADGui/FreeCADGui_Resources Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-occurrence-replace-20261001`.
Initial `grouped/` passed seven movement and seven appearance checks, plus four of
eight replacement checks. Qt findData did not match stored Python identity tuples;
replaced it with explicit key comparison. A test quantity increment also needed its
native length value. Only OccurrenceReplace.py was restaged; no second native build.
`replacement-verified/` passes all eight. **22 distinct selected passes** across
accepted suites, zero failures/errors/skips in accepted suites, native exits 0.
Initial failed aggregate remains recorded. Five reviewed `visual/` captures and
Occurrence-Replacement-Source.FCStd / Occurrence-Replacement-Result.FCStd provide
the owner fixture. Native assembly-path geometry agrees with preview for both
source-placement settings; whole Body sources, preserved appearance/placement,
other-occurrence isolation, Cancel/stale cleanup, unsupported consumers, rollback,
Undo/Redo and save/reopen pass. Later replacement edits update only its instances.
FreeCADGui SHA256: `8F48A425D59BFE4A5182B2F3CEDB920932AAFDB1104A5658B9CE2F63A529AE8A`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted checks; historical About metadata is not this source identity.
No installer/release update. Whole F022/12.6 remains open for mate/interface remapping,
multiple targets, realignment, external/mixed sources, arrays, broader appearance,
macro recording and physical acceptance. Stop at this checkpoint and rotate.

Item-level correction: previous Make Unique status had been attached to F008;
it now belongs to F019. F008 promotion acceptance remains open. The owning 12.2d/e
evidence is unchanged. tests/OccurrenceReplace.md is the new owner procedure.

Previous batch: F068 sewing, phase 13 tasks 13.1a/b. sewShape(tolerance) now passes
the requested tolerance and rejects non-finite/non-positive values. Existing Shape
Builder shell/solid modes add tolerance and Check shape diagnostics, independent
snapshot creation, and open-shell/invalid-solid refusal. Source geometry/visibility
stays intact; read-only source names/tolerance record snapshot provenance.

Both tasks preceded one PartGui/PartScripts Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-shape-sewing-20261001`.
Initial `grouped/` passed all 14 Trim Body checks and 6/8 sewing checks. Two test
expectations were corrected for native Part origin objects and the face-only
selection gate; no implementation rebuild. `sewing-verified/` passes all eight.
**22 distinct selected passes** across accepted suites, zero failures/errors/skips
in accepted suites, native process exits 0. Initial failed aggregate is retained.
Six reviewed `visual-settled/` captures and Sewing-Sources.FCStd / Sewing-Results.FCStd;
initial `visual/` captures caught native layout/radio animations before settling.
The 0.01 mm gapped enclosure stays disconnected at 1e-6 mm sewing tolerance;
explicit 0.05 mm joins it and reports 0.0105 mm maximum geometry tolerance. The
exact enclosure produces a valid 1000 mm^3 solid; the open shell is refused.
Part SHA256: `5DF2B65D6A4F06972AA7596371B7D777779D0AB11F86D29FA68A2C842725C128`.
PartGui SHA256: `7ACC4FBFDE731DA33A76528FC0373D16E563F2D7C01164AD8F5C6CEA0409CBE6`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted checks; historical About metadata is not this source identity.
No installer/release update. Root same-document inputs, 500 faces maximum.
Whole F068/13.1 stays open for associative links, graphical boundaries/preview,
gap-width measurement, broader nonmanifold/healing diagnostics, standalone macro
replay, localization and physical acceptance. Stop here for owner testing and rotate.

C++/UI line endings were restored to their original CRLF convention after build;
compiled semantics unchanged. tests/ShapeSewing.md is the owner procedure.

Previous batch: F123 offline command help and keyboard/display recovery, phase 10
10.9a/b. Existing command search now has thirteen local workflow guides, native
live availability, a scrollable plain-text pane, F1/Ctrl+L navigation, accessible
names and window-only Reset layout. Reading/reset leaves the model, selection,
Undo history and global fonts/shortcuts intact. Whole F123/10.9 remains open.

Both tasks preceded one successful FreeCADGui_Resources build/staging pass;
no C++ recompilation was needed. Initial grouped/ passed seven TestDocumentUpdates
and ten of eleven TestCommandSearch checks; F1 failed. Corrected palette-local
key handling and restaged only CommandSearch.py. help-verified/ passes all eleven.
Visual review exposed application styling overriding inherited test fonts; final
stress checks verify actual rendered 20-point text. enlarged-verified/ passes all
eleven; 18 distinct selected passes across accepted suites, no failures/errors/
skips, native process exits 0. Initial failed aggregate remains preserved.

Evidence: D:\Temp\Office-PC\freecad-plus-command-help-20261001.
Six reviewed visual-accepted/ captures and Command-Help-Example.FCStd; initial
visual/ font-stress captures retained. FreeCADGui SHA256:
72AD07F792C746280276D8388CB0845EB57BA293BBD17140E093CE98CF591655.
validated-identities.json records source/runtime hashes and native payload identity;
acceptance-summary.json links accepted suites. Historical About stamp is not this
Python source identity. tests/CommandSearch.md is the updated owner procedure.

Full shared workspace transitions, command-specific explanations, broader keyboard
modeling/downstream workflows, localization and physical screen-reader/high-DPI
acceptance remain open. No installer/release update. Stop here for owner testing
and rotate to another item family.

Previous batch: F104 assembly BOM scope/inclusion, phase 15 tasks 15.4a/b.
Existing native BOM quantities now group siblings only, keeping a later direct
component out of an earlier nested child row. Native scope also follows BOM-group
ownership; mirror classification uses checked link casts. The existing editor adds
per-BOM exclusions with explicit tree selection and include-again controls. Hidden
components remain counted unless excluded. Source objects and visibility stay intact.

The first target invocation failed because BUILD_ASSEMBLY was OFF in this local
validation build. Enabled BUILD_ASSEMBLY=ON in D:\Temp\Office-PC\freecad-plus-validation-20260928\build.
Existing OndselSolver sources were used unchanged. One actual AssemblyGui/
AssemblyTests Release build then succeeded, exit 0. No separately installed FreeCAD
was changed. The local validation payload now has Assembly enabled; older disabled-
workbench records describe their historical configuration, not the current one.

Initial grouped/ passed 13 AssemblyTests.TestCore and 6 of 7 new BOM tests; the
remaining assertion assumed fixed InList order. Corrected that test and aligned
the Python picker with actual assembly occurrences/native document tree roots.
Only CommandCreateBom.py was restaged; no second native build. All 8 new BOM tests
pass in bom-verified/. 21 distinct selected passes across accepted runs, no failures/
errors/skips in accepted suites; process exits 0. Initial aggregate remains failed.

Evidence: D:\Temp\Office-PC\freecad-plus-bom-scope-20261001.
AssemblyApp SHA256: 03682741c90cc84388080773890606b774174e4178605e432f149441f2004010.
AssemblyGui SHA256: dd7fe8cbce8d06a129708417342304187ee21a73cbe98c821e7955cb85287656.
Five reviewed visual/ captures; Assembly-BOM-Source.FCStd and Assembly-BOM-Excluded.FCStd.
Module quantity 2 / nested bolt 1 / direct bolt 3 stays distinct; excluding two direct
occurrences changes that row to 1. Scope, mirrored/unique items, hidden inclusion,
per-BOM independence, nested-child policy, Cancel, creation cleanup, Undo/Redo,
reopen and native CSV pass. acceptance-summary.json and validated-identities.json
record exact source/runtime/native identities and accepted suites. Historical About
metadata is not this source identity. tests/AssemblyBomScope.md is the owner guide.

Whole F104/15.4 stay open for arrays/suppression/configurations, external/unloaded
inputs, individual paths through reused definitions, custom-column identity,
persistent balloons, exploded documentation and physical acceptance. Item numbers
regenerate. No installer/release update. Stop at this checkpoint and rotate.

Previous batch: F053 sketch reuse, phase 11 tasks 11.6c/d.
Sketch > Copy reusable sketch preserves the complete native geometry/constraint
set, named dimensions and construction roles in an independent editable sketch.
Typed source-axis offsets and rotation about the source normal set the copy's
Placement. A view-only non-pickable preview frames both source and proposed copy;
confirmation makes one Undoable native copy. Source/consumers remain unchanged.

Both tasks preceded one SketcherGui/SketcherScripts Release build, exit 0.
Initial grouped/ has 35 passes, one inherited intentional skip, no failures/errors:
7 TestSketchReuse, 23 of 24 SketcherTests.TestSketcherSolver, 5 TestSketchSupportCommand.
The existing secant driving-distance test is skipped with its PR 9044 discussion
note. The strict no-skips harness records aggregate false; process exit 0. Do not
claim 36 passes or hide the skip. Visual inspection found native Fit All excluded
the view-only copy overlay; Preview now frames the complete scene. Only
SketchReuseGui.py was restaged; no second build. All 7 affected checks pass in
reuse-verified/, no failures/errors/skips; the 28 unchanged regression passes stand.

Evidence: D:\Temp\Office-PC\freecad-plus-sketch-reuse-20261001.
SketcherGui SHA256: 9b75530fb26a5c39b179aee9443e15f18122c298e040e9cbad8f85b66391bf2b.
Five final captures in visual-accepted/ with Reusable-Slot.FCStd, Copied-Slot.FCStd
and Edited-Copy-Solid.FCStd. visual/ retains the off-screen preview;
visual-frame-probe/ demonstrates the camera diagnosis. The slot has 5 geometry
items (including construction), 11 constraints and 0 DoF. Copy radius changes from
3 to 4 mm independently; its reopened 5 mm extrusion updates from 741.371669 to
1051.327412 mm3. Preview/commit, placement, rollback, Undo/Redo and lifecycle pass.
acceptance-summary.json / validated-identities.json record exact results, inherited
skip and source/runtime/native identities. Historical About metadata is not this
batch's source identity. tests/SketchReuse.md is the owner guide.

Whole F053/11.6 stay open: only free root sketches up to 500 geometry items; no
support/external geometry/expressions/other links. Partial paste/remapping,
reference choices, nested scopes, blocks/libraries/patterns and physical acceptance
remain pending. No installer/release update. Stop at this checkpoint and rotate.

Previous batch: F091 mesh preparation, phase 14 tasks 14.1a/b.
CAM > Review CAM mesh inspects one root imported mesh: mm dimensions/bounds,
boundary/nonmanifold edges, components, inconsistent normals, degenerate/duplicate
triangles, density and signed orientation. An explicit independent reversed-normal
copy preserves placement, coordinates, source visibility and existing CAM model
links. Native transactions provide atomic creation and Undo/Redo; active tasks,
booked/pending owner edits, inactive document and stale input reject.

Both tasks preceded one Release PathScripts/Tests build/staging pass, exit 0.
No C++ change/rebuild was needed. Initial grouped/ passed all 24 existing
CAMTests.TestMeshMachining checks but the new suite had two malformed native vector
fixtures and an empty booked-transaction guard failure. Fixtures corrected; added
incomplete-topology feedback and protected booked transactions. Only the two Python
modules were restaged; no second build. All 8 TestMeshPreparation checks pass in
preparation-verified/, including a real 100,352-triangle input, defects, placed copy,
model-link isolation, rollback, Undo/Redo, save/reopen and GUI lifecycle.
32 distinct selected passes across accepted runs, without failures/errors/skips in
accepted suites; process exits 0. The initial aggregate remains recorded as failed.

Evidence: D:\Temp\Office-PC\freecad-plus-mesh-preparation-20261001.
Five reviewed visual/ captures and Mesh-Preparation.FCStd cover inward/open/outward
reports, copy success and invalidated review. acceptance-summary.json and
validated-identities.json record accepted suites and matching source/runtime hashes,
plus the unchanged native CAM/Mesh artifacts. The historical About stamp is not
this batch's source identity. tests/MeshPreparation.md is the owner procedure.

Whole F091 and parent 14.1 remain open for self-intersection checks, defect-region
highlighting, per-piece repair, hole filling/welding/decimation, units conversion,
setup wizard and physical owner acceptance. Current scope is a root Mesh::Feature
up to 200,000 triangles. No installer/release updated. Stop here and rotate.

Previous batch: F074 precise occurrence movement, phase 10 tasks 10.7a/b.
Tools > Move occurrence once offers explicit world/occurrence-frame translation,
arbitrary-axis rotation and typed pivot for one unconstrained unscaled Link to a
same-document Part solid/Body within structural Part containers. View-only non-pickable
wireframe preview and numeric world origin preserve the model until one Undoable
confirmation. Source/other occurrences, visibility and LinkTransform remain intact.
This is bounded progress for F072/F075; no copy, mate or solver detachment.

Both tasks preceded one FreeCADGui/FreeCADGui_Resources Release build, exit 0.
Initial grouped/ passed 7 TestOccurrenceAppearance and 7 TestCommandSearch but had
3 movement geometry failures. frame-probe-2/ identified a shared resolver bug:
App::Link lacks getGlobalPlacement(), so linked_shape omitted enclosing Part transforms.
BasicShapes/ShapeReferences.py now applies the parent's native global placement for
that case. Only this Python module was restaged; no corrective native build.
Movement tests now compare against independent native assembly-path geometry.

All 54 checks pass in resolver-verified/, without failures/errors/skips: 7 movement,
9 manufacturing export, 7 interference, 6 Make Unique, 14 Trim Body and 11 Isocline.
68 distinct selected passes including the initial unaffected appearance/command
suites; accepted process exits 0. Evidence:
D:\Temp\Office-PC\freecad-plus-occurrence-move-20261001.
acceptance-summary.json / validated-identities.json record accepted suites and hashes;
installed OccurrenceMove.py and ShapeReferences.py match source. FreeCADGui SHA256:
1959269e7ea02b2760f4cb914d4693dcec41f0e425441939e5324e28823f7608.

visual-accepted/ has six reviewed captures and Nested-Occurrences.FCStd /
Moved-Occurrences.FCStd. World/local nested transforms, arbitrary-axis pivots, both
LinkTransform settings, preview/commit agreement, Cancel/lifecycle cleanup, rollback,
Undo/Redo and reopened shared-source edits pass. Initial visual/ omitted the extra
scene node; FramebufferObject captures the preview using isolated settings. No global
preferences changed. tests/OccurrenceMove.md is the owner guide.

Whole F072/F074/F075 remain open for Copy, point picking/snapping, movable triads,
work-part frames, external/subassembly scopes, maintained relationships and physical/
high-DPI acceptance. No installer/release update. Stop for owner testing and rotate.

Previous batch: F087/F088 document updates, phase 7 tasks 7.5.7a/b.
Tools > Document updates exposes native deferred recompute, explicit one-time document
update and failed/pending/affected loaded dependency status. Object/input navigation
preserves visibility. Cached shapes do not imply current inputs. Native recompute
checks cycles, bypasses deferral only for the explicit action, preserves the session
mode and opens no extra model transaction. No custom persistence or update engine.

Both tasks preceded one FreeCADGui/FreeCADGui_Resources Release build, exit 0.
21 distinct selected checks pass without failures/errors/skips: 7 TestDocumentUpdates
in updates-accepted/, 7 TestDependencyInspector and 7 TestCommandSearch in grouped/;
accepted process exits 0. Evidence:
D:\Temp\Office-PC\freecad-plus-document-updates-20261001.
acceptance-summary.json / validated-identities.json record accepted suites and identities;
installed DocumentUpdates.py matches source. FreeCADGui SHA256:
d2aab61ea0e6db907281baa3323e86b0c1379e051fceb7a84ca53f7dd0eba2c7.

visual/ contains five reviewed captures and Update-Bracket.FCStd /
Update-Bracket-Repaired.FCStd. Deferred grouped dimension changes, native Cut failure
and affected Link, input navigation, repair, existing manufacturing STL stale refusal,
cycle rejection, owner transaction guards, Undo/Redo and session-mode reopen pass.
Loaded external dependencies are inspected without claiming to update the external
document. tests/DocumentUpdates.md is the owner procedure. Initial grouped/ and
updates-verified/ retain fixture errors requiring the source and owner to be saved
before a native external link. Only that fixture changed; no app restaging or second
build. Accepted checks span directories, not a claim that earlier aggregates passed.

Whole F087/F088 remain open for unique first-cause classification, targeted dependency
updates, asynchronous progress/cancellation, unloaded references, broader downstream
currency and physical/high-DPI acceptance. No installer/release update. Stop for
owner workflow testing and rotate to another item family.

Previous batch: F102 drawing setup, phase 15 tasks 15.3a/b.
TechDraw > Page > Create drawing sheet creates native same-document pages for one
root solid/Body, with A4/A3 border-only templates, drawing/model scale, base orientation,
first/third-angle projection and optional top/right views. Native links and update
preferences remain authoritative; no proxy/schema or geometry ownership changes.
Creation is one Undo transaction; stale/context/fit checks and failure rollback are
explicit. Cancel creates nothing. Broader drawing/annotation workflows remain open.

Both tasks preceded one TechDrawGui/TechDraw_Data Release build, exit 0. All 16 final
selected checks pass together in accepted-grouped/, without failures/errors/skips:
7 TestDrawingSetup, one native projection-group test, one native view test and
7 TestCommandSearch. Process exit 0. Evidence:
D:\Temp\Office-PC\freecad-plus-drawing-setup-20261001.
acceptance-summary.json / validated-identities.json record accepted suites and identities;
installed DrawingSetup.py matches source. TechDrawGui SHA256:
f53a78f0b512c8242e534042c1fec5e35b943eaade935ffb05e80c88e48c67e5.

visual-accepted/ contains five reviewed captures and Drawing-Source.FCStd,
Drawing-Sheets.FCStd / Drawing-Edited.FCStd. First/third-angle placement, scale,
Body Tip/source placement preservation, live source edits, Undo/Redo, save/reopen,
Cancel, stale/context/fit guards and rollback after forced partial creation pass.
tests/DrawingSetup.md is the owner procedure. Initial grouped/ passed, but visual/
exposed bundled sample material/approval text and a fixed projection symbol. The
Python module was corrected to select border-only templates and restaged; no second
native build. accepted-grouped/ reran the entire selected group successfully.
Workbench.cpp line endings restored after build; no semantic native change.

Whole F102 remains open for occurrence/arrangement/external sources, custom templates,
graphical preview, section/detail setup, broken-reference repair and physical/high-DPI
acceptance. F103 annotations remain separate. No installer/release update.
Stop here for owner testing and rotate to another item family.

Previous batch: F019 Make Unique, phase 12 tasks 12.2d/e.
Tools > Make occurrence unique reviews and copies one same-document native Part
containing an independent sketch and its solid Part extrusion, then relinks only
the selected occurrence. New native object identities and internal input remapping
preserve independent histories; placement and visibility stay unchanged. One Undo
step, no custom schema. Unsupported definitions/dependencies/consumers are rejected.

Both tasks preceded one FreeCADGui/FreeCADGui_Resources Release build, exit 0.
A Python selection correction for structural Part paths was restaged afterward;
no second native build. 19 distinct selected checks pass without failures/errors/skips:
6 TestUniqueOccurrence in unique-verified/, 6 TestFeatureOrganizer and 7 TestCommandSearch
in selected-grouped/, process exits 0. Evidence:
D:\Temp\Office-PC\freecad-plus-unique-occurrence-20261001.
acceptance-summary.json / validated-identities.json record accepted suites and identities;
installed UniqueDefinition.py matches source. FreeCADGui SHA256:
149486d68741474b996be733a55188737ea324b1214031a410fa291ea3885768.

visual/ has three reviewed captures and Shared-Spacers.FCStd / Independent-Spacers.FCStd.
Source and enclosing assembly placements are nontrivial. Copy/source independent edits,
native identities/input isolation, Undo/Redo, save/reopen, Cancel, stale/context guards
and rollback after forced post-copy failure pass. Edited unique spacer is 48*pi mm3;
original remains 63*pi mm3. tests/UniqueOccurrence.md is the owner guide.
Earlier grouped/ is incomplete after an invalid-selection modal; only the isolated
validation process was stopped. selected-grouped/ retains a readiness fixture failure
from hiding the source without recomputing, corrected before unique-verified/ passed.
The accepted results span directories; earlier aggregates did not pass in full.

Whole F019 stays open for broader definitions/Body histories/subassemblies, external
destinations, provenance, relationship remapping and physical/high-DPI acceptance.
No installer/release update. Stop for owner testing and rotate item families.

Previous batch: F014 feature organization, phase 10 tasks 10.6b/c.
Tools > Find and describe features searches the active document's loaded objects by
label, internal name, type and native Label2 description. Type filtering and sorting
are presentation-only; explicit model selection preserves visibility. Staged native
Label/Label2 edits apply in one transaction with stale/identity/read-only/context
checks. Link metadata stays local to that object; no copied source or new schema.

Both tasks preceded one FreeCADGui/FreeCADGui_Resources Release build, exit 0.
20 selected checks pass without failures/errors/skips: 6 feature-organizer in
organizer-verified/, 7 dependency-inspector and 7 command-search in grouped/;
process exits 0. Evidence:
D:\Temp\Office-PC\freecad-plus-feature-organization-20260930.
acceptance-summary.json / validated-identities.json record suites and source/native
identities; installed Python script matches source. FreeCADGui SHA256:
c1c081a7212b15ed4355872cedb8241ab873e46b18be67d1e7581d015e7bfa3d.

visual/ contains four reviewed captures and Feature-Notes.FCStd / Feature-Notes-Edited.FCStd.
Metadata search, explicit selection, native identity/order/link/placement preservation,
Undo/Redo, no-op Apply, Close, stale/replaced/read-only/pending guards and persistence
pass. Stock.Width edit after reopening still drives the hole radius, Boolean result
and linked occurrence. tests/FeatureOrganizer.md is the owner guide. Earlier grouped/
retains an empty-transaction fixture assumption, corrected with an actual owner edit;
no application changes after build, no script restaging or corrective build.

Search caps at the first 2000 loaded document objects with explicit partial disclosure.
Whole F014 remains open for folders, bulk organization, navigator integration,
uncapped/external search and physical/high-DPI acceptance. No installer/release update.
Stop for owner feedback and rotate to another item family.

Previous batch: F100 section planes, phase 15 tasks 15.1e/f.
Clipping View now reports explicit world/mm offsets and synchronized custom/camera
normals, pauses zero-direction clipping with recovery guidance, and saves/loads
four native planes in a versioned .fcsection file. Loading validates the whole
preset first and restores a fixed direction without changing camera/model state.
The dock scrolls so short windows do not compress direction controls.

Both tasks preceded the first grouped FreeCADGui/FreeCADGui_Resources Release build.
Three builds, all exit 0: initial, minimum field-height correction, final scrollable
container correction after visual review found parent clipping. Final accepted-grouped/
has all 22 checks passing, no failures/errors/skips: 6 section, 9 temporary-display,
7 command-search; process exit 0. Evidence:
D:\Temp\Office-PC\freecad-plus-sections-20260930.
acceptance-summary.json / validated-identities.json record accepted suites and
source/native identities. FreeCADGui SHA256:
a5636bf1387c47568b8dd65e2db8ba4467ca4b51b662310ac4de9bd3064e1a11.

visual-accepted/ contains six reviewed captures, Section-Housings.FCStd and
Housing-Section.fcsection. Two planes/flips, camera normals, zero recovery, invalid
preset atomicity, write failure, nested Part/direct-Link example reopen, owner
transaction/Undo preservation and whole BREP export pass. tests/SectionPlanes.md
is the owner procedure and preset contract. Earlier grouped/ retains wrong widget
lookup; earlier visual/sizing probes are not final acceptance. Default image backend
omitted clipping; FramebufferObject captures the cuts correctly. No global user
preferences were changed; captures used isolated validation configuration.

Whole F100 remains open for embedded saved views, caps, section curves/measurements
and physical/high-DPI acceptance. No installer/release update. Stop for owner
feedback and rotate to another dependency-ready item family.

Previous batch: F057 mirror result modes, phase 13 tasks 13.5a/b.
Part > Mirror offers native associative results or independent reflected-shape
snapshots for document-root shapes and whole Bodies. Both preserve source geometry,
visibility and Body Tip. Snapshots contain no Source/MirrorPlane links or copied
feature history. Creation is atomic; stale/replaced inputs, pending edits and missing
references receive inline feedback, and invalid results roll back for correction.

Both tasks preceded a grouped PartGui/PartScripts Release build. First compile
failed on TopoDS_Shape validity methods; getShape() correction passed, exit 0.
21 selected checks pass together in combined-recheck/, no failures/errors/skips:
6 result-mode, 6 native mirror, 2 existing mirror GUI and 7 command-search.
Process exit 0. Evidence: D:\Temp\Office-PC\freecad-plus-mirror-modes-20260930.
acceptance-summary.json and validated-identities.json record suites/source/native
identities. PartGui SHA256:
a6c60e615d42e30f0760ca2de7d89fde709fca505981e3c65007c67de3006d13.

visual/ has five reviewed captures and Mirror-Modes.FCStd / Mirror-Modes-Compared.FCStd.
Asymmetric reflected geometry, source/plane updates, snapshot independence, Cancel,
error rollback/recovery, Undo/Redo and save/reopen pass. After a source edit, source
and associative volumes are 276 mm3 while the snapshot remains 228 mm3. Owner guide:
tests/MirrorResultMode.md. Earlier grouped/ retains a Compound centre-of-mass fixture
lookup error and access violation entering command-search. Corrected fixture, separate
suites and full combined recheck pass; the access violation did not recur and its
cause is unestablished. No application changes after the successful build.

Whole F057/13.5 remain open for feature reevaluation, nested snapshots, graphical
preview and physical/high-DPI acceptance. No installer/release update. Stop for
owner feedback and rotate to another item family.

Previous batch: F049 missing-coincidence review, phase 11 tasks 11.6a/b.
Existing Validate Sketch now lists both endpoints and measured mm gaps. Row selection
highlights candidates; checkboxes default off. Add Checked Coincidences owns one
transaction, retains existing constraints and aborts failed solves. Sketch/tolerance/
construction-policy edits invalidate the list. Invalid tolerance never falls back.

Both tasks preceded a grouped SketcherGui/SketcherScripts Release build. First attempt
failed on the observer connection type; scoped_connection correction passed, exit 0.
22 selected checks pass, no failures/errors/skips: 5 repair in repair-verified/;
5 native coincidence validator, 5 sketch-support and 7 command-search in grouped/.
All process exits 0. Evidence: D:\Temp\Office-PC\freecad-plus-sketch-repair-20260930.
acceptance-summary.json and validated-identities.json record exact accepted suites,
sources and binaries. SketcherGui SHA256:
ed450a6370921ed0012d7d2dab6873b1d3078cb0053a12bfb1a9066163cbdedc.

visual/ has five reviewed captures plus Sketch-Repair.FCStd and Sketch-Repaired-Solid.FCStd.
Read-only review/Close, markers, subset repair, conflict rollback, stale results,
pending transactions, Undo/Redo and save/reopen pass. The repaired profile extrudes
to 1000 mm³ and updates to 1250 mm³ after Width changes on reopen. Owner procedure:
tests/SketchRepairReview.md. Earlier grouped/ has a wrong widget lookup; repair-final/
and repair-accepted/ retain fixture assumptions resolved by native probes. Application
source was unchanged after the successful build; no further build was needed.

Native coincidence insertion can move Block-constrained geometry, and the detector
can omit dimension-referenced endpoints. The final conflict fixture uses dimensioned
lines with unreferenced ends that cannot meet. These native limitations, duplicate/
self-intersection diagnosis, broader geometric preview and physical/high-DPI acceptance
keep whole F049/11.6 open. No installer/release update. Stop for owner feedback and rotate.

Previous batch: F101 interference/clearance inspection, phase 15 tasks 15.1c/d.
Part > Interference and clearance checks 2-12 explicitly listed whole native solids
or direct shape/Body occurrences using the shared world-shape resolver. Native common
solid volume and minimum distance classify overlap, contact within tolerance,
insufficient clearance and clear. Unsupported/unavailable inputs remain unresolved;
the summary discloses incompleteness and counted exclusions. Result navigation selects
the pair without visibility/model edits; document changes invalidate the report.

One grouped PartGui/PartScripts Release build, exit 0. All 23 checks pass on the first
run, no failures/errors/skips: 7 interference, 9 manufacturing-export and 7 command-search.
Process exit 0. Evidence: D:\Temp\Office-PC\freecad-plus-interference-20260930.
grouped/, acceptance-summary.json and validated-identities.json record results and
identities. Installed Python modules match source; no corrective build or restaging.
PartGui SHA256: 61bbc89f4924f7c447af2177661090878d43d2b1f5e1468cf776c0eee51b31c4.

visual/ has four reviewed captures and Interference-Check.FCStd. Analytic overlap/
contact/gap, tolerance boundary, rotated Part/direct-Link coordinates, save/reopen,
read-only behavior, dirty/missing/mixed inputs, identity guards, exclusions, selection,
edit invalidation and lifecycle pass. tests/InterferenceCheck.md is the owner procedure.
Whole F101/15.1 remain open for broader assemblies, per-pair exceptions, large-set
acceleration/cancellation, persistent reports and physical/high-DPI acceptance.
No installer/release update. Stop for owner feedback and rotate to another item family.

Previous batch: F018 occurrence appearance, phase 12 tasks 12.2b/c.
View > Occurrence appearance stages native whole-link visibility and uniform
colour/transparency. Use source appearance restores inheritance; Apply owns one
Undo transaction. Source/other links, placement, geometry and engineering material
remain unchanged. Structural Part container selection is supported; paths through
another Link are rejected. Arrays/per-element overrides and external/mixed definitions
remain outside this bounded pilot.

One grouped FreeCADGui/FreeCADGui_Resources Release build, exit 0. All 23 selected
checks pass, no failures/errors/skips: 7 occurrence in occurrence-accepted/, 9
temporary-display and 7 command-search in grouped/, all process exits 0. Evidence:
D:\Temp\Office-PC\freecad-plus-occurrence-appearance-20260930.
acceptance-summary.json and validated-identities.json record exact accepted suites
and identities. Installed script matches source; FreeCADGui SHA256:
9f9ffbc6c1773c42d948c018ec71fc1533d850e988757a33741d6856254307fc.

Earlier grouped/ retains a whole-link container-path selector failure and placement/
empty-transaction fixture assumptions; occurrence-final/ retains a duplicate View
menu lookup failure. Python-only selector correction was staged without another
native build; corrected fixture/menu assertions pass. Earlier aggregates are not PASS.

visual/ contains five reviewed captures and Occurrence-Appearance.FCStd. Apply,
Undo/Redo, save/reopen, placement/source isolation, Body Tip, reset, stale state,
scope rejection and lifecycle pass. tests/OccurrenceAppearance.md is the owner guide.
Whole F018 and parent 12.2 stay open for broader occurrence/representation behavior
and physical/high-DPI acceptance. No installer/release update. Stop for feedback
and rotate to another item family.

Previous batch: F098/F099 measurement meaning and point snapshots, phase 15 tasks 15.1a/b.
The existing Measure task shows operand identities, distance/frame meaning and
geometric-centre density exclusion. Distance Free remains native fixed world points;
new read-only UpdatePolicy/CaptureTime/CaptureSources fields retain explicit policy
and UTC capture provenance without live links. Manual point edits clear provenance;
restore and Undo/Redo preserve recorded state. Old files retain unknown capture data.

One grouped MeasureGui Release build (including Measure), exit 0. All 13 selected
checks pass without failures/errors/skips: 6 measurement in measurement-final/ and
7 unchanged command-search in grouped/, process exits 0. Evidence:
D:\Temp\Office-PC\freecad-plus-measurement-20260930.
acceptance-summary.json and validated-identities.json record suites/source/native
identities. MeasureGui SHA256:
20ee15fd1b6db168b8320cbec941682dd5c66466ba7ee408810918b37b85c8e1.
grouped/ retains an earlier legacy-fixture XML Count error; the corrected fixture
counts only persisted Property elements. No application correction or second build.

visual/ has two reviewed task-panel captures, snapshot-metadata.json and native-only
Measurement-Context.FCStd with both saved measurement types. tests/MeasurementContext.md
is the owner procedure. Circle-centre/gap meaning, units, occurrence world points,
unsigned deltas, source movement, fixed snapshots, coordinate-edit Undo/Redo,
save/reopen, legacy unknown capture and Close pass. Whole F098/F099 remain open for
broader mass/material, thickness, mesh accuracy, associative stale/invalid repair
and physical/high-DPI acceptance. No release update. Stop for feedback and rotate.

Previous batch: F015 dependency inspection, phases 7 and 10 tasks 7.5.5a / 10.6a.
Tools > Inspect dependencies presents native property edges, direct/transitive
inputs/consumers, expression reasons, native status and loaded external sources.
Explicit model selection preserves visibility; node inspection changes only the
root. Edits invalidate the snapshot; Refresh reads current state without recompute.
Cycles and 500-edge/8-level traversal limits are reported.

One grouped FreeCADGui/FreeCADGui_Resources Release build, exit 0. All 23 selected
checks pass with no failures/errors/skips: 7 dependency inspector in inspector-final/,
7 command search and 9 temporary display in grouped/. Process exits 0. Evidence:
D:\Temp\Office-PC\freecad-plus-dependencies-20260930.
acceptance-summary.json and validated-identities.json record suite/module identities.
Installed script matches source; FreeCADGui SHA256:
a54d51a83333161ba4c2574648159b56117a31489160709279b6bdd11d581582.
No corrective build or script restaging. Earlier grouped/ and inspector-accepted/
retain fixture failures: seam fillet, unsaved external-link documents and tree
expansion state. Initial capture counts missed native Fillet EdgeLinks alongside
Base; final capture retains both. Do not claim those earlier aggregates PASS.

visual-accepted/ contains three reviewed captures and Dependency-Inspection.FCStd.
Ready for owner testing: tests/DependencyInspector.md. Shared sketch, two extrusions,
fillet/drawing, expressions/external links, cycles/limits, native broken support,
Undo/save/reopen and lifecycle pass. Whole F015 remains open for target roles,
unloaded-reference diagnosis, integrated navigator tabs/highlights and physical/
high-DPI acceptance. No installer/release update. Stop refining this pilot pending
owner feedback or a demonstrated blocker; rotate the next family.

Previous batch: F124 sketch support, phase 11 tasks 11.7y/z.
Sketcher > Sketch > Inspect and change sketch support promotes the proven direct
planar core and exposes current support, explicit replacement, preserve-local/world
numeric preview and undoable Apply/repair. Preview uses a disposable document and
requires unchanged inputs at Apply. The cross-part reference adapter stays test-only.

One grouped SketcherGui/SketcherScripts Release build passed after both tasks.
All 39 selected checks pass (5 installed editor, 34 history adapters), no failures/
errors/skips, process exit 0. Evidence:
D:\Temp\Office-PC\freecad-plus-sketch-support-20260930.
Use grouped/, acceptance-summary.json and validated-identities.json. Installed
scripts match source. No corrective build or script restaging. visual/ contains
three reviewed dialog captures and the native-only Sketch-Support.FCStd example.
Rotated/constrained sketch and downstream extrusion, world preservation, local
missing-face repair, stale preview, cycles, Undo/Redo and save/reopen pass.

Ready for owner testing: tests/SketchSupport.md. Numeric preview evaluates placement
only; check dependent features after Apply. Whole F124 remains open for graphical
preview, broader support/occurrence and external-projection behavior and physical/
high-DPI acceptance. No installer/release update. Stop refining this pilot pending
owner feedback or a demonstrated blocker; rotate to another item family.

Previous batch: F127 manufacturing STL handoff, phase 15 tasks 15.7a/b.
Part > Manufacturing export lists explicit solid/whole-occurrence identities and
world dimensions. Fixed mm/world coordinates, editable Coarse/Normal/Fine quality,
custom per-user presets/reset, explicit selection replacement and overwrite prompt.
Reuse BasicShapes.ShapeReferences and MeshPart; stale/unsupported inputs reject
before output replacement. Inputs never silently retarget after deletion/reuse.

One grouped PartGui/PartScripts Release build, exit 0, after both tasks. All 20
selected checks pass (9 export, 4 parameter-command, 7 command-search), zero failures/
errors/skips and process exit 0. Evidence:
D:\Temp\Office-PC\freecad-plus-manufacturing-export-20260930.
Use export-accepted/ for export and grouped/ for the two unchanged suites.
acceptance-summary.json and validated-identities.json record the results. Source/runtime
scripts match; PartGui SHA256:
57a246ae57ef5b199b8e83cac490aec7d570ac2236d82a830ae350a3458d68f0.
Reimport checks dimensions/volume/nested and occurrence transforms. Sphere Fine
improves volume error: 10,598 facets versus 302 Coarse. visual/ has two reviewed
captures, Manufacturing-Handoff.FCStd and three STL example outputs. Final Python-only
mixed-compound guard was staged without another native build.
export-final/ retains the earlier missed rejection; probe/ shows the inherited
resolver reducing mixed compounds. Final guard checks original and resolved shapes;
export-accepted/ passes. No installer/release update.

Ready for owner testing: tests/ManufacturingExport.md. Whole F127 stays open for
STEP/3MF/DXF, configuration/orientation/unit overrides, mesh/deep occurrence inputs,
broader mesh checks and physical/high-DPI acceptance. Closed mesh is not a collision
or printability guarantee. Stop refining this pilot pending owner feedback or a
proven blocker; rotate to another dependency-ready item family.

Previous batch: F040 temporary isolate/hide, phase 10 tasks 10.5a/b.
View > Visibility has Temporarily isolate/hide selection and Restore previous/
original display. Native visibility only; per-document nested snapshots. Whole
Body results and whole linked occurrences preserve model/definition identities.
New objects retain current visibility, deleted/replaced identities are ignored,
and document close clears its stack. Model Undo/Redo is independent.

One grouped FreeCADGui/FreeCADGui_Resources Release build passed after both tasks.
All 20 selected tests pass with zero failures/errors/skips (9 temporary display,
7 command search, 4 parameter commands); process exit 0. Evidence root:
D:\Temp\Office-PC\freecad-plus-temporary-display-20260930.
Use grouped/, acceptance-summary.json and validated-identities.json. Source/runtime
scripts match; FreeCADGui SHA256:
097c5e0cf486bcbc75bc7a98731c83d80440a9146c2633c28d126744f7e2ac11.
No corrective build or script restaging. probe/ records native container behavior;
visual/ has five reviewed viewport captures and Temporary-Display.FCStd.

Ready for owner workflow testing: tests/TemporaryDisplay.md. Stop refining this
pilot without feedback or a demonstrated blocker. Whole F040 remains open for
linked-member overrides, save-time policy and physical/high-DPI acceptance.
Session stacks are not saved; saving while isolated stores current visibility,
so restore before saving. No installer/release update. Rotate the next item family.

Previous batch: F033 command search, phase 8 tasks 8.4.2a/b; phase 10.4 progress.
Standard Tools > Command search / Ctrl+K indexes loaded commands plus familiar
modeling aliases, displays current shortcuts and selected context, explicitly
switches workbenches and invokes existing commands. Pocket keyboard entry reaches
Subtraction and passes native geometry, Undo/Redo and save/reopen.

One grouped FreeCADGui/FreeCADGui_Resources Release build, exit 0. Final accepted
checks: 59 distinct passes (7 palette, 43 Extrude task, 5 Revolve task, 4 parameter
command), no failures/errors/skips. Evidence:
D:\Temp\Office-PC\freecad-plus-command-search-20260930.
Use search-final/ plus the three passing unchanged suites in verified/. verified/
contains initial palette failures; do not claim its aggregate PASS. grouped/ ran
zero tests due unavailable optional QtTest; key events now use QApplication.
Final Python-only palette corrections were staged without a second native build.
validated-identities.json records matching source/runtime and native hashes;
FreeCADGui SHA256 9bcb059b9c0428816035ca768715b0282776cb4d8ac3e30599fc2c7dd14c3f53.
visual/ contains three reviewed captures and Search-Pocket.FCStd for owner testing.

BUILD_ASSEMBLY=OFF in this development build; missing-workbench/context feedback
passes, while active-assembly recovery remains unverified. Favorites, broader
aliases/diagnoses, navigation presets and physical/high-DPI/localized acceptance
remain open. Whole F033 and parent tasks are not complete. tests/CommandSearch.md
is the owner procedure. Stop this pilot for feedback and rotate the next batch.
No installer/release update; publication recorded separately in commit/remote history.

Previous batch: phase 10 named-parameter pilot, 10.8aa/ab (F122).
Installed native Part-menu command, explicit Part/set ownership, marked native
parameter containers, same-document expression reference copying, and the promoted
length/angle editor/core. Prototype imports forward to application modules.
One grouped PartGui/PartScripts Release build passed after both features were ready.
Final selected checks: 90 distinct passes (4 command, 14 editor, 22 capability,
24 Trim Body GUI, 26 Isocline GUI); no failures/errors/skips in accepted results.
Evidence: D:\Temp\Office-PC\freecad-plus-parameter-command-20260930.
Use built/ for the four unchanged suites and command-final/ for the final command
suite. built/ includes an earlier external Windows clipboard-lock failure, so its
aggregate is not claimed PASS. The final copy test checks the requested clipboard
payload through a test double and drives a real feature expression with it.
Physical copy/paste remains owner acceptance. Initial Python appendMenu failed for
the native workbench; the command is now registered in native Workbench.cpp.

visual-final/ contains two reviewed dialog captures and the native
Named-parameters-enclosure.FCStd example. acceptance-summary.json and
validated-identities.json record matching source/runtime modules and native hashes.
PartGui SHA256: 41bde8dbd15017f005b1937afd9e5d80fb2c90d0f83274922254324d7bb8440a.

Stop at this usable pilot for owner workflow testing. tests/NamedParameters.md
contains the entry point, example and step-by-step test. Do not continue polishing
F122 without owner feedback or a demonstrated blocker/dependency. Where-used,
publication/configuration scope and physical/high-DPI acceptance remain pending.
No release/installer update. Previous CAM and Extrude follow-ups remain recorded.

Previous batch: phase 6 indexed STL CAM output, task 6.4.3 (bounded F089/F097).
User requested diversification from repeated F029-F032 batches; start-reference
follow-up is deferred. Fixed indexed operation generation rewriting recomputed
model/stock producers and permanently blocking export. Consume current producers,
reject stale inputs and schedule indexed stock as an operation dependency.

Final acceptance: 116 distinct passing tests, no failures/errors/skips in the
selected results, process exits 0. Evidence root:
D:\Temp\Office-PC\freecad-plus-indexed-output-20260930.
Use acceptance-summary.json, validated-identities.json, the three existing suites
from fixed/ (24 + 7 + 82), and the final new suite from verified/ (3). The mixed
fixed aggregate contains earlier fixture failures; do not call it a full PASS.
17 retained output fixtures cover 180/45-degree jobs, both supported strategies,
LinuxCNC/Grbl, shared-tab edits, custom-origin isolation and exact saved commands.
Regenerated output matches current native paths and retains sampled tab clearance.

Open: 45-degree Waterline regenerated contours differ by up to 0.172558 mm in the
bounded comparison (persistence-comparison.json); viewport/indexed interaction and
material-removal simulation also remain unvalidated. 6.4.3 and whole F089/F097 stay
open. A slow OCC oracle was interrupted; its overlapping exploratory launch is
excluded from acceptance. Final verified/ was isolated. Source/runtime hashes
match; Python-only batch, no native rebuild, installer or release.
Rotate the next implementation batch to another dependency-ready item family;
retain contour repeatability as an explicit bounded follow-up, not an endless audit.

Previous product batch: phase 8, tasks 8.1.4e/f, advancing F029-F031. Extrude
end-limit typing/picking now reject self and downstream links before assignment.
Typed datum/origin planes follow the existing Body/type selection policy. Rejected
picks retain saved links and displayed names while keeping the picker active;
typed rejection, correction, invalid OK and edit Cancel remain recoverable.
Both fixes and six GUI cases preceded one native PartDesignGui Release build.
Final acceptance: 213 distinct passing tests, zero failures/errors/skips, macro
PASS and exit 0. Evidence:
D:\Temp\Office-PC\freecad-plus-extrude-reference-gates-20260930, including baseline,
baseline-scope, build.log, grouped, visual, acceptance-summary.json and
validated-identities.json. Old binaries reproduced typed foreign-plane scope
bypass; the final baseline assigns a unique foreign-origin label. Deliberate
cycles were not assigned to old binaries; the source audit found the missing guard.
No corrective native rebuild. All three source identities, staged test and native
hashes match. PartDesignGui SHA256:
065d9f5af5615cfcef42909b801840e0457132b924fb3420afca98376fa36969.
Three task captures are readable. New checks cover both sides/aliases, direct/
indirect synthetic dependants, rejected picks, correction, foreign/owned planes,
invalid OK and edit Cancel links/Body Tip/geometry/dependency preservation.
All 127 item specifications remain intact. Start-reference and broader command/
occurrence/global-filter, physical input/high-DPI and F032 Apply/repeat acceptance
remain open. No installer/release or format change. The older executable stamp
is not rebuilt-module identity. Next bounded focus: audit start-reference
restrictions/recovery separately, then group related changes before building.

Previous product batch: phase 8, tasks 8.1.4c/d, advancing F029/F032. Empty or
malformed Extrude face-limit text clears only the edited side's saved link,
invalidating the preview instead of retaining the previous valid result. Invalid
OK keeps the editor open with automatic preview on/off. Typed datum/origin planes
update their saved links and geometry before OK. Correction and Cancel recover.
Both fixes and six GUI cases preceded one native PartDesignGui Release build.
Final acceptance: 207 distinct passing tests, zero failures/errors/skips, macro
PASS and exit 0. Evidence:
D:\Temp\Office-PC\freecad-plus-extrude-limit-recovery-20260930, including baseline,
build.log, grouped, extrude-final, visual, acceptance-summary.json and
validated-identities.json.
Old binaries reproduced stale links, invalid OK closing the editor and delayed
plane assignment. Numeric missing-face errors already worked. The fixture now
checks a cleared PropertyLinkSub as None; its initial errors are preserved. Final
37-test Extrude GUI and 170 broader grouped checks pass on unchanged binaries.
No corrective native rebuild. All three source identities, staged test
and native hashes match. PartDesignGui SHA256:
7db59a73df9cc8f05193145f1a30265b52ae992506473cc636ed389c900a8b11.
Three task captures are readable. Tests include both sides/aliases, malformed
and missing inputs, correction, edit Cancel links/Body Tip/geometry, typed planes,
Undo/Redo and save/reopen followed by another plane move. All 127 item specs remain
intact. Broader command/occurrence/dependency-selection, physical input/high-DPI
and F032 Apply/repeat gates remain open. No installer/release or format change.
The older executable stamp is not rebuilt-module identity. Its end-limit selection
restriction follow-up is completed above.

Previous product batch: phase 8, tasks 8.1.4a/b, advancing F029. Extrude now
labels total symmetric and independent per-side lengths. Typed second-side face
limits update their own reference instead of the first-side preview link.
Both changes and six regression cases preceded one native PartDesignGui Release
build; no corrective rebuild. Final acceptance: 201 distinct passing tests,
zero failures/errors/skips, macro PASS and exit 0. Evidence:
D:\Temp\Office-PC\freecad-plus-extrude-extents-20260930, including baseline,
baseline-model-final, build.log, grouped, extrude-final, visual,
acceptance-summary.json and validated-identities.json. Old binaries reproduced generic labels and wrong-side
reference assignment. The persistence fixture now uses saveCopy to avoid opening
and then closing the active source document; initial failure evidence is retained.
The grouped GUI fixture assumed Pad's axis for Pocket; corrected opposite-direction
bounds pass in the final 31-test GUI run, alongside 170 passing grouped checks
on unchanged native binaries. All six source identities, staged tests and native
hashes match. PartDesignGui SHA256: 57acdd8b8fd4c545cfdf98fc18b15503aa6b542e7fac7604783d2b0214d2e3a5.
Three task captures are readable. F029's specified Extrude acceptance is verified:
face movement and signed end offsets remain associative; symmetric/two-sided spans
match labels; removed limits retain errors until repaired. Includes edit Cancel,
Undo/Redo, missing subelements and save/reopen followed by another face move.
All 127 specifications remain intact. Broader command-family and physical input/
high-DPI gates remain open; no installer/release or native-format change.
The older executable stamp is not rebuilt-module identity. Its typed-limit recovery
follow-up is completed above.

Previous product batch: phase 8, tasks 8.1.3m/8.1.5d, advancing F030-F032.
Combined Pattern retains saved direction/axis links when unfinished reference
picking ends through Originals controls, scope/type changes or OK. Abandoned
pickers stop consuming later selections. Body/sketch/datum rejection explains
accepted types; the Pattern result and supported dependants keep dependency reasons.
Both tasks preceded the initial native build. The first grouped run passed all
six new tests and 122 broader checks, but found one existing result-specific
diagnostic regression. One corrective rebuild followed. Final acceptance:
167 distinct passing tests, zero failures/errors/skips, macro PASS and exit 0.
Evidence: D:\Temp\Office-PC\freecad-plus-pattern-picker-recovery-20260930,
including baseline, build-initial.log, build.log, grouped, verified, visual,
acceptance-summary.json and validated-identities.json. Baseline old binaries
reproduce saved-link loss, stale picking and misleading rejection; failures after
failed loop cleanup are not independent defects. Final 45 Pattern task/model
and 122 broader tests pass on identical final native binaries. Source, staged test
and binary hashes match. PartDesignGui SHA256:
b2e935fb8bc4272854139c581a97aa8b53fdb142c467e94141d14d03c1fe2c65.
Three task captures are readable. All 127 item specifications remain intact.
The older executable stamp is not rebuilt-module identity. No installer/release.
Broader command/occurrence/disambiguation, physical input/high-DPI and F032
Apply/repeat gates remain open. Its F029 follow-up is completed above.

Previous product batch: phase 8, tasks 8.1.3k/l, advancing F030/F032. Combined Pattern
Direction/Direction 2/Circular Axis now show reference counts and picking state,
with accepted-type tooltips and Highlight reference. Inspection preserves links and
selection paths, isolates other pickers and restores source/Origin visibility.
Both tasks preceded the initial native build; two corrective incremental rebuilds
added source-path visibility lookup and restored reference combos for subsequent OK.
Final acceptance: 161 distinct passing tests, zero remaining failures/errors/skips.
Evidence: D:\Temp\Office-PC\freecad-plus-pattern-references-20260930, including
three build logs, grouped, pattern-final, verified, pattern-accepted, visual,
acceptance-summary.json and validated-identities.json. Initial fixture failures
are retained: PySide parent-wrapper lifetime and canonical GUI versus resolved
reference paths. Final 39 Pattern task/model tests pass, macro PASS, exit 0, plus
122 passing verified checks on identical final native binaries. Six new GUI cases
include reference recovery, role isolation, saved links after OK, source/Origin
visibility and Cancel selection recovery. Five source identities, staged test and
native hashes match. PartDesignGui SHA256:
abb35d8b7cdbc7e0822f2280c7aa7c2af4f38448adbeb649655cea732e677d0b.
Four reference captures are readable. Physical viewport/input/high-DPI and broader
occurrence acceptance remain open. The older executable stamp is not rebuilt-module
identity. All 127 item specifications remain intact. No installer/release. F032
Apply/repeat remains open. Its reference recovery/rejected-pick follow-up is
completed above.

Previous product batch: phase 8, tasks 8.1.2c/8.1.3j, advancing F030/F031. Combined
Pattern preselection and later Originals picks share document/Body/type/dependency
validation and assignment. Mixed inputs retain valid originals and explain rejects;
invalid-only input keeps a useful task. Rejected later picks leave the collector
active; correction or Clear dismisses feedback. Legacy startup behavior is retained.
Both tasks preceded one successful PartDesignGui Release build. Final acceptance:
155 distinct passing tests, zero remaining failures/errors/skips. Evidence:
D:\Temp\Office-PC\freecad-plus-pattern-selection-20260930, including build.log,
grouped, pattern-final, visual, acceptance-summary.json and validated-identities.json.
The initial fixture compared raw Originals input order. Native evaluation already
uses Body-history order; the corrected test compares membership/settings and both
geometric differences for Linear/Circular. All 33 Pattern task/model tests pass,
macro PASS, exit 0, plus 122 unchanged passing grouped checks on the same binaries.
No second native build. Four changed source identities, staged tests and binaries
are verified. PartDesignGui SHA256:
b1123a2ba699ab3f709d37a64419c2ca74b257b491946c037e7b453543b614c4.
Three mixed/rejected/recovered captures are readable. Physical viewport/input/
high-DPI acceptance remains open. The older executable stamp is not rebuilt-module
identity. All 127 item specifications remain intact. No installer/release. Broader
command-family/disambiguation/occurrence and F032 Apply/repeat remain open.
Its reference feedback/inspection follow-up is completed above.

Previous product batch: phase 8, tasks 8.1.3i/8.1.5c, advancing F030-F032. Combined
Pattern now inspects Originals rows by object identity, highlights all entries when
no row is selected, isolates reference picking and restores temporary visibility.
Creation/edit Cancel restores the original object/subelement selection and model.
Both tasks preceded one successful native PartDesignGui Release build. Final
acceptance: 149 distinct passing tests, zero remaining failures/errors/skips.
Evidence: D:\Temp\Office-PC\freecad-plus-pattern-inspection-20260930, including
build.log, grouped, final, visual, acceptance-summary.json and validated-identities.json.
Initial evidence retains a test-fixture visibility baseline failure and a later
inactivity timeout in Revolve (cause unconfirmed). The corrected fixture captures
visibility before entering edit. A fresh process passed 82 Pattern/Revolve/Trim/
Isocline checks, macro PASS, exit 0; 67 unchanged passing grouped checks are reused
on the same native binaries. No second native build. All five changed source
identities, staged test and native hashes match. PartDesignGui SHA256:
70fc6c433231bbabe8c1041eee565f10c91201da119ef4f02a9de3611af7bafc.
Three task-pane captures are readable; physical viewport/input/high-DPI remains
open. The older executable stamp is not rebuilt-module identity. All 127 item
specifications remain intact. No installer/release. Broader F030 command-family/
disambiguation/occurrence and F032 Apply/repeat remain open. Its Pattern preselection/feedback follow-up is completed above.

Previous product batch: phase 8, tasks 8.1.3f-h, advancing F030/F032. Combined Pattern
now shows Originals count/type/picking state, offers Clear with replacement recovery,
and coordinates originals with the embedded direction picker so one pick cannot
fill both roles. Whole body retains the selected-feature list and disables Clear.
Three tasks preceded one native PartDesignGui Release build and one grouped run:
144 distinct passing tests, 149 executions (five repeated Pattern model cases),
zero failures/errors/skips, macro PASS, process exit 0. Five new GUI cases cover
feedback/reopen, Clear recovery/settings, Cancel/Undo/Redo and role transitions.
Evidence: D:\Temp\Office-PC\freecad-plus-pattern-collectors-20260930, including
build.log, grouped/results.json, acceptance-summary.json and validated-identities.json.
Seven changed source identities and staged test hash match; PartDesignGui SHA256:
0843f5f52fd8bce6e68b952dc8f89cb2a3136ca47fa8f6baf702150467a83639.
Readable layouts and radio/model states are recorded in visual-final. The first
capture caught an unfinished radio animation; allowing Qt to settle corrected
the evidence without a product change or rebuild. Old executable version stamp
is not rebuilt-module identity; no installer/release. Broad F030/F031 inspection/
occurrence/disambiguation and physical gates, plus F032 Apply/repeat remain open.
Its Pattern inspection/selection recovery follow-up is completed above.

Previous product batch: phase 8, tasks 8.1.3d/e, advancing F030. Extrude/Pad/Pocket
profile row inspection and Highlight activate Profile without changing references;
count/type/picking feedback stays current on mutation and reopen. Inspection
visibility restores on Cancel and OK. Both tasks preceded one successful native
PartDesignGui Release build and one grouped run: 142 passes, zero failures/errors/
skips, macro PASS, process exit 0. Four added Extrude tests pass; existing Pad,
Extrude/Pocket model, Revolve/Pattern, Trim and Isocline suites also pass.
Evidence: D:\Temp\Office-PC\freecad-plus-extrude-collectors-20260930, including
build.log, grouped/results.json and validated-identities.json. Changed source and
staged tests hash-match; PartDesignGui SHA256:
1c1bef4b22a721fdc1335da5233062e21262dd0750ad3e56bbec39621adef3ce.
Three collector captures under visual are readable without clipping. Executable
version stamp remains older than rebuilt modules; no installer or release.
Broad F030 other-family/disambiguation/occurrence and physical interaction gates
remain open. Its Pattern collector follow-up is completed above.

Previous product batch: phase 8, tasks 8.1.2b/8.1.5b. F031's Extrude parity,
mixed-selection and Cancel acceptance example is complete for the active-Body
workflow. Extrude/Pad/Pocket reuse one profile gate; ambiguous picks stay in the
collector and invalid picks receive inline feedback. Cancel restores original
subelement selection and profile/Body Tip state for creation and editing.
Both tasks were grouped before the native build; regression-found edit snapshot
timing was fixed and rebuilt. Final 138 checks pass: 24 corrected Extrude tests
plus 114 passing grouped checks on the same native modules, zero remaining
failures/errors/skips, final macro PASS and process exit 0. Evidence root:
D:\Temp\Office-PC\freecad-plus-extrude-selection-20260930.
See acceptance-summary.json, validated-identities.json, build.log, verified,
extrude-final and visually checked captures in visual. Initial failures retained;
test-only compound/quantity fixture corrections require no further native build.
PartDesignGui SHA256 02d7224188574514a67f5a981d9a25cd5100f53f72c7df0256b248c76093e76c.
The executable's older version stamp is not the rebuilt module identity. No
installer/release. Broad occurrence/other-family and physical interaction gates
remain open. Its F030 Extrude collector follow-up is completed above.

Previous product batch: phase 5, tasks 5.1.12/5.2.4. F070 functional acceptance
is complete for the documented bounded single-angle workflow. The Isocline task
now edits Curve tolerance with length units and the existing native range, blocks
invalid drafts even with preview paused, and preserves expression-driven values.
Five new regressions cover tolerance limits/recovery, unit/editor/persistence
lifecycle, and oriented-normal plus pull reversal. All 130 grouped Isocline/Trim
and Pad/Extrude/Revolve/Pattern checks pass; zero failures/errors/skips, macro PASS,
process exit 0. Evidence:
D:\Temp\Office-PC\freecad-plus-isocline-tolerance-20260930\grouped.
Four changed source/development-build Python hashes match; existing fork engine
802e19d648, no native rebuild or release. Physical viewport/keyboard/high-DPI
acceptance remains 5.2.3; arbitrary singular-surface completeness is not claimed.
Its next F031 Extrude slice was completed in the phase 8 batch above.

Release 0.0.2 is built, validated and publicly published after 0.0.4:
https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.2
Packaging/tag: 71358d8fbf40122e6c998008e7ab3ca741dbc773; unchanged application:
802e19d64863ecdfc02817a2160b621579c2d8f2. All 14,584 runtime file hashes match the
0.0.4 tested payload, so its 312-pass evidence is reused rather than rerun.
New installer checks pass: all 14,586 installed hashes, launch/save/reopen,
shortcut/registration, uninstall and unrelated-file preservation. One Windows
installer asset, 356,439,411 bytes, unsigned; GitHub digest matches SHA256
69d9b406904bb49c22f1efddc1769bae10147edbe38ae0bc1c8993796bb0ddfe.
Evidence: D:\Temp\Office-PC\freecad-plus-release-0.0.2. Release ID 399816257;
public pre-release and source tag verified. Disposable installation removed.
Existing releases unchanged. Physical-machine, clean-VM and broader roadmap
acceptance remain open; no new application features were added in this packaging task.

Release 0.0.4 is built, validated and publicly published:
https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.4
Source/runtime/tag: 802e19d64863ecdfc02817a2160b621579c2d8f2.
Full native build passed, CAM startup fixes 16.2bs/bt passed 55 grouped tests, and
all 312 final packaged regressions pass with zero failures/errors/skips. Installed
launcher/save/reopen, 15,532 installed file hashes, shortcut/registration and
uninstall preservation checks pass. One Windows installer asset, 360,831,616 bytes,
GitHub digest matches SHA256 e5ea99f9b3e556c65f6dadcc5ade42eb4e2531b79f55ae5757ec9eec891e7464.
Evidence: D:\Temp\Office-PC\freecad-plus-release-0.0.4. Public pre-release verified;
release ID 399799828. Installer unsigned; engine remains 26.3.0. Physical-machine,
clean-VM and broader roadmap acceptance remain open. Disposable installation removed;
only the deliberate unrelated-file preservation fixture remains.

Release 0.0.1 Windows x64 installer is built, accepted and published:
https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.1
Verified public pre-release state, one installer asset and matching GitHub SHA256.
Release/tag commit 1a962bb23d; application source 2df76790b4. Evidence/artifact root:
D:\Temp\Office-PC\freecad-plus-release-0.0.1. Full build plus revision refresh
reports application source 2df76790b4; 120 staged tests pass and staged/installed
launcher, installed hashes, shortcut and uninstall checks pass. Unrelated test file
survives uninstall. Publication complete; see roadmap release checkpoint.
Packaging uses separate per-user FreeCADPlus settings and does not alter upstream
FreeCAD. The distribution version differs from the retained 26.3.0 engine version.

Latest roadmap batch: 16.2bq/br Plunge Milling postprocessing and persistence probes.
Grouped validation: 87 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-post-reopen-20260930-batch.
Macro PASS; process ended. G83 output passes real LinuxCNC and Grbl processors with
a mock job/configuration wrapper. FCStd reopen and forced regeneration preserve
settings and commands. Existing engine 2df76790b4 plus staged Python fixes; no native
rebuild, production changes or release. Other post/cycle combinations and physical
controller/machine acceptance remain pending.

Previous roadmap batch: 16.2bo/bp Plunge Milling cycle settings and variants.
Grouped validation: 84 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-cycles-20260930-verified.
Macro PASS; process ended. Source/staged PlungeMilling.py hashes match. Initial
negative-depth fixture correction is recorded in the roadmap. G82/G83/G73 command
checks now pass; controller postprocessing and physical machine acceptance remain
pending. Engine 2df76790b4; no native rebuild or release.

Previous roadmap batch: 16.2bm/bn Plunge Milling motion and cycle feed/cancellation.
Grouped validation: 82 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-motion-20260930-verified.
Macro PASS; process ended. Source/staged PlungeMilling.py hashes match. Initial
assertion corrections and final cycle retract are recorded in the roadmap.
Engine 2df76790b4; no native rebuild or release. Ordinary plunge/G81 command checks
pass; peck/dwell variants, postprocessor and physical machine acceptance remain open.

Previous roadmap batch: 16.2bk/bl Dogbone readiness and cutter validation.
79 CAM failure/recovery checks and 24 Dogbone geometry checks pass; zero final
failures/errors/skips. Evidence under D:\Temp\Office-PC\freecad-plus-validation-20260928:
cam-dogbone-readiness-20260930-batch and cam-dogbone-geometry-20260930-verified.
Macros PASS; processes ended. Source/staged DogboneII.py hashes match. Initial
geometry mock correction is recorded in the roadmap. Engine 2df76790b4; no native
rebuild or release. Physical GUI/machine acceptance remains pending; native skipped
recompute caching remains export-blocked.

Previous roadmap batch: 16.2bi/bj Plunge Milling/Boundary input readiness.
Grouped validation: 77 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-boundary-readiness-20260930-batch.
Macro PASS; process ended. Source/staged PlungeMilling.py and Boundary.py hashes match.
Engine 2df76790b4; no native rebuild or release. Explicit generation rejects stale
base/stock inputs and clears output; repaired inputs recover. Native skipped
execution may retain export-blocked caches. Physical GUI/machine acceptance pending.

Previous roadmap batch: 16.2bg/bh Dragknife/Ramp Entry input readiness.
Grouped validation: 74 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-entry-readiness-20260930-batch.
Macro PASS; process ended. Source/staged Dragknife.py and RampEntry.py hashes match.
Engine 2df76790b4; no native rebuild or release. Explicit generation clears/rejects
stale inputs and repairs regenerate output; skipped-native-recompute caches remain
export-blocked. Physical GUI/machine acceptance remains pending.

Previous roadmap batch: 16.2be/bf Axis Map/Z Correction readiness and cache cleanup.
Grouped validation: 72 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-axis-zcorrect-readiness-20260930-batch.
Macro PASS; process ended. Source/staged AxisMap.py and ZCorrect.py hashes match.
Engine 2df76790b4; no native rebuild or release. Native skipped-recompute caches
remain export-blocked; explicit generation clears/rejects stale inputs. Physical
GUI/machine acceptance remains pending.

Previous roadmap batch: 16.2bc/bd production Array/Mirror input readiness.
Shared requireCurrent guards base paths and Mirror center/reference geometry.
Grouped validation: 69 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-array-mirror-readiness-20260930-verified.
Macro PASS; process ended. Array.py/Mirror.py staging hashes match source; engine
2df76790b4, no native rebuild or release. Explicit generation rejects and clears
stale output; skipped-native-recompute caching remains export-blocked. Physical
GUI/machine acceptance remains pending. Initial fixture correction is in roadmap.

Previous roadmap batch: 16.2ba/bb production Boundary2 linking and empty results.
Linking uses native command Parameters for Z; empty clipping emits no moves.
Grouped validation: 66 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-boundary-links-20260930-final.
Macro PASS; process ended. Boundary2.py source/staging hashes match; engine
2df76790b4, no native rebuild or release. Earlier fixture failures and corrections
are recorded in the roadmap. Physical GUI/machine acceptance remains pending.

Previous roadmap batch: 16.2ay/az production holding-tag setup/query checks.
Setup clears path/tool caches, validates base readiness and positive finite tool
diameter; direct point queries rebuild current setup rather than reuse stale data.
Invalid tool/producer checks, export blocking and recovery pass.
Grouped validation: 64 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-tag-setup-20260930-batch.
Macro PASS; process ended. Matching Tags.py staged into engine 2df76790b4;
no native rebuild or release. Query interaction performance/physical acceptance
remain unmeasured; native skipped-recompute caching remains as documented.

Previous roadmap batch: 16.2aw/ax production direct holding-tag edit safeguards.
processTags clears old output and checks base readiness; setXyEnabled refreshes
path data and checks inputs before replacing Positions/Disabled. Direct failure/
repair tests pass; no physical task-panel acceptance is claimed.
Grouped validation: 62 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-tag-direct-edit-20260930-batch.
Macro PASS; process ended. Matching Tags.py staged into engine 2df76790b4;
no native rebuild, release or machine testing. Native skipped-recompute cache
behavior from 16.2au/av remains unchanged and export-blocked.

Previous roadmap batch: 16.2au/av production dressup input readiness.
Utils.requireCurrent guards Boundary2 base/boundary and holding-tag base execution.
Explicit generation rejects stale dependencies and clears output; repair recovers.
Grouped validation: 60 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-dressup-readiness-20260930-verified.
Initial batch had two expectation failures: native recompute can skip downstream
execution after upstream failure, retaining cache. Tests now verify export rejects
that cache before explicit execution clears it. Automatic skipped-execution cache
clearing and direct task callbacks remain separate gaps. Macro PASS; process ended.
Three matching modules staged into engine 2df76790b4; no native rebuild or release.

Previous roadmap batch: 16.2as/at production Boundary2 failure handling.
Output clears before generation; null/invalid/non-solid offsets reject before
clipping. Tests verify late-generation failure and null/plane offsets produce empty
Invalid output, block export and recover after correction.
Grouped validation: 58 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-boundary2-failures-20260930-batch.
Macro PASS; process ended. Matching Boundary2.py staged into engine 2df76790b4;
no native rebuild, release, machine or physical GUI acceptance.

Previous roadmap batch: 16.2aq/ar production holding-tag failure behavior.
Missing base clears cached path/tag/solid/pathData. Processing exceptions clear
output and propagate instead of substituting the untagged base path; native invalid
state blocks export and recovery regenerates tags. Separate from stock-bridge tabs.
Grouped validation: 56 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-holding-tag-failures-20260930-batch.
Macro PASS; process ended. Matching Tags.py staged into isolated engine 2df76790b4;
no native rebuild, release, machine or physical GUI acceptance.

Previous roadmap batch: 10.8y/z explicit Part parameter-set creation/editor entry.
create_parameter_set owns an undoable native container-creation transaction;
edit_parameter_set targets an explicit Part-owned container independently of active
document state. Ownership, Body/occurrence rejection and save/reopen pass.
Grouped validation: 75 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-part-scope-20260930-verified.
Initial batch had one empty-transaction fixture mismatch; corrected with a real
caller label edit. Macro PASS; process ended. Engine 2df76790b4; no native rebuild
or release update. Prototype only; full scope/publication/where-used and production
registration remain pending. Container creation is separate from editor lifetime.

Previous roadmap batch: 10.8w/x enclosure editor acceptance checks.
Actual prototype widgets drive width/clearance/spacing geometry, rename and inch
display. Unit/cycle/zero-width errors preserve geometry and remain correctable;
save/reopen allows editing through a fresh dialog. Application code unchanged.
Grouped validation: 73 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-enclosure-editor-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Automated T13 prototype slice is connected end to end; physical input/accessibility,
production integration and broader parameter requirements remain pending.

Previous roadmap batch: 10.8u/v native enclosure parameter benchmark.
Width/lid clearance/hole spacing drive native geometry; rename, unit/cycle rejection
and persistence pass. Shared occurrence placements and separate-definition isolation
survive parameter edits and Undo/Redo. This is bounded T13 evidence, not production UI.
Grouped validation: 71 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-enclosure-20260930-verified.
Initial batch had one fixture-readiness error; recompute after visibility setup fixed
it. Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Production integration, full physical T13 and broader occurrence consumers remain open.

Previous roadmap batch: 10.8s/t parameter descriptions and display-only units.
Creation stores native property documentation; read-only description survives
Undo/Redo, rename and save/reopen. Dialog length/angle display conversion leaves
stored values, expressions and geometry unchanged; no unit preference is persisted.
Grouped validation: 69 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-units-description-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Uninstalled prototype. Existing-description editing, localized display, physical
accessibility, full T13 and production integration remain pending.

Previous roadmap batch: 10.8q/r typed parameter creation prototype and dialog.
create_parameter adds native Length/Angle properties atomically, with explicit units
and ASCII identifier names. Invalid names/units/references leave no partial property.
Creation supports Undo/Redo/persistence; dialog correction and selection checks pass.
Grouped validation: 67 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-create-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Still uninstalled: parameter-object creation, deletion/where-used/publication,
broader types/scope, physical UI/accessibility and production integration remain open.

Previous roadmap batch: 10.8o/p prototype parameter-list and two-editor handling.
Loading a stale dropdown disables edit controls and requires Refresh. External
rename/removal, empty lists and subsequent additions recover. Same-object dialogs
reject conflicting drafts; closing one does not remove the other's observer.
Grouped validation: 65 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-editor-schema-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
The editor remains an uninstalled prototype. Physical UI/accessibility, broader
reference synchronization and full production parameter functionality remain open.

Previous roadmap batch: 10.8m/n parameter editor refresh/conflict and lifecycle.
External value/Undo changes reject stale Apply/Rename until explicit Refresh.
Deleting the parameter object or document closes the dialog and detaches observation;
subsequent edit calls do nothing. The dialog remains an uninstalled prototype.
Grouped validation: 62 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-editor-lifecycle-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
External property-list interaction, multi-dialog and physical UI/accessibility need
further acceptance; production integration and broader parameter requirements remain open.

Previous roadmap batch: 10.8k/l uninstalled parameter editor dialog prototype.
Existing length/angle selection, expression Apply, Rename and Close reuse atomic
helpers. Native widget tests cover commit boundaries, error correction, angle edits
and rename collision recovery; no application command has been registered.
Grouped Qt/model validation: 59 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-editor-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Physical UI/accessibility, external-document lifecycle, creation/deletion, where-used
and production integration remain pending. TestParameterEditor joins the three
architecture suites for future changes to this dialog/helpers.

Previous roadmap batch: 10.8i/j atomic parameter-expression edit prototype.
edit_parameter_expression validates units, owns a transaction, checks affected
native recompute state and rolls back failed geometry. Stale affected consumers and
caller-owned transactions reject before mutation; a disconnected invalid box does
not block a valid edit. Undo/Redo and native persistence pass.
Grouped architecture validation: 56 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-edit-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild, installed editor
or release update. Object-level dependency scope is conservative through containers;
production UI, property-level impact analysis and external/proxy effects remain open.

Previous roadmap batch: 10.8g/h atomic parameter rename and label-reference checks.
Test-only rename_parameter owns its transaction; native naming errors restore owned
formulas/consumers. Unrelated pending edits reject before mutation. Label-based and
internal-name references survive rename, Undo/Redo, label edit and save/reopen.
Grouped architecture validation: 54 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-rename-safety-20260930-batch.
Macro PASS; process ended. Existing fork engine 2df76790b4; no native rebuild,
installed UI or release update. Production editor, external reference handling,
where-used and failed recompute policy remain pending under 10.8.

Previous roadmap batch: 10.8e/f named angular parameters and native property rename.
Test-only angle assignment rejects incompatible or missing expressions before mutation;
native rename updates two consumers through Undo/Redo and save/reopen.
Grouped architecture validation: 52 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-angle-rename-20260930-verified.
Macro PASS; process ended. Existing fork engine 2df76790b4; no native rebuild,
installed UI changes or release update. Parameter editor, where-used, collision and
cross-document rename policies remain pending under 10.8.

Previous roadmap batch: 4.1.10/5.1.10 secondary task cleanup errors handled.
Independent cleanup continues and preserves the primary constructor/display error;
repeated annotation removal is harmless. Both feature retry checks pass.
Grouped model/GUI validation: 54 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-cleanup-errors-20260930-batch.
Macro PASS; process ended. Shared FeatureTask and both GUI test modules staged with
matching hashes. No native rebuild, release update or physical viewport acceptance.
Native cleanup/transaction failure coverage remains bounded to the tested faults.

Previous roadmap batch: 4.1.9/5.1.9 production transaction ownership guards complete.
Existing-feature editing rejects unrelated pending transactions; scoped command
creation still hands its own transaction to the task. Caller edit/abort/retry passes.
Grouped model/GUI validation: 52 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-ownership-20260930-batch.
Macro PASS; process ended. FeatureTask and two test modules staged with matching
hashes. No native rebuild, release update or physical viewport acceptance.

Previous roadmap batch: 4.1.8/5.1.8 production task cleanup complete for tested faults.
Initial-preview construction failure and dialog-display failure clean resources,
restore visibility and roll back owned edit transactions; reopen/accept succeeds.
Grouped model/GUI validation: 50 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-cleanup-20260930-verified.
Macro PASS; process ended. Three Python modules and two tests staged with matching
hashes. No native rebuild or release. Arbitrary allocation/cleanup faults and
physical viewport/high-DPI acceptance remain separate gates.

Previous roadmap batch: 4.1.7/5.1.7 production command startup rollback complete.
Shared creation transaction guard aborts factory failure/editor refusal; successful
startup leaves the transaction to the task. Retry passes for both commands.
Grouped model/GUI validation: 48 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-startup-20260930-batch.
Macro PASS; process ended. Three Python modules and two tests staged with matching
hashes; final formatting-only differences verified. No native rebuild or release.
Partial task construction/observer cleanup remains a separate failure-handling gap.

Previous roadmap batch: 4.1.6/5.1.6 production preselection filtering complete.
Stale Trim target/tool and Isocline face candidates are skipped; valid selections
remain and repaired inputs can be picked in the open task and accepted.
Grouped model/GUI validation: 46 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-preselection-20260930-batch.
Macro PASS; process ended. Two Python modules and two tests staged with matching
hashes. No native rebuild, release update or physical viewport acceptance.

Previous roadmap batch: 4.1.5/5.1.5 production input-selection guards complete.
Trim Target/Tool and Isocline Faces/Reference reject stale picks before changing
inputs, retaining selection mode. Repair/recompute allows selection and acceptance.
Grouped model/GUI validation: 44 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-selection-20260930-batch.
Macro PASS; process ended. Two Python modules and two test suites staged with
matching hashes. No native rebuild, release or physical viewport acceptance.

Previous roadmap batch: 4.1.4/5.1.4 production task-readiness guards complete.
Trim Body/Isocline preview and acceptance reject invalid/touched dependency results
after recompute, hide the result and remain editable; source repair recovers.
Grouped model/GUI validation: 42 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-readiness-20260930-batch.
Macro PASS; process ended. Three production Python modules plus two tests staged
with matching source hashes in the isolated build. No native rebuild or release.
This integrates readiness into these task panes only; exporters and other consumers
remain separate gates, as do physical viewport/high-DPI acceptance checks.

Previous roadmap batch: 11.7w/x complete as test-only current-result access checks.
Native downstream solid remains cached after reference failure, but the new accessor
rejects invalid/touched dependencies. Repair/restore recover access; recompute is
explicit and returned shapes are independent copies.
Grouped validation: 50 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reference-consumers-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Application exporters/GUI/other consumers do not yet use this test-only accessor.

Previous roadmap batch: 11.7u/v complete as test-only planar reference repair checks.
Missing face clears adapter output and rejects preview; face repair Undo/Redo and
restore pass. Deleted-source replacement needs explicit sketch face reselection;
obsolete placement dependencies clear and later source motion follows correctly.
Grouped validation: 48 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reference-repair-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production repair UI, ambiguous topology and downstream cached-result/export safety
remain pending. Adapter fixtures need the prototype module to recompute.

Previous roadmap batch: 11.7s/t complete as test-only atomic reference creation.
One transaction creates the local reference and reattaches; Undo removes it and
restores the original attachment, with Redo/restore passing. Injected late failure
rolls back objects, placement and transaction state; subsequent success passes.
Grouped validation: 46 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-atomic-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production UI/task transaction integration and source/consumer failure handling
remain pending. Adapter fixtures require the test-only Python module on restore.

Previous roadmap batch: 11.7q/r complete as test-only cross-part planar reference.
Native binder probes failed alignment/motion criteria; explicit PlanarSupport uses
existing ShapeReferences conversion/dependency helpers and passes alignment, both
preview policies, source motion, Undo/Redo and restore. Grouped validation: 44 passes,
zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-adapter-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Saved fixtures require SketchReattachment.py for proxy recompute. Production adapter
creation/deployment and missing-source consumer handling remain pending.

Previous roadmap batch: 11.7o/p complete as test-only support scope guards.
Cross-container placement probe found preview/native mismatch; different geometry
containers now reject before mutation. App::Link supports also reject pending an
explicit occurrence-edit policy. Grouped validation: 42 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-scope-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Cross-part reference adapters, occurrence policy and production UI remain pending.

Previous roadmap batch: 11.7m/n complete as test-only reversal/expression checks.
MapReversed preview/commit/restore passes. Preserve-world rejects expression-driven
offsets before mutation; preserve-local retains the named length expression through
restore and parameter edits. Grouped validation: 40 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-expressions-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production UI, support-dependent expressions and external projections remain open.

Previous roadmap batch: 11.7k/l complete as test-only isolated placement preview.
Disposable-document attachment evaluation replaces live rollback. Both policies
retain candidate/commit parity, leave original object/recompute notifications empty,
clean up the temporary document and preserve an already-populated redo stack.
Grouped validation: 38 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-isolation-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Application observers can see temporary-document lifecycle; full sketch/consumer
evaluation and production graphical preview remain pending. See roadmap 11.7.

Previous roadmap batch: 11.7i/j complete as test-only rollback preview probes.
Both policies return placements matching committed operations and restore support,
offset and downstream position. Repeated/rejected previews preserve an existing
committed edit's Undo/Redo. Grouped validation: 36 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-preview-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Trial recompute is observable; production preview isolation/UI and preservation of
pre-existing redo history remain pending. See roadmap 11.7 and ADR 001.

Previous roadmap batch: 11.7g/h complete as test-only support validation.
Derived native extrusion support rejects before introducing a cycle; touched and
failed supports reject before mutation. Repaired support accepts reattachment and
Undo restores the original support/placement.
Grouped validation: 34 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-support-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production UI and broader topology/consumer failure handling remain pending.

Previous roadmap batch: 11.7e/f complete as test-only recovery/transaction prototypes.
Explicit preserve-local repair of a missing face survives Undo/Redo and restore;
preserve-world rejects invalid placement. Caller-owned transactions reject before
mutation and retain their pending edits/abort behavior.
Grouped validation: 32 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-recovery-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production repair UI, ambiguous/deleted support recovery, transaction integration
and consumer stale-result policy remain pending; see roadmap 11.7 and ADR 001.

Previous roadmap batch: 11.7c/d complete as test-only placement-policy prototypes.
Preserve-local retains the full attachment offset across rotated supports;
preserve-world solves a compensating offset with unchanged sketch parent. Rotated
parent, Undo/Redo, restore and subsequent associative support motion pass.
Grouped validation: 30 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-policies-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production editor/preview, selected-occurrence placement, lost-support repair and
transaction integration remain pending. See roadmap 11.7 and ADR 001.

Previous roadmap batch: 11.7a/b complete as bounded test-only reattachment prototypes.
Two parallel planar supports preserve sketch offset and downstream result identity
through Undo/Redo and save/reopen. Missing/curved faces reject before mutation.
Grouped validation: 28 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\sketch-reattachment-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production editor, preserve-world policy, rotated reattachment and lost-support
repair remain pending; see roadmap 11.7 and ADR 001 for the prototype boundary.

Previous roadmap batch: 10.8c/d complete as bounded foundation proofs. Explicit native
parameter references remain independent across parts with matching labels; native
object-level reverse dependencies survive save/reopen. A unit-correct zero length
invalidates geometry; abort restores the valid model and later edits Undo/Redo.
Grouped architecture validation: 26 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-dependencies-20260930-batch.
Macro PASS; process ended. Test-only changes; no native rebuild or release update.
Property-level where-used, production scope resolution and parameter editor remain
pending. These checks do not implement automatic invalid-edit rollback in the UI.

Previous roadmap batch: 10.8a/b complete as bounded foundation proofs. Native named
length parameters drive two features with inch/mm conversion, label edits,
Undo/Redo and save/reopen; occurrence placement remains independent. Native angle-
to-length coercion exposed by the initial test requires a production boundary.
Test-only NamedParameters.py enforces length-valued expressions; native cycle
rejection and abort recovery pass. Final grouped architecture run: 24 passes,
zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\named-parameters-20260930-verified.
No application module installed, native rebuild or release update. Parameter editor,
property renaming, scope/publication and full T13 remain pending. Process ended.

Previous roadmap batch: 16.2ao/ap complete. Z Correction preserves parsed probe
precision and rejects conflicting heights at identical XY positions; identical
samples are deduplicated. Native precision, order-independent rejection/export
blocking and recovery pass. Grouped validation: 65 passes, zero failures/errors/
skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-probe-precision-20260930-batch.
Source/module hash and precision limits recorded in roadmap. Python-only update;
no native rebuild, GUI/machine acceptance or release. Test process ended.

Previous roadmap batch: 16.2am/an complete. Shared property inheritance rejects
cycles without recursion; job operation traversal is iterative, ordered and unique.
Native shared-base invalidation/recovery and deep/cyclic fixtures pass. Grouped
validation: 151 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-traversal-20260930-batch.
Source/module hashes and cycle policy recorded in roadmap. Python-only
synchronization; no native rebuild, schema migration, GUI/machine acceptance or
release update. Test process ended; broader consumer gates remain open.

Previous roadmap batch: 16.2ak/al complete. Shared dressup lookup recognizes current
proxies independently of internal names, keeps guarded legacy fallback, stops at
ordinary operations and handles deep/cyclic/disconnected chains. Native custom-name
nested and restored fixtures pass. Grouped validation: 84 passes, zero failures/
errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-dressup-lookup-20260930-batch.
Hash and compatibility limits recorded in roadmap. Python-only synchronization;
no native rebuild, schema migration, GUI/machine acceptance or release update.
Test process ended. Broader consumer gates remain open.

Previous roadmap batch: 16.2ai/aj complete. Plunge Milling clears cached output
before generation and marks invalid stepover as a native error. Final grouped run:
54 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-20260930-verified.
Initial fixture name correction and module hash recorded in roadmap. Next bounded
candidate: 16.2ak, audit shared dressup base lookup's internal-name dependence with
legacy/nested/ordinary-operation tests before changing recognition. Python-only
synchronization; no native rebuild, GUI/machine acceptance or release update.
Test process ended; broader consumer gates remain open.

Previous roadmap batch: 16.2ag/ah complete. Dragknife and Ramp Entry clear output
before input validation/generation. Missing/empty Dragknife input and native
failure/export rejection/recovery pass. Final grouped validation: 52 passes,
zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-dragknife-ramp-20260930-verified.
Initial zero-feed fixture correction and source/module hashes recorded in roadmap.
Python-only synchronization; no native rebuild, GUI/machine acceptance or release
update. Test process ended. Broader consumer gates remain open.

Previous roadmap batch: 16.2ad/ae/af complete. Z Correction rejects non-finite probe
coordinates and non-positive/non-finite interpolation settings, and uses the correct
source-line subdivision point count. Grouped validation: 51 passes, zero failures/
errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-zcorrect-numeric-20260930-batch.
Source/development-module hash and spacing limitation recorded in roadmap.
Python-only synchronization; no native rebuild, GUI/machine acceptance or release
update. Test process ended. Continue related consumer gates with grouped validation.

Previous roadmap batch: 16.2aa/ab/ac complete. Z Correction clears stale results,
rejects unusable specified probe files and blocks uncorrected fallback outside the
probe area. Empty filename deliberately retains placed-base passthrough. Grouped
validation: 48 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-zcorrect-20260930-batch.
Native constant-offset grid, failure/export rejection and recovery pass. Hash and
external-file recompute limitation recorded in roadmap. Python-only synchronization;
no native rebuild, GUI/machine acceptance or release update. Test process ended.

Previous roadmap batch: 16.2x/y/z complete. Axis Map clears failed conversion output
and requires positive finite radius. Rotary-post snapshot tests now recompute and
validate inputs before restoring their prepared output; production export guard
unchanged. Final grouped validation: 44 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-axis-map-20260930-final.
Earlier fixture failures and final hashes are recorded in the roadmap. Python-only
synchronization; no native rebuild, GUI/machine acceptance or release update.
Test process ended. Continue broader consumer gates with grouped validation.

Previous roadmap batch: 16.2u/v/w complete. Mirror preserves placement when disabled,
clears stale output before generation, publishes only completed combined results,
and copies live base paths before transformation/append. The identity-placement
source mutation found in the initial run is fixed. Final grouped validation:
53 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-mirror-20260930-verified.
Source/development-module hash recorded in roadmap. Python-only synchronization;
no native rebuild, GUI/machine acceptance or release update. Test process ended.
Continue broader consumer compatibility gates with grouped validation.

Previous roadmap batch: 16.2s/t complete. Array clears paths before input validation/
generation; Dogbone clears paths and corner caches before generation. Grouped
validation: 49 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-array-dogbone-20260930-verified.
Initial empty-source fixture exposed skipped downstream native execution; corrected
coverage verifies export rejection before explicit empty-input cleanup. Eager cache
invalidation of skipped consumers remains open. Python-only synchronization, no
native rebuild or GUI/machine/release acceptance. Validation process ended.

Previous roadmap batch: 16.2q/r complete. Missing/non-geometric Boundary stock
now causes native error/export rejection; offset outputs are checked before clipping.
Grouped run: 46 passes, zero failures/errors/skips, in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-boundary-inputs-20260930-batch.
Python synchronized to the existing development build, hash recorded in roadmap.
Test process ended. No native rebuild, GUI/machine acceptance or release update.
Continue broader consumer compatibility tasks in coherent groups.

Previous roadmap batch: 16.2o/p complete. Boundary clears cached output before
clipping/offset work, rejects empty boundary geometry in both modes, and returns
an empty native Path for missing base input. Four new failure/recovery checks and
related suites pass: 44 tests, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-boundary-20260930-batch.
Python synchronized to the existing development build; source/installed hash is
recorded in the roadmap. No native rebuild, GUI/machine acceptance or release.
Validation process ended. Continue broader consumer gates in coherent groups.

Previous roadmap batch: 16.2l/m/n complete. Empty Lead-in/Lead-out and Boundary inputs
now stop cleanly; lead generation clears stale paths before possible exceptions;
disabled leads return the placed base path directly. cam-leads-20260929-verified
records 40 passes, two existing linking skips, zero failures/errors. Missing-model
nested fixture now stays empty without invalid dressup objects and recovers.
Python-only synchronization, no native rebuild or GUI/machine acceptance. Broader
consumer/dressup failure gates remain open; continue related grouped validation.

Previous roadmap batch: 16.2j/k complete. Job.Model changes now rebind/clear nested
base operations and dressup paths using allOperations. Native fixture removal and
replacement/recovery checks pass, including restored export. cam-nested-20260929-batch
records 90 passes, one existing skip, zero test failures/errors. Python-only install.
Missing-model recompute reports Lead-in/Lead-out NoneType.Group diagnostics while
keeping paths empty; recovery passes. That diagnostic and broader consumer gates
remain open. No native build or GUI/machine acceptance in this batch.

Previous roadmap batch: 16.2h/i complete. Shared PostList refuses dirty/invalid native
operations and linked inputs before cached-path export. Dirty and failed-producer
recovery checks pass; nested dressup export tests now recompute edited inputs first.
cam-export-20260929-verified under the existing validation root records 88 passes,
one pre-existing skip, zero failures/errors (overall macro flag false for any skip).
PostList.py source/installed SHA256:
0C70E6249CF1AEF5BD346CE89B2CB507F750E7F97BD2A07EE702A258B7B2E078.
No native build; GUI/machine acceptance and broader semantic/export gates remain open.

Previous roadmap batch: 16.2f/g complete. Job.Model replacement/removal rebinds
operation dependencies and clears unfrozen paths; normal recompute recovers them.
Restored the full execute wait-cursor decorator displaced by the previous change.
75 distinct checks pass across cam-container-20260929-batch (67 broader passing)
and cam-container-20260929-corrected (eight targeted passing after fixture repair).
Both evidence folders are under D:\Temp\Office-PC\freecad-plus-validation-20260928.
Only Python modules synchronized; no native rebuild or GUI/machine acceptance.
Next: failed-producer, nested-operation and export gates; retain grouped validation.

Previous roadmap batch: 16.2d/e complete. Production CAM Base.py binds hidden native
ModelDependencies links on execution and restore; normal document recompute now
propagates source edits and empty-source recovery in the SurfaceScan fixture.
72 grouped checks pass in cam-dependencies-20260929-final. Installed/source SHA256:
8F38E250CD73C0B1BF8754BF64CA4879BF509D35C40620520212F780A8ECCC4C.
No native build or test process remains. Current Operations container is a plain
group, not an aggregate Path cache. Export guards, skipped failed producers, replaced
Model containers and broader reference/consumer graphs remain open. Next: targeted
remaining downstream gates; batch related changes before any expensive build.

Earlier roadmap batch: 16.2b/c complete. Production CAM Path/Op/Base.py clears
old Path before validation can return for missing model or tool controller, after
the existing frozen-job guard. Both defects retained 43 commands before correction;
69 grouped checks pass in cam-invalid-inputs-20260929-verified. Installed Python
module matches source SHA256 FE5A146430588CD2B3E5660B2CD9B16B67E6A57EEB12AFD3F5DA079B9BB3227D.
No native build or test process remains. Automatic dependency scheduling, aggregate
job/export invalidation and general failed-source behavior remain open. Continue
related downstream consumer work; do not equate these execution tests with those gates.

Earlier roadmap batch: 12.1a/12.2a complete. Mixed native definitions and a bounded
Make Unique helper pass in a 32-check grouped run, mixed-unique-20260929-final under
the existing external validation root. Native recursive copy remaps sketch links;
new metadata identities/provenance, selected-link reassignment and placement are
transactional. Undo/Redo, shared versus independent edits, restore and no-mutation
rejection pass. No installed module/native build and no test process remains.
Next: missing/ambiguous drawing references, CAM path/FEM consumers, complex/external
identity and production architecture. Keep the full 12.1/12.2 gates open.

Earlier roadmap batch: 7.1.3g/h complete; 29 grouped checks pass in
lineage-20260929-topology under the existing external validation root. New test-only
ResultLineage.py implements planar side roles and explicit-primary/new-ID merges.
Expected producer errors initially left stale downstream geometry; status/empty-output
propagation fixes the bounded prototype chain. No installed module or native build.
No test process remains. General lineage, native error/UI integration and broader
consumer safety remain open. Next: mixed definitions, reference repair, CAM paths/FEM
and production architecture decisions. Roadmap and ADR 001 retain evidence/limits.

Earlier roadmap batch: 7.1.3f and 16.2a complete; 24 grouped checks pass in
attachment-drawing-20260929-final under the existing external validation root.
Independent FlatFace attachment on a rotated plane propagates support movement;
TechDraw projected radius follows source edits, Undo/Redo and save/reopen.
Only tests and documentation changed; no installed source or native rebuild.
The initial drawing fixture needed TechDraw Edge0, not Edge1. No test process
remains. Next: semantic split/merge lineage, missing/ambiguous drawing references,
CAM generated-path and FEM consumers. Keep parent architecture/consumer gates open.
Evidence, fixture limits and module hashes are linked from the roadmap and ADR 001.

Earlier roadmap batch: 10.1 and 10.3a/b complete. Product/UI/guideline contracts
now match version 2; ADR 002 defines transient suggestions versus saved intent.
Test-only OperationIntent.py supports bounded single-part solid proposals and
committed operations with explicit native links. All 22 grouped checks pass in
operation-intent-20260929-final under the existing external validation root.
No application module installed, native build or GUI acceptance. No test process
remains. Next: Phase 7 lineage/consumers, production target discovery/access scope,
scale-aware contact behavior and real task preview lifecycle. Keep 10.3 open.
See roadmap/ADR 002 for evidence and limits; batch related work before builds.

Earlier roadmap batch (2026-09-29): 7.1.3c/7.1.3d/7.1.3e complete. Test-only
history adapters now handle tilted profiles and cross-part placement dependencies;
a native assembly-local cut preserves the shared definition and other occurrence.
Production Draft clones clear stale Shape when all sources become empty or the
source list is cleared. Native CAM job-model clones clear/restore geometry too;
generated-path invalidation is not established. All 88 grouped history, Draft
modification, PlanarSurface and STL/tab tests pass without failures/errors/skips
in `part-consumers-20260929-final/results.json` under the existing external build
root. Fifteen focused checks also passed after reproducing three defects.
Python clone module installed in the existing fork; no native build. Matching
source/installed SHA256: 6291E8A30ED3C4321833182412A6D8AC86C642CFF035A605F9FFD29327DF19A9.
The evidence manifest records adapter/module/test hashes. No test process remains.
Next: semantic lineage, actual attachments and remaining TechDraw/CAM-path/FEM
consumer gates. FEM is disabled in this build; batch future native build work.
History production architecture and cadprt schema remain undecided/unimplemented.

Earlier roadmap batch (2026-09-29): 7.1.3a/7.1.3b adapter prototypes and 7.1.6a
decision boundary complete. Eight native capability/adapter tests pass together
in `part-adapters-20260929-final`. Implementation is test-only under
tests/prototypes; no application code, installation or native build changed.
Probes cover Body binders sharing a sketch and explicit result roles/identities,
placement, dependencies, unavailable/reappearing results, transactions and restore.
See architecture/ADR_001_HISTORY_ADAPTER_BOUNDARY.md for limits. Next: transformed
attachments/occurrences, assembly-local edits and downstream consumers before
final architecture choice. Prototype FCStd files require the test module for
result-layer recompute; they are not cadprt files or released functionality.
No test process remains running; continue batching related tasks before builds.

Current roadmap batch (2026-09-29): logical contracts/mapping for 7.1.1, 7.1.2
and 7.1.4 are complete in architecture/PART_HISTORY_CONTRACT.md. Four grouped
native probes pass in `part-history-20260929-final`, covering independent/shared
sketches, multiple results, links, transactions and FCStd persistence. No production
application code changed and no build was needed. The saved native example is
disposable evidence, not the future cadprt format or a new history implementation.
Next: actual adapter comparison 7.1.3 and architecture decisions 7.1.5/7.1.6.
The owner requests groups of two or three tasks before costly build/test work.
No test process remains running. Earlier CAM evidence below remains valid.

Latest implementation (2026-09-29): U.23 corrects the reproduced modern #26300
freeform cutting-boundary stall. B-spline/Bezier selections now use tolerance-based
tessellation and NonZero polygon union; failure cannot drop selected faces.
All 91 CAM checks pass in `freeform-boundary-20260929-final`, including the
original fixture: 14.05 seconds generation versus the baseline 120-second timeout,
4,475 commands and 4,118 cutting endpoints inside the mask. Python-only update
installed, no rebuild. Module hash and limits are recorded in U.23.
U.15 native cancellation and U.14 exact GeomFillSurface acceptance remain pending;
legacy Surface and machine/post acceptance are not claimed. No test process remains.

Latest implementation (2026-09-29): U.22 rejects the modern CAM avoidance
fallback that silently filled selected holes when projection failed. The error
clears the stale operation path. Successful primary projection and outer-only
cutting fallback remain covered. All 81 CAM checks pass in one batch at
`avoidance-fallback-20260929-final`; Python-only update synchronized, no build.
Final module hash is in U.22. Avoidance inputs requiring this lossy fallback now
stop explicitly; a replacement projection algorithm remains future work.
#26300 and exact GeomFillSurface acceptance remain open. No test process remains.

Latest implementation (2026-09-29): U.16/U.21 fix #6864 in the replacement
Line/ZigZag generator. One targeted source compile/module relink completed; all
77 CAM checks pass in one batch, including final-strip geometry, avoidance and
STL/tab workflows. No full application build. Module/test hashes and evidence
are in U.21. The existing test application now contains this correction.
Next unresolved high-impact case remains U.15 (#26300); exact GeomFillSurface U.14
needs a relevant build with Surface enabled. No process remains running.

Earlier implementation (2026-09-29): U.20 fixes partial boundary loss in the modern
CAM pipeline. Failed isolated/group projections and boundary unions now stop
instead of dropping selected cutting/avoidance regions; stale paths are cleared.
Fourteen focused and 59 related checks pass across separate runs. Python-only
update is installed and hash-verified; no native rebuild or process remains active.
Evidence and installed module hash are recorded in U.20. The confirmed freeform
slowdown below remains open; no unsuccessful projection experiment was restored.

Earlier diagnosis (2026-09-29): U.19 reproduces #26300 in PlanarSurface.
The original saved freeform geometry with nine selected faces exceeds 120 seconds;
20/40-second stacks locate Path.Area boundary projection, before cutting generation.
Per-face/paired-face projection experiments were unsuccessful and fully removed.
Source-built app is restored to committed code (line endings normalized; module
hash is recorded in U.19). No native rebuild or application fix is claimed.
The opt-in TestIssue26300Fixture.py and bounded RunIssue26300.ps1 preserve the case.
Next: resolve U.15 with validated projection/coverage semantics; U.16 final-strip
coverage remains independent pending work. Exact GeomFillSurface testing U.14
still awaits a relevant batched build with Surface enabled. Prior ten-test curved
avoidance evidence remains valid. No test/build process remains running.

Latest CAM issue milestone (2026-09-29): two Python modules updated in the existing
app to stop generation when selected face-avoidance boundaries fail and to reject
strategy switches that would ignore those exclusions. Eight focused checks and
59 related CAM regressions pass (67 total, no skips). No native rebuild. See
U.12-U.17 in the roadmap for evidence and the remaining #27751 child cases:
curved external avoidance, freeform hang/crash, and final-strip line coverage.
Legacy Surface/Waterline and saved MillFace paths were not migrated. No test or
build process remains running.
CAM avoidance milestone `b2cfdf0f114ff2cba48004fe538991395b22f525` is committed
and pushed to `origin/main`; remote hash verified. No release was made.

Issue batch completed (2026-09-29): the local application now contains the Mirror
#32706 correction. A targeted compile of FeatureMirroring.cpp and Part relink
both exited 0; no full rebuild was needed. All 75 issue tests pass, including
Mirror save/reopen/recompute and translated/rotated face selection through the
real task pane. Three changed test scripts were synchronized and hash-verified.
See [issue work](DEVELOPMENT_ROADMAP.md#upstream-issue-work) for binary hashes and
exact evidence directories, and [procedures](../tests/UpstreamIssues.md) to rerun.
No build/test process remains running. The executable is the existing external
`build/bin/FreeCAD.exe`; its Part module has changed, not its historical version string.
Validation checkpoint `bb6d7607a78080bec36f8ade30c8925f09201874` is committed and
pushed to `origin/main`; remote hash verified.

The earlier five startup-recovery fixtures also passed; recovery, numeric input,
Extrude and tree fixes were inherited and not duplicated. #29376 still needs a
reproducible affected session/GPU trace. Legacy MillFace is superseded for new
workflow tasks, while saved legacy operations retain the documented risk.
The broader upstream CAM refactor epic is not declared complete. No release.

Earlier source checkpoints: Mirror/triage `85fd6ebc77`, then regression milestone
`24815217c9`, both pushed to origin/main. Their earlier notes about an unbuilt
Mirror correction are superseded by this completed build checkpoint.

CAM implementation and automated validation are complete. Direct STL
Parallel/Waterline, stock bridges and separate manually indexed setups are in the
source-built application. No build or automated test is still running.
Source milestone `648cff214ca78e1d8b3d72d87d6053e103390c60` is committed and
pushed to `origin/main`; the remote branch hash was verified. No release was made.

Indexed setups use one associative transform for model, stock and shared tabs;
each setup has its own work origin and separately generated/posted three-axis
paths. No automatic rotary motion is generated. Native viewport acceptance,
representative simulation and per-setup postprocessor review remain open.
The NX-style roadmap planning request is committed and pushed as Phases 7-9
(`4c9d7ed598`); no history architecture implementation has been started.
The concise upstream issue watchlist is in `FREECAD_ISSUES.md`, committed and
pushed initially as `bbcf78cffb`; the later issue pass now records applicability
and the reproduced Mirror defect, separately from inherited fixes.

Current CAM evidence under the external root below:

- `cam-completion-build-result.json`: full configured build exited 0;
  `cam-final-scripts.log`: final script/test targets also exited 0.
- `cam-tests-20260929-184049`: all 22 focused tests passed, no skips, process 0.
- `cam-tests-20260929-183855`: related suites had 112 passes, no failures/errors,
  one optional simplification test skipped for unavailable `fast_simplification`.
  Strict aggregate FAIL records that skip; do not report all tests as passing.
- `cam-validation-manifest.json`: 15 installed CAM Python files match source,
  with five native binary hashes. Runtime retains the historical native version
  stamp `8abce719de`; use file hashes and Git history to identify new CAM code.
- The [Phase 6 roadmap](DEVELOPMENT_ROADMAP.md#cam-mesh-machining) separates
  completed automated work from the remaining manual gates.

The previous shutdown handoff below records completed Part/Part Design evidence.
It predates the CAM changes. Do not mark CAM tests or native acceptance complete
based on the earlier 149-test result.

## Earlier Part/Part Design validation

- Native feature source: `8abce719de38a1b1ad255d0e7f4554a9d44e9c71`.
- Configured Windows x64 Release ALL_BUILD succeeded. First bounded pass timed out;
  resumed incremental build finished with exit 0. No application source fix needed.
- All 149 model/task tests passed at both scale factors 1 and 1.5, with no failures,
  errors or skips and both processes exiting 0. Actual device-pixel ratios: 1.5 and
  2.25, respectively. These are automated checks, not physical/visual acceptance.
- Nine binary hashes recorded; all 80 checked installed workflow/test Python files
  match the checkout. Added `tests/ValidateWorkflows.FCMacro` for repeatable testing.
- Roadmap milestone 2.2.4 is complete. Remaining manual gates are listed under
  [consolidated validation](DEVELOPMENT_ROADMAP.md#consolidated-validation).

## Earlier build and evidence

External root: `D:\Temp\Office-PC\freecad-plus-validation-20260928`.
Launch: `build\bin\FreeCAD.exe` beneath that root. It reports FreeCAD 26.3.0dev,
revision 49009 and source hash `8abce719de`. This is the focused development build;
disabled unrelated workbenches, installer packaging and upstream compatibility
testing are not included. Ignore the separately installed FreeCAD.

Evidence: `closeout-build-resume-results.json`, `closeout-build-manifest.json`,
`closeout-regressions/results.json`, `closeout-highdpi/results.json`, and their logs.
The two latter folders have isolated settings and successful process reports.

## Next CAM acceptance work

Follow `tests/CAMMeshMachining.md` for physical STL selection/placement, both
strategies, tab picking/editing, and indexed-frame interaction. Review material
removal and each setup's posted output. Keep the optional simplification skip
visible until its dependency is available and that inherited test can run.
No CNC machine motion or physical cutting has been performed.

## Earlier Part/Part Design acceptance handoff

1. Launch the development application for visible native testing with isolated
   preferences. Avoid `--hidden` for the interactive fixture: its startup/close
   behavior led to an Unsaved Document prompt rather than a ready test workspace.
2. Use the existing `tests/PadTaskPanel.md`, `PatternTaskPanel.md`,
   `RevolveTaskPanel.md`, `TrimBody.md`, and `IsoclineCurve.md` acceptance procedures.
   Start with 2.2.3: real viewport/tree picking on rotated profiles, keyboard input,
   direction/preview behavior, Cancel, visibility and Undo/Redo, including Pocket.
3. Record only checks actually completed. Close 2.2 and related feature gates only
   when their required interaction/visual evidence exists.

Native tool state: computer-use skill was initialized through `@oai/sky` in the
node REPL. User granted window testing, but graphics capture timed out. Accessibility
inspection found the fixture's save prompt. The user then pressed physical Escape,
stopping Computer Use, and subsequently requested shutdown. No further native input
was issued. Do not reuse old window handles, element indexes or screenshot state.
No native acceptance check was completed or marked passed.

Only task-created test documents were opened. Fixture files `Closeout-*.FCStd` and
`closeout-interactive.FCMacro` are in the external evidence root. No user design was
edited. Changes are local; no push, release or publication was made.
