# Prominent inline task errors — November 23, 2026

Status: historical native UI preview, subsequently approved by the owner with
"approved" and [implemented/installed](../task-errors-20261123/README.md).

Owner request: the sketch attachment error is insufficiently prominent; highlight
it like the Extrude target field, and use that treatment for future implemented errors.

## Direct screenshots

- [Current Sketch error](before.png)
- [Proposed Sketch error](sketch-error.png)
- [Proposed Plane error](plane-error.png)
- [Proposed Extrude error](extrude-error.png)
- [Proposed Revolve error](revolve-error.png)

The proposed shared label uses the existing target-field colors: 2px amber #bd780b
border, pale #fff3d6 background, dark #875300 text, 8px padding, semibold text and
wrapping. Idle, under-defined and successful guidance retains ordinary styling.
A newly raised error is scrolled into view if necessary without changing focus;
one follow-up adjustment accounts for native task-group resizing. Repeated reports
of the same error do not schedule further scrolling. Successful validation clears
the error style. No added modal dialog, wording or validation change is proposed.

These are actual native task widgets in isolated FreeCAD processes, running UI-only
candidate modules over the installed solver. Four baseline and four candidate cases
use the real later-input rejection. All candidate messages are fully visible; valid
recovery clears their highlighting. Rejected selections, object IDs, native links
and saved visibility are preserved. No task is accepted. The fixture creates its
own models and never reads or changes an owner document/profile.

Captures are literal crops of the visible task scroll area. Full application captures
also use the established live viewport readback to avoid Qt/OpenGL capture artifacts;
no differences or geometry are painted over. Earlier candidate checks caught a
partially visible error in long panels; the final capture passes all four cases.

## Provenance

- Product baseline: `6e3176e88a83f1d39857f7f2e8aceb393bd88e1d`.
- Exact three-file UI snapshot: `540c72a2736c2c24c08fa1ed7eb3195f3551993e`,
  `C:/Users/dgium/Documents/__Apps/FreeCAD/task-error-preview/review-source`.
  This avoids touching the unrelated untracked `project.previewfirst.json`.
- Companion session: `16176df60dd2`; allowed candidate files: `plane_task.py`,
  `sketch_task.py`, `extrude_task.py`, new `task_status.py`.
- Final fingerprint: `4f5aa46a46bf63433fa196c22609ad24163c52d38805f2ac1a0544c6c4581511`.
  Inspection: preview fresh, no scope violations, approval false. No approval state
  was changed on the owner's behalf.
- Renderer/scene remain in workspace `task-error-preview`; copies and final
  candidate sources are archived here. Results: `baseline.json`, `candidate.json`.

## After approval

Integrate the shared status widget and error call sites without changing admission,
geometry or task semantics. Register/install the new module. Check selection,
validation and acceptance failures, valid recovery, incomplete guidance, long/narrow
panel wrapping, focus preservation, repeated-error scrolling and closing before a
queued scroll. Apply the same prominent inline-error convention to future feature
workflows. Existing native modal errors retain their native presentation. Install
with rollback, validate in isolated profiles, preserve open owner sessions and follow
standing commit/push/remote-verification authorization.
