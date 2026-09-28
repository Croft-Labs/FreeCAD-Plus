# FreeCAD Plus: Development Roadmap

## Current focus

- Active milestone: 2.2, compiled validation of the Pad task workflow.
- Target outcome: [REQ-001 through REQ-007](PRODUCT_SPEC.md#capabilities-and-requirements).
- Source implementation exists; build and GUI acceptance are still pending.
  This roadmap records status; it does not authorize new phases or external publication.
- The [Part Design workflow audit](#part-design-workflow-audit) inventories the
  remaining selection and complete-editing work. Audit complete; implementation pending.
- Preferred future command layout: [unified geometry workflows](#unified-feature-workflows)
  with Add/Subtract inside the task pane; candidate mapping documented, implementation pending.

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

- [   ] 2.2.1 Configure a compatible FreeCAD LibPack and build outside Google Drive.
  Status: blocked at configuration on 2026-09-28: MSVC 19.44 was detected, but
  `FREECAD_LIBPACK_DIR` had no usable LibPack. Follow [setup](DEVELOPMENT_GUIDE.md#prerequisites-and-setup).
- [   ] 2.2.2 Correct and run the focused GUI regressions against the built fork.
  Source-review finding during documentation adoption: the selector for
  `buttonStartReference` in `TestPadTaskPanel.py` asks for `QToolButton`, while
  `TaskPadPocketParameters.ui` defines `QPushButton`. Correct that test before execution.
  GUI tests have not run; this documentation task does not change test code.
- [   ] 2.2.3 Verify viewport picking, rotated profiles, both directions, keyboard input,
  visibility restoration, Cancel, and Undo/Redo; check Pocket for shared-base regressions.
  Acceptance: [UI-001](UI_UX_SPEC.md#ui-001-pad-task-pane) and [test procedure](../tests/PadTaskPanel.md).

## [   ] Phase 3: Further Part Design operations

Outcome: extend the complete task-pane workflow after Pad is validated and scope is authorized.
Depends on: milestone 2.2.

### [   ] 3.1 Define the next operation

Complete when: an operation and its create/edit acceptance criteria are approved.

- [   ] 3.1.1 Choose the next operation, such as revolve or a pattern, and define its input workflow.
  Status: future scope; no implementation authorized by this roadmap alone.
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

1. Creating and reopening use the same task container and controls. Geometry inputs
   appear first, show existing selections, and support selection after invocation.
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
- [   ] 3.6.2 Define and validate the operation-switching compatibility approach;
  inventory parameter mappings, existing Common behavior, and legacy entry points.
- [   ] 3.6.3 Implement Extrude as the recommended first unified family, integrating
  Pad validation and Pocket task 3.2.1 rather than creating duplicate new controls.
- [   ] 3.6.4 Implement Revolve, covering both tasks 3.2.3 and 3.2.4.
- [   ] 3.6.5 Implement Loft and Sweep, covering all four tasks in 3.3.
- [   ] 3.6.6 Implement Helix, covering tasks 3.2.5 and 3.2.6.
- [   ] 3.6.7 Implement paired primitive workflows and decide whether to expose them
  through one Primitive command; validate all eight shapes in both operations.
- [   ] 3.6.8 Verify Add-to-Subtract and Subtract-to-Add during creation and on reopened
  features: common parameter retention, incompatible-mode guidance, no-base handling,
  preview/recompute, dependent links and expressions, save/reopen, Cancel, and Undo/Redo.
  Test existing additive, subtractive, and Common documents and legacy commands.
