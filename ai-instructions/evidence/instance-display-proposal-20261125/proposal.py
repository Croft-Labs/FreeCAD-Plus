# UI-only preview helper. Native link/tree actions are intentionally not wired.
def preview_instance_layout(dock):
    tree = dock.trees[1]
    tree.itemSelectionChanged.disconnect()
    tree.itemDoubleClicked.disconnect()
    tree.customContextMenuRequested.disconnect()
    dock._timer.stop()
    dock._timer.timeout.disconnect()
    def snapshot(item):
        return (item.data(0, _ROLE), item.icon(0), item.text(0),
                [snapshot(item.child(i)) for i in range(item.childCount())], item.icon(1),
                item.font(0), item.background(0), item.foreground(0), item.flags(),
                item.data(0, QtCore.Qt.CheckStateRole), item.isSelected())
    originals = [snapshot(tree.topLevelItem(i)) for i in range(tree.topLevelItemCount())]
    host = QtWidgets.QWidget()
    bar = QtWidgets.QHBoxLayout(host); bar.setContentsMargins(2, 0, 2, 0)
    bar.addWidget(QtWidgets.QLabel('Instances'))
    choice = QtWidgets.QComboBox(); choice.addItems(('Expanded', 'Condensed'))
    bar.addWidget(choice); bar.addStretch()
    dock.tabs.widget(1).layout().insertWidget(1, host)
    def fill():
        blocker = QtCore.QSignalBlocker(tree)
        tree.clear()
        def children(source, parent):
            siblings = source[3]
            repeated = {}
            for item in siblings:
                row = item[0]
                if row and row.kind == 'occurrence': repeated.setdefault(row.ref, []).append(item)
            emitted = set()
            for item in siblings:
                row = item[0]
                members = repeated.get(row.ref, []) if row and row.kind == 'occurrence' else []
                if len(members) > 1:
                    number = members.index(item) + 1
                    if choice.currentText() == 'Condensed':
                        if row.ref in emitted: continue
                        emitted.add(row.ref)
                        group = QtWidgets.QTreeWidgetItem(parent)
                        group.setText(0, row.label + ' \u00d7' + str(len(members)))
                        group.setIcon(0, item[1])
                        group.setToolTip(0, 'Expand to choose an individual instance')
                        group.setData(0, _ROLE, replace(row, kind='instance_group', path=(), selection=(), children=()))
                        for i, member in enumerate(members, 1): copy_item(member, group, member[0].label + ' (' + str(i) + ')')
                        group.setExpanded(False)
                        continue
                    copy_item(item, parent, row.label + ' (' + str(number) + ')')
                else: copy_item(item, parent)
        def copy_item(source, parent, label=None):
            item = QtWidgets.QTreeWidgetItem()
            item.setData(0, _ROLE, source[0]); item.setIcon(0, source[1]); item.setText(0, source[2])
            item.setIcon(1, source[4])
            item.setFont(0, source[5]); item.setBackground(0, source[6]); item.setForeground(0, source[7])
            item.setFlags(source[8]); item.setData(0, QtCore.Qt.CheckStateRole, source[9])
            if label is not None: item.setText(0, label)
            parent.addChild(item) if isinstance(parent, QtWidgets.QTreeWidgetItem) else parent.addTopLevelItem(item)
            item.setSelected(source[10])
            children(source, item)
            row = item.data(0, _ROLE)
            item.setExpanded(bool(row and row.kind != 'constraints'))
            return item
        for root in originals: copy_item(root, tree)
        del blocker
    choice.currentIndexChanged.connect(fill); fill()
    return choice
