# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part-owned native joints. Occurrences retain native placement and identity."""
import FreeCAD as App
from . import document


def owner_of(solver):
    owner = getattr(solver, 'PlusAssemblyOwner', None)
    if (solver.TypeId == 'Assembly::AssemblyObject' and owner is not None
            and owner.TypeId == 'App::Part' and owner.Document == solver.Document
            and solver in owner.Group):
        return owner
    return None


def solver_for(owner):
    return next((obj for obj in owner.Group if owner_of(obj) == owner), None)


def group_for(solver):
    return next((obj for obj in solver.Group if obj.TypeId == 'Assembly::JointGroup'), None)


def joints(owner):
    solver = solver_for(owner)
    group = group_for(solver) if solver is not None else None
    return tuple(group.Group) if group is not None else ()


def owned_children(solver):
    # Native GeoFeatureGroup lists the joints both directly and within JointGroup.
    # Visit each owned object once, through its collector.
    grouped = {child for group in solver.Group if group.TypeId == 'Assembly::JointGroup'
               for child in group.Group}
    return [solver.Origin, *(obj for obj in solver.Group if obj not in grouped)]


def ensure_solver(owner):
    """Caller owns a native transaction, including the lazy schema upgrade."""
    # Native transactions are lazy: HasPendingTransaction is false until the
    # first mutation, even after openTransaction/setActiveTransaction.
    root = document.validate(owner.Document)
    if owner not in root.Definitions:
        raise ValueError('Choose a component assembly')
    solver = solver_for(owner)
    if solver is not None:
        return solver
    import Assembly  # Register native types without switching the user's workbench.
    root.PlusSchema = max(root.PlusSchema, 6)
    solver = owner.Document.addObject('Assembly::AssemblyObject', 'AssemblyConstraints')
    solver.Label = 'Assembly constraints'
    solver.addProperty('App::PropertyLinkHidden', 'PlusAssemblyOwner', 'Component assembly')
    solver.PlusAssemblyOwner = owner
    solver.setEditorMode('PlusAssemblyOwner', 2)
    solver.setEditorMode('Placement', 1)
    solver.Type = 'Assembly'
    owner.addObject(solver)
    group = solver.newObject('Assembly::JointGroup', 'Constraints')
    group.Label = 'Assembly constraints'
    if App.GuiUp:
        solver.ViewObject.ShowInTree = False
        solver.Origin.Visibility = False
        for datum in solver.Origin.OriginFeatures:
            datum.Visibility = False
    return solver


def validate_solver(owner, solver):
    if owner_of(solver) != owner or not solver.Placement.isSame(App.Placement(), 1e-9):
        raise ValueError('The assembly constraint frame must remain fixed within its part')
    groups = [obj for obj in solver.Group if obj.TypeId == 'Assembly::JointGroup']
    if len(groups) != 1:
        raise ValueError('Expected one assembly constraint collector per part')
    group = groups[0]
    if set(solver.Group) != {group, *group.Group}:
        raise ValueError('Unexpected content in the assembly constraint solver')
    allowed = {owner.Origin, solver.Origin, *owner.Group} - {solver}
    for joint in group.Group:
        if (joint.TypeId != 'App::FeaturePython' or 'JointType' not in joint.PropertiesList
                or 'ObjectToGround' in joint.PropertiesList):
            raise ValueError('Assembly collectors contain native joints, not anchored children')
        for name in ('Reference1', 'Reference2'):
            ref = getattr(joint, name, None)
            if ref and ref[0] is not None and ref[0] not in allowed:
                raise ValueError('Constraint references must belong to their owning assembly')


def create(owner, kind, refs):
    """Native API used by automation/tests; the interactive editor shares these objects."""
    import JointObject
    if kind not in JointObject.JointTypes:
        raise ValueError('Unsupported assembly constraint type')
    with document.transaction(owner.Document, 'Create assembly constraint'):
        solver = ensure_solver(owner)
        joint = group_for(solver).newObject('App::FeaturePython', 'Joint')
        JointObject.Joint(joint, JointObject.JointTypes.index(kind))
        if App.GuiUp:
            JointObject.ViewProviderJoint(joint.ViewObject)
        joint.Label = kind + ' joint'
        validate_refs(owner, refs)
        joint.Proxy.setJointConnectors(joint, refs)
        if solver.solve() != 0:
            raise ValueError('The assembly constraints could not be solved')
        return joint


def validate_refs(owner, refs):
    if len(refs) != 2 or any(not ref or ref[0] is None for ref in refs):
        raise ValueError('Select two references from separate components or the assembly frame')
    allowed = {owner.Origin, *owner.Group}
    solver = solver_for(owner)
    if solver is not None:
        allowed.add(solver.Origin)
        allowed.discard(solver)
    if any(ref[0] not in allowed for ref in refs):
        raise ValueError('Choose references within this assembly')
    if refs[0][0] == refs[1][0]:
        raise ValueError('A component cannot be constrained to itself')
    from . import display
    for ref in refs:
        if ref[0].TypeId == 'App::Link' and display.state(ref[0])[0] in ('Reference', 'Excluded'):
            raise ValueError('Reference or excluded components cannot participate in assembly constraints')


def remove(joint):
    solver = joint.Proxy.getAssembly(joint)
    owner = owner_of(solver) if solver is not None else None
    if owner is None or joint not in joints(owner):
        raise ValueError('The assembly constraint is no longer available')
    with document.transaction(owner.Document, 'Delete assembly constraint'):
        owner.Document.removeObject(joint.Name)


def is_plus_document(doc=None):
    doc = doc or App.ActiveDocument
    return doc is not None and any('PlusFormat' in o.PropertiesList for o in doc.Objects)


def active_context():
    import FreeCADGui as Gui
    from . import panel
    dock = panel._panel
    if dock is None or dock._current() != dock._binding or dock._binding is None:
        raise ValueError('Choose an active assembly in the Components panel')
    active, route = dock._context(*dock._binding)
    owner, path = dock._assembly_context(dock._binding, active, route)
    if owner is None:
        raise ValueError('Choose an active assembly in the Components panel')
    document.validate(owner.Document)
    return owner, dock._binding, path


def can_create():
    import FreeCADGui as Gui
    if Gui.Control.activeDialog() or App.getActiveTransaction():
        return False
    try:
        owner, _, _ = active_context()
        return not owner.Document.HasPendingTransaction and any(o.TypeId == 'App::Link' for o in owner.Group)
    except (ValueError, RuntimeError, ReferenceError):
        return False


def can_solve():
    return can_create() and bool(joints(active_context()[0]))


def solve_active():
    import FreeCADGui as Gui
    if Gui.Control.activeDialog() or App.getActiveTransaction():
        raise ValueError('Finish the current operation before solving the assembly')
    owner, _, _ = active_context()
    solver = solver_for(owner)
    if solver is None:
        return
    with document.transaction(owner.Document, 'Solve assembly constraints'):
        owner.Document.recompute()
        if solver.solve() != 0:
            raise ValueError('The assembly constraints could not be solved')


def component_reference(solver, root_obj, sub):
    """Normalize host/linked selection paths to a direct child in the owning frame."""
    owner = owner_of(solver)
    if owner is None:
        return None, ''
    current = root_obj
    tokens = sub.split('.')
    while current is not None:
        effective = current.LinkedObject if current.TypeId == 'App::Link' else current
        if effective == owner:
            if not tokens or not tokens[0]:
                return owner.Origin, ''
            name = tokens.pop(0)
            candidate = next((o for o in [owner.Origin, *owner.Group] if o.Name == name), None)
            if candidate is None or candidate == solver:
                return None, ''
            return candidate, '.'.join(tokens)
        if not tokens or not tokens[0]:
            break
        name = tokens.pop(0)
        children = document.owned_children(effective)
        current = next((o for o in children if o.Name == name), None)
    # Native editor reselects saved component-rooted references directly.
    if root_obj in [owner.Origin, *owner.Group] and root_obj != solver:
        return root_obj, sub
    return None, ''


def open_task(index=0, joint=None):
    from .constraint_task import open_task as open_native_task
    return open_native_task(index, joint)
