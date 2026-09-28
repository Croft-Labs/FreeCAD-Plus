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

## Scope and non-goals

The current change unifies Pad and Pocket as Extrude in the Part Design workbench.
The broader direction is
complete task-pane workflows for operations such as revolve and patterns; these
remain future work. The preferred direction is one command per geometry operation,
with Add/Subtract chosen inside its shared create/edit task, following the workflow
described by the user. The [candidate inventory](DEVELOPMENT_ROADMAP.md#unified-feature-workflows)
defines the planned families; it does not establish implemented behavior.
Application-wide rebranding, changing the geometry kernel,
multi-object profile aggregation, modifying the installed FreeCAD, and release
packaging are outside the current implementation scope.

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

## Open questions

- Which unified family follows Extrude? See roadmap milestone 3.6.
- Is multi-object profile aggregation desired later? It requires a separate
  model/compatibility decision; it is not implied by curve selection within one source.
