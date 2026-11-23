# Revolve Solid/Sheet preview — November 23, 2026

Owner requested the same Solid/Sheet workflow as Extrude: Solid selected by default,
Sheet automatically selecting and locking New. Native proposal shows Solid/Sheet
on the left and New/Add/Subtract on the right. Sheet disables all three operation
buttons and removes the target; Solid re-enables them with New still selected.
Axis selection, angular start offset and rotation-angle controls remain in place.

Direct screenshots: [Solid default](solid-operation.png),
[Sheet with New locked](sheet-operation.png), [Revolve task](sheet-task.png),
[270-degree sheet illustration](sheet-viewport.png), [before](before.png).
Native Qt assertions verify the default, Add-to-Sheet switch, locked New and return
to Solid. The native geometry fixture revolves a 15 mm line at radius 10 mm through
270 degrees, yielding one valid face, zero solids and 706.858347 mm² area. This is
illustrative fixture geometry, not production Sheet Revolve; OK is disabled in the
prototype. The owner approved this preview and requested implementation. See
[production acceptance](../revolve-sheet-20261123/README.md) separately.

Implementation should share the Extrude output controls without changing its
behavior, persist Revolve output, default legacy Revolves to Solid and use native
uncapped edge/wire rotation for Sheet. Keep creation/edit identity, profile/axis
references, strict history, Undo/Redo and task visibility. Apply compatible angle,
reverse, symmetric/two-side and reference controls; report unsupported/degenerate
geometry clearly. Validate open and closed curves, full and partial rotation,
mode switching, save/reopen/recompute and Solid Extrude/Revolve regressions.

Companion session cb60cf0ed06c, minimal adapter baseline
c4bd6215b9e9efc1fcd8bc261156a2a0703aeb9c against installed 5d5dd45910.
Only revolve_output.py changes in the candidate. Fingerprint
5a6bd556b4a844cc7f4bb0adceb6581821d516cff91f39fb2b88457605985d80,
capture fresh with no scope violations. Tool approval state is untouched.
Isolated native profiles and synthetic documents only. Generated native fixtures
are removed after archiving; the companion source/capture remain for review.
Production implementation and owner settings remain unchanged.
