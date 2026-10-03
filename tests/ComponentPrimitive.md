# Unified component Primitive acceptance

REQ-014e/UI-003e apply the owner template to the eight native additive/subtractive
primitive pairs. Run `TestComponentPrimitive.py` with `RunComponentDocument.ps1`,
an isolated fork candidate, external evidence and `FREECAD_PLUS_PROFILE_SOURCE=0`.
Command routing requires the rebuilt PartDesignGui. Module hashes must match source.

The seven cases cover all eight shapes in New Body/Add/Subtract/Common, native
dimensions, placed/rotated geometry, transient preview parity, native command aliases,
type/mode replacement with stable operation/result IDs and downstream consumers,
undo/redo, property recompute and `.cadprt` save/reopen. Attachment coverage includes
datum placement changes, native offsets/reversal, type replacement, origin selection
and task reopen. Invalid edits roll back; cyclic targets and expressions are protected.
The task checks four section defaults, all shape fields, History routing, blue/green/red
preview policy, Final Result, failed-OK recovery and Cancel visibility restoration.

Native ellipsoid B-spline Boolean/refinement volumes differ from independent
`Part.fuse/cut` integration. Compare these against directly configured native
Classic primitive features, with exact preview/accepted-shape parity; do not change
the geometry engine or relax all solid checks. Other shapes also compare against
independent Part Boolean results. Run inherited `PartDesignTests/TestPrimitive.py`.

Owner procedure: use either Primitive or a shape in Primitives, switch shapes and
operations, specify a target, and adjust native dimensions. In Advanced select
ordered local references and a native attachment mode, edit placement/offset and
orientation, then compare Overlay/Final Result. Accept, reopen via History, switch
shape or Add/Subtract, undo/redo, edit the support and save/reopen. Confirm Classic
documents still use native Body tasks. Physical pointer and high-DPI acceptance
remain separate from scripted Qt captures. Tab remains disabled because no native
Tab primitive exists. WORK_STATE and the roadmap own build/delivery status.
