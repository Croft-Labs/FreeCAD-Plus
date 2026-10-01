# Reviewed face extension (F066)

Use the source-built FreeCAD Plus fork with the Surface workbench enabled.
Select one face on a root Part shape or root Body, then use **Surface > Extend
Face**. The existing command opens a review before creating geometry.

1. Check the source document/object/face identity. Set the four independent U/V
   side extensions. Values are percentages of the original parameter span:
   positive grows, negative shrinks. These are not millimetre distances and may
   have different physical effects on curved surfaces.
2. Choose fitting tolerance in mm and U/V sample counts. This bounded review
   supports 4–64 samples per direction and 0.0000001–10 mm tolerance.
3. **Preview surface** shows a non-pickable boundary overlay. Computation uses
   copied source geometry in a hidden temporary document; no source document
   feature or Undo transaction is created by preview.
4. Enter -50% on both U sides. The empty domain must be refused. Correct either
   side and preview again. Changed settings clear the old preview. A changed
   source requires closing the review and selecting the face again.
5. **Create surface** creates one native associative `Surface::Extend`. Cancel
   removes only the overlay. Source geometry and visibility remain unchanged.
   Undo/redo creation; save and reopen. Editing the source updates the result
   and downstream consumers. Later feature parameters remain available through
   the native property editor.

The native method samples the underlying surface and fits a rectangular B-spline
face. It does **not** preserve original trim loops or holes. A 10 × 8 mm plane
with 5% on all sides becomes 11 × 8.8 mm, area 96.8 mm². With a hole in that
plane, zero extension still fills the rectangular domain rather than retaining
the hole. This method does not reconstruct missing original design intent.

Fitting tolerance is an algorithm input, not a certified maximum-deviation or
self-intersection bound. Full F066 remains open for associative trim-region
selection, true supported untrim domains, graphical U/V direction handles,
broader periodic/imported surfaces and physical owner acceptance. Stop at this
bounded checkpoint and rotate pending workflow feedback.

Run `TestExtendFaceReview`, `TestSectionReview` and `SurfaceTests.TestBlendCurve`
in the matching built GUI with `tests` on `sys.path`. Roadmap 13.1e/f owns results.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-extend-face-20261001`.
One 190-second SurfaceGui/SurfaceScripts build followed both task implementations.
Surface was enabled in the local build configuration. All 19 grouped checks pass;
after a Python-only boundary-overlay correction, all nine task checks pass again
in extension-final/. Six visual-final/ captures are reviewed. Three FCStd fixtures
cover the source plane, accepted plane and accepted cylinder. No installer update,
release or physical owner acceptance is claimed.
