# SPDX-License-Identifier: LGPL-2.1-or-later
"""History Appearance actions preserve prior picks or target an exact feature."""
import FreeCADGui as Gui
from PySide6 import QtWidgets,QtGui

def history_menu(widget,tree,point,row):
    from . import appearance,appearance_task,panel
    doc,obj=widget._checked(row);owner=widget._context(*widget._binding)[0]
    initial=getattr(widget,'_appearance_selection',None)
    widget._appearance_selection=None
    if initial is None:initial=appearance_task.selection_snapshot()
    header=row.kind=='history_component'
    if header:owner=obj
    else:
        if owner is None or obj not in appearance.results(owner, include_history=True):return
        initial=((panel.identity(obj),''),)
    menu=QtWidgets.QMenu(widget);choices=[]
    if header:
        action=menu.addAction('Rename');action.triggered.connect(lambda:choices.append('rename'))
        menu.addSeparator()
    action=menu.addAction(QtGui.QIcon(':/icons/Std_SetAppearance.svg'),'Appearance\u2026')
    action.setEnabled(bool(appearance.results(owner, include_history=True)) if header else True)
    action.triggered.connect(lambda:choices.append('appearance'))
    binding=widget._binding
    menu.exec_(tree.viewport().mapToGlobal(point))
    try:
        if choices:
            if widget._current()!=binding:raise ValueError('The active file changed; reopen the menu')
            widget._checked(row)
            if choices[-1]=='rename':widget.rename_row(row)
            else:
                if not header:
                    Gui.Selection.clearSelection()
                    Gui.Selection.addSelection(*(row.selection or (obj.Document.Name,obj.Name,'')))
                appearance_task.open_task(owner,initial)
    except (ValueError,RuntimeError,ReferenceError) as error:widget._message(str(error))
    menu.deleteLater()
