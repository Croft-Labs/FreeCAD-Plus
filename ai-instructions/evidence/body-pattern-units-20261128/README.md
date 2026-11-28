# Body-pattern inch entry — fixed and installed November 28, 2026

The owner reported that the existing body-pattern workflows rejected inches.
The installed baseline reproduced it with real Qt keyboard input: typing `0.5 in`
left **0.5 mm**, not 12.7 mm. Its fields were plain QDoubleSpinBox controls with a
fixed mm suffix. This repairs the existing unit-entry workflow; no new controls,
layout, selection steps, defaults, angle behavior or geometry algorithms were added.

- [Reproduced baseline](before.png)
- [Installed inch entry](installed-inches.png)

## Correction

Length fields now reuse the established `quantity_fields.QuantityNumber`. It accepts
explicit lengths, retains native mm precision, displays the entered unit, defers
typed values until commit, and reports explicit spin changes through `committed`.
This covers Linear spacing/overall length, Mirror offset, Polar axis-origin XYZ,
and those steps inside Multi-transform. Occurrence counts and angle fields retain
their existing controls. Apply explicitly validates/commits pending lengths.

Each saved TransformSteps entry optionally includes a `units` map for its length
fields. Geometry values remain mm. Unit presentation follows a step when reordered,
survives save/reopen and in-place editing, and resets to existing mm defaults after
Apply. Recipes without that map continue to load as mm; there is no schema migration.

## Verification

- Nine native source checks passed; ten installed checks passed, including actual
  Mirror/Linear/Polar/Multi-transform toolbar commands.
- Real typed `0.5 in` gives 12.7 mm; `0.03125 in` retains exactly 0.79375 mm;
  `2.54 cm` gives 25.4 mm; negative mirror/origin coordinates are accepted.
- Verified body/sheet spacing and total length against result bounding boxes,
  Apply/reset, one Undo step, redo, save/reopen, Cancel and in-place edit.
- Verified Multi-transform reordering and restored units, incompatible pending
  input rejection, and old recipes without presentation metadata.
- Existing native build updated only the FreeCADPlusScripts target. Three Python
  payloads were installed with rollback copies. All source/build/app hashes match.
- Owner settings and desktop-shortcut hashes are unchanged. Tests used generated
  documents and isolated profiles, which were removed after archiving evidence.

`TestBodyPatternUnits` owns the five new regressions. Existing TestShapeTransforms
and the native button-routing test supply the remaining checks. No owner file was
opened or modified; no native binaries were replaced.
