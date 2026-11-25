# SPDX-License-Identifier: LGPL-2.1-or-later
"""Names belong to definitions; each imported catalog is one naming scope."""
from pathlib import Path
import unicodedata
import FreeCAD as App


def key(label):
    return unicodedata.normalize('NFC', label.strip()).casefold()


def file_label(doc):
    if not doc.FileName:
        return doc.Label
    path = Path(doc.FileName)
    if any(other != doc and other.FileName and Path(other.FileName).name.casefold() == path.name.casefold()
           for other in App.listDocuments().values()):
        return str(path)
    return path.name


def scopes(doc):
    """Include loaded reverse importers, but not unrelated open files."""
    from . import external
    result = []
    for current in App.listDocuments().values():
        roots = [obj for obj in current.Objects if getattr(obj, 'PlusFormat', None) == 'FreeCADPlus.ComponentDocument']
        if len(roots) != 1 or 'Definitions' not in roots[0].PropertiesList:
            continue
        root = roots[0]
        pending, visited = [root], set()
        affected = False
        while pending:
            candidate = pending.pop()
            if candidate in visited:
                continue
            visited.add(candidate)
            if candidate.Document == doc:
                affected = True
                break
            pending.extend(getattr(candidate, 'Imports', ()))
        if affected:
            result.append((root, external.available_definitions(root)))
    return result


def _check(records, scope):
    seen = {}
    for identity, label, owner in records:
        normalized = key(label)
        if not normalized:
            raise ValueError('Choose a nonempty component name unique within this file and all imported files.')
        previous = seen.get(normalized)
        if previous is not None and previous[0] != identity:
            raise ValueError(f'Component name "{label}" conflicts with "{previous[1]}" in '
                             f'{file_label(previous[2])}; the other component is in {file_label(owner)}. '
                             f'Names must be unique within this file and all imported files '
                             f'({file_label(scope)}). Rename one component in its defining file.')
        seen[normalized] = (identity, label, owner)


def check_name(doc, label, definition=None):
    normalized = key(label)
    if not normalized:
        raise ValueError('Choose a nonempty component name unique within this file and all imported files.')
    for root, definitions in scopes(doc):
        # Permit repairing one legacy collision at a time without requiring an
        # unrelated pre-existing collision to be repaired by the same rename.
        records = [(part, part.Label, part.Document) for part in definitions
                   if part != definition and key(part.Label) == normalized]
        _check([*records, (definition if definition is not None else object(), label, doc)], root.Document)


def check_imports(doc, targets):
    from .external import available_definitions
    incoming = [part for root in targets for part in available_definitions(root)]
    for root, definitions in scopes(doc):
        _check([(part, part.Label, part.Document) for part in [*definitions, *incoming]], root.Document)


def check_copies(doc, labels):
    additions = [(object(), label, doc) for label in labels]
    for root, definitions in scopes(doc):
        _check([*((part, part.Label, part.Document) for part in definitions), *additions], root.Document)


def reserved(doc):
    return {key(part.Label) for _, definitions in scopes(doc) for part in definitions}


def validate_for_save(doc):
    """Used by native Save/Save As/Save Copy as well as Plus operations."""
    for root, definitions in scopes(doc):
        _check([(part, part.Label, part.Document) for part in definitions], root.Document)


class _Observer:
    def __init__(self):
        self.before = {}
        self.reverting = False

    def slotBeforeChangeObject(self, obj, prop):
        if self.reverting or prop != 'Label' or obj.Document.Restoring or obj.Document.Transacting:
            return
        roots = [root for root in obj.Document.Objects if 'Definitions' in root.PropertiesList
                 and getattr(root, 'PlusFormat', None) == 'FreeCADPlus.ComponentDocument']
        if any(obj in root.Definitions for root in roots):
            self.before[obj] = obj.Label

    def slotChangedObject(self, obj, prop):
        if self.reverting or prop != 'Label' or obj not in self.before:
            return
        previous = self.before.pop(obj)
        try:
            check_name(obj.Document, obj.Label, obj)
        except ValueError as error:
            self.reverting = True
            try:
                obj.Label = previous
            finally:
                self.reverting = False
            App.Console.PrintError(str(error) + '\n')
            # Reuse existing panel feedback for native property-editor renames.
            import sys
            module = sys.modules.get('freecad_plus.panel')
            if module is not None and module._panel is not None:
                module._panel._message(str(error))

    def slotDeletedObject(self, obj):
        self.before.pop(obj, None)


_observer = None


def install():
    global _observer
    if _observer is None:
        _observer = _Observer()
        App.addDocumentObserver(_observer)
