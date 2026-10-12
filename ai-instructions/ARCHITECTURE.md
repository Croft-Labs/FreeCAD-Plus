# Component/document architecture

Status: G1.6b domestic/external unused-model editing validated in the native development build, October 10, 2026.
The native service module and panel foundation are opt-in; the complete panel, broader conversion and later Group 1
behavior below remain target design until their roadmap stages are completed.
Engineering choices below implement confirmed behavior; they do not approve
DOCX candidates or restore archived Plus code. The [component specification](ui-ux-specs/COMPONENT_PANEL.md)
owns UI requirements; [the roadmap](DEVELOPMENT_ROADMAP.md#group-1--component-panel-and-document-structure)
owns implementation order and acceptance status.

## System boundaries

Reuse FreeCAD documents, native feature/property identities, geometry, solvers,
transactions and links. Introduce component ownership and presentation around
these services. Keep the original workbench inventory and geometry algorithms.
Current services cover domestic/external catalogs, component hierarchies and shared
native instances. Further legacy conversion and the full panel remain separate stages.

The Plus/Legacy interface preference and redesigned modeling dialogs are outside
this stage. Component storage must not depend on the chosen toolbar presentation.
The archived fork is reference material, not a source of implicit requirements.

## Components and data flow

| Responsibility | Target ownership / native service |
| --- | --- |
| File | One native `App::Document`; one marked file-root container represents its global frame and top-level placements |
| Definition catalog | File-owned definitions, including unused ones; nested native imported-file catalogs |
| Component definition | Native `App::Part`, proven by the pilot, owns modeling content and child placements and can serve as part and assembly simultaneously |
| Placed instance | Native `App::Link` targets a definition; root instances belong to the file, child instances to their parent definition |
| Modeling content | Existing sketches, Part/PartDesign operations, geometry and required backend Bodies retain their native types and relationships |
| Component panel | Models, Part Tree and History are projections of the document model; tree rows do not own or duplicate geometry |
| Edit context | Per-view/tab selection of defining component and occurrence path, separate from ordinary selection and saved model identity |
| Persistence adapter | Native FreeCAD document serialization plus explicitly versioned component metadata; validated `.cadprt` open/save entry points |

The tests prove the `App::Part`/`App::Link` mapping for nested domestic definitions
and repeated parents. Stored definitions are hidden; placed links render the
instances without additional visible definition geometry. Broader command integration remains deferred. Backend grouping must not
introduce dependency cycles or silently change placement transforms.

## Data model and lifecycle

### Ownership and identity

- The file root owns the fixed global Origin/planes and root placements. It is not
  a component definition, and cannot own sketches or modeling features.
- A definition belongs to exactly one defining file. Modeling objects belong to
  exactly one component at the logical ownership level; their native Body/group
  relationships remain intact. More than one backend Body is allowed where needed.
- A child placement is owned by its parent definition. Its local transform is
  shared by all occurrences of that parent; it is not duplicated per visible row.
  World transforms are composed along the selected occurrence path.
- Use persistent, file-qualified identities independent of displayed labels.
  Reuse native document/object identity where it is stable; add persistent IDs
  only where the pilot demonstrates a missing identity. Store native links for
  native dependencies, not label-based lookups or a parallel geometry graph.
- Renaming changes presentation, not identity. Independent definition copies get
  independent identities; adding another placement retains the target definition.
  Repeated nested occurrences require a full placement path, not just a definition ID.
- Keep the definition catalog distinct from the instance hierarchy. Native
  container membership alone must not make a stored definition another placement.
  Retain unused definitions. Detailed destructive-action menus remain deferred.

### Creation, editing and history

New component-document creation is a transaction: establish the file root,
create domestic Part001, place it once and enter Edit for that occurrence.
An empty component document remains valid. Retrofitting an existing document
must not run this new-file initializer or insert an extra Part001.

A modeling command resolves its target from explicit Edit context. When the file
is edited, selecting a component once cannot silently supply that target. Feature
adapters preserve existing geometry semantics and native editors while assigning
content to the edited component. New combined operation workflows are separate work.

History presents the active component's sketches, producing operations and other
geometry in dependency-compatible sequence. Body containers remain backend items.
This does not authorize History reordering or temporary suppression workflows.
Temporary unused-model occurrences and contextual fading are view state; saving
must not turn them into permanent placements or authored visibility changes.

### Panel foundation (G1.6a)

[panel.py](../src/Mod/FreeCADPlus/freecad_plus/panel.py) provides the explicit
`show_panel()` opt-in. One Components dock contains Models, Part Tree and History.
This is a developer entry point, not an owner-build delivery, startup replacement,
or authorization to remove the native tree/workbenches or create new toolbar groups.
G1.6c retains the remaining confirmed panel actions.

Models projects domestic definitions and nested imported-file groups using qualified
external names. Part Tree projects full native occurrence paths beneath one file
row bearing the file name/FreeCAD icon. History projects owned sketches/features and
geometry without Body rows; File Edit shows its Origin and three planes with native
visibility controls in an undoable transaction. Plane visibility and its parent
Origin visibility are separate native states; showing a plane enables its Origin.

Single-click/native selection never changes Edit. Double-click or context-menu Edit
resolves a placed component in the current tab; Models uses its last edited occurrence
in that view, otherwise the first occurrence. All occurrences and the model row use
bold/configured native TreeActiveColor fill. A separate outline marks the edited
occurrence; ordinary selection remains distinct. The full native Part/Body context
continues to drive the existing feature adapters. Native feature editors prevent
switching Edit until they finish. No new modeling or task-dialog semantics are added.

Rows carry immutable native document UUID/object Name/ID and complete link identities,
not labels or pointers into a rebuilt tree. Actions recheck the active document/view,
current graph and occurrence target before using a row. Double-click verifies that
its first press referred to the same view/item. Native document/GUI/selection events
coalesce into a single queued refresh; existing QTreeWidgetItems are reconciled in
place, preserving expansion and avoiding repeated row reconstruction. There is no
idle refresh timer. Pending native transactions defer projection until commit/abort.
The panel's close path unregisters all observers/context callbacks and stops updates.

### Component file tabs (G1.6c1)

`editing.open_component_view` creates an ordinary native MDI view of the current
catalog document. A placed component retains its full assembly occurrence path;
an unused definition uses the existing independent per-view isolation. No file,
definition or placement is cloned, and no presentation state is serialized. The
owning document and native source-file save/Undo behavior are unchanged. Native
coordinated transactions may create forwarding Undo entries in dependent documents;
opening a view itself creates none. Contextual fading/Part Type remain G1.7.

The Models/Part Tree Open in new window action resolves identities and the preferred
occurrence before creating the view, preserving the originating tab's context and
camera. Ordinary Edit still stays in its current tab. New tabs have component labels
and a transient Qt marker so the opt-in panel can resume title tracking when reopened.
The panel coalesces existing notifications; no polling or persistent UI property is
added. Child Edit continues through the same full occurrence-path service.

Opening is refused during any native feature editor or pending transaction. The
menu captures its originating document/view to reject a tab switch while it is open.
If entry fails after native view creation, the new view/isolation is removed and the
original view reactivated. Closed views are removed from panel state. When dock layout changes temporarily
clear the active subwindow, state resolves the subwindow owning the native view;
it does not assume that activeSubWindow is always available. Source loss
uses the existing validated isolation/context teardown. File close/save prompts and
view ownership remain native. Linked Copy/Paste is a structural panel action.
Move Components and independent storage-copy dialogs are operation workflows;
menu routing belongs to the panel, but the dialogs do not become Group 1 work.

### Linked-instance clipboard (G1.6c2)

The Part Tree clipboard is panel-owned transient data, distinct from native document
Copy/Paste and from independent storage copying. Copy snapshots definition identities
(document name/UUID, object Name/ID), local LinkPlacement, LinkTransform and visibility.
It creates no objects or Undo entries. Selected descendants are omitted when a copied
ancestor already includes them. The same underlying child under different selected
parent occurrences remains two distinct copied occurrences.

Paste uses the explicitly selected file/placed-component row as its parent and retains
copied placements relative to that parent; this is the announced implementation
convention while an optional owner preference remains unanswered, not a recovered
owner requirement. No world-frame conversion or movement command is implied. The
parent definition owns new child links, so they appear under all its occurrences.
This is not the deferred Add Component dialog or independent external/domestic copy.

`hierarchy.add_instances` is the shared batch placement service; single-instance
creation delegates to it. It preflights the whole batch against the destination's
own catalog and circular nesting before mutation, then uses one native transaction.
External-parent Paste modifies its defining document; native coordinated Undo can
add forwarding records in dependent files. Existing imported definitions are reused;
no file import or same-label substitution is performed implicitly. Late failure
aborts every added link. Save/reopen uses native persistence; schema 5 additionally preserves copied display choices.

The opt-in panel scopes menu actions and keyboard interception to Part Tree. It
never replaces the operating-system clipboard or global FreeCAD shortcuts. Paste
selects the new instances without changing Edit. Missing identities, invalid source
catalogs, changed tabs/rows, active feature editors and pending transactions are
rejected. File/unused/model/history rows cannot be copied as placed instances; Paste
requires a file or placed parent. Closing the panel discards the clipboard. No new
persistent UI/model metadata is introduced.

### Move Components foundation and Translate (G1.6c3)

Scope correction: Move Components is an operation reached through the panel's menu,
not part of panel implementation. Historical IDs are retained for evidence links;
unimplemented movement methods do not block Group 1 acceptance.

`freecad_plus/movement.py` owns the native Tasks dialog and its transient controller.
Part Tree Move Components accepts whole occurrence rows. The first eligible row
establishes its immediate parent occurrence as Edit; all supplied rows must be
siblings under that same exact path. Mixed parent/child selections are refused as
a whole. The file container owns root placements. A shared definition owns nested
placements in its own document, including external definitions; moving a child
therefore changes that child in all occurrences of its parent. Existing links,
LinkTransform, orientations, descendants, definitions and schema identities remain.

Translate is one normalized parent-frame vector, nonnegative native length input
and Reverse. Parent X/Y/Z are explicit choices. Native `Part.getShape` resolves a
picked visible straight edge/line/axis through its occurrence transform, then the
parent rotation converts the direction (never its position). The result is a
snapshot, with no persistent reference or expression. Invalid geometry/length,
read-only/driven/constrained links and stale context are refused before mutation.
Scaled frames are explicitly unsupported in this bounded increment; they must not
silently produce incorrect movement.

Preview adds an unpickable Coin wire outline to the originating view. It includes
corresponding children under every visible parent occurrence; existing geometry
remains available for reference selection. No document placement, visibility,
geometry, object or transaction is changed by preview. Apply preflights all links,
adds the same translation to each native LinkPlacement and commits one transaction
in the defining file. Late failure aborts the entire group. No-op Apply creates no
Undo entry. Inputs reset after Apply; Persistent Selection defaults on and retains
component rows/highlights, while off clears both. Cancel removes pending preview
but leaves earlier committed moves; OK commits only a pending nonzero movement.

The workflow list preserves the six confirmed entries in order. Translate and Rotate are
implemented; selecting an unfinished method clears pending inputs, retains siblings
and parent, and explains that the method awaits implementation. This is a staged
boundary, not removal of the other confirmed workflows. Native Tasks owns the form;
closing the task, panel, source/view, changing Edit or switching file/workbench
releases the overlay and event subscriptions. Camera interaction remains native.
The original workbenches and owner settings are unchanged. Acceptance is recorded
in WORK_STATE; subsequent Move methods and complete owner delivery remain separate.

### Rotate (G1.6c4)

Rotate extends the same `movement.MoveTask`, not a separate dialog or document
feature. The shared motion contract is now an `App.Placement`: a rigid transform
left-multiplied onto each selected sibling's existing LinkPlacement. Translate is
a translation-only instance of this contract. Rotate computes a common rotation
about its resolved parent-frame axis/pivot, changing both position and orientation.
Native LinkTransform, shared definitions, nested descendants, geometry and IDs remain.

Axis choices are parent X/Y/Z through the parent origin, a visible straight edge,
line or native infinite axis with its location, or two distinct picked points.
An optional point relocates a parallel axis without changing direction. Point picks
accept vertices/native points, origins/coordinate systems and circular-edge centers.
Native shape extraction includes the picked occurrence transform; the chosen parent
frame's inverse transforms positions, while its inverse rotation transforms vectors.
All reference values are snapshots. They do not introduce persistent dependencies,
joints or changing placement inputs as the preview moves.

The native angle field accepts nonnegative angular magnitude. Positive follows the
shown axis arrow by the right-hand rule; Reverse negates the angle. Invalid units,
angles, incomplete axes and coincident points cannot commit movement. A full-turn
identity transform is a no-op. The resolved axis direction and pivot are labeled
in parent coordinates using native length units. An unpickable axis arrow and pivot
marker accompany the pending geometry in the originating view.

Preview uses `parent_world * motion * parent_world.inverse()` against freshly
extracted original geometry for each visible parent occurrence. It never updates
LinkPlacement or accumulates successive preview transforms. Apply retains the
existing source-owned atomic transaction, resets all axis/point/pivot/angle/Reverse
inputs and follows Persistent Selection. Method changes discard pending inputs;
Cancel and OK retain their existing semantics. The remaining four Move methods,
scaled-frame support and full owner delivery are separate work. WORK_STATE owns
build, native regression, persistence, visual and publication evidence.

### Unused definitions (G1.6b)

`editing.edit_unused(doc, definition)` isolates a domestic or imported definition in
the current view, retaining the defining-file qualifier for external models. The panel adds one temporary last child beneath the pinned file row, labeled
`Component name (unused model)`, with active fill/bold text and no drag flag. Existing
file/occurrence rows are gray but selectable and still support Edit. History routes
to the definition's native sketches/features; native Bodies stay out of the panel.
The Sketch/Pad adapters use the same owning-document transactions as placed edits.

[isolation.py](../src/Mod/FreeCADPlus/freecad_plus/isolation.py) owns transient view
sessions. A transient separator borrows the definition's live native display
children, bypassing only its top-level visibility switch. Native child identities,
picking metadata, transforms and editor preview updates remain live. Detached deep
copies are unsuitable because they lose native pick-path identity. Isolation wraps
native ObjectGroup,
GroupOnTop and RootDimensions in hidden scene switches. Keeping the original groups
alive preserves native add/remove behavior. Native EditingRoot remains available for
the Sketch editor. No App objects, instance links, Visibility properties, schema
fields or Undo entries are created by isolation. Save therefore persists definition
edits without persisting a temporary occurrence or hidden assembly state.

Relevant native observer bursts reconcile the display wrapper once per queued update;
there is no idle polling. Commit/abort defers incomplete graphs. Each session belongs
to one native view and resolves the definition by document UUID/object Name/ID.
Changing Edit, closing the panel/view/document, losing the definition/import, or
placing the previously unused model removes the preview and restores native groups.
Cleanup clears the unused Part/Body context. Undo of removal restores data without
reopening isolation. Native feature editing must finish before switching contexts.
The implementation is checked against 1.1.4's scene-group layout and refuses an
unrecognized definition display before replacing an existing context.

### Explicit native document contexts (G1.6b integration)

The native development build passed the bounded G1.6b acceptance. The opt-in panel
binds a view to its native file-root catalog with
`view.setDocumentContext(catalog, editRoot=None)`. The catalog must belong to that
view's document; an optional editing root must be an attached catalog dependency.
These are silent, transient ActiveObjectList entries, excluded from generic active
Body/Part discovery. They create no document objects, saved properties, highlighting
side effects or preference changes. Ordinary views without a context retain native
selection and editing behavior.

Tree selection stays in the active view only for objects reachable from its explicit
catalog context. Unrelated objects retain ordinary view synchronization. An unused
external definition additionally supplies the explicit editing root; native setEdit
accepts that parent only in the active owning view and while it remains reachable.
Other external-parent calls retain the original refusal. The existing native editor
still edits the source feature and source document; no temporary native link is
inserted into the assembly. History double-click uses `editing.edit_feature` to
resolve the current component and open its native editor through the correct path.
It starts the native active command transaction, matching a native feature double
click; the dialog owns commit/cancel. Existing transactions are not consumed, and
failed editor entry aborts only the new transaction. Source-owned Pad Undo/Redo is
verified after accepting a real parameter edit.

Native picking first retains ordinary document-map lookup. If it finds no provider,
Document resolves live foreign nodes only when the pick path contains the matching
view's scene root, that view has an explicit external editing root still reachable
from its catalog, and the provider belongs to that root's dependency graph. This
supports both mouse selection and native pick APIs without global foreign-object
selection or a temporary document object.

Changing component Edit clears the external editing root while retaining panel
selection context. Closing the panel clears its visited views' contexts. Native
object/document deletion clears references across views before freeing external
objects; existing native source-deletion handling closes an active feature editor.
Imported catalog membership is rechecked before native editing. Per-view contexts
are neither implicitly cloned into a new view nor serialized. G1.6c1 explicitly
initializes each new component view; other context actions remain G1.6c and
Part Type/fading remains G1.7.

The original official 1.1.4 binary lacks this API. With that runtime, domestic
unused editing remains supported but external unused Edit reports the required
native document-context build; it does not start a partial isolation session.

### Saved Part Type and visibility state (G1.7a)

`display.py` owns the schema-5 state contract. Optional native properties on a
component definition store its self Part Type/Shown choice; optional properties on
its owned child links store the parent's direct-child choices. Self and child
properties have distinct names to avoid native Link property forwarding. Defaults
are Full Component/Shown for self and Bodies Only/Shown for children. Reading old
files, panel refresh and entering Edit do not add properties or upgrade a file.
Changing a setting upgrades only its defining file, in the same Undo transaction.
Schema 1–4 remain readable; schema 5 prevents old readers silently accepting new
semantics. Missing optional choices have defaults; partial/wrongly typed metadata
is rejected. Native identities, geometry, placements and Visibility are unchanged.

Part Tree/active model menus resolve the active component's self or direct child
through exact occurrence paths, rechecking view, context and identity before write.
Native editors/pending tasks guard mutations. Choices are source-owned for external
parents and shared across their occurrences. Excluded cannot be made Shown; its
saved visibility is retained separately. Nested Reference resolves as Excluded
without erasing the saved Reference choice. No reference geometry becomes usable
for modeling through this state API. Linked Copy/Paste snapshots these choices;
independent copies reuse native property copying and upgrade their destination.

This increment exposes saved choices through checked menus and contextual tree
tooltips. It does **not** apply viewport filtering, fading, reference eligibility or
export rules. G1.7b1 below applies explicit hiding; remaining content, fading and
eligibility gates remain open. This opt-in development panel is not a delivered owner
UI. WORK_STATE owns actual acceptance evidence.

### View-local explicit hiding (G1.7b1)

`display.hidden_paths` resolves Hidden/Excluded and nested Reference to whole native
occurrence paths. The active occurrence uses its definition's self choice; entering
Edit traverses its ancestors even when a parent had excluded that occurrence.
Direct Reference is visible in the exact active parent occurrence; its corresponding
child beneath another occurrence is treated as nested, without rewriting saved state.
These are explicit resolver conventions, not new owner-approved requirements.

`view.setComponentHiddenPaths(root, paths)` adds one scene-owned selection root around
that view's native ObjectGroup. The unique outer root keys secondary Hide entries on
existing view-provider paths. Geometry, object identities, placements and saved native
Visibility remain unchanged; hidden paths also disappear from native ray picking.
An empty path list/no-argument call restores the original ObjectGroup. Native wrapper
teardown clears its secondary entries while child nodes are still available. Invalid
whole-object names are refused before disturbing existing filters. A temporarily
unavailable native scene path clears the temporary hide entries and reports failure.

The opt-in panel reapplies paths through its existing coalesced native events, including
recompute and Undo; there is no idle polling. Each visited view resolves its own Edit
and unused-isolation context. Missing/deleted Edit contexts use the same file projection
as the tree, without creating an Edit state. Entering unused isolation first restores
ObjectGroup; returning reapplies the placed view's saved choices. Panel disposal clears
every tracked view. No shared ViewProvider partial-render or Visibility writes are used.

This increment does not implement fading, Bodies Only content filtering, Reference
modeling eligibility, export policy, or saved display filtering inside an unused-model
preview. Bodies Only traversal follows the owner-example interpretation in
[Component Panel](ui-ux-specs/COMPONENT_PANEL.md#part-type-and-visibility). Those limits
must not be treated as completion of G1.7b or as approval for a new operation dialog.

### Contextual fading (G1.7b2)

Validated in the native development payload; WORK_STATE owns bounded acceptance
and remaining Group 1 limits.

`view.setComponentFade(root, activePath)` resolves the actual native occurrence path
and stores it on that view's existing `SoBoxSelectionRenderAction`. The no-argument
form clears it. The traversal callback compares full node/index paths within ObjectGroup,
so a repeated definition is opaque only at its edited occurrence and descendants.
Viewport furniture outside ObjectGroup retains its native appearance.

Immediately before native shape rendering, the traversal callback clamps each current
material transparency to at least 0.75, retaining larger authored values and native
colors/material bindings. A Coin stack element retains the authored array and restores
it before the next node; separator exit discards both temporary states together.
No document/view-provider property writes, geometry copies, additional objects or Undo
records are used. The callback always continues native drawing, including delayed
transparent passes; it never prunes siblings or substitutes its own geometry draw.
Temporary arrays use a private, changing Coin node identity: lazy material/color
packing caches are keyed by the supplying node ID, not the array contents. Reusing
a shared shape's ID risks aliasing faded and authored material arrays. Active per-face
arrays are re-published unchanged. Native geometry buffers and renderer preferences
remain unchanged. Sorted transparent faces use Coin primitive caches, whose generated
per-face colors must depend on the current material. SoBrepFaceSet::generatePrimitives
sends only diffuse material while a GL primitive cache is being constructed, registering
that dependency. Without it, shared occurrences can reuse faded vertex colors even
when the incoming material state and occurrence classification are correct. Faded draws invalidate
open render caches; context changes touch existing shapes once to discard prior opaque
caches. Equal paths do not repeat that invalidation. This is render-state behavior,
not a saved preference or a Part Type change.

The panel applies the context separately in every visited view. File Edit, missing
Edit context, unused isolation and panel disposal clear it; the native action releases
its retained path on view destruction. Hidden/Excluded filtering remains independent.
An invalid requested occurrence is rejected before changing the prior fading context.
A valid context whose native linked snapshot is not yet available returns false and
clears fading without clearing panel rows. The panel retries once after a viewport
paint per model/context invalidation; subsequent paints do not poll or rebuild it.
Bodies Only traversal, Reference modeling eligibility and operation dialogs remain
outside this increment. WORK_STATE records actual validation and remaining limits.

### Saved display in unused previews (G1.7b3a)

`display.unused_hidden_paths` shares the placed-occurrence resolver, rooted at the
unused definition. Its direct Reference children are visible, nested Reference and
explicit Hidden/Excluded children are omitted. The preview's own private SoSwitch
applies its saved self visibility/type; native definition/child switches are unchanged.

`view.setComponentPreviewHiddenPaths(definition, paths)` reuses the native hiding
implementation with a separate PlusUnusedVisibilityContext around PlusUnusedPreview.
The preview borrows native child nodes, so resolution starts at the first child
provider and continues through its native detail path. This works for domestic and
external definitions without requiring them to be a provider in the assembly's document.
Names are validated before existing filters are disturbed. Empty/no arguments restore
the original preview. The context destructor clears secondary entries from borrowed nodes.

Isolation refresh clears its native wrapper before replacing the preview and reapplies
saved choices afterward. Close restores the preview before removing it and returning
the original assembly nodes. These are transient per-view contexts, not new document
objects, saved native Visibility, material changes, geometry copies or Undo operations.
Native linked-document transactions may mirror source-owned edits in an assembly undo
list; the actual saved display properties remain on the defining source's objects.
Bodies Only filtering is implemented by G1.7b3b below. Reference-use eligibility remains unfinished.

### Bodies Only content filtering (G1.7b3b)

`display._hidden_paths` resolves the saved effective type at each occurrence,
including the active-self override and the route into Edit. For Bodies Only,
`_construction_paths` adds visible origin/non-Tip Body history and standalone
non-face-bearing objects to the existing native whole-object hide paths. Body Tips
remain the native result; standalone solids, shells and faces remain represented by
their original feature. Mixed compounds with faces are retained whole, not split or
rewritten. This is a display classification, not new persisted modeling semantics.

Nested links are traversed with their own saved choices. A Bodies Only parent does
not discard ordinary descendants or erase an explicit nested Full Component choice.
Reference/Excluded context continues through the existing resolver. Unused previews
apply their definition's saved self type and use the same child traversal. Native
Visibility is honored, not set; filtering never reveals an authored hidden result.

Placed and unused paths share `display.apply_hidden`. Native LinkInfo child
snapshots are rebuilt by delayed Coin sensors; on the specific native temporary-path
error, drain that queue once and retry once. Other errors and persistent failures
propagate. No recurring retry, Qt event-loop wait, native C++ patch, schema upgrade,
proxy geometry or independent identity registry is introduced.

TestComponentBodiesOnly covers native ray picking, Body history, curve/solid/sheet
content, nested overrides, shared views, source-owned external unused filtering,
Undo/recompute, native Sketch editing, cleanup and independent save/reopen. Actual
results and visual acceptance are in WORK_STATE. Reference-use eligibility and
separate operation workflows remain outside this completed increment.

### Geometry eligibility (G1.7b3c)

`geometry.require_access(doc, obj, sub, active=..., active_path=...)` is the shared
read-only boundary for consumers of component geometry. Call it before reading a
native shape, using the originating view's Edit context. It validates catalog and
occurrence ownership and delegates mapped topology/object paths to FreeCAD's native
parser. Native origin axes use object-identity lookup, not shape availability.

Each crossed component link applies its effective saved Part Type. Active Edit
uses its self setting and overrides ancestor restrictions only on the editing route.
Reference and Excluded geometry are rejected. Shared source definitions do not erase
occurrence distinctions; bare foreign members must supply an occurrence path.
Domestic/external unused definitions use their source-owned state. Hidden alone is
not an eligibility restriction; consumers retain their separate visibility checks.
A selected component aggregate is refused if any descendant is forbidden; no partial
replacement shape is constructed. An owned derived feature is checked at its own
identity without following outgoing source links. This supports the U069 ownership
rule but does not implement the separate promotion operation.

Existing Move Components reference reads use this boundary for directions, axes,
axis points and pivots. Their accepted references remain one-time placement snapshots.
Panel tooltips explain the restriction while selection and Edit remain available.
Do not install a global SelectionGate or override Part.getShape: navigation and
native command-specific selection gates have separate responsibilities. Remaining
native modeling/export consumers still need explicit integration; this service alone
does not establish universal enforcement or intercept direct Python shape reads.

TestComponentEligibility covers shared/aggregate rejection, editing overrides,
external unused ownership, no foreign-member bypass, owned source-linked features,
Undo/Redo, exact identity/visibility persistence and actual consumer rejection before
shape reads. WORK_STATE records runtime evidence and scope limits.

### Native export eligibility (G1.7b3d)

`Gui::Application::exportTo` adds a preflight only for documents carrying PlusFormat.
It calls geometry.export_objects to construct and validate the native export payload
before importing the exporter or invoking its options/writer. That adapter calls
geometry.require_export with the originating document. Legacy documents keep their
original dispatch. The recorded export command includes the same check.

The adapter checks unresolved native selection paths with the shared eligibility
service, then verifies that every actual payload object was approved. This preserves
shared-occurrence distinctions that the resolved export list otherwise loses.
Source-owned unused editing uses the originating assembly view. Std_Export falls
back to that view's ExternalEditContext source selection only when its ordinary
active-document selection is empty; legacy selection routing remains unchanged.
Whole-file export
uses saved restrictions without the active branch's temporary Edit override. With no
matching selection, refuse the native fallback that would export all document objects,
including unused catalog entries. Save/Save As and native archive persistence do not
pass through this geometry-export boundary and continue retaining Reference sources.

This increment refuses a selected aggregate containing forbidden geometry; it does
not silently strip child objects or create a replacement compound. Bare catalog or
foreign members still need an unambiguous editing/occurrence context. Direct calls to
individual exporter modules (including Python calls), view-image/PDF export paths and
native modeling commands remain separate integration work. This is not universal
Reference enforcement or a new export UI. TestComponentExport drives Std_Export,
its actual dialogs and a writer probe backed by native BREP export; WORK_STATE owns
build/runtime results and limitations.

#### Placed external export context (G1.7b3m)

Native selection can resolve an external member into its defining document while
its unresolved occurrence remains selected in the assembly view. export_objects
first checks selection in the export document; if absent, it uses the current
component view only when its resolved selection includes an object from that export
document. Native resolved selection supplies the actual deduplicated object payload;
require_export checks every originating unresolved occurrence before options/writing.
An allowed duplicate cannot mask a rejected Reference/Excluded occurrence.

The adapter never substitutes the defining file's whole catalog when its own
selection is empty. Source-owned unused Edit continues using its source selection
and the existing isolation context. Bare foreign members still need an occurrence;
no arbitrary source-link traversal, visibility change or new export geometry is
introduced. File names/options and native writer semantics remain upstream behavior.
Direct writer APIs and view-output paths remain outside this dispatch integration.

### Native modeling intake eligibility (G1.7b3e)

`Gui::componentGeometryError` in ComponentGeometry.h is the shared native-to-Python
bridge for two concrete consumers. It calls `geometry.require_modeling_inputs` only
for a consumer in a component document; ordinary FreeCAD documents retain their
native workflow. The adapter resolves the current view's placed/unused Edit context,
requires the consumer to belong to that component, and applies the existing
occurrence policy to every input. It does not traverse existing feature dependencies.

PartDesign's shared prepareProfileBased path checks unresolved selection before
creating a feature or opening a transaction. Its later native profile-picker callback
rechecks the actual candidate before creation, so a delayed picker cannot rely only
on an earlier selection. Native profile/body/geometry validity checks still apply.
Sketcher's Projection/Intersection external-geometry handler follows pOriginalMsg to
the original occurrence before addExternal and before opening an undo command. A
rejection reports its reason and clears the attempted selection without aborting the
surrounding sketch edit. The existing tool-specific selection gate stays in place;
no global selection gate, shape-reader override or recompute hook is introduced.

This is input admission, not universal reference enforcement. Existing references
and raw Python property/method writes are not reclassified during recompute. Other
attachment, task-dialog reference and non-profile commands still require integration.
No new Add Reference Feature, Sketcher or PartDesign operation workflow is defined.
TestComponentModeling owns focused native intake acceptance; WORK_STATE records
build/runtime evidence separately from the source contract.

### Attachment and shared task reference intake (G1.7b3f)

The native Part TaskAttacher checks the complete unresolved initial-selection batch
before converting occurrence paths or setting any AttachmentSupport entry. The same
boundary checks individual picked references. Typed nonempty references are checked
before changing Support or the line's RefName metadata; removing a reference remains
possible. Rejection uses the existing inline attachment message and leaves the
current support, placement and editor transaction intact.

PartDesign's getReferencedSelection checks the original selection message through
ComponentGeometry.h before resolving it into a shared definition or offering the
native external-reference/copy dialog. The output remains null on rejection, so its
existing callers retain their references. This covers picked Extrude direction,
Revolution/Groove and Helix axes, Draft neutral plane/pull direction, Mirrored plane
and Pattern direction/axis through that shared collector. Ordinary legacy documents
still bypass the component policy; native validity and reference behavior remain.

This does not cover every reference editor. The separate Python AttachmentEditor,
other task collectors (including Extrude up-to-face/shape and Loft/Pipe sections),
combo-box stored references, property-editor/direct Python writes and existing
reference reclassification remain outside this increment. No new promotion/copy
workflow is authorized. TestComponentReferences owns focused native acceptance;
WORK_STATE owns the actual build, runtime and publication evidence.

### Python attachment and Extrude face/shape intake (G1.7b3g)

The separate Part AttachmentEditor applies the same component policy before adding
an attachment extension or opening a transaction when taking initial selection.
Picked references are checked before shortening their original occurrence paths.
Parsed text references are checked as a complete batch before replacing the attach
engine's references or calculating a preview. Apply and OK recheck component input
text, so forbidden text cannot commit an earlier valid preview; rejection preserves
the open task/transaction. Component-task Cancel explicitly closes the application
transaction before display restoration, including the lazy empty transaction left
by Apply, so cleanup cannot create an extra Undo entry. Ordinary legacy files do not
import the Plus policy and retain their existing confirmation/transaction behavior.

TaskExtrudeParameters checks original occurrences for up-to-face, up-to-shape and
selected shape-face inputs on either side before mutation, selection clearing or
picker-mode changes. Typed up-to-face object ownership is checked before the native
setUpToFace helper, which itself writes and recomputes the feature. Rejection leaves
the prior property/field metadata and preview in place and uses existing notifications.
Native face parsing, geometry validation and Pad/Pocket semantics remain unchanged.

Remaining work includes Loft/Pipe section collectors, other feature inputs, stored
combo references, property-editor/raw Python writes, direct exporter/view-output
routes and existing-dependency reclassification. This is not universal enforcement
or a new attachment/Extrude workflow. TestComponentInputEditors owns the focused
acceptance; WORK_STATE records runtime coverage separately from this contract.

### Loft/Pipe profile, section and path intake (G1.7b3h)

`TaskLoftParameters` and the three `TaskPipeParameters` task boxes use the shared
component eligibility bridge before assigning a picked profile, adding a section,
or replacing/extending a main or auxiliary path. Checks follow `pOriginalMsg` to
the original occurrence before native reference normalization. A rejected pick
preserves the prior properties, section/edge lists, preview geometry and transaction;
existing native picker exit/reset behavior remains. Ordinary legacy documents bypass
the Plus policy. Existing C10/U069 rules govern; no new operation workflow is added.

Removing a Loft/Pipe section is cleanup and remains available even if that occurrence
is now ineligible. Pipe edge-removal picks also assign the selected source object in
the native implementation, so those picks need the same admission check; list Delete
continues to remove from the stored reference without introducing another source.
Native geometry, reference-copy dialogs and section ordering remain unchanged.

This is picked-input admission, not a recompute hook or retrospective validation of
stored dependencies. It does not cover raw property/Python writes, other operation
collectors or deferred Add Reference Feature design. Tests and bounded acceptance
are recorded in WORK_STATE; this is not full Group 1 acceptance or owner delivery.

### Shared dress-up and transformed-feature intake (G1.7b3i)

`TaskDressUpParameters` checks the original picked occurrence before appending an
edge/face to the stored Base reference. Toggling an existing entry off and list
Delete remain cleanup, without admitting new geometry. Its shared check also guards
Add All Edges before reading geometry or opening a transaction. Fillet/Chamfer Use
All Edges checks the stored base before enabling; rejection restores the checkbox
without changing the property, picker/list state or preview. Disabling remains
available. A stored-base action has no picked occurrence; it checks the current
component Edit context and the stored source ownership through the shared policy.

`TaskTransformedParameters` checks a newly picked Original against that policy
before list/property mutation or transaction creation, retaining the original
occurrence path. The top transformation is the consumer when a nested transformation
task is involved. Existing-entry removal remains available. Ordinary legacy files
bypass these Plus checks; native geometry, dialogs and operation choices remain.

This integrates C10/U069 eligibility, not new operation workflows. Command-start
preselection is covered by the following G1.7b3j boundary; other collectors, raw
property/Python writes and retrospective reclassification remain separate. Tests use
native Fillet/Chamfer controls and a Linear Pattern; this does not certify every
geometry variant served by the shared classes. WORK_STATE owns runtime acceptance.

### Dress-up and transformation command admission (G1.7b3j)

`Command.cpp` checks the active backend Body and the unresolved complete selection
through `componentGeometryError` before dress-up selection clearing/edge expansion,
transformation Feature filtering, transaction creation or feature/Tip mutation.
The same check precedes the separate conversion of an existing transformation into
Multi-Transform. An empty selection still requires explicit component Edit and
consumer ownership; native whole-shape/no-selection behavior then remains available.
Legacy documents bypass the Plus policy before its Python import. Chamfer clears
preselection only after shared preparation succeeds; rejection retains the selection.

The Pattern task routes Add/Remove Original selections only to the Original
collector. Rejected or duplicate Originals no longer fall through to direction/axis
parsing, and a rejected addition leaves the picker available for another selection.
This adds no operation workflow, new geometry semantics or saved schema. Native
active-Body resolution remains upstream behavior; the guard runs once a Body is
available. Other command families, raw writes and existing dependency reclassification
remain separate coverage boundaries. WORK_STATE records build and runtime evidence.

### Native Boolean ownership within a component (G1.7b3k)

Native PartDesign Boolean `Group` is an ownership group, not merely a list of
source dependencies: adding a tool removes it from its former GeoFeatureGroup.
`document.owned_children` recognizes that native ownership alongside Part/Body and
Origin ownership. Document validation and `document.owned_path` share that contract;
geometry eligibility reuses the same path traversal. Arbitrary property links,
BaseFeature dependencies and component-linked definitions are never traversed as
ownership. Orphans, cycles and multiply owned contents still fail validation.

History projects a Boolean's owned tool features before the Boolean and recursively
hides backend Body containers. Panel selection and feature Edit use the full native
ownership path, retaining nested tool feature editing without changing identities,
geometry algorithms or serialized native data. No schema migration is introduced.
This fixes same-component Boolean results previously appearing to contain orphaned
tools and thus failing component save validation.

Cross-component Boolean intake is unresolved: native grouping can transfer a tool
out of a different shared definition, altering all its instances. The reviewed C06,
C09 and C10/current owner instructions settle preservation, hidden backend Bodies
and mandatory promotion of Reference geometry, but do not specify Boolean tools
from another Full Component. An owner question is pending: require an owned linked
reference first (recommended), create one automatically, or intentionally move the
source tool. Do not infer a decision from native behavior. This increment implements
only the independent ownership prerequisite; Boolean command/picker eligibility
checks and cross-component behavior remain unfinished. WORK_STATE owns acceptance.

### Persistence contract

`.cadprt` retains the native FreeCAD archive and object/property serialization,
with component metadata that explicitly identifies the format and schema revision.
It is not a renamed legacy file with an assumed component structure. No historical
`.cadprt` schema is adopted implicitly. No owner files have been converted.

The schema owner is [freecad_plus/document.py](../src/Mod/FreeCADPlus/freecad_plus/document.py).
New files and conversions use schema 5; optional saved display choices extend schema 4. Schemas 1 and 2 remain readable/savable
with their original single-definition/single-instance bounds (schema 1 is Body-only).
Hierarchy operations require the explicit, undoable `hierarchy.upgrade(doc)` on an
older file; it validates the existing graph before changing only the schema marker.
External imports require `external.upgrade(doc)` to schema 4, adding native import
metadata in an undoable transaction. Schema 3 remains readable/savable without
automatically enabling external catalogs:

| Stored item | Native representation |
| --- | --- |
| Marker | File-root `PlusFormat = FreeCADPlus.ComponentDocument` |
| Revision | File-root integer `PlusSchema`: 1, 2, 3 or 4 |
| Definition catalog | File-root native `Definitions` PropertyLinkList |
| Imported catalogs | Schema-4 file-root `Imports` PropertyXLinkList targeting external file roots, with ordered source document UUIDs in `ImportIdentities` |
| Placements | File-root or parent-definition Group containing App::Link; copy-on-change disabled, no array elements or scale |
| Definition content | Native App::Part Group containing backend Bodies/geometry; schemas 3/4 additionally own child App::Links |
| Identity | Native Document.Uid and object Name; native object IDs also survive tested reopen |
| World frame | File-root Placement fixed at identity; native Origin/planes reused |
| Definition frame | Schema 3 preserves native definition Placement, including legacy Part frames; native LinkTransform controls how occurrence placement composes with it |

Ownership validation follows native groups and Origins, not arbitrary dependency
links. Orphaned objects, multiple roots and invalid targets are rejected. Schema 4 permits
native external catalog and instance links; arbitrary cross-file modeling dependencies
remain refused. Empty files and unused definitions are valid. Further content
migrations remain explicit; these service bounds are not final product restrictions.

[editing.py](../src/Mod/FreeCADPlus/freecad_plus/editing.py) uses the native per-view
`PlusEdit` active-object slot with a file-root-relative occurrence path, plus native
`part`/`pdbody` slots carrying the same full occurrence path. Selection never updates this context. A fresh reopen starts
in File Edit. Sketch creation supplies a Body automatically; the Pad adapter creates
the native PartDesign feature. History includes owned sketches/features/geometry
while excluding Body containers and child-instance links.
Native Sketch and Pad editors are retained and tested.

[hierarchy.py](../src/Mod/FreeCADPlus/freecad_plus/hierarchy.py) owns definition
creation, placement, movement and occurrence resolution across defining files. Definitions have one catalog
entry regardless of how many times they are placed. A child link belongs to its
parent definition, so its local placement is shared by every occurrence of that
parent. A full path of links selects one occurrence; a bare nested link is ambiguous
and is rejected. Native getSubObject composes world placement, including rotations
and LinkTransform. New hierarchy links use LinkTransform=true to include an existing
definition frame; legacy link transform modes and authored placements are preserved.

Add-instance checks reachability before creating a native link or transaction.
Validation checks all definitions, including unused ones, for cycles and checks
structural ownership separately from dependencies. Transaction validation now runs
before recompute as well as afterward, preventing invalid component graphs from
being traversed by recompute. Shared DAG branches are not mistaken for cycles.
Removing/undoing an occurrence invalidates its Edit path rather than selecting
another occurrence. Per-view contexts remain independent.

These are opt-in Python entry points, not replacements for File > New or arbitrary
workbench commands. Their ownership/Edit guards apply at these entry points. The
complete component panel and broader command routing remain later work; the stock
tree is still present alongside the explicit panel opt-in. No new toolbar placement or interface preference is implied.

The importer checks archive metadata before restoration and validates the restored
native graph. Unknown/future versions and renamed legacy archives are refused.
The save adapter assigns the exact FileName and invokes native save(), preserving
CheckExtension and native backup settings. It requires native safe-save BackupPolicy
rather than disabling safeguards. Pending transactions and partial loads are refused;
failed saves restore the previous filename/root label and retain GUI dirty state.
Only successful native save and archive verification clear that state.

Persist the file root, definition catalog, instance targets/local placements,
component ownership, import references and necessary history associations. Later
stages add confirmed parent-owned Part Type settings. Native objects retain
features, expressions, attachment references, geometry and appearance data.
Do not serialize transient edit-isolation rows or their temporary display changes.

Validate the marker, supported schema, identity uniqueness, ownership and native
references on load. A repeated open/save must not add roots, definitions or links.
A newer unsupported schema must be refused without rewriting the source. Older
schema upgrades must have an explicit versioned migration and recovery behavior.

Use native save/restore and transaction services. A failed save must leave the
previous valid file recoverable and must not claim success or clear dirty state.
Retain native backups and verify the actual final filename and a fresh-process
reopen. `.cadprt` extension handling needs explicit integration: stock
`Document::saveAs`/`saveCopy` append `.FCStd` for an unfamiliar extension when
`CheckExtension` is enabled. Do not disable that preference globally or silently
produce `name.cadprt.FCStd`.

### External files and conversion boundary

An external definition remains owned by its defining file; importing catalogs
and placing selected definitions are distinct actions. Cross-file references must
identify the actual file and definition, never substitute a same-named domestic
item. Validate file-import and component-nesting cycles before committing mutations.
The implemented [external service](../src/Mod/FreeCADPlus/freecad_plus/external.py)
uses native `PropertyXLinkList` for imported file roots and ordinary `App::Link` for
placed definitions. `import_file(doc, source_doc)` requires both files already saved
as `.cadprt`, matching the native XLink prerequisite. It imports the complete catalog
without creating an occurrence. `catalog(doc)` projects domestic definitions first,
then nested imported-file groups; `qualified_label` qualifies external names by file.
Labels never resolve identity. A shared imported file in two branches is valid;
file cycles and component cycles are refused before mutation/recompute.

Occurrence resolution changes defining document at each link in the full path.
The native per-view Part/Body contexts stay rooted in the assembly tab. Sketch/Pad
adapters transact against `definition.Document`; `save_definition(definition)` saves
only that defining file. Native cross-document dependency updates can add Undo
entries to importing files as well. This is native transaction behavior, not a
multi-file atomic disk save. Saving the assembly does not save dirty source geometry.
Save new external definitions and changed intermediate import catalogs before an
assembly that references them; otherwise preflight refuses to replace its archive.
A defining file with open dependents cannot change location through this Save API.

Before native restore, `archive_graph` reads every declared dependency's native
XLink path, format/schema, document UUID, root and definition names. Missing files,
wrong identities, unknown schemas, undeclared targets and import cycles fail before
opening any documents. Open-document identity conflicts are refused; a later native
restore/validation failure closes only newly opened documents. There is no same-name
fallback. Recovery at this stage is restoring the original file/path/identity and
retrying, which is tested. Relocation/search dialogs and path rewriting remain
unimplemented. Concurrent external replacement between preflight and native I/O is
not an atomic filesystem guarantee; retain native backups and check save failures.

`copy_definition(source, destination, label, placements_to_replace=..., child_labels=...)`
creates an independent native recursive graph in either storage direction. Nested
shared targets are copied once and remapped by the native copy service. It refuses
any surviving source dependency and rolls back unsupported graphs. Destination
names must be unique; callers provide conflicting child names explicitly. Replacement
placements must be explicitly supplied (an empty tuple retains all); only selected,
destination-owned links targeting the source are retargeted, preserving placement.
Copies and replacements are one undoable destination transaction. The original
external definition remains usable. The owner-facing placement checklist and storage
selection dialogs are still future UI work, not implicit defaults approved here.

Legacy conversion means `.FCStd` -> a separately saved `.cadprt`, preserving the
original source file. Inventory objects, native links, expressions, attachments
and placements before conversion. Keep editable native features where possible;
preserve recoverable final solid/curve geometry as explicitly identified
nonparametric content where conversion is unsupported. Report any loss of
parametric editing or unresolved dependency. Do not silently discard content.

Reparenting must preserve world placement and valid subelement references; it
cannot be considered successful merely because the final shape looks similar.
Validate conversion by editing, recomputing, saving, closing and reopening.
The initial converter is [conversion.convert_file](../src/Mod/FreeCADPlus/freecad_plus/conversion.py).
Its supported fixtures include domestic native Part trees/shared Part links, empty
files, a single native Body and its owned features, a single Part Box, and standalone
static Part features (including curves).
It creates only the required file root, definition wrapper and linked occurrence;
it never calls the new-file Part001 initializer. Names, labels, native object IDs,
authored placements, expressions and dependencies are checked before publication.
Native restore must account for every archived object. External references, scaled
or array/copy-on-change links, scripted Body graphs, mixed unowned content and other
unsupported graphs remain deferred, with no output written on rejection.

[legacy_hierarchy.py](../src/Mod/FreeCADPlus/freecad_plus/legacy_hierarchy.py) reuses
existing App::Parts as definitions, including their original Placement, Origin,
names, labels and IDs. Direct nested Part membership is replaced by an identity
App::Link with LinkTransform=true; original child links keep their targets and
transform settings. Former top-level Parts receive corresponding root occurrences;
top-level existing links remain instances. Original placement visibility is copied
to new occurrences before stored definitions are hidden. ConversionReport records
part_instances and replaced_group_edges. Only those intentional structural edge
replacements are excluded from the native dependency-preservation comparison;
other native references, expressions and authored placements remain checked.
Supported Parts can own geometry/Bodies and child instances at the same time.

#### Legacy Boolean tool ownership (G1.7b3l)

Both standalone Body and Part-hierarchy conversion use legacy_hierarchy.body_objects
with document.owned_children. A standalone supported graph has one outer Body;
Boolean-owned tool Bodies are nested content rather than independent roots. Native
Boolean Group, nested Body/Origin/features, expressions and dependencies stay intact.
The converter wraps only the outer Body or reuses the existing Part definition.
General dependencies and link targets never establish structural ownership.

Preflight rejects circular/multiple ownership, scripted features at any owned depth,
Parts inside Body graphs, independent root Bodies and unowned content. Existing
isolated restore, identity checks, explicit fallback and exclusive publication rules
remain. This preserves already-authored legacy graphs; it does not decide how new
Boolean commands may consume tools from another component. Acceptance uses one
nested tool Body in a Fuse, standalone and within a shared Part hierarchy. Other
Boolean modes and deeper graphs are not certified by this increment.

Conversion reads the on-disk FCStd into a separate native document, even when the
source is open with unsaved changes. The source is never saved or mutated. The
converted file gets a distinct native document UUID; its source UUID and original
object inventory are retained in the file-root ConversionReport JSON. This makes
the two retained files distinct while preserving native object identity within the
converted graph. FreeCAD itself regenerates duplicate document UUIDs on concurrent
restore; conversion deliberately assigns a new one consistently, regardless of
whether the source is open. This is not an external-reference migration.

Unknown standalone valid Part-derived shapes can be recovered only with explicit
`allow_geometry_fallback=True`. The new copy becomes a static Part::Feature,
retaining its name, label, shape and placement; source type is stored on the result.
ConversionReport records lost parameters/expressions and replacement object ID.
Body graphs are not silently flattened. Ordinary supported static geometry is kept
as its existing native type. No owner files have been converted during validation.

The destination must be new. Native safe-save runs in a temporary directory beside
it; an exclusive atomic hard link publishes the completed archive, then staging is
removed. Filesystems without hard-link support fail without replacing a source or
destination. Failed restore, conversion, validation or save closes only the working
copy and restores the prior active document. ConversionReport and the return value
make fallback warnings inspectable without inventing a conversion dialog.

Older fork `.cadprt` files need their own identified migration fixtures; do not
interpret them using the new schema merely because their extensions match.
Export back to `.FCStd` and direct `.cadprt` opening in stock FreeCAD are not
promised by this contract. They require separate compatibility decisions.

## Key invariants

1. One file root per component document; new-file Part001 creation occurs once.
2. Definitions, placements and visible occurrence paths have distinct roles.
3. Shared edits do not create independent definition copies accidentally.
4. File Edit cannot create file-owned modeling geometry.
5. Native geometry, expressions, dependencies and undo behavior remain authoritative.
6. Display state cannot bypass Excluded or make unpromoted Reference geometry a
   modeling input. Detailed Add Reference Feature interaction remains undefined.
7. Rename, save/reopen and conversion do not silently alter object identities,
   placements, reference targets or original workbench access.

## Failure and recovery behavior

Preflight ownership, reference and cycle checks before mutations. Group a logical
component mutation into a native transaction; abort failures without leaving a
partial definition, extra instance or stale Edit target. Treat view refresh as
presentation, not as an opportunity to recreate document objects.

Preserve unknown/unsupported native content where safely possible; report the
limitation rather than pretending it is a fully migrated editable feature.
Ambiguous external targets and missing definitions must not resolve by matching
labels. Do not overwrite a legacy source or silently downgrade a newer schema.
Native transactions are not a multi-file atomic-save guarantee. G1.5 checks missing,
replaced and unsupported dependencies, missing definition targets, unsaved catalog/
definition ordering, failed defining-file saves, retry and source-only persistence.

No owner clarification is required to begin the single-component pilot. Before
later dependent stages, resolve the deferred Add Component/Add Reference Feature
interactions, unconfirmed destructive/history/relationship controls, and whether
reverse `.FCStd` export is wanted. The pilot must report its limits explicitly.

## Source references

The native source establishes reused mechanisms; the pilot tests establish the bounded behavior above:

- [Document](../src/App/Document.h) and [serialization/save implementation](../src/App/Document.cpp):
  native Uid, ZIP/Document.xml serialization, save/restore and filename handling.
- [Part](../src/App/Part.h) and [origin groups](../src/App/OriginGroupExtension.h):
  native geometric grouping and Origin ownership.
- [Link](../src/App/Link.h): shared target, LinkPlacement, LinkTransform and copy-on-change.
  Schema 3 retains native transform behavior and keeps ordinary instances shared.
- [PartDesign Body](../src/Mod/PartDesign/App/Body.h): native feature grouping and Tip semantics.
- [Confirmed component behavior](ui-ux-specs/COMPONENT_PANEL.md#confirmed-requirements),
  [movement ownership](ui-ux-specs/TASK_PANEL.md#move-components),
  [edit display](ui-ux-specs/MODEL_VIEW_WINDOW.md#component-editing-display), and
  [owner evidence](ui-ux-specs/EVIDENCE_AND_DECISIONS.md): authoritative intent.

- [Pilot acceptance suite](../src/Mod/FreeCADPlus/TestComponentPilot.py): native ownership,
  context isolation, geometry, rollback/Undo/Redo, persistence and legacy controls.

- [Legacy conversion tests](../src/Mod/FreeCADPlus/TestLegacyConversion.py): native feature
  preservation, explicit fallback, source protection and fresh-process editing.

- [Hierarchy acceptance](../src/Mod/FreeCADPlus/TestComponentHierarchy.py): shared edits,
  native occurrence contexts, placement, cycles, schema upgrade and legacy Part/link conversion.

- [External-definition acceptance](../src/Mod/FreeCADPlus/TestExternalDefinitions.py):
  nested catalogs, external Edit/save ownership, independent copies, source protection,
  cycle rejection, failed save/recovery and fresh-process shared updates.

- [Panel interaction acceptance](../src/Mod/FreeCADPlus/TestComponentPanel.py): actual
  Qt single/double clicks, native occurrence selection, tab/stale-row guards, external
  Edit, origin visibility Undo/save/reopen and observer cleanup/idle behavior.

- [Native view context](../src/Gui/MDIView.cpp),
  [Python entry point](../src/Gui/MDIViewPy.cpp),
  [active-object lifetime](../src/Gui/ActiveObjectList.cpp),
  [native editor routing](../src/Gui/Document.cpp) and
  [tree view synchronization](../src/Gui/Tree.cpp): explicit, transient catalog routing.
- [Unused-model acceptance](../src/Mod/FreeCADPlus/TestUnusedModels.py): domestic and
  external selection/editing, source ownership/save, isolation, view and deletion lifecycle.

### Definition rename (G1.6c5)

hierarchy.rename_definition changes only the native definition Label in a single
transaction owned by the defining document. Names must be nonempty and unique
among that file's domestic definitions; equal labels in separate files remain
valid. Native names/IDs, shared links, placement and geometry are retained. Cancel,
unchanged names and preflight refusal do not add an Undo entry. Read-only Label
properties are refused; if the native assignment alters the requested name, the
transaction rolls back rather than silently substituting another name.

The Component Panel offers Rename for Models, placed occurrences and the temporary
unused row. Renaming an occurrence renames its shared definition and all displayed
uses; it is not a per-instance alias. The prompt makes that scope explicit. Menu
placement is a routine implementation choice for the owner's C09 rename permission,
not a recovered exact menu layout. File rows and History features are outside this
action. The dialog rechecks tab, identity, catalog membership, current name and
native task/transaction state before committing. Native observers update labels and
component window titles without polling or replacing stable rows. External names
remain qualified by defining file, and saving uses that source's existing service.

### Models file import (G1.6c6)

The Models menu, including its blank background and imported-file group rows,
exposes Import Models from File. The chooser names the defining file of the active
Edit component; file Edit targets that file itself. The action rechecks the tab,
active definition and native task/transaction state on acceptance. C09's October 9
14:03 and 19:00 UTC owner messages establish source-owned nested catalogs and the
separation of import from placement; the menu label/location is an implementation
choice. Add Component placement remains deferred.

external.import_path uses the existing archive/identity preflight and import_file
transaction. document.open_document(hidden=True) uses native hidden loading and
restores the previously active document without creating a source view or changing
Edit. Existing open source documents remain open. Failure closes only documents
opened during this attempt; expected archive/XML/file errors become panel feedback.
Successful imports remain open as native cross-file dependencies. Destination and
source must already be saved; the action does not silently save either file.

Only the owning file's Imports and ImportIdentities change in one native Undo step.
Repeated direct imports are no-ops; file cycles are rejected. Models projects nested
catalogs through the existing observer path. No definition/object identity, native
placement or Part Tree instance is created or rewritten. Cancel and refused actions
create no Undo step. Persistence uses the existing defining-file save service.
TestComponentImport covers the native menus/chooser, closed nested sources, external
Edit ownership, cancellation/duplicate/cycle/error guards and independent reopen.

### Boolean input admission (G1.7b3n)

PartDesign_Boolean calls the existing componentInputsAllowed helper before opening
its transaction, creating the Boolean or handing a normalized selection to native
addObjects. The complete unresolved selection is checked; a mixed selection is
rejected as one command before any tool can change ownership.

TaskBooleanParameters checks the original selection event through
Gui::componentGeometryError before adding a tool. It follows pOriginalMsg back to
the assembly occurrence so shared/external definitions cannot lose their contextual
Reference/Excluded restriction during native selection resolution. Refusal reports
the existing component-policy error, leaves the current list/model/transaction
unchanged and retains Add mode. Removal remains cleanup and bypasses admission.
Ordinary non-component FreeCAD documents bypass the Plus policy.

This integrates the October 11 Reference prerequisite with existing native Boolean
intake. It neither implements Add Reference Feature nor defines cross-component
Full Component tool transfer/copy behavior. Native same-component ownership,
operation types, recompute and existing dependencies are unchanged. Existing saved
features are not rewritten on recompute. TestComponentBooleanInputs covers refusal,
context checks, native picker continuation/removal and legacy bypass; the affected
Boolean ownership tests cover accepted creation, Undo/Cancel and persistence.

### Part Boolean eligibility and ownership (G1.7b3o)

Cut, Common and Fuse check the full unresolved selection before native shape checks
or transactions. DlgBooleanOperation checks its actual two list inputs before Apply
can create geometry. A Part-local bridge calls geometry.require_part_boolean_inputs,
which reuses the shared occurrence policy and requires an edited component. The
currently supported destination is that component's defining document; inputs must
be owned by the edited definition. The dialog's bare catalog objects cannot infer a
foreign occurrence, so such inputs are refused rather than acquiring permission
from an unrelated current selection. Reference geometry still requires the explicit
Add Reference Feature prerequisite.

BOPFeatures preflights component inputs before creating the native result. For this
component path, its existing move_input_objects service hides inputs but preserves
their original containers and returns the edited definition as result owner. Native
Base/Tool/Shapes dependencies are references, not ownership edges. Keeping source
features owned preserves History, document validation, Undo and save/reopen. Native
legacy files retain the upstream remove-from-parent behavior. This covers the six
existing BOPFeatures creation methods; it does not replace native shape algorithms.

This bounded integration does not define cross-component tool transfer/copy or
source-file routing through an importing assembly. Unsupported destinations/inputs
are refused before mutation. Direct Section, compound/split/join commands and other
geometry consumers remain separate. TestPartBooleanInputs covers command refusal,
accepted Cut/Common/Fuse ownership and Undo, dialog refusal/Apply, legacy bypass,
and independent persistence/source-edit recompute. WORK_STATE owns acceptance.

### Direct Part Section integration (G1.7b3p)

Part_Section checks unresolved component selections through the existing Part
Boolean preflight before transaction creation. Component files then reuse
BOPFeatures.make_section: inputs keep their original ownership, the native
Part::Section result belongs to the edited definition, and History includes its
sources before the result. The command retains the upstream line material inherited
from the base shape. Ordinary legacy files execute their original command body,
including unchanged parenting and appearance. The shared component-document probe
is factored out of the existing Part Boolean bridge without changing its policy.

The same local-input/defining-document support boundary as G1.7b3o applies. No new
Section algorithm, task workflow or cross-component transfer policy is introduced.
Four focused cases in TestPartBooleanInputs cover command refusal, accepted
ownership/Undo/save, the existing dialog's Section Apply/Undo, and legacy parenting/
policy bypass. A separate-process fixture checks persisted identity, dependencies
and source-driven section recompute. WORK_STATE owns the results and limitations.


### Part Compound integration (G1.7b3q)

Part_Compound checks the complete unresolved selection through the existing Part
preflight before native normalization or transaction creation. Its component path
creates the native Part::Compound in the edited definition; original input owners
remain unchanged. The original ordered, duplicate-free Links assignment and native
shape algorithm are retained. Links are dependencies, not ownership edges. Native
ViewProviderCompound still hides the sources and propagates their face appearance.
History includes the owned inputs before the compound. Legacy documents use the
original command creation path and bypass the component policy.

The same local-input/defining-document support limit as G1.7b3o applies, including
unused-model editing. The helper retains its existing require_part_boolean_inputs
name; its support/error wording now covers both Boolean and Compound consumers.
No cross-component transfer policy or Add Reference Feature workflow is inferred.
Compound link editing/drag-and-drop and other geometry consumers remain separate
intake paths; this milestone covers creation through Part_Compound only.
TestPartBooleanInputs adds four focused Compound cases and a separate-process
identity/dependency/source-edit probe. WORK_STATE owns build and runtime results.


### Compound link-edit admission (G1.7b3r)

ViewProviderCompound preflights new inputs at native drop eligibility, full-context
drop, bare drop and replacement hooks. Occurrence-qualified drops retain their
owner/subname until the shared component policy checks Reference/Excluded state.
Tree replacement also queries the Compound parent's full-context drop preflight
before its later identity-only replaceObject call and before any model mutation.
The target compound must belong to the edited component. The currently supported
inputs belong to that same definition, edited from its defining file, matching the
creation support boundary. Component compounds explicitly force drop-only behavior,
overriding the native extension's transfer permission to preserve original owners.
Legacy transfer permission is unchanged; Links remain dependencies. Removal through dragObject retains its native cleanup
behavior without an admission check.

DlgPropertyLink checks additions to Part::Compound.Links before accepting and keeps
the dialog open on refusal. PropertyLinkItem repeats the same preflight for every
selected target before its first write, protecting multi-object property edits.
The validator compares stable document/object/subpath identity, ignoring the cached
labels that native SubObjectT equality also compares, so removal/reordering
without additions remains available. Other object types/properties and ordinary
legacy documents retain their native behavior. This is a GUI consumer boundary:
scripting, file restore and recompute do not acquire a global property hook.

No new task workflow, reference promotion or foreign component transfer policy is
introduced. TestPartBooleanInputs owns focused native drop/replacement/property
editor checks and independent persistence; WORK_STATE owns actual acceptance and
remaining coverage limits.

### Split/join creation integration (G1.7b3s)

Native Boolean Fragments, Slice to Compound, Slice Apart, XOR, Connect, Embed and
Cutout preflight the full unresolved GUI selection before opening a transaction.
The shared component policy rejects unpromoted Reference, Excluded, missing Edit
and unsupported foreign inputs. Accepted inputs belong to the edited definition,
in its defining document. Native input links, algorithms and error dialogs remain.
This applies component rules to existing operations; no new operation workflow or
cross-component transfer policy is established.

New native feature results join the edited definition within the same transaction.
Slice Apart uses the native explode helper's ungrouped option and owns its Slice
and each native filter directly in component History. A separate document group is
not introduced into the component schema. Insertion is sequential because upstream
GeoFeatureGroup batch insertion expands shared coordinate-system dependencies
against the old membership and can duplicate related filters. Each sequential call
sees updated membership. Inputs retain their original ownership; native Abort rolls
back result creation and ownership together. Ordinary legacy documents retain
native parenting, including the Slice Apart group.

This boundary covers command creation, not later link/property editing, raw Python
assignment, file restoration or recompute. Those editing consumers are next.
TestPartBooleanInputs owns the focused command/ownership/Undo/persistence cases;
WORK_STATE records actual acceptance and limits. Add Reference Feature is separate.

### Split/join property-editor admission (G1.7b3t)

The existing DlgPropertyLink and PropertyLinkItem preflight now recognizes the
specific upstream Python proxy types for Boolean Fragments, XOR and Connect
(Objects), Slice (Base/Tools), Embed and Cutout (Base/Tool), and CompoundFilter
(Base/Stencil). The explicit proxy/property mapping lives in geometry.py. Matching
a generic Base or Objects property name alone does not opt another Python feature
into this policy. Ordinary legacy documents bypass the policy import.

Only newly admitted links are checked. The shared modeling validator requires the
consumer and new inputs to belong to the edited definition in its defining file,
and checks Reference/Excluded access before mutation. Removal/reordering remains
available without admitting new geometry. Rejected dialog acceptance leaves the
dialog open; the existing property item preflights every selected target before
writing any of a multi-feature edit. Native algorithms, property types, dependency
links, Undo and restore/recompute services remain unchanged.

This increment covers the property editor only. Split/join tree drop and replacement
are separate consumers and remain next; direct Python assignment is not intercepted.
No new workflow, automatic Add Reference Feature or foreign ownership policy is
inferred. WORK_STATE owns build/runtime evidence and the stopping boundary.

### Independent UI presentations (G1.6d)

General/Application owns three independent integer preferences: ModelPanelUIMode,
ToolbarUIMode and TaskPanelUIMode. Zero (and an absent key) selects Plus; one selects
Classic. The first three Application rows are the corresponding PrefComboBoxes.
Apply persists each choice and invokes the shared presentation controller. Cancel
does not apply draft choices. Native preference reset restores the Plus defaults.

FreeCADPlus/InitGui.py installs ui_modes at ordinary startup. A single-shot timer
coalesces startup/workbench events, without idle polling. Plus shows the Components
dock and hides the native tree while retaining the native property editor. Classic
hides Components and restores the native Model tree. Independent tree/property dock
layouts are also respected. On Plus startup/entry or replacement of the native
property dock, the controller stacks Components above Properties in the left dock
area. Ordinary workbench refreshes preserve the dock sizes. Components is
discoverable through the native Panels
menu. Closing/hiding the managed dock retains backend observers and Edit/view
contexts; changing UI mode never changes geometry eligibility or document schema.
The component panel can still be constructed explicitly by developer tests.

Toolbar and task modes initially use the same native presentation definitions and
commands. This is the owner's requested Classic-copy starting point; no new toolbar
layout or consolidated task workflow is claimed. Keeping command identities avoids
duplicated callbacks, features and Undo. Future Plus presentations must bind to the
same updated component/operation services as Classic adapters. In particular, native
Pad and Pocket already share PartDesign::FeatureExtrude::buildExtrusion, with fusion
and subtraction options supplied by their adapters. Both use the existing component
input protections independently of UI choice. This does not claim completion of the
planned consolidated Plus Extrude interface or every legacy adapter.

UI selection is presentation state, not a feature flag for using an old backend.
Native object/property identities and existing-file restore/recompute stay intact.
The native property editor and active native tasks remain available while mode
changes. Remaining normal component command/legacy-conversion integration and
unimplemented operation workflows retain their separate scope. TestUIModes (inside
TestComponentPanel.py) owns bounded acceptance with an isolated settings profile;
WORK_STATE owns results and delivery evidence.

## Native New File and definition-only New Part

Std_New calls document.new_document in both UI presentations: it creates the file
root, ordinary Part001 definition and its initial linked occurrence, then enters
Edit on Part001 as specified. Low-level App.newDocument remains unchanged for
upstream callers, macros and legacy fixtures.

Std_Part calls hierarchy.new_part for component documents or genuinely empty
native documents. It adds one unique PartNNN definition to the current defining
file's catalog, without creating links, moving selected objects, or activating the
new definition. Editing an external model targets that model's defining file and
Undo stack. Existing component Edit and selection context stay intact. The empty
native-document case initializes only the file frame and one unused definition in
one transaction, then edits the file. Existing nonempty legacy documents retain
the native Part path; this command does not silently convert loaded legacy content.

The native command is shared across Classic/Plus presentations; the full storage
chooser and separate instance-placement workflow remain deferred. Acceptance is
owned by TestNativeComponentCreation and WORK_STATE.

## Independent Plus toolbar presentation (TB.1 / TB.2a / TB.2b)

`freecad_plus/toolbar_layout.py` owns Plus modes, tab routing and Modeling groups.
`freecad_plus/toolbars.py` owns a separate Qt toolbar/ribbon widget tree, installed
through `ui_modes`. Classic toolbar widgets retain their parents, actions and native
layout. Plus shares native QActions/QMenus rather than command callbacks or feature
implementations. Native grouped commands therefore own their remembered choice;
Plus-only combined groups save their selected command under
`BaseApp/Preferences/FreeCADPlus/Toolbars`, resolving a selection by its native
command data rather than Python QAction wrapper identity. Shared actions retain native enablement,
checked state, shortcuts, tooltips, icons and transactions. Native commands remain
available through the copied Home/All Tools groups and the original workbench menus.

Plus owns caption layout: complete plain text, at most two balanced lines, with
natural minimum widths for long words. The scroll area's minimum height includes
page content and its horizontal scrollbar. Unavailable controls use the native
forbidden icon while keeping full accessible names/tooltips and disabled state;
this preserves the medium/small icon-only hierarchy without inventing operations.

Tab/mode navigation activates the corresponding available workbench, so its native
command lifecycle remains authoritative. An active task/editor prevents a ribbon
switch to a different workbench. View is presentation-only. Missing workbenches are
disabled; other registered workbenches remain selectable. There is no idle polling.
All Tools uses the complete ordered `Workbench.getToolbarItems()` inventory, which
includes workbench and global custom toolbars plus workbench manipulators. Every
separator and expanded command-group child is retained. The mode selector refreshes
its registry when opened, so later-added workbenches acquire routes without polling.
Closing the native Customize dialog queues one refresh. Plain QToolBars created by
that dialog are included when their names belong to the current native inventory;
Plus never observes/rebuilds pages on ordinary idle or toolbar paint/layout events.

The opt-in `Gui.Command.get(name).addToToolbar(toolbar)` API calls the existing
native `Command::addTo` factory on a separately owned Plus QToolBar. It validates the
PySide QToolBar argument and leaves native callbacks and action lifetime authoritative.
This creates separate specialized widgets (including the native workbench selector)
and complete expanded groups, without stealing Classic's single-widget actions.
Ordinary split buttons still share their native action/menu. Status-bar controls
created outside the normal toolbar inventory retain their native location/lifecycle.
The Plus native-toolbar scan recognizes QStatusBar descendants even when their
class is Gui::ToolBar (as in BIM). A transient FreeCADPlusStatusControl marker
preserves that ownership if upstream layout restoration reparents the widget.
These controls do not acquire Plus visibility bookkeeping or suppression; their
native owner continues to show/hide them when workbenches change.
Spreadsheet appends two QtColorPicker widgets outside the command inventory.
Plus discovers those untagged QWidgetActions in the realized toolbar and uses the
opt-in SpreadsheetGui.copyColorPicker(source, toolbar) factory. It creates and
attaches the same native picker class/palette to the separately owned QToolBar,
returns None, forwards colorSet to the original picker, and
mirrors native color changes with signals blocked. Existing Spreadsheet handlers,
selection and Undo remain authoritative; originals retain their parents/names.
Transient nested Plus toolbars are excluded from the Classic manager's widget scan.

While Plus hides Classic widgets, `FreeCADPlusClassicVisible` and
`FreeCADPlusClassicAvailable` preserve their logical native state. The small scoped
`ClassicToolbarStateGuard` in ToolBarManager exposes that state only during existing
setup/save/restore/context operations, then captures the native result and hides the
widgets again before returning to Qt. Nested guards skip already-managed operations;
unmarked toolbars follow unchanged native logic. This prevents Sketcher's explicit
enter/leave SaveState calls from persisting Plus suppression as user visibility.
Returning to Classic removes these transient properties and restores the native
contextual state. No document/property identities or geometry services change.

The separate primitive menu shares original native actions and adds the disabled
owner-requested Tab entry without modifying Classic's menu. Missing Plus operations
remain disabled; no command is substituted for Add Reference Object. Consolidated
operation tasks and complete ribbon placement remain separate from this adapter.
WORK_STATE owns build, native interaction and persistence evidence.

## Plus Design directional selection (TB.2c1)

`freecad_plus/selection_toolbar.py` owns the Design-only top-row control. It saves
`Directional` (default true) under `BaseApp/Preferences/FreeCADPlus/Selection`.
The active Plus Design presentation exposes that value as the transient main-window
property `FreeCADPlusDirectionalSelection`; Classic and other modes remove it.
No document properties, object identities, occurrence paths or geometry are changed.

`Gui/Selection/PlusSelection.h` reads this policy for native consumers. An absent
property leaves Classic semantics intact. Standard Box Selection/Box Element
Selection use native intersection for right-to-left when enabled, otherwise full
enclosure for rectangles in Plus. Classic retains its native center test and crossing
behavior; polygon selection retains its native policy. Nested object traversal,
transforms, subelement extraction and final command gate admission remain native.
The standard selection callback marks its viewer only for that tool's lifetime;
rectangle styling uses this marker so Box Zoom and feature-specific pickers retain
native visuals. Sketcher uses the same policy for its existing enclosure/touch tests
and themed solid/dashed feedback. Existing command selection gates are never replaced.
Operation persistence and Layers remain unimplemented parts of
the Selection/Layers scope. Curve intent is implemented by the adapter below. Runtime evidence belongs in WORK_STATE.

## Plus Design curve intent (TB.2c2a)

`freecad_plus/curve_selection.py` expands edge picks from native viewport left-button
events in Plus Design. The Selection toolbar owns a separate icon/arrow split
button with Single Curve, Connected Curves and Tangent Curves. Its selected action
is saved as `CurveIntent` under the existing Plus Selection preference group; the
default is Single Curve. Rebuilding the ribbon retains this choice. Classic and
other modes disable the observer's expansion; programmatic command/collector and
tree selections are not expanded. The adapter never replaces native selection gates.

Native `resolveSubElement` and `Part.splitSubname` resolve mapped geometry names and
preserve the original occurrence prefix. Traversal uses only the selected owner's
geometry, never spatial proximity to other document objects or occurrences. During
Sketcher edit it uses native Geometry indices, including construction curves; outside
edit it uses displayed Shape edge indices. Solid-edge joins require shared native
vertices, so overlapping independent solids do not become connected. Drawing edges
use native endpoint positions/tolerances, floored at OCCT linear confusion (1e-7 mm).
Closed single edges remain single items. Tangent traversal requires an unbranched
junction and parallel native normalized endpoint tangents (cross magnitude at most
1e-7); undefined tangents stop traversal. These are implementation tolerances, not
new owner-specified UI values.

A spatial endpoint index builds the adjacency graph; it is reused only within one
input event and discarded at the next event-loop turn. No graph or geometry snapshot
survives later edits. Expanded entries enter `Gui.Selection.addSelection` with their
original root/path, so current native command filters still apply. No geometry,
Undo entries, document properties or persistent identities are created by selection.
WORK_STATE owns native interaction, coverage and restart evidence.

## Plus Design selection categories (TB.2c2b)

`freecad_plus/category_selection.py` owns the eight checked categories in the
Design Selection row: Planes, Bodies, Surfaces, Faces, Edges, Curves, Points and
Vertices. Values live under the Plus Selection `Categories` preference group;
absent values are true to preserve existing selection access. This checkbox menu
has no default command. Existing command split buttons retain their icon/arrow
and last-used behavior.

Classification resolves native mapped subelement names and linked occurrence
owners. Datum planes map to Planes; origins/datum points to Points. Sketch edges
are Curves, including construction geometry; sketch vertices are Points. Solid
owners supply Bodies/Faces/Edges/Vertices. Sheets without solids are Surfaces;
standalone edges and points supply Curves/Points. Native constraint/axis editing
and workbench objects outside this geometry taxonomy retain their native admission.
No document properties, topology, identities, ownership or Undo state change.

The native Selection singleton owns a separate Python-backed Plus gate. Its
`setPlusSelectionGate` entry point does not replace `ActiveGate`, and removing a
command gate does not remove the Plus gate. The gate reference is released under
the Python GIL during singleton destruction. The new private member is appended
to the class, preserving existing member offsets for native consumers.

A viewport mouse event temporarily sets `FreeCADPlusCategoryPicking` on the main
window. During that event, native preselection and single/batch selection must
pass category admission and any active command gate. Previously ungated batch
paths check the command gate only in this Plus scope; Classic and programmatic
batch behavior remain unchanged. Non-viewport tree/script selections are outside
the scope. The property and classification cache clear at the next Qt turn or
presentation change. Mode changes unregister only the Plus gate. Checkbox changes
clear stale preselection but do not remove an existing selection. Curve-intent
expansion enters the same admission path. WORK_STATE owns runtime evidence.

## Plus Sketcher click selection (TB.2c2c)

The existing Design-only `PlusSelectionPolicy.enabled` presence flag also scopes
Sketcher click semantics; the Directional value itself does not govern clicks.
In `ViewProviderSketch::mouseButtonPressed`, only a completed plain left click on
a point, edge, axis or constraint clears the preceding selection before native
admission, retaining the current hover metadata needed to commit the pick.
Repeating a plain click retains the clicked item. Clearing happens at
release, after native drag/click classification, so drag initiation, box selection
and right-click picks retain native handling. Ctrl/Shift clicks keep native toggle
behavior. Native mapped names, occurrence paths, command/category gates and Curve
Intent expansion remain authoritative for the replacement selection.

An ordinary empty click clears selection. Plus Ctrl/Shift empty clicks preserve it;
Classic retains its existing modifier policy. An idle Escape press with a selection
clears it and uses the native unmatched-release guard to consume the release without
closing the sketch. Active drawing handlers, geometry/constraint drags and empty
Escape handling remain native. No persistent preference, geometry change, command
wrapper or operation-completion policy is introduced. Operation persistence and its
toolbar toggle remain separate work. WORK_STATE owns acceptance evidence.

## Plus operation selection retention: Equal / Construction (TB.2c2d)

The Design Selection row owns the `Persistent` boolean (default true) in the
existing Plus Selection preference group. It publishes the transient
`FreeCADPlusPersistentSelection` main-window property alongside Directional;
Classic and other modes remove it. `PlusSelectionPolicy.persistent` requires the
Design presence flag as well as the checked value. The icon-only control uses a
native icon and explicitly describes the currently integrated command scope.

Native Sketcher Equal and Toggle Construction consult this policy only at their
successful completion cleanup. They keep the existing native selection instead of
clearing and reconstructing it from names or shape indices. Equal does not replace
input geometry; Construction changes its geometry mode without changing its
Sketcher identity. The same selected construction edges can therefore feed another
native command even though construction geometry is excluded from the public Shape.
Native transactions, solver diagnostics, command filters and failure paths remain
in charge. Rejected Equal inputs stay selected with either toggle value.

The change does not intercept generic clearSelection, wrap QActions, replay stale
subelement names, or change drawing-handler, deletion, Undo, Escape, empty-click or
editor-exit cleanup. Classic retains its original post-command clearing. This is
the confirmed Equal-to-Construction retention increment; TB.2c2e below extends it
to basic preselected constraints. Geometry-changing commands, asynchronous modeling
tasks, the contextual palette and Move Components' task-local retention choice
are not integrated by this hook.
Broader retention must establish surviving-entity identity and operation completion
at each owning service before sharing this preference. WORK_STATE owns validation.

## Basic preselected constraint retention (TB.2c2e)

The existing Persistent Selection policy also covers the native Horizontal/Vertical
(and automatic HorVer), Parallel, Block, Coincident/concentric, Point on Object and
all three Symmetric input forms. The native legacy coincidence commands share the
same implementation as Unified Coincident; no command identities or menu dispatch
are replaced. Equal uses the same completion helper. Dimensions, direct Tangent/
Perpendicular and other unlisted operations remain outside this increment.

CommandConstraints.cpp owns finishConstraintSelection(applied). It retains native
selection only in Plus Design with an idle edited Sketcher view and either a
successful operation with persistence on, or a rejected operation. All other cases
use native clearing. No global clearSelection interception or selection replay is
introduced. Constraint creation preserves input geometry identities; the selection
therefore continues to refer to native points/edges after the solver changes their
coordinates. The native solver, transaction boundaries, warnings and Undo remain
unchanged, including Block's existing per-edge transactions.

Coincident/Point-on-Object can replace existing tangency constraints. Their shared
substitution cleanup uses the same helper: these callers select geometry, not the
constraint indices being removed/replaced. The helper checks STATUS_NONE, so active
continuous constraint handlers retain their own clearing/reset behavior. Coincident
passes whether any constraint was applied after its commit/abort decision. Block's
rejected point/external input path similarly keeps Plus inputs with either toggle
value; Classic retains its previous rejection cleanup. Native deletion, sketch exit,
ordinary empty click and Escape are not redirected by this integration. WORK_STATE
owns build, interaction, inventory and restart acceptance.
