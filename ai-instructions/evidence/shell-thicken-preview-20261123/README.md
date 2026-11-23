# Shell and Thicken preview — November 23, 2026

Owner requested renaming Thickness to Shell, a separate Thicken feature for sheets
and a fix for invalid input leaving an operation stuck. Owner clarified Thicken
must have New/Add/Subtract, like Extrude and Revolve. This is a native UI proposal;
production implementation/install await approval. No approval state was changed.
The later [combined Surface-in-Modeling preview](../surface-modeling-preview-20261123/README.md)
supersedes this placement: Thicken belongs in Modeling's new Surface section,
the six existing Surface tools move there, and the Surface tab is removed.

Direct screenshots:
- [Shell task rename](shell-task.png), retaining native hollow-solid parameters.
- [Thicken / New](thicken-new.png), [symmetric total thickness](thicken-symmetric.png).
- [Add with target cue](thicken-add-target.png).
- [Invalid Shell selection](shell-invalid.png), [invalid Thicken selection](thicken-invalid.png).
- [Ribbon placement](ribbon.png), [native thickened-sheet illustration](thicken-illustration.png).
- [Existing Thickness panel](before-task.png).

## Proposed behavior

Shell replaces the visible command/task name Thickness; the wall-thickness field
remains Thickness. Keep native solid hollowing and saved PartDesign::Thickness
identities/parameters. New feature labels use Shell; do not rewrite owner labels
of existing saved objects. Thicken uses the existing native Offset icon. Its
original Dress-Up placement is superseded by the owner's later direction to
place it in Modeling's new Surface section; Shell stays in Dress-Up.

Thicken selects one owned sheet or connected faces from one sheet, with a scrolling
five-row collector, Remove/Clear, positive Total thickness (initially 1 mm), and
Along normal/Opposite normal/Symmetric direction. Symmetric uses half of the total
on each side. Advanced corner join offers Sharp/Rounded. New creates a solid;
Add/Subtract require a current target solid and reuse sole-target selection,
highlighted missing-target cue, selected-target visibility/material behavior and
valid/invalid preview colors (Add green/yellow, Subtract red/pink). Target selection
comes before collecting sheets for Add/Subtract. Source/target ownership, strict
sequential dependencies, automatic History tab and restoration, usable tree eyes,
numeric blur/immediate arrows and shared creation/edit/cancel apply as elsewhere.
New/add/sub outputs must be one valid solid; failed offset/boolean operations
show prominent errors and cannot be accepted. Save the source references, thickness,
direction, join and operation, preserve identity on edit and recompute associations.
No user-facing Body-creation step. Existing Extrude/Revolve behavior stays intact.

Shell rejects sheets before creating a feature or opening a transaction, with a
highlighted message directing the user to Thicken. Thicken rejects solids as source
geometry with a corresponding Shell suggestion. The native command path must also
clean up a failed entry if task construction/setEdit throws: no dangling feature,
pending transaction, edit mode or visibility loss. Keep recoverable calculation
errors inside an already-open valid task editable; do not indiscriminately abort
all failed previews or unrelated pre-existing transactions. Check menu, toolbar,
command and edit entry paths, including Classic/native access.

## Evidence and implementation boundary

Installed 7adf23f3b2 reproduces the defect for Extrude sheet face, Revolve sheet face
and whole sheet selection. Each creates an invalid Thickness with "Base feature's
shape is not a solid", no task/edit dialog and a pending transaction. Valid solid
face selection opens the native task. Normal Undo removes only the failed Thickness,
restores the original sheet visibility and clears the transaction in all three
cases. See stuck-operation-reproduction.json; owner documents were not touched.

Preview assertions verify New default, Add/Subtract target visibility and cue,
symmetric meaning, native Shell title rename and clean prototype cancellation.
Thicken OK is disabled: this UI does not create saved production Thicken features.
A separate native filled-offset fixture thickens a 270-degree cylindrical sheet
by 1 mm into one valid solid (742.201264 mm³). Its screenshot illustrates the kernel
capability; persistence, boolean operations and live task wiring remain unimplemented.
The invalid Shell dialog is a UI prototype; the command preflight/rollback fix
still requires implementation and regression checks after approval.

Companion session 4ceae9ed5cc9 uses adapter baseline
dfbae579efaf14186f7a1840925398e5529e5acb against installed 7adf23f3b2.
Only shell_thicken_ui.py changes in the candidate. Final fingerprint
f4059258dcca41a7d974c793faebb936ee2a22a76049d447338bd8db9a45f096;
capture fresh, no scope violations. Isolated profiles and synthetic documents
only; generated runtime fixtures removed after archival. Source/captures remain
available for review. Unrelated project.previewfirst.json is preserved.
