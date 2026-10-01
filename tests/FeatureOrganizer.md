# Find and describe features: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Evidence: `D:\Temp\Office-PC\freecad-plus-feature-organization-20260930`.
Existing installers do not include this batch.

1. Open `visual\Feature-Notes.FCStd`. The native Stock and Drill create a Mounting
   hole result, reused by SecondBracket. Drill radius depends on Stock.Width.
2. Choose **Tools > Find and describe features**. The heading identifies the document.
   Search `M4 manufacture`: both words match the Mounting hole description, even
   though neither is in its label. Search is case-insensitive across label, internal
   name, native type and description. Words must all match somewhere in those fields.
3. Clear search and choose Part::Cylinder in the type filter. Only Drill remains.
   Sorting columns changes this list, never document ownership or feature order.
   Select a row, then **Select in model** to navigate; hidden inputs stay hidden.
4. Select Mounting hole. Change its label and enter a multiline description, then
   **Apply metadata**. Both fields save in one Undo step using native Label/Label2.
   Internal names, expressions, references and geometry remain intact. Undo/Redo
   restores/reapplies both fields. Unchanged Apply creates no Undo step.
5. Search for a word in the new description. Save/reopen and repeat the search.
   Changing Stock.Width to 25 mm still updates Drill radius to 2.5 mm, the hole
   geometry and the shared SecondBracket occurrence.
6. Add a note to SecondBracket: its source's label/description stay unchanged.
   Close after typing without Apply: unapplied text is discarded; earlier Apply
   operations remain. Changing rows, search/type filters or Refresh also discards
   unapplied text. There is no geometry preview.
7. An external model edit clears the stale list and disables editing until Refresh.
   Pending document transactions, active tasks, read-only metadata, empty labels
   and deleted/replaced inputs reject Apply with guidance. Return to this document
   before applying or changing model selection. Closing its document closes the editor.

Search is limited to the first 2000 loaded objects of this document, with an explicit
partial-search notice when capped. It does not open external documents or search
unloaded definitions. Links carry their own native metadata; editing a link here does
not edit its shared source. The native Label2 description remains accessible through
FreeCAD's existing description support. No new persistent schema is introduced.

Whole F014 remains open for folders, bulk organization, navigator integration and
physical/high-DPI acceptance. Stop here for workflow feedback and rotate.
