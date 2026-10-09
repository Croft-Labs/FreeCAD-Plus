# Component definition deletion

Run TestComponentDefinitionDeletion in this fork's native runtime with
FREECAD_PLUS_VALIDATION_DIR pointing to the authorized validation directory.
The service accepts an unused, unreferenced domestic definition after its placed
occurrences are removed. File/metadata roots remain protected. Tests cover the
initial Part001, empty save/reopen, identity-preserving Undo/Redo, native owned
Body payloads, child occurrence removal without deleting linked definitions,
loaded external occurrences, geometry/expression consumers, pending edits and
failure rollback. TestComponentFileContainer provides the adjacent migration
regression suite. UI deletion/edit-context acceptance remains roadmap 7.8.13d2c2;
these backend tests do not establish native Delete or Models menu behavior.
