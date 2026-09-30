# FreeCAD Plus: Development Roadmap

## Current focus

- Current batch: 7.1.3f attached-profile and 16.2a TechDraw dimension probes
  complete. All 24 grouped history/intent/consumer checks pass in the existing fork;
  no installed source or native build changed. These are bounded compatibility
  proofs, not a production history UI or general topology-reference guarantee.
  Next: split/merge lineage, missing/ambiguous drawing references, CAM path/FEM
  consumers and production target discovery before the parent gates can close.
- Previous batch: 10.1 and 10.3a/10.3b reconciled contracts and proved transient
  proposals versus committed operation intent with 22 grouped passing checks.
- Version 2 objectives remain in the [coverage register](#version-2-objective-coverage);
  the expanded portfolio is pending except for specifically evidenced subtasks.
- Previous batch: Phase 7 placement/occurrence/consumer comparison, 2026-09-29.
  Completed 7.1.3c/7.1.3d/7.1.3e: transformed inputs, an assembly-local cut,
  and a production fix for stale Draft clone/CAM job-model geometry.
  All 88 grouped history, Draft and CAM checks pass in the existing application;
  Python-only update, no native build. History adapters remain test-only.
  Next: lineage, transformed attachments and remaining consumers for 7.1.3 and decisions in
  7.1.5/7.1.6 before production navigator/model changes. Batch two or three related
  implementation tasks before any costly build, as requested by the owner.
- Previous implementation: [prioritized upstream issue work](#upstream-issue-work).
  Latest freeform fix: U.23 bypasses the reproduced #26300 exact-projection stall
  using tolerance-controlled mesh silhouettes. The fixture generates in 14 seconds;
  all 91 CAM checks pass without a rebuild. U.15 cancellation acceptance remains.
  Latest boundary correction: avoidance no longer uses a fallback that fills
  selected holes after projection fails; U.22 records 81 passing CAM checks.
  Latest geometry fix: #6864 final-strip coverage now passes in the compiled
  replacement generator; U.21 records the 77-test CAM batch.
  Latest safety fix: partial boundary projection/union can no longer drop selected
  regions; U.20 records 14 focused and 59 related passes without a build.
  U.19 retains the original #26300 timeout evidence, superseded for generation by
  U.23. Modern CAM avoidance now stops on boundary failures or unsupported
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
  user's preferred FreeCAD Plus workflow, drawing on NX and SolidWorks. The owner
  has now requested roadmap execution; proceed in dependency order and preserve
  the architecture/compatibility gates. Planned items do not imply product parity.
- [Phase 6: STL CAM and holding tabs](#cam-mesh-machining) is implemented and built.
  All 22 focused automated tests pass; related regressions have 112 passes and one
  optional dependency skip. Native acceptance and simulation remain pending.
  Two-sided/indexed machining uses separate manually indexed jobs.
  The NX-style history foundation is underway; production history remains pending.

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

<a id="planning-baseline-adoption"></a>
## Planning baseline adoption and version 2 reconciliation

The owner requested adoption of two supplied documents. Execution guidance is in
[DEVELOPMENT_GUIDELINES.md](DEVELOPMENT_GUIDELINES.md); the complete supplied
[FREECAD_PLUS_DEVELOPMENT_ROADMAP.md](archive/FREECAD_PLUS_DEVELOPMENT_ROADMAP.md)
is preserved as a historical reference. The owner subsequently supplied
`UPDATED_FREECAD_PLUS_DEVELOPMENT_ROADMAP.md`, version 2.0 (document updated date:
2026-09-30), and requested all additional objectives in this active roadmap.
The expanded inventory and concrete tasks below now own that backlog; the original
archive no longer defines its full scope. Supplied P0-P11/feature IDs are mappings,
not replacements for stable local task IDs. Estimates remain planning hypotheses.

This adoption imports desired objectives, not the attachment's embedded agent
startup assignment: retain PROGRAMMING_SUMMARY.md, this roadmap, WORK_STATE.md and
existing architecture records. Do not restart the fork, repeat established builds,
or create a second status ledger. Preserve existing evidence and batch two or three
related implementation tasks before costly build validation. Optional items remain
optional; no release, outreach, registration, rename or billing action is authorized
by listing it. The desktop application is planned to remain free of charge for the
foreseeable future, without subscriptions, activation or paid core feature gates.

Version 2's visible, overridable New Body/Unite suggestion policy supersedes the
unconditional New Body proposal and the unresolved-default wording in earlier
planning documents, including DEVELOPMENT_GUIDELINES.md. Task 7.4.8 records the
planning decision; its implementation remains open. Synchronize the owning product,
UI and guideline contracts in 10.1 before migrating commands. Preserve the owner's
operation-first task layout: guided prompts can advance through unresolved inputs
without relocating that first field. Retain Pocket/Groove as shared-command presets.
FreeCAD Plus remains the working name; evaluating a rename is optional.

| Supplied phases | Existing owner / integration rule |
| --- | --- |
| P0 / G0 baseline | Phase 1, consolidated validation and Development Guide. Reuse recorded builds/tests; audit only missing or invalidated evidence. No claim that the entire expanded G0 is satisfied. |
| P1-P3 / G1-G3 architecture | Phase 7. Decide contracts, prove the mixed-part/shared-occurrence pilot, then migrate. Include assembly-local effects, topology ambiguity, legacy documents and drawing/CAM/FEM consumers. |
| P4-P5 / G4-G5 modeling and sketches | Phases 3 and 8. Preserve implemented Extrude/Pattern/offset work; migrate behind stable contracts. New selection conventions require reconciliation with input collectors. |
| P6 / G6 assemblies | Phases 7 and 9. Shared versus local editing, reference sets, replacement, external links and load-state semantics remain planned. |
| P7 / G7 geometry portfolio | Phases 3-5 and 8. Trim and Isocline already have implementation/test evidence; advanced surfaces/direct editing remain candidates. Do not recreate completed work. |
| P8 / G8 mesh CAM | Phase 6. Preserve Parallel/Waterline, holding tabs and the user's two-sided/manually indexed requirement. Roughing, rest machining, simulation/post gates remain separate; three-axis wording does not drop indexed setups. |
| P9 / G9 downstream | Phase 9; preserve all supplied inventory rows as future candidates, activating bounded tasks only within authorized scope. |
| P10 / G10 maintenance | Upstream issue work, Phase 16 and release gates in the Development Guide. Local fixes/builds are not releases. |
| P11 / G11 onboarding | Phase 17: starter models, tutorials, independent-fork positioning and measured user adoption; external publication requires separate authorization. |

The [version 2 coverage register](#version-2-objective-coverage) gives every supplied
inventory ID a concrete task and status. Do not maintain parallel status in archived
files. Guideline B01-B10 benchmark IDs are user-task fixtures, distinct from the
assembly inventory IDs; the supplied T01-T12 benchmark register is retained below.
Usability/performance thresholds and effort estimates require measurements.

- [ X ] 1.3 Adopt the supplied agent guidance and map it to existing document owners.
  Evidence: guidelines and complete planning reference retained; root/index/guide
  links and future product direction updated. Documentation-only; no application
  behavior, build evidence or prior completion markers changed.
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
- [   ] U.14 #27950: exact GeomFillSurface integration remains pending for a
  batched build with Surface enabled (`BUILD_SURFACE=OFF` currently). Attachment
  inspection found no GeomFillSurface object: Base selects Clone.Face3 and
  Part__Mirroring.Face3 (mirrored Pad geometry). Saved BReps from that attachment
  generate a nonempty path in PlanarSurface, without restoring legacy proxies.
  This proves generation, not full attachment coverage or legacy backend repair.
  A generated non-planar B-spline exclusion independently passes cutting-segment
  exclusion and coverage-on-both-sides checks. Do not generalize to arbitrary
  freeform faces or mark the upstream issue closed.
- [   ] U.15 #26300: freeform generation corrected and geometry-validated in U.23;
  native task cancellation acceptance remains pending. The replacement operation
  was affected (U.19), so UI changes did not obsolete this backend issue. U.23
  preserves the existing outer cutting silhouette, separate avoidance holes,
  selected regions and cutter offsets; no bounding-box substitution or dropped
  failed faces. Legacy Surface applicability and machine/post acceptance remain
  separate. Do not mark the whole upstream report closed from the modern replay.
- [ X ] U.16 #6864: reproduced missing transverse edge passes in the current
  C++ Line generator, so the replacement UI/backend did not obsolete the defect.
  Add clipped finishing passes at each contour's transverse limits while retaining
  the regular stepover grid. Validate nonintegral/exact step ratios, separate
  regions, rotated masks, reverse order, and excluded holes. U.21 records the
  installed module and passing CAM batch. This is a modern-generator correction;
  saved legacy Surface operations and machine/post acceptance remain separate.
- [ X ] U.17 CAM avoidance fix published as
  `b2cfdf0f114ff2cba48004fe538991395b22f525`; `origin/main` hash verified. No release.

- [ X ] U.18 Extend #27950 applicability evidence with saved attachment geometry
  and a generated curved-face regression. `tests/TestIssueSurfaceAvoidance.py`
  now has nine passing checks; opt-in `tests/TestIssue27950Fixture.py` adds one.
  `curved-avoidance-20260929-final/results.json` under the external root below:
  10 PASS, no failures/errors/skips, process 0. Installed surface_common.py and
  PlanarSurface.py bytes match source and the U.13 recorded hashes. No app code
  changed or rebuild performed. Initial exact-object probe stopped with missing
  Surface module; that run is not acceptance evidence. Next actionable case U.15;
  retain the exact-object gap in U.14 for the next relevant batched build.

- [ X ] U.19 Reproduce and locate #26300 in the replacement workflow. Original
  attachment Clone BRep, saved placement, nine selected faces, 5 mm endmill,
  1 mm sampling, 5% stepover and saved depths exceed the isolated 120-second limit.
  Modern face masking replaces the removed legacy BoundaryEnforcement property;
  this is not an exact legacy-UI replay. A separate 55-second trace records
  Path.Area.getShape in surface_common._boundary_via_area at both 20 and 40 seconds,
  called while generating the selected-face mask. No OCL crash was observed.
  Individual projection plus planar union passed four simple geometry controls but
  failed on narrow trimmed faces; adding selected neighbours also stalled. Both
  candidates were removed, and source/installed module restored to committed code.
  This completes diagnosis only, not U.15 or the upstream issue.
  Evidence under the external root: `freeform-20260929-modern` (120-second timeout),
  `freeform-20260929-trace` (stacks and 55-second timeout), and
  `issue26300/diagnosis.json`. `tests/RunIssue26300.ps1` and the opt-in fixture test
  retain the reproduction without adding a hanging test to the default suite.
  Runner deadline behavior checked with a 30-second limit in
  `freeform-20260929-runner`; TIMEOUT is the expected diagnostic result, not PASS
  for toolpath generation. No native build, machine/post validation or release.
  Restored surface_common.py matches HEAD after CRLF normalization; source and
  installed SHA-256 now both
  `972F399E92F0509E4023556B4C057823429BBF9292652C51F4F13CE8B8CA097B`.
  The difference from U.13's raw hash is line endings only; no application change.

- [ X ] U.20 Stop partial-region fallback in build_optimized_boundary (#27950 /
  #27751). Inspection during U.15 found that a failed isolated face or connected
  group was silently omitted and failed union returned only the first boundary.
  This still affects the modern workflow and can remove requested keep-out areas;
  its wrong-toolpath impact takes priority over continuing projection experiments.
  Raise on missing/null/invalid region boundaries and failed/null/invalid union.
  Preserve all valid regions; the existing operation error path clears old paths.
  Five new checks cover isolated/group projection failure, union failure, valid
  disconnected exclusions and actual two-selection operation failure/stale-path
  clearing. Source and installed Python module SHA-256:
  `49647EC67FF15C603F341A71807640BB936E8C0FF0106632218AAD8B2EBB6003`.
  Evidence under the external root: `boundary-regions-20260929-red/results.json`
  reproduces three missing-error failures. `boundary-regions-20260929-green/results.json`
  has 59 related passes but an aggregate FAIL due to one exhausted mock in the
  new integration test. After making the fault repeatable across recomputes,
  `boundary-regions-20260929-focused/results.json` has all 14 focused checks PASS,
  no errors/skips. Application source unchanged between those two validation runs;
  together they establish 73 passing focused/related checks, not one all-pass batch.
  Python-only update installed; no native rebuild, schema change, legacy migration,
  or release. #26300 remains unresolved; U.14 and U.16 remain open.

- [ X ] U.21 Build and validate the bounded #6864 generator correction. Compiled
  only surface_generator.cpp using SelectedFiles, then relinked the existing CAM
  module; both commands exit 0. No full application/dependency rebuild. Added four
  regressions in TestIssueLineCoverage.py and replaced the older fixed-line-count
  expectation with endpoint/maximum-step checks. The regular grid alone missed
  1-5 mm at edges in the red fixtures. Additional passes sit at most 1e-6 mm inside
  contour extrema to accommodate the existing ray-cast boundary convention and
  still clip against the complete mask. No property/schema/default changes.
  `line-coverage-20260929-red/results.json` reproduces the defect;
  `line-coverage-20260929-final/results.json` reports 77 PASS, zero failures/errors/
  skips: 4 coverage, 14 avoidance, 12 common, 7 pattern, 18 operation and 22 mesh/tab.
  `line-build-20260929/build-result.json` records compile/link results and hashes.
  Installed `build/Mod/CAM/surface_generator.pyd` SHA-256:
  `B2BE185547170EB303508300A8B5639B9C301ABDFACDCD1BD0B364D101B65B94`.
  Updated TestSurfacePatternGenerator.py synchronized and hash-verified. Existing
  application version stamp remains unchanged. Default issue macro now includes
  the four coverage cases (93 tests); the full default has not run as one batch.
  This does not certify arbitrary contour finishing, legacy Surface, simulation,
  postprocessor output or physical machining. #26300 and exact U.14 remain open.

- [ X ] U.22 Reject lossy avoidance-outline fallback (#27950 / #27751 review).
  The replacement workflow still called TechDraw.findShapeOutline after failed
  hole-preserving projection. That API returns only an outer wire, silently
  filling holes in the exclusion and removing intended machining coverage.
  Unified UI changes do not obsolete this backend path. Now raise an actionable
  error before that fallback and clear the old operation path. Successful primary
  avoidance projection and outer-only cutting-outline fallback remain available.
  This deliberately rejects all avoidance requests that reach the lossy fallback,
  including triangulated avoidance inputs routed there; no general replacement
  projection algorithm is claimed. Direct STL machining/tab regressions still pass.
  Four added checks cover a holed selection, successful primary hole preservation,
  outer-outline fallback, and stale-path removal in a real operation. Two fail
  before the correction in `avoidance-fallback-20260929-red/results.json`.
  `avoidance-fallback-20260929-final/results.json`: 81 PASS, no failures/errors/skips
  (18 avoidance, 4 line coverage, 12 common, 7 pattern, 18 operation, 22 mesh/tab).
  Python-only update installed in the existing fork; no native build. Final
  docstrings synchronized after testing; executable statements unchanged.
  Source/installed surface_common.py SHA-256 in `module-manifest.json`:
  `0E23CD3491979F4346D21FC6FE3FDBDFA504D3AEFE057296F3147AF932F4D556`.
  Default issue macro now contains 97 tests; the entire default was not run as
  one batch. Exact U.14 GeomFillSurface and U.15 freeform timeout remain open.
  No legacy operation migration, postprocessor/machine acceptance or release.

- [ X ] U.23 Correct the reproduced #26300 freeform projection stall in the modern
  cutting-boundary pipeline. B-spline/Bezier selections use per-face tessellation
  at the operation's LinearDeflection, consistently oriented XY triangle union,
  and one offset per connected input group. Reuse Path.Area's NonZero polygon
  union without exact HLR or quadratic triangle nesting. Fill cutting-outline
  holes as Outline=True already did; explicit avoidance is subtracted separately.
  Failed face meshing, empty/invalid projection and invalid tolerance raise rather
  than dropping geometry or retrying the stalled exact projector. Non-freeform
  and avoidance projection remain on their existing paths. No new dependency,
  property, saved type or native build.
  Nine new analytic/fault checks cover seams, overlaps/reversed faces, islands,
  curved silhouette extrema, hole/avoidance behavior and failed/edge-on meshes.
  The original fixture now also verifies valid nonempty masks and every XY cutting
  endpoint inside the mask. `freeform-boundary-20260929-final/results.json` reports
  91 PASS, no failures/errors/skips: 9 boundary, 1 fixture and the prior 81 CAM
  checks. `freeform-details.json`: 14.05 seconds generation, 4,475 commands,
  4,235 G1 commands, 4,118 checked cutting endpoints, mask area 1336.60025 mm2.
  Baseline exceeded 120 seconds (U.19). The full fixture test also spends time on
  geometric assertions; elapsed generation is not whole-suite runtime.
  Earlier triangle-wire nesting timed out; a direct libarea experiment canceled
  overlaps under EvenOdd filling. Both failed candidates were discarded; overlap
  and sphere controls reject them. Retained implementation uses NonZero union.
  Source/installed surface_common.py SHA-256 in `module-manifest.json`:
  `873FA60DA4BDB414A1749219C8EBEC084F42DECBD55A33E537CD414009CB8D0C`.
  Default issue suite now has 106 tests; external-fixture test stays opt-in.
  Full default suite was not run together. This is a tessellated approximation,
  not an exact CAD boundary or general guarantee against all slow geometry.
  Native cancellation, legacy operation replay and machine/post acceptance are
  not established. Exact GeomFillSurface integration U.14 remains pending.

CAM avoidance evidence under the external validation root below:
`avoidance-tests-20260929-192717/results.json` reproduced four failing fault-handling
checks (two valid geometry controls passed). After correction,
`avoidance-tests-20260929-193013/results.json` reports 67 PASS, no errors/skips,
process 0. Eight focused, 12 common-generator, seven pattern-generator, 18 unified
operation and 22 STL/tab tests. `module-manifest.json` records installed Python
hashes. The expanded default issue macro now has 106 tests; it has not been run as a
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

- [ X ] 7.1.1 Specify a single ordered History list and a separate Bodies/results list. Roles and ownership are defined in [the logical contract](architecture/PART_HISTORY_CONTRACT.md#ownership-and-roles-711); no production schema is implied.
- [ X ] 7.1.2 Map current Part, Part Design Body/Tip, feature ownership, attachment and document-link restrictions to the proposed model. [Source mapping](architecture/PART_HISTORY_CONTRACT.md#current-native-model-and-required-changes-712) separates presentation from model/API changes and records existing multi-solid support.
- [   ] 7.1.3 Prototype native Body adapters versus a part-level feature/result layer. Evaluate multi-body outputs, shared inputs, references, recompute, persistence and upstream compatibility before choosing the architecture.
- [ X ] 7.1.3a Prototype native Body/SubShapeBinder/Pad adapters sharing one
  independent part-owned sketch. Validate source edits, separate Tips and native
  save/reopen without duplicating sketch constraints or reparenting the source.
- [ X ] 7.1.3b Prototype a part-level feature with two explicitly named output
  roles and separate identified result nodes. Validate a later result consumer,
  edits/rename/source order, unavailable/reappearing output, Undo/Redo, abort and
  native save/reopen. Fixed roles are a bounded identity proof, not general lineage.
- [ X ] 7.1.3c Resolve tilted sketch normals and cross-part placement dependencies
  in the explicit-result prototype. Validate transformed geometry against an
  independent solid, source-part moves/Undo, and native persistence.
- [ X ] 7.1.3d Prove a native cut of one App::Link occurrence in an assembly
  updates after shared source edits without changing the definition or second
  occurrence; preserve the cut through save/reopen.
- [ X ] 7.1.3e Probe Draft clone and CAM job-model invalidation. Fix production
  Draft clones retaining old geometry when all source shapes become empty or
  the source list is cleared; verify restored source geometry and clone placement.
  This does not establish CAM toolpath invalidation or general consumer safety.
- [ X ] 7.1.3f Prove an independent sketch attached to a rotated planar support,
  with attachment offset, feeds explicit history results. Support moves propagate;
  Undo/Redo and save/reopen retain attachment links, geometry and result identity.
  This is one FlatFace attachment case, not arbitrary topology repair.
- [ X ] 7.1.4 Define stable feature and body identities, explicit input/output links, and merge/split/disappear/reappear lineage. [Identity contract](architecture/PART_HISTORY_CONTRACT.md#identity-and-dependencies-714) separates modeling/display order from the dependency graph; storage and runtime implementation remain pending.
- [   ] 7.1.5 Document the chosen architecture, migration boundary and a small reference model; update product/UI specifications before production implementation.

Complete when: a prototype demonstrates one independent sketch driving features
on two bodies, one feature producing multiple bodies, and a later feature using
results from both, without silently duplicating sketches or losing references.

- [   ] 7.1.6 Before architecture implementation, record decisions for the supplied
  definition/occurrence, body-result, selection, transaction and persistence contracts;
  include alternatives, affected consumers and narrow proof criteria (G1-G3).
- [ X ] 7.1.6a Record the [adapter experiment boundary and decision gates](architecture/ADR_001_HISTORY_ADAPTER_BOUNDARY.md).
  Retain native Body adapters and an explicit-result layer as candidates; reuse
  native geometry, App::Link, links and transactions. Record unresolved production
  selection/default, schema and consumer gates. This is not the final architecture.

Attachment/drawing batch evidence: **24 PASS**, zero failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\attachment-drawing-20260929-final\results.json`.
Includes ten adapter probes, four native capabilities, three clone invalidation and
seven operation-intent checks. New probes cover a moved rotated support plane with
2 mm attachment offset, and an analytic TechDraw projected radius changing 2 to 3 mm
through source edit, Undo/Redo and restore. Initial drawing fixture used Edge1;
TechDraw's projected circle uses zero-based Edge0 (confirmed in native source and
existing upstream tests). Correcting the fixture required no application fix.
`prototype-manifest.json` records source hashes. Saved AttachedProfileProof.FCStd
and DrawingResultProof.FCStd require the test proxy module to recompute; no native
build, installed source change or GUI mouse/keyboard acceptance is claimed.
Missing/ambiguous drawing references, CAM paths, FEM, general attachment/topology
and lineage gates remain open. See 16.2a and ADR 001 for the bounded consumer proof.

Placement/consumer batch evidence (2026-09-29): **88 PASS**, zero failures/errors/
skips, in `D:\Temp\Office-PC\freecad-plus-validation-20260928\part-consumers-20260929-final\results.json`.
Grouped coverage: four native capabilities, eight adapters, three clone
invalidation checks, 33 existing Draft modifications, 18 PlanarSurface operations
and 22 STL/tab machining checks. Initial probes reproduced wrong tilted extrusion
direction, ignored source-part placement and stale clone geometry; focused rerun
passed all 15 checks before the broader batch. The history layer stays test-only.
The production change is limited to `Draft/draftobjects/clone.py`, synchronized
to the existing fork build without native compilation. Source/installed SHA256:
`6291E8A30ED3C4321833182412A6D8AC86C642CFF035A605F9FFD29327DF19A9`.
`prototype-manifest.json` in that evidence directory records module/test hashes.
No new GUI workflow or mouse/keyboard acceptance is claimed. CAM job-model refresh
is distinct from invalidating generated paths. TechDraw dimension references,
FEM supports/loads (FEM disabled in this build), actual sketch attachments,
general lineage and cold-start prototype deployment remain open.

Earlier adapter batch evidence (2026-09-29): `tests/TestPartHistoryAdapters.py` plus the
four native capability probes report **8 PASS**, no failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\part-adapters-20260929-final\results.json`.
`prototype-manifest.json` records the test/adapter hashes. All implementation is
under `tests/prototypes`; no application module was installed or rebuilt.
The first result adapter lost a shape's translation under native recompute and
merged distinct outputs; Shape/Placement synchronization corrected it, with
position assertions retained. Expected unavailable-result errors clear the
consumer instead of returning partial/stale geometry. Native BodyAdapterProof.FCStd
and test-module-dependent ExplicitResultProof.FCStd are disposable evidence only.
Final choice, general topology/lineage, transformed attachments, remaining downstream
consumers and cold-start deployment remain open under the parents; the later batch
above establishes one bounded assembly-local edit and Draft/CAM model refresh.

Foundation batch evidence (2026-09-29): `tests/TestPartHistoryCapabilities.py`
passes four native probes in the existing fork, with no failures/errors/skips.
Evidence: `D:\Temp\Office-PC\freecad-plus-validation-20260928\part-history-20260929-final\results.json`.
One independent sketch drives two Part extrusions without a Body; another
extrusion produces two solids; a later compound consumes all four results.
Shared radius edits propagate; Undo/Redo, abort and native `.FCStd` save/reopen
retain links and geometry. Two App::Link occurrences keep independent placements.
Native group ownership rejects direct sharing/reparenting from App::Part into a
Body; Body ownership is exclusive. The initial probe assumed an allowed move and
was corrected to test the observed restriction. No application source changed.
`PartHistoryNativeProof.FCStd` in that evidence directory is a disposable native
capability example, not `.cadprt` or a finished history-layer prototype.
7.1.3 remains open: compare actual Body/result adapters, semantic lineage,
mixed definition/occurrence content and drawing/CAM/FEM/Draft consumers before
choosing the architecture. 7.1.5/7.1.6 are not closed by this foundation batch.

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

Planned default reconciled by version 2: suggest New Body or a valid single-target
Unite at creation; require explicit resolution of ambiguity and preserve user intent.
See 7.4.8 and [baseline adoption](#planning-baseline-adoption). Implementation is pending.

- [   ] 7.4.1 Extend the existing Extrude and Revolve task workflows to start in an empty part without a declared/active Body. Keep Operation as the first field, followed by profile, target/result controls and parameters.
- [   ] 7.4.2 For Add with automatic targeting, create a new solid body when the generated solid has no valid volumetric overlap with an existing eligible solid. With exactly one eligible intersecting target, preview adding to that target.
- [   ] 7.4.3 If multiple bodies intersect, show and highlight candidate targets; require an explicit target set or New Body choice. Never choose a target by incidental tree order or visibility.
- [   ] 7.4.4 Provide an explicit New Body override even when geometry overlaps. For Subtract and Intersect, require valid target bodies and report a nonintersecting/empty result rather than creating an unintended body.
- [   ] 7.4.5 Define tangency, face/edge contact, coincident geometry, tolerances, disconnected profile regions, sheet results and multi-solid outputs. Make automatic decisions inspectable in the preview.
- [   ] 7.4.6 Persist target intent and body lineage. Commit concrete operation and target identities. Recompute must not rerun creation inference. When an edit removes the required intersection, report failure/repair instead of switching operation, target or body identity.
- [   ] 7.4.7 Reuse this result/target policy for Loft, Sweep, Helix, primitives and Boolean operations after the Extrude/Revolve pilot passes. Retain legacy command/API entry points.

First deliverable: open a new document, draw a sketch, Extrude without creating a
Body, then create a disconnected Extrude and obtain a second body. Reuse the first
sketch for another feature, modify one selected body with Subtract, and reopen each
feature in the same complete task pane. Repeat the body-creation cases with Revolve.

- [ X ] 7.4.8 Reconcile the planned default from the owner-supplied version 2:
  suggest New Body for no eligible intersection, Unite for exactly one eligible
  target with a valid union, and require deliberate selection for multiple targets.
  Explicit user operation/targets prevail. Other-component intersections do not
  authorize source modification. Pocket/Groove start in Subtract. This closes only
  the planning decision; 7.4.1-7.4.7 and 10.3 implement and validate it.

### [   ] 7.5 Add history editing, rollback and recovery

- [   ] 7.5.1 Add Make Current / rollback and return-to-end controls; show the exact intermediate body results and disable later features for the rollback preview without deleting them.
- [   ] 7.5.2 Insert new features at the current history position and update the dependency graph consistently. Restore the prior position and geometry on Cancel.
- [   ] 7.5.3 Support safe reorder/move with dependency validation and a clear explanation of prohibited moves; never treat arbitrary tree drag order as a valid modeling history.
- [   ] 7.5.4 Add suppress/unsuppress with explicit downstream status. Distinguish suppression, visibility, inactive setup and failed recompute.
- [   ] 7.5.5 Preview deletion effects and offer valid dependent-feature handling. Provide broken-reference repair and Replace Input within the complete feature editor.
- [   ] 7.5.6 Keep feature edits, target changes, body creation/removal and history-position changes atomic for Cancel and Undo/Redo; recover from recompute failures without displaying stale success.

### [   ] 7.6 Preserve documents and external consumers

Owner decision (2026-09-29): `.cadprt` is the planned native format. Continue
best-effort opening and conversion of legacy `.FCStd` files; the owner accepts
that compatibility may become harder and less complete over time. Follow the
[format policy](PRODUCT_SPEC.md#planned-native-format-and-legacy-import), including
untouched originals and explicit conversion-loss reporting. This is not implemented.

- [   ] 7.6.1 Build a compatibility matrix covering existing upstream files, existing Plus files and new history-model files: open/display, edit, recompute and round-trip save are separate checks.
- [   ] 7.6.2 Version any new persisted model and provide opt-in conversion with an untouched original. Opening a legacy file must not force migration.
- [   ] 7.6.3 Preserve existing type/property names and Python entry points where possible. Document any new feature modules required for recomputation; do not promise upstream compatibility for backend changes without evidence.
- [   ] 7.6.4 Define explicit neutral-geometry export as an exchange option, including loss of editable history. Never replace the editable original with a flattened export automatically.
- [   ] 7.6.5 Audit Assembly, TechDraw, CAM, expressions, links and scripts that currently resolve a Body Tip. Provide stable result references and invalidation behavior for the new history model.

- [   ] 7.6.6 Specify `.cadprt` schema/capabilities, legacy import/conversion,
  Save As/Copy/Make Unique identity, external relocation and unsupported-content
  handling before native-format implementation. Never convert owner files in place.
- [   ] 7.6.7 Implement versioned `.cadprt` reading/writing and make it the native
  format for new documents after migration gates pass. Update Open/Save dialogs
  and file associations while retaining legacy `.FCStd` opening.
- [   ] 7.6.8 Implement explicit `.FCStd` to `.cadprt` conversion into a separate
  file. Map editable history, geometry, references and workbench data where possible;
  report unsupported content and distinguish partial or geometry-only recovery.
- [   ] 7.6.9 Extend the compatibility fixtures across legacy versions and supported
  workbenches; verify converted save/reopen/recompute and unchanged original files.
  Publish tested conversion coverage and known losses as the formats diverge.
  Best-effort compatibility must not be represented as guaranteed lossless import.

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


<a id="version-2-objective-coverage"></a>
## Version 2 objective coverage and delivery boundaries

Source: owner-supplied `UPDATED_FREECAD_PLUS_DEVELOPMENT_ROADMAP.md`, version 2.0,
sections 3-7 and 12-15. Adopted as planning scope; all newly added implementation
work below is **not started** unless an existing task explicitly records evidence.
A matching older heading does not close a broader requirement. Existing Phase 3-7
implementations remain partial evidence for the expanded portfolio.

Apply dependency gates before utility/effort ranking. Establish C3 ownership,
identity and persistence contracts before broad dependents, and C2 shared services
before multiplying consumers. Prefer reusable existing code; no kernel or solver
replacement is presumed. Decompose XL items and timebox uncertain feasibility
spikes; engineering-hour estimates are hypotheses, not runtime or delivery promises.
Re-estimate after three delivered milestones using measured work and build time.
The first useful release is a coherent everyday-modeling/sketch slice, not completion
of all surfaces, assemblies, CAM strategies, business options or specialized modules.

Inventory ratings below preserve the supplied planning assessment: U/D are 1-5,
F is feasibility, C is architectural criticality 0-3, effort is an unvalidated band.
S=8-24, M=24-80, L=80-240 engineering hours; XL exceeds 240 with no defined upper
bound. Ranges overlap and must not be summed into a delivery date. `Pending` means
the full objective is unverified; `Partial` points to existing bounded evidence.

| ID | Desired objective | U | D | F | C | Effort | Supplied phase | Local tasks / full-objective status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A01 | Unified part definition with geometry and child occurrences | 5 | 5 | Medium | 3 | L–XL | P1/P2 | 7.1; 12.1; Partial |
| A02 | Part-owned history, independent body results, explicit targets | 5 | 5 | Medium | 3 | XL | P1/P2 | 7.1; 7.4; Partial |
| A03 | Shared instances, occurrence overrides, Make Unique, promote bodies | 5 | 3 | High | 3 | M–L | P2/P3 contracts; P6 product | 12.2; Partial |
| A04 | Work/display context and scoped selection services | 5 | 3 | High | 3 | M–L | P1/P3 | 10.5; 12.4; Pending |
| A05 | Persistent references, topology provenance, repair | 5 | 5 | Medium | 3 | XL | P1/P3 | 7.1.4; 12.5; Partial |
| A06 | Versioned persistence, legacy adapters, migration | 5 | 5 | Medium | 3 | L–XL | P1/P3 | 7.6; 16.1; Partial |
| A07 | Common feature lifecycle, undo, preview, cancellation | 5 | 4 | High | 2 | L | P2/P3 | 8.1; 10.2; Partial |
| A08 | Assembly-scoped feature semantics | 4 | 5 | Medium | 3 | L–XL | P2 proof; P6 product | 7.1.3d; 12.6; Partial |
| U01 | Separate navigators, docking, synchronized highlighting | 5 | 2 | High | 1 | M | P4 | 7.2; 10.6; Pending |
| U02 | Tree filters, columns, folders, comments, dependency display | 4 | 2 | High | 1 | M | P4 | 7.2; 10.6; Pending |
| U03 | Unified Extrude and Revolve command interfaces | 5 | 3 | High | 2 | M–L | P4; depends on A02/A07 | 8.2; 10.4; Partial |
| U04 | Search aliases, shortcut palette, navigation presets | 4 | 2 | High | 0 | S–M | P4; safe prototypes earlier | 10.4; Pending |
| U05 | Multiselection modifiers, filters, Select Other, selection rules | 5 | 3 | High | 2 | M | P4 | 10.5; Pending |
| U06 | Shared extent controls, collectors, interactive handles | 5 | 3 | High | 2 | M–L | P4 | 8.1; 8.4.3; Partial |
| U07 | Move/Copy, point-to-point, triad and coordinate alignment | 5 | 3 | High | 2 | M | P4 | 10.7; Pending |
| U08 | Rollback, valid insertion/reorder, suppression | 4 | 4 | Medium | 2 | L | P3 contract; P4 UI | 7.5; Pending |
| U09 | Guided/direct workflows, progressive disclosure, consistent feature presets | 5 | 3 | High | 2 | M–L | P1 contracts; P4 | 10.2; 10.4; Pending |
| U10 | Intelligent initial New Body/Unite suggestions with persisted explicit intent | 5 | 4 | Medium | 2 | M–L | P1/P3 contracts; P4 | 7.4; 10.3; Pending |
| S01 | Automatic constraints, previews, inference controls | 5 | 3 | High | 2 | M–L | P5 | 11.1; Pending |
| S02 | Cursor-adjacent suggested-constraint palette | 5 | 2 | High | 1 | S–M | P5; earlier prototype possible | 11.3; Pending |
| S03 | Smart dimensions, driving/reference values, entry while drawing | 5 | 3 | High | 1 | M | P5 | 11.4; Pending |
| S04 | Degrees of freedom, conflict repair, sketch diagnostics | 5 | 4 | Medium | 2 | L | P5 | 11.4; Pending |
| S05 | External projection/intersection points and curves | 5 | 3 | High | 2 | M | P5; existing capability audit first | 11.5; Pending |
| S06 | Regions, trim/extend, constrained copy, blocks and patterns | 4 | 4 | Medium | 2 | L | P5 in separate increments | 11.6; Pending |
| S07 | Selection-aware constraint applicability, conflict/redundancy states and reasons | 5 | 4 | Medium | 2 | L | P1 audit/contracts; P5 | 11.2; Pending |
| B01 | Entire/Model/Empty/custom reference sets | 5 | 3 | High | 2 | M–L | P3 contract; P6 UI | 12.3; Pending |
| B02 | Joint/mate assistance, grounding, freedom/conflict display | 5 | 4 | Medium | 2 | L | P6 | 12.4; Pending |
| B03 | Published interfaces, geometry links, external-reference manager | 5 | 5 | Medium | 3 | L–XL | P3 contracts; P6 product | 12.5; Pending |
| B04 | Replacement, component patterns/mirrors, explosions and motion | 4 | 4 | High | 2 | L | P6 in separate increments | 12.2; 12.6; Pending |
| B05 | Configurations, arrangements, flexible subassemblies | 4 | 5 | Medium | 3 | XL | P1 semantics; later P6 increments | 9.6; 12.7; Pending |
| B06 | Lightweight/partial loading and simplified representations | 4 | 5 | Medium | 3 | L–XL | P1 contracts; measured P6 need | 12.8; Pending |
| G01 | Solid/sheet trim and split | 5 | 3 | High | 1 | M–L | P7 | 13.1; Partial |
| G02 | Thicken sheets, sew/stitch, offset and gap diagnostics | 5 | 4 | Medium | 1 | L | P7 | 13.1; Pending |
| G03 | Sweep/loft and through-curves surfaces with guides | 5 | 5 | Medium | 2 | L–XL | P7 | 13.2; Pending |
| G04 | Curve-network/boundary surfaces and continuity controls | 4 | 5 | Unknown | 2 | XL | P7 after bounded spike | 13.3; Pending |
| G05 | Extract/project/intersect curves; isocline extraction | 4 | 4 | Medium | 1 | M–L | P7; split by operation | 13.4; Partial |
| G06 | Holes, patterns/mirrors, shell/draft/ribs and dress-up tools | 5 | 4 | High | 2 | L–XL | P7 in separate increments | 13.5; Partial |
| G07 | Direct face editing and healing | 4 | 5 | Medium | 2 | XL | Late P7 | 9.1; 13.6; Pending |
| G08 | Imported-solid feature recognition | 3 | 5 | Unknown | 1 | XL | Late P7 after spike | 13.7; Pending |
| C01 | Direct-STL input and first three-axis finishing workflow | 5 | 4 | Medium | 2 | L | P8 | 6; 14.1; Partial |
| C02 | Stock-aware roughing, rest machining, boundaries | 5 | 5 | Medium | 2 | XL | P8 after C01 | 14.2; Pending |
| C03 | Simulation, collision checks, posts and setup reuse | 5 | 5 | Medium | 2 | L–XL | P8; limited checks from first release | 14.3; 14.4; Partial |
| I01 | Measurements, mass, sections, interference/clearance | 4 | 3 | High | 1 | M–L | P9; isolated tools may move earlier | 15.1; Pending |
| I02 | Surface quality, continuity, and deviation inspection | 4 | 4 | Medium | 1 | M–L | P7 validation/P9 product | 15.2; Pending |
| D01 | Drawing workflows, associative annotation and repair | 4 | 4 | Medium | 2 | L–XL | P9 | 9.4; 15.3; Pending |
| D02 | BOM, balloons, exploded documentation | 4 | 3 | High | 2 | M–L | P9 after B01/B04 | 15.4; Pending |
| X01 | Sheet metal, frames/weldments, hardware libraries | 3 | 4 | Medium | 2 | XL | P9 by module | 15.5; Pending |
| X02 | Package/relocate projects, compatibility and export | 5 | 4 | High | 3 | L | P3 contracts/P9 UI | 7.6; 15.6; Pending |
| X03 | Performance, scripting, packaging, upstream integration | 5 | 4 | High | 2 | Ongoing | P0 onward | 16.3; 16.5; 16.6; Partial |
| X04 | Native .cadprt identity, capability/version checks, legacy import and associations | 5 | 4 | High | 3 | L | P1/P3; P10 packaging | 7.6; 16.1; 16.6; Pending |
| X05 | Early drawing/CAM/FEM/Draft compatibility probes and adapters | 5 | 4 | Medium | 3 | M–L | P2/P3; ongoing | 7.1; 16.2; Partial |
| X06 | Release licensing, matching source, notices, dependency and asset audit | 5 | 2 | High | 1 | S–M | P0 inventory; P10 releases | 16.7; Pending |
| X07 | Starter models, guided onboarding, compatibility and support documentation | 5 | 2 | High | 1 | M | P4/P11 | 17.2; 17.3; Pending |
| Q01 | Task benchmarks, baseline comparison, effort and release evidence | 5 | 3 | High | 2 | M | P0 onward | 16.3; 16.4; 16.5; Pending |
| M01 | Audience/competitor evidence and measured adoption assumptions | 4 | 2 | High | 0 | S–M | P0/P11 | 17.1; 17.5; Pending |
| M02 | Useful-model distribution, tutorials and focused channel experiments | 4 | 2 | High | 0 | M | P11; publication when authorized | 17.3; 17.4; 17.5; Pending |
| M03 | Independent-fork branding, optional extension/MIME registration | 3 | 2 | High | 1 | S–M | Identity early; P10/P11 | 17.6; 17.7; Pending |

## [   ] Phase 10: Shared workflow, selection and guided modeling (P1/P3/P4)

Depends on applicable Phase 7 decisions; presentation prototypes can proceed only
when they preserve existing semantics. These tasks extend Phase 8, not replace it.

- [ X ] 10.1 Reconcile PRODUCT_SPEC, UI_UX_SPEC, guidelines and ADRs with version 2:
  intelligent suggestions, guided/direct entry, aliases, selection rules, free-core
  commitment and engineering-document scope. Keep current implementation distinct
  from future requirements; retain the operation-first field and indexed CAM scope.
- [   ] 10.2 Implement guided/direct entry through one command model, validation
  and transaction path. Guide curves/regions, magnitude/direction, operation/target
  review and visible confirmation; skip satisfied inputs for preselection/experts.
  Revisit earlier inputs without discarding unrelated valid choices. Collapse
  advanced controls while keeping operation, targets, extent, units and consequential
  warnings visible. Guidance preferences are UI state, not new feature types.
  Pilot Extrude and Revolve before extracting shared behavior; retain Apply/OK/Cancel,
  previews, handles and numeric/expression controls from 8.1.
- [   ] 10.3 Implement 7.4's shared suggestion service: explain inferred versus
  explicitly chosen operations, highlight eligible targets, update proposals before
  explicit choice without oscillating near contact tolerances, and never override
  manual choices. Invalid unions need corrective guidance; mere overlap is not
  validity. Eligibility includes work part, occurrence, reference access/editability
  and geometry. Persist accepted targets/mode; edited features initialize from saved
  intent and fail/repair rather than infer a new operation. Keep Tools is explicit;
  temporary tool geometry need not become a permanent body.
- [ X ] 10.3a Prototype creation suggestions for single solids in one part:
  no/one/multiple candidates, explicit contact review, invalid/empty geometry,
  duplicate candidates and exclusion of cross-part/occurrence targets.
- [ X ] 10.3b Prototype committed New Body/Unite/Subtract/Intersect with concrete
  links. Validate explicit New Body override, changed-intersection failure without
  retargeting, Undo/Redo, aborted target removal and native save/reopen.

Batch evidence: [ADR 002](architecture/ADR_002_CREATION_INTENT.md) records the
accepted boundary, alternatives and limits. **22 PASS**, zero failures/errors/skips,
from seven new operation-intent checks plus 15 existing history/clone checks in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\operation-intent-20260929-final\results.json`.
An initial fixture translation was corrected to test overlap instead of face contact;
no failed application fix is hidden by this correction. `prototype-manifest.json`
records source hashes. No installed source update or native build was needed.
Implementation is test-only: no production selection service, tolerance hysteresis,
multi-target execution, semantic lineage or GUI acceptance is claimed. Task 10.3,
Phase 7 architecture gates and the full guided workflow remain open.

- [   ] 10.4 Retain searchable Pad/Pocket/Revolution/Groove shortcuts as presets
  into shared Extrude/Revolve validation and editing; Pocket/Groove select Subtract
  and request a valid target. Preserve legacy adapters until conversion is supported.
  Add expanded/searchable command catalog, shortcut palette and navigation presets
  without flooding contextual palettes. Track retirement of temporary UI adapters.
- [   ] 10.5 Define shared scoped selection: plain click replaces, Ctrl adds/toggles,
  Shift has documented range/extension semantics; separate sketch picks accumulate
  with modifiers, window picking can collect a group. Integrate existing task
  collectors without losing deliberate collection state. Add Select Other, entity
  filters, tangent/connected-chain rules, window/crossing and restored hide/isolate.
  Keep auto-inference suppression shortcuts nonconflicting; verify keyboard/DPI use.
- [   ] 10.6 Extend 7.2 with separate Assembly and Feature Navigator tabs, optional
  simultaneous docking, explicit work/display part, status columns, contributing-body
  filters, comments, folders and dependency highlights. Display grouping never
  changes ownership, transforms or valid history order.
- [   ] 10.7 Add shared Move/Copy with point-to-point, translation/rotation,
  coordinate-system/axis alignment, movable triad, snapping and local/global context.
  Distinguish one-time placement from a persistent assembly relationship; validate
  occurrence scope, exact numeric results, preview, Cancel, Undo and restore.

Gate G4: simple part/assembly creation, edits, precise moves and recovery survive
save/reopen. Guided/direct entry and aliases produce equivalent semantics. Test
zero/one/multiple targets, invalid contacts, cross-component overlap, missing cut
target, manual override and changed intersections. Compare measured tasks to baseline.

## [   ] Phase 11: Selection-aware Sketcher and reference workflows (P5)

Depends on stable selection/reference contracts; audit existing solver capabilities
before replacement. These tasks extend 8.3, with one reusable eligibility service.

- [   ] 11.1 Audit and improve automatic coincidence, horizontal/vertical, parallel,
  perpendicular, tangent and equal inference. Preview constraints, expose thresholds
  and per-sketch preferences, and support temporary suppression without conflicting
  with selection modifiers. Test cases where no constraint should be inferred.
- [   ] 11.2 Implement fast structural applicability separately from solver
  feasibility. One service serves palettes, toolbar/menu actions, shortcuts and
  execution. No selection shows drawing/global actions; one line offers supported
  single-line actions; two suitable lines add Parallel/Perpendicular. Other operand
  types/counts/roles use their supported relations. Hide structurally inapplicable
  actions; disable proven conflicts with reasons and highlighted constraints.
  Distinguish Valid, Already Applied, Redundant, Conflicting, Unsupported and
  Unverified. Use nonmutating/rolled-back trials, revision/selection caches and stale
  result rejection; revalidate on commit and never silently remove constraints.
- [   ] 11.3 Add a reachable near-cursor suggested-constraint palette using 11.2:
  stable pointer corridor/dismissal delay, useful ordering, keyboard access and
  disable preference. Test dense sketches, zoom/DPI and movement toward/away from
  it. Measure eligibility latency; a palette alone does not complete 11.2.
- [   ] 11.4 Unify smart dimensions and numeric entry while drawing; distinguish
  driving/reference dimensions from construction/reference geometry conversion.
  Show remaining degrees of freedom and conflict/redundancy diagnostics with
  deliberate, undoable repair that preserves intended design relationships.
- [   ] 11.5 Extend associative external projection and true plane intersections:
  curve/plane points versus face/plane curves, with source highlighting and explicit
  projection/intersection choice. Cover tangent, coplanar, disjoint and multiple
  results; changes update or report broken references across approved scopes.
- [   ] 11.6 Complete regions, gap/duplicate/self-intersection diagnostics and
  trim/extend improvements; add constraint-preserving copy/paste, blocks, reusable
  profiles and sketch patterns as separate increments.

Gate G5: solver trials cannot mutate live sketches; redundant/conflicting candidates
remain distinct and invalid suggestions cannot commit. Validate T12, inference/no
inference, external edits, stale asynchronous results and palette interaction.

## [   ] Phase 12: Assembly definitions, occurrences and interpart design (P2/P3/P6)

Depends on Phase 7 identity/persistence proof. A native Link or local-cut probe is
partial evidence, not completion of these production workflows.

- [   ] 12.1 Prove and productize mixed definitions containing geometry, datums and
  child occurrences, without converting a part to a different assembly type. Define
  logical definition versus document identity. Reuse one definition twice in one
  assembly and once in another; shared edits update loaded dependents, with explicit
  reload/update policy for closed external documents. Prevent double transforms.
- [   ] 12.2 Productize occurrence overrides, Make Unique and Promote Bodies to
  Part/Component with explicit associative/independent choices. Remap internal
  references and identity for independent copies while preserving provenance;
  occurrence placement stays local. Validate replacement and multi-assembly reuse.
- [   ] 12.3 Add Entire Part/Model/Empty/custom named reference sets. Keep visibility,
  suppression, reference-only BOM role, configuration/arrangement and load state
  independent. Define deliberate full-geometry access outside exposed reference sets.
- [   ] 12.4 Add contextual mates/joints, grounding, freedom/conflict display and
  joint limits using the existing solver. Preserve work/display context and clearly
  distinguish shared-definition edits from occurrence edits.
- [   ] 12.5 Add occurrence-aware in-context references and published datum/geometry/
  parameter interfaces, with source highlighting. Provide external-reference manager:
  source/version state, update/freeze/break, missing-path repair, unpublished-input
  diagnostics and dependency-cycle rejection. Extend 9.3 rather than inventing
  per-workbench traversal rules.
- [   ] 12.6 Productize assembly-owned cuts with explicit selected-occurrence scope;
  source propagation is a separate deliberate action. Add component patterns/mirrors
  with skipped instances and shared/unique behavior, exploded views and simple motion.
- [   ] 12.7 Define configurations, arrangements and flexible subassemblies after
  parameter scope, identity, solver context and persistence proof. Flexible behavior
  is not merely separate placement of a shared rigid result. Extend 9.6.
- [   ] 12.8 Profile then implement lightweight/partial loading and simplified
  representations. Missing/unloaded components remain represented; commands requiring
  full geometry resolve it explicitly or report unavailable validation.

Gate G6: nested multi-file assembly with shared/unique edits, replacement, reference
sets, in-context references, relocation repair and local cuts survives persistence.
Do not silently omit missing components from checks or BOMs.

## [   ] Phase 13: Solid, curve and surface portfolio (P7)

Depends on stable feature/result contracts. Preserve existing Trim/Isocline and
Phase 3 command work; extend only missing behavior. Each feature needs supported
inputs, tolerance, multi-result/target/tool retention and downstream-edit contracts.

- [   ] 13.1 Complete solid/sheet trim and split coverage beyond the existing Trim
  feature; implement sew/stitch, offsets, gap diagnostics and sheet thickening.
  Spike high-curvature/self-intersection cases; validate actual solid/shell counts.
- [   ] 13.2 Extend sweep/loft with ordered sections, guides, orientation/twist and
  Boolean targets; implement through-curves surfaces with guides. Reuse 3.6/8.2.
- [   ] 13.3 Spike curve-network/boundary surfaces and supported positional/tangent/
  curvature continuity. Measure continuity rather than judging rendered smoothness;
  explicitly limit unsupported inputs instead of assuming a kernel replacement.
- [   ] 13.4 Complete associative extract/project/intersect curve coverage; retain
  Isocline's explicit draft-angle/direction convention and distinguish isoclines
  from isoparametric curves and display-only analysis. Reuse Phase 5 evidence.
- [   ] 13.5 Extend Hole wizard, feature/body patterns/mirrors, shell/draft/rib/web
  and fillet/chamfer tools in bounded increments, preserving specialized parameters.
- [   ] 13.6 Implement 9.1's history-based face move/offset/replace/delete-and-heal
  on a declared class of native/imported solids; explicit repair limits and preview.
- [   ] 13.7 Spike imported-solid feature recognition only after direct-edit and
  reference foundations pass; record feasibility, bounded supported classes and
  geometry-only/unsupported fallback without claiming recovered original history.

Gate G7 per feature: analytic and difficult supported cases, explicit unsupported
cases, geometric validity, scale-appropriate tolerances and downstream recompute.

## [   ] Phase 14: CAM completion and verification expansion (P8)

Extends Phase 6 and 9.5; retain existing Parallel/Waterline, physical holding tabs
and required two-sided/manually indexed machining. Simultaneous rotary/multi-axis
is later scope, not a reason to defer required indexed setups. No rebuild solely
for this planning adoption.

- [   ] 14.1 Audit mesh-capable algorithms versus BRep-only operations; finish STL
  units/dimension/scaling, normals, orientation, bounds, disconnected-piece and
  strategy-specific validity checks. Add setup wizard for model, WCS, stock, tools,
  boundaries, allowances, tolerance and post. Reuse existing inputs and tab geometry.
- [   ] 14.2 Add stock-aware roughing then rest machining as separate deliverables;
  finishing drop-cutter paths do not prove either. Preserve holding-tab exclusions
  in all supported cutting/link moves and across indexed setups.
- [   ] 14.3 Complete containment/avoidance, reusable setups, stale-path detection,
  progress/cancellation and large-mesh profiling. Validate transformed source edits,
  units, stock and fixtures; distinguish model refresh from generated-path validity.
- [   ] 14.4 Add supported simulation/remaining-stock, gouge and tool/holder/fixture
  clearance checks with visible unavailable checks. Verify a narrow machine/post
  scope and expand strategies/tools/posts only with representative fixtures.
  Simulation is not proof of machine safety or authorization for actual motion.

Gate G8: reproducible paths within stated tolerance, supported collision/simulation
checks and independent checks where available; verified post output and explicit
unsupported capabilities. Existing implementation evidence does not close new scope.

## [   ] Phase 15: Inspection, drawing and specialized modules (P9)

Each module depends only on the contracts it consumes and can be delivered separately.

- [   ] 15.1 Unify transient/persistent measurement, units, materials/mass properties,
  interactive/saved sections, interference and minimum-clearance inspection.
- [   ] 15.2 Add curvature combs, zebra/reflection lines, continuity and deviation
  inspection with quantitative checks where claimed; support surface validation.
- [   ] 15.3 Extend 9.4 with drawing setup, projected/section/detail views,
  associative annotations/dimensions and explicit broken-reference repair after edits.
- [   ] 15.4 Add BOMs, balloons and exploded documentation; validate repeated
  instances, unique copies, suppression, reference-only roles and nested quantities.
- [   ] 15.5 Evaluate/reuse compatible sheet-metal, frames/weldments, hardware and
  profile libraries, delivering independently with configuration/persistence tests.
- [   ] 15.6 Package projects and collect dependencies, repair relocated references,
  and export with stated history/metadata losses. Preserve originals and distinguish
  native document packaging from flattened geometry exchange.

Gate G9: independently releasable modules update correctly after source/topology
changes, or explicitly report repair/stale state; drawing and BOM references cannot
silently bind to a different entity.

## [   ] Phase 16: Native documents, benchmark evidence and release hardening (P0-P3/P10)

- [   ] 16.1 Extend 7.6 with stable internal `.cadprt` format identity independent
  of branding; schema/producer/minimum-reader/required-capability declarations,
  units/transforms, embedded/external content and definition/file distinction.
  Preserve supported CAD, assemblies, TechDraw, CAM, FEM and other content; preserve
  unknown content safely or refuse unsupported required saves without silent loss.
  Test wrong-type/corrupt files, safe atomic save, backups/recovery, migration,
  Save As/Copy/Make Unique and relocation. Retain best-effort legacy import with
  untouched originals, conversion reports and distinct native/legacy/exchange paths.
- [   ] 16.2 Complete early TechDraw dimension, CAM path, FEM support/load/material/
  mesh/result and Draft consumer adapters exposed by Phase 7. Test units, transforms,
  occurrence identity, source deletion/suppression/topology changes, Undo/Redo and
  reopen; valid attachment or explicit repair/stale state is required. Do not wait
  for new CAM/FEM products to run these existing-consumer probes.
- [ X ] 16.2a Validate a native TechDraw view and projected radius dimension
  referencing an explicit history result: source radius edits, Undo/Redo and
  save/reopen preserve links and the correct numerical dimension. The fixture has
  one analytic projected circle; no general edge naming, removed-reference repair
  or topology-change safety is established. Batch evidence is in 7.1 above.
- [   ] 16.3 Maintain capability audit and patch/upstream map: usable, inconsistent,
  compatible component/add-on, bounded extension or demonstrated limitation. Cover
  auto constraints, projection/intersection, transforms, Links, multi-solids,
  disambiguation, reorder/suppression and mesh CAM; inspect code and actual behavior.
  Preserve completed baseline evidence and identify only missing/invalidated checks.
- [   ] 16.4 Implement the T01-T12 benchmark corpus below, choosing a coherent
  first-release subset plus required downstream probes. Record named builds,
  hardware, fixture parameters/design intent, operator experience, completion and
  recovery/errors/help needs, task time and recompute/open/save/memory. Separate
  learning from practiced work; use repeated trials/medians where useful. Measure
  baseline before improvement/regression thresholds and claims. Use a separate
  source-built upstream baseline, never the ignored installed FreeCAD. Compare
  Fusion/SolidWorks/Onshape only where available; NX informs workflow, not parity.
- [   ] 16.5 Measure full/incremental build, regeneration, loading, tessellation,
  graphics and cancellation costs before optimizing. Define document locking,
  thread safety and result-commit rules before background execution. Keep core
  commands deterministic/scriptable through the same validation as UI.
- [   ] 16.6 Maintain release/platform and upstream integration gates; test install,
  launch, open/edit/save/export, migration, older/new files and recovery on supported
  platforms. Verify `.cadprt` filters/icons/installer associations. One Windows
  build is not multi-platform evidence; no public release is implied by a push.
- [   ] 16.7 Audit actual source/dependency/asset licenses, notices, change records
  and branding permissions before distribution. Plan matching tagged source/archive,
  required build/install and applicable linking materials with binaries; verify
  artifact/source correspondence. Keep proprietary competitor code/assets out.
  This is an unperformed release audit, not a legal conclusion or publication order.

G0-G3 remain prerequisite evidence gates: known reproducible fork baseline; recorded
high-impact decisions; minimal mixed-definition/shared-occurrence/unique-copy/local-
cut/split-merge/external-link proof with interactive demonstration; then hardened
services and native/legacy/consumer round trips. Current narrow prototypes do not
close these gates. First architectural release requires G0-G3; first broadly useful
release adds G4 plus a selected G5 increment. G10 additionally requires the promised
workflows, package/source/licensing evidence and accurate compatibility limitations.

Benchmark acceptance targets for 16.4 (all full scenarios pending):

| ID | Task | Required evidence |
| --- | --- | --- |
| T01 | Build and revise a mounting bracket | Guided sketch, Extrude add/cut, dress-up, and editable dimensions |
| T02 | Model an enclosure and separate lid | Multiple bodies, shared dimensions, clear ownership, no accidental merge |
| T03 | Reuse one part three times and in another assembly | Shared source edits and independent placements |
| T04 | Make one occurrence independent | Remapped identity/references; other occurrences remain linked |
| T05 | Move/align parts point-to-point | Correct coordinate context, orientation, preview, cancel, undo |
| T06 | Change an upstream sketch/feature | Correct update or explicit repair; no silent wrong-target attachment |
| T07 | Create a dimensioned drawing | Correct source view/dimension updates after edits |
| T08 | Create/update an existing supported CAM operation | Correct setup/stock/reference scope and invalidated stale toolpaths |
| T09 | Attach FEM material, support, and load | Correct attachment or explicit repair/remeshing/recalculation need |
| T10 | Save/reopen/copy/relocate linked projects | Stable identities, dependencies, missing-file recovery |
| T11 | Download a useful model, change two named dimensions, export for printing | Successful customization without general CAD training; repeat after reopen |
| T12 | Apply constraints to one line, two lines, and a constrained sketch | Correct contextual options and distinct already-applied/redundant/conflict explanations |

## [   ] Phase 17: Free product onboarding, audience and optional outreach (P11)

Preparation may accompany engineering; public delivery depends on applicable G10
and actual authorization. No advertising, contact, publication, registration or
payment is authorized by this backlog. Distinct naming and revenue are optional.

- [   ] 17.1 Validate audience hypotheses separately: serious hobbyists, small
  engineering/manufacturing teams, recent/lapsed FreeCAD users, experienced users
  and beginners. Refresh primary competitor evidence before targeting decisions;
  distinguish survey population, team size, licenses, downloads and market share.
  Prioritize FreeCAD baseline, Fusion/SolidWorks task comparisons, Onshape workflow,
  with Inventor/Alibre/Solid Edge/Shapr3D/OpenSCAD and NX/Creo/CATIA where relevant.
  Study local/private ownership and commercial-use terms without assuming adoption.
- [   ] 17.2 Create a useful starter model with named parameters/descriptions/units,
  supported ready-to-print STL/3MF, editable `.cadprt` and STEP where appropriate.
  Include required build/version, image, installation/opening path, beginner guide,
  expert shortcuts and T11 customization route. Printing downloads must not require
  installing the CAD app. Candidate models: brackets, organizers, enclosures,
  drawer/mounting interfaces, RC receiver mounts, battery trays and workshop fixtures.
- [   ] 17.3 Prepare model-led distribution using existing owner model audiences:
  Thingiverse/Printables-compatible uploads, allowed archive or source links if
  `.cadprt` uploads are unsupported, never disguised FCStd files. Prepare one
  60-90-second demonstration, complete tutorial and landing page joining model,
  application download, tutorial and compatibility/support information. Advertise
  useful outcomes and only measured savings; preserve familiar command names.
- [   ] 17.4 Prepare bounded channel experiments: relevant Facebook maker/RC/CNC/
  printing groups, short videos/YouTube, FreeCAD communities/forums, independent
  small creators, searchable tutorials/comparison pages, makerspaces/robotics clubs,
  and later maker publications such as Hackaday. Respect community rules; test
  channel value rather than assuming rankings. Obtain authorization before outreach.
- [   ] 17.5 Measure discovery, trial, installation, first successful customization,
  voluntary return/second independent project, migration and support burden
  separately. Use consented feedback/referral data, no undisclosed telemetry.
  Refine beginner/expert friction using authorized observation; views/downloads or
  enthusiasm do not prove adoption. Revisit effort/support capacity with evidence.
- [   ] 17.6 Prepare independent-fork positioning: upstream credits, workflow/object
  differences, native/import/export limits, add-on/macro compatibility, support
  destination and maintenance status. Optional: evaluate a distinct public name
  before broad incompatible release, preserving built-on-FreeCAD acknowledgment and
  stable format identity. No approved rename or upstream endorsement is implied.
- [   ] 17.7 Optional after format specification: public `.cadprt` description,
  samples/icons, FileInfo submission and proposed IANA media type. Recheck naming,
  availability/process/fees before action; no assigned MIME type or exclusive
  extension ownership is claimed. Required OS association remains 16.6.
- [   ] 17.8 Deferred unless explicitly revisited by the owner: paid packaged
  distribution, support/training, hosted storage/collaboration/backups/computation,
  sponsored development or independent extensions. Reconsider only against real
  adoption/maintenance evidence and applicable code/licensing boundaries. No billing,
  subscription, activation or paid core gates; optional hosted services must not
  become prerequisites for ordinary local modeling.

Gate G11: release candidate, starter source/exports, tutorial and compatibility
notes agree; representative users complete T11. Outreach is reviewable before
publication, and repeated campaigns need evidence. Optional branding, registration
or revenue cannot delay a usable free modeling release.
