# Single Enter for sketch dimensions - November 23, 2026

Owner approved the isolated preview with "approved. implement". Session
e494680daf44 was re-inspected: preview valid, scope violations empty. Approval
is the explicit chat instruction; the tool approval state was not modified.

The Plus NumericCommitFilter used to consume Enter by moving focus, preventing
native sketch dimension dialogs from reaching their OK action. The correction
is restricted to the native InsertDatum dialog's labelEdit quantity field.
For a valid entry, it commits the native pending quantity on blur, then invokes
native OK exactly once. Both Enter keys work. Invalid/incomplete text remains
focused and open; autorepeat is ignored. Native units, expressions, solver checks,
Cancel/Escape, Reference/Name controls and other numeric-field behavior remain.
There is no layout or constraint persistence format change.

## Native acceptance

All seven focused installed tests passed (zero failures/errors). They cover length X/Y/distance/angle, radius and
diameter; plain values, explicit units, arithmetic, main/keypad Enter, Plus and
Classic layouts, persistent selection on/off, creation Undo/Redo, existing-value
editing, invalid-text recovery, Escape, reference dimensions and ordinary/native
spin arrows plus Extrude/Plane typing-on-blur. An early test incorrectly assumed
Qt rejected a parseable quantity with different units before native acceptance;
that precondition was removed to retain the native validation contract. The
corrected invalid-text/edit/Cancel case passed separately in the development build.

Two payloads are installed with source/build/installed SHA-256 verification and
rollback copies. Only numeric_fields.py changes runtime behavior; TestPlusToolbars.py
adds the native regression cases. Validation profiles are isolated. No owner
profile or unrelated project.previewfirst.json change is included.

The final capture-only test adjustment was checked again in an installed process
(one test passed). [Installed suite](regression.txt), [final focused check](repair.txt)
and [desktop-shortcut check](shortcut.json) record the results. The shortcut starts
the existing installed executable with an isolated profile; existing owner sessions
were not closed. Older running sessions need reopening to load the updated module.

[Native dialog before Enter](dimension-before-enter.png) shows the actual quantity
editor during the 25 mm creation case. [Native sketch after edit](dimension-after-enter.png)
shows the accepted 35 mm constraint after a single keypad Enter; a subsequent Escape
check retained that value. These are real native captures, not preview simulations.

[Install manifest](install-manifest.json) records source/build/installed hashes and
retained rollback locations. Task output was archived here before bounded cleanup;
rollback payloads and the shortcut's isolated profile remain in the runtime folder.
