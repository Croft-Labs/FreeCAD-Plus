# SPDX-License-Identifier: LGPL-2.1-or-later
"""Create/edit stock bridges in one task pane, including viewport placement."""

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtWidgets
from BasicShapes.FeatureTask import TaskFeatureViewProvider
from Path.Main import HoldingTab

tr = App.Qt.translate


class TaskPanel:
    def __init__(self, obj):
        self.obj = obj
        self.doc = obj.Document
        self.finished = False
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("CAM", "Holding tab"))
        layout = QtWidgets.QFormLayout(self.form)
        info = QtWidgets.QLabel(tr("CAM", "Position this bridge between the part and surrounding stock. "
                                  "Parallel and Waterline paths preserve it. Dimensions are in mm."))
        info.setWordWrap(True)
        layout.addRow(info)
        self.fields = {}
        base = obj.Placement.Base
        angle = obj.Placement.Rotation.toEuler()[0]
        for key, label, value in (
            ("X", "Center X", base.x), ("Y", "Center Y", base.y),
            ("Z", "Bottom Z", base.z), ("Length", "Length", obj.Length.Value),
            ("Width", "Width", obj.Width.Value), ("Height", "Height", obj.Height.Value),
            ("Angle", "Angle (degrees)", angle),
        ):
            field = QtWidgets.QDoubleSpinBox()
            field.setObjectName("tab" + key)
            field.setDecimals(3)
            field.setRange(0.001 if key in ("Length", "Width", "Height") else -1e6, 1e6)
            if key == "Angle":
                field.setRange(-360, 360)
            field.setValue(value)
            layout.addRow(tr("CAM", label), field)
            self.fields[key] = field
            field.valueChanged.connect(self.preview)
        self.pick = QtWidgets.QPushButton(tr("CAM", "Pick position on model"))
        self.pick.setCheckable(True)
        self.pick.setToolTip(tr("CAM", "Click the model to place the tab center in XY; Bottom Z is retained."))
        layout.addRow(self.pick)
        self.status = QtWidgets.QLabel()
        self.status.setWordWrap(True)
        layout.addRow(self.status)
        self.visible = obj.ViewObject.Visibility
        obj.ViewObject.Visibility = True
        Gui.Selection.addObserver(self)

    def addSelection(self, document, name, sub, point):
        if not self.pick.isChecked() or document != self.doc.Name or name == self.obj.Name:
            return
        for key, value in zip(("X", "Y"), point[:2]):
            self.fields[key].blockSignals(True)
            self.fields[key].setValue(value)
            self.fields[key].blockSignals(False)
        self.pick.setChecked(False)
        self.preview()

    def preview(self, *args):
        for key in ("Length", "Width", "Height"):
            setattr(self.obj, key, self.fields[key].value())
        self.obj.Placement = App.Placement(
            App.Vector(*(self.fields[key].value() for key in ("X", "Y", "Z"))),
            App.Rotation(App.Vector(0, 0, 1), self.fields["Angle"].value()),
        )
        # Preview the bridge without regenerating every toolpath on each keystroke.
        self.obj.Proxy.execute(self.obj)

    def accept(self):
        self.preview()
        if self.obj.Shape.isNull():
            self.status.setText(tr("CAM", "Enter positive tab dimensions."))
            return False
        self.doc.recompute()
        self.finished = True
        Gui.Selection.removeObserver(self)
        self.doc.commitTransaction()
        Gui.activeDocument().resetEdit()
        Gui.Control.closeDialog()
        return True

    def reject(self, reset_edit=True):
        if not self.finished:
            self.finished = True
            Gui.Selection.removeObserver(self)
            name = self.obj.Name
            self.doc.abortTransaction()
            self.doc.recompute()
            restored = self.doc.getObject(name)
            if restored:
                restored.ViewObject.Visibility = self.visible
        if reset_edit:
            Gui.activeDocument().resetEdit()
            Gui.Control.closeDialog()
        return True


class ViewProvider(TaskFeatureViewProvider):
    icon = ":/icons/CAM_Tags.svg"
    editLabel = tr("CAM", "Edit holding tab")

    def makeTask(self, obj):
        return TaskPanel(obj)

    def onDelete(self, view, subelements):
        original = view.Object
        HoldingTab.invalidate_consumers(original)
        pending = [original]
        copies = []
        while pending:
            source = pending.pop()
            for candidate in original.Document.Objects:
                if (getattr(candidate, "SetupFrame", None)
                        and not hasattr(candidate, "PathResource")
                        and source in getattr(candidate, "Objects", [])
                        and candidate not in copies):
                    copies.append(candidate)
                    pending.append(candidate)
        for copy in reversed(copies):
            original.Document.removeObject(copy.Name)
        return True


class Command:
    def GetResources(self):
        return {"Pixmap": ":/icons/CAM_Tags.svg",
                "MenuText": tr("CAM", "Holding Tab"),
                "ToolTip": tr("CAM", "Creates a stock bridge preserved by Parallel and Waterline paths")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        from Path.Op.Util import findParentJob

        selected = Gui.Selection.getSelection()
        job = None
        for obj in selected:
            job = obj if hasattr(obj, "JobType") else findParentJob(obj)
            if job:
                break
        jobs = [obj for obj in App.ActiveDocument.Objects if hasattr(obj, "JobType")]
        if not job and len(jobs) == 1:
            job = jobs[0]
        if not job:
            App.Console.PrintError(tr("CAM", "Select the CAM Job for the holding tab.") + "\n")
            return
        if getattr(job, "SourceJob", None):
            while getattr(job, "SourceJob", None):
                job = job.SourceJob
            App.Console.PrintMessage(tr("CAM", "Creating a shared tab in the original setup coordinates.") + "\n")
        job.Document.openTransaction(tr("CAM", "Create holding tab"))
        try:
            tab = HoldingTab.create(job)
            Gui.activeDocument().setEdit(tab.Name)
        except Exception:
            job.Document.abortTransaction()
            raise


Gui.addCommand("CAM_HoldingTab", Command())
