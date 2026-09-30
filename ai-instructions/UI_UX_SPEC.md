# FreeCAD Plus: UI and UX Specification

## Interface scope

This document specifies the fork's unified Extrude and Pattern task panes,
angular offset controls for Revolution/Groove, the Trim Body and Isocline Curve panes, and planned shared Add/Subtract
interaction for other feature families. The inherited desktop
shell and unmodified workbenches retain upstream behavior; consult their source
and the documentation linked in [the upstream overview](../README.md). This is
not a claim that every inherited screen has been inventoried or revalidated.

## Navigation and shared patterns

The model tree and 3D viewport supply geometry selections. Part Design commands
and existing-feature editing open the task pane. Standard OK/Cancel and preview
controls use the existing task-dialog and document transaction framework.
Only one reference-selection mode is active at a time. User-facing text remains
translatable; quantity fields retain FreeCAD's unit and expression behavior.

### Planned unified feature interaction

For the [candidate families](DEVELOPMENT_ROADMAP.md#unified-feature-workflows), use
one geometry command and one create/edit task. The first field is an Operation
dropdown with **Add** and **Subtract**, followed by geometry selections, then shared
dimensions and mode-specific options. Reopening an existing feature loads its current
operation and complete definition. Users can change operation without leaving the task.

Retain compatible inputs, dimensions, and expressions across operation changes.
If a mode has no equivalent, explain the conflict and require a valid choice instead
of silently resetting it. Subtract requires a suitable base solid; keep the task usable
and explain an unavailable operation. Preview and validation must reflect the selected
operation, and Cancel restores the original feature definition. Existing supported
intersection behavior must remain accessible where applicable; adding New Body or
other operation modes belongs to the planned part-level workflow below. These planned interactions satisfy
REQ-008/009; implementation and acceptance are tracked in roadmap milestone 3.6.

### Planned guided part-level workflow (not installed)

Operation remains the first field. Guidance advances through unresolved profile/
region, magnitude/direction, operation/target review and confirmation without moving
that field. Expert preselection and direct numeric entry skip satisfied steps.
Changing an earlier input keeps unrelated valid values; advanced controls collapse
without hiding operation, targets, extent, units or consequential warnings.

Display an inferred suggestion with its reason and highlighted target(s), distinct
from explicit user choice. No eligible intersection suggests New Body; one valid
eligible union suggests Unite; several candidates require deliberate selection.
Invalid contact/union, inaccessible references and missing subtraction targets show
corrective feedback and cannot silently commit. New Body remains selectable even
with overlap. Keep Tools is explicit where supported. Suggestions can refresh only
until explicit choice; near-contact behavior must avoid mode oscillation. Editing
loads saved mode/targets and never silently changes them after an extent edit.

Pad and additive Revolution route into shared Extrude/Revolve additive entry;
Pocket/Groove route into Subtract. Guided/direct paths share preview, validation,
Apply/OK/Cancel, handles and transactions. Guidance preferences are separate from
model properties; existing create/edit compatibility remains until migration passes.

Ordinary/Sketcher selection uses plain replace, Ctrl toggle/add and documented Shift
extension, plus window selection. Active feature collectors explicitly show their
accumulation mode; their existing multi-pick behavior remains. Auto-inference
suppression has a nonconflicting shortcut. Shared eligibility controls hide
structurally inapplicable constraints, disable proven conflicts with reasons and
highlighted causes, and distinguish existing, redundant, unsupported and unverified
states. The near-cursor palette uses the same service as menus/toolbars/shortcuts,
with stable ordering, keyboard access, an off preference and a reachable pointer
corridor/dismissal delay. Trials cannot remove constraints; commit revalidates.

## Screen index

| ID | Name | Purpose | Entry point | Specification |
| --- | --- | --- | --- | --- |
| UI-001 | Extrude task pane | Choose Add/Subtract and configure a new or existing extrusion | `PartDesign_Extrude`; legacy Pad/Pocket commands; Edit Extrude | [UI-001](#ui-001-pad-task-pane) |
| UI-002 | Pattern task pane | Choose Linear/Circular, features, and repetition parameters | `PartDesign_Pattern`; Edit Pattern | [UI-002](#ui-002-pattern-task-pane) |
| UI-003 | Revolve/Groove angular controls | Offset the angular start and reverse direction within the existing create/edit pane | Revolution or Groove; edit existing feature | [UI-003](#ui-003-revolve-and-groove-angular-controls) |
| UI-004 | Trim Body task pane | Select a target, cutting tool, and side to keep | Part or Part Design: Trim Body; double-click existing result | [UI-004](#ui-004-trim-body-task-pane) |
| UI-005 | Isocline Curve task pane | Trace draft-angle curves on selected faces | Part or Part Design: Isocline Curve; edit existing result | [UI-005](#ui-005-isocline-curve-task-pane) |

## Screen specifications

<a id="ui-001-pad-task-pane"></a>

### UI-001: Extrude task pane

- Purpose: satisfy REQ-001 through REQ-009 and REQ-013 in [the product specification](PRODUCT_SPEC.md#capabilities-and-requirements).
- Entry: invoke Extrude with an active body, with or without preselection; or edit an
  existing Pad/Pocket. Legacy commands remain callable. The normal body prerequisite remains in force.
- Exit: OK accepts a valid result; Cancel abandons the transaction. Empty and
  invalid profiles retain the dialog so the user can correct them.
- Layout: Operation is the first field inside Extrude Parameters, then Profile,
  shared extrusion parameters, and preview controls in the task pane.
- Data: show the source label and selected edge/face names, or a whole-profile
  entry. Refresh from `Profile`; geometry and feature status drive preview/errors.

| Control | Placement | Action | Availability and validation | Result/feedback |
| --- | --- | --- | --- | --- |
| Start offset | Above direction/extent controls, always visible | Enter a signed distance or click the adjacent flip button | Defaults to zero for a new feature in every direction mode; entering a nonzero distance selects Offset automatically. A selected start reference remains supported. | Uses the existing start offset along the selected extrusion direction; flipping negates the value or expression. At zero the start remains on the plane. Selecting Profile plane resets the offset and its expression. |
| Length direction buttons | Beside side 1 and side 2 Length | Flip the existing extrusion axis | The two buttons stay synchronized; symmetric Dimension disables length reversal. For non-dimensional extents the button sits beside Type. | Preserves lengths, expressions, and the existing opposite-side geometry; no separate Reversed checkbox. |
| Operation dropdown | First field | Choose Add or Subtract without leaving the task | Add is the new Extrude default; reopening loads the saved operation. Existing Common features also expose Intersect to retain that operation. | Retains profile, dimensions, direction, expressions, and extent meanings. Subtract without a base solid stays editable but cannot be accepted. |
| Profile list | Immediately after Operation | Select one or more rows for removal | Populated from one source object and optional subelements | Shows accumulated geometry; ordinary viewport clicks do not discard previous rows. |
| Select / Done | Below profile list | Enter/exit geometry selection | A new empty Pad enters selection automatically | Model/tree selections update the profile; other selectors are deselected. |
| Remove | Below profile list | Remove highlighted entries | Enabled only when list entries are selected | Remaining entries are retained; removing the last leaves an empty profile. |
| Clear | Below profile list | Remove the source and all entries; begin selection | Enabled when a source is assigned | A different source can now be selected. |
| Profile hint | Above list | Explain empty, invalid, or incompatible selection | Always visible | Empty-state instructions; geometry errors; explanation when another source is picked without clearing. |
| Start / Offset / Pick Reference | Existing parameter area | Choose profile plane, offset, or referenced start | Offset/reference fields follow the selected start mode | Retain inherited start and reference-picking behavior. |
| Direction, Reversed, custom X/Y/Z, Length along sketch normal | Existing direction controls | Set extrusion direction and length interpretation | Normal/reference/custom mode governs available fields | Changing the profile refreshes direction choices; explicit custom choices remain model-owned. |
| One sided / Two sided / Symmetric | Existing side mode | Choose extent arrangement | Side 2 controls appear when applicable | Retain inherited one/two/symmetric behavior. |
| Type, Length, end reference, Offset, Taper angle | Per-side parameter controls | Set dimension or limiting geometry and taper | Dimension, To last, To first, Up to face, Up to shape, Through all expose their applicable inputs | To last and Through all remain distinct when switching operation. Through all requires a base shape. |
| End-shape face list / Remove / all-faces control | Existing up-to-shape controls | Choose and refine limiting faces | Available in the applicable end mode | This list remains separate from Profile. |
| Update view and preview controls | Existing task/preview sections | Control recomputation and preview presentation | Inherited task framework behavior | Preview is feedback, not a saved feature until acceptance. |
| OK | Standard task controls | Validate and commit | Requires a profile and valid feature geometry | Hide accepted profile/base as appropriate; finish editing. |
| Cancel | Standard task controls | Abort editing | Available for new and existing Pad | Remove pending new feature or restore existing feature and temporary visibility. |

- States: no selection, preselected/previously saved profile, incomplete curve
  collection, valid preview, invalid geometry, and active reference selection.
  Network/offline state is not relevant to this local feature operation.
- Persistence: the profile and parameters use existing document properties and
  transaction history; no new persisted schema is introduced.
- Accessibility and input: keep standard keyboard focus, translated control
  names, and multi-row list selection. Keyboard and assistive-technology behavior
  must be checked in the built GUI; it has not yet been verified for this change.
- Acceptance examples: click Pad before choosing curves; retain four clicked
  rectangle edges across normal selection clears; remove/re-add an edge; edit
  and replace the profile after Clear; reject empty/incomplete profiles; cancel
  without losing the original feature; verify Undo/Redo and reference-mode switching.
- Implementation: [`TaskPadParameters.cpp`](../src/Mod/PartDesign/Gui/TaskPadParameters.cpp),
  [`TaskExtrudeParameters.cpp`](../src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp),
  [`TaskPadPocketParameters.ui`](../src/Mod/PartDesign/Gui/TaskPadPocketParameters.ui).
  Test procedure: [Pad regressions](../tests/PadTaskPanel.md).

### UI-002: Pattern task pane

Satisfies REQ-010 through REQ-012. Invoke **Pattern** in Part Design with an active
Body, with or without preselection, or double-click an existing combined Pattern.
Both entry paths use the same task. Legacy Linear/Polar commands remain callable
and edit their original types; they are not silently converted.

| Control | Order and behavior |
| --- | --- |
| Pattern type | First field: Linear or Circular. Switching replaces only the displayed parameter controls and active transformation; the result object and both sets of saved settings remain. |
| Features | Immediately follows the type selector. Add/Remove Feature and the list use model/tree selection. An empty new pattern enters Add Feature mode. Transform body remains an explicit alternative. Reject other-body and dependent-feature picks. |
| Direction / Axis | Follows the feature list. Linear exposes direction; Circular exposes rotation axis. Choose a Body/sketch axis or pick a reference in the model. Reference picking and feature picking are mutually exclusive. |
| Dimensions and occurrences | Linear: total length or spacing and count, with optional second direction. Circular: total angle or angular spacing and count. Retain reverse, expressions, custom spacing, and instance suppression. |
| Preview | Existing recompute and preview controls. Empty/invalid inputs stay editable; no stale valid result may be accepted after removing all features. |
| OK / Cancel | Standard task buttons commit a valid result or restore the pre-edit document. No nested OK is needed to finish defining the pattern. |

Persistence uses a new `PartDesign::Pattern` result with owned Linear/Polar settings,
reusing MultiTransform's geometry engine. Existing stored types and property units
are unchanged. Old upstream versions do not know the new result type; cross-version
recomputation is not established. Keyboard/viewport acceptance remains a separate
manual gate; see [the test procedure](../tests/PatternTaskPanel.md).

### UI-003: Revolve and Groove angular controls

Satisfies REQ-014. The existing **Revolution** command adds material; **Groove**
subtracts it. Both use the shared Revolution parameters controller for creation
and editing. This change covers angular controls, without consolidating the two
commands or changing their profile-selection workflow.

| Control | Behavior |
| --- | --- |
| Start offset | Always visible, in degrees, default 0. Accept -360 through +360 inclusive without wrapping those endpoints to 0. A nonzero value automatically selects Offset. One-sided and two-sided limits start at the rotated profile; Symmetric is centered on it. |
| Offset reverse | Button beside Offset negates its signed value or expression. At zero it leaves the start unchanged. The offset is measured about the selected axis in the existing revolution direction. |
| Angle reverse | Buttons beside Angle and second-side Angle replace the Reversed checkbox and stay synchronized with the existing shared direction. Symmetric angular sweeps disable them; reference extents retain the control beside Type when Angle is hidden. |
| Start reference | Existing reference picking remains available. Its offset uses the same signed field. Choosing Profile plane resets the offset and its expression to zero. |
| OK / Cancel | Accept valid geometry or restore the previous definition. Reopening loads the saved offset, signs, sides, angles, axis, and expressions. |

Uses existing `StartType`, `StartOffset`, `Reversed`, `Angle`, and `Angle2` properties;
no document schema change. The start-angle viewport gizmo is available at zero.
Keyboard/high-DPI/manual viewport acceptance is tracked separately in milestone 3.9.
Source: [`TaskRevolutionParameters.cpp`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.cpp),
[`TaskRevolutionParameters.ui`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.ui).
Validation: [Revolve task procedure](../tests/RevolveTaskPanel.md).

### UI-004: Trim Body task pane

Satisfies REQ-015 through REQ-017. Invoke **Trim Body** from Part's Boolean menu or
Boolean Tools toolbar, or Part Design's menu or Modeling Features toolbar. An open
document is required; an active Body and preselection are optional. Double-clicking
the result or choosing **Edit Trim Body** opens the same pane.

| Control | Order and behavior |
| --- | --- |
| Target body | First section. Select/Clear one solid or sheet object in the current document. A viewport face pick selects its owning target object. |
| Cutting tool | Second section. Select/Clear a datum plane, one face of another object, or a sheet. Selecting a whole solid as the tool is rejected; pick its face instead. After choosing a target, an empty tool field enters selection mode. |
| Keep side | Text and adjacent reverse button flip the side to keep. The green viewport arrow points toward the kept side along the local tool normal. |
| Extend planar tool | Enabled by default; extends a planar boundary across the target. Curved surfaces are not extended automatically and must span every region being trimmed. |
| Refine result | Enabled by default; removes redundant result edges. |
| Live preview and status | Preview hides the target and displays the kept result. Pausing preview defers computation until OK. Missing, self/dependent, wrong-document, or invalid cutting inputs stay editable with an explanation. Invalid or unrecomputed dependencies after recompute hide the result and block OK until repaired. |
| OK / Cancel | OK recomputes and accepts only valid geometry, hides the source inputs, and shows the separate result. Cancel removes a pending new feature or restores an existing feature and input visibility. Both remove temporary selection observation and the arrow. |

Invalid or unrecomputed target/tool picks leave the existing inputs and active
selection mode unchanged, with a repair/recompute message. Retry after repair.
Optional preselection skips stale targets/tools while retaining valid inputs;
the task remains available to select replacements.
If feature creation or editor startup fails, creation is rolled back so the command
can be retried. A pre-existing transaction must finish before starting this command
or reopening an existing feature; rejection preserves the caller's pending edits.

The source solid/sheet remains associative input. A Part Design Body keeps its Tip;
the new result appears separately in the document tree. Reopen the result to change
its target, cutter, or side. Original input visibility is restored while selecting.
Solid cuts close newly exposed faces. This first implementation uses one cutter,
not multiple cutting tools or an automatic curved-sheet Trim and Extend operation.
The saved feature requires the new BOPTools Python modules to recompute.
Source: [`TrimGui.py`](../src/Mod/Part/BOPTools/TrimGui.py).
Validation: [Trim Body procedure](../tests/TrimBody.md).

### UI-005: Isocline Curve task pane

Satisfies REQ-018 through REQ-020. Invoke **Isocline Curve** from the Part menu/Part
Tools toolbar or Part Design menu/Modeling Features toolbar. An open document is
required; an active Body is optional. Double-click a saved result or use **Edit
Isocline Curve** to reopen the same complete definition.

| Control | Order and behavior |
| --- | --- |
| Target faces | First section: accumulated face list with Add faces, Remove and Clear. Pick individual viewport faces or a whole source in the tree to include all its faces. Duplicate picks do not duplicate curves. Ordinary selection clearing retains collected references. |
| Pull direction | X, Y or Z world axis (default Z), Reference, or Custom vector. Adjacent reverse button flips the pull direction; the green viewport arrow follows it. |
| Direction reference | Visible in Reference mode. Pick a datum plane, a planar face, a straight edge or datum axis; planes supply their normal. Curved faces/edges, self/dependent objects, and other-document picks are rejected. |
| Custom vector | X/Y/Z components, visible in Custom vector mode. Normalize internally; a zero or nonfinite vector is invalid. |
| Draft angle | Degrees, default 0, range 0 through 90. Zero gives normals perpendicular to pull; positive values select normals increasingly facing pull. Reversing pull selects the opposite draft side. |
| Preview and status | Red curves are highlighted through source faces while editing, including hidden portions; the accepted feature uses normal depth rendering. The green arrow indicates pull. Live preview can be paused. Missing input, no curve, whole-face coincidence, or solver errors stay editable and clear stale output. Invalid or unrecomputed dependencies after recompute hide the result and block OK until repaired. |
| OK / Cancel | OK forces recompute and accepts valid wires; Cancel removes a pending feature or restores its previous definition and temporary visibility. Both remove selection observation and direction annotation. |

Invalid or unrecomputed face/direction-reference picks leave the existing inputs
and selection mode unchanged, with a repair/recompute message. Retry after repair.
Optional preselection skips stale face objects and retains valid faces from the
same selection. Repaired faces can be added in the task.
If feature creation or editor startup fails, creation is rolled back so the command
can be retried. A pre-existing transaction must finish before starting this command
or reopening an existing feature; rejection preserves the caller's pending edits.

Source objects remain unchanged and keep their Part Design Body Tip. Face boundary
holes split a contour into separate segments; each connected set becomes a wire.
At 90 degrees a sphere has only an isolated point and cannot produce a curve; a
cylinder can retain a valid line. A whole face at the requested inclination has
no unique isocline and is reported as such. This task does not split faces/bodies
or create a stepped series of angles. Source: [`IsoclineGui.py`](../src/Mod/Part/BasicShapes/IsoclineGui.py).
Validation: [Isocline procedure](../tests/IsoclineCurve.md).

### UI-006: CAM mesh machining and tabs

Entry: import STL, select it, create a CAM Job, set stock/tool and work origin,
then choose **Parallel / Waterline**. Use the Strategy selector for Parallel / surface
scan or Waterline; Parallel supports Line or ZigZag with the existing stepover and
angle controls. Depths, feeds, sampling and tool controls retain the inherited CAM
task pages. Selecting a CAD-only strategy for an STL reports an error.

For CAD face selections, **Avoid last N faces** is supported by Parallel machining.
Boundary-construction/subtraction failures stop generation and clear the previous
path; the operation must not continue without its selected exclusion regions.
Switching to Waterline or another strategy while this setting is nonzero reports
an error instead of silently ignoring it. Return to Parallel or clear its avoided
face selection before switching. This is separate from Holding Tabs, which remain
supported by both Parallel and Waterline.

For selected freeform CAD cutting faces, **Linear Deflection** also controls the
approximation of the projected machining boundary. Smaller values make a finer
boundary at greater computation cost. The outer cutting outline and separately
selected avoidance regions retain their existing meanings. Failed projection
stops generation; it must not silently expand to the model's bounding rectangle.

**Holding Tab** is in Project Setup and the CAM menu. Select a Job when more than
one exists. The new tab starts at the model's +X edge, near surrounding stock.
Double-click a tab to reopen the same complete editor.

| Control | Behavior |
| --- | --- |
| Center X/Y and Bottom Z | Position in the Job's machining coordinates, in mm. |
| Length / Width / Height | Positive dimensions in mm; changes preview the orange bridge. |
| Angle | Rotation about Z, -360 to +360 degrees. |
| Pick position on model | The next model pick sets center X/Y; bottom Z remains unchanged. |
| OK | Commit and recompute linked toolpaths. |
| Cancel | Abort creation or edits and restore the prior document state. |

Tabs appear under the Job and remain visible for placement against the part and
stock. They are shared by Parallel/Waterline operations. Other operations in a job
with these tabs report unsupported protection and clear their output. Clearance and
safe heights must be above every tab. Users must place bridges so they connect the
part to stock; this version does not infer strength or connectivity from an STL.
Controls support tab-key navigation, numeric keyboard editing, and translated labels.

**Indexed Setup** creates another job from the selected source job. Its shared
create/edit pane offers rotation axis X/Y/Z, an index angle (default 180 degrees),
and a work origin at stock top center, stock top corner, or a custom point in
rotated source coordinates. Edit the frame under the new Job to change these
values. Independent model moves are disabled for indexed jobs: model, stock and
tabs must stay registered. Create and post operations separately for each setup;
the command does not emit rotary-axis moves. Double-clicking a copied tab edits
its shared source in the original setup coordinates.

Source: [`HoldingTab.py`](../src/Mod/CAM/Path/Main/Gui/HoldingTab.py).
Validation: [CAM procedure](../tests/CAMMeshMachining.md).

## Open questions

Further unified families and multi-source profile behavior are [product questions](PRODUCT_SPEC.md#open-questions).
Record any visual or interaction defects found by GUI validation against UI-001
and the active roadmap milestone; do not silently change the intended workflow.


## Test-only parameter editor prototype (roadmap 10.8k/l)

`tests/prototypes/ParameterEditor.py` is an uninstalled dialog for one existing
parameter object, supplied by the test caller. It is not a production command or
replacement for the planned part-level parameter editor. Fields appear in order:
Parameter (existing length/angle property dropdown), Name, read-only Current value,
Expression, error message, Apply expression/Rename buttons, then Close.

Typing leaves the document unchanged. Apply evaluates units and affected recompute
state in an owned transaction; a failed edit rolls back, keeps the attempted text
and displays the error for correction. Success refreshes the value/expression.
Rename uses native rename through the atomic wrapper; a collision stays editable,
and success refreshes the dropdown to the new name. Selecting another parameter
reloads its data and discards unapplied text. Close discards unapplied text; it does
not undo earlier successful Apply/Rename transactions. Native Undo remains available.

Three native Qt tests exercise these interactions programmatically. Physical
keyboard/accessibility, high-DPI layout, external edits/document closure and the
full production creation/deletion/where-used/publication workflow remain pending.
