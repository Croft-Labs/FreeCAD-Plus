# Approved workflow batch — November 27, 2026

Owner's “Ensure that all of the pattern buttons are connected to the new workflows ...
Implement all” approved the seven outstanding previews listed below. Fingerprints
were rechecked fresh without violations. Chat approval was used; companion approval
state was not changed. This delivery supersedes pending-preview status in the earlier
evidence entries, while preserving their original diagnostic records.

## Delivered behavior

- Native Mirror, Linear Pattern, Polar/Circular Pattern and Multi-transform commands
  route Plus documents directly to whole-body/sheet collectors before the Classic
  active-Body gate. Complete finished solids include earlier cuts. Ordered multi
  steps, picked references, placement, reverse and editable dependencies persist.
  Merge fuses touching copies and keeps separated solids in one compound-capable
  Body/History item. Unmerged copies stay independently editable members of a group.
- Intersection curve remains inside sketch editing, with one mixed source list and
  no Pick dropdown. Earlier owned component geometry only; exact edge/face picks are
  preserved. Solids/sheets yield section curves; curves yield discrete crossing
  points. Self, later, foreign, coplanar-curve and missing intersections are rejected.
  Native linked geometry retains whole-source associativity as the source or sketch
  plane changes. Source/target Body placements and valid link scopes are respected.
- Mesh from Shape accepts selection after opening and creates one combined owned
  mesh from selected solids/sheets/faces. Native mesher parameter controls remain;
  the result belongs to component History, avoiding the ownerless-object projection
  failure. Recipes, source dependencies and supported face colors persist.
- Trim Body uses one connected finite surface boundary or an infinite fundamental/
  datum plane, offset and reverse. Short finite boundaries are rejected rather than
  extended. Linked results remain editable, with retained/source appearance.
- New body/surface clones copy source materials/transparency at creation, including
  direct-occurrence overrides; subsequent clone appearance edits remain independent.
- Native document tabs are above the viewer. New components hide fundamental planes
  while showing axes/origin. Sketch and datum-plane tasks temporarily reveal planes,
  restore prior visibility, and retain manual visibility choices.

Plus tasks use bottom Done/Apply/Cancel, clear their collectors and restore defaults
after successful Apply, retain inputs on failure, and preserve earlier Apply results
on Cancel. Transient previews do not create document objects or Undo entries. True
BRep edges avoid tessellation-line artifacts; draw-style changes update previews.

## Validation and installation

The native build completed successfully. The exact staged runtime passed 36 checks,
including adjacent Clone and joined-extraction regressions. After correcting Python
link scopes, all 20 batch checks passed again. The owner application passed the same
20 checks after installation. The final native Sketcher scope correction was checked
in staged and installed runtimes with the eight native command/picking tests.

Coverage includes all four actual transformation commands, analytic mirrored volumes,
touching/disconnected copies, linked recompute, Undo/Redo, saved reopening, task
Apply/reset/Cancel, mesh ownership/colors, whole and exact-topology intersections,
real viewport picking during sketch edit, placed Body sources, finite/combined/curved
trim boundaries, clone overrides, plane visibility and top document tabs. Screenshots
below are real task widgets captured from the installed application, not mockups.

All 39 installed payload hashes match the verified staging manifest. Installation
ran only while FreeCAD was closed, retained rollback copies, and preserved owner
profile and shortcut hashes. Tests use disposable documents and isolated profiles.
The final shortcut target, arguments and working directory are recorded separately.

Standard and Mefisto meshing succeeded. Netgen returns zero facets for the same box
through the unchanged native MeshPart API; the new task reports this failure without
changing objects or Undo state. A successful external Gmsh executable run was not
available for this verification; missing-executable failure is atomic. Saved documents
cannot choose an executable: recompute uses the user's native Gmsh preference.

## Direct installed screenshots

- [Linear pattern](LinearPattern.png)
- [Mirror](Mirrored.png)
- [Circular/polar pattern](PolarPattern.png)
- [Multi-transform](MultiTransform.png)
- [Intersection curve](IntersectionTask.png)
- [Mesh from Shape](Mesh.png)

## Approval records

| Preview | Session | Fingerprint |
| --- | --- | --- |
| Transformations | 57a9ef350816 | e5155de09ef0d38977d3304d63f55e4a50d320ffb7c8bf8cbad17edf077aab48 |
| Revised intersections | 87ac16544d40 | cb7f6976fc19abfc3e0f38cdc9512b1b309859f749d9cb941e0e98343f9c44db |
| Mesh from Shape | bd66e52a54b7 | 1dd42642e4633db7431d3e6e18f12dda0482b88d3550d1985421321332b09b15 |
| Clone appearance | c0b8bc31305f | 8a15aa40ce627f437098db93c3239043ba108c45c0c8df54b5770cdba7807332 |
| Document tabs | 305f2340501d | f9e5c2d6a754edfb801f48389d5bdfc3e8fd9e20a761452185ec7153625c16cf |
| Trim Body | 09e616fd8321 | f23cb753d14289f97f8de070e97439e27cbc06eaff6507deb3eaea54eacd51b4 |
| Fundamental planes | 40f73afdef86 | cc57c944c553e7bc62b9fa9f1c9d04c17075a8aa970dfc02de963015166c5de2 |

Implementation/build/runtime verification is complete. Publication is recorded by
the Git commits containing this evidence and verified origin branch state.
Saved last-active-part bookmarks remain separately pending and were not included.
