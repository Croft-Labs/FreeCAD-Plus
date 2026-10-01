# Sampled face deviation: owner workflow test

This bounded F071 workflow adds **Part > Sampled face deviation...**. It compares
two explicit faces using native point-to-face distance and a temporary color map.
It creates no geometry, links, document properties, appearance edits or Undo entries.

Use this checkout's development build:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD and published installers are unchanged.

1. Open the Part workbench. Select a face on a root Part shape or root Body result,
   open the command, and click **Capture sampled face**. A whole single-face object
   is also accepted. Labels include object and face names.
2. Select the face to compare against and click **Capture reference face**. Both
   must belong to the same document. Selection changes alone do not change roles.
3. Choose **Samples per UV direction** (3-25, default 11) and **Full color scale**
   in millimeters (default 1). Click **Check and show map**.
4. Read usable, outside-trim and singular/failed counts, sample minimum/maximum/mean,
   and the number at or above the color scale. Blue means zero; yellow means half
   the scale; red means the scale or greater. The full numerical values remain in
   the report even when colors saturate. Markers draw on top of geometry.
5. Change sampling/scale or click **Clear map** to remove the old result. Recheck
   after changing settings. Model edits clear it too; recapture any face whose
   geometry or placement changed, then check again. No face-number rebinding is inferred.
6. **Save sampling settings** explicitly stores only grid and color scale for later
   sessions. References, reports and maps are not saved in the document. **Close**
   or closing the source document removes the map without model edits.

The check uses UV grid cell centers on the sampled face. Holes and other trimmed-out
locations are excluded using native face membership. Singular or failed samples
are counted separately and make the report incomplete. Distances are **unsigned
nearest distances to the finite reference face, including its boundary**, in world
millimeters. There is no best-fit alignment or projection along normals. Swapping
roles can change results. Statistics are not area weighted. Grid sampling can miss
narrow defects and boundary extrema; sample maximum is not the true maximum or a
tolerance certification. Colors cannot certify surface quality.

Current inputs: two faces on current, valid, root Part shapes or root Bodies.
Links, nested members, external documents and pending edit transactions are refused.
Zebra/reflection lines, curvature combs, join-continuity checks, bidirectional or
adaptive sampling, certified global deviation, report export, face-reference
persistence and physical/high-DPI acceptance remain open. Full F071 is not complete.

`TestSurfaceDeviation.py` covers planar and curved 2 mm offsets, transformed faces,
tilt and trimmed holes, one-way finite-face differences, injected native failures,
source isolation, settings, selection/transaction/stale-input guards, map cleanup,
native command activation and save/reopen.

Both tasks preceded one PartGui/PartScripts Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-surface-deviation-20261001`.
`grouped/` passes nine new deviation checks and seven existing interference checks:
**16 selected passes**, zero failures/errors/skips, native exit 0. Six `visual/`
captures were reviewed: known offset, tilted report/map, changed-face refusal,
reopened report and trimmed-hole report. Known-Offset.FCStd and Tilted-Surfaces.FCStd
are the owner fixtures. Planar and cylindrical fixtures report 2 mm; the tilted
11 x 11 grid reports 0.155463702-3.264737732 mm. The trimmed fixture excludes 25
of 121 UV centers and reports 96 usable samples. Native whole Body results,
world placement, one-way finite-face differences, incomplete native sampling,
source/Undo isolation, saved settings, transaction/stale/context guards, map cleanup,
command activation and save/reopen pass.
Part SHA256: `93D8BCB643EEB020AB1466333DEA84F14BA934C0EF00C2043566111E5AFC8C66`.
PartGui SHA256: `5025C3E75A2D150FEC54B939C6C5DD49510517FF2BCD8AB6C8255F4049BC995A`.
validated-identities.json and acceptance-summary.json identify source/runtime and
accepted evidence; the historical About stamp is not this source identity.
Original tracked newline conventions were restored after build without changing
compiled semantics; InitGui.py was restaged before native command capture.
No installer/release update. Whole F071/15.2 remains open for zebra/reflection lines,
curvature combs, continuity, broader subjects, adaptive/bidirectional or certified
global deviation, reference/report persistence and physical/high-DPI acceptance.
Stop at this functional checkpoint for owner feedback and rotate to another family.
