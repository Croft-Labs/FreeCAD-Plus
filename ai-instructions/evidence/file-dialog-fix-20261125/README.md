# Open/import filters and conversion cursor correction

November 25, 2026. Implemented and installed in the existing owner payload.

## Requested correction

Open and Plus File > Import now default to **FreeCAD documents (*.cadprt *.FCStd)**.
The component import and Add existing source chooser uses the same combined filter.
Both file types remain visible without switching filters; per-format filters and
geometry importers remain available. Native Classic import behavior is unchanged.
Save/Save As/export still use their existing document-specific format rules.

The existing conversion/repair dialog temporarily overrides the native caller's
busy cursor with an arrow while waiting for input. Accepting conversion or
**Save .cadprt copy** shows busy only for the operation. Balanced cursor overrides
restore the arrow on error and the caller's original cursor after completion or
Cancel. No cursor stack is cleared, and no dialog layout or choices were changed.

This is a narrow owner-directed correction to the already approved file workflow,
not a new task-panel design. Clone and other pending previews remain unimplemented.

## Verification

- Existing native GUI/App/scripts build passed.
- Source final: **27/27** file-workflow checks passed.
- Installed payload: **27/27** passed in a fresh isolated profile.
- Existing desktop shortcut: **5/5** focused filter/cursor checks passed.
- Tests exercise actual Std_Open/Std_Import dispatch for both formats, Classic
  conversion, mislabelled Plus repair, source chooser file visibility, an old
  single-format import preference, error/retry/Cancel cursor restoration, and
  preservation of an enclosing cursor override.
- Existing Save/Save Copy/Save All/save-on-close, source preservation, conversion
  rejection and external-link relocation checks remain passing.
- Five installed files match their source hashes; rollback copies retained. Three
  DLLs were staged with the rebuilt GUI dependencies, plus file_workflows.py and
  TestFileWorkflows.py. Restart the owner app to load the changed DLL/module.
- Desktop shortcut still targets `Launch FreeCAD Plus.bat` in the existing
  `_temp builds/FreeCAD-Plus` payload directory, with that working directory and
  empty saved arguments. Validation supplied temporary isolated-profile arguments.

The first source run exposed two test-fixture issues: the Python source chooser
used a Windows native dialog without a Qt file model, and the generic callback
helper treated the previous error label as failure after a successful retry.
Fixtures now explicitly select Qt dialogs for model inspection and check the
accepted result before reporting a stale error. Intermediate results are retained;
the final full source and installed runs pass. No extra production fix was needed.

## Native screenshots

- [Open combined filter](open.png)
- [Import displaying both formats](import.png)
- [Existing repair dialog](repair.png)

These are actual installed Qt dialog captures. Cursor state is established by
runtime assertions before acceptance, during conversion/repair, and after return;
widget screenshots do not include the operating-system cursor. Test profiles and
temporary CAD fixtures were archived as results only and then removed. The owner
payload, build tree, desktop shortcut and rollback copies remain intact.
