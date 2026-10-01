# Sheet thickening: owner workflow (F067)

This bounded delivery uses the existing **Part > 3D Offset** command
(`Part_Offset`) and native `Part::Offset` feature. Select one whole face/shell
object, use Skin mode and enable **Fill between source and offset**.

1. Enter a **Signed distance**. Positive follows the sheet normals; negative
   uses the opposite side. Its absolute value is the entire one-sided thickness.
2. Use **Reverse side** to negate a numeric distance. An expression-driven
   distance keeps its formula; change the formula to reverse it.
3. Check the result message. A filled single sheet must produce a valid closed
   solid. Turning Fill off produces an offset sheet, which is identified separately.
   With Update view disabled, changed values are pending until recomputed.
4. Press OK to commit the separate associative feature. Edit it by double-clicking
   its tree item. The source link and native Value/Fill properties are retained.
5. If the offset fails, correct the distance/side or Cancel. A failed OK keeps the
   task open. Displayed cached geometry after failure is not a current result.
   Cancel restores the committed feature or removes an uncommitted new feature.

Use a 10 by 8 mm planar sheet and 2 mm thickness: both signs produce 160 mm^3,
on opposite sides. Reversing the sheet orientation reverses the positive side.
For the lateral sheet of a radius-5, height-10 cylinder, +1 mm produces 110*pi
mm^3 and -1 mm produces 90*pi mm^3. An inward -6 mm offset must fail without
changing the source; correct to -1 mm and commit. Check Undo/Redo, save/reopen,
then change the source dimensions and verify the offset and downstream cut update.

`TestSheetThickening.py` exercises those native geometry and task paths, expression
preservation, deferred preview, failed create/edit acceptance, Cancel and the
inherited 2D task controls. Run in the source-built fork with `tests` on sys.path:

```python
import unittest, TestSheetThickening
unittest.TextTestRunner(verbosity=2).run(
    unittest.defaultTestLoader.loadTestsFromModule(TestSheetThickening))
```

Build/runtime/capture results are recorded under roadmap 13.1c/d. Automated native
interaction and reviewed captures are separate from owner acceptance.

Symmetric/two-sided thickness, graphical normals, automatic Boolean targets,
compound-sheet filling and broader high-curvature/self-intersection diagnostics
remain open. The existing kernel and its tolerance policy are reused. No new
geometry engine, property identity or document format is introduced. The native
solid-shell Thickness form retains its face-selection controls. The 2D
Offset geometry implementation is unchanged. Native Invalid status remains the
authority after failure even when the last successful shape is retained.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-sheet-thickening-20261001`.
The final build passes; nine focused checks plus eight accepted sewing regressions
pass, and six native captures were reviewed. `visual/Sheet-Thickening-Sources.FCStd`
and `visual/Sheet-Thickening-Results.FCStd` provide owner fixtures. This is a local
source-built checkpoint; no installer or release was updated.
