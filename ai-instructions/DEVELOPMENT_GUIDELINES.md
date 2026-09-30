# Development Guidelines — FreeCAD-Plus

Updated: 2026-09-29  
Applies to: the existing FreeCAD-Plus fork and incremental development toward the approved product vision.  
Purpose: practical instructions for Codex and contributors. The market appendix is dated research, not a specification.

## Repository adoption and authority

Adopted from the owner-supplied `DEVELOPMENT_GUIDELINES.md` on 2026-09-29,
with repository path and authority adaptations. These are execution guidelines;
their proposed features are not a claim of implemented behavior or authorization
to execute the entire backlog. Explicit user instructions and the root
[AGENTS.md](../AGENTS.md) boundaries continue to apply.

- [Programming summary](PROGRAMMING_SUMMARY.md) is the existing orientation index.
- [Development roadmap](DEVELOPMENT_ROADMAP.md) alone owns live tasks, priorities,
  completion and evidence. Its [baseline adoption](DEVELOPMENT_ROADMAP.md#planning-baseline-adoption)
  maps the supplied P0-P10 phases onto existing work.
- [Supplied roadmap](archive/FREECAD_PLUS_DEVELOPMENT_ROADMAP.md) is retained as a
  dated planning reference, not a second live status ledger. Its startup assignment,
  suggested filenames and unaudited assumptions do not restart this project.
- [Product specification](PRODUCT_SPEC.md#future-architecture-direction) owns
  intended product contracts and planned creation defaults; the
  [UI specification](UI_UX_SPEC.md) owns interaction details.
- [Development guide](DEVELOPMENT_GUIDE.md) owns verified commands and build policy.
  Reuse completed evidence when applicable; batch costly builds as requested.
  Benchmarking stock FreeCAD does not authorize using or modifying the separately
  installed FreeCAD, or treating it as evidence for this fork.
- `.cadprt` is future native-format direction, not the current file format or a
  completed migration. Establish schema, compatibility and recovery gates before
  changing save behavior. Keep original legacy files intact.
- The owner-adopted version 2 [creation/interaction contracts](PRODUCT_SPEC.md#planned-creation-and-interaction-contracts)
  supersede unconditional New Body defaults. Creation suggestions are visible and
  overridable; saved operations/targets never change through recompute inference.
  Preserve operation-first layout, alias presets and active input collectors.
- Market research and access dates below are the supplied document's assertions,
  not independently reverified during this adoption. Refresh for decisions that
  require current evidence; do not infer commercial success from feature counts.

## 1. How to use this file

1. Read the repository's applicable `AGENTS.md`, then `ai-instructions/PROGRAMMING_SUMMARY.md` as the first project reference for most tasks.
2. Read these guidelines, current development status, and only the relevant sections of `archive/FREECAD_PLUS_DEVELOPMENT_ROADMAP.md` and architectural decision records (ADRs).
3. Treat the development roadmap as the feature/dependency inventory, these guidelines as execution policy, and the programming roadmap as a concise index to the actual code.
4. Update the existing sources of truth when decisions or implementation change. Avoid copying the full backlog into multiple instruction files.
5. Follow explicit user decisions. These guidelines refine execution; they do not authorize replacing the agreed product scope with the agent's preferences.
6. Continue work in the existing fork. Audit its actual branch, upstream base, patches, dependencies, and build before estimating or changing it.

The adopted `.cadprt` policy is the future native engineering-format direction. References to `.FCStd` in the earlier roadmap remain relevant to legacy import and compatibility; they do not require retaining that extension for new native documents.

The current desktop-core plan is free of charge without activation, subscriptions or paid feature gates. Optional future revenue and naming evaluation are not implementation mandates. See the product specification for this contract.

## 2. Product objective and first audience

Deliver a dependable parametric engineering application that makes frequent modeling and editing tasks easier while preserving useful drawing, CAM, FEM, and other FreeCAD workflows.

Use serious hobbyists and small mechanical-design/manufacturing teams as the initial audience hypothesis. Validate their actual work before expanding the first release. Keep the distinction between hobby use, paid commercial use, and design-team size explicit.

Evaluate progress through completed engineering tasks, repeat use, model reliability, and recovery from changes. Do not use the number of implemented commands as the primary success measure.

Draw workflow ideas from NX and SolidWorks while benchmarking accessibility and everyday productivity against Fusion, Onshape, and stock FreeCAD. A competitor's market presence is evidence for studying its users; it is not proof that every interaction should be copied.

## 3. Prioritize criticality without creating a rewrite

**Decide early, prove narrowly, implement incrementally.**

Use the roadmap's utility, difficulty, feasibility, effort, and criticality scales. Criticality means the extent of dependency and data-model consequences, not simply how useful a feature is.

| Decision class | Examples | Required timing |
| --- | --- | --- |
| C3: persistent/core contracts | Part definitions, occurrences, feature ownership, reference identity, transactions, native format | Decide and test a minimal coherent implementation before dependent features |
| C2: shared subsystem behavior | Selection context, command lifecycle, recompute/invalidation, geometry access for workbenches | Establish reusable interfaces before duplicating implementations |
| C1: local behavior | A particular dialog or feature implementation behind stable contracts | Deliver when its dependency and user-value case is ready |
| C0: isolated presentation | Icons, wording, spacing | Bundle with relevant work; avoid blocking architectural proof |

For every proposed change:

- Record the user task improved, current behavior, dependencies, reuse options, uncertainty, and a testable completion condition.
- Resolve prerequisites before comparing value versus effort.
- Prefer the smallest implementation that proves the intended contract.
- Timebox an uncertain technical experiment before committing to a large implementation.
- Keep unrelated rewrites out of the change.
- Move useful UI work forward when its boundaries are stable; do not wait for every future core feature to be implemented.

An early architecture proof should establish shared definitions, occurrence placement, multiple bodies, explicit Boolean targets, part-level history, and save/reopen/undo behavior. Use a narrowly scoped assembly-local operation to test ownership semantics. Full assembly-cut tooling, configurations, advanced surfacing, and large-assembly optimization can follow their roadmap gates.

## 4. Audit and reuse before rebuilding

Classify each requested capability as:

- Already available and usable.
- Available but difficult to discover or inconsistent.
- Available through an upstream component or compatible add-on.
- Partially available and requiring a bounded extension.
- Blocked by a demonstrated architectural or kernel limitation.

Record the relevant code locations and verify behavior with a small example. Do not infer absence from unfamiliar UI terminology.

Inspect `App::Link` and existing assembly infrastructure before designing a replacement instance system. Its documented design already includes shared references and independent placement/visibility [S7]. Verify the current implementation in the fork; historical documentation is not proof that every required behavior is supported.

Separate these concerns in ADRs:

- Geometry calculation.
- Feature/history ownership.
- Document persistence.
- Selection and editing context.
- Workbench consumption of geometry.

A different workflow does not, by itself, establish a need to replace the geometry kernel. Require a reproducible limitation and comparison of alternatives before proposing that change.

## 5. Define the first release through user tasks

Maintain a small benchmark corpus with explicit dimensions, intended relationships, expected outputs, and edit scenarios.

| ID | Representative task | What it should demonstrate |
| --- | --- | --- |
| B01 | Model a dimensioned mounting bracket | Sketch, constraints, Extrude add/cut, fillet, and predictable edits |
| B02 | Model an enclosure with separate lid | Several bodies, shared dimensions, clear ownership, and no accidental merge |
| B03 | Reuse a bracket three times and in another assembly | Shared definition; independent placement; source edits update intended occurrences |
| B04 | Make one occurrence independent | New definition identity; other occurrences remain linked to the original |
| B05 | Move and align components point-to-point | Correct coordinate context, preview, cancellation, and undo |
| B06 | Change an upstream sketch or feature | Downstream update or explicit repair request; no silent attachment to unintended geometry |
| B07 | Produce a dimensioned drawing | Geometry and dimensions update correctly after modeling edits |
| B08 | Create a CAM job from the revised geometry | Correct stock/setup references and visible invalidation of stale toolpaths |
| B09 | Apply FEM material, support, and load to a simple part | Reference behavior, remeshing needs, and stale-result handling remain explicit |
| B10 | Save, reopen, copy, and relocate a linked project | Preserved identity, recoverable dependencies, and understandable missing-file handling |

B08 and B09 initially test compatibility with existing capabilities. They do not require completing new mesh CAM or extending the FEM solver.

For meaningful comparisons, record application version, hardware, model, operator experience, and task definition. Use stock FreeCAD as the mandatory baseline and selected competitors where access permits.

Measure:

- Task completion and output correctness.
- Median completion time over repeated trials.
- User errors and time spent recovering.
- Clicks and context switches as diagnostic measures.
- Recompute time, memory, open/save time, and responsiveness on fixed models.

Set numerical improvement and regression thresholds after measuring the baseline, before declaring a milestone successful. Do not invent performance claims from unmeasured impressions. For unfamiliar software, separate learning time from practiced task performance.

The first useful release should complete a coherent subset of these tasks reliably. Advanced isoclines, sophisticated guided surfaces, feature recognition, and comprehensive mesh CAM are not prerequisites for releasing improvements to everyday modeling.

## 6. Preserve cross-workbench behavior from the beginning

Core ownership changes can affect much more than the modeling viewport.

Add representative drawing, CAM, and FEM consumers to the early architecture proof, and include Draft objects in compatibility coverage where their geometry or references cross the revised boundary.

Validate after source edits, recompute, undo/redo, and save/reopen:

- The intended shape, placement, units, and occurrence context reach each consumer.
- Drawing dimensions remain attached correctly or report unresolved references.
- CAM dependencies invalidate affected toolpaths; stale output cannot appear current.
- FEM supports, loads, materials, meshes, and results retain valid relationships or require explicit repair/recalculation.
- A changed face/edge identity is never silently accepted merely because an index exists.
- Shared-definition edits and assembly-local edits affect the correct scope.

Use shared geometry/reference adapters where practical. Avoid separate ad hoc traversal rules in every workbench.

When an upstream edit makes a reference ambiguous, report it and offer repair. A successful recompute with the wrong engineering meaning is a failure.

## 7. Preserve the requested workflow while testing defaults

Keep capabilities, default choices, and storage implementation distinct.

- Support part-owned history and a part definition containing both geometry and child occurrences.
- Apply the product specification's creation-time New Body/Unite suggestion policy and explicit supported operations. Do not resurrect the superseded unconditional default or infer new intent when editing/recomputing.
- Persist the intended operation and target references; do not resolve targets from whichever body happens to be active when reopening or recomputing.
- A conceptual tool body need not become an unnecessary permanent document object. Choose its representation through the ownership/history ADR.
- Treat full/reference/empty representations separately from suppression, loading, and BOM participation.
- Distinguish editing a shared definition from editing occurrence placement, making a unique copy, or applying an assembly-local operation.

Prototype and measure the requested interaction changes:

| Interaction | Validate |
| --- | --- |
| Separate assembly and feature navigators | Synchronization, active edit context, search, and correct occurrence selection |
| Unified Extrude and Revolve commands | Clear operation mode, target selection, preview, edit, cancel, and undo |
| Modifier-based sketch multiselection | Predictable additive picking, keyboard conventions, box selection, and tool-state behavior |
| Near-cursor constraint suggestions | Reachable targets, delayed dismissal, no accidental activation, keyboard access, and no obstruction of geometry |
| Automatic sketch constraints | Visible inference, user control, redundancy/conflict handling, and easy correction |
| Point-to-point movement | Source/target context, orientation options, preview, and correct local/world transforms |

Do not silently change an explicit user requirement because a different default appears familiar. Record evidence and propose a deliberate adjustment if tests reveal a problem.

## 8. Native format and interoperability

Plan `.cadprt` for new native documents under the future direction; do not change the current reader/writer until its migration gates pass. Treat it as an engineering document container that may include modeling, assemblies, drawings, CAM, FEM, and related data.

The extension is a recognizable label. Compatibility depends on the content contract.

Before broad native-format adoption, specify and test:

- Stable format identity independent of future application branding.
- Schema version and required reader capabilities.
- Persistent definition, occurrence, feature, and reference identities.
- Dependency resolution, units, and supported embedded/external content.
- Safe save behavior, recovery, backups, and migration.
- Rejection or controlled read-only handling of unsupported required content.
- Explicit behavior for Save As, Save Copy, Make Unique, and relocated projects.

A different extension reduces accidental association with stock FreeCAD; it cannot prevent someone from deliberately opening or renaming a file.

Preserve legacy `.FCStd` opening and conversion to `.cadprt` as fully as reasonably
possible, according to the owner's [native-format policy](PRODUCT_SPEC.md#planned-native-format-and-legacy-import).
The owner accepts that conversion may become harder and less complete over time;
maintain best-effort support and document tested coverage rather than promising
perpetual lossless compatibility or freezing the new architecture. Never overwrite
an original legacy file during conversion. Distinguish a lossless native save,
partial conversion, a supported legacy export, and geometry-only recovery/exchange.

Provide a tested exchange path for the first audience. Do not describe STEP geometry exchange as preserving proprietary parametric history. Report meaningful conversion losses, such as unsupported features or relationships.

Keep installer file associations and public format documentation consistent with the implemented reader/writer. Public extension listings are documentation activities, not a substitute for compatibility engineering.

## 9. Make effort estimates evidence-based

The roadmap's effort ranges are initial hypotheses. They are neither deadlines nor promises about autonomous agent runtime.

- Break active work into bounded changes with observable completion conditions.
- Track elapsed engineering effort separately from agent execution time.
- Include debugging, regression repair, integration, documentation, packaging, and review.
- Re-estimate after the first three completed milestones and after significant architectural discoveries.
- Record uncertainty and the next experiment that can reduce it.
- Forecast from observed delivery and remaining dependencies; avoid summing speculative task ranges into a precise release date.
- Reserve capacity for defects and upstream integration, then revise that allocation using actual maintenance effort.

AI assistance can accelerate implementation, but generated code still needs validation against design intent, geometry, persistence, and downstream behavior. Passing a build does not establish engineering correctness.

## 10. Control fork maintenance and release risk

Maintain a record of the upstream base and the reason for each persistent divergence.

Prefer localized adapters, extension points, and separable patches where they can implement the intended behavior. Contribute generally useful fixes upstream when appropriate.

For an architectural change, include:

1. ADR and dependency impact.
2. Minimal implementation.
3. Meaningful behavioral regression cases.
4. Persistence and legacy-compatibility result.
5. Downstream-consumer result.
6. Rollback or migration strategy.
7. Known limits and measured performance impact.

Use automated tests for identity, geometry, transactions, persistence, and regression-prone behavior. Use focused visual/manual verification for low-risk presentation changes; avoid tests that simply restate the implementation.

Protect the user's existing work. Do not claim a feature complete while known data loss, wrong-target edits, silent reference errors, or incorrect stale-result handling remain in its supported workflow.

A release should demonstrate installability and completion of its selected end-to-end tasks. Publish a clear capability boundary. Do not imply NX/SolidWorks parity from a few similarly named commands.

## 11. Validate adoption separately from engineering progress

Recruit representative hobbyists and small teams for task-based trials when that work is authorized. Ask which applications they actually use, what they manufacture, which recurring task fails or takes too long, and what prevents switching.

Record observed repeat use and switching barriers. Distinguish interest, willingness to test, willingness to migrate, and willingness to pay.

Study onboarding, tutorials, sample projects, migration, and support alongside modeling features. These are candidate adoption barriers to validate.

Ondsel's shutdown account reports useful FreeCAD contributions alongside failure to find adoption sufficient for its venture-funded business [S8]. Treat that as evidence that product usefulness and business sustainability are separate questions.

Do not infer commercial viability from a feature list, a distinctive extension, community membership, or compliments.

## 12. Completion record for each development task

Use the existing development-status file. Record concisely:

- User task and intended behavior.
- Changed code and shared interfaces.
- Evidence of correctness and any measured usability improvement.
- Save/reopen, undo/recompute, and downstream checks relevant to the change.
- Compatibility and migration impact.
- Remaining limits, actual effort, and revised estimate.
- Next dependency-ready task.

Keep the programming roadmap short and index-like. Link to detailed design, tests, and research instead of embedding them.

---

## Appendix A. CAD adoption evidence and competitor breakdown

Research checked: 2026-09-29. Historical survey years are retained below.

### A1. Scope and limitations

This appendix concerns parametric mechanical/product CAD used by hobbyists and small businesses. No representative, current census covering both populations was located.

Survey respondents, professional users, paying customers, small design teams, small companies, downloads, and registered accounts are different populations. Their percentages must not be combined into a synthetic market-share chart.

“Professional” does not establish company size. A team of 1–5 designers may work inside a much larger company. A free-license user is not necessarily a hobbyist.

### A2. Quantitative evidence

**CNCCookbook 2024 [S1]:** fewer than 400 production-CAD responses; 51.5% identified as professional CNC users. Overall ranks below include non-parametric/specialist applications in the denominator.

| Parametric application | Published overall position | Reported professional-subset usage |
| --- | ---: | ---: |
| Autodesk Fusion | 1 | 28.8% |
| SolidWorks | 2 | 26.5% |
| FreeCAD | 3 | — |
| Autodesk Inventor | 5 | — |
| Alibre/Geomagic | 6 | — |
| Onshape | — | 1.2% |

These are CNC-reader sample results, not worldwide shares. AutoCAD occupies the omitted fourth position. Missing values mean no value is asserted, not zero usage.

**CNCCookbook 2023 [S2]:** nearly 400 responses; the publisher explicitly identifies Fusion followed by SolidWorks as the leaders in both its hobby and professional segments. This is useful historical hobby-CNC evidence, not a universal maker ranking.

**Onshape/Isurus 2023–2024 [S3]:** 1,466 professional respondents, collected June 23–July 5, 2023; vendor-commissioned research with disclosed recruitment. 45.1% reported teams of 1–5 designers. The report groups SolidWorks, Onshape, Fusion, Solid Edge, and Inventor as its five main systems.

| Application | Its surveyed users on teams of 1–5 designers |
| --- | ---: |
| Fusion | 77.1% |
| Onshape | 55.0% |
| SolidWorks | 41.8% |

This table measures team size within each product's respondents. It does **not** mean 77.1% of small teams use Fusion. The report's five-product comparison assigns SolidWorks 55.7%; do not generalize that denominator to all companies or all 1,466 participants.

**FreeCAD-specific survey [S4]:** 650 respondents recruited through community channels. More than one in five reported having used FreeCAD to make money. This demonstrates commercial use within that sample, without measuring FreeCAD's share of the wider CAD market. The article's download/community-based total-user estimate is not used as an audited active-user count.

### A3. Practical interpretation for each audience

The following is a research-informed competitor shortlist, not an exact popularity ranking. Confidence concerns the adoption inference, not product quality.

| Program | Hobbyist interpretation | Small-business interpretation | Development comparison priority |
| --- | --- | --- | --- |
| Fusion | Strongest leadership evidence in the hobby-CNC data reviewed | Strong candidate for very small teams; integrated design/manufacturing offering [S5] | Primary: sketch-to-part speed, assemblies, drawings, and CAD-to-CAM |
| SolidWorks | Substantial presence in the surveyed hobby-CNC audience; a current Makers offering also exists [S6] | Major established comparator in professional data | Primary: predictable parametric editing, assemblies, drawings, and documentation |
| FreeCAD | Prominent in the mixed CNC sample; relevant existing community | Real commercial use is documented, but broad business share is uncertain | Mandatory baseline: model reliability, compatibility, and improvements to current workflows |
| Onshape | Relevant maker option; broad hobbyist position cannot be ranked from these surveys | Significant small-team relevance in the professional survey | Primary: part/assembly organization, selection, and management of changes |
| Inventor | Broad hobby prevalence unresolved in the reviewed evidence | Included among the main professional systems in the survey | Secondary: conventional mechanical-design and drawing workflows |
| Alibre | Relevant hobby and small-shop candidate | Worth comparing for a focused desktop product; vendor offers hobby and business products [S9] | Secondary: onboarding and a manageable feature set |
| Solid Edge | Broad hobby prevalence unresolved | Included among the main professional systems in the survey | Secondary: editing workflows and mechanical design |
| Shapr3D | Plausible audience overlap; no comparable adoption share located | Plausible small-team overlap; no comparable share located | Selective UI study; supports history-based parametric modeling [S10] |
| OpenSCAD | Relevant to code-driven parametric designs; no comparable share located | Specialized automation/generator use is a comparison hypothesis | Selective: reproducible parameter-driven generation; a different interaction model [S11] |
| NX / Creo / CATIA | Insufficient evidence for a leading hobbyist position | Relevant to specialized suppliers; broad small-business ranking unresolved | NX remains an architectural/workflow reference; avoid making enterprise feature parity the first release goal |

Onshape's current Free plan is for non-commercial, publicly accessible designs [S12]. Fusion's personal-use offering also has eligibility and capability restrictions [S5]. Treat entry cost, privacy, commercial eligibility, and data portability as separate comparison criteria. Check current terms before any purchase or licensing recommendation.

Tinkercad, SketchUp, Blender, Rhino/Grasshopper, and specialist CAM products matter in adjacent workflows. They are not interchangeable with the mainstream sketch/feature-history segment above. Some offer procedural or parametric capabilities; omission from the core comparison is a scope choice, not a claim that they cannot be parametric.

### A4. Implications for FreeCAD-Plus

These are development judgments drawn from the evidence:

1. Prioritize a coherent path from constrained sketch to editable part, reusable component, drawing, and manufacturing output.
2. Use Fusion and SolidWorks as the first external task benchmarks, stock FreeCAD as the baseline, and Onshape as an additional workflow comparator.
3. Preserve NX-inspired architecture where it supports the agreed behavior. Use measured audience needs to order specialized NX-style features.
4. Investigate local/private document ownership and predictable commercial-use terms as potential differentiators. Validate demand; do not assume those qualities alone cause adoption.
5. Give onboarding, export, reference repair, and reliable updates early attention. Test their impact rather than assuming that advanced feature coverage is the principal switching barrier.
6. Keep hobbyist and business test cohorts separate when interpreting results.
7. Refresh this appendix before major targeting or monetization decisions. Do not require web research on every coding task.

### A5. Sources

All links accessed 2026-09-29. Product pages substantiate capabilities or access conditions, not market share.

- **[S1]** CNCCookbook, [2024 CAD Survey](https://www.cnccookbook.com/cnccookbook-2024-cad-survey-market-share-customer-satisfaction/). Self-selected CNC audience; professional subset is not an SMB-only sample.
- **[S2]** CNCCookbook, [2023 CAD Survey](https://www.cnccookbook.com/cnccookbook-2023-cad-survey-market-share-customer-satisfaction/). Historical hobby/pro comparison from the survey publisher.
- **[S3]** Onshape/Isurus, [State of Product Development & Hardware Design 2023–2024](https://www.onshape.com/cdn-files/561abe5f1704f4f516eb42785347f7ea2746dcb9.pdf), especially printed pages 5–6, 12–15, and 51. Vendor sponsorship and sample boundaries are material.
- **[S4]** Ondsel, [FreeCAD user survey results, part 1](https://www.ondsel.com/blog/freecad-user-survey-results-part-1/). Community survey; not a cross-product market census.
- **[S5]** Autodesk, [Fusion personal-use and commercial-product comparison](https://www.autodesk.com/products/fusion-360/personal).
- **[S6]** Dassault Systèmes, [SolidWorks for Makers](https://www.solidworks.com/solution/solidworks-makers).
- **[S7]** Realthunder/Assembly3, [Link design documentation](https://github.com/realthunder/FreeCAD_assembly3/wiki/Link). Historical architecture reference; verify against the fork's code.
- **[S8]** Ondsel, [Shutdown statement](https://www.ondsel.com/blog/goodbye/).
- **[S9]** Alibre, [Product overview](https://www.alibre.com/).
- **[S10]** Shapr3D, [History-based parametric modeling](https://www.shapr3d.com/content-library/shapr3d-history-based-parametric-modeling).
- **[S11]** OpenSCAD, [About](https://openscad.org/about.html).
- **[S12]** Onshape, [Free plan](https://www.onshape.com/en/products/free).
