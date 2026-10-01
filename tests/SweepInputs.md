# Explicit Sweep inputs (F028)

Use Part > Sweep in the source-built FreeCAD Plus fork.

1. Add profile(s) to Sections in sweep order. The list order is the native Sections
   sequence. Tooltips include internal names to distinguish equal labels.
2. Click Sweep Path, select a whole edge/wire or connected edges from one object,
   then Done. Check the captured document, object and edge names.
3. Click a profile in the list or change global selection. The captured path must
   remain unchanged. To replace it, use Sweep Path and Done again; an invalid new
   selection clears the old choice and requires correction.
4. Review Create solid and Frenet. A closed circular section on a straight path
   can create a solid; an open line can create a sheet with Create solid off.
   Frenet/corrected orientation uses native rules. No twist preview is provided.
5. Try an open profile with solid output: failure must retain the task and leave
   no new Sweep/Undo entry. Turn Create solid off and retry. Stale/replaced inputs,
   disconnected paths and using one object as both path and section are refused.
6. Cancel even while selecting the path. No feature should remain, and ordinary
   model selection must work afterward. Finish other edit transactions before OK.
7. Create a valid Sweep, Undo/Redo, save and reopen. Change its path and recompute;
   the Sweep and a linked downstream consumer must update from the same inputs.

Full F028 remains open for broader orientation/scaling/guides, geometric twist
preview, section reversal, Boolean targets and unified command-family semantics.
This is a bounded native Part Sweep workflow; stop here and rotate pending owner
feedback rather than polishing further before testing.

## Recorded validation (2026-10-01)

Roadmap 13.2c/d is ready for owner testing. Both tasks preceded a successful
70-second PartGui build. The first grouped run retained eight passing Loft checks
and exposed Sweep source topology mutation; input copying with preserved element
maps fixed that demonstrated blocker in one 60-second corrective build. All eight
Sweep checks now pass, for 16 distinct accepted checks. Six captures were reviewed.
Installer acceptance and physical owner workflow testing remain pending.

Evidence: `D:\Temp\Office-PC\freecad-plus-sweep-inputs-20261001`.
Use `visual/Sweep-Sources.FCStd` to try the collector, `Associative-Sweep.FCStd`
for the created solid, `Edited-Sweep.FCStd` for the reopened path edit, and
`Surface-Sweep.FCStd` for open-profile surface output (all under `visual/`).
The automated procedure is `tests/TestSweepInputs.py`; reports, source/runtime
hashes and publication evidence are retained in `evidence.json` at the evidence root.
