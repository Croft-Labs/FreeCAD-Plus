# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unified primitive task with native dimensions and associative attachment."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.ComponentOperationTask import OperationTask
from freecad.gui.ComponentExtrudeTask import active_component

_task = None


def tr(text):
    return App.Qt.translate("ComponentPrimitive", text)


class PrimitiveTask(OperationTask):
    operation_name = "Primitive"

    def __init__(self, component, operation=None, preset=None, context=None, kind="Box"):
        import ComponentModel as Model
        import ComponentPrimitive as Primitive
        self.backend = Primitive
        self.component, self.operation, self.context = component, operation, context
        self.ghost = self.result = self.mouse_callback = self.reference_pick = None
        self.observing = False
        self.preview_transparency, self.preview_visibility = {}, {}
        self.view = Gui.getDocument(component.Document.Name).activeView()
        sections, mode, target, self.options = Primitive.read(operation) if operation else ([], preset or "New Body", None, Primitive.defaults(kind))
        outer = self.build_sections()
        outer.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        main, dimensions, advanced, preview = [section[2] for section in self.sections]
        self.mode = self.combo(main, "Operation", [(name, name) for name in Primitive.MODES])
        self.mode.setCurrentIndex(self.mode.findData(mode))
        self.target = self.combo(main, "Target body", [("Select a target body…", None)])
        for obj in Model.finished_results(component):
            if obj.Shape.Solids and (operation is None or operation not in obj.OutListRecursive):
                self.target.addItem(Model.display_object(obj).Label, obj.Name)
        if target:
            if self.target.findData(target.Name) < 0:
                self.target.addItem(Model.display_object(target).Label, target.Name)
            self.target.setCurrentIndex(self.target.findData(target.Name))
        self.kind = self.combo(main, "Shape", [(name, name) for name in Primitive.PARAMETERS])
        self.kind.setCurrentIndex(self.kind.findData(self.options["kind"]))
        self.fields = {}
        self.dimension_cache = {self.options["kind"]: dict(self.options["dimensions"])}
        self.current_kind = self.options["kind"]
        self.build_dimensions()
        engine = Primitive.attachment(self.options)
        modes = ["Deactivated"] + [name for name in engine.ImplementedModes if name != "Deactivated"]
        self.map_mode = self.combo(advanced, "Attachment", [(engine.getModeInfo(name)["UserFriendlyName"], name) for name in modes])
        self.map_mode.setCurrentIndex(self.map_mode.findData(self.options["map_mode"]))
        self.support = QtWidgets.QListWidget()
        self.support.setMaximumHeight(85)
        advanced.addRow(tr("References (ordered)"), self.support)
        for source, subs in self.options["support"]:
            for sub in subs or [""]:
                self.support.addItem(source.Name + ("." + sub if sub else ""))
        row = QtWidgets.QWidget()
        buttons = QtWidgets.QGridLayout(row)
        buttons.setContentsMargins(0, 0, 0, 0)
        for index, (label, callback) in enumerate((("Add selected", self.add_references), ("Remove", self.remove_reference), ("Clear", self.support.clear))):
            button = QtWidgets.QPushButton(tr(label))
            button.clicked.connect(callback)
            button.clicked.connect(self.changed)
            buttons.addWidget(button, index // 2, index % 2)
        advanced.addRow(row)
        self.support.setToolTip(tr("Select local faces, edges, vertices or datum/origin objects, then Add selected. Order defines the native attachment."))
        self.reverse = QtWidgets.QCheckBox(tr("Reverse attachment"))
        self.reverse.setChecked(self.options["reverse"])
        advanced.addRow(self.reverse)
        self.parameter = self.quantity(self.options["parameter"], "")
        advanced.addRow(tr("Path parameter"), self.parameter)
        self.placement_fields = {}
        self.placement_label = QtWidgets.QLabel()
        advanced.addRow(self.placement_label)
        for key, label, unit in (("x", "X", "mm"), ("y", "Y", "mm"), ("z", "Z", "mm"),
                                 ("yaw", "Yaw (Z)", "deg"), ("pitch", "Pitch (Y)", "deg"), ("roll", "Roll (X)", "deg")):
            field = self.quantity(0., unit)
            advanced.addRow(tr(label), field)
            self.placement_fields[key] = field
        self.current_map_mode = self.options["map_mode"]
        self.load_placement()
        self.boolean = self.combo(advanced, "Subtractive result", [("Subtraction", "Subtraction"), ("Common (keep intersection)", "Common")])
        self.boolean.setCurrentIndex(self.boolean.findData(self.options["boolean"]))
        self.refine = QtWidgets.QCheckBox(tr("Refine result"))
        self.refine.setChecked(self.options["refine"])
        advanced.addRow(self.refine)
        self.fuzzy = self.quantity(self.options["fuzzy"])
        self.fuzzy.setProperty("minimum", -1.)
        self.fuzzy.setProperty("maximum", 1.)
        advanced.addRow(tr("Fuzzy tolerance"), self.fuzzy)
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
        self.kind.currentIndexChanged.connect(self.kind_changed)
        self.map_mode.currentIndexChanged.connect(self.attachment_changed)
        for field in (self.mode, self.target, self.boolean, self.preview_mode):
            field.currentIndexChanged.connect(self.changed)
        for field in list(self.placement_fields.values()) + [self.parameter, self.fuzzy]:
            field.valueChanged.connect(self.changed)
        for field in (self.reverse, self.refine, self.auto_preview):
            field.toggled.connect(self.changed)
        self.preview_button.clicked.connect(self.preview)
        self.changed()

    def build_dimensions(self):
        layout = self.sections[1][2]
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        while layout.rowCount():
            layout.removeRow(0)
        self.fields = {}
        values = self.dimension_cache.get(self.kind.currentData(), self.backend.PARAMETERS[self.kind.currentData()])
        labels = {"FirstAngle": "X skew", "SecondAngle": "Y skew", "Polygon": "Sides", "Circumradius": "Circumradius",
                  "Angle1": "Lower angle", "Angle2": "Upper angle", "Angle3": "Sweep angle"}
        for key, value in values.items():
            field = self.quantity(value, "deg" if "Angle" in key else "" if key == "Polygon" else "mm")
            layout.addRow(tr(labels.get(key, key)), field)
            self.fields[key] = field
            field.valueChanged.connect(self.changed)
        layout.invalidate()
        self.sections[1][1].updateGeometry()

    def kind_changed(self, *args):
        self.dimension_cache[self.current_kind] = {key: float(field.property("rawValue")) for key, field in self.fields.items()}
        self.current_kind = self.kind.currentData()
        self.build_dimensions()
        self.changed()

    def load_placement(self):
        attached = self.current_map_mode != "Deactivated"
        placement = self.options["offset" if attached else "placement"]
        self.placement_label.setText(tr("Attachment offset" if attached else "Component-local placement"))
        for key, value in zip(self.placement_fields, list(placement.Base) + list(placement.Rotation.toEuler())):
            self.placement_fields[key].blockSignals(True)
            self.placement_fields[key].setProperty("rawValue", value)
            self.placement_fields[key].blockSignals(False)

    def save_placement(self):
        values = [float(field.property("rawValue")) for field in self.placement_fields.values()]
        self.options["offset" if self.current_map_mode != "Deactivated" else "placement"] = App.Placement(App.Vector(*values[:3]), App.Rotation(*values[3:]))

    def attachment_changed(self, *args):
        self.save_placement()
        self.current_map_mode = self.map_mode.currentData()
        self.load_placement()
        self.changed()

    def add_references(self):
        from freecad.gui import ComponentSelection as Selection
        import ComponentModel as Model
        for pick in Selection.selected(self.component, Gui.Selection.getSelectionEx("*", 0)):
            obj = pick.item
            if obj and not obj.isDerivedFrom("App::Origin") and (Model.owner(obj) == self.component or obj in self.component.Origin.OriginFeatures):
                text = obj.Name + ("." + pick.element if pick.element else "")
                if not self.support.findItems(text, QtCore.Qt.MatchExactly):
                    self.support.addItem(text)
        # Origin features are outside component.Group and do not have ObjectId.
        for entry in Gui.Selection.getSelectionEx("*", 0):
            for sub in entry.SubElementNames or [""]:
                obj = entry.Object.getSubObject(sub, 1) if sub else entry.Object
                if obj in self.component.Origin.OriginFeatures and not self.support.findItems(obj.Name, QtCore.Qt.MatchExactly):
                    self.support.addItem(obj.Name)
        self.changed()

    def remove_reference(self):
        for item in self.support.selectedItems():
            self.support.takeItem(self.support.row(item))

    def changed(self, *args):
        if not hasattr(self, "preview_timer"):
            return
        self.clear_preview()
        for layout, field, visible in ((self.sections[0][2], self.target, self.mode.currentData() != "New Body"),
                                      (self.sections[2][2], self.boolean, self.mode.currentData() == "Subtract")):
            field.setVisible(visible)
            layout.labelForField(field).setVisible(visible)
        self.preview_timer.stop()
        enabled = self.preview_mode.currentData() != "None"
        self.preview_button.setEnabled(enabled)
        if enabled and self.auto_preview.isChecked():
            self.preview_timer.start(300)
        self.status.setText(tr("Choose a shape and dimensions. Add/Subtract require an explicit target. Placement and attachment are in Advanced."))

    def values(self):
        self.save_placement()
        options = dict(self.options)
        doc = self.component.Document
        references = []
        for index in range(self.support.count()):
            parts = self.support.item(index).text().split(".", 1)
            references.append((doc.getObject(parts[0]), [parts[1] if len(parts) > 1 else ""]))
        options.update(kind=self.kind.currentData(), dimensions={key: float(field.property("rawValue")) for key, field in self.fields.items()},
                       map_mode=self.map_mode.currentData(), support=references, reverse=self.reverse.isChecked(),
                       parameter=float(self.parameter.property("rawValue")), refine=self.refine.isChecked(),
                       fuzzy=float(self.fuzzy.property("rawValue")), boolean=self.boolean.currentData())
        mode = self.mode.currentData()
        target = doc.getObject(self.target.currentData()) if mode != "New Body" and self.target.currentData() else None
        return [], mode, target, options

    def accept(self):
        self.preview_timer.stop()
        try:
            values = self.values()
            self.clear_preview()
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
        Gui.Control.closeDialog()
        _task = None
        if self.context:
            self.context.restore()


def launch(preset=None, operation=None, kind="Box"):
    global _task
    if Gui.Control.activeDialog():
        raise ValueError(tr("Finish the current task before starting Primitive."))
    import ComponentModel as Model
    from freecad.gui.ComponentNavigator import TaskContext
    component = Model.owner(operation) if operation else active_component()
    context = TaskContext(component)
    try:
        context.enter()
        _task = PrimitiveTask(component, operation, preset, context, kind)
        Gui.Control.showDialog(_task)
    except Exception:
        if _task:
            _task.finish()
        else:
            context.restore()
        raise
    return _task
