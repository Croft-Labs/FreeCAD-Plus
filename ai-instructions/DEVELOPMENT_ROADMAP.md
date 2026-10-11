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

**Owner scope correction:** menu access does not make the launched operation part
of Component Panel implementation. Group 1 owns Models/Part Tree/History, document
and instance structure, selection/Edit context, tabs, presentation and menu routing.
Move Components workflows belong to operation/task-panel work. They are not gates
for completing Group 1. Their historical IDs and completed evidence are retained
under the separate operation section below. Next increment: **G1.7b3 remaining Part Type integration**, not
Point to Point.

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
- [ X ] **G1.6b — Unused-model editing.** Domestic and external definitions support
  the temporary last Part Tree row, save-safe isolation, viewport picking and native
  Sketch/Pad editing in the assembly view. History uses native command transactions;
  external edits and Undo/Redo belong to the defining file. Per-view native contexts
  are cleared on context exit, import removal, panel/view/source closure and deletion.
  **Build:** native 1.1.4 development targets and required runtime resources passed.
  **Validation:** 9/9 focused and 38/38 combined tests, zero skips; fresh-process
  identity/save/reopen and source-only save checks passed. Normal viewport captures
  verified isolation/restoration and live Sketch/Pad preview; Part Tree inspected.
  **Publication:** source milestone `54ea2843a3` pushed to origin/codex/freecad-1.1.4-baseline
  and remote revision verified; no release or owner-build delivery.
  This is a bounded development build, not full-workbench or complete-panel acceptance.
  WORK_STATE records details; the remaining panel actions are separate increments.
- [   ] **G1.6c — Remaining confirmed panel actions.** Component file tabs, structural
  actions and confirmed menu routing. A menu entry opens its separately owned operation;
  it does not authorize implementing that operation within Group 1. Deferred Add
  Component and unconfirmed checklist/destructive-action details remain unapproved.
- [ X ] **G1.6c1 — Component file tabs.** Open in new window from Models/Part Tree;
  retain per-view Edit/camera and source ownership, native editor guards and cleanup.
  **Build:** eighteen-script payload copied/verified in the existing native development build.
  **Validation:** 6 focused and 44 combined tests passed, zero skips; fresh-process
  identity/source-only save/reopen and inspected tab/panel/viewport captures passed.
  Test cameras were made deterministic after diagnosing an animation/fitAll race.
  **Publication:** source milestone `a7c3adf492` pushed to origin/codex/freecad-1.1.4-baseline
  and remote revision verified; no release or owner-build delivery.
  WORK_STATE records evidence and limitations; remaining actions are separate increments.
- [ X ] **G1.6c2 — Linked-instance Copy/Paste.** Part Tree menu/keyboard actions
  create shared native links under the selected parent, preserving copied local
  placements. Batch preflight/Undo and source-file ownership are implemented.
  **Build:** script payload updated in the existing native development tree.
  **Validation:** six focused and 50 combined tests passed, followed by independent
  save/reopen and inspected viewport/tree/menu captures. Dock reopening also handles
  a temporarily absent active subwindow. WORK_STATE records evidence and limitations.
  **Publication:** source milestone `e092033275` pushed to
  origin/codex/freecad-1.1.4-baseline and remote revision verified; no owner-build delivery.
  The announced destination convention remains subject to owner correction.
- [ X ] **G1.6c5 - Shared definition Rename.** Component menus rename the defining
  object in its own file, updating all occurrences while retaining identity. Unique
  per-file names, no-op/Cancel, guarded dialogs and native Undo are supported. Script
  build, four new cases plus one affected window regression, and independent domestic/
  external reopen passed across the bounded status-observation correction. WORK_STATE
  owns exact evidence and limits. Source milestone `50d9d1c4ab` pushed to origin;
  exact remote revision verified. No owner delivery; stop here.
- [ X ] **G1.6c6 - Models file import.** Menu/chooser imports saved catalogs into
  the edited definition's owning file without placement or extra tabs. Nested
  catalogs, external Edit, Undo, cancellation, duplicate/cycle/error guards and
  independent domestic/external reopen passed. Five distinct native cases completed
  across bounded test-driver/fixture corrections; WORK_STATE owns exact evidence.
  Script build passed; source checkpoint `6eda0296fc` pushed to origin and exact
  remote revision verified. No owner delivery; stop here.
- [   ] **G1.7 — Contextual display.** Confirmed Part Type, visibility, reference
  restrictions and edit display; resolve undefined task interactions first.
- [ X ] **G1.7a — Part Type and visibility state.** Completed saved-state increment:
  parent-owned saved direct-child settings, separate Shown/Hidden state, corresponding
  tree controls and restoration on Edit. Follow the confirmed Component Panel contract.
  Viewport rendering belongs to MODEL_VIEW_WINDOW; Add Reference Feature and other
  operation dialogs remain separately scoped. Native script-copy build passed.
  Six new state cases and affected regressions passed after focused corrections;
  independent reopen and inspected menus passed. WORK_STATE owns exact run evidence.
  Source milestone `47f766073d` pushed to origin/codex/freecad-1.1.4-baseline;
  remote revision verified. No owner-build delivery.
  See [saved-state contract](ARCHITECTURE.md#saved-part-type-and-visibility-state-g17a).
- [   ] **G1.7b — Contextual viewport integration.** Apply saved Part Type and
  visibility without global visibility leaks, restore per-view state, fade other
  occurrences, and enforce Reference/Excluded eligibility. Separate Add Reference
  Feature operation remains deferred. Split into bounded increments below.
- [ X ] **G1.7b1 — Explicit per-view hiding.** Hidden/Excluded and nested Reference
  filtering use native view-local paths; clear on context changes, unused isolation,
  panel/view closure. No native Visibility writes. Native build, focused tests,
  affected regressions, independent reopen and normal-buffer inspection are recorded
  in WORK_STATE. Final five display/lifecycle cases passed, zero failures/errors/skips.
  Implementation and planned checks are complete; stopped. Source milestone
  `8b7b382834` pushed to origin/codex/freecad-1.1.4-baseline; remote verified.
  No owner-build delivery.
- [ X ] **G1.7b2 — Contextual fading.** Active occurrence and descendants keep
  authored appearance; other occurrences use at least 75% transparency, preserving
  greater authored transparency. File Edit and context exit restore appearance.
  Native development build, all five fading cases, independent reopen and normal
  framebuffer inspection passed. Shared mixed-material fading is corrected by a
  native primitive-cache material dependency. Planned checks complete; stopped.
  Source milestone `fbcecf8440` pushed to origin; remote revision verified.
  WORK_STATE owns evidence. No saved material property mutation or owner-build delivery.
- [   ] **G1.7b3 — Remaining content/eligibility integration.** Reference-use
  eligibility and its panel/operation boundary remain unfinished. Recover the latest
  owner conversation before treating further workflow details as undefined. Saved
  unused-preview display and Bodies Only filtering are complete in the increments
  below. Right-click access does not make a separate operation part of Group 1.
- [ X ] **G1.7b3a — Saved display in unused previews.** Self/child Hidden/Excluded
  and nested Reference choices apply without creating instances or changing native
  visibility. Native build, focused behavior/regression checks, independent reopen
  and inspected normal-buffer display passed. Planned checks complete; stopped.
  Source milestone `ad4fa8d26a` pushed to origin; remote verified.
  WORK_STATE owns evidence. No owner-build delivery.
- [ X ] **G1.7b3b — Bodies Only content filtering.** Native body results and eligible
  nested components remain; construction/history content is filtered per view.
  Saved types, native visibility, identities and source ownership are preserved.
  Script target, affected native regressions, Sketch editor, independent reopen
  and inspected normal-framebuffer comparison passed. WORK_STATE owns the exact
  initial failures, bounded snapshot fix and focused results. Source milestone
  `93f6ac4f38` pushed to origin; exact remote revision verified. Stop; no owner delivery.
- [ X ] **G1.7b3c — Shared geometry eligibility and existing consumers.** Read-only
  occurrence checks reject raw Reference/Excluded geometry before existing Move
  reference reads, preserving Edit access and owned derived features. Native scripts
  build, five eligibility cases, affected Move/Rotate/display regressions and an
  independent reopen passed. WORK_STATE records corrections and exact results.
  Source milestone `10ae708413` pushed to origin; exact remote revision verified.
  Stop here; no new operation or owner delivery. Remaining native modeling/export
  consumers still need integration; full G1.7b3 is not complete.
- [ X ] **G1.7b3d — Native export eligibility.** File > Export validates unresolved
  occurrences and its actual object payload before exporter options/writing. The
  existing source-owned unused Edit context supplies external export selections.
  Native build, four actual Export cases, five shared-policy regressions and an
  independent reopen passed; WORK_STATE records initial failures and corrections.
  Source milestone `8baa8ca44e` pushed to origin; exact remote revision verified.
  No owner delivery. Direct exporter and view-output routes remain separate
  integration work; full G1.7b3 is unfinished.
- [ X ] **G1.7b3e — Native modeling intake eligibility.** Shared native bridge checks
  PartDesign profile preparation/picking and Sketcher Projection/Intersection inputs
  before mutation, using original occurrence and explicit component Edit ownership.
  Batched native build, four focused modeling cases, five shared-policy cases and
  independent Pad/projection reopen passed across bounded corrective runs. WORK_STATE
  records exact coverage, fixture corrections and the inherited seam-reference limit.
  Source milestone `8aeb91a305` pushed to origin; exact remote revision verified.
  No owner delivery. Full G1.7b3 and Group 1 remain incomplete.
- [ X ] **G1.7b3f — Native attachment and shared picked references.** Native attachment
  checks picked/typed inputs and the full initial batch before mutation. The shared
  PartDesign axis/direction/plane collector checks original occurrence before native
  copy/reference handling. Batched native build, four focused cases and independent
  saved attachment/axis downstream checks passed. WORK_STATE records exact driver
  corrections and limits. Source milestone `5212b219b3` pushed to origin; exact remote
  revision verified. No owner delivery.
- [ X ] **G1.7b3g — Separate attachment and Extrude face/shape inputs.** Python
  attachment guards initial/picked/typed references, preview and Apply/OK; component
  Cancel closes Apply's lazy transaction before restoring display state. Native
  Extrude guards both sides' face/shape picks and typed face ownership before mutation.
  Batched native build, five focused cases across bounded corrective runs and
  independent saved-file/downstream checks passed. WORK_STATE records the actual
  transaction fix, driver correction and retained native link-scope warning.
  Source milestone `7bf802ac7a` pushed to origin; exact remote revision verified.
  No owner delivery.
- [ X ] **G1.7b3h — Loft/Pipe reference admission.** Shared component eligibility
  before picked profiles/sections and main/auxiliary path mutation; native workflows,
  legacy bypass and section cleanup remain. Batched native build, four focused cases
  across bounded driver corrections, and independent saved-file/source-update checks
  passed. WORK_STATE records exact runs and limits. Source milestone `0fdfdbf08a`
  pushed to origin; exact remote revision verified. No owner delivery.
- [ X ] **G1.7b3i — Shared dress-up/transformed input admission.** Guards new
  edge/face and Original additions before mutation; shared Add All Edges and both
  Fillet/Chamfer Use All Edges enforce component context/source eligibility. Removal
  cleanup and native legacy behavior remain. One batched native build, four focused
  cases across bounded driver corrections and independent reopen/source-change
  checks passed. WORK_STATE records the notification timeout, corrections and limits.
  Source milestone `4a047f0cb3` pushed to origin; exact remote revision verified.
  No owner delivery; command-start coverage follows in G1.7b3j.
- [ X ] **G1.7b3j — Dress-up/transformation command admission.** Full unresolved
  selection and active consumer checked before shared preparation and separate
  Multi-Transform conversion. Pattern Original picks no longer fall into direction
  parsing. Chamfer retains selection when preparation rejects. Initial and corrective
  native builds, eight focused cases across bounded corrective runs, and independent
  three-file reopen/source-change checks passed. WORK_STATE records the actual
  cleanup fix, driver corrections and unavailable upstream Scale command coverage.
  Source milestone `b35f8423e1` pushed to origin; exact remote revision verified.
  No owner delivery. Stop here. Next: component eligibility for
  existing PartDesign Boolean inputs. Full G1.7b3 and Group 1 remain incomplete.
- [ X ] **G1.7b3k — Same-component Boolean ownership prerequisite.** Native
  Boolean tool ownership is recognized by validation and eligibility; History hides
  nested Body containers and preserves tool features before their consuming Boolean.
  Full owned paths support selection/Edit. Script payload build, four new cases,
  two affected existing regressions and independent reopen/source-change passed.
  WORK_STATE records exact evidence and limits. Source milestone `2c48da7f9d`
  pushed to origin; exact remote revision verified. No owner delivery.
- [ X ] **G1.7b3l - Preserve legacy Boolean-owned tool graphs.** Standalone Body
  and native Part/shared-link conversion retain nested native tool ownership,
  expressions, identity and editing. Shared preflight rejects unsupported nested
  scripts and unowned content. Script payload build, four new conversion cases,
  two affected regressions and independent two-file reopen/source-edit passed.
  WORK_STATE owns exact evidence and limits. Source milestone `82028b9c0a` pushed
  to origin; exact revision verified. No owner delivery; stop here.
- [ X ] **G1.7b3m - Placed external export context.** Native dispatch retains
  originating assembly occurrences when external members resolve into their source
  file. Reference/Excluded checks precede exporter options/writing; source catalog
  fallback is refused. One native build, three new export cases, two affected
  regressions and independent assembly/source reopen passed. WORK_STATE owns exact
  evidence and limits. Source milestone `b9d3692472` pushed to origin; exact remote
  revision verified. No owner delivery; stop here.
- [ X ] **G1.7b3n - PartDesign Boolean Reference/Excluded input admission.** Full
  unresolved command selection and original picked occurrence checked before native
  mutation. Rejected picker state and removal cleanup retained. One native build,
  six focused cases and independent reopen/source-edit passed; WORK_STATE owns
  exact acceptance. Source checkpoint `751e77cbb2` pushed to origin; exact remote
  revision verified. This does not decide cross-component Full Component tool
  ownership. Next: remaining Part-workbench Boolean entry points.

- [ X ] **G1.7b3o - Core Part Boolean eligibility/ownership.** Cut/Common/Fuse
  and dialog Apply preflight component inputs. Native results retain input ownership
  and join the edited definition's History; legacy behavior remains. One native build,
  four focused cases and independent reopen/source-edit passed first run. WORK_STATE
  owns exact evidence and support limits. Source checkpoint `eae09d9177` pushed to
  origin; exact remote revision verified. Next: direct Part Section.

- [ X ] **G1.7b3p - Direct Part Section integration.** Shared input preflight and
  component-aware native result creation preserve ownership/History and line color.
  Original legacy parenting remains. One native build, four focused cases and
  independent reopen/source-edit passed first run. WORK_STATE owns evidence and
  limits. Source checkpoint `e6b3183c69` pushed to origin; exact remote revision
  verified. Next: compound input/result ownership. No owner delivery.

- [ X ] **G1.7b3q - Part Compound creation integration.** Shared input preflight,
  edited-definition result ownership and unchanged native Links/geometry. One build,
  four focused cases and independent reopen/source-edit passed first run. WORK_STATE
  owns evidence and limits. Source checkpoint `abcfa2a260` pushed to origin;
  exact remote revision verified. Next: Compound link-edit intake. No owner delivery.

- [ X ] **G1.7b3r - Compound link-edit admission.** Native drop/replacement and
  property-link additions share component checks; component drops preserve ownership.
  Six focused cases passed after correcting transfer permission and stable reference
  comparison; independent reopen/source-edit passed. WORK_STATE owns build evidence,
  correction history and limits. Source checkpoint `0dae6b5743` pushed to origin;
  exact remote revision verified. Next: split/join inputs/result ownership. No owner delivery.

- [ X ] **G1.7b3s - Split/join creation integration.** Seven native commands share
  occurrence-aware admission and edited-component ownership. Slice Apart keeps its
  native Slice/filter features directly in History; legacy grouping remains. Five
  focused cases and independent reopen/source-edit passed after correcting duplicate
  related-filter batch insertion. WORK_STATE owns evidence and limits. Next:
  split/join input editing admission. Source checkpoint `6416f489b1` pushed to origin;
  exact remote revision verified. No owner delivery.

- [ X ] **G1.7b3t - Split/join property-editor admission.** Eleven explicit native
  input properties share atomic dialog/property-item admission, cleanup and edited
  owner checks. Four focused cases, two affected Compound regressions and independent
  reopen/source-edit passed. WORK_STATE records build evidence, harness corrections
  and limits. Source checkpoint `3d6e6ddfdf` pushed to origin; exact remote revision
  verified. Next: split/join tree drop/replacement. No owner delivery.

- [   ] **Boolean input eligibility — pending owner decision.** Native Boolean
  grouping can transfer tools out of another shared component. Ask whether an owned
  linked reference is required first, created automatically, or ownership intentionally
  transferred. The question is outstanding; do not choose from current UI behavior.
  Complete command-start/picker guards once settled. Do not rerun G1.7b3k's completed
  checks without an affected change.
- [   ] **G1.8 — Group acceptance.** Representative legacy fixtures and combined
  persistence, dependency, original-workbench and responsiveness regression checks.

Each stage records implementation, runtime validation and owner delivery separately.
Do not claim all Group 1 tests are complete because G1.1 documentation checks pass.
Do not repeat the completed baseline checks without a new relevant concern.

## Operation workflows reached from the panel — outside Group 1

Historical IDs below remain stable for existing references; the G1 prefix does not
make these operations Component Panel scope. Translate/Rotate remain implemented;
their passing checks need no repetition for this documentation-only scope correction.

- [ X ] **G1.6c3 — Move Components foundation and Translate.** Implemented:
  sibling/parent context, component collector, transient preview/Apply/OK/Cancel,
  parent axes/picked directions and native length input. Copy remains separate.
  **Build:** script copy passed in the existing native development tree.
  **Validation:** 56 combined cases passed; six affected cases passed after final
  visibility/label corrections. Independent save/reopen and inspected preview,
  Cancel, committed placement and Tasks captures passed. WORK_STATE owns details.
  **Publication:** source milestone `6e18b9289d` pushed to
  origin/codex/freecad-1.1.4-baseline and remote revision verified; no owner-build delivery.
- [ X ] **G1.6c4 — Rotate.** Implemented in the shared task: parent/picked/two-point
  axes, optional pivot, native angle/Reverse, rigid group rotation and axis display.
  **Build:** FreeCADPlusScripts passed in the existing native development tree.
  **Validation:** 12 focused and 62 combined cases passed; independent save/reopen
  and inspected preview, Cancel, committed rotation, task and tree captures passed.
  WORK_STATE owns detailed results and limitations. Stopped after planned acceptance.
  **Publication:** source milestone `b14a8bc724` pushed to
  origin/codex/freecad-1.1.4-baseline and remote revision verified; no owner-build delivery.
- [   ] **G1.6c5 — Point to Point (operation, parked).** Unvalidated source and tests
  preserved locally on `codex/point-to-point-parked`, commit `288f99e69c`.
  Static parse/script copy completed; no runtime tests ran. Not on the baseline branch
  or active development payload. Resume only as separately scoped operation work.
  Align Axes, Align Coordinate Systems and Interactive also remain outside Group 1.

The [old roadmap](archive/pre-restart-docs/DEVELOPMENT_ROADMAP.md) records archived
work only. Its checked milestones and outstanding tasks do not describe this source
branch or authorize restoring old code. This file is the only current roadmap.
