# Manufacturing STL export: owner workflow test

This F127 pilot adds **Part > Manufacturing export...** in the Part workbench.
It exports selected, recomputed whole solids and whole solid occurrences using
visible mesh-quality settings. It is also discoverable through Ctrl+K.

Use this checkout's development launcher:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Previous installers and the separately installed FreeCAD do not contain this batch.
Evidence/examples are under
`D:\Temp\Office-PC\freecad-plus-manufacturing-export-20260930`.

1. Open `visual\Manufacturing-Handoff.FCStd`. Select **Box** and **Occurrence** in
   the tree, then open Manufacturing export. Review the listed input identities,
   dimensions and **STL - millimeters - world placement** contract.
2. Choose an output `.stl` filename and export. Import the STL as millimeters in
   your receiving program. Confirm Box is 12 x 8 x 6 mm and Occurrence retains its
   rotated, translated placement. Exporting does not create native model features.
3. Select **Sphere**, press **Use current selection**, and export separate Coarse
   and Fine files. Compare the triangle counts and curved surface approximation.
   Linear deflection is an absolute millimeter tolerance; angular deflection is
   in degrees. The selected preset fills both visible, editable values.
4. Change quality values, enter a custom preset name and save. Reopen the dialog
   and choose that preset. Saving an existing custom name updates it; built-in
   names are reserved. Reset presets removes custom settings. Presets store quality
   only, never objects, configurations or output paths.
5. Change tree selection while the dialog remains open: the listed inputs stay
   fixed until Use current selection. Faces/edges and members inside linked Part
   containers are rejected rather than expanded silently. Whole objects within
   ordinary native Part containers are supported.
6. Try an existing output path and decline replacement; the existing file should
   remain unchanged. Try a stale input or invalid path, correct it, and retry.
   Recompute/repair the model before exporting. Current recomputed geometry of the
   listed identities is exported; the dialog does not store an old geometry snapshot.

STL carries triangles, not parametric history, colors, assembly identities or units
metadata. Coordinates are written in millimeters in the document's world frame.
This pilot checks solid-only source geometry and closed output meshes; separate
solids are not fused, and collision/self-intersection/printability analysis is not
claimed. Fine settings can be expensive on large geometry.

Whole F127 remains open for STEP/3MF/DXF, explicit configurations and orientation/
unit overrides, mesh inputs, deep occurrence paths, broader output-property checks
and physical/high-DPI acceptance. Stop for workflow feedback before extending the
format portfolio or polishing this dialog.

Automated acceptance is in `TestManufacturingExport`: dimensions/volume after
reimport, nested world placement, selected occurrences, coarse/fine comparison,
stale/unsupported-input and existing-file protection, quality/preset/reset behavior,
native menu/dialog interaction, fixed input identity, and deleted/replaced inputs.
