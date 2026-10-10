# FreeCAD Plus: Programming Summary

Part type revision backend: ComponentModel.part_type / set_part_types own direct
child settings; effective_part_type resolves edit context and
part_type_allows_geometry supplies the pending consumer guard. CadDocument gates
explicit values with component-part-types-v1. See the component contract, roadmap
7.8.14 and TestComponentPartTypes. require_geometry_access now guards current_shape
and BasicShapes.ShapeReferences native paths/owned input validation; see
TestComponentGeometryAccess. Native output/consumer and UI integration remain pending.


File-root foundation: ComponentModel.ensure_file_container provides explicit,
undoable migration preserving old definitions/placements/external references.
CadDocument cross-checks component-file-container-v1 against the native marker.
TestComponentFileContainer covers this service. new_file_document now backs native
New with an active ordinary Part001 beneath the pinned file;
TestComponentFileWorkspace covers the UI and empty-tree/undo/reopen behavior.
External-copy and new-external-component destinations now use the same file root
without an extra Part001. Newly opened older .cadprt files/dependencies now migrate
after identity validation, without writing the originals; bootstrap undo cannot
remove the file root. File activation refreshes domestic references child-first.
Legacy conversion/recovery now creates the file root in the same undo transaction
(7.8.13d2b2b). Definition deletion now has a guarded transactional backend;
Models/native Delete now use it with unused-edit and isolated-tab cleanup;
shared modeling launchers now guard file Edit, including explicit sketch/plane
destinations. Native Part Primitive/Extrude/Revolve/Loft/Sweep now dispatch to the
shared tasks in component documents, retaining legacy dialogs elsewhere.
TestComponentNativePartRouting covers the native dispatch; TestComponentFileCommands
covers task guards and file placement. ComponentCommand.h/Command.cpp now share
file-Edit guards across 46 native Part modeling commands; native guard acceptance
is TestComponentNativeModelingGuards. The native assembly solver now supports an
internal context borrowing file occurrences (TestComponentAssemblySolver).
ensure_assembly_context now creates its joint owner transactionally; CadDocument
cross-checks component-file-assembly-v1 on save/open. TestComponentAssemblyPersistence
covers ownership, endpoint guards and native fixed-joint persistence. Ground/fixed
relationship services now create, edit and remove joints transactionally, verify
fixed connector frames and preserve grounded placements; external definitions stay
unchanged (TestComponentRelationshipTransactions). Part Tree Ground/Unground now
requires file Edit and one direct occurrence, with stale-menu and task guards
(TestComponentGroundingUI). Fixed creation preserves current relative placement;
Part Tree relationship review, offset editing and removal now use the same guarded
service (TestComponentRelationshipsUI). ValidateComponentEditing.FCMacro now
provides the bounded eight-suite integration batch; all 62 cases pass after two
legacy test assumptions were corrected. The final owner payload now passes 74
installed cases plus two fresh-process reopen cases through the updated desktop
shortcut, with no source overlays. Roadmap 7.8.13 is complete; see WORK_STATE for
build identity and delivery evidence. Add Component changes remain deferred.
The isolated-tab/contextual-fade repair (7.8.13f1) keeps native viewer roots in
place and attaches view-owned display branches. See WORK_STATE for validation;
definition deletion UI integration is covered by TestComponentDefinitionDeletionUI
(7.8.13d2c2). ComponentModel.delete_definition retains the shared ownership guards;
TestComponentDefinitionDeletion covers its backend transaction semantics.

Active-editing revision: ComponentNavigator resolves placed Models Edit in the
current tab with per-tab occurrence memory and native active-color decoration.
Unused models now use a per-window temporary LinkView and (unused model) tree entry;
existing assembly visibility remains authored and is restored by returning its scene.
TestComponentActiveEditing covers both steps. display_items shares native visibility
traversal with context_display_plan; TestComponentContextDisplayPlan checks exact
occurrence fade classification without changing materials. context_scene renders the
per-view transparency floor through native links beside the original selection
separator; cleanup removes only these view-owned nodes. Native picking and camera
state stay attached throughout contextual editing and tab switches. Pinned-file
and grouped delivery are accepted in roadmap 7.8.13; Add Component is deferred.

October 9 file hierarchy: ComponentModel owns explicit imports, file-cycle guards,
qualified names and independent domestic hierarchy copies; CadDocument persists the
additive `component-file-imports-v1` capability. ComponentNavigator provides nested
Models groups, three storage choices and selected domestic replacement. See
[acceptance checks](../tests/ComponentFileHierarchy.md), the component contract,
roadmap 7.8.12 and WORK_STATE for source/runtime versus owner-build status.

Legacy migration task two routes GUI File Open through native structural conversion:
Models definitions, shared Part Tree occurrences and retained Body/sketch payloads.
Exact frames/scales, external save order, missing links and explicit dumb recovery
are documented in tests/LegacyStructureConversion.md. The task-three Sketch/Pad
pilot preserves native identities, orders inputs before the original Body result
and uses an internal child-scoped Tip bridge. See tests/LegacyBodyHistory.md;
later feature adapters and installed delivery remain separate.
Task four exposes native datum frames in component History while retaining original
Origins, Body owners and attachment engines. LegacyFrameVersion upgrades verified
older converted files; native editors preserve supports/formulas. Linked planes
work with new associative sketches. See tests/LegacyDatumFrames.md.
Task five retains original sketch constraints/expressions/attachments and shared
consumers through component inputs or complete-frame History access links. The
safe Sketch/Pad pilot accepts independent dimensional expressions/external inputs;
Body-dependent attachments stay native for later feature adapters. See
tests/LegacySketchInputs.md; installed delivery remains batched.
Task six maps qualified native Pad/Pocket chains to explicit component results and
targets while preserving original feature/Body identities and native extents. Shared
Extrude edits Pocket directions/modes safely; other attachment/reference histories
remain editable native engines through History. Normal standalone Part Extrusions
are published; custom outputs retain native controls. See tests/LegacyExtrusions.md.
Task seven reuses native chain publishing for Revolution/Groove and qualified mixed
extrusion histories, retaining sketch axes, angular settings and explicit targets.
Other references/frames and standalone signed Part Revolutions retain native editors;
LegacyRevolveVersion upgrades prior converted files. Whole-sketch Revolve previews
retain native angular frames/construction axes. See tests/LegacyRevolutions.md.
Task eight preserves ordered native Loft sections and explicit Boolean targets using
the shared chain publisher and retained-operation editor links. Converted native
Loft edits retain their feature type/identity through persisted Boolean presets;
legacy whole-sketch subreferences/attachments and Part Loft settings remain native.
LegacyLoftVersion upgrades prior files. See tests/LegacyLofts.md.
Task nine extends the shared chain publisher to qualified Pipe profile/path sketches
and explicit targets, retaining native orientation and exact edge references.
Converted Pipe mode edits preserve native type/identity; unsupported histories and
standalone Part Sweep retain original editors. LegacyPipeVersion upgrades earlier
converted files. See tests/LegacyPipes.md; installed delivery remains batched.
Task ten adds bounded Helix and eight-primitive adapters through the same publisher,
retaining native parameter laws, axes/dimensions, original types and explicit targets.
Attached/unsupported histories and standalone Part primitives/Helix retain native
editors. Separate family versions upgrade older conversions; converted primitive
shape changes require separate operations. See tests/LegacyHelixPrimitives.md.
Task eleven exposes retained native dress-up, pattern/transformation and Boolean
operations through ordered component History access links. Native topology inputs,
owners, tools/settings and direct standalone outputs remain intact. Separate family
versions upgrade prior converted files. See tests/LegacyFinishing.md; physical
flattening and whole-file qualification are not implied by native retention.
Task twelve qualifies a bounded whole-file mixed/shared/external migration corpus
and packages the earlier compatible Python changes for owner testing. Legacy
Draft/CAM/TechDraw consumers, fresh-process restore and the saved desktop shortcut
are integration gates. See tests/LegacyIntegration.md and current WORK_STATE;
native FEM and exhaustive custom workbench qualification remain explicit boundaries.
Owner DOCX is UI/UX only; algorithms,
technical contracts and test/build/publication evidence belong in Markdown.

Legacy migration task one: CadDocument.legacy_plan delegates to LegacyConversion
inventory for read-only ownership/dependency/geometry planning. Recovery candidates
include dumb body/sheet/curve/point; all later feature tasks retain native editability
before geometry-only recovery. See tests/LegacyConversionPlan.md and WORK_STATE.

ConstraintPaletteGui synchronously hides the palette's native tooltip before
solving, refresh and close, and hides retired buttons before deferred deletion.
Native icons/tooltips and the one-second travel grace remain retained; WORK_STATE
owns the installed 19-check, increased-scale and actual saved-shortcut evidence.
The October 6 Modeling ribbon revision is owned by PlusRibbon.MODELING_GROUPS /
MODELING_SIZES. Gray group dividers apply to all tabs; RibbonButton paints complete
fitted two-line large captions, while medium/small buttons remain icon-only.
The canonical DOCX and toolbar reference contain the requested six-group layout.
Medium ribbon icons are 32 logical pixels in 42px-high buttons; the shared grid
starts at 86px and grows to fit captions. WORK_STATE owns the installed native/
scaled/shortcut evidence and the compatible Python owner payload.

Owner artifact policy: generated validation belongs only in
`C:\Users\GAMING-PC\Documents\_temp\freecad\validation` and is deleted at task
completion after recording verified summaries. Useful test payloads, native build
trees and their dependencies belong in the sibling `test-builds` directory.
WORK_STATE records the relocated current payload and verified desktop shortcut.

Startup and workspace persistence: StartupProcess seeds theme/docking preferences
before native managers initialize and exposes the completed workspace once.
ComponentNavigator registers its dock before restore and keeps user-customized
positions. PlusRibbon loads only Home command modules; movable Plus toolbars retain
saved locations. Native 13-case startup and six-case ribbon checks, packaged cold
restart/style/profile-copy checks and the actual desktop link launch pass.
WORK_STATE owns the new startup-workspace payload, hashes and validation limits.

Move Components workflows are in `MoveComponents.py` and
`MoveComponentsTask.py`: parent-owned native link placements, exact display paths,
shared-parent transient previews and atomic sibling transactions. The task includes
Translate, recovered Rotate, Point to Point, Align Axes and Align Coordinate Systems.
`MoveComponentsManipulator.py` uses native view-owned arrows/planes/rings for
Interactive and pivot editing. Entry points are Design Assembly and Part Tree.
October 6 final recovery acceptance passes 89 full native packaged checks,
55 at DPR 3.0 and 26 launched through the verified saved desktop shortcut.
The grouped incremental test payload is delivered; physical owner feedback is separate.
See `tests/MoveComponents.md` and WORK_STATE for evidence and remaining gates.

Design Layers and the Contextual Constraint Palette are implemented in source in
`DesignLayers.py` / `DesignLayersGui.py` and `ConstraintPalette.py` /
`ConstraintPaletteGui.py`. Layers use saved metadata without group/dependency edits;
native Body and Plus result chains keep input sketches independent. The palette
uses native Sketcher constraints and shared selection persistence. Its cloned-solver
diagnostic and driving-batch APIs were built in the October 6 grouped runtime;
current source/tests pass recovery item 7 native/packaged/high-DPI acceptance
and verified desktop launch delivery.
See WORK_STATE, UI_UX_SPEC and the corresponding tests for evidence and remaining gates.

Design Selection toolbar source: `DesignSelection.py` owns semantic categories,
curve chains and shared persistence; `DesignSelectionToolbar.py` integrates with
PlusRibbon. Native Selection/box/Sketcher hooks have earlier grouped build evidence.
The guarded late Escape race repair and changed fixtures pass item 7 acceptance.
See WORK_STATE, `tests/DesignSelection.md` and `tests/RecoveredWorkload.md`;
the DOCX renderer is resolved and affected pages are reviewed.

Modeling curve picks now arbitrate edge versus region hits before depth filtering.
`ComponentTaskWidgets.py` owns the reusable profile/section/path collector, selection
controller, preview controls, common fields and compact layout. Extrude, Revolve,
Helix, Loft and Pipe share the collector; all six modeling tasks share preview
controls. WORK_STATE records reproduction, native checks and owner delivery.

## Project at a glance

All Plus task forms now inherit Qt/theme colors: no task-wide color stylesheets
or copied form palettes. The development guide records this rule; WORK_STATE
records the focused theme checks and incremental owner payload.

Datum Plane create/edit now uses Plane orientation and location, Orientation,
Origin selection and Preview. Its mixed-reference lists extend the shared curve
collector; geometry combinations and explicit offset/normal values define an
associative native plane. Origin geometry temporarily doubles in size. Tasks
follow the active palette and the ribbon refreshes after palette changes.
New Sketch retains its independent/support placement workflow. WORK_STATE records
the grouped native build, runtime checks, Word review and owner delivery.

Editing a History item temporarily suppresses the later history tail through
shared TaskContext lifecycle handling. Authored suppression is preserved; finish,
cancel, startup failure and save-time restoration are covered by native checks.
WORK_STATE records the current Python-only owner payload and validation.

Model History now supports dependency-clamped drag/drop ordering with its native
Origin fixed first. Multi-item order, hidden results, expression dependencies,
Undo/Redo and persistence are covered by 40 distinct native checks. WORK_STATE
records the Python-only owner payload, Word review and shortcut delivery.

The Components panel now opens a feature/operation editor or Sketcher directly
when its History name, icon or status area is double-clicked. Native double-click
handling survives an intervening row rebuild. Twenty panel, History and component
context checks pass; WORK_STATE records the Python-only owner build and shortcut.

The modeling preview update adds None/Overlay/Result preview dropdowns to all six
shared component modeling tasks. Overlays show full blue/green/red tool shapes
without requiring Boolean contact; Result uses normal appearance. Seventy-five
workflow checks pass. This is Python-only staging on native identity
`03a6f6664448`; the desktop shortcut is verified. WORK_STATE records the
payload, evidence, Word review and source publication. The preceding combined
native rebuild and temp cleanup remain recorded separately below.

Component curve collectors now select the latest picked list entry, toggle it off
on a repeated pick and support Delete. Redundant selected-curve capture buttons
are removed. Shared profile and Pipe path lists retain persistent viewport emphasis;
WORK_STATE records the 31 distinct runtime checks and Python-only owner delivery.

Component curve tasks now keep collected geometry highlighted independently of
native selection. After the first curve, other sketches are light-medium gray
without region fill; Loft sections and Pipe paths share the behavior. See
WORK_STATE for the staged runtime, focused checks and owner shortcut.

The October 3 compact-Tasks update makes component modeling forms usable at
360 logical pixels with vertical scrolling only. Seventeen focused width and
workflow checks pass; the Python-only owner payload retains the preceding
native build. See WORK_STATE for delivery, provenance and visual evidence.

The October 3 sketch-feedback build fixes ribbon panel colors, unfilled sketches,
temporary blue profile regions, interior curve collection and sketch reuse after
Extrude deletion. The 25 selected checks and owner-shortcut verification pass;
see WORK_STATE for the current payload and source/native provenance.

The October 3 fresh owner build compiles all enabled targets and stages source/native
identity `f8a4d5c408`; 22 focused runtime/startup checks and the desktop shortcut
verification pass. See WORK_STATE for the latest payload and evidence.

Component Primitive, Helix, Pipe and Loft now combine their native additive/subtractive features
through `src/Mod/Part/ComponentPrimitive.py` / `ComponentHelix.py` / `ComponentPipe.py` / `ComponentLoft.py` and
their corresponding `src/Gui/ComponentHelixTask.py` / `ComponentPipeTask.py` /
`ComponentLoftTask.py` tasks.
`ComponentNativeOperation.py` owns their common binding and transactional lifecycle;
`ComponentSectionTask.py` owns ordered section collection. `ComponentTaskWidgets.py`
shares the collector, selection/display controller and common UI controls.
`ComponentOperationTask.py` retains the common lifecycle and axis-picking adapter. Primitive retains native dimensions, placement and attachment in
`ComponentPrimitiveTask.py`. The grouped native command build and routing tests pass;
owner delivery is recorded in WORK_STATE. See [Primitive acceptance](../tests/ComponentPrimitive.md), [Pipe acceptance](../tests/ComponentPipe.md),
[Loft acceptance](../tests/ComponentLoft.md), [Helix acceptance](../tests/ComponentHelix.md)
and current WORK_STATE.

FreeCAD Plus is Croft-Labs' FreeCAD fork, a desktop parametric CAD application
using C++, Python, Qt, OpenCASCADE, and Coin; the GUI executable enters through
[`src/Main/MainGui.cpp`](../src/Main/MainGui.cpp).

The delivered October 3 batch combines Revolution/Groove as component Revolve, implemented in
`src/Mod/Part/ComponentRevolve.py` and `src/Gui/ComponentRevolveTask.py`. It reuses
native geometry and the shared modeling curve collector; native command and Model History
routes share the four-section task. Acceptance: `tests/TestComponentRevolve.py`.
The batch also incorporates the shared Datum Plane workflow: Define Surface, Z Direction,
Sketch Origin and X Direction, with immediate availability as a New Sketch attachment.
See the roadmap and WORK_STATE for verification and owner-delivery status.

Latest source follows the owner's exact Design Home, Modeling, Sketch, Assembly and View layouts. Modeling
has Sketch, Modeling, Dress-Up, Transformation and one Primitives dropdown;
additive/subtractive operations use one icon. Tab is a disabled future primitive.
Sketch retains the complete seven-group outline, 16 ordered dropdowns and all
listed individual button options. Assembly exposes all joints individually with
three ordered dropdowns; its edit-exit task-watcher guard is packaged and validated.
Design View has exactly View and Individual Views, with ordered Standard Views and
Draw Style menus. Word requirements are synchronized. These revisions, master-first
component trees and screenshot defaults are in the October 2 batched owner payload.

The October 2 component-feedback batch incorporates application sources through `4cbb196bee`.
Five compatible Python modules were synchronized onto native engine `6be8eda4246a`;
no native sources changed. Acceptance retains 57 passing checks without overlays,
including actual curve creation/save/reopen and three launcher cold restarts.
Two obsolete test assumptions were corrected and their checks rerun. The physical
sketch drawing report remains unresolved. WORK_STATE owns delivery paths and evidence.

The preceding October 2 audit build incorporated the conversation's UI/workflow
changes, including the common toolbar above the ribbon, medium icons, completed
Home groups, Design Assembly tab and unplaced New Component action. Its application
sources are `ca244c0335`; it reuses the validated native engine at `6be8eda4246a`
and synchronizes two compatible GUI Python modules without a C++ rebuild.

Packaged acceptance passes 131 executions without failures/errors/skips or source
overlays: ribbon and every installed mode, component tabs/tree/naming/background
results, selected-profile Extrude, complete sketch workflow/cold reopen, startup
panes/Tasks/recent files/status and three actual owner-launcher cold restarts.
Plus/Blender/Imperial Decimal defaults preserve saved choices. Hidden-window
specialist initialization was corrected to preserve Classic toolbar visibility.
The desktop owner shortcut now points to the latest batch; root AGENTS.md makes its
verified update mandatory for every delivered owner build.

The [toolbar reference](ui/TOOLBARS.md) separates Classic command rows,
implemented Plus groups and the final 644-command function catalog with 616 native
icon renders. The [conversation audit](DEVELOPMENT_ROADMAP.md#october-2-conversation-and-payload-audit)
maps each request to incorporation/evidence. [WORK_STATE](WORK_STATE.md) owns exact
source/native identities, launcher/ZIP paths, shortcut verification, file hashes
and retained acceptance limits.

Earlier October 2 builds remain intact. Baseline native ALL_BUILD and 138
executions (136 distinct checks) remain recorded separately; they are not a new
native build/test claim. Start and Tux remain enabled; FEM remains disabled.
This is an unsigned local test build ready for owner testing. Physical owner
acceptance, upstream candidate integration and external publication are separate.

## Where to go

| Task or question | Start here | Related reference |
| --- | --- | --- |
| Owner UI requirements and defaults | [FreeCAD Plus UI & UX.docx](ui/FreeCAD%20Plus%20UI%20%26%20UX.docx), [`PlusDefaults.py`](../src/Gui/PlusDefaults.py) | Mandatory update for every owner change; preserve DOCX headings and automatic numbering. October 2 screenshot preset covers General, Selection, Display Colors and Sketcher Appearance. |
| Plus UI / Classic UI | [Toolbar governance and visual catalog](details/ui/TOOLBARS.md), [`PlusRibbon.py`](../src/Gui/PlusRibbon.py), [`DlgSettingsGeneral.cpp`](../src/Gui/PreferencePages/DlgSettingsGeneral.cpp) | Workbench groups, upstream-to-Plus consolidations, icons and functions; [shared UI rules](UI_UX_SPEC.md#toolbar-ui-styles); [owner procedure](../tests/PlusRibbon.md). |
| Reviewed face extension (F066) | [`ExtendFaceReview.py`](../src/Mod/Surface/ExtendFaceReview.py), [`ExtendFaceGui.py`](../src/Mod/Surface/ExtendFaceGui.py), native `Surface::Extend` | Existing Surface Extend Face command: explicit U/V approximation, view-only preview and transactional associative creation. [Owner procedure](../tests/ExtendFaceReview.md); roadmap 13.1e/f owns validation. |
| Joint motion/limit review (F076) | [`JointObject.py`](../src/Mod/Assembly/JointObject.py), native Assembly joint task | Relative-motion guidance, exact reference tooltips and enabled-limit refusal/recovery before solver normalization. [Owner procedure](../tests/JointReview.md); roadmap 12.4c/d. |
| Window/crossing selection (F039) | [`BoxSelection.cpp`](../src/Gui/Selection/BoxSelection.cpp), [`MouseSelection.cpp`](../src/Gui/MouseSelection.cpp) | Full projected enclosure, directional borders and filter-aware native collection. [Owner procedure](../tests/WindowSelection.md); roadmap 10.5g/h. |
| Entity selection filters (F035) | [`EntitySelectionFilter.py`](../src/Gui/EntitySelectionFilter.py), native [`Selection.cpp`](../src/Gui/Selection/Selection.cpp) | View > Visibility > Selection filters: session vertex/edge/face/whole-object policy, command-gate intersection and visible reset. [Owner procedure](../tests/EntitySelectionFilter.md); roadmap 10.5e/f owns validation. |
| Component document architecture | [Approved component contract](architecture/COMPONENT_DOCUMENT_CONTRACT.md) | Active owner priority: roadmap 7.8; Models, Part Tree, History, Attributes and `.cadprt` |
| Master component and unused assemblies | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py), [`TestComponentModelsPane.py`](../tests/TestComponentModelsPane.py) | Permanent automatic first component; master-first inventory/tree independent of edit context; unused assemblies retain their child trees. Packaged verification passes in the latest October 2 batch. |
| Part Tree rearrangement | [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py), [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py) | Cut/Paste and drag/drop of existing instances, ordering/reparenting, placement and reference guards; roadmap 7.8.7x; [`TestComponentTreeMove.py`](../tests/TestComponentTreeMove.py). |
| Origin and planes in History | [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py), native [`CommandDoc.cpp`](../src/Gui/CommandDoc.cpp) | Permanent Origin / hidden-by-default Origin Planes child, grouped native plane visibility and deletion protection; roadmap 7.8.7y; [`TestComponentModelsPane.py`](../tests/TestComponentModelsPane.py). |
| Component BOM participation | [`BomObject.cpp`](../src/Mod/Assembly/App/BomObject.cpp), [`CommandCreateBom.py`](../src/Mod/Assembly/CommandCreateBom.py), component model/navigator | Native BOM scope, occurrence inclusion, owning-file history editor and saved report policies; roadmap 7.8.7j. |
| Component display contexts | [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py), [`TestComponentDisplayContext.py`](../tests/TestComponentDisplayContext.py) | Background/isolated-view refresh, occurrence highlighting, Part View indications and history availability; roadmap 7.8.7i. |
| Component owning-file Undo/Redo | Native [`View3DInventor.cpp`](../src/Gui/View3DInventor.cpp), [`MDIView.cpp`](../src/Gui/MDIView.cpp), [`DlgUndoRedo.cpp`](../src/Gui/Dialogs/DlgUndoRedo.cpp), History | Consistent owning-file execution, enabled states/history menus and deferred navigator refresh; roadmap 7.8.5f owns build and feedback status. |
| Component owning-file saves | Native [`View3DInventor.cpp`](../src/Gui/View3DInventor.cpp), [`CommandDoc.cpp`](../src/Gui/CommandDoc.cpp), [`Document.cpp`](../src/Gui/Document.cpp) | Save/Save As/Save Copy follow the active component owner while retaining view context; roadmap 7.8.3d owns build and feedback status. |
| Component modeling task transitions | [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py), [`ComponentExtrudeTask.py`](../src/Gui/ComponentExtrudeTask.py), [`ComponentSketchTask.py`](../src/Gui/ComponentSketchTask.py) | Preserve originating view/occurrence across owning-file task entry/exit and resolve local profile/face preselection; roadmap 7.8.7h. |
| Cross-file component editing | [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py), [`ComponentSelection.py`](../src/Gui/ComponentSelection.py) | Exact active occurrence in the assembly view, tab/Undo restoration, missing-link fallback and isolated owning-file titles; roadmap 7.8.7g. |
| Save to External File feedback | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py) | Shared hierarchy/name preservation, current reference history, preflight and occurrence-context restoration; roadmap 7.8.8d; [owner procedure](../tests/ComponentDocument.md). |
| Component model and navigators | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py), [`ComponentResultView.py`](../src/Mod/Part/ComponentResultView.py) | Shared definitions, protected background solid results, references, representations and isolated views; [architecture decision](architecture/ADR_003_COMPONENT_DOCUMENT.md). |
| History suppression | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), History | Dependent branch/result restoration, shared-consumer visibility, bulk single-Undo changes and blocking-input tooltips; roadmap 7.8.5e. Native recompute scheduling remains open. |
| Component geometry conversion | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), History Convert to Dumb Object | Read-only removal/retention review, geometry-only exclusive-history pruning, identity-preserving freezing and independent extraction; roadmap 7.8.6c. |
| Component instance separation | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py) | Copy to New Part retains occurrence references, nested display choices and active edit context; geometry-only dependency eligibility; roadmap 7.8.8c. |
| Component file recovery | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), Component Structure, native `PropertyXLink` | Grouped missing instances, identity-based Locate Component File, partial reference recovery and clearing obsolete saved link targets; roadmap 7.8.3c. |
| Component reference recovery | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), [`CadDocument.py`](../src/Mod/Part/CadDocument.py), History | Repairable missing geometry, independent refresh and identity-preserving direct-child source repair; roadmap 7.8.4a. |
| Component selection and view context | [`ComponentSelection.py`](../src/Gui/ComponentSelection.py), [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py) | Native occurrence-path selection, direct-child reference preselection, grouped display Undo and isolated-tab context; roadmap 7.8.7f. |
| Independent component sketches and datum planes | [`ComponentSketch.py`](../src/Mod/Part/ComponentSketch.py), [`ComponentSketchTask.py`](../src/Gui/ComponentSketchTask.py), [`ComponentPlane.py`](../src/Mod/Part/ComponentPlane.py), [`ComponentPlaneTask.py`](../src/Gui/ComponentPlaneTask.py) | Datum-plane create/edit uses shared mixed-reference collectors, associative geometry or numeric normal/position, projected X/origin and purple preview. Sketch support and independent frames remain available; roadmap 7.8 datum-plane milestone; [validation procedure](../tests/SketchWorkflow.md). |
| Component Extrude feedback task | [`ComponentExtrude.py`](../src/Mod/Part/ComponentExtrude.py), [`ComponentExtent.py`](../src/Mod/Part/ComponentExtent.py), [`ComponentProfile.py`](../src/Mod/Part/ComponentProfile.py), [`ComponentExtrudeTask.py`](../src/Gui/ComponentExtrudeTask.py), native Part Design command routing | Independent New Body/Add/Subtract/history workflow, associative selected curves/regions, native extent/offset/taper/direction controls and colored volume previews; roadmap 7.8.5c/d, 7.8.7d/e/p/q. |
| Product intent and boundaries | [Product specification](PRODUCT_SPEC.md) | [UI scope](UI_UX_SPEC.md#interface-scope) |
| `.cadprt` persistence and legacy conversion | [`CadDocument.py`](../src/Mod/Part/CadDocument.py), native App/Gui document save/open | Versioned manifest with native payloads; automatic GUI conversion, untouched originals and reported limitations. Roadmap 7.8; [owner procedure](../tests/ComponentDocument.md). |
| Part-level history architecture | [Logical history/result contract](architecture/PART_HISTORY_CONTRACT.md), [adapter decision boundary](architecture/ADR_001_HISTORY_ADAPTER_BOUNDARY.md) | Historical probes; ADR 003 selects the initial production mapping. General lineage and remaining acceptance are tracked in 7.8 |
| Sketch support editor (F124) | [`SketchSupport.py`](../src/Mod/Sketcher/SketchSupport.py), [`SketchSupportGui.py`](../src/Mod/Sketcher/SketchSupportGui.py) | Sketcher > Sketch > Inspect and change sketch support: native planar reattachment, local/world numeric preview and undoable repair. [Owner procedure](../tests/SketchSupport.md); roadmap 11.7y/z. |
| Shell Thickness (F059) | [`TaskThickness.cpp`](../src/Mod/Part/Gui/TaskThickness.cpp), native Thickness in [`PartFeatures.cpp`](../src/Mod/Part/App/PartFeatures.cpp) | Removed-face review, signed side and recoverable acceptance. [Owner procedure](../tests/ShellThickness.md); roadmap 13.5g/h owns validation. |
| Sketch Trim gestures (F050) | [`DrawSketchHandlerTrimming.h`](../src/Mod/Sketcher/Gui/DrawSketchHandlerTrimming.h), existing Sketcher Trim tool | One Undo step per drag, cancellation rollback and native removed/replaced-constraint summary. [Owner procedure](../tests/TrimGesture.md); roadmap 11.6e/f owns validation. |
| Sketch reuse (F053) | [`SketchReuse.py`](../src/Mod/Sketcher/SketchReuse.py), [`SketchReuseGui.py`](../src/Mod/Sketcher/SketchReuseGui.py) | Sketch > Copy reusable sketch: native independent whole-sketch copy, preserved internal constraints, typed source-frame placement and view-only preview. [Owner procedure](../tests/SketchReuse.md); roadmap 11.6c/d. |
| Native state columns (F013) | [`FeatureOrganizer.py`](../src/Gui/FeatureOrganizer.py), Tools > Find and describe features | Read-only visibility/suppression/status/source/metadata columns, state filters and explicit snapshot refresh. [Owner procedure](../tests/FeatureStateColumns.md); roadmap 10.6d/e owns validation status. |
| Saved project packaging (F108) | [`ProjectPackage.py`](../src/Gui/ProjectPackage.py), Tools > Package saved project | Review recursive native relative links and create a byte-preserving ZIP with portable manifest. [Owner procedure](../tests/ProjectPackage.md); roadmap 15.6a/b owns validation status. |
| Fillet/chamfer recovery (F058) | [`DlgFilletEdges.cpp`](../src/Mod/Part/Gui/DlgFilletEdges.cpp), native FeatureFillet/FeatureChamfer | Existing Part edge tasks retain choices after failed acceptance; copied kernel inputs preserve source topology. [Owner procedure](../tests/EdgeTreatmentRecovery.md); roadmap 13.5e/f owns validation. |
| Hole specification review (F055) | [`TaskHoleParameters.cpp`](../src/Mod/PartDesign/Gui/TaskHoleParameters.cpp), existing Part Design Hole task | Profile/Body identity, native location readiness and explicit clearance/tap-drill/cosmetic/modeled thread semantics. [Owner procedure](../tests/HoleSpecification.md); roadmap 13.5c/d owns validation status. |
| Captured Sweep inputs (F028) | [`TaskSweep.cpp`](../src/Mod/Part/Gui/TaskSweep.cpp), native Part Sweep task | Explicit retained path, ordered sections, solid/surface frame review and atomic recoverable creation. [Owner procedure](../tests/SweepInputs.md); roadmap 13.2c/d owns validation status. |
| Ordered Loft sections (F063) | [`TaskLoft.cpp`](../src/Mod/Part/Gui/TaskLoft.cpp), existing Part Loft task | Native open-wire/edge collection, explicit ordered solid/surface review and atomic validated creation. [Owner procedure](../tests/LoftSections.md); roadmap 13.2a/b. |
| Assembly freedom guidance (F077) | [`TaskAssemblyMessages.cpp`](../src/Mod/Assembly/Gui/TaskAssemblyMessages.cpp), existing solver panel | Native grounding/connectivity selection and explicit assembly-wide freedom scope. [Owner procedure](../tests/AssemblyFreedom.md); roadmap 12.4a/b. |
| Drawing dimension repair (F103) | [`TaskDimRepair.cpp`](../src/Mod/TechDraw/Gui/TaskDimRepair.cpp), native TechDraw_DimensionRepair | Reviewed projected/true reference handoff, recompute before commit and recoverable failure. [Owner procedure](../tests/DimensionRepair.md); roadmap 15.3c/d. |
| Sketch freedom guidance (F047) | [`TaskSketcherMessages.cpp`](../src/Mod/Sketcher/Gui/TaskSketcherMessages.cpp), existing sketch edit task | Solver-state explanation and native unconstrained-geometry selection; [owner procedure](../tests/SketchFreedom.md), roadmap 11.4c/d. |
| Sketch constraint repair (F048) | [`ConstraintRepair.py`](../src/Mod/Sketcher/ConstraintRepair.py), [`ConstraintRepairGui.py`](../src/Mod/Sketcher/ConstraintRepairGui.py) | Sketch > Review constraint repair: isolated native-copy diagnosis and deactivation preview, retained constraint identity, explicit transactional Apply. [Owner procedure](../tests/ConstraintRepair.md); roadmap 11.4a/b owns acceptance status. |
| Move/copy occurrence (F072/F074) | [`OccurrenceMove.py`](../src/Gui/OccurrenceMove.py), standard Tools menu | One-time movement or one new shared-definition Link at a reviewed world/occurrence transform. [Owner procedure](../tests/OccurrenceMove.md); roadmap 10.7a-d. |
| Occurrence replacement (F022) | [`OccurrenceReplace.py`](../src/Gui/OccurrenceReplace.py), standard Tools menu | One unconstrained Link, same-document root solid/Body, preserved placement/appearance, native source reuse and view-only preview. [Owner procedure](../tests/OccurrenceReplace.md); roadmap 12.6a/b. |
| Reviewed intersection curves (F069) | [`SectionReview.py`](../src/Mod/Part/SectionReview.py), [`SectionReviewGui.py`](../src/Mod/Part/SectionReviewGui.py) | Part > Review intersection curves: explicit root-shape inputs, isolated native Section preview, empty-result disclosure and transactional associative creation. [Owner procedure](../tests/SectionReview.md); roadmap 13.4a/b owns validation status. |
| Sampled surface deviation (F071) | [`SurfaceDeviation.py`](../src/Mod/Part/SurfaceDeviation.py), [`SurfaceDeviationGui.py`](../src/Mod/Part/SurfaceDeviationGui.py) | Part > Sampled face deviation: explicit sampled/reference faces, native unsigned distances, temporary color map and saved grid/scale. [Owner procedure](../tests/SurfaceDeviation.md); roadmap 15.2a/b owns validation status. |
| Select Other / Clarify Selection (F037) | [`SelectionView.cpp`](../src/Gui/Selection/SelectionView.cpp), native Std_ClarifySelection | Existing ray-pick menu preserves equal-label occurrence identities, displays full context and respects native command gates. [Owner procedure](../tests/ClarifySelection.md); roadmap 10.5c/d owns validation status. |
| Sheet thickening (F067) | [`FeatureOffset.cpp`](../src/Mod/Part/App/FeatureOffset.cpp), [`TaskOffset.cpp`](../src/Mod/Part/Gui/TaskOffset.cpp) | Existing Part > 3D Offset: signed one-sided thickness, reversal, solid/sheet feedback and recoverable failed acceptance. Native associative feature; [owner procedure](../tests/SheetThickening.md), roadmap 13.1c/d owns acceptance status. |
| Shape Builder sewing (F068) | [`ShapeSewing.py`](../src/Mod/Part/ShapeSewing.py), [`TaskShapeBuilder.cpp`](../src/Mod/Part/Gui/TaskShapeBuilder.cpp) | Existing shell/solid modes: explicit tolerance, nonmutating boundary/classification checks, independent snapshots and closed-solid validation. [Owner procedure](../tests/ShapeSewing.md); roadmap 13.1a/b. |
| Manufacturing export (F127) | [`ManufacturingExport.py`](../src/Mod/Part/ManufacturingExport.py), [`ManufacturingExportGui.py`](../src/Mod/Part/ManufacturingExportGui.py) | Part > Manufacturing export: explicit solid/occurrence inputs, STL mm/world coordinates, reusable quality and stale-input guards. [Owner procedure](../tests/ManufacturingExport.md); roadmap 15.7a/b. |
| Temporary isolate/hide (F040) | [`TemporaryDisplay.py`](../src/Gui/TemporaryDisplay.py), standard View > Visibility menu | Native visibility with per-document nested restore; whole Body/link targets preserve model identities. [Owner procedure](../tests/TemporaryDisplay.md); roadmap 10.5a/b. |
| Command search and local help (F033/F123) | [`CommandSearch.py`](../src/Gui/CommandSearch.py), native standard Tools menu | Familiar aliases into existing commands, thirteen offline workflow guides, native live availability, F1/Ctrl+L navigation, scrollable details and window-only layout reset. [Owner procedure](../tests/CommandSearch.md); roadmap 8.4.2a/b, 10.4, 10.9a/b. |
| Named parameters (F122) | [`NamedParameters.py`](../src/Mod/Part/NamedParameters.py), [`NamedParameterGui.py`](../src/Mod/Part/NamedParameterGui.py) | Part > Named parameters for an explicitly selected native Part or marked set. Native length/angle expressions, rename, transactions and persistence; same-document reference copying. [Owner procedure](../tests/NamedParameters.md); roadmap 10.8aa/ab. |
| Parameter acceptance and enclosure | [`TestNamedParameterCommand.py`](../tests/TestNamedParameterCommand.py), [`TestParameterEditor.py`](../tests/TestParameterEditor.py), [`TestPartHistoryCapabilities.py`](../tests/TestPartHistoryCapabilities.py) | Installed command plus native geometry/recovery/persistence checks. `tests/prototypes/ParameterEnclosure.py` supplies the enclosure; former parameter prototype imports now forward to application modules. Broader scope/publication/where-used remains pending. |
| Creation suggestions and saved operation intent | [ADR 002](architecture/ADR_002_CREATION_INTENT.md), [product contract](PRODUCT_SPEC.md#planned-creation-and-interaction-contracts) | Test-only single-part solid prototype passes; installed Extrude/Revolve migration remains pending |
| Pad creation without preselection | [`Command.cpp`](../src/Mod/PartDesign/Gui/Command.cpp), `CmdPartDesignPad::activated` and `prepareProfileBased` | [Pad UI](UI_UX_SPEC.md#ui-001-pad-task-pane) |
| Unified Extrude command and Add/Subtract | [`Command.cpp`](../src/Mod/PartDesign/Gui/Command.cpp), `CmdPartDesignExtrude`; [`TaskPadParameters.cpp`](../src/Mod/PartDesign/Gui/TaskPadParameters.cpp), shared by Pad/Pocket | [Extrude UI](UI_UX_SPEC.md#ui-001-pad-task-pane) |
| Combined Linear/Circular Pattern | [`FeaturePattern.cpp`](../src/Mod/PartDesign/App/FeaturePattern.cpp), [`TaskMultiTransformParameters.cpp`](../src/Mod/PartDesign/Gui/TaskMultiTransformParameters.cpp), `CmdPartDesignPattern` | [Pattern UI](UI_UX_SPEC.md#ui-002-pattern-task-pane), [tests](../tests/PatternTaskPanel.md) |
| Revolve/Groove angular start offset | [`TaskRevolutionParameters.cpp`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.cpp), [`FeatureRevolved.cpp`](../src/Mod/PartDesign/App/FeatureRevolved.cpp) | [Shared angular controls](UI_UX_SPEC.md#ui-003-revolve-and-groove-angular-controls), [tests](../tests/RevolveTaskPanel.md) |
| Extrude start offset and direction buttons | [`TaskExtrudeParameters.cpp`](../src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp), [`TaskPadPocketParameters.ui`](../src/Mod/PartDesign/Gui/TaskPadPocketParameters.ui) | [Shared UI](UI_UX_SPEC.md#ui-001-pad-task-pane), [GUI regressions](../src/Mod/PartDesign/PartDesignTests/TestExtrudeTaskPanel.py) |
| Extrude extent semantics and face repair | `TaskExtrudeParameters::updateWholeUI`, `onFaceName`; `TaskSketchBasedParameters::setUpToFace` | Total/per-side labels and explicit typed-face destination; F029 regressions in `TestExtrude` and `TestExtrudeTaskPanel`, roadmap 8.1.4a/b. `changeFaceName` invalidates empty/malformed limits; explicit-target `setUpToFace` applies typed planes during preview (8.1.4c/d). End-limit typing/picking reuse `NoDependentsSelection` and plane ownership uses `ReferenceSelection` (8.1.4e/f). |
| Operation persistence and geometry | [`FeatureExtrude.cpp`](../src/Mod/PartDesign/App/FeatureExtrude.cpp), `setupExtrusionOperations`, `computeDirection`, `buildExtrusion` | [Regressions](../src/Mod/PartDesign/PartDesignTests/TestExtrude.py) |
| Extrude profile list and selection | [`TaskPadParameters.cpp`](../src/Mod/PartDesign/Gui/TaskPadParameters.cpp), `TaskPadParameters`, `ExtrudeProfileSelection` | [Extrude UI](UI_UX_SPEC.md#ui-001-pad-task-pane) |
| Reopen an existing Pad | [`ViewProviderPad.cpp`](../src/Mod/PartDesign/Gui/ViewProviderPad.cpp), `getEditDialog` | [Requirements](PRODUCT_SPEC.md#capabilities-and-requirements) |
| Trim Body geometry and shared create/edit pane | [`TrimAPI.py`](../src/Mod/Part/BOPTools/TrimAPI.py), [`TrimFeatures.py`](../src/Mod/Part/BOPTools/TrimFeatures.py), [`TrimGui.py`](../src/Mod/Part/BOPTools/TrimGui.py) | [Trim Body UI](UI_UX_SPEC.md#ui-004-trim-body-task-pane), [tests](../tests/TrimBody.md) |
| Isocline Curves | [`Isocline.py`](../src/Mod/Part/BasicShapes/Isocline.py), [`IsoclineGui.py`](../src/Mod/Part/BasicShapes/IsoclineGui.py), `Part.makeIsocline` in [`AppPartPy.cpp`](../src/Mod/Part/App/AppPartPy.cpp) | [Isocline UI](UI_UX_SPEC.md#ui-005-isocline-curve-task-pane), [tests](../tests/IsoclineCurve.md) |
| STL CAM and stock bridges | [`MeshModel.py`](../src/Mod/CAM/Path/Main/MeshModel.py), [`PlanarSurface.py`](../src/Mod/CAM/Path/Op/PlanarSurface.py), [`HoldingTab.py`](../src/Mod/CAM/Path/Main/HoldingTab.py) | [CAM UI](UI_UX_SPEC.md#ui-006-cam-mesh-machining-and-tabs), [validation](../tests/CAMMeshMachining.md) |
| CAM model setup review (F090) | [`JobDlg.py`](../src/Mod/CAM/Path/Main/Gui/JobDlg.py), existing New Job and Model Selection | Exact source identity, separate mesh candidates and read-only source size/unit review before native job setup. [Owner procedure](../tests/JobModelReview.md); roadmap 14.1c/d owns validation status. |
| CAM simulation input review (F095) | [`SimulationReview.py`](../src/Mod/CAM/Path/Main/SimulationReview.py), [`SimulatorGL.py`](../src/Mod/CAM/Path/Main/Gui/SimulatorGL.py) | Existing CAM Simulator shows stock/tool/operation scope, prepares all inputs before reset, preserves tool-change order and invalidates review after edits. [Owner procedure](../tests/SimulationReview.md); roadmap 14.3a/b owns validation status. |
| CAM setup templates (F096) | [`Template.py`](../src/Mod/CAM/Path/Main/Template.py), [`JobDlg.py`](../src/Mod/CAM/Path/Main/Gui/JobDlg.py), native Job/JobCmd | Export name/revision and review stored settings in New Job; preflight compatibility, exact post/accepted settings, native stock/tool reuse. [Owner procedure](../tests/SetupTemplates.md); roadmap 14.4a/b owns validation status. |
| Mesh preparation (F091) | [`MeshPreparation.py`](../src/Mod/CAM/Path/Main/MeshPreparation.py), [`GUI review`](../src/Mod/CAM/Path/Main/Gui/MeshPreparation.py) | CAM > Review CAM mesh: bounded topology/orientation/dimension review and independent reversed-normal copy. Native transactions and mesh data; [owner procedure](../tests/MeshPreparation.md), roadmap 14.1a/b. |
| Saved exploded-view output (F080) | [`CommandCreateView.py`](../src/Mod/Assembly/CommandCreateView.py), existing Assembly task and TechDraw consumer | Copied occurrence geometry preserves definition/parent transforms; successive trails and radial preview agree. [Owner procedure](../tests/ExplodedViewOutput.md); roadmap 12.7a/b owns validation status. |
| Assembly BOM inclusion (F104) | [`BomObject.cpp`](../src/Mod/Assembly/App/BomObject.cpp), [`CommandCreateBom.py`](../src/Mod/Assembly/CommandCreateBom.py) | Existing native BOM: assembly-group scope, per-parent quantities and per-BOM exclusions independent of visibility. [Owner procedure](../tests/AssemblyBomScope.md); roadmap 15.4a/b owns validation status. |
| Indexed STL CAM output | `Path/Main/IndexedSetup.py::require_current_geometry`, `Path/Op/Base.py::_bindModelDependencies` | Consume recomputed indexed producers and schedule stock dependencies; real-job LinuxCNC/Grbl output regressions in `tests/TestIndexedSetupExport.py`, roadmap 6.4.3. Native viewport/simulation remain separate. |
| Build or verify changes | [Development guide](DEVELOPMENT_GUIDE.md#commands) | [Pad test procedure](../tests/PadTaskPanel.md) |
| Priorities, completion, and blockers | [Roadmap](DEVELOPMENT_ROADMAP.md) | [Current focus](DEVELOPMENT_ROADMAP.md#current-focus) |
| Upstream integration and fork compatibility | [October 7 commit audit](DEVELOPMENT_ROADMAP.md#october-7-upstream-integration) | Integrated upstream through `e326ee2f07`; adapted CAM safety/frames and native pattern controls; next grouped native build remains pending. |
| Important upstream issues | [Prioritized issue watchlist](FREECAD_ISSUES.md) | [Issue work and pending validation](DEVELOPMENT_ROADMAP.md#upstream-issue-work) |
| Recovery, numeric input and tree regressions | [Issue validation procedure](../tests/UpstreamIssues.md) | Isolated existing-build checks; no real user documents |
| CAM dressup input readiness | [`Utils.py`](../src/Mod/CAM/Path/Dressup/Utils.py), `requireCurrent` | Array, Mirror, Axis Map, Z Correction, Boundary/Boundary2, Tags, Dragknife, Ramp Entry Plunge Milling and Dogbone reject invalid/touched recursive inputs; native skipped execution can retain an export-blocked cache. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2au/av and 16.2bc-bl. |
| CAM Boundary2 failure handling | [`Boundary2.py`](../src/Mod/CAM/Path/Dressup/Gui/Boundary2.py), `ObjectDressup.execute` | Clear old path before generation, require valid solid offsets, use native command Z for links and omit moves for empty clipping; export/recovery [regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2as/at and 16.2ba/bb. |
| CAM holding-tag failures | [`Tags.py`](../src/Mod/CAM/Path/Dressup/Tags.py), `ObjectTagDressup.doExecute` | Clear cached path/preview data before validation; processing errors propagate instead of falling back to untagged base. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2aq/ar. |
| CAM direct holding-tag edits | [`Tags.py`](../src/Mod/CAM/Path/Dressup/Tags.py), `processTags`, `setXyEnabled` | Direct processing clears old output; position edits refresh/validate input before changing saved positions. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2aw/ax. |
| CAM holding-tag setup and point queries | [`Tags.py`](../src/Mod/CAM/Path/Dressup/Tags.py), `setup`, `pointIsOnPath`, `pointAtBottom` | Reset caches, validate tool/input readiness and refresh query path data; [regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2ay/az. |
| CAM stale paths after invalid inputs | [`Path/Op/Base.py`](../src/Mod/CAM/Path/Op/Base.py), `ObjectOp.execute`; [`Job.py`](../src/Mod/CAM/Path/Main/Job.py), `onChanged` | Clear previous Path before validation; ModelDependencies schedule whole-model recompute, restore and model-container replacement. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2b-g; broader failure/export gates remain open |
| CAM operation property and job traversal | [`Base/Util.py`](../src/Mod/CAM/Path/Base/Util.py), `opProperty`; [`Job.py`](../src/Mod/CAM/Path/Main/Job.py), `allOperations` | Iterative property inheritance with cycle errors; ordered unique job traversal for invalidation/cleanup. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2am/an. |
| CAM shared dressup base lookup | [`Utils.py`](../src/Mod/CAM/Path/Dressup/Utils.py), `_isDressup`, `baseOp`, `toolController` | Current proxy recognition with guarded legacy fallback; iterative cycle rejection, disconnected-chain handling and ordinary-operation boundaries. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2ak/al. |
| CAM Plunge Milling input/failure validation | [`PlungeMilling.py`](../src/Mod/CAM/Path/Dressup/Gui/PlungeMilling.py), `execute` | Clear prior output, validate stepover/feed, establish clearance and emit explicit cycle feed/cancellation. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2ai/aj and 16.2bm-br (cycle variants, bounded LinuxCNC/Grbl export and reopen checks). |
| CAM Dragknife/Ramp Entry failure cleanup | [`Dragknife.py`](../src/Mod/CAM/Path/Dressup/Gui/Dragknife.py), [`RampEntry.py`](../src/Mod/CAM/Path/Dressup/Gui/RampEntry.py), `execute` | Clear old output before validation/generation. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2ag/ah. |
| CAM Z Correction probe validity | [`ZCorrect.py`](../src/Mod/CAM/Path/Dressup/Gui/ZCorrect.py), `_getinterpSurface` and `execute` | Clear old path/surface; reject unusable/non-finite probes, out-of-area corrections and invalid interpolation settings; honor source-line subdivision length; preserve probe precision and reject conflicting duplicate heights. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2aa-af and 16.2ao/ap. |
| CAM Axis Map validation | [`AxisMap.py`](../src/Mod/CAM/Path/Dressup/Gui/AxisMap.py), `ObjectDressup.execute` | Clear cached output before conversion and require a positive finite wrap radius. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2x/y. |
| CAM Mirror placement and output isolation | [`Mirror.py`](../src/Mod/CAM/Path/Dressup/Gui/Mirror.py), `ObjectDressup.execute` | Preserve placed passthrough, copy base paths before modification, and publish only completed output. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2u-w. |
| CAM Array/Dogbone failure recovery | [`Array.py`](../src/Mod/CAM/Path/Dressup/Array.py), [`DogboneII.py`](../src/Mod/CAM/Path/Dressup/DogboneII.py), `execute` | Clear previous machining output before generation; Dogbone also clears corner caches. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2s/t. |
| CAM boundary dressup failure/recovery | [`Boundary.py`](../src/Mod/CAM/Path/Dressup/Boundary.py), `DressupPathBoundary.execute` | Clear cached paths before offset/clipping; reject missing/non-geometric/null masks and empty/invalid offsets; native missing-base empty path. [Regressions](../tests/TestCAMInvalidInputs.py), roadmap 16.2o-r. |
| CAM face-avoidance failures | [`surface_common.py`](../src/Mod/CAM/Path/Base/Generator/surface_common.py), [`PlanarSurface.py`](../src/Mod/CAM/Path/Op/PlanarSurface.py) | Stop generation rather than omit exclusions; [regressions](../tests/TestIssueSurfaceAvoidance.py) |
| CAM dirty/failed-input export guard | [`PostList.py`](../src/Mod/CAM/Path/Post/PostList.py), `_wrap_op` | Reject native dirty/invalid operations and recursive inputs before cached-path export; roadmap 16.2h/i and [regressions](../tests/TestCAMInvalidInputs.py). General semantic/export compatibility remains open |
| Freeform CAM projection stalls | [`surface_common.py`](../src/Mod/CAM/Path/Base/Generator/surface_common.py), `_boundary_via_mesh` | Tolerance-based cutting silhouette; [geometry regressions](../tests/TestIssueFreeformBoundary.py), [opt-in fixture](../tests/TestIssue26300Fixture.py); roadmap U.23 |
| Mirror reference placement | [`FeatureMirroring.cpp`](../src/Mod/Part/App/FeatureMirroring.cpp), [`TestPartMirror.py`](../src/Mod/Part/parttests/TestPartMirror.py) | Issue #32706 fixed locally; geometry, persistence and task selection pass in 75-test batch |
| Resume the build-validation closeout | [Shutdown handoff](WORK_STATE.md) | Completed build/tests and remaining native acceptance gates |
| Development policy and future architecture | [Adopted guidelines](DEVELOPMENT_GUIDELINES.md) | [Baseline mapping](DEVELOPMENT_ROADMAP.md#planning-baseline-adoption), [future contracts](PRODUCT_SPEC.md#future-architecture-direction) |
| Agent instructions | [Root entry point](../AGENTS.md) | [Shared standard](../../ai-instructions/AGENTS_TEMPLATE.md) |

## Folder and module map

Precise occurrence movement (F074; bounded F072/F075): [`OccurrenceMove.py`](../src/Gui/OccurrenceMove.py)
provides Tools > Move occurrence once with explicit world/link frames, translation,
pivot rotation and view-only preview. Reuses native placements, world-shape resolver,
identity resolution and the whole-occurrence selector; [owner procedure](../tests/OccurrenceMove.md),
roadmap 10.7a/b. Copy/snapping/triads/maintained relationships remain open.
The shared `BasicShapes/ShapeReferences.py::linked_shape` now includes enclosing
Part transforms for native Links, which lack `getGlobalPlacement`; tested against
native assembly-path geometry with the affected export/inspection/feature consumers.

Document updates (F087/F088): [`DocumentUpdates.py`](../src/Gui/DocumentUpdates.py)
exposes native deferral/explicit recompute and pending/failed/affected input status.
Reuses dependency-inspector identities and native document updates; [owner procedure](../tests/DocumentUpdates.md),
roadmap 7.5.7a/b. Targeted updates and background completion remain open.

Drawing setup (F102): [`DrawingSetup.py`](../src/Mod/TechDraw/TechDrawTools/DrawingSetup.py)
provides TechDraw > Page > Create drawing sheet, using native templates and projection
groups with explicit orientation, scale and convention. [Owner procedure](../tests/DrawingSetup.md),
roadmap 15.3a/b. Broader views and annotations remain separate.

Make Unique (F019): [`UniqueDefinition.py`](../src/Gui/UniqueDefinition.py) provides
Tools > Make occurrence unique for reviewed native sketch/extrusion Part definitions.
Native copy/remap and one-occurrence relinking; [owner procedure](../tests/UniqueOccurrence.md),
roadmap 12.2d/e. The older `tests/prototypes/UniqueDefinition.py` remains test-only.

Feature organization (F014): [`FeatureOrganizer.py`](../src/Gui/FeatureOrganizer.py)
provides Tools > Find and describe features, native metadata search and undoable
Label/Label2 editing. Reuses dependency-inspector identity resolution.
[Owner procedure](../tests/FeatureOrganizer.md); roadmap 10.6b/c.

Section planes (F100): existing [`Clipping.cpp`](../src/Gui/Clipping.cpp) owns numeric
plane feedback and atomic `.fcsection` preset save/load. Native visual clipping;
[owner procedure and contract](../tests/SectionPlanes.md), roadmap 15.1e/f.

Mirror result mode (F057): existing [`Mirroring.cpp`](../src/Mod/Part/Gui/Mirroring.cpp)
offers native associative results or independent shape snapshots for root shapes/Bodies.
Transactional creation validates sources/results and reports recoverable errors inline.
[Owner procedure](../tests/MirrorResultMode.md); roadmap 13.5a/b.

Sketch repair review (F049): existing [`TaskSketcherValidation.cpp`](../src/Mod/Sketcher/Gui/TaskSketcherValidation.cpp)
lists missing-coincidence endpoints/gaps with row highlighting and checked-only,
undoable repair. Solver failures restore the sketch; edits/search-policy changes
invalidate candidates. [Owner procedure](../tests/SketchRepairReview.md); roadmap 11.6a/b.

Interference/clearance inspection (F101): [`InterferenceCheck.py`](../src/Mod/Part/InterferenceCheck.py)
and [`InterferenceCheckGui.py`](../src/Mod/Part/InterferenceCheckGui.py) inspect explicit
solid pairs using native world shapes, overlap volume and minimum distance. Part menu;
deliberate exclusions, unresolved rows, pair selection and edit invalidation.
[Owner procedure](../tests/InterferenceCheck.md); roadmap 15.1c/d.

Occurrence appearance (F018): [`OccurrenceAppearance.py`](../src/Gui/OccurrenceAppearance.py)
exposes native whole-link visibility/colour/transparency and source inheritance in
View > Occurrence appearance. Staged edits use one transaction and reject stale state;
geometry/placement are preserved. [Owner procedure](../tests/OccurrenceAppearance.md);
roadmap 12.2b/c. Make Unique has a separate bounded native command; see the entry above.

Measurement context (F098/F099): existing [`TaskMeasure.cpp`](../src/Mod/Measure/Gui/TaskMeasure.cpp)
shows operand identities and measurement/frame meaning. Native
[`MeasureDistanceDetached`](../src/Mod/Measure/App/MeasureDistance.cpp) stores fixed-point
policy and capture provenance without live source links. [Owner procedure](../tests/MeasurementContext.md);
roadmap 15.1a/b. Broader measurement acceptance remains open.

Dependency inspection (F015): [`DependencyInspector.py`](../src/Gui/DependencyInspector.py)
owns the bounded native property-edge snapshot and Tools > Inspect dependencies
dialog. Direct/transitive inputs and consumers, property reasons, status, external
sources and explicit selection/navigation reuse native graph/selection APIs.
[Owner procedure](../tests/DependencyInspector.md); roadmap 7.5.5a / 10.6a.

Extrude preselection: `TaskPadParameters::setPreselection` reuses the profile
gate/assignment for `Command.cpp`'s Pad/Pocket entry. `TaskDlgPadParameters` owns
Cancel selection snapshots; `ViewProviderExtrude::setEdit` captures editing
selection before the base editor clears it. Roadmap 8.1.2b/8.1.5b.
`highlightProfileItems` activates Profile for inspection under a guarded selection
callback; `updateProfileFeedback` owns entry counts/type/picking text (8.1.3d/e).

Combined Pattern Originals: `TaskTransformedParameters::updateOriginalsFeedback`
and `clearOriginals` add scoped count/type/state and Clear controls. The combined
controller's `prepareOriginalsSelection` and embedded Pattern reference cancellation
coordinate input roles without changing stored types/settings; roadmap 8.1.3f-h.
`highlightOriginals` resolves row identities and owns temporary inspection visibility;
combined Pattern command/view-provider entry captures selection for
`TaskDlgTransformedParameters::reject` rollback recovery (8.1.3i/8.1.5c).
`setOriginalsPreselection`, `originalSelectionError` and `changeOriginal` share
preselection/later-pick validation and assignment; Pattern-only inline rejection
feedback leaves the collector recoverable (8.1.2c/8.1.3j).
`TaskPatternParameters::setupReferenceCollectors` adds combined-only Direction/Axis
feedback and inspection. `TaskTransformedParameters::highlightReference` shares
visibility cleanup keyed by document/object identity (8.1.3k/l).
Combined Pattern `cancelReferenceSelection` restores reference combos for all role
exits; `apply` ends unfinished picking before recording links and scope changes call
`prepareOriginalsSelection` (8.1.5d). Originals type rejection precedes dependency
feedback (8.1.3m).




Isocline tolerance: `curve_tolerance` in
[`Isocline.py`](../src/Mod/Part/BasicShapes/Isocline.py) validates native distance
limits and length units; `IsoclineTask.applyTolerance` in
[`IsoclineGui.py`](../src/Mod/Part/BasicShapes/IsoclineGui.py) handles drafts and
protects expression-driven values. F070 acceptance mapping:
[Isocline tests](../tests/IsoclineCurve.md#f070-functional-acceptance-mapping).

Collector inspection and Cancel selection recovery: `highlight_references` and
`task_selection_snapshot` in [`FeatureTask.py`](../src/Mod/Part/BasicShapes/FeatureTask.py),
used by Trim Body and Isocline. Snapshots retain object/occurrence subelement paths;
inspection does not feed its own picks into active collectors. Isocline also offers
explicit direction-reference Clear; roadmap 8.1.3a/b and 8.1.5a.
`selection_link` in each editor shares preselection and interactive input checks;
collector counts/type hints/active-role text and ignored-input notices implement
8.1.2a/8.1.3c. Isocline whole-object LinkSubList entries use an explicit empty
subelement name so picking, removal and persistence retain the source (5.1.11).

Feature creation startup rollback: `creation_transaction` in
[`FeatureTask.py`](../src/Mod/Part/BasicShapes/FeatureTask.py), used by Trim Body and
Isocline and CAM Holding Tab/Indexed Setup commands (roadmap 4.1.7/5.1.7,
16.2bs/bt); successful tasks retain their transaction.
`guard_task_construction` and `TaskFeatureViewProvider.setEdit` clean up construction/
display failures and owned edit transactions (4.1.8/5.1.8).
Scoped creation ownership prevents existing editors from adopting unrelated pending
transactions (4.1.9/5.1.9).
Shared failed-task cleanup continues after secondary resource cleanup errors and
preserves the primary startup exception; annotation removal is idempotent (4.1.10/5.1.10).

Trim Body and Isocline task readiness uses `require_current` in
[`ShapeReferences.py`](../src/Mod/Part/BasicShapes/ShapeReferences.py) after recompute;
invalid/touched dependencies block preview acceptance and input replacement
and are omitted from optional preselection (roadmap 4.1.4-6/5.1.4-6).

Sketch reattachment: installed [`SketchSupport.py`](../src/Mod/Sketcher/SketchSupport.py)
owns direct same-container planar operations and disposable-document placement
preview. [`SketchSupportGui.py`](../src/Mod/Sketcher/SketchSupportGui.py) provides
inspection, local/world choices, numeric preview, stale rejection and Apply/repair
(11.7y/z). [Owner procedure](../tests/SketchSupport.md). Existing foundation tests
in [`TestPartHistoryAdapters.py`](../tests/TestPartHistoryAdapters.py) call that core
through compatibility imports in [`SketchReattachment.py`](../tests/prototypes/SketchReattachment.py).
Its cross-part PlanarSupport proxy and atomic reference creation remain test-only,
with their existing import identities preserved. `current_result_shape` in
[`PartHistoryAdapters.py`](../tests/prototypes/PartHistoryAdapters.py) remains an
experimental consumer guard. Graphical preview and broader support scope remain open.

All code paths are relative to the project root.

| Path | Responsibility | Key entry point |
| --- | --- | --- |
| `src/Main/` | GUI and command-line launch | `MainGui.cpp`, `MainCmd.cpp` |
| `src/App/` | Documents, properties, transactions, persistence | [`Document.cpp`](../src/App/Document.cpp) |
| `src/Gui/` | Application shell, selection, task view | [`Control.cpp`](../src/Gui/Control.cpp) |
| `src/Mod/Part/BasicShapes/` | Associative curve features and shared reference/task helpers | `Isocline.py`, `ShapeReferences.py`, `FeatureTask.py` |
| `src/Mod/Part/BOPTools/` | Boolean geometry helpers and associative Trim Body | `TrimAPI.py`, `TrimFeatures.py`, `TrimGui.py` |
| `src/Mod/Part/parttests/` | Part geometry and GUI regressions | `TestTrimBody.py`, `TestTrimBodyGui.py` |
| `src/Mod/PartDesign/App/` | Parametric feature models and geometry | [`FeaturePad.cpp`](../src/Mod/PartDesign/App/FeaturePad.cpp) |
| `src/Mod/PartDesign/Gui/` | Commands, view providers, task panels | `Command.cpp`, `TaskPadParameters.cpp` |
| `src/Mod/PartDesign/PartDesignTests/` | Python application and GUI regressions | [`TestPadTaskPanel.py`](../src/Mod/PartDesign/PartDesignTests/TestPadTaskPanel.py) |
| `tests/src/Mod/PartDesign/App/` | C++ feature tests | [`Pad.cpp`](../tests/src/Mod/PartDesign/App/Pad.cpp) |
| `cMake/`, `.github/workflows/` | Build configuration and upstream CI recipes | [`CMakeLists.txt`](../CMakeLists.txt) |
| `ai-instructions/` | Fork requirements, development guidance, and planning | This index |

## Common code and libraries

| Capability | Canonical implementation | Reuse guidance |
| --- | --- | --- |
| Pad/Pocket parameter controls | [`TaskExtrudeParameters`](../src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp), [`TaskPadPocketParameters.ui`](../src/Mod/PartDesign/Gui/TaskPadPocketParameters.ui) | Preserve Pocket behavior when changing the common base. |
| Sketch-based selection and visibility | [`TaskSketchBasedParameters`](../src/Mod/PartDesign/Gui/TaskSketchBasedParameters.cpp) | Coordinate selector lifetimes and visibility restoration. |
| Pattern parameters and transformations | [`TaskPatternParameters`](../src/Mod/PartDesign/Gui/TaskPatternParameters.cpp), [`MultiTransform`](../src/Mod/PartDesign/App/FeatureMultiTransform.cpp) | Reuse the Linear/Polar engines and parameter widgets; keep result identity separate from retained mode settings. |
| Task acceptance, rejection, and transactions | [`TaskFeatureParameters`](../src/Mod/PartDesign/Gui/TaskFeatureParameters.cpp) | Reuse existing recompute and undo/cancel handling. |
| Geometry reference checks | [`ReferenceSelection`](../src/Mod/PartDesign/Gui/ReferenceSelection.cpp) | Preserve document/body and dependency restrictions. |
| Profile and extrusion model | [`FeatureSketchBased.cpp`](../src/Mod/PartDesign/App/FeatureSketchBased.cpp), [`FeatureExtrude.cpp`](../src/Mod/PartDesign/App/FeatureExtrude.cpp) | UI changes must respect model constraints. |
| Associative feature references and edit lifecycle | [`ShapeReferences.py`](../src/Mod/Part/BasicShapes/ShapeReferences.py), [`FeatureTask.py`](../src/Mod/Part/BasicShapes/FeatureTask.py) | Shared by Trim Body and Isocline: resolve global shapes, reject cycles, track parent placements, open the complete editor, and manage direction arrows. |
| Solid/sheet trimming | [`SplitAPI.slice`](../src/Mod/Part/BOPTools/SplitAPI.py), Part half-spaces and Boolean common/cut | Validate finite separation before classifying kept regions; reuse one Trim command from both workbenches. |
| Dependency and submodule ownership | [`pixi.toml`](../pixi.toml), [`pixi.lock`](../pixi.lock), [`.gitmodules`](../.gitmodules) | Use declared dependencies; do not copy or edit vendor code for a UI task. |

## Data and contracts

| Area | Authoritative source | Related explanation |
| --- | --- | --- |
| Pad profile and dimensions | [`FeatureSketchBased.h`](../src/Mod/PartDesign/App/FeatureSketchBased.h), [`FeaturePad.h`](../src/Mod/PartDesign/App/FeaturePad.h), [`FeatureExtrude.h`](../src/Mod/PartDesign/App/FeatureExtrude.h) | Profile is one object with optional subelement references. |
| Trim Body | [`TrimFeatures.py`](../src/Mod/Part/BOPTools/TrimFeatures.py) | `Part::FeaturePython`, Target/Tool LinkSub, Reversed, ExtendPlanar, Refine; hidden parent placement dependencies. Result remains separate from a source Part Design Body. |
| Isocline Curve | [`Isocline.py`](../src/Mod/Part/BasicShapes/Isocline.py) | Separate Part::FeaturePython wire result; Faces LinkSubList, DirectionReference LinkSub, DirectionMode, CustomDirection, Reversed, Angle and Tolerance. |
| Document links and transactions | [`PropertyLinks.h`](../src/App/PropertyLinks.h), [`Document.cpp`](../src/App/Document.cpp) | Preserve persisted identities and undo semantics. |
| Build/version configuration | [`version.json`](../version.json), [`CMakeLists.txt`](../CMakeLists.txt) | Manifest versions are authoritative. |

No new app-to-app or cloud contract is part of the current fork scope.

## Critical conventions and boundaries

- The source checkout and separately installed FreeCAD are distinct; follow the
  [development guide](DEVELOPMENT_GUIDE.md#prerequisites-and-setup).
- Preserve existing preselection workflows while adding task-pane selection.
- Keep shared helpers reusable without applying Pad behavior to other operations
  before their requirements and validation are defined.

## Additional references

- [Upstream human-facing overview](../README.md)
- [Contribution guidance](../CONTRIBUTING.md), [AI policy](../AI_POLICY.md), [license](../LICENSE)
- [Pad regression procedure](../tests/PadTaskPanel.md)
