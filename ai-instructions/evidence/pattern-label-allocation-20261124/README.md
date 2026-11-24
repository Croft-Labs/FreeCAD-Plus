# Dense pattern constraint-label allocation correction — November 24, 2026

Starting source/install: d66eb0b6ade8122e9292ae44ee8bcbe0b494880b.
The owner supplied the saved source sketch after the error persisted following
restart. Testing uses copies; the desktop original is preserved byte-for-byte.
The source file, private preferences and desktop screenshots are not committed.

## Reproduced failure and earlier test limitation

The source contains a 0.65 mm diameter circle centered at (1.27, 1.27), two
construction lines from its center to the axes, an Equal relationship between
those lines and a 1.27 mm vertical dimension. It is fully constrained.
The failing pattern is 20 by 20, X/Y axes, 0.100 in pitch in both directions,
with spacing constraints and hidden spacing chains enabled.

The [baseline reproduction](exact-inches-owner/result.json) now reproduces the
same MemoryError at _ConstraintBatch._add_optional / sketch.solve(). The trace
and asserted options are in phases.jsonl. Camera height is 100 mm so intermediate
constraint labels merge densely; peak private bytes are 1,412,730,880.

The earlier screenshot reconstruction and first saved-file probes had a harness
bug: setting lineEdit text and emitting editingFinished did not commit the
QuantityNumber value. Those GUI probes actually used 20 mm pitches, not 0.100 in.
They cannot establish success for the reported dense pattern. The corrected
harness uses keyboard input, commits the field and asserts **value=2.54 mm and
unit=in** for both directions before Apply. The earlier solver memory reduction
remains valid for its documented 20 mm benchmark, but did not fix this failure.
The earlier [investigation record](../pattern-memory-repro-20261124/README.md)
is annotated with this limitation.

## Correction

solve() also redraws the sketch after calculating geometry. During pattern
creation, generated constraints previously remained individually visible until
the final PatternGroup assignment. Dense clusters merge hundreds of labels into
very wide raster images. The Coin image conversion uses signed-short dimensions;
oversized intermediate labels can cause the observed allocation failure.

Generated constraints are now hidden immediately after each batched insertion
and before solving, including the scalar angular-chain path. Final grouping then
sets their intended visibility using the existing single Pattern presentation.
The default shown-chain case remains shown; Hide spacing chain still hides its
geometry and all grouped constraint graphics. Original source constraints are
not changed. No solver equations, Equal relationships, driving lengths, native
geometry, group membership or preview behavior are removed. This is an internal
construction-order correction; final UI and workflows are unchanged.

## Verification and delivery

The exact failing file passes with the correction and verified inch values,
with hidden chains and with shown chains. Source checks took 17.24 and 18.66
seconds respectively, including task completion. The final installed exact-file
Apply took 16.86 seconds (18.33 seconds including capture/save/task completion),
with peak private memory of 1,349,287,936 bytes. The [installed suite](installed/result.json)
passes all 96 tests without failures, errors or skips in 240.96 seconds.
The [fresh-process check](fresh-reopen/result.json) passes at 420 instances with
419 helpers after editing and reopening. The [existing shortcut](shortcut/result.json)
passes its native Pattern editor/unit test. The original file's hash is unchanged;
see original-preserved.json. No native C++ tests were rerun for this Python-only fix.

The new native GUI regression recreates the source relationships, uses the dense
camera scale and explicitly verifies both entered quantities. It checks 400
circles, 399 spacing helpers, 399 Equal copy radii, 2,004 total constraints and
zero remaining DoF; edits the diameter and both pitches and verifies all circle
centers/radii and coincident chain endpoints; toggles group visibility and checks
one Pattern list row; and verifies Undo/Redo. Fresh-process acceptance opens the
saved hidden 400-circle pattern, preserves inch units, edits to 420 instances,
then saves/reopens again.

Two Python files are installed with backups and verified SHA-256 hashes in
install-manifest.json. No native DLL changes or rebuild were needed. The existing
desktop shortcut is retained. Restart FreeCAD Plus to load the updated Python
pattern service. The Elements-list proposal remains separately pending approval;
this correction does not change Elements rows.
