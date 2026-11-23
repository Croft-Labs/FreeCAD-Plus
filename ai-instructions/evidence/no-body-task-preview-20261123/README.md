# Remove New Body task prompts — November 23, 2026

Status: historical UI preview, subsequently approved with the other two pending
changes on November 23. See [implementation evidence](../component-task-updates-20261123/README.md).

Owner requests removal of every Tasks-panel New Body starting prompt: components
are the starting point, and Bodies are backend feature results. Inspection found
one actual `PartDesign_Body` command in the task-watcher arrays: `NoSel`, titled
Start Part. Other task-watcher mentions of that name are icon identifiers, not
New Body actions. Remove this registration for all task-panel modes and contexts.
Preserve Create Geometry, selection-specific actions and actual feature editors.
Menus/toolbars and internal Body generation are outside this task-card removal.

Direct screenshots: [before](before.png), [after](after.png),
[preserved Create Geometry](create-geometry.png).

These are native-widget UI simulations, not a compiled candidate. The renderer
loads the supplied Workbench.cpp and omits the matching native card when its
registration is absent. It does not alter other cards or paint over screenshots.
Three baseline/candidate cases cover Classic component context, Plus file context,
and Plus component context. Assertions verify the expected action lists and
unchanged object IDs. The installed native binary still contains the old watcher.
No owner document/profile or existing process was changed.

Product baseline: `973a94d1638303e74598befbc985dfc64b31ba89`.
Clean source snapshot: `87607f823e9feaf25837b2e4a148b668cd1f7d36`, workspace
`no-body-task-preview/review-source`; unrelated `project.previewfirst.json` preserved.
Companion session `2a58ba5b7e21`; allowlist `Workbench.cpp`.
Fingerprint `0ec7bc653838963774b88ff82eab08f92097cd5ffa05cd36c4275b7f13a9725a`.
Inspection: fresh, no scope violations, not approved; no approval state changed.
Source candidate, scene, runner and result JSON are archived here.

After approval: apply the exact registration removal, build PartDesignGui, check
real native watchers in both task modes, empty/active/no-component documents,
selection changes and workbench reactivation. Check New Sketch and feature editing
remain usable and automatic solid results still work. Install with rollback,
preserve owner sessions, validate the shortcut using isolated settings and
commit/push/remote-verify. Do not use prototype widget hiding in production.
