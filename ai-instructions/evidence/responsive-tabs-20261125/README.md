# Responsive component tabs — November 25, 2026

The owner requested equal Parts/Assembly/History tabs with a minimum fitting their
text and a maximum equal to the current padded tabs. After the native preview at
wide, intermediate and minimum widths, the owner replied **"approved. implement"**.

Preview session `c552c4c21917`, based on `553d21f4e1`, had only panel.py in scope.
The approved fingerprint was
`76addb914842a25a7d13146a7c2ee1e431a1e76561d7325b03f9ba09d95fde82`.
Post-approval inspection confirmed freshness and no scope violations. Chat approval
is authoritative; no companion approval controls were changed.

## Implementation

ComponentTabBar.minimumTabSizeHint supplies one shared lower bound, measuring all
labels in regular and bold fonts and adding the active native style's text-rectangle
inset. The existing tabSizeHint remains the common padded upper bound. Qt performs
the intervening layout; pixel rounding may distribute one extra pixel when the
available width is not divisible by three. Left alignment, native styling/height,
tab clicks and all model behavior remain unchanged. No native rebuild was required.

## Native verification

Source, installed app and existing desktop shortcut all pass the same isolated GUI
acceptance checks. At this profile's font/DPI, tabs measure 90 logical pixels each
in a 370-pixel panel, 77 each in a 231-pixel panel, and 64 each at the 192-pixel
text-fit minimum. These values are measured results, not hardcoded dimensions.

All three labels remain complete, including Assembly selected in bold. Each tab
is clicked successfully at minimum. Scroll arrows stay absent at supported widths,
appear one pixel below the combined minimum, and disappear on widening. The tabs
return to their original maximum and remain left aligned. The disposable model's
object identities and dependency graph remain unchanged. Native screenshots were
visually inspected; no broad geometry suite was needed for this sizing-only change.

## Installation and publication

Only `app/Mod/FreeCADPlus/freecad_plus/panel.py` was installed in the existing
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus` payload.
The installed/source SHA-256 is
`aad1867e8a8b6aae002a13746979e19deb69c725bf09a21e033eba7753791638`.
The manifest records the retained rollback copy under
`validation/responsive-tabs-20261125/backups/panel.py`.

The existing `C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk` still points to
`Launch FreeCAD Plus.bat` in that build root, with the same working directory and
no stored arguments. Checks use separate profiles and disposable documents; owner
files, preferences and running sessions are preserved. Restart existing sessions
to load the update. Generated validation output is removed after archiving results;
the payload and rollback copy remain. Commit/push follows standing authorization,
preserving the unrelated untracked project.previewfirst.json.

- [Approved sizing](approved.png)
- [Installed sizing](installed.png)
- [Source measurements](source-result.json)
- [Installed measurements](installed-result.json)
- [Existing-shortcut measurements](shortcut-result.json)
