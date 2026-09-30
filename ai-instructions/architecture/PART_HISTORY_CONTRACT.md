# Part-level history and result contract

Status: logical contract for roadmap 7.1.1, 7.1.2 and 7.1.4, 2026-09-29.
This defines the requested model, not an implemented document schema or a chosen
production adapter. Native capability probes inform 7.1.3; its architecture choice,
consumer validation and migration remain open. No existing document is migrated.

## Ownership and roles (7.1.1)

A part definition owns one ordered **History** and a separate **Bodies/results**
collection. History contains operations and reusable inputs once each. Bodies are
geometric results, not required owners of sketches or features. A part can contain
its own geometry and child occurrences, each with an independent occurrence identity.
An assembly does not interleave the histories of its component definitions.

| Role | Contract |
| --- | --- |
| Part definition | Owns history, results and local coordinate context. Shared by occurrences. |
| Sketch | Part-owned reusable geometry/constraints; references a support explicitly. Any compatible feature may consume it. |
| Datum | Part-owned plane, axis, point or coordinate system with explicit support dependencies. |
| Curve | Part-owned wire/curve result or construction input; never implies a solid body. |
| Imported object | Preserves source/provenance and available geometry; imported geometry is not invented editable history. |
| Linked/cloned object | Records source, transform and update semantics. Associative link, independent copy and occurrence are distinct operations. |
| Modeling feature | Stores its complete definition, inputs, operation and explicit target intent. May produce zero, one or several results. |
| Solid body | A connected solid result with semantic identity and a generating feature/output role. A compound of solids is multiple body results. |
| Sheet body | A surface/shell result with its own identity; never silently treated as a solid. |
| Occurrence | Refers to a definition plus placement and permitted local overrides. Editing placement does not edit the shared definition. |

History order expresses modeling intent and rollback position. Dependency links
govern recompute; a proposed reorder is legal only if inputs remain available and
acyclic. A folder or display sort cannot change dependencies. The Bodies view is
the current result set at the chosen history position, not every historical shape.
Hidden, suppressed, failed, unloaded and rolled-back are separate states.

An input collector refers to the shared object and optional selected regions;
it must not secretly copy or reparent a sketch. A body is created by an operation's
result. Starting a feature does not require a manually created/active Body.
Default New Body versus automatic Add remains the separate 7.4.8 decision;
this contract requires both explicit intent and stable targets, not a new default.

## Current native model and required changes (7.1.2)

All code references are to this checkout, not a separately installed application.

| Area | Existing capability/evidence | Required work |
| --- | --- | --- |
| Part container | [`App::Part`](../../src/App/Part.cpp) and [`GeoFeatureGroupExtension`](../../src/App/GeoFeatureGroupExtension.cpp) provide grouping, placement and child scope. | Reuse where compatible; grouping alone is not an ordered semantic history or definition/occurrence contract. |
| Body ownership/Tip | [`Body::addObject` and `isAllowed`](../../src/Mod/PartDesign/App/Body.cpp) remove an object from its prior group and manage the Tip. | A tree flattening cannot make one sketch belong to two Bodies. Preserve legacy Body semantics behind an explicit adapter, if chosen. |
| Multiple solids | [`Feature::singleSolidRuleMode`](../../src/Mod/PartDesign/App/Feature.cpp) already consults Body.AllowCompound. Native Part extrusion can produce multiple solids. | Do not claim the kernel forbids multiple bodies. AllowCompound alone does not provide stable per-result identities or shared ownership. |
| Independent sketches/extrusions | [`Part::Extrusion`](../../src/Mod/Part/App/FeatureExtrusion.cpp) consumes a Base link outside Part Design Body. | Reuse geometry capability; production unified Extrude/Pad/Pocket tasks and persisted types still need deliberate integration. |
| Part Design profiles | [`FeatureSketchBased.cpp`](../../src/Mod/PartDesign/App/FeatureSketchBased.cpp) handles profile support and Body context; [`Command.cpp`](../../src/Mod/PartDesign/Gui/Command.cpp) prepares current creation workflows. | Audit command, attachment, target and recompute restrictions separately. A successful Part extrusion is not proof all Part Design features work at part scope. |
| Links/occurrences | [`App::Link`](../../src/App/Link.cpp) already has linked-object and placement behavior. | Reuse it before inventing another instance system. Define current-result reference sets so occurrences do not display every historical intermediate shape. |
| References/transforms | [`ShapeReferences.py`](../../src/Mod/Part/BasicShapes/ShapeReferences.py) resolves global geometry, parent placements and cycle checks for current Plus features. | Preserve coordinate context; expand only after agreed cross-part/occurrence reference contracts. |
| Persistence/identity | [`Document.cpp`](../../src/App/Document.cpp) has document Uid and conditional export-time _ObjectUUID/_SourceUUID handling. | Do not assume every existing object already has a universal stable UUID. Define explicit persisted semantic identities and copy/import rules. |
| Downstream consumers | Existing drawing/CAM/FEM consumers use native shapes and links. | Validate result replacement, placements and invalidation; volume equality alone proves none of these consumers safe. |

Presentation-only candidates: a read-only History/Bodies navigator, filters,
folders, source/consumer navigation and selection synchronization. Reparenting,
feature input changes, result lineage, rollback, automatic targets, suppression and
`.cadprt` persistence change model/API semantics and require their own tests.

## Identity and dependencies (7.1.4)

The following are logical persistent identifiers; property names/storage remain
subject to 7.1.3/7.1.6. Labels, document object names, tree rows, face indices and
current solid enumeration are not semantic identity.

- A definition has a persistent DefinitionId. Features/inputs have FeatureId (or
  input-object identity) within that definition; each occurrence has OccurrenceId.
- BodyId identifies a semantic result lineage. A result revision is identified by
  its producer feature, explicit output role and evaluation revision. Editing
  parameters updates a revision without arbitrarily replacing its BodyId.
- An input binding names its source definition/occurrence context, producer and
  output role/BodyId at the appropriate history stage. It never resolves through
  the final Bodies view, which could introduce a dependency on its own future.
- Output registration is metadata; the producer/result bookkeeping must not create
  reverse recompute links and cycles. Store real dependencies in the native DAG.
- Subshape references retain topology/provenance information and must report
  ambiguity. A still-existing Face3 is not proof of the intended face's survival.

| Change | Identity/lineage rule |
| --- | --- |
| Rename, visibility, folder or display order | Preserve identities; do not alter geometry dependencies. |
| One-to-one edit of a result | Preserve BodyId and append/update the evaluated revision. |
| New disconnected result | Allocate a new BodyId and record its producer/output role. |
| Merge into an explicit primary target | Preserve the primary target's BodyId; record consumed input identities and the merge relation. No implicit primary based on tree order. |
| Merge without a specified continuing result | Allocate a new BodyId with all parents recorded. Resolve target intent before accepting the feature. |
| Split | Allocate child identities with explicit roles and parent lineage; reuse those identities on recompute only when the mapping remains unambiguous. |
| Result disappears, suppression or rollback | Keep identity/history records; mark availability explicitly. Do not redirect consumers to a different body. |
| Result reappears | Restore its identity only when producer/output-role correspondence is established; otherwise require reference repair. |
| Ambiguous topology or failed feature | Mark unresolved/failed and invalidate dependent live results; do not show stale geometry/toolpaths as successful current results. |
| Independent copy / Make Unique | Allocate new definition/object identities and preserve provenance. An occurrence keeps the shared definition identity. |

Feature edits, target changes, result registration and status changes belong to one
transaction. Cancel and Undo restore geometry, inputs, ordering and identity together.
An explicit last-good checkpoint may remain available for recovery; it is not a
valid current result after failure. Save/reopen must preserve dependency bindings
and identity, independent of labels and in-memory object addresses.

## Architecture alternatives and bounded native probe (7.1.3)

| Alternative | Useful inheritance | Gap to prove |
| --- | --- | --- |
| Native Body adapters | Existing Part Design feature/task behavior, Tip and legacy documents. | Independent inputs, multiple results, one feature affecting several bodies, adapter cycles and ownership. |
| Part-level feature/result layer over native geometry | Existing independent Sketcher/Part operations, App::Link and transactions. | Stable result lineage, native feature adapters, full task editing and downstream consumers. |
| Flatten existing tree only | Low-risk presentation changes. | Does not satisfy the requested ownership/result model; insufficient as the architecture. |

[`TestPartHistoryCapabilities.py`](../../tests/TestPartHistoryCapabilities.py)
uses only existing native objects in disposable documents. It checks a shared
sketch driving two extrusions without any Body, one extrusion producing two solids,
a later compound consuming all results, parameter propagation, native undo/redo,
abort and `.FCStd` save/reopen, independent App::Link placements and exclusive Body
reparenting. A compound is aggregation, not proof of a production Boolean/history
operator. These probes do not install a new command or prototype document schema.

All four checks passed in `part-history-20260929-final/results.json` under the
external validation root recorded in the roadmap. The native group check also
establishes that direct App::Part-to-Body reparenting is rejected while the sketch
still belongs to its Part. Removing it first is an explicit ownership change,
not shared ownership. No native rebuild was required for this probe batch.
To rerun, use the isolated existing-build procedure in
[`tests/UpstreamIssues.md`](../../tests/UpstreamIssues.md) with
`FREECAD_PLUS_ISSUE_TESTS=tests/TestPartHistoryCapabilities.py`; the shared
ValidateUpstreamIssues macro accepts this explicit suite. Use a new external
evidence directory because the persistence probe writes its own example there.

Subsequent batches implemented native Body and explicit-result adapters under
`tests/prototypes`, then extended placement, local-cut and consumer checks. See
[ADR 001](ADR_001_HISTORY_ADAPTER_BOUNDARY.md) for the comparison, placement defect
found/corrected, native persistence evidence and remaining decision gates.

Remaining before an architecture choice: extend the bounded adapter comparison;
extend the bounded explicit planar split/primary-merge proof to general lineage,
mixed definition/occurrence content,
general attachment/topology changes and remaining drawing/CAM/FEM/Draft consumers.
One assembly-local cut, transformed input placements and empty Draft/CAM job-model
refresh are now proven. A later batch also proves one planar attached profile and
one TechDraw projected radius through edits, Undo/Redo and restore; these do not
establish general reference repair, occurrence editing or path invalidation. The clone refresh fix is production Python; adapters remain test-only.
Resolve selection/default policies separately. Record the architecture decision
and `.cadprt` migration boundary before production implementation (7.1.5/7.1.6).
The native probe's `.FCStd` output is test evidence, not the new file format.
