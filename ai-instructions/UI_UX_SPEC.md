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
| UI-007 | Named parameters | Create/edit Part-owned lengths and angles; copy reusable expressions | Part > Named parameters... | [UI-007](#ui-007-named-parameters-roadmap-108) |

## Screen specifications

<a id="ui-001-pad-task-pane"></a>

### UI-001: Extrude task pane

- Purpose: satisfy REQ-001 through REQ-009 and REQ-013 in [the product specification](PRODUCT_SPEC.md#capabilities-and-requirements).
- Entry: invoke Extrude with an active body, with or without preselection; or edit an
  existing Pad/Pocket. Legacy commands remain callable. The normal body prerequisite remains in force.
- Exit: OK accepts a valid result; Cancel abandons the transaction. Empty and
  invalid profiles retain the dialog so the user can correct them.
- Preselection: Extrude and legacy Pad/Pocket use the editor's profile gate.
  One valid profile source is assigned regardless of its order among whole solid
  or Body picks. Those picks are not treated as explicit Boolean targets: the
  active Body remains the scope. Invalid/out-of-body picks are explained inside
  the Profile group; multiple valid profile objects leave the collector empty
  for explicit choice. No blocking selection-error dialog replaces the editor.
- Cancel restores the original object/subelement selection captured before
  creation or reopening, alongside the previous profile, visibility and Body Tip.
- Profile feedback shows the collected entry count, accepted types and whether
  Profile picking is active. A whole profile counts as one entry, not its edges.
  Selecting rows highlights their geometry; Highlight inspects selected rows or
  all entries when none are selected. Inspection explicitly activates Profile,
  leaves model references unchanged and restores temporary visibility on exit.
  Empty collectors disable Highlight. The Highlight button has its own row.
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
| One sided / Two sided / Symmetric | Existing side mode | Choose extent arrangement | Side 2 controls appear when applicable | One sided uses Length; Symmetric uses Total length, split equally about the start plane; Two sided uses independent Side 1 length and Side 2 length. Start offset moves the start plane without changing those lengths. |
| Type, Length, end reference, Offset, Taper angle | Per-side parameter controls | Set dimension or limiting geometry and taper | Dimension, To last, To first, Up to face, Up to shape, Through all expose their applicable inputs | To last and Through all remain distinct when switching operation. Through all requires a base shape. Face limits remain associative; a positive end offset moves the limiting face farther along that side's extrusion direction. Typing a side 2 face changes only its own reference. Removed limiting faces remain errors in Up to face mode until repaired. |
| Face-limit text | Per-side end reference | Enter an object label with FaceN, or a datum/origin plane label | Empty/malformed input clears only that side's saved limit and produces a repairable preview error. A missing numeric face remains an invalid reference. | Typed planes update the preview immediately. Invalid OK keeps the editor open, including when Recompute on change is off; correction or Cancel restores a valid state. |
| End-limit reference restrictions | Typed or picked end face/plane | Use an independent reference | Self and downstream references are rejected before linking. Datum/origin planes follow the existing Body/type selection rules. | Typed rejection invalidates only that side for correction; picked rejection preserves the saved reference and displayed name while keeping the picker active. Valid correction and Cancel retain their existing behavior. |
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
| Features | Immediately follows the type selector. Originals feedback shows entry count, accepted additive/subtractive feature types and add/remove/inactive picking state. Add/Remove Feature and the list use model/tree selection. Clear empties the list and activates replacement picking while retaining both pattern settings. Empty inputs cannot be accepted. Whole body disables Clear and reports the retained selected-feature count. Reject other-body and dependent-feature picks. |
| Direction / Axis | Follows the feature list. Linear exposes direction; Circular exposes rotation axis. Choose a Body/sketch axis or pick a reference in the model. Reference picking and feature picking are mutually exclusive. |
| Originals inspection | Selecting a row highlights that original by stored object identity. Highlight inspects the selected row, or all originals if none is selected. Inspection ends feature/reference picking without changing links. It temporarily reveals originals and hides the result; later picking and type/scope changes restore inspection visibility, while OK/Cancel restore source/result visibility through the normal editor lifecycle. Empty/Whole body collectors disable Highlight. |
| Initial and later picks | Both use the same Originals document, Body, additive/subtractive type and dependency checks. Multiple subelements of one feature count once. Valid mixed preselection is retained; rejected inputs receive inline reasons. Invalid-only preselection leaves the task open for correction. Later rejected picks keep the collector active; successful correction or Clear dismisses the feedback. Whole-body selection is an explicit scope choice. |
| Reference inspection | Combined Pattern Direction, Direction 2 and Circular Axis show reference count and active picking state, with accepted-type tooltips. Highlight reference inspects the stored object/subelement without changing any collector, ending other picking roles. No assigned reference disables Highlight. Inspection visibility is restored on role/type changes and through the normal OK/Cancel lifecycle. |
| Unfinished reference picking | Entering reference picking retains the existing link until a valid replacement is chosen. Leaving through Originals controls, scope/type changes or OK ends picking and restores the saved reference in the combo. Later picks cannot silently change the abandoned role. |
| Cancel selection | Combined Pattern captures object/subelement selection before creation or edit startup and restores it after transaction rollback. Deleted originals are skipped. Legacy transform dialogs retain their existing selection behavior. |
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
| Target body | First section. Select/Clear one solid or sheet object in the current document. A viewport face pick selects its owning target object. Highlight shows the assigned object without replacing an active collector's input. |
| Cutting tool | Second section. Select/Clear a datum plane, one face of another object, or a sheet. Highlight shows the assigned object/face; it is disabled when empty. Selecting a whole solid as the tool is rejected; pick its face instead. After choosing a target, an empty tool field enters selection mode. |
| Keep side | Text and adjacent reverse button flip the side to keep. The green viewport arrow points toward the kept side along the local tool normal. |
| Extend planar tool | Enabled by default; extends a planar boundary across the target. Curved surfaces are not extended automatically and must span every region being trimmed. |
| Refine result | Enabled by default; removes redundant result edges. |
| Live preview and status | Preview hides the target and displays the kept result. Pausing preview defers computation until OK. Missing, self/dependent, wrong-document, or invalid cutting inputs stay editable with an explanation. Invalid or unrecomputed dependencies after recompute hide the result and block OK until repaired. |
| OK / Cancel | OK recomputes and accepts only valid geometry, hides the source inputs, and shows the separate result. Cancel removes a pending new feature or restores an existing feature and input visibility. Both remove temporary selection observation and the arrow. |

Target and Cutting tool show 0/1 or 1/1 collected inputs and accepted type hints.
A Picking label below these groups identifies the active role without relying on
color. Preselection follows the established first-target, second-tool order;
extra objects, rejected inputs and multiple faces for a single tool are explained
in a persistent plain-text notice. No tool face is chosen from an ambiguous set.
Valid inputs remain available for correction; the notice is not saved with the
feature and is hidden on reopen. Preselection and later picks share validation.

Invalid or unrecomputed target/tool picks leave the existing inputs and active
selection mode unchanged, with a repair/recompute message. Retry after repair.
Optional preselection skips stale targets/tools while retaining valid inputs;
the task remains available to select replacements.
Cancel restores the selection captured before creation or editing, including
subelement and occurrence paths. Highlight temporarily shows hidden inputs;
normal acceptance/cancellation visibility rules still apply. Failed startup also
restores the original selection. If feature creation or editor startup fails,
creation is rolled back so the command can be retried.
A pre-existing transaction must finish before starting this command
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
| Target faces | First section: accumulated face list with Add faces, Remove and Clear. Selecting list rows highlights their geometry without adding/replacing collector inputs, including when picking a direction reference. Pick individual viewport faces or a whole source in the tree to include all its faces. Duplicate picks do not duplicate curves. Ordinary selection clearing retains collected references. |
| Pull direction | X, Y or Z world axis (default Z), Reference, or Custom vector. Adjacent reverse button flips the pull direction; the green viewport arrow follows it. |
| Direction reference | Visible in Reference mode. Pick a datum plane, a planar face, a straight edge or datum axis; planes supply their normal. Highlight inspects the assigned reference without adding it to Target faces. Clear removes the reference, clears the curve preview and enters reference picking while retaining Reference mode. OK stays blocked until a valid replacement or another direction mode is chosen. Highlight/Clear are disabled when empty. Curved faces/edges, self/dependent objects, and other-document picks are rejected. |
| Custom vector | X/Y/Z components, visible in Custom vector mode. Normalize internally; a zero or nonfinite vector is invalid. |
| Draft angle | Degrees, default 0, range 0 through 90. Zero gives normals perpendicular to pull; positive values select normals increasingly facing pull. Reversing pull selects the opposite draft side. |
| Curve tolerance | 3D curve distance tolerance, default 0.00001 mm; accepted range 0.0000001 through 0.01 mm. Accept length units or bare numbers in mm. Apply on leaving the field or OK; invalid drafts remain editable, hide preview and block OK, including when preview is paused. Reopen shows the saved physical value in mm. Expression-driven values are read-only, identify their expression in the tooltip, and remain controlled by it. This field does not change the angular residual criterion. |
| Preview and status | Red curves are highlighted through source faces while editing, including hidden portions; the accepted feature uses normal depth rendering. The green arrow indicates pull. Live preview can be paused. Missing input, no curve, whole-face coincidence, or solver errors stay editable and clear stale output. Invalid or unrecomputed dependencies after recompute hide the result and block OK until repaired. |
| OK / Cancel | OK forces recompute and accepts valid wires; Cancel removes a pending feature or restores its previous definition and temporary visibility. Both remove selection observation and direction annotation. |

Target faces shows a count of collected entries, with whole-object entries
explicitly labeled as all faces; the count is not the number of expanded faces.
Direction reference shows 0/1 or 1/1 and its accepted types. A Picking label below
the face group identifies the active collector, including after rejected picks.
Preselection uses the same checks as later picks: valid faces remain collected,
while rejected edges, vertices, stale or wrong-document inputs are named with
reasons in a plain-text notice. The notice remains while correcting the task and
is hidden on reopen. Whole-object picks are retained across other-row removal,
Undo/Redo and save/reopen, and continue to follow source geometry edits.

Invalid or unrecomputed face/direction-reference picks leave the existing inputs
and selection mode unchanged, with a repair/recompute message. Retry after repair.
Optional preselection skips stale face objects and retains valid faces from the
same selection. Repaired faces can be added in the task.
Cancel and failed startup restore the original object/subelement/occurrence
selection. Highlighted inputs return to their previous visibility on task exit.
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


## UI-007: Named parameters (roadmap 10.8)

Part workbench > **Part > Named parameters...** (`Part_NamedParameters`) opens
`NamedParameterGui.py` for the selected native App::Part definition or its marked
parameter set. The command is enabled for one supported selection with no pending
transaction. A Part with no set creates one in its own undoable transaction; a
Part with one set reuses it. Multiple sets require explicit set selection. Bodies,
occurrences and arbitrary FeaturePython objects are not inferred as parameter sets.
Reinvoking the command raises the existing dialog for that set.

Fields appear in order: Parameter (length/angle property dropdown), Name,
read-only Current value, Display unit, read-only Description, Expression,
read-only Reference in this document and Copy reference, error message,
Apply expression/Rename, New name/type/expression/description, Create parameter,
then Refresh/Close. Copy reference uses the container's internal object name and
parameter property name, for example `Parameters.Width`, suitable for a compatible
feature expression in the same document. Rename refreshes it; an empty or stale
selection cannot copy an outdated reference. Cross-document publication is future scope.

Typing leaves the document unchanged. Apply evaluates units and affected recompute
state in an owned transaction; a failed edit rolls back, keeps the attempted text
and displays the error for correction. Success refreshes the value/expression.
Rename uses native rename through the atomic wrapper; a collision stays editable,
and success refreshes the dropdown to the new name. Selecting another parameter
reloads its data and discards unapplied text. Close discards unapplied text; it does
not undo earlier successful Apply/Rename transactions. Native Undo remains available.

External typed-value/expression changes (including Undo) block stale Apply/Rename
with a Refresh instruction. Refresh explicitly discards draft text and reloads the
current selection. Parameter-object or document deletion closes the dialog and
removes its observer; closed dialogs ignore further edit actions. The snapshot is
object-level and does not track every external dependency revision.

When loading a selection after external parameter-list changes, editing is disabled
and a Refresh message replaces the stale value. Refresh rebuilds the list; an empty
list disables Apply/Rename, while a later added length/angle parameter can be loaded.
Two dialogs for the same object use the same conflict guard: either dialog must
Refresh after the other commits. Closing one leaves the other's observer active.

Create parameter operates on the existing parameter object. New type offers Length
and Angle; New expression requires explicit compatible units. New name uses an ASCII
identifier (letter/underscore followed by letters, digits or underscores); collisions
reject. Creation owns one transaction and rolls back on failure. Errors retain the
creation fields for correction; success selects the new property and clears New name/
expression. Existing conflict checks apply to Create as well as Apply/Rename.

New description is stored as native property documentation and shown read-only when
selected. Success clears it with the other creation text. Existing-description
editing is not implemented. Display unit offers mm/cm/m/in/ft for lengths and deg/rad
for angles; conversion changes the Current value display only. Expressions still
require explicit units. Unit choice is dialog state, not a saved preference.

Model/Qt acceptance and the example for owner testing are recorded in roadmap
10.8. Physical keyboard/accessibility, high-DPI/localized layout, general external
reference synchronization, existing-description editing, deletion/where-used and
publication remain pending.

The underlying create/edit functions accept explicit objects, independent of active
document. Close leaves the committed container intact; Undo of creation is separate.
Production command recognition requires a directly Part-owned App::FeaturePython
with integer ParameterSetVersion 1. Existing unmarked objects are not silently
adopted or migrated. The native properties and expressions require no custom
serialization proxy. This pilot does not select the future unified history model.


## UI-008: Command search and local help (F033/F123; roadmap 8.4.2, 10.4, 10.9a/b)

Tools > Command search... (`Std_CommandSearch`, default Ctrl+K) opens one reusable
modeless palette. Search matches registered names, menu labels, current shortcuts
and the bounded familiar-alias catalog. Results show command intent and shortcut;
the selected result shows guidance and current availability. Exact command names
precede incidental matches. No match disables Run and displays an empty state.

Pad/Boss-Extrude invokes PartDesign_Pad; Pocket/Cut-Extrude invokes
PartDesign_Pocket; Revolution/Revolved Boss invokes PartDesign_Revolution;
Groove/Revolved Cut invokes PartDesign_Groove. Existing feature identities and
editor presets remain authoritative. Linear/Circular Pattern, named parameters
and Insert Component have explicit catalog entries too. Other loaded commands
retain their native titles and tooltips.

Switch workbench is explicit, retains the query/result and creates no geometry.
Run rechecks command availability and releases palette focus before invoking the
existing command. Active task dialogs block launch/switch with a recovery message.
An unavailable Insert Component points to creating or activating an Assembly;
generic commands receive their existing tooltip/context guidance. Refresh reloads
commands/shortcuts and availability. Close/Escape makes no document changes.

Up/Down moves results from the query, Enter runs the selection, and Tab reaches
buttons. Reinvocation focuses/selects the query. Existing Customize > Keyboard
owns per-user shortcut editing, reset and conflict handling. Favorites, exhaustive
aliases, per-command diagnostics, navigation presets and physical/high-DPI/localized
acceptance remain pending. [Owner procedure](../tests/CommandSearch.md).

F123 extension: the same palette bundles plain-text guides for thirteen named
commands, including sketch reuse, one-time occurrence movement, document updates,
manufacturing STL export and CAM mesh preparation. Guides explain inputs, actions,
reversal/file effects and limitations. No network lookup, workbench activation or
model edit occurs when reading. Commands without a curated guide explicitly say so
and retain their native description. "Available to open" is not a geometry check;
native IsActive and each command's existing editor remain authoritative.

| Control | Action and feedback |
| --- | --- |
| Local help (F1) | Toggle extended guide for the selected row; focus the readable lower pane when opening. Works while Run is unavailable. |
| Guidance pane | Plain text, selectable and scrollable; arrows/Page Up/Down read without launching. Tab leaves the pane; Enter here does not run. |
| Ctrl+L | Focus and select the query from any palette control. These bindings are local to this window. |
| Vertical divider | Allocate space between results and guidance; neither pane can collapse completely. |
| Reset layout | Restore window size/position and divider, hide extended help and focus search; preserve query, application fonts, shortcuts and model. |
| Run/Switch/Refresh/Help/Reset/Close | Two button rows with mnemonics and explicit focus order after query/results/guidance. |

Availability and active-document text refresh every 750 ms while visible; unchanged
text preserves reading position. Refresh reloads the command/shortcut catalog.
Empty results disable Run/Switch and show the empty state. Guidance remains readable
without a document or required workbench. There is no new saved document property
or persistent help preference. Actual rendered enlarged-text layout is exercised in
automation; physical screen-reader/high-DPI and localization acceptance remain open.


## UI-009: Temporary display (F040; roadmap 10.5)

View > Visibility adds Temporarily isolate selection, Temporarily hide selection,
Restore previous display and Restore original display. The shared command search
indexes these native command registrations. No new default shortcut is assigned.
Isolate/hide snapshots the active document's current native visibility; each changed
display pushes one level. A no-op pushes nothing. The status bar confirms depth;
Restore commands remain available while the active document has saved levels.

Isolate retains selected objects and their containing Parts, hides other branches,
and preserves selected containers' internal hidden states. A Body-feature selection
addresses the whole Body result. A linked subelement addresses its whole local
occurrence, never its shared source member. Hide affects those same whole targets.
Input links, placements, ownership, suppression and Body Tips are not edited.

Restore previous pops one level; Restore original returns to the oldest snapshot
and clears the stack. Ordinary visibility changes since that snapshot are reset
too. Deleted objects are ignored; objects created after the snapshot retain their
visibility, including a replacement with a reused name and different native ID.
Document close discards its stack. Other documents retain independent stacks.

Empty/foreign selection, active tasks, pending edit transactions and ambiguous or
cyclic container ownership reject without applying a display. Errors appear in
the status bar and Report view. Restore is separate from model Undo/Redo. Native
visibility may mark the document modified; restore before save to retain the old
display. The session stack is not serialized. Save-time temporary-display policy,
linked member overrides and physical/high-DPI acceptance remain pending.
[Owner procedure](../tests/TemporaryDisplay.md).


## UI-010: Manufacturing STL export (F127; roadmap 15.7)

Part > Manufacturing export opens a modeless review dialog for selected whole
solid objects/Body results or whole solid link occurrences. Inputs list document,
label, internal identity and world bounding dimensions. Use current selection
explicitly replaces the list; unrelated selection changes do not retarget export.
Faces/edges, Part containers, mesh objects and members inside linked components
are rejected. Whole native objects selected through their Part tree path work.

Output is fixed and visible: STL, millimeters, world placement. Quality preset
offers Coarse/Normal/Fine and custom per-user names; linear deflection (0.001-10 mm)
and angular deflection (1-90 degrees) remain visible/editable. Save custom preset
stores only these values, updates an existing custom name, and reserves built-in
names. Reset removes custom presets. No input/configuration/path is saved with one.

Choose file fills the editable output path. Export requires a .stl suffix and
existing folder, rechecks input identities/current state and solid geometry, then
uses the existing mesh service and rejects nonclosed output. Existing-file replacement
requires an explicit Yes, default No; errors retain fields for correction. Success
reports triangle count, output dimensions and full file path. Close leaves exports
intact and creates no modeling transaction or feature. Stale/deleted inputs must
be repaired/reselected; export never falls back to an object with a reused name.

The loss notice states that STL lacks feature history, units metadata, colors and
assembly identity. It explicitly describes current recomputed input geometry and
no fusion/collision check. More formats, configuration/orientation/unit controls,
mesh inputs and physical/high-DPI acceptance remain pending.
[Owner procedure](../tests/ManufacturingExport.md).


## UI-011: Sketch support (F124; roadmap 11.7)

Sketcher workbench > Sketch > Inspect and change sketch support requires one
selected sketch outside edit mode. The modeless editor shows current support and
world placement, a read-only replacement object, editable face name, Use selected
planar face, local/world placement policy, numeric Preview, Apply and Close.
The selected face resolves native nested Part paths; occurrence paths reject.

Preserve local retains the native attachment offset and follows the new support.
Preserve world solves an offset to retain the sketch's current world transform.
Preview evaluates planar attachment in a disposable hidden document and reports
candidate world origin/axis/angle and attachment offset in mm/degrees. It does not
simulate constraints/downstream solids or add geometry to the source document.

Apply requires a matching fresh preview and revalidates the native support contract.
Changed sketch/support geometry, placement, attachment state, policy or expression
invalidates the preview; the user must preview again. A successful Apply owns one
undo transaction, refreshes current-support text and leaves dependent-result checking
to the user. Close discards unapplied choices; previous successful Apply remains.

Errors appear inline without closing the editor. Invalid/missing candidate faces,
dependency cycles, stale supports, pending edits and direct cross-container/occurrence
references reject. Preserve local supports broken-face repair; Preserve world needs
a valid old placement and cannot replace an expression-driven offset. Deleting the
replacement clears it; deleting the sketch or closing its document closes/detaches
the editor. Activate the target document before preview or Apply.

Graphical ghost preview, general datum/occurrence support and physical/high-DPI
acceptance remain pending. [Owner procedure](../tests/SketchSupport.md).

## UI-012: Dependency inspection (F015; roadmap 7.5.5a / 10.6a)

Tools > Inspect dependencies requires one selected object and no active task.
The modeless dialog shows root label/internal identity, type, native state/status,
Inspect selected object, Refresh and Include transitive dependencies. Inputs/upstream
and Consumers/downstream tabs list feature, relationship/depth, linking property,
state and document. Native expressions, container membership and loaded external
links are shown alongside geometry dependencies; no target role is guessed.

A row shows native status, a traversal path and source file (or Unsaved document).
Inspect this row changes the root explicitly. Select in model activates its document
and replaces native selection while preserving visibility; hidden objects remain
hidden. Selecting a table row alone changes neither document selection nor geometry.
Selection-changing actions reject while a native task is active.

Empty tables state that no links exist in that direction. Graph edits/recompute clear
rows and require Refresh. A deleted/replaced identity cannot be selected through an
old row. Deleting the root or closing its document closes and detaches the editor.
Native invalid-reference status is visible, but null optional links are not invented
as missing-reference errors. Inspection never opens unloaded files or recomputes.

Traversal uses at most 500 edges and 8 levels per direction, with an explicit partial
view notice and node navigation to continue. Cycles in the displayed portion produce
a warning. The view is inspection rather than a deletion plan. Broader navigator,
reference repair and physical/high-DPI acceptance remain open.
[Owner procedure](../tests/DependencyInspector.md).

## UI-013: Measurement meaning and snapshots (F098/F099; roadmap 15.1a/b)

The existing Tools > Measure task retains its Mode, Result, units, delta controls
and Save/Close behavior. Selected entities now lists operand labels and native
document/object/subelement paths. A plain-text meaning field explains the selected
measurement policy and frame. These are details of the current selection, not
editable input replacements.

Distance distinguishes circle/arc centres, infinite datum axes/planes and otherwise
minimum separation. Delta components are unsigned world-axis differences. Distance
Free is explicitly a point snapshot: picked world coordinates, not minimum clearance
and not associative after Save. It displays UTC capture time when available.
Geometric Center explains that density and physical mass are not included;
radius/diameter are not thickness. Existing native units control the displayed value.

Saved Distance Free objects expose read-only Snapshot properties: UpdatePolicy,
CaptureTime and CaptureSources. Paths describe the original pick and create no live
dependencies. Manual Position1/Position2 edits clear capture provenance; Undo/Redo
restore the recorded transaction state. Save/reopen preserves metadata. Old or
uncaptured objects keep unknown provenance rather than receiving a new capture date.
Clearing selection clears operand text and disables Save under the existing task
contract. Close removes an unsaved preview; saved objects remain.

Broader mass/thickness/mesh semantics, associative error/repair and physical/high-DPI
acceptance remain pending. [Owner procedure](../tests/MeasurementContext.md).

## UI-014: Occurrence appearance (F018; roadmap 12.2b/c)

View > Occurrence appearance requires one whole native Link selected in the tree.
The modeless editor identifies the occurrence and shared source, and provides Visible,
Override source appearance, Colour (all faces), Transparency (0-100%), Use source
appearance, Reload current values, Apply and Close. Colour uses the native Qt chooser.
Colour/transparency controls are disabled while inheriting source appearance.

Controls stage values without a live model preview. Apply validates the original
link/source identity and appearance state and owns one native Undo transaction.
Only link visibility and native display override properties change. Source geometry,
other occurrences, placement and engineering material are preserved. Use source
appearance stages disabling OverrideMaterial; it does not change visibility or copy
source values. Reload discards the staged form and reads current values. Close
discards unapplied choices while keeping completed Apply transactions.

Changed link targets or appearance require Reload before Apply. Deleted source
disables Apply until repair/reload; deleting the occurrence or closing its document
closes and detaches the editor. Active tasks and pending edits block Apply. Errors
appear inline and leave the form recoverable.

Supported links directly target a Part shape or Body in the same document. Structural
Part container selection paths are accepted; traversal through another Link is rejected. Arrays,
per-element overrides, selected subelements/nested occurrence paths, external
documents and mixed Part definitions remain outside this pilot. Visibility is display
state, not suppression or BOM policy; colour is not a material/mass/FEM assignment.
Physical/high-DPI and broader occurrence acceptance remain open.
[Owner procedure](../tests/OccurrenceAppearance.md).

## UI-015: Interference and clearance (F101; roadmap 15.1c/d)

Part > Interference and clearance opens with explicit whole-object selection. The
input list shows native identities and included checkboxes. Replace inputs with
current selection deliberately changes scope; ordinary selection navigation does not.
Required clearance and contact tolerance use explicit world mm. Check included pairs
produces first/second input, text status, distance, common solid volume and details.
Unreadable/unsupported inputs remain Unresolved, and the summary says Incomplete.
Exclusion counts and selected-set scope remain visible; no full-assembly claim is made.

Select result pair changes native selection only; hidden inputs are not revealed
automatically. Changing controls, exclusions or document objects clears results and
disables navigation until recheck. No live geometry preview or document edits occur.
Close detaches the document observer; closing the document closes the dialog.
Pending edits and active tasks must finish before checking. Errors stay inline.
Scope/limitations and owner procedure: [Interference check](../tests/InterferenceCheck.md).

## UI-016: Missing-coincidence review (F049; roadmap 11.6a/b)

Existing Sketcher Validate Sketch, Missing Coincidences section: explicit Search
tolerance (mm), Ignore construction geometry, Find, candidate list and Add Checked
Coincidences. Columns identify both geometry endpoints and measured gap. Selecting
a row displays endpoint markers; checkboxes default off. Only checked candidates
are committed, as one Undo step. Existing constraints remain. Solver conflict aborts
the repair and reports restoration inline. Close clears markers and preserves only
completed repairs. No geometric before/after preview is claimed.

Sketch or search-policy changes clear the list and disable repair until Find.
Invalid/zero/out-of-range tolerance reports a correction; no fallback search runs.
No candidates reports that other profile defects may remain. Other inherited
validation sections are unchanged. [Owner procedure](../tests/SketchRepairReview.md).

## UI-017: Mirror result behavior (F057; roadmap 13.5a/b)

Existing Part Mirror retains its shape list, standard/reference plane and base-point
controls. Result behavior explicitly chooses Associative mirror (default) or
Independent shape snapshot. The policy text distinguishes updates/links, separate
geometry and lack of copied feature history. OK creates all selected results in
one transaction; Cancel creates nothing. No live geometry preview is introduced.

Missing references, dirty/deleted/replaced sources, pending edits and unsupported
snapshot scope produce inline feedback while preserving the task for correction.
Invalid result creation aborts the transaction. Successful independent results have
snapshot labels; the native associative editor remains unchanged. No source hiding
or Body Tip mutation. [Owner procedure](../tests/MirrorResultMode.md).

## UI-018: Numeric and saved section planes (F100; roadmap 15.1e/f)

View > Clipping View retains native X/Y/Z or custom-plane controls in a scrollable
dock so short windows do not compress the direction inputs. Offsets show mm
and world-frame tooltips; View and camera-follow synchronize the displayed normal.
Zero direction pauses custom clipping with inline recovery guidance. Axis planes
may combine; custom clipping disables axis planes, following existing behavior.

Save section planes and Load section planes use standard file dialogs. Cancellation
leaves the view unchanged. Save captures actual native plane state; Load validates
the whole versioned preset before applying and disables camera following. Errors
stay inline; presets never alter camera/model or own a document transaction.
The panel explains whole-model export/measurement behavior, lack of caps, separate
preset storage and Close removing clipping. [Owner procedure](../tests/SectionPlanes.md).

## UI-019: Find and describe features (F014; roadmap 10.6b/c)

Tools > Find and describe features opens the active document's loaded metadata list.
Search matches all typed words across label/name/type/description, case-insensitively;
the type filter uses native types. Rows show label, stable internal name, type and
multiline description, with explicit scope/match count and partial-search disclosure.
Sorting only changes the list; Select in model preserves visibility and requires the
same active document with no task dialog.

Selecting a row fills staged Label and Description fields. Apply saves one native
transaction; unchanged values create none. Close, Refresh, row or filter changes discard
unapplied text, as explained in the panel. Model edits invalidate the snapshot and
require Refresh; failed Apply remains open with inline guidance. Document closure
closes the dialog and removes its observer. [Owner procedure](../tests/FeatureOrganizer.md).

## UI-020: Make occurrence unique (F019; roadmap 12.2d/e)

Tools > Make occurrence unique reviews one explicitly selected whole Link. The
modeless dialog lists occurrence/source identities, same-document destination and
copied sketch/extrusion inputs, plus an editable new definition label. The policy
explains internal remapping, independent source behavior, preserved placement and
one-step Undo. Make Unique commits and closes; Cancel creates nothing.

Unsupported definitions show inline reasons with creation disabled. Model edits
invalidate review; Review again revalidates current inputs after recompute. Pending
edits/active tasks, changed identity and empty labels prevent commit with inline
feedback. Occurrence/document deletion closes the dialog. Broader relationship or
subassembly remapping remains out of scope. [Owner procedure](../tests/UniqueOccurrence.md).

## UI-021: Drawing setup (F102; roadmap 15.3a/b)

TechDraw > Page > Create drawing sheet reviews one selected root solid/Body. The
modeless dialog identifies the source and offers A4/A3 landscape template, explicit
drawing/model scale, named base orientation, first/third-angle projection and optional
top/right views. Sheet coordinates are millimetres; no global unit preference changes.

Create sheet adds the page/template/views in one Undo transaction and opens the native
sheet. Cancel creates nothing. Source/document edits invalidate review; recompute and
Review again restore eligibility. Size/template/context errors stay inline for correction.
Source/document deletion closes the dialog. Geometry preview, section/detail views and
annotations remain separate. [Owner procedure](../tests/DrawingSetup.md).

## UI-022: Document updates (F087/F088; roadmap 7.5.7a/b)

Tools > Document updates opens a modeless panel bound to the current document. A native
deferral checkbox, failed/pending counts and object/status/affected-input/native-detail
columns distinguish visible cached results from model currency. Object/input selection
preserves visibility. Refresh status rereads flags; Recompute now updates once, retaining
mode. Pending owner transactions, wrong document and active tasks receive inline guidance.

Close retains the session setting; document closure removes observers/timers. The panel
states native preview exceptions, session persistence and background/external scope limits.
There is no custom geometry state or automatic repair. [Owner procedure](../tests/DocumentUpdates.md).

## UI-023: Move occurrence once (F074; roadmap 10.7a/b)

Tools > Move occurrence once reviews one explicitly selected whole Link. Translate/
Rotate and World/Occurrence selectors label frame meaning. Translation uses incremental
mm offsets; rotation uses a dimensionless axis, degrees and pivot coordinates in mm.
Irrelevant fields are disabled. Preview adds a non-pickable teal wireframe and reports
world-origin coordinates. Original geometry stays visible. Value changes remove the
old ghost; model/frame changes also invalidate review.

Move once commits one placement transaction and closes; Cancel removes the preview
without model changes. Failures remain inline for correction. Document/occurrence
closure removes the ghost and observer. No hidden mates, copies or solver detachment.
[Owner procedure](../tests/OccurrenceMove.md).


## UI-024: CAM mesh preparation (F091; roadmap 14.1a/b)

CAM > Review CAM mesh (`CAM_MeshPreparation`) opens a modeless review of one whole
root imported Mesh::Feature. The native source identity is fixed for the dialog.
The table reports mm dimensions/bounds, triangles/points, boundary/nonmanifold
edges, connected components, inconsistent normals, zero-area/duplicate triangles,
closed topology/orientation and density. At 100,000 triangles density is flagged;
above 200,000 this bounded review refuses without modifying the mesh.

STL units are not inferred. Open surfaces receive different Parallel/Waterline
advice; no new operation gate or path approval is implied. Self-intersections,
accessibility and stock/tool clearance are explicitly unchecked. Orientation is
undetermined for open, inconsistent, multiple-component or degenerate input.

Create reversed-normal copy is available only for a single consistently inward,
closed component without duplicate/zero-area triangles. Its explanation previews
reversal of every triangle with unchanged coordinates and dimensions. Confirmation
creates one independent native mesh in one Undo transaction; source visibility,
geometry and existing job model links are unchanged. The result may visually overlap
its source; success names the result and tells the user to choose it explicitly for
a new job. Failure rolls back. An active task, pending or booked owner transaction,
inactive source document or stale input refuses confirmation.

Review again refreshes the report; document edits clear stale findings and disable
copying. Source deletion/document closure closes the dialog and removes its observer.
Close without copying changes no model state. No hole filling, welding, smoothing,
decimation, scaling or per-piece repair is included. [Owner procedure](../tests/MeshPreparation.md).


## UI-025: Copy reusable sketch (F053; roadmap 11.6c/d)

Sketcher > Sketch > Copy reusable sketch (`Sketcher_CopyReusable`) opens a modeless
review of one whole free root sketch. Geometry/constraint/degree-of-freedom counts
identify the copy scope. Fields specify a new label, X/Y/Z offsets in the source
sketch axes and a signed angle about its normal. Rotate about the source origin,
then translate in source axes. The native whole-sketch copy keeps local geometry,
internal constraint indices, named dimensions and construction roles; changing its
Placement preserves horizontal/vertical semantics in the new sketch's own plane.

Preview reuses the non-pickable view-only overlay and shows the resulting world
origin in mm. It frames the complete scene including the proposed copy; native Fit
All would omit this overlay. Numeric edits clear the preview. Model edits invalidate
the reviewed snapshot, clear the overlay and disable Preview/Create until Review
again. Source deletion/document close removes the observer and overlay. Cancel
creates no object or Undo entry. Camera framing is a view change, not a model edit.

Create independent copy uses the native document copier in one transaction, shows
the new sketch and closes on success. The source and downstream consumers are not
copied or relinked. Failure aborts creation and leaves the dialog available. Empty
names/non-finite numeric inputs, stale geometry, inactive document, active tasks
and booked/pending owner transactions refuse confirmation.

The first increment accepts up to 500 geometry elements, with visible geometry and
valid current constraints. Body/Part/occurrence scopes, support, external geometry,
expressions and other linked inputs are refused with an inline explanation; the
command never silently drops them. Partial paste/remapping, reference policy choices,
blocks, libraries, patterns and physical/high-DPI acceptance remain open.
[Owner procedure](../tests/SketchReuse.md).


## UI-026: Native BOM scope and exclusions (F104; roadmap 15.4a/b)

The existing Assembly > Bill of Materials command and native BOM double-click
editor now expose Excluded from this BOM. A list shows omitted object labels and
internal names. Exclude tree selection adds whole same-document objects from the
BOM's assembly scope, or native document-wide tree roots when no assembly owns it.
Faces, unrelated assembly objects, the BOM and its ancestors are refused. Picker
traversal is limited to 2,000 objects. Select list rows and Include again to restore
inclusion. The native excludedObjects link-list property saves the policy per BOM.

Hidden components stay included. Selecting an occurrence excludes that occurrence;
a child occurrence stored in a reused definition is excluded in every use of that
child. This is not a path-specific override or global reference-only role. The
picker does not replace occurrences with their source definitions. Native quantities
are per parent; a repeated parent quantity multiplies its displayed child quantities
for overall totals. A later sibling cannot merge into an earlier nested child row.
Uniformly mirrored native links remain separate quantity groups. Native scope lookup
also follows the containing BOM group to its owning assembly.

Edits reuse the existing native BOM task transaction. Cancel restores prior policy
and counts; Accept commits, recomputes and opens the sheet. An inactive document or
pre-existing task/booked/pending edit transaction refuses editing/confirmation, and
commit/abort uses the owning GUI document. Exclusions do not alter visibility,
placements or source geometry. The existing spreadsheet export carries scoped rows.
Item numbers regenerate after structure/inclusion changes; no persistent balloon
numbering is claimed. Arrays, suppression/configurations, external/unloaded scopes,
custom-column identity and exploded documentation remain open. Native editor/
recompute refresh remains the workflow; no new automatic change tracker is added.
[Owner procedure](../tests/AssemblyBomScope.md).
