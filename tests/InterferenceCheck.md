# Interference and clearance: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD and published installers do not contain this batch.
Evidence: `D:\Temp\Office-PC\freecad-plus-interference-20260930`.

1. Open `visual\Interference-Check.FCStd` and activate the Part workbench.
2. Select First, Overlap, Contact and SmallGap in the tree. Choose
   **Part > Interference and clearance...**. Review the explicit input list.
3. Leave required clearance at 1 mm and contact tolerance at 0.000001 mm; click
   **Check included pairs**. Six pairs appear. First/Overlap has 200 mm³ common
   volume; Overlap/Contact touches; Contact/SmallGap has a 0.25 mm gap below clearance.
4. Select a result row and click **Select result pair**. Native selection highlights
   those inputs without hiding others or modifying the geometry. Hidden objects stay
   hidden; inspection includes them if listed. Use the tree to reveal them if needed.
5. Uncheck Overlap. Previous results clear; checking again reports three pairs and
   one explicitly excluded input. This is a check of the included set only.
6. Change the required clearance to 0.25 mm: the 0.25 mm gap meets it. Contact means
   no common solid volume and separation at or below the stated contact tolerance;
   it does not claim mathematical zero separation. Any positive common solid volume
   is reported as overlap, even if smaller than the linear contact tolerance.
7. Move SmallGap or edit a source dimension. Results clear immediately. Recompute
   and check again; dirty or invalid inputs appear as Unresolved rather than using
   a cached shape. Undo/Redo and recheck, then save/reopen and repeat.
8. Include the Unavailable link with valid solids using **Replace inputs with
   current selection**. Every affected pair is Unresolved and the summary says
   Incomplete. Removing an input from the document cannot silently retarget a new
   object with the same name. Repair or explicitly replace the inputs.
9. Close the dialog or document. No measurement objects, copied shapes, visibility
   changes or model transactions remain from inspection.

Scope: 2-12 whole, valid, solid-only Part shapes/Body results or direct same-document
shape/Body Links; structural Part container paths retain world placement. Face picks,
meshes, sheets, mixed compounds, Link arrays, paths through another occurrence and
external/missing definitions are unsupported. Unavailable whole objects can be listed
but their pairs remain unresolved. No automatic whole-assembly expansion or omission.
Exclusions apply to listed participants, not individual pair exceptions. Results are
transient; no persistent inspection report, broad-phase acceleration, cancellation,
contact-face graphics or automatic reveal is included. Larger inspections and physical/
high-DPI acceptance remain open under F101. Stop here for owner feedback.
