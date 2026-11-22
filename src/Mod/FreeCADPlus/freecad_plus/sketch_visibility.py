# SPDX-License-Identifier: LGPL-2.1-or-later
"""Scoped native origin visibility for sketch support selection and drawing."""
from . import document


class Drawing:
    """Mask coordinate render nodes without editing document properties.

    Sketcher commits transactions while drawing. Keeping the mask in Coin,
    outside those transactions and file serialization, preserves native Undo
    and save behavior. Explicit History eyes still edit native Visibility.
    """
    def __init__(self, definition, sketch, binding):
        self.definition = definition
        self.sketch = sketch
        self.binding = binding
        origins = [definition.Origin]
        for parent in document.owned_path(definition, sketch) or ():
            if parent.TypeId == 'PartDesign::Body':
                origins.append(parent.Origin)
        objects = dict.fromkeys(obj for origin in origins for obj in [origin, *origin.OriginFeatures])
        self.masked = {obj: (obj.ViewObject.SwitchNode,
                            obj.ViewObject.SwitchNode.whichChild.getValue()) for obj in objects}
        self.apply()

    def hides(self, obj):
        return obj in self.masked

    def apply(self):
        for obj, (node, saved) in tuple(self.masked.items()):
            try:
                current = node.whichChild.getValue()
                # A native recompute/display refresh may rebuild its switch.
                if current != -1:
                    self.masked[obj] = (node, current)
                node.whichChild = -1
            except (ReferenceError, RuntimeError):
                self.masked.pop(obj, None)

    def restore(self):
        for obj, (node, saved) in self.masked.items():
            try:
                node.whichChild = saved if obj.Visibility else -1
            except (ReferenceError, RuntimeError, NameError):
                pass  # Native document deletion can precede observer cleanup.

    def toggle_many(self, routes, shown, label):
        self.restore()
        changed = tuple(dict.fromkeys(obj for route in routes
                                     for obj in (route if shown else route[-1:])))
        try:
            if any(bool(obj.Visibility) != shown for obj in changed):
                with document.visibility_transaction(changed[-1].Document,
                                          ('Show ' if shown else 'Hide ') + label):
                    for obj in changed:
                        obj.Visibility = shown
            for obj in changed:
                self.masked.pop(obj, None)
        finally:
            self.apply()


def temporary_visibility(obj, shown):
    view = obj.ViewObject
    if view.Visibility == shown:
        return
    # Native view providers synchronize their App-side Visibility property.
    # Protect both halves so temporary solid/feature hiding cannot dirty a file.
    properties = [(obj, 'Visibility'), (view, 'Visibility')]
    # Native groups and linked instances relay child visibility through touch
    # properties. Keep those notifications, but inherit the transient edit's
    # NoModify status so they cannot mark the containing/source document dirty.
    properties += [(parent, name) for parent in obj.InListRecursive
                   for name in ('_GroupTouched', '_LinkTouched')
                   if name in parent.PropertiesList]
    # Part providers may lazily refresh these display properties while changing
    # Visibility, even though their values have not been edited.
    properties += [(view, name) for name in ('ShowPlacement', 'ShapeAppearance', 'Transparency')
                   if name in view.PropertiesList]
    changed = [(owner, name) for owner, name in properties if 'NoModify' not in owner.getPropertyStatus(name)]
    for owner, name in changed:
        owner.setPropertyStatus(name, 'NoModify')
    try:
        view.Visibility = shown
    finally:
        for owner, name in changed:
            owner.setPropertyStatus(name, '-NoModify')


class Planes:
    def __init__(self, definition):
        self.definition = definition
        self.origin = definition.Origin
        self.saved = {obj: bool(obj.Visibility) for obj in
                      [self.origin, *self.origin.OriginFeatures]}
        self.manual = set()
        self.closed = False
        self.apply()

    def apply(self):
        self.closed = False
        if self.origin not in self.manual:
            temporary_visibility(self.origin, True)
        for obj in self.origin.OriginFeatures:
            if obj in self.manual:
                continue
            temporary_visibility(obj, True if obj.Role.endswith('_Plane') else
                                 self.saved[self.origin] and self.saved[obj])

    def restore(self):
        if self.closed:
            return
        self.closed = True
        for obj, shown in self.saved.items():
            try:
                temporary_visibility(obj, shown)
            except (ReferenceError, RuntimeError, NameError):
                pass  # The document may already be deleting its origin children.

    def toggle(self, route, shown):
        self.toggle_many((route,), shown, route[-1].Label)

    def toggle_many(self, routes, shown, label):
        # Transactions record the persistent state, never the automatic reveal.
        self.restore()
        try:
            changed = tuple(dict.fromkeys(obj for route in routes
                                          for obj in (route if shown else route[-1:])))
            # Hiding a temporarily revealed plane may already match its saved
            # state. Do not leave an empty native transaction active in that case.
            if any(bool(obj.Visibility) != shown for obj in changed):
                with document.visibility_transaction(changed[-1].Document,
                                          ('Show ' if shown else 'Hide ') + label):
                    for obj in changed:
                        obj.Visibility = shown
            for obj in changed:
                if obj in self.saved:
                    self.saved[obj] = bool(obj.Visibility)
                    self.manual.add(obj)
        finally:
            self.apply()
