# Sketch Trim gestures: owner workflow (F050)

Use this checkout's source-built executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD is unchanged.

1. Edit a sketch containing several lines crossing two boundary lines. Activate
   the existing **Trim** tool and leave Include axes off unless needed.
2. Hold the left button and drag over several segments between the boundaries.
   The tool notice counts trims. Release to keep the whole gesture.
3. Undo once: the entire gesture should be restored. Redo should reproduce it.
   A separate completed drag creates another Undo step.
4. Begin another drag, then press Escape before releasing. Only that unfinished
   gesture should roll back. Leaving sketch edit also cancels an unfinished drag.
5. Inspect the completed notice for native removed/replaced-constraint identifiers. These
   are the identities reported by the sketch constraint system. A named constraint
   can remain on a new native identity. This is not a prediction
   that every remaining relation kept exactly its previous meaning.

Existing trim boundary markers, axes policy and geometry/constraint behavior remain
native. This increment does not add an extension boundary picker, new geometric
removal preview or general curve certification. Full F050 and physical/high-DPI
workflow acceptance remain open. Stop for owner feedback and rotate after the
bounded functional checkpoint.

`TestTrimGesture.py` drives viewport mouse events for multi-edge drag, Undo/Redo,
single click, removed/replaced constraints, empty drag, Escape and edit-exit rollback.
Roadmap 11.6e/f records the 2026-10-01 checkpoint: two tasks batched before the
initial build, one corrective notice build, twelve distinct passing checks and five
reviewed final captures. Save/reopen and named-constraint restoration on Undo pass.
Kernel-exception rollback has not been fault-injected; owner acceptance is pending.

Ready-to-open fixtures and final captures:
`D:\Temp\Office-PC\freecad-plus-trim-gesture-20261001\visual-final`.
Open `Trim-Gesture-Before.FCStd` to try the workflow, or
`Trim-Gesture-After.FCStd` to inspect the saved result. The parent evidence folder
contains build logs, grouped test results and the source/runtime hash manifest.
