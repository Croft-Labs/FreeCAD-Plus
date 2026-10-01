# Native state columns (F013)

Use Tools > Find and describe features in the source-built FreeCAD Plus fork.
This extends the existing feature organizer without changing model execution.

1. Open a model with hidden source features and visible results. Inspect Visibility,
   Suppression and Native state separately. Visibility is the object's flag; a
   hidden parent can still hide an object with a visible flag.
2. Use the state filter to find hidden flags, suppressed features, native errors,
   objects needing recompute, unresolved links or read-only metadata. Text/type
   filters still apply. Columns lets you hide/show the five added columns.
3. Select a row to read its full native status and source identity/path. Local
   objects show their document; a loaded Link shows its immediate source. An empty
   Link says Unresolved link and is not silently loaded or reported as healthy.
4. Change visibility or a source dimension outside the organizer. Rows should
   clear and ask for Refresh. Recompute and refresh to inspect the new state.
   A real feature failure must retain its native explanation. Fix the feature,
   recompute, refresh and verify the error clears.
5. Sorting, filtering and column choices must leave geometry, model order,
   visibility, suppression and Undo unchanged. Selecting a row alone does not
   select or reveal the object in the model; Select in model remains explicit.
6. Existing Label/Description edits still use one undo transaction. Read-only
   metadata disables Apply. Save/reopen and inspect source paths again.
7. Close the organizer, then edit the model; no stale observer should remain.
   Closing the owning document must also close the organizer.

Only loaded objects in the first 2000 entries are inspected, as disclosed in the
scope label. No native error does not certify geometry. Metadata access describes
Label/Label2, not file-system permissions. Full F013 remains open for integrated
navigator columns, reference sets, deeper/unloaded references, persistent global
column preferences, validated visibility/suppression toggles and owner acceptance.
Stop at this functional checkpoint and rotate pending owner workflow feedback.

Validated 2026-10-01: 14 checks pass together (eight state-column checks plus six
existing metadata checks), one grouped FreeCADGui_Resources staging pass and one
corrective Python-only restage for observer initialization guards. No native
recompilation. Seven final captures reviewed; no observer tracebacks in final logs.

Evidence: `D:\Temp\Office-PC\freecad-plus-feature-state-20261001`.
Open `visual-final/Feature-States.FCStd` using
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The fixture deliberately contains an empty Link and a Body whose only feature is
suppressed, so an unresolved link and empty-Tip error are expected diagnostic
examples. The Mounting hole and SecondBracket are valid separate results.
Installer and physical owner acceptance remain pending.
