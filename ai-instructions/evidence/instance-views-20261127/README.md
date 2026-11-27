# Corrected Assembly instance views — November 27, 2026

Owner: “implement the corrected condensed and expanded instances views in the
assembly tree.” This approves the instance-view portion of native review
`5826d20f99b1`, fingerprint
`03fda706509a442b0c616aa334b6b8f154c2275a62a119f7f8e1a1eccd98bc68`.
Inspection confirmed a fresh capture and no scope violations; companion approval
state was not changed. Edit within assembly/Edit in isolation, single-part default
assembly and the Sketcher Symmetry proposal remain separate pending work.

Condensed groups show no disclosure arrow and remain folded during double-click,
keyboard/bulk expansion, refresh and exact native occurrence selection. Context
Expand instances and the global controls restore numbered original occurrences.
Real assembly branches retain arrows and folding. Existing group menu parity is
preserved, with unavailable grouped display actions disabled when editing a member
whose siblings are outside that edit context. No geometry or persistence schema changes.

## Validation

- Source s1: 25/26 passed; the new bulk-expansion check found that Qt completes
  its expansion state after emitting signals. The synchronous guard was supplemented
  with a queued guard; stale deleted items are safely ignored.
- Source s2: all 12 instance-view tests passed after that correction.
- Installed i1: 25/26 passed; one menu-trigger check did not expand a group after
  editing a member. Added the panel's diagnostic text to that assertion. No further
  production change was made for this non-reproduced failure.
- Installed i2 and i3: the focused menu check and the preceding-keyboard/menu
  sequence both passed (1 and 2 checks).
- Final installed i4: **26/26 passed**, covering instance views, navigation and
  active assembly choices. Logs preserve earlier failures as well as the final run.

Coverage includes per-parent/global grouping, arrow policies, right/plus/asterisk
keys, double-click, Qt expandAll, nested exact selection, original item identity,
full context-menu parity, grouped Copy/Move/display/Undo, explicit single-member
actions, singleton/rename/Undo transitions, imported labels, saved active assembly,
retained tab and real assembly expansion. Model IDs/placements/visibility/Edit/
active assembly and Undo remain unchanged by presentation switches. No native
rebuild was needed: the changes are in the existing Python panel modules.

## Installation

Installed `freecad_plus/panel.py`, `freecad_plus/assembly_ui.py` and
`TestInstanceDisplay.py` into the existing FreeCAD Plus app. SHA-256 hashes match
source; rollback copies remain in the build's `validation/instance-views27/rollback`.
Owner profile CFG files and the FreeCAD Plus 2.0.0 desktop shortcut hashes are
unchanged. Restart the app to load the corrected views.

`condensed.png` and `expanded.png` are real installed native task snapshots from
i4. Scripts and logs are archived here; tests use isolated synthetic documents and
profiles. The menu-trigger failure above was not reproduced in the final combined
run. No owner files were opened or modified.
