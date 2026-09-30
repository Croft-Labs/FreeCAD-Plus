# ADR 002: Creation suggestions versus committed operation intent

Status: accepted product/interaction boundary; production architecture/API pending.
Basis: owner-adopted version 2, roadmap 7.4.8 and 10.1/10.3. Governing semantics:
[product contracts](../PRODUCT_SPEC.md#planned-creation-and-interaction-contracts).

## Decision

A creation suggestion is transient guidance, not a saved operation mode. Resolve
eligible geometry and explain the proposal; explicit choices always prevail. On
acceptance, store concrete mode and target references. Evaluation uses those saved
inputs exclusively; changed intersection triggers repair/failure, never a new target
or a switch to New Body. Guided/direct entry and aliases use this same boundary.

Keep operation first in the task pane. Guided prompts advance through unresolved
collectors without rearranging that field. Ordinary modifier selection and active
feature collector accumulation are distinct modes. The planned shared Sketcher
eligibility service must separate structural applicability from solver proof; its
implementation is not supplied by this operation prototype.

Alternatives rejected: unconditional New Body (superseded owner proposal), inference
on every recompute (unstable engineering intent), choosing the first intersecting
body (ambiguous scope), and separate guided/expert feature models (divergent semantics).
No current Extrude/Revolve backend or legacy document is migrated by this decision.

## Bounded proof and reuse

[`OperationIntent.py`](../../tests/prototypes/OperationIntent.py) uses native Part
Boolean geometry, property links, document transactions and the existing validate_link
cycle guard. The test-only proxy stores Tool, Targets and Operation; recompute never
calls the suggestion function. Existing PersistentProxy supplies persistence support.

[`TestOperationIntent.py`](../../tests/TestOperationIntent.py) verifies no/one/multiple
candidates, duplicate candidate elimination, visibility independence, cross-part/Link
exclusion, contact/unavailable geometry review, explicit New Body despite overlap,
saved Unite failure when the tool moves onto another body, Undo/Redo, Subtract and
Intersect, aborted target removal, and native save/reopen. The first run's alternate
target fixture accidentally tested face contact due to a translation offset; corrected
world-bound assertions distinguish the intended overlap from the separate contact test.

Seven new checks and 15 existing history/clone checks pass together; evidence is
recorded in roadmap 10.3a/b. No native build, installed module or GUI command changed.
Use the existing isolated ValidateUpstreamIssues procedure with the four suites in
that results.json. The saved FCStd fixture requires test modules on the Python path;
it is neither cadprt nor a portable production feature.

## Limits and next gates

The experiment supports single solids directly owned by one App::Part, using its
local frame; it deliberately excludes occurrences/cross-part targets and multi-target
execution. Candidate lists must be supplied, not discovered from document traversal.
It proves native link persistence, not the future semantic body-ID/lineage schema.
Contact uses an explicit fixture-scale distance and asks for review; scale-aware
policy, numerical boundary stability/hysteresis and invalid-union fixtures remain
open. No UI state machine, editability/reference-set filtering, solver eligibility,
full alias integration, general geometry/attachment or cold-start deployment claim.

Before production, prove shared target discovery, occurrence/edit/access scopes,
preview lifecycle and explicit-choice retention in real Extrude/Revolve tasks, plus
model identity, downstream consumers and persistence gates. Do not use test-only
helpers as an installed API by copying them into each command. Retain the existing
application behavior until the selected architecture supports a bounded migration.
