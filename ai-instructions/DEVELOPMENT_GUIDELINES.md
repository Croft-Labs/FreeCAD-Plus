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
    using the shared highlighted convention once its current native preview is approved.
    Preserve actionable text, wrapping, focus and valid-state recovery; ordinary
    incomplete/idle guidance is distinct from an error.

A clean checkout does not itself establish runtime stability or resolve the jitter
reported for the archived fork. Those comparisons need separately authorized build
and interaction verification with suitable settings profiles.
