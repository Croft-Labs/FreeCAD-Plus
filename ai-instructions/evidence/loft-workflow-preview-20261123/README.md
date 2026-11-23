# Unified Loft proposal — November 23, 2026

Subsequently approved in chat: "Approved. Implement". See
[implementation/acceptance](../loft-20261123/README.md). The following describes
the UI-only preview and its original evidence boundary.

Owner requests one Loft workflow with New/Add/Subtract and combined Plus task
entries, subsequently adding Solid/Sheet output. Concrete UI approval is pending; production code and installed payload
remain unchanged at 7479a0ff04278b9b15903e1fc6c8a00092b83d1a.
The [task specification](../../ui-ux-specs/TASK_PANEL.md#unified-loft--november-23-2026)
owns the proposed behavior and implementation scope.

Direct native widget screenshots:
- [Solid / New](loft-new.png), [Sheet / locked New](loft-sheet.png), [Add target cue](loft-add-target.png),
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
Up/Down and clean prototype Cancel were exercised. The amended widget checks
confirm Solid default, Sheet forcing/locking New and clearing target, return to
Solid re-enabling operations, and preservation of all section rows. Production picking, geometry,
boolean validity, drag events, editing, persistence and colors remain unimplemented.
The idle proposal modifies only process-local task action labels, not commands.
Both captures succeeded and were visually inspected. No owner profiles/documents
were used. The unrelated project.previewfirst.json was preserved.

Current Companion session `64ec80523dda` supersedes `f28df6cc461b` for Solid/Sheet;
isolated adapter baseline
`d8984bd9bd335247105d512b43622f1274ab7345`; exact candidate allowlist `loft_ui.py`.
Fingerprint `7f0837fb50c2141b8aa3107c2211c811187ef2617d025e89b32be62a6ace28ba`;
inspection: fresh preview, no scope violations, approval false/untouched.
Renderer/harness and both UI versions are retained with screenshots and results.
Render paths in the archived harness describe its original workspace location.
Source adapter remains at `../loft-workflow-preview` relative to the checkout.
Temporary render/profile output was removed after archival; the installed app and
owner sessions/settings are unchanged.
