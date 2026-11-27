# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit active-collector capabilities shared by selection controls and picks."""
import sys
import FreeCADGui as Gui
from PySide6 import QtWidgets


def current():
    for module in ('appearance_task', 'clone_task', 'extrude_task'):
        loaded = sys.modules.get('freecad_plus.' + module)
        task = getattr(loaded, '_active', None)
        if task is None or task.closed:
            continue
        token = (task, getattr(task, 'selection_epoch', 0))
        if module == 'appearance_task':
            face = task.collecting and task.form.mode == 'face'
            return ('surface' if face else 'curve', token + (task.form.mode, task.collecting))
        if module == 'clone_task':
            face = task.extract and task.collecting
            return ('surface' if face else 'curve', token + (task.extract, task.collecting))
        # Task classes declare collector capabilities, independently of labels.
        if task.pick in getattr(task, 'face_collectors', ()):
            return 'surface', token + (task.pick,)
        return 'curve', token + (getattr(task, 'pick', None),)
    for widget in Gui.getMainWindow().findChildren(QtWidgets.QListWidget):
        if widget.isVisible() and widget.property('FreeCADPlusPickDomain') == 'surface':
            return 'surface', (widget,)
    return 'curve', ()


def changed():
    """Immediately invalidate queued picks when a collector changes or resets."""
    from . import selection_toolbar
    if selection_toolbar._watcher is not None:
        selection_toolbar._watcher.refresh()
