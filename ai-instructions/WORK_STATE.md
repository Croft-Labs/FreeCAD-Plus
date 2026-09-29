# FreeCAD Plus: Build validation handoff

Stopped at the user's shutdown request on 2026-09-29. No new feature implementation
is in progress. Resume the manual acceptance work; do not rebuild or repeat completed
automated tests unless source/runtime changes or a newly found defect justify it.

## Completed

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

## Build and evidence

External root: `D:\Temp\Office-PC\freecad-plus-validation-20260928`.
Launch: `build\bin\FreeCAD.exe` beneath that root. It reports FreeCAD 26.3.0dev,
revision 49009 and source hash `8abce719de`. This is the focused development build;
disabled unrelated workbenches, installer packaging and upstream compatibility
testing are not included. Ignore the separately installed FreeCAD.

Evidence: `closeout-build-resume-results.json`, `closeout-build-manifest.json`,
`closeout-regressions/results.json`, `closeout-highdpi/results.json`, and their logs.
The two latter folders have isolated settings and successful process reports.

## Next action

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
