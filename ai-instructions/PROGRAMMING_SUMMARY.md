# FreeCAD Plus: Programming Summary

## Project at a glance

FreeCAD Plus is Croft-Labs' FreeCAD fork, a desktop parametric CAD application
using C++, Python, Qt, OpenCASCADE, and Coin; the GUI executable enters through
[`src/Main/MainGui.cpp`](../src/Main/MainGui.cpp).

## Where to go

| Task or question | Start here | Related reference |
| --- | --- | --- |
| Product intent and boundaries | [Product specification](PRODUCT_SPEC.md) | [UI scope](UI_UX_SPEC.md#interface-scope) |
| Planned `.cadprt` format and legacy `.FCStd` conversion | [Native-format policy](PRODUCT_SPEC.md#planned-native-format-and-legacy-import) | Roadmap 7.6; best-effort conversion with reported losses and untouched originals; not implemented yet |
| Part-level history architecture | [Logical history/result contract](architecture/PART_HISTORY_CONTRACT.md), [adapter decision boundary](architecture/ADR_001_HISTORY_ADAPTER_BOUNDARY.md) | Foundation and bounded placement/local-cut/consumer probes validated; Draft clone empty-source fix included; final choice/production history model pending |
| Temporary isolate/hide (F040) | [`TemporaryDisplay.py`](../src/Gui/TemporaryDisplay.py), standard View > Visibility menu | Native visibility with per-document nested restore; whole Body/link targets preserve model identities. [Owner procedure](../tests/TemporaryDisplay.md); roadmap 10.5a/b. |
| Command search (F033) | [`CommandSearch.py`](../src/Gui/CommandSearch.py), native standard Tools menu | Familiar aliases into existing commands, keyboard palette, explicit workbench switching and live availability. [Owner procedure](../tests/CommandSearch.md); roadmap 8.4.2a/b, 10.4. |
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
| Indexed STL CAM output | `Path/Main/IndexedSetup.py::require_current_geometry`, `Path/Op/Base.py::_bindModelDependencies` | Consume recomputed indexed producers and schedule stock dependencies; real-job LinuxCNC/Grbl output regressions in `tests/TestIndexedSetupExport.py`, roadmap 6.4.3. Native viewport/simulation remain separate. |
| Build or verify changes | [Development guide](DEVELOPMENT_GUIDE.md#commands) | [Pad test procedure](../tests/PadTaskPanel.md) |
| Priorities, completion, and blockers | [Roadmap](DEVELOPMENT_ROADMAP.md) | [Current focus](DEVELOPMENT_ROADMAP.md#current-focus) |
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

Sketch reattachment foundation: [`SketchReattachment.py`](../tests/prototypes/SketchReattachment.py)
and [`TestPartHistoryAdapters.py`](../tests/TestPartHistoryAdapters.py); roadmap 11.7a-x
covers test-only planar reattachment, local/world policies, missing-face repair,
transaction ownership, support validity/cycle checks and disposable-document placement
preview, reversed direction, expression-offset protection and explicit support scope.
Direct cross-container/occurrence supports reject; test-only PlanarSupport provides
an explicit cross-part reference with atomic creation/reattachment and deliberate
missing-face/source repair checks. `current_result_shape` in
[`PartHistoryAdapters.py`](../tests/prototypes/PartHistoryAdapters.py) prototypes
consumer rejection of invalid/unrecomputed cached results. Production editor and
graphical preview pending.

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
