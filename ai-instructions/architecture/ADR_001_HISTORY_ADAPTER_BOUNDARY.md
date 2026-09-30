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

- **Definition/occurrence:** separate shared definition edits from occurrence/local
  edits. App::Link is the reuse candidate; mixed geometry/children and one
  assembly-local edit still require proof before final choice.
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
- Exercise transformed part/sketch attachments, sheets, mixed definition/occurrence
  content, independent copies and an assembly-local operation without changing the
  shared definition or its other occurrences.
- Check TechDraw geometry/dimension references, CAM target and path invalidation,
  FEM supports/loads and Draft references through edit, undo and restore.
- Define `.cadprt` schema/version/identity and migration boundaries, including
  unsupported Python proxies and conversion losses; do not rename native fixtures.
- Integrate the complete task editor and navigator only after the model choice,
  keeping legacy document paths and matching tests intact.

These are distinct engineering gates. Successful native save/reopen with this
module already importable proves neither cold-start deployment nor consumer safety.
The next batch should address placement/occurrence and consumer probes, then revise
this decision with evidence rather than treating the prototypes as production code.
