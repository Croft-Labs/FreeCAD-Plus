# Native selected-curves list preview — awaiting approval

Owner request: at least five selected-curve lines, scrollable or expandable so every
selection can be seen. Proposed treatment enlarges the existing Extrude Profile list
and uses its native vertical scrollbar. No additional expansion control is needed.

Native staging runs the installed task at production commit
db46249adeb74ea7e93f20243a12591b1df33bd4 with an actual eight-edge sketch. The isolated
candidate changes only list height and scrolling. Baseline shows two complete rows;
candidate shows six at the current font (at least five), and scrolling reaches Edge8.
The geometric preview remains valid. Both screenshots were inspected. This is native
layout staging, not installed functionality. Only documentation is being published.

Companion session: c57a3fe6d5a1. Focused snapshot baseline:
73e0359e83b776a2bd6644abab7a96677b0492bb. Allowed file: preview_state.py.
Fingerprint: 8f415fd72188ca51606e7465a23b6181f0bf9bae0b97f31cd351a5447ca70b10.
Capture: baseline-84652b2a.png / candidate-8b2658bc.png. Fresh, no scope violations.
Tool approval state was not changed. The fixture and renderer are under workspace
extrude-selection-preview; native runs use isolated profiles. Production unrelated
project.previewfirst.json is preserved.

After chat approval, implement the matching list sizing in Extrude creation/editing,
retaining at least five complete rows with native font/DPI changes and any horizontal
scrollbar. Check short/long/many selections and reachability through the task scroll
area. Preserve Remove/Clear/Whole sketch, geometry, preview, selection and Undo.
Install with rollback, validate the installed layout, restart the existing shortcut
with isolated settings, update status and commit/push under standing authorization.
