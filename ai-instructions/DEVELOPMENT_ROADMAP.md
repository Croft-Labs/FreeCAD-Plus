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
- [   ] **G1.2 — Single-component pilot (next).** File root, one domestic Part001
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
- [   ] **G1.3 — Initial legacy conversion.** Simple `.FCStd` fixtures; preserve
  originals and editability, explicitly report fallback geometry, test fresh reopen.
- [   ] **G1.4 — Hierarchy and shared instances.** Nested components, shared edits,
  parent-owned transforms, cycle prevention and matching conversion cases.
- [   ] **G1.5 — External definitions.** Nested import catalogs, source-file ownership,
  independent copies and explicit cross-file failure/recovery checks.
- [   ] **G1.6 — Component panel.** Models/Part Tree/History, file row, explicit Edit,
  occurrence tracking, confirmed actions and temporary unused-model editing.
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
