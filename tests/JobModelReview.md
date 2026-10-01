# CAM model setup review (F090)

Use the source-built FreeCAD Plus fork, CAM > New Job. This bounded workflow
reviews model identity and size before the native Job setup opens.

1. Select a solid or mesh and open New Job. Check the selected model and count.
   With duplicate labels enabled in document preferences, give two models the same
   label and select only one: only that object should be
   preselected. Hover over a candidate for its internal name.
2. Inspect the Model review: type, count, X/Y/Z dimensions and minimum coordinates
   in mm. Mesh candidates appear under Meshes. These are source bounds including
   source placement, before final job setup; enclosing-parent/world/WCS bounds are
   not claimed. STL has no declared units: compare these dimensions with the part.
3. Change the Document Units selection. Dimensions in this review stay in mm;
   this does not scale the model. Cancel must preserve the model and document units.
4. Click OK, then use the native Job task to inspect orientation/work origin,
   stock, tools, operation strategy and postprocessor. This review does not create
   toolpaths or establish machining suitability.
5. In an existing job's Model Selection, verify repeated-source counts remain
   correct even when another source has the same label. Accept or Cancel normally.
6. Recompute stale source edits before proceeding. If a source changes while the
   picker is open, OK presents updated dimensions for renewed review. Empty or
   deleted inputs must be refused without creating a job.
7. Create jobs from both a mesh and a solid; inspect model clones, stock and tools,
   Undo/Redo, save and reopen. Source placement and native links must persist.

Full F090 remains open for a complete guided sequence, origin/WCS preview, declared
mesh-unit conversion, machine/strategy compatibility and owner acceptance. Stop at
this usable checkpoint and rotate to another workflow pending owner feedback.

Validated 2026-10-01: 16 distinct native checks (eight model review, eight existing
setup template checks), one grouped PathScripts staging pass, six reviewed final
captures. No native recompilation. The duplicate-label fixture explicitly enables
and restores the native duplicate-label preference in the isolated test session.

Evidence: `D:\Temp\Office-PC\freecad-plus-job-model-review-20261001`.
Open `visual-final/Setup-Sources.FCStd` or `visual-final/Reviewed-Mesh-Job.FCStd`
with `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The second fixture has a 24 x 10 x 5 mm mesh; its original label is intentionally
unchanged, illustrating why reviewed dimensions take precedence over labels.
Installer and physical owner acceptance remain pending.
