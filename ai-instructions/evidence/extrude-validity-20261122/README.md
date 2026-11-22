# Approved Extrude target display and validity colors

`approval.json` records explicit chat approval of direct native screenshots.
The implementation supplements hidden selected targets without changing their History
flags; visible targets keep native picking. The shared evaluator carries its actual
constructed tool through final-operation failure, while invalid acceptance still
fails. Green/yellow Add and red/pink Subtract tools use an annotation layer so the
translucent selected target cannot tint the colors. New Solid and valid Result keep
their existing presentation; invalid Result falls back to the colored tool.

`build-regression.txt` records eight passing focused native cases. Coverage includes
actual History selection through a hidden Body, configured selection color/focus
opacity, eyes/Undo, all four tool colors and atomic invalid acceptance, invalid Result
fallback, no stale tool after clearing a profile, manual-update/Show-preview states,
target replacement/removal/New Solid switch, native face-reference picking on visible
targets, save/cancel/reopen visibility and material preservation, existing feature
editing, external-source ownership, and native evaluator error/tool boundaries.

The broad suite retains Extrude modeling/face profiles, sketch creation/dimensions,
History tabs, coordinate display, exit fitting, shared eyes, planes, Move and Rotate.
All 177 installed cases passed with zero failures/errors (`regression.json`/`.txt`).
`visual.FCMacro` uses actual History row clicks in four installed native tasks. It
captures the target field and the four validity states, accepts and saves valid Add/
Subtract, rejects invalid acceptance atomically, and saves hidden-target source flags
while invalid previews are active. `reopen.FCMacro` loads those four files in a fresh
process, verifies target flags/materials and valid result identity/recompute, and opens
the saved features' shared editor. No preview staging code is injected.
Both checks passed (`visual.json`, `reopen.json`); all five installed screenshots
were reviewed and match the approved target presentation and green/yellow/red/pink colors.

Runtime validation uses explicit isolated user/system/data paths, bounded processes
and the existing development app. Installation checks source/build/app hashes and
retains original rollback copies. The existing desktop shortcut is verified before
launch with isolated settings. Cleanup checks absolute path containment and rejects
reparse points; it retains rollback copies, the active profile and durable evidence.
