from pathlib import Path
import hashlib, json, shutil
repo = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
root = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
validation = root/'validation/instance-quantity-20261125'
evidence = repo/'ai-instructions/evidence/instance-quantity-20261125'
evidence.mkdir(parents=True, exist_ok=True)
def replace(path, old, new):
    file = repo/path; text = file.read_text(encoding='utf-8')
    assert old in text, (path, old)
    file.write_text(text.replace(old,new), encoding='utf-8')
def section(path, heading, text):
    file=repo/path; source=file.read_text(encoding='utf-8'); start=source.index(heading)
    end=source.find('\n## ',start+len(heading)); end=len(source) if end<0 else end
    file.write_text(source[:start]+text.rstrip()+'\n'+source[end:],encoding='utf-8')
summary='''## Instance quantity and patterns — installed November 25, 2026

Add Component > Add existing/new > Next opens Quantity, Linear, Grid or Circular.
Counts apply per selected definition; Add new creates one definition. Patterns
remain editable through a member's Edit instance pattern menu. Shared native links,
parent-local placements, scene-only preview, atomic Undo and dependency guards are
implemented. Schema 7 persists parent-owned pattern metadata; schemas 1–6 remain
readable. Installed regressions pass 54/54; final shortcut checks 3/3 and fresh-process
reopen/reference/export checks pass. Thirteen Python files installed with verified
hashes and rollback copies. Restart required. See
[implementation and evidence](evidence/instance-quantity-20261125/README.md).
'''
section('ai-instructions/PROGRAMMING_SUMMARY.md','## Instance quantity and patterns — preview prepared',summary)
section('ai-instructions/WORK_STATE.md','## Instance quantity and patterns — native preview awaiting approval',summary)
replace('ai-instructions/WORK_STATE.md','Quantity/patterns and individual removal previews remain pending.','Quantity/patterns are now installed; individual removal remains a pending preview.')
section('ai-instructions/DEVELOPMENT_ROADMAP.md','## Instance quantity and patterns — November 25, 2026','''## Instance quantity and patterns — November 25, 2026

- [x] Audit existing behavior and render native navigator/create/edit controls.
- [x] Apply the prepared layout after the owner's renewed implementation instruction.
- [x] Implement quantities, parent-relative patterns, same-form editing and atomic Undo.
- [x] Verify cycle/reference guards, stable identities, constraint/Move protection,
  preview/Cancel, fresh-process persistence, linked ownership and editable export.
- [x] Install thirteen checked Python files; installed 54/54 and shortcut 3/3 pass.

See [implementation evidence](evidence/instance-quantity-20261125/README.md).
''')
replace('ai-instructions/DEVELOPMENT_ROADMAP.md','Quantity/patterns, removal and Clone remain separate work.','Removal and Clone remain separate work; quantities/patterns are installed below.')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','Separate pending quantity/removal workflows: Add existing should offer a\nquantity; Remove instance should remove selected links only, preserve the shared','Quantity creation is implemented below. The separate pending Remove instance\nworkflow should remove selected links only, preserve the shared')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','## Instance quantities and patterns — requested November 25, 2026','## Instance quantities and patterns — approved November 25, 2026')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','awaits direct screenshot approval. Add existing keeps its navigator, then opens','was authorized by the owner’s renewed implementation instruction. Add existing keeps its navigator, then opens')
replace('ai-instructions/ui-ux-specs/COMPONENT_PANEL.md','recursive nesting guards and the fixed active assembly are required. This is\nproposed behavior, not current implementation. Condensed/expanded display is now\nimplemented separately; Remove instance remains a pending preview. Name enforcement\nwas delivered separately and is not implemented by this proposal.','''recursive nesting guards and the fixed active assembly are required. Pattern members
cannot be moved or newly constrained independently; use Edit instance pattern.
Directions can use parent axes or native straight-edge/axis references; Linear also
accepts a typed vector. The operation supports at most 10,000 new links total.
Implemented and installed; see [acceptance](../evidence/instance-quantity-20261125/README.md).
Condensed/expanded display and name enforcement were delivered separately;
Remove instance remains a pending preview.''')
replace('ai-instructions/ui-ux-specs/TASK_PANEL.md','## Confirmed requirements\n','''## Confirmed requirements

### Create/edit component instances — November 25, 2026

Add existing/new keeps the component navigator and uses Next to open Create instances.
Quantity, Linear, Grid and Circular share one native form with per-definition counts,
parent-local coordinates, preview and prominent validation errors. Change parts
returns to the navigator preserving valid arrangement settings. New Component remains
separate. Right-click an individual pattern member to Edit instance pattern with the
same saved controls/references. Cancel leaves documents unchanged; OK commits one
operation. Preserve surviving identities and block referenced/edited-member removal.
Use native unit fields and reference collectors. Pattern members are controlled by
the pattern; independent Quantity links can be moved/constrained. See
[component contract](COMPONENT_PANEL.md#instance-quantities-and-patterns--approved-november-25-2026).
''')
replace('ai-instructions/ui-ux-specs/EVIDENCE_AND_DECISIONS.md','## Current\n','''## Current

### Instance quantities and patterns implementation — November 25, 2026

The owner renewed “implement an instance quantity workflow, allowing the user to
create several instances at once, including in patterns” after the native proposal.
This authorizes its navigator, Quantity/Linear/Grid/Circular and shared edit form.
Review ef9fa8610a64 was inspected fresh with no violations; fingerprint
9027c86fe3a312851df4dca056c5e4ce1f31059e249a268ff0bd56e209d50046.
Chat authorization governs; companion approval state was untouched. See
[proposal](../evidence/instance-quantity-proposal-20261125/README.md) and
[installed evidence](../evidence/instance-quantity-20261125/README.md).
''')
replace('ai-instructions/ui-ux-specs/EVIDENCE_AND_DECISIONS.md','Quantity/pattern creation, individual removal and Clone remain separately pending.','Quantity/pattern creation was authorized subsequently above. Individual removal and Clone remain pending.')
replace('ai-instructions/ARCHITECTURE.md','Schemas 1–5 remain readable. New files use schema 6. Existing files upgrade lazily in','Schemas 1–6 remain readable; new files now use schema 7 (instance patterns below).\nOlder files upgrade to at least schema 6 lazily in')
file=repo/'ai-instructions/ARCHITECTURE.md'; text=file.read_text(encoding='utf-8')
text += '''
## Component instance quantities and patterns — November 25, 2026

instance_patterns.py creates shared native App::Links in the edited destination
App::Part. Quantity creates only independent links. Linear/Grid/Circular additionally
create parent-owned App::FeaturePython metadata marked FreeCADPlus.InstancePattern.1,
with JSON Configuration, native Members/Seeds links and native LinkSubList References.
Schema 7 permits this metadata and omits it from geometry History. Existing files
upgrade in the first pattern transaction; Undo restores the old schema. Older Plus
versions reject schema 7 instead of dropping metadata. No geometry/history is copied.

The restored Pattern proxy computes parent-local placements on recompute, including
native direction-reference changes. No observer stores an alternate assembly graph.
Count edits retain each definition cohort's prefix links; new links use the same
definition. Removal checks direct dependencies, resolved indirect LinkSub paths and
live edited occurrences before mutation. Pattern-member Move and constraint inputs
are blocked so competing placement owners cannot silently overwrite one another.

instance_task.py owns the native form, identity/context checks, scene-only preview,
reference picking and cleanup. Creation/editing is one transaction in the destination
file. External-parent updates use native linked-document recomputation; its matching
host Undo entry is expected, while host objects/placements and active/Edit contexts
remain unchanged. Shared parent occurrences all see the same children. Native export
remaps metadata references and remains editable. See
[native acceptance and installed hashes](evidence/instance-quantity-20261125/README.md).
'''; file.write_text(text,encoding='utf-8')
file=repo/'ai-instructions/evidence/instance-quantity-proposal-20261125/README.md'
text=file.read_text(encoding='utf-8'); text=text.replace('\nNovember 25, 2026.', '\nSubsequently authorized and implemented: [installed evidence](../instance-quantity-20261125/README.md).\nThe record below describes the historical UI-only proposal.\n\nNovember 25, 2026.',1);file.write_text(text,encoding='utf-8')
for folder in validation.iterdir():
    if not folder.is_dir() or folder.name=='staged': continue
    target=evidence/'logs'/folder.name; target.mkdir(parents=True,exist_ok=True)
    for name in ('result.json','tests.txt','stderr.txt','stdout.txt'):
        if (folder/name).exists():shutil.copy2(folder/name,target/name)
for image in (validation/'shortcut/test_ui_all_arrangements_previews_and_errors_preserve_model').glob('*.png'):
    shutil.copy2(image,evidence/image.name)
shutil.copy2(validation/'install-manifest.json',evidence/'install-manifest.json')
helpers=evidence/'helpers';helpers.mkdir(exist_ok=True)
for source in Path(__file__).parent.iterdir():
    if source.is_file():shutil.copy2(source,helpers/source.name)
manifest=json.loads((validation/'install-manifest.json').read_text())
for entry in manifest:
    assert hashlib.sha256((root/'app'/entry['file']).read_bytes()).hexdigest()==entry['sha256']
    assert hashlib.sha256(Path(entry['source']).read_bytes()).hexdigest()==entry['sha256']
print('Documentation, evidence and 13 installed hashes verified')
