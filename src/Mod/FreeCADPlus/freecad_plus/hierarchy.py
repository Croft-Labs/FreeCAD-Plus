# SPDX-License-Identifier: LGPL-2.1-or-later
"""Definitions and occurrences; placement remains native App::Link data."""
import FreeCAD as App
from .document import transaction, validate


def _root(doc):
    root = validate(doc)
    if root.PlusSchema < 3:
        raise ValueError("Hierarchy changes require explicit upgrade to schema 3")
    return root


def upgrade(doc):
    """Explicit, undoable metadata-only upgrade; existing native graphs are a subset."""
    root = validate(doc)
    if root.PlusSchema < 3:
        with transaction(doc, "Upgrade component schema"):
            root.PlusSchema = 3
    return root


def create_definition(doc, label):
    root = _root(doc)
    if not label.strip() or any(d.Label == label for d in root.Definitions):
        raise ValueError("Choose a nonempty component name unique within this file")
    with transaction(doc, "Create domestic component"):
        definition = doc.addObject("App::Part", "Component")
        definition.Label = label
        root.Definitions = [*root.Definitions, definition]
        if App.GuiUp:
            definition.Visibility = False
    return definition


def add_instance(owner, definition, placement=None):
    return add_instances(owner, [(definition, placement, True, True)], 'Place shared component')[0]


def add_instances(owner, entries, label='Paste component instances'):
    """Place a complete batch in one native transaction; never clone definitions."""
    doc = owner.Document
    root = _root(doc)
    from .external import available_definitions
    available = available_definitions(root)
    entries = tuple(entries)
    if not entries:
        raise ValueError('Copy at least one component instance first')
    if owner not in [root, *root.Definitions]:
        raise ValueError('The destination must belong to its defining file')
    # Preflight the entire batch before creating any native objects or Undo entry.
    for definition, placement, transform, visible in entries:
        if definition not in available:
            raise ValueError('Import this component into the destination defining file first')
        todo, seen = [definition], set()
        while todo:
            current = todo.pop()
            if current == owner:
                raise ValueError('Circular component nesting is not allowed')
            if current in seen:
                continue
            seen.add(current)
            todo.extend(o.LinkedObject for o in current.Group if o.TypeId == 'App::Link')
    result = []
    with transaction(doc, label):
        for definition, placement, transform, visible in entries:
            instance = doc.addObject('App::Link', 'ComponentInstance')
            instance.setLink(definition)
            instance.LinkTransform = transform
            instance.LinkPlacement = placement if placement is not None else App.Placement()
            owner.addObject(instance)
            if App.GuiUp:
                instance.Visibility = visible
            result.append(instance)
    return result


def resolve(doc, path):
    """Resolve an explicit sequence of link objects/names from file to occurrence."""
    root = validate(doc)
    path = tuple(path)
    if not path:
        raise ValueError("An occurrence requires a complete path from the file")
    owner, links = root, []
    for token in path:
        link = owner.Document.getObject(token) if isinstance(token, str) else token
        if not link or link.TypeId != "App::Link" or link not in owner.Group:
            raise ValueError("Invalid or stale component occurrence path")
        links.append(link)
        owner = link.LinkedObject
    return owner, tuple(links)


def subname(path):
    return "".join(link.Name + "." for link in path)


def world_placement(doc, path):
    _, links = resolve(doc, path)
    # Let the native engine compose LinkTransform and definition placements.
    return validate(doc).getSubObject(subname(links), 3)


def move_instance(instance, placement):
    doc = instance.Document
    root = _root(doc)
    if instance.TypeId != "App::Link" or not any(instance in owner.Group for owner in [root, *root.Definitions]):
        raise ValueError("Expected an owned component instance")
    with transaction(doc, "Move component instance"):
        instance.LinkPlacement = placement
