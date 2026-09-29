# FreeCAD Plus: UI and UX Specification

## Interface scope

This document specifies the fork's unified Extrude and Pattern task panes and the
planned shared Add/Subtract interaction for other feature families. The inherited desktop
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
other operation modes is a separate scope decision. These planned interactions satisfy
REQ-008/009; implementation and acceptance are tracked in roadmap milestone 3.6.

## Screen index

| ID | Name | Purpose | Entry point | Specification |
| --- | --- | --- | --- | --- |
| UI-001 | Extrude task pane | Choose Add/Subtract and configure a new or existing extrusion | `PartDesign_Extrude`; legacy Pad/Pocket commands; Edit Extrude | [UI-001](#ui-001-pad-task-pane) |
| UI-002 | Pattern task pane | Choose Linear/Circular, features, and repetition parameters | `PartDesign_Pattern`; Edit Pattern | [UI-002](#ui-002-pattern-task-pane) |

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

## Open questions

Further unified families and multi-source profile behavior are [product questions](PRODUCT_SPEC.md#open-questions).
Record any visual or interaction defects found by GUI validation against UI-001
and the active roadmap milestone; do not silently change the intended workflow.
