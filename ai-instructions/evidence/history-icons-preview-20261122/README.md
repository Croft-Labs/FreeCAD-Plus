# Native History coordinate icons/default collapse — awaiting approval

The owner's requested presentation is implemented only in an isolated candidate
panel.py. Axes and Planes copy the native icon of their first child. Fresh Coordinate
System rows and descendants start collapsed; retained rows preserve manual expansion.
Far-left eyes, source visibility, labels and other tabs are unchanged.

Direct native screenshots: default.png, groups.png after opening only Coordinate
System, and children.png after manually opening the groups for icon comparison.
result.json confirms default expansion false for all three groups, matching group/
child icon pixels, preserved manual expansion on refresh and unchanged native flags.
Baseline checks confirm the previous expanded defaults and folder/child mismatch.

Companion session: 94bcfb75e36d. Exact allowed file: panel.py.
Focused source baseline: 5d53ace101ba660340132e27ce411b8eab142a5b.
Production baseline: 702e80970c3a6863328908702e36f343264709aa.
Fingerprint: 5f9b3e1eeb327600b8ef079fede79f38fa33af8c3e76d0955590b3631cd3c89f.
Capture: baseline-f0f6f586.png / candidate-27f4a6cc.png. Fresh, no scope violations.
Tool approval state was not changed. Fixture/renderer: workspace history-icons-preview.
The real native panel module is loaded from each worktree into a separate isolated
FreeCAD process; screenshots are direct dock captures, not an interactive simulation.
The owner profile and installed source are untouched.

After approval, apply the exact small panel diff, verify initial/repeated History
population and preserved manual expansion/eyes, build/install with rollback and verify
the installed panel. Restart through the existing shortcut with an isolated profile,
update status, commit/push and remote-verify under standing authorization.
