# FreeCAD Plus: Product Specification

## Purpose and users

Improve FreeCAD's feature workflows for CAD users who want to create and edit
parametric features in one task pane, including choosing their input geometry.

## Goals and success criteria

Users can start Extrude without preselection, choose Add/Subtract in the first
dropdown, select a valid profile, preview the result, and accept or cancel.
Editing an existing Pad or Pocket exposes
the same controls and preserves working document history. Acceptance is defined
in [the UI specification](UI_UX_SPEC.md#ui-001-pad-task-pane); implementation and
validation status belong in [the roadmap](DEVELOPMENT_ROADMAP.md).

Pattern users can choose Linear/Circular, select features after opening the command,
and configure the pattern in the same pane used for editing. The result remains the
same object when its pattern type changes; each type retains its own settings.

## Scope and non-goals

The current scope unifies Pad and Pocket as Extrude and Linear/Polar Pattern as
one Pattern command in the Part Design workbench. Pattern calls angular repetition
**Circular** in its task pane; the separate upstream concentric-circle pattern is
not part of this consolidation. Revolution and Groove also expose signed angular
start offsets and adjacent direction buttons; their command consolidation remains
future work. Trim Body adds associative solid/sheet trimming from Part and Part Design,
using a plane, selected face, or connected sheet cutter and a reversible keep side.
It creates a separate result object and preserves a source Part Design Body and its
Tip. Isocline Curve traces a specified draft angle on one or more oriented faces,
relative to a world axis, referenced plane/axis/edge, or custom vector. Its linked
wire result updates with the sources. The current CAM scope also includes direct
STL Parallel/Waterline machining and geometric stock-to-part holding tabs.
Other operations remain future work. The preferred direction is one command per geometry operation,
with Add/Subtract chosen inside its shared create/edit task, following the workflow
described by the user. The [candidate inventory](DEVELOPMENT_ROADMAP.md#unified-feature-workflows)
defines the planned families; it does not establish implemented behavior.
Application-wide rebranding, changing the geometry kernel,
multi-object profile aggregation, modifying the installed FreeCAD, and release
packaging are outside the current implementation scope.

## Named parameter pilot (F122)

The Part workbench exposes named length/angle parameters for an explicitly selected
native App::Part definition. Reuse native expressions, dimensional unit checks,
transactions, rename propagation and FCStd persistence. Parameter containers use
native App::FeaturePython properties and a read-only integer ParameterSetVersion
marker (version 1); no custom proxy, geometry ownership or format migration is added.
Existing unmarked objects are not automatically adopted. The command reuses one
marked set per selected Part, or requires explicit selection when several exist.

Users can create parameters with descriptions, edit expressions, rename, switch
display units and copy an internal-name expression reference for compatible fields
in the same document. Definition parameters are not silently localized to an
occurrence. Document/configuration scopes, where-used navigation, publication,
existing-description editing and automatic cross-document references remain future
increments. The usable pilot and owner acceptance are tracked separately in
[roadmap 10.8](DEVELOPMENT_ROADMAP.md#f122) and [UI-007](UI_UX_SPEC.md#ui-007-named-parameters-roadmap-108).

## Capabilities and requirements

| ID | Intended requirement |
| --- | --- |
| REQ-001 | Extrude creation and editing an existing Pad or Pocket open the same parameter editor. |
| REQ-002 | With an active body, starting Extrude or a legacy Pad/Pocket command without preselection opens the editor; it does not force a separate sketch picker or automatically choose a sketch. |
| REQ-003 | The first field is an Add/Subtract dropdown. The Profile section immediately follows and lets the user select, remove, or clear geometry within the task pane. |
| REQ-004 | Preserve preselection, whole-sketch selection, and individual edge/face selection from a supported source object. Ordinary selection clicks must retain already collected references. |
| REQ-005 | Valid geometry can be previewed and accepted; empty or invalid profiles remain editable and cannot be accepted. |
| REQ-006 | Cancel and Undo/Redo preserve feature/document integrity and restore temporary visibility changes. |
| REQ-007 | Profile selection cooperates with direction and limit-reference selectors, rejects invalid body/document/dependency links, and preserves existing Pad parameters. |
| REQ-008 | Planned unified feature families expose one geometry command with Add/Subtract in the same task pane used for creation and editing, retaining compatible selections and parameters when the operation changes. |
| REQ-009 | Operation changes preserve document history, references, expressions, and Cancel/Undo behavior. Unsupported parameter combinations require explicit handling; existing documents retain their intended geometry and persisted identities. |
| REQ-010 | Pattern has one standard menu/toolbar command. Its task pane starts with Linear/Circular, then feature selection, then direction/axis, extent or spacing, count, and applicable options. |
| REQ-011 | Pattern opens without preselection and uses the same complete pane when reopened. Switching type preserves its result identity, original-feature links, and independent per-type settings, including expressions and suppression. |
| REQ-012 | Empty or invalid patterns cannot be accepted; selection rejects other bodies and dependent features. Cancel, Undo/Redo, save/reopen, and legacy Linear/Polar/MultiTransform behavior remain supported. |
| REQ-013 | Extrude exposes a zero-default signed start offset in one-sided, two-sided, and symmetric modes, with an adjacent direction-flip button. Adjacent length-direction buttons replace the Reversed checkbox in the shared create/edit pane while preserving saved geometry semantics. |
| REQ-014 | Revolution (Add) and Groove (Subtract) expose a zero-default start offset from -360 to +360 degrees inclusive in one-sided, two-sided, and symmetric modes. Adjacent buttons reverse the signed offset and the existing revolution direction; creation and editing use the same controls, preserving expressions and document history. |
| REQ-015 | Trim Body opens without preselection in Part and Part Design. Target, tool, and keep-side controls share the same complete creation/editing task, with a visible direction arrow and live preview. |
| REQ-016 | Trim a solid or sheet with a datum plane, planar/curved face, or connected sheet. Planar tools may extend across the target; finite curved tools must fully separate it. Reverse selects the other side. Reject nonintersecting/incomplete cuts and keep solid outputs valid and closed. |
| REQ-017 | Persist target/tool links and recompute when their geometry or parent placement changes. Preserve source objects and Body Tip; Cancel, Undo/Redo, and reopening retain document integrity. Invalid edits clear stale output and cannot be accepted. |
| REQ-018 | Isocline Curve selects one or more target faces, a pull direction, and a draft angle in the same complete create/edit task. Preselection is optional. Axes, plane normals, straight edges, datum axes and a custom vector support direction selection and reversal. |
| REQ-019 | Use the draft convention n dot d = sin(angle), with unit oriented face normal n and unit pull d. Angle 0 degrees is the silhouette; 0..90 degrees is accepted. Trace source-surface curves within modeling tolerances and clip to face boundaries and holes. Report empty, isolated-point, and whole-face solutions instead of inventing curves. |
| REQ-020 | Persist face and direction references; recompute on geometry and parent-placement changes. Preserve source bodies and provide live preview, invalid-state recovery, Cancel, Undo/Redo, and save/reopen. The first version creates one angle per associative feature. |

### CAM mesh machining and stock bridges

| ID | Requirement |
| --- | --- |
| REQ-021 | A nonempty imported STL can be a CAM Job model without conversion to a CAD solid. Preserve triangles, placement, source association, and stock bounds. Parallel and Waterline machining use all selected job models. |
| REQ-022 | Expose Parallel/Waterline through the standard CAM interface when OpenCAMLib is available. Retain tool, feeds, depths, stepover, sampling, and path preview controls. Support separate three-axis jobs for two-sided and manually indexed machining, with an explicit orientation and work origin per setup. |
| REQ-023 | Create and edit visible stock-to-part bridges in the same task pane. Allow placement from the viewport and numeric position, length, width, height, and in-plane rotation. Reuse each Job's tabs across its Parallel/Waterline operations. |
| REQ-024 | Preserve tab material with cutter-radius clearance on cutting and linking moves. Changes invalidate affected paths. Invalid tab dimensions, insufficient safe height, unsupported strategies/motions, and tilted setups must not leave a stale usable path. Cancel, Undo/Redo, and save/reopen preserve links and geometry. |

Each indexed setup transforms the same source model, stock and physical tabs.
Changes to a shared tab update its dependent setups. A 180-degree flip and a
non-orthogonal index must be tested. Tilted tabs may use a conservative XY
protection envelope that leaves additional stock. Each setup is posted separately;
physical indexing and work-offset registration remain explicit operator steps.

Tabs represent protected stock, not fixture/holder collision models. This first version
leaves extra stock at bridge corners and retracts over the bridge. It does not implement
automatic rotary-axis motion, automatic bridge strength assessment, roughing, or a
complete machine/holder collision simulator. Existing profile holding-tag dressups
remain available in jobs without the new geometric tabs. Saved mesh clones and tabs
need FreeCAD Plus Python modules to recompute; upstream compatibility is not claimed.

## Constraints and quality requirements

- Retain FreeCAD's current single-source `Profile` property and closed-profile
  geometry requirements. Multiple subelements of that source are supported.
- Retain document format, Python API names, object types, units, and persisted
  properties unless a separately authorized migration defines otherwise.
- Preserve upstream licensing and attribution. Follow the applicable
  [contribution guidance](../CONTRIBUTING.md) and [AI policy](../AI_POLICY.md).
- Initial development is on Windows. Cross-platform inheritance is not evidence
  that fork changes have passed Linux/macOS validation.
- Build and GUI validation must use this checkout's binaries, never the
  separately installed FreeCAD. Follow [the guide](DEVELOPMENT_GUIDE.md).

## Planned native format and legacy import

Owner decision (2026-09-29): FreeCAD Plus will use **`.cadprt`** as its new native
file format. This is a planned reader/writer and schema change, not merely renaming
`.FCStd` files, and is not implemented yet. The migration tasks are in roadmap 7.6.

- Keep the ability to open legacy `.FCStd` documents and convert them to `.cadprt`
  as fully as reasonably possible. Preserve editable features, geometry, references
  and workbench data wherever a supported mapping exists.
- Conversion writes a new `.cadprt` file and leaves the original `.FCStd` intact.
  Opening a legacy document must not silently overwrite or convert its source.
- Report unsupported content and conversion losses. Distinguish fully editable
  conversion from partial conversion or geometry-only recovery; do not present
  recovered geometry as intact feature history.
- The owner accepts that conversion may become harder and less complete as the
  formats and application architectures diverge. Maintain best-effort legacy
  opening/conversion with tested compatibility, without freezing the new format
  to guarantee perpetual lossless `.FCStd` compatibility.
- This policy does not promise upstream FreeCAD can open `.cadprt`, or that every
  future Plus document can be exported back to an editable `.FCStd` document.

## Future architecture direction

The owner supplied an expanded planning baseline and development guidelines on
2026-09-29. Adopt their product direction for future design, subject to the
[roadmap gates](DEVELOPMENT_ROADMAP.md#planning-baseline-adoption); existing requirements
and validation records above are not declarations that these changes exist.

- Part-owned history, independent body results and reusable definitions containing
  both geometry and child occurrences; explicit work/display context and targets.
  The [part-history logical contract](architecture/PART_HISTORY_CONTRACT.md)
  defines the roles, current native mapping, dependency bindings and result lineage.
  These are design requirements; production storage and navigator remain pending.
- Shared-definition edits, occurrence placement/overrides, Make Unique and
  assembly-local operations have distinct, persisted scopes. Inspect App::Link and
  existing facilities before introducing replacements.
- Track reference identity and split/merge provenance; report ambiguous or stale
  geometry instead of silently binding to a different face or using stale CAM output.
- Keep reference sets, loading, suppression, visibility and BOM role separate.
- Implement the [planned native format and legacy import policy](#planned-native-format-and-legacy-import)
  through a versioned engineering container, recovery and a defined migration.
  The current format-retention constraint remains until that migration is implemented.
- Preserve drawing, CAM, FEM and relevant Draft consumers through ownership changes.
  Prove units, transforms, dependency invalidation, undo and persistence.

### Planned creation and interaction contracts

The [active version 2 inventory](DEVELOPMENT_ROADMAP.md#version-2-objective-coverage)
supersedes the archived baseline. These are requirements, not installed behavior.

- At creation, suggest New Body when no eligible body intersects; suggest Unite
  only for one eligible target with a valid union. Multiple eligible targets require
  deliberate selection. Invalid contact/Boolean results require corrective guidance.
  Target eligibility respects work-part ownership, occurrence/edit context, reference
  access and geometry. Intersection with another component alone never authorizes
  modifying that component. Explicit New Body, Unite, Subtract and Intersect choices
  take precedence wherever supported. Keep Tools is an explicit option.
- Distinguish inference from commitment. Update uncommitted suggestions coherently
  without oscillation near tolerance boundaries. Once chosen, preserve the user's
  mode/targets. Store accepted operation and target identities. Editing/recompute
  uses saved intent and reports invalid/missing references; it never reruns a
  heuristic to silently switch target or operation.
- Guided/direct entry and Pad/Pocket/Revolution/Groove aliases share one model,
  validation and transaction path. Pocket/Groove preset Subtract. Guidance changes
  neither geometry semantics nor saved types. Keep legacy editing adapters pending
  explicit supported conversion, and preserve the operation-first task layout.
- General/Sketcher plain picking replaces, Ctrl toggles/adds and Shift extends by
  documented context. Window picking can collect a group. An active feature input
  collector retains REQ-004's deliberate accumulation; leaving it restores ordinary
  selection. Inference suppression uses a separate nonconflicting shortcut.
- One Sketcher eligibility service distinguishes structural applicability from
  solver proof and Valid/Already Applied/Redundant/Conflicting/Unsupported/Unverified.
  No guessed conflicts, duplicate constraints, silent constraint deletion or live
  mutation by trials; stale results are discarded and commit revalidates.
- The desktop core remains free of charge for the foreseeable future, without
  subscription, activation or paid feature gates. Optional hosted services are not
  prerequisites for local modeling. A distinct public name remains an evaluation,
  not an approved rename; stable format identity stays independent of branding.
- `.cadprt` is an engineering container for supported CAD, assemblies, drawings,
  CAM, FEM and other workbench data, not one solid per file. Required capabilities,
  identity, units, transforms and external dependencies must survive round trips;
  unknown required content must be preserved safely or refused, never dropped.

## Current command-search pilot (F033)

Tools > Command search / Ctrl+K searches loaded native commands plus a bounded
alias catalog and current shortcuts. Familiar modeling names invoke the existing
Pad/Pocket/Revolution/Groove/Pattern commands; Pocket retains its subtractive
Extrude preset. Workbench switching is explicit, availability is checked before
execution, and native commands retain selection, transactions and document types.
Missing workbenches and active tasks receive recovery guidance. The pilot is ready
for owner workflow testing under roadmap 8.4.2a/b; favorites, broader context
explanations and physical/high-DPI acceptance remain pending. See
[UI-008](UI_UX_SPEC.md#ui-008-command-search-f033-roadmap-842-104) and the
[owner procedure](../tests/CommandSearch.md).

## Current temporary-display pilot (F040)

View > Visibility provides temporary isolate/hide and previous/original display
restore. Session-local, per-document snapshots change native visibility only;
Body Tips, modeling inputs, placements and link targets remain unchanged. Whole
Body results and whole linked occurrences define this pilot's target scope.
New objects retain current visibility on restore, deleted objects are ignored,
and native object IDs prevent reusing a deleted object's snapshot for a replacement.
Model Undo/Redo remains separate. Restore before saving: the transient stack is
not serialized and save during isolation stores current visibility. The bounded
workflow is ready for owner testing under roadmap 10.5a/b; linked-member overrides,
broader save-time policy and physical/high-DPI acceptance remain pending. See
[the owner procedure](../tests/TemporaryDisplay.md) and UI-009.

## Current manufacturing-export pilot (F127)

Part > Manufacturing export provides a bounded STL handoff for explicit whole
solids/Body results and whole solid occurrences. Existing shape services supply
world placement; the mesh service uses visible absolute linear and angular quality.
Output coordinates are millimeters; STL lacks units metadata, parametric history,
colors and assembly identity. Current-geometry, solid-only and closed-mesh checks
precede output replacement. Inputs remain bound to the selected native identities,
with explicit replacement and existing-file confirmation. Per-user presets store
quality only. No geometry feature or history conversion is created.

The pilot is ready for owner workflow testing under roadmap 15.7a/b. Other formats,
configuration/orientation/unit controls, mesh inputs, deep linked-member paths,
collision/printability checks and physical/high-DPI acceptance remain pending.
[Owner procedure](../tests/ManufacturingExport.md); UI-010 describes the dialog.

## Open questions

- Linear/Circular Pattern is the next family selected by the user; see roadmap
  milestone 3.7. Converting a saved legacy Linear/Polar object to the new Pattern
  type is not implemented; existing objects retain their full legacy parameter editor.
- Is multi-object profile aggregation desired later? It requires a separate
  model/compatibility decision; it is not implied by curve selection within one source.
