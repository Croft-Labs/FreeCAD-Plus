# Sketch Modeling Tools preview — November 23, 2026

Status: historical native task-list prototype, subsequently approved with the
component-navigation and New Body card-removal previews on November 23.
See [implementation evidence](../component-task-updates-20261123/README.md).

Owner requests current modeling workflows in the sketch-selection task card:
Plus shows one Extrude entry instead of Pad/Pocket. Apply the same convention to
the implemented shared Revolve workflow: one Revolve instead of Revolve/Groove.
Classic retains its native buttons but routes component operations to the shared
panels. Pocket and Groove start in Subtract. Pad/Revolve retain existing defaults
(New Solid in the no-target fixture). Selection prepopulates the profile.
Hole, Loft, Pipe and Helix retain their current entries until their shared workflows
are implemented. TaskPanelUIMode controls this presentation independently of
toolbar/model-panel mode. Classic legacy documents retain native compatibility.

Direct screenshots: [before](before.png), [Plus](plus.png), [Classic](classic.png).
They are literal native TaskBox captures from an isolated Python TaskWatcher
prototype. No C++ selection-watcher integration is installed. `task_actions.py`
starts as a manifest of the current Workbench.cpp single-sketch command list;
candidate aliases invoke the existing native commands. Candidate shared task
modules remove only the presentation-mode dispatch guard. No feature is accepted.

`candidate.json` records both ordered lists and six actual native command routes:
Plus Extrude/Revolve and Classic Pad/Pocket/Revolve/Groove. Every route opens the
correct shared panel with the selected sketch and expected operation. Cancel
preserves object IDs, native dependency links and saved visibility. Baseline and
candidate run in fresh isolated profiles; owner sessions/documents remain untouched.

Product baseline: `9eecc2f2ca724833224a6cf31606f9b47c42167e`.
Clean snapshot: `164609a1c425bc6e417a5e8760a1b628ee17eb13`, workspace
`sketch-tools-preview/review-source`; preserves untracked `project.previewfirst.json`.
Companion session `b886cd6595c6`; allowlist `task_actions.py`, `extrude_task.py`,
`revolve_task.py`. Fingerprint
`a0c7240bf520b3d51eb0cae2df3d97e39f6c82065e156130a8b730f30a4b62d8`.
Fresh capture, no scope violations, not approved; approval state was not changed.
Final captures use the TaskBox itself rather than the surrounding empty dock area.

After approval, integrate mode-specific native sketch watchers and properly named
shared workflow command aliases, retain Classic labels/icons, and remove mode-based
dispatch bypasses in component contexts. Keep legacy-input compatibility, validation,
geometry and all other commands. Verify actual selection changes, both task modes,
independent toolbar modes, prefilled profiles, target defaults, Cancel/acceptance and
task tab restoration. Build/install with rollback, validate fresh installed processes
and shortcut, preserve owner sessions, then commit/push/verify. Do not implement
unrequested Loft/Pipe/Helix workflows as part of this task-list update.
