# Document tabs at top — preview pending approval

Owner requested moving file tabs from the bottom to the top of the document
viewer. Proposed production change is exactly one line in `src/Gui/MainWindow.cpp`:
`d->mdiArea->setTabPosition(QTabWidget::South)` becomes `QTabWidget::North`.
Tabs sit directly beneath the toolbar, within the central viewer. No new setting,
tab-name/order/close behavior, component/task dock, status bar or geometry change.

**Not implemented, built or installed.** This does not approve the pending mesh,
transformation, plane-default, intersection or trimming workflows.

Companion session `305f2340501d`, allowed file `src/Gui/MainWindow.cpp`.
Fingerprint `f9e5c2d6a754edfb801f48389d5bdfc3e8fd9e20a761452185ec7153625c16cf`.
Inspected current with one-line diff, no scope violations, approval false.
Focused baseline is the exact file from main source `738cc2863c`; main repository
and unrelated untracked `project.previewfirst.json` remain untouched.

[Current window](baseline/window.png) · [Proposed window](candidate/window.png)

## Evidence

Separate native FreeCAD sessions read the source setting from each review worktree
and apply the same QMdiArea API, without rebuilding or changing installed binaries.
The live API recreates the tab bar, so the harness also executes the unchanged
constructor steps for closable/non-expanding tabs. This mirrors initialization;
those steps are not additional proposed production changes.

Start plus two disposable documents are shown. Native Qt mouse switching between
documents succeeds. Tab order and movable/closable flags remain, with unchanged
document object identities and Undo counts. The tab bar's Y position changes from
706 to 0 within an unchanged 736-high central viewer. Both results pass.

Windows QWidget/framebuffer grabs corrupt the OpenGL region. Both screenshots
therefore combine the actual native UI capture with that same view's native
offscreen render at its exact widget size, position and camera. Offscreen rendering
omits viewport overlays such as the navigation cube; this is a capture limitation,
not a proposed visual removal. The coordinate graphics and production renderer are
untouched. Screenshots are native runtime previews, not evidence of installation.

After approval: apply the one line to production source, build the native GUI,
install with the owner application closed, and verify startup tab placement and
document switching while preserving settings and shortcut. No new automated
regression suite is necessary for the single placement constant.

Private profiles/fixtures are removed after archiving verified evidence. Companion
worktrees remain available for approval. No approval record was changed.
