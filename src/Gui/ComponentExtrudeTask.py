# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Extrude creation/edit task with explicit profile and target choices."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.OccurrenceMove import Ghost

_task = None


def tr(text):
    return App.Qt.translate("ComponentExtrude", text)


def active_component():
    import ComponentModel as Model
    doc = App.ActiveDocument
    if doc is None:
        raise ValueError(tr("Create or open a component document first."))
    view = Gui.activeDocument().activeView()
    component = view.getActiveObject("part") if hasattr(view, "getActiveObject") else None
    return component if Model.is_component(component) else Model.metadata(doc).RootComponent


class ExtrudeTask:
    def __init__(self, component, operation=None, preset=None):
        import ComponentModel as Model
        import ComponentExtrude as Extrude
        self.component, self.operation = component, operation
        self.ghost = None
        self.result = None
        Model.activate(component, strict=False)
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("Extrude"))
        layout = QtWidgets.QFormLayout(self.form)
        self.mode = QtWidgets.QComboBox()
        for name in Extrude.MODES:
            self.mode.addItem(tr(name), name)
        layout.addRow(tr("Operation"), self.mode)
        self.profile = QtWidgets.QComboBox()
        self.profile.addItem(tr("Select a profile…"), None)
        for obj in Model.history(component):
            if (getattr(obj, "ComponentRole", "") in ("Object", "Reference", "Result")
                    and hasattr(obj, "Shape") and not obj.Shape.Solids and obj.Shape.Edges):
                self.profile.addItem(obj.Label + " (" + obj.Name + ")", obj.Name)
        layout.addRow(tr("Profile"), self.profile)
        self.capture = QtWidgets.QPushButton(tr("Use selected profile"))
        layout.addRow(self.capture)
        self.target = QtWidgets.QComboBox()
        self.target.addItem(tr("Select a target body…"), None)
        for obj in Model.finished_results(component):
            if obj.Shape.Solids and (operation is None or operation not in obj.OutListRecursive):
                self.target.addItem(obj.Label + " (" + obj.Name + ")", obj.Name)
        layout.addRow(tr("Target body"), self.target)
        self.length = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
        self.length.setProperty("unit", "mm")
        self.length.setProperty("minimum", 0.001)
        self.length.setProperty("maximum", 1e9)
        self.length.setProperty("rawValue", 10.0)
        layout.addRow(tr("Length"), self.length)
        self.reverse = QtWidgets.QCheckBox(tr("Reverse direction"))
        layout.addRow(self.reverse)
        self.preview_button = QtWidgets.QPushButton(tr("Preview"))
        layout.addRow(self.preview_button)
        self.status = QtWidgets.QLabel(tr("Choose a profile. No Body container is required."))
        self.status.setTextFormat(QtCore.Qt.PlainText)
        self.status.setWordWrap(True)
        layout.addRow(self.status)
        if preset in Extrude.MODES:
            self.mode.setCurrentIndex(Extrude.MODES.index(preset))
        if operation:
            tool, mode, target = Extrude.parameters(operation)
            self.profile.setCurrentIndex(self.profile.findData(tool.Base.Name))
            self.length.setProperty("rawValue", tool.LengthFwd.Value)
            self.reverse.setChecked(tool.Reversed)
            self.mode.setCurrentIndex(Extrude.MODES.index(mode))
            if target:
                if self.target.findData(target.Name) < 0:
                    self.target.addItem(target.Label, target.Name)
                self.target.setCurrentIndex(self.target.findData(target.Name))
        else:
            self.use_selection()
        self.capture.clicked.connect(self.use_selection)
        self.preview_button.clicked.connect(self.preview)
        self.mode.currentIndexChanged.connect(self.changed)
        self.profile.currentIndexChanged.connect(self.changed)
        self.target.currentIndexChanged.connect(self.changed)
        self.length.valueChanged.connect(self.changed)
        self.reverse.toggled.connect(self.changed)
        self.changed()

    def getStandardButtons(self):
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        return getattr(buttons, "value", buttons)

    def changed(self, *args):
        self.clear_preview()
        self.target.setEnabled(self.mode.currentData() != "New Body")
        if not self.profile.currentData():
            self.status.setText(tr("Choose a profile. No Body container is required."))
        elif self.mode.currentData() != "New Body" and not self.target.currentData():
            self.status.setText(tr("Choose the body to add to or subtract from."))
        else:
            self.status.setText(tr("Ready to preview. OK will recompute the operation."))

    def clear_preview(self):
        if self.ghost:
            self.ghost.remove()
            self.ghost = None

    def use_selection(self):
        for obj in Gui.Selection.getSelection():
            if obj.Document == self.component.Document:
                index = self.profile.findData(obj.Name)
                if index > 0:
                    self.profile.setCurrentIndex(index)
                    return

    def values(self):
        doc = self.component.Document
        profile = doc.getObject(self.profile.currentData()) if self.profile.currentData() else None
        if profile is None:
            raise ValueError(tr("Select a profile in the active component."))
        mode = self.mode.currentData()
        target = doc.getObject(self.target.currentData()) if self.target.currentData() and mode != "New Body" else None
        length = float(self.length.property("rawValue"))
        return profile, length, mode, target, self.reverse.isChecked()

    def preview(self):
        import ComponentExtrude as Extrude
        self.clear_preview()
        try:
            shape = Extrude.preview(self.component, *self.values())
            shape.Placement = self.component.getGlobalPlacement().multiply(shape.Placement)
            self.ghost = Ghost(shape)
            self.status.setText(tr("Preview ready. OK creates or updates the operation."))
            return True
        except Exception as error:
            self.status.setText(str(error))
            return False

    def accept(self):
        import ComponentExtrude as Extrude
        try:
            profile, length, mode, target, reverse = self.values()
            if self.operation:
                self.operation = Extrude.edit(self.operation, profile, length, reverse, mode, target)
            else:
                self.operation, self.result = Extrude.create(self.component, profile, length, mode, target, reverse)
        except Exception as error:
            self.status.setText(str(error))
            return False
        self.finish()
        return True

    def reject(self):
        self.finish()
        return True

    def finish(self):
        global _task
        self.clear_preview()
        Gui.Control.closeDialog()
        _task = None


def launch(preset=None, operation=None):
    global _task
    if Gui.Control.activeDialog():
        raise ValueError(tr("Finish the current task before starting Extrude."))
    import ComponentModel as Model
    component = Model.owner(operation) if operation else active_component()
    App.setActiveDocument(component.Document.Name)
    _task = ExtrudeTask(component, operation, preset)
    Gui.Control.showDialog(_task)
    return _task
