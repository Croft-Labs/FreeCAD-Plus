# Occurrence appearance: owner workflow test

Select one whole native Link object in the tree, then choose
**View > Occurrence appearance...**. Ctrl+K also finds the command.
Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Published installers and the separately installed FreeCAD do not contain this batch.

Evidence and the native example are under
`D:\Temp\Office-PC\freecad-plus-occurrence-appearance-20260930`.

1. Open `visual\Occurrence-Appearance.FCStd`. Three occurrences share one bracket
   shape inside a rotated Part. The source is hidden; all three links are visible.
2. Select **OccurrenceA** and open the editor. Verify its explicit occurrence and
   shared-source identities. Choose Override source appearance, a colour and a
   transparency percentage. The model remains unchanged until Apply.
3. Apply. Only OccurrenceA changes appearance. Its source, other occurrences,
   geometry and placement stay unchanged. Close keeps an already applied change.
4. Undo/Redo and save/reopen. The occurrence override survives persistence and
   remains independent. Edit the shared source dimensions: all occurrences still
   share the same geometry definition.
5. Reopen the editor, click **Use source appearance**, then Apply. This disables
   the native override and restores inheritance. Change the source appearance:
   inherited occurrences follow it. Reset does not change occurrence visibility.
6. Toggle Visible, then Apply. Visibility hides/shows this occurrence only; it does
   not suppress geometry, remove BOM participation or alter other instances.
7. Stage changes, then Close without applying. The staged values are discarded.
   Reload current values deliberately discards the staged form and reads native state.
8. Change the link target or appearance outside the open editor, then Apply: a
   stale-state message requires Reload. Deleting the source disables Apply until
   the link is repaired and reloaded; deleting the occurrence or closing its document
   closes the editor.

This pilot edits native Visibility, OverrideMaterial and ShapeAppearance in one
undoable transaction. Colour/transparency affect display, not engineering material,
mass or FEM. Uniform overrides apply to all faces. Reset turns off OverrideMaterial;
it does not copy source appearance into a disconnected value. Existing local
placement and source geometry are preserved; the editor adds no document properties.

Supported scope is a direct whole App::Link to a Part shape or Body in the same
document. Structural Part container paths are supported; selection through another
Link is rejected. Arrays, per-element overrides, linked subelements/nested occurrence paths,
external documents and mixed Part definitions are outside this pilot. A caller's
pending transaction or active task must finish before Apply. Colour uses RGB;
transparency ranges from 0 to 100 percent.

`TestOccurrenceAppearance` covers the installed menu, staging/Close, native
Apply/Undo/Redo/save/reopen, source/other-link isolation, placement, inheritance reset,
stale state, scope guards, Body Tip and editor lifecycle. Physical picking/high-DPI,
broader nested/material/representation overrides and full F018 acceptance remain open.
Stop here for owner feedback before expanding occurrence controls.
