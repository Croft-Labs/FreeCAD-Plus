# FreeCAD Plus: Development Roadmap

## Owner directive: functional workflows first, then move on

**Standing development priority, explicitly directed by the owner on 2026-09-30.**
Do not get stuck in any phase, section, item family or workflow. Make it sufficiently
functional for the owner to test, then move to another dependency-ready area.
The owner's hands-on workflow testing determines which refinements are actually
needed. Prolonged polishing before that feedback wastes effort when the workflow
is subsequently changed.

- Define a bounded, usable end-to-end outcome before starting a batch. Reach a
  representative working workflow, fix demonstrated blockers to that workflow,
  and run the relevant grouped checks. Do not require exhaustive edge-case closure
  or completion of every subtask before moving on.
- At that checkpoint, record what works, how the owner can test it, and the known
  limitations. Distinguish **ready for owner testing** from **owner accepted** and
  from full specification completion; leave unverified acceptance gates open.
- Then rotate to another authorized, dependency-ready section or item family.
  Do not keep generating successive microtasks, speculative audits, extra polish
  or broader regression campaigns merely because more improvements can be imagined.
- Resume refinement in response to owner testing, a demonstrated blocker, or a
  concrete dependency needed for another authorized workflow. State that reason
  before extending work in the same area. Hypothetical defects are not blockers.
- If a section stalls, record the blocker and move to useful independent work.
  Waiting for owner feedback on one workflow does not stop progress elsewhere.
- Continue batching related tasks before costly builds. This directive governs
  work selection across the roadmap, including F001-F127 and phase 16; it does not
  waive necessary checks for known correctness or data-integrity problems.

## Current focus

- Owner priority (2026-10-01): complete the component/document architecture under
  **7.8**, using the [approved contract](architecture/COMPONENT_DOCUMENT_CONTRACT.md).
  This explicitly supersedes rotation for this work: complete dependency-ready
  component, Model History and `.cadprt` tasks together; retain earlier validation
  evidence and do not resume unrelated polish. Implementation, native build,
  behavioral/GUI validation and publication remain separate gates.

- Bounded checkpoint ready for owner testing: F066 reviewed face extension,
  phase 13 tasks 13.1e/f. The existing Surface Extend Face command now reviews
  U/V percentages, fitting settings and approximation semantics before preview
  and associative creation. Both tasks preceded one grouped native build;
  nineteen distinct checks pass and six final GUI captures are reviewed.
  Full trim/untrim, broad imported/periodic surfaces and physical acceptance remain
  open. [Owner procedure](../tests/ExtendFaceReview.md). Stop here and rotate
  pending owner workflow feedback.

- Bounded checkpoint ready for owner testing: F076 joint motion and limit review,
  phase 12 tasks 12.4c/d. Native joint tasks explain five common joint meanings,
  expose exact reference identities and retain reversed-limit edits for correction
  or Cancel. Both tasks preceded grouped validation; this Python-only batch required
  no native rebuild. Twenty-nine distinct checks pass across accepted runs and six
  GUI captures are reviewed. Full contextual suggestions, motion-envelope previews,
  broader assemblies and physical acceptance remain open. [Owner procedure](../tests/JointReview.md).
  Stop here and rotate pending owner feedback.

- Bounded checkpoint ready for owner testing: F039 window/crossing selection,
  phase 10 tasks 10.5g/h. Left-to-right uses full projected enclosure with a solid
  border; right-to-left crosses with a dashed border. Both tasks preceded one
  grouped build; nineteen distinct checks pass and six captures are reviewed.
  Filters, command gates, hidden objects, Ctrl-add, Escape and Box Zoom pass.
  Full F039 remains open, including broad sketch/curve coverage and the recorded
  nested BRep flag observation. [Owner procedure](../tests/WindowSelection.md).
  Stop here and rotate pending owner feedback.

- Previous bounded checkpoint ready for owner testing: F059 native shell Thickness,
  phase 13 tasks 13.5g/h. Removed-face review, signed-side controls, expression
  preservation and recoverable failed acceptance pass. Both tasks preceded a
  grouped build; one corrective build fixed a demonstrated preview-status label.
  Sixteen distinct checks pass and six final captures are reviewed; Undo/Redo,
  save/reopen and downstream source edits pass. Full F059 stays open, including
  oversized inward offsets. [Owner procedure](../tests/ShellThickness.md).
  Stop at this usable checkpoint and rotate pending owner feedback.

- Previous bounded checkpoint ready for owner testing: F050 native sketch Trim gestures,
  phase 11 tasks 11.6e/f. One drag is one Undo step; unfinished gestures roll back,
  and the task reports native removed/replaced-constraint identities. Both tasks
  preceded the grouped build; a corrective build fixed demonstrated notice clipping
  and clarified replacement semantics. Twelve distinct selected checks pass, five
  final captures are reviewed, and save/reopen passes. Full F050 remains open.
  [Owner procedure](../tests/TrimGesture.md). Rotate pending owner feedback.

- Previous bounded checkpoint ready for owner testing: F058 fillet/chamfer
  recovery, phase 13 tasks 13.5e/f. Invalid acceptance keeps checked edges for
  correction and rolls back geometry; copied kernel inputs preserve sources.
  Both tasks preceded one grouped build; 16 distinct selected checks pass and
  six captures are reviewed. Full F058 remains open for tangent-chain controls,
  live previews, corners, exact failure localization and physical acceptance.
  [Owner procedure](../tests/EdgeTreatmentRecovery.md). Rotate pending owner feedback.

- Previous bounded checkpoint ready for owner testing: F035 entity selection
  filters, phase 10 tasks 10.5e/f. Native vertex/edge/face/whole-object policy
  intersects command gates and has visible reset/Close/Escape recovery. Both tasks
  preceded one grouped build, followed by one startup-registration correction;
  17 distinct selected checks pass and five captures are reviewed. Full F035 stays
  open for separate object categories, broader picking
  and physical acceptance. [Owner procedure](../tests/EntitySelectionFilter.md).
  Stop at this functional checkpoint and rotate pending owner feedback.

- Previous bounded checkpoint: F055 Hole specification review, phase 13 tasks
  13.5c/d. Profile/Body identity, location readiness and distinct thread result
  explanations are implemented. One grouped build passed; 17 bounded selected
  checks pass. **13.5d remains open:** deferred modeled-thread acceptance waits,
  and counterbore Redo after recompute changes volume. Preserve these findings and
  rotate instead of extending this workflow before owner feedback.
  [Owner procedure and limits](../tests/HoleSpecification.md).

- Previous product batch complete for owner testing: F108 saved project packaging,
  phase 15 tasks 15.6a/b. Tools > Package saved project reviews recursive relative
  native links and creates a byte-preserving portable ZIP. A nested assembly opens
  and updates after its original folder becomes unavailable. Both tasks preceded
  one native build; all 15 distinct selected checks pass and six captures are
  reviewed. [Owner procedure](../tests/ProjectPackage.md). Full F108 stays open for
  broader assets, relinking and independent duplication; rotate pending owner tests.

- Previous product batch complete for owner testing: F028 captured Sweep inputs,
  phase 13 tasks 13.2c/d. The native collector retains its path through later
  profile/global selection, reviews ordered sections/output and recovers failed
  creation without changing source topology. Both tasks preceded the grouped build;
  a demonstrated kernel input mutation was fixed in one corrective rebuild.
  All 16 distinct selected checks pass; six captures are reviewed and four owner
  fixtures saved. [Owner procedure](../tests/SweepInputs.md).
  Full F028 remains open; rotate after this usable checkpoint pending owner feedback.

- Previous product batch complete for owner testing: F013 native state columns, phase 10 tasks 10.6d/e.
  The existing feature organizer distinguishes visibility, suppression, native
  error/recompute, source and metadata access. Read-only filtering/column choices
  and change invalidation pass in 14 grouped checks after one staging pass and a
  narrow Python observer correction. Seven final captures are reviewed.
  [Owner procedure](../tests/FeatureStateColumns.md). Full F013 remains open; stop
  at this bounded inspection workflow and rotate pending owner feedback.

- Previous product batch complete for owner testing: F090 CAM model setup review, phase 14 tasks 14.1c/d.
  Exact source identity and repeated counts, separate mesh candidates and source
  size/unit review are implemented. Both tasks preceded one script-staging pass;
  all 16 distinct selected checks pass and six final captures are reviewed.
  [Owner procedure](../tests/JobModelReview.md). Stop at this bounded workflow and
  rotate pending owner feedback; the complete guided CAM wizard remains open.

- Previous product batch complete for owner testing: F063 ordered open-section Loft,
  phase 13 tasks 13.2a/b. Native open wires/single edges are selectable, section order
  and output modes are explicit, and invalid creation rolls back for correction.
  Both tasks preceded the grouped build; all 17 selected checks pass. Capture review
  found a misleading solid-output error detail, corrected in one incremental rebuild.
  Eight affected checks pass again and five final captures are reviewed. [Owner procedure](../tests/LoftSections.md). Full F063 stays open; rotate
  after this usable checkpoint pending owner testing.

- Previous product batch complete for owner testing: F077 assembly freedom guidance,
  phase 12 tasks 12.4a/b. Native solver messages explain the assembly-wide count;
  grounded/unconnected selection distinguishes connectivity from slider/hinge freedom.
  Contextual panel attachment/lifecycle is repaired. Both tasks preceded a grouped
  build; runtime evidence justified one corrective build. Twenty-eight distinct
  selected checks pass. Five native GUI captures were reviewed. [Owner procedure](../tests/AssemblyFreedom.md).
  Full F077 remains open; rotate pending workflow feedback.

- Previous product batch complete for owner testing: F103 associative dimension
  repair, phase 15 tasks 15.3c/d. Native reference review distinguishes projected
  and true geometry, clears obsolete 3D references and validates before committing.
  Failed repairs restore the original dimension and remain open for correction.
  One grouped build and 14 distinct selected checks pass. Five native task captures were reviewed.
  [Owner procedure](../tests/DimensionRepair.md). Full F103 remains open; rotate
  after this bounded checkpoint pending owner workflow feedback.

- Previous product batch complete for owner testing: F072 shared-definition Copy,
  phase 10 tasks 10.7c/d. Tools > Move or copy occurrence now offers explicit Move
  and Copy actions using the same preview and coordinate frames. Copy creates one
  new native Link in the same structural container and preserves the original.
  Both tasks preceded one grouped script-staging pass; 25 selected checks pass and
  five captures were reviewed. [Owner procedure](../tests/OccurrenceMove.md).
  Point picking/alignment, independent definitions and broader F072 acceptance stay
  open. Stop at this workflow checkpoint and rotate for owner feedback.

- Previous product batch complete for owner testing: F047 sketch freedom guidance,
  phase 11 tasks 11.4c/d. The existing sketch solver task explains remaining freedom,
  fixed/reference semantics and failed states, with a visible native selection
  button gated by successful underconstrained solves. Both tasks preceded a grouped
  build; a compile correction was followed by one successful incremental build.
  Fifteen distinct selected checks pass and five captures were reviewed.
  [Owner procedure](../tests/SketchFreedom.md). Full F047 remains open for movement
  directions, richer per-entity diagnosis and physical acceptance. Stop and rotate.

- Previous product batch complete for owner testing: F095 CAM Simulator input review,
  phase 14 tasks 14.3a/b. The existing OpenGL task shows selected operation order,
  stock dimensions, cutters, quality and explicit coverage limits. Complete input
  preparation precedes native reset; edits invalidate review and conflicting tool
  numbers/missing cutters are refused. Both tasks preceded one grouped script
  staging pass. 17 distinct selected checks pass across accepted suites, including
  native simulator startup; five captures were reviewed.
  [Owner procedure](../tests/SimulationReview.md). Full F095 stays open for removal
  accuracy, collision classification and physical acceptance. Stop and rotate.

- Previous product batch complete for owner testing: F069 intersection curves,
  phase 13 tasks 13.4a/b. Part > Review intersection curves captures explicit whole
  root shapes/Bodies, previews native Section on isolated copies and creates an
  associative result in one transaction. Empty results and changed inputs prevent
  creation; sources retain visibility, geometry and Body Tips. Both tasks preceded
  one grouped build. 18 distinct selected checks pass across accepted suites;
  six native captures were reviewed. [Owner procedure](../tests/SectionReview.md).
  Full F069 remains open for extraction/projection, wider references and physical
  acceptance. Stop at this usable checkpoint and rotate.

- Previous product batch complete for owner testing: F080 saved exploded-view output,
  phase 12 tasks 12.7a/b. Existing native steps now produce drawing geometry that
  preserves occurrence/definition and structural-parent transforms. Successive
  trails follow preceding moves; radial preview and output use the same frame.
  Both tasks preceded one grouped script-staging pass. 28 distinct selected checks
  pass across accepted suites; five final captures were reviewed.
  [Owner procedure](../tests/ExplodedViewOutput.md). Full F080 stays open for joint
  motion, broader arrangements/consumers and physical acceptance. Stop and rotate.

- Previous product batch complete for owner testing: F096 setup reuse, phase 14
  tasks 14.4a/b. Existing CAM templates now carry name/revision/units, preflight
  known compatibility failures and show stored/default settings in New Job.
  Accepted settings are captured exactly; native tools, stock and setup objects
  remain editable and independent. Both tasks preceded one grouped staging pass;
  16 distinct selected checks pass and six final captures were reviewed.
  [Owner procedure](../tests/SetupTemplates.md). Full F096 remains open for operation
  sequences, wider compatibility/remapping and physical acceptance. Stop and rotate.

- Previous product batch complete for owner testing: F067 sheet thickening, phase
  13 tasks 13.1c/d. Existing 3D Offset now explains signed one-sided thickness,
  reverses numeric direction, distinguishes sheets from solids, preserves sources
  during kernel work and keeps failed acceptance recoverable. Both tasks preceded
  the grouped build; demonstrated failures were fixed before the final pass.
  Seventeen distinct selected checks pass and six native captures were reviewed.
  [Owner procedure](../tests/SheetThickening.md). Symmetric thickness, Boolean targets
  and full F067 remain open. Stop here and rotate for owner feedback.

- Previous product batch complete for owner testing: F048 constraint repair, phase
  11 tasks 11.4a/b. Sketch > Review constraint repair diagnoses an isolated native
  copy and previews checked constraint deactivation, then applies a successful
  choice in one Undo step while retaining constraint numbers/names/values.
  Both tasks preceded one grouped build; 15 distinct selected checks pass and six
  final captures were reviewed. [Owner procedure](../tests/ConstraintRepair.md).
  Free root sketches only; full F048 remains open for broader repair/physical
  acceptance. Stop here and rotate.

- Previous product batch complete for owner testing: F037 Select Other, phase 10
  tasks 10.5c/d. The existing Clarify Selection command now preserves equal-label
  objects and full repeated-occurrence paths, labels their context, and respects
  native command selection gates through hover and acceptance. Both tasks preceded
  one native build; all 16 selected checks pass and five captures were reviewed.
  [Owner procedure](../tests/ClarifySelection.md). Full F037 remains open for broader
  live-topology and physical/high-DPI acceptance. Stop here and rotate.

- Previous product batch complete for owner testing: F071 sampled face deviation,
  phase 15 tasks 15.2a/b. Part > Sampled face deviation compares two explicit faces
  using native unsigned point-to-face distances and a temporary color map. Sampling,
  mm scale, trimmed-out/failed counts and non-certification limits are visible;
  saved settings do not create geometry. Both tasks preceded one grouped build;
  all 16 selected checks pass and six captures were reviewed.
  [Owner procedure](../tests/SurfaceDeviation.md). Full F071 remains open for zebra,
  combs, continuity and broader deviation/physical acceptance. Stop here and rotate.

- Previous product batch complete for owner testing: F022 single-occurrence source
  replacement, phase 12 tasks 12.6a/b. Tools > Replace occurrence source reuses a
  same-document root solid/Body while preserving one free Link's identity, placement,
  visibility and uniform appearance policy. Preview reuses the existing overlay;
  consumers/relationships are refused. Both tasks preceded one native build;
  22 distinct selected checks pass across accepted suites and five captures were
  reviewed. [Owner procedure](../tests/OccurrenceReplace.md). Full F022 remains open
  for mate/interface remapping and broader replacement scope. Stop here and rotate.
  Item-level bookkeeping also corrected: the prior Make Unique pilot belongs under
  F019, not F008. Body promotion F008 remains unimplemented by that pilot.

- Previous product batch complete for owner testing: F068 sewing tolerance and Shape
  Builder diagnostics, phase 13 tasks 13.1a/b. Native sewing now honors its supplied
  tolerance. Existing shell/solid modes expose computed classification/free-boundary
  reports and refuse open-shell solid creation while preserving sources. Both tasks
  preceded one native build; 22 distinct selected checks pass across accepted suites
  and six settled captures were reviewed. [Owner procedure](../tests/ShapeSewing.md).
  Full F068 remains open for associative sewing, graphical preview/repair tools and
  broader acceptance. Stop at this usable checkpoint and rotate for feedback.

- Previous product batch complete for owner testing: F123 local command help and
  keyboard/display recovery, phase 10 tasks 10.9a/b. Existing command search now
  includes thirteen offline guides, live native availability, scrollable details,
  F1/Ctrl+L navigation and a window-only layout reset. Both tasks preceded one
  resource build/staging pass; no C++ recompilation was needed. Eighteen selected
  checks pass across accepted suites; six final captures reviewed, including actual
  rendered 20-point text. [Owner procedure](../tests/CommandSearch.md#f123-local-help-and-accessibility-batch-phase-10-tasks-109ab).
  Full F123 remains open for unified workspaces, broader keyboard workflows and
  physical accessibility/high-DPI acceptance. Stop here for feedback and rotate.

- Previous product batch complete for owner testing: F104 native assembly BOM scope
  and inclusion, phase 15 tasks 15.4a/b. Quantities group only siblings; assembly-group
  scope is resolved explicitly, and per-BOM exclusions preserve visibility and source
  objects. Both tasks preceded one successful native build after enabling Assembly
  in the local validation configuration. 21 distinct selected checks pass across
  accepted runs; five captures reviewed. [Owner procedure](../tests/AssemblyBomScope.md).
  Arrays/configurations, custom-column identity, balloons and exploded documentation
  remain open. Stop here for owner workflow testing and rotate.

- Previous product batch complete for owner testing: F053 sketch reuse, phase 11
  tasks 11.6c/d. Sketch > Copy reusable sketch preserves whole-sketch internal
  constraints and construction geometry in an independent native copy, with typed
  placement and a view-only preview. Both tasks preceded one grouped build; the
  preview framing correction was Python-only. 35 distinct selected checks pass;
  one inherited solver case remains deliberately skipped. Five final captures
  reviewed. [Owner procedure](../tests/SketchReuse.md). Partial paste, external-reference
  policies, blocks/libraries/patterns and full F053 acceptance remain open. Stop at
  this owner-test checkpoint and rotate to another dependency-ready family.

- Previous product batch complete for owner testing: F091 mesh preparation, phase 14
  tasks 14.1a/b. CAM > Review CAM mesh reports imported dimensions, boundaries,
  components, orientation, degenerate/duplicate triangles and density. One explicit
  action makes an independent reversed-normal copy of a supported inward mesh.
  Both tasks preceded one PathScripts/Tests build/staging pass; Python corrections
  were staged afterward without another native build. 32 distinct selected checks
  pass across accepted runs; five captures reviewed. [Owner procedure](../tests/MeshPreparation.md).
  Broader repair, self-intersection checks and full F091 acceptance remain open.
  Stop at this usable checkpoint for owner testing and rotate to another family.

- Previous product batch complete for owner testing: F074 precise occurrence movement,
  phase 10 tasks 10.7a/b (bounded F072/F075). Tools > Move occurrence once provides
  world/occurrence translation, typed pivot/axis rotation and a view-only preview.
  Both tasks preceded one native build; a shared Python world-shape correction
  followed the nested-frame checks. 54 affected-consumer checks pass after the fix,
  plus 14 appearance/command checks from the initial group; six captures reviewed.
  [Try the nested occurrences](../tests/OccurrenceMove.md). Copy follows in 10.7c/d; snapping/triads and
  maintained relationships remain open. Stop here for owner testing and rotate.

- Previous product batch complete for owner testing: F087/F088 document updates,
  phase 7 tasks 7.5.7a/b.
  Tools > Document updates exposes native deferral, explicit recompute, failed/pending
  objects and affected loaded inputs. Both tasks preceded one grouped build;
  21 selected checks pass across accepted runs and five captures reviewed.
  [Try the deferred-edit/repair example](../tests/DocumentUpdates.md). Targeted updates,
  background cancellation and broader failure classification remain open; rotate
  after the owner-test checkpoint.

- Previous product batch complete for owner testing: F102 drawing creation,
  phase 15 tasks 15.3a/b.
  TechDraw > Page > Create drawing sheet provides A4/A3 border-only templates,
  explicit scale/base orientation/first- or third-angle convention and linked
  top/right views for a root solid/Body. Both tasks preceded one grouped build;
  all 16 final selected checks pass and five corrected captures reviewed.
  [Try the bracket drawing](../tests/DrawingSetup.md). Broader F102 views, sources,
  preview and repair remain open; stop at the owner-test checkpoint and rotate.

- Previous product batch complete for owner testing: F019 Make Unique,
  phase 12 tasks 12.2d/e. Tools > Make occurrence unique copies a same-document
  sketch/extrusion Part and relinks one occurrence in one Undo step. Other instances
  retain the original; native input remapping, placement, independent edits and
  persistence pass. Both tasks preceded one grouped build; 19 selected checks pass
  and three captures reviewed. [Try the spacers](../tests/UniqueOccurrence.md).
  Whole F019 stays open for broader definitions, relationship remapping, external
  destinations and physical acceptance. Stop here for feedback and rotate item families.

- Previous product batch complete for owner testing: F014 feature organization,
  phase 10 tasks 10.6b/c. Tools > Find and describe features searches native labels,
  names, types and descriptions and applies staged Label/Label2 edits in one Undo
  step. Native identity, shared links, geometry and order stay intact. Both tasks
  preceded one grouped build; 20 selected checks pass and four captures reviewed.
  [Try the hole/description example](../tests/FeatureOrganizer.md). Whole F014 stays
  open for folders, bulk organization, integrated navigators and physical acceptance.
  Stop here for owner feedback and rotate to another dependency-ready item family.

- Previous product batch complete for owner testing: F100 section planes,
  phase 15 tasks 15.1e/f. Clipping View has synchronized numeric direction, explicit
  mm/world offsets and save/load of portable plane presets. Invalid input preserves
  the current view; a scrollable dock keeps fields reachable. Both tasks preceded
  the first grouped build; two layout corrections followed visual review. All 22
  final checks pass and six captures reviewed. [Try the housings](../tests/SectionPlanes.md).
  Whole F100 remains open for embedded views, caps, section measurements and physical
  acceptance. Stop here for owner feedback and rotate to another item family.

- Previous product batch complete for owner testing: F057 mirror result behavior,
  phase 13 tasks 13.5a/b. Part > Mirror offers an associative mirror or independent
  reflected-shape snapshot, with atomic creation and recoverable inline errors.
  Both tasks preceded the grouped build; one compile correction was required.
  All 21 selected checks pass together and five captures reviewed.
  [Try the asymmetric bracket example](../tests/MirrorResultMode.md). Whole F057
  remains open for feature reevaluation, nested snapshots and graphical preview.
  Stop here for owner feedback and rotate to another dependency-ready item family.

- Previous product batch complete for owner testing: F049 missing-coincidence review,
  phase 11 tasks 11.6a/b. Existing Validate Sketch lists endpoints/gaps, highlights
  candidate rows and adds only checked coincidences in one undoable repair. Edits
  invalidate candidates; solver failures restore the sketch. Both tasks preceded
  the grouped build; one compile correction was required. All 22 selected checks
  pass and five captures reviewed. [Try the gap-repair example](../tests/SketchRepairReview.md).
  Whole F049 remains open for broader diagnostics/preview and physical acceptance.
  Native detector/Block limitations are recorded below. Rotate pending owner feedback.

- Previous product batch complete for owner testing: F101 interference/clearance,
  phase 15 tasks 15.1c/d. Part > Interference and clearance checks explicit native
  solid pairs, with overlap volume, contact tolerance, minimum clearance, unresolved
  inputs and counted exclusions. Result navigation selects each pair; edits invalidate
  the report. One grouped build; all 23 selected checks pass on the first run and
  four captures reviewed. [Try the overlap/contact/gap example](../tests/InterferenceCheck.md).
  Whole F101 remains open for broader assemblies, acceleration and physical acceptance.
  Stop here for owner feedback and rotate to another dependency-ready item family.

- Previous product batch complete for owner testing: F018 occurrence appearance,
  phase 12 tasks 12.2b/c. View > Occurrence appearance stages visibility and uniform
  colour/transparency for a whole shape/Body link, with native source inheritance.
  Source, other occurrences and placement remain unchanged. One grouped build;
  23 selected checks pass and five captures reviewed. [Try the repeated-part example](../tests/OccurrenceAppearance.md).
  Whole F018 remains open for broader occurrence paths, representations and physical
  acceptance. Stop here for owner feedback and rotate to another item family.

- Previous product batch complete for owner testing: F098/F099 measurement meaning
  and point snapshots, phase 15 tasks 15.1a/b. The existing Measure task now shows
  operand identities, distance/frame meaning and snapshot policy. Distance Free
  persists UTC capture information without live links. One grouped build; 13 selected
  checks pass and two task-panel captures reviewed. [Try the example](../tests/MeasurementContext.md).
  Broader measurement/repair and physical acceptance remain open. Rotate the next
  item family and defer refinements to owner workflow feedback.

- Previous product batch complete for owner testing: F015 dependency inspection,
  phases 7 and 10 tasks 7.5.5a / 10.6a. Tools > Inspect dependencies shows native
  inputs/consumers, direct/transitive property relationships, status and loaded
  external sources, with explicit model selection and node navigation. One grouped
  build; 23 distinct selected checks pass and three captures reviewed.
  [Try the shared-sketch example](../tests/DependencyInspector.md). Whole F015 remains
  open for broader navigator/target roles and physical acceptance. Rotate the next
  item family; defer further inspection refinements to owner feedback.

- Previous product batch complete for owner testing: F124 sketch support,
  phase 11 tasks 11.7y/z. Sketcher > Sketch > Inspect and change sketch support
  exposes current attachment, explicit planar replacement, local/world numeric
  previews and undoable Apply/repair. One grouped build and all 39 selected checks
  pass; three dialog captures reviewed. [Try the example](../tests/SketchSupport.md).
  Whole F124 remains open for graphical preview, broader support/occurrence and
  physical acceptance. Stop refining this pilot and rotate pending owner feedback.

- Previous product batch complete for owner testing: F127 manufacturing export,
  phase 15 tasks 15.7a/b. Part > Manufacturing export now hands selected solids and
  whole occurrences to STL with explicit mm/world placement and reusable quality.
  One grouped build, all 20 selected checks and two reviewed captures pass.
  [Try the handoff example](../tests/ManufacturingExport.md). Broader formats and
  configuration/physical acceptance remain open; rotate the next item family.

- Previous product batch complete for owner testing: F040 temporary isolate/hide,
  phase 10 tasks 10.5a/b. View > Visibility now has temporary isolate/hide and
  previous/original display restore. One grouped build and all 20 selected checks
  pass; five viewport captures reviewed. [Try the example](../tests/TemporaryDisplay.md).
  Whole F040 remains open for linked-member/save-time policy and physical acceptance.
  Defer further refinement to owner feedback and rotate to another item family.

- Previous product batch complete for owner testing: command search (F033,
  phase 8 tasks 8.4.2a/b and phase 10.4 progress). Tools > Command search / Ctrl+K
  finds familiar aliases and opens existing commands with context guidance.
  One grouped build; 59 distinct passing checks and three reviewed captures.
  [Try the palette](../tests/CommandSearch.md). Whole F033 remains open; defer
  further refinement to owner feedback and rotate to another item family.

- Previous product batch complete for owner testing: phase 10 named parameters
  (10.8aa/ab, F122). Part > Named parameters now opens the promoted length/angle
  editor for an explicit Part or marked parameter set, with reusable expression
  references. One grouped PartGui/PartScripts build passed; final selected evidence
  has 90 distinct passing checks and two reviewed dialog captures. No release update.
  [Try the enclosure and command](../tests/NamedParameters.md). Stop refining this
  workflow pending owner feedback or a demonstrated blocker/dependency. Whole F122
  remains open for scope/publication/where-used and physical acceptance. Rotate the
  next authorized batch to another dependency-ready family; CAM/Extrude follow-ups
  remain recorded separately.


- Release 0.0.2: requested after 0.0.4, built as a new Windows installer from
  the unchanged validated application and publicly published. Runtime hash
  comparison and installer acceptance pass; [release checkpoint](#pre-release-002).
  Existing 0.0.1 and 0.0.4 releases remain unchanged.

- Release 0.0.4: Windows x64 installer built, validated and published as a GitHub
  pre-release; [release checkpoint](#pre-release-004). All 312 packaged tests and
  installation/launch/hash/uninstall checks pass. Other roadmap acceptance gates
  remain open.


Specification update: see [the re-updated objective reconciliation](#re-updated-objective-specifications-and-delivery-slices) and [all 127 item-level specifications](#item-level-product-specifications-f001-f127). Added tasks 10.8-10.9, 11.7, 15.7, 16.8-16.9 and benchmarks T13-T16 are pending; existing completion evidence is preserved.

- Release 0.0.1: user-authorized Windows x64 installer built, accepted and published; publication
  tracked in [the release checkpoint](#pre-release-001). This does not close the
  remaining product, GUI, machine or broad compatibility gates.
- Specification refinement: the [detailed candidate inventory](#detailed-inventory-reconciliation)
  expands existing pending tasks and adds 7.5.7/8.1.6. Consult those concrete behaviors
  before treating a broad objective as complete; implementation evidence is unchanged.
- Previous batch: 16.2bs/bt repair Holding Tab and Indexed Setup command startup
  and protect unrelated transactions. Grouped validation: 55 passes; included in
  the published 0.0.4 installer.
- Previous batch: 16.2bq/br verify Plunge Milling LinuxCNC/Grbl output and FCStd
  save/reopen regeneration. Grouped validation: 87 passes, zero failures/errors/
  skips. Test-only batch using the existing build; no native rebuild or release.
- Previous batch: 16.2bo/bp validate Plunge Milling cycle settings and exercise
  dwell/peck/chip-breaking output. Grouped validation: 84 passes, zero failures/
  errors/skips. Python staging only; no native rebuild or release.
- Previous batch: 16.2bm/bn establish Plunge Milling entry/exit clearance and
  between-position retracts, validate feed and set/cancel drilling cycles explicitly.
  Grouped validation: 82 passes, zero failures/errors/skips. No native rebuild/release.
- Previous batch: 16.2bk/bl guard Dogbone stale inputs and invalid cutter data.
  Grouped CAM checks: 79 passes; Dogbone geometry suites: 24 passes. Final runs
  have zero failures/errors/skips. Python staging; no native rebuild or release.
- Previous batch: 16.2bi/bj guard Plunge Milling base inputs and original Boundary
  base/stock inputs. Grouped validation: 77 passes, zero failures/errors/skips.
  Python staging only; no native rebuild or release.
- Previous batch: 16.2bg/bh guard Dragknife and Ramp Entry against stale base
  dependencies. Grouped validation: 74 passes, zero failures/errors/skips.
  Python staging only; no native rebuild or release.
- Previous batch: 16.2be/bf guard Axis Map and Z Correction against stale base
  inputs and clear Z Correction surface caches before validation. Grouped tests:
  72 passes, zero failures/errors/skips. Python staging; no native rebuild/release.
- Previous batch: 16.2bc/bd reject stale Array/Mirror base paths and Mirror
  reference geometry during explicit generation. Grouped validation: 69 passes,
  zero failures/errors/skips. Python staging only; no native rebuild or release.
- Previous batch: 16.2ba/bb repair Boundary2 linking command access and omit all
  motion when clipping removes every cut. Grouped validation: 66 passes, zero
  failures/errors/skips. Python staging only; no native rebuild or release.
- Previous batch: 16.2ay/az validate holding-tag setup/tool data and refresh point
  queries instead of trusting old path caches. Grouped validation: 64 passes, zero
  failures/errors/skips. Python staging only; no native rebuild or release.
- Previous batch: 16.2aw/ax guard holding-tag direct processing and position edits.
  Grouped validation: 62 passes, zero failures/errors/skips; failed direct generation
  clears output, stale inputs preserve stored positions. Python staging only;
  no native rebuild or release update.
- Previous batch: 16.2au/av guard Boundary2 and holding-tag regeneration against
  invalid/unrecomputed dependencies. Grouped validation: 60 passes, zero failures/
  errors/skips. Native skipped-recompute caches remain export-blocked; explicit
  generation clears/rejects them. No native rebuild or release update.
- Previous batch: 16.2as/at clear stale Boundary2 paths on generation failure
  and reject empty/invalid/non-solid boundary offset results. Grouped validation:
  58 passes, zero failures/errors/skips. Python staging only; no native rebuild
  or release update.
- Previous batch: 16.2aq/ar fix production CAM holding-tag failure behavior:
  clear cached output on missing input and reject generation failure instead of
  falling back to an untagged cutting path. Grouped validation: 56 passes, zero
  failures/errors/skips; Python staging only, no native rebuild or release.
- Previous batch: 10.8y/z add explicit Part-owned parameter-container creation
  and an editor entry point independent of active document state. Grouped validation:
  75 passes, zero failures/errors/skips after correcting a test setup. Prototype only;
  no native rebuild or release update.
- Previous batch: 10.8w/x validate the enclosure benchmark through prototype
  editor widgets, including rename/display units, error recovery and save/reopen.
  Grouped validation: 73 passes, zero failures/errors/skips. No native rebuild
  or release update; physical acceptance and production integration remain open.
- Previous batch: 10.8u/v add a native enclosure/lid/hole parameter benchmark and
  shared-definition occurrence checks. Grouped validation: 71 passes, zero failures/
  errors/skips after fixture correction. Bounded T13 evidence; no native rebuild
  or release update, production integration remains pending.
- Previous batch: 10.8s/t add descriptions on parameter creation and display-only
  unit selection in the prototype editor. Grouped validation: 69 passes, zero
  failures/errors/skips. No native rebuild, installed command or release update.
- Previous batch: 10.8q/r prototype atomic length/angle parameter creation and
  its dialog workflow. Grouped validation: 67 passes, zero failures/errors/skips.
  No native rebuild, installed command or release update.
- Previous batch: 10.8o/p guard stale parameter lists and verify two-editor
  conflict/lifecycle isolation. Grouped validation: 65 passes, zero failures/errors/
  skips. Prototype only; no native rebuild, installed command or release update.
- Previous batch: 10.8m/n protect the editor prototype from stale external edits
  and close it on parameter/document deletion. Grouped validation: 62 passes, zero
  failures/errors/skips. No native rebuild, production installation or release.
- Previous batch: 10.8k/l add an uninstalled existing-parameter dialog prototype
  and verify apply/close, error correction and rename interactions. Grouped native
  Qt/model validation: 59 passes, zero failures/errors/skips. No native rebuild
  or release update; production editor integration remains open.
- Previous batch: 10.8i/j prototype atomic parameter-expression edits with downstream
  recompute validation, rollback and transaction/readiness boundaries. Grouped
  architecture validation: 56 passes, zero failures/errors/skips. Test-only code;
  no native rebuild, installed editor or release change.
- Previous batch: 10.8g/h prototype atomic parameter rename and verify label-based
  consumer references with owned formulas. Grouped architecture validation: 54 passes,
  zero failures/errors/skips. No native rebuild, installed UI or release change.
- Previous batch: 10.8e/f validate angular parameter expressions and native property
  rename propagation, including Undo/Redo and save/reopen. Grouped architecture
  validation: 52 passes, zero failures/errors/skips. Test-only prototype; no native
  rebuild, installed UI change or release update.
- Previous batch: 4.1.10/5.1.10 preserve the primary startup error and continue task
  cleanup after secondary cleanup errors; repeated annotation removal is harmless.
  Grouped model/GUI validation: 54 passes, zero failures/errors/skips; Python staging
  only, no native rebuild or release update.
- Previous batch: 4.1.9/5.1.9 protect unrelated caller transactions when reopening
  Trim Body or Isocline. Grouped model/GUI validation: 52 passes, zero failures/
  errors/skips; Python-only staging, no native rebuild or release update.
- Previous batch: 4.1.8/5.1.8 clean up task resources and edit transactions when
  construction/dialog display fails. Grouped model/GUI validation: 50 passes,
  zero failures/errors/skips; Python staging only, no native rebuild or release.
- Previous batch: 4.1.7/5.1.7 roll back feature creation when factory/editor startup
  fails. Grouped model/GUI validation: 48 passes, zero failures/errors/skips;
  shared Python transaction guard staged, no native rebuild or release update.
- Previous batch: 4.1.6/5.1.6 skip stale preselected inputs while retaining usable
  selections and an editable task. Grouped model/GUI validation: 46 passes, zero
  failures/errors/skips; Python-only staging, no native rebuild or release update.
- Previous batch: 4.1.5/5.1.5 reject invalid/unrecomputed picks before replacing
  Trim Body and Isocline inputs. Grouped model/GUI validation: 44 passes, zero
  failures/errors/skips; Python modules staged with matching hashes, no native
  rebuild or release update.
- Previous batch: 4.1.4/5.1.4 integrate dependency readiness checks into production
  Trim Body and Isocline task previews/acceptance. Grouped model/GUI validation:
  42 passes, zero failures/errors/skips. Python modules staged in the isolated build;
  no native rebuild or release update.
- Previous batch: 11.7w/x prototype a current-result accessor that rejects invalid
  or unrecomputed dependencies and returns an independent shape copy. Grouped
  validation: 50 passes, zero failures/errors/skips; no native rebuild. This is
  not installed in application consumers/exporters; production integration pending.
- Previous batch: 11.7u/v validate missing-face repair and deleted-source replacement
  for planar references. Grouped validation: 48 passes, zero failures/errors/skips;
  no native rebuild. Deleted-source recovery requires explicit sketch face reselection;
  production repair UI and broad consumer invalidation remain pending.
- Previous batch: 11.7s/t combine reference creation and reattachment in one undo
  transaction and verify late-failure rollback without orphan objects. Grouped
  validation: 46 passes, zero failures/errors/skips; no native rebuild. Test-only
  operation; production editor and deployment remain pending.
- Previous batch: 11.7q/r prove an explicit planar reference adapter across placed
  parts, including preview parity, source motion, Undo/Redo and restore. Grouped
  validation: 44 passes, zero failures/errors/skips; no native rebuild. Test-only
  Python proxy must remain importable; production reference integration pending.
- Previous batch: 11.7o/p enforce prototype support scope: cross-container and
  App::Link occurrence supports reject before mutation. Grouped validation: 42
  passes, zero failures/errors/skips; no native rebuild. Cross-part placement
  mismatch recorded; reference adapters and occurrence-edit policy remain pending.
- Previous batch: 11.7m/n validate reversed attachment preview/commit/restore and
  protect expression-driven offsets from preserve-world replacement. Grouped
  validation: 40 passes, zero failures/errors/skips; no native rebuild. Test-only
  work; production UI and broader expression/reference policies remain pending.
- Previous batch: 11.7k/l replace live rollback preview with disposable-document
  placement evaluation and verify live-document isolation and existing redo history.
  Grouped validation: 38 passes, zero failures/errors/skips; no native rebuild.
  Production graphical preview and full sketch/consumer evaluation remain pending.
- Previous batch: 11.7i/j prototype rollback-based reattachment placement previews
  and verify candidate/commit parity and preservation of existing undo history.
  Grouped validation: 36 passes, zero failures/errors/skips; no native rebuild.
  Production graphical preview and isolation from observers remain pending.
- Previous batch: 11.7g/h reject cyclic and stale/invalid reattachment supports
  before mutation. Grouped validation: 34 passes, zero failures/errors/skips;
  test-only changes, no native rebuild. Production reattachment UI remains pending.
- Previous batch: 11.7e/f prototype deliberate missing-face repair and protect
  caller-owned transactions. Grouped validation: 32 passes, zero failures/errors/
  skips; no native rebuild. Production repair UI and broad topology repair remain open.
- Previous batch: 11.7c/d extend the test-only reattachment operation to explicit
  preserve-local/preserve-world policies, validated with rotated supports and a
  rotated parent part. Grouped validation: 30 passes, zero failures/errors/skips.
  No native rebuild; production editor and lost-support repair remain pending.
- Previous batch: 11.7a/b prototype explicit planar sketch reattachment with local
  offset preservation and reject missing/curved supports before mutation. Grouped
  validation: 28 passes, zero failures/errors/skips; no native rebuild. Production
  reattachment editor, preserve-world policy and lost-support repair remain pending.
- Previous batch: 10.8c/d prove explicit parameter references remain independent
  across parts with matching labels and invalid geometry recovers after transaction
  abort. Grouped architecture validation: 26 passes, zero failures/errors/skips.
  Test-only changes; no native rebuild or parameter editor delivery.
- Previous batch: 10.8a/b prove shared named length parameters, native expression
  persistence/transactions and a test-only dimensional assignment guard. Grouped
  architecture validation: 24 passes, zero failures/errors/skips; no installed
  feature/editor or native rebuild. Native unit coercion remains a production gate.
- Previous batch: 16.2ao/ap preserve probe-file precision and reject conflicting
  duplicate heights. Grouped validation: 65 passes, zero failures/errors/skips;
  Python-only synchronization, no native rebuild.
- Previous batch: 16.2am/an make shared property inheritance and job operation
  traversal iterative, handling cycles/deep chains and duplicate bases. Grouped
  validation: 151 passes, zero failures/errors/skips; no native rebuild.
- Previous batch: 16.2ak/al recognize dressups by current proxy identity with
  guarded legacy fallback and traverse base chains iteratively with cycle errors.
  Grouped validation: 84 passes, zero failures/errors/skips; no native rebuild.
- Previous batch: 16.2ai/aj clear failed Plunge Milling output and reject
  invalid stepover with native error state. Grouped validation: 54 passes, zero
  failures/errors/skips; Python-only synchronization, no native rebuild.
- Previous batch: 16.2ag/ah clear Dragknife and Ramp Entry output before
  validation/generation. Grouped validation: 52 passes, zero failures/errors/skips;
  Python-only synchronization, no native rebuild.
- Previous batch: 16.2ad/ae/af reject non-finite probe coordinates and invalid
  interpolation settings, and correct source-line subdivision counts. Grouped
  validation: 51 passes, zero failures/errors/skips; no native rebuild.
- Previous batch: 16.2aa/ab/ac clear Z Correction caches, reject unusable probe
  files and block out-of-area fallback. Grouped validation: 48 passes, zero
  failures/errors/skips; Python-only synchronization, no native rebuild.
- Previous batch: 16.2x/y/z clear failed Axis Map results, validate positive
  finite radius and update rotary-post snapshot fixtures for the export guard.
  Grouped validation: 44 passes, zero failures/errors/skips; no native rebuild.
- Previous batch: 16.2u/v/w fix Mirror placed passthrough, failure-safe output
  assembly and source-path isolation. Grouped validation: 53 passes, zero
  failures/errors/skips; Python-only synchronization, no native rebuild.
- Previous batch: 16.2s/t clear Array paths before validation/generation and
  Dogbone machining/corner caches before generation. Grouped validation: 49
  passes, zero failures/errors/skips. Skipped native consumers remain a limitation;
  their export guard is verified. Python-only synchronization, no native build.
- Previous batch: 16.2q/r block export for missing/non-geometric Boundary stock
  and reject empty/invalid offset results before clipping. Grouped validation:
  46 passes, zero failures/errors/skips; Python-only update, no native build.
- Previous batch: 16.2o/p prevent cached Boundary paths after clipping/offset
  failures and reject empty boundary geometry in both inclusion/exclusion modes.
  Grouped validation: 44 passes, no failures/errors/skips; Python-only update
  to the existing development build. Native GUI/machine acceptance remains open.
- Previous batch: 16.2l/m/n handle empty dressup inputs, failed lead generation and
  disabled-lead passthrough. Grouped validation: 40 passes, two existing generator
  skips, zero failures/errors. Python-only synchronization, no native build.
- Previous batch: 16.2j/16.2k extend model-container invalidation/rebinding to
  nested CAM dressups and base operations. Grouped validation: 90 passes, one
  existing skip, zero test failures/errors; Python-only synchronization. Missing
  model diagnostics in Lead-in/Lead-out and general consumer gates remain open.
- Previous batch: 16.2h/16.2i reject postprocessing when a selected operation or
  its linked inputs are dirty/invalid. Native cached-path failure/recovery checks
  and postprocessor/dressup regressions: 88 pass, one pre-existing skip, zero
  failures/errors. Python-only synchronization; no native build. General missing
  links, semantic validity, frozen-job policy and machine acceptance remain open.
- Previous batch: 16.2f/16.2g handle replacing/removing CAM model containers and
  restore the wait cursor around full operation execution. Eight targeted checks
  and 67 broader CAM regressions pass across two runs; no native build required.
  Export guards, failed upstream producers and general consumer compatibility remain open.
- Previous batch: 16.2d/16.2e add explicit CAM job-model dependencies and restore
  them for older saved operations. All 72 grouped CAM checks pass; production Python
  synchronized to the existing fork without a native build. Normal document recompute
  now handles model edits and empty-source recovery in the SurfaceScan fixture.
  Export guards, failed producers and full consumer
  compatibility remain open.
- Prior batch: 16.2b/16.2c fixed stale paths on explicitly requested execution with
  missing models/tools, with 69 grouped checks. The new batch addresses scheduling.
- Prior mixed/unique batch: 12.1a/12.2a passed 32 grouped architecture checks.
- Previous batch: 7.1.3g/h planar split/primary-merge lineage passed 29 checks.
- Prior attachment/drawing batch: 7.1.3f and 16.2a passed 24 grouped checks.
  Next: missing/ambiguous drawing references, CAM path/FEM consumers, mixed-part
  identity and production target discovery before architecture selection.
- Previous batch: 10.1 and 10.3a/10.3b reconciled contracts and proved transient
  proposals versus committed operation intent with 22 grouped passing checks.
- Version 2 objectives remain in the [coverage register](#version-2-objective-coverage);
  the expanded portfolio is pending except for specifically evidenced subtasks.
- Previous batch: Phase 7 placement/occurrence/consumer comparison, 2026-09-29.
  Completed 7.1.3c/7.1.3d/7.1.3e: transformed inputs, an assembly-local cut,
  and a production fix for stale Draft clone/CAM job-model geometry.
  All 88 grouped history, Draft and CAM checks pass in the existing application;
  Python-only update, no native build. History adapters remain test-only.
  Next: lineage, transformed attachments and remaining consumers for 7.1.3 and decisions in
  7.1.5/7.1.6 before production navigator/model changes. Batch two or three related
  implementation tasks before any costly build, as requested by the owner.
- Previous implementation: [prioritized upstream issue work](#upstream-issue-work).
  Latest freeform fix: U.23 bypasses the reproduced #26300 exact-projection stall
  using tolerance-controlled mesh silhouettes. The fixture generates in 14 seconds;
  all 91 CAM checks pass without a rebuild. U.15 cancellation acceptance remains.
  Latest boundary correction: avoidance no longer uses a fallback that fills
  selected holes after projection fails; U.22 records 81 passing CAM checks.
  Latest geometry fix: #6864 final-strip coverage now passes in the compiled
  replacement generator; U.21 records the 77-test CAM batch.
  Latest safety fix: partial boundary projection/union can no longer drop selected
  regions; U.20 records 14 focused and 59 related passes without a build.
  U.19 retains the original #26300 timeout evidence, superseded for generation by
  U.23. Modern CAM avoidance now stops on boundary failures or unsupported
  strategy switches instead of ignoring exclusions. Python-only update installed;
  all 67 focused/related CAM regressions pass. Remaining child cases: U.14-U.16.
  Audit inherited fixes and changed workflow applicability first. Mirror #32706
  is now fixed in the local application: one targeted compile/relink completed
  the accumulated batch, and all 75 issue regressions pass. No full rebuild.
  Recovery, quantity input, unified Extrude keyboard editing and tree-selection
  regressions now pass against the existing fork; see U.5 and U.9 below.
- Planning priority: [NX-style unified feature history](#nx-feature-history), then
  [consistent modeling workflows](#nx-modeling-workflows), then
  [downstream integration](#nx-downstream-workflows). These phases describe the
  user's preferred FreeCAD Plus workflow, drawing on NX and SolidWorks. The owner
  has now requested roadmap execution; proceed in dependency order and preserve
  the architecture/compatibility gates. Planned items do not imply product parity.
- [Phase 6: STL CAM and holding tabs](#cam-mesh-machining) is implemented and built.
  All 22 focused automated tests pass; related regressions have 112 passes and one
  optional dependency skip. Native acceptance and simulation remain pending.
  Two-sided/indexed machining uses separate manually indexed jobs.
  The NX-style history foundation is underway; production history remains pending.

- Current build and closeout evidence: [consolidated validation, 2026-09-29](#consolidated-validation).
  Before the CAM changes, the configured Windows application built successfully
  and all 149 regression tests passed at both tested display scales. This evidence
  is separate from the later CAM validation in Phase 6. Physical viewport/keyboard acceptance remains pending:
  the user stopped native computer use with Escape before those checks completed.
- Isocline Curve implementation is recorded in [Phase 5](#isocline-curve), Trim Body
  in [Phase 4](#trim-body), and Revolve/Groove offsets in milestone 3.9.
  Milestone 2.2 and the later manual acceptance milestones remain open; another
  rebuild alone will not complete them.
  This roadmap records status; it does not authorize new phases or external publication.
- The [Part Design workflow audit](#part-design-workflow-audit) inventories the
  remaining selection and complete-editing work. Audit complete; implementation pending.
- Preferred future command layout: [unified geometry workflows](#unified-feature-workflows)
  with Add/Subtract first in the task pane; Extrude passes the automated checks below.

<a id="planning-baseline-adoption"></a>
## Planning baseline adoption and version 2 reconciliation

The owner requested adoption of two supplied documents. Execution guidance is in
[DEVELOPMENT_GUIDELINES.md](DEVELOPMENT_GUIDELINES.md); the complete supplied
[FREECAD_PLUS_DEVELOPMENT_ROADMAP.md](archive/FREECAD_PLUS_DEVELOPMENT_ROADMAP.md)
is preserved as a historical reference. The owner subsequently supplied
`UPDATED_FREECAD_PLUS_DEVELOPMENT_ROADMAP.md`, version 2.0 (document updated date:
2026-09-30), and requested all additional objectives in this active roadmap.
The expanded inventory and concrete tasks below now own that backlog; the original
archive no longer defines its full scope. Supplied P0-P11/feature IDs are mappings,
not replacements for stable local task IDs. Estimates remain planning hypotheses.

This adoption imports desired objectives, not the attachment's embedded agent
startup assignment: retain PROGRAMMING_SUMMARY.md, this roadmap, WORK_STATE.md and
existing architecture records. Do not restart the fork, repeat established builds,
or create a second status ledger. Preserve existing evidence and batch two or three
related implementation tasks before costly build validation. Optional items remain
optional; no release, outreach, registration, rename or billing action is authorized
by listing it. The desktop application is planned to remain free of charge for the
foreseeable future, without subscriptions, activation or paid core feature gates.

Version 2's visible, overridable New Body/Unite suggestion policy supersedes the
unconditional New Body proposal and the unresolved-default wording in earlier
planning documents, including DEVELOPMENT_GUIDELINES.md. Task 7.4.8 records the
planning decision; its implementation remains open. Synchronize the owning product,
UI and guideline contracts in 10.1 before migrating commands. Preserve the owner's
operation-first task layout: guided prompts can advance through unresolved inputs
without relocating that first field. Retain Pocket/Groove as shared-command presets.
FreeCAD Plus remains the working name; evaluating a rename is optional.

| Supplied phases | Existing owner / integration rule |
| --- | --- |
| P0 / G0 baseline | Phase 1, consolidated validation and Development Guide. Reuse recorded builds/tests; audit only missing or invalidated evidence. No claim that the entire expanded G0 is satisfied. |
| P1-P3 / G1-G3 architecture | Phase 7. Decide contracts, prove the mixed-part/shared-occurrence pilot, then migrate. Include assembly-local effects, topology ambiguity, legacy documents and drawing/CAM/FEM consumers. |
| P4-P5 / G4-G5 modeling and sketches | Phases 3 and 8. Preserve implemented Extrude/Pattern/offset work; migrate behind stable contracts. New selection conventions require reconciliation with input collectors. |
| P6 / G6 assemblies | Phases 7 and 9. Shared versus local editing, reference sets, replacement, external links and load-state semantics remain planned. |
| P7 / G7 geometry portfolio | Phases 3-5 and 8. Trim and Isocline already have implementation/test evidence; advanced surfaces/direct editing remain candidates. Do not recreate completed work. |
| P8 / G8 mesh CAM | Phase 6. Preserve Parallel/Waterline, holding tabs and the user's two-sided/manually indexed requirement. Roughing, rest machining, simulation/post gates remain separate; three-axis wording does not drop indexed setups. |
| P9 / G9 downstream | Phase 9; preserve all supplied inventory rows as future candidates, activating bounded tasks only within authorized scope. |
| P10 / G10 maintenance | Upstream issue work, Phase 16 and release gates in the Development Guide. Local fixes/builds are not releases. |
| P11 / G11 onboarding | Phase 17: starter models, tutorials, independent-fork positioning and measured user adoption; external publication requires separate authorization. |

The [version 2 coverage register](#version-2-objective-coverage) gives every supplied
inventory ID a concrete task and status. Do not maintain parallel status in archived
files. Guideline B01-B10 benchmark IDs are user-task fixtures, distinct from the
assembly inventory IDs; the supplied T01-T12 benchmark register is retained below.
Usability/performance thresholds and effort estimates require measurements.

- [ X ] 1.3 Adopt the supplied agent guidance and map it to existing document owners.
  Evidence: guidelines and complete planning reference retained; root/index/guide
  links and future product direction updated. Documentation-only; no application
  behavior, build evidence or prior completion markers changed.
<a id="upstream-issue-work"></a>
## [   ] Upstream issue work: reliability before workflow polish

Authorized 2026-09-29. Order and live links: [FREECAD_ISSUES.md](FREECAD_ISSUES.md).
Complete each issue only with relevant source, runtime and acceptance evidence;
closed upstream, inherited source, and obsolete UI entry points are distinct states.

- [ X ] U.1 Triage all ten watchlist issues against this fork, prioritized by data
  loss, system responsiveness, wrong geometry/toolpaths, numeric input and UI impact.
  Recovery #18044, numeric #32700/#32717/#32718, arc #32690 and tree #28412 fixes
  are inherited. #28412 is now closed upstream. No duplicate fixes were applied.
- [ X ] U.2 Verify CAM arc-offset regression #32690 using the existing build:
  all 43 `TestPathOpUtil` tests pass, including mixed circle-normal regression
  `test49`. Installed `Path/Op/Util.py` SHA-256 matches source:
  `8CEFCB9E818D91926EF29E9FDE36544735B72384B6AA99127B95E9477A2A8C98`.
- [ X ] U.3 Reproduce #32706 and prepare the bounded Part Mirror correction.
  Convert the reference plane from its enclosing Body/Part into the source's
  parent frame; preserve the source transform, shared Assembly frame and existing
  feature/property identities. Use the common GeoFeature base for datum planes.
  Added three regressions for translated/rotated Body faces, shared Assembly
  placement, Body-face references without double transformation and source moves.
  Registered them in the standard Part suite and added `ValidateUpstreamIssues.FCMacro`.
- [ X ] U.4 Build/install and validate the accumulated issue batch. Compiled only
  `FeatureMirroring.cpp`, relinked Part and synchronized three changed test scripts.
  Both build steps exit 0. All 75 regressions pass without errors/skips: six Mirror
  geometry tests (now including save/reopen and repeated recompute), two real
  Mirror task-pane reference-selection tests for translated/rotated Bodies, 43 CAM
  offset tests, four quantity tests, 19 Extrude tests and one tree test. #32706 is
  fixed locally; this does not close the upstream issue or certify physical picking.
- [ X ] U.5 Validate inherited recovery and quantity-input fixes in the existing
  source-built fork. Five isolated recovery fixtures pass through the real startup
  dialog: damaged ZIP, malformed model XML and malformed GUI XML originals still
  offer recovery; valid newer originals are excluded, valid older originals recover.
  All four recovered solids have volume 231 mm3; original hashes remain unchanged.
  Four native Qt quantity-event tests pass, including arrow/wheel focus-loss
  persistence and implicit inches with global millimetres. All 19 Extrude task tests
  pass, including two new Add/Subtract keyboard edit/step tests on create and reopen
  that check feature dimensions and solid volume. No application fix was duplicated.
  Procedure: [upstream issue validation](../tests/UpstreamIssues.md).
- [   ] U.6 #29376: obtain a reproducible affected session/GPU trace before changing
  rendering. Frame-rate limiting and background changes are already inherited;
  upstream still reports intermittent OS-wide slowdown. Do not infer resolution
  from a short successful session or one reporter's driver update.
- [ X ] U.7 Classify workflow overlap: legacy #10584 is superseded for new tasks
  by Mill Facing, but saved MillFace operations remain a regression risk (upstream
  closed as won't-fix). #27751's modern PlanarSurface/modular generator workflow
  is already inherited and used by our STL command; the wider upstream epic stays
  open. Neither classification authorizes silent migration of saved operations.
- [ X ] U.8 Publish the coherent source/triage milestone to `origin/main`:
  `85fd6ebc77a5a180d61ad116cf6507fb274e93d4`, remote hash verified.
  Python/macro syntax and diff whitespace checks pass. Build/acceptance gates
  were still open at that checkpoint; no release or new executable was produced then.
- [ X ] U.9 Validate inherited tree fix #28412 using native Qt mouse events.
  Expansion and collapse both toggle the container and preserve model selection
  during a held-button move. The planned NX history has not replaced this tree.
- [ X ] U.10 Recovery, numeric and tree regression milestone committed/pushed as
  `24815217c91ecbc2029771f34be02a5aa4c640d6`; `origin/main` hash verified.
  At that checkpoint U.4/U.6 remained open; no native build was needed for those
  inherited fixes. The subsequent U.4 checkpoint now includes the Mirror correction.
- [ X ] U.11 Passing Mirror persistence/GUI tests and build-validation checkpoint
  published as `bb6d7607a78080bec36f8ade30c8925f09201874`; `origin/main` hash verified.
  The unreproduced slowdown U.6 remains open.
- [ X ] U.12 Inspect the seven children linked from CAM umbrella #27751.
  Four are closed; open #27950, #26300 and #6864 require comparison with the
  replacement operation. Modern modular generators supersede the old code path,
  but this does not prove every reported geometry case is fixed.
- [ X ] U.13 Fix reproduced modern avoidance failure behavior related to #27950.
  Boundary/subtraction failure now raises an error instead of restoring the full
  cutting region or dropping selected exclusions. Valid fully excluded masks stay
  empty. Waterline/other strategy changes with retained face avoidance now report
  unsupported settings instead of ignoring them. Previous paths are cleared.
  Eight focused tests and 59 related generator/operation/STL/tab tests pass.
  The external planar open-face case retains full surrounding coverage and cutting
  segments do not cross the excluded face. Python files installed and hash-verified;
  no native build or document/property migration. UI behavior documented in UI-006.
- [   ] U.14 #27950: exact GeomFillSurface integration remains pending for a
  batched build with Surface enabled (`BUILD_SURFACE=OFF` currently). Attachment
  inspection found no GeomFillSurface object: Base selects Clone.Face3 and
  Part__Mirroring.Face3 (mirrored Pad geometry). Saved BReps from that attachment
  generate a nonempty path in PlanarSurface, without restoring legacy proxies.
  This proves generation, not full attachment coverage or legacy backend repair.
  A generated non-planar B-spline exclusion independently passes cutting-segment
  exclusion and coverage-on-both-sides checks. Do not generalize to arbitrary
  freeform faces or mark the upstream issue closed.
- [   ] U.15 #26300: freeform generation corrected and geometry-validated in U.23;
  native task cancellation acceptance remains pending. The replacement operation
  was affected (U.19), so UI changes did not obsolete this backend issue. U.23
  preserves the existing outer cutting silhouette, separate avoidance holes,
  selected regions and cutter offsets; no bounding-box substitution or dropped
  failed faces. Legacy Surface applicability and machine/post acceptance remain
  separate. Do not mark the whole upstream report closed from the modern replay.
- [ X ] U.16 #6864: reproduced missing transverse edge passes in the current
  C++ Line generator, so the replacement UI/backend did not obsolete the defect.
  Add clipped finishing passes at each contour's transverse limits while retaining
  the regular stepover grid. Validate nonintegral/exact step ratios, separate
  regions, rotated masks, reverse order, and excluded holes. U.21 records the
  installed module and passing CAM batch. This is a modern-generator correction;
  saved legacy Surface operations and machine/post acceptance remain separate.
- [ X ] U.17 CAM avoidance fix published as
  `b2cfdf0f114ff2cba48004fe538991395b22f525`; `origin/main` hash verified. No release.

- [ X ] U.18 Extend #27950 applicability evidence with saved attachment geometry
  and a generated curved-face regression. `tests/TestIssueSurfaceAvoidance.py`
  now has nine passing checks; opt-in `tests/TestIssue27950Fixture.py` adds one.
  `curved-avoidance-20260929-final/results.json` under the external root below:
  10 PASS, no failures/errors/skips, process 0. Installed surface_common.py and
  PlanarSurface.py bytes match source and the U.13 recorded hashes. No app code
  changed or rebuild performed. Initial exact-object probe stopped with missing
  Surface module; that run is not acceptance evidence. Next actionable case U.15;
  retain the exact-object gap in U.14 for the next relevant batched build.

- [ X ] U.19 Reproduce and locate #26300 in the replacement workflow. Original
  attachment Clone BRep, saved placement, nine selected faces, 5 mm endmill,
  1 mm sampling, 5% stepover and saved depths exceed the isolated 120-second limit.
  Modern face masking replaces the removed legacy BoundaryEnforcement property;
  this is not an exact legacy-UI replay. A separate 55-second trace records
  Path.Area.getShape in surface_common._boundary_via_area at both 20 and 40 seconds,
  called while generating the selected-face mask. No OCL crash was observed.
  Individual projection plus planar union passed four simple geometry controls but
  failed on narrow trimmed faces; adding selected neighbours also stalled. Both
  candidates were removed, and source/installed module restored to committed code.
  This completes diagnosis only, not U.15 or the upstream issue.
  Evidence under the external root: `freeform-20260929-modern` (120-second timeout),
  `freeform-20260929-trace` (stacks and 55-second timeout), and
  `issue26300/diagnosis.json`. `tests/RunIssue26300.ps1` and the opt-in fixture test
  retain the reproduction without adding a hanging test to the default suite.
  Runner deadline behavior checked with a 30-second limit in
  `freeform-20260929-runner`; TIMEOUT is the expected diagnostic result, not PASS
  for toolpath generation. No native build, machine/post validation or release.
  Restored surface_common.py matches HEAD after CRLF normalization; source and
  installed SHA-256 now both
  `972F399E92F0509E4023556B4C057823429BBF9292652C51F4F13CE8B8CA097B`.
  The difference from U.13's raw hash is line endings only; no application change.

- [ X ] U.20 Stop partial-region fallback in build_optimized_boundary (#27950 /
  #27751). Inspection during U.15 found that a failed isolated face or connected
  group was silently omitted and failed union returned only the first boundary.
  This still affects the modern workflow and can remove requested keep-out areas;
  its wrong-toolpath impact takes priority over continuing projection experiments.
  Raise on missing/null/invalid region boundaries and failed/null/invalid union.
  Preserve all valid regions; the existing operation error path clears old paths.
  Five new checks cover isolated/group projection failure, union failure, valid
  disconnected exclusions and actual two-selection operation failure/stale-path
  clearing. Source and installed Python module SHA-256:
  `49647EC67FF15C603F341A71807640BB936E8C0FF0106632218AAD8B2EBB6003`.
  Evidence under the external root: `boundary-regions-20260929-red/results.json`
  reproduces three missing-error failures. `boundary-regions-20260929-green/results.json`
  has 59 related passes but an aggregate FAIL due to one exhausted mock in the
  new integration test. After making the fault repeatable across recomputes,
  `boundary-regions-20260929-focused/results.json` has all 14 focused checks PASS,
  no errors/skips. Application source unchanged between those two validation runs;
  together they establish 73 passing focused/related checks, not one all-pass batch.
  Python-only update installed; no native rebuild, schema change, legacy migration,
  or release. #26300 remains unresolved; U.14 and U.16 remain open.

- [ X ] U.21 Build and validate the bounded #6864 generator correction. Compiled
  only surface_generator.cpp using SelectedFiles, then relinked the existing CAM
  module; both commands exit 0. No full application/dependency rebuild. Added four
  regressions in TestIssueLineCoverage.py and replaced the older fixed-line-count
  expectation with endpoint/maximum-step checks. The regular grid alone missed
  1-5 mm at edges in the red fixtures. Additional passes sit at most 1e-6 mm inside
  contour extrema to accommodate the existing ray-cast boundary convention and
  still clip against the complete mask. No property/schema/default changes.
  `line-coverage-20260929-red/results.json` reproduces the defect;
  `line-coverage-20260929-final/results.json` reports 77 PASS, zero failures/errors/
  skips: 4 coverage, 14 avoidance, 12 common, 7 pattern, 18 operation and 22 mesh/tab.
  `line-build-20260929/build-result.json` records compile/link results and hashes.
  Installed `build/Mod/CAM/surface_generator.pyd` SHA-256:
  `B2BE185547170EB303508300A8B5639B9C301ABDFACDCD1BD0B364D101B65B94`.
  Updated TestSurfacePatternGenerator.py synchronized and hash-verified. Existing
  application version stamp remains unchanged. Default issue macro now includes
  the four coverage cases (93 tests); the full default has not run as one batch.
  This does not certify arbitrary contour finishing, legacy Surface, simulation,
  postprocessor output or physical machining. #26300 and exact U.14 remain open.

- [ X ] U.22 Reject lossy avoidance-outline fallback (#27950 / #27751 review).
  The replacement workflow still called TechDraw.findShapeOutline after failed
  hole-preserving projection. That API returns only an outer wire, silently
  filling holes in the exclusion and removing intended machining coverage.
  Unified UI changes do not obsolete this backend path. Now raise an actionable
  error before that fallback and clear the old operation path. Successful primary
  avoidance projection and outer-only cutting-outline fallback remain available.
  This deliberately rejects all avoidance requests that reach the lossy fallback,
  including triangulated avoidance inputs routed there; no general replacement
  projection algorithm is claimed. Direct STL machining/tab regressions still pass.
  Four added checks cover a holed selection, successful primary hole preservation,
  outer-outline fallback, and stale-path removal in a real operation. Two fail
  before the correction in `avoidance-fallback-20260929-red/results.json`.
  `avoidance-fallback-20260929-final/results.json`: 81 PASS, no failures/errors/skips
  (18 avoidance, 4 line coverage, 12 common, 7 pattern, 18 operation, 22 mesh/tab).
  Python-only update installed in the existing fork; no native build. Final
  docstrings synchronized after testing; executable statements unchanged.
  Source/installed surface_common.py SHA-256 in `module-manifest.json`:
  `0E23CD3491979F4346D21FC6FE3FDBDFA504D3AEFE057296F3147AF932F4D556`.
  Default issue macro now contains 97 tests; the entire default was not run as
  one batch. Exact U.14 GeomFillSurface and U.15 freeform timeout remain open.
  No legacy operation migration, postprocessor/machine acceptance or release.

- [ X ] U.23 Correct the reproduced #26300 freeform projection stall in the modern
  cutting-boundary pipeline. B-spline/Bezier selections use per-face tessellation
  at the operation's LinearDeflection, consistently oriented XY triangle union,
  and one offset per connected input group. Reuse Path.Area's NonZero polygon
  union without exact HLR or quadratic triangle nesting. Fill cutting-outline
  holes as Outline=True already did; explicit avoidance is subtracted separately.
  Failed face meshing, empty/invalid projection and invalid tolerance raise rather
  than dropping geometry or retrying the stalled exact projector. Non-freeform
  and avoidance projection remain on their existing paths. No new dependency,
  property, saved type or native build.
  Nine new analytic/fault checks cover seams, overlaps/reversed faces, islands,
  curved silhouette extrema, hole/avoidance behavior and failed/edge-on meshes.
  The original fixture now also verifies valid nonempty masks and every XY cutting
  endpoint inside the mask. `freeform-boundary-20260929-final/results.json` reports
  91 PASS, no failures/errors/skips: 9 boundary, 1 fixture and the prior 81 CAM
  checks. `freeform-details.json`: 14.05 seconds generation, 4,475 commands,
  4,235 G1 commands, 4,118 checked cutting endpoints, mask area 1336.60025 mm2.
  Baseline exceeded 120 seconds (U.19). The full fixture test also spends time on
  geometric assertions; elapsed generation is not whole-suite runtime.
  Earlier triangle-wire nesting timed out; a direct libarea experiment canceled
  overlaps under EvenOdd filling. Both failed candidates were discarded; overlap
  and sphere controls reject them. Retained implementation uses NonZero union.
  Source/installed surface_common.py SHA-256 in `module-manifest.json`:
  `873FA60DA4BDB414A1749219C8EBEC084F42DECBD55A33E537CD414009CB8D0C`.
  Default issue suite now has 106 tests; external-fixture test stays opt-in.
  Full default suite was not run together. This is a tessellated approximation,
  not an exact CAD boundary or general guarantee against all slow geometry.
  Native cancellation, legacy operation replay and machine/post acceptance are
  not established. Exact GeomFillSurface integration U.14 remains pending.

CAM avoidance evidence under the external validation root below:
`avoidance-tests-20260929-192717/results.json` reproduced four failing fault-handling
checks (two valid geometry controls passed). After correction,
`avoidance-tests-20260929-193013/results.json` reports 67 PASS, no errors/skips,
process 0. Eight focused, 12 common-generator, seven pattern-generator, 18 unified
operation and 22 STL/tab tests. `module-manifest.json` records installed Python
hashes. The expanded default issue macro now has 106 tests; it has not been run as a
single batch. Preserve the separate 75-test native and 67-test CAM evidence.

Reproduction evidence: `D:\Temp\Office-PC\freecad-plus-validation-20260928\issue-tests-20260929-185401`.
Existing binary run: 49 tests, 47 pass, two expected newly exposed Mirror failures,
no errors/skips, process exit 0. Translated feature-face plane is 2 mm off; rotated
case also fails. Three prior Mirror regressions and the new Body-face control pass.
The aggregate result is FAIL, not a successful validation of the pending fix.

Continuation evidence under the same external validation root (2026-09-29):
`recovery-tests-20260929-final/recovery-results.json` reports PASS for five fixtures;
`quantity-tests-20260929-191045/results.json` reports 23 tests PASS, no errors/skips;
`tree-tests-20260929-191256/results.json` reports one test PASS (both expand/collapse
subcases), no errors/skips. All processes exited 0. Earlier harness-development
runs are not acceptance evidence. These checks used existing native revision
`8abce719de` with source-loaded tests, not the unbuilt Mirror correction. Native
Qt event testing is distinct from physical viewport/keyboard acceptance.

Completed build checkpoint: `issue-build-20260929-191841/build-result.json` in the
same external root records compile/link exit 0, source hash, old/new Part module
hashes and the three synchronized script hashes. Updated `build/Mod/Part/Part.pyd`
SHA-256: `93D4E36312B52B6C0BF134F0A05351CFA3930EE5D0B35755C419E42AA78D5CA8`.
`issue-batch-20260929-191959/results.json`: all 75 PASS, no errors/skips, process 0.
The native version string remains `8abce719de`; the Part binary hash identifies
this targeted update. Launch the existing `build/bin/FreeCAD.exe` under the
external root to test it. No release, full rebuild or upstream publication.

## [ X ] Phase 1: Repository and instruction foundation

Outcome: an identifiable fork and usable project guidance.
Depends on: None.

### [ X ] 1.1 Establish the fork

Complete when: the repository, local checkout, remotes, and submodules are identified.

- [ X ] 1.1.1 Create the public `Croft-Labs/FreeCAD-Plus` fork and local checkout.
  Evidence: GitHub creation/verification in the setup session; upstream base `a5908bb06e`.
- [ X ] 1.1.2 Configure `origin` for the fork and `upstream` for FreeCAD; initialize submodules.
  Evidence: setup session verified remotes, recursive submodule status, and matching `main`.

### [ X ] 1.2 Adopt the shared instruction standard

Complete when: the root router, five core documents, and their references are checked.

- [ X ] 1.2.1 Add the local entry point and standard document ownership.
- [ X ] 1.2.2 Consolidate Pad guidance and preserve source/build/GUI distinctions.
  Evidence: documentation adoption change, with local link and heading checks on 2026-09-28.

## [   ] Phase 2: Pad task-pane workflow

Outcome: validated creation and editing through [UI-001](UI_UX_SPEC.md#ui-001-pad-task-pane).
Depends on: Phase 1.

### [ X ] 2.1 Implement the source change

Complete when: source and regression cases exist and source-level checks pass.

- [ X ] 2.1.1 Allow opening Pad without preselection; add profile controls to its shared create/edit dialog.
- [ X ] 2.1.2 Add selection restrictions, profile removal, and empty-profile handling.
- [ X ] 2.1.3 Add 14 GUI regression cases and register them in the GUI test suite.
  Evidence: local commit `e35fea1841`; C++ formatting, Python syntax, and whitespace checks passed.
  These checks do not establish compiled correctness or passing GUI tests.

<a id="pad-validation"></a>

### [   ] 2.2 Build and validate the changed application

Complete when: this fork builds and the focused suite plus manual UI acceptance pass.

- [ X ] 2.2.1 Configure a compatible FreeCAD LibPack and build outside Google Drive.
  Windows x64 Release GUI, Part, Sketcher, and Part Design targets built successfully.
  Fixed the profile selector to use `Shape.getShape()` for FreeCAD's `TopoShape`
  methods; `getValue()` returns the raw OpenCASCADE shape and did not compile.
- [ X ] 2.2.2 Correct and run the focused GUI regressions against the built fork.
  All 21 task-pane tests passed. Tests now search the active dialog, retain the
  layout's parent wrapper, and reopen via the user double-click entry point so
  edit transactions are exercised. The earlier `QPushButton` selector fix is included.
- [   ] 2.2.3 Verify viewport picking, rotated profiles, both directions, keyboard input,
  visibility restoration, Cancel, and Undo/Redo; check Pocket for shared-base regressions.
  Automated selection, visibility, Cancel, Undo/Redo, and Pocket regressions pass.
  Physical viewport/tree picking, rotated previews, keyboard navigation, and the
  complete advanced-parameter click-through remain manual acceptance work.
  Acceptance: [UI-001](UI_UX_SPEC.md#ui-001-pad-task-pane) and [test procedure](../tests/PadTaskPanel.md).
- [ X ] 2.2.4 Consolidate the configured application build and rerun all implemented
  workflow and related legacy regressions against matching runtime modules.
  Evidence: [2026-09-29 validation](#consolidated-validation), including two display
  scales, current version identity, installed-script matching and binary hashes.

<a id="extrude-validation-evidence"></a>

#### Validation evidence, 2026-09-28

Tested this checkout at `f9d592dc1f` plus the selector and test-fixture corrections
in this validation change. The source-built application reported FreeCAD 26.3.0;
the separately installed FreeCAD was not launched or used.

| Check | Result |
| --- | --- |
| Native model tests | `TestExtrude`: 8/8; existing `TestPad`: 14/14; existing `TestPocket`: 6/6. No failures, errors, or skips. |
| Native GUI tests | `TestPadTaskPanel`: 14/14; `TestExtrudeTaskPanel`: 7/7. No failures, errors, or skips. |
| Task-pane inspection | Captured and inspected Add and Subtract in the built GUI. Operation is first, Profile is second, and shared dimensions remain visible. |
| Toolbar and material result | One `PartDesign_Extrude` action in the modeling toolbar. The same `Pad` object and `Profile` produced 1080 mm3 in Add and 920 mm3 in Subtract. |
| Remaining limits | GUI tests use Qt controls and FreeCAD selection APIs; they do not establish physical mouse/keyboard acceptance. Unrelated workbenches, C++ developer tests, and cross-version recomputation in upstream FreeCAD were not tested. |

Build and test artifacts are outside Google Drive at
`D:\Temp\Office-PC\freecad-plus-validation-20260928`:
`configure-command.txt` / `configure.log`, `build-initial.log`, successful
`repair-compile.log`, `repair-resource0.log`, `repair-resource1.log`, `repair-link.log`,
`model-results.json`, `results.json`, per-suite logs, `visual-check.json`, and
`extrude-add.png` / `extrude-subtract.png`. Executable: `build\bin\FreeCAD.exe`.

The fork build used source-pinned `LibPack-26.3.0-v3.5.3-x64-Release` and MSVC
19.44.35211. Archive SHA-256:
`DCAA2D21F61B0607CF06B6E98F6E7525DC266C04C20E7B4D7B2C77BEC24366E7`.
Focused build and test reproduction guidance is in the
[development guide](DEVELOPMENT_GUIDE.md#commands). Settings and test documents
were isolated from the normal user profile. No push, installer, or release was made.

<a id="consolidated-validation"></a>

#### Consolidated validation, 2026-09-29

This evidence supersedes the older executable/version-stamp limitations recorded
in the individual feature milestones below. Native application source is commit
`8abce719de38a1b1ad255d0e7f4554a9d44e9c71`. This closeout adds a reusable validation
macro and documentation; no feature implementation change was needed.

| Check | Result |
| --- | --- |
| Configured Windows x64 Release build | Normal CMake ALL_BUILD completed with exit 0, including the main executable, core libraries, Part, Sketcher and Part Design App/Gui modules. Existing focused configuration; unrelated disabled workbenches and installer packaging are not included. |
| Build execution | The first bounded pass reached its 40-minute hard deadline after compiling core dependencies. A resumed incremental pass reused completed outputs and finished successfully in 1,680 seconds. Dependency/deprecation and temporary-directory warnings remain; no compiler error required a source fix. |
| Runtime identity | FreeCAD 26.3.0dev, revision 49009, hash `8abce719de`. Nine application/module binary hashes are recorded in the build manifest. |
| Source/runtime matching | All 80 checked Python files in Part BasicShapes/BOPTools/parttests and PartDesignTests match the checkout byte for byte. |
| Integrated regressions | **149/149 passed** in one initialized GUI: 84 model tests and 65 task tests. Zero failures, errors or skips; process exit 0. Baseline device-pixel ratio 1.5. Covers Extrude, Pad, Pocket, unified/legacy Patterns, MultiTransform, Revolve, Trim Body and Isocline. |
| Additional display scaling | The same **149/149 passed** with `QT_SCALE_FACTOR=1.5`; process exit 0. This multiplies the Windows scale rather than setting an absolute DPI: the reported device-pixel ratio was 2.25. Automated control/geometry checks do not establish readable layout or physical picking at that scale. |
| Native mouse/keyboard acceptance | Not completed. Window-control approval was granted, but capture returned `FrameArrived timed out` / `window capture timed out`. Accessibility inspection exposed an isolated fixture's close/save prompt. The user then stopped Computer Use with physical Escape; no further native input was issued. No manual acceptance gate is marked complete on that basis. |

Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
`closeout-build.log`, `closeout-build-results.json`, `closeout-build-resume.log`,
`closeout-build-resume-results.json`, `closeout-build-manifest.json`, and
`closeout-regressions/` / `closeout-highdpi/` (results, per-suite logs, process reports).
Reproduction: [`ValidateWorkflows.FCMacro`](../tests/ValidateWorkflows.FCMacro) and
[development-guide validation](DEVELOPMENT_GUIDE.md#validation).

Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
This is the updated development application, not a published installer. The separately
installed FreeCAD was not used. No push, publication, upstream round-trip validation,
or Linux/macOS acceptance is established by this work.

Remaining closeout gates: 2.2.3, the manual portions of 3.6.3/3.6.8, 3.7.4, 3.8.4,
3.9.4, 4.2.3 and 5.2.3. These need the documented viewport, keyboard and visual
acceptance checks; their builds and automated regressions are already complete.

## [   ] Phase 3: Further Part Design operations

Outcome: extend the complete task-pane workflow after Pad is validated and scope is authorized.
Depends on: milestone 2.2.

### [ X ] 3.1 Define the next operation

Complete when: an operation and its create/edit acceptance criteria are approved.

- [ X ] 3.1.1 Choose the next operation and define its input workflow.
  Evidence: user selected unified Pad/Pocket Extrude, with Add/Subtract as the first
  dropdown, and requested implementation on 2026-09-28.
  Plan paired operations as unified workflows under 3.6, rather than duplicating their
  new task controls. The individual tasks below remain coverage checks for both modes.
- [ X ] 3.1.2 Audit Part Design profile selection and shared create/edit task workflows.
  Evidence: source review on 2026-09-28 at `e0517bc4bd`, recorded below. No application
  or GUI tests were run for this audit; the installed FreeCAD was not used.

<a id="part-design-workflow-audit"></a>

#### Profile-selection findings

**Ten remaining operations share Pad's former startup workflow:** Pocket, Hole,
Revolution, Groove, Additive Loft, Subtractive Loft, Additive Pipe, Subtractive Pipe,
Additive Helix, and Subtractive Helix. Pad's source change is already recorded in
milestone 2.1; its acceptance remains in [milestone 2.2](#pad-validation).
This inventory describes the audited baseline. Pocket's subsequent source update
is tracked in 3.6.3; it no longer uses that startup picker without preselection.

In [`Command.cpp`](../src/Mod/PartDesign/Gui/Command.cpp), these ten commands call
`prepareProfileBased`. Without preselection, it searches for sketches, automatically
uses the sole eligible sketch, or opens a separate `TaskDlgFeaturePick`; it can reject
the command when no sketch exists. Thus, preselection is not literally mandatory in
every case, but the main feature editor cannot simply open with an empty profile
and let the user choose its inputs there. Required Body/base-solid prerequisites
remain legitimate, particularly for subtractive operations.

`finishFeature` opens edit mode, and
[`ViewProvider::setEdit`](../src/Mod/PartDesign/Gui/ViewProvider.cpp) obtains
`getEditDialog` for both newly created and existing features. These operations already
share their main dialog between creation and editing; that alone does not make the
definition fully editable. The following table separates missing profile controls
from existing controls that need a better entry workflow.

| Operation | Profile editing in the current task pane | Planned work / owning task |
| --- | --- | --- |
| Pad | New profile list supports selection, removal, and clearing in the shared editor. | Validate existing implementation in 2.2; include it in the complete-parameter audit in 3.4.1. |
| Pocket | [`TaskPocketParameters`](../src/Mod/PartDesign/Gui/TaskPocketParameters.cpp) uses the shared extrusion controls but has no Pad-style profile editor. | 3.2.1: open empty; add the profile section while retaining extent, direction, and start/end references. |
| Hole | [`TaskHoleParameters`](../src/Mod/PartDesign/Gui/TaskHoleParameters.cpp) edits hole settings and start references, not the `Profile` link. Its base-profile-type filter does not replace source selection. | 3.2.2: open empty; select/replace hole inputs and preserve supported circles, arcs, and points, plus size, depth, thread, and cut options. |
| Revolution | [`TaskRevolutionParameters`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.cpp) selects axis/start references but does not replace `Profile`. | 3.2.3: profile section plus existing angle, axis, direction, and extent controls. |
| Groove | Shares the revolution parameter implementation; no profile replacement control. | 3.2.4: the equivalent subtractive workflow, including base-solid validation. |
| Additive Helix | [`TaskHelixParameters`](../src/Mod/PartDesign/Gui/TaskHelixParameters.cpp) selects the axis but does not replace `Profile`. | 3.2.5: profile section plus helix modes, dimensions, axis, and handedness. |
| Subtractive Helix | Shares the helix editor and the missing profile control. | 3.2.6: equivalent subtractive workflow, including base-solid validation. |
| Additive Loft | [`TaskLoftParameters`](../src/Mod/PartDesign/Gui/TaskLoftParameters.cpp) already replaces the base profile and adds/removes/reorders sections. A profile pick replaces the link with one picked source/subelement; it is not Pad's accumulated curve list. | 3.3.1: enter directly with empty inputs; expose clear profile/section lists and preserve ordered-section editing. |
| Subtractive Loft | Same selectors and startup gate as Additive Loft. | 3.3.2: equivalent subtractive workflow. |
| Additive Pipe | [`TaskPipeParameters`](../src/Mod/PartDesign/Gui/TaskPipeParameters.cpp) already replaces the profile and edits spine references. Orientation and section/scaling controls share the task dialog. | 3.3.3: enter directly with empty inputs; complete profile, path, auxiliary-reference, and section editing in that dialog. |
| Subtractive Pipe | Same selectors and startup gate as Additive Pipe. | 3.3.4: equivalent subtractive workflow. |

#### Other Part Design features: complete-editing audit

Inventory follows the registered commands and menus in
[`Workbench.cpp`](../src/Mod/PartDesign/Gui/Workbench.cpp) and `Command.cpp`.
An existing selector below is source evidence, not a claim of full GUI acceptance.
These features must not be counted as ten additional profile-startup defects.

| Features | Source finding | Remaining work |
| --- | --- | --- |
| Mirrored, Linear Pattern, Polar Pattern | `prepareTransformed` can start without selected originals using Whole shape mode. [`TaskTransformedParameters`](../src/Mod/PartDesign/Gui/TaskTransformedParameters.cpp) adds/removes originals and changes mode. [`TaskMirroredParameters`](../src/Mod/PartDesign/Gui/TaskMirroredParameters.cpp) and [`TaskPatternParameters`](../src/Mod/PartDesign/Gui/TaskPatternParameters.cpp) provide reference/parameter controls in the reused editors. | 3.4.2: verify originals, whole-shape mode, plane/axes/directions, counts and spacing/angles on both create and reopen. No Pad-style profile prerequisite identified. |
| MultiTransform, including Scale | [`TaskMultiTransformParameters`](../src/Mod/PartDesign/Gui/TaskMultiTransformParameters.cpp) manages an ordered transformation list and embedded editors for mirror, linear, polar, and scale operations. | 3.4.2: verify adding, editing, removing, and ordering child transformations without leaving the parent task. Standalone `PartDesign_Scaled` registration is commented out; do not count it as a normal menu command. |
| Circular Pattern, Path Pattern, Point Pattern model types | `TaskPatternParameters` contains controls for these model types, but the audited Part Design command/menu registration does not expose standalone commands for them. | 3.4.2: cover existing documents containing these types and establish supported entry paths before proposing new commands. Do not infer a missing-curve-startup defect from class names alone. |
| Fillet, Chamfer, Draft, Thickness, Defeaturing | Commands accept no preselection and use the active Body Tip. [`TaskDressUpParameters`](../src/Mod/PartDesign/Gui/TaskDressUpParameters.cpp) edits edge/face references on the existing base. Individual task panels hold operation parameters; Draft also selects neutral-plane/pull-direction references. | 3.4.3: validate all subelement and parameter changes. The selector fixes the source to the current base object: define safe base replacement or explain a required Body-history constraint inside the task. |
| Boolean | The command can create an empty tool list; [`TaskBooleanParameters`](../src/Mod/PartDesign/Gui/TaskBooleanParameters.cpp) adds/removes tools and changes operation type in the shared editor. | 3.4.4: verify tool replacement/removal, operation switching, empty-state recovery, and Body dependency restrictions. |
| Additive and Subtractive Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism, Wedge | [`CommandPrimitive.cpp`](../src/Mod/PartDesign/Gui/CommandPrimitive.cpp) creates these without curve input. [`TaskPrimitiveParameters`](../src/Mod/PartDesign/Gui/TaskPrimitiveParameters.cpp) combines geometry controls, attachment, and preview in the edit dialog. | 3.4.5: verify dimensions and placement/attachment for all 16 variants on create and reopen. Changing to a different primitive class is not ordinary parameter editing. |
| Shape Binder | [`TaskShapeBinder`](../src/Mod/PartDesign/Gui/TaskShapeBinder.cpp) supports selecting, changing, and clearing support references. Creation and editing use its task dialog. | 3.5.1: verify empty startup, support changes, tracking options, and transaction behavior. |
| Sub-Shape Binder | The command directly creates/links the binder. [`ViewProviderSubShapeBinder`](../src/Mod/PartDesign/Gui/ViewProviderShapeBinder.cpp) supplies synchronize/select-source actions, without a dedicated definition task editor. | 3.5.2: add a shared create/edit task for supports and applicable binding options. This is a task-editor gap, not the profile-based startup gate. |
| Clone / Base Feature | `CmdPartDesignClone` requires exactly one selected Part feature and directly creates a new Body/base feature. [`ViewProviderBase`](../src/Mod/PartDesign/Gui/ViewProviderBase.cpp) exposes placement editing when mutable, not a complete source-definition editor. | 3.5.3: plan one create/edit task for source and supported placement changes, preserving base-feature and Body semantics. |
| Datum Point, Datum Line, Datum Plane, Coordinate System | Current menus invoke Part datum commands. [`ViewProviderDatum`](../src/Mod/Part/Gui/ViewProviderDatum.cpp) routes to the attachment editor, including from creation. | 3.5.4: verify support, attachment mode, and offsets through the same task; these are reference geometry, not extrusion-profile features. |
| Involute Gear, Sprocket | [`InvoluteGearFeature.py`](../src/Mod/PartDesign/InvoluteGearFeature.py) and [`SprocketFeature.py`](../src/Mod/PartDesign/SprocketFeature.py) create objects then enter their respective task editors; editing reuses those panels. | 3.5.5: compare editable model properties against panel controls and test both entry paths. The standalone `fcsprocketdialog.py` demo is not the workbench command's editor. |
| Shaft Design Wizard, when available | [`WizardShaft.py`](../src/Mod/PartDesign/WizardShaft/WizardShaft.py) opens a task workflow, conditionally exposed by the workbench. It is not routed through the standard feature `getEditDialog` path. | 3.5.6: inspect generated-object re-entry and rollback before claiming create/edit parity; availability and behavior remain unverified. |

Sketch creation/editing belongs to the dedicated Sketcher workflow. Editing source
sketch geometry is distinct from selecting a feature's profile. Body creation,
setting Tip, moving/duplicating objects, material tools, and geometry inspection are
management or inspection actions rather than profile-consuming feature definitions;
they are outside this feature-dialog backlog.

**Cross-cutting parameter gap:**
[`FeatureRefine.cpp`](../src/Mod/PartDesign/App/FeatureRefine.cpp) defines editable
`Refine` and `FuzzyTolerance` properties, inherited by profile features, dress-ups,
transformations, primitives, and Boolean. The audited Part Design task-panel sources
contain no controls for these properties. Therefore even panels with input selectors
cannot yet be declared complete replacements for property-editor changes. Task 3.4.1
owns the common controls and the remaining property-by-property coverage audit.

<a id="feature-task-acceptance"></a>

#### Acceptance for every feature implementation milestone

These are backlog completion criteria. Detailed operation-specific screen behavior
belongs in the UI specification when that operation is selected for implementation.

1. Creating and reopening use the same task container and controls. For unified
   Add/Subtract families, Operation is first, immediately followed by geometry inputs
   showing existing selections and supporting selection after invocation.
   Multiple sections within that task are acceptable; a separate prerequisite picker
   or property-editor detour must not be required to define the feature.
2. Add, remove, clear, and replace inputs as supported by the feature; reorder ordered
   inputs such as loft sections and transformation steps. Retain valid preselection.
   Match each model's supported geometry, including Hole points/arcs, pipe paths, and
   loft sections; do not impose Pad's profile restrictions on every feature.
3. Cover the feature's editable definition: dimensions, modes, references, directions,
   secondary extents, advanced geometry options, and applicable placement/attachment.
   Audit persisted properties against controls, preserving units and expressions.
   Computed/internal properties and incompatible object-class changes are excluded;
   any intentionally fixed structural dependency must have an explicit rationale.
4. Empty/incomplete inputs stay editable with clear guidance and safe preview behavior.
   Invalid geometry or dependency cycles cannot be accepted. Inspect constructors,
   gizmos, and selection handlers for null-profile assumptions before bypassing pickers.
5. Verify create with/without preselection, reopen and replace inputs, change each
   supported mode, clear/recover, accept/save/reopen, Cancel, and Undo/Redo. Check tree
   and viewport picking, visibility restoration, and unchanged downstream dependencies.
   Run focused regressions in the built fork and manual viewport acceptance; record
   source, build, test, and GUI evidence separately.

### [   ] 3.2 Add missing in-task profile controls

Depends on: 2.2 and 3.1.1 for the selected operation.
Complete when: each operation passes the [common acceptance](#feature-task-acceptance),
including profile replacement while editing an existing feature.

- [   ] 3.2.1 Pocket: replace the startup picker with the shared feature task and profile controls.
  Source and automated validation completed through 3.6.3; manual viewport
  acceptance remains in 2.2.3.
- [   ] 3.2.2 Hole: add input selection with Hole-specific geometry rules.
- [   ] 3.2.3 Revolution: add profile selection alongside axis and revolution controls.
- [   ] 3.2.4 Groove: provide equivalent subtractive profile editing.
- [   ] 3.2.5 Additive Helix: add profile selection alongside helix controls.
- [   ] 3.2.6 Subtractive Helix: provide equivalent subtractive profile editing.

### [   ] 3.3 Complete Loft and Pipe input workflows

Depends on: 2.2 and operation-specific scope under 3.1.1.
Complete when: all four operations open their main task with empty inputs and pass
the [common acceptance](#feature-task-acceptance), reusing their existing selectors.

- [   ] 3.3.1 Additive Loft: integrate base-profile and ordered-section selection from startup.
- [   ] 3.3.2 Subtractive Loft: integrate the equivalent subtractive workflow.
- [   ] 3.3.3 Additive Pipe: integrate profile, spine, auxiliary references, and section/scaling controls.
- [   ] 3.3.4 Subtractive Pipe: integrate the equivalent subtractive workflow.

### [   ] 3.4 Close complete-editing gaps in solid features

Depends on: 2.2 and scoped implementation choices in 3.1.1; may proceed by family.
Complete when: the common parameter gap is addressed and each listed family passes
the [common acceptance](#feature-task-acceptance). Existing controls need validation,
not automatic replacement.

- [   ] 3.4.1 Add shared advanced geometry controls for `Refine` and `FuzzyTolerance`
  where applicable; inventory other editable properties missing from each task,
  including Pad, and implement required controls with regression coverage.
- [   ] 3.4.2 Validate Mirrored, Linear/Polar Pattern, and MultiTransform create/edit
  parity, including nested Scale and supported Circular/Path/Point Pattern objects.
- [   ] 3.4.3 Complete Fillet, Chamfer, Draft, Thickness, and Defeaturing reference/parameter
  editing; resolve the current fixed-base selection boundary without invalid history.
- [   ] 3.4.4 Validate Boolean's complete tool and operation workflow.
- [   ] 3.4.5 Validate all additive/subtractive primitive dimensions and attachment workflows.

### [   ] 3.5 Complete supporting-feature task workflows

Depends on: scoped implementation choices in 3.1.1 and the common acceptance criteria.
Complete when: each included helper has a documented and validated create/edit path;
conditional wizard scope is explicitly resolved.

- [   ] 3.5.1 Validate Shape Binder support and parameter editing.
- [   ] 3.5.2 Implement a shared Sub-Shape Binder definition task.
- [   ] 3.5.3 Implement Clone source/placement creation and editing in one task.
- [   ] 3.5.4 Validate datum and coordinate-system attachment editing.
- [   ] 3.5.5 Audit and complete Involute Gear and Sprocket task parameter coverage.
- [   ] 3.5.6 Establish Shaft Design Wizard availability and edit/re-entry semantics;
  resolve any missing persisted-definition and cancel behavior before scheduling a fix.

<a id="unified-feature-workflows"></a>

### [   ] 3.6 Unify opposite operations into geometry workflows

Outcome: implement the user's preferred one-command workflow with Add/Subtract in
the task pane, as defined by [REQ-008/009](PRODUCT_SPEC.md#capabilities-and-requirements)
and the [shared interaction](UI_UX_SPEC.md#planned-unified-feature-interaction).
Depends on: 2.2, operation-specific selection coverage in 3.2/3.3/3.4, and a safe
operation-switching design. These can be developed together by feature family;
finishing all separate commands first is not required.
Complete when: each selected family passes the [common acceptance](#feature-task-acceptance)
plus operation-switching and legacy-document regressions below.

#### Strong candidates: additive/subtractive pairs

Source-backed planning inventory, 2026-09-28. Names below are proposed primary
commands; existing API/document type names remain compatibility concerns.

| Proposed command | Current features combined | Common parameters / inputs | Differences to preserve |
| --- | --- | --- | --- |
| Extrude | Pad + Pocket | Profile, start plane/offset, direction, side arrangement, lengths, limiting references, taper | Extent modes differ: Pad has UpToLast, Pocket has ThroughAll. Map modes by meaning, not enum index; validate direction and material result when switching. |
| Revolve | Revolution + Groove | Profile, axis, angle, side arrangement, start and limiting references | Retain each mode's extent/geometry rules and the subtractive base-solid prerequisite. |
| Loft | Additive Loft + Subtractive Loft | Base profile, ordered sections, ruled/closed options | Keep section compatibility and additive/subtractive result validation. |
| Sweep (Pipe) | Additive Pipe + Subtractive Pipe | Profile, spine, orientation, auxiliary spine, section/scaling options | Preserve path/section semantics and validate the resulting union or cut. |
| Helix | Additive Helix + Subtractive Helix | Profile, axis, pitch/height/turns modes, handedness, growth | Preserve helix mode dependencies and existing subtractive intersection/outside compatibility. |
| Box | Additive Box + Subtractive Box | Length, width, height, placement/attachment | Same primitive geometry; operation changes how it combines with the Body. |
| Cylinder | Additive Cylinder + Subtractive Cylinder | Radius, height, angle, placement/attachment | Same primitive geometry; validate union/cut result. |
| Sphere | Additive Sphere + Subtractive Sphere | Radius, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Cone | Additive Cone + Subtractive Cone | Radii, height, angle, placement/attachment | Same primitive geometry; validate union/cut result. |
| Ellipsoid | Additive Ellipsoid + Subtractive Ellipsoid | Radii, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Torus | Additive Torus + Subtractive Torus | Radii, angular limits, placement/attachment | Same primitive geometry; validate union/cut result. |
| Prism | Additive Prism + Subtractive Prism | Polygon count, radius, height, placement/attachment | Same primitive geometry; validate union/cut result. |
| Wedge | Additive Wedge + Subtractive Wedge | Wedge bounds/dimensions, placement/attachment | Same primitive geometry; validate union/cut result. |

This combines **26 existing feature variants into 13 paired workflows**. The eight
primitive workflows can also share one **Primitive** command with a shape selector,
yielding six top-level families: Extrude, Revolve, Loft, Sweep, Helix, Primitive.
Changing an existing primitive's shape type needs its own compatibility design;
it is not implied by changing Add/Subtract for that same primitive.

#### Additional consolidation options

| Candidate | Possible shared workflow | Recommendation / boundary |
| --- | --- | --- |
| Linear Pattern, Polar Pattern, Mirrored; MultiTransform with Scale | Pattern/Transform with a type selector and shared original-feature list | A useful second-stage consolidation, but these are different transformations, not Add/Subtract opposites. Reuse MultiTransform's step editing; retain type-specific parameters. Circular/Path/Point model types need supported entry-path review under 3.4.2. |
| Boolean union, subtraction, intersection | Boolean with operation and tool-body selectors | Already one feature/editor; align naming and interaction with the shared operation selector rather than create another command. |
| Fillet and Chamfer | Optional Edge Treatment command with Round/Chamfer type | Shared edge selection is reusable, but curvature and parameter semantics differ. Lower priority than true additive/subtractive pairs; combining them is an option, not an agreed requirement. |

Keep **Hole** specialized for hole standards, threads, and counterbores/countersinks.
Keep Draft, Thickness, and Defeaturing distinct: they modify geometry in different
ways and are not opposite operations. Binders, Clone, datums, gears, and sketches
retain their own workflows while sharing appropriate selection and task conventions.

#### Implementation evidence and constraints

- Extrude already shares [`TaskExtrudeParameters`](../src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp).
  Revolution/Groove share [`TaskRevolutionParameters`](../src/Mod/PartDesign/Gui/TaskRevolutionParameters.cpp);
  Loft, Pipe, Helix, and primitive pairs also reuse their family task implementation.
  UI consolidation can build on those existing paths.
- [`FeatureAddSub`](../src/Mod/PartDesign/App/FeatureAddSub.cpp) already defines an
  `Operation` property, but `defineAdditive` restricts it to Union and
  `defineSubtractive` to Subtraction/Common. Existing operation controls do not make
  all feature types freely interchangeable. Inspect each geometry execution path
  and persistence behavior before implementing a shared selector.
- [`Pad::TypeEnums`](../src/Mod/PartDesign/App/FeaturePad.cpp) and
  [`Pocket::TypeEnums`](../src/Mod/PartDesign/App/FeaturePocket.cpp) demonstrate why
  copying raw property indices between feature types is unsafe. Preserve common
  parameters by meaning and identify incompatible settings explicitly.
- Unifying command presentation is separate from changing a stored object class.
  Decide how switching a committed feature between Add/Subtract preserves its
  identity, dependent links, expressions, and recompute history. Do not silently
  delete/recreate features or rename existing serialized types to match toolbar labels.

- [ X ] 3.6.1 Inventory combined-workflow candidates and record the preferred interaction.
  Evidence: the paired-feature/source mapping above; this is design documentation only.
- [ X ] 3.6.2 Define and validate the operation-switching compatibility approach;
  inventory parameter mappings, existing Common behavior, and legacy entry points.
  Source approach: retain Pad/Pocket objects and their links; append enum choices
  without changing legacy indices; match extent modes by name; restore old Operation
  lists with the saved meaning intact. Geometry direction remains independent of
  Add/Subtract. Existing Common features keep Intersect in their dropdown. Save/reopen
  and legacy-document model regressions passed, along with both legacy GUI entry
  points; see [evidence](#extrude-validation-evidence). Cross-version recomputation
  of switched features in unmodified upstream FreeCAD is not established.
- [   ] 3.6.3 Implement Extrude as the recommended first unified family, integrating
  Pad validation and Pocket task 3.2.1 rather than creating duplicate new controls.
  Source implemented on 2026-09-28: `PartDesign_Extrude` replaces the two standard
  menu/toolbar entries; legacy commands remain available. Both feature types share
  Extrude Parameters with Operation first, then Profile, and the existing dimensions.
  Switching changes the same object's Operation; To last and Through all remain
  separate choices. Subtract/Intersect require a base solid; incomplete tasks remain editable.
  Eight new model regressions, seven new GUI regressions, fourteen Pad GUI cases,
  and twenty existing Pad/Pocket model cases all pass in the built fork. The native
  build found and resolved the profile-selector API error recorded in 2.2.1.
  Task-pane layout and the single toolbar command were inspected in the built GUI.
  Source formatting, Python syntax, documentation links, and whitespace checks pass.
  Remaining gate: manual viewport/keyboard acceptance in 2.2.3; passing automated
  checks do not complete the common acceptance criteria for this milestone.
- [   ] 3.6.4 Implement Revolve, covering both tasks 3.2.3 and 3.2.4.
- [   ] 3.6.5 Implement Loft and Sweep, covering all four tasks in 3.3.
- [   ] 3.6.6 Implement Helix, covering tasks 3.2.5 and 3.2.6.
- [   ] 3.6.7 Implement paired primitive workflows and decide whether to expose them
  through one Primitive command; validate all eight shapes in both operations.
- [   ] 3.6.8 Verify Add-to-Subtract and Subtract-to-Add during creation and on reopened
  features: common parameter retention, incompatible-mode guidance, no-base handling,
  preview/recompute, dependent links and expressions, save/reopen, Cancel, and Undo/Redo.
  Test existing additive, subtractive, and Common documents and legacy commands.
  Automated coverage passed for both operations and legacy entry points, including
  parameter/identity retention, base-solid validation, save/reopen, Cancel, and
  Undo/Redo. Finish the manual rotated/reference/custom-direction, taper, start/end
  reference, and downstream-pattern scenarios in the [test procedure](../tests/PadTaskPanel.md).


<a id="combined-pattern-workflow"></a>

### [   ] 3.7 Combined Linear/Circular Pattern workflow

Outcome: [UI-002](UI_UX_SPEC.md#ui-002-pattern-task-pane) satisfies REQ-010/011/012.
Authorized by the user's request to combine pattern buttons with type first,
features second, and direction/axis and parameters after them. This advances the
Linear/Polar portion of 3.4.2; Mirror, Path, Point, concentric CircularPattern, and
other MultiTransform consolidation remain separate future work.

- [ X ] 3.7.1 Implement one Pattern command in standard menus/toolbars/task watchers.
  Creation without preselection and reopening the new Pattern share the same pane.
  Linear/Circular is first, followed by selected features and mode-specific controls.
  Keep legacy Linear/Polar commands and their persisted types unchanged.
- [ X ] 3.7.2 Preserve result identity and separate mode settings using a new
  `PartDesign::Pattern` feature backed by the existing MultiTransform engine.
  The result owns Linear/Polar parameter helpers in the same Body. Switching selects
  an existing helper; it does not replace the result, expressions, or original links.
  Empty patterns stay editable and cannot be accepted. Feature picks reject other
  bodies and dependents; list removal uses identity instead of labels/history order.
- [ X ] 3.7.3 Build and run model/GUI regressions and inspect the actual task layout.
  Windows x64 Release PartDesign App/Gui modules rebuilt with the existing MSVC/Qt
  LibPack configuration outside Google Drive. All **91 tests pass**: 58 model tests
  (Pattern 5, Linear 16, Polar 6, MultiTransform 3, Extrude 8, Pad 14, Pocket 6),
  plus 33 GUI tests (Pattern 12, Pad 14, Extrude 7), with no failures/errors/skips.
  Qt tests cover field ordering, no-preselection/face picking, mode switching, real
  direction/spacing/count controls, retained expressions, feature removal with
  duplicate labels/out-of-history order, invalid-body/dependent picks, empty-input
  rejection/recovery, same-pane reopening, Cancel, Undo/Redo, and legacy commands.
  Disabled live preview is honored and OK recomputes the final result.
  Existing MultiTransform embedded editing also passes. Corrected a Cancel cleanup
  path that could reapply parameters after rollback, and hid the embedded task
  controller to avoid overlaying the initial pane header.
  Task captures show Linear and Circular layouts in the requested order. The same
  Pattern result computes 8024 mm3 with three linear instances and 8032 mm3 with four
  circular instances in the regression fixture. Physical interaction remains 3.7.4.
  Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
  `pattern-model-results.json`, `pattern-gui-results.json`, `pattern-visual-check.json`,
  `pattern-linear.png`, `pattern-circular.png`, and `pattern-build-*.log`.
  The initial build found a task-header API mismatch, corrected to `setHeaderText`.
  The GUI harness invokes FreeCAD's unsigned count slot; using Qt's signed setter
  initially requested an excessive count, so that run was stopped and corrected.
  Final build/link and runtime reports supersede those intermediate failures.
  Source formatting, Python syntax, whitespace, and documentation checks pass.
  Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
  This is an incremental development build; its About/version stamp still reflects
  the earlier main-executable build, while the changed App/Gui modules are rebuilt.
- [   ] 3.7.4 Complete physical viewport/keyboard/high-DPI acceptance using
  [the Pattern procedure](../tests/PatternTaskPanel.md). Automated Qt interaction and
  captured layout inspection do not establish this manual gate.

Compatibility boundary: old Linear/Polar features keep their existing full editor;
there is no automatic conversion to the new type. Unmodified upstream FreeCAD does
not recognize `PartDesign::Pattern`; cross-version recomputation and release packaging
are not established. This work is local and does not authorize a push or publication.

### [   ] 3.8 Extrude start offset and direction controls

Outcome: REQ-013 is available in the shared new/edit Extrude pane for Pad and Pocket.
Existing signed StartOffset, StartType, and Reversed properties retain their model
semantics; no stored property or object migration is introduced.

- [ X ] 3.8.1 Expose the zero-default start offset in all three direction modes,
  automatically activate Offset when a distance is entered, and add a flip button
  that negates the value or its expression. Retain reference starts and explicit
  Profile plane reset.
- [ X ] 3.8.2 Replace the Reversed checkbox with synchronized buttons beside each
  length. Keep reversal beside Type for non-dimensional extents and disable it for
  symmetric Dimension. Keep the start-offset viewport gizmo available at zero.
- [ X ] 3.8.3 Rebuild the GUI module and run native geometry/task regressions; inspect
  the actual task-pane layout. Windows x64 Release GUI module rebuilt and linked
  using the existing MSVC/Qt LibPack environment outside Google Drive. All **42 GUI
  tests pass**: Extrude 16 (nine new cases), Pad 14, Pattern 12; no failures/errors/skips.
  Native tests assert positive/negative offset geometry in all three modes,
  Add/Subtract and legacy Pocket behavior, both synchronized length buttons,
  non-dimensional reversal, reference starts, expression flipping and rollback,
  save/reopen, Cancel, and Undo/Redo. Captured one-sided, two-sided, and symmetric
  task layouts were inspected; offset and length buttons align with their fields.
  Formatting, Python syntax, UI XML, whitespace, and documentation checks pass.
  Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
  `extrude-offset-gui-results.json`, `extrude-offset-visual-check.json`,
  `extrude-offset-one-side.png`, `extrude-offset-two-sides.png`,
  `extrude-offset-symmetric.png`, and `extrude-offset-build-*.log`.
  Final successful compile/link and tests supersede intermediate compile errors
  from a protected expression-widget API and a removed checkbox reference.
  Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
  Incremental GUI module update; the main executable About/version stamp still
  reflects its earlier build. The separately installed FreeCAD was not used.
- [   ] 3.8.4 Complete physical viewport/keyboard/high-DPI acceptance using the
  [Extrude procedure](../tests/PadTaskPanel.md#start-offset-and-direction-buttons).
- [ X ] 3.8.5 Verify Add/Subtract offsets across the full dimension-mode matrix.
  User-requested follow-up passed in the same source-built GUI: **72 geometry
  scenarios** (Extrude and legacy Pocket commands, Add/Subtract, one-sided/two-sided/
  symmetric, normal/reversed extrusion, and 0/+2/-2 mm offsets). Negative offsets
  use the real flip button. Each result is a valid single solid with the expected
  analytical volume, bounding box, and zero excess/missing volume against an
  independently constructed box union/cut. Accepted features reopen correctly;
  flipping after reopening and Cancel restore the expected solids. All **17 Extrude
  GUI tests pass**, including existing expression, reference, save/reopen, and
  Undo/Redo cases, with no failures/errors/skips. No implementation fix was needed.
  Evidence in the directory above: `extrude-offset-operations-gui-results.json`
  and `extrude-offset-operations-TestExtrudeTaskPanel.log`. Only tests/documentation
  changed for this follow-up; no binary rebuild was required.

This work is local; publication and release packaging are not part of this task.

### [   ] 3.9 Revolve/Groove angular start offsets

Outcome: REQ-014 in the shared Revolution (Add) and Groove (Subtract) create/edit
pane. This user-authorized angular-control change does not complete command/profile
consolidation in 3.6.4 or the broader Revolve/Groove workflow audit.

- [ X ] 3.9.1 Expose the existing signed StartOffset in all three side modes with
  default 0 degrees, inclusive -360/+360 endpoints, and automatic Offset activation.
  Add a sign-flip button preserving expressions and reference-start behavior.
- [ X ] 3.9.2 Replace Reversed with synchronized buttons beside each angular
  magnitude; keep reversal available for reference extents and disabled for
  symmetric angular sweeps. Keep the start-offset gizmo available at zero.
- [ X ] 3.9.3 Build and verify native geometry, controls, persistence, and task layout.
  Windows x64 Release PartDesignGui rebuilt and linked in the existing isolated
  MSVC/Qt LibPack environment. All **25 tests pass**: five new Revolve task tests,
  three existing Revolve model tests, and 17 Extrude task regressions; no failures,
  errors, or skips. The new suite includes **84 geometry scenarios** across Add and
  Subtract, three side modes, normal/reversed axes, and 0/+45/-45/+180/-180/+360/-360
  degree offsets. Independent cylindrical sectors verify analytical volume, exact
  bounds, and both geometric differences. Offset endpoints stay numerically +/-360
  through acceptance and reopening. Both buttons, zero default, range limits,
  expressions, reset/rollback, Cancel, Undo/Redo, and save/reopen pass for both types.
  Initial post-render bounds checks used display triangulation; corrected the test
  oracle to exact `optimalBoundingBox(False)` without relaxing geometric tolerances.
  Captured and inspected all three task modes for Revolution and Groove after Qt
  layout animations settled. Physical interaction remains task 3.9.4.
  C++ formatting, Python syntax, UI XML, whitespace, and documentation checks pass.
  Evidence: `D:\Temp\Office-PC\freecad-plus-validation-20260928`,
  `revolve-offset-gui-results.json`, `revolve-offset-visual-check.json`,
  `revolve-offset-add-*.png`, `revolve-offset-subtract-*.png`, and
  `revolve-offset-build-*.log`.
  Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
  Incremental GUI module update; the main executable About/version stamp still
  reflects its earlier build. The separately installed FreeCAD was not used.
  Follow-up user-requested verification on local commit `84c34732ef`: all eight
  focused tests passed (five Revolve task tests and three Revolve model tests),
  with **84 individually recorded geometry scenarios: 42 Add and 42 Subtract**.
  No failures/errors/skips and no implementation fix required. Source/build test
  copies matched; the existing development GUI module was used. Detailed report:
  `revolve-offset-verify-gui-results.json` in the evidence directory above.
- [   ] 3.9.4 Complete physical viewport, keyboard, and high-DPI acceptance using
  [the Revolve test procedure](../tests/RevolveTaskPanel.md).

This work preserves existing stored feature types and properties; command
consolidation, push/publication, and release packaging remain outside this task.


<a id="trim-body"></a>

## [   ] Phase 4: Associative Trim Body

Outcome: select a target solid/sheet, cutter, and side to keep in one complete
create/edit task, available from Part and Part Design. User-authorized scope;
requirements REQ-015 through REQ-017 and [UI-004](UI_UX_SPEC.md#ui-004-trim-body-task-pane).
Depends on: the existing Part geometry engine and native development build.

### [ X ] 4.1 Implement geometry and shared task

- [ X ] 4.1.1 Add a linked Trim Body feature reusing Part half-spaces, Boolean
  common/cut, and BOPTools SplitAPI. Support datum planes, planar/curved faces,
  connected sheets, solid/sheet targets, planar extension, and reversible keep side.
  Reject incomplete or nonintersecting cuts and invalid solid closure.
- [ X ] 4.1.2 Add Target then Tool selectors, side reversal and green viewport arrow,
  live preview, refine/planar-extension controls, and error recovery in one new/edit
  pane. Register the same command in both workbenches' menus and toolbars.
- [ X ] 4.1.3 Persist input links, track parent-container placement changes, and
  preserve transaction/visibility behavior. Keep source objects and Part Design
  Body Tip unchanged; the result is a separate Part::FeaturePython object.

### [   ] 4.2 Validate and prepare the local test build

- [ X ] 4.1.4 Reject stale dependency results in the Trim Body task pane after
  recompute. Keep the dialog open, hide the result and report a repair/recompute
  message instead of presenting it as ready. Verify acceptance recovery after repair.
- [ X ] 4.1.5 Apply readiness checks before replacing Target or Tool. Reject stale
  picks without changing links or selection mode; verify repair/recompute allows
  replacement and successful acceptance.
- [ X ] 4.1.6 Apply readiness checks to optional target/tool preselection. Skip
  stale inputs and open the task for correction; verify a failed target is skipped,
  its valid tool remains selected and the repaired target can be picked/accepted.
- [ X ] 4.1.7 Guard command creation with a shared transaction context. Factory
  exceptions and editor refusal roll back created objects; verify no pending
  transaction/dialog remains and a normal retry can be accepted.
- [ X ] 4.1.8 Clean up partially constructed Trim tasks and failed dialog display:
  remove registered selection observation/annotations, restore visibility and abort
  owned edit transactions. Verify scene count, no pending edit and successful retry.
- [ X ] 4.1.9 Refuse reopening Trim Body inside an unrelated pending transaction.
  Only the scoped feature-creation context can hand its transaction to the editor.
  Verify pending edits survive rejected edit/create attempts and caller abort/retry.

- [ X ] 4.1.10 Continue independent Trim task cleanup actions after a secondary
  cleanup exception, retain the original startup failure and allow repeated annotation
  removal. Verify constructor/display failure, restored resources and successful retry.

Secondary cleanup evidence (also 5.1.10): `task-cleanup-errors-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **54 PASS, zero failures/
errors/skips** (Trim 14 model/17 GUI; Isocline nine model/14 GUI). Both tasks preceded
one grouped validation. Macro PASS; process ended. Shared FeatureTask and both GUI
suites staged with matching hashes in the isolated fork build (engine 2df76790b4).
Injected arrow cleanup errors after repeated removal preserve the primary constructor/
dialog error; later cleanup restores scene counts and result visibility, leaves no
pending transaction/dialog and permits reopen/accept. Isocline additionally releases
its curve highlight. This does not exhaust native cleanup/transaction failures or
replace physical viewport/high-DPI acceptance. FeatureTask SHA256:
`8BD25B1B56D28500DAAA09F4434DF89CB07412D310A75727161131C0B875634C`.
No native rebuild or release update.

Transaction ownership evidence (also 5.1.9): `task-ownership-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **52 PASS, zero failures/
errors/skips** (Trim 14 model/16 GUI; Isocline nine model/13 GUI). Both tasks preceded
grouped tests; macro PASS and process ended. FeatureTask plus two GUI suites staged
with matching hashes in the isolated fork build (engine source 2df76790b4). A scoped
ContextVar marks command-owned creation transactions and resets on success/failure;
unrelated transactions reject before task construction. Pending label edits remain
uncommitted, can be aborted by their owner and permit a normal later edit. Existing
creation, failure cleanup, Cancel and Undo/Redo suites also pass. FeatureTask SHA256:
`C4F52FA1CD30BB41F9033DDAEC2AC48124D3DE687DFD75F2A4EDFC2783568763`.
No native rebuild, release or physical viewport acceptance.

Task cleanup evidence (also 5.1.8): `task-cleanup-20260930-verified/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **50 PASS, zero failures/
errors/skips** (Trim 14 model/15 GUI; Isocline nine model/12 GUI). Both tasks preceded
grouped validation. Macro PASS; process ended. Three production Python modules and
two tests staged with matching source hashes (engine 2df76790b4). Initial batch
had 48 passes/two test errors because native Control methods cannot be patched;
wrapping Control supplied the intended dialog-display failure without changing
production behavior. Tests inject failure during initial preview and dialog display,
check original scene child count/result visibility and absence of dialog/pending
transaction, then reopen/accept successfully. They do not exhaust every Qt allocation
or cleanup failure. No native rebuild, release or physical viewport acceptance.
SHA256: FeatureTask `74B27674A51132F90E0E6403027C58C1BD0F08665C16263BC2D0E9F29D0084E2`;
TrimGui `31ED4AFCE425830CED40800A472D627A21B5182FB2DA53EC165ADCCCFCF884CB`;
IsoclineGui `3C9A6BEBCC92E7739BE8571439EC3EAF8FF078079EC58898E3C1C4283D6CAC49`.

Startup evidence (also 5.1.7): `task-startup-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **48 PASS, zero failures/
errors/skips** (Trim 14 model/14 GUI; Isocline nine model/11 GUI). Both tasks preceded
grouped tests; macro PASS and process ended. Three production modules and two
tests staged with matching hashes in the isolated fork build, engine 2df76790b4.
Final newline-only formatting was compared to tested files before restaging.
`creation_transaction` leaves successful creation open for task acceptance/Cancel,
aborts on startup exceptions, and refuses an existing caller transaction. Tests
inject factory failure after object creation and a false editor-start return;
partial task-widget construction/observer cleanup remains a separate failure case.
Final SHA256: FeatureTask `5EEE50A76A4B96918A40C866FCBE17FD6A2D974086E20DAA255CEA0A79053BD0`;
TrimGui `A3EBA1CF76F8E141988BED2453753B5B79F20DAB1563A9ADAAD79642EEF7103D`;
IsoclineGui `7FBAAE80022851FF7BBAEF2BB2371026330C362034ED62D7F059C837BD7C824E`.
No native rebuild, release update or physical viewport acceptance.

Preselection evidence (also 5.1.6): `task-preselection-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **46 PASS, zero failures/
errors/skips** (Trim 14 model/13 GUI; Isocline nine model/10 GUI). Both tasks preceded
grouped testing; macro PASS and process ended. Two production Python modules and
two test modules staged with matching source/destination hashes in the isolated
fork build (engine source 2df76790b4). Source SHA256:
TrimGui `E7C0372BA962C784BE0E44C497777B55A5A86C778B1CA32398108B201C468204`;
IsoclineGui `C38C8D0F93FD31D39D02F2D60CBF5FB5011D20968A5834E42042E0D500902854`.
No native rebuild, release update or physical viewport acceptance. Invalid
preselection is omitted; this does not automatically repair or recompute inputs.

Input-selection evidence (also 5.1.5): `task-selection-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **44 PASS, zero failures/
errors/skips** (Trim 14 model/12 GUI; Isocline nine model/nine GUI). Both tasks
preceded grouped validation. Macro PASS; process ended. Two changed production
Python modules and their GUI suites were staged with matching source/destination
hashes in the isolated fork build (engine source 2df76790b4). Native selection
callbacks reject failed-box candidates for all four fields and retain existing
inputs; repaired candidates can then be selected. No native rebuild, release
update or physical viewport acceptance. Source SHA256:
TrimGui `957F6F782B6DE5268686C5BB113FA9CEDE7370DE1DB62C2FAF4A8783BD8BCB08`;
IsoclineGui `5F8A087476311AB0D5E7F2D78D4F3F2854D83B1867C10948057931548FBF2E2E`.

Shared task-readiness evidence (also 5.1.4): `task-readiness-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **42 PASS, zero failures/
errors/skips** (Trim 14 model/11 GUI; Isocline nine model/eight GUI). Both tasks
preceded grouped validation. Macro PASS; process ended. Three changed production
Python modules and two GUI test modules were staged and source/destination hashes
matched in the isolated fork build, engine source 2df76790b4. No native rebuild,
manual viewport acceptance or release update. Shared `require_current` checks
Invalid/Touched state across the result and dependencies after recompute; it does
not clear cached geometry or change exporters. Source SHA256:
ShapeReferences `44DD51DB6F76DB5B5F5A8F40B1715620380563B1E0A4F8822891F507CFBD514B`;
TrimGui `276C6FAAA9901B3A4BA99844783703FEC883EEFD59F02E54BA2D6244307AE8D7`;
IsoclineGui `649BD807CC20A00F026BB0BC9BDA93A26D4E62AB927468DC99A65F82B8F0F539`.

- [ X ] 4.2.1 Rebuild/link PartGui and PartDesignGui menu/toolbar entries, install
  source-matching Python modules and icon into the existing Windows x64 Release
  build. The separately installed FreeCAD was not used. No new dependencies.
- [ X ] 4.2.2 Run native tests: **72 passed**, zero failures/errors/skips. Trim Body:
  14 model and 10 GUI tests; existing Pad 14, Extrude 17, Revolve 5, Pattern 12.
  Coverage includes analytical plane/cylinder/B-spline volumes and sheet areas,
  connected curved tools, finite-cutter rejection, closed solids, selection and
  both side buttons, datum planes, Body targets and nested placements, automatic
  tool-parameter recomputation, save/reopen, Cancel, Undo/Redo, and arrow cleanup.
  Fixed two issues found during development: finite planar half-spaces failed
  outside a small tool's bounds, and resetting edit before abort committed Cancel.
  Planar extension now uses an unbounded plane; Cancel aborts before resetEdit.
  A toolbar-test assumption was corrected after confirming the isolated profile
  intentionally hid Part Design toolbars; the test invokes the actual toolbar action.
- [ X ] 4.2.4 Inspect native task and window captures for planar, curved, and sheet
  targets in both keep directions. Controls fit and the green arrow reverses correctly.
  FreeCAD image export omits transient annotations, so arrow visibility was verified
  in native window captures. Saved an editable `TrimBodyExample.FCStd` in the evidence
  directory. Python formatting/syntax, SVG XML, whitespace and documentation checks pass.
- [   ] 4.2.3 Complete physical viewport selection, keyboard and high-DPI acceptance
  using [the test procedure](../tests/TrimBody.md). Automated Qt tests and captured
  layout inspection do not establish this manual gate.

Evidence directory: `D:\Temp\Office-PC\freecad-plus-validation-20260928`.
Native reports: `trim-gui-gui-results.json`, `trim-gui-TestTrimBody.log`,
`trim-gui-TestTrimBodyGui.log`, and existing-suite logs with the `trim-gui-` prefix.
Visual evidence: `trim-visual-check.json`, `trim-*-task.png`, and `trim-*-window.png`.
Build logs: `trim-build-Part-Workbench.log`, `trim-build-PartGui-link.log`,
`trim-build-PartDesign-Workbench.log`, `trim-build-PartDesignGui-link.log`.
Launcher: `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Incremental modules are current; the main executable About/version stamp remains
from its earlier build. This task does not publish a release or push local commits.

Compatibility and geometry limits: one cutting tool, automatic extension for planar
boundaries only. Curved tools must fully span each trimmed region; automatic curved
Trim and Extend is future scope. Result recomputation needs the new BOPTools Python
modules. Upstream-only recomputation, Linux/macOS validation, and packaging are not
established. The output is associative but does not insert a new Part Design Body Tip.


<a id="isocline-curve"></a>

## [   ] Phase 5: Associative Isocline Curve

Outcome: trace a selected draft angle on one or more faces relative to an editable
pull direction. User-authorized scope; REQ-018 through REQ-020 and
[UI-005](UI_UX_SPEC.md#ui-005-isocline-curve-task-pane).
Depends on: the existing OpenCASCADE Part kernel and native development build.

### [ X ] 5.1 Implement contour geometry and complete editor

- [ X ] 5.1.1 Add the Part.makeIsocline binding around Contap_Contour, analytical
  curves and surface-parameter interpolation, clipping to trimmed faces and holes.
  Use draft convention normal dot pull = sin(angle), so 0 degrees is silhouette.
  Validate fit residual, suppress degenerate point output, report whole-face matches,
  and handle the limiting 90-degree cylinder line.
- [ X ] 5.1.2 Add the linked multi-face feature, axis/reference/custom direction,
  reversal, angle, live preview, and same create/edit pane. Register one command
  in Part's menu/Part Tools toolbar and Part Design's menu/Modeling Features toolbar.
- [ X ] 5.1.3 Reuse extracted ShapeReferences and FeatureTask helpers with Trim Body.
  Preserve stored Trim proxy names and input/transaction behavior. Both features
  track enclosing placements, preserve source objects and keep a separate result.

- [ X ] 5.1.4 Apply shared dependency-readiness validation to Isocline preview and
  acceptance. Failed source geometry keeps the task editable and result hidden;
  repair restores curve preview and acceptance. Evidence recorded with 4.1.4.
- [ X ] 5.1.5 Reject stale face/direction-reference picks before changing links,
  preserving the face list, direction reference and active selection mode. Verify
  repair/recompute permits reference selection and acceptance; evidence with 4.1.5.
- [ X ] 5.1.6 Filter stale face preselection without discarding valid faces in the
  same selection. Verify repaired faces can be added and accepted; evidence with 4.1.6.
- [ X ] 5.1.7 Use shared creation transaction handling for factory/editor startup
  failures and verify complete object rollback plus successful retry; evidence with 4.1.7.
- [ X ] 5.1.8 Apply shared construction/display failure cleanup to Isocline tasks,
  including curve highlight and direction arrow removal, visibility restoration and
  transaction rollback; verify retry. Evidence recorded with 4.1.8.
- [ X ] 5.1.9 Apply explicit transaction ownership to Isocline reopening and verify
  unrelated pending edit/create rejection without mutation; evidence with 4.1.9.
- [ X ] 5.1.10 Continue Isocline task cleanup after a secondary arrow cleanup error,
  including curve highlight removal, while preserving the primary startup error;
  repeated removal and reopen/accept verified with 4.1.10.

- [ X ] 5.1.11 Preserve whole-object face collection using an explicit empty
  subelement name in the native LinkSubList. Fix preselection, interactive picking
  and retention when other rows are removed. Verify geometry, Undo/Redo and
  save/reopen followed by source edits; evidence with 8.1.2a/8.1.3c. F031/F070.

- [ X ] 5.1.12 Expose the existing Isocline curve tolerance in the create/edit task.
  Accept length units or bare mm within native 1e-7..0.01 mm limits; reject invalid
  drafts without overwriting the saved value, hide preview and block OK even when
  paused. Preserve expression authority and Cancel/Undo/save/reopen semantics.
  Reuse the same unit/range boundary in model execution; no native/schema change.

### [   ] 5.2 Validate the local build

- [ X ] 5.2.1 Rebuild/link Part's contour binding plus PartGui/PartDesignGui command
  entries and install the matching scripts and icon in the isolated Windows x64
  Release build. Existing MSVC/Qt/OpenCASCADE LibPack; no added dependency.
- [ X ] 5.2.2 Complete native model/task regressions and inspect task/viewport captures.
  **88 tests passed**, with no failures/errors/skips: Isocline nine model and seven
  GUI, Trim Body 14 model and 10 GUI, Pad 14, Extrude 17, Revolve five, Pattern 12.
  Geometry checks include analytical lengths, normal-angle residuals and distance
  to the trimmed source face, freeform closed loops, boundary contours, holes,
  direction reversal, face orientation, multi-face wires and 90-degree degeneracy.
  Persistence, parameter/placement recomputation, picking, invalid recovery,
  paused preview, Cancel and Undo/Redo passed. Actual toolbar actions work in both
  workbenches; the test now allows FreeCAD's delayed enablement timer to settle.
  Visual inspection found a degree-symbol encoding issue and surface tessellation
  obscuring freeform lines. Fixed the symbol and added a transient curve highlight;
  the same 17 Isocline/Trim GUI tests passed after those presentation changes,
  including annotation cleanup. Native window captures verify readable controls,
  red curves and the reversing green arrow. Source geometry stays unchanged.
  Python/C++ formatting, syntax, SVG XML, whitespace and documentation checks pass.
  Saved editable sphere and freeform examples in the evidence directory below.
- [   ] 5.2.3 Complete physical viewport selection, keyboard and high-DPI acceptance
  using [the Isocline test procedure](../tests/IsoclineCurve.md). Automated Qt controls
  and window captures do not establish this manual gate.

- [ X ] 5.2.4 Complete F070 functional acceptance for the documented bounded,
  single-angle Isocline workflow. Add tolerance endpoint/recovery and native
  nonfinite checks, expression/units/editor lifecycle, and feature-level reversed
  normal plus reversed pull/Undo coverage. Map the item to analytic residual,
  trimmed-domain/hole, multiple/empty/nonunique/isolated-point, persistence and
  task tests in [the acceptance matrix](../tests/IsoclineCurve.md#f070-functional-acceptance-mapping).
  Five added tests; **130 grouped passes, zero failures/errors/skips**, macro PASS,
  process exit 0: Isocline model 11 and GUI 26; Trim model 14 and GUI 24; Pad 14,
  Extrude 19, Revolve 5 and Pattern 17 task tests. Four source/staged Python hashes
  match. Existing engine `802e19d648`; no native rebuild or release. Evidence:
  `D:\Temp\Office-PC\freecad-plus-isocline-tolerance-20260930\grouped`, with
  `staging-identities.json` in its parent. Valid and incompatible-unit error
  panels were captured and visually checked in sibling `visual`; controls and
  messages are readable. Physical acceptance remains 5.2.3; sampled tests do not
  establish completeness for arbitrary singular surfaces.

Evidence: `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
`isocline-gui-gui-results.json`, `isocline-gui-Test*.log`,
`isocline-visual-tests-gui-results.json`, `isocline-visual-check.json`,
`isocline-*-task.png`, `isocline-*-window.png`, and `isocline-build-*.log` /
`isocline-gui-build-*.log`. Examples: `Isocline-sphere-example.FCStd` and
`Isocline-freeform-example.FCStd`. Launcher:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Incremental Part/GUI modules are updated; the main executable About stamp remains
from its earlier build. The separately installed FreeCAD was not used.

Compatibility/scope: one angle per feature; source faces and Body Tips are preserved.
A result may have several connected wires. Empty, isolated-point and whole-face
solutions do not invent an isocline. Arbitrary-surface completeness is not proven
by sampled residual checks. Splitting bodies/faces, multiple stepped angles,
Linux/macOS validation, packaging, push and publication remain outside this task.
Recomputation requires the new Python modules and native Part API in FreeCAD Plus.


<a id="cam-mesh-machining"></a>
## [   ] Phase 6: STL CAM and holding tabs

User request: direct STL Parallel/Waterline machining similar to MeshCAM, with
simple tabs that toolpaths automatically avoid, including two-sided/indexed
machining. Separate manually indexed jobs share model/stock/tab transforms and
have independent origins. Implementation, build and automated workflow checks
are complete. Native acceptance and simulation remain pending; automatic
rotary-axis output is outside this implementation.

### [ X ] 6.1 Direct mesh workflow

- [ X ] 6.1.1 Accept and clone STL job models associatively; compute stock and placement without facet-to-BRep conversion.
- [ X ] 6.1.2 Use every mesh/CAD model in Parallel and Waterline generation; expose the command without experimental preference flags.
- [ X ] 6.1.3 Validate actual STL import, placement, both strategies, mesh edits and save/reopen in the CAM-enabled build.

### [   ] 6.2 Geometric holding tabs

- [ X ] 6.2.1 Add the shared create/edit pane, numeric dimensions and viewport placement; preserve transactions and document links.
- [ X ] 6.2.2 Protect tab stock across supported cutting/link moves using the cutter radius; reject unsupported strategies and unsafe heights without stale paths.
- [ X ] 6.2.3 Validate narrow crossings, rotated/overlapping bridges, operation recompute, Cancel/Undo/Redo and saved documents.
- [   ] 6.2.4 Complete native visual/viewport acceptance and record a representative simulation review. No machine cutting validation is implied by software tests.

### [ X ] 6.3 Build and validation

- [ X ] 6.3.1 Enable CAM, Draft, MeshPart and required dependency modules in the external development build.
- [ X ] 6.3.2 Run focused CAM and relevant existing regressions; record runtime/source identities and remaining limitations.
- [ X ] 6.3.3 Commit and push the validated milestone to origin; verify the remote branch.
  Evidence: `648cff214ca78e1d8b3d72d87d6053e103390c60` pushed to `origin/main`;
  `git ls-remote` returned the same hash. No release or installer was published.

### [   ] 6.4 Two-sided and indexed setups

- [ X ] 6.4.1 Define setup orientation, work origin, stock and part references for each side/index; distinguish manual indexing between jobs from controller-driven indexing.
- [ X ] 6.4.2 Preserve the same physical holding tabs across transformed setups; propagate tab edits and invalidate every affected path.
- [   ] 6.4.3 Validate opposing faces and a non-orthogonal index, coordinate transforms, stock registration, tab clearance, safe linking moves and per-setup output.
  Per-setup export and edit/persistence checks completed in the 2026-09-30 batch
  below. Native indexed viewport acceptance and regenerated-contour repeatability
  remain open; this parent is not marked complete by the output tests.

Evidence, 2026-09-30 (`D:\Temp\Office-PC\freecad-plus-indexed-output-20260930`):

- Completed the indexed producer/dependency fix: generation no longer invokes
  model/stock proxies after native recompute. Indexed stock joins the explicit
  operation dependencies; stale or invalid indexed inputs reject direct generation
  and leave no old path. The unchanged post guard still rejects stale export.
- Completed real-job output validation for 180/45-degree STL setups and both
  Parallel/Waterline strategies through LinuxCNC/Grbl. Explicit three-axis metric
  configuration, six-decimal axis output and G17/G90 preamble; 17 retained `.nc`
  fixtures. Every posted XYZ endpoint and rapid/feed mode agrees with its native
  operation within 0.000001 mm, with final clearance and sampled tab protection.
  No rotary motion, controller connection or machine certification is implied.
- Completed shared-tab and independent-origin edit checks: dirty jobs reject
  posting, native recompute refreshes both Waterline outputs after a shared-tab
  edit, and changing one custom origin preserves the other setup's path.
  Saved commands persist exactly; reopened, regenerated jobs post and retain tab
  clearance. This does not prove identical regenerated contours.
- Final acceptance uses `fixed` for the 24 mesh-workflow, 7 nested-post and 82
  invalid-input regressions, plus `verified` for the 3 final output tests: 116
  distinct passes, zero failures/errors/skips in those selected results, process
  exits 0. `acceptance-summary.json` and `validated-identities.json` record exact
  suites, matching source/runtime modules and binary identities. The mixed `fixed`
  aggregate includes earlier output-fixture failures and is not itself claimed PASS.
- Initial runs reproduced dirty indexed producers despite repeated recompute.
  Fixture corrections handle the existing helper's direct execute, configure the
  machine bundle preamble and avoid assuming a fixed Waterline contour start.
  A slow OCC-distance probe was interrupted; its overlapping exploratory launch
  is excluded from acceptance. The final `verified` run was isolated and passed.
- Open finding: the 45-degree Waterline regeneration comparison found horizontal
  cutting lengths 653.304546 versus 653.329250 mm and up to 0.172558 mm sampled
  bidirectional contour distance. The 180-degree contour matches at floating
  precision. Retain `persistence-comparison.json`, probe and output artifacts;
  investigate repeatability separately. Do not close F089 or 6.4.3 on this evidence.
- Both source changes and the three workflow cases preceded grouped validation.
  No native build was needed; installed Python modules match source. Viewport,
  material-removal simulation and broader post/machine acceptance remain pending.


Evidence, 2026-09-29 (external root `D:\Temp\Office-PC\freecad-plus-validation-20260928`):

- The first build was cancelled at the user's request. The resumed build linked
  its modules but did not capture an exit code. The incremental completion build
  passed with exit 0: `cam-completion-build-result.json`; final script targets
  also exited 0 (`cam-final-scripts.log`).
- `cam-tests-20260929-184049`: all 22 `TestMeshMachining` cases passed with no
  skips and process exit 0. Includes STL curved-surface height checks, layered
  Waterline, mixed translated mesh/CAD models, tab clearance and block-delete
  annotations, persistence, 180/45-degree indexing, shared-tab propagation,
  task transactions, indexed-stock refresh and command availability.
- `cam-tests-20260929-183855`: the seven related suites ran 113 cases: 112 passed,
  none failed/errored, one skipped. Suites: `TestPlanarSurfaceOp`,
  `TestSurfaceMeshGenerator`, `TestPathStock`, `TestPathDressupHoldingTags`,
  `TestPathOpUtil`, `TestPathUtil`, `TestPathSharedWorkplane`. The optional
  simplification test skipped because `fast_simplification` is unavailable.
  The strict aggregate marker is FAIL due to that skip, not a test failure.
- `cam-validation-manifest.json`: all 15 installed changed CAM Python files
  match source; five binary hashes recorded. The application still reports its
  historical native stamp `8abce719de` (26.3.0dev, revision 49009); this stamp is
  not the identity of the new Python implementation. Use the manifest and commit.
- Native mouse/viewport acceptance, representative material-removal simulation,
  and per-setup postprocessor review remained open at this checkpoint (6.2.4 and
  6.4.3); the later configured-output evidence above advances the latter. Automated
  indexed geometry/path checks pass; they do not establish machine/fixture safety.


<a id="nx-feature-history"></a>
## [   ] Phase 7: NX-style unified feature history ? first priority

Outcome: one ordered feature history for a model part, with sketches, datums,
linked/cloned geometry and modeling features available independently of a single
Body. Users do not have to create or activate a Body before modeling. Solid/sheet
bodies remain real geometric results with stable identities; they are not the
mandatory organizing containers for every input and feature. An assembly has a
history per component/model part, not one interleaved history for every component.

This is the user's desired behavior, not a statement that current FreeCAD supports
it through a tree preference. A flattened navigator is only the first visible step.
Backend ownership, feature inputs/outputs and reference rules must support the same
workflow. Reuse native FreeCAD capabilities where their semantics fit; do not hide
an unchanged single-body restriction behind a different-looking tree.

Implementation order: 7.1?7.3 establish the model and navigator; 7.4 delivers the
first end-to-end Extrude/Revolve workflow; 7.5?7.7 make history editing and adoption
safe. Existing Phase 2/3 implementation and tests are inputs, not work to recreate.

### [   ] 7.1 Define the part-level history and body model

- [ X ] 7.1.1 Specify a single ordered History list and a separate Bodies/results list. Roles and ownership are defined in [the logical contract](architecture/PART_HISTORY_CONTRACT.md#ownership-and-roles-711); no production schema is implied.
- [ X ] 7.1.2 Map current Part, Part Design Body/Tip, feature ownership, attachment and document-link restrictions to the proposed model. [Source mapping](architecture/PART_HISTORY_CONTRACT.md#current-native-model-and-required-changes-712) separates presentation from model/API changes and records existing multi-solid support.
- [   ] 7.1.3 Prototype native Body adapters versus a part-level feature/result layer. Evaluate multi-body outputs, shared inputs, references, recompute, persistence and upstream compatibility before choosing the architecture.
- [ X ] 7.1.3a Prototype native Body/SubShapeBinder/Pad adapters sharing one
  independent part-owned sketch. Validate source edits, separate Tips and native
  save/reopen without duplicating sketch constraints or reparenting the source.
- [ X ] 7.1.3b Prototype a part-level feature with two explicitly named output
  roles and separate identified result nodes. Validate a later result consumer,
  edits/rename/source order, unavailable/reappearing output, Undo/Redo, abort and
  native save/reopen. Fixed roles are a bounded identity proof, not general lineage.
- [ X ] 7.1.3c Resolve tilted sketch normals and cross-part placement dependencies
  in the explicit-result prototype. Validate transformed geometry against an
  independent solid, source-part moves/Undo, and native persistence.
- [ X ] 7.1.3d Prove a native cut of one App::Link occurrence in an assembly
  updates after shared source edits without changing the definition or second
  occurrence; preserve the cut through save/reopen.
- [ X ] 7.1.3e Probe Draft clone and CAM job-model invalidation. Fix production
  Draft clones retaining old geometry when all source shapes become empty or
  the source list is cleared; verify restored source geometry and clone placement.
  This does not establish CAM toolpath invalidation or general consumer safety.
- [ X ] 7.1.3f Prove an independent sketch attached to a rotated planar support,
  with attachment offset, feeds explicit history results. Support moves propagate;
  Undo/Redo and save/reopen retain attachment links, geometry and result identity.
  This is one FlatFace attachment case, not arbitrary topology repair.
- [ X ] 7.1.3g Prototype a real planar split with explicit negative/positive-X
  roles and distinct child identities/provenance. Validate moving the split,
  disappearance/reappearance and Undo; reject multiple solids per role explicitly.
- [ X ] 7.1.3h Prototype a merge preserving an explicitly chosen primary BodyId,
  or allocating a new identity when no primary continues. Persist parent identities;
  validate reorder/rename, geometry edits, save/reopen, unavailable inputs, duplicate
  identities and replaced source lineage without implicit retargeting.
- [ X ] 7.1.4 Define stable feature and body identities, explicit input/output links, and merge/split/disappear/reappear lineage. [Identity contract](architecture/PART_HISTORY_CONTRACT.md#identity-and-dependencies-714) separates modeling/display order from the dependency graph; storage and runtime implementation remain pending.
- [   ] 7.1.5 Document the chosen architecture, migration boundary and a small reference model; update product/UI specifications before production implementation.

Complete when: a prototype demonstrates one independent sketch driving features
on two bodies, one feature producing multiple bodies, and a later feature using
results from both, without silently duplicating sketches or losing references.

- [   ] 7.1.6 Before architecture implementation, record decisions for the supplied
  definition/occurrence, body-result, selection, transaction and persistence contracts;
  include alternatives, affected consumers and narrow proof criteria (G1-G3).
- [ X ] 7.1.6a Record the [adapter experiment boundary and decision gates](architecture/ADR_001_HISTORY_ADAPTER_BOUNDARY.md).
  Retain native Body adapters and an explicit-result layer as candidates; reuse
  native geometry, App::Link, links and transactions. Record unresolved production
  selection/default, schema and consumer gates. This is not the final architecture.

Split/merge batch evidence: **29 PASS**, zero failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\lineage-20260929-topology\results.json`.
Five new lineage checks join the previous 24 checks. The initial invalid-source test
found that a raised native recompute error skipped dependent evaluation, retaining
stale merge geometry. The new test-only lineage proxies report expected input/kernel
failures as ResultStatus/ErrorMessage with cleared outputs, allowing participating
result consumers to invalidate themselves. A U-shaped single solid that splits into
two solids on one side now fails explicitly; no arbitrary solid-index mapping occurs.
`prototype-manifest.json` records hashes; SplitMergeProof.FCStd requires test modules.
No installed source or native build changed. This is explicit planar-role lineage,
not arbitrary topology correspondence, persisted revision history, Make Unique or a
production error protocol. Parent architecture/consumer gates remain open; native
error icons and nonparticipating consumers still require deliberate integration.

Attachment/drawing batch evidence: **24 PASS**, zero failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\attachment-drawing-20260929-final\results.json`.
Includes ten adapter probes, four native capabilities, three clone invalidation and
seven operation-intent checks. New probes cover a moved rotated support plane with
2 mm attachment offset, and an analytic TechDraw projected radius changing 2 to 3 mm
through source edit, Undo/Redo and restore. Initial drawing fixture used Edge1;
TechDraw's projected circle uses zero-based Edge0 (confirmed in native source and
existing upstream tests). Correcting the fixture required no application fix.
`prototype-manifest.json` records source hashes. Saved AttachedProfileProof.FCStd
and DrawingResultProof.FCStd require the test proxy module to recompute; no native
build, installed source change or GUI mouse/keyboard acceptance is claimed.
Missing/ambiguous drawing references, CAM paths, FEM, general attachment/topology
and lineage gates remain open. See 16.2a and ADR 001 for the bounded consumer proof.

Placement/consumer batch evidence (2026-09-29): **88 PASS**, zero failures/errors/
skips, in `D:\Temp\Office-PC\freecad-plus-validation-20260928\part-consumers-20260929-final\results.json`.
Grouped coverage: four native capabilities, eight adapters, three clone
invalidation checks, 33 existing Draft modifications, 18 PlanarSurface operations
and 22 STL/tab machining checks. Initial probes reproduced wrong tilted extrusion
direction, ignored source-part placement and stale clone geometry; focused rerun
passed all 15 checks before the broader batch. The history layer stays test-only.
The production change is limited to `Draft/draftobjects/clone.py`, synchronized
to the existing fork build without native compilation. Source/installed SHA256:
`6291E8A30ED3C4321833182412A6D8AC86C642CFF035A605F9FFD29327DF19A9`.
`prototype-manifest.json` in that evidence directory records module/test hashes.
No new GUI workflow or mouse/keyboard acceptance is claimed. CAM job-model refresh
is distinct from invalidating generated paths. TechDraw dimension references,
FEM supports/loads (FEM disabled in this build), actual sketch attachments,
general lineage and cold-start prototype deployment remain open.

Earlier adapter batch evidence (2026-09-29): `tests/TestPartHistoryAdapters.py` plus the
four native capability probes report **8 PASS**, no failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\part-adapters-20260929-final\results.json`.
`prototype-manifest.json` records the test/adapter hashes. All implementation is
under `tests/prototypes`; no application module was installed or rebuilt.
The first result adapter lost a shape's translation under native recompute and
merged distinct outputs; Shape/Placement synchronization corrected it, with
position assertions retained. Expected unavailable-result errors clear the
consumer instead of returning partial/stale geometry. Native BodyAdapterProof.FCStd
and test-module-dependent ExplicitResultProof.FCStd are disposable evidence only.
Final choice, general topology/lineage, transformed attachments, remaining downstream
consumers and cold-start deployment remain open under the parents; the later batch
above establishes one bounded assembly-local edit and Draft/CAM model refresh.

Foundation batch evidence (2026-09-29): `tests/TestPartHistoryCapabilities.py`
passes four native probes in the existing fork, with no failures/errors/skips.
Evidence: `D:\Temp\Office-PC\freecad-plus-validation-20260928\part-history-20260929-final\results.json`.
One independent sketch drives two Part extrusions without a Body; another
extrusion produces two solids; a later compound consumes all four results.
Shared radius edits propagate; Undo/Redo, abort and native `.FCStd` save/reopen
retain links and geometry. Two App::Link occurrences keep independent placements.
Native group ownership rejects direct sharing/reparenting from App::Part into a
Body; Body ownership is exclusive. The initial probe assumed an allowed move and
was corrected to test the observed restriction. No application source changed.
`PartHistoryNativeProof.FCStd` in that evidence directory is a disposable native
capability example, not `.cadprt` or a finished history-layer prototype.
7.1.3 remains open: compare actual Body/result adapters, semantic lineage,
mixed definition/occurrence content and drawing/CAM/FEM/Draft consumers before
choosing the architecture. 7.1.5/7.1.6 are not closed by this foundation batch.

### [   ] 7.2 Build the unified history navigator

- [   ] 7.2.1 Add a part-level History view containing sketches, datums, linked geometry and features in modeling order. Show shared inputs once, with discoverable consumers, instead of nesting them exclusively under one body.
- [   ] 7.2.2 Add a Bodies/results view showing current solids and sheets, with source-feature links, names, visibility and selection. Body hiding must not suppress generating features.
- [   ] 7.2.3 Synchronize navigator selection and viewport highlighting; provide Find in History, Find Result, Show Parents and Show Dependents.
- [   ] 7.2.4 Provide search, type/status filters, user folders and meaningful names. Folders organize display without changing geometry ownership or recompute order.
- [   ] 7.2.5 Retain access to the native document tree for legacy documents and diagnostics. A view change must not migrate or rewrite a file by itself.

### [   ] 7.3 Make sketches and reference geometry independent

- [   ] 7.3.1 Create sketches on principal planes, datum planes or selected faces without requiring a Body. Preserve attachment, placement, units and expressions.
- [   ] 7.3.2 Allow one sketch or curve source to feed multiple features and bodies. Distinguish whole-sketch, region and curve-chain selection; define open/closed profile rules per operation.
- [   ] 7.3.3 Put datums, construction geometry and imported geometry at part scope, with explicit dependencies rather than incidental active-body ownership.
- [   ] 7.3.4 Add complete create/edit definitions for associative copies, clones and linked references: source, transform and update behavior. Keep independent copies a separate explicit choice.
- [   ] 7.3.5 Validate cross-body reuse, source replacement, moved references, circular-dependency rejection, Cancel and save/reopen without automatic destructive reparenting.

### [   ] 7.4 Automate body creation and target selection

Planned default reconciled by version 2: suggest New Body or a valid single-target
Unite at creation; require explicit resolution of ambiguity and preserve user intent.
See 7.4.8 and [baseline adoption](#planning-baseline-adoption). Implementation is pending.

- [   ] 7.4.1 Extend the existing Extrude and Revolve task workflows to start in an empty part without a declared/active Body. Keep Operation as the first field, followed by profile, target/result controls and parameters.
- [   ] 7.4.2 For Add with automatic targeting, create a new solid body when the generated solid has no valid volumetric overlap with an existing eligible solid. With exactly one eligible intersecting target, preview adding to that target.
- [   ] 7.4.3 If multiple bodies intersect, show and highlight candidate targets; require an explicit target set or New Body choice. Never choose a target by incidental tree order or visibility.
  Specify supported multi-target cuts, trims and other operations as one feature with an
  explicit target set, per-target results and deterministic lineage. This is broader
  than selecting a single target; the single-target prototypes do not complete it.
- [   ] 7.4.4 Provide an explicit New Body override even when geometry overlaps. For Subtract and Intersect, require valid target bodies and report a nonintersecting/empty result rather than creating an unintended body.
- [   ] 7.4.5 Define tangency, face/edge contact, coincident geometry, tolerances, disconnected profile regions, sheet results and multi-solid outputs. Make automatic decisions inspectable in the preview.
- [   ] 7.4.6 Persist target intent and body lineage. Commit concrete operation and target identities. Recompute must not rerun creation inference. When an edit removes the required intersection, report failure/repair instead of switching operation, target or body identity.
- [   ] 7.4.7 Reuse this result/target policy for Loft, Sweep, Helix, primitives and Boolean operations after the Extrude/Revolve pilot passes. Retain legacy command/API entry points.

First deliverable: open a new document, draw a sketch, Extrude without creating a
Body, then create a disconnected Extrude and obtain a second body. Reuse the first
sketch for another feature, modify one selected body with Subtract, and reopen each
feature in the same complete task pane. Repeat the body-creation cases with Revolve.

- [ X ] 7.4.8 Reconcile the planned default from the owner-supplied version 2:
  suggest New Body for no eligible intersection, Unite for exactly one eligible
  target with a valid union, and require deliberate selection for multiple targets.
  Explicit user operation/targets prevail. Other-component intersections do not
  authorize source modification. Pocket/Groove start in Subtract. This closes only
  the planning decision; 7.4.1-7.4.7 and 10.3 implement and validate it.

### [   ] 7.5 Add history editing, rollback and recovery

- [   ] 7.5.1 Add Make Current / rollback and return-to-end controls; show the exact intermediate body results and disable later features for the rollback preview without deleting them.
- [   ] 7.5.2 Insert new features at the current history position and update the dependency graph consistently. Restore the prior position and geometry on Cancel.
- [   ] 7.5.3 Support safe reorder/move with dependency validation and a clear explanation of prohibited moves; never treat arbitrary tree drag order as a valid modeling history.
- [   ] 7.5.4 Add suppress/unsuppress with explicit downstream status. Distinguish suppression, visibility, inactive setup and failed recompute.
- [   ] 7.5.5 Preview deletion effects and offer valid dependent-feature handling. Provide broken-reference repair and Replace Input within the complete feature editor.
- [   ] 7.5.6 Keep feature edits, target changes, body creation/removal and history-position changes atomic for Cancel and Undo/Redo; recover from recompute failures without displaying stale success.

- [x] 7.5.5a Add a read-only F015 dependency snapshot using native property edges,
  showing direct/transitive inputs and consumers, expression/link reasons, native
  error state and loaded external sources. Bound traversal and report cycles/limits;
  this is inspection, not a deletion or repair implementation.
  Installed with 10.6a; grouped evidence is recorded there. Native container edges
  remain visible without inferring target roles. Whole 7.5.5 remains open.

- [   ] 7.5.7 Add controlled recompute: automatic/manual update modes, deferred
  updates and targeted recomputation. Show stale/blocked dependents and the first
  failing input; provide a deliberate update action. Deferred results must not be
  treated as current by export, CAM or downstream analysis. Test switching modes,
  queued edits, failure recovery, cancellation and save/reopen status.

- [x] 7.5.7a Expose native deferred recompute plus explicit whole-document update
  (F088), preserving session mode, owner transactions and Undo/Redo. No replacement
  update engine or persistence schema; targeted/asynchronous cancellation remains open.
- [x] 7.5.7b Show native failed/pending objects and affected loaded dependents
  (F087/F088), with object/input navigation and native details. Validate stale export
  refusal, failure repair, mode changes, lifecycle and save/reopen. Bound inspection
  and stop at a usable owner-test checkpoint. Both tasks complete for owner testing;
  grouped build/runtime checks pass and five captures reviewed.

7.5.7a/b grouped evidence (2026-10-01): both tasks preceded one FreeCADGui/
FreeCADGui_Resources Release build, exit 0. 21 distinct selected checks pass without
failures/errors/skips: 7 TestDocumentUpdates in updates-accepted/, 7 dependency-inspector
and 7 command-search in grouped/; accepted process exits 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-document-updates-20261001`.
FreeCADGui SHA256: `d2aab61ea0e6db907281baa3323e86b0c1379e051fceb7a84ca53f7dd0eba2c7`.
Deferred dimension edits retain cached geometry until explicit update; native mode
is preserved, normal-mode results agree, and the existing manufacturing STL handoff
rejects pending/invalid linked results. Native Cut failure/input navigation/repair,
loaded external dependency status, cycle rejection, Undo/Redo, transaction guards,
session mode and save/reopen pass. Initial grouped/ and updates-verified/ retain
external-link fixture errors requiring first the source and then the owner document
to be saved. Only the fixture changed; no application restaging or corrective build.
Targeted recompute, asynchronous progress/cancellation, unloaded references, broader
first-cause classification and physical acceptance remain open. No installer/release
update; whole F087/F088 and parent 7.5.7 remain open. [Owner procedure](../tests/DocumentUpdates.md).
visual/ contains five reviewed captures, Update-Bracket.FCStd and
Update-Bracket-Repaired.FCStd. acceptance-summary.json / validated-identities.json
record accepted suite and source/runtime/native identities; installed DocumentUpdates.py
matches source. Stop here for owner workflow feedback and rotate item families.

### [   ] 7.6 Preserve documents and external consumers

Owner decision (2026-09-29): `.cadprt` is the planned native format. Continue
best-effort opening and conversion of legacy `.FCStd` files; the owner accepts
that compatibility may become harder and less complete over time. Follow the
[format policy](PRODUCT_SPEC.md#planned-native-format-and-legacy-import), including
untouched originals and explicit conversion-loss reporting. This is not implemented.

- [   ] 7.6.1 Build a compatibility matrix covering existing upstream files, existing Plus files and new history-model files: open/display, edit, recompute and round-trip save are separate checks.
- [   ] 7.6.2 Version the component model and convert supported legacy content in memory on opening; preserve the original and save separately as `.cadprt` (owner decision 2026-10-01).
- [   ] 7.6.3 Preserve existing type/property names and Python entry points where possible. Document any new feature modules required for recomputation; do not promise upstream compatibility for backend changes without evidence.
- [   ] 7.6.4 Define explicit neutral-geometry export as an exchange option, including loss of editable history. Never replace the editable original with a flattened export automatically.
- [   ] 7.6.5 Audit Assembly, TechDraw, CAM, expressions, links and scripts that currently resolve a Body Tip. Provide stable result references and invalidation behavior for the new history model.

- [   ] 7.6.6 Specify `.cadprt` schema/capabilities, legacy import/conversion,
  Save As/Copy/Make Unique identity, external relocation and unsupported-content
  handling before native-format implementation. Never convert owner files in place.
- [   ] 7.6.7 Implement versioned `.cadprt` reading/writing and make it the native
  format for new documents after migration gates pass. Update Open/Save dialogs
  and file associations while retaining legacy `.FCStd` opening.
- [   ] 7.6.8 Implement on-open in-memory `.FCStd` conversion, saved into a separate `.cadprt`
  file. Map editable history, geometry, references and workbench data where possible;
  report unsupported content and distinguish partial or geometry-only recovery.
- [   ] 7.6.9 Extend the compatibility fixtures across legacy versions and supported
  workbenches; verify converted save/reopen/recompute and unchanged original files.
  Publish tested conversion coverage and known losses as the formats diverge.
  Best-effort compatibility must not be represented as guaranteed lossless import.

### [   ] 7.8 Component Structure, Model History and native component documents

Owner-approved 2026-10-01; [canonical contract](architecture/COMPONENT_DOCUMENT_CONTRACT.md).
Execution order: contracts -> model/identities -> persistence -> history/reference
operations -> navigators/edit contexts -> migration/downstream acceptance. Existing
7.1-7.7 and phase 12 tasks retain their evidence; this milestone integrates them.

- [ X ] 7.8.1 Resolve owner choices and record component/file, representation,
  direct-child reference, dumb-object, suppression and conversion contracts.
- [ X ] 7.8.2 Implement component definitions and instances, stable identities,
  embedded/external ownership, independent placement and safe graph validation.
- [   ] 7.8.3 Implement versioned `.cadprt` persistence/capability preflight,
  atomic save/recovery, Save As/Copy identity and external dependency resolution.
- [ X ] 7.8.4 Implement direct-child evaluated references for bodies, sheets,
  sketches and curves, pending refresh on parent activation and parent-local edits.
- [   ] 7.8.5 Integrate ordered Model History, independent inputs/result identities,
  production modeling operations and dependency-aware suppression/restoration.
- [   ] 7.8.6 Implement Convert to Dumb Object: identity-preserving Delete Parameters
  with shared-producer pruning, plus independent Extract Dumb Body.
- [   ] 7.8.7 Implement Component Structure and Model History tabs, Add Component,
  display types/path overrides, constraints grouping and isolated component tabs.
- [   ] 7.8.8 Implement Make Independent and embedded/external conversion, retaining
  shared child definitions unless deep-copy was explicitly requested.
- [ X ] 7.8.9 Convert legacy FCStd in memory on opening; preserve original files,
  report tested editable mappings and unsupported/geometry-only content.
- [   ] 7.8.10 Complete grouped native/runtime, cold reopen, undo/redo, graph/failure,
  downstream and GUI acceptance against the contract's end-to-end example.
- [ X ] 7.8.11 Commit coherent verified milestones and push to origin; record exact
  remote branch verification. Packaging/public release require separate authority.

Complete when: the approved end-to-end component workflow works in the fork, with
recorded save/reopen, recompute, undo, downstream and UI evidence. A schema, Python
API or dialog alone does not complete this milestone.

2026-10-01 implementation: [architecture decision](architecture/ADR_003_COMPONENT_DOCUMENT.md),
[`ComponentModel.py`](../src/Mod/Part/ComponentModel.py),
[`CadDocument.py`](../src/Mod/Part/CadDocument.py) and
[`ComponentNavigator.py`](../src/Gui/ComponentNavigator.py). Native File New/Open/
Save As/Copy integrate the component schema. A `.cadprt` is a native archive plus
validated version/capability/identity manifest; merely renaming FCStd is refused.
Root-component Part icon, ordered history, shared embedded/external instances,
path representations, evaluated direct-child references, suppression, transactional
result conversion and isolated views are implemented for the bounded native result
mapping. Make Independent supports embedded/external definitions while sharing
children; externalization moves an embedded assembly closure and retains all shared
identities. Missing files require identity-preserving repair. Legacy root geometry
is adopted and unmapped native payloads retained/reported; original files are protected.

Remaining integration is dependency ordered, with this milestone retaining priority:

- [ X ] 7.8.3a Native envelope, required-capability preflight including renamed backup
  archives, atomic-writer reuse, external dependency identity and missing-file repair;
  Save As/Copy preserve identities and rejected Save As restores location/label.
- [   ] 7.8.3b Broader crash recovery/backup restoration, moved dependency packages,
  malformed graph/schema matrix and larger document acceptance.
- [ X ] 7.8.5a Body-independent shared sketch/extrusion and native transaction adoption;
  native Boolean result replacement restores prior visible results on suppression.
- [   ] 7.8.5b Integrate unified Extrude/Pad/Pocket and remaining native task editors
  with explicit component result roles; validate general split/merge and per-output
  topology lineage before enabling arbitrary multi-solid operations.
- [ X ] 7.8.5c Feedback iteration: route component-context Extrude/Pad/Pocket to a
  Body-independent native extrusion/Boolean task; explicit New Body/Add/Subtract,
  local profile/target, length/direction, preview/Cancel and editing without result
  identity replacement. This initial edit pilot kept the saved operation/target;
  7.8.5d extends editing to those choices.
  One solid result is required; no general split/merge or multi-target claim.
- [ X ] 7.8.5d Feedback batch: route both native New Sketch commands to a
  component-owned plane/face task without a Body prerequisite. Permit Extrude mode
  and target edits while preserving result and operation semantic identities;
  retain explicit refusal for direct operation consumers and expression remapping.
  Grouped Release build and three focused feedback checks pass; general topology
  and command migration remain under 7.8.5b.
- [ X ] 7.8.6a Result identity, exclusive-history pruning, shared producers, reference
  freezing, independent extraction and native Undo are covered by regression fixtures.
- [   ] 7.8.6b Prove real multi-body edge-treatment contribution detachment and
  expression/subelement reference preservation or explicit ambiguity refusal.
- [ X ] 7.8.7a Root component with native Part icon, both navigator tabs, representation
  inheritance/reset and a rendered isolated view; native New/Open/Save dialog checks.
- [   ] 7.8.7b Integrate assembly joint creation/solver with the first constraints
  group; complete repeated-path picking, native edit/create parity and owner GUI acceptance.
- [   ] 7.8.7c Connect separate BOM/mass participation flags to engineering consumers;
  validate multi-tab display overrides without changing engineering geometry.
- [ X ] 7.8.7d Feedback iteration: Model History double-click opens the component
  Extrude or native object editor; explicit suppression/dependency/repair states,
  Rename, retained navigator selection/expansion/scroll and single-Undo embedded
  component creation. Suppression invalidates dependent result caches even when a
  native Boolean fails before the result proxy can execute.
- [ X ] 7.8.7e Owner panel revision: remove path/file and creation buttons, make
  Edit first and double-click active, highlight the part, protect its visible branch,
  group repeated definitions with xN and expandable numbered instances, revise
  Instances/Part View/Save to External File menus, and add visibility and suppression
  controls before Model History item names. Three focused checks pass and four
  rendered captures were reviewed. Complete native navigator parity remains
  tracked in 7.8.7b.
- [ X ] 7.8.7f Native selection/context feedback batch: retain full occurrence paths
  between native selection and the two panel trees; preselect only unambiguous
  direct-child reference objects, make grouped Part View a single Undo, reuse open
  component tabs and restore per-view edit context. Grouped script/resource staging
  and three focused checks pass; full native interaction parity remains in 7.8.7b.
- [ X ] 7.8.8a Embedded/external Copy to New Part with child sharing; assembly
  externalization, reference remapping, shared child identity and save/reopen.
- [   ] 7.8.8b Explicit complete-hierarchy copy, general expression remapping and
  externalization with additional loaded external consumers. Current preflight
  refuses unsupported relationships instead of silently rebinding them.
- [ X ] 7.8.10a Published result updates through native Draft clone, CAM job model
  and TechDraw projection after save/reopen; suppressed inputs clear clone/CAM geometry.
- [   ] 7.8.10b FEM (disabled in this build), general drawing references, CAM path
  invalidation, broader topology changes, performance and interactive owner acceptance.

Validation evidence: `D:\Temp\Office-PC\freecad-plus-components-20261001`.
Grouped Release native App/Gui and PartScripts build passes are recorded under
`build-01` through `build-05`; the later builds correct demonstrated reader/save
integration defects. `model-21` passes **27** selected model, consumer and GUI checks;
`cold-03` passes **5** installed-module/native File command checks, with no failures,
errors or skips and native process exits 0. Cold module hashes match the checkout.
`cold-05` repeats all five checks successfully after the final native format guard,
including a legacy object named ComponentDocument and exact installed module hashes.
`cold-04` caught an unstaged navigator resource; staging corrected it, and the build
helper now explicitly includes FreeCADGui_Resources. Earlier failed runs remain
diagnostic evidence, not acceptance. The three model-21 captures
were reviewed: root Part icon/no file row, separate Model History and rendered
isolated geometry. TechDraw is checked after asynchronous restore finishes; edits
while that initial projection is still computing are not established by this fixture.
[Owner and test procedure](../tests/ComponentDocument.md).

Implementation/build/runtime evidence does not close the remaining child tasks.
No installer, public release or physical owner acceptance is claimed.
Implementation commit `d1a7a73be12ddd430e32689f9ff73bd3444d1606` was pushed to
`origin/main` (Croft-Labs/FreeCAD-Plus), then verified by `git ls-remote` at the same
full commit. This is source publication, not a release. Final native/runtime and
source identities are in `acceptance-identities.json` under the evidence root.
FreeCADApp SHA256: `8c6ac7d577afe97a526fbe9453e151573ea962b0d0d4ad62b0f0ac5e35c78d36`;
FreeCADGui SHA256: `280b29f39aeca19846c3ccf911d90fca9679c7a7d3a88ec31a781901f5eb39d9`.
The executable About/version metadata predates this rebuild and is not its source identity.

2026-10-01 feedback iteration (7.8.5c/7.8.7d): the owner requested several changes
before building, and limited checks until feedback stabilizes the file structure.
The extrusion service/task, native command routing and navigator/history changes
preceded **one grouped incremental Release build**, exit 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-component-iteration-20261001`.
`smoke-accepted` passes **three focused workflow checks**, no failures/errors/skips,
native process exit 0. Initial smoke failures identified quantity-widget use and
suppressed Boolean result-cache invalidation; Python corrections and a harness
widget-lifetime correction required no additional native build. The limited check
covers native Extrude/Pad/Pocket entry, no Body prerequisite for extrusion,
preview/Cancel, Add/Subtract, edit/Undo, suppression, failed-operation rollback,
save/reopen, atomic component creation and retained navigator selection. Two UI
captures were reviewed. A final status-text adjustment clears stale preview wording;
it is source-reviewed/staged without repeating the workflow suite.

This is an iteration for owner feedback, not file-format qualification. Existing
legacy native editors were retained at that milestone. Sketch routing and
operation/target editing continue in 7.8.5d; expressions, multi-result lineage,
assembly solver and broader consumer/recovery acceptance remain open. Do not rerun the broad suites solely to close this feedback
batch. [Procedure and current limits](../tests/ComponentDocument.md#current-feedback-iteration).
Source publication: implementation `7630012c25efae2e2c79b0102808b8331695a582`
pushed to `origin/main` and verified with `git ls-remote`. No installer or release.
The review fixture is `smoke-accepted/Component-Feedback.cadprt` under the iteration
evidence folder; use the local fork executable from the existing validation build.

2026-10-01 panel/sketch feedback batch (7.8.5d/7.8.7e): implementation preceded
one grouped Release build. The initial `build/` process ended during a session
interruption without a completion result; no processes survived. `build-resumed/`
completed with exit 0. Evidence root:
`D:\Temp\Office-PC\freecad-plus-component-panels-20261001`.
Native Part Design and Sketcher command routing, GUI resources and Part scripts are
included. Native Sketcher also needs the existing Show Python package; this was
staged afterward and added to the build helper for subsequent batches.

`smoke-accepted/` passes **three focused workflow checks**, no failures/errors/skips,
process exit 0 and an empty stderr log. Checked native New Sketch entry/cancel/editor,
Body-independent plane and associative local-face attachment, Extrude mode/target
editing with stable semantic operation/result identities, Undo and .cadprt reopen,
grouped instance names/counts and menus, active visibility protection, object
suppression/dependent result invalidation and restoration. Six loaded component
module hashes are checked against source by the suite. Four captures were reviewed:
component structure with x5/numbered instances, suppression/visibility columns,
Instances submenu and sketch plane task. `Component-Panel-Feedback.cadprt` and
`Component-Edit-Feedback.cadprt` in that folder are owner review fixtures.

Earlier smoke attempts exposed submenu wrapper lifetime/inspection and view-provider
close callbacks; Python corrections required no further native build. Capture review
then corrected ancestor expansion and unavailable-result visibility indicators.
This is bounded feedback evidence, not complete native-tree parity, schema lock-in,
assembly solver, arbitrary topology/expression or cross-workbench qualification.
No installer/release update. Implementation `5ecd62c94193cd040804147d9c9470062974fe2a`
was pushed to `origin/main` and verified with `git ls-remote`. Runtime/source/fixture
hashes are recorded in `acceptance-identities.json` under this evidence root.

2026-10-01 selection/context feedback batch (7.8.7f): native-path selection mapping,
reference preselection, grouped display transactions and tab context changes preceded
a grouped script/resource staging build. Evidence:
`D:\Temp\Office-PC\freecad-plus-component-selection-20261001`.
The initial build staged changed GUI/Part modules but failed at the inherited helper's
Show target, absent because BUILD_SHOW is disabled. The corrected helper uses that
target only when configured; otherwise it stages the existing Python support files.
`build-corrected/` exits 0. Native C++ artifacts were not rebuilt.

`smoke-accepted/` passes **three focused checks**, zero failures/errors/skips, native
process exit 0 and empty stderr: exact repeated/nested native selection round-trip,
active-context history selection, grouped selection and single-Undo display changes,
unambiguous direct-child reference preselection with whole-object review and .cadprt
reopen, and isolated-tab reuse/restoration. Two panel captures were reviewed. The
fixture is `smoke-accepted/Component-Selection-Feedback.cadprt`. Loaded module hashes
match source. Earlier attempts exposed a test assumption: native addSelection can
canonicalize a bare source object to an occurrence before the mapper sees it. The
ambiguity boundary is therefore checked before native normalization; the GUI always
reviews the native occurrence that it receives. No mouse-ray picking, full native
editor parity, external-view matrix, broader consumer or schema qualification is
claimed. No installer/release update. Source publication pending.

### [   ] 7.7 Validate and release the history pilot

- [   ] 7.7.1 Create regression fixtures for empty-part creation, disconnected solids, shared sketches, multiple intersecting targets, merge/split lineage, nested placements and legacy documents.
- [   ] 7.7.2 Test geometry, dependency recompute, references/expressions, rollback, reorder, suppression, deletion, Cancel, Undo/Redo and save/reopen, including edits that change the number of output bodies.
- [   ] 7.7.3 Run native mouse/keyboard acceptance for navigator and viewport selection, history insertion, create/edit parity and ambiguous-target recovery.
- [   ] 7.7.4 Compare recompute time and navigator responsiveness on small and larger multi-body histories; define measurable acceptance thresholds before declaring performance complete.
- [   ] 7.7.5 Supply a testable build and example document, record compatibility limitations, and retain a reversible opt-in until the pilot passes. Track source, build, tests, user acceptance and GitHub push separately.

<a id="nx-modeling-workflows"></a>
## [   ] Phase 8: Consistent NX/SolidWorks-inspired modeling workflows

Depends on the applicable Phase 7 model/result contracts. Shared task-pane work
that preserves current model semantics may proceed independently when separately
authorized. Phase 3 remains the canonical operation inventory; do not duplicate its
implementation or mark its unfinished validation complete through this plan.

### [   ] 8.1 Standardize the complete feature task

- [   ] 8.1.1 Define one shared task order: operation/type, input collectors, target bodies, geometry parameters, direction/extents, preview and acceptance. Hide only genuinely inapplicable controls.
  Name collectors by purpose: Profile, Axis, Target Bodies, Guides and Limits. Each
  collector highlights its assigned geometry. Preselection and selection after invoking
  the command must produce equivalent definitions, with the same editable inputs on
  reopen.
- [   ] 8.1.2 Apply command-first selection and identical create/edit coverage to the Phase 3 audit, including profile/section/path/axis replacement after reopening a feature.
- [ X ] 8.1.2a Reuse each Trim Body/Isocline collector's input validation for
  preselection and later picks. Show ignored inputs with reasons; retain valid
  inputs and reject ambiguous multiple Trim tool faces without choosing one.
  Verify mixed picks, document scope, correction and equivalent definitions. F031.
- [ X ] 8.1.2b Route Extrude and legacy Pad/Pocket preselection through the
  same profile gate and assignment as command-first picking. Ignore invalid picks
  with visible reasons; require explicit choice for multiple profile objects.
  Mixed whole solids/bodies do not replace the active Body or become profiles.
  Parity, invalid-input recovery and selection-order regressions pass; evidence below.
- [ X ] 8.1.2c Route combined Pattern preselection and later Originals picks through
  shared document/body/type/dependency validation and assignment. Retain valid
  mixed inputs, deduplicate subelements and leave invalid-only input recoverable.
  Linear/Circular parity, geometry and Cancel recovery pass. F031; evidence below.
- [   ] 8.1.3 Standardize named selection collectors with add/remove/clear, viewport/tree picking, compatible-type filters, chain/region selection and visible invalid-reference feedback.

- [ X ] 8.1.3a Add input inspection to existing Trim Body and Isocline collectors:
  Target/Tool Highlight, face-list row highlighting and direction-reference
  Highlight. Inspection retains the active role without consuming its own picks;
  temporary visibility follows task exit rules. F030 production slice.
- [ X ] 8.1.3b Add Isocline direction-reference Clear, retain Reference mode, clear
  stale preview even while paused, and permit correction or Cancel recovery.
  Empty collectors disable Highlight/Clear. F030 production slice.
- [ X ] 8.1.3c Show collector entry counts, accepted types and the active picking
  role as text in Trim Body and Isocline. Preserve required input-group ordering;
  refresh feedback after picks, duplicates, clear, removal and reopen. Counts are
  collected entries, not expanded face totals. F030.
- [ X ] 8.1.3d Add Extrude/Pad/Pocket profile row inspection and Highlight for
  selected/all entries. Explicitly activate Profile without assigning inspection
  picks to any collector; restore temporary visibility on exit. F030.
  Row/all-entry, role isolation and Cancel/OK visibility checks pass; evidence below.
- [ X ] 8.1.3e Show Extrude profile entry counts, accepted types and picking state.
  Refresh on pick/remove/clear/reopen and role switches; a whole profile counts
  as one entry. F030. Mutation, duplicate, clear and reopen checks pass; evidence below.
- [ X ] 8.1.3f Add named Originals count/type/picking feedback to the combined
  Pattern task, including retained feature counts in Whole body mode. F030.
  Mutation, duplicate, retained-count and reopen checks pass; evidence below.
- [ X ] 8.1.3g Add explicit Pattern Originals Clear with empty-input recovery,
  retained Linear/Circular settings and Cancel/Undo/Redo coverage. F030/F032.
  Clear/replacement, empty acceptance and rollback checks pass; evidence below.
- [ X ] 8.1.3h Coordinate combined Pattern originals and embedded direction/axis
  selection so a pick cannot fill both roles, including Clear/Add/Remove transitions.
  F030 role isolation. Both transition directions pass; evidence below.
- [ X ] 8.1.3i Add combined Pattern Originals row/all-entry inspection by object
  identity, with reference isolation and temporary visibility cleanup on role/type
  changes and OK/Cancel. F030. Native inspection and lifecycle checks pass; evidence below.
- [ X ] 8.1.3j Explain rejected Pattern Originals picks inline, including document,
  Body, type, dependency, duplicate and unlisted-removal cases. Keep picking active
  after rejection; clear feedback on successful correction or Clear. F030/F031.
  Rejection, correction and readable feedback checks pass; evidence below.
- [ X ] 8.1.3k Add combined Pattern reference counts/type hints and active picking
  feedback for Direction, Direction 2 and Circular Axis. Track replacement, empty
  references and type/role changes. F030. Native feedback and correction checks pass.
- [ X ] 8.1.3l Add stored direction/axis reference inspection without assigning to
  other collectors. Preserve subelement identity and restore temporary visibility
  on role/type changes and OK/Cancel. F030/F032. Identity, role/visibility lifecycle
  and saved-reference acceptance checks pass; evidence below.
- [ X ] 8.1.3m Explain rejected Body/sketch/datum Originals picks by accepted type
  before dependency checks. Keep genuine result/downstream rejections distinct and
  preserve correction behavior. F030/F031. Native rejection/correction checks pass;
  the Pattern result retains its dependency-specific reason. Grouped evidence below.
- [   ] 8.1.4 Standardize signed offsets, adjacent direction buttons, one/two-sided and symmetric modes, units and expressions. Preserve parameters by meaning when switching operation or type.
  Cover distance, symmetric, two-sided, through-all, to-face and offset-from-face
  extents where the command supports them; keep extent semantics distinct from the
  existing sketch-plane start offset. Specify shared solid/surface and Boolean/target
  conventions for Sweep and Loft.
- [ X ] 8.1.4a Clarify Extrude/Pad/Pocket total symmetric and independent per-side
  length labels, with measured geometry checks and edit/reopen coverage. F029.
  Native labels, measured extents and reopen checks pass; grouped evidence below.
- [ X ] 8.1.4b Route typed second-side face limits to their own saved reference;
  verify moving/offset limiting faces, missing-face repair, Cancel, Undo/Redo and
  save/reopen associativity. F029. Native reference isolation and lifecycle checks
  pass in the grouped 8.1.4a/b batch below.
- [ X ] 8.1.4c Clear only the edited Extrude face-limit link for empty/malformed
  text, preserving a repairable error and rejecting invalid OK with preview on/off.
  Verify both sides, aliases and edit Cancel. F029/F032. Native recovery/OK and
  Cancel checks pass; grouped evidence below.
- [ X ] 8.1.4d Apply typed datum/origin plane limits to the correct side during
  preview; verify face-to-plane repair, Undo/Redo and save/reopen associativity.
  F029. Native plane assignment, repair and persistence checks pass; grouped
  evidence with 8.1.4c below.
- [ X ] 8.1.4e Reject self/downstream Extrude end-limit references before assignment
  in typed and picked paths; keep picked rejection recoverable and typed invalid OK
  open, with Cancel restoring the definition. F029/F031. Native self/dependency,
  correction and transaction checks pass; grouped evidence below.
- [ X ] 8.1.4f Apply existing Body ownership/type rules to typed datum/origin end
  planes and preserve valid references on rejected picks. F029/F030. Native
  ownership and owned-plane correction checks pass; grouped evidence below.
- [   ] 8.1.5 Add consistent live-preview and error states; make Cancel restore geometry, visibility and selection. Define Apply/repeat behavior separately from OK so repeated creation does not create accidental features.

- [ X ] 8.1.5a Restore original selection on Trim Body/Isocline creation Cancel,
  edit Cancel and failed startup. Capture before command preselection is consumed;
  retain original occurrence/subelement paths instead of resolved definitions.
  Shared FeatureTask helpers; F031/F032 cancellation slice, not Apply/repeat.

- [ X ] 8.1.5b Restore original object/subelement selection after Extrude/Pad/Pocket
  creation or edit Cancel, alongside existing profile and Body Tip rollback.
  Create/edit Cancel passes for all three command entries; evidence below.
- [ X ] 8.1.5c Restore original combined Pattern selection on creation/edit Cancel,
  preserving original object/subelement paths alongside Originals/settings/Body Tip
  rollback. F031/F032. Both creation/edit cases pass; grouped evidence below.

- [ X ] 8.1.5d Preserve stored Pattern direction/axis references when unfinished
  picking ends through Originals controls, scope/type changes or OK. End stale
  reference observers and retain edit Cancel selection/model recovery. F031/F032.
  Primary/secondary/axis, scope/type/role, OK/Undo and edit Cancel checks pass;
  grouped evidence with 8.1.3m below.
- [   ] 8.1.6 Make previews responsive with cancellable computation, progress
  feedback and reduced-cost previews before final computation. Clearly distinguish
  provisional geometry from committed results; cancellation restores the previous
  model, and a late preview result cannot overwrite newer inputs. Integrate with
  16.5's thread-safety/result-commit rules before background document work.

**Collector batch evidence (8.1.3a/b, 8.1.5a), 2026-09-30:** Seven added GUI
regressions pass in one grouped checkpoint: Trim task 20, Isocline task 18,
Trim geometry 14, Isocline geometry 9, shared CAM/mesh lifecycle 24; **85 passes,
zero failures/errors/skips**, macro PASS and process exit 0. Five source/staged
Python file hashes match. Runtime engine `802e19d648` with staged Python changes;
no native rebuild or release. Evidence:
`D:\Temp\Office-PC\freecad-plus-collectors-20260930\grouped-staged`, with staging hashes
in its parent. Initial harness attempts stopped before tests (macro encoding and
already-loaded overlay modules); direct development-build staging resolved them.
Syntax/whitespace checks pass; all 127 specification IDs remain unique and ordered.
No property/schema, geometry or persistence format changes. Broad 8.1/F030-F032
acceptance (other commands, disambiguation, Apply/repeat and physical interaction)
remains open. Next dependency-ready slice: collector type/count feedback and
explicit invalid-preselection feedback in these production editors.

**Collector feedback batch (8.1.2a, 8.1.3c, 5.1.11), 2026-09-30:** Nine added
regressions plus existing GUI/model checks: Trim task 24, Isocline task 23,
Trim geometry 14, Isocline geometry 9; **70 passes, zero failures/errors/skips**,
macro PASS, process exit 0. Four changed Python files hash-match the development
build. Existing engine `802e19d648`; no native rebuild or release. Evidence:
`D:\Temp\Office-PC\freecad-plus-collector-feedback-20260930\verified` and parent
`staging-identities.json`. Both Qt task panels were captured and visually checked
under the sibling `visual` directory; labels, warnings and controls are readable
without clipping in those captures. Physical input/high-DPI acceptance remains
separate. Initial checks caught input-group ordering regressions (corrected) and the native whole-object LinkSubList omission (fixed under 5.1.11).
Preselection parity is verified for these editors, not the full F031 Extrude
acceptance. Counts/type hints and explicit rejection do not complete general
selection filters or disambiguation. Next independent product slice: expose the
existing Isocline tolerance in its create/edit task and validate its F070 semantics.

**Extrude selection batch (8.1.2b, 8.1.5b), 2026-09-30:** Both native changes
were grouped before the first PartDesignGui Release build. Initial regressions
caught the base view provider clearing edit selection before dialog construction;
`ViewProviderExtrude::setEdit` now captures it earlier. A follow-up native build
passes. Test fixtures were corrected to compare compound solids' centers and use
the quantity widget's `rawValue` helper; native code did not change afterward.
Final acceptance: **138 passes, zero remaining failures/errors/skips**: Extrude
task 24, Pad task 14, Extrude model 8, Pad model 14, Pocket model 6, Revolve task 5,
Pattern task 17, Trim task 24, Isocline task 26. The final 24-test Extrude rerun
passes (macro PASS, exit 0); the other 114 passing checks are retained from the
grouped run against the same rebuilt native modules. Earlier failed runs remain
in the evidence, not counted as acceptance. Evidence root:
`D:\Temp\Office-PC\freecad-plus-extrude-selection-20260930`, with `build.log`,
`verified`, `extrude-final`, `acceptance-summary.json`, `validated-identities.json`
and readable, visually checked mixed/ambiguous Profile captures under `visual`.
Six changed source hashes and the staged test identity are recorded; PartDesignGui
SHA256 `02d7224188574514a67f5a981d9a25cd5100f53f72c7df0256b248c76093e76c`.
The executable's existing `802e19d648` version stamp does not identify these rebuilt
modules. No installer or release. All 127 item IDs remain unique and ordered.
F031's specified Extrude parity/mixed-selection/Cancel example is complete for
the active-Body workflow. Whole solid/Body picks are explained as ignored profile
inputs; they do not introduce multi-target Boolean semantics. Broad occurrence,
other-family and physical input/high-DPI acceptance remains open, as does F032's
Apply/repeat workflow. Next bounded product slice: F030 Extrude collector inspection
and count/type feedback.

**Extrude collector batch (8.1.3d/e), 2026-09-30:** Both tasks were implemented
before one successful PartDesignGui Release build and one grouped native run.
**142 passes, zero failures/errors/skips**, macro PASS and process exit 0:
Extrude task 28 (four new regressions), Pad task 14, Extrude model 8, Pad model 14,
Pocket model 6, Revolve task 5, Pattern task 17, Trim task 24 and Isocline task 26.
Profile row/all-entry inspection explicitly activates Profile, guards its own
selection callbacks, preserves reference/geometry definitions and restores temporary
visibility on Cancel/OK. Feedback counts collected entries, not expanded edges;
duplicate picks, removal, clear, role switching and reopen are covered.
Evidence: `D:\Temp\Office-PC\freecad-plus-extrude-collectors-20260930`, with
`build.log`, `grouped/results.json`, `source-identities.json` and
`validated-identities.json`. Source/staged test hashes match. PartDesignGui SHA256:
`1c1bef4b22a721fdc1335da5233062e21262dd0750ad3e56bbec39621adef3ce`.
The unchanged executable version stamp is not the rebuilt module identity.
Empty/whole/individual-curve collector captures under `visual` were inspected;
text and buttons are readable without clipping. Physical input/high-DPI, general
occurrences and other command-family/disambiguation gates remain open. All 127
item IDs remain unique and ordered. No document property/schema changes, installer
or release. Next bounded focus: audit Pattern originals collection against F030.

**Pattern collector batch (8.1.3f-h), 2026-09-30:** Three related changes preceded
one successful PartDesignGui Release build and one grouped run. **144 distinct
tests pass (149 executions), zero failures/errors/skips**, macro PASS, process
exit 0. Pattern task module: 22 executions (17 GUI cases including five new cases,
plus five imported Pattern model cases); explicit Pattern model 5, Linear model
16, Polar model 6, MultiTransform model 3, Pad task 14, Extrude task 28, Revolve
task 5, Trim task 24 and Isocline task 26. The explicit Pattern model suite repeats
five imported cases; `acceptance-summary.json` records the distinct count.
New coverage includes count/type/picking feedback, Whole body retention, Clear
from direction picking, empty acceptance/recovery, retained settings, Cancel and
Undo/Redo, and direction/originals transitions that change only the intended role.
New controls are scoped to combined Pattern; legacy task/model checks pass.
Evidence: `D:\Temp\Office-PC\freecad-plus-pattern-collectors-20260930`, with
`build.log`, `grouped/results.json`, `source-identities.json` and
`validated-identities.json`. Seven changed source identities and the staged test
hash match. PartDesignGui SHA256:
`0843f5f52fd8bce6e68b952dc8f89cb2a3136ca47fa8f6baf702150467a83639`.
The executable's older version stamp does not identify these rebuilt modules.
Readable empty/selected/Whole body captures are under `visual-final`; an initial
capture caught an in-progress radio animation, so the harness now lets Qt settle
and records checked/model states. No product correction or rebuild was needed.
Physical input/high-DPI, broader inspection/disambiguation/occurrence and Apply/
repeat gates remain open. All 127 item IDs remain intact. No document property
schema changes, installer or release. Next slice: Pattern row inspection and
selection recovery against F030/F031.

**Pattern inspection/recovery batch (8.1.3i, 8.1.5c), 2026-09-30:** Both tasks
preceded one successful PartDesignGui Release build. **149 distinct final tests
pass, zero remaining failures/errors/skips**: 27 Pattern task/model, 16 Linear,
6 Polar, 3 MultiTransform, 14 Pad task, 28 Extrude task, 5 Revolve task, 24 Trim
task and 26 Isocline task. Five new GUI cases cover duplicate-label row identity,
all-entry inspection without model mutation, direction/type transitions, visibility
on OK/Cancel and original subelement selection plus model rollback on create/edit
Cancel. Pattern-only snapshot capture leaves legacy transformation behavior intact.
Evidence: `D:\Temp\Office-PC\freecad-plus-pattern-inspection-20260930`, including
`build.log`, `grouped`, `final`, `acceptance-summary.json` and
`validated-identities.json`. The initial run retained one test-fixture failure:
it compared editing visibility with idle visibility. It later reached the inactivity
limit in the existing Revolve matrix; that timeout's cause is unconfirmed. After
moving the fixture baseline before entering edit, a fresh process passed all 82
Pattern/Revolve/Trim/Isocline checks (macro PASS, exit 0). The other 67 passing
checks are reused from the initial run on identical native binaries. No native
correction or second build. Source, staged test and native identities are verified.
PartDesignGui SHA256:
`70fc6c433231bbabe8c1041eee565f10c91201da119ef4f02a9de3611af7bafc`.
The older executable version stamp is not rebuilt-module identity. Three readable
empty/inspection/Whole body task captures are under `visual`; this does not close
physical viewport/input/high-DPI acceptance. All 127 item IDs remain intact; no
property schema changes, installer or release. Broader F030 command-family,
disambiguation/occurrence, F031 Pattern preselection parity and F032 Apply/repeat
remain open. Next slice: Pattern preselection parity and invalid/mixed-selection
explanations, grouped before the next build.

**Pattern selection batch (8.1.2c, 8.1.3j), 2026-09-30:** Both tasks preceded
one successful PartDesignGui Release build. **155 distinct final tests pass,
zero remaining failures/errors/skips**: 33 Pattern task/model, 16 Linear, 6 Polar,
3 MultiTransform, 14 Pad task, 28 Extrude task, 5 Revolve task, 24 Trim task and
26 Isocline task. Six new GUI cases cover Linear/Circular preselection versus
later picks, mixed and invalid-only inputs, cross-document rejection, dependency/
duplicate rejection, unlisted removal and correction. The parity case checks
membership, saved settings and bidirectional geometry differences after reversing
selection order, and reopening/Cancel/Undo. Multiple face picks remain one original.
Combined Pattern startup uses its collector's validation/assignment instead of the
legacy modal preselection path; legacy commands retain their startup behavior.
Evidence: `D:\Temp\Office-PC\freecad-plus-pattern-selection-20260930`, including
`build.log`, `grouped`, `pattern-final`, `acceptance-summary.json` and
`validated-identities.json`. The initial run retained one fixture failure comparing
raw Originals input order. The native engine already evaluates in Body-history
order; the test now compares membership and adds both geometric differences.
All 33 corrected Pattern task/model tests pass (macro PASS, process exit 0), plus
122 unchanged passing grouped checks on identical native binaries. No native
correction or second build. Source, staged tests and native identities match.
PartDesignGui SHA256:
`b1123a2ba699ab3f709d37a64419c2ca74b257b491946c037e7b453543b614c4`.
Three mixed/rejected/recovered task captures under `visual` are readable without
clipping; corrected input hides the hint. The older executable version stamp does
not identify rebuilt modules. All 127 item IDs remain intact. No document property
schema change, installer or release. Broader command-family/occurrence/disambiguation,
physical input/high-DPI and F032 Apply/repeat acceptance remain open. Next bounded
slice: Pattern direction/axis collector inspection and recovery under F030.

**Pattern reference batch (8.1.3k/l), 2026-09-30:** Both tasks preceded the initial
PartDesignGui Release build. Native review follow-ups added source visibility lookup
through subobject paths and restored reference combos after inspection, preventing
OK from applying a pending "Select reference" item. Two incremental corrective
rebuilds followed; all builds passed. **161 distinct final tests pass, zero remaining
failures/errors/skips**: 39 Pattern task/model, 16 Linear, 6 Polar, 3 MultiTransform,
14 Pad task, 28 Extrude task, 5 Revolve task, 24 Trim task and 26 Isocline task.
Six new GUI cases cover primary/secondary/axis feedback, empty-reference recovery,
reference inspection without cross-role assignment, source and Origin visibility,
type/role transitions, saved links after OK and original-selection restoration on
Cancel. Resolved links and the GUI's canonical Body selection paths are checked
separately. New controls remain scoped to combined Pattern; shared visibility
cleanup preserves document/object identity. Broader assembly occurrence behavior
is not established by these active-Body cases.
Evidence: `D:\Temp\Office-PC\freecad-plus-pattern-references-20260930`, including
`build-initial.log`, `build-source-visibility.log`, `build.log`, `grouped`,
`pattern-final`, `verified`, `pattern-accepted`, `acceptance-summary.json` and
`validated-identities.json`. Initial fixture errors retained: temporary PySide
parent wrappers were released; a later assertion conflated resolved stored links
with canonical GUI paths. Corrected 39 Pattern tests pass (macro PASS, exit 0),
plus 122 passing `verified` checks on identical final native binaries. Final source,
staged test and native hashes match. PartDesignGui SHA256:
`abb35d8b7cdbc7e0822f2280c7aa7c2af4f38448adbeb649655cea732e677d0b`.
Four readable captures under `visual` cover picking, a hidden-source edge reference,
Direction 2 and Circular Axis. The older executable stamp is not rebuilt-module
identity. All 127 item IDs remain intact. No property schema change, installer or
release. Physical input/high-DPI, broader command/occurrence/disambiguation and
F032 Apply/repeat gates remain open. Its reference recovery/rejected-pick follow-up
is completed in the next batch below.

**Pattern picker recovery batch (8.1.3m, 8.1.5d), 2026-09-30:** Both tasks
preceded the initial PartDesignGui Release build. Old binaries reproduced saved
reference loss after abandoned picking, stale reference picking after scope changes
and misleading Body rejection. Combined Pattern now restores saved reference combos
whenever pending reference picking ends, including apply/type/scope transitions.
Body/sketch/datum Originals receive type guidance; the Pattern result and supported
downstream features retain dependency guidance. New behavior stays scoped to the
combined Pattern workflow; legacy transform regression checks pass.
The first grouped run passed all six new tests and 122 broader checks, but caught
one existing result-specific diagnostic regression. One corrective incremental
rebuild followed; both builds passed. **167 distinct final tests pass, zero
failures/errors/skips**: 45 Pattern task/model, 16 Linear, 6 Polar, 3 MultiTransform,
14 Pad task, 28 Extrude task, 5 Revolve task, 24 Trim task and 26 Isocline task.
Coverage includes Add/Remove/Clear exits, primary/secondary/axis OK, type switches,
scope changes without later-pick consumption, type rejection/correction, Undo and
edit Cancel selection/model recovery. No new test fixture correction was required.
Evidence: `D:\Temp\Office-PC\freecad-plus-pattern-picker-recovery-20260930`, including
`baseline`, `build-initial.log`, `build.log`, `grouped`, `verified`, `visual`,
`acceptance-summary.json` and `validated-identities.json`. Baseline loop failures
after failed cleanup are not separate defect evidence. Final macro PASS, exit 0;
source, staged test and native identities match. PartDesignGui SHA256:
`b2e935fb8bc4272854139c581a97aa8b53fdb142c467e94141d14d03c1fe2c65`.
Three readable captures cover Body rejection, Originals-role cancellation and
Whole body scope cancellation. The older executable stamp is not rebuilt-module
identity. All 127 item IDs remain intact. No property/schema or persistence-format
change, installer or release. Broader command-family/occurrence/disambiguation,
physical input/high-DPI and F032 Apply/repeat acceptance remain open.

**Extrude extent batch (8.1.4a/b), 2026-09-30:** Both changes and six new
regression cases preceded one successful PartDesignGui Release build. Symmetric
mode now labels Length as Total length, and two-sided mode shows independent
Side 1 length / Side 2 length. Tooltips explain half-length and end-face offset
semantics. Typed side 2 face references now target UpToFace2 instead of changing
UpToFace during preview; the shared parser keeps its first-side legacy default.
**201 distinct tests pass, zero failures/errors/skips**: 11 Extrude model, 14 Pad
model, 6 Pocket model, 31 Extrude task, 45 Pattern task/model, 16 Linear, 6 Polar,
3 MultiTransform, 14 Pad task, 5 Revolve task, 24 Trim task and 26 Isocline task.
New acceptance covers measured one/two/symmetric spans with a shifted start plane,
labels on edit/reopen, typed second-side isolation and edit Cancel, moving limiting
faces with signed end offsets for both operations and stored feature types, removed
limits with Undo/Redo, repair, save/reopen followed by another face move, lost face
subelements and repair in the existing editor. Missing limits retain Up to face
mode and report an error. Existing model behavior was reused without schema or
geometry-kernel changes; the new production fix is the typed-reference destination.
Evidence: `D:\Temp\Office-PC\freecad-plus-extrude-extents-20260930`, including
`baseline`, `baseline-model-final`, `build.log`, `grouped`, `extrude-final`, `visual`,
`acceptance-summary.json` and `validated-identities.json`. Old binaries reproduced
the generic labels and wrong-side reference mutation. Initial persistence fixture
error retained: reopening a just-saved active document returned that same document;
saveCopy provides an independent file. All three corrected model cases passed
before the build. The grouped run found a test assumption that Pocket shared Pad's
default axis; corrected bounds use Pocket's inherited opposite direction. The final
31-test Extrude GUI run and 170 broader grouped checks pass on identical native
binaries. No corrective native rebuild was needed. Final macro PASS,
exit 0; all six source files, two staged tests and native hashes match.
PartDesignGui SHA256:
`57acdd8b8fd4c545cfdf98fc18b15503aa6b542e7fac7604783d2b0214d2e3a5`.
Three readable task captures cover Symmetric, Two sided and independent face limits.
The older executable stamp is not rebuilt-module identity. All 127 item IDs remain
intact. No installer/release. F029's specified Extrude face-move, documented-length
and missing-limit repair examples are validated for this active-Body workflow;
broader command consistency and physical input/high-DPI acceptance remain open.

**Extrude typed-limit recovery batch (8.1.4c/d), 2026-09-30:** Both fixes and
six new GUI cases preceded one successful PartDesignGui Release build. Empty or
malformed text clears only the edited side's saved link and recomputes its error,
so OK cannot accept the previous result as valid. Numeric missing-face references
retain their repairable error. Explicit-target face parsing rejects trailing text;
typed datum/origin planes assign their saved link and recompute before OK. The
shared parser's legacy caller behavior remains unchanged.
**207 distinct tests pass, zero failures/errors/skips**: 11 Extrude model, 14 Pad
model, 6 Pocket model, 37 Extrude task, 45 Pattern task/model, 16 Linear, 6 Polar,
3 MultiTransform, 14 Pad task, 5 Revolve task, 24 Trim task and 26 Isocline task.
Six new cases cover both sides and stored Pad/Pocket aliases, empty/unknown/
incomplete/trailing input, missing numeric faces, valid correction, invalid OK
with automatic preview on/off, edit Cancel links/Body Tip/geometry, typed datum
and origin planes before OK, Undo/Redo and save/reopen followed by a plane move.
Evidence: `D:\Temp\Office-PC\freecad-plus-extrude-limit-recovery-20260930`, including
`baseline`, `build.log`, `grouped`, `extrude-final`, `visual`, `acceptance-summary.json` and
`validated-identities.json`. Old binaries reproduced stale links, invalid OK
closing the task and typed-plane assignment delayed until OK. Existing numeric
missing-face errors already passed. The first grouped run exposed a fixture error:
a cleared PropertyLinkSub returns None, not a tuple containing None. Corrected
37-test Extrude GUI checks pass alongside 170 broader grouped checks on unchanged
binaries. No corrective native rebuild. Final macro PASS, exit 0; source identities, the
staged test and native hashes match. PartDesignGui SHA256:
`7db59a73df9cc8f05193145f1a30265b52ae992506473cc636ed389c900a8b11`.
Three readable captures cover a cleared first side, malformed second side and
valid typed planes. All 127 item IDs remain intact. The older executable stamp
is not rebuilt-module identity. No schema/geometry-kernel/native-format change,
installer or release. Broader command/occurrence/dependency-selection, physical
input/high-DPI and F032 Apply/repeat acceptance remain open.

**Extrude end-limit restrictions batch (8.1.4e/f), 2026-09-30:** Both fixes
and six GUI regression cases preceded one successful PartDesignGui Release build.
Typed end limits reuse NoDependentsSelection before assigning a link. Picked end
faces also reject self/downstream references before assignment, retaining the saved
reference, displayed name and active picker for correction. Typed datum/origin
planes and picked datums use the existing ReferenceSelection Body/type policy.
The shared parser's legacy callers and ordinary external-face policy are preserved.
**213 distinct tests pass, zero failures/errors/skips**: 11 Extrude model, 14 Pad
model, 6 Pocket model, 43 Extrude task, 45 Pattern task/model, 16 Linear, 6 Polar,
3 MultiTransform, 14 Pad task, 5 Revolve task, 24 Trim task and 26 Isocline task.
New cases cover typed self links on both sides/aliases, direct and indirect
synthetic dependants, rejected self/dependent viewport picks, valid replacement,
foreign-Body datum/origin planes, owned-plane picking, invalid OK and edit Cancel
restoring accepted links, Body Tip, geometry and dependency direction.
Evidence: `D:\Temp\Office-PC\freecad-plus-extrude-reference-gates-20260930`, including
`baseline`, `baseline-scope`, `build.log`, `grouped`, `visual`,
`acceptance-summary.json` and `validated-identities.json`. Old binaries reproduced
foreign-plane scope bypass. The second baseline uses a unique foreign-origin label
so ownership is tested independently of label ambiguity. Deliberate cycles were
not assigned to old binaries; source audit identified the missing dependency guard.
No corrective native rebuild. Final macro PASS, exit 0; three source identities,
the staged test and native hashes match. PartDesignGui SHA256:
`065d9f5af5615cfcef42909b801840e0457132b924fb3420afca98376fa36969`.
Three readable captures cover typed self rejection, typed foreign-plane rejection
and a rejected dependent pick retaining its saved limit. All 127 item IDs remain
intact. The older executable stamp is not rebuilt-module identity. No schema,
geometry-kernel or native-format change, installer or release. Start-reference,
broader command/occurrence/global-filter, physical input/high-DPI and F032
Apply/repeat acceptance remain separate open gates.

### [   ] 8.2 Finish unified command families

- [   ] 8.2.1 Complete the existing Extrude and Linear/Circular Pattern acceptance gates, then adapt them to part-level results and reusable inputs without regressing legacy features.
- [   ] 8.2.2 Combine Revolution/Groove as Revolve with Add/Subtract, retaining angular offsets and direction controls; add automatic/new-body handling from 7.4.
- [   ] 8.2.3 Implement unified Loft, Sweep and Helix from milestone 3.6, retaining ordered sections, path/orientation controls and family-specific validity rules.
- [   ] 8.2.4 Consolidate primitives into a shape selector plus operation/target controls. Define parameter and identity behavior before allowing an existing primitive to change shape type.
- [   ] 8.2.5 Extend Pattern deliberately to Mirror and supported path/point patterns; distinguish repeating features, whole bodies and geometry copies, with clear result scope.
- [   ] 8.2.6 Align Boolean, Trim and future Split workflows with common target/tool collectors and keep/discard previews. Keep Hole, Draft, Shell/Thickness and edge treatments specialized where their parameters differ.

### [   ] 8.3 Improve sketch-to-feature interaction

- [   ] 8.3.1 Create or edit a sketch from a feature's profile collector and return to the same pending feature task, with clear transaction and cancellation behavior.
- [   ] 8.3.2 Preview selectable enclosed sketch regions and curve chains; explain gaps, self-intersections and ambiguous regions before attempting a solid operation.
- [   ] 8.3.3 Define consistent sketch orientation, origin, normal and attachment controls, plus associative projected/intersection geometry across bodies.
- [   ] 8.3.4 Test shared-sketch edits across multiple consumers and provide dependency feedback before changes invalidate downstream features.

### [   ] 8.4 Make the modeling interface consistent

- [   ] 8.4.1 Define a coherent Modeling command set across current Part/Part Design boundaries. Route by valid inputs/results rather than requiring users to change workbenches to find equivalent operations.
- [   ] 8.4.2 Add searchable command names and familiar aliases, contextual right-click actions, predictable double-click editing and discoverable shortcuts; retain legacy names for scripts and compatibility.
- [x] 8.4.2a Deliver a bounded F033 command-search catalog: preserve command
  identities, route familiar extrusion/revolution/pattern aliases into existing
  editors, and display current user shortcuts. Complete for owner testing.
- [x] 8.4.2b Add the standard Tools-menu/keyboard launcher, explicit workbench
  switching, selected-command availability and missing-workbench/context recovery.
  Pocket search reaches Subtract with native geometry, Undo/Redo and persistence.
  Complete for owner testing; active-Assembly and physical input acceptance remain open.

8.4.2a/b grouped evidence (2026-09-30): one FreeCADGui/FreeCADGui_Resources
Release build, exit 0, after both implementation tasks. Final selected acceptance
has 59 distinct passes: 7 palette tests, 43 Extrude task tests, 5 Revolve task
checks and 4 named-parameter command checks; no failures/errors/skips in accepted
results. Root: `D:\Temp\Office-PC\freecad-plus-command-search-20260930`.
Use `search-final/` for the corrected palette suite and the three passing suites
in `verified/`; the latter aggregate retains initial palette failures and is not
claimed PASS. `grouped/` stopped before tests because optional QtTest was absent;
key events now use QApplication. Final Python-only corrections were staged
without another native build. Source/runtime hashes match in
`validated-identities.json`; FreeCADGui SHA256:
`9bcb059b9c0428816035ca768715b0282776cb4d8ac3e30599fc2c7dd14c3f53`.
`visual/` holds three reviewed readable captures and `Search-Pocket.FCStd`.
`acceptance-summary.json` selects the passing evidence. Assembly is excluded by
this build's BUILD_ASSEMBLY=OFF: the palette reports the missing workbench and
required context without launching anything. Active-assembly recovery is unverified.
[Test the workflow](../tests/CommandSearch.md), then refine from owner feedback.
Whole F033, 8.4.2 and 10.4 remain open for broader interaction, favorites/context,
navigation and physical/high-DPI/localized acceptance. No installer/release update.
Rotate the next batch to another dependency-ready family.

- [   ] 8.4.3 Define viewport manipulators for direction, extent, offset and placement that update the same task properties and expressions as numeric controls.
  Handles include lengths, angles, offsets and radii, with exact numeric entry using the
  same properties. Dragging must not bypass expressions, validation or cancellation.
- [   ] 8.4.4 Add consistent face/edge/body/reference selection filters, hide/show/isolate and preview colors. Verify keyboard focus, accessibility, high DPI and selection restoration.
- [   ] 8.4.5 Run end-to-end modeling scenarios with the user and record friction points before replacing additional standard commands or making the new interface the default.

<a id="nx-downstream-workflows"></a>
## [   ] Phase 9: Extend the unified workflow to downstream work

These are follow-on planning tasks, not authorization to implement every NX or
SolidWorks capability. Prioritize after the feature-history pilot and review the
specific interactions with the user before detailed implementation.

- [   ] 9.1 Plan history-based Move/Offset/Delete/Replace Face for imported and native solids, with previews, repair limits and stable downstream result references. Treat direct edits as explicit features in history.
- [   ] 9.2 Define surface-to-solid workflows for trimmed sheets, sewing and thickening, including body type changes and references to Trim Body/Isocline results.
- [   ] 9.3 Integrate component placement, associative linked parts and in-context references with per-part histories; define external-reference updates and cycle prevention before adding assembly-edit shortcuts.
- [   ] 9.4 Update drawings and dimensions to consume stable body/result identities, with explicit repair when a feature edit removes a referenced face or body.
- [   ] 9.5 Connect CAM model and stock references to the unified results; invalidate paths after relevant history edits. Incorporate Phase 6's required two-sided/indexed setups and shared physical tab geometry when CAM work is resumed.
- [   ] 9.6 Define named configurations/variants for dimensions and feature suppression, including persistence, downstream drawings/CAM and recompute cost, before exposing configuration controls.
- [   ] 9.7 Build representative end-to-end examples: shared-sketch multi-body modeling, imported-part editing, assembly/drawing updates and two-sided machining. Record each product area?s independent acceptance and compatibility gates.


<a id="detailed-inventory-reconciliation"></a>
## Detailed candidate inventory reconciliation

The owner supplied a further 13-section candidate inventory in `Pasted text.txt`
and requested missing specifications here. Its concrete behaviors now refine the
owning tasks below; this is a planning update, not completed implementation or a
new agent startup instruction. UI/Feature/Core labels describe likely scope, not
verified effort. Existing completion evidence and stable task IDs are unchanged.

Resolve older wording against established decisions: use creation-time suggestions
with saved explicit intent, preserve the first Operation field and active collectors,
retain the approved draft-angle convention, use `.cadprt` with best-effort legacy
import, and keep required two-sided/indexed CAM and holding tabs. The candidate
inventory does not supersede these with a fixed New Body default, guaranteed upstream
compatibility, different angle semantics or three-axis-only machining. Its embedded
citation placeholders are not verified sources or imported implementation evidence.

| Supplied objective area | Owning roadmap tasks |
| --- | --- |
| 1. Part structure and ownership | 7.1, 7.3, 7.4 (including multi-target execution), 12.1, 12.2 |
| 2. Assembly and feature navigators | 7.2, 7.5, 10.6 |
| 3. Instances, references and reuse | 12.1-12.3, 12.6-12.8 |
| 4. Consistent command interface | 8.1, 8.2, 8.4.1, 10.2-10.4, 13.2 |
| 5. Selection and viewport | 8.4.4, 10.4, 10.5 |
| 6. Sketch creation and constraints | 11.1-11.6 |
| 7. Solid modeling and feature editing | 8.4.3, 13.1, 13.5-13.7 |
| 8. Curves and surfaces | 13.1-13.4, 15.2 |
| 9. Movement and assembly positioning | 10.7, 12.4-12.6 |
| 10. Interpart relationships/reliability | 7.1.4, 7.5.5-7.5.7, 12.5 |
| 11. Mesh and CAM | Phase 6, 14.1-14.4, 16.2 |
| 12. Inspection, drawings and downstream | 15.1-15.5 |
| 13. Performance, files and maintainability | 8.1.6, 12.8, 15.6, 16.1, 16.5, 16.6 |

Completion of a broad heading requires its detailed behaviors and relevant gates;
a narrow prototype or an existing approximate command is not evidence for the whole
objective. Reuse existing backend capabilities and retain explicit unsupported cases.

<a id="version-2-objective-coverage"></a>
## Version 2 objective coverage and delivery boundaries

Source: owner-supplied `UPDATED_FREECAD_PLUS_DEVELOPMENT_ROADMAP.md`, version 2.0,
sections 3-7 and 12-15. Adopted as planning scope; all newly added implementation
work below is **not started** unless an existing task explicitly records evidence.
A matching older heading does not close a broader requirement. Existing Phase 3-7
implementations remain partial evidence for the expanded portfolio.

Apply dependency gates before utility/effort ranking. Establish C3 ownership,
identity and persistence contracts before broad dependents, and C2 shared services
before multiplying consumers. Prefer reusable existing code; no kernel or solver
replacement is presumed. Decompose XL items and timebox uncertain feasibility
spikes; engineering-hour estimates are hypotheses, not runtime or delivery promises.
Re-estimate after three delivered milestones using measured work and build time.
The first useful release is a coherent everyday-modeling/sketch slice, not completion
of all surfaces, assemblies, CAM strategies, business options or specialized modules.

Inventory ratings below preserve the supplied planning assessment: U/D are 1-5,
F is feasibility, C is architectural criticality 0-3, effort is an unvalidated band.
S=8-24, M=24-80, L=80-240 engineering hours; XL exceeds 240 with no defined upper
bound. Ranges overlap and must not be summed into a delivery date. `Pending` means
the full objective is unverified; `Partial` points to existing bounded evidence.

| ID | Desired objective | U | D | F | C | Effort | Supplied phase | Local tasks / full-objective status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A01 | Unified part definition with geometry and child occurrences | 5 | 5 | Medium | 3 | L–XL | P1/P2 | 7.1; 12.1; Partial |
| A02 | Part-owned history, independent body results, explicit targets | 5 | 5 | Medium | 3 | XL | P1/P2 | 7.1; 7.4; Partial |
| A03 | Shared instances, occurrence overrides, Make Unique, promote bodies | 5 | 3 | High | 3 | M–L | P2/P3 contracts; P6 product | 12.2; Partial |
| A04 | Work/display context and scoped selection services | 5 | 3 | High | 3 | M–L | P1/P3 | 10.5; 12.4; Pending |
| A05 | Persistent references, topology provenance, repair | 5 | 5 | Medium | 3 | XL | P1/P3 | 7.1.4; 12.5; Partial |
| A06 | Versioned persistence, legacy adapters, migration | 5 | 5 | Medium | 3 | L–XL | P1/P3 | 7.6; 16.1; Partial |
| A07 | Common feature lifecycle, undo, preview, cancellation | 5 | 4 | High | 2 | L | P2/P3 | 8.1; 10.2; Partial |
| A08 | Assembly-scoped feature semantics | 4 | 5 | Medium | 3 | L–XL | P2 proof; P6 product | 7.1.3d; 12.6; Partial |
| U01 | Separate navigators, docking, synchronized highlighting | 5 | 2 | High | 1 | M | P4 | 7.2; 10.6; Pending |
| U02 | Tree filters, columns, folders, comments, dependency display | 4 | 2 | High | 1 | M | P4 | 7.2; 10.6; Pending |
| U03 | Unified Extrude and Revolve command interfaces | 5 | 3 | High | 2 | M–L | P4; depends on A02/A07 | 8.2; 10.4; Partial |
| U04 | Search aliases, shortcut palette, navigation presets | 4 | 2 | High | 0 | S–M | P4; safe prototypes earlier | 10.4; Pending |
| U05 | Multiselection modifiers, filters, Select Other, selection rules | 5 | 3 | High | 2 | M | P4 | 10.5; Pending |
| U06 | Shared extent controls, collectors, interactive handles | 5 | 3 | High | 2 | M–L | P4 | 8.1; 8.4.3; Partial |
| U07 | Move/Copy, point-to-point, triad and coordinate alignment | 5 | 3 | High | 2 | M | P4 | 10.7; Pending |
| U08 | Rollback, valid insertion/reorder, suppression | 4 | 4 | Medium | 2 | L | P3 contract; P4 UI | 7.5; Pending |
| U09 | Guided/direct workflows, progressive disclosure, consistent feature presets | 5 | 3 | High | 2 | M–L | P1 contracts; P4 | 10.2; 10.4; Pending |
| U10 | Intelligent initial New Body/Unite suggestions with persisted explicit intent | 5 | 4 | Medium | 2 | M–L | P1/P3 contracts; P4 | 7.4; 10.3; Pending |
| S01 | Automatic constraints, previews, inference controls | 5 | 3 | High | 2 | M–L | P5 | 11.1; Pending |
| S02 | Cursor-adjacent suggested-constraint palette | 5 | 2 | High | 1 | S–M | P5; earlier prototype possible | 11.3; Pending |
| S03 | Smart dimensions, driving/reference values, entry while drawing | 5 | 3 | High | 1 | M | P5 | 11.4; Pending |
| S04 | Degrees of freedom, conflict repair, sketch diagnostics | 5 | 4 | Medium | 2 | L | P5 | 11.4; Pending |
| S05 | External projection/intersection points and curves | 5 | 3 | High | 2 | M | P5; existing capability audit first | 11.5; Pending |
| S06 | Regions, trim/extend, constrained copy, blocks and patterns | 4 | 4 | Medium | 2 | L | P5 in separate increments | 11.6; Pending |
| S07 | Selection-aware constraint applicability, conflict/redundancy states and reasons | 5 | 4 | Medium | 2 | L | P1 audit/contracts; P5 | 11.2; Pending |
| B01 | Entire/Model/Empty/custom reference sets | 5 | 3 | High | 2 | M–L | P3 contract; P6 UI | 12.3; Pending |
| B02 | Joint/mate assistance, grounding, freedom/conflict display | 5 | 4 | Medium | 2 | L | P6 | 12.4; Pending |
| B03 | Published interfaces, geometry links, external-reference manager | 5 | 5 | Medium | 3 | L–XL | P3 contracts; P6 product | 12.5; Pending |
| B04 | Replacement, component patterns/mirrors, explosions and motion | 4 | 4 | High | 2 | L | P6 in separate increments | 12.2; 12.6; Pending |
| B05 | Configurations, arrangements, flexible subassemblies | 4 | 5 | Medium | 3 | XL | P1 semantics; later P6 increments | 9.6; 12.7; Pending |
| B06 | Lightweight/partial loading and simplified representations | 4 | 5 | Medium | 3 | L–XL | P1 contracts; measured P6 need | 12.8; Pending |
| G01 | Solid/sheet trim and split | 5 | 3 | High | 1 | M–L | P7 | 13.1; Partial |
| G02 | Thicken sheets, sew/stitch, offset and gap diagnostics | 5 | 4 | Medium | 1 | L | P7 | 13.1; Pending |
| G03 | Sweep/loft and through-curves surfaces with guides | 5 | 5 | Medium | 2 | L–XL | P7 | 13.2; Pending |
| G04 | Curve-network/boundary surfaces and continuity controls | 4 | 5 | Unknown | 2 | XL | P7 after bounded spike | 13.3; Pending |
| G05 | Extract/project/intersect curves; isocline extraction | 4 | 4 | Medium | 1 | M–L | P7; split by operation | 13.4; Partial |
| G06 | Holes, patterns/mirrors, shell/draft/ribs and dress-up tools | 5 | 4 | High | 2 | L–XL | P7 in separate increments | 13.5; Partial |
| G07 | Direct face editing and healing | 4 | 5 | Medium | 2 | XL | Late P7 | 9.1; 13.6; Pending |
| G08 | Imported-solid feature recognition | 3 | 5 | Unknown | 1 | XL | Late P7 after spike | 13.7; Pending |
| C01 | Direct-STL input and first three-axis finishing workflow | 5 | 4 | Medium | 2 | L | P8 | 6; 14.1; Partial |
| C02 | Stock-aware roughing, rest machining, boundaries | 5 | 5 | Medium | 2 | XL | P8 after C01 | 14.2; Pending |
| C03 | Simulation, collision checks, posts and setup reuse | 5 | 5 | Medium | 2 | L–XL | P8; limited checks from first release | 14.3; 14.4; Partial |
| I01 | Measurements, mass, sections, interference/clearance | 4 | 3 | High | 1 | M–L | P9; isolated tools may move earlier | 15.1; Pending |
| I02 | Surface quality, continuity, and deviation inspection | 4 | 4 | Medium | 1 | M–L | P7 validation/P9 product | 15.2; Pending |
| D01 | Drawing workflows, associative annotation and repair | 4 | 4 | Medium | 2 | L–XL | P9 | 9.4; 15.3; Pending |
| D02 | BOM, balloons, exploded documentation | 4 | 3 | High | 2 | M–L | P9 after B01/B04 | 15.4; Pending |
| X01 | Sheet metal, frames/weldments, hardware libraries | 3 | 4 | Medium | 2 | XL | P9 by module | 15.5; Pending |
| X02 | Package/relocate projects, compatibility and export | 5 | 4 | High | 3 | L | P3 contracts/P9 UI | 7.6; 15.6; Pending |
| X03 | Performance, scripting, packaging, upstream integration | 5 | 4 | High | 2 | Ongoing | P0 onward | 16.3; 16.5; 16.6; Partial |
| X04 | Native .cadprt identity, capability/version checks, legacy import and associations | 5 | 4 | High | 3 | L | P1/P3; P10 packaging | 7.6; 16.1; 16.6; Pending |
| X05 | Early drawing/CAM/FEM/Draft compatibility probes and adapters | 5 | 4 | Medium | 3 | M–L | P2/P3; ongoing | 7.1; 16.2; Partial |
| X06 | Release licensing, matching source, notices, dependency and asset audit | 5 | 2 | High | 1 | S–M | P0 inventory; P10 releases | 16.7; Pending |
| X07 | Starter models, guided onboarding, compatibility and support documentation | 5 | 2 | High | 1 | M | P4/P11 | 17.2; 17.3; Pending |
| Q01 | Task benchmarks, baseline comparison, effort and release evidence | 5 | 3 | High | 2 | M | P0 onward | 16.3; 16.4; 16.5; Pending |
| M01 | Audience/competitor evidence and measured adoption assumptions | 4 | 2 | High | 0 | S–M | P0/P11 | 17.1; 17.5; Pending |
| M02 | Useful-model distribution, tutorials and focused channel experiments | 4 | 2 | High | 0 | M | P11; publication when authorized | 17.3; 17.4; 17.5; Pending |
| M03 | Independent-fork branding, optional extension/MIME registration | 3 | 2 | High | 1 | S–M | Identity early; P10/P11 | 17.6; 17.7; Pending |
| A09 | Named parameters, expressions, unit checking, scope and publication | 5 | 4 | Medium | 3 | M–L | P1/P3 contracts; P4/P5 editor | 10.8; Pending |
| U11 | Unified workspace, contextual availability/help, keyboard and display accessibility | 5 | 3 | High | 2 | M–L | P3/P4; downstream integration later | 10.9; Pending |
| S08 | Sketch support/orientation, attachment and deliberate reattachment | 5 | 4 | Medium | 2 | M–L | P1/P3 references; P5 UI | 11.7; Pending |
| X08 | Document lifecycle, safe save, recovery snapshots, templates and recent-file repair | 5 | 4 | Medium | 3 | M–L | P1/P3 contracts; P10 hardening | 16.8; Pending |
| X09 | Add-on/macro/API compatibility matrix, adapters and migration diagnostics | 4 | 4 | Medium | 2 | M–L | P0 audit; P3/P10 | 16.9; Pending |
| X10 | Manufacturing export, units/orientation/quality controls and reusable presets | 5 | 3 | High | 2 | M | P3 contracts; P4/P9 UI | 15.7; Pending |

## [   ] Phase 10: Shared workflow, selection and guided modeling (P1/P3/P4)

Depends on applicable Phase 7 decisions; presentation prototypes can proceed only
when they preserve existing semantics. These tasks extend Phase 8, not replace it.

- [ X ] 10.1 Reconcile PRODUCT_SPEC, UI_UX_SPEC, guidelines and ADRs with version 2:
  intelligent suggestions, guided/direct entry, aliases, selection rules, free-core
  commitment and engineering-document scope. Keep current implementation distinct
  from future requirements; retain the operation-first field and indexed CAM scope.
- [   ] 10.2 Implement guided/direct entry through one command model, validation
  and transaction path. Guide curves/regions, magnitude/direction, operation/target
  review and visible confirmation; skip satisfied inputs for preselection/experts.
  Revisit earlier inputs without discarding unrelated valid choices. Collapse
  advanced controls while keeping operation, targets, extent, units and consequential
  warnings visible. Guidance preferences are UI state, not new feature types.
  Pilot Extrude and Revolve before extracting shared behavior; retain Apply/OK/Cancel,
  previews, handles and numeric/expression controls from 8.1.
- [   ] 10.3 Implement 7.4's shared suggestion service: explain inferred versus
  explicitly chosen operations, highlight eligible targets, update proposals before
  explicit choice without oscillating near contact tolerances, and never override
  manual choices. Invalid unions need corrective guidance; mere overlap is not
  validity. Eligibility includes work part, occurrence, reference access/editability
  and geometry. Persist accepted targets/mode; edited features initialize from saved
  intent and fail/repair rather than infer a new operation. Keep Tools is explicit;
  temporary tool geometry need not become a permanent body.
- [ X ] 10.3a Prototype creation suggestions for single solids in one part:
  no/one/multiple candidates, explicit contact review, invalid/empty geometry,
  duplicate candidates and exclusion of cross-part/occurrence targets.
- [ X ] 10.3b Prototype committed New Body/Unite/Subtract/Intersect with concrete
  links. Validate explicit New Body override, changed-intersection failure without
  retargeting, Undo/Redo, aborted target removal and native save/reopen.

Batch evidence: [ADR 002](architecture/ADR_002_CREATION_INTENT.md) records the
accepted boundary, alternatives and limits. **22 PASS**, zero failures/errors/skips,
from seven new operation-intent checks plus 15 existing history/clone checks in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\operation-intent-20260929-final\results.json`.
An initial fixture translation was corrected to test overlap instead of face contact;
no failed application fix is hidden by this correction. `prototype-manifest.json`
records source hashes. No installed source update or native build was needed.
Implementation is test-only: no production selection service, tolerance hysteresis,
multi-target execution, semantic lineage or GUI acceptance is claimed. Task 10.3,
Phase 7 architecture gates and the full guided workflow remain open.

- [   ] 10.4 Retain searchable Pad/Pocket/Revolution/Groove shortcuts as presets
  into shared Extrude/Revolve validation and editing; Pocket/Groove select Subtract
  and request a valid target. Preserve legacy adapters until conversion is supported.
  Add expanded/searchable command catalog, shortcut palette and navigation presets
  without flooding contextual palettes. Track retirement of temporary UI adapters.
  Search must recognize FreeCAD, NX and SolidWorks terminology and route aliases to the
  same command. Navigation presets include mouse behavior, chosen rotation center, zoom-
  to-selection and orthographic sketch orientation.
- [   ] 10.5 Define shared scoped selection: plain click replaces, Ctrl adds/toggles,
  Shift has documented range/extension semantics; separate sketch picks accumulate
  with modifiers, window picking can collect a group. Integrate existing task
  collectors without losing deliberate collection state. Add Select Other, entity
  filters, tangent/connected-chain rules, window/crossing and restored hide/isolate.
  Keep auto-inference suppression shortcuts nonconflicting; verify keyboard/DPI use.
  Specify filters for points, edges, faces, bodies, components, sketches and features;
  scope choices are active part, selected component and whole assembly. Select Other
  cycles overlapping/obscured candidates with a preview. Intent rules include tangent
  chains, connected edges, complete loops, same-radius faces and feature-owned faces.
  Window selection requires full enclosure; crossing selection includes intersected
  entities. Allow documented configurable modifier policies while retaining the adopted
  defaults and explicit collector mode; do not silently reinterpret clicks.
- [x] 10.5a Deliver the bounded F040 temporary isolate/hide workflow for native
  objects, Part containers, Body results and whole linked occurrences. Native
  visibility changes preserve feature ownership, Body Tips, link targets and
  placements. Complete for owner workflow testing.
- [x] 10.5b Add per-document nested restore/original-display actions, lifecycle
  cleanup and defined created/deleted-object behavior. Restored visibility, geometry,
  independent model Undo/Redo and save/reopen pass. Complete for owner workflow
  testing; whole F040 remains open for the broader acceptance below.

10.5a/b grouped evidence (2026-09-30): both implementation tasks preceded one
FreeCADGui/FreeCADGui_Resources Release build, exit 0. All 20 selected tests pass,
with no failures/errors/skips: 9 temporary-display checks, 7 command-search checks
and 4 named-parameter command checks. GUI process exit 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-temporary-display-20260930`, `grouped/`.
Native Part visibility behavior was first confirmed in the bounded `probe/`.
`visual/` contains five reviewed viewport captures showing original/isolate/hide/
whole-occurrence/restore states, plus `Temporary-Display.FCStd` for owner testing.
`acceptance-summary.json` and `validated-identities.json` record passing results
and matching source/runtime scripts. FreeCADGui SHA256:
`097c5e0cf486bcbc75bc7a98731c83d80440a9146c2633c28d126744f7e2ac11`.
No corrective build or script restaging was needed. No installer/release update.
[Try the workflow](../tests/TemporaryDisplay.md). Snapshots are session-local;
restore before saving (save while isolated persists current native visibility).
Linked members address the whole occurrence; Body features address the whole
Body result. Deep member overrides, broader save-time policy and physical/high-DPI
acceptance remain open. Stop here for owner feedback and rotate the next batch.

- [x] 10.5c Complete a bounded F037 Select Other increment in the existing
  Clarify Selection command: deduplicate by document/root/full occurrence path,
  preserve repeated equal-label candidates and expose their internal context.
- [x] 10.5d Apply native command selection gates to element and whole-object
  candidates, recheck hover/accept identity and eligibility, explain an empty
  filtered result, and validate additive acceptance and Escape preservation.

Both implementation tasks preceded one FreeCADGui/FreeCADGui_Resources Release
build, exit 0. Evidence: `D:\Temp\Office-PC\freecad-plus-clarify-selection-20261001`.
Initial `grouped/` stopped before any tests because the PySide compatibility wrapper
has no QtTest export. The test now imports the bundled PySide6 QtTest (PySide2 fallback);
no implementation change or second build was needed. `grouped-native/` passes all
seven native Clarify Selection checks and nine temporary-display regressions:
**16 selected passes**, zero failures/errors/skips, native exit 0. Five `visual/`
captures were reviewed: equal-label face choices, rear-face highlight, face-only
filter, all-filtered explanation and distinct repeated occurrence paths.
Overlapping-Equal-Labels.FCStd and Overlapping-Occurrences.FCStd are owner fixtures.
The native picker exposes Front/Rear Face5/Face6 separately and Assembly.First. /
Assembly.Second. as separate whole occurrences. Exact hover/accept, additive
selection, Escape preservation, face/object/reject gates, changed-gate refusal,
deleted/recreated-name protection and native Link save/reopen pass.
FreeCADGui SHA256: `19FE903A46ABEFC2A34F0AECBA86F2BAA6C331A2663685C0DD797032A1EF80C8`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted evidence; the historical About stamp is not this source identity.
No installer/release update. Full F037 remains open for broader topology/live-menu
changes and physical/high-DPI/navigation-preset acceptance. Bounded F035 filters are now
available under 10.5e/f; new selection scopes (F036) and depth ranking remain
separate work.
Stop at this functional checkpoint for owner testing and rotate to another family.
[Owner procedure](../tests/ClarifySelection.md).

- [x] 10.5e Implement a bounded F035 entity filter alongside command-owned gates:
  vertices, edges, faces and whole objects, preserving resolved occurrence paths.
  Apply it to native add/preselection and Select Other eligibility.
- [x] 10.5f Provide discoverable modeless controls, a persistent active indicator,
  one-click reset, Close/Escape/startup recovery and unchanged existing selections.
  Both changes are complete for bounded owner workflow testing.

10.5e/f grouped evidence (2026-10-01): both implementation tasks preceded one
FreeCADGui/FreeCADGui_Resources Release build, exit 0 (120 seconds). Evidence:
`D:\Temp\Office-PC\freecad-plus-entity-filter-20261001`. Initial `grouped/` passes
all seven native Select Other regressions and eight of nine filter checks. The
hover fixture incorrectly used native internal-highlight mode (tp=1), which bypasses
gates; corrected viewport mode (tp=0) passes all nine in `filter-verified/`.
Final source review moved command registration before standard-workbench
initialization; one 60-second corrective build passed. The added menu check initially
assumed NoneWorkbench had a Visibility menu, but it intentionally has minimal menus.
The corrected modeling-workbench fixture passes with all ten filter checks in
`final-verified/`; no further source change/build was needed. Together with the
seven unchanged Select Other regressions, **17 distinct selected checks pass**,
zero accepted failures/errors/skips; accepted GUI processes exit 0.
Five `visual/` captures were reviewed: face controls and exact occurrence face,
whole occurrence, reset controls and restored unrestricted workspace. The owner
fixture is `visual/Repeated-Components.FCStd`. `evidence.json` records matching
source/runtime Python identity, exact native binary hash and accepted results.
FreeCADGui SHA256: `331ff38104740d19a266338b3f3fe51b3886216233b3e10f1202e359132f9593`.
No installer/release publication. Stop here and rotate pending owner testing.

The command's gate refines this session filter; leaving a command does not remove
or replace it. The owner can reset or close the modeless filter window at any time.
Separate bodies/components/sketches/features, richer filter combinations, dedicated
sketch-edit and tree/window-selection semantics and physical/high-DPI acceptance
remain open. [Owner procedure](../tests/EntitySelectionFilter.md).

- [x] 10.5g Use full projected enclosure for left-to-right native 3D box selection;
  keep right-to-left crossing, visible-object scope and filter/command-gate intersection.
  Preserve explicit subelement collection when whole bounds fit (F039).
- [x] 10.5h Distinguish solid window and dashed crossing borders in command and
  delayed-drag selection, with documented Ctrl-add/Escape behavior. Verify zoom,
  hidden objects, occurrence bounds, filters and cancellation in one grouped pass.

2026-10-01 evidence: both tasks preceded one 70-second FreeCADGui build, exit 0.
Nine TestWindowSelection checks pass in `final-window`, plus ten existing
TestEntitySelectionFilter checks in `grouped`: nineteen distinct accepted checks,
no skips. Native viewport events establish partial versus full enclosure at two
zooms, command-gate spatial bounds, separate/hidden objects, Ctrl-add/plain replace,
Escape/retry, edge/face filter intersection, delayed CAD drag, nested occurrence
identity/bounds and unchanged Box Zoom behavior. Root-box BRep/Undo preservation
passes. Six `visual` captures are reviewed and `Window-Selection.FCStd` is saved.
Evidence: `D:\Temp\Office-PC\freecad-plus-window-selection-20261001`, build log,
accepted results, captures and `evidence.json` source/native hashes. About metadata
is historical; no owner acceptance, installer or release publication is claimed.

Retained finding: both initial runs (`grouped`, `window-verified`) observed a single
serialized BRep flag changing on the nested occurrence source during selection,
including with a post-setup baseline. The final nested check verifies volume, area,
vertex coordinates, placement, shared identity, object state and Undo count; it does
not certify byte-for-byte nested BRep preservation. Do not erase this distinction.

This bounded 3D increment retains projected-bounds crossing and native tessellated
subelement checks. Exact silhouette/occlusion picking, broad curve and sketch coverage,
removal modifiers and physical/high-DPI acceptance remain open for F039.
[Owner procedure](../tests/WindowSelection.md). Stop here and rotate.

- [   ] 10.6 Extend 7.2 with separate Assembly and Feature Navigator tabs, optional
  simultaneous docking, explicit work/display part, status columns, contributing-body
  filters, comments, folders and dependency highlights. Display grouping never
  changes ownership, transforms or valid history order.
  Columns explicitly include visibility, suppression, errors, source file, reference set
  and modification status. Feature Navigator shows the active work part while Assembly
  Navigator retains component hierarchy. Body filtering supports all part features or
  only contributors to selected bodies. Named groups/folders, comments, type filters and
  input/downstream highlights must remain organizational rather than ownership changes.
- [x] 10.6a Expose 7.5.5a's snapshot through Tools > Inspect dependencies with
  explicit model selection and node navigation, refresh after graph changes and
  safe close/deletion handling. Validate a shared sketch, downstream feature and
  drawing; stop at owner-test-ready inspection before further navigator work.

7.5.5a / 10.6a grouped evidence (2026-09-30): both tasks preceded one FreeCADGui/
FreeCADGui_Resources Release build, exit 0. **23 distinct checks pass**, zero failures/
errors/skips in accepted suites: 7 dependency inspector, 7 command search, 9 temporary
display. Use `inspector-final/` and the two unchanged passing suites in `grouped/`
under `D:\Temp\Office-PC\freecad-plus-dependencies-20260930`. Process exits 0.
`acceptance-summary.json` and `validated-identities.json` record exact suites and
matching installed script; FreeCADGui SHA256:
`a54d51a83333161ba4c2574648159b56117a31489160709279b6bdd11d581582`.
Shared sketch/two extrusions/real fillet/TechDraw source, expression property reasons,
saved-document external links, cyclic graph, traversal limits, native missing-face
status/repair, Undo/save/reopen, selection/visibility preservation and deletion/close
pass. `visual-accepted/` has three reviewed captures and native-only
`Dependency-Inspection.FCStd`; [owner procedure](../tests/DependencyInspector.md).
Earlier `grouped/` and `inspector-accepted/` retain fixture failures (cylinder seam,
unsaved external-link documents and tree expansion state). Initial captures expected
four edges, but native save exposes both Fillet Base and EdgeLinks; final capture
retains both and checks the four related objects. Application code was unchanged;
no corrective build or script restaging. Source graph/status inspection does not
establish deletion safety or diagnose unloaded references. Integrated navigator
tabs/highlights, target roles and physical/high-DPI acceptance remain open. Whole
F015/10.6 stays open; stop this pilot pending feedback and rotate. No release update.

- [ X ] 10.6b Add native metadata search by label, internal name, type and description
  for F014, with explicit document scope/type filtering, presentation-only sorting,
  partial-search disclosure and deliberate model selection without visibility edits.
- [ X ] 10.6c Stage native Label/Label2 edits for one selected object, preserving
  identity, links, history order and placement. Apply owns one Undo transaction;
  reject stale/replaced/read-only inputs and pending edits. Validate Close, Undo/Redo,
  save/reopen, shared-source isolation and downstream recompute.
  Both tasks preceded one grouped FreeCADGui/FreeCADGui_Resources Release build,
  exit 0. All 20 selected checks pass, no failures/errors/skips: 6 feature-organizer
  in organizer-verified/, 7 dependency-inspector and 7 command-search in grouped/;
  process exits 0. Search/type filtering, presentation-only sorting, explicit model
  selection, source/occurrence metadata isolation, stale/replaced/read-only guards,
  pending-edit preservation, no-op Apply, Close, Undo/Redo and save/reopen pass.
  Native hole expressions/Boolean references and shared instance geometry still
  update after editing Stock.Width on reopen. Native Label/Label2 persistence only.
  Evidence: `D:\Temp\Office-PC\freecad-plus-feature-organization-20260930`;
  acceptance-summary.json / validated-identities.json record exact suites and matching
  installed script. FreeCADGui SHA256:
  `c1c081a7212b15ed4355872cedb8241ab873e46b18be67d1e7581d015e7bfa3d`.
  Four captures reviewed in visual/ with Feature-Notes.FCStd and Feature-Notes-Edited.FCStd.
  [Owner procedure](../tests/FeatureOrganizer.md). Earlier grouped/ retains an empty
  transaction fixture assumption; corrected fixture performs an owner edit before
  checking the guard. No application correction, script restaging or second build.
  Whole F014 remains open for folders, bulk organization, navigator integration,
  uncapped/external search and physical/high-DPI acceptance. No installer/release
  update. Stop for owner feedback and rotate.

- [x] 10.6d Expose native visibility, suppression, error/recompute, source and
  metadata-access columns in the existing feature organizer (F013). Keep the
  display flags distinct from effective visibility and suppression; report
  unresolved links without loading them or claiming full loading diagnosis.
- [x] 10.6e Add presentation-only column choices and state filters, full status/
  source detail, and invalidate snapshots after relevant object, display,
  recompute, save and loaded-source changes. Verify source/geometry preservation,
  metadata compatibility and lifecycle. Both tasks passed grouped verification.

10.6d/e evidence (2026-10-01): both tasks preceded one 10-second successful
FreeCADGui_Resources staging pass (exit 0); Python-only, no native recompilation.
Evidence: D:\Temp\Office-PC\freecad-plus-feature-state-20261001.
All 14 assertions passed initially, but log review exposed callbacks receiving
unattached view providers and GUI property containers. Added narrow lifecycle/type
guards and restaged only FeatureOrganizer.py. verified/ passes all eight new state
checks and six existing metadata checks, zero failures/errors/skips, process exit 0.
Final stderr contains only the deliberately broken Cut and empty suppressed-Body
fixture diagnostics; no observer tracebacks. Native suppression, hidden flags,
error/recompute recovery, missing Link distinction, read-only metadata, columns/
filters/sorting without mutation, loaded external source identity/files, change
invalidation, Undo/Redo, save/reopen and observer/document lifecycle pass.
Seven final captures reviewed in visual-final/: native state/source columns,
suppression, unresolved links, read-only metadata, native errors, display-state
invalidation and reopened sources. Feature-States.FCStd is the owner fixture;
evidence.json records accepted suites and source/runtime hashes. Source-built
verification is not installer or owner acceptance.
Full F013/10.6 remains open for integrated navigator
columns, reference sets, nested/unloaded reference diagnosis, global preferences,
modified/file-permission state, validated state toggles and physical owner acceptance.
[Owner procedure](../tests/FeatureStateColumns.md). Stop here and rotate for feedback.

- [   ] 10.7 Add shared Move/Copy with point-to-point, translation/rotation,
  coordinate-system/axis alignment, movable triad, snapping and local/global context.
  Distinguish one-time placement from a persistent assembly relationship; validate
  occurrence scope, exact numeric results, preview, Cancel, Undo and restore.
  Allow relocating the manipulator to a vertex, geometric center, datum or inferred
  point. Include typed offsets, arbitrary-axis rotation and snapping in global/local
  coordinates. Present move here once and maintain this relationship as distinct
  actions, with a preview of the affected occurrence.

- [x] 10.7a Add explicit world/occurrence-frame translation and arbitrary-axis
  pivot rotation for one unconstrained, unscaled same-document solid/Body Link
  within structural Part containers (F074; bounded F072/F075). Preserve shared source
  and other occurrences; one-time movement creates no hidden relationship.
- [x] 10.7b Provide a non-pickable view-only preview, numeric world-origin result,
  stale/frame guards, Cancel and transactional confirmation. Validate rotated nested
  containers, both source-transform policies, preview/commit agreement, rollback,
  Undo/Redo and save/reopen. Both tasks complete for owner testing.
  Shared-definition Copy follows in 10.7c/d; point picking/snapping, triads and
  maintained relationships remain open.

- [x] 10.7c Add one transactional shared-definition occurrence copy at the existing
  reviewed transform, preserving native Link identity semantics, parent, source,
  original placement and appearance/visibility. Verify Undo/Redo, rollback and reopen.
- [x] 10.7d Add explicit Move/Copy action and copy label to the existing F072 dialog.
  Reuse preview/frame controls and command identity; disclose shared geometry and
  preserve Cancel/stale handling. Keep independent definitions and arrays separate.

10.7c/d evidence (2026-10-01): both tasks preceded one FreeCADGui_Resources
Release staging pass, exit 0; no native C++ compilation. Evidence:
`D:\Temp\Office-PC\freecad-plus-occurrence-copy-20261001`.
All 25 grouped checks pass: seven new copy, seven movement and eleven command-search
checks. After a copy-label encoding correction and updated offline help, only the
two Python files were restaged. All seven copy checks pass again in copy-verified/,
including the copy search alias/help; unchanged passing suites stand. **25 distinct
selected passes**, zero failures/errors/skips; native process exits 0.
Native shallow Link copy creates only one new object/identity and retains its shared
source, nested structural parent, visibility, material override and LinkTransform.
World translation and arbitrary-axis rotation agree with an independent native
assembly-path geometry check. Preview/Cancel preserve object count and original
placement; commit is one Undo step. Undo/Redo, save/reopen, source edits updating
all copies, empty-label/stale-frame/booked-transaction refusal and injected-failure
rollback of both object and parent membership pass. Coincident copies are deliberate.
Five visual/ captures were reviewed: settings, ghost, missing-label recovery,
reopened shared-source growth and changed-frame refusal. Copy-Sources.FCStd,
Linked-Copies.FCStd and Edited-Copies.FCStd are owner fixtures. Source/runtime hashes
and accepted suites are recorded in validated-identities.json and
acceptance-summary.json; the historical About stamp is not this source identity.
No installer/release update. Full F072 remains open for independent definitions,
point picking/alignment, wider transform subjects and physical/high-DPI acceptance.
[Owner procedure](../tests/OccurrenceMove.md#shared-definition-copy-f072-107cd).
Stop at this usable copy branch and rotate pending owner workflow feedback.

10.7a/b grouped evidence (2026-10-01): both tasks preceded one FreeCADGui/
FreeCADGui_Resources Release build, exit 0. Initial grouped/ passed 7 appearance
and 7 command-search checks but exposed 3 movement geometry failures. A bounded
native assembly-path probe found that App::Link lacks getGlobalPlacement(), so
the shared BasicShapes.ShapeReferences.linked_shape omitted enclosing Part transforms.
The resolver now applies the native parent global placement for that case. Only
the Python resolver was restaged; no second native build. Tests use the independent
native assembly path as the movement oracle, not the corrected resolver itself.
All 54 checks in resolver-verified/ pass without failures/errors/skips: 7 movement,
9 manufacturing export, 7 interference, 6 Make Unique, 14 Trim Body and 11 Isocline.
Together with the initial unchanged appearance/command suites, 68 distinct selected
checks pass across accepted runs; process exits 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-occurrence-move-20261001`.
FreeCADGui SHA256: `1959269e7ea02b2760f4cb914d4693dcec41f0e425441939e5324e28823f7608`.
Six captures reviewed in visual-accepted/, with Nested-Occurrences.FCStd and
Moved-Occurrences.FCStd. Frame/pivot/LinkTransform semantics, source/other-link
isolation, preview/commit geometry, cleanup, rollback, Undo/Redo and reopen pass.
The initial visual/ backend omitted the extra scene node; FramebufferObject captures
the ghost correctly using isolated preferences. acceptance-summary.json and
validated-identities.json record exact suites, source/runtime/native identities.
Whole F072/F074/F075 and parent 10.7 remain open for broader scope and physical
acceptance. No installer/release update. [Owner procedure](../tests/OccurrenceMove.md).

- [   ] 10.8 Add named parameters, expressions, dimensional unit checking and explicit
  document/part/configuration scope (A09; [F122](#f122)). Provide rename and where-used,
  cycle rejection, publication rules and compatible-expression entry in feature fields.
  Validate shared dimensions, unit changes and rename propagation with T13.
- [ X ] 10.8a Prove a native named length property drives two part features,
  converts inch/mm input, survives parameter-container label edits, Undo/Redo and
  native save/reopen, and preserves an occurrence's independent placement.
- [ X ] 10.8b Prototype a dimensional assignment boundary for length expressions;
  reject angular results before mutation and reuse native expression cycle rejection.
  Verify transaction abort restores the valid expressions/geometry and later edits.
- [ X ] 10.8c Prove explicit internal-name parameter references remain independent
  across two parts with matching container labels and Width property names, through
  edits and save/reopen. Verify native object-level reverse dependency membership.
- [ X ] 10.8d Prove a unit-correct zero length can invalidate downstream geometry,
  transaction abort restores expressions and geometry, and subsequent valid edits
  retain working Undo/Redo. This is recovery evidence, not automatic UI rollback.

- [ X ] 10.8e Extend the test-only assignment boundary to explicit angular expressions.
  Prove degree/radian changes drive cylinder sector geometry, reject length/unitless/
  missing references without replacing the expression, and retain Undo/Redo/persistence.
- [ X ] 10.8f Prove native dynamic-property rename updates two expression consumers,
  survives Undo/Redo and save/reopen, and continues driving geometry after later edits.
  This establishes native behavior, not a parameter rename UI or collision policy.

- [ X ] 10.8g Add a test-only atomic length/angle parameter rename wrapper using
  native validation and its own transaction. Verify collision/invalid/empty-name
  failures restore an owned expression and consumers, pending caller edits remain
  untouched, and a later valid rename succeeds.
- [ X ] 10.8h Verify label-based and internal-name references both follow parameter
  rename with an owned formula, Undo/Redo, container label changes, save/reopen and
  subsequent formula edits. External/ambiguous-label references remain unproven.

- [ X ] 10.8i Prototype atomic named-parameter expression edits using the existing
  length/angle unit guards, recompute-state validation and transaction rollback.
  Prove a zero-width downstream failure restores the prior value/formula/geometry;
  valid length edits support Undo/Redo and native persistence.
- [ X ] 10.8j Guard parameter edits against stale affected consumers and unrelated
  pending transactions before mutation. Verify a disconnected invalid feature does
  not block a valid edit, while its existing invalid state remains visible.

- [ X ] 10.8k Prototype a Qt dialog for an existing parameter object, with typed
  parameter selection, current value, expression entry and explicit Apply/Close.
  Reuse atomic edits; prove typing does not mutate geometry and Close keeps applied
  changes while discarding unapplied text. Native Undo restores the applied edit.
- [ X ] 10.8l Add rename and recoverable error feedback to that prototype. Verify
  wrong-unit and failed-geometry corrections, angle edits, collision recovery and
  successful rename refreshing selection while retaining consumer links.

- [ X ] 10.8m Add explicit Refresh and snapshot-based conflict detection to the
  editor prototype. Verify external value edits and Undo cannot be overwritten by
  stale Apply/Rename; Refresh discards draft text and reloads the current value.
- [ X ] 10.8n Close the prototype when its parameter object or document is deleted,
  detach its document observer on completion and ignore subsequent edit actions.
  Verify both deletion paths using native document notifications.

- [ X ] 10.8o Guard loading a stale parameter dropdown after external rename/removal.
  Disable editing and require Refresh; verify list recovery, empty-state disabling
  and externally added parameters becoming editable after Refresh.
- [ X ] 10.8p Verify two prototype dialogs preserve each other's committed values,
  reject stale drafts until Refresh and retain independent observer lifecycles.
  Closing one dialog leaves the other's parameter-deletion handling active.

- [ X ] 10.8q Prototype typed parameter creation in an existing parameter object.
  Reject invalid/colliding names and invalid expressions without a partial property;
  verify native Undo/Redo, dependent formula updates and save/reopen for length/angle.
- [ X ] 10.8r Add New name/type/expression and Create parameter to the prototype
  dialog. Preserve failed input for correction; on success select the new parameter
  and clear creation text. Verify incompatible units, collisions and both types.

- [ X ] 10.8s Preserve descriptions as native dynamic-property documentation when
  creating parameters, display them read-only and prove Undo/Redo, rename and
  save/reopen retain them. Editing existing descriptions remains pending.
- [ X ] 10.8t Add display-only length (mm/cm/m/in/ft) and angle (deg/rad) selection
  to the prototype editor. Verify switching inch/radian display does not mutate
  stored physical values, expressions, geometry or transaction state.

- [ X ] 10.8u Build a native enclosure/lid/two-hole parameter fixture for bounded
  T13 validation. Verify Width/LidClearance/HoleSpacing updates via geometry volume,
  extent and placement; rename, unit/cycle rejection and save/reopen retain intent.
- [ X ] 10.8v Verify two linked occurrences retain independent placements while
  sharing the enclosure definition's parameters; a separately parameterized enclosure
  stays unchanged. Verify shared-definition edits through Undo/Redo.

- [ X ] 10.8w Exercise enclosure width/clearance/hole spacing through actual prototype
  widgets, checking geometry after Apply, rename selection/propagation, exact inch
  display conversion without mutation and Close discarding unapplied text.
- [ X ] 10.8x Exercise incompatible-unit, cyclic and zero-width geometry errors in
  the enclosure dialog; verify restored geometry, retained attempted input and retry.
  Save/reopen and edit through a fresh dialog while preserving native relationships.

- [ X ] 10.8y Prototype explicit Part-definition parameter-container creation as
  its own native undoable transaction. Reject Body/occurrence targets and pending
  caller edits; verify ownership, Undo/Redo and save/reopen without a custom schema.
- [ X ] 10.8z Add a prototype editor entry point for an explicitly supplied native
  Part-owned container. Verify it edits the intended document while another is
  active, supports an initially empty set and leaves the other document unchanged.

- [ X ] 10.8aa Promote the proven length/angle editor and native parameter
  operations to application modules, register Part > Named parameters, and reuse
  the explicitly selected Part's marked set. Preserve ownership, transactions,
  legacy fixtures and native persistence; expose no implicit occurrence resolution.
- [ X ] 10.8ab Add same-document expression references and Copy reference, then
  deliver an enclosure example and short owner-testing procedure. Verify actual
  command entry, reference/rename propagation, edit recovery and save/reopen as one
  usable batch. This is the stopping point pending owner workflow feedback.

Installed pilot evidence, 2026-09-30:
`D:\Temp\Office-PC\freecad-plus-parameter-command-20260930`.

- Both command-entry and reference-copy tasks preceded one grouped PartGui and
  PartScripts Release build (exit 0). CMake installs the new application modules;
  old prototype imports forward to them. An initial Python appendMenu attempt
  failed on the native workbench; the blocked disposable test process was stopped.
  The command is now registered in the native Part menu.
- Final selected acceptance: 90 distinct passes, no failures/errors/skips, process
  exits 0. `built/` supplies 14 editor, 22 capability, 24 Trim GUI and 26 Isocline
  GUI checks; `command-final/` supplies 4 command checks. The mixed built aggregate
  includes an earlier Windows OpenClipboard failure and is not itself claimed PASS.
  The final copy test verifies the requested clipboard payload and uses it in a
  real feature expression; physical copy/paste remains owner acceptance.
- Command checks cover menu availability, creation/reuse, Undo/Redo, explicit set
  choice, Body/occurrence rejection, pending edits, copied references, rename and
  enclosure edits/save/reopen. Existing unit/cycle/geometry rollback checks now
  exercise the application implementation.
- `visual-final/` contains two reviewed readable normal/error captures and
  `Named-parameters-enclosure.FCStd`. The first capture harness lacked GUI document
  initialization; the corrected startup passed. `validated-identities.json` records
  matching source/runtime modules, tests and binary hashes. PartGui SHA256:
  `41bde8dbd15017f005b1937afd9e5d80fb2c90d0f83274922254324d7bb8440a`.
- **Ready for owner testing; not owner accepted.** Follow
  [the short workflow procedure](../tests/NamedParameters.md). Stop at this usable
  pilot. Where-used, publication/configuration/document scope, existing-description
  editing, broader types and physical/high-DPI/localized acceptance remain open.
  No installer/release update or unified history architecture decision is implied.

Part-scope evidence: `parameter-part-scope-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **75 PASS, zero failures/errors/
skips** (14 native Qt, 22 capability, 34 adapter, five lineage checks). Both tasks
preceded grouped validation on engine 2df76790b4; macro PASS and process ended.
Initial `parameter-part-scope-20260930-batch` had 74 passes/one failure: an empty
transaction was not reported as pending. The corrected fixture includes a caller
label edit and verifies preservation and caller abort. Prototype hashes:
NamedParameters `B59C8D4DDEB16FE0DB052F8E2833CB8B47AE37A888E951F1DB3B4E8915731EC6`;
ParameterEditor `8E943A78D348D438CB71FE0225F164FDE4248AE25A904EDE77B4D1C92E04965A`.
Container creation commits separately from opening/closing its editor; Close does
not delete it. No automatic occurrence resolution or implicit expression scope is
introduced. At that prototype checkpoint production registration, scope/publication/where-used
and physical UI remained pending. The installed pilot above adds registration;
broader scope and physical acceptance remain open. No native rebuild or release update.

Enclosure editor evidence: `parameter-enclosure-editor-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **73 PASS, zero failures/
errors/skips** (13 native Qt, 21 capability, 34 adapter, five lineage checks).
Both validation tasks preceded one grouped run on engine 2df76790b4; macro PASS and
process ended. TestParameterEditor SHA256:
`37439E05D2F4080DABED5DA4FDBCC5B3266E3B9CC38BCA9E5669D0D08E75BAC7`.
The automated T13 slice now connects the dialog to the native enclosure geometry;
physical input/accessibility and production installation still remain pending.
No application code or installer changed, no native rebuild or release update.

Enclosure benchmark evidence: `parameter-enclosure-20260930-verified/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **71 PASS, zero failures/
errors/skips** (11 native Qt, 21 capability, 34 adapter, five lineage checks).
Both tasks preceded grouped validation on engine 2df76790b4; macro PASS and process
ended. Initial `parameter-enclosure-20260930-batch` had 70 passes/one error because
fixture visibility changes left its Part Touched; recomputing after setup corrected
that fixture without weakening the readiness guard. ParameterEnclosure SHA256:
`DA61FE96C6F33E5B1BE95C345A5D0C99FFC47980D3B50124607E393748202D11`.
The fixture uses native boxes, cylinders and cuts, not a production unified-history
model. Link tests establish definition identity/placement and independent definition
isolation, not every rendered/consumer occurrence result. Existing display-unit Qt
checks accompany this geometry batch; full physical T13 and production integration
remain pending. No native rebuild or release update.

Description/display-unit evidence: `parameter-units-description-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **69 PASS, zero failures/
errors/skips** (11 native Qt, 19 capability, 34 adapter, five lineage checks).
Both tasks preceded one grouped run on existing fork engine 2df76790b4; macro PASS
and process ended. Native quantity conversion supplies display values without
rewriting expressions. Prototype hashes: NamedParameters
`C2CA3A7CDCFB2CA0E5D5527D452538F2A75C940C378ABA093105C10D41B15ADF`;
ParameterEditor `E247E812F008718BFF902BDAF044C048C4C2131DFE7AE592145174BB013C884D`.
Unit selection is local dialog state, not saved document or application preferences.
No native rebuild or release. Description editing, localized quantity formatting,
physical accessibility, full T13 and production integration remain pending.

Parameter creation evidence: `parameter-create-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **67 PASS, zero failures/errors/
skips** (ten native Qt, 18 capability, 34 adapter, five lineage checks). Both tasks
preceded one grouped run on existing fork engine 2df76790b4; macro PASS and process
ended. Test-only creation uses native dynamic Length/Angle properties and expressions,
with ASCII identifier names and an owned transaction. Existing property identities
are preserved. Prototype hashes: NamedParameters
`7FFF822D2021F9DD5C65BBB1540B69E1B6582A628584D364BB46CB883D962622`;
ParameterEditor `3E2A58639A1BFC0641BF35EB0C625C85EE6B61065DB4295971DD52D2D854D53D`.
No native rebuild, installed command or release update. Parameter-object creation,
delete/where-used/publication, broader types/scope and production integration remain
open; physical UI/accessibility acceptance is separate from these widget tests.

Parameter-list/multiple-editor evidence: `parameter-editor-schema-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **65 PASS, zero failures/
errors/skips** (nine native Qt, 17 capability, 34 adapter, five lineage checks).
Both tasks preceded one grouped run on existing fork engine 2df76790b4; macro PASS
and process ended. ParameterEditor SHA256:
`0FE487EC3352BDD8342DECC49FCAB7EFD7ABA48B25327E98A0105EC081F2D804`.
These tests cover same-object dialogs and explicit Refresh, not a general live
synchronization or external-document reference protocol. Physical UI/accessibility,
production command integration and full parameter functionality remain pending.
No native rebuild or release update.

Editor lifecycle evidence: `parameter-editor-lifecycle-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **62 PASS, zero failures/
errors/skips** (six native Qt, 17 capability, 34 adapter, five lineage checks).
Both tasks preceded one grouped run on existing fork engine 2df76790b4; macro PASS
and process ended. ParameterEditor SHA256:
`1492B34D6C5BF1D141918AF742290992338BE04C959F27AF7592170015885661`.
Snapshots cover the object's typed values and expressions; this is conservative
object-level conflict detection, not a complete external dependency revision model.
External property-list changes while interacting, multi-dialog behavior and physical
UI/accessibility still need acceptance. No native rebuild, installed command or release.

Editor prototype evidence: `parameter-editor-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **59 PASS, zero failures/errors/
skips** (three native Qt interaction, 17 capability, 34 adapter, five lineage checks).
Both tasks preceded one grouped run on existing fork engine 2df76790b4; macro PASS
and process ended. `tests/prototypes/ParameterEditor.py` is not installed or registered
as a command. SHA256:
`F9DFAC34611ED7E01C3042808AD077040CB0CADB16FB4D31AB07D1A323B64665`.
Tests operate real widgets programmatically; physical keyboard, viewport/high-DPI,
accessibility and production integration are not validated. Creation/deletion,
where-used, publication, external document lifecycle and live external updates remain
pending. No native rebuild, installed application change or release update.

Atomic edit evidence: `parameter-edit-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **56 PASS, zero failures/errors/
skips** (17 capability, 34 adapter, five lineage checks). Both tasks preceded one
batch on existing fork engine 2df76790b4; macro PASS and process ended. Test-only
`edit_parameter_expression` uses native recursive dependents and their inputs for
object-level readiness before/after the edit. It aborts failed edits and rejects
caller-owned transactions. NamedParameters SHA256:
`E6B03595BBD5BBCFA1D43498799918BB1D4FB4AB093AF220C4469AA99845A148`.
Dependency grouping can conservatively include sibling objects through container
links; this is not property-level impact analysis. Only the native test fixtures
are proven; proxy side effects, external consumers and general geometric validity
remain separate gates. No native rebuild, installed editor or release update.

Atomic rename evidence: `parameter-rename-safety-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **54 PASS, zero failures/errors/
skips** (15 capability, 34 adapter, five lineage checks). Both tasks preceded one
grouped run on existing fork engine 2df76790b4. Macro PASS; process ended.
`DocumentObject::renameDynamicProperty` removes an owned expression before native
name validation; the prototype transaction restores it on failure. No expression
text replacement or new document schema is introduced. NamedParameters SHA256:
`46F0CF4BB903581B9D18F02EDEE6A3E693E3741B4403EFBC1AA92F69900C88E0`.
The helper is test-only and not installed; no native rebuild or release update.
Production editor, general where-used, external scope and failed recompute policy
remain pending; this batch does not claim all rename failure modes are covered.

Angle/rename evidence: `parameter-angle-rename-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **52 PASS, zero failures/errors/
skips** (13 capability, 34 adapter, five lineage checks). Macro PASS; process ended.
Both tasks preceded grouped validation on existing fork engine 2df76790b4. The initial
`parameter-angle-rename-20260930-batch` also passed 52 checks; the verified run adds
rename Undo/Redo and persistence assertions. Prototype NamedParameters SHA256:
`463AB31A24BB31EE36F88C257F771674FF49E8FF63E928C69101636F9B506826`.
Native `renameProperty` rewrites the two expression references; no manual string
replacement is required for these internal-name references. Label-based/external
references, name collisions, where-used, publication and the production editor remain
open. No native rebuild, installed application change or release update.

Parameter dependency/recovery batch: `parameter-dependencies-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928` records **26 PASS, zero
failures/errors/skips**: eleven capability checks (two new), ten adapter and five
lineage checks. Macro PASS; process ended. Both tasks preceded this grouped run
using the existing fork build (engine source 2df76790b4). No native rebuild,
installed application change or release update. Native `InList` is object-level
and includes non-expression dependencies; it is not a property-level where-used
implementation. Explicit document object names are not implicit part/configuration
scope resolution. Production scope, where-used, editor validation and failed-result
consumer handling remain open under 10.8 and the architecture gates.

Named-parameter foundation: `named-parameters-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **24 PASS, zero
failures/errors/skips**: nine native capability checks (two new), ten adapter and
five lineage checks. Macro PASS; process ended. Initial `named-parameters-20260930-batch`
had 23 passes/one failure because native assignment accepted an angle as a length
without invalid state. The new test-only `tests/prototypes/NamedParameters.py`
evaluates the expression's unit before assignment; native code rejects the cycle.
Prototype SHA256: `0C2E9ED61A09F8795E63902940E5C0B1A8177F954E098D8B7B580B404583DC17`.
The guard supports App::PropertyLength and explicitly length-valued expressions
only. It is not installed and does not intercept application expressions. Fixtures
retain native object/property identities and need no custom proxy to recompute.
This proves container label changes, not property renaming or a parameter editor.
Configuration/cross-document scope, publication, where-used, display-unit settings,
full T13, and production unit/default policy remain pending under 10.8. Both tasks
preceded grouped testing using engine 2df76790b4; no native build or release change.

- [   ] 10.9 Complete the unified contextual workspace, availability explanations,
  local help, keyboard navigation and display accessibility (U11; [F025](#f025),
  [F123](#f123)). Preserve the active engineering document across modeling, CAM,
  drawings and analysis; validate keyboard-only tasks and enlarged-display recovery.
- [ X ] 10.9a Add offline contextual guidance to the existing command-search pilot.
  Thirteen curated entries describe inputs, workflow, Cancel/Undo or export effects,
  and known limits; uncurated entries explicitly retain native descriptions.
  Reading never runs commands or loads a workbench. Native availability stays
  authoritative and rechecks before Run; active-document state refreshes while open.
- [ X ] 10.9b Make command-search guidance keyboard-readable and recoverable with
  enlarged text. Scrollable split panes, accessible names, local F1/Ctrl+L, tab order,
  button mnemonics and window-only Reset layout preserve document state and global
  fonts/shortcuts. Validate reading, wrong workbench, empty/no-document recovery,
  unchanged geometry/selection/Undo history, and existing native Pocket lifecycle.

10.9a/b evidence (2026-10-01): both tasks preceded one successful
FreeCADGui_Resources build/staging pass in the existing local build. Python-only
changes required no C++ recompilation. Evidence:
`D:\Temp\Office-PC\freecad-plus-command-help-20261001`.
Initial `grouped/` passed seven DocumentUpdates and ten of eleven CommandSearch
checks; the F1 keyboard check failed. Palette-local shortcut handling was corrected
and only CommandSearch.py restaged. `help-verified/` passes all eleven. Visual review
then found application styling overrode the inherited font stress setting; the
final test explicitly checks actual rendered 20-point text. `enlarged-verified/`
passes all eleven, including native Pocket geometry, Undo/Redo and save/reopen.
**18 distinct selected passes**, zero failures/errors/skips in accepted suites;
all native process exits 0. Initial failed aggregate remains recorded.
Six reviewed `visual-accepted/` captures and Command-Help-Example.FCStd; `visual/`
retains the ineffective inherited-font stress captures. Source/runtime module hashes
match; `validated-identities.json` and `acceptance-summary.json` identify the payload.
FreeCADGui SHA256: `72AD07F792C746280276D8388CB0845EB57BA293BBD17140E093CE98CF591655`.
Historical About metadata is not the changed Python source identity.
No installer/release update. Whole 10.9/F123 remains open for shared workspace
transitions, broader command eligibility explanations, keyboard modeling/downstream
coverage, localization, physical screen-reader and multi-monitor/high-DPI acceptance.
The owner guide is [CommandSearch.md](../tests/CommandSearch.md). Stop at this
bounded owner-test checkpoint and rotate to another family.

Gate G4: simple part/assembly creation, edits, precise moves and recovery survive
save/reopen. Guided/direct entry and aliases produce equivalent semantics. Test
zero/one/multiple targets, invalid contacts, cross-component overlap, missing cut
target, manual override and changed intersections. Compare measured tasks to baseline.

## [   ] Phase 11: Selection-aware Sketcher and reference workflows (P5)

Depends on stable selection/reference contracts; audit existing solver capabilities
before replacement. These tasks extend 8.3, with one reusable eligibility service.

- [   ] 11.1 Audit and improve automatic coincidence, horizontal/vertical, parallel,
  perpendicular, tangent and equal inference. Preview constraints, expose thresholds
  and per-sketch preferences, and support temporary suppression without conflicting
  with selection modifiers. Test cases where no constraint should be inferred.
- [   ] 11.2 Implement fast structural applicability separately from solver
  feasibility. One service serves palettes, toolbar/menu actions, shortcuts and
  execution. No selection shows drawing/global actions; one line offers supported
  single-line actions; two suitable lines add Parallel/Perpendicular. Other operand
  types/counts/roles use their supported relations. Hide structurally inapplicable
  actions; disable proven conflicts with reasons and highlighted constraints.
  Distinguish Valid, Already Applied, Redundant, Conflicting, Unsupported and
  Unverified. Use nonmutating/rolled-back trials, revision/selection caches and stale
  result rejection; revalidate on commit and never silently remove constraints.
- [   ] 11.3 Add a reachable near-cursor suggested-constraint palette using 11.2:
  stable pointer corridor/dismissal delay, useful ordering, keyboard access and
  disable preference. Test dense sketches, zoom/DPI and movement toward/away from
  it. Measure eligibility latency; a palette alone does not complete 11.2.
- [   ] 11.4 Unify smart dimensions and numeric entry while drawing; distinguish
  driving/reference dimensions from construction/reference geometry conversion.
  Show remaining degrees of freedom and conflict/redundancy diagnostics with
  deliberate, undoable repair that preserves intended design relationships.
  Smart Dimension infers length, angle, radius, diameter or spacing from selected
  geometry. Numeric entry while drawing covers lines, rectangles, circles and slots.
  Degrees-of-freedom display highlights unconstrained entities and remaining movement
  directions. Constraint repair previews proposed removals/replacements and their
  effects before an explicit undoable commit.
- [x] 11.4a Add bounded F048 constraint-repair review for free root sketches:
  native isolated-copy diagnosis, explicit constraint choices and deactivation
  preview with remaining freedom, preserving source data and constraint identities.
- [x] 11.4b Add the review/geometry-selection/preview workflow and one transactional
  Apply, with failed-preview refusal, stale/context guards, rollback, Cancel and
  downstream/Undo/save-reopen acceptance.

Both implementation tasks preceded one SketcherGui/SketcherScripts Release build,
exit 0. Evidence: `D:\Temp\Office-PC\freecad-plus-constraint-repair-20261001`.
`grouped/` passes eight repair checks and seven existing sketch-reuse checks. A final
UI correction frames the temporary overlay automatically because native Fit All
excludes it; only ConstraintRepairGui.py was restaged, without a second native build.
`repair-verified/` passes all eight repair checks, including a 10,000 mm off-origin
preview. **15 distinct selected passes**, zero failures/errors/skips in accepted
suites, native exits 0. Six final `visual-accepted/` captures were reviewed: redundant
and conflicting diagnoses, failed choice, successful proposal, preview wireframe
and reopened inactive constraint. Earlier `visual/` used harness framing and is
retained separately. Constraint-Repair-Source.FCStd / Constraint-Repair-Result.FCStd
are owner fixtures; the unselected redundant profile intentionally remains unrepaired.
Native diagnostics distinguish equal-radius redundancy from unequal-radius conflict.
Preview preserves source content, constraints, object count, Undo and active document.
Choice/Cancel, retained dimension identity/values, transaction/stale guards, rollback,
Undo/Redo and save/reopen pass. A repaired radius-5 profile extrudes 4 mm to 100*pi
mm^3; changing the surviving radius to 6 after reopen updates it to 144*pi mm^3.
Sketcher SHA256: `0525D3CA7E6DB90B2830C504F9BC99DB1A092D6D72268E5A18D70C15F2EED0D6`.
SketcherGui SHA256: `1B375C675DBABA3373565643D0D493CA9E8EA58CE9A4E3FC09A09DF17D11E5D4`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted evidence; the historical About stamp is not this source identity.
No installer/release update. Full F048/11.4 remains open for Body/attached/external
and expression-driven sketches, constraint replacement, consumer-wide previews,
movement-direction diagnosis, macro recording, localization and physical acceptance.
Stop here for owner workflow testing and rotate to another item family.
[Owner procedure](../tests/ConstraintRepair.md).

- [x] 11.4c Add F047 text guidance to the existing sketch solver task: distinguish
  remaining freedom, fully constrained, empty and invalid solver states; explain
  coupled freedoms, fixed/Block constraints, construction and reference dimensions.
- [x] 11.4d Expose native unconstrained-geometry selection beside that guidance,
  enabled only for a successful underconstrained solve. Preserve geometry, constraints,
  edit context and native selection behavior; verify live repair, Undo/Redo and reopen.

11.4c/d evidence (2026-10-01): both tasks preceded the grouped SketcherGui/
SketcherScripts build. Initial compilation exposed constructor-parameter shadowing
in a lambda; the corrected incremental build exits 0. Initial failure log retained.
Evidence: `D:\Temp\Office-PC\freecad-plus-sketch-freedom-20261001`.
Seven TestSketchFreedom checks pass in freedom-verified/; eight unchanged
TestConstraintRepair checks pass in grouped/. **15 distinct selected checks pass**,
zero failures/errors/skips in accepted suites; native process exits 0. The initial
new-test failures used IsDriving instead of the native Driving property and reopened
an edit session between Undo/Redo. Corrected tests exercise Undo/Redo within edit;
no further implementation changes or build were needed after the passing build.
Native selection highlights solver-dependent elements while excluding fixed geometry,
preserving geometry/constraint values, placements and Undo count. Empty, successful
underconstrained, fully constrained, conflicting and redundant states are distinct;
repair reenables selection. Construction/reference geometry, live constraint
transitions, Body placement 10,000 mm off-origin and save/reopen pass. No new solver,
constraint types or document properties were introduced.
Five captures in visual/ were reviewed: underconstrained, selected native geometry,
conflict, fully constrained and reopened state. Sketch-Freedom.FCStd and
Sketch-Located.FCStd are owner fixtures. validated-identities.json and
acceptance-summary.json record source/runtime identity and accepted checks; the
historical About stamp does not identify this rebuilt module. No installer/release
update. Full F047 remains open for movement-direction indicators, richer per-entity
diagnosis, physical keyboard/high-DPI and owner acceptance.
[Owner procedure](../tests/SketchFreedom.md). Rotate after this workflow checkpoint.

- [   ] 11.5 Extend associative external projection and true plane intersections:
  curve/plane points versus face/plane curves, with source highlighting and explicit
  projection/intersection choice. Cover tangent, coplanar, disjoint and multiple
  results; changes update or report broken references across approved scopes.
- [   ] 11.6 Complete regions, gap/duplicate/self-intersection diagnostics and
  trim/extend improvements; add constraint-preserving copy/paste, blocks, reusable
  profiles and sketch patterns as separate increments.
  Sketch repair additionally detects tiny segments and overlapping geometry. Power
  trim/extend supports dragging across unwanted segments while retaining valid
  constraints where possible and reporting losses. Region picking selects closed areas
  inside a larger sketch without requiring the whole sketch as the profile.

- [x] 11.6a Extend existing Validate Sketch missing-coincidence search with
  endpoint identities, measured gaps, candidate-row highlighting and explicit mm
  search tolerance (F049). Search and review must not change geometry/constraints;
  no candidates must not imply that all profile defects are resolved.
- [x] 11.6b Add checked-candidate coincidence repair in one native transaction,
  preserving existing constraints and rolling back solver failures. Invalidate
  candidates after sketch/tolerance/construction-policy changes. Verify deliberate
  gap closure, subset repair, Undo/Redo, save/reopen and downstream solid creation.
  Duplicate, overlap/self-intersection diagnostics and geometric repair preview remain open.

11.6a/b evidence (2026-09-30): both tasks preceded the grouped SketcherGui/SketcherScripts
Release build. Initial attempt failed on the observer connection type; scoped_connection
correction built successfully (exit 0). **22 selected PASS**, no failures/errors/skips:
5 repair in repair-verified/, 5 inherited coincidence validator, 5 sketch-support
and 7 command-search checks in grouped/, all process exits 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-sketch-repair-20260930`, acceptance-summary.json,
validated-identities.json, build.log and build-initial-failed.log. SketcherGui SHA256:
`ed450a6370921ed0012d7d2dab6873b1d3078cb0053a12bfb1a9066163cbdedc`.

Search/review/Close are read-only; candidate markers clear on Close. Checked-only
repair, construction policy, invalid tolerance, edit invalidation, pending-transaction
guard, conflict rollback, Undo/Redo and save/reopen pass. A repaired 20 x 10 mm profile
produces a 1000 mm³ extrusion and updates to 1250 mm³ after a Width edit on reopen.
visual/ has five reviewed captures, Sketch-Repair.FCStd and Sketch-Repaired-Solid.FCStd.
[Owner procedure](../tests/SketchRepairReview.md). No release/installer update.

Earlier grouped/ retains a task-widget lookup error; repair-final/ and repair-accepted/
retain fixture assumptions corrected using native probes. Final application source
was unchanged after the successful build. Native coincidence insertion can move
Block-constrained geometry while retaining Block constraints; the detector can omit
already dimension-referenced endpoints. These native semantics are not redesigned here.
The accepted conflict fixture uses dimensioned lines with unreferenced candidate ends
that cannot meet. Whole F049/11.6 remain open for duplicate/self-intersection diagnosis,
broader repair, geometric preview and physical/high-DPI acceptance. Stop for feedback.

- [x] 11.6c Add independent whole-sketch reuse for free root sketches (F053), using
  the native document copier to preserve geometry order, internal constraints,
  named dimensions and construction roles. Typed source-axis offsets and rotation
  change the new sketch's Placement; source and consumers remain unchanged.
- [x] 11.6d Add an installed review/preview/confirmation workflow, reusing native
  selection identities and the existing non-pickable scene overlay. Frame the
  proposed result, remove it on numeric/model changes or close, refuse unsupported
  linked inputs explicitly and commit one Undoable copy with rollback. Both tasks
  are ready for owner testing; broader F053 scope stays open.

11.6c/d evidence (2026-10-01): both tasks preceded one SketcherGui/SketcherScripts
Release build, exit 0. Initial grouped/ has 35 passes and one inherited intentional
skip, no failures/errors: 7 TestSketchReuse, 23 of 24 SketcherTests.TestSketcherSolver,
and 5 TestSketchSupportCommand. The skipped native secant driving-distance test is
decorated with the existing PR 9044 discussion note; it was not changed or counted
as a pass. The strict no-skips harness marks that aggregate false; GUI process exit 0.
Visual inspection then showed native Fit All omitting the offset view-only overlay.
SketchReuseGui now frames the complete scene on Preview. Only this Python module
was restaged, no second native build. All 7 affected checks pass again without
failures/errors/skips in reuse-verified/; the 28 unchanged regression passes stand.
Evidence: `D:\Temp\Office-PC\freecad-plus-sketch-reuse-20261001`.
SketcherGui SHA256: `9b75530fb26a5c39b179aee9443e15f18122c298e040e9cbad8f85b66391bf2b`.
The fully constrained slot retains 5 geometry elements including construction,
11 constraints and named dimensions. A rotated/translated independent copy changes
radius from 3 to 4 mm while preserving the source; its reopened 5 mm extrusion
updates from 741.371669 to 1051.327412 mm³. Preview/commit geometry, native placement,
Cancel/invalidation/close, owner booked-transaction protection, rollback and
Undo/Redo pass. Five final captures reviewed in visual-accepted/; visual/ retains
the off-screen preview and visual-frame-probe/ demonstrates the framing diagnosis.
Reusable-Slot.FCStd, Copied-Slot.FCStd and Edited-Copy-Solid.FCStd are owner fixtures.
acceptance-summary.json and validated-identities.json record suite results, the
deliberate inherited skip and exact source/runtime/native identities. Historical
About metadata is not this batch's source identity. No installer/release update.
Root free sketches with at most 500 geometry elements only; support, external
geometry, expressions and other links are refused without silently stripping data.
Whole F053/11.6 remain open for partial paste/remapping, external-reference choices,
Body/Part/occurrence scope, blocks, libraries, sketch patterns and physical acceptance.
[Owner procedure](../tests/SketchReuse.md). Stop here for owner feedback and rotate.

- [x] 11.6e Group native hold-and-drag Trim changes into one Undo step, commit
  on release and roll back an unfinished/failed gesture on cancellation. Keep
  earlier completed gestures and native trim/constraint semantics (F050).
- [x] 11.6f Show completed trim count and native removed/replaced-constraint identifiers;
  prevent release from reusing a consumed pick. Verify real viewport drags,
  single click, Undo/Redo, empty gestures and Escape/edit-exit cancellation together.

2026-10-01 bounded validation: both tasks preceded one 90-second SketcherGui build.
A second 90-second build corrected notice clipping observed in captures and clarified
that native removal notifications can include replacement identities retaining a name.
Both builds exit 0. Five TestTrimGesture checks pass on the final source-built GUI;
seven unchanged TestSketchFreedom checks passed in the initial grouped run: twelve
distinct accepted checks, no skips. Final viewport-event coverage includes three-edge
one-step Undo/Redo, single click without a duplicate release trim, empty drag,
Escape preserving an earlier completed gesture and sketch-edit exit rollback.
Five final captures were reviewed; the eight-geometry/seven-constraint result saves
and reopens with matching geometry and a successful solve, and Undo restores the
original named constraint. Kernel-exception rollback is implemented but not
fault-injected. Evidence: `D:\Temp\Office-PC\freecad-plus-trim-gesture-20261001`
(`grouped`, `notice-verified`, `visual-final`, build logs and `evidence.json`).
An earlier capture run failed because its helper used an unavailable constraint-name
API; that failure and superseded captures are retained separately. The About commit
stamp is historical; source/runtime hashes identify this validation.

This increment reuses existing boundary markers, Include axes and native geometry
operations. New removal previews, extension-to-boundary guidance, general curve
coverage and physical/high-DPI acceptance remain open. No owner acceptance or release
is claimed. [Owner procedure](../tests/TrimGesture.md). Stop here and rotate.

- [   ] 11.7 Make sketch placement, orientation, offset and support/reattachment
  explicit (S08; [F124](#f124)). Preview preserve-local versus preserve-world policies,
  prefer stable references where appropriate, and repair lost supports deliberately.
  Validate rotated occurrences, external projections, constraints and Undo with T14.
- [ X ] 11.7a Prototype explicit same-document planar-face reattachment preserving
  the local attachment offset. Validate downstream result placement/identity,
  Undo/Redo and native save/reopen with two parallel supports.
- [ X ] 11.7b Reject missing and curved support faces before changing the sketch;
  verify existing support, placement, offset and downstream geometry remain intact.
- [ X ] 11.7c Verify preserve-local reattachment to a differently rotated planar
  support inside a rotated part, retaining the full offset and valid result volume.
- [ X ] 11.7d Prototype preserve-world reattachment by solving a compensating
  native attachment offset. Verify world translation/orientation, result position
  and identity, Undo/Redo, save/reopen and subsequent support movement.
- [ X ] 11.7e Prototype deliberate repair of a missing planar face reference using
  an explicit preserve-local replacement. Reject preserve-world for invalid sketch
  state; verify repair, Undo back to failure, Redo and save/reopen with result identity.
- [ X ] 11.7f Reject prototype reattachment while a caller-owned transaction is
  pending, before mutation. Verify the caller's edit remains uncommitted and can be
  aborted, followed by successful independent reattachment and Undo.
- [ X ] 11.7g Reject support geometry that depends on the sketch before introducing
  an attachment cycle. Verify with a native extrusion derived from the sketch,
  preserving support, placement, validity and transaction state after rejection.
- [ X ] 11.7h Reject supports with invalid or pending recompute state, including
  dependencies. Verify touched-plane and failed-box rejection, then repair the box,
  recompute, reattach successfully and Undo back to the original support.
- [ X ] 11.7i Prototype synchronous candidate placement preview by recomputing in
  a temporary transaction and aborting. Verify both placement policies match later
  commits while restoring support, offset, world placement and downstream position.
- [ X ] 11.7j Verify repeated previews and rejected missing-face preview preserve
  an existing committed user edit and its Undo/Redo without a pending transaction.
- [ X ] 11.7k Replace live-document rollback preview with planar attachment
  evaluation in a disposable hidden document. Verify candidate/commit parity,
  no original-object change/recompute notifications, cleanup and active-doc restore.
- [ X ] 11.7l Verify both placement previews preserve an already-populated redo
  stack: undo a committed label edit, preview, then redo that same edit successfully.
- [ X ] 11.7m Validate MapReversed attachment with both placement-policy previews
  and commits, Undo and native restore, including downstream result validity.
- [ X ] 11.7n Reject preserve-world preview/commit when AttachmentOffset is driven
  by an expression. Verify no mutation and preserve-local retention of a named
  length expression through restore and subsequent parameter edits.
- [ X ] 11.7o Probe differently placed part containers and guard the unsupported
  cross-container case. Verify both policies reject preview/commit before changing
  either part, opening a transaction or creating a temporary preview document.
- [ X ] 11.7p Reject App::Link occurrence supports until an explicit definition/
  occurrence edit policy exists. Verify preview/commit leave both occurrences,
  their definition links and the sketch unchanged.
- [ X ] 11.7q Prototype an explicit local planar reference with source/ancestor
  dependencies and world-to-local shape conversion. Verify alignment with a face
  in another placed part and preview/commit parity under both placement policies.
- [ X ] 11.7r Verify that reference follows source-part movement, Undo/Redo,
  save/reopen and further movement while preserving downstream result identity.
- [ X ] 11.7s Prototype atomic reference creation plus reattachment. Verify one
  Undo removes the reference/restores attachment and Redo/save/reopen retain it.
- [ X ] 11.7t Inject failure after attachment but before commit; verify rollback
  removes the reference, restores support/world placement and closes the transaction,
  then permits a subsequent successful operation.
- [ X ] 11.7u Verify missing-face failure clears adapter output and prevents preview;
  explicit face repair recovers through Undo/Redo and restore with result identity.
- [ X ] 11.7v Report deleted source explicitly and remove obsolete placement
  dependencies. Verify source replacement plus deliberate sketch face reselection,
  restore and subsequent source-part movement.
- [ X ] 11.7w Prototype an explicit consumer accessor that refuses cached results
  after dependency failure. Prove the old solid remains cached but access rejects;
  source repair and save/reopen restore successful access.
- [ X ] 11.7x Reject pending recompute without silently recomputing; verify source
  movement appears after explicit recompute and returned-shape mutation cannot
  change the stored/current result.

- [x] 11.7y Promote the proven same-container planar reattachment and disposable
  placement-preview operations into the installed Sketcher module. Keep experimental
  cross-part reference creation test-only and preserve native attachment identities.
- [x] 11.7z Add the sketch support editor: current-support inspection, explicit
  replacement face, local/world policy, numeric placement preview, stale-preview
  rejection and undoable Apply/repair. Stop for owner testing after grouped native
  geometry/persistence and command checks; viewport ghost preview remains pending.

11.7y/z grouped evidence (2026-09-30): both tasks preceded one SketcherGui/
SketcherScripts Release build, exit 0. All **39 selected checks pass**, zero
failures/errors/skips, process 0 (5 installed editor, 34 existing history adapter).
Evidence: `D:\Temp\Office-PC\freecad-plus-sketch-support-20260930`, `grouped/`,
`acceptance-summary.json` and `validated-identities.json`. Installed scripts match
source. The direct core is installed; the cross-part reference adapter retains its
test-only module identity. World preservation, rotated container, constrained sketch,
downstream extrusion, missing-face local repair, Undo/Redo, save/reopen, stale preview,
cycles, linked-support rejection and editor lifecycle pass. Three reviewed captures
and native-only `visual/Sketch-Support.FCStd` support [owner testing](../tests/SketchSupport.md).
Preview reports placement numerically without changing source geometry; it does not
simulate constraints/downstream solids. Physical/high-DPI interaction, graphical
ghosts, broader datums/occurrences and external-projection acceptance remain open.
No installer/release update. Whole 11.7/F124 remains open; rotate the next family.

Consumer boundary evidence: `reference-consumers-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **50 PASS, zero failures/
errors/skips** (11 capability, 34 adapter, five lineage checks). Macro PASS; process
ended. Both tasks preceded grouped testing using engine source 2df76790b4.
`current_result_shape` in `tests/prototypes/PartHistoryAdapters.py` checks native
Invalid/Touched state across the result and dependencies, Ready status and nonempty
geometry, returning a copy. Native failure can skip downstream execution and retain
the old solid; the test establishes that this accessor rejects that solid. It does
not clear caches or retrofit application exporters, GUI, CAM, FEM or TechDraw.
Prototype SHA256: `21B509DEBE9B5D04DF0D155E07AD65CF5A9F475445B07AC1D31F2550F459A32C`.
No installed module, native rebuild or release update. General consumer integration,
dependency-cycle/large-graph behavior and production result contracts remain open.

Reference repair evidence: `reference-repair-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **48 PASS, zero failures/
errors/skips** (11 capability, 32 adapter, five lineage checks). Macro PASS; process
ended. Both tasks preceded grouped testing using engine source 2df76790b4. Initial
batch had 47 passes/one failure: replacing a deleted source repaired the adapter
but left the sketch's old mapped face invalid. Explicit preserve-local reselection
repairs that reference; no automatic topology equivalence is claimed. Recovery
preserves result identity and native documents with the prototype module available.
Prototype SHA256: `1C54D5F05CEB52B78FBFAAB4E9ACBA9CA2CD437433C78D782776B999A1E6ED16`.
Test-only changes; no installed module, native rebuild or release update. These
checks establish adapter output clearing and deliberate repair, not absence of
cached downstream geometry during failure or general export-consumer safety.

Atomic operation evidence: `reattachment-atomic-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **46 PASS, zero failures/
errors/skips** (11 capability, 30 adapter, five lineage checks). Macro PASS; process
ended. Both tasks preceded grouped testing using engine source 2df76790b4.
`reattach_with_reference` validates source/policy first and owns the outer native
transaction; internal attachment participates without committing the caller's work.
Public operations still reject pre-existing caller transactions. Fault injection
tests transaction recovery, not a claim that all native failure paths were exercised.
Prototype SHA256: `F83559E7515736EF594DE65050D5713C0D5D65E14F435ADF348D853F415DFAAE`.
Test-only; saved adapter fixtures require the Python module. No installed application
change, native rebuild or release update. UI/task transaction integration and
source-topology/consumer failure handling remain pending.

Adapter evidence: `reattachment-adapter-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **44 PASS, zero failures/
errors/skips** (11 capability, 28 adapter, five lineage checks). Macro PASS; process
ended. Both tasks preceded grouped testing using engine source 2df76790b4. Native
SubShapeBinder probes are retained in evidence: `reattachment-binder-20260930-batch`
had two initial-alignment failures; parent-qualified support in
`reattachment-binder-20260930-verified` fixed alignment but failed the source-motion
criterion (7.389913 mm difference from expected displacement). These are bounded
fixture findings, not a general verdict on native binders. The passing PlanarSupport
prototype reuses BasicShapes.ShapeReferences validation, placement dependencies and
shape conversion. Direct cross-container attachment and occurrence selection still
reject; the explicit adapter resides beside the sketch. Saved adapter fixtures need
the prototype Python module to recompute; no installed module/schema/UI claim.
Prototype SHA256: `25C644F7B4E6A793112157AD31BB1C0B3D940510DFA091B366F65B88F5EB1A36`.
Missing/ambiguous source topology, failure consumers, atomic adapter creation and
production deployment remain pending. No native rebuild or release update.

Scope boundary evidence: `reattachment-scope-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **42 PASS, zero failures/
errors/skips** (11 capability, 26 adapter, five lineage checks). Macro PASS; process
ended. Both tasks preceded grouped testing using engine source 2df76790b4. Initial
batch had 41 passes/one failure: native direct attachment across differently placed
parts disagreed with the world-space preview (70.652620 mm origin difference).
The prototype now rejects different parent geometry containers rather than claiming
cross-part placement support. Native reference adapter/transform policy remains
unimplemented; no production functionality is removed by this test-only guard.
Prototype SHA256: `21D65714C897F62015DC199077455E2DE04C4536A2D75DEEC8CBF228166818D1`.
No installed application change, native rebuild or release update.

Expression/reversal evidence: `reattachment-expressions-20260930-verified/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **40 PASS, zero
failures/errors/skips** (11 capability, 24 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded grouped testing using engine source 2df76790b4.
Initial batch: 39 passes/one failure; a focused diagnostic exposed native expression
path `.AttachmentOffset.Base.z`, requiring leading-dot handling in the guard.
Prototype SHA256: `76981E9913335F1863490FF9BFDD89AD475721E220E1DEDC724620875F4323EB`.
No installed module, native rebuild or release update. The preserved expression
fixture references an independent named length; support-dependent expressions,
external projections and production expression editing remain separate gates.

Isolated placement evidence: `reattachment-isolation-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **38 PASS, zero
failures/errors/skips** (11 capability, 22 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded grouped testing using engine source 2df76790b4.
Prototype SHA256: `D2FA54E32FC736FFBF0D325DB72733AC4EA11861C049F1492830C52FF71EC588`.
This supersedes the live rollback implementation described in 11.7i/j. Preview
copies the support shape into world coordinates and evaluates native attachment on
a temporary sketch, retaining offset and MapReversed. It does not copy/evaluate
constraints, external sketch geometry or downstream solids. Application observers
can see temporary document creation/activation/closure. Graphical/asynchronous
preview, production transaction integration and broader attachment modes remain
pending. Test-only change; no installed module, native rebuild or release update.

Preview evidence: `reattachment-preview-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **36 PASS, zero failures/
errors/skips** (11 capability, 20 adapter, five lineage checks). Macro PASS; process
ended. Both tasks preceded grouped testing using engine source 2df76790b4.
Prototype SHA256: `FFB7C0A062757FE463A91837F40916108DE4EEB166E0063437C8BED4A8F97763`.
No installed module, native rebuild or release update. That synchronous test-only
preview temporarily mutated the document and recomputed: observers saw trial state.
It does not satisfy isolated trial execution or implement graphical preview,
asynchronous cancellation, production task transactions or preservation of an
already-populated redo stack. Those remain production gates under 11.7.

Support validation evidence: `reattachment-support-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **34 PASS, zero
failures/errors/skips** (11 capability, 18 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded grouped testing using engine source 2df76790b4.
Prototype SHA256: `4E22D978257BCF6A7758D7E6E0557F2FC1BE6A285BB4B3952E9DAEA4B9F02524`.
Native dependency traversal supplies cycle and state inspection; validation occurs
before opening the reattachment transaction. Tests cover a direct derived support,
a touched support and a failed native box; broader dependency graph and consumer
failure cases remain open. No installed application change, native rebuild or
release update. This is test-only prerequisite validation, not production UI delivery.

Recovery/transaction evidence: `reattachment-recovery-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **32 PASS, zero
failures/errors/skips** (11 capability, 16 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded grouped testing using engine source 2df76790b4.
Prototype SHA256: `6A006AFD9AD8C585BCB06FA0CBEFD178199296DB1B3F5985861A7995DA7B5C81`.
Test-only changes; no native rebuild, installed editor or release update. The
fixture uses an unavailable Face99 reference on an existing support, not deleted
object resurrection or ambiguous topology matching. Preserve-world requires valid,
recomputed placement; missing-face recovery is explicitly preserve-local. Nested
transactions are rejected, not integrated with a production task transaction.
Consumer stale-shape/export policy, general support repair and GUI remain pending.

Placement-policy evidence: `reattachment-policies-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **30 PASS, zero
failures/errors/skips** (11 capability, 14 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded this grouped run with engine source 2df76790b4;
no native build, installed module change or release update. Prototype SHA256:
`A48BA5C8C09FC164CE7A2F2D47C7DD8E1AFBA2F22F546996FCD27F1B558C5C7D`.
The sketch stays in its existing container. Preserve-world compensates the offset
at reattachment time; later support motion remains associative. This covers a
rotated parent definition, not a selected assembly occurrence, reparenting or
cross-document placement. Preview/UI, lost-support repair, production transaction
integration and broader consumer failure handling remain pending under 11.7.

Bounded reattachment evidence: `sketch-reattachment-20260930-verified/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **28 PASS, zero
failures/errors/skips** (11 capability, 12 adapter, five lineage checks). Macro PASS;
process ended. Both tasks preceded grouped testing with the existing fork build,
engine source 2df76790b4. Initial batch had 27 passes/one error: the native missing
face lookup raises IndexError, now converted into the prototype's validation error.
`tests/prototypes/SketchReattachment.py` SHA256:
`F52536AD4C705C29AD6569603E52D4416709000E20AD0D75FDC0EA0E44E0F770`.
Test-only operation, not installed; no native rebuild or release update. That batch did
not implement preserve-world placement, automatic topology repair, rotated
reattachment, external scope, preview or production transaction integration. The
caller must have no open transaction; broader consumer invalidation remains a gate.

Gate G5: solver trials cannot mutate live sketches; redundant/conflicting candidates
remain distinct and invalid suggestions cannot commit. Validate T12, inference/no
inference, external edits, stale asynchronous results and palette interaction.

## [   ] Phase 12: Assembly definitions, occurrences and interpart design (P2/P3/P6)

Depends on Phase 7 identity/persistence proof. A native Link or local-cut probe is
partial evidence, not completion of these production workflows.

- [   ] 12.1 Prove and productize mixed definitions containing geometry, datums and
  child occurrences, without converting a part to a different assembly type. Define
  logical definition versus document identity. Reuse one definition twice in one
  assembly and once in another; shared edits update loaded dependents, with explicit
  reload/update policy for closed external documents. Prevent double transforms.
- [ X ] 12.1a Prove a native definition containing a solid and a child occurrence
  can be instanced twice in one assembly and once in another. Shared dimension edits
  update all instances; child placement and resulting bounds/volume survive restore.
  Same-document proof only; external reload policy and product workflow remain open.
- [   ] 12.2 Productize occurrence overrides, Make Unique and Promote Bodies to
  Part/Component with explicit associative/independent choices. Remap internal
  references and identity for independent copies while preserving provenance;
  occurrence placement stays local. Validate replacement and multi-assembly reuse.
  Occurrence-local overrides explicitly include placement, visibility, color and
  representation; editing one override must not rewrite the shared definition or another
  occurrence. Component replacement preserves placement and recoverable mate/joint
  bindings, with unresolved relationships exposed for repair. Promoting selected bodies
  must present associative versus independent behavior explicitly.
- [ X ] 12.2a Implement a test-only Make Unique adapter for a definition containing
  one independent sketch and its native extrusion. Native recursive copy remaps
  inputs; assign fresh semantic IDs and provenance, relink only the chosen occurrence
  and preserve its placement. Verify Undo/Redo, independent edits and save/reopen;
  unsupported definition rejection must not create objects or change the link.

- [x] 12.2b Expose native whole-occurrence visibility and uniform appearance
  overrides for direct same-document shape/Body links (F018). Use native view
  properties, one Undo transaction and explicit source inheritance; preserve
  definition, other occurrences and placement. Arrays/per-element overrides remain out.
- [x] 12.2c Add an occurrence appearance editor with explicit identity, staged
  colour/transparency/visibility, Use source appearance, stale-state recovery and
  close/deletion handling. Verify native save/reopen and a repeated-part fixture;
  stop at owner-test-ready appearance before wider occurrence work.

Occurrence appearance evidence (12.2b/c): one grouped FreeCADGui/FreeCADGui_Resources
Release build, exit 0. **23 selected PASS**, no failures/errors/skips: 7 occurrence
checks in occurrence-accepted/, 9 unchanged temporary-display and 7 command-search
checks in grouped/, all process exits 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-occurrence-appearance-20260930`, acceptance-summary.json
and validated-identities.json. Source/runtime script hashes match. FreeCADGui SHA256:
`9f9ffbc6c1773c42d948c018ec71fc1533d850e988757a33741d6856254307fc`.
grouped/ retains an initial whole-link container-path selector failure and fixture
assumptions; occurrence-final/ retains a duplicate View menu lookup failure.
The Python selector now accepts structural Part paths and rejects traversal through
another Link; it was staged without a second native build. Corrected fixture/menu
checks pass. Do not report either earlier aggregate as passing.

visual/ has five reviewed captures and the native Occurrence-Appearance.FCStd example.
Apply/Undo/Redo/save/reopen, source/other-link isolation, placement, Body Tip, reset,
stale state and lifecycle pass. [Owner procedure](../tests/OccurrenceAppearance.md).
Whole F018 and parent 12.2 remain open: arrays/per-element overrides, nested occurrence
paths, external/mixed definitions, broader representations and physical/high-DPI
acceptance are deferred. No installer/release update. Rotate pending owner feedback.

Mixed/unique batch evidence: **32 PASS**, no failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\mixed-unique-20260929-final\results.json`.
Seven native capability probes plus ten history adapters, three clone checks,
seven intent and five lineage checks. `prototype-manifest.json` records source
hashes. The native mixed-part proof and the bounded copy require no application
change or native build; no GUI command is installed. MixedDefinitionProof.FCStd
and UniqueDefinitionProof.FCStd contain native objects with ordinary metadata.
The copy prototype excludes external dependencies, nested definitions, arbitrary
feature proxies, general body lineage and production identity/schema migration.
First run passed 31 checks; the final run adds no-mutation rejection coverage.
Parents 12.1/12.2 and architecture release gates remain open.

- [x] 12.2d Productize a bounded native Make Unique copy for a same-document
  Part containing one independent sketch and its Part extrusion (F019). Native
  recursive copy remaps internal inputs and assigns new native object identities;
  relink only the selected occurrence while preserving placement and visibility.
- [x] 12.2e Add explicit copy review, destination/name, stale-input recovery and
  transactional confirmation. Reject unsupported external/attached/expressed inputs,
  arrays/scales and occurrence consumers; verify independent edits, Cancel, rollback,
  Undo/Redo and save/reopen before expanding definition scope.
  Both tasks complete for owner testing. Arbitrary Body histories, subassemblies,
  provenance, external destinations and relationship remapping remain open.

12.2d/e grouped evidence (2026-10-01): both tasks preceded one FreeCADGui/
FreeCADGui_Resources Release build, exit 0. A Python-only selection correction
then resolved structural Part paths and was restaged without another native build.
19 distinct selected checks pass: 6 TestUniqueOccurrence in unique-verified/;
6 TestFeatureOrganizer and 7 TestCommandSearch in selected-grouped/, all accepted
suites without failures/errors/skips and process exits 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-unique-occurrence-20261001`.
acceptance-summary.json / validated-identities.json record source/runtime/native
identities; installed UniqueDefinition.py matches source. FreeCADGui SHA256:
`149486d68741474b996be733a55188737ea324b1214031a410fa291ea3885768`.
Native copy remaps the sketch input, creates new identities and preserves occurrence
world placement and visibility. Independent source/copy edits, Undo/Redo, save/reopen,
Cancel, stale/context guards and rollback after a forced post-copy failure pass.
Three captures reviewed; visual/ holds Shared-Spacers.FCStd / Independent-Spacers.FCStd
and the [owner procedure](../tests/UniqueOccurrence.md) describes the bounded workflow.
Earlier grouped/ is incomplete after an invalid-selection modal; only its isolated
validation process was stopped. selected-grouped/ retains the initial fixture failure
from hiding the source without recomputing; the corrected fixture passed in
unique-verified/. Do not interpret either earlier aggregate as a full passing run.
No installer/release update or physical acceptance. Parents 12.2 and F019 remain open;
stop at this usable checkpoint and rotate to another item family.

- [   ] 12.3 Add Entire Part/Model/Empty/custom named reference sets. Keep visibility,
  suppression, reference-only BOM role, configuration/arrangement and load state
  independent. Define deliberate full-geometry access outside exposed reference sets.
  Named reference subsets select bodies/datums. Empty changes the exposed representation
  only; it must not delete, suppress or exclude the component from BOMs implicitly.
  Fully loaded/lightweight/unloaded state is separately controlled.
- [   ] 12.4 Add contextual mates/joints, grounding, freedom/conflict display and
  joint limits using the existing solver. Preserve work/display context and clearly
  distinguish shared-definition edits from occurrence edits.
  Suggest mates/joints from selected faces, axes or points. Visually distinguish
  grounded, underconstrained, fully constrained and conflicting components. In-context
  editing keeps surrounding geometry visible, with selection/edit scope made explicit.
- [x] 12.4a Explain native assembly solver freedom and its distinction from grounding
  and connectivity; preserve existing conflict/malformed navigation (F077).
- [x] 12.4b Add read-only grounded/unconnected component navigation, refuse stale or
  failed freedom selection, and validate joint changes, Undo/Redo and persistence.
  Native solver guidance and selection pass. The task system now attaches contextual
  panels when no task dialog is open, transfers them across dialog open/close and
  hides another document's context. Native empty/incomplete-joint filtering is not
  certified as missing-reference diagnosis; full F077 remains open.

12.4a/b grouped evidence (2026-10-01): both tasks preceded a successful 70-second
AssemblyGui build. Runtime exposed the existing contextual-panel attachment defect;
one corrective 70-second build includes its shared TaskView fix. Eight assembly
checks pass in freedom-final/, including read-only grounding/connectivity selection,
slider versus unconnected distinction, redundant-joint disable/recovery, stale
refusal, task-dialog/document switching and joint Undo/Redo/save-reopen. Thirteen
inherited AssemblyTests.TestCore checks pass in grouped/; seven TestDimensionRepair
checks pass in freedom-verified/ against the corrected shared task view (28 distinct
selected checks total). Earlier harness failures and the interrupted run are retained:
Qt enum conversion and deferred widget deletion were corrected; the unsupported
empty-joint diagnosis fixture was replaced with native redundant-joint evidence.
Five native GUI captures were reviewed. Evidence: D:\Temp\Office-PC\freecad-plus-assembly-freedom-20261001.
[Owner procedure](../tests/AssemblyFreedom.md). Stop at this bounded checkpoint and
rotate pending owner feedback; per-component movement directions, incomplete-joint
and external/nested loading diagnosis and physical acceptance remain open.

- [x] 12.4c Explain relative motion for native Fixed/Revolute/Cylindrical/Slider/Ball
  joints, distinguish combined solver restrictions and expose exact reference paths (F076).
- [x] 12.4d Keep reversed/nonfinite enabled limits in the task for correction or
  Cancel; preserve expressions, displayed accepted bounds and native transactions.
  Verify disabled/unsupported limits, both Cylindrical pairs, equal bounds,
  new/edit Cancel, Undo/Redo and save/reopen. Full F076 remains open.

12.4c/d grouped evidence (2026-10-01): both tasks preceded staging the Python module
in the source-built fork and grouped validation; no C++ or resource rebuild was
required. Eight TestJointReview checks pass in joint-verified/; eight
TestAssemblyFreedom and thirteen inherited AssemblyTests.TestCore checks pass in
grouped/ (29 distinct accepted checks). Initial failures exposed native solver
normalization of reversed bounds. The task now checks displayed inputs and evaluates
expressions before solving, and synchronizes accepted literal bounds after any preview
normalization. Direct property-editor/scripted solver behavior is unchanged.
Earlier failed runs remain recorded; the Cancel assertion was corrected to compare
UndoCount before opening the native transaction. Six GUI captures were reviewed in
visual/ before the final acceptance-only synchronization correction; eight final
checks cover that correction. Two FCStd fixtures are included. Evidence:
D:\Temp\Office-PC\freecad-plus-joint-review-20261001.
[Owner procedure](../tests/JointReview.md). No installer/release or owner acceptance
is claimed. Automatic suggestions, ambiguity alternatives, full motion/conflict
previews, broad nested/external references and physical acceptance remain open.
Rotate to another family pending owner workflow feedback.

- [   ] 12.5 Add occurrence-aware in-context references and published datum/geometry/
  parameter interfaces, with source highlighting. Provide external-reference manager:
  source/version state, update/freeze/break, missing-path repair, unpublished-input
  diagnostics and dependency-cycle rejection. Extend 9.3 rather than inventing
  per-workbench traversal rules.
  Associative geometry linking copies selected geometry between parts with visible
  source tracking and update controls. Reference repair previews the downstream effects
  of replacing a missing face/edge. Preserve geometric selection intent as well as
  identity across topology changes; cycles must be rejected before acceptance. Failure
  reporting identifies the first failed feature, invalid input and blocked dependents.
- [   ] 12.6 Productize assembly-owned cuts with explicit selected-occurrence scope;
  source propagation is a separate deliberate action. Add component patterns/mirrors
  with skipped instances and shared/unique behavior, exploded views and simple motion.
  Save exploded arrangements and support simple mechanism animations with joint limits.
  Mirroring distinguishes linked/shared instances from independent mirrored definitions;
  skipped instances are stored explicitly.
- [ X ] 12.6a Add a bounded single-occurrence replacement using native Link.setLink.
  Reuse a same-document root solid/whole Body, preserving native occurrence identity,
  label, placement, source-placement setting, visibility and uniform appearance
  policy. Other occurrences and source definitions stay unchanged. Refuse consumers,
  relationships, scaled/array/copy-on-change links and unsupported source scope.
- [ X ] 12.6b Expose explicit source review, view-only preview, stale-input recovery
  and one Undoable confirmation in the standard Tools menu. Reuse native identity,
  occurrence selection, placement and appearance services; verify independent native
  geometry, failure rollback, Cancel, Undo/Redo and save/reopen.

12.6a/b evidence (2026-10-01):
Both tasks preceded one FreeCADGui/FreeCADGui_Resources Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-occurrence-replace-20261001`.
Initial `grouped/` passed seven movement and seven appearance checks, plus four of
eight replacement checks. Qt findData did not match stored Python identity tuples;
replaced it with explicit key comparison. A test quantity increment also needed its
native length value. Only OccurrenceReplace.py was restaged; no second native build.
`replacement-verified/` passes all eight. **22 distinct selected passes** across
accepted suites, zero failures/errors/skips in accepted suites, native exits 0.
Initial failed aggregate remains recorded. Five reviewed `visual/` captures and
Occurrence-Replacement-Source.FCStd / Occurrence-Replacement-Result.FCStd provide
the owner fixture. Native assembly-path geometry agrees with preview for both
source-placement settings; whole Body sources, preserved appearance/placement,
other-occurrence isolation, Cancel/stale cleanup, unsupported consumers, rollback,
Undo/Redo and save/reopen pass. Later replacement edits update only its instances.
FreeCADGui SHA256: `8F48A425D59BFE4A5182B2F3CEDB920932AAFDB1104A5658B9CE2F63A529AE8A`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted checks; historical About metadata is not this source identity.
No installer/release update. Whole F022/12.6 remains open for mate/interface remapping,
multiple targets, realignment, external/mixed sources, arrays, broader appearance,
macro recording and physical acceptance. Stop at this checkpoint and rotate.

- [   ] 12.7 Define configurations, arrangements and flexible subassemblies after
  parameter scope, identity, solver context and persistence proof. Flexible behavior
  is not merely separate placement of a shared rigid result. Extend 9.6.
  Dimension/suppression configurations and assembly-position arrangements are separately
  saved concepts; switching one must not implicitly overwrite the other.
- [ X ] 12.7a Preserve native occurrence/definition and enclosing structural-parent
  transforms in copied exploded-view output. Resolve the owning native ViewGroup;
  TechDraw explicitly consumes the saved view without moving modeled sources.
- [ X ] 12.7b Derive successive trails from each step's current geometry and align
  radial preview/output frames. Report unavailable move references instead of
  silently omitting steps. Prove the bounded solid-occurrence workflow through
  native task Accept/Cancel, Undo/Redo, save/reopen and a real TechDraw projection.

12.7a/b evidence (2026-10-01):
Both tasks preceded one AssemblyTests Release script-staging pass, exit 0; no C++
changes or native recompilation. Evidence:
`D:\Temp\Office-PC\freecad-plus-exploded-output-20261001`.
Initial grouped checks exposed a radial live-preview frame mismatch, corrected by
using copied world geometry and converting its delta into the structural parent
frame. Two inherited movement-row mocks lacked Label; the fixture now supplies it.
Only corrected Python files were restaged. The drawing test was completed with a
native page, the existing ISO template and asynchronous projection settling.
`corrected/` passes all 19 inherited movement-editor checks; `accepted/` passes all
nine output checks. **28 distinct selected passes**, zero failures/errors/skips in
accepted suites, native exits 0. Earlier failed aggregates remain recorded.
Five reviewed `visual-accepted/` captures show assembled geometry, two saved steps,
restored placements, explicit TechDraw output and reopened editing. The initial
capture attempt reopened on the drawing tab; the corrected harness activates the
model tab before entering assembly edit mode. `Exploded-Arrangement.FCStd` supplies
the owner fixture. Source geometry/placements/visibility, LinkTransform variants,
translated/rotated parents, repeated/radial trails, explicit missing-reference
failure, native dialog restoration, Undo/Redo and persistence pass.
validated-identities.json and acceptance-summary.json identify source/runtime and
accepted checks; historical About metadata is not the exact source identity.
No installer/release update. Whole F080/12.7 remains open for mixed parent/child
subassembly moves, broader link/visibility coverage, configurations, flexible and
joint-driven motion/limits, BOM arrangement choice and physical owner acceptance.
[Owner procedure](../tests/ExplodedViewOutput.md). Stop at this checkpoint and rotate.

- [   ] 12.8 Profile then implement lightweight/partial loading and simplified
  representations. Missing/unloaded components remain represented; commands requiring
  full geometry resolve it explicitly or report unavailable validation.
  Evaluate shared instance graphics and visibility-based processing in addition to
  selective loading and simplified representations. Optimization must not omit
  hidden/unloaded components from checks requiring their geometry.

Gate G6: nested multi-file assembly with shared/unique edits, replacement, reference
sets, in-context references, relocation repair and local cuts survives persistence.
Do not silently omit missing components from checks or BOMs.

## [   ] Phase 13: Solid, curve and surface portfolio (P7)

Depends on stable feature/result contracts. Preserve existing Trim/Isocline and
Phase 3 command work; extend only missing behavior. Each feature needs supported
inputs, tolerance, multi-result/target/tool retention and downstream-edit contracts.

- [   ] 13.1 Complete solid/sheet trim and split coverage beyond the existing Trim
  feature; implement sew/stitch, offsets, gap diagnostics and sheet thickening.
  Spike high-curvature/self-intersection cases; validate actual solid/shell counts.
  Body split/trim accepts supported planes, surfaces or other bodies and previews
  retained regions. Add surface untrim and extend, plus interactive keep-region
  selection and associative trimming tools. Thicken supports one-sided, opposite-sided
  and symmetric thickness with Boolean options. Sewing exposes gaps and tolerance and
  creates a solid only when a valid closed volume results; open results remain sheets.
- [ X ] 13.1a Honor explicit native Python sewing tolerance and expose it in the
  existing Shape Builder. Reject non-finite/non-positive API values; bound the task
  to 0.0000001-1 mm without automatic escalation. Sew copied source faces and disclose
  maximum result geometry tolerance, which may exceed the requested joining value.
- [ X ] 13.1b Add nonmutating shell/solid checks, open/closed/disconnected and free-
  boundary reports, snapshot provenance and atomic native creation. Refuse open or
  invalid shells for solid creation without losing inputs. Validate complete/gapped/
  open enclosures, a curved seam, source/placement preservation, native controls,
  invalid/stale/nested inputs, Undo/Redo and save/reopen.

13.1a/b evidence (2026-10-01):
Both tasks preceded one PartGui/PartScripts Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-shape-sewing-20261001`.
Initial `grouped/` passed all 14 Trim Body checks and 6/8 sewing checks. Two test
expectations were corrected for native Part origin objects and the face-only
selection gate; no implementation rebuild. `sewing-verified/` passes all eight.
**22 distinct selected passes** across accepted suites, zero failures/errors/skips
in accepted suites, native process exits 0. Initial failed aggregate is retained.
Six reviewed `visual-settled/` captures and Sewing-Sources.FCStd / Sewing-Results.FCStd;
initial `visual/` captures caught native layout/radio animations before settling.
The 0.01 mm gapped enclosure stays disconnected at 1e-6 mm sewing tolerance;
explicit 0.05 mm joins it and reports 0.0105 mm maximum geometry tolerance. The
exact enclosure produces a valid 1000 mm^3 solid; the open shell is refused.
Part SHA256: `5DF2B65D6A4F06972AA7596371B7D777779D0AB11F86D29FA68A2C842725C128`.
PartGui SHA256: `7ACC4FBFDE731DA33A76528FC0373D16E563F2D7C01164AD8F5C6CEA0409CBE6`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted checks; historical About metadata is not this source identity.
No installer/release update. Root same-document inputs, 500 faces maximum.
Whole F068/13.1 stays open for associative links, graphical boundaries/preview,
gap-width measurement, broader nonmanifold/healing diagnostics, standalone macro
replay, localization and physical acceptance. Stop here for owner testing and rotate.

- [ X ] 13.1c Make the native 3D Offset sheet-thickening workflow explicit:
  signed one-sided thickness, Reverse side without replacing expressions, separate
  associative result, and clear solid versus offset-sheet/preview-pending status.
- [ X ] 13.1d Validate filled face/shell results as closed valid solids; refuse zero
  or non-finite 3D distances; deep-copy kernel inputs with native element maps.
  Failed acceptance retains an editable transaction;
  correction or Cancel preserves the source and last committed feature. Validate
  planar/curved directions, tight inward radius, Undo/Redo, source changes,
  downstream consumption, save/reopen and existing 2D controls as one batch.

13.1c/d evidence (2026-10-01):
Both tasks preceded the first grouped PartGui/PartScripts Release build. Four build
attempts were needed for demonstrated defects: the initial compile exposed the
shared solid-shell Thickness form and a shape API type; later native tests exposed
kernel mutation of shared source data, feature-recompute status and resetEdit's
implicit commit before Cancel. Final build exit 0; earlier logs/results retained.
Evidence: `D:\Temp\Office-PC\freecad-plus-sheet-thickening-20261001`.
`grouped-corrected/` passes eight existing sewing checks; after the final Cancel
ordering fix, `thicken-verified/` passes all nine sheet-thickening checks.
**17 distinct selected passes**, zero failures/errors/skips in accepted suites;
native process exits 0. Initial failed aggregates are not acceptance evidence.
Six `visual/` captures reviewed: offset sheet, planar positive/opposite thickness,
curved inward thickness, excessive-thickness refusal and reopened results.
Sheet-Thickening-Sources.FCStd / Sheet-Thickening-Results.FCStd are owner fixtures.
Planar 10 x 8 x 2 mm results measure 160 mm^3 on either side; radius-5/height-10
cylindrical sheet offsets +1/-1 mm produce 110*pi/90*pi mm^3. Inward -6 mm is
refused. Deep native shape copies preserve source BRep data and element maps.
Failed OK remains editable, Cancel restores/removes the native feature correctly,
and Undo/Redo, formula preservation, deferred preview, 2D and solid-shell Thickness
controls pass. Reopened source growth updates the thickened solid and downstream cut.
Part SHA256: `53C9A44F356F8CD8912ED297813A5DA17BEC9636919F14FDB955B73192AD9C72`.
PartGui SHA256: `008DAA38E031E59809DA177CD2A7A66D8063ABD9DD760665158ED434266F8255`.
validated-identities.json and acceptance-summary.json identify exact source/runtime;
the historical About stamp is not this source identity. No installer/release update.
Full F067/13.1 stays open for symmetric/two-sided thickness, graphical normals,
Boolean target collection, compound-sheet filling, broader high-curvature diagnostics,
localization and physical owner acceptance. Stop here for owner testing and rotate.
[Owner procedure](../tests/SheetThickening.md).

- [x] 13.1e Add an explicit review to native Surface Extend Face: source identity,
  independent U/V percentages, fitting tolerance/samples and rectangular-domain
  approximation semantics; preview copied inputs without document mutations (F066).
- [x] 13.1f Reject empty/nonfinite domains and invalid native fits; recompute
  sample/tolerance edits, preserve source geometry and create a separate associative
  feature in one transaction. Validate correction, Cancel, Undo/Redo, source edits,
  downstream use and persistence together. Both tasks passed grouped build/runtime
  validation. Full F066 remains open.

13.1e/f grouped evidence (2026-10-01): enabled the existing Surface workbench in
the local validation configuration (`BUILD_SURFACE=ON`), then completed one
190-second SurfaceGui/SurfaceScripts build, exit 0. The first grouped run passes
nine TestExtendFaceReview, nine TestSectionReview and one inherited
SurfaceTests.TestBlendCurve check (19 distinct selected checks, no skips).
Visual review found internal tessellation lines in the reused face overlay; a
Python-only correction renders an edge compound. All nine affected task checks
pass again in extension-final/, without another native build.
Six visual-final/ captures were reviewed; the earlier visual/ run is retained.
Three FCStd owner fixtures cover source, accepted plane and accepted cylinder.
Evidence: D:\Temp\Office-PC\freecad-plus-extend-face-20261001.

Validated scope: placed planar dimensions/area, quarter-cylinder area/validity,
explicit loss of trim holes in the rectangular fit, source BRep/placement/visibility
preservation, no preview objects/transactions, invalid-domain/tolerance recovery,
changed-input refusal, fault-injected commit rollback/retry, Undo/Redo and
associative source growth through a downstream extrusion and save/reopen.
Native feature/property identities remain unchanged. Source and runtime hashes
are recorded in evidence.json; historical About metadata is not this batch identity.
No installer/release update or owner acceptance is claimed.
Full F066 remains open for true supported untrim domains, associative trim-region
selection, U/V direction handles, measured deviation/self-intersection guarantees,
broad nested/imported/periodic surfaces, localization and physical acceptance.
[Owner procedure](../tests/ExtendFaceReview.md). Rotate pending owner feedback.

- [   ] 13.2 Extend sweep/loft with ordered sections, guides, orientation/twist and
  Boolean targets; implement through-curves surfaces with guides. Reuse 3.6/8.2.
  Through-curves surfaces need section-to-section correspondence controls and twist
  preview, not only guide selection. Shared Sweep/Loft tasks distinguish solid versus
  surface output and show targets/results before commit.
- [x] 13.2a Expose native open-wire/single-edge sections in the existing Loft task,
  with ordered-section and surface/solid/ruled/closed-loop scope review (F063).
- [x] 13.2b Validate current section identities and committed result before one
  undo transaction, retain failed creation for correction, and verify association,
  Cancel, Undo/Redo and save/reopen. Both tasks passed grouped build/runtime checks.

13.2a/b grouped evidence (2026-10-01): both tasks preceded one successful 70-second
PartGui build (exit 0). Eight TestLoftSections checks and nine unchanged
TestSheetThickening checks pass together (17 total, no failures/skips). Native
open-wire/single-edge collection, section reordering with duplicate labels, smooth
surface and ruled output, closed-profile solid, rollback/retry, insufficient/stale
inputs, owner transaction preservation, document close, Undo/Redo and associative
source edits after save/reopen are covered. Evidence:
D:\Temp\Office-PC\freecad-plus-loft-sections-20261001 (grouped/ and build-initial.log).
Capture review exposed a misleading "Valid" detail when open profiles failed to
produce the requested solid. One corrective 60-second PartGui rebuild (exit 0;
build.log) reports invalid geometry or a solid-output mismatch accurately. All eight affected Loft checks pass again (loft-final/); the nine unchanged
companion results are retained, giving 17 accepted distinct checks. The first
corrective verification expected the solid-count message; its assertion was
corrected to the actual native invalid-shape result without a further source change.
All five final captures reviewed (visual-final/): ordered solid/surface modes,
recoverable failure, created surface and reopened source edit. Three owner fixtures
and source/runtime hashes are retained with evidence.json. Source-built validation
is not installer or owner acceptance. [Owner procedure](../tests/LoftSections.md).
Full F063/13.2 remains open for guides, section correspondence/reversal, geometric
and twist preview, continuity/tolerance certification and Boolean targets. Stop
at this bounded checkpoint and rotate pending owner workflow feedback.

- [ X ] 13.2c Make the native Sweep path collector retain its explicit object/edge
  choice independently of later global/profile selection, with identity checks,
  connected-edge validation and visible path/order/output review (F028).
- [ X ] 13.2d Validate native Sweep geometry and requested solid output before one
  undo commit. Keep failed creation editable, preserve owner transactions, support
  Cancel during path capture and close with the document. Verify association,
  downstream use, Undo/Redo and save/reopen.

13.2c/d grouped evidence (2026-10-01): both tasks preceded one 70-second PartGui
build (exit 0). Eight unchanged TestLoftSections checks pass in grouped/; Sweep
checks exposed source topology flag mutation during native wire/pipe construction.
Validation and native Sweep execution now deep-copy inputs with native element
maps before kernel construction. One corrective 60-second PartGui build (exit 0)
and all eight affected TestSweepInputs checks pass (sweep-verified/); 16 accepted
distinct checks, no skips. The document-switch assertion was corrected to native
task closure instead of assuming the task survives a new document.
Retained single/multiple-edge paths, disconnected/stale/replaced input refusal,
source BRep preservation, solid failure/surface retry, owner transaction and Cancel
behavior, Undo/Redo, save/reopen and associative edits through a downstream Link
are covered. All six final captures reviewed (visual/): missing/captured path,
solid creation, reopened path edit, recoverable refusal and surface retry. Four
owner fixtures and source/runtime hashes are retained with evidence.json.
Evidence: D:\Temp\Office-PC\freecad-plus-sweep-inputs-20261001.
Source-built validation is separate from installer and owner acceptance. Full
F028/13.2 remains open for guides, broader orientation/scaling, section reversal,
geometric/twist preview, Boolean targets and unified command-family semantics.
Stop at this bounded checkpoint and rotate pending owner workflow feedback.

- [   ] 13.3 Spike curve-network/boundary surfaces and supported positional/tangent/
  curvature continuity. Measure continuity rather than judging rendered smoothness;
  explicitly limit unsupported inputs instead of assuming a kernel replacement.
  Curve-network surfaces use intersecting curve families; expose positional, tangent and
  curvature boundary conditions only where supported, and validate the claimed
  continuity numerically.
- [   ] 13.4 Complete associative extract/project/intersect curve coverage; retain
  Isocline's explicit draft-angle/direction convention and distinguish isoclines
  from isoparametric curves and display-only analysis. Reuse Phase 5 evidence.
  Associative extraction sources include faces and edges; projection/intersection may
  involve intersecting bodies. Preserve source/update links and the established Isocline
  draft-angle convention rather than silently interpreting it as a different normal-
  angle measure.
- [ X ] 13.4a Add a bounded, nonmutating review of native Part::Section curves from
  two whole root Part shapes/whole root Bodies. Use copied BReps and the existing
  kernel feature in a hidden temporary document; report edge count, total length,
  empty/point-only output and the native approximation choice.
- [ X ] 13.4b Add explicit capture, temporary wire preview and one transactional
  associative creation under Part > Review intersection curves. Recheck identity,
  current geometry and context; invalidate stale previews, refuse empty creation,
  roll back mismatches and preserve source visibility and Body Tips. Verify native
  Undo/Redo, persistence and downstream update; keep the older Section command.

13.4a/b evidence (2026-10-01):
Both tasks preceded one PartGui/PartScripts Release build, exit 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-section-review-20261001`.
Initial grouped checks exposed native Boolean view-provider operand auto-hide;
creation now restores the reviewed visibility in the same transaction. Only the
corrected SectionReview.py was restaged; no second native build. Test fixtures were
corrected to use Part.sortEdges for multiple loops and to compare authored property
values/BReps independently of native transient property-status bits (Content is an
XML fragment). Earlier failed grouped/corrected reports are retained.
`accepted/` passes all nine Section checks; `grouped/` passes nine unchanged sampled
surface-deviation checks. **18 distinct selected passes**, zero failures/errors/
skips in accepted suites; native exits 0. A 10 x 8 mm box/plane intersection has
four edges totaling 36 mm; after save/reopen and changing length to 20 mm it becomes
56 mm, and a 2 mm downstream extrusion changes from 72 to 112 mm^2. Coplanar
boundaries, disjoint/point-only results, transformed multiple loops, whole Body
Tip preservation, Cancel, stale/context refusal and rollback pass.
Six reviewed `visual/` captures cover review/preview geometry, changed input, empty
output, native creation and reopened source editing. Intersection-Sources.FCStd,
Intersection-Result.FCStd and Intersection-Edited.FCStd provide owner fixtures.
PartGui SHA256: `84969A10FE8FA3B3AFB62E5618F09C34BD698D4029917D8503276C67DFA6D0B3`.
validated-identities.json and acceptance-summary.json record exact source/runtime
and accepted evidence; historical About metadata is not the exact source identity.
No installer/release update. Whole F069/13.4 remains open for associative face/edge
extraction, projection, nested/external references, topology repair, richer curve
selection, broader kernel coverage and physical/high-DPI acceptance.
[Owner procedure](../tests/SectionReview.md). Stop here and rotate for feedback.

- [   ] 13.5 Extend Hole wizard, feature/body patterns/mirrors, shell/draft/rib/web
  and fillet/chamfer tools in bounded increments, preserving specialized parameters.
  Hole wizard covers standard holes, counterbores, countersinks, threads and reusable
  position sketches. Unified patterns include linear, circular, curve-driven and table-
  driven placement with skipped instances. Feature/body mirrors distinguish mirrored
  geometry, linked copies and independent results. Fillets/chamfers include tangency
  propagation, variable radii, corner options and localized failure feedback.
  Shell/draft/ribs/webs need consistent tasks and specific geometric failure
  explanations.
- [ X ] 13.5a Expose associative mirror versus independent reflected-shape snapshot
  in the existing Part Mirror task (F057). Reuse native mirroring and preserve source
  geometry/Body Tip. Bound snapshot mode to document-root shapes and whole Bodies;
  snapshots have no source/plane dependencies and do not copy feature history.
- [ X ] 13.5b Make mirror creation transactional and recoverable: reject stale or
  replaced sources, pending edits and missing plane references; abort invalid results
  with inline feedback. Verify asymmetric geometry, source/plane edits, Cancel,
  Undo/Redo and save/reopen for both result choices.
  Both tasks completed before the grouped PartGui/PartScripts Release build.
  First compile failed on TopoDS_Shape versus TopoShape accessor; getShape() correction
  passed, exit 0. All 21 checks pass together in combined-recheck/: 6 new result-mode,
  6 native mirror, 2 existing mirror GUI and 7 command-search; no failures/errors/skips,
  process exit 0. Geometry/handedness, source/plane updates, source Tip preservation,
  snapshot independence, Cancel, rollback/recovery, Undo/Redo and save/reopen pass.
  Five captures reviewed; owner fixtures/procedure: [Mirror result mode](../tests/MirrorResultMode.md).
  Evidence: `D:\Temp\Office-PC\freecad-plus-mirror-modes-20260930`;
  acceptance-summary.json / validated-identities.json record suites and source/native
  hashes. PartGui SHA256: `a6c60e615d42e30f0760ca2de7d89fde709fca505981e3c65007c67de3006d13`.
  Earlier grouped/ retains an incorrect Compound centre-of-mass fixture lookup and
  an access violation when entering command-search. The fixture was corrected;
  separate suites and the full combined recheck pass. The access violation did not
  recur; its cause is unestablished. No application changes after the successful build.
  Whole F057/13.5 remain open for feature reevaluation, nested snapshot coordinates,
  graphical preview and physical/high-DPI acceptance. No installer/release update.
  Stop for owner feedback and rotate.
- [ X ] 13.5c Add native Hole location/specification review (F055): identify the
  profile and owning Body, show the native processed-location count only when
  current, and distinguish it from actual target cuts. Keep failed/pending preview
  state visible without changing source geometry or feature identities.
- [ ] 13.5d Explain clearance, tap-drill, cosmetic and modeled thread results in
  the existing Hole task, retaining native tables and controls. Verify repeated
  counterbores, deferred modeled-thread recompute, Cancel, Undo/Redo, save/reopen
  and downstream source edits. Review implementation is complete; the two acceptance
  blockers below keep this task open.

13.5c/d checkpoint (2026-10-01): both implementation tasks preceded one successful
120-second PartDesignGui build (exit 0). Ten existing PartDesignTests.TestHole
checks pass in grouped/. Seven bounded TestHoleSpecification checks pass in
review-accepted/: profile/Body identities, construction exclusion, current-count
review, clearance/tap-drill/cosmetic semantics, pending modeled-thread disclosure
and Cancel, native invalid-depth feedback, source preservation, counterbore create/
Undo, profile edits and cosmetic save/reopen with a downstream Body Link. This is
17 accepted bounded checks, not completion of the originally attempted acceptance
scope. Initial widget-parent and zero-diameter assumptions were corrected in the
fixtures; native diameter clamps to a supported minimum, so zero depth exercises
actual failure. No additional source change or native build was needed.

Open acceptance evidence, retained separately:
- Deferred modeled-thread task acceptance did not return in hole-verified/ and
  hole-dialog-check/; the isolated validation process was stopped. A bounded probe
  with the actual new review timer disabled also reached its deadline
  (task-refresh-disabled/, one timer found). This rules out its refresh callback
  for that reproduction, but does not establish the underlying cause. Standalone
  native recompute without the task succeeds (modeled-native-probe/), producing a
  valid 96-face, 5535.535590280199 mm3 result. That does not certify task acceptance.
- Counterbore create and Undo return expected geometry, but Redo after recompute
  changed volume from expected 5597.876140340506 to 5607.527112972334 mm3
  (hole-final/). Preserve the mismatch for a focused follow-up; do not mark Redo passed.

All six captures in visual/ were reviewed. Plain-Holes.FCStd,
Counterbore-Holes.FCStd and Cosmetic-Holes.FCStd support owner review;
Native-Modeled-Probe.FCStd is explicitly a task-free geometry probe, not accepted
modeled-thread task output. The counterbore capture shows the inherited head-size
control displaying its previous value after an API parameter edit; physical numeric
control acceptance is not established by these captures. Source/runtime hashes and
publication evidence are recorded in evidence.json.
Evidence: D:\Temp\Office-PC\freecad-plus-hole-specification-20261001. Full F055
also remains open for broader guided placement, versioned standard-table provenance,
drawing callouts, installer and physical owner acceptance. Stop here and rotate
pending owner feedback or a concrete dependency; do not keep polishing this section.

- [x] 13.5e Preserve native fillet/chamfer source topology with element-mapped
  copies before kernel construction. Keep native Base/Edges/EdgeLinks identities
  and associative downstream recompute (F058).
- [x] 13.5f Keep the existing edge task open after failure: validate sizes/current
  source, recompute before commit, roll back failed create/edit and retain checked
  edges for correction. Name the attempted edge set without inventing a uniquely
  failing edge. Verify bounded variable fillet/two-distance chamfer cases, Undo/Redo,
  Cancel and save/reopen together.

13.5e/f grouped evidence (2026-10-01): both implementation tasks preceded one
70-second PartGui Release build (including Part), exit 0. Eight native Loft task
regressions pass in grouped/. Initial edge-treatment fixtures assigned plain
floats to the Base::Quantity property and left native sizes unchanged; correcting
them to QuantitySpinBox.rawValue makes all eight checks pass in numeric-fixture/.
**16 distinct selected checks pass**, zero accepted failures/errors/skips; both GUI
processes exit 0. No implementation correction or second build was needed.
Evidence: `D:\Temp\Office-PC\freecad-plus-edge-treatment-20261001`.
Checks establish two-edge fillet/chamfer failure and retry, BRep source preservation,
no failed-create Undo entry, Undo/Redo, no-edge/zero-size refusal, changed-source
refusal, variable fillet save/reopen/downstream source editing, two-distance chamfer,
failed existing-fillet edit/Cancel, and numeric precision independent of display.
Six visual/ captures were reviewed: retained failed sets, recovered geometry,
variable-radius controls/result and two-distance chamfer. Owner fixtures:
Recovered-Fillet.FCStd, Variable-Fillet.FCStd and Two-Distance-Chamfer.FCStd.
`evidence.json` records exact source/native hashes and accepted results; historical
About metadata is not the source identity. No installer/release publication.
Stop at this working checkpoint and rotate pending owner workflow feedback.

This bounded increment preserves the existing edge/face collector and native
parameters. Tangent-chain controls, live radius previews, corner controls and precise
kernel failure localization remain open. [Owner procedure](../tests/EdgeTreatmentRecovery.md).

- [x] 13.5g Make native Thickness source/removed faces, signed direction and
  current/failed/pending result explicit; retain native face collection and expressions (F059).
- [x] 13.5h Keep failed shell acceptance editable, roll back through Cancel and
  isolate kernel inputs with native element maps. Validate enclosure creation/edit,
  side reversal, face changes, Undo/Redo, persistence and downstream updates together.

2026-10-01 evidence: both tasks preceded one 60-second PartGui build; one corrective
60-second build fixed a displayed pending state after live preview recomputation and
retained the cached-geometry warning after failed acceptance. Both exit 0. Seven final
TestShellThickness checks pass, plus nine unchanged TestSheetThickening checks from
the grouped run: sixteen distinct accepted checks, no skips. Coverage includes native
face reselection/clearing, signed sides, expressions, deferred preview, zero-thickness
and collapsed-wall failure/retry, new/existing Cancel, source BRep preservation,
Undo/Redo, save/reopen and a downstream Refine update. Six final native captures
were reviewed; three owner fixtures are saved in `visual-final`.
Evidence: `D:\Temp\Office-PC\freecad-plus-shell-thickness-20261001`:
`grouped`, `shell-verified`, `final-shell`, `visual-final`, both build logs and
`evidence.json`. The first grouped run retains one failed test assumption: -25 mm
inward on a 30 x 20 x 15 mm box was accepted by the native kernel. The verified
collapse/recovery case is -10 mm. Arbitrary oversized-offset wall correctness is
unresolved, not certified by shape validity. Initial captures are superseded by
`visual-final`. Exact source/native hashes identify evidence; About metadata is
historical. No owner acceptance, installer or release publication is claimed.

Full F059 remains open for Draft, Rib/Web, localized thin-region diagnostics,
oversized offsets, broader geometry and physical owner acceptance.
[Owner procedure](../tests/ShellThickness.md). Stop here and rotate.

- [   ] 13.6 Implement 9.1's history-based face move/offset/replace/delete-and-heal
  on a declared class of native/imported solids; explicit repair limits and preview.
- [   ] 13.7 Spike imported-solid feature recognition only after direct-edit and
  reference foundations pass; record feasibility, bounded supported classes and
  geometry-only/unsupported fallback without claiming recovered original history.
  Target recognition of editable holes, pockets and fillets on suitable imported solids.
  Define recognized parameters and confidence/unsupported cases explicitly; do not claim
  the original feature history has been recovered.

Gate G7 per feature: analytic and difficult supported cases, explicit unsupported
cases, geometric validity, scale-appropriate tolerances and downstream recompute.

## [   ] Phase 14: CAM completion and verification expansion (P8)

Extends Phase 6 and 9.5; retain existing Parallel/Waterline, physical holding tabs
and required two-sided/manually indexed machining. Simultaneous rotary/multi-axis
is later scope, not a reason to defer required indexed setups. No rebuild solely
for this planning adoption.

- [   ] 14.1 Audit mesh-capable algorithms versus BRep-only operations; finish STL
  units/dimension/scaling, normals, orientation, bounds, disconnected-piece and
  strategy-specific validity checks. Add setup wizard for model, WCS, stock, tools,
  boundaries, allowances, tolerance and post. Reuse existing inputs and tab geometry.
  Direct machining must not require converting STL triangles into thousands of CAD
  faces. Mesh preparation explicitly detects holes, inverted normals, disconnected
  regions and unsuitable geometry. Guided setup visibly includes units, orientation and
  work origin alongside stock/tools/boundaries.
- [x] 14.1a Add a bounded imported-mesh review (F091): native topology, dimensions
  and bounds in mm, boundary/nonmanifold edges, connected pieces, inconsistent
  normals, zero-area/duplicate triangles, density and signed orientation for a
  single closed component. Distinguish Parallel/open-surface guidance from Waterline
  contour review. No implicit scale correction, decimation or machining approval.
- [x] 14.1b Offer an explicit independent reversed-normal copy for a reviewed single
  closed inward component, preserving coordinates, placement, source and existing
  job links. Atomic confirmation, owner transaction guards, stale review, Cancel,
  Undo/Redo and save/reopen are validated. Both tasks are ready for owner testing.

14.1a/b grouped evidence (2026-10-01): both tasks preceded one Release PathScripts/
Tests build/staging pass, exit 0; these Python changes require no C++ rebuild.
Initial grouped/ passed all 24 CAMTests.TestMeshMachining checks, including direct-STL
Parallel/Waterline, holding tabs and indexed setups. The new suite initially had
two malformed native vector fixtures and an empty booked-transaction guard failure.
Corrected the fixtures, added an incomplete-topology diagnostic and protected native
booked transactions as well as pending edits. Native Mesh.Volume is absolute, so
orientation uses signed triangle volume; no assumption that positive absolute volume
means outward normals. Only the two Python modules were restaged; no second build.
All 8 TestMeshPreparation checks pass in preparation-verified/, including a real
100,352-triangle fixture, topology defects, placed independent copy, existing model
link isolation, rollback, Undo/Redo, reopen and installed command/lifecycle behavior.
Together with the unchanged CAM suite, 32 distinct selected checks pass across
accepted runs, no failures/errors/skips in the accepted suites and process exits 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-mesh-preparation-20261001`.
Five captures reviewed in visual/ with Mesh-Preparation.FCStd; source/runtime hashes
and unchanged native CAM/Mesh identities are in validated-identities.json, accepted
suites in acceptance-summary.json. The historical About stamp is not this batch's
source identity. Whole F091 and parent 14.1 remain open: root imported meshes only,
200,000-triangle review limit, no self-intersection check, defect highlighting,
per-piece orientation, hole/weld/decimation repairs, unit conversion or setup wizard.
No installer/release update or physical owner acceptance. [Owner procedure](../tests/MeshPreparation.md).

- [x] 14.1c Preserve exact model identity and repeated-source counts in New Job
  and existing-job model selection; distinguish mesh candidates from 2D shapes (F090).
- [x] 14.1d Review source dimensions/placement in mm before job creation, distinguish
  display units from model scaling, and recheck changed/stale inputs on acceptance.
  Preserve native job resources and prove Cancel, Undo/Redo and save/reopen for mesh
  and solid sources. Both tasks preceded the grouped PathScripts staging pass.

14.1c/d evidence (2026-10-01): both tasks preceded one 30-second PathScripts
Release staging pass (exit 0); Python-only changes, no native recompilation.
Evidence: D:\Temp\Office-PC\freecad-plus-job-model-review-20261001.
The grouped run passes all eight unchanged TestSetupTemplates checks and seven
of eight TestJobModelReview checks. Its duplicate-label fixture was automatically
renamed by native preferences; enabling duplicate labels in isolated test
preferences corrects the fixture. No implementation change or second staging.
model-verified/ passes all eight new checks, for 16 distinct accepted checks, no
failures/errors/skips in accepted suites, native process exits 0. Exact identity,
existing-job repeated counts, placed-mesh bounds, unchanged geometry/unit display,
empty/stale/deleted/context refusal, changed-source renewed review, modal Cancel,
native mesh/solid resources, Undo/Redo and save/reopen pass. Six final captures
reviewed in visual-final/: duplicate-label identity, mesh size, changed model,
empty selection, reopened Model Selection and native stock/model. The first visual
run captured an unsettled camera; the final harness waits for native view fitting.
Setup-Sources.FCStd and Reviewed-Mesh-Job.FCStd supply owner fixtures. Source/runtime
hashes and accepted suite locations are recorded in evidence.json. Source-built
verification is separate from installer and physical owner acceptance.
Full F090/14.1 remains open for the full guided sequence, final WCS/parent-world
preview, declared mesh-unit conversion, machine/strategy compatibility and owner
acceptance. Review uses native source geometry, not new WCS or origin semantics.
[Owner procedure](../tests/JobModelReview.md). Stop here and rotate for feedback.

- [   ] 14.2 Add stock-aware roughing then rest machining as separate deliverables;
  finishing drop-cutter paths do not prove either. Preserve holding-tab exclusions
  in all supported cutting/link moves and across indexed setups.
  Provide coherent roughing/finishing strategy presets with visible allowances,
  tolerances and stepovers; rest machining targets remaining stock from preceding
  operations rather than simply repeating a finishing path.
- [   ] 14.3 Complete containment/avoidance, reusable setups, stale-path detection,
  progress/cancellation and large-mesh profiling. Validate transformed source edits,
  units, stock and fixtures; distinguish model refresh from generated-path validity.
  Mesh boundaries include sketch-based containment, selected mesh regions and avoid
  areas. Reusable setup templates cover machines, tools, stock, posts and recurring
  operation sequences. Track geometry, stock and tooling changes separately and mark all
  affected paths stale; the existing missing-input execution fix proves only its
  recorded cases.
- [ X ] 14.3a Prepare the complete selected operation/stock/model/cutter set before
  resetting the existing OpenGL simulator. Validate current geometry, nonempty
  finite paths, native tool profiles and unique cutter identities per tool number;
  preserve saved job order and each operation's native tool-selection sequence.
- [ X ] 14.3b Add visible input/coverage review to CAM Simulator. Show stock in mm,
  selected operations/command counts, cutter numbers/diameters and quality meaning;
  disable Play for failed/empty input, invalidate after edits and require renewed
  review. Clean up observers on Close/document closure. Preserve native model and
  path data and keep Legacy CAM Simulator behavior separate.

14.3a/b evidence (2026-10-01):
Both tasks preceded one PathScripts Release staging pass, exit 0; no C++ source
changes/native compilation. Evidence:
`D:\Temp\Office-PC\freecad-plus-simulation-review-20261001`.
`native-close-verified/` passes all nine simulation-review checks; `grouped/` passes eight
unchanged setup-template checks. **17 distinct selected passes**, zero failures/
errors/skips in accepted suites; native exits 0. The initial native startup check
used a Python wrapper-name assertion; corrected it to query the actual native
CAMSimulator::ViewCAMSimulator. A repeated document-close failure exposed a task
left registered after its document closed; native auto-close now removes it and
its observer. The regression opens a new simulator task after document closure.
Earlier failed grouped/accepted/final-verified reports remain. Only affected Python
files were restaged for owning-document identity, native task closure and saved
operation order changed while the task is open; there was no second native build.
Native startup, source/path preservation, explicit operation selection/order,
stale-stock refusal, complete preparation before reset,
missing later tool, conflicting cutter numbers, profile failure, fresh-review
requirement, per-operation tool submission, save/reopen and observer cleanup pass.
Native AddTool inserts a T command; submission deliberately retains that ordering.
Five reviewed `visual-final/` captures show full review, no selected operations, missing
second cutter, stale inputs and the native simulator view. Simulation-Review.FCStd
and Simulation-Reviewed-Stock.FCStd are owner fixtures. Earlier capture-harness
view API errors remain recorded; the final harness uses supported native view commands. Native startup/rendering is
separate from quantitative material-removal or collision validation; test spies
establish the no-reset/no-feed behavior on preparation failure.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted evidence; the historical About stamp is not the source identity.
No installer/release update. Full F095 remains open for independent stock-removal
accuracy, gouge/collision classification, holder/fixture/machine envelope coverage,
postprocessor/controller behavior, wider model/tool scope and physical acceptance.
[Owner procedure](../tests/SimulationReview.md). Stop here and rotate for feedback.

- [   ] 14.4 Add supported simulation/remaining-stock, gouge and tool/holder/fixture
  clearance checks with visible unavailable checks. Verify a narrow machine/post
  scope and expand strategies/tools/posts only with representative fixtures.
  Simulation is not proof of machine safety or authorization for actual motion.

- [ X ] 14.4a Preflight native CAM setup templates before creating job resources:
  supported format/post/stock/tool data, portable setup expressions and explicit
  name/revision/unit metadata. Keep exact post selection and reject known silent
  fallbacks; preserve native job/model/stock/tool creation and rollback services.
- [ X ] 14.4b Add a read-only template settings review to New Job, with changed-file
  re-review and exact accepted settings. Export editable template names/revisions;
  verify different-model stock sizing, isolated tools, Undo/Redo and save/reopen.

14.4a/b evidence (2026-10-01):
Both tasks preceded one grouped PathScripts build/staging pass, exit 0. Compatible
Python changes use the existing native fork; no native C++ rebuild was needed.
Evidence: `D:\Temp\Office-PC\freecad-plus-setup-templates-20261001`.
`grouped/` passes eight new template checks plus eight existing setup-sheet checks.
After clearer stock-margin/default labels and restoration of an existing UTF-8 log
message, only affected Python files were restaged; `template-verified/` passes all
eight template checks. **16 distinct selected passes**, zero failures/errors/skips,
native process exits 0. Six final `visual-accepted/` captures reviewed: export
metadata, settings/tools, unavailable post, changed-file review and reopened reuse.
`job_metric_fixture.json` and `Reused-Setup.FCStd` are owner fixtures in that folder.
A 12 mm model with X margins 2/3 mm produces 17 mm stock; applying the same template
to a 30 mm model produces 35 mm stock with independent tools/setup and no operations.
Native exact post selection, 600 mm/min feed, metadata, portable setup-sheet
expression rebinding, known-incompatible-input refusal, GUI rollback, Undo/Redo,
save/reopen and later source growth pass. Template edits do not alter created jobs.
The fixture uses an available legacy post and no configured machine; no posted output
or physical machine motion is validated. Full machine compatibility remains open.
validated-identities.json and acceptance-summary.json identify exact source/staged
modules and unchanged native runtime; historical About metadata is not source identity.
No installer/release update. Full F096 remains open for operation sequences and
collector remapping, complete machine/tool asset compatibility, broader reference
repair, localization/high-DPI and owner acceptance. Stop here and rotate.
[Owner procedure](../tests/SetupTemplates.md).

Gate G8: reproducible paths within stated tolerance, supported collision/simulation
checks and independent checks where available; verified post output and explicit
unsupported capabilities. Existing implementation evidence does not close new scope.

## [   ] Phase 15: Inspection, drawing and specialized modules (P9)

Each module depends only on the contracts it consumes and can be delivered separately.

- [   ] 15.1 Unify transient/persistent measurement, units, materials/mass properties,
  interactive/saved sections, interference and minimum-clearance inspection.
  Measurement covers distance, angle, radius, thickness, minimum separation and mass
  properties. Saved measurements retain references and an explicit update policy.
  Sections support multiple planes, saved section views and measurements on sections.
  Interference/clearance results list component pairs, highlight conflicts and let users
  navigate each result.
- [x] 15.1a Extend the existing Measure task with explicit operand identities and
  measurement meaning/frame: circle-centre versus minimum distance, fixed picked
  points, unsigned deltas and geometric-centre versus density-based mass (F098).
- [x] 15.1b Persist explicit fixed-world-point policy, UTC capture time and original
  selection paths for Distance Free snapshots (F099). Preserve native type identity,
  avoid live source links, clear capture provenance after manual coordinate edits,
  and leave old/uncaptured timestamps unknown. Verify save/reopen and Undo/Redo.
- [x] 15.1c Add read-only, explicit solid-pair inspection for F101. Reuse native
  world geometry, common solid volume and minimum distance; classify overlap,
  contact within a stated tolerance, insufficient clearance, clear and unresolved.
  Keep unsupported/unavailable inputs in the report and preserve document geometry.
- [x] 15.1d Expose the bounded pair check in Part with explicit input replacement,
  deliberate exclusions, result navigation and invalidation after model edits.
  Verify analytic overlap/contact/gap, placed links, unavailable inputs and lifecycle.
  Cap this pilot at 12 selected inputs and defer broad assembly traversal/acceleration
  to feedback.

15.1c/d grouped evidence (2026-09-30): both tasks preceded one PartGui/PartScripts
Release build, exit 0. **23 PASS on the first run**, no failures/errors/skips:
7 interference, 9 manufacturing-export and 7 command-search checks; process exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-interference-20260930`, grouped/,
acceptance-summary.json and validated-identities.json. Installed Python scripts match
source; no corrective build or script restaging. PartGui SHA256:
`61bbc89f4924f7c447af2177661090878d43d2b1f5e1468cf776c0eee51b31c4`.
Analytic 200 mm³ overlap, zero-volume contact, 0.25 mm gap, tolerance/clearance
boundaries, rotated Part/direct-Link world geometry, native save/reopen, hidden inputs,
dirty/unavailable/mixed input disclosure, explicit exclusions, pair selection, identity
replacement, edit invalidation and document-close lifecycle pass. visual/ contains
four reviewed captures and Interference-Check.FCStd. [Owner procedure](../tests/InterferenceCheck.md).
Whole F101/15.1 remain open: broader nested/external assemblies, per-pair exceptions,
large-set acceleration/cancellation, persistent reports and physical/high-DPI
acceptance are deferred. No release update. Rotate pending owner workflow feedback.

15.1a/b grouped evidence (2026-09-30): both tasks preceded one MeasureGui Release
build including Measure and changed GUI dependencies, exit 0. **13 selected checks
pass**, no failures/errors/skips in accepted suites: 6 measurement in measurement-final/,
7 unchanged command-search in grouped/. Process exits 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-measurement-20260930`, `acceptance-summary.json` and
`validated-identities.json`. MeasureGui SHA256:
`20ee15fd1b6db168b8320cbec941682dd5c66466ba7ee408810918b37b85c8e1`.
Analytic circle-centre distance (20 mm versus 10 mm edge gap), display units,
occurrence world points/unsigned deltas, geometric-centre density disclosure,
associative source movement, fixed-point metadata, manual-coordinate Undo/Redo,
save/reopen, unknown legacy capture fields and Close pass. `visual/` contains two
reviewed task-panel captures, snapshot-metadata.json and native-only
`Measurement-Context.FCStd`; [owner procedure](../tests/MeasurementContext.md).
The earlier grouped aggregate retains a legacy-fixture XML error: transient property
entries were incorrectly included in persisted Count. Corrected fixture passes;
application code unchanged, no corrective build. Snapshot metadata adds no live
links; timestamps/paths clear on manual point edits and are not invented on restore.
Native identifiers/algorithms remain. Full F098/F099/15.1 stays open for broader
mass/material, thickness, mesh accuracy, stale/invalid associative repair and physical/
high-DPI acceptance. No installer/release update. Stop for owner feedback and rotate.

- [ X ] 15.1e Make existing Clipping View numeric controls describe the displayed
  world-space section: millimetre offsets, synchronized camera-derived normals,
  visible zero-direction pause/recovery and usable planar-fixture steps (F100).
- [ X ] 15.1f Save/load the four native clipping planes in versioned .fcsection
  presets. Capture camera-following orientation as fixed; validate the entire preset
  before applying. Preserve source geometry, document edits and full-model exports.
  Both tasks preceded the first grouped FreeCADGui/FreeCADGui_Resources Release
  build. Three builds total, all exit 0: initial, field-height correction, final
  scrollable-dock correction after visual review exposed parent clipping. All 22
  checks pass together in accepted-grouped/, no failures/errors/skips: 6 section,
  9 temporary-display and 7 command-search; process exit 0. Numeric/camera normals,
  zero recovery, two planes/flip, malformed preset atomicity, failed writes, nested
  Part/direct-Link fixture reopen, owner transaction/Undo preservation and whole
  BREP export pass. Direction fields fit their enclosing controls on the final build.
  Evidence: `D:\Temp\Office-PC\freecad-plus-sections-20260930`;
  acceptance-summary.json / validated-identities.json record accepted suites and
  source/native identities. FreeCADGui SHA256:
  `a5636bf1387c47568b8dd65e2db8ba4467ca4b51b662310ac4de9bd3064e1a11`.
  Six captures reviewed in visual-accepted/, with Section-Housings.FCStd and
  Housing-Section.fcsection. [Owner procedure and preset contract](../tests/SectionPlanes.md).
  Earlier grouped/ retains a wrong Qt widget-name lookup. Earlier visual/sizing
  captures show the layout problem; they are not final acceptance. The default
  image backend omitted clipping; FramebufferObject captures it correctly. Model
  exports remain whole. Presets are separate files, not embedded document views.
  Whole F100 remains open for caps, extracted curves/section measurements, embedded
  views and physical/high-DPI acceptance. No release update. Stop for feedback and rotate.

- [   ] 15.2 Add curvature combs, zebra/reflection lines, continuity and deviation
  inspection with quantitative checks where claimed; support surface validation.
  Deviation inspection includes deviation maps; keep analysis/display distinct from
  constructing new curves or surfaces.
- [x] 15.2a Add a bounded F071 one-way face-deviation calculation using native
  point-to-face distances, explicit sampled/reference roles, UV cell-center sampling,
  known-distance fixtures and reported trimmed-out/singular/failed samples.
- [x] 15.2b Add a nonmutating review dialog and temporary color map, visible mm
  scale and sampling, explicit settings persistence and stale-input/close cleanup.

Both tasks preceded one PartGui/PartScripts Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-surface-deviation-20261001`.
`grouped/` passes nine new deviation checks and seven existing interference checks:
**16 selected passes**, zero failures/errors/skips, native exit 0. Six `visual/`
captures were reviewed: known offset, tilted report/map, changed-face refusal,
reopened report and trimmed-hole report. Known-Offset.FCStd and Tilted-Surfaces.FCStd
are the owner fixtures. Planar and cylindrical fixtures report 2 mm; the tilted
11 x 11 grid reports 0.155463702-3.264737732 mm. The trimmed fixture excludes 25
of 121 UV centers and reports 96 usable samples. Native whole Body results,
world placement, one-way finite-face differences, incomplete native sampling,
source/Undo isolation, saved settings, transaction/stale/context guards, map cleanup,
command activation and save/reopen pass.
Part SHA256: `93D8BCB643EEB020AB1466333DEA84F14BA934C0EF00C2043566111E5AFC8C66`.
PartGui SHA256: `5025C3E75A2D150FEC54B939C6C5DD49510517FF2BCD8AB6C8255F4049BC995A`.
validated-identities.json and acceptance-summary.json identify source/runtime and
accepted evidence; the historical About stamp is not this source identity.
Original tracked newline conventions were restored after build without changing
compiled semantics; InitGui.py was restaged before native command capture.
No installer/release update. Whole F071/15.2 remains open for zebra/reflection lines,
curvature combs, continuity, broader subjects, adaptive/bidirectional or certified
global deviation, reference/report persistence and physical/high-DPI acceptance.
Stop at this functional checkpoint for owner feedback and rotate to another family.
[Owner procedure](../tests/SurfaceDeviation.md).

- [   ] 15.3 Extend 9.4 with drawing setup, projected/section/detail views,
  associative annotations/dimensions and explicit broken-reference repair after edits.
  Provide a drawing creation wizard for standard/projected/section/detail views using
  consistent templates. Associative annotation includes hole callouts and center marks
  as well as dimensions, with explicit lost-reference repair.
- [x] 15.3a Add bounded native drawing setup for one root solid/Body (F102):
  built-in A4/A3 templates, explicit scale/base orientation/projection convention,
  and optional top/right views through the existing TechDraw projection group.
- [x] 15.3b Make sheet creation atomic and reviewable, with source readiness,
  stale/context/fit checks, Cancel and rollback. Validate native associativity,
  projection placement, Undo/Redo and save/reopen; stop for owner testing.
  Both tasks complete for owner testing; grouped build/runtime and visual checks pass.
  Occurrence/external sources, geometric preview, section/detail and annotation
  workflows remain open under F102/F103 and parent 15.3.

15.3a/b grouped evidence (2026-10-01): both tasks preceded one TechDrawGui/
TechDraw_Data Release build, exit 0. All 16 selected checks pass together in
accepted-grouped/, without failures/errors/skips: 7 TestDrawingSetup, one native
projection-group test, one native view test and 7 command-search checks. Process exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-drawing-setup-20261001`.
TechDrawGui SHA256: `f53a78f0b512c8242e534042c1fec5e35b943eaade935ffb05e80c88e48c67e5`.
First/third-angle placement, scale, solid/Body source isolation, native links and
independent source edits after save/reopen pass. Cancel, stale/context/fit guards,
Undo/Redo and rollback after an injected post-page-creation failure pass.
The initial grouped/ also passed, but visual/ exposed sample material/approval text
and a fixed projection symbol in bundled minimal title blocks. DrawingSetup.py now
chooses the existing border-only templates, was restaged without another native
build, and the full selected group passed again. No custom schema or global preference
changes. Section/detail setup, occurrence/external sources, custom templates, graphical
preview, annotation/reference repair and physical acceptance remain open. No installer
or release update. [Owner procedure](../tests/DrawingSetup.md).
Five corrected captures reviewed in visual-accepted/, with Drawing-Source.FCStd,
Drawing-Sheets.FCStd and Drawing-Edited.FCStd. acceptance-summary.json and
validated-identities.json record the accepted source/runtime/native identities.
DrawingSetup.py matches the installed module. Stop here for owner workflow testing;
parent 15.3 and whole F102 remain open.

- [x] 15.3c Repair native drawing dimensions with explicit projected 2D versus true
  3D reference review; clear previous 3D references when returning to projection (F103).
- [x] 15.3d Commit only evaluable repairs, restore original references on failure,
  keep the task open for correction, and preserve Cancel/Undo/Redo/save-reopen.
  Fourteen distinct selected checks pass after one grouped build. Full F103 stays open.

15.3c/d grouped evidence (2026-10-01): both source tasks preceded one successful
TechDrawGui build (351 seconds, exit 0; includes TechDraw core). Seven native
repair checks cover projected/true handoff, read-only review/Cancel, incompatible
reference rollback/retry, no-choice and owner-transaction guards, formatting,
Undo/Redo and source edits after save/reopen. Seven unchanged DrawingSetup checks
also pass. The first persistence test edited during restored-view projection;
the final harness waits for that native asynchronous work before editing, as the
existing drawing tests do. No source rebuild was needed for that harness fix.

Accepted logs: D:\Temp\Office-PC\freecad-plus-dimension-repair-20261001,
repair-verified/ (7 repair checks) and grouped/ (7 drawing setup checks; initial
repair timing failure retained). Five native task captures were reviewed. See
[owner procedure](../tests/DimensionRepair.md). This checkpoint adds reference-list
review, not graphical annotation preview. Hole/thread metadata, automatic
ambiguous-reference repair, broader dimension types and physical owner acceptance
remain open under F103/15.3. Stop and rotate pending workflow feedback.

- [   ] 15.4 Add BOMs, balloons and exploded documentation; validate repeated
  instances, unique copies, suppression, reference-only roles and nested quantities.
  Expose reference-component exclusion explicitly and keep it independent of
  visibility/reference-set contents; exploded documentation must correspond to saved
  arrangements.
- [x] 15.4a Keep native BOM quantity aggregation within each sibling set (F104),
  with per-parent child quantities for repeated modules. Add assembly-group scope
  fallback and checked link casts for mirror classification. Repeated, unique,
  hidden and uniformly mirrored native-link fixtures pass; ready for owner testing.
- [x] 15.4b Add native per-BOM excludedObjects and editor exclude/include controls,
  independently of visibility. Tree selection uses native assembly/document scope;
  linked definitions are not substituted for selected occurrences. Existing task
  transactions preserve Cancel/Undo/Redo; native save/reopen and CSV export pass.
  This is a BOM-local policy, not a new global reference-only component role.

15.4a/b evidence (2026-10-01): both tasks preceded grouped validation. The first
build invocation found no AssemblyGui target because this development configuration
had BUILD_ASSEMBLY=OFF. Enabled BUILD_ASSEMBLY=ON in the existing D: validation
build only; the supplied OndselSolver source was already present and unchanged.
One actual AssemblyGui/AssemblyTests Release build then completed, exit 0, including
its native solver dependency. No separately installed FreeCAD was changed.
Initial grouped/ passed all 13 AssemblyTests.TestCore checks and six of seven new
BOM checks. The remaining test assumed a fixed InList parent order; corrected it
to check membership. The Python picker was aligned to native document-wide tree
roots and actual assembly occurrences, then restaged without another native build.
All 8 TestAssemblyBomScope checks pass in bom-verified/, no failures/errors/skips.
Together with the unchanged core suite, 21 distinct selected checks pass across
accepted runs, process exits 0; the initial aggregate remains recorded as failed.
Evidence: `D:\Temp\Office-PC\freecad-plus-bom-scope-20261001`.
AssemblyApp SHA256: `03682741c90cc84388080773890606b774174e4178605e432f149441f2004010`.
AssemblyGui SHA256: `dd7fe8cbce8d06a129708417342304187ee21a73cbe98c821e7955cb85287656`.
Five captures reviewed in visual/ with Assembly-BOM-Source.FCStd and
Assembly-BOM-Excluded.FCStd. The fixture preserves module quantity 2 / child bolt
quantity 1 / direct bolt quantity 3; excluding two direct occurrences changes only
the direct row to 1. Hidden items remain included until explicitly excluded;
second-BOM isolation, child-definition exclusions, Cancel, Undo/Redo, reopen, native
CSV and creation cancellation pass. acceptance-summary.json / validated-identities.json
record exact suites and source/runtime/native identities. Historical About metadata
is not this source identity. Assembly is now enabled in the local validation build;
earlier disabled-workbench records remain historical evidence.
Whole F104/15.4 stay open for arrays/suppression/configurations, external/unloaded
inputs, individual paths through reused subassemblies, custom-column identity,
persistent balloons, exploded documentation and physical/high-DPI acceptance.
Item numbers regenerate after structure/inclusion changes. No installer/release
update. [Owner procedure](../tests/AssemblyBomScope.md). Stop for feedback and rotate.

- [   ] 15.5 Evaluate/reuse compatible sheet-metal, frames/weldments, hardware and
  profile libraries, delivering independently with configuration/persistence tests.
- [   ] 15.6 Package projects and collect dependencies, repair relocated references,
  and export with stated history/metadata losses. Preserve originals and distinguish
  native document packaging from flattened geometry exchange.

- [ X ] 15.6a Review saved native project dependencies before packaging (F108):
  collect recursive serialized relative XLinks, preserve duplicate basenames and
  expose source/package paths. Refuse missing, unsaved/dirty, absolute-link,
  external file-asset and Python-feature dependencies in this bounded pilot.
- [ X ] 15.6b Create a new portable ZIP with byte-identical FCStd sources, native
  relative directory layout and hashed manifest. Revalidate before atomic publication;
  preserve originals and reject overwrite. Verify relocated nested assembly open,
  source edits/save/reopen and recoverable failures.

15.6a/b grouped evidence (2026-10-01): both tasks preceded one successful
110-second FreeCADGui build (exit 0), including menu/startup registration. The new
Python module was synchronized into the source-built runtime with matching hashes.
Seven TestDependencyInspector checks pass in grouped/; all eight TestProjectPackage
checks pass in package-final/ (15 accepted distinct checks, no skips). Initial
package fixtures were corrected to save external-link owner documents first and
use native GUI save to clear the unsaved flag. No implementation correction or
additional native rebuild was required.
Native nested and repeated links with duplicate source basenames retain their
relative paths and byte-identical documents. The extracted assembly opens with
its original folder moved aside, copied-source edits update both consumers, and
save/reopen retains the edit. Unsaved owner transactions, changed saved sources,
missing dependencies, external file assets, absolute links, overwrite and failed
atomic publication are checked; failures preserve originals and leave no package.
Six captures reviewed: source review, unsaved-change refusal, refreshed review,
created package, relocated assembly and relocated dependency review. Evidence:
D:\Temp\Office-PC\freecad-plus-project-package-20261001; visual/ contains
Portable-Project.zip, the relocated native project and original-unavailable fixtures.
Source/runtime hashes and publication evidence are in evidence.json.
The package preserves identities; this is not Make Unique or format conversion.
Absolute-link repair, independent duplication, add-on/Python code, external assets,
unsupported destination filesystems, installer and physical owner acceptance remain
open. Stop at this bounded checkpoint and rotate pending owner workflow feedback.

- [   ] 15.7 Add reusable manufacturing export presets (X10; [F127](#f127)).
  Make selected geometry/occurrences/configuration, units, orientation and mesh
  quality explicit; audit supported formats and report history/metadata losses.
  Validate dimensions, transforms and tessellation by reimport using T16.

- [x] 15.7a Add the bounded F127 solid-to-STL exporter using existing world-shape
  and mesh services. Explicit input identities, millimeter/world frame, visible
  quality and current-geometry checks precede file creation/replacement. Dimension,
  volume, nested placement and occurrence round trips pass; ready for owner testing.
- [x] 15.7b Add the installed manufacturing-export dialog, reusable per-user
  quality presets/reset, explicit selection replacement and overwrite recovery.
  Menu/dialog, preset, deleted-input and correction checks pass; ready for owner
  testing. Whole F127 remains open for the broader format/configuration portfolio.

15.7a/b grouped evidence (2026-09-30): both implementation tasks preceded one
PartGui/PartScripts Release build, exit 0. All 20 selected checks pass with no
failures/errors/skips: 9 manufacturing-export, 4 named-parameter command and 7
command-search checks; GUI process exit 0. Evidence:
`D:\Temp\Office-PC\freecad-plus-manufacturing-export-20260930`, `export-accepted/` for the final export suite and `grouped/` for the two unchanged suites.
Reimported STL dimensions, volume and transformed occurrence bounds match the
analytic fixtures. Fine sphere approximation improves volume error and produces
10,598 triangles versus 302 Coarse. `visual/` has two reviewed readable dialog
captures, `Manufacturing-Handoff.FCStd`, `Handoff.stl`, `Sphere-Coarse.stl` and
`Sphere-Fine.stl`. Source/runtime scripts match in `validated-identities.json`;
PartGui SHA256: `57a246ae57ef5b199b8e83cac490aec7d570ac2236d82a830ae350a3458d68f0`.
`acceptance-summary.json` records accepted evidence. Final Python-only mixed-compound rejection was staged without another native build.
`export-final/` retains the initial missed rejection; `probe/` confirms the inherited
shape resolver extracts solids from mixed input. The final guard checks source and
resolved shapes; `export-accepted/` passes. No installer/release update. [Test the handoff](../tests/ManufacturingExport.md).
STL uses mm/world coordinates and loses history, colors, units metadata and
assembly identity. Closed-mesh checks do not certify collisions/self-intersection
or printability. STEP/3MF/DXF, configurations/orientation/unit overrides, mesh
inputs, deep occurrence members and physical/high-DPI acceptance remain open.
Stop at this pilot for owner feedback; rotate the next dependency-ready item family.

Gate G9: independently releasable modules update correctly after source/topology
changes, or explicitly report repair/stale state; drawing and BOM references cannot
silently bind to a different entity.

## [   ] Phase 16: Native documents, benchmark evidence and release hardening (P0-P3/P10)

- [   ] 16.1 Extend 7.6 with stable internal `.cadprt` format identity independent
  of branding; schema/producer/minimum-reader/required-capability declarations,
  units/transforms, embedded/external content and definition/file distinction.
  Preserve supported CAD, assemblies, TechDraw, CAM, FEM and other content; preserve
  unknown content safely or refuse unsupported required saves without silent loss.
  Test wrong-type/corrupt files, safe atomic save, backups/recovery, migration,
  Save As/Copy/Make Unique and relocation. Retain best-effort legacy import with
  untouched originals, conversion reports and distinct native/legacy/exchange paths.
- [   ] 16.2 Complete early TechDraw dimension, CAM path, FEM support/load/material/
  mesh/result and Draft consumer adapters exposed by Phase 7. Test units, transforms,
  occurrence identity, source deletion/suppression/topology changes, Undo/Redo and
  reopen; valid attachment or explicit repair/stale state is required. Do not wait
  for new CAM/FEM products to run these existing-consumer probes.
- [ X ] 16.2a Validate a native TechDraw view and projected radius dimension
  referencing an explicit history result: source radius edits, Undo/Redo and
  save/reopen preserve links and the correct numerical dimension. The fixture has
  one analytic projected circle; no general edge naming, removed-reference repair
  or topology-change safety is established. Batch evidence is in 7.1 above.
- [ X ] 16.2b Clear an operation's previous path before a missing job model can
  return from execution. Validate removal after successful SurfaceScan generation
  and regenerated cutting commands after restoring the model.
- [ X ] 16.2c Apply the same early invalidation to missing tool-controller failures;
  restored controller regenerates the path. Preserve the existing frozen-job branch.

CAM invalid-input batch: both regressions reproduced **43 stale machining commands**
before the fix. Shared production `src/Mod/CAM/Path/Op/Base.py` now clears Path after
its frozen-job guard and before input validation. **69 PASS**, no failures/errors/
skips, in `D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-invalid-inputs-20260929-verified\results.json`:
two new cases, 18 PlanarSurface, 22 mesh/tab, 18 avoidance and nine Deburr checks.
Source/installed SHA256: `FE5A146430588CD2B3E5660B2CD9B16B67E6A57EEB12AFD3F5DA079B9BB3227D`;
`module-manifest.json` records matching source/module/test hashes. Python-only install,
no native build or GUI/machine acceptance. The earlier `red` and `final` directories
ran the pre-fix module; `verified` is the completed corrected batch.
This establishes clearing on execution and recovery, not automatic execution after
all history edits, aggregate-job/export invalidation or native failed-producer safety.
Task 16.2 and the broader CAM dependency gates remain open. See the
[regression procedure](../tests/UpstreamIssues.md#cam-invalid-input-paths-roadmap-162b162c).

- [ X ] 16.2d Add hidden native ModelDependencies links to the job model group
  and its geometry for whole-model operations without explicit Base picks. Prove
  document recompute regenerates after model-width edits and clears/rebuilds paths
  when the source becomes empty/returns, without manually touching/executing the op.
- [ X ] 16.2e Restore those links for an older saved operation lacking the property;
  save/reopen and a later empty source must still invalidate the path automatically.

CAM dependency batch: the empty-source case reproduced **43 stale commands** even
with 16.2b/c, because the operation was not scheduled. Shared ObjectOp now binds
ModelDependencies on execution and document restore, preserving existing feature
identities/properties and using additive native LinkList metadata. **72 PASS**, no
failures/errors/skips, in
`D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-dependencies-20260929-final\results.json`.
Coverage: five invalid-input/dependency cases, 18 PlanarSurface, 22 mesh/tab,
18 avoidance and nine Deburr checks. Source/installed Base.py SHA256:
`8F38E250CD73C0B1BF8754BF64CA4879BF509D35C40620520212F780A8ECCC4C`.
`module-manifest.json` records matching hashes. Python-only install, no native build.
The initial probe assumed an aggregate Operations.Path; current Job.setupOperations
creates App::DocumentObjectGroup, so that assertion was corrected to inspect real
operation paths. No aggregate-cache or postprocessor safety claim follows from it.
Remaining: failed upstream producers that skip execution, replacing the job's Model
container, arbitrary selection/occurrence graphs, export guards and frozen-job policy.
The restore fixture is native FCStd; no cadprt or upstream compatibility is asserted.

- [ X ] 16.2f Rebind whole-model operation dependencies when Job.Model is replaced
  or removed; clear old paths immediately for unfrozen jobs and recover through
  normal document recompute when geometry returns. Drop obsolete model links.
- [ X ] 16.2g Restore the wait-cursor decorator to full ObjectOp.execute, correcting
  its accidental placement on the dependency helper in 16.2d/e. Verify generation
  runs with the wait cursor and an exception restores the previous cursor and clears Path.

Container/cursor batch: production Python Base.py and Job.py synchronized into the
existing fork build. `cam-container-20260929-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records 67 passing broader
checks plus seven passing targeted cases and one fixture error (native objects
cannot belong to two groups). After correcting the fixture to transfer membership,
`cam-container-20260929-corrected/results.json` records all eight targeted cases
passing: **75 distinct checks pass across the two runs**, no remaining failures/skips.
Source/installed SHA256: Base.py
`53D660473414228095FC9B4F69132CF11DBB90356251A168AFDFB695AEFB57D6`, Job.py
`16D5377AF2A031543D64B7708E9DABDA04E2CF8239CF6D8216C879CCA09CD2A5`.
No native build, mouse/keyboard acceptance or machine/export safety claim.
Frozen-job preservation remains the existing policy; general failed-producer,
nested-operation and export gates remain pending under 16.2.

- [ X ] 16.2h Refuse post-list creation for dirty native operations or linked
  dependencies, reporting the offending object and requiring recompute. Verify
  dirty operation and dirty source with a clean operation cache, then recovery.
- [ X ] 16.2i Refuse post-list creation after a native producer failure even when
  downstream CAM retains machining commands. Verify failure and repaired-producer
  recovery; retain nested dressup Active/tool/coolant export regressions.

Export-state batch: shared `Path/Post/PostList.py` checks native `State` on each
active operation and its `OutListRecursive` before copying cached paths into a
Postable. All three output ordering strategies use this wrapper; shared legacy
and machine-based exporters consume these lists. No implicit recompute or document
mutation is performed by the guard. Frozen state does not bypass dirty/invalid
export checks; the existing generation freeze behavior remains unchanged.
`D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-export-20260929-verified\results.json`
records **88 PASS, one existing skipped classification test, zero failures/errors**
(11 invalid-input checks, 75 postprocessor checks including the skip, three dressup
checks). The macro's overall `passed` is false because it requires zero skips.
The first grouped run identified dressup tests exporting edited inputs without
recompute; corrected tests recompute before export and preserve their output assertions.
PostList.py source/installed SHA256:
`0C70E6249CF1AEF5BD346CE89B2CB507F750E7F97BD2A07EE702A258B7B2E078`.
Python-only install into the existing fork build, no native rebuild or GUI/machine
acceptance. These guards do not detect silently wrong but clean geometry, missing
references absent from the dependency graph, or external scripts bypassing PostList.
Full 16.2 consumer/export compatibility remains open.

- [ X ] 16.2j Clear nested base-operation and dressup caches when a job Model
  container is removed; prove all paths remain empty through recompute and recover
  after restoring the container, including successful postprocessing.
- [ X ] 16.2k Rebind nested base-operation model dependencies when the container
  is replaced, dropping the obsolete container and recovering paths/export after
  transferring model geometry. Reuse Job.allOperations traversal.

Nested CAM batch: Job.onChanged now visits existing allOperations, binding base
operations and clearing/touching all returned path objects for unfrozen jobs.
The existing native dressuptest.FCStd fixture includes four base operations and
increasingly nested dressups. Two new tests verify removal and replacement/recovery.
`D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-nested-20260929-batch\results.json`
records **90 PASS, one existing classification skip, zero test failures/errors**
(11 invalid-input, five dressup and 75 postprocessor tests including the skip).
Strict overall macro flag is false because of the skip. During missing-model
recompute, Lead-in/Lead-out reports a NoneType.Group error; paths remain empty and
restore/export succeeds. Improving that diagnostic remains pending, as do general
compound/occurrence graphs, frozen-job policy and full consumer compatibility.
Installed Job.py matches source SHA256
`57B42492F1E5CFCC4935D09CC40BCA469E2120B51C6E973C94FFA745FFDBDB33`;
Python-only synchronization, no native build or
GUI/machine acceptance. This closes the two bounded nested-fixture checks only.

- [ X ] 16.2l Stop Lead-in/Lead-out processing when the base Path has no commands;
  return a native empty Path from Boundary for empty input. Verify the nested
  missing-model fixture stays empty without invalid dressup objects and recovers.
- [ X ] 16.2m Clear a Lead-in/Lead-out result before generation, preventing a
  generator exception from retaining old machining commands; verify recovery.
- [ X ] 16.2n Return the placed base path immediately when both lead options are
  disabled; verify exact G-code passthrough without invoking the lead generator.

Dressup input batch: `cam-leads-20260929-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **40 PASS, two existing
linking-generator skips, zero failures/errors** (11 invalid-input, seven dressup,
nine lead-generator and 15 linking tests including the skips). Strict overall
macro flag is false because of skips. The first run exposed Boundary returning a
list for an empty path; correcting it allowed the strengthened native no-invalid-
objects assertion to pass. Prior missing-model Lead-in/Lead-out diagnostics are
resolved in this fixture; ordinary missing-model/empty-boundary log messages remain.
Source and installed hashes: LeadInOut.py
`9F70114D88B5EBAC91119BD2805326A5755C105528BE8811BC738F8FF03AFC63`;
Boundary.py `88DE0133429769A10821AAFE7EE408696502FE4E059176345CD5F2F4AAA674DA`.
Python-only synchronization into the existing fork build; no native build or
GUI/machine acceptance. General dressup failure/consumer compatibility remains open.

- [ X ] 16.2o Clear Boundary dressup output before offset/clipping work so an
  exception cannot leave cached machining commands. Verify both failure stages
  and regeneration after correction using the native CAM fixture.
- [ X ] 16.2p Reject null boundary shapes for both inclusion and exclusion masks;
  keep an empty path and native error state that prevents postprocessing. Return
  a native empty Path for a missing base instead of assigning None. Verify repair
  restores generation/export and missing-base recovery remains clean.

Boundary failure batch: `cam-boundary-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **44 PASS, zero
failures/errors/skips**: 15 invalid-input checks (four new), seven nested-dressup
checks and 22 STL/tab checks. The macro completed with PASS and the test process
ended. Source and development-build Boundary.py SHA256 both:
`1EC5F400DBD2CC116A281FEF24A16F117B1041C3097B546A342216098B2135D0`.
Both implementation tasks were completed before this grouped validation; no native
rebuild was needed. The existing engine reports revision 2df76790b4, with this
Python update synchronized separately. No GUI/machine acceptance or new release;
the published 0.0.1 installer is unchanged. General consumer gates remain open.

- [ X ] 16.2q Mark missing/non-geometric Boundary stock as a native operation
  error instead of logging and returning success. Confirm empty output, export
  rejection, and recovery after restoring the original boundary.
- [ X ] 16.2r Validate boundary offset results before clipping: reject empty
  collections and null/invalid shapes. Inject empty collections/null offset shapes
  for both inclusion/exclusion, assert clipping is not invoked, and verify native
  error/export rejection and recovery with a corrected offset.

Boundary input batch: `cam-boundary-inputs-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **46 PASS, zero
failures/errors/skips**: 17 invalid-input checks, seven nested-dressup checks and
22 STL/tab checks. Macro PASS; test process ended. Source and development-build
Boundary.py SHA256: `E7D4A2BB0D55DA4F1A8BE4CB7F6ADFA783783CAFBA9EB613DADF94BAE6D7CACE`.
Both changes preceded the grouped runtime check; Python-only synchronization, no
native rebuild. Existing engine revision is 2df76790b4. Offset failure injection
validates rejection/recovery, not general offset geometry correctness. No native
GUI/machine acceptance or release update; broader consumer gates remain open.

- [ X ] 16.2s Clear Array output before input checks and generation. Verify
  missing base, explicitly executed empty base, generation failure, export rejection
  for native errors and recovery after correction.
- [ X ] 16.2t Clear Dogbone output and maneuver/bone/tip caches before generation.
  Verify injected generation failure leaves no cached output/markers, blocks export
  and recovers; retain normal corner geometry regression coverage.

Array/Dogbone batch: `cam-array-dogbone-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **49 PASS, zero
failures/errors/skips**: 21 invalid-input checks (four new), four Array checks,
17 Dogbone checks and seven nested-dressup checks. Macro PASS; test process ended.
The initial `cam-array-dogbone-20260930-batch` had 48 passes and one failure:
native recompute skips the Array when its producer fails. The corrected fixture
verifies the existing export guard rejects the cached result, then explicitly
executes Array to validate empty-input cleanup. This is not a fix for eager
invalidation of every skipped consumer; that broader gate remains open.
Source/development-build SHA256: Array.py
`E50D7CB6E317918933D40CA4AF863F85C546D48B83447B8831BC7FEE3153A39F`;
DogboneII.py `9D51B57CAE2083D9E74E31074AD9D161674E1E9F8AE3A7EF7AB4BE36735AB280`.
Both implementations preceded grouped runtime validation; no native rebuild.
The reused engine reports 2df76790b4 with separately synchronized Python updates.
No native GUI/machine acceptance or release update. Dogbone cache failure injection
uses seeded markers; inherited tests separately verify normal corner geometry.

- [ X ] 16.2u Preserve base placement when MirrorAxis is None; validate translated/
  rotated passthrough and unchanged source G-code.
- [ X ] 16.2v Clear Mirror output before generation and assemble KeepBasePath output
  locally before publishing. Validate generation and assembly failures, empty output,
  native error/export rejection where recompute invokes execution, and recovery.
- [ X ] 16.2w Copy placed paths before Mirror transforms or appends commands. The
  identity-placement helper can return the live source Path. Validate combined
  output with identity and translated bases without changing source G-code/state.

Mirror batch: `cam-mirror-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **53 PASS, zero
failures/errors/skips**: 25 invalid-input/workflow checks (four new), seven nested
postprocessing, four Array and 17 Dogbone checks. Macro PASS; test process ended.
The initial `cam-mirror-20260930-batch` had 52 passes and one error: KeepBasePath
mutated the identity-placement base and export correctly rejected its touched
state. Copying the path fixed the production defect; the expanded identity/translated
fixture and recovery/export check pass. Source/development-build Mirror.py SHA256:
`DE48096DDD7D5C54F5FBACA65CDD52DB0F6BFCD28D02C36363D67AAFBF8FBE83`.
Grouped Python synchronization/testing, no native rebuild; reused engine 2df76790b4.
No GUI/machine acceptance or release update. General skipped-consumer invalidation
and broader downstream compatibility remain open.

- [ X ] 16.2x Clear Axis Map output before conversion so arc splitting or mapping
  failure cannot retain an old path. Verify native error/export rejection and recovery.
- [ X ] 16.2y Require finite positive Axis Map radius, with Reverse controlling
  direction. Verify zero/negative rejection and recovery; check all six X/Y-to-A/B/C
  mappings in both directions on linear motion, preserving source G-code.
- [ X ] 16.2z Adapt rotary-post snapshot fixtures to the dirty-input export guard:
  recompute dependencies, assert clean/valid inputs and valid operation, then restore
  and acknowledge only the deliberately injected compound/split test path. Preserve
  production export checks and validate LinuxCNC/Grbl rotary regression expectations.

Axis Map batch: `cam-axis-map-20260930-final/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **44 PASS, zero
failures/errors/skips**: 28 invalid-input/workflow checks (three new), seven nested
postprocessing checks and nine rotary-post regressions. Macro PASS; process ended.
The initial `cam-axis-map-20260930-batch` had 35 passes/nine errors because rotary
fixtures injected paths without clearing their deliberate dirty-output state.
The intermediate `cam-axis-map-20260930-verified` retained 35 passes/nine failures:
new dependency assertions exposed a dirty stock sketch. Explicit fixture recompute
before restoring snapshots resolved that prerequisite without weakening export.
Source/development-build AxisMap.py SHA256:
`A9E44123B1F057B5E7CEB21D510C22EE69E6A39627003A64DE663D022D83D9EE`;
rotary fixture SHA256: `1E721C0B4752F3207BA2EC54C83E776E0D32EC8CB71D1E90309E5111BCDD3290`.
Both production changes preceded grouped validation; only Python was synchronized
into the existing engine (2df76790b4). No native build, new release, GUI/machine
acceptance or new simultaneous-multiaxis capability. General consumer gates remain open.

- [ X ] 16.2aa Clear Z Correction output before execution and the previous
  interpolation surface before reading probe data. Verify missing-file and
  interpolation-failure cleanup, corrected-data recovery, and explicit empty-
  filename placed-base passthrough without an old surface.
- [ X ] 16.2ab Raise native errors for specified missing files, insufficient
  probe points and interpolation construction failures instead of silently
  returning the base path. Verify export rejection and valid-grid recovery.
- [ X ] 16.2ac Reject path points outside the probe area rather than replacing
  corrected output with the uncorrected base. Verify an undersized valid grid
  blocks output/export and a sufficient grid restores the expected correction.

Z Correction batch: `cam-zcorrect-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **48 PASS, zero
failures/errors/skips**: 32 invalid-input/workflow checks (four new), seven nested
postprocessing checks and nine rotary-post regressions. Native four-point grid
fixture produces the expected +0.5 mm cutting correction; missing, insufficient,
collinear, out-of-area and injected interpolation-error cases reject/recover.
Macro PASS; test process ended. Source/development-build ZCorrect.py SHA256:
`A0E10B279DA11FA09BD05FA04061A4D8307D83ED2B633F5699E0A376AC37D3C0`.
All three changes preceded grouped validation. Python-only synchronization into
engine 2df76790b4; no native rebuild, GUI/machine acceptance or release update.
An explicitly empty filename retains uncorrected placed-base behavior. External
probe-file changes require explicit recompute; automatic file monitoring and
arbitrary probe-grid quality remain outside this bounded validation.

- [ X ] 16.2ad Reject NaN/infinite probe coordinates before building a surface;
  identify file/line, leave no old output, and verify rejection/export blocking
  plus recovery for each X/Y/Z coordinate.
- [ X ] 16.2ae Require finite positive ArcInterpolate and SegInterpolate values
  when applying a correction. Verify zero/negative values yield native errors,
  empty output/export rejection, and recovery after restoring valid settings.
- [ X ] 16.2af Use ceiling division for source-line segment counts and include
  both endpoints in the discretization point count. Verify lengths 0.5, 1, 1.01,
  2 and 2.5 mm at a 1 mm setting preserve endpoints and bound source-line spacing.

Numeric Z Correction batch: `cam-zcorrect-numeric-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **51 PASS, zero
failures/errors/skips**: 35 invalid-input/workflow checks (three new), seven nested
postprocessing and nine rotary-post regressions. Macro PASS; process ended.
Source/development-build ZCorrect.py SHA256:
`636A64C32DBB9762352EF22D0B01D55B57551202A6E03F31B7863C519F46B716`.
All three changes preceded grouped validation; Python-only synchronization into
engine 2df76790b4, no native rebuild or release update. Spacing bounds apply to
source lines before height correction; no adaptive corrected-surface chord-error
claim is made. GUI/machine acceptance and broader consumer gates remain open.

- [ X ] 16.2ag Clear Dragknife output before input checks/generation. Verify
  missing/empty base cleanup, generation-failure native error/export rejection
  and regeneration after correction.
- [ X ] 16.2ah Clear Ramp Entry output before validation/generation. Verify
  generator-failure native error/export rejection and recovery with valid feed
  settings; run the inherited ramp-generator suite alongside nested postprocessing.

Dragknife/Ramp batch: `cam-dragknife-ramp-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **52 PASS, zero
failures/errors/skips**: 38 invalid-input/workflow checks (three new), seven nested
postprocessing and seven ramp-generator checks. Macro PASS; process ended.
Initial `cam-dragknife-ramp-20260930-batch` had 51 passes/one fixture failure:
Ramp Entry correctly rejected zero fixture feeds. Explicit positive horizontal,
vertical and ramp feeds resolved setup; no production validation was weakened.
Source/development-build SHA256: Dragknife.py
`C9AC7F3CF16FC374F9B07AB2EECE63F89E1B4A0971335DCFC01ED4E4B8945E13`;
RampEntry.py `BD9A86983A17461E4F302947DCA48D7B6CA9B1BAFC71AB60084C8D1FC5FAF3B5`.
Both implementations preceded grouped runtime validation. Python-only updates to
engine 2df76790b4; no native rebuild, release update or GUI/machine acceptance.
General dragknife geometry and skipped-consumer eager invalidation are not closed
by these bounded failure/recovery checks; broader consumer gates remain open.

- [ X ] 16.2ai Clear Plunge Milling output before generation. Verify injected
  edge-conversion failure removes cached commands, blocks export and recovers.
- [ X ] 16.2aj Reject non-finite/negative/approximately-zero stepover with native
  error state instead of warning and returning success. Verify zero/negative
  rejection/export blocking and recovery after restoring 1 mm stepover.
- [ X ] 16.2ak Audit and replace internal-name-only base lookup with recognition
  of current Path.Dressup proxies. Stop at Path.Op proxies; retain legacy naming
  fallback with native Path::Feature/single-Base-link checks. Validate custom-name
  nested Array/Mirror, restored custom-name Array, legacy links and ordinary
  operation/profile LinkSubList boundaries.
- [ X ] 16.2al Traverse dressup base chains iteratively, detect cycles with stable
  native document/object identity, and return None/default tool for disconnected
  chains. Validate a 1500-node duck-typed chain, a cycle and real missing-link repair.

Plunge Milling batch: `cam-plunge-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **54 PASS, zero
failures/errors/skips**: 40 invalid-input/workflow checks (two new), seven nested
postprocessing and seven ramp-generator checks. Macro PASS; process ended.
Initial `cam-plunge-20260930-batch` had 52 passes/two fixture failures: the inherited
base lookup requires "Dressup" in the internal name. Matching the application
creation convention fixed the fixture; structural lookup remains task 16.2ak.
Source/development-build PlungeMilling.py SHA256:
`109B684C9247EC18DFC62E1234CB81C307E428AA5EA5B9F194FE6954B2A19AD2`.
Both implementations preceded grouped validation. Python-only synchronization into
engine 2df76790b4; no native rebuild, release update or GUI/machine acceptance.
Drilling-cycle semantics and general physical milling suitability are not certified
by these bounded checks; broader consumer gates remain open.

Shared lookup batch: `cam-dressup-lookup-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **84 PASS, zero
failures/errors/skips**: 44 invalid-input/workflow checks (four new), seven nested
postprocessing, four Array, 17 Dogbone, five holding-tag and seven ramp-generator
checks. Macro PASS; process ended. Source/development-build Dressup/Utils.py SHA256:
`1DA658C5E228D8B423C752459646DCD7AD49B539730AC770DACC4BC747B7B6D2`.
Both changes preceded grouped testing. Current proxy namespaces and the legacy
single-link/name contract are covered; arbitrary third-party proxies are not
certified. Cycle/deep-chain tests use duck-typed fixtures; native custom-name,
nesting, missing-link and save/reopen paths are tested separately. No schema change,
native rebuild, GUI/machine acceptance or release update. Python synchronized into
engine 2df76790b4; broader consumer gates remain open.

- [ X ] 16.2am Replace recursive operation-property lookup with iterative traversal
  and cycle rejection. Preserve explicit overrides (including False/None), missing-
  property defaults and tool/coolant/active behavior; validate a 1500-link chain.
- [ X ] 16.2an Make job allOperations traversal iterative and unique by native
  document/object identity. Preserve outer-before-base/group order; handle shared
  bases/cycles without duplicate invalidation. Validate native shared Array bases
  through model removal/recovery and deep/cyclic duck-typed compound graphs.

Shared traversal batch: `cam-traversal-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **151 PASS, zero
failures/errors/skips**: 47 invalid-input/workflow checks (three new), seven nested
postprocessing, four Array, 17 Dogbone, five holding-tag, seven ramp-generator,
21 Path utility and 43 operation-utility checks. Macro PASS; process ended.
Source/development-build SHA256: Base/Util.py
`2EB08E210346860558224801B6654C64A65A2129E39AE9911AABEFE5C05F0F2E`;
Main/Job.py `9FF91E759C2EC4FE1D031118523C19E1C9BC7AA4B5445D6064834E89B8B548B1`.
Both changes preceded grouped validation. Python-only synchronization into engine
2df76790b4; no native rebuild, schema migration, release or GUI/machine acceptance.
Cycle tolerance in job invalidation/cleanup does not validate cyclic models for
machining/export; property lookup explicitly raises when a cycle prevents resolution.
Broader consumer gates remain open.

- [ X ] 16.2ao Preserve parsed probe XYZ precision instead of rounding to two
  decimal places. Validate sub-0.01 mm bounds and a 0.123456 mm height through the
  native interpolation surface and corrected cutting path.
- [ X ] 16.2ap Deduplicate identical XY/Z samples and reject conflicting heights
  at the same parsed XY rather than choosing the first line. Verify both file
  orders, empty output/surface on conflict, export rejection and recovery.

Probe precision batch: `cam-probe-precision-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928` records **65 PASS, zero
failures/errors/skips**: 49 invalid-input/workflow checks (two new), seven nested
postprocessing and nine rotary-post regressions. Macro PASS; process ended.
Source/development-build ZCorrect.py SHA256:
`96D5E1DE0D0AF53F367C682AF326F83C4F267DDF1D0DAA69DFFBF1FD882D7B97`.
Both changes preceded grouped validation. Python-only synchronization into engine
2df76790b4; no native rebuild, schema migration, release or GUI/machine acceptance.
Exact parsed XY duplicates are checked; no averaging or near-point merge tolerance
is implied. Probe-file changes still require recompute; arbitrary surface quality
and broader consumer gates remain open.

- [ X ] 16.2aq Clear the holding-tag dressup's cached Path, tags, solids and path
  data before input validation. Verify removing its base clears output/preview data
  and restoring the base regenerates the tagged path.
- [ X ] 16.2ar Remove untagged-base fallback on holding-tag processing exceptions.
  Clear output, propagate the failure to native invalid state, reject export and
  verify successful recompute after the fault is removed.

Holding-tag failure evidence: `cam-holding-tag-failures-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **56 PASS, zero failures/
errors/skips** (51 CAM invalid-input/workflow, five native tag geometry checks).
Both source changes preceded one grouped run; macro PASS and process ended.
Source/development-build Tags.py SHA256:
`989B0E1B8D79889A4FF532ED7DF55F28D391A6239E09FAF7218DE7FD0DEB47B3`.
The isolated fork engine remains 2df76790b4; matching Python module staged without
native rebuild. Failure injection verifies that a nonempty base remains available
but is not substituted for failed tag processing. This fixes the inherited profile
holding-tag dressup, not the separate stock-bridge geometry feature. No machine,
physical GUI, release or broader safety certification is implied.

- [ X ] 16.2as Clear Boundary2 output before validation/generation so exceptions
  cannot retain old cutting commands. Verify late feed-assignment failure produces
  empty native Invalid output, export rejection and subsequent recovery.
- [ X ] 16.2at Validate Boundary2 offset geometry before clipping: require nonempty,
  valid solids. Verify null and planar offset results reject with empty output,
  block export and recover when restored to a usable boundary.

Boundary2 evidence: `cam-boundary2-failures-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **58 PASS, zero failures/errors/
skips** (53 CAM invalid-input/workflow, five holding-tag geometry checks). Both
changes preceded one grouped run; macro PASS and process ended. Source/staged
Boundary2.py SHA256:
`C71874CC94DF236CA1325338E57E77E5A8734791A9827DD5175F170FF5F672CA`.
Python-only staging into the isolated fork engine 2df76790b4; no native rebuild.
Tests inject a late generation error and native null/plane offset results, then
verify regeneration. This covers Boundary2, distinct from the earlier Boundary
implementation; no machine/physical GUI acceptance or release update is implied.

- [ X ] 16.2au Add shared dressup input readiness checks to Boundary2's base and
  boundary before clipping cached results. Verify explicit regeneration rejects a
  failed recursive boundary dependency, clears output and recovers after repair.
- [ X ] 16.2av Apply the same check to holding-tag base inputs before path analysis.
  Verify cached base-path rejection, empty regenerated output, export blocking
  before/after explicit execution and recovery after repairing the producer.

Dressup readiness evidence: `cam-dressup-readiness-20260930-verified/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **60 PASS, zero failures/
errors/skips** (55 CAM invalid-input/workflow, five tag geometry checks). Both changes
preceded grouped validation; macro PASS and process ended. Initial `-batch` had 58
passes/two failures because native recompute skipped the downstream dressups after
producer failure and retained cached output. Corrected tests explicitly preserve
that observation: existing export guards reject the cache, explicit proxy execution
raises and clears output, and producer repair permits regeneration. Automatic cache
clearing when native execution is skipped is not implemented by this guard.
Source/staged hashes: Utils.py `8CA3B7C1D8B01EB164B812DBBC30C9D8B6DCF7D9CD903E43BF9CC31B1FC5CB11`;
Tags.py `A63513E05806E8C9DC90A40271900233B1EB042E6588DEDAF18FF6C9EDA511C9`;
Boundary2.py `AC903F5E164F68D766ACB096F573E892A5CD3D72F7ECB08A518CCFFAE722FD7C`.
Python-only staging into engine 2df76790b4; no native rebuild, release, physical GUI
or machine acceptance. Direct task callbacks outside execute remain separate audit scope.

- [ X ] 16.2aw Protect direct holding-tag processTags calls: clear old output/solid
  previews and require current base inputs before generation. Verify a createPath
  exception leaves empty output and a later direct call regenerates successfully.
- [ X ] 16.2ax Refresh path data for setXyEnabled and reject stale/missing/unsupported
  base inputs before replacing saved positions. Verify failed upstream dependencies
  preserve Positions/Disabled, clear output/caches and allow correction after repair.

Direct-tag edit evidence: `cam-tag-direct-edit-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **62 PASS, zero failures/errors/
skips** (57 CAM invalid-input/workflow, five tag geometry checks). Both changes
preceded one grouped run; macro PASS and process ended. Source/staged Tags.py SHA256:
`A29DEF69355820C5D8D1482226D774031C5C8AA223E94A4EC3BF4EEC5C6FF383`.
The regression invokes the native proxy methods directly; it is not physical task-panel
acceptance. Native skipped-recompute cache behavior recorded in 16.2au/av is unchanged.
Python-only staging into engine 2df76790b4; no native rebuild, release or machine test.

- [ X ] 16.2ay Clear holding-tag path/tool caches before setup, check base readiness
  and require a tool with positive finite diameter. Verify missing controller/tool,
  zero/infinite diameter leave empty output/caches, block export and recover.
- [ X ] 16.2az Refresh setup for holding-tag point queries and give a clear error
  for unsupported profile paths. Verify both point-query methods reject failed
  dependencies despite previous caches and recover after producer repair.

Tag setup/query evidence: `cam-tag-setup-20260930-batch/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **64 PASS, zero failures/errors/
skips** (59 CAM invalid-input/workflow, five tag geometry checks). Both changes
preceded one grouped run; macro PASS and process ended. Source/staged Tags.py SHA256:
`6D66A11C7979003AB6C75BD934830091B215855E2796C32325434B84D48B44C3`.
Tests use native document/path fixtures with injected controller data and real
producer failures. Queries rebuild path analysis; high-frequency interaction
performance and physical UI acceptance remain unmeasured. Skipped native recompute
behavior from 16.2au/av remains unchanged. Python staging into engine 2df76790b4;
no native rebuild, release or machine acceptance.

- [ X ] 16.2ba Read Boundary2 linking Z from native command Parameters, retaining
  feed moves below safe height. Verify real separated-cut linking, positive plunge
  feed and final clearance retraction.
- [ X ] 16.2bb Return an empty path when boundary clipping removes every wire;
  do not emit a standalone clearance move. Verify empty result and regeneration
  after restoring the boundary.

Boundary linking/empty-result evidence: `cam-boundary-links-20260930-final/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **66 PASS, zero failures/
errors/skips** (61 CAM invalid-input/workflow, five holding-tag geometry checks).
Both source changes preceded grouped testing; macro PASS and process ended.
Source/staged Boundary2.py SHA256:
`E18E7904E0288D1DF3D16CEEAD5F590287EDCEABBF6F0E4D34241D9FE36B549D`.
Initial `-batch` run had 65 passes/one failure because the fixture retained high
links; `-verified` had 65 passes/one failure due to its default zero cutting feed.
Final fixture clips below safe height and sets explicit controller feeds; it wraps
and executes the real linking generator. Production fixes were unchanged between
runs. Python staging into engine 2df76790b4, no native rebuild or release. Physical
GUI/machine acceptance and broad CAM completion remain pending.

- [ X ] 16.2bc Reuse the shared input-readiness guard in Array before generation;
  verify dirty and failed upstream producers cannot regenerate cached cuts, with
  empty output after explicit rejection and successful repair/recompute.
- [ X ] 16.2bd Guard Mirror base inputs before passthrough/transformation and check
  selected center/reference models before reading cached geometry. Verify stale
  base rejection, disabled-axis passthrough rejection, failed reference-offset
  geometry rejection, export blocking and recovery.

Array/Mirror readiness evidence: `cam-array-mirror-readiness-20260930-verified/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **69 PASS, zero failures/
errors/skips** (64 CAM invalid-input/workflow, five holding-tag geometry checks).
Both changes preceded grouped testing; macro PASS and process ended. Source/staged
SHA256: Array.py `5C4C11FDAE1C211EA9F59CC6EE8675ADFB392BEC8CB5B634986A89FDC9B4FFC7`;
Mirror.py `05FFAA6E206617B378B07F6AA0A3333A00730D737BFB88391DE978ED9BD8C920`.
The initial `-batch` run had 68 passes/one error: an older empty-base fixture expected
silent return despite its failed producer. The test now expects explicit stale-input
rejection; production changes were unchanged. That initial run's test hash reflects
the on-disk correction after module import; use the final verified report for evidence.
Native skipped execution may retain an export-blocked cache; explicit execute clears
it and rejects stale inputs. Python staging into engine 2df76790b4; no native rebuild,
release or physical GUI/machine acceptance. Broad task 16.2 remains open.

- [ X ] 16.2be Reject dirty/failed base dependencies before Axis Map conversion.
  Verified explicit regeneration clears
  output on rejection and restores rotary paths after repair/recompute.
- [ X ] 16.2bf Reject stale Z Correction base dependencies and clear interpolation
  surfaces before validation, including missing-base exits. Verified output/surface
  cleanup and successful recovery.

Axis Map/Z Correction readiness evidence: `cam-axis-zcorrect-readiness-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **72 PASS, zero failures/
errors/skips** (67 CAM invalid-input/workflow, five holding-tag geometry checks).
Both production changes preceded one grouped run; macro PASS and process ended.
Source/staged SHA256: AxisMap.py
`06F8ACD543B7C85FA09DB8BD3573A173BBE06FEDF4469776804B06B6F3BA524E`;
ZCorrect.py `1E9F75D9E63CA7CC8BF0197FE7D7F18EBE515B6694D06426D7FC39C984E3CE9F`.
Dirty/failed base producer rejection, export blocking, missing-base surface cleanup
and recovery pass. Native skipped recompute can retain an export-blocked downstream
cache; these fixes clear it during explicit execution. Python staging into engine
2df76790b4; no native rebuild, release or physical GUI/machine acceptance. Broader
CAM consumer/export gates in 16.2 remain open.

- [ X ] 16.2bg Guard Dragknife generation against dirty/failed base dependencies
  using the shared readiness check. Dirty/failed rejection and recovery verified.
- [ X ] 16.2bh Guard Ramp Entry generation against dirty/failed base dependencies
  before consuming cached commands. Dirty/failed rejection and recovery verified.

Dragknife/Ramp Entry readiness evidence: `cam-entry-readiness-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **74 PASS, zero failures/
errors/skips** (69 CAM invalid-input/workflow, five holding-tag geometry checks).
Both changes preceded one grouped run; macro PASS and process ended. Source/staged
SHA256: Dragknife.py `8532EA5CD8655FF59EA94C48CB0B891ACDE21E8A596EB585B3060DE10B52476C`;
RampEntry.py `C779906BCBFDC69D4DE351948D9A0532C11DCA7A9D632BA8EDF05961EFA37EDA`.
Tests verify export rejection for dirty/failed inputs, explicit execution clearing
output and raising, and regeneration after repair. Native skipped-recompute caching
remains export-blocked; automatic cache clearing is not established. Python staging
into engine 2df76790b4; no native rebuild, release or physical GUI/machine acceptance.
Broad CAM consumer/export completion remains open under 16.2.

- [ X ] 16.2bi Guard Plunge Milling against dirty/failed base dependencies.
  Verified explicit rejection, empty output and repair/recompute recovery.
- [ X ] 16.2bj Guard original Boundary base and stock dependencies before clipping.
  Verified stale path/stock rejection, empty output and recovery.

Plunge/Boundary readiness evidence: `cam-plunge-boundary-readiness-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **77 PASS, zero failures/
errors/skips** (72 CAM invalid-input/workflow, five holding-tag geometry checks).
Both changes preceded one grouped run; macro PASS and process ended. Source/staged
SHA256: PlungeMilling.py `E5FF6A073342A20B76F77D703540D53EACB6070B7D4B3F27A11A5183C1F13492`;
Boundary.py `0CAD6DBFD205C0DEF5B27113012EBC67CACEBD75A6E435421B4E540A0AD137BE`.
Dirty/failed base checks and a failed stock producer retaining cached geometry
verify export rejection, explicit generation rejection/cleanup and recovery.
Native skipped-recompute output may remain cached and export-blocked; automatic
cache clearing is not established. Python staging into engine 2df76790b4; no native
rebuild, release or physical GUI/machine acceptance. Full 16.2 remains open.

- [ X ] 16.2bk Reject dirty/failed base dependencies before Dogbone generation.
  Verify empty path/corner caches on explicit rejection and repair/recompute recovery.
- [ X ] 16.2bl Require a Dogbone tool controller/tool and positive finite diameter
  before generating even a path without corners. Verify missing controller/tool,
  zero/negative/infinite diameter rejection, cache cleanup, export blocking and recovery.

Dogbone evidence under `D:\Temp\Office-PC\freecad-plus-validation-20260928`:
`cam-dogbone-readiness-20260930-batch/results.json`: **79 PASS** (74 CAM invalid-input/
workflow and five holding-tag checks); `cam-dogbone-geometry-20260930-verified/results.json`:
**24 PASS** (17 dressup and seven generator geometry checks). Final runs have zero
failures/errors/skips, macro PASS and ended processes. Both production changes
preceded testing. Source/staged DogboneII.py SHA256:
`9B937286874F3841944806C58ACAFD7340538C65E50ED30CCFB66BD46E67F0DF`.
Initial geometry run had 23 passes/one error because a chained-dressup mock lacked
native State/OutListRecursive fields. Clean mock fields were added; geometry behavior
and production changes were unchanged before the successful rerun. Native dependency
failures use real documents; the SurfaceScan fixture does not insert corners, so the
existing geometry suites provide complementary coverage. Skipped native execution
may retain export-blocked caches. Python staging into engine 2df76790b4; no native
rebuild, release or physical GUI/machine acceptance. Broad 16.2 remains open.

- [ X ] 16.2bm Establish Plunge Milling clearance before first XY positioning and
  at completion; retract to safe height between both ordinary and cycle plunges.
  Verified ordinary/cycle command sequences in grouped validation.
- [ X ] 16.2bn Require positive finite vertical feed and put it on each generated
  drilling cycle; cancel each cycle with G80 before subsequent travel.
  Verified cycle feed/cancellation and zero-feed rejection/recovery.

Plunge motion evidence: `cam-plunge-motion-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **82 PASS, zero failures/errors/
skips** (77 CAM invalid-input/workflow, five holding-tag checks). Both source tasks
preceded grouped validation; macro PASS and process ended. Source/staged PlungeMilling.py
SHA256: `6FC91C1FA0FD9617B733AA21A88EE20BB87F36062BB7DC4282E05910E10C1AE4`.
Initial `-batch` had 80 passes/two assertion failures because FreeCAD adds F to rapid
commands; assertions now check the required Z rather than exact parameter dictionaries.
Final source also raises to SafeHeight after cycle cancellation; this was added during
review and verified in the final run. Ordinary plunge and G81 command sequences are
covered; individual peck/dwell variants, controller postprocessing and physical machine
acceptance remain pending. Python staging into engine 2df76790b4; no native rebuild
or release. These bounded fixes do not complete the broader CAM acceptance gates.

- [ X ] 16.2bo Validate Plunge Milling cycle parameters before generation: finite,
  non-negative depth/dwell; finite peck retract; mutually exclusive peck/dwell;
  chip breaking requires peck depth. Implemented; rejection/recovery checks pass.
- [ X ] 16.2bp Verify G82/G83/G73 command parameters, feed, cancellation and retracts,
  plus invalid settings/export rejection and repair. Grouped checks pass.

Plunge cycle evidence: `cam-plunge-cycles-20260930-verified/results.json` under
`D:\Temp\Office-PC\freecad-plus-validation-20260928`: **84 PASS, zero failures/errors/
skips** (79 CAM invalid-input/workflow, five holding-tag checks). Both tasks preceded
grouped testing; macro PASS and process ended. Source/staged PlungeMilling.py SHA256:
`DEF8CC6E1648BA321F80C9B083562A297CFFC8AA581A401338427D9908D39B42`.
G82/G83/G73 verify P/Q/R, feed, cancellation, safe-height retract and final clearance.
Negative dwell, peck+dwell and chip breaking without peck reject and recover. Initial
`-batch` had 83 passes/one failed subtest because native negative PeckDepth assignment
normalizes to zero; the final test verifies that normalization and valid output.
Non-finite checks are defensive source validation, not a claim of exhaustive native
property-domain testing. This closes the bounded command-level cycle variants left
open by 16.2bm/bn; controller postprocessing and physical machine acceptance remain
open. Python staging into engine 2df76790b4; no native rebuild or release.

- [ X ] 16.2bq Validate Plunge Milling peck output through real LinuxCNC and Grbl
  postprocessors: canned-cycle preservation versus expansion, retracts and feed.
  Native peck output passed both real processors in a mock job/configuration wrapper.
- [ X ] 16.2br Verify Plunge Milling cycle settings and regeneration after FCStd
  save/reopen. Settings persist and forced recompute reproduces identical commands.

Plunge post/reopen evidence: `cam-plunge-post-reopen-20260930-batch/results.json`
under `D:\Temp\Office-PC\freecad-plus-validation-20260928`: **87 PASS, zero failures/
errors/skips** (82 CAM workflow/input/export/persistence, five holding-tag checks).
Both verification tasks were prepared before one grouped run; macro PASS and process
ended. LinuxCNC retains G83 peck parameters (Q and R), G80 cancellation
and safe-height climbs; Grbl expands cycles and retains peck/safe/clearance heights.
The saved `plunge-cycle.FCStd` fixture reopens with cycle settings and regenerates
identical path commands. Test SHA256:
`37B7C24A8B1B655C51D3A7EC1113B7275483BB5C951C09EB43E18B4437D5DB86`.
Existing engine 2df76790b4 with previously staged Python fixes; no production changes,
native rebuild or release. This closes only the bounded G83 postprocessor fixture;
other posts/cycle combinations, controller execution and physical machining remain
unverified. Broader CAM acceptance gates remain open.

- [ X ] 16.2bs Repair Holding Tab command creation: use the canonical parent-job
  lookup and the shared owned creation transaction so the task pane can open.
- [ X ] 16.2bt Repair Indexed Setup command creation with the same lifecycle;
  verify cancellation removes created objects and unrelated transactions survive.

Release regression evidence: `D:\Temp\Office-PC\freecad-plus-release-0.0.4\cam-ui-verified`
records **55 PASS, zero failures/errors/skips**, process exit zero (24 mesh CAM,
17 Trim Body GUI, 14 Isocline GUI). Tests invoke the actual CAM commands rather
than bypassing startup. Initial release validation exposed the transaction guard
regression; command-level coverage then exposed both invalid parent-job imports.
Both fixes were staged together into the rebuilt application for the grouped run.
This is automated task-pane acceptance, not physical machining validation.

- [   ] 16.3 Maintain capability audit and patch/upstream map: usable, inconsistent,
  compatible component/add-on, bounded extension or demonstrated limitation. Cover
  auto constraints, projection/intersection, transforms, Links, multi-solids,
  disambiguation, reorder/suppression and mesh CAM; inspect code and actual behavior.
  Preserve completed baseline evidence and identify only missing/invalidated checks.
- [   ] 16.4 Implement the T01-T12 benchmark corpus below, choosing a coherent
  first-release subset plus required downstream probes. Record named builds,
  hardware, fixture parameters/design intent, operator experience, completion and
  recovery/errors/help needs, task time and recompute/open/save/memory. Separate
  learning from practiced work; use repeated trials/medians where useful. Measure
  baseline before improvement/regression thresholds and claims. Use a separate
  source-built upstream baseline, never the ignored installed FreeCAD. Compare
  Fusion/SolidWorks/Onshape only where available; NX informs workflow, not parity.
- [   ] 16.5 Measure full/incremental build, regeneration, loading, tessellation,
  graphics and cancellation costs before optimizing. Define document locking,
  thread safety and result-commit rules before background execution. Keep core
  commands deterministic/scriptable through the same validation as UI.
  Expose reproducible operation recording as well as scriptable commands. Reduced-cost
  previews must be identified as previews and replaced by validated final geometry;
  progress and cancellation remain responsive without committing partial results.
- [   ] 16.6 Maintain release/platform and upstream integration gates; test install,
  launch, open/edit/save/export, migration, older/new files and recovery on supported
  platforms. Verify `.cadprt` filters/icons/installer associations. One Windows
  build is not multi-platform evidence; no public release is implied by a push.
  Keep UI adaptations, new features and object-model changes separable so upstream
  integration does not require one inseparable rewrite. Clearly identify which persisted
  features require the fork; preserve the adopted best-effort legacy conversion policy
  rather than promising unlimited upstream compatibility.
- [   ] 16.7 Audit actual source/dependency/asset licenses, notices, change records
  and branding permissions before distribution. Plan matching tagged source/archive,
  required build/install and applicable linking materials with binaries; verify
  artifact/source correspondence. Keep proprietary competitor code/assets out.
  This is an unperformed release audit, not a legal conclusion or publication order.

- [   ] 16.8 Complete document lifecycle and recovery (X08; [F125](#f125)):
  dirty/read-only state, templates, recent-file repair, safe saves and rotating snapshots.
  Recover into an editable copy while protecting originals; distinguish file identity
  and external-dependency state without claiming atomic multi-file saves. Validate T15.
- [   ] 16.9 Establish an add-on/macro/API compatibility matrix (X09; [F126](#f126)).
  Audit representative extensions, define supported capability/version boundaries,
  adapters and deprecations, and test changed ownership through public APIs. Missing
  required extensions must preserve unsupported content safely or refuse unsafe saves.

G0-G3 remain prerequisite evidence gates: known reproducible fork baseline; recorded
high-impact decisions; minimal mixed-definition/shared-occurrence/unique-copy/local-
cut/split-merge/external-link proof with interactive demonstration; then hardened
services and native/legacy/consumer round trips. Current narrow prototypes do not
close these gates. First architectural release requires G0-G3; first broadly useful
release adds G4 plus a selected G5 increment. G10 additionally requires the promised
workflows, package/source/licensing evidence and accurate compatibility limitations.

Benchmark acceptance targets for 16.4 (all full scenarios pending):

| ID | Task | Required evidence |
| --- | --- | --- |
| T01 | Build and revise a mounting bracket | Guided sketch, Extrude add/cut, dress-up, and editable dimensions |
| T02 | Model an enclosure and separate lid | Multiple bodies, shared dimensions, clear ownership, no accidental merge |
| T03 | Reuse one part three times and in another assembly | Shared source edits and independent placements |
| T04 | Make one occurrence independent | Remapped identity/references; other occurrences remain linked |
| T05 | Move/align parts point-to-point | Correct coordinate context, orientation, preview, cancel, undo |
| T06 | Change an upstream sketch/feature | Correct update or explicit repair; no silent wrong-target attachment |
| T07 | Create a dimensioned drawing | Correct source view/dimension updates after edits |
| T08 | Create/update an existing supported CAM operation | Correct setup/stock/reference scope and invalidated stale toolpaths |
| T09 | Attach FEM material, support, and load | Correct attachment or explicit repair/remeshing/recalculation need |
| T10 | Save/reopen/copy/relocate linked projects | Stable identities, dependencies, missing-file recovery |
| T11 | Download a useful model, change two named dimensions, export for printing | Successful customization without general CAD training; repeat after reopen |
| T12 | Apply constraints to one line, two lines, and a constrained sketch | Correct contextual options and distinct already-applied/redundant/conflict explanations |
| T13 | Drive several features from named expressions, then rename/change display units | Correct dimensional meaning, dependency updates, and rejected cycles/incompatible units |
| T14 | Create and reattach an offset sketch in a rotated component | Explicit local/world placement policy, preserved valid constraints, deliberate reference repair |
| T15 | Recover from an interrupted save using a snapshot | Recoverable editable copy, protected original, explicit external-dependency state and identity |
| T16 | Export a part and selected assembly occurrences using supported presets | Correct dimensions, units, transforms, configuration, mesh quality, and disclosed data losses |

## [   ] Phase 17: Free product onboarding, audience and optional outreach (P11)

Preparation may accompany engineering; public delivery depends on applicable G10
and actual authorization. No advertising, contact, publication, registration or
payment is authorized by this backlog. Distinct naming and revenue are optional.

- [   ] 17.1 Validate audience hypotheses separately: serious hobbyists, small
  engineering/manufacturing teams, recent/lapsed FreeCAD users, experienced users
  and beginners. Refresh primary competitor evidence before targeting decisions;
  distinguish survey population, team size, licenses, downloads and market share.
  Prioritize FreeCAD baseline, Fusion/SolidWorks task comparisons, Onshape workflow,
  with Inventor/Alibre/Solid Edge/Shapr3D/OpenSCAD and NX/Creo/CATIA where relevant.
  Study local/private ownership and commercial-use terms without assuming adoption.
- [   ] 17.2 Create a useful starter model with named parameters/descriptions/units,
  supported ready-to-print STL/3MF, editable `.cadprt` and STEP where appropriate.
  Include required build/version, image, installation/opening path, beginner guide,
  expert shortcuts and T11 customization route. Printing downloads must not require
  installing the CAD app. Candidate models: brackets, organizers, enclosures,
  drawer/mounting interfaces, RC receiver mounts, battery trays and workshop fixtures.
- [   ] 17.3 Prepare model-led distribution using existing owner model audiences:
  Thingiverse/Printables-compatible uploads, allowed archive or source links if
  `.cadprt` uploads are unsupported, never disguised FCStd files. Prepare one
  60-90-second demonstration, complete tutorial and landing page joining model,
  application download, tutorial and compatibility/support information. Advertise
  useful outcomes and only measured savings; preserve familiar command names.
- [   ] 17.4 Prepare bounded channel experiments: relevant Facebook maker/RC/CNC/
  printing groups, short videos/YouTube, FreeCAD communities/forums, independent
  small creators, searchable tutorials/comparison pages, makerspaces/robotics clubs,
  and later maker publications such as Hackaday. Respect community rules; test
  channel value rather than assuming rankings. Obtain authorization before outreach.
- [   ] 17.5 Measure discovery, trial, installation, first successful customization,
  voluntary return/second independent project, migration and support burden
  separately. Use consented feedback/referral data, no undisclosed telemetry.
  Refine beginner/expert friction using authorized observation; views/downloads or
  enthusiasm do not prove adoption. Revisit effort/support capacity with evidence.
- [   ] 17.6 Prepare independent-fork positioning: upstream credits, workflow/object
  differences, native/import/export limits, add-on/macro compatibility, support
  destination and maintenance status. Optional: evaluate a distinct public name
  before broad incompatible release, preserving built-on-FreeCAD acknowledgment and
  stable format identity. No approved rename or upstream endorsement is implied.
- [   ] 17.7 Optional after format specification: public `.cadprt` description,
  samples/icons, FileInfo submission and proposed IANA media type. Recheck naming,
  availability/process/fees before action; no assigned MIME type or exclusive
  extension ownership is claimed. Required OS association remains 16.6.
- [   ] 17.8 Deferred unless explicitly revisited by the owner: paid packaged
  distribution, support/training, hosted storage/collaboration/backups/computation,
  sponsored development or independent extensions. Reconsider only against real
  adoption/maintenance evidence and applicable code/licensing boundaries. No billing,
  subscription, activation or paid core gates; optional hosted services must not
  become prerequisites for ordinary local modeling.

Gate G11: release candidate, starter source/exports, tutorial and compatibility
notes agree; representative users complete T11. Outreach is reviewable before
publication, and repeated campaigns need evidence. Optional branding, registration
or revenue cannot delay a usable free modeling release.

## Pre-release 0.0.2

- [ X ] Build the requested Windows installer with 0.0.2 version metadata, its own
  installation directory, shortcut and uninstall registration. Reuse the existing
  native Release build rather than recompile unchanged application sources.
- [ X ] Freshly stage and compare all **14,584 runtime files** with the 0.0.4
  payload. All SHA256 hashes match; reuse the **312 passing** model/task/CAM tests
  recorded for that identical application. These regression tests were not rerun.
- [ X ] Install the actual 0.0.2 `.exe`; all **14,586 installed files** match its
  payload. Launcher, isolated upstream settings, workbenches and FCStd save/reopen
  checks pass. FreeCAD Plus versions share their fork-specific settings.
- [ X ] Verify shortcut/version registration, then uninstall successfully while
  retaining an unrelated user file. Disposable test installation removed.
- [ X ] Publish GitHub pre-release 0.0.2 with exactly one Windows installer asset;
  verify source tag, public pre-release state, size and SHA256.

Published 2026-09-30 07:43:25 UTC:
[FreeCAD Plus 0.0.2](https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.2),
release ID **399816257**. Application/runtime source:
`802e19d64863ecdfc02817a2160b621579c2d8f2`; packaging/tag source:
`71358d8fbf40122e6c998008e7ab3ca741dbc773`. Engine remains 26.3.0.
Artifact: `FreeCAD-Plus-0.0.2-Windows-x64-Setup.exe`, **356,439,411 bytes**, unsigned.
SHA256: `69d9b406904bb49c22f1efddc1769bae10147edbe38ae0bc1c8993796bb0ddfe`.
GitHub confirms `draft=false`, `prerelease=true`, one matching asset. This requested
version was published after 0.0.4 and contains the same application feature set;
existing releases were not changed.

Evidence root: `D:\Temp\Office-PC\freecad-plus-release-0.0.2`:
`runtime-equivalence.json`, `package.log`, `install-results.json`,
`installed-validation/results.json`, `uninstall-results.json`,
`github-published.json` and `github-tag.json`. Reused native build/test evidence is
under `D:\Temp\Office-PC\freecad-plus-release-0.0.4` (`build.log`, revision logs,
`payload-final/results.json`). [Release notes](releases/0.0.2.md) record the focused
workbench set and limitations. Clean-VM, full manual GUI, controller/machine and
broader roadmap acceptance remain open. No `.cadprt` or production NX-history
implementation is claimed.

## Pre-release 0.0.4

- [ X ] Build the existing focused Windows x64 Release configuration after the
  accumulated roadmap batches; full native build exit 0. Refresh/relink Version.cpp
  after the final Python CAM fixes so the embedded identity matches release source.
- [ X ] Correct Holding Tab/Indexed Setup command startup (16.2bs/bt). Grouped
  command/transaction regressions: 55 passes. Final packaged run: **312 PASS** across
  22 model/task/CAM suites, zero failures/errors/skips, application process exit 0.
- [ X ] Package and install the actual Windows installer in an isolated directory.
  All **15,532 installed files** match the payload. Installed launcher, separate
  settings, module/workbench availability and FCStd save/reopen checks pass.
- [ X ] Verify version registration and Start-menu shortcut, uninstall successfully,
  remove application/shortcut/registration, and preserve an unrelated test file.
- [ X ] Publish GitHub pre-release 0.0.4 with exactly one Windows `.exe` asset;
  verify public state, source tag and uploaded SHA256 digest.

Published 2026-09-30 07:17:39 UTC:
[FreeCAD Plus 0.0.4](https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.4),
release ID 399799828. Source, embedded runtime and tag commit:
`802e19d64863ecdfc02817a2160b621579c2d8f2`; engine version remains 26.3.0.
Artifact: `FreeCAD-Plus-0.0.4-Windows-x64-Setup.exe`, **360,831,616 bytes**, unsigned.
SHA256: `e5ea99f9b3e556c65f6dadcc5ade42eb4e2531b79f55ae5757ec9eec891e7464`.
GitHub confirms `draft=false`, `prerelease=true`, one matching installer asset.

Evidence root: `D:\Temp\Office-PC\freecad-plus-release-0.0.4`:
`build.log`, `final-version-compile.log`, `final-version-link.log`,
`package-verified.log`, `cam-ui-verified/results.json`, `payload-final/results.json`,
`install-results.json`, `installed-validation/results.json`, `uninstall-results.json`,
`github-published.json` and `github-tag.json`. Initial packaged tests exposed two
CAM creation errors; command-level regression then exposed invalid job-lookup imports.
These failures were fixed and the full final run passed. Earlier packaging attempts
were intentionally stopped to include revision and source corrections; they are
not accepted artifacts. The initial interrupted test run does not supersede final
validation. [Release notes](releases/0.0.4.md) document included workbenches and limits.
No clean-VM, full manual GUI, controller or physical-machine acceptance is claimed.
Planned `.cadprt`, production NX-like history and parameter-editor prototypes remain
outside this installer; their roadmap tasks remain open.

## Pre-release 0.0.1

- [ X ] Build current application source `2df76790b4` in Release configuration and
  stage a self-contained Windows x64 runtime outside the source tree. Full build
  completed successfully. Refresh/relink Base/Version.cpp because incremental
  metadata still reported `8abce719de`; final launcher reports `2df76790b4`.
- [ X ] Package a per-user NSIS installer with a distinct FreeCAD Plus registration,
  Start-menu entry and launcher settings directories. Preserve native identities,
  upstream installation, file associations, licensing and unrelated files.
- [ X ] Validate 120 model/task/CAM cases against the staged runtime, zero failures,
  errors or skips. After revision-only relink, staged and installed launcher smoke
  checks pass: native imports, workbench inventory, isolated settings, save/reopen.
- [ X ] Install the actual artifact silently, verify 11 key installed hashes and
  registration, check shortcut target, uninstall and verify application/shortcut/
  registration removal while retaining an unrelated user file. No clean-VM or
  hardware cutting acceptance is claimed.
- [ X ] Publish GitHub pre-release `0.0.1` with only the Windows installer asset;
  verify public pre-release state and uploaded artifact digest.

Evidence root: `D:\Temp\Office-PC\freecad-plus-release-0.0.1`.
Records: `build.log`, `version-compile.log`, `version-link.log`, `package-final.log`,
`payload-validation/results.json`, `launcher-validation/results.json`,
`install-results.json`, `installed-validation/results.json`, `uninstall-results.json`.
Artifact: `FreeCAD-Plus-0.0.1-Windows-x64-Setup.exe`, 360,754,930 bytes, unsigned;
SHA256 `c969fb92aea4cbd4da400d78dfb18d3674de16ebb68d9a4432f3f1bcc1b33dd8`.
[Release notes](releases/0.0.1.md) list included/omitted workbenches, compatibility
limits and the distinction between fork version 0.0.1 and engine version 26.3.0.
[Packaging procedure](../package/WindowsInstaller/FREECAD_PLUS_RELEASE.md).

Published 2026-09-30 02:42:23 UTC (2026-09-29 local):
[FreeCAD Plus 0.0.1](https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.1).
Release ID 399674768, target/tag commit `1a962bb23da3795adc2b4c10c59b8218aea2fe9e`.
Verified `draft=false`, `prerelease=true`, exactly one asset, 360,754,930 bytes, and
GitHub asset digest matching the tested installer SHA256 above. Application source
remains `2df76790b4`; the tag additionally contains packaging/tests/release documentation.

## Re-updated objective specifications and delivery slices

Source: owner-supplied `RE-UPDATED_FREECAD_PLUS_DEVELOPMENT_ROADMAP.md`, reconciled
2026-09-29. The [item-level catalogue](#item-level-product-specifications-f001-f127)
retains all 127 goals, workflow descriptions and completion examples. F001-F111
expand the original inventory, F112-F121 capture later product decisions, and
F122-F127 add supporting requirements. The package coverage table and owning tasks
above remain the execution/status index; this catalogue adds acceptance detail.

This is a specification reconciliation, not feature implementation, a build, or
validation. Existing completed task records and the 0.0.1 release remain unchanged.
No catalogue item is newly declared complete. Read each item with its owning tasks:
existing bounded implementation/prototype evidence applies only to its tested scope;
unproven portions remain pending. Embedded agent rules, startup tasks, repository
reorganization and publication instructions from the supplied file are not adopted.
Market assertions and source citations are planning inputs, not newly verified facts.

Established decisions take precedence over ambiguous source wording: the Operation
field stays first; active command collectors accumulate picks, while ordinary click,
Ctrl and Shift retain the established selection semantics. Automatic body/mode
suggestions occur only at creation, with accepted intent persisted for recomputation.
Isocline uses the approved draft-angle convention (Phase 5), not a substituted raw
normal-vector angle. Required two-sided/indexed CAM and holding tabs remain in scope;
initial three-axis finishing is only a delivery increment. `.cadprt` remains planned;
0.0.1 still uses `.FCStd`. Benchmark comparisons use a separately scoped upstream
source build, never the installed upstream application. The roadmap does not itself
authorize implementation of every future capability or external publication.

### Dependency contracts added by the expanded specifications

- Definition/occurrence/document identities precede shared assembly reuse, Make
  Unique, replacement and configuration-aware copies (7.1, 12.1-12.2, 16.1).
- Feature provenance and stable references precede region selection, rollback,
  repair and reliable downstream consumers (7.1.4, 7.5, 11.6, 16.2).
- Parameter scope, dimensional units and cycle rules precede broad expression fields,
  configurations and published dimensions (10.8, 12.5, 12.7).
- Edit context, selection eligibility and sketch coordinate/reattachment policies
  precede shared collectors, contextual constraints and precise moves (10.4-10.7,
  11.2, 11.7). Prove local/world placement in a rotated occurrence.
- Transactions and preview invalidation precede shared command lifecycles, scripting
  and background results; stale work must not commit (8.1, 16.5, 16.9).
- Native save/copy/recovery and external-reference contracts precede format migration,
  project packaging and extension compatibility (7.6, 15.6, 16.1, 16.8-16.9).
- Downstream adapters must retain correct engineering references before production
  claims for TechDraw, CAM, FEM or Draft. Export boundaries explicitly distinguish
  native documents from geometry exchange (15.7, 16.2).

Use narrow probes before broad UI: one unit-aware parameter drives two features,
rename propagates and a cycle is rejected; sketch reattachment proves its coordinate
policy; recovery-as-copy preserves identity rules and the original. General feature
recognition, full configurations, simultaneous multiaxis CAM, cloud services and a
kernel replacement are not prerequisites for these contracts.

### Incremental product release slices

These are candidate capability slices, not dates, release authorizations or claims
about the published 0.0.1 installer. Dependencies govern ordering; independent
modules can ship separately after their applicable evidence gates.

| Slice | Minimum useful capability | Evidence before claiming the slice | Explicit later scope |
| --- | --- | --- | --- |
| R0: internal architecture proof | Mixed part definition, shared occurrences, part-level Extrude/cut, persisted identity; narrow parameter/document contracts | G0-G2 and early engineering-consumer probes | Polished UI and broad migration |
| R1: useful free modeling preview/beta | Navigators, guided/direct Extrude and Revolve, aliases, modifier selection, contextual constraints, precise moves, native-save/basic export | G3-G5 selected scope, G10-G11; T01, T02, T05, T10-T12 and architecture/legacy/consumer evidence. Constraint subset covers one/two lines, conflicts, redundancy and commit validation | Advanced surfaces, full configurations, recognition and complete CAM |
| R2: dependable assembly reuse | Instances, Make Unique, replacement, reference sets, mates and interpart links | G6; T03, T04, T06 plus reference repair and persistence | Broader configuration/loading increments |
| R3: modeling depth | Selected trim, thicken, holes, dress-ups, sweep and loft increments | G7 fixtures for each delivered operation | Arbitrary curve networks and general recognition |
| R4: mesh CAM | Finishing first, then separately validated rough/rest machining; preserve the required indexed/two-sided and tab roadmap | G8 for each operation with stated post, simulation and collision scope | Simultaneous multiaxis and any universal machining-safety claim |
| Independent downstream slices | Drawing, inspection, BOM, sheet metal and frames as bounded modules | G9 and relevant consumer/persistence evidence | Undelivered module capabilities |

A narrow prototype does not promote an entire slice to complete. Build and validate
coherent groups of changes as already requested, recording source, automated tests,
GUI acceptance and publication separately.

## Item-level product specifications (F001-F127)

Each entry preserves the supplied goal, workflow and completion example; the owning
roadmap tasks establish status and implementation boundaries. Source P-phase labels
and scope estimates are planning metadata, distinct from this roadmap's task numbers.
?Complete when? states required evidence, not evidence already obtained. Apply the
reconciliation rules above to every entry.

<a id="f001"></a>
### F001 — Unified part container

**Owning tasks:** 7.1, 12.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A01 · **First delivery:** P1/P2 · **Likely scope:** Core

**Goal:** Let a user start modeling a part and later add components without changing its fundamental object type.

**Workflow and behavior:** A definition contains its own sketches, datums, features, solid/sheet results, and child occurrences. Add Component adds an occurrence to that definition; it does not convert its geometry into a different assembly-only class. Distinguish structural children from feature inputs and keep child transforms explicit.

**Complete when:** Create a housing with its own geometry, insert a bearing and fastener, then insert the complete housing into another part. Edit the housing and reopen the project without duplicate transforms or ownership changes.

<a id="f002"></a>
### F002 — Part-level feature history

**Owning tasks:** 7.1, 7.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A02 · **First delivery:** P1/P2 · **Likely scope:** Core

**Goal:** Make the part's modeling sequence the primary history so features can act across several bodies.

**Workflow and behavior:** Create features in the work part and collect input geometry and target bodies explicitly. A sketch can drive multiple features; the active or last-visible body is not an implicit destination. The visible history represents an executable dependency order, while organizational folders remain presentation only.

**Complete when:** Create two solids, cut both with one part-owned feature, and edit an earlier sketch. The navigator, dependency graph, results, undo, and saved document agree about ownership and execution order.

<a id="f003"></a>
### F003 — Independent body results

**Owning tasks:** 7.1, 7.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A02 · **First delivery:** P2/P3 · **Likely scope:** Core

**Goal:** Create a solid or sheet without first preparing an active PartDesign Body.

**Workflow and behavior:** A geometry-creation command accepts valid profiles and datums in the part and produces one or more identified body results. Expose whether the selected input makes a solid, sheet, or several disconnected results. A Unite feature may use temporary tool geometry without leaving an extra permanent tool body unless Keep Tools is selected.

**Complete when:** Create two disjoint profiles in a new part and produce independently selectable/editable results. Save/reopen preserves their identities and a later Boolean operation can target either result.

<a id="f004"></a>
### F004 — Explicit Boolean mode

**Owning tasks:** 7.4, 10.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U03, U10, A02 · **First delivery:** P2/P4 · **Likely scope:** Feature/Core

**Goal:** Use the same modeling command to create independent material or alter selected existing material.

**Workflow and behavior:** Present New Body, Unite, Subtract, and Intersect where supported, with targets highlighted separately from profiles/tools. Apply tasks 7.4 and 10.3's contextual initial suggestion and sticky manual choices. Mode conversion edits the feature when supported; unsupported legacy conversions require a clear migration path. Validate topology as well as spatial intersection.

**Complete when:** Exercise every supported mode, change one feature's mode, and test missing targets and invalid contact. Accepted operation and target identities survive recompute and reopening without being inferred again.

<a id="f005"></a>
### F005 — Multiple targets

**Owning tasks:** 7.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A02, A07 · **First delivery:** P2/P3 · **Likely scope:** Core

**Goal:** Apply one coherent operation to several selected bodies without duplicating setup.

**Workflow and behavior:** Collect an ordered target set, preview each affected result, and define per-command semantics: a cut can modify each target separately, while a unite may produce combined results. Specify whether tools are retained and which results replace which inputs. Commit all supported targets atomically; any explicit partial-success mode must show exactly what will be skipped.

**Complete when:** A cut through two solids updates both after a profile edit. An invalid target causes a clear, reversible failure rather than a partially committed document or silent target omission.

<a id="f006"></a>
### F006 — Persistent body identity

**Owning tasks:** 7.1.4, 7.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A05 · **First delivery:** P1/P3 · **Likely scope:** Core

**Goal:** Keep intended relationships understandable when a feature splits, merges, or replaces bodies.

**Workflow and behavior:** Separate stable document identifiers from labels, output position, and transient kernel topology. Record provenance and explicit identity rules for surviving, split, merged, and deleted results. If more than one new result could satisfy an old reference, retain the unresolved reference and offer repair instead of guessing.

**Complete when:** A downstream feature, drawing reference, and assembly use remain correct through supported splits/merges, or report the exact ambiguity. Renaming a body or sorting the tree does not change identity.

<a id="f007"></a>
### F007 — Reusable sketches and datums

**Owning tasks:** 7.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A01, A02, S05 · **First delivery:** P2/P5 · **Likely scope:** Feature

**Goal:** Use one design input in several features without copying geometry merely to satisfy ownership restrictions.

**Workflow and behavior:** Keep sketches, planes, axes, points, and coordinate systems identifiable at part level. Consuming a sketch may change a visibility preference but does not transfer ownership or prevent reuse. Show its consumers and distinguish using original geometry, selecting a closed region, projecting geometry, and making an independent copy.

**Complete when:** One sketch drives two extrusions and a datum drives a revolve. Editing the shared input updates all intended consumers; deleting it previews affected features and supports cancellation.

<a id="f008"></a>
### F008 — Promote bodies to components

**Owning tasks:** 12.2. **Status:** Promotion workflow acceptance remains pending. The Make Unique pilot is tracked under F019; copying an existing occurrence definition does not establish body promotion.

**Packages:** A03 · **First delivery:** P3/P6 · **Likely scope:** Core

**Goal:** Turn bodies modeled together into reusable component definitions with deliberate design relationships.

**Workflow and behavior:** Select bodies, choose new part names and grouping, and choose associative derived parts or independent copies. Preview which sketches/datums or source references remain in the original definition. Place resulting occurrences so the assembly geometry does not jump. Prevent cycles and avoid duplicating ownership of the same editable result.

**Complete when:** Promote an enclosure and lid, reuse the lid elsewhere, and edit the original. Associative and independent modes behave as declared; placement, internal references, undo, and relocation remain correct.

<a id="f009"></a>
### F009 — Separate navigator tabs

**Owning tasks:** 7.2, 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U01 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Separate assembly structure from modeling history without forcing users to interpret a mixed tree.

**Workflow and behavior:** The Assembly Navigator shows occurrences and hierarchy; the Feature Navigator shows the work part's inputs/history/results. Switching tabs preserves relevant expansion, selection, scroll, and filter state. Selecting a tree item highlights the corresponding occurrence or feature in the viewport, with definition versus occurrence context explicit.

**Complete when:** A repeated component is selected through its exact occurrence in the assembly tab; switching to its feature tab reveals the correct definition and does not accidentally change the work part.

<a id="f010"></a>
### F010 — Optional simultaneous display

**Owning tasks:** 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U01 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Let users see structure and feature history together when screen space and the task justify it.

**Workflow and behavior:** Support docking/splitting the two navigator views independently while keeping one selection/context service. Remember layouts per user, provide a reset, and accommodate small screens and high DPI. Closing or moving a panel must not alter model state or leave duplicate active edit contexts.

**Complete when:** Dock both navigators, edit a nested component, switch work parts, then restore the default layout. Both panels stay synchronized and keyboard focus remains predictable.

<a id="f011"></a>
### F011 — Work part versus displayed assembly

**Owning tasks:** 10.6, 12.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A04, U01 · **First delivery:** P1/P4 · **Likely scope:** Core/UI

**Goal:** Make it unmistakable where a new feature will be created while the surrounding assembly remains visible.

**Workflow and behavior:** Provide explicit Set Work Part/Edit Component and Return to Parent actions, a breadcrumb or equivalent context indicator, and restrained highlighting of editable versus contextual geometry. Selecting a component is not automatically permission to edit its definition. Resolve nested occurrence paths and reject edits to unloaded or read-only sources with guidance.

**Complete when:** Create a feature while viewing three identical occurrences. The UI identifies the edited definition and occurrence context; all intended shared instances update, and no feature lands in the displayed parent accidentally.

<a id="f012"></a>
### F012 — Body-oriented filtering

**Owning tasks:** 7.2, 10.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U02 · **First delivery:** P4 · **Likely scope:** Feature/UI

**Goal:** Find the operations responsible for a selected body without introducing body-owned histories again.

**Workflow and behavior:** Filter the part history by contributors to one or several body results, optionally including upstream inputs and downstream consumers. Clearly indicate that the tree is filtered, preserve access to the full history, and handle operations contributing to multiple results. Filtering must not suppress features or alter execution.

**Complete when:** Selecting a body created by a Boolean displays the contributing features and relevant inputs. Clearing the filter restores the full tree without any model or visibility mutation.

<a id="f013"></a>
### F013 — Navigator columns

**Owning tasks:** 10.6, 10.6d/e. **Status:** Bounded native state columns implemented in the feature organizer: visibility flags, suppression, errors/recompute, immediate source file and metadata access, with read-only filters/column choices and explicit refresh after changes. Fourteen grouped checks pass, including metadata compatibility and loaded external-source persistence. Full F013 remains open for integrated navigators, reference sets, nested/unloaded diagnosis, modified/file-permission state and physical acceptance. [Owner procedure](../tests/FeatureStateColumns.md).

**Packages:** U02 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Expose important model state in the tree so users need not open properties to diagnose routine problems.

**Workflow and behavior:** Offer configurable visibility, suppression, error/stale state, source file, reference set, and modified/read-only columns. Use distinct icons and text/tooltips for different states. Source and status values are derived from the model; toggles call validated commands and cannot bypass loading, ownership, or recompute rules.

**Complete when:** A hidden but unsuppressed component, a suppressed feature, an unloaded occurrence, and a failed feature are visibly distinguishable. Sorting columns changes presentation only and editing a state is undoable where appropriate.

<a id="f014"></a>
### F014 — Feature organization

**Owning tasks:** 10.6, 10.6b/c. **Status:** Bounded native metadata search/editor ready for owner testing. Label/name/type/description search, filtering/sorting without history edits, one-object Label/Label2 transactions, stale/identity guards, source/occurrence isolation, Undo/Redo and reopen/downstream geometry verified. One grouped build, 20 selected passing checks and four captures reviewed. Whole F014 remains open for folders, bulk organization, integrated navigators, uncapped/external search and physical acceptance. See [owner procedure](../tests/FeatureOrganizer.md).

**Packages:** U02 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Keep large part histories navigable through names, folders, comments, and targeted search.

**Workflow and behavior:** Support renaming, lightweight folders/groups, descriptions or comments, feature-type filters, and search by labels and useful metadata. Clearly distinguish a presentation folder from an operation group with execution semantics. Preserve stable identifiers through renaming and avoid turning a drag into a reorder without an explicit valid operation.

**Complete when:** Organize and rename a long feature sequence, then search for a hole and its comment. Model order and references are unchanged; folders and comments persist after reopening.

<a id="f015"></a>
### F015 — Dependency inspection

**Owning tasks:** 7.5, 10.6. **Status:** Bounded native dependency inspector ready for owner testing under 7.5.5a / 10.6a. Direct/transitive inputs and consumers, linking properties/expressions, native status and loaded external sources support explicit model selection and node navigation. Shared sketch/two extrusions/real fillet/drawing, cycles, limits, missing-face status/repair, Undo/save/reopen and lifecycle checks pass; 23 selected checks and three reviewed captures. Broader target-role classification, unloaded-reference diagnosis, integrated navigator tabs/highlights and physical/high-DPI acceptance remain open. [Owner procedure](../tests/DependencyInspector.md).

**Packages:** U02, A05 · **First delivery:** P3/P4 · **Likely scope:** Feature/UI

**Goal:** Show why a feature depends on another and what an edit or deletion could affect.

**Workflow and behavior:** From a feature, reveal direct inputs, target bodies, upstream dependencies, downstream consumers, and external sources using highlights and a compact dependency view. Allow navigation between nodes and differentiate direct from transitive dependencies. Use the actual execution graph rather than reconstructing dependency assumptions from tree order.

**Complete when:** Selecting a shared sketch reveals both consuming extrusions; selecting one extrusion shows a downstream fillet and drawing reference. The view handles cycles rejected by the system and missing references explicitly.

<a id="f016"></a>
### F016 — History controls

**Owning tasks:** 7.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U08 · **First delivery:** P3/P4 · **Likely scope:** Core/Feature

**Goal:** Allow users to inspect earlier states and insert or reorder features without corrupting dependencies.

**Workflow and behavior:** Provide a rollback marker or equivalent edit position, an explicit return-to-tip action, and insertion/reorder only when the dependency graph permits it. Show what becomes temporarily inactive and why a proposed move is invalid. Distinguish rollback display from committed suppression and ensure downstream stale results are labeled.

**Complete when:** Insert a supported feature before a fillet, reject moving a consumer ahead of its input, and return to the tip. Undo and save/reopen retain the intended sequence and no transient rollback state is mistaken for final geometry.

<a id="f017"></a>
### F017 — Shared part definitions

**Owning tasks:** 12.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A03 · **First delivery:** P2/P6 · **Likely scope:** Core/Feature

**Goal:** Reuse a part in one or many assemblies while keeping one editable source definition.

**Workflow and behavior:** Occurrences reference a stable definition and carry their own placement. Editing through an occurrence clearly edits the shared source; notify users of the scope through the command context. Update loaded dependents and show stale/external update status for sources that must be reloaded. Do not promise automatic edits to closed files.

**Complete when:** Edit a bracket used twice in one assembly and once in another. All loaded occurrences reflect the change, their placements remain independent, and reopened external documents resolve the updated source predictably.

<a id="f018"></a>
### F018 — Occurrence-specific properties

**Owning tasks:** 12.1, 12.2, 12.3. **Status:** Native whole-link visibility and uniform colour/transparency editor completed under 12.2b/c, ready for owner testing. Source inheritance/reset, source/other-link isolation, placement preservation, Undo/Redo and save/reopen pass; 23 selected checks and five reviewed captures. Whole F018 remains open for broader nested occurrence paths, representations/reference sets and physical/high-DPI acceptance. [Owner procedure](../tests/OccurrenceAppearance.md).

**Packages:** A03, B01 · **First delivery:** P3/P6 · **Likely scope:** Feature

**Goal:** Allow local presentation and placement differences without accidentally making a separate part.

**Workflow and behavior:** Store placement, visibility, allowed color/material-display overrides, and reference-set selection on the occurrence, with inheritance/reset-to-source behavior. Distinguish visual material overrides from engineering material or configuration changes that affect mass/FEM. Nested overrides resolve through the selected occurrence path.

**Complete when:** Color or hide one of several bolts and move another. The source geometry and unselected instances remain unchanged; resetting an override restores inherited behavior and survives save/reopen.

<a id="f019"></a>
### F019 — Make Unique

**Owning tasks:** 12.2, 12.2d/e. **Status:** Bounded native Make Unique pilot ready for owner testing. A same-document sketch/extrusion Part is copied with independent native identities and remapped inputs, then only the selected occurrence is relinked. Placement/visibility, independent edits, Undo/Redo, save/reopen and rollback pass; one grouped build, 19 selected passing checks and three reviewed captures. Whole F019 remains open for broader definitions/subassemblies, external destinations, provenance, relationship remapping and physical acceptance. See [owner procedure](../tests/UniqueOccurrence.md).

**Packages:** A03 · **First delivery:** P2/P6 · **Likely scope:** Feature/Core

**Goal:** Intentionally break shared geometry identity when one occurrence must become a different design.

**Workflow and behavior:** Preview the new definition, destination document, copied internal dependencies, and external links to retain or detach. Remap internal references, assign new identities, and replace only the selected occurrence while preserving placement and recoverable relationships. For subassemblies, explicitly choose shallow versus supported deep duplication.

**Complete when:** Make one repeated bracket unique, change its hole spacing, and reopen the project. Original instances stay linked to the original; the unique copy has no accidental internal references back to its former source.

<a id="f020"></a>
### F020 — Reference sets

**Owning tasks:** 12.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B01 · **First delivery:** P3/P6 · **Likely scope:** Feature/Core

**Goal:** Choose a part's exposed representation without changing what the part fundamentally contains.

**Workflow and behavior:** Provide Entire Part, Model, Empty, and named custom sets of geometry/datums. Document what Model includes and how new members are handled. An occurrence selects a set; source editing manages set membership. Empty retains the occurrence, identity, placement, and product-structure role. Commands explain when requested geometry is outside the selected set.

**Complete when:** Switch a subassembly among full, simplified, datum-only, and empty sets. Placement, BOM role, shared definition, and saved structure remain intact; missing representation is not mistaken for missing source.

<a id="f021"></a>
### F021 — Separate loading controls

**Owning tasks:** 12.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B06 · **First delivery:** P1/P6 · **Likely scope:** Core

**Goal:** Reduce resource use without overloading visibility or reference-set choices.

**Workflow and behavior:** Represent fully loaded, lightweight, and unloaded states independently. Retain identifiers, bounds/proxy information, source location, and assembly structure where supported. Commands requiring exact geometry resolve it deliberately or report a blocker. Define cache freshness and what can be inspected versus edited in each state.

**Complete when:** Unload a component, keep its occurrence in the tree, and later reload it at the same placement. Exact measurements, CAM, and validation cannot silently use a stale proxy as authoritative geometry.

<a id="f022"></a>
### F022 — Component replacement

**Owning tasks:** 12.6, 12.6a/b. **Status:** Bounded single-occurrence replacement ready for owner testing. An unconstrained native Link can reuse a same-document root solid/Body with explicit preview while retaining identity, placement, visibility and uniform appearance policy. Other instances stay unchanged; consumers/relationships are refused. Twenty-two selected checks pass across accepted suites with five reviewed captures. Whole F022 remains open for mate/interface remapping, multiple replacements, realignment and broader scope/physical acceptance. See [owner procedure](../tests/OccurrenceReplace.md).

**Packages:** B04, A05 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Swap a component source while retaining placement and as much valid assembly intent as possible.

**Workflow and behavior:** Select one occurrence or an explicitly chosen set, preview the replacement, and map published interfaces or stable reference equivalents. Preserve placement by default; offer deliberate alignment alternatives. Classify relationships as preserved, remapped, or unresolved rather than matching arbitrary face numbers. Allow cancellation before committing.

**Complete when:** Replace a bearing with a different size. Valid datum-based mates remain; incompatible face references are listed for repair; other shared occurrences change only if selected.

<a id="f023"></a>
### F023 — Component patterns and mirrors

**Owning tasks:** 12.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B04 · **First delivery:** P6 · **Likely scope:** Feature

**Goal:** Create repeated assembly occurrences with clear linkage, skipped positions, and handedness.

**Workflow and behavior:** Support bounded linear/circular patterns first, then other useful distributions. Store a seed definition, transforms, parameters, and stable instance keys. Mirrors must explain whether they reflect placement, create a mirrored definition, or create independent geometry; changing handedness is not ordinary rigid placement. Skipped instances remain identifiable for later edits.

**Complete when:** Change a bolt-pattern count without silently redirecting surviving mate/BOM references. A mirrored handed bracket has the declared shared/unique behavior and correct orientation, quantity, and mass.

<a id="f024"></a>
### F024 — Configurations and arrangements

**Owning tasks:** 12.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B05 · **First delivery:** P1 semantics; later P6 · **Likely scope:** Core

**Goal:** Separate design variants from saved assembly positions and presentation states.

**Workflow and behavior:** Configurations own declared parameter/suppression overrides and their identity; arrangements own component positions/joint settings or supported presentation state. Define whether occurrences can select different configurations of one source and how cache keys and derived results are distinguished. Keep flexible subassembly evaluation scoped to occurrence context instead of overwriting the rigid source.

**Complete when:** Use two size configurations in one assembly, save a folded/unfolded arrangement, and reopen. Editing one configuration or arrangement does not unintentionally change another; dependencies, BOM policy, and active variant are explicit.

<a id="f025"></a>
### F025 — Unified modeling workspace

**Owning tasks:** 8.4, 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U11, U03 · **First delivery:** P3/P4 · **Likely scope:** UI/Feature

**Goal:** Let users perform ordinary modeling without knowing whether a command historically belongs to Part or PartDesign.

**Workflow and behavior:** Offer a coherent modeling workspace backed by shared feature contracts, with task-oriented access to sketching, solids, surfaces, and assembly actions. Preserve advanced workbench access and expose incompatible legacy objects honestly. Command availability follows selection/edit context, while search explains unavailable commands instead of silently hiding every discovery path.

**Complete when:** Complete a bracket and enclosure using the unified workspace without switching workbenches merely to obtain a Boolean operation. Retained legacy commands and downstream workbenches continue to resolve the correct edit context.

<a id="f026"></a>
### F026 — Extrude

**Owning tasks:** 3.6, 3.8, 7.4, 10.2, 10.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U03, U09, U10 · **First delivery:** P2/P4 · **Likely scope:** UI/Core

**Goal:** Create and edit extruded material through one guided command with an efficient direct path.

**Workflow and behavior:** Select curves/regions, establish a normal or supported custom direction, enter extents, and review the contextual New Body/Unite suggestion or explicit Subtract/Intersect choice. Highlight targets and solid/sheet output. Keep Pad and Pocket as presets, with Pocket explicitly subtractive. Support returning to earlier inputs without erasing valid choices.

**Complete when:** Model a base, add an intersecting boss, create a separate rib blank, and cut a pocket using the same feature semantics. Editing extents preserves accepted operation/targets; invalid inputs cannot partially modify the part.

<a id="f027"></a>
### F027 — Revolve

**Owning tasks:** 3.9, 8.2, 10.2, 10.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U03, U09, U10 · **First delivery:** P4 · **Likely scope:** UI/Core

**Goal:** Create rotational features through the same clear intent and target workflow as Extrude.

**Workflow and behavior:** Select profiles and an axis from a datum, line, or supported cylindrical reference; show the axis and rotation sense. Offer partial/full revolution and applicable symmetric/two-sided angle controls. Keep Revolution/additive Revolve and Groove/Subtract presets. Explain profiles crossing the axis, self-intersections, and invalid solid/sheet choices.

**Complete when:** Build a turned part and its annular groove, reverse the rotation, and edit the axis/angle. Guided and direct entry produce equivalent editable results; failed full or partial revolutions preserve the last committed model.

<a id="f028"></a>
### F028 — Consistent Sweep and Loft

**Owning tasks:** 3.3, 13.2, 13.2c/d. **Status:** Bounded native Sweep inputs ready for owner testing. Explicit retained path, ordered section/output review, source-preserving failure/retry and associative save/reopen/downstream edits pass in 16 distinct selected checks after the grouped build and one corrective rebuild. [Owner procedure](../tests/SweepInputs.md). The bounded Loft workflow is recorded under F063/13.2a/b. Broader guides/orientation/scaling, section reversal, twist preview, Boolean targets and unified command-family acceptance remain open.

**Packages:** G03, U06 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Use familiar profile, guide, output-type, and Boolean conventions when creating nonprismatic shapes.

**Workflow and behavior:** Sweep collects section, path, and supported orientation/scaling controls; Loft collects ordered sections and optional guides. Expose solid versus sheet and targets consistently with Extrude/Revolve, but show only geometrically meaningful extents. Preview section orientation and likely twist before committing. Keep algorithm-specific advanced controls available without inventing equivalence between sweep and loft.

**Complete when:** Create a constant-section routed feature and a changing-section transition. Reorder or reverse sections, edit a guide, and verify deterministic results, target behavior, and clear unsupported-input diagnostics.

<a id="f029"></a>
### F029 — Common extent controls

**Owning tasks:** 8.1, 10.4. **Status:** Extrude/Pad/Pocket total symmetric and independent per-side labels, measured spans, typed second-side limit isolation and edit Cancel are validated under 8.1.4a/b (201 distinct passing checks). The specified Extrude examples for associative face movement, signed end offsets, missing-limit errors, repair, Undo/Redo and save/reopen are complete for the active-Body workflow. Empty/malformed typed limits, invalid OK with preview on/off, typed datum/origin plane preview and repair persistence are validated under 8.1.4c/d (207 distinct passing checks). End-limit typing/picking reject self/downstream references before assignment; typed datum/origin planes follow Body selection policy under 8.1.4e/f (213 distinct passing checks). Broader command-family, occurrence/dependency-selection and physical input/high-DPI acceptance remain open.

**Packages:** U06 · **First delivery:** P4/P7 · **Likely scope:** Feature

**Goal:** Make termination choices consistent and understandable across commands that support them.

**Workflow and behavior:** Offer Distance, Symmetric, Two-sided, Through All, To Face, and Offset from Face where applicable. Label total versus per-side distance, positive direction, start offset, and reference face. Store associative face/limit references and explicitly define their behavior after edits. Do not expose a mode on a command that cannot implement its semantics.

**Complete when:** An extrusion terminated at a selected face updates when that face moves; symmetric and two-sided values produce the documented lengths. A removed limiting face produces a repairable error rather than becoming a fixed distance silently.

<a id="f030"></a>
### F030 — Selection collectors

**Owning tasks:** 8.1, 10.4. **Status:** Trim Body/Isocline inspection, direction-reference clearing, entry counts, type hints and active-role text are validated under 8.1.3a-c. Extrude/Pad/Pocket profile inspection and feedback are validated under 8.1.3d/e. Combined Pattern Originals feedback, Clear/replacement recovery and direction-role isolation are validated under 8.1.3f-h (144 distinct passing tests). Pattern row/all-entry inspection by object identity and visibility lifecycle are validated under 8.1.3i (149 distinct final checks). Pattern inline rejection/correction feedback is validated under 8.1.3j (155 distinct final checks). Direction/Direction 2/Axis reference feedback, inspection and visibility lifecycle are validated under 8.1.3k/l (161 distinct final checks). Precise Body/sketch/datum type rejection is validated under 8.1.3m (167 distinct final checks). Extrude rejected end-limit picks retain saved links/displayed names and an active picker; typed plane scope and correction are validated under 8.1.4e/f (213 distinct passing checks). Other command families, general occurrence/selection filters and disambiguation acceptance remain open.

**Packages:** U06, A04 · **First delivery:** P3/P4 · **Likely scope:** UI/Feature

**Goal:** Make every requested geometric role visible so users know what to select next.

**Workflow and behavior:** Provide labeled Profile, Axis, Target Bodies, Guides, and Limits collectors with counts, type hints, and active-role highlighting. Users can activate, clear, replace, or inspect individual entries; selecting a row highlights its geometry and occurrence path. Validate type, scope, ordering, and duplication before accepting picks.

**Complete when:** A user can identify and replace the wrong guide or target without restarting a command. Ambiguous picks go through disambiguation, and selected geometry cannot silently fill a different role.

<a id="f031"></a>
### F031 — Preselection and postselection

**Owning tasks:** 8.1, 10.4. **Status:** Specified Extrude parity, deterministic mixed selections and creation/edit Cancel acceptance are complete for the active-Body workflow under 8.1.2b/8.1.5b (138 final passing checks). Extrude/Pad/Pocket use the same profile gate before and after startup; multiple profiles require explicit choice, invalid picks receive inline feedback. Trim Body/Isocline checks remain validated under 8.1.2a, 8.1.5a and 5.1.11. Combined Pattern creation/edit Cancel now restores original subelement selection and model state under 8.1.5c (149 distinct final checks). Pattern active-Body preselection/later-pick parity, mixed/invalid-input recovery and inline reasons are validated under 8.1.2c/8.1.3j (155 distinct final checks), with both Linear/Circular geometry comparisons. Precise type rejection and abandoned reference-role/scope recovery are validated under 8.1.3m/8.1.5d (167 distinct final checks). Extrude typed/picked end-limit dependency rejection, plane ownership, valid correction and edit Cancel are validated under 8.1.4e/f (213 distinct passing checks). Broader command-family, occurrence and multi-target semantics remain open.

**Packages:** U06, A07 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Support experienced users who select first and beginners who launch a command first.

**Workflow and behavior:** Map preselected items to valid roles only when unambiguous; preserve unresolved items for a visible choice or explain why they were ignored. Postselection uses the same collectors and checks. Switching selection order must not change geometry semantics, and invalid preselection should leave a useful command rather than fail opaquely.

**Complete when:** Run Extrude with a profile preselected and with no initial selection; the resulting feature parameters agree. Mixed profile/target selection is handled deterministically and Cancel restores the prior selection where appropriate.

<a id="f032"></a>
### F032 — Consistent Apply/OK/Cancel

**Owning tasks:** 8.1. **Status:** Trim Body/Isocline Cancel and failed-startup selection recovery is validated under 8.1.5a (85-test grouped batch). Extrude/Pad/Pocket create/edit Cancel selection plus profile/Body Tip rollback is validated under 8.1.5b. Pattern Originals Clear/replacement Cancel and Undo/Redo is validated under 8.1.3g; original selection plus model rollback on creation/edit Cancel is validated under 8.1.5c. Reference inspection preserves links on OK and restores source/Origin visibility on OK/Cancel under 8.1.3l. Unfinished reference picking preserves primary/secondary/axis links through OK, role/type/scope changes, Undo and edit Cancel under 8.1.5d (167 distinct final checks). Extrude invalid face-limit OK stays open with automatic preview on/off, and edit Cancel restores saved links, Body Tip and geometry under 8.1.4c (207 distinct passing checks). Apply/repeat and the two-holes-then-Cancel acceptance example remain open.

**Packages:** A07, U09 · **First delivery:** P3/P4 · **Likely scope:** Feature/UI

**Goal:** Make repeated operations and reversibility predictable across all modeling dialogs.

**Workflow and behavior:** OK validates, commits one operation, and exits; Apply commits and keeps the command ready with documented retained/reset inputs; Cancel discards only the current uncommitted operation. Escape handling, preview rollback, and selection restoration follow a shared lifecycle. If several Apply operations were committed, subsequent Cancel must not erase them unexpectedly.

**Complete when:** Apply two holes, begin a third, then Cancel. Exactly the first two remain as sensible undo steps; failed preview or cancellation leaves no orphan geometry, references, or hidden temporary objects.

<a id="f033"></a>
### F033 — Command search and shortcut palette

**Owning tasks:** 8.4, 10.4, 10.9. **Status:** Bounded command-search pilot ready for owner testing under 8.4.2a/b: standard menu/Ctrl+K, familiar aliases, shortcut display, explicit workbench switching and live run guards. Pocket opens subtractive Extrude with geometry, Undo/Redo and reopen acceptance; 59 distinct selected checks pass. Missing Assembly workbench/context guidance is validated; active Assembly, favorites, broader diagnoses and physical/high-DPI acceptance remain open. See [owner procedure](../tests/CommandSearch.md).

**Packages:** U04, U11 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Help users find equivalent operations using terminology they already know.

**Workflow and behavior:** Index canonical commands and aliases such as Pad/Extrude, Pocket/Cut, Groove/Revolved Cut, and supported NX/SolidWorks terms. Show concise intent, shortcut, current availability, and a reason or path when unavailable. Keep customization and favorites per user, with a reset and conflict checks. Search aliases invoke the same validated commands.

**Complete when:** Searching Pocket opens subtractive Extrude; an unavailable assembly operation explains the required context. Keyboard users can invoke search, choose a result, and reach the relevant input without a mouse.

<a id="f034"></a>
### F034 — Modifier-based multiselection

**Owning tasks:** 10.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U05 · **First delivery:** P4/P5 · **Likely scope:** UI

**Goal:** Prevent accidental accumulation of sketch selections while keeping deliberate multiselection fast.

**Workflow and behavior:** Plain click replaces the current set; Ctrl toggles/adds and Shift provides the documented extension/range behavior. Allow consistent configurable presets where platform conventions require them. Window selection may select multiple entities in one gesture. Coordinate these rules with drawing tools, dragging, and the separate auto-inference override key.

**Complete when:** Select one sketch line, click another, then use modifiers to form a two-line set. Selection counts, eligible constraints, and deselection are predictable in the viewport and tree without breaking geometry creation.

<a id="f035"></a>
### F035 — Selection filters

**Owning tasks:** 10.5. **Status:** Bounded entity-filter workflow ready for owner testing under 10.5e/f. Vertex/edge/face/whole-object policy intersects command gates and preserves repeated occurrence paths; visible reset/Close/Escape/startup recovery passes. One grouped build plus a startup-registration correction, 17 distinct selected passing checks and five reviewed captures. Full F035 stays open for separate body/component/sketch/feature categories, dedicated sketch/tree/window picking and physical/high-DPI acceptance. [Owner procedure](../tests/EntitySelectionFilter.md).

**Packages:** U05 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Reduce accidental picks by letting users restrict selectable entity types.

**Workflow and behavior:** Expose points/vertices, edges, faces, bodies, components, sketches, and features, with a clear active-filter indicator and quick reset. Command-specific filters refine the global policy without becoming a persistent trap. Respect keyboard navigation and show why a visible object cannot be selected under the active filter.

**Complete when:** In a dense assembly, face-only selection cannot accidentally select a whole component. Leaving a command restores the documented previous filter state and the user can recover from an empty result easily.

<a id="f036"></a>
### F036 — Selection scope

**Owning tasks:** 10.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A04, U05 · **First delivery:** P1/P4 · **Likely scope:** Core/UI

**Goal:** Control whether selection addresses local geometry or surrounding assembly context.

**Workflow and behavior:** Provide active-part, selected-component, and whole-assembly scopes with occurrence-path-aware results. Scope is separate from visibility and loading. Commands declare whether they accept contextual references, editable targets, or both; a selectable external face is not automatically a writable target. Make scope changes deliberate and visible.

**Complete when:** During in-context editing, a user can reference a neighboring face while a local Boolean command refuses to alter that neighbor silently. Nested and repeated occurrences resolve the intended path.

<a id="f037"></a>
### F037 — Select Other

**Owning tasks:** 10.5, 10.5c/d. **Status:** Bounded Select Other increment is ready for owner testing in native Clarify Selection: equal-label candidates retain document/root/full occurrence identity and visible context; native gates filter element/whole-object roles and are rechecked for hover/accept. One grouped build, 16 selected checks and five reviewed captures pass. Full F037 remains open for broader live-topology and physical/high-DPI/navigation-preset acceptance. [Owner procedure](../tests/ClarifySelection.md).

**Packages:** U05 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Resolve overlapping or obscured picks without temporarily dismantling the display.

**Workflow and behavior:** Open a small candidate list or cycling interaction with transient highlights and useful labels/type/context. Order candidates predictably using pick location and scope; allow deeper/hidden candidates only under documented rules. Escape dismisses without replacing the existing selection. Keep filtering and occurrence identity intact.

**Complete when:** Select the rear of two coincident faces and one of overlapping repeated components. Hover/cycle previews accurately identify candidates, and the final selection matches the preview.

<a id="f038"></a>
### F038 — Selection intent rules

**Owning tasks:** 10.5, 7.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U05, A05 · **First delivery:** P3/P4 · **Likely scope:** Feature/Core

**Goal:** Let users specify a meaningful geometric set instead of manually picking every member.

**Workflow and behavior:** Offer tangent chain, connected edges, complete loop, same-radius faces, and feature-owned faces where supported. Preview included entities and expose tolerance/boundary choices. Distinguish storing an associative rule that reevaluates after edits from freezing an explicit selection set; avoid silently expanding operation scope when topology changes.

**Complete when:** A fillet uses an accepted tangent chain and a later edge split resolves according to the stored policy. Unexpected added branches or ambiguous loops produce a visible choice or repair rather than an unnoticed broad edit.

<a id="f039"></a>
### F039 — Window versus crossing selection

**Owning tasks:** 10.5, 10.5g/h. **Status:** Bounded native 3D window/crossing workflow ready for owner testing: full enclosure, directional borders and filter/gate-aware collection pass in nineteen distinct checks, with six reviewed captures. Full F039 remains open for broad sketch/curve and physical acceptance; nested serialized BRep flag preservation is not claimed. [Owner procedure](../tests/WindowSelection.md).

**Packages:** U05 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Make rectangle selection communicate whether partial overlap counts.

**Workflow and behavior:** Provide distinct enclosed-only and crossing modes through a documented drag-direction or explicit setting, with visible styling during the gesture. Define whether hidden/back-facing geometry is eligible and apply type/scope filters consistently. Preserve a deliberate modifier policy for replacing, adding, and removing window results.

**Complete when:** A rectangle around part of a sketch selects only fully enclosed entities in one mode and crossing entities in the other. The same behavior holds at different zoom levels and does not accidentally include hidden assembly geometry.

<a id="f040"></a>
### F040 — Temporary isolate/hide

**Owning tasks:** 10.5. **Status:** Bounded temporary isolate/hide/restore pilot ready for owner testing under 10.5a/b. Native Parts, whole Body results and whole linked occurrences support per-document nested restore. Created/deleted/reused objects, model Undo/Redo and restored save/reopen are validated; all 20 selected checks pass and five viewport captures are reviewed. Session snapshots do not persist; restore before saving. Linked-member overrides, save-time policy and physical/high-DPI acceptance remain open. [Owner procedure](../tests/TemporaryDisplay.md).

**Packages:** U05 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Inspect a subset quickly and return to the previous display without manual reconstruction.

**Workflow and behavior:** Isolate selected objects, hide selected objects, and restore the prior visibility snapshot using explicit temporary-display actions. Handle nested isolates and newly created objects predictably. Visibility must not imply suppression, exclusion from a Boolean target set, or removal from BOM/validation.

**Complete when:** Isolate a component, hide one of its bodies, inspect it, and restore. The prior assembly visibility returns; no suppressed or reference-only states change and retained operation targets remain intact.

<a id="f041"></a>
### F041 — Predictable navigation

**Owning tasks:** 8.4, 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U04, U11 · **First delivery:** P4 · **Likely scope:** UI

**Goal:** Make camera movement and sketch entry familiar and controllable.

**Workflow and behavior:** Offer configurable mouse/navigation presets, a visible or inferable rotation center, zoom-to-selection, fit-all, standard views, and orthographic sketch orientation. Preserve the previous 3D view when entering/exiting sketch edit and avoid wild camera jumps on small or off-origin geometry. Resolve shortcut conflicts with selection and command gestures.

**Complete when:** Orbit about a selected feature in a large assembly, enter a rotated sketch, and return to the previous view. Mouse presets and high-DPI settings remain usable without changing model coordinates.

<a id="f042"></a>
### F042 — Improved automatic relations

**Owning tasks:** 11.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S01 · **First delivery:** P5 · **Likely scope:** Feature

**Goal:** Infer common sketch intent as geometry is drawn without creating surprising constraints.

**Workflow and behavior:** Support configurable coincidence, tangent, horizontal/vertical, parallel, perpendicular, and equal inference where the solver supports them. Use screen-space proximity for interaction while respecting geometric tolerances and model units. Prioritize candidates, show what will be added, and distinguish transient snapping from persistent constraints.

**Complete when:** Draw representative lines, circles, and arcs with intended inferences and near-miss counterexamples. Only accepted relations persist, the override prevents unwanted inference, and dense geometry does not create arbitrary constraints.

<a id="f043"></a>
### F043 — Constraint preview

**Owning tasks:** 11.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S01 · **First delivery:** P5 · **Likely scope:** UI/Feature

**Goal:** Show the relationship about to be added before the user commits geometry.

**Workflow and behavior:** Display a legible relation glyph and highlight its operands as the pointer approaches a valid inference. Provide a temporary suppression key independent of Ctrl/Shift multiselection, plus optional inference controls. Preview state never mutates the committed sketch and disappears when the candidate or tool changes.

**Complete when:** Approach a tangent and then a coincident condition, suppress one inference, and complete drawing. The persisted relation matches the final preview and no abandoned candidate survives.

<a id="f044"></a>
### F044 — Cursor-adjacent constraint palette

**Owning tasks:** 11.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S02, S07 · **First delivery:** P5 · **Likely scope:** UI/Feature

**Goal:** Offer relevant constraints close to the user's selection without forcing a toolbar search.

**Workflow and behavior:** After selection, show a compact palette driven by the shared eligibility service. Use a reachable pointer corridor or dismissal delay, place it away from selected geometry and screen edges, and dismiss when the pointer genuinely leaves. Provide keyboard access, stable ordering, high-DPI sizing, and a user preference to disable it.

**Complete when:** Select one line and two lines, move into the palette, apply a relation, and move away. It remains reachable, shows the correct actions/states, and never applies a constraint merely because the pointer crossed it.

<a id="f045"></a>
### F045 — Smart Dimension

**Owning tasks:** 11.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S03 · **First delivery:** P5 · **Likely scope:** UI/Feature

**Goal:** Infer the useful dimensional relationship from geometry while allowing explicit control.

**Workflow and behavior:** For suitable selections offer length, angle, radius, diameter, horizontal/vertical spacing, and other supported measurements. Preview alternatives based on placement or an explicit switch; show units and driving versus reference state. Route overconstrained candidates through shared validation rather than silently converting or deleting existing dimensions.

**Complete when:** Dimension a line, circle, pair of lines, and point spacing. Users can deliberately select radial versus diameter or projected versus aligned length, and edits preserve their chosen dimension type.

<a id="f046"></a>
### F046 — Dimension during drawing

**Owning tasks:** 11.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S03 · **First delivery:** P5 · **Likely scope:** Feature

**Goal:** Let users establish exact geometry while drawing instead of repeatedly drawing approximately and editing afterward.

**Workflow and behavior:** Expose temporary numeric fields for supported line lengths/angles, rectangle dimensions, circle diameters, and slot dimensions. Define field cycling, locked versus inferred values, expression/unit entry, and Escape behavior. Commit a coherent set of geometry and constraints as one undoable action; keep advanced options accessible.

**Complete when:** Create a rectangle and slot from typed dimensions, correct a field before commit, and cancel another attempt. The resulting dimensions are editable driving constraints and no half-created geometry remains.

<a id="f047"></a>
### F047 — Visual degrees of freedom

**Owning tasks:** 11.4, bounded tasks 11.4c/d. **Status:** Native sketch-edit solver-state guidance and unconstrained-geometry selection are ready for owner testing; 15 selected checks and five reviewed captures cover live constraint/repair transitions, source preservation, Undo/Redo and reopen. Full F047 remains open for movement-direction indicators, richer per-entity diagnosis and physical acceptance. [Owner procedure](../tests/SketchFreedom.md).

**Packages:** S04 · **First delivery:** P5 · **Likely scope:** Feature/UI

**Goal:** Show what can still move and distinguish incompletely constrained geometry from a failed solve.

**Workflow and behavior:** Use visual states and optional movement-direction indicators for translation, rotation, size, or other supported freedoms, supplemented by text rather than color alone. Distinguish grounded/fixed geometry, reference geometry, solver conflict, and remaining freedom. Do not present a simple count as a complete diagnosis when freedoms are coupled.

**Complete when:** A partly constrained sketch reveals the intended remaining movement; adding a supported relation updates the indication. A conflicting sketch is clearly different from a merely underconstrained one.

<a id="f048"></a>
### F048 — Constraint repair

**Owning tasks:** 11.4, 11.4a/b. **Status:** Bounded constraint repair is ready for owner testing: native isolated-copy diagnosis, explicit deactivation choices, solve/freedom/wireframe preview and one transactional Apply. Constraint numbers/names/values survive; no automatic deletion. One grouped build, 15 distinct selected checks and six final captures pass. Full F048 remains open for attached/Body/external and expression-driven sketches, replacement, broader previews and physical acceptance. [Owner procedure](../tests/ConstraintRepair.md).

**Packages:** S04, S07 · **First delivery:** P5 · **Likely scope:** Feature/Core

**Goal:** Explain overconstraint and help users make a deliberate repair while preserving design intent.

**Workflow and behavior:** Separate existing, redundant, conflicting, and unsupported constraints. Highlight implicated geometry and candidate relations, preview the effect of removing/replacing a relation, and show resulting freedom where feasible. Candidates may be conservative solver-derived sets rather than a claimed unique cause. Never delete constraints automatically to make a new action succeed.

**Complete when:** Create a redundant dimension and a genuine conflict. The UI distinguishes them, offers an understandable reversible repair, and leaves the original sketch unchanged if the user cancels.

<a id="f049"></a>
### F049 — Sketch repair

**Owning tasks:** 11.6. **Status:** Missing-coincidence review and checked-only repair completed under 11.6a/b, ready for owner testing. Endpoint/gap list, highlighting, conflict rollback, invalidation, Undo/Redo, persistence and downstream extrusion pass; 22 selected checks and five reviewed captures. Native detector/Block limitations, duplicate/self-intersection diagnosis, broader repair/preview and physical acceptance remain open. [Owner procedure](../tests/SketchRepairReview.md).

**Packages:** S06 · **First delivery:** P5 · **Likely scope:** Feature

**Goal:** Find small defects that prevent profiles from becoming valid regions or downstream features.

**Workflow and behavior:** Detect gaps, duplicate entities, tiny segments, overlaps, self-intersections, and unsupported loops using explicit model-scale tolerances. Present a navigable results list with zoom/highlight and proposed fixes. Separate diagnostic tolerance from automatic merging tolerance, and preview changes to constraints before deleting or merging geometry.

**Complete when:** Repair an almost-closed profile and a duplicated edge deliberately. The intended region becomes usable, preserved dimensions still express the same design, and ignoring a tiny segment does not falsely certify a valid profile.

<a id="f050"></a>
### F050 — Power trim/extend

**Owning tasks:** 11.6. **Status:** Bounded native Trim gesture grouping and removed/replaced-constraint feedback ready for owner testing under 11.6e/f: twelve distinct checks pass, five final captures reviewed, Undo/Redo and save/reopen verified. Full power trim/extend acceptance remains open for removal previews, extension behavior, broader curves and owner workflow feedback. [Owner procedure](../tests/TrimGesture.md).

**Packages:** S06 · **First delivery:** P5 · **Likely scope:** Feature

**Goal:** Remove or extend sketch segments with fewer selections while keeping the result understandable.

**Workflow and behavior:** Support dragging across segments to trim and deliberate extension to a selected or inferred boundary. Preview the portion removed/added, distinguish construction geometry, and retain valid dimensions/relations or report which will be removed. Bundle one drag gesture into a sensible undo step and avoid silently changing unrelated loops.

**Complete when:** Trim several crossing lines, extend an arc to a boundary, and undo. Geometry matches the preview; surviving constraints remain valid and removed constraints are explained rather than left dangling.

<a id="f051"></a>
### F051 — Region selection

**Owning tasks:** 11.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S06, A05 · **First delivery:** P3/P5 · **Likely scope:** Feature/Core

**Goal:** Use closed areas inside a complex sketch without copying or deleting the rest of the sketch.

**Workflow and behavior:** Highlight bounded regions and nested holes, support multiple compatible regions, and explain ambiguous/open/self-intersecting boundaries. Define how selected regions are identified across sketch edits and how changes that split/merge regions are repaired. Keep full-sketch versus region inputs explicit in feature parameters.

**Complete when:** Extrude one compartment of a multi-region sketch and later move an internal boundary. The intended region updates or requests repair; the command does not silently extrude every newly formed region.

<a id="f052"></a>
### F052 — Associative external geometry

**Owning tasks:** 11.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S05, B03 · **First delivery:** P5 · **Likely scope:** Feature/Core

**Goal:** Bring useful neighboring geometry into a sketch through projection or true intersection with clear provenance.

**Workflow and behavior:** Offer projected edges, curve/plane intersection points, and face/plane intersection curves as distinct operations. Show source part/occurrence, transform, and association status. Define tangent, coplanar, coincident, disjoint, and multiple-result cases; a surface intersection is not necessarily a straight line. External inputs obey publication/scope and cycle rules.

**Complete when:** Intersect an angled edge and curved surface with a sketch plane, then move the source. Points/curves update correctly or report ambiguity; independent copies and associative references remain visibly distinct.

<a id="f053"></a>
### F053 — Sketch reuse tools

**Owning tasks:** 11.6, 11.6c/d. **Status:** Independent whole-sketch reuse is ready for owner testing: internal constraints/construction geometry, named dimensions, typed source-frame placement, view-only preview and one Undoable native copy. One grouped build; 35 distinct selected passes, one inherited solver skip; five final captures reviewed. Full F053 remains open for partial paste, external-reference policy choices, blocks/libraries/patterns and physical acceptance. [Owner procedure](../tests/SketchReuse.md).

**Packages:** S06, A05 · **First delivery:** P5 increments · **Likely scope:** Feature/Core

**Goal:** Reuse proven sketch content while controlling which relationships remain shared.

**Workflow and behavior:** Provide constraint-preserving copy/paste with transform, reusable profiles, blocks, and sketch patterns in separate increments. Remap internal geometry/constraint identifiers; require a choice for external references. Define block-local coordinates, editable block instances, explode behavior, and pattern members before claiming full block support.

**Complete when:** Copy a constrained slot, rotate/place it, and change its dimensions. Internal relations survive; external links follow the declared policy; block or pattern edits affect the intended members and remain undoable.

<a id="f054"></a>
### F054 — Interactive feature handles

**Owning tasks:** 8.4.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U06 · **First delivery:** P4/P7 · **Likely scope:** UI/Feature

**Goal:** Adjust common feature values visually while retaining exact parametric control.

**Workflow and behavior:** Expose handles for supported length, angle, radius, and offset values, with clear direction, snapping, numeric entry, and current units. Dragging changes a transient preview; typed values and expressions use the same parameter validation. Indicate limits and invalid ranges without committing unusable geometry.

**Complete when:** Drag an extrusion handle, type an exact value, cancel a second edit, and reopen the part. The stored parameter is exact and editable, while canceled or intermediate previews leave no document changes.

<a id="f055"></a>
### F055 — Hole wizard

**Owning tasks:** 13.5, 13.5c/d. **Status:** Native profile/Body and thread-result review implemented; 13.5c is ready for owner testing. One grouped build and 17 bounded passing checks cover working modes, Cancel, counterbore creation/Undo and cosmetic persistence/downstream edits. Task 13.5d stays open for deferred modeled-thread acceptance waiting and a counterbore Redo volume mismatch. Standalone modeled geometry succeeds but does not close task acceptance. Broader guided placement, table provenance, drawing callouts and owner acceptance remain open. [Owner procedure](../tests/HoleSpecification.md).

**Packages:** G06 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Create standard, documented holes through one guided placement and specification workflow.

**Workflow and behavior:** Separate hole locations from hole definition: select/reuse position sketches or points, then choose simple, counterbore, countersink, or thread specification and extent. Use versioned standard tables with explicit units/source and user overrides. Distinguish cosmetic thread metadata from actual helical geometry and communicate cost/compatibility.

**Complete when:** Create repeated counterbores and tapped holes, edit their standard/size, and produce supported drawing callouts. Location links, depth, thread representation, targets, and validation remain consistent after parameter changes.

<a id="f056"></a>
### F056 — Unified patterns

**Owning tasks:** 3.7, 13.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G06 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Repeat features or bodies with one recognizable interface and explicit pattern semantics.

**Workflow and behavior:** Offer linear, circular, curve-driven, and table-driven patterns in staged increments, with count/spacing, orientation, seeds, and skipped members. Distinguish copying resulting geometry from reevaluating a feature at each location when they yield different results. Preserve stable member keys for downstream references and report invalid members.

**Complete when:** Pattern a hole across uneven geometry, skip two members, and change count/spacing. Valid members retain predictable references; unsupported members are identified and do not silently change the chosen evaluation mode.

<a id="f057"></a>
### F057 — Feature/body mirror

**Owning tasks:** 13.5, 13.5a/b. **Status:** Bounded Part Mirror result-mode pilot is ready for owner testing: native associative mirror or independent reflected-shape snapshot for root shapes/whole Bodies, atomic creation and inline recovery. All 21 selected checks pass together; five captures reviewed. Source/plane edits, asymmetric geometry, Undo/Redo and save/reopen verified. Whole F057 remains open for feature reevaluation, broader occurrence/nested scope, target/handedness preview and physical acceptance. See 13.5a/b and [owner procedure](../tests/MirrorResultMode.md).

**Packages:** G06 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Make symmetry operations explicit about what is mirrored and whether results remain linked.

**Workflow and behavior:** Select features or body results and a mirror plane, then choose supported mirrored geometry, associative copies, or independent results. Preview Boolean target behavior and handedness. Feature mirroring must map inputs/targets under its declared semantics rather than merely duplicating viewport graphics.

**Complete when:** Mirror an asymmetric bracket body and a hole feature, edit the seed, and verify the chosen linkage. Reflected geometry, labels, target scope, and saved feature history remain correct.

<a id="f058"></a>
### F058 — Improved fillets/chamfers

**Owning tasks:** 13.5. **Status:** Bounded native fillet/chamfer recovery ready for owner testing under 13.5e/f. Failed acceptance retains checked edges/sizes and prior geometry; native kernel inputs are isolated with element maps intact. One grouped build, 16 distinct selected passing checks and six reviewed captures establish retry, Undo/Redo, variable fillet, two-distance chamfer, failed edit/Cancel and downstream save/reopen. Full tangent-chain, preview, corner, precise kernel-localization and physical acceptance remain open. [Owner procedure](../tests/EdgeTreatmentRecovery.md).

**Packages:** G06 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Make edge treatment easier to define and diagnose when complex geometry fails.

**Workflow and behavior:** Use edge collectors with tangent propagation, radius/offset previews, and supported variable-radius and corner controls. Separate attempted capabilities from validated kernel support. Localize failing edges or corners and let users revise a subset without losing valid selections. Keep tolerance and reference-repair behavior explicit.

**Complete when:** Create a chain fillet and a supported variable-radius case, then force a corner failure. The UI identifies a useful failing region, preserves prior geometry, and allows correction without rebuilding the entire selection.

<a id="f059"></a>
### F059 — Shell, draft, ribs, and webs

**Owning tasks:** 13.5, 13.5g/h. **Status:** Bounded native shell Thickness face/side review and recoverable acceptance ready for owner testing: sixteen distinct checks pass, six final captures reviewed, Undo/Redo, save/reopen and downstream source editing verified. Full F059 remains open for Draft, Rib/Web, oversized-offset correctness and broader acceptance. [Owner procedure](../tests/ShellThickness.md).

**Packages:** G06 · **First delivery:** P7 increments · **Likely scope:** Feature/Core

**Goal:** Provide consistent guided workflows for common manufacturing-oriented features.

**Workflow and behavior:** Shell collects removed faces and thickness/side; Draft collects neutral reference, pull direction, target faces, and angle; Rib/Web collects profiles, thickness, direction, and extent/targets. Explain when thickness, draft, or intersections make the result invalid. Keep each operation a separate bounded implementation with common lifecycle and reference behavior.

**Complete when:** Create and edit a thin enclosure, a drafted wall, and a reinforcing rib. Direction/thickness previews match final results; invalid thin regions or missing intersections produce localized, reversible failures.

<a id="f060"></a>
### F060 — Split and trim bodies

**Owning tasks:** 4, 13.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G01 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Divide solids or sheets with an explicit preview of which regions remain.

**Workflow and behavior:** Choose planes, surfaces, or bodies as tools, select target bodies, and preview resulting regions with keep/remove choices. Specify retained-tool behavior and distinguish a nondestructive split into multiple results from trimming away regions. Persist region choices/provenance and treat later ambiguous splits as repair cases.

**Complete when:** Split a housing with a plane, retain both halves, and trim one with a surface. Edit the tool and verify output identities, target scope, undo, and downstream-reference outcomes.

<a id="f061"></a>
### F061 — Direct editing

**Owning tasks:** 13.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G07 · **First delivery:** Late P7 · **Likely scope:** Feature/Core

**Goal:** Make bounded changes to imported and native geometry without pretending to recover its original feature history.

**Workflow and behavior:** Offer move, offset, replace, and delete-and-heal face operations as new editable steps. Show affected adjacent topology and whether tangent propagation or healing is supported. Do not alter an upstream feature's parameters silently. Limit initial support to reproducibly valid shape classes and expose failures explicitly.

**Complete when:** Offset an imported planar face, remove a suitable hole with healing, and undo. Native downstream references either remain valid or request repair, and unsupported healing leaves the original model intact.

<a id="f062"></a>
### F062 — Feature recognition

**Owning tasks:** 13.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G08 · **First delivery:** Late P7 after spike · **Likely scope:** Core

**Goal:** Recover useful editable structure from suitable imported solids while acknowledging incomplete information.

**Workflow and behavior:** Detect bounded candidates such as analytic holes, pockets, or fillets; preview recognized parameters and residual geometry before conversion. Label uncertain or unsupported candidates and retain the original solid as a recoverable source. Recognition is a new inferred model, not proof of the original designer's intent.

**Complete when:** Recognize a documented test set, edit an accepted hole diameter, and compare the unchanged surrounding geometry. False positives can be rejected and unrecognized portions remain usable rather than disappearing.

<a id="f063"></a>
### F063 — Through-curves surfaces

**Owning tasks:** 13.2, 13.2a/b. **Status:** Bounded ordered open-section Loft ready for owner testing: native open wires/single edges, explicit surface/solid/ruled/closed-loop review, valid atomic creation and recoverable failure. Association, Undo/Redo and save/reopen pass in 17 grouped checks; one corrective rebuild clarifies failed solid output. Full F063 remains open for guides, correspondence/reversal, geometric/twist preview, continuity/tolerance certification and Boolean targets. [Owner procedure](../tests/LoftSections.md).

**Packages:** G03 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Construct a controlled surface through ordered sections, using guides to shape correspondence.

**Workflow and behavior:** Collect sections in order, optional guide curves, start/end conditions, and curve directions; show correspondence markers and twist previews. Validate guide/section compatibility and supported intersections within explicit tolerances. Expose meaningful continuity controls only when the construction supports them and retain all input associations.

**Complete when:** Build a transition through three sections with guides, reverse one section, and adjust correspondence. The preview identifies twist; committed geometry meets documented interpolation/tolerance requirements and updates after source edits.

<a id="f064"></a>
### F064 — Curve-network surfaces

**Owning tasks:** 13.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G04 · **First delivery:** P7 after spike · **Likely scope:** Core

**Goal:** Build surfaces from two intersecting curve families when through-sections alone cannot express the intended shape.

**Workflow and behavior:** Collect and order the two curve directions, detect missing/inconsistent intersections, and show network cells/corners. Specify supported open/closed networks, trimming, interpolation, and approximation tolerance. Start with a bounded regular network instead of promising arbitrary networks or commercial-kernel equivalence.

**Complete when:** Construct and edit a regular network fixture, reject incompatible crossings with localized diagnostics, and verify claimed interpolation and surface validity independently of visual smoothness.

<a id="f065"></a>
### F065 — Boundary continuity

**Owning tasks:** 13.3, 15.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** G04, I02 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Control how a new surface joins neighboring geometry and verify the requested level.

**Workflow and behavior:** At each supported boundary, choose positional, tangent, or curvature continuity with the required adjacent reference and orientation. Explain unsupported boundary combinations, approximation limits, and conflicting conditions. Treat continuity as a measured geometric property, not an icon or display shading choice.

**Complete when:** Create representative G0/G1/G2 supported joins, alter neighboring geometry, and inspect them using numerical continuity checks and visual tools. A failed condition is reported rather than silently downgraded.

<a id="f066"></a>
### F066 — Trim/untrim/extend surfaces

**Owning tasks:** 13.1, 13.1e/f. **Status:** Bounded native face-extension review ready for owner testing: explicit parameter/fitting semantics, boundary-only preview, recoverable refusal and separate associative creation. One grouped native build; 19 distinct selected checks pass and six final captures reviewed. Full trim/untrim, measured deviation, broader surfaces and physical acceptance remain open. [Owner procedure](../tests/ExtendFaceReview.md).

**Packages:** G01, G02 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Edit sheet boundaries while preserving the distinction between underlying surfaces and trimming loops.

**Workflow and behavior:** Trim with selected curves/surfaces and pick kept regions; untrim exposes recoverable underlying surface domains; extend grows supported boundaries using a stated geometric method. Preview new boundaries and self-intersections. Do not claim untrim can recover original design intent or missing geometry from every imported sheet.

**Complete when:** Trim a sheet into two regions, restore a supported original domain, and extend an edge. Tool associations and region selections survive edits or become explicitly unresolved, without creating invalid shells.

<a id="f067"></a>
### F067 — Thicken sheet bodies

**Owning tasks:** 13.1, 13.1c/d. **Status:** Bounded one-sided sheet thickening is ready for owner testing through the existing native 3D Offset task. Signed distance/reversal, solid versus sheet feedback, source-preserving native copies and recoverable failed acceptance are verified. Seventeen distinct selected checks pass, with six captures reviewed. Full F067 remains open for symmetric thickness, graphical normals, Boolean targets, compound sheets, broader diagnostics and physical acceptance. See [owner procedure](../tests/SheetThickening.md).

**Packages:** G02 · **First delivery:** P7 · **Likely scope:** Feature/Core

**Goal:** Convert valid sheet geometry into material with a clear side, thickness, and Boolean result.

**Workflow and behavior:** Offer one-sided, opposite-sided, and symmetric thickness with unambiguous total/per-side dimensions. Show normals and side reversal; collect optional union/subtraction targets through common rules. Detect tight curvature, offset self-intersections, and unsuitable open boundaries; distinguish a thickened solid from separate offset sheets.

**Complete when:** Thicken a planar and a curved fixture in each supported direction, then test a radius smaller than the requested thickness. Valid results have the expected volume and failed offsets preserve the source.

<a id="f068"></a>
### F068 — Sew/stitch surfaces

**Owning tasks:** 13.1, 13.1a/b. **Status:** Bounded native Shape Builder sewing/solid workflow ready for owner testing. Explicit tolerance reaches the kernel; checks distinguish open/closed shells and disconnected sheets, list free boundaries and disclose actual geometry tolerance. Independent snapshots preserve sources; open-shell solid creation is refused. Twenty-two selected checks pass across accepted suites, with six settled captures reviewed. Whole F068 remains open for associative sources, graphical boundaries/preview, gap measurement, broader diagnostics and physical acceptance. See [owner procedure](../tests/ShapeSewing.md).

**Packages:** G02 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Join compatible sheets and reveal where gaps prevent a valid shell or solid.

**Workflow and behavior:** Collect sheets, display free edges/gaps, and use explicit tolerances with a preview of proposed joins. Indicate whether the result is an open shell, closed shell, or valid solid. Avoid silently escalating tolerances to force a join; show any healing/approximation effects and retain source choices.

**Complete when:** Stitch a known enclosure and an intentionally gapped version. The first becomes a verified solid; the second identifies the unresolved gap and cannot be labeled watertight merely because it renders closed.

<a id="f069"></a>
### F069 — Extract/project/intersect curves

**Owning tasks:** 13.4; bounded intersection tasks 13.4a/b. **Status:** Native Section review and associative creation are ready for owner testing. 18 selected checks and six reviewed captures cover preview/source preservation, empty results, multiple loops, Undo/Redo, persistence and downstream edits. Full F069 remains open for extraction, projection, broader references/topology repair and physical acceptance. [Owner procedure](../tests/SectionReview.md).

**Packages:** G05 · **First delivery:** P7 · **Likely scope:** Feature

**Goal:** Generate reusable design curves from existing geometry with clear source and method.

**Workflow and behavior:** Support extracting edges/face boundaries, projecting curves along a chosen direction or supported normal rule, and intersecting bodies/surfaces. Collect source and target roles separately, define multiple/disjoint/tangent results, and preserve association or deliberate snapshot copying. Display approximation tolerance for nonanalytic results.

**Complete when:** Project a curve onto a curved face and intersect two surfaces. Moving a source updates intended results; multiple branches remain identifiable and changed topology cannot silently switch the selected branch.

<a id="f070"></a>
### F070 — Isocline curves

**Owning tasks:** 5, 13.4. **Status:** Functional acceptance complete for the documented bounded, single-angle workflow under 5.1.12/5.2.4 (130-test grouped checkpoint). See the [acceptance mapping](../tests/IsoclineCurve.md#f070-functional-acceptance-mapping). Physical viewport/keyboard/high-DPI acceptance remains 5.2.3; arbitrary singular-surface completeness is not claimed.

**Packages:** G05, I02 · **First delivery:** P7 after spike · **Likely scope:** Feature/Core

**Goal:** Create constant-draft-angle curves on a surface relative to a chosen pull direction.

**Local convention:** Preserve Phase 5: normal dot pull = sin(draft angle), with 0 degrees at the silhouette. The supplied normal-angle wording is interpreted through this established convention, not as a change to stored feature semantics.

**Workflow and behavior:** Collect faces, direction, angle, domain, and tolerance; state the normal-orientation and signed/unsigned angle convention. Distinguish isoclines from isoparametric curves and purely visual draft-analysis coloring. Handle zero/multiple curves, singularities, boundary termination, and unsupported surface types explicitly.

**Complete when:** On analytic fixtures, sampled curve points satisfy the stated angle within tolerance. Reversing direction or normals follows the documented convention and does not create unexplained mirrored results.

<a id="f071"></a>
### F071 — Surface quality inspection

**Owning tasks:** 15.2, 15.2a/b. **Status:** Bounded sampled face deviation is ready for owner testing: explicit sampled/reference roles, unsigned native distances in world mm, temporary color map, sample statistics, trimmed-out/failed counts and saved grid/scale. One grouped build, 16 selected checks and six reviewed captures pass. Full F071 remains open for zebra/reflection, curvature combs, join continuity, broader/adaptive/global deviation and physical acceptance. [Owner procedure](../tests/SurfaceDeviation.md).

**Packages:** I02 · **First delivery:** P7/P9 · **Likely scope:** Feature

**Goal:** Help users diagnose shape quality and verify surfacing claims beyond shaded appearance.

**Workflow and behavior:** Provide zebra/reflection lines, curvature combs, continuity checks, and deviation maps with visible scale, sampling, units, and reference geometry. Distinguish approximate display sampling from numerical certification and show unsupported/singular regions. Save useful analysis settings without making them geometry features unless requested.

**Complete when:** Compare intentionally smooth and discontinuous joins and a known deviation fixture. The tools reveal the expected differences; colors/combs use documented scales and cannot substitute for the acceptance tolerance of a surface feature.

<a id="f072"></a>
### F072 — Unified Move/Copy dialog

**Owning tasks:** 10.7, bounded tasks 10.7a-d. **Status:** Move and shared-definition Copy branches are ready for owner testing. The explicit action reuses world/occurrence transforms and ghost preview; copying preserves original/source placements and native appearance. The copy batch passes 25 selected checks with five reviewed captures, including Undo/Redo, rollback and save/reopen. Full F072 remains open for independent definitions, point-to-point/alignment and wider transform scope/physical acceptance. [Owner procedure](../tests/OccurrenceMove.md).

**Packages:** U07 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Position or duplicate parts through one consistent interface with precise geometric references.

**Workflow and behavior:** Offer translation, rotation, point-to-point, axis alignment, and coordinate-system alignment, with Move versus Copy explicit. Identify whether the subject is a component occurrence, body transform feature, or supported geometry copy. Show source and destination references, transform order, and a live ghost preview; copy mode declares shared versus unique definition behavior.

**Complete when:** Move a repeated component point-to-point, rotate it, and copy it. The correct occurrence changes, shared source geometry stays intact, and Cancel/Undo restore placement without residual constraints.

<a id="f073"></a>
### F073 — Relocatable manipulator

**Owning tasks:** 10.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U07 · **First delivery:** P4 · **Likely scope:** UI/Feature

**Goal:** Place the movement triad where it makes a positioning task intuitive without changing the part itself.

**Workflow and behavior:** Relocate the manipulator to a vertex, edge midpoint, circle center, datum, coordinate system, or supported inferred point. Orient its axes from explicit references and distinguish editing the manipulator from moving the object. Define whether the chosen pivot is temporary, remembered for the command, or deliberately saved.

**Complete when:** Move the triad to a hole center and rotate around it. Relocating the triad alone leaves geometry unchanged; the resulting transform and preview agree and switching modes does not reset the pivot unexpectedly.

<a id="f074"></a>
### F074 — Precise placement

**Owning tasks:** 10.7, 10.7a/b. **Status:** Bounded precise placement ready for owner testing. Native nested Link movement, explicit world/occurrence frames, arbitrary-axis/pivot rotation and preview/commit agreement pass. A shared world-shape resolver correction includes enclosing Part transforms for native Links. One native build, 54 post-correction affected-consumer checks plus 14 initial appearance/command passes; six captures reviewed. Work-part frames, snapping, broader occurrence scope and physical acceptance remain open. [Owner procedure](../tests/OccurrenceMove.md).

**Packages:** U07, A04 · **First delivery:** P4 · **Likely scope:** Feature/UI

**Goal:** Expose exact coordinate meaning during movement, especially in nested assemblies.

**Workflow and behavior:** Allow global/work-part/component-local coordinates, typed offsets, snapping, and arbitrary-axis rotation. Label whether values are absolute positions or incremental transforms, show reference frames, and preserve units. Compose nested transforms through the shared occurrence service rather than treating displayed coordinates as local values.

**Complete when:** Translate a rotated nested component by a local-axis distance and then a global-axis distance. Reported coordinates and final placement agree with the chosen frames; repeated operations do not apply parent transforms twice.

<a id="f075"></a>
### F075 — Placement versus constraint

**Owning tasks:** 10.7, 12.4, 10.7a/b. **Status:** The one-time Move branch explicitly creates no mate and refuses driven/read-only/consumed links. Placement Undo/Redo and shared-source isolation pass under the F074 batch. Maintained relationships, solver-driven movement and the full paired acceptance example remain open. [Owner procedure](../tests/OccurrenceMove.md).

**Packages:** U07, B02 · **First delivery:** P4/P6 · **Likely scope:** UI/Feature

**Goal:** Separate positioning something once from creating a relationship that stays true after later edits.

**Workflow and behavior:** Move Here commits a placement; Maintain Relationship opens a supported mate/joint workflow with explicit references and degrees of freedom. Do not create hidden constraints from snapping alone. When a component is already constrained, explain whether movement is a solver-driven drag, an arrangement change, or blocked by existing relationships.

**Complete when:** Align two holes once, then move the supporting part: the unconstrained item stays at its placement. Repeat with a persistent relationship and it follows correctly; users can see and undo the relationship.

<a id="f076"></a>
### F076 — Contextual mates/joints

**Owning tasks:** 12.4, 12.4c/d. **Status:** Bounded native joint meaning/reference review and enabled-limit recovery ready for owner testing. Twenty-nine distinct checks pass across accepted runs; six GUI captures reviewed. Python-only staging, no native rebuild. Full F076 remains open for contextual suggestions, ambiguous alternatives, motion/conflict previews, broader assemblies and physical acceptance. [Owner procedure](../tests/JointReview.md).

**Packages:** B02 · **First delivery:** P6 · **Likely scope:** Feature

**Goal:** Suggest useful assembly relationships from selected geometry without hiding their mechanical meaning.

**Workflow and behavior:** Use selected planes, cylinders, axes, and points to offer supported planar, concentric, fixed, revolute, slider, or other available joint forms. Preview remaining freedom, alignment flip, offsets, and limits. Resolve multiple valid interpretations explicitly and use the existing assembly solver where it satisfies the contract.

**Complete when:** Select cylindrical and planar references to position a shaft, inspect the resulting motion, and adjust limits. Conflicting mates are explained and canceled without leaving an overconstrained partial assembly.

<a id="f077"></a>
### F077 — Assembly freedom display

**Owning tasks:** 12.4, 12.4a/b. **Status:** Bounded assembly freedom guidance and native grounded/unconnected selection ready for owner testing. Slider/connectivity distinction, redundant-state recovery, stale refusal, task lifecycle and Undo/Redo/save-reopen pass in 28 selected checks across accepted runs. Initial grouped build plus one corrective build. Full F077 stays open for per-component direction/rank, incomplete-joint and external/nested loading diagnosis and physical acceptance. [Owner procedure](../tests/AssemblyFreedom.md).

**Packages:** B02 · **First delivery:** P6 · **Likely scope:** Feature/UI

**Goal:** Show which components are grounded, movable, fully constrained, or conflicting.

**Workflow and behavior:** Provide consistent status indicators and optional movement/rotation cues from solver state. Grounding is a declared relationship rather than a color convention. Differentiate an unloaded/unresolved component from an underconstrained loaded component and provide navigation to controlling joints or conflicts.

**Complete when:** Inspect an assembly with one grounded base, one slider, one free part, and one conflict. The indicated freedoms match permitted manipulation and update after adding/removing a mate.

<a id="f078"></a>
### F078 — In-context part editing

**Owning tasks:** 12.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A04, B03 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Edit a component using its surroundings while preserving shared-definition and reference scope.

**Workflow and behavior:** Enter the intended occurrence context, visually distinguish the work part, and collect external geometry only through supported associative/snapshot policies. Store occurrence transforms and sources explicitly; warn through scope information when editing a shared definition affects other occurrences. Prevent relationships that create dependency cycles.

**Complete when:** Size a cover from neighboring geometry within a rotated subassembly. The cover edits its intended definition, contextual references transform correctly, and moving or replacing the neighbor updates or produces a repairable reference error.

<a id="f079"></a>
### F079 — Assembly-scoped cuts

**Owning tasks:** 12.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A08 · **First delivery:** P2 proof; P6 product · **Likely scope:** Core

**Goal:** Apply a manufacturing or installation modification to chosen occurrences without modifying every shared source instance.

**Workflow and behavior:** Create the operation in the assembly definition, collect affected occurrence paths and tool geometry, and show derived assembly-local results. Keep original source definitions and unselected occurrences unchanged. An explicit propagate-to-source action, if implemented, previews its broader consequences and rejects inconsistent transforms/scopes.

**Complete when:** Cut one of two occurrences of the same plate, reopen the assembly, and inspect the source part. Only the selected occurrence result is cut; BOM identity policy, drawing output, and subsequent source updates follow documented rules.

<a id="f080"></a>
### F080 — Exploded views and motion

**Owning tasks:** 12.6, 12.7; bounded output tasks 12.7a/b. **Status:** Saved solid-occurrence exploded output is ready for owner testing (28 selected checks and five reviewed captures). Full F080 remains open for broader arrangements, joint-driven motion/limits, consumer coverage and physical acceptance.

**Packages:** B04, B05 · **First delivery:** P6 increments · **Likely scope:** Feature/Core

**Goal:** Explain assembly structure and simple mechanisms without overwriting their modeled placement.

**Workflow and behavior:** Save exploded transforms and assembly arrangements separately from source placements. Provide explode steps, spacing, trails or sequence where useful, plus bounded joint-driven motion with limits. Distinguish visual animation from dynamic/physical simulation. Drawing/BOM consumers choose the intended saved arrangement explicitly.

**Complete when:** Create an exploded view, return to assembled state, and reopen both views. Animate a supported hinged mechanism within limits; source geometry and normal assembly placement remain unchanged.

**Validated checkpoint (2026-10-01):** Existing Assembly steps and explicit
TechDraw Source preserve modeled placements and copied occurrence transforms.
Successive translation/rotation/radial trails, native Accept/Cancel, Undo/Redo and
save/reopen are covered by 12.7a/b. [Owner procedure](../tests/ExplodedViewOutput.md).
The bounded checkpoint does not complete the hinged-motion acceptance above.

<a id="f081"></a>
### F081 — Published interfaces

**Owning tasks:** 12.5, 10.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B03, A05, A09 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Give other parts stable, intentional references instead of exposing arbitrary internal topology.

**Workflow and behavior:** Publish named datums, geometry, and parameters with identity, units/type, description, and source ownership. Consumers select those interfaces through controlled scope. Define rename, replacement, deprecation, and deletion behavior; changing internal construction should not break a maintained published interface unnecessarily.

**Complete when:** Publish mounting axes and spacing, consume them in a bracket, and replace internal source features while preserving the interfaces. Consumers update correctly; deleting an interface identifies affected downstream parts.

<a id="f082"></a>
### F082 — Associative geometry linking

**Owning tasks:** 12.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B03 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Reuse geometry between parts with visible provenance and deliberate update control.

**Workflow and behavior:** Create a link/derived feature from selected published or permitted geometry, preserve the source occurrence transform, and show live, frozen, or independent-copy status. Freezing retains provenance and a defined snapshot; breaking a link deliberately changes future update behavior. Avoid copying hidden source-document internals accidentally.

**Complete when:** Link a surface into another part, move/edit the source, then freeze and later resume updates if supported. Each state behaves as shown, cycles are rejected, and source relocation is repairable.

<a id="f083"></a>
### F083 — External-reference manager

**Owning tasks:** 12.5, 15.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B03, X02 · **First delivery:** P3/P6 · **Likely scope:** Feature/UI

**Goal:** Give users one place to understand and repair dependencies outside the current document.

**Workflow and behavior:** List source definitions/files, dependent features, resolved paths, versions/staleness, loading state, and update/freeze/break actions. Provide missing-path repair and dependency collection without changing geometry silently. Distinguish a missing file, inaccessible source, unsupported format, and intentionally unloaded object.

**Complete when:** Move a project folder, repair a missing source once, and identify all affected consumers. Updating or freezing a dependency has a previewable scope and the manager agrees with saved references.

<a id="f084"></a>
### F084 — Cycle prevention

**Owning tasks:** 7.5, 12.5, 10.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B03, A05, A09 · **First delivery:** P1/P3 · **Likely scope:** Core

**Goal:** Reject dependency relationships that cannot be evaluated deterministically.

**Workflow and behavior:** Check proposed feature inputs, external geometry links, parameter expressions, and configuration dependencies before commit. Include cross-document/occurrence context and report an understandable chain forming the cycle. Handle partially loaded graphs conservatively; do not call an unchecked graph valid.

**Complete when:** Attempt A-to-B-to-A links and an indirect expression cycle across three parts. The attempted final relationship is rejected with the dependency chain and no partially saved or partially computed link remains.

<a id="f085"></a>
### F085 — Reference repair

**Owning tasks:** 7.5, 12.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A05, B03 · **First delivery:** P3/P6 · **Likely scope:** Core/Feature

**Goal:** Recover from changed or missing geometry without rebuilding downstream work blindly.

**Workflow and behavior:** Show the broken reference, its original role/provenance, candidate replacements, and affected consumers. Let the user replace one reference or a clearly bounded group, preview the consequences, and undo the repair. Respect expected type, ownership, orientation, units, and occurrence path; do not choose by nearest face alone.

**Complete when:** Delete a referenced face, select a valid replacement, and preview an extrusion and drawing annotation that depend on it. Commit restores the intended relationships; Cancel preserves the diagnostic state.

<a id="f086"></a>
### F086 — Stable selection intent

**Owning tasks:** 7.1.4, 7.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A05, U05 · **First delivery:** P1/P3 · **Likely scope:** Core

**Goal:** Preserve the meaning of selected geometry across supported topology changes without pretending every edit is resolvable.

**Workflow and behavior:** Combine stable feature/result provenance with explicitly stored selection rules and geometric signatures where appropriate. Define when an edge split maps to several entities, when a merged face remains equivalent, and when ambiguity requires repair. Keep explicit frozen selections distinct from associative intent rules.

**Complete when:** Change upstream topology in a controlled corpus of splits, merges, and symmetry ambiguities. Supported references resolve correctly; ambiguous cases remain unresolved rather than attaching to plausible but wrong geometry.

<a id="f087"></a>
### F087 — Useful failure reporting

**Owning tasks:** 7.5, 10.9, 7.5.7b. **Status:** Bounded native failure/pending inspector ready for owner testing. Lists affected loaded dependents and reachable failed/pending inputs with native details and explicit navigation. Cut failure, linked-result stale export refusal and repair pass; 21 selected checks and five reviewed captures across the F087/F088 batch. Whole F087 remains open for broader failure classification, unique first-cause diagnosis, repair actions and physical acceptance. See [owner procedure](../tests/DocumentUpdates.md).

**Packages:** A07, U11 · **First delivery:** P3/P4 · **Likely scope:** Feature/UI

**Goal:** Explain what failed, what caused it, and what the user can do next.

**Workflow and behavior:** Identify the first failing feature, invalid/missing input, and blocked dependents, with navigation/highlighting and concise corrective actions. Distinguish unsupported input, geometric failure, solver conflict, cancellation, and internal error. Preserve the last valid result only with a visible stale marker and offer optional technical diagnostics separately.

**Complete when:** Break an upstream profile and inspect a downstream cascade. The user is directed to the first cause, not dozens of equivalent errors, and export/CAM cannot quietly treat stale geometry as current.

<a id="f088"></a>
### F088 — Controlled recompute

**Owning tasks:** 7.5.7, 7.5.7a/b. **Status:** Native session deferral and explicit whole-document recompute are ready for owner testing. Cached/pending/failed/affected states, loaded external inputs, cycle refusal, mode preservation, transactions, Undo/Redo and save/reopen pass. One grouped build; 21 selected passing checks and five reviewed captures. Whole F088 remains open for targeted dependency updates, asynchronous progress/cancellation, broader downstream currency and physical acceptance. See [owner procedure](../tests/DocumentUpdates.md).

**Packages:** A07, X03 · **First delivery:** P3/P10 · **Likely scope:** Core/Feature

**Goal:** Let users balance responsiveness and model currency during expensive or grouped edits.

**Workflow and behavior:** Support documented automatic/manual modes, deferred updates within a transaction, and targeted recompute of the necessary dependency closure. Track dirty/stale state at relevant feature/document boundaries. Commands requiring current geometry must update or explicitly refuse/ask for the needed action; manual mode cannot imply unchanged results are current.

**Complete when:** Change several parameters with deferred updates, recompute once, and compare with automatic mode. Results agree; targeted recompute includes required dependencies and stale drawings/toolpaths remain visibly marked.

<a id="f089"></a>
### F089 — Direct STL machining

**Owning tasks:** 6, 14.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C01 · **First delivery:** P8 · **Likely scope:** Feature/Core

**Goal:** Generate supported toolpaths directly from mesh geometry without tessellation-to-B-rep conversion.

**Workflow and behavior:** Accept a mesh as the CAM model through shared units/transforms and a validated mesh-capable algorithm. Audit existing facilities before adding new algorithms. Begin with a bounded three-axis finishing workflow, documenting supported tool shapes, mesh assumptions, and tolerance. Keep roughing/rest machining as distinct required increments.

**Complete when:** Load an STL, declare its units, set placement, generate the supported finishing path, and independently compare expected tool contact within stated tolerance. No thousands-of-faces conversion is required.

Bounded increment: phase 6.4.3 now covers configured per-setup STL post output;
regenerated Waterline contour repeatability and broader F089 acceptance remain open.

<a id="f090"></a>
### F090 — Guided CAM setup

**Owning tasks:** 14.1, 14.1c/d. **Status:** Bounded native model setup review implemented: exact model identity and repeated-source counts, separate mesh candidates, source dimensions/placement in mm, display-unit distinction and changed-input acceptance review. Native mesh/solid job handoff, Undo/Redo and save/reopen pass in 16 selected checks after one grouped staging pass. Full F090 remains open for complete guided setup, final WCS preview, mesh-unit conversion and owner acceptance. [Owner procedure](../tests/JobModelReview.md).

**Packages:** C01, C03, U09 · **First delivery:** P8 · **Likely scope:** UI/Feature

**Goal:** Guide users from a model to a complete machining setup with visible assumptions.

**Workflow and behavior:** Collect model, units, orientation, work coordinate system/origin, stock, machine, tools, boundaries, allowances, and postprocessor in a logical sequence. Show geometry/setup previews and explain missing inputs. Templates can prefill choices but consequential values remain visible, editable, and validated against the selected strategy.

**Complete when:** Create a setup from an STL and from supported solid geometry. Reopening preserves origins, units, stock, and tools; a wrong-scale mesh is obvious before toolpath generation or postprocessing.

<a id="f091"></a>
### F091 — Mesh preparation

**Owning tasks:** 14.1, 14.1a/b. **Status:** Bounded imported-mesh preparation is ready for owner testing: dimensions/topology/orientation/density review and an independent reversed-normal copy preserving the source and existing job links. One build/staging pass, 32 distinct selected checks across accepted runs and five reviewed captures. Full F091 remains open for broader repair, self-intersection and physical acceptance. [Owner procedure](../tests/MeshPreparation.md).

**Packages:** C01 · **First delivery:** P8 · **Likely scope:** Feature

**Goal:** Identify mesh conditions that matter to the chosen machining algorithm and offer controlled fixes.

**Workflow and behavior:** Inspect normals/orientation, holes, nonmanifold regions, disconnected pieces, degenerate triangles, bounds, and excessive density. Distinguish a diagnostic from a required repair: some algorithms tolerate open meshes while others require a solid stock model. Preview repair/decimation effects and never smooth away intentional detail without an explicit tolerance.

**Complete when:** Use inverted, open, disconnected, and dense fixtures. Report which conditions block each supported operation, and verify approved repairs respect dimensions/tolerance while preserving the original mesh.

<a id="f092"></a>
### F092 — Roughing and finishing workflow

**Owning tasks:** 14.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C01, C02 · **First delivery:** P8 staged · **Likely scope:** Feature/Core

**Goal:** Make a useful strategy sequence understandable without implying that a finishing path removes bulk stock safely.

**Workflow and behavior:** Ship finishing first where supported, then add stock-aware roughing with stepdown/stepover, allowance, entry/exit, clearance, and strategy-specific controls. Expose strategy presets as editable values with documented applicability. Carry stock/setup identity between operations and show the resulting order and remaining material assumptions.

**Complete when:** Machine-planning fixtures show roughing leaves the intended allowance and finishing reaches supported surfaces within tolerance. A finishing-only release is labeled clearly; unsupported stock engagement or access is reported.

<a id="f093"></a>
### F093 — Boundary selection on meshes

**Owning tasks:** 14.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C01, C02 · **First delivery:** P8 · **Likely scope:** Feature

**Goal:** Control where a mesh-based strategy may cut and where it must avoid.

**Workflow and behavior:** Offer sketch-based projected containment, supported picked mesh regions, and avoid areas with visible boundary loops. Specify projection direction, open/closed-loop rules, and whether containment applies to tool center, contact point, or tool envelope. Preserve references under mesh placement/unit changes and warn when a region cannot be reidentified.

**Complete when:** Restrict machining to one pocket-like region and protect a raised area. Generated paths respect the documented cutter/boundary rule and a moved mesh cannot leave boundaries silently in the wrong frame.

<a id="f094"></a>
### F094 — Rest machining

**Owning tasks:** 14.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C02 · **First delivery:** P8 after roughing · **Likely scope:** Core

**Goal:** Remove material left by earlier operations using their actual stock assumptions.

**Workflow and behavior:** Reference a preceding stock state or supported remaining-material representation, tool geometry, operation order, and tolerance. Recalculate when any upstream stock/toolpath changes. Distinguish true remaining-stock computation from merely rerunning finishing with a smaller tool; show approximation limits.

**Complete when:** Rough a fixture with a large tool, compute remaining stock, and plan a smaller-tool rest operation. It targets the expected remaining areas and is invalidated when the prior tool or stock changes.

<a id="f095"></a>
### F095 — Stock and collision simulation

**Owning tasks:** 14.3, bounded tasks 14.3a/b. **Status:** Existing CAM Simulator input/coverage review is ready for owner testing. Complete preparation before reset, native tool/operation order, stale-review recovery, source preservation and save/reopen pass in 17 selected checks; five captures reviewed. Native startup is verified separately from removal accuracy/collision acceptance. Full F095 remains open. [Owner procedure](../tests/SimulationReview.md).

**Packages:** C03 · **First delivery:** P8 increments · **Likely scope:** Feature/Core

**Goal:** Show what a supported toolpath removes and identify the checks actually performed.

**Workflow and behavior:** Visualize remaining stock, gouges, tool/holder clearance, and fixture interactions to the implemented fidelity. State whether checks use toolpaths, postprocessed motion, or a machine model; list missing coverage instead of implying complete collision safety. Keep tools, holders, fixtures, stock, and machine envelopes separately defined.

**Complete when:** Run known-clear and deliberately colliding fixtures, compare material removal with an independent reference where available, and verify units/transforms. Simulation results disclose their scope and cannot be presented as proof that real machine motion is safe.

<a id="f096"></a>
### F096 — Setup reuse

**Owning tasks:** 14.4, 14.4a/b. **Status:** Bounded native setup-template reuse is ready for owner testing. Name/revision/unit metadata, compatibility preflight, exact post selection and a visible accepted-settings review work with native job/stock/tool creation. Different-size model reuse, independent setup resources, Undo/Redo and persistence pass in 16 selected checks; six final captures reviewed. Full F096 remains open for recurring operation sequences, collector remapping, complete machine/tool compatibility and physical acceptance. [Owner procedure](../tests/SetupTemplates.md).

**Packages:** C03 · **First delivery:** P8 · **Likely scope:** UI/Feature

**Goal:** Reuse trustworthy machine/tool/setup choices without inheriting stale model references.

**Workflow and behavior:** Provide templates for machines, tools, stock rules, posts, and recurring operation sequences with names, versions, units, and compatibility metadata. Instantiate templates into an editable job, remap geometry collectors, and show unresolved inputs. Keep template changes distinct from modifying existing jobs unless explicitly applied.

**Complete when:** Apply a template to a new model of different size, resolve collectors, and inspect all consequential values. Updating the template does not silently alter previously approved jobs or toolpaths.

<a id="f097"></a>
### F097 — Change tracking

**Owning tasks:** 14.4, 16.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** C03, X05 · **First delivery:** P3/P8 · **Likely scope:** Core/Feature

**Goal:** Prevent outdated machining results from appearing current after their inputs change.

**Workflow and behavior:** Track dependencies on model geometry/placement, stock, tools/holders, fixtures, operation parameters, units, and relevant post settings. Mark affected stages stale and distinguish toolpath regeneration from reposting. If output is exported despite a permitted warning workflow, identify its source revision/state explicitly rather than silently using stale data.

**Complete when:** Change a cutter diameter, stock offset, and model placement separately. Exactly the affected paths/simulations/output states invalidate, and regeneration restores a traceable current state.

Bounded increment: phase 6.4.3 verifies shared-tab/origin invalidation through
real indexed-job export and recovery. Broader input/output-state tracking remains open.

<a id="f098"></a>
### F098 — Unified measurement

**Owning tasks:** 15.1. **Status:** Existing native Measure task gains operand identities and explicit measurement/frame meaning under 15.1a/b, ready for owner testing. Circle-centre versus edge-gap, unit conversion, occurrence world coordinates/unsigned deltas and geometric-centre density disclosure pass. The grouped batch has 13 selected passes and two reviewed captures. Broader material/mass, thickness, mesh-accuracy and physical/high-DPI acceptance remain open. [Owner procedure](../tests/MeasurementContext.md).

**Packages:** I01 · **First delivery:** P9; isolated tools earlier · **Likely scope:** UI/Feature

**Goal:** Inspect common geometric quantities through one tool with explicit meaning and units.

**Workflow and behavior:** Infer and allow choosing distance, angle, radius, thickness, minimum separation, area, volume, center of mass, and mass where supported. Show which entities and frames define a result, whether a value is minimum/projected/local, and what material/density is assumed. Label mesh/approximate measurements and unsupported shell mass cases.

**Complete when:** Measure known analytic fixtures and repeated assembly instances. Values and units are correct; missing density or ambiguous thickness is explained instead of replaced with a misleading default result.

<a id="f099"></a>
### F099 — Persistent measurements

**Owning tasks:** 15.1. **Status:** Distance Free point snapshots now persist explicit fixed-world policy, UTC capture time and informational selection paths under 15.1b. Native save/reopen, source-move independence, direct-coordinate provenance clearing, Undo/Redo and legacy unknown provenance pass. Existing associative distance follows source edits in the companion fixture. Ready for owner testing; broader valid/stale/unresolved associative status, notes/operand navigation and repair remain open. [Owner procedure](../tests/MeasurementContext.md).

**Packages:** I01, A05 · **First delivery:** P9 · **Likely scope:** Feature

**Goal:** Save useful engineering checks so they can be revisited after edits.

**Workflow and behavior:** Store references, measurement type, units, and either associative update behavior or an explicitly dated snapshot. Display valid, stale, and unresolved states; allow names, notes, and navigation to operands. Persisting a measurement does not automatically create a driving constraint or a dependency cycle.

**Complete when:** Save a clearance measurement, move a component, and reopen the document. An associative measurement updates or flags repair, while a snapshot remains labeled with its original state and does not imply current clearance.

<a id="f100"></a>
### F100 — Interactive sections

**Owning tasks:** 15.1, 15.1e/f. **Status:** Bounded section-plane pilot ready for owner testing: explicit mm/world numeric controls, synchronized camera-derived normals, zero-direction recovery and atomic portable preset save/load. All 22 final grouped checks pass and six captures reviewed. Two-plane persistence through separate preset/model reopen and unchanged geometry/Undo/full exports verified. Whole F100 remains open for embedded saved views, caps, section-specific curves/measurements and physical acceptance. See [owner procedure](../tests/SectionPlanes.md).

**Packages:** I01 · **First delivery:** P9 · **Likely scope:** UI/Feature

**Goal:** Inspect interiors and communicate selected cut views without changing modeled geometry.

**Workflow and behavior:** Provide one or more movable section planes with exact offsets/orientations, caps where supported, and saved view definitions. Let users inspect section curves and supported dimensions while distinguishing visual clipping from extracted/intersected geometry. Preserve source occurrence context and keep exports explicit about whether they use the clipped view or full model.

**Complete when:** Create two section planes through a nested assembly, save the view, and move a plane numerically. Reopening reproduces it; model geometry remains intact and section measurements describe the actual selected plane.

<a id="f101"></a>
### F101 — Interference/clearance checks

**Owning tasks:** 15.1. **Status:** Bounded explicit solid-pair inspection completed under 15.1c/d, ready for owner testing. Overlap volume, contact tolerance, minimum-clearance classification, unresolved inputs, explicit exclusions, pair navigation and edit invalidation pass. One grouped build; 23 passing checks and four reviewed captures. Whole F101 remains open for broader nested/external assemblies, per-pair exceptions, large-set acceleration and physical/high-DPI acceptance. [Owner procedure](../tests/InterferenceCheck.md).

**Packages:** I01, B06 · **First delivery:** P9 · **Likely scope:** Feature

**Goal:** Find and navigate assembly conflicts rather than requiring visual inspection of every pair.

**Workflow and behavior:** Choose component sets, exclude intended cases explicitly, and compute interference or minimum clearance with documented tolerance and touching-contact policy. Return pair lists, highlights, magnitudes where meaningful, and unresolved/unloaded participants. Use broad-phase acceleration without skipping required exact checks unnoticed.

**Complete when:** Check an assembly containing an overlap, a touch, a small clearance, and an unloaded component. Results classify each correctly, navigate to the relevant pair, and never label an incomplete check as fully clear.

<a id="f102"></a>
### F102 — Drawing creation wizard

**Owning tasks:** 15.3, 15.3a/b. **Status:** Bounded native drawing setup ready for owner testing: A4/A3 border-only templates, explicit scale/orientation/convention and optional linked top/right views for a root solid/Body. First/third-angle placement, source edits, Undo/Redo, rollback and save/reopen pass. One grouped build, 16 final selected checks and five reviewed captures. Whole F102 remains open for broader sources/templates, graphical preview, section/detail setup, reference repair and physical acceptance. See [owner procedure](../tests/DrawingSetup.md).

**Packages:** D01, X05 · **First delivery:** P9; compatibility P2/P3 · **Likely scope:** UI/Feature

**Goal:** Create common drawings through a guided view/template setup that remains associative.

**Workflow and behavior:** Select source definition/occurrence or arrangement, sheet template, units, scale, projection convention, and base orientation. Add projected, section, and detail views with preview and consistent placement. Keep drawing-only data within the engineering-document contract and preserve explicit external links if stored separately.

**Complete when:** Create a drawing with base/projected/section/detail views, edit the source, and reopen. Supported views update correctly; chosen scale, projection convention, and source arrangement remain explicit and broken references are surfaced.

<a id="f103"></a>
### F103 — Associative annotation

**Owning tasks:** 15.3, 15.3c/d. **Status:** Bounded native dimension reference repair ready for owner testing; 14 distinct selected checks pass after one grouped build. Explicit projected/true reference review clears old 3D links when switching to projection and validates before committing. Full F103 remains open for graphical preview, hole/thread metadata, ambiguous topology repair and physical acceptance. See [owner procedure](../tests/DimensionRepair.md).

**Packages:** D01, A05 · **First delivery:** P9 · **Likely scope:** Feature/Core

**Goal:** Keep dimensions and manufacturing notes attached to the intended geometry through supported edits.

**Workflow and behavior:** Support associative dimensions, center marks/lines, hole callouts, and relevant annotations with clear reference versus driving semantics. Reuse source hole/thread metadata where present; expose tolerances and formatting without duplicating model parameters. Detect lost or ambiguous topology and provide repair with a preview.

**Complete when:** Change a hole size and location, then split an annotated edge. Valid callouts update from source metadata, ambiguous annotations are marked for repair, and the drawing never silently displays a plausible dimension attached to the wrong edge.

<a id="f104"></a>
### F104 — Assembly documentation

**Owning tasks:** 15.4, 15.4a/b. **Status:** Bounded native BOM inclusion is ready for owner testing: sibling-only quantities, assembly scope, explicit per-BOM exclusions independent of visibility, native persistence/Undo/CSV. 21 distinct selected checks pass across accepted runs and five captures reviewed after one successful native build. Arrays/configurations, custom-column identity, balloons/exploded documentation and full F104 acceptance remain open. [Owner procedure](../tests/AssemblyBomScope.md).

**Packages:** D02, B01, B04 · **First delivery:** P9 · **Likely scope:** Feature

**Goal:** Produce BOMs, balloons, and exploded documentation from defined product-structure rules.

**Workflow and behavior:** Define quantities for repeated occurrences, unique parts, configurations, subassemblies, and reference-only/suppressed items. Keep reference-set visibility independent of BOM inclusion. Associate balloons with stable item identities, allow explicit item numbering policies, and use selected exploded arrangements for views.

**Complete when:** Document an assembly containing repeats, a unique copy, an empty reference set, and reference-only hardware. Quantities and balloons match the stated rules and remain stable or explicitly renumbered after supported edits.

<a id="f105"></a>
### F105 — Additional modeling modules

**Owning tasks:** 15.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X01 · **First delivery:** P9 by module · **Likely scope:** Feature/Core

**Goal:** Integrate useful sheet-metal, frame/weldment, and standard-hardware workflows without making them prerequisites for core modeling.

**Workflow and behavior:** Audit compatible modules first. Sheet metal should track thickness, bend rules, reliefs, and unfold/refold intent; frames should place profiles along paths and expose trim/joint/cut-list behavior; hardware should insert reusable parameterized definitions with source/standard metadata. Each is a separately scoped module using shared identity, units, references, and UI contracts.

**Complete when:** A bounded sheet-metal part unfolds/refolds as documented, a frame produces a consistent cut list, and repeated hardware preserves instance/BOM semantics. These are separate deliverables; passing one does not mark the whole package complete.

<a id="f106"></a>
### F106 — Responsive previews

**Owning tasks:** 8.1.6, 16.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X03, A07 · **First delivery:** P3/P10 · **Likely scope:** Feature/Core

**Goal:** Keep expensive commands responsive and make the difference between preview and final geometry clear.

**Workflow and behavior:** Use cancellable computation, progress feedback, and reduced-cost previews where useful. Give each request an input revision/token; discard late results after parameter changes, cancellation, or document closure. Use safe worker boundaries and commit geometry only on the appropriate thread/transaction path. Clearly indicate approximation and revalidate the final result.

**Complete when:** Rapidly change a complex feature, cancel, and close the document during a preview. No stale result commits, the UI remains recoverable, and final geometry meets the full tolerance contract rather than the preview approximation.

<a id="f107"></a>
### F107 — Large-assembly handling

**Owning tasks:** 12.8, 16.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** B06, X03 · **First delivery:** P6/P10 after measurement · **Likely scope:** Core

**Goal:** Scale shared-instance assemblies while preserving correctness and complete model state.

**Workflow and behavior:** Reuse geometry/tessellation across instances where supported, use selective loading and simplified representations, and profile culling/rendering separately from recompute. Visibility-based display optimizations must not suppress required dependency evaluation or omit hidden parts from engineering checks. Record cache keys by source/configuration/revision.

**Complete when:** Measure fixed assemblies at increasing instance counts on named hardware. Improvements are attributable to recorded bottlenecks; repeated geometry renders in correct transforms, and full-resolution checks still include required hidden/unloaded participants.

<a id="f108"></a>
### F108 — Project packaging

**Owning tasks:** 15.6, 15.6a/b, 16.1. **Status:** Bounded saved-native packaging ready for owner testing. Recursive relative XLink review, byte-preserving portable ZIP/manifest, no-overwrite publication and source-change guards are implemented. A relocated nested/repeated-link assembly opens, updates and saves/reopens without its original folder. One grouped native build, 15 distinct passing checks and six reviewed captures; [owner procedure](../tests/ProjectPackage.md). Absolute-link repair, external asset/code collection, independent duplication, format migration and physical owner acceptance remain open.

**Packages:** X02, X04 · **First delivery:** P3/P9 · **Likely scope:** Feature/Core

**Goal:** Move or share a project with its dependencies while preserving intentional identity relationships.

**Workflow and behavior:** Collect required files and supported embedded assets, preview missing/external references, and create a package manifest with portable paths. Specify Save Copy as a file/package operation versus Make Unique as new definition identity; document whether a copied project remains linked to external originals. Offer deliberate relinking and independent duplication.

**Complete when:** Package a nested assembly, move it to a different directory, and open it without the original path. Supported references resolve, omitted sources are listed, and a copy cannot accidentally overwrite or redirect the original project.

<a id="f109"></a>
### F109 — Compatibility strategy

**Owning tasks:** 7.6, 16.1, 16.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** A06, X04, X09 · **First delivery:** P1/P3/P10 · **Likely scope:** Core

**Goal:** Make native, legacy, and exchange behavior predictable as the fork diverges.

**Workflow and behavior:** Maintain a tested matrix for opening, displaying, editing, converting, and exporting representative FreeCAD/fork objects. Use `.cadprt` for new native documents and preserve original `.FCStd` files during conversion. Detect required capabilities from content, report losses, and refuse unsafe saves; an extension alone is not a compatibility check.

**Complete when:** Import supported legacy fixtures, convert a copy, and reopen with full editability for supported features. Unsupported objects/add-ons are named explicitly; native data is never silently dropped to produce an apparently successful legacy export.

<a id="f110"></a>
### F110 — Consistent automation

**Owning tasks:** 16.5, 16.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X03, A07 · **First delivery:** P3/P10 · **Likely scope:** Feature

**Goal:** Expose the same modeling behavior through scripts and reproducible operation recording.

**Workflow and behavior:** Provide stable command/model APIs with explicit inputs, operation/target identities, units, context, and transaction behavior. Record committed semantic actions rather than raw mouse coordinates; include deterministic replay fixtures and meaningful errors. Preview-only state and private filesystem/account data should not enter a shareable recording by accident.

**Complete when:** Record or script a bracket workflow, replay it headlessly where supported, and compare parameter relationships/results. UI and automation reject the same invalid targets and do not depend on whichever document or body happened to be active.

<a id="f111"></a>
### F111 — Upstream-friendly implementation

**Owning tasks:** 16.3, 16.6. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X03 · **First delivery:** P0/P10 · **Likely scope:** Feature/Core

**Goal:** Keep long-term maintenance feasible while preserving deliberate product differences.

**Workflow and behavior:** Record upstream base and fork-specific decisions; separate UI adapters, feature additions, and model/persistence changes into reviewable patches where practical. Reuse supported extension points, upstream useful general fixes, and retire adapters when shared contracts replace them. Do not preserve an incompatible architecture merely to minimize a diff.

**Complete when:** Integrate a representative upstream update using documented build/tests and the divergence map. Conflicts have identifiable owners/reasons, and supported legacy/new workflows still pass their release gates.

<a id="f112"></a>
### F112 — Guided workflows and progressive disclosure

**Owning tasks:** 10.2, 10.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U09, U11 · **First delivery:** P3/P4 · **Likely scope:** UI/Feature

**Goal:** Make common commands teach their own sequence while giving experienced users a direct, efficient route.

**Workflow and behavior:** Use one command state model for guided prompts, preselection, direct field editing, preview, and commit. Show the next unresolved input; keep consequential operation/target choices visible and reveal advanced options on demand. Help is specific to the active step and explains valid selections, not a mandatory tour. Preserve already valid choices when moving back.

**Complete when:** A first-time user completes Extrude from prompts; an experienced user performs the same operation through preselection and typed values. Both create equivalent editable features and can correct an earlier input without restarting.

<a id="f113"></a>
### F113 — Intelligent initial operation suggestions

**Owning tasks:** 10.3. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** U10, A02 · **First delivery:** P1/P4 · **Likely scope:** Feature/Core

**Goal:** Reduce routine Boolean decisions without taking control away from the user or changing saved intent.

**Workflow and behavior:** Within the editable work part, suggest New Body for no eligible intersection and Unite for exactly one valid eligible target. Require explicit resolution for multiple candidates; explain invalid contact and exclude unrelated component geometry from automatic mutation. Pocket/Groove start in Subtract. Manual choice takes precedence, and accepted mode/targets become stored feature parameters.

**Complete when:** Test zero, one, multiple, tangent-invalid, and cross-component candidates. Editing a committed Unite until it no longer intersects produces defined failure/repair behavior, not a silent conversion into New Body.

<a id="f114"></a>
### F114 — Selection-aware constraint eligibility

**Owning tasks:** 11.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** S07, S02, S04 · **First delivery:** P1 audit; P5 · **Likely scope:** Feature/Core

**Goal:** Show only relevant sketch actions and clearly distinguish a mathematical conflict from the wrong selection shape.

**Workflow and behavior:** Use selection type/count/roles for fast applicability: one line exposes supported single-line relations and construction/reference actions; two suitable lines add Parallel/Perpendicular. For applicable actions, use solver evidence to mark Valid, Already Applied, Redundant, Conflicting, Unsupported, or Unverified. Proven conflicts are disabled with reasons. Reuse this service in palettes, menus, toolbars, shortcuts, and commit validation.

**Complete when:** Selecting one line never suggests a two-line relation as immediately executable. A constrained horizontal line's Vertical candidate is evaluated correctly for its actual sketch state; stale checks cannot mutate the sketch or disable valid actions based on guessed conflicts.

<a id="f115"></a>
### F115 — Native .cadprt engineering documents

**Owning tasks:** 7.6, 16.1. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X04, A06 · **First delivery:** P1/P3/P10 · **Likely scope:** Core

**Goal:** Provide a recognizable native format for the entire application and reliable behavior as schemas evolve.

**Workflow and behavior:** Use a stable internal format identity, schema/capability declarations, producer metadata, and explicit part/document relationships. Preserve supported CAD, assembly, drawing, CAM, FEM, and Draft data; reject or safely retain unsupported required content. Reuse suitable existing container infrastructure rather than inventing a new binary format unnecessarily. Legacy conversion is explicit and preserves originals.

**Complete when:** Round-trip a mixed engineering document and an externally linked assembly. Required unknown capabilities, corrupt content, and legacy-only objects produce clear controlled outcomes; native files are not accepted or overwritten solely because their filename has the expected suffix.

<a id="f116"></a>
### F116 — Early cross-workbench compatibility

**Owning tasks:** 16.2. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X05 · **First delivery:** P2/P3 then each core change · **Likely scope:** Core/Feature

**Goal:** Discover downstream consequences of ownership changes before many commands depend on the new model.

**Workflow and behavior:** Include small existing drawing, CAM, FEM, and Draft consumers in the architecture proof. Verify references, transforms, units, materials/supports/loads, invalidation, and save/reopen through shared adapters. Distinguish geometry compatibility from a complete redesigned downstream UI; broaden each module only after this foundation works.

**Complete when:** Changing a shared definition and making an assembly-local cut affect the correct drawing views, CAM model, FEM assignments, and Draft references. Unsupported paths are explicit and stale meshes/toolpaths/results cannot appear current.

<a id="f117"></a>
### F117 — Task benchmarks and release evidence

**Owning tasks:** 16.4, 16.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** Q01 · **First delivery:** P0 onward · **Likely scope:** Process/Validation

**Goal:** Judge progress by usable engineering outcomes and reliable edits rather than command counts.

**Workflow and behavior:** Maintain task 16.4's fixed benchmark tasks, recorded builds/hardware, learning-versus-practiced comparisons, completion/error/recovery measurements, and relevant geometry/persistence checks. Measure new workflow benefits against stock FreeCAD and selected available comparators. Establish acceptance thresholds before evaluating a release and revise engineering estimates using actual work.

**Complete when:** A release report links each advertised workflow to completed task evidence and states unverified cases. Performance, click-count, time-saving, and adoption claims are not fabricated from demonstrations or code generation.

<a id="f118"></a>
### F118 — Model-led onboarding and outreach

**Owning tasks:** 17.2, 17.3, 17.4. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X07, M02 · **First delivery:** P4/P11 · **Likely scope:** Product/Documentation

**Goal:** Give people a concrete useful result that makes trying FC Plus worthwhile.

**Workflow and behavior:** Publish-ready examples include named parameters, units/descriptions, editable native sources, suitable fabrication exports, version information, and a short path to changing two dimensions. Prepare concise videos plus complete tutorials and channel-specific materials for Thingiverse/Printables, relevant Facebook groups, creators, forums, makerspaces, and search. Posting still follows actual authorization.

**Complete when:** A representative user can install/open the supported build, customize the sample, save, and export without a general CAD course. Track this success and subsequent independent use separately from model downloads or social impressions.

<a id="f119"></a>
### F119 — Independent branding and format discoverability

**Owning tasks:** 17.6, 17.7. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** M03, X04 · **First delivery:** Identity early; P10/P11 · **Likely scope:** Product/Documentation

**Goal:** Make the relationship to FreeCAD and the meaning of .cadprt clear without implying endorsement or exclusivity.

**Workflow and behavior:** Retain FreeCAD-Plus as the working name until a rename is chosen. Publish differences, compatibility, support destination, upstream credits, and stable format documentation. Evaluate a distinct public brand before major incompatible distribution. Optional FileInfo listing, IANA media-type registration, and installer association follow the process and limitations in tasks 17.6-17.7; they are not exclusive ownership claims.

**Complete when:** Release copy accurately describes the independent fork and supported imports/exports. Installers and sample files identify the format consistently, and any proposed registration identifier is not presented as assigned before it actually is.

<a id="f120"></a>
### F120 — Free releases, licensing, and maintenance sustainability

**Owning tasks:** 16.7, 17.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X06, X03 · **First delivery:** P0/P10 · **Likely scope:** Release/Process

**Goal:** Keep the application free for the foreseeable future and make each distributed build maintainable and properly accompanied.

**Workflow and behavior:** Preserve the free local-core commitment, audit actual code/dependency/asset terms, and prepare matching source/build materials and required notices as described in tasks 16.7 and 17.8. Record supported platforms and capability limits. Treat support, donations/sponsorship, hosted services, or paid distribution as optional later business decisions rather than reasons to build billing now.

**Complete when:** Each released binary has traceable source/build/license materials and a documented maintenance/support route. A future revenue discussion cannot silently introduce paywalls, unsupported proprietary claims, or mandatory cloud dependencies.

<a id="f121"></a>
### F121 — Audience and adoption research

**Owning tasks:** 17.1, 17.5. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** M01, M02 · **First delivery:** P0/P11 · **Likely scope:** Research/Product

**Goal:** Use real tasks and repeated use to refine which users the fork serves first.

**Workflow and behavior:** Keep hobbyist, professional, small-team, and small-company populations distinct. Use task 17.1's dated, verified competitor evidence to choose comparisons, then learn from frustrated/lapsed FreeCAD users, experienced CAD users, and small teams separately. Track migration barriers, compatibility needs, support load, first success, and a second real project.

**Complete when:** Product and release choices can point to observations or clearly labeled hypotheses. No probability of adoption or market-share claim is inferred merely from an enthusiastic model audience, a recognizable extension, or the owner's workflow expertise.

<a id="f122"></a>
### F122 — Named parameters, expressions, and units

**Owning tasks:** 10.8. **Status:** Part-level length/angle pilot ready for owner testing (10.8aa/ab); full F122 acceptance, broader scope, publication and where-used remain pending.

**Packages:** A09 · **First delivery:** P1/P3; editor P4/P5 · **Likely scope:** Core/Feature

**Goal:** Make design intent visible and reusable so people can customize a model without hunting through its entire feature history.

**Workflow and behavior:** Provide a part-level parameter editor with names, descriptions, types/units, values/expressions, and where-used links. Reuse existing expression facilities where adequate; define document/part/configuration scope, dimensional checking, cycles, renaming, and controlled publication to other parts. Common feature fields accept compatible expressions. Separate UI display units from stored physical meaning.

**Complete when:** Drive enclosure width, lid clearance, and hole spacing from named values, rename a parameter, and change display units. All intended consumers update; incompatible units and cycles are rejected; a shared definition does not accidentally acquire occurrence-local geometry parameters.

<a id="f123"></a>
### F123 — Contextual workspace, help, and accessibility

**Owning tasks:** 10.9, 10.9a/b. **Status:** Bounded offline command-help and keyboard/display recovery pilot ready for owner testing. Thirteen guides extend existing command search with native live availability, scrollable plain-text detail, local F1/Ctrl+L and window-only layout reset. Eighteen selected checks pass across accepted suites, with six reviewed captures including actual rendered 20-point text. Whole F123 remains open for broader workspace/keyboard workflows, command explanations, localization and physical accessibility/high-DPI acceptance. See [owner procedure](../tests/CommandSearch.md).

**Packages:** U11 · **First delivery:** P3/P4 · **Likely scope:** UI/Feature

**Goal:** Keep navigation, command availability, help, and accessibility coherent across modeling and supported engineering tasks.

**Workflow and behavior:** Use shared context/selection services for command availability and explain disabled operations. Offer local contextual help, searchable terminology, keyboard focus/order, configurable shortcuts, high-DPI sizing, text alternatives to color, and preference reset. Keep separate UI preferences from document semantics. Transition to drawing/CAM/FEM tasks without losing the identity of the active engineering document.

**Complete when:** Complete representative modeling and downstream setup tasks with keyboard navigation and enlarged display settings. Missing selections and wrong work context are recoverable from the interface; changing a preference does not change saved geometry.

<a id="f124"></a>
### F124 — Sketch placement and support management

**Owning tasks:** 11.7. **Status:** Same-container planar support editor is ready for owner testing under 11.7y/z. Installed core and native menu expose current support, explicit replacement, preserve-local/world numeric preview and undoable Apply/repair. All 39 selected checks pass, including rotated placement, constrained sketch/downstream extrusion, missing-face repair, Undo/Redo and save/reopen; three captures reviewed. Cross-part reference adapter stays test-only. Graphical preview, broader datum/occurrence and external-projection behavior and physical/high-DPI acceptance remain open. [Owner procedure](../tests/SketchSupport.md).

**Packages:** S08, A05 · **First delivery:** P1/P3 contracts; P5 · **Likely scope:** Feature/Core

**Goal:** Make where a sketch lives, how it is oriented, and how it follows its support understandable and repairable.

**Workflow and behavior:** Create a sketch on principal/datum planes or supported planar faces with explicit origin, axes, offsets, and attachment mode. Prefer stable datums where the workflow calls for them without banning face attachment. Provide support inspection and reattachment with a preview; distinguish preserving local coordinates from preserving world-space placement and warn about changed downstream geometry.

**Complete when:** Create an offset sketch on a rotated component, change its support, and repair a lost face reference. Orientation, external projections, dimensions, and occurrence transforms follow the selected policy; reattachment is undoable.

<a id="f125"></a>
### F125 — Recovery and document lifecycle

**Owning tasks:** 16.8. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X08, X04 · **First delivery:** P1/P3/P10 · **Likely scope:** Core/Feature

**Goal:** Protect editing work and make file identity, saving, and recovery predictable as documents become more complex.

**Workflow and behavior:** Provide dirty/read-only indicators, recent files with missing-path repair, intentional document templates, atomic save where supported, rotating recovery snapshots, and a recover-as-copy workflow. Define treatment of external dependencies and interrupted multi-file saves; do not claim cross-file atomicity unless implemented. Keep normal save, backup/recovery, Save Copy, and Make Unique distinct.

**Complete when:** Interrupt a controlled save/recovery fixture and recover a clearly labeled editable copy without overwriting a good original. Missing external sources remain explicit, and restoring a snapshot does not silently change definition identity or relink unrelated projects.

<a id="f126"></a>
### F126 — Add-on, macro, and API compatibility

**Owning tasks:** 16.9. **Status:** Follow the owning task evidence; expanded acceptance remains pending unless explicitly validated there.

**Packages:** X09, X03 · **First delivery:** P0 audit; P3/P10 · **Likely scope:** Feature/Core

**Goal:** Keep useful extensions usable where feasible and make incompatibility visible as the fork changes.

**Workflow and behavior:** Inventory important workbenches/macros/APIs, publish supported versions/capabilities, and test representative integrations against the changed ownership and document model. Prefer adapters and staged deprecation where practical. Detect unavailable required add-ons in files and preserve/refuse their data safely. Do not promise all upstream extensions work or silently run an incompatible migration.

**Complete when:** Open fixtures requiring a supported and an unavailable extension, replay a representative macro, and review migration diagnostics. Supported integrations work through stable contracts; unsupported ones identify a concrete dependency without corrupting the model.

<a id="f127"></a>
### F127 — Manufacturing export and reusable output presets

**Owning tasks:** 15.7. **Status:** Bounded solid/occurrence STL handoff and reusable quality presets are ready for owner testing under 15.7a/b. Explicit mm/world placement, stable selected identities, stale/unsupported-input guards and overwrite recovery pass; reimport verifies dimensions, volume and occurrence transforms, and Fine improves the curved fixture over Coarse. All 20 selected checks pass; two dialog captures reviewed. STEP/3MF/DXF, configuration/orientation/unit overrides, mesh inputs, deep occurrence members and physical/high-DPI acceptance remain open. [Owner procedure](../tests/ManufacturingExport.md).

**Packages:** X10, X02 · **First delivery:** P3 contracts; P4/P9 UI · **Likely scope:** Feature

**Goal:** Make reliable handoff to printing, machining, and other tools part of the everyday workflow.

**Workflow and behavior:** Provide explicit geometry/occurrence/configuration selection, units, placement/orientation, quality/tessellation, and output paths for supported STEP, STL, 3MF, DXF, and other audited formats. Offer reusable presets with visible consequential values. Validate watertightness or supported output properties where relevant and report lost history/metadata; never label a geometry export a parametric native file.

**Complete when:** Export a dimensioned part and selected assembly occurrences using supported formats, reopen/check dimensions and transforms, and compare coarse/fine mesh settings. Stale geometry and unsupported entities are disclosed and presets cannot silently export the wrong configuration.
