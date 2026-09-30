# SPDX-License-Identifier: LGPL-2.1-or-later
"""Task pane for creating/editing a manually indexed machining setup."""

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtWidgets
from BasicShapes.FeatureTask import TaskFeatureViewProvider, creation_transaction
from Path.Main import IndexedSetup

tr = App.Qt.translate


class TaskPanel:
    def __init__(self, obj):
        self.obj, self.doc, self.finished = obj, obj.Document, False
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("CAM", "Indexed setup"))
        layout = QtWidgets.QFormLayout(self.form)
        info = QtWidgets.QLabel(tr("CAM", "Manually index the part between jobs. Model, stock and "
                                  "tabs share this orientation. Create and post operations separately "
                                  "for this job; no rotary-axis moves are generated."))
        info.setWordWrap(True)
        layout.addRow(info)
        self.axis = QtWidgets.QComboBox()
        self.axis.addItems(["X", "Y", "Z"])
        self.axis.setCurrentText(obj.Axis)
        layout.addRow(tr("CAM", "Rotation axis"), self.axis)
        self.angle = QtWidgets.QDoubleSpinBox()
        self.angle.setRange(-360, 360)
        self.angle.setDecimals(3)
        self.angle.setSuffix(" deg")
        self.angle.setValue(obj.Angle.Value)
        layout.addRow(tr("CAM", "Index angle"), self.angle)
        self.origin = QtWidgets.QComboBox()
        for name in obj.getEnumerationsOfProperty("Origin"):
            self.origin.addItem(tr("CAM", name), name)
        self.origin.setCurrentIndex(self.origin.findData(obj.Origin))
        layout.addRow(tr("CAM", "Work origin"), self.origin)
        self.coordinates = []
        for axis, value in zip("XYZ", obj.CustomOrigin):
            field = QtWidgets.QDoubleSpinBox()
            field.setRange(-1e6, 1e6)
            field.setDecimals(3)
            field.setSuffix(" mm")
            field.setValue(value)
            field.setToolTip(tr("CAM", "Work origin measured in rotated source coordinates"))
            self.coordinates.append(field)
            layout.addRow(tr("CAM", "Custom origin") + " " + axis, field)
            field.valueChanged.connect(self.preview)
        self.status = QtWidgets.QLabel()
        self.status.setWordWrap(True)
        layout.addRow(self.status)
        self.axis.currentIndexChanged.connect(self.preview)
        self.angle.valueChanged.connect(self.preview)
        self.origin.currentIndexChanged.connect(self.preview)
        self.preview()

    def preview(self, *args):
        self.obj.Axis = self.axis.currentText()
        self.obj.Angle = self.angle.value()
        self.obj.Origin = self.origin.currentData()
        self.obj.CustomOrigin = App.Vector(*(field.value() for field in self.coordinates))
        for field in self.coordinates:
            field.setEnabled(self.obj.Origin == "Custom")
        try:
            self.obj.Proxy.execute(self.obj)
            self.doc.recompute()
            self.status.clear()
            return True
        except Exception as error:
            self.status.setText(str(error))
            return False

    def accept(self):
        if not self.preview():
            return False
        self.finished = True
        self.doc.commitTransaction()
        Gui.activeDocument().resetEdit()
        Gui.Control.closeDialog()
        return True

    def reject(self, reset_edit=True):
        if not self.finished:
            self.finished = True
            self.doc.abortTransaction()
            self.doc.recompute()
        if reset_edit:
            Gui.activeDocument().resetEdit()
            Gui.Control.closeDialog()
        return True


class FrameViewProvider(TaskFeatureViewProvider):
    icon = ":/icons/CAM_Job.svg"
    editLabel = tr("CAM", "Edit indexed setup")

    def makeTask(self, obj):
        return TaskPanel(obj)


class TabViewProvider:
    def __init__(self, view):
        view.Proxy = self

    def getIcon(self):
        return ":/icons/CAM_Tags.svg"

    def doubleClicked(self, view):
        if Gui.Control.activeDialog() or not view.Object.Objects:
            return False
        source = view.Object.Objects[0]
        App.Console.PrintMessage(tr("CAM", "Editing the shared tab in its original setup coordinates.") + "\n")
        return source.ViewObject.Proxy.doubleClicked(source.ViewObject)

    def dumps(self):
        return None

    def loads(self, state):
        pass


class Command:
    def GetResources(self):
        return {"Pixmap": ":/icons/CAM_Job.svg", "MenuText": tr("CAM", "Indexed Setup"),
                "ToolTip": tr("CAM", "Creates another manually indexed side of a Job, including its stock and tabs")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        from PathScripts.PathUtils import findParentJob

        job = None
        for selected in Gui.Selection.getSelection():
            job = selected if hasattr(selected, "JobType") else findParentJob(selected)
            if job:
                break
        if not job:
            jobs = [obj for obj in App.ActiveDocument.Objects if hasattr(obj, "JobType")]
            if len(jobs) == 1:
                job = jobs[0]
        if not job:
            App.Console.PrintError(tr("CAM", "Select the source CAM Job for the indexed setup.") + "\n")
            return
        with creation_transaction(job.Document, tr("CAM", "Create indexed setup")):
            result = IndexedSetup.create(job)
            if not Gui.activeDocument().setEdit(result.IndexFrame.Name):
                raise RuntimeError("Could not open the CAM task panel")


Gui.addCommand("CAM_IndexedSetup", Command())
