# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unified Helix task: native parameter modes, profile collector and shared preview."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.ComponentOperationTask import OperationTask
from freecad.gui.ComponentExtrudeTask import active_component

_task = None


def tr(text):
    return App.Qt.translate("ComponentHelix", text)


class HelixTask(OperationTask):
    operation_name = "Helix"

    def __init__(self, component, operation=None, preset=None, context=None):
        import ComponentModel as Model
        import ComponentHelix as Helix
        import ComponentExtent as Extent
        self.backend = Helix
        self.component, self.operation, self.context = component, operation, context
        self.ghost = self.result = self.mouse_callback = self.reference_pick = None
        self.observing, self.whole_profile = False, True
        self.profile_visibility, self.preview_transparency, self.preview_visibility = {}, {}, {}
        self.view = Gui.getDocument(component.Document.Name).activeView()
        outer = self.build_sections()
        main, dimensions, advanced, preview = [section[2] for section in self.sections]
        self.build_operation_controls(main, Helix.MODES)
        self.build_profile_collector(main)
        self.input_mode = self.combo(main, "Mode", [(name.title(), name) for name in Helix.INPUT_MODES])
        self.input_mode.setToolTip(tr("Choose the native independent parameters. Helix has no separate extent/termination type."))
        self.axis = self.combo(dimensions, "Axis", [("Sketch vertical axis", "V_Axis"), ("Sketch horizontal axis", "H_Axis"),
                                                    ("Sketch normal axis", "N_Axis"), ("Reference axis", "Reference")])
        for origin in component.Origin.OriginFeatures:
            if getattr(origin, "Role", "") in ("X_Axis", "Y_Axis", "Z_Axis"):
                self.axis.addItem(tr("Component ") + origin.Role[0] + tr(" axis"), "Origin:" + origin.Name)
        self.fixed_axis_count = self.axis.count()
        self.axis_reference, self.axis_row = self.reference_row(dimensions, "Axis reference")
        self.axis_reference.setPlaceholderText(tr("ObjectName.Edge1 or datum/origin axis"))
        self.fields = {}
        defaults = Helix.defaults()
        for key, title, unit in (("pitch", "Pitch", "mm"), ("height", "Height", "mm"), ("turns", "Turns", ""),
                                 ("angle", "Cone angle", "deg"), ("growth", "Radial growth per turn", "mm")):
            field = self.quantity(defaults[key], unit)
            field.setProperty("minimum", -89. if key == "angle" else -1e9 if key == "growth" else 0.)
            if key == "angle":
                field.setProperty("maximum", 89.)
            dimensions.addRow(tr(title), field)
            self.fields[key] = field
        self.reverse = QtWidgets.QToolButton()
        self.reverse.setText("↔")
        self.reverse.setCheckable(True)
        self.reverse.setToolTip(tr("Reverse axial direction; handedness is independent."))
        dimensions.addRow(tr("Reverse direction"), self.reverse)
        self.left = QtWidgets.QCheckBox(tr("Left handed"))
        dimensions.addRow(self.left)
        suggest = QtWidgets.QPushButton(tr("Suggest pitch and height from profile"))
        suggest.clicked.connect(self.suggest_dimensions)
        dimensions.addRow(suggest)
        self.boolean = self.combo(advanced, "Subtractive result", [("Subtraction", "Subtraction"), ("Common (keep intersection)", "Common")])
        self.refine = self.checkbox(advanced, "Refine result", True)
        self.tolerance = QtWidgets.QDoubleSpinBox()
        self.tolerance.setDecimals(4)
        self.tolerance.setRange(.1, 2147483647.)
        self.tolerance.setValue(.1)
        self.tolerance.setToolTip(tr("Native fusion tolerance factor, not a length."))
        advanced.addRow(tr("Fusion tolerance"), self.tolerance)
        self.fuzzy = self.fuzzy_tolerance(advanced)
        self.build_preview_controls(preview)
        self.build_status(outer)
        self.profile.currentIndexChanged.connect(self.profile_changed)
        self.profile.currentIndexChanged.connect(self.update_axes)
        self.mode.setCurrentIndex(Helix.MODES.index(preset) if preset in Helix.MODES else 0)
        if operation:
            sections, mode, target, values = Helix.read(operation)
            profile, elements = sections[0]
            self.profile.setCurrentIndex(self.profile.findData(profile.Name))
            if elements is not None:
                self.set_curves(elements, False)
            self.mode.setCurrentIndex(Helix.MODES.index(mode))
            if target:
                if self.target.findData(target.Name) < 0:
                    self.target.addItem(Model.display_object(target).Label, target.Name)
                self.target.setCurrentIndex(self.target.findData(target.Name))
            self.input_mode.setCurrentIndex(self.input_mode.findData(values["input_mode"]))
            self.axis.setCurrentIndex(self.axis.findData(values["axis"]))
            self.axis_reference.setText(Extent.reference_text(values["axis_reference"]) if values["axis"] == "Reference" else "")
            if values["axis"] == "Reference" and values["axis_reference"]:
                index = self.axis.findData("Origin:" + values["axis_reference"][0].Name)
                if index >= 0:
                    self.axis.setCurrentIndex(index)
            for key, field in self.fields.items():
                field.setProperty("rawValue", values[key])
            self.left.setChecked(values["left"])
            self.reverse.setChecked(values["reversed"])
            self.boolean.setCurrentIndex(self.boolean.findData(values["boolean"]))
            self.refine.setChecked(values["refine"])
            self.tolerance.setValue(values["tolerance"])
            self.fuzzy.setProperty("rawValue", values["fuzzy"])
        else:
            self.use_selection(context.profile_selection if context else None)
            if self.profile.currentData():
                self.suggest_dimensions()
        self.previous_input_mode = self.input_mode.currentData()
        self.input_mode.currentIndexChanged.connect(self.mode_changed)
        for field in (self.mode, self.target, self.axis, self.preview_mode):
            field.currentIndexChanged.connect(self.changed)
        for field in list(self.fields.values()) + [self.tolerance, self.fuzzy]:
            field.valueChanged.connect(self.changed)
        for field in (self.reverse, self.left, self.refine, self.auto_preview):
            field.toggled.connect(self.changed)
        self.preview_button.clicked.connect(self.preview)
        self.changed()

    def update_axes(self, *args):
        value = self.axis.currentData()
        self.axis.blockSignals(True)
        while self.axis.count() > self.fixed_axis_count:
            self.axis.removeItem(self.fixed_axis_count)
        profile = self.component.Document.getObject(self.profile.currentData() or "")
        for index in range(getattr(profile, "AxisCount", 0)):
            self.axis.addItem(tr("Construction axis ") + str(index + 1), "Axis" + str(index))
        self.axis.setCurrentIndex(max(0, self.axis.findData(value)))
        self.axis.blockSignals(False)
        self.changed()

    def suggest_dimensions(self):
        try:
            import ComponentModel as Model
            import ComponentProfile as Profile
            profile = self.component.Document.getObject(self.profile.currentData() or "")
            if profile is None:
                raise ValueError(tr("Choose a profile before requesting dimensions."))
            shape = Model.current_shape(profile) if self.whole_profile else Profile.face(profile, self.curve_names())
            pitch = 1.1 * shape.BoundBox.DiagonalLength
            self.fields["pitch"].setProperty("rawValue", pitch)
            self.fields["height"].setProperty("rawValue", 3 * pitch)
            self.fields["turns"].setProperty("rawValue", 3.)
            self.changed()
        except Exception as error:
            self.status.setText(str(error))

    def mode_changed(self, *args):
        values = self.backend.defaults()
        values.update({key: float(field.property("rawValue")) for key, field in self.fields.items()})
        values["input_mode"] = self.previous_input_mode
        try:
            values = self.backend.normalized(values)
            for key, field in self.fields.items():
                field.blockSignals(True)
                field.setProperty("rawValue", values[key])
                field.blockSignals(False)
        except ValueError:
            pass  # Keep invalid drafts for correction; never silently replace them.
        self.previous_input_mode = self.input_mode.currentData()
        self.changed()

    def changed(self, *args):
        if not hasattr(self, "preview_timer"):
            return
        self.clear_preview()
        mode = self.input_mode.currentData()
        for key, field in self.fields.items():
            visible = key in mode.split("-")
            field.setVisible(visible)
            self.sections[1][2].labelForField(field).setVisible(visible)
        for layout, field, visible in ((self.sections[0][2], self.target, self.mode.currentData() != "New Body"),
                (self.sections[1][2], self.axis_row, self.axis.currentData() == "Reference"),
                (self.sections[2][2], self.boolean, self.mode.currentData() == "Subtract")):
            field.setVisible(visible)
            layout.labelForField(field).setVisible(visible)
        self.preview_timer.stop()
        enabled = self.preview_mode.currentData() != "None"
        self.preview_button.setEnabled(enabled)
        if enabled and self.auto_preview.isChecked() and self.profile.currentData():
            self.preview_timer.start(300)
        self.status.setText(tr("Choose a profile, axis and parameter mode. Add/Subtract require an explicit target."))

    def values(self):
        import ComponentExtent as Extent
        doc = self.component.Document
        profile = doc.getObject(self.profile.currentData() or "")
        options = self.backend.defaults()
        options.update({key: float(field.property("rawValue")) for key, field in self.fields.items()})
        options.update(input_mode=self.input_mode.currentData(), axis=self.axis.currentData(), left=self.left.isChecked(),
                       reversed=self.reverse.isChecked(), refine=self.refine.isChecked(), tolerance=self.tolerance.value(),
                       fuzzy=float(self.fuzzy.property("rawValue")), boolean=self.boolean.currentData())
        if options["axis"] == "Reference":
            options["axis_reference"] = Extent.reference(self.component, self.axis_reference.text())
        elif options["axis"].startswith("Origin:"):
            options["axis_reference"] = doc.getObject(options["axis"].split(":", 1)[1]), [""]
            options["axis"] = "Reference"
        mode = self.mode.currentData()
        target = doc.getObject(self.target.currentData()) if mode != "New Body" and self.target.currentData() else None
        return [(profile, None if self.whole_profile else self.curve_names())], mode, target, options

    def accept(self):
        self.preview_timer.stop()
        try:
            values = self.values()
            self.clear_preview()
            self.restore_profile_visibility()
            if self.operation:
                self.operation = self.backend.edit(self.operation, *values)
            else:
                self.operation, self.result = self.backend.create(self.component, *values)
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
        raise ValueError(tr("Finish the current task before starting Helix."))
    import ComponentModel as Model
    from freecad.gui.ComponentNavigator import TaskContext
    component = Model.owner(operation) if operation else active_component()
    context = TaskContext(component)
    try:
        context.enter(operation)
        _task = HelixTask(component, operation, preset, context)
        Gui.Control.showDialog(_task)
        _task.start_selection()
    except Exception:
        if _task:
            _task.finish()
        else:
            context.restore()
        raise
    return _task
