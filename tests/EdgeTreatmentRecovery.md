# Fillet/chamfer recovery: owner workflow (F058)

Use this checkout's source-built executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD is unchanged.

1. In Part, create a 10 mm box. Select an edge and open **Fillet** or **Chamfer**.
2. Enter 100 mm and press OK. The operation should fail, keep the task open and
   retain the checked edges and sizes. The message identifies the attempted edge
   set and native error; it does not claim one edge is the proven cause.
3. Change the size to 1 mm and retry. A valid native feature should be created,
   with the source hidden. Undo restores the source; Redo restores the result.
4. Try a variable fillet (0.75 mm / 1.5 mm) or two-distance chamfer. Save and reopen
   the result and edit a source dimension to check the intended association.
5. Edit an existing treatment and force a failure. Its previous parameters and
   geometry should remain recoverable; Cancel exits. No checked edges requires
   no model transaction; a changed source requires a fresh edge review.

The task keeps its native collector and feature properties. Builders copy source
topology with element mappings before operating. There is no new live preview,
tangent-chain control, corner option or precise failing-edge classifier. General
topology repair and physical/high-DPI acceptance remain open; full F058 is not
complete. Stop at the usable recovery checkpoint and rotate pending owner feedback.

`TestEdgeTreatmentRecovery.py` covers failed creation/retry, source BRep retention,
Undo/Redo, empty/zero inputs, stale sources, variable fillet with downstream
save/reopen, two-distance chamfer, failed existing-feature edit/Cancel and entered
precision. Both tasks preceded one 70-second PartGui Release build (including Part),
exit 0. Evidence: `D:\Temp\Office-PC\freecad-plus-edge-treatment-20261001`.
All 16 distinct selected checks pass: eight recovery checks in `numeric-fixture/`
and eight unchanged Loft task regressions in `grouped/`. Initial fixtures used the
quantity property incorrectly; using its numeric rawValue corrected them without
an implementation change or second build. All accepted GUI processes exit 0.
Six captures in `visual/` were reviewed, with Recovered-Fillet.FCStd,
Variable-Fillet.FCStd and Two-Distance-Chamfer.FCStd for owner testing.
`evidence.json` records source/native hashes. No installer or release publication.
