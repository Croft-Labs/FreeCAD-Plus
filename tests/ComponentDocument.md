# Component documents: owner and regression procedure

Use the rebuilt FreeCAD Plus checkout, never the separately installed upstream
application. [Roadmap 7.8](../ai-instructions/DEVELOPMENT_ROADMAP.md)
owns acceptance status; the [component contract](../ai-instructions/architecture/COMPONENT_DOCUMENT_CONTRACT.md)
owns requirements.

## Owner workflow

Cross-file editing feedback (roadmap 7.8.7g): expand instances of an external
component and double-click a numbered occurrence. The assembly view should remain
active while Model History shows that definition. Selecting a history item retains
the chosen occurrence path. Open Component in Tab provides an isolated view; switching
between it and the assembly restores each view's active nested component. Rename or
Save As updates the isolated tab's component name/owning-file title. If an active link
becomes unresolved, the navigator falls back to the nearest available component.

`RunComponentDocument.ps1 -EditContextSmoke` runs three focused workflows in
`TestComponentEditContext.py`. The 2026-10-01 evidence is
`D:\Temp\Office-PC\freecad-plus-edit-context-20261001/smoke-final`.
The `testIsolatedTabsRestoreNestedContextAndOwningFileTitle/Assembly.cadprt` fixture
references sibling `Renamed-Support.cadprt`. Native modeling-task entry/exit and full
save-routing acceptance across owning files remain separate work.

Save to External File feedback (roadmap 7.8.8d): save the parent `.cadprt`, finish
the current edit and close isolated tabs for the component and its embedded children.
Right-click an embedded component and choose Save to External File with a new
`.cadprt` filename. Its embedded children move with it; shared instances, component
names and parent references remain linked. Parent Model History should immediately
show current reference/results geometry. The active component and parent view remain
selected. Already external components have this action disabled. Save the parent to
persist the new external links. Undo restores embedded definitions; the newly created
external file remains on disk.

Bounded automated feedback: `RunComponentDocument.ps1 -ExternalizationSmoke` runs
only `TestComponentExternalization.py` (three workflows). The 2026-10-01 evidence
is `D:\Temp\Office-PC\freecad-plus-externalization-20261001/smoke-final`.
Open `testSharedHierarchyReferencesUndoAndReopen/Parent.cadprt` there to review
the shared Bracket/Pin example. Broader compatibility, crash recovery and migration
of open isolated tabs remain pending; this check is not full schema acceptance.

1. File > New creates a component document. Component Structure starts with the
   root component and the native yellow Part icon. There is no file wrapper row.
   Tools > Component Structure reopens the navigator.
2. Add Component creates an embedded definition or inserts an existing definition.
   Save both documents before inserting an external `.cadprt`. Repeated instances
   share geometry and keep separate placements. Right-click a component for Add Component, Instances > Add Instance / Copy to
   New Part, Save to External File, Part View settings or repair. Expand Instances
   reveals numbered occurrences of a grouped part; the group shows its count.
3. Double-click a component to edit its definition, or choose Open Component in
   Tab (child rows only). Check the highlighted active part and editing label; the
   panel has no filename/path. The active component cannot be hidden. Editing
   a shared definition updates every instance; the isolated tab creates no copy.
4. Add Reference Object lists evaluated objects from direct children. It accepts
   bodies, sheets, sketches and curves. Referenced sketches contain evaluated
   geometry only. Edit the source, then activate the parent: its reference and
   downstream operations should update without changing source history.
5. Model History lists objects and operations. Use the checkbox to suppress/activate an
   item and the next icon to show/hide it. A partial check means an input is inactive.
   Its context menu offers Convert to Dumb Object. Delete Parameters retains the result identity and
   valid downstream links; Extract Dumb Body creates an independent copy. Check
   Undo/Redo and separate suppression on an independent operation.
6. Check Bodies Only, Full Component, Hidden and Reset to Inherited through a
   nested repeated component. A higher override must affect only that path, and
   a Hidden ancestor must hide its branch. These settings do not specify BOM/mass.
7. Save/reopen `.cadprt`, edit a source and check the result. Save Copy keeps the
   document identity and does not change the current save location. Move an
   external file and use Locate Component File to repair its identity-preserving
   link. Unresolved or wrong-identity links must not save silently.
8. Open a legacy FCStd via File > Open. Review legacy conversion details, save a
   new `.cadprt` and verify the original is unchanged. Retained native Body or
   unsupported payloads must not be mistaken for fully migrated component history.

## Current feedback iteration

The native Extrude/Pad/Pocket commands in a component document now open a component
Extrude task. Choose a local sketch or evaluated curve profile without creating a
Body container. Choose New Body, Add or Subtract; Add/Subtract require an explicit
local target. Length, direction and preview are available before committing.
Preview and Cancel leave no feature in the document. This iteration supports one
solid output; disjoint/multiple-solid results are refused.

Double-click an operation or its result in Model History to edit it. Component
Extrude opens the same task for profile/length/direction, mode and target changes,
while retaining the published result identity. Expression-driven extrusion edits remain in the property editor.
Other supported objects use their native task editor. Context menus also offer
Rename. History distinguishes explicit Suppressed, Inactive dependency and repair
states; refresh preserves the selected row and expanded component branches. Creating
an embedded component and its first occurrence is now one Undo step.

New Sketch in Part Design or Sketcher now offers an independent component sketch
on XY/XZ/YZ or a selected planar face with offset, then opens the native editor.
The new sketch belongs to the active component and needs no Body container.

This is a feedback build. Broader topology, native command parity, consumer and
file-format qualification wait for owner feedback. For the three current checks,
add `-PanelSmoke` to `RunComponentDocument.ps1` instead of running the full suites
below. They cover native sketch commands/attachment, Extrude mode and target edits
with Undo/save/reopen, and grouped instances/menu/visibility/history controls.
`-IterationSmoke` selects the preceding extrusion iteration instead. Neither is
full schema qualification. Current panel captures and two .cadprt feedback fixtures
are produced under the selected evidence directory.

## Selection and view-context feedback iteration

Selecting a component row or history item now uses its native occurrence path.
Select a face in a repeated nested component: Component Structure should reveal
that instance without changing which definition is being edited. History selection
appears when the picked object belongs to the active component. Clear selection
in the native view to clear the corresponding panel highlights.

Select a direct child's body (or one of its faces), then Add Reference Object:
the dialog reviews the whole evaluated object in that occurrence. Bare shared
geometry, grandchildren and unrelated selections must not choose a source silently.
Change a grouped row's Part View and use Undo once: every represented instance must
return to its prior state. Open a child in its own tab twice: the second request
focuses the existing tab. Switching back restores the original active component.

Native selection can normalize a bare scripted object into an occurrence before
the panel receives it. The reference dialog reviews that incoming occurrence; the
mapper itself refuses to pick a path when given genuinely ambiguous bare input.

Use `-SelectionSmoke` for the three current bounded checks: nested native selection /
history round-trip, direct-child reference choice and .cadprt reopen, and grouped
Undo plus isolated-tab context. For this Python-only batch, `-ScriptsOnly` on the
build helper stages GUI resources, Part scripts and Show without recompiling native
C++. Broad component suites and full GUI/consumer acceptance remain deferred.

## Reference recovery feedback iteration

A .cadprt with a missing reference object remains open for repair, provided its
component graph and format identities are valid. Model History shows the missing
source and a repair detail tooltip. Edit/double-click the reference, or use Repair
Reference Object, to choose replacement whole geometry from a direct child. The
reference identity, history position, valid whole-object consumers and authored
suppression remain intact. Change Reference Source uses the same review for an
existing source. Use Refresh References after source changes to update snapshots.

Independent references and new local sketch/Extrude branches continue when another
reference is broken. Failed references have no usable evaluated shape. Different
geometry kinds and unreviewed face/edge or expression consumers are refused before
retargeting; complete topology repair is still a future gate.

Use `-ReferenceSmoke` with the runner for the current three checks: broken-reference
save/open plus independent work, identity-preserving native Cut repair with Undo/Redo
and subelement refusal, and Model History repair/refresh/suppression controls. Stage
this Python-only batch with `-ScriptsOnly`. The generated broken and repaired .cadprt
files are feedback fixtures, not full format or cross-workbench qualification.

## Model History suppression feedback iteration

Suppress an operation in a chain: dependent items become partially checked/inactive,
while independent branches continue. Hover over the state or checkbox to see which
suppressed inputs block it. Earlier usable bodies reappear; a shared input remains
consumed while another active operation needs it. Unsuppressing restores eligible
results without clearing separately authored suppression or unrelated visibility.

Select several history rows and right-click Suppress Selected Items or Unsuppress
Selected Items. One Undo restores the whole selection's previous flags and geometry.
Right-clicking an unselected row scopes the command to that row. Suppression is saved
in .cadprt; the same dependent state should appear when reopening the feedback file.

Use `-HistorySmoke` for three bounded workflows; use `-ScriptsOnly` for this Python
batch. Native Boolean recompute can still log `Base shape is null` when suppression
empties its input. The published body stays unavailable and recovers on unsuppression;
native scheduling integration remains open. The feedback fixtures and checks do not
qualify the complete suppression model, external-document matrix or file schema.

## Copy to New Part feedback iteration

Expand repeated instances, then use Instances > Copy to New Part on the instance to
separate. Its placement remains intact; geometry edits to the copy leave the other
instances unchanged. Parent Add Reference Object items using the selected instance
follow its new geometry without changing their own identities or history positions.
References using other instances stay on the shared original. Child definitions
remain shared, including sources for reference objects within the copied definition.

Nested Part View overrides follow the copied child instances. Model History resolves
the active occurrence after Copy/Undo/Redo. If a deeper editing path no longer exists,
it falls back to the nearest surviving component; isolated views of the original
definition continue editing that original. Activating a changed component refreshes
its reference snapshots. Unrelated suppressed child history is not a geometry input
to a parent operation that references a different body in that child.

Use `-InstanceSmoke` for the three current workflows and `-ScriptsOnly` to stage this
Python batch. Review the generated independent-reference, assembly and embedded-copy
.cadprt fixtures in the fork build. Face/edge and expression rebinding remains guarded;
other open files with affected nested overrides must reset those overrides before
copying. Complete external-ancestor and topology remapping remains future work.

## Convert to Dumb Object feedback iteration

Right-click a body/sheet in Model History and choose Convert to Dumb Object. The
Delete Parameters review lists the selected geometry, exclusive history to remove,
and shared upstream items to retain. Cancel leaves the document untouched. Accept
keeps the selected object's identity and downstream links; child components survive
even when the deleted operation obtained its inputs through Add Reference Object.
An independent geometry tooltip identifies the converted result in Model History.

Choose Extract Dumb Body to keep the original and create an independent, unlinked
copy. Already independent objects default to extraction. Referenced curves and dumb
sketches can be extracted; Delete Parameters remains restricted to bodies/sheets.
Converting a body/sheet reference disconnects its source metadata; Undo restores it.

Use `-ConversionSmoke` for the three current feedback workflows and `-ScriptsOnly`
for this Python batch. Native Mirror may emit an empty-shape diagnostic during Undo
before reference activation; the focused workflow asserts current downstream geometry
after activation and final geometry after Redo/reopen. General native scheduling,
multi-body contribution detachment and arbitrary topology/expression consumers remain
open. These focused checks are not full file-format validation.

## Locate Component File feedback iteration

Missing instances remain grouped by their saved definition identity and can be
expanded to numbered rows. Geometry-dependent actions and visibility changes are
unavailable until the file is located. Right-click Locate Component File and choose
the moved .cadprt. Matching unresolved instances in the same owning file recover
together, preserving placement and reference identities in one Undo transaction.

A missing body in that file does not block recovery of the component. Healthy
references update; unavailable ones keep their source identity and appear as Missing
source in Model History for Repair Reference Object. Save/reopen preserves that
partial recovery. Choosing a file with another definition identity leaves the parent
unchanged and returns to its editing context. Unresolved native links explicitly
cleared during recovery no longer save the obsolete filename, including after Redo.

Use `-RecoverySmoke` for three focused workflows: grouped locate/Undo/Redo/reopen,
partial geometry recovery with independent modeling and saved-link inspection, and
wrong-file refusal with parent-context preservation. Intentionally missing files
produce native missing-file/broken-link diagnostics before repair. General package
relocation, recovery across multiple owning files, automatic searching and complete
crash/backup/schema qualification remain future work.

## Automated checks

Run from the repository root in PowerShell, with a new evidence directory each time:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests/BuildComponentDocument.ps1 -CMake <cmake.exe> -BuildDirectory <local-build> -OutputDirectory <build-evidence>
powershell -NoProfile -ExecutionPolicy Bypass -File tests/RunComponentDocument.ps1 -Executable <local-build>\bin\FreeCAD.exe -OutputDirectory <model-evidence>
powershell -NoProfile -ExecutionPolicy Bypass -File tests/RunComponentDocument.ps1 -Executable <local-build>\bin\FreeCAD.exe -OutputDirectory <cold-evidence> -ColdFixtureDirectory <model-evidence>
```

The model suite checks identities, cycles, references/transforms, shared sketches,
suppression and Boolean restoration, parameter removal, Undo, copies, assembly
externalization, missing-file repair, schema refusal, rejected-save preservation,
legacy source protection, downstream Draft/CAM/TechDraw updates and navigator
rendering. `results.json`, process logs and loaded module hashes identify evidence.
The cold suite imports installed modules without source-path injection, compares
their hashes and drives standard native File dialogs with isolated preferences.

The GUI suite captures `component-structure.png`, `model-history.png` and
`isolated-component.png`. Review those images in addition to structural assertions.
Source/runtime checks do not substitute for mouse/keyboard owner acceptance,
general topology changes, complete workbench migration or release validation.

## Current implementation limits

Native Part/Sketcher geometry can be adopted into component history in its original
transaction; unmigrated Part Design commands still use their native Body workflows.
Automatic multi-solid output-role assignment is refused. Expression-driven copies
and ambiguous reference remapping require explicit future support. Assembly
Constraints grouping is implemented as a projection, but joint creation and solver
integration remain open. BOM/mass flags are stored separately; consumer integration
is pending. FEM is disabled in the current local build. Deep hierarchy copying,
complete isolated-view picking/edit acceptance and broader recovery/performance
checks remain in the roadmap. There is no installer or public release from this batch.
