# FreeCAD Plus: Build validation handoff

Release 0.0.2 is built, validated and publicly published after 0.0.4:
https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.2
Packaging/tag: 71358d8fbf40122e6c998008e7ab3ca741dbc773; unchanged application:
802e19d64863ecdfc02817a2160b621579c2d8f2. All 14,584 runtime file hashes match the
0.0.4 tested payload, so its 312-pass evidence is reused rather than rerun.
New installer checks pass: all 14,586 installed hashes, launch/save/reopen,
shortcut/registration, uninstall and unrelated-file preservation. One Windows
installer asset, 356,439,411 bytes, unsigned; GitHub digest matches SHA256
69d9b406904bb49c22f1efddc1769bae10147edbe38ae0bc1c8993796bb0ddfe.
Evidence: D:\Temp\Office-PC\freecad-plus-release-0.0.2. Release ID 399816257;
public pre-release and source tag verified. Disposable installation removed.
Existing releases unchanged. Physical-machine, clean-VM and broader roadmap
acceptance remain open; no new application features were added in this packaging task.

Release 0.0.4 is built, validated and publicly published:
https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.4
Source/runtime/tag: 802e19d64863ecdfc02817a2160b621579c2d8f2.
Full native build passed, CAM startup fixes 16.2bs/bt passed 55 grouped tests, and
all 312 final packaged regressions pass with zero failures/errors/skips. Installed
launcher/save/reopen, 15,532 installed file hashes, shortcut/registration and
uninstall preservation checks pass. One Windows installer asset, 360,831,616 bytes,
GitHub digest matches SHA256 e5ea99f9b3e556c65f6dadcc5ade42eb4e2531b79f55ae5757ec9eec891e7464.
Evidence: D:\Temp\Office-PC\freecad-plus-release-0.0.4. Public pre-release verified;
release ID 399799828. Installer unsigned; engine remains 26.3.0. Physical-machine,
clean-VM and broader roadmap acceptance remain open. Disposable installation removed;
only the deliberate unrelated-file preservation fixture remains.

Release 0.0.1 Windows x64 installer is built, accepted and published:
https://github.com/Croft-Labs/FreeCAD-Plus/releases/tag/0.0.1
Verified public pre-release state, one installer asset and matching GitHub SHA256.
Release/tag commit 1a962bb23d; application source 2df76790b4. Evidence/artifact root:
D:\Temp\Office-PC\freecad-plus-release-0.0.1. Full build plus revision refresh
reports application source 2df76790b4; 120 staged tests pass and staged/installed
launcher, installed hashes, shortcut and uninstall checks pass. Unrelated test file
survives uninstall. Publication complete; see roadmap release checkpoint.
Packaging uses separate per-user FreeCADPlus settings and does not alter upstream
FreeCAD. The distribution version differs from the retained 26.3.0 engine version.

Latest roadmap batch: 16.2bq/br Plunge Milling postprocessing and persistence probes.
Grouped validation: 87 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-post-reopen-20260930-batch.
Macro PASS; process ended. G83 output passes real LinuxCNC and Grbl processors with
a mock job/configuration wrapper. FCStd reopen and forced regeneration preserve
settings and commands. Existing engine 2df76790b4 plus staged Python fixes; no native
rebuild, production changes or release. Other post/cycle combinations and physical
controller/machine acceptance remain pending.

Previous roadmap batch: 16.2bo/bp Plunge Milling cycle settings and variants.
Grouped validation: 84 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-cycles-20260930-verified.
Macro PASS; process ended. Source/staged PlungeMilling.py hashes match. Initial
negative-depth fixture correction is recorded in the roadmap. G82/G83/G73 command
checks now pass; controller postprocessing and physical machine acceptance remain
pending. Engine 2df76790b4; no native rebuild or release.

Previous roadmap batch: 16.2bm/bn Plunge Milling motion and cycle feed/cancellation.
Grouped validation: 82 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-motion-20260930-verified.
Macro PASS; process ended. Source/staged PlungeMilling.py hashes match. Initial
assertion corrections and final cycle retract are recorded in the roadmap.
Engine 2df76790b4; no native rebuild or release. Ordinary plunge/G81 command checks
pass; peck/dwell variants, postprocessor and physical machine acceptance remain open.

Previous roadmap batch: 16.2bk/bl Dogbone readiness and cutter validation.
79 CAM failure/recovery checks and 24 Dogbone geometry checks pass; zero final
failures/errors/skips. Evidence under D:\Temp\Office-PC\freecad-plus-validation-20260928:
cam-dogbone-readiness-20260930-batch and cam-dogbone-geometry-20260930-verified.
Macros PASS; processes ended. Source/staged DogboneII.py hashes match. Initial
geometry mock correction is recorded in the roadmap. Engine 2df76790b4; no native
rebuild or release. Physical GUI/machine acceptance remains pending; native skipped
recompute caching remains export-blocked.

Previous roadmap batch: 16.2bi/bj Plunge Milling/Boundary input readiness.
Grouped validation: 77 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-boundary-readiness-20260930-batch.
Macro PASS; process ended. Source/staged PlungeMilling.py and Boundary.py hashes match.
Engine 2df76790b4; no native rebuild or release. Explicit generation rejects stale
base/stock inputs and clears output; repaired inputs recover. Native skipped
execution may retain export-blocked caches. Physical GUI/machine acceptance pending.

Previous roadmap batch: 16.2bg/bh Dragknife/Ramp Entry input readiness.
Grouped validation: 74 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-entry-readiness-20260930-batch.
Macro PASS; process ended. Source/staged Dragknife.py and RampEntry.py hashes match.
Engine 2df76790b4; no native rebuild or release. Explicit generation clears/rejects
stale inputs and repairs regenerate output; skipped-native-recompute caches remain
export-blocked. Physical GUI/machine acceptance remains pending.

Previous roadmap batch: 16.2be/bf Axis Map/Z Correction readiness and cache cleanup.
Grouped validation: 72 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-axis-zcorrect-readiness-20260930-batch.
Macro PASS; process ended. Source/staged AxisMap.py and ZCorrect.py hashes match.
Engine 2df76790b4; no native rebuild or release. Native skipped-recompute caches
remain export-blocked; explicit generation clears/rejects stale inputs. Physical
GUI/machine acceptance remains pending.

Previous roadmap batch: 16.2bc/bd production Array/Mirror input readiness.
Shared requireCurrent guards base paths and Mirror center/reference geometry.
Grouped validation: 69 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-array-mirror-readiness-20260930-verified.
Macro PASS; process ended. Array.py/Mirror.py staging hashes match source; engine
2df76790b4, no native rebuild or release. Explicit generation rejects and clears
stale output; skipped-native-recompute caching remains export-blocked. Physical
GUI/machine acceptance remains pending. Initial fixture correction is in roadmap.

Previous roadmap batch: 16.2ba/bb production Boundary2 linking and empty results.
Linking uses native command Parameters for Z; empty clipping emits no moves.
Grouped validation: 66 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-boundary-links-20260930-final.
Macro PASS; process ended. Boundary2.py source/staging hashes match; engine
2df76790b4, no native rebuild or release. Earlier fixture failures and corrections
are recorded in the roadmap. Physical GUI/machine acceptance remains pending.

Previous roadmap batch: 16.2ay/az production holding-tag setup/query checks.
Setup clears path/tool caches, validates base readiness and positive finite tool
diameter; direct point queries rebuild current setup rather than reuse stale data.
Invalid tool/producer checks, export blocking and recovery pass.
Grouped validation: 64 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-tag-setup-20260930-batch.
Macro PASS; process ended. Matching Tags.py staged into engine 2df76790b4;
no native rebuild or release. Query interaction performance/physical acceptance
remain unmeasured; native skipped-recompute caching remains as documented.

Previous roadmap batch: 16.2aw/ax production direct holding-tag edit safeguards.
processTags clears old output and checks base readiness; setXyEnabled refreshes
path data and checks inputs before replacing Positions/Disabled. Direct failure/
repair tests pass; no physical task-panel acceptance is claimed.
Grouped validation: 62 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-tag-direct-edit-20260930-batch.
Macro PASS; process ended. Matching Tags.py staged into engine 2df76790b4;
no native rebuild, release or machine testing. Native skipped-recompute cache
behavior from 16.2au/av remains unchanged and export-blocked.

Previous roadmap batch: 16.2au/av production dressup input readiness.
Utils.requireCurrent guards Boundary2 base/boundary and holding-tag base execution.
Explicit generation rejects stale dependencies and clears output; repair recovers.
Grouped validation: 60 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-dressup-readiness-20260930-verified.
Initial batch had two expectation failures: native recompute can skip downstream
execution after upstream failure, retaining cache. Tests now verify export rejects
that cache before explicit execution clears it. Automatic skipped-execution cache
clearing and direct task callbacks remain separate gaps. Macro PASS; process ended.
Three matching modules staged into engine 2df76790b4; no native rebuild or release.

Previous roadmap batch: 16.2as/at production Boundary2 failure handling.
Output clears before generation; null/invalid/non-solid offsets reject before
clipping. Tests verify late-generation failure and null/plane offsets produce empty
Invalid output, block export and recover after correction.
Grouped validation: 58 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-boundary2-failures-20260930-batch.
Macro PASS; process ended. Matching Boundary2.py staged into engine 2df76790b4;
no native rebuild, release, machine or physical GUI acceptance.

Previous roadmap batch: 16.2aq/ar production holding-tag failure behavior.
Missing base clears cached path/tag/solid/pathData. Processing exceptions clear
output and propagate instead of substituting the untagged base path; native invalid
state blocks export and recovery regenerates tags. Separate from stock-bridge tabs.
Grouped validation: 56 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-holding-tag-failures-20260930-batch.
Macro PASS; process ended. Matching Tags.py staged into isolated engine 2df76790b4;
no native rebuild, release, machine or physical GUI acceptance.

Previous roadmap batch: 10.8y/z explicit Part parameter-set creation/editor entry.
create_parameter_set owns an undoable native container-creation transaction;
edit_parameter_set targets an explicit Part-owned container independently of active
document state. Ownership, Body/occurrence rejection and save/reopen pass.
Grouped validation: 75 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-part-scope-20260930-verified.
Initial batch had one empty-transaction fixture mismatch; corrected with a real
caller label edit. Macro PASS; process ended. Engine 2df76790b4; no native rebuild
or release update. Prototype only; full scope/publication/where-used and production
registration remain pending. Container creation is separate from editor lifetime.

Previous roadmap batch: 10.8w/x enclosure editor acceptance checks.
Actual prototype widgets drive width/clearance/spacing geometry, rename and inch
display. Unit/cycle/zero-width errors preserve geometry and remain correctable;
save/reopen allows editing through a fresh dialog. Application code unchanged.
Grouped validation: 73 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-enclosure-editor-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Automated T13 prototype slice is connected end to end; physical input/accessibility,
production integration and broader parameter requirements remain pending.

Previous roadmap batch: 10.8u/v native enclosure parameter benchmark.
Width/lid clearance/hole spacing drive native geometry; rename, unit/cycle rejection
and persistence pass. Shared occurrence placements and separate-definition isolation
survive parameter edits and Undo/Redo. This is bounded T13 evidence, not production UI.
Grouped validation: 71 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-enclosure-20260930-verified.
Initial batch had one fixture-readiness error; recompute after visibility setup fixed
it. Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Production integration, full physical T13 and broader occurrence consumers remain open.

Previous roadmap batch: 10.8s/t parameter descriptions and display-only units.
Creation stores native property documentation; read-only description survives
Undo/Redo, rename and save/reopen. Dialog length/angle display conversion leaves
stored values, expressions and geometry unchanged; no unit preference is persisted.
Grouped validation: 69 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-units-description-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Uninstalled prototype. Existing-description editing, localized display, physical
accessibility, full T13 and production integration remain pending.

Previous roadmap batch: 10.8q/r typed parameter creation prototype and dialog.
create_parameter adds native Length/Angle properties atomically, with explicit units
and ASCII identifier names. Invalid names/units/references leave no partial property.
Creation supports Undo/Redo/persistence; dialog correction and selection checks pass.
Grouped validation: 67 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-create-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Still uninstalled: parameter-object creation, deletion/where-used/publication,
broader types/scope, physical UI/accessibility and production integration remain open.

Previous roadmap batch: 10.8o/p prototype parameter-list and two-editor handling.
Loading a stale dropdown disables edit controls and requires Refresh. External
rename/removal, empty lists and subsequent additions recover. Same-object dialogs
reject conflicting drafts; closing one does not remove the other's observer.
Grouped validation: 65 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-editor-schema-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
The editor remains an uninstalled prototype. Physical UI/accessibility, broader
reference synchronization and full production parameter functionality remain open.

Previous roadmap batch: 10.8m/n parameter editor refresh/conflict and lifecycle.
External value/Undo changes reject stale Apply/Rename until explicit Refresh.
Deleting the parameter object or document closes the dialog and detaches observation;
subsequent edit calls do nothing. The dialog remains an uninstalled prototype.
Grouped validation: 62 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-editor-lifecycle-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
External property-list interaction, multi-dialog and physical UI/accessibility need
further acceptance; production integration and broader parameter requirements remain open.

Previous roadmap batch: 10.8k/l uninstalled parameter editor dialog prototype.
Existing length/angle selection, expression Apply, Rename and Close reuse atomic
helpers. Native widget tests cover commit boundaries, error correction, angle edits
and rename collision recovery; no application command has been registered.
Grouped Qt/model validation: 59 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-editor-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild or release update.
Physical UI/accessibility, external-document lifecycle, creation/deletion, where-used
and production integration remain pending. TestParameterEditor joins the three
architecture suites for future changes to this dialog/helpers.

Previous roadmap batch: 10.8i/j atomic parameter-expression edit prototype.
edit_parameter_expression validates units, owns a transaction, checks affected
native recompute state and rolls back failed geometry. Stale affected consumers and
caller-owned transactions reject before mutation; a disconnected invalid box does
not block a valid edit. Undo/Redo and native persistence pass.
Grouped architecture validation: 56 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-edit-20260930-batch.
Macro PASS; process ended. Engine 2df76790b4; no native rebuild, installed editor
or release update. Object-level dependency scope is conservative through containers;
production UI, property-level impact analysis and external/proxy effects remain open.

Previous roadmap batch: 10.8g/h atomic parameter rename and label-reference checks.
Test-only rename_parameter owns its transaction; native naming errors restore owned
formulas/consumers. Unrelated pending edits reject before mutation. Label-based and
internal-name references survive rename, Undo/Redo, label edit and save/reopen.
Grouped architecture validation: 54 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-rename-safety-20260930-batch.
Macro PASS; process ended. Existing fork engine 2df76790b4; no native rebuild,
installed UI or release update. Production editor, external reference handling,
where-used and failed recompute policy remain pending under 10.8.

Previous roadmap batch: 10.8e/f named angular parameters and native property rename.
Test-only angle assignment rejects incompatible or missing expressions before mutation;
native rename updates two consumers through Undo/Redo and save/reopen.
Grouped architecture validation: 52 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-angle-rename-20260930-verified.
Macro PASS; process ended. Existing fork engine 2df76790b4; no native rebuild,
installed UI changes or release update. Parameter editor, where-used, collision and
cross-document rename policies remain pending under 10.8.

Previous roadmap batch: 4.1.10/5.1.10 secondary task cleanup errors handled.
Independent cleanup continues and preserves the primary constructor/display error;
repeated annotation removal is harmless. Both feature retry checks pass.
Grouped model/GUI validation: 54 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-cleanup-errors-20260930-batch.
Macro PASS; process ended. Shared FeatureTask and both GUI test modules staged with
matching hashes. No native rebuild, release update or physical viewport acceptance.
Native cleanup/transaction failure coverage remains bounded to the tested faults.

Previous roadmap batch: 4.1.9/5.1.9 production transaction ownership guards complete.
Existing-feature editing rejects unrelated pending transactions; scoped command
creation still hands its own transaction to the task. Caller edit/abort/retry passes.
Grouped model/GUI validation: 52 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-ownership-20260930-batch.
Macro PASS; process ended. FeatureTask and two test modules staged with matching
hashes. No native rebuild, release update or physical viewport acceptance.

Previous roadmap batch: 4.1.8/5.1.8 production task cleanup complete for tested faults.
Initial-preview construction failure and dialog-display failure clean resources,
restore visibility and roll back owned edit transactions; reopen/accept succeeds.
Grouped model/GUI validation: 50 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-cleanup-20260930-verified.
Macro PASS; process ended. Three Python modules and two tests staged with matching
hashes. No native rebuild or release. Arbitrary allocation/cleanup faults and
physical viewport/high-DPI acceptance remain separate gates.

Previous roadmap batch: 4.1.7/5.1.7 production command startup rollback complete.
Shared creation transaction guard aborts factory failure/editor refusal; successful
startup leaves the transaction to the task. Retry passes for both commands.
Grouped model/GUI validation: 48 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-startup-20260930-batch.
Macro PASS; process ended. Three Python modules and two tests staged with matching
hashes; final formatting-only differences verified. No native rebuild or release.
Partial task construction/observer cleanup remains a separate failure-handling gap.

Previous roadmap batch: 4.1.6/5.1.6 production preselection filtering complete.
Stale Trim target/tool and Isocline face candidates are skipped; valid selections
remain and repaired inputs can be picked in the open task and accepted.
Grouped model/GUI validation: 46 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-preselection-20260930-batch.
Macro PASS; process ended. Two Python modules and two tests staged with matching
hashes. No native rebuild, release update or physical viewport acceptance.

Previous roadmap batch: 4.1.5/5.1.5 production input-selection guards complete.
Trim Target/Tool and Isocline Faces/Reference reject stale picks before changing
inputs, retaining selection mode. Repair/recompute allows selection and acceptance.
Grouped model/GUI validation: 44 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-selection-20260930-batch.
Macro PASS; process ended. Two Python modules and two test suites staged with
matching hashes. No native rebuild, release or physical viewport acceptance.

Previous roadmap batch: 4.1.4/5.1.4 production task-readiness guards complete.
Trim Body/Isocline preview and acceptance reject invalid/touched dependency results
after recompute, hide the result and remain editable; source repair recovers.
Grouped model/GUI validation: 42 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\task-readiness-20260930-batch.
Macro PASS; process ended. Three production Python modules plus two tests staged
with matching source hashes in the isolated build. No native rebuild or release.
This integrates readiness into these task panes only; exporters and other consumers
remain separate gates, as do physical viewport/high-DPI acceptance checks.

Previous roadmap batch: 11.7w/x complete as test-only current-result access checks.
Native downstream solid remains cached after reference failure, but the new accessor
rejects invalid/touched dependencies. Repair/restore recover access; recompute is
explicit and returned shapes are independent copies.
Grouped validation: 50 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reference-consumers-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Application exporters/GUI/other consumers do not yet use this test-only accessor.

Previous roadmap batch: 11.7u/v complete as test-only planar reference repair checks.
Missing face clears adapter output and rejects preview; face repair Undo/Redo and
restore pass. Deleted-source replacement needs explicit sketch face reselection;
obsolete placement dependencies clear and later source motion follows correctly.
Grouped validation: 48 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reference-repair-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production repair UI, ambiguous topology and downstream cached-result/export safety
remain pending. Adapter fixtures need the prototype module to recompute.

Previous roadmap batch: 11.7s/t complete as test-only atomic reference creation.
One transaction creates the local reference and reattaches; Undo removes it and
restores the original attachment, with Redo/restore passing. Injected late failure
rolls back objects, placement and transaction state; subsequent success passes.
Grouped validation: 46 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-atomic-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production UI/task transaction integration and source/consumer failure handling
remain pending. Adapter fixtures require the test-only Python module on restore.

Previous roadmap batch: 11.7q/r complete as test-only cross-part planar reference.
Native binder probes failed alignment/motion criteria; explicit PlanarSupport uses
existing ShapeReferences conversion/dependency helpers and passes alignment, both
preview policies, source motion, Undo/Redo and restore. Grouped validation: 44 passes,
zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-adapter-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Saved fixtures require SketchReattachment.py for proxy recompute. Production adapter
creation/deployment and missing-source consumer handling remain pending.

Previous roadmap batch: 11.7o/p complete as test-only support scope guards.
Cross-container placement probe found preview/native mismatch; different geometry
containers now reject before mutation. App::Link supports also reject pending an
explicit occurrence-edit policy. Grouped validation: 42 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-scope-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Cross-part reference adapters, occurrence policy and production UI remain pending.

Previous roadmap batch: 11.7m/n complete as test-only reversal/expression checks.
MapReversed preview/commit/restore passes. Preserve-world rejects expression-driven
offsets before mutation; preserve-local retains the named length expression through
restore and parameter edits. Grouped validation: 40 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-expressions-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production UI, support-dependent expressions and external projections remain open.

Previous roadmap batch: 11.7k/l complete as test-only isolated placement preview.
Disposable-document attachment evaluation replaces live rollback. Both policies
retain candidate/commit parity, leave original object/recompute notifications empty,
clean up the temporary document and preserve an already-populated redo stack.
Grouped validation: 38 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-isolation-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Application observers can see temporary-document lifecycle; full sketch/consumer
evaluation and production graphical preview remain pending. See roadmap 11.7.

Previous roadmap batch: 11.7i/j complete as test-only rollback preview probes.
Both policies return placements matching committed operations and restore support,
offset and downstream position. Repeated/rejected previews preserve an existing
committed edit's Undo/Redo. Grouped validation: 36 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-preview-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Trial recompute is observable; production preview isolation/UI and preservation of
pre-existing redo history remain pending. See roadmap 11.7 and ADR 001.

Previous roadmap batch: 11.7g/h complete as test-only support validation.
Derived native extrusion support rejects before introducing a cycle; touched and
failed supports reject before mutation. Repaired support accepts reattachment and
Undo restores the original support/placement.
Grouped validation: 34 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-support-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production UI and broader topology/consumer failure handling remain pending.

Previous roadmap batch: 11.7e/f complete as test-only recovery/transaction prototypes.
Explicit preserve-local repair of a missing face survives Undo/Redo and restore;
preserve-world rejects invalid placement. Caller-owned transactions reject before
mutation and retain their pending edits/abort behavior.
Grouped validation: 32 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-recovery-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production repair UI, ambiguous/deleted support recovery, transaction integration
and consumer stale-result policy remain pending; see roadmap 11.7 and ADR 001.

Previous roadmap batch: 11.7c/d complete as test-only placement-policy prototypes.
Preserve-local retains the full attachment offset across rotated supports;
preserve-world solves a compensating offset with unchanged sketch parent. Rotated
parent, Undo/Redo, restore and subsequent associative support motion pass.
Grouped validation: 30 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\reattachment-policies-20260930-batch.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production editor/preview, selected-occurrence placement, lost-support repair and
transaction integration remain pending. See roadmap 11.7 and ADR 001.

Previous roadmap batch: 11.7a/b complete as bounded test-only reattachment prototypes.
Two parallel planar supports preserve sketch offset and downstream result identity
through Undo/Redo and save/reopen. Missing/curved faces reject before mutation.
Grouped validation: 28 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\sketch-reattachment-20260930-verified.
Macro PASS; process ended. No installed module, native rebuild or release update.
Production editor, preserve-world policy, rotated reattachment and lost-support
repair remain pending; see roadmap 11.7 and ADR 001 for the prototype boundary.

Previous roadmap batch: 10.8c/d complete as bounded foundation proofs. Explicit native
parameter references remain independent across parts with matching labels; native
object-level reverse dependencies survive save/reopen. A unit-correct zero length
invalidates geometry; abort restores the valid model and later edits Undo/Redo.
Grouped architecture validation: 26 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\parameter-dependencies-20260930-batch.
Macro PASS; process ended. Test-only changes; no native rebuild or release update.
Property-level where-used, production scope resolution and parameter editor remain
pending. These checks do not implement automatic invalid-edit rollback in the UI.

Previous roadmap batch: 10.8a/b complete as bounded foundation proofs. Native named
length parameters drive two features with inch/mm conversion, label edits,
Undo/Redo and save/reopen; occurrence placement remains independent. Native angle-
to-length coercion exposed by the initial test requires a production boundary.
Test-only NamedParameters.py enforces length-valued expressions; native cycle
rejection and abort recovery pass. Final grouped architecture run: 24 passes,
zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\named-parameters-20260930-verified.
No application module installed, native rebuild or release update. Parameter editor,
property renaming, scope/publication and full T13 remain pending. Process ended.

Previous roadmap batch: 16.2ao/ap complete. Z Correction preserves parsed probe
precision and rejects conflicting heights at identical XY positions; identical
samples are deduplicated. Native precision, order-independent rejection/export
blocking and recovery pass. Grouped validation: 65 passes, zero failures/errors/
skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-probe-precision-20260930-batch.
Source/module hash and precision limits recorded in roadmap. Python-only update;
no native rebuild, GUI/machine acceptance or release. Test process ended.

Previous roadmap batch: 16.2am/an complete. Shared property inheritance rejects
cycles without recursion; job operation traversal is iterative, ordered and unique.
Native shared-base invalidation/recovery and deep/cyclic fixtures pass. Grouped
validation: 151 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-traversal-20260930-batch.
Source/module hashes and cycle policy recorded in roadmap. Python-only
synchronization; no native rebuild, schema migration, GUI/machine acceptance or
release update. Test process ended; broader consumer gates remain open.

Previous roadmap batch: 16.2ak/al complete. Shared dressup lookup recognizes current
proxies independently of internal names, keeps guarded legacy fallback, stops at
ordinary operations and handles deep/cyclic/disconnected chains. Native custom-name
nested and restored fixtures pass. Grouped validation: 84 passes, zero failures/
errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-dressup-lookup-20260930-batch.
Hash and compatibility limits recorded in roadmap. Python-only synchronization;
no native rebuild, schema migration, GUI/machine acceptance or release update.
Test process ended. Broader consumer gates remain open.

Previous roadmap batch: 16.2ai/aj complete. Plunge Milling clears cached output
before generation and marks invalid stepover as a native error. Final grouped run:
54 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-plunge-20260930-verified.
Initial fixture name correction and module hash recorded in roadmap. Next bounded
candidate: 16.2ak, audit shared dressup base lookup's internal-name dependence with
legacy/nested/ordinary-operation tests before changing recognition. Python-only
synchronization; no native rebuild, GUI/machine acceptance or release update.
Test process ended; broader consumer gates remain open.

Previous roadmap batch: 16.2ag/ah complete. Dragknife and Ramp Entry clear output
before input validation/generation. Missing/empty Dragknife input and native
failure/export rejection/recovery pass. Final grouped validation: 52 passes,
zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-dragknife-ramp-20260930-verified.
Initial zero-feed fixture correction and source/module hashes recorded in roadmap.
Python-only synchronization; no native rebuild, GUI/machine acceptance or release
update. Test process ended. Broader consumer gates remain open.

Previous roadmap batch: 16.2ad/ae/af complete. Z Correction rejects non-finite probe
coordinates and non-positive/non-finite interpolation settings, and uses the correct
source-line subdivision point count. Grouped validation: 51 passes, zero failures/
errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-zcorrect-numeric-20260930-batch.
Source/development-module hash and spacing limitation recorded in roadmap.
Python-only synchronization; no native rebuild, GUI/machine acceptance or release
update. Test process ended. Continue related consumer gates with grouped validation.

Previous roadmap batch: 16.2aa/ab/ac complete. Z Correction clears stale results,
rejects unusable specified probe files and blocks uncorrected fallback outside the
probe area. Empty filename deliberately retains placed-base passthrough. Grouped
validation: 48 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-zcorrect-20260930-batch.
Native constant-offset grid, failure/export rejection and recovery pass. Hash and
external-file recompute limitation recorded in roadmap. Python-only synchronization;
no native rebuild, GUI/machine acceptance or release update. Test process ended.

Previous roadmap batch: 16.2x/y/z complete. Axis Map clears failed conversion output
and requires positive finite radius. Rotary-post snapshot tests now recompute and
validate inputs before restoring their prepared output; production export guard
unchanged. Final grouped validation: 44 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-axis-map-20260930-final.
Earlier fixture failures and final hashes are recorded in the roadmap. Python-only
synchronization; no native rebuild, GUI/machine acceptance or release update.
Test process ended. Continue broader consumer gates with grouped validation.

Previous roadmap batch: 16.2u/v/w complete. Mirror preserves placement when disabled,
clears stale output before generation, publishes only completed combined results,
and copies live base paths before transformation/append. The identity-placement
source mutation found in the initial run is fixed. Final grouped validation:
53 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-mirror-20260930-verified.
Source/development-module hash recorded in roadmap. Python-only synchronization;
no native rebuild, GUI/machine acceptance or release update. Test process ended.
Continue broader consumer compatibility gates with grouped validation.

Previous roadmap batch: 16.2s/t complete. Array clears paths before input validation/
generation; Dogbone clears paths and corner caches before generation. Grouped
validation: 49 passes, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-array-dogbone-20260930-verified.
Initial empty-source fixture exposed skipped downstream native execution; corrected
coverage verifies export rejection before explicit empty-input cleanup. Eager cache
invalidation of skipped consumers remains open. Python-only synchronization, no
native rebuild or GUI/machine/release acceptance. Validation process ended.

Previous roadmap batch: 16.2q/r complete. Missing/non-geometric Boundary stock
now causes native error/export rejection; offset outputs are checked before clipping.
Grouped run: 46 passes, zero failures/errors/skips, in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-boundary-inputs-20260930-batch.
Python synchronized to the existing development build, hash recorded in roadmap.
Test process ended. No native rebuild, GUI/machine acceptance or release update.
Continue broader consumer compatibility tasks in coherent groups.

Previous roadmap batch: 16.2o/p complete. Boundary clears cached output before
clipping/offset work, rejects empty boundary geometry in both modes, and returns
an empty native Path for missing base input. Four new failure/recovery checks and
related suites pass: 44 tests, zero failures/errors/skips in
D:\Temp\Office-PC\freecad-plus-validation-20260928\cam-boundary-20260930-batch.
Python synchronized to the existing development build; source/installed hash is
recorded in the roadmap. No native rebuild, GUI/machine acceptance or release.
Validation process ended. Continue broader consumer gates in coherent groups.

Previous roadmap batch: 16.2l/m/n complete. Empty Lead-in/Lead-out and Boundary inputs
now stop cleanly; lead generation clears stale paths before possible exceptions;
disabled leads return the placed base path directly. cam-leads-20260929-verified
records 40 passes, two existing linking skips, zero failures/errors. Missing-model
nested fixture now stays empty without invalid dressup objects and recovers.
Python-only synchronization, no native rebuild or GUI/machine acceptance. Broader
consumer/dressup failure gates remain open; continue related grouped validation.

Previous roadmap batch: 16.2j/k complete. Job.Model changes now rebind/clear nested
base operations and dressup paths using allOperations. Native fixture removal and
replacement/recovery checks pass, including restored export. cam-nested-20260929-batch
records 90 passes, one existing skip, zero test failures/errors. Python-only install.
Missing-model recompute reports Lead-in/Lead-out NoneType.Group diagnostics while
keeping paths empty; recovery passes. That diagnostic and broader consumer gates
remain open. No native build or GUI/machine acceptance in this batch.

Previous roadmap batch: 16.2h/i complete. Shared PostList refuses dirty/invalid native
operations and linked inputs before cached-path export. Dirty and failed-producer
recovery checks pass; nested dressup export tests now recompute edited inputs first.
cam-export-20260929-verified under the existing validation root records 88 passes,
one pre-existing skip, zero failures/errors (overall macro flag false for any skip).
PostList.py source/installed SHA256:
0C70E6249CF1AEF5BD346CE89B2CB507F750E7F97BD2A07EE702A258B7B2E078.
No native build; GUI/machine acceptance and broader semantic/export gates remain open.

Previous roadmap batch: 16.2f/g complete. Job.Model replacement/removal rebinds
operation dependencies and clears unfrozen paths; normal recompute recovers them.
Restored the full execute wait-cursor decorator displaced by the previous change.
75 distinct checks pass across cam-container-20260929-batch (67 broader passing)
and cam-container-20260929-corrected (eight targeted passing after fixture repair).
Both evidence folders are under D:\Temp\Office-PC\freecad-plus-validation-20260928.
Only Python modules synchronized; no native rebuild or GUI/machine acceptance.
Next: failed-producer, nested-operation and export gates; retain grouped validation.

Previous roadmap batch: 16.2d/e complete. Production CAM Base.py binds hidden native
ModelDependencies links on execution and restore; normal document recompute now
propagates source edits and empty-source recovery in the SurfaceScan fixture.
72 grouped checks pass in cam-dependencies-20260929-final. Installed/source SHA256:
8F38E250CD73C0B1BF8754BF64CA4879BF509D35C40620520212F780A8ECCC4C.
No native build or test process remains. Current Operations container is a plain
group, not an aggregate Path cache. Export guards, skipped failed producers, replaced
Model containers and broader reference/consumer graphs remain open. Next: targeted
remaining downstream gates; batch related changes before any expensive build.

Earlier roadmap batch: 16.2b/c complete. Production CAM Path/Op/Base.py clears
old Path before validation can return for missing model or tool controller, after
the existing frozen-job guard. Both defects retained 43 commands before correction;
69 grouped checks pass in cam-invalid-inputs-20260929-verified. Installed Python
module matches source SHA256 FE5A146430588CD2B3E5660B2CD9B16B67E6A57EEB12AFD3F5DA079B9BB3227D.
No native build or test process remains. Automatic dependency scheduling, aggregate
job/export invalidation and general failed-source behavior remain open. Continue
related downstream consumer work; do not equate these execution tests with those gates.

Earlier roadmap batch: 12.1a/12.2a complete. Mixed native definitions and a bounded
Make Unique helper pass in a 32-check grouped run, mixed-unique-20260929-final under
the existing external validation root. Native recursive copy remaps sketch links;
new metadata identities/provenance, selected-link reassignment and placement are
transactional. Undo/Redo, shared versus independent edits, restore and no-mutation
rejection pass. No installed module/native build and no test process remains.
Next: missing/ambiguous drawing references, CAM path/FEM consumers, complex/external
identity and production architecture. Keep the full 12.1/12.2 gates open.

Earlier roadmap batch: 7.1.3g/h complete; 29 grouped checks pass in
lineage-20260929-topology under the existing external validation root. New test-only
ResultLineage.py implements planar side roles and explicit-primary/new-ID merges.
Expected producer errors initially left stale downstream geometry; status/empty-output
propagation fixes the bounded prototype chain. No installed module or native build.
No test process remains. General lineage, native error/UI integration and broader
consumer safety remain open. Next: mixed definitions, reference repair, CAM paths/FEM
and production architecture decisions. Roadmap and ADR 001 retain evidence/limits.

Earlier roadmap batch: 7.1.3f and 16.2a complete; 24 grouped checks pass in
attachment-drawing-20260929-final under the existing external validation root.
Independent FlatFace attachment on a rotated plane propagates support movement;
TechDraw projected radius follows source edits, Undo/Redo and save/reopen.
Only tests and documentation changed; no installed source or native rebuild.
The initial drawing fixture needed TechDraw Edge0, not Edge1. No test process
remains. Next: semantic split/merge lineage, missing/ambiguous drawing references,
CAM generated-path and FEM consumers. Keep parent architecture/consumer gates open.
Evidence, fixture limits and module hashes are linked from the roadmap and ADR 001.

Earlier roadmap batch: 10.1 and 10.3a/b complete. Product/UI/guideline contracts
now match version 2; ADR 002 defines transient suggestions versus saved intent.
Test-only OperationIntent.py supports bounded single-part solid proposals and
committed operations with explicit native links. All 22 grouped checks pass in
operation-intent-20260929-final under the existing external validation root.
No application module installed, native build or GUI acceptance. No test process
remains. Next: Phase 7 lineage/consumers, production target discovery/access scope,
scale-aware contact behavior and real task preview lifecycle. Keep 10.3 open.
See roadmap/ADR 002 for evidence and limits; batch related work before builds.

Earlier roadmap batch (2026-09-29): 7.1.3c/7.1.3d/7.1.3e complete. Test-only
history adapters now handle tilted profiles and cross-part placement dependencies;
a native assembly-local cut preserves the shared definition and other occurrence.
Production Draft clones clear stale Shape when all sources become empty or the
source list is cleared. Native CAM job-model clones clear/restore geometry too;
generated-path invalidation is not established. All 88 grouped history, Draft
modification, PlanarSurface and STL/tab tests pass without failures/errors/skips
in `part-consumers-20260929-final/results.json` under the existing external build
root. Fifteen focused checks also passed after reproducing three defects.
Python clone module installed in the existing fork; no native build. Matching
source/installed SHA256: 6291E8A30ED3C4321833182412A6D8AC86C642CFF035A605F9FFD29327DF19A9.
The evidence manifest records adapter/module/test hashes. No test process remains.
Next: semantic lineage, actual attachments and remaining TechDraw/CAM-path/FEM
consumer gates. FEM is disabled in this build; batch future native build work.
History production architecture and cadprt schema remain undecided/unimplemented.

Earlier roadmap batch (2026-09-29): 7.1.3a/7.1.3b adapter prototypes and 7.1.6a
decision boundary complete. Eight native capability/adapter tests pass together
in `part-adapters-20260929-final`. Implementation is test-only under
tests/prototypes; no application code, installation or native build changed.
Probes cover Body binders sharing a sketch and explicit result roles/identities,
placement, dependencies, unavailable/reappearing results, transactions and restore.
See architecture/ADR_001_HISTORY_ADAPTER_BOUNDARY.md for limits. Next: transformed
attachments/occurrences, assembly-local edits and downstream consumers before
final architecture choice. Prototype FCStd files require the test module for
result-layer recompute; they are not cadprt files or released functionality.
No test process remains running; continue batching related tasks before builds.

Current roadmap batch (2026-09-29): logical contracts/mapping for 7.1.1, 7.1.2
and 7.1.4 are complete in architecture/PART_HISTORY_CONTRACT.md. Four grouped
native probes pass in `part-history-20260929-final`, covering independent/shared
sketches, multiple results, links, transactions and FCStd persistence. No production
application code changed and no build was needed. The saved native example is
disposable evidence, not the future cadprt format or a new history implementation.
Next: actual adapter comparison 7.1.3 and architecture decisions 7.1.5/7.1.6.
The owner requests groups of two or three tasks before costly build/test work.
No test process remains running. Earlier CAM evidence below remains valid.

Latest implementation (2026-09-29): U.23 corrects the reproduced modern #26300
freeform cutting-boundary stall. B-spline/Bezier selections now use tolerance-based
tessellation and NonZero polygon union; failure cannot drop selected faces.
All 91 CAM checks pass in `freeform-boundary-20260929-final`, including the
original fixture: 14.05 seconds generation versus the baseline 120-second timeout,
4,475 commands and 4,118 cutting endpoints inside the mask. Python-only update
installed, no rebuild. Module hash and limits are recorded in U.23.
U.15 native cancellation and U.14 exact GeomFillSurface acceptance remain pending;
legacy Surface and machine/post acceptance are not claimed. No test process remains.

Latest implementation (2026-09-29): U.22 rejects the modern CAM avoidance
fallback that silently filled selected holes when projection failed. The error
clears the stale operation path. Successful primary projection and outer-only
cutting fallback remain covered. All 81 CAM checks pass in one batch at
`avoidance-fallback-20260929-final`; Python-only update synchronized, no build.
Final module hash is in U.22. Avoidance inputs requiring this lossy fallback now
stop explicitly; a replacement projection algorithm remains future work.
#26300 and exact GeomFillSurface acceptance remain open. No test process remains.

Latest implementation (2026-09-29): U.16/U.21 fix #6864 in the replacement
Line/ZigZag generator. One targeted source compile/module relink completed; all
77 CAM checks pass in one batch, including final-strip geometry, avoidance and
STL/tab workflows. No full application build. Module/test hashes and evidence
are in U.21. The existing test application now contains this correction.
Next unresolved high-impact case remains U.15 (#26300); exact GeomFillSurface U.14
needs a relevant build with Surface enabled. No process remains running.

Earlier implementation (2026-09-29): U.20 fixes partial boundary loss in the modern
CAM pipeline. Failed isolated/group projections and boundary unions now stop
instead of dropping selected cutting/avoidance regions; stale paths are cleared.
Fourteen focused and 59 related checks pass across separate runs. Python-only
update is installed and hash-verified; no native rebuild or process remains active.
Evidence and installed module hash are recorded in U.20. The confirmed freeform
slowdown below remains open; no unsuccessful projection experiment was restored.

Earlier diagnosis (2026-09-29): U.19 reproduces #26300 in PlanarSurface.
The original saved freeform geometry with nine selected faces exceeds 120 seconds;
20/40-second stacks locate Path.Area boundary projection, before cutting generation.
Per-face/paired-face projection experiments were unsuccessful and fully removed.
Source-built app is restored to committed code (line endings normalized; module
hash is recorded in U.19). No native rebuild or application fix is claimed.
The opt-in TestIssue26300Fixture.py and bounded RunIssue26300.ps1 preserve the case.
Next: resolve U.15 with validated projection/coverage semantics; U.16 final-strip
coverage remains independent pending work. Exact GeomFillSurface testing U.14
still awaits a relevant batched build with Surface enabled. Prior ten-test curved
avoidance evidence remains valid. No test/build process remains running.

Latest CAM issue milestone (2026-09-29): two Python modules updated in the existing
app to stop generation when selected face-avoidance boundaries fail and to reject
strategy switches that would ignore those exclusions. Eight focused checks and
59 related CAM regressions pass (67 total, no skips). No native rebuild. See
U.12-U.17 in the roadmap for evidence and the remaining #27751 child cases:
curved external avoidance, freeform hang/crash, and final-strip line coverage.
Legacy Surface/Waterline and saved MillFace paths were not migrated. No test or
build process remains running.
CAM avoidance milestone `b2cfdf0f114ff2cba48004fe538991395b22f525` is committed
and pushed to `origin/main`; remote hash verified. No release was made.

Issue batch completed (2026-09-29): the local application now contains the Mirror
#32706 correction. A targeted compile of FeatureMirroring.cpp and Part relink
both exited 0; no full rebuild was needed. All 75 issue tests pass, including
Mirror save/reopen/recompute and translated/rotated face selection through the
real task pane. Three changed test scripts were synchronized and hash-verified.
See [issue work](DEVELOPMENT_ROADMAP.md#upstream-issue-work) for binary hashes and
exact evidence directories, and [procedures](../tests/UpstreamIssues.md) to rerun.
No build/test process remains running. The executable is the existing external
`build/bin/FreeCAD.exe`; its Part module has changed, not its historical version string.
Validation checkpoint `bb6d7607a78080bec36f8ade30c8925f09201874` is committed and
pushed to `origin/main`; remote hash verified.

The earlier five startup-recovery fixtures also passed; recovery, numeric input,
Extrude and tree fixes were inherited and not duplicated. #29376 still needs a
reproducible affected session/GPU trace. Legacy MillFace is superseded for new
workflow tasks, while saved legacy operations retain the documented risk.
The broader upstream CAM refactor epic is not declared complete. No release.

Earlier source checkpoints: Mirror/triage `85fd6ebc77`, then regression milestone
`24815217c9`, both pushed to origin/main. Their earlier notes about an unbuilt
Mirror correction are superseded by this completed build checkpoint.

CAM implementation and automated validation are complete. Direct STL
Parallel/Waterline, stock bridges and separate manually indexed setups are in the
source-built application. No build or automated test is still running.
Source milestone `648cff214ca78e1d8b3d72d87d6053e103390c60` is committed and
pushed to `origin/main`; the remote branch hash was verified. No release was made.

Indexed setups use one associative transform for model, stock and shared tabs;
each setup has its own work origin and separately generated/posted three-axis
paths. No automatic rotary motion is generated. Native viewport acceptance,
representative simulation and per-setup postprocessor review remain open.
The NX-style roadmap planning request is committed and pushed as Phases 7-9
(`4c9d7ed598`); no history architecture implementation has been started.
The concise upstream issue watchlist is in `FREECAD_ISSUES.md`, committed and
pushed initially as `bbcf78cffb`; the later issue pass now records applicability
and the reproduced Mirror defect, separately from inherited fixes.

Current CAM evidence under the external root below:

- `cam-completion-build-result.json`: full configured build exited 0;
  `cam-final-scripts.log`: final script/test targets also exited 0.
- `cam-tests-20260929-184049`: all 22 focused tests passed, no skips, process 0.
- `cam-tests-20260929-183855`: related suites had 112 passes, no failures/errors,
  one optional simplification test skipped for unavailable `fast_simplification`.
  Strict aggregate FAIL records that skip; do not report all tests as passing.
- `cam-validation-manifest.json`: 15 installed CAM Python files match source,
  with five native binary hashes. Runtime retains the historical native version
  stamp `8abce719de`; use file hashes and Git history to identify new CAM code.
- The [Phase 6 roadmap](DEVELOPMENT_ROADMAP.md#cam-mesh-machining) separates
  completed automated work from the remaining manual gates.

The previous shutdown handoff below records completed Part/Part Design evidence.
It predates the CAM changes. Do not mark CAM tests or native acceptance complete
based on the earlier 149-test result.

## Earlier Part/Part Design validation

- Native feature source: `8abce719de38a1b1ad255d0e7f4554a9d44e9c71`.
- Configured Windows x64 Release ALL_BUILD succeeded. First bounded pass timed out;
  resumed incremental build finished with exit 0. No application source fix needed.
- All 149 model/task tests passed at both scale factors 1 and 1.5, with no failures,
  errors or skips and both processes exiting 0. Actual device-pixel ratios: 1.5 and
  2.25, respectively. These are automated checks, not physical/visual acceptance.
- Nine binary hashes recorded; all 80 checked installed workflow/test Python files
  match the checkout. Added `tests/ValidateWorkflows.FCMacro` for repeatable testing.
- Roadmap milestone 2.2.4 is complete. Remaining manual gates are listed under
  [consolidated validation](DEVELOPMENT_ROADMAP.md#consolidated-validation).

## Earlier build and evidence

External root: `D:\Temp\Office-PC\freecad-plus-validation-20260928`.
Launch: `build\bin\FreeCAD.exe` beneath that root. It reports FreeCAD 26.3.0dev,
revision 49009 and source hash `8abce719de`. This is the focused development build;
disabled unrelated workbenches, installer packaging and upstream compatibility
testing are not included. Ignore the separately installed FreeCAD.

Evidence: `closeout-build-resume-results.json`, `closeout-build-manifest.json`,
`closeout-regressions/results.json`, `closeout-highdpi/results.json`, and their logs.
The two latter folders have isolated settings and successful process reports.

## Next CAM acceptance work

Follow `tests/CAMMeshMachining.md` for physical STL selection/placement, both
strategies, tab picking/editing, and indexed-frame interaction. Review material
removal and each setup's posted output. Keep the optional simplification skip
visible until its dependency is available and that inherited test can run.
No CNC machine motion or physical cutting has been performed.

## Earlier Part/Part Design acceptance handoff

1. Launch the development application for visible native testing with isolated
   preferences. Avoid `--hidden` for the interactive fixture: its startup/close
   behavior led to an Unsaved Document prompt rather than a ready test workspace.
2. Use the existing `tests/PadTaskPanel.md`, `PatternTaskPanel.md`,
   `RevolveTaskPanel.md`, `TrimBody.md`, and `IsoclineCurve.md` acceptance procedures.
   Start with 2.2.3: real viewport/tree picking on rotated profiles, keyboard input,
   direction/preview behavior, Cancel, visibility and Undo/Redo, including Pocket.
3. Record only checks actually completed. Close 2.2 and related feature gates only
   when their required interaction/visual evidence exists.

Native tool state: computer-use skill was initialized through `@oai/sky` in the
node REPL. User granted window testing, but graphics capture timed out. Accessibility
inspection found the fixture's save prompt. The user then pressed physical Escape,
stopping Computer Use, and subsequently requested shutdown. No further native input
was issued. Do not reuse old window handles, element indexes or screenshot state.
No native acceptance check was completed or marked passed.

Only task-created test documents were opened. Fixture files `Closeout-*.FCStd` and
`closeout-interactive.FCMacro` are in the external evidence root. No user design was
edited. Changes are local; no push, release or publication was made.
