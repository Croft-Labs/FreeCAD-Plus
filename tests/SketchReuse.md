# Reusable sketch copy owner check (F053)

Use this fork's source-built application. In the Sketcher workbench, select a whole
root sketch in the tree, then **Sketch > Copy reusable sketch**. The first increment
accepts a free sketch with visible geometry, up to 500 geometry elements, and no
support, external geometry, expressions or other linked inputs. Body/Part-owned and
occurrence-selected sketches remain outside this increment; unsupported inputs show
an explanation and disable copying. References are never silently stripped.

1. Start with a dimensioned slot or other closed reusable profile, including a
   construction line. Recompute, select it and open the command. Review geometry,
   constraint and degree-of-freedom counts, and give the copy a name.
2. Set X/Y/Z offsets in the **source sketch's axes**, then a rotation about its
   normal. Rotation is about the source origin, followed by the offsets. Z offsets
   the sketch plane. These are placement changes on the new sketch, so horizontal
   and vertical constraints remain meaningful in its own plane.
3. Choose **Preview**. A non-pickable wireframe and numeric world origin show the
   proposed placement without creating an object or Undo entry. Preview frames the
   whole scene to include the proposed copy. Changing a value
   clears the old preview; choose Preview again. Cancel clears it without copying.
4. Choose **Create independent copy**. The dialog closes and a visible native sketch
   appears. Edit the copy's named radius/length dimension; its internal constraints
   should still solve, and construction geometry should retain its role. The source
   should not change. Source consumers are not copied or relinked.
5. Undo and Redo the copy. Extrude the copied closed profile, save/reopen, and change
   a copy dimension again. Verify the copy's solid updates independently. A source
   edit while the dialog is open invalidates its review and removes the preview;
   recompute as needed and choose **Review again**.

This copies the entire sketch through FreeCAD's native document copier. Geometry
order/internal constraint indices stay within the copied object; there is no partial
geometry paste or cross-sketch index remapping in this increment. Expression/reference
policy choices, blocks, reusable-profile libraries, sketch patterns, nested scopes,
selection snapping and physical/high-DPI acceptance remain open under F053.

Automated coverage: `TestSketchReuse`, grouped with the native Sketcher solver and
`TestSketchSupportCommand` suites. The tests cover a closed constrained slot, named dimensions,
construction geometry, a rotated source plane, typed copy placement, preview/commit
agreement, stale and unsupported inputs, owner transactions, rollback, Undo/Redo,
save/reopen and downstream extrusion. Exact accepted evidence is in roadmap 11.6c/d.
