# Move Components proposal — November 25, 2026

Status: **UI workflow awaiting owner approval. No production movement implementation.**

## Current-command audit

Production baseline: `22bb9eb20549e2048f7fad2e32abbb38505d72fe`.
`src/Mod/FreeCADPlus/freecad_plus/movement.py` implements Translate and Rotate;
Point to Point, Align Axes, Align Coordinate Systems and Interactive are listed
but rejected as unfinished. Current selection resolution assumes file-root
occurrence paths. `panel.py` offers Move Components on some Assembly instance
context menus but excludes anchored rows. No dedicated Plus Assembly move button
was found. The current active-assembly tree needs routing repairs as part of
implementation, not merely additional fields.

## Historical review

Read `archive/freecad-plus-2026-10-10`, checkpoint
`29496214b34a53fa1d479f35ab5669b41ed4fb18`, especially `src/Gui/MoveComponents.py`,
`MoveComponentsTask.py`, `MoveComponentsManipulator.py`, and
`tests/MoveComponents.md`. All six historical methods and interactive pivot/snap
controls informed the independently written proposal. Archive source was read,
not executed. See [archive findings](../../ARCHIVE_REFERENCE.md#move-components-review--november-25-2026).

## Direct native screenshots

- [Existing Translate task](baseline-translate.png)
- [Move: distance and direction](distance-vector.png)
- [Move: entered direction vector](vector-input.png)
- [Move: point to point](point-to-point.png)
- [Rotate: axis and angle](rotate.png)
- [Dynamic drag controls](dynamic.png)
- [Align axes](align-axes.png)
- [Align coordinate systems](align-frames.png)
- [Blocked by a constraint](constraint-blocked.png)

These are static screenshots of real native FreeCAD task widgets loaded from an
isolated candidate into the existing owner payload. Fixture labels and references
are mocked; selection acquisition, geometric previews, dragging, Apply and the
solver are not implemented by this UI proposal. The full-window OpenGL grab had
capture artifacts and is deliberately not offered as viewport acceptance evidence.
The task screenshots themselves were inspected for readable fields and labels.

## Verification and provenance

Companion review `f6ed77034205`; allowlist `movement.py`, `panel.py` only.
Final fingerprint:
`90eb5dc2609275f05befc4cc66b2c250cbc2c5b74758ea1863a75f5fcef92656`.
Final inspection: preview valid, no file-scope violations, **not approved**.
No approval state was set on the owner's behalf.

The separate native process used isolated user/system profiles and disposable
Machine > Drive unit > Motor/Coupling fixtures. Baseline and candidate both
completed successfully. [Candidate result](result.json) and
[baseline result](baseline-result.json) confirm object identities, links,
placements and Undo count were unchanged by task exercises. These checks establish
UI-only isolation, not correctness of future movement mathematics or constraints.

The candidate source is preserved in [ui-only-proposal.py](ui-only-proposal.py);
[prepare.py](prepare.py), [scene.FCMacro](scene.FCMacro) and [render.py](render.py)
record the original local harness and paths. They are provenance artifacts, not
production modules or portable test runners. Do not install the UI-only task.
The live review worktree is retained for approval. Task-generated validation
profiles/logs were removed after these durable captures were copied.

The confirmed fixed-active-assembly requirement and pending Type/Method proposal
are recorded separately in COMPONENT_PANEL and TASK_PANEL. Earlier pending
file-format workflow approval is unaffected by this review.
