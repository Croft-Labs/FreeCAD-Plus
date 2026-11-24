import json
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
evidence=repo/'ai-instructions/evidence/pattern-edit-20261124'
result=json.loads((evidence/'installed/result.json').read_text());assert result['ok']
edit=json.loads((evidence/'installed/grid12-edit-timing.json').read_text())['seconds']
create=json.loads((evidence/'installed/fixed-line-grid12-task-timing.json').read_text())['seconds']
text=f'''## Existing Sketch Pattern editing — installed

November 24, 2026. Owner approved the populated editor and Apply/Done/Cancel
workflow. Double-click either the single Pattern icon or constraint-list entry to
edit original geometry, counts, spacing and directions, including angular/radial
patterns and explicit units. Preview replaces the old instances without changing
the document. Done updates/closes; Apply updates/clears; Cancel discards pending
edits. Persistent native geometry IDs preserve definitions across save/reopen;
surviving copy identities and native spacing/Equal relationships are retained.
Recoverable older grouped patterns open with an equivalent layout; ambiguous or
dependent cases explain the blocker rather than discarding geometry.
All {result['tests']} installed application checks and 88 native tests pass, plus four
fresh-process saved-file edits and three existing-shortcut checks. A fixed-length
12-by-12 grid applies in {create:.2f} seconds and edits in {edit:.2f} seconds locally.
Restart FreeCAD Plus to load the update. See
[implementation, native captures and delivery](evidence/pattern-edit-20261124/README.md).

'''
for name in ('WORK_STATE.md','PROGRAMMING_SUMMARY.md'):
    path=repo/'ai-instructions'/name
    original=path.read_text(encoding='utf-8');first,rest=original.split('\n',1)
    path.write_text(first+'\n\n'+text+rest.lstrip('\n'),encoding='utf-8')
path=repo/'ai-instructions/DEVELOPMENT_ROADMAP.md'
original=path.read_text(encoding='utf-8');first,rest=original.split('\n',1)
section=f'''## Existing Sketch Pattern editing — November 24, 2026

- [x] Obtain explicit approval of the populated editor and Done/Apply/Cancel workflow.
- [x] Route both the native Pattern icon and constraint-list double-click to the dedicated task.
- [x] Persist full definitions using native geometry IDs; retain surviving copies and group identity.
- [x] Preview replacements without saved mutations; rebuild constraints/chains atomically with Undo.
- [x] Recover unambiguous older groups and explain unsupported/dependent edits.
- [x] Install and pass {result['tests']} application checks, 88 native tests, four fresh-process file
  edits and three checks through the existing desktop shortcut. Local 12-by-12 line
  editing: {edit:.2f} seconds. See [evidence](evidence/pattern-edit-20261124/README.md).

'''
path.write_text(first+'\n\n'+section+rest.lstrip('\n'),encoding='utf-8')
path=evidence/'README.md';text=path.read_text(encoding='utf-8')
text=text.replace('Final installed verification and delivery results are recorded below after all\nacceptance checks finish.',f'''The final [installed application suite](installed/result.json) passed **{result['tests']} tests**,
zero failures/errors. [All 88 native Sketcher tests](native/tests.txt) passed after
the native rebuild. [Fresh-process acceptance](fresh-reopen/result.json) reopened,
edited through the actual task, saved and reopened four files: the new definition,
multiple external-edge references, and pre-update grouped line/circle grids.
The unchanged desktop shortcut passed [three native task checks](shortcut/result.json),
including both real double-click routes and explicit-unit editing.

The installed fixed-length 12-by-12 grid applied through its task in **{create:.3f} s**
and updated its pitch through the edit service in **{edit:.3f} s**. These are local
measurements, not universal guarantees. The edit retains 430 geometry elements,
286 spacing helpers, 1,145 constraints, 143 Equal copy lengths and two pitch drivers.
Tests cover count/spacing/direction changes, symmetric and negative extents,
angular/radial modes, copy identity, unrelated geometry, other pattern groups,
source freedom, downstream extrusion, dependency rejection and rollback, Undo/Redo,
Cancel, Apply reset, units, native preview coordinates and persistence.

Actual installed captures: [populated task](installed/pattern-edit-panel.png) and
[replacement geometry with spacing preview](installed/pattern-edit-preview.png).
Transparent-child captures initially lost the parent's background; the final task
capture renders through the main window. Native scenegraph checks verify all 14
preview copies and their endpoints in the 5-by-3 fixture.

Testing caught and corrected grouped external-reference indexing and runtime tags
that did not persist across file reopening. Final definitions use serialized native
IDs, and saved-file acceptance includes prior grouped files without definitions.
Intermediate test harness issues (facade serialization, ZIP timestamps and an
initially redundant conflict fixture) were corrected before the passing runs;
rebuild rollback is tested by injecting a failure after old chains are removed.

Seven installed files match the SHA-256 [delivery manifest](install-manifest.json).
Original files have rollback backups; the existing launcher and desktop shortcut
target/working directory remain unchanged. Native compilation is recorded in
[the build log](build.log). Restart FreeCAD Plus to load the native/Python update.
Unrelated `project.previewfirst.json` remains untouched.''')
path.write_text(text,encoding='utf-8')
