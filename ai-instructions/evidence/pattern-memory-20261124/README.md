# 20-by-20 circle pattern memory reduction — November 24, 2026

Starting source/install: `76ec9dd6dfb2dee0a9209305e6ebb9b50ac1e7d7`.
Owner reported “not enough memory available” for a 20-by-20 circle pattern and
confirmed it appeared after Apply/Done. This is a solver/backend correction with
no changed interface or workflow; no additional visual approval was required.

## Finding and correction

The isolated baseline completed rather than reproducing the exact allocation error,
but the actual circle task consumed **1.538 GB** peak private committed memory
and took **32.779 seconds**. The preview itself completed promptly;
the expensive path was constraint diagnosis during Apply. These are process-wide
measurements in isolated profiles, not claims about the owner's unsupplied document.

The sparse solver previously assembled a full dense Jacobian, copied it into an
asynchronous task, converted it back to sparse, and materialized dense QR factors.
The parameter diagnosis reduced all of R even when only two free-parameter columns
were needed. The two sparse decompositions could retain large factors concurrently.

Sparse diagnosis now builds only the nonzero derivatives of active driving
constraints, with the same parameter/constraint mapping and tag multiplicity.
Shared parameter pointers are deduplicated before grad(), which already includes
their combined derivative. Dense diagnosis remains available for small sketches.
The dense worker receives read-only references, and worker exceptions propagate.

Parameter dependencies use one sparse triangular solve per free column, preserving
the original unnormalized 1e-10 comparison threshold. Eigen's unsorted R is sorted
through row-major storage before diagonal lookup. The parameter factor is released
before allocating the constraint factor. The constraint side materializes dense R
only when actual redundancy/conflict analysis needs it; rank checks and conflict
resolution are retained. Repeated diagnosis clears prior dependency groups.
No geometry, spacing helper, Equal relationship, pitch driver or solver check is
removed. There is no artificial increase to pattern limits or memory-error masking.

## Verification and delivery

All **91 native tests** pass, including new dense/sparse dependency equivalence,
driven/negative-tag exclusion, repeated diagnosis, shared parameters, zero rank,
and both compatible redundancy and genuine conflicts. The full application
[build-runtime suite](build-regression/result.json) passed **94 checks**.
The [installed suite](installed/result.json) ran **75 checks** with
zero failures/errors and one upstream skip, including upstream Sketcher coverage
and the 400-circle creation/editing regression. The skip is identified in its log.

| Actual installed task | Before | After |
| --- | ---: | ---: |
| 20 × 20 circles, Apply | 32.779 s | 17.429 s |
| Peak process private committed memory | 1.538 GB | 1.214 GB |

Memory reduction: **324 MB (21.1%)**.
Private committed memory is sampled every 200 ms; shorter peaks may be missed.
The [free-radius circle task](installed-free-circle20/result.json) also passes.
Timings and memory are local measurements; other documents and available memory
can differ. The exact original out-of-memory failure was not reproduced, so this
does not claim that every possible allocation failure has been eliminated.

The 400-circle test retains 799 geometry elements, 399 spacing lines, 1,996
constraints, 399 Equal copy radii, 397 Equal spacing lengths, 399 parallel relations,
798 coincident relations and two pitch drivers. It edits diameter and both pitches,
checks all centers and chain endpoints, preserves source freedom, toggles hiding,
and verifies Undo/Redo. [Fresh-process acceptance](fresh-reopen/result.json) reopens
the saved grid, edits it to 420 instances, then saves/reopens hidden chains and
Equal sizes. [Three existing-shortcut checks](shortcut/result.json) pass.

The clean before/after task probes exit normally. Early exploratory probes had a
completion-log naming collision; the retained baseline was rerun with that fixed.
An exploratory 20-by-20 fixed-line run exceeded its 150-second deadline before the
correction. That is not represented as a circle failure or a repaired line benchmark.

Three installed files match [the SHA-256 manifest](install-manifest.json), with
original files retained for rollback. The existing desktop shortcut still targets
`Launch FreeCAD Plus.bat` in the same build root. Restart FreeCAD Plus to load the
native solver. The unrelated `project.previewfirst.json` remains untouched.
