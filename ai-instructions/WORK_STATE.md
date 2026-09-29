# FreeCAD Plus: Build validation handoff

Issue-validation continuation (2026-09-29): five real startup recovery fixtures,
four quantity-event tests, all 19 Extrude task tests and one tree-selection test
pass against the existing fork. No application code change or native rebuild was
needed for those inherited fixes. See U.5/U.9 in the roadmap and
[repeatable procedures](../tests/UpstreamIssues.md). Mirror remains unbuilt and
#29376 still needs a reproducible affected session/GPU trace. No process is running.

Latest issue work (2026-09-29): the ten-entry watchlist is prioritized and checked
against inherited fixes and our changed UI. Part Mirror #32706 reproduces; a
source correction and three regressions are prepared. **The existing application
does not contain this C++ fix.** Native build and post-fix validation await the
next batch under the user's build policy. See [issue work](DEVELOPMENT_ROADMAP.md#upstream-issue-work)
for the 49-test baseline (47 pass, two expected new Mirror failures) and exact
evidence directory. No build/test process is running. Preserve this pending fix
when planning the next consolidated build; do not close it from old binary tests.
Source/triage milestone `85fd6ebc77a5a180d61ad116cf6507fb274e93d4` is committed
and pushed to `origin/main`; remote hash verified. Syntax/whitespace checks pass.

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
