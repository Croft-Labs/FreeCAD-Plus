# Contextual Constraint Palette acceptance

Run `test_tooltip_disappears_before_constraint_execution` for the October 6
lingering gray-frame regression. A real native tooltip and Qt button click must
prove the tooltip is already hidden on entry to the actual constraint backend,
without a sleep/event-loop settling allowance. Retired buttons are hidden before
deferred deletion. Check persistent selection on/off, immediate close and Undo;
retain `test_viewport_clamp_and_corridor_grace` for the separate one-second grace.

October 6 point-click regressions: run native
`test_plain_point_click_replaces_and_modifiers_extend` and
`test_candidate_point_constraints_do_not_log_errors`. They reproduce both reported
defects on the preceding Modeling payload. Check real sequential point clicks,
repeat click, Ctrl/Shift multiselection, Shift empty-click retention and plain
empty-click clearing without geometry/constraint/Undo changes. Capture the native
ReportOutput while probing a hypothetical collapsed line; it must be quiet.
An actual invalid constraint must still produce normal live-solver diagnostics.
Build these C++ changes together; older binaries are reproduction evidence only.
Also run `test_point_drag_undo_and_save_reopen`: real native press/move/release
must move the endpoint without adding a constraint; Undo/Redo and FCStd save/reopen
must retain its geometry and Sketch identity.

Run `TestConstraintPalette` in the Plus GUI runtime; after the grouped native build
run `TestConstraintPaletteNative` as well. The native class requires the new cloned
solver diagnostic and single-solve driving batch APIs; do not count an older payload
with Python overlays as verification of those methods.

Quick checks use real Sketcher geometry, constraints, native transactions and Qt:
Equal then Construction, mixed construction normal-first, persistent on/off,
failed input retention, dimension conversion in one Undo step, expression protection,
committed invalid Make Driving with Undo, save/reopen, structural action eligibility,
disabled tooltips with no mutation, viewport clamping, corridor and timer cancellation.
The viewport test uses Qt mouse events for click/open, Escape, empty space and drag.

Palette buttons use the corresponding native QAction icon and exact rich tooltip,
including translated descriptions/shortcuts; native changes refresh their
presentation. They remain icon-only and keep accessible action names, including
distinct Make Driving/Make Reference names with the existing batch behavior.
Disabled reasons are shown in the status bar on hover and remain accessible
descriptions while the tooltip matches the native toolbar. The presentation
test covers every action mapping, exact icon/tooltip parity, actual tooltip and
Equal-button events, persistence, Undo and narrow viewport wrapping.

Native diagnostic acceptance must compare geometry, constraints, document UndoCount
and solver state before/after repeated hover/update. Test indirect Equal redundancy,
conflicting dimensions and external-geometry safeguards. Failed batch API validation
must leave every selected dimension unchanged; solver failure must retain all driving
conversions and their values/identities as one undoable action.

Prompt 10 additionally covers real pointer travel at viewport corners and multiple
DPI settings; multiselection and connected-curve expansion; palette action updates
without jumping; no palette on box selection; undo/redo while visible; task/sketch
exit, document close and deletion; actual native dimension command dialogs; save and
reopen after an intentionally invalid conversion. No separate repair workflow is added.
