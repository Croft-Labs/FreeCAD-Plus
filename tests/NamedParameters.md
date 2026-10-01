# Named parameter workflow: owner testing

Use the source-built FreeCAD Plus application. The separately installed FreeCAD
and existing release installers do not contain this new command. Development
launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The current example is at
`D:\Temp\Office-PC\freecad-plus-parameter-command-20260930\visual-final\Named-parameters-enclosure.FCStd`.

## Try the supplied enclosure

Open `Named-parameters-enclosure.FCStd` from the latest phase 10.8 evidence folder
linked in the development roadmap. Switch to **Part**, select **Enclosure** in the
tree, and choose **Part > Named parameters...**.

1. Select **Width**, enter `76.2 mm` in Expression, then **Apply expression**.
   The enclosure width becomes 76.2 mm and its lid follows.
2. Set **LidClearance** to `1 mm` and **HoleSpacing** to `40 mm`. Inspect the lid
   and mounting-hole spacing. Changes apply only after clicking Apply.
3. Select Width, change Name to `EnclosureWidth`, and click **Rename**. The model
   should still update. Change Display unit to **in**: the value reads 3 inches
   while the model and stored expression keep their physical dimensions.
4. Try `30 deg` as that length's expression. The editor should explain the unit
   mismatch, retain your attempted text and preserve the last valid geometry.
   Correct it to `80 mm` and apply.
5. Close, use Undo/Redo, then save and reopen. Select the Part or **Enclosure
   dimensions** and reopen Named parameters. Previously applied edits persist;
   unapplied text is discarded on Close.

## Create parameters in your own model

Use the standard **Create part** container command (App::Part), select that Part,
and choose **Part > Named parameters...**. An empty parameter set is created once.
Under New name/type/expression/description, enter `Width`, Length, `25 mm` and a
useful description, then click **Create parameter**. Angles require units such as
`30 deg`. Select **Copy reference** to copy `Parameters.Width` (the actual internal
object name can have a numeric suffix). In a compatible feature property's native
expression editor, paste that reference without a spreadsheet-style `=` prefix.
Apply a new parameter value and inspect the dependent feature.

The command needs a Part definition or one of its marked parameter sets selected;
a Part Design Body or assembly occurrence is not resolved automatically. If a Part
has multiple sets, select the desired set explicitly. Closing the editor preserves
the created set; Undo of its creation is separate. Finish another active edit before
opening this command. Refresh reloads external changes and discards draft text.

## Scope and feedback

This pilot covers length/angle creation, descriptions at creation, expressions,
rename, display units and same-document references. Where-used navigation,
publication/configuration scope, editing existing descriptions and broader types
remain pending. Physical keyboard, high-DPI and translated layouts await owner
acceptance. Report whether the entry point, field order, Apply/Close behavior and
reference-copy workflow fit how you model before further UI refinement.

Automated checks: `TestNamedParameterCommand`, `TestParameterEditor` and
`TestPartHistoryCapabilities` use the source-built GUI with the checkout's `tests`
on `sys.path`. They exercise actual command/menu entry, consumer geometry,
transaction recovery and save/reopen. The old prototype imports forward to the
installed implementation; they do not maintain a second parameter editor.
