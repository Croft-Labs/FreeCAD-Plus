# SPDX-License-Identifier: LGPL-2.1-or-later
"""Design idle actions reuse shared sketch/plane and native datum editors."""
import FreeCAD as App
import FreeCADGui as Gui
from . import modeling


def plus_tasks():
    from . import ui_modes
    return ui_modes.modes()[2] == 'Plus'


def eligible():
    if not plus_tasks() or Gui.activeDocument() is None or Gui.Control.activeDialog():
        return False
    try:
        modeling._context(Gui.activeDocument().Document)
        return True
    except (ValueError, RuntimeError, ReferenceError):
        return False


def create_datum(kind):
    if kind not in ('Line', 'Point'):
        raise ValueError('Unsupported datum type')
    if Gui.Control.activeDialog():
        raise ValueError('Finish the current task first')
    doc = Gui.activeDocument().Document
    definition, path = modeling._context(doc)
    transaction = App.setActiveTransaction('Create Datum ' + kind)
    try:
        feature = definition.newObject('PartDesign::' + kind, 'Datum' + kind)
        definition.Document.recompute()
        modeling._enter_editor(doc, definition, path, feature)
        return feature
    except Exception:
        App.closeActiveTransaction(True, transaction)
        raise


class DatumCommand:
    def __init__(self, kind):
        self.kind = kind

    def GetResources(self):
        return {'MenuText': 'Datum ' + self.kind, 'ToolTip': 'Creates a datum ' + self.kind.lower(),
                'Pixmap': 'PartDesign_' + self.kind}

    def IsActive(self):
        return eligible()

    def Activated(self):
        try:
            create_datum(self.kind)
        except (ValueError, RuntimeError) as error:
            App.Console.PrintError(str(error) + '\n')


class ModelingCommand:
    """Plus task label over the native command and its shared component dispatch."""
    def __init__(self, title, command):
        self.title, self.command = title, command

    def GetResources(self):
        return {'MenuText': self.title, 'ToolTip': self.title,
                'Pixmap': self.command}

    def IsActive(self):
        native = Gui.Command.get(self.command)
        return bool(native and native.isActive())

    def Activated(self):
        Gui.runCommand(self.command)


def install():
    for kind in ('Line', 'Point'):
        Gui.addCommand('FreeCADPlus_Datum' + kind, DatumCommand(kind))
    for title, command in (('Extrude', 'PartDesign_Pad'), ('Revolve', 'PartDesign_Revolution')):
        Gui.addCommand('FreeCADPlus_' + title, ModelingCommand(title, command))
