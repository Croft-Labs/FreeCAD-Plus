# Component documents and History

Owner-approved contract, 2026-10-01; file hierarchy revision, 2026-10-09. Implementation and validation status belong
to roadmap 7.8. This supersedes conflicting part/navigator terminology and the
former opt-in legacy-conversion policy; it does not claim completed implementation.

## Ownership, instances and files

- UI names: **Models**, **Part Tree**, **History**, **Attributes**, **Add Component**,
  **Add Reference Object**, **Convert to Dumb Object**, **Instances > Add Instance**,
  **Copy to Domestic Components**, **Copy to External File**, **Import Component File**.
  Documentation may say sub-component; UI calls every instance a component.
- A component definition owns ordered history, evaluated result objects, child
  component instances and optional assembly constraints. Geometry and children
  may coexist. Bodies are results, never prerequisites for sketches or operations.
- Models is the first tab: domestic definitions appear first (master first), then
  collapsible imported-file groups listing every definition, including unused ones.
  Imported files can contain nested imported-file groups. File imports exist
  independently of placements and remain after deleting the last placed instance.
  Show domestic names without qualification and external names as `M3 screw (Hardware)`;
  qualify identical filenames by path where needed. Names must be unique within
  each defining file; matching names across files never merge their identities. Show each
  model's number of linked occurrences in the owning file's assembly, expanding
  repeated nested uses. The file root is a model/context, not an implicit linked
  instance, so it normally has count zero. Selection supplies native Attributes;
  Edit opens the same model, including models with no placed instances. Add Instance
  inserts that model into the active component without creating another definition.
- Add Reference Object is an operation command/button beside Extrude, not a
  creation entry in the Part Tree or History context menus. It uses the active
  component and preserves the existing direct-child evaluated-geometry contract.
- Entering a component makes its Origin visible by default in History. The eye
  remains editable; refresh preserves a deliberate hide until the next entry.
  Origin Planes is a child row controlling the native XY/XZ/YZ planes together.
  It starts hidden on entry; manual visibility persists through refresh and is
  undoable. Showing planes also shows their Origin parent. Both rows are permanent,
  cannot be suppressed or deleted, and reuse native origin/datum identities.
- Part Tree starts with the top-level component (Part001 by default),
  with linked occurrences beneath it. This permanent root context is selectable
  and editable, not a linked instance; it cannot be deleted as an instance and
  does not increase instance counts. Renaming updates its displayed label. The
  native Model pane is replaced with Attributes, retaining the native View/Data editors.
  Preserve native dock/command identifiers internally for layout compatibility.
- Every New File creates its first component as the permanent **master component**.
  Reuse the persisted `RootComponent` identity; renaming does not change its role.
  It cannot be deleted and is always first in Models and Part Tree. Activating or
  opening another component changes the editing/History context, never this order.
  Part Tree displays the master assembly first, followed by separate unused
  component assemblies at the same top level. Their child instances remain nested
  beneath them; they are not links in the master assembly and add no master instance
  or BOM count. Cover unused descendants beneath their unused parent rather than
  adding duplicate top-level rows. Removing the last master use exposes the retained
  definition in this unused inventory; adding a use places it back in the master tree.
- Each `.cadprt` has one root component and domestic definitions. New Component
  offers domestic storage, a new external file, or an existing external file.
  Adding to an imported Hardware file creates and saves a domestic definition there;
  importing that file exposes all its definitions. Definition identity remains
  distinct from occurrence identity, names and paths.
- Insertion uses the active component's defining file: its domestic definitions or
  directly imported files. Nested imports are visible but are not implicitly imports
  of their ancestors. Import into the active defining file before inserting from
  another file. Block component cycles and file cycles before any graph mutation.
  Before importing, check the combined existing and incoming file graphs for distinct
  loaded files claiming one document identity. Reusing the same loaded file through
  multiple branches remains valid; Save Copy does not create independent identities.
- Repeated instances share a definition with independent placements and display
  overrides. External edits save in the defining file; assemblies reopening it see
  those saved changes. There is no name-based domestic override or shadowing.
- Copy to Domestic Components creates independent identities for the copied
  definition and its domestic child hierarchy. Already-external child definitions
  remain explicitly imported and shared. Prompt for the owning placements to replace,
  initially selecting none; cancel retains the new copy and existing placements.
  Replacement preserves placement and occurrence identity. Unsupported expressions,
  outside-owned inputs and consumer/path remapping must refuse before mutation.
- Copy to External File creates a separate independent definition file and retains
  the original definition and placements. Do not expose identity-moving conversion
  as a normal user action. Legacy migration services are not the copy workflow.
- Move Components changes child LinkPlacement values owned by their immediate
  parent definition. The change applies to every use of that parent, including
  its standalone view. Never add a display-occurrence placement override. Accept
  only whole direct siblings within one exact parent occurrence context; preserve
  that path for world-reference conversion and transform descendants implicitly.
  The permanent root/master is a context, not a movable instance. External parents
  are edited in their owning file. See the Move Components interaction contract in
  [UI_UX_SPEC](../UI_UX_SPEC.md#move-components).
- Opening a component in a tab creates a view/edit context of the same definition.
  Embedded edits save with the owning file; external edits save with their file.
  The tab identifies both component and owning file. It is not an extraction.
- Native grouping, App::Link, OpenCASCADE geometry, properties, dependency graph
  and transactions remain reusable infrastructure. A new component/result layer
  owns the semantic contracts; tree flattening alone cannot implement them.

## Part type revision (October 10 owner contract)

This revision supersedes the older Hidden/path-override display contract below
when the new workflow is integrated. The first backend milestone is additive;
the existing Part Tree still uses the legacy representation service.

Part types are Full Component, Bodies Only, Excluded and Reference. An authored
type belongs to the owning part's direct occurrence, shared by every use of that
owning definition. Other parents referencing the same child remain independent.
The optional native String property PartType on the occurrence stores an
explicit setting. Absence reads the owner's direct legacy override, then the
occurrence's Representation; legacy Hidden maps to Excluded. Nested legacy
overrides remain intact and are not silently written into shared definitions.
An explicit reset stores Bodies Only. Native copying carries the property with
the occurrence, without creating a new UUID registry or remapping labels.

ComponentModel.set_part_types validates the whole direct-child batch before one
native transaction. It changes neither linked source definitions nor visibility,
BOM/mass flags, placements, history or native engineering shapes.
effective_part_type resolves a requested occurrence path against an explicit
active path. The active part defaults to Full Component, its children default
to Bodies Only. A Reference is displayed only when its direct owner is active;
elsewhere its effective type is Excluded, with the authored value preserved.
Nested exclusions still win. Editing an excluded component directly restores its
own context without changing the outer owner's exclusion.

part_type_allows_geometry is the consumer policy boundary for unpromoted
occurrence geometry: Reference and Excluded paths are refused independently of
their display visibility. Reference geometry requires the explicit Add Reference
Feature operation before any modeling use. A promoted Reference Body is an owned
body of the active part with an associative source link. Merely setting Reference
does not create that feature. The later Promote-like workflow is separate scope.
Connecting the policy to selection, modeling and export consumers is a required
subsequent gate; this backend API alone does not prevent existing consumers from
using raw native Link shapes.

The first consumer integration is ComponentModel.require_geometry_access.
current_shape and BasicShapes.ShapeReferences.linked_shape call it before reading
geometry. It inspects native occurrence paths, rejects Reference/Excluded links,
and refuses an unfiltered whole-component aggregate containing a forbidden
descendant. A permitted sibling path is checked independently: referencing one
use of a shared definition does not forbid its other normal occurrences.
The shared validate_link also requires a component-owned consumer to use an
owned reference instead of a bare foreign component member whose occurrence
placement is missing. Ordinary non-component geometry keeps its native behavior.
ShapeReferences retains its ReferenceError contract.

Owned reference features deliberately stop this access check at their own object.
Their SourceOccurrence/SourceObject links remain the explicit authorization and
associative dependency, including when the source occurrence becomes Excluded.
Adding a reference does not reclassify the child. Native cached operation shapes,
direct native exchange exporters and other consumers bypassing these shared
services still need integration. No blanket native export protection is claimed.

Files containing explicit PartType properties require component-part-types-v1.
The manifest records each authored value with its occurrence identity; preflight
cross-checks it against Document.xml and rejects missing capability declarations
or altered values. Older readers must refuse these files. Files without authored
new properties retain their old capability set. Rollback to an older reader
requires an explicit reviewed conversion, not stripping the capability.

Pending integration includes saved active-self overrides, activation and double
click, Part Type labels/menus, shown/hidden separation and effective Excluded
visibility refusal, legacy nested-rule reconciliation, reference use guards and
output traversal. Parent/sibling contextual transparency remains at least 75%;
children retain their authored appearance. The existing UI is not yet changed.

## Part Tree and representation

- The Components panel identifies the active component, without a filename/path or
  inline creation buttons. Add Component lives in context menus; Add Reference
  Object lives beside Extrude in the modeling toolbar/menu. Component tabs may
  still identify their owning file.
- The first tree column is the part name. Repeated occurrences of the same definition
  under one parent collapse into one row by default, with an instance count such as
  **x5**. **Expand Instances** reveals rows such as **support_angle#005**; **Collapse
  Instances** restores the grouped view. The number is a persistent display number,
  separate from the occurrence UUID; labels and numbers are not reference identities.
- Highlight the active component and provide a show/hide control. The active component
  and its ancestor branch cannot be hidden. Group actions apply to the represented
  occurrences; Copy to New Part requires an individual occurrence.
  Expanded instance rows identify the exact active occurrence; the grouped row
  remains highlighted when it contains that occurrence.
- Delete Instance/Instances and Delete key remove only represented owning links,
  never definitions, their geometry/history, or child definitions. Deleting a shared
  model's child link changes that child in all uses of the shared parent model,
  consistent with definition ownership. Deleting every placed use leaves Models
  showing the reusable definition with zero instances. Undo/Redo and save/reopen
  preserve unused definitions. References to removed instances keep their identity
  and become missing-source items for repair; cached geometry is not current.
  The generic Delete command also protects definitions and routes precise occurrence
  picks to link deletion. Removing the active occurrence returns editing to its
  nearest surviving parent. Models does not offer destructive definition deletion.
- Part Tree Cut/Paste and drag/drop rearrange existing owning links within one
  root and owning file. Cut stages a selection without deleting it; Paste appends
  it under the chosen part. Drop on a part reparents; drop above/below an instance
  orders siblings; drop on empty space appends at the root. The root cannot move.
  Group rows move all represented instances; expand a grouped destination first.
  Selected branches include their descendants once. Preserve identities, model
  reuse, geometry and placement in the chosen occurrence context. Reserve existing
  destination instance numbers, assigning a new number only to an incoming clash.
  Shared definition child-list changes apply to every use of that definition.
  One transaction supports Undo/Redo and persisted Group ordering. Refuse cycles,
  stale clipboard paths, cross-file edits, driven/scaled links, consumer relationships
  and path display overrides before reparenting; sibling ordering remains available
  with references/overrides. Relationship repair/remapping is separate scope.
- **Edit** is the first context action; double-click also activates the definition
  for editing. **Add Component** adds to that definition. Omit **Open Component in
  Tab** on the root row, which is already its own view. Use an **Instances** submenu
  for **Add Instance** and **Copy to New Part**, and **Copy to External File** for
  independent copying. **Part View** contains Full Component, Bodies Only, Hidden and
  Reset to Inherited. The view root is displayed in full; these settings apply to
  occurrences added to a parent.
  Indicate the effective Part View choice (no single choice for a mixed group)
  and whether an occurrence inherits its setting or has an override in this context.

- Contextual transparency is a view-only layer. Keep the native viewer root,
  camera and selection graph attached; hide native drawing within its selection
  separator and render unpickable per-occurrence display links beside it. Remove
  only the view-owned hiding/display nodes when leaving the context. Separate
  component tabs use a dedicated snapshot separator so child editing can apply
  the same layer without changing shared view providers or saved appearance.
  Ignore contextual refreshes until a newly created tab has its component context.

- Each child instance defaults to **Bodies Only**. It exposes finished solid/sheet
  results plus child instances evaluated under their own representation settings.
- **Full Component** also permits normally visible sketches, curves and construction
  objects; it does not reveal hidden inputs or every historical intermediate.
- **Hidden** hides the complete branch. It does not imply suppression, unloading,
  exclusion from BOM/mass, or removal of geometry needed by a dependency.
- Parent levels inherit child settings. A higher-level override is keyed by the
  occurrence path, never by label, and does not modify the shared child definition.
  **Reset to Inherited** removes that override. A Hidden ancestor wins.
- Do not introduce a Reference Only component role. BOM/mass inclusion remains
  separate. The owner may revisit reference-only display behavior later.
  BOM participation belongs to the occurrence in its owning component; changing
  a shared definition's child applies to all uses of that definition. Excluding an
  occurrence omits that branch from BOM counting without changing display or mass
  settings. Component BOM rows represent components, not their modeling history.
- Definition-owned constraints belong in History, not among occurrence rows
  in Part Tree.

## History and evaluated objects

Automatically created root definitions are labeled Part001; subsequent new
definitions default to the next available PartNNN within the owning document.
Nested definitions share that sequence. Explicit labels remain authoritative.
Occurrences reuse their definition's label and existing instance-number display;
they do not create a new part number. Native object names/UUIDs retain their roles.

- Component Extrude may consume a subset of curves from one sketch. The selected
  contours must be closed, non-self-intersecting, mutually non-touching and form
  one connected region with optional holes. Unselected sketch geometry is unused.
  Picking an interior region collects its outer boundary and immediate holes.
  Persist selected subelements as a native LinkSub on a component-owned Internal
  profile, not copied independent curves or label references. Recompute validates
  the subset and invalid/missing inputs require repair. Keep the published result
  identity through edits; the internal profile is not a History item.
- Component Extrude extent restoration reuses the native Pad geometry engine
  directly under a definition, without an auxiliary PartDesign::Body. Preserve
  native extent/start/limit properties and dependencies. Selected profiles retain
  the sketch coordinate frame and signed normal as native Part2DObjectPython
  helpers; use exact rigid transforms that preserve analytic curves. Legacy simple
  Extrusions/Booleans remain readable and migrate only on reviewed editing, with
  stable operation/result UUIDs and transactional rollback/Undo. Preview overlays
  and temporary target transparency never persist as model geometry.
- Every component always shows its native **Origin** as the first History
  item, including empty components and isolated views. It is permanent and cannot
  be suppressed or deleted; its visibility can be toggled. Origin Planes is its
  permanent child visibility item, hidden by default. Reuse native identities.
- The Components pane displays that item as **Origin**, without a document-wide
  numeric suffix. Default object/operation labels are numbered within their owning
  component, starting at **001**: Sketch001, Body001, Extrude001, etc. A second
  component starts its own sequence at 001 even in the same file. Preserve custom
  labels; reserve labels already used in that component. Native object names and
  UUIDs remain unique identities, and references never resolve by these labels.
- An **item** means an object or an operation. Show a suppression checkbox, then
  a visibility icon, then the item name. Checked means active, unchecked means
  explicitly suppressed, and partially checked means inactive because of an input.
  Visibility is separate from suppression and does not change dependencies.
- Display objects and operations in creation/history order. Reusable inputs and
  result identities are separate from producing operations. Solid/sheet results
  expose geometry; editable parameters remain on their operations.
- Owner feedback 7.8.7t: generated solid Body results are protected background
  objects, omitted from native Model and History. Their producing operation
  (for example Extrude001) is the public solid with visibility/edit/delete controls.
  Engineering picks retain the stable internal result identity. Existing results
  adopt this display without UUID changes. Deleting an operation removes its unused
  result in the same Undo transaction; referenced results stay unavailable for
  explicit repair. GUI deletion of background results is blocked, including forced
  deletion. Freezing exposes the retained result as an independent dumb Body again.
- Suppressing an operation disables its dependent operations, not independent
  branches. Restore the preceding eligible body state; never silently reconnect
  dependent features to different geometry. Unsuppress preserves explicit user
  suppression on other operations. Blocked, suppressed and failed are distinct.
- Retain the stable result lineage and reference-repair rules in
  [the history contract](PART_HISTORY_CONTRACT.md#identity-and-dependencies-714).

## Add Reference Object

- Select a direct child **occurrence** and an object owned by its definition.
  Eligible geometry: solid bodies, sheets, sketches and curves. Grandchildren,
  unrelated definitions and implicit traversal into their results are forbidden.
- Copy evaluated geometry in the parent's coordinate frame, retaining source
  definition/object/occurrence identity. Do not copy generating history or sketch
  constraints. Referenced sketches are dumb sketches (evaluated geometry only).
- The parent can operate on the copy without modifying the source. Source edits
  mark the copy pending; activating/editing the parent refreshes it and recomputes
  dependents. Missing, suppressed, failed or ambiguous sources require repair;
  cached shapes must never be advertised as current engineering results.
- Parent operations depend on the reference result; they are not baked into or
  overwritten by source refresh. Cycles are refused before committing changes.
- Repair or explicitly change a reference's direct-child source without replacing
  the reference object, its history position, authored suppression or valid whole-
  object consumers. Keep the same geometry kind. Refuse unreviewed face/edge or
  expression remapping before mutation; a failed dependent rebuild rolls back.
- Missing reference geometry must not close an otherwise structurally valid document
  or prevent independent references/operations from updating. Report each broken
  reference in History and retain its saved source identity for repair. This
  does not relax format, component-graph or external-definition identity checks.
- No separate snapshot option in this command: independent copies use Convert
  to Dumb Object. Adding a reference does not change its source's display type.

## Missing component files

Locate Component File resolves the saved definition identity and restores matching
unresolved instances in the same owning document together, preserving occurrence
identity and placement. Missing evaluated objects remain separate reference-repair
items; they do not prevent recovery of healthy geometry from that component.
Recovering an imported file preflights all matching definitions, then restores its
file reference, placements and evaluated-reference bindings in one owning-document
transaction. Refresh only after all bindings are restored. One Undo reverses the
complete file repair, and a failure rolls it all back. Single-component recovery
uses the same binding service; unavailable geometry remains independently repairable.
Component Structure retains missing instance groups and numbered rows, and prevents
geometry-dependent actions from implicitly creating replacement definitions.

## Convert to Dumb Object

The dropdown has **Delete Parameters** and **Extract Dumb Body**. The conversion
review identifies exclusive history to remove and shared upstream items to retain;
Cancel leaves the document unchanged.

- Delete Parameters freezes the selected current body/sheet, preserves its object
  identity and valid downstream references, and removes only history exclusively
  used to generate it. Shared operations/inputs needed by other results remain;
  detach only the selected result's contribution. Preflight ambiguous references
  before commit. Frozen reference results no longer update from their source.
- Extract Dumb Body retains all original history and creates a new, independent,
  unlinked geometry object with a new identity. Sheets and evaluated sketch/curve
  copies retain their geometry kind despite the owner-selected action wording.
- Both actions are transactional and undoable. Shape equality alone does not
  establish reference preservation or shared-operation correctness.

## File assembly solver boundary

The native solver membership pilot recognizes an Assembly::AssemblyObject marked
ComponentRole=AssemblyContext with a ComponentRoot link to a same-document marked
file App::Part. Both placements must remain identity. getAssemblyComponents borrows
the file's direct Occurrence links as rigid bodies; it does not reparent occurrences,
flatten component definitions or put solver geometry in file History. Existing
AssemblyObjects without this opt-in retain ordinary native Group traversal. Invalid
root/type/frame or non-occurrence membership is refused before gathering bodies.

ComponentModel.ensure_assembly_context creates the unique context and its native
JointGroup transactionally and idempotently. Model.validate/assembly_record check
context/group ownership, fixed context placement, absence of geometry, and native
ground or two-endpoint joint membership. Endpoints must be distinct direct file
occurrences; definition ownership may be external. Occurrence removal/reparenting
refuses referenced endpoints until their relationships are removed. Native solver
status updates defer during restore and Undo/Redo, when links are incomplete.

CadDocument declares component-file-assembly-v1 only when a context exists. Its
assembly record identifies the context UUID/native name, root, joint group and
joint native names/endpoints. Preflight cross-checks these against native XML;
restore checks the live graph again. Native connector/solver parameters retain
native persistence. Older readers lacking the capability refuse the file. Existing
files without contexts do not acquire the capability.

ComponentModel.ground_occurrence, create_fixed_relationship,
edit_fixed_relationship and remove_relationships provide the bounded Ground/Fixed
transaction service. Creating the first ground also creates its context in the
same Undo step. Fixed relationships connect two direct occurrences using explicit
local connector frames; creation requires a connection to ground. Editing preserves
joint/endpoints and changes only detached connector frames. Ground removal clears
native Placement/LinkPlacement locks, which Undo restores. Relationship deletion
preserves the component models and occurrence identities.

Solve status alone is insufficient: a native solve may report success while moving
a grounded occurrence. The service snapshots grounded placements and verifies those
plus resulting active detached Fixed connector frames (native placement tolerance
1e-7). A failing status or violated postcondition aborts the complete transaction,
including joint creation, connector edits and solver-driven placement changes.
External definitions are referenced through local occurrences; source placements,
placement locks and saved source files are not modified by assembly transactions.

The Part Tree command adapter now uses these services. The accepted backend scope is
Ground and detached Fixed frames; other native joint types and interactive geometry
picking are not implied by these services. See TestComponentAssemblySolver,
TestComponentAssemblyPersistence and TestComponentRelationshipTransactions.

The first UI adapter is ComponentNavigator.file_grounding_target/set_file_grounding.
It requires the current file root to remain edited, a single ungrouped direct owning
occurrence, the matching active document and no active task/transaction. Menu actions
resolve stable row identities at invocation and recheck that context before dispatch.
Ground state comes from the native ground relationship, not a placement lock alone.
AssemblyGui loads without switching workbenches/tabs. Models, definitions and nested
occurrences cannot become file-grounding targets through this adapter.

Fixed creation captures two direct occurrence identities plus the file identity,
revalidates them at invocation, and supplies first-frame inverse times second-frame
as the detached connector offset. This preserves the current relative placement.
FileRelationshipsDialog obtains joints from assembly_record, validates both native
object identity and ownership before mutation, and uses native occurrence subpaths
for selection without changing Edit. Editing converts the two local connector
placements into one relative placement and applies it through the transactional
service. Unchanged acceptance and cancellation create no transaction. The dialog
shares the file Edit/task guard with grounding. TestComponentRelationshipsUI covers
actual QAction dispatch, selection, offset acceptance/cancellation, Undo, removal,
and stale file/joint refusal; broader compatibility and owner delivery remain 13f.

## File modeling task guards

The shared active_component resolver rejects file containers for modeling and
accepts them only for callers explicitly requesting allow_file. The shared
modeling_component validator also checks explicit sketch/plane task destinations
before TaskContext entry, previews or document mutation. Datum Plane availability
uses the edited component rather than selection. Existing feature editors retain
their owning component; the file cannot own modeling history/results. Occurrence
movement changes links under the file transactionally while its global frame stays
fixed and its History remains origin-only. This does not establish native assembly
joint storage compatibility; that audit remains roadmap 7.8.13e2.

Native Part Primitive, Extrude, Revolve, Loft and Sweep commands inspect component
document metadata and dispatch to the existing Primitive, Extrude, Revolve, Loft
and Pipe tasks respectively. They inherit the file-Edit guard and ownership
contract before task creation. A failed shared launch cannot fall through to its
legacy dialog. Documents without component metadata retain their native dialogs.
The common Part allowComponentModeling check protects Boolean, copy, shape,
datum, direct primitive and link-array paths in Command.cpp, CommandSimple.cpp
and CommandParametric.cpp at both availability and activation. In a file-container
document it requires a native active Definition that is not a file container;
geometry selection cannot supply that ownership. A missing active part is refused
as well. Legacy documents without a marked file retain native behavior. This is a
file-Edit guard, not new feature/history adoption for those operations. Inspection,
import/export and display routes are unchanged. Native Assembly solver ownership
and broader workbench fallback compatibility remain separate gates.

## Definition deletion

`definition_deletion_plan` reviews the selected definition and its native owned
Group, Origin and origin features. It never follows occurrence targets or geometry
inputs. Separate nested definitions are refused rather than recursively erased.
File containers and the metadata root remain protected. Any outside consumer,
including an occurrence, geometry dependency, expression or loaded external link,
blocks deletion until the user removes or repairs it. Closed dependent files cannot
be inspected by this in-memory guard; this service is not a global reference index.
`delete_definition` removes the reviewed objects in one transaction and validates
the surviving document. Undo restores the same identities and native ownership;
Redo and save/reopen support an empty file. Linked child definitions are retained.
Pending user edits are refused. Models Delete (one selected definition) and the
native bare-definition Delete adapter call the same service. The current file
context must own the definition; imported models require opening their defining
file. Preflight runs before view cleanup, so a refused operation retains the edit
context. Successful deletion ends temporary unused views, closes the definition's
isolated tabs, and activates the file view. If only an isolated tab remains, create
a file view before closing it so the document survives. Undo restores objects but
not closed view tabs. Part Tree occurrence deletion stays separate. Native mixed
selections are consumed and refused instead of falling through to generic deletion.
The native blanket definition guard remains a fallback when no navigator is active.

## Persistence and conversion

The October 9 file-root revision uses `ComponentModel.ensure_file_container` as an
explicit migration service. It retains the previous native root definition and all
its children/history/IDs, adds one native occurrence beneath a new identity-frame
App::Part, and changes only the metadata root binding. The operation is idempotent
and transactional, including undo/redo. Existing external links keep targeting the
previous definition. The user-facing new_file_document entry wraps an ordinary
Part001 and clears bootstrap undo records before the navigator activates its first
occurrence. Independent external copies, the retained externalize compatibility
service, and New Component with new-external-file storage wrap their completed
component in the same file container before final save and clear bootstrap undo.
They return the actual component definition, not the file container, and never add
an extra Part001 to the destination.

CadDocument._open now applies the same migration to newly loaded older .cadprt
files and dependencies, after verifying their saved manifests/native identities
and upgrading retained datum frames. It does not rewrite the original archive;
an explicit save records the new capability/root. Bootstrap undo is cleared only
for the newly loaded migrated file, so Undo cannot remove its pinned container.
Existing already-open documents are returned unchanged, preserving active edits
and dependency rollback guarantees. Failed opens discard newly loaded documents
and retain pre-existing ones. Reopening an upgraded file does not add another root.
Legacy structural conversion and evaluated recovery wrap the converted domestic
definition in the file container before committing their existing transaction.
The internal _wrap_file_container helper joins that transaction; the public
ensure_file_container service retains its independent transaction boundary. One
Undo reverses conversion and container creation together, and Redo restores their
identities. Failed container creation rolls back the structural conversion. The
file owns no modeling history/results; recovered geometry belongs to its domestic
component. No extra Part001 is created. External documents retain separate
transactions and must still be saved before their parent.

Activating the file refreshes reachable domestic component definitions once each,
children before parents, so reference snapshots precede their consumers. It does
not take ownership of external edits or add file-owned History/geometry. Broken
branches are collected without preventing independent domestic refreshes.

The container retains internal `ComponentRole=Definition` storage for native graph
and serializer compatibility, with readonly `FileContainer=True` distinguishing it
from a component model. It is the only marked object, must be the metadata root,
and cannot be an occurrence source or own modeling history/results/geometry.
`definitions()` still includes this storage root; UI inventories must filter it via
`is_file_container`. Its native label is internal; the intended file row displays
the document label. No existing component is renamed to accommodate that label.
Saved migrated archives require `component-file-container-v1`, with `file_container`
equal to the root UUID. Preflight cross-checks this declaration against the native
marker; readers without this capability must refuse the file before restoration.


- Versioned `.cadprt` format/capabilities, stable document/definition/occurrence/
  object identities and explicit external dependency records. A renamed FCStd
  without the component schema is not a valid `.cadprt`.
- Reuse native object serialization where compatible; preserve other workbench
  payloads and native type/property identities rather than rebuilding serializers.
- Validate required capabilities before restoration; refuse unsupported required
  content. Save atomically, retain backups and preserve recovery behavior.
- Before native restoration, validate manifest record types and unique identities,
  match definition names/IDs and every occurrence against native archive records,
  and verify each occurrence's owning definition and domestic/external designation.
  Missing, duplicated or reparented placements are format errors, not repairable
  missing-reference states. Earlier files without native DefinitionId still use
  the existing identity-upgrade path after restoration.
- A failed component-file open rolls back the entire newly loaded dependency graph,
  including native auto-loaded documents. Preserve previously open documents, their
  unsaved edits and the prior active document. Recoverable missing references still
  open for repair; they are not failed restores.
- Open supported `.FCStd` content as an in-memory conversion. Save a new `.cadprt`,
  leaving the original untouched. Report unsupported content, partial conversion
  and geometry-only recovery explicitly. Expensive legacy mapping is lower priority
  than the requested architecture; no blanket round-trip compatibility promise.
- Before writing a component file, reject a destination whose resolved path belongs
  to another open document, including direct or nested imported files. A refused
  Save As retains the original location and label; existing file contents remain
  unchanged. Relocation to a new path retains shared identities and dependencies.
- Native link serialization uses the final archive destination, not cached relative
  paths or a temporary ZIP filename. Save Copy must not retarget the live document's
  links. Export serialization retains its existing absolute-path behavior.
- Save As changes location without making shared definitions independent. An
  explicit independent-copy operation creates new semantic identities. Relocation
  and externalization must retain or explicitly remap dependency identities.

## Required end-to-end acceptance

### Incremental legacy conversion planning and recovery

Before changing ownership, inventory native definitions/containers, Body Group and
Tip, sketches, occurrences, placements, properties, expressions and dependencies.
Preserve native source identity and geometry evidence. Define shared-model boundaries
before creating instances; retain the permanent master context. Body-owned inputs
must be ordered by their actual dependencies, including attachments and expressions.
Structural ownership backlinks must not create artificial computational cycles.

Every feature-family conversion uses the same recovery order: mapped editable
feature, retained editable native feature, then explicitly reported dumb body,
sheet, curve or point from validated evaluated geometry. Recovery must preserve
the final useful output when available; it must report the loss of parametrics and
never claim a dumb result is complete feature migration. Stale caches, invalid
geometry, missing references and unavailable outputs remain explicit. Read-only
planning records candidates and failures; it does not create fallback objects.
See [inventory API and acceptance](../../tests/LegacyConversionPlan.md).

Structural migration reuses legacy Part identities and shared native Links, with
definition/occurrence identity kept distinct. Preserve Body Group/Tip/native inputs
until feature adapters migrate them. The narrow Sketch/first-Pad adapter orders
the native input and operation before the original Body result, preserving their
names/types/identities and downstream Body references. A hidden internal native
feature bridges the component-owned Pad to the Body's child-scoped Tip; native
Origins, labels and view providers remain intact. Preserve evaluated placement and
geometry, expressions and protected source files; unqualified histories remain
editable native payloads with explicit reports. See
[Body history pilot and acceptance](../../tests/LegacyBodyHistory.md).
Native datum/Origin identities and attachment definitions remain retained. Direct
datums are construction History inputs, not physical results. Body-owned datum
History links have distinct identities, a complete Body-times-datum frame and
native source references; they do not reparent inputs or create assembly instances.
Native attachment editing must preserve formulas/supports, and missing sources must
be reported. Upgrade recognized older converted content only after manifest/identity
validation, through one idempotent undoable transaction. See
[datum frames and acceptance](../../tests/LegacyDatumFrames.md).
Native sketch constraints, expressions, attachments and external references remain
on the original editable object. Shared consumers must not acquire independent
copies. Component-owned sketches stay independent; retained Body-owned sketches
have distinct-identity hidden History input links with complete native Body/sketch
frames and dependency order before their Body. Native consumers and ownership stay
intact until their feature adapter qualifies physical reparenting. The safe first-Pad
pilot permits dimensional expressions/independent external inputs but refuses
Body-dependent frames or property expressions. Missing sources require repair;
recognized older converted files upgrade idempotently after manifest validation.
See [sketch input mapping and acceptance](../../tests/LegacySketchInputs.md).
Qualified independent native Pad/Pocket chains retain original feature identities
while replacing implicit previous-feature targets with explicit published results.
Keep the original final Body as the result carrier with its child-scoped native Tip
bridge. Preserve native extents/formulas, normalize Pocket direction at the shared
editor boundary, and update mode/target consumption without replacing native objects.
Reject downstream self-targets and formula overwrites. Native Body-dependent/reference
histories remain editable through complete-frame History links with original engines;
available validated output precedes any explicit dumb recovery. Older converted-file
upgrades retain sketch/access-link UUIDs and original files. See
[extrusion mapping and acceptance](../../tests/LegacyExtrusions.md).
Qualified native Pipe histories use the same identity-preserving chain publisher,
with ordered profile sections and exact Spine/AuxiliarySpine references. Independent
input sketches precede their operations once; native orientation/transition and
transformation settings remain authored properties. Persisted native Boolean
presets allow shared mode/target edits without changing converted feature types.
Attached/non-sketch/unsupported histories retain original owners and native editors;
standalone Part Sweep retains its distinct solid/Frenet/linearization controls.
LegacyPipeVersion upgrades recognized earlier conversions after manifest validation.
See [Pipe mapping and acceptance](../../tests/LegacyPipes.md).
Bounded Helix/primitive adapters share this publisher without sharing their native
parameter laws. Keep Helix profile/axis and authored dimensional mode, and native
primitive shape/dimensions/placement. Converted mode edits preserve native types;
changing a converted primitive's shape requires a separate operation. Attachments,
unsupported references and standalone native engines retain editor access and
available geometry. Separate LegacyHelixVersion/LegacyPrimitiveVersion upgrades
recognize prior conversions after manifest validation. See
[Helix/primitive contracts](../../tests/LegacyHelixPrimitives.md).
Dress-up, pattern/transformation and Boolean compatibility adapters preserve native
owners and topology inputs. Hidden distinct-identity History links open original
editors, ordered by dependencies first and authored native Body Group across
families where compatible. Keep native
Originals/Transformations/settings/suppression and Boolean tool/target references;
standalone outputs remain direct to avoid duplicated compound geometry. Separate
family versions upgrade recognized older conversions after manifest validation.
Missing/invalid sources require repair; stale caches are not certified by retention.
See [bounded finishing adapters](../../tests/LegacyFinishing.md).
Retain original world geometry through explicit
definition-frame and occurrence-frame compensation, including native scale modes.
Original source files remain protected; external converted files are saved to new
cadprt paths in dependency order. Transaction/Undo boundaries are per document.
Unresolved occurrences stay visible for repair and cannot silently pass strict save
validation. Unsafe mappings may present explicitly labelled dumb evaluated outputs
while retaining native payloads; unverified caches and missing geometry remain
reported. See [structural mapping and acceptance](../../tests/LegacyStructureConversion.md).

One root with its own body and two instances of an embedded child, plus an external
child. Independent sketches feed operations without Body containers. Exercise
direct-child body/sheet/dumb-sketch/curve references, parent-only edits, delayed
refresh, nested representation overrides, constraints ordering, isolated tabs,
suppression with an independent branch, shared-producer parameter removal and
independent extraction. Verify undo/redo, cold reopen, source edits after reopen,
missing dependencies, legacy-original preservation and representative drawing,
CAM, FEM and Draft consumers. Track unavailable gates separately from passing ones.
