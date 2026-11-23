# New component navigation preview — November 23, 2026

Historical native UI proposal, subsequently approved with the other two pending
changes on November 23. See [implementation evidence](../component-task-updates-20261123/README.md).
Creating a component should activate it in the current view and show
Components > History. Definition-only creation adds no extra placed instance.
New File retains its initial definition + instance contract and should land on
History too. Generic definition factories/import/copy must not navigate.

[Current](before.png): creating Part002 leaves Part001 active on Models.
[Proposed](after.png): Part002 is active with History open and Coordinate System
collapsed. [Empty file](empty.png): new Part001 is active with History open.

The isolated native scene invokes existing creation, then a candidate presentation
hook. These are actual Qt dock captures; command integration is not implemented.
Both cases pass activation/tab/ID/link assertions (`candidate.json`). Owner sessions,
documents and profiles are untouched. Existing document ownership, geometry,
identities, stored visibility, layout and feature-task tab restoration are preserved.

Product baseline: `350bac6cb61ec79f0b7466e2399e1a4cdd8d7043`.
Clean panel snapshot: `74e90f3218547ae39354a726e9dddf3719de88cd`, workspace
`new-component-preview/review-source`. Untracked `project.previewfirst.json` preserved.
Companion session: `96e077810961`; allowlist: `panel.py`.
Fingerprint: `3526496763a3b1d6fc09b16449499db2f093e195c95dff548ec11b4b2b124412`.
Inspection: fresh, no violations, not approved. Approval state was not changed.
Renderer, scene and candidate are archived here. Isolated runtime output uses
the development build's `validation/new-component-preview-20261123` directory.

After approval, wire navigation into `hierarchy.new_part` / `Std_Part` and New File
creation. Update old tests expecting the previous context. Check empty/existing
files, external-definition ownership, Undo/Redo, failed creation, both panel modes,
and subsequent feature-task tab restoration. Install with rollback, validate the
existing shortcut using isolated settings, then commit/push/verify.
