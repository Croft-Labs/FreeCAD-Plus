# ADR 001: history adapter experiment boundary

Date: 2026-09-29. Status: accepted boundary for experiments; final production
architecture is **not selected**. Supports 7.1.3a/7.1.3b and the bounded 7.1.6a
decision record. The [logical contract](PART_HISTORY_CONTRACT.md) remains the
model requirement. None of these prototypes is installed or exposed as a command.

## Decision and alternatives

Retain two compatible directions for the next comparison rather than treating
them as mutually exclusive replacements for all existing modeling code:

1. A native Body/SubShapeBinder adapter can reuse an independent sketch with
   Part Design Pad, preserving each Body's Tip and current feature types.
2. A part-level result adapter can expose separate identities and explicit output
   roles while retaining native shapes, property links, transactions and geometry.

A navigator-only change cannot implement result ownership. A new geometry kernel
or replacement instance system is not justified by these experiments. Continue to
reuse App::Link for occurrences and existing geometry operations where semantics fit.
Do not reparent shared sketches into adapter Bodies or duplicate their constraints.

## What the prototypes establish

[`PartHistoryAdapters.py`](../../tests/prototypes/PartHistoryAdapters.py) is a
test-only module, loaded by [the adapter suite](../../tests/TestPartHistoryAdapters.py).

| Prototype | Established behavior | Remaining limitation |
| --- | --- | --- |
| Body/SubShapeBinder/Pad | One part-owned sketch feeds two Bodies via separate associative binders. Radius edits update both Pads, each Tip stays correct, and native save/reopen/recompute preserves the shared source. | No complete production create/edit workflow, general multi-body operation, transformed attachment or downstream consumer claim. Binder objects are explicit adapters, not cloned sketches. |
| TwoResults feature and BodyResult nodes | One feature publishes Left/Right shapes; separate result objects store producer link, explicit role and UUID string. Rename, source-list reversal, profile/length changes and save/reopen preserve result identity and placement. | Roles are deliberately fixed. This is not general split/merge inference, topology naming or a final serialization schema. |
| ResultUnion consumer | Explicit result links recompute geometry. Missing Right output clears its live result and fails/clears the consumer; restoring the same role restores its identity. Undo/Redo and abort restore geometry and identities. | Disconnected union is valid in this fixture. General Boolean target policy, lineage registration and full history rollback remain unimplemented. |

Eight checks pass together (four original native capability probes plus four
adapter probes) in `part-adapters-20260929-final/results.json` under the external
validation root in the roadmap. Zero failures, errors or skips. No native build
or production source update. The initial result prototype failed placement checks:
its translated output was reset to the result object's identity placement during
recompute, making distinct solids overlap. Aligning the result object's Placement
with its published shape fixes this case; positions are checked after restore.
[`PartFeature.cpp`](../../src/Mod/Part/App/PartFeature.cpp), `Feature::onChanged`,
explains the native Shape/Placement synchronization. Preserve this contract in
future adapters; shape volume alone is insufficient validation.

## Contracts retained for the next batch

Follow-up placement/consumer batch (7.1.3c/7.1.3d/7.1.3e, 2026-09-29):

- The explicit-result prototype now resolves source geometry into its owning
  part frame and extrudes along the transformed sketch normal. PlacementSupport
  records cross-part dependencies. Independent solid comparisons, source-part
  moves/Undo and restore pass; these are placement checks, not attachment support.
- A native Part cut of one App::Link occurrence inside a translated assembly
  updates with source radius changes while the shared definition and second
  occurrence retain their full geometry. The local cut survives save/reopen.
- Draft clones previously retained cached geometry when every input became empty.
  The production clone now clears Shape in that case, including an empty Objects
  list. Native-source and unavailable-result checks pass; source restoration keeps
  clone placement. Native CAM job-model clones also clear/restore correctly.
  Mixed empty/nonempty input behavior is unchanged. Generated CAM path invalidation
  is a separate gate and is not established by the job-model check.

The final grouped batch passes **88 checks** (15 focused history/clone checks,
33 existing Draft modifications and 40 CAM operation/STL/tab checks), no failures,
errors or skips. Evidence: `part-consumers-20260929-final/results.json` and
`prototype-manifest.json` under the roadmap's external validation root. Initial
probes failed tilted extrusion, cross-part placement and stale clone checks;
all three are corrected. Only the Python Draft clone production module was
synchronized to the existing build. No native build or production history adapter
was installed. The earlier eight-check batch remains historical evidence.

Follow-up attachment/drawing batch (7.1.3f/16.2a): an independent sketch with
FlatFace support on a rotated Part plane and a 2 mm attachment offset propagates
support translations through results, Undo/Redo and restore without changing its
result UUID. A TechDraw view of one result supplies a projected radius dimension;
sketch radius 2 to 3 mm, Undo/Redo and save/reopen preserve both numeric values and
native links. The view is asserted to have one analytic circular visible edge.
TechDraw uses Edge0 for this projected edge; the initial Edge1 fixture failed and
was corrected using native source/upstream tests, not by changing application code.

All 24 grouped checks pass in `attachment-drawing-20260929-final/results.json`;
manifest and disposable FCStd examples accompany it. No native build or installed
source update. This closes two bounded proofs, not full attachment support or
TechDraw topology/reference repair. Shape/placement/identity checks and drawing
numeric values provide evidence beyond a successful recompute status.

- **Definition/occurrence:** separate shared definition edits from occurrence/local
  edits. App::Link is the reuse candidate; one assembly-local cut is now proven,
  and mixed geometry/children now has a same-document proof. General occurrence
  editing and cross-file behavior remain open.
- **Body results:** input dependencies point to the producing stage and explicit
  output role. Never retarget by label, tree position or raw solid index. Result
  nodes depend on producers; producers do not depend on their result registries.
- **Selection/defaults:** retain current input collectors in existing commands.
  Version 2 resolves 7.4.8 as creation-time suggestions with explicit saved intent;
  ordinary modifier selection coexists with active accumulating collectors. See
  [ADR 002](ADR_002_CREATION_INTENT.md); production migration remains pending.
- **Transactions:** use native document transactions for definitions, results and
  identities together. The checked prototype abort is not native GUI acceptance.
- **Persistence:** use disposable `.FCStd` fixtures only for this comparison.
  Native Body adapters retain native types. FeaturePython result fixtures require
  the test module on the Python path to recompute; do not promise editable upstream
  compatibility or distribute them as `.cadprt`. Follow the approved native-format
  and best-effort legacy-conversion policy when designing the actual schema.

## Bounded split/merge lineage and failure propagation

[`ResultLineage.py`](../../tests/prototypes/ResultLineage.py) adds real planar
half-space splits using native geometry already used by TrimAPI. Negative and
positive X are explicit semantic roles, not solid enumeration. Child result UUIDs
are allocated once and retain parent identity through parameter edits, disappearance
and reappearance. A merge either continues a deliberately chosen primary identity
or receives a new UUID; parent identities are retained separately from source order.

Five [lineage tests](../../tests/TestResultLineage.py) cover geometry/identity,
Undo/abort, source order/rename, save/reopen, missing output recovery, duplicate
identities, replaced lineage and a U-shaped source yielding two solids on one side.
The latter is rejected as ambiguous instead of allocating arbitrary child roles.
All 29 grouped checks pass; roadmap 7.1.3g/h owns the evidence location and hashes.

A material integration finding: raising an expected producer error caused native
recompute to skip downstream adapters, retaining old merge geometry. In these new
proxies only, expected ValueError/OCCError instead records Failed/ErrorMessage and
empty live outputs while completing native execution, so downstream adapters can
clear their geometry. Unexpected exceptions still use native error handling. This
is not a general solution for native GUI error icons, all consumers, export, or CAM;
production must expose failure explicitly and test those integration boundaries.

No production API/schema is selected. This proof is limited to one same-part solid,
a fixed X-normal split and at most one solid per side. It does not implement generic
shape correspondence, revision-history storage, cross-document remapping, arbitrary
role reassignment, Make Unique or topology reference repair. Existing BodyResult and
native transactions/property links are reused; no application module was installed.

## Mixed definition and bounded independent-copy proof

Native App::Part already combines its own solid with a child App::Link. Two
occurrences in one assembly and one in another preserve independent placements;
shared length edits propagate without double transforms and survive native restore.
This is a same-document native capability, not cross-file update policy.

[`UniqueDefinition.py`](../../tests/prototypes/UniqueDefinition.py) wraps native
recursive document copy and link reassignment in one transaction for exactly one
independent sketch plus native extrusion. Native copy remaps the extrusion Base;
the wrapper assigns fresh SemanticIdentity values and SourceIdentity provenance.
Only the selected occurrence becomes independent; placement remains unchanged.
Undo removes the new definition and restores sharing; Redo restores the same new
identities. Subsequent source edits change the still-shared instance alone.
Save/reopen preserves the distinction. An unsupported definition fails before
mutation. Three added checks join the existing suite for 32 passing checks.

This supports native-copy reuse, not a production Make Unique implementation.
Complex or nested definitions, external dependencies, custom feature proxies,
repeated unique-copy provenance and cross-document lineage require separate design.
No installed module/schema or UI changed. The fixtures use native types with
metadata, so recompute does not require this test helper after creation.
Roadmap 12.1a/12.2a records evidence and remaining parent gates.

## Named parameter and dimensional assignment proof

Native App::FeaturePython length properties can drive multiple native Part features
through expressions, with inch/mm conversion, native transactions, label changes,
and save/reopen. A linked part occurrence retains its placement while the shared
parameter changes. These fixtures preserve existing property/document identities;
no custom proxy is needed to recompute the saved parameter model.

The initial negative test exposed native coercion: an angular expression assigned
to a length was accepted without an invalid state. The test-only
[`NamedParameters.py`](../../tests/prototypes/NamedParameters.py) evaluates expression
units and requires a length result before native assignment. Native cycle rejection
and transaction abort preserve the valid model. This is a narrowly bounded future
editor boundary, not a production interception of FreeCAD expressions.

Roadmap 10.8a/b owns the 24-test grouped evidence. General quantity types, bare-number
unit defaults, production parameter/property rename UI, configuration/external scope, publication
and a parameter editor remain unimplemented. The production architecture decision
must account for native unit coercion rather than treating stored property types as
sufficient dimensional validation.

### Explicit parameter references and invalid geometry recovery

Roadmap 10.8c/d extends the grouped evidence to 26 passing checks. Two parts can
contain parameter objects with identical labels and Width property names without
cross-talk when expressions use unique internal object names. Native `InList`
membership distinguishes the two consumers from the unrelated part before and
after save/reopen. This is object-level dependency evidence: container links also
appear there, so a future property-level where-used view must inspect actual
expression references. No implicit local scope or publication policy is established.

A zero-valued shared length passes dimensional typing but invalidates a native box.
Aborting the transaction and recomputing restores the valid expressions and shapes;
subsequent valid edits, Undo and Redo work. The test performs the abort explicitly.
A production editor must distinguish unit validation from geometry validation and
define failed-edit behavior; this probe adds no automatic rollback to the UI.

### Angular parameters and native property rename

Roadmap 10.8e/f adds an explicit angle assignment boundary to the test-only helper.
A named angle drives a cylinder sector with degree/radian conversion, Undo/Redo and
save/reopen; length, bare-number and missing-reference inputs leave the expression
unchanged. Length and angle are the supported prototype types; no implicit unit
policy or production feature-field interception is introduced.

Native `renameProperty` propagates a dynamic Width-to-PanelWidth rename into two
consumers using internal object names. Undo/Redo restores the corresponding property
and expressions; save/reopen and subsequent edits retain valid geometry. Reuse this
native mechanism when designing the parameter editor rather than replacing expression
text manually. Subsequent 10.8g/h evidence covers collisions and label-based
references below. External references and a complete property-level where-used view
still require separate validation and UI decisions.

The test-only `rename_parameter` wrapper owns a transaction and rejects unrelated
pending transactions. Native rename removes a property's owned expression before
validating the requested name, so failure must abort the transaction to restore it.
Collision, invalid and empty names preserve the owned formula and both consumers;
a later valid rename succeeds. Native rules remain authoritative for names and
locked/dynamic properties. Tests also prove a uniquely labeled parameter container
and an internal-name reference both follow rename through Undo/Redo, a container
label edit and save/reopen, then react to a changed formula. No manual expression
rewriting is used. This does not establish cross-document or ambiguous-label behavior,
or a production editor policy for geometry failures after recompute.

## Remaining decision gates and consumers

Roadmap 11.7a/b adds a test-only explicit planar reattachment operation in
[`SketchReattachment.py`](../../tests/prototypes/SketchReattachment.py). It uses
native FlatFace attachment and transactions, keeping the local attachment offset.
Two parallel planes establish downstream placement, result identity, Undo/Redo and
restore. Missing/curved faces reject before mutation; grouped evidence is 28 passes.
Roadmap 11.7c/d extends the operation with explicit placement policies. For native
attachment P = A * O, preserve-world solves O_new = O_old * P_new^-1 * P_old after
the new support has established its attachment frame. The sketch parent stays
unchanged, so preserving parent-local placement also preserves world placement.
Thirty grouped checks pass, including a translated/rotated support in a rotated
part, local-offset preservation, world position/orientation, Undo/Redo, restore and
later associative support movement. Result position and identity remain intact.

Roadmap 11.7e/f adds deliberate missing-face repair: an invalid Face99 attachment
can be explicitly replaced with a valid planar face under preserve-local. Undo
restores the invalid reference; Redo and restore recover the result with its identity.
Preserve-world rejects invalid or touched sketch state rather than treating cached
placement as current. Calls inside an existing transaction reject before mutation;
the caller's edit and abort remain intact. Grouped evidence totals 32 passing checks.

Roadmap 11.7g/h validates support prerequisites before opening a transaction.
Native OutListRecursive rejects a support derived from the sketch and checks
support/dependency Invalid or Touched state. Native extrusion cycle rejection,
touched-plane rejection and failed-box rejection/recovery bring the grouped suite
to 34 passes. A cached face alone is not evidence that its support is usable.

Roadmap 11.7i/j adds a synchronous rollback preview sharing the same operation.
It returns candidate global placement and attachment offset, aborts the temporary
transaction and recomputes. Both policies match later commits; repeated previews
and missing-face rejection preserve the prior committed edit's Undo/Redo. Grouped
evidence totals 36 passing checks. This is not isolated evaluation: observers see
temporary state, and preservation of an already-populated redo stack is unproven.
That implementation is superseded by 11.7k/l: preview copies the support shape into
world coordinates and evaluates attachment on a temporary sketch in a disposable
hidden document. It retains offset and MapReversed, returning world placement and
the proposed offset without opening a transaction on the original document.
Thirty-eight grouped checks pass, including candidate/commit parity, absence of
original object-change/recompute notifications, document cleanup/active-doc restore
and an already-populated redo stack. Application observers still see temporary
document lifecycle. This is placement evaluation, not constraint solving or full
downstream geometry validation; production preview must retain that distinction.

Roadmap 11.7m/n adds reversed-direction parity and an expression policy boundary.
Preserve-world rejects expression-driven AttachmentOffset before replacing values;
native expression paths may start with a dot. Preserve-local retains the tested
independent named-length expression through restore and parameter edits. Both
policies preview/commit with MapReversed enabled; restore preserves orientation.
Grouped evidence totals 40 passes. Expressions depending on the changed support
and external sketch projections still need separate evaluation.

Roadmap 11.7o/p probes scope boundaries. Direct native attachment to a plane in a
differently placed part disagreed with the world-space preview. The prototype now
requires matching parent geometry containers and rejects App::Link support objects
before mutation. Forty-two grouped checks pass, covering rejection without changes
to either part or occurrence links/placements. This is a fail-closed prototype
boundary, not implemented cross-part or occurrence-aware attachment. A deliberate
reference adapter and occurrence-edit policy are prerequisites to expanding scope.

Roadmap 11.7q/r adds PlanarSupport, an explicit local reference prototype reusing
BasicShapes.ShapeReferences for source validation, placement dependencies and
world/local conversion. Native SubShapeBinder probes exposed alignment and motion
limitations in this fixture; parent qualification fixed only the initial alignment.
The explicit adapter passes both preview policies, source-part motion, Undo/Redo,
restore and further motion; grouped evidence totals 44 passes. Direct cross-container
attachment still rejects. Unlike the native-only attachment fixtures, this adapter
is a Python proxy whose module must be importable when restoring/recomputing. It is
not installed and establishes no production persistence/schema or deployment policy.
Missing/ambiguous source topology and failure-consumer handling remain open.

Roadmap 11.7s/t adds `reattach_with_reference`: source validation precedes one
transaction creating the adapter and changing the attachment. Internal attachment
participates without opening/committing a nested transaction. One Undo removes the
reference and restores support; Redo and restore pass. A fault injected after
attachment rolls back both changes and leaves no pending transaction; a later
attempt succeeds. Grouped evidence totals 46 passes. This remains a test-only
operation, not integration with an existing GUI task transaction.

Roadmap 11.7u/v verifies reference failure/repair. Missing faces clear adapter Shape
and invalidate it; explicit source-face repair supports Undo/Redo and restore.
Deleted sources clear placement dependencies and produce an explicit missing-source
error. Replacing the source alone does not repair the sketch's old mapped face:
explicit preserve-local face reselection is required. Restore and later source
movement pass, with result identity retained. Grouped evidence totals 48 passes.
This does not establish downstream cached-shape clearing or export safety during
failure; those remain consumer gates distinct from successful recovery.

Roadmap 11.7w/x adds test-only `current_result_shape` as an explicit consumer
boundary. It checks result/dependency Invalid and Touched state, Ready status and
nonempty geometry, then returns a copy without recomputing. The fixture confirms
that native upstream failure leaves a cached downstream solid, while this accessor
refuses it. Repair/restore recover access; pending source motion requires explicit
recompute and modifying the returned copy cannot change the stored result. Grouped
evidence totals 50 passes. No production consumer/exporter uses this helper yet;
cached-shape clearing and general consumer integration remain separate gates.

This does not establish reparenting, selected-occurrence placement, deleted support
resurrection, ambiguous topology repair, production transaction integration or a
task-pane UI/preview. Native attachment properties and document
identities remain unchanged; the helper is not needed to recompute saved fixtures.

Before closing 7.1.3/7.1.5/7.1.6 or shipping the model:

- Extend the explicit planar split/primary-merge proof to general lineage, ambiguous
  role changes and downstream reference repair, including invalid input and cycles.
- Exercise changing/removed attachment topology, sheets, mixed definition/occurrence
  content and independent copies beyond the bounded same-document native proofs.
- Check missing/ambiguous TechDraw references after topology changes, CAM path invalidation, FEM
  supports/loads and broader Draft references through edit, undo and restore.
  Native CAM job-model refresh and empty Draft clone invalidation are established;
  FEM is disabled in the current build and awaits a suitable grouped build.
- Define `.cadprt` schema/version/identity and migration boundaries, including
  unsupported Python proxies and conversion losses; do not rename native fixtures.
- Integrate the complete task editor and navigator only after the model choice,
  keeping legacy document paths and matching tests intact.

These are distinct engineering gates. Successful native save/reopen with this
module already importable proves neither cold-start deployment nor consumer safety.
The next batch should address lineage and remaining consumer/attachment probes,
then revise this decision without treating the prototypes as production code.
