# FreeCAD Plus: Programming Summary

## Project at a glance

FreeCAD Plus is Croft-Labs' FreeCAD fork, a desktop parametric CAD application
using C++, Python, Qt, OpenCASCADE, and Coin; the GUI executable enters through
[`src/Main/MainGui.cpp`](../src/Main/MainGui.cpp).

## Where to go

| Task or question | Start here | Related reference |
| --- | --- | --- |
| Reviewed face extension (F066) | [`ExtendFaceReview.py`](../src/Mod/Surface/ExtendFaceReview.py), [`ExtendFaceGui.py`](../src/Mod/Surface/ExtendFaceGui.py), native `Surface::Extend` | Existing Surface Extend Face command: explicit U/V approximation, view-only preview and transactional associative creation. [Owner procedure](../tests/ExtendFaceReview.md); roadmap 13.1e/f owns validation. |
| Joint motion/limit review (F076) | [`JointObject.py`](../src/Mod/Assembly/JointObject.py), native Assembly joint task | Relative-motion guidance, exact reference tooltips and enabled-limit refusal/recovery before solver normalization. [Owner procedure](../tests/JointReview.md); roadmap 12.4c/d. |
| Window/crossing selection (F039) | [`BoxSelection.cpp`](../src/Gui/Selection/BoxSelection.cpp), [`MouseSelection.cpp`](../src/Gui/MouseSelection.cpp) | Full projected enclosure, directional borders and filter-aware native collection. [Owner procedure](../tests/WindowSelection.md); roadmap 10.5g/h. |
| Entity selection filters (F035) | [`EntitySelectionFilter.py`](../src/Gui/EntitySelectionFilter.py), native [`Selection.cpp`](../src/Gui/Selection/Selection.cpp) | View > Visibility > Selection filters: session vertex/edge/face/whole-object policy, command-gate intersection and visible reset. [Owner procedure](../tests/EntitySelectionFilter.md); roadmap 10.5e/f owns validation. |
| Component document architecture | [Approved component contract](architecture/COMPONENT_DOCUMENT_CONTRACT.md) | Active owner priority: roadmap 7.8; Component Structure, Model History and `.cadprt` |
| Component model and navigators | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py) | Shared definitions, evaluated results/references, representations and isolated views; [architecture decision](architecture/ADR_003_COMPONENT_DOCUMENT.md). |
| Model History suppression | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), Model History | Dependent branch/result restoration, shared-consumer visibility, bulk single-Undo changes and blocking-input tooltips; roadmap 7.8.5e. Native recompute scheduling remains open. |
| Component geometry conversion | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), Model History Convert to Dumb Object | Read-only removal/retention review, geometry-only exclusive-history pruning, identity-preserving freezing and independent extraction; roadmap 7.8.6c. |
| Component instance separation | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py) | Copy to New Part retains occurrence references, nested display choices and active edit context; geometry-only dependency eligibility; roadmap 7.8.8c. |
| Component file recovery | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), Component Structure, native `PropertyXLink` | Grouped missing instances, identity-based Locate Component File, partial reference recovery and clearing obsolete saved link targets; roadmap 7.8.3c. |
| Component reference recovery | [`ComponentModel.py`](../src/Mod/Part/ComponentModel.py), [`CadDocument.py`](../src/Mod/Part/CadDocument.py), Model History | Repairable missing geometry, independent refresh and identity-preserving direct-child source repair; roadmap 7.8.4a. |
| Component selection and view context | [`ComponentSelection.py`](../src/Gui/ComponentSelection.py), [`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py) | Native occurrence-path selection, direct-child reference preselection, grouped display Undo and isolated-tab context; roadmap 7.8.7f. |
| Independent component sketches | [`ComponentSketch.py`](../src/Mod/Part/ComponentSketch.py), [`ComponentSketchTask.py`](../src/Gui/ComponentSketchTask.py) | Body-independent native New Sketch plane/face workflow; roadmap 7.8.5d. |
| Component Extrude feedback task | [`ComponentExtrude.py`](../src/Mod/Part/ComponentExtrude.py), [`ComponentExtrudeTask.py`](../src/Gui/ComponentExtrudeTask.py), native Part Design command routing | Independent profile/result workflow with explicit New Body/Add/Subtract and history editing; roadmap 7.8.5c/d and 7.8.7d/e. |
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
