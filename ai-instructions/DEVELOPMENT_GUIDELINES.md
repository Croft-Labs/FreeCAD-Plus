# Development guidelines

These guidelines apply to the clean FreeCAD 1.1.4 baseline selected October 10, 2026.
The earlier adopted guidelines are preserved in [the historical archive](archive/pre-restart-docs/DEVELOPMENT_GUIDELINES.md);
their implementation priorities and proposed feature lists are not an active queue.


1. Follow AGENTS.md, central workspace rules and the confirmed UI specifications.
2. Keep upstream source unchanged until a specific implementation task is authorized.
3. Reuse native geometry, links, solvers and services; decide ownership, identity,
   persistence and references before a narrow end-to-end component pilot.
4. Consult archived code for ideas, then verify each behavior against owner intent.
   Do not bulk-copy old customization modules or restore old workbench restrictions.
5. Test changes proportionately. Geometry success must be distinguished from Undo,
   recompute, save/reopen, downstream use, GUI behavior and owner delivery.
6. Keep one canonical roadmap and record source/build/runtime/publication separately.
7. Preserve the clean source checkpoint and use reviewable commits for future changes.
8. Keep build/validation output outside the checkout using the paths in AGENTS.md.
9. Every feature/operation must reuse its creation task for editing, prefilled from
   the existing feature. Verify in-place acceptance and unchanged Cancel alongside
   creation. Follow the [shared task contract](ui-ux-specs/TASK_PANEL.md#shared-task-patterns).
10. As similar feature workflows are implemented, apply the confirmed
    [selected-target visibility and validity colors](ui-ux-specs/TASK_PANEL.md#shared-selected-target-and-validity-display--november-22-2026).
    Include hidden-target selection, temporary display restoration and valid/invalid
    additive/subtractive previews in their applicable acceptance checks.
11. New feature-task errors must follow the owner's
    [prominent error feedback requirement](ui-ux-specs/TASK_PANEL.md#prominent-error-feedback--november-23-2026),
    using the approved shared `task_status.TaskStatus` widget (`setError` for errors,
    `setText` for normal guidance and successful recovery).
    Preserve actionable text, wrapping, focus and valid-state recovery; ordinary
    incomplete/idle guidance is distinct from an error.
12. When migrating additive/subtractive features to one shared workflow (for
    example Loft), combine their Plus task-panel entries in the same change.
    Keep the Classic buttons, routed to the shared workflow with the matching
    operation selected. Apply the same rule to future Pipe/Helix migrations;
    do not merge their task entries before their shared workflows exist.

## Component routing without an active Body â€” November 23, 2026

For Shell, Fillet/Radius and comparable feature collectors, use the owner's
[list-driven selection pattern](ui-ux-specs/TASK_PANEL.md#shell-selection-after-opening--november-23-2026)
when updating the workflow: activate picking by selecting its list, remove rows
with Delete/Remove, and clear references with Clear. Replace Select/Confirm
Selection toggles. Shell has no separate target field; its faces identify the solid.
Owner approved the revised Shell prototype and shared collectors. Shell, Fillet/Radius,
Chamfer and Draft now implement this interaction; apply it to comparable workflows
as they are migrated.

Owner clarification: FreeCAD Plus has an active Component, **no active Body**.
Every feature workflow we implement or modify must resolve its inputs and result
ownership from that Component, explicit geometry/target selections, or saved feature
references. Never require, infer a target from, or silently fall back to Classic's
`pdbody` state. Bodies are backend result containers. A native adapter may derive a
Body from an already resolved feature; its ambient active-Body state is not authority.

Use the approved sole-eligible-target rule where applicable; ambiguity requires
explicit selection. Retain component/occurrence access and strict History checks.
Acceptance must include multiple solids with a different or absent native active
Body, correct result ownership, Cancel/Undo and preservation of the other solid.
This rule applies to future feature migrations as well as corrections to existing
ones. Ordinary legacy FreeCAD documents retain their native workflows; changing
presentation to Classic within a Plus document does not change Plus routing.


A clean checkout does not itself establish runtime stability or resolve the jitter
reported for the archived fork. Those comparisons need separately authorized build
and interaction verification with suitable settings profiles.

## Feature input selection gestures - November 23, 2026

For feature input collectors, click adds an eligible item once; repeated clicks
retain it. Shift-click removes a matching selected input and never adds an absent
one. Preserve input order and carry the original gesture through connected/tangent
curve expansion, including deferred deliveries. Single-reference fields replace
on click and clear a matching Shift-click. Apply the same rule to comparable
feature workflows as they are implemented; retain Delete/Remove/Clear and the
existing list activation rules. History clicks must identify only the clicked
input during a feature task, without Shift range selection or visibility-eye changes.
