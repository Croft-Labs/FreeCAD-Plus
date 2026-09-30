# FreeCAD Plus: Build validation handoff

Latest roadmap batch: 16.2l/m/n complete. Empty Lead-in/Lead-out and Boundary inputs
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
