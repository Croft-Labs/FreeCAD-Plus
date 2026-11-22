# Approved view fitting after sketch exit

`approval.json` records the owner request, chat approval and direct native preview
provenance. The preview kept a large rectangle clipped after restoring a 40 mm
camera height; native fitAll included all four corners with the same orientation.

The implementation queues fitting after native sketch exit, camera restoration,
coordinate restoration and task cleanup. It checks the originating view/context and
sketch identity. New tasks invalidate pending fits; empty/deleted geometry and
document/view/panel closure skip fitting. No visibility, geometry, constraint,
preference, selection or Undo mutation implements the camera adjustment.

`build-regression.txt` records seven passing focused native tests. They cover native
Close, exit command and resetEdit; restored top/axonometric orientation; other visible
solids and full sketch corners in view; selection/visibility/dirty/Undo preservation;
new sketch Undo/Redo; cancelled placement and empty sketch; a replacement editor;
deleted sketch/document; Body-owned sketch; and an external source in its host view.
Native near/far clipping distances may change as Coin evaluates the scene; cancelled
placement checks the camera position and zoom rather than those clipping distances.

The installed suite uses those cases plus coordinate visibility, dimensions, tabs,
Extrude, planes, shared eyes, component visibility, Move and Rotate regressions.
All 169 installed tests passed (`regression.json` and `regression.txt`).
`visual.FCMacro` creates a large native rectangle and clicks the actual Close button;
it checks full corner containment and captures editing and exit. `reopen.FCMacro`
opens the saved sketch in a fresh installed process, edits/exits in an axonometric
view, and verifies identity, constraints, framing, orientation, tabs and coordinates.
Neither script injects preview or replacement product code.

`run-validation.py` bounds native processes and uses isolated settings. `install.py`
retains rollback files and checks source/build/app hashes. The existing desktop
shortcut is launched by `restart-shortcut.ps1` with explicit isolated settings and
verified by `shortcut.FCMacro`. `cleanup.ps1` validates absolute target containment
and rejects reparse points before removing only disposable fixtures/inactive profiles.
Rollback copies, active shortcut profile and durable evidence remain retained.
