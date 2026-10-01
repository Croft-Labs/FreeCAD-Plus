# Missing-coincidence review: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Published installers and the separately installed FreeCAD do not contain this batch.
Evidence: `D:\Temp\Office-PC\freecad-plus-sketch-repair-20260930`.

1. Open `visual\Sketch-Repair.FCStd`, activate Sketcher, select Profile outside edit
   mode, and choose **Sketch > Validate Sketch** (or find
   **Validate Sketch** through command search).
2. In Missing Coincidences, use search tolerance **0.1 mm**, then Find. The rectangle
   has a 0.01 mm gap. The list identifies both geometry endpoints and their measured
   separation. Select the row to highlight its endpoints in the 3D view.
3. Review/check the candidate. Neither Find, row selection nor checking a box changes
   the sketch. Close now leaves the original geometry and dimensions intact.
4. Reopen, Find, check the candidate, and **Add Checked Coincidences**. The existing
   Width/Height constraints remain; one coincidence closes the gap. Undo reopens it;
   Redo closes it. Close preserves a committed repair.
5. Create a solid extrusion 5 mm long from the repaired profile. The 20 × 10 mm
   rectangle yields 1000 mm³. Save/reopen and change Width to 25 mm: the extrusion
   updates to 1250 mm³ without losing the repair.
6. Test a sketch with several nearby endpoint pairs. Only checked candidates are
   repaired. Construction geometry follows the explicit Ignore construction setting.
   Changing that setting or tolerance clears candidates and requires another Find.
7. Edit the sketch while the task is open. Previous candidates clear; Find again.
   Invalid tolerance text produces a correction message instead of a fallback value.
8. Show and select the included ConstrainedGap sketch and Find at 0.1 mm. Its two
   10 mm lines start 20.01 mm apart, leaving endpoints that cannot meet while those
   dimensions remain. Check the candidate and apply: the repair rolls back,
   preserving all seven original constraints and the geometry.

Search reuses the native missing-coincidence detector and its X/Y tolerance policy;
the result list reports actual endpoint distance in mm. Tolerance only controls
candidate discovery. Adding a coincidence may move geometry according to the solver.
No existing constraint is silently deleted to make a repair succeed. Pending edit
transactions must finish before repair. No candidates does not certify profile
closure: duplicate/tiny/overlapping geometry and self-intersections may still remain.
Native coincidence insertion can move Block-constrained geometry while retaining
the Block constraints; do not treat Block as a guaranteed rejection of gap repair.
The native detector can omit endpoints already referenced by dimensional constraints;
an empty candidate list is therefore not an exhaustive gap report.

This bounded F049 increment improves the existing task, not the other inherited
validation/repair sections. Duplicate diagnostics, broader profile repair, before/
after geometric preview, zoom-to-candidate and physical/high-DPI acceptance remain
open. Stop for owner feedback before extending this workflow.
