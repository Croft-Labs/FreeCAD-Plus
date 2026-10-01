# CAM mesh preparation owner check (F091)

Use this fork's source-built application. In the CAM workbench, select one whole
imported mesh in the tree and choose **CAM > Review CAM mesh**. The command is in
the job/setup command group. It accepts root `Mesh::Feature` objects with up to
200,000 triangles; Links, nested meshes and generated job models are outside this
first increment. Inspect the imported source before creating a job.

1. Import a known-size STL and review it. Check its dimensions and minimum/maximum
   XYZ in millimetres. STL carries no unit declaration: the review reports the
   imported coordinates and does not guess or change the intended scale.
2. Compare a closed enclosure, an enclosure missing a face and two separate pieces.
   Boundary edges, nonmanifold edges and connected components should distinguish
   these cases. Orientation is reported only for a single closed, consistently
   oriented component without duplicate or zero-area triangles. Open boundaries
   are not automatically treated as unusable for Parallel finishing; Waterline
   reports the need to inspect open/broken contours.
3. Review a closed enclosure with all normals reversed. **Create reversed-normal
   copy** should become available. Its explanation is the preview: every triangle
   winding will reverse, with the same coordinates, placement and dimensions.
   Confirm to create an independent mesh. The source stays visible and unchanged,
   so the coincident meshes may look identical. Select the new tree object explicitly
   when making a new job; existing jobs remain linked to their original model.
4. Undo and Redo the copy. Save/reopen and inspect both meshes. Editing the original
   should not alter the independent copy. Closing the review without copying should
   create no objects or Undo entry. Changing the document invalidates the report;
   recompute when needed, then choose **Review again**.
5. Check a dense fixture. At 100,000 triangles the review reports density without
   changing it. Above 200,000 it refuses this bounded inspection and points to the
   Mesh workbench; no decimation is performed.

This is a preparation diagnostic, not machining approval. Self-intersection tests,
per-piece orientation, highlighted defect regions, hole filling, welding, smoothing,
decimation, scaling and broader input scopes remain open. It does not add toolpath
gates, generate paths, relink jobs or claim collision/stock/tool clearance checks.
The zero-area threshold is twice the triangle area <= 1e-12 mm², a numerical
degeneracy check rather than a welding or manufacturing tolerance.

Automated coverage: `TestMeshPreparation` (native meshes, dense/open/defective inputs,
placed copy isolation, atomic rollback, Undo/Redo, save/reopen, installed command and
dialog lifecycle), grouped with `CAMTests.TestMeshMachining` for existing direct-STL
Parallel/Waterline, stock, holding-tab and indexed-setup behavior. Exact accepted
results are recorded under roadmap 14.1a/b; physical owner acceptance remains open.
