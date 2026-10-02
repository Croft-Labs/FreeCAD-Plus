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

### Toolbar UI styles

[Toolbar governance and visual reference](details/ui/TOOLBARS.md) owns the
workbench-by-workbench Classic/Plus command placement, consolidation inventory,
icons and button/function catalog. Keep it synchronized when toolbar membership,
sections, dropdown choices or captions change. This section owns shared behavior
and sizing requirements.

**Standing owner UX directive (October 2, 2026):** apply action hierarchy to all
new or modified UI. Give the most commonly used actions visual priority, keep
secondary actions compact and collect infrequent related choices in dropdowns.
Keep choices discoverable through tooltips, accessible names and meaningful groups;
preserve native command states and shortcuts. Do not give every operation equal
visual weight or expand every rare variant into a separate labeled button.

For Plus ribbon sections, primary commands such as Extrude and Revolve occupy
one row of large buttons spanning the section's three-row grid. Secondary commands
use small icons without visible name text, stacked in three rows with as many
columns as required. Large-button captions have a bounded width (76 logical pixels
including button padding); retain full names in tooltips/accessibility when
elided. Align buttons to a consistent grid. Related variants share dropdowns:
Auto Dimension is the default dimension action, with vertical, horizontal, angle,
radius and diameter choices and less common dimension types in its menu.

#### Revised toolbar layout

The owner's revised outline adds a small-icon horizontal toolbar **above** the
ribbon, shared by all modes: File (New File/Open/Save/Save As), Edit
(Undo/Redo/Recompute), and Clipboard (Cut/Copy/Paste). These actions remain visible
across mode/tab switches. This is an intentional Plus toolbar, not permission to
show Classic workbench toolbars alongside the ribbon.

Add **medium / half-size** icons between full-size and small. Size and dropdown
are independent: any size may have a dropdown. Full and medium captions have
bounded widths; small icons have tooltips/accessibility but no visible caption.
Small ribbon icons retain a three-row grid; common-toolbar icons use one row.
Full icons use 40 logical pixels, medium 20, and small 16. The grid is 76px
high: full buttons span it, two 38px medium buttons or three 24px small buttons
fit a column. Reference-document artwork sizing is independent of these values.

Design Home contains the most frequently used actions from the other tabs.
Its Main group has medium New Component, Add Component, New Sketch and Coordinate
System; Coordinate System has coordinate-system/plane/axis/point choices.
The [toolbar reference](details/ui/TOOLBARS.md#plus-ui-target-layout) owns the
detailed placements completing the incomplete owner outline, including the added
Assembly tab and retained Sketch tab. Std_NewComponent creates an embedded model
with no assembly occurrences and opens its editing tab. Add Component inserts a
linked occurrence, reusing or creating a definition through the existing chooser.
Both follow the approved component contract and native transaction/ownership rules.

These changes are incorporated in the October 2 audit build. Earlier October 2
folders retain their previous layout; the owner shortcut must target the validated
audit payload. Initialize specialist Home actions only after the main window is
visible, to preserve Classic visibility when native setup saves toolbar state.

Edit > Preferences > General includes UI style: **Plus UI** and **Classic UI**.
Plus UI is the default when no UI style is saved. Preserve an explicitly saved
Classic UI choice and its existing workbench toolbar presentation. Apply/OK switches immediately and persists the
choice; Cancel leaves the unapplied selection unchanged. These are application UI
preferences, separate from document data, themes and geometry operations.
The styles are mutually exclusive: Plus hides all native Classic toolbars,
including newly created bars and late workbench/layout show events; Classic hides
both Plus bars. Restoring a saved layout must not override the selected style.
Switching back to Classic restores its toolbar visibility choices.

Plus UI replaces the visible toolbars with a top ribbon. A mode dropdown at the
upper left lists available workflow workbenches, including Design, Draft, CAM,
Assembly and Drawing where installed. FEM and installed 3D printing workbenches
are included when registered; do not show invented/unavailable modes. Other
installed workbenches retain their own labeled mode. Native workbench activation
keeps the selector synchronized; changing modes during an active task is refused.

Design has **Home, Modeling, Surface, Sketch, Assembly, Mesh, View**, in that order.
Home groups Main, Modeling, Surface, Sketch, Assembly, Mesh, View, Structure,
Utilities, Help and Macro. File/Edit/Clipboard commands stay in the common bar.
The New File button uses the standard New Document (`document-new`) icon and
native Std_New action, which routes to the component-document workflow.
Home retains Coordinate System/Plane/Axis/Point in the Coordinate System dropdown,
Variable Set as a small button, and Macro actions in one compact dropdown. Iconless native actions use ribbon-only
fallback artwork and retain their original QAction state and menu identity.
Modeling groups native Part Design Modeling, Transformation, Dress-Up and Helper
commands, in that order. Surface, Sketch, Assembly and Mesh reuse the
toolbar group boundaries of their corresponding native workbenches. View groups
standard view orientation/fit and display controls. Unavailable workbench tabs
are disabled. Other modes use Home, Tools and View; Tools preserves that mode's
native workbench command groups.

The ribbon presents primary native command icons with bounded captions beneath
them, secondary icons in three rows, labeled sections and grouped dropdowns.
It shares QAction enablement, checked
state, tooltips, shortcuts and operation lifecycle with menus/Classic toolbars.
Horizontal scrolling keeps sections reachable in a narrow window; the mode and
tabs remain at the top. Preserve Classic toolbar visibility across mode switches
and restoration. Do not apply a global stylesheet or change document ownership,
selection, geometry or command semantics to implement the ribbon.

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

### Component New Sketch support choices

In a component document, both native New Sketch commands open the component-owned
New Sketch task without requiring a Body. Plane offers XY, XZ, YZ, Selected planar
face, User plane and Create new plane. Origin planes are temporarily displayed;
preselection and viewport picks choose the support. Use selected face or plane
also captures a support explicitly. User plane lists local native datum planes
and Part planes by label while retaining object identity.

Create new plane reveals Base plane and Rotation X/Y/Z. The base can be an origin
plane, local planar face or existing user plane. Offset is measured along the
base normal; rotations apply X, then Y, then Z in the base frame. OK creates a
native PartDesign plane and the attached sketch in one creation transaction,
then opens native Sketcher after the New Sketch task closes. The sketch has zero
additional offset on its newly created plane. Cancel creates neither object.
Native Sketcher owns subsequent edit transactions separately.

Planes remain component-owned History objects, named Plane001, Plane002, etc.
per component; no Body is added. Origin and user-plane sketches use native
ObjectXY attachment, while face sketches use FlatFace. Edit AttachmentOffset
to change a supported sketch/plane's offset or rotation. New sketches follow
their support through recompute and save/reopen. Existing detached sketches
retain their prior placement and attachment state without migration.
Nonplanar, missing, stale and foreign-component supports reject inline and leave
the task open for correction; foreign geometry requires a local reference.

Sketcher construction curves are reference geometry: they participate in solving
but are excluded from the solid profile. Driving dimensions control geometry;
reference dimensions measure solved geometry. Existing native drawing, dimension,
constraint, expression and repair tools retain these semantics. Automated coverage
and physical acceptance limits are recorded in [the sketch workflow procedure](../tests/SketchWorkflow.md).

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

## UI-023: Move or copy occurrence (F072/F074; roadmap 10.7a-d)

Tools > Move or copy occurrence reviews one explicitly selected whole Link. Translate/
Rotate and World/Occurrence selectors label frame meaning. Translation uses incremental
mm offsets; rotation uses a dimensionless axis, degrees and pivot coordinates in mm.
Irrelevant fields are disabled. Preview adds a non-pickable teal wireframe and reports
world-origin coordinates. Original geometry stays visible. Value changes remove the
old ghost; model/frame changes also invalidate review.

Move once commits one placement transaction and closes; Cancel removes the preview
without model changes. Failures remain inline for correction. Document/occurrence
closure removes the ghost and observer. No hidden mates or solver detachment.

Action defaults to **Move existing occurrence**. **Copy occurrence (shared
definition)** enables Copy label and changes confirmation to **Create linked copy**.
The copy is a new native Link in the same structural container, with the same
source, appearance, visibility and LinkTransform policy. Only its placement changes;
source edits affect both links. The original occurrence stays in place. Zero offset
is allowed as an explicit coincident copy. Empty labels are refused inline.
Changing action or label clears the preview. Copy commits one Undo step and closes;
Cancel creates nothing. Copy does not create an independent definition or array.
The existing Std_MoveOccurrenceOnce command identity is preserved.
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


## UI-027: Shape Builder sewing and solids (F068; roadmap 13.1a/b)

Part > Shape Builder / Part_Builder keeps the existing shell and solid modes.
Edge/wire/face modes retain their existing behavior. Shell/solid inputs are bounded
to same-document root Part features or root Body results, 500 faces maximum;
Links/nested members, stale inputs and pending edit transactions are refused.

| Control | Action and feedback |
| --- | --- |
| Shell from faces | Select faces. All faces expands selected source objects; repeated input faces are deduplicated. |
| Sewing tolerance (mm) | Shell mode only; 0.0000001-1 mm, default 0.000001. Passes the explicit value to native sewing. |
| Check shape | Computes without document changes: classification, shell/face counts, free-edge names, requested/result maximum tolerance. |
| Solid from shell | Select one whole closed shell. Only one valid positive-volume solid can be created; failures stay inline. |
| Refine shape | Existing native refinement, followed by result validity checking. |
| Create | Rechecks current inputs and makes one independent Part feature in one native transaction. Source geometry/visibility stays unchanged. |
| Close | Ends this multi-create utility; accepted results remain. Undo removes each accepted result. |

Selection/tolerance/refine changes invalidate the displayed check. Status uses plain
wrapped text; errors preserve selection. The owner document is checked before
review/creation. Results store read-only source-name provenance and sewing tolerance;
these are snapshots, not associative features. Free-edge names belong to proposed
result topology, not stable source repair targets. Source tolerances may already
exceed requested sewing tolerance; the report discloses maximum result tolerance.
No automatic escalation, graphical boundaries or ghost preview is claimed. Recorded
UI calls require the live Shape Builder and selection; standalone macro replay,
localization and physical keyboard/high-DPI acceptance remain open.
[Owner procedure](../tests/ShapeSewing.md).


## UI-028: Replace occurrence source (F022; roadmap 12.6a/b)

Tools > Replace occurrence source / Std_ReplaceOccurrenceSource takes one whole
unscaled direct native Link in the active document. Structural Part container paths
reuse the existing whole-occurrence selector; links through links, arrays and native
assembly relationships are outside this workflow. Both old and replacement sources
must be current root single solids or whole root Bodies in the same document.

| Control | Action and feedback |
| --- | --- |
| Occurrence/current-source summary | Labels and internal names identify the edited instance and its current definition. |
| Source placement: Included/Ignored | Reports the existing native setting; replacement retains it and its consequence for source coordinates. |
| Replacement source | Same-document root shape candidates by label/internal name; invalid/stale/non-solid choices disable Preview/Replace with a reason. |
| Review again | Refresh candidates and native identities/state after recompute or changed inputs; retain the selected source by explicit identity comparison. |
| Preview | Existing non-pickable teal overlay in the occurrence's world frame; frame both model and overlay without adding document objects. |
| Replace | Revalidate and relink only this occurrence, preserving ID/name, label, placement, visibility and uniform appearance override. Inherited appearance follows the replacement. One native transaction; rollback on failure. |
| Cancel | Close and remove the preview, without model edits. |

No copying, alignment inference or face-number/mate remapping occurs. Consumers,
driven/read-only links, copy-on-change and per-element appearance are refused.
Document edits clear the preview and require review; deletion/close removes it.
An empty source list explains how to provide a replacement. Check/preview/commit
errors stay inline. UI state is separate from the saved native link. Keyboard/high-DPI
acceptance, macro recording and broader replacement scope remain pending.
[Owner procedure](../tests/OccurrenceReplace.md).

## UI-029: Sampled face deviation (F071; roadmap 15.2a/b)

Part > Sampled face deviation / Part_SurfaceDeviation compares two explicit faces
on current root Part shapes or root Body results in the active document. Links,
nested members, cross-document inputs and pending edit transactions are refused.

| Control | Action and feedback |
| --- | --- |
| Capture sampled face / Capture reference face | Capture exactly one selected face for that role; show label, internal name and face number. Failed capture clears that role. Whole single-face objects also work. |
| Samples per UV direction | 3-25 cell-center samples in each direction, default 11. Does not sample boundaries or guarantee uniform physical spacing. |
| Full color scale (mm) | Explicit 0.000001-1000000 mm, default 1. Blue zero, yellow half scale, red full scale or greater; numerical values are never clipped. |
| Check and show map | Native unsigned nearest distances to the finite reference face, including boundaries. Non-pickable colored point overlay; usable/outside/singular-failed counts and sample min/max/mean. |
| Clear map | Remove the overlay and current report; retain captured roles and settings. |
| Save sampling settings | Explicitly persist grid and scale in user preferences; never save references, results or geometry. |
| Close | Remove the map and observer. No geometry/appearance changes or Undo entries. |

Markers render on top of geometry. One-way UV sampling is not area weighted and can
miss narrow defects/boundary extrema. The dialog states that sample maximum and map
colors are not certification. No alignment or normal-direction projection occurs.
Singular/failed points produce an incomplete report; all-unusable input gives an
inline error. Input geometry/placement snapshots refuse silent face rebinding.
Settings and document edits clear the map; changed geometry requires deliberate
recapture. Document activation changes clear it, and closing its owner closes the
dialog. Native files contain only the original model. Zebra, combs, continuity,
adaptive/bidirectional/global deviation and physical/high-DPI acceptance remain open.
[Owner procedure](../tests/SurfaceDeviation.md).

## UI-030: Clarify Selection / Select Other (F037; roadmap 10.5c/d)

The existing Std_ClarifySelection command remains available from the native 3D-view
context menu and G, G shortcut. It uses the current cursor or stored context-menu
position and the existing ray-pick radius, geometry roles and selection service.

| Interaction | Behavior |
| --- | --- |
| Open over overlapping geometry | Show native type categories, then label/internal-path ordering. Candidates use document/root/full subpath identity, so repeated labels cannot collapse distinct occurrences. |
| Candidate labels | Include `[document#root.occurrence.path.]`; grouped submenu titles also include context. Tooltips show the complete selected path. |
| Hover / keyboard highlight | Native transient preselection of the candidate's exact path. Current root identity and command gate are rechecked. |
| Accept | Recheck identity and gate, then add the exact target through native selection. Existing selections remain for command collectors. |
| Escape / dismiss | Clear transient preselection; leave existing selection and model unchanged. |
| Active native command filter | Omit disallowed element/whole-object roles. Whole objects can still be derived from face hits for object-only gates. The menu never changes the gate. |
| All candidates filtered | Disabled explanation: No candidates pass the current selection filter. Leave the owning command to restore its selection policy. |

Only geometry participating in native ray picking is offered; intentionally hidden
objects are not revealed. Ordering is not a nearest-depth ranking. Invalid paths
are omitted instead of falling back to an outer container. Root deletion/recreation
with the same name cannot redirect hover or acceptance. No model, visibility, Undo
or persistence changes occur. Global type controls, new scopes, live topology/menu
rebuilding, localization and physical/high-DPI/navigation-preset acceptance remain
open. [Owner procedure](../tests/ClarifySelection.md).

## UI-031: Sketch constraint repair (F048; roadmap 11.4a/b)

Sketch > Review constraint repair / Sketcher_ReviewConstraintRepair accepts one
whole free root sketch outside edit mode. Invalid/conflicting native results are
allowed; a hidden temporary native copy is solved for diagnosis and preview.

| Control | Action and feedback |
| --- | --- |
| Solver summary | Native conflict/redundancy/malformed/failure groups, or successful fully/underconstrained state and freedom count. Failed counts are not presented as movement diagnosis. |
| Constraint table | Number/name, type, dimensional value/units, active/reference/diagnostic state and involved internal edges. No repair checkbox is selected automatically. Inactive constraints cannot be chosen. |
| Select row geometry | Select internal geometry through the native selection service; axes/origin-only relations have no internal edge. Source data stays unchanged. |
| Preview deactivation | Solve the checked choice on a temporary copy. Success shows resulting degrees of freedom and an automatically framed view-only wireframe; unresolved diagnostics disable Apply. |
| Apply deactivation | Recheck snapshot and native solve; deactivate selected constraints and recompute in one transaction, with rollback on failure. Preserve constraint numbers, names and values. |
| Review again | Remove preview and reload current native diagnostics; clear previous repair choices. |
| Cancel | Close and remove the overlay; leave source model unchanged. Explicit row selection is not undone. |

Document changes invalidate the proposal. Deletion/close cleans up the dialog.
Scratch documents close after every probe; source objects, Undo history and active
document remain intact. Scope is limited to 200 geometries/400 constraints on free
root sketches without external geometry, attachment, expressions or other linked
inputs. Body/Part members and active tasks/edit transactions are refused. Solver
groups are conservative candidate sets, not unique causes. Freedom counts do not
describe all coupled motions. Downstream geometry is recomputed only on Apply;
consumer-wide previews, constraint replacement and broader/physical acceptance
remain open. [Owner procedure](../tests/ConstraintRepair.md).

## UI-032: Native sheet thickening (F067; roadmap 13.1c/d)

Existing Part > 3D Offset / Part_Offset retains the native Source, Value, Fill,
Mode and Join identities. Select one whole sheet object; the bounded thickening
workflow uses Skin mode and Fill. A separate native result remains associative.

| Control | Behavior |
| --- | --- |
| Signed distance | Native length entry. Positive follows sheet normals; negative uses the opposite side. Absolute distance is the complete one-sided thickness when filled. |
| Reverse side | Negate a numeric value; preserve saved expressions by requiring formula editing instead. |
| Fill between source and offset | Join the source/offset boundaries. Filled face/shell inputs must yield a valid closed solid. Unfilled offsets remain sheets. |
| Result message | Solid/face counts, sheet classification, deferred-preview state or explicit failure. Cached last-success geometry after failure is not presented as a current result. |
| Update view | Recompute previews while checked. When unchecked, parameter edits stay pending until enabled or OK. |
| OK | Recompute the owning document and commit the native transaction only on success. Failure stays inline with the task and transaction open for correction. |
| Cancel | Abort the transaction before resetting native edit mode; restore an existing committed feature or remove a new uncommitted offset. |

The same task's 2D controls keep their labels and hide the 3D side/result controls.
No new Boolean targets or symmetric thickness mode are implied. Graphical normals,
compound inputs, broader kernel failures, localization/high-DPI and physical owner
acceptance remain open. [Owner procedure](../tests/SheetThickening.md).

## UI-033: CAM setup-template review (F096; roadmap 14.4a/b)

Existing CAM Export Template and New Job use native version-1 templates and native
job, model, stock, tool-controller and setup-sheet services. No operation/path copy.

| Control/state | Behavior |
| --- | --- |
| Export: Template name / Revision | Editable metadata; fallback to job label / revision 1. Template-only edits do not alter the source job. Native stored-value units are recorded separately from document display units. |
| Existing export inclusion choices | Preserve native post/tool/stock/setup selections. Excluding posts also excludes post-property overrides. Validate portable settings before writing the chosen file. |
| New Job: template selector | Existing search paths and descriptions. Read-only scrollable review shows identity, stored units, post/arguments/output, stock rules, tools/feeds and setup values. Omitted settings use current defaults. |
| Incompatible template | Inline explanation and disabled OK for unsupported format/post/tools/units, incomplete stock dimensions or detected model-specific expressions. Re-select after correcting the file. |
| File changed during review | Reload the review and require another OK. Job creation uses the exact accepted settings snapshot; later file edits cannot change it. |
| OK / Cancel | Existing model selection and unit-schema flow. Native transaction creates the editable job, clones, stock and tools; existing GUI creation rollback handles instantiation errors. Cancel creates no job. |
| Created job provenance | Read-only TemplateName and TemplateRevision properties under Setup template; no continuing link to the file. Native settings remain editable. |

Fixed stock size/placement may need adjustment for a different model. Current-format
embedded tool data and portable setup-sheet expressions are supported; unavailable
tool assets or other native instantiation failures roll back in the GUI path.
Legacy metadata is marked unknown. Recurring operation sequences, complete machine
compatibility, broader reference remapping, localization/high-DPI and physical
acceptance remain open. [Owner procedure](../tests/SetupTemplates.md).

## UI-034: Saved exploded-view output (F080; roadmap 12.7a/b)

The existing Assembly Exploded View task, step rows, distance/angle entries,
dragger and radial control retain their identities. Reopening a saved view edits
its native steps; Accept restores the assembly's modeled placements and saves
steps separately, while Cancel restores the previous transaction state.

For the validated solid-occurrence workflow, TechDraw uses the saved exploded
view as its explicit Source. Its geometry preserves each occurrence's existing
source-placement policy and enclosing structural transforms. Trails follow the
geometry through successive steps, including rotation and radial movement.
Missing move references raise an output error rather than silently omitting a
step. Native visibility filtering still controls which parts enter the drawing.

No new animation or configuration controls are introduced. Nested parent/child
step combinations, scaled/array/external links, broader visibility, joint limits,
BOM arrangement selection and physical owner acceptance remain open.
[Owner procedure](../tests/ExplodedViewOutput.md).

## UI-035: Reviewed intersection curves (F069; roadmap 13.4a/b)

Part > Review intersection curves opens a modeless review of two whole root Part
shapes/whole root Bodies, with up to 200 faces each. The original Section command
and native Part::Section/Base/Tool/Approximation identities remain unchanged.

| Control/state | Behavior |
| --- | --- |
| Capture first / second shape | Capture one whole tree selection from the active document, showing label and internal name. Two valid preselected objects initialize the roles. Nested members, Links and subelements are refused. |
| Approximate output curves | Native Section option, initially off. Changing it clears the previous preview. |
| Preview curves | Run native Section on copied BReps in a hidden temporary document. Show a temporary non-pickable wire, edge count and total millimeter length; no source transaction or geometry changes. |
| Empty or point-only result | Explain zero curves and isolated vertex count; disable creation. Coincident surfaces may yield boundary edges and require review. |
| Changed/unavailable input | Remove the old overlay and disable creation. Changed inputs require explicit recapture; edit/transaction/document context must be valid. |
| Create intersection | Recheck the inputs/result, then create one native associative Section transaction. Preserve source visibility and Body Tips; failed creation rolls back. Close after success. |
| Cancel / close document | Remove the temporary overlay and observer; leave no created feature. |

This review does not project curves, cut material or create clipping planes.
Individual-face extraction, nested/external scope, broad topology repair and
physical/high-DPI acceptance remain open. [Owner procedure](../tests/SectionReview.md).

## UI-036: CAM Simulator input review (F095; roadmap 14.3a/b)

Existing CAM Simulator (CAM_SimulatorGL) retains its job, operation, visibility and
quality controls. The Legacy CAM Simulator is unchanged.

| Control/state | Behavior |
| --- | --- |
| Review text | Read-only stock dimensions in mm, quality level, selected operations in saved job order, command counts and cutter number/diameter. Quality is a display setting, not a certified tolerance. |
| Job, operation checks, visibility policy, quality | Rebuild the review using the current choices. No selected operations disables Play. |
| Review inputs | Revalidate current stock/model, paths and cutter profiles. Show the first preparation error inline, disabling Play. |
| Play | Prepare the complete selected input set before resetting the native session. Submit each cutter selection before its operation's placed commands. Changed/unreviewed inputs show updated review and require another Play. |
| Model/tool/path edit | Clear the review and disable Play; ask for recompute as needed and renewed review. A previously opened simulator view is a snapshot of its submitted inputs. |
| Close | Remove the task's observer; native simulator view lifecycle remains native. |

Visible scope text identifies pre-postprocessor job paths and cutter profiles.
This review does not check holder, fixture or machine-envelope clearance, certify
stock removal accuracy or establish safe machine motion. Full collision/removal,
broader command/model scope and physical acceptance remain open.
[Owner procedure](../tests/SimulationReview.md).

## UI-037: Sketch freedom guidance (F047; roadmap 11.4c/d)

The existing Sketch Edit solver task retains its native status, diagnostic links,
geometry colors and update/settings controls. A word-wrapped text explanation and
**Select unconstrained geometry** button supplement those controls.

| State/control | Behavior |
| --- | --- |
| Underconstrained | Explain that geometry may move or change size, freedoms can be coupled, and construction geometry can retain freedom. Enable selection. |
| Fully constrained | Explain dimensions/relations/fixed or Block geometry and that reference dimensions do not remove freedom. Disable selection. |
| Conflict, redundancy, malformed or failed solve | Ask for resolution of the native solver issue before interpreting movement. Disable selection; keep native diagnostic links. |
| Empty sketch | Ask for geometry; disable selection. |
| Select unconstrained geometry | Replace selection using the existing solver-driven native command. No geometry, constraint or placement edits; recheck solver validity at activation. |

The button supports normal Qt keyboard focus and a tooltip explains its selection
replacement behavior. Native solve updates refresh both controls. Count and selected
entities do not assert independent movement directions. [Owner procedure](../tests/SketchFreedom.md).

## UI-038: Associative dimension repair (F103; roadmap 15.3c/d)

The existing TechDraw_DimensionRepair command, dimension identity, reference
properties and native geometry validators remain authoritative.

| Control/state | Behavior |
| --- | --- |
| Name, label and reference collections | Read-only review of the existing dimension, then the proposed owner view and geometry after Replace References With Selection. |
| Replace References With Selection | Collect native drawing/model references without changing the dimension. Explain projected 2D or true 3D mode and that drawing measurements do not drive the model. |
| OK without reviewed geometry | Stay open and ask for Replace References With Selection. |
| OK with replacement | Validate compatible reference form/current geometry and recompute in one transaction. Projected replacement clears old 3D references and measurements. |
| Failed repair | Abort that transaction, restore original references and remain open with an inline explanation for correction. |
| Another edit transaction | Preserve the owner's edit and ask for its completion before repair. |
| Cancel | Discard the proposed reference collection without changing the dimension or undo history. |

Native owner-view-change confirmation and selection errors remain in place.
Review is a reference list, not a graphical preview. Broader topology repair,
hole/thread annotations, full type coverage and physical acceptance remain open.
[Owner procedure](../tests/DimensionRepair.md).

## UI-039: Assembly freedom guidance (F077; roadmap 12.4a/b)

The existing assembly-edit Solver messages panel retains solver-state labels,
conflict/malformed navigation and native solver ownership. A word-wrapped plain
text explanation and two keyboard-focusable buttons supplement that status.

| State/control | Behavior |
| --- | --- |
| Underconstrained | Explain assembly-wide count and that connected sliders/hinges can still move. Enable unconnected selection. |
| Fully constrained | Explain the successful zero-freedom solve and distinguish grounding from ordinary joints. Disable unconnected selection. |
| Failed/conflicting/malformed solve | Explain that freedom is not established. Disable unconnected selection; retain native diagnostic links. |
| Empty | Ask for components and grounding; disable both buttons. |
| Select grounded components | Replace selection using the native grounding set filtered to assembly components, including native read-only/rigid-group rules. |
| Select unconnected components / DoF link | Replace selection with components without a joint path to ground. Recheck successful current solve; this does not identify every movable component. |
| Stale or invalid assembly/component | Preserve selection and ask for recompute/reference resolution. |

The contextual panel is visible without a task dialog, persists across dialog
open/close and follows its owning document. Both buttons preserve geometry,
placements and joints. Grounded selection states
a relationship, not solve success. Movement arrows, per-component rank, detailed
incomplete-joint/unresolved external/nested loading states and physical acceptance remain open.
[Owner procedure](../tests/AssemblyFreedom.md).

## UI-040: Ordered Loft section collection (F063; roadmap 13.2a/b)

The existing Part_Loft command and ActionSelector retain their identities. Native
Part::Loft owns Sections, Solid, Ruled and Closed persistence and geometry.

| Control/state | Behavior |
| --- | --- |
| Available profiles | Include a single wire (open or closed), single edge or vertex; keep native single-wire face support. Tooltips distinguish duplicate labels by internal name. |
| Sections in loft order | Top-to-bottom is the committed Sections sequence. Existing add/remove and Move up/down controls update the section count. |
| Create solid | Require a valid result containing one solid. Uncheck for a surface through open or closed sections. |
| Ruled surface | Explain joins between adjacent sections versus smooth interpolation. |
| Closed | Connect last section back to first; explicitly distinguish this from capping an open profile. |
| Review text | Show section count, order, output/connection modes and separate associative result. No geometric preview is claimed. |
| OK | Recheck section identity/readiness and edit context. Recompute and validate before committing one undo transaction. |
| Failed OK | Roll back creation, retain the task and show an inline correction message. |
| Cancel / document close | Create nothing; native task closes with its document. |

Guide curves, explicit correspondence, section reversal, twist preview, continuity
certification and Boolean targets remain open. [Owner procedure](../tests/LoftSections.md).

## UI-041: CAM model setup review (F090; roadmap 14.1c/d)

Native New Job and existing-job Model Selection keep their command and document
identities. Candidate selection uses document/object identity rather than display
labels. Duplicate-label candidates show internal names in tooltips. Repeated
sources retain their counts when reopening Model Selection. Meshes have a separate
group alongside Solids, 2D and Jobs; selected jobs expand to their model resources.

The read-only Model review lists source labels/internal names, type, count,
axis-aligned dimensions and minimum coordinates in mm including source placement,
before job setup. It does not claim enclosing-parent/world or final WCS bounds.
Document unit selection changes display rather than scaling geometry; STL source
units must be checked against the displayed dimensions. Native Job setup remains
the place to review orientation/work origin, stock, tools, strategy and post.

Count/selection and unit-display changes refresh review. Empty selection, empty
geometry, stale/invalid dependencies, replaced/deleted sources or changed document
context prevent acceptance. OK rechecks geometry and requires renewed review if
it changed since the displayed review. Template and model eligibility both gate
OK. Cancel creates nothing and does not apply the unit choice. Mesh/solid topology
repair, automatic unit conversion, final WCS preview and a complete step-by-step
strategy wizard remain open. [Owner procedure](../tests/JobModelReview.md).

## UI-042: Native state columns (F013; roadmap 10.6d/e)

Tools > Find and describe features keeps its existing document scope, metadata
editor, 2000-object limit and explicit selection action. Additional read-only
columns show native visibility flags, supported Boolean suppression, native error/
recompute state, immediate loaded source identity/file and metadata access.
The Columns menu changes presentation for this dialog; choices survive Refresh.
State filtering combines with the existing type and text filters. Sorting and
inspection do not change geometry, visibility, suppression or history order.

A selected row exposes the full native status/state and source path below the list.
Unresolved links remain explicit; inspection never requests loading. Visible/hidden
flags do not describe effective ancestor visibility. No native error is a native
status report, not geometry certification. Metadata access refers to Label/Label2,
not an operating-system file permission test. Read-only metadata disables Apply.

Relevant object/property, view visibility, recompute, Undo/Redo, save and immediate
loaded external-source changes invalidate the snapshot and clear rows until
Refresh. Closing detaches both application and GUI observers; closing the owner
document closes the dialog. Nested/external link chains, unloaded-state diagnosis,
reference sets, integrated navigator tabs, global column preferences and display/
suppression toggles remain open. [Owner procedure](../tests/FeatureStateColumns.md).

## UI-043: Explicit Sweep inputs (F028; roadmap 13.2c/d)

The native Part_Sweep command retains its profile list and Part::Sweep properties.
Sections in sweep order identifies the top-to-bottom sequence; candidate tooltips
include internal names. Sweep Path enters edge selection; Done captures one whole
edge/wire or connected edges of one object in the owning document. The path label
shows the captured document/object and selected edges. Later profile/global
selection does not replace this choice. Starting path capture clears the old choice;
invalid completion leaves no captured path and shows inline guidance.

Review text explains section count, solid/surface output and native Frenet/corrected
frame choice. No geometric orientation/twist preview or Boolean target is claimed.
OK rechecks document/edit context, object identities, current inputs, connected path
and distinct profile/path roles. Recompute and valid-shape/one-solid checks precede
transaction commit. Path validation and native Sweep construction deep-copy source
geometry with element mappings intact. Failed creation rolls back and stays open
for correction. Cancel works during path capture and removes the selection gate; document closure
closes the task. Native Sections/Spine/Solid/Frenet persistence is unchanged.
[Owner procedure](../tests/SweepInputs.md).

## UI-044: Saved project packaging (F108; roadmap 15.6a/b)

Tools > Package saved project reviews the active document's saved FCStd and
recursive serialized relative XLinks, including unopened source documents. The
read-only table shows original paths, portable package paths and byte counts.
Review never loads, saves, recomputes or redirects a document. Missing/inaccessible
files, unsupported archives, dirty/pending/invalid loaded documents, absolute
links, external PropertyFile/PropertyPath assets and Python feature code block
creation with explicit guidance. Embedded archive assets remain in the native files.

Refresh review replaces the snapshot. Choose ZIP selects a new destination;
Create package rechecks the exact saved sources, copies native bytes and relative
directory layout, writes a hashed portable manifest, verifies copied bytes and
publishes only the completed ZIP. Existing destinations are refused. Failure leaves
originals unchanged, removes the temporary package and keeps the dialog usable.
Success explains extraction and the root file to open. Close cancels without
model mutation; closing the root document closes the dialog.

The package is a file copy with native identities preserved, not Make Unique.
Close originals before opening the extracted project. Absolute-link repair,
external file asset/code collection, independent duplication and general format
migration remain open. Unsupported atomic-publication filesystems fail explicitly.
[Owner procedure](../tests/ProjectPackage.md).

## UI-045: Hole specification review (F055; roadmap 13.5c/d)

The existing Part Design Hole task identifies the location profile and owning Body
by document, internal name and label. It reports the native processed-location
count only for a current valid feature, explicitly separate from the number of
cuts that intersect the target. Failed features show the native error; deferred or
touched previews show pending state. A restored feature without a location cache
reports that the count is unavailable until recompute. Review does not recompute.

The thread summary follows saved native properties and current standard/size
controls: clearance diameter, tap-drill preparation, cosmetic visual/specification
without exported helical geometry, or actual modeled thread with recompute cost.
No standard means a plain hole diameter. Native tables and feature properties
remain unchanged; drawing callouts are not certified by this review. Model edits,
profile changes and native preview updates refresh the review after the event loop.
Native acceptance/Cancel/Undo and the existing Update View control retain ownership.
Broader placement collection, table version/provenance and drawing-callout acceptance
remain open. [Owner procedure](../tests/HoleSpecification.md).

## UI-046: Entity selection filters (F035; roadmap 10.5e/f)

View > Visibility > Selection filters opens a modeless window. The selectable
entities combo chooses All entities, Vertices only, Edges only, Faces only or
Whole objects only. Whole objects groups components, bodies, sketches and features;
no separate subtype selectors are claimed. The policy restricts subsequent native
selection/preselection and Select Other candidates without clearing existing picks.
Resolved native element names classify linked/nested occurrence paths. Command-owned
gates independently refine this policy; no gate is replaced, removed or restored by
the panel. A command ending leaves the selected session policy in effect.

An active status-bar button names the filter and resets it in one click. Reset to
all, Close and Escape restore All entities; application startup also resets the
policy. The window remains available during native task commands. Rejected picks
show native filter guidance; an empty Select Other result uses its existing filter
explanation. No model properties, geometry, visibility, transactions or persistent
reference identities change. Existing selections may include other entity types.

Dedicated sketch-edit, tree/window policies, separate object categories, multiple
filter combinations and physical/high-DPI acceptance remain open.
[Owner procedure](../tests/EntitySelectionFilter.md).

## UI-047: Fillet/chamfer failure recovery (F058; roadmap 13.5e/f)

The existing Part Fillet and Chamfer tasks retain their source dropdown, checked
edge/face collector, constant/variable radius and equal/two-distance controls.
An inline status explains that OK checks the result before committing. Empty
selection and nonpositive/nonfinite sizes are refused before a transaction. A
changed/touched/invalid source requires recompute and a fresh edge review; the
active document must own the selected source.

Native recompute and shape validity precede commit and source hiding. Failure
rolls back model changes and leaves the task and checked edges/sizes available.
The message names the attempted edge set, suggests reducing sizes/removing edges,
and includes the native error; it does not claim the kernel identified one failing
edge. Existing-feature edits retain prior parameters and geometry after failure.
Inputs are copied with native element mappings before kernel construction.
Accepted features retain native Base/Edges/EdgeLinks and downstream semantics.

No new live preview, tangent-chain collector, corner option or exact failure-region
classifier is claimed. Broader topology and physical/high-DPI acceptance remain open.
[Owner procedure](../tests/EdgeTreatmentRecovery.md).

## UI-048: Sketch Trim gestures (F050; roadmap 11.6e/f)

The existing Sketcher Trim tool retains its boundary markers and Include axes
control. Pressing and dragging applies native trims in one gesture transaction;
release commits it as one Undo step. An empty gesture creates no transaction.
A consumed pick is cleared so release cannot apply the same pick again. Escape,
right-click or leaving edit cancels unfinished work; completed gestures remain.
A trim exception aborts the current gesture and reports failure.

The existing tool notice shows progress and the release/Cancel rule, then completed
trim count and constraint identifiers supplied by native removal notifications. The notice says
removed or replaced because a native operation can retain a name on a new identity;
it wraps within the task pane.
No heuristic comparison or silent constraint reconstruction is introduced. Native
trim semantics own retained/remapped constraints and construction geometry.
New geometric previews and extension guidance remain open.
[Owner procedure](../tests/TrimGesture.md).

## UI-049: Shell Thickness (F059; roadmap 13.5g/h)

The existing Part Thickness task shows its source identity and removed face names.
The native collector starts with the saved faces selected; Done applies the current
selection, including an explicitly empty set for a closed thick solid. Face names
remain native references, without inferred replacement after ambiguous topology edits.

Signed thickness follows the native convention: positive outward and negative inward
for an outward-oriented solid. Reverse side changes the sign unless an expression
controls the value. Update view controls recomputation; the task distinguishes current,
pending and failed output, and identifies potentially cached geometry after failure.

OK recomputes and requires one valid solid before finishing the native transaction.
A failed attempt retains the feature and settings for correction. Cancel owns rollback
for both new and existing features. No new localized failure preview is claimed.
[Owner procedure](../tests/ShellThickness.md).

## UI-050: Window and crossing selection (F039; roadmap 10.5g/h)

Native 3D box selection uses left-to-right full enclosure with a solid border and
right-to-left crossing with a dashed border. The style updates if the drag crosses
its starting point. Command tooltips explain the directions, Ctrl-add and Escape.
Both explicit box commands and supported delayed drag selection share the policy.
Generic rectangles and Box Zoom retain their existing styles and camera behavior.

Whole-object picking uses projected bounds; element picking uses native projected
tessellation. Visible objects may include occluded/back-facing geometry. Hidden
objects are excluded through the existing visibility traversal. Whole bounds do
not replace element requests, and entity filters intersect command gates before
choosing an eligible element category. Plain selection replaces; Ctrl adds.
[Owner procedure](../tests/WindowSelection.md).

## UI-051: Joint motion and limit review (F076; roadmap 12.4c/d)

The native Assembly joint task explains relative motion for Fixed, Revolute,
Cylindrical, Slider and Ball joints and directs users to the assembly solver for
combined restrictions. Reference-row tooltips expose document/component/subelement
identity without changing native connectors, placement or selection semantics.

Enabled supported limits must be finite and ordered minimum <= maximum. An inline
message identifies length or angle bounds and keeps the task open on failed OK.
Validation reads task inputs and evaluates expressions before the solver can swap
reversed bounds. Disabled/unsupported limits do not block; equal bounds are valid.
Correction, acceptance and Cancel reuse native transactions. Direct property-editor
and scripted solver normalization remain unchanged. No contextual suggestions or
new motion-envelope/conflict preview is claimed.
[Owner procedure](../tests/JointReview.md).

## UI-052: Reviewed face extension (F066; roadmap 13.1e/f)

The existing Surface Extend Face command opens a modeless review for one face on
a root Part shape or Body. It shows exact source identity, four independent U/V
side percentages, fitting tolerance in mm and sample counts. The explanation
distinguishes parameter spans from physical distances and explicitly discloses
rectangular B-spline approximation and loss of trimming loops/holes.

Preview uses a copied source and native feature in a hidden temporary document,
then a non-pickable boundary overlay. Changed inputs remove the preview and disable
Create; changed source geometry requires reselection. Failure retains settings
for correction. Create rechecks the current source and native result before one
transaction commits a separate associative feature. Cancel leaves no feature.
Source visibility is preserved. Existing feature edits use the native properties.
No true untrim, kept-region trim selection, maximum-deviation certification or
complete self-intersection diagnosis is claimed.
[Owner procedure](../tests/ExtendFaceReview.md).

## Models, Part Tree and History (roadmap 7.8)

Owner-approved behavior is in the [component document contract](architecture/COMPONENT_DOCUMENT_CONTRACT.md).
Use Models, Part Tree and History as the tab labels, in that order.
Models is flat/non-expandable and lists all owning-file definitions, including
unused definitions and referenced external models, with expanded assembly-instance
counts. The root is an editing model/context, with zero linked uses unless explicitly
instanced elsewhere. Selecting a model shows native attributes; Edit accesses the
same definition even with zero instances. Add Instance reuses it in the active model.
Replace the native Model pane with Attributes, retaining its View and Data tabs.
On application startup, show Components even with no document open. Dock it at
the top left above Attributes, using two thirds of the available dock-column
height for Components and one third for Attributes. Restore this initial layout
after native saved-state restoration, including previously hidden, floating or
tabbed panels. Users can resize the split afterward; document changes and panel
Show commands do not reset it.
With no document open, Tasks shows **New File** and **Open**, including when the
saved mode is outside Design. New File uses the native New command and enters
Design; its idle Tasks pane shows **New Sketch**, **Coordinate System**, **Datum
Plane** and **Add Component**, in that order. These use the existing native sketch,
datum and component workflows and share command enablement/icons. The buttons
use compact text beside icons. Native operation dialogs take over during editing;
the idle actions return after finishing or cancelling. Native task watchers remain
available for legacy documents and other modes with a document open.
At startup, the central viewing area shows the upstream native Start page's
Recent Files cards. Hide its New File heading/creation row, example files,
custom-folder cards and setup/startup footer, and show the Documents page rather
than the first-start setup. New File/Open remain in Tasks. Preserve native recent
ordering, thumbnails/file metadata and card-click opening. An empty list shows
"No recent files." Do not take focus from a document opened by startup arguments.
This page requires the native Start module (`BUILD_START=ON`).
Keep the native status-bar Notifications (icon/unread count), Navigation Styles
and Dimension/Unit System menus visible by default. Restore the upstream Tux
navigation indicator (`BUILD_TUX=ON`), retaining its icon, style choices, tooltips
and native viewer behavior. Seed Blender navigation and Imperial Decimal (in, lb)
units before module initialization when no preference is saved. Preserve explicit
saved choices and document unit overrides. Units changes keep their native scope:
global without a document, the active document with one open. The native Blender
fallback also applies to navigation preference resets.
Add Reference Object is a modeling operation button beside Extrude in Part Design
and Part; omit its creation action from Part Tree and History context menus.
Existing reference repair/change-source actions remain available. The operation
uses the active component, supports direct-child preselection and cancellation,
and is unavailable during another task.
On entry to a component, its Origin eye in History defaults to visible. A manual
hide persists through refresh; re-entering the component restores the default.
Origin contains an Origin Planes child item for XY, XZ and YZ planes together.
The planes start hidden on component entry. Their eye/context Show/Hide control
is independent of the Origin eye; showing planes also shows the parent Origin.
Refresh preserves a manual show, and visibility changes support Undo/Redo.
Neither Origin nor Origin Planes can be suppressed, renamed or deleted. Standard
Delete also protects their native datum objects; no extra model object is created.
Part Tree always starts with its top-level component (Part001 by default),
with linked occurrence rows beneath it. The root row supplies selection/edit
context, persists even without children, and is not a deletable assembly instance.
Cut/Paste is available in Part Tree's context menu and through Ctrl+X/Ctrl+V.
Cut keeps the instances in place until Paste succeeds; Paste moves them under the
selected part. Drag onto a part to make it the parent, or use the row-edge indicator
to insert above/below a sibling. Empty-space drops append at the root. Multiple
selected rows and collapsed instance groups move together without making copies.
Expand a grouped destination to choose one occurrence. Part001 cannot be moved.
Moves preserve the selected occurrence's placement and are undoable. Child-list
edits of a shared model affect all its uses. Cross-file moves and unsafe reparenting
of referenced, constrained, driven/scaled or path-overridden instances are refused
with repair guidance; sibling reordering remains available for references/overrides.
Delete Instance/Instances, Delete key and standard occurrence Delete remove owning
links only. Definitions and their geometry remain under Models, including after
the last instance is removed. Missing instance references require repair; Undo
restores identities. The shared-parent child ownership contract still applies.
Add Component
adds a child instance to the active component; Add Reference Object selects evaluated
geometry from a direct child only. Full Component / Bodies Only / Hidden and Reset
to Inherited control occurrence-path representation. No Reference Only role is added.
Convert to Dumb Object offers Delete Parameters and Extract Dumb Body. Component
edit tabs identify the shared definition and owning file; they do not make copies.
Definition-owned constraints remain in History, outside occurrence rows.
Entry points are File > New/Open and Tools > Components. The panel shows
only the edited component name, without a file path or creation buttons. Right-click
provides Edit first and Add Component; Add Reference Object is an operation
button. Double-click edits the shared definition. Root editing is available in
Models and through the first Part Tree row. Instances contains Add
Instance and Copy to New Part; Part View contains the three display types and Reset
to Inherited. Save to External File replaces the earlier Externalize wording.
Missing components offer Locate Component File and legacy conversions expose their
report. Attributes and these projections share native document objects; complete
native command/edit/picking parity remains an explicit roadmap gate.

Part Tree's first column shows part names, with a visibility control,
instance count and Part View columns. Same-definition instances under a parent
start grouped (x5); Expand Instances reveals support_angle#001 through #005, and
Collapse Instances regroups them. The active part is highlighted and cannot be
hidden, including by hiding its parent branch. History places the active /
suppressed checkbox to the left of the visibility icon and item name. Partial
checks identify dependent inactivity; visibility does not suppress an item.

Component feedback tasks (7.8.5c/d and 7.8.7d/e):

New component documents use the default title/file basename untitled001; further
open documents reserve names case-insensitively and use untitled002, etc. Save As
therefore suggests untitled001.cadprt for the first new document. Explicitly named
documents and existing saved files retain their names; the root component's label
remains separate from the document filename.
The automatically created root part is Part001. New embedded part/component
definitions use the next available Part002, Part003, etc., across the document,
including nested additions. Add Component pre-fills that name and allows custom
names. Reusing a definition adds an occurrence with the definition's label and
does not consume another part number. Preserve existing/custom names and native
component identities; these names do not change the component's part/assembly role.

Extrude/Pad/Pocket in a component
context opens an operation-first task with New Body/Add/Subtract, local profile,
explicit target, length, reverse direction and Preview. OK commits one operation;
the component task also restores native extrusion extent controls: One dimension,
Two dimensions or Symmetric (total length, half each side); per-side Dimension,
To first, To last, Up to surface, Up to shape or Through all; second-side length,
limiting reference, signed end Offset and taper. Start offers Profile plane,
Offset or Reference with a signed start offset. Custom direction accepts a numeric
vector and Length along sketch normal; Refine result remains available. To first/
last/Through all need an explicit target body. Whole multi-face shape limits need
zero end offset; use one limiting face for an end offset. Pick/Clear and typed
native object/face names collect local start/limit references without changing the
profile list. Second-side fields appear only for Two dimensions. Automatic preview
can be switched off; Preview remains available. Added volume is filled green,
removed volume filled red; target transparency is temporary and returns when the
preview clears or the task ends. The restored native options use the existing
geometry engine without creating a Part Design Body container.
for a sketch profile, Selected curves lists each collected curve. Add selected
curves supports viewport/native multi-selection from that sketch; Remove, Clear
and Use all revise the list. The first explicit curve/region pick replaces the
default whole-sketch selection; subsequent picks add curves without duplicates.
Pick closed regions in the view collects the clicked region's outer contour and
immediate hole contours, including Sketcher's filled internal-face hits. Preview
and OK require one connected region with optional holes; open/self-intersecting,
touching/crossing contours and disconnected regions receive inline rejection.
The chosen sketch is temporarily visible for picking and prior visibility returns
on Cancel; successful OK hides the consumed sketch. Edits restore the saved subset.
Cancel leaves no provisional document objects. Editing a published result opens its
producer. Mode and target can change while preserving the published result identity;
unsupported direct operation consumers or expressions require explicit review.
New Sketch from Part Design or Sketcher temporarily shows the active component's
native XY/XZ/YZ origin planes and their labels in the owning-file view. Clicking
one selects its orientation in the task; the plane dropdown and selected local
planar face plus offset remain available. OK/Cancel restore the previous origin
and datum visibility; OK opens native Sketcher after the creation task closes,
without a close-task confirmation or requiring a Body. History
also uses native object editors and offers Rename and Convert to Dumb Object.
History displays every component's origin as Origin. Newly created default
labels use a component-local sequence starting at Sketch001, Body001, Extrude001,
etc.; other components may show the same labels. Custom labels are preserved.
Generated Body results are background objects: omit their rows from native Model
and History, and show the producing Extrude as the public solid. Its eye and
native visibility control display; geometry picks retain the internal result for
engineering references. Delete Extrude removes its unused result; one Undo restores
both. Internal results cannot be deleted separately. Convert to Dumb Object remains
available on Extrude; Delete Parameters exposes the retained independent Body.
Refresh retains row selection, expansion and scroll position. Broader acceptance
and owner feedback remain pending.

Component selection/context iteration (7.8.7f): selecting a Component Structure
row sends the full native occurrence path to the shared selection/property system;
a grouped row selects its represented instances. A native tree or 3D pick selects
matching rows without changing the active definition. A precise nested pick reveals
the required grouped instances; an ambiguous bare shared definition never chooses
an arbitrary path. History selection uses the active occurrence context.

Add Reference Object uses an unambiguous selected direct-child object as its initial
choice. Selecting a face/edge identifies that whole evaluated object, as the dialog
states. Ambiguous, unrelated or grandchild selections require an explicit choice.
Grouped Part View changes and show/reset fallback use one Undo transaction. Opening
an already-open isolated component focuses its existing tab; switching views restores
the stored active component and occurrence path. These are bounded native-integration
steps; complete picking/editor/consumer parity remains in roadmap 7.8.7b.

Reference recovery feedback (7.8.4a): History Edit/double-click on a reference
opens its direct-child source review. The context action says Repair Reference Object
for a broken source and Change Reference Source otherwise. The picker states that
it references whole evaluated geometry. Repair preserves identity and history order;
unsupported geometry-kind, face/edge or expression remapping is refused before commit.
A repair notice and state tooltip identify unavailable references. Their visibility
icon indicates unavailable geometry. Refresh References updates pending snapshots
without closing the component or blocking independent work on other inputs.
