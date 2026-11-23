# FreeCAD Plus: Programming Summary

## Latest strict sequential History — November 22, 2026

The approved change is installed: component History follows native dependencies
across Body boundaries, keeping sketches and other inputs before their consumers.
Shared editors reject later/self inputs before mutation. Existing graphs retain
geometry, identity, ownership and saved schema. All 28 targeted development and
165 unique installed checks passed, plus actual History-click and fresh-reopen checks.
A separate updated app was launched through the existing shortcut with isolated settings.
The owner's unsaved Unnamed window was preserved and needs a restart after saving.
See [acceptance](WORK_STATE.md#strict-sequential-history--november-22-2026).

## Latest History coordinate presentation — November 22, 2026

The approved change is installed: Axes/Planes use their children's native icons;
Coordinate System and descendants start collapsed. Refresh preserves manual expansion
choices and geometry visibility. All 14 existing native panel/History checks and a
separate installed visual check passed. The existing shortcut was restarted with
isolated settings. See
[acceptance](WORK_STATE.md#history-coordinate-icons-and-collapsed-defaults--november-22-2026).

## Latest unified Revolve and selection lists — November 22, 2026

Approved changes are installed. Extrude and Revolve share an at-least-five-row
scrollable profile collector. Revolution/Groove commands now share New Solid/Add/
Subtract creation and editing for component profiles, with axis references/guide,
degree-based offsets and angles, symmetric/two-sided rotation, selected-target display
and validity colors. Native saved links, identity, source ownership and Undo remain
intact. All 11 focused build checks and 188 installed tests passed, plus separate
native visual and saved-file reopen checks. Native To first/To last remain disabled;
angular references require planes through the axis. See
[acceptance](WORK_STATE.md#unified-revolve-implementation--november-22-2026).

## Latest Extrude target and preview colors — November 22, 2026

The approved change is installed: hidden targets selected in History display in the
configured selection color while their eyes remain unchanged. Visible targets retain
native reference picking. Add tools are green/yellow for valid/invalid results;
Subtract tools are red/pink. Invalid native operations retain the actual tool for
preview but remain impossible to accept. Source visibility/materials and transactions
are preserved. Eight focused build tests, all 177 installed native tests, four native
visual cases and fresh save/reopen checks passed. The existing shortcut was restarted
with isolated settings. See
[acceptance](WORK_STATE.md#extrude-selected-targets-and-validity-colors--november-22-2026).

## Latest sketch exit framing — November 22, 2026

The approved change is installed: leaving a new or existing nonempty sketch fits
the visible model to include the full sketch while retaining exit orientation.
It runs after native cleanup and skips empty/deleted sketches, cancelled placement
and stale views/editors. Visibility, selection, History restoration and Undo remain
intact. Seven focused build tests, all 169 installed tests, and separate native
Close-button/save-reopen checks passed. See
[acceptance](WORK_STATE.md#view-fitting-after-sketch-exit--november-22-2026).

## Latest sketch coordinate visibility — November 22, 2026

The approved change is installed: entering new or existing sketch drawing hides
the component Coordinate System temporarily. Plane selection still shows planes;
Sketcher's axes and other geometry remain visible as before. History eyes remain
usable, and exit restores prior display with native semantics for explicit choices.
Automatic hiding changes no saved visibility or transaction data. All 162 tests
passed in both build and installed payloads; separate drawing/save-reopen checks
and the existing shortcut restart passed with isolated settings. See
[acceptance](WORK_STATE.md#sketch-coordinate-system-visibility--november-22-2026).

## Latest sketch/task update — November 22, 2026

Approved changes are installed: mouse-only sketch creation adds no unsolicited
dimensions while geometric constraints and deliberate dimensions remain available.
Feature creation/edit temporarily selects History and restores the prior tab on
exit, including sketch placement-to-drawing and standalone native Part dialogs.
All 155 installed tests and separate GUI/save-reopen checks passed. The app was
restarted through the existing shortcut with isolated settings. See
[acceptance](WORK_STATE.md#sketch-dimensions-and-feature-task-history--november-22-2026).

## Latest Extrude update — November 22, 2026

Approved Extrude visibility behavior and shared task tree controls are installed.
New tasks filter unusable geometry; edits isolate profile/target; solids become
translucent with target-field selection coloring. Planar solid/sheet faces are
associative profiles. Temporary display restores cleanly; explicit eye choices
remain undoable. All 134 installed native tests plus separate GUI/reopen checks
passed, and the existing shortcut was restarted with isolated settings. See
[acceptance](WORK_STATE.md#extrude-visibility-and-shared-tree-controls--november-22-2026).

## Latest History update — November 22, 2026

Approved Coordinate System hierarchy is implemented and installed: native Origin
point, Axes and Planes subgroups, group and individual left-margin visibility eyes.
New components show their origin/axes/planes; existing saved visibility is retained.
63 native checks and installed fresh-process verification passed. See
[acceptance](WORK_STATE.md#coordinate-system-history--november-22-2026).

## Current baseline

November 22 approved toolbar layout is installed across all nine Design tabs:
bordered icons, separate icon/arrow segments, logical groups with separate dropdown
columns, and vertical section dividers. The three Constraints menus share a column.
Surplus spacing in the proposed renders was removed before installation; compact
natural-width buttons retain their arrow area on narrow scrolling pages. Thirteen
installed native regression cases passed. See
[acceptance](WORK_STATE.md#design-toolbar-layout--november-22-2026).

November 22 approved corrections are installed: rectangular Extrude previews no
longer show diagonal rear-face shading, and new/existing component sketch editing
preserves shown/hidden geometry, including native rendered LinkVisibility. The
previous checks covered saved flags but missed this rendering distinction. All 107
expanded native checks and independent GUI/save-reopen checks passed; see
[acceptance](WORK_STATE.md#extrude-rendering-and-sketch-visibility-correction--november-22-2026).

November 22 approved Design interactions are installed: New Sketch automatically
shows fundamental planes; History eyes remain usable during placement and native
drawing; idle Design offers New Sketch, Datum Plane, Datum Line and Datum Point.
Typed numeric values wait for field leave; arrow steps update immediately with
focus retained, including native quantity editors. Line/Point reuse native tasks
with component ownership. All 103 affected native checks and independent reopen/UI
verification passed; see [acceptance](WORK_STATE.md#design-interaction-implementation--november-22-2026).

November 22 approved Extrude is implemented and installed, including vertically
stacked New Solid/Add/Subtract radio buttons. The shared creation/edit task uses
explicit targets, sketch/curve/region picks, start/end references, independent
sides, direction/taper and transient tool/result previews. Numerical recompute
waits for field leave for typed values; explicit arrow steps update immediately. Managed operations retain native feature identity and use
internal Bodies. The native build, 90 installed checks, fresh-process persistence
and actual GUI acceptance passed; see [acceptance and boundaries](WORK_STATE.md#extrude-implementation--november-22-2026).

November 21 approved Sketch Offset/Reverse offset and orange local Plane/Sketch
axes are implemented. Offset persists in the shared creation/editing task, follows
the support normal and is unaffected by sketch normal reversal. Typed numeric previews
still wait for field leave; older managed sketches default to zero. See
[acceptance](WORK_STATE.md#sketch-offset-and-orange-axes-implementation--november-21-2026).

November 21 archive-guided plane improvements implement the approved concepts
afresh in current modules: next-pick guidance, numbered reference highlights,
repeat-pick/Delete removal and saved independent axis reversal. Creation/editing
share the task; older planes remain unchanged until acceptance. See
[acceptance](WORK_STATE.md#plane-guidance-implementation--november-21-2026).

November 21 approved New Sketch placement is installed: plane/face preselection,
automatic plane-frame inheritance or part-origin/X projection, editable references,
and the shared placement-edit task. Sketches retain native identity and drawing;
placement remains associative after extrusion and save/reopen. See
[installed acceptance](WORK_STATE.md#new-sketch-placement-implementation--november-21-2026).

Owner rule: every feature/operation must reuse its creation task for editing, with
saved inputs prefilled, identity-preserving acceptance and unchanged Cancel. Plane
editing has been verified through both existing entry routes; follow the
[shared task contract](ui-ux-specs/TASK_PANEL.md#shared-task-patterns) for all further work.

November 21 approved New Plane workflow is installed: the existing command opens
the right-hand task panel for Plus components, with associative geometry references,
point-only origin, X/Y direction assignment and Flip normal. Planes belong directly
to the component; no Body is created. Shared numerical editors and Move/Rotate
previews defer updates until focus leaves. See
[WORK_STATE](WORK_STATE.md#new-plane-implementation--november-21-2026) for installed
acceptance, persistence evidence and two independently reproduced baseline test failures.

November 21 approved History UI: component activation opens History, with native
Origin grouping its three axes and three fundamental planes. Every part History
item has a fixed left-margin visibility eye. Source-owned native visibility,
parent containers, task/context guards and Undo/Redo remain in use. See
[WORK_STATE](WORK_STATE.md#grouped-history-and-left-margin-visibility--november-21-2026)
for installed/native evidence and the component specification for direct approval.

November 21 owner terminology: original FreeCAD uses **body-centered modeling**;
FreeCAD Plus uses **feature-centered modeling**. The new backend module
`freecad_plus/modeling.py` creates sketches without Bodies and atomically supplies
a native Body when extruding a new solid. The existing ribbon New Sketch and
Extrude commands initially routed to these services. The approved sketch placement
task replaces the initial native placement dialog; drawing stays native. The
November 22 Plus Extrude task now owns creation/editing of managed operations and
explicit Add/Subtract targets. Classic commands and existing Body-owned chains
retain native compatibility through the original routing adapters.
See [architecture](ARCHITECTURE.md#feature-centered-modeling-foundation--november-21-2026)
for API scope and [WORK_STATE](WORK_STATE.md#feature-centered-modeling-foundation--november-21-2026)
for initial native acceptance and the newer
[command integration](WORK_STATE.md#feature-centered-command-integration--november-21-2026)
for command/installed-app validation. The newer
[Add/Subtract increment](WORK_STATE.md#feature-centered-addsubtract-targets--november-21-2026)
records target routing, Cancel/Undo/Redo and persistence acceptance. Arbitrary
imported Part targets, consumed-profile reuse and feature deletion remain
outstanding; this is not a completed replacement of every body-centered workflow.

This checkout starts from official **FreeCAD 1.1.4** source at
`4fd3bf320d9566a27e60069fc8387448aaa3a094`, plus owner documentation, an agent entry
point and focused generated-file ignore rules. Branch: `codex/freecad-1.1.4-baseline`.
No previous Plus application changes have been carried into this branch. Group 1
now has validated, opt-in domestic/external catalogs, hierarchy, shared-instance,
independent-copy and legacy-conversion services under src/Mod/FreeCADPlus.
G1.6a adds an opt-in Models/Part Tree/History panel foundation with placed-component
Edit and native selection. G1.6b domestic/external unused-model editing is validated
in the native development build, including source-owned Undo/save, picking and
per-view cleanup. G1.6c1 component file tabs are validated in the development
build; WORK_STATE records tests, fresh-process persistence and inspected captures.
G1.6c2 Part Tree linked-instance Copy/Paste is validated in the development build;
WORK_STATE records 50 combined tests, fresh-process persistence and inspected captures.
G1.6c3 Move Components foundation/Translate is validated in the development build;
WORK_STATE records regression, independent persistence and inspected visual acceptance.
G1.6c4 Rotate is validated in the development build; WORK_STATE records 62 combined
cases, independent persistence and inspected visual acceptance.
Move Components is operation/task-panel work; right-click access does not place its
workflows within Group 1. The unvalidated Point to Point increment is parked on a
separate local branch; WORK_STATE records its exact state. G1.7a saved Part Type
and visibility state is validated in the development payload; WORK_STATE records
acceptance and limits. G1.7b1 adds view-local explicit hiding/restoration; WORK_STATE
records its validation. G1.7b2 contextual fading is validated in the development
payload, including shared mixed face materials and independent reopen. Its planned
checks are complete. G1.7b3a saved self/child display in domestic/external unused
previews is also validated. G1.7b3b Bodies Only filtering is validated in placed
and unused views, with bounded native link-snapshot synchronization. G1.7b3c adds
validated occurrence-aware Reference/Excluded eligibility and guards the existing
Move Components reference consumers. G1.7b3d guards native File > Export before
options/writing and fixes source selection for external unused component exports.
G1.7b3e adds native PartDesign profile and Sketcher Projection/Intersection input
eligibility. Its focused native tests and independent reopen/source-update checks
passed. G1.7b3f native attachment and shared picked axis/direction/plane references
also passed focused native and independent reopen/downstream checks. G1.7b3g covers
the separate attachment editor and Extrude face/shape intake, with validated Apply/
Cancel cleanup and independent downstream checks. G1.7b3h Loft/Pipe picked profiles,
sections and main/auxiliary paths passed focused native and independent reopen checks.
G1.7b3i shared dress-up/transformed input guards, including whole-edge controls,
passed targeted native and independent reopen checks. G1.7b3j command-start
selection checks and Pattern feedback routing passed focused native and independent
reopen checks, including the Chamfer rejected-selection cleanup correction.
G1.7b3k same-component native Boolean ownership, History and nested edit paths passed
focused native and independent reopen checks. G1.7b3l extends isolated legacy
conversion to those native Boolean-owned tool graphs; focused conversion and
independent reopen/source-edit checks passed. G1.7b3m placed external export context
passed native build, focused export and independent reopen checks. Stop here.
WORK_STATE owns acceptance evidence. Boolean Reference/Excluded command and picker
admission passed focused native and independent reopen checks in G1.7b3n;
ownership of tools from another Full Component is
still undefined. Direct exporter/view-output paths still need integration. Check latest
owner conversations before asking design questions. Full G1.7b and Group 1
remain incomplete. WORK_STATE owns acceptance evidence.
G1.6c5 shared definition Rename passed native menu/dialog, source-owned Undo and
independent reopen checks. The complete G1.6 panel is unfinished.
G1.6c6 Models file import passed native menus/chooser, source-owned catalog/Undo,
closed-source hidden loading and independent reopen. It creates no placed instances.
The October 11 owner clarification explicitly requires all Reference geometry to
enter the active component's History through Add Reference Feature before any use.
G1.7b3o core Part Boolean admission and retained input/result ownership passed native
and independent reopen/source-edit checks. G1.7b3p direct Part Section also passed
native command/dialog and independent reopen/source-edit checks. G1.7b3q Compound
creation passed four focused native cases and independent reopen/source-edit.
G1.7b3r Compound drop/replacement and Links-editor intake passed six focused native
cases after two targeted corrections, plus independent reopen/source-edit.
G1.7b3s split/join command admission and result ownership passed five focused native
cases after correcting related-filter insertion, plus independent reopen/source-edit.
G1.7b3t split/join property editing passed four focused native cases, two affected
Compound regressions and independent reopen/source-edit. Next: split/join tree drop
and replacement. Other consumers remain unfinished; WORK_STATE owns support/stopping
boundaries.
The official 26.3 RC1 is a prerelease, not the stable version selected by the owner.

G1.6d supersedes the developer-only startup boundary: General/Application now has
independent model/components, toolbar and task-workflow selectors, all Plus by
default. InitGui installs the panel presentation controller; Classic preserves the
same component backend. Plus toolbars now have a separate ribbon module; tasks still share Classic definitions. Native
Pad/Pocket share FeatureExtrude; a consolidated Plus task is still future work.
WORK_STATE records startup, mixed-mode, active-task and persistence acceptance.
G1.6e connects native New File to document.new_document and New Part to
hierarchy.new_part: a catalog definition only, with placement kept separate.
WORK_STATE records bounded native command/Undo/reopen acceptance.

TB.2a completes Classic workbench/toolbar inclusion in the separate Plus module.
The full native development build now contains all nineteen baseline workbenches
plus None; All Tools preserves native groups, commands, specialized widgets and
custom toolbars. Eight interaction tests, every-workbench inventory audit and
independent restart passed. WORK_STATE owns evidence and the stopping boundary;
remaining curated layouts and Plus-only workflows are still separate work.
TB.2a1 routes modes by native workbench identity so duplicate/renamed labels preserve
added-workbench access and Design-only control scope; WORK_STATE owns acceptance.
TB.2a2 keeps enabled alternatives reachable in Plus split groups when the remembered
command is unavailable, without changing native command state or last-choice memory.
TB.2b adds validated complete two-line captions and icon-only unavailable controls;
nine interaction/layout cases and all-workbench coverage passed. TB.2c1 adds the
saved Design Directional Selection control and native model/Sketcher behavior.
TB.2c2a adds the saved Single/Connected/Tangent Curve Intent split button with native
viewport edge traversal and mapped Sketcher/occurrence handling. WORK_STATE owns
build and runtime evidence. TB.2c2b adds saved category-checkbox filtering with an
independent native selection gate, including model and Sketcher batch admission.
TB.2c2c corrects Plus Sketcher plain-click replacement, modified empty clicks and
selected Escape handling. Native build and focused point/edge/constraint interaction
checks passed; WORK_STATE owns combined acceptance and coverage evidence.
TB.2c2d adds the saved Persistent Selection toggle and native Equal-to-Construction
retention, plus a correction that preserves BIM status-toolbar ownership. WORK_STATE
owns native acceptance. TB.2c2e extends retention to basic preselected sketch
constraints, including point alignment, coincidence, symmetry and native tangency
substitutions. Continuous constraint picking retains its own cleanup. WORK_STATE
owns acceptance. TB.2c2f integrates named preselected distance, angle and circular
dimensions through native dialog completion, including Cancel and reference/no-dialog
paths, and fixes Curve Intent icon/arrow sizing under native styles. Continuous
dimension picking keeps native sequence cleanup. TB.2c2g connects direct Tangent/
Perpendicular completion and conic commit outcomes to the same retention policy;
WORK_STATE owns native acceptance and geometry-family limits. TB.2c2h extends
retention to selected Driving/Reference and Active toggles and menu-only Refraction,
including rejection/no-op handling and native creation-mode preservation. All 51
toolbar cases, full Classic inventory and independent restart passed; WORK_STATE
owns evidence. TB.2c2i integrates preselected contextual Dimension through native
activation, dialog/commit and handler teardown while preserving continuous picking
and native autoscale transactions. All 57 toolbar cases, complete Classic inventory
and independent restart passed; WORK_STATE owns acceptance limits. TB.2c2j adds
idle B-spline degree-elevation retention through the existing native identity and
transaction services. TB.2c2k retains surviving geometry through Delete All Constraints
and prevents native list refresh from clearing idle Plus selection. Native cleanup
uses original selection references for deleted constraints, including nested paths.
WORK_STATE owns targeted acceptance and preservation checks. Other operation integrations, Layers and unfinished Plus workflows remain outstanding.

## Where to go

| Task | Reference |
| --- | --- |
| Component/document target contract | [Architecture](ARCHITECTURE.md), [Group 1 stages](DEVELOPMENT_ROADMAP.md#group-1--component-panel-and-document-structure) |
| Intended UI/workflows | [UI specification index](UI_UX_SPEC.md) |
| Unconfirmed implemented ideas from old fork | [Review inventory](ui-ux-specs/UNVERIFIED_IMPLEMENTED_CHANGES.md) |
| Conversation evidence and conflicts | [Evidence ledger](ui-ux-specs/EVIDENCE_AND_DECISIONS.md) |
| Prior fork recovery | [Archive reference](ARCHIVE_REFERENCE.md) |
| Current work/status | [Roadmap](DEVELOPMENT_ROADMAP.md), [WORK_STATE](WORK_STATE.md) |
| Stable baseline inventory and local checks | [Runtime inventory and completed display check](WORK_STATE.md#stable-baseline-inventory-and-light-runtime-check--october-10-2026) |
| Execution/build guidance | [Development guidelines](DEVELOPMENT_GUIDELINES.md), [guide](DEVELOPMENT_GUIDE.md) |
| Product scope | [Product specification](PRODUCT_SPEC.md) |
| Old implementation records | [Historical documents](archive/pre-restart-docs/README.md) |

## Source map

- src/Mod/FreeCADPlus/freecad_plus/toolbars.py: separate Plus ribbon widgets, native action/menu adapters and Classic visibility restoration.
- src/Mod/FreeCADPlus/freecad_plus/selection_toolbar.py and src/Gui/Selection/PlusSelection.h: saved Design selection toggle and transient native selection policy.
- src/Mod/FreeCADPlus/freecad_plus/toolbar_layout.py: Plus mode/tab/group definitions.
- src/Mod/FreeCADPlus/freecad_plus/curve_selection.py: viewport-only native curve/edge connectivity and tangent traversal.
- src/Mod/FreeCADPlus/TestPlusToolbars.py: native split-button, mode/tab, independent preference and Classic restoration acceptance.

- src/App and src/Gui: upstream document/application and desktop services.
- src/Mod: original workbench modules; retain their source and availability.
- src/Mod/FreeCADPlus/freecad_plus/document.py: schema, native owned_children/owned_path traversal, History projection and creation/open/save.
- src/Mod/FreeCADPlus/TestPartBooleanInputs.py: native Part Boolean/Section/Compound admission, input/result ownership, Undo, dialog Apply, legacy bypass and persistence.
- src/Mod/Part/Gui/ComponentBoolean.h and src/Mod/Part/BOPTools/BOPFeatures.py: Part Boolean preflight bridge and component-owned native result creation.
- src/Mod/Part/Gui/ViewProviderCompound.cpp and src/Gui/Dialogs/DlgPropertyLink.cpp: Compound native input-edit admission; Tree and PropertyItem preflight context/multi-target edits.
- src/Mod/FreeCADPlus/TestComponentBooleanInputs.py: Boolean command/picker occurrence admission, atomic rejection, cleanup and legacy bypass.
- src/Mod/FreeCADPlus/TestComponentBooleanOwnership.py: same-component Boolean ownership, nested History/Edit, Undo/Cancel and independent persistence checks.
- src/Mod/FreeCADPlus/freecad_plus/editing.py: per-view Edit, backend Body and native feature adapters.
- src/Mod/FreeCADPlus/TestComponentPilot.py: G1.2 regression suite and fresh-process check.
- src/Mod/FreeCADPlus/freecad_plus/conversion.py: isolated legacy conversion and persisted loss report.
- src/Mod/FreeCADPlus/TestLegacyBooleanConversion.py: native Boolean graph conversion, source isolation and independent persistence checks.
- src/Mod/FreeCADPlus/TestLegacyConversion.py: G1.3 fixtures and fresh-process acceptance.
- src/Mod/FreeCADPlus/freecad_plus/hierarchy.py: domestic graph, placement and occurrence paths.
- src/Mod/FreeCADPlus/freecad_plus/legacy_hierarchy.py: native Part/link conversion.
- src/Mod/FreeCADPlus/TestComponentHierarchy.py: G1.4 regression and fresh-process checks.
- src/Mod/FreeCADPlus/freecad_plus/external.py: native import catalogs, file identity/preflight, defining-file saves and independent copies.
- src/Mod/FreeCADPlus/TestExternalDefinitions.py: G1.5 regression and fresh-process checks.
- src/Mod/FreeCADPlus/freecad_plus/panel.py: opt-in panel, stable row projection, selection/Edit and native document observers.
- src/Mod/FreeCADPlus/TestComponentImport.py: Models import menus/chooser, nested catalogs, external ownership, guards and independent reopen.
- src/Mod/FreeCADPlus/TestComponentRename.py: shared definition Rename, native menus/dialogs, source-owned Undo and persistence.
- src/Mod/FreeCADPlus/TestComponentPanel.py: G1.6a actual Qt interaction, lifecycle and persistence tests.
- src/Mod/FreeCADPlus/freecad_plus/isolation.py: transient per-view unused-definition display and cleanup.
- src/Mod/FreeCADPlus/TestUnusedModels.py: unused-model interaction, native editors/picking, source-owned Undo/save and lifecycle checks.
- src/Mod/FreeCADPlus/TestComponentWindows.py: component-tab menus, per-view context/camera, guards, cleanup and fresh-process persistence.
- src/Mod/FreeCADPlus/TestComponentClipboard.py: linked Copy/Paste menus/keys, batch Undo, shared identity, source ownership and save/reopen.
- src/Mod/FreeCADPlus/freecad_plus/geometry.py: occurrence-aware Reference/Excluded geometry eligibility, independent of display/selection.
- src/Mod/FreeCADPlus/TestComponentEligibility.py: consumer guard, shared/external ownership and fresh-process acceptance.
- src/Gui/ComponentGeometry.h: shared native modeling eligibility bridge for PartDesign/Sketcher.
- src/Mod/FreeCADPlus/TestComponentCommandInputs.py: native dress-up/transformation command starts, Pattern routing and independent persistence checks.
- src/Mod/FreeCADPlus/TestComponentDressUpInputs.py: native dress-up/transformed admission, whole-edge context guards, transactions and independent persistence checks.
- src/Mod/PartDesign/Gui/TaskDressUpParameters.cpp and TaskTransformedParameters.cpp: shared picked-input guards; TaskFilletParameters.cpp and TaskChamferParameters.cpp also guard Use All Edges.
- src/Mod/FreeCADPlus/TestComponentSweepInputs.py: Loft/Pipe reference admission, native transactions and independent recompute/persistence checks.
- src/Mod/PartDesign/Gui/TaskLoftParameters.cpp and TaskPipeParameters.cpp: picked profile, section and main/auxiliary path admission.
- src/Mod/FreeCADPlus/TestComponentInputEditors.py: Python attachment/Extrude input acceptance, confirmation/Undo and independent downstream checks.
- src/Mod/Part/AttachmentEditor/TaskAttachmentEditor.py and src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp: component admission for remaining attachment and Extrude face/shape inputs.
- src/Mod/FreeCADPlus/TestComponentReferences.py: native attachment/axis collector, atomic rejection, legacy bypass and downstream acceptance.
- src/Mod/Part/Gui/TaskAttacher.cpp and src/Mod/PartDesign/Gui/ReferenceSelection.cpp: component input guards for native attachment/shared picked references.
- src/Mod/FreeCADPlus/TestComponentModeling.py: native intake, transactions, legacy bypass and independent reopen checks.
- src/Mod/FreeCADPlus/TestComponentExternalExport.py: original external export occurrences, source payload and independent reopen checks.
- src/Mod/FreeCADPlus/TestComponentExport.py: native File > Export rejection, BREP/legacy/source-owned export and independent reopen.
- src/Gui/Application.cpp and CommandDoc.cpp: component-only export preflight and external unused source-selection routing.
- src/Mod/FreeCADPlus/freecad_plus/movement.py: parent-owned Translate/Rotate task, transient preview and atomic commit.
- src/Mod/FreeCADPlus/TestComponentMove.py: task/placement/source ownership and fresh-process persistence checks.
- src/Mod/FreeCADPlus/freecad_plus/display.py: schema-5 saved self/direct-child choices and occurrence hide-path resolution.
- src/Gui/View3DPy.cpp: native per-view hide wrapper and fading context; no saved display-property changes.
- src/Gui/Selection/SoFCSelectionAction.cpp: per-view transparency floor in native shape rendering.
- src/Mod/FreeCADPlus/TestComponentFading.py: normal-framebuffer blending, separate views, material/identity and reopen checks.
- src/Mod/FreeCADPlus/TestComponentVisibility.py: hiding, independent views, cleanup, recompute and reopen checks.
- src/Mod/FreeCADPlus/TestComponentBodiesOnly.py: content filtering, native editor, nested/shared/unused contexts and reopen checks.
- src/Mod/FreeCADPlus/TestComponentDisplay.py: panel/state ownership, migration, copy and persistence checks.
- src/Mod/FreeCADPlus/TestComponentRotate.py: located-axis/pivot rotation, shared placement and fresh-process acceptance.
- tests and per-workbench tests: upstream test infrastructure.
- CMakeLists.txt, CMakePresets.json and .github/workflows: this release's build definitions.
- .gitmodules: this release's pinned GSL, OndselSolver, AddonManager and GoogleTest.

Existing external FreeCAD Plus builds use the archived implementation. They do not
validate or represent this clean checkout. Reimplementation begins only from an
explicit task and confirmed requirements; historical backlog entries do not restart work.
