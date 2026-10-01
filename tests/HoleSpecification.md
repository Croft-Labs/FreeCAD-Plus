# Hole specification review (F055)

Use the source-built fork's native Part Design Hole task.

1. Make a Body with a block and a position sketch containing two circles. Add a
   construction circle too. Create Hole and inspect the profile/Body identities.
   The native location count excludes construction circles; it is not a count of
   successful target intersections.
2. Use a plain diameter and counterbore; review the live result and accept. Undo
   should restore the native feature and its links. Redo has a recorded mismatch
   below and is not accepted.
3. Choose ISO metric and a size. Compare Clearance, Tap-drill and Threaded.
   Threaded without Model thread uses cosmetic representation, not helical solid
   geometry. Enable Model thread to request actual geometry; the summary explains
   the cost. When Update View is off, the location review must say pending.
4. Cancel the pending modeled-thread edit. Deferred acceptance is currently an
   open blocker; avoid that path during this bounded review. On a plain-hole edit,
   try zero depth and Cancel; the prior committed shape and parameters must return.
5. Reopen a saved cosmetic-thread feature, edit its location sketch, recompute,
   and check that the Hole and a downstream Body Link update together.

These are native Hole controls and properties. The review does not save, solve or
change geometry. Full F055 remains open for broader guided placement, versioned
standard-table provenance, drawing callouts and physical owner acceptance.

## Recorded checkpoint and open gates (2026-10-01)

Both implementation tasks preceded one 120-second PartDesignGui build (exit 0).
Seven bounded review checks plus ten unchanged native Hole checks pass. **13.5d
is still open**, with the failing/waiting evidence retained separately:

- With ISO metric M6x1.0, Threaded and Model thread enabled, Update View off,
  task acceptance waited without returning. A probe with the new review timer
  disabled also timed out. Native recompute of the same thread without the task
  produced a valid 96-face result; it does not prove the task works.
- For two diameter-4, depth-10 holes with diameter-8, depth-2 counterbores in a
  30 x 20 x 10 block, create and Undo pass. Redo after recompute returned
  5607.527112972334 mm3 instead of 5597.876140340506 mm3.

Evidence: `D:\Temp\Office-PC\freecad-plus-hole-specification-20261001`.
`review-accepted/` contains the passing bounded checks; `hole-final/` retains the
Redo mismatch. The task-wait and standalone probe folders retain distinct evidence.
Do not expand this batch into repeated diagnosis; rotate pending owner feedback.

Six captures were reviewed in `visual/`. Owner fixtures there include
`Plain-Holes.FCStd`, `Counterbore-Holes.FCStd`, and `Cosmetic-Holes.FCStd`.
`Native-Modeled-Probe.FCStd` is a separate geometry probe made without task
acceptance. The counterbore capture retains an inherited numeric-control display
mismatch after an API edit; physical numeric entry remains unverified.
Source/runtime hashes and publication details are recorded in `evidence.json`.
