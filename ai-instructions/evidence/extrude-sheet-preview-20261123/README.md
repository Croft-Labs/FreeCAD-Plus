# Extrude Solid/Sheet preview — November 23, 2026

Status: native UI proposal awaiting approval; production source and installation
are unchanged. Owner requested sheet extrusion so that an open line can produce
a single sheet, then clarified the exact layout and operation restriction:

- Solid and Sheet on the left; Solid selected by default.
- New, Add and Subtract on the right (display New instead of New Solid).
- Sheet automatically selects New and disables the entire operation group,
  including New. Sheet has no Add/Subtract operation.
- Returning to Solid re-enables the operations with New still selected.

Direct screenshots: [Solid default](solid-operation.png),
[Sheet with New locked](sheet-operation.png), [task context](sheet-task.png),
[native line-to-sheet illustration](sheet-viewport.png), [before](before.png).

## What the prototype verifies

It adds the independent radio group to the actual installed native Extrude task
in an isolated temporary document. Default Solid, switching from Add to Sheet,
locked New, re-enabling Solid operations and choosing Subtract pass native Qt
checks. The example extrudes a 30 mm native line by 8 mm: one valid face,
240 mm² area, zero solids. This is fixture geometry, not the implemented Extrude
evaluator. The separate native offscreen render illustrates that result; the
task's OK remains disabled so no unimplemented operation can be committed.
The candidate also replaces Tool volume with Extrusion preview for Sheet and
shows open-curve guidance. Other task controls retain their existing layout.

## Implementation scope after approval

Add a persisted output type and default existing saved features to Solid. Keep
legacy operation identifiers compatible while the new UI displays New. Sheet
admits open sketch curves/edges and generates uncapped faces/sheets; one straight
line yields one face, not a thin solid. Closed-curve sheet output should likewise
remain uncapped. Solid keeps its existing closed-region/planar-face validation.

Sheet must force New at both UI and evaluator boundaries and remove any target
reference; the right-side options stay disabled until returning to Solid. Preserve
shared creation/edit, saved profile references, strict sequential history, Undo/
Redo, cancellation, task visibility and selected-profile presentation. Use an
appropriate native result representation for a sheet without introducing any
user-facing Body creation. Preserve existing solid identities and saved behavior.
Validate extent/direction/offset/taper using the appropriate native sheet kernel;
do not silently reinterpret unsupported end conditions or fabricate volume results.
Revolve inherits Extrude task code, so scope the new output choice to Extrude
unless the owner separately requests sheet Revolve.

Acceptance needs open line, connected/open curves, closed curves without caps,
selection/reselection and mode switching, invalid/degenerate extrusions, direction/
extent controls, save/reopen/edit with retained identities, dependency handling,
undo/redo and existing Extrude/Revolve/visibility regressions. Preview geometry
alone does not establish those production behaviors.

## Provenance

Companion f0abee35bf1b uses the minimal clean native-task adapter snapshot
a61c33d6cda3148378a80ca065b9115861956520, with production at e17c147ccd.
Exact allowlist: extrude_output.py. The session was created before the owner
clarified Sheet naming, left/right placement and New-only output; the captured
candidate and this record reflect that later clarification.
Fingerprint 2fc032542f08973bb961114bd6a11041866309b71fcbf08d01ccf28f826b368c;
capture is fresh, no scope violations, approval false. No approval state changed.
The renderer uses isolated settings and synthetic documents, no owner data.
Native task screenshots include the parent backdrop and scroll to the operation
group. Offscreen rendering of an overlay was blank, so the sheet illustration
uses a separate synthetic native Part feature containing the same native shape.
Source adapters and result records are archived here; generated fixtures are
removed after archival. Unrelated project.previewfirst.json is preserved.
