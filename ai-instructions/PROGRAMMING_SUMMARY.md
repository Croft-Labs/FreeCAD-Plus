# FreeCAD Plus: Programming Summary

## Current baseline

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
Stop here. Next: shared dress-up and transformed-feature input collectors.
Direct exporter/view-output paths still need integration. Check latest
owner conversations before asking design questions. Full G1.7b and Group 1
remain incomplete. WORK_STATE owns acceptance evidence.
The complete G1.6 panel is unfinished.
The official 26.3 RC1 is a prerelease, not the stable version selected by the owner.

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

- src/App and src/Gui: upstream document/application and desktop services.
- src/Mod: original workbench modules; retain their source and availability.
- src/Mod/FreeCADPlus/freecad_plus/document.py: schema, ownership, creation/open/save.
- src/Mod/FreeCADPlus/freecad_plus/editing.py: per-view Edit, backend Body and native feature adapters.
- src/Mod/FreeCADPlus/TestComponentPilot.py: G1.2 regression suite and fresh-process check.
- src/Mod/FreeCADPlus/freecad_plus/conversion.py: isolated legacy conversion and persisted loss report.
- src/Mod/FreeCADPlus/TestLegacyConversion.py: G1.3 fixtures and fresh-process acceptance.
- src/Mod/FreeCADPlus/freecad_plus/hierarchy.py: domestic graph, placement and occurrence paths.
- src/Mod/FreeCADPlus/freecad_plus/legacy_hierarchy.py: native Part/link conversion.
- src/Mod/FreeCADPlus/TestComponentHierarchy.py: G1.4 regression and fresh-process checks.
- src/Mod/FreeCADPlus/freecad_plus/external.py: native import catalogs, file identity/preflight, defining-file saves and independent copies.
- src/Mod/FreeCADPlus/TestExternalDefinitions.py: G1.5 regression and fresh-process checks.
- src/Mod/FreeCADPlus/freecad_plus/panel.py: opt-in panel, stable row projection, selection/Edit and native document observers.
- src/Mod/FreeCADPlus/TestComponentPanel.py: G1.6a actual Qt interaction, lifecycle and persistence tests.
- src/Mod/FreeCADPlus/freecad_plus/isolation.py: transient per-view unused-definition display and cleanup.
- src/Mod/FreeCADPlus/TestUnusedModels.py: unused-model interaction, native editors/picking, source-owned Undo/save and lifecycle checks.
- src/Mod/FreeCADPlus/TestComponentWindows.py: component-tab menus, per-view context/camera, guards, cleanup and fresh-process persistence.
- src/Mod/FreeCADPlus/TestComponentClipboard.py: linked Copy/Paste menus/keys, batch Undo, shared identity, source ownership and save/reopen.
- src/Mod/FreeCADPlus/freecad_plus/geometry.py: occurrence-aware Reference/Excluded geometry eligibility, independent of display/selection.
- src/Mod/FreeCADPlus/TestComponentEligibility.py: consumer guard, shared/external ownership and fresh-process acceptance.
- src/Gui/ComponentGeometry.h: shared native modeling eligibility bridge for PartDesign/Sketcher.
- src/Mod/FreeCADPlus/TestComponentSweepInputs.py: Loft/Pipe reference admission, native transactions and independent recompute/persistence checks.
- src/Mod/PartDesign/Gui/TaskLoftParameters.cpp and TaskPipeParameters.cpp: picked profile, section and main/auxiliary path admission.
- src/Mod/FreeCADPlus/TestComponentInputEditors.py: Python attachment/Extrude input acceptance, confirmation/Undo and independent downstream checks.
- src/Mod/Part/AttachmentEditor/TaskAttachmentEditor.py and src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp: component admission for remaining attachment and Extrude face/shape inputs.
- src/Mod/FreeCADPlus/TestComponentReferences.py: native attachment/axis collector, atomic rejection, legacy bypass and downstream acceptance.
- src/Mod/Part/Gui/TaskAttacher.cpp and src/Mod/PartDesign/Gui/ReferenceSelection.cpp: component input guards for native attachment/shared picked references.
- src/Mod/FreeCADPlus/TestComponentModeling.py: native intake, transactions, legacy bypass and independent reopen checks.
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
