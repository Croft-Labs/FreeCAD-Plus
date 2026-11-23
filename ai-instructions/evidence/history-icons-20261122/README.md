# History coordinate icons and collapsed defaults — installed

Owner approval: **"implement"**, following the direct native screenshots in
[preview evidence](../history-icons-preview-20261122/README.md).
The production panel.py is identical to the approved candidate from session
94bcfb75e36d, fingerprint
5f9b3e1eeb327600b8ef079fede79f38fa33af8c3e76d0955590b3631cd3c89f.

Axes and Planes copy the native icon of their first child. New Coordinate System
rows and their descendants start collapsed. Existing rows retain manual expansion
choices across refresh. Visibility flags, eye controls and other tabs are preserved.

- `FreeCADPlusScripts` refreshed the development payload; no native rebuild needed.
- [Install manifest](install-manifest.json): source/build/installed hashes match;
  the prior panel.py is retained under the task runtime's install-backup directory.
- [Regression results](regression.json), [full log](regression.txt): all 14 existing
  TestComponentPanel and TestHistoryVisibility tests passed in the installed app,
  covering actual eyes, mixed states, task-time clicks, selection, Undo, saved
  visibility and external source ownership.
- [Native visual result](visual.json): all groups initially collapsed, group/child
  icon pixels identical, manual expansion preserved and geometry visibility unchanged.
  Direct installed screenshots were visually reviewed:
  [default](default.png), [root opened](groups.png), [children opened](children.png).
- [Shortcut result](shortcut.json), [target](shortcut-target.json): restarted using
  the existing desktop shortcut, with explicit isolated user/system/data paths.
  The previous empty isolated window closed gracefully. The updated app remains open.
- [Cleanup](cleanup.json): disposable fixtures and inactive validation profile removed;
  rollback files, durable evidence and the active shortcut profile retained.

Runtime: C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus.
The owner profile and unrelated project.previewfirst.json were never changed.
Helper scripts/macros here reproduce installation and isolated native acceptance.
