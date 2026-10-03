# Unified component Loft acceptance

REQ-014b and UI-003b govern this component workflow. `TestComponentLoft.py`
uses the real native AdditiveLoft/SubtractiveLoft engines and checks matching
runtime module hashes. Use `RunComponentDocument.ps1` with an isolated fork
candidate and an external evidence directory, without source overlays.

The eight Python/runtime cases cover additive/subtractive geometry and overlay
volumes; nonmutating previews; mode changes with stable result/operation identities;
downstream geometry, undo/redo and `.cadprt` reopening; selected-curve association,
reorder and upstream recompute; invalid-edit rollback and cyclic targets; empty-task
recovery, preselection, History editing, preview colors and Cancel restoration;
placed sections and vertex tips; closed native lofts and expression protection.
The ninth case, `testNativeCommandRouting`, requires the rebuilt PartDesignGui.

For the grouped build, run all nine tests without a filter. Also run
`TestComponentRevolve.testTaskSectionsPreviewAndEdit` and
`testPreviewColorsVisibilityAndCancel`, plus `TestPlusRibbon`'s
`testCompactPrimaryAndSecondaryGrid` and `testExactOwnerDesignModelingLayout`.
Pass each file's TestNames separately: the runner applies one filter to every file.

Owner acceptance: open Loft with no selected profiles, then append two placed
sketches or closed curve subsets. Inspect/reorder/replace/remove sections. Exercise
New Body, Add and Subtract with explicit targets, Smooth/Ruled and Closed where
geometrically suitable. Confirm Advanced starts collapsed, target hides for New
Body, Overlay defaults to blue/green/red, None removes it, Final Result hides the
previous display, and Cancel restores it. Reopen through History and save/reopen
the document. Check pointer picking and high-DPI layout separately from scripted
Qt evidence. Implementation/build/delivery status belongs to the roadmap and WORK_STATE.
