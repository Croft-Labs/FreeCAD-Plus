# SPDX-License-Identifier: LGPL-2.1-or-later
"""Assembly navigation and counts; never change component membership or placement."""
import json
import FreeCAD as App
from . import document, display


def files(current):
    """Current file first, then other loaded component catalogs."""
    result = []
    for doc in sorted(App.listDocuments().values(), key=lambda d: (d != current, d.Label)):
        if not any('PlusFormat' in obj.PropertiesList for obj in doc.Objects):
            continue
        root = document.validate(doc)
        result.append((doc, tuple(root.Definitions)))
    return result


def counts(definitions):
    """Count descendant instances, not unique definitions; visibility is irrelevant."""
    memo, visiting = {}, set()
    def count(part):
        key = (str(part.Document.Uid), part.Name, part.ID)
        if key in visiting:
            raise ValueError('Circular component nesting cannot be counted')
        if key not in memo:
            visiting.add(key)
            total = 0
            for link in part.Group:
                if link.TypeId != 'App::Link' or display.state(link)[0] in ('Reference', 'Excluded'):
                    continue
                child = link.LinkedObject
                if child is None:
                    raise ValueError('An assembly component is no longer available')
                total += 1 + count(child)
            visiting.remove(key)
            memo[key] = total
        return memo[key]
    return {part: count(part) for part in definitions}


def label(part, current):
    from pathlib import Path
    return part.Label if part.Document == current else part.Label + ' (' + (Path(part.Document.FileName).stem if part.Document.FileName else part.Document.Label) + ')'


BOOKMARK = 'FreeCADPlus.ActiveAssembly'


def _reference(obj):
    return [str(obj.Document.Uid), obj.Name, obj.ID]


def _resolve_reference(ref):
    uid, name, object_id = ref
    source = next((d for d in App.listDocuments().values() if str(d.Uid) == uid), None)
    obj = source.getObject(name) if source else None
    return obj if obj is not None and obj.ID == object_id else None


def remember(doc, part, path=()):
    """Store navigation in the host archive without creating dependency edges."""
    value = json.dumps({'version': 1, 'part': _reference(part),
                        'path': [_reference(obj) for obj in path]}, sort_keys=True)
    meta = dict(doc.Meta)
    if meta.get(BOOKMARK) != value:
        meta[BOOKMARK] = value
        doc.Meta = meta


def recalled_path(doc, part):
    try:
        data = json.loads(doc.Meta.get(BOOKMARK, '{}'))
        path = tuple(_resolve_reference(ref) for ref in data.get('path', ()))
        if path and all(obj is not None for obj in path):
            from . import hierarchy
            if hierarchy.resolve(doc, path)[0] == part:
                return path
    except (ValueError, TypeError, KeyError, RuntimeError, ReferenceError):
        pass
    return ()


def recalled(doc):
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/FreeCADPlus/Assembly')
    try:
        if BOOKMARK in doc.Meta:
            data = json.loads(doc.Meta[BOOKMARK])
            if data.get('version') != 1:
                return None
            ref = data['part']
        else:
            # Migration fallback only: saved bookmarks always beat workspace history.
            ref = json.loads(prefs.GetString(str(doc.Uid)))
        part = _resolve_reference(ref)
        if part is not None and part in document.validate(part.Document).Definitions:
            return part
    except (ValueError, TypeError, KeyError, AttributeError, RuntimeError, ReferenceError):
        pass
    return None


def resolve(anchor, path):
    owner = anchor
    for link in path:
        if link.TypeId != 'App::Link' or link not in owner.Group or link.LinkedObject is None:
            raise ValueError('The assembly occurrence changed; select it again')
        owner = link.LinkedObject
    return owner
