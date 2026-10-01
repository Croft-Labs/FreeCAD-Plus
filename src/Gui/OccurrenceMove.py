# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit one-time movement of an unconstrained native occurrence."""
import math
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve
from freecad.gui.UniqueDefinition import selected_occurrence


def tr(text):
    return App.Qt.translate("OccurrenceMove", text)


def parent_frame(link):
    parent = link.getParentGeoFeatureGroup()
    current = parent
    while current:
        if current.TypeId != "App::Part":
            raise ValueError(tr("Only structural Part containers are supported around this occurrence."))
        current = current.getParentGeoFeatureGroup()
    return parent.getGlobalPlacement() if parent else App.Placement()


def review(link):
    from BasicShapes.ShapeReferences import require_current, linked_shape
    if (link.TypeId != "App::Link" or link.ElementCount or link.Scale != 1
            or tuple(link.ScaleVector) != (1, 1, 1)):
        raise ValueError(tr("Select a whole unscaled native Link, not an array or source definition."))
    source = link.LinkedObject
    if source is None or source.Document != link.Document or not source.isDerivedFrom("Part::Feature"):
        raise ValueError(tr("This move supports a direct same-document link to a Part solid or Body."))
    if (link.ExpressionEngine or any(obj.TypeId != "App::Part" for obj in link.InList)
            or "ReadOnly" in link.getPropertyStatus("LinkPlacement")
            or "ReadOnly" in link.getPropertyStatus("Placement")):
        raise ValueError(tr("Driven, read-only or consumed occurrences require their relationship workflow."))
    require_current(link)
    parent = parent_frame(link)
    shape = linked_shape((link, []))
    if shape.isNull() or not shape.isValid() or not shape.Solids:
        raise ValueError(tr("The occurrence needs current valid solid geometry."))
    return {"link": identity(link), "source": identity(source), "shape": source.Shape.hashCode(),
            "parent": tuple(parent.toMatrix().A), "placement": tuple(link.LinkPlacement.toMatrix().A),
            "transform": link.LinkTransform}


def candidate(link, expected, mode, frame, vector, angle=0., pivot=(0., 0., 0.)):
    from BasicShapes.ShapeReferences import linked_shape
    if review(link) != expected:
        raise ValueError(tr("The occurrence or its frame changed. Review again."))
    if mode not in ("Translate", "Rotate") or frame not in ("World", "Occurrence"):
        raise ValueError(tr("Choose a move type and coordinate frame."))
    if len(vector) != 3 or len(pivot) != 3 or not all(math.isfinite(v) for v in (*vector, angle, *pivot)):
        raise ValueError(tr("Enter finite coordinates and angle."))
    parent = parent_frame(link)
    world = parent.multiply(link.LinkPlacement)
    direction = App.Vector(*vector)
    if frame == "Occurrence":
        direction = world.Rotation.multVec(direction)
    if mode == "Translate":
        target = App.Placement(world)
        target.Base = world.Base + direction
    else:
        if direction.Length < 1e-12:
            raise ValueError(tr("The rotation axis must be nonzero."))
        center = App.Vector(*pivot)
        if frame == "Occurrence":
            center = world.multVec(center)
        rotation = App.Placement(App.Vector(), App.Rotation(direction, angle), center)
        target = rotation.multiply(world)
    shape = linked_shape((link, []))
    shape.transformShape(target.multiply(world.inverse()).toMatrix())
    return parent.inverse().multiply(target), shape, target


def move(link, expected, mode, frame, vector, angle=0., pivot=(0., 0., 0.)):
    if App.ActiveDocument != link.Document or Gui.Control.activeDialog() or link.Document.HasPendingTransaction:
        raise ValueError(tr("Activate this document and finish the current task or edit transaction."))
    placement, shape, world = candidate(link, expected, mode, frame, vector, angle, pivot)
    if placement.isSame(link.LinkPlacement, 1e-9):
        return False
    doc = link.Document
    doc.openTransaction("Move occurrence once")
    try:
        link.LinkPlacement = placement
        doc.recompute()
        review(link)
        doc.commitTransaction()
        return True
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


class Ghost:
    """A non-pickable, view-owned overlay; never a document object or transaction."""
    def __init__(self, shape):
        from pivy import coin
        view = Gui.activeDocument().activeView()
        self.root = view.getSceneGraph()
        self.node = coin.SoSeparator()
        pick = coin.SoPickStyle()
        pick.style = coin.SoPickStyle.UNPICKABLE
        pick.setOverride(True)
        style = coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.LINES
        style.lineWidth = 2
        style.setOverride(True)
        material = coin.SoMaterial()
        material.diffuseColor = (0., 0.85, 0.8)
        material.setOverride(True)
        stream = coin.SoInput()
        stream.setBuffer(shape.writeInventor())
        geometry = coin.SoDB.readAll(stream)
        if geometry is None:
            raise ValueError(tr("Could not prepare the move preview."))
        for node in (pick, style, material, geometry):
            self.node.addChild(node)
        self.root.addChild(self.node)

    def remove(self):
        if self.root.findChild(self.node) >= 0:
            self.root.removeChild(self.node)


class MoveDialog(QtWidgets.QDialog):
    def __init__(self, link, parent=None):
        super().__init__(parent)
        self.key, self.doc = identity(link), link.Document
        self.closed = self.saving = False
        self.expected = self.ghost = None
        self.setWindowTitle(tr("Move occurrence once"))
        self.resize(660, 480)
        layout = QtWidgets.QVBoxLayout(self)
        self.summary = QtWidgets.QLabel(link.Label + " [" + link.Name + "]")
        self.summary.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.summary)
        form = QtWidgets.QFormLayout()
        self.mode = QtWidgets.QComboBox()
        self.mode.addItems(["Translate", "Rotate"])
        self.frame = QtWidgets.QComboBox()
        self.frame.addItems(["World", "Occurrence"])
        form.addRow(tr("Move type"), self.mode)
        form.addRow(tr("Coordinate frame"), self.frame)
        def coordinates(label):
            row = QtWidgets.QWidget()
            fields = []
            line = QtWidgets.QHBoxLayout(row)
            line.setContentsMargins(0, 0, 0, 0)
            for axis in ("X", "Y", "Z"):
                line.addWidget(QtWidgets.QLabel(axis))
                field = QtWidgets.QDoubleSpinBox()
                field.setRange(-1e6, 1e6)
                field.setDecimals(4)
                line.addWidget(field)
                fields.append(field)
            form.addRow(label, row)
            return fields
        self.offset = coordinates(tr("Translation (mm)"))
        self.axis = coordinates(tr("Rotation axis"))
        self.axis[2].setValue(1)
        self.pivot = coordinates(tr("Pivot coordinates (mm)"))
        self.angle = QtWidgets.QDoubleSpinBox()
        self.angle.setRange(-360, 360)
        self.angle.setSuffix(" °")
        self.angle.setDecimals(3)
        form.addRow(tr("Rotation angle"), self.angle)
        layout.addLayout(form)
        note = QtWidgets.QLabel(tr(
            "Offsets are incremental. Rotation uses the typed axis and pivot in the chosen frame. "
            "Occurrence axes use this link's current orientation within its parent containers. "
            "The teal wireframe previews the result; original geometry stays visible. Move once "
            "changes only this placement in one Undo step. It creates no mate or persistent "
            "relationship. Cancel removes the preview without changing the model."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.message = QtWidgets.QLabel()
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setWordWrap(True)
        layout.addWidget(self.message)
        buttons = QtWidgets.QHBoxLayout()
        self.reviewButton = QtWidgets.QPushButton(tr("Review again"))
        self.previewButton = QtWidgets.QPushButton(tr("Preview"))
        self.moveButton = QtWidgets.QPushButton(tr("Move once"))
        cancel = QtWidgets.QPushButton(tr("Cancel"))
        for button in (self.reviewButton, self.previewButton, self.moveButton, cancel):
            button.setAutoDefault(False)
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.reviewButton.clicked.connect(self.refresh)
        self.previewButton.clicked.connect(self.preview)
        self.moveButton.clicked.connect(self.commit)
        cancel.clicked.connect(self.reject)
        self.mode.currentIndexChanged.connect(self.fieldsChanged)
        self.frame.currentIndexChanged.connect(self.clearGhost)
        for field in self.offset + self.axis + self.pivot + [self.angle]:
            field.valueChanged.connect(self.clearGhost)
        self.fieldsChanged()
        self.refresh()
        App.addDocumentObserver(self)

    def clearGhost(self, *args):
        if self.ghost is not None:
            self.ghost.remove()
            self.ghost = None
            self.message.setText(tr("Preview cleared. Preview again to inspect the current values."))

    def fieldsChanged(self):
        self.clearGhost()
        rotation = self.mode.currentText() == "Rotate"
        for field in self.offset:
            field.setEnabled(not rotation)
        for field in self.axis + self.pivot + [self.angle]:
            field.setEnabled(rotation)

    def values(self):
        rotation = self.mode.currentText() == "Rotate"
        return (self.mode.currentText(), self.frame.currentText(),
                tuple(field.value() for field in (self.axis if rotation else self.offset)),
                self.angle.value(), tuple(field.value() for field in self.pivot))

    def refresh(self):
        self.clearGhost()
        self.expected = None
        try:
            self.expected = review(resolve(self.key))
            self.message.setText(tr("Ready. Preview or move using the explicit frame and values."))
        except Exception as error:
            self.message.setText(str(error))
        self.previewButton.setEnabled(self.expected is not None)
        self.moveButton.setEnabled(self.expected is not None)

    def preview(self):
        self.clearGhost()
        try:
            link = resolve(self.key)
            if App.ActiveDocument != self.doc:
                raise ValueError(tr("Activate this document before previewing."))
            placement, shape, world = candidate(link, self.expected, *self.values())
            self.ghost = Ghost(shape)
            self.message.setText(tr("Preview origin in world mm: ") +
                                 ", ".join("{:.4f}".format(value) for value in world.Base))
        except Exception as error:
            self.message.setText(str(error))

    def commit(self):
        self.saving = True
        try:
            move(resolve(self.key), self.expected, *self.values())
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
            self.moveButton.setEnabled(False)
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


class CommandMove:
    def GetResources(self):
        return {"MenuText": tr("Move occurrence once..."),
                "ToolTip": tr("Translate or rotate one unconstrained occurrence in world or occurrence axes")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        try:
            link = selected_occurrence()
        except ValueError as error:
            QtWidgets.QMessageBox.information(Gui.getMainWindow(), tr("Move occurrence once"), str(error))
            return
        dialog = MoveDialog(link, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Std_MoveOccurrenceOnce", CommandMove())
