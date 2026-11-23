# SPDX-License-Identifier: LGPL-2.1-or-later
"""Temporary Extrude display, separate from explicit source-owned eye choices."""
from contextlib import contextmanager
import FreeCAD as App
from . import document
from .sketch_visibility import temporary_visibility


@contextmanager
def appearance_edit(view):
    names = [name for name in ('ShapeAppearance', 'ShapeColor', 'Transparency')
             if name in view.PropertiesList and 'NoModify' not in view.getPropertyStatus(name)]
    for name in names:
        view.setPropertyStatus(name, 'NoModify')
    try:
        yield
    finally:
        for name in names:
            view.setPropertyStatus(name, '-NoModify')


def usable(obj, sheet=False):
    if obj.isDerivedFrom('Sketcher::SketchObject'):
        return True
    if obj.TypeId in ('PartDesign::Plane', 'PartDesign::Line', 'PartDesign::Point',
                      'Part::DatumPlane', 'Part::DatumLine', 'Part::DatumPoint'):
        return False
    return obj.isDerivedFrom('Part::Feature') and bool(obj.Shape.Faces or (sheet and obj.Shape.Edges))


class ExtrudeDisplay:
    def __init__(self, task):
        self.task = task
        self.saved = {}
        self.desired = {}
        self.materials = {}
        self.manual = set()
        self.closed = False
        self.style = None
        self.sheet = task.output() == 'Sheet'
        def visit(obj):
            for child in document.owned_children(obj):
                self.saved[child] = bool(child.Visibility)
                visit(child)
        visit(task.owner)
        self.desired = dict(self.saved)
        if task.feature is None:
            for obj in self.saved:
                if not document.owned_children(obj) and not usable(obj, self.sheet):
                    self.desired[obj] = False
                elif obj.TypeId == 'App::Link':
                    self.desired[obj] = False
        else:
            self.desired = {obj: False for obj in self.saved}
            # Face donors stay hidden: the task draws just the referenced face.
            reveal = [obj for obj, _ in task.refs if obj.isDerivedFrom('Sketcher::SketchObject')
                      or (self.sheet and hasattr(obj, 'Shape') and not obj.Shape.Faces)]
            if task.mode() != 'New Solid' and 'target' in task.links:
                reveal.append(task.links['target'][0])
            for obj in reveal:
                for member in document.owned_path(task.owner, obj) or ():
                    self.desired[member] = True
        for obj in self.saved:
            # A Body delegates face colors to its Tip. Editing its container
            # appearance also pastes properties into every historical feature,
            # bypassing their temporary-property guards. Style the actual results.
            if (obj.TypeId != 'PartDesign::Body' and hasattr(obj, 'Shape') and obj.Shape.Solids
                    and 'ShapeAppearance' in obj.ViewObject.PropertiesList):
                self.materials[obj] = (obj.ViewObject.ShapeAppearance, obj.ViewObject.Transparency)
        self.apply()

    def update_usable(self):
        sheet = self.task.output() == 'Sheet'
        if sheet == self.sheet:return
        self.sheet = sheet
        if self.task.feature is None:
            for obj in self.saved:
                if obj not in self.manual and usable(obj, True) and not usable(obj):
                    self.desired[obj] = self.saved[obj] if sheet else False
            self.apply()

    def apply(self):
        self.closed = False
        for obj, shown in self.desired.items():
            temporary_visibility(obj, shown)
        self.update_style()

    def update_style(self):
        if self.closed:
            return
        task = self.task
        target = task.links.get('target', (None, ''))[0] if task.mode() != 'New Solid' else None
        choosing = task.pick == 'target' and task.mode() != 'New Solid'
        packed = App.ParamGet('User parameter:BaseApp/Preferences/View').GetUnsigned('SelectionColor', 0x1CAD1CFF)
        state = (target, choosing, packed)
        if state == self.style:
            return
        self.style = state
        color = tuple(((packed >> shift) & 255) / 255. for shift in (24, 16, 8))
        for obj, (materials, transparency) in self.materials.items():
            view = obj.ViewObject
            with appearance_edit(view):
                view.ShapeAppearance = materials
                view.Transparency = 0 if choosing else 65
                if obj == target:
                    colored = view.ShapeAppearance
                    for material in colored:
                        material.DiffuseColor = color
                    view.ShapeAppearance = colored
        task.refresh_target()

    def restore(self):
        if self.closed:
            return
        self.closed = True
        self.style = None
        for obj, shown in self.saved.items():
            try:
                temporary_visibility(obj, shown)
            except (ReferenceError, RuntimeError, NameError):
                pass
        for obj, (materials, transparency) in self.materials.items():
            try:
                with appearance_edit(obj.ViewObject):
                    obj.ViewObject.Transparency = transparency
                    obj.ViewObject.ShapeAppearance = materials
            except (ReferenceError, RuntimeError, NameError):
                pass

    def toggle_many(self, routes, shown, label):
        self.restore()
        try:
            changed = tuple(dict.fromkeys(obj for route in routes for obj in (route if shown else route[-1:])))
            if any(bool(obj.Visibility) != shown for obj in changed):
                with document.visibility_transaction(changed[-1].Document, ('Show ' if shown else 'Hide ') + label):
                    for obj in changed:
                        obj.Visibility = shown
            for obj in changed:
                if obj in self.saved:
                    self.saved[obj] = bool(obj.Visibility)
                    self.desired[obj] = shown
                    self.manual.add(obj)
        finally:
            self.apply()
