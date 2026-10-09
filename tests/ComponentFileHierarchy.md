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

Failed-open regressions cover a replaced external file's identity mismatch after
nested dependencies have loaded, with and without a dependency already open, plus
failure after native root restoration. Only newly opened documents may close;
pre-existing unsaved documents and the active document must be retained.

Manifest preflight cases alter saved archives to omit, duplicate or reparent a
placement, mislabel external ownership, and rename a definition record. Malformed
definitions, occurrence lists/entries, flags and histories must raise ValueError
before native restoration. Normal domestic/external and older occurrence-only
archives remain covered by the same hierarchy/core regression batch.

Import identity regression uses a native Save Copy to open a second file retaining
the original identity. Both a direct alias and an alias below another imported
branch must refuse before adding objects or opening a transaction. The destination
remains valid, while the existing shared-file diamond fixture remains accepted.

Multi-definition file-recovery fixtures move a Hardware file containing two placed
definitions and evaluated references. One Undo must clear the recovered import and
all bindings; Redo/save/reopen retain identities, placements and geometry. An injected
refresh failure after rebinding both definitions must roll back the complete repair.
Include TestComponentFileRecovery.py when changing this shared recovery service.

Save collision regressions use native Save Copy against a directly imported file
and Save As against a nested unused import. Both must refuse without modifying any
fixture bytes or the assembly location/label. Save As and Save Copy into another
directory verify dependency paths, shared identities and reopening; Save Copy
also preserves the original assembly bytes/location. These two relocation tests
require the new native Writer/PropertyXLink implementation, not a Python overlay.
They reproduce broken native links on the current owner runtime and must be run
unfiltered after the next complete native build. Other hierarchy tests can run
with an explicit test-name filter that excludes these two pending native cases.
