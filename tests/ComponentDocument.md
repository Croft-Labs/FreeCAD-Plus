# Component documents: owner and regression procedure

Use the rebuilt FreeCAD Plus checkout, never the separately installed upstream
application. [Roadmap 7.8](../ai-instructions/DEVELOPMENT_ROADMAP.md)
owns acceptance status; the [component contract](../ai-instructions/architecture/COMPONENT_DOCUMENT_CONTRACT.md)
owns requirements.

## Owner workflow

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
