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

## Current sketch-support pilot (F124)

Sketcher > Sketch > Inspect and change sketch support promotes the proven direct
planar attachment core into the installed application. An explicit sketch and
replacement face in the same native container use preserve-local or preserve-world
policy. Numeric preview uses a disposable document; source attachment and geometry
stay unchanged until Apply. Apply requires current preview inputs and owns one native
undoable transaction. Preserve-local can repair a missing face; preserve-world needs
a valid old placement and refuses expression-driven offsets. The dialog explains
that numeric preview does not simulate constraints or downstream solids.

This bounded workflow is ready for owner testing under 11.7y/z. The experimental
cross-part adapter remains test-only. Graphical ghosts, broader datum/occurrence and
external-projection behavior and physical/high-DPI acceptance remain pending.
[Owner procedure](../tests/SketchSupport.md); UI-011 describes the editor.

## Current dependency-inspection pilot (F015)

Tools > Inspect dependencies provides a bounded view of actual native property
edges for an explicit object. Inputs/upstream and consumers/downstream distinguish
direct and transitive relationships, show linking properties and native error state,
and identify loaded external documents. Expressions and container links remain
visible without inventing geometric roles. Explicit row navigation and model
selection preserve geometry, ownership and visibility. Model changes invalidate the
snapshot; Refresh reads current state without recompute. Cycles and traversal limits
are reported. Unresolved references use native status, not inferred null-link errors.

The bounded pilot implements roadmap 7.5.5a / 10.6a. Broader deletion/repair controls,
unloaded-reference diagnoses, target-role classification, integrated navigator
tabs/highlights and physical/high-DPI acceptance remain open.
[Owner procedure](../tests/DependencyInspector.md); UI-012 defines interaction.

## Current measurement-context batch (F098/F099)

The existing Measure task exposes native operand identities and the meaning of
each result. Distance can report circle/arc centres or infinite datum separation;
Distance Free uses picked world points and is explicitly a fixed snapshot. World
frame and unsigned deltas, geometric-centre density exclusion and radius-versus-
thickness distinctions are visible alongside existing units and Save controls.

Native Measure::MeasureDistanceDetached adds read-only UpdatePolicy, CaptureTime
and CaptureSources properties. Capture time is UTC and selection paths are metadata,
not live links. Direct coordinate edits clear provenance, while restore and Undo/
Redo preserve recorded state. Old files default to unknown capture information.
Native types, geometric algorithms and existing associative references are retained.

Roadmap 15.1a/b covers this bounded improvement. Broader material/mass, thickness,
mesh accuracy, stale/invalid associative measurement repair and physical/high-DPI
acceptance remain open. [Owner procedure](../tests/MeasurementContext.md); UI-013.

## Current occurrence-appearance pilot (F018)

View > Occurrence appearance exposes visibility and uniform colour/transparency
overrides for one direct same-document link to a Part shape or Body. Explicit
occurrence/source identities and staged controls precede a single native transaction.
Use source appearance restores native inheritance without changing visibility.
Placement, shared geometry, other links and engineering material remain separate.
No new object schema or copy semantics are introduced.

Roadmap 12.2b/c covers this bounded workflow. Arrays, per-element overrides, nested
occurrence paths, external documents, mixed Part definitions and broader representation/
physical acceptance remain open. [Owner procedure](../tests/OccurrenceAppearance.md);
UI-014 defines the interaction. The Make Unique prototype remains test-only.

## Current interference/clearance pilot (F101)

Part > Interference and clearance checks an explicit set of 2-12 whole native solids
or direct same-document shape/Body occurrences. Common solid volume identifies overlap;
minimum distance classifies contact within the stated tolerance, below-clearance or
clear pairs. Unsupported/unavailable inputs produce unresolved pairs and an incomplete
summary, never implicit omission. Distances/volume use world mm/mm³. Deliberate input
exclusions are counted; this is not automatic whole-assembly acceptance.

The read-only dialog selects result pairs without visibility changes. Geometry edits
invalidate results; recheck requires current geometry and never recomputes the model.
No persistent inspection objects or model properties are introduced. Broader nested/
external assemblies, pair-specific exclusions, acceleration and physical acceptance
remain open. [Owner procedure](../tests/InterferenceCheck.md); roadmap 15.1c/d, UI-015.

## Current sketch-repair review pilot (F049)

The existing Validate Sketch task lists native missing-coincidence candidates with
endpoint identities and measured mm gaps. Row selection highlights endpoints; checkboxes
select repairs explicitly. Search/review do not mutate the document. Add Checked
Coincidences owns one Undo transaction, preserves existing constraints and restores the
original sketch if the solver cannot accept the repair. Sketch edits, tolerance and
construction-policy changes require a fresh search. Invalid tolerance cannot silently
fall back to another value. No candidates is not a valid-profile certification.

Roadmap 11.6a/b covers this bounded improvement. Duplicate/self-intersection diagnosis,
geometric change preview and broader repair/physical acceptance remain open.
[Owner procedure](../tests/SketchRepairReview.md); UI-016.

## Current mirror result-mode pilot (F057)

Existing Part Mirror explicitly offers associative mirroring or independent reflected
shape snapshots. Associative results remain native Part::Mirroring with source/plane
dependencies; snapshots are native Part::Feature shapes without those links or copied
feature history. Snapshot scope is document-root shapes and whole Bodies. Both modes
create separate geometry and preserve source geometry/Body Tips and visibility.

Creation owns one transaction, rejects stale/replaced sources and pending edits,
and aborts invalid results with recoverable inline feedback. No new schema is added.
Roadmap 13.5a/b covers the bounded workflow. Feature reevaluation, nested snapshots,
graphical target/handedness preview and physical acceptance remain open.
[Owner procedure](../tests/MirrorResultMode.md); UI-017.

## Current section-plane pilot (F100)

Existing Clipping View uses explicit world-coordinate millimetre offsets and
camera-derived/custom direction fields that describe the displayed plane. Zero
direction pauses custom clipping until corrected. Portable `.fcsection` presets
capture the four native planes, enabled states and retained sides; camera-following
orientation is saved as a fixed plane. Loading validates all data before changing
this view, preserving camera, geometry, document transactions and model exports.

Presets are separate versioned files, not embedded document views or geometry.
No caps or section-specific measurements are claimed. Roadmap 15.1e/f covers this
bounded pilot; broader F100 remains open. [Owner procedure and preset contract](../tests/SectionPlanes.md);
UI-018.

## Current feature organization pilot (F014)

A document-scoped metadata list searches native labels, internal names, types and
Label2 descriptions. Type filtering and sorting affect presentation only; deliberate
model selection preserves visibility. A partial-search notice identifies the bounded
2000-object scope. Closed/unloaded external definitions are not opened implicitly.

One-object label/description edits are staged until Apply, stored in one native Undo
transaction, and guarded against stale identity/metadata, pending edits and read-only
properties. Link metadata stays local to that object. No new persistent schema,
ownership changes or history reordering. Roadmap 10.6b/c covers this bounded pilot;
folders, bulk organization and integrated navigators remain open.
[Owner procedure](../tests/FeatureOrganizer.md); UI-019.

## Current Make Unique pilot (F019)

One direct unscaled occurrence of a same-document Part containing an independent
sketch and its native extrusion can receive a private native copy. The review shows
source, destination, copied inputs and new label. Native recursive copy assigns new
object identities and remaps internal inputs; only the chosen occurrence is relinked.
Its placement/visibility and other instances remain unchanged. Confirmation owns one
Undo transaction; Cancel and failed copying retain the original model.

External/attached inputs, expressions, arrays, prototype identity fields and occurrence
consumers requiring relationship remapping are explicitly unsupported. No new schema
or experimental semantic IDs are introduced. Roadmap 12.2d/e covers this bounded
pilot; arbitrary Body histories/subassemblies and broader provenance/remapping remain
open. [Owner procedure](../tests/UniqueOccurrence.md); UI-020.

## Current drawing setup pilot (F102)

TechDraw > Page > Create drawing sheet guides one document-root solid/Body into a
native same-document drawing. Built-in A4/A3 ISO landscape border-only templates, explicit
drawing/model scale, base orientation and first/third-angle convention create a base
view and optional top/right projections using the existing projection group. Native
source links, persistence and update preferences remain authoritative.

Creation is one transaction; Cancel creates nothing. Unsupported/stale sources,
pending edits, missing templates and oversized view envelopes receive explicit
feedback. No new proxy/schema is introduced. Roadmap 15.3a/b covers this bounded
pilot; occurrence/external sources, custom templates, graphical preview, section/detail
setup and reference repair remain open. [Owner procedure](../tests/DrawingSetup.md); UI-021.

## Current document update pilot (F087/F088)

Tools > Document updates exposes native failed/pending objects and affected loaded
inputs, with deliberate navigation and native error text. Native Skip Recomputes
controls deferral; explicit Recompute now updates the document once with cycle checking
and leaves its session mode unchanged. No error flags are cleared and no update engine
or persisted schema is introduced. Existing model edits retain their Undo/Redo history.

Inspection is bounded to 2000 objects including loaded inputs. A reachable affected
input is evidence, not unique-cause classification. Native edit previews can still
update individual objects; unloaded references and asynchronous background completion
are not certified. Roadmap 7.5.7a/b; [owner procedure](../tests/DocumentUpdates.md), UI-022.

## Current precise occurrence movement pilot (F074)

Tools > Move occurrence once provides incremental translation and arbitrary-axis
rotation about a typed pivot in world or current occurrence axes. The world result
is converted back through enclosing native Part transforms; only the selected
LinkPlacement changes. Source identity/geometry, other occurrences and native
LinkTransform semantics remain intact. A non-pickable view-only wireframe previews
the result, with no document objects or preview transactions.

Confirmation is one Undo transaction; Cancel removes the preview. Stale frames,
unsupported/driven/consumed links and pending edits receive explicit feedback.
This advances the one-time positioning boundary of F072/F075 without creating mates
or copies. Roadmap 10.7a/b; [owner procedure](../tests/OccurrenceMove.md), UI-023.

## Open questions

- Linear/Circular Pattern is the next family selected by the user; see roadmap
  milestone 3.7. Converting a saved legacy Linear/Polar object to the new Pattern
  type is not implemented; existing objects retain their full legacy parameter editor.
- Is multi-object profile aggregation desired later? It requires a separate
  model/compatibility decision; it is not implied by curve selection within one source.
