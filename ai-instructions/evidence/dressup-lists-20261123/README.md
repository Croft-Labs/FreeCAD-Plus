# Shell and shared dress-up list controls - November 23, 2026

Owner approved implementation of the amended Shell face-list preview and the same
interaction for Fillet/Radius and similar workflows. The chat approval is
"implement all previewed changes, the shell, radius, etc". Companion session
b5a2f4e5bd58 remains a prototype record; its approval flag was not changed by the agent.

Shell opens without preselection, including with curves or sheets selected. Faces
identify the solid; there is no target field or selection toggle. Click the list
to collect faces, Delete/Remove to remove highlighted rows, or Clear faces to start
a different solid. Invalid inputs retain valid rows and show a prominent error.
Thickness, mode, join, intersection, inward direction and preview options remain.

Fillet/Radius, Chamfer and Draft use the shared native list controls in component
documents. List focus activates picking; parameter focus leaves collection while
retaining references. Repeated picks add only once. Clear disables Use all edges.
Selection and persistence use explicit component geometry, not Classic active Body.
Classic documents retain their native controls and semantics.

Shell previews use native OpenCascade thickness geometry without creating document
objects. Accept commits a native PartDesign::Thickness atomically. Existing feature
IDs/properties remain native; Cancel creates no undo step. Shared History switching,
manual visibility choices, source eligibility and predecessor ordering apply.

## Validation

- Development build completed; 20 focused native tests passed.
- All 99 installed native regression checks passed, including component input
  boundaries, Classic compatibility, the consuming-selection freeze regression,
  numeric commit, History/visibility, list scrolling, Cancel and Undo/Redo.
- Installed viewport audit passed after switching from final preview to collecting.
- Fresh-process saved Shell retained identity, Face6 reference and volume
  1376.0000000000007; recompute and edit/Cancel passed.
- Existing desktop shortcut target/working directory and isolated launch passed.
- Eight installed payloads have hash-verified rollback records.

Earlier validation iterations exposed test assumptions about the removed selection
button and a test that accessed a deleted status widget after successful acceptance.
Those tests now exercise the approved interaction. Scrolling uses an eight-face
solid so its list actually overflows the viewport.

## Direct captures

Screenshots are real installed native UI, not the prototype.
- [Shell face collector](shell-installed.png)
- [Invalid curve stays in the task with highlighted guidance](shell-invalid-curve.png)
- [Fillet/Radius shared collector](fillet-installed.png)

The installed payload is the app runtime, not the build tree. Native dependencies
were rebuilt as needed; the changed native payload is PartDesignGui.pyd. The eight
installed files and rollback hashes are recorded in install-manifest.json.
Validation profiles were isolated, and the owner profile was not changed. The
shortcut verification leaves an empty isolated app window open.
