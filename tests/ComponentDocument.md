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
   share geometry and keep separate placements. Right-click an instance for Make
   Independent, Externalize Component, representation settings or repair.
3. Double-click a component to edit its definition, or choose Open Component in
   Tab. Check the edited component and owning file shown above the tabs. Editing
   a shared definition updates every instance; the isolated tab creates no copy.
4. Add Reference Object lists evaluated objects from direct children. It accepts
   bodies, sheets, sketches and curves. Referenced sketches contain evaluated
   geometry only. Edit the source, then activate the parent: its reference and
   downstream operations should update without changing source history.
5. Model History lists objects and operations. Its context menu offers suppression
   and Convert to Dumb Object. Delete Parameters retains the result identity and
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
Extrude opens the same task for profile/length/direction edits while retaining its
saved mode/target. Expression-driven extrusion edits remain in the property editor.
Other supported objects use their native task editor. Context menus also offer
Rename. History distinguishes explicit Suppressed, Inactive dependency and repair
states; refresh preserves the selected row and expanded component branches. Creating
an embedded component and its first occurrence is now one Undo step.

This is a feedback build. Standard Part Design sketch creation still has its native
Body workflow; full sketch/command integration remains pending. Broader topology,
consumer and file-format qualification waits for owner feedback. For the small
current smoke check, add `-IterationSmoke` to `RunComponentDocument.ps1` instead of
running the full suites below.

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
