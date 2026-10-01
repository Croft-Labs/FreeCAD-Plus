# Associative dimension reference repair (F103)

Use the source-built FreeCAD Plus fork and TechDraw's existing **Repair dimension
references** command (`TechDraw_DimensionRepair`). Select a drawing dimension,
then open the command.

1. Select replacement projected edges/vertices in the drawing and click **Replace References With
   Selection**. The reference lists show the proposed replacement. Geometry and
   the saved dimension remain unchanged while reviewing.
2. Read the mode message. Projected 2D replacement clears previous 3D references;
   selecting source-model geometry instead establishes true 3D measurement.
   Drawing dimensions measure the source; they do not drive its dimensions.
3. Click **OK**. A compatible repair recomputes and commits as one undo action.
   Inspect the measured value, undo and redo, then save and reopen.
4. For a diameter dimension, review two projected circle edges and click OK.
   The incompatible reference count must leave the task open, restore the original
   references/value, and report the failure. Select one circle and retry.
5. Cancel a reviewed replacement. References, measurement mode, source geometry
   and undo history must be unchanged. OK without reviewing a replacement stays open.
6. Edit the referenced source after saving/reopening and recompute. The dimension
   must follow its replacement source. Existing formatting remains intact.

The bounded fixture uses two cylinders of radius 5 and 8: true measurement of the
first is diameter 10; repairing to the second's projected circle yields 16. Editing
the second radius to 9 after reopen yields 18 while the first stays radius 5.

This checkpoint covers native reference-list review and atomic reference handoff.
It does not add graphical dimension preview, automatic lost-reference matching,
hole/thread callouts, topology-stable annotation metadata or broader dimension
type certification. Full F103 and physical owner acceptance remain open. Stop at
this workflow checkpoint and rotate pending feedback.

Run `TestDimensionRepair` and `TestDrawingSetup` in the matching source-built GUI
with `tests` on `sys.path`. Roadmap 15.3c/d owns current validation evidence.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-dimension-repair-20261001`.
Seven repair checks (repair-verified/) and seven unchanged drawing setup checks
(grouped/) pass after one grouped native build. Five task captures were reviewed.
The visual/ folder contains Original-3D-Diameter.FCStd,
Repaired-2D-Diameter.FCStd and Edited-Repaired-Diameter.FCStd for owner testing.
Allow a reopened drawing to finish projecting before editing its source.
This is source-built validation, not an installer update or owner acceptance.
