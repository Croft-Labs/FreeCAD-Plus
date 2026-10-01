# Joint motion and limit review (F076)

Use the source-built FreeCAD Plus fork and enter an Assembly. Select references
on two different components, then open a native Fixed, Revolute, Cylindrical,
Slider or Ball joint. Existing joints can also be edited.

1. Read the motion explanation beneath the controls. It describes this joint's
   relative motion; other joints and grounding may restrict it further. Review
   the existing assembly solver messages for the combined result.
2. Hover a selected-reference row to inspect its document, component and subelement
   identity. The normal joint coordinate systems, flip and offset controls remain.
3. For Slider, enable both length limits and enter minimum 10 mm, maximum -10 mm.
   The inline message should explain the reversed bounds. OK keeps the task open.
   Correct them to -10 mm and 10 mm, then accept.
4. For Revolute, repeat with angle minimum 90 degrees and maximum -90 degrees.
   Cancel restores the previous joint and placements. For a new joint, Cancel
   removes the unfinished relationship. Cylindrical validates both limit pairs.
5. Disabled or unsupported limits do not block acceptance. Equal enabled bounds
   are permitted. Expressions are evaluated before acceptance and retained.
6. Undo/redo the accepted edit, save, close and reopen. Check the joint type,
   references, enabled limits and their values.

This task checks inputs before the native solver can swap reversed bounds. It does
not change direct property-editor or scripted solver behavior. It does not certify
collision-free movement, the full motion envelope, or solver conflict diagnosis.
Automatic contextual suggestions, ambiguous-reference alternatives, direction
previews, broad nested/external assemblies and owner physical acceptance remain
open under full F076. Rotate to another family pending owner workflow feedback.

Run `TestJointReview`, `TestAssemblyFreedom` and `AssemblyTests.TestCore` in the
source-built GUI with `tests` on `sys.path`. Roadmap 12.4c/d owns the evidence.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-joint-review-20261001`.
Eight task checks pass in joint-verified/ and 21 existing Assembly checks pass in
grouped/. Six reviewed visual/ captures and two FCStd fixtures show Slider correction
and Revolute Cancel. Captures preceded the final acceptance-only synchronization
correction; final tests include a preview solve followed by correction to 10..20 mm.
Both tasks preceded validation. Only Python staging was needed; no native rebuild,
installer update, release or physical owner acceptance is claimed. Earlier failed
runs retain the solver-normalization finding and Undo-count fixture correction.
