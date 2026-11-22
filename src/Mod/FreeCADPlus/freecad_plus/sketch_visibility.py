# SPDX-License-Identifier: LGPL-2.1-or-later
"""Scoped native origin visibility for sketch support selection."""
from . import document


def temporary_visibility(obj, shown):
    view = obj.ViewObject
    if view.Visibility == shown:
        return
    no_modify = 'NoModify' in view.getPropertyStatus('Visibility')
    if not no_modify:
        view.setPropertyStatus('Visibility', 'NoModify')
    try:
        view.Visibility = shown
    finally:
        if not no_modify:
            view.setPropertyStatus('Visibility', '-NoModify')


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
        # Transactions record the persistent state, never the automatic reveal.
        self.restore()
        try:
            changed = route if shown else route[-1:]
            # Hiding a temporarily revealed plane may already match its saved
            # state. Do not leave an empty native transaction active in that case.
            if any(bool(obj.Visibility) != shown for obj in changed):
                with document.transaction(route[-1].Document,
                                          ('Show ' if shown else 'Hide ') + route[-1].Label):
                    for obj in changed:
                        obj.Visibility = shown
            for obj in changed:
                if obj in self.saved:
                    self.saved[obj] = bool(obj.Visibility)
                    self.manual.add(obj)
        finally:
            self.apply()
