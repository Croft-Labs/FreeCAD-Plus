# SPDX-License-Identifier: LGPL-2.1-or-later
"""Layers task, compact toolbar menus and non-destructive Coin visibility gates."""
import weakref
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from pivy import coin
from freecad.gui import DesignLayers as Layers

_timer = None
_refreshing = False
_bars = weakref.WeakSet()
_panel = None
GATE = "FreeCADPlusLayerGate"


def tr(text):
    return QtCore.QCoreApplication.translate("DesignLayers", text)


class _MetadataView:
    def onDelete(self, view, subelements):
        return False

    def dumps(self):
        return None

    def loads(self, state):
        pass


def gate(view, visible):
    """Gate display branches, leaving native Visibility and mode indices intact.

    The Body's Group branch must remain traversable for independently layered
    sketches. Its own Tip branches and each body operation get their own gate.
    SelectionRoot Group branches are native scene containers, not geometry.
    """
    switch = view.SwitchNode
    for index in range(switch.getNumChildren()):
        child = switch.getChild(index)
        if str(child.getTypeId().getName()) == "SoFCSelectionRoot":
            continue
        if str(child.getName()) != GATE:
            wrapper = coin.SoSwitch()
            wrapper.setName(GATE)
            wrapper.addChild(child)
            switch.replaceChild(index, wrapper)
            child = wrapper
        value = coin.SO_SWITCH_ALL if visible else coin.SO_SWITCH_NONE
        if child.whichChild.getValue() != value:
            child.whichChild = value


def selection(doc):
    objects = []
    for entry in Gui.Selection.getSelectionEx("*", 0):
        for subname in entry.SubElementNames or [""]:
            from freecad.gui.DesignSelection import resolve
            obj, _, _ = resolve(entry.Object, subname)
            # An external definition is edited in its own document, never by
            # implicitly converting a selected occurrence to parent ownership.
            if obj and obj.Document == doc:
                objects.append(obj)
    return Layers.targets(doc, objects)


def refresh():
    global _refreshing
    if _refreshing:
        return
    _refreshing = True
    hidden = False
    try:
        for doc in App.listDocuments().values():
            if doc.Restoring:
                continue
            Layers.initialize(doc)
            meta = Layers.manager(doc)
            if meta and meta.ViewObject and not isinstance(meta.ViewObject.Proxy, _MetadataView):
                meta.ViewObject.Proxy = _MetadataView()
            data = Layers.state(doc)
            hidden = hidden or any(not row["visible"] for row in data["layers"])
            owners = Layers.units(doc)
            for obj in owners:
                if obj.ViewObject:
                    gate(obj.ViewObject, Layers.visible(obj, owners))
        App.ParamGet("User parameter:BaseApp/Preferences/DesignSelection").SetBool("LayerVisibilityActive", hidden)
        for bar in list(_bars):
            bar.refresh()
        if _panel:
            _panel.refresh()
    finally:
        _refreshing = False


def schedule(*args):
    if _timer and not _refreshing:
        _timer.start(0)


class _Observer:
    def slotCreatedDocument(self, doc):
        schedule()

    def slotActivateDocument(self, doc):
        if _panel and (not App.ActiveDocument or App.ActiveDocument.Name != _panel.docname):
            _panel.reject()
        schedule()

    def slotDeletedDocument(self, doc):
        if _panel and _panel.docname == getattr(doc, "Document", doc).Name:
            _panel.reject()
        schedule()

    def slotCreatedObject(self, obj):
        schedule()

    def slotDeletedObject(self, obj):
        schedule()

    def slotChangedObject(self, obj, prop):
        if prop in ("DesignLayerData", "DesignLayer", "Group", "DisplayMode", "DisplayModeBody",
                    "Visibility", "Shape", "Producer", "ConsumedResults", "ComponentRole"):
            schedule()

    def slotUndoDocument(self, doc):
        schedule()

    def slotRedoDocument(self, doc):
        schedule()

    def addSelection(self, *args):
        schedule()

    def removeSelection(self, *args):
        schedule()

    def clearSelection(self, *args):
        schedule()


_observer = _Observer()


def install():
    global _timer
    Layers.install()
    if _timer is None:
        _timer = QtCore.QTimer(Gui.getMainWindow())
        _timer.setSingleShot(True)
        _timer.timeout.connect(refresh)
        App.addDocumentObserver(_observer)
        Gui.addDocumentObserver(_observer)
        Gui.Selection.addObserver(_observer)
        schedule()


def run(callback):
    try:
        callback()
        refresh()
    except (ValueError, RuntimeError, StopIteration) as error:
        text = str(error) or tr("The layer no longer exists. Refresh and try again.")
        Gui.getMainWindow().statusBar().showMessage(text, 10000)
        App.Console.PrintWarning(text + "\n")


class LayersTask:
    def __init__(self, doc):
        self.docname = doc.Name
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("Layers"))
        layout = QtWidgets.QVBoxLayout(self.form)
        self.list = QtWidgets.QTreeWidget()
        self.list.setObjectName("designLayerList")
        self.list.setHeaderLabels([tr("Visible"), tr("Layer")])
        self.list.setRootIsDecorated(False)
        self.list.setColumnWidth(0, 50)
        layout.addWidget(self.list)
        self.list.itemClicked.connect(self.clicked)
        self.list.itemDoubleClicked.connect(lambda item, col: self.apply(Layers.activate, item.data(1, QtCore.Qt.UserRole)))
        self.list.itemSelectionChanged.connect(self.update_buttons)
        self.buttons = {}
        for label, callback in (("Create", self.create), ("Rename", self.rename),
                                ("Delete", self.delete), ("Move selection to layer", self.assign),
                                ("Make active", self.activate)):
            button = QtWidgets.QPushButton(tr(label))
            button.clicked.connect(callback)
            layout.addWidget(button)
            self.buttons[label] = button
        note = QtWidgets.QLabel(tr("Deleting a layer moves its objects to Base. Origins always remain on Base."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.refresh()

    def document(self):
        return App.listDocuments().get(self.docname)

    def chosen(self):
        item = self.list.currentItem()
        return item.data(1, QtCore.Qt.UserRole) if item else None

    def refresh(self):
        doc = self.document()
        if not doc:
            return
        current = self.chosen()
        data = Layers.state(doc)
        self.list.blockSignals(True)
        self.list.clear()
        for row in data["layers"]:
            active = row["id"] == data["active"]
            item = QtWidgets.QTreeWidgetItem(["", ("✓ " if active else "") + row["name"]])
            item.setData(1, QtCore.Qt.UserRole, row["id"])
            item.setData(0, QtCore.Qt.UserRole, row["visible"])
            item.setIcon(0, QtGui.QIcon(":/icons/TreeItemVisible.svg" if row["visible"] else ":/icons/TreeItemInvisible.svg"))
            item.setToolTip(0, tr("Hide layer") if row["visible"] else tr("Show layer"))
            font = item.font(1)
            font.setBold(active)
            item.setFont(1, font)
            self.list.addTopLevelItem(item)
            if row["id"] == (current or data["active"]):
                self.list.setCurrentItem(item)
        self.list.blockSignals(False)
        self.update_buttons()

    def update_buttons(self):
        doc, layer = self.document(), self.chosen()
        for name in ("Rename", "Delete"):
            self.buttons[name].setEnabled(bool(layer and layer != Layers.BASE))
        self.buttons["Make active"].setEnabled(bool(layer))
        self.buttons["Move selection to layer"].setEnabled(bool(doc and layer and selection(doc)))

    def apply(self, fn, *args):
        doc = self.document()
        if doc and doc == App.ActiveDocument:
            run(lambda: fn(doc, *args))

    def clicked(self, item, column):
        if column == 0:
            self.apply(Layers.set_visible, item.data(1, QtCore.Qt.UserRole), not item.data(0, QtCore.Qt.UserRole))

    def create(self):
        name, ok = QtWidgets.QInputDialog.getText(self.form, tr("Create layer"), tr("Name"))
        if ok:
            self.apply(Layers.create, name)

    def rename(self):
        doc, layer = self.document(), self.chosen()
        if doc and layer:
            name = Layers._row(Layers.state(doc), layer)["name"]
            name, ok = QtWidgets.QInputDialog.getText(self.form, tr("Rename layer"), tr("Name"), text=name)
            if ok:
                self.apply(Layers.rename, layer, name)

    def delete(self):
        if self.chosen():
            self.apply(Layers.delete, self.chosen())

    def assign(self):
        doc = self.document()
        if doc and self.chosen():
            self.apply(Layers.move, selection(doc), self.chosen())

    def activate(self):
        if self.chosen():
            self.apply(Layers.activate, self.chosen())

    def getStandardButtons(self):
        value = QtWidgets.QDialogButtonBox.Close
        return getattr(value, "value", value)

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def reject(self):
        global _panel
        if _panel is self:
            _panel = None
            Gui.Control.closeDialog()
        return True


def show():
    global _panel
    if App.ActiveDocument and not Gui.Control.activeDialog():
        Layers.initialize(App.ActiveDocument)
        _panel = LayersTask(App.ActiveDocument)
        Gui.Control.showDialog(_panel)


class LayersToolbar(QtWidgets.QToolBar):
    def __init__(self, window):
        super().__init__(tr("Layers"), window)
        install()
        self.setObjectName("FreeCADPlusLayers")
        self.setMovable(False)
        self.setFloatable(False)
        self.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toggleViewAction().setVisible(False)
        self.open = self.addAction(tr("Layers"))
        self.open.triggered.connect(show)
        self.move = self.menu_button("Move to Layer")
        self.active = self.menu_button("Change Active Layer")
        self.move.menu().aboutToShow.connect(lambda: self.fill(self.move, False))
        self.active.menu().aboutToShow.connect(lambda: self.fill(self.active, True))
        _bars.add(self)
        self.destroyed.connect(lambda: _bars.discard(self))
        self.hide()
        self.refresh()

    def menu_button(self, label):
        button = QtWidgets.QToolButton(self)
        button.setText(tr(label))
        button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        button.setMenu(QtWidgets.QMenu(button))
        self.addWidget(button)
        return button

    def refresh(self):
        doc = App.ActiveDocument
        allowed = bool(doc and not doc.HasPendingTransaction and (not Gui.Control.activeDialog() or _panel))
        self.open.setEnabled(bool(doc and not Gui.Control.activeDialog()))
        self.active.setEnabled(allowed)
        self.move.setEnabled(bool(allowed and selection(doc)))

    def fill(self, button, active):
        menu = button.menu()
        menu.clear()
        doc = App.ActiveDocument
        if not doc:
            return
        Layers.initialize(doc)
        data = Layers.state(doc)
        selected = selection(doc)
        for row in data["layers"]:
            action = menu.addAction(row["name"])
            if active:
                action.setCheckable(True)
                action.setChecked(row["id"] == data["active"])
            action.triggered.connect(lambda checked=False, layer=row["id"]: run(
                lambda: Layers.activate(doc, layer) if active else Layers.move(doc, selected, layer)))

    def set_design_active(self, enabled):
        self.setVisible(enabled)
        if not enabled and _panel:
            _panel.reject()
        if enabled:
            self.refresh()
