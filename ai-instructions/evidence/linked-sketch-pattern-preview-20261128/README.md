# Linked sketch pattern — native Qt UI proposal

November 28, 2026. Owner requested implementing the suggested associative pattern
workflow after reporting solver trouble with constraint-generated copies.
The behavior is requested; approval of this concrete revised UI is pending under
the standing preview-first workflow. No production code or installed app changed.

## Direct screenshots

- [Current controls](before.png)
- [Linked pattern, new](linked-pattern.png)
- [Advanced options](advanced-linked.png)
- [Legacy constraint options](advanced-constraints.png)
- [Editing a linked pattern](edit-linked.png)
- [Make independent confirmation](make-independent.png)
- [Circular/angular and radial controls](circular-linked.png)

These are real Qt controls rendered inside an isolated FreeCAD process, using the
installed controls as the baseline. Behavior selection and confirmations are
UI-only simulations; geometry generation, solver changes and conversion are not
implemented or validated by these screenshots. No owner document was opened.

## Requested implementation contract

New patterns default to **Linked pattern**. Solve editable original geometry, then
generate exact transformed copies from the source and pattern parameters, without
copying tangency/orientation/equality/dimension constraints into every instance.
Generated geometry adds no independent degrees of freedom. It stays usable as
normal profile geometry for downstream modeling. Source edits, pattern changes,
dragging and document recompute must update copies consistently.

Preserve Linear, two-direction, Circular, angular/radial, symmetric/reverse,
pitch/total distance and native units, one Pattern row/icon, exact source selection,
and bottom Done/Apply/Cancel. Apply clears picks and restores defaults. Ordinary
sketch editing remains active after closing the pattern collector.

Advanced contains Linked/Constraint-based behavior radios and the previous
Create spacing constraints/Hide spacing chain controls. Cancel restores draft
options. Existing patterns initially retain their saved constraint behavior.
Switching an existing group to Linked requires explicit choice and Apply; conversion
must retain source constraints and surviving geometry identities. Reject conversion
if external constraints/expressions would be silently discarded or retargeted.

Editing a linked group exposes **Make independent**. Confirmation detaches all
generated copies in that pattern at current positions, leaving ordinary editable
curves and preserving originals; no replacement constraints are added. This is
one undoable operation. It deliberately breaks future updates, unlike Linked mode.

Generated copies cannot independently deform or drive their sources. Do not use
iterative observer callbacks, hidden per-copy equations or arbitrary anchors to
masquerade as a solver-independent pattern. Validate dependency order/cycles and
one-way references, including pattern chains and references to direction/center.
Protect direct downstream references when changing source/count or deleting members.

## Native implementation investigation and acceptance

Existing `PatternDefinitions` recipes already store persistent geometry facade IDs,
instance slots and references. Keep those identities through edits. Current groups
and viewport symbols also rely on `PatternGroup` constraint metadata; update native
group rendering/selection/edit routing so linked patterns need no dummy constraints.
Current `SketchObject::solve` passes all internal geometry to `Sketch::setUpSketch`;
generated geometry needs explicit native handling in solving, dragging and recompute,
not merely a post-recompute Python patch.

Validate source changes and dragging, exact transformed lines/arcs/circles/splines,
all layouts, construction geometry, source-only solver freedoms, empty inputs,
unrelated geometry/constraints, Undo/Redo, Cancel, save/reopen, stable references,
legacy edit/conversion, detachment, native commands and grouped viewport/list behavior.
Compare constraint/unknown counts and timings over increasing instance counts;
report measured results without promising a specific speedup. No problematic owner
file was supplied, so this work cannot diagnose that file's specific solver failure.

## Preview evidence

Production checkpoint `5adaef0a1113fc9641adca64b001c987e3572e49`.
Clean UI-only snapshot `6a3d0e7f8b82cc31529bf85f00e704bf08eb59c1` preserves the
unrelated untracked project.previewfirst.json. Companion `14eabfb1d1d4`, allowlist
`pattern_ui.py`, fingerprint `4bcad379a9e18d8abf1fa59f2172a2f02317af288039dbc10938d139c89d1e7b`.
Scope is valid with no violations. Eight UI checks pass: default, Cancel, explicit
legacy choice, old-mode edit state, detachment cancellation, circular controls,
simulated Apply/reset and no CAD/document changes. Captures were corrected to use
the native task group background in both baseline and candidate. No approval state
was set by the agent. Functional implementation/build/install remain pending.
