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


def remember(doc, part):
    """Last explicit choice is a workspace preference, not document geometry/data."""
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/FreeCADPlus/Assembly')
    prefs.SetString(str(doc.Uid), json.dumps([str(part.Document.Uid), part.Name, part.ID]))


def recalled(doc):
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/FreeCADPlus/Assembly')
    try:
        uid, name, object_id = json.loads(prefs.GetString(str(doc.Uid)))
        source = next((d for d in App.listDocuments().values() if str(d.Uid) == uid), None)
        part = source.getObject(name) if source else None
        if part is not None and part.ID == object_id and part in document.validate(source).Definitions:
            return part
    except (ValueError, TypeError, RuntimeError, ReferenceError):
        pass
    return None


def resolve(anchor, path):
    owner = anchor
    for link in path:
        if link.TypeId != 'App::Link' or link not in owner.Group or link.LinkedObject is None:
            raise ValueError('The assembly occurrence changed; select it again')
        owner = link.LinkedObject
    return owner
