# Move occurrence once: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Evidence: `D:\Temp\Office-PC\freecad-plus-occurrence-move-20261001`.
Existing installers do not contain this batch.

1. Open `visual-accepted\Nested-Occurrences.FCStd`. First and Second share Bracket inside
   two rotated Part containers. The source and occurrence also have rotations.
2. Select First itself in the tree, then **Tools > Move occurrence once**.
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
App::Part containers. No geometry copy, point picking, snapping, movable triad,
work-part frame, external links, subassembly paths or maintained relationship is
implemented here. Whole F072/F074/F075 and parent 10.7 remain open for those broader
requirements and physical/high-DPI acceptance. Stop here for owner workflow feedback.
