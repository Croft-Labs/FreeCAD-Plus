# Window and crossing selection: owner workflow (F039)

Use the source-built fork at
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.

1. In Part, create two separated boxes. Choose **Edit > Box selection** (Shift+B).
2. Drag left to right around only the center of a box. The solid rectangle requires
   full projected enclosure; that box should not be selected.
3. Drag over the same region right to left. The dashed rectangle uses crossing
   selection and includes the box. Whole-object crossing tests projected bounds,
   so it is not exact silhouette or frontmost-only picking.
4. Enclose the whole box left to right. Hold Ctrl to add to an existing selection;
   release without Ctrl to replace it. Escape abandons the active rectangle.
5. Try the same behavior by dragging from empty space in CAD navigation mode.
6. Choose **Box element selection** (Shift+E) and a vertex, edge or face filter.
   The chosen element category should be collected rather than a whole-object
   shortcut. Command-specific selection gates still apply. Hidden objects are
   excluded, while occluded/back-facing entities of visible objects remain eligible.

Selection does not edit geometry, placements, history or saved files. Native projected
bounds and tessellated subelement geometry remain the selection representation.
General curve accuracy, sketch-wide parity, subtract modifiers and physical/high-DPI
acceptance remain open. Stop for feedback at the bounded workflow checkpoint.

Known observation: selecting the nested assembly changes one native serialized
BRep flag on its source. Geometry coordinates, volume, area, placement, identity,
object state and Undo count pass; byte-for-byte nested BRep preservation is not claimed.

Roadmap 10.5g/h records the 2026-10-01 checkpoint: two tasks batched before one
successful build, nineteen distinct passing checks and six reviewed captures.

Open the owner fixture at
`D:\Temp\Office-PC\freecad-plus-window-selection-20261001\visual\Window-Selection.FCStd`.
The same folder holds captures; the parent holds build logs, test results and the
source/runtime hash manifest.
