# Remove individual instances: native workflow proposal

Subsequently authorized and implemented: [installed evidence](../instance-removal-20261125/README.md).
The record below is the historical UI-only proposal.

November 25, 2026. Owner requested implementation of Remove individual instances.
Required native layout preview is prepared for direct screenshot approval.
No production deletion behavior or installed payload changes have been made.

## Screenshots

- [Current menu](baseline.png) and [proposed Assembly menu](menu.png).
- [Single occurrence](simple.png): selected child and parent, remaining quantity,
  shared definition/geometry/history preserved, Cancel default.
- [Dependent constraint](constraints.png): explicit unchecked opt-in to remove
  the listed constraint; removal disabled until resolved or included.
- [Shared parent](shared.png): changing a child changes that parent's assembly
  contents everywhere it is used. Explicit acknowledgement of this scope.
- [Other dependency](blocked.png): removal blocked with the named reference and
  actionable recovery. Uses shared TaskStatus error appearance.
- [All review states](proposal.png).

The target is one native occurrence link in its owning parent, never its definition.
Removing an entire subassembly occurrence preserves that subassembly's definition,
children, history and constraints. Removing a child *inside* a shared subassembly
changes the shared assembly contents, including occurrences in other files after
their normal source-save/reload cycle. The review must not promise uniqueness for
that case. The example removes Bolt (1 of 2) from Gearbox, not one arbitrary visual
copy of that child under only one Gearbox placement.

## Intended implementation after layout approval

Offer Remove instance on individual Assembly occurrence rows, including Hidden,
Reference and Excluded links. Parts definition rows, active assembly root and
collectors are ineligible. Future condensed groups must expose individual children;
never silently interpret a group as remove-all. Protect current Edit ancestry and
active task/context state, with actionable guidance to select an eligible parent.
Pattern-controlled links will defer to the pattern editor once patterns exist.

Resolve actual owning-document/link identity and qualified occurrence path, not
labels or display ordinals. Preview the exact owning file/parent, selected link,
remaining sibling count and dependencies. Capture and revalidate a removal plan
before acceptance so switching documents, editing dependencies or changing the
assembly cannot execute a stale selection. Duplicate visible projections of one
shared native link must not become separate removals.

Remove only that link and explicitly included assembly constraints in one owning
document transaction. Preserve all other links, definitions, geometry/history,
imports/catalogs and source files. Refuse unsupported geometry/expression/external
dependents or dependencies of constraints that would themselves be removed.
Do not silently clear references or recursively delete definition contents.
Keep fixed assembly/solver frames and collector consistency; recompute/refresh
without solver-driven movement of surviving links. Cancel leaves state unchanged.
Undo/Redo restores exact link/constraint identities and references. Route Assembly
Delete through the same scoped workflow rather than an unrestricted native fallback;
do not alter definition deletion elsewhere.

Acceptance still required: real single-link removal among repeated instances;
last instance while definition survives; shared subassembly scope; imported links;
constraints and blocked feature/external dependents; stale plan; cancellation;
Undo/Redo; save/reopen; selection/Edit state; native Delete routing; installed app
and existing shortcut. No such deletion tests have run yet.

Condensed/expanded display and quantity/patterns remain separate pending proposals.
This request supplies no approval for those earlier layouts or global name enforcement.

## Capture evidence

Snapshot panel.py from production 8e8745b3297a68c16951100cca028b186c982b2e.
Review c631e12413ea allows panel.py and instance_remove_ui.py only. Final fingerprint
b370f2d705dd001d08bda7ed9d43df68d82222d178babe46a84177be57e2fb0c.
Fresh capture, no scope violations, approval unset. Preserved unrelated
project.previewfirst.json. Existing owner FreeCAD executable rendered actual Qt
controls in isolated profiles with disposable native links and a native constraint.

Baseline/candidate menu checks pass. Four presentation scenarios verify enabled
state, dependency/shared-impact acknowledgements, safe Cancel and nonmutating
preview acceptance. Document structure/placements, Undo count and Edit context
remain unchanged; final candidate stderr is empty. Scenarios are explicit fixture
data: no dependency detector, removal backend or real Undo behavior is implemented.
The candidate menu opens the constrained fixture dialog, not a computed deletion plan.

Helpers and final results are archived. Generated validation profiles are removed
after archiving; review worktrees remain available for approval. The renderer's
source-root assumptions refer to its original local helper directory; adjust them
if replaying from this evidence directory. Existing installed behavior is unchanged.
