# Component documents and History

Owner-approved contract, 2026-10-01. Implementation and validation status belong
to roadmap 7.8. This supersedes conflicting part/navigator terminology and the
former opt-in legacy-conversion policy; it does not claim completed implementation.

## Ownership, instances and files

- UI names: **Models**, **Part Tree**, **History**, **Attributes**, **Add Component**,
  **Add Reference Object**, **Convert to Dumb Object**, **Instances > Add Instance**,
  **Instances > Copy to New Part**, **Save to External File**.
  Documentation may say sub-component; UI calls every instance a component.
- A component definition owns ordered history, evaluated result objects, child
  component instances and optional assembly constraints. Geometry and children
  may coexist. Bodies are results, never prerequisites for sketches or operations.
- Models is the first tab: a flat, non-expandable inventory of owning-file component
  definitions, including unused models and referenced external models. Show each
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
- Each `.cadprt` has one root component and embedded definitions, and may link
  definitions in other `.cadprt` files. New definitions are embedded by default.
  Definition identity is distinct from occurrence identity and labels/file paths.
- Repeated instances share a definition, with independent placements and display
  overrides. Copy to New Part copies the selected definition and its own model;
  child definitions remain shared unless a deep hierarchy copy is explicitly chosen.
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
  for **Add Instance** and **Copy to New Part**, and **Save to External File** for
  externalization. **Part View** contains Full Component, Bodies Only, Hidden and
  Reset to Inherited. The view root is displayed in full; these settings apply to
  occurrences added to a parent.
  Indicate the effective Part View choice (no single choice for a mixed group)
  and whether an occurrence inherits its setting or has an override in this context.

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

## Persistence and conversion

- Versioned `.cadprt` format/capabilities, stable document/definition/occurrence/
  object identities and explicit external dependency records. A renamed FCStd
  without the component schema is not a valid `.cadprt`.
- Reuse native object serialization where compatible; preserve other workbench
  payloads and native type/property identities rather than rebuilding serializers.
- Validate required capabilities before restoration; refuse unsupported required
  content. Save atomically, retain backups and preserve recovery behavior.
- Open supported `.FCStd` content as an in-memory conversion. Save a new `.cadprt`,
  leaving the original untouched. Report unsupported content, partial conversion
  and geometry-only recovery explicitly. Expensive legacy mapping is lower priority
  than the requested architecture; no blanket round-trip compatibility promise.
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
until feature adapters migrate them. Retain original world geometry through explicit
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
