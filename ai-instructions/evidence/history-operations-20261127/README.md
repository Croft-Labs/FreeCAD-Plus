# History operation icons and labels — November 27, 2026

The owner corrected the earlier palette to yellow for both New and Add, red for
Subtract, then explicitly approved implementation. The approved native screenshot
is [here](approved-preview.png): session `3bbe1c582151`, fingerprint
`abd0aea313d7713fa3578fa96d7f3c83a301ddf7ce708a72e4e2c3d0ba212342`.
It supersedes `45ea6c4ba72f`; no companion approval state was changed.

History now appends `(new body)`, `(new surface)`, `(add)` or `(subtract)` to the
feature's displayed label and tints a copy of its native glyph. Stored Label/Name,
IDs and original ViewProvider/toolbar icons remain unchanged. Bounded caching
avoids repeating pixel conversion for the same icon/palette pair. New and Add use
the same yellow. The selected-row text remains controlled by the normal palette.

Supported contracts are version-1 Plus Extrude, Revolve, Loft and Thicken, native
Part Design additive/subtractive profile operations and primitives, and native Part
Extrusion/Revolution/Loft/Sweep New output. Native additive classification checks
the actual BaseFeature solid; broken or unknown contracts are left unclassified.
Names and generic shape removal are never used to infer an operation. The tree's
Row identity and raw label remain unchanged; presentation is applied only to
History feature items during normal reconciliation.

## Verification

Source `s1`: all 20 checks pass. New checks use actual Plus extrusion New/Add/Subtract
results, a successful Add-to-Subtract edit with native Undo, custom-label refresh,
native primitive predecessor classification and save/reopen. They also verify
source icon preservation, exact selection routing, visibility eyes/Undo, schema
fallbacks, new-sheet suffixes, cache reuse and unchanged coordinate/sketch rows.
Existing History Appearance and component navigation regressions are included.

Initial source `s1` and installed `i1` each passed 20 checks, but final log review
found Qt warnings: bright highlights could exceed the 8-bit RGB channel range.
The conversion now clamps channels to 255, and the icon test captures Qt messages
on a bright highlight to prevent regression. Focused source `s2` passes all six
new tests with empty stderr. Original repetitive warning logs are retained as
losslessly compressed `.gz` files.

Final installed `i2`: **all 20 checks pass**, with zero failures/errors and empty
stderr. The inspected
[native screenshot](installed-history-operations.png) confirms the approved palette
and suffixes on real extrusion features. The harness uses isolated profiles and
disposable fixtures. To rerun, restore
the harness to the workspace's `history-operations-validation` directory: its
preference-pack source is relative to that location. Build log trailing whitespace
is normalized for repository checks. Owner documents were not opened by tests.

## Scope and installation

Three Python payloads comprise this change: the new History presentation module,
the panel integration, and the native regression suite. Build/install manifests
confirm matching source/build/app hashes and unchanged owner settings/shortcut.
`FreeCADPlusScripts` built successfully. Rollback copies are
retained under the external build's `validation/history-operation-colors27/rollback`.
The owner saved and closed the app before installation.

Transformation workflow `57a9ef350816` and plane-visibility workflow `40f73afdef86`
remain separately pending approval and are not implemented in this delivery.
