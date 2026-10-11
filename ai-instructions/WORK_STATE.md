# FreeCAD Plus: Current work state

## Authorized objective and stopping boundary

The owner clarified that Point to Point is an operation, not Component Panel work.
A right-click entry provides access but does not bring the operation into Group 1.
Next actual panel increment is **G1.7a Part Type and visibility state**, not started.
No additional runtime verification is required for this scope correction.

## Scope correction and parked operation — October 10, 2026

Point to Point implementation began after the owner allowed necessary new work,
but was stopped when the owner corrected its classification. Its unfinished source
and five proposed regression cases are preserved on local branch
`codex/point-to-point-parked`, commit `288f99e69c`; the branch was not pushed.
Python parsing and the script-copy target passed. **No runtime tests ran** and
no functional acceptance is claimed. The baseline checkout retains the previously
validated Translate/Rotate implementation. The development payload's twenty-two
scripts were restored byte-for-byte from that baseline and the new test copy removed;
no owner package, settings or shortcut was changed. Future CMake builds must use
the active branch's source configuration, as usual.

Group 1 owns panel/document structure and menu integration. Task-operation behavior
is tracked separately even where launched by that menu; its completion is not a
Group 1 gate. The roadmap preserves historical operation IDs/evidence without using
them as the next panel queue. For subsequent increments, run only relevant acceptance
checks once; repeat only in response to a failure, a fix or a material new concern.

## G1.6c4 Rotate — October 10, 2026

**Implementation:** the existing native task supports located parent/picked/two-point
axes, an optional picked pivot, native angular magnitude and Reverse. Both positions
and orientations change through one parent-frame rigid transform. Point references
include vertices/points, origins and circular-edge centers; references remain snapshots.
The view-only preview includes an axis arrow/pivot marker and corresponding shared
occurrences. Translate now uses the same placement-transform path. Existing atomic
source-owned Apply, Undo, reset, Persistent Selection, OK/Cancel and lifecycle guards
are reused. No modeling feature, joint, definition copy or persistence schema is added.

**Build:** FreeCADPlusScripts passed in the retained G1.6b native development tree.
Only the script payload changed; no native rebuild or owner/shortcut delivery.

**Validation:** **12/12 focused Translate/Rotate cases** passed (24.327 seconds),
then **62/62 combined Group 1 cases** passed (98.016 seconds). Both runs had zero
failures/errors/skips and normal native application exit. Coverage includes non-origin
pivots, located axes under rotated shared parents, two-point/reversed axes, circle
centers/origins, snapshot stability, rigid relative placement, nonaccumulating preview,
method switching, invalid angles, atomic rollback, full-turn no-op and Undo/Redo.

An independent process retained exact native IDs, rotated positions/orientations and
unchanged feature geometry. External source rotation survived standalone and assembly
reopen; source-only save left the assembly checksum unchanged. Inspected normal
framebuffer captures show clean shared previews with a located cyan axis arrow,
Cancel restoring original geometry without ghosts/axis overlay, and committed rigid
rotation matching the preview. Native task and Part Tree captures show the intended
controls, units and shared hierarchy. Camera, document identities and Undo state were
checked across preview/Cancel/Apply. The initial capture harness assumed an active
MDI subwindow while Tasks had focus; selecting the subwindow owning the model view
resolved that capture-only failure. The independent persistence verifier had already
passed and was not repeated. No renderer or owner-setting changes were made.

**Packaging/checks:** all twenty-two Python source/test scripts parse and match the
copied native development payload. All 117 checked local Markdown file targets
resolve; diff whitespace passed. Complete Group 1, remaining Move methods, original
workbench and long-session responsiveness acceptance remain unfinished. The bounded
development payload's known unavailable Std_Measure warning remains a limitation.
No further feature implementation or runtime tests followed planned acceptance.

**Cleanup:** task-only profiles, fixtures, captures and logs were removed from
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6c_rotate`
after recording results. Useful native build/dependencies and tracked tests remain.

**Publication:** source milestone `b14a8bc724` pushed to
`origin/codex/freecad-1.1.4-baseline`; remote revision verified. No owner-build
delivery, desktop shortcut change, release or deployment.

## G1.6c3 Move Components foundation and Translate — October 10, 2026

**Implementation:** the Part Tree action opens native Tasks. Whole sibling instances
move in their immediate parent's coordinates; shared/external parents own changes
in their defining file. Translate uses parent axes or a snapshot of a visible straight
reference, one nonnegative unit-aware length and Reverse. A temporary, unpickable
wire outline previews corresponding shared occurrences without document mutations.
Apply is one atomic Undo group; no-op, reset, Persistent Selection, Cancel after
Apply and OK behavior follow the confirmed workflow. Other workflow entries explain
that they await later implementation. No definitions/geometry/schema are copied.
The technical contract is in ARCHITECTURE, owner behavior in TASK_PANEL.

**Build:** existing G1.6b native development tree; FreeCADPlusScripts passed. Script
changes only, no native rebuild, owner package or desktop shortcut change.

**Validation:** **56/56 combined Group 1 cases** passed, zero failures/errors/skips,
normal application exit (79.406 seconds). After final preview-visibility and component
label corrections, the affected six movement cases passed again (14.677 seconds,
zero failures/errors/skips). Native context-menu entry and the Tasks Apply button,
preview without document mutations, rigid sibling movement, rotated/shared parents,
reverse, no-op, Apply/OK/Cancel, selection retention/removal and atomic Undo/Redo are
covered. Picked lines and infinite origin axes convert to parent coordinates; curved
or hidden references and invalid lengths are refused. Expression/read-only guards,
late-failure rollback, panel/file/Edit-context cleanup and external source ownership
also passed. Scaled frames remain explicitly unsupported; other Move methods and
complete Group 1/workbench/long-session responsiveness acceptance remain unfinished.

The independent fresh process retained exact native IDs, domestic placements and
external-source placements when opened both independently and through the assembly.
A further source-only save left the assembly archive checksum unchanged; a second
reopen retained that movement. Inspected viewport captures show temporary cyan wire
previews for shared children in differently rotated parents, restored original
placements after Cancel, and corresponding committed movement after Apply. Part Tree
shows the shared parent Edit state and the exact selected child; Tasks shows the
component's qualified model label, controls and unit-aware distance. Camera orientation
and document identities were retained. No owner settings or renderer changes were made.

Initial failures led to corrections for native form ownership, file-root context,
InputField rawValue/signals, Delete ShortcutOverride and qualified expression paths.
The first combined run had one old clipboard-fixture failure from delayed native
SyncView selection; draining that event before each independent fixture resolved it.
A final source review caught infinite axes without endpoints and preview of hidden
occurrences. Visual inspection caught internal link labels and a blank framebuffer
after the Tasks layout transition. The label is fixed; normal view.redraw before
capture produced clean Cancel pixels. That blank capture is not accepted evidence
of a renderer or on-screen display defect. No new feature work followed acceptance.

**Packaging/checks:** all twenty-one Python source/test scripts parse and match the
copied native development payload. All 115 checked local Markdown file targets
resolve. Diff whitespace passed. Task-only profiles, fixtures, captures and logs
were removed from
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6c_translate`
after recording results. Useful native build/dependencies and tracked tests remain.

**Publication:** source milestone `6e18b9289d` pushed to
`origin/codex/freecad-1.1.4-baseline`; remote revision verified. No owner-build
delivery, desktop shortcut change, release or deployment.

## G1.6c2 linked-instance Copy/Paste — October 10, 2026

**Implementation:** context-menu Copy/Paste and focused-tree Ctrl+C/Ctrl+V create
native links to the same definitions. A copied parent includes its children through
that shared definition; descendant selections are not pasted again. Repeated visible
occurrences remain distinct selections. Clipboard snapshots use document UUID/object
Name/ID plus copied local placement, LinkTransform and visibility. Paste preflights
all definitions and cycles, then creates the whole batch in one defining-document
transaction. External destinations require their own file's catalog/imports. No
implicit import, definition clone, schema change or system-clipboard override.
Failed transactions roll back all new links. New occurrences are selected; Edit,
History and camera remain unchanged. Native editors/pending operations and stale
menus/rows are guarded; panel closure discards its transient clipboard.

**Destination convention:** the owner notes confirm shared Copy/Paste followed by
movement but do not specify the exact Paste destination. An optional clarification
was asked; no answer had arrived when implementation began. The announced default
is the explicitly selected file/component parent, with copied placements retained
relative to that parent. This is an implementation convention, not recovered owner
approval. The technical contract records it; newer owner direction supersedes it.

**Build:** FreeCADPlusScripts passed in the existing native G1.6b development tree.
Only scripts changed; no native rebuild, owner delivery or shortcut change.

**Validation:** six focused cases and **50/50 combined Group 1 cases** passed,
zero failures/errors/skips, normal application exit (combined run 60.597 seconds). Two initial fixture assumptions
were corrected: a missing imported source removes invalid panel rows, and an empty
native transaction need not report HasPendingTransaction. Tests now retain the stale
row before closure and make an actual caller change before testing its transaction
guard. The first combined run's existing tab-switch check also required native
delayed SyncView selection to finish before starting its independent new-document
scenario; the isolated diagnostic confirmed this without changing application
preferences or selection behavior. A subsequent combined run exposed a real dock
reopen error: activeSubWindow could be temporarily absent while a native view still
existed. Panel state now finds the subwindow owning that view, and the singleton
releases the retiring panel before constructing its replacement. The clipboard's
panel-reopen case explicitly covers an absent activeSubWindow. The final combined
run passed after these fixes.

An independent process reopened domestic and external `.cadprt` fixtures with exact
native IDs, shared definitions/links and copied placements retained. A subsequent
external source-only change saved without changing the importing assembly checksum;
a second reopen retained that change. Clipboard contents correctly did not persist.
Inspected normal OpenGL pixels show three clean shared cylinders; the Part Tree
shows three parent occurrences with their shared children. The context menu shows
Copy and the expected disabled Paste after fresh startup. No owner preference or
renderer changes were made. These checks finish this increment; no further feature
implementation or runtime testing follows.

**Packaging/checks:** nineteen Python source/test files parse and match the copied
native development payload byte for byte. All 93 checked local Markdown file targets
resolve. Final diff whitespace passed. Task-only profiles, fixtures, captures and
logs were removed from
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6c_clipboard`
after recording the results; useful native build/dependencies and tracked tests remain.

**Publication:** source milestone `e092033275` pushed to
`origin/codex/freecad-1.1.4-baseline`; remote revision verified.
No owner build, shortcut delivery, release or deployment was performed.

## G1.6c1 component file tabs — October 10, 2026

**Implementation:** the two component context menus offer Open in new window.
It creates another native view of the current file with the selected occurrence's
Edit context, or the existing view-only isolation for an unused definition. Models
uses the originating tab's remembered occurrence. The original tab's context/camera
are retained, the new tab is labeled for its edited component, and the same native
source objects/transactions/save services are reused. No new document, placement,
model property, schema or permanent window record is introduced. Native feature
editors/pending operations block opening; stale menu actions are rejected. Failed
entry closes only the new view and returns to the original. View closure clears
panel state; panel reopening recognizes component tabs through a transient Qt property.
The component-window contract is in ARCHITECTURE.md.

**Build:** the existing native G1.6b development payload is reused; only the
FreeCADPlusScripts target changed. Its copy target passed. No native recompilation,
owner build, desktop shortcut change, release or deployment is part of this increment.

**Validation:** six focused GUI cases passed, followed by **44/44 combined Group 1
cases**, zero failures/errors/skips, normal application exit. These cover Models and
Part Tree menus, exact/remembered occurrence paths, child Edit in the same new tab,
original camera/context, source-owned Sketch/Pad and Undo/Redo, pending-editor and
stale-menu/row refusal, failed-open rollback, independent isolation, source/view
closure, event-driven labels and panel reopening.

The independent fresh-process verifier retained native IDs and source ownership,
changed a source Pad from 7 to 9 mm, saved it without changing the importing assembly's
archive checksum, then reopened again to confirm 9 mm. Inspected normal OpenGL
captures show the domestic component tab with its assembly context, a clean isolated
external cylinder, and the original two-cylinder assembly restored. Panel/tab-bar
captures show component/qualified external labels, active rows and Sketch/Pad History.
The original camera and Edit context remained intact. Contextual fading is still G1.7.

Two initial test expectations were corrected: native coordinated Undo legitimately
adds forwarding entries in dependent files for source changes (opening adds none),
and routine panel refresh clears transient menu feedback. The first combined runs'
sole picking failure was traced to the test fitting geometry before native camera
animation completed, producing an invalid camera/clipping combination. Test-owned
views now disable animation before rotation/fitAll; application defaults are unchanged.
The first visual harness also needed camera settling and an explicit hide/showNormal
transition after the hidden process launch before normal rendered pixels were
available. Renderer/read/draw framebuffer state was checked; final exposed-window
captures were clean. Earlier blank/widget-grab captures are not application display
acceptance. No renderer/driver/owner-preference change was made.

**Packaging/checks:** eighteen Python source/test files parse and match the copied
native-build payload byte for byte; 115 local Markdown link targets resolve. Diff
whitespace passed. Task-only profiles, fixtures, captures, probes and logs were
removed from `C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6c_windows`
after recording the results. Useful native build/dependencies and tracked tests remain.

**Publication/cleanup:** source milestone `a7c3adf4927648fb50213d95bda180af796b3654`
was committed and pushed to origin/codex/freecad-1.1.4-baseline; the remote revision
was verified. Task validation cleanup is complete. No broader
G1.6 completion, full-workbench inventory or long-session jitter acceptance claimed.
The development payload is retained; no owner delivery or shortcut change.

## G1.6b external completion and native acceptance — October 10, 2026

**Implementation:** unused external definitions stay in the assembly view for Models
selection, Edit, native Sketch/Pad History editing and viewport picking. Native
per-view catalog/edit contexts validate ownership and imported reachability, remain
silent/transient, and clear safely on view/panel/source/object teardown. A view-only
separator borrows live native display children rather than detached copies, preserving
picking and live editor preview. History starts the same active transaction as native
feature double-click, so accepted parameter edits support source-owned Undo/Redo.
No temporary App objects/links, visibility writes by isolation or schema changes.
The [architecture](ARCHITECTURE.md#unused-definitions-g16b) owns the contract.

**Build:** native development targets passed in
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_1.1.4_context`.
Release-pinned LibPack 3.1.1.3 was taken from this tag's Windows workflow; local tools
were MSVC 19.44, CMake 3.31.6, Ninja, Python 3.12 and Qt/PySide 6.8.3. The release
preset kept default workbench options; three compile jobs and native precompiled
headers were used. One internal MSVC C1001 in unchanged TaskDressUpParameters.cpp
passed an unchanged single-file retry; the remaining build then passed.

Application/Part/Sketcher/PartDesign native libraries and script targets were built,
plus FreeCADPlusScripts and the standard materials, appearance/models, Show,
stylesheet/interface and Part Design data targets listed in DEVELOPMENT_GUIDE.
The initial narrow payload lacked material data and Show/styles; those setup gaps
were corrected before acceptance. Native configuration also exposed the old Plus
module condition `BUILD_PARTDESIGN`; src/Mod/CMakeLists.txt now correctly uses
`BUILD_PART_DESIGN`, so its script target participates in the native build.

**Validation:** the final focused run passed **9/9** cases, and the combined pilot,
legacy conversion, hierarchy, external-file, panel and unused-model suite passed
**38/38**, with **zero skips**. All loaded modeling/interface modules came from the
new development build. Two actual workflow failures were found and fixed: History
entry lacked the native command transaction, and detached display copies were not
natively pickable. Tests now cover source-owned accepted Pad Undo/Redo, real viewport
selection retaining the assembly tab, per-view contexts, invalid/removed imports,
ordinary external-parent refusal, and closing the source during a native Sketch edit.

Fresh-process domestic/external reopen checks passed with object identities intact.
An external Pad changed from 7 to 9 mm and saved through its defining file; the
assembly archive checksum stayed unchanged, and another reopen retained 9 mm.
Normal OpenGL framebuffer captures were inspected: two assembly cylinders before
isolation, one external cylinder during isolation, clean native Sketch editing,
a shortened native Pad preview without an old solid, and the original two cylinders
restored afterward. The qualified temporary Part Tree row was bold/active and last;
other rows remained gray/selectable. Capture used the normal framebuffer, not
QOpenGLWidget.grabFramebuffer.

**Packaging/checks:** all seventeen Python source/test files parsed and matched the
native build's copied payload byte for byte. Diff whitespace and 115 local Markdown
link targets passed. Task-only profiles, fixtures, logs and captures were removed
from `C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6b_external` after
recording the results. The extracted pinned LibPack and useful native development
build remain; the unneeded downloaded LibPack archive was removed.

**Publication/delivery:** source milestone `54ea2843a3f8c3fe89d2a495964fa290274708cf`
was committed and pushed to origin/codex/freecad-1.1.4-baseline; the remote revision
was verified. No release, deployment or owner-build delivery. This bounded development payload is not full-workbench or
long-session responsiveness acceptance. The existing owner desktop shortcut was
not changed; original workbench source/configuration remains intact.

## G1.6b domestic increment and acceptance - October 10, 2026

Historical checkpoint: its external-editing limitations are resolved by the native
completion record above; the following preserves the earlier evidence.

**Implementation:** unused domestic definitions support Edit in the current view,
a temporary last Part Tree child, active fill/bold text, gray selectable assembly
rows, native History and Sketch/Pad adapters. Native display groups are hidden by
view-only scene switches while a detached native definition display is shown.
No temporary App objects, instance links, authored Visibility writes or Undo entries
are used for isolation. File/placed Edit and panel/view/document close clean up;
definition removal clears isolation and Undo does not reopen it. The
[architecture](ARCHITECTURE.md#unused-definitions-g16b) owns details.

**Runtime:** all thirty-five combined tests passed in 34.668 seconds using this
checkout's scripts in the verified 1.1.4 GUI runtime with an isolated profile.
Six new cases cover actual Qt domestic Edit/selection, temporary row placement,
native visibility commands remaining hidden, restoration, native Sketch editor and
context-exit guard, geometry/History ownership, Undo/Redo, save while isolated,
per-view state, panel/view/document cleanup and source-removal recovery. IDs, native
link inventory and authored visibility survive saving; no temporary instance is
serialized. External-unused Edit is tested for refusal without mutation or losing
an existing domestic isolation session. All twenty-nine earlier regressions passed,
including legacy conversion and placed-external editing.

**Known remaining case:** two focused attempts at external unused Edit failed when
native selection activated the source tab. A trace localized the switch after panel
Edit returned; native Tree sync and Document::trySetEdit's local-parent requirement
explain why an unplaced external definition does not have the same editor route as
a placed link. The unsupported route is now refused before isolation starts, with
a message directing editing to the defining file. Selecting its catalog row can
still activate that source tab. This is a bounded partial implementation, not a
change to owner requirements or a passed external-unused workflow. The next task
is to finish that integration, including source-only save and Undo checks.

**Fresh process / visual:** the saved isolated fixture reopened without isolation,
with all IDs, visibility and native link names intact. Editing its unused Pad from
7 to 9 mm produced valid 81*pi mm3 geometry and saved a separate file. Inspected
3441 x 1767 normal framebuffer captures show two assembly cylinders before editing,
only the larger unused cylinder during editing and both originals after exit.
The initial panel capture exposed a theme whose disabled text was white; explicit
gray inactive-row styling corrects that confirmed presentation requirement.
The repeated fresh-process/visual check passed and the final panel pixels show gray
assembly rows and the green/bold temporary last child. These are bounded automated
checks, not complete panel or long-session responsiveness acceptance.

**Build / delivery:** CMake script copy/install and syntax checks passed for all
seventeen module/test scripts. Native C++ was not rebuilt. No owner executable was
delivered or desktop shortcut changed; the panel remains developer opt-in.

**Publication / cleanup:** this domestic increment is committed and pushed to
origin/codex/freecad-1.1.4-baseline with remote hash verification at handoff. Task-only
profiles, fixtures, captures, logs and script packaging outputs are removed after
recording these results. Tracked code/tests and useful baseline builds are retained.

## G1.6a implementation and acceptance - October 10, 2026

**Implementation:** opt-in Components dock with Models/Part Tree/History, nested
external catalogs, one pinned file row, placed-component Edit, full occurrence
tracking and native selection. All shared occurrences/model rows have active fill
and bold text; the edited occurrence has a separate outline. Models reuses the last
occurrence per view. File History has undoable Origin/plane visibility controls.
Rows retain identity across updates; document/GUI events coalesce, idle has no polling,
invalid/stale actions are refused and closing unregisters observers. The
[architecture](ARCHITECTURE.md#panel-foundation-g16a) owns the detailed contract.
Unused-model editing, component windows, remaining context actions, Part Type and
contextual fading are not implemented by this increment.

**Runtime:** all twenty-nine combined tests passed in 24.228 seconds in the verified
1.1.4 GUI runtime with the checkout's scripts and an isolated profile. Six panel
cases joined all twenty-three prior regressions. Actual Qt mouse events checked
single-click selection without Edit, double-click Edit, occurrence memory and shared
highlighting. Tests also covered row preservation across rename/refresh, independent
view contexts, changed-tab/stale-row refusal, Undo of occurrence removal, external
Edit staying in the assembly, origin visibility Undo/Redo/save/reopen, observer cleanup
and no idle refresh. Twenty rename events coalesced into at most two refreshes.
Panel presentation created no native objects or Undo transactions.

The first focused run had a click-selection failure and an origin fixture that
assumed a hidden Origin implied a hidden plane. The fixture now explicitly hides
the plane before Show. The click failure did not reproduce in the next focused run
or the full suite; no speculative application fix is claimed for that first result.
The two final suites exited normally with no panel observer errors. Baseline regression
logs contained their expected invalid-Pad and source-copy UUID diagnostics.

**GUI/fresh process:** a separate process opened the saved panel fixture, retained
all native object IDs and Undo count through panel interaction, and returned to the
four file-origin History rows. Inspected captures of Models, Part Tree, component
History and file History were clean/readable. Both shared-child occurrences were
highlighted and the second had the Edit outline; History showed Sketch/Pad without
Body rows. This is bounded automated interaction evidence, not long-session jitter
acceptance or full panel completion.

**Build/delivery:** CMake script copy/install passed and all fifteen module/test
scripts matched source; syntax and whitespace passed. Native C++ was not rebuilt.
The developer panel is opt-in and the original tree/workbenches remain. No owner
executable was delivered or desktop shortcut changed. Reproduction is in the
[guide](DEVELOPMENT_GUIDE.md#component-panel-foundation-validation).

**Publication/cleanup:** the coherent G1.6a milestone is committed and pushed to
origin/codex/freecad-1.1.4-baseline, with remote hash verification at handoff. Task-only
profiles, generated CAD fixtures, captures, logs and script packaging outputs are
removed after recording results. Tracked implementation and tests are retained.

## G1.5 implementation and acceptance - October 10, 2026

**Implementation:** schema 4 adds native imported-file catalogs with persisted
source UUIDs and pre-restore dependency checks. Importing includes nested catalogs
without placing geometry. Native linked occurrences resolve across defining files;
Sketch/Pad edits transact in the source file while retaining the assembly tab/context.
Explicit source Save writes only that file. Independent recursive copies preserve
native graphs and require an explicit placement-replacement selection. Circular
imports/nesting are refused before mutation. Schemas 1-3 remain supported with an
explicit undoable upgrade before external imports. Full contracts, save ordering,
exact-path recovery and remaining UI boundaries are in [ARCHITECTURE](ARCHITECTURE.md).

**Runtime:** twenty-three tests passed in 14.221 seconds in the verified official
1.1.4 GUI runtime using this checkout's module and an isolated profile: seven new
external-definition cases and all sixteen prior regressions. They cover nested
unused catalogs, same-name distinct definitions, source-only geometry ownership,
source Undo/Redo, domestic/external independent copies with nested shared links,
explicit selected-placement replacement and Undo/Redo, unimported targets, file and
component cycles, schema upgrade, unsaved files, missing/wrong/future dependencies,
missing definition targets, failed defining-file saves and recovery. A review-found
save-order case now refuses unsaved intermediate import catalogs before overwriting
the assembly. Native dependent-file Undo entries are expected, not evidence that
model geometry moved into the importing file.

A separate process reopened the Assembly -> Hardware -> Fasteners fixture, retained
native source UUID/object IDs and full occurrence paths, changed the external Pad
from 5 to 8 mm and saved only Fasteners. The assembly archive hash stayed unchanged;
its two occurrences updated to 32*pi mm3 and retained the 8 mm length on reopen.
Missing dependency recovery restored the original exact file/path and retried;
identity mismatches never fell back to same-named definitions. Failure preflight
opened no documents and preserved fixture archives. No owner files were touched.

**GUI:** native Sketch and Pad editors entered/exited through the second nested
external occurrence using setEdit/resetEdit. The assembly stayed active; resolved
source feature and Edit path remained correct. The normal framebuffer (3441 x 1767)
showed exactly two clean cylinder instances. Initial capture-harness attempts found
an additional native OpenGL widget and an unloaded Qt binding; selecting the active
MDI window and importing QtOpenGLWidgets resolved capture, without product changes.
This does not claim full panel, mouse-driven flow or long-session jitter acceptance.

**Build/delivery:** script-only CMake copy/install passed; all thirteen module/test
scripts matched source and syntax/whitespace passed. Native C++ was not rebuilt.
No new owner executable or panel is delivered; the desktop shortcut remains on the
archived fork. G1.6 and other groups have not begun. Reproduction is documented in
[external-definition validation](DEVELOPMENT_GUIDE.md#external-definition-validation).

**Publication/cleanup:** the coherent G1.5 milestone is committed and pushed to
origin/codex/freecad-1.1.4-baseline, with the remote hash verified at handoff.
Task-generated profiles, fixtures, captures, logs and temporary script-build outputs
are removed after the recorded checks; tracked tests remain available.

## G1.4 implementation and acceptance - October 10, 2026

**Implementation:** schema 3 supports nested domestic definitions and shared native
App::Link instances, parent-owned local placements, full occurrence paths and cycle
preflight. Native Plus Edit, Part and Body contexts carry the selected path; History
omits child links and Body rows. Legacy Part/link trees convert with native IDs,
frames and shared targets preserved, with intentional group-edge replacements
recorded. Schemas 1/2 retain their previous bounds until an explicit undoable upgrade.
The [architecture](ARCHITECTURE.md) owns the full contract and remaining limitations.

**Runtime:** sixteen tests passed in 7.358 seconds using the verified official
1.1.4 GUI runtime, an isolated profile and this checkout's scripts. Five hierarchy
cases joined all eleven existing pilot/conversion regressions. They covered shared
Pad edits in repeated parents, composed rotations/translations, moving one child
placement across all parent occurrences, Undo/Redo, cycle/cross-file rejection,
rollback, independent view contexts, stale/ambiguous paths and explicit schema upgrade.
Definitions could retain their own geometry and child components simultaneously.

A second process reopened both a newly created hierarchy and a converted legacy
assembly, retained object IDs/paths/placements, edited shared geometry and saved
separate results. In the native fixture a 2 mm radius Pad changed from 9 to 11 mm;
in the converted fixture three occurrence paths reflected Box lengths of 5 then
7 mm (volumes 60 then 84 mm3). Legacy Part and link placements, native transform
modes, geometry centers and shared targets survived conversion. The source FCStd
hash remained unchanged. No owner files were converted.

**GUI:** original Sketch and Pad editors opened through the second repeated
occurrence and exited using native resetEdit. The full Edit path remained selected
and the original 9 mm Pad remained valid. A normal viewport framebuffer capture
(2301 x 1202) showed exactly two parent boxes and two shared child cylinders, with
no extra visible stored definitions or capture corruption. The check did not claim
full panel interaction, mouse-driven acceptance or long-session jitter testing.

**Build/delivery:** script-only CMake copy/install passed; all eleven module/test
scripts matched source and syntax/whitespace passed. Native C++ was not rebuilt.
No new owner executable or full panel is delivered; the desktop shortcut remains
on the archived fork. External-file work and panel construction have not started.

**Publication/cleanup:** the coherent G1.4 milestone is committed and pushed to
origin/codex/freecad-1.1.4-baseline with the remote hash verified at handoff.
Task-generated fixtures, profiles, captures, logs and temporary script-build outputs
were removed after results were recorded. Tracked tests are reproducible through
the [guide](DEVELOPMENT_GUIDE.md#hierarchy-validation).

## G1.3 implementation and acceptance - October 10, 2026

**Implementation:** isolated `conversion.convert_file` plus schema-2 support for
native standalone geometry. Preserves native single-Body features, sketch attachment
and profile references, expressions, names, labels, object IDs and placements.
Empty files, native Boxes and static shapes/curves are supported. Unknown standalone
Part-derived geometry requires explicit fallback; loss reporting persists in the
new file. Unsupported graphs fail without an output file. The [architecture](ARCHITECTURE.md)
owns the complete conversion and schema contract.

**Runtime:** eleven tests passed in 5.253 seconds in the matching official 1.1.4 GUI
process: five conversion tests and the six existing pilot tests. A separate process
then passed reopen/edit/recompute/save of the converted Body. Final processes exited
normally with code 0. Checks used only generated fixtures in an isolated profile.
No owner document was converted or modified.

The native Body fixture retained translation/rotation, an origin-plane sketch
attachment, Pad Profile and an expression-driven Length. The converted input changed
from 5 to 7 with Length changing from 10 to 14 mm; Undo/Redo restored those values.
A fresh process verified identity/reference/placement persistence and changed the
input to 8, producing Length 16 mm and valid geometry before saving a separate file.
The original FCStd hash remained unchanged. An open source's deliberately different,
unsaved input stayed at 9 and remained dirty; conversion used the saved disk version.

Other checks covered an editable native Box, a static curve, a valid empty file,
explicit geometry-only recovery and persisted warnings after reopen, rejection of
multiple roots, injected save failure, existing-destination protection and staging
cleanup. Schema-1 files reopened and saved without upgrading. Adding a new sketch
to a converted direct-geometry component still creates the backend Body correctly.
The new converted file deliberately has a distinct Document.Uid, with source/output
UUIDs recorded in ConversionReport; native object IDs remain stable except for the
explicitly reported replacement of a geometry-only fallback object.

**Build and delivery:** script-only CMake build/install passed; all eight scripts
matched source byte-for-byte and syntax/whitespace checks passed. Native C++ was
not rebuilt. No new owner executable, conversion dialog or full panel is delivered;
the desktop shortcut remains on the archived fork. No unrelated workbench/UI
behavior was changed or baseline display testing repeated.

**Publication/cleanup:** the coherent G1.3 milestone is committed and pushed to
origin/codex/freecad-1.1.4-baseline with the remote hash verified at handoff.
Task-generated profiles, fixtures, logs and temporary script-build outputs were
removed after recording results. Tracked fixtures remain reproducible through the
[guide](DEVELOPMENT_GUIDE.md#legacy-conversion-validation).

## G1.2 implementation and acceptance — October 10, 2026

**Implementation:** a new opt-in script module under src/Mod/FreeCADPlus and its
CMake inclusion. One native file root, domestic Part001 catalog definition and
linked occurrence; native per-view explicit Edit; automatically owned backend Body;
native Sketch/Pad adapters; Body-free history projection; validated schema-1 `.cadprt`
open/save. No archived application code was restored. Original native application
and workbench source and submodule pins remain unchanged. The [architecture](ARCHITECTURE.md)
owns metadata, invariants and pilot limits.

**Runtime validation:** this checkout's scripts loaded into the verified official
1.1.4 executable listed below, with an isolated temporary profile. Six regression
cases passed in 2.109 seconds: structure/empty file, per-view Edit isolation,
modeling/ownership/rollback/Undo/Redo, persistence, future-schema/failed-save
protection, and unchanged native legacy modeling. All final test processes exited 0.

The rectangle Sketch -> Pad produced 1000 mm3 at 5 mm and 1600 mm3 at 8 mm;
Undo/Redo restored both states. Invalid Pad and unowned geometry transactions
rolled back. A valid empty component file saved successfully. Selecting a component
while in File Edit did not grant the adapter an editing target. Independent views
retained separate contexts.

Exact `.cadprt` filenames, preserved CheckExtension, idempotent reopen, native
Document.Uid/object names/IDs, linked targets and rotated/translated occurrence
placement passed. A second process reopened the saved pilot, changed its native
Pad to 7 mm (1400 mm3), recomputed and saved a separate edited file. Future-schema
files were refused without content changes; a native save failure preserved the
prior valid file, pending edit and dirty state. A renamed FCStd was refused as
unversioned. A normal FCStd native Body/Sketch/Pad control remained functional.

**GUI validation:** the pilot sketch entered/exited the original Sketch editor.
The original PartDesign_Pad command opened its native task and accepted through
its existing OK button, producing a valid 2000 mm3 solid and the correct Body Tip.
The normal viewport buffer (2301 x 1202) showed one clean solid with definition
hidden and linked instance visible. Capture used the previously established
framebuffer-read procedure. Full panel, physical monitor and long-session jitter
acceptance are not claimed.

**Build:** this script-only module configured, copied and installed successfully
using the repository's CMake helper and existing Ninja. No unchanged native C++
code was rebuilt. Build/install outputs were byte-compared to source. No new owner
executable was produced; the desktop shortcut still targets the archived fork.
This is a development pilot, not a delivered component-panel UI. Original file and
workbench commands are not globally overridden. The full panel is G1.6.

**Publication and cleanup:** the coherent G1.2 milestone is committed and pushed
to origin/codex/freecad-1.1.4-baseline, with the remote hash verified at handoff.
Task-generated profiles, fixtures, captures, logs and the temporary script-build
harness/output were removed after recording these results. Tracked tests remain
reproducible using the [development guide](DEVELOPMENT_GUIDE.md#component-pilot-validation).

## Clean FreeCAD 1.1.4 baseline

Owner requested the clean latest stable source in the existing fork on October 10,
2026. Official releases/latest resolves to 1.1.4; 26.3rc1 is separately labeled a
release candidate. Selected official commit:
4fd3bf320d9566a27e60069fc8387448aaa3a094.

Local branch: codex/freecad-1.1.4-baseline. Source checkout and release-pinned
submodules are present. Original tracked source matched the official tag before
the documentation/ignore overlay. Four stable submodules replace the previous
seven recursive modules. Old dependency/cache remnants were removed only after
3,740 files in 45 directories matched the verified source archive.

Preserved the five UI specifications, source evidence, original documents/icons,
unverified-change inventory and archive reference. Historical implementation
records now live under archive/pre-restart-docs. Active source links in the review
inventory point to the immutable old-fork commit, not similarly named stock files.
No owner requirement has been approved or rejected by this transition.

Integrity checks pass: all original application source matches upstream 1.1.4;
all four pinned submodules are clean; requirement wording in the five specifications
is unchanged apart from evidence-link destinations; 664 historical documents/assets
are byte-preserved. Active documentation links/icons and staged whitespace pass.
Published baseline commit f608ea07afffa1ed3a426b09d207b59bf4e8bfd7 to
origin/codex/freecad-1.1.4-baseline and verified the remote hash. GitHub default
branch and local origin/HEAD now point to this baseline. Old main and the archive
tag remain intact. A final documentation commit records this completed handoff.
Committed archival blob hashes also match all 664 preserved documents/assets.
Temporary source staging was removed after checks. The subsequent runtime check
below uses the official binary; this checkout has not been compiled locally.

## Stable baseline inventory and light runtime check â€” October 10, 2026

**Result: provenance, source integrity, core functionality and the light baseline
display check pass.** The earlier viewport artifacts were reproduced only through
the capture method; direct display-buffer reads are clean. This is a bounded
baseline check, not exhaustive GUI acceptance or an owner-ready Plus build.
No application source was changed.

### External release evidence

- [Official FreeCAD 1.1.4 release](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4):
  published September 28, 2026; neither draft nor prerelease. The latest-stable
  endpoint selected this release; 26.3 RC1 is a prerelease.
- Release commit `4fd3bf320d9566a27e60069fc8387448aaa3a094` has successful upstream
  [Build Release](https://github.com/FreeCAD/FreeCAD/actions/runs/36432494038) and
  [FreeCAD master CI](https://github.com/FreeCAD/FreeCAD/actions/runs/36431033844)
  workflow runs. This is publisher release/CI evidence, not an independent
  certification of this PC or a guarantee of every operation.
- Original source, workbench definitions, build files and tests still match
  `upstream-1.1.4`. Only the instruction/documentation/ignore overlay differs.
  All four release-pinned submodules are clean.

### Local package inventory

The tested executable is a fresh official portable package on this PC, separate
from older Plus builds and any separately installed FreeCAD. It reports exactly
this checkout's source commit. It is not a locally compiled fork binary.

| Item | Observed value |
| --- | --- |
| Package | `FreeCAD_1.1.4-Windows-x86_64-py311.7z`, 418,088,341 bytes |
| Package SHA256 | `4828741fc91ee37fafcdb97a1abacb18b04ba451ac4372d9ff7a7349b36f4d6d`, matches publisher release digest |
| Executable SHA256 | `7b38c5d5aa2c74f830539c1c5c44cbf6e3e8e157292c718f9ee24ac6d3e12cf6` |
| Windows signature | Valid; The FreeCAD project association AISBL |
| FreeCAD runtime | 1.1.4, revision `20260928 (Git shallow)`, commit `4fd3bf320d9566a27e60069fc8387448aaa3a094` |
| Python / Qt / Open CASCADE | 3.11.14 / 6.8.3 / 7.8.1 |
| Payload after checks | 35,589 files; 2,307,887,823 bytes, including runtime-created caches |
| Local source build | Not configured or compiled; cached 26.3 LibPack is not assumed compatible with 1.1.4 |

Payload directory:
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_1.1.4_official_baseline/FreeCAD_1.1.4-Windows-x86_64-py311`.
Executable: `bin/freecad.exe` beneath it. The verified download is retained under
`test-builds/dependencies/FreeCAD-1.1.4-official` for reproducible extraction.
Both are useful baseline dependencies, not superseded builds.

All 19 registered workbenches activated successfully: Assembly, BIM, CAM, Draft,
FEM, Inspection, Material, Mesh, OpenSCAD, Part Design, Part, Points, Reverse
Engineering, Robot, Sketcher, Spreadsheet, Surface, TechDraw and Test Framework.
`NoneWorkbench` is additionally registered as the empty workbench.

The package contains 30 module directories: AddonManager, Assembly, BIM, CAM,
Draft, Fem, Help, Idf, Import, Inspection, Material, Measure, Mesh, MeshPart,
OpenSCAD, Part, PartDesign, Plot, Points, ReverseEngineering, Robot, Show, Sketcher,
Spreadsheet, Start, Surface, TechDraw, Test, Tux and Web. Module directories are
not all selectable workbenches: upstream MeshPart does not register its own
workbench, and Start is a command. No Plus workbench filtering was applied.

### Local checks and limits

Checks used the actual GUI executable's Python/Qt APIs with temporary
`FREECAD_USER_HOME`, `FREECAD_USER_DATA`, `FREECAD_USER_TEMP`, user and system
configuration paths. Existing owner preferences and addons were not used.

| Check | Result |
| --- | --- |
| GUI startup, runtime identity and workbench activation | Pass; all 19 registered workbenches loaded |
| Sketch solver and Pad | Pass; constrained 20 x 10 mm rectangle padded 5 mm produced a valid 1,000 mm3 solid |
| Recompute, Undo and Redo | Pass; Pad length 5 -> 8 mm changed volume 1,000 -> 1,600 mm3; Undo and Redo restored both states |
| Pocket | Pass; radius 2 mm, depth 3 mm produced a valid 1,562.300888 mm3 solid |
| Spreadsheet expression and native Link | Pass; cell-driven pocket depth updated model and linked instance; 30 mm instance offset retained |
| Part Boolean | Pass; box/cylinder cut produced a valid solid with expected volume |
| STEP and STL | Pass; STEP export/reimport preserved volume; STL reopened as a solid mesh with 124 facets |
| FCStd persistence | Pass; 15-object model, expression and link survived save/reopen and separate-process restart; subsequent edits recomputed correctly |
| Model image export | Pass; visually inspected image shows both solid instances and their circular pockets correctly |
| Event processing and process exit | Pass; timed Qt callbacks and view switching completed; successful primary and cold runs exited normally with code 0 |
| Baseline viewport rendering and responsiveness | Pass in the focused follow-up below; capture-induced artifacts isolated, camera/resize/workbench checks clean. No comprehensive jitter benchmark claimed |

The primary run passed 10 automated check groups and the fresh-process run passed
four, including repeated startup/render/event-loop checks. Successful capture calls
alone do **not** establish correct visible rendering. The primary run took about
30 seconds, the cold run about 12; these include initialization and test delays,
and are not startup benchmarks. No exhaustive suite, complex real-world assembly,
CAM machining, FEM solver, long-duration interaction or manual jitter comparison
was performed.

Initial automation waited at BIM's normal welcome dialog. Only the task-owned
process was stopped; BIM `FirstTime=false` in the temporary profile allowed the
check to finish. A later capture-only harness used an unavailable compatibility
import; correcting it to PySide6 allowed that probe to finish. Neither interruption
is counted as an application crash.

OpenSCAD's workbench loaded, but reported its external OpenSCAD executable was
not found. Operations requiring that program are not verified or ready. Other
external solvers/toolchains were not validated.

### Display gate resolved â€” October 10, 2026

The owner requested resolution and was unavailable for manual tests. The agent
completed an automated comparison and interaction check using the same official
binary with fresh temporary settings. Native computer-use inspection still failed
to initialize (Windows sandbox helper setup), so FreeCAD's own GUI/OpenGL APIs
provided the evidence. No owner visual test or mouse-driven test is claimed.

**Finding:** `QOpenGLWidget.grabFramebuffer()` produces the stippled/colored image
on this system. Reading the existing viewport framebuffer directly with
`glReadPixels`, without invoking a capture-triggered redraw, produces the correct
image, including both blue solids, circular pockets, navigation cube and axes.
The normal display buffers before capture, after capture and after an ordinary
redraw were visually clean and byte-identical. This isolates the observed defect
to the capture path; it does not establish the precise underlying Qt/Coin/driver
fault. No application or graphics-driver workaround was necessary.

| Evidence | Observed result |
| --- | --- |
| Renderer | NVIDIA GeForce GTX 970/PCIe/SSE2; OpenGL 4.6.0 NVIDIA 560.94 |
| Qt / display scaling | Qt 6.8.3; device pixel ratio 1.5 |
| Initial display buffer | Default FBO 2 was bound; color attachment read; no OpenGL read error |
| Clean before/after/redraw images | All SHA256 `798ad968468a15cfc27962dcabf38c17f78e8baaea4834a6d165fd881a6ea040` |
| Corrupt Qt capture | SHA256 `9fb219e96b5cdf5ee91f865e2aa79dc63e906e1d79f05c14bc09569222b68133` |
| Camera changes | Front view, 13 orientation updates through 48 degrees, zoom to 80% of prior camera height, and restored isometric view completed |
| Window resizing | 1280 x 900 -> 1100 x 760 -> 1280 x 900 logical window sizes; viewport resized correctly |
| Workbench changes | Part -> Sketcher -> Part Design completed with clean viewport buffers |
| Display captures | Eight interaction-stage buffer reads, all without OpenGL errors; inspected front, rotated, zoomed, resized, switched-workbench and restored views were clean |
| Idle stability | Final view and repeat after a one-second idle interval were byte-identical: SHA256 `057eba7ce2c0cf4f4f4adea10f3feda72f22864970fb965b1f7307c38cc44252` |
| Event processing | 262 callbacks on a 50 ms timer; largest observed gap 0.344 seconds, including workbench initialization/capture overhead |
| Geometry and exit | Sample remained a valid solid at its expected volume; successful diagnostic and interaction runs exited with code 0 |

The first interaction harness omitted the Pivy camera binding import and stopped
advancing at zoom. Only its own process was terminated; importing the binding made
the complete rerun pass. This was a probe error, not an application crash. A Pivy
SWIG deprecation warning did not affect the completed check.

This closes the light baseline display gate without requiring owner testing.
It establishes clean rendered viewport contents and bounded API-driven interaction
on this PC; it is not a monitor/video capture, frame-rate benchmark, long-session
stress test, or proof about the archived fork's unrelated UI jitter. No source,
owner settings, global graphics settings or driver changes were made. The
[development guide](DEVELOPMENT_GUIDE.md#viewport-capture-validation) records the
capture method for future checks.

The existing desktop `FreeCADPlus.exe - Shortcut.lnk` still targets
`test-builds/freecad_plus_2026-10-10_part_types_payload/FreeCADPlus.exe`, with that
payload as its working directory. It launches the archived fork, not this baseline.
The official package is retained for baseline verification; no new owner build,
shortcut delivery or release is claimed. Temporary macros, test profiles, models,
logs and captures are removed after recording this durable result.

## Recovery references

Verified source archive and restoration evidence: [ARCHIVE_REFERENCE.md](ARCHIVE_REFERENCE.md).
Previous fork final main: b3d8a0a2fe532ca1693132eac5ab24a2bd1651c2.
Archive tag: archive/freecad-plus-2026-10-10, checkpoint
29496214b34a53fa1d479f35ab5669b41ed4fb18.
The old main history remains available; no force-push or history replacement is used.
