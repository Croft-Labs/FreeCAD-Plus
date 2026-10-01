# Sketch support: owner workflow test

In the **Sketcher workbench**, select one sketch outside edit mode, then choose
**Sketch > Inspect and change sketch support...**. The command is also available
through Ctrl+K after loading Sketcher.

Use this checkout's development launcher:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The previously published installers and separately installed FreeCAD do not contain
this batch. Evidence is under
`D:\Temp\Office-PC\freecad-plus-sketch-support-20260930`.

1. Open `visual\Sketch-Support.FCStd`, which uses native objects only. It contains a
   rotated Part, two planar supports, a radius-constrained Profile and an extrusion.
   Select **Profile** and open the command. Inspect its current support and world
   placement.
2. Select the face of **ReplacementPlane**, then click **Use selected planar face**.
   The replacement identity and editable face name appear in the dialog.
3. Choose **Preserve local attachment offset**, then **Preview placement**. The
   numeric result reports candidate world position/orientation and attachment
   offset. Change to **Preserve world placement** and preview again. No original
   model changes occur during either preview. Close now to discard the attempt.
4. Reopen and preview Preserve world, then Apply. The support changes while the
   sketch and extrusion keep their world placement. Undo returns to OriginalPlane;
   Redo restores the replacement. Save, reopen, and inspect the support/geometry.
5. Try Preserve local instead: the existing offset follows the new face's frame,
   so downstream geometry may move. Check the extrusion after Apply. The numerical
   preview evaluates attachment placement only, not constraints or downstream solids.
6. Enter an unavailable face such as Face99 and preview: Apply stays disabled and
   an inline error explains the problem. Correct to Face1 and preview again. An
   existing broken face attachment can be repaired with Preserve local; Preserve
   world requires a valid, recomputed old sketch placement.
7. Move/recompute the replacement plane after preview, then Apply: the stale preview
   is rejected. Preview again to accept the updated candidate. Deleting the replacement
   clears it; closing/deleting the sketch's document closes its editor.

This pilot supports planar faces in the sketch's same native container. It rejects
dependency cycles, stale/invalid supports, linked occurrence supports and direct
cross-container support changes. Preserve world also rejects expression-driven
attachment offsets; Preserve local retains those expressions. Apply owns one native
transaction and refuses a caller's pending edit. Close does not undo an earlier Apply.

The experimental cross-part reference adapter remains test-only; it has not been
promoted or added to this workflow. Graphical ghost previews, direct datum/principal
plane creation, occurrence policies, general external-projection acceptance and
physical/high-DPI interaction remain open under F124. Stop at this usable editor
for owner feedback before adding more refinements.

Automated acceptance: `TestSketchSupportCommand` covers installed entry, both previews,
Close, world Apply/Undo/Redo/reopen, local missing-face repair, invalid-face correction,
stale-preview rejection, cycles, occurrence rejection and editor lifecycle.
`TestPartHistoryAdapters` retains the existing attachment/reference regression evidence
while direct reattachment now executes the installed `SketchSupport.py` core.
