# Feature selection gestures preview - November 23, 2026

Owner requested click to select/add and Shift-click to deselect in all curve, edge
and other feature selectors. Proposed common contract:

- Plain click adds an eligible input once; repeat clicks retain it.
- Shift-click removes matching inputs; absent inputs stay absent.
- Connected/tangent expansion applies the same intent to the resulting chain.
- Single-reference inputs keep replacement semantics; Shift-click clears a match.
- Preserve eligibility, predecessor ordering, conflicting plane replacement,
  ordered Loft sections, existing Remove/Delete/Clear and collection focus rules.

Scope includes Extrude/Revolve, Loft, Thicken, Shell, Fillet/Radius, Chamfer, Draft,
plane/sketch placement and comparable feature collectors. Both view and History
picks must respect the rule where they feed those collectors. Preserve unrelated
selection outside feature tasks, visibility eyes, native geometry and saved IDs.
Future collectors must follow the same interaction.

[Baseline](baseline.png) and [proposal](proposed.png) show the actual Extrude list
widget with simulated picking. The baseline invokes the existing selection handler;
the candidate only updates list state. Three steps produce baseline counts 2/1/0
and proposed counts 2/2/1. This is UI-only evidence, not working gesture integration
or proof of all workflows. No production code or installed payload changed.

Companion session 19c92fb00c8b; isolated adapter baseline
8ea1dc5fd9702bc7a44314bf620e2223ab41c5e9; preview fingerprint
e07195b4afa79c97923f14b75bd7bb5b8b7d6734db3e35520a17a08e33c0e10a.
Scope violations empty; preview valid. Only selection_ui.py changed in candidate.
Owner approved with "approved"; tool approval state was not modified.
See [implementation and acceptance](../feature-pick-20261123/README.md).

Implementation should retain modifier intent across delayed curve expansion and
native consuming-picker notifications, with actual viewport and History tests,
duplicate/no-op checks, empty-list recovery, and the existing freeze regression.
Use isolated validation profiles; retain the unrelated project.previewfirst.json.
