# Saved project packaging (F108)

Use the source-built fork: Tools > Package saved project.

1. Save a root document and its linked source documents after recomputing.
2. Review the source files and package paths. Relative native links are followed
   recursively, even for unopened documents. Equal filenames retain their separate
   directories. This copies saved files; unsaved edits are never silently discarded.
3. Resolve any listed blocker. Missing files, absolute links, external file/path
   assets and Python feature code are outside this pilot. Refresh after changes.
4. Choose a new `.zip` filename and Create package. Existing files are never
   overwritten. Source changes require a fresh review; failures leave no package.
5. Extract the entire ZIP into a new folder. Close the original root and sources,
   then open the manifest's entrypoint under `documents/`. Keep its layout intact.
6. Check nested/repeated links, edit a copied source, recompute and save/reopen.
   The originals must remain untouched. The package preserves document/object
   identities; it does not make independent definition identities (Make Unique).

Embedded native archive assets are retained byte-for-byte. Add-ons, external
assets, general reference repair, independent duplication, format migration and
unsupported destination filesystems remain open. Native packaging is separate
from flattened geometry export. Stop at this bounded workflow pending owner tests.

## Recorded validation (2026-10-01)

Tasks 15.6a/b preceded one successful 110-second FreeCADGui build and matching
Python staging. Eight package checks and seven companion dependency checks pass
(15 distinct, no skips). Six captures were reviewed. Fixture setup was corrected
to save owner documents before linking and use native GUI save; no implementation
correction or extra native build was needed. Full F108 and owner acceptance stay open.

Evidence: `D:\Temp\Office-PC\freecad-plus-project-package-20261001`.
Try `visual/Portable-Project.zip`, or open the extracted
`visual/relocated/documents/root/main.FCStd` after closing original documents.
The original test sources were moved to `visual/original-unavailable/` before
opening the extracted package. Source/runtime hashes are in `evidence.json`.
Automated native procedure: `tests/TestProjectPackage.py`.
