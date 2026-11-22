# Approved sketch coordinate-system hiding

Owner approval and direct native preview provenance are recorded in `approval.json`.
This folder contains focused implementation evidence, not a Companion dashboard.

The render mask hides the component native Origin/axes/planes during sketch drawing.
History eyes use the effective mask and continue to edit persistent Visibility only
when explicitly clicked. Other geometry, native task transactions, stored visibility,
Sketcher drawing axes, geometric constraints and deliberate dimensions are preserved.
Plane selection remains a separate stage with visible reference planes.

`build-regression.txt` and `regression.txt` each record 162 successful native tests
against the development build and installed app respectively. Seven
new focused cases cover default/mixed/hidden frames; new-sketch handoff and Undo/Redo;
eye accept/abort/Undo/Redo; native save during edit; body ownership; external source
ownership and host closure; and the mask's absence of dirty/transaction side effects.
The broader suite retains existing sketch, Extrude, plane, tree-eye, numeric-input,
History-tab, Move and Rotate checks. Plus Save still guards pending operations; the
save-during-edit test exercises native Document.save directly without changing that
guard. The mask itself adds no dirty state; native Sketcher may modify its own data
on editor entry as before.

`visual.FCMacro` creates a rectangle through real mouse input in the installed app.
Its screenshots show placement, drawing and exit. No injected product implementation
or staged preview code is used. `reopen.FCMacro` starts a separate installed process
and verifies geometry/constraint identity, persistent coordinate visibility, existing
sketch hiding/restoration and the previous History tab. Native screenshots were
visually reviewed; the drawing frame is absent and Sketcher's red/green axes remain.

`run-validation.py` runs bounded native processes with isolated settings; it supports
`regression --broad`, `regression --installed --broad`, `visual --installed`, and
`reopen --installed`. `install.py` retains rollback copies and verifies the three
changed Python files against source, build and installed hashes. `restart-shortcut.ps1`
uses the existing desktop shortcut with explicit isolated user/system/data settings.
No owner profile, unrelated shortcut or unrelated untracked config is modified.
`shortcut.json` verifies the actual installed module and isolated settings paths;
the app remains open. `cleanup.ps1` validates absolute target containment and rejects
reparse points before removing disposable fixtures and inactive profiles. Rollback
copies, the active shortcut profile, logs and screenshots remain available.
