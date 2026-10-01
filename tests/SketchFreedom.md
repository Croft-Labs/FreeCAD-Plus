# Sketch freedom guidance (F047)

Use the source-built FreeCAD Plus fork. Open a sketch in edit mode and inspect the
existing **Sketch Edit** solver task.

1. Draw a circle and constrain its radius. The solver still reports freedom for
   the center. The new text explains that freedoms may be coupled and that the
   count does not identify separate movement directions.
2. Click **Select unconstrained geometry** (also reachable by Tab). Native Sketcher
   selection highlights geometry/points where the solver detects freedom. This
   replaces the current selection and does not add or remove constraints.
3. Locate the center at the origin. The task reports fully constrained and disables
   the selection button. Undo and redo the constraint to check the state changes.
4. Add an incompatible second radius. The task explains that a solver issue must
   be repaired before interpreting movement; the freedom button stays disabled.
   Remove the conflicting constraint and inspect the recovered state.
5. Try construction geometry and a reference dimension: these are distinct from
   fixed geometry. A reference dimension measures rather than removes freedom.
   Save, close, reopen and edit the sketch again; native constraints remain intact.

This checkpoint reuses the native solver state, geometry colors and selection
command. It adds no movement arrows or numerical per-direction diagnosis. Fixed or
Block geometry can be fully constrained without dimensions. A degree-of-freedom
count is not a complete diagnosis of coupled movement or a guarantee of a valid
closed profile. Full F047 and physical keyboard/high-DPI acceptance remain open.

Run `TestSketchFreedom` and `TestConstraintRepair` in the matching rebuilt GUI
with `tests` on `sys.path`. Roadmap 11.4c/d owns build and acceptance evidence.
Stop at this usable checkpoint and rotate pending owner workflow feedback.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-sketch-freedom-20261001`.
Seven freedom checks plus eight unchanged repair checks pass; five GUI captures
were reviewed. The visual/ folder contains Sketch-Freedom.FCStd (free center) and
Sketch-Located.FCStd (located center). This is source-built validation, not an
installer update or physical owner acceptance.
