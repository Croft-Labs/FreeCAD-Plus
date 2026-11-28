# Intersection curve — unified selection revision, preview pending

Owner clarification November 27: remove the Pick dropdown. One intersection
workflow accepts curves from previous sketches, solid edges/faces, surfaces and
other eligible geometry, limited to objects native to the component and earlier
in its History. This supersedes Body/Surface/Curve modes and cross-component
admission language in the earlier preview `4bf58e04f7e2`.

**UI-only revision. No production implementation or installation.**
New session `87ac16544d40`; allowed file `intersection_ui.py`.
Fingerprint `cb7f6976fc19abfc3e0f38cdc9512b1b309859f749d9cb941e0e98343f9c44db`.
Inspected fresh, no violations, approval false. Original project source remains
`3c693ff49a`. The baseline is the previous proposed Qt form, not the installed tool.

[Previous proposal](baseline/panel.png) · [Revised proposal](candidate/panel.png)
· [Ineligible-source feedback](candidate/ineligible-source.png)

## Updated selection contract

- One mixed source collector, no Pick dropdown or replacement type-mode control.
  The workflow is not face-only or edge-only, so do not force the selection toolbar
  into a single surface/curve domain. Apply a fixed eligibility gate.
- Viewport selection keeps the exact picked edge/face. Do not silently promote it
  to an entire Body. History selection can supply a whole earlier result or sketch;
  prior sketch curves, solid edges, solid faces, sheets and whole solids can coexist.
- Ownership must resolve to the currently edited component; the producer must
  occur strictly before the active sketch in that component's History sequence.
  Use actual History/dependency ordering, not labels or file timestamps.
- Reject the current sketch, later features, cyclic inputs, and raw geometry owned
  by child/other components or another file. A clone already owned by this component
  and earlier in History is local geometry; do not traverse through its source to
  admit unowned external topology. A whole Body pick must resolve an eligible
  finished result, never use a later Tip merely because the container is older.
- Check admission while collecting, before commit, and when reopening/recomputing
  saved references. Reordering, deletion, source replacement or retargeting must
  produce actionable feedback rather than bypass ownership/history constraints.
- Click adds once; Shift-click removes existing references only; Delete/Remove/Clear
  work on list entries. Keep native topology identities and deduplicate references.

## Preserved intersection behavior

Use the actual sketch plane. Solids/faces/sheets produce section curves; crossing
edges/sketch curves produce all crossing points. Results remain linked and update
with their sources and sketch support. Whole-source selection must track newly
intersecting topology, not only the faces that intersected when first created.

Keep preview, prominent errors, bottom Done/Apply/Cancel and successful Apply/reset.
Failure retains inputs. Done closes this tool, not the outer sketch edit. Cancel
discards unapplied input and retains earlier Apply results/native Undo entries.
Preserve prior coplanar-curve and nonintersecting-source feedback requirements.

The prior native API investigation still applies: `addExternal(..., True, True)`
handles basic sections/crossing points, but its initial whole-body face expansion
left stale geometry after sketch-plane rotation. That backend limitation remains
unfixed. The existing `document.history` / `require_predecessors` helpers provide
ordering infrastructure, but exact ownership and subshape admission must still be
implemented and tested. Do not claim that this UI enforces native eligibility yet.

## Verification and scope

Nine UI check groups pass: mixed fixture rows, duplicates/Shift, Apply reset,
preserved outer sketch editing, unchanged sketch geometry/references/Undo, no
dropdown, ineligible-source error retaining inputs/blocking commit, error recovery,
and Delete removal. Candidate rows and error eligibility are simulated; native
picking, admission, calculation, linking, persistence and Undo integration are not
implemented. The source/plane numerical probes are retained in the earlier preview;
they were not rerun as evidence for this UI-only revision.

Only the candidate UI file and task documentation changed. No approval records,
installed app, owner files/settings or unrelated preview configuration changed.
After approval, implement the linked workflow plus the whole-source update fix;
test local earlier sketches/edges/faces/sheets/bodies, later/self/foreign rejection,
historical body results, geometry/plane edits, save/reopen and Undo/Redo.
Private run data is removed after archive verification; review worktrees remain.
