# FreeCAD Plus: Development Roadmap

## Current focus

- Active work: always-visible Extrude start offsets and adjacent direction buttons
  in milestone 3.8. Target: [REQ-013](PRODUCT_SPEC.md#capabilities-and-requirements).
  Combined Pattern automated validation is recorded in milestone 3.7.
- Extrude native build, 49 automated regressions, and task-pane visual inspection
  passed on 2026-09-28; see [validation evidence](#extrude-validation-evidence).
  Its manual viewport/keyboard acceptance remains pending in 2.2.3.
  This roadmap records status; it does not authorize new phases or external publication.
- The [Part Design workflow audit](#part-design-workflow-audit) inventories the
  remaining selection and complete-editing work. Audit complete; implementation pending.
- Preferred future command layout: [unified geometry workflows](#unified-feature-workflows)
  with Add/Subtract first in the task pane; Extrude passes the automated checks below.

## [ X ] Phase 1: Repository and instruction foundation

Outcome: an identifiable fork and usable project guidance.
Depends on: None.

### [ X ] 1.1 Establish the fork

Complete when: the repository, local checkout, remotes, and submodules are identified.

- [ X ] 1.1.1 Create the public `Croft-Labs/FreeCAD-Plus` fork and local checkout.
  Evidence: GitHub creation/verification in the setup session; upstream base `a5908bb06e`.
- [ X ] 1.1.2 Configure `origin` for the fork and `upstream` for FreeCAD; initialize submodules.
  Evidence: setup session verified remotes, recursive submodule status, and matching `main`.

### [ X ] 1.2 Adopt the shared instruction standard

Complete when: the root router, five core documents, and their references are checked.

- [ X ] 1.2.1 Add the local entry point and standard document ownership.
- [ X ] 1.2.2 Consolidate Pad guidance and preserve source/build/GUI distinctions.
  Evidence: documentation adoption change, with local link and heading checks on 2026-09-28.

## [   ] Phase 2: Pad task-pane workflow

Outcome: validated creation and editing through [UI-001](UI_UX_SPEC.md#ui-001-pad-task-pane).
Depends on: Phase 1.

### [ X ] 2.1 Implement the source change

Complete when: source and regression cases exist and source-level checks pass.

- [ X ] 2.1.1 Allow opening Pad without preselection; add profile controls to its shared create/edit dialog.
- [ X ] 2.1.2 Add selection restrictions, profile removal, and empty-profile handling.
- [ X ] 2.1.3 Add 14 GUI regression cases and register them in the GUI test suite.
  Evidence: local commit `e35fea1841`; C++ formatting, Python syntax, and whitespace checks passed.
  These checks do not establish compiled correctness or passing GUI tests.

<a id="pad-validation"></a>

### [   ] 2.2 Build and validate the changed application

Complete when: this fork builds and the focused suite plus manual UI acceptance pass.

- [ X ] 2.2.1 Configure a compatible FreeCAD LibPack and build outside Google Drive.
  Windows x64 Release GUI, Part, Sketcher, and Part Design targets built successfully.
  Fixed the profile selector to use `Shape.getShape()` for FreeCAD's `TopoShape`
  methods; `getValue()` returns the raw OpenCASCADE shape and did not compile.
- [ X ] 2.2.2 Correct and run the focused GUI regressions against the built fork.
  All 21 task-pane tests passed. Tests now search the active dialog, retain the
  layout's parent wrapper, and reopen via the user double-click entry point so
  edit transactions are exercised. The earlier `QPushButton` selector fix is included.
- [   ] 2.2.3 Verify viewport picking, rotated profiles, both directions, keyboard input,
  visibility restoration, Cancel, and Undo/Redo; check Pocket for shared-base regressions.
  Automated selection, visibility, Cancel, Undo/Redo, and Pocket regressions pass.
  Physical viewport/tree picking, rotated previews, keyboard navigation, and the
  complete advanced-parameter click-through remain manual acceptance work.
  Acceptance: [UI-001](UI_UX_SPEC.md#ui-001-pad-task-pane) and [test procedure](../tests/PadTaskPanel.md).

<a id="extrude-validation-evidence"></a>

#### Validation evidence, 2026-09-28

Tested this checkout at `f9d592dc1f` plus the selector and test-fixture corrections
in this validation change. The source-built application reported FreeCAD 26.3.0;
the separately installed FreeCAD was not launched or used.

| Check | Result |
| --- | --- |
| Native model tests | `TestExtrude`: 8/8; existing `TestPad`: 14/14; existing `TestPocket`: 6/6. No failures, errors, or skips. |
| Native GUI tests | `TestPadTaskPanel`: 14/14; `TestExtrudeTaskPanel`: 7/7. No failures, errors, or skips. |
| Task-pane inspection | Captured and inspected Add and Subtract in the built GUI. Operation is first, Profile is second, and shared dimensions remain visible. |
| Toolbar and material result | One `PartDesign_Extrude` action in the modeling toolbar. The same `Pad` object and `Profile` produced 1080 mm3 in Add and 920 mm3 in Subtract. |
| Remaining limits | GUI tests use Qt controls and FreeCAD selection APIs; they do not establish physical mouse/keyboard acceptance. Unrelated workbenches, C++ developer tests, and cross-version recomputation in upstream FreeCAD were not tested. |

Build and test artifacts are outside Google Drive at
`D:\Temp\Office-PC\freecad-plus-validation-20260928`:
`configure-command.txt` / `configure.log`, `build-initial.log`, successful
`repair-compile.log`, `repair-resource0.log`, `repair-resource1.log`, `repair-link.log`,
`model-results.json`, `results.json`, per-suite logs, `visual-check.json`, and
`extrude-add.png` / `extrude-subtract.png`. Executable: `build\bin\FreeCAD.exe`.

The fork build used source-pinned `LibPack-26.3.0-v3.5.3-x64-Release` and MSVC
19.44.35211. Archive SHA-256:
`DCAA2D21F61B0607CF06B6E98F6E7525DC266C04C20E7B4D7B2C77BEC24366E7`.
Focused build and test reproduction guidance is in the
[development guide](DEVELOPMENT_GUIDE.md#commands). Settings and test documents
were isolated from the normal user profile. No push, installer, or release was made.

## [   ] Phase 3: Further Part Design operations

Outcome: extend the complete task-pane workflow after Pad is validated and scope is authorized.
Depends on: milestone 2.2.

### [ X ] 3.1 Define the next operation

Complete when: an operation and its create/edit acceptance criteria are approved.

- [ X ] 3.1.1 Choose the next operation and define its input workflow.
  Evidence: user selected unified Pad/Pocket Extrude, with Add/Subtract as the first
  dropdown, and requested implementation on 2026-09-28.
  Plan paired operations as unified workflows under 3.6, rather than duplicating their
  new task controls. The individual tasks below remain coverage checks for both modes.
- [ X ] 3.1.2 Audit Part Design profile selection and shared create/edit task workflows.
  Evidence: source review on 2026-09-28 at `e0517bc4bd`, recorded below. No application
  or GUI tests were run for this audit; the installed FreeCAD was not used.

<a id="part-design-workflow-audit"></a>

#### Profile-selection findings

**Ten remaining operations share Pad's former startup workflow:** Pocket, Hole,
Revolution, Groove, Additive Loft, Subtractive Loft, Additive Pipe, Subtractive Pipe,
Additive Helix, and Subtractive Helix. Pad's source change is already recorded in
milestone 2.1; its acceptance remains in [milestone 2.2](#pad-validation).
This inventory describes the audited baseline. Pocket's subsequent source update
is tracked in 3.6.3; it no longer uses that startup picker without preselection.

In [`Command.cpp`](../src/Mod/PartDesign/Gui/Command.cpp), these ten commands call
`prepareProfileBased`. Without preselection, it searches for sketches, automatically
uses the sole eligible sketch, or opens a separate `TaskDlgFeaturePick`; it can reject
the command when no sketch exists. Thus, preselection is not literally mandatory in
every case, but the main feature editor cannot simply open with an empty profile
and let the user choose its inputs there. Required Body/base-solid prerequisites
remain legitimate, particularly for subtractive operations.

`finishFeature` opens edit mode, and
[`ViewProvider::setEdit`](../src/Mod/PartDesign/Gui/ViewProvider.cpp) obtains
`getEditDialog` for both newly created and existing features. These operations already
share their main dialog between creation and editing; that alone does not make the
definition fully editable. The following table separates missing profile controls
from existing controls that need a better entry workflow.

| Operation | Profile editing in the current task pane | Planned work / owning task |
| --- | --- | --- |
| Pad | New profile list supports selection, removal, and clearing in the shared editor. | Validate existing implementation in 2.2; include it in the complete-parameter audit in 3.4.1. |
| Pocket | [`TaskPocketParameters`](../src/Mod/PartDesign/Gui/TaskPocketParameters.cpp) uses the shared extrusion controls but has no Pad-style profile editor. | 3.2.1: open empty; add the profile section while retaining extent, direction, and start/end references. |
| Hole | [`TaskHoleParameters`](../src/Mod/PartDesign/Gui/TaskHoleParameters.cpp) edits hole settings and start references, not the `Profile` link. Its base-profile-type filter does not replace source selection. | 3.2.2: open empty; select/replace hole inputs and preserve supported circles, arcs, and points, plus size, depth, thread, and cut options. |
| Revolution | [`TaskRevolutionParameters`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.cpp) selects axis/start references but does not replace `Profile`. | 3.2.3: profile section plus existing angle, axis, direction, and extent controls. |
| Groove | Shares the revolution parameter implementation; no profile replacement control. | 3.2.4: the equivalent subtractive workflow, including base-solid validation. |
| Additive Helix | [`TaskHelixParameters`](../src/Mod/PartDesign/Gui/TaskHelixParameters.cpp) selects the axis but does not replace `Profile`. | 3.2.5: profile section plus helix modes, dimensions, axis, and handedness. |
| Subtractive Helix | Shares the helix editor and the missing profile control. | 3.2.6: equivalent subtractive workflow, including base-solid validation. |
| Additive Loft | [`TaskLoftParameters`](../src/Mod/PartDesign/Gui/TaskLoftParameters.cpp) already replaces the base profile and adds/removes/reorders sections. A profile pick replaces the link with one picked source/subelement; it is not Pad's accumulated curve list. | 3.3.1: enter directly with empty inputs; expose clear profile/section lists and preserve ordered-section editing. |
| Subtractive Loft | Same selectors and startup gate as Additive Loft. | 3.3.2: equivalent subtractive workflow. |
| Additive Pipe | [`TaskPipeParameters`](../src/Mod/PartDesign/Gui/TaskPipeParameters.cpp) already replaces the profile and edits spine references. Orientation and section/scaling controls share the task dialog. | 3.3.3: enter directly with empty inputs; complete profile, path, auxiliary-reference, and section editing in that dialog. |
| Subtractive Pipe | Same selectors and startup gate as Additive Pipe. | 3.3.4: equivalent subtractive workflow. |

#### Other Part Design features: complete-editing audit

Inventory follows the registered commands and menus in
[`Workbench.cpp`](../src/Mod/PartDesign/Gui/Workbench.cpp) and `Command.cpp`.
An existing selector below is source evidence, not a claim of full GUI acceptance.
These features must not be counted as ten additional profile-startup defects.

| Features | Source finding | Remaining work |
| --- | --- | --- |
| Mirrored, Linear Pattern, Polar Pattern | `prepareTransformed` can start without selected originals using Whole shape mode. [`TaskTransformedParameters`](../src/Mod/PartDesign/Gui/TaskTransformedParameters.cpp) adds/removes originals and changes mode. [`TaskMirroredParameters`](../src/Mod/PartDesign/Gui/TaskMirroredParameters.cpp) and [`TaskPatternParameters`](../src/Mod/PartDesign/Gui/TaskPatternParameters.cpp) provide reference/parameter controls in the reused editors. | 3.4.2: verify originals, whole-shape mode, plane/axes/directions, counts and spacing/angles on both create and reopen. No Pad-style profile prerequisite identified. |
| MultiTransform, including Scale | [`TaskMultiTransformParameters`](../src/Mod/PartDesign/Gui/TaskMultiTransformParameters.cpp) manages an ordered transformation list and embedded editors for mirror, linear, polar, and scale operations. | 3.4.2: verify adding, editing, removing, and ordering child transformations without leaving the parent task. Standalone `PartDesign_Scaled` registration is commented out; do not count it as a normal menu command. |
| Circular Pattern, Path Pattern, Point Pattern model types | `TaskPatternParameters` contains controls for these model types, but the audited Part Design command/menu registration does not expose standalone commands for them. | 3.4.2: cover existing documents containing these types and establish supported entry paths before proposing new commands. Do not infer a missing-curve-startup defect from class names alone. |
| Fillet, Chamfer, Draft, Thickness, Defeaturing | Commands accept no preselection and use the active Body Tip. [`TaskDressUpParameters`](../src/Mod/PartDesign/Gui/TaskDressUpParameters.cpp) edits edge/face references on the existing base. Individual task panels hold operation parameters; Draft also selects neutral-plane/pull-direction references. | 3.4.3: validate all subelement and parameter changes. The selector fixes the source to the current base object: define safe base replacement or explain a required Body-history constraint inside the task. |
| Boolean | The command can create an empty tool list; [`TaskBooleanParameters`](../src/Mod/PartDesign/Gui/TaskBooleanParameters.cpp) adds/removes tools and changes operation type in the shared editor. | 3.4.4: verify tool replacement/removal, operation switching, empty-state recovery, and Body dependency restrictions. |
| Additive and Subtractive Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism, Wedge | [`CommandPrimitive.cpp`](../src/Mod/PartDesign/Gui/CommandPrimitive.cpp) creates these without curve input. [`TaskPrimitiveParameters`](../src/Mod/PartDesign/Gui/TaskPrimitiveParameters.cpp) combines geometry controls, attachment, and preview in the edit dialog. | 3.4.5: verify dimensions and placement/attachment for all 16 variants on create and reopen. Changing to a different primitive class is not ordinary parameter editing. |
| Shape Binder | [`TaskShapeBinder`](../src/Mod/PartDesign/Gui/TaskShapeBinder.cpp) supports selecting, changing, and clearing support references. Creation and editing use its task dialog. | 3.5.1: verify empty startup, support changes, tracking options, and transaction behavior. |
| Sub-Shape Binder | The command directly creates/links the binder. [`ViewProviderSubShapeBinder`](../src/Mod/PartDesign/Gui/ViewProviderShapeBinder.cpp) supplies synchronize/select-source actions, without a dedicated definition task editor. | 3.5.2: add a shared create/edit task for supports and applicable binding options. This is a task-editor gap, not the profile-based startup gate. |
| Clone / Base Feature | `CmdPartDesignClone` requires exactly one selected Part feature and directly creates a new Body/base feature. [`ViewProviderBase`](../src/Mod/PartDesign/Gui/ViewProviderBase.cpp) exposes placement editing when mutable, not a complete source-definition editor. | 3.5.3: plan one create/edit task for source and supported placement changes, preserving base-feature and Body semantics. |
| Datum Point, Datum Line, Datum Plane, Coordinate System | Current menus invoke Part datum commands. [`ViewProviderDatum`](../src/Mod/Part/Gui/ViewProviderDatum.cpp) routes to the attachment editor, including from creation. | 3.5.4: verify support, attachment mode, and offsets through the same task; these are reference geometry, not extrusion-profile features. |
| Involute Gear, Sprocket | [`InvoluteGearFeature.py`](../src/Mod/PartDesign/InvoluteGearFeature.py) and [`SprocketFeature.py`](../src/Mod/PartDesign/SprocketFeature.py) create objects then enter their respective task editors; editing reuses those panels. | 3.5.5: compare editable model properties against panel controls and test both entry paths. The standalone `fcsprocketdialog.py` demo is not the workbench command's editor. |
| Shaft Design Wizard, when available | [`WizardShaft.py`](../src/Mod/PartDesign/WizardShaft/WizardShaft.py) opens a task workflow, conditionally exposed by the workbench. It is not routed through the standard feature `getEditDialog` path. | 3.5.6: inspect generated-object re-entry and rollback before claiming create/edit parity; availability and behavior remain unverified. |

Sketch creation/editing belongs to the dedicated Sketcher workflow. Editing source
sketch geometry is distinct from selecting a feature's profile. Body creation,
setting Tip, moving/duplicating objects, material tools, and geometry inspection are
management or inspection actions rather than profile-consuming feature definitions;
they are outside this feature-dialog backlog.

**Cross-cutting parameter gap:**
[`FeatureRefine.cpp`](../src/Mod/PartDesign/App/FeatureRefine.cpp) defines editable
`Refine` and `FuzzyTolerance` properties, inherited by profile features, dress-ups,
transformations, primitives, and Boolean. The audited Part Design task-panel sources
contain no controls for these properties. Therefore even panels with input selectors
cannot yet be declared complete replacements for property-editor changes. Task 3.4.1
owns the common controls and the remaining property-by-property coverage audit.

<a id="feature-task-acceptance"></a>

#### Acceptance for every feature implementation milestone

These are backlog completion criteria. Detailed operation-specific screen behavior
belongs in the UI specification when that operation is selected for implementation.

1. Creating and reopening use the same task container and controls. For unified
   Add/Subtract families, Operation is first, immediately followed by geometry inputs
   showing existing selections and supporting selection after invocation.
   Multiple sections within that task are acceptable; a separate prerequisite picker
   or property-editor detour must not be required to define the feature.
2. Add, remove, clear, and replace inputs as supported by the feature; reorder ordered
   inputs such as loft sections and transformation steps. Retain valid preselection.
   Match each model's supported geometry, including Hole points/arcs, pipe paths, and
   loft sections; do not impose Pad's profile restrictions on every feature.
3. Cover the feature's editable definition: dimensions, modes, references, directions,
   secondary extents, advanced geometry options, and applicable placement/attachment.
   Audit persisted properties against controls, preserving units and expressions.
   Computed/internal properties and incompatible object-class changes are excluded;
   any intentionally fixed structural dependency must have an explicit rationale.
4. Empty/incomplete inputs stay editable with clear guidance and safe preview behavior.
   Invalid geometry or dependency cycles cannot be accepted. Inspect constructors,
   gizmos, and selection handlers for null-profile assumptions before bypassing pickers.
5. Verify create with/without preselection, reopen and replace inputs, change each
   supported mode, clear/recover, accept/save/reopen, Cancel, and Undo/Redo. Check tree
   and viewport picking, visibility restoration, and unchanged downstream dependencies.
   Run focused regressions in the built fork and manual viewport acceptance; record
   source, build, test, and GUI evidence separately.

### [   ] 3.2 Add missing in-task profile controls

Depends on: 2.2 and 3.1.1 for the selected operation.
Complete when: each operation passes the [common acceptance](#feature-task-acceptance),
including profile replacement while editing an existing feature.

- [   ] 3.2.1 Pocket: replace the startup picker with the shared feature task and profile controls.
  Source and automated validation completed through 3.6.3; manual viewport
  acceptance remains in 2.2.3.
- [   ] 3.2.2 Hole: add input selection with Hole-specific geometry rules.
- [   ] 3.2.3 Revolution: add profile selection alongside axis and revolution controls.
- [   ] 3.2.4 Groove: provide equivalent subtractive profile editing.
- [   ] 3.2.5 Additive Helix: add profile selection alongside helix controls.
- [   ] 3.2.6 Subtractive Helix: provide equivalent subtractive profile editing.

### [   ] 3.3 Complete Loft and Pipe input workflows

Depends on: 2.2 and operation-specific scope under 3.1.1.
Complete when: all four operations open their main task with empty inputs and pass
the [common acceptance](#feature-task-acceptance), reusing their existing selectors.

- [   ] 3.3.1 Additive Loft: integrate base-profile and ordered-section selection from startup.
- [   ] 3.3.2 Subtractive Loft: integrate the equivalent subtractive workflow.
- [   ] 3.3.3 Additive Pipe: integrate profile, spine, auxiliary references, and section/scaling controls.
- [   ] 3.3.4 Subtractive Pipe: integrate the equivalent subtractive workflow.

### [   ] 3.4 Close complete-editing gaps in solid features

Depends on: 2.2 and scoped implementation choices in 3.1.1; may proceed by family.
Complete when: the common parameter gap is addressed and each listed family passes
the [common acceptance](#feature-task-acceptance). Existing controls need validation,
not automatic replacement.

- [   ] 3.4.1 Add shared advanced geometry controls for `Refine` and `FuzzyTolerance`
  where applicable; inventory other editable properties missing from each task,
  including Pad, and implement required controls with regression coverage.
- [   ] 3.4.2 Validate Mirrored, Linear/Polar Pattern, and MultiTransform create/edit
  parity, including nested Scale and supported Circular/Path/Point Pattern objects.
- [   ] 3.4.3 Complete Fillet, Chamfer, Draft, Thickness, and Defeaturing reference/parameter
  editing; resolve the current fixed-base selection boundary without invalid history.
- [   ] 3.4.4 Validate Boolean's complete tool and operation workflow.
- [   ] 3.4.5 Validate all additive/subtractive primitive dimensions and attachment workflows.

### [   ] 3.5 Complete supporting-feature task workflows

Depends on: scoped implementation choices in 3.1.1 and the common acceptance criteria.
Complete when: each included helper has a documented and validated create/edit path;
conditional wizard scope is explicitly resolved.

- [   ] 3.5.1 Validate Shape Binder support and parameter editing.
- [   ] 3.5.2 Implement a shared Sub-Shape Binder definition task.
- [   ] 3.5.3 Implement Clone source/placement creation and editing in one task.
- [   ] 3.5.4 Validate datum and coordinate-system attachment editing.
- [   ] 3.5.5 Audit and complete Involute Gear and Sprocket task parameter coverage.
- [   ] 3.5.6 Establish Shaft Design Wizard availability and edit/re-entry semantics;
  resolve any missing persisted-definition and cancel behavior before scheduling a fix.

<a id="unified-feature-workflows"></a>

### [   ] 3.6 Unify opposite operations into geometry workflows

Outcome: implement the user's preferred one-command workflow with Add/Subtract in
the task pane, as defined by [REQ-008/009](PRODUCT_SPEC.md#capabilities-and-requirements)
and the [shared interaction](UI_UX_SPEC.md#planned-unified-feature-interaction).
Depends on: 2.2, operation-specific selection coverage in 3.2/3.3/3.4, and a safe
operation-switching design. These can be developed together by feature family;
finishing all separate commands first is not required.
Complete when: each selected family passes the [common acceptance](#feature-task-acceptance)
plus operation-switching and legacy-document regressions below.

#### Strong candidates: additive/subtractive pairs

Source-backed planning inventory, 2026-09-28. Names below are proposed primary
commands; existing API/document type names remain compatibility concerns.

| Proposed command | Current features combined | Common parameters / inputs | Differences to preserve |
| --- | --- | --- | --- |
| Extrude | Pad + Pocket | Profile, start plane/offset, direction, side arrangement, lengths, limiting references, taper | Extent modes differ: Pad has UpToLast, Pocket has ThroughAll. Map modes by meaning, not enum index; validate direction and material result when switching. |
| Revolve | Revolution + Groove | Profile, axis, angle, side arrangement, start and limiting references | Retain each mode's extent/geometry rules and the subtractive base-solid prerequisite. |
| Loft | Additive Loft + Subtractive Loft | Base profile, ordered sections, ruled/closed options | Keep section compatibility and additive/subtractive result validation. |
| Sweep (Pipe) | Additive Pipe + Subtractive Pipe | Profile, spine, orientation, auxiliary spine, section/scaling options | Preserve path/section semantics and validate the resulting union or cut. |
| Helix | Additive Helix + Subtractive Helix | Profile, axis, pitch/height/turns modes, handedness, growth | Preserve helix mode dependencies and existing subtractive intersection/outside compatibility. |
| Box | Additive Box + Subtractive Box | Length, width, height, placement/attachment | Same primitive geometry; operation changes how it combines with the Body. |
| Cylinder | Additive Cylinder + Subtractive Cylinder | Radius, height, angle, placement/attachment | Same primitive geometry; validate union/cut result. |
| Sphere | Additive Sphere + Subtractive Sphere | Radius, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Cone | Additive Cone + Subtractive Cone | Radii, height, angle, placement/attachment | Same primitive geometry; validate union/cut result. |
| Ellipsoid | Additive Ellipsoid + Subtractive Ellipsoid | Radii, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Torus | Additive Torus + Subtractive Torus | Radii, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Prism | Additive Prism + Subtractive Prism | Polygon count, radius, height, placement/attachment | Same primitive geometry; validate union/cut result. |
| Wedge | Additive Wedge + Subtractive Wedge | Wedge bounds/dimensions, placement/attachment | Same primitive geometry; validate union/cut result. |

This combines **26 existing feature variants into 13 paired workflows**. The eight
primitive workflows can also share one **Primitive** command with a shape selector,
yielding six top-level families: Extrude, Revolve, Loft, Sweep, Helix, Primitive.
Changing an existing primitive's shape type needs its own compatibility design;
it is not implied by changing Add/Subtract for that same primitive.

#### Additional consolidation options

| Candidate | Possible shared workflow | Recommendation / boundary |
| --- | --- | --- |
| Linear Pattern, Polar Pattern, Mirrored; MultiTransform with Scale | Pattern/Transform with a type selector and shared original-feature list | A useful second-stage consolidation, but these are different transformations, not Add/Subtract opposites. Reuse MultiTransform's step editing; retain type-specific parameters. Circular/Path/Point model types need supported entry-path review under 3.4.2. |
| Boolean union, subtraction, intersection | Boolean with operation and tool-body selectors | Already one feature/editor; align naming and interaction with the shared operation selector rather than create another command. |
| Fillet and Chamfer | Optional Edge Treatment command with Round/Chamfer type | Shared edge selection is reusable, but curvature and parameter semantics differ. Lower priority than true additive/subtractive pairs; combining them is an option, not an agreed requirement. |

Keep **Hole** specialized for hole standards, threads, and counterbores/countersinks.
Keep Draft, Thickness, and Defeaturing distinct: they modify geometry in different
ways and are not opposite operations. Binders, Clone, datums, gears, and sketches
retain their own workflows while sharing appropriate selection and task conventions.

#### Implementation evidence and constraints

- Extrude already shares [`TaskExtrudeParameters`](../src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp).
  Revolution/Groove share [`TaskRevolutionParameters`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.cpp);
  Loft, Pipe, Helix, and primitive pairs also reuse their family task implementation.
  UI consolidation can build on those existing paths.
- [`FeatureAddSub`](../src/Mod/PartDesign/App/FeatureAddSub.cpp) already defines an
  `Operation` property, but `defineAdditive` restricts it to Union and
  `defineSubtractive` to Subtraction/Common. Existing operation controls do not make
  all feature types freely interchangeable. Inspect each geometry execution path
  and persistence behavior before implementing a shared selector.
- [`Pad::TypeEnums`](../src/Mod/PartDesign/App/FeaturePad.cpp) and
  [`Pocket::TypeEnums`](../src/Mod/PartDesign/App/FeaturePocket.cpp) demonstrate why
  copying raw property indices between feature types is unsafe. Preserve common
  parameters by meaning and identify incompatible settings explicitly.
- Unifying command presentation is separate from changing a stored object class.
  Decide how switching a committed feature between Add/Subtract preserves its
  identity, dependent links, expressions, and recompute history. Do not silently
  delete/recreate features or rename existing serialized types to match toolbar labels.

- [ X ] 3.6.1 Inventory combined-workflow candidates and record the preferred interaction.
  Evidence: the paired-feature/source mapping above; this is design documentation only.
- [ X ] 3.6.2 Define and validate the operation-switching compatibility approach;
  inventory parameter mappings, existing Common behavior, and legacy entry points.
  Source approach: retain Pad/Pocket objects and their links; append enum choices
  without changing legacy indices; match extent modes by name; restore old Operation
  lists with the saved meaning intact. Geometry direction remains independent of
  Add/Subtract. Existing Common features keep Intersect in their dropdown. Save/reopen
  and legacy-document model regressions passed, along with both legacy GUI entry
  points; see [evidence](#extrude-validation-evidence). Cross-version recomputation
  of switched features in unmodified upstream FreeCAD is not established.
- [   ] 3.6.3 Implement Extrude as the recommended first unified family, integrating
  Pad validation and Pocket task 3.2.1 rather than creating duplicate new controls.
  Source implemented on 2026-09-28: `PartDesign_Extrude` replaces the two standard
  menu/toolbar entries; legacy commands remain available. Both feature types share
  Extrude Parameters with Operation first, then Profile, and the existing dimensions.
  Switching changes the same object's Operation; To last and Through all remain
  separate choices. Subtract/Intersect require a base solid; incomplete tasks remain editable.
  Eight new model regressions, seven new GUI regressions, fourteen Pad GUI cases,
  and twenty existing Pad/Pocket model cases all pass in the built fork. The native
  build found and resolved the profile-selector API error recorded in 2.2.1.
  Task-pane layout and the single toolbar command were inspected in the built GUI.
  Source formatting, Python syntax, documentation links, and whitespace checks pass.
  Remaining gate: manual viewport/keyboard acceptance in 2.2.3; passing automated
  checks do not complete the common acceptance criteria for this milestone.
- [   ] 3.6.4 Implement Revolve, covering both tasks 3.2.3 and 3.2.4.
- [   ] 3.6.5 Implement Loft and Sweep, covering all four tasks in 3.3.
- [   ] 3.6.6 Implement Helix, covering tasks 3.2.5 and 3.2.6.
- [   ] 3.6.7 Implement paired primitive workflows and decide whether to expose them
  through one Primitive command; validate all eight shapes in both operations.
- [   ] 3.6.8 Verify Add-to-Subtract and Subtract-to-Add during creation and on reopened
  features: common parameter retention, incompatible-mode guidance, no-base handling,
  preview/recompute, dependent links and expressions, save/reopen, Cancel, and Undo/Redo.
  Test existing additive, subtractive, and Common documents and legacy commands.
  Automated coverage passed for both operations and legacy entry points, including
  parameter/identity retention, base-solid validation, save/reopen, Cancel, and
  Undo/Redo. Finish the manual rotated/reference/custom-direction, taper, start/end
  reference, and downstream-pattern scenarios in the [test procedure](../tests/PadTaskPanel.md).


<a id="combined-pattern-workflow"></a>

### [   ] 3.7 Combined Linear/Circular Pattern workflow

Outcome: [UI-002](UI_UX_SPEC.md#ui-002-pattern-task-pane) satisfies REQ-010/011/012.
Authorized by the user's request to combine pattern buttons with type first,
features second, and direction/axis and parameters after them. This advances the
Linear/Polar portion of 3.4.2; Mirror, Path, Point, concentric CircularPattern, and
other MultiTransform consolidation remain separate future work.

- [ X ] 3.7.1 Implement one Pattern command in standard menus/toolbars/task watchers.
  Creation without preselection and reopening the new Pattern share the same pane.
  Linear/Circular is first, followed by selected features and mode-specific controls.
  Keep legacy Linear/Polar commands and their persisted types unchanged.
- [ X ] 3.7.2 Preserve result identity and separate mode settings using a new
  `PartDesign::Pattern` feature backed by the existing MultiTransform engine.
  The result owns Linear/Polar parameter helpers in the same Body. Switching selects
  an existing helper; it does not replace the result, expressions, or original links.
  Empty patterns stay editable and cannot be accepted. Feature picks reject other
  bodies and dependents; list removal uses identity instead of labels/history order.
- [ X ] 3.7.3 Build and run model/GUI regressions and inspect the actual task layout.
  Windows x64 Release PartDesign App/Gui modules rebuilt with the existing MSVC/Qt
  LibPack configuration outside Google Drive. All **91 tests pass**: 58 model tests
  (Pattern 5, Linear 16, Polar 6, MultiTransform 3, Extrude 8, Pad 14, Pocket 6),
  plus 33 GUI tests (Pattern 12, Pad 14, Extrude 7), with no failures/errors/skips.
  Qt tests cover field ordering, no-preselection/face picking, mode switching, real
  direction/spacing/count controls, retained expressions, feature removal with
  duplicate labels/out-of-history order, invalid-body/dependent picks, empty-input
  rejection/recovery, same-pane reopening, Cancel, Undo/Redo, and legacy commands.
  Disabled live preview is honored and OK recomputes the final result.
  Existing MultiTransform embedded editing also passes. Corrected a Cancel cleanup
  path that could reapply parameters after rollback, and hid the embedded task
  controller to avoid overlaying the initial pane header.
  Task captures show Linear and Circular layouts in the requested order. The same
  Pattern result computes 8024 mm3 with three linear instances and 8032 mm3 with four
  circular instances in the regression fixture. Physical interaction remains 3.7.4.
  Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
  `pattern-model-results.json`, `pattern-gui-results.json`, `pattern-visual-check.json`,
  `pattern-linear.png`, `pattern-circular.png`, and `pattern-build-*.log`.
  The initial build found a task-header API mismatch, corrected to `setHeaderText`.
  The GUI harness invokes FreeCAD's unsigned count slot; using Qt's signed setter
  initially requested an excessive count, so that run was stopped and corrected.
  Final build/link and runtime reports supersede those intermediate failures.
  Source formatting, Python syntax, whitespace, and documentation checks pass.
  Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
  This is an incremental development build; its About/version stamp still reflects
  the earlier main-executable build, while the changed App/Gui modules are rebuilt.
- [   ] 3.7.4 Complete physical viewport/keyboard/high-DPI acceptance using
  [the Pattern procedure](../tests/PatternTaskPanel.md). Automated Qt interaction and
  captured layout inspection do not establish this manual gate.

Compatibility boundary: old Linear/Polar features keep their existing full editor;
there is no automatic conversion to the new type. Unmodified upstream FreeCAD does
not recognize `PartDesign::Pattern`; cross-version recomputation and release packaging
are not established. This work is local and does not authorize a push or publication.

### [   ] 3.8 Extrude start offset and direction controls

Outcome: REQ-013 is available in the shared new/edit Extrude pane for Pad and Pocket.
Existing signed StartOffset, StartType, and Reversed properties retain their model
semantics; no stored property or object migration is introduced.

- [ X ] 3.8.1 Expose the zero-default start offset in all three direction modes,
  automatically activate Offset when a distance is entered, and add a flip button
  that negates the value or its expression. Retain reference starts and explicit
  Profile plane reset.
- [ X ] 3.8.2 Replace the Reversed checkbox with synchronized buttons beside each
  length. Keep reversal beside Type for non-dimensional extents and disable it for
  symmetric Dimension. Keep the start-offset viewport gizmo available at zero.
- [ X ] 3.8.3 Rebuild the GUI module and run native geometry/task regressions; inspect
  the actual task-pane layout. Windows x64 Release GUI module rebuilt and linked
  using the existing MSVC/Qt LibPack environment outside Google Drive. All **42 GUI
  tests pass**: Extrude 16 (nine new cases), Pad 14, Pattern 12; no failures/errors/skips.
  Native tests assert positive/negative offset geometry in all three modes,
  Add/Subtract and legacy Pocket behavior, both synchronized length buttons,
  non-dimensional reversal, reference starts, expression flipping and rollback,
  save/reopen, Cancel, and Undo/Redo. Captured one-sided, two-sided, and symmetric
  task layouts were inspected; offset and length buttons align with their fields.
  Formatting, Python syntax, UI XML, whitespace, and documentation checks pass.
  Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
  `extrude-offset-gui-results.json`, `extrude-offset-visual-check.json`,
  `extrude-offset-one-side.png`, `extrude-offset-two-sides.png`,
  `extrude-offset-symmetric.png`, and `extrude-offset-build-*.log`.
  Final successful compile/link and tests supersede intermediate compile errors
  from a protected expression-widget API and a removed checkbox reference.
  Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
  Incremental GUI module update; the main executable About/version stamp still
  reflects its earlier build. The separately installed FreeCAD was not used.
- [   ] 3.8.4 Complete physical viewport/keyboard/high-DPI acceptance using the
  [Extrude procedure](../tests/PadTaskPanel.md#start-offset-and-direction-buttons).

This work is local; publication and release packaging are not part of this task.
