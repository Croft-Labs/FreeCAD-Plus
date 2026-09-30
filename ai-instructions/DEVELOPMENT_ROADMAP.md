# FreeCAD Plus: Development Roadmap

## Current focus

Specification update: see [the re-updated objective reconciliation](#re-updated-objective-specifications-and-delivery-slices) and [all 127 item-level specifications](#item-level-product-specifications-f001-f127). Added tasks 10.8-10.9, 11.7, 15.7, 16.8-16.9 and benchmarks T13-T16 are pending; existing completion evidence is preserved.

- Release 0.0.1: user-authorized Windows x64 installer built, accepted and published; publication
  tracked in [the release checkpoint](#pre-release-001). This does not close the
  remaining product, GUI, machine or broad compatibility gates.
- Specification refinement: the [detailed candidate inventory](#detailed-inventory-reconciliation)
  expands existing pending tasks and adds 7.5.7/8.1.6. Consult those concrete behaviors
  before treating a broad objective as complete; implementation evidence is unchanged.
- Current batch: 11.7i/j prototype rollback-based reattachment placement previews
  and verify candidate/commit parity and preservation of existing undo history.
  Grouped validation: 36 passes, zero failures/errors/skips; no native rebuild.
  Production graphical preview and isolation from observers remain pending.
- Previous batch: 11.7g/h reject cyclic and stale/invalid reattachment supports
  before mutation. Grouped validation: 34 passes, zero failures/errors/skips;
  test-only changes, no native rebuild. Production reattachment UI remains pending.
- Previous batch: 11.7e/f prototype deliberate missing-face repair and protect
  caller-owned transactions. Grouped validation: 32 passes, zero failures/errors/
  skips; no native rebuild. Production repair UI and broad topology repair remain open.
- Previous batch: 11.7c/d extend the test-only reattachment operation to explicit
  preserve-local/preserve-world policies, validated with rotated supports and a
  rotated parent part. Grouped validation: 30 passes, zero failures/errors/skips.
  No native rebuild; production editor and lost-support repair remain pending.
- Previous batch: 11.7a/b prototype explicit planar sketch reattachment with local
  offset preservation and reject missing/curved supports before mutation. Grouped
  validation: 28 passes, zero failures/errors/skips; no native rebuild. Production
  reattachment editor, preserve-world policy and lost-support repair remain pending.
- Previous batch: 10.8c/d prove explicit parameter references remain independent
  across parts with matching labels and invalid geometry recovers after transaction
  abort. Grouped architecture validation: 26 passes, zero failures/errors/skips.
  Test-only changes; no native rebuild or parameter editor delivery.
- Previous batch: 10.8a/b prove shared named length parameters, native expression
  persistence/transactions and a test-only dimensional assignment guard. Grouped
  architecture validation: 24 passes, zero failures/errors/skips; no installed
  feature/editor or native rebuild. Native unit coercion remains a production gate.
- Previous batch: 16.2ao/ap preserve probe-file precision and reject conflicting
  duplicate heights. Grouped validation: 65 passes, zero failures/errors/skips;
  Python-only synchronization, no native rebuild.
- Previous batch: 16.2am/an make shared property inheritance and job operation
  traversal iterative, handling cycles/deep chains and duplicate bases. Grouped
  validation: 151 passes, zero failures/errors/skips; no native rebuild.
- Previous batch: 16.2ak/al recognize dressups by current proxy identity with
  guarded legacy fallback and traverse base chains iteratively with cycle errors.
  Grouped validation: 84 passes, zero failures/errors/skips; no native rebuild.
- Previous batch: 16.2ai/aj clear failed Plunge Milling output and reject
  invalid stepover with native error state. Grouped validation: 54 passes, zero
  failures/errors/skips; Python-only synchronization, no native rebuild.
- Previous batch: 16.2ag/ah clear Dragknife and Ramp Entry output before
  validation/generation. Grouped validation: 52 passes, zero failures/errors/skips;
  Python-only synchronization, no native rebuild.
- Previous batch: 16.2ad/ae/af reject non-finite probe coordinates and invalid
  interpolation settings, and correct source-line subdivision counts. Grouped
  validation: 51 passes, zero failures/errors/skips; no native rebuild.
- Previous batch: 16.2aa/ab/ac clear Z Correction caches, reject unusable probe
  files and block out-of-area fallback. Grouped validation: 48 passes, zero
  failures/errors/skips; Python-only synchronization, no native rebuild.
- Previous batch: 16.2x/y/z clear failed Axis Map results, validate positive
  finite radius and update rotary-post snapshot fixtures for the export guard.
  Grouped validation: 44 passes, zero failures/errors/skips; no native rebuild.
- Previous batch: 16.2u/v/w fix Mirror placed passthrough, failure-safe output
  assembly and source-path isolation. Grouped validation: 53 passes, zero
  failures/errors/skips; Python-only synchronization, no native rebuild.
- Previous batch: 16.2s/t clear Array paths before validation/generation and
  Dogbone machining/corner caches before generation. Grouped validation: 49
  passes, zero failures/errors/skips. Skipped native consumers remain a limitation;
  their export guard is verified. Python-only synchronization, no native build.
- Previous batch: 16.2q/r block export for missing/non-geometric Boundary stock
  and reject empty/invalid offset results before clipping. Grouped validation:
  46 passes, zero failures/errors/skips; Python-only update, no native build.
- Previous batch: 16.2o/p prevent cached Boundary paths after clipping/offset
  failures and reject empty boundary geometry in both inclusion/exclusion modes.
  Grouped validation: 44 passes, no failures/errors/skips; Python-only update
  to the existing development build. Native GUI/machine acceptance remains open.
- Previous batch: 16.2l/m/n handle empty dressup inputs, failed lead generation and
  disabled-lead passthrough. Grouped validation: 40 passes, two existing generator
  skips, zero failures/errors. Python-only synchronization, no native build.
- Previous batch: 16.2j/16.2k extend model-container invalidation/rebinding to
  nested CAM dressups and base operations. Grouped validation: 90 passes, one
  existing skip, zero test failures/errors; Python-only synchronization. Missing
  model diagnostics in Lead-in/Lead-out and general consumer gates remain open.
- Previous batch: 16.2h/16.2i reject postprocessing when a selected operation or
  its linked inputs are dirty/invalid. Native cached-path failure/recovery checks
  and postprocessor/dressup regressions: 88 pass, one pre-existing skip, zero
  failures/errors. Python-only synchronization; no native build. General missing
  links, semantic validity, frozen-job policy and machine acceptance remain open.
- Previous batch: 16.2f/16.2g handle replacing/removing CAM model containers and
  restore the wait cursor around full operation execution. Eight targeted checks
  and 67 broader CAM regressions pass across two runs; no native build required.
  Export guards, failed upstream producers and general consumer compatibility remain open.
- Previous batch: 16.2d/16.2e add explicit CAM job-model dependencies and restore
  them for older saved operations. All 72 grouped CAM checks pass; production Python
  synchronized to the existing fork without a native build. Normal document recompute
  now handles model edits and empty-source recovery in the SurfaceScan fixture.
  Export guards, failed producers and full consumer
  compatibility remain open.
- Prior batch: 16.2b/16.2c fixed stale paths on explicitly requested execution with
  missing models/tools, with 69 grouped checks. The new batch addresses scheduling.
- Prior mixed/unique batch: 12.1a/12.2a passed 32 grouped architecture checks.
- Previous batch: 7.1.3g/h planar split/primary-merge lineage passed 29 checks.
- Prior attachment/drawing batch: 7.1.3f and 16.2a passed 24 grouped checks.
  Next: missing/ambiguous drawing references, CAM path/FEM consumers, mixed-part
  identity and production target discovery before architecture selection.
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
- [ X ] 7.1.3g Prototype a real planar split with explicit negative/positive-X
  roles and distinct child identities/provenance. Validate moving the split,
  disappearance/reappearance and Undo; reject multiple solids per role explicitly.
- [ X ] 7.1.3h Prototype a merge preserving an explicitly chosen primary BodyId,
  or allocating a new identity when no primary continues. Persist parent identities;
  validate reorder/rename, geometry edits, save/reopen, unavailable inputs, duplicate
  identities and replaced source lineage without implicit retargeting.
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

Split/merge batch evidence: **29 PASS**, zero failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\lineage-20260929-topology\results.json`.
Five new lineage checks join the previous 24 checks. The initial invalid-source test
found that a raised native recompute error skipped dependent evaluation, retaining
stale merge geometry. The new test-only lineage proxies report expected input/kernel
failures as ResultStatus/ErrorMessage with cleared outputs, allowing participating
result consumers to invalidate themselves. A U-shaped single solid that splits into
two solids on one side now fails explicitly; no arbitrary solid-index mapping occurs.
`prototype-manifest.json` records hashes; SplitMergeProof.FCStd requires test modules.
No installed source or native build changed. This is explicit planar-role lineage,
not arbitrary topology correspondence, persisted revision history, Make Unique or a
production error protocol. Parent architecture/consumer gates remain open; native
error icons and nonparticipating consumers still require deliberate integration.

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
  Specify supported multi-target cuts, trims and other operations as one feature with an
  explicit target set, per-target results and deterministic lineage. This is broader
  than selecting a single target; the single-target prototypes do not complete it.
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

- [   ] 7.5.7 Add controlled recompute: automatic/manual update modes, deferred
  updates and targeted recomputation. Show stale/blocked dependents and the first
  failing input; provide a deliberate update action. Deferred results must not be
  treated as current by export, CAM or downstream analysis. Test switching modes,
  queued edits, failure recovery, cancellation and save/reopen status.

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
  Name collectors by purpose: Profile, Axis, Target Bodies, Guides and Limits. Each
  collector highlights its assigned geometry. Preselection and selection after invoking
  the command must produce equivalent definitions, with the same editable inputs on
  reopen.
- [   ] 8.1.2 Apply command-first selection and identical create/edit coverage to the Phase 3 audit, including profile/section/path/axis replacement after reopening a feature.
- [   ] 8.1.3 Standardize named selection collectors with add/remove/clear, viewport/tree picking, compatible-type filters, chain/region selection and visible invalid-reference feedback.
- [   ] 8.1.4 Standardize signed offsets, adjacent direction buttons, one/two-sided and symmetric modes, units and expressions. Preserve parameters by meaning when switching operation or type.
  Cover distance, symmetric, two-sided, through-all, to-face and offset-from-face
  extents where the command supports them; keep extent semantics distinct from the
  existing sketch-plane start offset. Specify shared solid/surface and Boolean/target
  conventions for Sweep and Loft.
- [   ] 8.1.5 Add consistent live-preview and error states; make Cancel restore geometry, visibility and selection. Define Apply/repeat behavior separately from OK so repeated creation does not create accidental features.

- [   ] 8.1.6 Make previews responsive with cancellable computation, progress
  feedback and reduced-cost previews before final computation. Clearly distinguish
  provisional geometry from committed results; cancellation restores the previous
  model, and a late preview result cannot overwrite newer inputs. Integrate with
  16.5's thread-safety/result-commit rules before background document work.

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
  Handles include lengths, angles, offsets and radii, with exact numeric entry using the
  same properties. Dragging must not bypass expressions, validation or cancellation.
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


<a id="detailed-inventory-reconciliation"></a>
## Detailed candidate inventory reconciliation

The owner supplied a further 13-section candidate inventory in `Pasted text.txt`
and requested missing specifications here. Its concrete behaviors now refine the
owning tasks below; this is a planning update, not completed implementation or a
new agent startup instruction. UI/Feature/Core labels describe likely scope, not
verified effort. Existing completion evidence and stable task IDs are unchanged.

Resolve older wording against established decisions: use creation-time suggestions
with saved explicit intent, preserve the first Operation field and active collectors,
retain the approved draft-angle convention, use `.cadprt` with best-effort legacy
import, and keep required two-sided/indexed CAM and holding tabs. The candidate
inventory does not supersede these with a fixed New Body default, guaranteed upstream
compatibility, different angle semantics or three-axis-only machining. Its embedded
citation placeholders are not verified sources or imported implementation evidence.

| Supplied objective area | Owning roadmap tasks |
| --- | --- |
| 1. Part structure and ownership | 7.1, 7.3, 7.4 (including multi-target execution), 12.1, 12.2 |
| 2. Assembly and feature navigators | 7.2, 7.5, 10.6 |
| 3. Instances, references and reuse | 12.1-12.3, 12.6-12.8 |
| 4. Consistent command interface | 8.1, 8.2, 8.4.1, 10.2-10.4, 13.2 |
| 5. Selection and viewport | 8.4.4, 10.4, 10.5 |
| 6. Sketch creation and constraints | 11.1-11.6 |
| 7. Solid modeling and feature editing | 8.4.3, 13.1, 13.5-13.7 |
| 8. Curves and surfaces | 13.1-13.4, 15.2 |
| 9. Movement and assembly positioning | 10.7, 12.4-12.6 |
| 10. Interpart relationships/reliability | 7.1.4, 7.5.5-7.5.7, 12.5 |
| 11. Mesh and CAM | Phase 6, 14.1-14.4, 16.2 |
| 12. Inspection, drawings and downstream | 15.1-15.5 |
| 13. Performance, files and maintainability | 8.1.6, 12.8, 15.6, 16.1, 16.5, 16.6 |

Completion of a broad heading requires its detailed behaviors and relevant gates;
a narrow prototype or an existing approximate command is not evidence for the whole
objective. Reuse existing backend capabilities and retain explicit unsupported cases.

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
| A09 | Named parameters, expressions, unit checking, scope and publication | 5 | 4 | Medium | 3 | M–L | P1/P3 contracts; P4/P5 editor | 10.8; Pending |
| U11 | Unified workspace, contextual availability/help, keyboard and display accessibility | 5 | 3 | High | 2 | M–L | P3/P4; downstream integration later | 10.9; Pending |
| S08 | Sketch support/orientation, attachment and deliberate reattachment | 5 | 4 | Medium | 2 | M–L | P1/P3 references; P5 UI | 11.7; Pending |
| X08 | Document lifecycle, safe save, recovery snapshots, templates and recent-file repair | 5 | 4 | Medium | 3 | M–L | P1/P3 contracts; P10 hardening | 16.8; Pending |
| X09 | Add-on/macro/API compatibility matrix, adapters and migration diagnostics | 4 | 4 | Medium | 2 | M–L | P0 audit; P3/P10 | 16.9; Pending |
| X10 | Manufacturing export, units/orientation/quality controls and reusable presets | 5 | 3 | High | 2 | M | P3 contracts; P4/P9 UI | 15.7; Pending |

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
  Search must recognize FreeCAD, NX and SolidWorks terminology and route aliases to the
  same command. Navigation presets include mouse behavior, chosen rotation center, zoom-
  to-selection and orthographic sketch orientation.
- [   ] 10.5 Define shared scoped selection: plain click replaces, Ctrl adds/toggles,
  Shift has documented range/extension semantics; separate sketch picks accumulate
  with modifiers, window picking can collect a group. Integrate existing task
  collectors without losing deliberate collection state. Add Select Other, entity
  filters, tangent/connected-chain rules, window/crossing and restored hide/isolate.
  Keep auto-inference suppression shortcuts nonconflicting; verify keyboard/DPI use.
  Specify filters for points, edges, faces, bodies, components, sketches and features;
  scope choices are active part, selected component and whole assembly. Select Other
  cycles overlapping/obscured candidates with a preview. Intent rules include tangent
  chains, connected edges, complete loops, same-radius faces and feature-owned faces.
  Window selection requires full enclosure; crossing selection includes intersected
  entities. Allow documented configurable modifier policies while retaining the adopted
  defaults and explicit collector mode; do not silently reinterpret clicks.
- [   ] 10.6 Extend 7.2 with separate Assembly and Feature Navigator tabs, optional
  simultaneous docking, explicit work/display part, status columns, contributing-body
  filters, comments, folders and dependency highlights. Display grouping never
  changes ownership, transforms or valid history order.
  Columns explicitly include visibility, suppression, errors, source file, reference set
  and modification status. Feature Navigator shows the active work part while Assembly
  Navigator retains component hierarchy. Body filtering supports all part features or
  only contributors to selected bodies. Named groups/folders, comments, type filters and
  input/downstream highlights must remain organizational rather than ownership changes.
- [   ] 10.7 Add shared Move/Copy with point-to-point, translation/rotation,
  coordinate-system/axis alignment, movable triad, snapping and local/global context.
  Distinguish one-time placement from a persistent assembly relationship; validate
  occurrence scope, exact numeric results, preview, Cancel, Undo and restore.
  Allow relocating the manipulator to a vertex, geometric center, datum or inferred
  point. Include typed offsets, arbitrary-axis rotation and snapping in global/local
  coordinates. Present move here once and maintain this relationship as distinct
  actions, with a preview of the affected occurrence.

- [   ] 10.8 Add named parameters, expressions, dimensional unit checking and explicit
  document/part/configuration scope (A09; [F122](#f122)). Provide rename and where-used,
  cycle rejection, publication rules and compatible-expression entry in feature fields.
  Validate shared dimensions, unit changes and rename propagation with T13.
- [ X ] 10.8a Prove a native named length property drives two part features,
  converts inch/mm input, survives parameter-container label edits, Undo/Redo and
  native save/reopen, and preserves an occurrence's independent placement.
- [ X ] 10.8b Prototype a dimensional assignment boundary for length expressions;
  reject angular results before mutation and reuse native expression cycle rejection.
  Verify transaction abort restores the valid expressions/geometry and later edits.
- [ X ] 10.8c Prove explicit internal-name parameter references remain independent
  across two parts with matching container labels and Width property names, through
  edits and save/reopen. Verify native object-level reverse dependency membership.
- [ X ] 10.8d Prove a unit-correct zero length can invalidate downstream geometry,
  transaction abort restores expressions and geometry, and subsequent valid edits
  retain working Undo/Redo. This is recovery evidence, not automatic UI rollback.

Parameter dependency/recovery batch: `parameter-dependencies-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928` records **26 PASS, zero
failures/errors/skips**: eleven capability checks (two new), ten adapter and five
lineage checks. Macro PASS; process ended. Both tasks preceded this grouped run
using the existing fork build (engine source 2df76790b4). No native rebuild,
installed application change or release update. Native `InList` is object-level
and includes non-expression dependencies; it is not a property-level where-used
implementation. Explicit document object names are not implicit part/configuration
scope resolution. Production scope, where-used, editor validation and failed-result
consumer handling remain open under 10.8 and the architecture gates.

Named-parameter foundation: `named-parameters-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **24 PASS, zero
failures/errors/skips**: nine native capability checks (two new), ten adapter and
five lineage checks. Macro PASS; process ended. Initial `named-parameters-20260930-batch`
had 23 passes/one failure because native assignment accepted an angle as a length
without invalid state. The new test-only `tests/prototypes/NamedParameters.py`
evaluates the expression's unit before assignment; native code rejects the cycle.
Prototype SHA256: `0C2E9ED61A09F8795E63902940E5C0B1A8177F954E098D8B7B580B404583DC17`.
The guard supports App::PropertyLength and explicitly length-valued expressions
only. It is not installed and does not intercept application expressions. Fixtures
retain native object/property identities and need no custom proxy to recompute.
This proves container label changes, not property renaming or a parameter editor.
Configuration/cross-document scope, publication, where-used, display-unit settings,
full T13, and production unit/default policy remain pending under 10.8. Both tasks
preceded grouped testing using engine 2df76790b4; no native build or release change.

- [   ] 10.9 Complete the unified contextual workspace, availability explanations,
  local help, keyboard navigation and display accessibility (U11; [F025](#f025),
  [F123](#f123)). Preserve the active engineering document across modeling, CAM,
  drawings and analysis; validate keyboard-only tasks and enlarged-display recovery.

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
  Smart Dimension infers length, angle, radius, diameter or spacing from selected
  geometry. Numeric entry while drawing covers lines, rectangles, circles and slots.
  Degrees-of-freedom display highlights unconstrained entities and remaining movement
  directions. Constraint repair previews proposed removals/replacements and their
  effects before an explicit undoable commit.
- [   ] 11.5 Extend associative external projection and true plane intersections:
  curve/plane points versus face/plane curves, with source highlighting and explicit
  projection/intersection choice. Cover tangent, coplanar, disjoint and multiple
  results; changes update or report broken references across approved scopes.
- [   ] 11.6 Complete regions, gap/duplicate/self-intersection diagnostics and
  trim/extend improvements; add constraint-preserving copy/paste, blocks, reusable
  profiles and sketch patterns as separate increments.
  Sketch repair additionally detects tiny segments and overlapping geometry. Power
  trim/extend supports dragging across unwanted segments while retaining valid
  constraints where possible and reporting losses. Region picking selects closed areas
  inside a larger sketch without requiring the whole sketch as the profile.

- [   ] 11.7 Make sketch placement, orientation, offset and support/reattachment
  explicit (S08; [F124](#f124)). Preview preserve-local versus preserve-world policies,
  prefer stable references where appropriate, and repair lost supports deliberately.
  Validate rotated occurrences, external projections, constraints and Undo with T14.
- [ X ] 11.7a Prototype explicit same-document planar-face reattachment preserving
  the local attachment offset. Validate downstream result placement/identity,
  Undo/Redo and native save/reopen with two parallel supports.
- [ X ] 11.7b Reject missing and curved support faces before changing the sketch;
  verify existing support, placement, offset and downstream geometry remain intact.
- [ X ] 11.7c Verify preserve-local reattachment to a differently rotated planar
  support inside a rotated part, retaining the full offset and valid result volume.
- [ X ] 11.7d Prototype preserve-world reattachment by solving a compensating
  native attachment offset. Verify world translation/orientation, result position
  and identity, Undo/Redo, save/reopen and subsequent support movement.
- [ X ] 11.7e Prototype deliberate repair of a missing planar face reference using
  an explicit preserve-local replacement. Reject preserve-world for invalid sketch
  state; verify repair, Undo back to failure, Redo and save/reopen with result identity.
- [ X ] 11.7f Reject prototype reattachment while a caller-owned transaction is
  pending, before mutation. Verify the caller's edit remains uncommitted and can be
  aborted, followed by successful independent reattachment and Undo.
- [ X ] 11.7g Reject support geometry that depends on the sketch before introducing
  an attachment cycle. Verify with a native extrusion derived from the sketch,
  preserving support, placement, validity and transaction state after rejection.
- [ X ] 11.7h Reject supports with invalid or pending recompute state, including
  dependencies. Verify touched-plane and failed-box rejection, then repair the box,
  recompute, reattach successfully and Undo back to the original support.
- [ X ] 11.7i Prototype synchronous candidate placement preview by recomputing in
  a temporary transaction and aborting. Verify both placement policies match later
  commits while restoring support, offset, world placement and downstream position.
- [ X ] 11.7j Verify repeated previews and rejected missing-face preview preserve
  an existing committed user edit and its Undo/Redo without a pending transaction.

Preview evidence: `reattachment-preview-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **36 PASS, zero failures/
errors/skips** (11 capability, 20 adapter, five lineage checks). Macro PASS; process
ended. Both tasks preceded grouped testing using engine source 2df76790b4.
Prototype SHA256: `FFB7C0A062757FE463A91837F40916108DE4EEB166E0063437C8BED4A8F97763`.
No installed module, native rebuild or release update. This synchronous test-only
preview temporarily mutates the document and recomputes: observers see trial state.
It does not satisfy isolated trial execution or implement graphical preview,
asynchronous cancellation, production task transactions or preservation of an
already-populated redo stack. Those remain production gates under 11.7.

Support validation evidence: `reattachment-support-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **34 PASS, zero
failures/errors/skips** (11 capability, 18 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded grouped testing using engine source 2df76790b4.
Prototype SHA256: `4E22D978257BCF6A7758D7E6E0557F2FC1BE6A285BB4B3952E9DAEA4B9F02524`.
Native dependency traversal supplies cycle and state inspection; validation occurs
before opening the reattachment transaction. Tests cover a direct derived support,
a touched support and a failed native box; broader dependency graph and consumer
failure cases remain open. No installed application change, native rebuild or
release update. This is test-only prerequisite validation, not production UI delivery.

Recovery/transaction evidence: `reattachment-recovery-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **32 PASS, zero
failures/errors/skips** (11 capability, 16 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded grouped testing using engine source 2df76790b4.
Prototype SHA256: `6A006AFD9AD8C585BCB06FA0CBEFD178199296DB1B3F5985861A7995DA7B5C81`.
Test-only changes; no native rebuild, installed editor or release update. The
fixture uses an unavailable Face99 reference on an existing support, not deleted
object resurrection or ambiguous topology matching. Preserve-world requires valid,
recomputed placement; missing-face recovery is explicitly preserve-local. Nested
transactions are rejected, not integrated with a production task transaction.
Consumer stale-shape/export policy, general support repair and GUI remain pending.

Placement-policy evidence: `reattachment-policies-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **30 PASS, zero
failures/errors/skips** (11 capability, 14 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded this grouped run with engine source 2df76790b4;
no native build, installed module change or release update. Prototype SHA256:
`A48BA5C8C09FC164CE7A2F2D47C7DD8E1AFBA2F22F546996FCD27F1B558C5C7D`.
The sketch stays in its existing container. Preserve-world compensates the offset
at reattachment time; later support motion remains associative. This covers a
rotated parent definition, not a selected assembly occurrence, reparenting or
cross-document placement. Preview/UI, lost-support repair, production transaction
integration and broader consumer failure handling remain pending under 11.7.

Bounded reattachment evidence: `sketch-reattachment-20260930-verified/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **28 PASS, zero
failures/errors/skips** (11 capability, 12 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded grouped testing with the existing fork build,
engine source 2df76790b4. Initial batch had 27 passes/one error: the native missing
face lookup raises IndexError, now converted into the prototype's validation error.
`tests/prototypes/SketchReattachment.py` SHA256:
`F52536AD4C705C29AD6569603E52D4416709000E20AD0D75FDC0EA0E44E0F770`.
Test-only operation, not installed; no native rebuild or release update. That batch did
not implement preserve-world placement, automatic topology repair, rotated
reattachment, external scope, preview or production transaction integration. The
caller must have no open transaction; broader consumer invalidation remains a gate.

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
- [ X ] 12.1a Prove a native definition containing a solid and a child occurrence
  can be instanced twice in one assembly and once in another. Shared dimension edits
  update all instances; child placement and resulting bounds/volume survive restore.
  Same-document proof only; external reload policy and product workflow remain open.
- [   ] 12.2 Productize occurrence overrides, Make Unique and Promote Bodies to
  Part/Component with explicit associative/independent choices. Remap internal
  references and identity for independent copies while preserving provenance;
  occurrence placement stays local. Validate replacement and multi-assembly reuse.
  Occurrence-local overrides explicitly include placement, visibility, color and
  representation; editing one override must not rewrite the shared definition or another
  occurrence. Component replacement preserves placement and recoverable mate/joint
  bindings, with unresolved relationships exposed for repair. Promoting selected bodies
  must present associative versus independent behavior explicitly.
- [ X ] 12.2a Implement a test-only Make Unique adapter for a definition containing
  one independent sketch and its native extrusion. Native recursive copy remaps
  inputs; assign fresh semantic IDs and provenance, relink only the chosen occurrence
  and preserve its placement. Verify Undo/Redo, independent edits and save/reopen;
  unsupported definition rejection must not create objects or change the link.

Mixed/unique batch evidence: **32 PASS**, no failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\mixed-unique-20260929-final\results.json`.
Seven native capability probes plus ten history adapters, three clone checks,
seven intent and five lineage checks. `prototype-manifest.json` records source
hashes. The native mixed-part proof and the bounded copy require no application
change or native build; no GUI command is installed. MixedDefinitionProof.FCStd
and UniqueDefinitionProof.FCStd contain native objects with ordinary metadata.
The copy prototype excludes external dependencies, nested definitions, arbitrary
feature proxies, general body lineage and production identity/schema migration.
First run passed 31 checks; the final run adds no-mutation rejection coverage.
Parents 12.1/12.2 and architecture release gates remain open.

- [   ] 12.3 Add Entire Part/Model/Empty/custom named reference sets. Keep visibility,
  suppression, reference-only BOM role, configuration/arrangement and load state
  independent. Define deliberate full-geometry access outside exposed reference sets.
  Named reference subsets select bodies/datums. Empty changes the exposed representation
  only; it must not delete, suppress or exclude the component from BOMs implicitly.
  Fully loaded/lightweight/unloaded state is separately controlled.
- [   ] 12.4 Add contextual mates/joints, grounding, freedom/conflict display and
  joint limits using the existing solver. Preserve work/display context and clearly
  distinguish shared-definition edits from occurrence edits.
  Suggest mates/joints from selected faces, axes or points. Visually distinguish
  grounded, underconstrained, fully constrained and conflicting components. In-context
  editing keeps surrounding geometry visible, with selection/edit scope made explicit.
- [   ] 12.5 Add occurrence-aware in-context references and published datum/geometry/
  parameter interfaces, with source highlighting. Provide external-reference manager:
  source/version state, update/freeze/break, missing-path repair, unpublished-input
  diagnostics and dependency-cycle rejection. Extend 9.3 rather than inventing
  per-workbench traversal rules.
  Associative geometry linking copies selected geometry between parts with visible
  source tracking and update controls. Reference repair previews the downstream effects
  of replacing a missing face/edge. Preserve geometric selection intent as well as
  identity across topology changes; cycles must be rejected before acceptance. Failure
  reporting identifies the first failed feature, invalid input and blocked dependents.
- [   ] 12.6 Productize assembly-owned cuts with explicit selected-occurrence scope;
  source propagation is a separate deliberate action. Add component patterns/mirrors
  with skipped instances and shared/unique behavior, exploded views and simple motion.
  Save exploded arrangements and support simple mechanism animations with joint limits.
  Mirroring distinguishes linked/shared instances from independent mirrored definitions;
  skipped instances are stored explicitly.
- [   ] 12.7 Define configurations, arrangements and flexible subassemblies after
  parameter scope, identity, solver context and persistence proof. Flexible behavior
  is not merely separate placement of a shared rigid result. Extend 9.6.
  Dimension/suppression configurations and assembly-position arrangements are separately
  saved concepts; switching one must not implicitly overwrite the other.
- [   ] 12.8 Profile then implement lightweight/partial loading and simplified
  representations. Missing/unloaded components remain represented; commands requiring
  full geometry resolve it explicitly or report unavailable validation.
  Evaluate shared instance graphics and visibility-based processing in addition to
  selective loading and simplified representations. Optimization must not omit
  hidden/unloaded components from checks requiring their geometry.

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
  Body split/trim accepts supported planes, surfaces or other bodies and previews
  retained regions. Add surface untrim and extend, plus interactive keep-region
  selection and associative trimming tools. Thicken supports one-sided, opposite-sided
  and symmetric thickness with Boolean options. Sewing exposes gaps and tolerance and
  creates a solid only when a valid closed volume results; open results remain sheets.
- [   ] 13.2 Extend sweep/loft with ordered sections, guides, orientation/twist and
  Boolean targets; implement through-curves surfaces with guides. Reuse 3.6/8.2.
  Through-curves surfaces need section-to-section correspondence controls and twist
  preview, not only guide selection. Shared Sweep/Loft tasks distinguish solid versus
  surface output and show targets/results before commit.
- [   ] 13.3 Spike curve-network/boundary surfaces and supported positional/tangent/
  curvature continuity. Measure continuity rather than judging rendered smoothness;
  explicitly limit unsupported inputs instead of assuming a kernel replacement.
  Curve-network surfaces use intersecting curve families; expose positional, tangent and
  curvature boundary conditions only where supported, and validate the claimed
  continuity numerically.
- [   ] 13.4 Complete associative extract/project/intersect curve coverage; retain
  Isocline's explicit draft-angle/direction convention and distinguish isoclines
  from isoparametric curves and display-only analysis. Reuse Phase 5 evidence.
  Associative extraction sources include faces and edges; projection/intersection may
  involve intersecting bodies. Preserve source/update links and the established Isocline
  draft-angle convention rather than silently interpreting it as a different normal-
  angle measure.
- [   ] 13.5 Extend Hole wizard, feature/body patterns/mirrors, shell/draft/rib/web
  and fillet/chamfer tools in bounded increments, preserving specialized parameters.
  Hole wizard covers standard holes, counterbores, countersinks, threads and reusable
  position sketches. Unified patterns include linear, circular, curve-driven and table-
  driven placement with skipped instances. Feature/body mirrors distinguish mirrored
  geometry, linked copies and independent results. Fillets/chamfers include tangency
  propagation, variable radii, corner options and localized failure feedback.
  Shell/draft/ribs/webs need consistent tasks and specific geometric failure
  explanations.
- [   ] 13.6 Implement 9.1's history-based face move/offset/replace/delete-and-heal
  on a declared class of native/imported solids; explicit repair limits and preview.
- [   ] 13.7 Spike imported-solid feature recognition only after direct-edit and
  reference foundations pass; record feasibility, bounded supported classes and
  geometry-only/unsupported fallback without claiming recovered original history.
  Target recognition of editable holes, pockets and fillets on suitable imported solids.
  Define recognized parameters and confidence/unsupported cases explicitly; do not claim
  the original feature history has been recovered.

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
  Direct machining must not require converting STL triangles into thousands of CAD
  faces. Mesh preparation explicitly detects holes, inverted normals, disconnected
  regions and unsuitable geometry. Guided setup visibly includes units, orientation and
  work origin alongside stock/tools/boundaries.
- [   ] 14.2 Add stock-aware roughing then rest machining as separate deliverables;
  finishing drop-cutter paths do not prove either. Preserve holding-tab exclusions
  in all supported cutting/link moves and across indexed setups.
  Provide coherent roughing/finishing strategy presets with visible allowances,
  tolerances and stepovers; rest machining targets remaining stock from preceding
  operations rather than simply repeating a finishing path.
- [   ] 14.3 Complete containment/avoidance, reusable setups, stale-path detection,
  progress/cancellation and large-mesh profiling. Validate transformed source edits,
  units, stock and fixtures; distinguish model refresh from generated-path validity.
  Mesh boundaries include sketch-based containment, selected mesh regions and avoid
  areas. Reusable setup templates cover machines, tools, stock, posts and recurring
  operation sequences. Track geometry, stock and tooling changes separately and mark all
  affected paths stale; the existing missing-input execution fix proves only its
  recorded cases.
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
  Measurement covers distance, angle, radius, thickness, minimum separation and mass
  properties. Saved measurements retain references and an explicit update policy.
  Sections support multiple planes, saved section views and measurements on sections.
  Interference/clearance results list component pairs, highlight conflicts and let users
  navigate each result.
- [   ] 15.2 Add curvature combs, zebra/reflection lines, continuity and deviation
  inspection with quantitative checks where claimed; support surface validation.
  Deviation inspection includes deviation maps; keep analysis/display distinct from
  constructing new curves or surfaces.
- [   ] 15.3 Extend 9.4 with drawing setup, projected/section/detail views,
  associative annotations/dimensions and explicit broken-reference repair after edits.
  Provide a drawing creation wizard for standard/projected/section/detail views using
  consistent templates. Associative annotation includes hole callouts and center marks
  as well as dimensions, with explicit lost-reference repair.
- [   ] 15.4 Add BOMs, balloons and exploded documentation; validate repeated
  instances, unique copies, suppression, reference-only roles and nested quantities.
  Expose reference-component exclusion explicitly and keep it independent of
  visibility/reference-set contents; exploded documentation must correspond to saved
  arrangements.
- [   ] 15.5 Evaluate/reuse compatible sheet-metal, frames/weldments, hardware and
  profile libraries, delivering independently with configuration/persistence tests.
- [   ] 15.6 Package projects and collect dependencies, repair relocated references,
  and export with stated history/metadata losses. Preserve originals and distinguish
  native document packaging from flattened geometry exchange.

- [   ] 15.7 Add reusable manufacturing export presets (X10; [F127](#f127)).
  Make selected geometry/occurrences/configuration, units, orientation and mesh
  quality explicit; audit supported formats and report history/metadata losses.
  Validate dimensions, transforms and tessellation by reimport using T16.

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
- [ X ] 16.2b Clear an operation's previous path before a missing job model can
  return from execution. Validate removal after successful SurfaceScan generation
  and regenerated cutting commands after restoring the model.
- [ X ] 16.2c Apply the same early invalidation to missing tool-controller failures;
  restored controller regenerates the path. Preserve the existing frozen-job branch.

CAM invalid-input batch: both regressions reproduced **43 stale machining commands**
before the fix. Shared production `src/Mod/CAM/Path/Op/Base.py` now clears Path after
its frozen-job guard and before input validation. **69 PASS**, no failures/errors/
skips, in `D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-invalid-inputs-20260929-verified\results.json`:
two new cases, 18 PlanarSurface, 22 mesh/tab, 18 avoidance and nine Deburr checks.
Source/installed SHA256: `FE5A146430588CD2B3E5660B2CD9B16B67E6A57EEB12AFD3F5DA079B9BB3227D`;
`module-manifest.json` records matching source/module/test hashes. Python-only install,
no native build or GUI/machine acceptance. The earlier `red` and `final` directories
ran the pre-fix module; `verified` is the completed corrected batch.
This establishes clearing on execution and recovery, not automatic execution after
all history edits, aggregate-job/export invalidation or native failed-producer safety.
Task 16.2 and the broader CAM dependency gates remain open. See the
[regression procedure](../tests/UpstreamIssues.md#cam-invalid-input-paths-roadmap-162b162c).

- [ X ] 16.2d Add hidden native ModelDependencies links to the job model group
  and its geometry for whole-model operations without explicit Base picks. Prove
  document recompute regenerates after model-width edits and clears/rebuilds paths
  when the source becomes empty/returns, without manually touching/executing the op.
- [ X ] 16.2e Restore those links for an older saved operation lacking the property;
  save/reopen and a later empty source must still invalidate the path automatically.

CAM dependency batch: the empty-source case reproduced **43 stale commands** even
with 16.2b/c, because the operation was not scheduled. Shared ObjectOp now binds
ModelDependencies on execution and document restore, preserving existing feature
identities/properties and using additive native LinkList metadata. **72 PASS**, no
failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-dependencies-20260929-final\results.json`.
Coverage: five invalid-input/dependency cases, 18 PlanarSurface, 22 mesh/tab,
18 avoidance and nine Deburr checks. Source/installed Base.py SHA256:
`8F38E250CD73C0B1BF8754BF64CA4879BF509D35C40620520212F780A8ECCC4C`.
`module-manifest.json` records matching hashes. Python-only install, no native build.
The initial probe assumed an aggregate Operations.Path; current Job.setupOperations
creates App::DocumentObjectGroup, so that assertion was corrected to inspect real
operation paths. No aggregate-cache or postprocessor safety claim follows from it.
Remaining: failed upstream producers that skip execution, replacing the job's Model
container, arbitrary selection/occurrence graphs, export guards and frozen-job policy.
The restore fixture is native FCStd; no cadprt or upstream compatibility is asserted.

- [ X ] 16.2f Rebind whole-model operation dependencies when Job.Model is replaced
  or removed; clear old paths immediately for unfrozen jobs and recover through
  normal document recompute when geometry returns. Drop obsolete model links.
- [ X ] 16.2g Restore the wait-cursor decorator to full ObjectOp.execute, correcting
  its accidental placement on the dependency helper in 16.2d/e. Verify generation
  runs with the wait cursor and an exception restores the previous cursor and clears Path.

Container/cursor batch: production Python Base.py and Job.py synchronized into the
existing fork build. `cam-container-20260929-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records 67 passing broader
checks plus seven passing targeted cases and one fixture error (native objects
cannot belong to two groups). After correcting the fixture to transfer membership,
`cam-container-20260929-corrected/results.json` records all eight targeted cases
passing: **75 distinct checks pass across the two runs**, no remaining failures/skips.
Source/installed SHA256: Base.py
`53D660473414228095FC9B4F69132CF11DBB90356251A168AFDFB695AEFB57D6`, Job.py
`16D5377AF2A031543D64B7708E9DABDA04E2CF8239CF6D8216C879CCA09CD2A5`.
No native build, mouse/keyboard acceptance or machine/export safety claim.
Frozen-job preservation remains the existing policy; general failed-producer,
nested-operation and export gates remain pending under 16.2.

- [ X ] 16.2h Refuse post-list creation for dirty native operations or linked
  dependencies, reporting the offending object and requiring recompute. Verify
  dirty operation and dirty source with a clean operation cache, then recovery.
- [ X ] 16.2i Refuse post-list creation after a native producer failure even when
  downstream CAM retains machining commands. Verify failure and repaired-producer
  recovery; retain nested dressup Active/tool/coolant export regressions.

Export-state batch: shared `Path/Post/PostList.py` checks native `State` on each
active operation and its `OutListRecursive` before copying cached paths into a
Postable. All three output ordering strategies use this wrapper; shared legacy
and machine-based exporters consume these lists. No implicit recompute or document
mutation is performed by the guard. Frozen state does not bypass dirty/invalid
export checks; the existing generation freeze behavior remains unchanged.
`D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-export-20260929-verified\results.json`
records **88 PASS, one existing skipped classification test, zero failures/errors**
(11 invalid-input checks, 75 postprocessor checks including the skip, three dressup
checks). The macro's overall `passed` is false because it requires zero skips.
The first grouped run identified dressup tests exporting edited inputs without
recompute; corrected tests recompute before export and preserve their output assertions.
PostList.py source/installed SHA256:
`0C70E6249CF1AEF5BD346CE89B2CB507F750E7F97BD2A07EE702A258B7B2E078`.
Python-only install into the existing fork build, no native rebuild or GUI/machine
acceptance. These guards do not detect silently wrong but clean geometry, missing
references absent from the dependency graph, or external scripts bypassing PostList.
Full 16.2 consumer/export compatibility remains open.

- [ X ] 16.2j Clear nested base-operation and dressup caches when a job Model
  container is removed; prove all paths remain empty through recompute and recover
  after restoring the container, including successful postprocessing.
- [ X ] 16.2k Rebind nested base-operation model dependencies when the container
  is replaced, dropping the obsolete container and recovering paths/export after
  transferring model geometry. Reuse Job.allOperations traversal.

Nested CAM batch: Job.onChanged now visits existing allOperations, binding base
operations and clearing/touching all returned path objects for unfrozen jobs.
The existing native dressuptest.FCStd fixture includes four base operations and
increasingly nested dressups. Two new tests verify removal and replacement/recovery.
`D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-nested-20260929-batch\results.json`
records **90 PASS, one existing classification skip, zero test failures/errors**
(11 invalid-input, five dressup and 75 postprocessor tests including the skip).
Strict overall macro flag is false because of the skip. During missing-model
recompute, Lead-in/Lead-out reports a NoneType.Group error; paths remain empty and
restore/export succeeds. Improving that diagnostic remains pending, as do general
compound/occurrence graphs, frozen-job policy and full consumer compatibility.
Installed Job.py matches source SHA256
`57B42492F1E5CFCC4935D09CC40BCA469E2120B51C6E973C94FFA745FFDBDB33`;
Python-only synchronization, no native build or
GUI/machine acceptance. This closes the two bounded nested-fixture checks only.

- [ X ] 16.2l Stop Lead-in/Lead-out processing when the base Path has no commands;
  return a native empty Path from Boundary for empty input. Verify the nested
  missing-model fixture stays empty without invalid dressup objects and recovers.
- [ X ] 16.2m Clear a Lead-in/Lead-out result before generation, preventing a
  generator exception from retaining old machining commands; verify recovery.
- [ X ] 16.2n Return the placed base path immediately when both lead options are
  disabled; verify exact G-code passthrough without invoking the lead generator.

Dressup input batch: `cam-leads-20260929-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **40 PASS, two existing
linking-generator skips, zero failures/errors** (11 invalid-input, seven dressup,
nine lead-generator and 15 linking tests including the skips). Strict overall
macro flag is false because of skips. The first run exposed Boundary returning a
list for an empty path; correcting it allowed the strengthened native no-invalid-
objects assertion to pass. Prior missing-model Lead-in/Lead-out diagnostics are
resolved in this fixture; ordinary missing-model/empty-boundary log messages remain.
Source and installed hashes: LeadInOut.py
`9F70114D88B5EBAC91119BD2805326A5755C105528BE8811BC738F8FF03AFC63`;
Boundary.py `88DE0133429769A10821AAFE7EE408696502FE4E059176345CD5F2F4AAA674DA`.
Python-only synchronization into the existing fork build; no native build or
GUI/machine acceptance. General dressup failure/consumer compatibility remains open.

- [ X ] 16.2o Clear Boundary dressup output before offset/clipping work so an
  exception cannot leave cached machining commands. Verify both failure stages
  and regeneration after correction using the native CAM fixture.
- [ X ] 16.2p Reject null boundary shapes for both inclusion and exclusion masks;
  keep an empty path and native error state that prevents postprocessing. Return
  a native empty Path for a missing base instead of assigning None. Verify repair
  restores generation/export and missing-base recovery remains clean.

Boundary failure batch: `cam-boundary-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **44 PASS, zero
failures/errors/skips**: 15 invalid-input checks (four new), seven nested-dressup
checks and 22 STL/tab checks. The macro completed with PASS and the test process
ended. Source and development-build Boundary.py SHA256 both:
`1EC5F400DBD2CC116A281FEF24A16F117B1041C3097B546A342216098B2135D0`.
Both implementation tasks were completed before this grouped validation; no native
rebuild was needed. The existing engine reports revision 2df76790b4, with this
Python update synchronized separately. No GUI/machine acceptance or new release;
the published 0.0.1 installer is unchanged. General consumer gates remain open.

- [ X ] 16.2q Mark missing/non-geometric Boundary stock as a native operation
  error instead of logging and returning success. Confirm empty output, export
  rejection, and recovery after restoring the original boundary.
- [ X ] 16.2r Validate boundary offset results before clipping: reject empty
  collections and null/invalid shapes. Inject empty collections/null offset shapes
  for both inclusion/exclusion, assert clipping is not invoked, and verify native
  error/export rejection and recovery with a corrected offset.

Boundary input batch: `cam-boundary-inputs-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **46 PASS, zero
failures/errors/skips**: 17 invalid-input checks, seven nested-dressup checks and
22 STL/tab checks. Macro PASS; test process ended. Source and development-build
Boundary.py SHA256: `E7D4A2BB0D55DA4F1A8BE4CB7F6ADFA783783CAFBA9EB613DADF94BAE6D7CACE`.
Both changes preceded the grouped runtime check; Python-only synchronization, no
native rebuild. Existing engine revision is 2df76790b4. Offset failure injection
validates rejection/recovery, not general offset geometry correctness. No native
GUI/machine acceptance or release update; broader consumer gates remain open.

- [ X ] 16.2s Clear Array output before input checks and generation. Verify
  missing base, explicitly executed empty base, generation failure, export rejection
  for native errors and recovery after correction.
- [ X ] 16.2t Clear Dogbone output and maneuver/bone/tip caches before generation.
  Verify injected generation failure leaves no cached output/markers, blocks export
  and recovers; retain normal corner geometry regression coverage.

Array/Dogbone batch: `cam-array-dogbone-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **49 PASS, zero
failures/errors/skips**: 21 invalid-input checks (four new), four Array checks,
17 Dogbone checks and seven nested-dressup checks. Macro PASS; test process ended.
The initial `cam-array-dogbone-20260930-batch` had 48 passes and one failure:
native recompute skips the Array when its producer fails. The corrected fixture
verifies the existing export guard rejects the cached result, then explicitly
executes Array to validate empty-input cleanup. This is not a fix for eager
invalidation of every skipped consumer; that broader gate remains open.
Source/development-build SHA256: Array.py
`E50D7CB6E317918933D40CA4AF863F85C546D48B83447B8831BC7FEE3153A39F`;
DogboneII.py `9D51B57CAE2083D9E74E31074AD9D161674E1E9F8AE3A7EF7AB4BE36735AB280`.
Both implementations preceded grouped runtime validation; no native rebuild.
The reused engine reports 2df76790b4 with separately synchronized Python updates.
No native GUI/machine acceptance or release update. Dogbone cache failure injection
uses seeded markers; inherited tests separately verify normal corner geometry.

- [ X ] 16.2u Preserve base placement when MirrorAxis is None; validate translated/
  rotated passthrough and unchanged source G-code.
- [ X ] 16.2v Clear Mirror output before generation and assemble KeepBasePath output
  locally before publishing. Validate generation and assembly failures, empty output,
  native error/export rejection where recompute invokes execution, and recovery.
- [ X ] 16.2w Copy placed paths before Mirror transforms or appends commands. The
  identity-placement helper can return the live source Path. Validate combined
  output with identity and translated bases without changing source G-code/state.

Mirror batch: `cam-mirror-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **53 PASS, zero
failures/errors/skips**: 25 invalid-input/workflow checks (four new), seven nested
postprocessing, four Array and 17 Dogbone checks. Macro PASS; test process ended.
The initial `cam-mirror-20260930-batch` had 52 passes and one error: KeepBasePath
mutated the identity-placement base and export correctly rejected its touched
state. Copying the path fixed the production defect; the expanded identity/translated
fixture and recovery/export check pass. Source/development-build Mirror.py SHA256:
`DE48096DDD7D5C54F5FBACA65CDD52DB0F6BFCD28D02C36363D67AAFBF8FBE83`.
Grouped Python synchronization/testing, no native rebuild; reused engine 2df76790b4.
No GUI/machine acceptance or release update. General skipped-consumer invalidation
and broader downstream compatibility remain open.

- [ X ] 16.2x Clear Axis Map output before conversion so arc splitting or mapping
  failure cannot retain an old path. Verify native error/export rejection and recovery.
- [ X ] 16.2y Require finite positive Axis Map radius, with Reverse controlling
  direction. Verify zero/negative rejection and recovery; check all six X/Y-to-A/B/C
  mappings in both directions on linear motion, preserving source G-code.
- [ X ] 16.2z Adapt rotary-post snapshot fixtures to the dirty-input export guard:
  recompute dependencies, assert clean/valid inputs and valid operation, then restore
  and acknowledge only the deliberately injected compound/split test path. Preserve
  production export checks and validate LinuxCNC/Grbl rotary regression expectations.

Axis Map batch: `cam-axis-map-20260930-final/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **44 PASS, zero
failures/errors/skips**: 28 invalid-input/workflow checks (three new), seven nested
postprocessing checks and nine rotary-post regressions. Macro PASS; process ended.
The initial `cam-axis-map-20260930-batch` had 35 passes/nine errors because rotary
fixtures injected paths without clearing their deliberate dirty-output state.
The intermediate `cam-axis-map-20260930-verified` retained 35 passes/nine failures:
new dependency assertions exposed a dirty stock sketch. Explicit fixture recompute
before restoring snapshots resolved that prerequisite without weakening export.
Source/development-build AxisMap.py SHA256:
`A9E44123B1F057B5E7CEB21D510C22EE69E6A39627003A64DE663D022D83D9EE`;
rotary fixture SHA256: `1E721C0B4752F3207BA2EC54C83E776E0D32EC8CB71D1E90309E5111BCDD3290`.
Both production changes preceded grouped validation; only Python was synchronized
into the existing engine (2df76790b4). No native build, new release, GUI/machine
acceptance or new simultaneous-multiaxis capability. General consumer gates remain open.

- [ X ] 16.2aa Clear Z Correction output before execution and the previous
  interpolation surface before reading probe data. Verify missing-file and
  interpolation-failure cleanup, corrected-data recovery, and explicit empty-
  filename placed-base passthrough without an old surface.
- [ X ] 16.2ab Raise native errors for specified missing files, insufficient
  probe points and interpolation construction failures instead of silently
  returning the base path. Verify export rejection and valid-grid recovery.
- [ X ] 16.2ac Reject path points outside the probe area rather than replacing
  corrected output with the uncorrected base. Verify an undersized valid grid
  blocks output/export and a sufficient grid restores the expected correction.

Z Correction batch: `cam-zcorrect-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **48 PASS, zero
failures/errors/skips**: 32 invalid-input/workflow checks (four new), seven nested
postprocessing checks and nine rotary-post regressions. Native four-point grid
fixture produces the expected +0.5 mm cutting correction; missing, insufficient,
collinear, out-of-area and injected interpolation-error cases reject/recover.
Macro PASS; test process ended. Source/development-build ZCorrect.py SHA256:
`A0E10B279DA11FA09BD05FA04061A4D8307D83ED2B633F5699E0A376AC37D3C0`.
All three changes preceded grouped validation. Python-only synchronization into
engine 2df76790b4; no native rebuild, GUI/machine acceptance or release update.
An explicitly empty filename retains uncorrected placed-base behavior. External
probe-file changes require explicit recompute; automatic file monitoring and
arbitrary probe-grid quality remain outside this bounded validation.

- [ X ] 16.2ad Reject NaN/infinite probe coordinates before building a surface;
  identify file/line, leave no old output, and verify rejection/export blocking
  plus recovery for each X/Y/Z coordinate.
- [ X ] 16.2ae Require finite positive ArcInterpolate and SegInterpolate values
  when applying a correction. Verify zero/negative values yield native errors,
  empty output/export rejection, and recovery after restoring valid settings.
- [ X ] 16.2af Use ceiling division for source-line segment counts and include
  both endpoints in the discretization point count. Verify lengths 0.5, 1, 1.01,
  2 and 2.5 mm at a 1 mm setting preserve endpoints and bound source-line spacing.

Numeric Z Correction batch: `cam-zcorrect-numeric-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **51 PASS, zero
failures/errors/skips**: 35 invalid-input/workflow checks (three new), seven nested
postprocessing and nine rotary-post regressions. Macro PASS; process ended.
Source/development-build ZCorrect.py SHA256:
`636A64C32DBB9762352EF22D0B01D55B57551202A6E03F31B7863C519F46B716`.
All three changes preceded grouped validation; Python-only synchronization into
engine 2df76790b4, no native rebuild or release update. Spacing bounds apply to
source lines before height correction; no adaptive corrected-surface chord-error
claim is made. GUI/machine acceptance and broader consumer gates remain open.

- [ X ] 16.2ag Clear Dragknife output before input checks/generation. Verify
  missing/empty base cleanup, generation-failure native error/export rejection
  and regeneration after correction.
- [ X ] 16.2ah Clear Ramp Entry output before validation/generation. Verify
  generator-failure native error/export rejection and recovery with valid feed
  settings; run the inherited ramp-generator suite alongside nested postprocessing.

Dragknife/Ramp batch: `cam-dragknife-ramp-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **52 PASS, zero
failures/errors/skips**: 38 invalid-input/workflow checks (three new), seven nested
postprocessing and seven ramp-generator checks. Macro PASS; process ended.
Initial `cam-dragknife-ramp-20260930-batch` had 51 passes/one fixture failure:
Ramp Entry correctly rejected zero fixture feeds. Explicit positive horizontal,
vertical and ramp feeds resolved setup; no production validation was weakened.
Source/development-build SHA256: Dragknife.py
`C9AC7F3CF16FC374F9B07AB2EECE63F89E1B4A0971335DCFC01ED4E4B8945E13`;
RampEntry.py `BD9A86983A17461E4F302947DCA48D7B6CA9B1BAFC71AB60084C8D1FC5FAF3B5`.
Both implementations preceded grouped runtime validation. Python-only updates to
engine 2df76790b4; no native rebuild, release update or GUI/machine acceptance.
General dragknife geometry and skipped-consumer eager invalidation are not closed
by these bounded failure/recovery checks; broader consumer gates remain open.

- [ X ] 16.2ai Clear Plunge Milling output before generation. Verify injected
  edge-conversion failure removes cached commands, blocks export and recovers.
- [ X ] 16.2aj Reject non-finite/negative/approximately-zero stepover with native
  error state instead of warning and returning success. Verify zero/negative
  rejection/export blocking and recovery after restoring 1 mm stepover.
- [ X ] 16.2ak Audit and replace internal-name-only base lookup with recognition
  of current Path.Dressup proxies. Stop at Path.Op proxies; retain legacy naming
  fallback with native Path::Feature/single-Base-link checks. Validate custom-name
  nested Array/Mirror, restored custom-name Array, legacy links and ordinary
  operation/profile LinkSubList boundaries.
- [ X ] 16.2al Traverse dressup base chains iteratively, detect cycles with stable
  native document/object identity, and return None/default tool for disconnected
  chains. Validate a 1500-node duck-typed chain, a cycle and real missing-link repair.

Plunge Milling batch: `cam-plunge-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **54 PASS, zero
failures/errors/skips**: 40 invalid-input/workflow checks (two new), seven nested
postprocessing and seven ramp-generator checks. Macro PASS; process ended.
Initial `cam-plunge-20260930-batch` had 52 passes/two fixture failures: the inherited
base lookup requires "Dressup" in the internal name. Matching the application
creation convention fixed the fixture; structural lookup remains task 16.2ak.
Source/development-build PlungeMilling.py SHA256:
`109B684C9247EC18DFC62E1234CB81C307E428AA5EA5B9F194FE6954B2A19AD2`.
Both implementations preceded grouped validation. Python-only synchronization into
engine 2df76790b4; no native rebuild, release update or GUI/machine acceptance.
Drilling-cycle semantics and general physical milling suitability are not certified
by these bounded checks; broader consumer gates remain open.

Shared lookup batch: `cam-dressup-lookup-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **84 PASS, zero
failures/errors/skips**: 44 invalid-input/workflow checks (four new), seven nested
postprocessing, four Array, 17 Dogbone, five holding-tag and seven ramp-generator
checks. Macro PASS; process ended. Source/development-build Dressup/Utils.py SHA256:
`1DA658C5E228D8B423C752459646DCD7AD49B539730AC770DACC4BC747B7B6D2`.
Both changes preceded grouped testing. Current proxy namespaces and the legacy
single-link/name contract are covered; arbitrary third-party proxies are not
certified. Cycle/deep-chain tests use duck-typed fixtures; native custom-name,
nesting, missing-link and save/reopen paths are tested separately. No schema change,
native rebuild, GUI/machine acceptance or release update. Python synchronized into
engine 2df76790b4; broader consumer gates remain open.

- [ X ] 16.2am Replace recursive operation-property lookup with iterative traversal
  and cycle rejection. Preserve explicit overrides (including False/None), missing-
  property defaults and tool/coolant/active behavior; validate a 1500-link chain.
- [ X ] 16.2an Make job allOperations traversal iterative and unique by native
  document/object identity. Preserve outer-before-base/group order; handle shared
  bases/cycles without duplicate invalidation. Validate native shared Array bases
  through model removal/recovery and deep/cyclic duck-typed compound graphs.

Shared traversal batch: `cam-traversal-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **151 PASS, zero
failures/errors/skips**: 47 invalid-input/workflow checks (three new), seven nested
postprocessing, four Array, 17 Dogbone, five holding-tag, seven ramp-generator,
21 Path utility and 43 operation-utility checks. Macro PASS; process ended.
Source/development-build SHA256: Base/Util.py
`2EB08E210346860558224801B6654C64A65A2129E39AE9911AABEFE5C05F0F2E`;
Main/Job.py `9FF91E759C2EC4FE1D031118523C19E1C9BC7AA4B5445D6064834E89B8B548B1`.
Both changes preceded grouped validation. Python-only synchronization into engine
2df76790b4; no native rebuild, schema migration, release or GUI/machine acceptance.
Cycle tolerance in job invalidation/cleanup does not validate cyclic models for
machining/export; property lookup explicitly raises when a cycle prevents resolution.
Broader consumer gates remain open.

- [ X ] 16.2ao Preserve parsed probe XYZ precision instead of rounding to two
  decimal places. Validate sub-0.01 mm bounds and a 0.123456 mm height through the
  native interpolation surface and corrected cutting path.
- [ X ] 16.2ap Deduplicate identical XY/Z samples and reject conflicting heights
  at the same parsed XY rather than choosing the first line. Verify both file
  orders, empty output/surface on conflict, export rejection and recovery.

Probe precision batch: `cam-probe-precision-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **65 PASS, zero
failures/errors/skips**: 49 invalid-input/workflow checks (two new), seven nested
postprocessing and nine rotary-post regressions. Macro PASS; process ended.
Source/development-build ZCorrect.py SHA256:
`96D5E1DE0D0AF53F367C682AF326F83C4F267DDF1D0DAA69DFFBF1FD882D7B97`.
Both changes preceded grouped validation. Python-only synchronization into engine
2df76790b4; no native rebuild, schema migration, release or GUI/machine acceptance.
Exact parsed XY duplicates are checked; no averaging or near-point merge tolerance
is implied. Probe-file changes still require recompute; arbitrary surface quality
and broader consumer gates remain open.

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
  Expose reproducible operation recording as well as scriptable commands. Reduced-cost
  previews must be identified as previews and replaced by validated final geometry;
  progress and cancellation remain responsive without committing partial results.
- [   ] 16.6 Maintain release/platform and upstream integration gates; test install,
  launch, open/edit/save/export, migration, older/new files and recovery on supported
  platforms. Verify `.cadprt` filters/icons/installer associations. One Windows
  build is not multi-platform evidence; no public release is implied by a push.
  Keep UI adaptations, new features and object-model changes separable so upstream
  integration does not require one inseparable rewrite. Clearly identify which persisted
  features require the fork; preserve the adopted best-effort legacy conversion policy
  rather than promising unlimited upstream compatibility.
- [   ] 16.7 Audit actual source/dependency/asset licenses, notices, change records
  and branding permissions before distribution. Plan matching tagged source/archive,
  required build/install and applicable linking materials with binaries; verify
  artifact/source correspondence. Keep proprietary competitor code/assets out.
  This is an unperformed release audit, not a legal conclusion or publication order.

- [   ] 16.8 Complete document lifecycle and recovery (X08; [F125](#f125)):
  dirty/read-only state, templates, recent-file repair, safe saves and rotating snapshots.
  Recover into an editable copy while protecting originals; distinguish file identity
  and external-dependency state without claiming atomic multi-file saves. Validate T15.
- [   ] 16.9 Establish an add-on/macro/API compatibility matrix (X09; [F126](#f126)).
  Audit representative extensions, define supported capability/version boundaries,
  adapters and deprecations, and test changed ownership through public APIs. Missing
  required extensions must preserve unsupported content safely or refuse unsafe saves.

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
| T13 | Drive several features from named expressions, then rename/change display units | Correct dimensional meaning, dependency updates, and rejected cycles/incompatible units |
| T14 | Create and reattach an offset sketch in a rotated component | Explicit local/world placement policy, preserved valid constraints, deliberate reference repair |
| T15 | Recover from an interrupted save using a snapshot | Recoverable editable copy, protected original, explicit external-dependency state and identity |
| T16 | Export a part and selected assembly occurrences using supported presets | Correct dimensions, units, transforms, configuration, mesh quality, and disclosed data losses |

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

## Pre-release 0.0.1

- [ X ] Build current application source `2df76790b4` in Release configuration and
  stage a self-contained Windows x64 runtime outside the source tree. Full build
  completed successfully. Refresh/relink Base/Version.cpp because incremental
  metadata still reported `8abce719de`; final launcher reports `2df76790b4`.
- [ X ] Package a per-user NSIS installer with a distinct FreeCAD Plus registration,
  Start-menu entry and launcher settings directories. Preserve native identities,
  upstream installation, file associations, licensing and unrelated files.
- [ X ] Validate 120 model/task/CAM cases against the staged runtime, zero failures,
  errors or skips. After revision-only relink, staged and installed launcher smoke
  checks pass: native imports, workbench inventory, isolated settings, save/reopen.
- [ X ] Install the actual artifact silently, verify 11 key installed hashes and
  registration, check shortcut target, uninstall and verify application/shortcut/
  registration removal while retaining an unrelated user file. No clean-VM or
  hardware cutting acceptance is claimed.
- [ X ] Publish GitHub pre-release `0.0.1` with only the Windows installer asset;
  verify public pre-release state and uploaded artifact digest.

Evidence root: `D:\Temp\Office-PC\freecad-plus-release-0.0.1`.
Records: `build.log`, `version-compile.log`, `version-link.log`, `package-final.log`,
`payload-validation/results.json`, `launcher-validation/results.json`,
`install-results.json`, `installed-validation/results.json`, `uninstall-results.json`.
Artifact: `FreeCAD-Plus-0.0.1-Windows-x64-Setup.exe`, 360,754,930 bytes, unsigned;
SHA256 `c969fb92aea4cbd4da400d78dfb18d3674de16ebb68d9a4432f3f1bcc1b33dd8`.
[Release notes](releases/0.0.1.md) list included/omitted workbenches, compatibility
limits and the distinction between fork version 0.0.1 and engine version 26.3.0.
[Packaging procedure](../package/WindowsInstaller/FREECAD_PLUS_RELEASE.md).

Published 2026-09-30 02:42:23 UTC (2026-09-29 local):
[FreeCAD Plus 0.0.1](https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.1).
Release ID 399674768, target/tag commit `1a962bb23da3795adc2b4c10c59b8218aea2fe9e`.
Verified `draft=false`, `prerelease=true`, exactly one asset, 360,754,930 bytes, and
GitHub asset digest matching the tested installer SHA256 above. Application source
remains `2df76790b4`; the tag additionally contains packaging/tests/release documentation.

## Re-updated objective specifications and delivery slices

Source: owner-supplied `RE-UPDATED_FREECAD_PLUS_DEVELOPMENT_ROADMAP.md`, reconciled
2026-09-29. The [item-level catalogue](#item-level-product-specifications-f001-f127)
retains all 127 goals, workflow descriptions and completion examples. F001-F111
expand the original inventory, F112-F121 capture later product decisions, and
F122-F127 add supporting requirements. The package coverage table and owning tasks
above remain the execution/status index; this catalogue adds acceptance detail.

This is a specification reconciliation, not feature implementation, a build, or
validation. Existing completed task records and the 0.0.1 release remain unchanged.
No catalogue item is newly declared complete. Read each item with its owning tasks:
existing bounded implementation/prototype evidence applies only to its tested scope;
unproven portions remain pending. Embedded agent rules, startup tasks, repository
reorganization and publication instructions from the supplied file are not adopted.
Market assertions and source citations are planning inputs, not newly verified facts.

Established decisions take precedence over ambiguous source wording: the Operation
field stays first; active command collectors accumulate picks, while ordinary click,
Ctrl and Shift retain the established selection semantics. Automatic body/mode
suggestions occur only at creation, with accepted intent persisted for recomputation.
Isocline uses the approved draft-angle convention (Phase 5), not a substituted raw
normal-vector angle. Required two-sided/indexed CAM and holding tabs remain in scope;
initial three-axis finishing is only a delivery increment. `.cadprt` remains planned;
0.0.1 still uses `.FCStd`. Benchmark comparisons use a separately scoped upstream
source build, never the installed upstream application. The roadmap does not itself
authorize implementation of every future capability or external publication.

### Dependency contracts added by the expanded specifications

- Definition/occurrence/document identities precede shared assembly reuse, Make
  Unique, replacement and configuration-aware copies (7.1, 12.1-12.2, 16.1).
- Feature provenance and stable references precede region selection, rollback,
  repair and reliable downstream consumers (7.1.4, 7.5, 11.6, 16.2).
- Parameter scope, dimensional units and cycle rules precede broad expression fields,
  configurations and published dimensions (10.8, 12.5, 12.7).
- Edit context, selection eligibility and sketch coordinate/reattachment policies
  precede shared collectors, contextual constraints and precise moves (10.4-10.7,
  11.2, 11.7). Prove local/world placement in a rotated occurrence.
- Transactions and preview invalidation precede shared command lifecycles, scripting
  and background results; stale work must not commit (8.1, 16.5, 16.9).
- Native save/copy/recovery and external-reference contracts precede format migration,
  project packaging and extension compatibility (7.6, 15.6, 16.1, 16.8-16.9).
- Downstream adapters must retain correct engineering references before production
  claims for TechDraw, CAM, FEM or Draft. Export boundaries explicitly distinguish
  native documents from geometry exchange (15.7, 16.2).

Use narrow probes before broad UI: one unit-aware parameter drives two features,
rename propagates and a cycle is rejected; sketch reattachment proves its coordinate
policy; recovery-as-copy preserves identity rules and the original. General feature
recognition, full configurations, simultaneous multiaxis CAM, cloud services and a
kernel replacement are not prerequisites for these contracts.

### Incremental product release slices

These are candidate capability slices, not dates, release authorizations or claims
about the published 0.0.1 installer. Dependencies govern ordering; independent
modules can ship separately after their applicable evidence gates.

| Slice | Minimum useful capability | Evidence before claiming the slice | Explicit later scope |
| --- | --- | --- | --- |
| R0: internal architecture proof | Mixed part definition, shared occurrences, part-level Extrude/cut, persisted identity; narrow parameter/document contracts | G0-G2 and early engineering-consumer probes | Polished UI and broad migration |
| R1: useful free modeling preview/beta | Navigators, guided/direct Extrude and Revolve, aliases, modifier selection, contextual constraints, precise moves, native-save/basic export | G3-G5 selected scope, G10-G11; T01, T02, T05, T10-T12 and architecture/legacy/consumer evidence. Constraint subset covers one/two lines, conflicts, redundancy and commit validation | Advanced surfaces, full configurations, recognition and complete CAM |
| R2: dependable assembly reuse | Instances, Make Unique, replacement, reference sets, mates and interpart links | G6; T03, T04, T06 plus reference repair and persistence | Broader configuration/loading increments |
| R3: modeling depth | Selected trim, thicken, holes, dress-ups, sweep and loft increments | G7 fixtures for each delivered operation | Arbitrary curve networks and general recognition |
| R4: mesh CAM | Finishing first, then separately validated rough/rest machining; preserve the required indexed/two-sided and tab roadmap | G8 for each operation with stated post, simulation and collision scope | Simultaneous multiaxis and any universal machining-safety claim |
| Independent downstream slices | Drawing, inspection, BOM, sheet metal and frames as bounded modules | G9 and relevant consumer/persistence evidence | Undelivered module capabilities |

A narrow prototype does not promote an entire slice to complete. Build and validate
coherent groups of changes as already requested, recording source, automated tests,
GUI acceptance and publication separately.

## Item-level product specifications (F001-F127)

Each entry preserves the supplied goal, workflow and completion example; the owning
roadmap tasks establish status and implementation boundaries. Source P-phase labels
and scope estimates are planning metadata, distinct from this roadmap's task numbers.
?Complete when? states required evidence, not evidence already obtained. Apply the
reconciliation rules above to every entry.

<a id="f001"></a>
### F001 — Unified part container

**Owning tasks:** 7.1, 12.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A01 · **First delivery:** P1/P2 · **Likely scope:** Core

**Goal:** Let a user start modeling a part and later add components without changing its fundamental object type.

**Workflow and behavior:** A definition contains its own sketches, datums, features, solid/sheet results, and child occurrences. Add Component adds an occurrence to that definition; it does not convert its geometry into a different assembly-only class. Distinguish structural children from feature inputs and keep child transforms explicit.

**Complete when:** Create a housing with its own geometry, insert a bearing and fastener, then insert the complete housing into another part. Edit the housing and reopen the project without duplicate transforms or ownership changes.

<a id="f002"></a>
### F002 — Part-level feature history

**Owning tasks:** 7.1, 7.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A02 · **First delivery:** P1/P2 · **Likely scope:** Core

**Goal:** Make the part's modeling sequence the primary history so features can act across several bodies.

**Workflow and behavior:** Create features in the work part and collect input geometry and target bodies explicitly. A sketch can drive multiple features; the active or last-visible body is not an implicit destination. The visible history represents an executable dependency order, while organizational folders remain presentation only.

**Complete when:** Create two solids, cut both with one part-owned feature, and edit an earlier sketch. The navigator, dependency graph, results, undo, and saved document agree about ownership and execution order.

<a id="f003"></a>
### F003 — Independent body results

**Owning tasks:** 7.1, 7.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A02 · **First delivery:** P2/P3 · **Likely scope:** Core

**Goal:** Create a solid or sheet without first preparing an active PartDesign Body.

**Workflow and behavior:** A geometry-creation command accepts valid profiles and datums in the part and produces one or more identified body results. Expose whether the selected input makes a solid, sheet, or several disconnected results. A Unite feature may use temporary tool geometry without leaving an extra permanent tool body unless Keep Tools is selected.

**Complete when:** Create two disjoint profiles in a new part and produce independently selectable/editable results. Save/reopen preserves their identities and a later Boolean operation can target either result.

<a id="f004"></a>
### F004 — Explicit Boolean mode

**Owning tasks:** 7.4, 10.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U03, U10, A02 · **First delivery:** P2/P4 · **Likely scope:** Feature/Core

**Goal:** Use the same modeling command to create independent material or alter selected existing material.

**Workflow and behavior:** Present New Body, Unite, Subtract, and Intersect where supported, with targets highlighted separately from profiles/tools. Apply tasks 7.4 and 10.3's contextual initial suggestion and sticky manual choices. Mode conversion edits the feature when supported; unsupported legacy conversions require a clear migration path. Validate topology as well as spatial intersection.

**Complete when:** Exercise every supported mode, change one feature's mode, and test missing targets and invalid contact. Accepted operation and target identities survive recompute and reopening without being inferred again.

<a id="f005"></a>
### F005 — Multiple targets

**Owning tasks:** 7.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A02, A07 · **First delivery:** P2/P3 · **Likely scope:** Core

**Goal:** Apply one coherent operation to several selected bodies without duplicating setup.

**Workflow and behavior:** Collect an ordered target set, preview each affected result, and define per-command semantics: a cut can modify each target separately, while a unite may produce combined results. Specify whether tools are retained and which results replace which inputs. Commit all supported targets atomically; any explicit partial-success mode must show exactly what will be skipped.

**Complete when:** A cut through two solids updates both after a profile edit. An invalid target causes a clear, reversible failure rather than a partially committed document or silent target omission.

<a id="f006"></a>
### F006 — Persistent body identity

**Owning tasks:** 7.1.4, 7.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A05 · **First delivery:** P1/P3 · **Likely scope:** Core

**Goal:** Keep intended relationships understandable when a feature splits, merges, or replaces bodies.

**Workflow and behavior:** Separate stable document identifiers from labels, output position, and transient kernel topology. Record provenance and explicit identity rules for surviving, split, merged, and deleted results. If more than one new result could satisfy an old reference, retain the unresolved reference and offer repair instead of guessing.

**Complete when:** A downstream feature, drawing reference, and assembly use remain correct through supported splits/merges, or report the exact ambiguity. Renaming a body or sorting the tree does not change identity.

<a id="f007"></a>
### F007 — Reusable sketches and datums

**Owning tasks:** 7.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A01, A02, S05 · **First delivery:** P2/P5 · **Likely scope:** Feature

**Goal:** Use one design input in several features without copying geometry merely to satisfy ownership restrictions.

**Workflow and behavior:** Keep sketches, planes, axes, points, and coordinate systems identifiable at part level. Consuming a sketch may change a visibility preference but does not transfer ownership or prevent reuse. Show its consumers and distinguish using original geometry, selecting a closed region, projecting geometry, and making an independent copy.

**Complete when:** One sketch drives two extrusions and a datum drives a revolve. Editing the shared input updates all intended consumers; deleting it previews affected features and supports cancellation.

<a id="f008"></a>
### F008 — Promote bodies to components

**Owning tasks:** 12.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A03 · **First delivery:** P3/P6 · **Likely scope:** Core

**Goal:** Turn bodies modeled together into reusable component definitions with deliberate design relationships.

**Workflow and behavior:** Select bodies, choose new part names and grouping, and choose associative derived parts or independent copies. Preview which sketches/datums or source references remain in the original definition. Place resulting occurrences so the assembly geometry does not jump. Prevent cycles and avoid duplicating ownership of the same editable result.

**Complete when:** Promote an enclosure and lid, reuse the lid elsewhere, and edit the original. Associative and independent modes behave as declared; placement, internal references, undo, and relocation remain correct.

<a id="f009"></a>
### F009 — Separate navigator tabs

**Owning tasks:** 7.2, 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U01 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Separate assembly structure from modeling history without forcing users to interpret a mixed tree.

**Workflow and behavior:** The Assembly Navigator shows occurrences and hierarchy; the Feature Navigator shows the work part's inputs/history/results. Switching tabs preserves relevant expansion, selection, scroll, and filter state. Selecting a tree item highlights the corresponding occurrence or feature in the viewport, with definition versus occurrence context explicit.

**Complete when:** A repeated component is selected through its exact occurrence in the assembly tab; switching to its feature tab reveals the correct definition and does not accidentally change the work part.

<a id="f010"></a>
### F010 — Optional simultaneous display

**Owning tasks:** 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U01 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Let users see structure and feature history together when screen space and the task justify it.

**Workflow and behavior:** Support docking/splitting the two navigator views independently while keeping one selection/context service. Remember layouts per user, provide a reset, and accommodate small screens and high DPI. Closing or moving a panel must not alter model state or leave duplicate active edit contexts.

**Complete when:** Dock both navigators, edit a nested component, switch work parts, then restore the default layout. Both panels stay synchronized and keyboard focus remains predictable.

<a id="f011"></a>
### F011 — Work part versus displayed assembly

**Owning tasks:** 10.6, 12.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A04, U01 · **First delivery:** P1/P4 · **Likely scope:** Core/UI

**Goal:** Make it unmistakable where a new feature will be created while the surrounding assembly remains visible.

**Workflow and behavior:** Provide explicit Set Work Part/Edit Component and Return to Parent actions, a breadcrumb or equivalent context indicator, and restrained highlighting of editable versus contextual geometry. Selecting a component is not automatically permission to edit its definition. Resolve nested occurrence paths and reject edits to unloaded or read-only sources with guidance.

**Complete when:** Create a feature while viewing three identical occurrences. The UI identifies the edited definition and occurrence context; all intended shared instances update, and no feature lands in the displayed parent accidentally.

<a id="f012"></a>
### F012 — Body-oriented filtering

**Owning tasks:** 7.2, 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U02 · **First delivery:** P4 · **Likely scope:** Feature/UI

**Goal:** Find the operations responsible for a selected body without introducing body-owned histories again.

**Workflow and behavior:** Filter the part history by contributors to one or several body results, optionally including upstream inputs and downstream consumers. Clearly indicate that the tree is filtered, preserve access to the full history, and handle operations contributing to multiple results. Filtering must not suppress features or alter execution.

**Complete when:** Selecting a body created by a Boolean displays the contributing features and relevant inputs. Clearing the filter restores the full tree without any model or visibility mutation.

<a id="f013"></a>
### F013 — Navigator columns

**Owning tasks:** 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U02 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Expose important model state in the tree so users need not open properties to diagnose routine problems.

**Workflow and behavior:** Offer configurable visibility, suppression, error/stale state, source file, reference set, and modified/read-only columns. Use distinct icons and text/tooltips for different states. Source and status values are derived from the model; toggles call validated commands and cannot bypass loading, ownership, or recompute rules.

**Complete when:** A hidden but unsuppressed component, a suppressed feature, an unloaded occurrence, and a failed feature are visibly distinguishable. Sorting columns changes presentation only and editing a state is undoable where appropriate.

<a id="f014"></a>
### F014 — Feature organization

**Owning tasks:** 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U02 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Keep large part histories navigable through names, folders, comments, and targeted search.

**Workflow and behavior:** Support renaming, lightweight folders/groups, descriptions or comments, feature-type filters, and search by labels and useful metadata. Clearly distinguish a presentation folder from an operation group with execution semantics. Preserve stable identifiers through renaming and avoid turning a drag into a reorder without an explicit valid operation.

**Complete when:** Organize and rename a long feature sequence, then search for a hole and its comment. Model order and references are unchanged; folders and comments persist after reopening.

<a id="f015"></a>
### F015 — Dependency inspection

**Owning tasks:** 7.5, 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U02, A05 · **First delivery:** P3/P4 · **Likely scope:** Feature/UI

**Goal:** Show why a feature depends on another and what an edit or deletion could affect.

**Workflow and behavior:** From a feature, reveal direct inputs, target bodies, upstream dependencies, downstream consumers, and external sources using highlights and a compact dependency view. Allow navigation between nodes and differentiate direct from transitive dependencies. Use the actual execution graph rather than reconstructing dependency assumptions from tree order.

**Complete when:** Selecting a shared sketch reveals both consuming extrusions; selecting one extrusion shows a downstream fillet and drawing reference. The view handles cycles rejected by the system and missing references explicitly.

<a id="f016"></a>
### F016 — History controls

**Owning tasks:** 7.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U08 · **First delivery:** P3/P4 · **Likely scope:** Core/Feature

**Goal:** Allow users to inspect earlier states and insert or reorder features without corrupting dependencies.

**Workflow and behavior:** Provide a rollback marker or equivalent edit position, an explicit return-to-tip action, and insertion/reorder only when the dependency graph permits it. Show what becomes temporarily inactive and why a proposed move is invalid. Distinguish rollback display from committed suppression and ensure downstream stale results are labeled.

**Complete when:** Insert a supported feature before a fillet, reject moving a consumer ahead of its input, and return to the tip. Undo and save/reopen retain the intended sequence and no transient rollback state is mistaken for final geometry.

<a id="f017"></a>
### F017 — Shared part definitions

**Owning tasks:** 12.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A03 · **First delivery:** P2/P6 · **Likely scope:** Core/Feature

**Goal:** Reuse a part in one or many assemblies while keeping one editable source definition.

**Workflow and behavior:** Occurrences reference a stable definition and carry their own placement. Editing through an occurrence clearly edits the shared source; notify users of the scope through the command context. Update loaded dependents and show stale/external update status for sources that must be reloaded. Do not promise automatic edits to closed files.

**Complete when:** Edit a bracket used twice in one assembly and once in another. All loaded occurrences reflect the change, their placements remain independent, and reopened external documents resolve the updated source predictably.

<a id="f018"></a>
### F018 — Occurrence-specific properties

**Owning tasks:** 12.1, 12.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A03, B01 · **First delivery:** P3/P6 · **Likely scope:** Feature

**Goal:** Allow local presentation and placement differences without accidentally making a separate part.

**Workflow and behavior:** Store placement, visibility, allowed color/material-display overrides, and reference-set selection on the occurrence, with inheritance/reset-to-source behavior. Distinguish visual material overrides from engineering material or configuration changes that affect mass/FEM. Nested overrides resolve through the selected occurrence path.

**Complete when:** Color or hide one of several bolts and move another. The source geometry and unselected instances remain unchanged; resetting an override restores inherited behavior and survives save/reopen.

<a id="f019"></a>
### F019 — Make Unique

**Owning tasks:** 12.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A03 · **First delivery:** P2/P6 · **Likely scope:** Feature/Core

**Goal:** Intentionally break shared geometry identity when one occurrence must become a different design.

**Workflow and behavior:** Preview the new definition, destination document, copied internal dependencies, and external links to retain or detach. Remap internal references, assign new identities, and replace only the selected occurrence while preserving placement and recoverable relationships. For subassemblies, explicitly choose shallow versus supported deep duplication.

**Complete when:** Make one repeated bracket unique, change its hole spacing, and reopen the project. Original instances stay linked to the original; the unique copy has no accidental internal references back to its former source.

<a id="f020"></a>
### F020 — Reference sets

**Owning tasks:** 12.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B01 · **First delivery:** P3/P6 · **Likely scope:** Feature/Core

**Goal:** Choose a part's exposed representation without changing what the part fundamentally contains.

**Workflow and behavior:** Provide Entire Part, Model, Empty, and named custom sets of geometry/datums. Document what Model includes and how new members are handled. An occurrence selects a set; source editing manages set membership. Empty retains the occurrence, identity, placement, and product-structure role. Commands explain when requested geometry is outside the selected set.

**Complete when:** Switch a subassembly among full, simplified, datum-only, and empty sets. Placement, BOM role, shared definition, and saved structure remain intact; missing representation is not mistaken for missing source.

<a id="f021"></a>
### F021 — Separate loading controls

**Owning tasks:** 12.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B06 · **First delivery:** P1/P6 · **Likely scope:** Core

**Goal:** Reduce resource use without overloading visibility or reference-set choices.

**Workflow and behavior:** Represent fully loaded, lightweight, and unloaded states independently. Retain identifiers, bounds/proxy information, source location, and assembly structure where supported. Commands requiring exact geometry resolve it deliberately or report a blocker. Define cache freshness and what can be inspected versus edited in each state.

**Complete when:** Unload a component, keep its occurrence in the tree, and later reload it at the same placement. Exact measurements, CAM, and validation cannot silently use a stale proxy as authoritative geometry.

<a id="f022"></a>
### F022 — Component replacement

**Owning tasks:** 12.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B04, A05 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Swap a component source while retaining placement and as much valid assembly intent as possible.

**Workflow and behavior:** Select one occurrence or an explicitly chosen set, preview the replacement, and map published interfaces or stable reference equivalents. Preserve placement by default; offer deliberate alignment alternatives. Classify relationships as preserved, remapped, or unresolved rather than matching arbitrary face numbers. Allow cancellation before committing.

**Complete when:** Replace a bearing with a different size. Valid datum-based mates remain; incompatible face references are listed for repair; other shared occurrences change only if selected.

<a id="f023"></a>
### F023 — Component patterns and mirrors

**Owning tasks:** 12.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B04 · **First delivery:** P6 · **Likely scope:** Feature

**Goal:** Create repeated assembly occurrences with clear linkage, skipped positions, and handedness.

**Workflow and behavior:** Support bounded linear/circular patterns first, then other useful distributions. Store a seed definition, transforms, parameters, and stable instance keys. Mirrors must explain whether they reflect placement, create a mirrored definition, or create independent geometry; changing handedness is not ordinary rigid placement. Skipped instances remain identifiable for later edits.

**Complete when:** Change a bolt-pattern count without silently redirecting surviving mate/BOM references. A mirrored handed bracket has the declared shared/unique behavior and correct orientation, quantity, and mass.

<a id="f024"></a>
### F024 — Configurations and arrangements

**Owning tasks:** 12.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B05 · **First delivery:** P1 semantics; later P6 · **Likely scope:** Core

**Goal:** Separate design variants from saved assembly positions and presentation states.

**Workflow and behavior:** Configurations own declared parameter/suppression overrides and their identity; arrangements own component positions/joint settings or supported presentation state. Define whether occurrences can select different configurations of one source and how cache keys and derived results are distinguished. Keep flexible subassembly evaluation scoped to occurrence context instead of overwriting the rigid source.

**Complete when:** Use two size configurations in one assembly, save a folded/unfolded arrangement, and reopen. Editing one configuration or arrangement does not unintentionally change another; dependencies, BOM policy, and active variant are explicit.

<a id="f025"></a>
### F025 — Unified modeling workspace

**Owning tasks:** 8.4, 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U11, U03 · **First delivery:** P3/P4 · **Likely scope:** UI/Feature

**Goal:** Let users perform ordinary modeling without knowing whether a command historically belongs to Part or PartDesign.

**Workflow and behavior:** Offer a coherent modeling workspace backed by shared feature contracts, with task-oriented access to sketching, solids, surfaces, and assembly actions. Preserve advanced workbench access and expose incompatible legacy objects honestly. Command availability follows selection/edit context, while search explains unavailable commands instead of silently hiding every discovery path.

**Complete when:** Complete a bracket and enclosure using the unified workspace without switching workbenches merely to obtain a Boolean operation. Retained legacy commands and downstream workbenches continue to resolve the correct edit context.

<a id="f026"></a>
### F026 — Extrude

**Owning tasks:** 3.6, 3.8, 7.4, 10.2, 10.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U03, U09, U10 · **First delivery:** P2/P4 · **Likely scope:** UI/Core

**Goal:** Create and edit extruded material through one guided command with an efficient direct path.

**Workflow and behavior:** Select curves/regions, establish a normal or supported custom direction, enter extents, and review the contextual New Body/Unite suggestion or explicit Subtract/Intersect choice. Highlight targets and solid/sheet output. Keep Pad and Pocket as presets, with Pocket explicitly subtractive. Support returning to earlier inputs without erasing valid choices.

**Complete when:** Model a base, add an intersecting boss, create a separate rib blank, and cut a pocket using the same feature semantics. Editing extents preserves accepted operation/targets; invalid inputs cannot partially modify the part.

<a id="f027"></a>
### F027 — Revolve

**Owning tasks:** 3.9, 8.2, 10.2, 10.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U03, U09, U10 · **First delivery:** P4 · **Likely scope:** UI/Core

**Goal:** Create rotational features through the same clear intent and target workflow as Extrude.

**Workflow and behavior:** Select profiles and an axis from a datum, line, or supported cylindrical reference; show the axis and rotation sense. Offer partial/full revolution and applicable symmetric/two-sided angle controls. Keep Revolution/additive Revolve and Groove/Subtract presets. Explain profiles crossing the axis, self-intersections, and invalid solid/sheet choices.

**Complete when:** Build a turned part and its annular groove, reverse the rotation, and edit the axis/angle. Guided and direct entry produce equivalent editable results; failed full or partial revolutions preserve the last committed model.

<a id="f028"></a>
### F028 — Consistent Sweep and Loft

**Owning tasks:** 3.3, 13.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G03, U06 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Use familiar profile, guide, output-type, and Boolean conventions when creating nonprismatic shapes.

**Workflow and behavior:** Sweep collects section, path, and supported orientation/scaling controls; Loft collects ordered sections and optional guides. Expose solid versus sheet and targets consistently with Extrude/Revolve, but show only geometrically meaningful extents. Preview section orientation and likely twist before committing. Keep algorithm-specific advanced controls available without inventing equivalence between sweep and loft.

**Complete when:** Create a constant-section routed feature and a changing-section transition. Reorder or reverse sections, edit a guide, and verify deterministic results, target behavior, and clear unsupported-input diagnostics.

<a id="f029"></a>
### F029 — Common extent controls

**Owning tasks:** 8.1, 10.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U06 · **First delivery:** P4/P7 · **Likely scope:** Feature

**Goal:** Make termination choices consistent and understandable across commands that support them.

**Workflow and behavior:** Offer Distance, Symmetric, Two-sided, Through All, To Face, and Offset from Face where applicable. Label total versus per-side distance, positive direction, start offset, and reference face. Store associative face/limit references and explicitly define their behavior after edits. Do not expose a mode on a command that cannot implement its semantics.

**Complete when:** An extrusion terminated at a selected face updates when that face moves; symmetric and two-sided values produce the documented lengths. A removed limiting face produces a repairable error rather than becoming a fixed distance silently.

<a id="f030"></a>
### F030 — Selection collectors

**Owning tasks:** 8.1, 10.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U06, A04 · **First delivery:** P3/P4 · **Likely scope:** UI/Feature

**Goal:** Make every requested geometric role visible so users know what to select next.

**Workflow and behavior:** Provide labeled Profile, Axis, Target Bodies, Guides, and Limits collectors with counts, type hints, and active-role highlighting. Users can activate, clear, replace, or inspect individual entries; selecting a row highlights its geometry and occurrence path. Validate type, scope, ordering, and duplication before accepting picks.

**Complete when:** A user can identify and replace the wrong guide or target without restarting a command. Ambiguous picks go through disambiguation, and selected geometry cannot silently fill a different role.

<a id="f031"></a>
### F031 — Preselection and postselection

**Owning tasks:** 8.1, 10.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U06, A07 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Support experienced users who select first and beginners who launch a command first.

**Workflow and behavior:** Map preselected items to valid roles only when unambiguous; preserve unresolved items for a visible choice or explain why they were ignored. Postselection uses the same collectors and checks. Switching selection order must not change geometry semantics, and invalid preselection should leave a useful command rather than fail opaquely.

**Complete when:** Run Extrude with a profile preselected and with no initial selection; the resulting feature parameters agree. Mixed profile/target selection is handled deterministically and Cancel restores the prior selection where appropriate.

<a id="f032"></a>
### F032 — Consistent Apply/OK/Cancel

**Owning tasks:** 8.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A07, U09 · **First delivery:** P3/P4 · **Likely scope:** Feature/UI

**Goal:** Make repeated operations and reversibility predictable across all modeling dialogs.

**Workflow and behavior:** OK validates, commits one operation, and exits; Apply commits and keeps the command ready with documented retained/reset inputs; Cancel discards only the current uncommitted operation. Escape handling, preview rollback, and selection restoration follow a shared lifecycle. If several Apply operations were committed, subsequent Cancel must not erase them unexpectedly.

**Complete when:** Apply two holes, begin a third, then Cancel. Exactly the first two remain as sensible undo steps; failed preview or cancellation leaves no orphan geometry, references, or hidden temporary objects.

<a id="f033"></a>
### F033 — Command search and shortcut palette

**Owning tasks:** 8.4, 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U04, U11 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Help users find equivalent operations using terminology they already know.

**Workflow and behavior:** Index canonical commands and aliases such as Pad/Extrude, Pocket/Cut, Groove/Revolved Cut, and supported NX/SolidWorks terms. Show concise intent, shortcut, current availability, and a reason or path when unavailable. Keep customization and favorites per user, with a reset and conflict checks. Search aliases invoke the same validated commands.

**Complete when:** Searching Pocket opens subtractive Extrude; an unavailable assembly operation explains the required context. Keyboard users can invoke search, choose a result, and reach the relevant input without a mouse.

<a id="f034"></a>
### F034 — Modifier-based multiselection

**Owning tasks:** 10.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U05 · **First delivery:** P4/P5 · **Likely scope:** UI

**Goal:** Prevent accidental accumulation of sketch selections while keeping deliberate multiselection fast.

**Workflow and behavior:** Plain click replaces the current set; Ctrl toggles/adds and Shift provides the documented extension/range behavior. Allow consistent configurable presets where platform conventions require them. Window selection may select multiple entities in one gesture. Coordinate these rules with drawing tools, dragging, and the separate auto-inference override key.

**Complete when:** Select one sketch line, click another, then use modifiers to form a two-line set. Selection counts, eligible constraints, and deselection are predictable in the viewport and tree without breaking geometry creation.

<a id="f035"></a>
### F035 — Selection filters

**Owning tasks:** 10.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U05 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Reduce accidental picks by letting users restrict selectable entity types.

**Workflow and behavior:** Expose points/vertices, edges, faces, bodies, components, sketches, and features, with a clear active-filter indicator and quick reset. Command-specific filters refine the global policy without becoming a persistent trap. Respect keyboard navigation and show why a visible object cannot be selected under the active filter.

**Complete when:** In a dense assembly, face-only selection cannot accidentally select a whole component. Leaving a command restores the documented previous filter state and the user can recover from an empty result easily.

<a id="f036"></a>
### F036 — Selection scope

**Owning tasks:** 10.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A04, U05 · **First delivery:** P1/P4 · **Likely scope:** Core/UI

**Goal:** Control whether selection addresses local geometry or surrounding assembly context.

**Workflow and behavior:** Provide active-part, selected-component, and whole-assembly scopes with occurrence-path-aware results. Scope is separate from visibility and loading. Commands declare whether they accept contextual references, editable targets, or both; a selectable external face is not automatically a writable target. Make scope changes deliberate and visible.

**Complete when:** During in-context editing, a user can reference a neighboring face while a local Boolean command refuses to alter that neighbor silently. Nested and repeated occurrences resolve the intended path.

<a id="f037"></a>
### F037 — Select Other

**Owning tasks:** 10.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U05 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Resolve overlapping or obscured picks without temporarily dismantling the display.

**Workflow and behavior:** Open a small candidate list or cycling interaction with transient highlights and useful labels/type/context. Order candidates predictably using pick location and scope; allow deeper/hidden candidates only under documented rules. Escape dismisses without replacing the existing selection. Keep filtering and occurrence identity intact.

**Complete when:** Select the rear of two coincident faces and one of overlapping repeated components. Hover/cycle previews accurately identify candidates, and the final selection matches the preview.

<a id="f038"></a>
### F038 — Selection intent rules

**Owning tasks:** 10.5, 7.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U05, A05 · **First delivery:** P3/P4 · **Likely scope:** Feature/Core

**Goal:** Let users specify a meaningful geometric set instead of manually picking every member.

**Workflow and behavior:** Offer tangent chain, connected edges, complete loop, same-radius faces, and feature-owned faces where supported. Preview included entities and expose tolerance/boundary choices. Distinguish storing an associative rule that reevaluates after edits from freezing an explicit selection set; avoid silently expanding operation scope when topology changes.

**Complete when:** A fillet uses an accepted tangent chain and a later edge split resolves according to the stored policy. Unexpected added branches or ambiguous loops produce a visible choice or repair rather than an unnoticed broad edit.

<a id="f039"></a>
### F039 — Window versus crossing selection

**Owning tasks:** 10.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U05 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Make rectangle selection communicate whether partial overlap counts.

**Workflow and behavior:** Provide distinct enclosed-only and crossing modes through a documented drag-direction or explicit setting, with visible styling during the gesture. Define whether hidden/back-facing geometry is eligible and apply type/scope filters consistently. Preserve a deliberate modifier policy for replacing, adding, and removing window results.

**Complete when:** A rectangle around part of a sketch selects only fully enclosed entities in one mode and crossing entities in the other. The same behavior holds at different zoom levels and does not accidentally include hidden assembly geometry.

<a id="f040"></a>
### F040 — Temporary isolate/hide

**Owning tasks:** 10.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U05 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Inspect a subset quickly and return to the previous display without manual reconstruction.

**Workflow and behavior:** Isolate selected objects, hide selected objects, and restore the prior visibility snapshot using explicit temporary-display actions. Handle nested isolates and newly created objects predictably. Visibility must not imply suppression, exclusion from a Boolean target set, or removal from BOM/validation.

**Complete when:** Isolate a component, hide one of its bodies, inspect it, and restore. The prior assembly visibility returns; no suppressed or reference-only states change and retained operation targets remain intact.

<a id="f041"></a>
### F041 — Predictable navigation

**Owning tasks:** 8.4, 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U04, U11 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Make camera movement and sketch entry familiar and controllable.

**Workflow and behavior:** Offer configurable mouse/navigation presets, a visible or inferable rotation center, zoom-to-selection, fit-all, standard views, and orthographic sketch orientation. Preserve the previous 3D view when entering/exiting sketch edit and avoid wild camera jumps on small or off-origin geometry. Resolve shortcut conflicts with selection and command gestures.

**Complete when:** Orbit about a selected feature in a large assembly, enter a rotated sketch, and return to the previous view. Mouse presets and high-DPI settings remain usable without changing model coordinates.

<a id="f042"></a>
### F042 — Improved automatic relations

**Owning tasks:** 11.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S01 · **First delivery:** P5 · **Likely scope:** Feature

**Goal:** Infer common sketch intent as geometry is drawn without creating surprising constraints.

**Workflow and behavior:** Support configurable coincidence, tangent, horizontal/vertical, parallel, perpendicular, and equal inference where the solver supports them. Use screen-space proximity for interaction while respecting geometric tolerances and model units. Prioritize candidates, show what will be added, and distinguish transient snapping from persistent constraints.

**Complete when:** Draw representative lines, circles, and arcs with intended inferences and near-miss counterexamples. Only accepted relations persist, the override prevents unwanted inference, and dense geometry does not create arbitrary constraints.

<a id="f043"></a>
### F043 — Constraint preview

**Owning tasks:** 11.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S01 · **First delivery:** P5 · **Likely scope:** UI/Feature

**Goal:** Show the relationship about to be added before the user commits geometry.

**Workflow and behavior:** Display a legible relation glyph and highlight its operands as the pointer approaches a valid inference. Provide a temporary suppression key independent of Ctrl/Shift multiselection, plus optional inference controls. Preview state never mutates the committed sketch and disappears when the candidate or tool changes.

**Complete when:** Approach a tangent and then a coincident condition, suppress one inference, and complete drawing. The persisted relation matches the final preview and no abandoned candidate survives.

<a id="f044"></a>
### F044 — Cursor-adjacent constraint palette

**Owning tasks:** 11.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S02, S07 · **First delivery:** P5 · **Likely scope:** UI/Feature

**Goal:** Offer relevant constraints close to the user's selection without forcing a toolbar search.

**Workflow and behavior:** After selection, show a compact palette driven by the shared eligibility service. Use a reachable pointer corridor or dismissal delay, place it away from selected geometry and screen edges, and dismiss when the pointer genuinely leaves. Provide keyboard access, stable ordering, high-DPI sizing, and a user preference to disable it.

**Complete when:** Select one line and two lines, move into the palette, apply a relation, and move away. It remains reachable, shows the correct actions/states, and never applies a constraint merely because the pointer crossed it.

<a id="f045"></a>
### F045 — Smart Dimension

**Owning tasks:** 11.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S03 · **First delivery:** P5 · **Likely scope:** UI/Feature

**Goal:** Infer the useful dimensional relationship from geometry while allowing explicit control.

**Workflow and behavior:** For suitable selections offer length, angle, radius, diameter, horizontal/vertical spacing, and other supported measurements. Preview alternatives based on placement or an explicit switch; show units and driving versus reference state. Route overconstrained candidates through shared validation rather than silently converting or deleting existing dimensions.

**Complete when:** Dimension a line, circle, pair of lines, and point spacing. Users can deliberately select radial versus diameter or projected versus aligned length, and edits preserve their chosen dimension type.

<a id="f046"></a>
### F046 — Dimension during drawing

**Owning tasks:** 11.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S03 · **First delivery:** P5 · **Likely scope:** Feature

**Goal:** Let users establish exact geometry while drawing instead of repeatedly drawing approximately and editing afterward.

**Workflow and behavior:** Expose temporary numeric fields for supported line lengths/angles, rectangle dimensions, circle diameters, and slot dimensions. Define field cycling, locked versus inferred values, expression/unit entry, and Escape behavior. Commit a coherent set of geometry and constraints as one undoable action; keep advanced options accessible.

**Complete when:** Create a rectangle and slot from typed dimensions, correct a field before commit, and cancel another attempt. The resulting dimensions are editable driving constraints and no half-created geometry remains.

<a id="f047"></a>
### F047 — Visual degrees of freedom

**Owning tasks:** 11.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S04 · **First delivery:** P5 · **Likely scope:** Feature/UI

**Goal:** Show what can still move and distinguish incompletely constrained geometry from a failed solve.

**Workflow and behavior:** Use visual states and optional movement-direction indicators for translation, rotation, size, or other supported freedoms, supplemented by text rather than color alone. Distinguish grounded/fixed geometry, reference geometry, solver conflict, and remaining freedom. Do not present a simple count as a complete diagnosis when freedoms are coupled.

**Complete when:** A partly constrained sketch reveals the intended remaining movement; adding a supported relation updates the indication. A conflicting sketch is clearly different from a merely underconstrained one.

<a id="f048"></a>
### F048 — Constraint repair

**Owning tasks:** 11.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S04, S07 · **First delivery:** P5 · **Likely scope:** Feature/Core

**Goal:** Explain overconstraint and help users make a deliberate repair while preserving design intent.

**Workflow and behavior:** Separate existing, redundant, conflicting, and unsupported constraints. Highlight implicated geometry and candidate relations, preview the effect of removing/replacing a relation, and show resulting freedom where feasible. Candidates may be conservative solver-derived sets rather than a claimed unique cause. Never delete constraints automatically to make a new action succeed.

**Complete when:** Create a redundant dimension and a genuine conflict. The UI distinguishes them, offers an understandable reversible repair, and leaves the original sketch unchanged if the user cancels.

<a id="f049"></a>
### F049 — Sketch repair

**Owning tasks:** 11.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S06 · **First delivery:** P5 · **Likely scope:** Feature

**Goal:** Find small defects that prevent profiles from becoming valid regions or downstream features.

**Workflow and behavior:** Detect gaps, duplicate entities, tiny segments, overlaps, self-intersections, and unsupported loops using explicit model-scale tolerances. Present a navigable results list with zoom/highlight and proposed fixes. Separate diagnostic tolerance from automatic merging tolerance, and preview changes to constraints before deleting or merging geometry.

**Complete when:** Repair an almost-closed profile and a duplicated edge deliberately. The intended region becomes usable, preserved dimensions still express the same design, and ignoring a tiny segment does not falsely certify a valid profile.

<a id="f050"></a>
### F050 — Power trim/extend

**Owning tasks:** 11.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S06 · **First delivery:** P5 · **Likely scope:** Feature

**Goal:** Remove or extend sketch segments with fewer selections while keeping the result understandable.

**Workflow and behavior:** Support dragging across segments to trim and deliberate extension to a selected or inferred boundary. Preview the portion removed/added, distinguish construction geometry, and retain valid dimensions/relations or report which will be removed. Bundle one drag gesture into a sensible undo step and avoid silently changing unrelated loops.

**Complete when:** Trim several crossing lines, extend an arc to a boundary, and undo. Geometry matches the preview; surviving constraints remain valid and removed constraints are explained rather than left dangling.

<a id="f051"></a>
### F051 — Region selection

**Owning tasks:** 11.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S06, A05 · **First delivery:** P3/P5 · **Likely scope:** Feature/Core

**Goal:** Use closed areas inside a complex sketch without copying or deleting the rest of the sketch.

**Workflow and behavior:** Highlight bounded regions and nested holes, support multiple compatible regions, and explain ambiguous/open/self-intersecting boundaries. Define how selected regions are identified across sketch edits and how changes that split/merge regions are repaired. Keep full-sketch versus region inputs explicit in feature parameters.

**Complete when:** Extrude one compartment of a multi-region sketch and later move an internal boundary. The intended region updates or requests repair; the command does not silently extrude every newly formed region.

<a id="f052"></a>
### F052 — Associative external geometry

**Owning tasks:** 11.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S05, B03 · **First delivery:** P5 · **Likely scope:** Feature/Core

**Goal:** Bring useful neighboring geometry into a sketch through projection or true intersection with clear provenance.

**Workflow and behavior:** Offer projected edges, curve/plane intersection points, and face/plane intersection curves as distinct operations. Show source part/occurrence, transform, and association status. Define tangent, coplanar, coincident, disjoint, and multiple-result cases; a surface intersection is not necessarily a straight line. External inputs obey publication/scope and cycle rules.

**Complete when:** Intersect an angled edge and curved surface with a sketch plane, then move the source. Points/curves update correctly or report ambiguity; independent copies and associative references remain visibly distinct.

<a id="f053"></a>
### F053 — Sketch reuse tools

**Owning tasks:** 11.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S06, A05 · **First delivery:** P5 increments · **Likely scope:** Feature/Core

**Goal:** Reuse proven sketch content while controlling which relationships remain shared.

**Workflow and behavior:** Provide constraint-preserving copy/paste with transform, reusable profiles, blocks, and sketch patterns in separate increments. Remap internal geometry/constraint identifiers; require a choice for external references. Define block-local coordinates, editable block instances, explode behavior, and pattern members before claiming full block support.

**Complete when:** Copy a constrained slot, rotate/place it, and change its dimensions. Internal relations survive; external links follow the declared policy; block or pattern edits affect the intended members and remain undoable.

<a id="f054"></a>
### F054 — Interactive feature handles

**Owning tasks:** 8.4.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U06 · **First delivery:** P4/P7 · **Likely scope:** UI/Feature

**Goal:** Adjust common feature values visually while retaining exact parametric control.

**Workflow and behavior:** Expose handles for supported length, angle, radius, and offset values, with clear direction, snapping, numeric entry, and current units. Dragging changes a transient preview; typed values and expressions use the same parameter validation. Indicate limits and invalid ranges without committing unusable geometry.

**Complete when:** Drag an extrusion handle, type an exact value, cancel a second edit, and reopen the part. The stored parameter is exact and editable, while canceled or intermediate previews leave no document changes.

<a id="f055"></a>
### F055 — Hole wizard

**Owning tasks:** 13.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G06 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Create standard, documented holes through one guided placement and specification workflow.

**Workflow and behavior:** Separate hole locations from hole definition: select/reuse position sketches or points, then choose simple, counterbore, countersink, or thread specification and extent. Use versioned standard tables with explicit units/source and user overrides. Distinguish cosmetic thread metadata from actual helical geometry and communicate cost/compatibility.

**Complete when:** Create repeated counterbores and tapped holes, edit their standard/size, and produce supported drawing callouts. Location links, depth, thread representation, targets, and validation remain consistent after parameter changes.

<a id="f056"></a>
### F056 — Unified patterns

**Owning tasks:** 3.7, 13.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G06 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Repeat features or bodies with one recognizable interface and explicit pattern semantics.

**Workflow and behavior:** Offer linear, circular, curve-driven, and table-driven patterns in staged increments, with count/spacing, orientation, seeds, and skipped members. Distinguish copying resulting geometry from reevaluating a feature at each location when they yield different results. Preserve stable member keys for downstream references and report invalid members.

**Complete when:** Pattern a hole across uneven geometry, skip two members, and change count/spacing. Valid members retain predictable references; unsupported members are identified and do not silently change the chosen evaluation mode.

<a id="f057"></a>
### F057 — Feature/body mirror

**Owning tasks:** 13.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G06 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Make symmetry operations explicit about what is mirrored and whether results remain linked.

**Workflow and behavior:** Select features or body results and a mirror plane, then choose supported mirrored geometry, associative copies, or independent results. Preview Boolean target behavior and handedness. Feature mirroring must map inputs/targets under its declared semantics rather than merely duplicating viewport graphics.

**Complete when:** Mirror an asymmetric bracket body and a hole feature, edit the seed, and verify the chosen linkage. Reflected geometry, labels, target scope, and saved feature history remain correct.

<a id="f058"></a>
### F058 — Improved fillets/chamfers

**Owning tasks:** 13.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G06 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Make edge treatment easier to define and diagnose when complex geometry fails.

**Workflow and behavior:** Use edge collectors with tangent propagation, radius/offset previews, and supported variable-radius and corner controls. Separate attempted capabilities from validated kernel support. Localize failing edges or corners and let users revise a subset without losing valid selections. Keep tolerance and reference-repair behavior explicit.

**Complete when:** Create a chain fillet and a supported variable-radius case, then force a corner failure. The UI identifies a useful failing region, preserves prior geometry, and allows correction without rebuilding the entire selection.

<a id="f059"></a>
### F059 — Shell, draft, ribs, and webs

**Owning tasks:** 13.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G06 · **First delivery:** P7 increments · **Likely scope:** Feature/Core

**Goal:** Provide consistent guided workflows for common manufacturing-oriented features.

**Workflow and behavior:** Shell collects removed faces and thickness/side; Draft collects neutral reference, pull direction, target faces, and angle; Rib/Web collects profiles, thickness, direction, and extent/targets. Explain when thickness, draft, or intersections make the result invalid. Keep each operation a separate bounded implementation with common lifecycle and reference behavior.

**Complete when:** Create and edit a thin enclosure, a drafted wall, and a reinforcing rib. Direction/thickness previews match final results; invalid thin regions or missing intersections produce localized, reversible failures.

<a id="f060"></a>
### F060 — Split and trim bodies

**Owning tasks:** 4, 13.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G01 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Divide solids or sheets with an explicit preview of which regions remain.

**Workflow and behavior:** Choose planes, surfaces, or bodies as tools, select target bodies, and preview resulting regions with keep/remove choices. Specify retained-tool behavior and distinguish a nondestructive split into multiple results from trimming away regions. Persist region choices/provenance and treat later ambiguous splits as repair cases.

**Complete when:** Split a housing with a plane, retain both halves, and trim one with a surface. Edit the tool and verify output identities, target scope, undo, and downstream-reference outcomes.

<a id="f061"></a>
### F061 — Direct editing

**Owning tasks:** 13.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G07 · **First delivery:** Late P7 · **Likely scope:** Feature/Core

**Goal:** Make bounded changes to imported and native geometry without pretending to recover its original feature history.

**Workflow and behavior:** Offer move, offset, replace, and delete-and-heal face operations as new editable steps. Show affected adjacent topology and whether tangent propagation or healing is supported. Do not alter an upstream feature's parameters silently. Limit initial support to reproducibly valid shape classes and expose failures explicitly.

**Complete when:** Offset an imported planar face, remove a suitable hole with healing, and undo. Native downstream references either remain valid or request repair, and unsupported healing leaves the original model intact.

<a id="f062"></a>
### F062 — Feature recognition

**Owning tasks:** 13.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G08 · **First delivery:** Late P7 after spike · **Likely scope:** Core

**Goal:** Recover useful editable structure from suitable imported solids while acknowledging incomplete information.

**Workflow and behavior:** Detect bounded candidates such as analytic holes, pockets, or fillets; preview recognized parameters and residual geometry before conversion. Label uncertain or unsupported candidates and retain the original solid as a recoverable source. Recognition is a new inferred model, not proof of the original designer's intent.

**Complete when:** Recognize a documented test set, edit an accepted hole diameter, and compare the unchanged surrounding geometry. False positives can be rejected and unrecognized portions remain usable rather than disappearing.

<a id="f063"></a>
### F063 — Through-curves surfaces

**Owning tasks:** 13.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G03 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Construct a controlled surface through ordered sections, using guides to shape correspondence.

**Workflow and behavior:** Collect sections in order, optional guide curves, start/end conditions, and curve directions; show correspondence markers and twist previews. Validate guide/section compatibility and supported intersections within explicit tolerances. Expose meaningful continuity controls only when the construction supports them and retain all input associations.

**Complete when:** Build a transition through three sections with guides, reverse one section, and adjust correspondence. The preview identifies twist; committed geometry meets documented interpolation/tolerance requirements and updates after source edits.

<a id="f064"></a>
### F064 — Curve-network surfaces

**Owning tasks:** 13.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G04 · **First delivery:** P7 after spike · **Likely scope:** Core

**Goal:** Build surfaces from two intersecting curve families when through-sections alone cannot express the intended shape.

**Workflow and behavior:** Collect and order the two curve directions, detect missing/inconsistent intersections, and show network cells/corners. Specify supported open/closed networks, trimming, interpolation, and approximation tolerance. Start with a bounded regular network instead of promising arbitrary networks or commercial-kernel equivalence.

**Complete when:** Construct and edit a regular network fixture, reject incompatible crossings with localized diagnostics, and verify claimed interpolation and surface validity independently of visual smoothness.

<a id="f065"></a>
### F065 — Boundary continuity

**Owning tasks:** 13.3, 15.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G04, I02 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Control how a new surface joins neighboring geometry and verify the requested level.

**Workflow and behavior:** At each supported boundary, choose positional, tangent, or curvature continuity with the required adjacent reference and orientation. Explain unsupported boundary combinations, approximation limits, and conflicting conditions. Treat continuity as a measured geometric property, not an icon or display shading choice.

**Complete when:** Create representative G0/G1/G2 supported joins, alter neighboring geometry, and inspect them using numerical continuity checks and visual tools. A failed condition is reported rather than silently downgraded.

<a id="f066"></a>
### F066 — Trim/untrim/extend surfaces

**Owning tasks:** 13.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G01, G02 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Edit sheet boundaries while preserving the distinction between underlying surfaces and trimming loops.

**Workflow and behavior:** Trim with selected curves/surfaces and pick kept regions; untrim exposes recoverable underlying surface domains; extend grows supported boundaries using a stated geometric method. Preview new boundaries and self-intersections. Do not claim untrim can recover original design intent or missing geometry from every imported sheet.

**Complete when:** Trim a sheet into two regions, restore a supported original domain, and extend an edge. Tool associations and region selections survive edits or become explicitly unresolved, without creating invalid shells.

<a id="f067"></a>
### F067 — Thicken sheet bodies

**Owning tasks:** 13.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G02 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Convert valid sheet geometry into material with a clear side, thickness, and Boolean result.

**Workflow and behavior:** Offer one-sided, opposite-sided, and symmetric thickness with unambiguous total/per-side dimensions. Show normals and side reversal; collect optional union/subtraction targets through common rules. Detect tight curvature, offset self-intersections, and unsuitable open boundaries; distinguish a thickened solid from separate offset sheets.

**Complete when:** Thicken a planar and a curved fixture in each supported direction, then test a radius smaller than the requested thickness. Valid results have the expected volume and failed offsets preserve the source.

<a id="f068"></a>
### F068 — Sew/stitch surfaces

**Owning tasks:** 13.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G02 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Join compatible sheets and reveal where gaps prevent a valid shell or solid.

**Workflow and behavior:** Collect sheets, display free edges/gaps, and use explicit tolerances with a preview of proposed joins. Indicate whether the result is an open shell, closed shell, or valid solid. Avoid silently escalating tolerances to force a join; show any healing/approximation effects and retain source choices.

**Complete when:** Stitch a known enclosure and an intentionally gapped version. The first becomes a verified solid; the second identifies the unresolved gap and cannot be labeled watertight merely because it renders closed.

<a id="f069"></a>
### F069 — Extract/project/intersect curves

**Owning tasks:** 13.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G05 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Generate reusable design curves from existing geometry with clear source and method.

**Workflow and behavior:** Support extracting edges/face boundaries, projecting curves along a chosen direction or supported normal rule, and intersecting bodies/surfaces. Collect source and target roles separately, define multiple/disjoint/tangent results, and preserve association or deliberate snapshot copying. Display approximation tolerance for nonanalytic results.

**Complete when:** Project a curve onto a curved face and intersect two surfaces. Moving a source updates intended results; multiple branches remain identifiable and changed topology cannot silently switch the selected branch.

<a id="f070"></a>
### F070 — Isocline curves

**Owning tasks:** 5, 13.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G05, I02 · **First delivery:** P7 after spike · **Likely scope:** Feature/Core

**Goal:** Create constant-draft-angle curves on a surface relative to a chosen pull direction.

**Local convention:** Preserve Phase 5: normal dot pull = sin(draft angle), with 0 degrees at the silhouette. The supplied normal-angle wording is interpreted through this established convention, not as a change to stored feature semantics.

**Workflow and behavior:** Collect faces, direction, angle, domain, and tolerance; state the normal-orientation and signed/unsigned angle convention. Distinguish isoclines from isoparametric curves and purely visual draft-analysis coloring. Handle zero/multiple curves, singularities, boundary termination, and unsupported surface types explicitly.

**Complete when:** On analytic fixtures, sampled curve points satisfy the stated angle within tolerance. Reversing direction or normals follows the documented convention and does not create unexplained mirrored results.

<a id="f071"></a>
### F071 — Surface quality inspection

**Owning tasks:** 15.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** I02 · **First delivery:** P7/P9 · **Likely scope:** Feature

**Goal:** Help users diagnose shape quality and verify surfacing claims beyond shaded appearance.

**Workflow and behavior:** Provide zebra/reflection lines, curvature combs, continuity checks, and deviation maps with visible scale, sampling, units, and reference geometry. Distinguish approximate display sampling from numerical certification and show unsupported/singular regions. Save useful analysis settings without making them geometry features unless requested.

**Complete when:** Compare intentionally smooth and discontinuous joins and a known deviation fixture. The tools reveal the expected differences; colors/combs use documented scales and cannot substitute for the acceptance tolerance of a surface feature.

<a id="f072"></a>
### F072 — Unified Move/Copy dialog

**Owning tasks:** 10.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U07 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Position or duplicate parts through one consistent interface with precise geometric references.

**Workflow and behavior:** Offer translation, rotation, point-to-point, axis alignment, and coordinate-system alignment, with Move versus Copy explicit. Identify whether the subject is a component occurrence, body transform feature, or supported geometry copy. Show source and destination references, transform order, and a live ghost preview; copy mode declares shared versus unique definition behavior.

**Complete when:** Move a repeated component point-to-point, rotate it, and copy it. The correct occurrence changes, shared source geometry stays intact, and Cancel/Undo restore placement without residual constraints.

<a id="f073"></a>
### F073 — Relocatable manipulator

**Owning tasks:** 10.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U07 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Place the movement triad where it makes a positioning task intuitive without changing the part itself.

**Workflow and behavior:** Relocate the manipulator to a vertex, edge midpoint, circle center, datum, coordinate system, or supported inferred point. Orient its axes from explicit references and distinguish editing the manipulator from moving the object. Define whether the chosen pivot is temporary, remembered for the command, or deliberately saved.

**Complete when:** Move the triad to a hole center and rotate around it. Relocating the triad alone leaves geometry unchanged; the resulting transform and preview agree and switching modes does not reset the pivot unexpectedly.

<a id="f074"></a>
### F074 — Precise placement

**Owning tasks:** 10.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U07, A04 · **First delivery:** P4 · **Likely scope:** Feature/UI

**Goal:** Expose exact coordinate meaning during movement, especially in nested assemblies.

**Workflow and behavior:** Allow global/work-part/component-local coordinates, typed offsets, snapping, and arbitrary-axis rotation. Label whether values are absolute positions or incremental transforms, show reference frames, and preserve units. Compose nested transforms through the shared occurrence service rather than treating displayed coordinates as local values.

**Complete when:** Translate a rotated nested component by a local-axis distance and then a global-axis distance. Reported coordinates and final placement agree with the chosen frames; repeated operations do not apply parent transforms twice.

<a id="f075"></a>
### F075 — Placement versus constraint

**Owning tasks:** 10.7, 12.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U07, B02 · **First delivery:** P4/P6 · **Likely scope:** UI/Feature

**Goal:** Separate positioning something once from creating a relationship that stays true after later edits.

**Workflow and behavior:** Move Here commits a placement; Maintain Relationship opens a supported mate/joint workflow with explicit references and degrees of freedom. Do not create hidden constraints from snapping alone. When a component is already constrained, explain whether movement is a solver-driven drag, an arrangement change, or blocked by existing relationships.

**Complete when:** Align two holes once, then move the supporting part: the unconstrained item stays at its placement. Repeat with a persistent relationship and it follows correctly; users can see and undo the relationship.

<a id="f076"></a>
### F076 — Contextual mates/joints

**Owning tasks:** 12.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B02 · **First delivery:** P6 · **Likely scope:** Feature

**Goal:** Suggest useful assembly relationships from selected geometry without hiding their mechanical meaning.

**Workflow and behavior:** Use selected planes, cylinders, axes, and points to offer supported planar, concentric, fixed, revolute, slider, or other available joint forms. Preview remaining freedom, alignment flip, offsets, and limits. Resolve multiple valid interpretations explicitly and use the existing assembly solver where it satisfies the contract.

**Complete when:** Select cylindrical and planar references to position a shaft, inspect the resulting motion, and adjust limits. Conflicting mates are explained and canceled without leaving an overconstrained partial assembly.

<a id="f077"></a>
### F077 — Assembly freedom display

**Owning tasks:** 12.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B02 · **First delivery:** P6 · **Likely scope:** Feature/UI

**Goal:** Show which components are grounded, movable, fully constrained, or conflicting.

**Workflow and behavior:** Provide consistent status indicators and optional movement/rotation cues from solver state. Grounding is a declared relationship rather than a color convention. Differentiate an unloaded/unresolved component from an underconstrained loaded component and provide navigation to controlling joints or conflicts.

**Complete when:** Inspect an assembly with one grounded base, one slider, one free part, and one conflict. The indicated freedoms match permitted manipulation and update after adding/removing a mate.

<a id="f078"></a>
### F078 — In-context part editing

**Owning tasks:** 12.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A04, B03 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Edit a component using its surroundings while preserving shared-definition and reference scope.

**Workflow and behavior:** Enter the intended occurrence context, visually distinguish the work part, and collect external geometry only through supported associative/snapshot policies. Store occurrence transforms and sources explicitly; warn through scope information when editing a shared definition affects other occurrences. Prevent relationships that create dependency cycles.

**Complete when:** Size a cover from neighboring geometry within a rotated subassembly. The cover edits its intended definition, contextual references transform correctly, and moving or replacing the neighbor updates or produces a repairable reference error.

<a id="f079"></a>
### F079 — Assembly-scoped cuts

**Owning tasks:** 12.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A08 · **First delivery:** P2 proof; P6 product · **Likely scope:** Core

**Goal:** Apply a manufacturing or installation modification to chosen occurrences without modifying every shared source instance.

**Workflow and behavior:** Create the operation in the assembly definition, collect affected occurrence paths and tool geometry, and show derived assembly-local results. Keep original source definitions and unselected occurrences unchanged. An explicit propagate-to-source action, if implemented, previews its broader consequences and rejects inconsistent transforms/scopes.

**Complete when:** Cut one of two occurrences of the same plate, reopen the assembly, and inspect the source part. Only the selected occurrence result is cut; BOM identity policy, drawing output, and subsequent source updates follow documented rules.

<a id="f080"></a>
### F080 — Exploded views and motion

**Owning tasks:** 12.6, 12.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B04, B05 · **First delivery:** P6 increments · **Likely scope:** Feature/Core

**Goal:** Explain assembly structure and simple mechanisms without overwriting their modeled placement.

**Workflow and behavior:** Save exploded transforms and assembly arrangements separately from source placements. Provide explode steps, spacing, trails or sequence where useful, plus bounded joint-driven motion with limits. Distinguish visual animation from dynamic/physical simulation. Drawing/BOM consumers choose the intended saved arrangement explicitly.

**Complete when:** Create an exploded view, return to assembled state, and reopen both views. Animate a supported hinged mechanism within limits; source geometry and normal assembly placement remain unchanged.

<a id="f081"></a>
### F081 — Published interfaces

**Owning tasks:** 12.5, 10.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B03, A05, A09 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Give other parts stable, intentional references instead of exposing arbitrary internal topology.

**Workflow and behavior:** Publish named datums, geometry, and parameters with identity, units/type, description, and source ownership. Consumers select those interfaces through controlled scope. Define rename, replacement, deprecation, and deletion behavior; changing internal construction should not break a maintained published interface unnecessarily.

**Complete when:** Publish mounting axes and spacing, consume them in a bracket, and replace internal source features while preserving the interfaces. Consumers update correctly; deleting an interface identifies affected downstream parts.

<a id="f082"></a>
### F082 — Associative geometry linking

**Owning tasks:** 12.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B03 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Reuse geometry between parts with visible provenance and deliberate update control.

**Workflow and behavior:** Create a link/derived feature from selected published or permitted geometry, preserve the source occurrence transform, and show live, frozen, or independent-copy status. Freezing retains provenance and a defined snapshot; breaking a link deliberately changes future update behavior. Avoid copying hidden source-document internals accidentally.

**Complete when:** Link a surface into another part, move/edit the source, then freeze and later resume updates if supported. Each state behaves as shown, cycles are rejected, and source relocation is repairable.

<a id="f083"></a>
### F083 — External-reference manager

**Owning tasks:** 12.5, 15.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B03, X02 · **First delivery:** P3/P6 · **Likely scope:** Feature/UI

**Goal:** Give users one place to understand and repair dependencies outside the current document.

**Workflow and behavior:** List source definitions/files, dependent features, resolved paths, versions/staleness, loading state, and update/freeze/break actions. Provide missing-path repair and dependency collection without changing geometry silently. Distinguish a missing file, inaccessible source, unsupported format, and intentionally unloaded object.

**Complete when:** Move a project folder, repair a missing source once, and identify all affected consumers. Updating or freezing a dependency has a previewable scope and the manager agrees with saved references.

<a id="f084"></a>
### F084 — Cycle prevention

**Owning tasks:** 7.5, 12.5, 10.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B03, A05, A09 · **First delivery:** P1/P3 · **Likely scope:** Core

**Goal:** Reject dependency relationships that cannot be evaluated deterministically.

**Workflow and behavior:** Check proposed feature inputs, external geometry links, parameter expressions, and configuration dependencies before commit. Include cross-document/occurrence context and report an understandable chain forming the cycle. Handle partially loaded graphs conservatively; do not call an unchecked graph valid.

**Complete when:** Attempt A-to-B-to-A links and an indirect expression cycle across three parts. The attempted final relationship is rejected with the dependency chain and no partially saved or partially computed link remains.

<a id="f085"></a>
### F085 — Reference repair

**Owning tasks:** 7.5, 12.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A05, B03 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Recover from changed or missing geometry without rebuilding downstream work blindly.

**Workflow and behavior:** Show the broken reference, its original role/provenance, candidate replacements, and affected consumers. Let the user replace one reference or a clearly bounded group, preview the consequences, and undo the repair. Respect expected type, ownership, orientation, units, and occurrence path; do not choose by nearest face alone.

**Complete when:** Delete a referenced face, select a valid replacement, and preview an extrusion and drawing annotation that depend on it. Commit restores the intended relationships; Cancel preserves the diagnostic state.

<a id="f086"></a>
### F086 — Stable selection intent

**Owning tasks:** 7.1.4, 7.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A05, U05 · **First delivery:** P1/P3 · **Likely scope:** Core

**Goal:** Preserve the meaning of selected geometry across supported topology changes without pretending every edit is resolvable.

**Workflow and behavior:** Combine stable feature/result provenance with explicitly stored selection rules and geometric signatures where appropriate. Define when an edge split maps to several entities, when a merged face remains equivalent, and when ambiguity requires repair. Keep explicit frozen selections distinct from associative intent rules.

**Complete when:** Change upstream topology in a controlled corpus of splits, merges, and symmetry ambiguities. Supported references resolve correctly; ambiguous cases remain unresolved rather than attaching to plausible but wrong geometry.

<a id="f087"></a>
### F087 — Useful failure reporting

**Owning tasks:** 7.5, 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A07, U11 · **First delivery:** P3/P4 · **Likely scope:** Feature/UI

**Goal:** Explain what failed, what caused it, and what the user can do next.

**Workflow and behavior:** Identify the first failing feature, invalid/missing input, and blocked dependents, with navigation/highlighting and concise corrective actions. Distinguish unsupported input, geometric failure, solver conflict, cancellation, and internal error. Preserve the last valid result only with a visible stale marker and offer optional technical diagnostics separately.

**Complete when:** Break an upstream profile and inspect a downstream cascade. The user is directed to the first cause, not dozens of equivalent errors, and export/CAM cannot quietly treat stale geometry as current.

<a id="f088"></a>
### F088 — Controlled recompute

**Owning tasks:** 7.5.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A07, X03 · **First delivery:** P3/P10 · **Likely scope:** Core/Feature

**Goal:** Let users balance responsiveness and model currency during expensive or grouped edits.

**Workflow and behavior:** Support documented automatic/manual modes, deferred updates within a transaction, and targeted recompute of the necessary dependency closure. Track dirty/stale state at relevant feature/document boundaries. Commands requiring current geometry must update or explicitly refuse/ask for the needed action; manual mode cannot imply unchanged results are current.

**Complete when:** Change several parameters with deferred updates, recompute once, and compare with automatic mode. Results agree; targeted recompute includes required dependencies and stale drawings/toolpaths remain visibly marked.

<a id="f089"></a>
### F089 — Direct STL machining

**Owning tasks:** 6, 14.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C01 · **First delivery:** P8 · **Likely scope:** Feature/Core

**Goal:** Generate supported toolpaths directly from mesh geometry without tessellation-to-B-rep conversion.

**Workflow and behavior:** Accept a mesh as the CAM model through shared units/transforms and a validated mesh-capable algorithm. Audit existing facilities before adding new algorithms. Begin with a bounded three-axis finishing workflow, documenting supported tool shapes, mesh assumptions, and tolerance. Keep roughing/rest machining as distinct required increments.

**Complete when:** Load an STL, declare its units, set placement, generate the supported finishing path, and independently compare expected tool contact within stated tolerance. No thousands-of-faces conversion is required.

<a id="f090"></a>
### F090 — Guided CAM setup

**Owning tasks:** 14.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C01, C03, U09 · **First delivery:** P8 · **Likely scope:** UI/Feature

**Goal:** Guide users from a model to a complete machining setup with visible assumptions.

**Workflow and behavior:** Collect model, units, orientation, work coordinate system/origin, stock, machine, tools, boundaries, allowances, and postprocessor in a logical sequence. Show geometry/setup previews and explain missing inputs. Templates can prefill choices but consequential values remain visible, editable, and validated against the selected strategy.

**Complete when:** Create a setup from an STL and from supported solid geometry. Reopening preserves origins, units, stock, and tools; a wrong-scale mesh is obvious before toolpath generation or postprocessing.

<a id="f091"></a>
### F091 — Mesh preparation

**Owning tasks:** 14.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C01 · **First delivery:** P8 · **Likely scope:** Feature

**Goal:** Identify mesh conditions that matter to the chosen machining algorithm and offer controlled fixes.

**Workflow and behavior:** Inspect normals/orientation, holes, nonmanifold regions, disconnected pieces, degenerate triangles, bounds, and excessive density. Distinguish a diagnostic from a required repair: some algorithms tolerate open meshes while others require a solid stock model. Preview repair/decimation effects and never smooth away intentional detail without an explicit tolerance.

**Complete when:** Use inverted, open, disconnected, and dense fixtures. Report which conditions block each supported operation, and verify approved repairs respect dimensions/tolerance while preserving the original mesh.

<a id="f092"></a>
### F092 — Roughing and finishing workflow

**Owning tasks:** 14.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C01, C02 · **First delivery:** P8 staged · **Likely scope:** Feature/Core

**Goal:** Make a useful strategy sequence understandable without implying that a finishing path removes bulk stock safely.

**Workflow and behavior:** Ship finishing first where supported, then add stock-aware roughing with stepdown/stepover, allowance, entry/exit, clearance, and strategy-specific controls. Expose strategy presets as editable values with documented applicability. Carry stock/setup identity between operations and show the resulting order and remaining material assumptions.

**Complete when:** Machine-planning fixtures show roughing leaves the intended allowance and finishing reaches supported surfaces within tolerance. A finishing-only release is labeled clearly; unsupported stock engagement or access is reported.

<a id="f093"></a>
### F093 — Boundary selection on meshes

**Owning tasks:** 14.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C01, C02 · **First delivery:** P8 · **Likely scope:** Feature

**Goal:** Control where a mesh-based strategy may cut and where it must avoid.

**Workflow and behavior:** Offer sketch-based projected containment, supported picked mesh regions, and avoid areas with visible boundary loops. Specify projection direction, open/closed-loop rules, and whether containment applies to tool center, contact point, or tool envelope. Preserve references under mesh placement/unit changes and warn when a region cannot be reidentified.

**Complete when:** Restrict machining to one pocket-like region and protect a raised area. Generated paths respect the documented cutter/boundary rule and a moved mesh cannot leave boundaries silently in the wrong frame.

<a id="f094"></a>
### F094 — Rest machining

**Owning tasks:** 14.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C02 · **First delivery:** P8 after roughing · **Likely scope:** Core

**Goal:** Remove material left by earlier operations using their actual stock assumptions.

**Workflow and behavior:** Reference a preceding stock state or supported remaining-material representation, tool geometry, operation order, and tolerance. Recalculate when any upstream stock/toolpath changes. Distinguish true remaining-stock computation from merely rerunning finishing with a smaller tool; show approximation limits.

**Complete when:** Rough a fixture with a large tool, compute remaining stock, and plan a smaller-tool rest operation. It targets the expected remaining areas and is invalidated when the prior tool or stock changes.

<a id="f095"></a>
### F095 — Stock and collision simulation

**Owning tasks:** 14.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C03 · **First delivery:** P8 increments · **Likely scope:** Feature/Core

**Goal:** Show what a supported toolpath removes and identify the checks actually performed.

**Workflow and behavior:** Visualize remaining stock, gouges, tool/holder clearance, and fixture interactions to the implemented fidelity. State whether checks use toolpaths, postprocessed motion, or a machine model; list missing coverage instead of implying complete collision safety. Keep tools, holders, fixtures, stock, and machine envelopes separately defined.

**Complete when:** Run known-clear and deliberately colliding fixtures, compare material removal with an independent reference where available, and verify units/transforms. Simulation results disclose their scope and cannot be presented as proof that real machine motion is safe.

<a id="f096"></a>
### F096 — Setup reuse

**Owning tasks:** 14.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C03 · **First delivery:** P8 · **Likely scope:** UI/Feature

**Goal:** Reuse trustworthy machine/tool/setup choices without inheriting stale model references.

**Workflow and behavior:** Provide templates for machines, tools, stock rules, posts, and recurring operation sequences with names, versions, units, and compatibility metadata. Instantiate templates into an editable job, remap geometry collectors, and show unresolved inputs. Keep template changes distinct from modifying existing jobs unless explicitly applied.

**Complete when:** Apply a template to a new model of different size, resolve collectors, and inspect all consequential values. Updating the template does not silently alter previously approved jobs or toolpaths.

<a id="f097"></a>
### F097 — Change tracking

**Owning tasks:** 14.4, 16.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C03, X05 · **First delivery:** P3/P8 · **Likely scope:** Core/Feature

**Goal:** Prevent outdated machining results from appearing current after their inputs change.

**Workflow and behavior:** Track dependencies on model geometry/placement, stock, tools/holders, fixtures, operation parameters, units, and relevant post settings. Mark affected stages stale and distinguish toolpath regeneration from reposting. If output is exported despite a permitted warning workflow, identify its source revision/state explicitly rather than silently using stale data.

**Complete when:** Change a cutter diameter, stock offset, and model placement separately. Exactly the affected paths/simulations/output states invalidate, and regeneration restores a traceable current state.

<a id="f098"></a>
### F098 — Unified measurement

**Owning tasks:** 15.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** I01 · **First delivery:** P9; isolated tools earlier · **Likely scope:** UI/Feature

**Goal:** Inspect common geometric quantities through one tool with explicit meaning and units.

**Workflow and behavior:** Infer and allow choosing distance, angle, radius, thickness, minimum separation, area, volume, center of mass, and mass where supported. Show which entities and frames define a result, whether a value is minimum/projected/local, and what material/density is assumed. Label mesh/approximate measurements and unsupported shell mass cases.

**Complete when:** Measure known analytic fixtures and repeated assembly instances. Values and units are correct; missing density or ambiguous thickness is explained instead of replaced with a misleading default result.

<a id="f099"></a>
### F099 — Persistent measurements

**Owning tasks:** 15.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** I01, A05 · **First delivery:** P9 · **Likely scope:** Feature

**Goal:** Save useful engineering checks so they can be revisited after edits.

**Workflow and behavior:** Store references, measurement type, units, and either associative update behavior or an explicitly dated snapshot. Display valid, stale, and unresolved states; allow names, notes, and navigation to operands. Persisting a measurement does not automatically create a driving constraint or a dependency cycle.

**Complete when:** Save a clearance measurement, move a component, and reopen the document. An associative measurement updates or flags repair, while a snapshot remains labeled with its original state and does not imply current clearance.

<a id="f100"></a>
### F100 — Interactive sections

**Owning tasks:** 15.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** I01 · **First delivery:** P9 · **Likely scope:** UI/Feature

**Goal:** Inspect interiors and communicate selected cut views without changing modeled geometry.

**Workflow and behavior:** Provide one or more movable section planes with exact offsets/orientations, caps where supported, and saved view definitions. Let users inspect section curves and supported dimensions while distinguishing visual clipping from extracted/intersected geometry. Preserve source occurrence context and keep exports explicit about whether they use the clipped view or full model.

**Complete when:** Create two section planes through a nested assembly, save the view, and move a plane numerically. Reopening reproduces it; model geometry remains intact and section measurements describe the actual selected plane.

<a id="f101"></a>
### F101 — Interference/clearance checks

**Owning tasks:** 15.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** I01, B06 · **First delivery:** P9 · **Likely scope:** Feature

**Goal:** Find and navigate assembly conflicts rather than requiring visual inspection of every pair.

**Workflow and behavior:** Choose component sets, exclude intended cases explicitly, and compute interference or minimum clearance with documented tolerance and touching-contact policy. Return pair lists, highlights, magnitudes where meaningful, and unresolved/unloaded participants. Use broad-phase acceleration without skipping required exact checks unnoticed.

**Complete when:** Check an assembly containing an overlap, a touch, a small clearance, and an unloaded component. Results classify each correctly, navigate to the relevant pair, and never label an incomplete check as fully clear.

<a id="f102"></a>
### F102 — Drawing creation wizard

**Owning tasks:** 15.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** D01, X05 · **First delivery:** P9; compatibility P2/P3 · **Likely scope:** UI/Feature

**Goal:** Create common drawings through a guided view/template setup that remains associative.

**Workflow and behavior:** Select source definition/occurrence or arrangement, sheet template, units, scale, projection convention, and base orientation. Add projected, section, and detail views with preview and consistent placement. Keep drawing-only data within the engineering-document contract and preserve explicit external links if stored separately.

**Complete when:** Create a drawing with base/projected/section/detail views, edit the source, and reopen. Supported views update correctly; chosen scale, projection convention, and source arrangement remain explicit and broken references are surfaced.

<a id="f103"></a>
### F103 — Associative annotation

**Owning tasks:** 15.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** D01, A05 · **First delivery:** P9 · **Likely scope:** Feature/Core

**Goal:** Keep dimensions and manufacturing notes attached to the intended geometry through supported edits.

**Workflow and behavior:** Support associative dimensions, center marks/lines, hole callouts, and relevant annotations with clear reference versus driving semantics. Reuse source hole/thread metadata where present; expose tolerances and formatting without duplicating model parameters. Detect lost or ambiguous topology and provide repair with a preview.

**Complete when:** Change a hole size and location, then split an annotated edge. Valid callouts update from source metadata, ambiguous annotations are marked for repair, and the drawing never silently displays a plausible dimension attached to the wrong edge.

<a id="f104"></a>
### F104 — Assembly documentation

**Owning tasks:** 15.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** D02, B01, B04 · **First delivery:** P9 · **Likely scope:** Feature

**Goal:** Produce BOMs, balloons, and exploded documentation from defined product-structure rules.

**Workflow and behavior:** Define quantities for repeated occurrences, unique parts, configurations, subassemblies, and reference-only/suppressed items. Keep reference-set visibility independent of BOM inclusion. Associate balloons with stable item identities, allow explicit item numbering policies, and use selected exploded arrangements for views.

**Complete when:** Document an assembly containing repeats, a unique copy, an empty reference set, and reference-only hardware. Quantities and balloons match the stated rules and remain stable or explicitly renumbered after supported edits.

<a id="f105"></a>
### F105 — Additional modeling modules

**Owning tasks:** 15.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X01 · **First delivery:** P9 by module · **Likely scope:** Feature/Core

**Goal:** Integrate useful sheet-metal, frame/weldment, and standard-hardware workflows without making them prerequisites for core modeling.

**Workflow and behavior:** Audit compatible modules first. Sheet metal should track thickness, bend rules, reliefs, and unfold/refold intent; frames should place profiles along paths and expose trim/joint/cut-list behavior; hardware should insert reusable parameterized definitions with source/standard metadata. Each is a separately scoped module using shared identity, units, references, and UI contracts.

**Complete when:** A bounded sheet-metal part unfolds/refolds as documented, a frame produces a consistent cut list, and repeated hardware preserves instance/BOM semantics. These are separate deliverables; passing one does not mark the whole package complete.

<a id="f106"></a>
### F106 — Responsive previews

**Owning tasks:** 8.1.6, 16.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X03, A07 · **First delivery:** P3/P10 · **Likely scope:** Feature/Core

**Goal:** Keep expensive commands responsive and make the difference between preview and final geometry clear.

**Workflow and behavior:** Use cancellable computation, progress feedback, and reduced-cost previews where useful. Give each request an input revision/token; discard late results after parameter changes, cancellation, or document closure. Use safe worker boundaries and commit geometry only on the appropriate thread/transaction path. Clearly indicate approximation and revalidate the final result.

**Complete when:** Rapidly change a complex feature, cancel, and close the document during a preview. No stale result commits, the UI remains recoverable, and final geometry meets the full tolerance contract rather than the preview approximation.

<a id="f107"></a>
### F107 — Large-assembly handling

**Owning tasks:** 12.8, 16.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B06, X03 · **First delivery:** P6/P10 after measurement · **Likely scope:** Core

**Goal:** Scale shared-instance assemblies while preserving correctness and complete model state.

**Workflow and behavior:** Reuse geometry/tessellation across instances where supported, use selective loading and simplified representations, and profile culling/rendering separately from recompute. Visibility-based display optimizations must not suppress required dependency evaluation or omit hidden parts from engineering checks. Record cache keys by source/configuration/revision.

**Complete when:** Measure fixed assemblies at increasing instance counts on named hardware. Improvements are attributable to recorded bottlenecks; repeated geometry renders in correct transforms, and full-resolution checks still include required hidden/unloaded participants.

<a id="f108"></a>
### F108 — Project packaging

**Owning tasks:** 15.6, 16.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X02, X04 · **First delivery:** P3/P9 · **Likely scope:** Feature/Core

**Goal:** Move or share a project with its dependencies while preserving intentional identity relationships.

**Workflow and behavior:** Collect required files and supported embedded assets, preview missing/external references, and create a package manifest with portable paths. Specify Save Copy as a file/package operation versus Make Unique as new definition identity; document whether a copied project remains linked to external originals. Offer deliberate relinking and independent duplication.

**Complete when:** Package a nested assembly, move it to a different directory, and open it without the original path. Supported references resolve, omitted sources are listed, and a copy cannot accidentally overwrite or redirect the original project.

<a id="f109"></a>
### F109 — Compatibility strategy

**Owning tasks:** 7.6, 16.1, 16.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A06, X04, X09 · **First delivery:** P1/P3/P10 · **Likely scope:** Core

**Goal:** Make native, legacy, and exchange behavior predictable as the fork diverges.

**Workflow and behavior:** Maintain a tested matrix for opening, displaying, editing, converting, and exporting representative FreeCAD/fork objects. Use `.cadprt` for new native documents and preserve original `.FCStd` files during conversion. Detect required capabilities from content, report losses, and refuse unsafe saves; an extension alone is not a compatibility check.

**Complete when:** Import supported legacy fixtures, convert a copy, and reopen with full editability for supported features. Unsupported objects/add-ons are named explicitly; native data is never silently dropped to produce an apparently successful legacy export.

<a id="f110"></a>
### F110 — Consistent automation

**Owning tasks:** 16.5, 16.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X03, A07 · **First delivery:** P3/P10 · **Likely scope:** Feature

**Goal:** Expose the same modeling behavior through scripts and reproducible operation recording.

**Workflow and behavior:** Provide stable command/model APIs with explicit inputs, operation/target identities, units, context, and transaction behavior. Record committed semantic actions rather than raw mouse coordinates; include deterministic replay fixtures and meaningful errors. Preview-only state and private filesystem/account data should not enter a shareable recording by accident.

**Complete when:** Record or script a bracket workflow, replay it headlessly where supported, and compare parameter relationships/results. UI and automation reject the same invalid targets and do not depend on whichever document or body happened to be active.

<a id="f111"></a>
### F111 — Upstream-friendly implementation

**Owning tasks:** 16.3, 16.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X03 · **First delivery:** P0/P10 · **Likely scope:** Feature/Core

**Goal:** Keep long-term maintenance feasible while preserving deliberate product differences.

**Workflow and behavior:** Record upstream base and fork-specific decisions; separate UI adapters, feature additions, and model/persistence changes into reviewable patches where practical. Reuse supported extension points, upstream useful general fixes, and retire adapters when shared contracts replace them. Do not preserve an incompatible architecture merely to minimize a diff.

**Complete when:** Integrate a representative upstream update using documented build/tests and the divergence map. Conflicts have identifiable owners/reasons, and supported legacy/new workflows still pass their release gates.

<a id="f112"></a>
### F112 — Guided workflows and progressive disclosure

**Owning tasks:** 10.2, 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U09, U11 · **First delivery:** P3/P4 · **Likely scope:** UI/Feature

**Goal:** Make common commands teach their own sequence while giving experienced users a direct, efficient route.

**Workflow and behavior:** Use one command state model for guided prompts, preselection, direct field editing, preview, and commit. Show the next unresolved input; keep consequential operation/target choices visible and reveal advanced options on demand. Help is specific to the active step and explains valid selections, not a mandatory tour. Preserve already valid choices when moving back.

**Complete when:** A first-time user completes Extrude from prompts; an experienced user performs the same operation through preselection and typed values. Both create equivalent editable features and can correct an earlier input without restarting.

<a id="f113"></a>
### F113 — Intelligent initial operation suggestions

**Owning tasks:** 10.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U10, A02 · **First delivery:** P1/P4 · **Likely scope:** Feature/Core

**Goal:** Reduce routine Boolean decisions without taking control away from the user or changing saved intent.

**Workflow and behavior:** Within the editable work part, suggest New Body for no eligible intersection and Unite for exactly one valid eligible target. Require explicit resolution for multiple candidates; explain invalid contact and exclude unrelated component geometry from automatic mutation. Pocket/Groove start in Subtract. Manual choice takes precedence, and accepted mode/targets become stored feature parameters.

**Complete when:** Test zero, one, multiple, tangent-invalid, and cross-component candidates. Editing a committed Unite until it no longer intersects produces defined failure/repair behavior, not a silent conversion into New Body.

<a id="f114"></a>
### F114 — Selection-aware constraint eligibility

**Owning tasks:** 11.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S07, S02, S04 · **First delivery:** P1 audit; P5 · **Likely scope:** Feature/Core

**Goal:** Show only relevant sketch actions and clearly distinguish a mathematical conflict from the wrong selection shape.

**Workflow and behavior:** Use selection type/count/roles for fast applicability: one line exposes supported single-line relations and construction/reference actions; two suitable lines add Parallel/Perpendicular. For applicable actions, use solver evidence to mark Valid, Already Applied, Redundant, Conflicting, Unsupported, or Unverified. Proven conflicts are disabled with reasons. Reuse this service in palettes, menus, toolbars, shortcuts, and commit validation.

**Complete when:** Selecting one line never suggests a two-line relation as immediately executable. A constrained horizontal line's Vertical candidate is evaluated correctly for its actual sketch state; stale checks cannot mutate the sketch or disable valid actions based on guessed conflicts.

<a id="f115"></a>
### F115 — Native .cadprt engineering documents

**Owning tasks:** 7.6, 16.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X04, A06 · **First delivery:** P1/P3/P10 · **Likely scope:** Core

**Goal:** Provide a recognizable native format for the entire application and reliable behavior as schemas evolve.

**Workflow and behavior:** Use a stable internal format identity, schema/capability declarations, producer metadata, and explicit part/document relationships. Preserve supported CAD, assembly, drawing, CAM, FEM, and Draft data; reject or safely retain unsupported required content. Reuse suitable existing container infrastructure rather than inventing a new binary format unnecessarily. Legacy conversion is explicit and preserves originals.

**Complete when:** Round-trip a mixed engineering document and an externally linked assembly. Required unknown capabilities, corrupt content, and legacy-only objects produce clear controlled outcomes; native files are not accepted or overwritten solely because their filename has the expected suffix.

<a id="f116"></a>
### F116 — Early cross-workbench compatibility

**Owning tasks:** 16.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X05 · **First delivery:** P2/P3 then each core change · **Likely scope:** Core/Feature

**Goal:** Discover downstream consequences of ownership changes before many commands depend on the new model.

**Workflow and behavior:** Include small existing drawing, CAM, FEM, and Draft consumers in the architecture proof. Verify references, transforms, units, materials/supports/loads, invalidation, and save/reopen through shared adapters. Distinguish geometry compatibility from a complete redesigned downstream UI; broaden each module only after this foundation works.

**Complete when:** Changing a shared definition and making an assembly-local cut affect the correct drawing views, CAM model, FEM assignments, and Draft references. Unsupported paths are explicit and stale meshes/toolpaths/results cannot appear current.

<a id="f117"></a>
### F117 — Task benchmarks and release evidence

**Owning tasks:** 16.4, 16.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** Q01 · **First delivery:** P0 onward · **Likely scope:** Process/Validation

**Goal:** Judge progress by usable engineering outcomes and reliable edits rather than command counts.

**Workflow and behavior:** Maintain task 16.4's fixed benchmark tasks, recorded builds/hardware, learning-versus-practiced comparisons, completion/error/recovery measurements, and relevant geometry/persistence checks. Measure new workflow benefits against stock FreeCAD and selected available comparators. Establish acceptance thresholds before evaluating a release and revise engineering estimates using actual work.

**Complete when:** A release report links each advertised workflow to completed task evidence and states unverified cases. Performance, click-count, time-saving, and adoption claims are not fabricated from demonstrations or code generation.

<a id="f118"></a>
### F118 — Model-led onboarding and outreach

**Owning tasks:** 17.2, 17.3, 17.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X07, M02 · **First delivery:** P4/P11 · **Likely scope:** Product/Documentation

**Goal:** Give people a concrete useful result that makes trying FC Plus worthwhile.

**Workflow and behavior:** Publish-ready examples include named parameters, units/descriptions, editable native sources, suitable fabrication exports, version information, and a short path to changing two dimensions. Prepare concise videos plus complete tutorials and channel-specific materials for Thingiverse/Printables, relevant Facebook groups, creators, forums, makerspaces, and search. Posting still follows actual authorization.

**Complete when:** A representative user can install/open the supported build, customize the sample, save, and export without a general CAD course. Track this success and subsequent independent use separately from model downloads or social impressions.

<a id="f119"></a>
### F119 — Independent branding and format discoverability

**Owning tasks:** 17.6, 17.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** M03, X04 · **First delivery:** Identity early; P10/P11 · **Likely scope:** Product/Documentation

**Goal:** Make the relationship to FreeCAD and the meaning of .cadprt clear without implying endorsement or exclusivity.

**Workflow and behavior:** Retain FreeCAD-Plus as the working name until a rename is chosen. Publish differences, compatibility, support destination, upstream credits, and stable format documentation. Evaluate a distinct public brand before major incompatible distribution. Optional FileInfo listing, IANA media-type registration, and installer association follow the process and limitations in tasks 17.6-17.7; they are not exclusive ownership claims.

**Complete when:** Release copy accurately describes the independent fork and supported imports/exports. Installers and sample files identify the format consistently, and any proposed registration identifier is not presented as assigned before it actually is.

<a id="f120"></a>
### F120 — Free releases, licensing, and maintenance sustainability

**Owning tasks:** 16.7, 17.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X06, X03 · **First delivery:** P0/P10 · **Likely scope:** Release/Process

**Goal:** Keep the application free for the foreseeable future and make each distributed build maintainable and properly accompanied.

**Workflow and behavior:** Preserve the free local-core commitment, audit actual code/dependency/asset terms, and prepare matching source/build materials and required notices as described in tasks 16.7 and 17.8. Record supported platforms and capability limits. Treat support, donations/sponsorship, hosted services, or paid distribution as optional later business decisions rather than reasons to build billing now.

**Complete when:** Each released binary has traceable source/build/license materials and a documented maintenance/support route. A future revenue discussion cannot silently introduce paywalls, unsupported proprietary claims, or mandatory cloud dependencies.

<a id="f121"></a>
### F121 — Audience and adoption research

**Owning tasks:** 17.1, 17.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** M01, M02 · **First delivery:** P0/P11 · **Likely scope:** Research/Product

**Goal:** Use real tasks and repeated use to refine which users the fork serves first.

**Workflow and behavior:** Keep hobbyist, professional, small-team, and small-company populations distinct. Use task 17.1's dated, verified competitor evidence to choose comparisons, then learn from frustrated/lapsed FreeCAD users, experienced CAD users, and small teams separately. Track migration barriers, compatibility needs, support load, first success, and a second real project.

**Complete when:** Product and release choices can point to observations or clearly labeled hypotheses. No probability of adoption or market-share claim is inferred merely from an enthusiastic model audience, a recognizable extension, or the owner's workflow expertise.

<a id="f122"></a>
### F122 — Named parameters, expressions, and units

**Owning tasks:** 10.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A09 · **First delivery:** P1/P3; editor P4/P5 · **Likely scope:** Core/Feature

**Goal:** Make design intent visible and reusable so people can customize a model without hunting through its entire feature history.

**Workflow and behavior:** Provide a part-level parameter editor with names, descriptions, types/units, values/expressions, and where-used links. Reuse existing expression facilities where adequate; define document/part/configuration scope, dimensional checking, cycles, renaming, and controlled publication to other parts. Common feature fields accept compatible expressions. Separate UI display units from stored physical meaning.

**Complete when:** Drive enclosure width, lid clearance, and hole spacing from named values, rename a parameter, and change display units. All intended consumers update; incompatible units and cycles are rejected; a shared definition does not accidentally acquire occurrence-local geometry parameters.

<a id="f123"></a>
### F123 — Contextual workspace, help, and accessibility

**Owning tasks:** 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U11 · **First delivery:** P3/P4 · **Likely scope:** UI/Feature

**Goal:** Keep navigation, command availability, help, and accessibility coherent across modeling and supported engineering tasks.

**Workflow and behavior:** Use shared context/selection services for command availability and explain disabled operations. Offer local contextual help, searchable terminology, keyboard focus/order, configurable shortcuts, high-DPI sizing, text alternatives to color, and preference reset. Keep separate UI preferences from document semantics. Transition to drawing/CAM/FEM tasks without losing the identity of the active engineering document.

**Complete when:** Complete representative modeling and downstream setup tasks with keyboard navigation and enlarged display settings. Missing selections and wrong work context are recoverable from the interface; changing a preference does not change saved geometry.

<a id="f124"></a>
### F124 — Sketch placement and support management

**Owning tasks:** 11.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S08, A05 · **First delivery:** P1/P3 contracts; P5 · **Likely scope:** Feature/Core

**Goal:** Make where a sketch lives, how it is oriented, and how it follows its support understandable and repairable.

**Workflow and behavior:** Create a sketch on principal/datum planes or supported planar faces with explicit origin, axes, offsets, and attachment mode. Prefer stable datums where the workflow calls for them without banning face attachment. Provide support inspection and reattachment with a preview; distinguish preserving local coordinates from preserving world-space placement and warn about changed downstream geometry.

**Complete when:** Create an offset sketch on a rotated component, change its support, and repair a lost face reference. Orientation, external projections, dimensions, and occurrence transforms follow the selected policy; reattachment is undoable.

<a id="f125"></a>
### F125 — Recovery and document lifecycle

**Owning tasks:** 16.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X08, X04 · **First delivery:** P1/P3/P10 · **Likely scope:** Core/Feature

**Goal:** Protect editing work and make file identity, saving, and recovery predictable as documents become more complex.

**Workflow and behavior:** Provide dirty/read-only indicators, recent files with missing-path repair, intentional document templates, atomic save where supported, rotating recovery snapshots, and a recover-as-copy workflow. Define treatment of external dependencies and interrupted multi-file saves; do not claim cross-file atomicity unless implemented. Keep normal save, backup/recovery, Save Copy, and Make Unique distinct.

**Complete when:** Interrupt a controlled save/recovery fixture and recover a clearly labeled editable copy without overwriting a good original. Missing external sources remain explicit, and restoring a snapshot does not silently change definition identity or relink unrelated projects.

<a id="f126"></a>
### F126 — Add-on, macro, and API compatibility

**Owning tasks:** 16.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X09, X03 · **First delivery:** P0 audit; P3/P10 · **Likely scope:** Feature/Core

**Goal:** Keep useful extensions usable where feasible and make incompatibility visible as the fork changes.

**Workflow and behavior:** Inventory important workbenches/macros/APIs, publish supported versions/capabilities, and test representative integrations against the changed ownership and document model. Prefer adapters and staged deprecation where practical. Detect unavailable required add-ons in files and preserve/refuse their data safely. Do not promise all upstream extensions work or silently run an incompatible migration.

**Complete when:** Open fixtures requiring a supported and an unavailable extension, replay a representative macro, and review migration diagnostics. Supported integrations work through stable contracts; unsupported ones identify a concrete dependency without corrupting the model.

<a id="f127"></a>
### F127 — Manufacturing export and reusable output presets

**Owning tasks:** 15.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X10, X02 · **First delivery:** P3 contracts; P4/P9 UI · **Likely scope:** Feature

**Goal:** Make reliable handoff to printing, machining, and other tools part of the everyday workflow.

**Workflow and behavior:** Provide explicit geometry/occurrence/configuration selection, units, placement/orientation, quality/tessellation, and output paths for supported STEP, STL, 3MF, DXF, and other audited formats. Offer reusable presets with visible consequential values. Validate watertightness or supported output properties where relevant and report lost history/metadata; never label a geometry export a parametric native file.

**Complete when:** Export a dimensioned part and selected assembly occurrences using supported formats, reopen/check dimensions and transforms, and compare coarse/fine mesh settings. Stale geometry and unsupported entities are disclosed and presets cannot silently export the wrong configuration.
