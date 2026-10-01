# Measurement meaning and point snapshots: owner test

Use **Tools > Measure** in the development application:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
This extends the existing native tool; existing published installers do not contain
this batch. Evidence and the example are under
`D:\Temp\Office-PC\freecad-plus-measurement-20260930`.

1. Open the native example in `visual\Measurement-Context.FCStd`. It contains two
   radius-5 circles whose centres are 20 mm apart. Select both circular edges and
   open Measure. Choose **Distance**. The result is **20 mm**, not the 10 mm gap
   between their nearest edges. Read the new Selected entities and meaning text.
2. Change the unit to inches. The displayed value changes; the geometry and native
   measured distance remain unchanged. Delta components are unsigned world-axis
   differences, not signed offsets or local component coordinates.
3. Choose **Distance Free** after picking two viewport points. This measures those
   picked world coordinates, not minimum clearance. The panel labels it a point
   snapshot and shows UTC capture time. Tree selection alone does not supply useful
   picked positions; use viewport points for this mode.
4. Save the point measurement and close Measure. Select the saved measurement in
   the tree. Its **Snapshot** properties show UpdatePolicy, CaptureTime and
   CaptureSources. Sources are informational paths, not live links. Rename the
   measurement if useful; the native label/result behavior remains unchanged.
5. Move CircleB and recompute. A saved **Distance** measurement follows its native
   geometry references. A saved **Distance Free** measurement keeps its captured
   points and value. Save/reopen preserves this distinction and capture information.
6. Manually edit a saved snapshot's Position1/Position2. CaptureTime and CaptureSources
   clear because the coordinates no longer represent the original pick. Undo restores
   the coordinates and provenance; Redo clears provenance again. Missing capture
   time means unknown, including old files without this metadata, not a new capture.
7. Try Geometric Center on a placed box. The text identifies a geometric centre in
   world coordinates, without material density or physical mass. Radius/diameter
   text distinguishes those measurements from wall thickness.
8. Clear selection or Close without Save. The current unsaved measurement is removed;
   previously saved measurements remain.

The existing native measurement types, commands, geometry algorithms and file
identities remain in use. New snapshot fields are additive properties on
Measure::MeasureDistanceDetached; CaptureTime and CaptureSources default to empty.
Restore does not invent historical provenance. Explicit point edits clear metadata
outside restore/Undo/Redo. No live links or driving constraints are added.

This bounded F098/F099 batch does not establish a complete material/mass, thickness,
mesh-accuracy or saved-measurement repair workflow. Physical picking, high-DPI and
broader invalid/stale associative-result handling remain open. Stop at this usable
improvement for owner feedback and rotate the next item family.

Automated native GUI checks: `TestMeasurementContext`. They exercise circle-centre
versus edge-gap meaning, units, named operands, picked world points, occurrence
context, source movement, snapshot metadata, coordinate-edit Undo/Redo, save/reopen,
Cancel and geometric-centre density disclosure.
