# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bounded, read-only inspection of the native property dependency graph."""
from collections import deque

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets


def _tr(text):
    return App.Qt.translate("DependencyInspector", text)


def identity(obj):
    return (obj.Document.Name, obj.Name, obj.ID)


def resolve(key):
    doc = App.listDocuments().get(key[0])
    obj = doc.getObject(key[1]) if doc else None
    if obj is None or obj.ID != key[2]:
        raise ValueError(_tr("The object is no longer available. Select another feature."))
    return obj


def describe(obj):
    return {"key": identity(obj), "label": obj.Label, "type": obj.TypeId,
            "state": ", ".join(obj.State), "status": obj.getStatusString(),
            "file": obj.Document.FileName or _tr("Unsaved document")}


def _has_cycle(adjacency):
    """Kahn's traversal also handles shared inputs without mistaking them for cycles."""
    degrees = {node: 0 for node in adjacency}
    for targets in adjacency.values():
        for target in targets:
            degrees[target] = degrees.get(target, 0) + 1
    pending = deque(node for node, degree in degrees.items() if not degree)
    count = 0
    while pending:
        node = pending.popleft()
        count += 1
        for target in adjacency.get(node, ()):
            degrees[target] -= 1
            if not degrees[target]:
                pending.append(target)
    return count != len(degrees)


def inspect_graph(root, direction, transitive=True, max_edges=500, max_depth=8):
    """Snapshot property edges, including native expressions and loaded external links.

    Every row is one native edge. Depth is its path length from the inspected root;
    each reached object is expanded once. No recompute, geometry access or mutation.
    Container links are included and are not interpreted as geometric target roles.
    """
    if direction not in ("inputs", "consumers") or max_edges < 1 or max_depth < 1:
        raise ValueError("Invalid dependency inspection options")
    start = identity(root)
    pending = deque([(root, 0, (root.Name,))])
    visited = {start}
    adjacency = {}
    rows = []
    truncated = False
    while pending:
        obj, depth, path = pending.popleft()
        edges = obj.OutListProp if direction == "inputs" else obj.InListProp
        if depth >= max_depth:
            truncated = truncated or bool(edges)
            continue
        for edge in edges:
            if len(rows) >= max_edges:
                truncated = True
                pending.clear()
                break
            target = edge.ToObj if direction == "inputs" else edge.FromObj
            key = identity(target)
            adjacency.setdefault(identity(obj), set()).add(key)
            reason = (edge.FromObj.Name + "." + (edge.FromProp or "(object)") + " -> " +
                      edge.ToObj.Name + ("." + edge.ToProp if edge.ToProp else ""))
            row = describe(target)
            row.update(depth=depth + 1, reason=reason, path=path + (target.Name,),
                       external=target.Document != root.Document)
            rows.append(row)
            if transitive and key not in visited:
                visited.add(key)
                pending.append((target, depth + 1, row["path"]))
    return {"rows": rows, "cycle": _has_cycle(adjacency), "truncated": truncated}


def selected_object():
    objects = Gui.Selection.getSelection()
    if len(objects) != 1:
        raise ValueError(_tr("Select exactly one feature or object."))
    return objects[0]


class InspectorDialog(QtWidgets.QDialog):
    def __init__(self, obj, parent=None):
        super().__init__(parent)
        self.root = identity(obj)
        self._closed = False
        self._fresh = False
        self.setWindowTitle(_tr("Inspect dependencies"))
        self.resize(1040, 620)
        layout = QtWidgets.QVBoxLayout(self)
        self.heading = QtWidgets.QLabel()
        self.heading.setTextFormat(QtCore.Qt.PlainText)
        self.heading.setWordWrap(True)
        layout.addWidget(self.heading)
        controls = QtWidgets.QHBoxLayout()
        self.useSelection = QtWidgets.QPushButton(_tr("Inspect selected object"))
        self.refreshButton = QtWidgets.QPushButton(_tr("Refresh"))
        self.transitive = QtWidgets.QCheckBox(_tr("Include transitive dependencies"))
        self.transitive.setChecked(True)
        for widget in (self.useSelection, self.refreshButton, self.transitive):
            controls.addWidget(widget)
        layout.addLayout(controls)
        note = QtWidgets.QLabel(_tr(
            "Native property links, including expressions and container membership. "
            "These are dependencies, not a deletion plan. Only loaded objects are inspected; "
            "unresolved references are reported through native object status. No automatic recompute."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.tabs = QtWidgets.QTabWidget()
        self.tables = []
        for title in (_tr("Inputs / upstream"), _tr("Consumers / downstream")):
            tree = QtWidgets.QTreeWidget()
            tree.setHeaderLabels([_tr("Feature"), _tr("Relationship"), _tr("Native link"),
                                  _tr("State"), _tr("Document")])
            tree.setRootIsDecorated(False)
            tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            tree.itemSelectionChanged.connect(self.showDetails)
            self.tables.append(tree)
            self.tabs.addTab(tree, title)
        self.tabs.currentChanged.connect(self.showDetails)
        layout.addWidget(self.tabs)
        self.details = QtWidgets.QLabel()
        self.details.setWordWrap(True)
        self.details.setTextFormat(QtCore.Qt.PlainText)
        self.details.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        layout.addWidget(self.details)
        self.message = QtWidgets.QLabel()
        self.message.setWordWrap(True)
        self.message.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.message)
        actions = QtWidgets.QHBoxLayout()
        self.selectButton = QtWidgets.QPushButton(_tr("Select in model"))
        self.inspectButton = QtWidgets.QPushButton(_tr("Inspect this row"))
        close = QtWidgets.QPushButton(_tr("Close"))
        for button in (self.selectButton, self.inspectButton, close):
            actions.addWidget(button)
        layout.addLayout(actions)
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setAutoDefault(False)
        self.useSelection.clicked.connect(self.inspectSelection)
        self.refreshButton.clicked.connect(self.refresh)
        self.transitive.toggled.connect(self.refresh)
        self.selectButton.clicked.connect(self.selectRow)
        self.inspectButton.clicked.connect(self.inspectRow)
        close.clicked.connect(self.reject)
        self.refresh()
        App.addDocumentObserver(self)

    def invalidate(self, *args):
        self._fresh = False
        for table in self.tables:
            table.clear()
        self.showDetails()
        self.message.setText(_tr("The document graph changed. Refresh to inspect current dependencies."))

    def refresh(self, *args):
        self.invalidate()
        try:
            root = resolve(self.root)
            info = describe(root)
            self.heading.setText(root.Label + " [" + root.Document.Name + "#" + root.Name + "]\n" +
                                 info["type"] + " | " + info["state"] + " | " + info["status"])
            graphs = [inspect_graph(root, direction, self.transitive.isChecked())
                      for direction in ("inputs", "consumers")]
            notes = []
            for table, graph in zip(self.tables, graphs):
                for row in graph["rows"]:
                    relation = _tr("Direct") if row["depth"] == 1 else _tr("Transitive") + " ({})".format(row["depth"])
                    if row["external"]:
                        relation += " / " + _tr("External")
                    item = QtWidgets.QTreeWidgetItem([row["label"] + " [" + row["key"][1] + "]",
                                                     relation, row["reason"], row["state"], row["key"][0]])
                    item.setData(0, QtCore.Qt.UserRole, row)
                    table.addTopLevelItem(item)
                for column in range(5):
                    table.resizeColumnToContents(column)
                if graph["cycle"]:
                    notes.append(_tr("A cycle is present in the displayed native graph."))
                if graph["truncated"]:
                    notes.append(_tr("Partial view: limit of 500 links or 8 levels reached. Inspect a row to continue."))
            self._fresh = True
            self.message.setText(" ".join(dict.fromkeys(notes)) or
                                 _tr("Current snapshot. Empty tables mean no links in this direction. Select a row for details."))
            self.showDetails()
        except Exception as error:
            self.message.setText(str(error))

    def currentRow(self):
        item = self.tables[self.tabs.currentIndex()].currentItem()
        return item.data(0, QtCore.Qt.UserRole) if item and self._fresh else None

    def showDetails(self, *args):
        row = self.currentRow()
        self.selectButton.setEnabled(row is not None)
        self.inspectButton.setEnabled(row is not None)
        self.details.setText((row["type"] + " | " + row["status"] + "\n" +
                              _tr("Path: ") + " -> ".join(row["path"]) + "\n" +
                              _tr("Source: ") + row["file"]) if row else "")

    def context(self):
        if Gui.Control.activeDialog():
            raise ValueError(_tr("Finish or cancel the active task before changing selection."))

    def inspectSelection(self):
        try:
            self.context()
            self.root = identity(selected_object())
            self.refresh()
        except Exception as error:
            self.message.setText(str(error))

    def rowObject(self):
        self.context()
        row = self.currentRow()
        if row is None:
            raise ValueError(_tr("Refresh and select a dependency row."))
        return resolve(row["key"])

    def selectRow(self):
        try:
            obj = self.rowObject()
            App.setActiveDocument(obj.Document.Name)
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
            self.message.setText(_tr("Selected in the model. Visibility is unchanged; hidden objects remain hidden."))
        except Exception as error:
            self.message.setText(str(error))

    def inspectRow(self):
        try:
            self.root = identity(self.rowObject())
            self.refresh()
        except Exception as error:
            self.message.setText(str(error))

    def slotChangedObject(self, obj, prop):
        self.invalidate()

    def slotCreatedObject(self, obj):
        self.invalidate()

    def slotRecomputedDocument(self, doc):
        self.invalidate()

    def slotDeletedObject(self, obj):
        if identity(obj) == self.root:
            self.reject()
        else:
            self.invalidate()

    def slotDeletedDocument(self, doc):
        if doc.Name == self.root[0]:
            self.reject()
        else:
            self.invalidate()

    def done(self, result):
        if not self._closed:
            self._closed = True
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class CommandInspectDependencies:
    def GetResources(self):
        return {"MenuText": _tr("Inspect dependencies..."),
                "ToolTip": _tr("Inspect a feature's native inputs, consumers and reference status")}

    def IsActive(self):
        return not Gui.Control.activeDialog() and len(Gui.Selection.getSelection()) == 1

    def Activated(self):
        dialog = InspectorDialog(selected_object(), Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Std_InspectDependencies", CommandInspectDependencies())
