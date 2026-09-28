# FreeCAD Plus: Development Roadmap

## Current focus

- Active milestone: 2.2, compiled validation of the Pad task workflow.
- Target outcome: [REQ-001 through REQ-007](PRODUCT_SPEC.md#capabilities-and-requirements).
- Source implementation exists; build and GUI acceptance are still pending.
  This roadmap records status; it does not authorize new phases or external publication.

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

- [   ] 2.2.1 Configure a compatible FreeCAD LibPack and build outside Google Drive.
  Status: blocked at configuration on 2026-09-28: MSVC 19.44 was detected, but
  `FREECAD_LIBPACK_DIR` had no usable LibPack. Follow [setup](DEVELOPMENT_GUIDE.md#prerequisites-and-setup).
- [   ] 2.2.2 Correct and run the focused GUI regressions against the built fork.
  Source-review finding during documentation adoption: the selector for
  `buttonStartReference` in `TestPadTaskPanel.py` asks for `QToolButton`, while
  `TaskPadPocketParameters.ui` defines `QPushButton`. Correct that test before execution.
  GUI tests have not run; this documentation task does not change test code.
- [   ] 2.2.3 Verify viewport picking, rotated profiles, both directions, keyboard input,
  visibility restoration, Cancel, and Undo/Redo; check Pocket for shared-base regressions.
  Acceptance: [UI-001](UI_UX_SPEC.md#ui-001-pad-task-pane) and [test procedure](../tests/PadTaskPanel.md).

## [   ] Phase 3: Further Part Design operations

Outcome: extend the complete task-pane workflow after Pad is validated and scope is authorized.
Depends on: milestone 2.2.

### [   ] 3.1 Define the next operation

Complete when: an operation and its create/edit acceptance criteria are approved.

- [   ] 3.1.1 Choose the next operation, such as revolve or a pattern, and define its input workflow.
  Status: future scope; no implementation authorized by this roadmap alone.
