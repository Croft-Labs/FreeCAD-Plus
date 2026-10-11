# Component/document architecture

Status: G1.6b domestic unused-model increment validated; external unused-model integration remains open, October 10, 2026.
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
G1.6b/c retain the rest of the confirmed panel work.

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

### Unused domestic definitions (G1.6b partial)

`editing.edit_unused(doc, definition)` isolates a domestic definition in the current
view. The panel adds one temporary last child beneath the pinned file row, labeled
`Component name (unused model)`, with active fill/bold text and no drag flag. Existing
file/occurrence rows are gray but selectable and still support Edit. History routes
to the definition's native sketches/features; native Bodies stay out of the panel.
The Sketch/Pad adapters use the same owning-document transactions as placed edits.

[isolation.py](../src/Mod/FreeCADPlus/freecad_plus/isolation.py) owns transient view
sessions. It copies the native definition's Coin display graph, forcing only the
copied top-level display switch. It temporarily wraps the native ObjectGroup,
GroupOnTop and RootDimensions in hidden scene switches. Keeping the original groups
alive preserves native add/remove behavior. Native EditingRoot remains available for
the Sketch editor. No App objects, instance links, Visibility properties, schema
fields or Undo entries are created by isolation. Save therefore persists definition
edits without persisting a temporary occurrence or hidden assembly state.

Relevant native observer bursts refresh the detached display once per queued update;
there is no idle polling. Commit/abort defers incomplete graphs. Each session belongs
to one native view and resolves the definition by document UUID/object Name/ID.
Changing Edit, closing the panel/view/document, losing the definition/import, or
placing the previously unused model removes the preview and restores native groups.
Cleanup clears the unused Part/Body context. Undo of removal restores data without
reopening isolation. Native feature editing must finish before switching contexts.
The implementation is checked against 1.1.4's scene-group layout and refuses an
unrecognized definition display before replacing an existing context.

**Open boundary:** in-place Edit of an unused external definition is refused before
mutation; existing domestic isolation survives that refusal. A failed exploratory
check showed native source selection activating the defining-file tab. Native
Document::trySetEdit also requires a local parent (an external subobject reached
through a placed link is supported). The next G1.6b increment must integrate external
unused selection/native editors without adding saveable temporary links, changing
owner preferences or redirecting the source's geometry ownership. The external
qualifier remains in Models; prior placed-external editing remains supported. Native
selection of an unplaced external catalog item can still activate its source tab.
This limitation does not change the confirmed UI requirement or mark G1.6b complete.
Component windows/remaining actions are G1.6c; Part Type/fading are G1.7.

### Persistence contract

`.cadprt` retains the native FreeCAD archive and object/property serialization,
with component metadata that explicitly identifies the format and schema revision.
It is not a renamed legacy file with an assumed component structure. No historical
`.cadprt` schema is adopted implicitly. No owner files have been converted.

The schema owner is [freecad_plus/document.py](../src/Mod/FreeCADPlus/freecad_plus/document.py).
New files and conversions use schema 4. Schemas 1 and 2 remain readable/savable
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
