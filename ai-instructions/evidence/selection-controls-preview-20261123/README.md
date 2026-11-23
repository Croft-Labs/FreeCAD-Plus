# Selection toolbar preview — November 23, 2026

Status: native Qt UI simulation prepared for owner review. Not implemented in the
production checkout or installed application. Sketch Exit/Cancel preview remains
separately pending. Owner clarified Select 1 means choosing one filter category,
not selecting one geometry object.

## Proposed behavior

- Curve-intent button shows its existing native icon and current setting name:
  Single Curve, Connected Curves, or Tangent Curves.
- Category button shows its icon and All, one named category omitted, an omitted
  count, or the sole category followed by only. Tooltip lists enabled categories.
- Select all / reset enables all eight existing categories.
- Select 1 highlights guidance and arms replacement; existing categories remain
  checked and effective until the next category click commits a singleton.
- Closing the popup, clicking outside or Escape cancels the armed state and keeps
  the prior filter. No intermediate empty filter exists.
- The last enabled checkbox cannot be cleared manually. Guidance explains why;
  enabling another category allows it to be unchecked again.
- Existing taxonomy, Directional/Persistent controls, command gate intersection,
  curve-expansion semantics, geometry, task selection and Classic mode stay intact.

## Direct screenshots

[Before](before.png), [proposed menu](menu.png), [Select 1 waiting](select-one.png),
[Curves only](curves-only.png), [Curves omitted](curves-omitted.png),
[2 omitted](two-omitted.png), [Single Curve](single-curve.png),
[Connected Curves](connected-curves.png), [Tangent Curves](tangent-curves.png).

These are actual native Qt widgets/icons rendered in a separate FreeCAD dialog,
not a full-ribbon installation. The fixture replaces preferences with memory and
disconnects selection gates. Candidate filter state is UI-only. Interactive dialog
is available in an isolated FreeCAD process; close its window when finished.

## Validation and provenance

Native Qt mouse checks passed: All → Curves omitted → 2 omitted, armed-state
outside-click dismissal, Escape dismissal, Select 1 → Curves only, last-checkbox
guard, re-enabling Edges, reset, all three intent labels and non-null icons.
Outside-click check sends a mouse event outside the popup and verifies native
dismissal; it does not force-close the menu. See candidate.json. Baseline capture
uses unchanged selection modules. Owner profiles/documents were not accessed.

Companion c81b636d7ce5; clean snapshot bf0a6e9407958e3a500022332369374da4e1c09e
from production 9d6b4928608ba3238c79619c2171492d4f6a92e8. Exact allowlist:
selection_preview/category_selection.py and selection_preview/selection_toolbar.py.
Fingerprint 7df145a89e9179dc4c689e1da50fede7f6d1d6360f01e05bc32db8772c4e8898;
fresh capture, no scope violations, approval false. Approval state was not changed.
Candidate sources and harness are archived here. Rendering dependencies remain in
the existing external development runtime; no builds/installations performed.

## Implementation scope after approval

Integrate the approved controls with saved category preferences and native gate;
initialize from current preferences rather than the prototype's All state. Recover
legacy all-disabled preferences to All and enforce nonempty state at the shared
configuration boundary. Commit Select 1 category atomically; dismiss without saving.
Keep summaries current after reload/rebuild and clear stale preselection after a
committed category change. Use the shared task-status styling where appropriate
rather than copying prototype CSS as a new error style. The amber prompt here is
normal pending-choice guidance, not a selection error.

Verify actual viewport admission and task-gate intersection, empty-preference
recovery, persistence/restart, menu mouse/keyboard use, intent selection, both UI
modes, responsive toolbar width at owner resolution, and unchanged directional/
persistent behavior. Then build scripts, install with rollback, validate using an
isolated profile through the existing shortcut, and commit/push completed changes.
