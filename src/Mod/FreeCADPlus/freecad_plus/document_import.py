# SPDX-License-Identifier: LGPL-2.1-or-later
from .document import open_document


def open(filename):
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
    return external.import_path(doc, filename)
