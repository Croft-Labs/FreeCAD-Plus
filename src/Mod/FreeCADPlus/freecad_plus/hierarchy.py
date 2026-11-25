# SPDX-License-Identifier: LGPL-2.1-or-later
"""Definitions and occurrences; placement remains native App::Link data."""
import FreeCAD as App
from .document import transaction, validate, show_new_component_frame


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
    from . import naming
    naming.check_name(doc, label)
    with transaction(doc, "Create domestic component"):
        definition = _create_definition(root, label)
    return definition


def _create_definition(root, label):
    """Caller owns validation and the defining-file transaction."""
    definition = root.Document.addObject('App::Part', 'Component')
    show_new_component_frame(definition)
    definition.Label = label
    root.Definitions = [*root.Definitions, definition]
    if App.GuiUp:
        definition.Visibility = False
    return definition


def check_nesting(owner, definition):
    """References and excluded links still participate in cycle prevention."""
    todo, seen = [definition], set()
    while todo:
        current = todo.pop()
        if current == owner:
            raise ValueError('Circular component nesting is not allowed: this would create a parent-child cycle')
        if current in seen:
            continue
        seen.add(current)
        todo.extend(o.LinkedObject for o in current.Group if o.TypeId == 'App::Link')


def _place_instance(owner, definition, placement=None, transform=True, visible=True):
    """Caller owns one transaction, preflight and final graph validation."""
    instance = owner.Document.addObject('App::Link', 'ComponentInstance')
    instance.setLink(definition)
    instance.LinkTransform = transform
    instance.LinkPlacement = placement if placement is not None else App.Placement()
    owner.addObject(instance)
    if App.GuiUp:
        instance.Visibility = visible
    return instance


def add_child(owner, definition=None, *, label=None):
    """Add an existing or new child; catalog/definition/link changes share one Undo."""
    import json
    from . import external
    root = _root(owner.Document)
    if owner not in root.Definitions:
        raise ValueError('Edit a component before adding a child')
    if (definition is None) == (label is None):
        raise ValueError('Choose an existing component or a new component name')
    imported = None
    if definition is None:
        label = label.strip()
        from . import naming
        naming.check_name(owner.Document, label)
    else:
        if definition not in validate(definition.Document).Definitions:
            raise ValueError('The selected component is no longer available')
        check_nesting(owner, definition)
        if definition not in external.available_definitions(root):
            _, imported = external.prepare_import(owner.Document, definition.Document)
    with transaction(owner.Document, 'Add new component' if definition is None else 'Add existing component'):
        if imported is not None:
            root.Imports = [*root.Imports, imported]
            root.ImportIdentities = json.dumps([str(o.Document.Uid) for o in root.Imports])
        if definition is None:
            definition = _create_definition(root, label)
        return _place_instance(owner, definition)


def add_children(owner, definitions):
    """Import the necessary catalogs and place a checked batch in one Undo step."""
    import json
    from . import external
    root = _root(owner.Document)
    if owner not in root.Definitions:
        raise ValueError('Edit a component before adding children')
    definitions = tuple(dict.fromkeys(definitions))
    if not definitions:
        raise ValueError('Choose at least one available component to add')
    available = set(external.available_definitions(root))
    imports = []
    for definition in definitions:
        if definition not in validate(definition.Document).Definitions:
            raise ValueError('The selected component is no longer available')
        check_nesting(owner, definition)
        if definition not in available:
            _, imported = external.prepare_import(owner.Document, definition.Document)
            imports.append(imported)
            available.update(external.available_definitions(imported))
    from . import naming
    naming.check_imports(owner.Document, imports)
    with transaction(owner.Document, 'Add existing components'):
        if imports:
            root.Imports = [*root.Imports, *imports]
            root.ImportIdentities = json.dumps([str(o.Document.Uid) for o in root.Imports])
        return [_place_instance(owner, definition) for definition in definitions]


def new_part():
    """Native New Part adapter: create and activate a definition, showing History.

    The current defining file owns it, including when editing an imported model.
    Empty native documents can be initialized; existing legacy content is never
    migrated implicitly. New File has its own Part001 + instance contract.
    """
    import FreeCADGui as Gui
    from . import document, editing, panel
    doc = App.ActiveDocument
    if doc is None or Gui.Control.activeDialog() or Gui.activeDocument().getInEdit():
        raise ValueError('Finish the current task before creating a component')
    if not doc.Objects:
        with transaction(doc, 'Create domestic component'):
            root = document.create_file_root(doc)
            definition = doc.addObject('App::Part', 'Part001')
            show_new_component_frame(definition)
            root.Definitions = [definition]
            definition.Visibility = False
        panel.show_created_component(doc, definition)
        return definition
    host = doc
    root = _root(doc)
    view = Gui.activeDocument().activeView()
    active = view.getActiveObject('PlusEdit')
    if active is not None and active != root:
        active, unused_path = editing.context_path(doc)
        doc = active.Document
        root = _root(doc)
    from . import naming
    names = naming.reserved(doc)
    index = 1
    while naming.key(f'Part{index:03d}') in names:
        index += 1
    definition = create_definition(doc, f'Part{index:03d}')
    panel.show_created_component(host, definition)
    return definition


def rename_definition(definition, label):
    """Rename the shared definition in its owning file without replacing identity."""
    doc = definition.Document
    root = validate(doc)
    if definition not in root.Definitions:
        raise ValueError('Choose a component definition to rename')
    from . import naming
    naming.check_name(doc, label, definition)
    if label == definition.Label:
        return False
    if any(flag in definition.getPropertyStatus('Label') for flag in ('ReadOnly', 'Immutable')):
        raise ValueError('This component name is read-only')
    with transaction(doc, 'Rename component', check_names=False):
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
        check_nesting(owner, definition)
    from . import display
    choices = tuple(display_states) if display_states is not None else (None,) * len(entries)
    if len(choices) != len(entries) or any(value is not None and
            (len(value) != 2 or value[0] not in display.TYPES or type(value[1]) is not bool) for value in choices):
        raise ValueError('Invalid copied component display settings')
    result = []
    with transaction(doc, label):
        for (definition, placement, transform, visible), choice in zip(entries, choices):
            instance = _place_instance(owner, definition, placement, transform, visible)
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
