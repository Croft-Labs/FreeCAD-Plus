# SPDX-License-Identifier: LGPL-2.1-or-later
"""Replace one unconstrained native solid occurrence without copying its source."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve
from freecad.gui.UniqueDefinition import selected_occurrence
from freecad.gui import OccurrenceAppearance as Appearance
from freecad.gui import OccurrenceMove as Move


def tr(text):
    return App.Qt.translate("OccurrenceReplace", text)


def source_state(source, doc):
    from BasicShapes.ShapeReferences import require_current
    if (source.Document != doc or not source.isDerivedFrom("Part::Feature")
            or source.getParentGeoFeatureGroup() is not None):
        raise ValueError(tr("Choose a root solid or whole root Body in this document."))
    require_current(source)
    shape = source.Shape
    if shape.isNull() or not shape.isValid() or shape.ShapeType != "Solid" or shape.Volume <= 0:
        raise ValueError(tr("The source must have one current valid positive-volume solid."))
    return (identity(source), shape.hashCode(), tuple(source.Placement.toMatrix().A))


def review(link, replacement):
    if link.TypeId != "App::Link" or not hasattr(link.LinkedObject, "Document"):
        raise ValueError(tr("Select a whole direct Link, not an array or a linked face."))
    if link.LinkCopyOnChange != "Disabled":
        raise ValueError(tr("Copy-on-change occurrences require their own replacement workflow."))
    current = Move.review(link)
    source_state(link.LinkedObject, link.Document)
    if replacement == link.LinkedObject:
        raise ValueError(tr("Choose a different source; the current definition is already linked."))
    target = source_state(replacement, link.Document)
    if replacement == link or link in replacement.OutListRecursive:
        raise ValueError(tr("This source depends on the occurrence and would create a cycle."))
    if "ReadOnly" in link.getPropertyStatus("LinkedObject"):
        raise ValueError(tr("This occurrence's source is read-only."))
    return {"occurrence": current, "target": target, "appearance": Appearance.state(link),
            "label": link.Label}


def candidate(link, replacement, expected):
    if review(link, replacement) != expected:
        raise ValueError(tr("The occurrence or replacement changed. Review again."))
    shape = replacement.Shape.copy()
    # Match the native Link contract: include the source's placement only when
    # LinkTransform is set, then apply occurrence and structural-parent placement.
    if not link.LinkTransform:
        shape.Placement = App.Placement()
    world = Move.parent_frame(link).multiply(link.LinkPlacement)
    shape.transformShape(world.toMatrix())
    return shape


def replace(link, replacement, expected):
    if (App.ActiveDocument != link.Document or Gui.Control.activeDialog()
            or link.Document.HasPendingTransaction or App.getActiveTransaction()):
        raise ValueError(tr("Activate this document and finish the current task or edit transaction."))
    candidate(link, replacement, expected)
    doc = link.Document
    placement, transform = App.Placement(link.LinkPlacement), link.LinkTransform
    visible, label = link.Visibility, link.Label
    override = link.ViewObject.OverrideMaterial
    materials = link.ViewObject.ShapeAppearance
    doc.openTransaction("Replace occurrence source")
    try:
        link.setLink(replacement)
        link.LinkTransform = transform
        link.LinkPlacement = placement
        link.Label = label
        link.Visibility = visible
        link.ViewObject.OverrideMaterial = override
        if override:
            link.ViewObject.ShapeAppearance = materials
        doc.recompute()
        Move.review(link)
        if (link.LinkedObject != replacement or not link.LinkPlacement.isSame(placement, 1e-9)
                or link.LinkTransform != transform):
            raise ValueError(tr("The native occurrence did not retain the reviewed placement."))
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


class ReplaceDialog(QtWidgets.QDialog):
    def __init__(self, link, parent=None):
        super().__init__(parent)
        self.key, self.doc = identity(link), link.Document
        self.closed = self.saving = False
        self.expected = self.ghost = None
        self.setWindowTitle(tr("Replace occurrence source"))
        self.resize(680, 390)
        layout = QtWidgets.QVBoxLayout(self)
        self.summary = QtWidgets.QLabel()
        self.summary.setTextFormat(QtCore.Qt.PlainText)
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)
        self.sources = QtWidgets.QComboBox()
        self.sources.setAccessibleName(tr("Replacement source"))
        form = QtWidgets.QFormLayout()
        form.addRow(tr("Replacement source"), self.sources)
        layout.addLayout(form)
        note = QtWidgets.QLabel(tr(
            "Reuses the selected source; no definition is copied. Only this occurrence changes. "
            "Its name, placement, visibility and uniform appearance override stay intact; inherited "
            "appearance follows the new source. The source-placement setting is preserved. "
            "Consumers, joints, scaled links, arrays and external sources are not supported. "
            "Preview is a teal wireframe. Replace commits one Undo step; Cancel changes nothing."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.message = QtWidgets.QLabel()
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setWordWrap(True)
        layout.addWidget(self.message)
        buttons = QtWidgets.QHBoxLayout()
        self.reviewButton = QtWidgets.QPushButton(tr("Review again"))
        self.previewButton = QtWidgets.QPushButton(tr("Preview"))
        self.replaceButton = QtWidgets.QPushButton(tr("Replace"))
        self.cancelButton = QtWidgets.QPushButton(tr("Cancel"))
        for button in (self.reviewButton, self.previewButton, self.replaceButton, self.cancelButton):
            button.setAutoDefault(False)
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.reviewButton.clicked.connect(self.refresh)
        self.previewButton.clicked.connect(self.preview)
        self.replaceButton.clicked.connect(self.commit)
        self.cancelButton.clicked.connect(self.reject)
        self.sources.currentIndexChanged.connect(self.check)
        self.refresh()
        App.addDocumentObserver(self)

    def target(self):
        key = self.sources.currentData()
        if key is None:
            raise ValueError(tr("No other root solid is available. Create or load a replacement in this document."))
        return resolve(key)

    def clearGhost(self):
        if self.ghost is not None:
            self.ghost.remove()
            self.ghost = None

    def refresh(self):
        previous = self.sources.currentData()
        previous = tuple(previous) if previous is not None else None
        self.sources.blockSignals(True)
        self.sources.clear()
        try:
            link = resolve(self.key)
            candidates = [obj for obj in self.doc.Objects if obj != link.LinkedObject
                          and obj.isDerivedFrom("Part::Feature") and obj.getParentGeoFeatureGroup() is None]
            for obj in candidates:
                self.sources.addItem(obj.Label + " [" + obj.Name + "]", identity(obj))
            # QVariant conversion/comparison does not reliably match Python tuples.
            index = next((i for i in range(self.sources.count())
                          if tuple(self.sources.itemData(i)) == previous), -1)
            if index >= 0:
                self.sources.setCurrentIndex(index)
        finally:
            self.sources.blockSignals(False)
        self.check()

    def check(self, *args):
        self.clearGhost()
        self.expected = None
        try:
            link = resolve(self.key)
            replacement = self.target()
            self.expected = review(link, replacement)
            self.summary.setText(tr("Occurrence: ") + link.Label + " [" + link.Name + "]\n" +
                                 tr("Current source: ") + link.LinkedObject.Label + " [" + link.LinkedObject.Name + "]\n" +
                                 tr("Source placement: ") + (tr("Included") if link.LinkTransform else tr("Ignored")))
            self.message.setText(tr("Ready: one occurrence, no dependent features or relationships to remap."))
        except Exception as error:
            self.message.setText(str(error))
        self.previewButton.setEnabled(self.expected is not None)
        self.replaceButton.setEnabled(self.expected is not None)

    def preview(self):
        self.clearGhost()
        try:
            if App.ActiveDocument != self.doc:
                raise ValueError(tr("Activate this document before previewing."))
            shape = candidate(resolve(self.key), self.target(), self.expected)
            self.ghost = Move.Ghost(shape)
            from pivy import coin
            view = Gui.activeDocument().activeView()
            view.getCameraNode().viewAll(view.getSceneGraph(), coin.SbViewportRegion(*view.getSize()))
            self.message.setText(tr("Preview ready. Review the replacement before committing."))
        except Exception as error:
            self.message.setText(str(error))

    def commit(self):
        self.saving = True
        try:
            replace(resolve(self.key), self.target(), self.expected)
            self.accept()
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.saving = False

    def invalidate(self, obj):
        if obj.Document == self.doc and not self.closed and not self.saving:
            self.clearGhost()
            self.expected = None
            self.previewButton.setEnabled(False)
            self.replaceButton.setEnabled(False)
            self.message.setText(tr("The document changed. Recompute if needed, then Review again."))

    def slotChangedObject(self, obj, prop):
        self.invalidate(obj)

    def slotCreatedObject(self, obj):
        self.invalidate(obj)

    def slotDeletedObject(self, obj):
        if identity(obj) == self.key:
            self.reject()
        else:
            self.invalidate(obj)

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def done(self, result):
        if not self.closed:
            self.closed = True
            self.clearGhost()
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class Command:
    def GetResources(self):
        return {"MenuText": tr("Replace occurrence source..."),
                "ToolTip": tr("Replace one unconstrained solid occurrence while retaining its placement")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        try:
            link = selected_occurrence()
            Move.review(link)
        except Exception as error:
            QtWidgets.QMessageBox.information(Gui.getMainWindow(), tr("Replace occurrence source"), str(error))
            return
        dialog = ReplaceDialog(link, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Std_ReplaceOccurrenceSource", Command())
