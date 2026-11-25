# Native file formats and Classic conversion — November 25, 2026

Owner approval: **"implement file extensions and conversions"**, following the
unfinished-work audit. The native preview was session `a888d3336f92`, fingerprint
`c85cb74d68a13804a657ac917a71db97946334dba0dfde9f6bcb2f2056f871d8`. Its candidate
was fresh and within scope when implementation began. Chat approval is the
authority; companion approval state was not modified.

## Delivered behavior

- Content determines format: Plus `.cadprt`, Classic `.FCStd`, independent of UI
  presentation. Native Save/Save As/Save Copy/Save All/save-on-close agree.
- Open names both formats clearly, defaults to Plus, and retains other registered
  geometry formats. Classic offers explicit conversion, Open Classic, or Cancel.
- Parts import and Add existing source selection accept Classic and convert a
  separate new Plus file. Conversion alone places nothing. Export stays `.cadprt`.
- A Plus archive incorrectly named `.FCStd` can be saved as a corrected `.cadprt`
  copy with a new file identity, preserving the original and external references.
- Conversions read the saved source and preserve unsaved live source edits. They
  refuse existing destinations and unfinished operations in other documents.
- Plus external links are recalculated during Save As/repair. Save Copy uses
  absolute external paths in the output while retaining the original live filename.

## Validation

The native App and GUI targets built successfully with the existing Windows
toolchain; [build log](build-verified.log). The source run passed 60 affected tests;
the final transaction safeguard passed all 22 workflow tests (61 distinct cases
across source checks). Final installed acceptance passed **61/61**, covering the
22 workflow cases plus conversion, Boolean conversion, component imports, external
definitions and part transfer regressions. See [installed results](installed-final-result.json)
and [test details](installed-final-tests.txt).

A fresh installed process reopened six outputs: converted, native saved,
saved-on-close, repaired, relocated and Save Copy files. Native geometry editing
and Undo passed; original Classic data remained Classic. [Reopen results](reopen-result.json).
The existing `freecad plus 0.1.0.lnk` completed four native Open/Save As/Save All/
save-on-close checks. [Shortcut results](shortcut-result.json). The shortcut still
targets `Launch FreeCAD Plus.bat` in the existing payload root, whose executable
remains `app/bin/FreeCAD.exe`; neither shortcut nor launcher was changed.

Validation used isolated settings and disposable fixture documents. Final native
dialog screenshots were inspected directly. The tests found and fixed conversion
commit deferral under native Open and stale external-link paths when changing
directories. An additional guard prevents consuming unrelated pending edits.
Earlier harness failures from long Windows fixture paths and visible QFileDialog
automation were corrected before acceptance.

## Direct screenshots

- [Installed Open](installed-open.png)
- [Installed Plus Save As](installed-save-as.png)
- [Installed Classic save filter](installed-classic-save.png)
- [Installed Convert and open](installed-convert-open.png)
- [Installed Convert and import](installed-convert-import.png)
- [Installed Convert and select parts](installed-convert-add.png)
- [Approved extension-repair dialog](approved-repair-extension.png)
- [Approved component export](approved-component-export.png)

The `approved-*` images are the earlier UI-only proposal. The `installed-*` images
are real widgets exercised in functional installed-app tests.

## Delivery and limits

Three native DLLs and eight Python files were installed into the existing owner
application. All eleven source/installed hashes match the [manifest](install-manifest.json).
Prior files are retained beside their installed counterparts with a
`.before-file-formats-20261125` suffix; newly introduced files have no prior copy.
Restart running FreeCAD Plus sessions to load the native update.

Conversion retains its existing supported editable cases: native Body graphs,
supported Part hierarchies/shared links/Boolean ownership, empty documents and
standalone supported primitives/features. Unsupported structures are reported
without output or automatic geometry flattening; Open Classic remains available.
This is not a claim that every arbitrary `.FCStd` graph is convertible. Independent
part export remains a separate copy operation, and pending Clone, movement and
instance-management work was not implemented here.

Harness files preserve local paths and provenance. Task-generated validation
files/profiles were removed after archiving these results; the useful build,
installed payload, retained rollback files and review worktree remain.
