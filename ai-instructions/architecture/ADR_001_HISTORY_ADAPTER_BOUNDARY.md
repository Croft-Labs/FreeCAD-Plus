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

- **Definition/occurrence:** separate shared definition edits from occurrence/local
  edits. App::Link is the reuse candidate; one assembly-local cut is now proven,
  while mixed geometry/children and general occurrence editing remain open.
- **Body results:** input dependencies point to the producing stage and explicit
  output role. Never retarget by label, tree position or raw solid index. Result
  nodes depend on producers; producers do not depend on their result registries.
- **Selection/defaults:** retain current input collectors in existing commands.
  New Body versus automatic Add (7.4.8) and modifier-selection policy remain open;
  neither prototype silently chooses a production default.
- **Transactions:** use native document transactions for definitions, results and
  identities together. The checked prototype abort is not native GUI acceptance.
- **Persistence:** use disposable `.FCStd` fixtures only for this comparison.
  Native Body adapters retain native types. FeaturePython result fixtures require
  the test module on the Python path to recompute; do not promise editable upstream
  compatibility or distribute them as `.cadprt`. Follow the approved native-format
  and best-effort legacy-conversion policy when designing the actual schema.

## Remaining decision gates and consumers

Before closing 7.1.3/7.1.5/7.1.6 or shipping the model:

- Compare true merge/split lineage, ambiguous role changes and downstream reference
  repair, including invalid feature input and cycles.
- Exercise actual part/sketch attachments, sheets, mixed definition/occurrence
  content and independent copies beyond the bounded placement/local-cut proof.
- Check TechDraw geometry/dimension references, CAM path invalidation, FEM
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
