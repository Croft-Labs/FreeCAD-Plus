# Document updates: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Evidence: `D:\Temp\Office-PC\freecad-plus-document-updates-20261001`.
Existing installers do not contain this batch.

1. Open `visual\Update-Bracket.FCStd` and choose **Tools > Document updates**.
   The example contains a native box minus a bore and a linked occurrence.
2. Check **Defer normal document recomputes**. Change Blank.Length and Blank.Width
   in their native property editor. Cached geometry may remain visible. The panel
   lists pending objects and affected dependents; normal document recomputes are
   deferred. Some native edit previews can still update an active object.
3. Select an affected row and use **Select affected input** to locate its input,
   or **Select object** to locate the row itself. Visibility is unchanged. The input
   column reports a reachable pending/failed input, not a guaranteed unique cause.
4. Choose **Recompute now** to update this document once. Deferred mode stays on.
   Disable deferral to restore normal native recompute behavior. Disabling deferral
   alone does not update pending geometry; explicitly recompute when needed.
5. To try a failure, clear Bracket.Tool. Recompute and inspect Failed and affected
   rows. Restore Tool to Bore and recompute. The existing manufacturing STL handoff
   refuses pending/invalid inputs before repair and works after repair.
6. Undo/Redo a dimension edit, recomputing afterward as needed. The inspector adds
   no extra model transaction and does not clear the redo history. Finish an active
   task or pending edit transaction before changing mode or explicitly updating.
7. Close retains the chosen session mode. Save after recomputing, close and reopen:
   geometry and links persist; the native deferred flag is not a saved model property.

`visual\Update-Bracket-Repaired.FCStd` contains the repaired, updated example.
The view uses native object status and dependency links, including loaded external
inputs, bounded to 2000 objects. It never clears error/dirty flags or changes model
visibility. Whole-document recompute uses the existing native engine with cycle
checking and an explicit bypass of deferral for that update only. It does not own an
external document's update policy; repair/recompute loaded external inputs there.

F087/F088 remain open for first-cause classification across all workbenches, targeted
dependency recompute, asynchronous progress/cancellation, unloaded-reference diagnosis,
and physical/high-DPI acceptance. No claim is made that an empty status list proves
asynchronous drawing/render/analysis completion or that all exporters reject stale
data. The manufacturing STL handoff is the downstream gate exercised here.
Stop here for owner feedback before broadening this workflow.
