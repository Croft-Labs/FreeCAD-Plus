# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Extrude creation/edit task with explicit profile and target choices."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.OccurrenceMove import Ghost
from freecad.gui.ComponentTaskWidgets import (CompactFormLayout, CurveListWidget,
                                              ModelingTaskUI, CurveSelection)

_task = None


def tr(text):
    return App.Qt.translate("ComponentExtrude", text)


def modeling_component(component):
    """Validate explicit task destinations as well as the active view's owner."""
    import ComponentModel as Model
    if not Model.is_component(component) or Model.is_file_container(component):
        raise ValueError(tr("Edit or create a component before starting a modeling command."))
    return component


def active_component(allow_file=False):
    import ComponentModel as Model
    doc = App.ActiveDocument
    if doc is None:
        raise ValueError(tr("Create or open a component document first."))
    view = Gui.activeDocument().activeView()
    component = view.getActiveObject("part") if hasattr(view, "getActiveObject") else None
    component = component if Model.is_component(component) else Model.metadata(doc).RootComponent
    return component if allow_file else modeling_component(component)


class ExtrudeTask(ModelingTaskUI, CurveSelection):
    def __init__(self, component, operation=None, preset=None, context=None):
        import ComponentModel as Model
        import ComponentExtrude as Extrude
        self.backend = Extrude
        self.component, self.operation = component, operation
        self.context = context
        self.ghost = None
        self.result = None
        self.whole_profile = True
        self.observing = False
        self.mouse_callback = None
        self.profile_visibility = {}
        self.region_visibility = {}
        self.reference_pick = None
        self.preview_transparency = {}
        self.preview_visibility = {}
        self.view = Gui.getDocument(component.Document.Name).activeView()
        Model.activate(component, strict=False)
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("Extrude"))
        layout = CompactFormLayout(self.form)
        self.mode = self.combo(layout, "Operation", [(name, name) for name in Extrude.MODES])
        self.build_profile_collector(layout)
        self.build_target_control(layout)
        self.length = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
        self.length.setProperty("unit", "mm")
        self.length.setProperty("minimum", 0.001)
        self.length.setProperty("maximum", 1e9)
        self.length.setProperty("rawValue", 10.0)
        layout.addRow(tr("Length"), self.length)
        self.reverse = QtWidgets.QCheckBox(tr("Reverse direction"))
        layout.addRow(self.reverse)
        self.build_extents(layout)
        self.build_preview_controls(layout)
        self.build_status(layout)
        self.status.setText(tr("Choose a profile. No Body container is required."))
        self.profile.currentIndexChanged.connect(self.profile_changed)
        if preset in Extrude.MODES:
            self.mode.setCurrentIndex(Extrude.MODES.index(preset))
        if operation:
            tool, mode, target = Extrude.parameters(operation)
            import ComponentProfile as Profile
            source, elements = Profile.selection(tool)
            self.profile.setCurrentIndex(self.profile.findData(source.Name))
            if elements is not None:
                self.set_curves(elements, False)
            self.length.setProperty("rawValue", tool.Length.Value if tool.TypeId in ("PartDesign::Pad", "PartDesign::Pocket") else tool.LengthFwd.Value)
            self.load_extents(tool)
            self.reverse.setChecked(Extrude.reversed_direction(tool))
            self.mode.setCurrentIndex(Extrude.MODES.index(mode))
            if target:
                if self.target.findData(target.Name) < 0:
                    self.target.addItem(Model.display_object(target).Label, target.Name)
                self.target.setCurrentIndex(self.target.findData(target.Name))
        else:
            self.use_selection(context.profile_selection if context else None)
        self.preview_button.clicked.connect(self.preview)
        self.mode.currentIndexChanged.connect(self.changed)
        self.target.currentIndexChanged.connect(self.changed)
        self.length.valueChanged.connect(self.changed)
        self.reverse.toggled.connect(self.changed)
        self.auto_preview.toggled.connect(self.changed)
        self.preview_mode.currentIndexChanged.connect(self.changed)
        self.changed()

    def getStandardButtons(self):
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        return getattr(buttons, "value", buttons)

    def begin_reference_pick(self, field):
        self.reference_pick = field
        self.status.setText(tr("Pick a local limiting face, plane or shape. Profile collection is paused for this pick."))

    def build_extents(self, layout):
        import ComponentExtent as Extent
        self.sides = QtWidgets.QComboBox()
        for label, value in (("One dimension", "One side"), ("Two dimensions", "Two sides"), ("Symmetric", "Symmetric")):
            self.sides.addItem(tr(label), value)
        layout.addRow(tr("Sides"), self.sides)
        self.extent, self.extent2 = QtWidgets.QComboBox(), QtWidgets.QComboBox()
        for label, value in Extent.TYPES:
            self.extent.addItem(tr(label), value)
            self.extent2.addItem(tr(label), value)
        layout.addRow(tr("Type"), self.extent)
        self.limit, self.limit_row = self.reference_row(layout, "Limiting surface / shape")
        self.offset = self.quantity()
        self.offset.setToolTip(tr("Offset from the limiting surface; positive extends farther along side 1."))
        layout.addRow(tr("Offset"), self.offset)
        self.taper = self.quantity(unit="deg")
        layout.addRow(tr("Taper angle"), self.taper)
        layout.addRow(tr("Side 2 type"), self.extent2)
        self.length2 = self.quantity(10.)
        layout.addRow(tr("Side 2 length"), self.length2)
        self.limit2, self.limit_row2 = self.reference_row(layout, "Side 2 limiting surface / shape")
        self.offset2 = self.quantity()
        self.offset2.setToolTip(tr("Offset from the limiting surface; positive extends farther along side 2."))
        layout.addRow(tr("Side 2 offset"), self.offset2)
        self.taper2 = self.quantity(unit="deg")
        layout.addRow(tr("Side 2 taper angle"), self.taper2)
        self.start = QtWidgets.QComboBox()
        for label in ("Profile plane", "Offset", "Reference"):
            self.start.addItem(tr(label), label)
        layout.addRow(tr("Start"), self.start)
        self.start_offset = self.quantity()
        self.start_offset.setToolTip(tr("Signed offset from the profile plane or start reference along the extrusion direction."))
        layout.addRow(tr("Start offset"), self.start_offset)
        self.start_reference, self.start_row = self.reference_row(layout, "Start reference")
        self.custom = QtWidgets.QCheckBox(tr("Custom direction"))
        layout.addRow(self.custom)
        row = QtWidgets.QWidget()
        box = CompactFormLayout(row)
        box.setContentsMargins(0, 0, 0, 0)
        self.direction = []
        for label, value in (("X", 0.), ("Y", 0.), ("Z", 1.)):
            widget = QtWidgets.QDoubleSpinBox()
            widget.setRange(-1e6, 1e6)
            widget.setDecimals(6)
            widget.setValue(value)
            box.addRow(label, widget)
            self.direction.append(widget)
        self.direction_row = row
        layout.addRow(tr("Direction vector"), row)
        self.along_normal = QtWidgets.QCheckBox(tr("Length along sketch normal"))
        self.along_normal.setChecked(True)
        layout.addRow(self.along_normal)
        self.refine = self.checkbox(layout, "Refine result", True)
        for widget in (self.sides, self.extent, self.extent2, self.start):
            widget.currentIndexChanged.connect(self.changed)
        for widget in (self.offset, self.offset2, self.taper, self.taper2, self.length2, self.start_offset, *self.direction):
            widget.valueChanged.connect(self.changed)
        for widget in (self.custom, self.along_normal, self.refine):
            widget.toggled.connect(self.changed)

    def load_extents(self, tool):
        import ComponentExtent as Extent
        values = Extent.read(tool)
        for widget, key in ((self.sides, "sides"), (self.extent, "extent"), (self.extent2, "extent2"), (self.start, "start")):
            widget.setCurrentIndex(widget.findData(values[key]))
        for widget, key in ((self.length2, "length2"), (self.offset, "offset"), (self.offset2, "offset2"),
                            (self.taper, "taper"), (self.taper2, "taper2"), (self.start_offset, "start_offset")):
            widget.setProperty("rawValue", values[key])
        for widget, key in ((self.limit, "limit"), (self.limit2, "limit2"), (self.start_reference, "start_reference")):
            widget.setText(Extent.reference_text(values[key]))
        self.custom.setChecked(values["custom"])
        self.along_normal.setChecked(values["along_normal"])
        self.refine.setChecked(values["refine"])
        for widget, value in zip(self.direction, values["direction"]):
            widget.setValue(value)

    def extent_options(self):
        import ComponentExtent as Extent
        values = Extent.defaults()
        values.update(sides=self.sides.currentData(), extent=self.extent.currentData(), extent2=self.extent2.currentData(),
                      start=self.start.currentData(), custom=self.custom.isChecked(),
                      direction=tuple(widget.value() for widget in self.direction),
                      along_normal=self.along_normal.isChecked(), refine=self.refine.isChecked())
        for widget, key in ((self.length2, "length2"), (self.offset, "offset"), (self.offset2, "offset2"),
                            (self.taper, "taper"), (self.taper2, "taper2"), (self.start_offset, "start_offset")):
            values[key] = float(widget.property("rawValue"))
        if values["extent"] in ("UpToFace", "UpToShape"):
            values["limit"] = Extent.reference(self.component, self.limit.text())
        if values["sides"] == "Two sides" and values["extent2"] in ("UpToFace", "UpToShape"):
            values["limit2"] = Extent.reference(self.component, self.limit2.text())
        if values["start"] == "Reference":
            values["start_reference"] = Extent.reference(self.component, self.start_reference.text())
        return values

    def changed(self, *args):
        if not hasattr(self, "status"):
            return
        self.clear_preview()
        two = self.sides.currentData() == "Two sides"
        layout = self.form.layout()
        layout.labelForField(self.length).setText(tr("Total length") if self.sides.currentData() == "Symmetric" else tr("Side 1 length") if two else tr("Length"))
        for widget in (self.extent2, self.length2, self.limit_row2, self.offset2, self.taper2):
            widget.setVisible(two)
            label = layout.labelForField(widget)
            if label:
                label.setVisible(two)
        self.length.setEnabled(self.extent.currentData() == "Length")
        self.length.setToolTip(tr("Total span, half on each side") if self.sides.currentData() == "Symmetric" else tr("Side 1 length"))
        self.limit_row.setEnabled(self.extent.currentData() in ("UpToFace", "UpToShape"))
        self.offset.setEnabled(self.extent.currentData() in ("UpToFace", "UpToShape", "UpToFirst", "UpToLast"))
        self.extent2.setEnabled(two)
        self.length2.setEnabled(two and self.extent2.currentData() == "Length")
        self.limit_row2.setEnabled(two and self.extent2.currentData() in ("UpToFace", "UpToShape"))
        self.offset2.setEnabled(two and self.extent2.currentData() in ("UpToFace", "UpToShape", "UpToFirst", "UpToLast"))
        self.taper2.setEnabled(two)
        self.start_offset.setEnabled(self.start.currentData() != "Profile plane")
        self.start_row.setEnabled(self.start.currentData() == "Reference")
        self.direction_row.setEnabled(self.custom.isChecked())
        self.along_normal.setEnabled(self.custom.isChecked())
        if self.auto_preview.isChecked() and self.profile.currentData() and self.preview_mode.currentData() != "None":
            self.preview_timer.start(300)
        else:
            self.preview_timer.stop()
        self.target.setEnabled(self.mode.currentData() != "New Body")
        if not self.profile.currentData():
            self.status.setText(tr("Choose a profile. No Body container is required."))
        elif self.mode.currentData() != "New Body" and not self.target.currentData():
            self.status.setText(tr("Choose the body to add to or subtract from."))
        else:
            self.status.setText(tr("Select curves from one sketch, or click a closed region. Preview and OK require one connected region with optional holes."))


    def clear_preview(self):
        if self.ghost:
            self.ghost.remove()
            self.ghost = None
        for name, transparency in self.preview_transparency.items():
            target = self.component.Document.getObject(name)
            if target:
                target.ViewObject.Transparency = transparency
        self.preview_transparency.clear()
        for name, visible in self.preview_visibility.items():
            obj = self.component.Document.getObject(name)
            if obj:
                obj.Visibility = visible
        self.preview_visibility.clear()


    def values(self):
        doc = self.component.Document
        profile = doc.getObject(self.profile.currentData()) if self.profile.currentData() else None
        if profile is None:
            raise ValueError(tr("Select a profile in the active component."))
        mode = self.mode.currentData()
        target = doc.getObject(self.target.currentData()) if self.target.currentData() and mode != "New Body" else None
        length = float(self.length.property("rawValue"))
        elements = self.curve_names() if profile.isDerivedFrom("Sketcher::SketchObject") else None
        return profile, length, mode, target, self.reverse.isChecked(), elements, self.extent_options()

    def preview(self):
        import ComponentModel as Model
        self.clear_preview()
        if self.preview_mode.currentData() == "None":
            return True
        try:
            final = self.preview_mode.currentData() == "Result"
            shape = self.backend.preview(self.component, *self.values(), tool_only=not final)
            shape.Placement = self.component.getGlobalPlacement().multiply(shape.Placement)
            target = None
            if self.mode.currentData() != "New Body" and self.target.currentData():
                target = Model.display_object(self.component.Document.getObject(self.target.currentData()))
            color = {"New Body": (0., 0., 1.), "Add": (0., 1., 0.), "Subtract": (1., 0., 0.)}[self.mode.currentData()]
            transparency = 0.5
            if final:
                appearance = self.operation or target
                if appearance:
                    color = tuple(appearance.ViewObject.ShapeColor[:3])
                    transparency = appearance.ViewObject.Transparency / 100.
                else:
                    packed = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned("DefaultShapeColor", 0xCCCCCCFF)
                    color = tuple(((packed >> shift) & 255) / 255. for shift in (24, 16, 8))
                    transparency = 0.
            self.ghost = Ghost(shape, color=color, filled=True, transparency=transparency)
            targets = [target] if target else []
            if self.operation:
                targets.append(self.operation)
                targets.extend(Model.display_object(obj) for obj in self.operation.InList
                               if getattr(obj, "Producer", None) == self.operation)
            for obj in set(targets):
                self.preview_visibility[obj.Name] = bool(obj.Visibility)
                if final or obj == self.operation:
                    obj.Visibility = False
                else:
                    obj.Visibility = True
                    self.preview_transparency[obj.Name] = obj.ViewObject.Transparency
                    obj.ViewObject.Transparency = max(75, obj.ViewObject.Transparency)
            self.status.setText(tr("Result preview ready. OK creates or updates the operation.") if final else
                                tr("Tool overlay ready. OK validates the target and final result."))
            return True
        except Exception as error:
            self.clear_preview()
            self.status.setText(str(error))
            return False

    def accept(self):
        import ComponentExtrude as Extrude
        try:
            profile, length, mode, target, reverse, elements, options = self.values()
            self.clear_preview()
            self.restore_profile_visibility()
            if self.operation:
                self.operation = Extrude.edit(self.operation, profile, length, reverse, mode, target, elements, options)
            else:
                self.operation, self.result = Extrude.create(self.component, profile, length, mode, target, reverse, elements, options)
        except Exception as error:
            if self.profile.currentData():
                source = self.component.Document.getObject(self.profile.currentData())
                if source:
                    source.Visibility = True
            self.status.setText(str(error))
            return False
        self.finish(committed=True)
        return True

    def reject(self):
        self.finish()
        return True

    def finish(self, committed=False):
        global _task
        self.stop_selection()
        self.preview_timer = None
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
        raise ValueError(tr("Finish the current task before starting Extrude."))
    import ComponentModel as Model
    from freecad.gui.ComponentNavigator import TaskContext
    component = Model.owner(operation) if operation else active_component()
    context = TaskContext(component)
    try:
        context.enter(operation)
        _task = ExtrudeTask(component, operation, preset, context)
        Gui.Control.showDialog(_task)
        _task.start_selection()
    except Exception:
        if _task:
            _task.stop_selection()
            _task.restore_profile_visibility()
            Gui.Control.closeDialog()
        _task = None
        context.restore()
        raise
    return _task
