# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Structure and Model History views over the shared component model."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets

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
        if not hasattr(obj, "Shape") or not obj.Visibility:
            continue
        if getattr(obj, "ComponentRole", "") in ("Occurrence", "Operation"):
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
        self.refreshing = False
        self.component_views = []
        self.tabs = QtWidgets.QTabWidget()
        self.structure = QtWidgets.QTreeWidget()
        self.structure.setHeaderLabels([tr("Component"), tr("Type")])
        self.history = QtWidgets.QTreeWidget()
        self.history.setHeaderLabels([tr("Object / operation"), tr("State")])
        for tree in (self.structure, self.history):
            tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            tree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
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
        buttons = QtWidgets.QHBoxLayout()
        for label, callback in [("Add Component", self.add_component),
                                ("Add Reference Object", self.add_reference)]:
            button = QtWidgets.QPushButton(tr(label))
            button.clicked.connect(lambda checked=False, fn=callback: self.run(fn))
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.setWidget(widget)
        self.structure.itemSelectionChanged.connect(self.select_structure)
        self.history.itemSelectionChanged.connect(self.select_history)
        self.structure.itemDoubleClicked.connect(lambda item, column: self.run(lambda: self.activate_item(item)))
        self.history.itemDoubleClicked.connect(lambda item, column: self.run(
            lambda: self.edit_history(item.data(0, QtCore.Qt.UserRole))))
        for tree in (self.structure, self.history):
            tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            tree.customContextMenuRequested.connect(lambda point, tree=tree: self.menu(tree, point))
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.refresh)
        self.mdi = Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        if self.mdi:
            self.mdi.subWindowActivated.connect(self.view_activated)
        App.addDocumentObserver(self)
        self.destroyed.connect(lambda: App.removeDocumentObserver(self))

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
        Gui.getDocument(doc.Name).activeView().setActiveObject("part", root)
        if self.mdi and self.mdi.activeSubWindow():
            self.mdi.activeSubWindow().setProperty("ComponentKey", self.root_key)
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
            self.context.setText(tr("Editing: {0}\nFile: {1}").format(
                active.Label, active.Document.FileName or tr("Unsaved component document")))
            apply_representation(root)
            for entry in list(self.component_views):
                component = resolve(entry["key"])
                if component:
                    paths = visible_paths(component, component, [])
                    entry["snapshot"].setLink(component if paths else None, paths)
            # The root is the component itself, not the document/file wrapper.
            root_item = QtWidgets.QTreeWidgetItem(self.structure, [root.Label, ""])
            root_item.setData(0, QtCore.Qt.UserRole, (object_key(root), []))
            root_item.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
            self.populate(root_item, root, root, [], set())
            if not structure_state[0]:
                self.structure.expandToDepth(1)
            for obj in model().history(active):
                status = tr(model().history_state(obj))
                item = QtWidgets.QTreeWidgetItem(self.history, [obj.Label, status])
                item.setData(0, QtCore.Qt.UserRole, object_key(obj))
                if obj.ViewObject:
                    item.setIcon(0, obj.ViewObject.Icon)
                item.setToolTip(0, tr("Operation") if obj.ComponentRole == "Operation" else tr("Object"))
            self.restore_tree(self.structure, structure_state)
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
                rows[key] = item.isExpanded(), item.isSelected()
            iterator += 1
        return rows, tree.verticalScrollBar().value()

    def restore_tree(self, tree, state):
        rows, scroll = state
        iterator = QtWidgets.QTreeWidgetItemIterator(tree)
        while iterator.value():
            item = iterator.value()
            saved = rows.get(self.row_key(item))
            if saved:
                item.setExpanded(saved[0])
                item.setSelected(saved[1])
            iterator += 1
        tree.verticalScrollBar().setValue(scroll)

    def populate(self, row, component, root, path, seen):
        key = object_key(component)
        if key in seen:
            return
        seen = seen | {key}
        constraints = [o for o in component.Group if getattr(o, "ComponentRole", "") == "Constraint"]
        if constraints:
            group = QtWidgets.QTreeWidgetItem(row, [tr("Assembly Constraints"), ""])
            for constraint in constraints:
                QtWidgets.QTreeWidgetItem(group, [constraint.Label, ""])
        for link in model().children(component):
            ids = path + [link.ObjectId]
            definition = link.LinkedObject
            item = QtWidgets.QTreeWidgetItem(row, [link.Label,
                model().representation(root, ids) if definition else tr("Missing component")])
            item.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
            item.setData(0, QtCore.Qt.UserRole, (object_key(link), ids))
            if definition:
                self.populate(item, definition, root, ids, seen)

    def select_structure(self):
        if self.refreshing:
            return
        items = self.structure.selectedItems()
        if not items:
            return
        value = items[0].data(0, QtCore.Qt.UserRole)
        if value:
            obj = resolve(value[0])
            if obj:
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(obj)

    def select_history(self):
        if self.refreshing:
            return
        items = self.history.selectedItems()
        if items:
            obj = resolve(items[0].data(0, QtCore.Qt.UserRole))
            if obj:
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(obj)

    def activate_item(self, item):
        value = item.data(0, QtCore.Qt.UserRole)
        if not value:
            return
        obj = resolve(value[0])
        if getattr(obj, "ComponentRole", "") == "Occurrence":
            obj = obj.LinkedObject
        if not model().is_component(obj):
            return
        model().activate(obj)
        self.active_key = object_key(obj)
        App.setActiveDocument(obj.Document.Name)
        Gui.activeDocument().activeView().setActiveObject("part", obj)
        self.tabs.setCurrentWidget(self.history)

    def open_component_tab(self, key):
        obj = resolve(key)
        if getattr(obj, "ComponentRole", "") == "Occurrence":
            obj = obj.LinkedObject
        if not model().is_component(obj):
            raise ValueError(tr("Select a resolved component."))
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
            window.setProperty("ComponentKey", object_key(obj))
            window.setWindowTitle(obj.Label + " — " + (obj.Document.FileName or tr("Unsaved")))
            window.destroyed.connect(lambda: self.component_views.remove(entry) if entry in self.component_views else None)
        self.root_key = self.active_key = object_key(obj)
        view.viewAxonometric()
        view.fitAll()
        return view

    def view_activated(self, window):
        if window is None:
            return
        key = window.property("ComponentKey")
        if key and resolve(key):
            self.root_key = self.active_key = tuple(key)
            self.run(lambda: model().activate(resolve(key)))

    def add_component(self):
        active = resolve(self.active_key)
        root_key, active_key = self.root_key, self.active_key
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
        self.root_key, self.active_key = root_key, active_key

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
            self, tr("Externalize Component"), "", "Component document (*.cadprt)")
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

    def add_reference(self):
        active = resolve(self.active_key)
        choices = []
        for occurrence in model().children(active):
            if occurrence.LinkedObject:
                for obj in occurrence.LinkedObject.Group:
                    if hasattr(obj, "Shape") and getattr(obj, "ComponentRole", "") not in ("Operation", "Occurrence"):
                        choices.append((occurrence, obj))
        if not choices:
            raise ValueError(tr("Add a direct child with evaluated geometry first."))
        labels = [f"{link.Label} / {obj.Label} ({link.Name}/{obj.Name})" for link, obj in choices]
        selected, ok = QtWidgets.QInputDialog.getItem(self, tr("Add Reference Object"), tr("Direct child object"), labels, 0, False)
        if ok:
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

    def menu(self, tree, point):
        item = tree.itemAt(point)
        if item is None:
            return
        menu = QtWidgets.QMenu(self)
        if tree == self.structure:
            value = item.data(0, QtCore.Qt.UserRole)
            if not value:
                return
            menu.addAction(tr("Rename…"), lambda: self.run(lambda: self.rename_item(value[0])))
            menu.addAction(tr("Edit Component"), lambda: self.run(lambda: self.activate_item(item)))
            menu.addAction(tr("Open Component in Tab"), lambda: self.run(lambda: self.open_component_tab(value[0])))
            if value[1]:
                menu.addAction(tr("Locate Component File…"), lambda: self.run(lambda: self.repair_component(value[0])))
                menu.addAction(tr("Make Independent"), lambda: self.run(lambda: model().make_independent(resolve(value[0]))))
                menu.addAction(tr("Externalize Component…"), lambda: self.run(lambda: self.externalize_component(value[0])))
                for label in model().TYPES + ("Reset to Inherited",):
                    setting = None if label == "Reset to Inherited" else label
                    menu.addAction(tr(label), lambda checked=False, setting=setting:
                        self.run(lambda: model().set_representation(resolve(self.root_key), value[1], setting)))
        else:
            key = item.data(0, QtCore.Qt.UserRole)
            obj = resolve(key)
            menu.addAction(tr("Edit…"), lambda: self.run(lambda: self.edit_history(key)))
            menu.addAction(tr("Rename…"), lambda: self.run(lambda: self.rename_item(key)))
            if hasattr(obj, "Shape") and obj.ComponentRole != "Operation":
                menu.addAction(tr("Convert to Dumb Object…"), lambda: self.run(lambda: self.convert(key)))
            if getattr(obj, "ComponentRole", "") == "Operation":
                suppressed = getattr(obj, "UserSuppressed", False)
                menu.addAction(tr("Unsuppress") if suppressed else tr("Suppress"),
                               lambda: self.run(lambda: model().set_suppressed(resolve(key), not suppressed)))
        menu.exec(tree.viewport().mapToGlobal(point))

    def convert(self, key):
        choice, ok = QtWidgets.QInputDialog.getItem(self, tr("Convert to Dumb Object"), tr("Operation"),
                                                  [tr("Delete Parameters"), tr("Extract Dumb Body")], 0, False)
        if ok:
            fn = model().delete_parameters if choice == tr("Delete Parameters") else model().extract_dumb
            fn(resolve(self.active_key), resolve(key))

    def slotChangedObject(self, obj, prop):
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
