# Entity selection filters: owner workflow (F035)

Use this checkout's source-built executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD has not been changed.

1. Open a model with overlapping solids or repeated linked components. Clear any
   existing selection, then use **View > Visibility > Selection filters**.
2. Choose **Faces only**. Pick a face or invoke native **Clarify Selection**.
   Face candidates remain eligible; whole-object candidates are excluded. Existing
   selections are deliberately retained when the filter changes.
3. Try **Vertices only**, **Edges only** and **Whole objects only**. Whole objects
   includes bodies, components, sketches and features together; separate filters
   for these types are not implemented in this bounded increment.
4. Enter a native command with its own selection restrictions. Both policies
   apply. If their intersection is empty, use the status-bar **Pick filter … Reset**
   button. Reset does not remove the command's own gate. Leaving a command retains
   the filter selected in this modeless window.
5. Use **Reset to all**, **Close** or **Escape** to restore All entities. Restarting
   the application also starts unrestricted. No filter is stored in the model.

The filter affects new native picks; it does not purge existing selections, change
visibility or modify geometry/Undo. The modeless window remains available during
commands. Select Other keeps native document/root/occurrence/element identity.
Dedicated sketch-edit, tree/window picking, subtype filters, combinations and
physical/high-DPI navigation acceptance remain open. Full F035 is not complete.

`TestEntitySelectionFilter.py` checks native entity acceptance, command-gate
intersection and retention, nested repeated links, unchanged existing selection /
geometry / Undo, modeling-menu discovery, visible reset, Escape/Close/startup reset and native ray-menu
eligibility including a filter changed while its menu is open.

Both tasks preceded one FreeCADGui/FreeCADGui_Resources Release build (exit 0),
followed by one short corrective build to register the command before standard
workbench initialization. Evidence:
`D:\Temp\Office-PC\freecad-plus-entity-filter-20261001`.
All 17 distinct selected checks pass: ten in `final-verified/` plus seven unchanged
native Select Other regressions in `grouped/`. Initial test fixtures were corrected
to use viewport hover mode and the modeling workbench (NoneWorkbench has no
Visibility menu); these corrections required no implementation change or rebuild.
Five captures in `visual/` were reviewed; use `visual/Repeated-Components.FCStd`
as a starting model. `evidence.json` records the capture and final runtime identities.
No installer or release publication. Ready for owner testing, not full-specification
completion; rotate pending workflow feedback.
