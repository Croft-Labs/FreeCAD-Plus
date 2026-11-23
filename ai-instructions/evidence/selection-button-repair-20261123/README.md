# Selection button correction — November 23, 2026

Owner reported that the newly expanded curve-intent button was dark in the light
theme and opened its menu only through the arrow. This repairs that specific
approved control to the owner's explicit correction, without adding a new design.

The button no longer uses its checked menu item as a default action. Instead it
copies the current setting's text/icon/tooltip and uses native InstantPopup mode.
The exclusive current-setting checkmark remains inside the menu; the toolbar
button is neither checkable nor checked. Its existing theme styling now renders
the normal light/dark background. Clicking icon, caption or arrow opens the menu.
The redundant split-button size override was removed. Category filtering, chain
expansion, saved intent and Classic mode are retained.

Before source edits, an isolated native preview reproduced the failure using the
actual ribbon stylesheet and verified the proposed fix in both themes. Direct
images: [before](preview-before.png), [light](preview-light.png),
[dark](preview-dark.png). Companion fa1a1f6e8983 used clean snapshot
8c7eaf38da4a6e249857338806b0b67f31b86ec4 from production 393e5b1ab4;
only selection_preview/selection_toolbar.py changed. Capture fingerprint
a0b7d7b00a7d9b4a210ad368ddca753ccb1fcf6e33a1bf5c8e43d095a930ddea,
fresh with no scope violations. No tool approval state was modified.

Five focused build checks passed: full-button interaction/current state/scope,
native topology, viewport chain picking and filters, ribbon theme backgrounds,
and category-menu gate ownership. Additional native assertions cover all three
setting labels and icon/caption/arrow clicks in both themes. The initial build
run had one synthetic sketch click miss; the runner lacked the standard per-test
QApplication window activation. After restoring that fixture behavior, all five
passed without further production changes. Both initial and corrected logs are
retained rather than discarding the failure.

Two script files are installed with source/build/installed hashes and rollback
copies recorded in install-manifest.json. Owner sessions/settings are preserved.
All five installed regressions, both-theme interaction assertions and the existing
shortcut verification passed. Direct installed images: [Light](installed-light.png),
[Dark](installed-dark.png). The shortcut uses its unchanged target with an isolated profile.
Existing processes need restart to load the revised Python module.

Generated validation fixtures are removed after archival, retaining rollback
files and the shortcut's running profile. Unrelated project.previewfirst.json
is preserved and excluded from this change.
