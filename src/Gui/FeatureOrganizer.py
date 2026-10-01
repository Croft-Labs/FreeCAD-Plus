# SPDX-License-Identifier: LGPL-2.1-or-later
"""Search native document metadata and edit labels/descriptions without reordering."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve

LIMIT = 2000


def tr(text):
    return App.Qt.translate("FeatureOrganizer", text)


def record(obj):
    return {"key": identity(obj), "label": obj.Label, "description": obj.Label2,
            "type": obj.TypeId}


def state_record(obj):
    """Native loaded-object snapshot; no geometry evaluation or reference loading."""
    states = list(obj.State)
    flags = set()
    view = obj.ViewObject
    visible = bool(view.Visibility) if view is not None else None
    if visible is False:
        flags.add("hidden")
    suppression = tr("Not supported")
    if "Suppressed" in obj.PropertiesList and obj.getTypeIdOfProperty("Suppressed") == "App::PropertyBool":
        suppression = tr("Suppressed") if obj.Suppressed else tr("Not suppressed")
        if obj.Suppressed:
            flags.add("suppressed")
    if "Invalid" in states:
        flags.add("error")
    if "Touched" in states or "Recompute" in states or "Recompute2" in states:
        flags.add("stale")
    readonly = any("ReadOnly" in obj.getPropertyStatus(prop) for prop in ("Label", "Label2"))
    if readonly:
        flags.add("readonly")
    source = obj
    linked = obj.isDerivedFrom("App::Link")
    if linked:
        source = obj.LinkedObject
        if isinstance(source, tuple):
            source = source[0]
        if source is None:
            flags.add("unresolved")
    if source is None:
        source_text = tr("Unresolved link")
        source_doc = None
    else:
        source_doc = source.Document.Name
        source_text = (tr("Linked source: ") if linked else tr("Local: ")) + source_doc + "#" + source.Name
        source_text += "\n" + (source.Document.FileName or tr("Unsaved document"))
    status = (tr("Error") if "error" in flags else
              tr("Needs recompute") if "stale" in flags else tr("No native error"))
    if "unresolved" in flags:
        status = tr("Unresolved link")
    return {"visibility": tr("Visible flag") if visible else tr("Hidden flag") if visible is False else tr("No view"),
            "suppression": suppression, "status": status,
            "detail": obj.getStatusString() + " | " + ", ".join(states),
            "source": source_text, "source_doc": source_doc, "flags": flags,
            "metadata": tr("Read-only") if readonly else tr("Editable")}


class _ViewObserver:
    def __init__(self, dialog):
        self.dialog = dialog

    def slotChangedObject(self, view, prop):
        if prop != "Visibility" or self.dialog.closed:
            return
        try:
            doc = view.Object.Document
        except Exception:
            # Native view providers can notify before attachment or during teardown.
            return
        if doc.Name in self.dialog.watched:
            self.dialog.invalidate()


def matches(row, query, type_id=""):
    text = " ".join((row["key"][1], row["label"], row["description"], row["type"])).casefold()
    return (not type_id or row["type"] == type_id) and all(
        term in text for term in query.casefold().split())


def apply_metadata(doc, expected, label, description):
    if App.ActiveDocument != doc or Gui.Control.activeDialog() or doc.HasPendingTransaction:
        raise ValueError(tr("Activate this document and finish the current task or edit transaction."))
    obj = resolve(expected["key"])
    if obj.Document != doc or record(obj) != expected:
        raise ValueError(tr("The object or metadata changed. Refresh before applying."))
    if not label.strip() or "\x00" in label + description:
        raise ValueError(tr("Enter a nonempty label and text without null characters."))
    for prop in ("Label", "Label2"):
        if "ReadOnly" in obj.getPropertyStatus(prop):
            raise ValueError(tr("This object's metadata is read-only."))
    if (label, description) == (obj.Label, obj.Label2):
        return False
    doc.openTransaction("Edit feature metadata")
    try:
        obj.Label = label
        obj.Label2 = description
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        raise
    return True


class OrganizerDialog(QtWidgets.QDialog):
    def __init__(self, doc, parent=None):
        super().__init__(parent)
        self.doc = doc
        self.rows = []
        self.states = {}
        self.watched = {doc.Name}
        self.fresh = False
        self.saving = False
        self.closed = False
        self.setWindowTitle(tr("Find and describe features"))
        self.resize(1200, 720)
        layout = QtWidgets.QVBoxLayout(self)
        self.scope = QtWidgets.QLabel()
        self.scope.setTextFormat(QtCore.Qt.PlainText)
        self.scope.setWordWrap(True)
        layout.addWidget(self.scope)
        controls = QtWidgets.QHBoxLayout()
        self.query = QtWidgets.QLineEdit()
        self.query.setPlaceholderText(tr("Search label, internal name, type or description"))
        self.query.setAccessibleName(tr("Search features"))
        self.types = QtWidgets.QComboBox()
        self.types.setAccessibleName(tr("Feature type"))
        self.stateFilter = QtWidgets.QComboBox()
        self.stateFilter.setAccessibleName(tr("Native object state"))
        for title, key in ((tr("All states"), ""), (tr("Errors"), "error"),
                           (tr("Needs recompute"), "stale"), (tr("Hidden flag"), "hidden"),
                           (tr("Suppressed"), "suppressed"), (tr("Unresolved links"), "unresolved"),
                           (tr("Read-only metadata"), "readonly")):
            self.stateFilter.addItem(title, key)
        self.columnsButton = QtWidgets.QToolButton()
        self.columnsButton.setText(tr("Columns"))
        self.columnsButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.columnsMenu = QtWidgets.QMenu(self.columnsButton)
        self.columnsButton.setMenu(self.columnsMenu)
        self.refreshButton = QtWidgets.QPushButton(tr("Refresh"))
        for widget in (self.query, self.types, self.stateFilter, self.columnsButton, self.refreshButton):
            controls.addWidget(widget)
        layout.addLayout(controls)
        self.table = QtWidgets.QTreeWidget()
        self.table.setHeaderLabels([tr("Label"), tr("Internal name"), tr("Type"), tr("Description"),
                                    tr("Visibility"), tr("Suppression"), tr("Native state"),
                                    tr("Source"), tr("Metadata access")])
        for column in range(4, 9):
            action = self.columnsMenu.addAction(self.table.headerItem().text(column))
            action.setCheckable(True)
            action.setChecked(True)
            action.toggled.connect(lambda checked, col=column: self.table.setColumnHidden(col, not checked))
        self.table.setRootIsDecorated(False)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        layout.addWidget(self.table)
        self.count = QtWidgets.QLabel()
        layout.addWidget(self.count)
        self.stateDetails = QtWidgets.QLabel()
        self.stateDetails.setTextFormat(QtCore.Qt.PlainText)
        self.stateDetails.setWordWrap(True)
        self.stateDetails.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        layout.addWidget(self.stateDetails)
        form = QtWidgets.QFormLayout()
        self.label = QtWidgets.QLineEdit()
        self.description = QtWidgets.QPlainTextEdit()
        self.description.setMaximumHeight(100)
        form.addRow(tr("Label"), self.label)
        form.addRow(tr("Description"), self.description)
        layout.addLayout(form)
        note = QtWidgets.QLabel(tr(
            "Edits affect only the selected object's native label and description. "
            "Links keep their own metadata; their shared source is not edited. "
            "State columns are read-only snapshots. Visibility flags do not account for hidden parents. "
            "No native error does not certify geometry; unresolved links are not loaded by this tool. "
            "Sorting changes this list only. Refresh or changing rows discards unapplied text. "
            "Apply creates one Undo step; Close discards only unapplied text."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.message = QtWidgets.QLabel()
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setWordWrap(True)
        layout.addWidget(self.message)
        actions = QtWidgets.QHBoxLayout()
        self.selectButton = QtWidgets.QPushButton(tr("Select in model"))
        self.applyButton = QtWidgets.QPushButton(tr("Apply metadata"))
        close = QtWidgets.QPushButton(tr("Close"))
        for button in (self.selectButton, self.applyButton, close):
            actions.addWidget(button)
        layout.addLayout(actions)
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setAutoDefault(False)
        self.query.textChanged.connect(self.filterRows)
        self.types.currentIndexChanged.connect(self.filterRows)
        self.stateFilter.currentIndexChanged.connect(self.filterRows)
        self.table.itemSelectionChanged.connect(self.showRow)
        self.refreshButton.clicked.connect(self.refresh)
        self.selectButton.clicked.connect(self.selectRow)
        self.applyButton.clicked.connect(self.commit)
        close.clicked.connect(self.reject)
        self.refresh()
        App.addDocumentObserver(self)
        self.viewObserver = _ViewObserver(self)
        Gui.addDocumentObserver(self.viewObserver)

    def refresh(self):
        selected_type = self.types.currentData()
        objects = self.doc.Objects
        self.rows = [record(obj) for obj in objects[:LIMIT]]
        self.states = {identity(obj): state_record(obj) for obj in objects[:LIMIT]}
        self.watched = {self.doc.Name} | {state["source_doc"] for state in self.states.values() if state["source_doc"]}
        self.scope.setText(tr("Document: ") + self.doc.Label + " [" + self.doc.Name + "]" +
                           (tr(" — Partial search: only the first 2000 loaded objects are included.")
                            if len(objects) > LIMIT else tr(" — All loaded objects in this document.")))
        self.types.blockSignals(True)
        self.types.clear()
        self.types.addItem(tr("All types"), "")
        for type_id in sorted({row["type"] for row in self.rows}):
            self.types.addItem(type_id, type_id)
        self.types.setCurrentIndex(max(0, self.types.findData(selected_type)))
        self.types.blockSignals(False)
        self.fresh = True
        self.filterRows()
        self.message.setText(tr("Select a row to review or edit its metadata. Searching does not change the model."))

    def filterRows(self, *args):
        self.table.clear()
        if self.fresh:
            for row in self.rows:
                state = self.states[row["key"]]
                wanted = self.stateFilter.currentData()
                if (matches(row, self.query.text(), self.types.currentData())
                        and (not wanted or wanted in state["flags"])):
                    item = QtWidgets.QTreeWidgetItem([
                        row["label"], row["key"][1], row["type"], row["description"],
                        state["visibility"], state["suppression"], state["status"],
                        state["source"].split("\n")[0], state["metadata"]])
                    item.setData(0, QtCore.Qt.UserRole, row)
                    item.setToolTip(3, row["description"])
                    item.setToolTip(6, state["detail"])
                    item.setToolTip(7, state["source"])
                    self.table.addTopLevelItem(item)
        self.count.setText(tr("Matching objects: ") + str(self.table.topLevelItemCount()))
        for column in range(3):
            self.table.resizeColumnToContents(column)
        for column, width in ((3, 160), (4, 100), (5, 125), (6, 145), (7, 180), (8, 115)):
            self.table.setColumnWidth(column, width)
        self.showRow()

    def currentRow(self):
        item = self.table.currentItem()
        return item.data(0, QtCore.Qt.UserRole) if item and self.fresh else None

    def showRow(self):
        row = self.currentRow()
        for widget in (self.label, self.description, self.applyButton, self.selectButton):
            widget.setEnabled(row is not None)
        state = self.states[row["key"]] if row else None
        self.stateDetails.setText((state["status"] + ": " + state["detail"] + "\n" + state["source"]) if state else "")
        if state and "readonly" in state["flags"]:
            self.applyButton.setEnabled(False)
        self.label.setText(row["label"] if row else "")
        self.description.setPlainText(row["description"] if row else "")

    def selectRow(self):
        try:
            if Gui.Control.activeDialog() or App.ActiveDocument != self.doc:
                raise ValueError(tr("Activate this document and finish the current task before selecting."))
            row = self.currentRow()
            if row is None:
                return
            obj = resolve(row["key"])
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
            self.message.setText(tr("Selected in the model. Visibility is unchanged."))
        except Exception as error:
            self.message.setText(str(error))

    def commit(self):
        row = self.currentRow()
        if row is None:
            return
        self.saving = True
        try:
            changed = apply_metadata(self.doc, row, self.label.text(), self.description.toPlainText())
            self.refresh()
            self.message.setText(tr("Metadata saved. Undo restores the previous values.") if changed
                                 else tr("Metadata is unchanged; no Undo step was added."))
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.saving = False

    def invalidate(self):
        if not self.saving and not self.closed:
            self.fresh = False
            self.filterRows()
            self.message.setText(tr("The document or display state changed. Refresh to inspect current state and metadata."))

    def slotChangedObject(self, obj, prop):
        if obj.Document.Name in self.watched:
            self.invalidate()

    def slotCreatedObject(self, obj):
        if obj.Document.Name in self.watched:
            self.invalidate()

    def slotDeletedObject(self, obj):
        if obj.Document.Name in self.watched:
            self.invalidate()

    def slotRecomputedDocument(self, doc):
        if doc.Name in self.watched:
            self.invalidate()

    def slotUndoDocument(self, doc):
        self.slotRecomputedDocument(doc)

    def slotRedoDocument(self, doc):
        self.slotRecomputedDocument(doc)

    def slotFinishSaveDocument(self, doc, filename):
        self.slotRecomputedDocument(doc)

    def slotChangePropertyEditor(self, obj, prop):
        if prop not in ("Label", "Label2"):
            return
        doc = getattr(obj, "Document", None)
        if getattr(doc, "Name", None) in self.watched:
            self.invalidate()

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()
        elif doc.Name in self.watched:
            self.invalidate()

    def done(self, result):
        if not self.closed:
            self.closed = True
            App.removeDocumentObserver(self)
            Gui.removeDocumentObserver(self.viewObserver)
        super().done(result)


_dialogs = []


class CommandOrganizer:
    def GetResources(self):
        return {"MenuText": tr("Find and describe features..."),
                "ToolTip": tr("Search document labels, types and descriptions; edit native metadata")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        if not self.IsActive():
            return
        dialog = OrganizerDialog(App.ActiveDocument, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Std_FeatureOrganizer", CommandOrganizer())
