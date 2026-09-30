# SPDX-License-Identifier: LGPL-2.1-or-later

"""One create/edit task for the associative Trim Body feature."""

from pathlib import Path
from BasicShapes.FeatureTask import (
    creation_transaction, guard_task_construction, task_selection_snapshot, highlight_references,
)
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui
from BasicShapes.FeatureTask import TaskFeatureViewProvider, DirectionArrow as KeepArrow
from BasicShapes.ShapeReferences import require_current, ReferenceError
from . import TrimAPI, TrimFeatures

translate = App.Qt.translate
ICON = str(Path(__file__).with_name("TrimBody.svg"))


def selection_link(feature, candidate, sub, role):
    """Use identical reference checks for preselection and interactive picking."""
    TrimAPI.validate_link(feature, candidate)
    require_current(candidate)
    other = feature.Tool if role == "Target" else feature.Target
    if other and other[0] == candidate:
        raise TrimAPI.TrimError("Use a separate object as the cutting tool.")
    link = (candidate, [sub] if role == "Tool" and sub else [])
    if role == "Tool":
        TrimAPI.tool_shape(link)
    else:
        shape = TrimAPI.linked_shape(link)
        if shape.isNull() or not shape.Faces:
            raise TrimAPI.TrimError("Select a solid or sheet target.")
    return link


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
    @guard_task_construction
    def __init__(self, obj):
        self.selection = task_selection_snapshot()
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
        self.preselectionFeedback = QtGui.QLabel()
        self.preselectionFeedback.setObjectName("trimPreselectionFeedback")
        self.preselectionFeedback.setTextFormat(QtCore.Qt.PlainText)
        self.preselectionFeedback.setWordWrap(True)
        self.preselectionFeedback.hide()
        self.activeCollector = QtGui.QLabel(translate("TrimBody", "Picking: none"))
        self.activeCollector.setObjectName("trimActiveCollector")
        self.fields = {}
        self.buttons = {}
        self.inspectButtons = {}
        self.collectorHints = {}
        for key, title in (("Target", "Target body"), ("Tool", "Cutting tool")):
            group = QtGui.QGroupBox(translate("TrimBody", title))
            group.setObjectName("trim" + key + "Group")
            rows = QtGui.QVBoxLayout(group)
            hint = QtGui.QLabel()
            hint.setObjectName("trim" + key + "Hint")
            hint.setWordWrap(True)
            rows.addWidget(hint)
            self.collectorHints[key] = hint
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
            inspect = QtGui.QPushButton(translate("TrimBody", "Highlight"))
            inspect.setObjectName("trimHighlight" + key)
            inspect.clicked.connect(lambda checked=False, key=key: self.highlight(key))
            controls.addWidget(button)
            controls.addWidget(inspect)
            controls.addWidget(clear)
            rows.addLayout(controls)
            layout.addWidget(group)
            self.fields[key], self.buttons[key] = field, button
            self.inspectButtons[key] = inspect
        layout.addWidget(self.activeCollector)
        layout.addWidget(self.preselectionFeedback)
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
            self.collectorHints[key].setText(
                translate("TrimBody", "Selected: {}/1. Solid or sheet body.").format(int(bool(link)))
                if key == "Target" else
                translate("TrimBody", "Selected: {}/1. Plane, face or sheet body.").format(int(bool(link)))
            )
            self.inspectButtons[key].setEnabled(bool(link and link[0]))
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
        self.activeCollector.setText(translate("TrimBody", {
            "Target": "Picking: Target body", "Tool": "Picking: Cutting tool",
            None: "Picking: none",
        }[key]))
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

    def highlight(self, key):
        link = getattr(self.obj, key)
        if not self.finished and link and link[0]:
            highlight_references(self, [(link[0], sub) for sub in (link[1] or [""])])

    def addSelection(self, document, name, sub, position):
        if self.finished or not self.mode or getattr(self, "_inspecting_selection", False):
            return
        try:
            if document != self.doc.Name:
                raise TrimAPI.TrimError("Select an object in this document.")
            obj = self.doc.getObject(name)
            key = self.mode
            link = selection_link(self.obj, obj, sub, key)
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
        self.selection.restore()
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
        selections = Gui.Selection.getSelectionEx("*")
        doc = App.ActiveDocument
        with creation_transaction(doc, translate("TrimBody", "Create Trim Body")):
            obj = TrimFeatures.makeTrimBody(doc)
            messages = []
            # Preserve the established order: first target, second tool. Never
            # silently choose one of several tool faces or reassign ignored picks.
            for index, selection in enumerate(selections):
                try:
                    if index > 1:
                        raise TrimAPI.TrimError("Only the first target and second cutting tool are used.")
                    role = "Target" if index == 0 else "Tool"
                    if role == "Tool" and len(selection.SubElementNames) > 1:
                        raise TrimAPI.TrimError("Select one cutting-tool face; multiple faces were preselected.")
                    sub = selection.SubElementNames[0] if selection.SubElementNames else ""
                    setattr(obj, role, selection_link(obj, selection.Object, sub, role))
                except Exception as error:
                    messages.append(translate("TrimBody", "Ignored preselection: {0}: {1}").format(
                        selection.Object.Label, error))
            Gui.Selection.clearSelection()
            if not Gui.getDocument(doc.Name).setEdit(obj.Name):
                raise RuntimeError("Could not open the feature task editor.")
            task = obj.ViewObject.Proxy.task
            task.preselectionFeedback.setText("\n".join(messages))
            task.preselectionFeedback.setVisible(bool(messages))


def registerCommand():
    if "Part_TrimBody" not in Gui.listCommands():
        Gui.addCommand("Part_TrimBody", CommandTrimBody())
