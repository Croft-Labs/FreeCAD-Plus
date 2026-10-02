# SPDX-License-Identifier: LGPL-2.1-or-later
"""Models, Part Tree and History."""
import FreeCAD as App
import json
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui import ComponentSelection as Selection

_dock = None
_startup_layout = None


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


def task_geometry(component):
    """One unambiguous evaluated item selected through a component occurrence."""
    root = resolve(_dock.root_key) if _dock and _dock.root_key else component
    picks = Selection.selected(root or component, Gui.Selection.getSelectionEx("*", 0))
    if len(picks) == 1 and picks[0].component == component and picks[0].item is not None:
        return [(picks[0].item, picks[0].element)]
    return []


class TaskContext:
    """Return from a definition-owned task to the originating component view."""
    def __init__(self, component):
        self.component = component
        self.selection = task_geometry(component)
        root = resolve(_dock.root_key) if _dock and _dock.root_key else component
        self.profile_selection = [(pick.item, pick.element)
                                  for pick in Selection.selected(root or component, Gui.Selection.getSelectionEx("*", 0))
                                  if pick.item is not None]
        self.dock = _dock
        self.window = self.dock.mdi.activeSubWindow() if self.dock and self.dock.mdi else None
        self.root_key = self.dock.root_key if self.dock else None
        self.path = list(self.dock.active_path) if self.dock else []
        self.edit_key = None
        self.finished = False

    def enter(self):
        App.setActiveDocument(self.component.Document.Name)
        Gui.activeDocument().activeView().setActiveObject("part", self.component)
        if self.dock:
            # Task inputs/preview use definition-local geometry. Keep the origin
            # window's saved context intact until the task returns there.
            self.dock.root_key = self.dock.active_key = object_key(self.component)
            self.dock.active_path = []
            self.dock.refresh()

    def edit(self, obj):
        self.edit_key = object_key(obj)
        Gui.addDocumentObserver(self)
        try:
            if not Gui.getDocument(obj.Document.Name).setEdit(obj.Name):
                raise ValueError(tr("This object has no task editor. Its properties are available in the property editor."))
        except Exception:
            self.restore()
            raise

    def slotResetEdit(self, view_provider):
        if object_key(view_provider.Object) == self.edit_key:
            QtCore.QTimer.singleShot(0, self.restore)

    def restore(self):
        if self.finished:
            return
        self.finished = True
        if self.edit_key:
            Gui.removeDocumentObserver(self)
        if not self.dock or not self.root_key or not resolve(self.root_key):
            return
        if self.window not in self.dock.mdi.subWindowList():
            return
        self.dock.mdi.setActiveSubWindow(self.window)
        root = resolve(self.root_key)
        App.setActiveDocument(root.Document.Name)
        active, path = self.dock.edit_context(root, self.path)
        self.dock.root_key, self.dock.active_key, self.dock.active_path = self.root_key, object_key(active), path
        self.dock.bind_edit_context(self.window)
        model().activate(active, strict=False)
        self.dock.refresh()


def visible_paths(root, component, ids, prefix=""):
    """Resolve representation to native sub-object paths, never change sources."""
    try:
        Gui.getDocument(component.Document.Name)
    except NameError:
        return []  # External GUI providers are removed before their App objects.
    mode = model().representation(root, ids)
    if mode == "Hidden":
        return []
    paths = []
    model().prepare_result_display(component)
    results = {model().display_object(o).Name for o in model().finished_results(component)}
    for obj in [component.Origin] + list(component.Group):
        if getattr(obj, "ComponentRole", "") in ("Occurrence", "Internal") or model().background_result(obj):
            continue
        if not obj.ViewObject or not obj.Visibility or not item_display_available(obj):
            continue
        if mode == "Bodies Only" and obj.Name not in results:
            continue
        paths.append(prefix + obj.Name + ".")
    for child in model().children(component):
        if child.LinkedObject and child.Visibility:
            paths.extend(visible_paths(root, child.LinkedObject, ids + [child.ObjectId],
                                       prefix + child.Name + "."))
    return paths


def item_display_available(obj):
    """Use the same availability for history eyes and component representations."""
    return model().history_state(obj) not in (
        "Suppressed", "Inactive \u2014 dependency", "Missing source", "Needs repair",
        "Unavailable", "Pending")


def is_origin(obj):
    return obj is not None and obj.isDerivedFrom("App::Origin")


def origin_planes(origin):
    return [obj for obj in origin.OriginFeatures if obj.isDerivedFrom("App::Plane")]


def planes_row(item):
    key = item.data(0, QtCore.Qt.UserRole)
    return bool(key and len(key) == 3 and key[2] == "planes")


def protected_origin_item(obj):
    origins = ([obj] if is_origin(obj) else
               [parent for parent in obj.InList if is_origin(parent)] if obj else [])
    return any(any(model().is_component(parent) and parent.Origin == origin
                   for parent in origin.InList) for origin in origins)


def apply_representation(root):
    for child in model().children(root):
        if child.LinkedObject:
            paths = visible_paths(root, child.LinkedObject, [child.ObjectId])
            # Native LinkView preserves source view providers and occurrence pick
            # paths. Restrict its representation without changing source visibility,
            # suppression, native engineering geometry, or BOM/mass participation.
            child.ViewObject.LinkView.setType(-2, False)
            child.ViewObject.LinkView.setLink(child.LinkedObject if paths else None, paths)
        else:
            child.ViewObject.LinkView.setLink(None, [])


class ConversionDialog(QtWidgets.QDialog):
    def __init__(self, component, source, parent=None):
        super().__init__(parent)
        self.component_key, self.source_key = object_key(component), object_key(source)
        self.result_object = None
        self.setWindowTitle(tr("Convert to Dumb Object"))
        self.resize(560, 410)
        layout = QtWidgets.QVBoxLayout(self)
        name = QtWidgets.QLabel(source.Label)
        name.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(name)
        self.choice = QtWidgets.QComboBox()
        self.choice.addItems([tr("Delete Parameters"), tr("Extract Dumb Body")])
        layout.addWidget(self.choice)
        self.summary = QtWidgets.QLabel()
        self.summary.setTextFormat(QtCore.Qt.PlainText)
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)
        self.items = QtWidgets.QTreeWidget()
        self.items.setHeaderLabels([tr("Action"), tr("History item")])
        self.items.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        layout.addWidget(self.items)
        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.choice.currentIndexChanged.connect(self.review)
        if not isinstance(getattr(source, "Proxy", None), (model().ResultProxy, model().ReferenceProxy)) or getattr(source, "Frozen", False):
            self.choice.setCurrentIndex(1)
        self.review()

    def review(self):
        self.items.clear()
        self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        try:
            component, source = resolve(self.component_key), resolve(self.source_key)
            if self.choice.currentIndex() == 0:
                plan = model().parameter_removal_plan(component, source)
                self.summary.setText(tr("Keep this body's or sheet's identity and downstream references. Remove only its exclusive history; shared inputs remain editable."))
                QtWidgets.QTreeWidgetItem(self.items, [tr("Keep geometry"), source.Label])
                for action, objects in ((tr("Remove"), plan["remove"]), (tr("Keep shared"), plan["retain"])):
                    for obj in objects:
                        QtWidgets.QTreeWidgetItem(self.items, [action, obj.Label])
                if plan["reference"]:
                    self.summary.setText(tr("Keep this object's identity and downstream references. Disconnect its source; the child component and its history remain intact."))
            else:
                model().current_shape(source)
                self.summary.setText(tr("Create independent, unlinked geometry. Keep the original object and all of its history."))
                QtWidgets.QTreeWidgetItem(self.items, [tr("Keep original"), source.Label])
                QtWidgets.QTreeWidgetItem(self.items, [tr("Create copy"), source.Label + tr(" copy")])
            self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        except Exception as error:
            self.summary.setText(str(error))

    def accept(self):
        try:
            component, source = resolve(self.component_key), resolve(self.source_key)
            fn = model().delete_parameters if self.choice.currentIndex() == 0 else model().extract_dumb
            self.result_object = fn(component, source)
        except Exception as error:
            self.summary.setText(str(error))
            return
        super().accept()


class PartTree:
    MIME = "application/x-freecad-plus-part-tree-move"


class Navigator(QtWidgets.QDockWidget):
    def __init__(self):
        super().__init__(tr("Components"), Gui.getMainWindow())
        self.setObjectName("ComponentNavigator")
        self.root_key = None
        self.active_key = None
        self.active_path = []
        self.expanded_instances = set()
        self.origin_context = None
        self.restored_documents = set()
        self.refreshing = False
        self.selecting = False
        self.component_views = []
        self.tabs = QtWidgets.QTabWidget()
        self.models = QtWidgets.QTreeWidget()
        self.models.setHeaderLabels([tr("Model"), tr("Instances")])
        self.models.setRootIsDecorated(False)
        self.models.setItemsExpandable(False)
        self.models.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.models.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.structure = QtWidgets.QTreeWidget()
        self.structure.setAcceptDrops(True)
        self.structure.viewport().setAcceptDrops(True)
        self.drag_start = None
        self.drop_position = QtWidgets.QAbstractItemView.OnItem
        self.drop_indicator = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.structure.viewport())
        self.structure.setHeaderLabels([tr("Part name"), tr("View"), tr("Instances"), tr("Part View")])
        self.history = QtWidgets.QTreeWidget()
        self.history.setHeaderLabels([tr("Active"), tr("View"), tr("Item"), tr("State")])
        for tree in (self.structure, self.history):
            tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            for column in range(3):
                tree.header().setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            tree.header().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.history.setRootIsDecorated(False)
        self.tabs.addTab(self.models, tr("Models"))
        self.tabs.addTab(self.structure, tr("Part Tree"))
        self.tabs.addTab(self.history, tr("History"))
        self.context = QtWidgets.QLabel()
        self.context.setWordWrap(True)
        self.context.setTextFormat(QtCore.Qt.PlainText)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(self.context)
        self.reference_notice = QtWidgets.QLabel()
        self.reference_notice.setWordWrap(True)
        self.reference_notice.setTextFormat(QtCore.Qt.PlainText)
        self.reference_notice.hide()
        layout.addWidget(self.reference_notice)
        self.conversion = QtWidgets.QPushButton(tr("Review legacy conversion"))
        self.conversion.clicked.connect(lambda: self.run(self.show_conversion_report))
        self.conversion.hide()
        layout.addWidget(self.conversion)
        layout.addWidget(self.tabs)
        self.setWidget(widget)
        self.structure.itemSelectionChanged.connect(self.select_structure)
        self.models.itemSelectionChanged.connect(self.select_models)
        self.models.itemDoubleClicked.connect(lambda item, column: self.run(
            lambda: self.edit_model(item)) if column == 0 else None)
        self.structure.installEventFilter(self)
        self.structure.viewport().installEventFilter(self)
        self.models.installEventFilter(self)
        self.history.itemSelectionChanged.connect(self.select_history)
        self.structure.itemDoubleClicked.connect(lambda item, column: self.run(lambda: self.activate_item(item)) if column == 0 else None)
        self.structure.itemClicked.connect(lambda item, column: self.run(lambda: self.toggle_component(item)) if column == 1 else None)
        self.history.itemDoubleClicked.connect(lambda item, column: self.run(
            lambda: self.edit_history(item.data(0, QtCore.Qt.UserRole))) if column == 2 else None)
        self.history.itemClicked.connect(lambda item, column: self.run(lambda: self.toggle_item_view(item)) if column == 1 else None)
        self.history.itemChanged.connect(self.history_checked)
        for tree in (self.models, self.structure, self.history):
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

    def run(self, callback, refresh=True):
        try:
            callback()
            if refresh:
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
        models_state = self.tree_state(self.models)
        history_state = self.tree_state(self.history)
        try:
            # Take ownership before disposing Python-backed row data. Native
            # clear() can crash during repeated rebuilds after moving rows.
            for tree in (self.structure, self.models, self.history):
                blocked = tree.blockSignals(True)
                try:
                    removed = [tree.takeTopLevelItem(0) for unused in range(tree.topLevelItemCount())]
                    removed.clear()
                finally:
                    tree.blockSignals(blocked)
            root = resolve(self.root_key) if self.root_key else None
            active = None
            if root:
                active, self.active_path = self.edit_context(root, self.active_path)
                try:
                    Gui.getDocument(active.Document.Name)
                except NameError:
                    # An external App object may briefly outlive its GUI document.
                    return
                active_key = object_key(active)
                origin_context = (root.Document.Name, root.ObjectId, tuple(self.active_path), active.ObjectId)
                if self.origin_context != origin_context:
                    self.origin_context = origin_context
                    active.Origin.Visibility = True
                    for plane in origin_planes(active.Origin):
                        plane.Visibility = False
                if self.active_key != active_key:
                    self.active_key = active_key
                    self.bind_edit_context()
                    if not active.Document.HasPendingTransaction:
                        model().activate(active, strict=False)
                if (active.Document.Name in self.restored_documents
                        and not active.Document.HasPendingTransaction and not Gui.Control.activeDialog()):
                    self.restored_documents.discard(active.Document.Name)
                    model().activate(active, strict=False)
            self.refresh_representations()
            if root is None or active is None:
                self.root_key = self.active_key = None
                self.active_path = []
                self.origin_context = None
                self.context.setText(tr("Create or open a component document."))
                self.conversion.hide()
                self.reference_notice.hide()
                return
            self.conversion.setVisible(bool(model().metadata(active.Document).LegacySource))
            self.context.setText(tr("Editing: {0}").format(active.Label))
            references = [obj for obj in model().history(active) if obj.ComponentRole == "Reference"]
            repair = [obj for obj in references if obj.ResultStatus in ("Missing source", "Needs repair")]
            pending = [obj for obj in references if obj.ResultStatus == "Pending"]
            self.reference_notice.setVisible(bool(repair or pending))
            if repair:
                self.reference_notice.setText(tr("{0} reference object(s) need repair. Edit them in History.").format(len(repair)))
            elif pending:
                self.reference_notice.setText(tr("{0} reference object(s) need updating. Use Refresh References.").format(len(pending)))
            # Definitions are inventory, not extra instances in the assembly.
            file_root = model().metadata(root.Document).RootComponent
            counts = model().instance_counts(file_root)
            definitions = list(model().definitions(root.Document))
            definitions.extend(obj for obj in counts if obj not in definitions)
            for definition in definitions:
                row = QtWidgets.QTreeWidgetItem(self.models, [definition.Label, str(counts.get(definition, 0))])
                row.setData(0, QtCore.Qt.UserRole, object_key(definition))
                row.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
                row.setToolTip(1, tr("Linked occurrences in this file's assembly, including repeated nested uses. The assembly root is a model, not a linked instance."))
                if definition == active:
                    font = row.font(0)
                    font.setBold(True)
                    row.setFont(0, font)
            root_row = QtWidgets.QTreeWidgetItem(self.structure, [root.Label, "", "", ""])
            root_row.setData(0, QtCore.Qt.UserRole, (object_key(root), []))
            root_row.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
            root_row.setFlags((root_row.flags() | QtCore.Qt.ItemIsDropEnabled) & ~QtCore.Qt.ItemIsDragEnabled)
            self.decorate_component(root_row, root, [[]])
            root_row.setExpanded(True)
            self.populate(root_row, root, root, [], set())
            if not structure_state[0]:
                self.structure.expandToDepth(1)
            # The native origin exists independently of editable feature history.
            # Include it exactly once, even for a component with no model items.
            model().prepare_result_display(active)
            items = [active.Origin] + [obj for obj in model().history(active)
                                       if obj != active.Origin and not model().background_result(obj)]
            for obj in active.Group:
                if getattr(obj, "ComponentRole", "") == "Constraint" and obj not in items:
                    model().register_object(active, obj, "Constraint")
                    items.append(obj)
            for obj in items:
                origin = obj == active.Origin
                status = tr("Always active") if origin else tr(model().history_state(obj))
                item = QtWidgets.QTreeWidgetItem(self.history, ["", "", tr("Origin") if origin else obj.Label, status])
                item.setData(0, QtCore.Qt.UserRole, object_key(obj))
                if not origin:
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                inactive = status == tr("Inactive \u2014 dependency")
                state = QtCore.Qt.Checked if origin else (QtCore.Qt.Unchecked if getattr(obj, "UserSuppressed", False) else (QtCore.Qt.PartiallyChecked if inactive else QtCore.Qt.Checked))
                item.setCheckState(0, state)
                if origin:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsUserCheckable)
                item.setToolTip(0, model().history_detail(obj) or tr("Unchecked: suppressed. Partially checked: an input is inactive."))
                if origin:
                    item.setToolTip(0, tr("The component origin is permanent and cannot be suppressed."))
                unavailable = not origin and not item_display_available(obj)
                self.visibility_icon(item, bool(obj.Visibility) and not unavailable, 1)
                if unavailable:
                    item.setToolTip(1, getattr(obj, "ReferenceError", "") or tr("Geometry is unavailable. Restore or repair the item and its inputs."))
                if obj.ViewObject:
                    item.setIcon(2, obj.ViewObject.Icon)
                item.setToolTip(2, tr("Component origin") if origin else tr("Operation") if obj.ComponentRole == "Operation" else tr("Object"))
                item.setToolTip(3, model().history_detail(obj))
                if getattr(obj, "ComponentRole", "") == "Reference":
                    item.setToolTip(2, tr("Reference object. Edit to review or replace its direct-child source."))
                if origin:
                    item.setExpanded(True)
                    planes = QtWidgets.QTreeWidgetItem(item, ["", "", tr("Origin Planes"), tr("Always active")])
                    planes.setData(0, QtCore.Qt.UserRole, object_key(obj) + ("planes",))
                    planes.setCheckState(0, QtCore.Qt.Checked)
                    planes.setFlags(planes.flags() & ~QtCore.Qt.ItemIsUserCheckable)
                    planes.setIcon(2, Gui.getIcon("PartDesign_Plane.svg"))
                    self.visibility_icon(planes, any(plane.Visibility for plane in origin_planes(obj)))
                    planes.setToolTip(0, tr("Origin planes are permanent and cannot be suppressed or deleted."))
                    planes.setToolTip(2, tr("XY, XZ and YZ origin planes. Permanent; cannot be deleted."))
            self.restore_tree(self.structure, structure_state)
            iterator = QtWidgets.QTreeWidgetItemIterator(self.structure)
            while iterator.value():
                row = iterator.value()
                if row.data(0, QtCore.Qt.UserRole + 2) in self.expanded_instances:
                    row.setExpanded(True)
                iterator += 1
            self.restore_tree(self.history, history_state)
            self.restore_tree(self.models, models_state)
        finally:
            self.refreshing = False

    def refresh_representations(self):
        # Native LinkViews belong to definitions, not to the active window. Keep
        # background assemblies current too, evaluating each in its own context.
        for doc in list(App.listDocuments().values()):
            try:
                Gui.getDocument(doc.Name)
            except NameError:
                continue  # App objects can briefly outlive GUI documents on close.
            for component in model().definitions(doc):
                apply_representation(component)
        for entry in list(self.component_views):
            component = resolve(entry["key"])
            paths = visible_paths(component, component, []) if component else []
            entry["snapshot"].setLink(component if paths else None, paths)
            if component and entry.get("window"):
                entry["window"].setWindowTitle(self.component_title(component))

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
        try:
            return bool(root.Visibility) and model().representation(root, ids) != "Hidden" and all(
                link.Visibility for link in model()._path(root, ids))
        except ValueError:
            return False

    def decorate_component(self, item, definition, paths):
        root = resolve(self.root_key)
        visible = not paths or any(self.path_visible(root, ids) for ids in paths)
        self.visibility_icon(item, visible)
        if definition is None:
            item.setToolTip(1, tr("Locate the component file before changing its display."))
            item.setToolTip(3, tr("Right-click and choose Locate Component File. Matching unresolved instances in this file are repaired together."))
        if self.protected(item):
            item.setToolTip(1, tr("The active component and its parent branch cannot be hidden."))
        if definition and any(list(ids) == self.active_path for ids in paths or [[]]):
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)
            item.setBackground(0, self.palette().brush(QtGui.QPalette.Highlight))
            item.setForeground(0, self.palette().brush(QtGui.QPalette.HighlightedText))
        if definition and paths:
            overrides = model().representation_overrides(root, [])
            explicit = sum("/".join(ids) in overrides for ids in paths)
            detail = (tr("Inherited from the component definition.") if not explicit else
                      tr("Override in this view's root component. Reset to Inherited removes it.")
                      if explicit == len(paths) else tr("Mixed inherited settings and occurrence overrides."))
            item.setToolTip(3, detail)

    def populate(self, row, component, root, path, seen):
        key = object_key(component)
        if key in seen:
            return
        seen = seen | {key}
        # Below the root context, only linked occurrences belong in this tree.
        # Constraints remain definition-owned items in History.
        groups = {}
        for link in model().children(component):
            definition = link.LinkedObject
            group_key = object_key(definition) if definition else ("missing", getattr(link, "DefinitionId", "") or link.ObjectId)
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
                        mode = model().representation(root, value[1]) if definition else tr("Missing component")
                        instance = QtWidgets.QTreeWidgetItem(item, [name, "", "", mode])
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
        if any(getattr(resolve(key), "ComponentRole", "") == "Occurrence"
               and resolve(key).LinkedObject is None for key, ids in self.members(item)):
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
        if not item_display_available(obj):
            return
        with model().transaction(obj.Document, "Toggle item visibility"):
            if planes_row(item):
                planes = origin_planes(obj)
                visible = not any(plane.Visibility for plane in planes)
                for plane in planes:
                    plane.Visibility = visible
                if visible:
                    obj.Visibility = True
            else:
                obj.Visibility = not obj.Visibility

    def history_checked(self, item, column):
        if self.refreshing or column != 0:
            return
        key = item.data(0, QtCore.Qt.UserRole)
        if is_origin(resolve(key)):
            return
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

    def select_models(self):
        if self.refreshing or self.selecting:
            return
        self.selecting = True
        try:
            Gui.Selection.clearSelection()
            for row in self.models.selectedItems():
                obj = resolve(row.data(0, QtCore.Qt.UserRole))
                if obj:
                    Gui.Selection.addSelection(obj)
        finally:
            self.selecting = False

    def edit_model(self, item):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before editing another component."))
        key = item.data(0, QtCore.Qt.UserRole)
        if key == self.root_key:
            self.active_key, self.active_path = key, []
            self.bind_edit_context()
            model().activate(resolve(key), strict=False)
        else:
            self.open_component_tab(key)
        self.tabs.setCurrentWidget(self.history)

    def eventFilter(self, watched, event):
        if watched == self.structure.viewport():
            kind = event.type()
            if kind == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
                self.drag_start = event.position().toPoint() if hasattr(event, "position") else event.pos()
            elif kind == QtCore.QEvent.MouseMove and event.buttons() & QtCore.Qt.LeftButton and self.drag_start is not None:
                point = event.position().toPoint() if hasattr(event, "position") else event.pos()
                if (point - self.drag_start).manhattanLength() >= QtWidgets.QApplication.startDragDistance():
                    self.drag_start = None
                    self.run(self.start_tree_drag, refresh=False)
                    return True
            elif kind == QtCore.QEvent.MouseButtonRelease:
                self.drag_start = None
            elif kind in (QtCore.QEvent.DragEnter, QtCore.QEvent.DragMove):
                if not event.mimeData().hasFormat(PartTree.MIME):
                    event.ignore()
                    return True
                self.update_drop_indicator(event)
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
                return True
            elif kind == QtCore.QEvent.DragLeave:
                self.drop_indicator.hide()
                event.accept()
                return True
            elif kind == QtCore.QEvent.Drop:
                self.drop_instances(event)
                return True
        if watched in (self.structure, self.models) and event.type() in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress):
            if watched == self.structure and (event.matches(QtGui.QKeySequence.Cut) or event.matches(QtGui.QKeySequence.Paste)):
                event.accept()
                if event.type() == QtCore.QEvent.KeyPress:
                    callback = self.cut_instances if event.matches(QtGui.QKeySequence.Cut) else lambda: self.paste_instances(deferred=True)
                    self.run(callback, refresh=False)
                return True
            if event.key() == QtCore.Qt.Key_Delete:
                event.accept()
                if event.type() == QtCore.QEvent.KeyPress and watched == self.structure:
                    self.run(self.delete_instances)
                return True
        return super().eventFilter(watched, event)

    def start_tree_drag(self):
        drag = QtGui.QDrag(self.structure)
        drag.setMimeData(self.move_mime())
        drag.exec(QtCore.Qt.MoveAction)
        self.drop_indicator.hide()

    def update_drop_indicator(self, event):
        point = event.position().toPoint() if hasattr(event, "position") else event.pos()
        item = self.structure.itemAt(point)
        if item is None:
            self.drop_position = QtWidgets.QAbstractItemView.OnViewport
            self.drop_indicator.hide()
            return
        rect = self.structure.visualItemRect(item)
        edge = min(5, max(2, rect.height() // 4))
        if point.y() < rect.top() + edge:
            self.drop_position = QtWidgets.QAbstractItemView.AboveItem
            rect.setHeight(2)
        elif point.y() > rect.bottom() - edge:
            self.drop_position = QtWidgets.QAbstractItemView.BelowItem
            rect.setTop(rect.bottom() - 1)
        else:
            self.drop_position = QtWidgets.QAbstractItemView.OnItem
        self.drop_indicator.setGeometry(rect)
        self.drop_indicator.show()

    def drop_instances(self, event):
        self.drop_indicator.hide()
        if not event.mimeData().hasFormat(PartTree.MIME):
            event.ignore()
            return
        point = event.position().toPoint() if hasattr(event, "position") else event.pos()
        item = self.structure.itemAt(point)
        succeeded = []
        self.run(lambda: succeeded.append(self.paste_instances(item, event.mimeData(), self.drop_position, deferred=True)), refresh=False)
        if succeeded:
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def move_mime(self, item=None):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before rearranging parts."))
        rows = self.structure.selectedItems() if item is None or item.isSelected() else [item]
        values = [value for row in rows for value in self.members(row)]
        if not values or any(not value or not value[1] for value in values):
            raise ValueError(tr("Select linked instances; the top-level part cannot be moved."))
        # Selecting a branch moves its children with it, without duplicating them.
        paths = list(dict.fromkeys(tuple(value[1]) for value in values))
        paths = [path for path in paths if not any(path[:len(parent)] == parent
                                                 for parent in paths if len(parent) < len(path))]
        root = resolve(self.root_key)
        payload = {"root": root.ObjectId, "document": model().metadata(root.Document).ObjectId,
                   "items": [{"path": path, "id": model()._path(root, path)[-1].ObjectId} for path in paths]}
        mime = QtCore.QMimeData()
        mime.setData(PartTree.MIME, json.dumps(payload).encode("utf-8"))
        return mime

    def cut_instances(self, item=None):
        QtWidgets.QApplication.clipboard().setMimeData(self.move_mime(item))

    def paste_instances(self, item=None, mime=None, position=None, deferred=False):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before rearranging parts."))
        mime = mime or QtWidgets.QApplication.clipboard().mimeData()
        if not mime.hasFormat(PartTree.MIME):
            raise ValueError(tr("Cut linked instances from this Part Tree first."))
        payload = json.loads(bytes(mime.data(PartTree.MIME)).decode("utf-8"))
        root = resolve(self.root_key)
        if (payload.get("root") != root.ObjectId
                or payload.get("document") != model().metadata(root.Document).ObjectId):
            raise ValueError(tr("Move parts within the same Part Tree and owning file."))
        paths = [tuple(value["path"]) for value in payload["items"]]
        if any(model()._path(root, path)[-1].ObjectId != value["id"]
               for path, value in zip(paths, payload["items"])):
            raise ValueError(tr("The cut selection changed; select and cut it again."))
        item = (self.structure.topLevelItem(0) if position == QtWidgets.QAbstractItemView.OnViewport
                else item or self.structure.currentItem() or self.structure.topLevelItem(0))
        values = self.members(item)
        if len(values) != 1:
            raise ValueError(tr("Expand Instances and choose a single destination instance."))
        destination = tuple(values[0][1])
        before = None
        if position in (QtWidgets.QAbstractItemView.AboveItem, QtWidgets.QAbstractItemView.BelowItem):
            if not destination:
                raise ValueError(tr("The top-level part must remain first."))
            target = model()._path(root, destination)[-1]
            destination = destination[:-1]
            if position == QtWidgets.QAbstractItemView.AboveItem:
                before = target
            else:
                siblings = model().children(model().owner(target))
                following = siblings[siblings.index(target) + 1:]
                moving = {model()._path(root, path)[-1] for path in paths}
                before = next((link for link in following if link not in moving), None)
        elif position == QtWidgets.QAbstractItemView.OnViewport:
            destination = ()
        Gui.Selection.clearSelection()
        changed = model().move_instances(root, paths, destination, before)
        # Follow a moved active branch, including its edited descendants.
        for path in paths:
            if tuple(self.active_path[:len(path)]) == path:
                self.active_path = list(destination + (path[-1],) + tuple(self.active_path[len(path):]))
                break
        if deferred:
            QtCore.QTimer.singleShot(0, self.finish_tree_move)
        else:
            self.finish_tree_move()
        if mime == QtWidgets.QApplication.clipboard().mimeData():
            QtWidgets.QApplication.clipboard().clear()
        return changed

    def finish_tree_move(self):
        self.refresh()
        if resolve(self.root_key):
            self.bind_edit_context()

    def delete_instances(self, item=None):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before deleting instances."))
        rows = self.structure.selectedItems() if item is None or item.isSelected() else [item]
        objects = [resolve(key) for row in rows for key, ids in self.members(row) if ids]
        model().remove_instances(objects)
        root = resolve(self.root_key)
        if root:
            active, self.active_path = self.edit_context(root, self.active_path)
            self.active_key = object_key(active)
            self.bind_edit_context()

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
            self.models.clearSelection()
            self.history.clearSelection()
            for pick in picks:
                for index in range(self.models.topLevelItemCount()):
                    row = self.models.topLevelItem(index)
                    if row.data(0, QtCore.Qt.UserRole) == object_key(pick.component):
                        row.setSelected(True)
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
                        if row.data(0, QtCore.Qt.UserRole) == object_key(model().display_object(pick.item)):
                            row.setSelected(True)
                            self.history.scrollToItem(row)
        finally:
            self.selecting = False

    def store_edit_context(self, window):
        window.setProperty("ComponentActiveKey", self.active_key)
        window.setProperty("ComponentActivePath", self.active_path)

    def bind_edit_context(self, window=None):
        """Bind the exact occurrence in the displayed document, including external definitions."""
        root = resolve(self.root_key)
        try:
            Gui.getDocument(resolve(self.active_key).Document.Name)
            view = Gui.getDocument(root.Document.Name).activeView()
        except NameError:
            # Closing MDI views can outlive their GUI document.
            return False
        if view is None:
            return False
        view.setActiveObject("part", root, Selection.native_path(root, self.active_path))
        window = window or (self.mdi.activeSubWindow() if self.mdi else None)
        if window and tuple(window.property("ComponentKey") or ()) == self.root_key:
            self.store_edit_context(window)
        return True

    @staticmethod
    def component_title(component):
        return component.Label + " \u2014 " + (component.Document.FileName or tr("Unsaved"))

    @staticmethod
    def edit_context(root, ids):
        # Copy, Undo and deleted occurrences can invalidate part of a path.
        # Keep the nearest surviving component instead of editing a stale definition.
        ids = list(ids)
        while ids:
            try:
                component = model()._path(root, ids)[-1].LinkedObject
                if model().is_component(component):
                    return component, ids
            except ValueError:
                pass
            ids.pop()
        return root, []

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
        model().activate(obj, strict=False)
        App.setActiveDocument(root.Document.Name)
        self.root_key, self.active_key, self.active_path = root_key, object_key(obj), list(value[1])
        self.bind_edit_context()
        self.tabs.setCurrentWidget(self.history)

    def open_component_tab(self, key):
        obj = resolve(key)
        if getattr(obj, "ComponentRole", "") == "Occurrence":
            obj = obj.LinkedObject
        if not model().is_component(obj):
            raise ValueError(tr("Select a resolved component."))
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before opening another component view."))
        for entry in list(self.component_views):
            if entry.get("window") not in self.mdi.subWindowList():
                self.component_views.remove(entry)
                continue
            if entry["key"] == object_key(obj) and entry.get("window"):
                self.mdi.setActiveSubWindow(entry["window"])
                self.view_activated(entry["window"])
                return entry["view"]
        model().activate(obj, strict=False)
        App.setActiveDocument(obj.Document.Name)
        existing_windows = list(self.mdi.subWindowList()) if self.mdi else []
        view = Gui.getDocument(obj.Document.Name).createView("Gui::View3DInventor")
        snapshot = Gui.LinkView()
        snapshot.setType(-2, False)
        paths = visible_paths(obj, obj, [])
        snapshot.setLink(obj if paths else None, paths)
        view.getViewer().setSceneGraph(snapshot.RootNode)
        view.setActiveObject("part", obj)
        entry = {"key": object_key(obj), "view": view, "snapshot": snapshot}
        self.component_views.append(entry)
        windows = [window for window in self.mdi.subWindowList() if window not in existing_windows] if self.mdi else []
        if windows:
            # Native view creation can leave the previous document window active.
            # Attach context to the newly created view, then activate that view.
            window = windows[0]
            entry["window"] = window
            window.setProperty("ComponentKey", object_key(obj))
            window.setProperty("ComponentActiveKey", object_key(obj))
            window.setProperty("ComponentActivePath", [])
            window.setWindowTitle(self.component_title(obj))
            window.destroyed.connect(lambda: self.component_views.remove(entry) if entry in self.component_views else None)
            self.mdi.setActiveSubWindow(window)
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
            component, self.active_path = self.edit_context(root, self.active_path)
            self.active_key = object_key(component)
            if not self.bind_edit_context(window):
                return
            self.run(lambda: model().activate(component, strict=False))
            self.selection_timer.start(0)

    def add_component(self, parent_key=None):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before adding a component."))
        active = resolve(parent_key or self.active_key)
        if getattr(active, "ComponentRole", "") == "Occurrence":
            active = active.LinkedObject
        if not model().is_component(active):
            raise ValueError(tr("Select a resolved component to add to."))
        if active.Document.HasPendingTransaction:
            raise ValueError(tr("Finish the active edit before adding a component."))
        context = TaskContext(active)
        choices = [d for d in model().definitions(active.Document)
                   if d != active and not model()._reachable(d, active)]
        labels = [tr("New embedded component…"), tr("Component from file…")] + [f"{d.Label} ({d.Name})" for d in choices]
        selected, ok = QtWidgets.QInputDialog.getItem(self, tr("Add Component"), tr("Component"), labels, 0, False)
        if not ok:
            return
        index = labels.index(selected)
        try:
            if index == 0:
                label, ok = QtWidgets.QInputDialog.getText(self, tr("Add Component"), tr("Name"),
                                                         text=model().next_part_label(active.Document))
                if not ok or not label.strip():
                    return
                return model().add_component(active, label=label.strip())
            elif index == 1:
                path, unused = QtWidgets.QFileDialog.getOpenFileName(self, tr("Add Component"), "", "Component document (*.cadprt)")
                if not path:
                    return
                import CadDocument
                definition = model().metadata(CadDocument.open(path)).RootComponent
            else:
                definition = choices[index - 2]
            return model().add_component(active, definition)
        finally:
            # Opening a source file activates its view. Restore the original root,
            # exact occurrence and native part binding, also on Cancel or failure.
            context.restore()

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
        definition = occurrence.LinkedObject
        if definition is None or definition.Document != occurrence.Document:
            raise ValueError(tr("Select an embedded component to save to an external file."))
        if Gui.Control.activeDialog() or occurrence.Document.HasPendingTransaction:
            raise ValueError(tr("Finish the current edit before saving a component to an external file."))
        if any(resolve(entry["key"]) and resolve(entry["key"]).Document == definition.Document
               and model()._reachable(definition, resolve(entry["key"]))
               for entry in self.component_views):
            raise ValueError(tr("Close isolated tabs for this component and its embedded children before saving to an external file."))
        root_key, active_path = self.root_key, list(self.active_path)
        window = self.mdi.activeSubWindow() if self.mdi else None
        filename, unused = QtWidgets.QFileDialog.getSaveFileName(
            self, tr("Save to External File"), "", "Component document (*.cadprt)")
        if filename:
            parent = model().owner(occurrence)
            try:
                model().externalize(definition, filename)
            finally:
                App.setActiveDocument(parent.Document.Name)
                if window:
                    self.mdi.setActiveSubWindow(window)
                self.root_key, self.active_path = root_key, active_path
                active, self.active_path = self.edit_context(resolve(root_key), active_path)
                self.active_key = object_key(active)
                self.bind_edit_context(window)
                self.refresh()

    def repair_component(self, key):
        occurrence = resolve(key)
        root_key, active_key, active_path = self.root_key, self.active_key, list(self.active_path)
        filename, unused = QtWidgets.QFileDialog.getOpenFileName(
            self, tr("Locate Component File"), "", "Component document (*.cadprt)")
        if filename:
            parent = model().owner(occurrence)
            try:
                model().repair_component(parent, occurrence, filename)
            finally:
                App.setActiveDocument(parent.Document.Name)
                self.root_key, self.active_key, self.active_path = root_key, active_key, active_path

    def choose_reference_source(self, active, reference=None):
        choices = []
        for occurrence in model().children(active):
            if occurrence.LinkedObject:
                for obj in occurrence.LinkedObject.Group:
                    if (hasattr(obj, "Shape") and not obj.Shape.isNull()
                            and getattr(obj, "ComponentRole", "") in ("Object", "Result", "Reference")
                            and model().history_state(obj) == "Ready"):
                        choices.append((occurrence, obj))
        if not choices:
            raise ValueError(tr("Add a direct child with evaluated geometry first."))
        labels = [f"{link.Label} / {obj.Label} ({link.Name}/{obj.Name})" for link, obj in choices]
        root = resolve(self.root_key)
        preferred = Selection.reference_choice(root, active, Gui.Selection.getSelectionEx("*", 0))
        if reference is not None and preferred not in choices:
            preferred = (reference.SourceOccurrence, reference.SourceObject)
        index = choices.index(preferred) if preferred in choices else -1
        prompt = tr("Direct child object (whole evaluated geometry)")
        if index < 0:
            labels.insert(0, tr("Choose a direct child object"))
            choices.insert(0, None)
            index = 0
        title = tr("Repair Reference Object") if reference is not None else tr("Add Reference Object")
        if reference is not None:
            prompt = reference.Label + " (" + reference.GeometryKind + ")\n" + prompt
            if getattr(reference, "ReferenceError", ""):
                prompt += "\n" + reference.ReferenceError
        selected, ok = QtWidgets.QInputDialog.getItem(self, title, prompt, labels, index, False)
        if ok and choices[labels.index(selected)] is not None:
            return choices[labels.index(selected)]
        return None

    def add_reference(self, parent_key=None):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before adding a reference object."))
        active = resolve(parent_key or self.active_key)
        if getattr(active, "ComponentRole", "") == "Occurrence":
            active = active.LinkedObject
        choice = self.choose_reference_source(active)
        if choice:
            return model().add_reference(active, *choice)

    def edit_reference(self, key):
        reference = resolve(key)
        parent = model().owner(reference)
        choice = self.choose_reference_source(parent, reference)
        if choice:
            return model().repair_reference(parent, reference, *choice)

    def refresh_references(self):
        model().activate(resolve(self.active_key), strict=False)

    def edit_history(self, key):
        obj = resolve(key)
        if obj is None or is_origin(obj):
            return
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before editing history."))
        if getattr(obj, "ComponentRole", "") == "Reference":
            self.edit_reference(key)
            return
        if getattr(obj, "ComponentRole", "") == "Result" and not obj.Frozen:
            obj = obj.Producer
        if obj is None:
            return
        component = model().owner(obj)
        model().activate(component, strict=False)
        self.active_key = object_key(component)
        if obj.TypeId == "Assembly::BomObject":
            from CommandCreateBom import CommandCreateBom
            CommandCreateBom().Activated(obj)
        elif getattr(obj, "OperationKind", "") == "Extrude":
            from freecad.gui.ComponentExtrudeTask import launch
            launch(operation=obj)
        else:
            context = TaskContext(component)
            context.enter()
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
            context.edit(obj)

    def rename_item(self, key):
        obj = resolve(key)
        name, ok = QtWidgets.QInputDialog.getText(self, tr("Rename"), tr("Name"), text=obj.Label)
        if ok and name.strip() and name.strip() != obj.Label:
            with model().transaction(obj.Document, "Rename"):
                obj.Label = name.strip()

    def add_instance(self, key):
        occurrence = resolve(key)
        if not model().is_component(occurrence.LinkedObject):
            raise ValueError(tr("Locate the missing component file before adding an instance."))
        model().add_component(model().owner(occurrence), occurrence.LinkedObject,
                              placement=App.Placement(occurrence.LinkPlacement))

    def copy_part(self, key):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before copying a component."))
        occurrence = resolve(key)
        if not model().is_component(occurrence.LinkedObject):
            raise ValueError(tr("Locate the missing component file before copying this instance."))
        name, ok = QtWidgets.QInputDialog.getText(self, tr("Copy to New Part"), tr("Part name"),
                                                 text=occurrence.LinkedObject.Label + " copy")
        if ok and name.strip():
            model().make_independent(occurrence, label=name.strip())

    def new_sketch(self):
        from freecad.gui.ComponentSketchTask import launch
        launch(resolve(self.active_key))

    def new_extrude(self):
        from freecad.gui.ComponentExtrudeTask import launch
        launch()

    def create_bom(self):
        import AssemblyGui  # Register native BOM objects and providers.
        from CommandCreateBom import CommandCreateBom
        CommandCreateBom().Activated()

    def menu_row(self, tree, key, context):
        root = resolve(self.root_key) if self.root_key else None
        if root is None or (self.root_key, root.ObjectId) != context:
            raise ValueError(tr("The component view changed. Open the menu again."))
        iterator = QtWidgets.QTreeWidgetItemIterator(tree)
        while iterator.value():
            row = iterator.value()
            if self.row_key(row) == key:
                return row
            iterator += 1
        raise ValueError(tr("The selected item changed. Open the menu again."))

    def build_menu(self, tree, item):
        menu = QtWidgets.QMenu(self)
        # Retain the Python submenu wrappers throughout popup execution.
        menu.component_submenus = []
        root = resolve(self.root_key) if self.root_key else None
        context = (self.root_key, root.ObjectId) if root else None
        row_key = self.row_key(item) if item else None
        # Timed refreshes replace QTreeWidgetItems even while a popup is open.
        # Resolve the stable row identity when an action fires, never a dead item.
        target = lambda: self.menu_row(tree, row_key, context)
        if tree == self.models:
            if item:
                key = item.data(0, QtCore.Qt.UserRole)
                menu.addAction(tr("Edit"), lambda: self.run(lambda: self.edit_model(target())))
                menu.addAction(tr("Rename"), lambda: self.run(lambda: self.rename_item(key)))
                menu.addAction(tr("Add Instance"), lambda: self.run(
                    lambda: model().add_component(resolve(self.active_key), resolve(key))))
            menu.addAction(tr("Add Component"), lambda: self.run(self.add_component))
            return menu
        if tree == self.structure and item:
            value = item.data(0, QtCore.Qt.UserRole)
            if not value:
                return menu
            obj = resolve(value[0])
            definition = obj.LinkedObject if getattr(obj, "ComponentRole", "") == "Occurrence" else obj
            menu.addAction(tr("Edit"), lambda: self.run(lambda: self.activate_item(target()))).setEnabled(definition is not None)
            if value[1]:
                menu.addAction(tr("Cut"), lambda: self.run(lambda: self.cut_instances(target())))
            paste = menu.addAction(tr("Paste"), lambda: self.run(lambda: self.paste_instances(target())))
            paste.setEnabled(definition is not None and QtWidgets.QApplication.clipboard().mimeData().hasFormat(PartTree.MIME))
            if value[1]:
                menu.addAction(tr("Delete Instance") if len(self.members(item)) == 1 else tr("Delete Instances"),
                               lambda: self.run(lambda: self.delete_instances(target())))
            menu.addAction(tr("Add Component"), lambda: self.run(lambda: self.add_component(value[0]))).setEnabled(definition is not None)
            if definition:
                menu.addAction(tr("Rename"), lambda: self.run(lambda: self.rename_item(object_key(definition))))
            if value[1]:
                menu.addAction(tr("Open Component in Tab"), lambda: self.run(lambda: self.open_component_tab(value[0]))).setEnabled(definition is not None)
                instances = menu.addMenu(tr("Instances"))
                menu.component_submenus.append(instances)
                instances.addAction(tr("Add Instance"), lambda: self.run(lambda: self.add_instance(value[0]))).setEnabled(definition is not None)
                copy = instances.addAction(tr("Copy to New Part"), lambda: self.run(lambda: self.copy_part(value[0])))
                copy.setEnabled(definition is not None and len(self.members(item)) == 1)
                copy.setToolTip(tr("Expand instances to choose the instance that becomes a new part."))
                if len(self.members(item)) > 1:
                    expanded = item.data(0, QtCore.Qt.UserRole + 2) in self.expanded_instances
                    menu.addAction(tr("Collapse Instances") if expanded else tr("Expand Instances"),
                                   lambda: self.run(lambda: self.toggle_instances(target())))
                externalize = menu.addAction(tr("Save to External File"), lambda: self.run(lambda: self.externalize_component(value[0])))
                externalize.setEnabled(definition is not None and definition.Document == obj.Document)
                externalize.setToolTip(tr("Move this embedded definition and its embedded children to a new file; all instances stay shared."))
                menu.addAction(tr("Locate Component File"), lambda: self.run(lambda: self.repair_component(value[0])))
                occurrences = [resolve(key) for key, unused in self.members(item)]
                participation = menu.addMenu(tr("Bill of Materials"))
                menu.component_submenus.append(participation)
                for included, title in ((True, "Include"), (False, "Exclude")):
                    action = participation.addAction(tr(title), lambda checked=False, included=included:
                        self.run(lambda: model().set_bom_inclusion(occurrences, included)))
                    action.setCheckable(True)
                    action.setChecked(all(bool(link.IncludeInBOM) == included for link in occurrences))
                    action.setToolTip(tr("Changes this occurrence in its owning component, including all uses of that component. Display and mass settings are separate. Refresh existing BOMs in their editor."))
            view = menu.addMenu(tr("Part View"))
            menu.component_submenus.append(view)
            paths = [ids for unused, ids in self.members(item) if ids]
            modes = {model().representation(resolve(self.root_key), ids) for ids in paths} if definition else set()
            overrides = model().representation_overrides(resolve(self.root_key), [])
            for label in model().TYPES + ("Reset to Inherited",):
                setting = None if label == "Reset to Inherited" else label
                action = view.addAction(tr(label), lambda checked=False, setting=setting:
                    self.run(lambda: self.set_part_view(target(), setting)))
                action.setEnabled(definition is not None and bool(value[1]) and not (setting == "Hidden" and self.protected(item)))
                if setting is not None:
                    action.setCheckable(True)
                    action.setChecked(modes == {setting})
                else:
                    action.setEnabled(definition is not None and any("/".join(ids) in overrides for ids in paths))
                if not value[1]:
                    action.setToolTip(tr("The root is displayed in full. Part View applies to components added to a parent."))
        else:
            if item and is_origin(resolve(item.data(0, QtCore.Qt.UserRole))):
                origin = resolve(item.data(0, QtCore.Qt.UserRole))
                visible = (any(plane.Visibility for plane in origin_planes(origin))
                           if planes_row(item) else origin.Visibility)
                menu.addAction(tr("Hide") if visible else tr("Show"),
                               lambda: self.run(lambda: self.toggle_item_view(target())))
                menu.addSeparator()
                item = None
            if item:
                key = item.data(0, QtCore.Qt.UserRole)
                obj = resolve(key)
                menu.addAction(tr("Edit"), lambda: self.run(lambda: self.edit_history(key)))
                menu.addAction(tr("Rename"), lambda: self.run(lambda: self.rename_item(key)))
                if obj.ComponentRole == "Reference":
                    action = "Repair Reference Object" if obj.ResultStatus in ("Missing source", "Needs repair") else "Change Reference Source"
                    menu.addAction(tr(action), lambda: self.run(lambda: self.edit_reference(key)))
                if hasattr(obj, "Shape") and (obj.ComponentRole != "Operation" or model().result_for_operation(obj) != obj):
                    menu.addAction(tr("Convert to Dumb Object"), lambda: self.run(lambda: self.convert(key)))
                selected = self.history.selectedItems() if item.isSelected() else [item]
                keys = [row.data(0, QtCore.Qt.UserRole) for row in selected
                        if not is_origin(resolve(row.data(0, QtCore.Qt.UserRole)))]
                for suppressed, title in ((True, "Suppress Selected Items"), (False, "Unsuppress Selected Items")):
                    action = menu.addAction(tr(title), lambda checked=False, keys=keys, suppressed=suppressed:
                        self.run(lambda: model().set_items_suppressed([resolve(key) for key in keys], suppressed)))
                    action.setEnabled(any(bool(getattr(resolve(key), "UserSuppressed", False)) != suppressed for key in keys))
                menu.addSeparator()
            if self.active_key:
                menu.addAction(tr("Refresh References"), lambda: self.run(self.refresh_references))
                menu.addAction(tr("New Sketch"), lambda: self.run(self.new_sketch))
                menu.addAction(tr("Extrude"), lambda: self.run(self.new_extrude))
                menu.addAction(tr("Bill of Materials"), lambda: self.run(self.create_bom))
        return menu

    def menu(self, tree, point):
        menu = self.build_menu(tree, tree.itemAt(point))
        menu.exec(tree.viewport().mapToGlobal(point))

    def convert(self, key):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before converting an object."))
        dialog = ConversionDialog(resolve(self.active_key), model().result_for_operation(resolve(key)), self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self.refresh()
            self.select_native([(self.active_path, dialog.result_object)])

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
        if prop in ("Label", "Group", "ModelHistory", "ResultObjects", "Representation", "RepresentationOverrides", "ResultStatus", "Shape", "Visibility", "UserSuppressed", "ReferenceError", "LinkedObject", "IncludeInBOM"):
            self.timer.start(100)

    def slotDeletedObject(self, obj):
        self.timer.start(100)

    def slotDeletedDocument(self, doc):
        name = getattr(doc, "Document", doc).Name
        # Closed MDI widgets can await deferred destruction. Their document names
        # may already be reused; never reuse those views for a new document.
        self.component_views = [entry for entry in self.component_views if entry["key"][0] != name]
        self.restored_documents.discard(name)
        self.expanded_instances = {group for group in self.expanded_instances
                                   if group[0][0] != name and group[2][0] != name}
        self.timer.start(100)

    def slotFinishSaveDocument(self, doc, filename):
        self.timer.start(100)

    def slotUndoDocument(self, doc):
        self.restored_documents.add(doc.Name)
        # Native Undo restores properties before GUI providers finish restoring.
        self.timer.start(0)

    def slotRedoDocument(self, doc):
        self.slotUndoDocument(doc)


def add_component_from_command():
    """Route legacy creation commands through the component ownership service."""
    from freecad.gui.ComponentExtrudeTask import active_component
    component = active_component()
    panel = _dock or show(component.Document)
    panel.run(lambda: panel.add_component(object_key(component)))


def show(doc=None):
    global _dock
    if _dock is None:
        _dock = Navigator()
        Gui.getMainWindow().addDockWidget(QtCore.Qt.LeftDockWidgetArea, _dock)
    if doc:
        _dock.set_document(doc)
    _dock.show()
    attributes = Gui.getMainWindow().findChild(QtWidgets.QDockWidget, "Model")
    if attributes:
        attributes.setWindowTitle(tr("Attributes"))
        for widget in attributes.findChildren(QtWidgets.QWidget):
            if widget.metaObject().className().endswith("TreePanel"):
                widget.hide()
    _dock.raise_()
    return _dock


class StartupLayout(QtCore.QObject):
    """Apply the component workspace once, after native saved-state restoration."""
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.applied = False
        window.installEventFilter(self)
        if window.isVisible():
            QtCore.QTimer.singleShot(0, self.apply)

    def eventFilter(self, watched, event):
        if watched is self.window and event.type() == QtCore.QEvent.Show:
            QtCore.QTimer.singleShot(0, self.apply)
        return False

    def apply(self):
        if self.applied:
            return
        self.applied = True
        self.window.removeEventFilter(self)
        panel = show()
        attributes = self.window.findChild(QtWidgets.QDockWidget, "Model")
        panel.setFloating(False)
        self.window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, panel)
        if attributes:
            attributes.setFloating(False)
            self.window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, attributes)
            self.window.splitDockWidget(panel, attributes, QtCore.Qt.Vertical)
            attributes.show()
            # Size only after Qt has laid out the newly separated docks.
            QtCore.QTimer.singleShot(0, self.size_panels)

    def size_panels(self):
        attributes = self.window.findChild(QtWidgets.QDockWidget, "Model")
        if attributes and _dock:
            height = _dock.height() + attributes.height()
            self.window.resizeDocks([_dock, attributes],
                                    [round(height * 2 / 3), round(height / 3)],
                                    QtCore.Qt.Vertical)


def install_startup_layout():
    global _startup_layout
    if _startup_layout is None:
        _startup_layout = StartupLayout(Gui.getMainWindow())


def delete_selected_instances():
    """Std_Delete adapter for precise occurrence picks, never bare model selections."""
    if _dock is None or Gui.Control.activeDialog() or not _dock.root_key:
        return False
    entries = Gui.Selection.getSelectionEx("*", 0)
    # Remove permanent datum selections before native Delete, including precise
    # occurrence paths that select their component root in the native tree.
    root = resolve(_dock.root_key)
    for entry in entries:
        for subname in entry.SubElementNames or [""]:
            picks = Selection.resolve(root, entry.Object, subname) if root else []
            if (protected_origin_item(entry.Object)
                    or any(protected_origin_item(pick.item) for pick in picks)):
                Gui.Selection.removeSelection(entry.DocumentName, entry.ObjectName, subname)
    entries = Gui.Selection.getSelectionEx("*", 0)
    if not entries or any(model().is_component(entry.Object) and not entry.SubElementNames for entry in entries):
        return False
    root = resolve(_dock.root_key)
    picks = Selection.selected(root, entries) if root else []
    if not picks or any(not pick.ids or pick.item is not None for pick in picks):
        return False
    occurrences = [model()._path(root, pick.ids)[-1] for pick in picks]
    model().remove_instances(occurrences)
    Gui.Selection.clearSelection()
    _dock.refresh()
    return True


class Command:
    def __init__(self, create=False):
        self.create = create

    def GetResources(self):
        return {"MenuText": tr("New Component Document") if self.create else tr("Components"),
                "ToolTip": tr("Create a component document") if self.create else tr("Show Models, Part Tree and History"),
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


class AddReferenceCommand:
    def GetResources(self):
        return {"MenuText": tr("Add Reference Object"),
                "ToolTip": tr("Reference evaluated geometry from a direct child of the active component"),
                "Pixmap": "LinkImport.svg"}

    def IsActive(self):
        if Gui.Control.activeDialog():
            return False
        try:
            from freecad.gui.ComponentExtrudeTask import active_component
            return model().is_component(active_component())
        except (ValueError, NameError):
            return False

    def Activated(self):
        from freecad.gui.ComponentExtrudeTask import active_component
        component = active_component()
        panel = _dock or show(component.Document)
        panel.run(lambda: panel.add_reference(object_key(component)))


def registerCommands():
    Gui.addCommand("Std_NewComponentDocument", Command(True))
    Gui.addCommand("Std_ComponentStructure", Command())
    Gui.addCommand("PartDesign_AddReferenceObject", AddReferenceCommand())
    install_startup_layout()
