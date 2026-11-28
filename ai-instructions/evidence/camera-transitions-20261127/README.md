# Camera transitions — installed November 27, 2026

Owner reported zoom-out, flicker and zoom-in when opening/activating parts and
requested testing and a fix. Owner could not recall the exact activation gesture,
so coverage includes Parts/Assembly double-clicks, isolation, component windows,
normal saved-file reopening and the actual `Gui.loadFile` import dispatch.

## Findings and correction

1. `animatedViewAll` fitted a bounding sphere, processed a nested Qt event loop,
   and then applied a separate Coin fit. The two destinations differed. A baseline
   component-window trace went from height 165.25 through 93.93, then snapped to
   23.71 instead of continuing a single transition.
2. Native origin graphics use `SoShapeScale`, whose world size follows the camera
   to maintain fixed pixel size. Including that transient size in a fit created a
   feedback loop. Repeated baseline fits on the same isolated part produced heights
   39.9253, 11.4791, 7.6176. `SoSkipBoundingGroup` now excludes those graphics during
   a fit, preserving their normal drawing, picking bounds and visibility flags.
3. `setCamera` did not cancel an older navigation animation. A saved camera was
   overwritten by a pending rotation. Restoration and projection changes now
   cancel the older animation. Fits use the shared navigation animator and one
   exact copied-camera target, preserving a pending standard-view orientation.
   There is no nested event loop or final refit/snap. Scaled fits supersede prior
   fits too; pre-existing skip-bounding modes are restored rather than overwritten.
4. Generic importer dispatch automatically refitted `.cadprt` after restoring its
   saved camera. Native Plus archives with saved camera settings now retain that
   camera, matching native FCStd behavior; imports without a saved camera retain
   the existing AutoFitToView behavior.

This repairs camera ownership and bounding-box calculations in the existing
workflow; it adds no UI controls or workflow redesign. Navigation animation
preferences remain enabled and unchanged. No camera changes were observed for
ordinary settled Parts/Assembly activation in the test fixture; those routes are
covered for preservation rather than falsely claimed as independently reproduced.

## Verification

- New `TestCameraTransitions`: **10 installed native tests pass**, covering actual
  double-clicks, exact fits, origin feedback, no nested callbacks, saved-camera
  restoration, interrupted/scaled fits, projection switches, orthographic and
  perspective orientation+fit, new views and GUI file reopening. Geometry/Undo and
  original-view camera are preserved. Installed image capture inspected.
- Old binaries: the initial eight-test camera suite produced seven failing
  assertions (one test has two projection subtests). See `b4/tests.txt`.
- Final staged broad run: **51 tests, 46 pass; four failures and one error**. All
  five reproduce identically on the unchanged installed binaries (`b5`), verified
  by matching test names and exception messages. They concern historical panel
  expectations (automatic History switching, active-root rows, occurrence memory,
  dock-close isolation teardown) and a duplicate-name import fixture. They are
  not repaired or marked passing by this camera change.
- Final installed focused suite: **33 tests, zero failures/errors** (`i1`). It
  includes camera transitions, current component navigation, single-part opening
  and coordinate-frame/target workflows. Existing intentional invalid-geometry
  cases may emit expected messages in stderr; test results remain successful.
- Whitespace checks pass for changed production/test source and maintained project
  documentation with `core.whitespace=cr-at-eol`, matching existing CRLF source.
  Raw archived logs/harness retain their original whitespace for hash verification.

## Installation and scope

Installed only `bin/FreeCADGui.dll` and `Mod/FreeCADPlus/TestCameraTransitions.py`.
The DLL matches the verified staged/build library; the test matches source/build.
Owner profile `.cfg` files and desktop shortcut hashes are unchanged. The owner
application was confirmed closed before replacement. Rollback copies remain at
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/camera-activation27/rollback`.

Previously pending Transformation, fundamental-plane defaults, Sketch Intersection
Curve and Trim Body previews are not implemented or approved by this correction.
Untracked `project.previewfirst.json` is unrelated and remains untouched.

## Evidence notes

`i1` is authoritative installed evidence; `s4` is the final broad staged run.
`b1`/`b2` are initial camera traces. The attempted `Gui.open` call in b2 is an image
API and did not open cadprt; b3 records its wrong-arity variant. Both are retained
as harness errors, not successful file-open evidence; the final tests use the
verified `Gui.loadFile` API. `s1` ran an old library after initial staging hit a
Windows path-length limit in an unused Qt compiler object. The completed staging
excludes compiler objects and verifies the DLL hash. `s2` is an intermediate
diagnostic, before the origin-fit correction; `s3` passed the first eight tests.

Trace JSON is losslessly gzip-compressed where large. `archive-manifest.json`
records original hashes and archive paths. Generated test documents/profiles and
the private test runtime are removed only after archive verification. Build and
owner runtime remain outside the checkout. Retain rollback and install manifests.
