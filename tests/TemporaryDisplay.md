# Temporary isolate/hide: owner workflow test

The F040 pilot adds four commands under **View > Visibility**:

- **Temporarily isolate selection** shows the selection and its containing Parts.
- **Temporarily hide selection** hides the selected objects.
- **Restore previous display** returns one temporary display level.
- **Restore original display** returns to the display before all temporary actions.

Use this checkout's development launcher:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD and previous installers do not contain this batch.
Commands are also available through **Ctrl+K** by searching their displayed names;
no extra default shortcuts replace existing assignments.

1. Open the example `visual\Temporary-Display.FCStd` under
   `D:\Temp\Office-PC\freecad-plus-temporary-display-20260930`.
2. Select **Component**, then **Temporarily isolate selection**. Other should
   disappear; Component's Box and Body remain visible. Hidden should stay hidden.
3. Select **Body**, then **Temporarily hide selection**. Restore previous display
   once to show Body again while keeping the isolation, then again to recover the
   original display. Alternatively Restore original display returns in one action.
4. Isolate Component, then isolate its Box. Restore levels in reverse order.
   Ordinary Space/Hide changes made during inspection are also reset to the snapshot
   when that level is restored.
5. Select a face inside **Occurrence**, then isolate it. This pilot isolates the
   **whole occurrence**, keeping its source's internal visibility and placement.
   Selecting a feature inside a Body addresses the whole current Body result,
   without showing intermediate history features or changing the Body Tip.
6. Create another object while isolated, then restore. The new object's current
   visibility is retained. A deleted object is ignored; a new object reusing its
   name does not inherit the deleted object's snapshot. Each open document has
   its own restore stack; closing a document discards that stack.
7. Restore before saving, then reopen and verify the recovered display and model.
   The session restore stack is not serialized. Saving while isolated stores the
   current native visibility; reopen cannot recover an unsaved earlier snapshot.

An empty/foreign selection, active task or pending edit is rejected without changing
the display. A no-op does not add a restore level. The status bar confirms the level
count; Restore actions remain enabled while levels exist in the active document.
Temporary display changes only native visibility, not suppression, feature inputs,
Body Tips, link targets or modeling geometry. It may mark the document modified,
as ordinary visibility changes do. It is separate from model Undo/Redo.

Stop here for owner feedback on names, discoverability and restore behavior. Whole
F040 remains open for individual members inside linked occurrences, save-time
temporary-display policy and physical/high-DPI workflow acceptance.

Automated acceptance: `TestTemporaryDisplay` exercises native menu commands,
nested isolate/hide/restore, whole Body/link selection, hidden-source preservation,
created/deleted/reused identities, document cleanup, invalid contexts, model Undo/Redo
and restored save/reopen. Evidence and selected results are recorded in roadmap 10.5a/b.
