# Unified component Helix acceptance

REQ-014d/UI-003d apply the owner template to native AdditiveHelix/SubtractiveHelix.
Run `TestComponentHelix.py` with `RunComponentDocument.ps1`, an isolated fork
candidate, an external output directory and `FREECAD_PLUS_PROFILE_SOURCE=0`.
Tests verify runtime source hashes. The ninth case, `testNativeCommandRouting`,
requires the grouped PartDesignGui build; the other eight use the existing native engine.

Coverage includes all four parameter modes, dependent dimensions, handedness and
axial reversal, conical growth and flat spirals; New Body/Add/Subtract/Common and
nonmutating previews; mode-edit IDs/downstream consumers, undo/redo and persistence;
whole/selected profiles, construction-axis edits and save/reopen, origin/edge/datum
axes and placed/rotated profile preview parity; invalid input/rollback, cycles and
expression protection; four-section defaults, preselection, mode conversion,
History editing, preview colors, None/Result, failed-OK recovery and Cancel.

Native sweep approximation can differ slightly between an explicit reference-line
preview and a sketch construction axis. The roughly 31.4 cubic mm construction
fixture allows five decimal places for volume comparison; positioned-result
comparisons additionally require less than 1e-5 cubic mm difference. Preserve native
Refine fallback warnings in logs; a valid result does not establish successful
splitter removal. Startup stylesheet warnings remain separately recorded.

Shared regressions: Loft's `testModeEditIdentityDownstreamUndoAndCadprt`,
`testSelectedCurvesRecomputeAndReorder`, `testTaskPreselectionOrderPreviewAndHistory`;
Pipe's `testModeEditIdentityUndoAndCadprt`,
`testMultisectionSubsetAssociationAndUnsupportedPoint`, `testTaskPreselectionHistoryAndCollectors`;
Revolve's `testTaskSectionsPreviewAndEdit`, `testPreviewColorsVisibilityAndCancel`;
ribbon's `testCompactPrimaryAndSecondaryGrid`, `testExactOwnerDesignModelingLayout`.
Use per-file filters separately. After the grouped native build run full Helix,
Pipe and Loft suites including native aliases, then the owner shortcut delivery gate.

Owner acceptance: start empty or with a selected profile, collect closed curves,
switch the four parameter modes and axis choices, change handedness separately
from axial direction, and exercise Add/Subtract/Common against explicit targets.
Compare Overlay/Result, cancel, reopen from History, change upstream geometry
and save/reopen. Inspect normal and expanded controls using the task's scroll area.
Physical pointer/high-DPI checks remain separate from scripted Qt test captures.
The roadmap and WORK_STATE own native build, owner delivery and evidence status.
