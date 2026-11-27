# SPDX-License-Identifier: LGPL-2.1-or-later
"""Assembly presentation controls and identity-preserving group actions."""
import FreeCAD as App, FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets


def configure(panel, page, tree):
    panel._assembly_empty=None
    tree.setColumnCount(2);tree.header().setStretchLastSection(False)
    tree.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
    tree.header().setSectionResizeMode(1,QtWidgets.QHeaderView.Fixed);tree.setColumnWidth(1,112)
    tree.setTextElideMode(QtCore.Qt.ElideRight)


def set_all(panel, condensed):
    state(panel).clear();state(panel)[None]=condensed
    App.ParamGet('User parameter:BaseApp/Preferences/Mod/FreeCADPlus').SetBool('CondensedInstances',condensed)
    panel.refresh();panel._sync_selection(reveal=True)


def set_group(panel, key, condensed):
    state(panel)[key]=condensed;panel.refresh()
    item=panel._maps[1].get(('instance_group',*key))
    if condensed and item and not any(item.child(i).isSelected() for i in range(item.childCount())):item.setExpanded(False)


def attach(panel, tree):
    empty=panel._assembly_empty
    if empty is not None:
        index=tree.indexOfTopLevelItem(empty)
        if index>=0:tree.takeTopLevelItem(index)
        panel._assembly_empty=None
    root=tree.topLevelItem(0)
    if root is None:
        root=QtWidgets.QTreeWidgetItem(tree,['Choose active assembly',''])
        root.setFlags(QtCore.Qt.ItemIsEnabled);panel._assembly_empty=root
    root.setToolTip(0,root.text(0))
    existing=tree.itemWidget(root,1)
    if existing is not None:
        for control in existing.findChildren(QtWidgets.QToolButton):control.setEnabled(panel._binding is not None)
        panel.assembly_button.setText('Active assembly: '+root.text(0)+'...')
        return
    host=QtWidgets.QWidget(tree);row=QtWidgets.QHBoxLayout(host);row.setContentsMargins(0,0,0,0);row.setSpacing(1)
    def button(name,icon,callback):
        item=QtWidgets.QToolButton();item.setObjectName(name.replace(' ',''));item.setIcon(icon)
        item.setToolTip(name);item.setAccessibleName(name);item.setAutoRaise(True);item.setFixedSize(26,26)
        item.clicked.connect(callback);row.addWidget(item);return item
    style=tree.style()
    panel.expand_all=button('Expand all instances',style.standardIcon(QtWidgets.QStyle.SP_ArrowDown),lambda:set_all(panel,False))
    panel.condense_all=button('Condense all instances',style.standardIcon(QtWidgets.QStyle.SP_ArrowRight),lambda:set_all(panel,True))
    panel.assembly_button=button('Choose active assembly',Gui.getIcon('Assembly_ActivateAssembly'),panel.choose_assembly)
    panel.move_button=button('Move Components',Gui.getIcon('Std_TransformManip'),panel.move_selected)
    for control in host.findChildren(QtWidgets.QToolButton):control.setEnabled(panel._binding is not None)
    panel.assembly_button.setText('Active assembly: '+root.text(0)+'...' if panel._maps[1] else 'Choose active assembly...')
    tree.setItemWidget(root,1,host)


def group_key(item):
    from .panel import _ROLE
    row=item.data(0,_ROLE)
    if row.kind=='instance_group':return (row.key[1],row.ref),True
    parent=item.parent();pr=parent.data(0,_ROLE) if parent else None
    if pr and pr.kind=='instance_group':return (pr.key[1],row.ref),True
    siblings=parent or item.treeWidget().invisibleRootItem()
    matches=[siblings.child(i) for i in range(siblings.childCount())
             if siblings.child(i).data(0,_ROLE) and siblings.child(i).data(0,_ROLE).kind=='occurrence'
             and siblings.child(i).data(0,_ROLE).ref==row.ref]
    if len(matches)<2:return None,False
    return ((pr.key if pr else ()),row.ref),False


def add_group_action(panel,item,menu,actions):
    key,condensed=group_key(item)
    if key is None:return
    menu.addSeparator();action=menu.addAction('Expand instances' if condensed else 'Condense instances')
    actions[action]=lambda unused:set_group(panel,key,not condensed)



def state(panel):
    binding=panel._current()
    if binding is None:return {None:False}
    prefs=App.ParamGet('User parameter:BaseApp/Preferences/Mod/FreeCADPlus')
    return panel._state(binding).setdefault('instance_groups',{None:prefs.GetBool('CondensedInstances',False)})


def members(rows):
    result={}
    for row in rows:
        for child in row.children if row.kind=='instance_group' else (row,):
            result[child.key]=child
    return tuple(result.values())


def choose_member(panel, row, callback):
    from .panel import _ROLE
    item=panel._maps[1].get(row.key)
    if item is None or item.data(0,_ROLE).children!=row.children:
        raise ValueError('The group changed; reopen its menu')
    labels=[child.label for child in row.children]
    name,ok=QtWidgets.QInputDialog.getItem(panel,'Choose instance','Instance',labels,0,False)
    if ok:callback(row.children[labels.index(name)])


def group_display(panel, group, *, part_type=None, shown=None):
    from . import display, document
    from .panel import _ROLE
    panel._clipboard_guard()
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first')
    item=panel._maps[1].get(group.key)
    if item is None or item.data(0,_ROLE).children!=group.children:
        raise ValueError('The group changed; reopen its menu')
    prepared=[display.prepare_state(*panel._display_target(row),part_type=part_type,shown=shown)
              for row in group.children]
    docs={root.Document for root,obj,value in prepared}
    if len(docs)!=1:raise ValueError('The group no longer belongs to one parent file')
    with document.transaction(next(iter(docs)),'Change grouped instance display'):
        for root,obj,value in prepared:display.enable(root);display.write_state(obj,value)
    panel.refresh()
