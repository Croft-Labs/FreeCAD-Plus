# Component file hierarchy acceptance

The [component contract](../ai-instructions/architecture/COMPONENT_DOCUMENT_CONTRACT.md)
owns behavior; roadmap 7.8.12 and WORK_STATE own status and build evidence.

`TestComponentFileHierarchy.py` exercises native document/link/transaction APIs and
Qt navigator interactions: explicit unused imports, deletion retention, nested reopen,
file/component cycle refusal, shared diamonds, legacy capability compatibility,
manifest tamper refusal, same-name qualification, all three storage choices,
active-file insertion, external source updates after reopen, missing-import recovery,
independent domestic subtree/external copies, selected replacement and preservation
of IDs/transforms, replacement prompt defaults/cancel, and driven-copy refusal.

Run with `tests/RunComponentDocument.ps1`, a verified Plus executable and a new
output directory under the designated validation root. Set
`FREECAD_PLUS_PROFILE_SOURCE=1` for source-overlay testing. This module loads the
three changed Python modules explicitly and checks loaded core hashes. The engine
remains that executable's native build. Set TestFiles to the hierarchy test followed
by TestComponentDocument.py for the core persistence/identity regression batch.
Do not confuse these checks with a matching native build or owner shortcut delivery.

Copies include the source's domestic definition hierarchy and native owned contents;
already-external children stay shared. General expressions, outside-owned inputs,
replacement consumers/scales/arrays and path overrides refuse before mutation.
Copy and placement replacement are separate undo steps. Cross-file creation saves
the destination before importing it; the two files do not have an atomic shared undo.
The legacy identity-moving service is retained for internal compatibility only.

For installed cold acceptance, set `FREECAD_PLUS_PROFILE_SOURCE=0` and first run
TestComponentFileHierarchy.py without source overlays. Its final case writes ColdAssembly, ColdHardware, ColdCoatings
and ColdOtherAssembly plus stable expected identities into the validation folder.
Start a separate process with TestComponentFileHierarchyCold.py and pass the first
folder through RunComponentDocument.ps1 -ColdFixtureDirectory. This verifies
installed module hashes, nested unused imports, shared definition identity across
assemblies, retained placements and an independent same-name domestic copy. A
second saved source edit and reopen must update only the external uses.

The cold process copies the four files together into its own validation directory
before opening them. This checks relocation and keeps the writer fixtures unchanged
for the later saved-shortcut run. Installed acceptance records application location,
loaded module hashes and process exit; source-overlay passes cannot substitute for it.
