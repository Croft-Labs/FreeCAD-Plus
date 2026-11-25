# SPDX-License-Identifier: LGPL-2.1-or-later
"""Identity-qualified, nonrecursive removal of one component occurrence."""
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import re
import FreeCAD as App
import FreeCADGui as Gui
from . import assembly, constraints, document, instance_patterns, panel


def qualified(obj):
    return (Path(obj.Document.FileName).name or obj.Document.Label) + ' / ' + obj.Label


def guard(dock):
    dock._clipboard_guard()
    if Gui.Control.activeDialog():
        raise ValueError('Finish the current task before removing an instance')
    if dock._binding is None or dock._current() != dock._binding:
        raise ValueError('The active file tab changed; reopen Remove instance')


def contexts(dock, link):
    result = []
    for binding, state in dock._states:
        try:
            active, path = dock._context(*binding)
        except (ValueError, RuntimeError, ReferenceError):
            continue
        if link in path:
            raise ValueError('Edit the parent component before removing this instance or its Edit ancestor')
        # Preserve the selected fixed assembly route in every open component view.
        assembly_path = tuple(state.get('assembly_path', ()))
        if panel.identity(link) in assembly_path:
            raise ValueError('Choose an active assembly above this instance before removing it')
        result.append((binding, panel.identity(active) if active else None,
                       tuple(panel.identity(o) for o in path), state.get('assembly'), assembly_path))
    return tuple(result)


def linked_dependencies(targets):
    """Include hidden links and native subpaths rooted at an ancestor."""
    targets = set(targets)
    dependents = {o for target in targets for o in target.InList}
    for doc in App.listDocuments().values():
        for obj in doc.Objects:
            for name in obj.PropertiesList:
                kind = obj.getTypeIdOfProperty(name)
                if 'Link' not in kind: continue
                value = getattr(obj, name)
                if 'LinkSub' in kind:
                    for ref in (value if 'List' in kind else [value]):
                        if not ref or ref[0] is None: continue
                        base, subs = ref
                        if base in targets: dependents.add(obj); continue
                        for sub in ([subs] if isinstance(subs, str) else subs):
                            try: route = base.getSubObjectList(sub)
                            except (ValueError, RuntimeError): route = ()
                            if targets.intersection(route): dependents.add(obj)
                else:
                    values = value if isinstance(value, (list, tuple)) else [value]
                    if any(item in targets for item in values if hasattr(item, 'Document')):
                        dependents.add(obj)
            # Native expressions usually contribute a direct InList dependency.
            # Also protect qualified references through a parent object.
            for _, expression in getattr(obj, 'ExpressionEngine', ()):
                for target in targets:
                    reachable = any(target == root or target in root.OutListRecursive for root in obj.OutList)
                    if reachable and (re.search(r'(?<![A-Za-z0-9_])' + re.escape(target.Name) + r'(?![A-Za-z0-9_])', expression)
                            or '<<' + target.Label + '>>' in expression):
                        dependents.add(obj)
    return dependents


def shared_parent(owner, host):
    """Count loaded placements through shared ancestors, capped at two."""
    memo = {}
    def uses(part, visiting=()):
        if part in memo: return memo[part]
        if part in visiting: return 2
        total = 0
        for doc in App.listDocuments().values():
            for link in doc.Objects:
                if link.TypeId != 'App::Link' or link.LinkedObject != part: continue
                parents = [o for o in link.InList if o.TypeId == 'App::Part' and link in o.Group]
                for parent in parents:
                    total += 1 if 'PlusFormat' in parent.PropertiesList else uses(parent, (*visiting, part))
                    if total >= 2: memo[part] = 2; return 2
        memo[part] = total
        return total
    if owner.Document != host or uses(owner) > 1: return True
    # Catalog imports can be used later even when not presently placed.
    return any(doc != owner.Document and owner.Document in doc.OutList
               for doc in App.listDocuments().values())


def properties(obj):
    return tuple((name, repr(getattr(obj, name))) for name in obj.PropertiesList
                 if name != 'Proxy' and ('JointType' in obj.PropertiesList
                 or 'Link' in obj.getTypeIdOfProperty(name) or name in ('ExpressionEngine', 'Label')))


@dataclass(frozen=True)
class Plan:
    row: object
    link: tuple
    owner: tuple
    definition: tuple
    context: tuple
    siblings: tuple
    constraints: tuple
    blocked: tuple
    shared: bool
    signature: tuple


def plan(dock, row):
    guard(dock)
    if row.kind != 'occurrence' or not row.path:
        raise ValueError('Choose one individual child instance in Assembly; roots and groups cannot be removed')
    host, definition = dock._checked(row)
    if row.key not in dock._maps[1]:
        raise ValueError('The assembly changed; select the instance again')
    link = panel.lookup(row.path[-1])
    route = tuple(panel.lookup(ref) for ref in row.path[:-1])
    owner = assembly.resolve(panel.lookup(row.anchor), route) if row.anchor else (
        hierarchy_owner(host, route))
    if owner not in document.validate(owner.Document).Definitions or link not in owner.Group:
        raise ValueError('Choose a child of a component assembly')
    state = contexts(dock, link)
    siblings = tuple(panel.identity(o) for o in owner.Group
                     if o.TypeId == 'App::Link' and o.LinkedObject == definition)
    members = set(constraints.joints(owner))
    dependents = linked_dependencies([link]) - {owner}
    joints = dependents.intersection(members)
    blocked = dependents - joints
    if joints:
        solver = constraints.solver_for(owner); group = constraints.group_for(solver)
        blocked.update(linked_dependencies(joints) - {solver, group, owner, *joints})
    reasons = tuple(sorted('Cannot remove: ' + qualified(o) + ' uses this instance or a listed constraint. '
                           'Edit or remove that reference first.' for o in blocked))
    if instance_patterns.controller(link):
        reasons = ('This instance is controlled by a pattern. Use Edit instance pattern to change its quantity.',)
    shared = shared_parent(owner, host)
    joint_refs = tuple(sorted(panel.identity(o) for o in joints))
    signature = (dock._binding, state, tuple(panel.identity(o) for o in owner.Group), siblings,
                 owner.Document.FileName, host.FileName,
                 qualified(owner), qualified(definition), tuple(link.LinkPlacement.toMatrix().A),
                 joint_refs, tuple((panel.identity(o), properties(o)) for o in sorted(joints | blocked, key=panel.identity)),
                 reasons, shared)
    return Plan(row, panel.identity(link), panel.identity(owner), panel.identity(definition),
                state, siblings, joint_refs, reasons, shared, signature)


def hierarchy_owner(doc, route):
    from . import hierarchy
    return hierarchy.resolve(doc, route)[0] if route else document.validate(doc)


@contextmanager
def without_solving():
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/Mod/Assembly')
    exists = any(entry[1] == 'SolveOnRecompute' for entry in (prefs.GetContents() or ()))
    previous = prefs.GetBool('SolveOnRecompute', True)
    prefs.SetBool('SolveOnRecompute', False)
    try: yield
    finally:
        if exists: prefs.SetBool('SolveOnRecompute', previous)
        else: prefs.RemBool('SolveOnRecompute')


def selection_without(link):
    keep, original = [], []
    for selected in Gui.Selection.getSelectionEx('', 0):
        obj = selected.Object
        for sub in selected.SubElementNames or ('',):
            entry = (obj.Document.Name, obj.Name, sub); original.append(entry)
            if obj != link and link not in obj.getSubObjectList(sub): keep.append(entry)
    return original, keep


def restore_selection(entries):
    Gui.Selection.clearSelection()
    for doc, name, sub in entries:
        source = App.listDocuments().get(doc); obj = source.getObject(name) if source else None
        if obj is not None: Gui.Selection.addSelection(doc, name, sub)


def remove(dock, expected, *, include_constraints=False, acknowledge_shared=False):
    if dock._current() != expected.signature[0]:
        raise ValueError('The active file tab changed; reopen Remove instance')
    current = plan(dock, expected.row)
    if current.signature != expected.signature:
        raise ValueError('The removal plan changed. Cancel and reopen Remove instance to review it again.')
    if current.blocked: raise ValueError('\n'.join(current.blocked))
    if current.constraints and not include_constraints:
        raise ValueError('Include the listed assembly constraints or change their references first')
    if current.shared and not acknowledge_shared:
        raise ValueError('Acknowledge removal from the shared parent assembly')
    link, owner = panel.lookup(current.link), panel.lookup(current.owner)
    host = dock._binding[0]
    original, keep = selection_without(link)
    placements = [(o, App.Placement(o.LinkPlacement)) for doc in App.listDocuments().values()
                  for o in doc.Objects if o.TypeId == 'App::Link' and o != link]
    try:
        with without_solving(), document.transaction(owner.Document, 'Remove component instance'):
            names = [panel.lookup(ref).Name for ref in current.constraints] + [link.Name]
            for name in names: owner.Document.removeObject(name)
            if any(owner.Document.getObject(name) is not None for name in names):
                raise ValueError('The native document could not remove the selected instance and constraints')
            owner.Document.recompute()
            if host != owner.Document: host.recompute()
            if any(not obj.LinkPlacement.isSame(value, 1e-9) for obj, value in placements):
                raise ValueError('Removal would reposition another instance; no changes were kept')
    except Exception:
        restore_selection(original)
        raise
    restore_selection(keep)
    dock.refresh()
