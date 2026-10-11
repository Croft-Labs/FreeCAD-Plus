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


def new_part():
    """Native New Part adapter: create a definition only, preserving Edit/selection.

    The current defining file owns it, including when editing an imported model.
    Empty native documents can be initialized; existing legacy content is never
    migrated implicitly. New File has its own Part001 + instance contract.
    """
    import FreeCADGui as Gui
    from . import document, editing
    doc = App.ActiveDocument
    if doc is None or Gui.Control.activeDialog() or Gui.activeDocument().getInEdit():
        raise ValueError('Finish the current task before creating a component')
    if not doc.Objects:
        with transaction(doc, 'Create domestic component'):
            root = document.create_file_root(doc)
            definition = doc.addObject('App::Part', 'Part001')
            root.Definitions = [definition]
            definition.Visibility = False
        editing.edit_file(doc)
        return definition
    root = _root(doc)
    view = Gui.activeDocument().activeView()
    active = view.getActiveObject('PlusEdit')
    if active is not None and active != root:
        active, unused_path = editing.context_path(doc)
        doc = active.Document
        root = _root(doc)
    names = {definition.Label for definition in root.Definitions}
    index = 1
    while f'Part{index:03d}' in names:
        index += 1
    return create_definition(doc, f'Part{index:03d}')


def rename_definition(definition, label):
    """Rename the shared definition in its owning file without replacing identity."""
    doc = definition.Document
    root = validate(doc)
    if definition not in root.Definitions:
        raise ValueError('Choose a component definition to rename')
    if not label.strip() or any(d != definition and d.Label == label for d in root.Definitions):
        raise ValueError('Choose a nonempty component name unique within this file')
    if label == definition.Label:
        return False
    if any(flag in definition.getPropertyStatus('Label') for flag in ('ReadOnly', 'Immutable')):
        raise ValueError('This component name is read-only')
    with transaction(doc, 'Rename component'):
        definition.Label = label
        if definition.Label != label:
            raise ValueError('The native document could not retain the requested component name')
    return True


def add_instance(owner, definition, placement=None):
    return add_instances(owner, [(definition, placement, True, True)], 'Place shared component')[0]


def add_instances(owner, entries, label='Paste component instances', display_states=None):
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
    from . import display
    choices = tuple(display_states) if display_states is not None else (None,) * len(entries)
    if len(choices) != len(entries) or any(value is not None and
            (len(value) != 2 or value[0] not in display.TYPES or type(value[1]) is not bool) for value in choices):
        raise ValueError('Invalid copied component display settings')
    result = []
    with transaction(doc, label):
        for (definition, placement, transform, visible), choice in zip(entries, choices):
            instance = doc.addObject('App::Link', 'ComponentInstance')
            instance.setLink(definition)
            instance.LinkTransform = transform
            instance.LinkPlacement = placement if placement is not None else App.Placement()
            owner.addObject(instance)
            if App.GuiUp:
                instance.Visibility = visible
            if choice is not None and choice != display.state(instance):
                display.enable(root); display.write_state(instance, choice)
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
