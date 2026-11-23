# Clear selection after component creation — November 23, 2026

Owner correction: creating a component opens History with a selected object and
therefore an empty Tasks panel; deselect all after navigation. The repair keeps
the new component active and History selected, then synchronously clears native
selection and synchronizes the tree highlights. No delayed callback can erase the
user's next pick. Geometry, identity, ownership, visibility, instance counts, generic
factories/import/copy and existing feature commands remain unchanged.

This restores the already-approved creation navigation and Create Geometry idle
UI. The existing approvals are reused for this defect repair, together with the
owner's explicit selection-clear instruction; no new UI design is introduced.
See [approved navigation](../new-component-preview-20261123/README.md) and
[installed idle geometry actions](../design-interactions-20261122/README.md).

## Native preview and verification

The isolated panel candidate reproduced all three affected paths: New File,
New Component and creation in an empty native file. The baseline retained a
selection and hid idle actions; the candidate leaves all native/tree selections
empty and displays New Sketch, Datum Plane, Datum Line, Datum Point. A subsequent
selection survives. `baseline.json` and `candidate.json` record these results.
`before.png`/`proposed.png` juxtapose literal Qt dock captures for inspection.

Product baseline `e83c9015918e654363c3f572ea53c83166ec8214`; one-file snapshot
`10faf687f6732b1f2c5769560e2a5dc697e25b96`, workspace
`creation-selection-preview/review-source`. Companion session `7120b046957c`,
allowlist `panel.py`, fingerprint
`fcff902dd67b18557ac13fedd5aa7b9324c78ad6028d96cca9cc8346e0b8ee08`.
Inspection was fresh with no violations. No approval flag was changed.

- `build-focused.json/txt`: 8/8 focused native checks passed.
- `installed-regression.json/txt`: 8/8 passed against installed modules, including
  external ownership, both presentations, creation/Undo/Redo, shared commands,
  History/task restoration, empty selection and preservation of the next pick.
- `visual.json`: all three real installed native command creation paths passed
  active-component, History, empty selection and idle-action assertions.
- [Installed History](history.png) and [installed idle tasks](idle-tasks.png) show
  the corrected state; idle tasks were visually inspected.
- `shortcut.json` and `shortcut-target.json`: existing desktop launcher verified
  with explicit isolated settings. Owner sessions were not closed or modified.

## Delivery

Only FreeCADPlusScripts was built (`build.log`); no native rebuild was needed.
`install.py` installed `panel.py` and the two updated test modules, verified
source/build/install hashes and retained rollback originals (`install-manifest.json`).
`run-validation.py regression --repair` runs focused build checks; add `--installed`
for installed checks. `visual --installed` verifies real command creation in a fresh
process. `restart-shortcut.ps1` launches the existing shortcut with an isolated profile.

Validation output uses the development runtime's `validation/creation-selection-20261123`
directory. `cleanup.ps1` verifies resolved paths before deleting generated fixtures
and archived screenshots; it retains `install-backup` and the running
`profile-shortcut`. See `cleanup.json`. Existing processes must be saved/restarted
to reload cached Python modules. Untracked `project.previewfirst.json` is preserved.
