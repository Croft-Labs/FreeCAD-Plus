# Component/document architecture

Status: G1.2 single-component pilot implemented and validated, October 10, 2026.
The native service module is opt-in; the complete panel, conversion and later Group 1
behavior below remain target design until their roadmap stages are completed.
Engineering choices below implement confirmed behavior; they do not approve
DOCX candidates or restore archived Plus code. The [component specification](ui-ux-specs/COMPONENT_PANEL.md)
owns UI requirements; [the roadmap](DEVELOPMENT_ROADMAP.md#group-1--component-panel-and-document-structure)
owns implementation order and acceptance status.

## System boundaries

Reuse FreeCAD documents, native feature/property identities, geometry, solvers,
transactions and links. Introduce component ownership and presentation around
these services. Keep the original workbench inventory and geometry algorithms.
The first pilot covers one domestic component only; nested definitions, external
files, broad legacy conversion and full panel behavior follow in separate stages.

The Plus/Legacy interface preference and redesigned modeling dialogs are outside
this stage. Component storage must not depend on the chosen toolbar presentation.
The archived fork is reference material, not a source of implicit requirements.

## Components and data flow

| Responsibility | Target ownership / native service |
| --- | --- |
| File | One native `App::Document`; one marked file-root container represents its global frame and top-level placements |
| Definition catalog | File-owned definitions, including unused ones; imported-file catalog follows later |
| Component definition | Native `App::Part`, proven by the pilot, owns modeling content and child placements and can serve as part and assembly simultaneously |
| Placed instance | Native `App::Link` targets a definition; root instances belong to the file, child instances to their parent definition |
| Modeling content | Existing sketches, Part/PartDesign operations, geometry and required backend Bodies retain their native types and relationships |
| Component panel | Models, Part Tree and History are projections of the document model; tree rows do not own or duplicate geometry |
| Edit context | Per-view/tab selection of defining component and occurrence path, separate from ordinary selection and saved model identity |
| Persistence adapter | Native FreeCAD document serialization plus explicitly versioned component metadata; validated `.cadprt` open/save entry points |

The pilot proves the `App::Part`/`App::Link` mapping for one domestic component.
The definition is hidden and its one linked occurrence is visible, avoiding a
duplicate rendered definition. Broader command integration remains deferred. Backend grouping must not
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

### Persistence contract

`.cadprt` retains the native FreeCAD archive and object/property serialization,
with component metadata that explicitly identifies the format and schema revision.
It is not a renamed legacy file with an assumed component structure. No historical
`.cadprt` schema is adopted implicitly. No owner files have been converted.

The schema owner is [freecad_plus/document.py](../src/Mod/FreeCADPlus/freecad_plus/document.py).
Schema 1 is deliberately bounded to zero or one domestic definition and occurrence:

| Stored item | Schema 1 representation |
| --- | --- |
| Marker | File-root `PlusFormat = FreeCADPlus.ComponentDocument` |
| Revision | File-root integer `PlusSchema = 1` |
| Definition catalog | File-root native `Definitions` PropertyLinkList |
| Placements | File-root native Group containing App::Link; LinkTransform false, copy-on-change disabled, no array elements |
| Definition content | Native App::Part Group containing backend PartDesign Bodies |
| Identity | Native Document.Uid and object Name; native object IDs also survive tested reopen |
| World frame | File-root Placement fixed at identity; native Origin/planes reused |
| Definition frame | Identity in the pilot; placement is authored on the occurrence |

Ownership validation follows native groups and Origins, not arbitrary dependency
links. Orphaned objects, multiple roots, invalid targets and external dependencies
are rejected. Empty files and unused domestic definitions are valid. Nested,
external and other modeling-content schemas require explicit extension/migration;
these pilot bounds are not final product restrictions.

[editing.py](../src/Mod/FreeCADPlus/freecad_plus/editing.py) uses the native per-view
`PlusEdit` active-object slot with a file-root-relative occurrence path, plus native
`part`/`pdbody` slots. Selection never updates this context. A fresh reopen starts
in File Edit. Sketch creation supplies a Body automatically; the Pad adapter creates
the native PartDesign feature. History is a projection of native Body contents.
Native Sketch and Pad editors are retained and tested.

These are opt-in Python entry points, not replacements for File > New or arbitrary
workbench commands. Their ownership/Edit guards apply at these entry points. The
complete component panel and broader command routing are later stages; the stock
tree is still present. No new toolbar placement or interface preference is implied.

The importer checks archive metadata before restoration and validates the restored
native graph. Unknown/future versions and renamed legacy archives are refused.
The save adapter assigns the exact FileName and invokes native save(), preserving
CheckExtension and native backup settings. It requires native safe-save BackupPolicy
rather than disabling safeguards. Pending transactions and partial loads are refused;
failed saves restore the previous filename/root label and retain GUI dirty state.
Only successful native save and archive verification clear that state.

Persist the file root, definition catalog, instance targets/local placements,
component ownership and necessary history associations. Later stages add import
references and confirmed parent-owned Part Type settings. Native objects retain
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
Exact reference-location recovery interactions are deferred to their stage.

Legacy conversion means `.FCStd` -> a separately saved `.cadprt`, preserving the
original source file. Inventory objects, native links, expressions, attachments
and placements before conversion. Keep editable native features where possible;
preserve recoverable final solid/curve geometry as explicitly identified
nonparametric content where conversion is unsupported. Report any loss of
parametric editing or unresolved dependency. Do not silently discard content.

Reparenting must preserve world placement and valid subelement references; it
cannot be considered successful merely because the final shape looks similar.
Validate conversion by editing, recomputing, saving, closing and reopening.
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
Native transactions are not a multi-file atomic-save guarantee; external-file
failure/recovery must be designed and tested in the external-definition stage.

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
  The pilot must choose transform behavior explicitly and keep ordinary instances shared.
- [PartDesign Body](../src/Mod/PartDesign/App/Body.h): native feature grouping and Tip semantics.
- [Confirmed component behavior](ui-ux-specs/COMPONENT_PANEL.md#confirmed-requirements),
  [movement ownership](ui-ux-specs/TASK_PANEL.md#move-components),
  [edit display](ui-ux-specs/MODEL_VIEW_WINDOW.md#component-editing-display), and
  [owner evidence](ui-ux-specs/EVIDENCE_AND_DECISIONS.md): authoritative intent.

- [Pilot acceptance suite](../src/Mod/FreeCADPlus/TestComponentPilot.py): native ownership,
  context isolation, geometry, rollback/Undo/Redo, persistence and legacy controls.
