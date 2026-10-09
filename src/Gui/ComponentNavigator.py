# SPDX-License-Identifier: LGPL-2.1-or-later
"""Models, Part Tree and History."""
import FreeCAD as App
import json
from pathlib import Path
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui import ComponentSelection as Selection

_dock = None
_startup_layout = None
_start_actions = None


def tr(text):
    return App.Qt.translate("ComponentNavigator", text)


def model():
    import ComponentModel
    return ComponentModel


def object_key(obj):
    return obj.Document.Name, obj.Name


def resolve(key):
    if not key or len(key) < 2:
        return None
    doc = App.listDocuments().get(key[0])
    return doc.getObject(key[1]) if doc else None


def task_geometry(component, multiple=False):
    """Evaluated geometry in one component; single-item callers stay unambiguous."""
    root = resolve(_dock.root_key) if _dock and _dock.root_key else component
    picks = Selection.selected(root or component, Gui.Selection.getSelectionEx("*", 0))
    if (picks and (multiple or len(picks) == 1)
            and all(pick.component == component and pick.item is not None for pick in picks)):
        return [(pick.item, pick.element) for pick in picks]
    return []


class TaskContext:
    """Return from a definition-owned task to the originating component view."""
    def __init__(self, component):
        self.component = component
        self.document_name = component.Document.Name
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
        self.rollback = None
        self.monitor = QtCore.QTimer()
        self.monitor.setInterval(100)
        self.monitor.timeout.connect(self.check_edit)

    def enter(self, operation=None):
        App.setActiveDocument(self.component.Document.Name)
        Gui.activeDocument().activeView().setActiveObject("part", self.component)
        if operation is not None:
            self.begin_history_edit(operation)
        if self.dock:
            # Task inputs/preview use definition-local geometry. Keep the origin
            # window's saved context intact until the task returns there.
            self.dock.root_key = self.dock.active_key = object_key(self.component)
            self.dock.active_path = []
            self.dock.refresh()
            self.dock.tabs.setCurrentWidget(self.dock.history)
            self.dock.show()
            self.dock.raise_()

    def edit(self, obj):
        self.begin_history_edit(obj)
        self.edit_key = object_key(obj)
        Gui.addDocumentObserver(self)
        try:
            if not Gui.getDocument(obj.Document.Name).setEdit(obj.Name):
                raise ValueError(tr("This object has no task editor. Its properties are available in the property editor."))
        except Exception:
            self.restore()
            raise

    def begin_history_edit(self, obj):
        if self.rollback is not None:
            return
        items = model().history(self.component)
        obj = model().display_object(obj)
        visible = [item for item in items if not model().background_result(item)]
        if obj not in visible:
            return
        later = set(visible[visible.index(obj) + 1:])
        blocked = {item for item in items if model().display_object(item) in later}
        from Show import TempoVis
        self.rollback = TempoVis(self.component.Document)
        # Capture before any published-result visibility observer mirrors changes.
        self.rollback.modifyVPProperty(items, "Visibility")
        App.addDocumentObserver(self)
        model()._edit_rollbacks[self] = blocked
        self.rollback.hide(list(blocked))
        # Expose the result at the edited history position, if later consumers hid it.
        for result in model().finished_results(self.component):
            if any(result in getattr(item, "ConsumedResults", []) for item in blocked):
                self.rollback.show(result)
        self.monitor.start()
        if self.dock:
            self.dock.refresh()

    def slotStartSaveDocument(self, doc, filename):
        if doc.Name != self.document_name or self.finished:
            return
        # Save evaluated geometry, never cached outputs from the temporary history tail.
        blocked = model()._edit_rollbacks.pop(self, set())
        try:
            for obj in blocked:
                try:
                    obj.touch()
                except RuntimeError:
                    pass
            doc.recompute()
        finally:
            # Restore eligibility even if saving fails before its finish notification.
            model()._edit_rollbacks[self] = blocked

    def slotFinishSaveDocument(self, doc, filename):
        if doc.Name == self.document_name:
            self.check_edit()

    def check_edit(self):
        if self.finished:
            return
        doc = App.listDocuments().get(self.document_name)
        if doc is None:
            self.restore()
            return
        if not Gui.Control.activeDialog() and not Gui.getDocument(doc.Name).getInEdit():
            self.restore()
            return
        # Native editors/previews may restore visibility while the task is open.
        for obj in model()._edit_rollbacks.get(self, ()):
            try:
                if obj.Visibility:
                    obj.Visibility = False
            except RuntimeError:
                pass  # Deleted objects cannot be restored or displayed.

    def slotResetEdit(self, view_provider):
        if object_key(view_provider.Object) == self.edit_key:
            QtCore.QTimer.singleShot(0, self.restore)

    def restore(self):
        if self.finished:
            return
        self.finished = True
        self.monitor.stop()
        blocked = model()._edit_rollbacks.pop(self, set())
        if self.rollback is not None:
            App.removeDocumentObserver(self)
            self.rollback.restore()
            self.rollback = None
            doc = App.listDocuments().get(self.document_name)
            if doc:
                for obj in blocked:
                    try:
                        if doc.getObject(obj.Name) == obj:
                            obj.touch()
                    except RuntimeError:
                        pass
                doc.recompute()
        if self.edit_key:
            Gui.removeDocumentObserver(self)
        if not self.dock or not self.root_key or not resolve(self.root_key):
            return
        if self.window not in self.dock.mdi.subWindowList():
            return
        self.dock.mdi.setActiveSubWindow(self.window)
        root = resolve(self.root_key)
        unused = self.dock.unused_edit(self.window)
        display_root = resolve(unused["file_root"]) if unused else root
        App.setActiveDocument(display_root.Document.Name)
        active, path = self.dock.edit_context(root, self.path)
        self.dock.root_key, self.dock.active_key, self.dock.active_path = self.root_key, object_key(active), path
        self.dock.bind_edit_context(self.window)
        model().activate(active, strict=False)
        self.dock.refresh()


def display_items(root, component, ids, prefix=""):
    """Visible (native path, occurrence IDs, object) without changing appearance."""
    try:
        Gui.getDocument(component.Document.Name)
    except NameError:
        return []  # External GUI providers are removed before their App objects.
    mode = model().representation(root, ids)
    if mode == "Hidden":
        return []
    items = []
    model().prepare_result_display(component)
    results = {model().display_object(o).Name for o in model().finished_results(component)}
    for obj in [component.Origin] + list(component.Group):
        if getattr(obj, "ComponentRole", "") in ("Occurrence", "Internal") or model().background_result(obj):
            continue
        if not obj.ViewObject or not obj.Visibility or not item_display_available(obj):
            continue
        if mode == "Bodies Only" and obj.Name not in results:
            continue
        items.append((prefix + obj.Name + ".", tuple(ids), obj))
    for child in model().children(component):
        if child.LinkedObject and child.Visibility:
            items.extend(display_items(root, child.LinkedObject, ids + [child.ObjectId],
                                       prefix + child.Name + "."))
    return items


def visible_paths(root, component, ids, prefix=""):
    """Native LinkView paths share the context display traversal."""
    return [path for path, unused_ids, unused_obj in display_items(root, component, ids, prefix)]


def context_display_plan(root, active_ids):
    """Return native paths with their per-occurrence transparency floor.

    This is view-local render input, not saved materials. Zero means retain the
    authored appearance. A renderer must take max(authored transparency, floor)
    separately for each material, retaining its colors and other properties.
    Validate the complete active path rather than guessing a surviving ancestor.
    """
    active_ids = tuple(active_ids)
    model()._path(root, active_ids)
    return [(path, obj, 0.0 if ids[:len(active_ids)] == active_ids else 0.75)
            for path, ids, obj in display_items(root, root, [])]


def context_transparencies(root, path, obj, floor):
    """Keep per-face transparency and the outermost occurrence material override."""
    component = root
    provider = obj.ViewObject
    for token in path.split(".")[:-1]:
        link = next((link for link in model().children(component) if link.Name == token), None)
        if link is None:
            break
        if getattr(link.ViewObject, "OverrideMaterial", False):
            provider = link.ViewObject
            break
        component = link.LinkedObject
    materials = getattr(provider, "ShapeAppearance", ())
    values = [material.Transparency for material in materials]
    if not values:
        values = [getattr(provider, "Transparency", 0) / 100.0]
    return [max(floor, value) for value in values]


def context_scene(root, active_ids):
    """Build a view-owned native link scene with transparency-only overrides."""
    from pivy import coin
    scene = coin.SoSeparator()
    links = []
    materials = {}
    for path, obj, floor in context_display_plan(root, active_ids):
        branch = coin.SoSeparator()
        if floor:
            material = coin.SoMaterial()
            for field in (material.ambientColor, material.diffuseColor,
                          material.specularColor, material.emissiveColor, material.shininess):
                field.setIgnored(True)
            values = context_transparencies(root, path, obj, floor)
            material.transparency.setValues(0, len(values), values)
            material.setOverride(True)
            branch.addChild(material)
            materials[path] = material
        link = Gui.LinkView()
        link.setType(-2, False)
        link.setLink(root, [path])
        branch.addChild(link.RootNode)
        scene.addChild(branch)
        links.append(link)
    return scene, links, materials


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
    HISTORY_MIME = "application/x-freecad-plus-history-order"

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
        self.unused_views = []
        self.context_views = []
        self.tabs = QtWidgets.QTabWidget()
        self.models = QtWidgets.QTreeWidget()
        self.models.setHeaderLabels([tr("Model"), tr("Instances")])
        self.models.setRootIsDecorated(True)
        self.models.setItemsExpandable(True)
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
        self.history.setAcceptDrops(True)
        self.history.viewport().setAcceptDrops(True)
        self.history_drag_start = None
        self.history_drop_indicator = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.history.viewport())
        self.history_drag_context = None
        self.history_scroll_timer = QtCore.QTimer(self)
        self.history_scroll_timer.setInterval(80)
        self.history_scroll_timer.timeout.connect(self.scroll_history_drag)
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
        self.history.viewport().installEventFilter(self)
        self.structure.itemDoubleClicked.connect(lambda item, column: self.run(lambda: self.activate_item(item)) if column == 0 else None)
        self.structure.itemClicked.connect(lambda item, column: self.run(lambda: self.toggle_component(item)) if column == 1 else None)
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

    def set_document(self, doc, edit_path=None):
        self.end_unused_edit()
        root = model().metadata(doc).RootComponent
        self.root_key = object_key(root)
        active, self.active_path = self.edit_context(root, edit_path or [])
        self.active_key = object_key(active)
        Gui.getDocument(doc.Name).activeView().setActiveObject(
            "part", root, Selection.native_path(root, self.active_path))
        if self.mdi and self.mdi.activeSubWindow():
            self.mdi.activeSubWindow().setProperty("ComponentKey", self.root_key)
            self.store_edit_context(self.mdi.activeSubWindow())
        self.refresh()

    def refresh(self):
        if self.refreshing:
            return
        unused = self.unused_edit()
        if unused and not model().is_component(resolve(unused["key"])):
            self.end_unused_edit()
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
            # Undo of legacy conversion can restore the original native Part
            # under the same name after removing its component UUID/role.
            # Treat it as legacy again until Redo/reopen restores the definition.
            if not model().is_component(root):
                root = None
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
            self.context.setText(tr("Editing: {0}").format(
                active.Document.Label if model().is_file_container(active)
                else model().component_label(active, root.Document)))
            references = [obj for obj in model().history(active) if obj.ComponentRole == "Reference"]
            repair = [obj for obj in references if obj.ResultStatus in ("Missing source", "Needs repair")]
            pending = [obj for obj in references if obj.ResultStatus == "Pending"]
            self.reference_notice.setVisible(bool(repair or pending))
            if repair:
                self.reference_notice.setText(tr("{0} reference object(s) need repair. Edit them in History.").format(len(repair)))
            elif pending:
                self.reference_notice.setText(tr("{0} reference object(s) need updating. Use Refresh References.").format(len(pending)))
            # Definitions are inventory, not extra instances in the assembly.
            unused = self.unused_edit()
            file_context = resolve(unused["file_root"]) if unused else root
            file_root = model().metadata(file_context.Document).RootComponent
            counts = model().instance_counts(file_root)
            self.populate_models(self.models, file_root.Document, file_root.Document, counts, active, ())
            roots = [file_root]
            if unused:
                roots.append(resolve(unused["key"]))
            elif root != file_root:
                roots.append(root)
            for tree_root in roots:
                file_container = model().is_file_container(tree_root)
                title = tree_root.Document.Label if file_container else tree_root.Label
                root_row = QtWidgets.QTreeWidgetItem(self.structure, [title, "", "", ""])
                root_row.setData(0, QtCore.Qt.UserRole, (object_key(tree_root), []))
                root_row.setIcon(0, Gui.getIcon("freecad.svg" if file_container else "Geofeaturegroup.svg"))
                root_row.setFlags((root_row.flags() | QtCore.Qt.ItemIsDropEnabled) & ~QtCore.Qt.ItemIsDragEnabled)
                self.decorate_component(root_row, tree_root, [[]])
                temporary = unused and object_key(tree_root) == unused["key"]
                if temporary:
                    root_row.setText(0, model().component_label(tree_root, file_root.Document)
                                     + tr(" (unused model)"))
                    root_row.setFlags(root_row.flags() & ~QtCore.Qt.ItemIsDropEnabled)
                root_row.setToolTip(0, tr("Temporary editing view; not an assembly occurrence.") if temporary
                                   else tr("File; fixed global coordinate system.") if file_container
                                   else tr("Component editing context."))
                root_row.setExpanded(True)
                self.populate(root_row, tree_root, tree_root, [], set())
            if not structure_state[0]:
                self.structure.expandToDepth(1)
            # The native origin exists independently of editable feature history.
            # Include it exactly once, even for a component with no model items.
            model().prepare_result_display(active)
            items = [active.Origin] + [obj for obj in model().history(active)
                                       if obj != active.Origin and not model().background_result(obj)]
            for obj in ([] if model().is_file_container(active) else active.Group):
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
                state = QtCore.Qt.Checked if origin else (QtCore.Qt.Unchecked if model().edit_suppressed(obj) or getattr(obj, "UserSuppressed", False) else (QtCore.Qt.PartiallyChecked if inactive else QtCore.Qt.Checked))
                item.setCheckState(0, state)
                if origin or model().edit_suppressed(obj):
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
                item.setToolTip(2, tr("Component origin") if origin else
                               tr("Double-click to edit sketch") if obj.isDerivedFrom("Sketcher::SketchObject") else
                               tr("Double-click to edit"))
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

    def populate_models(self, parent, document, context_document, counts, active, ancestors):
        ident = model().metadata(document).ObjectId
        if ident in ancestors:
            return
        path = ancestors + (ident,)
        for definition in model().definitions(document):
            if model().is_file_container(definition):
                continue
            row = QtWidgets.QTreeWidgetItem(parent, [model().component_label(definition, context_document),
                                                     str(counts.get(definition, 0))])
            row.setData(0, QtCore.Qt.UserRole, object_key(definition))
            row.setData(0, QtCore.Qt.UserRole + 4, path)
            row.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
            row.setToolTip(0, document.FileName or document.Label)
            row.setToolTip(1, tr("Linked occurrences in this file's assembly, including repeated nested uses. The assembly root is a model, not a linked instance."))
            if definition == active:
                self.decorate_active(row)
        for source in model().external_documents(document, allow_unresolved=True):
            row = QtWidgets.QTreeWidgetItem(parent, [Path(source.FileName).stem or source.Label, ""])
            row.setData(0, QtCore.Qt.UserRole + 3, (document.Name, source.Name))
            row.setData(0, QtCore.Qt.UserRole + 4, path + (model().metadata(source).ObjectId,))
            row.setIcon(0, Gui.getIcon("folder.svg"))
            row.setToolTip(0, source.FileName)
            self.populate_models(row, source, context_document, counts, active, path)
        for record in model().file_imports(document):
            if record.Source is None:
                row = QtWidgets.QTreeWidgetItem(parent, [record.Label, tr("Missing file")])
                row.setData(0, QtCore.Qt.UserRole + 3, object_key(record))
                row.setData(0, QtCore.Qt.UserRole + 4, path + (record.DocumentId,))
                row.setToolTip(0, tr("Locate the original imported file to restore its component definitions."))

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
            if not model().is_component(component):
                component = None
            paths = visible_paths(component, component, []) if component else []
            entry["snapshot"].setLink(component if paths else None, paths)
            if component and entry.get("window"):
                entry["window"].setWindowTitle(self.component_title(component))

        for entry in list(self.unused_views):
            component = resolve(entry["key"])
            if not model().is_component(component):
                self.end_unused_edit(entry["window"])
                continue
            paths = visible_paths(component, component, [])
            entry["snapshot"].setLink(component if paths else None, paths)

        self.refresh_context_view()

    def clear_context_view(self, window=None, restore=True):
        window = window or (self.mdi.activeSubWindow() if self.mdi else None)
        entry = next((entry for entry in self.context_views if entry["window"] == window), None)
        if entry:
            # These nodes belong to this view, not to shared view providers. Remove
            # them even during window destruction while the retained root is alive.
            entry["selection"].removeChild(entry["hidden"])
            entry["original"].removeChild(entry["scene"])
            self.context_views.remove(entry)
            entry["original"].unref()

    def refresh_context_view(self):
        window = self.mdi.activeSubWindow() if self.mdi else None
        # Native view creation can refresh before its isolated scene and component
        # context are registered. Do not apply the previous tab's context yet.
        if not window or not window.property("ComponentKey"):
            return
        if self.unused_edit(window) or not self.active_path or not resolve(self.root_key):
            self.clear_context_view(window)
            return
        from pivy import coin
        root = resolve(self.root_key)
        scene, links, materials = context_scene(root, self.active_path)
        entry = next((entry for entry in self.context_views if entry["window"] == window), None)
        if not entry:
            view = Gui.getDocument(root.Document.Name).activeView()
            original = view.getViewer().getSceneGraph()
            isolated = next((item for item in self.component_views if item.get("window") == window), None)
            selection = isolated["selection"] if isolated else next(
                original.getChild(i) for i in range(original.getNumChildren())
                if original.getChild(i).getTypeId().getName() == "SoFCUnifiedSelection")
            original.ref()
            hidden = coin.SoDrawStyle()
            hidden.style = coin.SoDrawStyle.INVISIBLE
            hidden.setOverride(True)
            selection.insertChild(hidden, 0)
            entry = {"window": window, "view": view, "original": original,
                     "selection": selection, "hidden": hidden, "document": root.Document.Name}
            self.context_views.append(entry)
            window.destroyed.connect(lambda: self.clear_context_view(window, restore=False))
        # Keep the viewer's native root, camera and selection graph in place. Full
        # scene replacement here can invalidate native state when another view is
        # created. Hide native drawing inside its selection separator, retaining
        # native picking; render unpickable per-occurrence links beside it.
        unpickable = coin.SoPickStyle()
        unpickable.style = coin.SoPickStyle.UNPICKABLE
        unpickable.setOverride(True)
        scene.insertChild(unpickable, 0)
        if "scene" in entry:
            entry["original"].removeChild(entry["scene"])
        entry["original"].addChild(scene)
        entry.update(scene=scene, links=links, materials=materials)

    def unused_edit(self, window=None):
        window = window or (self.mdi.activeSubWindow() if self.mdi else None)
        return next((entry for entry in self.unused_views if entry["window"] == window), None)

    def begin_unused_edit(self, key):
        self.clear_context_view()
        self.end_unused_edit()
        obj = resolve(key)
        window = self.mdi.activeSubWindow()
        if window is None or not model().is_component(obj):
            raise ValueError(tr("Activate a file tab before editing this model."))
        root = resolve(self.root_key)
        view = Gui.getDocument(root.Document.Name).activeView()
        snapshot = Gui.LinkView()
        snapshot.setType(-2, False)
        paths = visible_paths(obj, obj, [])
        snapshot.setLink(obj if paths else None, paths)
        entry = {"window": window, "view": view, "snapshot": snapshot,
                 "scene": view.getViewer().getSceneGraph(),
                 "file_root": self.root_key, "key": tuple(key)}
        # The viewer releases its Coin reference when replacing the scene. A
        # Python wrapper alone does not keep the native graph alive.
        entry["scene"].ref()
        self.unused_views.append(entry)
        window.destroyed.connect(lambda: self.discard_unused_edit(entry))
        view.getViewer().setSceneGraph(snapshot.RootNode)
        window.setProperty("ComponentKey", tuple(key))
        self.root_key = self.active_key = tuple(key)
        self.active_path = []
        self.bind_edit_context(window)
        model().activate(obj, strict=False)

    def discard_unused_edit(self, entry):
        if entry in self.unused_views:
            self.unused_views.remove(entry)
            entry["scene"].unref()

    def end_unused_edit(self, window=None):
        entry = self.unused_edit(window)
        if not entry:
            return
        entry["view"].getViewer().setSceneGraph(entry["scene"])
        self.discard_unused_edit(entry)
        entry["window"].setProperty("ComponentKey", entry["file_root"])
        entry["window"].setProperty("ComponentActiveKey", entry["file_root"])
        entry["window"].setProperty("ComponentActivePath", [])
        if entry["window"] == self.mdi.activeSubWindow():
            self.root_key = self.active_key = entry["file_root"]
            self.active_path = []
            if resolve(self.root_key):
                self.bind_edit_context(entry["window"])

    def temporarily_hidden(self, item):
        entry = self.unused_edit()
        return bool(entry and object_key(self.tree_root(item)) != entry["key"])

    @staticmethod
    def row_key(item):
        def freeze(value):
            return tuple(freeze(v) for v in value) if isinstance(value, (list, tuple)) else value
        key = freeze(item.data(0, QtCore.Qt.UserRole))
        file_path = freeze(item.data(0, QtCore.Qt.UserRole + 4))
        return (key, file_path) if file_path else key

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

    def tree_root(self, item):
        while item.parent():
            item = item.parent()
        return resolve(item.data(0, QtCore.Qt.UserRole)[0])

    def protected(self, item):
        # The active occurrence and its ancestors must remain visible.
        if object_key(self.tree_root(item)) != self.root_key:
            obj = resolve(item.data(0, QtCore.Qt.UserRole)[0])
            definition = obj.LinkedObject if getattr(obj, "ComponentRole", "") == "Occurrence" else obj
            return definition is not None and (object_key(definition) == self.active_key
                   or model()._reachable(definition, resolve(self.active_key)))
        return any(value is not None and list(value[1]) == self.active_path[:len(value[1])]
                   for value in self.members(item))

    @staticmethod
    def path_visible(root, ids):
        try:
            return bool(root.Visibility) and model().representation(root, ids) != "Hidden" and all(
                link.Visibility for link in model()._path(root, ids))
        except ValueError:
            return False

    def decorate_active(self, item):
        # Use the native active-item preference, independently of selection color.
        packed = App.ParamGet("User parameter:BaseApp/Preferences/TreeView").GetUnsigned(
            "TreeActiveColor", 1538528255)
        color = QtGui.QColor((packed >> 24) & 255, (packed >> 16) & 255,
                            (packed >> 8) & 255, packed & 255)
        font = item.font(0)
        font.setBold(True)
        item.setFont(0, font)
        item.setBackground(0, QtGui.QBrush(color))

    def model_edit_path(self, definition):
        """Resolve a per-tab remembered occurrence, or the first depth-first use."""
        root = resolve(self.root_key)
        if definition == root:
            return []
        window = self.mdi.activeSubWindow() if self.mdi else None
        remembered = dict(window.property("ComponentEditPaths") or {}) if window else {}
        ids = remembered.get(definition.ObjectId)
        if ids:
            component, path = self.edit_context(root, ids)
            if component == definition and path == list(ids):
                return path
        def visit(component, path, ancestors):
            key = object_key(component)
            if key in ancestors:
                return None
            for link in model().children(component):
                child = link.LinkedObject
                if not model().is_component(child):
                    continue
                child_path = path + [link.ObjectId]
                if child == definition:
                    return child_path
                found = visit(child, child_path, ancestors | {key})
                if found is not None:
                    return found
            return None
        return visit(root, [], set())

    def decorate_component(self, item, definition, paths):
        root = self.tree_root(item)
        visible = not paths or any(self.path_visible(root, ids) for ids in paths)
        unused = self.unused_edit()
        if unused and object_key(root) == unused["key"]:
            # The temporary view ignores the definition's assembly visibility.
            visible = not paths or any(model().representation(root, ids) != "Hidden"
                                       and all(link.Visibility for link in model()._path(root, ids))
                                       for ids in paths)
        self.visibility_icon(item, visible)
        if self.temporarily_hidden(item):
            self.visibility_icon(item, False)
            for column in range(self.structure.columnCount()):
                item.setForeground(column, QtGui.QBrush(QtGui.QColor(128, 128, 128)))
            item.setToolTip(1, tr("Hidden while editing an unused model. Edit this component to return."))
            return
        if definition is None:
            item.setToolTip(1, tr("Locate the component file before changing its display."))
            item.setToolTip(3, tr("Right-click and choose Locate Component File. Matching unresolved instances in this file are repaired together."))
        if self.protected(item):
            item.setToolTip(1, tr("The active component and its parent branch cannot be hidden."))
        if definition and object_key(definition) == self.active_key:
            self.decorate_active(item)
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
            title = model().component_label(definition, root.Document) if definition else links[0].Label
            item = QtWidgets.QTreeWidgetItem(row, [title, "", "x" + str(len(links)), modes.pop() if len(modes) == 1 else tr("Mixed")])
            item.setIcon(0, Gui.getIcon("Geofeaturegroup.svg"))
            item.setData(0, QtCore.Qt.UserRole, values[0])
            item.setData(0, QtCore.Qt.UserRole + 1, values)
            group_id = (object_key(root), tuple(path), definition_key)
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

    def change_part_view(self, updates, show=False, root=None):
        root = root or resolve(self.root_key)
        overrides = model().representation_overrides(root, updates)
        if object_key(root) == self.root_key and model().representation(root, self.active_path, root_overrides=overrides) == "Hidden":
            raise ValueError(tr("The active component cannot be hidden. Edit another component first."))
        model().set_representations(root, updates, show=show)

    def set_part_view(self, item, setting):
        if self.temporarily_hidden(item):
            raise ValueError(tr("Edit a component in the assembly before changing its visibility."))
        updates = [(ids, setting) for key, ids in self.members(item) if ids]
        if not updates:
            raise ValueError(tr("The root component is displayed in full."))
        if setting == "Hidden" and self.protected(item):
            raise ValueError(tr("The active component and its parent branch cannot be hidden."))
        self.change_part_view(updates, root=self.tree_root(item))

    def toggle_component(self, item):
        if self.temporarily_hidden(item):
            return
        if not item.data(0, QtCore.Qt.UserRole):
            return
        if any(getattr(resolve(key), "ComponentRole", "") == "Occurrence"
               and resolve(key).LinkedObject is None for key, ids in self.members(item)):
            return
        root = self.tree_root(item)
        members = self.members(item)
        visible = any(self.path_visible(root, ids) for key, ids in members)
        if visible:
            self.set_part_view(item, "Hidden")
            return
        updates = [(ids, None) for key, ids in members if ids]
        overrides = model().representation_overrides(root, updates)
        updates = [(ids, "Bodies Only" if model().representation(root, ids, root_overrides=overrides) == "Hidden"
                    else None) for ids, unused in updates]
        self.change_part_view(updates, show=True, root=root)

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
        if self.refreshing or self.selecting:
            return
        self.selecting = True
        try:
            Gui.Selection.clearSelection()
            for row in self.structure.selectedItems():
                root = self.tree_root(row)
                for value in self.members(row):
                    if value:
                        Gui.Selection.addSelection(root.Document.Name, root.Name,
                                                   Selection.native_path(root, value[1], None))
        finally:
            self.selecting = False

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
        if not key:
            return
        definition = resolve(key)
        self.end_unused_edit()
        path = self.model_edit_path(definition)
        if path is not None:
            root = resolve(self.root_key)
            obj = model()._path(root, path)[-1] if path else root
            # Reuse exactly the same activation/visibility path as Part Tree Edit.
            root_row = QtWidgets.QTreeWidgetItem()
            root_row.setData(0, QtCore.Qt.UserRole, (self.root_key, []))
            row = QtWidgets.QTreeWidgetItem(root_row)
            row.setData(0, QtCore.Qt.UserRole, (object_key(obj), path))
            self.activate_item(row)
        else:
            self.begin_unused_edit(key)
        self.tabs.setCurrentWidget(self.history)

    def eventFilter(self, watched, event):
        if watched == self.history.viewport():
            kind = event.type()
            if kind == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
                point = event.position().toPoint() if hasattr(event, "position") else event.pos()
                index = self.history.indexAt(point)
                row = self.history.itemAt(point)
                self.history_drag_start = point if (index.isValid() and index.column() in (2, 3)
                    and not is_origin(resolve(row.data(0, QtCore.Qt.UserRole)))) else None
            elif kind == QtCore.QEvent.MouseMove and event.buttons() & QtCore.Qt.LeftButton and self.history_drag_start is not None:
                point = event.position().toPoint() if hasattr(event, "position") else event.pos()
                if (point - self.history_drag_start).manhattanLength() >= QtWidgets.QApplication.startDragDistance():
                    self.history_drag_start = None
                    self.run(self.start_history_drag, refresh=False)
                    return True
            elif kind == QtCore.QEvent.MouseButtonRelease:
                self.history_drag_start = None
            elif kind in (QtCore.QEvent.DragEnter, QtCore.QEvent.DragMove, QtCore.QEvent.Drop):
                return self.history_drag_event(event)
            elif kind == QtCore.QEvent.DragLeave:
                self.finish_history_drag()
                event.accept()
                return True
        if (watched == self.history.viewport() and event.type() == QtCore.QEvent.MouseButtonDblClick
                and event.button() == QtCore.Qt.LeftButton):
            point = event.position().toPoint() if hasattr(event, "position") else event.pos()
            index = self.history.indexAt(point)
            if index.isValid() and index.column() in (2, 3):
                # A document refresh can replace the row after the first click,
                # invalidating QTreeWidget's pressed index and itemDoubleClicked.
                # Resolve the current row at the native double-click, then carry
                # only its document identity across task startup/tree rebuilds.
                key = tuple(self.history.itemAt(point).data(0, QtCore.Qt.UserRole))
                QtCore.QTimer.singleShot(0, lambda key=key: self.run(lambda: self.edit_history(key)))
                event.accept()
                return True
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
                if event.type() == QtCore.QEvent.KeyPress:
                    self.run(self.delete_instances if watched == self.structure else self.delete_models)
                return True
        return super().eventFilter(watched, event)

    def history_move_mime(self):
        component = resolve(self.active_key)
        if Gui.Control.activeDialog() or component.Document.HasPendingTransaction:
            raise ValueError(tr("Finish the current task before reordering history."))
        items = [resolve(row.data(0, QtCore.Qt.UserRole)) for row in self.history.selectedItems()]
        items = [obj for obj in items if obj and not is_origin(obj)]
        model().history_move_order(component, items, 0)  # Validate movable membership.
        payload = {"component": object_key(component), "id": component.ObjectId,
                   "items": [(obj.Name, obj.ObjectId) for obj in items]}
        mime = QtCore.QMimeData()
        mime.setData(self.HISTORY_MIME, json.dumps(payload).encode("utf-8"))
        return mime

    def start_history_drag(self):
        drag = QtGui.QDrag(self.history)
        drag.setMimeData(self.history_move_mime())
        try:
            drag.exec(QtCore.Qt.MoveAction)
        finally:
            self.finish_history_drag()

    def finish_history_drag(self):
        self.history_drop_indicator.hide()
        self.history_scroll_timer.stop()
        self.history_drag_context = None

    def scroll_history_drag(self):
        if not self.history_drag_context:
            return
        mime, point = self.history_drag_context
        bar = self.history.verticalScrollBar()
        delta = -1 if point.y() < 24 else 1
        bar.setValue(bar.value() + delta * max(1, bar.singleStep()))
        try:
            component, items, index, ordered = self.history_drop_plan(mime, point)
            self.show_history_drop_indicator(component, items, ordered)
        except (ValueError, TypeError, KeyError, AttributeError):
            self.finish_history_drag()

    def show_history_drop_indicator(self, component, items, ordered):
        moving = {obj.Name for obj in items}
        visible = [name for name in ordered if not model().background_result(component.Document.getObject(name))]
        first = next(i for i, name in enumerate(visible) if name in moving)
        following = next((name for name in visible[first:] if name not in moving), None)
        rows = [self.history.topLevelItem(i) for i in range(self.history.topLevelItemCount())]
        row = next((row for row in rows if row.data(0, QtCore.Qt.UserRole) == (component.Document.Name, following)), None)
        y = self.history.visualItemRect(row).top() if row else self.history.visualItemRect(rows[-1]).bottom()
        self.history_drop_indicator.setGeometry(0, y, self.history.viewport().width(), 2)
        self.history_drop_indicator.show()

    def history_drop_plan(self, mime, point):
        if not mime.hasFormat(self.HISTORY_MIME) or Gui.Control.activeDialog():
            raise ValueError(tr("Drop history items from the active component."))
        payload = json.loads(bytes(mime.data(self.HISTORY_MIME)))
        component = resolve(self.active_key)
        if (tuple(payload["component"]) != self.active_key or payload["id"] != component.ObjectId
                or component.Document.HasPendingTransaction):
            raise ValueError(tr("Drop history items from the active component after finishing its edit."))
        items = [component.Document.getObject(name) for name, identifier in payload["items"]]
        if any(obj is None or obj.ObjectId != identifier for obj, (name, identifier) in zip(items, payload["items"])):
            raise ValueError(tr("The dragged history items have changed. Select them again."))
        visible = [obj for obj in model().history(component) if not is_origin(obj) and not model().background_result(obj)]
        row = self.history.itemAt(point)
        if row:
            obj = resolve(row.data(0, QtCore.Qt.UserRole))
            index = (visible.index(obj) + (point.y() > self.history.visualItemRect(row).center().y())) if obj in visible else 0
        else:
            index = len(visible)
        ordered = model().history_move_order(component, items, index)
        return component, items, index, ordered

    def history_drag_event(self, event):
        point = event.position().toPoint() if hasattr(event, "position") else event.pos()
        try:
            component, items, index, ordered = self.history_drop_plan(event.mimeData(), point)
        except (ValueError, TypeError, KeyError, AttributeError):
            self.finish_history_drag()
            event.ignore()
            return True
        if event.type() == QtCore.QEvent.Drop:
            self.finish_history_drag()
            # Defer the row rebuild until Qt has finished dispatching the drop.
            keys = [(object_key(obj), obj.ObjectId) for obj in items]
            component_key = object_key(component)
            component_id = component.ObjectId
            def commit():
                if self.active_key != component_key or Gui.Control.activeDialog():
                    return
                current = resolve(component_key)
                objects = [resolve(key) for key, identifier in keys]
                if (current is None or current.ObjectId != component_id
                        or any(obj is None or obj.ObjectId != identifier for obj, (key, identifier) in zip(objects, keys))):
                    return
                model().reorder_history(current, objects, index)
            QtCore.QTimer.singleShot(0, lambda: self.run(commit))
        else:
            self.show_history_drop_indicator(component, items, ordered)
            if point.y() < 24 or point.y() > self.history.viewport().height() - 24:
                mime = QtCore.QMimeData()
                mime.setData(self.HISTORY_MIME, event.mimeData().data(self.HISTORY_MIME))
                self.history_drag_context = mime, point
                self.history_scroll_timer.start()
            else:
                self.history_scroll_timer.stop()
                self.history_drag_context = None
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()
        return True

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
        root = self.tree_root(rows[0])
        if any(self.tree_root(row) != root for row in rows):
            raise ValueError(tr("Cut instances from one component assembly at a time."))
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
        item = (self.structure.topLevelItem(0) if position == QtWidgets.QAbstractItemView.OnViewport
                else item or self.structure.currentItem() or self.structure.topLevelItem(0))
        root = self.tree_root(item)
        if (payload.get("root") != root.ObjectId
                or payload.get("document") != model().metadata(root.Document).ObjectId):
            raise ValueError(tr("Move parts within the same Part Tree and owning file."))
        paths = [tuple(value["path"]) for value in payload["items"]]
        if any(model()._path(root, path)[-1].ObjectId != value["id"]
               for path, value in zip(paths, payload["items"])):
            raise ValueError(tr("The cut selection changed; select and cut it again."))
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
            if object_key(root) == self.root_key and tuple(self.active_path[:len(path)]) == path:
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

    def delete_models(self):
        rows = self.models.selectedItems()
        if len(rows) != 1 or not rows[0].data(0, QtCore.Qt.UserRole):
            raise ValueError(tr("Select one domestic component definition to delete."))
        self.delete_model(rows[0].data(0, QtCore.Qt.UserRole))

    def delete_model(self, key):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before deleting a component."))
        component = resolve(key)
        unused = self.unused_edit()
        context = resolve(unused["file_root"] if unused else self.root_key)
        if not model().is_component(component) or context is None or component.Document != context.Document:
            raise ValueError(tr("Open the defining file before deleting an external component."))
        doc = component.Document
        if doc.HasPendingTransaction:
            raise ValueError(tr("Finish the active edit before deleting a component."))
        model().definition_deletion_plan(component)
        key = object_key(component)
        root = model().metadata(doc).RootComponent
        root_key = object_key(root)
        # Release temporary scenes before their native providers are removed.
        for entry in list(self.unused_views):
            if entry["key"] == key:
                self.end_unused_edit(entry["window"])
        views = [entry for entry in self.component_views if entry["key"] == key]
        windows = list(self.mdi.subWindowList())
        file_window = next((window for window in windows
                            if tuple(window.property("ComponentKey") or ()) == root_key), None)
        if views and file_window is None:
            before = list(self.mdi.subWindowList())
            Gui.getDocument(doc.Name).createView("Gui::View3DInventor")
            file_window = next(window for window in self.mdi.subWindowList() if window not in before)
            self.mdi.setActiveSubWindow(file_window)
            self.set_document(doc)
        for entry in views:
            window = entry.get("window")
            self.clear_context_view(window)
            entry["snapshot"].setLink(None)
            if window in self.mdi.subWindowList():
                window.close()
            if entry in self.component_views:
                self.component_views.remove(entry)
        if file_window is not None:
            self.mdi.setActiveSubWindow(file_window)
            self.set_document(doc)
        Gui.Selection.clearSelection()
        model().delete_definition(component)
        self.refresh()

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

    def move_components(self, item=None):
        from freecad.gui.MoveComponentsTask import open_task
        rows = self.structure.selectedItems() if item is None or item.isSelected() else [item]
        roots = {self.tree_root(row) for row in rows}
        if len(roots) != 1:
            raise ValueError(tr("Choose component instances in one Part Tree."))
        paths = [tuple(ids) for row in rows for key, ids in self.members(row)]
        open_task(roots.pop(), paths)

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
        entries = Gui.Selection.getSelectionEx("*", 0)
        roots = model().tree_roots(root.Document)
        if root not in roots:
            roots.append(root)
        picks = [(context, pick) for context in roots for pick in Selection.selected(context, entries)]
        self.selecting = True
        try:
            # Reveal a precise pick through grouped instances. An ambiguous bare
            # definition selection must never choose an arbitrary occurrence.
            changed = False
            for context, pick in picks:
                prefix, component = [], context
                for link in model()._path(context, pick.ids):
                    peers = [child for child in model().children(component)
                             if child.LinkedObject == link.LinkedObject]
                    group = (object_key(context), tuple(prefix), object_key(link.LinkedObject))
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
            for context, pick in picks:
                model_rows = QtWidgets.QTreeWidgetItemIterator(self.models)
                while model_rows.value():
                    row = model_rows.value()
                    if row.data(0, QtCore.Qt.UserRole) == object_key(pick.component):
                        row.setSelected(True)
                    model_rows += 1
                matches = []
                iterator = QtWidgets.QTreeWidgetItemIterator(self.structure)
                while iterator.value():
                    row = iterator.value()
                    if self.tree_root(row) == context and any(
                            value and tuple(value[1]) == pick.ids for value in self.members(row)):
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
            unused = self.unused_edit(window)
            view = unused["view"] if unused else Gui.getDocument(root.Document.Name).activeView()
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
        root_key = object_key(self.tree_root(item))
        unused = self.unused_edit()
        if unused and root_key != unused["key"]:
            self.end_unused_edit()
        if root_key != self.root_key:
            self.open_component_tab(root_key)
        root = resolve(root_key)
        root.Visibility = True
        for depth in range(1, len(value[1]) + 1):
            ids = value[1][:depth]
            link = model()._path(root, ids)[-1]
            link.Visibility = True
            if model().representation(root, ids) == "Hidden":
                model().set_representation(root, ids, "Bodies Only")
        model().activate(obj, strict=False)
        unused = self.unused_edit()
        display_root = resolve(unused["file_root"]) if unused else root
        App.setActiveDocument(display_root.Document.Name)
        self.root_key, self.active_key, self.active_path = root_key, object_key(obj), list(value[1])
        window = self.mdi.activeSubWindow() if self.mdi else None
        if window:
            remembered = dict(window.property("ComponentEditPaths") or {})
            remembered[obj.ObjectId] = list(self.active_path)
            window.setProperty("ComponentEditPaths", remembered)
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
                # Undo may restore this window's saved master context. An explicit
                # Models/open request must reopen the requested definition view.
                entry["window"].setProperty("ComponentKey", object_key(obj))
                entry["window"].setProperty("ComponentActiveKey", object_key(obj))
                entry["window"].setProperty("ComponentActivePath", [])
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
        from pivy import coin
        scene = coin.SoSeparator()
        selection = coin.SoSeparator()
        selection.addChild(snapshot.RootNode)
        scene.addChild(selection)
        view.getViewer().setSceneGraph(scene)
        view.setActiveObject("part", obj)
        entry = {"key": object_key(obj), "view": view, "snapshot": snapshot,
                 "scene": scene, "selection": selection}
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

    def insert_model(self, key):
        active = resolve(self.active_key)
        definition = resolve(key)
        if definition not in model().available_definitions(active.Document):
            raise ValueError(tr("Import the component's file into the active component's defining file before adding it."))
        return model().add_component(active, definition)

    def import_component_file(self, document=None):
        document = document or resolve(self.active_key).Document
        if not document.FileName.lower().endswith(".cadprt"):
            raise ValueError(tr("Save the defining file as .cadprt before importing another file."))
        path, unused = QtWidgets.QFileDialog.getOpenFileName(self, tr("Import Component File"), "", "Component document (*.cadprt)")
        if not path:
            return
        context = TaskContext(resolve(self.active_key))
        try:
            import CadDocument
            source = CadDocument.open(path)
            model().import_file(document, source)
            return source
        finally:
            context.restore()

    def locate_import(self, key):
        path, unused = QtWidgets.QFileDialog.getOpenFileName(self, tr("Locate Component File"), "", "Component document (*.cadprt)")
        if path:
            context = TaskContext(resolve(self.active_key))
            try:
                model().repair_file_import(resolve(key), path)
            finally:
                context.restore()

    def new_component(self, document=None, open_editor=True):
        active = resolve(self.active_key)
        document = document or active.Document
        if Gui.Control.activeDialog() or document.HasPendingTransaction:
            raise ValueError(tr("Finish the current edit before creating a component."))
        choices = [tr("Domestic — current defining file"), tr("External — new file"),
                   tr("External — existing file")]
        choice, ok = QtWidgets.QInputDialog.getItem(self, tr("New Component"), tr("Store component in"), choices, 0, False)
        if not ok:
            return
        index = choices.index(choice)
        if index and not document.FileName.lower().endswith(".cadprt"):
            raise ValueError(tr("Save the defining file as .cadprt before creating an external component."))
        context = TaskContext(active)
        created_document = None
        try:
            destination = document
            filename = None
            if index == 1:
                filename, unused = QtWidgets.QFileDialog.getSaveFileName(self, tr("New Component File"), "", "Component document (*.cadprt)")
                if not filename:
                    return
                filename = str(Path(filename).with_suffix(".cadprt"))
                if Path(filename).exists():
                    raise ValueError(tr("Choose a new file, or use the existing-file storage option."))
            elif index == 2:
                filename, unused = QtWidgets.QFileDialog.getOpenFileName(self, tr("Existing Component File"), "", "Component document (*.cadprt)")
                if not filename:
                    return
                import CadDocument
                destination = CadDocument.open(filename)
                if destination == document:
                    raise ValueError(tr("Use domestic storage for the current defining file."))
                model()._check_file_import(document, destination)
                if destination.HasPendingTransaction:
                    raise ValueError(tr("Finish editing the destination file first."))
            name, ok = QtWidgets.QInputDialog.getText(self, tr("New Component"), tr("Component name"),
                                                     text=model().next_part_label(destination))
            if not ok:
                return
            name = str(name).strip()
            if not name:
                raise ValueError(tr("Enter a component name."))
            if index != 1:
                name = model().definition_label(destination, name)
            if index == 1:
                created_document = model().new_document(name)
                destination = created_document
                definition = model().metadata(destination).RootComponent
                model().ensure_file_container(destination)
                destination.clearUndos()
                destination.saveAs(filename)
            else:
                definition = model().create_definition(destination, name)
                if index == 2:
                    try:
                        destination.save()
                    except Exception:
                        destination.undo()
                        raise
            if index:
                model().import_file(document, destination)
        except Exception:
            if created_document and not created_document.FileName:
                App.closeDocument(created_document.Name)
            raise
        finally:
            context.restore()
        if open_editor:
            self.open_component_tab(object_key(definition))
        return definition

    def add_component(self, parent_key=None):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before adding a component."))
        active = resolve(parent_key or self.active_key)
        if getattr(active, "ComponentRole", "") == "Occurrence":
            active = active.LinkedObject
        if not model().is_component(active):
            raise ValueError(tr("Select a resolved component to add to."))
        choices = [d for d in model().available_definitions(active.Document)
                   if d != active and not model()._reachable(d, active)]
        labels = [tr("New component…"), tr("Import component file…")] + [model().component_label(d, active.Document) for d in choices]
        selected, ok = QtWidgets.QInputDialog.getItem(self, tr("Add Component"), tr("Component"), labels, 0, False)
        if not ok:
            return
        index = labels.index(selected)
        if index == 0:
            definition = self.new_component(active.Document, open_editor=False)
        elif index == 1:
            source = self.import_component_file(active.Document)
            if source is None:
                return
            choices = model().definitions(source)
            labels = [model().component_label(d, active.Document) for d in choices]
            selected, ok = QtWidgets.QInputDialog.getItem(self, tr("Add Component"), tr("Component"), labels, 0, False)
            if not ok:
                return  # The explicit file import remains available in Models.
            definition = choices[labels.index(selected)]
        else:
            definition = choices[index - 2]
        if definition:
            return model().add_component(active, definition)

    def copy_domestic(self, key):
        source = resolve(key)
        if getattr(source, "ComponentRole", "") == "Occurrence":
            source = source.LinkedObject
        document = resolve(self.root_key).Document
        name, ok = QtWidgets.QInputDialog.getText(self, tr("Copy to Domestic Components"), tr("Component name"),
                                                 text=source.Label + " copy")
        if not ok:
            return
        copy = model().copy_definition(source, document, name)
        occurrences = [link for definition in model().definitions(document) for link in model().children(definition)
                       if link.LinkedObject == source]
        if not occurrences:
            return copy
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(tr("Replace with Domestic Copy"))
        layout = QtWidgets.QVBoxLayout(dialog)
        notice = QtWidgets.QLabel(tr("The domestic copy is independent. Select placements to replace; leave unchecked to keep their existing definition."))
        notice.setWordWrap(True)
        layout.addWidget(notice)
        listing = QtWidgets.QListWidget()
        for link in occurrences:
            row = QtWidgets.QListWidgetItem(model().owner(link).Label + " / " + source.Label + " #" + str(link.InstanceNumber))
            row.setData(QtCore.Qt.UserRole, object_key(link))
            row.setFlags(row.flags() | QtCore.Qt.ItemIsUserCheckable)
            row.setCheckState(QtCore.Qt.Unchecked)
            listing.addItem(row)
        layout.addWidget(listing)
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            selected = [resolve(listing.item(i).data(QtCore.Qt.UserRole)) for i in range(listing.count())
                        if listing.item(i).checkState() == QtCore.Qt.Checked]
            model().replace_instances(source, copy, selected)
        return copy

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
        source = resolve(key)
        if getattr(source, "ComponentRole", "") == "Occurrence":
            source = source.LinkedObject
        filename, unused = QtWidgets.QFileDialog.getSaveFileName(self, tr("Copy to External File"), "", "Component document (*.cadprt)")
        if not filename:
            return
        filename = str(Path(filename).with_suffix(".cadprt"))
        if Path(filename).exists():
            raise ValueError(tr("Choose a new file for this independent copy."))
        context = TaskContext(resolve(self.active_key))
        try:
            model().copy_to_external_file(source, filename)
        finally:
            context.restore()

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
        if any(getattr(obj, "Legacy" + family + "State", "")
               for family in model().RETAINED_OPERATION_FAMILIES):
            component = model().owner(obj)
            source = model().retained_operation_source(obj)
            if source is None:
                raise ValueError(tr("Repair the retained native input before editing it."))
            context = TaskContext(component)
            context.enter()
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(source)
            context.edit(source)
            return
        if getattr(obj, "ComponentRole", "") == "Reference":
            context = TaskContext(model().owner(obj))
            try:
                context.enter(obj)
                context.monitor.stop()  # The reference picker is a modal dialog.
                self.edit_reference(key)
            finally:
                context.restore()
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
            context = TaskContext(component)
            try:
                context.enter(obj)
                CommandCreateBom().Activated(obj)
            except Exception:
                context.restore()
                raise
        elif obj.isDerivedFrom("PartDesign::Plane"):
            from freecad.gui.ComponentPlaneTask import launch
            launch(operation=obj)
        elif getattr(obj, "OperationKind", "") == "Extrude":
            from freecad.gui.ComponentExtrudeTask import launch
            launch(operation=obj)
        elif getattr(obj, "OperationKind", "") == "Primitive":
            from freecad.gui.ComponentPrimitiveTask import launch
            launch(operation=obj)
        elif getattr(obj, "OperationKind", "") == "Helix":
            from freecad.gui.ComponentHelixTask import launch
            launch(operation=obj)
        elif getattr(obj, "OperationKind", "") == "Pipe":
            from freecad.gui.ComponentPipeTask import launch
            launch(operation=obj)
        elif getattr(obj, "OperationKind", "") == "Loft":
            from freecad.gui.ComponentLoftTask import launch
            launch(operation=obj)
        elif getattr(obj, "OperationKind", "") == "Revolve":
            from freecad.gui.ComponentRevolveTask import launch
            launch(operation=obj)
        else:
            context = TaskContext(component)
            context.enter()
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
            context.edit(obj)

    def rename_item(self, key):
        obj = resolve(key)
        current = obj.Document.Label if model().is_file_container(obj) else obj.Label
        name, ok = QtWidgets.QInputDialog.getText(self, tr("Rename"), tr("Name"), text=current)
        if ok and name.strip() and name.strip() != current:
            with model().transaction(obj.Document, "Rename"):
                if model().is_file_container(obj):
                    obj.Document.Label = name.strip()
                else:
                    obj.Label = (model().definition_label(obj.Document, name, obj)
                                 if model().is_component(obj) else name.strip())

    def add_instance(self, key):
        occurrence = resolve(key)
        if not model().is_component(occurrence.LinkedObject):
            raise ValueError(tr("Locate the missing component file before adding an instance."))
        model().add_component(model().owner(occurrence), occurrence.LinkedObject,
                              placement=App.Placement(occurrence.LinkPlacement))

    def copy_part(self, key):
        if Gui.Control.activeDialog():
            raise ValueError(tr("Finish the current task before copying a component."))
        return self.copy_domestic(key)

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

    def file_grounding_target(self, item):
        """Grounding belongs to a file occurrence, never its shared definition."""
        root = resolve(self.root_key) if self.root_key else None
        if (root is None or not model().is_file_container(root)
                or self.active_key != self.root_key or self.unused_edit()
                or App.ActiveDocument != root.Document):
            raise ValueError(tr("Edit the file before changing assembly grounding."))
        if Gui.Control.activeDialog() or root.Document.HasPendingTransaction:
            raise ValueError(tr("Finish the current task before changing assembly grounding."))
        rows = self.structure.selectedItems() if item.isSelected() else [item]
        members = self.members(item)
        if (len(rows) != 1 or len(members) != 1 or not members[0]
                or len(members[0][1]) != 1 or self.tree_root(item) != root):
            raise ValueError(tr("Select one top-level occurrence. Expand grouped instances first."))
        occurrence = resolve(members[0][0])
        if occurrence not in model().children(root):
            raise ValueError(tr("The occurrence changed. Select it again."))
        return occurrence

    def set_file_grounding(self, item, grounded):
        occurrence = self.file_grounding_target(item)
        # Register the native engine/view providers without switching workbenches or tabs.
        import AssemblyGui  # noqa: F401
        if grounded:
            model().ground_occurrence(occurrence)
        else:
            record = model().assembly_record(occurrence.Document)
            joints = [occurrence.Document.getObject(entry["object"])
                      for entry in record["joints"]] if record else []
            grounds = [joint for joint in joints if getattr(joint, "ObjectToGround", None) == occurrence]
            model().remove_relationships(occurrence.Document, grounds)

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
            if item and item.data(0, QtCore.Qt.UserRole):
                key = item.data(0, QtCore.Qt.UserRole)
                menu.addAction(tr("Edit"), lambda: self.run(lambda: self.edit_model(target())))
                menu.addAction(tr("Open in new window"), lambda: self.run(lambda: self.open_component_tab(key)))
                menu.addAction(tr("Rename"), lambda: self.run(lambda: self.rename_item(key)))
                menu.addAction(tr("Delete component"), lambda: self.run(lambda: self.delete_model(key)))
                menu.addAction(tr("Add Instance"), lambda: self.run(
                    lambda: self.insert_model(key)))
                if resolve(key).Document != root.Document:
                    menu.addAction(tr("Copy to Domestic Components"), lambda: self.run(lambda: self.copy_domestic(key)))
            elif item:
                file_key = item.data(0, QtCore.Qt.UserRole + 3)
                record = resolve(file_key)
                if record and getattr(record, "ComponentRole", "") == "FileImport":
                    menu.addAction(tr("Locate Component File"), lambda: self.run(lambda: self.locate_import(file_key)))
            menu.addAction(tr("New Component"), lambda: self.run(self.new_component))
            menu.addAction(tr("Import Component File"), lambda: self.run(self.import_component_file))
            menu.addAction(tr("Add Component"), lambda: self.run(self.add_component))
            return menu
        if tree == self.structure and item:
            value = item.data(0, QtCore.Qt.UserRole)
            if not value:
                return menu
            obj = resolve(value[0])
            definition = obj.LinkedObject if getattr(obj, "ComponentRole", "") == "Occurrence" else obj
            menu.addAction(tr("Edit"), lambda: self.run(lambda: self.activate_item(target()))).setEnabled(definition is not None)
            unused = self.unused_edit()
            if unused and not value[1] and object_key(definition) == unused["key"]:
                menu.addAction(tr("Open in new window"), lambda: self.run(lambda: self.open_component_tab(value[0])))
                return menu
            if value[1]:
                assembly = model().assembly_context(obj.Document)
                grounded = bool(assembly and any(
                    getattr(joint, "ObjectToGround", None) == obj
                    for group in assembly.Group if group.isDerivedFrom("Assembly::JointGroup")
                    for joint in group.Group))
                action = menu.addAction(tr("Unground component") if grounded else tr("Ground component"),
                    lambda checked=False, grounded=grounded:
                        self.run(lambda: self.set_file_grounding(target(), not grounded)))
                action.setObjectName("fileUngroundOccurrence" if grounded else "fileGroundOccurrence")
                action.setToolTip(tr("Fix this occurrence at its current position in the file. Shared component definitions are unchanged."))
                try:
                    self.file_grounding_target(item)
                except ValueError as exc:
                    action.setEnabled(False)
                    action.setToolTip(str(exc))
            if value[1]:
                menu.addAction(tr("Cut"), lambda: self.run(lambda: self.cut_instances(target())))
                menu.addAction(tr("Move Components"), lambda: self.run(lambda: self.move_components(target())))
            paste = menu.addAction(tr("Paste"), lambda: self.run(lambda: self.paste_instances(target())))
            paste.setEnabled(definition is not None and QtWidgets.QApplication.clipboard().mimeData().hasFormat(PartTree.MIME))
            if value[1]:
                menu.addAction(tr("Delete Instance") if len(self.members(item)) == 1 else tr("Delete Instances"),
                               lambda: self.run(lambda: self.delete_instances(target())))
            menu.addAction(tr("Add Component"), lambda: self.run(lambda: self.add_component(value[0]))).setEnabled(definition is not None)
            if definition:
                menu.addAction(tr("Rename"), lambda: self.run(lambda: self.rename_item(object_key(definition))))
            if value[1]:
                menu.addAction(tr("Open in new window"), lambda: self.run(lambda: self.open_component_tab(value[0]))).setEnabled(definition is not None)
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
                externalize = menu.addAction(tr("Copy to External File"), lambda: self.run(lambda: self.externalize_component(value[0])))
                externalize.setEnabled(definition is not None and definition.Document == obj.Document)
                externalize.setToolTip(tr("Create an independent component file. Existing definitions and placements are retained."))
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
            modes = {model().representation(self.tree_root(item), ids) for ids in paths} if definition else set()
            overrides = model().representation_overrides(self.tree_root(item), [])
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
            if self.active_key and not model().is_file_container(resolve(self.active_key)):
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
        if prop in ("Label", "Group", "ModelHistory", "ResultObjects", "Representation", "RepresentationOverrides", "ResultStatus", "Shape", "Visibility", "UserSuppressed", "ReferenceError", "LinkedObject", "Source", "DocumentId", "IncludeInBOM", "Transparency", "ShapeAppearance", "OverrideMaterial"):
            self.timer.start(100)

    def slotDeletedObject(self, obj):
        self.timer.start(100)

    def slotDeletedDocument(self, doc):
        name = getattr(doc, "Document", doc).Name
        # Closed MDI widgets can await deferred destruction. Their document names
        # may already be reused; never reuse those views for a new document.
        self.component_views = [entry for entry in self.component_views if entry["key"][0] != name]
        for entry in list(self.context_views):
            if entry["document"] == name:
                self.clear_context_view(entry["window"], restore=False)
        for entry in list(self.unused_views):
            if entry["file_root"][0] == name:
                self.discard_unused_edit(entry)
            elif entry["key"][0] == name:
                self.end_unused_edit(entry["window"])
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
    component = active_component(allow_file=True)
    panel = _dock or show(component.Document)
    panel.run(lambda: panel.add_component(object_key(component)))


def show(doc=None, edit_path=None):
    global _dock
    if _dock is None:
        _dock = Navigator()
        Gui.getMainWindow().addDockWidget(QtCore.Qt.LeftDockWidgetArea, _dock)
    if doc:
        _dock.set_document(doc, edit_path)
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
        self.saved_state = App.ParamGet("User parameter:BaseApp/Preferences/MainWindow").GetString("MainWindowState", "")
        # Register the named custom dock before native window-state restoration.
        show()
        window.installEventFilter(self)
        if window.isVisible():
            QtCore.QTimer.singleShot(0, self.apply)

    def eventFilter(self, watched, event):
        if watched is self.window and event.type() == QtCore.QEvent.Show:
            self.apply()
        return False

    def apply(self):
        if self.applied:
            return
        self.applied = True
        self.window.removeEventFilter(self)
        panel = _dock
        install_start_actions()
        saved = self.saved_state
        attributes = self.window.findChild(QtWidgets.QDockWidget, "Model")
        if not saved:
            panel.setFloating(False)
            self.window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, panel)
        if attributes and not saved:
            attributes.setFloating(False)
            self.window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, attributes)
            self.window.splitDockWidget(panel, attributes, QtCore.Qt.Vertical)
            attributes.show()
            # Size only after Qt has laid out the newly separated docks.
            QtCore.QTimer.singleShot(0, self.size_panels)
        if not saved:
            tasks = self.window.findChild(QtWidgets.QDockWidget, "Tasks")
            if tasks:
                tasks.setFloating(False)
                self.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, tasks)
                tasks.show()
        show_recent_files()

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


def show_recent_files():
    """Reuse the native Start MDI view, presenting only its recent-file cards."""
    window = Gui.getMainWindow()
    view = window.findChild(QtWidgets.QWidget, "StartView")
    if view is None:
        # Do not take focus away from a file opened by command-line/startup scripts.
        if App.ActiveDocument:
            return
        try:
            import StartGui
        except ImportError:
            App.Console.PrintWarning(tr("Recent files requires the Start module. Enable BUILD_START for the next build.") + "\n")
            return
        Gui.runCommand("Start_Start")
        view = window.findChild(QtWidgets.QWidget, "StartView")
    if view is not None and not App.ActiveDocument:
        mdi = window.findChild(QtWidgets.QMdiArea)
        if mdi:
            for sub in mdi.subWindowList():
                if sub.isAncestorOf(view):
                    mdi.setActiveSubWindow(sub)
                    break
    if view is None or view.property("PlusRecentFilesOnly"):
        return
    contents = view.findChild(QtWidgets.QStackedWidget)
    recent = next((cards for cards in view.findChildren(QtWidgets.QListView)
                   if cards.model() and cards.model().metaObject().className()
                   == "Start::RecentFilesModel"), None)
    if contents is None or recent is None:
        return
    # The upstream Documents page contains the recent heading/cards, creation
    # row, examples and optional custom-folder cards in one content layout.
    # Keep the native parent wrapper alive while accessing its layout. A
    # temporary parentWidget() wrapper can invalidate the returned PySide layout.
    cards_parent = recent.parentWidget()
    layout = cards_parent.layout()
    heading = layout.itemAt(layout.indexOf(recent) - 1).widget()
    for index in range(layout.count()):
        widget = layout.itemAt(index).widget()
        if widget and widget not in (heading, recent):
            widget.hide()
    documents = contents.widget(1)
    for widget in documents.findChildren(QtWidgets.QPushButton) + documents.findChildren(QtWidgets.QCheckBox):
        widget.hide()
    contents.setCurrentWidget(documents)
    empty = QtWidgets.QLabel(tr("No recent files."), cards_parent)
    empty.setObjectName("RecentFilesEmpty")
    layout.insertWidget(layout.indexOf(recent) + 1, empty)

    def update_empty():
        has_files = recent.model().rowCount() > 0
        heading.show()
        recent.setVisible(has_files)
        empty.setVisible(not has_files)

    # Run after the native refresh finishes setting heading/card visibility.
    empty_timer = QtCore.QTimer(view)
    empty_timer.setSingleShot(True)
    empty_timer.timeout.connect(update_empty)

    def queue_empty_update():
        empty_timer.start(0)

    recent.model().modelReset.connect(queue_empty_update)
    recent.model().rowsInserted.connect(queue_empty_update)
    recent.model().rowsRemoved.connect(queue_empty_update)
    update_empty()
    # StartView is a native MDI subclass exposed as QWidget. Retain its wrapper
    # on the main window, not only on itself, until native MDI ownership closes it.
    window._plus_recent_widgets = (view, contents, cards_parent, layout, heading, recent, empty, empty_timer)
    view.setProperty("PlusRecentFilesOnly", True)


class StartActionButton(QtWidgets.QToolButton):
    def __init__(self, caption, parent):
        self.caption = tr(caption)
        super().__init__(parent)
        self.setAccessibleName(self.caption)

    def actionEvent(self, event):
        super().actionEvent(event)
        self.setText(self.caption)


class StartActions(QtCore.QObject):
    """Idle Design actions alongside, without replacing, native task watchers."""
    DESIGN = {"NoneWorkbench", "PartDesignWorkbench", "PartWorkbench",
              "SketcherWorkbench", "SurfaceWorkbench", "MeshWorkbench"}
    FILE = (("Std_New", "New File"), ("Std_Open", "Open"))
    COMPONENT = (("PartDesign_NewSketch", "New Sketch"),
                 ("Part_CoordinateSystem", "Coordinate System"),
                 ("Std_ComponentDatumPlane", "Datum Plane"), ("Std_Part", "Add Component"))

    def __init__(self, window):
        super().__init__(window)
        from freecad.gui.ComponentSketchTask import install_datum_command
        install_datum_command()
        self.window = window
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(150)
        self.refresh()

    def refresh(self):
        doc = App.ActiveDocument
        component_doc = bool(doc and any(
            getattr(obj, "ComponentRole", "") == "Document" for obj in doc.Objects))
        design = Gui.activeWorkbench().name() in self.DESIGN
        choices = self.FILE if doc is None else self.COMPONENT
        eligible = doc is None or (design and component_doc)
        if eligible and doc and any(not Gui.Command.get(name) for name, caption in self.COMPONENT):
            # Load existing command implementations, without switching workbenches.
            import PartGui
            import PartDesignGui
        for view in self.window.findChildren(QtWidgets.QStackedWidget):
            if view.metaObject().className() != "Gui::TaskView::TaskView":
                continue
            idle = view.widget(0)
            pane = idle.findChild(QtWidgets.QWidget, "ComponentStartActions",
                                  QtCore.Qt.FindDirectChildrenOnly)
            scroll = idle.findChild(QtWidgets.QScrollArea)
            if not pane:
                if not eligible:
                    continue
                pane = QtWidgets.QWidget(idle)
                pane.setObjectName("ComponentStartActions")
                layout = QtWidgets.QVBoxLayout(pane)
                layout.setContentsMargins(12, 12, 12, 12)
                for command, caption in self.FILE + self.COMPONENT:
                    actions = Gui.Command.get(command)
                    if not actions:
                        continue
                    for action in actions.getAction()[:1]:
                        button = StartActionButton(caption, pane)
                        button.setObjectName(command)
                        button.setDefaultAction(action)
                        button.setText(tr(caption))
                        button.setAccessibleName(tr(caption))
                        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
                        button.setIconSize(QtCore.QSize(24, 24))
                        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Fixed)
                        if command == "Std_New":
                            button.clicked.connect(lambda: Gui.activateWorkbench("PartDesignWorkbench"))
                        layout.addWidget(button)
                layout.addStretch()
                idle.layout().insertWidget(0, pane, 1)
            # PartDesign commands may load only after the first file is created.
            names = {command for command, caption in choices}
            missing = eligible and any(not pane.findChild(QtWidgets.QToolButton, name)
                                       for name in names)
            if missing:
                idle.layout().removeWidget(pane)
                pane.setObjectName("")
                pane.hide()
                pane.deleteLater()
                continue
            for button in pane.findChildren(QtWidgets.QToolButton):
                button.setVisible(button.objectName() in names)
            pane.setVisible(eligible)
            if scroll:
                scroll.setVisible(not eligible)
            state = ("file" if doc is None else "component:" + doc.Name) if eligible else ""
            if eligible and pane.property("StartActionState") != state and not Gui.Control.activeDialog():
                dock = view.parentWidget()
                if isinstance(dock, QtWidgets.QDockWidget):
                    dock.show()
            pane.setProperty("StartActionState", state)


def install_start_actions():
    global _start_actions
    if _start_actions is None:
        _start_actions = StartActions(Gui.getMainWindow())


def delete_selected_instances():
    """Std_Delete adapter for guarded definitions and precise occurrence picks."""
    if _dock is None or Gui.Control.activeDialog() or not _dock.root_key:
        return False
    entries = Gui.Selection.getSelectionEx("*", 0)
    # Remove permanent datum selections before native Delete, including precise
    # occurrence paths that select their component root in the native tree.
    root = resolve(_dock.root_key)
    roots = model().tree_roots(root.Document) if root else []
    if root and root not in roots:
        roots.append(root)
    for entry in entries:
        for subname in entry.SubElementNames or [""]:
            picks = [pick for context in roots for pick in Selection.resolve(context, entry.Object, subname)]
            if ((model().is_file_container(entry.Object) and not subname)
                    or protected_origin_item(entry.Object)
                    or any(protected_origin_item(pick.item) for pick in picks)):
                Gui.Selection.removeSelection(entry.DocumentName, entry.ObjectName, subname)
    entries = Gui.Selection.getSelectionEx("*", 0)
    definitions = [entry for entry in entries
                   if model().is_component(entry.Object) and not entry.SubElementNames]
    if definitions:
        # Consume the selection even on refusal; never fall through to native deletion.
        Gui.Selection.clearSelection()
        def delete_definition_selection():
            if len(entries) != 1:
                raise ValueError(tr("Select one component definition to delete."))
            _dock.delete_model(object_key(definitions[0].Object))
        _dock.run(delete_definition_selection)
        return True
    if not entries:
        return False
    picks = [(context, pick) for context in roots for pick in Selection.selected(context, entries)]
    if not picks or any(not pick.ids or pick.item is not None for context, pick in picks):
        return False
    occurrences = list(dict.fromkeys(model()._path(context, pick.ids)[-1] for context, pick in picks))
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
        doc = model().new_file_document() if self.create else App.ActiveDocument
        root = model().metadata(doc).RootComponent
        initial = [model().children(root)[0].ObjectId] if self.create else []
        show(doc, initial)


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


class NewComponentCommand:
    def GetResources(self):
        return {"MenuText": tr("New Component"),
                "ToolTip": tr("Create a domestic or external component and open its defining file for editing"),
                "Pixmap": "Geofeaturegroup.svg"}

    def IsActive(self):
        if Gui.Control.activeDialog():
            return False
        try:
            from freecad.gui.ComponentExtrudeTask import active_component
            component = active_component(allow_file=True)
            return model().is_component(component) and not component.Document.HasPendingTransaction
        except (ValueError, NameError):
            return False

    def Activated(self):
        from freecad.gui.ComponentExtrudeTask import active_component
        component = active_component(allow_file=True)
        panel = _dock or show(component.Document)

        def create():
            definition = panel.new_component(component.Document)
            if definition is None:
                return
            panel.refresh()
            panel.tabs.setCurrentWidget(panel.history)
        panel.run(create)


def registerCommands():
    Gui.addCommand("Std_NewComponentDocument", Command(True))
    Gui.addCommand("Std_ComponentStructure", Command())
    Gui.addCommand("Std_NewComponent", NewComponentCommand())
    Gui.addCommand("PartDesign_AddReferenceObject", AddReferenceCommand())
    install_startup_layout()
