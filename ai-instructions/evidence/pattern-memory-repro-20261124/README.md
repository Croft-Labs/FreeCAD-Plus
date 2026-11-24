# Persistent pattern allocation failure — November 24, 2026

**Superseded by the [saved-file reproduction and correction](../pattern-label-allocation-20261124/README.md).**
The owner subsequently supplied the source sketch. The GUI probes below had a
harness input bug: they set text but did not commit the quantity field, leaving
20 mm pitches in place. They do not verify 0.100-inch spacing. The corrected test
asserts both physical values and unit strings and reproduces the original error.
Retain the original results as historical evidence with this limitation.

**Unresolved.** The owner confirmed the error persists after restarting the
updated app. Their sketch was unsaved. They were asked to save the source sketch
before applying the pattern and provide its local path. No path has arrived yet.
Starting source/install: 94fcfa4c7f908555e33097f1878870620307d6f0.

The screenshots show a 20-by-20 linear circle grid, X/Y axes, 0.100 in pitches,
Create spacing constraints and Hide spacing chain checked, and a source circle
with a displayed 0.65 mm diameter and 0.050 in vertical construction-line length.
The exact center X coordinate and full constraint definitions cannot be recovered
from screenshots. The reconstruction uses X=1.1 mm, Y=1.27 mm, a 0.65 mm diameter,
two construction lines, center coincidences, horizontal/vertical relationships,
endpoints on the axes and a 1.27 mm vertical line length.

## Reproduction results

All four isolated native task probes succeeded without reproducing the error:

| Fixture | Apply/close time | Peak private bytes |
| --- | ---: | ---: |
| Clean profile, construction lines | 17.75 s | 1,232,904,192 |
| Copied owner preferences | 17.40 s | 1,615,503,360 |
| Plus Component, copied preferences | 17.47 s | 1,621,491,712 |
| Unsaved Plus Component, copied preferences | 17.03 s | 1,616,826,368 |

Each produced 801 geometry, 2,003 constraints, and one remaining degree of freedom.
The probes run the actual task with hidden chains and inch input. Peak memory is
sampled every 200 ms. These results do not establish that the owner's sketch is
fixed or equivalent to this reconstructed fixture. Original owner preferences and
launch log were only read/copied; private copies and document snapshots are not
included in this evidence. The desktop launcher target was verified unchanged.

## Installed diagnostic change

The task previously retained only str(error) in its warning. It now also sends the
full Python traceback (including chained rollback errors) to FreeCAD's normal
error log. This exposes the native API call site on the next recurrence. Logging
is guarded so failure to log cannot prevent the existing task recovery. Task
layout, warning text, solver, geometry, constraints and options are unchanged.
This is **diagnostic logging, not another memory fix**.

The regression injects MemoryError inside spacing-chain creation after copies
have been added. It verifies rollback, retained inputs and count, the original
warning, a traceback identifying _spacing_chains, and a successful retry. All
seven installed TestPatternTask tests pass; the new test also passes through the
existing desktop shortcut. Two installed Python files match install-manifest.json;
their previous versions are backed up. No native rebuild was required.

Restart FreeCAD Plus to load the diagnostic handler. The existing launcher writes
the full trace to `_temp builds/FreeCAD-Plus/logs/owner-launch.log`. Preserve that
log before another launch overwrites it. Next work: obtain the exact saved source
sketch or the recurrence trace, reproduce the actual failure, then implement and
verify a targeted fix. Do not claim resolution based on these successful fixtures.

The separate Elements-list single Pattern-row preview remains unapproved and
unimplemented (companion 8aa0a38df7a0); its local handoff is
`../pattern-elements-preview/README.md` relative to the repository root.
