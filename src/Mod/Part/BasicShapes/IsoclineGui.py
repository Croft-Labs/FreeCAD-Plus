# SPDX-License-Identifier: LGPL-2.1-or-later

"""Complete face/direction/angle selection for new and existing Isocline Curves."""

from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui
from . import Isocline
from .FeatureTask import TaskFeatureViewProvider, DirectionArrow, CurveOverlay
from .ShapeReferences import validate_link, linked_shape, require_current, ReferenceError

translate = App.Qt.translate
ICON = str(Path(__file__).with_name("Isocline.svg"))


class ViewProviderIsocline(TaskFeatureViewProvider):
    icon = ICON
    editLabel = translate("Isocline", "Edit Isocline Curve")

    def makeTask(self, obj):
        return IsoclineTask(obj)


class IsoclineTask:
    def __init__(self, obj):
        self.obj = obj
        self.doc = obj.Document
        self.gui_doc = Gui.getDocument(self.doc.Name)
        self.name = obj.Name
        self.result_visible = obj.ViewObject.Visibility
        self.finished = False
        self.mode = None
        self.visibility = {}
        self.arrow = DirectionArrow(self.gui_doc.activeView())
        self.curveHighlight = CurveOverlay(self.gui_doc.activeView())
        self.form = QtGui.QWidget()
        self.form.setObjectName("isoclineTask")
        self.form.setWindowTitle(translate("Isocline", "Isocline Curve"))
        self.form.setWindowIcon(QtGui.QIcon(ICON))
        layout = QtGui.QVBoxLayout(self.form)
        group = QtGui.QGroupBox(translate("Isocline", "Target faces"))
        group.setObjectName("isoclineFacesGroup")
        rows = QtGui.QVBoxLayout(group)
        self.faces = QtGui.QListWidget()
        self.faces.setObjectName("isoclineFaces")
        self.faces.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.faces.setMaximumHeight(120)
        rows.addWidget(self.faces)
        buttons = QtGui.QHBoxLayout()
        self.add = QtGui.QPushButton(translate("Isocline", "Add faces"))
        self.add.setObjectName("isoclineAddFaces")
        self.add.setCheckable(True)
        self.add.clicked.connect(lambda on: self.select("Faces" if on else None))
        remove = QtGui.QPushButton(translate("Isocline", "Remove"))
        remove.setObjectName("isoclineRemoveFaces")
        remove.clicked.connect(self.removeFaces)
        clear = QtGui.QPushButton(translate("Isocline", "Clear"))
        clear.setObjectName("isoclineClearFaces")
        clear.clicked.connect(self.clearFaces)
        for button in (self.add, remove, clear):
            buttons.addWidget(button)
        rows.addLayout(buttons)
        layout.addWidget(group)
        layout.addWidget(QtGui.QLabel(translate("Isocline", "Pull direction")))
        direction_row = QtGui.QHBoxLayout()
        self.direction = QtGui.QComboBox()
        self.direction.setObjectName("isoclineDirection")
        for mode in ("X axis", "Y axis", "Z axis", "Reference", "Custom vector"):
            self.direction.addItem(translate("Isocline", mode), mode)
        self.direction.setCurrentIndex(self.direction.findData(str(obj.DirectionMode)))
        self.direction.currentIndexChanged.connect(self.directionChanged)
        self.reverse = QtGui.QToolButton()
        self.reverse.setObjectName("isoclineReverse")
        self.reverse.setIcon(Gui.getIcon("button_sort"))
        self.reverse.setToolTip(translate("Isocline", "Reverse pull direction"))
        self.reverse.setAccessibleName(translate("Isocline", "Reverse pull direction"))
        self.reverse.setCheckable(True)
        self.reverse.setChecked(obj.Reversed)
        self.reverse.toggled.connect(lambda value: self.change("Reversed", value))
        direction_row.addWidget(self.direction, 1)
        direction_row.addWidget(self.reverse)
        layout.addLayout(direction_row)
        self.reference = QtGui.QWidget()
        ref_layout = QtGui.QVBoxLayout(self.reference)
        ref_layout.setContentsMargins(0, 0, 0, 0)
        self.refName = QtGui.QLineEdit()
        self.refName.setObjectName("isoclineReference")
        self.refName.setReadOnly(True)
        self.refName.setPlaceholderText(
            translate("Isocline", "Plane, planar face, straight edge or axis")
        )
        ref_layout.addWidget(self.refName)
        self.pickRef = QtGui.QPushButton(translate("Isocline", "Select direction reference"))
        self.pickRef.setObjectName("isoclineSelectReference")
        self.pickRef.setCheckable(True)
        self.pickRef.clicked.connect(lambda on: self.select("Reference" if on else None))
        ref_layout.addWidget(self.pickRef)
        layout.addWidget(self.reference)
        self.custom = QtGui.QWidget()
        custom_layout = QtGui.QFormLayout(self.custom)
        self.components = []
        for index, label in enumerate(("X", "Y", "Z")):
            control = QtGui.QDoubleSpinBox()
            control.setObjectName("isoclineVector" + label)
            control.setRange(-1e6, 1e6)
            control.setDecimals(6)
            control.setValue(obj.CustomDirection[index])
            control.valueChanged.connect(self.vectorChanged)
            self.components.append(control)
            custom_layout.addRow(label, control)
        layout.addWidget(self.custom)
        angle_row = QtGui.QFormLayout()
        self.angle = QtGui.QDoubleSpinBox()
        self.angle.setObjectName("isoclineAngle")
        self.angle.setRange(0, 90)
        self.angle.setDecimals(4)
        self.angle.setSuffix(" \u00b0")
        self.angle.setValue(obj.Angle.Value)
        self.angle.valueChanged.connect(lambda value: self.change("Angle", value))
        angle_row.addRow(translate("Isocline", "Draft angle"), self.angle)
        layout.addLayout(angle_row)
        self.preview = QtGui.QCheckBox(translate("Isocline", "Live preview"))
        self.preview.setObjectName("isoclinePreview")
        self.preview.setChecked(True)
        self.preview.toggled.connect(self.updatePreview)
        layout.addWidget(self.preview)
        hint = QtGui.QLabel(
            translate(
                "Isocline",
                "0\u00b0 is the silhouette. Positive draft faces the green pull arrow. Preview also highlights hidden portions.",
            )
        )
        hint.setWordWrap(True)
        layout.addWidget(hint)
        self.status = QtGui.QLabel()
        self.status.setObjectName("isoclineStatus")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        layout.addStretch()
        Gui.Selection.addObserver(self)
        self.refresh()
        self.updatePreview()
        if not obj.Faces:
            self.select("Faces")

    def remember(self, obj):
        if obj and obj.Name not in self.visibility:
            self.visibility[obj.Name] = obj.ViewObject.Visibility

    def restoreVisibility(self):
        for name, visible in self.visibility.items():
            obj = self.doc.getObject(name)
            if obj:
                obj.ViewObject.Visibility = visible

    def entries(self):
        return [(obj, sub) for obj, subs in self.obj.Faces for sub in (subs or [""])]

    def refresh(self):
        self.faces.clear()
        for obj, sub in self.entries():
            self.remember(obj)
            self.faces.addItem(obj.Label + (" : " + sub if sub else " (all faces)"))
        link = self.obj.DirectionReference
        self.refName.setText(
            link[0].Label + (" : " + link[1][0] if link[1] else "") if link else ""
        )
        self.reference.setVisible(self.obj.DirectionMode == "Reference")
        self.custom.setVisible(self.obj.DirectionMode == "Custom vector")

    def select(self, mode):
        self.mode = mode
        for button, name in ((self.add, "Faces"), (self.pickRef, "Reference")):
            blocker = QtCore.QSignalBlocker(button)
            button.setChecked(mode == name)
            del blocker
        Gui.Selection.clearSelection()
        if mode:
            for obj, _ in self.entries():
                self.remember(obj)
                obj.ViewObject.show()
            self.status.setText(
                translate(
                    "Isocline",
                    (
                        "Select target faces."
                        if mode == "Faces"
                        else "Select a direction plane or straight axis."
                    ),
                )
            )
        else:
            self.updatePreview()

    def addSelection(self, document, name, sub, position):
        if self.finished or not self.mode:
            return
        try:
            if document != self.doc.Name:
                raise ValueError("Select an object in this document.")
            obj = self.doc.getObject(name)
            validate_link(self.obj, obj)
            require_current(obj)
            if self.mode == "Reference":
                link = (obj, [sub] if sub else [])
                Isocline.reference_direction(link)
                self.obj.DirectionReference = link
                self.select(None)
            else:
                shape = linked_shape((obj, [sub] if sub else []))
                if not shape.Faces or (sub and shape.ShapeType != "Face"):
                    raise ValueError("Select faces, not edges or vertices.")
                entries = self.entries()
                if (obj, sub) not in entries and (obj, "") not in entries:
                    if not sub:
                        entries = [(o, n) for o, n in entries if o != obj]
                    entries.append((obj, sub))
                    self.obj.Faces = [(o, [n] if n else []) for o, n in entries]
            self.refresh()
            self.updatePreview()
            Gui.Selection.clearSelection()
        except Exception as error:
            self.status.setText(str(error))

    def removeFaces(self):
        rows = {self.faces.row(item) for item in self.faces.selectedItems()}
        self.obj.Faces = [
            (o, [n] if n else []) for i, (o, n) in enumerate(self.entries()) if i not in rows
        ]
        self.refresh()
        self.updatePreview()

    def clearFaces(self):
        self.obj.Faces = []
        self.refresh()
        self.updatePreview()
        self.select("Faces")

    def directionChanged(self, *args):
        self.obj.DirectionMode = self.direction.currentData()
        self.refresh()
        self.select(
            "Reference"
            if self.obj.DirectionMode == "Reference" and not self.obj.DirectionReference
            else None
        )

    def vectorChanged(self, *args):
        self.change("CustomDirection", App.Vector(*(field.value() for field in self.components)))

    def change(self, name, value):
        setattr(self.obj, name, value)
        self.updatePreview()

    def updatePreview(self, *args, force=False):
        if self.finished:
            return False
        self.arrow.clear()
        self.curveHighlight.clear()
        self.obj.ViewObject.hide()
        if not force and not self.preview.isChecked():
            self.status.setText(translate("Isocline", "Preview paused. OK will recompute."))
            return False
        self.doc.recompute()
        try:
            require_current(self.obj)
        except ReferenceError as error:
            self.status.setText(str(error))
            return False
        if not self.obj.isValid() or self.obj.Shape.isNull():
            self.status.setText(self.obj.StatusMessage or self.obj.getStatusString())
            return False
        self.obj.ViewObject.show()
        self.curveHighlight.update(linked_shape((self.obj, [])))
        box = self.obj.Shape.BoundBox
        self.arrow.update(box.Center, self.obj.Direction, max(box.DiagonalLength * 0.2, 1))
        self.status.setText(
            translate("Isocline", "Ready. The red curves follow the selected draft angle.")
        )
        return True

    def cleanup(self):
        Gui.Selection.removeObserver(self)
        self.arrow.close()
        self.curveHighlight.close()
        Gui.Selection.clearSelection()

    def accept(self):
        self.obj.touch()
        if not self.updatePreview(force=True):
            return False
        self.finished = True
        self.cleanup()
        self.restoreVisibility()
        self.obj.ViewObject.show()
        self.doc.commitTransaction()
        self.gui_doc.resetEdit()
        return True

    def reject(self, reset_edit=True):
        if self.finished:
            return True
        self.finished = True
        self.cleanup()
        self.doc.abortTransaction()
        if reset_edit:
            self.gui_doc.resetEdit()
        self.restoreVisibility()
        obj = self.doc.getObject(self.name)
        if obj:
            obj.ViewObject.Visibility = self.result_visible
        self.doc.recompute()
        return True

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def isAllowedAlterView(self):
        return True


class CommandIsocline:
    def GetResources(self):
        return {
            "Pixmap": ICON,
            "MenuText": translate("Isocline", "Isocline Curve"),
            "ToolTip": translate(
                "Isocline", "Create associative draft-angle curves on selected faces"
            ),
        }

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        if not self.IsActive():
            return
        selections = Gui.Selection.getSelectionEx()
        doc = App.ActiveDocument
        doc.openTransaction(translate("Isocline", "Create Isocline Curve"))
        obj = Isocline.makeIsocline(doc)
        links = []
        for selection in selections:
            if selection.DocumentName != doc.Name:
                continue
            names = [n for n in selection.SubElementNames if n.startswith("Face")]
            if names or (
                not selection.SubElementNames
                and hasattr(selection.Object, "Shape")
                and selection.Object.Shape.Faces
            ):
                links.append((selection.Object, names))
        obj.Faces = links
        Gui.Selection.clearSelection()
        Gui.getDocument(doc.Name).setEdit(obj.Name)


def registerCommand():
    if "Part_IsoclineCurve" not in Gui.listCommands():
        Gui.addCommand("Part_IsoclineCurve", CommandIsocline())
