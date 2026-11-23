# Surface tools inside Modeling — November 23, 2026

Subsequently approved in chat and implemented. See [installed acceptance](../thicken-20261123/README.md).

Owner revised the pending Shell/Thicken proposal: move the Surface tab's tools
into a Surface section on Modeling, remove that tab, and place Thicken in the new
section. Shell stays in Dress-Up. This supersedes the earlier proposed Thicken
placement beside Shell; the pending feature/error-recovery scope is retained.

Direct native screenshots: [updated Modeling ribbon](modeling-ribbon.png),
[Surface section](surface-section.png), [before](before-ribbon.png),
[Thicken task](thicken-new.png), [Add target](thicken-add-target.png),
[Shell task](shell-task.png), [invalid Shell selection](shell-invalid.png).

The section is between Dress-Up and Transformation. Thicken is a large labeled
button; six native Surface actions remain individual compact buttons: Filling,
Fill Boundary Curves, Sections, Extend Face, Curve on Mesh and Blend Curve. Each
retains its icon, native command name/tooltip and independent action. Ribbon
borders, dividers and scrolling remain. Only the Plus Surface tab is removed;
the native workbench and Classic access remain available.

Implementation must load Surface commands without switching from Modeling,
map former Surface Design navigation to Modeling, and avoid an extra Surface
entry in the Plus mode selector. Surface geometry/tasks are not reimplemented
by this placement change. Thicken's pending New/Add/Subtract, target behavior,
thickness/directions, persistence, history and Shell invalid-entry repair remain
as recorded in the [earlier scope](../shell-thicken-preview-20261123/README.md),
except for this explicit placement correction.

Native preview checks confirm all seven controls and their names, no Surface
tab, active PartDesign/Modeling, Shell task rename, New default, Add/Subtract
target cue, symmetric total thickness and clean prototype cancellation. Initial
widget lookup assumed plain buttons; native Surface actions can use toolbar-factory
wrappers. The corrected harness recognizes both actual control types. Disabled
native actions reflect the current empty document/selection normally.

This remains UI-only: Thicken OK is disabled and the filled-offset illustration
is independent fixture geometry, not a saved Plus feature. No production install
or invalid-entry repair has been performed. Combined preview approval is pending.

Companion session 5e9afa49ce33 supersedes 4ceae9ed5cc9 for this combined proposal.
Adapter baseline dfbae579efaf14186f7a1840925398e5529e5acb against installed
7adf23f3b2; exact candidate allowlist shell_thicken_ui.py. Final fingerprint
54411b35662f1b635829af79c86f77f4f28f2201cd715b2343c81026f8634db4;
capture fresh with no scope violations. Tool approval state untouched. Isolated
profiles/synthetic documents only; generated fixtures removed after archival.
Unrelated project.previewfirst.json is untouched.
