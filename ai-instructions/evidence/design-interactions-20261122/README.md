# Installed Design interaction acceptance — November 22, 2026

These captures show working functionality in the installed FreeCAD Plus app,
not isolated preview fixtures. The three previews were approved in chat before
production changes. Native runs use disposable profiles and fixture documents.

- `design_regression.txt/json`: 103 tests passed, zero failures/errors.
- `design_visual.json`: exact ordered native idle actions, selection guard,
  command-opened sketch placement, real History clicks and numeric arrow updates.
- `design_reopen.json`: independent-process geometry, identity, downstream features,
  source-owned History visibility and component datum edit/Cancel persistence.
- `installation.json`: source/installed SHA-256 pairs verified after final build.
- `shortcut.json`: existing desktop launch target and working directory verified.
- `native-build.log`, `datum-build.log`, `final-build.log`: successful native and
  final incremental build transcripts (compiler output was also checked live).

The FCMacro harnesses reproduce the native acceptance with `PLUS_TEST_DIR` set to
a disposable output folder; run the regression harness before the reopen harness.
Expected invalid-geometry cases print native diagnostic errors. Native unattached
datum tests explicitly confirm the placement warning; other dialogs are not
silently dismissed. Test-window activation is maintained only for docked tasks.

The first screenshot path using QWidget.grab produced OpenGL capture corruption;
the checked and retained screenshots use the native screen capture path. Existing
UI layout, coordinate graphics, units and manual-preview behavior are preserved.
