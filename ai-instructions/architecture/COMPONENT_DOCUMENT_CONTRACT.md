# Component documents and Model History

Owner-approved contract, 2026-10-01. Implementation and validation status belong
to roadmap 7.8. This supersedes conflicting part/navigator terminology and the
former opt-in legacy-conversion policy; it does not claim completed implementation.

## Ownership, instances and files

- UI names: **Component Structure**, **Model History**, **Add Component**,
  **Add Reference Object**, **Convert to Dumb Object**, **Instances > Add Instance**,
  **Instances > Copy to New Part**, **Save to External File**.
  Documentation may say sub-component; UI calls every instance a component.
- A component definition owns ordered history, evaluated result objects, child
  component instances and optional assembly constraints. Geometry and children
  may coexist. Bodies are results, never prerequisites for sketches or operations.
- Component Structure starts at the root component, using the existing native Part
  icon. Do not display a file/document wrapper row above it.
- Each `.cadprt` has one root component and embedded definitions, and may link
  definitions in other `.cadprt` files. New definitions are embedded by default.
  Definition identity is distinct from occurrence identity and labels/file paths.
- Repeated instances share a definition, with independent placements and display
  overrides. Copy to New Part copies the selected definition and its own model;
  child definitions remain shared unless a deep hierarchy copy is explicitly chosen.
- Opening a component in a tab creates a view/edit context of the same definition.
  Embedded edits save with the owning file; external edits save with their file.
  The tab identifies both component and owning file. It is not an extraction.
- Native grouping, App::Link, OpenCASCADE geometry, properties, dependency graph
  and transactions remain reusable infrastructure. A new component/result layer
  owns the semantic contracts; tree flattening alone cannot implement them.

## Component Structure and representation

- The Components panel identifies the active component, without a filename/path or
  Add Component / Add Reference Object buttons. Creation actions live in context
  menus. Component tabs may still identify their owning file.
- The first tree column is the part name. Repeated occurrences of the same definition
  under one parent collapse into one row by default, with an instance count such as
  **x5**. **Expand Instances** reveals rows such as **support_angle#005**; **Collapse
  Instances** restores the grouped view. The number is a persistent display number,
  separate from the occurrence UUID; labels and numbers are not reference identities.
- Highlight the active component and provide a show/hide control. The active component
  and its ancestor branch cannot be hidden. Group actions apply to the represented
  occurrences; Copy to New Part requires an individual occurrence.
- **Edit** is the first context action; double-click also activates the definition
  for editing. **Add Component** adds to that definition. Omit **Open Component in
  Tab** on the root row, which is already its own view. Use an **Instances** submenu
  for **Add Instance** and **Copy to New Part**, and **Save to External File** for
  externalization. **Part View** contains Full Component, Bodies Only, Hidden and
  Reset to Inherited. The view root is displayed in full; these settings apply to
  occurrences added to a parent.

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
- An **Assembly Constraints** grouping item appears first under its component
  only when constraints exist. It contains constraints, not real child components.

## Model History and evaluated objects

- An **item** means an object or an operation. Show a suppression checkbox, then
  a visibility icon, then the item name. Checked means active, unchecked means
  explicitly suppressed, and partially checked means inactive because of an input.
  Visibility is separate from suppression and does not change dependencies.
- Display objects and operations in creation/history order. Reusable inputs and
  result identities are separate from producing operations. Solid/sheet results
  expose geometry; editable parameters remain on their operations.
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
  reference in Model History and retain its saved source identity for repair. This
  does not relax format, component-graph or external-definition identity checks.
- No separate snapshot option in this command: independent copies use Convert
  to Dumb Object. Adding a reference does not change its source's display type.

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

One root with its own body and two instances of an embedded child, plus an external
child. Independent sketches feed operations without Body containers. Exercise
direct-child body/sheet/dumb-sketch/curve references, parent-only edits, delayed
refresh, nested representation overrides, constraints ordering, isolated tabs,
suppression with an independent branch, shared-producer parameter removal and
independent extraction. Verify undo/redo, cold reopen, source edits after reopen,
missing dependencies, legacy-original preservation and representative drawing,
CAM, FEM and Draft consumers. Track unavailable gates separately from passing ones.
