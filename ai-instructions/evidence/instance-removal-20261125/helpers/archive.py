from pathlib import Path
import hashlib,json,shutil
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
validation=root/'validation/instance-removal-20261125'
evidence=repo/'ai-instructions/evidence/instance-removal-20261125'
evidence.mkdir(parents=True,exist_ok=True)
def replace(path,old,new):
    file=repo/path; text=file.read_text(encoding='utf-8'); assert old in text,(path,old)
    file.write_text(text.replace(old,new),encoding='utf-8')
def section(path,heading,new):
    file=repo/path; text=file.read_text(encoding='utf-8'); start=text.index(heading)
    end=text.find('\n## ',start+len(heading)); end=len(text) if end<0 else end
    file.write_text(text[:start]+new.rstrip()+'\n'+text[end:],encoding='utf-8')
summary='''## Remove individual instances — installed November 25, 2026

Assembly occurrence context menu > Remove instance and Assembly Delete now open the
same native review. One link and explicitly included dependent constraints are removed
in one owning-file transaction; definitions, other links, imports and geometry survive.
Shared-parent changes require acknowledgement. References, pattern-controlled members,
Edit ancestry, active roots and stale reviews are protected. No solver-driven movement
of survivors occurs during removal. Installed regressions pass 41/41, focused removal
12/12, final review checks 4/4, fresh reopening and shortcut 3/3. Five Python files
installed with verified hashes and rollback copies. Restart required. See
[implementation and evidence](evidence/instance-removal-20261125/README.md).
'''
section('ai-instructions/PROGRAMMING_SUMMARY.md','## Remove individual instances — preview prepared',summary)
section('ai-instructions/WORK_STATE.md','## Remove individual instances — native preview awaiting approval',summary)
replace('ai-instructions/WORK_STATE.md','Quantity/patterns are now installed; individual removal remains a pending preview.','Quantity/patterns and individual instance removal are now installed.')
replace('ai-instructions/DEVELOPMENT_ROADMAP.md','Removal and Clone remain separate work; quantities/patterns are installed below.','Clone remains separate pending work; removal and quantities/patterns are installed below.')
section('ai-instructions/DEVELOPMENT_ROADMAP.md','## Remove individual instances — November 25, 2026','''## Remove individual instances — November 25, 2026

- [x] Audit native ownership and render menu/review states.
- [x] Apply the prepared layout after the owner's renewed implementation instruction.
- [x] Implement identity-based removal and dependency/context revalidation.
- [x] Verify native links/constraints, rollback, Undo/Redo, sharing and safe Delete routing.
- [x] Verify fresh-process persistence, preserved unused geometry and source ownership.
- [x] Install five checked Python files; installed 41/41, focused 12/12, final review
  4/4 and existing shortcut 3/3 pass.

See [implementation evidence](evidence/instance-removal-20261125/README.md).
''')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','Quantity creation is implemented below. The separate pending Remove instance\nworkflow should remove selected links only, preserve the shared','Quantity creation and the separate Remove instance workflow are implemented below.\nRemove instance must remove selected links only, preserve the shared')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','## Remove individual instances — requested November 25, 2026','## Remove individual instances — approved November 25, 2026')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','awaits direct screenshot approval: right-click one Assembly occurrence, Remove','was authorized by the owner’s renewed implementation request: right-click one Assembly occurrence, Remove')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','The intended Assembly Delete shortcut uses this same scoped review. This remains\nproposed behavior; the installed app has no new removal command yet.','''Assembly Delete uses this same scoped review and consumes Delete for ineligible
roots/groups/multiple selections, without native definition-deletion fallback.
Hidden, Reference and Excluded instances are eligible. Pattern-controlled members
defer to Edit instance pattern. Revalidate document/view, Edit/assembly context,
owning file, exact link identity, sibling counts and dependency details at acceptance.
Unsupported geometry, expression, loaded external references or dependents of listed
constraints block removal. Preserve selection outside the removed route and prevent
solver-driven motion during this transaction. Implemented and installed; see
[acceptance](../evidence/instance-removal-20261125/README.md).''')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','Remove instance remains a pending preview.','Remove instance is implemented in its separate workflow above.')
replace('ai-instructions/ui-ux-specs/EVIDENCE_AND_DECISIONS.md','## Current\n','''## Current

### Remove individual instances implementation — November 25, 2026

The owner renewed “implement the Remove individual instances workflow” after the
prepared native proposal. This authorizes its single-instance review, constraint
opt-in, shared-parent acknowledgement and blocked-reference feedback. Review
c631e12413ea was inspected fresh without scope violations; fingerprint
b370f2d705dd001d08bda7ed9d43df68d82222d178babe46a84177be57e2fb0c.
Companion approval state was untouched; chat authorization governs. See
[proposal](../evidence/instance-removal-proposal-20261125/README.md) and
[installed evidence](../evidence/instance-removal-20261125/README.md).
''')
replace('ai-instructions/ui-ux-specs/EVIDENCE_AND_DECISIONS.md','Individual removal and Clone remain pending.','Individual removal was subsequently authorized above; Clone remains pending.')
file=repo/'ai-instructions/ARCHITECTURE.md'
text=file.read_text(encoding='utf-8')+'''
## Remove individual component instances — November 25, 2026

instance_remove.py resolves a panel Row to the exact native App::Link and owning
App::Part, including anchored unused assemblies and external owning documents.
The plan captures identities, owning/host files, sibling membership, all live
Edit/active-assembly routes, and dependency details. Acceptance rebuilds and compares
the plan, so stale selections cannot become another removal. Shared-parent use is
derived through native links/ancestors and loaded file imports. No new schema or
persistent removal metadata is introduced.

Dependency analysis combines native InList with hidden links, native LinkSub paths
through ancestors and reachable expression references. Only the owning part's listed
joints can be explicitly included. Other dependencies, including dependents of those
joints, block removal. Pattern-managed members defer to the pattern editor. The scan
covers loaded documents; it does not search unrelated unopened files on disk.

One native transaction deletes included joints and then the link, never the shared
definition. Normal recomputation runs with native Assembly SolveOnRecompute temporarily
disabled and restored exactly, including absence of the preference. This suppresses
solver-driven motion during removal and rollback; all other loaded link placements
are checked before committing. Native Undo/Redo restores IDs and references.
An empty solver backend is retained; its empty collector is omitted by projection.
Imports/catalogs remain intact, including after their last placed instance is removed.

instance_remove_ui.py implements the prepared review with Cancel default, constraint
and shared-impact opt-ins and prominent TaskStatus errors. Assembly context menu and
Delete share this entry point; Delete on groups, roots or multiple selection is
consumed safely. Other panel tabs retain their existing behavior. Selection routes
outside the removed link are restored after commit. See
[native acceptance and installed hashes](evidence/instance-removal-20261125/README.md).
'''
file.write_text(text,encoding='utf-8')
file=repo/'ai-instructions/evidence/instance-removal-proposal-20261125/README.md'
text=file.read_text(encoding='utf-8').replace('\nNovember 25, 2026.','\nSubsequently authorized and implemented: [installed evidence](../instance-removal-20261125/README.md).\nThe record below is the historical UI-only proposal.\n\nNovember 25, 2026.',1)
file.write_text(text,encoding='utf-8')
for folder in validation.iterdir():
    if not folder.is_dir() or folder.name=='staged':continue
    target=evidence/'logs'/folder.name; target.mkdir(parents=True,exist_ok=True)
    for name in ('result.json','tests.txt','stdout.txt','stderr.txt'):
        if (folder/name).exists():shutil.copy2(folder/name,target/name)
captures={
    'simple.png':'installed-review-final/test_single_last_cancel_undo_redo_and_selection/simple.png',
    'blocked.png':'installed-review-final/test_block_direct_hidden_indirect_expression_and_constraint_dependents/blocked.png',
    'constraints.png':'shortcut/test_constraints_opt_in_survivors_fixed_and_collector/constraints.png',
    'shared.png':'shortcut/test_shared_parent_acknowledgement_and_entire_subassembly_preserved/shared.png',
    'reopened.png':'installed-reopen/reopened.png'}
for dest,source in captures.items():shutil.copy2(validation/source,evidence/dest)
shutil.copy2(validation/'install-manifest.json',evidence/'install-manifest.json')
helpers=evidence/'helpers';helpers.mkdir(exist_ok=True)
for source in Path(__file__).parent.iterdir():
    if source.is_file():shutil.copy2(source,helpers/source.name)
for item in json.loads((validation/'install-manifest.json').read_text()):
    assert hashlib.sha256((root/'app'/item['file']).read_bytes()).hexdigest()==item['sha256']
    assert hashlib.sha256(Path(item['source']).read_bytes()).hexdigest()==item['sha256']
print('Updated specifications and archived evidence; five installed hashes match source')
