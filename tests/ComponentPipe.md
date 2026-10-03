# Unified component Pipe acceptance

REQ-014c/UI-003c apply the owner's shared operation template to native Pipe.
`TestComponentPipe.py` uses actual AdditivePipe/SubtractivePipe geometry and verifies
runtime source hashes. Run with `RunComponentDocument.ps1`, an isolated fork
candidate, external evidence directory and `FREECAD_PLUS_PROFILE_SOURCE=0`.

Seven compatible cases cover New Body/Add/Subtract/Common, nonmutating final and
volume previews, stable mode-edit identities and downstream consumers, undo/redo,
path recompute and `.cadprt` reopening; all five orientations and three native
corner transitions; selected path edges, Constant/Multisection retention, selected
profile curves and upstream sketch recompute; rollback, cyclic targets, expressions
and unsupported inputs; task defaults, preselection, collectors, History editing,
preview colors, failed-OK recovery and Cancel visibility restoration.

The native Auxiliary algorithm approximates the circular sweep; its straight-path
analytic-volume check allows 0.05 cubic mm for a roughly 31.4 cubic mm fixture,
while preview/committed native volumes must match closely. The Transformed corner
mode has different volume semantics from Right/Round corner; require valid native
results spanning both legs, rather than imposing a different sweep algorithm.
Point-ended sections and unfinished scaling laws are rejected with clear messages.

The eighth case, `testNativeCommandRouting`, requires rebuilt PartDesignGui. At the
grouped build run the full Pipe and Loft files without filters. For shared-code
regressions, run all eight compatible Loft cases plus the ribbon tests
`testCompactPrimaryAndSecondaryGrid` and `testExactOwnerDesignModelingLayout`.
Supply per-file TestNames separately; one filter otherwise applies to every file.

Owner acceptance: launch Pipe empty; collect a profile and sweep path, switch
between profile/path/auxiliary picking, add/remove/clear edges and reorder sections.
Try explicit targets for Add/Subtract, Common, Constant/Multisection, all orientation
and corner modes, and recover after invalid inputs. Confirm the four collapsible
sections and default Overlay, blue/green/red colors, None, Final Result and Cancel.
Edit through History, change an upstream path and save/reopen. Physical pointer and
high-DPI checks remain separate from scripted Qt tests and task captures. The
roadmap and WORK_STATE record native build, owner shortcut delivery and evidence.
