# Target highlighting and sole-solid selection — awaiting approval

Owner revision: highlight the missing target field instead of a popup, and choose
the sole body automatically when entering Add/Subtract. This supersedes the
unapproved November 22 popup; production and installed task code remain unchanged.

Direct native UI screenshots:

- [Multiple solids](multiple-solids.png): focused amber Target solid and inline guidance.
- [One solid](sole-solid.png): target filled automatically; profile picking is active.
- [No solid](no-solid.png): amber target and explanation that a new solid is needed.
- [Current baseline](baseline.png): original task presentation.

[Candidate results](candidate.json) record 12 cases: zero/one/two fixture candidates
for Extrude/Revolve Add/Subtract. All show the intended selection/highlight states,
no modal popup, unchanged hidden-target eye when selected automatically, and restored
native IDs/visibility after task cancellation. [Baseline results](baseline.json)
record the current behavior. Native Qt task code runs in separate isolated FreeCAD
processes. The candidate uses renderer-supplied target lists: it is a UI simulation,
not a finished production eligibility algorithm or intake guard.

After approval, derive eligible current Body results from the active component,
respect native/source/predecessor validation on creation and edit, keep existing
valid targets and preselected curves, and use the selected-target display already
implemented for hidden solids. Handle direct command startup, zero/multiple results,
target clearing/deletion/invalidity, region picking and task cleanup. Do not reselect
on every update after deliberate Clear. New Solid has no target requirement. Verify
native picking, history eyes, Undo, Cancel and save/reopen as applicable, install
with rollback and isolated shortcut verification, then commit/push/remote-verify.

Companion session ac148f57d8fe; exact allowed file extrude_task.py.
Source snapshot e56d5fefc6411a151d5656af4782266c6315ed93 from production
04e5bcb684fffc3b8a2c25dae12f3a0c47129baf.
Fingerprint b53ce972452a4bfb803940133c9713795dea855d781661e1b2618c254b3f55be.
Captures baseline-05d1b7f2.png / candidate-4832a296.png; fresh, no scope violations.
Approval state was not changed. Fixture/renderer: workspace target-highlight-preview.
Owner documents, settings and unrelated project.previewfirst.json were untouched.
