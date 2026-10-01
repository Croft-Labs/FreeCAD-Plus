# Move or copy occurrence: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Evidence: `D:\Temp\Office-PC\freecad-plus-occurrence-move-20261001`.
Existing installers do not contain this batch.

1. Open `visual-accepted\Nested-Occurrences.FCStd`. First and Second share Bracket inside
   two rotated Part containers. The source and occurrence also have rotations.
2. Select First itself in the tree, then **Tools > Move or copy occurrence**.
   Choose Translate, Occurrence frame, and X = 10 mm. Click **Preview**: the teal
   wireframe shows the destination while the original remains visible. No document
   object or model transaction is created by preview.
3. Click **Move once**. Only First moves along its current occurrence X axis.
   Reopen the command with World frame and X = 10 mm: this moves along world X.
   Coordinates are incremental offsets, not absolute positions. Numeric fields
   use explicit mm, degrees or a dimensionless axis direction.
4. Choose Rotate. Enter a nonzero axis, angle and pivot coordinates in the selected
   frame. World pivot (0,0,0) means the document origin; Occurrence pivot (0,0,0)
   means this link's placement origin. Preview reports the resulting world origin.
5. Cancel removes the ghost and leaves placement unchanged. Editing fields clears
   the old preview. An external model/frame edit invalidates the review and ghost;
   recompute if needed, then **Review again**. Confirmed movement has one Undo step.
6. Undo/Redo, save/reopen and edit Bracket.Length. Both occurrences still share the
   source geometry, while only the selected placement changed. The saved
   `visual-accepted\Moved-Occurrences.FCStd` is a ready-made result.

The movement service composes enclosing structural Part transforms with LinkPlacement
and converts the resulting world placement back into the parent frame. Occurrence axes
refer to that link frame; LinkTransform controls source placement through native Link
semantics and is preserved. This is a one-time placement change, not a solver drag or
new relationship. Objects with non-Part consumers, expressions, scales/arrays or
read-only placement are refused rather than detaching constraints.

Scope: one same-document direct Link to a Part solid/Body, nested only in structural
App::Part containers. No independent geometry copy, point picking, snapping, movable triad,
work-part frame, external links, subassembly paths or maintained relationship is
implemented here. Whole F072/F074/F075 and parent 10.7 remain open for those broader
requirements and physical/high-DPI acceptance. Stop here for owner workflow feedback.

## Shared-definition copy (F072; 10.7c/d)

1. Select First and open **Tools > Move or copy occurrence**. Choose **Copy occurrence
   (shared definition)**, enter a copy label and a translation or pivot rotation.
2. Preview. The teal wireframe uses the same frame/transform semantics as Move;
   the source occurrence stays in place and no document object is created yet.
3. Choose **Create linked copy**. One new native Link is created in the same
   structural Part container, retaining source, appearance and visibility. This is
   a shared-definition instance, not Make Unique. Original/source placements stay.
4. Undo removes the copy; Redo restores it. Save/reopen, then edit Bracket.Length:
   First, Second and the copy all update from that definition. Copy placement stays
   independent. A zero offset deliberately makes a coincident copy.
5. Cancel an additional preview. No extra link should remain. A changed source or
   parent invalidates review; recompute and Review again before copying. Empty labels
   and pending owner transactions refuse creation without changing the original.

Run `TestOccurrenceCopy`, `TestOccurrenceMove` and `TestCommandSearch` in the matching
source-built GUI. Native appearance, LinkTransform, nested placement and rollback
are covered; independent definitions, constrained occurrence remapping, external
sources and full F072 acceptance remain outside this checkpoint.

Copy evidence: `D:\Temp\Office-PC\freecad-plus-occurrence-copy-20261001`.
One grouped script-staging pass; 25 distinct selected checks pass and five captures
were reviewed. In visual/, Copy-Sources.FCStd is the original fixture;
Linked-Copies.FCStd contains the new link; Edited-Copies.FCStd shows all three
occurrences following a later source-length edit. Existing installers are unchanged.
