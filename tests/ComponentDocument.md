# Component documents: owner and regression procedure

October 1 incorporation: the existing September 28 build was rebuilt while closed.
Run `RunComponentDocument.ps1 -FeedbackSmoke` for 39 feedback checks with source
overlays disabled and exact loaded-payload/native Attributes verification.
`-IntegrationSmoke` covers 24 display/edit/externalization/recovery/save/Undo/BOM
checks; `-CoreSmoke` covers 39 ownership, geometry, conversion, suppression,
copy/persistence and downstream-consumer checks. Use a fresh evidence directory
and this fork executable; results/logs retain failures as well as final passes.
The same desktop shortcut still targets the updated build. Physical owner
acceptance remains separate from automated native GUI and screenshot checks.

Pane follow-up (7.8.7w): check the Add Reference Object button beside Extrude in
Part Design and Part. It must use the active component, preserve the direct-child
source contract, cancel without changes and refuse entry during another task.
Creation must be absent from Part Tree/History context menus; existing reference
repair actions remain. Origin starts visible in History on component entry; hide
it using the eye, refresh, then switch away/back to check the default is restored.
Origin follow-up (7.8.7y): Origin Planes appears as a child of Origin and controls
the three native XY/XZ/YZ planes together. It starts hidden on component entry;
Show reveals planes and the parent, refresh preserves the choice, Undo/Redo restores
it, and re-entry resets the default. Check both eyes, nested/external edit contexts
and New Sketch temporary plane display/Cancel restoration. Origin and Origin Planes
have no suppression/rename/delete action. Delete key and standard Delete must
preserve the origin and its planes, including direct native plane selections and
forced dependency deletion. AssemblyStructureSmoke exercises row/visibility and
source Delete routing; compilation of the native guard remains a separate gate.

Part Tree rearrangement (7.8.7x): run `RunComponentDocument.ps1 -TreeMoveSmoke`
against the grouped payload. Source-overlay evidence is recorded separately in
WORK_STATE. Select linked rows, use Ctrl+X/Ctrl+V and right-click Cut/Paste to move
under another part; Cut alone must leave the document unchanged. Drag onto a part,
above/below a sibling and into empty space; check the insertion indicator, order
and preserved placement. Move a collapsed group and a parent with descendants.
Part001 stays first and cannot move. Expand a grouped destination before choosing
its instance. Check one-step Undo/Redo, save/reopen order, stable IDs, existing
destination numbers and repeated moves without duplicate models or crashes.
Shared-model child changes affect every use. Cycles, stale/cross-file clipboard,
referenced/constrained or driven/scaled reparenting and path display overrides
must be refused without document mutation; sibling ordering remains permitted
with references/overrides. Repair relationships/reset overrides before reparenting.

Models/assembly feedback (7.8.7u): check Models, Part Tree and History
tab order. Models must be flat and show unused definitions plus assembly-use counts.
Part Tree starts with the top-level part (Part001 by default), with its
linked instances beneath it. Selecting Edit on that row returns to top-level
editing; Delete must preserve the root. The row remains after all child instances
are removed and follows a custom root name. Add Component produces one child
occurrence row. Attributes
must retain native View/Data editing without a visible Model tree. Add a second
instance, delete one and then the last: geometry/history must remain in Models with
zero uses and be reusable through Add Instance. Check nested/repeated counts, Delete
key and standard Edit > Delete, active-parent fallback, references becoming missing,
Undo/Redo and save/reopen of unused models. Shared model child-link deletion affects
all uses of that model. Run `RunComponentDocument.ps1 -AssemblyStructureSmoke` after the
grouped build; source overlays cannot verify native Delete/Attributes compilation.

Background result feedback (7.8.7t): after the grouped update, create Extrude001.
Its solid appears with no generated Body row in Model or History. Toggle
Extrude visibility, edit its dimensions, create a downstream Add/Subtract, suppress
and restore that feature, and save/reopen. Face picks must retain reference lineage.
Delete an unused Extrude: its internal result disappears with it; Undo restores both.
Internal-result deletion must be refused, including forced dependency deletion.
Convert to Dumb Object / Delete Parameters exposes an independent Body again.
Run `RunComponentDocument.ps1 -BackgroundResultSmoke` against the grouped payload;
source-overlay tests do not validate the new native Std_Delete guard.

Use the rebuilt FreeCAD Plus checkout, never the separately installed upstream
application. [Roadmap 7.8](../ai-instructions/DEVELOPMENT_ROADMAP.md)
owns acceptance status; the [component contract](../ai-instructions/architecture/COMPONENT_DOCUMENT_CONTRACT.md)
owns requirements.

## Owner workflow

In the updated 9/28 build (roadmap 7.8.7k): standard/Assembly **New Part** routes
to **Add Component**, adding under the active root or child and retaining that
parent's edit context. Adding a component from file returns to the original
occurrence/window. October 1 native feedback/integration checks pass. Use the
intended parent's Part Tree context menu **Add Component**. Do not replace
build files while the owner is testing.

Component BOM feedback (roadmap 7.8.7j): activate a component and choose **Bill of
Materials** from History's context menu (or the existing Assembly command).
The report belongs to that component, appears in its history, and counts child
instances with quantities per parent. **Include nested components** controls deeper
rows. Bodies, sketches and operations are not separate BOM parts.

In Component Structure, use **Bill of Materials > Include / Exclude** on an instance
or a grouped row. This is an owning-component policy, independent of Part View and
mass inclusion. Reopen an existing BOM's editor to refresh counts. Its exclusion list
can omit additional whole instances stored in that report's owning file without
changing other BOMs. Double-click the report in History to edit; OK/Cancel
returns to the original component occurrence.

`RunComponentDocument.ps1 -BomSmoke` runs three workflows from `TestComponentBom.py`.
Final evidence is `D:\Temp\Office-PC\freecad-plus-component-bom-20261001/feedback`;
open `testBOMPolicyReopenAndPerReportExclusions/Assembly.cadprt` with sibling
`Support.cadprt` for saved-policy feedback. Native Assembly builds use
`BuildComponentDocument.ps1 -ScriptsOnly -AssemblyConsumer`. Mass consumers,
automatic cross-file invalidation and broader BOM recovery remain open.

Display-context feedback (roadmap 7.8.7i): open an assembly and a component's isolated
tab. Change a child's Part View in the isolated tab; inactive parent windows should
update inherited occurrences while retaining their explicit path overrides. Hidden
does not change geometry, source-object visibility or BOM/mass participation flags.
Expand repeated instances to see which occurrence is active. The Part View menu
checks the effective choice and enables Reset to Inherited only for local overrides.
Unavailable reference snapshots cannot be shown through the History eye.

`RunComponentDocument.ps1 -DisplayContextSmoke` runs three focused workflows from
`TestComponentDisplayContext.py`: cross-window inheritance and Undo/Redo, menu/active
occurrence behavior, and unavailable history plus `.cadprt` reopen. Evidence:
`D:\Temp\Office-PC\freecad-plus-display-context-20261001/smoke-ready`.
Open `testBackgroundAssemblyAndIsolatedInheritance/Assembly.cadprt` with its sibling
`Support.cadprt` for feedback. The second Support instance overrides the hidden Pin.
Broad task-time display, construction-provider coverage and large-assembly performance
remain pending. One Qt window-activation diagnostic remains in the focused run.

Owning-file Undo/Redo feedback (roadmap 7.8.5f): while an external component is active
in an assembly, Undo and Redo use that component's owning document. Their enabled
states and toolbar history lists follow the same owner. A multi-step toolbar choice
keeps the requested range in that file. Activate the parent to undo parent edits.
An embedded component shares its containing file's history, including in an isolated
tab. History refreshes after the native transaction finishes; sketch/task editor
refreshes stay deferred until editing ends.

`RunComponentDocument.ps1 -UndoRoutingSmoke` runs three focused workflows from
`TestComponentUndoRouting.py`: external operation/suppression restoration and command
availability, multi-step toolbar history, and embedded/ordinary document ownership.
Mixed-file grouped-transaction prompts and close-during-Undo remain broader acceptance.
The 2026-10-01 evidence is
`D:\Temp\Office-PC\freecad-plus-undo-routing-20261001/smoke`.
Open `testExternalOperationUndoRedoAndAvailability/Assembly.cadprt` with sibling
`Support.cadprt` to review the restored Extrude history.

Owning-file Save feedback (roadmap 7.8.3d): activate an external component in the
assembly and use File > Save. Its own file receives the changes while the assembly
view stays open. Save As changes that owning document's location; Save a Copy writes
a separate snapshot while retaining the current location and shared identities.
Activate and save the parent afterward to persist a changed external path. An embedded component,
including one in an isolated tab, saves with its entire containing `.cadprt` document.
The save-dialog title names the owning file. Cancel keeps the current file and view.

`RunComponentDocument.ps1 -SaveRoutingSmoke` runs three focused workflows from
`TestComponentSaveRouting.py`. They cover external Save with an independently dirty
parent, Save As/Copy/Cancel ownership and context, and first-save from an isolated
embedded component. Save All and close/recovery prompts remain broader acceptance.
The 2026-10-01 evidence is
`D:\Temp\Office-PC\freecad-plus-save-routing-20261001/smoke-ready`.
The `testExternalSaveCopyCancelAndSaveAsPreserveContext/Assembly.cadprt` fixture
references sibling `Support-Renamed.cadprt`.

Modeling task transitions (roadmap 7.8.7h): edit an external component instance in an
assembly, select its sketch, then start Extrude/Pad. The task uses the definition's
owning document for geometry; OK or Cancel returns to the original assembly view and
instance. Select a planar face in that same component before New Sketch to prefill
its support. Cancel returns immediately; OK enters the native Sketcher editor and
closing that editor restores the original view. History editing also returns
there, including Extrude edits within an isolated component tab.

`RunComponentDocument.ps1 -TaskContextSmoke` runs three focused workflows from
`TestComponentTaskContext.py`. Evidence is
`D:\Temp\Office-PC\freecad-plus-task-context-20261001/smoke-ready`.
Open `testExtrudePreselectionPreviewCancelAndAccept/Assembly.cadprt` with sibling
`Support.cadprt` for feedback. Save ownership/routing and general native editor
coverage remain separate acceptance work.

Cross-file editing feedback (roadmap 7.8.7g): expand instances of an external
component and double-click a numbered occurrence. The assembly view should remain
active while History shows that definition. Selecting a history item retains
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
names and parent references remain linked. Parent History should immediately
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
5. History lists objects and operations. Use the checkbox to suppress/activate an
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

Pending curve-selection feedback (7.8.7p): after the next grouped update, create
one sketch with nested closed contours, a separate closed contour and an unused
open line. Pick the area between the nested contours: Selected curves must list
both boundaries; Preview/OK must create the annulus only. Clear and pick its edges
individually for the same result; Remove and Use all revise the list. Selecting
the separate contour as well, an open contour, crossing/self-crossing contours or
curves from another sketch must not commit. Edit the sketch dimensions, edit the
saved subset, Undo/Redo and save/reopen; the same body identity and chosen region
must remain. Repeat on a rotated/offset sketch and component. Cancel restores
visibility; successful OK hides the source. Four isolated source-overlay checks
pass; staging/installed-runtime and physical owner acceptance are pending.
Run `RunComponentDocument.ps1 -CurveProfileSmoke` against the updated fork.
For pre-build source checks only, set `FREECAD_PLUS_PROFILE_SOURCE=1`; this loads
repository Python in that isolated process and does not update the owner build.

Pending restored controls (7.8.7q): after the grouped update, compare a one-dimension,
two-dimension and symmetric extrusion. Symmetric length is the total span; the
second-side length/type/reference is independent. Check To first/last, Up to
surface/shape and Through all with a target where required. Move a limiting surface
and check recompute; test signed end offsets, signed start offset/reference, taper,
custom direction, normal-length measurement and Refine. Offsets to a whole
multi-face shape require choosing one limiting face instead. Verify an Add preview
shows only green added volume and Subtract only red removed volume; automatic
preview and manual Preview agree. Target transparency and sketch visibility must
restore on Cancel; successful OK hides consumed inputs. Edit an older simple
extrusion, Undo/Redo and save/reopen while retaining its body and operation UUIDs.
Ten source-overlay workflows pass including region selection; payload validation,
copy/externalization, downstream face references and physical acceptance remain open.

Double-click an operation or its result in History to edit it. Component
Extrude opens the same task for profile/length/direction, mode and target changes,
while retaining the published result identity. Expression-driven extrusion edits remain in the property editor.
Other supported objects use their native task editor. Context menus also offer
Rename. History distinguishes explicit Suppressed, Inactive dependency and repair
states; refresh preserves the selected row and expanded component branches. Creating
an embedded component and its first occurrence is now one Undo step.

New Sketch should display the active component's XY/XZ/YZ origin planes in the
3D view with their labels. Pick each plane and verify the task selects the matching
orientation; test OK and Cancel with previously hidden/visible origin items.
Prior visibility must return. For an external component, the planes belong to
its owning-file task view. Automated selection/visibility checks pass in the
updated development build (roadmap 7.8.7m); physical owner picking remains open.

Click the actual New Sketch OK button and verify Sketcher opens directly, with
no "A dialog is already open in the task panel" confirmation and exactly one
new sketch. Repeat with a selected local face in an external component; closing
Sketcher must restore the originating occurrence/view. Earlier direct Python
acceptance calls missed TaskView's deferred closure (roadmap 7.8.7n). The native
OK-button regression now passes; retain this step for owner acceptance.

New Sketch in Part Design or Sketcher now offers an independent component sketch
whose first default label is Sketch001. Create sketches and bodies in two
components in one file: each starts with Sketch001 and Body001, and only later
items in the same component advance to 002. Every Origin row says Origin.
Check custom names, Undo/Redo and save/reopen without changing native identities.
Run `RunComponentDocument.ps1 -LocalNameSmoke` after the matching native rebuild;
roadmap 7.8.7o is source-only until that grouped update.

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
component graph and format identities are valid. History shows the missing
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
and subelement refusal, and History repair/refresh/suppression controls. Stage
this Python-only batch with `-ScriptsOnly`. The generated broken and repaired .cadprt
files are feedback fixtures, not full format or cross-workbench qualification.

## History suppression feedback iteration

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

Nested Part View overrides follow the copied child instances. History resolves
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

Right-click a body/sheet in History and choose Convert to Dumb Object. The
Delete Parameters review lists the selected geometry, exclusive history to remove,
and shared upstream items to retain. Cancel leaves the document untouched. Accept
keeps the selected object's identity and downstream links; child components survive
even when the deleted operation obtained its inputs through Add Reference Object.
An independent geometry tooltip identifies the converted result in History.

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
source in History for Repair Reference Object. Save/reopen preserves that
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
