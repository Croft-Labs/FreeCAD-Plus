# Single-part opening correction — November 27, 2026

The owner reported that reopening a one-part file did not activate the part or
show its features in History. The installed assembly default was independent of
Edit: `document.open_document` unconditionally called `editing.edit_file`.
The corrected initialization uses the sole local definition and its unambiguous
occurrence, or definition isolation when no unique occurrence exists. Multiple
local definitions retain file-level initialization. Normal opening, recovered
opening and sub-file new windows call the same helper. No controls/layout changed.

The current bug report and earlier explicit one-part-opening instruction authorize
this correction. The earlier simulation `21199169778b` remains historical preview
evidence; this delivery does not claim approval or implementation of the separate
saved last-active-part bookmark proposal. No companion approval state was changed.

## Verification

- Baseline `b2`: 4 of 7 checks reproduce missing Edit context; the other 3 pass.
- Source `s3`: all 16 focused checks pass.
- Installed `i1`: all 17 checks pass in 17.456 seconds, including observer cleanup.
- Geometry, placement, visibility and metadata survive reopening unchanged; native
  Undo is empty and the reopened document is unmodified. History contains the part's
  Solid feature. Parts remains the selected tab until the test selects History
  solely for the [installed screenshot](reopened-history.png).
- Hidden imports retain the host context; refreshing/reopening an already-loaded
  file does not override explicit file-level Edit. A new sub-file view initializes
  independently of its previous view. Relocation recovery preserves the saved file
  until explicitly saved. Existing active-assembly navigation checks pass.

The first exploratory run loaded imported legacy panel tests as well as navigation
tests. Four legacy failures reproduce in untouched installed baseline `b3` (old
tab/assembly expectations, occurrence-memory expectation and duplicate-name fixture).
An additional source-only observer failure came from reloading `editing` in the
harness and losing its callback list; the harness now preserves that list. The
installed observer cleanup check passes. Early new-test fixture mistakes were
corrected before final validation; logs are retained for traceability.

## Installation and publication

`FreeCADPlusScripts` built successfully. Four Python implementation files and
`TestSinglePartOpen.py` were installed with matching source/build/app hashes.
Owner settings and desktop shortcut hashes are unchanged. The rollback is retained
under the build root's `validation/single-part-open27/rollback`.

The test runner uses an isolated profile and disposable CAD fixtures; no owner
documents were opened or saved. Evidence includes build/install results, final
native screenshot, baseline/source/installed results and the validation harness.
Generated runs are removed after archiving. This change is committed and pushed
to `codex/freecad-1.1.4-baseline`, with remote SHA verified at delivery.
