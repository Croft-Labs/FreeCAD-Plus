# Target-first Add/Subtract popup — superseded

Owner revision, November 23: use field highlighting and automatic sole-body selection.
This popup was never approved or installed. Use the
[revised preview](../target-highlight-preview-20261123/README.md); the text below is
historical preview evidence, not a pending implementation instruction.

Owner request: missing-target errors must appear before choosing profile curves for
Add/Subtract. The native candidate shared by Extrude and Revolve shows a warning on
mode entry without a target, then focuses the existing Target solid field after OK.

- [Add popup](add-popup.png): choose a target before curves; select the solid to add to.
- [Subtract popup](subtract-popup.png): select the solid to subtract from.
- [After OK](target-focus.png): native Target solid field focused.
- [Current task](baseline.png): current mode entry does not show the warning.
- [Candidate results](candidate.json), [baseline results](baseline.json): four native
  feature/mode cases. Candidate prompts all four and focuses the target; no popup on
  preview updates or when a target exists. Native document IDs are unchanged.

These are native Qt screenshots from the actual task code in an isolated worktree,
not an installed feature. The candidate only demonstrates the mode-entry popup/focus
handler. Complete intake guards are pending: direct Subtract startup, missing/invalid
or cleared targets, viewport region picks, preserved existing profile selections,
New Solid/edit behavior and safe dialog/task cleanup. Repeated updates must not nag;
target selection continues to use existing History visibility and sequential rules.

Session: 22942ee0d6a0; exact allowed source: extrude_task.py.
Production baseline: 04e5bcb684fffc3b8a2c25dae12f3a0c47129baf.
Focused source snapshot: e56d5fefc6411a151d5656af4782266c6315ed93.
Final fingerprint: 6fe52a36daf751850326d6e430263bfa9a9614140b78f844bdd1387ac9ebe2da.
Captures: baseline-e2fb903b.png / candidate-549364e2.png; fresh, no scope violations.
Tool approval state was not modified. Chat approval is the remaining gate.
Fixture and renderer: workspace target-first-preview/scene.FCMacro and render.py.

Original source, installed payload, the owner's unsaved document window and unrelated
project.previewfirst.json remain untouched. After approval, implement the complete
shared guard, run focused native lifecycle/picking checks, install with retained
rollback, verify through the existing shortcut using isolated settings, and commit/
push/remote-verify under standing authorization.
