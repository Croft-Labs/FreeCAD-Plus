# SPDX-License-Identifier: LGPL-2.1-or-later
"""Toolbar entry into the existing component Appearance task."""
import FreeCAD as App
import FreeCADGui as Gui
from . import appearance, document, editing


def target():
    doc = App.ActiveDocument
    if doc is None:
        raise ValueError('Open a component file and activate the component to change.')
    owner, unused = editing.context_path(doc)
    if owner not in document.validate(owner.Document).Definitions:
        raise ValueError('Activate a component before opening Appearance.')
    if not appearance.results(owner, include_history=True):
        raise ValueError('This component has no bodies or meshes to color.')
    return owner


class Command:
    def GetResources(self):
        return dict(MenuText='Appearance', Pixmap='Std_SetAppearance',
                    ToolTip='Change body or face appearance in the active component')

    def IsActive(self):
        try:
            if Gui.Control.activeDialog() or (Gui.activeDocument() and Gui.activeDocument().getInEdit()):
                return False
            target()
            return True
        except (ValueError, RuntimeError, ReferenceError, AttributeError):
            return False

    def Activated(self):
        from .appearance_task import open_task, selection_snapshot
        try:
            open_task(target(), selection_snapshot())
        except (ValueError, RuntimeError, ReferenceError, AttributeError) as error:
            from .thicken_task import show_error
            show_error('Appearance', str(error))


def install():
    Gui.addCommand('Plus_Appearance', Command())
