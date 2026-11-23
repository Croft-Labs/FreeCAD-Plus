# Strict sequential History — native presentation preview

Owner request: the sketch used by Extrude or Revolve stays before that feature;
reordering it after a consumer is forbidden. Modeling is strictly sequential.

The installed History projection flattens each backend Body before moving to the
next member of definition.Group. An Add feature appended to an older Body therefore
appears before its newer component-owned sketch. This preview uses actual saved-in-
memory Extrude, Revolve Add and Extrude Add features to reproduce the problem.
All three native result shapes are valid. No owner documents or settings are used.

- [Current native History](baseline.png): both later sketches are below their consumers.
- [Proposed native display](candidate.png): each sketch precedes its operation.
- [Baseline record](baseline.json) and [candidate record](candidate.json): displayed
  sequence, unchanged native ownership order and unchanged geometry/visibility.

The candidate contains only a presentation sort by creation ID. This is a visual
stand-in for the intended sequence, not dependency validation or persistent ordering.
Production source and installed application remain unchanged. The installed app's
existing isolated window remains open; preview processes closed their own fixtures.

Companion session: f56b79f8df59. Allowed file: panel.py.
Source snapshot baseline: 75187c52041800e8db06d4f2ec322be9af25bdae.
Production baseline: 193cc907acdb3db09c644489bc3d67e516274d18.
Fingerprint: 3fe344aa83245ac2eced333283b2f48c059239923e9719d9be8ae1961aeea944.
Captures: baseline-846d6e5e.png / candidate-02aa7c77.png.
Capture is fresh, with no scope violations. Tool approval state was not modified.
Renderer and native fixture: workspace sequential-history-preview/render.py and scene.FCMacro.

After chat approval: implement a dependency-aware component-wide sequence independent
of backend Body membership. Keep profiles, targets and applicable axis/limit/reference
inputs before consumers; prevent forward/cyclic inputs during edits, and preserve
dependency constraints for any future ordering action. Do not implement the full
unconfirmed historical drag/suppression proposals by inference. Existing misprojected
documents must display correctly without changing geometry, identity or ownership.
Verify create/edit, indirect dependencies, legacy/native chains, Undo/Redo and
save/reopen, then install with rollback, restart through the existing shortcut using
isolated settings, commit/push and remote-verify under standing authorization.
