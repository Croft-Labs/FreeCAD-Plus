# Sketch constraint repair: owner workflow test

This bounded F048 workflow adds **Sketch > Review constraint repair...** in the
Sketcher workbench. It diagnoses a temporary native copy, previews deliberate
deactivation, and applies a successful choice in one native Undo transaction.

Use this checkout's development build:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD and published installers are unchanged.

1. Leave sketch edit mode, select one whole free root sketch in the tree, and open
   the command. Conflicting/invalid sketch results are allowed: the review solves
   copied authored geometry and constraints rather than trusting an old Shape.
2. Read the native solver state. The table lists constraint number/name, type,
   dimensional value with units, active/reference state, native diagnostic group
   and involved geometry. Solver groups are candidate sets, not a unique cause.
3. Select a row and click **Select row geometry** to select its internal edges
   through the existing selection service. Axes/origin-only relations have no
   internal edge to select. This deliberate action changes selection only.
4. Check exactly the active constraints you want to deactivate. None are checked
   automatically; already inactive constraints cannot be chosen again.
5. Click **Preview deactivation**. The temporary native sketch reports the resulting
   solve state and degrees of freedom; a successful result has an automatically framed
   view-only wireframe.
   A remaining conflict/redundancy/failure disables Apply. A freedom count describes
   the solve, not every possible coupled movement. Source geometry stays unchanged.
6. **Apply deactivation** rechecks the source and proposal, deactivates only the
   checked constraints, solves and recomputes, and creates one Undo step. Constraint
   numbers, names and values are retained. No automatic deletion or substitution
   occurs. Existing downstream consumers recompute from the repaired sketch.
7. Undo/Redo, save/reopen, and edit a surviving driving dimension. The model should
   follow the remaining constraints. Native constraint activation remains available
   for later re-enabling a retained constraint; that may recreate the original issue.
8. **Cancel** removes the preview without changing the sketch. Editing the source
   invalidates the preview and requires **Review again**, which clears repair choices.
   Closing the document also closes the dialog and removes the overlay.

Scope: one free root Sketcher::SketchObject, 1-200 geometry elements and 1-400
constraints. Body/Part/occurrence members, attachment/external geometry, expressions,
other linked inputs and active edit/task/transaction contexts are refused. Preview
uses a hidden temporary document, closed on success or failure; it creates no source
objects, source Undo entries or saved copies. Apply updates native downstream objects;
the preview covers the sketch, not a geometric preview of every consumer.

Constraint replacement, automatic minimal repair, externally driven/attached and
in-Body workflows, movement-direction diagnosis, macro recording, localization and
physical/high-DPI acceptance remain open. Full F048 is not claimed complete.

`TestConstraintRepair.py` covers isolated native diagnostics/preview, explicit
choices, retained identity, rollback, owner-context/stale guards, UI Cancel/Apply,
Undo/Redo, save/reopen and downstream extrusion.

Both implementation tasks preceded one SketcherGui/SketcherScripts Release build,
exit 0. Evidence: `D:\Temp\Office-PC\freecad-plus-constraint-repair-20261001`.
`grouped/` passes eight repair checks and seven existing sketch-reuse checks. A final
UI correction frames the temporary overlay automatically because native Fit All
excludes it; only ConstraintRepairGui.py was restaged, without a second native build.
`repair-verified/` passes all eight repair checks, including a 10,000 mm off-origin
preview. **15 distinct selected passes**, zero failures/errors/skips in accepted
suites, native exits 0. Six final `visual-accepted/` captures were reviewed: redundant
and conflicting diagnoses, failed choice, successful proposal, preview wireframe
and reopened inactive constraint. Earlier `visual/` used harness framing and is
retained separately. Constraint-Repair-Source.FCStd / Constraint-Repair-Result.FCStd
are owner fixtures; the unselected redundant profile intentionally remains unrepaired.
Native diagnostics distinguish equal-radius redundancy from unequal-radius conflict.
Preview preserves source content, constraints, object count, Undo and active document.
Choice/Cancel, retained dimension identity/values, transaction/stale guards, rollback,
Undo/Redo and save/reopen pass. A repaired radius-5 profile extrudes 4 mm to 100*pi
mm^3; changing the surviving radius to 6 after reopen updates it to 144*pi mm^3.
Sketcher SHA256: `0525D3CA7E6DB90B2830C504F9BC99DB1A092D6D72268E5A18D70C15F2EED0D6`.
SketcherGui SHA256: `1B375C675DBABA3373565643D0D493CA9E8EA58CE9A4E3FC09A09DF17D11E5D4`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted evidence; the historical About stamp is not this source identity.
No installer/release update. Full F048/11.4 remains open for Body/attached/external
and expression-driven sketches, constraint replacement, consumer-wide previews,
movement-direction diagnosis, macro recording, localization and physical acceptance.
Stop here for owner workflow testing and rotate to another item family.
