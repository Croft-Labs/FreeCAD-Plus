# Assembly freedom guidance (F077)

Use the source-built FreeCAD Plus fork. Activate Assembly and double-click an
assembly to edit it. Its existing **Solver messages** panel now explains the
scope of the solver's freedom count and offers two selection buttons.

1. Create a grounded base, a second component joined by a slider, and a free part.
   Recompute/solve. The assembly is underconstrained even though the slider has
   a joint path to ground.
2. Click **Select grounded components**. Native grounding selects the base;
   read-only placements and grounded rigid groups also follow native rules.
3. Click **Select unconnected components**. Only the free part is selected.
   A connected slider or hinge may still move. The assembly count is not a
   per-component movement diagnosis, and the button does not select all movable parts.
4. Select the slider in the tree and use **Select Component Joints** to inspect
   its controlling joint. Existing solver links navigate malformed/conflicting joints.
5. Add fixed joints until the solver reports fully constrained. Freedom selection
   is disabled; grounding remains distinct from being held through ordinary joints.
6. Undo/redo a joint, then save, close, reopen and edit the assembly. Selection and
   solver guidance should follow the restored relationships. If the solve fails,
   resolve its reported issue before interpreting movement. Stale assemblies require
   recompute; selection buttons do not alter placement, joints or undo history.

This bounded checkpoint adds visible explanations and relationship navigation.
Per-component degrees of freedom/direction arrows, detailed conflict attribution,
incomplete-joint/unloaded/external/nested assembly diagnosis and physical acceptance remain open
under full F077. Grounding does not certify a successful solve. Stop here and
rotate to another family pending owner workflow feedback.

Run `TestAssemblyFreedom` and `AssemblyTests.TestCore` in the matching rebuilt GUI,
with `tests` on `sys.path`. Roadmap 12.4a/b owns validation evidence.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-assembly-freedom-20261001`.
Eight assembly checks (freedom-final/), thirteen inherited core checks (grouped/)
and seven shared task-dialog regression checks (freedom-verified/) pass. Five
captures were reviewed after the initial grouped build and one corrective build.
The visual/ folder contains Slider-and-Free-Part.FCStd and Fully-Constrained.FCStd.
The solver panel now appears before a task dialog is opened, survives dialog
open/close and follows its owning document. This is source-built validation,
not an installer update or physical owner acceptance.

Known boundary: the native solver filters out some empty/incomplete joints.
This batch validates actual redundant-joint feedback; the displayed freedom count
is not proof that every unresolved joint or external reference has been diagnosed.
