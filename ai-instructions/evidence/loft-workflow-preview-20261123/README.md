# Unified Loft proposal — November 23, 2026

Owner requests one Loft workflow with New/Add/Subtract and combined Plus task
entries. Concrete UI approval is pending; production code and installed payload
remain unchanged at 7479a0ff04278b9b15903e1fc6c8a00092b83d1a.
The [task specification](../../ui-ux-specs/TASK_PANEL.md#unified-loft--november-23-2026)
owns the proposed behavior and implementation scope.

Direct native widget screenshots:
- [New](loft-new.png), [Add target cue](loft-add-target.png),
  [Subtract target cue](loft-subtract-target.png),
  [selected target](loft-subtract-selected.png), [error](loft-invalid.png).
- One Loft entry for [single sketch](modeling-tools-single.png) and
  [multiple sketches](modeling-tools-multiple.png).
- Installed baseline: [native task](before-task.png),
  [separate task entries](before-modeling-tools.png).

The baseline native task uses an isolated legacy three-circle Loft fixture;
the candidate uses the same named section examples in native shared widgets.
Task-entry screenshots use the same synthetic Plus component and sketches.
Candidate OK is disabled. Target text and error states are simulated. Section
Up/Down and clean prototype Cancel were exercised; production picking, geometry,
boolean validity, drag events, editing, persistence and colors remain unimplemented.
The idle proposal modifies only process-local task action labels, not commands.
Both captures succeeded and were visually inspected. No owner profiles/documents
were used. The unrelated project.previewfirst.json was preserved.

Companion session `f28df6cc461b`; isolated adapter baseline
`d8984bd9bd335247105d512b43622f1274ab7345`; exact candidate allowlist `loft_ui.py`.
Fingerprint `35d02ca3190f8dcb9000ab296a39d609040a21aeacb2d478b8889cde133dd5dc`;
inspection: fresh preview, no scope violations, approval false/untouched.
Renderer/harness and both UI versions are retained with screenshots and results.
Render paths in the archived harness describe its original workspace location.
Source adapter remains at `../loft-workflow-preview` relative to the checkout.
