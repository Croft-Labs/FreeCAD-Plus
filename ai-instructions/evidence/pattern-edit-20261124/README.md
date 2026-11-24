# Editing existing Sketch Patterns — November 24, 2026

Starting source/install: `0272712e7fbcf589523db245c1ad640ea150e00f`.
The owner explicitly approved reopening either Pattern icon/list entry in the
populated Sketch Pattern panel, with Done updating and closing, Apply updating
then clearing for another pattern, and Cancel discarding pending edits:
**“Approve and implement.”**

The [baseline](preview/baseline.png) and [approved proposal](preview/proposed.png)
are isolated Qt simulations, not installed functionality. Companion session
`f191f8a6d7c9`, candidate fingerprint
`45c2984b0dbc09b47832518729e2b4b0dfb50c6c8660f67f47b129582991a09e`.
The preview was valid with no violations after the chat approval. No companion
approval state was set on the owner's behalf.

## Implementation

Both native double-click routes open the same dedicated Sketch Pattern task.
It restores original geometry, counts, spacing/total modes, directions and
references, reverse and independent/symmetric extents, linear/circular modes,
angular/radial settings, explicit units, and spacing/hide choices. Native task
activation is deferred until the list or viewport event unwinds. Other sketch
sections stay hidden for the task and restore when it closes.

Pending edits render replacement instances and spacing chains. The old generated
geometry and associated constraint graphics are temporarily hidden through the
view provider, without changing geometry properties, saved constraints or Undo.
The source and unrelated geometry remain visible. Done updates and closes;
Apply updates and clears the editor for another pattern; Escape/Cancel restores
the unmodified existing pattern. Errors retain the inputs with an explanation.

`PatternDefinitions` is a hidden native `App::PropertyMap`, keyed by the existing
Pattern UUID. Version 1 JSON stores persistent native `SketchGeometryExtension`
IDs for originals, internal references, helpers and copies by source and signed
ordinal slot, plus all authored options and native external geometry IDs.
Native external IDs avoid the grouped LinkSubList ordering
trap and remain distinct when multiple edges belong to one external object.
Reopening refreshes spacing from the current driving constraints and explicit units.

An update is one native transaction. It retains source geometry and surviving
copies' native IDs and runtime tags, moves those copies by relative rigid transforms, batches old
group constraint/helper removal, and reuses the creation service to regenerate
native Equal relationships and connected spacing chains. The existing group UUID
and name survive. New copies are appended; obsolete copies are removed. Undo/Redo,
save/reopen and whole-sketch downstream consumers remain supported. A failed
rebuild aborts the transaction and restores the previous definition and geometry.

Older *grouped* patterns without a recipe recover an equivalent layout from their
connected spacing topology when it is unambiguous. Lost authoring choices such as
pitch versus total or symmetric versus balanced independent extents cannot be
recovered exactly. Radial-only groups without a stored center recover an equivalent
linear direction. Missing/nonuniform topology produces an inline explanation.
Ungrouped legacy sketches are not guessed into patterns.

Edits reject removal of instances/helpers referenced by unrelated constraints,
authored driving-pitch expressions, outside expressions referencing rebuilt group
constraints, and explicit downstream subelement consumers. The downstream guard
is conservative because rebuilding helpers can renumber edges; whole-sketch
extrusions remain supported. These cases explain the dependency instead of
silently deleting or retargeting it. New direction/center references cannot depend
on the pattern's own generated geometry. Patterns without any generated constraints
continue to have no Pattern constraint entry.

## Verification and delivery

The final [installed application suite](installed/result.json) passed **93 tests**,
zero failures/errors. [All 88 native Sketcher tests](native/tests.txt) passed after
the native rebuild. [Fresh-process acceptance](fresh-reopen/result.json) reopened,
edited through the actual task, saved and reopened four files: the new definition,
multiple external-edge references, and pre-update grouped line/circle grids.
The unchanged desktop shortcut passed [three native task checks](shortcut/result.json),
including both real double-click routes and explicit-unit editing.

The installed fixed-length 12-by-12 grid applied through its task in **4.036 s**
and updated its pitch through the edit service in **3.795 s**. These are local
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
Unrelated `project.previewfirst.json` remains untouched.
