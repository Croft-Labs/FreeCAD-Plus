# Design Selection toolbar acceptance

`TestDesignSelection.py` separates Python policy and toolbar tests from checks that
require the new native FreeCADGui and SketcherGui. WORK_STATE owns current evidence.
The source-overlay run must not be treated as proof of the new C++ selection gate.

## Automated fixtures

- `TestDesignSelectionPolicy`: actual sketch/solid/sheet/origin taxonomy, checkbox
  policy, construction indices, nested repeated occurrence paths, object boundaries,
  periodic seams, branches/loops/tolerance, body chains and persistence/deletion.
- `TestDesignSelectionToolbar`: defaults, preferences, controls and Design/CAM/Classic
  visibility transitions through the actual Ribbon class.
- `TestDesignSelectionNative`: run after rebuild; gate/filter intersection,
  preselection and Equal followed by Construction with retained native selection.
- `TestDesignSelectionBoxes`: run after rebuild; actual viewport drag events for
  directional off/on and checkbox union across edges and vertices.

## Grouped acceptance in workload prompt 10

1. Start the intended Plus payload with isolated settings. Confirm the Selection
   toolbar is beside Save/Edit above the ribbon in every Design tab. Switch mode
   and Classic/Plus; verify no restrictive Design policy leaks into other modes.
2. Use a Body, its sketch, a separate sheet, a spatial wire, datum planes and points.
   Independently toggle each category and compare native hover, clicking and box
   selection. A body-owned sketch edge is a Curve, not an Edge; its endpoint is a
   Point, not a Vertex. Confirm a command gate remains narrower than the filter.
3. Click curves using each intent, including construction curves, a branched chain,
   a tangent arc/line pair, a closed loop, coincident screen projections at different
   depths, and repeated component instances. Check selected paths and highlight.
   Do not expand input lists owned by Extrude/Loft/Pipe reference collectors.
4. Drag partial and full boxes in both directions at two zoom levels, in 3D and
   sketch edit. Directional OFF requires enclosure in both directions. ON permits
   crossing right-to-left, with a dashed border. Test a thin box between samples.
5. With Persistent ON select three sketch lines, apply Equal, then Construction.
   Verify retained highlight, native operation results and undo/redo. Turn it OFF
   and verify completion clearing. Invalid input retains correction context.
6. Escape and clicking empty space must clear selection; hiding a palette or merely
   moving the pointer must not. Delete selected geometry/objects and undo; verify
   no delayed callback selects a different entity under a reused index.
7. Reopen a saved fixture, confirm geometry/history/occurrence identity is unchanged
   by selection-only operations, and restart with explicit toggle preferences.

Native projected bounds/tessellation retain their existing accuracy limits. Tests
and scripted GUI events do not replace physical owner/high-DPI acceptance. The
owner DOCX must be rendered and visually reviewed before final delivery.

Recovery item 6 adds nested queued Escape lifecycle/generation guards and a native
later-click/mode-exit regression. Controlled Python scheduler checks pass four
orderings; native execution remains deferred to item 7. See RecoveredWorkload.md
for the updated 19-check Selection group and exact grouped acceptance procedure.
