# SPDX-License-Identifier: LGPL-2.1-or-later
"""Map native selections to component occurrences without guessing a shared path."""
from typing import NamedTuple

import ComponentModel as Model


class Pick(NamedTuple):
    ids: tuple
    component: object
    item: object
    element: str


def definition_paths(root, definition, ids=(), seen=frozenset()):
    key = (root.Document.Name, root.Name)
    if key in seen:
        return []
    if root == definition:
        return [ids]
    paths = []
    for child in Model.children(root):
        if child.LinkedObject:
            paths.extend(definition_paths(child.LinkedObject, definition,
                                          ids + (child.ObjectId,), seen | {key}))
    return paths


def native_path(root, ids, item=None):
    """Native sub-object path, retaining each Link instead of selecting its source."""
    chain = Model._path(root, ids)
    component = chain[-1].LinkedObject if chain else root
    names = [link.Name for link in chain]
    if item is not None and item != component:
        if Model.owner(item) != component:
            raise ValueError("Select an item owned by this component occurrence.")
        names.append(item.Name)
    return "".join(name + "." for name in names)


def resolve(root, base, subname=""):
    """Return all possible contexts; a bare shared object is intentionally ambiguous."""
    if base is None:
        return []
    if Model.is_component(base):
        component, item = base, None
        starts = definition_paths(root, base)
    elif getattr(base, "ComponentRole", "") == "Occurrence":
        parent = Model.owner(base)
        if not Model.is_component(parent) or not base.LinkedObject:
            return []
        starts = [ids + (base.ObjectId,) for ids in definition_paths(root, parent)]
        component, item = base.LinkedObject, None
    else:
        component, item = Model.owner(base), base
        if not Model.is_component(component):
            return []
        starts = definition_paths(root, component)
    suffix = []
    element = ""
    for token in filter(None, subname.split(".")):
        if item is not None:
            # Face/edge/vertex selections still identify the whole evaluated item.
            element = token
            break
        members = [obj for obj in component.Group if obj.Name == token]
        if len(members) != 1:
            return []
        obj = members[0]
        if getattr(obj, "ComponentRole", "") == "Occurrence":
            if not obj.LinkedObject:
                return []
            suffix.append(obj.ObjectId)
            component = obj.LinkedObject
        else:
            item = obj
    return [Pick(ids + tuple(suffix), component, item, element) for ids in starts]


def selected(root, entries):
    picks = []
    for entry in entries:
        for subname in entry.SubElementNames or [""]:
            for pick in resolve(root, entry.Object, subname):
                if pick not in picks:
                    picks.append(pick)
    return picks


def reference_choice(root, parent, entries):
    """Use only one unambiguous direct-child geometry relationship, never a grandchild."""
    entries = list(entries)
    if len(entries) != 1:
        return None
    candidates = []
    for pick in selected(root, entries):
        if pick.item is None or not pick.ids or not hasattr(pick.item, "Shape"):
            return None
        occurrence = Model._path(root, pick.ids)[-1]
        if Model.owner(occurrence) != parent:
            return None
        if getattr(pick.item, "ComponentRole", "") not in ("Object", "Result", "Reference"):
            return None
        pair = (occurrence, pick.item)
        if pair not in candidates:
            candidates.append(pair)
    return candidates[0] if len(candidates) == 1 else None
