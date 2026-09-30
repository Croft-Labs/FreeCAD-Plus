# SPDX-License-Identifier: LGPL-2.1-or-later

"""One create/edit task for the associative Trim Body feature."""

from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui
from BasicShapes.FeatureTask import TaskFeatureViewProvider, DirectionArrow as KeepArrow
from BasicShapes.ShapeReferences import require_current, ReferenceError
from . import TrimAPI, TrimFeatures

translate = App.Qt.translate
ICON = str(Path(__file__).with_name("TrimBody.svg"))


class ViewProviderTrimBody(TaskFeatureViewProvider):
    icon = ICON
    editLabel = translate("TrimBody", "Edit Trim Body")

    def makeTask(self, obj):
        return TrimBodyTask(obj)

    def onDelete(self, view, subelements):
        for link in (view.Object.Target, view.Object.Tool):
            if link and link[0]:
                link[0].ViewObject.show()
        return True


class TrimBodyTask:
    def __init__(self, obj):
        self.obj = obj
        self.name = obj.Name
        self.result_visible = obj.ViewObject.Visibility
        self.doc = obj.Document
        self.gui_doc = Gui.getDocument(self.doc.Name)
        self.finished = False
        self.mode = None
        self.visibility = {}
        self.arrow = KeepArrow(self.gui_doc.activeView())
        self.form = QtGui.QWidget()
        self.form.setObjectName("trimBodyTask")
        self.form.setWindowTitle(translate("TrimBody", "Trim Body"))
        self.form.setWindowIcon(QtGui.QIcon(ICON))
        layout = QtGui.QVBoxLayout(self.form)
        self.fields = {}
        self.buttons = {}
        for key, title in (("Target", "Target body"), ("Tool", "Cutting tool")):
            group = QtGui.QGroupBox(translate("TrimBody", title))
            group.setObjectName("trim" + key + "Group")
            rows = QtGui.QVBoxLayout(group)
            field = QtGui.QLineEdit()
            field.setObjectName("trim" + key)
            field.setReadOnly(True)
            field.setPlaceholderText(translate("TrimBody", "Nothing selected"))
            rows.addWidget(field)
            controls = QtGui.QHBoxLayout()
            button = QtGui.QPushButton(translate("TrimBody", "Select"))
            button.setObjectName("trimSelect" + key)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, key=key: self.select(key if checked else None))
            clear = QtGui.QPushButton(translate("TrimBody", "Clear"))
            clear.setObjectName("trimClear" + key)
            clear.clicked.connect(lambda checked=False, key=key: self.clear(key))
            controls.addWidget(button)
            controls.addWidget(clear)
            rows.addLayout(controls)
            layout.addWidget(group)
            self.fields[key], self.buttons[key] = field, button
        side = QtGui.QHBoxLayout()
        self.side = QtGui.QLabel()
        self.side.setObjectName("trimKeepSide")
        self.reverse = QtGui.QToolButton()
        self.reverse.setObjectName("trimReverse")
        self.reverse.setIcon(Gui.getIcon("button_sort"))
        self.reverse.setToolTip(translate("TrimBody", "Reverse the side to keep"))
        self.reverse.setAccessibleName(translate("TrimBody", "Reverse the side to keep"))
        self.reverse.setCheckable(True)
        self.reverse.setChecked(obj.Reversed)
        self.reverse.toggled.connect(lambda value: self.change("Reversed", value))
        side.addWidget(self.side, 1)
        side.addWidget(self.reverse)
        layout.addLayout(side)
        self.extend = QtGui.QCheckBox(translate("TrimBody", "Extend planar tool across target"))
        self.extend.setObjectName("trimExtendPlanar")
        self.extend.setChecked(obj.ExtendPlanar)
        self.extend.toggled.connect(lambda value: self.change("ExtendPlanar", value))
        layout.addWidget(self.extend)
        self.refine = QtGui.QCheckBox(translate("TrimBody", "Refine result"))
        self.refine.setObjectName("trimRefine")
        self.refine.setChecked(obj.Refine)
        self.refine.toggled.connect(lambda value: self.change("Refine", value))
        layout.addWidget(self.refine)
        self.preview = QtGui.QCheckBox(translate("TrimBody", "Live preview"))
        self.preview.setObjectName("trimPreview")
        self.preview.setChecked(True)
        self.preview.toggled.connect(self.updatePreview)
        layout.addWidget(self.preview)
        hint = QtGui.QLabel(
            translate(
                "TrimBody",
                "The green arrow points to the side kept. Curved tools must span the target completely.",
            )
        )
        hint.setWordWrap(True)
        layout.addWidget(hint)
        self.status = QtGui.QLabel()
        self.status.setObjectName("trimStatus")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        layout.addStretch()
        Gui.Selection.addObserver(self)
        self.refreshFields()
        self.updatePreview()
        if not obj.Target:
            self.select("Target")
        elif not obj.Tool:
            self.select("Tool")

    def remember(self, obj):
        if obj and obj.Name not in self.visibility:
            self.visibility[obj.Name] = obj.ViewObject.Visibility

    def restoreVisibility(self):
        for name, visible in self.visibility.items():
            obj = self.doc.getObject(name)
            if obj:
                obj.ViewObject.Visibility = visible

    def refreshFields(self):
        for key in self.fields:
            link = getattr(self.obj, key)
            if link and link[0]:
                self.remember(link[0])
                text = link[0].Label
                if link[1] and link[1][0]:
                    text += " : " + link[1][0]
                self.fields[key].setText(text)
            else:
                self.fields[key].clear()
        self.side.setText(
            translate("TrimBody", "Keep: opposite tool normal")
            if self.obj.Reversed
            else translate("TrimBody", "Keep: along tool normal")
        )

    def select(self, key):
        self.mode = key
        for field, button in self.buttons.items():
            blocker = QtCore.QSignalBlocker(button)
            button.setChecked(field == key)
            del blocker
        Gui.Selection.clearSelection()
        if key:
            self.restoreVisibility()
            for link in (self.obj.Target, self.obj.Tool):
                if link and link[0]:
                    self.remember(link[0])
                    link[0].ViewObject.show()
            self.obj.ViewObject.hide()
            self.arrow.clear()
            self.status.setText(
                translate(
                    "TrimBody",
                    (
                        "Select a target body."
                        if key == "Target"
                        else "Select a datum plane, a face, or a sheet body."
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
                raise TrimAPI.TrimError("Select an object in this document.")
            obj = self.doc.getObject(name)
            TrimAPI.validate_link(self.obj, obj)
            require_current(obj)
            key = self.mode
            other = self.obj.Tool if key == "Target" else self.obj.Target
            if other and other[0] == obj:
                raise TrimAPI.TrimError("Use a separate object as the cutting tool.")
            link = (obj, [sub] if key == "Tool" and sub else [])
            if key == "Tool":
                TrimAPI.tool_shape(link)
            else:
                shape = TrimAPI.linked_shape(link)
                if shape.isNull() or not shape.Faces:
                    raise TrimAPI.TrimError("Select a solid or sheet target.")
            self.restoreVisibility()
            setattr(self.obj, key, link)
            self.refreshFields()
            self.select("Tool" if key == "Target" and not self.obj.Tool else None)
        except Exception as error:
            self.status.setText(str(error))

    def clear(self, key):
        self.restoreVisibility()
        setattr(self.obj, key, None)
        self.obj.Shape = Part.Shape()
        self.refreshFields()
        self.select(key)

    def change(self, property_name, value):
        setattr(self.obj, property_name, value)
        self.refreshFields()
        self.updatePreview()

    def updatePreview(self, *args, force=False):
        if self.finished:
            return False
        self.restoreVisibility()
        self.arrow.clear()
        self.obj.ViewObject.hide()
        if not self.obj.Target or not self.obj.Tool:
            self.obj.Shape = Part.Shape()
            self.status.setText(translate("TrimBody", "Select a target body and cutting tool."))
            return False
        if not force and not self.preview.isChecked():
            self.status.setText(
                translate("TrimBody", "Preview paused. OK will recompute the trim.")
            )
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
        self.obj.Target[0].ViewObject.hide()
        self.obj.ViewObject.show()
        self.arrow.update(
            self.obj.ArrowOrigin,
            self.obj.Direction,
            max(self.obj.Shape.BoundBox.DiagonalLength * 0.2, 0.5),
        )
        self.status.setText(translate("TrimBody", "Ready. The displayed result is the side kept."))
        return True

    def cleanup(self):
        Gui.Selection.removeObserver(self)
        self.arrow.close()
        Gui.Selection.clearSelection()

    def accept(self):
        self.obj.touch()
        if not self.updatePreview(force=True):
            return False
        self.finished = True
        self.cleanup()
        self.restoreVisibility()
        for link in (self.obj.Target, self.obj.Tool):
            if link and link[0]:
                link[0].ViewObject.hide()
        self.obj.ViewObject.show()
        self.doc.commitTransaction()
        self.gui_doc.resetEdit()
        return True

    def reject(self, reset_edit=True):
        if self.finished:
            return True
        self.finished = True
        self.cleanup()
        # resetEdit commits a pending GUI edit; roll back before closing it.
        self.doc.abortTransaction()
        if reset_edit:
            self.gui_doc.resetEdit()
        self.restoreVisibility()
        result = self.doc.getObject(self.name)
        if result:
            result.ViewObject.Visibility = self.result_visible
        self.doc.recompute()
        return True

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def isAllowedAlterView(self):
        return True


class CommandTrimBody:
    def GetResources(self):
        return {
            "Pixmap": ICON,
            "MenuText": translate("TrimBody", "Trim Body"),
            "ToolTip": translate(
                "TrimBody",
                "Trim a solid or sheet with a plane, face, or sheet and choose the side to keep",
            ),
        }

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        if not self.IsActive():
            return
        selections = Gui.Selection.getSelectionEx()
        doc = App.ActiveDocument
        doc.openTransaction(translate("TrimBody", "Create Trim Body"))
        obj = TrimFeatures.makeTrimBody(doc)
        # Preselection is optional. The same task remains available for incomplete input.
        if selections and selections[0].DocumentName == doc.Name:
            candidate = selections[0].Object
            try:
                shape = TrimAPI.linked_shape((candidate, []))
                if shape.Faces:
                    obj.Target = (candidate, [])
            except Exception:
                pass
        if len(selections) > 1 and selections[1].DocumentName == doc.Name:
            selection = selections[1]
            sub = selection.SubElementNames[0] if selection.SubElementNames else ""
            link = (selection.Object, [sub] if sub else [])
            try:
                if not obj.Target or obj.Target[0] != selection.Object:
                    TrimAPI.tool_shape(link)
                    obj.Tool = link
            except Exception:
                pass
        Gui.Selection.clearSelection()
        Gui.getDocument(doc.Name).setEdit(obj.Name)


def registerCommand():
    if "Part_TrimBody" not in Gui.listCommands():
        Gui.addCommand("Part_TrimBody", CommandTrimBody())
