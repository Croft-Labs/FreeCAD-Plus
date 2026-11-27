# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native-topology face chains, confined to one occurrence and geometry owner."""
import Part
from .curve_selection import _walk

INTENTS = ('Single Surface', 'Connected Surfaces', 'Tangent Surfaces')


def intent():
    from .selection_toolbar import preferences
    value = preferences().GetString('SurfaceIntent', INTENTS[0])
    return value if value in INTENTS else INTENTS[0]


def tangent(first, second, edge):
    try:
        return first.isTangentAt(edge, second, 1e-7)
    except (RuntimeError, ValueError, Part.OCCError):
        return False


def graph(faces, smooth=False):
    result = {i: set() for i in faces}
    buckets = {}
    for index, face in faces.items():
        for edge in face.Edges:
            bucket = buckets.setdefault(edge.hashCode(), [])
            for other, shared in bucket:
                if other == index or not edge.isSame(shared):continue
                if not smooth or tangent(face, faces[other], edge):
                    result[index].add(other);result[other].add(index)
            bucket.append((index, edge))
    return result


def candidates(root, subname, mode, cache=None):
    prefix, _, _ = Part.splitSubname(subname)
    _, _, element = Part.splitSubname(root.resolveSubElement(subname)[2])
    if not element.startswith('Face') or not element[4:].isdigit():return []
    owner = root.getSubObject(prefix, 1) if prefix else root
    if owner is None:return []
    owner = owner.getLinkedObject(True)
    if not hasattr(owner, 'Shape'):return []
    if cache is None:cache = {}
    key = ('surface', root.Document.Name, root.Name, prefix, mode)
    if key not in cache:
        cache[key] = graph(dict(enumerate(owner.Shape.Faces, 1)), mode == INTENTS[2])
    return [prefix+'Face'+str(i) for i in _walk(cache[key], int(element[4:]))]
