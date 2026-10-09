# Component definition deletion

Run TestComponentDefinitionDeletion in this fork's native runtime with
FREECAD_PLUS_VALIDATION_DIR pointing to the authorized validation directory.
The service accepts an unused, unreferenced domestic definition after its placed
occurrences are removed. File/metadata roots remain protected. Tests cover the
initial Part001, empty save/reopen, identity-preserving Undo/Redo, native owned
Body payloads, child occurrence removal without deleting linked definitions,
loaded external occurrences, geometry/expression consumers, pending edits and
failure rollback. TestComponentFileContainer provides the adjacent migration
regression suite. TestComponentDefinitionDeletionUI covers Models menu/keyboard, actual native Delete,
file protection, blocked referenced definitions, unused-edit cleanup, isolated-tab
closing, the last-tab replacement file view and Undo/Redo. Run it alongside
TestComponentActiveEditing and TestComponentFileWorkspace. Source-overlay runs
must replace the installed navigator command adapter and bind the test modules to
the source navigator; otherwise they exercise the older installed implementation.
