# SPDX-License-Identifier: LGPL-2.1-or-later
"""Expose native deferred recompute and bounded dependency status without a new engine."""
from collections import deque
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve


def tr(text):
    return App.Qt.translate("DocumentUpdates", text)


def snapshot(doc, limit=2000):
    """Inspect local objects and loaded input dependencies; never recompute or clear flags."""
    local = list(doc.Objects)
    if len(local) > limit:
        raise ValueError(tr("This inspector supports at most 2000 objects including loaded inputs."))
    objects = {identity(obj): obj for obj in local}
    pending = deque(local)
    inputs = {}
    consumers = {}
    while pending:
        obj = pending.popleft()
        key = identity(obj)
        inputs[key] = []
        for dep in obj.OutList:
            target = identity(dep)
            inputs[key].append(target)
            consumers.setdefault(target, []).append(key)
            if target not in objects:
                if len(objects) >= limit:
                    raise ValueError(tr("This inspector supports at most 2000 objects including loaded inputs."))
                objects[target] = dep
                pending.append(dep)
    failures = {key for key, obj in objects.items() if "Invalid" in obj.State}
    touched = {key for key, obj in objects.items() if "Touched" in obj.State}
    causes = {}
    # Native input errors are evidence, not a claim that every error has one unique cause.
    for seed in sorted(failures) + sorted(touched - failures):
        todo = deque(consumers.get(seed, ()))
        visited = {seed}
        while todo:
            key = todo.popleft()
            if key in visited:
                continue
            visited.add(key)
            causes.setdefault(key, seed)
            todo.extend(consumers.get(key, ()))
    rows = []
    for obj in local:
        key = identity(obj)
        if key not in failures and key not in touched and key not in causes:
            continue
        state = tr("Failed") if key in failures else tr("Pending") if key in touched else tr("Affected by input")
        cause = objects.get(causes.get(key))
        rows.append({"key": key, "label": obj.Label, "state": state,
                     "native": obj.getStatusString(),
                     "cause": identity(cause) if cause else None,
                     "input": (cause.Document.Name + "." + cause.Name) if cause else ""})
    rows.sort(key=lambda row: (0 if row["key"] in failures else 1, row["key"][1]))
    return {"rows": rows, "failed": sum(identity(obj) in failures for obj in local),
            "pending": sum(identity(obj) in touched for obj in local),
            "deferred": doc.RecomputesFrozen}


def context(doc):
    if App.listDocuments().get(doc.Name) != doc or App.ActiveDocument != doc:
        raise ValueError(tr("Activate this document before changing its update settings."))
    if Gui.Control.activeDialog() or doc.HasPendingTransaction:
        raise ValueError(tr("Finish the active task or edit transaction first."))


def set_deferred(doc, value):
    context(doc)
    doc.RecomputesFrozen = bool(value)


def recompute_now(doc):
    context(doc)
    snapshot(doc)  # Do not start an unreviewable oversized update from this bounded tool.
    # Force bypasses native SkipRecompute for this explicit action only. Cycle checking
    # is mandatory. No extra transaction is opened, preserving the owner's Undo/Redo.
    doc.recompute(None, True, True)
    return snapshot(doc)


class UpdatesDialog(QtWidgets.QDialog):
    def __init__(self, doc, parent=None):
        super().__init__(parent)
        self.doc = doc
        self.closed = False
        self.busy = False
        self.rows = []
        self.setWindowTitle(tr("Document updates"))
        self.resize(850, 450)
        layout = QtWidgets.QVBoxLayout(self)
        self.summary = QtWidgets.QLabel()
        self.summary.setTextFormat(QtCore.Qt.PlainText)
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)
        self.deferred = QtWidgets.QCheckBox(tr("Defer normal document recomputes (native Skip Recomputes)"))
        self.deferred.clicked.connect(self.changeMode)
        layout.addWidget(self.deferred)
        self.table = QtWidgets.QTreeWidget()
        self.table.setHeaderLabels([tr("Object"), tr("Status"), tr("Affected by input"), tr("Native detail")])
        self.table.setRootIsDecorated(False)
        layout.addWidget(self.table)
        note = QtWidgets.QLabel(tr(
            "Cached shapes can remain visible while updates are pending or failed. Recompute now "
            "updates this document once, even when deferred, and keeps the chosen mode. Native "
            "edit previews may still update individual objects. Re-enabling normal updates does "
            "not itself recompute. Close retains the session setting; it is not a saved model property. "
            "Drawing/background-render completion and unloaded external inputs are not certified here."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.message = QtWidgets.QLabel()
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setWordWrap(True)
        layout.addWidget(self.message)
        actions = QtWidgets.QHBoxLayout()
        self.refreshButton = QtWidgets.QPushButton(tr("Refresh status"))
        self.updateButton = QtWidgets.QPushButton(tr("Recompute now"))
        self.selectButton = QtWidgets.QPushButton(tr("Select object"))
        self.inputButton = QtWidgets.QPushButton(tr("Select affected input"))
        close = QtWidgets.QPushButton(tr("Close"))
        for button in (self.refreshButton, self.updateButton, self.selectButton, self.inputButton, close):
            button.setAutoDefault(False)
            actions.addWidget(button)
        layout.addLayout(actions)
        self.refreshButton.clicked.connect(self.refresh)
        self.updateButton.clicked.connect(self.updateModel)
        self.selectButton.clicked.connect(lambda: self.select(False))
        self.inputButton.clicked.connect(lambda: self.select(True))
        close.clicked.connect(self.reject)
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.refresh)
        self.modeTimer = QtCore.QTimer(self)
        self.modeTimer.timeout.connect(self.syncMode)
        self.modeTimer.start(500)
        self.refresh()
        App.addDocumentObserver(self)

    def syncMode(self):
        if not self.closed:
            self.deferred.setChecked(self.doc.RecomputesFrozen)

    def refresh(self):
        if self.closed or self.busy:
            return
        key = self.table.currentItem().data(0, QtCore.Qt.UserRole) if self.table.currentItem() else None
        self.table.clear()
        self.rows = []
        try:
            data = snapshot(self.doc)
            self.rows = data["rows"]
            self.syncMode()
            self.summary.setText(self.doc.Label + " [" + self.doc.Name + "] — " +
                                 tr("Failed: ") + str(data["failed"]) + tr("; pending: ") +
                                 str(data["pending"]) + tr("; affected objects listed: ") + str(len(self.rows)))
            for row in self.rows:
                item = QtWidgets.QTreeWidgetItem([row["label"] + " [" + row["key"][1] + "]",
                                                 row["state"], row["input"], row["native"]])
                item.setData(0, QtCore.Qt.UserRole, row["key"])
                self.table.addTopLevelItem(item)
                if row["key"] == key:
                    self.table.setCurrentItem(item)
            for column in range(3):
                self.table.resizeColumnToContents(column)
            self.updateButton.setEnabled(True)
            self.message.setText(tr("Inspect failed inputs, repair them using their normal editor, then recompute.")
                                 if self.rows else tr("No native pending/error flags or affected loaded inputs detected."))
        except Exception as error:
            self.updateButton.setEnabled(False)
            self.message.setText(str(error))

    def changeMode(self, value):
        try:
            set_deferred(self.doc, value)
            self.refresh()
        except Exception as error:
            self.syncMode()
            self.message.setText(str(error))

    def updateModel(self):
        self.busy = True
        self.updateButton.setEnabled(False)
        error = None
        try:
            recompute_now(self.doc)
        except Exception as failure:
            error = str(failure)
        finally:
            self.busy = False
        self.refresh()
        if error:
            self.message.setText(error)

    def select(self, affected_input):
        try:
            item = self.table.currentItem()
            row = next((row for row in self.rows if item and row["key"] == item.data(0, QtCore.Qt.UserRole)), None)
            if row is None or (affected_input and not row["cause"]):
                raise ValueError(tr("Select a row with the required object or affected input."))
            obj = resolve(row["cause"] if affected_input else row["key"])
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(obj)
        except Exception as error:
            self.message.setText(str(error))

    def changed(self, doc):
        if not self.closed and not self.busy:
            self.timer.start(100)

    def slotChangedObject(self, obj, prop):
        self.changed(obj.Document)

    def slotCreatedObject(self, obj):
        self.changed(obj.Document)

    def slotDeletedObject(self, obj):
        self.changed(obj.Document)

    def slotRecomputedDocument(self, doc):
        self.changed(doc)

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()
        else:
            self.changed(doc)

    def done(self, result):
        if not self.closed:
            self.closed = True
            self.timer.stop()
            self.modeTimer.stop()
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class CommandUpdates:
    def GetResources(self):
        return {"MenuText": tr("Document updates..."),
                "ToolTip": tr("Inspect pending and failed inputs, defer or explicitly recompute the document")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        dialog = UpdatesDialog(App.ActiveDocument, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Std_DocumentUpdates", CommandUpdates())
