# Unified Clone and separate Extract geometry: native UI proposal

November 25, 2026. Owner requested unified Clone with whole-object-only input and
simple lowercase result names. Face extraction must follow cloning as a separate
Extract geometry operation. This was the native task-layout proposal; it did not
change production functionality. The owner subsequently renewed implementation
authorization. See [implemented functionality and delivery](../clone-extract-20261125/README.md).

## Direct screenshots

- [Clone and Extract geometry side by side](proposal.png).
- [Clone](clone.png): one whole-object list and automatic result names.
- [Direct-child browser](direct-children.png): objects beneath child occurrences.
- [Whole-object-only feedback](whole-object-only.png): no direct face cloning.
- [Edit cloned body](edit-clone.png): same form with the existing result's source.
- [Extract geometry](extract.png): a face on cloned body becomes extracted surface.
- [Edit extracted surface](edit-extract.png): same form, prefilled face reference.
- [Current ribbon group](baseline.png) and [proposed group](commands.png).

The disabled Modeling / Other Add Reference Object placeholder becomes one Clone
command. Extract geometry is a distinct adjacent command; no whole-part versus
single-element Clone split. Existing upstream unrelated Clone tools are untouched.
Native ribbon entries retain the current icon-only medium-button style and named
tooltips. Screenshots of tasks are the primary deliverable.

## Owner contract and proposed interaction

Clone selects complete geometric objects owned by a direct child, via that exact
child occurrence. No grandchildren, component-aggregate flattening, or isolated
faces/edges/vertices. Bodies, surfaces/sheets, sketches and planes produce the
default labels `cloned body`, `cloned surface`, `cloned sketch`, `cloned plane`.
Repeated result types may receive a distinguishing suffix while retaining that
simple base name. These are geometry-feature labels, not new component definitions.
Parent component-name uniqueness and shared-definition identities remain separate.

The list follows existing collector gestures: activate by clicking, click adds,
Shift-click removes, Remove/Delete/Clear remove inputs. Browse direct children
offers whole objects only; each occurrence remains distinct even for the same
shared definition. Native body/feature containers do not introduce component levels.
Reference children are eligible for explicit promotion; Excluded children are not
new Clone inputs. The fixture browser is not a working eligibility implementation.

Results are parent-owned derived geometry with no copied child construction history.
The source child retains sketches, driving constraints and modeling operations.
A cloned sketch supplies its complete geometric result, without the source's driving
constraints. Cloned planes preserve their plane/frame semantics. Parent feature
operations may modify or combine the cloned body; Clone itself does not merge bodies.

Source association is retained as in the prior contract. Geometry and occurrence
placement updates recompute the Clone in the parent's coordinates, then downstream
features. Missing sources/topology must report errors, not silently select another
object or detach the result. The update statement is part of this proposed review.

Extract geometry is a separate parent feature. The reviewed example selects one
or more faces on a parent-owned object, such as cloned body, and produces extracted
surface results while retaining the input object. Raw child faces cannot bypass
Clone. This proposal covers face-to-surface extraction; edge/point extraction modes
are not invented here. The result retains its source-face association.

Batch Clone creation makes one result per selected object in one Undo operation.
Editing one existing result reopens the same form with one source, preserves its
identity/downstream references, and does not edit other batch results. Extract
creation/editing follows the same pattern. Cancel changes no source, result, document
or Undo state; preview is scene-only. Neither operation edits the child's history.

## Remaining functional work after approval

Implement commands and native result types; bind occurrence-aware collectors to
actual direct-child ownership; transform source result into parent coordinates;
persist explicit source/occurrence references and recompute; validate broken refs,
topology, cycles, excluded inputs, stale Edit state and read-only sources. Native
format validation must recognize only this explicit derived-geometry association,
without weakening raw Reference/cross-file modeling guards. No schema decision has
been implemented by this presentation proposal.

Verify whole body/surface/sketch/plane outputs, repeated/imported children, rejection
of grandchildren and subelements, native body Boolean/feature use, extracted-face
surface use, source changes, create/edit/Cancel, Undo/Redo, save/reopen and independent
export. Verify installed behavior and the existing desktop shortcut before delivery.

## Capture provenance

Clean toolbar_layout.py snapshot from production d68bab2182e6e1048d2f5988b8a7a8056c5150e7.
Review 4a3678c76c7b allows toolbar_layout.py and clone_ui.py only. Final fingerprint
a74982217414f97465e8e4d10887fffb42efe054dab2c7eb6e1685f292193db8.
Capture is fresh with no scope violations; approval remains unset. Unrelated
project.previewfirst.json and all pending earlier instance proposals are preserved.

Existing installed FreeCAD rendered actual Qt tasks, browser, ribbon entries and
shared TaskStatus feedback in isolated profiles. Disposable fixture has a real
direct-child native body, sketch, plane and sheet, with a Reference child. Both
final runs pass unchanged document structure/placements, Undo and Edit checks.
Expected lowercase result labels are asserted. Final stderr is empty. The first
fixture run supplied the wrong parent to display.set_state; the harness was corrected.

Source/result lists, eligibility and edit states are presentation fixtures, not
persisted Clone objects. The preview accepts no geometry operation. No live source
recompute, geometry preview, extraction, body combination or functional edit is
implemented/tested. These screenshots must not be described as installed features.

Helpers and final logs/results are archived. Disposable validation profiles are
removed after archiving; isolated review worktrees remain for approval. Helper
paths record their original local runtime and require adjustment for other locations.
