# Drawing setup: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Evidence: `D:\Temp\Office-PC\freecad-plus-drawing-setup-20261001`.
Existing installers do not contain this batch.

1. Open `visual-accepted\Drawing-Source.FCStd`, switch to TechDraw and select Bracket in
   the tree. It is a 40 x 25 x 12 mm native Boolean solid with an 8 mm bore.
2. Choose **TechDraw > Page > Create drawing sheet**. Select A4 or A3 landscape,
   a drawing/model scale ratio, base orientation and first/third-angle projection.
   The optional top/right projections are relative to that base orientation.
3. Click **Create sheet**. The native sheet opens with linked views. Double-click
   its tree entry to reopen it later. Inspect view placement and scale. First angle
   places the top view below the base and the right view to its left; third angle
   places them above and to its right.
4. Change Blank.Length from 40 to 50 mm and recompute. The base view widens with
   the solid. Native TechDraw update preferences still apply; use Redraw Page if
   automatic drawing updates are disabled. Save/reopen and edit again.
5. In a separate pass, Undo immediately after creation removes the sheet, template
   and views together; Redo restores them. Cancel before creation adds nothing.
6. Start another setup and edit the source. Creation disables until recompute and
   **Review again**. Try an excessive scale: an inline message asks for a smaller
   scale/larger sheet and keeps the dialog open without creating partial objects.

`visual-accepted\Drawing-Sheets.FCStd` contains first- and third-angle examples.
`visual-accepted\Drawing-Edited.FCStd` contains the widened source and updated views.
All objects use native TechDraw persistence and references; there is no custom proxy
or new file format. Sheet coordinates are mm; scale is dimensionless. Dimension
units and annotations continue to use existing TechDraw controls.

Scope: one whole document-root solid or Body, same-document destination, two built-in
ISO landscape templates, base orientation and optional top/right projected views.
The templates contain borders only: no sample authors/materials or fixed projection
symbol is added. The chosen convention is saved on the page and projection group;
inspect their native Projection Type properties. Add your own title block/annotations
using the existing drawing tools.
A conservative bounding-diagonal fit check leaves space for borders and title block;
it can reject some layouts that an expert could place manually. Later source growth
may require manually adjusting the native group scale/position. No geometry is created
during review, and no graphical pre-creation preview is claimed.

F102 remains open for occurrence/arrangement and external sources, custom templates,
section/detail setup, graphical preview, broken-reference repair and physical/high-DPI
acceptance. F103 annotations remain separate. Stop here for owner workflow feedback.
