# FreeCAD Plus: Development roadmap

## Clean stable baseline — October 10, 2026

- [x] Verify official latest stable is 1.1.4; distinguish 26.3 RC1 prerelease.
- [x] Start clean branch from official 1.1.4 commit with its pinned submodules.
- [x] Preserve owner UI specifications/evidence and segregate old implementation documents.
- [x] Verify source equivalence and preserved-document integrity.
- [x] Publish the baseline branch and make it the fork's default working branch.
- [x] Record final status and remove temporary staging.

Source checkout, build, runtime validation and owner delivery are separate stages.
Original workbench source is retained.

## Light baseline verification — October 10, 2026

- [x] Confirm stable-release status and successful upstream release/CI workflows.
- [x] Recheck source equivalence and four pinned submodules.
- [x] Verify official Windows package checksum and executable signature.
- [x] Inventory runtime versions, shipped modules and all registered workbenches.
- [x] Check basic modeling, recompute, Undo/Redo, expressions, links and file exchange.
- [x] Check FCStd save/reopen and separate-process reopen/recompute.
- [x] Inspect exported model image; verify event processing and normal test exits.
- [x] Isolate capture artifacts; verify clean viewport buffers through automated rotation, zoom, resizing, workbench changes and idle stability.

[WORK_STATE](WORK_STATE.md#stable-baseline-inventory-and-light-runtime-check--october-10-2026)
owns inventory, provenance, results and limitations. Core checks pass using the
official binary matching this checkout. No local compilation or owner shortcut
delivery occurred. The light baseline display gate is closed; exhaustive GUI or
long-session jitter acceptance is not claimed.

## Group 1 — component panel and document structure

Owner authorized Group 1 on October 10, 2026, with a stop after the current task's
checks pass. Work proceeds in reviewable stages; subsequent groups remain outside
scope. [ARCHITECTURE](ARCHITECTURE.md) owns the structural contract.

- [ X ] **G1.1 — Structural contract.** Define native service reuse, file/definition/
  instance ownership, persistent identity, `.cadprt` storage and legacy-conversion
  boundaries. Checked against confirmed requirements and current native source;
  documentation links and whitespace pass. No runtime implementation claimed.
- [ X ] **G1.2 — Single-component pilot.** File root, one domestic Part001
  definition and one native linked instance; explicit Edit context; an existing
  Sketch -> Pad workflow with backend Body; genuine versioned `.cadprt` persistence.
  Acceptance: correct ownership/instance count, valid editable geometry, recompute,
  transaction rollback and Undo/Redo, save/reopen in a fresh process, stable identities
  and placement, exact filename, no duplicate root on reopen, and unchanged original
  command behavior outside the pilot. Native mapping validated in the opt-in module.
  Six native GUI-process tests passed, plus separate-process reopen/edit/save and
  native Sketch/Pad editor acceptance; clean normal framebuffer inspected. Script-only
  CMake build/install passed. No native rebuild, full panel or owner-build delivery.
  Detailed evidence and stopping boundary are in [WORK_STATE](WORK_STATE.md).
- [ X ] **G1.3 — Initial legacy conversion.** Simple `.FCStd` fixtures; preserve
  originals and editability, explicitly report fallback geometry, test fresh reopen.
  Completed for empty files, single native Bodies, Boxes and static shapes/curves;
  explicitly requested standalone geometry fallback is persistently reported.
  Eleven native-process tests (five conversion, six pilot regression) and a separate
  process reopen/edit/save passed. Schema 1 remains readable; schema 2 adds direct
  geometry ownership. Script build/install passed. No owner executable or full UI
  delivery. See WORK_STATE for source protection, limits and identity handling.
- [ X ] **G1.4 — Hierarchy and shared instances.** Nested components, shared edits,
  parent-owned transforms, cycle prevention and matching conversion cases.
  Sixteen native-process tests (five hierarchy plus eleven prior regressions), fresh
  reopen/edit/save of both new and converted hierarchies, and native Sketch/Pad
  editing through the second occurrence passed. Clean four-solid viewport inspected;
  script build/install passed. No owner executable or full panel delivery claimed.
  WORK_STATE records evidence and the explicit schema-3 upgrade boundary.
- [ X ] **G1.5 — External definitions.** Nested native import catalogs, defining-file
  Edit/save ownership, independent recursive copies and explicit replacement selection.
  Twenty-three native-process tests (seven external cases plus sixteen prior regressions),
  fresh-process identity/reopen/shared-update checks, and native Sketch/Pad editors
  through a nested external occurrence passed. Missing/wrong/future dependencies,
  unsaved source/catalog ordering and failed saves were refused and recovery checked.
  Clean two-instance viewport inspected; all thirteen script build/install files matched.
  No owner executable, full panel or storage/replacement dialogs delivered. WORK_STATE
  and ARCHITECTURE record schema-4 boundaries and exact-path recovery limitations.
- [   ] **G1.6 — Component panel.** Overall panel stage remains incomplete; split into
  reviewable increments so the owner can stop after each increment's checks.
- [ X ] **G1.6a — Panel foundation.** Opt-in Models/Part Tree/History, pinned file row,
  nested imported catalogs, placed-component Edit, occurrence tracking/highlighting,
  native selection and file-origin visibility controls. Stable rows and coalesced
  native observers preserve interaction state; no polling while idle. Twenty-nine
  combined native/Qt tests passed, plus fresh-process panel reopen/identity checks,
  inspection of all three tabs and file History, and fifteen-script build/install.
  No owner executable or full G1.6 completion claimed; WORK_STATE records boundaries.
- [   ] **G1.6b — Unused-model editing (next).** Temporary last Part Tree row,
  definition editing, assembly hiding/restoration and save-safe transient isolation.
- [   ] **G1.6c — Remaining confirmed panel actions.** Component file tabs and the
  confirmed context actions; integrate shared workflows only against their approved
  contracts. Deferred Add Component and unconfirmed checklist/destructive-action
  details are not approved by this task list.
- [   ] **G1.7 — Contextual display.** Confirmed Part Type, visibility, reference
  restrictions and edit display; resolve undefined task interactions first.
- [   ] **G1.8 — Group acceptance.** Representative legacy fixtures and combined
  persistence, dependency, original-workbench and responsiveness regression checks.

Each stage records implementation, runtime validation and owner delivery separately.
Do not claim all Group 1 tests are complete because G1.1 documentation checks pass.
Do not repeat the completed baseline checks without a new relevant concern.

The [old roadmap](archive/pre-restart-docs/DEVELOPMENT_ROADMAP.md) records archived
work only. Its checked milestones and outstanding tasks do not describe this source
branch or authorize restoring old code. This file is the only current roadmap.
