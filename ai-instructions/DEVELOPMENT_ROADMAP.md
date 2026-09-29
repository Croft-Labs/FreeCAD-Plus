# FreeCAD Plus: Development Roadmap

## Current focus

- Active implementation: [prioritized upstream issue work](#upstream-issue-work).
  Latest: modern CAM avoidance now stops on boundary failures or unsupported
  strategy switches instead of ignoring exclusions. Python-only update installed;
  all 67 focused/related CAM regressions pass. Remaining child cases: U.14-U.16.
  Audit inherited fixes and changed workflow applicability first. Mirror #32706
  is now fixed in the local application: one targeted compile/relink completed
  the accumulated batch, and all 75 issue regressions pass. No full rebuild.
  Recovery, quantity input, unified Extrude keyboard editing and tree-selection
  regressions now pass against the existing fork; see U.5 and U.9 below.
- Planning priority: [NX-style unified feature history](#nx-feature-history), then
  [consistent modeling workflows](#nx-modeling-workflows), then
  [downstream integration](#nx-downstream-workflows). These phases describe the
  user's preferred FreeCAD Plus workflow, drawing on NX and SolidWorks; they are
  not a claim of exact product parity or authorization to start implementation.
- [Phase 6: STL CAM and holding tabs](#cam-mesh-machining) is implemented and built.
  All 22 focused automated tests pass; related regressions have 112 passes and one
  optional dependency skip. Native acceptance and simulation remain pending.
  Two-sided/indexed machining uses separate manually indexed jobs.
  The NX-style history plan remains planning only.

- Current build and closeout evidence: [consolidated validation, 2026-09-29](#consolidated-validation).
  Before the CAM changes, the configured Windows application built successfully
  and all 149 regression tests passed at both tested display scales. This evidence
  is separate from the later CAM validation in Phase 6. Physical viewport/keyboard acceptance remains pending:
  the user stopped native computer use with Escape before those checks completed.
- Isocline Curve implementation is recorded in [Phase 5](#isocline-curve), Trim Body
  in [Phase 4](#trim-body), and Revolve/Groove offsets in milestone 3.9.
  Milestone 2.2 and the later manual acceptance milestones remain open; another
  rebuild alone will not complete them.
  This roadmap records status; it does not authorize new phases or external publication.
- The [Part Design workflow audit](#part-design-workflow-audit) inventories the
  remaining selection and complete-editing work. Audit complete; implementation pending.
- Preferred future command layout: [unified geometry workflows](#unified-feature-workflows)
  with Add/Subtract first in the task pane; Extrude passes the automated checks below.

<a id="upstream-issue-work"></a>
## [   ] Upstream issue work: reliability before workflow polish

Authorized 2026-09-29. Order and live links: [FREECAD_ISSUES.md](FREECAD_ISSUES.md).
Complete each issue only with relevant source, runtime and acceptance evidence;
closed upstream, inherited source, and obsolete UI entry points are distinct states.

- [ X ] U.1 Triage all ten watchlist issues against this fork, prioritized by data
  loss, system responsiveness, wrong geometry/toolpaths, numeric input and UI impact.
  Recovery #18044, numeric #32700/#32717/#32718, arc #32690 and tree #28412 fixes
  are inherited. #28412 is now closed upstream. No duplicate fixes were applied.
- [ X ] U.2 Verify CAM arc-offset regression #32690 using the existing build:
  all 43 `TestPathOpUtil` tests pass, including mixed circle-normal regression
  `test49`. Installed `Path/Op/Util.py` SHA-256 matches source:
  `8CEFCB9E818D91926EF29E9FDE36544735B72384B6AA99127B95E9477A2A8C98`.
- [ X ] U.3 Reproduce #32706 and prepare the bounded Part Mirror correction.
  Convert the reference plane from its enclosing Body/Part into the source's
  parent frame; preserve the source transform, shared Assembly frame and existing
  feature/property identities. Use the common GeoFeature base for datum planes.
  Added three regressions for translated/rotated Body faces, shared Assembly
  placement, Body-face references without double transformation and source moves.
  Registered them in the standard Part suite and added `ValidateUpstreamIssues.FCMacro`.
- [ X ] U.4 Build/install and validate the accumulated issue batch. Compiled only
  `FeatureMirroring.cpp`, relinked Part and synchronized three changed test scripts.
  Both build steps exit 0. All 75 regressions pass without errors/skips: six Mirror
  geometry tests (now including save/reopen and repeated recompute), two real
  Mirror task-pane reference-selection tests for translated/rotated Bodies, 43 CAM
  offset tests, four quantity tests, 19 Extrude tests and one tree test. #32706 is
  fixed locally; this does not close the upstream issue or certify physical picking.
- [ X ] U.5 Validate inherited recovery and quantity-input fixes in the existing
  source-built fork. Five isolated recovery fixtures pass through the real startup
  dialog: damaged ZIP, malformed model XML and malformed GUI XML originals still
  offer recovery; valid newer originals are excluded, valid older originals recover.
  All four recovered solids have volume 231 mm3; original hashes remain unchanged.
  Four native Qt quantity-event tests pass, including arrow/wheel focus-loss
  persistence and implicit inches with global millimetres. All 19 Extrude task tests
  pass, including two new Add/Subtract keyboard edit/step tests on create and reopen
  that check feature dimensions and solid volume. No application fix was duplicated.
  Procedure: [upstream issue validation](../tests/UpstreamIssues.md).
- [   ] U.6 #29376: obtain a reproducible affected session/GPU trace before changing
  rendering. Frame-rate limiting and background changes are already inherited;
  upstream still reports intermittent OS-wide slowdown. Do not infer resolution
  from a short successful session or one reporter's driver update.
- [ X ] U.7 Classify workflow overlap: legacy #10584 is superseded for new tasks
  by Mill Facing, but saved MillFace operations remain a regression risk (upstream
  closed as won't-fix). #27751's modern PlanarSurface/modular generator workflow
  is already inherited and used by our STL command; the wider upstream epic stays
  open. Neither classification authorizes silent migration of saved operations.
- [ X ] U.8 Publish the coherent source/triage milestone to `origin/main`:
  `85fd6ebc77a5a180d61ad116cf6507fb274e93d4`, remote hash verified.
  Python/macro syntax and diff whitespace checks pass. Build/acceptance gates
  were still open at that checkpoint; no release or new executable was produced then.
- [ X ] U.9 Validate inherited tree fix #28412 using native Qt mouse events.
  Expansion and collapse both toggle the container and preserve model selection
  during a held-button move. The planned NX history has not replaced this tree.
- [ X ] U.10 Recovery, numeric and tree regression milestone committed/pushed as
  `24815217c91ecbc2029771f34be02a5aa4c640d6`; `origin/main` hash verified.
  At that checkpoint U.4/U.6 remained open; no native build was needed for those
  inherited fixes. The subsequent U.4 checkpoint now includes the Mirror correction.
- [ X ] U.11 Passing Mirror persistence/GUI tests and build-validation checkpoint
  published as `bb6d7607a78080bec36f8ade30c8925f09201874`; `origin/main` hash verified.
  The unreproduced slowdown U.6 remains open.
- [ X ] U.12 Inspect the seven children linked from CAM umbrella #27751.
  Four are closed; open #27950, #26300 and #6864 require comparison with the
  replacement operation. Modern modular generators supersede the old code path,
  but this does not prove every reported geometry case is fixed.
- [ X ] U.13 Fix reproduced modern avoidance failure behavior related to #27950.
  Boundary/subtraction failure now raises an error instead of restoring the full
  cutting region or dropping selected exclusions. Valid fully excluded masks stay
  empty. Waterline/other strategy changes with retained face avoidance now report
  unsupported settings instead of ignoring them. Previous paths are cleared.
  Eight focused tests and 59 related generator/operation/STL/tab tests pass.
  The external planar open-face case retains full surrounding coverage and cutting
  segments do not cross the excluded face. Python files installed and hash-verified;
  no native build or document/property migration. UI behavior documented in UI-006.
- [   ] U.14 #27950: exercise the original curved GeomFillSurface fixture with the
  replacement workflow; record whether failure/coverage matches the legacy report.
  Do not infer arbitrary freeform coverage from planar/cylindrical regressions.
  Legacy Surface/Waterline remain unchanged and are not certified by U.13.
- [   ] U.15 #26300: attempt the attached freeform hang/crash case in an isolated,
  bounded process through the replacement operation; distinguish legacy applicability
  and OCL/kernel behavior before modifying algorithms.
- [   ] U.16 #6864: check final-strip coverage for nonintegral width/stepover ratios
  in the current line generator; reproduce before porting a legacy algorithm fix.
- [   ] U.17 Publish the validated CAM avoidance fix and verify `origin/main`.

CAM avoidance evidence under the external validation root below:
`avoidance-tests-20260929-192717/results.json` reproduced four failing fault-handling
checks (two valid geometry controls passed). After correction,
`avoidance-tests-20260929-193013/results.json` reports 67 PASS, no errors/skips,
process 0. Eight focused, 12 common-generator, seven pattern-generator, 18 unified
operation and 22 STL/tab tests. `module-manifest.json` records installed Python
hashes. The expanded default issue macro has 83 tests; it has not been run as a
single batch. Preserve the separate 75-test native and 67-test CAM evidence.

Reproduction evidence: `D:\Temp\Office-PC\freecad-plus-validation-20260928\issue-tests-20260929-185401`.
Existing binary run: 49 tests, 47 pass, two expected newly exposed Mirror failures,
no errors/skips, process exit 0. Translated feature-face plane is 2 mm off; rotated
case also fails. Three prior Mirror regressions and the new Body-face control pass.
The aggregate result is FAIL, not a successful validation of the pending fix.

Continuation evidence under the same external validation root (2026-09-29):
`recovery-tests-20260929-final/recovery-results.json` reports PASS for five fixtures;
`quantity-tests-20260929-191045/results.json` reports 23 tests PASS, no errors/skips;
`tree-tests-20260929-191256/results.json` reports one test PASS (both expand/collapse
subcases), no errors/skips. All processes exited 0. Earlier harness-development
runs are not acceptance evidence. These checks used existing native revision
`8abce719de` with source-loaded tests, not the unbuilt Mirror correction. Native
Qt event testing is distinct from physical viewport/keyboard acceptance.

Completed build checkpoint: `issue-build-20260929-191841/build-result.json` in the
same external root records compile/link exit 0, source hash, old/new Part module
hashes and the three synchronized script hashes. Updated `build/Mod/Part/Part.pyd`
SHA-256: `93D4E36312B52B6C0BF134F0A05351CFA3930EE5D0B35755C419E42AA78D5CA8`.
`issue-batch-20260929-191959/results.json`: all 75 PASS, no errors/skips, process 0.
The native version string remains `8abce719de`; the Part binary hash identifies
this targeted update. Launch the existing `build/bin/FreeCAD.exe` under the
external root to test it. No release, full rebuild or upstream publication.

## [ X ] Phase 1: Repository and instruction foundation

Outcome: an identifiable fork and usable project guidance.
Depends on: None.

### [ X ] 1.1 Establish the fork

Complete when: the repository, local checkout, remotes, and submodules are identified.

- [ X ] 1.1.1 Create the public `Croft-Labs/FreeCAD-Plus` fork and local checkout.
  Evidence: GitHub creation/verification in the setup session; upstream base `a5908bb06e`.
- [ X ] 1.1.2 Configure `origin` for the fork and `upstream` for FreeCAD; initialize submodules.
  Evidence: setup session verified remotes, recursive submodule status, and matching `main`.

### [ X ] 1.2 Adopt the shared instruction standard

Complete when: the root router, five core documents, and their references are checked.

- [ X ] 1.2.1 Add the local entry point and standard document ownership.
- [ X ] 1.2.2 Consolidate Pad guidance and preserve source/build/GUI distinctions.
  Evidence: documentation adoption change, with local link and heading checks on 2026-09-28.

## [   ] Phase 2: Pad task-pane workflow

Outcome: validated creation and editing through [UI-001](UI_UX_SPEC.md#ui-001-pad-task-pane).
Depends on: Phase 1.

### [ X ] 2.1 Implement the source change

Complete when: source and regression cases exist and source-level checks pass.

- [ X ] 2.1.1 Allow opening Pad without preselection; add profile controls to its shared create/edit dialog.
- [ X ] 2.1.2 Add selection restrictions, profile removal, and empty-profile handling.
- [ X ] 2.1.3 Add 14 GUI regression cases and register them in the GUI test suite.
  Evidence: local commit `e35fea1841`; C++ formatting, Python syntax, and whitespace checks passed.
  These checks do not establish compiled correctness or passing GUI tests.

<a id="pad-validation"></a>

### [   ] 2.2 Build and validate the changed application

Complete when: this fork builds and the focused suite plus manual UI acceptance pass.

- [ X ] 2.2.1 Configure a compatible FreeCAD LibPack and build outside Google Drive.
  Windows x64 Release GUI, Part, Sketcher, and Part Design targets built successfully.
  Fixed the profile selector to use `Shape.getShape()` for FreeCAD's `TopoShape`
  methods; `getValue()` returns the raw OpenCASCADE shape and did not compile.
- [ X ] 2.2.2 Correct and run the focused GUI regressions against the built fork.
  All 21 task-pane tests passed. Tests now search the active dialog, retain the
  layout's parent wrapper, and reopen via the user double-click entry point so
  edit transactions are exercised. The earlier `QPushButton` selector fix is included.
- [   ] 2.2.3 Verify viewport picking, rotated profiles, both directions, keyboard input,
  visibility restoration, Cancel, and Undo/Redo; check Pocket for shared-base regressions.
  Automated selection, visibility, Cancel, Undo/Redo, and Pocket regressions pass.
  Physical viewport/tree picking, rotated previews, keyboard navigation, and the
  complete advanced-parameter click-through remain manual acceptance work.
  Acceptance: [UI-001](UI_UX_SPEC.md#ui-001-pad-task-pane) and [test procedure](../tests/PadTaskPanel.md).
- [ X ] 2.2.4 Consolidate the configured application build and rerun all implemented
  workflow and related legacy regressions against matching runtime modules.
  Evidence: [2026-09-29 validation](#consolidated-validation), including two display
  scales, current version identity, installed-script matching and binary hashes.

<a id="extrude-validation-evidence"></a>

#### Validation evidence, 2026-09-28

Tested this checkout at `f9d592dc1f` plus the selector and test-fixture corrections
in this validation change. The source-built application reported FreeCAD 26.3.0;
the separately installed FreeCAD was not launched or used.

| Check | Result |
| --- | --- |
| Native model tests | `TestExtrude`: 8/8; existing `TestPad`: 14/14; existing `TestPocket`: 6/6. No failures, errors, or skips. |
| Native GUI tests | `TestPadTaskPanel`: 14/14; `TestExtrudeTaskPanel`: 7/7. No failures, errors, or skips. |
| Task-pane inspection | Captured and inspected Add and Subtract in the built GUI. Operation is first, Profile is second, and shared dimensions remain visible. |
| Toolbar and material result | One `PartDesign_Extrude` action in the modeling toolbar. The same `Pad` object and `Profile` produced 1080 mm3 in Add and 920 mm3 in Subtract. |
| Remaining limits | GUI tests use Qt controls and FreeCAD selection APIs; they do not establish physical mouse/keyboard acceptance. Unrelated workbenches, C++ developer tests, and cross-version recomputation in upstream FreeCAD were not tested. |

Build and test artifacts are outside Google Drive at
`D:\Temp\Office-PC\freecad-plus-validation-20260928`:
`configure-command.txt` / `configure.log`, `build-initial.log`, successful
`repair-compile.log`, `repair-resource0.log`, `repair-resource1.log`, `repair-link.log`,
`model-results.json`, `results.json`, per-suite logs, `visual-check.json`, and
`extrude-add.png` / `extrude-subtract.png`. Executable: `build\bin\FreeCAD.exe`.

The fork build used source-pinned `LibPack-26.3.0-v3.5.3-x64-Release` and MSVC
19.44.35211. Archive SHA-256:
`DCAA2D21F61B0607CF06B6E98F6E7525DC266C04C20E7B4D7B2C77BEC24366E7`.
Focused build and test reproduction guidance is in the
[development guide](DEVELOPMENT_GUIDE.md#commands). Settings and test documents
were isolated from the normal user profile. No push, installer, or release was made.

<a id="consolidated-validation"></a>

#### Consolidated validation, 2026-09-29

This evidence supersedes the older executable/version-stamp limitations recorded
in the individual feature milestones below. Native application source is commit
`8abce719de38a1b1ad255d0e7f4554a9d44e9c71`. This closeout adds a reusable validation
macro and documentation; no feature implementation change was needed.

| Check | Result |
| --- | --- |
| Configured Windows x64 Release build | Normal CMake ALL_BUILD completed with exit 0, including the main executable, core libraries, Part, Sketcher and Part Design App/Gui modules. Existing focused configuration; unrelated disabled workbenches and installer packaging are not included. |
| Build execution | The first bounded pass reached its 40-minute hard deadline after compiling core dependencies. A resumed incremental pass reused completed outputs and finished successfully in 1,680 seconds. Dependency/deprecation and temporary-directory warnings remain; no compiler error required a source fix. |
| Runtime identity | FreeCAD 26.3.0dev, revision 49009, hash `8abce719de`. Nine application/module binary hashes are recorded in the build manifest. |
| Source/runtime matching | All 80 checked Python files in Part BasicShapes/BOPTools/parttests and PartDesignTests match the checkout byte for byte. |
| Integrated regressions | **149/149 passed** in one initialized GUI: 84 model tests and 65 task tests. Zero failures, errors or skips; process exit 0. Baseline device-pixel ratio 1.5. Covers Extrude, Pad, Pocket, unified/legacy Patterns, MultiTransform, Revolve, Trim Body and Isocline. |
| Additional display scaling | The same **149/149 passed** with `QT_SCALE_FACTOR=1.5`; process exit 0. This multiplies the Windows scale rather than setting an absolute DPI: the reported device-pixel ratio was 2.25. Automated control/geometry checks do not establish readable layout or physical picking at that scale. |
| Native mouse/keyboard acceptance | Not completed. Window-control approval was granted, but capture returned `FrameArrived timed out` / `window capture timed out`. Accessibility inspection exposed an isolated fixture's close/save prompt. The user then stopped Computer Use with physical Escape; no further native input was issued. No manual acceptance gate is marked complete on that basis. |

Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
`closeout-build.log`, `closeout-build-results.json`, `closeout-build-resume.log`,
`closeout-build-resume-results.json`, `closeout-build-manifest.json`, and
`closeout-regressions/` / `closeout-highdpi/` (results, per-suite logs, process reports).
Reproduction: [`ValidateWorkflows.FCMacro`](../tests/ValidateWorkflows.FCMacro) and
[development-guide validation](DEVELOPMENT_GUIDE.md#validation).

Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
This is the updated development application, not a published installer. The separately
installed FreeCAD was not used. No push, publication, upstream round-trip validation,
or Linux/macOS acceptance is established by this work.

Remaining closeout gates: 2.2.3, the manual portions of 3.6.3/3.6.8, 3.7.4, 3.8.4,
3.9.4, 4.2.3 and 5.2.3. These need the documented viewport, keyboard and visual
acceptance checks; their builds and automated regressions are already complete.

## [   ] Phase 3: Further Part Design operations

Outcome: extend the complete task-pane workflow after Pad is validated and scope is authorized.
Depends on: milestone 2.2.

### [ X ] 3.1 Define the next operation

Complete when: an operation and its create/edit acceptance criteria are approved.

- [ X ] 3.1.1 Choose the next operation and define its input workflow.
  Evidence: user selected unified Pad/Pocket Extrude, with Add/Subtract as the first
  dropdown, and requested implementation on 2026-09-28.
  Plan paired operations as unified workflows under 3.6, rather than duplicating their
  new task controls. The individual tasks below remain coverage checks for both modes.
- [ X ] 3.1.2 Audit Part Design profile selection and shared create/edit task workflows.
  Evidence: source review on 2026-09-28 at `e0517bc4bd`, recorded below. No application
  or GUI tests were run for this audit; the installed FreeCAD was not used.

<a id="part-design-workflow-audit"></a>

#### Profile-selection findings

**Ten remaining operations share Pad's former startup workflow:** Pocket, Hole,
Revolution, Groove, Additive Loft, Subtractive Loft, Additive Pipe, Subtractive Pipe,
Additive Helix, and Subtractive Helix. Pad's source change is already recorded in
milestone 2.1; its acceptance remains in [milestone 2.2](#pad-validation).
This inventory describes the audited baseline. Pocket's subsequent source update
is tracked in 3.6.3; it no longer uses that startup picker without preselection.

In [`Command.cpp`](../src/Mod/PartDesign/Gui/Command.cpp), these ten commands call
`prepareProfileBased`. Without preselection, it searches for sketches, automatically
uses the sole eligible sketch, or opens a separate `TaskDlgFeaturePick`; it can reject
the command when no sketch exists. Thus, preselection is not literally mandatory in
every case, but the main feature editor cannot simply open with an empty profile
and let the user choose its inputs there. Required Body/base-solid prerequisites
remain legitimate, particularly for subtractive operations.

`finishFeature` opens edit mode, and
[`ViewProvider::setEdit`](../src/Mod/PartDesign/Gui/ViewProvider.cpp) obtains
`getEditDialog` for both newly created and existing features. These operations already
share their main dialog between creation and editing; that alone does not make the
definition fully editable. The following table separates missing profile controls
from existing controls that need a better entry workflow.

| Operation | Profile editing in the current task pane | Planned work / owning task |
| --- | --- | --- |
| Pad | New profile list supports selection, removal, and clearing in the shared editor. | Validate existing implementation in 2.2; include it in the complete-parameter audit in 3.4.1. |
| Pocket | [`TaskPocketParameters`](../src/Mod/PartDesign/Gui/TaskPocketParameters.cpp) uses the shared extrusion controls but has no Pad-style profile editor. | 3.2.1: open empty; add the profile section while retaining extent, direction, and start/end references. |
| Hole | [`TaskHoleParameters`](../src/Mod/PartDesign/Gui/TaskHoleParameters.cpp) edits hole settings and start references, not the `Profile` link. Its base-profile-type filter does not replace source selection. | 3.2.2: open empty; select/replace hole inputs and preserve supported circles, arcs, and points, plus size, depth, thread, and cut options. |
| Revolution | [`TaskRevolutionParameters`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.cpp) selects axis/start references but does not replace `Profile`. | 3.2.3: profile section plus existing angle, axis, direction, and extent controls. |
| Groove | Shares the revolution parameter implementation; no profile replacement control. | 3.2.4: the equivalent subtractive workflow, including base-solid validation. |
| Additive Helix | [`TaskHelixParameters`](../src/Mod/PartDesign/Gui/TaskHelixParameters.cpp) selects the axis but does not replace `Profile`. | 3.2.5: profile section plus helix modes, dimensions, axis, and handedness. |
| Subtractive Helix | Shares the helix editor and the missing profile control. | 3.2.6: equivalent subtractive workflow, including base-solid validation. |
| Additive Loft | [`TaskLoftParameters`](../src/Mod/PartDesign/Gui/TaskLoftParameters.cpp) already replaces the base profile and adds/removes/reorders sections. A profile pick replaces the link with one picked source/subelement; it is not Pad's accumulated curve list. | 3.3.1: enter directly with empty inputs; expose clear profile/section lists and preserve ordered-section editing. |
| Subtractive Loft | Same selectors and startup gate as Additive Loft. | 3.3.2: equivalent subtractive workflow. |
| Additive Pipe | [`TaskPipeParameters`](../src/Mod/PartDesign/Gui/TaskPipeParameters.cpp) already replaces the profile and edits spine references. Orientation and section/scaling controls share the task dialog. | 3.3.3: enter directly with empty inputs; complete profile, path, auxiliary-reference, and section editing in that dialog. |
| Subtractive Pipe | Same selectors and startup gate as Additive Pipe. | 3.3.4: equivalent subtractive workflow. |

#### Other Part Design features: complete-editing audit

Inventory follows the registered commands and menus in
[`Workbench.cpp`](../src/Mod/PartDesign/Gui/Workbench.cpp) and `Command.cpp`.
An existing selector below is source evidence, not a claim of full GUI acceptance.
These features must not be counted as ten additional profile-startup defects.

| Features | Source finding | Remaining work |
| --- | --- | --- |
| Mirrored, Linear Pattern, Polar Pattern | `prepareTransformed` can start without selected originals using Whole shape mode. [`TaskTransformedParameters`](../src/Mod/PartDesign/Gui/TaskTransformedParameters.cpp) adds/removes originals and changes mode. [`TaskMirroredParameters`](../src/Mod/PartDesign/Gui/TaskMirroredParameters.cpp) and [`TaskPatternParameters`](../src/Mod/PartDesign/Gui/TaskPatternParameters.cpp) provide reference/parameter controls in the reused editors. | 3.4.2: verify originals, whole-shape mode, plane/axes/directions, counts and spacing/angles on both create and reopen. No Pad-style profile prerequisite identified. |
| MultiTransform, including Scale | [`TaskMultiTransformParameters`](../src/Mod/PartDesign/Gui/TaskMultiTransformParameters.cpp) manages an ordered transformation list and embedded editors for mirror, linear, polar, and scale operations. | 3.4.2: verify adding, editing, removing, and ordering child transformations without leaving the parent task. Standalone `PartDesign_Scaled` registration is commented out; do not count it as a normal menu command. |
| Circular Pattern, Path Pattern, Point Pattern model types | `TaskPatternParameters` contains controls for these model types, but the audited Part Design command/menu registration does not expose standalone commands for them. | 3.4.2: cover existing documents containing these types and establish supported entry paths before proposing new commands. Do not infer a missing-curve-startup defect from class names alone. |
| Fillet, Chamfer, Draft, Thickness, Defeaturing | Commands accept no preselection and use the active Body Tip. [`TaskDressUpParameters`](../src/Mod/PartDesign/Gui/TaskDressUpParameters.cpp) edits edge/face references on the existing base. Individual task panels hold operation parameters; Draft also selects neutral-plane/pull-direction references. | 3.4.3: validate all subelement and parameter changes. The selector fixes the source to the current base object: define safe base replacement or explain a required Body-history constraint inside the task. |
| Boolean | The command can create an empty tool list; [`TaskBooleanParameters`](../src/Mod/PartDesign/Gui/TaskBooleanParameters.cpp) adds/removes tools and changes operation type in the shared editor. | 3.4.4: verify tool replacement/removal, operation switching, empty-state recovery, and Body dependency restrictions. |
| Additive and Subtractive Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism, Wedge | [`CommandPrimitive.cpp`](../src/Mod/PartDesign/Gui/CommandPrimitive.cpp) creates these without curve input. [`TaskPrimitiveParameters`](../src/Mod/PartDesign/Gui/TaskPrimitiveParameters.cpp) combines geometry controls, attachment, and preview in the edit dialog. | 3.4.5: verify dimensions and placement/attachment for all 16 variants on create and reopen. Changing to a different primitive class is not ordinary parameter editing. |
| Shape Binder | [`TaskShapeBinder`](../src/Mod/PartDesign/Gui/TaskShapeBinder.cpp) supports selecting, changing, and clearing support references. Creation and editing use its task dialog. | 3.5.1: verify empty startup, support changes, tracking options, and transaction behavior. |
| Sub-Shape Binder | The command directly creates/links the binder. [`ViewProviderSubShapeBinder`](../src/Mod/PartDesign/Gui/ViewProviderShapeBinder.cpp) supplies synchronize/select-source actions, without a dedicated definition task editor. | 3.5.2: add a shared create/edit task for supports and applicable binding options. This is a task-editor gap, not the profile-based startup gate. |
| Clone / Base Feature | `CmdPartDesignClone` requires exactly one selected Part feature and directly creates a new Body/base feature. [`ViewProviderBase`](../src/Mod/PartDesign/Gui/ViewProviderBase.cpp) exposes placement editing when mutable, not a complete source-definition editor. | 3.5.3: plan one create/edit task for source and supported placement changes, preserving base-feature and Body semantics. |
| Datum Point, Datum Line, Datum Plane, Coordinate System | Current menus invoke Part datum commands. [`ViewProviderDatum`](../src/Mod/Part/Gui/ViewProviderDatum.cpp) routes to the attachment editor, including from creation. | 3.5.4: verify support, attachment mode, and offsets through the same task; these are reference geometry, not extrusion-profile features. |
| Involute Gear, Sprocket | [`InvoluteGearFeature.py`](../src/Mod/PartDesign/InvoluteGearFeature.py) and [`SprocketFeature.py`](../src/Mod/PartDesign/SprocketFeature.py) create objects then enter their respective task editors; editing reuses those panels. | 3.5.5: compare editable model properties against panel controls and test both entry paths. The standalone `fcsprocketdialog.py` demo is not the workbench command's editor. |
| Shaft Design Wizard, when available | [`WizardShaft.py`](../src/Mod/PartDesign/WizardShaft/WizardShaft.py) opens a task workflow, conditionally exposed by the workbench. It is not routed through the standard feature `getEditDialog` path. | 3.5.6: inspect generated-object re-entry and rollback before claiming create/edit parity; availability and behavior remain unverified. |

Sketch creation/editing belongs to the dedicated Sketcher workflow. Editing source
sketch geometry is distinct from selecting a feature's profile. Body creation,
setting Tip, moving/duplicating objects, material tools, and geometry inspection are
management or inspection actions rather than profile-consuming feature definitions;
they are outside this feature-dialog backlog.

**Cross-cutting parameter gap:**
[`FeatureRefine.cpp`](../src/Mod/PartDesign/App/FeatureRefine.cpp) defines editable
`Refine` and `FuzzyTolerance` properties, inherited by profile features, dress-ups,
transformations, primitives, and Boolean. The audited Part Design task-panel sources
contain no controls for these properties. Therefore even panels with input selectors
cannot yet be declared complete replacements for property-editor changes. Task 3.4.1
owns the common controls and the remaining property-by-property coverage audit.

<a id="feature-task-acceptance"></a>

#### Acceptance for every feature implementation milestone

These are backlog completion criteria. Detailed operation-specific screen behavior
belongs in the UI specification when that operation is selected for implementation.

1. Creating and reopening use the same task container and controls. For unified
   Add/Subtract families, Operation is first, immediately followed by geometry inputs
   showing existing selections and supporting selection after invocation.
   Multiple sections within that task are acceptable; a separate prerequisite picker
   or property-editor detour must not be required to define the feature.
2. Add, remove, clear, and replace inputs as supported by the feature; reorder ordered
   inputs such as loft sections and transformation steps. Retain valid preselection.
   Match each model's supported geometry, including Hole points/arcs, pipe paths, and
   loft sections; do not impose Pad's profile restrictions on every feature.
3. Cover the feature's editable definition: dimensions, modes, references, directions,
   secondary extents, advanced geometry options, and applicable placement/attachment.
   Audit persisted properties against controls, preserving units and expressions.
   Computed/internal properties and incompatible object-class changes are excluded;
   any intentionally fixed structural dependency must have an explicit rationale.
4. Empty/incomplete inputs stay editable with clear guidance and safe preview behavior.
   Invalid geometry or dependency cycles cannot be accepted. Inspect constructors,
   gizmos, and selection handlers for null-profile assumptions before bypassing pickers.
5. Verify create with/without preselection, reopen and replace inputs, change each
   supported mode, clear/recover, accept/save/reopen, Cancel, and Undo/Redo. Check tree
   and viewport picking, visibility restoration, and unchanged downstream dependencies.
   Run focused regressions in the built fork and manual viewport acceptance; record
   source, build, test, and GUI evidence separately.

### [   ] 3.2 Add missing in-task profile controls

Depends on: 2.2 and 3.1.1 for the selected operation.
Complete when: each operation passes the [common acceptance](#feature-task-acceptance),
including profile replacement while editing an existing feature.

- [   ] 3.2.1 Pocket: replace the startup picker with the shared feature task and profile controls.
  Source and automated validation completed through 3.6.3; manual viewport
  acceptance remains in 2.2.3.
- [   ] 3.2.2 Hole: add input selection with Hole-specific geometry rules.
- [   ] 3.2.3 Revolution: add profile selection alongside axis and revolution controls.
- [   ] 3.2.4 Groove: provide equivalent subtractive profile editing.
- [   ] 3.2.5 Additive Helix: add profile selection alongside helix controls.
- [   ] 3.2.6 Subtractive Helix: provide equivalent subtractive profile editing.

### [   ] 3.3 Complete Loft and Pipe input workflows

Depends on: 2.2 and operation-specific scope under 3.1.1.
Complete when: all four operations open their main task with empty inputs and pass
the [common acceptance](#feature-task-acceptance), reusing their existing selectors.

- [   ] 3.3.1 Additive Loft: integrate base-profile and ordered-section selection from startup.
- [   ] 3.3.2 Subtractive Loft: integrate the equivalent subtractive workflow.
- [   ] 3.3.3 Additive Pipe: integrate profile, spine, auxiliary references, and section/scaling controls.
- [   ] 3.3.4 Subtractive Pipe: integrate the equivalent subtractive workflow.

### [   ] 3.4 Close complete-editing gaps in solid features

Depends on: 2.2 and scoped implementation choices in 3.1.1; may proceed by family.
Complete when: the common parameter gap is addressed and each listed family passes
the [common acceptance](#feature-task-acceptance). Existing controls need validation,
not automatic replacement.

- [   ] 3.4.1 Add shared advanced geometry controls for `Refine` and `FuzzyTolerance`
  where applicable; inventory other editable properties missing from each task,
  including Pad, and implement required controls with regression coverage.
- [   ] 3.4.2 Validate Mirrored, Linear/Polar Pattern, and MultiTransform create/edit
  parity, including nested Scale and supported Circular/Path/Point Pattern objects.
- [   ] 3.4.3 Complete Fillet, Chamfer, Draft, Thickness, and Defeaturing reference/parameter
  editing; resolve the current fixed-base selection boundary without invalid history.
- [   ] 3.4.4 Validate Boolean's complete tool and operation workflow.
- [   ] 3.4.5 Validate all additive/subtractive primitive dimensions and attachment workflows.

### [   ] 3.5 Complete supporting-feature task workflows

Depends on: scoped implementation choices in 3.1.1 and the common acceptance criteria.
Complete when: each included helper has a documented and validated create/edit path;
conditional wizard scope is explicitly resolved.

- [   ] 3.5.1 Validate Shape Binder support and parameter editing.
- [   ] 3.5.2 Implement a shared Sub-Shape Binder definition task.
- [   ] 3.5.3 Implement Clone source/placement creation and editing in one task.
- [   ] 3.5.4 Validate datum and coordinate-system attachment editing.
- [   ] 3.5.5 Audit and complete Involute Gear and Sprocket task parameter coverage.
- [   ] 3.5.6 Establish Shaft Design Wizard availability and edit/re-entry semantics;
  resolve any missing persisted-definition and cancel behavior before scheduling a fix.

<a id="unified-feature-workflows"></a>

### [   ] 3.6 Unify opposite operations into geometry workflows

Outcome: implement the user's preferred one-command workflow with Add/Subtract in
the task pane, as defined by [REQ-008/009](PRODUCT_SPEC.md#capabilities-and-requirements)
and the [shared interaction](UI_UX_SPEC.md#planned-unified-feature-interaction).
Depends on: 2.2, operation-specific selection coverage in 3.2/3.3/3.4, and a safe
operation-switching design. These can be developed together by feature family;
finishing all separate commands first is not required.
Complete when: each selected family passes the [common acceptance](#feature-task-acceptance)
plus operation-switching and legacy-document regressions below.

#### Strong candidates: additive/subtractive pairs

Source-backed planning inventory, 2026-09-28. Names below are proposed primary
commands; existing API/document type names remain compatibility concerns.

| Proposed command | Current features combined | Common parameters / inputs | Differences to preserve |
| --- | --- | --- | --- |
| Extrude | Pad + Pocket | Profile, start plane/offset, direction, side arrangement, lengths, limiting references, taper | Extent modes differ: Pad has UpToLast, Pocket has ThroughAll. Map modes by meaning, not enum index; validate direction and material result when switching. |
| Revolve | Revolution + Groove | Profile, axis, angle, side arrangement, start and limiting references | Retain each mode's extent/geometry rules and the subtractive base-solid prerequisite. |
| Loft | Additive Loft + Subtractive Loft | Base profile, ordered sections, ruled/closed options | Keep section compatibility and additive/subtractive result validation. |
| Sweep (Pipe) | Additive Pipe + Subtractive Pipe | Profile, spine, orientation, auxiliary spine, section/scaling options | Preserve path/section semantics and validate the resulting union or cut. |
| Helix | Additive Helix + Subtractive Helix | Profile, axis, pitch/height/turns modes, handedness, growth | Preserve helix mode dependencies and existing subtractive intersection/outside compatibility. |
| Box | Additive Box + Subtractive Box | Length, width, height, placement/attachment | Same primitive geometry; operation changes how it combines with the Body. |
| Cylinder | Additive Cylinder + Subtractive Cylinder | Radius, height, angle, placement/attachment | Same primitive geometry; validate union/cut result. |
| Sphere | Additive Sphere + Subtractive Sphere | Radius, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Cone | Additive Cone + Subtractive Cone | Radii, height, angle, placement/attachment | Same primitive geometry; validate union/cut result. |
| Ellipsoid | Additive Ellipsoid + Subtractive Ellipsoid | Radii, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Torus | Additive Torus + Subtractive Torus | Radii, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Prism | Additive Prism + Subtractive Prism | Polygon count, radius, height, placement/attachment | Same primitive geometry; validate union/cut result. |
| Wedge | Additive Wedge + Subtractive Wedge | Wedge bounds/dimensions, placement/attachment | Same primitive geometry; validate union/cut result. |

This combines **26 existing feature variants into 13 paired workflows**. The eight
primitive workflows can also share one **Primitive** command with a shape selector,
yielding six top-level families: Extrude, Revolve, Loft, Sweep, Helix, Primitive.
Changing an existing primitive's shape type needs its own compatibility design;
it is not implied by changing Add/Subtract for that same primitive.

#### Additional consolidation options

| Candidate | Possible shared workflow | Recommendation / boundary |
| --- | --- | --- |
| Linear Pattern, Polar Pattern, Mirrored; MultiTransform with Scale | Pattern/Transform with a type selector and shared original-feature list | A useful second-stage consolidation, but these are different transformations, not Add/Subtract opposites. Reuse MultiTransform's step editing; retain type-specific parameters. Circular/Path/Point model types need supported entry-path review under 3.4.2. |
| Boolean union, subtraction, intersection | Boolean with operation and tool-body selectors | Already one feature/editor; align naming and interaction with the shared operation selector rather than create another command. |
| Fillet and Chamfer | Optional Edge Treatment command with Round/Chamfer type | Shared edge selection is reusable, but curvature and parameter semantics differ. Lower priority than true additive/subtractive pairs; combining them is an option, not an agreed requirement. |

Keep **Hole** specialized for hole standards, threads, and counterbores/countersinks.
Keep Draft, Thickness, and Defeaturing distinct: they modify geometry in different
ways and are not opposite operations. Binders, Clone, datums, gears, and sketches
retain their own workflows while sharing appropriate selection and task conventions.

#### Implementation evidence and constraints

- Extrude already shares [`TaskExtrudeParameters`](../src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp).
  Revolution/Groove share [`TaskRevolutionParameters`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.cpp);
  Loft, Pipe, Helix, and primitive pairs also reuse their family task implementation.
  UI consolidation can build on those existing paths.
- [`FeatureAddSub`](../src/Mod/PartDesign/App/FeatureAddSub.cpp) already defines an
  `Operation` property, but `defineAdditive` restricts it to Union and
  `defineSubtractive` to Subtraction/Common. Existing operation controls do not make
  all feature types freely interchangeable. Inspect each geometry execution path
  and persistence behavior before implementing a shared selector.
- [`Pad::TypeEnums`](../src/Mod/PartDesign/App/FeaturePad.cpp) and
  [`Pocket::TypeEnums`](../src/Mod/PartDesign/App/FeaturePocket.cpp) demonstrate why
  copying raw property indices between feature types is unsafe. Preserve common
  parameters by meaning and identify incompatible settings explicitly.
- Unifying command presentation is separate from changing a stored object class.
  Decide how switching a committed feature between Add/Subtract preserves its
  identity, dependent links, expressions, and recompute history. Do not silently
  delete/recreate features or rename existing serialized types to match toolbar labels.

- [ X ] 3.6.1 Inventory combined-workflow candidates and record the preferred interaction.
  Evidence: the paired-feature/source mapping above; this is design documentation only.
- [ X ] 3.6.2 Define and validate the operation-switching compatibility approach;
  inventory parameter mappings, existing Common behavior, and legacy entry points.
  Source approach: retain Pad/Pocket objects and their links; append enum choices
  without changing legacy indices; match extent modes by name; restore old Operation
  lists with the saved meaning intact. Geometry direction remains independent of
  Add/Subtract. Existing Common features keep Intersect in their dropdown. Save/reopen
  and legacy-document model regressions passed, along with both legacy GUI entry
  points; see [evidence](#extrude-validation-evidence). Cross-version recomputation
  of switched features in unmodified upstream FreeCAD is not established.
- [   ] 3.6.3 Implement Extrude as the recommended first unified family, integrating
  Pad validation and Pocket task 3.2.1 rather than creating duplicate new controls.
  Source implemented on 2026-09-28: `PartDesign_Extrude` replaces the two standard
  menu/toolbar entries; legacy commands remain available. Both feature types share
  Extrude Parameters with Operation first, then Profile, and the existing dimensions.
  Switching changes the same object's Operation; To last and Through all remain
  separate choices. Subtract/Intersect require a base solid; incomplete tasks remain editable.
  Eight new model regressions, seven new GUI regressions, fourteen Pad GUI cases,
  and twenty existing Pad/Pocket model cases all pass in the built fork. The native
  build found and resolved the profile-selector API error recorded in 2.2.1.
  Task-pane layout and the single toolbar command were inspected in the built GUI.
  Source formatting, Python syntax, documentation links, and whitespace checks pass.
  Remaining gate: manual viewport/keyboard acceptance in 2.2.3; passing automated
  checks do not complete the common acceptance criteria for this milestone.
- [   ] 3.6.4 Implement Revolve, covering both tasks 3.2.3 and 3.2.4.
- [   ] 3.6.5 Implement Loft and Sweep, covering all four tasks in 3.3.
- [   ] 3.6.6 Implement Helix, covering tasks 3.2.5 and 3.2.6.
- [   ] 3.6.7 Implement paired primitive workflows and decide whether to expose them
  through one Primitive command; validate all eight shapes in both operations.
- [   ] 3.6.8 Verify Add-to-Subtract and Subtract-to-Add during creation and on reopened
  features: common parameter retention, incompatible-mode guidance, no-base handling,
  preview/recompute, dependent links and expressions, save/reopen, Cancel, and Undo/Redo.
  Test existing additive, subtractive, and Common documents and legacy commands.
  Automated coverage passed for both operations and legacy entry points, including
  parameter/identity retention, base-solid validation, save/reopen, Cancel, and
  Undo/Redo. Finish the manual rotated/reference/custom-direction, taper, start/end
  reference, and downstream-pattern scenarios in the [test procedure](../tests/PadTaskPanel.md).


<a id="combined-pattern-workflow"></a>

### [   ] 3.7 Combined Linear/Circular Pattern workflow

Outcome: [UI-002](UI_UX_SPEC.md#ui-002-pattern-task-pane) satisfies REQ-010/011/012.
Authorized by the user's request to combine pattern buttons with type first,
features second, and direction/axis and parameters after them. This advances the
Linear/Polar portion of 3.4.2; Mirror, Path, Point, concentric CircularPattern, and
other MultiTransform consolidation remain separate future work.

- [ X ] 3.7.1 Implement one Pattern command in standard menus/toolbars/task watchers.
  Creation without preselection and reopening the new Pattern share the same pane.
  Linear/Circular is first, followed by selected features and mode-specific controls.
  Keep legacy Linear/Polar commands and their persisted types unchanged.
- [ X ] 3.7.2 Preserve result identity and separate mode settings using a new
  `PartDesign::Pattern` feature backed by the existing MultiTransform engine.
  The result owns Linear/Polar parameter helpers in the same Body. Switching selects
  an existing helper; it does not replace the result, expressions, or original links.
  Empty patterns stay editable and cannot be accepted. Feature picks reject other
  bodies and dependents; list removal uses identity instead of labels/history order.
- [ X ] 3.7.3 Build and run model/GUI regressions and inspect the actual task layout.
  Windows x64 Release PartDesign App/Gui modules rebuilt with the existing MSVC/Qt
  LibPack configuration outside Google Drive. All **91 tests pass**: 58 model tests
  (Pattern 5, Linear 16, Polar 6, MultiTransform 3, Extrude 8, Pad 14, Pocket 6),
  plus 33 GUI tests (Pattern 12, Pad 14, Extrude 7), with no failures/errors/skips.
  Qt tests cover field ordering, no-preselection/face picking, mode switching, real
  direction/spacing/count controls, retained expressions, feature removal with
  duplicate labels/out-of-history order, invalid-body/dependent picks, empty-input
  rejection/recovery, same-pane reopening, Cancel, Undo/Redo, and legacy commands.
  Disabled live preview is honored and OK recomputes the final result.
  Existing MultiTransform embedded editing also passes. Corrected a Cancel cleanup
  path that could reapply parameters after rollback, and hid the embedded task
  controller to avoid overlaying the initial pane header.
  Task captures show Linear and Circular layouts in the requested order. The same
  Pattern result computes 8024 mm3 with three linear instances and 8032 mm3 with four
  circular instances in the regression fixture. Physical interaction remains 3.7.4.
  Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
  `pattern-model-results.json`, `pattern-gui-results.json`, `pattern-visual-check.json`,
  `pattern-linear.png`, `pattern-circular.png`, and `pattern-build-*.log`.
  The initial build found a task-header API mismatch, corrected to `setHeaderText`.
  The GUI harness invokes FreeCAD's unsigned count slot; using Qt's signed setter
  initially requested an excessive count, so that run was stopped and corrected.
  Final build/link and runtime reports supersede those intermediate failures.
  Source formatting, Python syntax, whitespace, and documentation checks pass.
  Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
  This is an incremental development build; its About/version stamp still reflects
  the earlier main-executable build, while the changed App/Gui modules are rebuilt.
- [   ] 3.7.4 Complete physical viewport/keyboard/high-DPI acceptance using
  [the Pattern procedure](../tests/PatternTaskPanel.md). Automated Qt interaction and
  captured layout inspection do not establish this manual gate.

Compatibility boundary: old Linear/Polar features keep their existing full editor;
there is no automatic conversion to the new type. Unmodified upstream FreeCAD does
not recognize `PartDesign::Pattern`; cross-version recomputation and release packaging
are not established. This work is local and does not authorize a push or publication.

### [   ] 3.8 Extrude start offset and direction controls

Outcome: REQ-013 is available in the shared new/edit Extrude pane for Pad and Pocket.
Existing signed StartOffset, StartType, and Reversed properties retain their model
semantics; no stored property or object migration is introduced.

- [ X ] 3.8.1 Expose the zero-default start offset in all three direction modes,
  automatically activate Offset when a distance is entered, and add a flip button
  that negates the value or its expression. Retain reference starts and explicit
  Profile plane reset.
- [ X ] 3.8.2 Replace the Reversed checkbox with synchronized buttons beside each
  length. Keep reversal beside Type for non-dimensional extents and disable it for
  symmetric Dimension. Keep the start-offset viewport gizmo available at zero.
- [ X ] 3.8.3 Rebuild the GUI module and run native geometry/task regressions; inspect
  the actual task-pane layout. Windows x64 Release GUI module rebuilt and linked
  using the existing MSVC/Qt LibPack environment outside Google Drive. All **42 GUI
  tests pass**: Extrude 16 (nine new cases), Pad 14, Pattern 12; no failures/errors/skips.
  Native tests assert positive/negative offset geometry in all three modes,
  Add/Subtract and legacy Pocket behavior, both synchronized length buttons,
  non-dimensional reversal, reference starts, expression flipping and rollback,
  save/reopen, Cancel, and Undo/Redo. Captured one-sided, two-sided, and symmetric
  task layouts were inspected; offset and length buttons align with their fields.
  Formatting, Python syntax, UI XML, whitespace, and documentation checks pass.
  Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
  `extrude-offset-gui-results.json`, `extrude-offset-visual-check.json`,
  `extrude-offset-one-side.png`, `extrude-offset-two-sides.png`,
  `extrude-offset-symmetric.png`, and `extrude-offset-build-*.log`.
  Final successful compile/link and tests supersede intermediate compile errors
  from a protected expression-widget API and a removed checkbox reference.
  Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
  Incremental GUI module update; the main executable About/version stamp still
  reflects its earlier build. The separately installed FreeCAD was not used.
- [   ] 3.8.4 Complete physical viewport/keyboard/high-DPI acceptance using the
  [Extrude procedure](../tests/PadTaskPanel.md#start-offset-and-direction-buttons).
- [ X ] 3.8.5 Verify Add/Subtract offsets across the full dimension-mode matrix.
  User-requested follow-up passed in the same source-built GUI: **72 geometry
  scenarios** (Extrude and legacy Pocket commands, Add/Subtract, one-sided/two-sided/
  symmetric, normal/reversed extrusion, and 0/+2/-2 mm offsets). Negative offsets
  use the real flip button. Each result is a valid single solid with the expected
  analytical volume, bounding box, and zero excess/missing volume against an
  independently constructed box union/cut. Accepted features reopen correctly;
  flipping after reopening and Cancel restore the expected solids. All **17 Extrude
  GUI tests pass**, including existing expression, reference, save/reopen, and
  Undo/Redo cases, with no failures/errors/skips. No implementation fix was needed.
  Evidence in the directory above: `extrude-offset-operations-gui-results.json`
  and `extrude-offset-operations-TestExtrudeTaskPanel.log`. Only tests/documentation
  changed for this follow-up; no binary rebuild was required.

This work is local; publication and release packaging are not part of this task.

### [   ] 3.9 Revolve/Groove angular start offsets

Outcome: REQ-014 in the shared Revolution (Add) and Groove (Subtract) create/edit
pane. This user-authorized angular-control change does not complete command/profile
consolidation in 3.6.4 or the broader Revolve/Groove workflow audit.

- [ X ] 3.9.1 Expose the existing signed StartOffset in all three side modes with
  default 0 degrees, inclusive -360/+360 endpoints, and automatic Offset activation.
  Add a sign-flip button preserving expressions and reference-start behavior.
- [ X ] 3.9.2 Replace Reversed with synchronized buttons beside each angular
  magnitude; keep reversal available for reference extents and disabled for
  symmetric angular sweeps. Keep the start-offset gizmo available at zero.
- [ X ] 3.9.3 Build and verify native geometry, controls, persistence, and task layout.
  Windows x64 Release PartDesignGui rebuilt and linked in the existing isolated
  MSVC/Qt LibPack environment. All **25 tests pass**: five new Revolve task tests,
  three existing Revolve model tests, and 17 Extrude task regressions; no failures,
  errors, or skips. The new suite includes **84 geometry scenarios** across Add and
  Subtract, three side modes, normal/reversed axes, and 0/+45/-45/+180/-180/+360/-360
  degree offsets. Independent cylindrical sectors verify analytical volume, exact
  bounds, and both geometric differences. Offset endpoints stay numerically +/-360
  through acceptance and reopening. Both buttons, zero default, range limits,
  expressions, reset/rollback, Cancel, Undo/Redo, and save/reopen pass for both types.
  Initial post-render bounds checks used display triangulation; corrected the test
  oracle to exact `optimalBoundingBox(False)` without relaxing geometric tolerances.
  Captured and inspected all three task modes for Revolution and Groove after Qt
  layout animations settled. Physical interaction remains task 3.9.4.
  C++ formatting, Python syntax, UI XML, whitespace, and documentation checks pass.
  Evidence: `D:\Temp\Office-PC\freecad-plus-validation-20260928`,
  `revolve-offset-gui-results.json`, `revolve-offset-visual-check.json`,
  `revolve-offset-add-*.png`, `revolve-offset-subtract-*.png`, and
  `revolve-offset-build-*.log`.
  Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
  Incremental GUI module update; the main executable About/version stamp still
  reflects its earlier build. The separately installed FreeCAD was not used.
  Follow-up user-requested verification on local commit `84c34732ef`: all eight
  focused tests passed (five Revolve task tests and three Revolve model tests),
  with **84 individually recorded geometry scenarios: 42 Add and 42 Subtract**.
  No failures/errors/skips and no implementation fix required. Source/build test
  copies matched; the existing development GUI module was used. Detailed report:
  `revolve-offset-verify-gui-results.json` in the evidence directory above.
- [   ] 3.9.4 Complete physical viewport, keyboard, and high-DPI acceptance using
  [the Revolve test procedure](../tests/RevolveTaskPanel.md).

This work preserves existing stored feature types and properties; command
consolidation, push/publication, and release packaging remain outside this task.


<a id="trim-body"></a>

## [   ] Phase 4: Associative Trim Body

Outcome: select a target solid/sheet, cutter, and side to keep in one complete
create/edit task, available from Part and Part Design. User-authorized scope;
requirements REQ-015 through REQ-017 and [UI-004](UI_UX_SPEC.md#ui-004-trim-body-task-pane).
Depends on: the existing Part geometry engine and native development build.

### [ X ] 4.1 Implement geometry and shared task

- [ X ] 4.1.1 Add a linked Trim Body feature reusing Part half-spaces, Boolean
  common/cut, and BOPTools SplitAPI. Support datum planes, planar/curved faces,
  connected sheets, solid/sheet targets, planar extension, and reversible keep side.
  Reject incomplete or nonintersecting cuts and invalid solid closure.
- [ X ] 4.1.2 Add Target then Tool selectors, side reversal and green viewport arrow,
  live preview, refine/planar-extension controls, and error recovery in one new/edit
  pane. Register the same command in both workbenches' menus and toolbars.
- [ X ] 4.1.3 Persist input links, track parent-container placement changes, and
  preserve transaction/visibility behavior. Keep source objects and Part Design
  Body Tip unchanged; the result is a separate Part::FeaturePython object.

### [   ] 4.2 Validate and prepare the local test build

- [ X ] 4.2.1 Rebuild/link PartGui and PartDesignGui menu/toolbar entries, install
  source-matching Python modules and icon into the existing Windows x64 Release
  build. The separately installed FreeCAD was not used. No new dependencies.
- [ X ] 4.2.2 Run native tests: **72 passed**, zero failures/errors/skips. Trim Body:
  14 model and 10 GUI tests; existing Pad 14, Extrude 17, Revolve 5, Pattern 12.
  Coverage includes analytical plane/cylinder/B-spline volumes and sheet areas,
  connected curved tools, finite-cutter rejection, closed solids, selection and
  both side buttons, datum planes, Body targets and nested placements, automatic
  tool-parameter recomputation, save/reopen, Cancel, Undo/Redo, and arrow cleanup.
  Fixed two issues found during development: finite planar half-spaces failed
  outside a small tool's bounds, and resetting edit before abort committed Cancel.
  Planar extension now uses an unbounded plane; Cancel aborts before resetEdit.
  A toolbar-test assumption was corrected after confirming the isolated profile
  intentionally hid Part Design toolbars; the test invokes the actual toolbar action.
- [ X ] 4.2.4 Inspect native task and window captures for planar, curved, and sheet
  targets in both keep directions. Controls fit and the green arrow reverses correctly.
  FreeCAD image export omits transient annotations, so arrow visibility was verified
  in native window captures. Saved an editable `TrimBodyExample.FCStd` in the evidence
  directory. Python formatting/syntax, SVG XML, whitespace and documentation checks pass.
- [   ] 4.2.3 Complete physical viewport selection, keyboard and high-DPI acceptance
  using [the test procedure](../tests/TrimBody.md). Automated Qt tests and captured
  layout inspection do not establish this manual gate.

Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`.
Native reports: `trim-gui-gui-results.json`, `trim-gui-TestTrimBody.log`,
`trim-gui-TestTrimBodyGui.log`, and existing-suite logs with the `trim-gui-` prefix.
Visual evidence: `trim-visual-check.json`, `trim-*-task.png`, and `trim-*-window.png`.
Build logs: `trim-build-Part-Workbench.log`, `trim-build-PartGui-link.log`,
`trim-build-PartDesign-Workbench.log`, `trim-build-PartDesignGui-link.log`.
Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Incremental modules are current; the main executable About/version stamp remains
from its earlier build. This task does not publish a release or push local commits.

Compatibility and geometry limits: one cutting tool, automatic extension for planar
boundaries only. Curved tools must fully span each trimmed region; automatic curved
Trim and Extend is future scope. Result recomputation needs the new BOPTools Python
modules. Upstream-only recomputation, Linux/macOS validation, and packaging are not
established. The output is associative but does not insert a new Part Design Body Tip.


<a id="isocline-curve"></a>

## [   ] Phase 5: Associative Isocline Curve

Outcome: trace a selected draft angle on one or more faces relative to an editable
pull direction. User-authorized scope; REQ-018 through REQ-020 and
[UI-005](UI_UX_SPEC.md#ui-005-isocline-curve-task-pane).
Depends on: the existing OpenCASCADE Part kernel and native development build.

### [ X ] 5.1 Implement contour geometry and complete editor

- [ X ] 5.1.1 Add the Part.makeIsocline binding around Contap_Contour, analytical
  curves and surface-parameter interpolation, clipping to trimmed faces and holes.
  Use draft convention normal dot pull = sin(angle), so 0 degrees is silhouette.
  Validate fit residual, suppress degenerate point output, report whole-face matches,
  and handle the limiting 90-degree cylinder line.
- [ X ] 5.1.2 Add the linked multi-face feature, axis/reference/custom direction,
  reversal, angle, live preview, and same create/edit pane. Register one command
  in Part's menu/Part Tools toolbar and Part Design's menu/Modeling Features toolbar.
- [ X ] 5.1.3 Reuse extracted ShapeReferences and FeatureTask helpers with Trim Body.
  Preserve stored Trim proxy names and input/transaction behavior. Both features
  track enclosing placements, preserve source objects and keep a separate result.

### [   ] 5.2 Validate the local build

- [ X ] 5.2.1 Rebuild/link Part's contour binding plus PartGui/PartDesignGui command
  entries and install the matching scripts and icon in the isolated Windows x64
  Release build. Existing MSVC/Qt/OpenCASCADE LibPack; no added dependency.
- [ X ] 5.2.2 Complete native model/task regressions and inspect task/viewport captures.
  **88 tests passed**, with no failures/errors/skips: Isocline nine model and seven
  GUI, Trim Body 14 model and 10 GUI, Pad 14, Extrude 17, Revolve five, Pattern 12.
  Geometry checks include analytical lengths, normal-angle residuals and distance
  to the trimmed source face, freeform closed loops, boundary contours, holes,
  direction reversal, face orientation, multi-face wires and 90-degree degeneracy.
  Persistence, parameter/placement recomputation, picking, invalid recovery,
  paused preview, Cancel and Undo/Redo passed. Actual toolbar actions work in both
  workbenches; the test now allows FreeCAD's delayed enablement timer to settle.
  Visual inspection found a degree-symbol encoding issue and surface tessellation
  obscuring freeform lines. Fixed the symbol and added a transient curve highlight;
  the same 17 Isocline/Trim GUI tests passed after those presentation changes,
  including annotation cleanup. Native window captures verify readable controls,
  red curves and the reversing green arrow. Source geometry stays unchanged.
  Python/C++ formatting, syntax, SVG XML, whitespace and documentation checks pass.
  Saved editable sphere and freeform examples in the evidence directory below.
- [   ] 5.2.3 Complete physical viewport selection, keyboard and high-DPI acceptance
  using [the Isocline test procedure](../tests/IsoclineCurve.md). Automated Qt controls
  and window captures do not establish this manual gate.

Evidence: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
`isocline-gui-gui-results.json`, `isocline-gui-Test*.log`,
`isocline-visual-tests-gui-results.json`, `isocline-visual-check.json`,
`isocline-*-task.png`, `isocline-*-window.png`, and `isocline-build-*.log` /
`isocline-gui-build-*.log`. Examples: `Isocline-sphere-example.FCStd` and
`Isocline-freeform-example.FCStd`. Launcher:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Incremental Part/GUI modules are updated; the main executable About stamp remains
from its earlier build. The separately installed FreeCAD was not used.

Compatibility/scope: one angle per feature; source faces and Body Tips are preserved.
A result may have several connected wires. Empty, isolated-point and whole-face
solutions do not invent an isocline. Arbitrary-surface completeness is not proven
by sampled residual checks. Splitting bodies/faces, multiple stepped angles,
Linux/macOS validation, packaging, push and publication remain outside this task.
Recomputation requires the new Python modules and native Part API in FreeCAD Plus.


<a id="cam-mesh-machining"></a>
## [   ] Phase 6: STL CAM and holding tabs

User request: direct STL Parallel/Waterline machining similar to MeshCAM, with
simple tabs that toolpaths automatically avoid, including two-sided/indexed
machining. Separate manually indexed jobs share model/stock/tab transforms and
have independent origins. Implementation, build and automated workflow checks
are complete. Native acceptance and simulation remain pending; automatic
rotary-axis output is outside this implementation.

### [ X ] 6.1 Direct mesh workflow

- [ X ] 6.1.1 Accept and clone STL job models associatively; compute stock and placement without facet-to-BRep conversion.
- [ X ] 6.1.2 Use every mesh/CAD model in Parallel and Waterline generation; expose the command without experimental preference flags.
- [ X ] 6.1.3 Validate actual STL import, placement, both strategies, mesh edits and save/reopen in the CAM-enabled build.

### [   ] 6.2 Geometric holding tabs

- [ X ] 6.2.1 Add the shared create/edit pane, numeric dimensions and viewport placement; preserve transactions and document links.
- [ X ] 6.2.2 Protect tab stock across supported cutting/link moves using the cutter radius; reject unsupported strategies and unsafe heights without stale paths.
- [ X ] 6.2.3 Validate narrow crossings, rotated/overlapping bridges, operation recompute, Cancel/Undo/Redo and saved documents.
- [   ] 6.2.4 Complete native visual/viewport acceptance and record a representative simulation review. No machine cutting validation is implied by software tests.

### [ X ] 6.3 Build and validation

- [ X ] 6.3.1 Enable CAM, Draft, MeshPart and required dependency modules in the external development build.
- [ X ] 6.3.2 Run focused CAM and relevant existing regressions; record runtime/source identities and remaining limitations.
- [ X ] 6.3.3 Commit and push the validated milestone to origin; verify the remote branch.
  Evidence: `648cff214ca78e1d8b3d72d87d6053e103390c60` pushed to `origin/main`;
  `git ls-remote` returned the same hash. No release or installer was published.

### [   ] 6.4 Two-sided and indexed setups

- [ X ] 6.4.1 Define setup orientation, work origin, stock and part references for each side/index; distinguish manual indexing between jobs from controller-driven indexing.
- [ X ] 6.4.2 Preserve the same physical holding tabs across transformed setups; propagate tab edits and invalidate every affected path.
- [   ] 6.4.3 Validate opposing faces and a non-orthogonal index, coordinate transforms, stock registration, tab clearance, safe linking moves and per-setup output.

Evidence, 2026-09-29 (external root `D:\Temp\Office-PC\freecad-plus-validation-20260928`):

- The first build was cancelled at the user's request. The resumed build linked
  its modules but did not capture an exit code. The incremental completion build
  passed with exit 0: `cam-completion-build-result.json`; final script targets
  also exited 0 (`cam-final-scripts.log`).
- `cam-tests-20260929-184049`: all 22 `TestMeshMachining` cases passed with no
  skips and process exit 0. Includes STL curved-surface height checks, layered
  Waterline, mixed translated mesh/CAD models, tab clearance and block-delete
  annotations, persistence, 180/45-degree indexing, shared-tab propagation,
  task transactions, indexed-stock refresh and command availability.
- `cam-tests-20260929-183855`: the seven related suites ran 113 cases: 112 passed,
  none failed/errored, one skipped. Suites: `TestPlanarSurfaceOp`,
  `TestSurfaceMeshGenerator`, `TestPathStock`, `TestPathDressupHoldingTags`,
  `TestPathOpUtil`, `TestPathUtil`, `TestPathSharedWorkplane`. The optional
  simplification test skipped because `fast_simplification` is unavailable.
  The strict aggregate marker is FAIL due to that skip, not a test failure.
- `cam-validation-manifest.json`: all 15 installed changed CAM Python files
  match source; five binary hashes recorded. The application still reports its
  historical native stamp `8abce719de` (26.3.0dev, revision 49009); this stamp is
  not the identity of the new Python implementation. Use the manifest and commit.
- Native mouse/viewport acceptance, representative material-removal simulation,
  and per-setup postprocessor review remain open (6.2.4 and 6.4.3). Automated
  indexed geometry/path checks pass; they do not establish machine/fixture safety.


<a id="nx-feature-history"></a>
## [   ] Phase 7: NX-style unified feature history ? first priority

Outcome: one ordered feature history for a model part, with sketches, datums,
linked/cloned geometry and modeling features available independently of a single
Body. Users do not have to create or activate a Body before modeling. Solid/sheet
bodies remain real geometric results with stable identities; they are not the
mandatory organizing containers for every input and feature. An assembly has a
history per component/model part, not one interleaved history for every component.

This is the user's desired behavior, not a statement that current FreeCAD supports
it through a tree preference. A flattened navigator is only the first visible step.
Backend ownership, feature inputs/outputs and reference rules must support the same
workflow. Reuse native FreeCAD capabilities where their semantics fit; do not hide
an unchanged single-body restriction behind a different-looking tree.

Implementation order: 7.1?7.3 establish the model and navigator; 7.4 delivers the
first end-to-end Extrude/Revolve workflow; 7.5?7.7 make history editing and adoption
safe. Existing Phase 2/3 implementation and tests are inputs, not work to recreate.

### [   ] 7.1 Define the part-level history and body model

- [   ] 7.1.1 Specify a single ordered History list and a separate Bodies/results list. Define feature, sketch, datum, curve, imported object, linked object, solid body and sheet body roles.
- [   ] 7.1.2 Map current Part, Part Design Body/Tip, feature ownership, attachment and document-link restrictions to the proposed model. Identify which changes are presentation only and which require model/API changes.
- [   ] 7.1.3 Prototype native Body adapters versus a part-level feature/result layer. Evaluate multi-body outputs, shared inputs, references, recompute, persistence and upstream compatibility before choosing the architecture.
- [   ] 7.1.4 Define stable feature and body identities, explicit input/output links, and lineage when bodies merge, split, disappear or reappear after an edit. Keep display order distinct from dependency evaluation order.
- [   ] 7.1.5 Document the chosen architecture, migration boundary and a small reference model; update product/UI specifications before production implementation.

Complete when: a prototype demonstrates one independent sketch driving features
on two bodies, one feature producing multiple bodies, and a later feature using
results from both, without silently duplicating sketches or losing references.

### [   ] 7.2 Build the unified history navigator

- [   ] 7.2.1 Add a part-level History view containing sketches, datums, linked geometry and features in modeling order. Show shared inputs once, with discoverable consumers, instead of nesting them exclusively under one body.
- [   ] 7.2.2 Add a Bodies/results view showing current solids and sheets, with source-feature links, names, visibility and selection. Body hiding must not suppress generating features.
- [   ] 7.2.3 Synchronize navigator selection and viewport highlighting; provide Find in History, Find Result, Show Parents and Show Dependents.
- [   ] 7.2.4 Provide search, type/status filters, user folders and meaningful names. Folders organize display without changing geometry ownership or recompute order.
- [   ] 7.2.5 Retain access to the native document tree for legacy documents and diagnostics. A view change must not migrate or rewrite a file by itself.

### [   ] 7.3 Make sketches and reference geometry independent

- [   ] 7.3.1 Create sketches on principal planes, datum planes or selected faces without requiring a Body. Preserve attachment, placement, units and expressions.
- [   ] 7.3.2 Allow one sketch or curve source to feed multiple features and bodies. Distinguish whole-sketch, region and curve-chain selection; define open/closed profile rules per operation.
- [   ] 7.3.3 Put datums, construction geometry and imported geometry at part scope, with explicit dependencies rather than incidental active-body ownership.
- [   ] 7.3.4 Add complete create/edit definitions for associative copies, clones and linked references: source, transform and update behavior. Keep independent copies a separate explicit choice.
- [   ] 7.3.5 Validate cross-body reuse, source replacement, moved references, circular-dependency rejection, Cancel and save/reopen without automatic destructive reparenting.

### [   ] 7.4 Automate body creation and target selection

- [   ] 7.4.1 Extend the existing Extrude and Revolve task workflows to start in an empty part without a declared/active Body. Keep Operation as the first field, followed by profile, target/result controls and parameters.
- [   ] 7.4.2 For Add with automatic targeting, create a new solid body when the generated solid has no valid volumetric overlap with an existing eligible solid. With exactly one eligible intersecting target, preview adding to that target.
- [   ] 7.4.3 If multiple bodies intersect, show and highlight candidate targets; require an explicit target set or New Body choice. Never choose a target by incidental tree order or visibility.
- [   ] 7.4.4 Provide an explicit New Body override even when geometry overlaps. For Subtract and Intersect, require valid target bodies and report a nonintersecting/empty result rather than creating an unintended body.
- [   ] 7.4.5 Define tangency, face/edge contact, coincident geometry, tolerances, disconnected profile regions, sheet results and multi-solid outputs. Make automatic decisions inspectable in the preview.
- [   ] 7.4.6 Persist target intent and body lineage. When editing an earlier feature changes overlap, report any target change; do not silently cut/join a different body or break downstream identity.
- [   ] 7.4.7 Reuse this result/target policy for Loft, Sweep, Helix, primitives and Boolean operations after the Extrude/Revolve pilot passes. Retain legacy command/API entry points.

First deliverable: open a new document, draw a sketch, Extrude without creating a
Body, then create a disconnected Extrude and obtain a second body. Reuse the first
sketch for another feature, modify one selected body with Subtract, and reopen each
feature in the same complete task pane. Repeat the body-creation cases with Revolve.

### [   ] 7.5 Add history editing, rollback and recovery

- [   ] 7.5.1 Add Make Current / rollback and return-to-end controls; show the exact intermediate body results and disable later features for the rollback preview without deleting them.
- [   ] 7.5.2 Insert new features at the current history position and update the dependency graph consistently. Restore the prior position and geometry on Cancel.
- [   ] 7.5.3 Support safe reorder/move with dependency validation and a clear explanation of prohibited moves; never treat arbitrary tree drag order as a valid modeling history.
- [   ] 7.5.4 Add suppress/unsuppress with explicit downstream status. Distinguish suppression, visibility, inactive setup and failed recompute.
- [   ] 7.5.5 Preview deletion effects and offer valid dependent-feature handling. Provide broken-reference repair and Replace Input within the complete feature editor.
- [   ] 7.5.6 Keep feature edits, target changes, body creation/removal and history-position changes atomic for Cancel and Undo/Redo; recover from recompute failures without displaying stale success.

### [   ] 7.6 Preserve documents and external consumers

- [   ] 7.6.1 Build a compatibility matrix covering existing upstream files, existing Plus files and new history-model files: open/display, edit, recompute and round-trip save are separate checks.
- [   ] 7.6.2 Version any new persisted model and provide opt-in conversion with an untouched original. Opening a legacy file must not force migration.
- [   ] 7.6.3 Preserve existing type/property names and Python entry points where possible. Document any new feature modules required for recomputation; do not promise upstream compatibility for backend changes without evidence.
- [   ] 7.6.4 Define explicit neutral-geometry export as an exchange option, including loss of editable history. Never replace the editable original with a flattened export automatically.
- [   ] 7.6.5 Audit Assembly, TechDraw, CAM, expressions, links and scripts that currently resolve a Body Tip. Provide stable result references and invalidation behavior for the new history model.

### [   ] 7.7 Validate and release the history pilot

- [   ] 7.7.1 Create regression fixtures for empty-part creation, disconnected solids, shared sketches, multiple intersecting targets, merge/split lineage, nested placements and legacy documents.
- [   ] 7.7.2 Test geometry, dependency recompute, references/expressions, rollback, reorder, suppression, deletion, Cancel, Undo/Redo and save/reopen, including edits that change the number of output bodies.
- [   ] 7.7.3 Run native mouse/keyboard acceptance for navigator and viewport selection, history insertion, create/edit parity and ambiguous-target recovery.
- [   ] 7.7.4 Compare recompute time and navigator responsiveness on small and larger multi-body histories; define measurable acceptance thresholds before declaring performance complete.
- [   ] 7.7.5 Supply a testable build and example document, record compatibility limitations, and retain a reversible opt-in until the pilot passes. Track source, build, tests, user acceptance and GitHub push separately.

<a id="nx-modeling-workflows"></a>
## [   ] Phase 8: Consistent NX/SolidWorks-inspired modeling workflows

Depends on the applicable Phase 7 model/result contracts. Shared task-pane work
that preserves current model semantics may proceed independently when separately
authorized. Phase 3 remains the canonical operation inventory; do not duplicate its
implementation or mark its unfinished validation complete through this plan.

### [   ] 8.1 Standardize the complete feature task

- [   ] 8.1.1 Define one shared task order: operation/type, input collectors, target bodies, geometry parameters, direction/extents, preview and acceptance. Hide only genuinely inapplicable controls.
- [   ] 8.1.2 Apply command-first selection and identical create/edit coverage to the Phase 3 audit, including profile/section/path/axis replacement after reopening a feature.
- [   ] 8.1.3 Standardize named selection collectors with add/remove/clear, viewport/tree picking, compatible-type filters, chain/region selection and visible invalid-reference feedback.
- [   ] 8.1.4 Standardize signed offsets, adjacent direction buttons, one/two-sided and symmetric modes, units and expressions. Preserve parameters by meaning when switching operation or type.
- [   ] 8.1.5 Add consistent live-preview and error states; make Cancel restore geometry, visibility and selection. Define Apply/repeat behavior separately from OK so repeated creation does not create accidental features.

### [   ] 8.2 Finish unified command families

- [   ] 8.2.1 Complete the existing Extrude and Linear/Circular Pattern acceptance gates, then adapt them to part-level results and reusable inputs without regressing legacy features.
- [   ] 8.2.2 Combine Revolution/Groove as Revolve with Add/Subtract, retaining angular offsets and direction controls; add automatic/new-body handling from 7.4.
- [   ] 8.2.3 Implement unified Loft, Sweep and Helix from milestone 3.6, retaining ordered sections, path/orientation controls and family-specific validity rules.
- [   ] 8.2.4 Consolidate primitives into a shape selector plus operation/target controls. Define parameter and identity behavior before allowing an existing primitive to change shape type.
- [   ] 8.2.5 Extend Pattern deliberately to Mirror and supported path/point patterns; distinguish repeating features, whole bodies and geometry copies, with clear result scope.
- [   ] 8.2.6 Align Boolean, Trim and future Split workflows with common target/tool collectors and keep/discard previews. Keep Hole, Draft, Shell/Thickness and edge treatments specialized where their parameters differ.

### [   ] 8.3 Improve sketch-to-feature interaction

- [   ] 8.3.1 Create or edit a sketch from a feature's profile collector and return to the same pending feature task, with clear transaction and cancellation behavior.
- [   ] 8.3.2 Preview selectable enclosed sketch regions and curve chains; explain gaps, self-intersections and ambiguous regions before attempting a solid operation.
- [   ] 8.3.3 Define consistent sketch orientation, origin, normal and attachment controls, plus associative projected/intersection geometry across bodies.
- [   ] 8.3.4 Test shared-sketch edits across multiple consumers and provide dependency feedback before changes invalidate downstream features.

### [   ] 8.4 Make the modeling interface consistent

- [   ] 8.4.1 Define a coherent Modeling command set across current Part/Part Design boundaries. Route by valid inputs/results rather than requiring users to change workbenches to find equivalent operations.
- [   ] 8.4.2 Add searchable command names and familiar aliases, contextual right-click actions, predictable double-click editing and discoverable shortcuts; retain legacy names for scripts and compatibility.
- [   ] 8.4.3 Define viewport manipulators for direction, extent, offset and placement that update the same task properties and expressions as numeric controls.
- [   ] 8.4.4 Add consistent face/edge/body/reference selection filters, hide/show/isolate and preview colors. Verify keyboard focus, accessibility, high DPI and selection restoration.
- [   ] 8.4.5 Run end-to-end modeling scenarios with the user and record friction points before replacing additional standard commands or making the new interface the default.

<a id="nx-downstream-workflows"></a>
## [   ] Phase 9: Extend the unified workflow to downstream work

These are follow-on planning tasks, not authorization to implement every NX or
SolidWorks capability. Prioritize after the feature-history pilot and review the
specific interactions with the user before detailed implementation.

- [   ] 9.1 Plan history-based Move/Offset/Delete/Replace Face for imported and native solids, with previews, repair limits and stable downstream result references. Treat direct edits as explicit features in history.
- [   ] 9.2 Define surface-to-solid workflows for trimmed sheets, sewing and thickening, including body type changes and references to Trim Body/Isocline results.
- [   ] 9.3 Integrate component placement, associative linked parts and in-context references with per-part histories; define external-reference updates and cycle prevention before adding assembly-edit shortcuts.
- [   ] 9.4 Update drawings and dimensions to consume stable body/result identities, with explicit repair when a feature edit removes a referenced face or body.
- [   ] 9.5 Connect CAM model and stock references to the unified results; invalidate paths after relevant history edits. Incorporate Phase 6's required two-sided/indexed setups and shared physical tab geometry when CAM work is resumed.
- [   ] 9.6 Define named configurations/variants for dimensions and feature suppression, including persistence, downstream drawings/CAM and recompute cost, before exposing configuration controls.
- [   ] 9.7 Build representative end-to-end examples: shared-sketch multi-body modeling, imported-part editing, assembly/drawing updates and two-sided machining. Record each product area?s independent acceptance and compatibility gates.
