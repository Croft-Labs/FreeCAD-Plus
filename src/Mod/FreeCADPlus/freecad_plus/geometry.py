# SPDX-License-Identifier: LGPL-2.1-or-later
"""Occurrence-aware geometry eligibility, separate from selection and visibility.

Consumers call this before reading native shapes. This is not a global selection
filter and does not intercept arbitrary native commands or direct Python access.
"""
from . import document, display, hierarchy, external


# Keep eligibility and persistence on the same native ownership contract.
_owned_path = document.owned_path


def require_access(doc, obj, sub='', *, active=None, active_path=()):
    """Refuse raw Reference/Excluded geometry before a consumer reads its shape.

    The caller supplies its originating view's Edit context, never a global active
    component. Native occurrence paths retain distinctions between shared uses.
    Bare foreign members must be selected through an occurrence; owned derived
    features stop at their own object, without following their dependency links.
    A raw component aggregate is refused if it contains any forbidden descendant.
    """
    root = document.validate(doc)
    active_path = tuple(active_path)
    if active_path:
        if hierarchy.resolve(doc, active_path)[0] != active:
            raise ValueError('The geometry editing context changed')
    elif active is not None and active not in external.available_definitions(root):
        raise ValueError('The edited component is not in this file catalog')
    if obj is None or obj.Document.getObject(obj.Name) != obj:
        raise ValueError('The geometry reference is no longer available')

    base = root
    if obj == root:
        objects = []
    elif active is not None and (owned := _owned_path(active, obj)) is not None:
        # A member of the active definition has an unambiguous editing occurrence.
        base = active if not active_path else root
        objects = [*active_path, *owned]
    elif obj in root.Group:
        objects = [obj]
    else:
        raise ValueError('Select geometry through its component occurrence in this file')
    # Let FreeCAD parse mapped element names, which themselves can contain dots.
    # Splitting a subname would mistake a native topology token for another object.
    if sub and obj.getSubObject(sub, 1) is None:
        raise ValueError('The geometry occurrence path is invalid or no longer available')
    chain = obj.getSubObjectList(sub)
    if not chain or chain[0] != obj:
        raise ValueError('The geometry occurrence path is invalid or no longer available')
    objects.extend(chain[1:])
    current = base
    route = () if base == root else active_path

    def check_type(target, path, is_self=False):
        if active_path and active_path[:len(path)] == path:
            kind = display.state(active)[0] if path == active_path else 'Full Component'
        elif is_self:
            kind = display.state(target)[0]
        else:
            kind = display.resolved(target, direct=(path[:-1] == active_path))[0]
        if kind == 'Reference':
            raise ValueError('Add Reference Feature before using Reference geometry')
        if kind == 'Excluded':
            raise ValueError('Change Part Type before using Excluded geometry')

    if base != root:
        check_type(base, route, is_self=True)
    for child in objects:
        if _owned_path(current, child) is None:
            raise ValueError('The geometry occurrence path is invalid or no longer available')
        if child.TypeId == 'App::Link':
            route = (*route, child)
            check_type(child, route)
            current = child.LinkedObject
        else:
            current = child

    def check_aggregate(owner, path):
        for child in getattr(owner, 'Group', ()):
            if child.TypeId == 'App::Link':
                nested = (*path, child)
                check_type(child, nested)
                check_aggregate(child.LinkedObject, nested)
    # A feature's outgoing source dependencies are deliberately not traversed.
    # Promotion owns a new feature; its source association is not an occurrence.
    if current.TypeId == 'App::Part':
        check_aggregate(current, route)
    return current


def export_objects(doc):
    """Build the native resolved payload from its original component selection.

    A placed external feature resolves into its defining file, while the selection
    and saved occurrence restrictions belong to the visible assembly. Never replace
    that selection with all objects in the source catalog.
    """
    import FreeCADGui as Gui

    context = doc
    if not Gui.Selection.getSelectionEx(doc.Name, 0):
        gui = Gui.activeDocument()
        if gui is not None and gui.Document != doc:
            candidate = gui.Document
            if any('PlusFormat' in obj.PropertiesList for obj in candidate.Objects):
                resolved = Gui.Selection.getSelectionEx(candidate.Name)
                if any(entry.Object.Document == doc for entry in resolved):
                    context = candidate
    objects = list(dict.fromkeys(entry.Object for entry in
                                 Gui.Selection.getSelectionEx(context.Name)))
    require_export(context, objects)
    return objects


def require_export(doc, objects):
    """Check the native File > Export payload before options or a writer run.

    Preserve unresolved occurrence paths before the exporter's object-only list
    loses them. Never infer an occurrence from a shared definition's first use.
    Whole-file fallback would include unused catalog/source objects, so require
    an explicit selection in component files. Ordinary files do not call here.
    """
    import FreeCAD as App
    import FreeCADGui as Gui
    from . import isolation

    root = document.validate(doc)
    selections = Gui.Selection.getSelectionEx(doc.Name, 0)
    if not selections:
        raise ValueError('Select a component occurrence or an owned feature to export')
    context_doc, active, path = doc, None, ()
    gui = Gui.activeDocument()
    if gui is not None:
        view = gui.activeView()
        unused = isolation.current(view)
        if unused is not None and unused.definition().Document == doc:
            context_doc, active = unused.doc, unused.definition()
        elif App.ActiveDocument == doc:
            resolved, parent, sub = view.getActiveObject('PlusEdit', False)
            if parent == root and sub:
                active, path = hierarchy.resolve(doc, sub.rstrip('.').split('.'))
                if active != resolved:
                    raise ValueError('The component Edit context changed')

    approved = set()
    for entry in selections:
        for sub in entry.SubElementNames or ('',):
            # Exporting the file must respect every saved exclusion, even when
            # its currently edited branch has a temporary display override.
            whole_file = entry.Object == root and not sub
            result = require_access(context_doc, entry.Object, sub,
                                    active=None if whole_file else active,
                                    active_path=() if whole_file else path)
            approved.add(result)
            approved.add(entry.Object.getSubObject(sub, 1) if sub else entry.Object)
    # Check the actual object list as well as its originating selections. A
    # mismatched/fallback catalog payload must not acquire permission by accident.
    if any(obj is None or obj not in approved for obj in objects):
        raise ValueError('The export selection changed; select the component geometry again')


def require_modeling_inputs(consumer, inputs=None):
    """Check native modeling intake without replacing its own geometry rules.

    None means the current unresolved selection (command start); an explicit list
    means the native picker/selection callback's actual references. Existing feature
    dependencies are not traversed or rewritten on recompute.
    """
    import FreeCADGui as Gui
    from . import isolation

    gui = Gui.activeDocument()
    if gui is None:
        raise ValueError('Edit a component before using modeling geometry')
    doc = gui.Document
    root = document.validate(doc)
    view = gui.activeView()
    unused = isolation.current(view)
    if unused is not None:
        active, path = unused.definition(), ()
    else:
        resolved, parent, sub = view.getActiveObject('PlusEdit', False)
        if parent != root or not sub:
            raise ValueError('Edit a component before using modeling geometry')
        active, path = hierarchy.resolve(doc, sub.rstrip('.').split('.'))
        if active != resolved:
            raise ValueError('The component Edit context changed')
    if _owned_path(active, consumer) is None:
        raise ValueError('The modeling object must belong to the edited component')
    if inputs is None:
        inputs = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('*', 0)
                  for sub in entry.SubElementNames or ('',)]
    if consumer.isDerivedFrom('Part::Compound') and consumer.Document != doc:
        raise ValueError('Open the defining file to edit Compound inputs')
    for obj, sub in inputs:
        require_access(doc, obj, sub, active=active, active_path=path)
        if consumer.isDerivedFrom('Part::Compound'):
            target = obj.getSubObject(sub, 1) if sub else obj
            if _owned_path(active, target) is None or target == active:
                raise ValueError('Compound inputs must be owned by the edited component')


def require_part_boolean_inputs(doc, inputs=None):
    """Preflight supported Part Boolean/Compound inputs before native mutation.

    Result and inputs retain ownership in the edited definition. Foreign component
    transfer/reference workflows are not inferred from the native flattening helper.
    """
    import FreeCADGui as Gui
    from . import isolation
    gui = Gui.activeDocument()
    if gui is None:
        raise ValueError('Edit a component before using modeling geometry')
    view = gui.activeView()
    unused = isolation.current(view)
    active = unused.definition() if unused is not None else view.getActiveObject('PlusEdit')
    if active is None or active == document.validate(gui.Document):
        raise ValueError('Edit a component before using modeling geometry')
    if active.Document != doc:
        raise ValueError('Open the defining file to use this Part operation')
    if inputs is None:
        inputs = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('*', 0)
                  for sub in entry.SubElementNames or ('',)]
    require_modeling_inputs(active, inputs)
    for obj, sub in inputs:
        target = obj.getSubObject(sub, 1) if sub else obj
        if _owned_path(active, target) is None or target == active:
            raise ValueError('This Part operation currently requires inputs owned by the edited component')
    return active
