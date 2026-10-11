# SPDX-License-Identifier: LGPL-2.1-or-later
"""Independent presentation choices over the same component/operation backend.

Toolbar and task presentations initially share their unchanged native definitions.
Their saved choices are independent; future Plus adapters must reuse the same commands.
"""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from . import panel

KEYS = ('ModelPanelUIMode', 'ToolbarUIMode', 'TaskPanelUIMode')
_installed = False
_model_mode = None
_property_dock = None
_timer = None


def modes():
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
    return tuple('Classic' if prefs.GetInt(key, 0) == 1 else 'Plus' for key in KEYS)


def apply_modes():
    """Change presentation only; keep document identity, Edit and tasks intact."""
    global _model_mode, _property_dock
    window = Gui.getMainWindow()
    model, toolbar, task = modes()
    changed = model != _model_mode
    # These two presentations intentionally start from the same native definition.
    # Do not duplicate QAction callbacks, task dialogs or feature implementations.
    window.setProperty('ToolbarUIMode', toolbar)
    window.setProperty('TaskPanelUIMode', task)
    window.setProperty('ModelPanelUIMode', model)
    dock = panel._panel
    if dock is None or dock._closed:
        dock = panel.show_panel()
        dock._ui_mode_managed = True
        changed = True
    dock.toggleViewAction().setVisible(model == 'Plus')
    if model == 'Classic':
        dock.hide()  # Backend observers and component Edit contexts remain alive.
    elif changed:
        dock.show()
        dock.raise_()
    properties = None
    dock_prefs = App.ParamGet('User parameter:BaseApp/Preferences/DockWindows')
    # Keep the native property editor: only replace the Model tree presentation.
    for native in window.findChildren(QtWidgets.QDockWidget):
        if native.objectName() == 'Model':
            content = native.widget()
            for tree in content.findChildren(QtWidgets.QWidget):
                if tree.metaObject().className() == 'Gui::TreePanel':
                    tree.setVisible(model == 'Classic')
            native.setWindowTitle('Model' if model == 'Classic' else 'Properties')
            if dock_prefs.GetGroup('ComboView').GetBool('Enabled', True):
                properties = native
        elif native.objectName() == 'Property view':
            if dock_prefs.GetGroup('PropertyView').GetBool('Enabled', False):
                properties = native
        elif native.objectName() == 'Tree view':
            # Also respect FreeCAD's existing independent tree/property layout.
            enabled = App.ParamGet('User parameter:BaseApp/Preferences/DockWindows/TreeView').GetBool('Enabled', False)
            native.toggleViewAction().setVisible(enabled and model == 'Classic')
            if model == 'Plus':
                native.hide()
            elif changed and enabled:
                native.show()
    if model == 'Plus' and properties is not None:
        if changed or properties is not _property_dock:
            # Establish the owner layout on startup/mode or native-layout changes.
            # Ordinary workbench refreshes must not reset the user's dock sizing.
            dock.setFloating(False)
            properties.setFloating(False)
            window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
            window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties)
            window.splitDockWidget(dock, properties, QtCore.Qt.Vertical)
            properties.show()
    _property_dock = properties
    _model_mode = model


def schedule(*args):
    if _timer is not None:
        _timer.start(0)


def install():
    global _installed, _timer
    if _installed:
        return
    _installed = True
    window = Gui.getMainWindow()
    _timer = QtCore.QTimer(window)
    _timer.setSingleShot(True)
    _timer.timeout.connect(apply_modes)
    # Workbench activation resets dock menu actions; restore the selected presentation.
    window.workbenchActivated.connect(schedule)
    schedule()
