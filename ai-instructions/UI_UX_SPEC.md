# FreeCAD Plus: UI and UX Specification

## Interface scope

This document specifies the fork's Pad task-pane changes and the planned shared
Add/Subtract interaction. The inherited desktop
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
one geometry command and one create/edit task. Geometry selections remain the first
section; an Operation control with **Add** and **Subtract** follows, before shared
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
| UI-001 | Pad task pane | Select the profile and configure a new or existing Pad | `PartDesign_Pad`; Edit Pad / feature edit | [UI-001](#ui-001-pad-task-pane) |

## Screen specifications

### UI-001: Pad task pane

- Purpose: satisfy REQ-001 through REQ-007 in [the product specification](PRODUCT_SPEC.md#capabilities-and-requirements).
- Entry: invoke Pad with an active body, with or without preselection; or edit an
  existing Pad. The normal body prerequisite remains in force.
- Exit: OK accepts a valid result; Cancel abandons the transaction. Empty and
  invalid profiles retain the dialog so the user can correct them.
- Layout: Profile is the first section inside Pad Parameters, followed by the
  existing extrusion parameters and preview controls in the task pane.
- Data: show the source label and selected edge/face names, or a whole-profile
  entry. Refresh from `Profile`; geometry and feature status drive preview/errors.

| Control | Placement | Action | Availability and validation | Result/feedback |
| --- | --- | --- | --- | --- |
| Profile list | First section | Select one or more rows for removal | Populated from one source object and optional subelements | Shows accumulated geometry; ordinary viewport clicks do not discard previous rows. |
| Select / Done | Below profile list | Enter/exit geometry selection | A new empty Pad enters selection automatically | Model/tree selections update the profile; other selectors are deselected. |
| Remove | Below profile list | Remove highlighted entries | Enabled only when list entries are selected | Remaining entries are retained; removing the last leaves an empty profile. |
| Clear | Below profile list | Remove the source and all entries; begin selection | Enabled when a source is assigned | A different source can now be selected. |
| Profile hint | Above list | Explain empty, invalid, or incompatible selection | Always visible | Empty-state instructions; geometry errors; explanation when another source is picked without clearing. |
| Start / Offset / Pick Reference | Existing parameter area | Choose profile plane, offset, or referenced start | Offset/reference fields follow the selected start mode | Retain inherited start and reference-picking behavior. |
| Direction, Reversed, custom X/Y/Z, Length along sketch normal | Existing direction controls | Set extrusion direction and length interpretation | Normal/reference/custom mode governs available fields | Changing the profile refreshes direction choices; explicit custom choices remain model-owned. |
| One sided / Two sided / Symmetric | Existing side mode | Choose extent arrangement | Side 2 controls appear when applicable | Retain inherited one/two/symmetric behavior. |
| Type, Length, end reference, Offset, Taper angle | Per-side parameter controls | Set dimension or limiting geometry and taper | Dimension, To last, To first, Up to face, Up to shape expose their applicable inputs | Existing geometric validation and preview remain authoritative. |
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

## Open questions

The next operation and multi-source profile behavior are [product questions](PRODUCT_SPEC.md#open-questions).
Record any visual or interaction defects found by GUI validation against UI-001
and the active roadmap milestone; do not silently change the intended workflow.
