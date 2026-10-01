# Ordered open-section Loft (F063)

Use the source-built FreeCAD Plus fork. In Part, choose **Loft** and add profiles
from the available list to **Sections in loft order**. The existing picker now
includes single open wires and single edges as well as closed profiles/vertices.
Duplicate labels remain separate entries; tooltips include internal names.

1. Prepare three open wires at different heights. Add them in sequence and use
   **Move up/down** to put the middle section between the first and last.
2. Turn **Create solid** off. Read the output/order message. Smooth interpolation
   and **Ruled surface** are native alternatives; **Closed** connects the last
   section back to the first and does not cap an open profile.
3. Click OK. A valid separate native associative Loft is created in one undo step.
   Inspect the surface, undo/redo, save and reopen. Edit the middle section and
   recompute; the surface should follow that section without changing other inputs.
4. Try the open profiles with **Create solid** enabled. Failure stays in the task,
   leaves no Loft or undo entry, and asks for correction. Turn solid off and retry.
5. With only one selected section, OK must stay open. Cancel must leave the
   document unchanged. Finish other edit transactions or recompute stale profiles
   before accepting. Missing/replaced profiles require reopening the collector.
6. Try three closed circular profiles with **Create solid** enabled; native solid
   loft creation still works. Existing document/property identities are retained.

This checkpoint provides ordered collection and native solid/surface output. It
does not add guide curves, correspondence handles, a geometric/twist preview,
continuity/tolerance certification, Boolean targets or section reversal controls.
Full F063 remains open. Stop at this usable workflow and rotate pending owner testing.

Run `TestLoftSections` and `TestSheetThickening` in the matching rebuilt GUI with
`tests` on `sys.path`. Roadmap 13.2a/b owns build and acceptance evidence.

Validated 2026-10-01: 17 distinct native GUI checks (eight Loft plus nine sheet
thickening). Both roadmap tasks preceded the grouped PartGui build; one corrective
incremental rebuild fixed a demonstrated misleading error detail. All eight Loft
checks pass again. Five final captures were reviewed.

Evidence: `D:\Temp\Office-PC\freecad-plus-loft-sections-20261001`. Open fixtures
from `visual-final`: `Open-Sections.FCStd`, `Associative-Loft.FCStd` and
`Edited-Loft.FCStd`. The latter retains the widened middle section and recomputed
surface. Use `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
This is source-built verification; installer and owner workflow acceptance remain
pending. Full F063 remains open for the capabilities listed above.
