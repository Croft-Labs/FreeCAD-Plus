# SPDX-License-Identifier: LGPL-2.1-or-later
from .document import open_document


def insert_mesh(filename, doc, importer, **options):
    """Keep native mesh data and component ownership in one defining-file Undo."""
    import FreeCAD as App
    import FreeCADGui as Gui
    from . import document, editing
    if Gui.Control.activeDialog():
        raise ValueError('Finish the current task before importing a mesh')
    definition, path = editing.context_path(doc)
    owner = definition.Document
    if any(d.HasPendingTransaction for d in App.listDocuments().values()):
        raise ValueError('Finish the current operation before importing a mesh')
    if document.validate(owner).PlusSchema < 8:
        raise ValueError('Mesh history requires component document schema 8')
    before = set(owner.Objects)
    with document.transaction(owner, 'Import mesh'):
        try:
            importer(filename, owner.Name, **options)
        except App.Base.AbortIOException:
            # Native cancellation derives directly from BaseException, bypassing
            # the ordinary transaction helper's Exception rollback.
            owner.abortTransaction()
            owner.recompute()
            raise
        created = [obj for obj in owner.Objects if obj not in before]
        if not created or any(not obj.isDerivedFrom('Mesh::Feature') for obj in created):
            raise ValueError('The mesh reader did not produce supported mesh objects')
        for obj in created:
            definition.addObject(obj)
    editing._restore(doc, definition, path)
    return created


def open(filename):
    import FreeCAD as App
    if App.GuiUp:
        from .file_workflows import open_file
        return open_file(filename)
    return open_document(filename)


def insert(filename, document_name):
    import FreeCAD as App
    from . import external
    doc = App.getDocument(document_name)
    if App.GuiUp and doc == App.ActiveDocument:
        import FreeCADGui as Gui
        from . import editing
        if Gui.Control.activeDialog() or Gui.activeDocument().getInEdit():
            raise ValueError('Finish the current task before importing parts')
        owner, _ = editing.context_path(doc)
        doc = owner.Document
    # Std_Import opens a lazy, still-empty native command before calling insert.
    # Allow that wrapper, but never consume an operation that already has edits.
    if any(d.HasPendingTransaction for d in App.listDocuments().values()):
        raise ValueError('Finish the current operation before importing parts')
    if App.GuiUp:
        from .file_workflows import prepare_source
        filename = prepare_source(filename, purpose='import')
        if not filename:
            return None
    return external.import_path(doc, filename)
