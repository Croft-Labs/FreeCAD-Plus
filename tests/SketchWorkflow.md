# Component sketch workflow validation

Use only the source-built FreeCAD Plus executable. Run
`tests/RunComponentDocument.ps1` with `-Executable`, a fresh `-OutputDirectory`
and one switch per native GUI process. The runner isolates preferences/documents
and rejects unexpected GUI lifecycle diagnostics. Source overlays are disabled.

| Switch | Scope |
| --- | --- |
| `-SketchWorkflow` | New Sketch commands, all support choices, native plane creation/Cancel/atomic Undo/Redo, visible support-plane region picking, signed offsets/rotations, support picking and recovery, local labels, curves, dimensions, constraints, persistence and downstream Extrude |
| `-SketchRegression` | Component panel/task contexts, sketch freedom guidance, support repair, Validate Sketch, constraint repair, reuse and native Trim mouse gestures |
| `-SketchSolver` | Inherited native solver, oriented dimensions, tangent/symmetry, construction, external references, topology naming and save/load |
| `-SketchColdFixtureDirectory <SketchWorkflow output>` | Fresh-process standard Open, native editor entry, saved support/dimension/reference state, plane recompute/Undo/Redo and reuse of a saved plane |
| `-FeedbackSmoke` / `-CoreSmoke` | Broader component geometry/history/profile/ownership regressions and exact build/source module identities |

The inherited solver suite intentionally skips one driving circle-to-line secant
case whose support remains under upstream discussion. Report that skip explicitly;
do not remove its decorator or count it as a passing test. The strict runner marks
that evidence run incomplete even when its remaining assertions pass.

`TestComponentSketchWorkflow.py` includes native Qt viewport drawing of an active
line, arc and rectangle, and a construction circle. Native geometric commands
cover Horizontal, Vertical, Parallel, Perpendicular, Equal, Coincident,
Point-on-object and Block with Undo/Redo. Native radius creation, value-dialog
Accept/Cancel, driving/reference conversion and direct reference creation exercise
dimensions. Additional solver cases cover tangent/symmetry, length/X/Y/angle/
radius/diameter dimensions on active and construction geometry, unit expressions,
and associative external projection. Line/circle/arc/ellipse/B-spline geometry
families retain active/construction flags through reopen.

`test_plus_new_file_sketch_and_viewport_curves` starts at the Plus New File
button, clicks New Sketch and the native OK button, then creates line, circle,
arc and rectangle through ribbon actions and viewport input. It does not force
the camera or call `setEdit` directly. It checks that the viewport receives the
clicks, the solver succeeds, and all seven curves survive `.cadprt` save/reopen.
This is an automated regression; it does not establish physical pointer acceptance
or resolve a reported failure that cannot yet be reproduced.

`test_origin_plane_viewport_picks_select_only_the_clicked_plane` starts with
the component selected and makes actual native viewport clicks on XY, XZ and
YZ in each New Sketch command. It checks the exact leaf selection and task
selector, Cancel identity/visibility restoration and Base-layer hiding. Each
pick starts a fresh task so another expanded selected plane cannot occlude the
target. Its ray coordinates come from the actual screen-scaled datum geometry.
Inspect the six plane captures: only the clicked plane should have selection
color. Layer gates must preserve the native coordinate-system child container;
its individual descendants retain their own non-destructive visibility gates.

With default first-dimension autoscaling, native radius insertion and Scale
geometries are separate Undo entries. The value-dialog test verifies both Undo
steps, both Redo steps and Cancel. Preserve that established native behavior;
do not misclassify the first Undo retaining a constraint as failed rollback.
Native Sketcher also owns its edit transaction separately from New Sketch.
Optional `-TestNames <Class.method,...>` runs focused diagnosis and records the
filter in results; exclude those reruns from distinct final coverage counts.

A fully constrained rectangle with a reference construction diagonal drives an
Extrude. Width edits update measured dimensions and solid volume; Undo/Redo and
`.cadprt` reopen retain constraints, support and semantic object identities.
Cold-process checks move the saved support plane and verify downstream position.
Task failure checks cover nonplanar/edge/missing/foreign and deleted supports,
pending tasks and correction without leaked planes/sketches.

Review `new-plane-options.png` and `constrained-reference-sketch.png` in the
workflow output. `results.json`, suite logs, process results and runtime hashes
are evidence; screenshots alone do not establish solver or persistence behavior.
The current run and exact incorporation evidence live in
[WORK_STATE](../ai-instructions/WORK_STATE.md). Automated Qt events establish GUI
coverage. Physical gestures, additional DPI/themes and exhaustive combinations
of every native Sketcher tool remain separate acceptance work.

Datum-plane acceptance covers the new-file Tasks action and New Sketch's Create
new plane choice. Confirm Define Surface, Z Direction, Sketch Origin and X
Direction appear in order. Projected references defaults to the component origin
and closest component axis projected onto the surface. Pick a vertex/datum point,
an edge (curved edges use their midpoint tangent), or two ordered points. Verify
independent X/Z reversals, right-handed axes and inline rejection of degenerate
projections. Test tilted/moved supports, moved components, symmetric-axis ties,
recompute, Undo/Redo, helper cleanup and .cadprt reopen with native attached sketches.
`TestComponentPlaneFrame.py` owns these checks. Retain explicit legacy Rotation
angles and Axis directions modes and their existing API tests. Create Datum Plane
keeps New Sketch open and selects its new attachment; Cancel after explicit
creation keeps the plane, while Cancel before creation leaves no objects. The
projected-plane task and 360-pixel width captures record the UI acceptance.
