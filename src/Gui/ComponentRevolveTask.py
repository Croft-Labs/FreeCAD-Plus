# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unified component Revolve create/edit task; shares the sketch curve collector."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui.ComponentExtrudeTask import ExtrudeTask, active_component
from freecad.gui.ComponentOperationTask import OperationTask

_task = None


def tr(text):
    return App.Qt.translate("ComponentRevolve", text)


class RevolveTask(OperationTask):
    operation_name = "Revolve"

    def __init__(self, component, operation=None, preset=None, context=None):
        import ComponentModel as Model
        import ComponentRevolve as Revolve
        self.backend = Revolve
        import ComponentProfile as Profile
        self.component, self.operation, self.context = component, operation, context
        self.ghost = self.result = self.mouse_callback = self.reference_pick = None
        self.observing, self.whole_profile = False, True
        self.profile_visibility, self.preview_transparency, self.preview_visibility = {}, {}, {}
        self.view = Gui.getDocument(component.Document.Name).activeView()
        outer = self.build_sections()
        main, dimensions, advanced, preview = [section[2] for section in self.sections]
        self.mode = self.combo(main, "Operation", [(name, name) for name in Revolve.MODES])
        self.target = self.combo(main, "Target body", [("Select a target body…", None)])
        for obj in Model.finished_results(component):
            if obj.Shape.Solids and (operation is None or operation not in obj.OutListRecursive):
                self.target.addItem(Model.display_object(obj).Label, obj.Name)
        self.build_profile_collector(main)
        self.sides = self.combo(main, "Mode", [("One angle", "One side"), ("Two angles", "Two sides"), ("Symmetric", "Symmetric")])
        self.extent = self.combo(main, "Type", [])
        self.extent2 = self.combo(main, "Side 2 type", [])
        self.axis = self.combo(dimensions, "Axis", [("Sketch vertical axis", "V_Axis"), ("Sketch horizontal axis", "H_Axis"), ("Reference axis", "Reference")])
        self.axis_reference, self.axis_row = self.reference_row(dimensions, "Axis reference")
        self.axis_reference.setPlaceholderText(tr("ObjectName.Edge1 or datum/origin axis"))
        self.angle, self.reverse, self.angle_row = self.angle_row_widget(dimensions, "Angle", 360., True)
        self.angle2, self.reverse2, self.angle2_row = self.angle_row_widget(dimensions, "Side 2 angle", 90., True)
        self.reverse.toggled.connect(self.reverse2.setChecked)
        self.reverse2.toggled.connect(self.reverse.setChecked)
        self.start = self.combo(dimensions, "Start", [(name, name) for name in ("Profile plane", "Offset", "Reference")])
        self.offset, self.offset_reverse, self.offset_row = self.angle_row_widget(dimensions, "Angular offset", 0., False)
        self.offset.setProperty("minimum", -360.)
        self.offset.valueChanged.connect(self.offset_changed)
        self.offset_reverse.clicked.connect(lambda: self.offset.setProperty("rawValue", -float(self.offset.property("rawValue"))))
        self.start.currentIndexChanged.connect(self.start_changed)
        self.start_reference, self.start_row = self.reference_row(dimensions, "Start reference")
        self.limit, self.limit_row = self.reference_row(advanced, "Limiting surface")
        self.limit2, self.limit_row2 = self.reference_row(advanced, "Side 2 limiting surface")
        self.project = QtWidgets.QCheckBox(tr("Project axis onto profile plane"))
        advanced.addRow(self.project)
        self.refine = QtWidgets.QCheckBox(tr("Refine result"))
        self.refine.setChecked(True)
        advanced.addRow(self.refine)
        self.auto_preview = QtWidgets.QCheckBox(tr("Recompute on change"))
        self.auto_preview.setChecked(True)
        preview.addRow(self.auto_preview)
        self.preview_mode = self.combo(preview, "Preview type", [(name, name) for name in ("None", "Overlay", "Result")])
        self.preview_mode.setCurrentIndex(1)
        self.preview_button = QtWidgets.QPushButton(tr("Update preview"))
        preview.addRow(self.preview_button)
        self.status = QtWidgets.QLabel()
        self.status.setTextFormat(QtCore.Qt.PlainText)
        self.status.setWordWrap(True)
        outer.addWidget(self.status)
        outer.addStretch()
        self.preview_timer = QtCore.QTimer(self.form)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.preview)
        self.profile.currentIndexChanged.connect(self.profile_changed)
        self.mode.setCurrentIndex(Revolve.MODES.index(preset) if preset in Revolve.MODES else 0)
        self.update_types()
        if operation:
            source, elements = Profile.selection(operation)
            self.profile.setCurrentIndex(self.profile.findData(source.Name))
            if elements is not None:
                self.set_curves(elements, False)
            self.mode.setCurrentIndex(Revolve.MODES.index(operation.RevolveMode))
            self.update_types()
            target = operation.BaseFeature
            if target:
                if self.target.findData(target.Name) < 0:
                    self.target.addItem(Model.display_object(target).Label, target.Name)
                self.target.setCurrentIndex(self.target.findData(target.Name))
            self.angle.setProperty("rawValue", operation.Angle.Value)
            self.reverse.setChecked(operation.Reversed)
            self.load_options(Revolve.read(operation))
        else:
            self.use_selection(context.profile_selection if context else None)
        for widget in (self.mode, self.target, self.sides, self.extent, self.extent2, self.axis, self.start, self.preview_mode):
            widget.currentIndexChanged.connect(self.changed)
        for widget in (self.angle, self.angle2, self.offset):
            widget.valueChanged.connect(self.changed)
        for widget in (self.reverse, self.project, self.refine, self.auto_preview):
            widget.toggled.connect(self.changed)
        self.preview_button.clicked.connect(self.preview)
        self.changed()

    def angle_row_widget(self, layout, label, value, checkable):
        row = QtWidgets.QWidget()
        box = QtWidgets.QHBoxLayout(row)
        box.setContentsMargins(0, 0, 0, 0)
        field = self.quantity(value, "deg")
        field.setProperty("minimum", 0.)
        field.setProperty("maximum", 360.)
        arrow = QtWidgets.QToolButton()
        arrow.setText("↔")
        arrow.setToolTip(tr("Reverse direction") if checkable else tr("Reverse offset"))
        arrow.setCheckable(checkable)
        box.addWidget(field)
        box.addWidget(arrow)
        layout.addRow(tr(label), row)
        return field, arrow, row

    def update_types(self):
        subtract = self.mode.currentData() == "Subtract"
        for field in (self.extent, self.extent2):
            value = field.currentData()
            field.blockSignals(True)
            field.clear()
            for text, data in (("Angle", "Angle"), ("Through all" if subtract else "To last", "ThroughAll" if subtract else "UpToLast"), ("To first", "UpToFirst"), ("Up to surface", "UpToFace")):
                field.addItem(tr(text), data)
            field.setCurrentIndex(max(0, field.findData(value)))
            field.blockSignals(False)

    def load_options(self, values):
        import ComponentExtent as Extent
        for field, key in ((self.sides, "sides"), (self.extent, "extent"), (self.extent2, "extent2"), (self.axis, "axis"), (self.start, "start")):
            field.setCurrentIndex(field.findData(values[key]))
        self.angle2.setProperty("rawValue", values["angle2"])
        self.offset.setProperty("rawValue", values["start_offset"])
        self.project.setChecked(values["project"])
        self.refine.setChecked(values["refine"])
        for field, key in ((self.axis_reference, "axis_reference"), (self.limit, "limit"), (self.limit2, "limit2"), (self.start_reference, "start_reference")):
            field.setText(Extent.reference_text(values[key]))

    def changed(self, *args):
        if not hasattr(self, "preview_timer"):
            return
        self.clear_preview()
        self.update_types()
        two = self.sides.currentData() == "Two sides"
        for layout, widget, visible in ((self.sections[0][2], self.target, self.mode.currentData() != "New Body"),
                (self.sections[0][2], self.extent2, two), (self.sections[1][2], self.angle2_row, two),
                (self.sections[1][2], self.axis_row, self.axis.currentData() == "Reference"),
                (self.sections[1][2], self.start_row, self.start.currentData() == "Reference"),
                (self.sections[2][2], self.limit_row, self.extent.currentData() == "UpToFace"),
                (self.sections[2][2], self.limit_row2, two and self.extent2.currentData() == "UpToFace")):
            widget.setVisible(visible)
            layout.labelForField(widget).setVisible(visible)
        self.angle.setEnabled(self.extent.currentData() == "Angle")
        self.angle2.setEnabled(self.extent2.currentData() == "Angle")
        self.reverse.setEnabled(self.sides.currentData() != "Symmetric")
        self.preview_button.setEnabled(self.preview_mode.currentData() != "None")
        self.preview_timer.stop()
        if self.auto_preview.isChecked() and self.preview_mode.currentData() != "None" and self.profile.currentData():
            self.preview_timer.start(300)
        self.status.setText(tr("Choose curves, an axis and an operation. Add and Subtract require a target body."))

    def offset_changed(self, *args):
        if float(self.offset.property("rawValue")) and self.start.currentData() == "Profile plane":
            self.start.setCurrentIndex(self.start.findData("Offset"))

    def start_changed(self, *args):
        if self.start.currentData() == "Profile plane":
            self.offset.setProperty("rawValue", 0.)

    def values(self):
        import ComponentExtent as Extent
        import ComponentRevolve as Revolve
        doc = self.component.Document
        profile = doc.getObject(self.profile.currentData()) if self.profile.currentData() else None
        if profile is None:
            raise ValueError(tr("Select a profile."))
        mode = self.mode.currentData()
        target = doc.getObject(self.target.currentData()) if mode != "New Body" and self.target.currentData() else None
        values = Revolve.defaults()
        values.update(sides=self.sides.currentData(), extent=self.extent.currentData(), extent2=self.extent2.currentData(),
                      angle2=float(self.angle2.property("rawValue")), axis=self.axis.currentData(), project=self.project.isChecked(),
                      start=self.start.currentData(), start_offset=float(self.offset.property("rawValue")), refine=self.refine.isChecked())
        for field, key, active in ((self.axis_reference, "axis_reference", values["axis"] == "Reference"),
                (self.limit, "limit", values["extent"] == "UpToFace"),
                (self.limit2, "limit2", values["sides"] == "Two sides" and values["extent2"] == "UpToFace"),
                (self.start_reference, "start_reference", values["start"] == "Reference")):
            if active:
                values[key] = Extent.reference(self.component, field.text())
                if key == "axis_reference" and values[key] and not values[key][1]:
                    values[key] = values[key][0], [""]
        elements = None if self.whole_profile else self.curve_names()
        return profile, float(self.angle.property("rawValue")), mode, target, self.reverse.isChecked(), elements, values

    def accept(self):
        import ComponentRevolve as Revolve
        self.preview_timer.stop()
        try:
            values = self.values()
            self.clear_preview()
            self.restore_profile_visibility()
            if self.operation:
                self.operation = Revolve.edit(self.operation, *values)
            else:
                self.operation, self.result = Revolve.create(self.component, *values)
        except Exception as error:
            self.status.setText(str(error))
            return False
        self.finish(committed=True)
        return True

    def finish(self, committed=False):
        global _task
        self.stop_selection()
        self.clear_preview()
        if not committed:
            self.restore_profile_visibility()
        Gui.Control.closeDialog()
        _task = None
        if self.context:
            self.context.restore()


def launch(preset=None, operation=None):
    global _task
    if Gui.Control.activeDialog():
        raise ValueError(tr("Finish the current task before starting Revolve."))
    import ComponentModel as Model
    from freecad.gui.ComponentNavigator import TaskContext
    component = Model.owner(operation) if operation else active_component()
    context = TaskContext(component)
    try:
        context.enter()
        _task = RevolveTask(component, operation, preset, context)
        Gui.Control.showDialog(_task)
        _task.start_selection()
    except Exception:
        if _task:
            _task.finish()
        else:
            context.restore()
        raise
    return _task
