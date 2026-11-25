# Condensed/expanded instance display proposal

**Update November 25:** the owner's renewed implementation instruction approved
this prepared layout. [Implementation and installed verification](../instance-display-20261125/README.md)
are now complete. The text below records the earlier UI-only proposal state.

November 25, 2026. The owner requested implementation of condensed/expanded
instances. This is the required native Qt presentation preview, awaiting direct
screenshot approval; production behavior and the installed payload are unchanged.

Compare [current panel](baseline.png) with [proposed modes](proposal.png).
The new Instances selector defaults to Expanded. Repeated siblings are numbered;
Condensed groups the same definition beneath its immediate parent with a count.
Opening a group reveals individual occurrences and their own constraint collectors.
Singletons retain their labels. The group itself has no bulk component action.
Numbers are display ordinals, not stored identifiers or definition renames.

Rendered from a clean snapshot of production panel.py at commit
626ce9bb6886adfc13efedc0a6cad5202f3b5902. Companion review 1339cd788f26 allows
only panel.py; final fingerprint
b97aa8298195bd804b0de852dacca11fa8524fe0c183480ecd9f7930f2bf3639.
The capture is fresh and scope has no violations. Approval remains unset.
An earlier disposable capture failed due to Qt item ownership; its replacement
uses plain presentation snapshots and disables bytecode writes into worktrees.

The existing owner FreeCAD executable rendered disposable documents in isolated
profiles. Fixture includes Motor x3, Gearbox x2, nested Bolt x2, singletons, and
constraints owned by Machine and Gearbox. Both final captures pass unchanged
document structure/placements, Undo count and Edit context checks. Candidate
normal tree actions are disconnected: these images demonstrate layout only,
not working selection, movement or document mutation integration.

Remaining after approval: integrate view grouping and stable per-occurrence
selection/actions, preserve selection when switching modes, reveal a selected
hidden occurrence, persist view preference, verify source/installed/reopening
behavior and the existing owner shortcut. No new native build is anticipated.
Quantity, Remove instance and name enforcement remain separate requests.

Archived render.py, scene.FCMacro and proposal.py preserve fixture provenance;
they are validation helpers, not production modules. Generated profiles and
temporary validation outputs are removed after archiving. Review worktrees remain
available for approval. Unrelated project.previewfirst.json is preserved.
