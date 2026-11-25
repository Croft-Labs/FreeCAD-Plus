# Instance quantity and patterns: native UI proposal

November 25, 2026. Owner requested an instance quantity workflow including patterns.
Required native layout preview is ready for direct screenshot approval. Production
source and installed behavior are unchanged; no backend implementation is claimed.

## Screenshots

- [Current Add existing](baseline.png) and [proposed navigator](navigator.png).
- [Quantity](quantity.png): independent placements, one shared definition.
- [Linear](linear.png): count, start, direction and spacing.
- [Grid](grid.png): columns/rows, two directions and spacings; count is their product.
- [Circular](circular.png): count, center, axis, radius, start angle, full-circle or
  angular spacing, and orientation. Full circle excludes a duplicate endpoint.
- [Edit pattern](edit-pattern.png): same form, populated presentation fixture.
- [All creation modes](proposal.png).

The existing navigator remains the first step. Next opens Create instances; Change
parts returns to the navigator. Quantity defaults to one. Examples show six new
instances per checked definition; two checked definitions would create twelve.
Count includes the first newly created placement and excludes existing occurrences.
Add new creates exactly one definition and the requested links upon acceptance;
the separate New Component command remains unchanged. Pattern coordinates belong
to the edited destination component, independently of the active assembly.

## Intended functional contract after approval

Quantity creates independent native links at the entered position. Linear, Grid
and Circular create an editable pattern with native links and saved parameters
owned by the destination component. Members continue sharing the source definition;
this never duplicates modeling history. Right-click a member to Edit instance
pattern using the same form. Pattern placements remain controlled by that pattern;
ordinary quantity instances can be moved/constrained independently.

Preflight definitions, destination/Edit token, geometry references and all recursive
component/file dependencies before mutation. Reject invalid counts, nonfinite
values, zero direction vectors, parallel grid directions and invalid angular/radius
combinations with shared TaskStatus errors. Preview is scene-only. Create/edit is
one atomic Undo step; Cancel creates no links or new definitions. References and
placements resolve in the destination's frame; active assembly stays fixed.

Preserve surviving link identities on pattern edits. Refuse reductions that would
remove members used by constraints or other dependents, with an actionable message.
Do not silently delete constraints or reassign references. Save/reopen, external
definition ownership, shared subassembly occurrences, editable export and schema
compatibility require acceptance checks. Native constraint/Move integration must
not silently fight pattern-controlled placements. No implementation is yet present.

The earlier condensed/expanded view proposal remains separately pending. Group
counts eventually derive from actual links, not pattern metadata. Explicit Remove
instance and global name enforcement remain separate requests.

## Capture provenance and verification

Clean snapshot of component_add.py from production f7af81a30e10fe0a701b2acd4d5c569f4c0002e0.
Review ef9fa8610a64 allows component_add.py and instance_quantity_ui.py only.
Final fingerprint 9027c86fe3a312851df4dca056c5e4ce1f31059e249a268ff0bd56e209d50046.
Fresh capture; no scope violations; approval unset. Unrelated project.previewfirst.json
was preserved. Neither original repository modules nor installed modules were edited.

Existing owner FreeCAD executable rendered actual Qt navigator/task controls with
native unit inputs, in isolated profiles and disposable documents. Final baseline
and candidate fixture runs pass unchanged document structure/placements, Undo count
and Edit context checks; candidate stderr is empty. Mode totals and an eight-member
edit fixture are checked. This is presentation evidence only: Next, reference picking,
Change parts, live geometry preview, commit and persistence are not wired. No runtime
pattern creation/editing tests have run. The displayed edit form does not prove a
saved pattern can reopen.

Helper scripts and final logs/results are archived here. Generated validation
profiles are removed after archiving; isolated review worktrees remain for approval.
The renderer uses the archived helper's original local location when replayed;
adapt its source root if replaying directly from this evidence directory.
