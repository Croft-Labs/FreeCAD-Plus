# CAM setup-template reuse (F096)

This delivery extends the existing CAM **Export Template** and **New Job**
commands. Native model clones, stock, tools, setup sheets and job properties are
reused. It does not copy an operation sequence or generated toolpath.

1. Configure a representative job, including its tools/feeds, stock rule and post.
   Export Template, choose a name and revision, and select the settings to include.
   Model-bound stock offsets are useful for differently sized models. A fixed box,
   cylinder or stored placement still requires review against the new model.
2. Save as `job_*.json` in the CAM template search directory. Export writes native
   format 1 and the stored-value unit convention (`mm, s, deg`). Quantity strings
   retain their explicit units. Document display units do not rescale the model.
3. Create a new job, choose its model and template, and read the settings review.
   It lists stored post arguments/output, stock rules, tools/feeds and setup values;
   omitted settings explicitly use current defaults. Legacy files identify their
   missing name/revision metadata rather than inventing a revision.
4. Unavailable posts, unsupported formats/tools, incomplete stock data and detected
   model-specific expressions block template use before job resources are added.
   Correct the file or choose another template. A file changed during review must
   be reviewed again; acceptance captures the exact displayed settings.
5. Inspect the created job. Tools and setup objects are independent, stock uses the
   new model, and name/revision provenance appears under **Setup template**. Values
   remain editable. Changing the template file later does not update existing jobs.

For a simple check, use a 12 x 10 x 5 mm box with X stock margins 2 and 3 mm.
Reuse its template on a 30 mm long box: X stock length should become 35 mm while
the original job stays at 17 mm. Verify the selected post and 600 mm/min horizontal
feed. Undo/Redo the new job, save/reopen, and enlarge the new model again. No cutting
operations should have appeared automatically.

Run `TestSetupTemplates` in the source-built GUI with `tests` on `sys.path`, alongside
`CAMTests.TestPathSetupSheet` for the grouped encoding/rebinding checks. The roadmap's
14.4a/b entry owns build/staging, runtime and reviewed-capture evidence.

Full F096 remains open for operation sequences and geometry-collector remapping,
complete machine/tool asset compatibility, broader expression/reference repair,
localization and physical workflow acceptance. Compatibility checks do not certify
machine motion or replace reviewing the instantiated job. No installer or release
is implied by this local checkpoint.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-setup-templates-20261001`.
One PathScripts staging pass and 16 distinct native checks pass; six final captures
were reviewed. `visual-accepted/job_metric_fixture.json` and
`visual-accepted/Reused-Setup.FCStd` provide the owner fixtures. The fixture's available
legacy post is not a tested machine configuration or posted-output validation.
