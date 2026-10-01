# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component sketch-plane choice followed by the native Sketcher editor."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.ComponentExtrudeTask import active_component

_task = None


def tr(text):
    return App.Qt.translate("ComponentSketch", text)


class SketchTask:
    def __init__(self, component):
        import ComponentModel as Model
        import ComponentSketch as Sketch
        Model.activate(component, strict=False)
        self.component, self.support, self.result = component, None, None
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("New Sketch"))
        layout = QtWidgets.QFormLayout(self.form)
        self.plane = QtWidgets.QComboBox()
        for name in Sketch.PLANES:
            self.plane.addItem(tr(name), name)
        layout.addRow(tr("Plane"), self.plane)
        self.offset = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
        self.offset.setProperty("unit", "mm")
        self.offset.setProperty("minimum", -1e9)
        self.offset.setProperty("maximum", 1e9)
        layout.addRow(tr("Offset"), self.offset)
        self.capture = QtWidgets.QPushButton(tr("Use selected face"))
        layout.addRow(self.capture)
        self.source = QtWidgets.QLabel(tr("No face selected"))
        self.source.setTextFormat(QtCore.Qt.PlainText)
        self.source.setWordWrap(True)
        layout.addRow(self.source)
        self.status = QtWidgets.QLabel(tr("The sketch belongs to the active component. OK opens Sketcher."))
        self.status.setWordWrap(True)
        self.status.setTextFormat(QtCore.Qt.PlainText)
        layout.addRow(self.status)
        self.capture.clicked.connect(self.capture_face)
        self.plane.currentIndexChanged.connect(self.update_plane)
        self.update_plane()
        selected = Gui.Selection.getSelectionEx()
        if len(selected) == 1 and len(selected[0].SubElementNames) == 1:
            self.capture_face()

    def update_plane(self, *args):
        self.source.setVisible(self.plane.currentData() == "Selected planar face")

    def capture_face(self):
        import ComponentSketch as Sketch
        try:
            selected = Gui.Selection.getSelectionEx()
            if len(selected) != 1 or len(selected[0].SubElementNames) != 1:
                raise ValueError(tr("Select one planar face in the active component."))
            candidate = (selected[0].Object, selected[0].SubElementNames[0])
            self.support = Sketch.check_support(self.component, candidate)
            self.plane.setCurrentIndex(self.plane.findData("Selected planar face"))
            self.source.setText(self.support[0].Label + " / " + self.support[1])
            self.status.setText(tr("Ready. The sketch will remain attached to this face."))
        except Exception as error:
            self.status.setText(str(error))

    def getStandardButtons(self):
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        return getattr(buttons, "value", buttons)

    def accept(self):
        import ComponentSketch as Sketch
        try:
            self.result = Sketch.create(self.component, self.plane.currentData(),
                                        float(self.offset.property("rawValue")), self.support)
        except Exception as error:
            self.status.setText(str(error))
            return False
        self.finish()
        App.setActiveDocument(self.component.Document.Name)
        Gui.Selection.clearSelection()
        Gui.getDocument(self.component.Document.Name).setEdit(self.result.Name)
        return True

    def reject(self):
        self.finish()
        return True

    def finish(self):
        global _task
        Gui.Control.closeDialog()
        _task = None


def launch(component=None):
    global _task
    if Gui.Control.activeDialog():
        raise ValueError(tr("Finish the current task before creating a sketch."))
    component = component or active_component()
    App.setActiveDocument(component.Document.Name)
    _task = SketchTask(component)
    Gui.Control.showDialog(_task)
    return _task
