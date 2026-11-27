# Task panel

## Shared Apply workflow — approved November 27, 2026

The owner approved all pending previews together. Appearance, Move Components,
Sketch Pattern and Sketch Symmetry place **Done, Apply, Cancel** below every input
and selection field. Successful Apply commits once and restores fresh task defaults:
empty lists/references, default modes/numbers/options, and cleared pending picks,
previews and drag handles. Failed Apply retains inputs. Empty Done closes; otherwise
Done applies valid inputs and closes. Cancel discards only unapplied inputs, retaining
earlier Apply transactions. Move no longer offers Keep selection after Apply.
Native workbench tasks outside these Plus workflows retain their own behavior.

Symmetry starts with Create symmetry constraints enabled and Delete original disabled.
These remain mutually exclusive. A source point on a line axis receives Coincident
with its mirrored counterpart; other points retain Symmetric. Point-center symmetry
retains its native behavior. The bottom Cancel exits the tool; Exit Sketch remains
separate. The duplicate header Cancel is hidden for Pattern and Symmetry only.

Appearance Face mode shows collected/hovered faces in the View selection/preselection
preference colors, respecting both enable flags. Unpickable view overlays preserve
original materials, placements, visibility, native picking and Undo. Removing/clearing
targets, switching to Body, applying or closing removes these temporary highlights.
This section supersedes earlier retained-input/default-off descriptions below.

## Appearance workflow — owner approval November 27, 2026

Parts/History > Appearance opens a native task panel. Body and Face radio buttons choose
the selection mode; a list shows the targeted geometry. Body-to-Face expands all
CAD faces of the listed bodies; Face-to-Body lists each owning body once. The
collector follows existing click/Shift-click, Remove, Clear and Delete behavior.
Eligible explicitly selected bodies/faces are retained. Without such a selection,
the list starts empty; hover, edge and vertex inputs never select all component
results. A History feature action selects that exact owned feature, including
older Body features. Selecting a Body container resolves its current tip. Sketches
and child components remain excluded. Meshes support whole Body appearance;
mesh facets are not CAD faces. The November 27 approved History/selection correction
supersedes the earlier automatic whole-component default.

Selected/preselected face overlays contain only the requested face subelement,
never the whole source solid. Other faces retain their authored appearance, and
the existing selection preferences control highlight colors and enable flags.

Color uses a native chooser. Transparency uses a synchronized 0–100 percent slider
and number field, with Mixed displayed for differing initial values. Only edited
appearance fields change. A whole-body color replaces its face colors; editing
selected faces preserves other faces and all unrelated material fields.

Done applies and closes. Apply commits and keeps the task open. Cancel discards
unapplied edits, retaining earlier Apply results. Each application uses native Undo;
shared imported definitions retain native linked Undo across source and host files.
Changes affect all instances of the shared definition, with no occurrence overrides
or geometry/history nodes. Stale geometry/context is rejected before applying.

Status: owner-intent specification, reconstructed 2026-10-10. **Only the confirmed requirements are authoritative.** Material headed **Needs owner confirmation** is preserved for review and must not be treated as an approved change. The current application, agent-written specifications and implementation reports do not establish owner approval. Newer explicit owner decisions supersede older decisions on the same subject. See [evidence and unresolved decisions](EVIDENCE_AND_DECISIONS.md).

## Confirmed requirements

### Create/edit component instances — November 25, 2026

November 26 approved refinement: placement follows the native draw style live,
retains source colors, and applies at least 50% face transparency to the temporary
preview only. Parts > Add to active component opens this same task with the selected
sources. Outside-assembly destinations require the assembly-switch/Cancel prompt
specified in [Component Panel](COMPONENT_PANEL.md#active-component-additions-and-placement-display--november-26-2026).

Add existing/new keeps the component navigator and uses Next to open Create instances.
Quantity, Linear, Grid and Circular share one native form with per-definition counts,
parent-local coordinates, preview and prominent validation errors. Change parts
returns to the navigator preserving valid arrangement settings. New Component remains
separate. Right-click an individual pattern member to Edit instance pattern with the
same saved controls/references. Cancel leaves documents unchanged; OK commits one
operation. Preserve surviving identities and block referenced/edited-member removal.
Use native unit fields and reference collectors. Pattern members are controlled by
the pattern; independent Quantity links can be moved/constrained. See
[component contract](COMPONENT_PANEL.md#instance-quantities-and-patterns--approved-november-25-2026).

### Unified Clone and separate Extract geometry — November 25, 2026

Owner-approved extension, November 27: **Join surfaces** is checked by default
for new Extract geometry tasks. One face or one connected set of faces sharing
edges creates one extracted surface History feature. Connectivity may pass through
other selected faces; point-only contact is insufficient. Disconnected, overlapping
or invalid/nonmanifold joined input shows prominent TaskStatus feedback and blocks
acceptance without changing the document. The user can correct the selected faces
or uncheck Join surfaces. Unchecked creates one separate History feature per face,
in selection order, including disconnected faces. Keep the source solid intact.

History Edit restores the saved faces and checkbox. Joined results retain all source
associations and recompute as surfaces/shells, never solids. Splitting an existing
joined result retains its identity for the first face and appends the other results,
in one Undo step. Cancel preserves the existing feature. Missing source faces must
produce an error rather than silently shrink the joined result. Legacy extractions
open as separate-face results. Retain existing component ownership, face selection
gestures, preview controls, and contextual surface-selection toolbar behavior.
See [delivery evidence](../evidence/joined-extraction-20261127/README.md).

One Clone workflow collects whole geometric objects from direct child occurrences,
with parent-owned results named cloned body/surface/sketch/plane. Faces, edges and
vertices cannot be Clone inputs. Extraction is a later, separate operation: select
a face on a parent-owned cloned body to produce an extracted surface. Keep the
source body and child construction history intact. The native proposal uses the
existing list gestures, Remove/Clear, source/result columns, preview controls and
shared TaskStatus feedback. Creation and editing use the same task with saved
references. See [owner contract](COMPONENT_PANEL.md#clone-from-direct-children--november-25-2026).
The owner subsequently authorized implementation. Modeling > Other opens these forms;
History Edit reopens the existing result with its source. Direct-child browsing retains
occurrence identity. Preview creates no model objects; OK is atomic and Cancel leaves
no Undo entry. Saved source associations update independently of the preview toggle.

### Part-owned assembly constraints — November 25, 2026

Use the native joint tools and editor for constraints in the selected active assembly,
independent of the component in Edit. The parent row represents its fixed origin;
references may also use its own geometry or geometry within its direct child instances.
Reference/Excluded children cannot be selected as new assembly-constraint inputs.
Show component labels in the native reference list. Retain native joint types, values,
offsets, reversals and limit controls. Solve Assembly operates on the selected assembly.

Double-click/Edit on a saved constraint reopens the same editor with its references
and values. Acceptance updates that object in place. Cancel restores references,
values and placements; cancelling the first constraint also removes the newly created
backend. Creation, editing and deletion support native Undo/Redo. Invalid references,
incomplete input and conflicting constraints keep the editor open with the shared
prominent error feedback and do not commit a successful result. Collector layout and
approval are owned by [Component panel](COMPONENT_PANEL.md#assembly-constraints-and-padded-tabs--november-25-2026).

### Fillet edge selection repair — November 23, 2026

Owner reported a freeze after opening Fillet on an Extrude, clearing the automatically
selected edges, then picking an edge. Fillet must not automatically select every edge
on entry. In Plus component documents, whole-solid selection opens an empty collector;
explicit edge/face picks are retained. Keep the native explicit Use all edges option.
With no selection, a sole component result supplies the target; multiple results
require explicit selection, independent of Classic active Body. Connected/Tangent
curve selection must deliver each edge once and remain responsive when the task
consumes and clears picks. Preserve the native Fillet editor, geometry and identities.
This is a correction of the existing workflow, not a new task layout. See
[repair evidence](../evidence/fillet-20261123/README.md).

### Shell selection after opening — November 23, 2026

Owner requests opening Shell without choosing faces beforehand. Empty selection
or an incompatible curve must not prevent entry; users select faces in the open
task. This supersedes launch-blocking geometry guidance in the earlier routing repair.

Owner amended the proposal: **no target body/solid field**, and no Select faces or
Confirm Selection toggle. The selected faces implicitly identify their owning solid.
Clicking/focusing the face list activates viewport picking; clicking new faces adds
them. Delete removes highlighted list rows, as does Remove; Clear faces empties the
list. These actions remove references, never the source geometry. Keep at least five
visible rows with scrolling. Editing a parameter retains the list; click the list to
resume picking, without a confirmation step. Compatible preselection still populates
the list; empty or incompatible preselection still opens the task.

The owner requests this same list-driven selection pattern for Fillet/Radius and
comparable feature workflows, replacing their Select/Confirm Selection toggles as
they are updated. Preserve the installed selection-loop safeguards and native gates.

The [amended UI-only proposal](../evidence/shell-list-preview-20261123/README.md)
supersedes the earlier target-field prototype and awaits approval. It derives one
solid from the faces, preserves valid inputs on incompatible picks and allows a
different solid after clearing the list. Keep native Shell options and saved feature
identities, prominent recoverable errors and component access/history rules. No
active Body dependency. Owner approved Shell and shared Fillet/Radius, Chamfer and Draft list controls.
Implemented and installed; 20 focused and 99 installed native checks passed.
See [implementation acceptance](../evidence/dressup-lists-20261123/README.md).

### Unified Loft — November 23, 2026

Owner requests combining Additive/Subtractive Loft into one Loft with New/Add/Subtract,
matching Extrude/Revolve, and merging their Plus task entries. The
[native UI proposal](../evidence/loft-workflow-preview-20261123/README.md), including
the Solid/Sheet amendment, was explicitly approved in chat: "Approved. Implement".
Session `64ec80523dda`, fingerprint
`7f0837fb50c2141b8aa3107c2211c811187ef2617d025e89b32be62a6ace28ba`, was re-inspected
as fresh and within scope before implementation; tool approval state was untouched.

Owner additionally requested Solid/Sheet output. The approved workflow uses the
same two-column arrangement as Extrude/Revolve: Solid/Sheet left, New/Add/Subtract
right. Solid defaults on. Sheet selects and locks New, disables all operation
buttons, clears/hides the target and accepts compatible open or closed section
curves/edges/wires to create an uncapped sheet without thickness. Returning to
Solid keeps New, re-enables operation choices and preserves section selections.
Solid requires closed section profiles with supported native vertex endpoints.
Closed connects the final section back to the first; it does not cap a sheet.
Store output in saved features and restore it on editing; existing supported
Lofts default Solid. Sheet uses Loft preview in place of Tool volume.

New defaults to a new solid. Add/Subtract require an explicit current target or
the approved sole-eligible-target shortcut, independent of Classic active Body.
Choose target before collecting additional sections. Collect section profiles in
order in a five-row scrolling list, with drag reorder and Up/Down/Remove/Clear.
Use sketch profiles and planar faces, retaining supported native vertex end
sections. Require at least two compatible sections; preserve native validation
and expose Ruled surface, Closed and Refine result. Reordering sections changes
loft traversal, never the required predecessor order in History.

Reuse shared target highlighting/temporary visibility, Add green/yellow and
Subtract red/pink validity colors, Tool volume/Result, Show preview, Recompute on
update, Update preview and prominent recoverable errors. Same creation/edit task,
identity-preserving acceptance, clean Cancel, Undo/Redo and save/reopen; History
navigation/restoration, tree eyes and dependency/access rules remain applicable.
All sources/target belong to the explicit Component context; no ambient Body fallback.

Plus single/multiple-sketch and applicable binder task cards show one Loft entry.
Classic retains Additive/Subtractive Loft labels and routes to shared Add/Subtract
in Plus documents. Plus Loft entry defaults New. Preserve native legacy document
workflows, existing identities/settings and unrelated ribbon/tab/coordinate visuals.
Implementation scope: shared Loft engine/task, creation/edit dispatch, native Loft
command bridges, Plus task watchers/entry command and relevant registration/tests.
No Pipe/Helix migration is included. Saved native Loft features retain their native
editor and properties; newly created Plus Lofts use the shared creation/edit task.
See [implementation and native acceptance](../evidence/loft-20261123/README.md).

### Component-owned operation routing — November 23, 2026

Owner explicitly clarified that FreeCAD Plus has no active Body. Every modified
operation uses the active Component plus selected inputs/targets or saved feature
references. Selecting a solid for Shell must operate on that solid even when the
Classic native active Body is different or absent. Shell opens with an empty face
list when no faces are preselected; the first valid face determines the solid.
Extrude/Revolve use their shared Plus tasks for older Body-owned sketches too.
The rule and migration acceptance live in
[development guidelines](../DEVELOPMENT_GUIDELINES.md#component-routing-without-an-active-body--november-23-2026).
This repairs the approved workflow; no new layout was proposed.

### Shell and Thicken — November 23, 2026

Owner requests renaming Thickness to Shell for solid hollowing and a separate
Thicken feature that turns sheets into solids with designated thickness. Thicken
must offer New/Add/Subtract, matching Extrude/Revolve. Invalid geometry must not
leave a feature operation stuck. Existing prominent-error, target-selection,
preview-color, History and tree-visibility conventions apply. The
[native proposal](../evidence/shell-thicken-preview-20261123/README.md) illustrates total thickness, direction and invalid-selection feedback.
Owner later placed Thicken in Modeling's new Surface section, alongside the six
existing Surface tools, and removed the standalone Plus Surface tab. See the
[updated combined preview](../evidence/surface-modeling-preview-20261123/README.md).
Owner approved the combined scope in chat: "approved, implement". Session
`5e9afa49ce33`, fingerprint `54411b35662f1b635829af79c86f77f4f28f2201cd715b2343c81026f8634db4`
was re-inspected as fresh and within scope before implementation; tool approval
state was left untouched.

### Revolve Solid/Sheet output — November 23, 2026

Owner requests the same Solid/Sheet options as Extrude. Solid is selected by
default; Sheet automatically selects and locks New. Use the same left/right
operation layout and preserve the rotation axis and angular controls.
The owner approved the [native preview](../evidence/revolve-sheet-preview-20261123/README.md)
and requested implementation. Sheet clears any target; returning to Solid leaves
New selected and re-enables all operations. Open curves generate uncapped sheets;
existing saved Revolves default to Solid. See
[implementation evidence](../evidence/revolve-sheet-20261123/README.md).

### Extrude Solid/Sheet output — November 23, 2026

Owner requests Solid/Sheet radio buttons on the left of Operation, with
New/Add/Subtract on the right. Solid is the default. Sheet automatically selects
New and grays out/locks the entire operation group. Solid re-enables those choices.
Extruding an open line as Sheet creates a sheet with no solid thickness. Preserve
the shared creation/edit workflow. The owner approved the
[native proposal](../evidence/extrude-sheet-preview-20261123/README.md) and explicitly
requested implementation. Returning to Solid leaves New selected. Closed profiles
in Sheet produce uncapped sheets as well; existing saved Extrudes default to Solid.
See [implementation evidence](../evidence/extrude-sheet-20261123/README.md).

### Sketch Exit and action Cancel — November 23, 2026

Owner requests **Exit Sketch** replacing the sketch editor's Close button, plus an
adjacent **Cancel** while geometry creation, constraint application or another sketch
action is active. Cancel follows native Escape semantics for that action and keeps
the sketch open. Completed geometry/constraints are retained. Hide Cancel when no
action is active; Exit Sketch keeps native sketch-closing behavior. The
[native-widget proposal](../evidence/sketch-exit-preview-20261123/README.md) was
approved for implementation together with the selection toolbar changes. Cancel
is an action button rather than a dialog rejection: one Escape may reset an
unfinished drawing step while leaving its tool active, in which case Cancel
remains visible. This applies in both task UI modes and preserves the existing
LeaveSketchWithEscape preference.

### Sketch-selected modeling workflows — November 23, 2026

Owner requests Plus-mode Modeling Tools use current shared workflows, with Extrude
instead of separate Pad/Pocket entries. Classic retains its native buttons but
redirects to the shared workflow. The [proposal](../evidence/sketch-tools-preview-20261123/README.md)
also consolidates implemented Revolve/Groove in Plus and routes both Classic buttons
to shared Revolve; subtractive entries preselect Subtract. Other modeling tools keep
their current entries until corresponding workflows are implemented. The owner
approved the preview and implementation.

Owner subsequently approved implementation of all three pending previews. For
future migrations, combining additive/subtractive workflows (such as Loft) must
also combine their Plus task entries. Classic buttons remain and route to the
shared workflow with the matching operation. See the
[feature migration contract](../DEVELOPMENT_ROADMAP.md#shared-feature-workflow-migration-contract--november-23-2026).

### Remove New Body starting prompts — November 23, 2026

Owner instruction: remove all Tasks-panel entries offering New Body as the starting
point for a part. Component feature workflows create Bodies internally as results.
The proposal removes the Start Part watcher card across task-panel modes, preserving
Create Geometry and other task actions. [UI preview](../evidence/no-body-task-preview-20261123/README.md)
was approved for implementation with the other two pending previews.

### Prominent error feedback — November 23, 2026

Owner instruction: highlight the task-panel attachment/order error like the existing
Extrude target field; apply the same prominent treatment to all future implemented
error messages. Inline errors must stand out from ordinary task guidance and remain
readable. Use the target field's amber/pale-amber/dark-text palette consistently.
Keep the reason and recovery action in the text; do not rely only on color.

The owner approved the [native proposal](../evidence/task-error-preview-20261123/README.md).
It defines a
shared wrapped amber error box in Plane, Sketch, Extrude and Revolve. Newly raised
offscreen errors are brought fully into view without changing focus; repeats do not
keep scrolling. Valid recovery clears the highlight, while incomplete/idle/success
guidance remains normal. Use the shared treatment for future implemented inline
errors; existing native modal errors retain their native presentation. See
[implementation evidence](../evidence/task-errors-20261123/README.md).

### Reject later sketch supports before attachment — November 23, 2026

Owner bug report identifies the Attach Sketch button (`Sketcher_MapSketch`): creating
a sketch, then a plane, must not allow attaching that sketch to the later plane.
Validate the pre-attachment History order before writing any support or map mode.
Reject the selection, preserve the previous support/placement/order, and tell the
user to reorder History so the input precedes the sketch, then try again. Do not
silently reorder History as a side effect of accepting the new dependency. After
the user explicitly reorders the independent plane before the sketch, attachment
may proceed. Apply the same guard to sketch support-property picks. This repairs
the already-approved sequential-input contract; it adds no new task layout.
See [repair evidence](../evidence/sketch-attachment-order-20261123/README.md).

### Compatible plane picks and interchangeable references — November 23, 2026

Owner request applies to both creating a datum plane and choosing a sketch plane.
Each pick updates the preview. Keep compatible defining references together; when
the newly picked reference conflicts with the existing defining set, replace the
whole set with that new reference alone. In particular, XY then XZ leaves only XZ
and previews that plane. Two distinct coplanar lines remain together and define a
plane; compatible incomplete sets stay available for the next pick.

A line and point define a plane through the point, normal to the line, in either
selection order. Planes and planar faces are interchangeable; so are lines and
straight edges, and points and vertices. These rules belong to the defining-geometry
collector. Keep the separate origin and axis override controls and their meanings.
Unusable/foreign/later geometry must not discard valid prior selections; distinguish
geometric conflicts from admission failures or invalid offset/axis settings.

The existing saved line-plus-point construction defines a containing plane. Preserve
those saved results and reference identities when adding the new normal-through-point
construction. No implicit geometry migration on open, recompute or Cancel.

Owner approved implementation together with History ordering: "implement the plane
and sketch placement as well as the reordering of the history tab". Both shared
tasks and the production solver are installed. A hidden `NormalToLine` construction
flag preserves older containing-plane results when absent/false; new selections use
the normal-through-point construction. Opening or cancelling does not migrate it.
See [implementation evidence](../evidence/plane-history-20261123/README.md).

### Target guidance and sole-solid selection — November 23, 2026

Owner revision supersedes the unapproved November 22 popup: highlight the target field
instead, and automatically choose the sole body when Add/Subtract is selected.
The approved shared Extrude/Revolve behavior selects the current result when exactly
one eligible solid exists in the edited component. Preserve an existing valid target.
With multiple candidates, focus/highlight Target solid in amber and say "Choose a
target solid before selecting curves." With none, explain that a solid is needed.
Use inline guidance, not a modal popup.

Count eligible current Body results, not every History feature. Respect source
ownership, validity and predecessor rules for edited features; never select the
edited feature or a later result. A hidden sole target uses the existing temporary
selected-solid display without changing its History eye. Retain profile selections.
New Solid needs no target. Handle direct startup, target removal/invalidity, region
picking and Cancel. Deliberate Clear must not trigger automatic reselection on every
preview/numeric update. Continue the shared behavior for similar future workflows.

The owner approved implementation together with coordinate-system persistence:
"then implement both the target selection and the coordinate system persistence".
The [revised native UI preview](../evidence/target-highlight-preview-20261123/README.md)
defines the appearance. See [implementation evidence](../evidence/target-coordinate-20261123/README.md).

### Unified Revolve workflow request — November 22, 2026

Owner instruction: apply the same workflow to Revolve New Body, Add and Subtract,
combining the former Revolution and Groove workflows, with an identified rotation
axis, offset measured in degrees and distance replaced by degrees of rotation.
Use the existing feature-centered New Solid wording for the new-body result, matching
Extrude. Creation and editing use one task. Carry over profile collection, the requested
at-least-five-row scrollable list, selected-target visibility/color, Add green/yellow
and Subtract red/pink validity colors, numeric commit timing, History task scope,
source ownership, visibility restoration and native validation/Undo behavior.

The owner approved implementation: **"implement the expanded selection list and revolves"**.
The [layout proposal](../evidence/revolve-workflow-preview-20261122/README.md) adds
Axis of rotation, angular Start offset and Rotation angle controls to the shared
sections. This instruction supersedes D2763–D2765's old confirmation gate
for combining the workflows and angular fields. Other archived details below remain
unconfirmed unless explicitly covered by this request or existing shared-task rules.

The implementation uses native angular construction for Angle, symmetric/two-sided
rotation and Through all (360°). Angular start/end references are planes containing
the selected axis; end offsets are also degrees. Unsupported native To first/To last
entries remain disabled with an explanation. Invalid axes, intersecting profiles,
overlapping sweeps beyond 360°, unreachable/unsupported limits and invalid Boolean
results cannot be accepted. Native/body-owned legacy Revolution and Groove editors
remain available outside the shared component workflow; no legacy conversion is implied.

### Expanded selected-curves lists — November 22, 2026

Approved with the combined Revolve implementation: Extrude and Revolve profile lists
must show at least five complete rows and scroll to every selection. Size from native
font/row metrics and allow for a horizontal scrollbar so long names do not consume
the five-row minimum. Full labels remain available in tooltips. Keep native selection,
Remove/Clear/Whole sketch actions and task-panel scrolling in creation and editing.

### Shared selected-target and validity display — November 22, 2026

Owner instruction: apply Extrude's selected-target visibility and valid/invalid
preview colors to all similar feature workflows as they are implemented. A selected
target must remain visible in the configured selection color even with its History
eye off, without changing saved visibility; use the same target-field opacity and
temporary-display cleanup. Additive volumes use green when valid and yellow when
invalid; subtractive volumes use red when valid and pink when invalid. Preserve real
validation and prevent invalid acceptance. Apply these operation meanings where
applicable; do not invent color meanings for unrelated operations. This is a standing
requirement for future workflow work, not a claim that those workflows exist today.

### Extrude selected targets and validity colors — November 22, 2026

The owner approved displaying a selected Add/Subtract target even when its History
eye is off. Show it in the configured selection color, opaque while the Target
field is active and translucent after leaving it. This is temporary task display;
do not turn on or save its History visibility. Keep this selected-target display
when Show preview is off or automatic recomputation is disabled. A target already
visible remains natively pickable for face/edge references.

Add tool volumes are green when valid and yellow when invalid. Subtract tool volumes
are red when valid and pink when invalid, including no intersection/no material
removed. Retain a constructible tool after result validation fails, with the real
error and disabled OK. Do not reuse stale geometry or invent a tool when construction
fails. New Solid remains blue. Valid Result view keeps its normal result; invalid
Result view falls back to the invalid colored tool. Changing inputs with automatic
recompute off clears the displayed old volume until Update preview; target display
and eyes still work without recomputing. Keep native geometry/validity rules, numeric
commit timing, source ownership, selection settings, saved visibility/materials,
Undo and task cleanup. Tool colors must remain distinct through translucent solids.

### View fitting after sketch exit — November 22, 2026

The owner requested "exiting a sketch should resize the view to include the sketch"
and approved the direct native preview. Leaving new or existing nonempty sketch
drawing fits the visible model so the full sketch is included. Retain the normal
post-exit camera orientation and existing object visibility; fit after native camera,
coordinate-system and task-layout restoration. Drawing zoom remains under user
control while editing. Empty/deleted sketches, cancelled placement and closed or
replaced views must not trigger a stale camera adjustment. Preserve History tab
restoration, selection, constraints, geometry and native Undo/Redo.

### Sketch coordinate-system visibility — November 22, 2026

The owner requested "opening a sketch should hide the coordinate system" and
approved the direct native preview. Entering new sketch drawing or editing an
existing sketch temporarily hides the component Coordinate System: Origin point,
X/Y/Z axes and XY/XZ/YZ planes. New Sketch plane selection still shows its planes.
Sketcher's own red/green drawing axes remain visible. Leaving restores prior
coordinate visibility, while explicit History eye choices retain native task and
Undo semantics. Other geometry visibility is preserved. Automatic hiding must
not change saved visibility, add document edits or persist through save/reopen.
History eyes remain usable and reflect the current viewport display.

### Sketch dimensions and feature-task History — November 22, 2026

Owner approval: "Approved, implement both changes: no automatic dimensions and
switch to History during feature tasks, then restore the previous tab when leaving."
Mouse-only sketch drawing must not create unsolicited width, height, length,
radius, diameter or angle dimensions. Clearly applicable geometric constraints,
including coincidence and horizontal/vertical, remain enabled. Deliberate numeric
entry and explicit dimension commands remain available; existing dimensions stay
intact. Cursor-driven numeric labels must not be mistaken for user-entered values.
Typed fields still commit on focus leave; spin steps still commit immediately.

Part-feature creation/edit selects Components History on entry and restores the
prior Models/Part Tree/History tab when finishing, cancelling or abandoning the
task. New Sketch placement and native drawing form one task for this purpose.
Manual browsing remains possible during editing; refreshes do not force History
again. Scope tab restoration to the task's panel/view and clean it up on view or
document closure. See the component-panel specification for tab ownership.

### Extrude visibility and shared tree controls — November 22, 2026

The owner approved the direct native storyboard and instructed: **"Approved,
implement these changes for Extrude and enable the tree visibility controls in
all similar workflows."** The [approval and preview record](../evidence/extrude-visibility-20261122/approval.json)
identifies the exact candidate; no Companion approval state was written for the owner.

History eyes and Part Tree visibility remain usable during feature tasks. Preserve
the edited component/occurrence checks. A visibility action joins an existing native
editor transaction without accepting, cancelling or replacing it; idle eye actions
remain independently undoable. Unrelated pending operations still guard idle changes.
This covers shared Sketch, Plane, Extrude and Move workflows and native feature/datum
tasks through their common panel controls; it does not change their geometry or forms.

New Extrude initially hides construction planes, axes, points and other unusable
geometry. Currently shown sketches and solids/sheets with faces remain visible;
previously hidden eligible geometry is not revealed. Explicit eye choices can show
or hide geometry throughout the task, including optional direction/start/end references.
Editing an existing Extrude initially reveals only its profile geometry and target
solid if applicable, alongside the operation preview. For a face profile, display
the referenced face, not the whole donor object unless that object is also the target.

Visible model solids are temporarily 65% transparent. Entering Target solid makes
them opaque for picking. The chosen target uses the SelectionColor preference;
moving to another task control restores translucency while retaining that color.
Viewport/tree picking continues the active reference field. Hidden objects stay
hidden through focus changes. Temporary colors/transparency and automatic visibility
restore on completion, cancellation, context change and document close; explicit
Extrude eye choices remain source-owned and undoable. Accept does not copy temporary
target materials into the new feature. Eye clicks do not recompute a manually held preview.

Extrude profiles accept whole sketches, closed sketch regions and individual planar
faces of solids or sheets. Native face links stay associative, including picks through
Body/occurrence paths. Bare solid edges, axes, points and datum planes are not profiles;
nonplanar faces report the native planar-profile limitation. Existing sketch profiles,
optional references, New Solid/Add/Subtract, numeric commit timing and panel layout
remain intact. A face profile does not consume/hide its entire donor solid or sheet.

### Extrude rendering and sketch visibility correction — November 22, 2026

The owner reported diagonal artifacts in a rectangular Extrude preview and existing
geometry disappearing when entering the next sketch. Owner direction: visible
items must stay visible, and hidden items must stay hidden during sketch editing.
Both corrections were previewed in native disposable fixtures and explicitly
approved in chat: "Approve both corrections".

Extrude keeps its existing colors, transparency, controls and operation behavior;
its solid preview must shade faces consistently without diagonal triangle artifacts.
Entering a component sketch editor preserves other geometry's visibility, including
prior sketches, solids, supports and external geometry. Native editing graphics and
camera behavior remain; History eyes continue to allow explicit changes. Temporary
fundamental planes during placement retain the previously approved lifecycle.

Direct native proposal: [clean extrusion](../evidence/render-visibility-fix-20261122/proposed-extrude.png),
[preserved sketch visibility](../evidence/render-visibility-fix-20261122/proposed-sketch.png).
Session `6701f7246f6c`, seed `988a72b88d2d9ac7a06c23b7ec83f508bcbc9e4d`,
allowlist `ui/fixes.py`, fingerprint
`3716426d3f9acdcae424a11acfdf14f7bc8e11418a1c7c276f3511096c95b927`.
The proposal changed only a disposable native fixture; production acceptance is
recorded in [WORK_STATE](../WORK_STATE.md#extrude-rendering-and-sketch-visibility-correction--november-22-2026).

### Typed values versus arrow steps — November 22, 2026

**Approved in chat November 22; implementation acceptance is recorded in WORK_STATE.** Owner:
“while editing an extrude and any other feature, keep it such that editing the
number value doesnt change the preview until the field is left. however, clicking
the up and down arrows to adjust the length should update the preview immediately”.
This refines the earlier blanket focus-leave rule: typed input is deferred, while
an explicit up/down spin-button step commits immediately with focus retained.
The step uses the current valid entry. Later focus leave must not duplicate that
update unless more text was entered. Recompute on update off retains manual preview.
Keep existing controls, units, precision, limits, expression handling and validation.
Apply consistently to shared feature inputs and native numeric editors; do not
special-case only the Extrude Length control in production.

The isolated native Extrude editing prototype demonstrates:
[typed 12, preview still 8](evidence/numeric-step-20261122/numeric-typing-proposed.png),
[Up to 13, preview immediately 13](evidence/numeric-step-20261122/numeric-arrow-proposed.png),
and the [current delayed-arrow baseline](evidence/numeric-step-20261122/numeric-arrow-before.png).
[Checks](evidence/numeric-step-20261122/prototype-check.json) exercise actual Qt
up/down clicks, retained focus, deferred typing, no duplicate blur update, manual
mode, and unchanged saved geometry/Undo. The temporary prototype step handler is
not the shared implementation; production implementation and native editor verification are recorded in
[acceptance](../WORK_STATE.md#design-interaction-implementation--november-22-2026).

Companion session `bd29cb90beec`, seed `0bbb563eaa428cad592b86ea209bea6eb0793d12`,
allowlist `ui/step_preview.py`, fingerprint
`cedbece46e79b70c1f021f61cf36368073b38dfa7b14c45a5ce5d13fbc1763db`.
The isolated prototype remains historical evidence; the owner subsequently approved
production implementation together with the Design idle and sketch visibility changes.

### Design idle actions proposal — November 22, 2026

**Approved in chat November 22; implementation acceptance is recorded in WORK_STATE.** Owner: “while in design
mode and nothing is selected, the options in the task panel should be new sketch,
Datum Plane, Datum Line, and Datum Point”. This is approved together with the sketch visibility
proposal below and the numeric arrow-step refinement above.

With an active editable component, no selection and no active operation, the Design
task panel offers exactly **New Sketch**, **Datum Plane**, **Datum Line**, and
**Datum Point**, vertically in that order. The proposal uses native task command
icons/links under **Create Geometry**, replacing the idle **Start Part / New Body**
prompt. Selection returns to contextual options; an ongoing operation retains its
task even if selection is empty. Toolbar, History, Origin visibility and operation
layouts are preserved. Datum Line/Point creation tasks are not redesigned here.

Direct screenshots: [current idle panel](evidence/design-empty-20261122/before.png),
[proposed four actions](evidence/design-empty-20261122/proposed.png).
Native TaskWatcher prototype commands only record activation; actual creation,
component ownership and transitions were subsequently implemented and verified;
see [acceptance](../WORK_STATE.md#design-interaction-implementation--november-22-2026).
[Fixture checks](evidence/design-empty-20261122/prototype-check.json) verified order,
stub activation, selection/active-task guards and unchanged objects/Undo.

Companion session `197361ac1c38`, seed `83398ae6271b74ccaecd0338a1c74cca0cba4a42`,
allowlist `ui/empty_preview.py`, fingerprint
`309d1ca9e3c8eb504bb6a4160de44cd23e96d9662dc6244343cb071d06b85a69`.
The isolated prototype remains historical evidence; production acceptance is separate.

### Sketch planes and History visibility proposal — November 22, 2026

**Approved in chat November 22; implementation acceptance is recorded in WORK_STATE.** Owner: “automatically show
the fundamental planes when creating a new sketch. also make it possible to hide
and show objects in the history tab while doing so”.

Approved sequence: New Sketch shows the edited component's XY, XZ and YZ planes
while choosing support. The existing fixed-left History eyes can hide/show model
objects and individual planes without closing the task or changing support picks.
Axes retain their existing visibility, and the task layout, native plane appearance,
Origin grouping, preselection and numerical focus-leave behavior are preserved.
Automatic plane visibility is temporary and restores when placement ends; explicit
eye choices should retain normal user visibility semantics. Implementation must
handle History visibility safely during native sketch drawing too, without breaking
the sketch transaction or Cancel. This last phase is not validated by the prototype.

Direct native simulation screenshots: [before](evidence/sketch-visibility-20261122/before.png),
[planes shown](evidence/sketch-visibility-20261122/proposed.png),
[solid and YZ plane hidden through History](evidence/sketch-visibility-20261122/hidden.png).
No new controls are proposed. The isolated handler changes only disposable fixture
visibility and restores it afterward; it is not production persistence integration.

Companion session `e312b15f0ebe`, seed `13628139222557fb2255a66696293e00e8372623`,
allowlist `ui/visibility_preview.py`, fingerprint
`02b290a86faa425eba51f54ce8c8a489b1350bb3e6ba4c3e483e7d85d99d47fe`.
Both sides use the installed native app corresponding to `74537162bf` and equivalent
disposable fixtures. [Prototype checks](evidence/sketch-visibility-20261122/prototype-check.json)
exercise actual eye clicks, hide/show, preserved task/support, restored visibility
and unchanged object inventory/Undo. Production acceptance is recorded separately.

### Sketch offset and local axes proposal — November 21, 2026

**Approved in chat and implemented.** The owner noted that Create Sketch lacks Offset and
asked how local X/Y/Z could stand out from coincident fundamental axes, suggesting
orange and bold. The isolated native proposal adds **Offset** and **Reverse offset**
under sketch support selection. Zero remains on the support; signed distance follows
its unflipped normal. Flip normal changes orientation without moving the offset
sketch plane. Numeric updates wait for focus leave, and automatic-off keeps the last
preview. Creation and placement editing share the saved control.

The proposed shared Plane/Sketch local indicator uses orange, thicker lines and
larger bold X/Y/Z labels. Its arms are 1.4 times the previous length, separating
local labels from fundamental labels when origins coincide. The preview draws the
local indicator visibly over geometry; fundamental/global axes remain unchanged.
This is a visual distinction, not a change to coordinate frames or geometry.

Direct screenshots: [current Sketch](evidence/sketch-offset-20261121/before.png),
[5 mm offset and orange axes](evidence/sketch-offset-20261121/proposal.png),
[coincident-origin axes](evidence/sketch-offset-20261121/axes.png) and
[reversed offset](evidence/sketch-offset-20261121/reverse.png).
[Prototype checks](evidence/sketch-offset-20261121/prototype.json) passed for deferred
updates, reverse offset, position-preserving normal flip, automatic-off, inherited
plane frame and unchanged object inventory/Undo. OK was disabled in that isolated
candidate. Production creation/editing now saves the offset and enters native sketch
drawing normally; older managed sketches default to zero without migration on open
or Cancel. See [installed acceptance](../WORK_STATE.md#sketch-offset-and-orange-axes-implementation--november-21-2026).

Session `3a22e0142561` supersedes unrendered `daeaead683ed` after the axes request.
Seed `b423e491db3a5fac2d5f9d571c5f615f61f98bb6`; allowlist `ui/sketch_task.py`.
Final inspected fingerprint:
`cd97d1eb5894ba755d80faa829ef7cbb4827e5d2d4807ccf3c00e5d4b6098e4f`.
Scope/capture checks passed; no tool approval state was changed.

### Idle task panel

Before a document exists, show **New File** and **Open**. Dock Tasks at the right initially and preserve the user's later customized location. The DOCX's proposed actions after New File are retained below for confirmation. Do not derive additional idle actions from whichever commands the current build happens to display. [C06](EVIDENCE_AND_DECISIONS.md#c06)

### Right-hand Tasks dock — November 21, 2026

The owner approved the docked Tasks preview in chat and instructed implementation.
Tasks initially occupies a resizable dock to the right of the modeling viewport,
both while idle and during an operation. Existing Tasks overlay/floating layouts
receive this default once. Subsequent user choices of location, width, floating
state and visibility are remembered; other overlay memberships are preserved.
The initial width is 320 logical pixels. Native task contents are unchanged.

Approved native screenshots: [before](evidence/tasks-dock-20261121/before.png),
[docked task](evidence/tasks-dock-20261121/approved-task.png) and
[docked idle](evidence/tasks-dock-20261121/approved-idle.png).
Companion session `c074100600fa` used an isolated source snapshot at
`b9f1a232a8c99be460c910180515ca82a295ca31` because the main repository's preview
configuration/submodules prevented direct review creation. Candidate fingerprint:
`11ae30691ad140ce547dd63dec99b1f701823dd8137c8d52ff216805a8c6daa5`.
Approval is the owner's chat instruction; no tool approval state was changed.
Installed-app and persistence evidence is in
[WORK_STATE](../WORK_STATE.md#right-hand-tasks-dock--november-21-2026).

### New Plane workflow revision — November 21, 2026

Owner direction: New Plane opens in the right-hand Tasks panel. Remove the
Select geometry/Enter values dropdown and the separate Select button. Geometry
selection is active immediately; retain the XY/XZ/YZ plane shortcuts. Once the
selected elements define a plane, show a purple preview with its origin and
orientation. A combined **Origin and Orientation** section expands for adjustments.
Owner refinement: remove origin-coordinate and X/Y/Z-vector readouts from this
section, including its collapsed summary. Retain the origin marker and axes in the
3D preview. Origin accepts only a selected point;
clearing/deselecting that point defaults to the universal origin projected onto the
plane. Choose X or Y, then use a line, edge or two points to define that axis. The
proposal uses first-to-second point order for direction and derives the other axis
to maintain a right-handed frame. **Flip normal** reverses the preview's Z axis,
preserving the plane position and chosen in-plane axis. No numeric origin/vector
entry fields are present. A selected off-plane point is projected onto the plane.
Direction references must be straight edges/lines or two distinct points; their
direction is projected into the plane. Degenerate/perpendicular directions are refused.
The preview's coordinate frame is local
to the proposed plane; existing global coordinate graphics stay unchanged.

The owner approved this simplified UI in chat and explicitly requested implementation.
The approved native prototype is session `bb9622ce36bb`, fingerprint
`26f40e674d694d71da62c2ad1da6a1ac8b5d4703e7c4915dbce94f4fb4e9bec9`:
[combined section](evidence/plane-task-20261121/combined.png),
[flipped normal](evidence/plane-task-20261121/flipped.png),
[native prototype checks](evidence/plane-task-20261121/combined-prototype.json).
This supersedes session `b81d0fbb375d`; its separate-section screenshots remain historical.
Those prototype images used presentation fixtures. The implemented task now accepts
real geometry picks, creates/edits associative component-owned planes, and supports
native Undo/Redo and save/reopen. Plane definition accepts a planar face/plane,
three noncollinear points, a line and off-line point, or two distinct coplanar lines.
The existing New Plane command opens this task for Plus component documents without
requiring a Body. Legacy documents retain their native datum command.
Approval is the owner's chat instruction; no tool approval record was modified.
See [installed acceptance](../WORK_STATE.md#new-plane-implementation--november-21-2026).
This direction supersedes conflicting unconfirmed plane-form proposals below.

### Archive-guided plane proposal — November 21, 2026

**Approved in chat:** “implement the concepts, do not copy over the code.”
The owner requested a review of the abandoned fork, starting with Create Plane.
[Source findings](../ARCHIVE_REFERENCE.md#plane-workflow-review--november-21-2026)
inform a focused refinement of the approved form above:

- Specific next-pick guidance distinguishes incomplete from invalid selections.
- Readable numbered reference names match persistent amber point markers;
  straight-line references also receive a temporary highlight.
- Picking an existing defining reference again toggles it off. Delete removes
  selected list entries or clears the focused origin/axis reference field.
- **Reverse axis** sits beside Clear axis, reversing X/Y together while preserving
  the origin and Z. Flip normal keeps its existing meaning.

Preserve the combined section, universal-origin default, X/Y definition controls,
purple plane/local frame, XY/XZ/YZ shortcuts and focus-leave numeric recompute.
No coordinate/vector forms or selection-mode controls return. Creation and editing
share the resulting workflow; axis reversal is now saved on the plane, while older
planes default to unreversed without mutation on opening/Cancel. Temporary origin-plane visibility and broader curve support
remain separate recommendations in the archive review.

Direct native screenshots: [current two-point state](evidence/plane-guidance-20261121/before.png),
[proposed next-pick guidance](evidence/plane-guidance-20261121/proposal.png),
[defined plane](evidence/plane-guidance-20261121/defined.png), and
[expanded frame with reversed axis](evidence/plane-guidance-20261121/frame.png).
The fixture uses an isolated document/profile; the candidate reuses the installed
read-only plane solver. OK is deliberately simulated and creates nothing.
[Prototype checks](evidence/plane-guidance-20261121/prototype.json) passed for
guidance/highlights, reversal preserving origin/normal, repeat-pick toggling,
Delete, focus-leave numeric updates and unchanged object inventory/Undo count.
These checks do not establish production acceptance or archived-build behavior.

Companion session `1a6b86c4f6b2`, source seed
`651cac309f2f62aa21f801f7ff1ecdcc0e86d537`, allowlist `ui/plane_task.py`.
Candidate fingerprint:
`4036cbc0e10ddda0f4528687063d79cbb4cd40b0503b73d1b017c9f27d5318c3`.
Scope inspection passed and capture was current at approval. No tool approval state
was changed. The concepts were implemented afresh in the current plane task/solver;
archived source was not copied. See [implementation acceptance](../WORK_STATE.md#plane-guidance-implementation--november-21-2026).

### New Sketch placement workflow — November 21, 2026

Owner direction: choose a plane or face, designate origin and orientation, then
create the sketch. Preselected items must appear as the sketch-plane references
when the task opens. The approved task reuses New Plane's visual structure:
**Sketch plane**, **Origin and Orientation**, and **Preview**. It retains XY/XZ/YZ
shortcuts and point-origin/X-or-Y-direction/Flip normal controls, without coordinate
readouts, a Select button or a selection-mode dropdown. The later approved Offset
controls above extend the initial support-only proposal. At zero offset the sketch
lies on the selected support. OK creates the sketch and proceeds
to native drawing/constraint editing; Cancel creates nothing. Placement editing must
reuse this same task with saved inputs under the shared create/edit rule.

Owner refinement: choosing a plane automatically inherits its origin and complete
orientation. Choosing a planar face instead projects the part-local origin and
part X axis onto that face. The existing fields show readable automatic reference
labels, without coordinates or vectors. Explicit point/direction overrides remain
available; clearing an override restores the support-dependent default. If part X
is perpendicular to the face, its zero-length projection requires an explicit axis
selection. These sketch defaults do not change the New Plane origin rule.

The proposal accepts one plane or planar face. Multiple preselected references are
shown without silently choosing one; the user removes extras to obtain a valid
support. References retain native mapped identities but display readable face names.
The original preview candidate used read-only frame calculation and a transient
overlay; its OK action was a simulation. The approved implementation now creates
a native sketch, enters drawing, and reuses the task for saved placement editing.
Reorient Sketch and attachment editing open that workflow for sketches created by
it; regular sketch drawing/constraint editing remains native. See
[installed acceptance](../WORK_STATE.md#new-sketch-placement-implementation--november-21-2026).

Owner approved this revised workflow and authorized creation/placement-editing
implementation in chat on November 21, 2026: "approved. implement the new sketch
workflow with these automatic origin and orientation defaults, and make sure
editing sketch placement opens the same workflow."
Approved session `a2bc3ec0e274` supersedes `c01f5acbdf83`, seed
`f4fe8fd90a4b432e238d95aca4a62b7b11f89f12`, candidate fingerprint
`64b13aadcffc48e2218b08dd30990acce93548ad83826dadf361dfe4b6d70d67`.
Direct renders: [current attachment dialog](evidence/sketch-task-20261121/baseline.png),
[preselected face](evidence/sketch-task-20261121/preselected-face.png),
[origin/orientation](evidence/sketch-task-20261121/origin-orientation.png),
[inherited plane frame](evidence/sketch-task-20261121/inherited-plane.png),
[preselected History plane](evidence/sketch-task-20261121/history-plane.png).
[Prototype checks](evidence/sketch-task-20261121/prototype.json) verify face/History
preselection, translated/rotated plane frame inheritance, part-local face defaults
under a moved/rotated part, restoring defaults, degenerate projection feedback and
recovery, preservation of multiple selections, invalid empty support and no
model-object creation. No tool approval state has been modified. This new owner
direction supersedes conflicting unconfirmed New Sketch proposals below.

### Extrude task proposal — November 21, 2026

This initial length-only proposal is superseded for review by the
[archive-guided proposal](#archive-guided-extrude-proposal--november-21-2026) below.
The archive-guided proposal was approved with the November 22 radio-button
amendment recorded below.

Owner request: preview a similar Extrude task with **New Solid**, **Add** and
**Subtract**, including target selection, before implementation. The isolated
native proposal reuses the New Plane/New Sketch section style: **Operation**,
**Profile**, **Extent** and **Preview**. New Solid hides the target field. Add and
Subtract show **Target solid**; click the field and pick the current result in
History or the model. Clear removes that target; OK requires one for these modes.
Selected sketch/curve references populate Profile, with Remove/Clear controls.

This first proposal covers length-based extrusion: One side, Symmetric or Two
sides (revealing Second length), Sketch normal and Reverse. Alternative native
termination types, custom directions and taper are not part of this first UI
proposal and remain available in the unchanged installed native task. The
proposal uses blue/green/red translucent tool volumes for New Solid/Add/Subtract,
including the full removal volume through the target. These are tool overlays,
not evaluated Boolean results. Show preview and Recompute on update follow the
existing task pattern; numbers redraw only after focus leaves their field.
Future creation and operation editing must share this task with saved inputs.

**Approval pending.** Companion session `45e8bcfeb03a`, isolated seed
`b81bd2ded194f80b2d3aa95a5c24ed7a14f7bc30`, exact allowlist `ui/extrude_task.py`,
candidate fingerprint `0890da6ef6250cd9f5060eec482d2c43cbd9d2b7b162dcfc64b47c75162a3607`.
Direct screenshots: [current native task](evidence/extrude-task-20261121/baseline.png),
[New Solid](evidence/extrude-task-20261121/new-solid.png),
[Add](evidence/extrude-task-20261121/add.png),
[Subtract](evidence/extrude-task-20261121/subtract.png),
[missing target](evidence/extrude-task-20261121/missing-target.png).
[Prototype checks](evidence/extrude-task-20261121/prototype.json) verify preselection,
mode/target controls, selection, deferred numeric redraw, automatic-update-off and
unchanged model object inventory/Undo count. The candidate renders a disposable
fixture through transient Coin geometry; OK is simulated. No production command,
extrusion/Boolean backend, persistence or installed payload has been changed.
No companion approval state was modified. This proposal does not approve the
conflicting historical/unconfirmed Extrude items below.

### Archive-guided Extrude proposal — November 21, 2026

**Approved November 22, 2026, with the radio-button amendment below.** The owner requested a fresh workflow informed
by archived concepts, with no old implementation copied. The
[archive review](../ARCHIVE_REFERENCE.md#extrude-workflow-review--november-21-2026)
explains what to recover and what to leave behind. The new native Qt proposal uses
the current light theme and right Tasks dock:

- **Operation:** New Solid/Add/Subtract; Add/Subtract require an explicitly picked
  current target solid. Mode changes retain the selected target for reuse.
- **Profile:** preselected sketch/curves, Remove/Clear/Whole sketch, persistent
  amber outline and planned closed-region picking. One connected closed region
  with optional holes is the intended initial solid-profile contract.
- **Start:** Profile plane, Offset or Reference; reveal a signed start offset and
  picked start reference only when relevant. This offsets the extrusion start,
  independently of the saved sketch placement offset.
- **Extent:** One side/Symmetric/Two sides; label a symmetric dimension Total length.
  Independent side end controls expose Length, Up to face, Up to shape, To first,
  To last and Through all. Reference and end-offset rows appear only when relevant.
  Target-dependent ends require a target; missing references receive direct guidance.
- **Direction and taper:** collapsed by default; profile normal or a picked straight
  axis/edge, length measurement convention, per-side taper and Refine result.
  No numeric XYZ direction-vector form is restored.
- **Preview:** Tool volume (blue/green/red) or Result, Show preview, Recompute on
  update and explicit Update preview. Numeric changes commit only on focus leave;
  automatic-off retains the previous overlay until refreshed. Future creation and
  editing must share all controls and saved inputs.

Direct screenshots: [New Solid](evidence/extrude-guidance-20261121/new-solid.png),
[Add to a picked face limit](evidence/extrude-guidance-20261121/add-limit.png),
[Subtract tool volume](evidence/extrude-guidance-20261121/subtract-tool.png),
[Subtract result](evidence/extrude-guidance-20261121/subtract-result.png),
[two sides](evidence/extrude-guidance-20261121/two-sides.png),
[start/direction/taper controls](evidence/extrude-guidance-20261121/advanced.png),
[missing target](evidence/extrude-guidance-20261121/missing-target.png), and
[installed native baseline](evidence/extrude-guidance-20261121/before.png).

**Prototype limits:** OK creates nothing. This fresh candidate simulates a known
circular profile and plate; transient Part shapes demonstrate actual fixture
Boolean results without adding document features. Region hit-testing, optional-hole
profiles, general first/last/whole-shape limits, nonplanar references, custom direction,
independent taper/measurement semantics, persistence and operation editing still
require production design/integration and tests. Showing controls does not establish
backend support. Temporary target visibility is restored on mode change/Cancel;
the owner documents/profile and installed payload were untouched.

[Prototype checks](evidence/extrude-guidance-20261121/prototype.json) passed for
preselection, required target/limit, real selection field routing, the shown
up-to-face and through-plate fixtures, tool/result switching, numerical focus-leave,
manual refresh, symmetric/two-side controls, unchanged object inventory/Undo and
restored target visibility. The archived tests were not run.

Session `c706bf161145`, clean isolated seed
`29009520f1f7d7a60e2e4be1c1713f600c477794`, allowlist `ui/extrude_task.py`.
Final inspected fingerprint:
`1284f27b1decce0620010a1e4fe709bc6a105cdb57a2505272f0a51841e06439`.
Scope/capture checks passed. No tool approval state was modified.

### Extrude implementation — November 22, 2026

Owner instruction: **"make the operation a radio button option stacked vertically,
new solid, add, subtract. then implement"**. This approves the preceding direct
native preview and explicitly authorizes that amendment and implementation.
Operation now uses an exclusive vertical **New Solid / Add / Subtract** radio
group; other approved sections, controls, colors and terminology are retained.

The amendment was rendered in isolated session `c706bf161145`, fingerprint
`551bd082d03c3d3e78b1c70bbff4de8f930d718086556f408faf88fba69e74dc`.
[Direct amended native preview](evidence/extrude-20261122/radio-preview.png).
Chat authorization governs this limited amendment; companion approval state was
not modified. No archived implementation was copied.

Plus Extrude opens the task directly, including with no profile selected.
Preselected sketch/curves and eligible targets populate their fields. After
selecting a sketch, clicking inside a closed region selects its boundary curves
and immediate holes; Whole sketch restores the complete profile. Fields route
native picks to target/start/limit/direction references. Remove, Clear and Delete
edit the profile/reference lists. The amber profile outline remains while an
end or target is incomplete. Numbers commit on field leave; automatic-off keeps
the old preview until Update preview. OK validates the latest field values.

OK creates one associative Extrude, supplying its internal native Body. History
Edit/double-click reopens the same prefilled task and preserves feature identity.
Cancel and previews do not change model objects, persistent visibility or Undo.
Result preview hiding is local to the active view and composes with component
display rules. Existing native body-centered features retain their editors.

Geometry boundaries: closed planar profiles must produce one valid solid;
targets are current component-owned native Body results. Start references must
be parallel to the profile. Taper uses Length ends; native until-face coverage
restrictions apply to face/shape limits. Whole solid limits resolve the first
forward boundary intersected by the profile. Moving an operation to another
internal Body after it has downstream features is rejected. Imported-Part
targets and legacy migration remain separate. These are explicit validation
errors, not disabled mockup controls.

See [implementation and installed acceptance](../WORK_STATE.md#extrude-implementation--november-22-2026).

### Numerical field updates

**Numeric recompute rule — owner instruction, November 21, 2026:** all numerical
fields must defer "Recompute on update" until the user leaves the field. Do not
recompute previews or geometry for intermediate keystrokes, incomplete values or
while the user is still editing the field. Tab or clicking another control commits
the field; valid committed values trigger recompute only when that option is on.
When it is off, keep the prior preview until an explicit refresh or final acceptance.
Final acceptance validates the latest values before creating/updating geometry.
This is application-wide intent, including native and Plus task forms. Shared Qt
integer/decimal editors, native QuantitySpinBox/InputField and Plus Move/Rotate
preview consumers now defer numerical value updates until focus leaves. Bound
InputField expressions also avoid document writes while typing. Final acceptance
reads the latest valid value. The [acceptance record](../WORK_STATE.md#new-plane-implementation--november-21-2026)
distinguishes tested editor families and workflows from arbitrary third-party editors.

### Shared task patterns

**Shared create/edit workflow — owner instruction, November 21, 2026:** editing
any feature or operation must reopen the same task-panel workflow used to create
it. Reuse the same form, controls, selection methods, preview and validation;
populate them from the feature's saved parameters and references. Acceptance
updates that existing feature in one undoable operation, preserving its identity
and downstream references. Cancel leaves it unchanged. Numerical fields use the
same focus-leave recompute rule in both modes. Do not introduce a separate editing
dialog or a reduced editing form. This applies to all current and future feature/
operation workflows; each integration must verify both creation and editing.
Plane creation and editing already share `PlaneTask`, including History Edit and
native tree double-click. This rule does not claim that all legacy/native feature
editors have been individually audited or retrofitted.

Use sketches, operations/features and other geometry as the user's modeling vocabulary. Background Body ownership must not require independent Body management. Feature selection lists, collapsible sections, preview choices and their exact defaults are preserved in the DOCX-derived sections below; most earlier authorizing conversations are unavailable. Do not silently remove fields just because a toolbar action is consolidated. [Current owner direction](EVIDENCE_AND_DECISIONS.md#current)

A modeling operation requires an edited component. The file cannot own sketches or modeling geometry; selecting a component once does not enter Edit. Definitions, storage, external edits and the November 24 approved Add Component workflow follow [Component Panel](COMPONENT_PANEL.md). [C09](EVIDENCE_AND_DECISIONS.md#c09)

Component geometry inputs must respect the confirmed [Part Type rules](COMPONENT_PANEL.md#part-type-and-visibility): unpromoted Reference and Excluded geometry cannot be used. [C10/U069](EVIDENCE_AND_DECISIONS.md#c10) The owner reaffirmed that all Reference geometry must first be added to the active component's History through **Add Reference Feature**, before any use in that component. Direct selection or silent automatic reference creation cannot bypass this prerequisite. [October 11 clarification](EVIDENCE_AND_DECISIONS.md#reference-geometry-prerequisite---october-11-2026)

G1.7b3t extends that admission check to existing split/join link-property editors,
including Slice Apart filters. A refusal keeps the editor open; removing links
remains available. See the [technical boundary](../ARCHITECTURE.md#splitjoin-property-editor-admission-g17b3t).
Tree drop/replacement remains separate; this adds no new operation workflow.

G1.7b3s applies the prerequisite and edited-component result ownership to existing
split/join command creation, including individual Slice Apart results in History.
The [technical boundary](../ARCHITECTURE.md#splitjoin-creation-integration-g17b3s)
records supported inputs and deferred input editing; this defines no new workflow.

G1.7b3r extends that admission boundary to existing Compound link additions through
native drop/replacement hooks and the Links editor. Refusal retains current links;
removal remains available. See the [technical boundary](../ARCHITECTURE.md#compound-link-edit-admission-g17b3r).
This integrates component rules with the existing operation UI.

G1.7b3q applies the same prerequisite and component ownership to native Compound
creation, keeping ordered input links and the native geometry behavior. Its
[technical boundary](../ARCHITECTURE.md#part-compound-integration-g17b3q) covers
command creation only; this does not define a new Compound task workflow.

G1.7b3p applies that same component preflight and ownership to the separate
Part Section command, preserving the existing Section algorithm and base-derived
line appearance. Its [technical contract](../ARCHITECTURE.md#direct-part-section-integration-g17b3p)
records the supported scope; WORK_STATE records acceptance.

G1.7b3o extends eligibility checks to Part Cut, Intersection, Union and the Boolean
operation dialog's Apply action. Accepted local operations keep input ownership
and place the result in the edited component's History. Cross-component inputs and
external destinations through an importing assembly remain outside this supported
path; the [technical contract](../ARCHITECTURE.md#part-boolean-eligibility-and-ownership-g17b3o)
records the boundary. This does not approve a new Boolean workflow.

G1.7b3n applies the same prerequisite at PartDesign Boolean command start and tool
addition, before native selection normalization or ownership mutation. Refusal keeps
the current task and tool list intact; removal remains available. This is component
eligibility integration, not a redesigned Boolean or Add Reference Feature workflow.
See the [technical boundary](../ARCHITECTURE.md#boolean-input-admission-g17b3n);
WORK_STATE owns build/runtime acceptance. Cross-component Full Component tool
ownership remains undefined by the latest Reference-only clarification.

Implementation boundary: G1.7b3e guards native PartDesign profile intake and Sketcher
Projection/Intersection reference admission using the shared component policy. Their
native editors and geometry rules remain the baseline. G1.7b3f extends this to native
attachment inputs (picked, initial batch and typed) and the shared PartDesign picked
axis/direction/plane collector. A rejected input keeps the existing reference and
editor transaction. G1.7b3g adds the separate attachment editor's input/preview and
Apply/OK checks, plus Extrude up-to-face/shape intake. G1.7b3h adds picked Loft/Pipe
profile, section, main-path and auxiliary-path admission; its [bounded contract](../ARCHITECTURE.md#loftpipe-profile-section-and-path-intake-g17b3h) preserves native operation workflows. G1.7b3i adds shared dress-up edge/face and
transformed-feature Original admission, including whole-edge controls; see its
[bounded contract](../ARCHITECTURE.md#shared-dress-up-and-transformed-feature-intake-g17b3i).
G1.7b3j adds command-start checks before dress-up/transformation selection
normalization or mutation, including Multi-Transform conversion, and prevents a
rejected Pattern Original being treated as a direction; see the
[command boundary](../ARCHITECTURE.md#dress-up-and-transformation-command-admission-g17b3j).
G1.7b3k supplies the same-component [native Boolean ownership prerequisite](../ARCHITECTURE.md#native-boolean-ownership-within-a-component-g17b3k), including History/Edit and persistence. Boolean input guards and cross-component tool handling remain pending; native Boolean tasks have not been redesigned.
Other collectors remain unfinished; see the [intake contract](../ARCHITECTURE.md#native-modeling-intake-eligibility-g17b3e),
[attachment/reference boundary](../ARCHITECTURE.md#attachment-and-shared-task-reference-intake-g17b3f)
and [attachment/Extrude boundary](../ARCHITECTURE.md#python-attachment-and-extrude-faceshape-intake-g17b3g).

### Layers

Open Layers in Tasks from the Design-only toolbar. Support create, rename, delete, assignment and choosing the active layer. Double-click a layer to activate it; show bold text and a check mark. Provide an eye on each row for visibility. Base is permanent and cannot be deleted or renamed; Origin stays on Base. [R03](EVIDENCE_AND_DECISIONS.md#r03)

Each independent object has one layer. A sketch and a body consuming it are separate units and may use different layers. A body's building operations stay with that body; moving its layer does not move input sketches. Selecting a body-producing operation for assignment resolves its result unit; do not require the user to manage an exposed backend Body container. New independent objects use the active layer; operations on an existing result retain its layer. [R03](EVIDENCE_AND_DECISIONS.md#r03), [current owner direction](EVIDENCE_AND_DECISIONS.md#current)

Hide/show preserves individual visibility choices and must not reveal intermediate results. Deleting a layer moves its members to Base and never deletes geometry. Deleting the active layer activates Base. Save/reopen and Undo/Redo preserve layers, assignments, visibility and active choice. [R03](EVIDENCE_AND_DECISIONS.md#r03)

### Clone

Owner direction, November 25, 2026: provide one **Clone** task for geometric objects
from direct child components, with no single-element/whole-part mode split. The
[component ownership contract](COMPONENT_PANEL.md#clone-from-direct-children--november-25-2026)
owns source depth, history-free parent geometry and child history retention.
This is the current name for the earlier Add Reference Feature prerequisite.
References to that older name elsewhere in this document retain their admission
rules but do not authorize an additional competing promotion workflow.

Proposed task for subsequent review: one geometry collector, selecting eligible
objects through a specific direct-child occurrence, preview in the edited parent's
frame, and the shared Apply/OK/Cancel pattern. No copied child feature tree and no
automatic body union. Subsequent parent features modify/combine the clone. Exact
layout, multi-selection/result grouping and source-update controls are not yet
approved. This documentation records requirements, not implemented Clone behavior.

### Move Components

#### November 25, 2026 — approved Move/Rotate/Align workflow

The owner approved implementation with “implement the move component workflow”.
The reviewed Type/Method layout supersedes the older flat Workflow control.
Native occurrence routing must use the selected active assembly, including
unused and externally owned definitions, rather than treating the file as the root.

The workflow offers **Move Components** beside the Assembly selector and
on child-instance right-click menus. The fixed active assembly and immediate
parent frame are shown above the task inputs. The active root cannot be moved.
Keep active assembly and Edit independent; collecting a child identifies the
movement owner without silently replacing either user choice.

| Type | Method | Inputs |
| --- | --- | --- |
| Move | Distance and vector | Parent X/Y/Z, picked edge/axis, two points or entered direction vector; distance and Reverse. Normalize an entered nonzero vector; its magnitude does not multiply the distance. |
| Move | Point to point | From and To references; preserve orientation. |
| Move | Dynamic drag | Translation arrows/planes, editable/resettable pivot, numeric active-handle distance and optional snapping. |
| Rotate | Axis and angle | Parent/picked/two-point axis, pivot, angle and Reverse. |
| Rotate | Dynamic drag | Rotation rings, editable/resettable pivot, numeric active-handle angle and optional snapping. |
| Align | Axes | Source/target axes, Coincident or Parallel, Reverse target. |
| Align | Coordinate systems | Source/target frames; expandable origin/Z/X reference definitions. |

One Components collector supports tree/view picking, Remove/Delete/Clear and
Keep selection after Apply. One operation accepts siblings with a common parent
occurrence. Moving an assembly instance carries its descendants; moving children
inside a shared parent definition affects every occurrence of that parent.
References are transformed into the immediate parent's frame. The active
assembly supplies the fixed outer frame. Neither root switching nor pivot
editing rewrites geometry or saved placements.

Retain the established Apply/OK/Cancel and one-Undo group movement contract below.
Automatic preview updates after a numeric field is committed, with an explicit
Update preview option. Drag release keeps a pending preview; Escape cancels the
current drag. Invalid, constrained, expression-driven or read-only selections
must explain the blocker and disable Apply/OK; never silently detach constraints
or move only an unexpected subset. Solver-driven movement of partially constrained
components is outside this initial proposal; edit the constraint instead.

The owner approved the proposal directly in chat; companion approval state was not
changed on the owner's behalf. Earlier screenshots remain UI-only proposal evidence.
Current source and native validation are recorded in
[implementation evidence](../evidence/move-components-20261125/README.md), separately
from the [proposal](../evidence/move-components-proposal-20261125/README.md) and
[archive findings](../ARCHIVE_REFERENCE.md#move-components-review--november-25-2026).
The older detailed requirements below remain applicable where consistent with this
approved workflow. Pivot-only relocation uses Move / Dynamic drag; Rotate lets the
user pick/reset a rotation pivot without relocating components.

#### Established requirements and implementation boundary

Scope: this is an operation task, separate from Component Panel implementation.
Its Part Tree right-click entry is a convenient access point. The owner explicitly
clarified that Point to Point and the other movement workflows must not be treated
as panel work or required to finish Group 1. Confirmed workflow requirements below
remain valid for separately scoped operation implementation.

Implementation boundary: the November 25 implementation supplies the complete approved Type/Method workflow. The technical contract, WORK_STATE and linked evidence own native acceptance; the earlier G1.6c3/G1.6c4 entries are historical checkpoints.

This is one task panel for whole linked **component instances**, including descendants. Copy is performed separately through Part Tree Copy/Paste. Use the approved **Type** and **Method** controls above, followed by the Components collector with Remove/Delete and Clear. This supersedes the earlier flat Workflow order. [R03](EVIDENCE_AND_DECISIONS.md#r03)

The first movable instance establishes its immediate parent as the movement owner; accept only siblings under that exact parent occurrence. Preserve the independent active assembly and Edit choices. Listed children carry their descendants implicitly. Several siblings move as one rigid group. A parent definition owns its children's relative placements: moving them changes corresponding children in every instance of that parent. Visible geometry may supply a reference only when eligible under the newer [Part Type rules](COMPONENT_PANEL.md#part-type-and-visibility): raw Reference or Excluded geometry cannot be used; Add Reference Feature must precede use of Reference geometry. [C10/U069](EVIDENCE_AND_DECISIONS.md#c10) Resulting placement stays relative to the parent. Do not introduce global/local mode switches or individual child frames. [R03](EVIDENCE_AND_DECISIONS.md#r03)

Provide **Apply, OK, Cancel**. Preview does not commit geometry or placement. Apply commits one undoable group movement, keeps the task open and resets movement inputs. With Persistent Selection on, retain the component list; off clears it. OK applies pending movement and closes; after Apply it only closes. Cancel discards the pending preview but leaves earlier applied moves available through Undo. A no-op creates no Undo entry. Switching methods discards uncommitted movement inputs while retaining eligible siblings and context. Explain invalid selections inline; do not move an unexpected subset. [R03](EVIDENCE_AND_DECISIONS.md#r03)

| Method | Fields and reference choices | Interaction and reset |
| --- | --- | --- |
| Translate | Parent X/Y/Z or straight visible line/edge/axis; nonnegative Distance; Reverse | One direction and distance, not XYZ displacement fields. Apply clears direction, zeros distance and turns Reverse off. |
| Rotate | Parent axis through its origin, picked located line/axis, or two points; optional pivot; angle magnitude; Reverse | Positive follows the displayed axis/right-hand rule. Rotate both positions and orientations about the common pivot. Apply clears axis/pivot/angle and Reverse. |
| Point to Point | Separate Source and Destination point collectors; vertices, sketch/reference points, origins or well-defined centers | Pure translation; keep orientation. Source may be outside moved set. Coincident points are a no-op. Clear both references on Apply. |
| Align Axes | Source/Target line, reference, circular or cylindrical axes; Make Parallel / Make Coincident; Reverse Target Direction | Default Coincident maps source anchor to closest target-axis point. Parallel preserves source anchor. Use minimal rotation; no arbitrary axial slide or hidden roll. Reset picks and method defaults after Apply. |
| Align Coordinate Systems | Source and Target frames; existing origins/datums, Parent frame, or expandable Origin/Z/X definitions | Align origin and all axes including roll. Reject degenerate, reflected or scaled frames. Show triads, not matrices. Clear frame inputs on Apply. |
| Interactive | Translation arrows and plane handles, rotation rings, Move Components / Edit Pivot, Reset Pivot, numeric active-handle input, optional snapping | Parent-aligned group-center pivot initially. Pivot editing alone changes no geometry or Undo. Drag release leaves pending preview. Escape cancels the current drag before broader selection handling. Apply commits composed movement and resets/recenters the pivot for retained selection. |

References are snapshots for a one-time placement edit, not new joints or associative features. Respect constrained/read-only instances. Preview must remain stable as references on moving objects are picked. Preserve camera interaction and clean up handles and capture on task/mode/document exit. [R03 and adopted prompts 4–9](EVIDENCE_AND_DECISIONS.md#r03)

The owner explicitly allowed extrapolation **within the remaining Move Components workflows**. That permission does not authorize extrapolating other operation dialogs. The detailed adopted prompts are source evidence, not a queue to run again.

### Operation coverage and unconfirmed workflows

Every original toolbar command remains cataloged in [Toolbars and Buttons](TOOLBARS_AND_BUTTONS.md#section-3-combined-button-catalog-by-original-workbench). Unless a confirmed change appears here, its original upstream workflow is retained as the baseline; this does not approve the fork's later custom editor. Task fields not yet defined must remain explicitly unspecified.

The following transferred DOCX material covers New Component, Coordinate System/Plane/Axis/Point, New Sketch/attachment, Extrude, Revolve, Loft, Pipe, Helix, Primitive, Pattern, native dress-ups/transformations and CAM. Do not infer a new custom workflow for placeholders such as New Group or Variable Set. Sketch Freedom and Constraint Repair, Interactive Feature Handles, and Broken Reference Repair were explicitly deferred in the recovered discussion; their appearance in an old roadmap or implementation is not approval. [R03](EVIDENCE_AND_DECISIONS.md#r03)

## Transferred DOCX requirements — Needs owner confirmation

The following source candidates are not instructions to implement. Exact values, added restrictions and implementation-derived details need owner confirmation. D numbers identify the archived DOCX paragraphs; [the coverage record](archive/2026-10-10/docx-coverage.json) accounts for every source block. Confirmed rules above override conflicting candidate wording. Implementation reports remain archival only.

### Shared modeling task sections

**D2668 — Needs owner confirmation:** Combine the specified additive and subtractive Part Design operations into shared feature workflows. Preserve their native parameters and the additional fields specified here. A change in icon, toolbar grouping or task layout must not silently remove a required field or choice.

**D2669 — Needs owner confirmation:** Use the same task pane for creating and editing a feature.

**D2670 — Needs owner confirmation:** Section 1: Main Parameters, expanded by default.

**D2671 — Needs owner confirmation:** Boolean choice: New Body, Add or Subtract. Show the target Body selector for Add and Subtract only; the selected target remains a background result object.

**D2672 — Needs owner confirmation:** Profile selection: Whole Sketch or Selected Curves, with a list of the selected curves.

**D2673 — Needs owner confirmation:** Keep Mode and Type as separate fields: Mode controls sidedness; Type controls the extent or termination.

**D2674 — Needs owner confirmation:** Section 2: Dimensions, expanded by default.

**D2675 — Needs owner confirmation:** Retain the applicable direction selector, sketch-normal default, length and reverse-direction arrow buttons.

**D2676 — Needs owner confirmation:** Retain Offset and the other dimensions native to the selected operation, including taper or angular fields where applicable.

**D2677 — Needs owner confirmation:** Section 3: Advanced/Optional, collapsed by default. Keep applicable native controls available rather than deleting them to simplify the main section.

**D2678 — Needs owner confirmation:** Section 4: Preview, expanded by default.

**D2679 — Needs owner confirmation:** Retain Recompute on Change and the preview choices None, Overlay and Result. Overlay is the default.

**D2680 — Needs owner confirmation:** Overlay colors: blue for New Body, green for Add and red for Subtract. Show the full tool even without a target or Boolean intersection.

**D2681 — Needs owner confirmation:** Keep preview behavior consistent when fields, profile selection, direction or termination change.

### Common actions

**D2684 — Needs owner confirmation:** The common toolbar retains New File, Open, Save, Save As, Undo, Redo, Recompute, Cut, Copy and Paste. New File uses the native New Document icon. Detailed command placement and the complete button descriptions are now in TOOLBARS_AND_BUTTONS.md (the original reference is archived).

### Component creation and storage

**D2686 — Needs owner confirmation:** Use the component definition/instance distinction for structure actions. Do not create both a visible definition and a linked occurrence as two assembly instances when the user requests one.

**D2689 — Needs owner confirmation:** New Component offers domestic storage in the active componentâ€™s defining file, a new external file, or an existing external file. Choose a location for a new file or select the existing file, then enter a unique component name. Creation does not place an instance in the current assembly. A new external file contains the named component beneath its pinned file row, without an extra Part001. Add Component places one linked instance under the active component.

**D2691 — Needs owner confirmation:** Name automatically added parts Part001, Part002, Part003 and so on, using the next available number.

**D2692 — Needs owner confirmation:** Deleting an instance from Part Tree leaves its definition available in Models.

**D2693 — Needs owner confirmation:** Domestic components belong to the current file. External components belong to imported files. Display a domestic name as M3 screw and an external name as M3 screw (Hardware). The qualifier is the source filename; use its path when identical filenames would be ambiguous. Names must be unique within a file, but different files may contain components with the same name.

**D2694 — Needs owner confirmation:** Import Component File adds a collapsible file group to Models without placing a component. Show all components in that file, including unused components, and nested file imports beneath its definitions. Removing the last placed instance retains the imported file in Models. A missing file remains visible with Locate Component File for recovery.

**D2697 — Needs owner confirmation:** Copy to Domestic Components creates a separate definition and copies its domestic subcomponent hierarchy. Existing external child definitions remain shared. Prompt with a checklist of placements in the domestic file to replace; leave all unchecked by default. Cancel keeps the new copy and leaves placements unchanged. Preserve placement positions when replacing. Explain any downstream reference or display override that must be repaired before replacement.

**D2698 — Needs owner confirmation:** Copy to External File creates an independent file definition and retains the original definition and its placements. Do not offer an identity-preserving move between domestic and external storage. Editing a copied definition does not change the original definition. The destination file places the copied component beneath its pinned file row, without creating an extra Part001.

### Coordinate System and Datum Plane

**D2700 — Needs owner confirmation:** Provide a Coordinate System action in the new-file Tasks pane and as a medium Home action.

**D2701 — Needs owner confirmation:** Its dropdown offers Plane, Axis and Point.

**D2703 — Needs owner confirmation:** Make Datum Plane available from the new-file Tasks pane and within New Sketch creation.

**D2704 — Needs owner confirmation:** Section 1: Plane orientation and location. Select geometry is the default; Enter values is the alternative. The shared selection list accepts an origin/user plane, flat face, two coplanar non-collinear body edges or lines (including an origin axis with a line), three non-collinear points, or a line and an off-line point. Planar curves may participate; reject contradictory or non-coplanar geometry. An adjacent [...] menu offers XY, YZ and XZ planes. Show Under-defined, Defined or Invalid with an explanation. Enter values exposes X/Y/Z offsets and x'/y'/z' normal components, normalized on acceptance. Provide Reverse normal direction and a signed Offset distance with its own Reverse button.

**D2705 — Needs owner confirmation:** Section 2: Orientation. Use the same shared selection list for the projected X direction. Accept one body edge, line or origin axis, or two points including curve endpoints. The adjacent [...] menu offers X, Y and Z axes. Show Under-defined, Defined or Invalid. An empty list defaults to the component axis closest to the plane; break ties X, then Y, then Z. Project the chosen direction onto the plane; reject a zero projection. Provide Reverse direction for +X versus -X; derive Y to keep a right-handed frame.

**D2706 — Needs owner confirmation:** Section 3: Origin selection. A single-item selection textbox defaults to the part origin projected onto the plane. Clicking the field activates picking of an origin, point or curve endpoint. Project the selected point onto the plane. Delete clears the reference and restores the default.

**D2707 — Needs owner confirmation:** Section 4: Preview. Preview enables a translucent purple plane overlay; Recompute on update controls automatic updates. Both checkboxes default on. The overlay creates no document object and cannot intercept selections. When automatic updates are off, toggling Preview off/on refreshes it; OK always validates and recomputes the saved plane.

**D2708 — Needs owner confirmation:** A plane created while preparing a sketch becomes an available sketch attachment in the same workflow.

**D2835 — Needs owner confirmation:** Datum-plane create/edit uses the four sections specified above from the standalone Plus Plane action, native Datum Plane command in a component document, and component History editing. Both geometry lists reuse the modeling curve collector with broader reference filters, latest-item highlighting, repeat-click deselection, Remove/Clear and Delete. Plane inputs accept faces, planes, axes, edges, curves and points; orientation accepts edges, axes and points. Retain associative native dependencies, Undo/Redo, save/reopen, public PartDesign plane identity and hidden-helper cleanup. Opening older planes preserves their frame; legacy arbitrary rotations are retained as explicit values with stored origin and X direction. Existing sketch attachment and embedded Create Datum Plane behavior remain available. All task forms inherit Qt and active-theme colors. Prohibit task-level stylesheets that force foreground/background palette colors across child widgets, and copied form palettes that freeze colors. Preserve native dropdown, disabled-text and live theme handling; ribbon colors refresh with palette changes. Keep origin axes and planes small normally; show axes, planes and the origin point at twice normal size during plane and sketch placement editors, then restore prior size and visibility. Use a narrow task panel with vertical scrolling only.

### Other structure actions

**D2710 — Needs owner confirmation:** Keep Axis available from the Coordinate System dropdown. No additional task-field changes have been specified.

**D2712 — Needs owner confirmation:** Keep Point available from the Coordinate System dropdown. No additional task-field changes have been specified.

**D2714 — Needs owner confirmation:** No additional New Group changes are specified.

**D2716 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2718 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2720 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2722 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2724 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2726 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2728 — Needs owner confirmation:** No additional Variable Set changes are specified.

### New Sketch and attachments

**D2732 — Needs owner confirmation:** Open a sketch creation task without requiring a Body or attachment to another object.

**D2733 — Needs owner confirmation:** Show the origin XY, XZ and YZ planes when New Sketch is clicked. Clicking a plane selects and highlights only that plane and updates the task selector. Keep the other planes visible without selecting the whole Origin container. Retain temporary visibility restoration on Cancel and Base layer hiding of individual datums.

**D2734 — Needs owner confirmation:** Choose an origin plane, an existing user-created plane, one planar body face, two coplanar edges of one body, or Independent plane. Independent plane defines the sketch origin X, Y and Z and its orientation with rotation angles or explicit in-plane and normal directions, in component coordinates. Creating a separate datum plane remains available.

**D2735 — Needs owner confirmation:** Retain the plane selector and Offset field. Follow support is enabled by default; turn it off to copy the selected frame once without an attachment. Independent plane has no support. Reject collinear or non-coplanar edge pairs that do not define one flat plane.

**D2736 — Needs owner confirmation:** On OK, close the creation task before opening Sketcher. Do not show the prompt that another task dialog is already open.

**D2737 — Needs owner confirmation:** Retain New Sketch, Attach Sketch and Edit Sketch actions. For a body face, two-edge or user-plane attachment, save the last valid support plane location and orientation and the sketch origin and axes. Follow valid support movement. If the support is deleted, missing or unavailable because of an upstream error, keep the sketch at exactly its last valid frame and allow editing and downstream modeling. Resume following when the same support is repaired or restored by Undo; never attach to an unrelated replacement with the same name. Preserve the frame and support references through save/reopen.

**D2738 — Needs owner confirmation:** In Sketcher, retain active and reference curves, active and reference dimensions, and geometric constraints.

**D2739 — Needs owner confirmation:** Use Sketch001 for the first sketch in each component, independently of sketches in other components.

### Extrude

**D2741 — Needs owner confirmation:** The following sections capture the specified shared modeling workflows and the fields that must remain available.

**D2743 — Needs owner confirmation:** Combine Classic Pad and Pocket into Extrude, using the Pad icon. Classic Pad opens Add; Classic Pocket opens Subtract.

**D2744 — Needs owner confirmation:** Section 1: Main Parameters.

**D2745 — Needs owner confirmation:** Boolean: New Body, Add or Subtract; target Body selector for Add and Subtract only.

**D2746 — Needs owner confirmation:** Profile choice: Whole Sketch or Selected Curves. List all chosen curves in the task pane and allow a subset of a sketch.

**D2747 — Needs owner confirmation:** Selected curves must belong to the same sketch and form closed, non-self-intersecting boundaries.

**D2748 — Needs owner confirmation:** Require one connected region, with optional holes. Separate disconnected regions are not accepted as one extrusion.

**D2749 — Needs owner confirmation:** Clicking the area between two sets of closed curves in the viewport adds both boundary sets to the selected-curves list.

**D2750 — Needs owner confirmation:** Mode: One Sided, Two Sided and Symmetric. Preserve the familiar one-dimension, two-dimension and symmetric choices.

**D2751 — Needs owner confirmation:** Type: Dimension, To Last, To First, Up to Face/Surface and Up to Shape, with the native termination choices applicable to the operation retained.

**D2752 — Needs owner confirmation:** Section 2: Dimensions.

**D2753 — Needs owner confirmation:** Direction defaults to Sketch Normal; retain direction selection and reverse arrow buttons.

**D2754 — Needs owner confirmation:** Retain Length, the second length for Two Sided mode, Taper Angle and Offset, with the applicable termination reference fields.

**D2755 — Needs owner confirmation:** Section 3: Advanced/Optional. Keep applicable native Extrude settings available.

**D2756 — Needs owner confirmation:** Section 4: Preview.

**D2757 — Needs owner confirmation:** Retain Recompute on Change and None, Overlay and Result; default to Overlay.

**D2758 — Needs owner confirmation:** Show blue New Body, green Add and red Subtract preview volumes.

**D2759 — Needs owner confirmation:** Document window interaction.

**D2760 — Needs owner confirmation:** Show the selected preview and allow the specified handles to change Length and Taper Angle.

**D2761 — Needs owner confirmation:** Keep the background Body attached to its parent Extrude. Do not permit independent pane deletion to leave a visible orphaned solid.

### Revolve

**D2763 — Needs owner confirmation:** Combine Revolve and Groove into a shared additive/subtractive revolve workflow.

**D2764 — Needs owner confirmation:** Use the common task sections, preserving the native axis, angular extent, direction, target and termination fields applicable to the operation.

**D2765 — Needs owner confirmation:** Keep the colored Add/Subtract preview and the applicable native fields when changing the toolbar presentation. Additional angular-field changes are not specified here.

**D2836 — Needs owner confirmation:** Unified Revolve: Plus combines additive Revolution and subtractive Groove in one Tasks workflow for both creation and history editing. Main parameters, Dimensions, Advanced and Preview are collapsible sections. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, a target body shown only for Add or Subtract, a whole-sketch or selected-curves list, One angle / Two angles / Symmetric mode and native applicable extent types.

**D2837 — Needs owner confirmation:** Dimensions retains sketch vertical or horizontal axes and picked local axis references, angle values with synchronized direction arrows, and signed angular offsets from -360 through +360 degrees with an offset-flip arrow. Symmetric disables direction reversal. Entering a nonzero offset selects Offset automatically. Reference starts, first/last or surface termination, axis projection and refinement remain available where applicable. The rotational axis replaces the extrusion-only sketch-normal direction and angle replaces linear length.

**D2838 — Needs owner confirmation:** Preview offers Recompute on change, enabled by default, and None, Overlay or Result; Overlay is the default and uses blue for New Body, green for Add and red for Subtract. Cancel restores visibility and removes preview geometry. Native Revolution and Groove features retain geometry semantics. Type-changing edits preserve the component operation identity and published result references through undo/redo and save/reopen. Expression-driven definitions remain protected from task overwrites and can be edited through their native properties.

### Loft

**D2767 — Needs owner confirmation:** Combine Additive Loft and Subtractive Loft into the shared Loft workflow.

**D2768 — Needs owner confirmation:** Preserve the native section selection and applicable Loft fields, together with the common Boolean, target and preview controls.

**D2839 — Needs owner confirmation:** Unified Loft: Plus combines Additive Loft and Subtractive Loft in one component Tasks workflow for creation and History editing. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters has New Body, Add or Subtract, a target shown only for Add or Subtract, ordered sections, and Smooth or Ruled interpolation. Sections accept whole profiles, selected closed sketch regions with optional holes, or native end vertices. Retain ordered preselection and empty startup. Provide append, replace, remove, clear and section inspection.

**D2840 — Needs owner confirmation:** Loft Dimensions provides Move up, Move down and Reverse order. Section placements define the span; extrusion lengths, angular extents and offsets do not apply. Advanced retains Closed, Refine and Fuzzy tolerance: zero uses the native default; negative values request automatic tolerance. Preview has Recompute on change enabled and None, Overlay or Result. Default Overlay is blue for New Body, green for Add and red for Subtract. Cancel removes previews and restores visibility. Retain native geometry, associative sections and component result identities through edits, Boolean mode changes, undo/redo and save/reopen. Reject invalid or ineffective Booleans and protect expression-driven definitions from task overwrites.

### Helix

**D2770 — Needs owner confirmation:** Combine Additive Helix and Subtractive Helix into the shared Helix workflow.

**D2771 — Needs owner confirmation:** Preserve the native Helix geometry and dimension fields and the common Boolean, target and preview controls.

**D2845 — Needs owner confirmation:** Unified Helix: Plus combines Additive Helix and Subtractive Helix in one Tasks workflow for creation and History editing, with one Helix ribbon button and no additive/subtractive dropdown. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, an explicit target only for Add or Subtract, whole-profile or selected closed sketch-curve collection, and the four native modes Pitch-Height-Angle, Pitch-Turns-Angle, Height-Turns-Angle and Height-Turns-Growth. Helix has no independent sidedness or extent Type. Retain empty startup, preselection and curve add/remove/clear controls.

**D2846 — Needs owner confirmation:** Helix Dimensions retains sketch vertical (default), horizontal, normal and construction axes, direct component X/Y/Z choices, and picked or typed datum/origin/straight-edge/circular-edge axes. Show the selected mode's pitch, height, turns, cone angle or radial growth fields; derive dependent values when changing modes. Preserve the separate axial reverse arrow and Left handed choice. Suggest pitch and height from the profile uses the native bounds heuristic, also applied to initial preselection. Without a profile, defaults are pitch 10 mm, height 30 mm, 3 turns and zero angle/growth. Height-Turns-Growth supports native flat spirals. Advanced retains Subtraction/Common, Refine, fusion tolerance factor (default 0.1) and Fuzzy tolerance; the fusion factor is not a length. Do not invent extrusion-only length offsets or termination choices.

**D2847 — Needs owner confirmation:** Helix Preview retains Recompute on change enabled and None/Overlay/Result, default Overlay with blue/green/red for New Body/Add/Subtract. Cancel restores visibility. Preserve native geometry, associative references, component operation and published result identities, downstream consumers, undo/redo and save/reopen. Invalid geometry, stale/cyclic inputs and ineffective Booleans cannot be accepted; failed edits roll back and expressions remain protected.

### Primitive

**D2773 — Needs owner confirmation:** Combine additive and subtractive primitives into the shared Primitive workflow.

**D2774 — Needs owner confirmation:** Preserve the selected primitive type and its native dimensions, with the common Boolean, target and preview controls.

**D2848 — Needs owner confirmation:** Unified Primitive: Plus combines Additive and Subtractive Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism and Wedge into one creation and History editing task. Modeling retains one Primitive action and the Primitives dropdown presets a shape in the same task. Classic documents retain native Body tasks. Tab remains disabled because no native Tab feature exists. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters contains New Body, Add or Subtract, an explicit target only for Add or Subtract, and the shape selector. No sketch profile is required.

**D2849 — Needs owner confirmation:** Primitive Dimensions preserves every native shape property and default, including cylinder/prism X and Y skew, prism sides, angular limits and all ten wedge bounds. Shape switches retain the drafts dimensions during the task. Advanced retains the native attachment modes, ordered references with Add selected, Remove and Clear, reversal, path parameter and offset. Unattached primitives expose component-local XYZ and yaw/pitch/roll; attached primitives expose their offset. Defaults are Box, unattached, zero placement, Refine enabled and fuzzy tolerance zero. Subtract retains Subtraction or Common. Native attachment and dimension properties remain associative and editable.

**D2850 — Needs owner confirmation:** Primitive Preview uses Recompute on change enabled and None, Overlay or Result, default Overlay, with blue/green/red for New Body/Add/Subtract. Cancel restores display state. Shape or mode changes preserve operation and published-result identity, downstream consumers and History order. Native geometry, attachments, undo/redo and save/reopen remain intact; invalid solids, ineffective Booleans, stale/cyclic inputs and expressions are guarded.

### Dress-ups and transformations

**D2776 — Superseded placement:** The October 6 owner outline places Delete Face/Defeaturing in Other. The older DOCX Dress-Up placement is superseded; see [Modeling tab](TOOLBARS_AND_BUTTONS.md#confirmed-design-modeling-tab).

**D2778 — Needs owner confirmation:** Keep Part Design transformation operations in the Modeling Transformation group.

**D2779 — Needs owner confirmation:** Pattern editing must show individual instance suppression controls immediately on opening. Suppress or restore a selected copy without losing direction, reference collectors or the shared Linear/Circular settings; accepting with live preview disabled must still apply the final parameters. MultiTransform supports Circular, Path and Point Pattern entries and opens the matching native parameter editor. Preserve the Plus unified Pattern entry and its existing ribbon groups.

### Inherited workbench workflows

**D2781 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2783 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2785 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2787 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2789 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2791 — Needs owner confirmation:** Preserve the existing CAM workflows while applying the inherited controls and behavior below.

**D2792 — Needs owner confirmation:** CAM operations and dress-ups use the selected work plane origin and orientation consistently in preview, inspection and post-processing. Avoid Faces keeps the selected regions protected with the corrected Safe STL clearance. Missing or invalid inputs must clear the generated toolpath and report the failure, including failed holding-tag generation and probe-map points outside the valid area. The CAM Job preferences include the Sanity report output-file setting; Mill Facing offers Circular clearing, and Simple Copy opens its native task.

### Idle actions after New File

**D2799 — Superseded November 22, 2026:** The approved Design idle actions above are New Sketch, Datum Plane, Datum Line and Datum Point.

### Pipe

**D2842 — Needs owner confirmation:** Unified Pipe: Plus combines Additive Pipe and Subtractive Pipe in one component Tasks workflow for creation and History editing, with one Pipe button after Loft in Modeling. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, a target only for Add or Subtract, ordered whole-profile or selected closed sketch-curve sections, append/replace/remove/clear, Constant or Multisection mode, and Transformed/Right corner/Round corner transition type. Constant retains additional sections for later Multisection use. Allow empty startup and ordered profile/path/section preselection.

**D2843 — Needs owner confirmation:** Pipe Dimensions collects the sweep path as a whole curve object or selected edges from one local object, with pick/remove/clear controls and section reordering. Path geometry and section placements define length and direction; extrusion lengths and offsets do not apply. Advanced retains Standard/Fixed/Frenet/Auxiliary/Binormal orientation, a separate auxiliary-path collector, curvilinear equivalence, binormal XYZ, native Subtraction/Common, Refine and Fuzzy tolerance. Preserve inactive options and stored tangent flags; native tangent expansion and Linear/S-shape/Interpolation scaling laws are not implemented. The inherited Pipe engine requires closed sections and cannot accept point-ended sections; report this clearly. Preserve native orientation and corner semantics.

**D2844 — Needs owner confirmation:** Pipe Preview retains Recompute on change enabled, None/Overlay/Result, and default Overlay colors blue/green/red for New Body/Add/Subtract. Cancel restores visibility. Preserve native associative profile/path links, component operation and result identities, downstream references, undo/redo and save/reopen through edits and Boolean type changes. Reject invalid, stale or cyclic inputs and ineffective Booleans atomically; protect expressions.

### Shared selection, preview, deletion and compact layout

**D2853 — Needs owner confirmation:** Deleting an Extrude must preserve its source sketch, remove unused internal profile helpers and make the sketch available again when no other operation consumes it. Both edge and region selection must support creating another Extrude. Delete, Undo and Redo retain geometry and visibility consistently; shared inputs remain protected.

**D2854 — Needs owner confirmation:** Compact Tasks panels: component Extrude, Revolve, Loft, Pipe, Helix, Primitive and Sketch/Datum Plane forms must remain usable in a narrow panel. Use vertical scrolling when the controls exceed the available height; do not require horizontal scrolling. Labels wrap above fields when space is limited. Long object names and attachment descriptions must not force the panel wider; dropdowns and curve lists retain full text in tooltips. Arrange vector components vertically, group collection buttons in short rows, and retain usable reference entry fields with Pick/Clear below them. Preserve all field values, native units, section defaults and create/edit/preview behavior.

**D2855 — Needs owner confirmation:** Narrow-panel acceptance covers a 360 logical-pixel Tasks dock with all applicable sections expanded, two-sided Extrude and custom direction, Primitive Wedge dimensions and attachment, and Sketch axis directions. Every displayed field must remain horizontally within the viewport and reachable by vertical scrolling. Retain the native task scroller and OK/Cancel controls.

**D2859 — Needs owner confirmation:** Component operation entry: starting Extrude or another component operation automatically displays the active component's History tab as its creation task opens. This applies to the shared Sketch, Extrude, Revolve, Loft, Pipe, Helix and Primitive workflows, including entry from Models or Part Tree. If the Components panel is hidden, reveal it. Preserve profile preselection, the active component and occurrence context, and return to the original component view on OK or Cancel. History editing continues to use the same task.

**D2860 — Needs owner confirmation:** Curve-list interaction: in every shared component modeling curve collector, highlight and scroll to the most recently picked curve in the task list. Picking a collected curve again removes it and leaves no row highlighted. Give the curve list keyboard focus after a viewport pick so Delete removes its highlighted entries immediately; Delete with no highlighted entries does nothing and never deletes the source sketch. Apply the same behavior to Extrude, Revolve, Helix, Loft and Pipe profile curves and Pipe sweep/auxiliary path edges. Remove the redundant Add selected curves, Add selected and Use selected capture buttons; retain automatic collection, preselection, Remove, Clear, Use all/Use whole and the explicit Pipe path-role picker. Region picking continues to collect the complete boundary and highlights its last collected entry. Keep persistent viewport emphasis for the remaining collected curves, preview validation and OK/Cancel restoration.

**D2862 — Needs owner confirmation:** Modeling preview types: Extrude, Revolve, Loft, Pipe, Helix and Primitive use a dropdown with None, Overlay (default) and Result. Automatic updates remain enabled by default. Once the required closed profile and other geometric inputs are complete, Overlay shows the full native tool in blue for New Body, green for Add or red for Subtract. Add/Subtract overlays do not require a target or Boolean intersection and are not clipped to the target: a 5-inch subtract extrusion remains 5 inches long through a 1-inch body. Reference-defined extents still require their geometric references. Result shows the evaluated final geometry in normal body appearance without operation colors; it requires valid targets and a valid result. None removes the preview. Switching types, failed previews and Cancel restore prior visibility and transparency; collected curves retain their task highlights. OK continues to validate the actual operation and preserve native geometry, undo and persistence.

### Layers details

**D2872 — Needs owner confirmation:** Design Layers: Each document has permanent Base and exactly one active layer, initially Base. Base cannot be renamed or deleted. Origin and origin features always belong to Base. New independent model objects take the active layer; missing or foreign assignments in an existing document migrate to Base. Layer IDs, labels, visibility, active choice and assignments are native saved properties, with undo/redo. Layer metadata has NoRecompute semantics and introduces no document dependency links.

**D2873 — Needs owner confirmation:** Design Layers: A sketch is indivisible and remains independent of every body that consumes it, including a sketch nested in a native Body. A Body and its building operations share a layer. Native Body membership and explicit Plus Producer/ConsumedResults relationships define the body unit; arbitrary dependency recursion is forbidden. Selecting several operations of one body resolves to one assignment owner. Sketch selection moves only that sketch. New operations inherit their existing body's layer. Same-document occurrences resolve the shared definition's model objects; external definitions are edited in their owning document, not implicitly reparented.

**D2875 — Needs owner confirmation:** Design Layers: The task panel creates, renames, deletes, assigns and activates layers. Double-click a layer to activate it; active text is bold with a check. An eye control toggles each row's visibility. Layer hiding gates scene geometry without changing individual Visibility properties or taking snapshots. Hidden intermediate results remain hidden, individual changes while hidden are respected, and independently layered sketches remain traversable in the Body's native Group display. Native container Visibility and native Through/Tip display choices continue to govern their own scene traversal. Delete moves assignments to Base, never deletes geometry, and activates Base when the deleted layer was active. Changes are individually undoable from the task panel.

### Movement details and historical constraints

**D2881 — Needs owner confirmation:** Move Components: Move Components opens one Tasks panel from Design Assembly or the Part Tree instance context menu. It moves whole linked component instances and their descendants. Models, permanent master/root contexts and geometry subelements are not movable instances. Copy remains a separate Part Tree operation. The first field is Workflow, ordered Translate, Rotate, Point to Point, Align Axes, Align Coordinate Systems, Interactive.

The permanent-master wording is superseded by C09’s pinned file container and ordinary Part001.

**D2882 — Needs owner confirmation:** Move Components: The next control is the Components list, using the existing add-selection, Remove/Delete and Clear collector conventions. The first valid batch establishes the immediate parent definition and its exact displayed occurrence path as the active editing context. Only direct siblings under that same displayed parent are accepted; mixed batches are rejected in full with inline explanation. Descendants are implicit and receive no second placement change. Clearing the list retains the parent context. Ordinary component clicks outside the task do not activate parents. External parent definitions must be opened in their owning file.

**D2883 — Needs owner confirmation:** Move Components: A parent definition owns its children's relative LinkPlacement values. Moving children changes them in every occurrence of that parent, including its standalone component tab. Preserve the selected parent occurrence path for reference conversion; do not create a display-path placement override, reparent links, copy definitions or change source shapes/history. The task displays this shared-parent consequence. Driven, read-only, grounded and relationship-owned instances are refused, including native assembly joint references that traverse a root plus a deep subpath.

**D2884 — Needs owner confirmation:** Move Components: Translate uses one normalized direction, one nonnegative unit-aware Distance and a Reverse toggle, initially direction unset, zero length and Reverse off. Directions are Parent X, Parent Y, Parent Z or a picked straight edge, line/reference axis from visible geometry. Picked occurrence/world vectors transform by the inverse parent rotation only; parent translation does not affect a direction. Reject curved, undefined, zero or ambiguous bare shared references. Snapshot the direction without adding associative dependencies. All selected siblings receive the same parent-frame rigid transform. Reverse changes sign while retaining Distance.

**D2885 — Needs owner confirmation:** Move Components: Teal, non-pickable geometry previews intended placements without writing document properties or creating document objects/undo records. Show the effects in every displayed occurrence of the shared parent, using each occurrence's native frame. Apply commits all siblings in one transaction and keeps the panel open. It resets Direction, Distance and Reverse; Persistent Selection on retains the list/highlights, off clears both. No-op Apply creates no undo record. OK applies a valid nonzero pending move and closes; after Apply it simply closes. Cancel discards only the pending preview, retaining earlier Apply transactions for Undo. Switching workflows discards uncommitted parameters/preview while retaining siblings and parent context.

**D2886 — Needs owner confirmation:** Move Components: Errors remain inline in the task. A changed parent or selected placement invalidates the pending preview and requires Reset movement inputs; stale placements are never silently applied. Selection changes and removals reset movement inputs. Close the task and release observers/preview on document or component-view exit; deleted instances leave the list, and deletion of the parent context closes the task.

**D2887 — Needs owner confirmation:** Move Components: Rotate uses Parent X/Y/Z through the parent origin, a picked straight line with its location and direction, or two distinct points. An optional picked pivot relocates a parallel axis. Vertex, native sketch/reference point, origin and analytic circle center picks retain their displayed occurrence transforms. Angle is a finite magnitude from 0 to 360 degrees; positive follows the right-hand rule and Reverse negates it. Rotate applies one common rigid delta to sibling positions and orientations. The transient preview labels the parent-frame pivot, positive axis and signed angle. Apply clears axis, pivot and angle and turns Reverse off.

**D2888 — Needs owner confirmation:** Move Components: Point to Point snapshots a Source and Destination vertex, sketch/reference point, origin or analytic circle center from any visible displayed occurrence. The Source need not belong to the moved group. Convert both to the active parent frame and translate every sibling by Destination minus Source, preserving orientations, group spacing and descendants. Show labeled points and distance with transient markers/vector; no joints, constraints or lasting references are created. Coincident points create no undo entry. Missing, invalid or deleted references prevent Apply. Apply clears both point inputs; selection follows Persistent. Reset/method switch/Cancel remove pending preview.

**D2889 — Needs owner confirmation:** Move Components: Align Axes snapshots Source and Target straight/reference axes, analytic circular axes or cylindrical-face axes through exact displayed occurrences. Default Make Coincident uses minimal-angle rotation and maps the Source anchor to its closest point on the Target axis; Make Parallel rotates about and retains the Source anchor. Reverse Target Direction explicitly negates Target. Opposite directions use Source cross the least-aligned parent X/Y/Z basis, with X winning ties, for a stable 180-degree rotation. Show resolved Source/Target direction arrows and transformed Source; all siblings receive one rigid parent-frame delta. Apply clears picks and restores Coincident/Reverse-off defaults. No joints, associations or arbitrary axial slide.

**D2890 — Needs owner confirmation:** Move Components: Align Coordinate Systems maps a complete Source rigid frame to a complete Target frame, including origin and roll, with one Target times inverse Source delta shared by siblings. Pick existing native component origins/datums, explicitly choose Parent, or expand Origin/Z/X definitions. Normalize Z, project X perpendicular to Z and derive right-handed Y. Reject zero/parallel directions and scaled, sheared, reflected or nonfinite frames. Show Source/Target triads and origins, without exposing matrices. Picks snapshot displayed occurrences against unchanged geometry; Apply clears definitions and references, and Cancel removes only pending preview.

### Legacy conversion interactions

**D2899 — Needs owner confirmation:** When a legacy file opens, Models lists its part definitions and Part Tree shows linked instances beneath the pinned file row. Repeated instances reference the same model. Review legacy conversion explains incomplete mappings, missing instances and any geometry-only recovery. Label recovered outputs as recovered geometry and explain that their parametric history has not been converted. Missing instances remain visible for repair. Save converted external parts as new .cadprt files before the parent, leaving legacy originals untouched. For supported simple Sketch and Pad histories, History lists the sketch, Pad operation and original Body result in that order, preserving their labels. Double-click the sketch to edit its constraints or Pad to open the Extrude task. Repeated instances update from the shared model. Review legacy conversion identifies histories that remain native and editable. Retained expressions use the property editor; operation and target changes reject downstream self-references and preserve the original feature identity. Legacy datum planes, axes, points and coordinate systems retain their labels and native attachment settings. Body-owned datums appear as hidden links in component History. Double-click opens the original attachment editor; Cancel preserves supports and offsets. Retained planes are available to New Sketch and follow their native offsets and frame changes. Missing or invalid datum sources show Needs repair. Origins and their planes keep their existing names and permanent controls. Retained Body-owned sketches appear as hidden links before their Body in History. Double-click edits the original sketch and its existing constraints; all consumers and repeated instances use that same sketch. Existing attachments, external references and expression-driven dimensions remain editable in their native controls. Missing or invalid sketch sources show Needs repair; repair the original input before using it.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2900 — Needs owner confirmation:** Supported legacy Pad and Pocket chains appear in History as independent sketches and Extrude operations with explicit target bodies, ending in the original Body result. Double-click a converted Pocket opens the shared Extrude task with Subtract, its existing target and the correct direction selected. Accept updates the operation; Cancel leaves its saved parameters and target unchanged. Existing expression-driven parameters remain available in the property editor. Converted Pad/Pocket modes and targets can be edited while keeping the original feature. Standalone native Part Extrusion retains New Body; create a separate operation to change its operation kind. Retained native Pad/Pocket histories appear as hidden History links; double-click opens the original native editor with its attachments and extent references intact. Missing or invalid retained operation sources show Needs repair. Supported independent Part Extrusions also open in the shared task; custom direction, taper and sheet or curve outputs retain their native controls.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2901 — Needs owner confirmation:** Supported legacy Revolution and Groove histories show their original sketches, Revolve operations, target bodies and final Body in History. Double-click opens the shared Revolve task with saved axes, angles, direction and signed start offset. Accept updates the operation; Cancel preserves saved settings. Preview follows rotated sketches and construction axes. Converted features retain their native Revolution or Groove type; create a separate operation to switch additive/subtractive type. Formulas remain editable in properties. Attached or reference-dependent histories and standalone Part Revolution retain their native editors and signed-axis controls. Missing or invalid retained sources show Needs repair. Review legacy conversion distinguishes mapped operations from retained native histories. Undo/Redo restores conversion and edits without stale component views.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2902 — Needs owner confirmation:** Supported legacy Lofts show their original section sketches before Loft operations, explicit target bodies and the final Body in History. Double-click opens the shared Loft task with sections in their saved order and existing Smooth/Ruled, Closed, Refine and tolerance settings. Preview section reorder or replacement before Accept; Cancel preserves saved sections and targets. Converted Loft modes and targets can change while keeping the original Loft. Vertex end sections retain their picks. Formula-driven settings use properties. Attached histories, native Common operations and legacy sketch-edge references that mean the whole sketch retain the original native editor. Standalone Part Loft retains its native degree, linearization and solid/sheet controls. Missing or invalid retained sources show Needs repair. Undo/Redo restores conversion and edits; repeated instances update from the shared model.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2903 — Needs owner confirmation:** Supported legacy Pipes show their original profile sections and path sketches before Pipe operations, explicit target bodies and the final Body in History. Double-click opens the shared Pipe task with saved section order, path and auxiliary edge picks, orientation, corner transition and Constant/Multisection settings. Preview changes before Accept; Cancel preserves saved references and targets. Converted Pipe modes and targets can change while keeping the original feature. Formula-driven settings use properties. Attached or unsupported histories, native Common operations and whole-sketch edge references retain the original native editor. Standalone Part Sweep retains its native solid/sheet, Frenet and linearization controls. Missing or invalid retained sources show Needs repair; unavailable selected path edges give a repair message. Review legacy conversion identifies stale outputs requiring recompute. Undo/Redo restores conversion and edits; repeated instances update from their shared model.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2904 — Needs owner confirmation:** Supported legacy Helix histories show original profiles before Helix operations, explicit targets and the final Body in History. Double-click opens the shared Helix task with saved parameter mode, pitch, height, turns, cone angle or growth, axis, handedness and direction. Preview changes before Accept; Cancel preserves saved settings and references. Converted modes and targets retain the original Helix feature. Formula-driven parameters remain editable in properties. Attached or unsupported axes and histories retain their native editors and available geometry. Standalone Part Helix retains its native curve controls. Review legacy conversion identifies unverified output requiring recompute; missing retained sources show Needs repair. Undo/Redo restores conversion and edits; repeated instances update from the shared model.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2905 — Needs owner confirmation:** Supported legacy Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism and Wedge histories show Primitive operations with explicit targets and the final Body in History. Double-click opens the shared Primitive task with the saved shape, native dimensions and placement. Preview changes before Accept; Cancel preserves saved settings. Converted Add/Subtract/New Body modes and targets retain the original primitive; create a separate operation to change its shape type. Formula-driven dimensions use properties. Attached or unsupported histories retain the original native editor. Standalone Part primitives retain their native controls. Review legacy conversion identifies stale or unavailable output; missing retained sources show Needs repair. Undo/Redo restores conversion and edits; shared instances update together.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2906 — Needs owner confirmation:** Legacy Fillet, Chamfer, Draft and Thickness operations appear in component History while retaining their native Body and selected faces or edges. Double-click opens the original native editor with saved settings. Standalone Part dress-ups retain their original controls and outputs. Missing or invalid retained sources show Needs repair; Review legacy conversion identifies unverified output requiring recompute.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2907 — Needs owner confirmation:** Legacy patterns and transformations appear in History with referenced inputs before consumers, retaining authored order where compatible. Double-click opens the native editor with saved originals, direction or axis references and transformation settings. MultiTransform preserves its ordered transformations; combined Pattern retains both Linear and Circular settings and suppressed copies. Boolean History opens the original native editor with its saved operation, target and tool Bodies. Native owners and geometry remain retained; these operations are not presented as newly flattened shared operations. Undo/Redo restores conversion and edits; saved files preserve the original model shared by repeated instances.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.


### File Open and legacy conversion

**D2908 — Needs owner confirmation:** Open legacy FCStd files through File > Open. Models contains definitions, Part Tree contains linked instances, and History shows inputs, operations and finished results. Mapped operations use the shared task; retained operations open their original native editor. Save converted content to a new cadprt file, saving external definitions before their parent. Legacy originals remain protected. Missing definitions remain visible; right-click and choose Locate Component File to repair them before saving. Review legacy conversion identifies retained native histories, unverified caches and explicit dumb geometry recovery. Geometry-only recovery preserves available output while reporting loss of parametric component editing. Repeated instances share model edits; instance placements remain independent. Conversion and geometry-only recovery both add the pinned file row, with its global Origin, above the converted domestic component. Recovered outputs belong to that component; the file has no modeling geometry. The file row is excluded from Models. One Undo reverses the entire conversion, including the file container, and Redo restores it. No additional Part001 is created.

Any exposed backend Body rows in historical conversion descriptions are superseded by the current background-Body requirement.

## Older Markdown-only workflows — Needs owner confirmation

The [separate implemented-change inventory](UNVERIFIED_IMPLEMENTED_CHANGES.md) lists these workflows individually with source evidence and review scope. It does not promote their archived details to approved requirements.

The former [UI specification](archive/2026-10-10/UI_UX_SPEC.md) retains detailed custom dialogs for Trim Body, Isocline, CAM/STL machining and holding tabs, named parameters, command search, temporary display, export, sketch support, dependency inspection, measurement, occurrence appearance, interference, sketch repair, Mirror, section planes, feature organization, Make Unique, drawing setup, document updates, mesh preparation, reusable sketches, BOM, Shape Builder, source replacement, face deviation, Select Other, thickening, CAM templates/simulation, exploded views, intersection curves, freedom guidance, dimension repair, joints, ordered Loft sections, CAM model review, state columns, Sweep, project packaging, Hole, selection filters, fillet/chamfer recovery, Trim gestures, Shell and face extension. These are preserved **only as archived candidates**; no accessible original owner message confirms their detailed custom UI. Native upstream workflows remain the baseline unless a confirmed owner requirement above changes them.

The removed [component-contract UI passages](archive/2026-10-10/superseded-passages/ai-instructions/architecture/COMPONENT_DOCUMENT_CONTRACT.md) similarly preserve proposed instance grouping, deletion/reparenting, context menus, Add Reference Object, missing-file repair and dumb conversion details. Use them to ask targeted confirmation questions, never to infer approval from implementation.

## Classic and Plus workflow presentations

Task panel (workflow) has its own Classic/Plus selector, independent of toolbars
and model/components presentation. Plus starts as a copy of the Classic workflows;
new Plus workflows are developed later. Both presentations use the same updated
component structure and operation services. Switching presentation does not cancel
or duplicate an active task. Pad/Pocket are additive/subtractive adapters to the
shared extrusion operation. Do not fork a legacy backend when building a Classic
adapter; investigate incompatibilities as they arise.

See [the October 11 owner decision](EVIDENCE_AND_DECISIONS.md#independent-classic-and-plus-ui-sections---october-11-2026) and [mode defaults](DEFAULT_SETTINGS.md#independent-ui-modes).

### Sketch dimensional constraint Enter - November 23, 2026

Approved and installed: after a valid numerical dimension, main or keypad Enter
commits once and closes the native dimension dialog, for creating and editing.
Native units/expressions, validation, Cancel/Escape, name/reference controls and
other task-panel numeric behavior are preserved. Invalid or incomplete text
stays focused with the dialog open. See the [approved preview](../evidence/dimension-enter-preview-20261123/README.md)
and [native implementation checks](../evidence/dimension-enter-20261123/README.md).

### Feature input click and Shift-click - November 23, 2026

Approved and installed: click to add/select and Shift-click to remove/deselect in feature
collectors: repeated plain clicks retain existing entries, Shift-click
on an absent entry does nothing, and curve-chain selection carries the gesture
through expansion. Apply across profile/edge/face/section/reference collectors;
preserve validation, History ordering, single-input replacement and existing list
controls. See the [approved native-list preview](../evidence/feature-pick-preview-20261123/README.md)
and [implementation acceptance](../evidence/feature-pick-20261123/README.md).

### Approved single Pattern item in Elements — November 24, 2026

Owner instructed: “also finish making the pattern show as a single item in the
elements list instead of listing all the curves”, authorizing completion of the
previously presented Elements preview. Show one non-expandable Pattern row with
the existing Pattern icon and counts for generated curves and spacing helpers.
Original inputs and unrelated geometry retain normal rows. Select the operation's
members together; retain individual viewport picking. Double-click or keyboard
activation opens the existing populated Pattern task with its approved completion
and Cancel behavior. Group visibility respects Hide spacing chain. Filters inspect
member types while retaining at most one row. Delete removes generated members and
their relationships, keeps originals, and supports Undo. Preserve equations, native
geometry identities and save/reopen. Free copies also retain their operation identity.
Use saved membership; never guess unrelated legacy curves into a group.
See [implementation and validation](../evidence/pattern-elements-20261124/README.md).

### Approved existing Sketch Pattern editor — November 24, 2026

Owner requested double-clicking either the Pattern icon in the sketch or its
constraint-list entry to reopen the populated Sketch Pattern task, then approved
the concrete workflow with “Approve and implement”. This replaces the pitch-only
popup described below. The dedicated panel restores original geometry, counts,
spacing modes/values, direction references, reverse and one/two/symmetric extents,
linear/circular and angular/radial modes, explicit units and spacing-chain choices.
The current pattern previews its replacement while pending edits leave the saved
model unchanged. Done on the left updates and closes; Apply on the right updates
and clears for another pattern; Cancel/Escape discards the pending edits.
Preserve the single nonexpandable group entry/icon, native constraints, surviving
geometry identities, Undo/Redo and save/reopen. Dependency conflicts retain the
inputs and explain what prevents the edit. Older grouped patterns may recover an
equivalent current layout where the spacing topology is unambiguous; unavailable
historical authoring choices must not be invented.
See [approval, native captures and implementation](../evidence/pattern-edit-20261124/README.md).

### Approved Pattern constraint presentation — November 24, 2026

Owner approved the concrete single-icon/list presentation in chat: “Approve this
presentation”. Each newly created sketch pattern represents all its generated
constraints with one Pattern icon in the viewer and one Pattern row in the constraint
list. There are no expandable children. Source constraints remain separate. The group
is selectable; deleting it removes its relationships while retaining geometry, and
Undo restores them. The later approved existing-pattern editor above supersedes the
initial pitch-only double-click popup and retains explicit units. Hide spacing chain hides the
helper geometry and every associated constraint graphic, including the Pattern icon;
the list entry remains available. Showing it restores one icon. Existing legacy
patterns retain their independent constraints rather than guessing membership.
See [approved screenshots and actual implementation evidence](../evidence/pattern-group-20261124/README.md).

### Approved and installed pattern/task corrections — November 24, 2026

Owner requests fields that fit narrow docks, previews for each ready direction
before all selected directions are complete, and visible preview spacing lines/arcs
unless Hide spacing chain is checked. Copied geometric sizes use Equal relationships
to the original instead of individual driving measurements. Keep source size drivers
and independent spacing drivers. For task completion Done/Apply pairs: Done is left
and applies then closes; Apply is right and applies then clears selections/references
for another operation, retaining settings. Cancel/Escape does not apply pending input.
See [the concrete workflow, simulations and implementation scope](../evidence/pattern-corrections-preview-20261124/README.md).
The owner approved the simulation with “Approved. Implement”. Functional changes are
installed in Pattern and Mirror, the audited completion pairs. Empty Done closes;
invalid or failed Done retains input. Geometry/reference selections clear after Apply,
while numeric and mode settings remain. Preview helpers never mutate the document.
Projected X/Y distances become Equal lengths only when a driving Horizontal/Vertical
constraint makes them actual lengths; otherwise endpoint spacing preserves source freedom.
See [native screenshots and final acceptance](../evidence/pattern-corrections-20261124/README.md).

### Approved spacing chains and quantity units — November 24, 2026

Owner follow-up replaces repeated pattern coordinate dimensions with connected,
equal spacing lines and confirms one driving length per independent pitch. Angular
spacing uses connected arcs; radial spacing uses connected lines. A Hide spacing
chain checkbox must hide helpers without disabling constraints or deleting geometry.
Keep independent positive/negative extents, symmetry and the existing pattern workflow.

All task dimension/value fields must support six-decimal numeric entry independently
of leader rounding, and accept/retain compatible explicitly entered units through
editing and save/reopen. Example: `1.29999 mm` displays `1.30 mm` but edits at its
full value; `0.100 in` remains `0.100 in` on the leader and in the editor even in
a millimeter document. General preferences need secondary units and their display
decimal count. Counts remain integers; preserve expressions and physical values.

[The new preference/field/chain previews and detailed contract](../evidence/spacing-units-preview-20261124/README.md)
were approved with “Approved. Implement”. The implemented persistence and native
acceptance are recorded in [spacing and units evidence](../evidence/spacing-units-20261124/README.md).

### Sketch Pattern task - approved November 24, 2026

Owner requests a dedicated geometry-first task replacing Move / Array Transform,
following Mirror's Apply/Done and task-section isolation. Linear supports one/two
directions, each with One dimension, Two dimensions (independent forward/backward
spacing and counts), or Symmetric. Circular uses the same extent options for
Angular, Radial, or Angular + radial directions. Counts include the original;
angular extents offer angular pitch or total angle. A compact click-add/Shift-remove
collector, reference pickers, reverse and optional dimensions are required.
Owner follow-up: **Create dimensions is selected by default**, creating relative
dimensions and constraints. Users can clear it to create copies without those dimensions.

The owner approved the [concrete workflow and screenshots](../evidence/sketch-pattern-preview-20261124/README.md)
in chat: "approved. implement". Each side of Two dimensions counts the original,
so its total is forward + backward - 1. Symmetric uses an odd total count around
the original; total distance/angle spans both sides. Full-circle total angle uses
360 / instances without duplicating the endpoint. Other overlapping angular
extents are invalid. Combined direction totals multiply.

Apply alone creates native geometry and optional relative dimensions, clears the
geometry list and retains parameters/references. Done, Cancel and Escape discard
pending input and restore the prior sketch sections, keeping earlier applies.
Undo/Redo clears pending input and references. Rotation centers accept points,
circle/arc centers and their radius/diameter dimensions. Radial reference defines
outward, with translation without scaling; reject inward extents reaching center.
Normal sketch axes, coordinate graphics and the separate move-only command remain.

### Compatible symmetry constraints - November 24, 2026

Owner correction: adding symmetry to an already horizontal/vertical rectangle must
not report an error merely because some symmetry equations are redundant. Retain
the rectangle's existing constraints and the symmetry constraint, including fully
constrained compatible cases. Actual contradictions must still fail validation.
Constraint creation, selection, appearance, editing and native Undo remain unchanged;
this is a solver correction within the existing workflow, with no new interface.

### Sketcher symmetric geometry task - November 23, 2026

Approved, including the owner's larger-list revision: Mirror opens its own symmetry
task while a sketch is being edited, with or without preselection. Its large,
scrollable Geometry list has a 360 logical-pixel minimum height and expands with
available space. Click adds once, Shift-click removes; Delete/Remove/Clear are
available without Select/Confirm toggles. A single-line Axis of symmetry field
collects native sketch axes, straight sketch/construction/external lines or a point
center; new valid references replace old ones, Shift-click clears a matching input.
Invalid picks retain valid references and show prominent feedback.

Apply alone creates mirrored geometry and remains open, clearing geometry while
retaining the axis for another set. Adjacent Done closes symmetry without applying
pending inputs. Previously applied sets remain. Native Delete original geometries
and Create symmetry constraints remain mutually exclusive and off by default.
No automatic dimensions are introduced; native copied constraints are preserved.

The dedicated symmetry task hides ordinary Sketch Edit, Constraints, Elements/lines
and advanced solver panels while active, restoring their prior visibility on exit.
Viewport sketch geometry remains selectable. Cancel/Escape discards pending picks
and preview; Exit Sketch retains its existing role. Undo/Redo clears pending
references so stale indices cannot be reused. A reference removed by Delete original
geometries is cleared; surviving internal references are remapped.

See the [approved native-widget preview](../evidence/sketch-symmetry-preview-20261123/README.md).
## Reference image — approved November 27, 2026

Design Tasks > Create Geometry includes Reference image for the active component.
Use one task for creation and History editing. Browse selects an image that is
embedded in the part file. Attachment is deliberately simple: select XY, XZ, YZ,
or an existing created plane in this component and enter a normal distance offset.
Do not introduce the sketch/plane-definition collector here. Free placement offers
component-local XYZ position and rotation instead of a support.

Width and height provide scaling, with aspect lock enabled initially. Two picked
image points and a known distance calibrate the size. Scaling and rotation use one
anchor: nine rectangle presets or a picked image point. Changing the anchor keeps
the image stationary; resizing and rotating keep the selected anchor stationary.
Attached images rotate within their plane; all rotation fields display two decimal
places and step by 0.01 degrees. Transparency uses a synchronized slider and percent
field. Preview is temporary; Done commits and closes, Apply commits and clears the
task to defaults for another image, and Cancel discards unapplied changes. Buttons
are below all fields. Invalid inputs retain fields and use the shared error display.

Each image appears in component History. Double-click and Edit reference image
reopen its populated task. History offers Hide/Show and Delete, with native Undo.
Images follow their attached planes after recompute and reopen. A missing plane
can be replaced in the image task without making the Components panel disappear.
