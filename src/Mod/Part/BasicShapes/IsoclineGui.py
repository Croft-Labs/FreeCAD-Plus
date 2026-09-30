# SPDX-License-Identifier: LGPL-2.1-or-later

"""Complete face/direction/angle selection for new and existing Isocline Curves."""

from pathlib import Path
from .FeatureTask import (
    creation_transaction, guard_task_construction, task_selection_snapshot, highlight_references,
)
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui
from . import Isocline
from .FeatureTask import TaskFeatureViewProvider, DirectionArrow, CurveOverlay
from .ShapeReferences import validate_link, linked_shape, require_current, ReferenceError

translate = App.Qt.translate
ICON = str(Path(__file__).with_name("Isocline.svg"))


def selection_link(feature, candidate, sub, role):
    """Validate preselection and later picks through the same geometry boundary."""
    validate_link(feature, candidate)
    require_current(candidate)
    link = (candidate, [sub] if sub else [])
    if role == "Reference":
        Isocline.reference_direction(link)
    else:
        shape = linked_shape(link)
        if not shape.Faces or (sub and shape.ShapeType != "Face"):
            raise ValueError("Select faces, not edges or vertices.")
        # PropertyLinkSubList drops an object paired with an empty subelement
        # list. An explicit empty name represents the whole-object reference.
        link = (candidate, [sub])
    return link


class ViewProviderIsocline(TaskFeatureViewProvider):
    icon = ICON
    editLabel = translate("Isocline", "Edit Isocline Curve")

    def makeTask(self, obj):
        return IsoclineTask(obj)


class IsoclineTask:
    @guard_task_construction
    def __init__(self, obj):
        self.selection = task_selection_snapshot()
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
        self.preselectionFeedback = QtGui.QLabel()
        self.preselectionFeedback.setObjectName("isoclinePreselectionFeedback")
        self.preselectionFeedback.setTextFormat(QtCore.Qt.PlainText)
        self.preselectionFeedback.setWordWrap(True)
        self.preselectionFeedback.hide()
        self.activeCollector = QtGui.QLabel(translate("Isocline", "Picking: none"))
        self.activeCollector.setObjectName("isoclineActiveCollector")
        group = QtGui.QGroupBox(translate("Isocline", "Target faces"))
        group.setObjectName("isoclineFacesGroup")
        rows = QtGui.QVBoxLayout(group)
        self.facesHint = QtGui.QLabel()
        self.facesHint.setObjectName("isoclineFacesHint")
        self.facesHint.setWordWrap(True)
        rows.addWidget(self.facesHint)
        self.faces = QtGui.QListWidget()
        self.faces.setObjectName("isoclineFaces")
        self.faces.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.faces.setMaximumHeight(120)
        self.faces.itemSelectionChanged.connect(self.highlightFaces)
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
        layout.addWidget(self.activeCollector)
        layout.addWidget(self.preselectionFeedback)
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
        self.referenceHint = QtGui.QLabel()
        self.referenceHint.setObjectName("isoclineReferenceHint")
        self.referenceHint.setWordWrap(True)
        ref_layout.addWidget(self.referenceHint)
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
        reference_actions = QtGui.QHBoxLayout()
        self.highlightRef = QtGui.QPushButton(translate("Isocline", "Highlight"))
        self.highlightRef.setObjectName("isoclineHighlightReference")
        self.highlightRef.clicked.connect(self.highlightReference)
        self.clearRef = QtGui.QPushButton(translate("Isocline", "Clear"))
        self.clearRef.setObjectName("isoclineClearReference")
        self.clearRef.clicked.connect(self.clearReference)
        reference_actions.addWidget(self.highlightRef)
        reference_actions.addWidget(self.clearRef)
        ref_layout.addLayout(reference_actions)
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
        self.tolerance = QtGui.QLineEdit()
        self.tolerance.setObjectName("isoclineTolerance")
        self.tolerance.setText("{} mm".format(obj.Tolerance.Value))
        self.toleranceHelp = translate(
            "Isocline", "3D curve distance tolerance: 0.0000001 mm to 0.01 mm. "
            "Enter a length with units; bare numbers use mm. This is not an angular tolerance."
        )
        self.tolerance.setToolTip(self.toleranceHelp)
        self.toleranceDirty = False
        self.tolerance.textChanged.connect(self.toleranceEdited)
        self.tolerance.editingFinished.connect(self.updatePreview)
        angle_row.addRow(translate("Isocline", "Curve tolerance"), self.tolerance)
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
        blocker = QtCore.QSignalBlocker(self.faces)
        self.faces.clear()
        for obj, sub in self.entries():
            self.remember(obj)
            self.faces.addItem(obj.Label + (" : " + sub if sub else " (all faces)"))
        del blocker
        self.facesHint.setText(translate(
            "Isocline", "Selected entries: {}. Pick faces or whole objects (all faces)."
        ).format(self.faces.count()))
        link = self.obj.DirectionReference
        self.referenceHint.setText(translate(
            "Isocline", "Selected: {}/1. Plane, planar face, straight edge or axis."
        ).format(int(bool(link))))
        self.highlightRef.setEnabled(bool(link and link[0]))
        self.clearRef.setEnabled(bool(link and link[0]))
        self.refName.setText(
            link[0].Label + (" : " + link[1][0] if link[1] else "") if link else ""
        )
        self.reference.setVisible(self.obj.DirectionMode == "Reference")
        self.custom.setVisible(self.obj.DirectionMode == "Custom vector")

    def select(self, mode):
        self.mode = mode
        self.activeCollector.setText(translate("Isocline", {
            "Faces": "Picking: Target faces", "Reference": "Picking: Direction reference",
            None: "Picking: none",
        }[mode]))
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

    def highlightFaces(self):
        if self.finished:
            return
        entries = self.entries()
        highlight_references(self, [entries[self.faces.row(item)]
                                    for item in self.faces.selectedItems()])

    def highlightReference(self):
        link = self.obj.DirectionReference
        if not self.finished and link and link[0]:
            highlight_references(self, [(link[0], sub) for sub in (link[1] or [""])])

    def clearReference(self):
        if self.finished:
            return
        self.restoreVisibility()
        self.obj.DirectionReference = None
        self.obj.Shape = Part.Shape()
        self.refresh()
        self.updatePreview()
        self.select("Reference")

    def addSelection(self, document, name, sub, position):
        if self.finished or not self.mode or getattr(self, "_inspecting_selection", False):
            return
        try:
            if document != self.doc.Name:
                raise ValueError("Select an object in this document.")
            obj = self.doc.getObject(name)
            link = selection_link(self.obj, obj, sub, self.mode)
            if self.mode == "Reference":
                self.obj.DirectionReference = link
                self.select(None)
            else:
                entries = self.entries()
                if (obj, sub) not in entries and (obj, "") not in entries:
                    if not sub:
                        entries = [(o, n) for o, n in entries if o != obj]
                    entries.append((obj, sub))
                    self.obj.Faces = [(o, [n]) for o, n in entries]
            self.refresh()
            self.updatePreview()
            Gui.Selection.clearSelection()
        except Exception as error:
            self.status.setText(str(error))

    def removeFaces(self):
        rows = {self.faces.row(item) for item in self.faces.selectedItems()}
        self.obj.Faces = [
            (o, [n]) for i, (o, n) in enumerate(self.entries()) if i not in rows
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

    def toleranceEdited(self, *args):
        self.toleranceDirty = True

    def applyTolerance(self):
        expression = dict(self.obj.ExpressionEngine).get("Tolerance")
        self.tolerance.setReadOnly(bool(expression))
        self.tolerance.setToolTip(self.toleranceHelp)
        if expression:
            blocker = QtCore.QSignalBlocker(self.tolerance)
            self.tolerance.setText("{} mm".format(self.obj.Tolerance.Value))
            del blocker
            self.toleranceDirty = False
            self.tolerance.setToolTip(translate(
                "Isocline", "Controlled by expression: {}. Edit the expression in the property editor."
            ).format(expression))
        elif self.toleranceDirty:
            try:
                value = Isocline.curve_tolerance(self.tolerance.text())
            except Exception as error:
                self.status.setText(translate("Isocline", "Curve tolerance: {}").format(error))
                return False
            self.obj.Tolerance = value
            self.toleranceDirty = False
        return True

    def updatePreview(self, *args, force=False):
        if self.finished:
            return False
        self.arrow.clear()
        self.curveHighlight.clear()
        self.obj.ViewObject.hide()
        if not self.applyTolerance():
            return False
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
        self.selection.restore()
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
        selections = Gui.Selection.getSelectionEx("*")
        doc = App.ActiveDocument
        with creation_transaction(doc, translate("Isocline", "Create Isocline Curve")):
            obj = Isocline.makeIsocline(doc)
            links = []
            messages = []
            for selection in selections:
                for sub in (selection.SubElementNames or [""]):
                    try:
                        link = selection_link(obj, selection.Object, sub, "Faces")
                        if link not in links:
                            links.append(link)
                    except Exception as error:
                        label = selection.Object.Label + (" : " + sub if sub else "")
                        messages.append(translate("Isocline", "Ignored preselection: {0}: {1}").format(
                            label, error))
            obj.Faces = links
            Gui.Selection.clearSelection()
            if not Gui.getDocument(doc.Name).setEdit(obj.Name):
                raise RuntimeError("Could not open the feature task editor.")
            task = obj.ViewObject.Proxy.task
            task.preselectionFeedback.setText("\n".join(messages))
            task.preselectionFeedback.setVisible(bool(messages))


def registerCommand():
    if "Part_IsoclineCurve" not in Gui.listCommands():
        Gui.addCommand("Part_IsoclineCurve", CommandIsocline())
