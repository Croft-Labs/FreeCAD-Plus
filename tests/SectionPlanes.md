# Section planes: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Evidence: `D:\Temp\Office-PC\freecad-plus-sections-20260930`.
Existing installers do not include this batch.

1. Open `visual-accepted\Section-Housings.FCStd` and choose **View > Clipping View**.
   The fixture contains a housing in nested Parts and a second linked housing.
2. Enable Clipping Y and Z. Set Y to 15 mm and click its Flip button; set Z to 8 mm.
   Inspect the interiors. Offsets use world coordinates, not the housing's local frame.
3. Use **Save section planes...** to write a `.fcsection` preset. Close removes
   the clipping. Reopen the model, open Clipping View and load the preset: the two
   section planes and retained sides return. `visual-accepted\Housing-Section.fcsection`
   is a ready-made example. The preset does not save camera or visibility changes.
4. Enable the custom plane, which turns off the axis planes. Click View after
   changing camera orientation: the Direction fields now show its normal.
   Enter (1, 1, 0) for a diagonal section. A zero vector pauses custom clipping
   and explains how to recover; enter a nonzero vector to resume.
5. Enable Adjust to view direction and orbit. Direction fields track the displayed
   plane. Saving captures the current plane; loading deliberately turns camera
   following off so the saved section is reproducible.
6. Close the panel: all clipping disappears. The model, Body Tips, placements,
   Undo history and ordinary geometry exports remain unchanged. Save the model
   separately; section presets are not embedded in FCStd files.

Malformed, unsupported-version, invalid-normal or incompatible simultaneous-mode
presets leave all current planes unchanged. Failed writes report an inline error.
Loading a preset from another model deliberately uses the same world coordinates;
there are no object/occurrence references to remap.

Preset contract: UTF-8 JSON, `format=FreeCADPlus.SectionPlanes`, `version=1`,
`frame=world`, and four `planes` in X/Y/Z/custom order. Each contains boolean
`enabled`, unit vector `normal` and signed plane equation `offsetMm`. The first
three normals are signed axis unit vectors. Custom and axis modes are mutually
exclusive. The display uses native Coin single-precision clipping planes.
Unknown versions, oversized files (over 64 KiB) and malformed values are rejected.
Files carry no executable code, paths to other assets or model links.

For a clipped image capture, select the FramebufferObject image-saving backend.
The default image backend did not include clipping in this validation; this is a
capture-backend limitation, not a change to the preset or model export contract.

This is visual clipping, with no caps or extracted section curves. Model-based
measurements and manufacturing exports still use whole geometry. Whole F100 remains
open for embedded saved views, caps, section measurements and physical/high-DPI
acceptance. Stop here for owner feedback and rotate to another item family.
