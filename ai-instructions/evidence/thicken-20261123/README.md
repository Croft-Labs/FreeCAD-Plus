# Shell, Thicken and Modeling Surface section — November 23, 2026

The owner approved the combined native preview in chat: **"approved, implement"**.
The [task specification](../../ui-ux-specs/TASK_PANEL.md#shell-and-thicken--november-23-2026)
owns approval provenance and the [Surface preview](../surface-modeling-preview-20261123/README.md)
owns the reviewed layout. Production implementation follows that scope.

## Implementation

- Modeling now has Surface between Dress-Up and Transformation: Thicken plus all
  six native Surface actions. Plus no longer has a Surface tab or duplicate mode;
  former Surface navigation maps to Modeling. Native Surface/Classic access remains.
- PartDesign Thickness is presented as Shell in its command, task heading, context
  action and newly created feature label. `PartDesign_Thickness`, native feature
  type/properties, existing feature identities and owner labels remain unchanged.
- Shell rejects sheets before creating a feature/transaction, with prominent amber
  guidance toward Thicken. Failed initial native editor entry aborts its transaction;
  an unrelated pending operation is rejected before starting. Recoverable errors in
  an already-open native Shell task retain the native workflow.
- Thicken accepts one owned sheet or connected faces from one sheet. New/Add/Subtract,
  positive total thickness, Along/Opposite normal/Symmetric and Sharp/Rounded joins
  use the native filled-offset kernel. Symmetric uses half the thickness on each side.
  Disconnected sheets, solid donors, edges/vertices and invalid offsets are rejected.
  Boolean output must be one valid solid and must add/remove material.
- The common task lifecycle supplies five-row scrolling selections, explicit/sole
  targets, hidden-target selected display, transparency and green/yellow Add or
  red/pink Subtract tools, History switching/restoration, eye controls, deferred
  numeric typing, immediate arrows, read-only previews and clean Cancel.
- Native `FeatureAddSubPython` results store owned LinkSub references and hidden
  `Thicken_*` settings. Creation and editing share the task, preserve feature identity
  and use the common atomic Body/target service. Saved recompute validates ownership
  without requiring an active edit view. Input intake still checks occurrence access
  and strict predecessor ordering. Native topology mapping and Body transforms are reused.

## Validation

Validation is performed with synthetic documents and isolated profiles in the
established development runtime. Owner documents and settings are preserved.

The initial build found an incorrect native shape accessor; it was corrected.
Initial regression exposed an active-view dependency during saved recompute; stored
reference evaluation was separated from interactive intake. A native command fixture
needed an explicit active Body, and its prompt handling was bounded. The numeric
fixture now uses actual typing and focus leave, rather than directly calling a handler.
These were resolved before final acceptance.

The first installed broad suite passed all **106 checks** across Thicken, Extrude,
Revolve, visibility, task entry, Plane/Sketch placement and strict History. The final
Shell decline-entry safeguard has a separate focused regression. All **11 final
build checks** and **11 final installed checks** pass: **107 distinct cases overall**.
See [build results](build-focused.json), [installed broad results](installed-broad.json),
[final focused results](installed-focused.json), [native UI acceptance](installed.json),
[fresh-process recompute](reopen.json) and [existing shortcut](shortcut.json).

Eleven payload files were installed, including the native PartDesign GUI module;
[the manifest](install-manifest.json) records source/build/installed hashes and retained
rollback locations. Existing owner sessions were preserved. A new isolated app was
launched through the existing shortcut; older processes need restart to load changes.

Direct installed captures: [Modeling ribbon](modeling-ribbon.png),
[Thicken task](thicken-new-task.png), [symmetric](thicken-symmetric-task.png),
[Add valid](thicken-add-valid-window.png), [Add invalid](thicken-add-invalid-window.png),
[Subtract valid](thicken-subtract-valid-window.png),
[Subtract invalid](thicken-subtract-invalid-window.png),
[Shell task](shell-task.png), [invalid Shell feedback](shell-invalid.png).
The ribbon is cropped from the native parent capture; OpenGL windows use the native
screen/window capture because QWidget grabs did not preserve the framebuffer.
The corrected captures were visually inspected; no mocked geometry is substituted.

Temporary test documents/profiles were removed after archival. Rollback files, the
installation manifest and the running isolated shortcut profile were retained; see
[cleanup evidence](cleanup.json).

## Boundaries

Thicken uses the native offset kernel; complex sheets or excessive thickness can
fail and produce actionable error feedback. New/Add/Subtract target eligibility is
shared with Extrude/Revolve: a current component-owned Body result. This change does
not migrate Loft/Pipe/Helix or replace the existing six Surface workflows.
