# Clone appearance — diagnosis and pending preview

**Awaiting owner approval. No functional implementation or installation.**
Owner requests that cloning a body or surface import its child-object appearance
into the active part. No additional controls or changes to the Clone task layout.

Companion session `c0b8bc31305f`; UI-only allowlist `appearance_ui.py`.
Fingerprint `8a15aa40ce627f437098db93c3239043ba108c45c0c8df54b5770cdba7807332`.
Inspection: current, valid scope, approval false. Main source `c07b767008`.

[Current native result](baseline/comparison.png) · [Proposed appearance](candidate/comparison.png)

## Diagnosis

The installed `derived_geometry.save` copies shape and source dependencies but
never initializes the result's materials. An actual two-source Clone operation
was run in a disposable Plus assembly: a six-face Body and a two-face sheet.
The source Body's final feature has blue faces, a green top and 20% transparency;
the sheet has purple/gold faces with 45%/10% transparency. Both cloned outputs
instead have default grey/opaque materials. Geometry face counts and one-Undo
creation are correct; source materials remain unchanged.

PartDesign `ViewProviderBody::getElementColors` resolves through the Body's tip.
Body rendering modes and persistent occurrence overrides require appropriate
material resolution; reading stale Body-container defaults alone is insufficient.
Appearance task colors are authored on the final feature. Temporary editing fades,
selection highlights and task preview colors must not become permanent materials.

## Proposed contract

- New body and surface clones receive authored whole/per-face materials, including
  diffuse color, transparency, ambient/specular/emissive fields and shininess,
  plus applicable edge/point appearance. Respect the displayed finished Body and
  persistent occurrence overrides while excluding temporary display overrides.
- Copy at creation. The clone's later local appearance edits remain independent;
  recompute, reopening and geometry-task edits do not repeatedly overwrite them.
  Existing clones are not recolored automatically. Geometry remains associative.
- Preserve exact face correspondence/occurrence placement, source visibility and
  materials, component ownership, direct-child admission, identities, native Undo
  and persistence. No change to Extract, sketches, planes, curves or points.
- Integrate into the existing creation transaction after successful geometry
  evaluation, using existing/native material utilities. No unrelated UI, schema,
  selection or material-system redesign.
- After approval, verify actual task acceptance/Apply, multiple sources, body
  Through/Tip modes, face mapping under rotated placements, surfaces, imported
  children, persistent overrides, no temporary fade/highlight transfer, rollback,
  Undo/Redo, save/reopen and preservation of subsequent local appearance edits.

## Preview limits and evidence

Both sides execute the installed Clone code without modification. Comparison
geometry is copied to disposable native display objects and rendered with the
native viewer. Source/current panels use actual source/result materials. Candidate
styling sets **fixed fixture materials on display copies only**; it is not a generic
material-copy implementation and does not alter actual clones. This distinction
is labelled directly on the screenshots.

Native checks confirm source/result material mismatch, unchanged sources, one
Clone Undo entry, correct face counts and unchanged real clone/source state after
the display-only illustration. Candidate displayed material values match the
fixture source values. These establish the bug and visual target, not completed
functional acceptance. See each `result.json`.

Source and candidate fixture code, harness, screenshots and result data are
archived here. Private run profiles/fixtures are removed after hash verification;
companion worktrees remain for approval. Main source, installed app, owner settings,
shortcut and unrelated `project.previewfirst.json` remain untouched. Other pending
workflow previews are not approved or implemented by this request.
