import json
from pathlib import Path
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
dest=repo/'ai-instructions/evidence/pattern-memory-20261124'
def result(stage,name='result.json'):return json.loads((dest/stage/name).read_text())
before=result('baseline-circle20-gui');after=result('installed-circle20-gui')
mbefore=result('baseline-circle20-gui','process.json')['peakPrivateBytes']
mafter=result('installed-circle20-gui','process.json')['peakPrivateBytes']
installed=result('installed');build=result('build-regression')
readme=f'''# 20-by-20 circle pattern memory reduction — November 24, 2026

Starting source/install: `76ec9dd6dfb2dee0a9209305e6ebb9b50ac1e7d7`.
Owner reported “not enough memory available” for a 20-by-20 circle pattern and
confirmed it appeared after Apply/Done. This is a solver/backend correction with
no changed interface or workflow; no additional visual approval was required.

## Finding and correction

The isolated baseline completed rather than reproducing the exact allocation error,
but the actual circle task consumed **{mbefore/1e9:.3f} GB** peak private committed memory
and took **{before['seconds']:.3f} seconds**. The preview itself completed promptly;
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
[build-runtime suite](build-regression/result.json) passed **{build['tests']} checks**.
The [installed suite](installed/result.json) ran **{installed['tests']} checks** with
zero failures/errors and one upstream skip, including upstream Sketcher coverage
and the 400-circle creation/editing regression. The skip is identified in its log.

| Actual installed task | Before | After |
| --- | ---: | ---: |
| 20 × 20 circles, Apply | {before['seconds']:.3f} s | {after['seconds']:.3f} s |
| Peak process private committed memory | {mbefore/1e9:.3f} GB | {mafter/1e9:.3f} GB |

Memory reduction: **{(mbefore-mafter)/1e6:.0f} MB ({100*(mbefore-mafter)/mbefore:.1f}%)**.
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
'''
(dest/'README.md').write_text(readme,encoding='utf-8')
section=f'''## Large circle-pattern memory — installed

November 24, 2026. Owner reported an allocation error after applying a 20-by-20
circle grid. Sparse solver diagnosis now avoids dense Jacobian/factor copies and
reduces only needed dependency columns; factorization memory is reused sequentially.
The installed task completes in {after['seconds']:.2f} seconds versus {before['seconds']:.2f},
with peak private memory reduced from {mbefore/1e9:.2f} GB to {mafter/1e9:.2f} GB.
All spacing/Equal relationships, conflict checks, pitch edits, hiding and Undo remain.
The exact original allocation error did not reproduce in the isolated fixture;
these are verified reductions in memory pressure, not a universal OOM guarantee.
91 native tests and {build['tests']} build-runtime application checks pass; {installed['tests']} installed
cases have no failures/errors and one upstream skip. Saved-grid reopening and the
existing shortcut pass too. Restart the app.
See [measurements, implementation and limits](evidence/pattern-memory-20261124/README.md).

'''
for name in ('WORK_STATE.md','PROGRAMMING_SUMMARY.md'):
    path=repo/'ai-instructions'/name;first,rest=path.read_text(encoding='utf-8').split('\n',1)
    path.write_text(first+'\n\n'+section+rest.lstrip('\n'),encoding='utf-8')
path=repo/'ai-instructions/DEVELOPMENT_ROADMAP.md';first,rest=path.read_text(encoding='utf-8').split('\n',1)
roadmap='''## Large circle-pattern memory — November 24, 2026

- [x] Measure the reported 20-by-20 circle Apply path in an isolated task.
- [x] Avoid unnecessary dense allocations and overlapping sparse factorizations.
- [x] Preserve dependency, redundancy/conflict diagnosis and native constraints.
- [x] Add 400-circle chain/size/edit/Undo regression and native solver comparisons.
- [x] Build, install, verify memory/timing, saved-grid reopening and the existing shortcut.
  The exact reported OOM did not reproduce; see [measured reductions and limits](evidence/pattern-memory-20261124/README.md).

'''
path.write_text(first+'\n\n'+roadmap+rest.lstrip('\n'),encoding='utf-8')
