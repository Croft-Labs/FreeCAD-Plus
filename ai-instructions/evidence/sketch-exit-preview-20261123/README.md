# Sketch Exit and Cancel controls preview — November 23, 2026

Status: owner approved implementation on November 23, 2026. This directory retains
the original prototype evidence; see the subsequent
[implementation and installed checks](../selection-sketch-controls-20261123/README.md).

Owner requests that sketch editing rename Close to **Exit Sketch** and add a
**Cancel** button beside it while a geometry, constraint or similar action is active.
Cancel follows one native Escape action while staying in sketch edit. Exit Sketch
retains the current Close behavior. The shared sketch edit panel uses this behavior
in both task UI modes; no special Classic exception was requested.

## Direct previews

- [Current drawing task](before.png)
- [Idle: Exit Sketch only](idle.png), [button row](idle-buttons.png)
- [Drawing action: Cancel and Exit Sketch](drawing.png), [button row](drawing-buttons.png)
- [Constraint action: Cancel and Exit Sketch](constraint.png)

The buttons use the existing native style and Qt ordering: Cancel immediately left
of Exit Sketch. Cancel is absent while idle. No solver/tool/constraint/element
sections, geometry visuals, numeric fields, icons or keyboard preferences change.
Completed geometry and constraints remain intact; only the current action receives
Escape. For tools where Escape resets an intermediate step but leaves the handler
active, Cancel must remain available, matching the keyboard semantics exactly.

These are actual native sketch-task widgets with an isolated Python button-row
prototype. The fixture drives the active flag; automatic handler lifecycle detection
is not implemented. Cancel sends Escape to the native viewport. `candidate.json`
records idle/drawing/constraint states, continued sketch edit after Cancel, unchanged
completed geometry/constraint counts and successful Exit Sketch. The fixture uses
rectangle and horizontal-constraint tools, and no owner document/profile.

## Provenance and implementation scope

Product baseline `adc3cf24e3b1e3019cb907f97f517b6eed3d14ef`.
Clean prototype seed `370239f692e0580614920c6287ba59e5656deef6`, workspace
`sketch-exit-preview/review-source`. Companion session `ffd9bec27c7c`; exact allowlist
`sketch_buttons.py`; fingerprint
`f9348b1d29d76b3ae1f096711093b24fe4cc250fd251544912d4b5e182057369`.
Inspection: fresh, no violations, not approved. No approval state was changed.
The runner, scene and candidate are archived here; untracked
`project.previewfirst.json` remains untouched.

After approval, implement the button row through native `TaskDlgEditSketch`
(`modifyStandardButtons`), using a non-reject Cancel action so it cannot trigger
TaskView's sketch-closing rejection. Reuse `ViewProviderSketch::keyPressed` Escape
handling instead of unconditional handler purging. Track real handler state,
including constraint tools with no ToolSettings widget or a `DSH_None` tool name.
The current tool-change notification fires before teardown completes, so account
for that lifecycle and protect queued updates against task destruction.

Validate idle, geometry creation (initial and partial/continuous stages), constraint
tools, action switching, keyboard Escape, completed-geometry preservation, clicking
Exit Sketch during an action, focus in numeric fields, both task modes and both
LeaveSketchWithEscape settings. Hide Cancel when no handler remains. Preserve
existing History-tab restoration, sketch exit fitting and coordinate visibility.
Build/install with rollback, verify native installed controls and shortcut using
isolated settings, then commit/push/remote-verify after approval.
