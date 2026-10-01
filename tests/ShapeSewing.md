# Shape Builder sewing: owner workflow test

This F068 increment extends **Part > Shape Builder**, using the existing
**Shell from faces** and **Solid from shell** modes. It is a bounded independent
snapshot workflow ready for owner feedback; whole F068 remains open.

Use this checkout's development build:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD and published installers are unchanged.

1. Select **Shell from faces**, then select adjacent faces from root Part shapes
   or a whole root Body result. **All faces** collects every face of the selected
   source objects. Links and nested Part/Body members are outside this pilot.
2. Enter **Sewing tolerance (mm)**, from 0.0000001 to 1 mm. The default is
   0.000001 mm. **Check shape** computes without creating a document object and
   reports open/closed shell or disconnected sheets, shell/face counts, free-edge
   names in the proposed result, requested tolerance and resulting maximum
   geometry tolerance. Source tolerances can already exceed the requested value.
3. Try the complete and gapped enclosure examples. At the default tolerance, the
   gapped example stays disconnected and lists free boundaries. Increase tolerance
   deliberately and check again. A larger tolerance can join or alter boundaries;
   it does not prove exact coincidence. No automatic tolerance escalation occurs.
4. **Create** makes a separate native Part feature. Sources remain visible and
   unchanged. The result records its creation tolerance and source-face names as
   read-only snapshot information. Source edits do not update the result.
5. Choose **Solid from shell**, then select the whole created shell and check it.
   Only a closed shell that produces one valid positive-volume solid may be
   created. Open-shell failure stays inline and preserves the selection and source.
   **Refine shape** uses the existing native refinement operation.
6. Close the task, Undo/Redo, save and reopen. **Close** leaves previously created
   results in the document; it is not rollback for this multi-create utility.
   Undo removes each accepted result. Checking and closing without Create adds
   nothing. Verify source edits leave the snapshot unchanged.

Known limits: 500 input faces; same-document root geometry only. Free boundaries
are counted/listed, not highlighted in the viewport. Check is a computed diagnostic,
not a ghost preview. Gap widths, nonmanifold localization, associative sources,
topology-stable repair, standalone macro replay, localization and physical/high-DPI acceptance
remain open. Source names are provenance text, not live links. Whole F068 remains
open; do not infer watertightness from shading or from a larger joining tolerance.

Automated checks are in `TestShapeSewing.py`: explicit native tolerance behavior,
non-finite rejection, enclosure/open/gap and curved-seam classification, independent
placement, source preservation, transaction/stale/nested-input refusal, native task
controls, failure recovery, Undo/Redo and save/reopen.


Recorded UI calls require the live Shape Builder and selection; standalone macro
replay is not supported by this increment. Direct ShapeSewing.review/create calls
accept explicit document/input lists for scripted use.

Both tasks preceded one PartGui/PartScripts Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-shape-sewing-20261001`.
Initial `grouped/` passed all 14 Trim Body checks and 6/8 sewing checks. Two test
expectations were corrected for native Part origin objects and the face-only
selection gate; no implementation rebuild. `sewing-verified/` passes all eight.
**22 distinct selected passes** across accepted suites, zero failures/errors/skips
in accepted suites, native process exits 0. Initial failed aggregate is retained.
Six reviewed `visual-settled/` captures and Sewing-Sources.FCStd / Sewing-Results.FCStd;
initial `visual/` captures caught native layout/radio animations before settling.
The 0.01 mm gapped enclosure stays disconnected at 1e-6 mm sewing tolerance;
explicit 0.05 mm joins it and reports 0.0105 mm maximum geometry tolerance. The
exact enclosure produces a valid 1000 mm^3 solid; the open shell is refused.
Part SHA256: `5DF2B65D6A4F06972AA7596371B7D777779D0AB11F86D29FA68A2C842725C128`.
PartGui SHA256: `7ACC4FBFDE731DA33A76528FC0373D16E563F2D7C01164AD8F5C6CEA0409CBE6`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted checks; historical About metadata is not this source identity.
No installer/release update. Root same-document inputs, 500 faces maximum.
Whole F068/13.1 stays open for associative links, graphical boundaries/preview,
gap-width measurement, broader nonmanifold/healing diagnostics, standalone macro
replay, localization and physical acceptance. Stop here for owner testing and rotate.
