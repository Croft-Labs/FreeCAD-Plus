# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Structure and Model History views over the shared component model."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui import ComponentSelection as Selection

_dock = None


def tr(text):
    return App.Qt.translate("ComponentNavigator", text)


def model():
    import ComponentModel
    return ComponentModel


def object_key(obj):
    return obj.Document.Name, obj.Name


def resolve(key):
    doc = App.listDocuments().get(key[0])
    return doc.getObject(key[1]) if doc else None


def visible_paths(root, component, ids, prefix=""):
    """Resolve representation to native sub-object paths, never change sources."""
    mode = model().representation(root, ids)
    if mode == "Hidden":
        return []
    paths = []
    results = {o.Name for o in model().finished_results(component)}
    for obj in component.Group:
        if not hasattr(obj, "Shape") or not obj.Visibility or model().history_state(obj) in ("Suppressed", "Inactive \u2014 dependency"):
            continue
        if getattr(obj, "ComponentRole", "") in ("Occurrence", "Internal"):
            continue
        if mode == "Bodies Only" and obj.Name not in results:
            continue
        paths.append(prefix + obj.Name + ".")
    for child in model().children(component):
        if child.LinkedObject and child.Visibility:
            paths.extend(visible_paths(root, child.LinkedObject, ids + [child.ObjectId],
                                       prefix + child.Name + "."))
    return paths


def apply_representation(root):
    for child in model().children(root):
        if child.LinkedObject:
            paths = visible_paths(root, child.LinkedObject, [child.ObjectId])
            # Native LinkView preserves source view providers and occurrence pick
            # paths. Restrict its representation without changing source visibility,
            # suppression, native engineering geometry, or BOM/mass participation.
            child.ViewObject.LinkView.setType(-2, False)
            child.ViewObject.LinkView.setLink(child.LinkedObject if paths else None, paths)


class Navigator(QtWidgets.QDockWidget):
    def __init__(self):
        super().__init__(tr("Components"), Gui.getMainWindow())
        self.setObjectName("ComponentNavigator")
        self.root_key = None
        self.active_key = None
        self.active_path = []
        self.expanded_instances = set()
        self.refreshing = False
        self.selecting = False
        self.component_views = []
        self.tabs = QtWidgets.QTabWidget()
        self.structure = QtWidgets.QTreeWidget()
        self.structure.setHeaderLabels([tr("Part name"), tr("View"), tr("Instances"), tr("Part View")])
        self.history = QtWidgets.QTreeWidget()
        self.history.setHeaderLabels([tr("Active"), tr("View"), tr("Item"), tr("State")])
        for tree in (self.structure, self.history):
            tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            for column in range(3):
                tree.header().setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            tree.header().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.history.setRootIsDecorated(False)
        self.tabs.addTab(self.structure, tr("Component Structure"))
        self.tabs.addTab(self.history, tr("Model History"))
        self.context = QtWidgets.QLabel()
        self.context.setWordWrap(True)
        self.context.setTextFormat(QtCore.Qt.PlainText)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(self.context)
        self.conversion = QtWidgets.QPushButton(tr("Review legacy conversion"))
        self.conversion.clicked.connect(lambda: self.run(self.show_conversion_report))
        self.conversion.hide()
        layout.addWidget(self.conversion)
        layout.addWidget(self.tabs)
        self.setWidget(widget)
        self.structure.itemSelectionChanged.connect(self.select_structure)
        self.history.itemSelectionChanged.connect(self.select_history)
        self.structure.itemDoubleClicked.connect(lambda item, column: self.run(lambda: self.activate_item(item)) if column == 0 else None)
        self.structure.itemClicked.connect(lambda item, column: self.run(lambda: self.toggle_component(item)) if column == 1 else None)
        self.history.itemDoubleClicked.connect(lambda item, column: self.run(
            lambda: self.edit_history(item.data(0, QtCore.Qt.UserRole))) if column == 2 else None)
        self.history.itemClicked.connect(lambda item, column: self.run(lambda: self.toggle_item_view(item)) if column == 1 else None)
        self.history.itemChanged.connect(self.history_checked)
        for tree in (self.structure, self.history):
            tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            tree.customContextMenuRequested.connect(lambda point, tree=tree: self.menu(tree, point))
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.refresh)
        self.selection_timer = QtCore.QTimer(self)
        self.selection_timer.setSingleShot(True)
        self.selection_timer.timeout.connect(self.sync_selection)
        self.mdi = Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        if self.mdi:
            self.mdi.subWindowActivated.connect(self.view_activated)
        App.addDocumentObserver(self)
        Gui.addDocumentObserver(self)
        Gui.Selection.addObserver(self, 0)
        self.destroyed.connect(lambda: App.removeDocumentObserver(self))
        self.destroyed.connect(lambda: Gui.removeDocumentObserver(self))
        self.destroyed.connect(lambda: Gui.Selection.removeObserver(self))

    def run(self, callback):
        try:
            callback()
            self.refresh()
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self, tr("Component operation"), str(exc))

    def set_document(self, doc):
        root = model().metadata(doc).RootComponent
        self.root_key = object_key(root)
        self.active_key = self.root_key
        self.active_path = []
        Gui.getDocument(doc.Name).activeView().setActiveObject("part", root)
        if self.mdi and self.mdi.activeSubWindow():
            self.mdi.activeSubWindow().setProperty("ComponentKey", self.root_key)
            self.store_edit_context(self.mdi.activeSubWindow())
        self.refresh()

    def refresh(self):
        if self.refreshing:
            return
        self.refreshing = True
        structure_state = self.tree_state(self.structure)
        history_state = self.tree_state(self.history)
        try:
            self.structure.clear()
            self.history.clear()
            root = resolve(self.root_key) if self.root_key else None
            active = resolve(self.active_key) if self.active_key else None
            if root is None or active is None:
                self.context.setText(tr("Create or open a component document."))
                self.conversion.hide()
                return
            self.conversion.setVisible(bool(model().metadata(active.Document).LegacySource))
            self.context.setText(tr("Editing: {0}").format(active.Label))
            apply_representation(root)
            for entry in list(self.component_views):
                component = resolve(entry["key"])
                if component:
                    paths = visible_paths(component, component, [])
                    entry["snapshot"].setLink(component if paths else None, paths)
            # The root is the component itself, not the document/file wrapper.
            root_item = QtWidgets.QTreeWidgetItem(self.structure, [root.Label, "", "", ""])
            root_item.setData(0, QtCore.Qt.UserRole, (object_key(root), []))
            root_item.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
            self.decorate_component(root_item, root, [])
            self.populate(root_item, root, root, [], set())
            root_item.setExpanded(True)
            if not structure_state[0]:
                self.structure.expandToDepth(1)
            for obj in model().history(active):
                status = tr(model().history_state(obj))
                item = QtWidgets.QTreeWidgetItem(self.history, ["", "", obj.Label, status])
                item.setData(0, QtCore.Qt.UserRole, object_key(obj))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                inactive = status == tr("Inactive \u2014 dependency")
                state = QtCore.Qt.Unchecked if getattr(obj, "UserSuppressed", False) else (QtCore.Qt.PartiallyChecked if inactive else QtCore.Qt.Checked)
                item.setCheckState(0, state)
                item.setToolTip(0, tr("Unchecked: suppressed. Partially checked: an input is inactive."))
                unavailable = inactive or bool(getattr(obj, "UserSuppressed", False))
                self.visibility_icon(item, bool(obj.Visibility) and not unavailable, 1)
                if unavailable:
                    item.setToolTip(1, tr("Geometry is unavailable while this item or an input is suppressed."))
                if obj.ViewObject:
                    item.setIcon(2, obj.ViewObject.Icon)
                item.setToolTip(2, tr("Operation") if obj.ComponentRole == "Operation" else tr("Object"))
            self.restore_tree(self.structure, structure_state)
            iterator = QtWidgets.QTreeWidgetItemIterator(self.structure)
            while iterator.value():
                row = iterator.value()
                if row.data(0, QtCore.Qt.UserRole + 2) in self.expanded_instances:
                    row.setExpanded(True)
                iterator += 1
            self.restore_tree(self.history, history_state)
        finally:
            self.refreshing = False

    @staticmethod
    def row_key(item):
        def freeze(value):
            return tuple(freeze(v) for v in value) if isinstance(value, (list, tuple)) else value
        return freeze(item.data(0, QtCore.Qt.UserRole))

    def tree_state(self, tree):
        rows = {}
        iterator = QtWidgets.QTreeWidgetItemIterator(tree)
        while iterator.value():
            item = iterator.value()
            key = self.row_key(item)
            if key is not None:
                rows[key] = item.isExpanded(), item.isSelected(), item.childCount() > 0
            iterator += 1
        return rows, tree.verticalScrollBar().value()

    def restore_tree(self, tree, state):
        rows, scroll = state
        iterator = QtWidgets.QTreeWidgetItemIterator(tree)
        while iterator.value():
            item = iterator.value()
            saved = rows.get(self.row_key(item))
            if saved:
                if saved[2]:
                    item.setExpanded(saved[0])
                item.setSelected(saved[1])
            iterator += 1
        tree.verticalScrollBar().setValue(scroll)

    @staticmethod
    def visibility_icon(item, visible, column=1):
        item.setIcon(column, Gui.getIcon("TreeItemVisible.svg" if visible else "TreeItemInvisible.svg"))
        item.setToolTip(column, tr("Hide") if visible else tr("Show"))

    def members(self, item):
        return item.data(0, QtCore.Qt.UserRole + 1) or [item.data(0, QtCore.Qt.UserRole)]

    def protected(self, item):
        # The active occurrence and its ancestors must remain visible.
        return any(value is not None and list(value[1]) == self.active_path[:len(value[1])]
                   for value in self.members(item))

    @staticmethod
    def path_visible(root, ids):
        return bool(root.Visibility) and model().representation(root, ids) != "Hidden" and all(
            link.Visibility for link in model()._path(root, ids))

    def decorate_component(self, item, definition, paths):
        root = resolve(self.root_key)
        visible = not paths or any(self.path_visible(root, ids) for ids in paths)
        self.visibility_icon(item, visible)
        if self.protected(item):
            item.setToolTip(1, tr("The active component and its parent branch cannot be hidden."))
        if definition and object_key(definition) == self.active_key:
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)
            item.setBackground(0, self.palette().brush(QtGui.QPalette.Highlight))
            item.setForeground(0, self.palette().brush(QtGui.QPalette.HighlightedText))

    def populate(self, row, component, root, path, seen):
        key = object_key(component)
        if key in seen:
            return
        seen = seen | {key}
        constraints = [o for o in component.Group if getattr(o, "ComponentRole", "") == "Constraint"]
        if constraints:
            group = QtWidgets.QTreeWidgetItem(row, [tr("Assembly Constraints")])
            for constraint in constraints:
                QtWidgets.QTreeWidgetItem(group, [constraint.Label])
        groups = {}
        for link in model().children(component):
            definition = link.LinkedObject
            group_key = object_key(definition) if definition else object_key(link)
            groups.setdefault(group_key, []).append(link)
        for definition_key, links in groups.items():
            definition = links[0].LinkedObject
            values = [(object_key(link), path + [link.ObjectId]) for link in links]
            modes = {model().representation(root, value[1]) for value in values} if definition else {tr("Missing component")}
            title = definition.Label if definition else links[0].Label
            item = QtWidgets.QTreeWidgetItem(row, [title, "", "x" + str(len(links)), modes.pop() if len(modes) == 1 else tr("Mixed")])
            item.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
            item.setData(0, QtCore.Qt.UserRole, values[0])
            item.setData(0, QtCore.Qt.UserRole + 1, values)
            group_id = (self.root_key, tuple(path), definition_key)
            item.setData(0, QtCore.Qt.UserRole + 2, group_id)
            self.decorate_component(item, definition, [value[1] for value in values])
            if len(links) > 1:
                if group_id in self.expanded_instances:
                    for index, (link, value) in enumerate(zip(links, values), 1):
                        number = getattr(link, "InstanceNumber", index)
                        name = "_".join(title.split()) + "#" + str(number).zfill(3)
                        instance = QtWidgets.QTreeWidgetItem(item, [name, "", "", model().representation(root, value[1])])
                        instance.setData(0, QtCore.Qt.UserRole, value)
                        instance.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
                        self.decorate_component(instance, definition, [value[1]])
                        if definition:
                            self.populate(instance, definition, root, value[1], seen)
                    item.setExpanded(True)
            elif definition:
                self.populate(item, definition, root, values[0][1], seen)

    def toggle_instances(self, item):
        group_id = item.data(0, QtCore.Qt.UserRole + 2)
        if group_id in self.expanded_instances:
            self.expanded_instances.remove(group_id)
        else:
            self.expanded_instances.add(group_id)
        item.setExpanded(group_id in self.expanded_instances)

    def change_part_view(self, updates, show=False):
        root = resolve(self.root_key)
        overrides = model().representation_overrides(root, updates)
        if model().representation(root, self.active_path, root_overrides=overrides) == "Hidden":
            raise ValueError(tr("The active component cannot be hidden. Edit another component first."))
        model().set_representations(root, updates, show=show)

    def set_part_view(self, item, setting):
        updates = [(ids, setting) for key, ids in self.members(item) if ids]
        if not updates:
            raise ValueError(tr("The root component is displayed in full."))
        self.change_part_view(updates)

    def toggle_component(self, item):
        if not item.data(0, QtCore.Qt.UserRole):
            return
        root = resolve(self.root_key)
        members = self.members(item)
        visible = any(self.path_visible(root, ids) for key, ids in members)
        if visible:
            self.set_part_view(item, "Hidden")
            return
        updates = [(ids, None) for key, ids in members if ids]
        overrides = model().representation_overrides(root, updates)
        updates = [(ids, "Bodies Only" if model().representation(root, ids, root_overrides=overrides) == "Hidden"
                    else None) for ids, unused in updates]
        self.change_part_view(updates, show=True)

    def toggle_item_view(self, item):
        obj = resolve(item.data(0, QtCore.Qt.UserRole))
        if obj is None:
            return
        if getattr(obj, "UserSuppressed", False) or model().history_state(obj) == "Inactive \u2014 dependency":
            return
        with model().transaction(obj.Document, "Toggle item visibility"):
            obj.Visibility = not obj.Visibility

    def history_checked(self, item, column):
        if self.refreshing or column != 0:
            return
        key = item.data(0, QtCore.Qt.UserRole)
        checked = item.checkState(0) != QtCore.Qt.Unchecked
        self.run(lambda: model().set_suppressed(resolve(key), not checked))

    def select_native(self, values):
        if self.refreshing or self.selecting:
            return
        root = resolve(self.root_key) if self.root_key else None
        if root is None:
            return
        self.selecting = True
        try:
            Gui.Selection.clearSelection()
            for ids, item in values:
                Gui.Selection.addSelection(root.Document.Name, root.Name,
                                           Selection.native_path(root, ids, item))
        finally:
            self.selecting = False

    def select_structure(self):
        values = []
        for row in self.structure.selectedItems():
            for value in self.members(row):
                if value:
                    values.append((value[1], None))
        self.select_native(values)

    def select_history(self):
        self.select_native([(self.active_path, resolve(row.data(0, QtCore.Qt.UserRole)))
                            for row in self.history.selectedItems()])

    def selection_changed(self, *args):
        if not self.selecting and not self.refreshing:
            self.selection_timer.start(0)

    addSelection = selection_changed
    removeSelection = selection_changed
    clearSelection = selection_changed
    setSelection = selection_changed

    def sync_selection(self):
        root = resolve(self.root_key) if self.root_key else None
        if root is None or self.selecting or self.refreshing:
            return
        picks = Selection.selected(root, Gui.Selection.getSelectionEx("*", 0))
        self.selecting = True
        try:
            # Reveal a precise pick through grouped instances. An ambiguous bare
            # definition selection must never choose an arbitrary occurrence.
            changed = False
            if len(picks) == 1:
                prefix, component = [], root
                for link in model()._path(root, picks[0].ids):
                    peers = [child for child in model().children(component)
                             if child.LinkedObject == link.LinkedObject]
                    group = (self.root_key, tuple(prefix), object_key(link.LinkedObject))
                    if len(peers) > 1 and group not in self.expanded_instances:
                        self.expanded_instances.add(group)
                        changed = True
                    prefix.append(link.ObjectId)
                    component = link.LinkedObject
            if changed:
                self.refresh()
            self.structure.clearSelection()
            self.history.clearSelection()
            for pick in picks:
                matches = []
                iterator = QtWidgets.QTreeWidgetItemIterator(self.structure)
                while iterator.value():
                    row = iterator.value()
                    if any(value and tuple(value[1]) == pick.ids for value in self.members(row)):
                        matches.append(row)
                    iterator += 1
                if matches:
                    row = min(matches, key=lambda candidate: len(self.members(candidate)))
                    row.setSelected(True)
                    parent = row.parent()
                    while parent:
                        parent.setExpanded(True)
                        parent = parent.parent()
                    self.structure.scrollToItem(row)
                if pick.item is not None and object_key(pick.component) == self.active_key:
                    for index in range(self.history.topLevelItemCount()):
                        row = self.history.topLevelItem(index)
                        if row.data(0, QtCore.Qt.UserRole) == object_key(pick.item):
                            row.setSelected(True)
                            self.history.scrollToItem(row)
        finally:
            self.selecting = False

    def store_edit_context(self, window):
        window.setProperty("ComponentActiveKey", self.active_key)
        window.setProperty("ComponentActivePath", self.active_path)

    def activate_item(self, item):
        value = item.data(0, QtCore.Qt.UserRole)
        if not value:
            return
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before editing another component."))
        obj = resolve(value[0])
        if getattr(obj, "ComponentRole", "") == "Occurrence":
            obj = obj.LinkedObject
        if not model().is_component(obj):
            return
        parent = item.parent()
        while parent:
            parent.setExpanded(True)
            parent = parent.parent()
        root_key = self.root_key
        root = resolve(root_key)
        root.Visibility = True
        for depth in range(1, len(value[1]) + 1):
            ids = value[1][:depth]
            link = model()._path(root, ids)[-1]
            link.Visibility = True
            if model().representation(root, ids) == "Hidden":
                model().set_representation(root, ids, "Bodies Only")
        model().activate(obj)
        App.setActiveDocument(obj.Document.Name)
        self.root_key, self.active_key, self.active_path = root_key, object_key(obj), list(value[1])
        Gui.activeDocument().activeView().setActiveObject("part", obj)
        if self.mdi and self.mdi.activeSubWindow():
            self.mdi.activeSubWindow().setProperty("ComponentActiveKey", self.active_key)
            self.mdi.activeSubWindow().setProperty("ComponentActivePath", self.active_path)
        self.tabs.setCurrentWidget(self.history)

    def open_component_tab(self, key):
        obj = resolve(key)
        if getattr(obj, "ComponentRole", "") == "Occurrence":
            obj = obj.LinkedObject
        if not model().is_component(obj):
            raise ValueError(tr("Select a resolved component."))
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before opening another component view."))
        for entry in self.component_views:
            if entry["key"] == object_key(obj) and entry.get("window"):
                self.mdi.setActiveSubWindow(entry["window"])
                self.view_activated(entry["window"])
                return entry["view"]
        model().activate(obj)
        App.setActiveDocument(obj.Document.Name)
        view = Gui.getDocument(obj.Document.Name).createView("Gui::View3DInventor")
        snapshot = Gui.LinkView()
        snapshot.setType(-2, False)
        paths = visible_paths(obj, obj, [])
        snapshot.setLink(obj if paths else None, paths)
        view.getViewer().setSceneGraph(snapshot.RootNode)
        view.setActiveObject("part", obj)
        entry = {"key": object_key(obj), "view": view, "snapshot": snapshot}
        self.component_views.append(entry)
        if self.mdi and self.mdi.activeSubWindow():
            window = self.mdi.activeSubWindow()
            entry["window"] = window
            window.setProperty("ComponentKey", object_key(obj))
            window.setProperty("ComponentActiveKey", object_key(obj))
            window.setProperty("ComponentActivePath", [])
            window.setWindowTitle(obj.Label + " — " + (obj.Document.FileName or tr("Unsaved")))
            window.destroyed.connect(lambda: self.component_views.remove(entry) if entry in self.component_views else None)
        self.root_key = self.active_key = object_key(obj)
        self.active_path = []
        view.viewAxonometric()
        view.fitAll()
        return view

    def view_activated(self, window):
        if window is None:
            return
        key = window.property("ComponentKey")
        if key and resolve(key):
            self.root_key = tuple(key)
            active = window.property("ComponentActiveKey") or key
            self.active_key = tuple(active)
            self.active_path = list(window.property("ComponentActivePath") or [])
            root = resolve(self.root_key)
            try:
                chain = model()._path(root, self.active_path)
                component = chain[-1].LinkedObject if chain else root
            except ValueError:
                component, self.active_path = root, []
            self.active_key = object_key(component)
            Gui.getDocument(component.Document.Name).activeView().setActiveObject("part", component)
            self.store_edit_context(window)
            self.run(lambda: model().activate(component))
            self.selection_timer.start(0)

    def add_component(self, parent_key=None):
        active = resolve(parent_key or self.active_key)
        if getattr(active, "ComponentRole", "") == "Occurrence":
            active = active.LinkedObject
        root_key, active_key, active_path = self.root_key, self.active_key, list(self.active_path)
        choices = [d for d in model().definitions(active.Document)
                   if d != active and not model()._reachable(d, active)]
        labels = [tr("New embedded component…"), tr("Component from file…")] + [f"{d.Label} ({d.Name})" for d in choices]
        selected, ok = QtWidgets.QInputDialog.getItem(self, tr("Add Component"), tr("Component"), labels, 0, False)
        if not ok:
            return
        index = labels.index(selected)
        if index == 0:
            label, ok = QtWidgets.QInputDialog.getText(self, tr("Add Component"), tr("Name"))
            if not ok or not label.strip():
                return
            model().add_component(active, label=label.strip())
            return
        elif index == 1:
            path, unused = QtWidgets.QFileDialog.getOpenFileName(self, tr("Add Component"), "", "Component document (*.cadprt)")
            if not path:
                return
            import CadDocument
            definition = model().metadata(CadDocument.open(path)).RootComponent
        else:
            definition = choices[index - 2]
        model().add_component(active, definition)
        App.setActiveDocument(active.Document.Name)
        self.root_key, self.active_key, self.active_path = root_key, active_key, active_path
        if self.mdi and self.mdi.activeSubWindow():
            self.store_edit_context(self.mdi.activeSubWindow())

    def show_conversion_report(self):
        component = resolve(self.active_key)
        metadata = model().metadata(component.Document)
        message = QtWidgets.QMessageBox(self)
        message.setWindowTitle(tr("Legacy conversion"))
        message.setText(tr("Source: {0}").format(metadata.LegacySource))
        message.setInformativeText(tr("Save this component document as a new .cadprt file. The original remains unchanged."))
        message.setDetailedText("\n".join(metadata.ConversionReport))
        message.exec()

    def externalize_component(self, key):
        occurrence = resolve(key)
        filename, unused = QtWidgets.QFileDialog.getSaveFileName(
            self, tr("Save to External File"), "", "Component document (*.cadprt)")
        if filename:
            parent = model().owner(occurrence)
            model().externalize(occurrence.LinkedObject, filename)
            App.setActiveDocument(parent.Document.Name)

    def repair_component(self, key):
        occurrence = resolve(key)
        filename, unused = QtWidgets.QFileDialog.getOpenFileName(
            self, tr("Locate Component File"), "", "Component document (*.cadprt)")
        if filename:
            parent = model().owner(occurrence)
            model().repair_component(parent, occurrence, filename)
            App.setActiveDocument(parent.Document.Name)

    def add_reference(self, parent_key=None):
        active = resolve(parent_key or self.active_key)
        if getattr(active, "ComponentRole", "") == "Occurrence":
            active = active.LinkedObject
        choices = []
        for occurrence in model().children(active):
            if occurrence.LinkedObject:
                for obj in occurrence.LinkedObject.Group:
                    if (hasattr(obj, "Shape") and not obj.Shape.isNull()
                            and getattr(obj, "ComponentRole", "") in ("Object", "Result", "Reference")):
                        choices.append((occurrence, obj))
        if not choices:
            raise ValueError(tr("Add a direct child with evaluated geometry first."))
        labels = [f"{link.Label} / {obj.Label} ({link.Name}/{obj.Name})" for link, obj in choices]
        root = resolve(self.root_key)
        preferred = Selection.reference_choice(root, active, Gui.Selection.getSelectionEx("*", 0))
        index = choices.index(preferred) if preferred in choices else -1
        prompt = tr("Direct child object (whole evaluated geometry)")
        if index < 0:
            labels.insert(0, tr("Choose a direct child object"))
            choices.insert(0, None)
            index = 0
        selected, ok = QtWidgets.QInputDialog.getItem(self, tr("Add Reference Object"), prompt, labels, index, False)
        if ok and choices[labels.index(selected)] is not None:
            link, obj = choices[labels.index(selected)]
            model().add_reference(active, link, obj)

    def edit_history(self, key):
        obj = resolve(key)
        if obj is None:
            return
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before editing history."))
        if getattr(obj, "ComponentRole", "") == "Result" and not obj.Frozen:
            obj = obj.Producer
        if obj is None:
            return
        component = model().owner(obj)
        model().activate(component)
        self.active_key = object_key(component)
        App.setActiveDocument(component.Document.Name)
        Gui.activeDocument().activeView().setActiveObject("part", component)
        if getattr(obj, "OperationKind", "") == "Extrude":
            from freecad.gui.ComponentExtrudeTask import launch
            launch(operation=obj)
        else:
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
            if not Gui.getDocument(obj.Document.Name).setEdit(obj.Name):
                raise ValueError(tr("This object has no task editor. Its properties are available in the property editor."))

    def rename_item(self, key):
        obj = resolve(key)
        name, ok = QtWidgets.QInputDialog.getText(self, tr("Rename"), tr("Name"), text=obj.Label)
        if ok and name.strip() and name.strip() != obj.Label:
            with model().transaction(obj.Document, "Rename"):
                obj.Label = name.strip()

    def add_instance(self, key):
        occurrence = resolve(key)
        model().add_component(model().owner(occurrence), occurrence.LinkedObject,
                              placement=App.Placement(occurrence.LinkPlacement))

    def copy_part(self, key):
        occurrence = resolve(key)
        name, ok = QtWidgets.QInputDialog.getText(self, tr("Copy to New Part"), tr("Part name"),
                                                 text=occurrence.LinkedObject.Label + " copy")
        if ok and name.strip():
            model().make_independent(occurrence, label=name.strip())

    def new_sketch(self):
        from freecad.gui.ComponentSketchTask import launch
        launch(resolve(self.active_key))

    def new_extrude(self):
        from freecad.gui.ComponentExtrudeTask import launch
        active = resolve(self.active_key)
        App.setActiveDocument(active.Document.Name)
        Gui.activeDocument().activeView().setActiveObject("part", active)
        launch()

    def build_menu(self, tree, item):
        menu = QtWidgets.QMenu(self)
        # Retain the Python submenu wrappers throughout popup execution.
        menu.component_submenus = []
        if tree == self.structure and item:
            value = item.data(0, QtCore.Qt.UserRole)
            if not value:
                return menu
            obj = resolve(value[0])
            menu.addAction(tr("Edit"), lambda: self.run(lambda: self.activate_item(item)))
            menu.addAction(tr("Add Component"), lambda: self.run(lambda: self.add_component(value[0])))
            menu.addAction(tr("Add Reference Object"), lambda: self.run(lambda: self.add_reference(value[0])))
            definition = obj.LinkedObject if getattr(obj, "ComponentRole", "") == "Occurrence" else obj
            if definition:
                menu.addAction(tr("Rename"), lambda: self.run(lambda: self.rename_item(object_key(definition))))
            if value[1]:
                menu.addAction(tr("Open Component in Tab"), lambda: self.run(lambda: self.open_component_tab(value[0])))
                instances = menu.addMenu(tr("Instances"))
                menu.component_submenus.append(instances)
                instances.addAction(tr("Add Instance"), lambda: self.run(lambda: self.add_instance(value[0])))
                copy = instances.addAction(tr("Copy to New Part"), lambda: self.run(lambda: self.copy_part(value[0])))
                copy.setEnabled(definition is not None and len(self.members(item)) == 1)
                copy.setToolTip(tr("Expand instances to choose the instance that becomes a new part."))
                if len(self.members(item)) > 1:
                    expanded = item.data(0, QtCore.Qt.UserRole + 2) in self.expanded_instances
                    menu.addAction(tr("Collapse Instances") if expanded else tr("Expand Instances"),
                                   lambda: self.run(lambda: self.toggle_instances(item)))
                menu.addAction(tr("Save to External File"), lambda: self.run(lambda: self.externalize_component(value[0])))
                menu.addAction(tr("Locate Component File"), lambda: self.run(lambda: self.repair_component(value[0])))
            view = menu.addMenu(tr("Part View"))
            menu.component_submenus.append(view)
            for label in model().TYPES + ("Reset to Inherited",):
                setting = None if label == "Reset to Inherited" else label
                action = view.addAction(tr(label), lambda checked=False, setting=setting:
                    self.run(lambda: self.set_part_view(item, setting)))
                action.setEnabled(bool(value[1]) and not (setting == "Hidden" and self.protected(item)))
                if not value[1]:
                    action.setToolTip(tr("The root is displayed in full. Part View applies to components added to a parent."))
        else:
            if item:
                key = item.data(0, QtCore.Qt.UserRole)
                obj = resolve(key)
                menu.addAction(tr("Edit"), lambda: self.run(lambda: self.edit_history(key)))
                menu.addAction(tr("Rename"), lambda: self.run(lambda: self.rename_item(key)))
                if hasattr(obj, "Shape") and obj.ComponentRole != "Operation":
                    menu.addAction(tr("Convert to Dumb Object"), lambda: self.run(lambda: self.convert(key)))
                menu.addSeparator()
            if self.active_key:
                menu.addAction(tr("New Sketch"), lambda: self.run(self.new_sketch))
                menu.addAction(tr("Extrude"), lambda: self.run(self.new_extrude))
                menu.addAction(tr("Add Reference Object"), lambda: self.run(self.add_reference))
        return menu

    def menu(self, tree, point):
        menu = self.build_menu(tree, tree.itemAt(point))
        menu.exec(tree.viewport().mapToGlobal(point))

    def convert(self, key):
        choice, ok = QtWidgets.QInputDialog.getItem(self, tr("Convert to Dumb Object"), tr("Operation"),
                                                  [tr("Delete Parameters"), tr("Extract Dumb Body")], 0, False)
        if ok:
            fn = model().delete_parameters if choice == tr("Delete Parameters") else model().extract_dumb
            fn(resolve(self.active_key), resolve(key))

    def slotChangedObject(self, obj, prop):
        try:
            obj = getattr(obj, "Object", obj)
        except (RuntimeError, App.Base.FreeCADError):
            # GUI providers can outlive their document object during close.
            return
        if prop == "Visibility" and self.root_key and not obj.Visibility:
            root = resolve(self.root_key)
            if root:
                try:
                    protected = [root] + model()._path(root, self.active_path)
                    if obj in protected:
                        obj.Visibility = True
                except ValueError:
                    pass
        if prop in ("Label", "Group", "ModelHistory", "Representation", "RepresentationOverrides", "ResultStatus", "Shape", "Visibility", "UserSuppressed"):
            self.timer.start(100)

    def slotDeletedObject(self, obj):
        self.timer.start(100)

    def slotDeletedDocument(self, doc):
        self.timer.start(100)


def show(doc=None):
    global _dock
    if _dock is None:
        _dock = Navigator()
        Gui.getMainWindow().addDockWidget(QtCore.Qt.LeftDockWidgetArea, _dock)
    if doc:
        _dock.set_document(doc)
    _dock.show()
    _dock.raise_()
    return _dock


class Command:
    def __init__(self, create=False):
        self.create = create

    def GetResources(self):
        return {"MenuText": tr("New Component Document") if self.create else tr("Component Structure"),
                "ToolTip": tr("Create a component document") if self.create else tr("Show Component Structure and Model History"),
                "Pixmap": "Geofeaturegroup.svg"}

    def IsActive(self):
        if self.create:
            return not Gui.Control.activeDialog()
        return App.ActiveDocument is not None and any(
            getattr(obj, "ComponentRole", "") == "Document" for obj in App.ActiveDocument.Objects)

    def Activated(self):
        doc = model().new_document() if self.create else App.ActiveDocument
        Gui.activeDocument().activeView().setActiveObject("part", model().metadata(doc).RootComponent)
        show(doc)


def registerCommands():
    Gui.addCommand("Std_NewComponentDocument", Command(True))
    Gui.addCommand("Std_ComponentStructure", Command())
