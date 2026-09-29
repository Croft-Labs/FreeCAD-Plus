# FreeCAD-Plus Development Roadmap and Codex Agent Instructions

Version: 1.0  
Prepared: 2026-09-29  
Project: **FreeCAD-Plus, the owner's existing FreeCAD fork**  
Status: Proposed execution baseline; repository audit and estimates are not yet validated.

## 1. Mission and operating assumptions

Incrementally evolve the existing FreeCAD-Plus fork into a coherent mechanical CAD/CAM application with selected NX- and SolidWorks-inspired workflows. Preserve useful existing FreeCAD functionality and the owner's fork changes. Reuse upstream geometry, solver, assembly, and CAM capabilities wherever they meet the intended behavior.

**Do not create a replacement fork, restart from pristine upstream, or rewrite the application wholesale.** Start by inspecting the actual FreeCAD-Plus repository, its instructions, history, upstream relationship, and current functionality. No repository URL, checkout, build configuration, or existing modification has been inspected for this document; discover and record them before implementation.

The product goal is functional workflow improvement, not pixel-identical imitation or guaranteed NX/SolidWorks parity. UI simplification must preserve meaningful distinctions in the underlying data model. A working dialog is not a completed feature if its model cannot recompute, undo, save, reopen, and remain editable.

### Execution rule

**Resolve high-ripple architectural questions early; prove them in a narrow working implementation; migrate dependent workflows incrementally.** Do not defer foundational decisions until after dozens of commands depend on the old assumptions. Equally, do not use architectural criticality as justification for an unbounded core rewrite.

Default scope is the feature inventory below. All items remain tracked until implemented, superseded by verified existing functionality, or explicitly deferred with a reason. Future modules must not delay a usable modeling release.

## 2. How Codex must use this file

1. Follow the repository's applicable `AGENTS.md` instructions. Make the project's **Programming Roadmap** its first project-orientation reference after those instructions.
2. If missing, create `ai-instructions/PROGRAMMING_ROADMAP.md` during phase P0. Keep it a concise index, approximately 100–150 lines rather than a second specification.
3. Read the current milestone and relevant decisions; inspect the actual implementation before changing it.
4. Choose the earliest unblocked task according to section 4. Work in small, reviewable increments and maintain a runnable main development line.
5. Implement, validate, update progress, and continue authorized work. A phase gate is an evidence requirement, not an automatic request for owner confirmation.
6. Ask the owner only for material product ambiguity, abandoning a stated requirement, destructive action, or a decision outside existing authorization. Resolve routine implementation choices from evidence.
7. Do not claim a milestone complete solely because code was generated, compiled, or its happy-path demonstration succeeded.

Recommended location for this file inside the existing repository: `ai-instructions/FREECAD_PLUS_DEVELOPMENT_ROADMAP.md`. Preserve any established equivalent structure instead of duplicating it.

## 3. Product contracts to establish before broad implementation

These are intended product semantics, not mandates for particular C++ classes. P0–P2 must determine which existing FreeCAD facilities can implement them and where extensions are actually necessary.

| Concept | Required behavior | Why it must be decided early |
| --- | --- | --- |
| Part definition | One reusable definition may contain sketches, datums, solid/sheet bodies, modeling features, and child component occurrences. A part does not require conversion to a different object type to become an assembly. | Ownership, navigation, serialization, and edit context depend on it. |
| Component occurrence | References a part definition and owns its placement and permitted local overrides. It does not silently become an independent geometry copy. | Instancing, assembly constraints, replacement, and BOMs depend on it. |
| Part feature history | Features belong to the part and select explicit input geometry and target bodies. They are not required to live inside a single PartDesign Body history. | Every modeling command and dependency traversal depends on it. |
| Body result | A solid or sheet result with tracked identity and feature provenance; one feature can create, modify, split, or combine bodies. | Selection, history, references, and regeneration depend on it. |
| Geometry creation | Default is New Body. A feature can instead Unite/Add, Subtract, or Intersect with explicitly selected valid targets. | Avoids rebuilding individual command assumptions later. |
| Shared editing | Editing a part definition through any occurrence changes that definition. All occurrences update when their owning documents are recomputed/reloaded under the defined update policy. | Prevents unexpected divergence of supposedly identical parts. |
| Local editing | Placement and declared occurrence overrides affect only that occurrence. Independent geometry requires an explicit Make Unique action. | Prevents accidental global changes. |
| Assembly feature | An assembly-owned operation can affect chosen occurrences without silently rewriting their source definitions. Source propagation, if supported, is explicit. | Assembly cuts otherwise corrupt shared-instance semantics. |
| Work context | Work part is the destination for edits; displayed part/assembly is the viewing context. Show both clearly. | Prevents features being created in the wrong definition. |
| Reference set | Entire Part, Model, Empty, or a custom named geometry/datum subset chosen for an occurrence. | Representation must not be confused with part identity. |
| Load state | Fully loaded, lightweight, or unloaded, independent of reference set. | Large-assembly behavior must not overload visibility semantics. |
| Reference-only role | A separate component usage/BOM attribute, independent of reference set, visibility, and loading. | A hidden component is not automatically excluded from product structure. |
| Persistence | Versioned data, preserved identifiers, explicit external references, predictable migration and unsupported-feature handling. | New model semantics must survive file operations. |

### Modeling details

- Distinguish the generated tool volume from the final body result. New Body retains an independent result; Unite need not leave a redundant persistent tool body. Offer explicit Keep Tools where appropriate.
- For Unite, validate that the chosen result is geometrically valid. Intersection alone is insufficient if it creates a non-manifold result; report the problem and preserve the prior model.
- Selected targets must be stored explicitly. Do not make recompute depend on whichever body happens to be active or visible later.
- Define deterministic ordering for multi-target operations, output-body ordering, and split/merge identity. Never silently redirect an ambiguous reference to a different face or body.
- One part can exist in more than one document context. Define the logical relationship between a part definition and an `.FCStd` document; do not assume they are the same concept.
- Local definition edits should update loaded dependents. Changes to closed external documents need a documented reload/update policy, not a promise of background synchronization.
- All feature transactions include parameter changes, reference changes, generated outputs, and selection/visibility restoration needed for correct cancellation and undo.
- Reference sets initially govern exposed representation. Establish explicit rules for whether a command may resolve geometry outside that set, and require a deliberate scope change when necessary.
- Keep configuration, assembly arrangement, visibility, suppression, reference-set selection, and load state distinct, even if a UI combines their controls.

## 4. Prioritization: utility, difficulty, feasibility, time, and criticality

Do not collapse these factors into one misleading numerical score. Apply dependency gates first, then compare useful work that is actually unblocked.

| Factor | Scale | Meaning |
| --- | --- | --- |
| Utility (U) | 1–5 | Frequency and breadth of user benefit; 5 affects routine modeling. |
| Difficulty (D) | 1–5 | Technical implementation and validation difficulty; 5 includes substantial geometry/solver or cross-document complexity. |
| Feasibility (F) | High / Medium / Unknown | Confidence that existing technology can meet the bounded requirement. A spike can change this assessment. |
| Architectural criticality (C) | 0–3 | 0: isolated presentation; 1: local feature contract; 2: shared subsystem; 3: ownership, identity, persistence, or dependency semantics with broad ripple effects. |
| Effort | XS / S / M / L / XL | Initial hands-on engineering effort bands below, not elapsed Codex runtime. |

**High difficulty does not itself imply high criticality.** An advanced surface algorithm can be isolated and deferred; a modest identity or selection API decision can affect nearly every future command.

### Effort bands and uncertainty

| Band | Preliminary engineering effort | Planning treatment |
| --- | --- | --- |
| XS | 2–8 hours | Small isolated change with clear existing support. |
| S | 8–24 hours | Bounded workflow or integration change. |
| M | 24–80 hours | Several interacting components and meaningful regression coverage. |
| L | 80–240 hours | Significant subsystem work or migration. |
| XL | More than 240 hours; upper bound unresolved | Split into research spikes and separately estimated deliverables. |

These are deliberately rough planning hypotheses for an engineer working with Codex. They include implementation, review, debugging, and required validation; machine-only build/test waiting time is separate. Repository state, experience with FreeCAD, and geometric edge cases can move an item several bands. Pro 20× usage is not a productivity multiplier or completion guarantee.

Do not sum broad inventory rows into a project completion promise: they overlap, and XL items are not bounded. After the first three completed milestones, record estimated versus actual effort and revise the remaining ranges. Convert to calendar time only after the owner supplies available engineering/review hours and the actual build/test bottlenecks are measured.

### Scheduling rules

1. Restore or establish a trusted build before product changes.
2. Investigate C3 questions before implementing broad dependents; investigate C2 contracts before adding many consumers.
3. Deliver the minimum proven foundation, not every possible future capability.
4. Among unblocked tasks, favor high utility, existing backend reuse, and short validation loops.
5. Time-box uncertainty research. A spike ends with evidence, a prototype, options, and an updated estimate, even if the feature remains infeasible.
6. Keep an independent feature track only where its interfaces are stable. Do not create two incompatible implementations of the same model semantics.
7. Fix regressions in a completed gate before building more work on it. Independent documentation or isolated UI work may continue if it cannot hide the failure.
8. Revisit feasibility before attempting a kernel replacement, broad solver rewrite, or full native-file migration. None is an assumed prerequisite.

Break each phase into tasks with an initial target of roughly 4–16 engineering hours and one demonstrable acceptance result. This is a decomposition aid, not a deadline: larger changes need explicit substeps and checkpoints. Define each task's prerequisite API/decision IDs so dependencies remain actionable as the code evolves.

### Delivery order and dependencies

| Phase | Purpose | Entry dependency | Effort outlook |
| --- | --- | --- | --- |
| P0 | Inventory and stabilize the existing fork | Existing FreeCAD-Plus checkout | M, adjusted for existing build health |
| P1 | Decide and probe the high-ripple contracts | P0 | M–L |
| P2 | Prove a minimal end-to-end model architecture | P1 | L; reassess if XL |
| P3 | Harden coexistence, persistence, and service interfaces | P2 | L–XL |
| P4 | Deliver the coherent everyday modeling UI | Relevant P3 contracts stable | L across multiple increments |
| P5 | Improve sketching and reference workflows | P3 selection/reference contracts; P4 integration | L across multiple increments |
| P6 | Expand assemblies and interpart modeling | P3 and core P4 workflows | L–XL |
| P7 | Expand solids, curves, and surfaces | P3 feature/result contracts; P5 references as needed | XL portfolio; estimate features individually |
| P8 | Deliver direct-mesh CAM incrementally | P0 CAM audit, P1 geometry contracts, stable required P3 APIs | L–XL |
| P9 | Add downstream productivity modules | Relevant P3/P6/P7 contracts only | XL portfolio; optional release increments |
| P10 | Release hardening and upstream maintenance | Runs throughout; each release has its own gate | Budget from measured maintenance work |

P4 selection conventions can be prototyped after P1 behind adapters. P5 improvements that are genuinely independent can also advance earlier. P8 does not wait for all advanced surfacing. P10 is continuous, not postponed until the end. All production features migrate onto the shared contracts when those contracts become stable.

## 5. Phase instructions and acceptance gates

### P0 — Establish the actual FreeCAD-Plus baseline

**Goal:** Start from what the owner already built, with a trustworthy development loop.

Actions:

1. Identify the repository, current branch/commit, remotes, upstream base, local modifications, submodules, applicable agent instructions, and existing fork-specific features.
2. Preserve dirty work and existing history. Use a task branch according to repository conventions; never reset, force-push, discard, or overwrite unrelated changes.
3. Reproduce the existing build and application launch on the owner's development platform. Record exact working commands and dependencies instead of copying unverified commands from this roadmap.
4. Locate the actual implementations for document objects, Part/PartDesign features, links, assembly, Sketcher, selection, undo, persistence, and CAM. Record paths and symbols in the Programming Roadmap.
5. Build a capability inventory: upstream capability, fork behavior, limitation, proposed adaptation, relevant source path, validation evidence.
6. Specifically verify existing auto constraints, projection/intersection, transforms, App::Link, multi-solid behavior, selection disambiguation, feature suppression/reordering, and mesh CAM support. Do not mark documented functionality as adequate without checking behavior.
7. Run the relevant baseline tests. Record existing failures separately from new regressions and establish a small deterministic fixture corpus.
8. Record build time, representative recompute time, memory, and assembly interaction behavior on named hardware and fixture sizes.

**Gate G0:** A known commit builds and launches; baseline failures are documented; fork changes are inventoried; reproducible build/test commands exist; the Programming Roadmap points to real code. If the build is blocked, repair or document the concrete blocker before implementing broad CAD changes.

### P1 — Settle the contracts that would otherwise cause rework

**Goal:** Reduce architectural uncertainty without committing to a wholesale replacement.

Create concise architecture decision records for:

- Definition/occurrence ownership and how a part definition maps to documents.
- Part-level feature execution, body results, target selection, and split/merge provenance.
- Reference identity, topology tracking, published interfaces, and cross-document update rules.
- Assembly-local results versus source-part edits, including the scope of assembly features.
- Work/display context, occurrence paths, and selection scope.
- Persistence versioning, legacy coexistence, migration, and unsupported-feature behavior.
- Reference sets, load states, configuration/arrangement identity, and BOM role separation.
- Common feature command lifecycle, undo transactions, cancellation, and error reporting.

For each decision, compare reuse/extension of existing facilities with a new abstraction. Identify actual dependency boundaries and integration costs. Prefer adapters over invasive changes where they meet the requirements; do not preserve an incompatible design solely to avoid touching core code.

Run narrow spikes for the highest-risk assumptions. Initial spike budget: 8–24 engineering hours per question, revised when evidence warrants it. Suggested probes: a reusable part with both geometry and children; a part-owned feature with explicit targets; persistence of occurrence paths; a linked instance referencing a historical body result.

Define the expected semantics first, then test whether existing `App::Part`, `App::Link`, document properties, feature machinery, and geometry APIs can support them. Class names are investigation leads, not prescribed replacements.

**Gate G1:** The principal contracts are recorded with tests/prototype evidence, alternatives, and consequences. Any unresolved C3 issue names exactly which dependent work is blocked. The agent must not portray an unresolved identity or persistence design as a stable API.

### P2 — Build the minimum architecture proof

**Goal:** Prove the intended workflow through editing, regeneration, and persistence before broad command migration.

Implement on an isolated branch or behind a feature flag within FreeCAD-Plus:

1. A part definition containing two separately created solid bodies, a sketch/datum, and a child part occurrence.
2. One part-level Extrude feature supporting New Body and explicit Unite/Subtract targets; use existing geometry operations where possible.
3. A second part containing two occurrences of the first part; a third part containing another occurrence of it.
4. Editing a shared dimension through one occurrence updates all loaded occurrences; placements remain independent.
5. Make Unique creates an intentional independent definition with correctly remapped internal references.
6. Minimal Assembly and Feature navigator views reflect structure and work context without assigning ownership through UI grouping.
7. A minimal assembly-owned cut affects one selected occurrence while the source definition and its other occurrences remain unchanged. This is a semantics probe, not the full assembly-feature product.
8. Save/reopen, undo/redo, cancel an invalid operation, rebuild from changed upstream parameters, and resolve an external linked part.
9. Exercise one split/merge case and one missing or ambiguous reference. Report ambiguity rather than binding to unrelated geometry.

Keep UI styling and advanced commands out of this proof. Do not convert the owner's production files in place.

**Gate G2:** The scenario is reproducible in an automated fixture plus an interactive demonstration. Ownership, shared-instance behavior, local assembly effects, history, and persistence agree. A failed proof triggers a revised design or narrower experiment; it does not justify shipping a cosmetic imitation of the requested architecture.

### P3 — Harden shared services and migrate without breaking the fork

**Goal:** Turn the proven design into reusable production contracts while keeping existing documents usable.

Actions:

- Establish one shared implementation of edit context, occurrence resolution, reference resolution, feature input/target collection, transactions, and error reporting.
- Define feature execution inputs, output identities, validation, preview/commit behavior, and dependency invalidation. Geometry work must not depend on UI state.
- Make body changes traceable through history. Store persistent identifiers; mutable tree labels and display ordering are not identifiers.
- Preserve the distinction between an ambiguous reference and a missing reference. Provide replacement UI and show affected dependents.
- Introduce versioned serialization and representative round-trip tests. Save a copy before any explicit conversion and report unsupported legacy cases.
- Keep legacy objects working through their existing behavior or well-defined adapters. Convert a limited supported subset first; do not attempt every old object type in one migration.
- Define Save Copy, Make Unique, component replacement, and project relocation behavior so they cannot accidentally retain or sever shared identity.
- Define Promote Bodies to Part/Component with explicit associative-versus-independent behavior. Productize it after body identity and reference remapping are reliable.
- Establish basic publication/link contracts for interpart geometry and parameters; reject dependency cycles with useful diagnostics.
- Keep configuration/arrangement schema extensible without implementing the whole feature immediately. Reserve concepts and validation rules rather than speculative unused frameworks.
- Document which files containing fork-only features upstream FreeCAD can read, display, edit, or cannot support. Export is a separate compatibility path and must disclose loss of parametric history.

**Gate G3:** Prototype and legacy fixture subsets pass round-trip, dependency, cancellation, and undo tests. Common contracts are available to command developers; schema/API changes are recorded. At least one ordinary upstream document still opens and edits correctly, and unsupported cases are explicit.

**First architectural release:** Publishable only when G0–G3 pass and its limitations are documented. It may expose an experimental modeling mode while preserving the established workflow.

### P4 — Deliver the everyday modeling workflow

**Goal:** A useful, coherent UI built on the new contracts, not another disconnected workbench.

Implement in this order:

1. Assembly Navigator and Feature Navigator tabs, optional simultaneous docking, explicit work/display context, search, and synchronized viewport highlighting.
2. A shared selection policy: plain click replaces selection; Ctrl toggles/adds entities; Shift provides the documented range/extension behavior. In Sketcher, accumulating separate picks requires a modifier. Window selection can still select a group in one gesture. Choose nonconflicting shortcuts for temporarily disabling auto constraints.
3. Selection filters/scope, Select Other, tangent/connected-chain rules, window/crossing selection, temporary isolate/hide, and restored visibility state.
4. Unified Extrude and Revolve interfaces, with New Body/Add/Subtract/Intersect, explicit targets, common extent controls, live previews, and exact numeric input. Map Pad/Pocket and Revolution/Groove terminology to these commands. Preserve legacy feature editing until migration supports it.
5. A consistent command lifecycle: preselection or postselection, labeled input collectors, preview, Apply, OK, Cancel, and meaningful errors. Start with two commands and extract only demonstrated shared behavior.
6. Move/Copy UI: point-to-point, translation, rotation, axis/coordinate-system alignment, movable triad, global/local coordinates, and snapping. Distinguish a one-time move from creating a persistent assembly relationship.
7. Feature filtering by contributing body, folders/comments, dependency highlighting, status columns, command search/aliases, shortcut palette, and navigation presets.
8. Safe rollback/insertion/reordering supported by the dependency graph; show why an invalid reorder is rejected. Do not implement arbitrary tree dragging as unconditional feature reordering.

For early prototypes, a unified dialog may dispatch to existing backend feature types. Label this internally as a UI adapter; it is not evidence that part-level history or conversion between operation types is complete.

**Gate G4:** Complete a simple part and assembly through the new workflow; edit operation modes; move an instance precisely; recover from invalid input; save/reopen. The interface consistently identifies work context and targets. Compare clicks and task completion with the baseline using the same task, and verify legacy commands still work where retained.

**First broadly useful release:** G4 plus a selected P5 sketch increment; do not wait for the entire advanced-feature inventory.

### P5 — Improve sketching and geometric references

**Goal:** Fast, predictable sketching with immediate feedback and repairable relationships.

Prioritize existing capability improvements before adding solver complexity:

- Audit and improve automatic coincidence, horizontal/vertical, parallel, perpendicular, tangent, and equal inference; expose supported choices and predictable thresholds.
- Preview inferred constraints before commitment; support temporary inference suppression and per-sketch preferences without conflicting with multiselection modifiers.
- Show a cursor-adjacent palette of valid suggested constraints after selection. Provide a stable pointer corridor/dismissal delay so moving toward the palette does not make it disappear. Add keyboard access and an option to disable it.
- Unify dimension selection and direct numeric entry while drawing. Distinguish driving dimensions from reference measurements.
- Visualize remaining degrees of freedom and conflicting/redundant constraints; explain candidate repairs and preserve user intent.
- Integrate external projection and true plane intersections: curve/plane intersections produce points; face/plane intersections generally produce curves, not necessarily straight lines. Define coplanar, tangent, disjoint, and multiple-result behavior.
- Support associative external references across the approved scopes, with source highlighting and deliberate projected-versus-intersected selection.
- Add region selection, gap/duplicate/self-intersection detection, and trim/extend improvements where missing.
- Later increments: constraint-preserving copy/paste, blocks, reusable profiles, and sketch patterns.

**Gate G5:** Test both intended automatic constraints and cases where none should be added. Invalid suggestions are never silently committed. Underconstrained movement remains understandable; redundancy does not corrupt the sketch. External-reference changes update or fail explicitly. Verify the palette with dense sketches, different zoom/DPI settings, keyboard use, and pointer dismissal.

### P6 — Mature assemblies, reference sets, and interpart modeling

**Goal:** Reusable components and dependable in-context design without unintended source changes.

Delivery sequence:

1. Productize shared-definition editing, occurrence overrides, Make Unique, replacement, and multiple-assembly reuse from P2/P3.
2. Entire Part/Model/Empty/custom reference sets; expose load state, suppression, and reference-only role separately.
3. Contextual mates/joints, grounding, degrees-of-freedom display, joint limits, and conflict diagnostics using the existing assembly solver where feasible.
4. In-context editing with occurrence-path-aware selections, source highlighting, and published interfaces for linked datums/geometry/parameters.
5. External-reference manager with source state, update/freeze/break-link behavior, missing-path repair, and cycle diagnostics.
6. Assembly-owned cuts and other bounded operations with explicit occurrence scope. Provide a separate explicit action for source-definition modification.
7. Component patterns and mirrors with skipped instances and declared shared/unique behavior; exploded views, arrangements, and simple motion.
8. Configurations and flexible subassembly behavior only after identity, parameter scope, solver context, and persistence are validated. Do not treat flexible subassemblies as merely different placements of a shared rigid result.
9. Lightweight/partial loading and simplified representations after measurement identifies bottlenecks. Define full-geometry resolution for commands that require it.

**Gate G6:** A nested multi-file assembly demonstrates duplicate parts, replacements, reference-set switching, in-context references, relocation repair, and assembly-local cuts. Test both source edits and occurrence edits. Missing/unloaded components remain represented in the assembly structure and cannot be silently omitted from required validation.

### P7 — Add solid, curve, and surface capabilities

**Goal:** Extend modeling depth through independently validated features using the common feature contract.

Default order, subject to measured feasibility and user utility:

1. Solid/sheet trim and split; sew/stitch; basic sheet thickening; extract/project/intersect curves.
2. Consistent sweep/loft operations with section ordering, guide selection, twist controls, and Boolean targets.
3. Through-curves surfaces using guide curves and then curve-network/boundary surfaces with supported positional, tangent, and curvature continuity.
4. Isocline extraction with an explicit direction and angle convention; distinguish it from isoparametric curves and display-only surface analysis.
5. Hole wizard, feature/body patterns and mirrors, shell/draft/rib/web improvements, and fillet/chamfer enhancements.
6. Direct face move/offset/replace/delete-and-heal on a bounded supported class of imported and native geometry.
7. Feature recognition and broader geometric editing only after earlier operations demonstrate robust results.

Create per-feature capability contracts. Examples: closed/open input requirements, supported continuity, tolerances, self-intersection policy, multi-result behavior, target selection, and retained-tool behavior. Reuse available kernel functions and compatible add-ons only after code/API/license compatibility is checked; the presence of a similarly named function does not prove equivalent behavior.

Use focused research spikes for guided surfaces, high-curvature thickening, isocline extraction, and direct-edit healing. Do not schedule a geometry-kernel replacement by default. If the current kernel cannot meet a bounded requirement, record the limitation and compare a restricted feature, isolated alternative algorithm, or explicit deferral.

**Gate G7:** Each feature ships separately with analytic/simple examples, difficult supported examples, known unsupported cases, geometric validity checks, and downstream recompute tests. A surface that looks smooth is not sufficient evidence of the claimed continuity; a thickened shape must meet the stated geometry/tolerance contract.

### P8 — Build a practical direct-STL CAM workflow

**Goal:** Machine mesh geometry directly with a clear setup workflow, reusing the current CAM stack where viable.

This is a separate bounded integration/algorithm track, not dependent on completion of all P7 features. Begin its feasibility spike once geometry access, transforms, and model identity contracts are settled.

1. Prove direct mesh input through a supported existing toolpath algorithm. Record precisely which CAM operations already accept meshes and which assume boundary-representation solids.
2. Handle STL units explicitly because the format does not establish a dependable unit convention; show dimensions and allow deliberate scaling. Validate orientation, normals, bounds, disconnected pieces, and algorithm-specific mesh requirements.
3. Add a setup wizard: model, work coordinate system, stock, tools, boundaries, allowances, tolerance, and output postprocessor.
4. Deliver one validated three-axis finishing strategy and a narrow documented machine/post scope before claiming general STL CAM support.
5. Add roughing and then rest machining as separate deliverables. A finishing drop-cutter path alone does not provide a full stock-aware roughing workflow.
6. Support containment/avoid regions, reusable setups, stale-toolpath detection, progress/cancellation, and large-mesh profiling.
7. Validate simulation, remaining stock, gouges, and tool/holder/fixture clearance to the extent actually implemented. Clearly expose checks that are unavailable.
8. Broaden strategy/tool/post coverage only with representative fixtures. Rotary and simultaneous multi-axis machining are later scope, not implied by three-axis completion.

**Gate G8:** Known geometry produces reproducible paths within documented tolerance, including units and transforms. Toolpaths have been checked through simulation and an independent reference/check where available. Post output is verified for the supported target; simulation is not represented as proof of machine safety. Actual machine motion requires the owner's normal separate operating authorization.

### P9 — Add inspection, documentation, and specialized workflows

Implement high-utility independent modules after the contracts they consume are stable:

- Unified measurement and persistent measurements; interactive/saved sections; interference and minimum-clearance inspection.
- Surface-quality inspection: curvature combs, zebra/reflection lines, continuity and deviation checks.
- Drawing setup, projected/section/detail views, associative dimensions and annotations, and explicit broken-reference repair.
- BOMs, balloons, exploded documentation, materials/mass properties, and reference-only component rules.
- Sheet-metal and weldment/frame workflows, reusable hardware/profile libraries, and configurations integrated with existing compatible modules where practical.
- Project packaging, dependency collection, relocation repair, and explicit exports with reported parametric/metadata losses.

**Gate G9:** Each module is separately releasable and updates correctly when source models change. BOM quantity/identity rules must be tested with repeated instances, unique copies, suppressed/reference-only items, and nested assemblies. Drawing annotation validity must be checked after topology changes.

### P10 — Continuous release hardening and upstream maintenance

Begin in P0 and repeat for every release:

- Maintain a clean upstream relationship, documented integration strategy, and a concise map of fork-specific patches. Review upstream changes before reimplementing equivalent work.
- Keep modifications focused and shared code centralized. Avoid whole-repository formatting churn and unnecessary public API changes.
- Preserve existing build/package behavior on supported platforms; expand platform coverage incrementally rather than claiming it from one local build.
- Profile representative models before optimization. Measure full/incremental build time, regeneration, memory, large-instance rendering, and cancellation responsiveness.
- Add background computation only with explicit thread-safety, document locking, and result-commit rules. Never move document mutation to a worker thread merely to hide UI stalls.
- Verify install/start/open/edit/save/export on release candidates and document migrations, unsupported cases, and known regressions.
- Audit the actual licenses, attribution, redistribution requirements, and dependencies when adding third-party code or preparing distribution. Do not copy proprietary NX/SolidWorks code or assets.
- Keep new features scriptable and deterministic. Expose the same validated core behavior through UI and automation.

**Release gate G10:** The release's promised workflows pass their applicable gates; representative older files and new files round-trip; no unexplained data loss or identity corruption remains; known limitations are stated; build/package and upstream-base information are recorded. Performance regressions are measured and explained rather than inferred from impressions.

## 6. Feature inventory and initial priority assessment

This table is a planning index. Effort covers a bounded first useful implementation, not commercial-CAD parity. Existing features can lower the cost substantially after P0. Ratings are estimates, not findings from the uninspected fork. Keep each row linked to concrete issues/milestones once implementation starts.

| ID | Capability package | U | D | F | C | Effort | First implementation phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A01 | Unified part definition with geometry and child occurrences | 5 | 5 | Medium | 3 | L–XL | P1/P2 |
| A02 | Part-owned history, independent body results, explicit targets | 5 | 5 | Medium | 3 | XL | P1/P2 |
| A03 | Shared instances, occurrence overrides, Make Unique, promote bodies | 5 | 3 | High | 3 | M–L | P2/P3 contracts; P6 product |
| A04 | Work/display context and scoped selection services | 5 | 3 | High | 3 | M–L | P1/P3 |
| A05 | Persistent references, topology provenance, repair | 5 | 5 | Medium | 3 | XL | P1/P3 |
| A06 | Versioned persistence, legacy adapters, migration | 5 | 5 | Medium | 3 | L–XL | P1/P3 |
| A07 | Common feature lifecycle, undo, preview, cancellation | 5 | 4 | High | 2 | L | P2/P3 |
| A08 | Assembly-scoped feature semantics | 4 | 5 | Medium | 3 | L–XL | P2 proof; P6 product |
| U01 | Separate navigators, docking, synchronized highlighting | 5 | 2 | High | 1 | M | P4 |
| U02 | Tree filters, columns, folders, comments, dependency display | 4 | 2 | High | 1 | M | P4 |
| U03 | Unified Extrude and Revolve command interfaces | 5 | 3 | High | 2 | M–L | P4; depends on A02/A07 |
| U04 | Search aliases, shortcut palette, navigation presets | 4 | 2 | High | 0 | S–M | P4; safe prototypes earlier |
| U05 | Multiselection modifiers, filters, Select Other, selection rules | 5 | 3 | High | 2 | M | P4 |
| U06 | Shared extent controls, collectors, interactive handles | 5 | 3 | High | 2 | M–L | P4 |
| U07 | Move/Copy, point-to-point, triad and coordinate alignment | 5 | 3 | High | 2 | M | P4 |
| U08 | Rollback, valid insertion/reorder, suppression | 4 | 4 | Medium | 2 | L | P3 contract; P4 UI |
| S01 | Automatic constraints, previews, inference controls | 5 | 3 | High | 2 | M–L | P5 |
| S02 | Cursor-adjacent suggested-constraint palette | 5 | 2 | High | 1 | S–M | P5; earlier prototype possible |
| S03 | Smart dimensions, driving/reference values, entry while drawing | 5 | 3 | High | 1 | M | P5 |
| S04 | Degrees of freedom, conflict repair, sketch diagnostics | 5 | 4 | Medium | 2 | L | P5 |
| S05 | External projection/intersection points and curves | 5 | 3 | High | 2 | M | P5; existing capability audit first |
| S06 | Regions, trim/extend, constrained copy, blocks and patterns | 4 | 4 | Medium | 2 | L | P5 in separate increments |
| B01 | Entire/Model/Empty/custom reference sets | 5 | 3 | High | 2 | M–L | P3 contract; P6 UI |
| B02 | Joint/mate assistance, grounding, freedom/conflict display | 5 | 4 | Medium | 2 | L | P6 |
| B03 | Published interfaces, geometry links, external-reference manager | 5 | 5 | Medium | 3 | L–XL | P3 contracts; P6 product |
| B04 | Replacement, component patterns/mirrors, explosions and motion | 4 | 4 | High | 2 | L | P6 in separate increments |
| B05 | Configurations, arrangements, flexible subassemblies | 4 | 5 | Medium | 3 | XL | P1 semantics; later P6 increments |
| B06 | Lightweight/partial loading and simplified representations | 4 | 5 | Medium | 3 | L–XL | P1 contracts; measured P6 need |
| G01 | Solid/sheet trim and split | 5 | 3 | High | 1 | M–L | P7 |
| G02 | Thicken sheets, sew/stitch, offset and gap diagnostics | 5 | 4 | Medium | 1 | L | P7 |
| G03 | Sweep/loft and through-curves surfaces with guides | 5 | 5 | Medium | 2 | L–XL | P7 |
| G04 | Curve-network/boundary surfaces and continuity controls | 4 | 5 | Unknown | 2 | XL | P7 after bounded spike |
| G05 | Extract/project/intersect curves; isocline extraction | 4 | 4 | Medium | 1 | M–L | P7; split by operation |
| G06 | Holes, patterns/mirrors, shell/draft/ribs and dress-up tools | 5 | 4 | High | 2 | L–XL | P7 in separate increments |
| G07 | Direct face editing and healing | 4 | 5 | Medium | 2 | XL | Late P7 |
| G08 | Imported-solid feature recognition | 3 | 5 | Unknown | 1 | XL | Late P7 after spike |
| C01 | Direct-STL input and first three-axis finishing workflow | 5 | 4 | Medium | 2 | L | P8 |
| C02 | Stock-aware roughing, rest machining, boundaries | 5 | 5 | Medium | 2 | XL | P8 after C01 |
| C03 | Simulation, collision checks, posts and setup reuse | 5 | 5 | Medium | 2 | L–XL | P8; limited checks from first release |
| I01 | Measurements, mass, sections, interference/clearance | 4 | 3 | High | 1 | M–L | P9; isolated tools may move earlier |
| I02 | Surface quality, continuity, and deviation inspection | 4 | 4 | Medium | 1 | M–L | P7 validation/P9 product |
| D01 | Drawing workflows, associative annotation and repair | 4 | 4 | Medium | 2 | L–XL | P9 |
| D02 | BOM, balloons, exploded documentation | 4 | 3 | High | 2 | M–L | P9 after B01/B04 |
| X01 | Sheet metal, frames/weldments, hardware libraries | 3 | 4 | Medium | 2 | XL | P9 by module |
| X02 | Package/relocate projects, compatibility and export | 5 | 4 | High | 3 | L | P3 contracts/P9 UI |
| X03 | Performance, scripting, packaging, upstream integration | 5 | 4 | High | 2 | Ongoing | P0 onward |

## 7. Validation strategy: verify behavior, not just implementation

Keep a small set of deterministic fixtures that grows with the supported behavior. Avoid duplicating existing upstream tests or adding tests that merely restate implementation details. Isolated cosmetic changes usually need focused visual verification; ownership, references, geometry, CAM, and persistence require behavioral regression coverage.

| Fixture or scenario | Required assertions |
| --- | --- |
| Mixed part | A definition contains geometry and children; navigator grouping does not alter ownership or transform geometry twice. |
| Shared definition | Two occurrences in one assembly and one in another update together; local placements/overrides remain independent. |
| Unique copy | Internal references remap to the new definition; original and copy can diverge deliberately. |
| Feature results | New Body, Unite, Subtract, Intersect, multiple targets, split, and merge produce documented results and identities. |
| Assembly-local operation | One occurrence changes; the source and unselected occurrences do not; save/reopen preserves the distinction. |
| External references | Missing files, renamed/moved projects, unpublished inputs, stale source versions, cycles, and ambiguous topology are surfaced correctly. |
| Persistence/undo | Save/reopen and undo/redo preserve dimensions, dependencies, identities, occurrence paths, and editability. Cancellation removes partial changes. |
| Legacy document | A representative upstream/fork document retains expected behavior; conversion is explicit and unsupported features are reported. |
| Sketch | Underconstraint, redundancy, conflicting inference, external intersections, and modifier selection remain predictable. |
| Surface/solid | Check validity, expected solid/shell counts, volume/area or analytic references, tolerances, continuity where claimed, and downstream edits. |
| Mesh CAM | Verify units, transforms, stock bounds, cutter geometry, boundary compliance, stale state, supported collision checks, and post output. |
| Performance | Compare named fixtures on recorded hardware/build settings; distinguish algorithm, tessellation, graphics, and file-loading cost. |

Numerical expectations must use explicit, scale-appropriate tolerances and units. Do not use one arbitrary global epsilon for every geometry test, raw face numbering as a universal oracle, or screenshot similarity as the only correctness check.

Test hostile but relevant edits: remove a referenced feature, change a sketch enough to split an edge, suppress an upstream operation, replace a component, close/reopen a source document, and change a mesh's placement or units. A graceful and explicit unsupported result is preferable to silently producing different geometry.

For each feature, record the acceptance test, actual result, and limitations. If interactive testing cannot be performed in the available environment, report it as unverified rather than passed. Build success and headless tests do not substitute for validating mouse/keyboard workflows.

## 8. Risk controls and fallback decisions

| Risk | Earliest mitigation | Response if evidence is unfavorable |
| --- | --- | --- |
| Existing fork changes are lost | P0 inventory, history, and baseline | Restore the original work and integrate narrowly; do not restart the fork. |
| New ownership conflicts with current execution | P1 comparison and P2 proof | Revise adapters/data design before migrating commands. |
| New files cannot preserve identity/references | P2/P3 round-trip fixtures | Block dependent release; fix schema/serialization before adding more features. |
| Topology changes redirect references silently | P2 split/merge tests and P3 provenance | Mark ambiguity, retain diagnostic context, require deliberate repair. |
| Legacy support forces duplicate architectures forever | P3 supported-conversion matrix | Migrate bounded feature families; state remaining legacy-only behavior. |
| Temporary UI wrappers become permanent incompatible models | P4 mapping to A02/A07 | Track wrapper retirement explicitly; preserve a single intended execution contract. |
| Surface algorithms cannot meet claimed robustness | P7 bounded spikes and pathological fixtures | Narrow supported inputs or isolate an alternative algorithm; keep limitation visible. |
| STL finishing is mistaken for complete CAM | P8 staged capabilities | Ship a clearly bounded strategy; retain roughing/rest/collision items as incomplete. |
| Large assembly performance obscures correctness | Baseline profiling and instance fixtures | Optimize measured hot spots after semantics pass; do not hide missing components. |
| Upstream changes repeatedly break the fork | P0 patch map and P10 integration cadence | Reduce unnecessary core edits and consolidate extension points based on real use. |
| Roadmap grows faster than delivery | Bounded release slices and effort review | Reorder unblocked work, reduce per-release scope, preserve the remaining backlog. |

Time-box research, not correctness. If a spike exceeds its budget, summarize evidence and re-estimate the next bounded experiment. Do not repeatedly rewrite the same subsystem without a decision record explaining what new evidence changed the approach.

## 9. Repository instruction and progress structure

Use the repository's existing equivalents when present. Keep each fact authoritative in one location; link to it elsewhere.

| File | Role and size discipline |
| --- | --- |
| `AGENTS.md` | Short entry point and repository-wide rules. Reference the Programming Roadmap first; preserve existing instructions. |
| `ai-instructions/PROGRAMMING_ROADMAP.md` | Concise orientation index: schema/object model, real directories, modules, shared services, conventions, build/test commands, and links to detailed decisions. |
| `ai-instructions/FREECAD_PLUS_DEVELOPMENT_ROADMAP.md` | This document: product contracts, priorities, phase gates, and feature inventory. Update when scope or sequencing changes materially. |
| `ai-instructions/DEVELOPMENT_STATUS.md` | Current phase/task, completed gates, concrete blockers, next actions, estimate/actuals, and links to evidence. Keep current state near the top. |
| `docs/architecture/ADR-*.md` | Short architecture decisions with context, options, decision, affected interfaces, compatibility, and evidence. |
| Existing test/fixture directories | Executable specifications and representative models. Follow the repository's layout rather than inventing a duplicate test system. |

The Programming Roadmap should identify, at a high level:

- Definition, occurrence, feature, body-result, reference, transaction, and persistence responsibilities.
- The real source locations for UI commands, model operations, geometry integration, Sketcher, assembly, and CAM.
- Shared services that must be reused instead of reimplemented.
- Supported build/test/run commands and environment prerequisites.
- Feature flags, compatibility boundaries, identifier/unit/tolerance conventions, and external dependency ownership.
- Where to find the current milestone, known limitations, architecture decisions, and regression fixtures.

Suggested `AGENTS.md` reference block, merged into existing instructions rather than replacing the file:

```markdown
## FreeCAD-Plus development

- Read ai-instructions/PROGRAMMING_ROADMAP.md first for project orientation.
- Read ai-instructions/DEVELOPMENT_STATUS.md for the active milestone.
- Follow the applicable phase and gates in ai-instructions/FREECAD_PLUS_DEVELOPMENT_ROADMAP.md.
- Preserve this existing fork, its history, existing features, and unrelated working changes.
- Reuse shared services; prove high-ripple model changes before migrating consumers.
- Keep the Programming Roadmap concise and update it when code organization or contracts change.
```

### Task record template

```markdown
### TASK-ID — Concrete user-visible result

Status: NOT_STARTED | READY | IN_PROGRESS | BLOCKED | VERIFIED | DEFERRED
Roadmap IDs / phase:
Dependencies / applicable ADRs:
Utility / difficulty / feasibility / architectural criticality:
Estimated effort range and confidence:
Scope / explicit exclusions:
Acceptance criteria:
Relevant source paths / shared services:
Validation commands or interactive procedure:
Observed results / evidence:
Actual engineering effort / machine waiting time, if measured:
Compatibility / migration impact:
Remaining limitations / next action:
```

Use `VERIFIED` only after the declared acceptance criteria pass. `DEFERRED` needs a reason, dependency or feasibility evidence, and a reconsideration trigger. Do not silently drop a requested feature or mark a legacy approximation equivalent to the intended behavior.

## 10. Codex implementation rules

1. **Inspect before replacing.** Search the actual repository with `rg` and inspect nearby patterns and tests. Verify both upstream and existing FreeCAD-Plus behavior.
2. **Separate fact from plan.** Label observed functionality, proposed architecture, estimates, and unresolved assumptions distinctly.
3. **Maintain one source of shared behavior.** Centralize selection scope, edit context, occurrence transforms, references, feature execution, units, tolerance policy, and transactions. Avoid duplicate utility layers.
4. **Keep changes bounded.** Finish one coherent task or a tightly related set. Avoid opportunistic refactors, dependency upgrades, broad formatting changes, and invented frameworks.
5. **Use existing implementation languages and extension patterns.** Follow established C++/Python/Qt boundaries discovered in P0. Prototypes may use scripting; production choices follow performance, lifetime, persistence, and API requirements.
6. **Make changes reversible.** Use task branches/checkpoints according to repository conventions. Keep experimental model semantics behind explicit flags until the applicable gate passes.
7. **Do not hide model failures.** Preserve recoverability and report the first failing feature. If showing a last-valid result, mark it stale; do not let CAM or exports silently treat it as current.
8. **Make updates deterministic.** Store explicit inputs/targets and resolved instance paths. Reject dependency cycles and detect stale external inputs.
9. **Validate to the actual risk.** Reuse upstream coverage and add focused behavioral tests for changed semantics. Stop redundant testing once the concrete risks and required gates are covered.
10. **Review the whole change.** Inspect diffs, unintended files, regression results, serialization changes, and documentation consistency before calling work complete.
11. **Track time honestly.** Record measured work where available; do not fabricate elapsed engineering time from token count or assume more subscription usage creates proportional speed.
12. **Keep the project runnable.** If an architectural branch is temporarily incomplete, identify it explicitly; do not merge a known broken workflow into the normal development line.
13. **Respect authorization.** Continue authorized local implementation and validation without repetitive confirmation. Publishing, destructive repository operations, external messages, and machine operation follow the actual owner authorization and environment rules.
14. **Maintain continuity.** End each bounded task with current status, results, remaining issues, and the next unblocked action in the repository. Future sessions must not rely on conversation memory alone.

### Completion report format

Keep owner-facing reports short:

- Result: the workflow now supported.
- Validation: what passed, what remains unverified.
- Impact: any file/API compatibility change or known limitation.
- Progress: completed roadmap IDs/gates and the next unblocked task.

## 11. First execution task for the existing fork

When implementation is authorized in the FreeCAD-Plus repository, start with this bounded assignment:

> Inspect the existing FreeCAD-Plus fork and all applicable agent instructions. Preserve its current changes and history. Establish the actual upstream base, fork-specific modifications, build/run/test commands, and capability inventory for this roadmap. Create or update the concise Programming Roadmap and development status using existing project conventions. Reproduce the baseline build and relevant tests, recording existing failures separately. Identify the minimum P1 experiments needed to prove unified part definitions, occurrences, and part-level feature results. Do not start a new fork or begin broad command migration during this task. Report G0 evidence and the next bounded task; continue already-authorized work when the gate passes.

No FreeCAD-Plus source code was changed or validated while preparing this roadmap. The first implementation agent must establish the baseline instead of assuming any gate has passed.

## 12. Evidence and implementation research references

These sources informed the planning baseline. They do not replace inspection of the selected FreeCAD-Plus commit. Some official FreeCAD documentation mirrors are archived and may omit later improvements; check the corresponding current code and upstream documentation during P0. No exact schedule or feasibility rating in this file is a vendor claim.

- [FreeCAD source repository](https://github.com/FreeCAD/FreeCAD): authoritative upstream code and history for comparison with the existing fork.
- [FreeCAD 1.1 release announcement](https://blog.freecad.org/2026/03/25/freecad-version-1-1-released/): existing interactive controls, selection, assembly, and CAM improvements worth auditing before replacement.
- [FreeCAD Sketcher documentation](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Sketcher_Workbench.md): documented auto constraints, dimensions, external projection, and external intersections.
- [FreeCAD linked-object command](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Std_LinkMake.md): existing links within and across documents; verify exact copy/override behavior in the chosen codebase.
- [FreeCAD CAM Surface documentation](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/CAM_Surface.md): existing surface machining and OpenCAMLib integration; verify supported model inputs and operations directly.
- [OpenCAMLib source](https://github.com/aewallin/opencamlib): reusable CAM algorithms and STL-related examples; not evidence that a complete mesh-CAM workflow already exists in FreeCAD-Plus.
- [SolidWorks sketch relations overview](https://help.solidworks.com/2026/english/SolidWorks/Sldworks/c_Sketch_Relations_Overview.htm): interaction reference for inference, snapping, and automatic relations.
- [Siemens freeform modeling walkthrough](https://blogs.sw.siemens.com/nx-design/freeform-modeling-walk-through/): workflow reference for swept/through-curves surfaces and sewing.
- [Siemens interpart modeling](https://blogs.sw.siemens.com/nx-design/nx-tips-tricks-interpart-modeling-2/): workflow reference for published geometry and expressions.
- [OpenAI guidance for long-running Codex tasks](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex): repository-held plans, bounded milestones, and continuous validation.
