# SPDX-License-Identifier: LGPL-2.1-or-later
"""Independent native part-file export; sources are never edited or saved."""
import os
from pathlib import Path
import tempfile
import FreeCAD as App
from . import document, hierarchy


def collect(definitions):
    selected = tuple(dict.fromkeys(definitions))
    if not selected:
        raise ValueError('Select at least one part to export')
    result, seen, catalogs = [], set(), {}
    def visit(part):
        source = part.Document
        if source not in catalogs:
            if source.HasPendingTransaction:
                raise ValueError('Finish the current operation before exporting parts')
            catalogs[source] = set(document.validate(source).Definitions)
        if part not in catalogs[source]:
            raise ValueError('The selected part is no longer available')
        if part in seen:
            return
        seen.add(part); result.append(part)
        for child in part.Group:
            if child.TypeId == 'App::Link':
                visit(child.LinkedObject)
    for part in selected:
        visit(part)
    return selected, result


def export_parts(definitions, filename):
    """Publish a complete new archive, atomically and without replacing any file.

    Native deep copy remaps shared geometry, expressions, links and joint references
    together. Distinct parts with identical labels receive unique destination labels.
    A private sibling directory contains all intermediate saves and native backups.
    """
    if App.getActiveTransaction():
        raise ValueError('Finish the current operation before exporting parts')
    selected, definitions = collect(definitions)
    path = Path(filename).expanduser().absolute()
    if path.suffix.lower() != '.cadprt':
        raise ValueError('Choose a new .cadprt filename')
    if path.exists() or path.is_symlink():
        raise ValueError('This file already exists; choose a new filename')
    if not path.parent.is_dir():
        raise ValueError('Choose an existing folder for the new file')
    if any(d.FileName and Path(d.FileName).resolve() == path.resolve() for d in App.listDocuments().values()):
        raise ValueError('Choose a filename that is not open in FreeCAD')
    previous = App.ActiveDocument
    destination = None
    try:
        with tempfile.TemporaryDirectory(prefix='.part-export-', dir=path.parent) as temporary:
            staged = Path(temporary) / path.name
            destination = App.newDocument('PartExport', path.stem, hidden=True)
            root = document.create_file_root(destination)
            # Native XLink copying requires a saved destination even when all
            # referenced definitions are included and become domestic afterward.
            document.save_document(destination, staged)
            before = set(destination.Objects)
            copies = destination.copyObject(definitions, True)
            if len(copies) != len(definitions):
                raise ValueError('Native copy did not return the complete part graph')
            created = set(destination.Objects) - before
            if any(target not in created for obj in created for target in obj.OutList):
                raise ValueError('The copied parts retain an outside dependency')
            names = set()
            for original, copied in zip(definitions, copies):
                name = original.Label
                index = 2
                while name in names:
                    name = f'{original.Label} ({index})'; index += 1
                copied.Label = name; names.add(name)
                if App.GuiUp:
                    copied.Visibility = False
            root.Definitions = copies
            mapping = dict(zip(definitions, copies))
            for part in selected:
                hierarchy._place_instance(root, mapping[part])
            document.validate(destination)  # Includes hidden solver ownership/refs.
            document.save_document(destination, staged)
            # A published export must be self-contained, including every XLink.
            from .external import archive_graph
            if len(archive_graph(staged)) != 1:
                raise ValueError('The exported file still depends on a source file')
            App.closeDocument(destination.Name); destination = None
            if os.name == 'nt':
                os.rename(staged, path)  # Windows rename fails if target exists.
            else:
                os.link(staged, path)  # Same filesystem, exclusive publication.
    finally:
        if destination is not None:
            App.closeDocument(destination.Name)
        if previous is not None and previous.Name in App.listDocuments():
            App.setActiveDocument(previous.Name)
    return path
