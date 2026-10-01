# Shell Thickness: owner workflow (F059)

Use the source-built fork at
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.

1. In Part, create a box (for example 30 x 20 x 15 mm), select its top face,
   and start **Thickness**. The source identity and removed faces appear in the task.
2. Enter **-2 mm** for an inward shell. **Reverse side** changes the sign for an
   outward shell; formulas must be edited explicitly. Inspect the native preview.
3. Use **Removed faces** to review the current selection. Change the selected faces
   and press **Done**. Clearing the selection explicitly removes all openings.
4. Enter zero, or -10 mm on the 30 x 20 x 15 box, and press OK. The task stays open
   with a failure message. Correct the settings, or Cancel to restore the earlier
   model. Any displayed old geometry during failure is identified as stale.
5. Turn off **Update view**, change thickness, and inspect the pending message.
   OK recomputes before accepting. Check Undo/Redo, save/reopen, and a source edit.

This increment uses native Part::Thickness geometry, properties and face references.
It is a shell workflow checkpoint, not completion of Draft, Rib/Web, local thin-region
failure diagnosis or arbitrary geometry support. Physical/high-DPI acceptance awaits
owner testing. Stop for feedback and rotate once the bounded workflow is usable.

Known limit: an inward value of -25 mm on this box can be accepted by the native
kernel. This batch does not establish that arbitrary oversized offsets produce the
intended wall geometry. The verified -1/-2 mm enclosure and -10 mm collapse/recovery
cases are distinct from that unresolved limit.

Roadmap 13.5g/h records the 2026-10-01 checkpoint: two tasks batched before the
first build, one corrective status build, sixteen distinct passing checks and six
reviewed final captures. Undo/Redo, save/reopen and downstream source edits pass.

Owner fixtures and final captures:
`D:\Temp\Office-PC\freecad-plus-shell-thickness-20261001\visual-final`.
Open `Shell-Before.FCStd` to start, `Shell-After.FCStd` for the accepted enclosure,
or `Shell-Source-Edited.FCStd` for the recomputed larger enclosure. Build logs,
test results and the source/runtime hash manifest are in the parent folder.
